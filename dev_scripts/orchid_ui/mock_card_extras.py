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

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# ---- the new back icons ("block", "bp") and the link pill's "badge" live in card_ext.ICONS

# ---- back with the two new rows
rows = [("hof", "HALL OF FAME DEBUT", "31:09:46"), ("link", "LINK BATTLES", "W:12  L:5"),
        ("trade", "POKéMON TRADES", "8"), ("contest", "CONTESTS W/FRIENDS", "3"),
        ("block", "POKéBLOCKS W/FRIENDS", "14"), ("bp", "BATTLE POINTS WON", "120BP")]
M.back_rows = lambda d: rows
M.save(M.render_back(dict(M.CHAMP)), os.path.join(OUT, "back_icons.png"))


# ---- link front (variant B = mock_card.draw_link_front_*; A = full-width well, no pill)
def link_front(variant, d):
    pill = variant == "B"
    pal = C.card_palette(d["gender"], d["stars"])
    out = KX.grid_frame(0)
    a = C.card_sheet(240, 160)
    M.draw_link_front_art(Canvas(a), d, pill)
    out.alpha_composite(KX.sheet_rgba(a, pal))
    pic, _ = C.trainer_pic(d["gender"])
    bb = pic.getbbox()
    out.alpha_composite(pic, (M.DAIS_C[0] - 32, M.DAIS_C[1] + int(M.DAIS_IN * .55) + 3 - bb[3]))
    t = C.card_sheet(240, 160)
    M.draw_link_front_text(Canvas(t), d, pill)
    out.alpha_composite(KX.sheet_rgba(t, pal))
    return out


friend = dict(M.HEROINE, stars=2, badges=6)
for v in ("A", "B"):
    M.save(link_front(v, friend), os.path.join(OUT, "link_%s.png" % v))
