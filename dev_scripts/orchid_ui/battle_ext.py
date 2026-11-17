"""
Battle-only helpers for the Orchid battle UI mockups (mock_battle.py / anim_battle.py).

* scene(): the vanilla battle environment (BG3 in vanilla, the Mode 7 floor on the
  engine branch) + the two battlers at the vanilla singles coordinates.
* Layout constants for the new UI, all inside the vanilla UI zones:
    - opponent healthbox  OBJ  top-left   (vanilla 13..112 x 16..43)
    - player healthbox    OBJ  right      (vanilla 127..230 x 74..111)
    - bottom tray         BG0  y 112..159 (vanilla textbox area, 30x6 tiles)
"""
import os
import struct
from PIL import Image
from kit import *
import kit_ext as K

W, H = 240, 160
G = K.G

# ------------------------------------------------------------------ vanilla coordinates
# sBattlerCoords (battle_anim_mons.c) + species pic Y offsets (GBA-style gfx).
PLAYER_C = (72, 80)
ENEMY_C = (176, 40)
SPECIES = {
    "grovyle": dict(front_y=4, back_y=8),
    "treecko": dict(front_y=13, back_y=11),
    "zigzagoon": dict(front_y=15, back_y=11),
    "poochyena": dict(front_y=12, back_y=9),
}
TRAY_Y = 112                    # textbox area = tile rows 14..19


def _tilemap(path):
    d = open(path, "rb").read()
    return struct.unpack("<%dH" % (len(d) // 2), d)


_ENV_CACHE = {}


def environment(name="tall_grass"):
    if name not in _ENV_CACHE:
        _ENV_CACHE[name] = _environment(name)
    return _ENV_CACHE[name].copy()


def _environment(name="tall_grass"):
    """Composite graphics/battle_environment/<name>/{tiles.png,map.bin,palette.pal} -> 240x160 RGBA.
    64x32 map (two 32x32 screens); the visible window starts at 0,0."""
    d = G("battle_environment", name)
    tiles = Image.open(os.path.join(d, "tiles.png"))
    tp = tiles.load()
    tw = tiles.size[0] // 8
    pal = [snap(c) for c in K.load_jasc(os.path.join(d, "palette.pal"))]   # BG rows 2..4
    tm = _tilemap(os.path.join(d, "map.bin"))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    op = out.load()
    for ty in range(H // 8):
        for tx in range(W // 8):
            e = tm[ty * 32 + tx]                # screen 0
            idx, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            sx, sy = (idx % tw) * 8, (idx // tw) * 8
            for y in range(8):
                for x in range(8):
                    v = tp[sx + (7 - x if hf else x), sy + (7 - y if vf else y)]
                    row = pn - 2
                    if v == 0 or row < 0:
                        c = (255, 0, 255)           # would show the backdrop colour (debug magenta)
                    else:
                        c = pal[row * 16 + v]
                    op[tx * 8 + x, ty * 8 + y] = c + (255,)
    return out


def scene(player="grovyle", enemy="zigzagoon", env="tall_grass", show_player=True, show_enemy=True,
          enemy_dx=0, player_dx=0, enemy_flash=False):
    out = environment(env)
    if show_enemy:
        spr = K.mon_front(enemy)
        if enemy_flash:
            spr = Image.new("RGBA", spr.size, (0, 0, 0, 0))
        K.place(out, spr, ENEMY_C[0] + enemy_dx, ENEMY_C[1] + SPECIES[enemy]["front_y"])
    if show_player:
        K.place(out, K.mon_back(player), PLAYER_C[0] + player_dx, PLAYER_C[1] + SPECIES[player]["back_y"])
    return out


# ------------------------------------------------------------------ big rounded shapes
def round_mask(w, h, r):
    """Filled rounded-rect mask with an arbitrary corner radius (pixel-circle corners)."""
    m = set()
    for y in range(h):
        for x in range(w):
            cx = min(max(x + 0.5, r), w - r)
            cy = min(max(y + 0.5, r), h - r)
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r:
                m.add((x, y))
    return m


def mask_box(cv, x0, y0, mask, face, outline=INK, light=WHITE, shade=PANEL_SHADE):
    """Gen 3 shading for any filled mask: 1px ink outline, light inner edge top/left, shade bottom/right."""
    edge = {p for p in mask if any((p[0] + dx, p[1] + dy) not in mask
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    for (x, y) in mask:
        c = face
        if (x, y) in edge:
            c = outline
        elif any((x + dx, y + dy) in edge for dx, dy in ((0, -1), (-1, 0))):
            c = light
        elif any((x + dx, y + dy) in edge for dx, dy in ((0, 1), (1, 0))):
            c = shade
        cv.set(x0 + x, y0 + y, c)
    return edge


def big_round_box(cv, x0, y0, w, h, r, face, outline=INK, light=WHITE, shade=PANEL_SHADE):
    return mask_box(cv, x0, y0, round_mask(w, h, r), face, outline, light, shade)


# ------------------------------------------------------------------ action-button icon fields
# White silhouettes (1px drop shadow in the field's dark tone) on BW-coded fields.
SILHOUETTES = {
    "fight": [            # boxing glove punching right: thumb seam + cuff
        "......XXXXXX....",
        "....XXXXXXXXXX..",
        "...XXXXXXXXXXXX.",
        "..XXXXXXXXXXXXXX",
        "..XXXXXXXXXXXXXX",
        ".XX..XXXXXXXXXXX",
        "XXXX..XXXXXXXXXX",
        "XXXXX..XXXXXXXXX",
        ".XXXXXXXXXXXXXX.",
        "..XXXXXXXXXXXX..",
        "................",
        "..XXXXXXXX......",
        "..XXXXXXXX......",
    ],
    "bag": [              # satchel: 2px handle, flap tip
        "...XXX...",
        "..XX.XX..",
        "XXXXXXXXX",
        "XXXXXXXXX",
        "XXX...XXX",
        "XXXXXXXXX",
        "XXXXXXXXX",
    ],
    "pokemon": [          # Poké Ball: 2-row band gap, 2x2 centre button
        "..XXXX..",
        ".XXXXXX.",
        "XXX..XXX",
        "...XX...",
        "...XX...",
        "XXX..XXX",
        ".XXXXXX.",
        "..XXXX..",
    ],
    "run": [              # sneaker (sole split off) + speed lines
        "...XXX....",
        "XX.XXXX...",
        "...XXXXX..",
        "XX.XXXXXXX",
        "...XXXXXXX",
        "XX........",
        "...XXXXXXX",
    ],
}


def silhouette(cv, x, y, rows, fg, shadow):
    for dx, dy, c in ((1, 1, shadow), (0, 0, fg)):
        for r, row in enumerate(rows):
            for q, ch in enumerate(row):
                if ch == "X":
                    cv.set(x + q + dx, y + r + dy, c)


# ================================================================== healthbox directions (round 3)
# Three layered designs, all OBJ (each <= 2x 64x32), all drawn with one healthbox palette
# laid out on kit role indices so text/panel code is shared:
#   1 INK  2 FRAME_DARK  3 WHITE  4 PANEL  5 PANEL_SHADE  6 PANEL_DARK  7 FRAME
#   8 NAME_MALE shadow  9 FRAME_LIGHT  10 NAME_MALE fg  11 BRASS_DARK  12 BRASS
#   13 BRASS_LIGHT  14 NAME_FEMALE fg (+ caught-ball red)  15 NAME_FEMALE shadow
from gamefont import draw_text, text_width, _font

FRAME_DARK, FRAME, FRAME_LIGHT = 2, 7, 9
# Gender is shown by the NAME colour (no ♂/♀ glyph). Shared with the party mockups:
# (fg, shadow), tuned for 1x on the light name pill; genderless = INK / PANEL_SHADE.
NAME_MALE = ((40, 80, 184), (168, 192, 232))
NAME_FEMALE = ((184, 48, 72), (232, 176, 184))
HB_MALE, HB_MALE_SH, HB_FEMALE, HB_FEMALE_SH = 10, 8, 14, 15
HB_ACCENT, HB_ACCENT_LIGHT = HB_MALE_SH, HB_FEMALE_SH     # legacy (frozen A/C emblem)
BRASS_DARK, BRASS, BRASS_LIGHT = 11, 12, 13
HB_PAL = [snap(c) for c in [
    (0, 0, 0), (40, 40, 64), (24, 24, 32), (248, 248, 248), (232, 232, 224), (192, 192, 184),
    (144, 144, 152), (56, 56, 72), NAME_MALE[1], (96, 104, 120), NAME_MALE[0],
    (160, 104, 40), (216, 168, 72), (248, 224, 144), NAME_FEMALE[0], NAME_FEMALE[1]]]


def hb_pal(flash=0.0):
    if not flash:
        return list(HB_PAL)
    return [snap(tuple(int(v + (248 - v) * flash) for v in c)) for c in HB_PAL]


def draw_code(cv, x, y, code, fg, shadow, font="small"):
    """One raw charmap glyph (0x34 = the ROM's Lv ligature, 0xB5/0xB6 = male/female)."""
    px, widths = _font(font)
    ox, oy = (code % 16) * 16, (code // 16) * 16
    w = widths[code]
    for gy in range(16):
        for gx in range(min(w, 16)):
            v = px[ox + gx, oy + gy]
            if v == 1:
                cv.set(x + gx, y + gy, fg)
            elif v == 2 and shadow is not None:
                cv.set(x + gx, y + gy, shadow)
    return x + w


CAUGHT = ["..III..",
          ".IRRRI.",
          "IRRRRRI",
          "IIIWIII",
          "IWWWWWI",
          ".IWWWI.",
          "..III.."]
ORCHID = [".A.A.",            # tiny orchid emblem (empty status socket)
          "AAAAA",
          ".AWA.",
          "AAAAA",
          ".A.A."]
MEANDER = ["XXX.", "X.X.", "X.XX"]   # 3-row square-wave key, period 4


def caught_ball(cv, x, y):
    stamp(cv, x, y, CAUGHT, {"I": INK, "R": HB_FEMALE, "W": WHITE})


def rivet(cv, x, y):
    cv.set(x, y, BRASS_LIGHT)
    cv.set(x + 1, y, BRASS)
    cv.set(x, y + 1, BRASS)
    cv.set(x + 1, y + 1, BRASS_DARK)


def chamfer_mask(w, h, tl=0, bl=0, tr=0, br=0):
    m = set()
    for y in range(h):
        for x in range(w):
            if x + y < tl or x + (h - 1 - y) < bl or (w - 1 - x) + y < tr or (w - 1 - x) + (h - 1 - y) < br:
                continue
            m.add((x, y))
    return m


def name_gender(cv, x, y, mon, fg=INK, sh=PANEL_SHADE):
    """Name in the gender colour (male blue / female rose / genderless ink); no gender glyph."""
    font = "small" if text_width(mon.name, "small") <= 50 else "narrow"
    if mon.gender == "M":
        fg, sh = HB_MALE, HB_MALE_SH
    elif mon.gender == "F":
        fg, sh = HB_FEMALE, HB_FEMALE_SH
    return draw_text(cv, x, y, mon.name, fg, sh, font=font)


def lv_text(cv, xr, y, lv, fg=INK, sh=PANEL_SHADE):
    """Right-aligned Lv ligature + number ending at xr."""
    _, widths = _font("small")
    wd = widths[0x34] + text_width(str(lv), "small")
    x = draw_code(cv, xr - wd, y, 0x34, fg, sh)
    draw_text(cv, x, y, str(lv), fg, sh, font="small")


def hp_numbers(mon):
    return "%d/%3d" % (mon.hp, mon.maxhp)


# ---------------------------------------------------------------- A: brass-trimmed chamfered frame
def hb_rect(variant, side):
    h = {"A": (28, 31), "B": (31, 32), "C": (28, 32)}[variant][side == "plr"]
    if side == "opp":
        return (4, 14, 128 if variant != "C" else 126, h)
    w = 128 if variant != "C" else 126
    return (240 - w - 2, 111 - h, w, h)


def hb_A(cv, mon, side, hp_shown=None):
    x, y, w, h = hb_rect("A", side)
    END = 20                                         # ornament / status end
    mask_box(cv, x, y, chamfer_mask(w, h, tl=3, bl=3, tr=6, br=6), FRAME, INK, FRAME_LIGHT, FRAME_DARK)
    px0, py0, px1, py1 = x + 4, y + 4, x + w - END - 1, y + 24
    # brass trim line around the plate
    for xx in range(px0, px1 + 1):
        cv.set(xx, py0 - 1, BRASS)
        cv.set(xx, py1 + 1, BRASS_DARK)
    for yy in range(py0, py1 + 1):
        cv.set(px0 - 1, yy, BRASS)
        cv.set(px1 + 1, yy, BRASS_DARK)
    rounded_box(cv, px0, py0, px1 - px0 + 1, py1 - py0 + 1, 2, PANEL, INK, WHITE, PANEL_SHADE)
    # end ornament = status socket: recessed ring with a brass boss (status icon covers it)
    cx, cy = x + w - END // 2 - 1, y + 14
    disc(cv, cx, cy, 9, FRAME_DARK, INK)
    ring(cv, cx, cy, 8, BRASS_DARK)
    ring(cv, cx, cy, 8, BRASS, 0.6)
    disc(cv, cx, cy, 3.5, BRASS, INK, BRASS_LIGHT, BRASS_DARK)
    rivet(cv, cx - 1, y + 2)
    rivet(cv, cx - 1, y + h - 4)
    # text
    name_gender(cv, px0 + 4, y + 2, mon)
    lv_text(cv, px1 - 4, y + 2, mon.lv)
    bar = (px0 + 16, y + 15)
    exp = None
    if side == "plr":
        s = hp_numbers(mon if hp_shown is None else mon.copy(hp=hp_shown))
        draw_text(cv, px1 - 4 - text_width(s, "small"), y + 10, s, INK, PANEL_SHADE, font="small")
        exp = (x + 6, x + w - END - 2, y + h - 4, "embedded")
    elif mon.caught:
        caught_ball(cv, px1 - 11, y + 14)
    return dict(bar=bar, status=(cx - 7, cy - 8), exp=exp)


# ---------------------------------------------------------------- B: stepped top tab + inset name pill
ORCHID6 = ["..AA..",           # 6x6 orchid gem for the empty status socket (even -> exact centre)
           ".AAAA.",
           "AAWWAA",
           "AAWWAA",
           ".AAAA.",
           "..AA.."]


def hb_B(cv, mon, side, hp_shown=None):
    """Stepped top tab (brass Lv / HP numbers) over a body with a pointed outer end
    (status socket), the name on its own inset pill, HP bar under the pill, EXP strip
    set into the bottom edge (player)."""
    x, y, w, h = hb_rect("B", side)
    TAB_W, TAB_H, BODY_Y = 72, 12, 8
    body = {(a, b + BODY_Y) for (a, b) in chamfer_mask(w, h - BODY_Y, tl=7, bl=7, tr=2, br=2)}
    tab = {(a + w - TAB_W, b) for (a, b) in chamfer_mask(TAB_W, TAB_H, tl=TAB_H - 3, tr=2)}
    mask_box(cv, x, y, body | tab, FRAME, INK, BRASS, FRAME_DARK)
    # status socket at the pointed end, centred on the body's inner rows
    inner0, inner1 = y + BODY_Y + 1, y + h - 2
    sy = inner0 + ((inner1 - inner0 + 1) - 16) // 2
    sx = x + 7
    rounded_box(cv, sx - 1, sy - 1, 18, 18, 3, FRAME_DARK, INK, FRAME_DARK, FRAME_LIGHT)
    for dx, dy in ((3, 3), (12, 3), (3, 12), (12, 12)):   # quiet corner studs, hidden by a status icon
        cv.set(sx + dx, sy + dy, FRAME)
    # name pill (13 tall: caps 3px below its top edge, clear of both bevels)
    px0, py0 = sx + 19, y + BODY_Y + 2
    pw = x + w - 5 - px0
    rounded_box(cv, px0, py0, pw, 13, 4, PANEL, INK, WHITE, PANEL_SHADE)
    name_gender(cv, px0 + 5, py0 - 1, mon)
    # tab text in brass: Lv at the right; HP numbers (player) or the caught ball (opp) before it
    lv_text(cv, x + w - 5, y - 2, mon.lv, BRASS_LIGHT, FRAME_DARK)
    _, widths = _font("small")
    lv_w = widths[0x34] + text_width(str(mon.lv), "small")
    if side == "plr":
        s = hp_numbers(mon if hp_shown is None else mon.copy(hp=hp_shown))
        draw_text(cv, x + w - 5 - lv_w - 7 - text_width(s, "small"), y - 2, s, BRASS_LIGHT, FRAME_DARK, font="small")
    elif mon.caught:
        caught_ball(cv, x + w - 5 - lv_w - 11, y + 2)
    bar = (px0 + 16, py0 + 14)
    exp = (px0, x + w - 6, y + h - 3, "embedded") if side == "plr" else None
    return dict(bar=bar, status=(sx, sy), exp=exp)


# ---------------------------------------------------------------- C: party disc + meander band
def hb_C(cv, mon, side, hp_shown=None):
    x, y, w, h = hb_rect("C", side)
    R = 12.5
    cx, cy = x + 13, y + h / 2
    sx0 = x + 13
    rounded_box(cv, sx0, y, w - 13, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
    # meander band along the top edge
    bx0, bx1 = sx0 + 12, x + w - 3
    cv.rect(bx0, y + 1, bx1, y + 5, FRAME)
    cv.hline(bx0, bx1, y + 1, FRAME_LIGHT)
    cv.hline(bx0 - 1, bx1, y + 6, INK)
    cv.hline(bx0, bx1, y + 7, WHITE)
    for xx in range(bx0 + 1, bx1 - 8):
        for r in range(3):
            if MEANDER[r][(xx - bx0) % 4] == "X":
                cv.set(xx, y + 2 + r, BRASS)
    if side == "opp" and mon.caught:
        caught_ball(cv, bx1 - 7, y)
    else:
        rivet(cv, bx1 - 5, y + 2)
    # status disc (party-row dais): dark socket, brass ring
    disc(cv, cx, cy, R, FRAME_DARK, INK)
    ring(cv, cx, cy, R - 1, BRASS_LIGHT)
    ring(cv, cx, cy, R - 2, BRASS)
    ring(cv, cx, cy, R - 3, BRASS_DARK)
    for (a, b) in ((cx + 7.5, cy + 7.5),):
        pass
    stamp(cv, int(cx) - 2, int(cy) - 2, ORCHID, {"A": HB_ACCENT, "W": HB_ACCENT_LIGHT})
    tx = sx0 + 14
    name_gender(cv, tx, y + 4, mon)
    lv_text(cv, x + w - 6, y + 4, mon.lv)
    bar = (tx + 12, y + 19)
    exp = None
    if side == "plr":
        s = hp_numbers(mon if hp_shown is None else mon.copy(hp=hp_shown))
        draw_text(cv, x + w - 6 - text_width(s, "small"), y + 14, s, INK, PANEL_SHADE, font="small")
        exp = (tx - 1, x + w - 6, y + h - 6, "framed")
    return dict(bar=bar, status=(int(cx) - 8, int(cy) - 8), exp=exp)


HB_DRAW = {"A": hb_A, "B": hb_B, "C": hb_C}


# ================================================================== party lineup (trainer battles)
# Orchid version of the vanilla party status summary (ball_status_bar.png + 6 ball_display.png
# sprites per side). Bar = healthbox-B language (dark frame, brass top trim, chamfered leading
# end) on HB_PAL; balls = 9x9 Gen 3 Poké Balls on their own OBJ palette (LINEUP_PAL, colours
# from graphics/items/icon_palettes/poke_ball.pal) + per-status dot colours.
LINEUP_PAL = [snap(c) for c in [
    (0, 0, 0), (49, 49, 49), (74, 82, 82), (123, 123, 131), (164, 164, 197), (222, 205, 246),
    (255, 255, 255), (156, 74, 57), (180, 82, 57), (222, 90, 57), (255, 148, 57),
    (192, 96, 192), (184, 176, 24), (160, 160, 136), (120, 168, 224), (232, 112, 80)]]
LU_STATUS = {"psn": 11, "tox": 11, "par": 12, "slp": 13, "frz": 14, "frb": 14, "brn": 15}
BALL9 = ["..IIIII..",
         ".IhllRRI.",
         "IhllllRdI",
         "IllRIRRdI",
         "IIIIWIIII",
         "IwwwIwwgI",
         "IwwwwwwgI",
         ".IwwwwgI.",
         "..IIIII.."]
_BALL_MAP = {"I": 1, "h": 10, "l": 9, "R": 8, "d": 7, "W": 6, "w": 6, "g": 4}
_BALL_DIM = {"I": 1, "h": 4, "l": 3, "R": 3, "d": 2, "W": 5, "w": 4, "g": 3}   # fainted: greyed
DOT = [".III.",
       "IsssI",
       "IsssI",
       "IsssI",
       ".III."]
LU_BAR_W, LU_BAR_H, LU_PITCH = 92, 16, 12


def lineup_bar(cv, x, y, side):
    """Bar sprite (3x 32x16 OBJ) on HB_PAL. side 'opp' = flush left, leading end right."""
    if side == "opp":
        m = chamfer_mask(LU_BAR_W + 6, LU_BAR_H, tr=LU_BAR_H - 4, br=2)
        mask_box(cv, x - 6, y, m, FRAME, INK, BRASS, FRAME_DARK)
    else:
        m = chamfer_mask(LU_BAR_W + 6, LU_BAR_H, tl=LU_BAR_H - 4, bl=2)
        mask_box(cv, x, y, m, FRAME, INK, BRASS, FRAME_DARK)
    for i in range(6):
        sx, sy = lineup_socket(x, y, side, i)
        disc(cv, sx + 5.5, sy + 5.5, 5.5, FRAME_DARK, INK)
        cv.set(sx + 8, sy + 9, FRAME_LIGHT)
        cv.set(sx + 9, sy + 8, FRAME_LIGHT)


def lineup_socket(x, y, side, k):
    """Top-left of socket k (k = 0 nearest the screen centre, as vanilla orders the party)."""
    if side == "opp":
        return x + LU_BAR_W - 22 - 11 - k * LU_PITCH + 6, y + 3
    return x + 16 + k * LU_PITCH, y + 3


def lineup_ball(cv, x, y, state):
    """state: ok | fnt | empty | psn/par/slp/frz/brn/tox/frb. (x, y) = socket top-left."""
    if state == "empty":
        return
    cmap = _BALL_DIM if state == "fnt" else _BALL_MAP
    stamp(cv, x + 1, y + 1, BALL9, cmap)
    if state in LU_STATUS:
        stamp(cv, x + 7, y + 7, DOT, {"I": 1, "s": LU_STATUS[state]})   # status dot, lower right
