"""Shared plumbing for the Centre / Mart design mockups.

Art is drawn on free-size canvases (multiples of 16 px) with colours taken from named palettes,
then checked the way the GBA would need it: every 8x8 tile of every layer must fit ONE 15-colour
palette, and a map cell can hold only two layers. Previews are composited over real map renders
(vanilla.py) with real NPC sprites.
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
sys.path.insert(0, os.path.join(HERE, "..", "hawker_tileset"))
from kit import Art as _Art, snap, sprite, up, TileBank  # noqa: E402

PEOPLE = "graphics/object_events/pics/people/"
OBJ_PALS = "graphics/object_events/palettes/"


def palette(**cols):
    """Named colours, snapped to BGR555. Max 15 (index 0 is transparent)."""
    d = {k: snap(v) for k, v in cols.items()}
    assert len(set(d.values())) <= 15, f"{len(set(d.values()))} colours"
    return d


class Art(_Art):
    """Canvas of RGB tuples (None = transparent) with a few drawing helpers."""

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def frame(self, x0, y0, x1, y1, c):
        self.hline(x0, x1, y0, c), self.hline(x0, x1, y1, c)
        self.vline(x0, y0, y1, c), self.vline(x1, y0, y1, c)

    def fill(self, x0, y0, x1, y1, fn):
        """fn(x, y) -> colour or None (leave), with x/y relative to the region's corner."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = fn(x - x0, y - y0)
                if c is not None:
                    self.put(x, y, c)

    def stamp(self, legend, text, x0=0, y0=0, flip=False):
        """ASCII art at (x0, y0). '.' / ' ' = transparent."""
        rows = [r for r in text.split("\n") if r.strip()]
        for y, row in enumerate(rows):
            if flip:
                row = row[::-1]
            for x, ch in enumerate(row):
                if ch in ". ":
                    continue
                self.put(x0 + x, y0 + y, legend[ch])
        return self

    def mirror_x(self):
        """Copy the left half onto the right half, mirrored."""
        for y in range(self.h):
            for x in range(self.w // 2):
                self.px[y][self.w - 1 - x] = self.px[y][x]
        return self

    def image(self):
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        px = im.load()
        for y in range(self.h):
            for x in range(self.w):
                if self.px[y][x] is not None:
                    px[x, y] = self.px[y][x] + (255,)
        return im


def from_image(im):
    """RGBA image -> Art (alpha 0 = transparent)."""
    im = im.convert("RGBA")
    a = Art(im.width, im.height)
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, al = px[x, y]
            if al:
                a.px[y][x] = (r, g, b)
    return a


# ------------------------------------------------------------------ GBA checks
def check(layers, palettes, name=""):
    """layers: {label: Art}; palettes: {label: {key: colour}}.
    Returns (unique tile count, [(layer, tile x, tile y, message)])."""
    bank, errors, usage = TileBank(), [], {k: 0 for k in palettes}
    pal_lists = {k: list(dict.fromkeys(v.values())) for k, v in palettes.items()}
    for label, a in layers.items():
        assert a.w % 8 == 0 and a.h % 8 == 0, (label, a.w, a.h)
        for ty in range(a.h // 8):
            for tx in range(a.w // 8):
                px = [[a.px[ty * 8 + y][tx * 8 + x] for x in range(8)] for y in range(8)]
                cols = {c for r in px for c in r} - {None}
                if not cols:
                    continue
                fit = [k for k, pl in pal_lists.items() if cols <= set(pl)]
                if not fit:
                    best = min(pal_lists, key=lambda k: len(cols - set(pal_lists[k])))
                    missing = sorted(cols - set(pal_lists[best]))
                    errors.append((label, tx, ty, f"closest '{best}' lacks {missing}"))
                    continue
                pl = pal_lists[fit[0]]
                usage[fit[0]] += 1
                bank.add(tuple(tuple(0 if c is None else pl.index(c) + 1 for c in r) for r in px))
    n = len(bank.tiles) - 1
    print(f"[{name}] {n} unique 8x8 tiles, palettes: "
          + ", ".join(f"{k} {len(pal_lists[k])}c/{usage[k]}t" for k in palettes)
          + (f", {len(errors)} PALETTE ERRORS" if errors else ", ok"))
    for e in errors[:12]:
        print("   ", e)
    return n, errors


def check_two_layers(under, over, ground_is_layer=True, name=""):
    """A cell where the under art has holes (ground shows through) AND over art exists would
    need three layers."""
    bad = []
    for ty in range(under.h // 16):
        for tx in range(under.w // 16):
            u = under.crop(tx * 16, ty * 16)
            o = over.crop(tx * 16, ty * 16)
            holes = any(c is None for r in u.px for c in r)
            if ground_is_layer and holes and not u.empty() and not o.empty():
                bad.append((tx, ty))
    if bad:
        print(f"[{name}] cells needing 3 layers: {bad}")
    return bad


def mark_errors(im, errors, layer_origin, scale=1):
    """Draw magenta boxes on failing tiles (debug)."""
    dr = ImageDraw.Draw(im)
    for label, tx, ty, _ in errors:
        ox, oy = layer_origin.get(label, (0, 0))
        x, y = (ox + tx * 8) * scale, (oy + ty * 8) * scale
        dr.rectangle((x, y, x + 8 * scale - 1, y + 8 * scale - 1), outline=(255, 0, 255))
    return im


# ------------------------------------------------------------------ staging
class Stage:
    """Ground render + art under sprites + sprites + art over sprites."""

    def __init__(self, under, over=None):
        self.under = under.convert("RGBA")
        self.over = over.convert("RGBA") if over else Image.new("RGBA", under.size, (0, 0, 0, 0))
        self.sprites = []

    @classmethod
    def blank(cls, w, h, colour=(0, 0, 0)):
        return cls(Image.new("RGBA", (w * 16, h * 16), colour + (255,)))

    def add(self, a, px, py, over=False):
        (self.over if over else self.under).alpha_composite(a.image(), (px, py))

    def paste(self, im, px, py, over=False):
        (self.over if over else self.under).alpha_composite(im.convert("RGBA"), (px, py))

    def npc(self, png, pal, frame, tx, ty, hflip=False, dy=0):
        """Frames: 0 down, 1 up, 2 left (hflip = right). (tx, ty) = the tile the NPC stands on."""
        self.sprites.append((ty, tx, png, pal, frame, hflip, dy))

    def render(self):
        im = self.under.copy()
        for ty, tx, png, pal, frame, hf, dy in sorted(self.sprites):
            s = sprite(PEOPLE + png, OBJ_PALS + pal, frame, hflip=hf)
            im.alpha_composite(s, (tx * 16, ty * 16 - 16 + dy))
        im.alpha_composite(self.over)
        return im

    def camera(self, tx, ty):
        """240x160 GBA view with the player standing on tile (tx, ty)."""
        im = self.render()
        ox, oy = tx * 16 - 112, ty * 16 - 72
        ox = max(0, min(im.width - 240, ox))
        oy = max(0, min(im.height - 160, oy))
        return im.crop((ox, oy, ox + 240, oy + 160))


def save(im, name, scale=3):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    up(im, scale).convert("RGB").save(p)
    return p
