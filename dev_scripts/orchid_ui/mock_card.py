"""
Pixel-accurate mockups of the Orchid Trainer Card ("Gen 5 layout, Gen 3 pixels").

Layers (bottom-up, like the GBA; matches trainer_card.c's BG use):
    BG2  scrolling BW grid (own palette) - replaces vanilla's bg.bin screen
    BG0  card art: band + header tab + pills + dais + badge case (front.bin / back.bin)
    BG3  badges (badges.png, own palette) + trainer pic window (front pic palette)
    BG1  text window over the whole card (card palette)
    OBJ  none
Tier (0-4 stars) = 3 palette colours (METAL ramp) + lit star pips; gender = accent
theme + name colour. Both are palette-only, so front/back tiles are shared.

usage: mock_card.py OUT_DIR
"""
import os
import sys
import json
from PIL import Image, ImageDraw
from kit import *
import kit_ext as KX
import card_ext as C
from card_ext import METAL_DARK, METAL, METAL_LIGHT, NAME_FG, NAME_SH
from gamefont import draw_text, text_width
from backdrop import GRID_PAL

W, H = 240, 160

# ------------------------------------------------------------------ layout
CARD = (8, 8, 224, 144)            # x, y, w, h  (1-tile margin of grid all round)
HEAD_H = 22                        # accent header strip; face ink line at y 30
TAB = (13, 11, 138, 17)            # stepped title tab
TITLE = (19, 11)
PIPS_X, PIPS_Y, PIP_PITCH = 93, 14, 12
ID_PILL = (153, 13, 69, 30)        # x, y, w, cap
COL_X, COL_W = 19, 116
NAME_Y = 35
ROWS_Y = (54, 72, 90)
ROW_H = 16
DAIS_C, DAIS_R, DAIS_IN = (183, 71), 38, 30
CASE = (19, 113, 202, 28)
SOCK_Y, SOCK_X0, SOCK_PITCH = 127, 32, 25
BACK_ROWS_Y0, BACK_PITCH, BACK_ROW_H = 33, 16, 15
SIG = (19, 130, 202, 16)

# ------------------------------------------------------------------ sample save data
HERO = dict(gender="male", name="KAITO", id=48213, money=12480, dex=41, has_dex=True,
            time=(12, 34), badges=4, stars=0,
            hof=None, link=(12, 5), trades=8, union=23, berry=1250, contests=3)
HEROINE = dict(HERO, gender="female", name="HANA", id=30571, money=9875, dex=37, time=(10, 2), badges=3)
CHAMP = dict(HERO, money=999999, dex=202, time=(87, 15), badges=8, stars=4, hof=(31, 9, 46))
FRESH = dict(HERO, money=3000, dex=0, has_dex=False, time=(0, 12), badges=0, stars=0,
             link=None, trades=0, union=0, berry=0, contests=0)


def theme_of(d):
    return d["gender"]


# ------------------------------------------------------------------ art (BG0)
def draw_header(cv, stars):
    C.header_tab(cv, *TAB)
    for k in range(4):
        C.star_pip(cv, PIPS_X + k * PIP_PITCH, PIPS_Y, k < stars)
    x, y, w, cap = ID_PILL
    C.label_cap_pill(cv, x, y, w, cap, 14, cap=(ACCENT_DARK, ACCENT, INK))


def draw_front_art(cv, d):
    C.card_shell(cv, *CARD, HEAD_H)
    draw_header(cv, d["stars"])
    # name plate: inset pill with metal rivets at each end
    C.nameplate(cv, COL_X + 2, NAME_Y, COL_W - 4, ROW_H)
    rows = ["money", "dex", "time"] if d["has_dex"] else ["money", "time"]
    for name, y in zip(rows, ROWS_Y):
        C.icon_pill(cv, COL_X, y, COL_W, name, 20, ROW_H)
    C.dais(cv, DAIS_C[0], DAIS_C[1], DAIS_R, DAIS_IN)
    x, y, w, h = CASE
    C.badge_case(cv, x, y, w, h)
    for k in range(8):
        C.socket(cv, SOCK_X0 + k * SOCK_PITCH, SOCK_Y, k < d["badges"])


def back_rows(d):
    rows = []
    if d.get("hof"):
        h, m, s = d["hof"]
        rows.append(("hof", "HALL OF FAME DEBUT", "%d:%02d:%02d" % (h, m, s)))
    if d.get("link"):
        rows.append(("link", "LINK BATTLES", "W:%d  L:%d" % d["link"]))
    if d.get("trades"):
        rows.append(("trade", "POKéMON TRADES", str(d["trades"])))
    if d.get("union"):
        rows.append(("union", "UNION ROOM", str(d["union"])))
    if d.get("berry"):
        rows.append(("berry", "BERRY CRUSH", str(d["berry"])))
    if d.get("contests"):
        rows.append(("contest", "CONTESTS W/FRIENDS", str(d["contests"])))
    return rows


def draw_back_art(cv, d):
    C.card_shell(cv, *CARD, HEAD_H)
    draw_header(cv, d["stars"])
    for k, (ic, _, _) in enumerate(back_rows(d)):
        C.icon_pill(cv, COL_X, BACK_ROWS_Y0 + k * BACK_PITCH, SIG[2], ic, 20, BACK_ROW_H)
    x, y, w, h = SIG
    C.sig_well(cv, x, y, w, h)
    C.icon(cv, x + 6, y + 3, "pen", INK_SOFT, PANEL_SHADE)


# ------------------------------------------------------------------ text (BG1)
def draw_header_text(tc, d):
    draw_text(tc, TITLE[0], TITLE[1], "TRAINER CARD", WHITE, INK)
    x, y, w, cap = ID_PILL
    draw_text(tc, x + (cap - text_width("IDNo.")) // 2 + 1, y - 1, "IDNo.", WHITE, INK)
    s = "%05d" % d["id"]
    draw_text(tc, x + cap + (w - cap - text_width(s)) // 2, y - 1, s, INK, PANEL_SHADE)


def draw_front_text(tc, d, colon=True):
    draw_header_text(tc, d)
    draw_text(tc, COL_X + (COL_W - text_width(d["name"])) // 2, NAME_Y, d["name"], NAME_FG, NAME_SH)
    h, m = d["time"]
    vals = ["¥%d" % d["money"]]
    if d["has_dex"]:
        vals.append(str(d["dex"]))
    vals.append(None)
    for v, y in zip(vals, ROWS_Y):
        xr = COL_X + COL_W - 7
        if v is None:   # TIME: colon blinks every 61 frames (BlinkTimeColon) - keep fixed width
            hs, ms = "%d" % h, "%02d" % m
            x = xr - text_width(hs + ":" + ms)
            x = draw_text(tc, x, y, hs, INK, PANEL_SHADE)
            if colon:
                draw_text(tc, x, y, ":", INK, PANEL_SHADE)
            draw_text(tc, x + text_width(":"), y, ms, INK, PANEL_SHADE)
        else:
            draw_text(tc, xr - text_width(v), y, v, INK, PANEL_SHADE)


def draw_back_text(tc, d):
    draw_header_text(tc, d)
    for k, (_, label, val) in enumerate(back_rows(d)):
        y = BACK_ROWS_Y0 + k * BACK_PITCH - 1
        draw_text(tc, COL_X + 25, y, label, INK, PANEL_SHADE)
        draw_text(tc, COL_X + SIG[2] - 7 - text_width(val), y, val, INK, PANEL_SHADE)
    x, y, w, h = SIG
    draw_text(tc, x + 26, y - 1, d["name"], NAME_FG, NAME_SH)


# ------------------------------------------------------------------ compositing
def card_layers(d, side="front", colon=True, tier=None):
    """All card layers (BG0 art, BG3 badges + pic, BG1 text) as one RGBA, transparent outside."""
    theme = theme_of(d)
    tier = d["stars"] if tier is None else tier
    pal = C.card_palette(theme, tier)
    out = KX.blank()
    art = C.card_sheet(W, H, theme, tier)
    (draw_front_art if side == "front" else draw_back_art)(Canvas(art), d)
    out.alpha_composite(KX.sheet_rgba(art, pal))
    if side == "front":
        for k in range(d["badges"]):
            cx = SOCK_X0 + k * SOCK_PITCH
            out.alpha_composite(C.badge_rgba(k), (cx - 8, SOCK_Y - 8))
        pic, _ = C.trainer_pic(d["gender"])
        stage = DAIS_C[1] + int(DAIS_IN * 0.55)
        bb = pic.getbbox()
        out.alpha_composite(pic, (DAIS_C[0] - 32, stage + 3 - bb[3]))
    txt = C.card_sheet(W, H, theme, tier)
    (draw_front_text(Canvas(txt), d, colon) if side == "front" else draw_back_text(Canvas(txt), d))
    out.alpha_composite(KX.sheet_rgba(txt, pal))
    return out


def render(d, side="front", grid_scroll=0, colon=True, card_top=0, down=True):
    out = KX.grid_frame(grid_scroll)
    card = card_layers(d, side, colon)
    if card_top:
        card = C.darken(C.squash(card, card_top, down), C.blend_y(card_top))
    out.alpha_composite(card)
    return out


def render_front(d=HERO, **kw):
    return render(d, "front", **kw)


def render_back(d=HERO, **kw):
    return render(d, "back", **kw)


# ------------------------------------------------------------------ parts sheet (4x)
def parts_sheet():
    cw, ch = 300, 130
    out = KX.grid_frame(0, cw, ch)
    lab = []

    def put(fn, x, y, theme="male", tier=0, size=None):
        im = C.card_sheet(cw, ch, theme, tier)
        fn(Canvas(im))
        out.alpha_composite(KX.sheet_rgba(im, C.card_palette(theme, tier)))

    # header tab with pips, tiers 0..4 stacked (palette swap only)
    for t in range(5):
        y = 4 + t * 20

        def f(cv, t=t, y=y):
            cv.rect(2, y - 2, 145, y + 18, ACCENT)
            C.header_tab(cv, 4, y, TAB[2], 17)
            for k in range(4):
                C.star_pip(cv, PIPS_X - TAB[0] + 4 + k * PIP_PITCH, y + 3, k < t)
            draw_text(cv, 10, y, "TRAINER CARD", WHITE, INK)
        put(f, 0, 0, tier=t)

    # sockets: empty / earned per tier
    def g(cv):
        for t in range(2):
            C.socket(cv, 160 + t * 26, 16, t == 1)
    put(g, 0, 0)
    # one earned socket in each tier on a row
    for t in range(5):
        put(lambda cv, t=t: C.socket(cv, 160 + t * 26, 44, True), 0, 0, tier=t)
    out.alpha_composite(C.badge_rgba(0), (186 - 8, 16 - 8))
    for t in range(5):
        out.alpha_composite(C.badge_rgba(t + 1), (160 + t * 26 - 8, 44 - 8))

    # icon pills
    names = ["money", "dex", "time", "hof", "link", "trade", "union", "berry", "contest"]

    def p(cv):
        for k, n in enumerate(names):
            x, y = 150 + (k % 3) * 50, 62 + (k // 3) * 20
            C.icon_pill(cv, x, y, 46, n, 20, 16)
        C.sig_well(cv, 4, 108, 140, 16)
        C.icon(cv, 10, 111, "pen", INK_SOFT, PANEL_SHADE)
        draw_text(cv, 30, 107, "KAITO", NAME_FG, NAME_SH)
    put(p, 0, 0)
    big = KX.upscale(out, 4)
    # palette strips: card pal per tier (male), female, badges, grid
    sw = 22
    pals = [C.card_palette("male", t) for t in range(5)] + [C.card_palette("female", 0)]
    bim = Image.open(KX.G("trainer_card", "badges.png"))
    pals.append([snap(tuple(bim.getpalette()[k * 3:k * 3 + 3])) for k in range(16)])
    pals.append(C.trainer_pic("male")[1])
    pals.append(list(GRID_PAL) + [(0, 0, 0)] * 12)
    strip = Image.new("RGBA", (big.size[0], len(pals) * (sw + 4) + 8), (24, 24, 32, 255))
    dr = ImageDraw.Draw(strip)
    for r, pl in enumerate(pals):
        for i, col in enumerate(pl[:16]):
            x, y = 6 + i * (sw + 4), 6 + r * (sw + 4)
            dr.rectangle((x, y, x + sw - 1, y + sw - 1), fill=tuple(col) + (255,),
                         outline=(255, 255, 255, 255) if i == 0 else None)
    full = Image.new("RGBA", (big.size[0], big.size[1] + strip.size[1]))
    full.paste(big, (0, 0))
    full.paste(strip, (0, big.size[1]))
    return full


# ------------------------------------------------------------------ budget
def budget():
    fr = C.card_sheet(W, H)
    draw_front_art(Canvas(fr), HERO)
    t_front, _ = to_tiles(fr)
    bk = C.card_sheet(W, H)
    draw_back_art(Canvas(bk), dict(CHAMP))
    t_both, _ = to_tiles(bk, base=t_front)
    # empty-socket variants used by fewer badges (earned vs empty differ) -> count a fresh card too
    fz = C.card_sheet(W, H)
    draw_front_art(Canvas(fz), FRESH)
    t_all, _ = to_tiles(fz, base=t_both)
    ch = C.card_sheet(W, H)
    draw_front_art(Canvas(ch), CHAMP)
    t_all2, _ = to_tiles(ch, base=t_all)
    return len(t_front), len(t_both), len(t_all2)


def save(im, path, k=3):
    KX.upscale(im.convert("RGB"), k).save(path)


def ab_sheet(ims, cols=2, k=2, gap=12):
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W * k + (cols - 1) * gap, rows * H * k + (rows - 1) * gap), (16, 16, 20))
    for i, im in enumerate(ims):
        sheet.paste(KX.upscale(im.convert("RGB"), k), ((i % cols) * (W * k + gap), (i // cols) * (H * k + gap)))
    return sheet


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    s1 = render_front(HERO)
    s2 = render_back(HERO)
    s3 = render_front(HEROINE)
    s4 = render_front(CHAMP)
    s5 = render_front(FRESH)
    s6 = render_front(HERO, card_top=42)
    s7 = render_back(CHAMP)
    s8 = render_back(dict(HEROINE, stars=2))
    save(s1, os.path.join(out, "main.png"))
    for i, im in enumerate((s1, s2, s3, s4, s5, s6, s7, s8), 1):
        save(im, os.path.join(out, "state_%02d.png" % i))
    parts_sheet().convert("RGB").save(os.path.join(out, "parts.png"))
    ab_sheet([render_front(dict(HERO, stars=t)) for t in range(5)] + [render_back(dict(HERO, stars=4))],
             cols=3).save(os.path.join(out, "variants.png"))
    print("BG0 tiles front / +back / +fresh+champ:", budget())
