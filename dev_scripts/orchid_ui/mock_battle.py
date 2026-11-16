"""
Orchid battle UI — pixel-accurate mockups ("Gen 5 layout, Gen 3 pixels"), round 2.

Everything sits where vanilla puts it, so the Mode 7 floor (mode 1, BG2 affine)
on the engine branch keeps working:
  * BG0  bottom tray y 112..159 (vanilla textbox area): BW near-black grid (static
         tiles), message box, action menu, move select, YES/NO. BG palettes 0 (tray +
         panels, kit roles + grid colours) and 5 (menu windows: kit roles + PP colours).
         Rows 10..15 are never touched.
  * OBJ  healthboxes (round 3: three layered directions, battle_ext.hb_A/B/C) at the vanilla singles spots, HP/EXP bars,
         status icons (status_icons.py), action-button icon fields, Gen 3 type icons.
  * scene: vanilla battle environment + battlers (the Mode 7 floor on the engine branch).

usage: mock_battle.py OUT_DIR      (writes main.png, state_XX.png, parts.png,
                                    status_icons.png, notes.json)
"""
import json
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as K
import windows as Wn
from gamefont import draw_text, text_width
from backdrop import GRID_PAL, grid_index, GRID_BASE, GRID_MINOR, GRID_MAJOR
import battle_ext as BX
import status_icons as SI

W, H = 240, 160
THEME = "orchid"


# ================================================================== data
class Mon:
    def __init__(self, species, name, lv, hp, maxhp, gender=None, status=None, exp=0.0, caught=False):
        self.species, self.name, self.lv = species, name, lv
        self.hp, self.maxhp, self.gender, self.status = hp, maxhp, gender, status
        self.exp, self.caught = exp, caught

    def copy(self, **kw):
        m = Mon(self.species, self.name, self.lv, self.hp, self.maxhp, self.gender, self.status,
                self.exp, self.caught)
        for k, v in kw.items():
            setattr(m, k, v)
        return m


MOVES = [  # name, type, pp, maxpp  (Grovyle's Emerald moves around Lv 18)
    ("Absorb", "grass", 23, 25),
    ("Quick Attack", "normal", 6, 30),
    ("Pursuit", "dark", 9, 20),
    ("Fury Cutter", "bug", 20, 20),
]
ACTIONS = ["FIGHT", "BAG", "POKéMON", "RUN"]


def default_player():
    return Mon("grovyle", "Grovyle", 18, 48, 52, "M", exp=0.62)


def default_enemy():
    return Mon("zigzagoon", "Zigzagoon", 7, 24, 24, "F", caught=True)


# ================================================================== palettes
# BG pal 0: kit roles; SPARE_A / SPARE_B = BW grid base / major line (minor line = INK).
GRID_BG, GRID_LINE = SPARE_A, SPARE_B
UI_PAL = palette(THEME, spare_a=GRID_PAL[GRID_BASE], spare_b=GRID_PAL[GRID_MAJOR])
_GRID_MAP = {GRID_BASE: GRID_BG, GRID_MINOR: INK, GRID_MAJOR: GRID_LINE}

# BG pal 5 (menu windows): kit roles; PP warning colours from text_pp.pal in the free slots.
PP_FG = {3: (248, 248, 248), 0: (216, 200, 0), 1: (248, 128, 0), 2: (232, 24, 0)}
PP_YELLOW, PP_ORANGE, PP_RED = ACCENT_PALE, SPARE_A, SPARE_B
MENU_PAL = palette(THEME, spare_a=PP_FG[1], spare_b=PP_FG[2])
MENU_PAL[PP_YELLOW] = snap(PP_FG[0])
PP_INDEX = {3: WHITE, 0: PP_YELLOW, 1: PP_ORANGE, 2: PP_RED}


def pp_state(pp, maxpp):
    """GetCurrentPPToMaxPPState (battle_message.c): 3 normal, 0 <= 1/2, 1 <= 1/4, 2 empty."""
    if maxpp == pp:
        return 3
    if maxpp <= 2:
        return 3 if pp > 1 else 2 - pp
    if maxpp <= 7:
        return 3 if pp > 2 else 2 - pp
    if pp == 0:
        return 2
    if pp <= maxpp // 4:
        return 1
    if pp > maxpp // 2:
        return 3
    return 0


# OBJ healthbar palette (HP/EXP fills + HP tag) — separate, like vanilla TAG_HEALTHBAR_PAL.
HB_I = {"ink": 1, "trough": 2, "trough_hi": 3, "g1": 4, "g2": 5, "y1": 6, "y2": 7,
        "r1": 8, "r2": 9, "e1": 10, "e2": 11, "tag": 12, "white": 13}
HBAR_PAL = [snap(c) for c in [
    (0, 0, 0), (40, 40, 64), (144, 144, 152), (120, 120, 136),
    K.HP_GREEN[0], K.HP_GREEN[1], K.HP_YELLOW[0], K.HP_YELLOW[1],
    K.HP_RED[0], K.HP_RED[1], K.EXP_BLUE[0], K.EXP_BLUE[1],
    (96, 48, 128), (248, 248, 248), (0, 0, 0), (0, 0, 0)]]

# OBJ action-button palette: BW colour coding as Gen 3 3-step ramps (light, face, dark).
BTN_RAMPS = {
    "red": ((248, 160, 136), (224, 80, 64), (152, 32, 48)),
    "yellow": ((248, 224, 120), (224, 168, 32), (152, 96, 16)),
    "green": ((160, 224, 120), (80, 168, 72), (32, 104, 56)),
    "blue": ((152, 192, 248), (72, 128, 216), (40, 72, 152)),
}
BTN_ORDER = ["red", "yellow", "green", "blue"]
BTN_PAL = [snap(c) for c in [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
           + [c for k in BTN_ORDER for c in BTN_RAMPS[k]] + [(0, 0, 0)]]


def btn_idx(colour, step):   # step 0 light, 1 face, 2 dark
    return 3 + BTN_ORDER.index(colour) * 3 + step


# ================================================================== helpers
def p_sheet(w, h, pal):
    im = Image.new("P", (w, h), 0)
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def comp(out, im, pal=None, at=(0, 0)):
    out.alpha_composite(K.sheet_rgba(im, pal), at)


def wrap(text, width, font="normal"):
    """Greedy word wrap like the expansion's automatic battle-string line breaks."""
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if text_width(t, font) <= width or not line:
                line = t
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


HP_GLYPH = ["X.X.XX.",
            "X.X.X.X",
            "XXX.XX.",
            "X.X.X..",
            "X.X.X.."]
B_GLYPH = ["XXX.",
           "X..X",
           "XXX.",
           "X..X",
           "XXX."]

# ================================================================== BG0 tray
TRAY = BX.TRAY_Y                 # 112: vanilla textbox area, tile rows 14..19
TOP, BOT = TRAY + 2, H - 3       # usable rows inside the tray (114..157)
MSG_X, MSG_Y, MSG_W = 16, 120, 26 * 8      # B_WIN_MSG text rect (tiles 2,15 26x4)


def draw_tray(cv):
    """Static tray: BW near-black grid (same colours as the party/bag BG3 grid), ink top edge
    with a grid-line highlight under it. Static tiles on BG0 (grid repeats every 2x2 tiles)."""
    for y in range(TRAY, H):
        for x in range(W):
            cv.set(x, y, _GRID_MAP[grid_index(x, y)])
    cv.hline(0, W - 1, TRAY, INK)
    cv.hline(0, W - 1, TRAY + 1, GRID_LINE)


def msg_panel(cv, x0, x1):
    """Message panel on the tray: white rounded box; each end carries a quiet column of three
    2x2 brass rivets (gold ramp of BG pal 0) echoing healthbox B, instead of purple end-caps."""
    h = BOT - TOP + 1
    rounded_box(cv, x0, TOP, x1 - x0 + 1, h, 3, WHITE, INK, WHITE, PANEL_SHADE)
    cy = TOP + h // 2
    for rx in (x0 + 5, x1 - 6):
        for ry in (cy - 9, cy - 1, cy + 7):
            cv.set(rx, ry, SELECT_LIGHT)
            cv.set(rx + 1, ry, SELECT)
            cv.set(rx, ry + 1, SELECT)
            cv.set(rx + 1, ry + 1, SELECT_DARK)
    cv.hline(x0 + 11, x1 - 8, BOT - 3, PANEL_SHADE)


def draw_back_tab(cv, label="BACK"):
    """Small near-black tab rising from the tray's top-left corner: B-button hint."""
    tw = text_width(label, "small")
    x1, y0 = 18 + tw, TRAY - 11
    ins = lambda r: {0: 3, 1: 1, 2: 1}.get(r, 0)
    for y in range(y0, TRAY + 2):
        cv.hline(0, x1 - ins(y - y0), y, GRID_BG)
        cv.set(x1 - ins(y - y0), y, INK)
    cv.hline(0, x1 - ins(0), y0, INK)
    cv.hline(0, x1 - ins(1) - 1, y0 + 1, GRID_LINE)
    cv.set(x1 - 2, y0 + 1, INK)
    cv.hline(x1 - 1, x1 + 1, TRAY, INK)
    cv.set(x1, TRAY + 1, GRID_LINE)
    cv.set(x1 + 1, TRAY + 1, GRID_LINE)
    cv.hline(0, x1 - 1, TRAY, GRID_BG)          # open into the tray
    cv.hline(0, x1 - 1, TRAY + 1, GRID_BG)
    disc(cv, 8, y0 + 6, 5, WHITE, INK, None, PANEL_SHADE)
    stamp(cv, 6, y0 + 4, B_GLYPH, {"X": INK})
    draw_text(cv, 15, y0 - 1, label, WHITE, INK, font="small")


# ---------------------------------------------------------------- action menu
# BG0 window (pal 5): button faces + labels, gold face when selected.
# OBJ (BTN_PAL): the coloured icon fields with white silhouettes — they never change colour.
FIGHT_BTN = (130, TOP, 44, 44)                 # big round BW-style button
FIGHT_R = 12
FIGHT_FIELD = (136, TOP + 3, 32, 22)           # red field, OBJ 32x32
SIDE_X, SIDE_W = 177, 61
SIDE_Y = [TOP, TOP + 15, TOP + 30]             # 14px pills, 1px gap
SIDE_FIELD_W = 16                              # 16x14 field = pill's left end, OBJ 16x16
BTN_COL = ["red", "yellow", "green", "blue"]
BTN_ICON = ["fight", "bag", "pokemon", "run"]


def side_rect(i):
    return SIDE_X, SIDE_Y[i], SIDE_W, 14


def draw_action(cv, cursor):
    x, y, w, h = FIGHT_BTN
    sel = cursor == 0
    face, lt, sh = (SELECT, SELECT_LIGHT, SELECT_DARK) if sel else (PANEL, WHITE, PANEL_SHADE)
    BX.big_round_box(cv, x, y, w, h, FIGHT_R, face, INK, lt, sh)
    draw_text(cv, x + (w - text_width("FIGHT")) // 2 + 1, y + 25, "FIGHT", INK, PANEL_SHADE)
    for i in range(3):
        x, y, w, h = side_rect(i)
        if cursor == i + 1:
            Wn.selection_bar(cv, x, y, w, h)
        else:
            rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
        draw_text(cv, x + SIDE_FIELD_W + 3, y - 1, ACTIONS[i + 1], INK, PANEL_SHADE, font="narrow")


def draw_field(cv, x, y, w, h, colour, icon, r=3):
    rounded_box(cv, x, y, w, h, r, btn_idx(colour, 1), 1, btn_idx(colour, 0), btn_idx(colour, 2))
    rows = BX.SILHOUETTES[icon]
    pw, ph = len(rows[0]) + 1, len(rows) + 1           # + drop shadow
    BX.silhouette(cv, x + (w - pw + 1) // 2, y + (h - ph + 1) // 2, rows, 2, btn_idx(colour, 2))


def button_fields(out):
    im = p_sheet(W, H, BTN_PAL)
    cv = Canvas(im)
    draw_field(cv, *FIGHT_FIELD, "red", "fight", r=4)
    for i in range(3):
        x, y, w, h = side_rect(i)
        draw_field(cv, x, y, SIDE_FIELD_W, h, BTN_COL[i + 1], BTN_ICON[i + 1])
    comp(out, im)


# ---------------------------------------------------------------- move select (BG0 window, pal 5)
MOVE_W, MOVE_H = 116, 22
MOVE_POS = [(3, TOP), (121, TOP), (3, TOP + 23), (121, TOP + 23)]


def draw_move_pill(cv, x, y, move, selected):
    name, typ, pp, mx = move
    if selected:
        Wn.selection_bar(cv, x, y, MOVE_W, MOVE_H)
    else:
        rounded_box(cv, x, y, MOVE_W, MOVE_H, 4, PANEL, INK, WHITE, PANEL_SHADE)
    f = "normal" if text_width(name) <= MOVE_W - 42 else "narrow"
    draw_text(cv, x + 38, y - 1, name, INK, PANEL_SHADE, font=f)
    # PP counter = ink notch in the pill's bottom edge (approved): text_pp.pal warning colours
    num = "%d/%d" % (pp, mx)
    tw = text_width("PP " + num, "small")
    px = x + MOVE_W - 9 - tw
    nx0, nx1 = px - 4, x + MOVE_W - 5
    cv.rect(nx0, y + 12, nx1, y + MOVE_H - 1, INK)
    cv.set(nx0, y + 12, cv.get(nx0, y + 11))
    cv.set(nx1, y + 12, cv.get(nx1, y + 11))
    draw_text(cv, px, y + 9, "PP", PANEL_DARK, None, font="small")
    draw_text(cv, px + text_width("PP ", "small"), y + 9, num, PP_INDEX[pp_state(pp, mx)], None, font="small")


def draw_moves(cv, moves, cursor):
    for i, mv in enumerate(moves):
        draw_move_pill(cv, *MOVE_POS[i], mv, i == cursor)


def type_icons(out, moves):
    for i, mv in enumerate(moves):
        x, y = MOVE_POS[i]
        out.alpha_composite(K.type_icon(mv[1]), (x + 3, y + 3))


# ---------------------------------------------------------------- YES/NO (approved: docked in the tray)
YESNO_T = (25, 15, 4, 4)    # text rect in tiles; frame = x 192..239, y 112..159
YESNO_MSG_W = 20 * 8          # text must stop before the panel end-cap at x 183


def draw_yesno(cv, cursor):
    tx, ty, tw, th = YESNO_T
    for i, t in enumerate(("YES", "NO")):
        y = ty * 8 + i * 16
        if i == cursor:
            Wn.selection_bar(cv, tx * 8 + 2, y + 1, tw * 8 - 4, 14)
        draw_text(cv, tx * 8 + 8, y, t, INK, PANEL_SHADE)


# ================================================================== healthboxes (OBJ)
# Round 3: three layered directions live in battle_ext (hb_A / hb_B / hb_C), all on one
# healthbox OBJ palette (BX.HB_PAL: dark frame + brass trim + kit panel roles).
# Bars use the separate healthbar palette; status = status_icons.py (16x16 OBJ).
HB_VARIANT = "B"              # chosen by the user in round 3


def box_rect(side, variant=None):
    return BX.hb_rect(variant or HB_VARIANT, side)


def draw_bars(cv, mon, anchors, hp=None, exp=None):
    """HP tag (party style) + 48px HP bar (+ EXP strip on the player box), healthbar palette."""
    hp = mon.hp if hp is None else hp
    exp = mon.exp if exp is None else exp
    bar_x, bar_y = anchors["bar"]
    tx, ty = bar_x - 12, bar_y - 1
    rounded_box(cv, tx, ty, 11, 7, 1, HB_I["tag"], HB_I["tag"], HB_I["tag"], HB_I["tag"], bevel=False)
    stamp(cv, tx + 2, ty + 1, HP_GLYPH, {"X": HB_I["white"]})
    lvl, n = hp_level(hp, mon.maxhp)
    cv.rect(bar_x, bar_y, bar_x + 49, bar_y + 4, HB_I["ink"])
    cv.rect(bar_x + 1, bar_y + 1, bar_x + 48, bar_y + 3, HB_I["trough"])
    cv.hline(bar_x + 1, bar_x + 48, bar_y + 1, HB_I["trough_hi"])
    if n:
        cv.rect(bar_x + 1, bar_y + 1, bar_x + n, bar_y + 3, HB_I[lvl + "2"])
        cv.hline(bar_x + 1, bar_x + n, bar_y + 1, HB_I[lvl + "1"])
    if anchors.get("exp"):
        ex0, ex1, ey, style = anchors["exp"]
        if style == "framed":           # ink-framed strip on the panel
            cv.rect(ex0, ey, ex1, ey + 3, HB_I["ink"])
            ey += 1
            ex0, ex1 = ex0 + 1, ex1 - 1
        cv.hline(ex0, ex1, ey, HB_I["trough"])
        cv.hline(ex0, ex1, ey + 1, HB_I["trough_hi"])
        n = int(round((ex1 - ex0 + 1) * max(0.0, min(1.0, exp))))
        if n:
            cv.hline(ex0, ex0 + n - 1, ey, HB_I["e1"])
            cv.hline(ex0, ex0 + n - 1, ey + 1, HB_I["e2"])


def exp_strip_px(variant=None):
    an = BX.HB_DRAW[variant or HB_VARIANT](Canvas(p_sheet(W, H, BX.HB_PAL)), default_player(), "plr")
    ex0, ex1, ey, style = an["exp"]
    return ex1 - ex0 + 1 - (2 if style == "framed" else 0)


def hp_level(hp, maxhp, pixels=48):
    """Gen 3 GetHPBarLevel: thresholds are in bar pixels (>24 green, >9 yellow, else red)."""
    px = 0 if hp <= 0 else max(1, hp * pixels // maxhp)
    return ("g" if px > 24 else "y" if px > 9 else "r"), px


def healthboxes(out, player, enemy, show=("opp", "plr"), hp=None, exp=None, flash=None, variant=None):
    hp, flash = hp or {}, flash or {}
    draw = BX.HB_DRAW[variant or HB_VARIANT]
    for side, mon in (("opp", enemy), ("plr", player)):
        if side not in show or mon is None:
            continue
        box = p_sheet(W, H, BX.hb_pal(flash.get(side, 0)))
        an = draw(Canvas(box), mon, side)
        comp(out, box)
        bars = p_sheet(W, H, HBAR_PAL)
        draw_bars(Canvas(bars), mon, an, hp.get(side), exp if side == "plr" else None)
        comp(out, bars)
        status = mon.status or ("fnt" if (hp.get(side, mon.hp) or 0) <= 0 else None)
        if status:
            out.alpha_composite(SI.status_icon(status.lower()), an["status"])


# ================================================================== render
# ================================================================== party lineup (trainer battles)
# Vanilla: CreatePartyStatusSummarySprites — opponent bar at (104, 40) [balls at y 36],
# player bar at (136, 96) [balls at y 92]; balls ordered from the screen centre outward,
# empty slots at the screen edge.
LU_POS = {"opp": (0, 28), "plr": (240 - BX.LU_BAR_W, 84)}


def lineup_layer(out, side, slots, bar_dx=0, ball_dx=None, alpha=1.0):
    """slots: 6 states, k = 0 nearest the screen centre. ball_dx: per-ball x offset (anim)."""
    x, y = LU_POS[side]
    frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bar = p_sheet(W, H, BX.HB_PAL)
    BX.lineup_bar(Canvas(bar), x + bar_dx, y, side)
    comp(frame, bar)
    balls = p_sheet(W, H, BX.LINEUP_PAL)
    bc = Canvas(balls)
    for k, st in enumerate(slots):
        if ball_dx is not None and ball_dx[k] is None:
            continue
        sx, sy = BX.lineup_socket(x, y, side, k)
        BX.lineup_ball(bc, sx + (ball_dx[k] if ball_dx else bar_dx), sy, st)
    comp(frame, balls)
    if alpha < 1.0:
        a = frame.getchannel("A").point(lambda v: int(v * alpha))
        frame.putalpha(a)
    out.alpha_composite(frame)


def intro_scene(env="tall_grass", trainer="youngster", player_back="brendan", trainer_dx=0):
    """Trainer battle intro: both trainers at the battler spots, no mons / healthboxes yet."""
    out = BX.environment(env)
    K.place(out, K.sprite_rgba(K.G("trainers", "front_pics", trainer + ".png")), BX.ENEMY_C[0] + trainer_dx, BX.ENEMY_C[1])
    back = K.sprite_rgba(K.G("trainers", "back_pics", player_back + ".png"), 0, 64)
    K.place(out, back, 80, 80)
    return out


def render(mode="action", cursor=0, msg=None, player=None, enemy=None, moves=None, yesno=0,
           show_enemy=True, show_boxes=("opp", "plr"), hp=None, exp=None, env="tall_grass",
           enemy_visible=True, ball=False, flash=None, chars=None, variant=None,
           intro=False, lineups=None):
    """mode: msg | action | moves | yesno.  chars = number of message characters printed.
    intro = trainer-battle intro scene (no mons / healthboxes). lineups = {side: (slots, kwargs)}."""
    player = player or default_player()
    enemy = enemy if enemy is not None else default_enemy()
    moves = moves or MOVES
    if intro:
        out = intro_scene(env)
    else:
        out = BX.scene(player.species, enemy.species, env, show_enemy=show_enemy and enemy_visible)
    if ball:   # caught: closed Poké Ball resting on the enemy spot
        K.place(out, K.sprite_rgba(K.G("balls", "poke.png"), 0, 16), BX.ENEMY_C[0], BX.ENEMY_C[1] + 30)
    if not intro:
        healthboxes(out, player, enemy if show_enemy else None, show_boxes, hp, exp, flash, variant)
    for side, (slots, kw) in (lineups or {}).items():
        lineup_layer(out, side, slots, **kw)

    bg = p_sheet(W, H, UI_PAL)          # BG0 static tilemap art, pal 0
    cv = Canvas(bg)
    draw_tray(cv)
    if mode in ("msg", "yesno"):
        msg_panel(cv, 2, 237 if mode == "msg" else 189)
        if mode == "yesno":
            Wn.std_frame(cv, *YESNO_T)
        lines = wrap(msg or "", MSG_W if mode == "msg" else YESNO_MSG_W)[-2:]
        text = "\n".join(lines)
        if chars is not None:
            text = text[:chars]
        draw_text(cv, MSG_X, MSG_Y, text, INK, PANEL_SHADE)
    elif mode == "action":
        msg_panel(cv, 2, 126)
        draw_text(cv, MSG_X, MSG_Y, msg or "What will\n%s do?" % player.name, INK, PANEL_SHADE)
    elif mode == "moves":
        draw_back_tab(cv)
    comp(out, bg)

    win = p_sheet(W, H, MENU_PAL)       # BG0 menu windows, pal 5
    wc = Canvas(win)
    if mode == "action":
        draw_action(wc, cursor)
    elif mode == "moves":
        draw_moves(wc, moves, cursor)
    elif mode == "yesno":
        draw_yesno(wc, yesno)
    comp(out, win)
    if mode == "action":
        button_fields(out)
    elif mode == "moves":
        type_icons(out, moves)
    return out


# ================================================================== sheets
def healthbox_sheet():
    """266x200: opponent variants (left) + player variants (right) on the battle sky colour."""
    SW, SH = 266, 200
    out = Image.new("RGBA", (SW, SH), BX.environment().getpixel((4, 60)))
    zig = default_enemy()
    opp = [
        zig.copy(),                                                    # full, caught ball
        zig.copy(hp=11, status="PSN", caught=False),                   # yellow + PSN
        zig.copy(hp=3, status="PAR"),                                  # red + PAR
        Mon("beldum", "Beldum", 12, 30, 30, None, status="SLP"),       # genderless
        Mon("wurmple", "Wurmple", 3, 14, 15, "M", status="BRN"),
        Mon("poochyena", "Poochyena", 9, 0, 28, "M"),                  # fainted -> FNT icon
    ]
    gro = default_player()
    plr = [
        gro.copy(hp=52, exp=0.94),                                     # full, EXP nearly full
        gro.copy(hp=24, status="FRZ", gender="F", exp=0.30),
        gro.copy(hp=7, status="TOX", exp=0.62),                        # low (red), badly poisoned
        Mon("treecko", "Treecko", 9, 31, 31, None, status="PKRS", exp=0.05),
        Mon("treecko", "Treecko", 9, 12, 31, "M", status="FRB", exp=0.5),
    ]
    ox, oy, ow, oh = box_rect("opp")
    for i, m in enumerate(opp):
        f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        healthboxes(f, None, m, ("opp",))
        out.alpha_composite(f.crop((0, oy, 132, oy + oh)), (0, 4 + i * 32))
    px, py, pw, ph = box_rect("plr")
    for i, m in enumerate(plr):
        f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        healthboxes(f, m, None, ("plr",))
        out.alpha_composite(f.crop((108, py, 240, py + ph)), (134, 4 + i * 38))
    return out


def box_closeup(variant, player=None, enemy=None):
    """Both healthboxes of a variant on the battle scene, cropped side by side (1x)."""
    f = BX.environment()
    healthboxes(f, player or default_player(), enemy or default_enemy(), variant=variant)
    ox, oy, ow, oh = box_rect("opp", variant)
    px, py, pw, ph = box_rect("plr", variant)
    out = Image.new("RGBA", (268, 36), (28, 28, 36, 255))
    out.alpha_composite(f.crop((0, oy - 2, 132, oy + 34)), (0, 0))
    out.alpha_composite(f.crop((106, py - 2, 240, py + 34 if py + 34 <= 112 else 112)), (134, 0))
    return out


HB_IDEAS = {
    "A": "A: brass-trimmed chamfered frame - dark frame, brass trim line, panel plate, ornament end that doubles as the status socket",
    "B": "B: stepped top tab + inset name pill - Lv / HP numbers on a brass-lettered tab, name on its own pill, pointed end with status socket",
    "C": "C: meander band + party disc - party-row slab with a brass greek-key band, rivet, and the party dais as a brass-ringed status disc",
}


def variants_sheet():
    """healthbox_variants.png: per variant a 2x full frame (state 1) + 4x close-up of both boxes."""
    S2, S4 = 2, 4
    rows = []
    for v in "ABC":
        full = K.upscale(render("action", 0, variant=v, player=default_player().copy(status="PSN")), S2)
        cu = K.upscale(box_closeup(v, default_player().copy(status="PSN")), S4)
        cu2 = K.upscale(box_closeup(v, default_player().copy(hp=7, exp=0.9),
                                    default_enemy().copy(hp=11, caught=False, status="PAR")), S4)
        rows.append((v, full, cu, cu2))
    Wd = 16 + 480 + 16 + 268 * S4 + 16
    Hd = 16 + len(rows) * (24 + 320 + 24)
    sheet = Image.new("RGBA", (Wd, Hd), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    y = 16
    for v, full, cu, cu2 in rows:
        d.text((16, y), HB_IDEAS[v] + ("   [recommended]" if v == HB_VARIANT else ""), fill=(240, 220, 150) if v == HB_VARIANT else (230, 230, 240))
        sheet.alpha_composite(full, (16, y + 20))
        sheet.alpha_composite(cu, (16 + 480 + 16, y + 20))
        sheet.alpha_composite(cu2, (16 + 480 + 16, y + 20 + cu.size[1] + 8))
        y += 24 + 320 + 24
    return sheet


def parts_sheet():
    """4x sheet of the new pieces with their palettes."""
    S = 4
    sheet = Image.new("RGBA", (266 * S + 2 * 16, 1500), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    y = 12

    def put(img, x, y, caption):
        d.text((x, y), caption, fill=(230, 230, 240))
        sheet.alpha_composite(K.upscale(img, S), (x, y + 14))
        return y + 14 + img.size[1] * S + 14

    sky = BX.environment().getpixel((4, 60))
    hb = box_closeup(HB_VARIANT, enemy=default_enemy().copy(status="PSN"))
    y = put(hb, 16, y, "Healthboxes, direction B (OBJ 2x 64x32 each): stepped tab with brass Lv / HP numbers / caught ball, pointed end with status socket (quiet corner studs when empty), name (gender-coloured) on an inset pill, HP bar under it, EXP strip in the bottom edge")
    a0 = render("action", 0).crop((0, TRAY - 2, W, H))
    y = put(a0, 16, y, "Action menu: grid tray (BG0 pal 0) + button faces/labels (window, pal 5) + icon fields (OBJ: FIGHT 32x32, others 16x16, one palette)")
    a1 = render("action", 2).crop((120, TRAY - 2, W, H))
    a2 = Image.new("RGBA", (W, a1.size[1]), (28, 28, 36, 255))
    a2.alpha_composite(a1, (0, 0))
    big = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    bc = p_sheet(64, 32, BTN_PAL)
    cv = Canvas(bc)
    draw_field(cv, 0, 0, 32, 22, "red", "fight", r=4)
    for i in range(3):
        draw_field(cv, 34 + (i % 2) * 18, (i // 2) * 16, 16, 14, BTN_COL[i + 1], BTN_ICON[i + 1])
    big.alpha_composite(K.sheet_rgba(bc))
    a2.alpha_composite(big, (130, 4))
    y = put(a2, 16, y, "POKéMON selected (gold face, green field stays) + the four icon fields on their own")
    m1 = render("moves", 0).crop((0, TRAY - 12, W, H))
    y = put(m1, 16, y, "Move select: two-line pills, Gen 3 type icon (OBJ 32x16), PP notch with text_pp.pal colours; BACK tab on the grid tray")
    lu = Image.new("RGBA", (W, 28), (88, 96, 112, 255))
    f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lineup_layer(f, "opp", ["ok", "psn", "fnt", "empty", "brn", "par"])
    lineup_layer(f, "plr", ["ok", "slp", "frz", "tox", "fnt", "empty"])
    lu.alpha_composite(f.crop((0, LU_POS["opp"][1] - 2, 120, LU_POS["opp"][1] + 18)), (0, 0))
    lu.alpha_composite(f.crop((120, LU_POS["plr"][1] - 2, 240, LU_POS["plr"][1] + 18)), (120, 8))
    y = put(lu, 16, y, "Party lineup (trainer battles): bar = 3x 32x16 OBJ on the healthbox palette; balls = 16x16 OBJ each on LINEUP_PAL. States: ready, statused (status-colour dot), fainted (greyed), empty socket")
    d.text((16, y), "Palettes", fill=(230, 230, 240))
    y += 16
    for label, pal in (("BG 0  tray + panels (kit orchid; 14 grid base, 15 grid line, 1 = minor line)", UI_PAL),
                       ("BG 5  menu windows (kit; 10 PP yellow, 14 PP orange, 15 PP red)", MENU_PAL),
                       ("OBJ  healthbox (2/7/9 frame dark/mid/light, 11-13 brass, 10 male, 14 female/ball, 8/15 orchid)", BX.HB_PAL),
                       ("OBJ  healthbar (HP ramps, EXP blue, HP tag)", HBAR_PAL),
                       ("OBJ  action icon fields (red / yellow / green / blue)", BTN_PAL),
                       ("OBJ  status icons (status_icons.STATUS_PAL)", SI.STATUS_PAL),
                       ("OBJ  lineup balls (poke_ball.pal + 5 status dots)", BX.LINEUP_PAL)):
        for i, c in enumerate(pal):
            d.rectangle((16 + i * 30, y, 16 + i * 30 + 26, y + 26), fill=tuple(c), outline=(60, 60, 70))
            d.text((16 + i * 30 + 2, y + 28), str(i), fill=(160, 160, 170))
        d.text((16 + 16 * 30 + 8, y + 6), label, fill=(230, 230, 240))
        y += 46
    return sheet.crop((0, 0, sheet.size[0], y + 8))


# ================================================================== states
def states():
    P, E = default_player(), default_enemy()
    S = []
    S.append(("state_01.png", "Action menu — FIGHT", render("action", 0),
              "Black grid tray. FIGHT = big round button with a red field + fist; BAG / POKéMON / RUN pills open with "
              "a yellow bag, green ball, blue shoe field. Selection turns the button face gold; the icon fields keep their colour."))
    S.append(("state_02.png", "Action menu — RUN", render("action", 3),
              "RUN selected: gold pill, blue shoe field unchanged."))
    S.append(("state_03.png", "Move select", render("moves", 0),
              "2x2 two-line pills on the black tray: Gen 3 type icon, name, PP notch (Quick Attack 6/30 orange, "
              "Pursuit 9/20 yellow). B / BACK tab restyled for the grid."))
    S.append(("state_04.png", "Battle message", render("msg", msg="The wild Zigzagoon had its energy drained!"),
              "Full-width message box on the tray (B_WIN_MSG rect, 16px pitch); both healthboxes (direction B) visible."))
    S.append(("state_05.png", "Healthbox variants", healthbox_sheet(),
              "Direction B. Left: opponent — full + caught ball (on the tab, before Lv; empty status socket = plain recess), yellow + PSN (not caught), red + PAR, genderless + SLP, "
              "BRN, fainted (FNT icon). Right: player — EXP nearly full, female + FRZ, red + TOX, genderless + PKRS, FRB."))
    S.append(("state_06.png", "YES/NO — nickname",
              render("yesno", msg="Would you like to give Zigzagoon a nickname?", show_enemy=False, ball=True),
              "Std frame + gold pill docked in the tray's right end; message narrows to 20 tiles. The caught ball rests on the enemy spot."))
    pooch = Mon("poochyena", "Poochyena", 9, 28, 28, "M")
    S.append(("state_07.png", "Switch prompt",
              render("yesno", msg="Youngster Calvin is about to send out Poochyena. Will you switch your Pokémon?",
                     enemy=pooch, show_enemy=False),
              "Trainer battle, foe's mon fainted (no enemy box); last page of the auto-wrapped expansion string."))
    S.append(("state_08.png", "Low HP", render("action", 0, player=P.copy(hp=7, status="PSN"), enemy=E.copy(hp=11)),
              "Player at 7/52: red bar + poison icon; foe at about half (yellow)."))
    S.append(("state_09.png", "Trainer battle intro — party lineups",
              render("msg", msg="You are challenged by Youngster Calvin!", intro=True,
                     lineups={"opp": (LINEUP_OPP, {}), "plr": (LINEUP_PLR, {})}),
              "Both lineup bars at the vanilla spots (foe top-left, player above the tray), healthbox-B frame with brass "
              "trim and six sockets. Foe: 4 ready, 1 fainted (greyed), 1 empty socket. Player: 5 balls, one poisoned "
              "(purple dot), 1 empty. Expansion string."))
    S.append(("state_10.png", "Foe about to send out — lineup",
              render("msg", msg="Youngster Calvin is about to send out\nPoochyena.", show_enemy=False,
                     lineups={"opp": (LINEUP_OPP_MID, {})}),
              "Mid-battle: the foe's mon fainted, so its healthbox is gone and only the foe's lineup slides in (vanilla "
              "skipPlayer case). First page of the switch-prompt string; state 7 is the page after it."))
    return S


LINEUP_OPP = ["ok", "ok", "ok", "fnt", "ok", "empty"]        # k = 0 nearest the screen centre
LINEUP_PLR = ["ok", "psn", "ok", "ok", "ok", "empty"]
LINEUP_OPP_MID = ["fnt", "ok", "ok", "fnt", "ok", "empty"]


def budget_lines():
    lines = []
    for mode, label in (("msg", "message"), ("action", "action menu"), ("moves", "move select"), ("yesno", "YES/NO")):
        bg = p_sheet(W, H, UI_PAL)
        cv = Canvas(bg)
        draw_tray(cv)
        if mode == "msg":
            msg_panel(cv, 2, 237)
        elif mode == "yesno":
            msg_panel(cv, 2, 189)
            Wn.std_frame(cv, *YESNO_T)
        elif mode == "action":
            msg_panel(cv, 2, 126)
            draw_action(cv, -1)
        else:
            draw_back_tab(cv)
            draw_moves(cv, [("", "normal", 1, 1)] * 4, -1)
        tiles, _ = to_tiles(bg.crop((0, 96, W, H)))
        lines.append("BG0 %s layout (tray + panels + unselected buttons, no text): %d unique 4bpp tiles incl. blank" % (label, len(tiles)))
    tray = p_sheet(W, H, UI_PAL)
    draw_tray(Canvas(tray))
    tiles, _ = to_tiles(tray.crop((0, 112, W, H)))
    lines += [
        "Grid tray alone: %d unique tiles (2x2-tile repeat + the top edge). Static, recommended: the grid lives on BG0 with the panels, "
        "so it can't scroll by BG offset; it could fake the scroll by re-uploading/cycling 4 grid tile frames (1px / 4 frames) "
        "but that costs a VBlank copy for a barely visible effect under the windows." % len(tiles),
        "BG layers: BG0 = all battle UI; BG1 free (vanilla level-up box); BG2/BG3 untouched (Mode 7 floor / environment).",
        "BG palettes: 0 (tray/panels, kit orchid + 2 grid colours) + 5 (menu windows + PP colours). Rows 10-15 untouched; vanilla's pal 1 is freed.",
        "Healthbox OBJ palette (direction B; shared layout with A/C): 1 ink, 2/7/9 frame dark/mid/light, 3-6 kit panel roles, 8/15 orchid accent, 10 male, 11-13 brass ramp, 14 female + ball red — full 16.",
        "OBJ palettes: battlers 0-3 (vanilla) + healthbox 1 + healthbar 1 + status icons 1 (status_icons.STATUS_PAL, shared with the party menu) "
        "+ action icon fields 1 (action menu only) + type icons 3 (move select only, gMoveTypes_Pal; this moveset needs 2). Peak 10 of 16.",
        "OBJ tiles: direction B = 128x31 (opp) / 128x32 (player), 2x 64x32 each = 64 tiles per box (vanilla player = 128), status icon 16x16 = 4 per battler, "
        "FIGHT field 32x32 = 16 + 3 side fields 16x16 = 12 (28 total, action menu only), type icons 4x 32x16 = 32 (move select only).",
        "Selection: re-blit the selected button's tiles in its gold variant (custom cursor routine, DESIGN.md); icon-field OBJs are untouched.",
        "Party lineup (trainer battles, per side, same counts as vanilla's bar + 6 balls): bar 3x 32x16 = 24 tiles on the healthbox palette (no extra palette), 6 balls 16x16 = 24 tiles (vanilla 8x8; ours are 9x9 + status dot). Ball palette LINEUP_PAL: poke_ball.pal ramp + 5 status-dot colours = 1 OBJ palette shared by both sides. Shown only when healthboxes are hidden, so the peak stays 10 of 16 (battlers 4, healthbox/bar 1, healthbar 1, status icons 1, lineup balls 1, trainer pics use battler slots).",
    ]
    return lines


def notes(states_list, gifs):
    return {
        "title": "Battle UI — Orchid (Gen 5 layout, Gen 3 pixels) — round 2",
        "main": {"file": "main.png", "zones": [
            ["Opponent healthbox", "Direction B (chosen), OBJ 2x 64x32 (x 4..131, y 14..44): dark frame with a brass top trim; a stepped tab carries Lv and the caught ball in brass; the pointed left end is the status socket (plain recess when healthy); the name sits on an inset pill, coloured by gender (blue / rose / ink); HP tag + 48px bar under it."],
            ["Player healthbox", "Same shape (x 110..237, y 79..110); the tab carries HP numbers + Lv, and the EXP strip is set into the bottom edge."],
            ["Tray", "BG0, y 112..159: static BW near-black grid (party/bag colours) with an ink top edge; every panel sits on it."],
            ["Prompt box", "White message box with a quiet column of brass rivets at each end (no purple end-caps), vanilla prompt text origin."],
            ["FIGHT", "Big round button: red field with a white fist silhouette (OBJ 32x32) above the FIGHT label; face turns gold when selected."],
            ["BAG / POKéMON / RUN", "Pills whose left end is a coloured field (yellow bag, green Poké Ball, blue running shoe; OBJ 16x16). D-pad: left/right FIGHT <-> column, up/down in the column."],
            ["Scene", "Vanilla tall-grass environment + battlers at sBattlerCoords; on the engine branch this is the Mode 7 floor."]]},
        "states": [{"file": f, "title": t, "desc": d} for f, t, _, d in states_list],
        "gifs": gifs,
        "extras": [
            {"file": "parts.png", "title": "Parts + palettes (4x)",
             "desc": "Healthboxes, action tray (normal + POKéMON selected), the four icon fields, move tray and every palette the battle UI adds."},
            {"file": "status_icons.png", "title": "Status icons (status_icons.py, 4x)",
             "desc": "Shared pictogram tags for battle + party: psn, tox (skull), par, slp, brn, frz, frb, fnt, pkrs. 16x16 tag; the white pictogram is centred exactly on the 12x12 coloured face (margins printed under each icon, all >= 2px); one 16-colour OBJ palette for all."},
            {"file": "healthbox_variants.png", "title": "Healthbox directions A / B / C",
             "desc": "Three layered healthbox designs, each as a 2x full action-menu frame plus 4x close-ups (default data + low HP / status). A = brass-trimmed chamfered frame, B = stepped tab + inset name pill (chosen), C = meander band + party disc. Frozen as shown in round 3."}],
        "decisions": [
            "Healthbox direction B (stepped top tab + inset name pill) chosen by the user in round 3; healthbox_variants.png keeps the A / B / C comparison as it was shown.",
            "Gender = name colour, no ♂/♀ glyph: male names NAME_MALE fg (40,80,184) / shadow (168,192,232), female NAME_FEMALE fg (184,48,72) / shadow (232,176,184), genderless INK / PANEL_SHADE (battle_ext constants, shared with the party screen).",
            "Message box: purple end-caps replaced by a quiet column of three 2x2 brass rivets at each end.",
            "Empty status socket: plain recess with four faint corner studs (no orchid gem); a status icon covers it completely.",
            "Tray grid stays static.",
        ],
        "budget": budget_lines(),
        "kit_additions": [
            "status_icons.py (new, shared): status_icon(kind) / status_index(kind) / margins(kind) / STATUS_PAL / status_sheet().",
            "battle_ext healthbox kit: HB_PAL (frame dark/mid/light + brass ramp on kit role slots), chamfer_mask, rivet, CAUGHT, ORCHID emblem, MEANDER band, hb_A / hb_B / hb_C.",
            "battle_ext.SILHOUETTES + silhouette(): white-with-shadow pictograms for the action buttons (fist, bag, Poké Ball, shoe).",
            "battle_ext.big_round_box / round_mask / mask_box: Gen 3 shading for any corner radius (FIGHT button).",
            "Tray grid on BG0: GRID_PAL base/major in BG pal 0's spare slots, minor line = INK.",
            "Icon-field OBJ palette: four Gen 3 ramps (red / yellow / green / blue) + ink + white — reusable for any BW colour-coded button.",
            "draw_move_pill (two-line pill + PP notch) and draw_back_tab as reusable pieces.",
        ],
        "questions": [],
    }


GIFS = [
    {"file": "action_menu.gif", "title": "Action menu cursor",
     "desc": "Gold face steps FIGHT -> BAG -> POKéMON -> RUN -> FIGHT (instant moves, 24 frames apart; icon fields stay coloured), then A opens move select, the cursor walks the moves and B returns."},
    {"file": "hp_drain.gif", "title": "Hit + HP drain",
     "desc": "'Grovyle used Absorb!' prints at MID speed (4 frames/char), Zigzagoon blinks, its bar drains 1 HP/frame (max HP < 48, Gen 3 rule) and turns yellow / red at 24 / 9 px; 'A critical hit!', then the drain refills Grovyle's bar 1 px/frame."},
    {"file": "exp_levelup.gif", "title": "EXP + level up",
     "desc": "EXP strip fills 1px/frame, the player box flashes white (8 frames), Lv18 -> Lv19 and max HP 52 -> 55, EXP restarts from 0."},
    {"file": "lineup.gif", "title": "Trainer-battle party lineups",
     "desc": "Vanilla timing: both bars slide in at 5 px/frame (20 frames); balls zip in one by one from the screen edge, nearest-the-centre first (delays 10 / 17 + 7 frames per ball, accelerating); the challenge message prints; then balls and bars drift toward the centre (2 px/frame) while alpha-fading out over 32 frames."},
]


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    S = states()
    for f, t, im, d in S:
        K.upscale(im, 3).save(os.path.join(OUT, f))
    K.upscale(S[0][2], 3).save(os.path.join(OUT, "main.png"))
    parts_sheet().save(os.path.join(OUT, "parts.png"))
    SI.status_sheet().save(os.path.join(OUT, "status_icons.png"))
    # healthbox_variants.png is the frozen round-3 comparison (A/B/C); regenerate only on request:
    # variants_sheet().save(os.path.join(OUT, "healthbox_variants.png"))
    old = os.path.join(OUT, "state_05b.png")
    if os.path.exists(old):
        os.remove(old)
    json.dump(notes(S, GIFS), open(os.path.join(OUT, "notes.json"), "w"), indent=1, ensure_ascii=False)
    print("ok")
