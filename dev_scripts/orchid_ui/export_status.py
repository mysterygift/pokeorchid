"""
Export the shared Orchid status pictograms (battle healthboxes + party menu).

Writes graphics/interface/orchid_status_icons.png: a 16x(16*N) indexed sheet,
one 16x16 OBJ frame per status in STATUS_ORDER, palette = status_icons.STATUS_PAL.
C side: gOrchidStatusIcons_Gfx / gOrchidStatusIcons_Pal (src/graphics.c) and the
frame enum ORCHID_STATUS_* in include/constants/orchid_ui.h.
usage: export_status.py
"""
import os
from PIL import Image
import status_icons as S

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STATUS_ORDER = ("psn", "tox", "par", "slp", "brn", "frz", "frb", "fnt", "pkrs")


def main():
    n = len(STATUS_ORDER)
    sheet = Image.new("P", (16, 16 * n), 0)
    flat = [c for rgb in S.STATUS_PAL for c in rgb]
    sheet.putpalette(flat + [0] * (768 - len(flat)))
    for i, k in enumerate(STATUS_ORDER):
        sheet.paste(S.status_index(k), (0, 16 * i))
    out = os.path.join(ROOT, "graphics", "interface", "orchid_status_icons.png")
    sheet.save(out, transparency=0)
    print("wrote", out, sheet.size, "colours", len(S.STATUS_PAL))


if __name__ == "__main__":
    main()
