#!/usr/bin/env python3
"""
Mt. Drake (Tiksi): placeholder exteriors at every exit and a multi-floor climb to the existing summit,
built with the Tosa placeholder builder (placeholders.build, like Mt. Batok / Challenger's Trail).

  Route 402 --edge-- South Face --cave mouth--> 1F --ladder--> 2F --ladder--> 3F --mat--> Peak --cave mouth--> Summit
                                                 |               |
                                  mat --> West Face              mat --> North Face --edge-- Drake Base Camp
                                          (Ferrum Shrine mouth; a one-way ledge down to a path north to Route 403)

Ferrum Shrine ("at the core of Mt. Drake") and the Summit used to be entered from mounds in Drake Base
Camp (tiksi_people.py now leaves those out); their guardians stand here instead. The West Face is drawn
by hand (west_face()): Gen 3 has no north-facing ledge tile, so the drop is a west-facing ledge
(General 0x0FE / 0x085 / 0x106) off the plateau onto the path that runs north to Route 403. Everything is in
MAPSEC_MT_DRAKE. Edge connections to Route 402 and Drake Base Camp are set here (both maps line up at
offset 0); re-running rebuilds the six maps and relinks the Summit and Ferrum Shrine.
usage: python3 dev_scripts/tiksi_maps/mt_drake.py
"""
import json
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tosa_maps"))
import placeholders as PH        # noqa: E402
import dress                     # noqa: E402
import towns as TW               # noqa: E402

P = PH.P
GROUP, SEC = "gMapGroup_Tiksi", "MAPSEC_MT_DRAKE"
G = lambda s: "OBJ_EVENT_GFX_" + s
CAVE_MUS, OUT_MUS = "MUS_VICTORY_ROAD", "MUS_MT_PYRE_EXTERIOR"
# name, theme, size, builder extras, edge openings, sign (exteriors), people [(gfx, near warp key, line)]
MAPS = [
    ("MtDrake_SouthFace", "rocky", (30, 36), {"mouths": {"cave": "N"}}, {"S": [14]},
     "Mt. Drake\nSouth Face. The trail into the mountain starts here.",
     [(G("HIKER"), "mouth:cave", "Mt. Drake's peaks were carved by beams of light from an ancient Pokémon's maw.\\pThat's what my grandmother said, anyway.")]),
    ("MtDrake_1F", "cave", (44, 34), {"floor": {"mats": {"south": "c", "west": "w"}, "ladders": {"up": (0.8, 0.25)}}}, {}, None,
     [(G("PICNICKER"), "mat:west", "That passage comes out on the west face. Ferrum Shrine is out there, and a drop down to Route 403."),
      (G("CAMPER"), "ladder:up", "The way up is steep. Don't push your Pokémon too hard.")]),
    ("MtDrake_2F", "cave", (40, 32), {"floor": {"mats": {"north": "e"}, "ladders": {"down": (0.8, 0.25), "up": (0.2, 0.3)}}}, {}, None,
     [(G("HIKER"), "mat:north", "That opening leads out onto the north face. Drake Base Camp is just down the slope.")]),
    ("MtDrake_NorthFace", "rocky", (30, 30), {"mouths": {"cave": "S"}}, {"N": [14]},
     "Mt. Drake\nNorth Face. Drake Base Camp is just ahead.",
     [(G("EXPERT_M"), "mouth:cave", "Climbers rest at Drake Base Camp before trying for the peak. Smart ones, anyway.")]),
    ("MtDrake_3F", "cave", (36, 30), {"floor": {"mats": {"peak": "c"}, "ladders": {"down": (0.2, 0.3)}}}, {}, None,
     [(G("EXPERT_F"), "mat:peak", "Fresh air ahead… the peak is close.")]),
    ("MtDrake_WestFace", "west", (30, 36), {}, {},
     "Mt. Drake\nWest Face. Ferrum Shrine lies within the rock.",
     [(G("BLACK_BELT"), "mouth:ferrum", "Ferrum Shrine lies at the core of Mt. Drake. The steel giant has returned to it.\\pI am sworn to guard this door.")]),
    ("MtDrake_Peak", "rocky", (30, 30), {"mouths": {"low": "S", "summit": "N"}, "closed": True}, {},
     "Mt. Drake\nThe peak. The summit cave is above.",
     [(G("HIKER"), "mouth:summit", "Beyond here, the old trail climbs into the summit. They say the dragon giant waits at the top.\\pI guard the way. Be ready.")]),
]
LINKS = [
    (("MtDrake_SouthFace", "mouth:cave"), ("MtDrake_1F", "mat:south")),
    (("MtDrake_1F", "ladder:up"), ("MtDrake_2F", "ladder:down")),
    (("MtDrake_2F", "mat:north"), ("MtDrake_NorthFace", "mouth:cave")),
    (("MtDrake_2F", "ladder:up"), ("MtDrake_3F", "ladder:down")),
    (("MtDrake_3F", "mat:peak"), ("MtDrake_Peak", "mouth:low")),
    (("MtDrake_1F", "mat:west"), ("MtDrake_WestFace", "mouth:cave")),
]
EXTERNAL = [(("MtDrake_Peak", "mouth:summit"), "MtDrakeSummit"), (("MtDrake_WestFace", "mouth:ferrum"), "FerrumShrine")]
EDGES = [("MtDrake_SouthFace", "down", "MAP_ROUTE402", 0, "Route402", "up"),
         ("MtDrake_NorthFace", "up", "MAP_DRAKE_BASE_CAMP", 0, "DrakeBaseCamp", "down"),
         ("MtDrake_WestFace", "up", "MAP_ROUTE403", 0, "Route403", "down")]


def west_face(w, h):
    """Plateau (east) with the cave back into 1F and Ferrum Shrine's mouth; a west-facing ledge down its
    west side onto a lower path that runs north to the top edge (x 14-15, under Route 403's path)."""
    cv = PH.Canvas(w, h, "R")
    cv.rect(2, 2, 11, h - 3, "P")                    # lower path, west
    cv.rect(2, 2, 17, 6, "P")                        # ... and across the top to the opening
    cv.rect(14, 0, 15, 1, "P")                       # the opening, under Route 403's path
    cv.rect(13, 9, w - 3, h - 3, "P")                # plateau
    cv.rect(18, 4, 26, 8, "R")                       # rock above the plateau, with the way back into Mt. Drake
    cv.stamp(21, 5, PH.MOUTH)
    cv.warps["mouth:cave"] = (22, 8, 0)
    cv.rect(17, 23, 23, 27, "R")                     # Ferrum Shrine's rock, inside the plateau
    cv.stamp(19, 24, PH.MOUTH)
    cv.warps["mouth:ferrum"] = (20, 27, 0)
    for y in range(10, h - 4):                       # the ledge: jump west off the plateau
        cv.raw[(12, y)] = 0x0400 | (0x0FE if y == 10 else 0x106 if y == h - 5 else 0x085)
    for (x, y) in ((12, 9), (12, h - 4), (12, h - 3)):
        cv.t[y][x] = "R"
    rnd = __import__("random").Random("mtdrake/west")
    for _ in range(14):                              # boulders
        bx, by = rnd.randrange(14, w - 4) & ~1, rnd.randrange(11, h - 5) & ~1
        if all(cv.t[by + j][bx + i] == "P" and (bx + i, by + j) not in cv.raw for i in (0, 1) for j in (0, 1)) and \
                all(abs(bx - x) > 3 or abs(by - y) > 3 for (x, y, _) in cv.warps.values()):
            cv.rect(bx, by, bx + 1, by + 1, "R")
    return cv, (22, 12)


def set_connection(path, direction, target, offset):
    m = json.load(open(path), object_pairs_hook=OrderedDict)
    m["connections"] = [c for c in (m.get("connections") or []) if c["direction"] != direction] + \
        [OrderedDict([("map", target), ("offset", offset), ("direction", direction)])]
    PH.write_json(path, m)


def spot(vals, w, h, near, avoid):
    best = None
    for y in range(2, h - 2):
        for x in range(2, w - 2):
            v = vals[y * w + x]
            if (v >> 10) & 3 or dress.CLASS.get(v & 0x3FF) in ("Q", "W"):
                continue
            if any(abs(x - a) <= 1 and abs(y - b) <= 1 for a, b in avoid):
                continue
            d = abs(x - near[0]) + abs(y - near[1]) + (0 if abs(x - near[0]) + abs(y - near[1]) >= 2 else 50)
            if best is None or d < best[0]:
                best = (d, x, y)
    return best[1:]


def main():
    lj_path = P("data", "layouts", "layouts.json")
    lj = json.load(open(lj_path), object_pairs_hook=OrderedDict)
    built = {}
    for name, theme, (w, h), extras, opens, sign_text, people in MAPS:
        if theme == "west":
            cv, hub = west_face(w, h)
            theme = "rocky"
        else:
            cv, hub = PH.build(name, theme, w, h, opens, extras, None, None)
        sign = PH.place_sign(cv, hub, "P") if sign_text else None
        vals = PH.render(cv, theme)
        keys = list(cv.warps.keys())
        warp_xy = [cv.warps[k][:2] for k in keys]
        if theme == "rocky":
            vals = dress.apply(vals, w, h, "dirt", warp_xy + ([sign] if sign else []), name, flowers=0, groves=0)
        avoid = list(warp_xy) + ([sign] if sign else [])
        objs, pory = [], "mapscripts %s_MapScripts {}\n\n" % name
        bg = []
        if sign:
            pory += TW.msg(name + "_EventScript_Sign", sign_text, "MSGBOX_SIGN")
            bg.append(OrderedDict([("type", "sign"), ("x", sign[0]), ("y", sign[1]), ("elevation", 0),
                                   ("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"), ("script", name + "_EventScript_Sign")]))
        for k, (gfx, near_key, line) in enumerate(people):
            wx, wy = cv.warps[near_key][:2]
            x, y = spot(vals, w, h, (wx + 2, wy + 1), avoid)
            avoid.append((x, y))
            label = "%s_EventScript_Npc%d" % (name, k + 1)
            objs.append(TW.obj(gfx, x, y, (vals[y * w + x] >> 12) & 0xF, "look" if k == 0 else "wander", label))
            pory += TW.msg(label, line, "MSGBOX_NPC")
        tiles = PH.CAVE if theme == "cave" else PH.ROCKY
        PH.write_bin(P("data", "layouts", name, "map.bin"), vals)
        PH.write_bin(P("data", "layouts", name, "border.bin"), tiles[2])
        lid = "LAYOUT_" + PH.snake(name)
        lj["layouts"] = [l for l in lj["layouts"] if l.get("id") != lid] + [OrderedDict([
            ("id", lid), ("name", name + "_Layout"), ("width", w), ("height", h),
            ("primary_tileset", tiles[0]), ("secondary_tileset", tiles[1]),
            ("border_filepath", "data/layouts/%s/border.bin" % name),
            ("blockdata_filepath", "data/layouts/%s/map.bin" % name), ("layout_version", "emerald")])]
        mpath = P("data", "maps", name, "map.json")
        old_conn = json.load(open(mpath)).get("connections") if os.path.exists(mpath) else None
        cave = theme == "cave"
        m = OrderedDict([
            ("id", "MAP_" + PH.snake(name)), ("name", name), ("layout", lid), ("music", CAVE_MUS if cave else OUT_MUS),
            ("region", "REGION_HOENN"), ("region_map_section", SEC), ("requires_flash", False),
            ("weather", "WEATHER_NONE" if cave else "WEATHER_SUNNY"),
            ("map_type", "MAP_TYPE_UNDERGROUND" if cave else "MAP_TYPE_ROUTE"),
            ("allow_cycling", True), ("allow_escaping", cave), ("allow_running", True), ("show_map_name", True),
            ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", old_conn), ("object_events", objs),
            ("warp_events", [OrderedDict([("x", cv.warps[k][0]), ("y", cv.warps[k][1]), ("elevation", cv.warps[k][2]),
                                          ("dest_map", "X"), ("dest_warp_id", "X")]) for k in keys]),
            ("coord_events", []), ("bg_events", bg)])
        built[name] = (m, keys)
        os.makedirs(P("data", "maps", name), exist_ok=True)
        TW.write_pory(name, pory)
    for (a, ka), (b, kb) in LINKS:
        (A, akeys), (B, bkeys) = built[a], built[b]
        ia, ib = akeys.index(ka), bkeys.index(kb)
        A["warp_events"][ia].update(dest_map=B["id"], dest_warp_id=str(ib))
        B["warp_events"][ib].update(dest_map=A["id"], dest_warp_id=str(ia))
    for (a, ka), folder in EXTERNAL:
        A, akeys = built[a]
        ia = akeys.index(ka)
        fpath = P("data", "maps", folder, "map.json")
        fm = json.load(open(fpath), object_pairs_hook=OrderedDict)
        A["warp_events"][ia].update(dest_map=fm["id"], dest_warp_id="0")
        for wv in fm["warp_events"]:
            wv.update(dest_map=A["id"], dest_warp_id=str(ia))
        PH.write_json(fpath, fm)
    for name, (m, _) in built.items():
        assert not [wv for wv in m["warp_events"] if wv["dest_map"] == "X"], name
        PH.write_json(P("data", "maps", name, "map.json"), m)
    for name, d, target, off, other, back in EDGES:
        set_connection(P("data", "maps", name, "map.json"), d, target, off)
        set_connection(P("data", "maps", other, "map.json"), back, "MAP_" + PH.snake(name), -off)
    PH.write_json(lj_path, lj)
    mg_path = P("data", "maps", "map_groups.json")
    mg = json.load(open(mg_path), object_pairs_hook=OrderedDict)
    for name in built:
        if name not in mg[GROUP]:
            mg[GROUP].append(name)
    PH.write_json(mg_path, mg)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    anchor = [l for l in es.split("\n") if "data/maps/MtDrakeSummit/scripts.inc" in l][0] + "\n"
    add = "".join('\t.include "data/maps/%s/scripts.inc" @ mt-drake\n' % n for n in built
                  if 'data/maps/%s/scripts.inc"' % n not in es)
    open(es_path, "w").write(es.replace(anchor, anchor + add))
    for name, (m, keys) in built.items():
        print("%-18s warps %s" % (name, ["%s->%s" % (k, wv["dest_map"][4:]) for k, wv in zip(keys, m["warp_events"])]))


if __name__ == "__main__":
    main()
