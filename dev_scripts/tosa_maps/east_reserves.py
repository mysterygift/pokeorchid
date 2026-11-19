#!/usr/bin/env python3
"""
Extra East Tosa Reserve maps (all in MAPSEC_EAST_TOSA_RESERVE), placed on the region-map cells they cover:

  - EastTosaReserve2 (80x40): cells (22, 8)-(23, 8), east of Bura City. Openings west to Bura, north
    (right half) up to EastTosaReserve3, south (right half) to Route 310.
  - EastTosaReserve3 (100x50): the L of cells (23, 7) and (23..26, 6) above it. Opening south (left)
    down to EastTosaReserve2 and east (top) to Senoko City; the unused corner of its box is forest.

Each is dressed like the other routes (dress.py) and gets a sign, two NPCs and South Tosa Reserve 1's
land encounters as a placeholder table. Map connections are left to the user; re-running keeps any
connections already set on a map.
usage: python3 dev_scripts/tosa_maps/east_reserves.py [--only EastTosaReserve3]
"""
import json
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import placeholders as PH        # noqa: E402
import dress                     # noqa: E402
import towns as TW               # noqa: E402

P = PH.P
MAPSEC = "MAPSEC_EAST_TOSA_RESERVE"
SPECS = OrderedDict()
SPECS["EastTosaReserve2"] = dict(
    cells=[(22, 8), (23, 8)], size=(80, 40), forest=None,
    sign="East Tosa Reserve\nWest: Bura City",
    people=[("OBJ_EVENT_GFX_POKEMON_RANGER_M", "look",
             "This end of the reserve backs right onto Bura City. We get a lot of runaway pet Persian out here."
             "\\pThey don't last long against the wild Pokémon."),
            ("OBJ_EVENT_GFX_BUG_CATCHER", "wander",
             "The tall grass out here is huge! I lost my net in it twice already.")],
    spots=lambda hub: [(hub[0] + 3, hub[1] + 5), (hub[0] - 14, hub[1] - 6)])
SPECS["EastTosaReserve3"] = dict(
    cells=[(23, 7), (23, 6), (24, 6), (25, 6), (26, 6)], size=(100, 50), forest=(26, 28),
    sign="East Tosa Reserve\nEast: Senoko City",
    people=[("OBJ_EVENT_GFX_POKEMON_RANGER_F", "look",
             "On a clear day you can see Senoko's wind turbines from here. Mo keeps the whole region running."),
            ("OBJ_EVENT_GFX_HIKER", "wander",
             "I'm walking the whole reserve, end to end. Bura City to Senoko City! My feet hate me.")],
    spots=lambda hub: [(hub[0] + 6, hub[1] - 4), (hub[0] - 30, hub[1] + 10)])


def build_one(NAME, spec):
    MAP_ID = "MAP_" + PH.snake(NAME)
    LAYOUT = "LAYOUT_" + PH.snake(NAME)
    W, H = spec["size"]
    SIGN, PEOPLE = spec["sign"], spec["people"]
    opens = PH.openings(spec["cells"], PH.region_cells(), W, H)
    cv, hub = PH.build(NAME, "reserve", W, H, opens, {}, None, None)
    if spec["forest"]:                                   # the corner of the box outside the L: woods
        fx, fy = spec["forest"]
        PH.trees_where(cv, lambda bx, by: bx * 2 >= fx and by * 2 >= fy and
                       all(cv.t[by * 2 + j][bx * 2 + i] != "P" for i in (0, 1) for j in (0, 1)))
    sign = PH.place_sign(cv, (hub[0], hub[1] + 1), "G")      # a row lower so its patch clears the road
    blocks = PH.render(cv, "reserve")
    events, objs, pory = [sign], [], "mapscripts %s_MapScripts {}\n\n" % NAME
    pory += TW.msg(NAME + "_EventScript_Sign", SIGN, "MSGBOX_SIGN")
    spots = spec["spots"](hub)
    for k, ((gfx, move, text), (tx, ty)) in enumerate(zip(PEOPLE, spots)):
        x, y = min(((x, y) for y in range(3, H - 3) for x in range(3, W - 3)
                    if (blocks[y * W + x] & 0x3FF) in (0x001, 0x00D) and not (blocks[y * W + x] >> 10) & 3
                    and all(abs(x - a) + abs(y - b) > 2 for a, b in events)),
                   key=lambda p: abs(p[0] - tx) + abs(p[1] - ty))
        events.append((x, y))
        label = "%s_EventScript_Npc%d" % (NAME, k + 1)
        objs.append(TW.obj(gfx, x, y, 3, move, label))
        pory += TW.msg(label, text, "MSGBOX_NPC")
    blocks = dress.apply(blocks, W, H, "dirt", events, NAME, ledges=W * H // 450, flowers=W * H // 260,
                         groves=W * H // 300)
    PH.write_bin(P("data", "layouts", NAME, "map.bin"), blocks)
    PH.write_bin(P("data", "layouts", NAME, "border.bin"), PH.OUTDOOR[2])

    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    lj["layouts"] = [l for l in lj["layouts"] if l.get("id") != LAYOUT] + [OrderedDict([
        ("id", LAYOUT), ("name", NAME + "_Layout"), ("width", W), ("height", H),
        ("primary_tileset", "gTileset_General"), ("secondary_tileset", "gTileset_TosaPort"),
        ("border_filepath", "data/layouts/%s/border.bin" % NAME),
        ("blockdata_filepath", "data/layouts/%s/map.bin" % NAME), ("layout_version", "emerald")])]
    PH.write_json(lj_path, lj)

    mpath = P("data", "maps", NAME, "map.json")
    old = json.load(open(mpath)) if os.path.exists(mpath) else {}
    m = OrderedDict([
        ("id", MAP_ID), ("name", NAME), ("layout", LAYOUT), ("music", "MUS_SOUTHTOSARESERVE"),
        ("region", "REGION_HOENN"), ("region_map_section", MAPSEC), ("requires_flash", False),
        ("weather", "WEATHER_SUNNY"), ("map_type", "MAP_TYPE_ROUTE"), ("allow_cycling", True),
        ("allow_escaping", False), ("allow_running", True), ("show_map_name", True),
        ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", old.get("connections")),
        ("object_events", objs), ("warp_events", []), ("coord_events", []),
        ("bg_events", [OrderedDict([("type", "sign"), ("x", sign[0]), ("y", sign[1]), ("elevation", 0),
                                    ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"),
                                    ("script", NAME + "_EventScript_Sign")])])])
    PH.write_json(mpath, m)
    TW.write_pory(NAME, pory)

    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    if NAME not in mg[PH.GROUP]:
        mg[PH.GROUP].append(NAME)
        PH.write_json(mg_path, mg)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    if inc not in es:
        anchor = '\t.include "data/maps/EastTosaReserve/scripts.inc"\n'
        assert anchor in es
        prev = [n for n in SPECS if '\t.include "data/maps/%s/scripts.inc"\n' % n in es]
        if prev:
            anchor = '\t.include "data/maps/%s/scripts.inc"\n' % prev[-1]
        open(es_path, "w").write(es.replace(anchor, anchor + inc))

    we_path = P("src", "data", "wild_encounters.json")
    we = json.load(open(we_path), object_pairs_hook=OrderedDict)
    enc = we["wild_encounter_groups"][0]["encounters"]
    enc[:] = [e for e in enc if e.get("map") != MAP_ID]
    src = next(e for e in enc if e.get("map") == "MAP_SOUTHTOSARESERVE")
    enc.insert(enc.index(src) + 1, OrderedDict([("map", MAP_ID), ("base_label", "g" + NAME),
                                                ("land_mons", json.loads(json.dumps(src["land_mons"]), object_pairs_hook=OrderedDict))]))
    with open(we_path, "w") as f:
        json.dump(we, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("%s %dx%d openings %s, people at %s" % (NAME, W, H, opens, events[1:]))


def main():
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    for name, spec in SPECS.items():
        if not only or name in only:
            build_one(name, spec)


if __name__ == "__main__":
    main()
