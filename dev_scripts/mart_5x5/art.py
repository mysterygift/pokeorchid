#!/usr/bin/env python3
"""Widen the 64x80 v2 Mart art to 80x80 (5 metatiles) so the door sits inside the centre metatile.

    ../centre_mart_v2/art/mart.png (64x80)  ->  art/mart.png (80x80)

Each half grows 32 -> 40 px. Per row band, columns are repeated only where the art is periodic or
flat (glass stripes, horizontal bands, window panes), so the slanted corners and outlines are
untouched and the door (18 px incl. outline) moves from straddling metatiles 1|2 to inside metatile 2.

    python art.py
"""
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "centre_mart_v2", "art", "mart.png")
OUT = os.path.join(HERE, "art", "mart.png")

# Left-half column numbers (0..31; 31 is the centre). (c0, c1, k) repeats columns [c0, c1) k extra
# times right after c1 - 1. Every row band adds exactly 8 columns.
PLAN = [
    (0, 13, [(16, 17, 8)]),               # roof top: horizontal lines
    (13, 45, [(14, 17, 2),                # glass stripes "8778778" -> two more "778"
              (22, 23, 2)]),              # dark gutter between glass and centre tower
    (45, 64, [(15, 16, 8)]),              # base: horizontal bands
    (64, 80, [(11, 15, 2)]),              # front windows: two more "8777" panes
]


def stretch(half):
    out = np.zeros((half.shape[0], 40, 4), np.uint8)
    for y0, y1, ins in PLAN:
        cols = []
        for x in range(32):
            cols.append(x)
            for c0, c1, k in ins:
                if x == c1 - 1:
                    cols += list(range(c0, c1)) * k
        assert len(cols) == 40, (y0, len(cols))
        out[y0:y1] = half[y0:y1][:, cols]
    return out


def main():
    a = np.array(Image.open(SRC).convert("RGBA"))
    assert a.shape[:2] == (80, 64)
    left = stretch(a[:, :32])
    right = stretch(a[:, 32:][:, ::-1])[:, ::-1]       # right half keeps its own window display
    img = np.concatenate([left, right], axis=1)
    Image.fromarray(img).save(OUT)
    print("wrote", OUT, img.shape[1], "x", img.shape[0])


if __name__ == "__main__":
    main()
