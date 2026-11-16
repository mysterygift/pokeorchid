"""Reusable Orchid backdrop + panel pieces (screen-agnostic)."""
from kit import *


# 16x16 repeat: little four-petal orchid "dots" on a pale field, offset grid.
_PETAL = [
    "..x..",
    ".xox.",
    "xo.ox",
    ".xox.",
    "..x..",
]


def backdrop(cv, x0, y0, x1, y1, base=ACCENT_PALE, motif=ACCENT_LIGHT, centre=WHITE):
    cv.rect(x0, y0, x1, y1, base)
    for gy in range(y0 - 16, y1 + 16, 16):
        for gx in range(x0 - 16, x1 + 16, 16):
            for oy, ox in ((0, 0), (8, 8)):
                for r, row in enumerate(_PETAL):
                    for c, ch in enumerate(row):
                        x, y = gx + ox + c + 1, gy + oy + r + 1
                        if x0 <= x <= x1 and y0 <= y <= y1:
                            if ch == "x":
                                cv.set(x, y, motif)
                            elif ch == "o" and (ox == 0):
                                cv.set(x, y, motif)


def band(cv, x0, y0, x1, y1, face=ACCENT, light=ACCENT_LIGHT, dark=ACCENT_DARK):
    """Flat accent band with a 1px light top edge and dark bottom edge (header / footer bars)."""
    cv.rect(x0, y0, x1, y1, face)
    cv.hline(x0, x1, y0, light)
    cv.hline(x0, x1, y1, dark)


def pill(cv, x, y, w, h=14, face=PANEL, outline=INK, light=WHITE, shade=PANEL_SHADE, r=4):
    rounded_box(cv, x, y, w, h, r, face, outline, light, shade)


# ---------------------------------------------------------------- scrolling grid (BW style)
# Lives on its own BG layer (BG3) under the screen art and scrolls diagonally.
# 16x16 repeat = 2x2 tiles: 1px major line every 16px, faint minor line at 8px.
GRID_PAL = [(0, 0, 0), (24, 24, 32), (40, 40, 56), (88, 96, 112)]   # -, base, minor, major
GRID_BASE, GRID_MINOR, GRID_MAJOR = 1, 2, 3
GRID_CELL = 16


def grid_index(x, y):
    gx, gy = x % GRID_CELL, y % GRID_CELL
    if gx == 0 or gy == 0:
        return GRID_MAJOR
    if gx == GRID_CELL // 2 or gy == GRID_CELL // 2:
        return GRID_MINOR
    return GRID_BASE


def grid_tile_image():
    """16x16 indexed image (2x2 tiles) for BG3; palette = GRID_PAL padded to 16."""
    im = Image.new("P", (GRID_CELL, GRID_CELL), 0)
    flat = [c for rgb in GRID_PAL for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for y in range(GRID_CELL):
        for x in range(GRID_CELL):
            px[x, y] = grid_index(x, y)
    return im
