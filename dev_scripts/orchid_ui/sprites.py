"""
Orchid bag-screen sprites: the satchel (6 frames) and the round pocket buttons.

    python dev_scripts/orchid_ui/sprites.py [preview_dir]

Writes graphics/bag/satchel_male.png, satchel_female.png, pocket_icons.png
(indexed, 16 colours, index 0 = transparent) and, if preview_dir is given,
a 3x preview sheet there.

Style: Gen 3 pixels - 1px ink outline, 3-4 step ramps lit from the top-left,
no anti-aliasing. Everything is drawn at native size.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import snap, Canvas  # noqa: E402
import kit  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# =============================================================== satchel palette
# Same indices for male / female; only the strap+flap ramp (8-10) changes.
(S_T, S_INK, S_WHITE, LAV, LEA_D, LEA_S, LEA_M, LEA_L,
 ACC_D, ACC, ACC_L, BRASS, PALE, RED, BLUE, VIOLET) = range(16)

# Item ramps, re-derived from the Gen 3 item icon palettes
# (graphics/items/icon_palettes/poke_ball.pal, potion.pal, oran_berry.pal,
# *_tm_hm.pal), snapped to BGR555. The satchel only has room for four item
# colours, so items borrow the leather/brass ramps for their dark/light ends:
#   Poke Ball  : RED, LEA_S/LEA_D (shade), BRASS + PALE (orange/yellow shine),
#                WHITE + LAV (lavender-white bottom), INK band
#   Potion     : WHITE/LAV nozzle, LAV + VIOLET bottle
#   Oran Berry : BLUE + VIOLET body, WHITE/LAV crown
#   TM         : BLUE disc, WHITE/LAV sheen, VIOLET rim
GEN3 = {
    "red": (224, 88, 56),        # poke_ball.pal (222,90,57)
    "red_dark": (168, 80, 56),   # poke_ball.pal (180,82,57)/(156,74,57)
    "lav_white": (224, 208, 248),  # poke_ball.pal (222,205,246) / potion (230,197,255)
    "lav": (168, 144, 216),      # potion.pal (164,131,205) / poke_ball (164,164,197)
    "violet": (104, 88, 176),    # oran (106,106,189) / potion (131,98,172)
    "blue": (80, 160, 248),      # oran_berry.pal (82,164,246)
}

_SATCHEL_BASE = {
    S_INK: kit.palette()[kit.INK],
    S_WHITE: (248, 248, 248),
    LAV: GEN3["lav"],
    LEA_D: (96, 56, 40),       # deepest leather shade, bag interior
    LEA_S: (152, 96, 56),      # leather shade (also brass shadow)
    LEA_M: (200, 136, 80),     # leather face
    LEA_L: (232, 184, 120),    # leather light
    BRASS: (232, 176, 56),
    PALE: (248, 232, 160),     # leather/brass highlight, thread
    RED: GEN3["red"],
    BLUE: GEN3["blue"],
    VIOLET: GEN3["violet"],
}
_SATCHEL_ACCENT = {
    "male": [(40, 64, 128), (64, 104, 184), (112, 160, 224)],
    "female": [(152, 40, 64), (208, 80, 104), (240, 144, 160)],
}
_SATCHEL_KEY = {"male": (208, 232, 248), "female": (248, 216, 224)}


def satchel_palette(gender):
    p = dict(_SATCHEL_BASE)
    p[S_T] = _SATCHEL_KEY[gender]
    for i, c in zip((ACC_D, ACC, ACC_L), _SATCHEL_ACCENT[gender]):
        p[i] = c
    return [snap(p[i]) for i in range(16)]


SCHARS = {
    ".": None, "_": S_T, "k": S_INK, "w": S_WHITE, "g": LAV,
    "d": LEA_D, "s": LEA_S, "m": LEA_M, "l": LEA_L,
    "N": ACC_D, "A": ACC, "a": ACC_L,
    "b": BRASS, "p": PALE, "r": RED, "u": BLUE, "v": VIOLET,
}


def stamp(cv, x0, y0, grid, chars, clip=None):
    """Paint a string pixel-map. '.' = leave as is. clip(x, y) -> False skips."""
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            c = chars[ch]
            if c is None:
                continue
            if clip and not clip(x0 + x, y0 + y):
                continue
            cv.set(x0 + x, y0 + y, c)


# ---------------------------------------------------------------- mask helpers
def outline_of(mask):
    """Pixels of mask that touch (4-neighbour) a pixel outside it."""
    return {(x, y) for (x, y) in mask
            if any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


def superellipse(cx, cy, a_of_y, b, n, y0, y1):
    m = set()
    for y in range(y0, y1 + 1):
        dy = (y + 0.5 - cy) / b
        if abs(dy) >= 1:
            continue
        a = a_of_y(y)
        half = a * (1 - abs(dy) ** n) ** (1 / n)
        for x in range(int(cx - a - 2), int(cx + a + 3)):
            if abs(x + 0.5 - cx) <= half:
                m.add((x, y))
    return m


def row_span(mask, y):
    xs = [x for (x, yy) in mask if yy == y]
    return (min(xs), max(xs)) if xs else None


def col_span(mask, x):
    ys = [y for (xx, y) in mask if xx == x]
    return (min(ys), max(ys)) if ys else None


# ================================================================== the satchel
CX = 31.5           # horizontal centre of the bag
BODY_TOP, BODY_BOT = 24, 57
FLAP_TOP, FLAP_BOT = 20, 45
LIP_Y = BODY_TOP + 4          # front panel top edge when the flap is open


def half_w(y):
    """Half-width of the bag body at row y (it sags a little wider at the bottom)."""
    return 21.0 + 2.0 * (min(max(y, BODY_TOP), BODY_BOT) - BODY_TOP) / (BODY_BOT - BODY_TOP)


def body_mask():
    return superellipse(CX, (BODY_TOP + BODY_BOT + 1) / 2, half_w,
                        (BODY_BOT - BODY_TOP + 1) / 2, 4.2, BODY_TOP, BODY_BOT)


def box_mask(y0, y1, half, top_ins, bot_ins):
    """Rows y0..y1, centred on CX with half(y) half-width and corner inset tables."""
    m = set()
    for y in range(y0, y1 + 1):
        h = half(y)
        x0, x1 = int(round(CX - h)), int(round(CX + h)) - 1
        ins = max(top_ins[y - y0] if y - y0 < len(top_ins) else 0,
                  bot_ins[y1 - y] if y1 - y < len(bot_ins) else 0)
        for x in range(x0 + ins, x1 - ins + 1):
            m.add((x, y))
    return m


# ------------------------------------------------------------------ strap
# A short shoulder strap arching BEHIND the bag, buckled to both side gussets.
STRAP_CY = 31
STRAP_O = (25.5, 26.0)
STRAP_I = (20.5, 21.5)
STRAP_END = 30          # strap runs down into the side buckles


def strap_mask():
    m = set()
    for y in range(0, STRAP_END + 1):
        for x in range(0, 64):
            dx, dy = x + 0.5 - CX, y + 0.5 - STRAP_CY
            o = (dx / STRAP_O[0]) ** 2 + (dy / STRAP_O[1]) ** 2
            i = (dx / STRAP_I[0]) ** 2 + (dy / STRAP_I[1]) ** 2
            if o <= 1 and i > 1:
                m.add((x, y))
    # knock off lone pixels on the crown so the arch reads as a clean curve
    for (x, y) in list(m):
        if sum((x + dx, y) in m for dx in (-1, 1)) == 0 and (x, y + 1) in m:
            m.discard((x, y))
    return m


def draw_strap(cv):
    """Drawn first: the body and flap are painted over it."""
    m = strap_mask()
    for (x, y) in m:
        dx, dy = x + 0.5 - CX, y + 0.5 - STRAP_CY
        r_o = ((dx / STRAP_O[0]) ** 2 + (dy / STRAP_O[1]) ** 2) ** 0.5
        r_i = ((dx / STRAP_I[0]) ** 2 + (dy / STRAP_I[1]) ** 2) ** 0.5
        t = (r_i - 1) / ((r_i - 1) + (1 - r_o) + 1e-9)   # 0 inner .. 1 outer
        c = ACC
        if t > 0.6 and dx < 10:
            c = ACC_L                 # outer edge catches the light (top-left)
        if t < 0.34 or (dx > 12 and t < 0.5):
            c = ACC_D
        cv.set(x, y, c)
    for (x, y) in outline_of(m):
        cv.set(x, y, S_INK)
    return m


# Buckle on the side gusset, seen edge-on: brass frame with the strap
# threaded through it, and the strap's tail tucked below.
SIDE_BUCKLE = [
    ".kkkkk.",
    "kppbbbk",
    "kbkAkbk",
    "kbkAksk",
    "kbkNksk",
    "kbbssdk",
    ".kkkkk.",
    "..kAk..",
    "..kkk..",
]
BUCKLE_Y = 29


def side_buckles(cv):
    stamp(cv, 5, BUCKLE_Y, SIDE_BUCKLE, SCHARS)
    right = [r[::-1].replace("p", "b").replace("A", "N") for r in SIDE_BUCKLE]
    stamp(cv, 52, BUCKLE_Y, right, SCHARS)


# ------------------------------------------------------------------ leather body
GUSSET = 4      # width of the shaded side panel on the right


def shade_leather(cv, body):
    """Leather: pillowy face lit from the top-left, side panel on the right."""
    for (x, y) in body:
        sp = row_span(body, y)
        cs = col_span(body, x)
        from_l, from_r = x - sp[0], sp[1] - x
        from_b = cs[1] - y
        c = LEA_M
        if from_l <= 2 and from_b > 2:
            c = LEA_L
        if from_b <= 2:
            c = LEA_S
        if from_r <= GUSSET:                 # side panel, turned away from the light
            c = LEA_S
            if from_r <= 1 or from_b <= 3:
                c = LEA_D
        elif from_r == GUSSET + 1:
            c = LEA_D                        # seam between front and side panel
        if from_b <= 1 and from_l > 3:
            c = LEA_D
        cv.set(x, y, c)
    # soft highlight band under the top-left
    for (x, y) in body:
        sp = row_span(body, y)
        if sp[0] + 3 <= x <= sp[0] + 3 and cv.get(x, y) == LEA_M and y < BODY_BOT - 6:
            cv.set(x, y, LEA_L if y % 2 else LEA_M)
    for (x, y) in outline_of(body):
        cv.set(x, y, S_INK)


POCKET = (13, 47, 32, 52)    # x0, x1, y0, y1 of the stitched front pocket


def front_pocket(cv):
    x0, x1, y0, y1 = POCKET
    # pocket panel sits proud: light top/left edge, shade bottom/right
    for x in range(x0, x1 + 1):
        cv.set(x, y1 + 1, LEA_S)
        cv.set(x, y0, LEA_L)
        cv.set(x, y0 - 1, LEA_S)
    for y in range(y0, y1 + 1):
        cv.set(x0, y, LEA_L)
        cv.set(x0 - 1, y, LEA_S)
        cv.set(x1, y, LEA_S)
    cv.set(x0 - 1, y1 + 1, LEA_D)
    cv.set(x1, y1 + 1, LEA_D)
    cv.set(x0 - 1, y0 - 1, LEA_M)
    cv.set(x0, y0 - 1, LEA_M)
    # stitches
    for x in range(x0 + 3, x1 - 1, 3):
        cv.set(x, y1 - 1, PALE)
        cv.set(x + 1, y1 - 1, PALE)
        cv.set(x, y0 + 2, PALE)
        cv.set(x + 1, y0 + 2, PALE)
    for y in range(y0 + 4, y1 - 2, 3):
        cv.set(x0 + 2, y, PALE)
        cv.set(x0 + 2, y + 1, PALE)
        cv.set(x1 - 2, y, LEA_L)
        cv.set(x1 - 2, y + 1, LEA_L)


# ------------------------------------------------------------------ closed flap
def flap_closed_mask():
    return box_mask(FLAP_TOP, FLAP_BOT, lambda y: half_w(y) + 1,
                    [5, 3, 2, 1, 1], [6, 4, 2, 1, 1, 0])


def shade_flap_closed(cv, m):
    top, bot = FLAP_TOP, FLAP_BOT
    for (x, y) in m:
        sp, cs = row_span(m, y), col_span(m, x)
        from_l, from_r = x - sp[0], sp[1] - x
        from_t, from_b = y - cs[0], cs[1] - y
        c = ACC
        if from_t <= 3:
            c = ACC_L                   # the roll over the top catches the light
        if from_t <= 1 and from_r <= 12:
            c = ACC
        if from_l <= 1 and from_t > 3:
            c = ACC_L
        if from_r <= GUSSET and from_t > 3:
            c = ACC_D                   # flap wrapping round the side panel
        if from_b <= 1 and from_l > 1:
            c = ACC_D
        if from_t > 4 and (from_b <= 2 or from_b + from_r - GUSSET <= 6) and from_l > 6:
            c = ACC_D                   # the face turns under toward the bottom edge
        if from_t == 4 and from_r > GUSSET:
            c = ACC_D if from_l > 1 else ACC   # crease under the roll
        cv.set(x, y, c)
    # specular glints on the roll
    for (x, y) in ((13, 22), (14, 21), (15, 21), (16, 21), (17, 21)):
        cv.set(x, y, S_WHITE)
    for (x, y) in ((12, 27), (12, 28), (13, 26)):
        cv.set(x, y, ACC_L)             # sheen on the flap face
    # cast shadow of the flap on the leather
    for x in range(64):
        cs = col_span(m, x)
        if cs and cv.get(x, cs[1] + 1) not in (S_T, S_INK):
            cv.set(x, cs[1] + 1, LEA_D if cv.get(x, cs[1] + 1) in (LEA_S, LEA_D) else LEA_S)
    for (x, y) in outline_of(m):
        cv.set(x, y, S_INK)
    # stitching along the sides and bottom
    for (x, y) in m:
        sp, cs = row_span(m, y), col_span(m, x)
        if y < top + 6 or cv.get(x, y) == S_INK:
            continue
        if x == sp[0] + 3 and y < bot - 4 and y % 3:
            cv.set(x, y, ACC_L)
        if x == sp[1] - GUSSET - 2 and y < bot - 4 and y % 3:
            cv.set(x, y, ACC_L)
        if y == cs[1] - 3 and sp[0] + 4 < x < sp[1] - GUSSET - 3 and x % 3:
            cv.set(x, y, ACC_L)


CLASP = [
    ".kkkkkkkkk.",
    "kpppppppbbk",
    "kpbbbbbbbsk",
    "kpbkkkkkbsk",
    "kpbbbbbbbsk",
    "kbbbbbbbssk",
    ".kkkkkkkkk.",
]

CATCH = [            # the brass plate the clasp locks onto (visible when open)
    "kkkkkkkkk",
    "kppppbbbk",
    "kbkkkkkbk",
    "kbbbbbbsk",
    "kkkkkkkkk",
]


def satchel_closed(cv):
    body = body_mask()
    draw_strap(cv)
    shade_leather(cv, body)
    front_pocket(cv)
    shade_flap_closed(cv, flap_closed_mask())
    stamp(cv, 26, 41, CLASP, SCHARS)
    for x in range(27, 37):       # clasp shadow
        if cv.get(x, 48) in (LEA_M, LEA_L, LEA_S):
            cv.set(x, 48, LEA_D if x > 30 else LEA_S)
    side_buckles(cv)


# ------------------------------------------------------------------ open flap
OPEN_TOP = 13


def flap_open_mask():
    """Flap swung up and back: we see its lining, slightly foreshortened."""
    return box_mask(OPEN_TOP, BODY_TOP - 1,
                    lambda y: half_w(BODY_TOP) - 1.0 * (BODY_TOP - y) / (BODY_TOP - OPEN_TOP),
                    [4, 2, 1, 1], [])


def shade_flap_open(cv, m):
    """Open flap seen from underneath: lining in shadow, lit rim, hinge roll."""
    for (x, y) in m:
        sp, cs = row_span(m, y), col_span(m, x)
        from_l, from_r = x - sp[0], sp[1] - x
        from_t = y - cs[0]
        c = ACC_D                       # lining, turned away from the light
        if from_t <= 7 and from_l <= 20 - from_t * 2:
            c = ACC                     # lit corner of the lining
        if from_t <= 1 or from_l <= 1:
            c = ACC_L                   # rim of the flap
        elif from_t == 2 or from_r <= 1:
            c = ACC
        cv.set(x, y, c)
    for (x, y) in outline_of(m):
        cv.set(x, y, S_INK)
    # stitching just inside the rim
    for (x, y) in m:
        sp, cs = row_span(m, y), col_span(m, x)
        if cv.get(x, y) not in (ACC_D, ACC):
            continue
        on = ((x == sp[0] + 3 or x == sp[1] - 3) and y % 3 and y < BODY_TOP - 1) or \
             (y == cs[0] + 4 and x % 3 and sp[0] + 3 < x < sp[1] - 3)
        if on:
            cv.set(x, y, ACC_L if cv.get(x, y) == ACC else ACC)
    # buckle hanging off the free edge (seen from behind)
    stamp(cv, 26, OPEN_TOP - 2, [
        ".kkkkkkkkk.",
        "kbbbbbbbbsk",
        "kbssssssssk",
        ".kkkkkkkkk.",
    ], SCHARS)


def satchel_open(cv, item):
    body = body_mask()
    draw_strap(cv)
    shade_flap_open(cv, flap_open_mask())
    shade_leather(cv, body)
    # mouth: back wall rim, dark interior
    for y in range(BODY_TOP, LIP_Y):
        sp = row_span(body, y)
        for x in range(sp[0] + 1, sp[1]):
            c = LEA_D
            if y == BODY_TOP:
                c = S_INK
            elif y == BODY_TOP + 1:
                c = LEA_S if x < sp[1] - GUSSET else LEA_D
            cv.set(x, y, c)
    if item:
        item(cv)
    # front panel lip, drawn over the item's lower half
    sp = row_span(body, LIP_Y)
    for x in range(sp[0], sp[1] + 1):
        cv.set(x, LIP_Y, S_INK)
    for x in range(sp[0] + 1, sp[1]):
        fr = sp[1] - x
        cv.set(x, LIP_Y + 1, PALE if fr > GUSSET + 8 else (LEA_L if fr > GUSSET else LEA_S))
        if fr > GUSSET + 1:
            cv.set(x, LIP_Y + 2, LEA_L if fr > GUSSET + 4 else LEA_M)
    front_pocket(cv)
    stamp(cv, 27, 41, CATCH, SCHARS)
    for x in range(28, 37):
        cv.set(x, 46, LEA_S)
    side_buckles(cv)


# ------------------------------------------------------------------ the items
def clip_above(ylim):
    return lambda x, y: y < ylim


ITEM_CLIP = LIP_Y


def item_potion(cv):
    """Spray Potion (Gen 3 potion.pal ramps: pale nozzle, lavender bottle)."""
    g = [
        "....kkkkk...",
        "...kwwwwgk..",
        ".kkkwggggk..",
        "kwgkkkkkkkk.",
        ".kk..kwwgk..",
        ".....kwggk..",
        "...kkkkkkk..",
        "..kwwggggvk.",
        ".kwwgggggvvk",
        ".kwggggggvvk",
        ".kgggggggvvk",
        ".kgggggggvvk",
        ".kggggggvvvk",
        ".kgggggvvvvk",
        ".kgggggvvvvk",
        ".kgggggvvvvk",
        ".kgggggvvvvk",
    ]
    stamp(cv, 26, 12, g, SCHARS, clip_above(ITEM_CLIP))


# Gen 3 item-icon Poke Ball: seen a little from above, so the band sits
# below the middle and tilts down to the right; button front-left on the band.
BALL_16 = [
    ".....kkkkkk.....",
    "...kkrrrrrrkk...",
    "..krrrrrrrrrsk..",
    ".krrbbrrrrrrrsk.",
    ".krbppbrrrrrrsk.",
    "krrbppbrrrrrrssk",
    "krrrbbrrrrrrrssk",
    "krrrrkkkrrrrsssk",
    "ksrrkwwwkrrrsssk",
    "kkkkkwwwkkkssssk",
    "kgggkwwgkggkkkkk",
    ".kwwwkkkwwwgggk.",
    ".kwwwwwwwwwwwgk.",
    "..kwwwwwwwwwgk..",
    "...kkwwwwwgkk...",
    ".....kkkkkk.....",
]


def item_ball(cv):
    stamp(cv, 24, 11, BALL_16, SCHARS, clip_above(ITEM_CLIP))


def item_tm(cv):
    """TM disc (Gen 3 tm.png look: coloured disc, white sheen wedges, open hub)."""
    import math
    cx, cy, r = 32.0, 20.0, 8.0
    for y in range(11, 30):
        for x in range(22, 42):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = (dx * dx + dy * dy) ** 0.5
            if d > r or y >= ITEM_CLIP:
                continue
            if d < 1.1:
                continue                 # hole: whatever is behind shows through
            ang = math.degrees(math.atan2(-dy, dx)) % 180   # sheen is symmetric
            c = BLUE
            if abs(ang - 55) < 10:
                c = S_WHITE
            elif abs(ang - 55) < 22:
                c = LAV
            if d > r - 1.8 and dx + dy > 3.5:
                c = VIOLET               # rim turning away from the light
            if d < 2.0:
                c = S_INK
            elif d < 3.0:
                c = LAV if dx + dy > 0 else S_WHITE
            if d > r - 1:
                c = S_INK
            cv.set(x, y, c)


def item_berry(cv):
    """Oran Berry (Gen 3 oran_berry.pal: blue body, lilac crown, no leaf)."""
    g = [
        "......kkkk......",
        ".....kwwggk.....",
        "....kkkwgkkk....",
        "..kkuuukkuuukk..",
        ".kuwwuuuuuuuuuk.",
        "kuwwuuuuuuuuuuvk",
        "kuwuuuuuuuuuuuvk",
        "kuuuuuuuuuuuuvvk",
        "kuuuuuuuuuuuvvvk",
        "kvuuuuuuuuuvvvvk",
        ".kvuuuuuuuvvvvk.",
        "..kkvvvvvvvvkk..",
        "....kkkkkkkk....",
    ]
    stamp(cv, 24, 13, g, SCHARS, clip_above(ITEM_CLIP))


def item_key(cv):
    g = [
        "..kkkkk...",
        ".kpppbbk..",
        "kpbkkkbsk.",
        "kpk...ksk.",
        "kbk...ksk.",
        "kbbkkkbsk.",
        ".kbbbbsk..",
        "..kpbsk...",
        "..kpbsk...",
        "..kpbskkk.",
        "..kpbsbbsk",
        "..kpbskkk.",
        "..kpbsk...",
        "..kpbskk..",
        "..kpbsbsk.",
        "..kpbskk..",
        "..kpbsk...",
    ]
    stamp(cv, 28, 11, g, SCHARS, clip_above(ITEM_CLIP))


SATCHEL_ITEMS = [item_potion, item_ball, item_tm, item_berry, item_key]


def build_satchel():
    im = Image.new("P", (64, 384), S_T)
    for f in range(6):
        fim = Image.new("P", (64, 64), S_T)
        fcv = Canvas(fim)
        if f == 0:
            satchel_closed(fcv)
        else:
            satchel_open(fcv, SATCHEL_ITEMS[f - 1])
        im.paste(fim, (0, f * 64))
    return im


def with_palette(im, pal):
    out = im.copy()
    flat = []
    for c in pal:
        flat += list(c)
    out.putpalette(flat)
    return out


# ============================================================ pocket buttons
(I_T, I_INK, I_INK_SOFT, I_WHITE, I_PANEL, I_PANEL_SHADE, I_PANEL_DARK,
 I_RED_D, I_RED, I_LAV, I_BLUE, I_SEL_D, I_SEL, I_SEL_L, I_VIOLET, I_LAV_L) = range(16)


def icon_palette():
    """Kit roles 1-6 and 11-13; 7-10/14-15 hold Gen 3 item-icon ramps (see GEN3)."""
    base = kit.palette("orchid", key=(208, 232, 248))
    base[I_RED_D] = snap(GEN3["red_dark"])
    base[I_RED] = snap(GEN3["red"])
    base[I_LAV] = snap(GEN3["lav"])
    base[I_BLUE] = snap(GEN3["blue"])
    base[I_VIOLET] = snap(GEN3["violet"])
    base[I_LAV_L] = snap(GEN3["lav_white"])
    return base


ICHARS = {
    ".": None, "k": I_INK, "K": I_INK_SOFT, "w": I_WHITE, "p": I_PANEL,
    "s": I_PANEL_SHADE, "d": I_PANEL_DARK, "R": I_RED_D, "r": I_RED,
    "g": I_LAV, "l": I_LAV_L, "b": I_BLUE, "B": I_VIOLET,
    "O": I_SEL_D, "o": I_SEL, "y": I_SEL_L,
}

# Small icons (normal state) ~12px and large (selected) ~14px.
def circle_mask(cx, cy, d, fudge=0.2):
    """Clean pixel circle of even diameter d centred on the pixel corner (cx, cy)."""
    r = d / 2
    m = set()
    for y in range(int(cy - r), int(cy + r)):
        dy = y + 0.5 - cy
        half = (max(0.0, (r - fudge) ** 2 - dy * dy)) ** 0.5 + 0.5
        for x in range(int(cx - r), int(cx + r)):
            if abs(x + 0.5 - cx) <= half:
                m.add((x, y))
    return m


def bevel_disc(cv, cx, cy, d, face, light, shade, outline=I_INK):
    m = circle_mask(cx, cy, d)
    edge = outline_of(m)
    inner = outline_of(m - edge)
    for (x, y) in m:
        cv.set(x, y, face)
    for (x, y) in inner:
        dx, dy = x + 0.5 - cx, y + 0.5 - cy
        dot = (-dx - dy) / ((dx * dx + dy * dy) ** 0.5 + 1e-9)
        if dot > 0.3:
            cv.set(x, y, light)
        elif dot < -0.3:
            cv.set(x, y, shade)
    for (x, y) in edge:
        cv.set(x, y, outline)
    return m


# Icon art follows the Gen 3 item icons: Poke Ball seen slightly from above
# (band low and tilted, button front-left), lavender potion with a pale spray
# head, Oran Berry as a blue blob with a lilac crown, TM as a coloured disc
# with sheen wedges and an open hub, Key Items as a silver key (key.pal greys).
ICON_GRIDS = {
    ("items", 0): [
        ".....kkkk...",
        "....kwwwdk..",
        ".kkkkwdddk..",
        "kwddkkkkkkk.",
        ".kk.kkwwdk..",
        "...kkkkkkkk.",
        "..kwlgggggBk",
        "..klggggggBk",
        "..klggggggBk",
        "..kgggggggBk",
        "..kggggggBBk",
        "..kgggggBBBk",
        "...kkkkkkkk.",
    ],
    ("items", 1): [
        "......kkkk...",
        ".....kwwwdk..",
        "..kkkkwdddk..",
        ".kwddkkkkkkk.",
        "..kk.kkwwdk..",
        "......kwwdk..",
        "....kkkkkkkk.",
        "...kwllggggBk",
        "...kwlgggggBk",
        "...klggggggBk",
        "...kgggggggBk",
        "...kggggggBBk",
        "...kggggggBBk",
        "...kgggggBBBk",
        "....kkkkkkkk.",
    ],
    ("balls", 0): [
        "....kkkk....",
        "..kkrrrrkk..",
        ".krOOrrrrRk.",
        ".kOooOrrrRk.",
        "krrOOrrrrRRk",
        "kRrrkkrrRRRk",
        "kkkkwwkkkRRk",
        "kKKkwlkKKkkk",
        ".kllkkllKKk.",
        ".kllllllggk.",
        "..kklllgkk..",
        "....kkkk....",
    ],
    ("balls", 1): [
        ".....kkkk.....",
        "...kkrrrrkk...",
        "..krOOrrrrRk..",
        ".krOooOrrrrRk.",
        ".krrOOrrrrrRk.",
        "krrrkkkrrrrRRk",
        "kRrkwwwkrrRRRk",
        "kkkkwwwkkkRRRk",
        "kKKkwwlkKKkkkk",
        ".kllkkkllKKKk.",
        ".klllllllllgk.",
        "..klllllllgk..",
        "...kklllgkk...",
        ".....kkkk.....",
    ],
    ("tms", 0): [
        "....kkkk....",
        "..kkbblwkk..",
        ".kbbbblwbbk.",
        ".kbbbblbbBk.",
        "kbbbbKKbbbBk",
        "klbbK..KbbBk",
        "kwlbK..KbBBk",
        "kblbbKKbbBBk",
        ".kbwlbbbBBk.",
        ".kbblbbBBBk.",
        "..kkbbBBkk..",
        "....kkkk....",
    ],
    ("tms", 1): [
        ".....kkkk.....",
        "...kkbblwkk...",
        "..kbbbblwbbk..",
        ".kbbbbblwbbBk.",
        ".kbbbbblbbbBk.",
        "kbbbbbKKbbbbBk",
        "klbbbK..KbbbBk",
        "kwlbbK..KbbBBk",
        "kblbbbKKbbbBBk",
        ".kbwlbbbbbBBk.",
        ".kbbwlbbbBBBk.",
        "..kbblbbBBBk..",
        "...kkbbBBkk...",
        ".....kkkk.....",
    ],
    ("berries", 0): [
        "....kkkk....",
        "...kwllgk...",
        "..kkkllkkk..",
        ".kbbbkkbbbk.",
        "kbwwbbbbbbbk",
        "kbwbbbbbbbbk",
        "kbbbbbbbbbBk",
        "kbbbbbbbbBBk",
        ".kBbbbbbBBk.",
        "..kkBBBBkk..",
        "....kkkk....",
    ],
    ("berries", 1): [
        ".....kkkk.....",
        "....kwllgk....",
        "..kkkkllkkkk..",
        ".kbbbbkkbbbbk.",
        "kbwwbbbbbbbbbk",
        "kbwbbbbbbbbbbk",
        "kbbbbbbbbbbbBk",
        "kbbbbbbbbbbBBk",
        "kBbbbbbbbbBBBk",
        ".kBbbbbbbBBBk.",
        "..kkBBBBBBkk..",
        "....kkkkkk....",
    ],
    ("keys", 0): [
        ".......kkk..",
        "......kwwsk.",
        ".....kwskdsk",
        ".....kwk.kdk",
        ".....ksdkddk",
        "....kssddkk.",
        "...kwsdkk...",
        "..kwsdkwk...",
        ".kwsdkkdk...",
        "kwsdkwdk....",
        "ksdkkkk.....",
        ".kk.........",
    ],
    ("keys", 1): [
        "........kkkk..",
        ".......kwwssk.",
        "......kwskksdk",
        "......kwk..kdk",
        "......ksk..kdk",
        ".....kssdkkddk",
        "....kwsdddddk.",
        "...kwsdkkkkk..",
        "..kwsdkwk.....",
        ".kwsdkkdk.....",
        "kwsdkwdk......",
        "ksdkkkk.......",
        ".kk...........",
    ],
}


# Horizontal nudges so the visual mass (not the grid box) sits on the disc
# centre, e.g. the potion's bottle body rather than its sideways spray nozzle.
ICON_NUDGE_X = {("items", 0): -1, ("items", 1): -2}


def draw_icon(cv, pocket, big):
    key = (pocket, 1 if big else 0)
    g = ICON_GRIDS[key]
    h, w = len(g), max(len(r) for r in g)
    stamp(cv, 16 - w // 2 + ICON_NUDGE_X.get(key, 0), 16 - h // 2, g, ICHARS)


POCKETS = ["items", "balls", "tms", "berries", "keys"]
NORMAL_D, SELECTED_D = 20, 24


def build_icons():
    im = Image.new("P", (32, 320), I_T)
    for i in range(10):
        sel = i >= 5
        f = Image.new("P", (32, 32), I_T)
        cv = Canvas(f)
        if sel:
            bevel_disc(cv, 16, 16, SELECTED_D, I_SEL, I_SEL_L, I_SEL_D)
        else:
            bevel_disc(cv, 16, 16, NORMAL_D, I_PANEL, I_WHITE, I_PANEL_SHADE)
        draw_icon(cv, POCKETS[i % 5], sel)
        im.paste(f, (0, i * 32))
    return with_palette(im, icon_palette())


# ================================================================== preview
def to_rgba(im, bg):
    pal = im.getpalette()[:48]
    px = im.load()
    out = Image.new("RGB", im.size, bg)
    opx = out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            i = px[x, y]
            if i:
                opx[x, y] = tuple(pal[i * 3:i * 3 + 3])
    return out


def palette_strip(im, size=12):
    pal = im.getpalette()[:48]
    s = Image.new("RGB", (16 * size, size), (0, 0, 0))
    for i in range(16):
        s.paste(tuple(pal[i * 3:i * 3 + 3]), (i * size, 0, (i + 1) * size, size))
    return s


GEN3_REFS = [("potion", "potion"), ("poke_ball", "poke_ball"), ("tm", "water_tm_hm"),
             ("oran_berry", "oran_berry"), ("key_to_room_1", "key")]


def gen3_icon(icon, pal, bg):
    """Render a real in-game 24x24 item icon (padded to 32x32) for comparison."""
    base = os.path.join(REPO, "graphics", "items")
    try:
        im = Image.open(os.path.join(base, "icons", icon + ".png"))
        lines = open(os.path.join(base, "icon_palettes", pal + ".pal")).read().split()
    except OSError:
        return None
    vals = list(map(int, lines[3:3 + 48]))
    out = Image.new("RGB", (32, 32), bg)
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            v = px[x, y]
            if v:
                out.putpixel((x + 4, y + 4), tuple(vals[v * 3:v * 3 + 3]))
    return out


def item_sheet(flatpal):
    """Each satchel item drawn on its own, cropped to 32x32."""
    out = []
    for fn in SATCHEL_ITEMS:
        f = Image.new("P", (64, 64), S_T)
        f.putpalette(flatpal)
        fn(Canvas(f))
        out.append(f.crop((16, 4, 48, 36)))
    return out


def preview(path, male, female, icons, scale=3):
    from PIL import ImageDraw
    bgs = [(208, 232, 248), (248, 216, 224)]
    fw = 64 * scale
    W = 6 * fw + 20
    H = 2 * (fw + 10) * 2 + 2 * (32 * scale + 10) + 5 * (32 * scale + 6) + 3 * 40 + 40
    sheet = Image.new("RGB", (W, H + 80), (64, 64, 72))
    y = 10
    for sat in (male, female):
        for bg in bgs:
            rgb = to_rgba(sat, bg)
            for f in range(6):
                fr = rgb.crop((0, f * 64, 64, f * 64 + 64)).resize((fw, fw), Image.NEAREST)
                sheet.paste(fr, (10 + f * fw, y))
            y += fw + 6
    for bg in bgs:
        rgb = to_rgba(icons, bg)
        for f in range(10):
            fr = rgb.crop((0, f * 32, 32, f * 32 + 32)).resize((32 * scale, 32 * scale), Image.NEAREST)
            sheet.paste(fr, (10 + f * 32 * scale, y))
        y += 32 * scale + 6
    d = ImageDraw.Draw(sheet)
    # comparison: in-game Gen 3 icon | satchel item | pocket button normal | selected
    d.text((10, y), "in-game icon | satchel item | button | button selected", fill=(255, 255, 255))
    y += 14
    sat_rgb = to_rgba(male, bgs[0])
    ic_rgb = to_rgba(icons, bgs[0])
    items = item_sheet(male.getpalette()[:48])
    cell = 32 * scale
    for i, (ic, pal) in enumerate(GEN3_REFS):
        x = 10
        ref = gen3_icon(ic, pal, bgs[0])
        if ref:
            sheet.paste(ref.resize((cell, cell), Image.NEAREST), (x, y))
        x += cell + 8
        sheet.paste(to_rgba(items[i], bgs[0]).resize((cell, cell), Image.NEAREST), (x, y))
        x += cell + 8
        for f in (i, i + 5):
            sheet.paste(ic_rgb.crop((0, f * 32, 32, f * 32 + 32)).resize((cell, cell), Image.NEAREST), (x, y))
            x += cell + 8
        y += cell + 6
    del sat_rgb
    for lbl, im in (("male", male), ("female", female), ("icons", icons)):
        d.text((10, y), lbl, fill=(255, 255, 255))
        sheet.paste(palette_strip(im, 20), (60, y))
        y += 24
    sheet = sheet.crop((0, 0, W, y + 6))
    sheet.save(path)


def main():
    base = build_satchel()
    male = with_palette(base, satchel_palette("male"))
    female = with_palette(base, satchel_palette("female"))
    icons = build_icons()
    out = os.path.join(REPO, "graphics", "bag")
    male.save(os.path.join(out, "satchel_male.png"), transparency=0)
    female.save(os.path.join(out, "satchel_female.png"), transparency=0)
    icons.save(os.path.join(out, "pocket_icons.png"), transparency=0)
    if len(sys.argv) > 1:
        preview(os.path.join(sys.argv[1], "satchel_preview.png"), male, female, icons)
        # big 1-frame zooms for close inspection
        for name, im, bg in (("m", male, (208, 232, 248)), ("f", female, (248, 216, 224))):
            to_rgba(im, bg).resize((64 * 8, 384 * 8), Image.NEAREST).save(
                os.path.join(sys.argv[1], "zoom_%s.png" % name))
        to_rgba(icons, (208, 232, 248)).resize((32 * 8, 320 * 8), Image.NEAREST).save(
            os.path.join(sys.argv[1], "zoom_icons.png"))


if __name__ == "__main__":
    main()
