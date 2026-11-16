"""
Mock platform scene (16x16 metatile grid, 15x10 tiles = 240x160) for the train storyboard.

    row 0      canopy underside
    row 1      station wall + name board
    row 2      wall base + far ballast        (the train's roof/body covers rows 1-3)
    row 3      TRACK ROW: ballast, sleepers, far rail (y+3..4), near rail (y+12..13)
    row 4      platform edge (white edge stones + yellow tactile strip) — boarding tile row
    rows 5-9   platform paving

Placeholder art only (not tileset-ready); colours snapped to BGR555.
"""
from common import *

TRACK_ROW = 3
EDGE_ROW = 4
TRAIN_Y = TRACK_ROW * 16 + 16 - 64     # piece bottoms on the track tile's bottom edge

# Train art is owned by the engine-side session: graphics/train/train.png (read-only here).
# 64x256 = four 64x64 pieces stacked: 0 rear car, 1 boarding car door shut, 2 loco,
# 3 boarding car door open. On screen: [0][1][2] left -> right.
TRAIN_PNG = G("train", "train.png")
TRAIN_W = 192
TRAIN_DOOR_X = 88                      # door x 88..103 from the train's left edge

THEMES_ = {
    "TOSA PORT": dict(wall=(72, 128, 152), wall_d=(48, 96, 120), wall_l=(112, 168, 184),
                      canopy=(56, 64, 88)),
    "TELOK TOWN": dict(wall=(168, 112, 80), wall_d=(128, 80, 64), wall_l=(200, 152, 112),
                       canopy=(72, 56, 64)),
}

C = lambda *c: snap(c)
INKC = C(40, 40, 56)
STONE = (C(232, 232, 216), C(200, 200, 184), C(160, 160, 152))
PAVE = (C(224, 216, 192), C(200, 192, 168), C(176, 168, 144))
YEL = (C(248, 216, 80), C(216, 168, 48))
GRAVEL = (C(128, 120, 112), C(104, 96, 96), C(152, 144, 128), C(80, 72, 72))
SLEEPER = (C(136, 96, 64), C(96, 64, 48), C(168, 128, 88))
RAIL = (C(216, 224, 232), C(136, 144, 160), C(72, 72, 88))


def scene(station="TOSA PORT", width=240, rows=10):
    th = {k: snap(v) for k, v in THEMES_[station].items()}
    h = rows * 16
    im = Image.new("RGBA", (width, h), (0, 0, 0, 255))
    px = im.load()

    def put(x, y, c):
        if 0 <= x < width and 0 <= y < h:
            px[x, y] = c + (255,)

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                put(x, y, c)

    # row 0: canopy underside with beams
    rect(0, 0, width - 1, 15, th["canopy"])
    for x in range(0, width, 32):
        rect(x, 0, x + 3, 13, snap(tuple(max(0, v - 24) for v in th["canopy"])))
        rect(x, 0, x, 13, snap(tuple(min(248, v + 24) for v in th["canopy"])))
    rect(0, 13, width - 1, 13, snap(tuple(min(248, v + 32) for v in th["canopy"])))
    rect(0, 14, width - 1, 15, INKC)
    # row 1: wall (tiled), name board, posters
    rect(0, 16, width - 1, 31, th["wall"])
    for y in (19, 23, 27):
        rect(0, y, width - 1, y, th["wall_d"])
    for y0 in (16, 20, 24, 28):
        off = 0 if (y0 // 4) % 2 else 4
        for x in range(off, width, 8):
            put(x, y0, th["wall_d"])
            put(x + 1, y0 + 1, th["wall_l"])
    rect(0, 16, width - 1, 16, th["wall_l"])
    # row 2: wall base, then far ballast
    rect(0, 32, width - 1, 39, th["wall_d"])
    rect(0, 32, width - 1, 32, th["wall"])
    rect(0, 40, width - 1, 40, INKC)
    _ballast(put, rect, width, 41, 47, sleepers=False)
    # row 3: track
    y0 = TRACK_ROW * 16
    _ballast(put, rect, width, y0, y0 + 15, sleepers=True)
    for ry in (y0 + 3, y0 + 12):
        rect(0, ry - 1, width - 1, ry - 1, RAIL[2])     # shadow above (far side)
        rect(0, ry, width - 1, ry, RAIL[0])
        rect(0, ry + 1, width - 1, ry + 1, RAIL[1])
        rect(0, ry + 2, width - 1, ry + 2, RAIL[2])
    # row 4: platform edge
    y0 = EDGE_ROW * 16
    rect(0, y0, width - 1, y0, INKC)
    rect(0, y0 + 1, width - 1, y0 + 1, STONE[0])
    rect(0, y0 + 2, width - 1, y0 + 4, STONE[1])
    for x in range(0, width, 16):
        rect(x, y0 + 1, x, y0 + 4, STONE[2])
    rect(0, y0 + 5, width - 1, y0 + 5, STONE[2])
    rect(0, y0 + 6, width - 1, y0 + 10, YEL[0])
    for x in range(1, width, 4):
        put(x, y0 + 7, YEL[1])
        put(x + 2, y0 + 9, YEL[1])
    rect(0, y0 + 11, width - 1, y0 + 11, YEL[1])
    _paving(put, rect, width, y0 + 12, h - 1)
    # name board (centred), drawn last on row 1
    bw = text_width(station, "small") + 14
    bx = (width - bw) // 2
    # hangs from the canopy (row 0) so it stays visible above a parked train
    for hx in (bx + 4, bx + bw - 5):
        rect(hx, 0, hx, 1, INKC)
    rect(bx, 2, bx + bw - 1, 15, INKC)
    rect(bx + 1, 3, bx + bw - 2, 14, (248, 248, 248))
    rect(bx + 1, 14, bx + bw - 2, 14, STONE[1])
    rect(bx + 1, 3, bx + 3, 13, snap((152, 88, 184)))           # Orchid rail-brand tab
    board = Image.new("P", (bw, 16), 0)
    board.putpalette([0, 0, 0] + list(INKC) + [0] * 6 + list(STONE[1]) + [0] * 750)
    from kit import Canvas as _Cv
    draw_text(_Cv(board), 0, 0, station, 1, 3, font="small")
    bp = board.load()
    for y in range(16):
        for x in range(bw):
            if bp[x, y] == 1:
                put(bx + 7 + x, -1 + y, INKC)
    # posters
    for x in (24, width - 40):
        rect(x, 19, x + 15, 29, INKC)
        rect(x + 1, 20, x + 14, 28, snap((232, 208, 240)))
        rect(x + 3, 22, x + 12, 24, snap((152, 88, 184)))
        rect(x + 3, 26, x + 9, 26, snap((112, 112, 136)))
    return im


def _ballast(put, rect, width, y0, y1, sleepers):
    rect(0, y0, width - 1, y1, GRAVEL[0])
    for y in range(y0, y1 + 1):
        for x in range(width):
            v = (x * 7 + y * 13 + (x * y) % 5) % 11
            if v == 0:
                put(x, y, GRAVEL[2])
            elif v in (3, 7):
                put(x, y, GRAVEL[1])
    if sleepers:
        for x in range(2, width, 8):
            rect(x, y0 + 1, x + 4, y1 - 1, SLEEPER[0])
            rect(x, y0 + 1, x + 4, y0 + 1, SLEEPER[2])
            rect(x + 4, y0 + 1, x + 4, y1 - 1, SLEEPER[1])
            rect(x, y1 - 1, x + 4, y1 - 1, SLEEPER[1])


def _paving(put, rect, width, y0, y1):
    rect(0, y0, width - 1, y1, PAVE[0])
    for y in range(y0, y1 + 1):
        row = (y - y0) // 16
        if (y - y0) % 16 == 15:
            rect(0, y, width - 1, y, PAVE[2])
        elif (y - y0) % 16 == 0:
            rect(0, y, width - 1, y, (248, 248, 232))
        for x in range(((row % 2) * 8), width, 16):
            if (y - y0) % 16 != 15:
                put(x + 15 if x + 15 < width else x, y, PAVE[1])


def bench(out, x, y):
    """32x16 platform bench (placeholder)."""
    im = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
    p = im.load()

    def r(x0, y0, x1, y1, c):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                p[xx, yy] = c + (255,)
    r(1, 3, 30, 9, INKC)
    r(2, 4, 29, 5, SLEEPER[2])
    r(2, 6, 29, 8, SLEEPER[0])
    r(3, 10, 5, 14, INKC)
    r(26, 10, 28, 14, INKC)
    out.alpha_composite(im, (x, y))


_TRAIN = {}


def train_rgba(door_open=False):
    """192x64 RGBA train from graphics/train/train.png, or a grey placeholder if it is missing."""
    key = bool(door_open)
    if key in _TRAIN:
        return _TRAIN[key]
    out = Image.new("RGBA", (TRAIN_W, 64), (0, 0, 0, 0))
    if os.path.exists(TRAIN_PNG):
        src = Image.open(TRAIN_PNG)
        order = [0, 3 if door_open else 1, 2]
        for i, piece in enumerate(order):
            out.alpha_composite(KX.sheet_rgba(src.crop((0, piece * 64, 64, piece * 64 + 64))), (i * 64, 0))
    else:
        p = out.load()
        for x in range(TRAIN_W):
            for y in range(16, 60):
                edge = x % 64 in (0, 63) or y in (16, 59)
                p[x, y] = INKC + (255,) if edge else (200, 200, 208, 255)
        for x in range(TRAIN_DOOR_X, TRAIN_DOOR_X + 16):
            for y in range(28, 59):
                p[x, y] = (32, 40, 64, 255) if door_open else (128, 136, 152, 255)
    _TRAIN[key] = out
    return out
