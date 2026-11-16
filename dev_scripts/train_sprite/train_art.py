"""
Tosa Rail overworld train — Gen 3 object style, rendered like the FRLG S.S. Anne:
neutral lavender-grey ramp (taken from graphics/door_anims/ss_anne.png), roof drawn as a "deck"
(inset panel inside a white rim, rim follows the nose like a ship's bow), 2-step rounded corners,
banded side (white -> lavender lower hull), periwinkle glass, navy-grey outline.

Approved 2026-11-16: option C (Tosa Commuter), plain rear carriage end, no pantograph,
dark open-door interior, wheels on the track tile's bottom row. Export with export.py.

Builds the four 64x64 pieces the engine (src/train_travel.c) expects:
    piece 0 = rear carriage / tail cab      piece 1 = boarding carriage, door SHUT
    piece 2 = locomotive (front, right)     piece 3 = boarding carriage, door OPEN
Laid out on screen [0][1][2] = 192 px, travelling left -> right.

Piece-local geometry (rows):
    16        roof outline (content rows 16..63 = 48 px)
    17..28    roof "deck": far rim, rim shadow, panel, near rim
    29        cant highlight (roof/side edge)
    30..56    side face  (windows 33..40, livery ~44..47, lower-hull band 52..56)
    57        body bottom outline
    58..63    underframe + bogies (wheel bottoms on row 63 = bottom of the track tile)
Boarding door: x 24..39 (16 px) in pieces 1/3, opening rows 31..56.
    -> TRAIN_DOOR_X = 64 + 24, TRAIN_DOOR_WIDTH = 16, TRAIN_BOTTOM_DROP = 0 (unchanged)
Carriages join with a 4 px gangway: x 62..63 of one piece + x 0..1 of the next.

usage:  python train_art.py [option]   (imported by mockups.py / export.py)
"""
from PIL import Image

P = 64

# Fixed palette roles so every option draws with the same code.
(TRANSP, OUT, DARK, MID, ROOF, SHADE, BODY, HI,
 GLASS, GLASS_M, GLINT, ACC_D, ACC, ACC_L, LAMP, TAIL) = range(16)

BASE = {
    TRANSP:  (112, 192, 160),   # Gen 3 object-event transparency key
    OUT:     (64, 64, 88),      # outline (S.S. Anne darkest grey-lavender, one step darker)
    DARK:    (80, 80, 104),     # S.S. Anne ramp ->
    MID:     (112, 112, 136),
    ROOF:    (144, 144, 168),
    SHADE:   (184, 184, 200),
    BODY:    (216, 216, 224),
    HI:      (248, 248, 248),   # <- S.S. Anne ramp
    GLASS:   (96, 96, 168),     # S.S. Anne window glass ramp
    GLASS_M: (128, 128, 208),
    GLINT:   (160, 160, 248),
    ACC_D:   (96, 48, 120),     # Orchid livery ramp
    ACC:     (144, 80, 176),
    ACC_L:   (192, 136, 216),
    LAMP:    (248, 216, 96),    # headlight / interior light
    TAIL:    (224, 80, 88),     # tail light
}


def snap(c):
    return tuple((v // 8) * 8 for v in c)


OPTIONS = {
    "A": dict(name="Orchid Express", nose="bullet", windows="band", livery="stripe"),
    "B": dict(name="Orchid Liner", nose="bullet", windows="panes", livery="twotone"),
    "C": dict(name="Tosa Commuter", nose="blunt", windows="panes", livery="band", rear="plain"),
}


class Piece:
    def __init__(self):
        self.px = [[TRANSP] * P for _ in range(P)]

    def set(self, x, y, c):
        if 0 <= x < P and 0 <= y < P:
            self.px[y][x] = c

    def get(self, x, y):
        if 0 <= x < P and 0 <= y < P:
            return self.px[y][x]
        return TRANSP

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, c)

    def image(self, pal):
        im = Image.new("P", (P, P))
        im.putdata([c for row in self.px for c in row])
        im.putpalette([v for i in range(16) for v in snap(pal[i])] + [0] * (256 - 16) * 3)
        return im


# ---------------------------------------------------------------- silhouettes
TOP, EDGE, BOT = 16, 29, 56   # roof outline row, cant row, last side row
CORNER = {0: 2, 1: 1}         # 2-step rounded corner: column offset -> rows dropped


def ease(u, p):
    return max(0.0, min(1.0, u)) ** p


def profile(kind, x, opt):
    """(t, e, b) for column x: t = top outline row, e = cant row (roof/side boundary),
    b = last side-face row; None if the column is empty.
    kind: 'car' (gangways both ends), 'loco' (nose right), 'tail' (nose left)."""
    if kind == "tail":
        x = P - 1 - x                     # mirror geometry; lighting stays top-left
    if x < 2:
        return None
    rnd = CORNER.get(x - 2, 0)            # rounded corner at the gangway end
    if kind == "car":
        if x > 61:
            return None
        rnd = max(rnd, CORNER.get(61 - x, 0))
        return (TOP + rnd, EDGE, BOT - (1 if rnd == 2 else 0))
    if opt["nose"] == "bullet":
        u = (x - 28) / 35.0
        t = TOP + max(rnd, round(34 * ease(u, 2.0)))
        e = EDGE + round(21 * ease(u, 1.5))
        b = BOT - round(5 * ease((x - 54) / 9.0, 1.6)) - (1 if rnd == 2 else 0)
        return (t, max(e, t + 1), b)
    # blunt commuter cab: big rounded roof corner + slightly raked front
    if x > 61:
        return None
    t = TOP + max(rnd, round(8 * ease((x - 53) / 8.0, 2.0)))
    b = BOT - (1 if x == 61 else 0) - (1 if rnd == 2 else 0)
    return (t, EDGE + (1 if x >= 60 else 0), b)


def side_colour(y, b):
    """Banded hull: white face, then a 3-step lower-hull ramp."""
    if y >= b:
        return MID
    if y >= b - 2:
        return ROOF
    if y >= b - 4:
        return SHADE
    return BODY


def draw_body(pc, kind, opt):
    cols = {x: profile(kind, x, opt) for x in range(P)}
    for x, pr in cols.items():
        if not pr:
            continue
        t, e, b = pr
        for y in range(t, b + 2):
            if y == t or y == b + 1:
                c = OUT
            elif y < e:                       # roof deck
                if y == t + 1:
                    c = HI                    # far rim (lit)
                elif y == t + 2 and y < e - 2:
                    c = ROOF                  # rim's shadow on the panel
                elif y == e - 1:
                    c = BODY                  # near rim
                elif y == e - 2:
                    c = HI if e - t > 4 else BODY
                else:
                    c = SHADE                 # panel
            elif y == e:
                c = BODY                      # cant edge (lip under the rim)
            else:
                c = side_colour(y, b)
            pc.set(x, y, c)
    # left/right silhouette outline + deck rim on the ends
    for y in range(P):
        for x in range(P):
            if pc.get(x, y) not in (TRANSP, OUT) and (
                    pc.get(x - 1, y) == TRANSP or pc.get(x + 1, y) == TRANSP):
                pc.set(x, y, OUT)
    for x, pr in cols.items():
        if not pr:
            continue
        t, e, b = pr
        for y in range(t + 2, e - 2):
            if pc.get(x - 1, y) == OUT and cols.get(x - 1) and pc.get(x, y) == SHADE:
                pc.set(x, y, HI)              # left rim (lit)
                if pc.get(x + 1, y) == SHADE:
                    pc.set(x + 1, y, ROOF)
            if pc.get(x + 1, y) == OUT and pc.get(x, y) == SHADE:
                pc.set(x, y, BODY)            # right rim


def gangway(pc, left, right):
    cols = []
    if left:
        cols += [(0, ROOF), (1, MID)]
    if right:
        cols += [(62, MID), (63, ROOF)]
    for x, c in cols:
        pc.set(x, 21, OUT)
        for y in range(22, 55):
            pc.set(x, y, c if (y - 22) % 4 else DARK)   # bellows folds every 4 px
        pc.set(x, 55, OUT)


def side_ok(kind, opt, x):
    pr = profile(kind, x, opt)
    return pr and pr[1] <= 30 and pr[2] >= 50 and pr[0] <= 18


def windows(pc, kind, opt, runs):
    """runs: list of (x0, x1); window rows 33..40."""
    for x0, x1 in runs:
        xs = [x for x in range(x0, x1 + 1) if side_ok(kind, opt, x)]
        if not xs:
            continue
        a, z = xs[0], xs[-1]
        if opt["windows"] == "band":
            pc.rect(a, 33, z, 40, GLASS)
            pc.rect(a, 34, z, 35, GLASS_M)
            pc.rect(a, 33, z, 33, OUT)
            for x in range(a + 10, z - 1, 11):              # pillars (2 px)
                pc.rect(x, 34, x + 1, 40, OUT)
            for x in range(a, z - 3, 11):
                pc.rect(x + 2, 34, x + 3, 34, GLINT)
                pc.set(x + 2, 35, GLINT)
        else:
            x = a
            while x + 6 <= z:
                pc.rect(x, 33, x + 6, 40, GLASS)
                pc.rect(x, 34, x + 6, 35, GLASS_M)
                pc.rect(x, 33, x + 6, 33, OUT)
                pc.rect(x, 33, x, 40, OUT)
                pc.rect(x + 1, 34, x + 2, 34, GLINT)
                pc.set(x + 1, 35, GLINT)
                x += 10


def livery(pc, kind, opt, xs):
    for x in xs:
        pr = profile(kind, x, opt)
        if not pr:
            continue
        t, e, b = pr

        def paint(y, c):
            if e < y <= b and pc.get(x, y) not in (OUT, GLASS, GLASS_M, GLINT, TRANSP):
                pc.set(x, y, c)
        if opt["livery"] == "stripe":
            paint(44, ACC_L); paint(45, ACC); paint(46, ACC); paint(47, ACC_D)
        elif opt["livery"] == "twotone":
            paint(43, ACC_L)
            for y in range(44, b + 1):
                paint(y, ACC if y < b - 1 else ACC_D)
        elif opt["livery"] == "band":
            for y in range(31, 43):
                paint(y, ACC_L if y == 31 else ACC)
            paint(42, ACC_D)
            paint(47, ACC); paint(48, ACC_D)


def roof_unit(pc, x0, x1):
    """Raised roof unit drawn like an S.S. Anne deck tier: lit top, front face with slits."""
    pc.rect(x0, 18, x1, 26, OUT)
    pc.rect(x0 + 1, 19, x1 - 1, 19, HI)
    pc.rect(x0 + 1, 20, x1 - 1, 21, BODY)
    pc.rect(x0 + 1, 22, x1 - 1, 22, SHADE)
    pc.rect(x0 + 1, 23, x1 - 1, 25, BODY)
    pc.rect(x0 + 2, 23, x1 - 2, 24, MID)          # louvre
    for x in range(x0 + 4, x1 - 2, 4):
        pc.rect(x, 23, x, 24, ROOF)
    pc.rect(x0 + 1, 27, x1 + 1, 27, ROOF)            # cast shadow on the deck


def bogies(pc, xs):
    for x in range(3, 61):
        if pc.get(x, 57) == OUT:
            pc.set(x, 58, DARK)
    for bx in xs:
        pc.rect(bx, 58, bx + 15, 59, OUT)
        pc.rect(bx + 1, 58, bx + 14, 58, DARK)
        for wx in (bx + 1, bx + 9):
            for y, (a, z) in zip(range(59, 64), [(1, 4), (0, 5), (0, 5), (0, 5), (1, 4)]):
                pc.rect(wx + a, y, wx + z, y, OUT)
            pc.rect(wx + 2, 60, wx + 3, 61, MID)
            pc.set(wx + 2, 60, ROOF)


def door(pc, opened):
    x0, x1 = 24, 39
    if not opened:
        for y in range(31, 57):
            pc.rect(x0, y, x1, y, side_colour(y, BOT))
        pc.rect(x0, 31, x1, 31, OUT)
        pc.rect(x0, 31, x0, 56, OUT)
        pc.rect(x1, 31, x1, 56, OUT)
        pc.rect(x0 + 1, 32, x1 - 1, 32, HI)
        pc.rect(31, 32, 31, 56, SHADE)          # leaf seam
        pc.rect(32, 32, 32, 56, OUT)
        for wx in (26, 34):                     # door windows
            pc.rect(wx, 34, wx + 3, 41, GLASS)
            pc.rect(wx, 35, wx + 3, 36, GLASS_M)
            pc.rect(wx, 34, wx + 3, 34, OUT)
            pc.rect(wx + 1, 35, wx + 1, 36, GLINT)
    else:
        pc.rect(x0, 31, x1, 56, OUT)
        pc.rect(x0 + 1, 32, x1 - 1, 32, LAMP)   # interior light
        pc.rect(x0 + 1, 33, x1 - 1, 49, DARK)   # back wall
        pc.rect(x0 + 1, 33, x1 - 1, 33, MID)
        pc.rect(x0 + 1, 50, x1 - 1, 55, ROOF)   # floor
        pc.rect(x0 + 1, 50, x1 - 1, 50, MID)
        pc.rect(x0 + 1, 56, x1 - 1, 56, SHADE)  # threshold
        pc.rect(x0, 31, x0, 56, MID)            # leaf pockets
        pc.rect(x1, 31, x1, 56, MID)


def nose_details(pc, kind, opt):
    mirror = kind == "tail"
    X = (lambda x: P - 1 - x) if mirror else (lambda x: x)
    lamp = TAIL if mirror else LAMP
    if opt["nose"] == "bullet":
        for lx in range(30, 50):                # windscreen on the hood
            t, e, b = profile("loco", lx, opt)
            depth = 8 if lx < 44 else 8 - (lx - 43)
            y0, y1 = t + 2, min(t + 1 + depth, e - 2)
            if y1 <= y0:
                continue
            for y in range(y0, y1 + 1):
                pc.set(X(lx), y, GLASS_M if y <= y0 + 2 else GLASS)
            pc.set(X(lx), y0, OUT)
            pc.set(X(lx), y1, OUT)
        for lx, y in [(35, 20), (36, 20), (35, 21), (40, 22), (41, 22), (40, 23)]:
            pc.set(X(lx), y + 1, GLINT)
        for lx, y in [(57, 51), (58, 51), (59, 51), (58, 52), (59, 52), (60, 52)]:
            pc.set(X(lx), y, lamp)
    else:
        for lx in range(55, 61):                # wrap-round windscreen at the front corner
            t, e, b = profile("loco", lx, opt)
            for y in range(max(t + 2, 31), 41):
                pc.set(X(lx), y, GLASS_M if y < 35 else GLASS)
            pc.set(X(lx), max(t + 2, 31), OUT)
        pc.rect(min(X(56), X(57)), 33, max(X(56), X(57)), 33, GLINT)
        pc.set(X(56), 34, GLINT)
        lo, hi = sorted((X(46), X(51)))         # cab side window
        pc.rect(lo, 33, hi, 40, GLASS)
        pc.rect(lo, 34, hi, 35, GLASS_M)
        pc.rect(lo, 33, hi, 33, OUT)
        pc.rect(min(X(58), X(59)), 50, max(X(58), X(59)), 51, lamp)


def build(opt_key):
    opt = OPTIONS[opt_key]
    pieces = []
    for idx in range(4):
        pc = Piece()
        kind = {0: "tail", 1: "car", 2: "loco", 3: "car"}[idx]
        if kind == "tail" and opt.get("rear") == "plain":
            # plain rear carriage end: car body, gangway on the right only, no door/cab
            draw_body(pc, "car", opt)
            gangway(pc, False, True)
            roof_unit(pc, 8, 19)
            roof_unit(pc, 44, 55)
            windows(pc, "car", opt, [(5, 59)])
            livery(pc, "car", opt, range(P))
            bogies(pc, [6, 42])
            pieces.append(pc)
            continue
        draw_body(pc, kind, opt)
        if kind == "car":
            gangway(pc, True, True)
            roof_unit(pc, 8, 19)
            roof_unit(pc, 44, 55)
            windows(pc, kind, opt, [(5, 21), (43, 59)])
            door(pc, opened=(idx == 3))
            skip = range(24, 40) if (idx == 3 or opt["livery"] == "band") else range(24, 24)
            livery(pc, kind, opt, [x for x in range(P) if x not in skip])
            if idx == 1:                              # keep door frame/seam over the livery
                for x, c in ((24, OUT), (39, OUT), (32, OUT), (31, SHADE)):
                    for y in range(43, 57):
                        if pc.get(x, y) != OUT or c == OUT:
                            pc.set(x, y, c)
            bogies(pc, [6, 42])
        else:
            gangway(pc, kind == "loco", kind == "tail")
            bullet = opt["nose"] == "bullet"
            if kind == "loco":
                roof_unit(pc, 8, 19)
                windows(pc, kind, opt, [(5, 40 if bullet else 42)])
            else:
                roof_unit(pc, 44, 55)
                windows(pc, kind, opt, [(23 if bullet else 21, 59)])
            livery(pc, kind, opt, range(P))
            nose_details(pc, kind, opt)
            bogies(pc, [8, 40])
        pieces.append(pc)
    return pieces


def palette(opt_key):
    return dict(BASE)


def sheet(opt_key):
    """64 x 256 indexed image in engine order (pieces stacked vertically)."""
    pcs = build(opt_key)
    pal = palette(opt_key)
    im = Image.new("P", (P, P * 4))
    im.putpalette(pcs[0].image(pal).getpalette())
    for i, pc in enumerate(pcs):
        im.paste(pc.image(pal), (0, i * P))
    return im


def strip(opt_key, door_open=False):
    """192 x 64 RGBA preview of the assembled train as the engine lays it out."""
    pcs = build(opt_key)
    pal = palette(opt_key)
    out = Image.new("RGBA", (P * 3, P), (0, 0, 0, 0))
    for slot, idx in enumerate([0, 3 if door_open else 1, 2]):
        im = pcs[idx].image(pal).convert("RGBA")
        px = im.load()
        for y in range(P):
            for x in range(P):
                if pcs[idx].px[y][x] == TRANSP:
                    px[x, y] = (0, 0, 0, 0)
        out.alpha_composite(im, (slot * P, 0))
    return out


if __name__ == "__main__":
    import sys, os
    k = sys.argv[1] if len(sys.argv) > 1 else "A"
    o = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(o, exist_ok=True)
    s = strip(k)
    s.resize((s.width * 4, s.height * 4), Image.NEAREST).save(os.path.join(o, f"strip_{k}_4x.png"))
    print("wrote", k)
