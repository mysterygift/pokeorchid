#!/usr/bin/env python3
"""
South Tosa Reserve 4: a short reserve route from the Abandoned House's south road down to Moongrove
Marsh (region cells (9..11, 11), inside South Tosa Reserve 3's section, so it shares that map section).

  - 48x28, north edge joined to the Abandoned House (offset 0: its road x 10-15 lines up), south edge
    joined to Moongrove Marsh (offset 8: the marsh's new opening at its x 18-23 is our x 26-31)
  - opens the marsh's north edge and runs a path from it to the marsh's existing road (the marsh is
    re-dressed from its stored undressed base, so dress.py stays in step)
  - a Ranger, a reserve sign, and South Tosa Reserve 1's land encounters

Re-running rebuilds the route and re-applies the marsh opening and connections.
usage: python3 dev_scripts/tosa_maps/south_reserve4.py
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
NAME, MAP_ID, LAYOUT = "SouthTosaReserve4", "MAP_SOUTH_TOSA_RESERVE4", "LAYOUT_SOUTH_TOSA_RESERVE4"
W, H = 48, 28
NORTH_X, SOUTH_X = 12, 28              # opening positions (PH.openings style: the road is x .. x+1, gap x-2 .. x+3)
MARSH_OFFSET = 8                       # marsh x 0 sits under our x 8
SIGN = "South Tosa Reserve\nNorth: Abandoned House  South: Moongrove Marsh"
RANGER = ("The old house up north gives me the creeps. Lights in the windows, and nobody's lived there for decades."
          "\\pIf you're heading to the marsh, the tall grass here is full of Pokémon.")


def set_connections(m, conns):
    """conns: list of (direction, map, offset); replaces any connection in those directions."""
    dirs = {d for d, _, _ in conns}
    keep = [c for c in (m.get("connections") or []) if c["direction"] not in dirs]
    m["connections"] = keep + [OrderedDict([("map", mp), ("offset", off), ("direction", d)]) for d, mp, off in conns]


def build_route():
    cv, hub = PH.build(NAME, "reserve", W, H, {"N": [NORTH_X], "S": [SOUTH_X]}, {}, None, None)
    sign = PH.place_sign(cv, hub, "G")
    blocks = PH.render(cv, "reserve")
    return blocks, hub, sign


def open_marsh():
    """Cut the marsh's north edge at x 18-23 and lay a path down to its road."""
    lay = next(l for l in json.load(open(P("data", "layouts", "layouts.json")))["layouts"] if l.get("id") == "LAYOUT_MOONGROVE_MARSH")
    w, h = lay["width"], lay["height"]
    state = json.load(open(dress.STATE))
    st = state["MoongroveMarsh"]
    base = [int(st["base"][k:k + 4], 16) for k in range(0, len(st["base"]), 4)]
    gx = SOUTH_X - MARSH_OFFSET                       # 20
    for y in (0, 1):
        for x in range(gx - 2, gx + 4):
            base[y * w + x] = PH.GRASS
    is_path = lambda x, y: (base[y * w + x] & 0x3FF) == (PH.PATH & 0x3FF)
    y = 0
    while y < h and not (y > 2 and is_path(gx, y) and is_path(gx + 1, y)):
        for x in (gx, gx + 1):
            base[y * w + x] = PH.PATH
        y += 1
    assert y < h, "no road to join in the marsh"
    st["base"] = "".join("%04x" % v for v in base)
    json.dump(state, open(dress.STATE, "w"), indent=0)


def main():
    blocks, hub, sign = build_route()
    events = [sign]
    # a Ranger near the middle, off the road
    rx, ry = next((x, y) for d in range(1, 12) for x, y in ((hub[0] + d, hub[1] + 3), (hub[0] - d, hub[1] + 3))
                  if (blocks[y * W + x] & 0x3FF) in (0x001, 0x00D) and not (blocks[y * W + x] >> 10) & 3)
    events.append((rx, ry))
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

    m = OrderedDict([
        ("id", MAP_ID), ("name", NAME), ("layout", LAYOUT), ("music", "MUS_SOUTHTOSARESERVE"),
        ("region", "REGION_HOENN"), ("region_map_section", "MAPSEC_SOUTH_TOSA_RESERVE_3"), ("requires_flash", False),
        ("weather", "WEATHER_SUNNY"), ("map_type", "MAP_TYPE_ROUTE"), ("allow_cycling", True),
        ("allow_escaping", False), ("allow_running", True), ("show_map_name", True),
        ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None),
        ("object_events", [TW.obj("OBJ_EVENT_GFX_POKEMON_RANGER_F", rx, ry, 3, "look", NAME + "_EventScript_Ranger")]),
        ("warp_events", []), ("coord_events", []),
        ("bg_events", [OrderedDict([("type", "sign"), ("x", sign[0]), ("y", sign[1]), ("elevation", 0),
                                    ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"),
                                    ("script", NAME + "_EventScript_Sign")])])])
    set_connections(m, [("up", "MAP_ABANDONED_HOUSE", 0), ("down", "MAP_MOONGROVE_MARSH", MARSH_OFFSET)])
    PH.write_json(P("data", "maps", NAME, "map.json"), m)
    TW.write_pory(NAME, "mapscripts %s_MapScripts {}\n\n" % NAME
                  + TW.msg(NAME + "_EventScript_Sign", SIGN, "MSGBOX_SIGN")
                  + TW.msg(NAME + "_EventScript_Ranger", RANGER, "MSGBOX_NPC"))

    for other, conns in (("AbandonedHouse", [("down", MAP_ID, 0)]),
                         ("MoongroveMarsh", [("up", MAP_ID, -MARSH_OFFSET)])):
        p = P("data", "maps", other, "map.json")
        om = json.load(open(p), object_pairs_hook=OrderedDict)
        set_connections(om, conns)
        PH.write_json(p, om)
    open_marsh()
    sys.argv = [sys.argv[0], "--only", "MoongroveMarsh"]
    dress.main()

    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    if NAME not in mg[PH.GROUP]:
        mg[PH.GROUP].append(NAME)
        PH.write_json(mg_path, mg)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    if inc not in es:
        anchor = '\t.include "data/maps/SouthTosaReserve3/scripts.inc"\n'
        open(es_path, "w").write(es.replace(anchor, anchor + inc))

    we_path = P("src", "data", "wild_encounters.json")
    we = json.load(open(we_path), object_pairs_hook=OrderedDict)
    enc = we["wild_encounter_groups"][0]["encounters"]
    src = next(e for e in enc if e.get("map") == "MAP_SOUTHTOSARESERVE")
    enc[:] = [e for e in enc if e.get("map") != MAP_ID]
    at = enc.index(src) + 1
    enc.insert(at, OrderedDict([("map", MAP_ID), ("base_label", "gSouthTosaReserve4"),
                                ("land_mons", json.loads(json.dumps(src["land_mons"]), object_pairs_hook=OrderedDict))]))
    with open(we_path, "w") as f:
        json.dump(we, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("%s %dx%d, ranger at %s, sign at %s" % (NAME, W, H, (rx, ry), sign))


if __name__ == "__main__":
    main()
