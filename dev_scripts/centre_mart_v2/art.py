#!/usr/bin/env python3
"""Fit the supplied Centre / Mart art to the metatile grid and to General palettes 1 / 0.

    art/centre_src.png  79x80, mirror axis on column 39      -> art/centre.png 80x80 (5x5 metatiles)
    art/mart_src.png    66x72, mirror axis between 32 | 33   -> art/mart.png   64x80 (4x5 metatiles)

Both are made exactly symmetric (left half mirrored) so the right half reuses the left half's tiles
with h-flip; only the Centre's arrow sign and the Mart's window display keep their own right-hand
pixels. Colours are snapped to the existing palette entries (the General palettes are shared with
houses in a dozen town tilesets, so their colours cannot change).

    python art.py
"""
import os

import numpy as np
from PIL import Image

from common import HERE, GEN


def read_pal(i):
    lines = open(os.path.join(GEN, "palettes", f"{i:02d}.pal")).read().split("\n")[3:19]
    return [tuple(int(v) for v in l.split()) for l in lines]


# source colour -> palette colour
MAP_CENTRE = {  # palette 1: four reds instead of five, no dark blue
    (248, 200, 136): (255, 189, 131), (232, 144, 112): (238, 148, 115), (216, 104, 96): (222, 106, 98),
    (200, 80, 72): (222, 106, 98), (168, 32, 40): (205, 65, 82), (200, 216, 232): (222, 230, 238),
    (240, 240, 248): (255, 255, 255), (168, 184, 200): (189, 205, 230), (144, 160, 176): (156, 180, 222),
    (120, 120, 128): (131, 131, 139), (64, 72, 104): (65, 74, 106), (112, 184, 240): (115, 189, 246),
    (96, 160, 216): (98, 172, 238), (72, 128, 192): (98, 98, 123), (152, 208, 248): (189, 205, 230),
}
MAP_MART = {  # palette 0
    (72, 128, 192): (82, 139, 197), (48, 96, 160): (74, 115, 172), (112, 184, 240): (115, 189, 246),
    (96, 160, 216): (98, 164, 222), (152, 208, 248): (189, 205, 230), (240, 240, 248): (255, 255, 255),
    (200, 216, 232): (222, 230, 238), (168, 184, 200): (189, 205, 230), (144, 160, 176): (156, 180, 222),
    (120, 120, 128): (131, 131, 139), (88, 88, 112): (98, 98, 123), (80, 80, 104): (98, 98, 123),
    (64, 72, 104): (65, 74, 106),
}


def load(name):
    return np.array(Image.open(os.path.join(HERE, "art", name)).convert("RGBA"))


def snap(a, mapping):
    out = a.copy()
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x, 3]:
                out[y, x, :3] = mapping[tuple(int(v) for v in a[y, x, :3])]
            else:
                out[y, x] = 0
    return out


OUTLINE = (65, 74, 106)


def close_door_gap(w, x0, x1):
    """Door animations redraw the door cells without the ground layer, so the door cells must be
    opaque: carry the building's dark base line under the door (no raised step)."""
    for y in range(64, 80):
        for x in range(x0, x1):
            if not w[y, x, 3]:
                w[y, x] = (*OUTLINE, 255)


def centre():
    c = load("centre_src.png")
    w = np.zeros((80, 80, 4), np.uint8)
    w[:, :40] = c[:, :40]
    w[:, 40:] = c[:, :40][:, ::-1]
    w[58:80, 56:80] = c[58:80, 55:79]          # arrow sign (source column j -> j + 1)
    w = snap(w, MAP_CENTRE)
    close_door_gap(w, 32, 48)
    return w


def mart():
    m = load("mart_src.png")
    left = np.concatenate([m[:, 0:1], m[:, 2:33]], axis=1)       # 32 px: drop one column inside the outline
    right = np.concatenate([m[:, 33:64], m[:, 65:66]], axis=1)
    w = np.zeros((80, 64, 4), np.uint8)
    w[8:, :32] = left
    w[8:, 32:] = left[:, ::-1]
    w[60:80, 43:63] = right[52:72, 11:31]       # window display
    w = snap(w, MAP_MART)
    close_door_gap(w, 16, 48)
    return w


def main():
    for name, a in (("centre", centre()), ("mart", mart())):
        Image.fromarray(a).save(os.path.join(HERE, "art", name + ".png"))
        Image.fromarray(a).resize((a.shape[1] * 4, a.shape[0] * 4), Image.NEAREST).save(
            os.path.join(HERE, "out", name + "_x4.png"))
        print(name, a.shape[1], "x", a.shape[0])


if __name__ == "__main__":
    main()
