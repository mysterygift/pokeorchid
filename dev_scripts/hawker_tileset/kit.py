"""Shared plumbing for the hawker-centre tileset generator: colours, palettes, ASCII art -> tiles,
metatile packing, file writers. Art lives in art_shell.py / art_stalls.py; the list of metatiles
and the mock map live in export_tileset.py."""
import os
import struct

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TS_DIR = os.path.join(ROOT, "data", "tilesets", "secondary", "hawker_centre")
OUT = os.path.join(HERE, "out")

SECONDARY_TILE_BASE = 512
SECONDARY_METATILE_BASE = 0x200
LAYER_NORMAL, LAYER_COVERED, LAYER_SPLIT = 0, 1, 2

BLACK = (0, 0, 0)


def snap(c):
    """Round to BGR555 (multiples of 8, max 248)."""
    return tuple(min(248, max(0, (v + 4) // 8 * 8)) for v in c)


# ------------------------------------------------------------------ colours
# Shared base: vanilla interiors use (82,82,106) as the outline instead of black.
INK = snap((80, 80, 104))
STEEL_D, STEEL_M, STEEL_L, WHITE = (snap(c) for c in
                                    ((128, 136, 152), (176, 184, 192), (216, 224, 232), (248, 248, 248)))

# pal 6: floors, potted plants, the black void beyond the open sides
FLOOR = dict(
    K=INK,
    H=snap((248, 240, 216)), F=snap((232, 220, 188)), G=snap((200, 184, 152)),      # dining tile
    S=snap((192, 180, 160)), s=snap((160, 144, 128)),                               # ... in shade
    t=snap((232, 160, 120)), T=snap((208, 128, 96)), D=snap((168, 96, 80)), E=snap((128, 72, 64)),  # quarry
    y=snap((168, 224, 128)), g=snap((120, 200, 104)), v=snap((80, 160, 88)), V=snap((48, 120, 72)),  # leaves
    X=BLACK,                                                                        # void outside the hall
)
# pal 7: stall shell (walls, counters, pillars, kitchen floor, railings)
SHELL = dict(
    K=INK, d=STEEL_D, M=STEEL_M, l=STEEL_L, W=WHITE,
    C=snap((240, 232, 208)), c=snap((208, 200, 176)), x=snap((160, 152, 136)),      # wall tiles
    N=snap((56, 64, 88)), n=snap((40, 40, 56)), o=snap((104, 104, 128)),            # roof edge, dark
    e=snap((40, 112, 120)), T=snap((80, 160, 160)), t=snap((160, 216, 208)),        # teal trim
    Y=snap((248, 232, 144)),
)
# pal 8: furniture + tableware
FURN = dict(
    K=INK, d=STEEL_D, M=STEEL_M, l=STEEL_L, W=WHITE,
    o=snap((184, 80, 32)), O=snap((240, 128, 48)), p=snap((248, 184, 104)),         # orange stools
    e=snap((32, 120, 112)), T=snap((64, 176, 160)), t=snap((144, 224, 200)),        # teal trim, trays
    Y=snap((248, 216, 80)), R=snap((216, 56, 48)), B=snap((136, 88, 56)), c=snap((248, 232, 184)),
)


def stall_pal(ramp_a, ramp_b, extras):
    """Stall palettes share slots: 1-4 base, 5-7 sign ramp A, 8-10 sign ramp B, 11-15 extras.
    Sign frames / counter stripes drawn with a/A/h or g/G/j therefore share tiles across stalls."""
    d = dict(K=INK, d=STEEL_D, l=STEEL_L, W=WHITE)
    d.update(zip("aAh", map(snap, ramp_a)))
    d.update(zip("gGj", map(snap, ramp_b)))
    d.update({k: snap(v) for k, v in extras.items()})
    assert len(d) <= 15, len(d)
    return d


ORANGE = ((176, 64, 32), (232, 112, 40), (248, 176, 96))
GREEN = ((40, 104, 64), (72, 160, 88), (152, 216, 128))
YELLOW = ((184, 128, 24), (240, 192, 48), (248, 232, 136))
RED = ((152, 32, 40), (216, 56, 48), (248, 128, 104))
BROWN = ((96, 56, 40), (152, 96, 56), (216, 168, 112))
PINK = ((184, 64, 112), (240, 120, 160), (248, 192, 208))
BLUE = ((48, 104, 184), (96, 168, 232), (176, 216, 248))

# pal 9: curry (A orange) + satay (B green)
P1 = stall_pal(ORANGE, GREEN, dict(b=(112, 64, 40), B=(168, 104, 56), Y=(248, 208, 72),
                                   m=(152, 40, 40), c=(248, 232, 184)))
# pal 10: hokkien mee (A yellow) + chicken rice (B green)
P2 = stall_pal(YELLOW, GREEN, dict(o=(200, 120, 48), c=(248, 224, 176), r=(216, 56, 48),
                                   p=(248, 144, 96), n=(56, 56, 72)))
# pal 11: soft-shell crab (A red) + kopi (B brown)
P3 = stall_pal(RED, BROWN, dict(u=(72, 136, 200), U=(152, 208, 240), o=(248, 160, 72),
                                c=(248, 232, 184), n=(56, 56, 72)))
# pal 12: berries (A pink) + ice kachang (B blue)
P4 = stall_pal(PINK, BLUE, dict(e=(88, 176, 80), E=(48, 120, 64), Y=(248, 216, 80),
                                r=(224, 64, 56), B=(168, 104, 56)))

LEGENDS = {6: FLOOR, 7: SHELL, 8: FURN, 9: P1, 10: P2, 11: P3, 12: P4}
PALETTES = {slot: [BLACK] + list(leg.values()) for slot, leg in LEGENDS.items()}


# ------------------------------------------------------------------ art
class Art:
    """A small RGB canvas; None = transparent."""

    def __init__(self, w=16, h=16, fill=None):
        self.w, self.h = w, h
        self.px = [[fill] * w for _ in range(h)]

    def copy(self):
        a = Art(self.w, self.h)
        a.px = [r[:] for r in self.px]
        return a

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def blit(self, other, ox=0, oy=0):
        """Paint `other` over this canvas (its transparent pixels leave ours alone)."""
        for y in range(other.h):
            for x in range(other.w):
                c = other.px[y][x]
                if c is not None:
                    self.put(ox + x, oy + y, c)
        return self

    def over(self, other, ox=0, oy=0):
        return self.copy().blit(other, ox, oy)

    def crop(self, x0, y0, w=16, h=16):
        a = Art(w, h)
        for y in range(h):
            for x in range(w):
                if 0 <= x0 + x < self.w and 0 <= y0 + y < self.h:
                    a.px[y][x] = self.px[y0 + y][x0 + x]
        return a

    def hflip(self):
        a = Art(self.w, self.h)
        a.px = [list(reversed(r)) for r in self.px]
        return a

    def recolour(self, mapping):
        a = self.copy()
        a.px = [[mapping.get(c, c) for c in r] for r in a.px]
        return a

    def empty(self):
        return all(c is None for r in self.px for c in r)


def art(legend, text, w=16, h=None, anchor="top", subs=None):
    """ASCII -> Art. '.' is transparent; short rows are right-padded; `subs` renames characters
    first (e.g. {'S': 'A'} to point a generic sign at a palette ramp). anchor='bottom' pads rows
    at the top so the drawing sits on the tile's bottom edge."""
    rows = [r for r in text.split("\n") if r.strip()]
    h = h or (max(16, len(rows)) if w == 16 else len(rows))
    if len(rows) > h:
        raise ValueError(f"too many rows ({len(rows)} > {h}):\n{text}")
    pad = [""] * (h - len(rows))
    rows = pad + rows if anchor == "bottom" else rows + pad
    a = Art(w, h)
    for y, row in enumerate(rows):
        if len(row) > w:
            raise ValueError(f"row {y} too long ({len(row)} > {w}): {row!r}")
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            if subs:
                ch = subs.get(ch, ch)
            if ch not in legend:
                raise ValueError(f"unknown colour {ch!r} in row {y}: {row!r}")
            a.px[y][x] = legend[ch]
    return a


def bands(legend, spec, w=16):
    """Horizontal bands: 'K W l*4 M' -> rows of solid colour."""
    a, y = Art(w, 0), 0
    for tok in spec.split():
        ch, _, n = tok.partition("*")
        for _ in range(int(n or 1)):
            a.px.append([legend[ch]] * w)
    a.h = len(a.px)
    return a


# ------------------------------------------------------------------ tiles / metatiles
def tile_of(a, qx, qy, transparent_ok):
    px = [[a.px[qy * 8 + y][qx * 8 + x] for x in range(8)] for y in range(8)]
    cols = {c for r in px for c in r}
    if cols == {None}:
        return None
    if None in cols and not transparent_ok:
        raise ValueError("bottom layer has transparent pixels")
    cols.discard(None)
    for slot, pal in PALETTES.items():
        if all(c in pal[1:] for c in cols):
            return slot, tuple(tuple(0 if c is None else pal.index(c, 1) for c in r) for r in px)
    raise ValueError(f"no single palette holds {sorted(cols)}")


def flips(tile):
    h = tuple(tuple(reversed(r)) for r in tile)
    v = tuple(reversed(tile))
    hv = tuple(reversed(h))
    return ((tile, 0, 0), (h, 1, 0), (v, 0, 1), (hv, 1, 1))


class TileBank:
    def __init__(self):
        blank = tuple(tuple(0 for _ in range(8)) for _ in range(8))
        self.tiles = [blank]
        self.lookup = {blank: (0, 0, 0)}

    def add(self, tile):
        for variant, hf, vf in flips(tile):
            if variant in self.lookup:
                idx, h0, v0 = self.lookup[variant]
                return idx, hf ^ h0, vf ^ v0
        idx = len(self.tiles)
        self.tiles.append(tile)
        self.lookup[tile] = (idx, 0, 0)
        return idx, 0, 0


class Metatile:
    def __init__(self, label, bottom, top=None, behaviour=0, layer=LAYER_COVERED, group=""):
        self.label, self.bottom, self.top = label, bottom, top
        self.behaviour, self.layer, self.group = behaviour, layer, group


def pack(metatile_list):
    bank = TileBank()
    data, attrs = [], []
    for m in metatile_list:
        entries = []
        for layer_art, transparent_ok in ((m.bottom, False), (m.top, True)):
            for qy in range(2):
                for qx in range(2):
                    if layer_art is None:
                        entries.append(0)
                        continue
                    try:
                        t = tile_of(layer_art, qx, qy, transparent_ok)
                    except ValueError as e:
                        raise ValueError(f"{m.label} quadrant ({qx},{qy}): {e}") from None
                    if t is None:
                        entries.append(0)
                        continue
                    slot, tile = t
                    idx, hf, vf = bank.add(tile)
                    entries.append((SECONDARY_TILE_BASE + idx) | (hf << 10) | (vf << 11) | (slot << 12))
        data.append(entries)
        attrs.append((m.behaviour & 0xFF) | (m.layer << 12))
    return bank, data, attrs


def write_pal(path, cols):
    cols = list(cols) + [BLACK] * (16 - len(cols))
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in cols:
            f.write(f"{c[0]} {c[1]} {c[2]}\n")


def write_tileset(bank, data, attrs):
    os.makedirs(os.path.join(TS_DIR, "palettes"), exist_ok=True)
    rows = (len(bank.tiles) + 15) // 16
    im = Image.new("P", (128, rows * 8), 0)
    flat = list(PALETTES[7]) + [BLACK] * (16 - len(PALETTES[7]))
    im.putpalette([v for c in flat for v in c])
    px = im.load()
    for i, tile in enumerate(bank.tiles):
        ox, oy = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = tile[y][x]
    im.save(os.path.join(TS_DIR, "tiles.png"), bits=4, optimize=False)
    with open(os.path.join(TS_DIR, "metatiles.bin"), "wb") as f:
        for m in data:
            f.write(struct.pack("<8H", *m))
    with open(os.path.join(TS_DIR, "metatile_attributes.bin"), "wb") as f:
        for a in attrs:
            f.write(struct.pack("<H", a))
    for slot in range(16):
        write_pal(os.path.join(TS_DIR, "palettes", f"{slot:02d}.pal"), PALETTES.get(slot, [BLACK]))


# ------------------------------------------------------------------ rendering (from packed data)
def render_metatile(bank, entries):
    """16x16 RGBA straight from the packed tiles, the way the game composites the two layers."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 255))
    px = im.load()
    for k, e in enumerate(entries):
        t, hf, vf, pal = (e & 0x3FF) - SECONDARY_TILE_BASE, (e >> 10) & 1, (e >> 11) & 1, e >> 12
        if t < 0:
            continue
        tile, q = bank.tiles[t], k & 3
        for y in range(8):
            for x in range(8):
                ci = tile[7 - y if vf else y][7 - x if hf else x]
                if ci == 0 and k >= 4:
                    continue
                px[(q & 1) * 8 + x, (q >> 1) * 8 + y] = PALETTES[pal][ci] + (255,)
    return im


def load_jasc(path):
    vals = open(path).read().split()[3:]
    return [tuple(int(v) for v in vals[i * 3:i * 3 + 3]) for i in range(len(vals) // 3)]


def sprite(png, pal, frame, w=16, h=32, hflip=False):
    """Object-event frame -> RGBA, index 0 transparent, colours floored to BGR555 like the GBA."""
    src = Image.open(os.path.join(ROOT, png)).crop((frame * w, 0, frame * w + w, h))
    pal = [tuple(v // 8 * 8 for v in c) for c in load_jasc(os.path.join(ROOT, pal))]
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    sp, op = src.load(), out.load()
    for y in range(h):
        for x in range(w):
            i = sp[x, y] & 15
            if i:
                op[x, y] = pal[i] + (255,)
    return out.transpose(Image.FLIP_LEFT_RIGHT) if hflip else out


def up(im, k=3):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)
