#!/usr/bin/env python3
"""Where do Pokemon Centres and Marts appear, and what can the tilesets hold?

    python inventory.py            # doors, interior maps, primary tileset usage
"""
import glob
import json
import os
import struct
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def layouts():
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    return {e["id"]: e for e in js["layouts"] if "id" in e}


def blocks(entry):
    w, h = entry["width"], entry["height"]
    raw = open(os.path.join(ROOT, entry["blockdata_filepath"]), "rb").read()
    if len(raw) != w * h * 2:
        return None                      # stale / placeholder layout entry
    b = struct.unpack(f"<{w * h}H", raw)
    return [[b[y * w + x] for x in range(w)] for y in range(h)]


def maps():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "maps", "*", "map.json"))):
        js = json.load(open(p))
        out[js["id"]] = (p, js)
    return out


def is_centre(map_id):
    return "POKEMON_CENTER_1F" in map_id


def is_mart(map_id):
    return map_id.endswith("_MART")


def doors():
    """Every outdoor warp that leads into a Centre 1F or a Mart."""
    L, M = layouts(), maps()
    found = []
    for mid, (p, js) in M.items():
        for i, w in enumerate(js.get("warp_events") or []):
            dest = w["dest_map"]
            if not (is_centre(dest) or is_mart(dest)) or is_centre(mid) or is_mart(mid):
                continue
            lay = L[js["layout"]]
            g = blocks(lay)
            x, y = w["x"], w["y"]
            found.append(dict(map=mid, layout=js["layout"], path=p, warp=i, dest=dest, x=x, y=y,
                              metatile=g[y][x] & 0x3FF, primary=lay["primary_tileset"],
                              secondary=lay["secondary_tileset"]))
    return found


def main():
    L, M = layouts(), maps()
    print("== outdoor doors into Centres / Marts")
    for d in doors():
        g = blocks(L[d["layout"]])
        kind = "C" if is_centre(d["dest"]) else "M"
        x, y = d["x"], d["y"]
        rows = []
        for yy in range(y - 3, y + 1):
            rows.append(" ".join(f"{g[yy][xx] & 0x3FF:03X}" if 0 <= xx < len(g[0]) and 0 <= yy < len(g) else "---"
                                 for xx in range(x - 3, x + 5)))
        print(f"{kind} {d['map']:<34} {d['layout']:<34} door ({x},{y}) mt {d['metatile']:03X}  {d['primary']} / {d['secondary']}")
        for r in rows:
            print("      " + r)
    print("\n== interior maps")
    by_layout = defaultdict(list)
    for mid, (p, js) in M.items():
        if is_centre(mid) or is_mart(mid):
            by_layout[js["layout"]].append(mid)
    for lay, mids in by_layout.items():
        e = L[lay]
        print(f"{lay}: {e['width']}x{e['height']} {e['primary_tileset']} / {e['secondary_tileset']}  ({len(mids)} maps)")
        print("    " + ", ".join(mids))


if __name__ == "__main__":
    main()
