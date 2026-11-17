"""
Export the Orchid YES/NO window art (approved yesno_mock.png).

Writes graphics/text_window/orchid_yesno.png: the 24x24 Orchid std frame (windows.std_frame_tiles)
re-indexed into the "Orchid window" palette layout, so ONE 16-colour palette serves the frame, the
text and the gold pill:

    0 transparent   1 WHITE (window fill)   2 INK (text, outlines)   3 PANEL_SHADE (text shadow)
    4/5 red  6/7 green  8/9 accent dark/light (TEXT_COLOR_* slots, same as party_menu's text palette)
    10 SELECT_DARK  11 SELECT  12 SELECT_LIGHT  (gold pill)
    13 ACCENT_DARK  14 ACCENT  15 ACCENT_LIGHT  (frame band)

menu.c loads the whole palette into a free BG slot (field: 13), or only entries 10-15 into a
screen's standard menu palette (whose 10-15 are unused), and the 9 tiles into free BG tiles.
usage: export_yesno.py
"""
import os
from PIL import Image
from kit import *
import windows as Wn
import export_party as EP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REMAP = {TRANSPARENT: 0, WHITE: 1, INK: 2, ACCENT_DARK: 13, ACCENT: 14, ACCENT_LIGHT: 15}


def window_palette():
    k = palette("orchid")
    p = EP.menu_text_palette()
    p[13], p[14], p[15] = k[ACCENT_DARK], k[ACCENT], k[ACCENT_LIGHT]
    return p


def main():
    src = Wn.std_frame_tiles("orchid")
    out = Image.new("P", src.size, 0)
    sp, op = src.load(), out.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            v = sp[x, y]
            assert v in REMAP, "unexpected frame colour role %d" % v
            op[x, y] = REMAP[v]
    path = os.path.join(ROOT, "graphics", "text_window", "orchid_yesno.png")
    EP.save_indexed(out, path, window_palette())
    print("wrote", path)


if __name__ == "__main__":
    main()
