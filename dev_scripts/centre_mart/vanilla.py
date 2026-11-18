"""Render existing layouts / tilesets straight from the repo data, so new building art can be
mocked up inside real maps. Two passes are returned: everything under sprites, and the top layer
of LAYER_NORMAL metatiles (drawn over sprites)."""
import json
import os
import re
import struct

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def load_jasc(path):
    vals = open(path).read().split()[3:]
    return [tuple(int(v) // 8 * 8 for v in vals[i * 3:i * 3 + 3]) for i in range(len(vals) // 3)]


def tileset_dir(sym):
    """gTileset_PokemonCenter -> data/tilesets/secondary/pokemon_center"""
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", sym.replace("gTileset_", "")).lower()
    for kind in ("primary", "secondary"):
        p = os.path.join(ROOT, "data", "tilesets", kind, name)
        if os.path.isdir(p):
            return p
    raise FileNotFoundError(sym)


class Tileset:
    def __init__(self, sym):
        d = tileset_dir(sym)
        im = Image.open(os.path.join(d, "tiles.png"))
        assert im.mode == "P", im.mode
        self.w = im.width // 8
        self.px = im.load()
        self.n = self.w * (im.height // 8)
        raw = open(os.path.join(d, "metatiles.bin"), "rb").read()
        self.metatiles = [struct.unpack_from("<8H", raw, i * 16) for i in range(len(raw) // 16)]
        raw = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
        self.attrs = list(struct.unpack(f"<{len(raw) // 2}H", raw))
        self.pals = [load_jasc(os.path.join(d, "palettes", f"{i:02d}.pal")) for i in range(16)]

    def tile(self, i):
        ox, oy = (i % self.w) * 8, (i // self.w) * 8
        return [[self.px[ox + x, oy + y] & 15 for x in range(8)] for y in range(8)]


class Scene:
    """A primary + secondary pair that can draw any metatile id."""

    def __init__(self, primary, secondary):
        self.p, self.s = Tileset(primary), Tileset(secondary)
        self.pals = self.p.pals[:6] + self.s.pals[6:13] + self.p.pals[13:]
        self.cache = {}

    def _meta(self, mid):
        ts, i = (self.p, mid) if mid < 0x200 else (self.s, mid - 0x200)
        if i >= len(ts.metatiles):
            return (0,) * 8, 0
        return ts.metatiles[i], (ts.attrs[i] >> 12) & 3

    def metatile(self, mid):
        """-> (under, over) RGBA 16x16 images."""
        if mid in self.cache:
            return self.cache[mid]
        entries, layer = self._meta(mid)
        under = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
        over = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for k, e in enumerate(entries):
            t, hf, vf, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            ts, ti = (self.p, t) if t < 512 else (self.s, t - 512)
            if ti >= ts.n:
                continue
            tile, q = ts.tile(ti), k & 3
            top = k >= 4
            dst = (over if (top and layer == 0) else under).load()
            for y in range(8):
                for x in range(8):
                    ci = tile[7 - y if vf else y][7 - x if hf else x]
                    if ci == 0 and top:
                        continue
                    dst[(q & 1) * 8 + x, (q >> 1) * 8 + y] = self.pals[pal][ci] + (255,)
        self.cache[mid] = (under, over)
        return under, over


def _git(ref, path):
    import subprocess
    return subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{path}"], capture_output=True, check=True).stdout


def layout(layout_id, ref=None):
    """ref: read the layout from a git ref (e.g. "upstream/master") instead of the working tree,
    for art lifted from vanilla maps that Orchid has since rebuilt."""
    if ref:
        js = json.loads(_git(ref, "data/layouts/layouts.json"))
        for entry in js["layouts"]:
            if entry.get("id") == layout_id:
                w, h = entry["width"], entry["height"]
                blocks = struct.unpack(f"<{w * h}H", _git(ref, entry["blockdata_filepath"])[:2 * w * h])
                grid = [[blocks[y * w + x] & 0x3FF for x in range(w)] for y in range(h)]
                border = struct.unpack("<4H", _git(ref, entry["border_filepath"])[:8])
                return entry, grid, [b & 0x3FF for b in border]
        raise KeyError(layout_id)
    js = json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))
    for entry in js["layouts"]:
        if entry.get("id") == layout_id:
            w, h = entry["width"], entry["height"]
            raw = open(os.path.join(ROOT, entry["blockdata_filepath"]), "rb").read()
            blocks = struct.unpack(f"<{w * h}H", raw)
            grid = [[blocks[y * w + x] & 0x3FF for x in range(w)] for y in range(h)]
            border = struct.unpack("<4H", open(os.path.join(ROOT, entry["border_filepath"]), "rb").read()[:8])
            return entry, grid, [b & 0x3FF for b in border]
    raise KeyError(layout_id)


def render(layout_id, pad=0):
    entry, grid, border = layout(layout_id)
    sc = Scene(entry["primary_tileset"], entry["secondary_tileset"])
    w, h = entry["width"], entry["height"]
    under = Image.new("RGBA", ((w + 2 * pad) * 16, (h + 2 * pad) * 16))
    over = Image.new("RGBA", under.size, (0, 0, 0, 0))
    for y in range(-pad, h + pad):
        for x in range(-pad, w + pad):
            mid = grid[y][x] if (0 <= x < w and 0 <= y < h) else border[(y & 1) * 2 + (x & 1)]
            u, o = sc.metatile(mid)
            under.paste(u, ((x + pad) * 16, (y + pad) * 16))
            over.paste(o, ((x + pad) * 16, (y + pad) * 16))
    return sc, grid, under, over



_town = None


def emblem(kind):
    """The roof emblem of the existing Centre ('centre') or Mart ('mart'), 20x14 px, exactly as it
    is in gTileset_General (taken from the buildings placed in the Oldale/Telok layout). Opaque:
    the corners are the roof band colour it sits on."""
    global _town
    if _town is None:
        _, _, under, over = render("LAYOUT_OLDALE_TOWN")
        under.alpha_composite(over)
        _town = under
    tx = {"centre": 5, "mart": 14}[kind]
    return _town.crop((tx * 16 + 22, 13 * 16 + 25, tx * 16 + 42, 13 * 16 + 39))


if __name__ == "__main__":
    import sys
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for lid in sys.argv[2:]:
        sc, grid, under, over = render(lid)
        under.alpha_composite(over)
        under = under.resize((under.width * 2, under.height * 2), Image.NEAREST)
        under.save(os.path.join(out, lid.lower() + ".png"))
        print(lid, under.size)
