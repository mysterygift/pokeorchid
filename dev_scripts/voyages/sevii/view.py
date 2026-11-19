#!/usr/bin/env python3
"""ASCII view of a Sevii map: '#' blocked, digit = elevation, '~' water, W warp, o object, i item, s sign, h hidden.
usage: python3 view.py MapFolder [x0 y0 x1 y1]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mtattr as MA
import check_sevii as C
f = sys.argv[1]
m = json.load(open(MA.P("data", "maps", f, "map.json")))
L = MA.Layout(m["layout"])
x0, y0, x1, y1 = (list(map(int, sys.argv[2:6])) + [0, 0, L.w, L.h][len(sys.argv[2:6]):])
mark = {}
for w in m["warp_events"]: mark[(w["x"], w["y"])] = "W"
for o in m["object_events"]: mark[(o["x"], o["y"])] = "i" if "ITEM_BALL" in o["graphics_id"] else "r" if "ROCK" in o["graphics_id"] or "BOULDER" in o["graphics_id"] or "CUTTABLE" in o["graphics_id"] else "o"
for b in m["bg_events"]: mark[(b["x"], b["y"])] = "h" if b["type"] == "hidden_item" else "s"
seen, _ = C.flood(m, L)
print("    " + "".join(str(x % 10) for x in range(x0, x1)))
for y in range(y0, y1):
    row = ""
    for x in range(x0, x1):
        c = mark.get((x, y))
        if not c:
            c = "#" if L.coll(x, y) else "~" if C.is_water(L.beh(x, y)) else str(L.elev(x, y))
            if (x, y) in seen and c not in "#~": c = "."
        row += c
    print("%3d %s" % (y, row))
