#!/usr/bin/env python3
"""
gTileset_UrbanInterior: the train-station platform from dev_scripts/train_ui/journey_scene.py
turned into a real secondary tileset (pairs with the interior primary gTileset_Building).

    python export_tileset.py                      # tileset files only (safe to re-run)
    python export_tileset.py --paint-test-layout  # also repaint LAYOUT_TRAIN_TEST_STATION
    python export_tileset.py --previews           # also write previews to ./out

Writes data/tilesets/secondary/urban_interior/{tiles.png, metatiles.bin,
metatile_attributes.bin, palettes/00..15.pal}. Deterministic: same input -> same bytes.
NOTE: re-running overwrites any Porymap edits to this tileset.

Row structure (map rows of the test station; the train sprite, OBJ priority 2, covers rows 2-4):

    row 0   ceiling (roof underside)                 COVERED, top layer empty
    row 1   canopy with beams + fascia               COVERED, top layer empty
    row 2   station wall (+ poster, pillar)          COVERED, top layer empty   <- train body
    row 3   wall base + far ballast                  COVERED, top layer empty   <- train body
    row 4   TRACK: ballast, sleepers, two rails      COVERED, top layer empty   <- train body
    row 5   platform edge stones + tactile strip     NORMAL  (boarding row)
    row 6+  paving, offset bricks: A on even rows, B on odd rows; exit mat (south arrow warp)

Nothing in this tileset uses the top layer, so BG1 can never draw over the train.

Two wall themes share every tile and differ only by palette: "Tosa" teal tiles (pal 6) and
"Telok" brick (pal 9). No lettering / station-name tiles (by request: too much space).

Palettes (secondary slots 6-12; the rest are written as unused black files):
    6  shell, Tosa teal     ceiling, canopy, wall, poster, pillar, void
    7  track                gravel, sleepers, rails (also the far ballast under the wall base)
    8  platform             edge stones, tactile strip, paving, exit mat
    9  shell, Telok brick   same index layout as 6
    10-12 unused
"""
import os
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TS_DIR = os.path.join(ROOT, "data", "tilesets", "secondary", "urban_interior")
LAYOUT_DIR = os.path.join(ROOT, "data", "layouts", "TrainTestStation")
OUT = os.path.join(HERE, "out")

SECONDARY_TILE_BASE = 512
SECONDARY_METATILE_BASE = 0x200

# metatile behaviours (include/constants/metatile_behaviors.h)
MB_NORMAL = 0x00
MB_SOUTH_ARROW_WARP = 0x65
# layer types (include/global.fieldmap.h)
LAYER_NORMAL, LAYER_COVERED, LAYER_SPLIT = 0, 1, 2


def snap(c):
    """Round to BGR555 (multiples of 8, max 248)."""
    return tuple(min(248, max(0, (v + 4) // 8 * 8)) for v in c)


def shade(c, d):
    return snap(tuple(v + d for v in c))


# ------------------------------------------------------------------ colours (journey_scene.py)
BLACK = (0, 0, 0)
INK = snap((40, 40, 56))
STONE = [snap(c) for c in ((232, 232, 216), (200, 200, 184), (160, 160, 152))]
PAVE = [snap(c) for c in ((224, 216, 192), (200, 192, 168), (176, 168, 144))]
PAVE_HI = snap((248, 248, 232))
YEL = [snap(c) for c in ((248, 216, 80), (216, 168, 48))]
GRAVEL = [snap(c) for c in ((128, 120, 112), (104, 96, 96), (152, 144, 128), (80, 72, 72))]
SLEEPER = [snap(c) for c in ((136, 96, 64), (96, 64, 48), (168, 128, 88))]
RAIL = [snap(c) for c in ((216, 224, 232), (136, 144, 160), (72, 72, 88))]
POSTER = [snap(c) for c in ((232, 208, 240), (152, 88, 184), (112, 112, 136))]
MAT = [snap(c) for c in ((64, 48, 88), (104, 72, 136), (184, 152, 208))]

THEMES = {
    "tosa": dict(wall=(72, 128, 152), wall_d=(48, 96, 120), wall_l=(112, 168, 184),
                 canopy=(56, 64, 88)),
    "telok": dict(wall=(168, 112, 80), wall_d=(128, 80, 64), wall_l=(200, 152, 112),
                  canopy=(72, 56, 64)),
}


def theme_colours(name):
    t = {k: snap(v) for k, v in THEMES[name].items()}
    c = t["canopy"]
    t.update(canopy_dd=shade(c, -40), canopy_d=shade(c, -24), canopy_l=shade(c, 24),
             canopy_ll=shade(c, 32))
    return t


def shell_palette(name):
    t = theme_colours(name)
    return [BLACK, BLACK, INK, t["canopy_dd"], t["canopy_d"], t["canopy"], t["canopy_l"],
            t["canopy_ll"], t["wall_d"], t["wall"], t["wall_l"]] + POSTER


PAL_TRACK = [BLACK, INK] + GRAVEL + SLEEPER + RAIL
PAL_PLATFORM = [BLACK, INK] + STONE + YEL + PAVE + [PAVE_HI] + MAT

PALETTES = {6: shell_palette("tosa"), 7: PAL_TRACK, 8: PAL_PLATFORM, 9: shell_palette("telok")}
# Which palettes a theme may pick from, in order of preference (track/platform are shared).
THEME_PALS = {"tosa": (6, 7, 8), "telok": (9, 7, 8)}


# ------------------------------------------------------------------ 16x16 drawing
class Block:
    def __init__(self):
        self.px = [[None] * 16 for _ in range(16)]

    def put(self, x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            self.px[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)


def gravel(b, y0, y1, yoff):
    """Ballast noise, periodic in 16 px so it tiles horizontally."""
    b.rect(0, y0, 15, y1, GRAVEL[0])
    for y in range(y0, y1 + 1):
        gy = y + yoff
        for x in range(16):
            v = (x * 7 + gy * 13 + (x * gy) % 5) % 11
            if v == 0:
                b.put(x, y, GRAVEL[2])
            elif v in (3, 7):
                b.put(x, y, GRAVEL[1])


def pave_px(x, py):
    """Paving colour at x, paving-row y (py = 0 at the first brick row's top line)."""
    row, ly = py // 16, py % 16
    c = PAVE[0]
    if ly == 15:
        return PAVE[2]
    if ly == 0:
        c = PAVE_HI
    if x % 16 == (7 if row % 2 else 15):
        c = PAVE[1]
    return c


def paving(b, y0, y1, py0):
    for y in range(y0, y1 + 1):
        for x in range(16):
            b.put(x, y, pave_px(x, py0 + y - y0))


def draw_ceiling(t, beam):
    b = Block()
    b.rect(0, 0, 15, 15, t["canopy_dd"])
    for y in (1, 5, 9, 13):                      # corrugated roof ridges
        b.rect(0, y, 15, y, t["canopy_d"])
    if beam:
        b.rect(0, 0, 3, 15, INK)
        b.rect(0, 0, 0, 15, t["canopy_d"])
    return b


def draw_canopy(t, beam):
    b = Block()
    b.rect(0, 0, 15, 15, t["canopy"])
    b.rect(0, 0, 15, 0, t["canopy_d"])           # meets the darker ceiling
    if beam:
        b.rect(0, 0, 3, 13, t["canopy_d"])
        b.rect(0, 0, 0, 13, t["canopy_l"])
    b.rect(0, 13, 15, 13, t["canopy_ll"])        # fascia lip
    b.rect(0, 14, 15, 15, INK)
    return b


def draw_wall(t):
    b = Block()
    b.rect(0, 0, 15, 15, t["wall"])
    for y in (3, 7, 11):
        b.rect(0, y, 15, y, t["wall_d"])
    for y0 in (0, 4, 8, 12):
        off = 0 if (y0 // 4) % 2 else 4
        for x in range(off, 16, 8):
            b.put(x, y0, t["wall_d"])
            b.put(x + 1, y0 + 1, t["wall_l"])
    b.rect(0, 0, 15, 0, t["wall_l"])
    return b


def draw_poster(t):
    b = draw_wall(t)
    b.rect(1, 3, 14, 13, INK)
    b.rect(2, 4, 13, 12, POSTER[0])
    b.rect(4, 6, 11, 8, POSTER[1])
    b.rect(4, 10, 9, 10, POSTER[2])
    return b


def draw_wall_base(t):
    b = Block()
    b.rect(0, 0, 15, 7, t["wall_d"])
    b.rect(0, 0, 15, 0, t["wall"])
    b.rect(0, 8, 15, 8, INK)
    gravel(b, 9, 15, 32)
    return b


def column(b, t, y0, y1):
    b.rect(5, y0, 10, y1, t["canopy_l"])
    b.rect(5, y0, 5, y1, INK)
    b.rect(10, y0, 10, y1, INK)
    b.rect(6, y0, 6, y1, t["canopy_ll"])
    b.rect(9, y0, 9, y1, t["canopy"])


def draw_pillar_canopy(t):
    b = draw_canopy(t, beam=False)
    column(b, t, 0, 13)
    b.rect(3, 10, 12, 12, t["canopy_d"])         # capital under the fascia
    b.rect(3, 10, 12, 10, t["canopy_l"])
    b.rect(3, 13, 12, 13, t["canopy_ll"])
    return b


def draw_pillar_wall(t):
    b = draw_wall(t)
    column(b, t, 0, 15)
    return b


def draw_pillar_base(t):
    b = draw_wall_base(t)
    column(b, t, 0, 7)
    b.rect(4, 5, 11, 7, t["canopy_d"])           # plinth
    b.rect(4, 5, 11, 5, t["canopy_l"])
    return b


def draw_track():
    b = Block()
    gravel(b, 0, 15, 48)
    for x in range(2, 16, 8):
        b.rect(x, 1, x + 4, 14, SLEEPER[0])
        b.rect(x, 1, x + 4, 1, SLEEPER[2])
        b.rect(x + 4, 1, x + 4, 14, SLEEPER[1])
        b.rect(x, 14, x + 4, 14, SLEEPER[1])
    for ry in (3, 12):
        b.rect(0, ry - 1, 15, ry - 1, RAIL[2])
        b.rect(0, ry, 15, ry, RAIL[0])
        b.rect(0, ry + 1, 15, ry + 1, RAIL[1])
        b.rect(0, ry + 2, 15, ry + 2, RAIL[2])
    return b


def draw_edge():
    b = Block()
    b.rect(0, 0, 15, 0, INK)
    b.rect(0, 1, 15, 1, STONE[0])
    b.rect(0, 2, 15, 4, STONE[1])
    b.rect(0, 1, 0, 4, STONE[2])
    b.rect(0, 5, 15, 5, STONE[2])
    b.rect(0, 6, 15, 10, YEL[0])
    for x in range(1, 16, 4):
        b.put(x, 7, YEL[1])
        b.put(x + 2, 9, YEL[1])
    b.rect(0, 11, 15, 11, YEL[1])
    paving(b, 12, 15, 0)
    return b


def draw_paving(odd):
    b = Block()
    paving(b, 0, 15, 20 if odd else 4)
    return b


def draw_exit_mat():
    """Sits on an odd paving row (the map's bottom row is 11)."""
    b = draw_paving(True)
    b.rect(1, 1, 14, 14, MAT[0])
    b.rect(2, 2, 13, 13, MAT[1])
    b.put(1, 1, pave_px(1, 21))
    b.put(14, 1, pave_px(14, 21))
    b.put(1, 14, pave_px(1, 34))
    b.put(14, 14, pave_px(14, 34))
    for y in (3, 12):
        b.rect(3, y, 12, y, MAT[0])
    # down arrow
    b.rect(7, 4, 8, 8, MAT[2])
    b.rect(4, 8, 11, 8, MAT[2])
    b.rect(5, 9, 10, 9, MAT[2])
    b.rect(6, 10, 9, 10, MAT[2])
    b.rect(7, 11, 8, 11, MAT[2])
    return b


def draw_void():
    b = Block()
    b.rect(0, 0, 15, 15, BLACK)
    return b


# ------------------------------------------------------------------ metatile list
# (label, theme, draw(), behaviour, layer type). Order = metatile id from 0x200.
def metatile_defs():
    defs = [("Void", "tosa", draw_void, MB_NORMAL, LAYER_NORMAL)]
    for theme, suffix in (("tosa", ""), ("telok", "_Brick")):
        t = theme_colours(theme)
        shell = [
            ("Ceiling_Beam", lambda t=t: draw_ceiling(t, True)),
            ("Ceiling", lambda t=t: draw_ceiling(t, False)),
            ("Canopy_Beam", lambda t=t: draw_canopy(t, True)),
            ("Canopy", lambda t=t: draw_canopy(t, False)),
            ("Wall", lambda t=t: draw_wall(t)),
            ("Wall_Poster", lambda t=t: draw_poster(t)),
            ("WallBase", lambda t=t: draw_wall_base(t)),
            ("Pillar_Canopy", lambda t=t: draw_pillar_canopy(t)),
            ("Pillar_Wall", lambda t=t: draw_pillar_wall(t)),
            ("Pillar_Base", lambda t=t: draw_pillar_base(t)),
        ]
        for label, fn in shell:
            defs.append((label + suffix, theme, fn, MB_NORMAL, LAYER_COVERED))
        if theme == "tosa":
            defs += [
                ("Track", "tosa", draw_track, MB_NORMAL, LAYER_COVERED),
                ("PlatformEdge", "tosa", draw_edge, MB_NORMAL, LAYER_NORMAL),
                ("Paving_A", "tosa", lambda: draw_paving(False), MB_NORMAL, LAYER_NORMAL),
                ("Paving_B", "tosa", lambda: draw_paving(True), MB_NORMAL, LAYER_NORMAL),
                ("ExitMat", "tosa", draw_exit_mat, MB_SOUTH_ARROW_WARP, LAYER_NORMAL),
            ]
    return defs


# ------------------------------------------------------------------ conversion
def quadrant_to_tile(b, qx, qy, theme):
    cols = {b.px[qy * 8 + y][qx * 8 + x] for y in range(8) for x in range(8)}
    if None in cols:
        raise ValueError("undrawn pixel")
    for slot in THEME_PALS[theme]:
        pal = PALETTES[slot]
        if all(c in pal[1:] for c in cols):
            # index 0 is transparent: look colours up from index 1
            tile = tuple(tuple(pal.index(b.px[qy * 8 + y][qx * 8 + x], 1) for x in range(8))
                         for y in range(8))
            return slot, tile
    raise ValueError(f"no palette holds {sorted(cols)}")


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


def build():
    bank = TileBank()
    metatiles, attrs, labels = [], [], []
    for label, theme, fn, behaviour, layer in metatile_defs():
        b = fn()
        bottom = []
        for qy in range(2):
            for qx in range(2):
                slot, tile = quadrant_to_tile(b, qx, qy, theme)
                idx, hf, vf = bank.add(tile)
                bottom.append((SECONDARY_TILE_BASE + idx) | (hf << 10) | (vf << 11) | (slot << 12))
        metatiles.append(bottom + [0, 0, 0, 0])     # top layer: all transparent
        attrs.append((behaviour & 0xFF) | (layer << 12))
        labels.append(label)
    return bank, metatiles, attrs, labels


def write_pal(path, cols):
    cols = list(cols) + [BLACK] * (16 - len(cols))
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in cols:
            f.write(f"{c[0]} {c[1]} {c[2]}\n")


def write_tileset(bank, metatiles, attrs):
    os.makedirs(os.path.join(TS_DIR, "palettes"), exist_ok=True)
    n = len(bank.tiles)
    rows = (n + 15) // 16
    im = Image.new("P", (128, rows * 8), 0)
    flat = list(PALETTES[6]) + [BLACK] * (16 - len(PALETTES[6]))
    im.putpalette([v for c in flat for v in c])
    px = im.load()
    for i, tile in enumerate(bank.tiles):
        ox, oy = (i % 16) * 8, (i // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = tile[y][x]
    im.save(os.path.join(TS_DIR, "tiles.png"), bits=4, optimize=False)
    with open(os.path.join(TS_DIR, "metatiles.bin"), "wb") as f:
        for m in metatiles:
            f.write(struct.pack("<8H", *m))
    with open(os.path.join(TS_DIR, "metatile_attributes.bin"), "wb") as f:
        for a in attrs:
            f.write(struct.pack("<H", a))
    for slot in range(16):
        write_pal(os.path.join(TS_DIR, "palettes", f"{slot:02d}.pal"), PALETTES.get(slot, [BLACK]))


# ------------------------------------------------------------------ test layout
def mid(labels, name):
    return SECONDARY_METATILE_BASE + labels.index(name)


def paint_test_layout(labels, brick=False):
    """LAYOUT_TRAIN_TEST_STATION, 20x12. Track row 4, boarding row 5, exit mat at (9,11)."""
    W, H = 20, 12
    s = "_Brick" if brick else ""
    posters, pillars = (2, 17), (6, 13)
    grid = []
    for y in range(H):
        for x in range(W):
            beam = x % 2 == 0
            if y == 0:
                name, walk = ("Ceiling_Beam" if beam else "Ceiling") + s, False
            elif y == 1:
                name = ("Pillar_Canopy" if x in pillars else
                        "Canopy_Beam" if beam else "Canopy") + s
                walk = False
            elif y == 2:
                name = ("Pillar_Wall" if x in pillars else
                        "Wall_Poster" if x in posters else "Wall") + s
                walk = False
            elif y == 3:
                name, walk = ("Pillar_Base" if x in pillars else "WallBase") + s, False
            elif y == 4:
                name, walk = "Track", False
            elif y == 5:
                name, walk = "PlatformEdge", True
            elif (x, y) == (9, 11):
                name, walk = "ExitMat", True
            else:
                name, walk = ("Paving_A" if y % 2 == 0 else "Paving_B"), True
            m = mid(labels, name)
            grid.append(m | (0x3000 if walk else 0x0400))    # walkable: elev 3; else collision 1
    with open(os.path.join(LAYOUT_DIR, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{W * H}H", *grid))
    void = mid(labels, "Void") | 0x0400
    with open(os.path.join(LAYOUT_DIR, "border.bin"), "wb") as f:
        f.write(struct.pack("<4H", *([void] * 4)))


# ------------------------------------------------------------------ previews
def sheet(metatiles, labels, scale=3):
    """Every metatile at `scale`x, straight from the generated data (round-trip check)."""
    from PIL import ImageDraw
    tiles_im = Image.open(os.path.join(TS_DIR, "tiles.png"))
    tp = tiles_im.load()
    cols = 4
    cell_w, cell_h = 16 * scale + 150, 16 * scale + 8
    rows = (len(metatiles) + cols - 1) // cols
    im = Image.new("RGB", (cols * cell_w, rows * cell_h), (24, 24, 32))
    dr = ImageDraw.Draw(im)
    for n, m in enumerate(metatiles):
        blk = Image.new("RGB", (16, 16))
        bp = blk.load()
        for q in range(4):
            e = m[q]
            t, hf, vf, pal = (e & 0x3FF) - SECONDARY_TILE_BASE, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            for y in range(8):
                for x in range(8):
                    sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                    ci = tp[(t % 16) * 8 + sx, (t // 16) * 8 + sy]
                    bp[(q & 1) * 8 + x, (q >> 1) * 8 + y] = PALETTES[pal][ci]
        x, y = (n % cols) * cell_w, (n // cols) * cell_h
        im.paste(blk.resize((16 * scale, 16 * scale), Image.NEAREST), (x + 4, y + 4))
        dr.text((x + 16 * scale + 10, y + 12), f"{SECONDARY_METATILE_BASE + n:03X} {labels[n]}",
                fill=(230, 230, 230))
    return im


def load_jasc(path):
    vals = open(path).read().split()[3:]
    return [tuple(int(v) for v in vals[i * 3:i * 3 + 3]) for i in range(len(vals) // 3)]


def sprite(png, pal, box):
    """Indexed sprite crop -> RGBA, index 0 transparent."""
    src = Image.open(os.path.join(ROOT, png)).crop(box)
    pal = load_jasc(os.path.join(ROOT, pal))
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    sp, op = src.load(), out.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            i = sp[x, y] & 15
            if i:
                op[x, y] = pal[i] + (255,)
    return out


def station_mock(door_x=9, track_y=4, door_open=False):
    """Test layout + parked train (door centred on (door_x, track_y)) + the map's NPCs."""
    sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "train_ui"))
    import render_layout as RL
    path = os.path.join(OUT, "_layout_1x.png")
    RL.render_layout("LAYOUT_TRAIN_TEST_STATION", path)
    im = Image.open(path).convert("RGBA")
    os.remove(path)
    # graphics/train/train.png: 64x256, pieces 0 rear, 1 door shut, 2 loco, 3 door open
    left = door_x * 16 + 8 - (64 + 24) - 8          # TRAIN_DOOR_X = 88, door width 16
    top = track_y * 16 + 16 - 64                    # piece bottoms on the track tile's bottom
    for i, piece in enumerate((0, 3 if door_open else 1, 2)):
        im.alpha_composite(sprite("graphics/train/train.png", "graphics/train/train.pal",
                                  (0, piece * 64, 64, piece * 64 + 64)), (left + i * 64, top))
    people = "graphics/object_events/pics/people/"
    obj = [  # (png, pal, frame, tile x, tile y, hflip)
        (people + "man_1.png", "graphics/object_events/palettes/npc_3.pal", 2, 11, 5, False),
        (people + "scientist_1.png", "graphics/object_events/palettes/npc_3.pal", 0, 5, 8, False),
        (people + "brendan/walking.png", "graphics/object_events/palettes/brendan.pal", 1, 9, 5, False),
    ]
    for png, pal, f, tx, ty, hf in obj:
        s = sprite(png, pal, (f * 16, 0, f * 16 + 16, 32))
        if hf:
            s = s.transpose(Image.FLIP_LEFT_RIGHT)
        im.alpha_composite(s, (tx * 16, ty * 16 + 16 - 32))
    return im


def up(im, k=3):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def main(argv):
    bank, metatiles, attrs, labels = build()
    write_tileset(bank, metatiles, attrs)
    print(f"tiles: {len(bank.tiles)} (incl. blank tile 0) / 512")
    print(f"metatiles: {len(metatiles)}")
    for slot, pal in sorted(PALETTES.items()):
        print(f"  pal {slot:2d}: {len(pal) - 1} colours")
    if "--paint-test-layout" in argv:
        paint_test_layout(labels, brick="--brick" in argv)
        print("painted LAYOUT_TRAIN_TEST_STATION")
    if "--previews" in argv:
        os.makedirs(OUT, exist_ok=True)
        sheet(metatiles, labels).save(os.path.join(OUT, "metatile_sheet_3x.png"))
        sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "train_ui"))
        import render_layout as RL
        p = os.path.join(OUT, "test_layout_1x.png")
        RL.render_layout("LAYOUT_TRAIN_TEST_STATION", p)
        up(Image.open(p)).save(os.path.join(OUT, "test_layout_3x.png"))
        RL.render_layout("LAYOUT_TRAIN_TEST_STATION", p, collision=True)
        up(Image.open(p)).save(os.path.join(OUT, "test_layout_collision_3x.png"))
        os.remove(p)
        mock = station_mock()
        up(mock).save(os.path.join(OUT, "station_with_train_3x.png"))
        # in-game camera with the player on (9,5): player tile at screen (112, 64)
        cam = mock.crop((9 * 16 - 112, 5 * 16 - 64, 9 * 16 - 112 + 240, 5 * 16 - 64 + 160))
        up(cam).save(os.path.join(OUT, "station_with_train_camera_3x.png"))
        up(station_mock(door_open=True)).save(os.path.join(OUT, "station_with_train_open_3x.png"))
    if "--labels" in argv:
        for i, lab in enumerate(labels):
            print(f"#define METATILE_UrbanInterior_{lab:<22} 0x{SECONDARY_METATILE_BASE + i:03X}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
