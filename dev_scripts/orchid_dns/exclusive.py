#!/usr/bin/env python3
"""Which (palette, index) pairs are drawn ONLY at glass pixels? Those can be lit by a .pla line alone.

    exclusive.py PAIR

Counts every pixel of every metatile of the pair (and, for primary palettes, of every secondary tileset the
primary is used with) and splits it into glass / not glass using windows.py's detection."""
import sys

import dns_tool as T
import windows as W

key = sys.argv[1]
cfg = W.CONFIG[key]
ts = T.Tilesets(cfg["primary"], cfg["secondary"])
gm = W.glass_by_metatile(cfg)
glass, other = {}, {}


def count(tsx, mids, is_main):
    for m in mids:
        cells = tsx.metatile(m)
        for y in range(16):
            for x in range(16):
                p, i, _ = cells[y][x]
                if not is_main and p >= T.NUM_PALS_IN_PRIMARY:
                    continue
                d = glass if (is_main and (x, y) in gm.get(m, ())) else other
                d[(p, i)] = d.get((p, i), 0) + 1


count(ts, list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))], True)
for sec in W.primary_partners(cfg):
    if sec in (cfg["secondary"], "0"):
        continue
    try:
        o = T.Tilesets(cfg["primary"], sec)
    except SystemExit:
        continue
    count(o, [512 + i for i in range(len(o.smeta))], False)
for k in sorted(glass):
    print(f"pal {k[0]:2d} idx {k[1]:2d} {ts.pals[k[0]][k[1]]}: glass {glass[k]}, elsewhere {other.get(k, 0)}")
