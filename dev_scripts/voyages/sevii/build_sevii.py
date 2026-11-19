#!/usr/bin/env python3
"""
Wavebreak Voyages, Sevii stream: turn the frlg_translate export into real, registered maps.

  1. run the export first:  <venv python> dev_scripts/voyages/sevii/frlg_translate.py export --out DIR
  2. then:                  python3 dev_scripts/voyages/sevii/build_sevii.py DIR

Idempotent (re-run after re-exporting). What it writes:
  data/tilesets/secondary/sevii_islands/   gTileset_SeviiIslands (headers/graphics/metatiles/tilesets.h entries,
                                            metatile labels, Rustboro anim callback, field_door.c entries + the
                                            Rocket Warehouse door anim graphics/door_anims/sevii_rocket_warehouse.png)
  data/layouts/<Folder>/, layouts.json      FRLG layout ids replaced in place (layout_version emerald), new ids appended
  data/maps/<Map>/                          map.json + scripts.pory for every Sevii map, Centre/Mart/Game Corner clones
  data/maps/map_groups.json                 gMapGroup_Sevii (rewritten as a whole; group appended once)
  data/event_scripts.s                      the "@ sevii-maps" include block
  src/data/heal_locations.json              HEAL_LOCATION_<ISLAND> entries updated in place
  include/constants/flags.h, vars.h         visited flags, reused item / hidden-item flags (+ aliases), shop var
  region_map_sections.json + aliases        Sevii names, the four straits renamed
  src/data/wild_encounters.json             gSevii_* tables (Emerald)
  include/constants/sevii.h                 arrival point + ferry constants
Switches for the open questions are the CONFIG dict below.
"""
import copy
import glob
import json
import os
import re
import shutil
import struct
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mtattr as MA          # noqa: E402
import sevii_text as TX      # noqa: E402
import reach_flags as RF     # noqa: E402

ROOT = MA.ROOT
P = MA.P
GROUP = "gMapGroup_Sevii"
MARK = "@ sevii-maps"

CONFIG = {
    "seal_dotted_hole": True,        # Ruin Valley's dotted door: impassable + sign (maps stay built and linked)
    "seal_tanoby_chambers": True,    # the 7 chamber doors on Tanoby Ruins: same
    "stall_price_multiplier": 3,     # Two Island market stall (VAR_SHOP_PRICE_MULTIPLIER)
    "villain_gfx": "AQUA",           # FRLG Rocket -> Team Aqua sprites (export_maps.EXPORT_SWAP)
}

ISLANDS = [  # const, folder, harbour map folder, harbour section, music
    ("ONE_ISLAND", "OneIsland", "OneIsland_Harbor"),
    ("TWO_ISLAND", "TwoIsland", "TwoIsland_Harbor"),
    ("THREE_ISLAND", "ThreeIsland", "ThreeIsland_Harbor"),
    ("FOUR_ISLAND", "FourIsland", "FourIsland_Harbor"),
    ("FIVE_ISLAND", "FiveIsland", "FiveIsland_Harbor"),
    ("SIX_ISLAND", "SixIsland", "SixIsland_Harbor"),
    ("SEVEN_ISLAND", "SevenIsland", "SevenIsland_Harbor"),
]
HARBOUR_NAME = {"OneIsland_Harbor": "One Island", "TwoIsland_Harbor": "Two Island",
                "ThreeIsland_Harbor": "Three Isle Port", "FourIsland_Harbor": "Four Island",
                "FiveIsland_Harbor": "Five Island", "SixIsland_Harbor": "Six Island",
                "SevenIsland_Harbor": "Seven Island"}
CLUSTER = {"OneIsland_Harbor": 1, "TwoIsland_Harbor": 1, "ThreeIsland_Harbor": 1, "FourIsland_Harbor": 2,
           "FiveIsland_Harbor": 2, "SixIsland_Harbor": 3, "SevenIsland_Harbor": 3}
HARBOUR_LAND = (8, 4)          # IslandHarbor: the dock cell in front of the sailor (8,5); boat at (8,7)

MARTS = {"ThreeIsland", "FourIsland", "SixIsland", "SevenIsland"}
SEA_ROUTE_SEC = {"SeviiSeaRouteA": "MAPSEC_ONE_TWO_STRAIT", "SeviiSeaRouteB": "MAPSEC_TWO_THREE_STRAIT",
                 "SeviiSeaRouteC": "MAPSEC_FOUR_FIVE_STRAIT", "SeviiSeaRouteD": "MAPSEC_SIX_SEVEN_STRAIT"}
SEC_RENAMES = {"MAPSEC_SEVII_ISLE_22": "MAPSEC_ONE_TWO_STRAIT", "MAPSEC_SEVII_ISLE_23": "MAPSEC_TWO_THREE_STRAIT",
               "MAPSEC_SEVII_ISLE_24": "MAPSEC_FOUR_FIVE_STRAIT", "MAPSEC_THREE_ISLE_PATH": "MAPSEC_SIX_SEVEN_STRAIT"}
SEC_NAMES = {
    "MAPSEC_ONE_ISLAND": "One Island", "MAPSEC_TWO_ISLAND": "Two Island", "MAPSEC_THREE_ISLAND": "Three Island",
    "MAPSEC_FOUR_ISLAND": "Four Island", "MAPSEC_FIVE_ISLAND": "Five Island", "MAPSEC_SIX_ISLAND": "Six Island",
    "MAPSEC_SEVEN_ISLAND": "Seven Island", "MAPSEC_KINDLE_ROAD": "Kindle Road",
    "MAPSEC_TREASURE_BEACH": "Treasure Beach", "MAPSEC_CAPE_BRINK": "Cape Brink", "MAPSEC_BOND_BRIDGE": "Bond Bridge",
    "MAPSEC_THREE_ISLE_PORT": "Three Isle Port", "MAPSEC_FIVE_ISLE_MEADOW": "Five Isle Meadow",
    "MAPSEC_MEMORIAL_PILLAR": "Memorial Pillar", "MAPSEC_WATER_PATH": "Water Path", "MAPSEC_RUIN_VALLEY": "Ruin Valley",
    "MAPSEC_CANYON_ENTRANCE": "Canyon Entrance", "MAPSEC_SEVAULT_CANYON": "Sevault Canyon",
    "MAPSEC_TANOBY_RUINS": "Tanoby Ruins", "MAPSEC_MT_EMBER": "Mt. Ember", "MAPSEC_BERRY_FOREST": "Berry Forest",
    "MAPSEC_ICEFALL_CAVE": "Icefall Cave", "MAPSEC_ROCKET_WAREHOUSE": "Warehouse", "MAPSEC_DOTTED_HOLE": "Dotted Hole",
    "MAPSEC_TANOBY_KEY": "Tanoby Key", "MAPSEC_MONEAN_CHAMBER": "Monean Chamber",
    "MAPSEC_LIPTOO_CHAMBER": "Liptoo Chamber", "MAPSEC_WEEPTH_CHAMBER": "Weepth Chamber",
    "MAPSEC_DILFORD_CHAMBER": "Dilford Chamber", "MAPSEC_SCUFIB_CHAMBER": "Scufib Chamber",
    "MAPSEC_RIXY_CHAMBER": "Rixy Chamber", "MAPSEC_VIAPOIS_CHAMBER": "Viapois Chamber", "MAPSEC_EMBER_SPA": "Ember Spa",
    "MAPSEC_ONE_TWO_STRAIT": "One-Two Strait", "MAPSEC_TWO_THREE_STRAIT": "Two-Three Strait",
    "MAPSEC_FOUR_FIVE_STRAIT": "Four-Five Strait", "MAPSEC_SIX_SEVEN_STRAIT": "Six-Seven Strait",
}
LAYOUT_FOLDER_RENAME = {"House3": "SeviiHouse3", "House4": "SeviiHouse4"}   # Emerald already has data/layouts/House3

DOLL_SWAP = {"WIGGLYTUFF": "CLEFAIRY_DOLL", "SEEL": "MARILL_DOLL", "SLOWPOKE": "AZURILL_DOLL", "SLOWBRO": "DITTO_DOLL",
             "PSYDUCK": "TOGEPI_DOLL", "CHANSEY": "SMOOCHUM_DOLL", "NIDORAN_F": "SKITTY_DOLL",
             "NIDORAN_M": "WYNAUT_DOLL", "PIDGEOT": "SWABLU_DOLL", "FEAROW": "PICHU_DOLL"}
DROP_GFX = ("RUBY", "SAPPHIRE", "VAR_0", "OBJ_EVENT_GFX_BLUE", "MOLTRES")
DROP_OBJECTS = {"FourIsland_IcefallCave_Back"}                  # Lorelei + grunts story scene: all objects
ITEM_FIX = {"ITEM_HM07": "ITEM_ICE_STONE", "ITEM_UP_GRADE": "ITEM_UPGRADE"}
MART_STOCK = ["ITEM_ULTRA_BALL", "ITEM_GREAT_BALL", "ITEM_FULL_RESTORE", "ITEM_MAX_POTION", "ITEM_HYPER_POTION",
              "ITEM_REVIVE", "ITEM_FULL_HEAL", "ITEM_MAX_REPEL", "ITEM_ESCAPE_ROPE", "ITEM_X_ATTACK"]
STALL_STOCK = ["ITEM_ABILITY_CAPSULE", "ITEM_ABILITY_PATCH", "ITEM_BOTTLE_CAP", "ITEM_GOLD_BOTTLE_CAP", "ITEM_PP_MAX",
               "ITEM_RARE_CANDY", "ITEM_EXP_CANDY_XL", "ITEM_LUCKY_EGG", "ITEM_DESTINY_KNOT", "ITEM_ADAMANT_MINT",
               "ITEM_JOLLY_MINT", "ITEM_MODEST_MINT", "ITEM_TIMID_MINT", "ITEM_LINKING_CORD", "ITEM_DUSK_STONE",
               "ITEM_SHINY_STONE", "ITEM_DAWN_STONE", "ITEM_ICE_STONE", "ITEM_RAZOR_CLAW", "ITEM_RAZOR_FANG",
               "ITEM_KINGS_ROCK", "ITEM_METAL_COAT", "ITEM_PRISM_SCALE", "ITEM_PROTECTOR", "ITEM_ELECTIRIZER",
               "ITEM_MAGMARIZER", "ITEM_REAPER_CLOTH", "ITEM_DUBIOUS_DISC", "ITEM_UPGRADE", "ITEM_DRAGON_SCALE"]


def jload(p):
    return json.load(open(p), object_pairs_hook=OrderedDict)


def jdump(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def snake(name):
    s = re.sub(r"(?<=[a-z])(?=[A-Z0-9])", "_", name)
    s = re.sub(r"(?<=[0-9])(?=[A-Z][a-z])", "_", s)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    return s.upper().replace("__", "_")


def mapconst(folder):
    return "MAP_" + snake(folder)


def esc(t):
    return t.replace('"', "'")


# ------------------------------------------------------------------ tileset
def install_tileset(ex):
    src = os.path.join(ex, "tilesets", "sevii_islands")
    dst = P("data", "tilesets", "secondary", "sevii_islands")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("labels.json"))
    labels = json.load(open(os.path.join(src, "labels.json")))["labels"]
    d = open(os.path.join(dst, "metatiles.bin"), "rb").read()
    ents = struct.unpack("<%dH" % (len(d) // 2), d)
    num_tiles = max((e & 0x3FF) - 512 for e in ents if (e & 0x3FF) >= 512) + 1
    num_tiles = max(num_tiles, 452)                  # Rustboro anim destinations end at 451

    def add_block(path, marker, block, before=None):
        txt = open(path).read()
        txt = re.sub(r"\n// %s begin.*?// %s end\n" % (marker, marker), "\n", txt, flags=re.S)
        block = "\n// %s begin\n%s// %s end\n" % (marker, block, marker)
        if before:
            i = txt.rindex(before)
            txt = txt[:i] + block.lstrip("\n") + "\n" + txt[i:]
        else:
            txt = txt.rstrip("\n") + "\n" + block
        open(path, "w").write(txt)

    pal = "".join('    INCGFX_U16("data/tilesets/secondary/sevii_islands/palettes/%02d.pal", ".gbapal"),\n' % i
                  for i in range(16))
    add_block(P("src", "data", "tilesets", "graphics.h"), "Sevii Islands",
              'const u32 gTilesetTiles_SeviiIslands[] = INCGFX_U32("data/tilesets/secondary/sevii_islands/tiles.png", '
              '".4bpp.fastSmol", "-num_tiles %d -Wnum_tiles");\n\nconst u16 gTilesetPalettes_SeviiIslands[][16] =\n{\n%s};\n'
              % (num_tiles, pal))
    add_block(P("src", "data", "tilesets", "metatiles.h"), "Sevii Islands",
              'const u16 gMetatiles_SeviiIslands[] = INCBIN_U16("data/tilesets/secondary/sevii_islands/metatiles.bin");\n'
              'const u16 gMetatileAttributes_SeviiIslands[] = INCBIN_U16("data/tilesets/secondary/sevii_islands/'
              'metatile_attributes.bin");\n')
    add_block(P("src", "data", "tilesets", "headers.h"), "Sevii Islands",
              "// Sevii Islands (Wavebreak Voyages): Sevii-only copy of gTileset_Rustboro (same metatile ids, city-only\n"
              "// metatiles blanked) plus cottages, market stall, Onix tails, Memorial Pillar, Dotted Hole, Rocket\n"
              "// Warehouse and arrow-warp duplicates (dev_scripts/voyages/sevii). Keeps Rustboro's animations.\n"
              "const struct Tileset gTileset_SeviiIslands =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
              "    .tiles = gTilesetTiles_SeviiIslands,\n    .palettes = gTilesetPalettes_SeviiIslands,\n"
              "    .metatiles = gMetatiles_SeviiIslands,\n    .metatileAttributes = gMetatileAttributes_SeviiIslands,\n"
              "    .callback = InitTilesetAnim_Rustboro,\n};\n")
    add_block(P("include", "tilesets.h"), "Sevii Islands", "extern const struct Tileset gTileset_SeviiIslands;\n",
              before="#endif")
    lab = "".join("#define METATILE_SeviiIslands_%-32s %s\n" % (k, v) for k, v in sorted(labels.items()))
    add_block(P("include", "constants", "metatile_labels.h"), "Sevii Islands", "// gTileset_SeviiIslands\n" + lab,
              before="#endif")
    return num_tiles, labels


def install_door(labels):
    """Rocket Warehouse door: Cold Storage's 3 frames, glass moved to index 13 and the snowflake swapped for the
    R (sevii_art_pieces._rocket_door_images does the same to the closed metatile). Rustboro doors are copied
    for the Sevii copy of the tileset."""
    from PIL import Image
    import sevii_art_pieces as AP
    im = Image.open(P("graphics", "door_anims", "cold_storage.png"))
    px = im.load()
    out = im.copy()
    op = out.load()
    for f in range(im.size[1] // 32):
        for y in range(32):
            for x in range(16):
                c = px[x, f * 32 + y]
                if c == 14:
                    c = 11 if x == 7 else 10 if x == 8 else 9
                if 8 <= y < 27 and 1 <= x < 15 and c == 9:
                    c = 13
                op[x, f * 32 + y] = c
        if f == 0:                           # the R only on the first (barely open) frame
            for j, r in enumerate(AP.R_GLYPH):
                for i, ch in enumerate(r):
                    X, Y = AP.R_AT[0] + i, AP.R_AT[1] + j
                    op[X, Y] = 14 if ch == "R" else 12 if ch == "d" else 13
    out.save(P("graphics", "door_anims", "sevii_rocket_warehouse.png"))
    path = P("src", "field_door.c")
    txt = open(path).read()
    txt = re.sub(r"\n// sevii-door begin.*?// sevii-door end\n", "\n", txt, flags=re.S)
    txt = re.sub(r"\n    // sevii-door-table begin.*?// sevii-door-table end\n", "\n", txt, flags=re.S)
    i = txt.index("static const u8 sDoorAnimPalettes_ColdStorage[]")
    i = txt.index("\n", i) + 1
    txt = txt[:i] + ('\n// sevii-door begin\nstatic const u8 sDoorAnimTiles_SeviiRocketWarehouse[] = '
                     'INCGFX_U8("graphics/door_anims/sevii_rocket_warehouse.png", ".4bpp");\n'
                     '// sevii-door end\n') + txt[i:]
    # Rustboro door entries, re-pointed at the Sevii copy
    rust = re.findall(r"    \{\n        \.metatileNum = (METATILE_Rustboro_\w+),\n        \.tileset = &gTileset_Rustboro,\n"
                      r"(.*?)\n    \},", txt, flags=re.S)
    ent = ["    {\n        .metatileNum = %s,\n        .tileset = &gTileset_SeviiIslands,\n%s\n    }," % (m, rest)
           for m, rest in rust]
    ent.append("    {\n        .metatileNum = METATILE_SeviiIslands_RocketWarehouse_Door,\n"
               "        .tileset = &gTileset_SeviiIslands,\n        .sound = DOOR_SOUND_SLIDING,\n"
               "        .size = DOOR_SIZE_1x2,\n        .tiles = sDoorAnimTiles_SeviiRocketWarehouse,\n"
               "        .palettes = sDoorAnimPalettes_ColdStorage\n    },")
    anchor = "    // Tosa Port uses a copy of Slateport"
    i = txt.index(anchor)
    txt = txt[:i] + "    // sevii-door-table begin: gTileset_SeviiIslands (Rustboro copy + Rocket Warehouse)\n" + \
        "\n".join(ent) + "\n    // sevii-door-table end\n" + txt[i:]
    open(path, "w").write(txt)
    return [m for m, _ in rust]


# ------------------------------------------------------------------ layouts
def install_layouts(ex):
    lj_path = P("data", "layouts", "layouts.json")
    lj = jload(lj_path)
    new = jload(os.path.join(ex, "layouts.json"))["layouts"]
    by_id = {l.get("id"): i for i, l in enumerate(lj["layouts"])}
    for L in new:
        folder = L["blockdata_filepath"].split("/")[2]
        nf = LAYOUT_FOLDER_RENAME.get(folder, folder)
        L = OrderedDict(L)
        L["name"] = nf + "_Layout"
        L["border_filepath"] = "data/layouts/%s/border.bin" % nf
        L["blockdata_filepath"] = "data/layouts/%s/map.bin" % nf
        d = P("data", "layouts", nf)
        os.makedirs(d, exist_ok=True)
        for f in ("map.bin", "border.bin"):
            shutil.copy(os.path.join(ex, "layouts", folder, f), os.path.join(d, f))
        if L["id"] in by_id:
            lj["layouts"][by_id[L["id"]]] = L
        else:
            by_id[L["id"]] = len(lj["layouts"])
            lj["layouts"].append(L)
    jdump(lj_path, lj)
    MA.reset()


def restore_game_corner_layout():
    """LAYOUT_TWO_ISLAND_JOYFUL_GAME_CORNER = the deleted Mauville Game Corner room (git 1d1d50b3a2^)."""
    import subprocess
    ref = "1d1d50b3a2^"
    d = P("data", "layouts", "TwoIsland_JoyfulGameCorner")
    os.makedirs(d, exist_ok=True)
    for f in ("map.bin", "border.bin"):
        data = subprocess.run(["git", "-C", ROOT, "show", "%s:data/layouts/MauvilleCity_GameCorner/%s" % (ref, f)],
                              capture_output=True, check=True).stdout
        open(os.path.join(d, f), "wb").write(data)
    lj_path = P("data", "layouts", "layouts.json")
    lj = jload(lj_path)
    entry = OrderedDict([("id", "LAYOUT_TWO_ISLAND_JOYFUL_GAME_CORNER"), ("name", "TwoIsland_JoyfulGameCorner_Layout"),
                         ("width", 22), ("height", 11), ("primary_tileset", "gTileset_Building"),
                         ("secondary_tileset", "gTileset_MauvilleGameCorner"),
                         ("border_filepath", "data/layouts/TwoIsland_JoyfulGameCorner/border.bin"),
                         ("blockdata_filepath", "data/layouts/TwoIsland_JoyfulGameCorner/map.bin"),
                         ("layout_version", "emerald")])
    for i, l in enumerate(lj["layouts"]):
        if l.get("id") == entry["id"]:
            lj["layouts"][i] = entry
            break
    else:
        lj["layouts"].append(entry)
    jdump(lj_path, lj)
    MA.reset()
    src = subprocess.run(["git", "-C", ROOT, "show", "%s:data/maps/MauvilleCity_GameCorner/scripts.pory" % ref],
                         capture_output=True, text=True, check=True).stdout
    src = src.strip()
    assert src.startswith("raw `") and src.endswith("`")
    src = src[len("raw `"):-1].strip("\n")
    mj = json.loads(subprocess.run(["git", "-C", ROOT, "show", "%s:data/maps/MauvilleCity_GameCorner/map.json" % ref],
                                   capture_output=True, text=True, check=True).stdout, object_pairs_hook=OrderedDict)
    return src, mj


# ------------------------------------------------------------------ layout fixes
def frlg_layout_cells(layout_id):
    import subprocess
    lj = json.loads(subprocess.run(["git", "-C", ROOT, "show", "8ee39561d7~1:data/layouts/layouts.json"],
                                   capture_output=True, text=True, check=True).stdout)
    F = next(l for l in lj["layouts"] if l.get("id") == layout_id)
    d = subprocess.run(["git", "-C", ROOT, "show", "8ee39561d7~1:" + F["blockdata_filepath"]], capture_output=True,
                       check=True).stdout
    return F["width"], struct.unpack("<%dH" % (len(d) // 2), d)


def fix_layouts():
    """Mt. Ember: the translator copied Lavaridge's ash 0x271 with the collision vanilla gives it outside the
    paths, so FRLG's walkable ash came out solid. Take collision/elevation from FRLG for those cells."""
    fixed = {}
    for lid in ("LAYOUT_MT_EMBER_EXTERIOR", "LAYOUT_MT_EMBER_SUMMIT"):
        L = MA.Layout(lid)
        w, F = frlg_layout_cells(lid)
        n = 0
        for y in range(L.h):
            for x in range(L.w):
                f = F[y * w + x]
                if L.mt(x, y) == 0x271 and not (f >> 10) & 3 and L.coll(x, y):
                    L.cells[y * L.w + x] = 0x271 | ((f >> 12) << 12)
                    n += 1
        L.save()
        fixed[lid] = n
    # FRLG water the translator drew with a blocked pond/sea metatile (Berry Forest / Four Island ponds): surfable again
    import check_sevii as C
    for L0 in jload(P("data", "layouts", "layouts.json"))["layouts"]:
        if L0.get("secondary_tileset") not in ("gTileset_SeviiIslands",):
            continue
        try:
            w, F = frlg_layout_cells(L0["id"])
        except StopIteration:
            continue
        L = MA.Layout(entry=L0)
        if w != L.w or len(F) != L.w * L.h:
            continue
        n = 0
        for y in range(L.h):
            for x in range(L.w):
                f = F[y * w + x]
                if not (f >> 10) & 3 and L.coll(x, y) and C.is_water(L.beh(x, y)) and (f >> 12) == 1:
                    L.cells[y * L.w + x] &= ~(3 << 10)
                    n += 1
        if n:
            L.save()
            fixed[L0["id"]] = n
    # Elevation 4 on walkable cells: Route 104's pier planks (harbour docks, Bond Bridge, Canyon Entrance) and the
    # ported Memorial Pillar plaza came with elevation 4 while the land around them is 3, so the docks were cut off
    # from the towns. Make them 3.
    for L0 in jload(P("data", "layouts", "layouts.json"))["layouts"]:
        if L0.get("secondary_tileset") != "gTileset_SeviiIslands":
            continue
        L = MA.Layout(entry=L0)
        n = 0
        for i, v in enumerate(L.cells):
            if not (v >> 10) & 3 and v >> 12 == 4:
                L.cells[i] = (v & 0x0FFF) | (3 << 12)
                n += 1
        if n:
            L.save()
            fixed[L0["id"] + " (elev 4->3)"] = n
    # two openings the translation closed: Four Island's channel up to the Icefall Cave pond (FRLG had a path at
    # x40), and Six Island's dock edge, the only way from the island onto the sea (Six-Seven Strait)
    for lid, (x, y), mt in (("LAYOUT_FOUR_ISLAND", (39, 27), 0x001), ("LAYOUT_SIX_ISLAND", (14, 25), None)):
        L = MA.Layout(lid)
        v = L.raw(x, y)
        L.cells[y * L.w + x] = (mt if mt is not None else v & 0x3FF) | (3 << 12)
        L.save()
        fixed["%s (%d,%d) opened" % (lid, x, y)] = 1
    return fixed


# ------------------------------------------------------------------ scripts (poryscript)
class Script:
    def __init__(self, folder):
        self.folder, self.parts, self.on_transition, self.raw = folder, [], [], []
        self.labels = set()

    def label(self, suffix):
        lab = "%s_EventScript_%s" % (self.folder, suffix)
        i, base = 2, lab
        while lab in self.labels:
            lab, i = "%s%d" % (base, i), i + 1
        self.labels.add(lab)
        return lab

    def msg(self, label, text, kind="MSGBOX_NPC"):
        self.labels.add(label)
        self.parts.append('script %s {\n    msgbox(format("%s"), %s)\n}\n' % (label, esc(text), kind))

    def sign(self, label, text):
        self.labels.add(label)
        if "\n" in text:
            head, rest = text.split("\n", 1)
            body = '"%s\\n"\n        "%s"' % (esc(head), esc(rest).replace("\n", " "))
            self.parts.append('script %s {\n    msgbox(format(%s), MSGBOX_SIGN)\n}\n' % (label, body))
        else:
            self.parts.append('script %s {\n    msgbox(format("%s"), MSGBOX_SIGN)\n}\n' % (label, esc(text)))

    def mon(self, label, species, text):
        self.labels.add(label)
        self.parts.append('script %s {\n    lock\n    faceplayer\n    waitse\n    playmoncry(%s, CRY_MODE_NORMAL)\n'
                          '    msgbox(format("%s"))\n    waitmoncry\n    release\n}\n' % (label, species, esc(text)))

    def text(self):
        out = []
        if self.on_transition:
            out.append("mapscripts %s_MapScripts {\n    MAP_SCRIPT_ON_TRANSITION {\n%s    }\n}\n" % (
                self.folder, "".join("        %s\n" % l for l in self.on_transition)))
        else:
            out.append("mapscripts %s_MapScripts {}\n" % self.folder)
        out += self.parts
        if self.raw:
            out.append("raw `\n%s\n`\n" % "\n".join(self.raw))
        return "\n".join(out)


def write_map(folder, m, scr):
    d = P("data", "maps", folder)
    os.makedirs(d, exist_ok=True)
    jdump(os.path.join(d, "map.json"), m)
    open(os.path.join(d, "scripts.pory"), "w").write(scr.text() if isinstance(scr, Script) else scr)
    stale = os.path.join(d, "scripts.inc")
    if os.path.exists(stale):
        os.remove(stale)


def pick(pool, key):
    h = 0
    for ch in key:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return pool[h % len(pool)]


def npc_line(folder, suffix, gfx):
    if "%s:%s" % (folder, suffix) in TX.LINES:
        return TX.LINES["%s:%s" % (folder, suffix)]
    role = TX.GFX_ROLE.get(gfx.replace("OBJ_EVENT_GFX_", ""), "gentle")
    pool = list(TX.POOLS[role]) + TX.MAP_POOLS.get(folder, []) * 2
    return pick(pool, folder + suffix)


def sign_text(folder, suffix):
    if "%s:%s" % (folder, suffix) in TX.SIGNS:
        return TX.SIGNS["%s:%s" % (folder, suffix)]
    if suffix.startswith("Braille"):
        return TX.SIGNS["Braille"]
    return "A weathered sign. The words have worn away."


def item_const(label_suffix):
    """ItemMaxPotion -> ITEM_MAX_POTION, ItemTM36 -> ITEM_TM36, ItemHM07 -> ITEM_HM07 (then ITEM_FIX)."""
    s = label_suffix[4:]
    c = "ITEM_" + snake(re.sub(r"([A-Z]+)(\d+)", r"\1_\2", s)).replace("TM_", "TM").replace("HM_", "HM")
    return ITEM_FIX.get(c, c)


FLAGS_JSON = os.path.join(HERE, "sevii_flags.json")


def allocate_flags(items, hidden):
    """items / hidden: lists of (sevii_flag_name, item_const). Returns {sevii_name: vanilla_name} and writes
    sevii_flags.json (kept between runs so re-runs reuse the same vanilla slots)."""
    old = json.load(open(FLAGS_JSON)) if os.path.exists(FLAGS_JSON) else {}
    res = RF.main(quiet=True)
    free = {"items": [n for _, n in res["items"]], "hidden": [n for _, n in res["hidden"]
                                                                if "SS_TIDAL" not in n and "NAVEL_ROCK" not in n]}
    taken = set(old.values())
    # non-item entries (event flags such as FLAG_SEVII_DOTTED_HOLE_OPEN from polish_content) are kept as they are
    out = {k: v for k, v in old.items() if not k.startswith(("FLAG_ITEM_", "FLAG_HIDDEN_ITEM_"))}
    for kind, wanted in (("items", items), ("hidden", hidden)):
        pool = [n for n in free[kind] if n not in taken]
        for name, item in wanted:
            if name in old:
                out[name] = old[name]
                continue
            short = item.replace("ITEM_", "")
            match = next((n for n in pool if n.endswith("_" + short)), None) or pool[0]
            pool.remove(match)
            out[name] = match
    json.dump(out, open(FLAGS_JSON, "w"), indent=1, sort_keys=True)
    return out


def apply_flags(alloc, visited):
    """Rename the reused vanilla flags in flags.h (value kept) + aliases for the old names; name the visited
    flags in the sevii FLAG_UNUSED range; rename VAR_UNUSED_0x409B; point FLAG_WORLD_MAP_*_ISLAND at them."""
    path = P("include", "constants", "flags.h")
    txt = open(path).read()
    txt = re.sub(r"\n// sevii-flags begin.*?// sevii-flags end\n", "\n", txt, flags=re.S)
    for new, van in alloc.items():
        txt = re.sub(r"#define %s(\s+)(\([^)\n]*\)|\S+)( //[^\n]*)?\n" % re.escape(van),
                     lambda m: "#define %s%s%s // Sevii (was %s)\n" % (new, " " * max(1, len(m.group(1)) + len(van) - len(new)),
                                                                     m.group(2), van), txt, count=1)
    aliases = "".join("#define %-52s %s\n" % (van, new) for new, van in sorted(alloc.items(), key=lambda kv: kv[1]))
    anchor = "#define FLAG_ITEM_SAFARI_ZONE_SOUTH_EAST_BIG_PEARL"
    i = txt.index("\n", txt.index(anchor)) + 1
    txt = txt[:i] + ("\n// sevii-flags begin: vanilla item / hidden-item flags reused for Sevii items (their maps can't be "
                     "reached in Orchid,\n// dev_scripts/voyages/sevii/reach_flags.py); the aliases keep those maps building.\n"
                     + aliases + "// sevii-flags end\n") + txt[i:]
    for n, (const, _, _) in enumerate(visited):
        v = 0x264 + n
        txt = re.sub(r"#define FLAG_UNUSED_0x%03X(\s+)0x%03X // Unused Flag" % (v, v),
                     "#define FLAG_VISITED_%s  0x%03X // Sevii: set on entering the island (fly / region map)" % (const, v),
                     txt)
        txt = re.sub(r"#define FLAG_VISITED_%s\s+0\n" % const,
                     "// FLAG_VISITED_%s: defined with the Sevii flags (0x%03X)\n" % (const, v), txt)
        txt = re.sub(r"#define FLAG_WORLD_MAP_%s(\s+)0\n" % const,
                     lambda m: "#define FLAG_WORLD_MAP_%s%sFLAG_VISITED_%s\n" % (const, m.group(1), const), txt)
    open(path, "w").write(txt)
    vp = P("include", "constants", "vars.h")
    vt = open(vp).read()
    vt = vt.replace("#define VAR_UNUSED_0x409B                                0x409B // Unused Var",
                    "#define VAR_SHOP_PRICE_MULTIPLIER                        0x409B // Sevii: buy-price multiplier "
                    "for the next pokemart (0 = x1); the stall script resets it")
    open(vp, "w").write(vt)


# ------------------------------------------------------------------ maps
GFX_SCRIPT = {"OBJ_EVENT_GFX_BREAKABLE_ROCK": "EventScript_RockSmash",
              "OBJ_EVENT_GFX_PUSHABLE_BOULDER": "EventScript_StrengthBoulder",
              "OBJ_EVENT_GFX_CUTTABLE_TREE": "EventScript_CutTree"}
ISLAND_FOLDERS = {f: c for c, f, _ in ISLANDS}
EDGE_WARPS = {   # Mt. Ember's FRLG arrow warps sit on shared Lavaridge ash: warp events + facing-checked coord triggers
    "MtEmber_Exterior": [((28, 48), "DIR_SOUTH", "MAP_ONE_ISLAND_KINDLE_ROAD", 0),
                         ((29, 48), "DIR_SOUTH", "MAP_ONE_ISLAND_KINDLE_ROAD", 1),
                         ((29, 7), "DIR_NORTH", "MAP_MT_EMBER_SUMMIT", 0)],
    "MtEmber_Summit": [((9, 15), "DIR_SOUTH", "MAP_MT_EMBER_EXTERIOR", 4)],
}
SEALED = {}
OBJ_MOVES = {("MtEmber_Exterior", 41, 40): (40, 41), ("MtEmber_Exterior", 42, 40): (39, 41)}   # off Ruby Path's mouth      # folder -> [(x, y, text key)], filled from CONFIG in build_maps


def item_flag_name(folder, item, kind, used):
    base = snake(folder).replace("SEVII_SEA_ROUTE", "SEA_ROUTE")
    name = "FLAG_%s_SEVII_%s_%s" % (kind, base, item.replace("ITEM_", ""))
    n, out = 2, name
    while out in used:
        out, n = "%s_%d" % (name, n), n + 1
    used.add(out)
    return out


def build_maps(ex):
    maps, scripts = OrderedDict(), {}
    items, hidden, used = [], [], set()
    if CONFIG["seal_dotted_hole"]:
        SEALED["SixIsland_RuinValley"] = [("DottedHoleDoor",)]
    for folder in sorted(os.listdir(os.path.join(ex, "maps"))):
        m = jload(os.path.join(ex, "maps", folder, "map.json"))
        for k in ("_export_notes", "region"):
            m.pop(k, None)
        m["connections"] = m.get("connections") or None
        sec = m["region_map_section"]
        if folder in SEA_ROUTE_SEC:
            sec = SEA_ROUTE_SEC[folder]
        elif sec == "MAPSEC_THREE_ISLE_PATH":           # FRLG's Dunsparce Tunnel section is a strait now
            sec = "MAPSEC_THREE_ISLE_PORT"
        m["region_map_section"] = sec
        if folder == "ThreeIsland_DunsparceTunnel":       # the dug-out tunnel: both ends joined (no Prospector story)
            m["layout"] = "LAYOUT_THREE_ISLAND_DUNSPARCE_TUNNEL_DUG_OUT"
        scr = Script(folder)
        objs = []
        for o in m["object_events"]:
            if o.get("type") == "clone" or folder in DROP_OBJECTS:
                continue
            g = o["graphics_id"]
            if any(k in g for k in DROP_GFX):
                continue
            if "MR_BRINEYS_BOAT" in g:
                g = "OBJ_EVENT_GFX_MR_BRINEYS_BOAT"
            elif "doll (no Emerald gfx)" in g:
                g = "OBJ_EVENT_GFX_" + DOLL_SWAP[g.split()[0].replace("OBJ_EVENT_GFX_", "")]
            elif "BIG_LAPRAS_DOLL" in g:
                g = "OBJ_EVENT_GFX_BIG_LAPRAS_DOLL"
            elif g.startswith("OBJ_EVENT_GFX_CHANSEY"):
                g = "OBJ_EVENT_GFX_SPECIES(CHANSEY)"
            assert " " not in g, (folder, g)
            o = OrderedDict((k, v) for k, v in o.items() if k not in ("local_id", "type"))
            o["graphics_id"] = g
            o["trainer_type"] = "TRAINER_TYPE_NONE"
            o["trainer_sight_or_berry_tree_id"] = "0"
            script = o["script"]
            pre = folder + "_EventScript_"
            suffix = script[len(pre):] if script.startswith(pre) else None
            if g == "OBJ_EVENT_GFX_ITEM_BALL":
                if suffix and suffix.startswith("Item"):
                    item = item_const(suffix)
                elif str(o.get("trainer_sight_or_berry_tree_id", "")).startswith("ITEM_") and o["trainer_sight_or_berry_tree_id"] != "ITEM_NONE":
                    item = o["trainer_sight_or_berry_tree_id"]
                else:
                    item = {"SeviiSeaRouteA": "ITEM_PEARL", "SeviiSeaRouteB": "ITEM_STAR_PIECE",
                            "SeviiSeaRouteC": "ITEM_BIG_PEARL"}.get(folder, "ITEM_PEARL")
                name = item_flag_name(folder, item, "ITEM", used)
                items.append((name, item))
                o.update(script="Common_EventScript_FindItem", trainer_sight_or_berry_tree_id=item, flag=name)
                o["movement_type"] = "MOVEMENT_TYPE_NONE"
                objs.append(o)
                continue
            orig_flag = str(o.get("flag", ""))
            o["flag"] = "0"
            if g in GFX_SCRIPT:
                o["script"] = GFX_SCRIPT[g]
            elif g == "OBJ_EVENT_GFX_MR_BRINEYS_BOAT":
                o["script"] = "0x0"
            elif g.startswith("OBJ_EVENT_GFX_SPECIES("):
                sp = g[len("OBJ_EVENT_GFX_SPECIES("):-1]
                lab = script if suffix else scr.label(sp.title().replace("_", ""))
                o["script"] = lab
                line = TX.LINES.get("%s:%s" % (folder, suffix)) or "%s: %s!" % (
                    sp.replace("_F", "").replace("_M", ""), pick(["Gyaoo", "Kyuu", "Grrr", "Pii-pii", "Mrrrr"], folder + sp))
                scr.mon(lab, "SPECIES_" + sp, line)
            elif "_DOLL" in g:
                lab = folder + "_EventScript_Doll"
                o["script"] = lab
                if lab not in scr.labels:
                    scr.msg(lab, TX.LINES["FourIsland_LoreleisHouse:Doll"], "MSGBOX_SIGN")
            elif folder.endswith("_Harbor") and g == "OBJ_EVENT_GFX_SAILOR":
                o["script"] = folder + "_EventScript_Sailor"            # ferry, written by harbours()
            elif folder == "TwoIsland" and suffix == "Clerk":
                o["script"] = "TwoIsland_EventScript_Clerk"             # market stall, scripts in sevii.inc
            else:
                if suffix is None:
                    lab = scr.label("BILL" if "BILL" in orig_flag else "Person")
                    suffix = lab[len(pre):]
                    scr.labels.discard(lab)
                else:
                    lab = script
                o["script"] = lab
                if lab not in scr.labels:
                    scr.msg(lab, npc_line(folder, suffix, g))
            objs.append(o)
        for o in objs:                                   # story blockers that stay as flavour NPCs step aside
            o["x"], o["y"] = OBJ_MOVES.get((folder, o["x"], o["y"]), (o["x"], o["y"]))
        m["object_events"] = objs
        bgs = []
        for b in m["bg_events"]:
            b = OrderedDict(b)
            if b["type"] == "hidden_item":
                item = ITEM_FIX.get(b["item"], b["item"])
                name = item_flag_name(folder, item, "HIDDEN_ITEM", used)
                hidden.append((name, item))
                b.update(item=item, flag=name)
                b.setdefault("quantity", 1)
                b["underfoot"] = False
            elif b["type"] == "sign":
                lab = b["script"]
                suffix = lab[len(folder + "_EventScript_"):]
                if lab not in scr.labels:
                    scr.sign(lab, sign_text(folder, suffix))
            bgs.append(b)
        m["bg_events"] = bgs
        coords = []
        if folder == "OneIsland_KindleRoad_EmberSpa":
            for c in m["coord_events"]:
                coords.append(OrderedDict(c, script="OneIsland_KindleRoad_EmberSpa_EventScript_SpaHeal",
                                          var="VAR_TEMP_1", var_value="0"))
        for (x, y), facing, dest, wid in EDGE_WARPS.get(folder, []):
            lab = "%s_EventScript_EdgeWarp_%d_%d" % (folder, x, y)
            coords.append(OrderedDict([("type", "trigger"), ("x", x), ("y", y), ("elevation", 0), ("var", "VAR_TEMP_0"),
                                       ("var_value", "0"), ("script", lab)]))
            scr.raw.append("%s::\n\tspecialvar VAR_RESULT, GetPlayerFacingDirection\n"
                           "\tgoto_if_ne VAR_RESULT, %s, Sevii_EventScript_End\n"
                           "\twarp %s, %d\n\twaitstate\n\tend\n" % (lab, facing, dest, wid))
        m["coord_events"] = coords
        if folder in ISLAND_FOLDERS:
            scr.on_transition.append("setflag(FLAG_VISITED_%s)" % ISLAND_FOLDERS[folder])
        maps[folder], scripts[folder] = m, scr
    return maps, scripts, items, hidden


def seal_doors(maps, scripts):
    """Sealed entrances: the door cell stays impassable (it already is in the translation), the warp stays (so
    re-opening = make the cell a door again), and a sign on the door cell explains."""
    sealed = []
    targets = []
    if CONFIG["seal_dotted_hole"]:
        targets += [("SixIsland_RuinValley", "MAP_SIX_ISLAND_DOTTED_HOLE_1F", "SixIsland_RuinValley:DottedHoleDoor")]
    if CONFIG["seal_tanoby_chambers"]:
        targets += [("SevenIsland_TanobyRuins", d, "TanobySealed") for d in
                    [w["dest_map"] for w in maps["SevenIsland_TanobyRuins"]["warp_events"]]]
    for folder, dest, key in targets:
        m, scr = maps[folder], scripts[folder]
        L = MA.Layout(m["layout"])
        for w in m["warp_events"]:
            if w["dest_map"] != dest:
                continue
            x, y = w["x"], w["y"]
            if not L.coll(x, y):
                L.cells[y * L.w + x] |= 1 << 10
                L.save()
            lab = "%s_EventScript_Sealed" % folder
            if lab not in scr.labels:
                scr.sign(lab, TX.SIGNS[key])
            m["bg_events"] = [b for b in m["bg_events"] if (b["x"], b["y"]) != (x, y)] + [OrderedDict([
                ("type", "sign"), ("x", x), ("y", y), ("elevation", 0),
                ("player_facing_dir", "BG_EVENT_PLAYER_FACING_NORTH"), ("script", lab)])]
            sealed.append((folder, x, y, dest))
    return sealed


# ------------------------------------------------------------------ harbours (ferry)
def harbours(maps, scripts):
    order = [h for _, _, h in ISLANDS]
    for const, town, folder in ISLANDS:
        m, scr = maps[folder], scripts[folder]
        sailor, boat = "LOCALID_%s_HARBOR_SAILOR" % const, "LOCALID_%s_HARBOR_BOAT" % const
        m["object_events"] = [
            OrderedDict([("local_id", sailor), ("graphics_id", "OBJ_EVENT_GFX_SAILOR"), ("x", 8), ("y", 5),
                         ("elevation", 0), ("movement_type", "MOVEMENT_TYPE_FACE_UP"), ("movement_range_x", 1),
                         ("movement_range_y", 1), ("trainer_type", "TRAINER_TYPE_NONE"),
                         ("trainer_sight_or_berry_tree_id", "0"), ("script", folder + "_EventScript_Sailor"),
                         ("flag", "0")]),
            OrderedDict([("local_id", boat), ("graphics_id", "OBJ_EVENT_GFX_MR_BRINEYS_BOAT"), ("x", 8), ("y", 7),
                         ("elevation", 1), ("movement_type", "MOVEMENT_TYPE_FACE_RIGHT"), ("movement_range_x", 1),
                         ("movement_range_y", 1), ("trainer_type", "TRAINER_TYPE_NONE"),
                         ("trainer_sight_or_berry_tree_id", "0"), ("script", "0x0"), ("flag", "0")])]
        exit_ = m["warp_events"][0]
        exit_["elevation"] = 0
        # warp 1 = landing spot on the dock (not a warp tile: only used as an arrival point, SEVII_ARRIVAL_WARP)
        m["warp_events"] = [exit_, OrderedDict(exit_, x=HARBOUR_LAND[0], y=HARBOUR_LAND[1])]
        m["show_map_name"] = False
        dests = [h for h in order if h != folder]
        dests.sort(key=lambda h: (CLUSTER[h] != CLUSTER[folder], order.index(h)))
        texts = ", ".join("SeviiFerry_Text_%s" % h.replace("_Harbor", "") for h in dests) + ", SeviiFerry_Text_Stay_Option"
        L = ["%s_EventScript_Sailor::" % folder, "\tlock", "\tfaceplayer", "\tmessage SeviiFerry_Text_WhereTo",
             "\twaitmessage", "\tdynmultichoice 0, 0, FALSE, 7, 0, DYN_MULTICHOICE_CB_NONE, %s" % texts,
             "\tswitch VAR_RESULT"]
        L += ["\tcase %d, %s_EventScript_To%s" % (i, folder, h.replace("_Harbor", "")) for i, h in enumerate(dests)]
        L += ["\tmsgbox SeviiFerry_Text_Stay, MSGBOX_DEFAULT", "\trelease", "\tend", ""]
        for h in dests:
            L += ["%s_EventScript_To%s::" % (folder, h.replace("_Harbor", "")),
                  "\tsetvar VAR_0x8004, %s" % boat, "\tsetvar VAR_0x8005, %s" % sailor,
                  "\tcall SeviiFerry_EventScript_Board",
                  "\twarp %s, %d, %d" % (maps[h]["id"], HARBOUR_LAND[0], HARBOUR_LAND[1]), "\twaitstate", "\trelease",
                  "\tend", ""]
        scr.raw.append("\n".join(L))


# ------------------------------------------------------------------ Centres / Marts / Game Corner
def centre(maps, scripts, town, const, sec):
    folder = town + "_PokemonCenter_1F"
    m = jload(P("data", "maps", "TelokTown_PokemonCenter_1F", "map.json"))
    nurse = "LOCALID_%s_NURSE" % const
    keep = []
    scr = Script(folder)
    for o in m["object_events"]:
        if o.get("local_id", "").endswith("_NURSE"):
            keep.append(OrderedDict(o, local_id=nurse, script=folder + "_EventScript_Nurse"))
        elif o.get("script") == "Common_EventScript_OrchidCafe":
            keep.append(o)
    if town == "OneIsland":     # One Island's Centre is the Net Center
        keep.append(OrderedDict([("graphics_id", "OBJ_EVENT_GFX_SCIENTIST_1"), ("x", 3), ("y", 4), ("elevation", 3),
                                 ("movement_type", "MOVEMENT_TYPE_FACE_RIGHT"), ("movement_range_x", 0),
                                 ("movement_range_y", 0), ("trainer_type", "TRAINER_TYPE_NONE"),
                                 ("trainer_sight_or_berry_tree_id", "0"), ("script", folder + "_EventScript_NetTech"),
                                 ("flag", "0")]))
        scr.msg(folder + "_EventScript_NetTech", "This is the POKéMON NET CENTER. The network machine in the back links "
                "the Sevii Islands with Tosa. It's still being tuned, though!")
    m.update(id="MAP_%s_POKEMON_CENTER_1F" % const, name=folder, region_map_section=sec, object_events=keep,
             warp_events=[OrderedDict(wv, dest_map="MAP_" + const, dest_warp_id="0")
                          for wv in m["warp_events"] if wv["dest_map"] == "MAP_OLDALE_TOWN"])
    if town == "OneIsland":
        m["music"] = "MUS_RG_NET_CENTER"
    scr.on_transition.append("setrespawn(HEAL_LOCATION_%s)" % const)
    scr.raw.append("\n".join(["%s_EventScript_Nurse::" % folder, "\tsetvar VAR_0x800B, %s" % nurse,
                              "\tcall Common_EventScript_PkmnCenterNurse", "\twaitmessage", "\twaitbuttonpress",
                              "\trelease", "\tend"]))
    txt = scr.text().replace("mapscripts %s_MapScripts {\n" % folder,
                             "mapscripts %s_MapScripts {\n    MAP_SCRIPT_ON_RESUME: CableClub_OnResume\n" % folder)
    maps[folder], scripts[folder] = m, txt
    return folder


def mart(maps, scripts, town, const, sec):
    folder = town + "_Mart"
    m = jload(P("data", "maps", "TelokTown_Mart", "map.json"))
    clerk = [OrderedDict(o, script=folder + "_EventScript_Clerk") for o in m["object_events"]
             if o.get("script", "").endswith("_Clerk")]
    for o in clerk:
        o.pop("local_id", None)
    m.update(id="MAP_%s_MART" % const, name=folder, region_map_section=sec, object_events=clerk,
             warp_events=[OrderedDict(wv, dest_map="MAP_" + const, dest_warp_id="0") for wv in m["warp_events"]])
    scr = Script(folder)
    scr.raw.append("\n".join(["%s_EventScript_Clerk::" % folder, "\tlock", "\tfaceplayer",
                              "\tmessage gText_HowMayIServeYou", "\twaitmessage", "\tpokemart SeviiMart_Items",
                              "\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT", "\trelease", "\tend"]))
    maps[folder], scripts[folder] = m, scr
    return folder


GC_LINES = {
    "Woman2": "The slots here are a little kinder than the ones in Tosa. Or maybe I'm just lucky today!",
    "Gentleman": "I sailed all the way from Tosa just to play here. The owner's smile is worth the trip.",
    "OldMan": "I opened this Game Corner so the islanders would have somewhere joyful to gather.",
    "Cook": "I cook for the market stall, then spend my wages right here. Ha ha!",
    "Man": "Roulette is all luck. Slots? Also luck. I love it.",
    "Maniac": "I've counted every reel symbol. Doesn't help at all.",
    "Woman": "The prize corner has dolls you can't get anywhere else in the islands.",
}


def game_corner(maps, scripts, src, mj):
    folder = "TwoIsland_JoyfulGameCorner"
    m = mj
    m.update(id="MAP_TWO_ISLAND_JOYFUL_GAME_CORNER", name=folder, layout="LAYOUT_TWO_ISLAND_JOYFUL_GAME_CORNER",
             region_map_section="MAPSEC_TWO_ISLAND", music="MUS_RG_GAME_CORNER")
    m.pop("region", None)
    for w in m["warp_events"]:
        w.update(dest_map="MAP_TWO_ISLAND", dest_warp_id="0")
    body = src.replace("MauvilleCity_GameCorner", folder)
    for o in m["object_events"]:
        o["script"] = o["script"].replace("MauvilleCity_GameCorner", folder)
    for b in m["bg_events"]:
        b["script"] = b["script"].replace("MauvilleCity_GameCorner", folder)
    # tweaked NPC lines: replace each plain chatter NPC's script with a fresh label
    extra = []
    for o in m["object_events"]:
        suf = o["script"].replace(folder + "_EventScript_", "")
        if suf in GC_LINES:
            lab = "%s_EventScript_Joyful%s" % (folder, suf)
            o["script"] = lab
            extra.append('script %s {\n    msgbox(format("%s"), MSGBOX_NPC)\n}\n' % (lab, esc(GC_LINES[suf])))
    maps[folder] = m
    scripts[folder] = "raw `\n%s\n`\n\n%s" % (body.replace("`", "'"), "\n".join(extra))
    return folder


# ------------------------------------------------------------------ warps
def mat_warps(maps):
    """Emerald exit mats are 2 wide: duplicate every interior exit warp onto a neighbouring cell with the same
    arrow-warp behaviour. Also moves the Rocket Warehouse exit onto its (moved) mat."""
    names, _ = MA.mb()
    arrows = {names[k] for k in ("MB_SOUTH_ARROW_WARP", "MB_NORTH_ARROW_WARP", "MB_EAST_ARROW_WARP",
                                 "MB_WEST_ARROW_WARP")}
    added = []
    for folder, m in maps.items():
        L = MA.Layout(m["layout"])
        ws = m["warp_events"]
        cells = {(w["x"], w["y"]) for w in ws}
        if folder == "FiveIsland_RocketWarehouse":
            for w in ws:
                if L.beh(w["x"], w["y"]) not in arrows:
                    for y in range(L.h - 1, -1, -1):
                        xs = [x for x in range(L.w) if L.beh(x, y) in arrows]
                        if xs:
                            w["x"], w["y"] = xs[0], y
                            break
            cells = {(w["x"], w["y"]) for w in ws}
        for w in list(ws):
            x, y = w["x"], w["y"]
            if not L.inside(x, y) or L.beh(x, y) not in arrows:
                continue
            for dx in (-1, 1):
                if L.inside(x + dx, y) and (x + dx, y) not in cells and L.beh(x + dx, y) == L.beh(x, y) \
                        and m["map_type"] == "MAP_TYPE_INDOOR":
                    ws.append(OrderedDict(w, x=x + dx))
                    cells.add((x + dx, y))
                    added.append((folder, x + dx, y))
    return added


def link_warps(maps):
    """Make warp pairs point at each other: warp i of A -> B; if B has exactly one 'group' of warps back to A
    (adjacent cells), point i at the first of them and each of them back at the first warp of A's group."""
    ids = {m["id"]: f for f, m in maps.items()}
    problems = []

    def groups(m, dest):
        out = []
        for i, w in enumerate(m["warp_events"]):
            if w["dest_map"] != dest:
                continue
            for g in out:
                if any(abs(m["warp_events"][j]["x"] - w["x"]) + abs(m["warp_events"][j]["y"] - w["y"]) == 1 for j in g):
                    g.append(i)
                    break
            else:
                out.append([i])
        return out
    for f, m in maps.items():
        for i, w in enumerate(m["warp_events"]):
            B = ids.get(w["dest_map"])
            if B is None:
                problems.append("%s warp %d -> unknown %s" % (f, i, w["dest_map"]))
                continue
            back = groups(maps[B], m["id"])
            mine = next(g for g in groups(m, w["dest_map"]) if i in g)
            if len(back) == 1 and len(groups(m, w["dest_map"])) == 1:
                w["dest_warp_id"] = str(back[0][0])
            elif not back:
                problems.append("%s warp %d -> %s has no warp back" % (f, i, w["dest_map"]))
    return problems


# ------------------------------------------------------------------ registration
def register(maps, scripts):
    groups = jload(P("data", "maps", "map_groups.json"))
    island_first = [f for _, f, _ in ISLANDS]
    order = island_first + sorted(f for f in maps if f not in island_first)
    groups[GROUP] = order
    if GROUP not in groups["group_order"]:
        groups["group_order"].append(GROUP)
    jdump(P("data", "maps", "map_groups.json"), groups)
    for f in order:
        write_map(f, maps[f], scripts[f])
    path = P("data", "event_scripts.s")
    lines = [l for l in open(path).read().split("\n") if MARK not in l]
    at = next(i for i, l in enumerate(lines) if "data/maps/Route124_DivingTreasureHuntersHouse/scripts.inc" in l) + 1
    lines[at:at] = ['\t.include "data/maps/%s/scripts.inc" %s' % (f, MARK) for f in order] + \
        ['\t.include "data/scripts/sevii.inc" %s' % MARK]
    open(path, "w").write("\n".join(lines))
    return order


def heal_locations(maps):
    path = P("src", "data", "heal_locations.json")
    hj = jload(path)
    done = []
    for const, town, _ in ISLANDS:
        door = next(w for w in maps[town]["warp_events"] if w["dest_map"] == "MAP_%s_POKEMON_CENTER_1F" % const)
        entry = OrderedDict([("id", "HEAL_LOCATION_" + const), ("map", "MAP_" + const), ("x", door["x"]),
                             ("y", door["y"] + 1), ("respawn_map", "MAP_%s_POKEMON_CENTER_1F" % const),
                             ("respawn_npc", "LOCALID_%s_NURSE" % const)])
        for i, h in enumerate(hj["heal_locations"]):
            if h["id"] == entry["id"]:
                hj["heal_locations"][i] = entry
                break
        else:
            hj["heal_locations"].append(entry)
        done.append(entry)
    jdump(path, hj)
    return done


def mapsecs():
    path = P("src", "data", "region_map", "region_map_sections.json")
    j = jload(path)
    for e in j["map_sections"]:
        if e["id"] in SEC_RENAMES:
            e["id"] = SEC_RENAMES[e["id"]]
        if e["id"] in SEC_NAMES:
            e["name"] = SEC_NAMES[e["id"]]
    jdump(path, j)
    ap = P("include", "constants", "region_map_section_aliases.h")
    lines = open(ap).read().split("\n")
    have = {l.split()[1] for l in lines if l.startswith("#define MAPSEC_")}
    add = ["#define %-36s %s" % (o, n) for o, n in sorted(SEC_RENAMES.items()) if o not in have]
    if add:
        i = max(k for k, l in enumerate(lines) if l.startswith("#define MAPSEC_")) + 1
        lines[i:i] = add
        # keep the generator's sort order
        defs = sorted(l for l in lines if l.startswith("#define MAPSEC_"))
        it = iter(defs)
        lines = [next(it) if l.startswith("#define MAPSEC_") else l for l in lines]
    open(ap, "w").write("\n".join(lines))


def constants_header():
    open(P("include", "constants", "sevii.h"), "w").write(
        "#ifndef GUARD_CONSTANTS_SEVII_H\n#define GUARD_CONSTANTS_SEVII_H\n\n"
        "// Wavebreak Voyages: where a voyage to the Sevii Islands lands (dev_scripts/voyages/sevii/build_sevii.py).\n"
        "// One Island's harbour dock, in front of the ferry sailor; warp id 1 is a landing-only warp event on that cell.\n"
        "#define SEVII_ARRIVAL_MAP      MAP_ONE_ISLAND_HARBOR\n"
        "#define SEVII_ARRIVAL_WARP_ID  1\n"
        "#define SEVII_ARRIVAL_X        %d\n#define SEVII_ARRIVAL_Y        %d\n\n"
        "// Every island harbour (MAP_<N>_ISLAND_HARBOR, Three's is reached from Three Isle Port) uses the same landing\n"
        "// cell and warp id; the ferry sailor stands at (8,5) and Mr. Briney's boat at (8,7).\n"
        "#define SEVII_HARBOR_LANDING_WARP_ID  1\n\n"
        "#endif // GUARD_CONSTANTS_SEVII_H\n" % HARBOUR_LAND)


def common_scripts():
    harb = [h for _, _, h in ISLANDS]
    L = ["@ Sevii Islands shared scripts (dev_scripts/voyages/sevii/build_sevii.py)", "",
         "Sevii_EventScript_End::", "\tend", "",
         "@ VAR_0x8004 = boat local id, VAR_0x8005 = sailor local id",
         "SeviiFerry_EventScript_Board::", "\tmsgbox SeviiFerry_Text_AllAboard, MSGBOX_DEFAULT", "\tclosemessage",
         "\tapplymovement VAR_0x8005, Common_Movement_WalkInPlaceFasterDown", "\twaitmovement 0", "\tdelay 20",
         "\tremoveobject VAR_0x8005", "\tcall Common_EventScript_FerryDepartIsland", "\treturn", "",
         "SeviiFerry_Text_WhereTo:", '\t.string "Ahoy! Mr. Briney\'s boat runs between\\n"',
         '\t.string "all seven islands. Where to?$"', "",
         "SeviiFerry_Text_AllAboard:", '\t.string "All aboard! Hold on to your hat!$"', "",
         "SeviiFerry_Text_Stay:", '\t.string "Right you are. Come back any time!$"', ""]
    for h in harb:
        L += ["SeviiFerry_Text_%s:" % h.replace("_Harbor", ""), '\t.string "%s$"' % HARBOUR_NAME[h].upper(), ""]
    L += ["SeviiFerry_Text_Stay_Option:", '\t.string "STAY HERE$"', ""]
    L += ["@ Two Island market stall: rare goods at CONFIG stall_price_multiplier x their price",
          "TwoIsland_EventScript_Clerk::", "\tlock", "\tfaceplayer", "\tmessage SeviiStall_Text_Welcome",
          "\twaitmessage", "\tsetvar VAR_SHOP_PRICE_MULTIPLIER, %d" % CONFIG["stall_price_multiplier"],
          "\tpokemart SeviiStall_Items", "\tsetvar VAR_SHOP_PRICE_MULTIPLIER, 0",
          "\tmsgbox SeviiStall_Text_Bye, MSGBOX_DEFAULT", "\trelease", "\tend", "",
          "\t.align 2", "SeviiStall_Items:"] + ["\t.2byte %s" % i for i in STALL_STOCK] + ["\tpokemartlistend", "",
          "SeviiStall_Text_Welcome:", '\t.string "Welcome to the market stall!\\n"',
          '\t.string "Rare goods from every island!$"', "",
          "SeviiStall_Text_Bye:", '\t.string "Rare goods don\'t come cheap.\\n"', '\t.string "Come again!$"', "",
          "\t.align 2", "SeviiMart_Items:"] + ["\t.2byte %s" % i for i in MART_STOCK] + ["\tpokemartlistend", "",
          "OneIsland_KindleRoad_EmberSpa_EventScript_SpaHeal::", "\tlockall", "\tfadescreen FADE_TO_WHITE",
          "\tspecial HealPlayerParty", "\tfadescreen FADE_FROM_WHITE",
          "\tmsgbox SeviiSpa_Text_Healed, MSGBOX_DEFAULT", "\tsetvar VAR_TEMP_1, 1", "\treleaseall", "\tend", "",
          "SeviiSpa_Text_Healed:", '\t.string "The hot spring water soothed your\\n"',
          '\t.string "POKéMON. They look refreshed!$"', ""]
    open(P("data", "scripts", "sevii.inc"), "w").write("\n".join(L) + "\n")


def shop_patch():
    path = P("src", "shop.c")
    t = open(path).read()
    if "SeviiShopPrice" in t:
        return
    t = t.replace("GetItemPrice(itemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT)", "SeviiShopPrice(itemId)")
    t = t.replace("GetItemPrice(tItemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT)", "SeviiShopPrice(tItemId)")
    i = t.index("static void BuyMenuPrintPriceInList(u8 windowId, u32 itemId, u8 y);")
    i = t.index("\n", i) + 1
    t = t[:i] + "static u32 SeviiShopPrice(u32 itemId);\n" + t[i:]
    t = t.rstrip("\n") + (
        "\n\n// Sevii (Wavebreak Voyages): a per-shop buy-price multiplier. A shop script sets VAR_SHOP_PRICE_MULTIPLIER\n"
        "// before `pokemart` and clears it after (Two Island's market stall uses x3); 0 means x1.\n"
        "static u32 SeviiShopPrice(u32 itemId)\n{\n"
        "    u32 mult = VarGet(VAR_SHOP_PRICE_MULTIPLIER);\n"
        "    u32 price = GetItemPrice(itemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT);\n"
        "    return mult > 1 ? price * mult : price;\n}\n")
    open(path, "w").write(t)


# ------------------------------------------------------------------ wild encounters
EVOLVE = {"SPEAROW": "FEAROW", "SENTRET": "FURRET", "ODDISH": "GLOOM", "MEOWTH": "PERSIAN", "PSYDUCK": "GOLDUCK",
          "HORSEA": "SEADRA", "POLIWAG": "POLIWHIRL", "GOLDEEN": "SEAKING", "PONYTA": "RAPIDASH",
          "GEODUDE": "GRAVELER", "ZUBAT": "GOLBAT", "SWINUB": "PILOSWINE", "SEEL": "DEWGONG", "SLOWPOKE": "SLOWBRO",
          "WOOPER": "QUAGSIRE", "HOPPIP": "SKIPLOOM", "MANKEY": "PRIMEAPE", "KRABBY": "KINGLER",
          "NIDORAN_F": "NIDORINA", "NIDORAN_M": "NIDORINO", "BELLSPROUT": "WEEPINBELL", "PIDGEY": "PIDGEOTTO",
          "RATTATA": "RATICATE", "VENONAT": "VENOMOTH", "DODUO": "DODRIO", "MACHOP": "MACHOKE", "MAREEP": "FLAAFFY",
          "PHANPY": "DONPHAN", "TEDDIURSA": "URSARING", "HOUNDOUR": "HOUNDOOM", "LARVITAR": "PUPITAR",
          "SLUGMA": "MAGCARGO", "TENTACOOL": "TENTACRUEL", "SPINARAK": "ARIADOS", "LEDYBA": "LEDIAN",
          "HOOTHOOT": "NOCTOWL", "NATU": "XATU", "MURKROW": "MURKROW", "MARILL": "AZUMARILL", "CHINCHOU": "LANTURN",
          "REMORAID": "OCTILLERY", "STARYU": "STARMIE", "PARAS": "PARASECT", "DIGLETT": "DUGTRIO", "ONIX": "ONIX",
          "MACHOKE": "MACHOKE", "GLOOM": "GLOOM", "WEEPINBELL": "WEEPINBELL", "CUBONE": "MAROWAK",
          "SANDSHREW": "SANDSLASH", "EKANS": "ARBOK", "GASTLY": "HAUNTER", "MAGNEMITE": "MAGNETON",
          "SHUPPET": "BANETTE", "BALTOY": "CLAYDOL"}
# folder -> FRLG source map (its FireRed + LeafGreen tables), or a list of (mon type, source map) to borrow
WILD_SRC = {
    "OneIsland": "MAP_ONE_ISLAND", "TwoIsland": [("water_mons", "MAP_ONE_ISLAND"), ("fishing_mons", "MAP_ONE_ISLAND")],
    "ThreeIsland": [("water_mons", "MAP_ONE_ISLAND"), ("fishing_mons", "MAP_ONE_ISLAND")],
    "OneIsland_KindleRoad": "MAP_ONE_ISLAND_KINDLE_ROAD", "OneIsland_TreasureBeach": "MAP_ONE_ISLAND_TREASURE_BEACH",
    "TwoIsland_CapeBrink": "MAP_TWO_ISLAND_CAPE_BRINK", "ThreeIsland_BondBridge": "MAP_THREE_ISLAND_BOND_BRIDGE",
    "ThreeIsland_Port": "MAP_THREE_ISLAND_PORT", "ThreeIsland_BerryForest": "MAP_THREE_ISLAND_BERRY_FOREST",
    "MtEmber_Exterior": "MAP_MT_EMBER_EXTERIOR", "MtEmber_SummitPath_1F": "MAP_MT_EMBER_SUMMIT_PATH_1F",
    "MtEmber_SummitPath_2F": "MAP_MT_EMBER_SUMMIT_PATH_2F", "MtEmber_SummitPath_3F": "MAP_MT_EMBER_SUMMIT_PATH_3F",
    "MtEmber_RubyPath_1F": "MAP_MT_EMBER_RUBY_PATH_1F", "MtEmber_RubyPath_B1F": "MAP_MT_EMBER_RUBY_PATH_B1F",
    "MtEmber_RubyPath_B2F": "MAP_MT_EMBER_RUBY_PATH_B2F", "MtEmber_RubyPath_B3F": "MAP_MT_EMBER_RUBY_PATH_B3F",
    "MtEmber_RubyPath_B1F_Stairs": "MAP_MT_EMBER_RUBY_PATH_B1F_STAIRS",
    "MtEmber_RubyPath_B2F_Stairs": "MAP_MT_EMBER_RUBY_PATH_B2F_STAIRS",
    "MtEmber_RubyPath_B4F": [("land_mons", "MAP_MT_EMBER_RUBY_PATH_B3F")],
    "MtEmber_RubyPath_B5F": [("land_mons", "MAP_MT_EMBER_RUBY_PATH_B3F")],
    "FourIsland": "MAP_FOUR_ISLAND", "FourIsland_IcefallCave_Entrance": "MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE",
    "FourIsland_IcefallCave_1F": "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F",
    "FourIsland_IcefallCave_B1F": "MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F",
    "FourIsland_IcefallCave_Back": "MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK",
    "FiveIsland": "MAP_FIVE_ISLAND", "FiveIsland_Meadow": "MAP_FIVE_ISLAND_MEADOW",
    "FiveIsland_MemorialPillar": "MAP_FIVE_ISLAND_MEMORIAL_PILLAR",
    "SixIsland": [("water_mons", "MAP_FIVE_ISLAND"), ("fishing_mons", "MAP_SIX_ISLAND_WATER_PATH")],
    "SixIsland_WaterPath": "MAP_SIX_ISLAND_WATER_PATH", "SixIsland_RuinValley": "MAP_SIX_ISLAND_RUIN_VALLEY",
    "SevenIsland": [("water_mons", "MAP_FIVE_ISLAND"), ("fishing_mons", "MAP_FIVE_ISLAND")],
    "SevenIsland_SevaultCanyon_Entrance": "MAP_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE",
    "SevenIsland_SevaultCanyon": "MAP_SEVEN_ISLAND_SEVAULT_CANYON",
    "SevenIsland_TanobyRuins": "MAP_SEVEN_ISLAND_TANOBY_RUINS",
    "SeviiSeaRouteA": [("water_mons", "MAP_ONE_ISLAND"), ("fishing_mons", "MAP_ONE_ISLAND")],
    "SeviiSeaRouteB": [("water_mons", "MAP_ONE_ISLAND"), ("fishing_mons", "MAP_THREE_ISLAND_PORT")],
    "SeviiSeaRouteC": [("water_mons", "MAP_FIVE_ISLAND"), ("fishing_mons", "MAP_FOUR_ISLAND")],
    "SeviiSeaRouteD": [("water_mons", "MAP_FIVE_ISLAND"), ("fishing_mons", "MAP_SIX_ISLAND_WATER_PATH")],
}
DUNSPARCE = {"land_mons": {"encounter_rate": 7, "mons": [
    ("DUNSPARCE", 56, 58), ("GOLBAT", 56, 58), ("GRAVELER", 55, 57), ("DUNSPARCE", 58, 60), ("ONIX", 56, 58),
    ("GOLBAT", 58, 60), ("GRAVELER", 57, 59), ("DUNSPARCE", 60, 62), ("ONIX", 60, 62), ("STEELIX", 62, 64),
    ("DUNSPARCE", 63, 65), ("STEELIX", 65, 67)]}}


def lvl(l):
    return max(55, min(68, int(round(55 + (l - 5) * 13.0 / 58))))


def wild(maps):
    path = P("src", "data", "wild_encounters.json")
    j = jload(path)
    grp = j["wild_encounter_groups"][0]
    src = {}
    for e in grp["encounters"]:
        if e["base_label"].endswith("_FireRed"):
            src.setdefault(e["map"], {})["fr"] = e
        elif e["base_label"].endswith("_LeafGreen"):
            src.setdefault(e["map"], {})["lg"] = e
    grp["encounters"] = [e for e in grp["encounters"] if not e["base_label"].startswith("gSevii_")]

    def table(kind, mapc):
        fr, lg = src[mapc]["fr"], src[mapc].get("lg", src[mapc]["fr"])
        if kind not in fr:
            return None
        mons = []
        for i, (a, b) in enumerate(zip(fr[kind]["mons"], lg[kind]["mons"])):
            m = b if i % 2 and b["species"] != a["species"] else a
            sp = m["species"][len("SPECIES_"):]
            old_rod = kind == "fishing_mons" and i < 2
            if not old_rod:
                sp = EVOLVE.get(sp, sp)
            lo, hi = lvl(m["min_level"]), lvl(m["max_level"])
            if lo == hi and not old_rod:
                hi = min(68, lo + 2)
            mons.append(OrderedDict([("min_level", lo), ("max_level", hi), ("species", "SPECIES_" + sp)]))
        return OrderedDict([("encounter_rate", fr[kind]["encounter_rate"]), ("mons", mons)])
    added = []
    for folder, s in WILD_SRC.items():
        e = OrderedDict([("map", maps[folder]["id"]), ("base_label", "gSevii_" + folder.replace("_", ""))])
        parts = [(k, s) for k in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons")] \
            if isinstance(s, str) else s
        for kind, mapc in parts:
            t = table(kind, mapc)
            if t:
                e[kind] = t
        grp["encounters"].append(e)
        added.append(folder)
    e = OrderedDict([("map", "MAP_THREE_ISLAND_DUNSPARCE_TUNNEL"), ("base_label", "gSevii_ThreeIslandDunsparceTunnel")])
    e["land_mons"] = OrderedDict([("encounter_rate", 7), ("mons", [OrderedDict(
        [("min_level", a), ("max_level", b), ("species", "SPECIES_" + s)]) for s, a, b in DUNSPARCE["land_mons"]["mons"]])])
    grp["encounters"].append(e)
    added.append("ThreeIsland_DunsparceTunnel")
    jdump(path, j)
    return added


# ------------------------------------------------------------------ main
def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    ex = sys.argv[1]
    num_tiles, labels = install_tileset(ex)
    doors = install_door(labels)
    install_layouts(ex)
    fixed = fix_layouts()
    gc_src, gc_mj = restore_game_corner_layout()
    maps, scripts, items, hidden = build_maps(ex)
    sealed = seal_doors(maps, scripts)
    harbours(maps, scripts)
    clones = []
    for const, town, _ in ISLANDS:
        sec = maps[town]["region_map_section"]
        clones.append(centre(maps, scripts, town, const, sec))
        if town in MARTS:
            clones.append(mart(maps, scripts, town, const, sec))
    clones.append(game_corner(maps, scripts, gc_src, gc_mj))
    mats = mat_warps(maps)
    problems = link_warps(maps)
    moved = relocate_unreachable(maps)
    alloc = allocate_flags(items, hidden)
    apply_flags(alloc, ISLANDS)
    order = register(maps, scripts)
    heals = heal_locations(maps)
    mapsecs()
    constants_header()
    common_scripts()
    shop_patch()
    w = wild(maps)
    report = OrderedDict([("num_tiles", num_tiles), ("door_entries", doors), ("ash_cells_fixed", fixed),
                          ("maps", order), ("clones", clones), ("sealed", sealed), ("mat_warps", mats),
                          ("warp_problems", problems), ("relocated", moved), ("flags", alloc), ("heal_locations", heals), ("wild", w)])
    jdump(os.path.join(HERE, "build_report.json"), report)
    print("maps %d (clones %d), item flags %d, hidden %d, sealed %d, mat warps %d, wild %d" % (
        len(order), len(clones), len(items), len(hidden), len(sealed), len(mats), len(w)))
    for p in problems:
        print("WARP:", p)



def relocate_unreachable(maps):
    """Items / NPCs that the translation walled in (Meadow, Berry Forest, Four Island, Six Island) move to the
    nearest reachable land cell. Decorations (dolls, the Day-Care pen POKéMON) stay where they are."""
    import check_sevii as C
    moved = []
    for f, m in maps.items():
        L = MA.Layout(m["layout"])
        seen, _ = C.flood(m, L)
        busy = {(o["x"], o["y"]) for o in m["object_events"]} | {(w["x"], w["y"]) for w in m["warp_events"]} | \
            {(b["x"], b["y"]) for b in m["bg_events"]}

        def nearest(x0, y0):
            best = None
            for (x, y) in seen:
                if (x, y) in busy or C.is_water(L.beh(x, y)) or L.elev(x, y) in (0, 15):
                    continue
                d = abs(x - x0) + abs(y - y0)
                if best is None or d < best[0]:
                    best = (d, x, y)
            return best
        things = [("obj", o) for o in m["object_events"]] + [("bg", b) for b in m["bg_events"] if b["type"] == "hidden_item"]
        for kind, o in things:
            g = o.get("graphics_id", "")
            if "_DOLL" in g or g.startswith("OBJ_EVENT_GFX_SPECIES(") or "BOAT" in g or o.get("script") == "0x0":
                continue
            if kind == "bg" and (o["x"], o["y"]) in seen:
                continue
            if kind == "obj" and C.reachable_from(seen, L, o["x"], o["y"]):
                continue
            nb = nearest(o["x"], o["y"])
            if nb:
                busy.add((nb[1], nb[2]))
                moved.append((f, g or o.get("item"), (o["x"], o["y"]), (nb[1], nb[2])))
                o["x"], o["y"], o["elevation"] = nb[1], nb[2], L.elev(nb[1], nb[2])
    # interaction needs matching elevations: give every object the elevation of the cell it is talked from
    for f, m in maps.items():
        L = MA.Layout(m["layout"])
        seen, _ = C.flood(m, L)
        for b in m["bg_events"]:                     # signs / hidden items: any elevation
            b["elevation"] = 0
        for o in m["object_events"]:
            x, y = o["x"], o["y"]
            g = o["graphics_id"]
            if not L.inside(x, y) or "_DOLL" in g or g.startswith("OBJ_EVENT_GFX_SPECIES("):
                continue
            e = L.elev(x, y)
            if L.coll(x, y) or e in (0, 15):
                adj = [(x + dx, y + dy) for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)) if (x + dx, y + dy) in seen]
                es = [L.elev(*a) for a in adj if L.elev(*a) not in (0, 15)]
                if not es:
                    continue
                e = es[0]
            if o["elevation"] != e:
                moved.append((f, o["graphics_id"], "elevation %d -> %d" % (o["elevation"], e), (x, y)))
                o["elevation"] = e
    return moved


if __name__ == "__main__":
    main()
