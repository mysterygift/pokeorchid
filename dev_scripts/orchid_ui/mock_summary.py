"""
Pixel-accurate mockups of the Orchid Pokémon summary screen ("Gen 5 layout, Gen 3 pixels").

Player-owned screen -> gender theme (male blue hero, female rose in a state).
Pages follow include/config/summary_screen.h + contest.h of the satchel worktree:
INFO (A: RENAME), SKILLS (A cycles STATS / IVs / EVs, values shown as numbers),
BATTLE MOVES (A: INFO / SWITCH, START: RELEARN). CONTEST MOVES is hidden (user decision:
C_HIDE_CONTEST_DATA TRUE); render_contest() is kept in case Orchid ever keeps contests.

Layers (bottom-up, like the GBA):
    BG3  BW scrolling grid (own palette)
    BG2  right-hand page art (one tilemap per page; slides on page switch, clipped by WIN0
         to x >= 90); selected / moving pills = palette 1 / 2 cell swaps
    BG1  static art: stepped tab header + left column (dais with ball / status sockets,
         name pill, No. pill, held-item row); detail tray in move-select mode
    BG0  text windows (text palette: kit roles + gender / nature colours; move windows use
         the battle PP-colour palette)
    OBJ  front pic, ball, status tag, item icon, type icons, category tag, red chevrons

usage: mock_summary.py OUT_DIR
"""
import json
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as KX
import dex_ext as D
import status_icons as SI
import mock_battle as MB
import summary_ext as S
from battle_ext import draw_code
from gamefont import draw_text, text_width, _font

W, H = 240, 160

# ------------------------------------------------------------------ layout
TABS = ["INFO", "SKILLS", "MOVES"]            # contest page hidden (C_HIDE_CONTEST_DATA TRUE)
TAB_W, TAB_GAP = 62, 4
TAB_X0 = (W - (3 * TAB_W + 2 * TAB_GAP)) // 2          # 23
TAB_ARROWS = ((11, 8), (228, 8))
CONTENT_Y = 20

DAIS_C, DAIS_R, DAIS_IN = (44, 60), 38, 30
SOCK_BALL, SOCK_STATUS = (12, 86), (76, 86)             # rim studs, lower corners
LX, LW = 2, 84                                         # left column pills
NAME_Y, NO_Y, ITEM_Y = 104, 120, 135
NO_CAP = 26

RX, RW = 92, 146                                       # right page: x 92..237
CAP = 44                                               # stat / info label caps
ROW = 17                                               # info row pitch
STAT_Y0, STAT_PITCH = 36, 15                          # HP row alone, then 5 stats + EXP/NEXT
MOVE_H, MOVE_PITCH = 19, 20
TRAY_Y = 120                                           # just under the name pill                                           # move-select detail tray
DESC_X, DESC_PITCH = 94, 14
HINT_Y = 146

PAGE_CLIP_X = 90                                       # WIN0 left edge for the page slide


def stage_y():
    return DAIS_C[1] + int(DAIS_IN * 0.55) + 3


# ------------------------------------------------------------------ small helpers
def sheet(theme, pal=None):
    im = new_sheet(W, H, theme)
    return im


def comp(out, im, pal, at=(0, 0)):
    out.alpha_composite(KX.sheet_rgba(im, pal), at)


def lv_text(cv, x, y, lv, fg=INK, sh=PANEL_SHADE, right=True):
    _, widths = _font("small")
    wd = widths[0x34] + text_width(str(lv), "small")
    if right:
        x -= wd
    x = draw_code(cv, x, y, 0x34, fg, sh)
    draw_text(cv, x, y, str(lv), fg, sh, font="small")


def rtext(cv, xr, y, s, fg, sh, font="normal"):
    draw_text(cv, xr - text_width(s, font), y, s, fg, sh, font=font)


def ctext(cv, x0, w, y, s, fg, sh, font="normal"):
    draw_text(cv, x0 + (w - text_width(s, font)) // 2, y, s, fg, sh, font=font)


def cap_text(cv, x, y, cap_w, s):
    """WHITE label on the accent cap of a label pill (dex HT/WT rule)."""
    f = "normal" if text_width(s) <= cap_w - 4 else "narrow"
    draw_text(cv, x + (cap_w - text_width(s, f)) // 2 + 1, y - 1, s, WHITE, ACCENT_DARK, font=f)


def cap_pill(cv, x, y, w, h=14):
    """A label pill that is all cap (TYPE)."""
    rounded_box(cv, x, y, w, h, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)


def tri(cv, x, y, up, c):
    rows = ["...X...", "..XXX..", ".XXXXX.", "XXXXXXX"]
    rows = rows if up else rows[::-1]
    stamp(cv, x, y, rows, {"X": c})


# ------------------------------------------------------------------ BG1: header + left column
def draw_header(cv, page, style="B", learn=False, egg=False):
    vis = [0] if egg else None
    if style == "C" and not learn:
        return S.tab_strip_icons(cv, page, len(TABS))
    if learn:
        S.tab_strip(cv, TABS, -1, TAB_X0, TAB_W, TAB_GAP, style, visible=[])
        return []
    return S.tab_strip(cv, TABS, page, TAB_X0, TAB_W, TAB_GAP, style, visible=vis)


def draw_left(cv, mon):
    D.dais(cv, DAIS_C[0], DAIS_C[1], DAIS_R, DAIS_IN)
    S.socket(cv, *SOCK_BALL)
    S.socket(cv, *SOCK_STATUS)
    rounded_box(cv, LX, NAME_Y, LW, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    if mon.egg:
        return
    D.label_pill(cv, LX, NO_Y, LW, NO_CAP)
    S.item_row(cv, LX - 1, ITEM_Y, LW + 1)


def left_text(tc, mon, tray=False):
    fg, sh = S.gender_ink(mon.gender)
    draw_text(tc, LX + 5, NAME_Y - 1, mon.name, fg, sh)
    if mon.egg:
        return
    lv_text(tc, LX + LW - 5, NAME_Y + 1, mon.lv)
    if tray:                         # detail tray covers the No. / item rows
        return
    cap_text(tc, LX, NO_Y, NO_CAP, "No.")
    rtext(tc, LX + LW - 6, NO_Y - 1, "%03d" % mon.dex, INK, PANEL_SHADE)
    name = mon.item_name or "None"
    f = "normal" if text_width(name) <= LW - 30 else "narrow"
    draw_text(tc, LX + 25, ITEM_Y + 3, name, INK if mon.item else INK_SOFT, PANEL_SHADE, font=f)


def left_objs(out, mon, sprite_frame=0, sprite_dy=0, tray=False):
    spr = KX.mon_front(mon.species, sprite_frame)
    out.alpha_composite(spr, (DAIS_C[0] - 32, stage_y() - D.sprite_bottom(spr) + sprite_dy))
    if mon.ball:
        b = S.ball_sprite(mon.ball)
        out.alpha_composite(b, (SOCK_BALL[0] - 8, SOCK_BALL[1] - 8))
    if mon.status:
        out.alpha_composite(SI.status_icon(mon.status), (SOCK_STATUS[0] - 8, SOCK_STATUS[1] - 8))
    if mon.item and not tray:
        ic = KX.item_icon(mon.item)
        out.alpha_composite(ic, (LX + 10 - 12, ITEM_Y + 11 - 12))


# ------------------------------------------------------------------ page builders
class Page:
    """One right-hand page: BG2 art (normal / gold / moving cells), BG0 text, OBJs."""

    def __init__(self, theme):
        self.theme = theme
        self.art, self.sel, self.mov = sheet(theme), sheet(theme), sheet(theme)
        self.a, self.s, self.m = Canvas(self.art), Canvas(self.sel), Canvas(self.mov)
        self.txt, self.mtxt = sheet(theme), sheet(theme)
        self.t, self.mt = Canvas(self.txt), Canvas(self.mtxt)
        self.bars = MB.p_sheet(W, H, MB.HBAR_PAL)
        self.b = Canvas(self.bars)
        self.objs = []          # (rgba, (x, y))
        self.static = []        # extra BG1 art callbacks (tray) drawn on the static layer

    def art_rgba(self):
        pal = S.art_pal(self.theme)
        im = KX.sheet_rgba(self.art, pal)
        im.alpha_composite(KX.sheet_rgba(self.sel, S.selected(pal)))
        im.alpha_composite(KX.sheet_rgba(self.mov, S.moving(pal)))
        im.alpha_composite(KX.sheet_rgba(self.bars))
        return im

    def text_rgba(self):
        im = KX.sheet_rgba(self.txt, S.txt_pal(self.theme))
        im.alpha_composite(KX.sheet_rgba(self.mtxt, S.move_txt_pal(self.theme)))
        return im


def info_page(pg, mon):
    a, t = pg.a, pg.t
    half = (RW - 4) // 2
    # OT | ID
    D.label_pill(a, RX, CONTENT_Y, half, 22)
    D.label_pill(a, RX + RW - half, CONTENT_Y, half, 22)
    cap_text(t, RX, CONTENT_Y, 22, "OT")
    fg, sh = S.gender_ink(mon.ot_gender)
    f = "normal" if text_width(mon.ot) <= half - 22 - 10 else "narrow"
    rtext(t, RX + half - 6, CONTENT_Y - 1, mon.ot, fg, sh, f)
    cap_text(t, RX + RW - half, CONTENT_Y, 22, "ID")
    rtext(t, RX + RW - 6, CONTENT_Y - 1, mon.id_no, INK, PANEL_SHADE)
    if mon.egg:
        return egg_info(pg, mon)
    # TYPE: cap-only pill + Gen 3 type icons on the grid (dex entry rule)
    y = CONTENT_Y + ROW
    cap_pill(a, RX, y, CAP)
    cap_text(t, RX, y, CAP, "TYPE")
    for k, ty in enumerate(mon.types):
        pg.objs.append((KX.type_icon(ty), (RX + CAP + 6 + 36 * k, y - 1)))
    # NATURE
    y += ROW
    D.label_pill(a, RX, y, RW, CAP)
    cap_text(t, RX, y, CAP, "NATURE")
    mx = _nature_hint(t, RX + RW - 6, y, mon)
    nx = RX + CAP + 6
    nf = "normal" if nx + text_width(mon.nature) + NATURE_GAP <= mx else "narrow"
    assert nx + text_width(mon.nature, nf) + NATURE_GAP <= mx, mon.nature
    draw_text(t, nx, y - 1, mon.nature, INK, PANEL_SHADE, font=nf)
    # ABILITY + description drawer under it
    y += ROW
    rounded_box(a, RX + 4, y + 8, RW - 8, 23, 3, WHITE, INK, WHITE, PANEL_SHADE)
    a.hline(RX + 6, RX + RW - 7, y + 14, PANEL_SHADE)
    D.label_pill(a, RX, y, RW, CAP)
    cap_text(t, RX, y, CAP, "ABILITY")
    draw_text(t, RX + CAP + 6, y - 1, mon.ability, INK, PANEL_SHADE)
    desc = mon.ability_desc
    f = "normal" if text_width(desc) <= RW - 18 else "narrow"
    draw_text(t, RX + 9, y + 13, desc, INK, PANEL_SHADE, font=f)
    # MET: level in the pill, place in a drawer under it (same build as ABILITY)
    y += 34
    rounded_box(a, RX + 4, y + 8, RW - 8, 23, 3, WHITE, INK, WHITE, PANEL_SHADE)
    D.label_pill(a, RX, y, RW, CAP)
    cap_text(t, RX, y, CAP, "MET")
    lv_text(t, RX + CAP + 6, y + 1, mon.met_lv, right=False)
    f = "normal" if text_width(mon.met_place) <= RW - 18 else "narrow"
    draw_text(t, RX + 9, y + 13, mon.met_place, INK, PANEL_SHADE, font=f)
    pg.hint = ("A", "RENAME")


NATURE_GAP = 5          # min px between the nature name and its marks


def nature_marks_w(mon):
    names = dict(atk="ATK", def_="DEF", spa="SPA", spd="SPD", spe="SPE")
    return 8 + text_width(names[mon.up], "small") + 3 + 8 + text_width(names[mon.down], "small")


def _nature_hint(t, xr, y, mon):
    """Small +/- stat pair right-aligned in the NATURE pill: ▲ATK ▼SPA (nature colours).
    Returns the marks' left edge so the name can keep clear of it."""
    names = dict(atk="ATK", def_="DEF", spa="SPA", spd="SPD", spe="SPE")
    if mon.up == mon.down:                 # neutral nature: no marks
        return xr
    s_dn, s_up = names[mon.down], names[mon.up]
    x0 = x = xr - nature_marks_w(mon)
    tri(t, x, y + 5, True, S.NAT_UP_FG)
    draw_text(t, x + 8, y + 1, s_up, S.NAT_UP_FG, S.NAT_UP_SH, font="small")
    x += 8 + text_width(s_up, "small") + 3
    tri(t, x, y + 5, False, S.NAT_DOWN_FG)
    draw_text(t, x + 8, y + 1, s_dn, S.NAT_DOWN_FG, S.NAT_DOWN_SH, font="small")
    return x0


def egg_info(pg, mon):
    a, t = pg.a, pg.t
    y = CONTENT_Y + ROW
    for k, (cap, text) in enumerate((("WATCH", "It looks like this EGG will\ntake a long time to hatch."),
                                     ("MEMO", "A POKéMON EGG received\nin %s." % mon.met_place))):
        yy = y + k * 50
        rounded_box(a, RX + 4, yy + 8, RW - 8, 38, 3, WHITE, INK, WHITE, PANEL_SHADE)
        a.hline(RX + 6, RX + RW - 7, yy + 14, PANEL_SHADE)
        cap_pill(a, RX, yy, CAP + 8)
        cap_text(t, RX, yy, CAP + 8, cap)
        f = "normal" if max(text_width(l) for l in text.split("\n")) <= RW - 18 else "narrow"
        draw_text(t, RX + 9, yy + 14, text, INK, PANEL_SHADE, font=f, line_h=DESC_PITCH)
    pg.hint = None


STATS = [("ATTACK", "atk"), ("DEFENSE", "def_"), ("SP. ATK", "spa"), ("SP. DEF", "spd"), ("SPEED", "spe")]


def skills_page(pg, mon, mode="stats"):
    """mode: stats | ivs | evs."""
    a, t, b = pg.a, pg.t, pg.b
    y = CONTENT_Y
    D.label_pill(a, RX, y, RW, CAP)
    cap_text(t, RX, y, CAP, "HP")
    bx = RX + CAP + 6
    if mode == "stats":
        lvl, n = MB.hp_level(mon.hp, mon.maxhp)
        _hbar(b, bx, y + 5, n, lvl)
        rtext(t, RX + RW - 6, y - 1, "%d/%d" % (mon.hp, mon.maxhp), INK, PANEL_SHADE)
    else:
        _gold_bar(a, bx, y + 5, mon, "hp", mode)
        rtext(t, RX + RW - 6, y - 1, str(getattr(mon, mode)["hp"]), INK, PANEL_SHADE)
    for k, (lab, key) in enumerate(STATS):
        yy = STAT_Y0 + k * STAT_PITCH
        D.label_pill(a, RX, yy, RW, CAP)
        cap_text(t, RX, yy, CAP, lab)
        if mode == "stats":
            v = mon.stats[key]
            fg, sh = INK, PANEL_SHADE
            if key == mon.up:
                fg, sh = S.NAT_UP_FG, S.NAT_UP_SH
                tri(t, RX + CAP + 6, yy + 5, True, fg)
            elif key == mon.down:
                fg, sh = S.NAT_DOWN_FG, S.NAT_DOWN_SH
                tri(t, RX + CAP + 6, yy + 5, False, fg)
            rtext(t, RX + RW - 6, yy - 1, str(v), fg, sh)
        else:
            _gold_bar(a, bx, yy + 5, mon, key, mode)
            rtext(t, RX + RW - 6, yy - 1, str(getattr(mon, mode)[key]), INK, PANEL_SHADE)
    # EXP block
    y = STAT_Y0 + 5 * STAT_PITCH + 3
    D.label_pill(a, RX, y, RW, CAP)
    cap_text(t, RX, y, CAP, "EXP")
    rtext(t, RX + RW - 6, y - 1, "{:,}".format(mon.exp), INK, PANEL_SHADE)
    y += STAT_PITCH
    D.label_pill(a, RX, y, RW, CAP)
    cap_text(t, RX, y, CAP, "NEXT")
    _ebar(b, bx, y + 5, mon.exp_frac)
    rtext(t, RX + RW - 6, y - 1, str(mon.exp_next - mon.exp), INK, PANEL_SHADE)
    pg.hint = ("A", {"stats": "IVs", "ivs": "EVs", "evs": "STATS"}[mode])


def _hbar(cv, x, y, n, lvl, w=48):
    I = MB.HB_I
    cv.rect(x, y, x + w + 1, y + 4, I["ink"])
    cv.rect(x + 1, y + 1, x + w, y + 3, I["trough"])
    cv.hline(x + 1, x + w, y + 1, I["trough_hi"])
    if n:
        cv.rect(x + 1, y + 1, x + n, y + 3, I[lvl + "2"])
        cv.hline(x + 1, x + n, y + 1, I[lvl + "1"])


def _ebar(cv, x, y, frac, w=48):
    I = MB.HB_I
    cv.rect(x, y, x + w + 1, y + 4, I["ink"])
    cv.rect(x + 1, y + 1, x + w, y + 3, I["trough"])
    cv.hline(x + 1, x + w, y + 1, I["trough_hi"])
    n = int(round(w * frac))
    if n:
        cv.rect(x + 1, y + 1, x + n, y + 3, I["e2"])
        cv.hline(x + 1, x + n, y + 1, I["e1"])


def _gold_bar(cv, x, y, mon, key, mode, w=48):
    v = getattr(mon, mode)[key]
    mx = 31 if mode == "ivs" else 252
    KX.bar(cv, x, y, w, v / mx, SELECT_LIGHT, SELECT_DARK, trough=PANEL_DARK, h=3)


def moves_page(pg, mon, cursor=None, mode="view", moving=None, new_move=None, contest=False):
    """mode: view (list, no cursor) | select (gold cursor + tray) | learn (5th new move) | swap."""
    a, t, mt = pg.a, pg.t, pg.mt
    keys = list(mon.moves) + ([new_move] if new_move else [])
    for i, key in enumerate(keys):
        name, typ, pp, mx, cat, pw, acc, desc = S.MV[key]
        y = CONTENT_Y + i * MOVE_PITCH
        cv = pg.s if i == cursor else pg.m if i == moving else a
        S.move_pill(cv, RX, y, RW, MOVE_H)
        f = "normal" if text_width(name) <= RW - 42 - 46 else "narrow"
        if i == cursor:
            draw_text(mt, RX + 38, y - 1, name, INK, SELECT_DARK, font=f)
        elif i == moving:
            draw_text(mt, RX + 38, y - 1, name, ACCENT_DARK, None, font=f)
        else:
            draw_text(mt, RX + 38, y - 1, name, INK, PANEL_SHADE, font=f)
        # PP notch (battle language)
        nx0, nx1, ny0, ny1, px, num = S.pp_notch_rect(RX, y, RW, MOVE_H, pp, mx)
        S.notch(cv, nx0, nx1, ny0, ny1)
        draw_text(mt, px, y + 8, "PP", PANEL_DARK, None, font="small")
        draw_text(mt, px + text_width("PP ", "small"), y + 8, num, S.PP_INDEX[S.pp_state(pp, mx)], None, font="small")
        if new_move and i == len(keys) - 1:
            _new_flag(cv, mt, RX + RW - 29, y)
        icon = KX.type_icon(("contest_" + S.CONTEST[key][0]) if contest else typ)
        pg.objs.append((icon, (RX + 3, y + 2)))
    if mode == "view":
        pg.hint = ("A", "INFO")
        pg.hint2 = None if contest else ("START", "RELEARN")
        return
    pg.hint = None
    # detail tray (BG1, covers the lower left column)
    key = keys[cursor]
    name, typ, pp, mx, cat, pw, acc, desc = S.MV[key]
    pg.static.append(lambda cv: S.move_tray(cv, TRAY_Y))
    pg.tray_text = (cat, pw, acc, desc)


def _new_flag(cv, mt, x, y):
    """Brass 'NEW' notch cut into the pill's top edge (mirror of the PP notch)."""
    cv.rect(x, y, x + 22, y + 9, INK)
    cv.rect(x + 1, y + 1, x + 21, y + 8, SELECT)
    cv.vline(x + 1, y + 1, y + 8, SELECT_LIGHT)
    cv.vline(x + 21, y + 1, y + 8, SELECT_DARK)
    cv.set(x, y + 9, cv.get(x - 1, y + 9))
    cv.set(x + 22, y + 9, cv.get(x + 23, y + 9))
    draw_text(mt, x + 4, y - 3, "NEW", INK, None, font="small")


def tray_text(tc, out, cat, pw, acc, desc):
    y0 = TRAY_Y
    out.alpha_composite(S.cat_icon(cat), (8, y0 + 12))
    for k, (lab, v) in enumerate((("POWER", pw), ("ACC.", acc))):
        yy = y0 + 2 + k * DESC_PITCH
        draw_text(tc, 30, yy, lab, INK_SOFT, PANEL_SHADE, font="narrow")
        rtext(tc, 84, yy, str(v) if v else "---", INK, PANEL_SHADE)
    lines = desc.split("\n")
    f = "normal" if max(text_width(l) for l in lines) <= 240 - DESC_X - 4 else "narrow"
    draw_text(tc, DESC_X, y0 + 2, desc, INK, PANEL_SHADE, font=f, line_h=DESC_PITCH)


# ------------------------------------------------------------------ render
def build_page(page, mon, theme, **kw):
    pg = Page(theme)
    pg.hint = pg.hint2 = None
    pg.tray_text = None
    if page == 0:
        info_page(pg, mon)
    elif page == 1:
        skills_page(pg, mon, kw.get("skills_mode", "stats"))
    else:
        moves_page(pg, mon, kw.get("cursor"), kw.get("mode", "view"), kw.get("moving"),
                   kw.get("new_move"), contest=page == 3)
    return pg


def render(page=1, mon=None, theme="male", grid_scroll=0, style="B", page_dx=0, show_text=True,
           other=None, other_dx=0, sprite_frame=0, sprite_dy=0, hide_page_objs=False, **kw):
    """page 0 INFO / 1 SKILLS / 2 MOVES (3 CONTEST: only if contests return). kw -> page builder (cursor, mode, moving,
    new_move, skills_mode). other = a second Page sliding alongside (page switch animation)."""
    mon = mon or S.hero()
    pal = S.art_pal(theme)
    out = KX.grid_frame(grid_scroll)
    learn = kw.get("mode") == "learn"
    pg = build_page(page, mon, theme, **kw)

    # BG2 page art (slides, clipped at PAGE_CLIP_X by WIN0)
    for p, dx in ((pg, page_dx),) + (((other, other_dx),) if other else ()):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(p.art_rgba(), (dx, 0))
        if p is pg and show_text and dx == 0:
            lay.alpha_composite(p.text_rgba())
        clip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        clip.paste(lay.crop((PAGE_CLIP_X, 0, W, H)), (PAGE_CLIP_X, 0))
        out.alpha_composite(clip)

    # BG1 static art: header, left column, tray
    art = sheet(theme)
    ac = Canvas(art)
    rects = draw_header(ac, page, style, learn, mon.egg)
    draw_left(ac, mon)
    for fn in pg.static:
        fn(ac)
    a = KX.sheet_rgba(art, pal)
    if rects and 0 <= page < len(rects) and rects[page]:
        x0, y0, x1, y1 = rects[page]
        a.alpha_composite(KX.sheet_rgba(art.crop((x0, y0, x1 + 1, y1 + 1)), S.selected(pal)), (x0, y0))
    out.alpha_composite(a)

    # BG0 text (static windows) + hints
    txt = sheet(theme)
    tc = Canvas(txt)
    if learn:
        msg = "Forget which move?"
        draw_text(tc, 8, -1, msg, WHITE, ACCENT_DARK)
    elif rects:
        for i, r in enumerate(rects):
            if r is None:
                continue
            x0, y0, x1, y1 = r
            label = TABS[i]
            if i == 1 and kw.get("skills_mode", "stats") != "stats" and page == 1:
                label = kw["skills_mode"].upper()[:-1] + "s"
            fg, sh = (INK, SELECT_DARK) if i == page else (INK_SOFT, PANEL_SHADE)
            f = "normal" if text_width(label) <= TAB_W - 6 else "narrow"
            if style == "C":
                if i == page:
                    ctext(tc, x0 + 14, x1 - x0 - 16, 1, label, fg, sh, f)
                continue
            ctext(tc, x0, TAB_W, 1 if i == page else 2, label, fg, sh, f)
    left_text(tc, mon, bool(pg.static))
    hint_art = sheet(theme)
    hc = Canvas(hint_art)
    if show_text and page_dx == 0:
        if learn:
            S.hint_tab(hc, 170, 2, "B", "CANCEL")
        elif not pg.static:
            items = [h for h in (pg.hint, pg.hint2) if h]
            xr = RX + RW
            for hb, lab in items:
                wdt = S.hint_w(hb, lab)
                S.hint_tab(hc, xr - wdt, HINT_Y, hb, lab)
                xr -= wdt + 4
    if pg.tray_text:
        tray_text(tc, out, *pg.tray_text)
    comp(out, hint_art, pal)
    comp(out, txt, S.txt_pal(theme))

    # OBJ
    left_objs(out, mon, sprite_frame, sprite_dy, bool(pg.static))
    if pg.tray_text:
        out.alpha_composite(S.cat_icon(pg.tray_text[0]), (8, TRAY_Y + 12))
    if not hide_page_objs and page_dx == 0:
        for spr, (x, y) in pg.objs:
            out.alpha_composite(spr, (x, y))
    if not learn and not mon.egg:
        for i, (ax, ay) in enumerate(TAB_ARROWS):
            D.chevron(out, ax, ay, right=i == 1)
    return out


def render_info(mon=None, theme="male", **kw):
    return render(0, mon, theme, **kw)


def render_skills(mon=None, theme="male", skills_mode="stats", **kw):
    return render(1, mon, theme, skills_mode=skills_mode, **kw)


def render_moves(mon=None, theme="male", cursor=None, mode="view", moving=None, new_move=None, **kw):
    return render(2, mon, theme, cursor=cursor, mode=mode, moving=moving, new_move=new_move, **kw)


def render_contest(mon=None, theme="male", **kw):
    return render(3, mon, theme, **kw)


def render_egg(theme="male", **kw):
    return render(0, S.egg_mon(), theme, **kw)


def save(im, path, k=3):
    KX.upscale(im.convert("RGB"), k).save(path)


STATES = [
    ("state_01.png", "INFO page", "OT / ID, Gen 3 type icons, nature (with its +/- stats), ability with its description in a drawer, met level + place. A: RENAME.",
     lambda: render_info()),
    ("state_02.png", "SKILLS page (hero)", "Stat pills; HP with the Gen 3 HP bar; nature-boosted stat in rose with an up mark, lowered in blue with a down mark; EXP total and the EXP bar to the next level. A cycles IVs / EVs.",
     lambda: render_skills()),
    ("state_03.png", "BATTLE MOVES list", "Moves as type-capped pills with the battle PP notch (PP warning colours). No cursor until A. START: RELEARN (summary relearner is on). The CONTEST MOVES page is hidden (C_HIDE_CONTEST_DATA TRUE); it returns as a 4th tab with the same pills and Gen 3 contest icons if Orchid ever keeps contests.",
     lambda: render_moves()),
    ("state_04.png", "Move selected + detail tray", "Gold pill = cursor. The detail tray rises over the lower left column: category tag, POWER, ACC., and the description at a 14px pitch under the seam.",
     lambda: render_moves(cursor=1, mode="select")),
    ("state_05.png", "Learn a move: forget which?", "Header shows the prompt (tabs and chevrons hidden), B CANCEL hint. The new move is a 5th pill with a brass NEW notch; the cursor's move is described in the tray.",
     lambda: render_moves(S.hero().copy(lv=29), cursor=1, mode="learn", new_move="leaf_blade")),
    ("state_06.png", "Swapping two moves", "Picked-up move keeps the party's moving look (accent face, accent outline); the gold cursor marks the destination.",
     lambda: render_moves(cursor=3, mode="swap", moving=0)),
    ("state_07.png", "Female theme, paralysed", "Female player's rose theme; female Kirlia's name in rose; paralysis tag in the status socket; OT MAY in rose; dual type icons.",
     lambda: render_info(S.heroine_mon(), "female")),
    ("state_08.png", "Egg", "Eggs only get the INFO tab: no chevrons, no Lv / No. / item; EGG WATCH and MEMO drawers.",
     lambda: render_egg()),
    ("state_09.png", "SKILLS: IV view", "A on SKILLS cycles STATS -> IVs -> EVs (config). The tab reads IVs, values are numbers (P_SUMMARY_SCREEN_IV_EV_VALUES) with a gold 0-31 bar.",
     lambda: render_skills(skills_mode="ivs")),
]


# ================================================================== review sheets
def _caption(img, x, y, text, k):
    d = ImageDraw.Draw(img)
    d.text((x * k, y * k - 12), text, fill=(230, 230, 240))


def parts_sheet(k=4):
    """New pieces at 4x, cropped from real renders (so they are exactly what ships)."""
    info = render_info()
    fem = render_info(S.heroine_mon(), "female")
    skills = render_skills()
    sel = render_moves(cursor=1, mode="select")
    swap = render_moves(cursor=3, mode="swap", moving=0)
    learn = render_moves(S.hero().copy(lv=29), cursor=1, mode="learn", new_move="leaf_blade")
    varc = render_skills(style="C")
    cw, ch = 330, 300
    can = Image.new("RGBA", (cw, ch), (24, 24, 32, 255))
    pieces = [
        (info.crop((0, 0, 125, 20)), 4, 14, "B: stepped tabs, brass trim (hero)"),
        (varc.crop((30, 0, 210, 20)), 140, 14, "C: icon tabs, selected widens"),
        (fem.crop((0, 20, 90, 102)), 4, 46, "dais + ball / status sockets"),
        (fem.crop((0, 102, 90, 160)), 4, 140, "name, No., held-item row"),
        (skills.crop((92, 20, 238, 50)), 100, 46, "HP pill (Gen 3 bar) / nature up"),
        (skills.crop((92, 65, 238, 80)), 100, 90, "nature down"),
        (skills.crop((92, 113, 238, 160)), 100, 110, "EXP / NEXT + A hint"),
        (sel.crop((92, 20, 238, 60)), 100, 172, "move pill / gold cursor"),
        (swap.crop((92, 20, 238, 40)), 100, 226, "moving (swap)"),
        (learn.crop((92, 100, 238, 120)), 100, 260, "new move: brass NEW notch"),
        (sel.crop((0, 118, 90, 160)), 4, 210, "detail tray (left half)"),
    ]
    for im, x, y, cap in pieces:
        can.alpha_composite(im, (x, y))
    # category tags: Orchid vs expansion's own
    x0, y0 = 4, 266
    for i, kind in enumerate(("physical", "special", "status")):
        can.alpha_composite(S.cat_icon(kind), (x0 + i * 20, y0))
        can.alpha_composite(S.rom_cat_icon(kind), (x0 + i * 20, y0 + 18))
    big = KX.upscale(can, k)
    for im, x, y, cap in pieces:
        _caption(big, x, y, cap, k)
    _caption(big, x0, y0, "category tags: Orchid (top) / expansion ROM (bottom)", k)
    return big


def variants_sheet():
    out = Image.new("RGB", (W * 2 * 3 + 32, H * 2 + 30), (16, 16, 20))
    d = ImageDraw.Draw(out)
    for i, (st, lab) in enumerate((("A", "A  flat dex pills"), ("B", "B  stepped brass tabs (chosen)"),
                                   ("C", "C  icon tabs, selected widens"))):
        im = render_skills(style=st)
        out.paste(KX.upscale(im.convert("RGB"), 2), (8 + i * (W * 2 + 8), 24))
        d.text((8 + i * (W * 2 + 8), 6), lab, fill=(230, 230, 240))
    return out


# ================================================================== budget
def _merge(*ims):
    out = ims[0].copy()
    px = out.load()
    for im in ims[1:]:
        q = im.load()
        for y in range(H):
            for x in range(W):
                if q[x, y]:
                    px[x, y] = q[x, y]
    return out


def budget_lines():
    mon = S.hero()
    # BG1: header (4 selected positions + learn prompt band) + left column + tray
    tiles = None
    for p in range(len(TABS)):
        im = sheet("male")
        cv = Canvas(im)
        draw_header(cv, p)
        draw_left(cv, mon)
        tiles, _ = to_tiles(im, base=tiles)
    n_static = len(tiles)
    im = sheet("male")
    cv = Canvas(im)
    draw_header(cv, 2, learn=True)
    draw_left(cv, mon)
    S.move_tray(cv, TRAY_Y)
    tiles, _ = to_tiles(im, base=tiles)
    n_static_all = len(tiles)
    # BG2: each page's art (normal + gold + moving cells share tiles; palette swap only)
    per, union = [], None
    for p, kw in ((0, {}), (1, {}), (1, dict(skills_mode="ivs")), (2, dict(cursor=1, mode="select")),
                  (2, dict(cursor=1, mode="learn", new_move="leaf_blade"))):
        pg = build_page(p, mon, "male", **kw)
        im = _merge(pg.art, pg.sel, pg.mov)
        t, _ = to_tiles(im)
        union, _ = to_tiles(im, base=union)
        per.append((["INFO", "SKILLS", "SKILLS-IV", "MOVES", "MOVES-learn"][len(per)], len(t)))
    egg = build_page(0, S.egg_mon(), "male")
    t, _ = to_tiles(_merge(egg.art, egg.sel, egg.mov))
    union, _ = to_tiles(_merge(egg.art, egg.sel, egg.mov), base=union)
    per.append(("EGG", len(t)))
    return [
        "BG3: BW grid, 2x2 tiles + 32x32 map, own palette (as bag / party / dex).",
        "BG1 static art (header with the 3 tab positions + left column): %d unique tiles; +learn "
        "band + detail tray = %d." % (n_static, n_static_all),
        "BG2 page art per page: " + ", ".join("%s %d" % p for p in per) +
        " — all pages together %d tiles (one tilemap per page, like vanilla, which keeps one per page). "
        "BG1 + BG2 fit one 512-tile charblock." % len(union),
        "BG0 text windows: tab labels 30x2, name/Lv 11x2, No. 11x2, item 9x2, right page as per-row "
        "windows (about 8 rows x 18x2 = 288), tray 30x5 — about 440 tiles worst case, under one 512-tile "
        "charblock (one 18x17 block would be 578, too many). HP/EXP bars add ~14 BG2 tiles.",
        "BG palettes (7): 0 art (kit roles, gender theme, SPARE_A = ball red), 1 gold cells (tab, cursor pill), "
        "2 moving pill, 3 text (gender / nature colours in the spare + accent-light/pale slots), 4 move text "
        "(battle PP colours), 5 HP/EXP bars (battle healthbar palette), 6 grid.",
        "OBJ: front pic 64x64, ball 16x16, status tag 16x16 (STATUS_PAL), item icon 32x32, type icons 32x16 "
        "(up to 5 on the learn page), category tag 16x16 (CAT_PAL), 2 red chevrons — max 11 OBJs.",
        "OBJ palettes: pic, ball, item, status, category, chevron red + vanilla type-icon palettes (3) = 9/16.",
        "Page switch: BG2 HOFS slide + WIN0 (x 90..239 shows BG2) so BG1 / OBJ left column never moves.",
    ]


def notes():
    st = [{"file": fn, "title": t, "desc": d} for fn, t, d, _ in STATES]
    return {
        "title": "Pokémon summary screen",
        "main": {"file": "main.png", "zones": [
            ["Stepped tab header", "Gender-theme band with a brass trim; three roomy INFO / SKILLS / MOVES tabs rise from the trim, the selected one is gold and steps down through it. Red Gen 3 chevrons at the ends."],
            ["Dais + sockets", "The Pokémon's real front pic on the dex dais; two studs on the rim hold the caught Poké Ball (ROM ball sprite) and the status tag (empty = plain recess)."],
            ["Left column", "Name in the gender colour (no glyph) with Lv, a No. label pill, and the held item in a party-row style disc + slab. Identical on every page."],
            ["Stat pills", "Label pills (dex HT/WT build). HP carries the Gen 3 HP bar; the nature's boosted stat is rose with an up mark, the lowered one blue with a down mark."],
            ["EXP block", "Total EXP, then NEXT with the Gen 3 EXP-blue bar and the points still needed."],
            ["Button hint", "Dark hint pill with the ROM's own keypad glyph: A cycles STATS / IVs / EVs (config)."],
        ]},
        "states": st,
        "gifs": [{"file": "page_switch.gif", "title": "Page switch",
                  "desc": "→ ×2 then ← ×2 (INFO / SKILLS / MOVES). The gold tab moves on the press; page text clears; the page art slides 148px in 12 frames (ease-out) under a WIN0 clip at x 90, so the Pokémon and left column never move; text returns when it lands. Grid scrolls 1px / 4 frames."}],
        "extras": [
            {"file": "parts.png", "title": "New pieces (4x)", "desc": "Tabs (B and C), dais sockets, left column rows, stat pills (bar, nature marks), move pill states, NEW notch, detail tray, category tags vs the expansion's own icons."},
            {"file": "variants.png", "title": "Tab header A / B / C", "desc": "A = the dex's flat tab pills; B = stepped brass folder tabs (chosen); C = icon tabs where only the selected tab shows its label. All shown with the 3 tabs left once the contest page is hidden."},
        ],
        "budget": budget_lines(),
        "kit_additions": [
            "summary_ext.tab_strip(style B): stepped folder tabs on a brass-trimmed band — reusable for any paged player screen (trainer card, PC box summary).",
            "summary_ext.socket(): recessed stud on a dais rim for 16x16 OBJs (ball, status).",
            "summary_ext.item_row(): party-row disc + slab for a 24x24 item icon with a name.",
            "summary_ext.notch() + _new_flag: dark bottom notch (PP / numbers) and its brass top-edge mirror (NEW).",
            "summary_ext.hint_tab() / keypad(): button hint pill that blits the ROM's keypad_icons.png glyphs (A, B, START).",
            "summary_ext category tags (CAT_PAL, cat_icon): physical / special / status in the status_icons.py tag build.",
            "summary_ext.move_tray(): bag-style tray with a round well + stitched divider, for any detail readout.",
        ],
        "questions": [],
    }


def main_all(out):
    os.makedirs(out, exist_ok=True)
    for fn, title, desc, f in STATES:
        save(f(), os.path.join(out, fn))
    save(render_skills(), os.path.join(out, "main.png"))
    parts_sheet().convert("RGB").save(os.path.join(out, "parts.png"))
    variants_sheet().save(os.path.join(out, "variants.png"))
    with open(os.path.join(out, "notes.json"), "w") as f:
        json.dump(notes(), f, indent=1, ensure_ascii=False)
    print("\n".join(budget_lines()))


if __name__ == "__main__":
    out = sys.argv[1]
    only = sys.argv[2:]
    if only:
        for fn, title, desc, f in STATES:
            if fn in only:
                save(f(), os.path.join(out, fn))
    else:
        main_all(out)
