"""
Orchid battle UI — pixel-accurate mockups ("Gen 5 layout, Gen 3 pixels").

Everything sits where vanilla puts it, so the Mode 7 floor (mode 1, BG2 affine)
on the engine branch keeps working:
  * BG0  bottom tray y 112..159 (vanilla textbox area) — message box, action menu,
         move select, YES/NO. BG palettes 0 (tray, kit roles) and 5 (menu windows:
         kit roles + Gen 3 PP warning colours). Rows 10..15 are never touched.
  * OBJ  healthboxes at the vanilla singles spots, HP/EXP bars, the four colour beads
         of the action menu, Gen 3 type icons in move select.
  * scene: vanilla battle environment + battlers (BG3 + sprites on vanilla; the
         Mode 7 floor on the engine branch).

usage: mock_battle.py OUT_DIR      (writes main.png, state_XX.png, parts.png, notes.json)
"""
import json
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as K
import windows as Wn
from gamefont import draw_text, text_width
import battle_ext as BX

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
UI_PAL = palette(THEME)                         # BG pal 0: tray + message panels (kit roles)

# PP warning colours = graphics/battle_interface/text_pp.pal. Gen 3 swaps one fg/shadow
# pair per selected move; we show all four PP counters at once, so the three warning
# foregrounds get their own slots in the menu palette (BG pal 5).
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


# Healthbox OBJ palette (one, shared by all boxes). 12..15 = per-battler status colour,
# exactly like vanilla UpdateStatusIconInHealthbox (index 12 + battler).
HB_MALE, HB_FEMALE = ACCENT_PALE, SELECT_DARK
HB_STATUS0 = 12


def healthbox_pal(status_cols=(None,) * 4, theme=THEME, flash=0.0):
    p = palette(theme)
    p[HB_MALE] = snap(K.MALE_BLUE)
    p[HB_FEMALE] = snap(K.FEMALE_RED)
    for i, c in enumerate(status_cols):
        p[HB_STATUS0 + i] = snap(c) if c else p[PANEL]
    if flash:
        p = [snap(tuple(int(v + (248 - v) * flash) for v in c)) for c in p]
    return p


# sStatusIconColors (battle_interface.c), RGB5 -> RGB8
STATUS_COL = {"PSN": (192, 96, 192), "PAR": (184, 184, 24), "SLP": (160, 160, 136),
              "FRZ": (136, 176, 224), "BRN": (224, 112, 80)}
STATUS_ROW = {"PSN": 0, "PAR": 1, "SLP": 2, "FRZ": 3, "BRN": 4}

# Healthbar OBJ palette (HP/EXP fills + HP tag) — separate, like vanilla TAG_HEALTHBAR_PAL.
HB_I = {"ink": 1, "trough": 2, "trough_hi": 3, "g1": 4, "g2": 5, "y1": 6, "y2": 7,
        "r1": 8, "r2": 9, "e1": 10, "e2": 11, "tag": 12, "tag_txt": 13, "white": 14, "tag_hi": 15}
HBAR_PAL = [snap(c) for c in [
    (0, 0, 0), (40, 40, 64), (80, 72, 96), (112, 104, 128),
    K.HP_GREEN[0], K.HP_GREEN[1], K.HP_YELLOW[0], K.HP_YELLOW[1],
    K.HP_RED[0], K.HP_RED[1], K.EXP_BLUE[0], K.EXP_BLUE[1],
    (96, 48, 128), (248, 176, 120), (248, 248, 248), (152, 88, 184)]]

# Action-menu bead OBJ palette: BW colour coding as Gen 3 3-step ramps (light, face, dark).
BEAD_RAMPS = {
    "red": ((248, 160, 136), (232, 80, 64), (168, 40, 48)),
    "yellow": ((248, 232, 136), (240, 184, 40), (184, 120, 16)),
    "green": ((168, 232, 128), (88, 184, 72), (40, 120, 56)),
    "blue": ((152, 200, 248), (72, 136, 224), (40, 80, 160)),
}
BEAD_ORDER = ["red", "yellow", "green", "blue"]
BEAD_PAL = [snap(c) for c in [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
            + [c for k in BEAD_ORDER for c in BEAD_RAMPS[k]] + [(0, 0, 0)]]


def bead_idx(colour, step):   # step 0 light, 1 face, 2 dark
    return 3 + BEAD_ORDER.index(colour) * 3 + step


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
CAUGHT = ["..III..",
          ".IRRRI.",
          "IRRRRRI",
          "IIIWIII",
          "IWWWWWI",
          ".IWWWI.",
          "..III.."]


# ================================================================== BG0 tray
TRAY = BX.TRAY_Y                 # 112: vanilla textbox area, tile rows 14..19
TOP, BOT = TRAY + 2, H - 3       # usable rows inside the tray (114..157)
MSG_X, MSG_Y, MSG_W = 16, 120, 26 * 8      # B_WIN_MSG text rect (tiles 2,15 26x4)


def draw_tray(cv):
    """Static tray base: orchid band (like the std frame's accent band), ink top edge."""
    cv.rect(0, TRAY, W - 1, H - 1, ACCENT_DARK)
    cv.hline(0, W - 1, TRAY, INK)
    cv.hline(0, W - 1, TRAY + 1, ACCENT)


def msg_panel(cv, x0, x1):
    """Message panel = the approved field dialogue box (white, purple end-caps), in the tray."""
    h = BOT - TOP + 1
    rounded_box(cv, x0, TOP, x1 - x0 + 1, h, 3, WHITE, INK, WHITE, PANEL_SHADE)
    rounded_box(cv, x0 + 3, TOP + 4, 6, h - 8, 2, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    rounded_box(cv, x1 - 6, TOP + 4, 4, h - 8, 1, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    cv.hline(x0 + 11, x1 - 8, BOT - 3, PANEL_SHADE)


def draw_back_tab(cv, label="BACK"):
    """Small tab rising from the tray's top-left corner: B-button hint for sub-menus."""
    tw = text_width(label, "small")
    x1, y0 = 18 + tw, TRAY - 11
    ins = lambda r: {0: 3, 1: 1, 2: 1}.get(r, 0)
    for y in range(y0, TRAY + 2):
        cv.hline(0, x1 - ins(y - y0), y, ACCENT_DARK)
        cv.set(x1 - ins(y - y0), y, INK)
    cv.hline(0, x1 - ins(0), y0, INK)
    cv.hline(0, x1 - ins(1) - 1, y0 + 1, ACCENT)
    cv.set(x1 - 2, y0 + 1, INK)
    cv.hline(x1 - 1, x1 + 1, TRAY, INK)
    cv.set(x1, TRAY + 1, ACCENT)
    cv.set(x1 + 1, TRAY + 1, ACCENT)
    disc(cv, 8, y0 + 6, 5, WHITE, INK, None, PANEL_SHADE)
    stamp(cv, 6, y0 + 4, B_GLYPH, {"X": INK})
    draw_text(cv, 15, y0 - 1, label, WHITE, INK, font="small")


# ---------------------------------------------------------------- action menu (BG0 window, pal 5)
FIGHT_BTN = (130, TOP, 44, 44)                 # x, y, w, h — big round BW-style button
FIGHT_R = 12
SIDE_X, SIDE_W = 177, 61
SIDE_Y = [TOP, TOP + 15, TOP + 30]             # 14px pills, 1px gap
BTN_COL = ["red", "yellow", "green", "blue"]


def side_rect(i):
    return SIDE_X, SIDE_Y[i], SIDE_W, 14


def draw_action(cv, cursor):
    x, y, w, h = FIGHT_BTN
    sel = cursor == 0
    face, lt, sh = (SELECT, SELECT_LIGHT, SELECT_DARK) if sel else (PANEL, WHITE, PANEL_SHADE)
    BX.big_round_box(cv, x, y, w, h, FIGHT_R, face, INK, lt, sh)
    draw_text(cv, x + (w - text_width("FIGHT")) // 2 + 1, y + 21, "FIGHT", INK, PANEL_SHADE)
    for i in range(3):
        x, y, w, h = side_rect(i)
        if cursor == i + 1:
            Wn.selection_bar(cv, x, y, w, h)
        else:
            rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
        draw_text(cv, x + 16, y - 1, ACTIONS[i + 1], INK, PANEL_SHADE, font="narrow")


def bead_positions():
    x, y, w, h = FIGHT_BTN
    out = [(x + w // 2, y + 13)]
    for i in range(3):
        sx, sy, sw, sh = side_rect(i)
        out.append((sx + 8, sy + 7))
    return out


def draw_bead(cv, cx, cy, colour, r=5.0):
    disc(cv, cx, cy, r, bead_idx(colour, 1), 1, bead_idx(colour, 0), bead_idx(colour, 2))
    cv.set(int(cx - r / 2), int(cy - r / 2), 2)


def beads_layer(out):
    im = p_sheet(W, H, BEAD_PAL)
    cv = Canvas(im)
    for i, ((cx, cy), col) in enumerate(zip(bead_positions(), BTN_COL)):
        draw_bead(cv, cx, cy, col, 6.5 if i == 0 else 5.0)
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
    # PP counter = ink notch sunk into the pill's bottom edge: Gen 3 warning colours
    # (text_pp.pal) stay legible whether the pill is grey or gold.
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


# ---------------------------------------------------------------- YES/NO (std frame, pal 5)
# Lives in the tray's right end (BW puts YES/NO on the bottom screen) instead of vanilla's
# (26,9) spot, so it never chops the player healthbox. The frame is baked into a tray
# layout (its 2px margin shows tray, not the scene); the message window narrows to 21 tiles.
YESNO_T = (25, 15, 4, 4)    # text rect in tiles; frame = x 192..239, y 112..159
YESNO_MSG_W = 21 * 8


def draw_yesno_frame(cv):
    Wn.std_frame(cv, *YESNO_T)


def draw_yesno(cv, cursor):
    tx, ty, tw, th = YESNO_T
    for i, t in enumerate(("YES", "NO")):
        y = ty * 8 + i * 16
        if i == cursor:
            Wn.selection_bar(cv, tx * 8 + 2, y + 1, tw * 8 - 4, 14)
        draw_text(cv, tx * 8 + 8, y, t, INK, PANEL_SHADE)


# ================================================================== healthboxes (OBJ)
# Both boxes are flush with the screen edge (BW), inside the vanilla healthbox zones.
OPP_BOX = (-8, 18, 114, 23)      # x, y, w, h : visible 0..105 x 18..40   (2x 64x32 OBJ)
PLR_BOX = (130, 79, 118, 32)     # visible 130..239 x 79..110             (2x 64x32 OBJ)
CAP_OPP_W, CAP_PLR_W = 12, 8


def draw_healthbox(cv, mon, side, battler, status_style="orchid"):
    """Frame + text on the healthbox palette. Returns the HP bar origin."""
    if side == "opp":
        x, y, w, h = OPP_BOX
        rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
        rounded_box(cv, x + w - CAP_OPP_W - 2, y + 2, CAP_OPP_W, h - 4, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        tx = 5
        lv_right = x + w - CAP_OPP_W - 5
    else:
        x, y, w, h = PLR_BOX
        rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)
        rounded_box(cv, x + 2, y + 2, CAP_PLR_W, h - 4, 2, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        tx = x + CAP_PLR_W + 6
        lv_right = 235
    draw_text(cv, tx, y - 1, mon.name, INK, PANEL_SHADE, font="small")
    gx = tx + text_width(mon.name, "small") + 2
    if mon.gender == "M":
        draw_text(cv, gx, y - 1, "♂", HB_MALE, PANEL_SHADE, font="small")
    elif mon.gender == "F":
        draw_text(cv, gx, y - 1, "♀", HB_FEMALE, PANEL_SHADE, font="small")
    lv = "Lv%d" % mon.lv
    draw_text(cv, lv_right - text_width(lv, "small"), y - 1, lv, INK, PANEL_SHADE, font="small")
    bar_x, bar_y = tx + 12, y + 12
    if mon.status:
        draw_status(cv, bar_x + 53, y + 12, mon.status, battler, status_style)
    if side == "opp" and mon.caught:
        stamp(cv, x + w - CAP_OPP_W - 2 + 2, y + 7, CAUGHT, {"I": INK, "R": HB_FEMALE, "W": WHITE})
    if side == "plr":
        hp = "%d/%3d" % (mon.hp, mon.maxhp)
        draw_text(cv, bar_x + 50 - text_width(hp, "small"), y + 15, hp, INK, PANEL_SHADE, font="small")
    return bar_x, bar_y


def draw_status(cv, x, y, status, battler, style="gen3"):
    """Gen 3 status icon (graphics/battle_interface/status.png), colour in slot 12+battler.
    style 'gen3' = vanilla knock-out letters; 'orchid' = ink-outlined tag, white letters."""
    src = Image.open(K.G("battle_interface", "status.png")).load()
    row = STATUS_ROW[status]
    col = HB_STATUS0 + battler
    if style == "gen3":
        for yy in range(8):
            for xx in range(20):
                v = src[xx, row * 8 + yy]
                if v >= 12:
                    cv.set(x + xx, y + yy, col)
                elif v == 2 and not (xx in (0, 19) and yy in (0, 7)):
                    cv.set(x + xx, y + yy, PANEL)
                elif v == 3:
                    cv.set(x + xx, y + yy, PANEL_SHADE)
        return
    # Orchid tag: 21x10, ink outline, status-colour face, white letters lifted from status.png
    rounded_box(cv, x, y - 1, 21, 10, 1, col, INK, col, col, bevel=False)
    for yy in range(1, 7):
        for xx in range(2, 18):
            if src[xx, row * 8 + yy] == 2:
                cv.set(x + xx + 1, y + yy + 1, WHITE)


def hp_level(hp, maxhp, pixels=48):
    """Gen 3 GetHPBarLevel: thresholds are in bar pixels (>24 green, >9 yellow, else red)."""
    px = 0 if hp <= 0 else max(1, hp * pixels // maxhp)
    return ("g" if px > 24 else "y" if px > 9 else "r"), px


def draw_bars(cv, mon, side, bar_x, bar_y, hp=None, exp=None):
    """HP tag + 48px HP bar (+ EXP strip on the player box) on the healthbar palette."""
    hp = mon.hp if hp is None else hp
    exp = mon.exp if exp is None else exp
    tx, ty = bar_x - 11, bar_y - 1
    rounded_box(cv, tx, ty, 12, 7, 1, HB_I["tag"], HB_I["ink"], HB_I["tag_hi"], HB_I["tag"])
    stamp(cv, tx + 3, ty + 1, HP_GLYPH, {"X": HB_I["tag_txt"]})
    lvl, n = hp_level(hp, mon.maxhp)
    cv.rect(bar_x, bar_y, bar_x + 49, bar_y + 4, HB_I["ink"])
    cv.rect(bar_x + 1, bar_y + 1, bar_x + 48, bar_y + 3, HB_I["trough"])
    cv.hline(bar_x + 1, bar_x + 48, bar_y + 1, HB_I["trough_hi"])
    if n:
        cv.rect(bar_x + 1, bar_y + 1, bar_x + n, bar_y + 3, HB_I[lvl + "2"])
        cv.hline(bar_x + 1, bar_x + n, bar_y + 1, HB_I[lvl + "1"])
    if side == "plr":
        # thin EXP strip sunk into the box's bottom edge (BW), fills left -> right
        x, y, w, h = PLR_BOX
        ex0, ex1, ey = x + CAP_PLR_W + 4, 236, y + h - 4
        cv.rect(ex0, ey, ex1, ey + 3, HB_I["ink"])
        cv.hline(ex0 + 1, ex1 - 1, ey + 1, HB_I["trough"])
        cv.hline(ex0 + 1, ex1 - 1, ey + 2, HB_I["trough"])
        n = int(round((ex1 - ex0 - 1) * max(0.0, min(1.0, exp))))
        if n:
            cv.hline(ex0 + 1, ex0 + n, ey + 1, HB_I["e1"])
            cv.hline(ex0 + 1, ex0 + n, ey + 2, HB_I["e2"])


def healthboxes(out, player, enemy, show=("opp", "plr"), hp=None, exp=None, flash=None,
                status_style="orchid", shake=None):
    hp, flash, shake = hp or {}, flash or {}, shake or {}
    stat = [None] * 4
    if player is not None and player.status:
        stat[0] = STATUS_COL[player.status]
    if enemy is not None and enemy.status:
        stat[1] = STATUS_COL[enemy.status]
    for side, mon, b in (("opp", enemy, 1), ("plr", player, 0)):
        if side not in show or mon is None:
            continue
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        box = p_sheet(W, H, healthbox_pal(stat, flash=flash.get(side, 0)))
        bx, by = draw_healthbox(Canvas(box), mon, side, b, status_style)
        comp(frame, box)
        bars = p_sheet(W, H, HBAR_PAL)
        draw_bars(Canvas(bars), mon, side, bx, by, hp.get(side), exp if side == "plr" else None)
        comp(frame, bars)
        out.alpha_composite(frame, (0, shake.get(side, 0)))


# ================================================================== render
def render(mode="action", cursor=0, msg=None, player=None, enemy=None, moves=None, yesno=0,
           show_enemy=True, show_boxes=("opp", "plr"), hp=None, exp=None, env="tall_grass",
           enemy_visible=True, ball=False, flash=None, status_style="orchid", chars=None):
    """mode: msg | action | moves | yesno.  chars = number of message characters printed."""
    player = player or default_player()
    enemy = enemy if enemy is not None else default_enemy()
    moves = moves or MOVES
    out = BX.scene(player.species, enemy.species, env, show_enemy=show_enemy and enemy_visible)
    if ball:   # caught: closed Poké Ball resting on the enemy spot
        spr = K.sprite_rgba(K.G("balls", "poke.png"), 0, 16)
        K.place(out, spr, BX.ENEMY_C[0], BX.ENEMY_C[1] + 30)
    healthboxes(out, player, enemy if show_enemy else None, show_boxes, hp, exp, flash, status_style)

    bg = p_sheet(W, H, UI_PAL)          # BG0 static tilemap art, pal 0
    cv = Canvas(bg)
    draw_tray(cv)
    if mode in ("msg", "yesno"):
        msg_panel(cv, 2, 237 if mode == "msg" else 189)
        if mode == "yesno":
            draw_yesno_frame(cv)
        lines = wrap(msg or "", MSG_W if mode == "msg" else YESNO_MSG_W)[-2:]
        text = "\n".join(lines)
        if chars is not None:
            text = text[:chars]
        draw_text(cv, MSG_X, MSG_Y, text, INK, PANEL_SHADE)
    elif mode == "action":
        msg_panel(cv, 2, 126)
        prompt = msg or "What will\n%s do?" % player.name
        draw_text(cv, MSG_X, MSG_Y, prompt, INK, PANEL_SHADE)
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
        beads_layer(out)
    elif mode == "moves":
        type_icons(out, moves)
    return out


# ================================================================== sheets
def healthbox_sheet(status_style="orchid"):
    """240x208: opponent variants (left, flush like in game) + player variants (right)."""
    SH = 208
    out = Image.new("RGBA", (W, SH), BX.environment().getpixel((4, 60)))
    zig = default_enemy()
    opp = [
        zig.copy(),                                                    # full, caught ball
        zig.copy(hp=11, status="PSN", caught=False),                   # yellow + PSN
        zig.copy(hp=3, status="PAR"),                                  # red + PAR
        Mon("beldum", "Beldum", 12, 30, 30, None, status="SLP"),       # genderless
        Mon("wurmple", "Wurmple", 3, 14, 15, "M", status="BRN"),
        Mon("poochyena", "Poochyena", 9, 9, 28, "M", status="FRZ"),
        Mon("zigzagoon", "Zigzagoon", 7, 0, 24, "F"),                  # fainted / empty
    ]
    gro = default_player()
    plr = [
        gro.copy(hp=52, exp=0.94),                                     # full, EXP nearly full
        gro.copy(hp=24, status="BRN", gender="F", exp=0.30),
        gro.copy(hp=7, status="PSN", exp=0.62),                        # low (red)
        Mon("treecko", "Treecko", 9, 31, 31, None, status="SLP", exp=0.05),
        Mon("treecko", "Treecko", 9, 12, 31, "M", status="FRZ", exp=0.5),
    ]
    for i, m in enumerate(opp):
        f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        healthboxes(f, None, m, ("opp",), status_style=status_style)
        out.alpha_composite(f.crop((0, OPP_BOX[1], 114, OPP_BOX[1] + OPP_BOX[3])), (0, 4 + i * 29))
    for i, m in enumerate(plr):
        f = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        healthboxes(f, m, None, ("plr",), status_style=status_style)
        out.alpha_composite(f.crop((120, PLR_BOX[1], 240, PLR_BOX[1] + PLR_BOX[3])), (120, 4 + i * 40))
    return out


def parts_sheet():
    """4x sheet of the new pieces with their palettes."""
    S = 4
    sheet = Image.new("RGBA", (W * S + 2 * 16, 1400), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    y = 12

    def put(img, x, y, caption):
        d.text((x, y), caption, fill=(230, 230, 240))
        sheet.alpha_composite(K.upscale(img, S), (x, y + 14))
        return y + 14 + img.size[1] * S + 14

    bgc = (88, 96, 112, 255)
    f = Image.new("RGBA", (W, H), bgc)
    healthboxes(f, default_player(), default_enemy())
    hb = Image.new("RGBA", (W, 36), bgc)
    hb.alpha_composite(f.crop((0, OPP_BOX[1] - 2, 112, OPP_BOX[1] + 30)), (0, 2))
    hb.alpha_composite(f.crop((120, PLR_BOX[1] - 2, 240, PLR_BOX[1] + 34)), (120, 0))
    y = put(hb, 16, y, "Healthboxes (OBJ, 2x 64x32 each): opponent flush-left, caught-ball cap; player flush-right, HP numbers + EXP strip in the bottom edge")
    a0 = render("action", 0).crop((0, TRAY - 2, W, H))
    y = put(a0, 16, y, "Action menu (BG0 tray pal 0 + menu window pal 5; beads = 4 OBJ 16x16 on 1 palette). FIGHT = big round button")
    a1 = render("moves", 0).crop((0, TRAY - 12, W, H))
    y = put(a1, 16, y, "Move select: 2x2 two-line pills, Gen 3 type icon (OBJ 32x16), PP counter notch with Gen 3 warning colours; BACK tab")
    d.text((16, y), "Palettes", fill=(230, 230, 240))
    y += 16
    for label, pal in (("BG 0  tray / message (kit orchid roles)", UI_PAL),
                       ("BG 5  menu windows (kit roles; 10 = PP yellow, 14 = orange, 15 = red)", MENU_PAL),
                       ("OBJ  healthbox (10 male, 11 female / ball red, 12-15 status per battler)",
                        healthbox_pal((STATUS_COL["PSN"], STATUS_COL["PAR"]))),
                       ("OBJ  healthbar (HP green / yellow / red, EXP blue, HP tag)", HBAR_PAL),
                       ("OBJ  action beads (red / yellow / green / blue ramps)", BEAD_PAL)):
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
              "Prompt in the field-style message box on the left; FIGHT is the big round button, "
              "BAG / POKéMON / RUN are pills. Gold face = selection; colour beads keep BW's red/yellow/green/blue coding."))
    S.append(("state_02.png", "Action menu — RUN", render("action", 3),
              "RUN selected: only the pill face turns gold, the blue bead stays, so colour coding never fights the cursor."))
    S.append(("state_03.png", "Move select", render("moves", 0),
              "2x2 two-line pills: Gen 3 type icon, move name, PP counter notch. Quick Attack 6/30 shows orange (<= 1/4), "
              "Pursuit 9/20 yellow (<= 1/2) — text_pp.pal colours. BACK tab = B."))
    S.append(("state_04.png", "Battle message", render("msg", msg="The wild Zigzagoon had its energy drained!"),
              "Full-width message box (B_WIN_MSG rect, 16px line pitch); two lines clear the bottom hairline. "
              "Both healthboxes stay visible."))
    S.append(("state_05.png", "Healthbox variants", healthbox_sheet("orchid"),
              "Left: opponent — full + caught ball, yellow + PSN (not caught), red + PAR, genderless + SLP, BRN, FRZ, fainted. "
              "Right: player — EXP nearly full, female + BRN, red + PSN, genderless + SLP, FRZ. Orchid status tags: ink outline, "
              "white letters lifted from status.png, vanilla status colours."))
    S.append(("state_05b.png", "Healthbox variants — real Gen 3 status icons", healthbox_sheet("gen3"),
              "Same sheet with the untouched Gen 3 status.png icons (knock-out letters in the box face colour)."))
    S.append(("state_06.png", "YES/NO — nickname",
              render("yesno", msg="Would you like to give Zigzagoon a nickname?", show_enemy=False, ball=True),
              "Approved std frame + gold pill on YES, docked in the tray's right end (BW puts YES/NO on the bottom screen) "
              "instead of vanilla's spot over the player box; the message window narrows to 21 tiles. Expansion's real string; "
              "the caught ball rests on the enemy spot."))
    pooch = Mon("poochyena", "Poochyena", 9, 28, 28, "M")
    S.append(("state_07.png", "Switch prompt",
              render("yesno", msg="Youngster Calvin is about to send out Poochyena. Will you switch your Pokémon?",
                     enemy=pooch, show_enemy=False),
              "Trainer battle, the foe's last mon fainted (no enemy box). Expansion string, auto-wrapped; this is the last "
              "page. YES/NO in the same std frame."))
    S.append(("state_08.png", "Low HP", render("action", 0, player=P.copy(hp=7, status="PSN"), enemy=E.copy(hp=11)),
              "Player at 7/52: red bar + PSN tag; foe at about half (yellow)."))
    return S


def budget_lines():
    lines = []
    for mode, label in (("msg", "message"), ("action", "action menu"), ("moves", "move select")):
        bg = p_sheet(W, H, UI_PAL)
        cv = Canvas(bg)
        draw_tray(cv)
        if mode == "msg":
            msg_panel(cv, 2, 237)
        elif mode == "action":
            msg_panel(cv, 2, 126)
            draw_action(cv, -1)
        else:
            draw_back_tab(cv)
            draw_moves(cv, [("", "normal", 1, 1)] * 4, -1)
        tiles, _ = to_tiles(bg.crop((0, 96, W, H)))
        lines.append("BG0 %s layout, tray + panels + unselected buttons (no text): %d unique 4bpp tiles incl. blank" % (label, len(tiles)))
    lines += [
        "BG layers: BG0 = all battle UI (tray + windows), BG1 free (vanilla level-up box), BG2/BG3 untouched (Mode 7 floor / environment).",
        "BG palettes: 0 (tray, kit orchid) + 5 (menu windows + PP colours, vanilla's window slot). Rows 10-15 untouched; vanilla's 2nd textbox palette (1) is freed.",
        "OBJ palettes: battlers 0-3 (vanilla) + healthbox 1 + healthbar 1 + beads 1 (action menu only) + type icons 3 (move select only; gMoveTypes_Pal as in the summary screen, this moveset uses 2). Peak 9 of 16.",
        "OBJ tiles: opponent box 2x 64x32 = 64, player box 2x 64x32 = 64 (vanilla player = 2x 64x64 = 128), beads 4x 16x16 = 16, type icons 4x 32x16 = 32.",
        "Layouts: like vanilla's 32x64 BG0 map (msg / action / moves screens switched by BG0 VOFS), plus a YES/NO variant (std frame baked into the tray's right 6x6 tiles).",
        "Selection: re-blit the selected button's tiles in the gold variant (same tiles, SELECT colours) — custom cursor routine from DESIGN.md; FIGHT has its own round gold variant (~36 tiles). Text = vanilla text windows (prompt, 4 move names, PP).",
    ]
    return lines


def notes(states_list, gifs):
    return {
        "title": "Battle UI — Orchid (Gen 5 layout, Gen 3 pixels)",
        "main": {"file": "main.png", "zones": [
            ["Opponent healthbox", "OBJ 2x 64x32 in the vanilla top-left zone, flush to the screen edge like BW: name + gender + Lv, HP tag + 48px bar, status after the bar, caught ball in the orchid end-cap."],
            ["Player healthbox", "OBJ 2x 64x32, flush right just above the tray: name / gender / Lv, HP bar, HP numbers under the bar end, thin EXP strip sunk into the bottom edge."],
            ["Tray", "BG0 static tiles, y 112..159 (vanilla textbox area): orchid band like the std frame's accent; every panel sits inside it."],
            ["Prompt box", "The approved field dialogue box (white, purple end-caps), vanilla prompt text origin, 16px line pitch."],
            ["FIGHT", "Big round BW-style button (44x44); face turns gold when selected; red bead OBJ on top."],
            ["BAG / POKéMON / RUN", "14px pills, 1px gaps, yellow / green / blue beads. D-pad: left/right = FIGHT <-> column, up/down inside the column."],
            ["Scene", "Vanilla tall-grass environment + battlers at sBattlerCoords; on the engine branch this is the Mode 7 floor. The UI never uses BG2/BG3 or BG palette rows 10-15."]]},
        "states": [{"file": f, "title": t, "desc": d} for f, t, _, d in states_list],
        "gifs": gifs,
        "extras": [{"file": "parts.png", "title": "Parts + palettes (4x)",
                    "desc": "Healthboxes, action tray, move tray and every palette the battle UI adds."}],
        "budget": budget_lines(),
        "kit_additions": [
            "battle_ext.big_round_box / round_mask / mask_box: Gen 3 shading for any corner radius (FIGHT button); could fold into kit.rounded_box for r > 4.",
            "battle_ext.environment() + scene(): composites graphics/battle_environment/<env> + battlers for mockups (stand-in for the Mode 7 floor).",
            "Menu palette (BG 5): kit roles with ACCENT_PALE / SPARE_A / SPARE_B = text_pp.pal yellow / orange / red.",
            "Healthbox OBJ palette: kit roles, ACCENT_PALE = male blue, SELECT_DARK = female / ball red, 12-15 = per-battler status colour (vanilla convention).",
            "Healthbar OBJ palette: Gen 3 HP ramps + EXP blue + HP tag (orchid face, Gen 3 peach letters).",
            "Bead OBJ palette: four Gen 3 ramps (red / yellow / green / blue) + ink + white — reusable for any BW colour-coded button.",
            "draw_move_pill (two-line pill + PP notch) and draw_back_tab (B hint tab) as reusable pieces.",
        ],
        "questions": [
            ["Gender tint on the player box?", "Battle is shared, so both boxes use the Orchid end-cap. Option: tint only the player box's end-cap + HP tag by player gender (4 colours, no layout change). Recommend keeping Orchid on both for consistency with the shared-window rule."],
            ["Status tag style", "A: Orchid tags — ink outline + white letters, same letter shapes and colours as status.png (state_05, used in every state). B: real Gen 3 status.png icons with knock-out letters (state_05b). Recommend A: matches the kit's ink-outline rule and reads better on the light box."],
            ["FIGHT button shape", "Big rounded square (r=12, current) vs full circle vs a wide pill like the others. Recommend the rounded square: reads as BW's big FIGHT button and fits FIGHT + bead."],
            ["PP colours", "Gen 3's yellow/orange PP text is unreadable on the gold pill, so PP sits in an ink notch (white / yellow / orange / red). Alternative: plain text on the pill with darker warning colours. Recommend the notch."],
            ["Message wording", "Mockups use the expansion's real strings ('Would you like to give Zigzagoon a nickname?', '…is about to send out Poochyena. Will you switch your Pokémon?'), auto-wrapped to the 26-tile window. Keep, or restore Gen 3 wording?"],
            ["YES/NO position", "Vanilla opens YES/NO at tiles (26,9), on top of the player healthbox. The mockup docks the std frame in the tray's right end instead (message narrows to 21 tiles, longer prompts paginate sooner). Recommend docked; the vanilla spot is a one-line change if you prefer it."],
            ["BACK tab", "Move select shows a small B/BACK tab rising 11px above the tray's top-left (over the platform, not the mon). Keep it, or drop it for a cleaner scene?"],
        ],
    }


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    S = states()
    for f, t, im, d in S:
        K.upscale(im, 3).save(os.path.join(OUT, f))
    K.upscale(S[0][2], 3).save(os.path.join(OUT, "main.png"))
    parts_sheet().save(os.path.join(OUT, "parts.png"))
    gifs = [
        {"file": "action_menu.gif", "title": "Action menu cursor",
         "desc": "Gold pill steps FIGHT -> BAG -> POKéMON -> RUN -> FIGHT (instant moves, 24 frames apart), then A opens move select and the cursor walks the four moves."},
        {"file": "hp_drain.gif", "title": "Hit + HP drain",
         "desc": "'Grovyle used Absorb!' prints at MID speed (4 frames/char), Zigzagoon blinks, its bar drains 1 HP/frame (max HP < 48, Gen 3 rule) and turns yellow / red at 24 / 9 px; 'A critical hit!', then the drain refills Grovyle's bar 1 px/frame."},
        {"file": "exp_levelup.gif", "title": "EXP + level up",
         "desc": "EXP strip fills 1px/frame, the player box flashes white for 8 frames at the top, Lv18 -> Lv19 and max HP 52 -> 55, EXP restarts from 0."},
    ]
    json.dump(notes(S, gifs), open(os.path.join(OUT, "notes.json"), "w"), indent=1, ensure_ascii=False)
    print("ok")
