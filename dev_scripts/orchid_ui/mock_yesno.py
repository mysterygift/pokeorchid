"""
Orchid YES/NO mock: current ROM vs proposed, in three places that use the shared YES/NO menu.

Inputs are real mGBA screenshots (240x160) of the current ROM:
  <ctx>_cur.png   the prompt with today's YES/NO (frame + ▶ cursor)
  <ctx>_bg.png    the same screen right after the YES/NO closed (what sits under the box)
for ctx in: field (script question), party (party-menu prompt), save (save prompt).

Proposed = the approved save-prompt YES/NO (system_ext.yes_no): Orchid std frame, YES / NO rows,
gold pill on the selected row, no ▶. Window (23,9,5,4) -> frame x 176..231, the right edge of the
other Orchid popups. Everything outside the YES/NO area is the current screen, unchanged.

usage: mock_yesno.py SHOTS_DIR OUT_PNG
"""
import os
import sys
from PIL import Image, ImageDraw
import kit_ext as K
import system_ext as X

CONTEXTS = [
    ("field", "Overworld script question (msgbox MSGBOX_YESNO -> DisplayYesNoMenuDefaultYes)"),
    ("party", "Party menu prompt (party_menu.c PartyMenuDisplayYesNoMenu -> CreateYesNoMenu)"),
    ("save", "Save prompt (start_menu.c -> DisplayYesNoMenuDefaultYes)"),
]
OLD_WIN = (21, 9, 5, 4)          # sYesNo_WindowTemplates / sPartyMenuYesNoWindowTemplate
BG = (28, 28, 36)
LABEL = (230, 230, 240)


def frame_px(win):
    tx, ty, tw, th = win
    return tx * 8 - 8, ty * 8 - 8, (tx + tw) * 8 + 8, (ty + th) * 8 + 8


def proposed(cur, bg, cursor=0):
    out = cur.copy()
    x0, y0, x1, y1 = frame_px(OLD_WIN)
    out.paste(bg.crop((x0, y0, x1, y1)), (x0, y0))          # remove today's box
    X.yes_no(out, cursor)
    return out


def zoom_region():
    a = frame_px(OLD_WIN)
    b = frame_px(X.YESNO)
    return min(a[0], b[0]) - 8, min(a[1], b[1]) - 8, max(a[2], b[2]) + 8, max(a[3], b[3]) + 8


def main(shots, out_path):
    zx0, zy0, zx1, zy1 = zoom_region()
    zw, zh = (zx1 - zx0) * 4, (zy1 - zy0) * 4
    colw = 750 + zw
    roww = 160 * 2 + 40
    sheet = Image.new("RGB", (40 + 2 * colw + 40, 60 + len(CONTEXTS) * (max(roww, zh) + 50)), BG)
    d = ImageDraw.Draw(sheet)
    d.text((40, 16), "Orchid YES/NO: current ROM (left) vs proposed (right). 1x screen at 2x for legibility + 4x zoom of the box.", fill=LABEL)
    for r, (ctx, title) in enumerate(CONTEXTS):
        cur = Image.open(os.path.join(shots, ctx + "_cur.png")).convert("RGBA")
        bg = Image.open(os.path.join(shots, ctx + "_bg.png")).convert("RGBA")
        new = proposed(cur, bg)
        y = 60 + r * (max(roww, zh) + 50)
        d.text((40, y), title, fill=LABEL)
        for c, (name, im) in enumerate((("current", cur), ("proposed", new))):
            x = 40 + c * colw
            d.text((x, y + 18), name, fill=LABEL)
            sheet.paste(im.convert("RGB"), (x, y + 36))                      # true 1x
            sheet.paste(K.upscale(im, 2).convert("RGB"), (x + 250, y + 36))  # 2x
            z = im.crop((zx0, zy0, zx1, zy1))
            sheet.paste(K.upscale(z, 4).convert("RGB"), (x + 250 + 490, y + 36))
    sheet.save(out_path)
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
