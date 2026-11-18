#!/usr/bin/env python3
"""Pokémart exterior as a 24h convenience store: flat blue roof, white fascia with a tri-blue
stripe, sign box with the blue Poké Ball emblem, glass storefront, sliding door.

build() -> dict(under, over, palettes, door_col, props). Canvas 80x64 (5x4 tiles; vanilla Mart is 4x4); the bottom
row of tiles is the storefront the player walks up to (door at tile column `door_col`).
Props are separate 16x32 Arts that stand on the ground row in front of the building.
"""
from mock import Art, palette, check, save

W_PX, H_PX = 80, 64
DOOR_COL = 2

# ---- shared colours: the vanilla Mart's own greys and blues, plus glass and goods
INK, INK2 = (64, 72, 104), (96, 96, 120)
WHITE, LITE, MID, DARK = (248, 248, 248), (216, 224, 232), (184, 200, 224), (128, 128, 136)
SKY, BLUE, DEEP, NAVY = (112, 184, 240), (96, 160, 216), (80, 136, 192), (72, 112, 168)
G1, G2, G3 = LITE, (152, 200, 240), BLUE
YEL, RED, GRN, ORA = (248, 224, 120), (216, 104, 96), (112, 192, 128), (232, 144, 112)

# roof + fascia + sign
PAL_ROOF = palette(K=INK, q=INK2, W=WHITE, l=LITE, m=MID, d=DARK, s=SKY, b=BLUE, D=DEEP, n=NAVY)
# storefront: glass, goods seen through it, door
PAL_FRONT = palette(K=INK, q=INK2, W=WHITE, l=LITE, m=MID, d=DARK, a=G1, g=G2, G=G3, b=BLUE, n=NAVY,
                    s=SKY, Y=YEL, R=RED, E=GRN, O=ORA, i=(152, 176, 216))
# street props
PAL_PROP = palette(K=INK, W=WHITE, l=LITE, m=MID, d=DARK, s=SKY, b=BLUE, D=NAVY, a=G1, g=G2,
                   Y=YEL, R=RED, E=GRN, O=ORA, k=INK2)

BALL = """
...KKKKKK...
.KKssssssKK.
.KsWsssssbK.
KsWsssssssbK
KssssKKssbbK
KKKKKWWKKKKK
KWWWKWWKWWWK
KWWWWKKWWWlK
KWWWWWWWWWlK
.KWWWWWWWlK.
.KKWWWWllKK.
...KKKKKK...
"""


# Geometry. The building is a box with cut corners (like the vanilla Mart) seen in the Gen 3
# oblique view: depth runs up the screen, so the roof slab shows its top as an octagon, its front
# as a rectangle, and its two front corner faces as slanted parallelograms whose lower edge rises
# towards the outside. The walls repeat the same plan, set in 3px under the roof.
CW, CH = 8, 5        # a corner cut: 8 px across, 5 px of screen height
DECK_FRONT = 22      # roof top (seen from above) is y 0..22: about 1 part top to 2 parts front
BAND_H = 14          # height of the roof's front face (the sign band)
WALL_TOP = DECK_FRONT + BAND_H + 4
STRIPES = "llsssbbbnnnlll"      # the sign band, top to bottom
FACET = {"l": "m", "s": "b", "b": "D", "n": "n"}     # same band on a corner face, in shade


def deck_inset(y):
    if y < CH:
        return round((CH - y) * CW / CH)
    if y > DECK_FRONT - CH:
        return round((y - (DECK_FRONT - CH)) * CW / CH)
    return 0


def facet_top(k):
    """Top y of the band on a corner face, k = 0 at the outside edge .. CW-1 next to the front."""
    return DECK_FRONT - CH + round(k * CH / CW) + 1


def roof(a):
    """Roof top: pale parapet rim, deck in broad stripes (darker towards the sides), AC unit, hatch."""
    P = PAL_ROOF
    K, q, W, l, m, s, b, D = (P[k] for k in "KqWlmsbD")
    for y in range(0, DECK_FRONT + 1):
        x0, x1 = deck_inset(y), (W_PX - 1) - deck_inset(y)
        for x in range(x0, x1 + 1):
            edge = x in (x0, x1) or y == 0
            rim = x - x0 <= 2 or x1 - x <= 2 or y <= 2 or y >= DECK_FRONT - 1
            side = x - x0 < 12 or x1 - x < 12
            if edge:
                c = K
            elif rim:
                c = W if (y == 1 or x - x0 == 1) else l
            else:
                c = D if x % 4 == 3 else (b if side else s)
            a.put(x, y, c)
    for x in range(3, W_PX - 3):                     # shadow the far parapet casts on the deck
        if a.px[3][x] in (s, b):
            a.put(x, 3, D)
    # AC condenser: top + front face
    a.rect(13, 6, 28, 17, K)
    a.rect(14, 7, 27, 11, l)
    a.rect(14, 12, 27, 16, m)
    a.rect(16, 13, 20, 15, q)
    a.hline(23, 26, 14, q)
    # roof hatch
    hx = W_PX - 27
    a.rect(hx, 8, hx + 11, 16, K)
    a.rect(hx + 1, 9, hx + 10, 12, l)
    a.rect(hx + 1, 13, hx + 10, 15, m)


def fascia(a):
    """Front of the roof slab: the sign band with its tri-blue stripe. The corner faces carry the
    same band, slanted and in darker tones. The existing Mart emblem sits on a navy panel."""
    import vanilla
    from mock import from_image
    P = PAL_ROOF
    K, q, n = P["K"], P["q"], P["n"]
    y0 = DECK_FRONT + 1
    for x in range(CW, W_PX - CW):               # front face
        for i, ch in enumerate(STRIPES):
            a.put(x, y0 + i, P[ch])
        a.put(x, y0 + BAND_H, K)
        a.put(x, y0 + BAND_H + 1, q), a.put(x, y0 + BAND_H + 2, q)   # shadow on the wall below
    for k in range(CW):                        # corner faces
        yt = facet_top(k)
        for x in (k, (W_PX - 1) - k):
            for i, ch in enumerate(STRIPES):
                a.put(x, yt + i, P[FACET[ch]])
            a.put(x, yt + BAND_H, K)
            if k >= 3:                         # the walls are set in 3px
                a.put(x, yt + BAND_H + 1, q), a.put(x, yt + BAND_H + 2, q)
    a.vline(0, facet_top(0) - 1, facet_top(0) + BAND_H, K), a.vline((W_PX - 1), facet_top(0) - 1, facet_top(0) + BAND_H, K)
    a.vline(CW, y0, y0 + BAND_H - 1, q), a.vline((W_PX - 1) - CW, y0, y0 + BAND_H - 1, q)
    # sign panel + emblem, centred like the vanilla one
    x0, x1 = W_PX // 2 - 12, W_PX // 2 + 11
    a.rect(x0, y0 - 3, x1, y0 + BAND_H, K)
    a.rect(x0 + 1, y0 - 2, x1 - 1, y0 + BAND_H - 1, n)
    a.blit(from_image(vanilla.emblem("mart")), W_PX // 2 - 10, y0)


def window(a, x0, x1, goods):
    """A modest shop window: flat two-tone glass like the vanilla door, one reflection, a row of
    chunky goods on the sill."""
    P = PAL_FRONT
    y = WALL_TOP + 4
    a.rect(x0, y, x1, y + 9, P["q"])
    a.rect(x0 + 1, y + 1, x1 - 1, y + 3, P["b"])
    a.rect(x0 + 1, y + 4, x1 - 1, y + 8, P["s"])
    for k in range(4):
        a.hline(x1 - 6 - k, x1 - 4 - k, y + 1 + k, P["l"])
    x = x0 + 2
    for ch in goods:
        a.rect(x, y + 6, x + 2, y + 8, P[ch])
        x += 4
    a.hline(x0 - 1, x1 + 1, y + 10, P["l"])                     # sill


WALL_BASE = 63       # the wall's front base line


def storefront(a):
    """Walls, set in 3px under the roof: flat front in the vanilla wall grey, lighter angled corner
    faces whose base line rises towards the outside (the same slant as the roof's corner faces).
    The entrance has a small canopy over the door."""
    P = PAL_FRONT
    K, q, W, l, m, i = (P[k] for k in "KqWlmi")
    R = W_PX - 10
    a.rect(9, WALL_TOP - 8, R, WALL_BASE, K)                    # front face (top is under the roof)
    a.rect(9, WALL_TOP - 8, R, WALL_BASE - 1, m)
    a.hline(9, R, WALL_BASE - 6, q)
    a.rect(9, WALL_BASE - 5, R, WALL_BASE - 1, i)               # base band
    for side in (0, 1):                                         # angled corner faces
        for k in range(6):                                      # k = 0 at the outside
            x = 3 + k if side == 0 else W_PX - 4 - k
            yb = WALL_BASE - round((5 - k) * CH / CW)
            a.vline(x, WALL_TOP - 10, yb - 1, W if (side == 0 and 0 < k < 5) else l)
            a.put(x, yb - 1, i), a.put(x, yb - 2, i), a.put(x, yb - 3, i)
            a.put(x, yb, K)
            if k == 0:
                a.vline(x, WALL_TOP - 10, yb, K)
    window(a, 12, 27, "YRE")
    window(a, W_PX - 28, W_PX - 13, "ORY")
    # entrance on tile column 2: a canopy seen from above, and the door (vanilla Mart door width)
    # running down to the base line. No doorstep.
    x0, x1, top = 30, 49, WALL_TOP + 1
    a.rect(x0, top, x1, top + 6, K)                             # canopy
    a.rect(x0 + 1, top + 1, x1 - 1, top + 3, l)
    a.hline(x0 + 1, x1 - 1, top + 1, W)
    a.rect(x0 + 1, top + 4, x1 - 1, top + 5, P["n"])
    a.rect(32, top + 6, 47, WALL_BASE, K)                       # door
    a.rect(33, top + 7, 46, WALL_BASE - 1, P["b"])
    a.hline(33, 46, top + 7, q)                                 # canopy shadow on the glass
    a.rect(39, top + 8, 40, WALL_BASE - 1, q)                   # sliding-door split


def prop_ice_chest():
    """Chest freezer with sliding glass lids and a snowflake badge."""
    P = PAL_PROP
    a = Art(16, 32)
    a.rect(0, 13, 15, 31, P["K"])
    a.rect(1, 14, 14, 20, P["l"])
    a.rect(2, 15, 7, 19, P["g"]), a.rect(9, 15, 13, 19, P["g"])
    a.hline(2, 5, 16, P["a"]), a.hline(9, 11, 16, P["a"])
    a.put(4, 18, P["R"]), a.put(5, 18, P["Y"]), a.put(11, 18, P["E"]), a.put(12, 18, P["O"])
    a.vline(8, 14, 20, P["d"])
    a.rect(1, 21, 14, 29, P["W"])
    a.hline(1, 14, 21, P["m"])
    a.rect(1, 23, 14, 27, P["b"])
    a.hline(1, 14, 23, P["s"])
    a.stamp(P, """
..W..
W.W.W
.WWW.
W.W.W
..W..
""", 6, 23)
    a.hline(1, 14, 29, P["m"])
    a.rect(1, 30, 14, 30, P["d"])
    return a


def prop_vending():
    """Drinks vending machine."""
    P = PAL_PROP
    a = Art(16, 32)
    a.rect(1, 2, 14, 31, P["K"])
    a.rect(2, 3, 13, 5, P["s"])                                # top
    a.rect(2, 6, 13, 30, P["b"])
    a.hline(2, 13, 6, P["D"])
    a.rect(3, 8, 10, 20, P["K"])
    a.rect(4, 9, 9, 19, P["a"])
    for r, cols in enumerate(("RYE", "OER", "YRO")):
        y = 9 + r * 4
        for c, ch in enumerate(cols):
            a.rect(4 + c * 2, y, 5 + c * 2, y + 2, P[ch])
            a.put(4 + c * 2, y, P["W"])
        a.hline(4, 9, y + 3, P["m"]) if r < 2 else None
    a.rect(11, 9, 12, 10, P["W"])                              # coin panel
    a.put(12, 13, P["Y"]), a.put(11, 13, P["k"])
    a.rect(11, 15, 12, 16, P["k"])
    a.rect(3, 23, 12, 27, P["K"])
    a.rect(4, 24, 11, 26, P["k"])
    a.hline(4, 11, 24, P["d"])
    a.hline(2, 13, 22, P["s"])
    a.rect(2, 29, 13, 30, P["D"])
    return a


def prop_bin():
    P = PAL_PROP
    a = Art(16, 32)
    a.rect(3, 18, 12, 31, P["K"])
    a.rect(4, 19, 11, 21, P["l"])
    a.rect(5, 20, 10, 20, P["k"])
    a.rect(4, 22, 11, 30, P["E"])
    a.hline(4, 11, 22, P["K"])
    a.vline(4, 23, 30, P["Y"])
    a.rect(6, 25, 9, 27, P["W"])
    a.rect(7, 26, 8, 26, P["E"])
    a.hline(4, 11, 30, P["k"])
    a.put(3, 18, None), a.put(12, 18, None), a.put(3, 31, None), a.put(12, 31, None)
    return a


def build():
    under = Art(W_PX, H_PX)
    storefront(under)
    roof(under)
    fascia(under)
    over = Art(W_PX, H_PX)
    return dict(under=under, over=over, door_col=DOOR_COL,
                palettes={"mart_roof": PAL_ROOF, "mart_front": PAL_FRONT},
                prop_palettes={"mart_prop": PAL_PROP},
                props={"ice_chest": prop_ice_chest(), "vending": prop_vending(), "bin": prop_bin()})


if __name__ == "__main__":
    from town import Town

    m = build()
    check({"under": m["under"]}, m["palettes"], "mart exterior")
    check(m["props"], m["prop_palettes"], "mart props")

    t = Town(16, 11)
    for x in (0, 2, 12, 14):
        t.tree(x, 0)
    t.tree(0, 4), t.tree(14, 5)
    t.path(3, 7, 12, 8)
    t.path(0, 9, 15, 10)
    t.flowers([(2, 8), (13, 3), (1, 7)])
    st = t.stage()
    bx, by = 5, 3                                   # building's top-left tile
    st.add(m["under"], bx * 16, by * 16)
    ground = by + 4
    st.add(m["props"]["ice_chest"], (bx + 0) * 16, ground * 16 - 16)
    st.add(m["props"]["bin"], (bx + 1) * 16, ground * 16 - 16)
    st.add(m["props"]["vending"], (bx + 4) * 16, ground * 16 - 16)
    st.npc("brendan/walking.png", "brendan.pal", 1, bx + DOOR_COL, ground)
    st.npc("woman_1.png", "npc_1.pal", 2, bx + 5, ground + 1, hflip=True)
    st.npc("boy_1.png", "npc_3.pal", 0, bx - 1, ground + 2)
    print(save(st.render(), "mart_exterior_3x.png"))
    print(save(st.camera(bx + DOOR_COL, ground), "mart_exterior_cam_3x.png"))
