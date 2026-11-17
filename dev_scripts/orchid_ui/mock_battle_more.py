"""
Orchid battle UI, phase 2 mockups: doubles / multi healthboxes, the Safari player box,
gimmick trigger placement and 4-digit (Dynamax) HP. Same language as healthbox direction B
(battle_ext.hb_B): dark frame + brass trim, stepped tab with brass text, pointed end with the
status socket, gender-coloured name on an inset pill, HP tag + bar, EXP strip.

usage: mock_battle_more.py OUT_DIR
writes doubles_mock.png, safari_mock.png, triggers_mock.png, dynamax_hp_mock.png
"""
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as K
import gamefont
from gamefont import draw_text, text_width, _font
import battle_ext as BX
import mock_battle as M
import status_icons as SI

gamefont._FONTS["smallnarrower"] = ("latin_small_narrower.png", "gFontSmallNarrowerLatinGlyphWidths")
W, H = 240, 160
HP_FONT = "smallnarrower"          # player HP digits (approved for singles)


def hp_text(mon, hp_shown=None, current_only=False):
    hp = mon.hp if hp_shown is None else hp_shown
    if current_only:
        return "%d" % hp
    return "%d/%3d" % (hp, mon.maxhp)


# ================================================================== compact box (doubles / multi)
# Two boxes per side at the vanilla doubles spots, 25 px apart (opponent) / 27 px (player).
# Box = 116 wide; tab 72 x 11 (brass Lv, HP numbers / caught ball), body from row 7 with the
# 16x16 status socket filling its inner height, a 10 px name pill, HP tag + 48 px bar under it,
# and (player) the EXP strip in the bottom edge. Each box fits a 2x 64x32 OBJ pair like vanilla.
CW = 116
C_TAB_W, C_TAB_H, C_BODY_Y = 72, 11, 7
C_H = {"opp": 25, "plr": 27}
# top-left of each box (vanilla doubles centres are (44,19) (32,44) / (159,76) (171,101);
# ours are shifted so a 116 px box stays on screen and the pairs don't touch)
C_POS = {"opp": [(12, 3), (0, 28)], "plr": [(112, 57), (124, 84)]}


def hb_compact(cv, mon, side, x, y, hp_shown=None, dynamax=False):
    h = C_H[side]
    body = {(a, b + C_BODY_Y) for (a, b) in BX.chamfer_mask(CW, h - C_BODY_Y, tl=6, bl=6, tr=2, br=2)}
    tab = {(a + CW - C_TAB_W, b) for (a, b) in BX.chamfer_mask(C_TAB_W, C_TAB_H, tl=C_TAB_H - 3, tr=2)}
    BX.mask_box(cv, x, y, body | tab, BX.FRAME, INK, BX.BRASS, BX.FRAME_DARK)
    inner0, inner1 = y + C_BODY_Y + 1, y + h - 2
    sy = inner0 + ((inner1 - inner0 + 1) - 16) // 2
    sx = x + 6
    # recess = exactly the 16x16 icon (no room for the full design's extra ring)
    rounded_box(cv, sx, sy, 16, 16, 3, BX.FRAME_DARK, INK, BX.FRAME_DARK, BX.FRAME_LIGHT)
    for dx, dy in ((3, 3), (12, 3), (3, 12), (12, 12)):
        cv.set(sx + dx, sy + dy, BX.FRAME)
    px0, py0 = sx + 18, y + C_BODY_Y + 1
    rounded_box(cv, px0, py0, x + CW - 5 - px0, 10, 3, PANEL, INK, WHITE, PANEL_SHADE)
    BX.name_gender(cv, px0 + 4, py0 - 2, mon)
    lv_right = x + CW - 5
    _, widths = _font("small")
    lv_w = widths[0x34] + text_width(str(mon.lv), "small")
    BX.lv_text(cv, lv_right, y - 2, mon.lv, BX.BRASS_LIGHT, BX.FRAME_DARK)
    if side == "plr":
        s = hp_text(mon, hp_shown, current_only=dynamax)
        draw_text(cv, lv_right - lv_w - 7 - text_width(s, HP_FONT), y - 2, s, BX.BRASS_LIGHT, BX.FRAME_DARK, font=HP_FONT)
    elif mon.caught:
        BX.caught_ball(cv, lv_right - lv_w - 11, y + 2)
    bar = (px0 + 16, py0 + 11)
    exp = (px0, x + CW - 6, y + h - 3, "embedded") if side == "plr" else None
    return dict(bar=bar, status=(sx, sy), exp=exp)


def draw_compact(out, mon, side, slot, hp=None, exp=None):
    x, y = C_POS[side][slot]
    box = M.p_sheet(W, H, BX.HB_PAL)
    an = hb_compact(Canvas(box), mon, side, x, y, hp)
    M.comp(out, box)
    bars = M.p_sheet(W, H, M.HBAR_PAL)
    M.draw_bars(Canvas(bars), mon, an, hp, exp)
    M.comp(out, bars)
    st = mon.status or ("fnt" if (mon.hp if hp is None else hp) <= 0 else None)
    if st:
        out.alpha_composite(SI.status_icon(st.lower()), an["status"])
    return an


DOUBLES_COORDS = {"pl": (32, 80), "ol": (200, 40), "pr": (90, 84), "or": (152, 32)}


def doubles_scene():
    out = BX.environment()
    for key, sp, front in (("or", "poochyena", True), ("ol", "zigzagoon", True),
                           ("pl", "grovyle", False), ("pr", "treecko", False)):
        cx, cy = DOUBLES_COORDS[key]
        if front:
            K.place(out, K.mon_front(sp), cx, cy + BX.SPECIES[sp]["front_y"])
        else:
            K.place(out, K.mon_back(sp), cx, cy + BX.SPECIES[sp]["back_y"])
    return out


def doubles_frame(boxes):
    out = doubles_scene()
    for side, slot, mon, hp in boxes:
        draw_compact(out, mon, side, slot, hp)
    # tray + action menu exactly as approved
    bg = M.p_sheet(W, H, M.UI_PAL)
    cv = Canvas(bg)
    M.draw_tray(cv)
    M.msg_panel(cv, 2, 126)
    draw_text(cv, M.MSG_X, M.MSG_Y, "What will\nTreecko do?", INK, PANEL_SHADE)
    M.comp(out, bg)
    win = M.p_sheet(W, H, M.MENU_PAL)
    M.draw_action(Canvas(win), 0)
    M.comp(out, win)
    M.button_fields(out)
    return out


def doubles_sheet():
    zig = M.Mon("zigzagoon", "Zigzagoon", 7, 24, 24, "F", caught=True)
    pooch = M.Mon("poochyena", "Poochyena", 9, 11, 28, "M", status="PAR")
    gro = M.Mon("grovyle", "Grovyle", 18, 48, 52, "M", exp=0.62)
    tree = M.Mon("treecko", "Treecko", 100, 999, 999, None, status="PSN", exp=0.3)
    boxes = [("opp", 0, zig, None), ("opp", 1, pooch, None), ("plr", 0, gro, None), ("plr", 1, tree, None)]
    frame = doubles_frame(boxes)
    # close-ups: each pair on the sky colour + worst-case HP / statuses
    sky = BX.environment().getpixel((4, 60))
    def pair(side, mons):
        f = Image.new("RGBA", (W, H), sky)
        for slot, m in enumerate(mons):
            draw_compact(f, m, side, slot)
        if side == "opp":
            return f.crop((0, 0, 132, 56))
        return f.crop((108, 53, 240, 113))
    cu = [pair("opp", [zig, pooch]), pair("plr", [gro, tree]),
          pair("opp", [M.Mon("beldum", "Beldum", 12, 0, 30, None), M.Mon("wurmple", "Wurmple", 3, 14, 15, "M", status="BRN")]),
          pair("plr", [gro.copy(hp=7, maxhp=999, lv=100, status="TOX", gender="F"), tree.copy(hp=100, maxhp=100, status="FRB", exp=0.95)])]
    S2, S4 = 2, 4
    sheet = Image.new("RGBA", (16 + 480 + 16 + 2 * (132 * S4 + 8), 16 + 360 + 2 * (60 * S4 + 26)), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    d.text((16, 4), "Doubles action menu (2x): compact direction-B boxes at the vanilla doubles spots", fill=(240, 220, 150))
    sheet.alpha_composite(K.upscale(frame, S2), (16, 20))
    x0 = 16 + 480 + 16
    d.text((x0, 4), "4x close-ups: opponent pair / player pair (top: frame data, bottom: FNT + BRN, 7/999 Lv100 TOX, 100/100 FRB)", fill=(230, 230, 240))
    for i, im in enumerate(cu):
        sheet.alpha_composite(K.upscale(im, S4), (x0 + (i % 2) * (132 * S4 + 8), 20 + (i // 2) * (60 * S4 + 26)))
    notes = [
        "Box 116x25 (foe) / 116x27 (player): stepped tab 72x11, body from row 7, 16x16 socket fills the body's inner height,",
        "10 px name pill, HP tag + 48 px bar, player EXP strip in the bottom edge. Each box = 2x 64x32 OBJ + 128x8 bar strip (as singles).",
        "Positions: foe (12,3) / (0,28); player (112,57) / (124,84) - vanilla spots nudged so 116 px fits the screen, pairs do not touch and nothing dips under the tray.",
        "Player HP numbers always on the tab (narrow digits), so the vanilla START bars<->numbers toggle becomes a no-op in doubles.",
        "OBJ palettes in doubles: 4 battlers (reserved) + vanilla healthbox (enemy shadows) + Orchid box + Orchid bar + status icons",
        "+ category icons + 3 gimmick indicators = 13; move select adds up to 3 type icons (16) - the vanilla bar palette is no longer loaded.",
        "OBJ tiles: 4 boxes x (64 + 16) + status sheet 36 = 356 (vanilla doubles 288); lineup sheets are loaded once (80).",
    ]
    for i, n in enumerate(notes):
        d.text((x0, 20 + 2 * (60 * S4 + 26) + i * 14), n, fill=(200, 200, 210))
    return sheet


# ================================================================== Safari player box
SAFARI_BALL = ["..III..",
               ".IGGGI.",
               "IGgGgGI",
               "IIIWIII",
               "IWWWWWI",
               ".IWWWI.",
               "..III.."]


def hb_safari(cv, balls_left):
    """Player box B with no HP / EXP: the pill reads SAFARI BALLS, the tab carries the ball
    count in brass after a small Safari Ball; the status socket stays an empty recess."""
    x, y, w, h = BX.hb_rect("B", "plr")
    saved = (BX.name_gender, BX.lv_text)
    BX.name_gender = lambda cv_, x_, y_, mon, *a, **k: draw_text(cv_, x_, y_, "SAFARI BALLS", INK, PANEL_SHADE, font="small")
    BX.lv_text = lambda *a, **k: None
    try:
        BX.hb_B(cv, M.default_player(), "safari")
    finally:
        BX.name_gender, BX.lv_text = saved
    s = "×%d" % balls_left
    tx = x + w - 5 - text_width(s, "small")
    draw_text(cv, tx, y - 2, s, BX.BRASS_LIGHT, BX.FRAME_DARK, font="small")
    # 3-step green from the Safari Ball item icon, on spare healthbox slots? -> uses FEMALE(red) slot
    stamp(cv, tx - 10, y + 2, SAFARI_BALL, {"I": INK, "G": BX.BRASS, "g": BX.BRASS_DARK, "W": WHITE})


def safari_sheet():
    out = BX.scene("grovyle", "zigzagoon", show_player=False)
    K.place(out, K.sprite_rgba(K.G("trainers", "back_pics", "brendan.png"), 0, 64), 80, 80)
    box = M.p_sheet(W, H, BX.HB_PAL)
    # hb_B with side 'safari' behaves like the player box minus HP numbers
    x, y, w, h = BX.hb_rect("B", "plr")
    real_rect = BX.hb_rect
    BX.hb_rect = lambda v, side: real_rect(v, "plr")
    try:
        hb_safari(Canvas(box), 30)
    finally:
        BX.hb_rect = real_rect
    M.comp(out, box)
    zig = M.default_enemy()
    M.healthboxes(out, None, zig, ("opp",))
    bg = M.p_sheet(W, H, M.UI_PAL)
    cv = Canvas(bg)
    M.draw_tray(cv)
    M.msg_panel(cv, 2, 126)
    draw_text(cv, M.MSG_X, M.MSG_Y, "What will\nBRENDAN do?", INK, PANEL_SHADE)
    M.comp(out, bg)
    win = M.p_sheet(W, H, M.MENU_PAL)
    wc = Canvas(win)
    saved = (M.ACTIONS, M.draw_text)
    M.ACTIONS = ["BALL", "{POKEBLOCK}", "GO NEAR", "RUN"]
    def dt(cv_, x_, y_, s_, fg, sh, font="normal", **k):
        if s_ == "FIGHT":
            w0 = text_width("FIGHT")
            s_ = "BALL"
            x_ += (w0 - text_width("BALL")) // 2
        if s_ == "{POKEBLOCK}":          # the ROM's 5-glyph POKéBLOCK ligature (charmap 55..59)
            for code in range(0x55, 0x5A):
                x_ = BX.draw_code(cv_, x_, y_, code, fg, sh, font=font)
            return x_
        return draw_text(cv_, x_, y_, s_, fg, sh, font=font, **k)
    M.draw_text = dt
    try:
        M.draw_action(wc, 0)
    finally:
        M.ACTIONS, M.draw_text = saved
    M.comp(out, win)
    M.button_fields(out)
    sheet = Image.new("RGBA", (16 + 480 + 16 + 140 * 4, 16 + 340), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    d.text((16, 2), "Safari: player box (2x frame + 4x close-up). No HP / EXP; SAFARI BALLS on the pill, brass ball count on the tab.", fill=(240, 220, 150))
    sheet.alpha_composite(K.upscale(out, 2), (16, 18))
    sheet.alpha_composite(K.upscale(out.crop((106, 74, 240, 112)), 4), (16 + 480 + 16, 18))
    for i, n in enumerate(["Action menu keeps the approved layout with Safari labels (BALL / {POKEBLOCK} ligature /",
                           "GO NEAR / RUN, so the label fits the pill). Icon fields stay as approved (fist / bag / ball /",
                           "shoe) unless you want Safari pictograms. Ball count = brass x30 after a brass Safari Ball",
                           "(healthbox palette has no green). Socket stays an empty recess; no HP tag, bar or EXP strip."]):
        d.text((16 + 480 + 16, 18 + 38 * 4 + 6 + i * 14), n, fill=(200, 200, 210))
    return sheet


# ================================================================== gimmick triggers
def trigger_rgba(name, frame=0):
    return K.sprite_rgba(K.G("battle_interface", name + "_trigger.png"), frame, 32)


def indicator_rgba(name):
    return K.sprite_rgba(K.G("battle_interface", name + "_indicator.png"), 0, 16)


TRIG_NOW = (112, 100)      # current sprite centre: healthbox.x - 30, healthbox.y + 5
TRIG_NEW = (101, 102)      # proposed: healthbox.x - 41, healthbox.y + 7 (left of the pointed end)


def gimmick_frame(trigger, indicator, pos, mon=None, label=None, info=True, info_dy=0, moves=True):
    mon = mon or M.default_player()
    out = BX.scene("grovyle", "zigzagoon")
    # player box with the indicator in place of the "Lv" glyph
    box = M.p_sheet(W, H, BX.HB_PAL)
    saved = BX.lv_text
    def lv_ind(cv, xr, y, lv, fg=INK, sh=PANEL_SHADE):
        _, widths = _font("small")
        wd = widths[0x34] + text_width(str(lv), "small")
        draw_text(cv, xr - wd + widths[0x34], y, str(lv), fg, sh, font="small")
    if indicator:
        BX.lv_text = lv_ind
    try:
        an = BX.hb_B(Canvas(box), mon, "plr")
    finally:
        BX.lv_text = saved
    M.comp(out, box)
    bars = M.p_sheet(W, H, M.HBAR_PAL)
    M.draw_bars(Canvas(bars), mon, an)
    M.comp(out, bars)
    M.healthboxes(out, None, M.default_enemy(), ("opp",))
    if mon.status:
        out.alpha_composite(SI.status_icon(mon.status.lower()), an["status"])
    if indicator:
        x, y, w, h = BX.hb_rect("B", "plr")
        _, widths = _font("small")
        lv_w = widths[0x34] + text_width(str(mon.lv), "small")
        ind = indicator_rgba(indicator)
        out.alpha_composite(ind, (x + w - 5 - lv_w, y - 6))         # 8x16, art in rows 7..15
    if trigger:
        t = trigger_rgba(trigger, 1)
        out.alpha_composite(t, (pos[0] - 16, pos[1] - 16))
    bg = M.p_sheet(W, H, M.UI_PAL)
    cv = Canvas(bg)
    M.draw_tray(cv)
    if moves:
        M.draw_back_tab(cv)
    M.comp(out, bg)
    win = M.p_sheet(W, H, M.MENU_PAL)
    if moves:
        M.draw_moves(Canvas(win), M.MOVES, 0)
    M.comp(out, win)
    if moves:
        M.type_icons(out, M.MOVES)
    if info:
        inf = K.sprite_rgba(K.G("battle_interface", "move_info_window_l.png"), 0, 32)
        out.alpha_composite(inf, (14 - 16, 92 - 16 + info_dy))
    if label:
        ImageDraw.Draw(out).text((2, 2), label, fill=(20, 20, 30))
    return out


def triggers_sheet():
    S = 2
    rows = [
        ("now: Mega trigger at healthbox.x-30 / y+5 covers the status socket; move info overlaps the BACK tab by 2 rows",
         [gimmick_frame("mega", None, TRIG_NOW, M.default_player().copy(status="PSN"), info=True)]),
        ("proposed: triggers 11 px further left and 2 px lower (clear of the pointed end + socket); move info 3 px up",
         [gimmick_frame("mega", "mega", TRIG_NEW, M.default_player().copy(status="PSN"), info=True, info_dy=-3),
          gimmick_frame("tera", "fire", TRIG_NEW, info=True, info_dy=-3)]),
        ("proposed, continued: Z-Move, Dynamax (indicator replaces the Lv glyph, 8x9 art = the glyph's size)",
         [gimmick_frame("z_move", None, TRIG_NEW, info=True, info_dy=-3),
          gimmick_frame("dynamax", "dynamax", TRIG_NEW, info=True, info_dy=-3)]),
    ]
    sheet = Image.new("RGBA", (16 + 2 * (480 + 16), 16 + len(rows) * (320 + 30)), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    y = 8
    for label, frames in rows:
        d.text((16, y), label, fill=(240, 220, 150))
        for i, f in enumerate(frames):
            sheet.alpha_composite(K.upscale(f, S), (16 + i * (480 + 16), y + 16))
        y += 320 + 30
    return sheet


# ================================================================== 4-digit HP (Dynamax)
def dynamax_sheet():
    mon = M.default_player().copy(hp=1428, maxhp=1428, lv=100)
    sky = BX.environment().getpixel((4, 60))
    def box(current_only, indicator, hp=None):
        f = Image.new("RGBA", (W, H), sky)
        b = M.p_sheet(W, H, BX.HB_PAL)
        saved_dt, saved_lv = BX.draw_text, BX.lv_text
        def dt(cv, x, y, s, fg, sh, font="normal", **k):
            if "/" in s or s.isdigit() and len(s) >= 3 and fg == BX.BRASS_LIGHT and s != str(mon.lv):
                xr = x + text_width(s, "small")
                s2 = ("%d" % (hp or mon.hp)) if current_only else s
                return saved_dt(cv, xr - text_width(s2, HP_FONT), y, s2, fg, sh, font=HP_FONT, **k)
            return saved_dt(cv, x, y, s, fg, sh, font=font, **k)
        def lv_ind(cv, xr, y, lv, fg=INK, sh=PANEL_SHADE):
            _, widths = _font("small")
            wd = widths[0x34] + text_width(str(lv), "small")
            saved_dt(cv, xr - wd + widths[0x34], y, str(lv), fg, sh, font="small")
        BX.draw_text = dt
        if indicator:
            BX.lv_text = lv_ind
        try:
            m = mon.copy(hp=hp or mon.hp)
            an = BX.hb_B(Canvas(b), m, "plr")
        finally:
            BX.draw_text, BX.lv_text = saved_dt, saved_lv
        M.comp(f, b)
        bars = M.p_sheet(W, H, M.HBAR_PAL)
        M.draw_bars(Canvas(bars), m, an)
        M.comp(f, bars)
        if indicator:
            x, y, w, h = BX.hb_rect("B", "plr")
            f.alpha_composite(indicator_rgba("dynamax"), (x + w - 5 - 8 - text_width("100", "small"), y - 6))
        return f.crop((106, 74, 240, 114))
    tiles = [("as is: 1428/1428 + Dynamax indicator overflows the tab", box(False, True)),
             ("proposed: max HP >= 1000 -> current HP only", box(True, True)),
             ("proposed, mid drain (731)", box(True, True, hp=731)),
             ("unchanged below 1000 (Dynamax ended): 714/714", None)]
    mon = mon.copy(hp=714, maxhp=714)
    tiles[3] = (tiles[3][0], box(False, False))
    S = 4
    sheet = Image.new("RGBA", (16 + 2 * (134 * S + 12), 16 + 2 * (40 * S + 30)), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(tiles):
        x, y = 16 + (i % 2) * (134 * S + 12), 8 + (i // 2) * (40 * S + 30)
        d.text((x, y), label, fill=(240, 220, 150))
        sheet.alpha_composite(K.upscale(im, S), (x, y + 16))
    return sheet


# ================================================================== Safari action pictograms (proposal)
SAFARI_SILHOUETTES = {
    "safari_ball": [      # Safari Ball: camo-hatched top half, band + button, plain lower half
        "....XXXXXX....",
        "..XX.XX.XX.X..",
        ".X.XX.XX.XX.X.",
        ".XX.XX.XX.XX..",
        "X.XX.XX.XX.XXX",
        "XXXXX....XXXXX",
        ".....X..X.....",
        "XXXXX....XXXXX",
        "XXXXXXXXXXXXXX",
        ".XXXXXXXXXXXX.",
        "..XXXXXXXXXX..",
        "....XXXXXX....",
    ],
    "block": [            # PokéBlock: isometric cube, a Y of gaps splits the three faces
        "....XX....",
        "..XXXXXX..",
        "XXXXXXXXXX",
        "X..XXXX..X",
        "XXX.XX.XXX",
        "XXXX..XXXX",
        "XXXX..XXXX",
        "XXXX..XXXX",
        ".XXX..XXX.",
        "...X..X...",
    ],
    "go_near": [          # two footprints stepping up-right, 2 px apart (8 px wide, nothing clipped)
        "......XX",
        ".....XXX",
        ".....XXX",
        "XX...XX.",
        "XXX.....",
        "XXX..XX.",
        ".XX..XX.",
        "........",
        ".XX.....",
        ".XX.....",
    ],
    # BALL: the POKéMON button's Poké Ball pictogram at an integer 2x
    "ball2x": [row.replace("X", "XX").replace(".", "..") for row in BX.SILHOUETTES["pokemon"] for _ in (0, 1)],
}
SAFARI_COL = ["green", "yellow", "red", "blue"]      # BALL / BLOCK / GO NEAR / RUN (same 4 ramps)


def _safari_field(cv, x, y, w, h, colour, icon, r=3):
    rounded_box(cv, x, y, w, h, r, M.btn_idx(colour, 1), 1, M.btn_idx(colour, 0), M.btn_idx(colour, 2))
    rows = SAFARI_SILHOUETTES.get(icon) or BX.SILHOUETTES[icon]
    pw, ph = len(rows[0]) + 1, len(rows) + 1
    BX.silhouette(cv, x + (w - pw + 1) // 2, y + (h - ph + 1) // 2, rows, 2, M.btn_idx(colour, 2))


def safari_tray(cursor, proposed):
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bg = M.p_sheet(W, H, M.UI_PAL)
    cv = Canvas(bg)
    M.draw_tray(cv)
    M.msg_panel(cv, 2, 126)
    draw_text(cv, M.MSG_X, M.MSG_Y, "What will\nBRENDAN do?", INK, PANEL_SHADE)
    M.comp(out, bg)
    win = M.p_sheet(W, H, M.MENU_PAL)
    saved = (M.ACTIONS, M.draw_text)
    M.ACTIONS = ["BALL", "BLOCK", "GO NEAR", "RUN"]
    def dt(cv_, x_, y_, s_, fg, sh, font="normal", **k):
        if s_ == "FIGHT":
            x_ += (text_width("FIGHT") - text_width("BALL")) // 2
            s_ = "BALL"
        return draw_text(cv_, x_, y_, s_, fg, sh, font=font, **k)
    M.draw_text = dt
    try:
        M.draw_action(Canvas(win), cursor)
    finally:
        M.ACTIONS, M.draw_text = saved
    M.comp(out, win)
    if proposed:
        im = M.p_sheet(W, H, M.BTN_PAL)
        fc = Canvas(im)
        _safari_field(fc, *M.FIGHT_FIELD, "green", "ball2x", r=4)
        icons = ["block", "go_near", "run"]
        for i in range(3):
            x, y, w, h = M.side_rect(i)
            _safari_field(fc, x, y, M.SIDE_FIELD_W, h, SAFARI_COL[i + 1], icons[i])
        M.comp(out, im)
    else:
        M.button_fields(out)
    sky = Image.new("RGBA", (W, H), (28, 28, 36, 255))
    sky.alpha_composite(out)
    return sky.crop((0, M.TRAY - 2, W, H))


def safari_icons_sheet():
    S = 4
    th = H - (M.TRAY - 2)
    rows = [("current (FIGHT / BAG / POKéMON pictograms)", [safari_tray(c, False) for c in (0, 1)]),
            ("approved: Poké Ball pictogram at 2x (green), PokéBlock cube (yellow), footprints closer together (red), RUN shoe (blue)",
             [safari_tray(c, True) for c in (0, 1)]),
            ("proposed, GO NEAR / RUN selected", [safari_tray(c, True) for c in (2, 3)])]
    sheet = Image.new("RGBA", (16 + 2 * (W + 16) + 2 * (120 * S + 16), 16 + len(rows) * (th * S + 30)), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    y = 8
    for label, ims in rows:
        d.text((16, y), label + "   (1x left, 4x right: right half of the tray)", fill=(240, 220, 150))
        for i, im in enumerate(ims):
            sheet.alpha_composite(im, (16 + i * (W + 16), y + 16))
            sheet.alpha_composite(K.upscale(im.crop((120, 0, 240, th)), S), (16 + 2 * (W + 16) + i * (120 * S + 16), y + 16))
        y += th * S + 30
    d.text((16, y - 10), "Same 32x32 / 16x16 icon-field OBJ and the same BTN_PAL ramps (no extra palette); Safari loads its own 28-tile sheet instead of the standard one.", fill=(200, 200, 210))
    return sheet


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    doubles_sheet().save(os.path.join(OUT, "doubles_mock.png"))
    safari_sheet().save(os.path.join(OUT, "safari_mock.png"))
    triggers_sheet().save(os.path.join(OUT, "triggers_mock.png"))
    dynamax_sheet().save(os.path.join(OUT, "dynamax_hp_mock.png"))
    safari_icons_sheet().save(os.path.join(OUT, "safari_icons_mock.png"))
    print("ok")
