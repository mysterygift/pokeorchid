#!/usr/bin/env python3
"""Vanilla Centre / Mart next to the new ones at 5x on grass, for judging shading and contrast.

    python study.py      # writes out/study_5x.png
"""
import collections
import os

from PIL import Image

import centre_exterior
import mart_exterior
import vanilla
from mock import OUT


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def stats(name, b):
    cnt = collections.Counter(c for a in (b["under"], b["over"]) for r in a.px for c in r if c)
    tot = sum(cnt.values())
    white = 100 * sum(n for c, n in cnt.items() if lum(c) >= 240) / tot
    dark = 100 * sum(n for c, n in cnt.items() if lum(c) <= 80) / tot
    print(f"{name}: {len(cnt)} colours, {white:.0f}% near-white, {dark:.0f}% dark outline")


if __name__ == "__main__":
    sc, grid, under, over = vanilla.render("LAYOUT_OLDALE_TOWN")
    under.alpha_composite(over)
    c, m = centre_exterior.build(), mart_exterior.build()
    stats("new Centre", c), stats("new Mart", m)
    gap = 8
    im = Image.new("RGBA", (64 + c["under"].w + 64 + m["under"].w + gap * 5, 64 + gap * 2), (112, 192, 152, 255))
    x = gap
    for kind in ("vc", "c", "vm", "m"):
        if kind == "vc":
            im.paste(under.crop((5 * 16, 13 * 16, 9 * 16, 17 * 16)), (x, gap)); x += 64 + gap
        elif kind == "vm":
            im.paste(under.crop((14 * 16, 13 * 16, 18 * 16, 17 * 16)), (x, gap)); x += 64 + gap
        else:
            b = c if kind == "c" else m
            y = gap + 64 - b["under"].h
            im.alpha_composite(b["under"].image(), (x, y)), im.alpha_composite(b["over"].image(), (x, y))
            x += b["under"].w + gap
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "study_5x.png")
    im.resize((im.width * 5, im.height * 5), Image.NEAREST).convert("RGB").save(p)
    print(p)
