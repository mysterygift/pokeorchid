"""Read Gen 3 tilesets (tiles.png + JASC palettes + metatiles.bin) and render metatiles."""
import os
import struct
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_pal(path):
    lines = open(path).read().split()
    n = int(lines[2])
    vals = list(map(int, lines[3:3 + n * 3]))
    return [tuple(vals[i * 3:i * 3 + 3]) for i in range(n)]


class Tileset:
    def __init__(self, rel):
        d = os.path.join(ROOT, "data", "tilesets", rel)
        self.dir = d
        im = Image.open(os.path.join(d, "tiles.png"))
        assert im.mode == "P", im.mode
        self.w, self.h = im.size
        px = im.load()
        self.tiles = []
        for ty in range(self.h // 8):
            for tx in range(self.w // 8):
                self.tiles.append([[px[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)])
        self.pals = [load_pal(os.path.join(d, "palettes", "%02d.pal" % i)) for i in range(16)]
        raw = open(os.path.join(d, "metatiles.bin"), "rb").read()
        self.metatiles = [struct.unpack_from("<8H", raw, i) for i in range(0, len(raw), 16)]
        araw = open(os.path.join(d, "metatile_attributes.bin"), "rb").read()
        self.attrs = list(struct.unpack("<%dH" % (len(araw) // 2), araw)) if len(araw) // 2 == len(self.metatiles) \
            else list(struct.unpack("<%dI" % (len(araw) // 4), araw))


class Pair:
    """primary + secondary as the game sees them (tiles 0-511 / 512+, metatiles 0-511 / 512+)."""

    def __init__(self, primary, secondary=None):
        self.p = Tileset(primary)
        self.s = Tileset(secondary) if secondary else None

    def tile(self, n):
        if not self.s:
            return self.p.tiles[n] if n < len(self.p.tiles) else [[0] * 8] * 8
        if n < 512:
            return self.p.tiles[n] if n < len(self.p.tiles) else [[0] * 8] * 8
        n -= 512
        return self.s.tiles[n] if self.s and n < len(self.s.tiles) else [[0] * 8] * 8

    def pal(self, n):
        if n < 6 or not self.s:
            return self.p.pals[n]
        return self.s.pals[n]

    def meta(self, n):
        if n < 512 or not self.s:
            return self.p.metatiles[n]
        return self.s.metatiles[n - 512]

    def attr(self, n):
        return self.p.attrs[n] if n < 512 else self.s.attrs[n - 512]

    def render_entry(self, img, e, ox, oy, transparent):
        t = self.tile(e & 0x3FF)
        hf, vf, pal = e >> 10 & 1, e >> 11 & 1, e >> 12
        cols = self.pal(pal)
        px = img.load()
        for y in range(8):
            for x in range(8):
                c = t[7 - y if vf else y][7 - x if hf else x]
                if c == 0 and transparent:
                    continue
                if 0 <= ox + x < img.width and 0 <= oy + y < img.height:
                    px[ox + x, oy + y] = cols[c]

    def render_meta(self, img, n, ox, oy, layers=(0, 1)):
        m = self.meta(n)
        for li, layer in enumerate(layers):
            for i in range(4):
                e = m[layer * 4 + i]
                self.render_entry(img, e, ox + (i % 2) * 8, oy + (i // 2) * 8, transparent=li > 0)


def sheet(pair, ids, cols=8, scale=1):
    ids = list(ids)
    rows = (len(ids) + cols - 1) // cols
    img = Image.new("RGB", (cols * 16, rows * 16), (255, 0, 255))
    for i, n in enumerate(ids):
        pair.render_meta(img, n, (i % cols) * 16, (i // cols) * 16)
    return img.resize((img.width * scale, img.height * scale), Image.NEAREST)
