"""Level-crossing signage art (approved by the user 2026-11-18): advance warning sign and
boom barriers. Palette 4 of gTileset_General, whose three unused (magenta) slots 3-5 hold
yellow, dark yellow and black for this kit. '.' is transparent.
"""

PAL = 4
LEGEND = {".": 0, "W": 1, "w": 2, "Y": 3, "y": 4, "K": 5, "s": 6}
PAL4_EXTRA = {3: (248, 208, 48), 4: (200, 144, 24), 5: (40, 40, 48)}


def _check(rows, w):
    for r in rows:
        assert len(r) == w, (len(r), r)
    return rows


# yellow diamond with a black locomotive face, on a grey post: 16x32 (two metatiles)
WARNING_SIGN = _check([
    ".......KK.......",
    "......KYYK......",
    ".....KYYYYK.....",
    "....KYYKKYYK....",
    "...KYYKwwKYYK...",
    "..KYYKKKKKKYYK..",
    ".KYYYKwKKwKYYYK.",
    "KYYYYKKKKKKYYYyK",
    ".KyYYKKYYKKYYyK.",
    "..KyYYKKKKYYyK..",
    "...KyYYYYYYyK...",
    "....KyYYYYyK....",
    ".....KyYYyK.....",
    "......KyyK......",
    ".......KK.......",
    ".......KK.......",
] + [".......sK......."] * 11 + [
    "......wsKs......",
    "......KKKK......",
    "................",
    "................",
    "................",
], 16)

# 16x16 barrier cabinet with chevron foot; pivot hub on the right (x 11-12, rows 7-8)
HOUSING = _check([
    "................",
    "................",
    "...KKKKKKKKK....",
    "...KsssssssKK...",
    "...KwwwwwwwKK...",
    "...KKKKKKKKKK...",
    "...KKKKKKKKKKK..",
    "...KKKKKKKKWsK..",
    "...KKKKKKKKsKK..",
    "...KKKKKKKKKKK..",
    "...KKKKKKKKKK...",
    "..KYYKKYYKKYYK..",
    "..KYKKYYKKYYKK..",
    "..KKKKKKKKKKKK..",
    "...KKKKKKKKKK...",
    "................",
], 16)


def blank(w, h):
    return [["."] * w for _ in range(h)]


def paste(dst, rows, ox, oy):
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != "." and 0 <= oy + y < len(dst) and 0 <= ox + x < len(dst[0]):
                dst[oy + y][ox + x] = ch


def lowered_strip():
    """64x16, facing east: cabinet in the first 16 px, arm at waist height (rows 6-9) from the
    cabinet edge to the end of the fourth tile, 3 px diagonal stripes, closed tip."""
    c = blank(64, 16)
    paste(c, HOUSING, 0, 0)
    x0, x1 = 13, 63
    for x in range(x0, x1 + 1):
        stripe = ((x - 16) // 3) % 2 == 0
        c[6][x] = "K"
        c[7][x] = "Y" if stripe else "K"
        c[8][x] = "y" if stripe else "K"
        c[9][x] = "K"
    c[7][x1] = "K"; c[8][x1] = "K"
    return c


def raised_column():
    """16x48, facing east: arm standing up from the hub (x 11-14) through the two tiles above;
    the cabinet is drawn over the arm's foot."""
    c = blank(16, 48)
    top = 8
    for y in range(top, 32 + 8):
        stripe = ((y - top) // 3) % 2 == 0
        c[y][11] = "K"
        c[y][12] = "Y" if stripe else "K"
        c[y][13] = "y" if stripe else "K"
        c[y][14] = "K"
    for x in range(11, 15):
        c[top][x] = "K"
    paste(c, HOUSING, 0, 32)
    return c


def hflip(c):
    return [list(reversed(r)) for r in c]


def cell(c, tx, ty):
    """16x16 cell (tx, ty) of a canvas, as rows of characters."""
    return [r[tx * 16:tx * 16 + 16] for r in c[ty * 16:ty * 16 + 16]]
