#!/usr/bin/env python3
"""Day/night (DNS) helper for Orchid's overworld tilesets.

The expansion's DNS (OW_ENABLE_DNS) tints outdoor maps by time of day. A palette colour listed in the
palette's .pla file is a "light": at night it blends toward warm yellow (src/palette.c DEFAULT_LIGHT_COLOR)
instead of darkening, so window glass listed there glows. A colour may only be a light if nothing but
windows/lamps uses that (palette, index) pair, so this tool renders maps with every pixel's pair recorded.

    dns_tool.py render LAYOUT_ID out.png [--night] [--zoom N]
        day (or simulated full-night) render of a layout, using the .pla files on disk
    dns_tool.py where LAYOUT_ID PAL IDX out.png
        day render with every pixel using (PAL, IDX) outlined in magenta, to spot conflicts
    dns_tool.py pairs LAYOUT_ID X0 Y0 X1 Y1
        (pal, idx) pairs used inside a pixel rectangle of the layout, with counts and colours
    dns_tool.py usage TILESET_LABEL PAL IDX
        every metatile of the tileset pair that uses (PAL, IDX), so a split can be checked tileset-wide
"""
import json
import os
import re
import struct
import sys

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LIGHT = (248, 224, 120)                       # src/palette.c DEFAULT_LIGHT_COLOR
TINT_NIGHT = (0.456, 0.456, 0.615)            # src/overworld.c TINT_NIGHT (Q8.8 multiply)
NUM_PALS_IN_PRIMARY = 6


def tileset_dir(label):
    name = re.sub(r"^gTileset_", "", label)
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    for kind in ("primary", "secondary"):
        p = os.path.join(ROOT, "data", "tilesets", kind, snake)
        if os.path.isdir(p):
            return p
    raise SystemExit(f"tileset dir for {label} not found ({snake})")


def load_pal(path):
    v = open(path).read().split()
    vals = list(map(int, v[3:3 + 48]))
    return [tuple(vals[j * 3:j * 3 + 3]) for j in range(16)]


def load_pla(path):
    if not os.path.exists(path):
        return set()
    out = set()
    for line in open(path):
        line = line.split("#")[0].strip()
        if line:
            out.add(int(line))
    return out


def load_tiles(d):
    img = Image.open(os.path.join(d, "tiles.png"))
    w, h = img.size
    px = img.load()
    return [[[px[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)]
            for ty in range(h // 8) for tx in range(w // 8)]


def load_metatiles(d):
    data = open(os.path.join(d, "metatiles.bin"), "rb").read()
    return [struct.unpack_from("<8H", data, i) for i in range(0, len(data), 16)]


class Tilesets:
    def __init__(self, primary, secondary):
        self.pd, self.sd = tileset_dir(primary), tileset_dir(secondary)
        self.ptiles, self.stiles = load_tiles(self.pd), load_tiles(self.sd)
        self.pals, self.lights = [], []
        for i in range(16):
            d = self.pd if i < NUM_PALS_IN_PRIMARY or i >= 13 else self.sd
            p = os.path.join(d, "palettes", f"{i:02d}.pal")
            self.pals.append(load_pal(p) if os.path.exists(p) else [(0, 0, 0)] * 16)
            self.lights.append(load_pla(p[:-4] + ".pla"))
        self.pmeta, self.smeta = load_metatiles(self.pd), load_metatiles(self.sd)

    def entries(self, mid):
        if mid < 512:
            return self.pmeta[mid] if mid < len(self.pmeta) else None
        return self.smeta[mid - 512] if mid - 512 < len(self.smeta) else None

    def metatile(self, mid):
        """16x16 list of (pal, idx, tile) for the topmost opaque pixel (layer 1 over layer 0)."""
        cells = [[(0, 0, -1)] * 16 for _ in range(16)]
        ent = self.entries(mid)
        if ent is None:
            return cells
        for layer in range(2):
            for q in range(4):
                e = ent[layer * 4 + q]
                t, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                tile = self.ptiles[t] if t < 512 else (self.stiles[t - 512] if t - 512 < len(self.stiles) else None)
                if tile is None:
                    continue
                ox, oy = (q & 1) * 8, (q >> 1) * 8
                for y in range(8):
                    for x in range(8):
                        c = tile[7 - y if vf else y][7 - x if hf else x]
                        if c == 0 and layer == 1:
                            continue
                        cells[oy + y][ox + x] = (pal, c, t)
        return cells


def load_layout(layout_id):
    L = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    lay = next(l for l in L if l.get("id") == layout_id)
    ts = Tilesets(lay["primary_tileset"], lay["secondary_tileset"])
    w, h = lay["width"], lay["height"]
    blocks = struct.unpack(f"<{w*h}H", open(os.path.join(ROOT, lay["blockdata_filepath"]), "rb").read())
    info = [[None] * (w * 16) for _ in range(h * 16)]
    cache = {}
    for i, b in enumerate(blocks):
        mid = b & 0x3FF
        if mid not in cache:
            cache[mid] = ts.metatile(mid)
        x0, y0 = (i % w) * 16, (i // w) * 16
        for y in range(16):
            info[y0 + y][x0:x0 + 16] = cache[mid][y]
    return ts, info, blocks, w


def colour(ts, cell, night):
    pal, idx, _ = cell
    c = ts.pals[pal][idx if idx else 0]
    if not night:
        return c
    if idx in ts.lights[pal] and pal != 0:
        alt = ts.pals[pal][0] if 0 in ts.lights[pal] else LIGHT
        return tuple(int(c[k] + (alt[k] - c[k]) * 16 / 32) for k in range(3))
    return tuple(min(248, int(c[k] * TINT_NIGHT[k])) for k in range(3))


def image(ts, info, night=False, mark=None):
    h, w = len(info), len(info[0])
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            cell = info[y][x]
            px[x, y] = colour(ts, cell, night)
            if mark and (cell[0], cell[1]) == mark:
                px[x, y] = (255, 0, 255)
    return im


def main():
    cmd = sys.argv[1]
    if cmd == "render":
        ts, info, _, _ = load_layout(sys.argv[2])
        im = image(ts, info, night="--night" in sys.argv)
        z = int(sys.argv[sys.argv.index("--zoom") + 1]) if "--zoom" in sys.argv else 1
        im.resize((im.width * z, im.height * z), Image.NEAREST).save(sys.argv[3])
    elif cmd == "where":
        ts, info, _, _ = load_layout(sys.argv[2])
        image(ts, info, mark=(int(sys.argv[3]), int(sys.argv[4]))).save(sys.argv[5])
    elif cmd == "pairs":
        ts, info, _, _ = load_layout(sys.argv[2])
        x0, y0, x1, y1 = map(int, sys.argv[3:7])
        cnt = {}
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                k = info[y][x][:2]
                cnt[k] = cnt.get(k, 0) + 1
        for (p, i), n in sorted(cnt.items(), key=lambda kv: -kv[1]):
            print(f"pal {p:2d} idx {i:2d} {ts.pals[p][i]} x{n}{'  LIGHT' if i in ts.lights[p] else ''}")
    elif cmd == "sheet":
        # sheet PRIMARY SECONDARY out_prefix [--night]: pages of 16x16 metatiles (2x), hex id of each row's first
        from PIL import ImageDraw
        ts = Tilesets(sys.argv[2], sys.argv[3])
        night = "--night" in sys.argv
        ids = list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))]
        rows_per_page = 16
        rows = [ids[i:i + 16] for i in range(0, len(ids), 16)]
        for pg in range(0, len(rows), rows_per_page):
            chunk = rows[pg:pg + rows_per_page]
            im = Image.new("RGB", (40 + 16 * 18, len(chunk) * 18), (20, 20, 20))
            dr = ImageDraw.Draw(im)
            for r, row in enumerate(chunk):
                dr.text((2, r * 18 + 3), f"{row[0]:03X}", fill=(255, 255, 0))
                for c, m in enumerate(row):
                    cells = ts.metatile(m)
                    for y in range(16):
                        for x in range(16):
                            im.putpixel((40 + c * 18 + x, r * 18 + y), colour(ts, cells[y][x], night))
            im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(f"{sys.argv[4]}_{pg // rows_per_page}.png")
    elif cmd in ("usage", "usesheet"):
        # usage PRIMARY SECONDARY PAL IDX[,IDX...] [out.png]
        ts = Tilesets(sys.argv[2], sys.argv[3])
        pal = int(sys.argv[4])
        idxs = {int(i) for i in sys.argv[5].split(",")}
        ids = list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))]
        hits = [m for m in ids if any(c[0] == pal and c[1] in idxs for row in ts.metatile(m) for c in row)]
        print(len(hits), " ".join(f"{m:03X}" for m in hits))
        if cmd == "usesheet":
            cols = 16
            rows = (len(hits) + cols - 1) // cols
            im = Image.new("RGB", (cols * 34, rows * 18), (20, 20, 20))
            for n, m in enumerate(hits):
                cells = ts.metatile(m)
                x0, y0 = (n % cols) * 34, (n // cols) * 18
                for y in range(16):
                    for x in range(16):
                        c = cells[y][x]
                        im.putpixel((x0 + x, y0 + y), colour(ts, c, False))
                        im.putpixel((x0 + 17 + x, y0 + y),
                                    (255, 0, 255) if c[0] == pal and c[1] in idxs else colour(ts, c, False))
            im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(sys.argv[6])


if __name__ == "__main__":
    main()
