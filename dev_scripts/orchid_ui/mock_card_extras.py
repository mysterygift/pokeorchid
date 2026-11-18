"""Trainer card extras: link/Union Room front (A, B) and the back with PokéBlock + BP icons.
usage (cwd = dev_scripts/orchid_ui): mock_card_extras.py OUT_DIR"""
import os
import sys
sys.path.insert(0, os.getcwd())
import mock_card as M
import card_ext as C
import kit_ext as KX
from kit import *
from gamefont import draw_text, text_width
import mock_battle_more as MB

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# ---- new back icons
C.ICONS["block"] = MB.SAFARI_SILHOUETTES["block"]
C.ICONS["bp"] = [            # medal on a V ribbon (Battle Points), distinct from the HoF trophy
    "XXX....XXX",
    ".XXX..XXX.",
    "..XXXXXX..",
    "..XXXXXX..",
    ".XXXXXXXX.",
    ".XXX..XXX.",
    ".XXX..XXX.",
    ".XXXXXXXX.",
    "..XXXXXX..",
]
C.ICONS["badge"] = [
    "....X....",
    "...XXX...",
    "..XX.XX..",
    ".XX...XX.",
    "XX..X..XX",
    ".XX...XX.",
    "..XX.XX..",
    "...XXX...",
    "....X....",
]

# ---- back with the two new rows
rows = [("hof", "HALL OF FAME DEBUT", "31:09:46"), ("link", "LINK BATTLES", "W:12  L:5"),
        ("trade", "POKéMON TRADES", "8"), ("contest", "CONTESTS W/FRIENDS", "3"),
        ("block", "POKéBLOCKS W/FRIENDS", "14"), ("bp", "BATTLE POINTS WON", "120BP")]
M.back_rows = lambda d: rows
M.save(M.render_back(dict(M.CHAMP)), os.path.join(OUT, "back_icons.png"))


# ---- link front
def link_front(variant, d, phrase=("HELLO  POKéMON", "BATTLE  AWESOME")):
    x, y, w, h = M.CASE
    pw = w if variant == "A" else w - 42

    def art(cv):
        C.card_shell(cv, *M.CARD, M.HEAD_H)
        M.draw_header(cv, d["stars"])
        C.nameplate(cv, M.COL_X + 2, M.NAME_Y, M.COL_W - 4, M.ROW_H)
        for name, yy in zip(["money", "dex", "time"], M.ROWS_Y):
            C.icon_pill(cv, M.COL_X, yy, M.COL_W, name, 20, M.ROW_H)
        C.dais(cv, M.DAIS_C[0], M.DAIS_C[1], M.DAIS_R, M.DAIS_IN)
        C.sig_well(cv, x, y, pw, h)
        if variant == "B":
            C.icon_pill(cv, x + pw + 4, y + 6, 38, "badge", 18, 16)

    out = KX.grid_frame(0)
    a = C.card_sheet(240, 160)
    art(Canvas(a))
    out.alpha_composite(KX.sheet_rgba(a, C.card_palette(d["gender"], d["stars"])))
    pic, _ = C.trainer_pic(d["gender"])
    bb = pic.getbbox()
    out.alpha_composite(pic, (M.DAIS_C[0] - 32, M.DAIS_C[1] + int(M.DAIS_IN * .55) + 3 - bb[3]))
    t = C.card_sheet(240, 160)
    tc = Canvas(t)
    M.draw_front_text(tc, d)
    draw_text(tc, x + 8, y - 1, phrase[0], INK, PANEL_SHADE)
    draw_text(tc, x + 8, y + 11, phrase[1], INK, PANEL_SHADE)
    if variant == "B":
        s = str(d["badges"])
        draw_text(tc, x + pw + 4 + 18 + (20 - text_width(s)) // 2, y + 5, s, INK, PANEL_SHADE)
    out.alpha_composite(KX.sheet_rgba(t, C.card_palette(d["gender"], d["stars"])))
    return out


friend = dict(M.HEROINE, stars=2, badges=6)
for v in ("A", "B"):
    M.save(link_front(v, friend), os.path.join(OUT, "link_%s.png" % v))
