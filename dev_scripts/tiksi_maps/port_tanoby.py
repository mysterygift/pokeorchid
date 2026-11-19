#!/usr/bin/env python3
"""
gTileset_TanobyDelta: the Tanoby Ruins chamber facade (FRLG Sevii Islands 6-7, metatiles 0x2C8-0x2E2)
ported onto Emerald's General primary, so Tanoby Delta can sit next to the other Tiksi maps.

Only the brick shrine itself comes from FRLG: it is the TOP layer of the 3x4 facade (one FRLG palette,
now slot 6). The BOTTOM layer is Emerald's own art: the rock-face metatile (0x071) behind the upper
rows, Emerald sand (0x124) under the bases, and the FRLG doorway's dark tiles behind the opening.
Sea, sand edges and rocks around the chambers are Emerald General tiles (dress.py), as the user asked.

Writes data/tilesets/secondary/tanoby_delta/{tiles.png, palettes/00-15.pal, metatiles.bin,
metatile_attributes.bin}; metatiles 0x200-0x20B are the facade, row by row.
usage: <venv>/python dev_scripts/tiksi_maps/port_tanoby.py   (needs Pillow)
"""
import os
import struct
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
OUT = P("data", "tilesets", "secondary", "tanoby_delta")
FACADE = [[0x2C8, 0x2C9, 0x2CA], [0x2D0, 0x2D1, 0x2D2], [0x2D8, 0x2D9, 0x2DA], [0x2E0, 0x2E1, 0x2E2]]
EM_ROCK, EM_SAND = 0x071, 0x124
NEW_PAL = 6                                   # first secondary palette slot
MB_NORMAL, LAYER_COVERED = 0x00, 1


def read_pal(path):
    tok = open(path).read().split()
    return [tuple(map(int, tok[3 + i * 3:6 + i * 3])) for i in range(int(tok[2]))]


def write_pal(path, cols):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in cols))


class Tiles:
    def __init__(self, d):
        im = Image.open(os.path.join(d, "tiles.png"))
        self.px, self.tw, self.n = im.load(), im.width // 8, (im.width // 8) * (im.height // 8)

    def get(self, t):
        x0, y0 = (t % self.tw) * 8, (t // self.tw) * 8
        return tuple(tuple(self.px[x0 + i, y0 + j] & 15 for i in range(8)) for j in range(8))


def metatiles(d):
    b = open(os.path.join(d, "metatiles.bin"), "rb").read()
    return [struct.unpack_from("<8H", b, i * 16) for i in range(len(b) // 16)]


def main():
    fr_pri = P("data", "tilesets", "primary", "general_frlg")
    fr_sec = P("data", "tilesets", "secondary", "sevii_islands_67_frlg")
    em_pri = P("data", "tilesets", "primary", "general")
    fp, fs = Tiles(fr_pri), Tiles(fr_sec)
    fmt_p, fmt_s = metatiles(fr_pri), metatiles(fr_sec)
    emt = metatiles(em_pri)
    fr_tile = lambda t: fp.get(t) if t < 640 else fs.get(t - 640)
    fr_mt = lambda m: fmt_p[m] if m < 640 else fmt_s[m - 640]
    src_pal = read_pal(os.path.join(fr_sec, "palettes", "05.pal"))

    bank, out_tiles = {}, []                 # pixel rows -> new secondary tile index (from 512)

    def add(px):
        if not any(any(r) for r in px):
            return None
        if px not in bank:
            bank[px] = 512 + len(out_tiles)
            out_tiles.append(px)
        return bank[px]

    mts, attrs = [], []
    for ry, row in enumerate(FACADE):
        for rx, m in enumerate(row):
            src = fr_mt(m)
            top = []
            for v in src[4:]:
                t, flips, p = v & 0x3FF, v & 0x0C00, v >> 12
                assert p == 5, (hex(m), p)
                idx = add(fr_tile(t))
                top.append(0 if idx is None else (idx | flips | NEW_PAL << 12))
            if ry <= 1 or (ry == 2 and rx != 1):
                bottom = list(emt[EM_ROCK][:4])
            elif ry == 3 and rx != 1:
                bottom = list(emt[EM_SAND][:4])
            else:                             # the doorway: FRLG's dark tiles where it shows, else rock / sand
                base = emt[EM_ROCK] if ry == 2 else emt[EM_SAND]
                bottom = []
                for q, v in enumerate(src[:4]):
                    t, flips, p = v & 0x3FF, v & 0x0C00, v >> 12
                    door = (ry == 2 and q >= 2) or (ry == 3 and q < 2)
                    if door and p == 5:
                        bottom.append(add(fr_tile(t)) | flips | NEW_PAL << 12)
                    else:
                        bottom.append(base[q])
            mts.append(bottom + top)
            attrs.append(MB_NORMAL | LAYER_COVERED << 12)

    os.makedirs(os.path.join(OUT, "palettes"), exist_ok=True)
    cols = (src_pal + [(0, 0, 0)] * 16)[:16]
    for i in range(16):
        write_pal(os.path.join(OUT, "palettes", "%02d.pal" % i), cols if i == NEW_PAL else [(0, 0, 0)] * 16)
    n = len(out_tiles)
    w, h = 16, max(1, (n + 15) // 16)
    im = Image.new("P", (w * 8, h * 8), 0)
    im.putpalette([c for rgb in cols for c in rgb] + [0] * (768 - 48))
    px = im.load()
    for k, t in enumerate(out_tiles):
        x0, y0 = (k % w) * 8, (k // w) * 8
        for j in range(8):
            for i in range(8):
                px[x0 + i, y0 + j] = t[j][i]
    im.save(os.path.join(OUT, "tiles.png"))
    open(os.path.join(OUT, "metatiles.bin"), "wb").write(b"".join(struct.pack("<8H", *m) for m in mts))
    open(os.path.join(OUT, "metatile_attributes.bin"), "wb").write(b"".join(struct.pack("<H", a) for a in attrs))
    print("tanoby_delta: %d metatiles (0x200-0x%03X), %d tiles, palette slot %d" % (len(mts), 0x200 + len(mts) - 1, n, NEW_PAL))


if __name__ == "__main__":
    main()
