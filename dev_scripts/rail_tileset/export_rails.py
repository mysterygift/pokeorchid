#!/usr/bin/env python3
"""Outdoor rail kit for the primary route tileset (gTileset_General).

    python3 dev_scripts/rail_tileset/export_rails.py [--preview DIR] [--dry-run]

Draws sleepers + rails as a transparent overlay and installs them into fixed, previously unused
slots of data/tilesets/primary/general (tiles.png, metatiles.bin, metatile_attributes.bin).
Rerunning rewrites the same slots, so it is safe to run again after changing the art.
Needs Pillow.

Why it fits the tileset:
  * Palette: the overlay only uses colours already in primary palette 3 (rock / dirt palette:
    greys for steel, brown ramp for timber). No palette file is edited.
  * Layers: each rail metatile is  bottom = an existing ground metatile's tiles (grass is
    palette 2, sand palette 5),  top = rail overlay (palette 3, index 0 transparent),
    layer type COVERED. Both layers draw under sprites and the top BG stays empty, which the
    train sprite needs (see docs/orchid/tosa_rail.md). One set of rail tiles serves every ground.
  * Tiles: 37 new 8x8 tiles in blank slots. East curves are h-flips of the west curves, so the
    vertical rail is drawn symmetric (dark, light, light, dark).
  * The horizontal track copies the station track tile of gTileset_UrbanInterior
    (dev_scripts/station_tileset/export_tileset.py draw_track): sleepers 5 px wide every 8 px,
    rails on rows 2-5 and 11-14.

To put rails on another ground (e.g. brown dirt 0x10C) add rows to METATILES using free slots.
"""
import math
import os
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TS_DIR = os.path.join(ROOT, "data", "tilesets", "primary", "general")

PAL = 3
# palette-3 indices
T, W, L, M, G, K = 0, 1, 2, 4, 5, 8          # transparent, white, light grey, mid grey, steel grey, dark outline
B9, B10, B11, B12, B13, B14 = 9, 10, 11, 12, 13, 14   # brown ramp, light -> dark
SL_HI, SL, SL_SH = B12, B13, B14             # sleeper highlight / body / shadow ("warm" option A)

LAYER_COVERED = 1
MB_NORMAL = 0x00

# 8x8 tile slots that were blank and referenced by no metatile of General or of any secondary
# tileset paired with it (checked on dev and engine-dev, 2026-11-17). Order matters: fixed.
TILE_SLOTS = [15, 26, 31, 42, 58, 167, 183, 197, 219, 235, 237, 258, 290, 306, 315, 322, 331, 338,
              346, 348, 349, 362, 364, 365, 370, 378, 380, 394, 397, 409, 413, 422, 423, 425, 429,
              490, 491, 492, 493, 494, 495]

GROUND = {"grass": 0x001, "sand": 0x121}

# metatile slot -> (piece, ground). All of these slots held vanilla metatiles that no map with
# General as its primary tileset used, and that have no METATILE_General_* label.
# Curve cells are named <W|E><N|S><col><row> inside the 2x2 block.
METATILES = {
    # grass: curves as 2x2 blocks in the Porymap picker (8 metatiles per row)
    0x10E: ("ES00", "grass"), 0x10F: ("ES10", "grass"), 0x116: ("ES01", "grass"), 0x117: ("ES11", "grass"),
    0x11E: ("WS00", "grass"), 0x11F: ("WS10", "grass"), 0x126: ("WS01", "grass"), 0x127: ("WS11", "grass"),
    0x13B: ("EN00", "grass"), 0x13C: ("EN10", "grass"), 0x143: ("EN01", "grass"), 0x144: ("EN11", "grass"),
    0x09D: ("WN00", "grass"), 0x09E: ("WN10", "grass"), 0x0A5: ("WN01", "grass"), 0x0A6: ("WN11", "grass"),
    0x12E: ("H", "grass"), 0x12F: ("HX", "grass"),
    0x0DD: ("HW", "grass"), 0x0DE: ("HE", "grass"),
    0x0AD: ("V", "grass"), 0x0AE: ("VX", "grass"),
    0x0B5: ("VN", "grass"), 0x0BD: ("VS", "grass"),
    # sand: straights, buffers and crossings
    0x0E3: ("H", "sand"), 0x0E4: ("HX", "sand"), 0x0E5: ("HW", "sand"), 0x0E6: ("HE", "sand"),
    0x0E7: ("V", "sand"), 0x0D7: ("VX", "sand"),
    0x0C5: ("VN", "sand"), 0x0CD: ("VS", "sand"),
}

CHARS = {".": T, "K": K, "W": W, "M": M, "G": G}


def blank(w=16, h=16):
    return [[T] * w for _ in range(h)]


# ------------------------------------------------------------------ straights
def piece_h():
    """Station geometry: sleepers 5 px wide every 8 px, rails at y 3 and 12."""
    p = blank()
    for x in (2, 10):
        for y in range(1, 15):
            for xx in range(x, x + 5):
                p[y][xx] = SL
        for xx in range(x, x + 5):
            p[1][xx] = SL_HI
        for y in range(1, 15):
            p[y][x + 4] = SL_SH
        for xx in range(x, x + 5):
            p[14][xx] = SL_SH
    for ry in (3, 12):
        for x in range(16):
            p[ry - 1][x] = K; p[ry][x] = L; p[ry + 1][x] = G; p[ry + 2][x] = K
    return p


VR = (1, 11)   # left column of each vertical rail; symmetric so curves can be h-flipped


def v_rails(p, rows):
    for rx in VR:
        for y in rows:
            p[y][rx] = K; p[y][rx + 1] = L; p[y][rx + 2] = L; p[y][rx + 3] = K


def v_sleeper(p, y):
    for yy in range(y, y + 5):
        for x in range(16):
            p[yy][x] = SL
    for x in range(16):
        p[y][x] = SL_HI
        p[y + 4][x] = SL_SH


def piece_v():
    p = blank()
    v_sleeper(p, 2); v_sleeper(p, 10)
    v_rails(p, range(16))
    return p


# ------------------------------------------------------------------ curves
def curve(south):
    """2x2-metatile curve joining a west H leg to a north (south=False) or south (south=True) V leg.
    The H leg is on the row farthest from the centre of curvature, the V leg in the right column."""
    n, off = 32, 16
    cx, cy = 0.0, (n + 1.0 if south else 0.0)
    in0, out0 = off + 2, off + 11          # rail band starts at the H end (rows 2-5 / 11-14)
    in1, out1 = off + 1, off + 11          # ... and at the V end (cols 1-4 / 11-14)
    sl0, sl1 = (off + 1, off + 15), (off + 0, off + 16)   # sleeper radial extent at each end
    nsl = 5

    def geom(x, y):
        dx, dy = x + 0.5 - cx, y + 0.5 - cy
        ady = -dy if south else dy
        if dx < 0:
            return dx, ady, ady, 0.0       # west of the block: straight H leg
        if ady < 0:
            return dx, ady, dx, 1.0        # past the V end: straight V leg
        return dx, ady, math.hypot(dx, ady), math.atan2(dx, ady) / (math.pi / 2)

    def rail(x, y):
        _, _, r, t = geom(x, y)
        for b0, b1 in ((in0, in1), (out0, out1)):
            rho = r - (b0 + (b1 - b0) * t)
            if 0 <= rho < 4:
                return "k" if (rho < 1 or rho >= 3) else "m"
        return None

    def sleeper(x, y):
        dx, ady, _, _ = geom(x, y)
        if dx < 0 or ady < 0:
            return False
        for i in range(nsl):
            ti = (i + 0.5) / nsl
            ph = ti * math.pi / 2
            ux, uy = math.sin(ph), math.cos(ph)
            along = dx * ux + ady * uy
            across = abs(dx * uy - ady * ux)
            lo = sl0[0] + (sl1[0] - sl0[0]) * ti
            hi = sl0[1] + (sl1[1] - sl0[1]) * ti
            if lo <= along < hi and across < 2.5:
                return True
        return False

    p = blank(n, n)
    for y in range(n):
        for x in range(n):
            if sleeper(x, y):
                c = SL
                if not sleeper(x, y - 1):
                    c = SL_HI
                elif not sleeper(x, y + 1):
                    c = SL_SH
                p[y][x] = c
            rc = rail(x, y)
            if rc == "k":
                p[y][x] = K
            elif rc == "m":
                t = geom(x, y)[3]
                # front-face shade on the lowest light pixel, only where the rail runs mostly sideways
                p[y][x] = G if (rail(x, y + 1) != "m" and rail(x, y - 1) == "m" and t < 0.62) else L
    # tile budget: an 8x8 tile holding only a few stray sleeper-corner pixels is not worth a slot
    for ty in range(0, n, 8):
        for tx in range(0, n, 8):
            pts = [(x, y) for y in range(ty, ty + 8) for x in range(tx, tx + 8) if p[y][x] != T]
            if 0 < len(pts) <= 6 and not any(rail(x, y) for x, y in pts):
                for x, y in pts:
                    p[y][x] = T
    return p


def hflip(p):
    return [r[::-1] for r in p]


def cells(p):
    n = len(p) // 16
    return [[[row[cx * 16:cx * 16 + 16] for row in p[cy * 16:cy * 16 + 16]] for cx in range(n)] for cy in range(n)]


# ------------------------------------------------------------------ buffer stops and crossings
BEAM_V = ["KKKKK", "KWWWK", "KWWWK", "KGGGK", "KGGGK", "KWWWK", "KWWWK", "KWWWK", "KGGGK", "KGGGK",
          "KWWWK", "KWWWK", "KWWWK", "KMMMK", "KMMMK", "KKKKK"]
BEAM_H = ["KKKKKKKKKKKKKKKK", "KWWWGGWWWWGGWWWK", "KWWWGGWWWWGGWWWK", "KMMMGGMMMMGGMMMK", "KMMMGGMMMMGGMMMK",
          "KKKKKKKKKKKKKKKK"]


def piece_h_end():
    """H track from the west ending at a striped buffer beam on the right."""
    p = piece_h()
    for y in range(16):
        for x in range(10, 16):
            p[y][x] = T
    for y, r in enumerate(BEAM_V):
        for i, c in enumerate(r):
            p[y][10 + i] = CHARS[c]
    return p


def piece_v_end(top):
    """V track ending at a buffer beam; top=True puts the beam at the north end."""
    p = blank()
    v_sleeper(p, 10 if top else 2)
    v_rails(p, range(7, 16) if top else range(0, 9))
    y0 = 1 if top else 9
    for i, r in enumerate(BEAM_H):
        for x, c in enumerate(r):
            p[y0 + i][x] = CHARS[c]
    return p


def piece_h_cross():
    """Timber deck for a footpath crossing an H track."""
    p = blank()
    for y in range(16):
        for x in range(16):
            c = B10
            if y == 0: c = B9
            if y == 8: c = B11
            if y == 15: c = B12
            if x in (0, 15): c = B12
            p[y][x] = c
    for ry in (3, 12):
        for x in range(16):
            p[ry - 1][x] = K; p[ry][x] = L; p[ry + 1][x] = G; p[ry + 2][x] = K
    return p


def piece_v_cross():
    p = blank()
    for y in range(1, 15):
        for x in range(16):
            c = B10
            if y == 1: c = B9
            if x in (6, 9) and y > 1: c = B11
            if y == 14: c = B12
            p[y][x] = c
    v_rails(p, range(16))
    return p


def build_pieces():
    P = {"H": piece_h(), "V": piece_v()}
    for south, nm in ((False, "N"), (True, "S")):
        big = curve(south)
        cw, ce = cells(big), cells(hflip(big))
        for cy in range(2):
            for cx in range(2):
                P[f"W{nm}{cx}{cy}"] = cw[cy][cx]
                P[f"E{nm}{cx}{cy}"] = ce[cy][cx]
    P["HE"] = piece_h_end(); P["HW"] = hflip(P["HE"])
    P["VN"] = piece_v_end(True); P["VS"] = piece_v_end(False)
    P["HX"] = piece_h_cross(); P["VX"] = piece_v_cross()
    return P


PIECE_ORDER = (["H", "V"] + [f"{s}{n}{cx}{cy}" for s in "WE" for n in "NS" for cy in (0, 1) for cx in (0, 1)]
               + ["HE", "HW", "VN", "VS", "HX", "VX"])


# ------------------------------------------------------------------ packing (flip-aware tile bank)
class Bank:
    def __init__(self, slots):
        self.slots, self.tiles, self.lut = slots, [], {}

    def add(self, t):
        t = tuple(tuple(r) for r in t)
        if all(c == T for r in t for c in r):
            return 0                                    # tile 0, palette 0: the usual empty top layer
        if t not in self.lut:
            if len(self.tiles) >= len(self.slots):
                raise SystemExit("out of tile slots: add entries to TILE_SLOTS")
            idx = self.slots[len(self.tiles)]
            self.tiles.append(t)
            h = tuple(r[::-1] for r in t); v = tuple(t[::-1]); hv = tuple(r[::-1] for r in v)
            for f, bits in ((t, 0), (h, 0x400), (v, 0x800), (hv, 0xC00)):
                self.lut.setdefault(f, idx | bits | (PAL << 12))
        return self.lut[t]


def pack(P):
    bank = Bank(TILE_SLOTS)
    packed = {nm: [bank.add([row[qx * 8:qx * 8 + 8] for row in P[nm][qy * 8:qy * 8 + 8]])
                   for qy in (0, 1) for qx in (0, 1)] for nm in PIECE_ORDER}
    return bank, packed


# ------------------------------------------------------------------ tileset i/o
def read_metatiles():
    b = open(os.path.join(TS_DIR, "metatiles.bin"), "rb").read()
    a = open(os.path.join(TS_DIR, "metatile_attributes.bin"), "rb").read()
    return (list(struct.unpack(f"<{len(b) // 2}H", b)), list(struct.unpack(f"<{len(a) // 2}H", a)))


def install(bank, packed, dry=False):
    png = os.path.join(TS_DIR, "tiles.png")
    im = Image.open(png)
    assert im.mode == "P" and im.size == (128, 256), (im.mode, im.size)
    px = im.load()
    for i, t in enumerate(bank.tiles):
        slot = bank.slots[i]
        ox, oy = (slot % 16) * 8, (slot // 16) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = t[y][x]
    meta, attr = read_metatiles()
    for mid, (piece, ground) in METATILES.items():
        g = GROUND[ground]
        meta[mid * 8:mid * 8 + 4] = meta[g * 8:g * 8 + 4]          # bottom layer: the ground's own tiles
        meta[mid * 8 + 4:mid * 8 + 8] = packed[piece]              # top layer: rails
        attr[mid] = MB_NORMAL | (LAYER_COVERED << 12)
    if not dry:
        im.save(png, bits=4, optimize=False)
        open(os.path.join(TS_DIR, "metatiles.bin"), "wb").write(struct.pack(f"<{len(meta)}H", *meta))
        open(os.path.join(TS_DIR, "metatile_attributes.bin"), "wb").write(struct.pack(f"<{len(attr)}H", *attr))
    return im, meta, attr


# ------------------------------------------------------------------ preview (rendered from the packed data)
def load_pal(i):
    lines = open(os.path.join(TS_DIR, "palettes", f"{i:02d}.pal")).read().split("\n")
    return [tuple(int(v) & ~7 for v in lines[3 + k].split()) for k in range(16)]


def draw_meta(out, tiles_im, pals, meta, mid, x, y):
    tp = tiles_im.load()
    for layer in (0, 1):
        for q in range(4):
            e = meta[mid * 8 + layer * 4 + q]
            t, hf, vf, pal = e & 0x3FF, e & 0x400, e & 0x800, pals[(e >> 12) % 6]
            ox, oy = (t % 16) * 8, (t // 16) * 8
            for yy in range(8):
                for xx in range(8):
                    c = tp[ox + (7 - xx if hf else xx), oy + (7 - yy if vf else yy)] & 15
                    if c:
                        out.putpixel((x + (q % 2) * 8 + xx, y + (q // 2) * 8 + yy), pal[c] + (255,))


def preview(tiles_im, meta, outdir, scale=3):
    """Metatile sheet of every installed slot, in picker order, plus a small sample layout."""
    os.makedirs(outdir, exist_ok=True)
    pals = [load_pal(i) for i in range(6)]
    back = pals[0][0] + (255,)
    ids = sorted(METATILES)
    sheet = Image.new("RGBA", (len(ids) * 17 + 1, 18), (255, 0, 255, 255))
    for i, mid in enumerate(ids):
        cell = Image.new("RGBA", (16, 16), back)
        draw_meta(cell, tiles_im, pals, meta, mid, 0, 0)
        sheet.paste(cell, (1 + i * 17, 1))
    sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST).save(os.path.join(outdir, "rail_metatiles.png"))
    by = {v: k for k, v in METATILES.items()}
    g = lambda nm, gr="grass": by[(nm, gr)]
    blk = lambda k: [[g(k + "00"), g(k + "10")], [g(k + "01"), g(k + "11")]]
    w, h = 12, 9
    grid = [[0x001] * w for _ in range(h)]
    for (bx, by_), k in (((1, 1), "ES"), ((7, 1), "WS"), ((1, 5), "EN"), ((7, 5), "WN")):
        for j, row in enumerate(blk(k)):
            for i, mid in enumerate(row):
                grid[by_ + j][bx + i] = mid
    for x in range(3, 7):
        grid[1][x] = g("H"); grid[6][x] = g("H")
    grid[1][5] = g("HX")
    for y in (3, 4):
        grid[y][1] = g("V"); grid[y][8] = g("V")
    grid[4][1] = g("VX")
    for x in range(w):
        grid[8][x] = 0x121
    grid[8][0] = g("HW", "sand"); grid[8][w - 1] = g("HE", "sand")
    for x in range(1, w - 1):
        grid[8][x] = g("H", "sand")
    grid[8][6] = g("HX", "sand")
    for y, nm in ((0, "VN"), (1, "V"), (2, "VX"), (3, "VS")):
        grid[y][10] = g(nm, "grass")
    out = Image.new("RGBA", (w * 16, h * 16), back)
    for y in range(h):
        for x in range(w):
            draw_meta(out, tiles_im, pals, meta, grid[y][x], x * 16, y * 16)
    out.resize((out.width * scale, out.height * scale), Image.NEAREST).save(os.path.join(outdir, "rail_sample.png"))


def main(argv):
    dry = "--dry-run" in argv
    P = build_pieces()
    bank, packed = pack(P)
    tiles_im, meta, attr = install(bank, packed, dry)
    print(f"{len(bank.tiles)} tiles in slots {bank.slots[:len(bank.tiles)]}")
    print(f"{len(METATILES)} metatiles:", " ".join(f"{m:03X}={p}/{g}" for m, (p, g) in sorted(METATILES.items())))
    if "--preview" in argv:
        preview(tiles_im, meta, argv[argv.index("--preview") + 1])
    print("dry run, nothing written" if dry else "written to " + os.path.relpath(TS_DIR, ROOT))


if __name__ == "__main__":
    main(sys.argv[1:])
