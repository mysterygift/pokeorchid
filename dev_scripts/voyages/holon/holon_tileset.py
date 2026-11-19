"""
gTileset_Holon (DRAFT, round 2): a Holon-only copy of gTileset_Fortree plus the approved Holon additions.

Writes the draft tileset to dev_scripts/voyages/out/batch4/gTileset_Holon/ (tiles.png, metatiles.bin,
metatile_attributes.bin, palettes/00-15.pal, holon_metatiles.json). Nothing under data/ is touched: when
approved, the folder is copied to data/tilesets/secondary/holon and wired up (graphics.h with
"-num_tiles 512", metatiles.h, headers.h, layouts). Fortree and every other tileset stay as they are.

What changes against the Fortree copy:
  * palette 06 (blank in Fortree): "Holon rock" = General palette 03 with its brown rock ramp (slots 8-14)
    swapped for blue-grey of the same luminance. Grass / grey slots stay identical, so the grass drawn
    inside rock tiles still matches.
  * palettes 07 and 12 stay blank (free); 08-11 are Fortree's, unchanged.
  * blue-grey rock = NEW METATILES that reuse the existing rock tiles (General primary tiles, Fortree
    mound / spike tiles) with palette 03 -> 06 in their entries: no new tiles. The dome stays the vanilla
    Ancient Tomb dome art (vanilla dithering), only recoloured.
  * rails = the existing Orchid rail kit pieces (export_rails.build_pieces: straight H, buffer stop HW) on
    grass, exactly as install_area_kit.py builds them (grass bottom layer, rail overlay in palette 03 on
    the top layer, COVERED). Palette 03 is General's own, unchanged.
  * new art (palette 06 only): carved standing stone 1x2, lake pillar 1x3 (in water), sphere plinth 3x2,
    sealed dome door (2 cells: the arch over 0x064 and the door 0x0A7 of the tomb dome, opening filled
    with a carved slab).

usage: <venv python> dev_scripts/voyages/holon/holon_tileset.py      (writes the draft folder)
"""
import json
import math
import os
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
VOY = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(VOY, "..", ".."))
DRAFT = os.path.join(HERE, "_draft")
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "rail_tileset"))
import export_rails as ER   # noqa: E402  (the approved rail kit geometry; nothing is installed)

FORTREE = os.path.join(ROOT, "data", "tilesets", "secondary", "fortree")
GENERAL = os.path.join(ROOT, "data", "tilesets", "primary", "general")
OUT = os.path.join(DRAFT, "gTileset_Holon")

ROCK_PAL = 6
COVERED, NORMAL = 1, 0
FIRST_NEW = 0x120          # secondary-relative index of the first Holon metatile (0x320); Fortree ends 0x11C

# Rock metatiles that get a blue-grey copy (General primary ids + Fortree mound / spike ids). Pond edges keep
# their brown bank lip (they are earth, not rock).
ROCK_IDS = [0x064, 0x06A, 0x071, 0x072, 0x073, 0x074, 0x075, 0x079, 0x07A, 0x07B, 0x07C, 0x07D, 0x089,
            0x091, 0x0A7, 0x0A9, 0x0D4, 0x0E0, 0x0E1, 0x0E2, 0x230, 0x231, 0x232, 0x238, 0x23A, 0x240, 0x242,
            # Weather Institute cells whose palette-03 part is the rock face behind the roof
            0x2D9, 0x2DA, 0x2A0, 0x2A1, 0x2A2, 0x2A4, 0x2A5, 0x2AC, 0x2AD, 0x2AE]

# Drained-grass copies (palette 02 -> 07): metatiles drawn only in General palette 02 (grass, tall / long grass,
# 1-wide trees, peeks, flowers). Ids that turn out to use any other palette are skipped by build().
DRAIN_IDS = [0x001, 0x004, 0x00D, 0x00E, 0x00F, 0x015, 0x016, 0x017, 0x01D, 0x0C6, 0x0C7, 0x1C6, 0x1C7, 0x1CE,
             0x1CF, 0x208]
DRAIN_PAL = 7

# Holon palette 06: General 03 with the rock ramp + outline in blue-grey (same luminance steps).
BLUEGREY = {8: (48, 48, 72), 9: (224, 232, 240), 10: (184, 196, 216), 11: (152, 164, 192), 12: (120, 132, 168),
            13: (88, 100, 136), 14: (64, 72, 104)}

# pal-06 letters for the new art: K outline, 1..6 rock ramp light->dark (slots 9..14), W white, a b c d greys,
# S shadow on grass (General's dark grass slot 6), '.' transparent
L6 = {".": 0, "W": 1, "a": 2, "b": 3, "c": 4, "d": 5, "S": 6, "K": 8,
      "1": 9, "2": 10, "3": 11, "4": 12, "5": 13, "6": 14}


def read_u16(p):
    b = open(p, "rb").read()
    return list(struct.unpack("<%dH" % (len(b) // 2), b))


def load_pal(p):
    rows = open(p).read().split("\n")[3:19]
    return [tuple(int(v) for v in r.split()) for r in rows]


def jasc(cols):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in cols)


# ------------------------------------------------------------------ green desaturation (Holon story beat)
def _hsv(c):
    import colorsys
    return colorsys.rgb_to_hsv(*(v / 255 for v in c))


def _rgb(h, sat, v):
    import colorsys
    return tuple(min(248, int(round(x * 255 / 8)) * 8) for x in colorsys.hsv_to_rgb(h, sat, v))


def is_green(c):
    h, sat, v = _hsv(c)
    return 70 / 360 <= h <= 175 / 360 and sat > 0.12 and v > 0.08


def desat(c, amount=0.35, toward=72 / 360, shift=0.10):
    """Greens only: saturation -amount, hue nudged toward olive; value kept (ramps / dithering still read)."""
    if not is_green(c):
        return c
    h, sat, v = _hsv(c)
    return _rgb(h + (toward - h) * shift, sat * (1 - amount), v)


def drained(c):
    """The stronger 'drained by the Power Spot' ramp: greens lose ~70% saturation and drift to dry straw."""
    if not is_green(c):
        return c
    h, sat, v = _hsv(c)
    return _rgb(h + (60 / 360 - h) * 0.25, sat * 0.45, min(1.0, v * 1.03))


GREEN_VARIANTS = {
    # name: (secondary dir suffix, desaturate secondary greens, primary copy dir or None)
    "current": ("gTileset_Holon", False, None),
    "secondary": ("gTileset_HolonDesat", True, None),
    "full": ("gTileset_HolonDesat", True, "gTileset_GeneralHolon"),
}


def write_green_variants():
    """gTileset_HolonDesat = the Holon draft with palettes 06 and 08-11 desaturated (07 stays the drained
    ramp, 12 free); gTileset_GeneralHolon = General's tiles / metatiles with palettes 00-05 desaturated (in the
    game this needs only a new palette array: the struct can point at General's own tiles and metatiles).
    Returns {palette file: [(slot, old, new)]} of what changed."""
    import shutil
    changes = {}
    sec = os.path.join(os.path.dirname(OUT), "gTileset_HolonDesat")
    if os.path.isdir(sec):
        shutil.rmtree(sec)
    shutil.copytree(OUT, sec)
    for i in (6, 8, 9, 10, 11):
        p = os.path.join(sec, "palettes", "%02d.pal" % i)
        old = load_pal(p)
        new = [old[0]] + [desat(c) for c in old[1:]]
        changes["gTileset_Holon %02d" % i] = [(k, a, b) for k, (a, b) in enumerate(zip(old, new)) if a != b]
        open(p, "w").write(jasc(new))
    prim = os.path.join(os.path.dirname(OUT), "gTileset_GeneralHolon")
    os.makedirs(os.path.join(prim, "palettes"), exist_ok=True)
    for f in ("tiles.png", "metatiles.bin", "metatile_attributes.bin"):
        shutil.copy(os.path.join(GENERAL, f), os.path.join(prim, f))
    for i in range(16):
        old = load_pal(os.path.join(GENERAL, "palettes", "%02d.pal" % i))
        new = [old[0]] + [desat(c) for c in old[1:]] if i < 6 else old
        if i < 6:
            changes["General_Holon %02d" % i] = [(k, a, b) for k, (a, b) in enumerate(zip(old, new)) if a != b]
        open(os.path.join(prim, "palettes", "%02d.pal" % i), "w").write(jasc(new))
    return changes


# ------------------------------------------------------------------ art helpers
def art(rows):
    """ASCII rows (L6 letters) -> list of lists of palette indices; validates the width."""
    w = len(rows[0])
    out = []
    for r in rows:
        assert len(r) == w, (len(r), r)
        out.append([L6[c] for c in r])
    return out


def cut(a, cx, cy):
    """16x16 cell (cx, cy) of an index grid."""
    return [row[cx * 16:cx * 16 + 16] for row in a[cy * 16:cy * 16 + 16]]


def checker(x, y):
    return (x + y) & 1


def shade_cols(w, lit=2, mid=3, dark=4, deep=5, y=0):
    """A front-face row for a column of width w (inner pixels): lit edge, a mid body, a checker-dithered step
    to the darker body, and the shadow side - dithering only at the two ramp transitions."""
    row = []
    for x in range(w):
        f = x / max(1, w - 1)
        if x == 0:
            v = lit
        elif f < 0.40:
            v = mid
        elif f < 0.55:
            v = mid if checker(x, y) else dark          # transition mid -> dark
        elif f < 0.75:
            v = dark
        elif f < 0.88:
            v = dark if checker(x, y) else deep         # transition dark -> deep
        else:
            v = deep
        row.append(v)
    return row


def diamond(g, cx, cy, r, inner=None):
    """Incised diamond centred (cx, cy) (top-left pixel of the 2x2 centre), half size r: upper-left walls
    dark (face away from the top-left light), lower-right walls light, other two mid."""
    for i in range(r + 1):
        # top tip -> widest row
        y = cy - r + i
        xl, xr = cx - i, cx + 1 + i
        g[y][xl] = L6["6"]; g[y][xr] = L6["5"]
        y2 = cy + 1 + r - i
        g[y2][xl] = L6["2"]; g[y2][xr] = L6["1"]
        if inner is not None:
            for x in range(xl + 1, xr):
                g[y][x] = inner
                g[y2][x] = inner


# ------------------------------------------------------------------ new pieces (palette 06 indices)
def carved_stone():
    """1x2 standing stone (16x32), 3/4 view: a slab whose rounded top is seen from above (lit, ~5 rows), a
    dark lip, a front face shaded lit-left / dark-right with a large incised diamond, a darker foot, and a
    shadow cast down-right on the grass."""
    g = [[0] * 16 for _ in range(32)]
    top = ["....KKKKKKKK....",
           "...K11111111K...",
           "..K1111111112K..",
           "..K1111111122K..",
           "..K2111111223K..",
           "..K2222222233K..",
           "..K5555555556K.."]
    for j, r in enumerate(top):
        g[1 + j] = art([r])[0]
    for y in range(8, 27):
        row = [0] * 16
        row[2], row[13] = L6["K"], L6["K"]
        body = shade_cols(10, y=y)
        body = [{2: L6["2"], 3: L6["3"], 4: L6["4"], 5: L6["5"]}[v] for v in body]
        if y == 8:
            body = [L6["4"] if checker(i, y) else L6["5"] for i in range(10)]
        elif y == 24:
            body = [L6["4"] if checker(i, y) else L6["5"] for i in range(10)]
        elif y >= 25:
            body = [L6["5"]] * 9 + [L6["6"]]
        row[3:13] = body
        g[y] = row
    g[27] = art(["..KKKKKKKKKKKKS."])[0]
    g[28] = art(["...SSSSSSSSSSSS."])[0]
    g[29] = art([".....SSSSSSSSS.."])[0]
    for y in range(22, 27):
        g[y][14] = L6["S"]
    diamond(g, 7, 15, 4, inner=L6["3"])
    return g


def pillar():
    """1x3 carved pillar standing in the lake (16x48), classic column in 3/4 view: a wide capital whose top
    is seen from above (lit slab, dark lip, short front band), a narrower shaft shaded lit-left / dark-right
    with an incised diamond and a ring groove, a wider base block, a dark wet band at the waterline and a
    ripple ring on the water. Light from the top-left; checker dither only at ramp steps."""
    g = [[0] * 16 for _ in range(48)]
    capital = ["...KKKKKKKKKK...",
               "..K1111111112K..",
               ".K111111111122K.",
               ".K111111111223K.",
               ".K211111112233K.",
               ".K555555555556K.",
               ".K233333344455K.",
               ".K333333444555K.",
               "..KKKKKKKKKKKK.."]
    for j, r in enumerate(capital):
        g[2 + j] = art([r])[0]
    for y in range(11, 39):
        row = [0] * 16
        row[3], row[12] = L6["K"], L6["K"]
        body = shade_cols(8, y=y)
        body = [{2: L6["2"], 3: L6["3"], 4: L6["4"], 5: L6["5"]}[v] for v in body]
        if y == 11:                                    # shadow of the capital on the shaft
            body = [L6["5"] if checker(i, y) else L6["6"] for i in range(8)]
        elif y == 12:
            body = [L6["4"] if checker(i, y) else L6["5"] for i in range(8)]
        elif y == 31:                                  # ring groove: shadowed line, lit lower edge
            body = [L6["5"]] * 7 + [L6["6"]]
        elif y == 32:
            body = [L6["1"]] + [L6["2"]] * 4 + [L6["3"], L6["3"], L6["4"]]
        row[4:12] = body
        g[y] = row
    base = ["..KKKKKKKKKKKK..",
            "..K2222222333K..",
            "..K3333344455K..",
            "..K5555555556K..",
            ".W.KKKKKKKKKK.W.",
            "WaW..........WaW",
            ".WWaW......WaWW.",
            "...WWWaaaaWWW..."]
    for j, r in enumerate(base):
        g[39 + j] = art([r])[0]
    diamond(g, 7, 22, 2, inner=L6["3"])
    return g


def plinth():
    """3x2 stone plinth (48x32) for the sphere object: a big top surface seen from above with a socket ring
    (where the sphere sits), dark lip, a front band with two incised diamonds, shadow down-right."""
    g = [[0] * 48 for _ in range(32)]
    W, x0, x1 = 48, 4, 43
    for y in range(5, 20):                       # top surface (rounded corners), lit from the top-left
        row = [0] * W
        inset = {5: 3, 6: 1}.get(y, 0)
        row[x0 + inset - 1] = L6["K"] if y > 5 else 0
        row[x1 - inset + 1] = L6["K"] if y > 5 else 0
        for x in range(x0 + inset, x1 - inset + 1):
            f = (x - x0) / (x1 - x0) * 0.6 + (y - 5) / 15 * 0.4
            v = "1" if f < 0.35 else ("1" if checker(x, y) else "2") if f < 0.45 else "2" if f < 0.7 else \
                ("2" if checker(x, y) else "3") if f < 0.8 else "3"
            row[x] = L6[v]
        g[y] = row
    for x in range(x0 + 3, x1 - 2):
        g[4][x] = L6["K"]
    g[5][x0 + 1] = g[5][x0 + 2] = L6["K"]
    g[5][x1 - 1] = g[5][x1 - 2] = L6["K"]
    # socket ring, an ellipse seen from above: inner far rim in shadow, near rim lit
    cx, cy, rx, ry = 23.5, 12.0, 9.5, 4.5
    for y in range(6, 19):
        for x in range(x0, x1 + 1):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if 0.70 <= d <= 1.15:
                g[y][x] = L6["5"] if y <= cy else L6["W"] if (y > cy + 2 and x < cx) else L6["2"]
            elif d < 0.70:
                g[y][x] = L6["4"] if y < cy - 1 else L6["3"]
    for y in range(20, 28):                      # lip + front band
        row = [0] * W
        row[x0 - 1] = row[x1 + 1] = L6["K"]
        for x in range(x0, x1 + 1):
            if y == 20:
                row[x] = L6["5"]
            elif y >= 26:
                row[x] = L6["5"] if y == 26 else L6["6"]
            else:
                f = (x - x0) / (x1 - x0)
                row[x] = L6["3"] if f < 0.5 else (L6["3"] if checker(x, y) else L6["4"]) if f < 0.62 else \
                    L6["4"] if f < 0.85 else (L6["4"] if checker(x, y) else L6["5"]) if f < 0.92 else L6["5"]
        g[y] = row
    g[28] = [0] * x0 + [L6["K"]] * (x1 - x0 + 1) + [0] * (W - x1 - 1)
    for y, (a, b) in ((26, (x1 + 2, x1 + 3)), (27, (x1 + 2, x1 + 3)), (28, (x1 + 1, x1 + 3))):
        for x in range(a, b + 1):
            g[y][x] = L6["S"]
    for x in range(x0 + 2, x1 + 4):
        g[29][x] = L6["S"]
    for x in range(x0 + 4, x1 + 3):
        g[30][x] = L6["S"]
    diamond(g, 13, 22, 2, inner=L6["3"])
    diamond(g, 34, 22, 2, inner=L6["4"])
    return g


def sphere_sprite(on=False):
    """32x32 OBJ sprite: the stone sphere (diameter 24), lit from the top-left, banded shading with a checker
    dither only on the band edges, outline dark on the shadow side, lighter on the lit side. Returns RGBA.
    on=True: the glowing palette (same indices, swapped OBJ palette at run time)."""
    stone = [(0, 0, 0), (232, 240, 248), (192, 204, 224), (152, 164, 192), (120, 132, 168), (88, 100, 136),
             (64, 72, 104), (40, 40, 64)]
    glow = [(0, 0, 0), (240, 255, 255), (168, 240, 248), (112, 208, 248), (72, 168, 232), (48, 120, 208),
            (32, 80, 168), (24, 40, 104)]
    pal = glow if on else stone
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = im.load()
    cx, cy, r = 15.5, 15.5, 11.6
    lx, ly, lz = -0.55, -0.6, 0.58
    n = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / n, ly / n, lz / n
    for y in range(32):
        for x in range(32):
            dx, dy = (x - cx) / r, (y - cy) / r
            d2 = dx * dx + dy * dy
            if d2 > 1.0:
                continue
            dz = math.sqrt(1 - d2)
            lum = max(0.0, dx * lx + dy * ly + dz * lz)          # 0..1
            t = (1 - lum) * 5.0                                    # 0 = brightest band
            band = int(t)
            fr = t - band
            if 0.42 < fr < 0.58 and band < 5:
                band += checker(x, y)                              # dither only at the band edge
            idx = 1 + min(5, band)
            edge = d2 > 0.80
            if edge:
                idx = 7 if (dx + dy) > -0.2 else max(idx, 5)      # outline: dark on the shadow side
            if on and d2 < 0.10 and dx < 0 and dy < 0:
                idx = 1
            px[x, y] = pal[idx] + (255,)
    return im


def sealed_door_cells(gen_tile):
    """The tomb dome's opening (General 0x064 above 0x0A7, dark slot 8) refilled with a carved slab.
    gen_tile(mid) -> 16x16 pal-03 index grid of a General metatile's bottom layer. Returns two grids in the
    same indices (they are drawn with palette 06, so the dome around them is blue-grey too)."""
    up, dn = gen_tile(0x064), gen_tile(0x0A7)
    g = up + dn                                   # 32 rows
    # the opening = slot-8 pixels connected to the door's interior
    seen, stack = set(), [(7, 20)]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < 16 and 0 <= y < 32) or g[y][x] != 8:
            continue
        seen.add((x, y))
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    ys = sorted({y for _, y in seen})
    top = ys[0]
    for (x, y) in seen:
        xs = sorted(xx for xx, yy in seen if yy == y)
        l, rgt = xs[0], xs[-1]
        f = (x - l) / max(1, rgt - l)
        if y - top < 2:
            v = L6["6"] if y == top else (L6["5"] if checker(x, y) else L6["6"])     # shadow under the arch
        elif x == l:
            v = L6["2"]                                                            # lit left jamb
        elif x == rgt:
            v = L6["6"]
        elif f < 0.45:
            v = L6["3"]
        elif f < 0.6:
            v = L6["3"] if checker(x, y) else L6["4"]
        elif f < 0.85:
            v = L6["4"]
        else:
            v = L6["4"] if checker(x, y) else L6["5"]
        g[y][x] = v
    # slab joint + incised diamond
    mid = (top + 2 + max(ys)) // 2
    diamond(g, 7, mid - 1, 2, inner=L6["3"])
    for x in range(16):
        if (x, max(ys) - 2) in seen:
            g[max(ys) - 2][x] = L6["5"]
    return g[:16], g[16:]


# ------------------------------------------------------------------ packing
class Bank:
    def __init__(self, free):
        self.free, self.used, self.lut = list(free), [], {}

    def add(self, t, pal):
        t = tuple(tuple(r) for r in t)
        if all(c == 0 for r in t for c in r):
            return 0
        if t not in self.lut:
            idx = self.free[len(self.used)]
            self.used.append((idx, t))
            h = tuple(r[::-1] for r in t)
            v = tuple(t[::-1])
            hv = tuple(r[::-1] for r in v)
            for f, bits in ((t, 0), (h, 0x400), (v, 0x800), (hv, 0xC00)):
                self.lut.setdefault(f, (512 + idx) | bits)
        return self.lut[t] | (pal << 12)


def quads(c):
    return [[row[qx * 8:qx * 8 + 8] for row in c[qy * 8:qy * 8 + 8]] for qy in (0, 1) for qx in (0, 1)]


def build(write=True):
    gmeta = read_u16(os.path.join(GENERAL, "metatiles.bin"))
    gattr = read_u16(os.path.join(GENERAL, "metatile_attributes.bin"))
    fmeta = read_u16(os.path.join(FORTREE, "metatiles.bin"))
    fattr = read_u16(os.path.join(FORTREE, "metatile_attributes.bin"))
    n_fortree = len(fattr)
    tiles = Image.open(os.path.join(FORTREE, "tiles.png"))
    gtiles = Image.open(os.path.join(GENERAL, "tiles.png"))
    assert tiles.mode == "P" and tiles.width == 128

    def gen_tile(mid):
        """16x16 indices of a General metatile's bottom layer."""
        out = [[0] * 16 for _ in range(16)]
        gp = gtiles.load()
        for k in range(4):
            e = gmeta[mid * 8 + k]
            t, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
            ox, oy = (t % 16) * 8, (t // 16) * 8
            for y in range(8):
                for x in range(8):
                    sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                    out[(k >> 1) * 8 + y][(k & 1) * 8 + x] = gp[ox + sx, oy + sy] & 15
        return out

    def entries(mid):
        if mid < 0x200:
            return gmeta[mid * 8:mid * 8 + 8], gattr[mid]
        i = mid - 0x200
        return fmeta[i * 8:i * 8 + 8], fattr[i]

    used_tiles = {e & 0x3FF for e in fmeta if (e & 0x3FF) >= 512}
    # free slots: the blank tail past Fortree's 493 tiles first, then Fortree tiles no metatile references
    free = [i for i in range(493, 512)] + [i for i in range(493) if 512 + i not in used_tiles]
    bank = Bank(free)
    meta = fmeta + [0] * ((FIRST_NEW - n_fortree) * 8)
    attr = fattr + [0] * (FIRST_NEW - n_fortree)
    ids = {}

    def add_meta(name, ents, at):
        ids[name] = 0x200 + len(attr)
        meta.extend(ents)
        attr.append(at)

    # 1 blue-grey rock copies (no new tiles)
    for m in ROCK_IDS:
        e, a = entries(m)
        add_meta("rock_%03X" % m, [(x & 0x0FFF) | (ROCK_PAL << 12) if (x >> 12) == 3 else x for x in e], a)

    # 1b drained foliage copies (no new tiles): palette 02 -> 07
    for m in DRAIN_IDS:
        e, a = entries(m)
        if all((x >> 12) == 2 or x == 0 for x in e):
            add_meta("drain_%03X" % m, [(x & 0x0FFF) | (DRAIN_PAL << 12) if x else 0 for x in e], a)

    grass = gmeta[0x001 * 8:0x001 * 8 + 4]
    water = gmeta[0x0A1 * 8:0x0A1 * 8 + 4]
    water_attr = gattr[0x0A1] & 0x0FFF

    def piece(name, grid, bottom, layer, behaviour=0, pal=ROCK_PAL):
        top = [bank.add(q, pal) for q in quads(grid)]
        add_meta(name, list(bottom) + top, behaviour | (layer << 12))
        if bottom is grass:      # a drained twin for the Power Spot rings (grass bottom on palette 07)
            add_meta(name + "_drained", [(x & 0x0FFF) | (DRAIN_PAL << 12) for x in bottom] + top,
                     behaviour | (layer << 12))

    # 2 rails: the existing Orchid kit pieces on grass (as install_area_kit.py does), palette 03 overlay
    rails = ER.build_pieces()
    for p in ("H", "HW", "HE"):
        piece("rail_" + p, rails[p], grass, COVERED, pal=ER.PAL)
    # 3 carved standing stone (top passable, drawn over sprites; bottom solid)
    cs = carved_stone()
    piece("stone_top", cut(cs, 0, 0), grass, NORMAL)
    piece("stone_bottom", cut(cs, 0, 1), grass, COVERED)
    # 4 lake pillar in water: top + middle surfable water drawn over sprites; base solid
    pl = pillar()
    piece("pillar_top", cut(pl, 0, 0), water, NORMAL, water_attr)
    piece("pillar_mid", cut(pl, 0, 1), water, NORMAL, water_attr)
    piece("pillar_base", cut(pl, 0, 2), water, COVERED, water_attr)
    # 5 sphere plinth 3x2 on grass (solid; the sphere is an object)
    pn = plinth()
    for cy in range(2):
        for cx in range(3):
            piece("plinth_%d%d" % (cx, cy), cut(pn, cx, cy), grass, COVERED)
    # 6 sealed dome door: full bottom-layer cells (dome rock + slab), palette 06
    up, dn = sealed_door_cells(gen_tile)
    for name, gcell, src in (("door_arch", up, 0x064), ("door_slab", dn, 0x0A7)):
        bottom = [bank.add(q, ROCK_PAL) for q in quads(gcell)]
        add_meta(name, bottom + [0, 0, 0, 0], gattr[src] & 0x0FFF)   # layer NORMAL, empty top (as vanilla)

    # tiles.png: Fortree's tiles + the new ones in free slots, 512 tiles
    im = Image.new("P", (128, 256), 0)
    im.putpalette(tiles.getpalette())
    im.paste(tiles, (0, 0))
    px = im.load()
    for idx, t in bank.used:
        for y in range(8):
            for x in range(8):
                px[(idx % 16) * 8 + x, (idx // 16) * 8 + y] = t[y][x]

    pals = [load_pal(os.path.join(FORTREE, "palettes", "%02d.pal" % i)) for i in range(16)]
    gp3 = load_pal(os.path.join(GENERAL, "palettes", "03.pal"))
    pals[ROCK_PAL] = [BLUEGREY.get(i, c) for i, c in enumerate(gp3)]
    gp2 = load_pal(os.path.join(GENERAL, "palettes", "02.pal"))
    pals[DRAIN_PAL] = [drained(c) for c in gp2]
    info = dict(metatiles=ids, n_metatiles=len(attr), fortree_metatiles=n_fortree,
                new_tiles=len(bank.used), tile_slots=[i for i, _ in bank.used], free_tiles_left=len(free) - len(bank.used),
                palettes={"06": "Holon rock (blue-grey copy of General 03) - was blank in Fortree",
                          "07": "drained foliage (General 02, greens strongly desaturated) - was blank",
                          "12": "free (blank)", "08-11": "Fortree's (desaturated greens in the desat variant)"})
    if write:
        os.makedirs(os.path.join(OUT, "palettes"), exist_ok=True)
        im.save(os.path.join(OUT, "tiles.png"))
        open(os.path.join(OUT, "metatiles.bin"), "wb").write(struct.pack("<%dH" % len(meta), *meta))
        open(os.path.join(OUT, "metatile_attributes.bin"), "wb").write(struct.pack("<%dH" % len(attr), *attr))
        for i, p in enumerate(pals):
            open(os.path.join(OUT, "palettes", "%02d.pal" % i), "w").write(jasc(p))
        json.dump(info, open(os.path.join(OUT, "holon_metatiles.json"), "w"), indent=1)
    return info


if __name__ == "__main__":
    info = build()
    print("metatiles: %d (Fortree %d), new tiles: %d, free tile slots left: %d"
          % (info["n_metatiles"], info["fortree_metatiles"], info["new_tiles"], info["free_tiles_left"]))
    for k, v in info["metatiles"].items():
        print("  0x%03X %s" % (v, k))
