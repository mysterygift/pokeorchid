#!/usr/bin/env python3
"""Vanilla buildings (copied tile-for-tile out of the Telok Town layout) next to the new Centre
and Mart on one baseline, to compare footprints.

    python height_compare.py      # writes out/height_compare_2x.png
"""
import os

from PIL import ImageDraw

import centre_exterior
import mart_exterior
import vanilla
from mock import OUT, up
from town import Town

W, H, BASE = 37, 10, 7          # BASE = the row every building's bottom tile sits on

# (label, x, y, w, h) of vanilla buildings in LAYOUT_OLDALE_TOWN (Telok Town)
VANILLA = [
    ("house", 7, 4, 4, 4),
    ("Centre", 5, 13, 4, 4),
    ("Mart", 14, 13, 4, 4),
    ("large building", 27, 2, 7, 5),
]


def build():
    _, src, _ = vanilla.layout("LAYOUT_OLDALE_TOWN")
    t = Town(W, H)
    t.path(0, BASE + 1, W - 1, H - 1)
    labels, x = [], 1

    def place_vanilla(i):
        nonlocal x
        name, sx, sy, w, h = VANILLA[i]
        for dy in range(h):
            for dx in range(w):
                t.g[BASE - h + 1 + dy][x + dx] = src[sy + dy][sx + dx]
        labels.append((x, w, h, f"vanilla {name}"))
        x += w + 1

    slots = []
    place_vanilla(0)
    place_vanilla(1)
    slots.append(("centre", x)); labels.append((x, 5, 4, "NEW Centre")); x += 6
    place_vanilla(2)
    slots.append(("mart", x)); labels.append((x, 5, 4, "NEW Mart")); x += 6
    place_vanilla(3)

    st = t.stage()
    c, m = centre_exterior.build(), mart_exterior.build()
    for kind, bx in slots:
        b = c if kind == "centre" else m
        st.add(b["under"], bx * 16, (BASE - 3) * 16)
        st.add(b["over"], bx * 16, (BASE - 3) * 16, over=True)
    for bx, w, h, _ in labels:
        st.npc("brendan/walking.png", "brendan.pal", 0, bx + w // 2, BASE + 1)
    im = up(st.render(), 2).convert("RGB")
    dr = ImageDraw.Draw(im)
    for bx, w, h, name in labels:
        x0, x1 = bx * 32, (bx + w) * 32 - 1
        y0, y1 = (BASE - h + 1) * 32, (BASE + 1) * 32 - 1
        dr.line((x0, y0 - 6, x1, y0 - 6), fill=(255, 255, 255), width=2)
        dr.text((x0, y0 - 20), f"{w} x {h} tiles", fill=(255, 255, 255))
        dr.text((x0, (BASE + 2) * 32 + 8), name, fill=(40, 40, 40))
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "height_compare_2x.png")
    build().save(p)
    print(p)
