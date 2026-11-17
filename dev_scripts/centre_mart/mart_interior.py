#!/usr/bin/env python3
"""Pokémart interior as a 24h convenience store (14x9 tiles, black void outside).

Two art layers, the way the metatiles would be built: `base` (floor, walls, counter and cabinet
shells; fully opaque inside the room) and `top` (goods, machines, furniture; transparent
elsewhere). Both draw under sprites. Four 15-colour palettes: floor, shell, goods, chill.
"""
from mock import Art, palette, check, Stage, save

W, H = 14, 9                       # tiles
PAD = 2                            # void tiles around the room in the previews

INK = (80, 80, 104)
WHITE, LITE, MID, DARK = (248, 248, 248), (216, 224, 232), (176, 184, 200), (128, 136, 160)
SKY, BLUE, DEEP, NAVY = (136, 192, 248), (72, 144, 216), (40, 88, 160), (32, 56, 120)
G1, G2, G3 = (208, 240, 248), (160, 216, 232), (104, 168, 200)
YEL, RED, GRN, ORA = (248, 216, 80), (232, 88, 72), (96, 192, 112), (248, 152, 64)
PUR, LPUR = (144, 104, 216), (200, 176, 248)
CREAM, BROWN = (248, 232, 184), (176, 120, 72)

PAL_FLOOR = palette(K=INK, f=(232, 240, 248), e=(208, 224, 240), c=(160, 200, 240),
                    F=(192, 208, 232), E=(168, 192, 224), C=(136, 168, 216),
                    W=WHITE, s=SKY, b=BLUE, D=DEEP, n=NAVY)
PAL_SHELL = palette(K=INK, W=WHITE, l=LITE, m=MID, d=DARK, s=SKY, b=BLUE, D=DEEP, n=NAVY,
                    a=G1, g=G2, G=G3, Y=YEL, R=RED)
PAL_GOODS = palette(K=INK, W=WHITE, l=LITE, m=MID, d=DARK, R=RED, Y=YEL, O=ORA, E=GRN,
                    P=PUR, p=LPUR, b=BLUE, s=SKY, C=CREAM, B=BROWN)
PAL_CHILL = palette(K=INK, W=WHITE, l=LITE, m=MID, d=DARK, a=G1, g=G2, G=G3, R=RED, Y=YEL,
                    E=GRN, O=ORA, b=BLUE, s=SKY, P=PUR)
PALETTES = {"mart_floor": PAL_FLOOR, "mart_shell": PAL_SHELL, "mart_goods": PAL_GOODS,
            "mart_chill": PAL_CHILL}

SHADE = {PAL_FLOOR["f"]: PAL_FLOOR["F"], PAL_FLOOR["e"]: PAL_FLOOR["E"],
         PAL_FLOOR["c"]: PAL_FLOOR["C"]}


def swap(text, mapping):
    return text.translate(str.maketrans(mapping))


# ------------------------------------------------------------------ small goods (ASCII)
BALL = """
..KKKK..
.KRRRRK.
KRWRRRRK
KRRRRRRK
KKKWWKKK
KWWWWWWK
.KWWWlK.
..KKKK..
"""
GREAT = swap(BALL, {"R": "b"}).replace(".KbbbbK.", ".KRbbRK.")
POTION = """
.dd...
.dWK..
..KK..
.KPPK.
KPpPPK
KPpPPK
KPWWPK
KPPPPK
.KKKK.
"""
SUPER = swap(POTION, {"P": "O", "p": "Y"})
BAG = """
.KKKKK.
KYYYYYK
KYWWWYK
KYWRWYK
KYWWWYK
KYYYYYK
KYYYYYK
KYYYYYK
.KKKKK.
"""
CUP = """
.KKKKK.
KWWWWWK
KKKKKKK
KRRRRRK
KWWWWWK
.KRRRK.
.KRRRK.
..KKK..
"""
CARTON = """
..KK..
.KWWK.
KWWWWK
KEEEEK
KEWWEK
KEWWEK
KEEEEK
KEEEEK
KKKKKK
"""
BOTTLE = """
.WW.
cccc
cWcc
cccc
cccc
"""
CAN = """
llll
cccc
cWWc
cccc
cccc
"""
CLOCK = """
...KKKK...
.KKWWWWKK.
.KWWWKWWK.
KWWWWKWWWK
KWWWWKWWWK
KWWWWRRRWK
KWWWWWWWWK
.KWWWWWWK.
.KKWWWWKK.
...KKKK...
"""
REGISTER = """
....KKKKKKK.
....KssssWK.
....KsssssK.
.KKKKKKKKKK.
.KlllllllmK.
.KlKlKlKlmK.
.KlllllllmK.
.KlKlKlKlmK.
KKKKKKKKKKKK
KmmmmmmmmmmK
KmmmKKKKmmmK
KddddddddddK
KKKKKKKKKKKK
"""
BUN = """
.WWWW.
WWWWWC
WWCCCC
"""


# ------------------------------------------------------------------ base layer
def floor_px(x, y):
    P = PAL_FLOOR
    fx, fy = x % 16, y % 16
    dx, dy = min(fx, 16 - fx), min(fy, 16 - fy)
    if dx + dy <= 2:
        return P["c"]                                   # pale blue diamond on the tile corners
    if fx == 0 or fy == 0:
        return P["e"]                                   # grout
    if 3 <= fx <= 13 and 3 <= fy <= 13 and (fx == 13 or fy == 13):
        return P["e"]                                   # bevel on the tile face
    return P["f"]


def shade(a, x0, y0, x1, y1):
    for y in range(max(0, y0), min(a.h, y1 + 1)):
        for x in range(max(0, x0), min(a.w, x1 + 1)):
            a.px[y][x] = SHADE.get(a.px[y][x], a.px[y][x])


def wall(a, x0, x1):
    P = PAL_SHELL
    a.rect(x0, 0, x1, 31, P["W"])
    a.hline(x0, x1, 0, P["K"])
    a.hline(x0, x1, 1, P["m"])
    a.rect(x0, 4, x1, 5, P["s"])
    a.rect(x0, 7, x1, 8, P["b"])
    a.rect(x0, 10, x1, 11, P["n"])
    a.rect(x0, 25, x1, 26, P["l"])
    a.hline(x0, x1, 27, P["d"])
    a.rect(x0, 28, x1, 30, P["m"])
    a.hline(x0, x1, 28, P["l"])
    a.hline(x0, x1, 31, P["K"])


def chiller_door(a, x, kinds, first=False):
    """One glass door of the drinks chiller (16x32). kinds = three (shape, colour) shelves."""
    P = PAL_CHILL
    a.rect(x, 0, x + 15, 31, P["K"])
    a.rect(x + 1, 1, x + 15, 4, P["l"])                  # lit header strip
    a.rect(x + 1, 2, x + 15, 3, P["s"])
    a.hline(x + 1, x + 15, 3, P["b"])
    a.vline(x + 1, 6, 27, P["l"])
    a.rect(x + 2, 6, x + 15, 27, P["g"])
    a.hline(x + 2, x + 15, 6, P["G"])
    for t, (shape, col) in enumerate(kinds):
        y = 8 + t * 7
        for i in range(3):
            a.stamp({**P, "c": P[col]}, shape, x + 2 + i * 5, y)
        a.hline(x + 2, x + 15, y + 5, P["W"])
        if t < 2:
            a.hline(x + 2, x + 15, y + 6, P["G"])
    for i in range(10):                                  # reflection, glass pixels only
        for dx in (0, 1):
            px, py = x + 12 - i // 2 + dx, 7 + i
            if a.px[py][px] == P["g"]:
                a.px[py][px] = P["a"]
    a.rect(x + 1, 28, x + 15, 30, P["d"])
    a.hline(x + 1, x + 15, 28, P["m"])
    for vx in range(x + 3, x + 14, 3):
        a.put(vx, 30, P["K"])


def counter(a):
    """Checkout counter: row 3, cols 0-3, with a return up the east end (3,2)."""
    P = PAL_SHELL
    y = 48
    a.rect(0, y, 63, y + 15, P["K"])
    a.rect(0, y + 1, 62, y + 7, P["s"])
    a.hline(0, 62, y + 1, P["W"])
    a.hline(0, 62, y + 7, P["b"])
    a.rect(0, y + 9, 62, y + 14, P["W"])
    a.hline(0, 62, y + 10, P["s"])
    a.rect(0, y + 11, 62, y + 12, P["b"])
    a.hline(0, 62, y + 13, P["n"])
    a.hline(0, 62, y + 14, P["l"])
    # return: a top-down slab at (3,2)
    a.rect(48, 32, 63, 48, P["K"])
    a.rect(49, 33, 62, 48, P["s"])
    a.vline(49, 33, 55, P["W"])
    a.vline(62, 33, 55, P["b"])
    a.hline(50, 61, 49, P["W"])
    for sx in (15, 31):                                  # seams on the counter top
        a.vline(sx, y + 2, y + 6, P["b"])


def base_layer():
    a = Art(W * 16, H * 16)
    a.fill(0, 32, W * 16 - 1, H * 16 - 1, floor_px)
    wall(a, 0, W * 16 - 1)
    drinks = [((BOTTLE, "R"), (CAN, "Y"), (BOTTLE, "E")),
              ((CAN, "b"), (BOTTLE, "O"), (CAN, "R")),
              ((BOTTLE, "P"), (CAN, "E"), (BOTTLE, "Y")),
              ((CAN, "O"), (BOTTLE, "b"), (CAN, "P")),
              ((BOTTLE, "E"), (CAN, "R"), (BOTTLE, "O")),
              ((CAN, "Y"), (BOTTLE, "P"), (CAN, "b"))]
    for i, kinds in enumerate(drinks):
        chiller_door(a, (5 + i) * 16, kinds)
    a.vline(11 * 16, 0, 31, PAL_SHELL["K"])
    counter(a)
    # entrance mat, cols 6-7 on the bottom row
    P = PAL_FLOOR
    a.rect(97, 131, 126, 143, P["D"])
    a.rect(98, 132, 125, 143, P["b"])
    a.frame(100, 134, 123, 146, P["s"])
    a.rect(98, 132, 125, 132, P["s"])
    # baked shadows: under the wall, under the counter, right of / below furniture
    shade(a, 0, 32, W * 16 - 1, 36)
    shade(a, 0, 64, 67, 67), shade(a, 64, 37, 67, 67)
    for gx in (5, 9):
        shade(a, gx * 16 + 48, 4 * 16 + 6, gx * 16 + 51, 6 * 16 + 3)
        shade(a, gx * 16 + 4, 6 * 16, gx * 16 + 51, 6 * 16 + 3)
    shade(a, 10 * 16 + 32, 7 * 16 + 4, 10 * 16 + 35, 8 * 16 + 3)
    shade(a, 10 * 16 + 4, 8 * 16, 10 * 16 + 35, 8 * 16 + 3)
    shade(a, 4 * 16 + 15, 7 * 16 + 6, 4 * 16 + 18, 8 * 16 + 2)
    shade(a, 4 * 16 + 4, 8 * 16, 4 * 16 + 18, 8 * 16 + 2)
    return a


# ------------------------------------------------------------------ top layer
def gondola(a, x, y, tier1, tier2):
    """Shelf run, 48x32: light top cap, two tiers of goods facing the camera."""
    P = PAL_GOODS
    a.rect(x, y, x + 47, y + 31, P["K"])
    a.rect(x + 1, y + 1, x + 46, y + 4, P["l"])
    a.hline(x + 1, x + 46, y + 1, P["W"])
    for t, goods in enumerate((tier1, tier2)):
        y0 = y + 6 + t * 12
        a.rect(x + 1, y0, x + 46, y0 + 8, P["l"])
        a.hline(x + 1, x + 46, y0, P["m"])
        gx = x + 2
        for g in goods:
            rows = [r for r in g.split("\n") if r.strip()]
            a.stamp(P, g, gx, y0 + 9 - len(rows))
            gx += len(rows[0]) + 1
        a.hline(x + 1, x + 46, y0 + 9, P["W"])
        a.hline(x + 1, x + 46, y0 + 10, P["m"])
        if t == 0:
            a.hline(x + 1, x + 46, y0 + 11, P["d"])
    a.hline(x + 1, x + 46, y + 29, P["d"])
    a.hline(x + 1, x + 46, y + 30, P["d"])


def frozen_drinks(a, x):
    """Twin-barrel frozen-drink machine against the back wall (16x32)."""
    P = PAL_GOODS
    a.rect(x + 1, 4, x + 14, 31, P["K"])
    a.rect(x + 2, 5, x + 13, 6, P["d"])                  # lids
    a.hline(x + 2, x + 13, 5, P["m"])
    for bx, c1, c2 in ((x + 2, "s", "b"), (x + 9, "R", "O")):
        a.rect(bx, 7, bx + 4, 16, P["W"])                # clear barrel
        a.rect(bx, 9, bx + 4, 16, P[c1])                 # slush
        a.hline(bx, bx + 4, 9, P["W"]) if c1 == "R" else a.hline(bx, bx + 4, 9, P["W"])
        a.vline(bx + 4, 10, 16, P[c2])
        a.vline(bx + 1, 11, 14, P["W"])                  # shine
        a.hline(bx, bx + 4, 7, P["l"])
    a.rect(x + 7, 5, x + 8, 16, P["K"])
    a.hline(x + 2, x + 13, 17, P["K"])
    a.rect(x + 2, 18, x + 13, 21, P["l"])
    a.hline(x + 2, x + 13, 18, P["W"])
    for nx in (x + 4, x + 11):                           # taps
        a.rect(nx, 18, nx, 20, P["K"])
    a.rect(x + 2, 22, x + 13, 23, P["d"])                # drip tray
    a.hline(x + 2, x + 13, 24, P["K"])
    a.rect(x + 2, 25, x + 13, 30, P["W"])
    a.hline(x + 2, x + 13, 26, P["s"])
    a.rect(x + 2, 27, x + 13, 28, P["b"])
    a.hline(x + 2, x + 13, 30, P["m"])


def magazine_rack(a, x):
    """Two tiers of magazines against the back wall (32 wide, drawn from y=9)."""
    P = PAL_GOODS
    a.rect(x + 1, 9, x + 30, 31, P["K"])
    a.rect(x + 2, 10, x + 29, 30, P["m"])
    covers = ["RY", "bW", "EY", "OW", "PY", "Yb", "sR", "RW"]
    for t in range(2):
        y0 = 11 + t * 10
        for i in range(4):
            mx = x + 3 + i * 7
            c, k = covers[t * 4 + i]
            a.rect(mx, y0, mx + 5, y0 + 7, P[c])
            a.rect(mx, y0, mx + 5, y0 + 1, P["W"])
            a.rect(mx + 1, y0 + 3, mx + 3, y0 + 5, P[k])
        a.hline(x + 2, x + 29, y0 + 8, P["W"])
        a.hline(x + 2, x + 29, y0 + 9, P["d"])


def atm(a, x):
    P = PAL_SHELL
    a.rect(x + 1, 7, x + 14, 31, P["K"])
    a.rect(x + 2, 8, x + 13, 10, P["s"])
    a.rect(x + 2, 11, x + 13, 30, P["b"])
    a.hline(x + 2, x + 13, 11, P["D"])
    a.rect(x + 3, 13, x + 12, 20, P["K"])
    a.rect(x + 4, 14, x + 11, 19, P["a"])
    a.rect(x + 5, 15, x + 8, 16, P["g"]), a.hline(x + 5, x + 10, 18, P["g"])
    a.rect(x + 4, 22, x + 9, 24, P["l"])
    for kx in (x + 4, x + 6, x + 8):
        a.put(kx, 23, P["d"])
    a.rect(x + 11, 22, x + 12, 23, P["Y"])
    a.hline(x + 4, x + 11, 26, P["K"])
    a.rect(x + 2, 28, x + 13, 30, P["D"])


def back_shelf(a, x, items):
    """Small wall shelf behind the counter with two tiers of goods."""
    P = PAL_GOODS
    a.rect(x + 1, 13, x + 14, 30, P["K"])
    a.rect(x + 2, 14, x + 13, 29, P["l"])
    for t, g in enumerate(items):
        rows = [r for r in g.split("\n") if r.strip()]
        yb = 21 + t * 9
        w = len(rows[0])
        n = 2 if w <= 6 else 1
        for i in range(n):
            a.stamp(P, g, x + 2 + i * (w + (12 - n * w)), yb - len(rows))
        a.hline(x + 2, x + 13, yb, P["W"])
        if t == 0:
            a.hline(x + 2, x + 13, yb + 1, P["m"])


def warmer(a, x, y):
    """Hot-snack case on the counter: lamp hood, two shelves of steamed buns."""
    P = PAL_GOODS
    a.rect(x, y, x + 13, y + 16, P["K"])
    a.rect(x + 1, y + 1, x + 12, y + 2, P["R"])
    a.hline(x + 1, x + 12, y + 1, P["O"])
    a.hline(x + 1, x + 12, y + 3, P["K"])
    a.rect(x + 1, y + 4, x + 12, y + 13, P["O"])
    a.hline(x + 1, x + 12, y + 4, P["Y"])
    for sy in (y + 5, y + 10):
        a.stamp(P, BUN, x + 1, sy)
        a.stamp(P, BUN, x + 7, sy)
        a.hline(x + 1, x + 12, sy + 3, P["B"])
    a.rect(x + 1, y + 14, x + 12, y + 15, P["m"])
    a.hline(x + 1, x + 12, y + 14, P["K"])


def coffee(a, x, y):
    P = PAL_GOODS
    a.rect(x, y, x + 11, y + 13, P["K"])
    a.rect(x + 1, y + 1, x + 10, y + 3, P["l"])
    a.rect(x + 1, y + 4, x + 10, y + 12, P["d"])
    a.hline(x + 1, x + 10, y + 4, P["m"])
    a.rect(x + 2, y + 6, x + 7, y + 11, P["K"])
    a.rect(x + 4, y + 8, x + 5, y + 10, P["W"])          # cup
    a.put(x + 9, y + 6, P["R"]), a.put(x + 9, y + 8, P["E"])


def freezer(a, x, y):
    """Chest freezer, 32x16: sliding glass lids over ice creams."""
    P = PAL_CHILL
    a.rect(x, y, x + 31, y + 15, P["K"])
    a.rect(x + 1, y + 1, x + 30, y + 9, P["l"])
    a.hline(x + 1, x + 30, y + 1, P["W"])
    for i, cols in enumerate(("REYO", "OPEs")):
        lx = x + 2 + i * 14
        a.rect(lx, y + 2, lx + 13, y + 8, P["G"])
        a.rect(lx + 1, y + 3, lx + 12, y + 7, P["g"])
        for j, ch in enumerate(cols[:3]):
            a.rect(lx + 1 + j * 4, y + 5, lx + 3 + j * 4, y + 7, P[ch])
        a.hline(lx + 1, lx + 5, y + 3, P["a"])
        a.put(lx + 12, y + 5, P["d"])                    # handle
    a.hline(x + 1, x + 30, y + 10, P["K"])
    a.rect(x + 1, y + 11, x + 30, y + 14, P["W"])
    a.hline(x + 1, x + 30, y + 12, P["s"])
    a.hline(x + 1, x + 30, y + 13, P["b"])
    a.hline(x + 1, x + 30, y + 14, P["m"])


def baskets(a, x, y):
    P = PAL_FLOOR
    a.rect(x + 1, y + 2, x + 14, y + 15, P["K"])
    a.rect(x + 2, y + 3, x + 13, y + 7, P["D"])
    a.frame(x + 2, y + 3, x + 13, y + 7, P["s"])
    for by in (y + 9, y + 11, y + 13):
        a.hline(x + 2, x + 13, by, P["b"])
        a.hline(x + 2, x + 13, by + 1, P["D"])
    a.rect(x + 6, y + 4, x + 9, y + 4, P["W"])          # handle


def top_layer():
    a = Art(W * 16, H * 16)
    G = PAL_GOODS
    back_shelf(a, 0, (BALL, POTION))
    a.stamp(G, CLOCK, 19, 14)
    back_shelf(a, 32, (GREAT, SUPER))
    frozen_drinks(a, 64)
    magazine_rack(a, 11 * 16)
    atm(a, 13 * 16)
    # counter props
    warmer(a, 1, 39)
    a.stamp(G, REGISTER, 34, 43)
    coffee(a, 50, 30)
    a.stamp(G, BALL, 52, 47)
    a.rect(20, 51, 27, 53, G["s"]), a.frame(20, 51, 27, 53, G["K"])   # scanner pad
    yel, red, grn = BAG, swap(BAG, {"Y": "R", "R": "Y"}), swap(BAG, {"Y": "E"})
    gondola(a, 5 * 16, 4 * 16, [BALL, BALL, BALL, GREAT, GREAT],
            [POTION, POTION, POTION, SUPER, SUPER, swap(POTION, {"P": "E", "p": "Y"})])
    gondola(a, 9 * 16, 4 * 16, [yel, red, grn, yel, red],
            [CUP, CUP, CARTON, CARTON, swap(CARTON, {"E": "b"}), CUP])
    freezer(a, 10 * 16, 7 * 16)
    baskets(a, 4 * 16, 7 * 16)
    return a


def build():
    return dict(base=base_layer(), top=top_layer(), palettes=PALETTES, size=(W, H))


if __name__ == "__main__":
    m = build()
    check({"base": m["base"], "top": m["top"]}, PALETTES, "mart interior")
    st = Stage.blank(W + 2 * PAD, H + 2 * PAD)
    st.add(m["base"], PAD * 16, PAD * 16)
    st.add(m["top"], PAD * 16, PAD * 16)

    def npc(png, pal, frame, tx, ty, hflip=False):
        st.npc(png, pal, frame, tx + PAD, ty + PAD, hflip)

    npc("mart_employee.png", "npc_1.pal", 0, 1, 2)
    npc("brendan/walking.png", "brendan.pal", 1, 1, 4)
    npc("girl_1.png", "npc_2.pal", 1, 8, 2)
    npc("youngster.png", "npc_1.pal", 1, 12, 2)
    npc("gentleman.png", "npc_3.pal", 2, 9, 7, hflip=True)
    full = st.render()
    print(save(full.crop((16, 16, full.width - 16, full.height - 16)), "mart_interior_3x.png"))
    print(save(st.camera(1 + PAD + 3, 4 + PAD), "mart_interior_cam_3x.png"))
