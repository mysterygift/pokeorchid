"""
Pixel-accurate mockups of the Orchid party menu ("Gen 5 layout, Gen 3 pixels").

Layers composited bottom-up like the GBA: BG3 grid -> BG1 CANCEL art -> BG0 slot windows
(art + text, one palette per slot) -> OBJ (mon icons, hold icons, status tags) -> BG2 popups.

usage: mock_party.py OUT_DIR
"""
import json
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as KX
import windows as Wn
import party_ext as P
from gamefont import draw_text, text_width

# ---------------------------------------------------------------- example party (real species)
GROVYLE = dict(species="grovyle", pal=1, name="Grovyle", sex="m", lv=18, hp=52, maxhp=52, item="item")
TAILLOW = dict(species="taillow", pal=2, name="Taillow", sex="f", lv=12, hp=29, maxhp=35, status="psn")
RALTS = dict(species="ralts", pal=1, name="Ralts", sex="f", lv=10, hp=24, maxhp=29)
ZIGZAGOON = dict(species="zigzagoon", pal=2, name="Zigzagoon", sex="m", lv=9, hp=5, maxhp=31)
POOCHYENA = dict(species="poochyena", pal=2, name="Poochyena", sex="m", lv=8, hp=0, maxhp=27, status="fnt")
WINGULL = dict(species="wingull", pal=0, name="Wingull", sex="f", lv=11, hp=30, maxhp=31, item="mail")
PARTY5 = [GROVYLE, TAILLOW, RALTS, ZIGZAGOON, POOCHYENA, None]
PARTY6 = [GROVYLE, TAILLOW, RALTS, ZIGZAGOON, POOCHYENA, WINGULL]
CANCEL = 6


def anim_period(m):
    """sMonIconAnims speed by HP bar level (frame duration + 1 GBA frames)."""
    if m["hp"] == 0:
        return None
    f = m["hp"] / m["maxhp"]
    return 7 if f == 1 else 9 if f > 0.5 else 15 if f > 0.2 else 23


def slot_state(i, m, cursor, moving):
    fainted = m["hp"] == 0
    sel = i == cursor
    if moving is not None and i == moving:
        return "moving_sel" if sel else "moving"
    if fainted:
        return "fainted_sel" if sel else "fainted"
    return "selected" if sel else "normal"


# ---------------------------------------------------------------- popups (BG2, shared -> orchid theme)
def message(text, win=P.MSG_WIN):
    def fn(cv):
        tx, ty, tw, th = win
        Wn.std_frame(cv, tx, ty, tw, th)
        draw_text(cv, tx * 8, ty * 8 + 1, text, INK, PANEL_SHADE)
    return fn


ACTION_WIN = (21, 9, 8, 10)          # DisplaySelectionWindow(SELECTWINDOW_ACTIONS): was (19, 9, 10, 2n)


def action_menu(entries, cursor, field=1):
    """field = number of leading field-move entries (drawn in the accent like Gen 3's blue)."""
    def fn(cv):
        tx, _, tw, _ = ACTION_WIN
        ty = 19 - 2 * len(entries)
        Wn.std_frame(cv, tx, ty, tw, 2 * len(entries))
        for i, e in enumerate(entries):
            y = ty * 8 + i * 16
            if i == cursor:
                Wn.selection_bar(cv, tx * 8 + 2, y + 1, tw * 8 - 4, 14)
            fg, sh = (ACCENT_DARK, ACCENT_LIGHT) if i < field else (INK, PANEL_SHADE)
            if i == cursor and i < field:
                sh = SELECT_DARK
            draw_text(cv, tx * 8 + 6, y, e, fg, sh)
    return fn


# ---------------------------------------------------------------- frame renderer
def render(theme="male", party=PARTY5, cursor=0, moving=None, popups=(), grid_scroll=0, t=0,
           slide=None, mode="hp", able=None, hide=(), sel_t=None):
    """
    cursor: 0..5 slot, 6 = CANCEL, None = no cursor.  moving: slot being switched.
    slide: {slot: dx_px} (switch animation, whole tiles).  t: GBA frame for icon anim/bounce.
    mode: 'hp' or 'tm' (ABLE / NOT ABLE tags; able = list of bools).  hide: slots drawn empty.
    """
    slide = slide or {}
    out = KX.grid_frame(grid_scroll)

    # BG1: CANCEL button art (+ its BG0 label; same palette swap)
    cpal = palette(theme)
    if cursor == CANCEL:
        cpal = P.slot_palette(theme, "selected")
    cx, cy, _, _ = P.CANCEL_WIN
    P.composite_sheet(out, P.cancel_sheet(theme), cpal, (cx * 8, cy * 8))

    # BG0: slot windows
    sprites = []
    for i, m in enumerate(party):
        if m is None or i in hide:
            continue                      # empty slot: window cleared -> backdrop shows
        wx, wy, ww, wh = P.slot_px(i)
        wx += slide.get(i, 0)
        lead = i == 0
        md = "hp" if mode == "hp" else ("able" if able[i] else "notable")
        im = P.slot_sheet(theme, m, lead, md)
        pal = P.slot_palette(theme, slot_state(i, m, cursor, moving), m.get("sex"), m["hp"] / m["maxhp"])
        P.safe_comp(out, KX.sheet_rgba(im, pal), wx, wy)
        sprites.append((i, m, wx, wy, lead))

    # OBJ: icons, hold icons, status tags
    for i, m, wx, wy, lead in sprites:
        g = P.LEAD if lead else P.WIDE
        per = anim_period(m)
        tt = sel_t if (i == cursor and sel_t is not None) else t
        frame = 0 if per is None else (tt // per) % 2
        dy = 0
        if i == cursor and per is not None:
            dy = -3 if frame == 0 else 1          # SpriteCB_BouncePartyMonIcon
        icx, icy = g["icon"]
        P.safe_comp(out, P.mon_icon(m["species"], frame, m["pal"]), wx + icx - 16, wy + icy - 16 + dy)
        if m.get("item"):
            hx, hy = g["hold"]
            P.safe_comp(out, P.hold_icon(m["item"] == "mail"), wx + hx - 4, wy + hy - 4 + dy)
        if m.get("status") and mode == "hp":
            sx, sy = g["status"]
            P.safe_comp(out, P.status_icon(m["status"]), wx + sx, wy + sy)

    # BG2: popups (orchid)
    for fn in popups:
        KX.layer(out, fn, "orchid")
    return out


def save3(im, path):
    KX.upscale(im, 3).save(path)


# ---------------------------------------------------------------- states
def states():
    S = []
    choose = message("Choose a POKéMON.")
    S.append(("Main — cursor on the lead (male)",
              "Lead slot is gold (palette swap of its window); Grovyle bobs. Empty 6th slot shows the grid.",
              render("male", PARTY5, cursor=0, popups=[choose], t=0)))
    S.append(("Cursor on a right-column slot (female)",
              "Same tiles, female palette. Ralts' slot goes gold; PSN tag, red HP bar and the fainted slot are all visible.",
              render("female", PARTY6, cursor=2, popups=[choose], t=0, grid_scroll=5)))
    S.append(("Cursor on CANCEL",
              "CANCEL is a pill on BG1 that turns gold like a slot; no Poké Ball sprite.",
              render("male", PARTY5, cursor=CANCEL, popups=[choose], t=7, grid_scroll=9)))
    acts = ["CUT", "SUMMARY", "SWITCH", "ITEM", "CANCEL"]
    S.append(("Action popup",
              "Std Orchid frame, 8 tiles wide; field move CUT in the accent colour at the top, gold pill on SUMMARY.",
              render("male", PARTY5, cursor=0, t=0,
                     popups=[message("Do what with this Grovyle?", P.DOWHAT_WIN), action_menu(acts, 1)])))
    S.append(("Switch mode — Move to where?",
              "Grovyle's slot is 'picked up' (accent face + accent outline); the gold cursor is on the target, Ralts.",
              render("female", PARTY5, cursor=2, moving=0, t=7, popups=[message("Move to where?")])))
    S.append(("Fainted, status and low HP together",
              "Poochyena: rose face, grey dais, FNT tag, still icon. Taillow: PSN tag. Zigzagoon: red HP. Cursor on the fainted slot.",
              render("male", PARTY6, cursor=4, popups=[choose], t=0, grid_scroll=3)))
    able = [True, True, False, True, False, True]
    S.append(("Use on which POKéMON? (TM teach)",
              "HP row is replaced by an ABLE (accent) / NOT ABLE (grey) tag; status tags hide in this mode like vanilla.",
              render("female", PARTY6, cursor=1, mode="tm", able=able,
                     popups=[message("Teach which POKéMON?")], t=0)))
    return S


# ---------------------------------------------------------------- parts sheet (4x)
def parts_sheet(out_path):
    themes = ["male", "female"]
    rows = [("normal", GROVYLE), ("selected", GROVYLE), ("moving", GROVYLE), ("moving_sel", GROVYLE),
            ("fainted", POOCHYENA), ("fainted_sel", POOCHYENA)]
    k = 4
    pad = 8
    cellw, cellh = 144 + 80 + 3 * pad, 56
    sheet = Image.new("RGBA", ((cellw * len(themes) + pad) * k, (len(rows) * (cellh + 14) + 40) * k), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    for ti, th in enumerate(themes):
        for ri, (st, m) in enumerate(rows):
            x0, y0 = ti * cellw + pad, 24 + ri * (cellh + 14)
            frame = KX.grid_frame(0, cellw - pad, cellh)
            pal = P.slot_palette(th, st, m["sex"], m["hp"] / m["maxhp"])
            P.composite_sheet(frame, P.slot_sheet(th, m, True), pal, (0, 0))
            P.composite_sheet(frame, P.slot_sheet(th, m, False), pal, (80 + pad, 16))
            for (wx, wy, lead) in ((0, 0, True), (80 + pad, 16, False)):
                g = P.LEAD if lead else P.WIDE
                frame.alpha_composite(P.mon_icon(m["species"], 0, m["pal"]), (wx + g["icon"][0] - 16, wy + g["icon"][1] - 16))
                if m.get("item"):
                    frame.alpha_composite(P.hold_icon(), (wx + g["hold"][0] - 4, wy + g["hold"][1] - 4))
                if m.get("status"):
                    frame.alpha_composite(P.status_icon(m["status"]), (wx + g["status"][0], wy + g["status"][1]))
            sheet.paste(KX.upscale(frame, k), (x0 * k, y0 * k))
            d.text((x0 * k, (y0 - 10) * k + 8), "%s - %s" % (th, st), fill=(230, 230, 240))
            # palette strip
            for ci, c in enumerate(pal):
                xx = (x0 + 80 + pad) * k + ci * 22
                d.rectangle((xx, (y0 + 44) * k, xx + 20, (y0 + 44) * k + 20), fill=c)
    d.text((pad * k, 8), "Party slot parts (4x): one set of tiles per slot shape, states are palette swaps "
           "(LoadPartyBoxPalette). Palette strip = slot palette 0..15 (11 gender, 14/15 HP ramp).", fill=(230, 230, 240))
    sheet.save(out_path)


# ---------------------------------------------------------------- A/B layout sheet
def render_bw(theme="male", party=PARTY6, cursor=0, t=0):
    """Alt layout: 2 columns x 3 equal 15x5-tile slots (BW). Message + CANCEL keep their rows."""
    out = KX.grid_frame(0)
    P.composite_sheet(out, P.cancel_sheet(theme), P.slot_palette(theme, "selected") if cursor == CANCEL else palette(theme), (192, 136))
    BW = dict(disc=(16, 19.5, 13.0), slab=(9, 3, 110, 35),
              name=(32, 2), lv=(32, 12), sex_x=60, status=(82, 6),
              hp_tag=(32, 27), bar=(44, 28, 48), hpnum_r=114, hpnum_y=16,
              icon=(16, 15), hold=(24, 27))
    old = P.WIDE
    sprites = []
    for i, m in enumerate(party):
        if m is None:
            continue
        col, row = i % 2, i // 2
        wx, wy = 0 + col * 120, 0 + row * 40 + 4
        im = new_sheet(120, 40, theme)
        P.WIDE = BW
        P.draw_slot(Canvas(im), m, False)
        P.WIDE = old
        pal = P.slot_palette(theme, slot_state(i, m, cursor, None), m.get("sex"), m["hp"] / m["maxhp"])
        P.composite_sheet(out, im, pal, (wx, wy))
        sprites.append((i, m, wx, wy))
    for i, m, wx, wy in sprites:
        per = anim_period(m)
        dy = -3 if (i == cursor and per) else 0
        out.alpha_composite(P.mon_icon(m["species"], 0, m["pal"]), (wx + BW["icon"][0] - 16, wy + BW["icon"][1] - 16 + dy))
        if m.get("item"):
            out.alpha_composite(P.hold_icon(m["item"] == "mail"), (wx + BW["hold"][0] - 4, wy + BW["hold"][1] - 4 + dy))
        if m.get("status"):
            out.alpha_composite(P.status_icon(m["status"]), (wx + BW["status"][0], wy + BW["status"][1]))
    KX.layer(out, message("Choose a POKéMON."), "orchid")
    return out


def ab_sheet(out_path):
    a = render("male", PARTY6, cursor=0, popups=[message("Choose a POKéMON.")])
    b = render_bw("male", PARTY6, cursor=0)
    k = 3
    sheet = Image.new("RGBA", (240 * k * 2 + 72, 160 * k + 60), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    d.text((24, 12), "A - Gen 3 structure (lead panel + 5 rows), Orchid slabs. Recommended: drop-in for party_menu.c.", fill=(230, 230, 240))
    d.text((240 * k + 48, 12), "B - BW structure: 2 columns x 3 equal slots (15x5 tiles each).", fill=(230, 230, 240))
    sheet.paste(KX.upscale(a, k), (24, 40))
    sheet.paste(KX.upscale(b, k), (240 * k + 48, 40))
    sheet.save(out_path)
    return a, b


# ---------------------------------------------------------------- budget
def budget():
    # unique tiles of the slot art the GBA would store (one copy per shape, text excluded)
    blankmon = dict(name="", sex=None, lv="", hp=1, maxhp=1)
    lines = []
    lead_t, _ = to_tiles(_art_only(True))
    wide_t, _ = to_tiles(_art_only(False))
    can_t, _ = to_tiles(_cancel_art())
    lines.append("Slot art source tiles: lead %d + wide %d + CANCEL %d (incl. blank) — vs 62 in vanilla bg.png" %
                 (len(lead_t), len(wide_t), len(can_t)))
    return lines


def _art_only(lead):
    w, h = (80, 56) if lead else (144, 24)
    im = new_sheet(w, h, "male")
    cv = Canvas(im)
    g = P.LEAD if lead else P.WIDE
    sx, sy, sw, sh = g["slab"]
    rounded_box(cv, sx, sy, sw, sh, 4, PANEL, INK, WHITE, PANEL_SHADE)
    P._dais(cv, g)
    P.hp_tag(cv, *g["hp_tag"])
    return im


def _cancel_art():
    im = new_sheet(48, 16, "male")
    rounded_box(Canvas(im), 1, 1, 46, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    return im


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    S = states()
    for n, (title, desc, im) in enumerate(S, 1):
        save3(im, os.path.join(out, "state_%02d.png" % n))
    save3(S[0][2], os.path.join(out, "main.png"))
    parts_sheet(os.path.join(out, "parts.png"))
    ab_sheet(os.path.join(out, "extra_layout_ab.png"))
    for l in budget():
        print(l)
    print("ok", len(S))
