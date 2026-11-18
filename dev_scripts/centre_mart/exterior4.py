#!/usr/bin/env python3
"""Integration versions of the two exteriors: 4x4 tiles (the footprint every Centre and Mart has
on the maps) and drawn only with colours that exist in gTileset_General's palettes 0 and 1, the
palettes the vanilla Mart and Centre use. That lets them replace the vanilla buildings in every
town without touching map layouts or palettes.

    centre() / mart() -> dict(under=Art, over=Art)   # 64x64 each
        under: drawn below sprites.  over: drawn above sprites (Centre's facade over the walkway).

    python exterior4.py      # writes out/exterior4_5x.png (vanilla Centre/Mart beside the new ones)
"""
import os

from mock import Art, OUT, from_image

W = 64

# gTileset_General palette 1 (vanilla Centre) and palette 0 (vanilla Mart). Index 0 is transparent.
GREYS = dict(W=(248, 248, 248), l=(216, 224, 232), m=(184, 200, 224), s=(152, 176, 216),
             d=(128, 128, 136), k=(96, 96, 120), K=(64, 72, 104))
GLASS = dict(B=(96, 168, 232), b=(112, 184, 240))
RED = dict(p=(248, 184, 128), o=(232, 144, 112), r=(216, 104, 96), R=(200, 64, 80))
GREEN = (112, 192, 160)
BLUE = dict(s2=(112, 184, 240), b2=(96, 160, 216), D=(80, 136, 192), n=(72, 112, 168))
PAL1 = [None, GREYS["W"], GREYS["l"], GREYS["m"], GREYS["s"], GREYS["d"], GREYS["k"], GREYS["K"],
        (40, 48, 88), GLASS["b"], GLASS["B"], RED["p"], RED["o"], RED["r"], RED["R"], GREEN]
PAL0 = [None, GREYS["W"], GREYS["l"], GREYS["m"], GREYS["s"], GREYS["d"], GREYS["k"], GREYS["K"],
        (184, 184, 128), GLASS["b"], GLASS["B"], BLUE["s2"], BLUE["b2"], BLUE["D"], BLUE["n"], GREEN]


# Both buildings are drawn on a 16 px module that lines up with the 8x8 tile grid, and are
# left-right symmetric wherever they can be, so that most tiles repeat (or mirror) and the art
# fits in the few dozen tile slots the shared outdoor tileset can spare.

# ------------------------------------------------------------------ Pokemon Centre
SLOPE_BOTTOM, BAND_BOTTOM = 19, 26              # roof slope y 0..19, red band y 21..26
STOREY, FRONT_EDGE = 30, 38                     # upper storey y 30..37, overhang edge y 38
C_WALL, C_FLOOR = 39, 56                        # recessed wall y 39..55, walkway floor y 56..63
HIP = 8
C_DOOR_COL = 1                                  # the door is in the second of four arches


def centre():
    import vanilla
    c = dict(GREYS, **GLASS, **RED, g=GREEN)
    front, u, o = Art(W, W), Art(W, W), Art(W, W)

    # hipped tile roof: narrower at the ridge, end faces in shade
    for y in range(0, SLOPE_BOTTOM + 1):
        inset = max(0, HIP - y)
        for x in range(inset, W - inset):
            edge = x in (inset, W - 1 - inset) or y == 0
            dist = min(x, W - 1 - x) - HIP * (1 - y / SLOPE_BOTTOM)
            front.put(x, y, c["K"] if edge else c["o"] if dist < -0.5 else c["r"] if dist < 0.5
                      else c["r"] if x % 4 == 3 else c["p"])
    front.hline(1, W - 2, SLOPE_BOTTOM + 1, c["k"])
    front.rect(1, SLOPE_BOTTOM + 2, W - 2, BAND_BOTTOM, c["R"])          # solid red band
    front.hline(1, W - 2, BAND_BOTTOM, c["k"])
    front.vline(0, SLOPE_BOTTOM + 1, BAND_BOTTOM + 1, c["K"]), front.vline(W - 1, SLOPE_BOTTOM + 1, BAND_BOTTOM + 1, c["K"])
    front.hline(0, W - 1, BAND_BOTTOM + 1, c["K"])
    front.rect(0, BAND_BOTTOM + 2, W - 1, BAND_BOTTOM + 3, c["k"])       # eave shadow

    # raised centre section (two tiles wide) with the existing Centre emblem
    top = BAND_BOTTOM - 13
    front.hline(19, 44, top - 3, c["k"])
    front.hline(17, 46, top - 2, c["R"]), front.hline(17, 18, top - 2, c["k"]), front.hline(45, 46, top - 2, c["k"])
    front.rect(16, top - 1, 47, BAND_BOTTOM - 1, c["R"])
    front.vline(16, top - 1, SLOPE_BOTTOM + 1, c["k"]), front.vline(47, top - 1, SLOPE_BOTTOM + 1, c["k"])
    front.blit(from_image(vanilla.emblem("centre")).crop(0, 0, 20, 13), 22, top)

    # upper storey: one louvred shutter per module
    y0, y1 = STOREY, FRONT_EDGE - 1
    front.rect(0, y0, W - 1, y1, c["m"])
    for mx in range(0, W, 16):
        for x, ch in ((0, "l"), (1, "W"), (14, "W"), (15, "l")):       # pier, split across the joint
            front.vline(mx + x, y0, y1, c[ch])
        front.rect(mx + 3, y0 + 1, mx + 12, y1, c["K"])
        for y in range(y0 + 2, y1 + 1):
            front.hline(mx + 4, mx + 11, y, c["k"] if (y - y0) % 3 == 1 else c["g"])
        front.rect(mx + 7, y0 + 2, mx + 8, y1, c["K"])
    front.vline(0, y0, y1, c["K"]), front.vline(W - 1, y0, y1, c["K"])
    front.hline(0, W - 1, FRONT_EDGE, c["K"])

    # tile rows 0-1 sit behind sprites; the facade over the walkway (rows 2-3) draws over the player
    u.blit(front.crop(0, 0, W, 32))
    o.blit(front.crop(0, 32, W, 32), 0, 32)

    # recessed wall, in the shade of the upper storey
    g = C_WALL
    u.rect(0, 32, W - 1, C_FLOOR - 1, c["s"])
    u.rect(0, 32, W - 1, g + 2, c["k"])
    u.rect(0, g + 3, W - 1, g + 5, c["d"])
    for i, mx in enumerate(range(0, W, 16)):
        if i == C_DOOR_COL:                          # sliding glass door
            u.rect(mx + 2, g + 1, mx + 13, C_FLOOR - 1, c["K"])
            u.rect(mx + 3, g + 2, mx + 12, g + 4, c["k"])
            u.rect(mx + 3, g + 5, mx + 12, g + 10, c["B"])
            u.rect(mx + 3, g + 11, mx + 12, C_FLOOR - 1, c["b"])
            u.rect(mx + 7, g + 2, mx + 8, C_FLOOR - 1, c["k"])
        else:                                        # window
            u.rect(mx + 4, g + 4, mx + 11, g + 12, c["k"])
            u.rect(mx + 5, g + 5, mx + 10, g + 7, c["B"])
            u.rect(mx + 5, g + 8, mx + 10, g + 11, c["b"])
            u.hline(mx + 3, mx + 12, g + 13, c["l"])
    # walkway floor
    for y in range(C_FLOOR, C_FLOOR + 6):
        for x in range(W):
            u.put(x, y, c["l"] if (x // 4 + (y - C_FLOOR) // 3) % 2 else c["o"])
    for x in range(W):
        u.put(x, C_FLOOR, c["s"] if u.px[C_FLOOR][x] == c["l"] else c["r"])
    u.hline(0, W - 1, C_FLOOR + 6, c["l"])
    u.hline(0, W - 1, C_FLOOR + 7, c["K"])

    # piers and arches (over the player)
    for mx in range(0, W, 16):
        for x, ch in ((0, "l"), (1, "W"), (14, "W"), (15, "l")):
            o.vline(mx + x, g, 62, c[ch])
            o.put(mx + x, g + 5, c["s"]), o.put(mx + x, 59, c["s"]), o.put(mx + x, 63, c["K"])
        for k_, n in enumerate((3, 2, 1, 1)):
            y = g + k_
            o.hline(mx + 2, mx + 1 + n, y, c["l"]), o.hline(mx + 14 - n, mx + 13, y, c["l"])
            o.put(mx + 2 + n, y, c["k"]), o.put(mx + 13 - n, y, c["k"])
    o.vline(0, g, 63, c["K"]), o.vline(W - 1, g, 63, c["K"])
    return dict(under=u, over=o)


# ------------------------------------------------------------------ Pokemart
CW, CH = 8, 5              # a corner cut: 8 px across, 5 px of screen height
DECK_FRONT = 20            # roof top (seen from above) is y 0..20
BAND_H = 14                # the roof's front face: sign band y 21..34
WALL_TOP = DECK_FRONT + BAND_H + 4
STRIPES = "llsssbbbnnnlll"
FACET = {"l": "m", "s": "b", "b": "D", "n": "n"}
M_DOOR_COL = 1


def deck_inset(y):
    if y < CH:
        return round((CH - y) * CW / CH)
    if y > DECK_FRONT - CH:
        return round((y - (DECK_FRONT - CH)) * CW / CH)
    return 0


def facet_top(k):
    return DECK_FRONT - CH + round(k * CH / CW) + 1


def mart():
    import vanilla
    c = dict(GREYS, s=BLUE["s2"], b=BLUE["b2"], D=BLUE["D"], n=BLUE["n"], i=GREYS["s"], q=GREYS["k"])
    glass, sky = GLASS["B"], GLASS["b"]
    a = Art(W, W)
    K, q, Wh, l, m, i = c["K"], c["q"], c["W"], c["l"], c["m"], c["i"]
    R = W - 10

    # walls (drawn first; the roof overlaps their top): flat front, lighter angled corner faces
    a.rect(9, WALL_TOP - 8, R, 63, K)
    a.rect(9, WALL_TOP - 8, R, 62, m)
    a.hline(9, R, 57, q)
    a.rect(9, 58, R, 62, i)
    for k_ in range(6):
        yb = 63 - round((5 - k_) * CH / CW)
        for x in (3 + k_, W - 4 - k_):
            a.vline(x, WALL_TOP - 10, yb - 1, Wh if 0 < k_ < 5 else l)
            for j in range(1, 6):                      # base band and its dark line carry on round the corner
                a.put(x, yb - j, i)
            a.put(x, yb - 6, q)
            a.put(x, yb, K)
            if k_ == 0:
                a.vline(x, WALL_TOP - 10, yb, K)
    # one shop window right of the door: flat glass, a reflection, a row of chunky goods
    x0, x1, y = 40, 53, WALL_TOP + 4
    a.rect(x0, y, x1, y + 9, q)
    a.rect(x0 + 1, y + 1, x1 - 1, y + 3, glass)
    a.rect(x0 + 1, y + 4, x1 - 1, y + 8, sky)
    for k_ in range(4):
        a.hline(x1 - 6 - k_, x1 - 4 - k_, y + 1 + k_, l)
    for j, col in enumerate((RED["R"], RED["p"], GREEN)):
        a.rect(x0 + 2 + j * 4, y + 6, x0 + 4 + j * 4, y + 8, col)
    a.hline(x0 - 1, x1 + 1, y + 10, l)
    # door: exactly the bottom tile of column 1, under a small canopy
    dx = M_DOOR_COL * 16
    a.rect(dx - 2, 41, dx + 17, 47, K)
    a.rect(dx - 1, 42, dx + 16, 44, l)
    a.hline(dx - 1, dx + 16, 42, Wh)
    a.rect(dx - 1, 45, dx + 16, 46, c["n"])
    a.rect(dx, 47, dx + 15, 63, K)
    a.rect(dx + 1, 48, dx + 14, 62, glass)
    a.hline(dx + 1, dx + 14, 48, q)
    a.rect(dx + 7, 49, dx + 8, 62, q)

    # roof top: pale parapet rim, deck in broad stripes (darker towards the sides), two AC units
    for y in range(0, DECK_FRONT + 1):
        xa, xb = deck_inset(y), W - 1 - deck_inset(y)
        for x in range(xa, xb + 1):
            edge = x in (xa, xb) or y == 0
            rim = x - xa <= 2 or xb - x <= 2 or y <= 2 or y >= DECK_FRONT - 1
            side = x < 8 or x > W - 9
            a.put(x, y, K if edge else (Wh if (y == 1 or x - xa == 1 or xb - x == 1) else l) if rim
                  else c["D"] if x % 4 == 3 else (c["b"] if side else c["s"]))
    for x0 in (8, 40):                                            # AC condensers, one each side
        a.rect(x0, 8, x0 + 15, 15, K)
        a.rect(x0 + 1, 9, x0 + 14, 11, l)
        a.rect(x0 + 1, 12, x0 + 14, 14, m)
        a.rect(x0 + 6, 13, x0 + 9, 13, q)

    # front of the roof slab: sign band; corner faces carry it slanted and in shade
    y0 = DECK_FRONT + 1
    for x in range(CW, W - CW):
        for j, ch in enumerate(STRIPES):
            a.put(x, y0 + j, c[ch])
        a.put(x, y0 + BAND_H, K)
        a.put(x, y0 + BAND_H + 1, q), a.put(x, y0 + BAND_H + 2, q)
    for k_ in range(CW):
        yt = facet_top(k_)
        for x in (k_, W - 1 - k_):
            for j, ch in enumerate(STRIPES):
                a.put(x, yt + j, c[FACET[ch]])
            a.put(x, yt + BAND_H, K)
            if k_ >= 3:
                a.put(x, yt + BAND_H + 1, q), a.put(x, yt + BAND_H + 2, q)
    a.vline(0, facet_top(0) - 1, facet_top(0) + BAND_H, K), a.vline(W - 1, facet_top(0) - 1, facet_top(0) + BAND_H, K)
    a.vline(CW, y0, y0 + BAND_H - 1, q), a.vline(W - 1 - CW, y0, y0 + BAND_H - 1, q)
    a.rect(16, y0 - 3, 47, y0 + BAND_H, K)                                 # sign panel (two tiles wide)
    a.rect(17, y0 - 2, 46, y0 + BAND_H - 1, c["n"])
    a.blit(from_image(vanilla.emblem("mart")), 22, y0)
    return dict(under=a, over=Art(W, W))


def preview():
    import vanilla
    from PIL import Image
    sc, grid, under, over = vanilla.render("LAYOUT_OLDALE_TOWN")
    under.alpha_composite(over)
    gap = 8
    im = Image.new("RGBA", (64 * 4 + gap * 5, 64 + gap * 2), (112, 192, 160, 255))
    x = gap
    for kind in ("vc", "c", "vm", "m"):
        if kind in ("vc", "vm"):
            tx = 5 if kind == "vc" else 14
            im.paste(under.crop((tx * 16, 13 * 16, tx * 16 + 64, 17 * 16)), (x, gap))
        else:
            b = centre() if kind == "c" else mart()
            im.alpha_composite(b["under"].image(), (x, gap)), im.alpha_composite(b["over"].image(), (x, gap))
        x += 64 + gap
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "exterior4_5x.png")
    im.resize((im.width * 5, im.height * 5), Image.NEAREST).convert("RGB").save(p)
    return p


if __name__ == "__main__":
    for name, b, pals in (("centre", centre(), [PAL1]), ("mart", mart(), [PAL0, PAL1])):
        bad = 0
        for layer in ("under", "over"):
            a = b[layer]
            for ty in range(8):
                for tx in range(8):
                    cols = {a.px[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8)} - {None}
                    if cols and not any(cols <= set(p) for p in pals):
                        bad += 1
                        print(f"  {name} {layer} tile ({tx},{ty}) fits no palette: {sorted(cols - set(pals[0]))}")
        print(name, "palette errors:", bad)
    print(preview())
