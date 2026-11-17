"""
Start menu v2 mock: icon-only banner mounted to the right screen edge, slides in from the right.
Location pill sits on the field with no window around it.

Variants
  A  icons only; the selected icon sits on a gold tab that pokes out of the banner
  B  same, but the gold tab slides out further left and carries the option's name
Approved: variant B (2026-11-17). export_system.py builds the ROM art from draw_banner_body / draw_tab /
chip_bare, and the slide tables from slide_open / slide_close.
usage: mock_start_v2.py OUT_DIR
"""
import math
import os
import sys

UI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, UI)
os.chdir(UI)
from PIL import Image  # noqa: E402
from kit import *  # noqa: E402,F401
import kit_ext as K  # noqa: E402
import system_ext as X  # noqa: E402
from gamefont import draw_text, text_width  # noqa: E402
import mock_system as M  # noqa: E402

W, H = 240, 160
PITCH = 18          # icon row pitch
BAND = 3            # accent band on the banner's left edge
BW = BAND + 2 + 16 + 4   # banner width on screen (flush right)
LABEL = {"POKéDEX": "POKéDEX", "POKéMON": "POKéMON", "BAG": "BAG", "POKéNAV": "POKéNAV",
         "SAVE": "SAVE", "OPTION": "OPTION", "EXIT": "EXIT", "RETIRE": "RETIRE", "REST": "REST"}


def banner_geom(n):
    h = n * PITCH + 6
    return W - BW, (H - h) // 2, h


def draw_banner_body(cv, x0, y0, h, n):
    # body: ink slab, rounded on the left only (the right side runs off-screen)
    rounded_box(cv, x0, y0, BW + 8, h, 4, INK, INK, INK_SOFT, INK, bevel=True)
    # chunky accent band down the left edge
    for y in range(y0 + 3, y0 + h - 3):
        cv.hline(x0 + 1, x0 + BAND, y, ACCENT)
    cv.vline(x0 + 1, y0 + 3, y0 + h - 4, ACCENT_LIGHT)
    cv.vline(x0 + BAND, y0 + 3, y0 + h - 4, ACCENT_DARK)
    # faint row separators between icons
    for i in range(1, n):
        y = y0 + 3 + i * PITCH - 1
        cv.hline(x0 + BAND + 3, x0 + BW - 3, y, INK_SOFT if i % 1 == 0 else INK)
        for x in range(x0 + BAND + 3, x0 + BW - 2, 2):
            cv.set(x, y, INK)


def tab_geom(x0, y0, cursor, variant, label_w):
    ty = y0 + 3 + cursor * PITCH
    if variant == "A":
        tx, tw = x0 - 4, BW + 8
    else:
        tw = BW + 8 + label_w + 10
        tx = x0 - (label_w + 10) - 4
    return tx, ty, tw


def draw_tab(cv, x0, y0, cursor, variant, label, label_w, name_col):
    # selection tab: gold, pokes out of the banner to the left
    tx, ty, tw = tab_geom(x0, y0, cursor, variant, label_w)
    rounded_box(cv, tx, ty, tw, PITCH - 1, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    if variant == "B":
        fg, sh = name_col if name_col else (INK, SELECT_DARK)
        draw_text(cv, tx + 6, ty + 1, label, fg, sh)


def draw_banner(cv, x0, y0, h, cursor, n, variant, label, label_w, name_col):
    draw_banner_body(cv, x0, y0, h, n)
    draw_tab(cv, x0, y0, cursor, variant, label, label_w, name_col)


def start_v2(out, entries, cursor, gender="M", name="KAITO", variant="A", slide=0, icon_lift=-1):
    """slide = pixels the whole banner is still pushed to the right (0 = docked)."""
    n = len(entries)
    x0, y0, h = banner_geom(n)
    x0 += slide
    e = entries[cursor]
    label = name if e == "PLAYER" else LABEL.get(e, e)
    label_w = text_width(label)
    name_col = (SPARE_A, SPARE_B) if e == "PLAYER" else None
    K.layer(out, lambda cv: draw_banner(cv, x0, y0, h, cursor, n, variant, label, label_w, name_col),
            "orchid", **X.std_pal_kw(gender))
    for i, en in enumerate(entries):
        sel = i == cursor
        ix = x0 + BAND + 3 + (-4 if sel else 0)
        iy = y0 + 3 + i * PITCH + (icon_lift if sel else 0)
        out.alpha_composite(X.menu_icon(en, 0.0 if sel else 0.35), (ix, iy + 1))


def chip_bare(out, loc="Tosa Port", slide=0):
    """Location pill straight on the field: same spot as the approved chip, no window.
    slide = pixels it is still pushed off to the left (0 = docked)."""
    w = X.CAP_W + 4 + text_width(loc) + 7
    x = 8 - slide

    def fn(cv):
        X.label_pill(cv, x, 9, w, "pin")
        draw_text(cv, x + X.CAP_W + 4, 8, loc, INK, PANEL_SHADE)
    K.layer(out, fn, "orchid")


def render(entries=M.NORMAL, cursor=2, gender="M", variant="A", slide=0, chip="location", chip_slide=0):
    out = X.field_scene("brendan" if gender == "M" else "may")
    name = "KAITO" if gender == "M" else "MAY"
    if chip == "location":
        chip_bare(out, slide=chip_slide)
    elif chip == "safari":
        M.chip_safari(out)
    elif chip == "pyramid":
        M.chip_pyramid(out)
    start_v2(out, entries, cursor, gender, name, variant, slide)
    return out


EASE_OUT = lambda t: 1 - (1 - t) ** 3
SLIDE_FULL = BW + 40 + 8       # banner pushed fully off-screen right
CHIP_FULL = 8 + 96             # pill width + its left margin: fully off-screen left


def slide_open():
    """[(banner slide, chip slide)] for open frames 0..12 (ease-out)."""
    return [(round(SLIDE_FULL * (1 - EASE_OUT(f / 12))), round(CHIP_FULL * (1 - EASE_OUT(f / 12)))) for f in range(13)]


def slide_close():
    """[(banner slide, chip slide)] for close frames 0..8 (ease-in)."""
    return [(round(SLIDE_FULL * (f / 8) ** 2), round(CHIP_FULL * (f / 8) ** 2)) for f in range(9)]


def slide_gif(path, variant):
    """Open: banner eases in from off-screen right (12 frames); cursor walks; close: eases out."""
    frames, durs = [], []
    ease = lambda t: 1 - (1 - t) ** 3
    full = BW + 40 + 8
    cfull = 8 + 96              # pill width + its left margin: fully off-screen
    for f in range(13):
        k = 1 - ease(f / 12)
        frames.append(render(variant=variant, cursor=0, slide=round(full * k), chip_slide=round(cfull * k)))
        durs.append(33)
    durs[-1] = 500
    for c in (1, 2, 3, 4, 5):
        frames.append(render(variant=variant, cursor=c))
        durs.append(450)
    for f in range(9):
        k = (f / 8) ** 2
        frames.append(render(variant=variant, cursor=5, slide=round(full * k), chip_slide=round(cfull * k)))
        durs.append(33)
    durs[-1] = 600
    frames = [K.upscale(fr.convert("RGB"), 3) for fr in frames]
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durs, loop=0)


def sheet(path, rows):
    from PIL import ImageDraw
    sc, pad, cap = 2, 12, 18
    cols = 2
    w = cols * (W * sc + pad) + pad
    hh = ((len(rows) + 1) // 2) * (H * sc + pad + cap) + pad
    im = Image.new("RGB", (w, hh), (28, 28, 36))
    d = ImageDraw.Draw(im)
    for k, (title, fr) in enumerate(rows):
        x = pad + (k % cols) * (W * sc + pad)
        y = pad + (k // cols) * (H * sc + pad + cap)
        d.text((x, y), title, fill=(230, 230, 240))
        im.paste(K.upscale(fr.convert("RGB"), sc), (x, y + cap))
    im.save(path)


def main(out):
    os.makedirs(out, exist_ok=True)
    for v in ("A", "B"):
        K.upscale(render(variant=v).convert("RGB"), 3).save(os.path.join(out, "v2_%s_bag.png" % v))
        K.upscale(render(variant=v, cursor=4).convert("RGB"), 3).save(os.path.join(out, "v2_%s_player.png" % v))
        slide_gif(os.path.join(out, "v2_%s_slide.gif" % v), v)
        sheet(os.path.join(out, "v2_%s_sheet.png" % v), [
            ("%s - BAG selected" % v, render(variant=v)),
            ("%s - PLAYER selected (name colour)" % v, render(variant=v, cursor=4)),
            ("%s - Safari Zone (female)" % v, render(M.SAFARI, 0, "F", v, chip="safari")),
            ("%s - Battle Pyramid" % v, render(M.PYRAMID, 3, "M", v, chip="pyramid")),
        ])
    K.upscale(M.render_start().convert("RGB"), 3).save(os.path.join(out, "v1_approved.png"))


if __name__ == "__main__":
    main(sys.argv[1])
