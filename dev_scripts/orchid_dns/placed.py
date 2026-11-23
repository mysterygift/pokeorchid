#!/usr/bin/env python3
"""What do the maps that still exist actually use of a primary tileset?

    placed.py PRIMARY_LABEL

For every layout on PRIMARY (and its secondary), collects the metatiles placed in blockdata, then reports:
  * per primary palette (0-5): colour indices drawn by placed metatiles, and the free ones;
  * primary tiles referenced by any placed metatile (the rest are free tile slots);
  * primary metatiles no map places (free metatile slots).
"""
import json
import os
import struct
import sys

import dns_tool as T

ROOT = T.ROOT


def placed_usage(primary):
    L = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    by_sec = {}
    for l in L:
        if l.get("primary_tileset") != primary:
            continue
        p = os.path.join(ROOT, l["blockdata_filepath"])
        if not os.path.exists(p):
            continue
        s = by_sec.setdefault(l["secondary_tileset"], set())
        s.update(b & 0x3FF for (b,) in struct.iter_unpack("<H", open(p, "rb").read()))
    used_idx = [set() for _ in range(16)]
    used_ptiles, used_pmeta = set(), set()
    for sec, mids in by_sec.items():
        try:
            ts = T.Tilesets(primary, sec)
        except SystemExit:
            continue
        for m in mids:
            ent = ts.entries(m)
            if ent is None:
                continue
            if m < 512:
                used_pmeta.add(m)
            for layer in range(2):
                for q in range(4):
                    e = ent[layer * 4 + q]
                    t, pal = e & 0x3FF, e >> 12
                    if t < 512:
                        used_ptiles.add(t)
                    if pal >= T.NUM_PALS_IN_PRIMARY:
                        continue
                    tile = ts.ptiles[t] if t < 512 else (ts.stiles[t - 512] if t - 512 < len(ts.stiles) else None)
                    if tile is None:
                        continue
                    for row in tile:
                        used_idx[pal].update(c for c in row if c or layer == 0)
    return by_sec, used_idx, used_ptiles, used_pmeta


if __name__ == "__main__":
    prim = sys.argv[1]
    by_sec, used_idx, used_ptiles, used_pmeta = placed_usage(prim)
    print("secondaries:", sorted(by_sec))
    for p in range(T.NUM_PALS_IN_PRIMARY):
        print(f"pal {p}: free {[i for i in range(1, 16) if i not in used_idx[p]]}")
    print("primary tiles used", len(used_ptiles), "free", 512 - len(used_ptiles))
    print("primary metatiles placed", len(used_pmeta))
