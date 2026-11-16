"""
Orchid UI kit — shared palette roles + pixel primitives.

Design language: "Gen 5 layout, Gen 3 pixels".
  * Gen 5 (Black/White): rounded pill rows, round pocket "buttons", a big
    circular dais, flat two-tone panels, soft patterned backdrop.
  * Gen 3 (R/S/E): 1px dark ink outline, light top-left bevel, dark
    bottom-right shade, 3-step ramps, chunky corners (no anti-aliasing),
    colours snapped to BGR555 (multiples of 8).

Every 16-colour UI palette built from this kit uses the same ROLE layout,
so any tile drawn with the kit can be re-themed by swapping palettes only.

    idx  role            use
    0    TRANSPARENT     backdrop / colour key
    1    INK             outlines, dark text
    2    INK_SOFT        text shadow, inner outline on dark accents
    3    WHITE           panel face highlight, light text
    4    PANEL           panel face
    5    PANEL_SHADE     panel bottom-right bevel, row separators
    6    PANEL_DARK      recessed troughs (scroll track, icon wells)
    7    ACCENT_DARK     theme colour, darkest (frame bands, header)
    8    ACCENT          theme colour
    9    ACCENT_LIGHT    theme colour, light (backdrop pattern)
    10   ACCENT_PALE     theme colour, palest (backdrop base)
    11   SELECT_DARK     selection outline (gold)
    12   SELECT         selection fill
    13   SELECT_LIGHT    selection highlight
    14   SPARE_A         free per-screen colour
    15   SPARE_B         free per-screen colour
"""
from PIL import Image

TRANSPARENT, INK, INK_SOFT, WHITE, PANEL, PANEL_SHADE, PANEL_DARK, \
    ACCENT_DARK, ACCENT, ACCENT_LIGHT, ACCENT_PALE, \
    SELECT_DARK, SELECT, SELECT_LIGHT, SPARE_A, SPARE_B = range(16)


def snap(c):
    """Round an RGB triple to what the GBA can show (BGR555)."""
    return tuple(min(248, (v + 4) // 8 * 8) for v in c)


# Neutral roles shared by every theme.
_NEUTRAL = {
    TRANSPARENT: (0, 0, 0),           # never shown (overridden per sheet)
    INK: (40, 40, 64),
    INK_SOFT: (112, 112, 136),
    WHITE: (248, 248, 248),
    PANEL: (232, 232, 224),
    PANEL_SHADE: (192, 192, 184),
    PANEL_DARK: (144, 144, 152),
    SELECT_DARK: (216, 128, 32),
    SELECT: (248, 208, 88),
    SELECT_LIGHT: (248, 240, 168),
    SPARE_A: (0, 0, 0),
    SPARE_B: (0, 0, 0),
}

# Theme accents (ACCENT_DARK, ACCENT, ACCENT_LIGHT, ACCENT_PALE).
THEMES = {
    # Default Orchid theme — used by shared windows/menus.
    "orchid": [(96, 48, 128), (152, 88, 184), (200, 152, 224), (232, 208, 240)],
    # Player-gender themes (bag, trainer card...), BW style blue / red.
    "male": [(32, 80, 136), (64, 128, 200), (136, 184, 232), (208, 232, 248)],
    "female": [(152, 40, 72), (216, 88, 112), (240, 152, 168), (248, 216, 224)],
    # Leafy secondary theme for nature-ish screens.
    "leaf": [(40, 104, 64), (72, 160, 88), (144, 208, 136), (216, 240, 200)],
}


def palette(theme="orchid", spare_a=None, spare_b=None, key=(0, 0, 0)):
    roles = dict(_NEUTRAL)
    roles[TRANSPARENT] = key
    for i, c in zip((ACCENT_DARK, ACCENT, ACCENT_LIGHT, ACCENT_PALE), THEMES[theme]):
        roles[i] = c
    if spare_a:
        roles[SPARE_A] = spare_a
    if spare_b:
        roles[SPARE_B] = spare_b
    return [snap(roles[i]) for i in range(16)]


def new_sheet(w, h, theme="orchid", **kw):
    im = Image.new("P", (w, h), 0)
    flat = []
    for c in palette(theme, **kw):
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def write_jasc(path, pal):
    with open(path, "w", newline="\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(pal))
        for c in pal:
            f.write("%d %d %d\n" % c)


# ---------------------------------------------------------------- primitives
class Canvas:
    """Thin wrapper over a 'P' image with pixel helpers (indices only)."""

    def __init__(self, im):
        self.im = im
        self.px = im.load()
        self.w, self.h = im.size

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h and c is not None:
            self.px[x, y] = c

    def get(self, x, y):
        return self.px[x, y] if 0 <= x < self.w and 0 <= y < self.h else 0

    def rect(self, x0, y0, x1, y1, c):  # inclusive
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)


def _round_inset(r, y, h):
    """Columns to inset at row y for a rounded box of height h, corner radius r."""
    table = {
        0: [0],
        1: [1, 0],
        2: [2, 1, 0],
        3: [3, 1, 1, 0],
        4: [4, 2, 1, 1, 0],
    }[r]
    if y < len(table) - 1:
        return table[y]
    if h - 1 - y < len(table) - 1:
        return table[h - 1 - y]
    return 0


def rounded_box(cv, x0, y0, w, h, r, face, outline=INK, light=WHITE, shade=PANEL_SHADE,
                bevel=True):
    """Gen-3 style rounded box: ink outline, top-left light bevel, bottom-right shade."""
    for y in range(h):
        ins = _round_inset(r, y, h)
        xa, xb = x0 + ins, x0 + w - 1 - ins
        cv.hline(xa, xb, y0 + y, face)
        cv.set(xa, y0 + y, outline)
        cv.set(xb, y0 + y, outline)
    # top / bottom edges
    ins0 = _round_inset(r, 0, h)
    cv.hline(x0 + ins0, x0 + w - 1 - ins0, y0, outline)
    cv.hline(x0 + ins0, x0 + w - 1 - ins0, y0 + h - 1, outline)
    # diagonal corner pixels so the outline is closed
    for y in range(1, h - 1):
        ins, insp = _round_inset(r, y, h), _round_inset(r, y - 1, h)
        if insp > ins + 1:
            for x in range(ins + 1, insp):
                cv.set(x0 + x, y0 + y - 1 if y <= h // 2 else y0 + y, outline)
                cv.set(x0 + w - 1 - x, y0 + y - 1 if y <= h // 2 else y0 + y, outline)
    for y in range(h - 2, 0, -1):
        ins, insn = _round_inset(r, y, h), _round_inset(r, y + 1, h)
        if insn > ins + 1:
            for x in range(ins + 1, insn):
                cv.set(x0 + x, y0 + y + 1, outline)
                cv.set(x0 + w - 1 - x, y0 + y + 1, outline)
    if not bevel:
        return
    # bevel: light one pixel inside top + left, shade inside bottom + right
    for y in range(1, h - 1):
        ins = _round_inset(r, y, h)
        if y == 1:
            cv.hline(x0 + ins + 1, x0 + w - 2 - ins, y0 + y, light)
        elif y == h - 2:
            cv.hline(x0 + ins + 1, x0 + w - 2 - ins, y0 + y, shade)
        else:
            cv.set(x0 + ins + 1, y0 + y, light)
            cv.set(x0 + w - 2 - ins, y0 + y, shade)


def disc(cv, cx, cy, r, face, outline=INK, light=None, shade=None):
    """Filled pixel circle centred on (cx, cy) (half-pixel centres allowed)."""
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            d2 = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
            if d2 <= r * r:
                cv.set(x, y, face)
    if light is not None or shade is not None:
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                d2 = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
                if (r - 1.6) ** 2 < d2 <= (r - 0.5) ** 2:
                    up = (x + 0.5 - cx) + (y + 0.5 - cy) < 0
                    if up and light is not None:
                        cv.set(x, y, light)
                    elif not up and shade is not None:
                        cv.set(x, y, shade)
    if outline is not None:
        ring(cv, cx, cy, r, outline)


def ring(cv, cx, cy, r, c, thick=1.0):
    """1px (or thicker) circle outline, 8-connected, no doubled corners."""
    pts = set()
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5
            if r - thick < d <= r:
                pts.add((x, y))
    for x, y in pts:
        cv.set(x, y, c)


def checker_dither(cv, x0, y0, x1, y1, c, phase=0):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x + y + phase) % 2 == 0:
                cv.set(x, y, c)


# ---------------------------------------------------------------- tiling
def to_tiles(im, dedupe=True, flips=True, base=None):
    """
    Cut a 'P' image into 8x8 tiles. Returns (tiles, tilemap) where tilemap is a
    list of (tile_index, hflip, vflip) per cell, row-major. Tile 0 is blank if
    `base` is None. Flip-dedupe follows GBA tilemap semantics.
    """
    W, H = im.size
    px = im.load()
    tiles = [] if base is None else list(base)
    lookup = {}
    if base is None:
        blank = tuple([0] * 64)
        tiles.append(blank)
        lookup[blank] = (0, 0, 0)
    for i, t in enumerate(tiles):
        lookup.setdefault(t, (i, 0, 0))
    tm = []
    for ty in range(H // 8):
        for tx in range(W // 8):
            t = tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            if dedupe and t in lookup:
                tm.append(lookup[t])
                continue
            if dedupe and flips:
                found = None
                for hf, vf in ((1, 0), (0, 1), (1, 1)):
                    f = tuple(t[(7 - y if vf else y) * 8 + (7 - x if hf else x)]
                              for y in range(8) for x in range(8))
                    if f in lookup and lookup[f][1] == 0 and lookup[f][2] == 0:
                        found = (lookup[f][0], hf, vf)
                        break
                if found:
                    tm.append(found)
                    continue
            idx = len(tiles)
            tiles.append(t)
            lookup[t] = (idx, 0, 0)
            tm.append((idx, 0, 0))
    return tiles, tm


def tiles_to_image(tiles, pal_im, per_row=16):
    rows = (len(tiles) + per_row - 1) // per_row
    im = Image.new("P", (per_row * 8, rows * 8), 0)
    im.putpalette(pal_im.getpalette())
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % per_row) * 8, (i // per_row) * 8
        for j, c in enumerate(t):
            px[ox + j % 8, oy + j // 8] = c
    return im


def write_tilemap(path, tm, pal_num=0, width_cells=None, pad_to=None, tile_offset=0):
    """Write a GBA text-mode tilemap (u16 LE per cell)."""
    import struct
    out = bytearray()
    for item in tm:
        if item is None:
            out += struct.pack("<H", 0)
            continue
        idx, hf, vf = item[:3]
        pn = item[3] if len(item) > 3 else pal_num
        out += struct.pack("<H", ((idx + tile_offset) & 0x3FF) | (hf << 10) | (vf << 11) | (pn << 12))
    if pad_to:
        out += b"\0" * (pad_to - len(out))
    with open(path, "wb") as f:
        f.write(out)


# ---------------------------------------------------------------- small arrow
# 6x9 Gen 3 chevron (points left; flip for right). O = outline, F = fill.
SMALL_ARROW = [
    "....OO",
    "...OFO",
    "..OFFO",
    ".OFFO.",
    "OFFO..",
    ".OFFO.",
    "..OFFO",
    "...OFO",
    "....OO",
]
# Gen 3's own arrow colours (graphics/interface/red.pal): fill, outline.
ARROW_RED = ((248, 80, 0), (128, 32, 0))


def stamp(cv, x, y, rows, cmap, hflip=False):
    for r, row in enumerate(rows):
        if hflip:
            row = row[::-1]
        for c, ch in enumerate(row):
            if ch in cmap:
                cv.set(x + c, y + r, cmap[ch])
