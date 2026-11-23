#!/usr/bin/env python3
"""Per-palette colour-index usage across every metatile of a primary+secondary tileset pair.

    pal_usage.py PRIMARY_LABEL SECONDARY_LABEL

Prints, per palette slot, pixel counts per index plus duplicate colours, so free / reclaimable indices for
light colours (windows, lamps) can be found. Primary palettes 0-5 are counted over primary AND secondary
metatiles (secondaries draw with primary palettes too)."""
import sys
from dns_tool import Tilesets

ts = Tilesets(sys.argv[1], sys.argv[2])
cnt = [[0] * 16 for _ in range(16)]
ids = list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))]
for m in ids:
    ent = ts.entries(m)
    for layer in range(2):
        for q in range(4):
            e = ent[layer * 4 + q]
            t, pal = e & 0x3FF, e >> 12
            tile = ts.ptiles[t] if t < 512 else (ts.stiles[t - 512] if t - 512 < len(ts.stiles) else None)
            if tile is None:
                continue
            for row in tile:
                for c in row:
                    if c or layer == 0:
                        cnt[pal][c] += 1
for p in range(13):
    cols = ts.pals[p]
    dup = {}
    for i, c in enumerate(cols[1:], 1):
        dup.setdefault(c, []).append(i)
    dups = [v for v in dup.values() if len(v) > 1]
    free = [i for i in range(1, 16) if cnt[p][i] == 0]
    print(f"pal {p:2d} free={free} dups={dups} lights={sorted(ts.lights[p])}")
    print("        " + " ".join(f"{i}:{cnt[p][i]}" for i in range(16)))
