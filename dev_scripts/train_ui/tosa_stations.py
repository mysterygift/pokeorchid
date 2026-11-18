#!/usr/bin/env python3
"""
Tosa Rail: the real network (round 3, approved 2026-11-18) — every station's maps and data from one
table. Re-runnable: rewrites what it owns, leaves everything else alone.

Per station (Tosa Port already exists; its platform is only recoloured):
    <Town>                  placeholder exterior: the Tosa Port gatehouse building in a small clearing
                            (the user builds the real town around it later)
    <Town>_Station          concourse: copy of the Tosa Port gatehouse without its story NPCs or
                            rear arch; fare gates reuse TosaGateway_FareGateNorth/South
    <Town>_StationPlatform  platform: copy of the Tosa Port platform, wall in the line's colour
                            (gTileset_UrbanPlatform; interchanges split the wall per line)
All new maps go in gMapGroup_TosaRail.

Writes
    include/constants/train_stations.h      ids (test stations removed)
    include/constants/flags.h               FLAG_TRAIN_UNLOCK_* / FLAG_TRAIN_CLOSED_* pairs
    src/data/train_stations.h               station table
    data/maps/<map>/{map.json,scripts.pory}, data/maps/map_groups.json, data/event_scripts.s includes
    data/layouts/<layout>/{map.bin,border.bin}, data/layouts/layouts.json
    data/layouts/TosaPort_BrendansHouse_2F  West (purple) wall, gTileset_UrbanPlatform
    dev_scripts/train_ui/network.json       station map network (then run export_station_map.py)

usage: python3 dev_scripts/train_ui/tosa_stations.py
"""
import json
import os
import re
import struct
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)

# ---------------------------------------------------------------- the network
# key, station name, map prefix, region map section, lines, town visited flag, music, map type
STATIONS = [
    ("TOSA_PORT",      "TOSA PORT",      "TosaPort",      "MAPSEC_TOSA_PORT",      ("west",),                     "FLAG_VISITED_TOSA_PORT",       None,             None),
    ("MOONGROVE_CITY", "MOONGROVE CITY", "MoongroveCity", "MAPSEC_MOONGROVE_CITY", ("west",),                     "FLAG_VISITED_MOSSDEEP_CITY",   "MUS_RUSTBORO",   "MAP_TYPE_CITY"),
    ("TIMAH_CITY",     "TIMAH CITY",     "TimahCity",     "MAPSEC_TIMAH_CITY",     ("west",),                     "FLAG_VISITED_PETALBURG_CITY",  "MUS_PETALBURG",  "MAP_TYPE_CITY"),
    ("FABER_TOWN",     "FABER TOWN",     "FaberTown",     "MAPSEC_FABER_TOWN",     ("west",),                     "0",                            "MUS_FALLARBOR",  "MAP_TYPE_TOWN"),
    ("CHANGU_CITY",    "CHANGU CITY",    "ChanguCity",    "MAPSEC_CHANGU_CITY",    ("west", "central", "east"),   "FLAG_VISITED_SLATEPORT_CITY",  "MUS_SLATEPORT",  "MAP_TYPE_CITY"),
    ("CHANGU_AIRPORT", "CHANGU AIRPORT", "ChanguAirport", "MAPSEC_CHANGU_AIRPORT", ("central",),                  "0",                            "MUS_SLATEPORT",  "MAP_TYPE_CITY"),
    ("INKA_CITY",      "INKA CITY",      "InkaCity",      "MAPSEC_INKA_CITY",      ("central",),                  "FLAG_VISITED_RUSTBORO_CITY",   "MUS_RUSTBORO",   "MAP_TYPE_CITY"),
    ("BURA_CITY",      "BURA CITY",      "BuraCity",      "MAPSEC_BURA_CITY",      ("central",),                  "0",                            "MUS_VERDANTURF", "MAP_TYPE_CITY"),
    ("JURAN_CITY",     "JURAN CITY",     "JuranCity",     "MAPSEC_JURAN_CITY",     ("central", "poketopia"),      "FLAG_VISITED_LILYCOVE_CITY",   "MUS_LILYCOVE",   "MAP_TYPE_CITY"),
    ("SENOKO_CITY",    "SENOKO CITY",    "SenokoCity",    "MAPSEC_SENOKO_CITY",    ("east",),                     "FLAG_VISITED_MAUVILLE_CITY",   "MUS_RUSTBORO",   "MAP_TYPE_CITY"),
    ("POKEMON_LEAGUE", "POKéMON LEAGUE", "PokemonLeague", "MAPSEC_PKMN_LEAGUE",    ("east",),                     "0",                            "MUS_EVER_GRANDE", "MAP_TYPE_CITY"),
    ("POKETOPIA_GATE", "POKéTOPIA GATE", "PoketopiaGate", "MAPSEC_POKETOPIA_GATE", ("poketopia",),                "0",                            "MUS_LILYCOVE",   "MAP_TYPE_TOWN"),
    ("CORRAL_CITY",    "CORRAL CITY",    "CorralCity",    "MAPSEC_CORRAL_CITY",    ("poketopia",),                "FLAG_VISITED_SOOTOPOLIS_CITY", "MUS_SOOTOPOLIS", "MAP_TYPE_CITY"),
]
# station-map lines: key, legend name, BG palette slot of the tube colour (export_station_map.py)
LINES = [("west", "WEST", 0), ("central", "CENTRAL", 1), ("east", "EAST", 2), ("poketopia", "POKéTOPIA", 6)]

# unlock / closed flag pairs, in station order (0x40-0x4F were the Tosa Rail block; 0x30-0x39 were unused)
FLAG_SLOTS = [0x40, 0x42, 0x44, 0x46, 0x48, 0x4A, 0x4C, 0x4E, 0x30, 0x32, 0x34, 0x36, 0x38]


def c(cx, cy):
    """station-map canvas cell -> pixel centre (8k+4)"""
    return cx * 8 + 4, cy * 8 + 4


# station-map layout (round 3 mock, re-routed so lines leave every node at least 90 deg apart; the
# exporter rejects a cell shared by two edges): node cell, label (anchor, dx, dy)
DIAGRAM = {
    "TOSA_PORT": ((3, 22), ("c", 0, 6)),       "MOONGROVE_CITY": ((9, 22), ("r", 7, 6)),
    "TIMAH_CITY": ((13, 3), ("c", 0, -18)),    "FABER_TOWN": ((18, 3), ("r", 7, -6)), 
    "CHANGU_CITY": ((23, 12), ("l", -8, 6)),   "CHANGU_AIRPORT": ((23, 17), ("r", 7, -6)),
    "INKA_CITY": ((23, 27), ("c", 0, 6)),      "BURA_CITY": ((38, 12), ("c", 0, -18)),
    "JURAN_CITY": ((43, 22), ("r", 8, -18)),   "SENOKO_CITY": ((56, 8), ("c", 0, 6)),
    "POKEMON_LEAGUE": ((43, 3), ("c", 0, 6)),  "POKETOPIA_GATE": ((51, 27), ("c", 0, 6)),
    "CORRAL_CITY": ((59, 27), ("c", -6, -18)),
}
EDGES = [  # a, b, line, bend cells
    ("TOSA_PORT", "MOONGROVE_CITY", "west", []), ("MOONGROVE_CITY", "TIMAH_CITY", "west", [(9, 7)]),
    ("TIMAH_CITY", "FABER_TOWN", "west", []), ("FABER_TOWN", "CHANGU_CITY", "west", [(18, 12)]),
    ("CHANGU_CITY", "BURA_CITY", "central", []), ("BURA_CITY", "JURAN_CITY", "central", [(43, 17)]),
    ("JURAN_CITY", "INKA_CITY", "central", [(38, 27)]), ("INKA_CITY", "CHANGU_AIRPORT", "central", []),
    ("CHANGU_AIRPORT", "CHANGU_CITY", "central", []), ("CHANGU_CITY", "SENOKO_CITY", "east", [(23, 10), (25, 8)]),
    ("SENOKO_CITY", "POKEMON_LEAGUE", "east", [(56, 3)]),
    ("JURAN_CITY", "POKETOPIA_GATE", "poketopia", [(45, 22), (50, 27)]), ("POKETOPIA_GATE", "CORRAL_CITY", "poketopia", []),
]

# gTileset_UrbanPlatform shell blocks (dev_scripts/station_tileset/platform_tileset.py)
SHELL_FIRST = {"central": 0x201, "west": 0x210, "east": 0x21A, "poketopia": 0x224}
TRACK_X, TRACK_Y = 9, 4                       # boarding door tile on every platform (Tosa Port copy)
GROUP = "gMapGroup_TosaRail"


# ---------------------------------------------------------------- small helpers
def snake(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def map_id(name):
    return "MAP_" + snake(name)


def read_bin(path):
    d = open(path, "rb").read()
    return list(struct.unpack(f"<{len(d) // 2}H", d))


def write_bin(path, vals):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(struct.pack(f"<{len(vals)}H", *vals))


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def layout_entry(lid, name, w, h, primary, secondary, folder):
    return OrderedDict([("id", lid), ("name", name + "_Layout"), ("width", w), ("height", h),
                        ("primary_tileset", primary), ("secondary_tileset", secondary),
                        ("border_filepath", f"data/layouts/{folder}/border.bin"),
                        ("blockdata_filepath", f"data/layouts/{folder}/map.bin"),
                        ("layout_version", "emerald")])


def obj(gfx, x, y, script, facing="MOVEMENT_TYPE_FACE_DOWN", elevation=3):
    return OrderedDict([("graphics_id", gfx), ("x", x), ("y", y), ("elevation", elevation),
                        ("movement_type", facing), ("movement_range_x", 0), ("movement_range_y", 0),
                        ("trainer_type", "TRAINER_TYPE_NONE"), ("trainer_sight_or_berry_tree_id", "0"),
                        ("script", script), ("flag", "0")])


def warp(x, y, dest, wid, elevation=0):
    return OrderedDict([("x", x), ("y", y), ("elevation", elevation), ("dest_map", dest), ("dest_warp_id", str(wid))])


def sign(x, y, script):
    return OrderedDict([("type", "sign"), ("x", x), ("y", y), ("elevation", 0),
                        ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", script)])


def map_json(name, layout, music, mapsec, mtype, objects, warps, bgs, outdoor):
    return OrderedDict([
        ("id", map_id(name)), ("name", name), ("layout", layout), ("music", music), ("region", "REGION_HOENN"),
        ("region_map_section", mapsec), ("requires_flash", False),
        ("weather", "WEATHER_SUNNY" if outdoor else "WEATHER_NONE"), ("map_type", mtype),
        ("allow_cycling", outdoor), ("allow_escaping", False), ("allow_running", True), ("show_map_name", outdoor),
        ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None), ("object_events", objects),
        ("warp_events", warps), ("coord_events", []), ("bg_events", bgs)])


# ---------------------------------------------------------------- layouts
def exterior_blocks():
    """15x12 clearing with the Tosa Port gatehouse (TosaPort x 8-14, rows 2-7) and its door at (7, 7)."""
    W = 38
    tp = read_bin(P("data", "layouts", "TosaPort", "map.bin"))
    at = lambda x, y: tp[y * W + x]
    w, h = 15, 12
    grass = at(15, 2)
    g = [grass] * (w * h)
    for x in range(w):                                     # tree line (2x2 pattern by column parity)
        sx = 5 if x % 2 else 6
        g[0 * w + x], g[1 * w + x] = at(sx, 0), at(sx, 1)
    for y in range(6):
        for x in range(7):
            g[(2 + y) * w + 4 + x] = at(8 + x, 2 + y)
    g[8 * w + 6], g[8 * w + 7] = at(10, 8), at(11, 8)      # cobbles under the door
    return w, h, g


def concourse_blocks():
    w, h = 14, 11
    g = read_bin(P("data", "layouts", "TosaPort_BrendansHouse_1F", "map.bin"))
    for x in (5, 6):                                       # wall up the rear arch (Tosa Port only)
        g[0 * w + x], g[1 * w + x] = g[0 * w + 4], g[1 * w + 4]
    return w, h, g


def platform_blocks(lines, src=None):
    """Tosa Port platform with rows 0-3 (shell) recoloured; interchanges split the wall per line."""
    w, h = 20, 12
    g = src or read_bin(P("data", "layouts", "TosaPort_BrendansHouse_2F", "map.bin"))
    n = len(lines)
    for y in range(4):
        for x in range(w):
            v = g[y * w + x]
            mt = v & 0x3FF
            for base in SHELL_FIRST.values():
                if base <= mt < base + 10:
                    line = lines[min(n - 1, x * n // w)]
                    g[y * w + x] = (v & ~0x3FF) | (SHELL_FIRST[line] + mt - base)
                    break
    return w, h, g


# ---------------------------------------------------------------- writers
def write_constants():
    L = ["#ifndef GUARD_CONSTANTS_TRAIN_STATIONS_H", "#define GUARD_CONSTANTS_TRAIN_STATIONS_H", "",
         "// Tosa Rail stations. Order = order in src/data/train_stations.h.",
         "// GENERATED by dev_scripts/train_ui/tosa_stations.py (station table) - edit the table, not this file.", ""]
    for i, s in enumerate(STATIONS):
        L.append("#define TRAIN_STATION_%-16s %d" % (s[0], i))
    L += ["#define TRAIN_STATION_COUNT            %d" % len(STATIONS), "",
          "#define TRAIN_STATION_NONE          0xFF", "",
          "// settrainstation modes",
          "#define TRAIN_ACCESS_LOCKED         0   // back to default: accessible only once its town is visited",
          "#define TRAIN_ACCESS_OPEN           1   // accessible now, even if never visited (and not closed)",
          "#define TRAIN_ACCESS_CLOSED         2   // greyed out as \"closed\" even if visited", "",
          "// Station states, as shown on the station map",
          "#define TRAIN_STATION_STATE_UNVISITED   0", "#define TRAIN_STATION_STATE_OPEN        1",
          "#define TRAIN_STATION_STATE_CLOSED      2", "", "#endif // GUARD_CONSTANTS_TRAIN_STATIONS_H"]
    open(P("include", "constants", "train_stations.h"), "w").write("\n".join(L) + "\n")


def write_flags():
    path = P("include", "constants", "flags.h")
    s = open(path).read()
    pairs = {}
    for (key, *_), slot in zip(STATIONS, FLAG_SLOTS):
        pairs[slot] = "#define %-36s 0x%02X" % ("FLAG_TRAIN_UNLOCK_" + key, slot)
        pairs[slot + 1] = "#define %-36s 0x%02X" % ("FLAG_TRAIN_CLOSED_" + key, slot + 1)
    out = []
    for line in s.split("\n"):
        m = re.match(r"#define (FLAG_UNUSED_0x0([0-9A-F]{2})|FLAG_TRAIN_(UNLOCK|CLOSED)_\w+)\s+0x([0-9A-F]{2})\b", line)
        if m:
            val = int(m.group(4), 16)
            if val in pairs:
                out.append(pairs.pop(val))
                continue
            if m.group(1).startswith("FLAG_TRAIN_"):       # spare pair from the old block
                out.append("#define FLAG_UNUSED_0x%03X    0x%02X // Unused Flag" % (val, val))
                continue
        out.append(line)
    assert not pairs, "flag slots not found: %s" % sorted(pairs)
    open(path, "w").write("\n".join(out).replace(
        "// even when visited. Rename the spare STATION_n pairs when real stations are added.",
        "// even when visited. Pairs are written by dev_scripts/train_ui/tosa_stations.py (station order)."))


def write_station_table(maps):
    L = ["// Tosa Rail station table. Indexed by TRAIN_STATION_* (include/constants/train_stations.h).",
         "// GENERATED by dev_scripts/train_ui/tosa_stations.py - edit the station table there.", "//",
         "//   name         shown on the station map / confirm prompt",
         "//   mapGroup/Num the map the platform is on",
         "//   trackX/Y     map tile (no MAP_OFFSET) where the boarding door stops on arrival",
         "//   visitedFlag  FLAG_VISITED_* of the town (0 = none: using the station there marks it visited)",
         "//   unlockFlag   accessible even if never visited (settrainstation ..., TRAIN_ACCESS_OPEN)",
         "//   closedFlag   greyed out even if visited (settrainstation ..., TRAIN_ACCESS_CLOSED)",
         "//   (station map positions and lines live in dev_scripts/train_ui/network.json → src/data/train_station_map.h)", ""]
    for key, name, *_ in STATIONS:
        L.append('static const u8 sStationName_%s[] = _("%s");' % (key.title().replace("_", ""), name))
    L += ["", "static const struct TrainStation sTrainStations[TRAIN_STATION_COUNT] =", "{"]
    for key, name, prefix, mapsec, lines, vflag, *_ in STATIONS:
        plat = maps[key]
        L += ["    [TRAIN_STATION_%s] =" % key, "    {",
              "        .name = sStationName_%s," % key.title().replace("_", ""),
              "        .mapGroup = MAP_GROUP(%s)," % plat, "        .mapNum = MAP_NUM(%s)," % plat,
              "        .trackX = %d," % TRACK_X, "        .trackY = %d," % TRACK_Y,
              "        .visitedFlag = %s," % vflag,
              "        .unlockFlag = FLAG_TRAIN_UNLOCK_%s," % key, "        .closedFlag = FLAG_TRAIN_CLOSED_%s," % key,
              "    },"]
    L.append("};")
    open(P("src", "data", "train_stations.h"), "w").write("\n".join(L) + "\n")


def write_network():
    by_key = {s[0]: s for s in STATIONS}
    net = OrderedDict()
    net["_comment"] = ("Tosa Rail station-map network. GENERATED by tosa_stations.py (edit the table there). Source of "
                       "truth for export_station_map.py. Coordinates are canvas pixels on cell centres (8k+4), runs "
                       "0/45/90 deg. label = [anchor, dx, dy]: c centred, l ends left of the node, r starts right of it. "
                       "bgPalette: tube colour slot (0 orchid/purple, 1 sea/teal, 2 forest/green, 6 sun/orange).")
    net["canvas"] = [512, 256]
    net["lines"] = [OrderedDict([("key", k), ("name", n), ("bgPalette", p)]) for k, n, p in LINES]
    net["stations"] = []
    for key, (cell, label) in DIAGRAM.items():
        x, y = c(*cell)
        net["stations"].append(OrderedDict([("id", "TRAIN_STATION_" + key), ("name", by_key[key][1]),
                                            ("x", x), ("y", y), ("label", list(label))]))
    net["edges"] = [OrderedDict([("a", "TRAIN_STATION_" + a), ("b", "TRAIN_STATION_" + b), ("line", line),
                                 ("via", [list(c(*v)) for v in via])]) for a, b, line, via in EDGES]
    write_json(os.path.join(HERE, "network.json"), net)


def main():
    layouts_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(layouts_path), object_pairs_hook=OrderedDict)
    layouts = OrderedDict((l["id"], l) for l in lj["layouts"])
    border_ext = [0x1D4, 0x1D5, 0x1DC, 0x1DD]          # gTileset_General tree block (Tosa Port's border is sea)
    border_int = read_bin(P("data", "layouts", "TosaPort_BrendansHouse_1F", "border.bin"))
    border_plat = read_bin(P("data", "layouts", "TosaPort_BrendansHouse_2F", "border.bin"))

    def put_layout(lid, name, folder, w, h, g, border, primary, secondary):
        assert len(g) == w * h
        write_bin(P("data", "layouts", folder, "map.bin"), g)
        write_bin(P("data", "layouts", folder, "border.bin"), border)
        layouts[lid] = layout_entry(lid, name, w, h, primary, secondary, folder)

    # shared concourse; platforms shared per line set
    w, h, g = concourse_blocks()
    put_layout("LAYOUT_TOSA_RAIL_CONCOURSE", "TosaRailConcourse", "TosaRailConcourse", w, h, g, border_int,
               "gTileset_Building", "gTileset_UrbanInterior")
    plat_layout = {}
    for _, _, _, _, lines, *_ in STATIONS[1:]:
        tag = "_".join(l.upper() for l in lines)
        if tag in plat_layout:
            continue
        folder = "TosaRailPlatform_" + "".join(l.capitalize() for l in lines)
        lid = "LAYOUT_TOSA_RAIL_PLATFORM_" + tag
        w, h, g = platform_blocks(lines)
        put_layout(lid, folder, folder, w, h, g, border_plat, "gTileset_Building", "gTileset_UrbanPlatform")
        plat_layout[tag] = lid
    # Tosa Port platform: West wall, platform tileset
    tp = P("data", "layouts", "TosaPort_BrendansHouse_2F", "map.bin")
    w, h, g = platform_blocks(STATIONS[0][4], read_bin(tp))
    write_bin(tp, g)
    layouts["LAYOUT_TOSA_PORT_BRENDANS_HOUSE_2F"]["secondary_tileset"] = "gTileset_UrbanPlatform"

    maps, group = {"TOSA_PORT": "MAP_TOSA_PORT_BRENDANS_HOUSE_2F"}, []
    for key, name, prefix, mapsec, lines, vflag, music, mtype in STATIONS[1:]:
        ext, conc, plat = prefix, prefix + "_Station", prefix + "_StationPlatform"
        w, h, g = exterior_blocks()
        put_layout("LAYOUT_" + snake(ext), ext, ext, w, h, g, border_ext, "gTileset_General", "gTileset_TosaPort")
        write_json(P("data", "maps", ext, "map.json"), map_json(
            ext, "LAYOUT_" + snake(ext), music, mapsec, mtype, [],
            [warp(7, 7, map_id(conc), 0)], [], True))
        write_json(P("data", "maps", conc, "map.json"), map_json(
            conc, "LAYOUT_TOSA_RAIL_CONCOURSE", music, mapsec, "MAP_TYPE_INDOOR",
            [obj("OBJ_EVENT_GFX_CLIPBOARD", 7, 4, "NULL", "MOVEMENT_TYPE_FACE_LEFT", 0),
             obj("OBJ_EVENT_GFX_LINK_RECEPTIONIST", 8, 3, "TosaRail_EventScript_Receptionist", elevation=0)],
            [warp(7, 10, map_id(ext), 0), warp(6, 10, map_id(ext), 0), warp(1, 4, map_id(plat), 0, 4)],
            [sign(4, 3, "TosaGateway_FareGateNorth"), sign(4, 5, "TosaGateway_FareGateSouth")], False))
        write_json(P("data", "maps", plat, "map.json"), map_json(
            plat, plat_layout["_".join(l.upper() for l in lines)], music, mapsec, "MAP_TYPE_INDOOR",
            [obj("OBJ_EVENT_GFX_MAN_2", 11, 5, "TosaRail_EventScript_PlatformAttendant", "MOVEMENT_TYPE_FACE_LEFT")],
            [warp(1, 7, map_id(conc), 2, 4)], [], False))
        for m in (ext, conc, plat):
            pory = P("data", "maps", m, "scripts.pory")
            if not os.path.exists(pory):
                open(pory, "w").write("mapscripts %s_MapScripts {}\n" % m)
            group.append(m)
        maps[key] = map_id(plat)

    lj["layouts"] = list(layouts.values())
    write_json(layouts_path, lj)
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    if GROUP not in mg["group_order"]:
        mg["group_order"].append(GROUP)
    mg[GROUP] = group
    write_json(mg_path, mg)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    anchor = '\t.include "data/maps/TrainTestNorth/scripts.inc"\n'
    add = "".join('\t.include "data/maps/%s/scripts.inc"\n' % m for m in group if ('data/maps/%s/scripts.inc' % m) not in es)
    assert anchor in es
    open(es_path, "w").write(es.replace(anchor, anchor + add))
    write_constants()
    write_flags()
    write_station_table(maps)
    write_network()
    print("stations %d, new maps %d, platform layouts %s" % (len(STATIONS), len(group), sorted(plat_layout.values())))


if __name__ == "__main__":
    main()
