#!/usr/bin/env python3
"""Pokemon Centre exterior as a Singapore shophouse, drawn in the vanilla Emerald building idiom.

Proportions follow the vanilla Centre (64 px tall: about 1 part roof seen from above to 2 parts
front elevation): a hipped tile roof 20 px deep, a solid red band carrying the existing Centre
emblem on a raised centre section, a 2 px eave shadow, a squat shuttered upper storey, and the
five-foot way (a covered walkway the player walks under to reach the door).
Colours: the vanilla Centre's own 11, plus two jade and two door blues = one palette.

5 tiles wide x 4 tall. Tile rows 2-3 hold the walkway; the facade in front of it (upper storey,
columns, arches) is the over-the-player layer.

    python centre_exterior.py      # writes out/centre_exterior_3x.png, out/centre_exterior_cam_3x.png
"""
from mock import Art, palette, check, check_two_layers, save, from_image

W_PX, H_PX = 80, 64
DOOR_COL = 2

C = palette(
    K=(64, 72, 104), k=(96, 96, 120), d=(128, 128, 136), s=(152, 176, 216), m=(184, 200, 224),
    l=(216, 224, 232), W=(248, 248, 248),
    R=(200, 64, 80), r=(216, 104, 96), o=(232, 144, 112), p=(248, 184, 128),
    J=(48, 112, 104), j=(80, 168, 144),
    B=(96, 160, 216), b=(112, 184, 240),
)
PALETTES = {"centre": C}

COLS = (0, 24, 50, 74)                      # left x of the four 6px columns
BAYS = ((6, 23), (30, 49), (56, 73))        # openings between them
SLOPE_BOTTOM, BAND_BOTTOM = 19, 26          # roof slope y 1..19, red band y 21..26
STOREY, FRONT_EDGE = 30, 38                 # upper storey y 30..37, overhang edge at y 38
WALL, FLOOR = 39, 56                        # recessed wall y 39..55, walkway floor y 56..63
HIP = 9                                     # how far the ridge is set in from each end


def roof(a):
    c = C
    for y in range(0, SLOPE_BOTTOM + 1):            # hipped slope: narrower at the ridge
        inset = max(0, HIP - y)
        for x in range(inset, 80 - inset):
            edge = x in (inset, 79 - inset) or y == 0
            # hip line: from the ridge end down to the front eave corner. Outside it is the end
            # face of the hipped roof, which faces sideways and so sits in shade.
            hip = HIP * (1 - y / SLOPE_BOTTOM)
            dist = min(x, 79 - x) - hip
            if edge:
                col = c["K"]
            elif dist < -0.5:
                col = c["o"]
            elif dist < 0.5:
                col = c["r"]
            else:
                col = c["r"] if (x % 4) == 3 else c["p"]
            a.put(x, y, col)
    a.hline(1, 78, SLOPE_BOTTOM + 1, c["k"])
    a.rect(1, SLOPE_BOTTOM + 2, 78, BAND_BOTTOM, c["R"])     # solid red band
    a.hline(1, 78, BAND_BOTTOM, c["k"])                      # groove, as on the vanilla roof
    a.vline(0, SLOPE_BOTTOM + 1, BAND_BOTTOM + 1, c["K"]), a.vline(79, SLOPE_BOTTOM + 1, BAND_BOTTOM + 1, c["K"])
    a.hline(0, 79, BAND_BOTTOM + 1, c["K"])
    a.rect(0, BAND_BOTTOM + 2, 79, BAND_BOTTOM + 3, c["k"])  # eave shadow on the wall


def emblem(a):
    """Raised centre section in the band colour with the existing Centre emblem, unchanged."""
    import vanilla
    c = C
    top = BAND_BOTTOM - 13
    for y, (x0, x1) in {top - 2: (31, 48), top - 1: (29, 50)}.items():
        a.hline(x0, x1, y, c["R"])
        a.put(x0, y, c["k"]), a.put(x1, y, c["k"])
    a.hline(31, 48, top - 3, c["k"])
    a.put(30, top - 2, c["k"]), a.put(49, top - 2, c["k"])
    a.rect(27, top, 52, BAND_BOTTOM, c["R"])
    a.vline(27, top, SLOPE_BOTTOM + 1, c["k"]), a.vline(52, top, SLOPE_BOTTOM + 1, c["k"])
    a.put(28, top - 1, c["k"]), a.put(51, top - 1, c["k"])
    a.blit(from_image(vanilla.emblem("centre")), 30, top)


def upper_storey(a):
    c = C
    y0, y1 = STOREY, FRONT_EDGE - 1
    a.rect(0, y0, 79, y1, c["m"])
    a.vline(0, y0, y1, c["K"]), a.vline(79, y0, y1, c["K"])
    for x0 in COLS:                                 # pilasters: lighter strips, no outlines
        a.rect(max(1, x0), y0, min(78, x0 + 5), y1, c["l"])
        a.vline(max(1, x0 + 1), y0, y1, c["W"])
    for x0, x1 in ((9, 21), (34, 46), (59, 71)):    # louvred shutters
        a.rect(x0, y0 + 1, x1, y1, c["K"])
        for y in range(y0 + 2, y1 + 1):
            a.hline(x0 + 1, x1 - 1, y, c["j"] if (y - y0) % 2 == 0 else c["J"])
        a.vline((x0 + x1) // 2, y0 + 2, y1, c["K"])
    a.hline(0, 79, FRONT_EDGE, c["K"])              # front edge of the overhang


def recessed_wall(u):
    c = C
    g = WALL
    u.rect(0, g, 79, FLOOR - 1, c["s"])
    u.rect(0, g, 79, g + 2, c["k"])                 # shade under the arches: deep, then softer
    u.rect(0, g + 3, 79, g + 5, c["d"])
    # sliding glass door, flat like the vanilla one
    u.rect(32, g + 1, 47, FLOOR - 1, c["K"])
    u.rect(33, g + 2, 46, g + 4, c["k"])
    u.rect(33, g + 5, 46, g + 10, c["B"])
    u.rect(33, g + 11, 46, FLOOR - 1, c["b"])
    u.vline(39, g + 2, FLOOR - 1, c["K"]), u.vline(40, g + 5, FLOOR - 1, c["l"])
    # side windows
    for x0, x1 in ((9, 21), (59, 71)):
        u.rect(x0, g + 4, x1, g + 12, c["k"])
        u.rect(x0 + 1, g + 5, x1 - 1, g + 7, c["B"])
        u.rect(x0 + 1, g + 8, x1 - 1, g + 11, c["b"])
        u.hline(x0 - 1, x1 + 1, g + 13, c["l"])


def walkway_floor(u):
    c = C
    for y in range(FLOOR, FLOOR + 6):
        for x in range(0, 80):
            u.put(x, y, c["l"] if ((x + 2) // 4 + (y - FLOOR) // 3) % 2 else c["o"])
    for x in range(0, 80):                          # shade at the foot of the wall
        u.put(x, FLOOR, c["s"] if u.px[FLOOR][x] == c["l"] else c["r"])
    u.hline(0, 79, FLOOR + 6, c["l"])
    u.hline(0, 79, FLOOR + 7, c["K"])
    u.vline(0, FLOOR, FLOOR + 7, c["K"]), u.vline(79, FLOOR, FLOOR + 7, c["K"])


def columns(o):
    c = C
    g = WALL
    for x0 in COLS:
        o.rect(x0, g, x0 + 5, 63, c["k"])
        o.hline(x0, x0 + 5, 63, c["K"])
        o.rect(x0 + 1, g, x0 + 4, 62, c["l"])
        o.vline(x0 + 1, g, 62, c["W"]), o.vline(x0 + 4, g, 62, c["m"])
        o.hline(x0 + 1, x0 + 4, g + 5, c["s"])
        o.hline(x0 + 1, x0 + 4, 59, c["s"])
    for x0, x1 in BAYS:                              # arch spandrels
        for k, n in enumerate((5, 3, 2, 1, 1)):
            y = g + k
            o.hline(x0, x0 + n - 1, y, c["l"]), o.hline(x1 - n + 1, x1, y, c["l"])
            o.put(x0 + n, y, c["k"]), o.put(x1 - n, y, c["k"])
        o.put(x0 + 4, g, c["k"]), o.put(x1 - 4, g, c["k"])


def prop_palm():
    import centre_interior as ci
    a = Art(16, 32)
    rows = [r for r in ci.PALM.split("\n") if r.strip()]
    a.stamp(ci.DECO, ci.PALM, 0, 32 - len(rows) - 1)
    return a


def build():
    u, o = Art(W_PX, H_PX), Art(W_PX, H_PX)
    front = Art(W_PX, H_PX)
    roof(front)
    emblem(front)
    upper_storey(front)
    # tile rows 0-1 sit behind sprites; the facade over the walkway (rows 2-3) draws over the player
    u.blit(front.crop(0, 0, W_PX, 32))
    o.blit(front.crop(0, 32, W_PX, 32), 0, 32)
    u.rect(0, 32, W_PX - 1, WALL - 1, C["k"])      # hidden behind the upper storey; keeps row 2 to two layers
    recessed_wall(u)
    walkway_floor(u)
    columns(o)
    return dict(under=u, over=o, palettes=PALETTES, door_col=DOOR_COL, props={"palm": prop_palm()})


def stage_scene():
    from town import Town
    b = build()
    t = Town(17, 11)
    for x, y in ((0, 0), (2, 1), (11, 0), (13, 1), (15, 0)):
        t.tree(x, y)
    t.path(0, 6, 16, 7)
    t.path(7, 7, 8, 10)
    t.flowers([(4, 4), (12, 4), (3, 9), (13, 9), (14, 9)])
    st = t.stage()
    bx, by = 5, 2
    st.add(b["under"], bx * 16, by * 16)
    st.add(b["over"], bx * 16, by * 16, over=True)
    for dx in (0, 4):
        st.add(b["props"]["palm"], (bx + dx) * 16, (by + 4) * 16 - 16)
    st.npc("brendan/walking.png", "brendan.pal", 1, bx + DOOR_COL, by + 3)
    st.npc("woman_1.png", "npc_1.pal", 2, 12, 6)
    st.npc("boy_1.png", "npc_3.pal", 0, 3, 7)
    return b, st, (bx, by)


if __name__ == "__main__":
    b, st, (bx, by) = stage_scene()
    check({"under": b["under"], "over": b["over"]}, PALETTES, "centre exterior")
    check_two_layers(b["under"], b["over"], name="centre exterior")
    print(save(st.render(), "centre_exterior_3x.png"))
    print(save(st.camera(bx + DOOR_COL, by + 3), "centre_exterior_cam_3x.png"))
