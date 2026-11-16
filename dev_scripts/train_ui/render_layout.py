#!/usr/bin/env python3
"""Render a map layout (or a tileset's metatile sheet) to PNG, straight from the repo data.

    python3 dev_scripts/train_ui/render_layout.py layout LAYOUT_TRAIN_TEST_STATION out.png [--collision]
    python3 dev_scripts/train_ui/render_layout.py sheet general slateport out.png

Reads data/layouts/layouts.json, data/tilesets/{primary,secondary}/<name>/{tiles.png,palettes/*.pal,
metatiles.bin} and blockdata. Only bottom+top layers are composited (no animations). --collision
tints impassable blocks red so test maps can be checked without Porymap.
"""
import json
import os
import re
import struct
import sys

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def tileset_dir(label):
    # gTileset_General -> general ; gTileset_SecretBaseBrownCave -> secret_base/brown_cave is rare; good enough
    name = re.sub(r"^gTileset_", "", label)
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    for kind in ("primary", "secondary"):
        p = os.path.join(ROOT, "data", "tilesets", kind, snake)
        if os.path.isdir(p):
            return p
    raise SystemExit(f"tileset dir for {label} not found ({snake})")


def load_pals(d):
    pals = []
    for i in range(16):
        p = os.path.join(d, "palettes", f"{i:02d}.pal")
        cols = [(0, 0, 0)] * 16
        if os.path.exists(p):
            lines = open(p).read().split()
            vals = list(map(int, lines[3:3 + 48]))
            cols = [tuple(vals[j * 3:j * 3 + 3]) for j in range(16)]
        pals.append(cols)
    return pals


def load_tiles(d):
    img = Image.open(os.path.join(d, "tiles.png"))
    w, h = img.size
    px = img.load()
    tiles = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            tiles.append([[px[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)])
    return tiles


def load_metatiles(d):
    data = open(os.path.join(d, "metatiles.bin"), "rb").read()
    return [struct.unpack_from("<8H", data, i) for i in range(0, len(data), 16)]


class Tilesets:
    def __init__(self, primary, secondary):
        pd, sd = tileset_dir(primary), tileset_dir(secondary)
        self.ptiles, self.stiles = load_tiles(pd), load_tiles(sd)
        ppals, spals = load_pals(pd), load_pals(sd)
        self.pals = ppals[:6] + spals[6:13] + ppals[13:]
        self.pmeta, self.smeta = load_metatiles(pd), load_metatiles(sd)

    def metatile(self, mid):
        entries = self.pmeta[mid] if mid < 512 else self.smeta[mid - 512] if mid - 512 < len(self.smeta) else None
        im = Image.new("RGB", (16, 16), (255, 0, 255))
        if entries is None:
            return im
        px = im.load()
        for layer in range(2):
            for q in range(4):
                e = entries[layer * 4 + q]
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
                        px[ox + x, oy + y] = self.pals[pal][c]
        return im


def render_layout(layout_id, out, collision=False):
    L = json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
    lay = next(l for l in L if l.get("id") == layout_id)
    ts = Tilesets(lay["primary_tileset"], lay["secondary_tileset"])
    w, h = lay["width"], lay["height"]
    blocks = struct.unpack(f"<{w*h}H", open(os.path.join(ROOT, lay["blockdata_filepath"]), "rb").read())
    im = Image.new("RGB", (w * 16, h * 16))
    dr = ImageDraw.Draw(im, "RGBA")
    cache = {}
    for i, b in enumerate(blocks):
        mid = b & 0x3FF
        if mid not in cache:
            cache[mid] = ts.metatile(mid)
        x, y = (i % w) * 16, (i // w) * 16
        im.paste(cache[mid], (x, y))
        if collision and (b >> 10) & 3:
            dr.rectangle([x, y, x + 15, y + 15], fill=(255, 0, 0, 70))
    im.save(out)


def render_sheet(primary, secondary, out, cols=8):
    ts = Tilesets(f"gTileset_{primary.title().replace('_','')}", f"gTileset_{secondary.title().replace('_','')}")
    ids = list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))]
    rows = (len(ids) + cols - 1) // cols
    im = Image.new("RGB", (cols * 16 * 3 + cols * 30, rows * 50), (40, 40, 40))
    dr = ImageDraw.Draw(im)
    for n, mid in enumerate(ids):
        x, y = (n % cols) * (48 + 30), (n // cols) * 50
        im.paste(ts.metatile(mid).resize((48, 48), Image.NEAREST), (x, y))
        dr.text((x + 50, y + 18), f"{mid:03X}", fill=(255, 255, 255))
    im.save(out)


if __name__ == "__main__":
    if sys.argv[1] == "layout":
        render_layout(sys.argv[2], sys.argv[3], "--collision" in sys.argv)
    else:
        render_sheet(sys.argv[2], sys.argv[3], sys.argv[4])
