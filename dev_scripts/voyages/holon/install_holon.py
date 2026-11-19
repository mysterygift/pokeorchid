"""
Install Holon (Wavebreak Voyages, holon stream) into the game data, from the approved batch-4 specs.

  * gTileset_Holon          data/tilesets/secondary/holon/  (= the approved "full greens" draft gTileset_HolonDesat:
                            Fortree copy + blue-grey rock copies, rail kit pieces, carved stones, lake pillars,
                            plinth, sealed dome door, drained-ring metatiles; desaturated foliage palettes)
  * gTileset_General_Holon  data/tilesets/primary/general_holon/palettes/ (palettes only; the struct points at
                            General's own tiles / metatiles / attributes)
  * field-effect palettes   graphics/field_effects/palettes/general_{0,1}_holon.pal (greens desaturated)
  * sphere OBJ              graphics/object_events/pics/misc/holon_sphere.png + palettes holon_sphere{,_glow}.pal
  * layouts + maps          gMapGroup_Holon: coast, village (+ Centre, Mart, 7 houses, ruins house), Research
                            Tower 1F/2F, lake; map.json + scripts.pory; heal location; wild encounters
  * C wiring is done by hand (see DONE.md); this script only writes data files and prints a check summary.

Re-runnable: every output is rewritten from the specs. usage: <venv python> install_holon.py
"""
import json
import os
import shutil
import struct
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mock_holon as mh          # noqa: E402  (rebuilds the draft tileset into _draft/)
import specs_holon as sp         # noqa: E402
import holon_tileset as ht       # noqa: E402
import voyage_compose as vc      # noqa: E402
import holon_text as T           # noqa: E402
from PIL import Image            # noqa: E402

ROOT = vc.ROOT
P = lambda *a: os.path.join(ROOT, *a)   # noqa: E731
DRAFT = os.path.join(HERE, "_draft")
GROUP = "gMapGroup_Holon"
PAIR = ("gTileset_General_Holon", "gTileset_Holon")

# ---------------------------------------------------------------------------------------------- tilesets
def install_tilesets():
    src = os.path.join(DRAFT, "gTileset_HolonDesat")
    dst = P("data", "tilesets", "secondary", "holon")
    os.makedirs(os.path.join(dst, "palettes"), exist_ok=True)
    for f in ("tiles.png", "metatiles.bin", "metatile_attributes.bin"):
        shutil.copy(os.path.join(src, f), os.path.join(dst, f))
    for i in range(16):
        shutil.copy(os.path.join(src, "palettes", "%02d.pal" % i), os.path.join(dst, "palettes", "%02d.pal" % i))
    gsrc = os.path.join(DRAFT, "gTileset_GeneralHolon", "palettes")
    gdst = P("data", "tilesets", "primary", "general_holon", "palettes")
    os.makedirs(gdst, exist_ok=True)
    for i in range(16):
        shutil.copy(os.path.join(gsrc, "%02d.pal" % i), os.path.join(gdst, "%02d.pal" % i))
    # field-effect OBJ palettes with the same green desaturation as the primary copy
    for n in (0, 1):
        pal = ht.load_pal(P("graphics", "field_effects", "palettes", "general_%d.pal" % n))
        new = [pal[0]] + [ht.desat(c) for c in pal[1:]]
        open(P("graphics", "field_effects", "palettes", "general_%d_holon.pal" % n), "w").write(ht.jasc(new))
    # sphere OBJ: 32x32 indexed PNG (dormant palette) + the two palettes (same indices)
    stone = [(0, 0, 0), (232, 240, 248), (192, 204, 224), (152, 164, 192), (120, 132, 168), (88, 100, 136),
             (64, 72, 104), (40, 40, 64)]
    glow = [(0, 0, 0), (240, 255, 255), (168, 240, 248), (112, 208, 248), (72, 168, 232), (48, 120, 208),
            (32, 80, 168), (24, 40, 104)]
    snap = lambda c: tuple(min(248, (v // 8) * 8) for v in c)   # noqa: E731
    stone, glow = [snap(c) for c in stone], [snap(c) for c in glow]
    rgba = ht.sphere_sprite(False)
    lut = {c: i for i, c in enumerate(stone)}
    im = Image.new("P", (32, 32), 0)
    pal = [v for c in stone + [(0, 0, 0)] * (16 - len(stone)) for v in c]
    im.putpalette(pal + [0] * (768 - len(pal)))
    for y in range(32):
        for x in range(32):
            r, g, b, a = rgba.getpixel((x, y))
            if a:
                im.putpixel((x, y), lut[snap((r, g, b))])
    im.save(P("graphics", "object_events", "pics", "misc", "holon_sphere.png"))
    pad = [(0, 0, 0)] * (16 - len(stone))
    open(P("graphics", "object_events", "palettes", "holon_sphere.pal"), "w").write(ht.jasc(stone + pad))
    open(P("graphics", "object_events", "palettes", "holon_sphere_glow.pal"), "w").write(ht.jasc(glow + pad))


# ---------------------------------------------------------------------------------------------- layouts
def write_bin(path, vals):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(struct.pack("<%dH" % len(vals), *vals))


def read_bin(path):
    b = open(path, "rb").read()
    return list(struct.unpack("<%dH" % (len(b) // 2), b))


def layout_entry(lid, folder, w, h, ts):
    return OrderedDict([("id", lid), ("name", folder + "_Layout"), ("width", w), ("height", h),
                        ("primary_tileset", ts[0]), ("secondary_tileset", ts[1]),
                        ("border_filepath", "data/layouts/%s/border.bin" % folder),
                        ("blockdata_filepath", "data/layouts/%s/map.bin" % folder),
                        ("layout_version", "emerald")])


GRIDS = {}
PLANKS = {0x210, 0x218, 0x216, 0x21E, 0x217, 0x21F}     # Route 119 bridge planks (top layer over sprites)
POSTS = {0x2FE, 0x306}                                  # its grass end posts (elevation 4 in vanilla)


def _set_elev(g, x, y, e):
    g[y][x] = (g[y][x] & 0x0FFF) | (e << 12)


def _land3(g, x, y):
    return 0 <= y < len(g) and 0 <= x < len(g[0]) and not (g[y][x] >> 10) & 3 and g[y][x] >> 12 == 3


def fix_bridges(g):
    """Route 119's planks are drawn over sprites, so whoever walks on them must be at elevation 4 (sprite
    priority 1), as on Route 119 where the banks are elevation 4. Holon's banks are elevation 3, so:
    a bridge with end posts keeps posts at 4 and gets a transition cell (elevation 0) beyond each post;
    a bridge without posts gets its planks at 4 (no surfing under it) and a transition cell at each end."""
    for y, row in enumerate(g):
        x = 0
        while x < len(row):
            if row[x] & 0x3FF not in PLANKS:
                x += 1
                continue
            x0 = x
            while x < len(row) and row[x] & 0x3FF in PLANKS:
                x += 1
            x1 = x - 1
            ends = [(x0 - 1, -1), (x1 + 1, 1)]
            posts = [0 <= ex < len(row) and row[ex] & 0x3FF in POSTS for ex, _d in ends]
            if not all(posts):
                for i in range(x0, x1 + 1):
                    _set_elev(g, i, y, 4)
            for (ex, d), post in zip(ends, posts):
                if post:
                    _set_elev(g, ex, y, 4)
                    if _land3(g, ex + d, y):
                        _set_elev(g, ex + d, y, 0)
                elif _land3(g, ex, y):
                    _set_elev(g, ex, y, 0)


def build_layouts():
    out = []
    outdoor = {"holon_coast": ("LAYOUT_HOLON_MIRAGE_FOREST", "HolonMirageForest", [0x3170] * 4),
               "holon_village": ("LAYOUT_HOLON_VILLAGE", "HolonVillage", [0x0C6, 0x0C7, 0x0C7, 0x0C6]),
               "holon_lake": ("LAYOUT_HOLON_LAKE", "HolonLake", [0x0C6, 0x0C7, 0x0C7, 0x0C6])}
    for name, (lid, folder, border) in outdoor.items():
        spec = sp.ALL[name]
        g = mh.to_holon(vc.build(spec), spec)
        fix_bridges(g)
        GRIDS[name] = g
        h, w = len(g), len(g[0])
        vc.check_size(w, h)
        write_bin(P("data", "layouts", folder, "map.bin"), [v for r in g for v in r])
        write_bin(P("data", "layouts", folder, "border.bin"), border)
        out.append(layout_entry(lid, folder, w, h, PAIR))
    for name, lid, folder, base in (
            ("holon_tower_2f", "LAYOUT_HOLON_RESEARCH_TOWER_2F", "HolonResearchTower_2F", "Route119_WeatherInstitute_2F"),
            ("holon_ruins_house", "LAYOUT_HOLON_RUINS_HOUSE", "HolonVillage_RuinsHouse", "House1")):
        spec = sp.ALL[name]
        g = vc.build(spec)
        GRIDS[name] = g
        h, w = len(g), len(g[0])
        write_bin(P("data", "layouts", folder, "map.bin"), [v for r in g for v in r])
        shutil.copy(P("data", "layouts", base, "border.bin"), P("data", "layouts", folder, "border.bin"))
        out.append(layout_entry(lid, folder, w, h, spec["tileset"]))
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    ids = {e["id"] for e in out}
    lj["layouts"] = [e for e in lj["layouts"] if e.get("id") not in ids] + out
    write_json(lj_path, lj)


# ---------------------------------------------------------------------------------------------- helpers
def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def elev_at(name, x, y, default=3):
    g = GRIDS.get(name)
    if g is None:
        return default
    e = g[y][x] >> 12
    return default if e in (0, 15) else e


def obj(gfx, x, y, elev, move, script, flag="0", rng=0, trainer=None, sight=0, local_id=None, berry=None):
    o = OrderedDict()
    if local_id:
        o["local_id"] = local_id
    o.update([("graphics_id", gfx), ("x", x), ("y", y), ("elevation", elev), ("movement_type", move),
              ("movement_range_x", rng), ("movement_range_y", rng),
              ("trainer_type", "TRAINER_TYPE_NORMAL" if trainer else
               ("TRAINER_TYPE_NONE")),
              ("trainer_sight_or_berry_tree_id", str(sight) if trainer else (berry or "0")),
              ("script", script), ("flag", flag)])
    return o


def warp(x, y, dest, wid, elev=0):
    return OrderedDict([("x", x), ("y", y), ("elevation", elev), ("dest_map", dest), ("dest_warp_id", str(wid))])


def sign(x, y, script, face="BG_EVENT_PLAYER_FACING_ANY"):
    return OrderedDict([("type", "sign"), ("x", x), ("y", y), ("elevation", 0), ("player_facing_dir", face),
                        ("script", script)])


def map_json(mid, folder, layout, music, mapsec, map_type, conns=None, objs=(), warps=(), bgs=(), coords=(),
             weather="WEATHER_SUNNY", indoor=False):
    return OrderedDict([
        ("id", mid), ("name", folder), ("layout", layout), ("music", music), ("region", "REGION_HOENN"),
        ("region_map_section", mapsec), ("requires_flash", False),
        ("weather", "WEATHER_NONE" if indoor else weather), ("map_type", map_type),
        ("allow_cycling", not indoor), ("allow_escaping", False), ("allow_running", not indoor),
        ("show_map_name", not indoor), ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"),
        ("connections", conns if conns else None), ("object_events", list(objs)), ("warp_events", list(warps)),
        ("coord_events", list(coords)), ("bg_events", list(bgs))])


def esc(t):
    return t.replace('"', "'")


def msg_script(label, text, kind="MSGBOX_NPC"):
    return '\nscript %s {\n    msgbox(format("%s"), %s)\n}\n' % (label, esc(text), kind)


def text_block(label, text):
    return '\ntext %s {\n    format("%s")\n}\n' % (label, esc(text))


MAPS = OrderedDict()         # folder -> (map.json, pory text)


def add_map(folder, j, pory):
    MAPS[folder] = (j, pory)


def trainer_script(folder, n, key):
    """T.TRAINERS[key] = intro/defeat/post; trainer id = TODO placeholder (constants/holon.h)."""
    t = T.TRAINERS[key]
    lab = "%s_EventScript_Researcher%d" % (folder, n)
    return lab, ("\nscript %s {\n    trainerbattle_single(%s, %s_Text_Researcher%dIntro, %s_Text_Researcher%dDefeat)\n"
                 "    msgbox(%s_Text_Researcher%dPost, MSGBOX_AUTOCLOSE)\n}\n" % (
                     lab, T.TRAINER_IDS[key], folder, n, folder, n, folder, n)
                 + text_block("%s_Text_Researcher%dIntro" % (folder, n), t["intro"])
                 + text_block("%s_Text_Researcher%dDefeat" % (folder, n), t["defeat"])
                 + text_block("%s_Text_Researcher%dPost" % (folder, n), t["post"]))


FACE = {"left": "MOVEMENT_TYPE_FACE_LEFT", "right": "MOVEMENT_TYPE_FACE_RIGHT", "up": "MOVEMENT_TYPE_FACE_UP",
        "down": "MOVEMENT_TYPE_FACE_DOWN", "look": "MOVEMENT_TYPE_LOOK_AROUND", "wander": "MOVEMENT_TYPE_WANDER_AROUND"}
RESEARCHER_GFX = "OBJ_EVENT_GFX_SCIENTIST_1"     # TODO(trainers): OBJ_EVENT_GFX_HOLON_RESEARCHER


# ---------------------------------------------------------------------------------------------- coast
ARRIVAL = (5, 36)            # where the voyage lands the player (on the jetty, right of the Sailor)


def coast():
    F, name = "HolonMirageForest", "holon_coast"
    objs = [obj("OBJ_EVENT_GFX_MR_BRINEYS_BOAT", 1, 36, 1, FACE["right"], "0x0", local_id="LOCALID_HOLON_BOAT"),
            obj("OBJ_EVENT_GFX_SAILOR", 3, 36, 4, FACE["right"], F + "_EventScript_Sailor",
                local_id="LOCALID_HOLON_SAILOR"),
            obj("OBJ_EVENT_GFX_GIRL_2", 16, 31, elev_at(name, 16, 31), FACE["wander"], F + "_EventScript_Lass", rng=1)]
    pory = "mapscripts %s_MapScripts {}\n" % F
    pory += ("\nscript %s_EventScript_Sailor {\n    lock\n    faceplayer\n"
             "    // TODO(core): replace with the voyage return menu (Wavebreak / other unlocked destinations)\n"
             "    call(Holon_SailorReturnPlaceholder)\n    release\n}\n" % F)
    pory += ("\nscript Holon_SailorReturnPlaceholder {\n"
             "    msgbox(format(\"%s\"), MSGBOX_DEFAULT)\n}\n" % esc(T.SAILOR_PLACEHOLDER))
    pory += msg_script(F + "_EventScript_Lass", T.COAST["lass"])
    pory += msg_script(F + "_EventScript_Sign", T.COAST["sign"], "MSGBOX_SIGN")
    for n, (x, y, face, key) in enumerate([(21, 9, "left", "c1"), (34, 22, "left", "c2")], 1):
        lab, s = trainer_script(F, n, key)
        objs.append(obj(RESEARCHER_GFX, x, y, elev_at(name, x, y), FACE[face], lab, trainer=True, sight=4))
        pory += s
    j = map_json("MAP_HOLON_MIRAGE_FOREST", F, "LAYOUT_HOLON_MIRAGE_FOREST", "MUS_ROUTE119", "MAPSEC_MIRAGE_FOREST",
                 "MAP_TYPE_ROUTE", conns=[OrderedDict([("map", "MAP_HOLON_VILLAGE"), ("offset", -sp.C_OFFSET),
                                                      ("direction", "right")])],
                 objs=objs, bgs=[sign(20, 34, F + "_EventScript_Sign")])
    add_map(F, j, pory)


# ---------------------------------------------------------------------------------------------- village
HOUSES = OrderedDict([   # village key -> (folder suffix, interior template index)
    ("H1", 0), ("H2", 1), ("H3", 2), ("H4", 3), ("H5", 4), ("H6", 5), ("H7", 6)])
INTERIORS = [   # towns.py templates: layout, exit warps, NPC spot
    ("LAYOUT_HOUSE1", [(3, 8), (4, 8)], (6, 4, "wander")),
    ("LAYOUT_HOUSE2", [(3, 7), (4, 7)], (4, 4, "right")),
    ("LAYOUT_HOUSE3", [(3, 7), (4, 7)], (6, 3, "left")),
    ("LAYOUT_HOUSE4", [(3, 8), (4, 8)], (6, 5, "right")),
    ("LAYOUT_PACIFIDLOG_TOWN_HOUSE1", [(4, 8), (5, 8)], (3, 5, "down")),
    ("LAYOUT_PACIFIDLOG_TOWN_HOUSE2", [(4, 8), (5, 8)], (3, 5, "down")),
    ("LAYOUT_ROUTE116_TUNNELERS_REST_HOUSE", [(4, 8), (5, 8)], (6, 5, "right")),
]
BERRY_TREES = [  # (x, y, berry tree id, berry): reused ids of vanilla Route 102/104 trees (maps deleted)
    (5, 43, "BERRY_TREE_ROUTE_104_SOIL_1", "BERRY_ID_ORAN"), (7, 43, "BERRY_TREE_ROUTE_104_ORAN_1", "BERRY_ID_PECHA"),
    (9, 43, "BERRY_TREE_ROUTE_104_CHERI_1", "BERRY_ID_ORAN"), (6, 46, "BERRY_TREE_ROUTE_104_SOIL_2", "BERRY_ID_SITRUS"),
    (8, 46, "BERRY_TREE_ROUTE_104_LEPPA", "BERRY_ID_ORAN"), (10, 46, "BERRY_TREE_ROUTE_104_ORAN_2", "BERRY_ID_LUM"),
    (22, 12, "BERRY_TREE_ROUTE_104_SOIL_3", "BERRY_ID_PECHA"), (24, 12, "BERRY_TREE_ROUTE_104_PECHA", "BERRY_ID_ORAN"),
    (26, 12, "BERRY_TREE_ROUTE_102_ORAN", "BERRY_ID_PERSIM")]


def village():
    F, name = "HolonVillage", "holon_village"
    vb = sp.V_BUILD
    door = lambda k, d=(1, 3): (vb[k][1] + d[0], vb[k][2] + d[1])   # noqa: E731
    warps, keys = [], []

    def add(key, xy, dest, wid):
        keys.append(key)
        warps.append(warp(xy[0], xy[1], dest, wid))
    add("centre", door("Centre", (2, 4)), "MAP_HOLON_VILLAGE_POKEMON_CENTER_1F", 0)
    add("mart", door("Mart", (1, 4)), "MAP_HOLON_VILLAGE_MART", 0)
    add("mart2", door("Mart", (2, 4)), "MAP_HOLON_VILLAGE_MART", 0)
    for i, k in enumerate(HOUSES, 1):
        add(k, door(k), "MAP_HOLON_VILLAGE_HOUSE%d" % i, 0)
    add("ruins", door("Ruins"), "MAP_HOLON_VILLAGE_RUINS_HOUSE", 0)
    add("tower", (35, 36), "MAP_HOLON_RESEARCH_TOWER_1F", 0)

    objs = []
    pory = ("mapscripts %s_MapScripts {\n    MAP_SCRIPT_ON_TRANSITION {\n        setflag(FLAG_VISITED_HOLON_VILLAGE)\n"
            "        call_if_unset(FLAG_HOLON_BERRIES_PLANTED, %s_EventScript_PlantBerries)\n    }\n}\n" % (F, F))
    pory += "\nscript %s_EventScript_PlantBerries {\n" % F
    for x, y, tid, berry in BERRY_TREES:
        pory += "    setberrytree(%s, %s, BERRY_STAGE_BERRIES)\n" % (tid, berry)
        objs.append(obj("OBJ_EVENT_GFX_BERRY_TREE", x, y, 3, "MOVEMENT_TYPE_BERRY_TREE_GROWTH",
                        "BerryTreeScript", berry=tid))
    pory += "    setflag(FLAG_HOLON_BERRIES_PLANTED)\n}\n"
    npcs = [("OBJ_EVENT_GFX_SCIENTIST_1", 36, 39, "down", "walkway"), ("OBJ_EVENT_GFX_MAN_4", 25, 14, "left", "farmer_nw"),
            ("OBJ_EVENT_GFX_WOMAN_5", 62, 44, "down", "farmer_se"), ("OBJ_EVENT_GFX_GIRL_2", 9, 37, "look", "lass"),
            ("OBJ_EVENT_GFX_EXPERT_M", 56, 16, "down", "mentor"), ("OBJ_EVENT_GFX_MAN_4", 46, 7, "wander", "farmer_n")]
    for gfx, x, y, face, key in npcs:
        lab = "%s_EventScript_%s" % (F, "".join(p.title() for p in key.split("_")))
        objs.append(obj(gfx, x, y, elev_at(name, x, y), FACE[face], lab, rng=1 if face == "wander" else 0))
        pory += msg_script(lab, T.VILLAGE[key])
    bgs = [sign(3, 36, F + "_EventScript_TownSign"), sign(29, 66, F + "_EventScript_LakeSign"),
           sign(16, 9, F + "_EventScript_FarmSign"), sign(38, 37, F + "_EventScript_TowerSign")]
    cx, cy = vb["Centre"][1], vb["Centre"][2]
    mx, my = vb["Mart"][1], vb["Mart"][2]
    # Centre / Mart signs on the solid front cells beside the doors (read from the street, facing north)
    bgs += [sign(cx + 3, cy + 4, "Common_EventScript_ShowPokemonCenterSign", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(cx + 4, cy + 4, "Common_EventScript_ShowPokemonCenterSign", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(mx, my + 4, "Common_EventScript_ShowPokemartSign", "BG_EVENT_PLAYER_FACING_NORTH"),
            sign(mx + 3, my + 4, "Common_EventScript_ShowPokemartSign", "BG_EVENT_PLAYER_FACING_NORTH")]
    for key in ("town", "lake", "farm", "tower"):
        pory += msg_script("%s_EventScript_%sSign" % (F, key.title()), T.VILLAGE["sign_" + key], "MSGBOX_SIGN")
    j = map_json("MAP_HOLON_VILLAGE", F, "LAYOUT_HOLON_VILLAGE", "MUS_FORTREE", "MAPSEC_HOLON_VILLAGE", "MAP_TYPE_TOWN",
                 conns=[OrderedDict([("map", "MAP_HOLON_MIRAGE_FOREST"), ("offset", sp.C_OFFSET), ("direction", "left")]),
                        OrderedDict([("map", "MAP_HOLON_LAKE"), ("offset", 0), ("direction", "down")])],
                 objs=objs, warps=warps, bgs=bgs)
    add_map(F, j, pory)
    widx = {k: i for i, k in enumerate(keys)}

    # Centre + Mart (clones of the Tosa ones: LAYOUT_POKEMON_CENTER_1F / LAYOUT_MART)
    C = F + "_PokemonCenter_1F"
    cj = map_json("MAP_HOLON_VILLAGE_POKEMON_CENTER_1F", C, "LAYOUT_POKEMON_CENTER_1F", "MUS_POKE_CENTER",
                  "MAPSEC_HOLON_VILLAGE", "MAP_TYPE_INDOOR", indoor=True,
                  objs=[obj("OBJ_EVENT_GFX_NURSE", 7, 2, 3, FACE["down"], C + "_EventScript_Nurse",
                            local_id="LOCALID_HOLON_VILLAGE_NURSE"),
                        obj("OBJ_EVENT_GFX_OLD_MAN", 12, 2, 3, FACE["down"], "Common_EventScript_OrchidCafe"),
                        obj("OBJ_EVENT_GFX_SCIENTIST_1", 3, 5, 3, FACE["wander"], C + "_EventScript_Visitor", rng=1)],
                  warps=[warp(7, 9, "MAP_HOLON_VILLAGE", widx["centre"], 3),
                         warp(6, 9, "MAP_HOLON_VILLAGE", widx["centre"], 3)])
    cp = ("raw `\n%s_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition\n"
          "\tmap_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume\n\t.byte 0\n\n%s_OnTransition:\n"
          "\tsetrespawn HEAL_LOCATION_HOLON_VILLAGE\n\tend\n\n%s_EventScript_Nurse::\n"
          "\tsetvar VAR_0x800B, LOCALID_HOLON_VILLAGE_NURSE\n\tcall Common_EventScript_PkmnCenterNurse\n"
          "\twaitmessage\n\twaitbuttonpress\n\trelease\n\tend\n`\n" % (C, C, C, C))
    cp += msg_script(C + "_EventScript_Visitor", T.VILLAGE["centre_visitor"])
    add_map(C, cj, cp)
    M = F + "_Mart"
    mj = map_json("MAP_HOLON_VILLAGE_MART", M, "LAYOUT_MART", "MUS_POKE_MART", "MAPSEC_HOLON_VILLAGE",
                  "MAP_TYPE_INDOOR", indoor=True,
                  objs=[obj("OBJ_EVENT_GFX_MART_EMPLOYEE", 1, 2, 3, FACE["down"], "TelokTown_Mart_EventScript_Clerk")],
                  warps=[warp(6, 8, "MAP_HOLON_VILLAGE", widx["mart"]), warp(7, 8, "MAP_HOLON_VILLAGE", widx["mart"])])
    add_map(M, mj, "mapscripts %s_MapScripts {}\n" % M)

    # houses
    for i, (k, tpl) in enumerate(HOUSES.items(), 1):
        H = "%s_House%d" % (F, i)
        lid, exits, (nx, ny, face) = INTERIORS[tpl]
        gfx, text = T.HOUSES[i - 1]
        hj = map_json("MAP_HOLON_VILLAGE_HOUSE%d" % i, H, lid, "MUS_FORTREE", "MAPSEC_HOLON_VILLAGE", "MAP_TYPE_INDOOR",
                      indoor=True, objs=[obj(gfx, nx, ny, 3, FACE[face], H + "_EventScript_Npc",
                                             rng=1 if face == "wander" else 0)],
                      warps=[warp(ex, ey, "MAP_HOLON_VILLAGE", widx[k]) for ex, ey in exits])
        add_map(H, hj, "mapscripts %s_MapScripts {}\n" % H + msg_script(H + "_EventScript_Npc", text))

    # ruins house (stripped HOUSE1 copy)
    R = F + "_RuinsHouse"
    rj = map_json("MAP_HOLON_VILLAGE_RUINS_HOUSE", R, "LAYOUT_HOLON_RUINS_HOUSE", "MUS_SEALED_CHAMBER",
                  "MAPSEC_HOLON_VILLAGE", "MAP_TYPE_INDOOR", indoor=True,
                  objs=[obj("OBJ_EVENT_GFX_ITEM_BALL", 4, 5, 3, FACE["down"], R + "_EventScript_LoreItem",
                            flag="FLAG_ITEM_HOLON_RUINS_HOUSE_STAR_PIECE")],
                  warps=[warp(3, 8, "MAP_HOLON_VILLAGE", widx["ruins"]), warp(4, 8, "MAP_HOLON_VILLAGE", widx["ruins"])],
                  bgs=[sign(4, 1, R + "_EventScript_Bookshelf"), sign(5, 1, R + "_EventScript_Bookshelf")])
    rp = "mapscripts %s_MapScripts {}\n" % R
    rp += ("\nscript %s_EventScript_LoreItem {\n    lock\n    msgbox(format(\"%s\"), MSGBOX_DEFAULT)\n"
           "    finditem(ITEM_STAR_PIECE)\n    release\n}\n" % (R, esc(T.RUINS["lore"])))
    rp += msg_script(R + "_EventScript_Bookshelf", T.RUINS["shelf"], "MSGBOX_SIGN")
    add_map(R, rj, rp)
    return widx


# ---------------------------------------------------------------------------------------------- tower
def tower(widx):
    F1, F2 = "HolonResearchTower_1F", "HolonResearchTower_2F"
    o1 = []
    p1 = "mapscripts %s_MapScripts {}\n" % F1
    for n, (gfx, x, y, face, key) in enumerate([
            ("OBJ_EVENT_GFX_SCIENTIST_1", 14, 2, "down", "reception"), ("OBJ_EVENT_GFX_SCIENTIST_1", 5, 4, "right", "r1"),
            ("OBJ_EVENT_GFX_SCIENTIST_1", 15, 5, "left", "r2"), ("OBJ_EVENT_GFX_WOMAN_5", 2, 11, "up", "visitor")], 1):
        lab = "%s_EventScript_Npc%d" % (F1, n)
        o1.append(obj(gfx, x, y, 3, FACE[face], lab))
        p1 += msg_script(lab, T.TOWER1[key])
    bed = "%s_EventScript_Bed" % F1
    j1 = map_json("MAP_HOLON_RESEARCH_TOWER_1F", F1, "LAYOUT_ROUTE119_WEATHER_INSTITUTE_1F", "MUS_RUSTBORO",
                  "MAPSEC_RESEARCH_TOWER", "MAP_TYPE_INDOOR", indoor=True, objs=o1,
                  warps=[warp(9, 12, "MAP_HOLON_VILLAGE", widx["tower"]), warp(10, 12, "MAP_HOLON_VILLAGE", widx["tower"]),
                         warp(17, 1, "MAP_HOLON_RESEARCH_TOWER_2F", 0)],
                  bgs=[sign(x, y, bed) for x, y in ((1, 2), (1, 3))])
    p1 += msg_script(bed, T.TOWER1["bed"], "MSGBOX_SIGN")
    add_map(F1, j1, p1)

    o2 = []
    p2 = "mapscripts %s_MapScripts {}\n" % F2
    for n, (x, y, face, key) in enumerate([(18, 6, "left", "t1"), (11, 9, "up", "t2")], 1):
        lab, s = trainer_script(F2, n, key)
        o2.append(obj(RESEARCHER_GFX, x, y, 3, FACE[face], lab, trainer=True, sight=3))
        p2 += s
    o2.append(obj("OBJ_EVENT_GFX_SCIENTIST_1", 6, 6, 3, FACE["right"], F2 + "_EventScript_Npc"))
    p2 += msg_script(F2 + "_EventScript_Npc", T.TOWER2["npc"])
    o2.append(obj("OBJ_EVENT_GFX_EXPERT_M", 2, 6, 3, FACE["down"], F2 + "_EventScript_HeadOfResearch",
                  local_id="LOCALID_HOLON_HEAD_OF_RESEARCH"))
    p2 += eevee_gift(F2)
    j2 = map_json("MAP_HOLON_RESEARCH_TOWER_2F", F2, "LAYOUT_HOLON_RESEARCH_TOWER_2F", "MUS_RUSTBORO",
                  "MAPSEC_RESEARCH_TOWER", "MAP_TYPE_INDOOR", indoor=True, objs=o2,
                  warps=[warp(17, 1, "MAP_HOLON_RESEARCH_TOWER_1F", 2)],
                  bgs=[sign(x, y, F2 + "_EventScript_Machine") for x, y in ((8, 7), (9, 7), (13, 7), (14, 7))])
    p2 += msg_script(F2 + "_EventScript_Machine", T.TOWER2["machine"], "MSGBOX_SIGN")
    add_map(F2, j2, p2)


def eevee_gift(F):
    s = T.TOWER2
    return ("raw `\n%(F)s_EventScript_HeadOfResearch::\n\tlock\n\tfaceplayer\n"
            "\tgoto_if_set FLAG_HOLON_RECEIVED_EEVEE, %(F)s_EventScript_HeadAfter\n"
            "\tmsgbox %(F)s_Text_HeadOffer, MSGBOX_YESNO\n"
            "\tgoto_if_eq VAR_RESULT, NO, %(F)s_EventScript_HeadDeclined\n"
            "\t@ TODO(delta): SPECIES_EEVEE -> SPECIES_EEVEE_DELTA (Eevee-δ gift, Lv 50)\n"
            "\tsetvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_EEVEE\n"
            "\tgivemon SPECIES_EEVEE, 50\n"
            "\tgoto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, %(F)s_EventScript_EeveeParty\n"
            "\tgoto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, %(F)s_EventScript_EeveePC\n"
            "\tgoto Common_EventScript_NoMoreRoomForPokemon\n\tend\n\n"
            "%(F)s_EventScript_EeveeParty::\n\tcall %(F)s_EventScript_EeveeFanfare\n"
            "\tmsgbox gText_NicknameThisPokemon, MSGBOX_YESNO\n"
            "\tgoto_if_eq VAR_RESULT, NO, %(F)s_EventScript_EeveeDone\n"
            "\tcall Common_EventScript_GetGiftMonPartySlot\n\tcall Common_EventScript_NameReceivedPartyMon\n"
            "\tgoto %(F)s_EventScript_EeveeDone\n\tend\n\n"
            "%(F)s_EventScript_EeveePC::\n\tcall %(F)s_EventScript_EeveeFanfare\n"
            "\tmsgbox gText_NicknameThisPokemon, MSGBOX_YESNO\n"
            "\tgoto_if_eq VAR_RESULT, NO, %(F)s_EventScript_EeveeToPC\n"
            "\tcall Common_EventScript_NameReceivedBoxMon\n\tgoto %(F)s_EventScript_EeveeToPC\n\tend\n\n"
            "%(F)s_EventScript_EeveeToPC::\n\tcall Common_EventScript_TransferredToPC\n"
            "\tgoto %(F)s_EventScript_EeveeDone\n\tend\n\n"
            "%(F)s_EventScript_EeveeFanfare::\n\tbufferspeciesname STR_VAR_1, SPECIES_EEVEE\n"
            "\tplayfanfare MUS_OBTAIN_ITEM\n\tmessage %(F)s_Text_ReceivedEevee\n\twaitmessage\n\twaitfanfare\n"
            "\treturn\n\n"
            "%(F)s_EventScript_EeveeDone::\n\tsetflag FLAG_HOLON_RECEIVED_EEVEE\n"
            "\tmsgbox %(F)s_Text_HeadAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n\n"
            "%(F)s_EventScript_HeadDeclined::\n\tmsgbox %(F)s_Text_HeadDeclined, MSGBOX_DEFAULT\n\trelease\n\tend\n\n"
            "%(F)s_EventScript_HeadAfter::\n\tmsgbox %(F)s_Text_HeadAfter, MSGBOX_DEFAULT\n\trelease\n\tend\n`\n"
            % {"F": F}
            + text_block(F + "_Text_HeadOffer", s["offer"]) + text_block(F + "_Text_HeadDeclined", s["declined"])
            + text_block(F + "_Text_HeadAfter", s["after"])
            + '\ntext %s_Text_ReceivedEevee {\n    "{PLAYER} received {STR_VAR_1}!"\n}\n' % F)


# ---------------------------------------------------------------------------------------------- lake
GYARADOS = (40, 44)          # shiny Gyarados static, in the south bay (Surf)


def lake():
    F, name = "HolonLake", "holon_lake"
    objs = [obj("OBJ_EVENT_GFX_HOLON_SPHERE", sp.L_SPHERE[0], sp.L_SPHERE[1], 3, "MOVEMENT_TYPE_NONE",
                F + "_EventScript_Sphere", local_id="LOCALID_HOLON_SPHERE"),
            # TODO(trainers): Cynthia OW gfx (npc_white) + her battle script; placeholder woman sprite
            obj("OBJ_EVENT_GFX_WOMAN_2", 24, 35, elev_at(name, 24, 35), FACE["up"], F + "_EventScript_Cynthia",
                local_id="LOCALID_HOLON_CYNTHIA"),
            obj("OBJ_EVENT_GFX_EXPERT_M", 16, 45, elev_at(name, 16, 45), FACE["look"], F + "_EventScript_Mentor"),
            # TODO(delta): OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS_DELTA)
            obj("OBJ_EVENT_GFX_SPECIES_SHINY(GYARADOS)", GYARADOS[0], GYARADOS[1], 1, FACE["look"],
                F + "_EventScript_Gyarados", flag="FLAG_HOLON_HIDE_GYARADOS", local_id="LOCALID_HOLON_GYARADOS")]
    pory = ("raw `\n%(F)s_MapScripts::\n\tmap_script MAP_SCRIPT_ON_RESUME, %(F)s_OnResume\n"
            "\tmap_script MAP_SCRIPT_ON_TRANSITION, %(F)s_OnTransition\n\t.byte 0\n\n"
            "%(F)s_OnTransition:\n\tsetflag FLAG_VISITED_HOLON_LAKE\n\tend\n\n"
            "%(F)s_OnResume:\n\tcall_if_set HOLON_SPHERE_GLOW_FLAG, %(F)s_EventScript_SphereGlowOn\n"
            "\tcall_if_set FLAG_SYS_CTRL_OBJ_DELETE, %(F)s_EventScript_TryRemoveGyarados\n\tend\n\n"
            "%(F)s_EventScript_SphereGlowOn::\n\tcallnative Holon_SetSphereGlow\n\treturn\n\n"
            "%(F)s_EventScript_TryRemoveGyarados::\n\tspecialvar VAR_RESULT, GetBattleOutcome\n"
            "\tgoto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn\n"
            "\tremoveobject VAR_LAST_TALKED\n\treturn\n\n"
            "%(F)s_EventScript_Sphere::\n\tlock\n"
            "\tgoto_if_set HOLON_SPHERE_GLOW_FLAG, %(F)s_EventScript_SphereAwake\n"
            "\tmsgbox %(F)s_Text_SphereDormant, MSGBOX_DEFAULT\n\trelease\n\tend\n\n"
            "%(F)s_EventScript_SphereAwake::\n\tmsgbox %(F)s_Text_SphereAwake, MSGBOX_DEFAULT\n\trelease\n\tend\n\n"
            "@ Called once Cynthia is beaten (trainers stream): the sphere's OBJ palette swaps to the glow copy.\n"
            "Holon_EventScript_AwakenSphere::\n\tsetflag HOLON_SPHERE_GLOW_FLAG\n\tcallnative Holon_SetSphereGlow\n"
            "\tplayse SE_M_DETECT\n\twaitse\n\treturn\n\n"
            "%(F)s_EventScript_Cynthia::\n\tlock\n\tfaceplayer\n"
            "\t@ TODO(trainers): replace with Cynthia's battle script (encounter music, trainerbattle, then\n"
            "\t@ call Holon_EventScript_AwakenSphere and hide her here / move her to the Changu Battle Cafe)\n"
            "\tcall Holon_CynthiaPlaceholder\n\trelease\n\tend\n\n"
            "Holon_CynthiaPlaceholder::\n\tmsgbox %(F)s_Text_CynthiaPlaceholder, MSGBOX_DEFAULT\n\treturn\n\n"
            "%(F)s_EventScript_Gyarados::\n\tlock\n\tfaceplayer\n"
            "\t@ TODO(delta): SPECIES_GYARADOS -> SPECIES_GYARADOS_DELTA (shiny Gyarados-delta static, Lv 65)\n"
            "\twaitse\n\tplaymoncry SPECIES_GYARADOS, CRY_MODE_ENCOUNTER\n\tdelay 40\n\twaitmoncry\n"
            "\tsetwildbattle SPECIES_GYARADOS, 65\n"
            "\tcreatemon 1, 0, SPECIES_GYARADOS, 65, shinyMode=SHINY_MODE_ALWAYS\n"
            "\tsetflag FLAG_SYS_CTRL_OBJ_DELETE\n\tdowildbattle\n\tclearflag FLAG_SYS_CTRL_OBJ_DELETE\n"
            "\tspecialvar VAR_RESULT, GetBattleOutcome\n"
            "\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, %(F)s_EventScript_GyaradosGone\n"
            "\tgoto_if_eq VAR_RESULT, B_OUTCOME_RAN, %(F)s_EventScript_GyaradosStays\n"
            "\tgoto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, %(F)s_EventScript_GyaradosStays\n"
            "\tsetflag FLAG_HOLON_HIDE_GYARADOS\n\trelease\n\tend\n\n"
            "%(F)s_EventScript_GyaradosGone::\n\tsetflag FLAG_HOLON_HIDE_GYARADOS\n"
            "\tgoto Common_EventScript_RemoveStaticPokemon\n\tend\n\n"
            "%(F)s_EventScript_GyaradosStays::\n\tmsgbox %(F)s_Text_GyaradosDived, MSGBOX_DEFAULT\n\trelease\n\tend\n`\n"
            % {"F": F})
    L = T.LAKE
    pory += text_block(F + "_Text_SphereDormant", L["sphere"]) + text_block(F + "_Text_SphereAwake", L["sphere_glow"])
    pory += text_block(F + "_Text_CynthiaPlaceholder", L["cynthia_placeholder"])
    pory += text_block(F + "_Text_GyaradosDived", L["gyarados_ran"])
    pory += msg_script(F + "_EventScript_Mentor", L["mentor"])
    for n, (x, y, face, key) in enumerate([(8, 36, "right", "l1"), (40, 13, "left", "l2")], 1):
        lab, s = trainer_script(F, n, key)
        objs.append(obj(RESEARCHER_GFX, x, y, elev_at(name, x, y), FACE[face], lab, trainer=True, sight=4))
        pory += s
    bgs = [sign(28, 6, F + "_EventScript_Sign")]
    for tx, ty in sp.L_TOMBS:
        bgs.append(sign(tx + 2, ty + 3, F + "_EventScript_SealedDome", "BG_EVENT_PLAYER_FACING_NORTH"))
    for _n, (px, py) in sp.L_PILLARS.items():
        bgs.append(sign(px, py, F + "_EventScript_Pillar"))
    pory += msg_script(F + "_EventScript_Sign", L["sign"], "MSGBOX_SIGN")
    pory += msg_script(F + "_EventScript_SealedDome", L["dome"], "MSGBOX_SIGN")
    pory += msg_script(F + "_EventScript_Pillar", L["pillar"], "MSGBOX_SIGN")
    j = map_json("MAP_HOLON_LAKE", F, "LAYOUT_HOLON_LAKE", "MUS_ROUTE120", "MAPSEC_HOLON_LAKE", "MAP_TYPE_ROUTE",
                 conns=[OrderedDict([("map", "MAP_HOLON_VILLAGE"), ("offset", 0), ("direction", "up")])],
                 objs=objs, bgs=bgs)
    add_map(F, j, pory)


# ---------------------------------------------------------------------------------------------- write
def write_maps():
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    if GROUP not in mg["group_order"]:
        mg["group_order"].append(GROUP)
    mg[GROUP] = list(MAPS.keys())
    write_json(mg_path, mg)
    for folder, (j, pory) in MAPS.items():
        write_json(P("data", "maps", folder, "map.json"), j)
        open(P("data", "maps", folder, "scripts.pory"), "w").write(pory)
        stale = P("data", "maps", folder, "scripts.inc")
        if os.path.exists(stale):
            os.remove(stale)
    es = P("data", "event_scripts.s")
    lines = open(es).read().split("\n")
    lines = [l for l in lines if "@ holon-maps" not in l]
    last = max(i for i, l in enumerate(lines) if l.strip().startswith('.include "data/maps/'))
    new = ['\t.include "data/maps/%s/scripts.inc" @ holon-maps' % f for f in MAPS]
    lines[last + 1:last + 1] = new
    open(es, "w").write("\n".join(lines))
    # heal location (Centre door (6,35); respawn in front of it)
    hp = P("src", "data", "heal_locations.json")
    heal = json.load(open(hp), object_pairs_hook=OrderedDict)
    heal["heal_locations"] = [e for e in heal["heal_locations"] if e["id"] != "HEAL_LOCATION_HOLON_VILLAGE"]
    cx, cy = sp.V_BUILD["Centre"][1] + 2, sp.V_BUILD["Centre"][2] + 4
    heal["heal_locations"].append(OrderedDict([
        ("id", "HEAL_LOCATION_HOLON_VILLAGE"), ("map", "MAP_HOLON_VILLAGE"), ("x", cx), ("y", cy + 1),
        ("respawn_map", "MAP_HOLON_VILLAGE_POKEMON_CENTER_1F"), ("respawn_npc", "LOCALID_HOLON_VILLAGE_NURSE")]))
    write_json(hp, heal)


# ---------------------------------------------------------------------------------------------- wild
WILD_MAPS = {"Mirage Forest coast": ("MAP_HOLON_MIRAGE_FOREST", "gHolonMirageForest"),
             "Holon village": ("MAP_HOLON_VILLAGE", "gHolonVillage"),
             "Holon Lake": ("MAP_HOLON_LAKE", "gHolonLake"),
             "Holon Research Tower": ("MAP_HOLON_RESEARCH_TOWER_1F", "gHolonResearchTower_1F")}
RATES = {"land_mons": 20, "water_mons": 4, "rock_smash_mons": 20, "fishing_mons": 30}


def species_const(name, delta):
    base = name.replace("-δ", "").replace("'", "").replace(".", "").replace(" ", "_").replace("-", "_").upper()
    return "SPECIES_" + base + ("_DELTA" if delta and "-δ" in name else "")


def wild_tables():
    import csv
    rows = list(csv.DictReader(open(os.path.join(HERE, "wild_tables.csv"))))
    tables = OrderedDict()      # (map key, time) -> {type: [rows]}
    for r in rows:
        key = r["map"].split(" (")[0]
        t = r["table"]
        typ = {"land": "land_mons", "water": "water_mons", "rock_smash": "rock_smash_mons"}.get(t, "fishing_mons")
        tables.setdefault((key, r["time"]), OrderedDict()).setdefault(typ, []).append(r)
    built = {False: [], True: []}
    for delta in (False, True):
        for (key, time), types in tables.items():
            mid, label = WILD_MAPS[key]
            e = OrderedDict([("map", mid), ("base_label", label + ("_Night" if time == "night" else ""))])
            # day tables also carry the time-independent water / rock smash / fishing tables; night tables get a copy
            merged = OrderedDict(types)
            if time in ("day", "night"):
                for (k2, t2), ty2 in tables.items():
                    if k2 == key and t2 == "any":
                        merged.update(ty2)
            elif any(k2 == key and t2 in ("day", "night") for (k2, t2) in tables):
                continue
            for typ, rs in merged.items():
                if typ == "fishing_mons":
                    order = {"old_rod": 0, "good_rod": 1, "super_rod": 2}
                    rs = sorted(rs, key=lambda r: (order[r["table"]], int(r["slot"])))
                else:
                    rs = sorted(rs, key=lambda r: int(r["slot"]))
                e[typ] = OrderedDict([("encounter_rate", RATES[typ]), ("mons", [
                    OrderedDict([("min_level", int(r["min_lv"])), ("max_level", int(r["max_lv"])),
                                 ("species", species_const(r["species"], delta))]) for r in rs])])
            built[delta].append(e)
    wp = P("src", "data", "wild_encounters.json")
    wj = json.load(open(wp), object_pairs_hook=OrderedDict)
    grp = wj["wild_encounter_groups"][0]
    labels = {e["base_label"] for e in built[False]}
    grp["encounters"] = [e for e in grp["encounters"] if e.get("base_label") not in labels] + built[False]
    write_json(wp, wj)
    write_json(os.path.join(HERE, "wild_delta.json"),
               OrderedDict([("_note", "Intended Holon tables with Delta species (SPECIES_<BASE>_DELTA); swap them "
                                      "into src/data/wild_encounters.json once the delta stream is merged "
                                      "(same map / base_label keys as the base-species tables installed now)."),
                            ("encounters", built[True])]))
    return built


def check_grass_rates(built):
    for e in built[False]:
        for typ, t in e.items():
            if typ.endswith("_mons"):
                n = {"land_mons": 12, "water_mons": 5, "rock_smash_mons": 5, "fishing_mons": 10}[typ]
                assert len(t["mons"]) == n, (e["base_label"], typ, len(t["mons"]))


def main():
    install_tilesets()
    build_layouts()
    coast()
    w = village()
    tower(w)
    lake()
    write_maps()
    built = wild_tables()
    check_grass_rates(built)
    for f, (j, _p) in MAPS.items():
        print("%-34s %-32s objs %2d warps %2d" % (f, j["layout"], len(j["object_events"]), len(j["warp_events"])))
    print("wild tables:", [e["base_label"] for e in built[False]])


if __name__ == "__main__":
    main()
