#!/usr/bin/env python3
"""World edits of the content polish (called by apply_polish.py apply; idempotent):
  - FLAG_SEVII_DOTTED_HOLE_OPEN / FLAG_SEVII_TANOBY_OPEN (0x26B / 0x26C) and the flag-gated doors
  - gTileset_SeviiIslands: + metatile 0x3D7 "open dotted door" (4 new tiles, MB_NON_ANIMATED_DOOR)
  - gTileset_HolonLab: Lab tiles/palettes + own metatiles/attributes with 0x29E = lab floor + MB_INDOOR_ENCOUNTER
  - Holon Research Tower 2F: encounter floor around the machines + the tower wild table (moved from 1F)
  - Holon Lake: 4 Rock Smash rocks on the shore
"""
import json
import os
import re
import struct
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)

FLAGS = [("FLAG_SEVII_DOTTED_HOLE_OPEN", 0x26B, "Ruin Valley's dotted door opens (default sealed)"),
         ("FLAG_SEVII_TANOBY_OPEN", 0x26C, "the seven Tanoby chamber doors open (default sealed)")]
SEVII_DOOR_MT = 0x3D7          # appended to gTileset_SeviiIslands
SEVII_NEW_TILES = 498          # first new tile (secondary index); -num_tiles 498 -> 502
LAB_FLOOR, LAB_ENC = 0x269, 0x29E
MB_NON_ANIMATED_DOOR, MB_INDOOR_ENCOUNTER = 0x60, 0x0B
RV_DOOR = (24, 24)
RV_SCIENTIST_OPEN = (26, 25)
TANOBY_DOOR_MT = 0x20A
LAKE_ROCKS = [(9, 23), (27, 41), (44, 26), (62, 24)]
TOWER_ENC_BOX = (6, 4, 16, 10)         # x0, y0, x1, y1 inclusive: the lab floor around the four machines


def jload(p):
    return json.load(open(p), object_pairs_hook=OrderedDict)


def jdump(p, d):
    open(p, "w").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def drop_inc(folder):
    inc = P("data", "maps", folder, "scripts.inc")
    if os.path.exists(inc):
        os.remove(inc)


# ------------------------------------------------------------------ flags
def flags():
    path = P("include", "constants", "flags.h")
    txt = open(path).read()
    for name, v, what in FLAGS:
        txt = re.sub(r"#define FLAG_UNUSED_0x%03X(\s+)0x%03X // Unused Flag\n" % (v, v),
                     "#define %s  0x%03X // Sevii (was FLAG_UNUSED_0x%03X): %s\n" % (name, v, v, what), txt)
        assert "#define %s " % name in txt, name
    open(path, "w").write(txt)
    fj = P("dev_scripts", "voyages", "sevii", "sevii_flags.json")
    d = json.load(open(fj))
    for name, v, _ in FLAGS:
        d[name] = "FLAG_UNUSED_0x%03X" % v
    json.dump(d, open(fj, "w"), indent=1, sort_keys=True)


# ------------------------------------------------------------------ Sevii tileset: opened dotted door
def sevii_door_tiles():
    from PIL import Image
    d = P("data", "tilesets", "secondary", "sevii_islands")
    im = Image.open(os.path.join(d, "tiles.png"))
    assert im.mode == "P"
    W = im.size[0] // 8
    px = im.load()

    def get(t):
        return [[px[(t % W) * 8 + x, (t // W) * 8 + y] for x in range(8)] for y in range(8)]

    def put(t, rows):
        for y in range(8):
            for x in range(8):
                px[(t % W) * 8 + x, (t // W) * 8 + y] = rows[y][x]

    # 16x16 slab = tiles 0x100..0x103 (TL, TR, BL, BR), palette 3. Keep the stone frame, hollow the slab out:
    # 8 = darkest (65,49,65), e = (98,65,82) for the lintel shadow, d = frame brown.
    src = [get(0x100 + i) for i in range(4)]
    g = [[0] * 16 for _ in range(16)]
    for i, tile in enumerate(src):
        ox, oy = (i % 2) * 8, (i // 2) * 8
        for y in range(8):
            for x in range(8):
                g[oy + y][ox + x] = tile[y][x]
    for y in range(2, 14):
        for x in range(2, 14):
            g[y][x] = 0xE if y == 2 else 0x8
    for x in range(16):                       # sill: the slab's grey bottom edge becomes frame brown
        if g[15][x] == 0x5:
            g[15][x] = 0xD
    for i in range(4):
        ox, oy = (i % 2) * 8, (i // 2) * 8
        put(SEVII_NEW_TILES + i, [g[oy + y][ox:ox + 8] for y in range(8)])
    im.save(os.path.join(d, "tiles.png"))

    gh = P("src", "data", "tilesets", "graphics.h")
    t = open(gh).read()
    t = t.replace('sevii_islands/tiles.png", ".4bpp.fastSmol", "-num_tiles %d -Wnum_tiles"' % SEVII_NEW_TILES,
                  'sevii_islands/tiles.png", ".4bpp.fastSmol", "-num_tiles %d -Wnum_tiles"' % (SEVII_NEW_TILES + 4))
    assert "-num_tiles %d" % (SEVII_NEW_TILES + 4) in t
    open(gh, "w").write(t)

    mp, ap = os.path.join(d, "metatiles.bin"), os.path.join(d, "metatile_attributes.bin")
    mt, at = bytearray(open(mp, "rb").read()), bytearray(open(ap, "rb").read())
    idx = SEVII_DOOR_MT - 0x200
    entry = struct.pack("<8H", *[(0x200 + SEVII_NEW_TILES + i) | (3 << 12) for i in range(4)], 0, 0, 0, 0)
    attr = struct.pack("<H", MB_NON_ANIMATED_DOOR)
    if len(mt) // 16 == idx:
        mt += entry
        at += attr
    else:
        assert len(mt) // 16 == idx + 1
        mt[idx * 16:(idx + 1) * 16] = entry
        at[idx * 2:idx * 2 + 2] = attr
    open(mp, "wb").write(mt)
    open(ap, "wb").write(at)

    lp = P("include", "constants", "metatile_labels.h")
    lt = open(lp).read()
    if "METATILE_SeviiIslands_DottedDoor_Open" not in lt:
        last = list(re.finditer(r"#define METATILE_SeviiIslands_\w+\s+0x[0-9A-F]+\n", lt))[-1]
        lt = lt[:last.end()] + "#define METATILE_SeviiIslands_DottedDoor_Open                 0x%03X\n" % SEVII_DOOR_MT \
            + lt[last.end():]
        open(lp, "w").write(lt)


# ------------------------------------------------------------------ Ruin Valley + Tanoby doors
RV_MAPSCRIPTS = """mapscripts SixIsland_RuinValley_MapScripts {
    MAP_SCRIPT_ON_LOAD {
        if (flag(FLAG_SEVII_DOTTED_HOLE_OPEN)) {
            setmetatile(%d, %d, METATILE_SeviiIslands_DottedDoor_Open, FALSE)
        }
    }
    MAP_SCRIPT_ON_TRANSITION {
        if (flag(FLAG_SEVII_DOTTED_HOLE_OPEN)) {
            setobjectxyperm(LOCALID_RUIN_VALLEY_SCIENTIST, %d, %d)
            setobjectmovementtype(LOCALID_RUIN_VALLEY_SCIENTIST, MOVEMENT_TYPE_FACE_LEFT)
        }
    }
}
""" % (RV_DOOR + RV_SCIENTIST_OPEN)


def ruin_valley():
    f = "SixIsland_RuinValley"
    mp = P("data", "maps", f, "map.json")
    m = jload(mp)
    sci = next(o for o in m["object_events"] if o["script"] == f + "_EventScript_Scientist")
    if "local_id" not in sci:
        new = OrderedDict([("local_id", "LOCALID_RUIN_VALLEY_SCIENTIST")])
        new.update(sci)
        m["object_events"][m["object_events"].index(sci)] = new
    jdump(mp, m)
    sp = P("data", "maps", f, "scripts.pory")
    s = open(sp).read()
    s = re.sub(r"mapscripts SixIsland_RuinValley_MapScripts \{\}\n|mapscripts SixIsland_RuinValley_MapScripts \{\n.*?\n\}\n",
               RV_MAPSCRIPTS, s, count=1, flags=re.S)
    s = re.sub(r"script SixIsland_RuinValley_EventScript_Scientist \{\n.*?\n\}\n",
               'script SixIsland_RuinValley_EventScript_Scientist {\n'
               '    if (flag(FLAG_SEVII_DOTTED_HOLE_OPEN)) {\n'
               '        msgbox(format("The dotted door finally opened! I only hope what\'s down there is friendly."), MSGBOX_NPC)\n'
               '    } else {\n'
               '        msgbox(format("That dotted door is a puzzle from ancient times. I\'ve studied it for years with no luck."), MSGBOX_NPC)\n'
               '    }\n}\n', s, count=1, flags=re.S)
    s = re.sub(r"script SixIsland_RuinValley_EventScript_Sealed \{\n(.*?)\n\}\n",
               lambda mm: mm.group(0) if "FLAG_SEVII_DOTTED_HOLE_OPEN" in mm.group(1) else
               "script SixIsland_RuinValley_EventScript_Sealed {\n    if (flag(FLAG_SEVII_DOTTED_HOLE_OPEN)) {\n"
               "        end\n    }\n" + mm.group(1) + "\n}\n", s, count=1, flags=re.S)
    open(sp, "w").write(s)
    drop_inc(f)


def tanoby():
    f = "SevenIsland_TanobyRuins"
    mp = P("data", "maps", f, "map.json")
    m = jload(mp)
    doors = [(w["x"], w["y"], w["dest_map"]) for w in m["warp_events"] if "CHAMBER" in w["dest_map"]]
    assert len(doors) == 7
    coords = [c for c in (m.get("coord_events") or []) if not c["script"].startswith(f + "_EventScript_EnterChamber")]
    scripts = []
    for x, y, dest in doors:
        lab = "%s_EventScript_EnterChamber_%d_%d" % (f, x, y)
        coords.append(OrderedDict([("type", "trigger"), ("x", x), ("y", y), ("elevation", 0), ("var", "VAR_TEMP_1"),
                                   ("var_value", "0"), ("script", lab)]))
        scripts.append("script %s {\n    if (flag(FLAG_SEVII_TANOBY_OPEN)) {\n        warp(%s, 0)\n"
                       "    }\n}\n" % (lab, dest))
    m["coord_events"] = coords
    jdump(mp, m)
    sp = P("data", "maps", f, "scripts.pory")
    s = open(sp).read()
    ons = "".join("            setmetatile(%d, %d, 0x%03X, FALSE)\n" % (x, y, TANOBY_DOOR_MT) for x, y, _ in doors)
    ms = ("mapscripts SevenIsland_TanobyRuins_MapScripts {\n    MAP_SCRIPT_ON_LOAD {\n"
          "        if (flag(FLAG_SEVII_TANOBY_OPEN)) {\n" + ons + "        }\n    }\n}\n")
    s = re.sub(r"mapscripts SevenIsland_TanobyRuins_MapScripts \{\}\n|mapscripts SevenIsland_TanobyRuins_MapScripts \{\n.*?\n\}\n",
               ms, s, count=1, flags=re.S)
    s = re.sub(r"script SevenIsland_TanobyRuins_EventScript_Sealed \{\n(.*?)\n\}\n",
               lambda mm: mm.group(0) if "FLAG_SEVII_TANOBY_OPEN" in mm.group(1) else
               "script SevenIsland_TanobyRuins_EventScript_Sealed {\n    if (flag(FLAG_SEVII_TANOBY_OPEN)) {\n"
               "        end\n    }\n" + mm.group(1) + "\n}\n", s, count=1, flags=re.S)
    s = re.sub(r"\n// polish: chamber doors.*", "\n", s, flags=re.S).rstrip("\n") + "\n"
    s += "\n// polish: chamber doors (coord triggers; the door metatile is TanobyDelta's, shared with Tiksi)\n" + \
        "\n".join(scripts)
    open(sp, "w").write(s)
    drop_inc(f)


# ------------------------------------------------------------------ Holon Research Tower
TOWER_TABLE = [("SPECIES_MAGNEMITE", 55, 57), ("SPECIES_VOLTORB", 55, 57), ("SPECIES_MAGNETON", 57, 57),
               ("SPECIES_KLINK_DELTA", 55, 55), ("SPECIES_CASTFORM", 56, 56), ("SPECIES_ELECTRODE", 57, 57),
               ("SPECIES_BELDUM_DELTA", 55, 55), ("SPECIES_KLANG_DELTA", 57, 57), ("SPECIES_METANG_DELTA", 58, 58),
               ("SPECIES_PORYGON2", 58, 58), ("SPECIES_KLINKLANG_DELTA", 60, 60), ("SPECIES_METAGROSS_DELTA", 62, 62)]


def holon_lab():
    src = P("data", "tilesets", "secondary", "lab")
    dst = P("data", "tilesets", "secondary", "holon_lab")
    os.makedirs(dst, exist_ok=True)
    mt = bytearray(open(os.path.join(src, "metatiles.bin"), "rb").read())
    at = bytearray(open(os.path.join(src, "metatile_attributes.bin"), "rb").read())
    assert len(mt) // 16 == LAB_ENC - 0x200, hex(len(mt) // 16 + 0x200)
    i = LAB_FLOOR - 0x200
    mt += mt[i * 16:(i + 1) * 16]
    a = struct.unpack("<H", at[i * 2:i * 2 + 2])[0]
    at += struct.pack("<H", (a & ~0xFF) | MB_INDOOR_ENCOUNTER)
    open(os.path.join(dst, "metatiles.bin"), "wb").write(mt)
    open(os.path.join(dst, "metatile_attributes.bin"), "wb").write(at)

    mh = P("src", "data", "tilesets", "metatiles.h")
    t = open(mh).read()
    if "gMetatiles_HolonLab" not in t:
        anchor = 'const u16 gMetatileAttributes_Lab[] = INCBIN_U16("data/tilesets/secondary/lab/metatile_attributes.bin");\n'
        assert anchor in t
        t = t.replace(anchor, anchor +
                      "\n// Orchid Holon: Lab metatiles + 0x29E (lab floor 0x269 with MB_INDOOR_ENCOUNTER) for Research Tower 2F\n"
                      'const u16 gMetatiles_HolonLab[] = INCBIN_U16("data/tilesets/secondary/holon_lab/metatiles.bin");\n'
                      'const u16 gMetatileAttributes_HolonLab[] = INCBIN_U16("data/tilesets/secondary/holon_lab/metatile_attributes.bin");\n')
        open(mh, "w").write(t)
    hh = P("src", "data", "tilesets", "headers.h")
    t = open(hh).read()
    if "gTileset_HolonLab" not in t:
        anchor = "const struct Tileset gTileset_Underwater ="
        t = t.replace(anchor,
                      "// Orchid Holon: gTileset_Lab's tiles and palettes with its own metatiles (+ an encounter copy of the\n"
                      "// lab floor). Only Holon Research Tower 2F uses it; gTileset_Lab stays untouched.\n"
                      "const struct Tileset gTileset_HolonLab =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
                      "    .tiles = gTilesetTiles_Lab,\n    .palettes = gTilesetPalettes_Lab,\n"
                      "    .metatiles = gMetatiles_HolonLab,\n    .metatileAttributes = gMetatileAttributes_HolonLab,\n"
                      "    .callback = NULL,\n};\n\n" + anchor, 1)
        open(hh, "w").write(t)
    lp = P("include", "constants", "metatile_labels.h")
    lt = open(lp).read()
    if "METATILE_HolonLab_EncounterFloor" not in lt:
        lt = lt.replace("#define METATILE_SeviiIslands_DottedDoor_Open",
                        "#define METATILE_HolonLab_EncounterFloor                      0x%03X\n"
                        "#define METATILE_SeviiIslands_DottedDoor_Open" % LAB_ENC, 1)
        assert "METATILE_HolonLab_EncounterFloor" in lt
        open(lp, "w").write(lt)

    lj = P("data", "layouts", "layouts.json")
    js = jload(lj)
    e = next(l for l in js["layouts"] if l.get("id") == "LAYOUT_HOLON_RESEARCH_TOWER_2F")
    e["secondary_tileset"] = "gTileset_HolonLab"
    jdump(lj, js)
    bp = P(e["blockdata_filepath"])
    w, h = e["width"], e["height"]
    v = list(struct.unpack("<%dH" % (w * h), open(bp, "rb").read()[:2 * w * h]))
    x0, y0, x1, y1 = TOWER_ENC_BOX
    n = 0
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = v[y * w + x]
            if c & 0x3FF in (LAB_FLOOR, LAB_ENC) and not (c >> 10) & 3:
                v[y * w + x] = (c & ~0x3FF) | LAB_ENC
                n += 1
    open(bp, "wb").write(struct.pack("<%dH" % (w * h), *v))
    print("tower 2F: %d encounter cells" % n)

    wp = P("src", "data", "wild_encounters.json")
    raw = open(wp).read()
    d = json.loads(raw, object_pairs_hook=OrderedDict)
    enc = d["wild_encounter_groups"][0]["encounters"]
    ent = next(x for x in enc if x["map"] in ("MAP_HOLON_RESEARCH_TOWER_1F", "MAP_HOLON_RESEARCH_TOWER_2F"))
    ent["map"] = "MAP_HOLON_RESEARCH_TOWER_2F"
    ent["base_label"] = "gHolonResearchTower_2F"
    ent["land_mons"]["encounter_rate"] = 10
    ent["land_mons"]["mons"] = [OrderedDict([("min_level", lo), ("max_level", hi), ("species", sp)])
                                for sp, lo, hi in TOWER_TABLE]
    indent = 2 if raw.startswith("{\n  \"") else 4
    open(wp, "w").write(json.dumps(d, indent=indent, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ Holon Lake rocks
def lake_rocks():
    mp = P("data", "maps", "HolonLake", "map.json")
    m = jload(mp)
    # the lake had no rocks before this pass: drop any (older placements) and add the current list
    m["object_events"] = [o for o in m["object_events"] if o["graphics_id"] != "OBJ_EVENT_GFX_BREAKABLE_ROCK"]
    for x, y in LAKE_ROCKS:
        m["object_events"].append(OrderedDict([
            ("graphics_id", "OBJ_EVENT_GFX_BREAKABLE_ROCK"), ("x", x), ("y", y), ("elevation", 3),
            ("movement_type", "MOVEMENT_TYPE_LOOK_AROUND"), ("movement_range_x", 0), ("movement_range_y", 0),
            ("trainer_type", "TRAINER_TYPE_NONE"), ("trainer_sight_or_berry_tree_id", "0"),
            ("script", "EventScript_RockSmash"), ("flag", "0")]))
    jdump(mp, m)


def main():
    flags()
    sevii_door_tiles()
    ruin_valley()
    tanoby()
    holon_lab()
    lake_rocks()


if __name__ == "__main__":
    main()
