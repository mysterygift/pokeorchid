"""Shared plumbing for the Cold Storage tileset generators: ASCII art -> tiles, metatile packing,
file writers, previews. Same pattern as dev_scripts/hawker_tileset/kit.py, but the palette set and
tile base are passed in, so one module serves both the new interior tileset (export_tileset.py)
and the tiles appended to gTileset_Slateport (export_exterior.py)."""
import os
import struct

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")

SECONDARY_TILE_BASE = 512
SECONDARY_METATILE_BASE = 0x200
LAYER_NORMAL, LAYER_COVERED, LAYER_SPLIT = 0, 1, 2
BLACK = (0, 0, 0)


def snap(c):
    """Round to BGR555 (multiples of 8, max 248)."""
    return tuple(min(248, max(0, (v + 4) // 8 * 8)) for v in c)


def legend(**cols):
    return {k: snap(v) for k, v in cols.items()}


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
        return self

    def blit(self, other, ox=0, oy=0):
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

    def cell(self, cx, cy):
        """The 16x16 metatile at column cx, row cy of a multi-tile drawing."""
        return self.crop(cx * 16, cy * 16)

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


def art(leg, text, w=16, h=None, anchor="top", subs=None):
    """ASCII -> Art. '.' and ' ' are transparent; short rows are right-padded; `subs` renames
    characters first. anchor='bottom' pads rows at the top."""
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
            if ch not in leg:
                raise ValueError(f"unknown colour {ch!r} in row {y}: {row!r}")
            a.px[y][x] = leg[ch]
    return a


def tiled(leg, rows8, w, h):
    """Repeat a small ASCII pattern (list of equal-length rows) over a w x h canvas."""
    a = Art(w, h)
    ph, pw = len(rows8), len(rows8[0])
    for y in range(h):
        for x in range(w):
            ch = rows8[y % ph][x % pw]
            if ch not in ". ":
                a.px[y][x] = leg[ch]
    return a


# ------------------------------------------------------------------ tiles / metatiles
def flips(tile):
    h = tuple(tuple(reversed(r)) for r in tile)
    v = tuple(reversed(tile))
    hv = tuple(reversed(h))
    return ((tile, 0, 0), (h, 1, 0), (v, 0, 1), (hv, 1, 1))


BLANK = tuple(tuple(0 for _ in range(8)) for _ in range(8))


class TileBank:
    """Deduplicating (flip-aware) tile store. `slots` optionally lists the tile indices new
    tiles may occupy (for patching an existing tileset); otherwise tiles are appended from 1."""

    def __init__(self, slots=None, blank_index=0):
        self.tiles = {blank_index: BLANK}
        self.lookup = {BLANK: (blank_index, 0, 0)}
        self.slots = list(slots) if slots is not None else None
        self.next = 1

    def add(self, tile):
        for variant, hf, vf in flips(tile):
            if variant in self.lookup:
                idx, h0, v0 = self.lookup[variant]
                return idx, hf ^ h0, vf ^ v0
        if self.slots is not None:
            if not self.slots:
                raise ValueError("out of free tile slots")
            idx = self.slots.pop(0)
        else:
            idx = self.next
            self.next += 1
        self.tiles[idx] = tile
        self.lookup[tile] = (idx, 0, 0)
        return idx, 0, 0

    @property
    def new_count(self):
        return len(self.tiles) - 1


class Metatile:
    def __init__(self, label, bottom, top=None, behaviour=0, layer=LAYER_COVERED, group="",
                 walk=False):
        self.label, self.bottom, self.top = label, bottom, top
        self.behaviour, self.layer, self.group, self.walk = behaviour, layer, group, walk


class Packer:
    def __init__(self, legends, bank=None):
        """legends: {palette slot: {char: rgb}}; slot colour order = dict order, index 0 unused."""
        self.legends = legends
        self.palettes = {slot: [BLACK] + list(leg.values()) for slot, leg in legends.items()}
        for slot, pal in self.palettes.items():
            assert len(pal) <= 16, f"palette {slot} has {len(pal) - 1} colours"
        self.bank = bank or TileBank()

    def tile_of(self, a, qx, qy, transparent_ok):
        px = [[a.px[qy * 8 + y][qx * 8 + x] for x in range(8)] for y in range(8)]
        cols = {c for r in px for c in r}
        if cols == {None}:
            return None
        if None in cols and not transparent_ok:
            raise ValueError("bottom layer has transparent pixels")
        cols.discard(None)
        for slot, pal in self.palettes.items():
            if all(c in pal[1:] for c in cols):
                return slot, tuple(tuple(0 if c is None else pal.index(c, 1) for c in r) for r in px)
        raise ValueError(f"no single palette holds {sorted(cols)}")

    def pack(self, metatile_list):
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
                            t = self.tile_of(layer_art, qx, qy, transparent_ok)
                        except ValueError as e:
                            raise ValueError(f"{m.label} quadrant ({qx},{qy}): {e}") from None
                        if t is None:
                            entries.append(0)
                            continue
                        slot, tile = t
                        idx, hf, vf = self.bank.add(tile)
                        entries.append((SECONDARY_TILE_BASE + idx) | (hf << 10) | (vf << 11) | (slot << 12))
            data.append(entries)
            attrs.append((m.behaviour & 0xFF) | (m.layer << 12))
        return data, attrs

    # -------------------------------------------------------------- rendering (from packed data)
    def render_metatile(self, entries, layers=(0, 1)):
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        px = im.load()
        for k, e in enumerate(entries):
            if (k >> 2) not in layers:
                continue
            t, hf, vf, pal = (e & 0x3FF) - SECONDARY_TILE_BASE, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            if t not in self.bank.tiles or pal not in self.palettes:
                continue
            tile, q = self.bank.tiles[t], k & 3
            for y in range(8):
                for x in range(8):
                    ci = tile[7 - y if vf else y][7 - x if hf else x]
                    if ci == 0:
                        continue
                    px[(q & 1) * 8 + x, (q >> 1) * 8 + y] = self.palettes[pal][ci] + (255,)
        return im


def write_pal(path, cols):
    cols = list(cols) + [BLACK] * (16 - len(cols))
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in cols:
            f.write(f"{c[0]} {c[1]} {c[2]}\n")


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


def behaviours():
    import re
    text = open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read()
    names = re.findall(r"^\s*(MB_\w+)\s*,", text[text.index("enum"):], re.M)
    return {n: i for i, n in enumerate(names)}
