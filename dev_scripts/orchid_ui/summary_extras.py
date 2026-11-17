"""
Shiny star + markings on the Orchid summary screen (proposal, round after the summary was approved).

  * Shiny: a gold Gen 3 star (ink outline, SELECT ramp) set into the dais band between the ball and
    status sockets, under the stage (clear of the front pic). OBJ, shown only for shiny Pokémon.
  * Markings (● ■ ▲ ♥, Gen 3 order): four 5x5 marks in the No. pill's value area, left of the dex
    number. Set marks in ACCENT_DARK, unset marks in PANEL_SHADE (the pill's own bevel colour).
    Drawn as BG0 pixels in the left-column text window; same on every page.

usage: summary_extras.py OUT_DIR
"""
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as KX
import mock_summary as M
import summary_ext as S

STAR_C = (M.DAIS_C[0], M.DAIS_C[1] + M.DAIS_R - 4)      # centre of the 9x9 star OBJ
STAR = ["....X....",
        "...XYX...",
        "...XYX...",
        "XXXXYXXXX",
        "XYYYYYYZX",
        ".XYYYYZX.",
        "..XYXZX..",
        ".XYX.XZX.",
        ".XX...XX."]
STAR_MAP = {"X": INK, "Y": SELECT_LIGHT, "Z": SELECT}

MARKS = [[".XXX.", "XXXXX", "XXXXX", "XXXXX", ".XXX."],     # circle
         ["XXXXX", "XXXXX", "XXXXX", "XXXXX", "XXXXX"],     # square
         ["..X..", "..X..", ".XXX.", ".XXX.", "XXXXX"],     # triangle
         ["XX.XX", "XXXXX", "XXXXX", ".XXX.", "..X.."]]     # heart
MARK_X0 = M.LX + M.NO_CAP + 3         # first mark's left edge (inside the No. pill value area)
MARK_Y = M.NO_Y + 4                   # 5x5 marks centred in the pill face
MARK_PITCH = 6                        # 4 marks end at x 53, clear of a 4-digit dex number
MARK_ON, MARK_OFF = ACCENT_DARK, PANEL_SHADE


def star_sheet():
    """9x9 star, kit roles (drawn as a 16x16 OBJ, star at the top-left)."""
    im = M.sheet("male").crop((0, 0, 16, 16))
    stamp(Canvas(im), 0, 0, STAR, STAR_MAP)
    return im


def draw_marks(cv, markings):
    for i, rows in enumerate(MARKS):
        stamp(cv, MARK_X0 + i * MARK_PITCH, MARK_Y, rows, {"X": MARK_ON if markings & (1 << i) else MARK_OFF})


def render(base, theme, markings, shiny):
    out = base.copy()
    txt = M.sheet(theme)
    draw_marks(Canvas(txt), markings)
    out.alpha_composite(KX.sheet_rgba(txt, S.txt_pal(theme)))
    if shiny:
        out.alpha_composite(KX.sheet_rgba(star_sheet(), S.art_pal(theme)), (STAR_C[0] - 4, STAR_C[1] - 4))
    return out


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    k = 3
    a = render(M.render_info(), "male", 0b1001, True)
    b = render(M.render_skills(S.heroine_mon(), "female"), "female", 0b0110, True)
    c = render(M.render_moves(), "male", 0, False)
    shots = [(a, "INFO: shiny, circle + heart marked"), (b, "SKILLS, female theme: shiny, square + triangle marked"), (c, "MOVES: not shiny, nothing marked")]
    zoom = a.crop((0, 80, 92, 140))
    W = 240 * k
    canvas = Image.new("RGB", (W * 3 + 32, 160 * k + 40 + 60 * 4 + 40), (16, 16, 20))
    d = ImageDraw.Draw(canvas)
    for i, (im, cap) in enumerate(shots):
        canvas.paste(KX.upscale(im.convert("RGB"), k), (8 + i * (W + 8), 24))
        d.text((8 + i * (W + 8), 6), cap, fill=(230, 230, 240))
    y = 160 * k + 40
    canvas.paste(KX.upscale(zoom.convert("RGB"), 4), (8, y + 16))
    d.text((8, y), "left column at 4x: shiny star in the dais band, markings in the No. pill", fill=(230, 230, 240))
    path = os.path.join(out_dir, "summary_extras_mock.png")
    canvas.save(path)
    print(path)


if __name__ == "__main__":
    main(sys.argv[1])
