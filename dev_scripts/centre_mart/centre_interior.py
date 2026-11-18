#!/usr/bin/env python3
"""Pokemon Centre interior, Singapore flavour: Peranakan floor tiles with a Poke Ball mosaic,
white plaster wall over a red rail and a tile dado, jade shuttered windows, a marble-topped red
counter, kopitiam table and stools, a rattan bench, palms in porcelain pots and an orchid.
14 x 10 tiles. Two layers: `base` (wall + floor, opaque) and `top` (furniture and wall decor).

    python centre_interior.py      # writes out/centre_interior_3x.png, out/centre_interior_cam_3x.png
"""
import math

from mock import Art, Stage, palette, check, save

W_T, H_T = 14, 10
W_PX, H_PX = W_T * 16, H_T * 16
INK = (80, 80, 104)

FLOOR = palette(
    K=INK,
    F1=(248, 240, 216), F2=(240, 224, 192), F3=(232, 192, 160),          # tile, diamond, dots
    S1=(216, 208, 192), S2=(208, 192, 168), S3=(200, 164, 140),          # ... in shade
    q1=(248, 192, 176), q2=(232, 144, 136), qw=(248, 248, 240),          # Poke Ball mosaic
    r1=(248, 144, 112), r2=(224, 72, 64), r3=(176, 40, 48),              # door mat
)
WALL = palette(
    K=INK, W=(248, 248, 248), c1=(248, 240, 224), c2=(224, 212, 196),
    r2=(224, 72, 64), r3=(176, 40, 48), p=(248, 184, 176),
    j1=(152, 224, 192), j2=(72, 168, 136), j3=(40, 112, 96),
    y=(248, 224, 136), b1=(168, 112, 72), b2=(112, 72, 56), s=(168, 224, 248),
)
FURN = palette(
    K=INK, W=(248, 248, 248), l=(224, 228, 236), m=(184, 192, 208), d=(136, 144, 168),
    r1=(248, 144, 112), r2=(224, 72, 64), r3=(176, 40, 48),
    g1=(184, 224, 248), g2=(104, 176, 232), g3=(56, 112, 184),
    y=(248, 216, 96), o=(200, 152, 48),
)
DECO = palette(
    K=INK, W=(248, 248, 248), l=(216, 224, 232),
    y=(176, 232, 128), g=(112, 200, 104), v=(64, 152, 88), V=(40, 104, 72),
    U=(64, 112, 200), t=(240, 208, 144), T=(208, 160, 104),
    B=(168, 112, 72), b=(112, 72, 56), o=(184, 104, 208), r=(224, 72, 64),
)
PALETTES = {"centre_floor": FLOOR, "centre_wall": WALL, "centre_furniture": FURN, "centre_decor": DECO}
SHADE = {FLOOR["F1"]: FLOOR["S1"], FLOOR["F2"]: FLOOR["S2"], FLOOR["F3"]: FLOOR["S3"]}


# ------------------------------------------------------------------ base layer
def floor_px(x, y):
    fx, fy = x % 16, y % 16
    dist = abs(fx - 7.5) + abs(fy - 7.5)
    if 6 <= fx <= 9 and 6 <= fy <= 9:
        return FLOOR["F3"]
    if (fx < 2 or fx > 13) and (fy < 2 or fy > 13):
        return FLOOR["F3"]
    if dist <= 6:
        return FLOOR["F2"]
    return FLOOR["F1"]


def floor(a):
    a.fill(0, 32, W_PX - 1, H_PX - 1, lambda x, y: floor_px(x, y))
    # Poke Ball mosaic set into the floor in front of the counter
    cx, cy, rad = 111.5, 111.5, 21.3
    for y in range(int(cy - rad), int(cy + rad) + 2):
        for x in range(int(cx - rad), int(cx + rad) + 2):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy)
            if r > rad:
                continue
            if r > rad - 2 or abs(dy) < 2 and r > 6:
                col = FLOOR["q2"]
            elif r <= 6.6:
                col = FLOOR["q2"] if r > 4.2 else FLOOR["qw"]
            elif dy < 0:
                col = FLOOR["q1"]
            else:
                col = FLOOR["qw"]
            a.put(x, y, col)


def shade(a, x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < a.w and 0 <= y < a.h:
                a.px[y][x] = SHADE.get(a.px[y][x], a.px[y][x])


def floret(a, x, y, centre, petal):
    a.rect(x + 1, y, x + 2, y + 3, petal)
    a.rect(x, y + 1, x + 3, y + 2, petal)
    a.rect(x + 1, y + 1, x + 2, y + 2, centre)


def wall(a):
    c = WALL
    a.rect(0, 0, W_PX - 1, 31, c["c1"])
    a.rect(0, 0, W_PX - 1, 1, c["b2"])              # ceiling beam
    a.hline(0, W_PX - 1, 2, c["K"])
    a.hline(0, W_PX - 1, 3, c["c2"])
    a.hline(0, W_PX - 1, 20, c["r3"])               # red rail
    a.hline(0, W_PX - 1, 21, c["r2"])
    a.rect(0, 22, W_PX - 1, 27, c["W"])             # tile dado
    for i, x in enumerate(range(2, W_PX - 4, 8)):
        if i % 2 == 0:
            floret(a, x, 23, c["r2"], c["p"])
        else:
            floret(a, x, 23, c["j2"], c["j1"])
    a.hline(0, W_PX - 1, 28, c["b1"])               # timber skirting
    a.hline(0, W_PX - 1, 29, c["b1"])
    a.hline(0, W_PX - 1, 30, c["b2"])
    a.hline(0, W_PX - 1, 31, c["K"])


def mat(a):
    c = FLOOR
    x0, x1, y0, y1 = 98, 125, 147, 159
    a.rect(x0, y0, x1, y1, c["r3"])
    a.rect(x0 + 1, y0 + 1, x1 - 1, y1, c["r2"])
    a.frame(x0 + 3, y0 + 3, x1 - 3, y1 + 3, c["r1"])


# ------------------------------------------------------------------ wall decor (top layer)
def window(t, x0, y0):
    c = WALL
    x1, y1 = x0 + 25, y0 + 14
    t.rect(x0, y0, x1, y1, c["K"])
    t.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, c["s"])
    for lx in (x0 + 1, x1 - 6):                     # folded-back louvred shutters
        for y in range(y0 + 1, y1):
            t.hline(lx, lx + 5, y, c["j2"] if (y - y0) % 2 else c["j3"])
        t.hline(lx, lx + 5, y0 + 1, c["j1"])
    t.vline(x0 + 7, y0 + 1, y1 - 1, c["K"]), t.vline(x1 - 7, y0 + 1, y1 - 1, c["K"])
    t.vline(x0 + 12, y0 + 1, y1 - 1, c["W"]), t.vline(x0 + 13, y0 + 1, y1 - 1, c["W"])
    t.hline(x0 + 8, x1 - 8, y0 + 6, c["W"])
    t.rect(x0 + 9, y0 + 9, x0 + 10, y0 + 10, c["W"]), t.put(x0 + 11, y0 + 10, c["W"])   # cloud
    t.rect(x0 + 15, y0 + 3, x0 + 16, y0 + 3, c["W"])
    t.hline(x0 - 1, x1 + 1, y1 + 1, c["b1"])        # sill
    t.hline(x0 - 1, x1 + 1, y1 + 2, c["b2"])


def scroll(t, x0, y0):
    """Hanging scroll with an orchid."""
    c = WALL
    t.rect(x0, y0 + 1, x0 + 9, y0 + 15, c["W"])
    t.vline(x0, y0 + 1, y0 + 15, c["c2"]), t.vline(x0 + 9, y0 + 1, y0 + 15, c["c2"])
    t.hline(x0 - 1, x0 + 10, y0, c["b2"]), t.hline(x0 - 1, x0 + 10, y0 + 16, c["b2"])
    t.stamp({"j": c["j3"], "g": c["j2"], "r": c["r2"], "p": c["p"]}, """
...pp...
..prrp..
...pp.j.
.pp..j..
prrp.j..
.pp.jg..
...jg...
..jgg...
.gj.g...
..j.....
""", x0 + 1, y0 + 3)


def crest(t, x0, y0):
    c = WALL
    t.stamp({"K": c["K"], "r": c["r2"], "W": c["W"], "p": c["p"], "c": c["c2"]}, """
...KKKK...
.KKrrrrKK.
.KrprrrrK.
KrprrrrrrK
KrrrKKrrrK
KKKKWWKKKK
KWWWKKWWWK
.KWWWWWcK.
.KKWWWcKK.
...KKKK...
""", x0, y0)


def region_map(t, x0, y0):
    c = WALL
    t.rect(x0, y0, x0 + 25, y0 + 14, c["b2"])
    t.rect(x0 + 1, y0 + 1, x0 + 24, y0 + 13, c["b1"])
    t.rect(x0 + 2, y0 + 2, x0 + 23, y0 + 12, c["s"])
    t.stamp({"g": c["j2"], "l": c["j1"], "d": c["j3"], "r": c["r2"]}, """
....ll.........gg...
..llggg......lggg...
.lggggd.....lgggd...
.gggdd..ll..gggdd...
..gd...lggl..gd.....
......lggggd....lg..
.......gdrd....lggd.
........dd......gd..
""", x0 + 3, y0 + 3)


CABINET = """
.KKK..KKK..KKK..
.KWK..KjK..KrK..
.KWK..KjK..KrK..
KKKKKKKKKKKKKKKK
KBBBBBBBBBBBBBBK
KbbbbbbbbbbbbbbK
KBBBKBBBBKBBBBbK
KByBKBByBKBByBbK
KBBBKBBBBKBBBBbK
KbbbbbbbbbbbbbbK
KBBBKBBBBKBBBBbK
KByBKBByBKBByBbK
KBBBKBBBBKBBBBbK
KbbbbbbbbbbbbbbK
KBBBKBBBBKBBBBbK
KByBKBByBKBByBbK
KBBBKBBBBKBBBBbK
KbbbbbbbbbbbbbbK
KBBBBBBBBBBBBBBK
KBBBBBByyBBBBBBK
KBBBBBBBBBBBBBbK
KbbbbbbbbbbbbbbK
KKKKKKKKKKKKKKKK
"""


def cabinet(t, x0, ybot):
    """Medicine-hall drawer cabinet with jars on top."""
    c = WALL
    leg = {"K": c["K"], "B": c["b1"], "b": c["b2"], "y": c["y"], "W": c["W"], "j": c["j2"], "r": c["r2"]}
    rows = [r for r in CABINET.split("\n") if r.strip()]
    t.stamp(leg, CABINET, x0, ybot - len(rows) + 1)


# ------------------------------------------------------------------ furniture (top layer)
TABLET = """
..KKKKKKKKKKKK..
.KWWWWWWWWWWWWK.
.KWGGGGGGGGGGWK.
.KWGWWGyyGrrGWK.
.KWGWWGyyGrrGWK.
.KWGGGGGGGGGGWK.
.KWGggGWWGyyGWK.
.KWGggGWWGyyGWK.
.KWGGGGGGGGGGWK.
.KWWWWWWlWWWWlK.
..KKKKKKKKKKKK..
......KlmK......
......KlmK......
......KlmK......
......KlmK......
......KlmK......
....KKKlmKKK....
...KllllllmmK...
...KKKKKKKKKK...
"""


def tablet(t, x0, ybot):
    """Storage-system terminal as a touchscreen tablet on a slim stand."""
    c = FURN
    leg = {"K": c["K"], "W": c["W"], "l": c["l"], "m": c["m"], "G": c["g2"], "g": c["g1"],
           "y": c["y"], "r": c["r2"]}
    rows = [r for r in TABLET.split("\n") if r.strip()]
    t.stamp(leg, TABLET, x0, ybot - len(rows) + 1)


def vanilla_machine():
    """The existing healing machine, lifted pixel-for-pixel from gTileset_PokemonCenter (the four
    metatiles at (5..6, 1..2) of PokemonCenter_1F, without the wall and counter around them)."""
    import vanilla
    e, g, _ = vanilla.layout("LAYOUT_POKEMON_CENTER_1F", ref="upstream/master")
    sc = vanilla.Scene(e["primary_tileset"], e["secondary_tileset"])
    a = Art(32, 32)
    for ty in (1, 2):
        for tx in (5, 6):
            ent, _ = sc._meta(g[ty][tx])
            # row 1: top layer. row 2: top layer's upper half + bottom layer's lower half (the tray)
            for k in ((4, 5, 6, 7) if ty == 1 else (2, 3, 4, 5)):
                en = ent[k]
                tl, hf, vf, pal = en & 0x3FF, (en >> 10) & 1, (en >> 11) & 1, en >> 12
                ts, ti = (sc.p, tl) if tl < 512 else (sc.s, tl - 512)
                tile, q = ts.tile(ti), k & 3
                for y in range(8):
                    for x in range(8):
                        ci = tile[7 - y if vf else y][7 - x if hf else x]
                        if ci:
                            a.put((tx - 5) * 16 + (q & 1) * 8 + x, (ty - 1) * 16 + (q >> 1) * 8 + y,
                                  sc.pals[pal][ci])
    return a


# The fern + machine share one 15-colour palette slot; the pot's pale grey is one colour too many,
# so it snaps to the machine's near-identical grey (12 pixels, distance 16 in one channel).
PLANT_SNAP = {(200, 184, 192): (200, 200, 192)}


def vanilla_plant():
    """The existing potted fern from the vanilla Pokemon Center (metatiles at (1, 0..2) of the
    untouched PokemonCenter_1F), lifted pixel-for-pixel from its top layer: Gen 3 3/4 view with the
    pot rim seen from above. Returns (art 16x48, bottom row of the pot)."""
    import vanilla
    e, g, _ = vanilla.layout("LAYOUT_POKEMON_CENTER_1F", ref="upstream/master")
    sc = vanilla.Scene(e["primary_tileset"], e["secondary_tileset"])
    a = Art(16, 48)
    bottom = 0
    for ty in (0, 1, 2):                    # leaves on the wall rows, pot base on the floor row
        ent, _ = sc._meta(g[ty][1])
        for k in (4, 5, 6, 7):
            en = ent[k]
            tl, hf, vf, pal = en & 0x3FF, (en >> 10) & 1, (en >> 11) & 1, en >> 12
            ts, ti = (sc.p, tl) if tl < 512 else (sc.s, tl - 512)
            if pal < 6:
                continue                    # primary-palette tiles here are the vanilla wall trim, not the plant
            tile, q = ts.tile(ti), k & 3
            for y in range(8):
                for x in range(8):
                    ci = tile[7 - y if vf else y][7 - x if hf else x]
                    if ci:
                        py = ty * 16 + (q >> 1) * 8 + y
                        col = sc.pals[pal][ci]
                        a.put((q & 1) * 8 + x, py, PLANT_SNAP.get(col, col))
                        bottom = max(bottom, py)
    return a, bottom


def plant(t, tx, ty):
    """Vanilla potted fern standing on the bottom edge of tile (tx, ty)."""
    art, bottom = vanilla_plant()
    t.blit(art, tx * 16, ty * 16 + 14 - bottom)


BALL = """
..KKKK..
.KrrrrK.
KrprrrrK
KKKWWKKK
KWWKKWWK
.KWWWlK.
..KKKK..
"""


def counter(t):
    c = FURN
    x0, x1, y = 64, 159, 48
    # side returns (top-down marble slabs)
    for sx in (x0, x1 - 9):
        t.rect(sx, 34, sx + 9, y + 2, c["K"])
        t.rect(sx + 1, 35, sx + 8, y + 2, c["W"])
        t.vline(sx + 8, 35, y, c["l"])
    # top
    t.rect(x0, y, x1, y + 9, c["K"])
    t.rect(x0 + 1, y + 1, x1 - 1, y + 7, c["W"])
    t.rect(x0 + 1, y - 2, x0 + 8, y, c["W"]), t.rect(x1 - 8, y - 2, x1 - 1, y, c["W"])
    t.hline(x0 + 1, x1 - 1, y + 8, c["m"])
    for vx in (x0 + 20, x0 + 47, x0 + 70, x0 + 86):  # marble veining
        t.put(vx, y + 3, c["l"]), t.put(vx + 1, y + 4, c["l"]), t.put(vx + 2, y + 5, c["l"])
        t.put(vx + 3, y + 5, c["l"])
    # red front
    t.rect(x0 + 1, y + 10, x1 - 1, y + 14, c["r2"])
    t.hline(x0 + 1, x1 - 1, y + 10, c["r1"])
    t.hline(x0 + 1, x1 - 1, y + 14, c["r3"])
    for gx in range(x0 + 15, x1, 16):
        t.vline(gx, y + 11, y + 14, c["r3"])
        t.vline(gx + 1, y + 11, y + 13, c["r1"])
    t.hline(x0, x1, y + 15, c["K"])
    t.vline(x0, y, y + 15, c["K"]), t.vline(x1, y, y + 15, c["K"])
    # Poke Balls on the corners, a bell by the nurse
    leg = {"K": c["K"], "r": c["r2"], "p": c["r1"], "W": c["W"], "l": c["l"]}
    t.stamp(leg, BALL, x0 + 1, y - 1)
    t.stamp(leg, BALL, x1 - 8, y - 1)
    t.stamp({"K": c["K"], "y": c["y"], "o": c["o"], "W": c["W"]}, """
..KK..
.KyyK.
KyWyoK
KyyyoK
KKKKKK
""", 131, y + 1)


PALM = """
......v...g.....
..vg..vg.gy..v..
.vgyg.vgygy.vgv.
..vvgygyvgyvgyv.
.g.vvgygvgygvv..
vgygvvgyvgvvgygv
.vvgygvgvgvgyvv.
...vvgvvVvgvv.g.
.vg..vvgVgvv.gv.
..vv...vVv..vv..
.......VVV......
....KKKKKKKK....
....KWWUWWWK....
....KWUWUWlK....
....KUWWWUlK....
....KWWUWWlK....
.....KWUWlK.....
.....KKKKKK.....
"""
TABLE = """
..KKKKKKKKKKKK..
.KWWWWWWWWWWWWK.
KWWWWWWWWWWWWWWK
KWWWWWWWWWWWWWWK
KWWWWWWWWWWWWWWK
KWWWWWWWWWWWWWlK
KlWWWWWWWWWWWllK
.KllllllllllllK.
..KKKKKKKKKKKK..
......KbbK......
......KbbK......
....KKKbbKKK....
....KbbbbbbK....
....KKKKKKKK....
"""
STOOL = """
....KKKKKKKK....
..KKBBBBBBBBKK..
.KBBtTttTttTBBK.
.KBtTttTttTttBK.
.KBBtTttTttTBBK.
..KKBBBBBBBBKK..
..KbKKKKKKKKbK..
..KbK......KbK..
..KbK......KbK..
..KKK......KKK..
"""
CUP = """
.KKKK........
KbbbbKK.KKKK.
KWbbWKK.KTTBK
.KWWK...KTTBK
..KK....KKKK.
"""
ORCHID = """
......oo........
.....oWoo.......
......oo.v......
...oo...v.......
..ooWo..v.......
...oo..v........
.......v...oo...
......v...oWoo..
......v....oo...
.....gv..v......
....KKKKKKK.....
...KWVvgvVlK....
...KlWWWWWlK....
...KWUWUWUlK....
....KUWUWlK.....
.....KKKKK......
"""
SIDE_TABLE = """
..KKKKKKKKKKKK..
.KBBBBBBBBBBBBK.
.KBBBBBBBBBBBbK.
..KKKKKKKKKKKK..
....KbK..KbK....
....KbK..KbK....
....KbK..KbK....
....KKK..KKK....
"""


def bench(t, x0, y0):
    """Rattan bench, 32x21."""
    c = DECO
    t.rect(x0, y0, x0 + 31, y0 + 8, c["K"])
    t.rect(x0 + 1, y0 + 1, x0 + 30, y0 + 7, c["B"])
    for y in range(y0 + 2, y0 + 7):
        for x in range(x0 + 2, x0 + 30):
            t.put(x, y, c["t"] if (x + y) % 3 else c["T"])
    t.vline(x0 + 15, y0 + 1, y0 + 7, c["B"]), t.vline(x0 + 16, y0 + 1, y0 + 7, c["B"])
    t.rect(x0, y0 + 9, x0 + 31, y0 + 15, c["K"])
    t.rect(x0 + 1, y0 + 9, x0 + 30, y0 + 13, c["W"])            # cushion
    t.hline(x0 + 1, x0 + 30, y0 + 13, c["l"])
    t.hline(x0 + 1, x0 + 30, y0 + 14, c["r"])
    t.vline(x0 + 15, y0 + 9, y0 + 13, c["l"])
    t.rect(x0 + 1, y0 + 15, x0 + 30, y0 + 16, c["B"])
    t.hline(x0, x0 + 31, y0 + 17, c["K"])
    for lx in (x0, x0 + 28):
        t.rect(lx, y0 + 17, lx + 3, y0 + 20, c["K"])
        t.rect(lx + 1, y0 + 17, lx + 2, y0 + 19, c["b"])


def stamp_bottom(t, legend, text, tx, ty, dy=0):
    """Stamp a 16px-wide prop so it stands on the bottom edge of tile (tx, ty)."""
    rows = [r for r in text.split("\n") if r.strip()]
    t.stamp(legend, text, tx * 16, ty * 16 + 16 - len(rows) + dy)


URN = """
.....KKKK.....
....KlWWlK....
...KKKKKKKK...
...KWWlllTK...
...KWlllTTK...
...KWlllTTKKK.
...KWlllTTKlK.
...KWlllTTKKK.
...KWlllTTK...
...KKKKKKKK...
..KbBBBBBBbK..
..KKKKKKKKKK..
"""
JAR = """
.KKKK.
KrrrrK
.KKKK.
KWtTWK
KWTtWK
KWtTWK
.KKKK.
"""
MENU = """
KKKKKKKKKKKKKKKK
KbbbbbbbbbbbbbbK
KbWWWbbbTTTTbbbK
KbWbWWbbbbbbbbbK
KbWWWbbbTTTbbbbK
KbbbbbbbbbbbbbbK
KbttttbbTTTTbbbK
KbtTTtbbbbbbbbbK
KbttttbbTTTbbbbK
KbbbbbbbbbbbbbbK
KKKKKKKKKKKKKKKK
"""
TIN = """
KKKK
KccK
KccK
KccK
KKKK
"""
MUG = """
KKKK.
KWWKK
KWWKK
KKKK.
"""


def cafe(t, x0):
    """Kopi counter in the back-right corner: menu board and shelf on the wall, an urn behind a
    marble-topped timber counter, stools in front. x0 = left edge; runs to the right wall."""
    c = DECO
    x1 = W_PX - 1
    # wall: menu board (icons only) and a two-tier shelf of tins and cups
    t.stamp(c, MENU, x0 + 2, 5)
    sx0, sx1 = x0 + 21, x1 - 2
    for sy in (11, 18):
        t.hline(sx0, sx1, sy, c["B"])
        t.hline(sx0, sx1, sy + 1, c["b"])
    for i, col in enumerate(("r", "U", "T", "v")):
        t.stamp({"K": c["K"], "c": c[col]}, TIN, sx0 + 1 + i * 6, 6)
    for i in range(4):
        t.stamp(c, MUG, sx0 + 1 + i * 6, 14)
    # counter: return, marble top, timber front
    y = 48
    t.rect(x0, 34, x0 + 9, y + 2, c["K"])
    t.rect(x0 + 1, 35, x0 + 8, y + 2, c["W"])
    t.vline(x0 + 8, 35, y, c["l"])
    t.rect(x0, y, x1, y + 9, c["K"])
    t.rect(x0 + 1, y + 1, x1, y + 7, c["W"])
    t.rect(x0 + 1, y - 2, x0 + 8, y, c["W"])
    t.hline(x0 + 1, x1, y + 8, c["l"])
    t.rect(x0 + 1, y + 10, x1, y + 14, c["B"])
    t.hline(x0 + 1, x1, y + 10, c["T"])
    t.hline(x0 + 1, x1, y + 14, c["b"])
    for gx in range(x0 + 12, x1, 12):
        t.vline(gx, y + 11, y + 14, c["b"])
    t.hline(x0, x1, y + 15, c["K"])
    t.vline(x0, y, y + 15, c["K"])
    # on the counter: kopi and kaya toast, a biscuit jar; the urn stands behind
    t.stamp(c, CUP, x0 + 13, y + 2)
    t.stamp(c, JAR, x1 - 9, y - 1)
    t.stamp(c, URN, x1 - 15, 33)


def back_doorway(t, x0):
    """A plain timber-framed doorway in the back wall (Lavaridge: out to the hot springs)."""
    c = WALL
    t.rect(x0, 4, x0 + 15, 31, c["b2"])
    t.rect(x0 + 1, 5, x0 + 14, 31, c["b1"])
    t.rect(x0 + 3, 7, x0 + 12, 31, c["K"])
    t.hline(x0 + 3, x0 + 12, 31, c["c2"])


def build(back_door=False):
    base, top = Art(W_PX, H_PX), Art(W_PX, H_PX)
    floor(base)
    wall(base)
    mat(base)
    legend = dict(DECO)
    cafe_x = 11 * 16

    # wall decor
    if back_door:
        back_doorway(top, 32)
    else:
        window(top, 17, 4)           # x17 keeps its sill (1px wider) out of the fern's 8x8 column
        scroll(top, 141, 2)          # was x3, now behind the vanilla fern; moved to the old map spot
    crest(top, 115, 5)
    # (the wall region map was removed 2026-11-18: it looked interactive but isn't)

    # service area: vanilla healing machine, counter, medicine cabinet, tablet terminal
    top.blit(vanilla_machine(), 80, 16)
    counter(top)
    cabinet(top, 48, 46)
    tablet(top, 160, 46)

    # kopi cafe, back right
    cafe(top, cafe_x)
    for tx in (11, 13):
        stamp_bottom(top, legend, STOOL, tx, 4, dy=-2)
    stamp_bottom(top, legend, TABLE, 11, 7, dy=-1)
    top.stamp(legend, CUP, 11 * 16 + 2, 7 * 16 + 2)
    stamp_bottom(top, legend, STOOL, 10, 7, dy=-2)
    stamp_bottom(top, legend, STOOL, 12, 7, dy=-2)

    # waiting area, left
    plant(top, 0, 2)
    plant(top, 13, 9)
    bench(top, 1 * 16, 5 * 16 + 9)
    stamp_bottom(top, legend, SIDE_TABLE, 3, 6, dy=-1)
    top.stamp(legend, ORCHID, 3 * 16, 5 * 16 + 8)

    # baked floor shadows
    shade(base, 0, 32, W_PX - 1, 35)                    # under the wall
    shade(base, 64, 64, 161, 66)                        # in front of the counter
    shade(base, 160, 47, 175, 49)                       # tablet stand
    shade(base, 48, 47, 65, 49)                         # cabinet
    shade(base, cafe_x, 64, W_PX - 1, 66)               # cafe counter
    shade(base, 3, 47, 13, 49)
    shade(base, 13 * 16 + 3, 9 * 16 + 15, 13 * 16 + 13, 9 * 16 + 15)
    for tx, ty in ((11, 4), (13, 4), (10, 7), (11, 7), (12, 7)):
        shade(base, tx * 16 + 2, ty * 16 + 14, tx * 16 + 14, ty * 16 + 16)
    shade(base, 1 * 16 + 1, 6 * 16 + 14, 1 * 16 + 33, 6 * 16 + 16)
    shade(base, 3 * 16 + 3, 6 * 16 + 14, 3 * 16 + 14, 6 * 16 + 16)
    return dict(base=base, top=top, palettes=palettes_with_machine())


def palettes_with_machine():
    """Our four palettes plus the existing gTileset_PokemonCenter palette the machine uses."""
    cols = list(dict.fromkeys(c for art in (vanilla_machine(), vanilla_plant()[0]) for r in art.px for c in r if c))
    assert len(cols) <= 15, len(cols)
    pals = dict(PALETTES)
    pals["vanilla_pokemon_center"] = palette(**{f"c{i}": c for i, c in enumerate(cols)})
    return pals


def stage_scene():
    b = build()
    st = Stage.blank(W_T + 2, H_T + 1)
    st.add(b["base"], 16, 0)
    st.add(b["top"], 16, 0)
    ox = 1
    st.npc("nurse.png", "npc_1.pal", 0, ox + 7, 2)
    st.npc("brendan/walking.png", "brendan.pal", 1, ox + 7, 4)
    st.npc("old_man.png", "npc_4.pal", 0, ox + 12, 2)                  # kopi uncle
    st.npc("woman_1.png", "npc_1.pal", 1, ox + 11, 4, dy=-4)           # at the cafe counter
    st.npc("gentleman.png", "npc_3.pal", 2, ox + 12, 7, dy=-4)
    st.npc("little_girl.png", "npc_2.pal", 0, ox + 4, 8)
    return b, st


if __name__ == "__main__":
    b, st = stage_scene()
    check({"base": b["base"], "top": b["top"]}, b["palettes"], "centre interior")
    print(save(st.render(), "centre_interior_3x.png"))
    print(save(st.camera(8, 4), "centre_interior_cam_3x.png"))
