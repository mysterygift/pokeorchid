"""
Satchel bag screen — background art (BG2) + layout constants shared with the mockups.

Screen grid is 30x20 tiles (240x160).
    left column   x 0..95    pocket wheel + satchel (sprites)
    header        x 96..239, y 0..15   pocket name tab with Gen 3 red arrows
    list          x 96..231, y 16..111 6 pill rows (16px), arrow gutter x 96..103
    scrollbar     x 232..239, y 16..111
    info tray     y 112..159 full width: item icon well + 3-line description
"""
import math
from kit import *
from backdrop import backdrop, band, pill

W, H = 240, 160

# --- layout (pixels) ----------------------------------------------------------
WHEEL_C = (48, 56)
WHEEL_R_OUT = 45          # outer ink ring
WHEEL_R_BAND = 44         # accent band
WHEEL_R_IN = 32           # inner face
BUTTON_R = 38             # ring radius where pocket buttons sit
HEADER = (96, 0, 239, 15)
LIST_X, LIST_Y, ROW_H, ROWS = 96, 16, 16, 6
PILL_X, PILL_W, PILL_H = 104, 128, 14
TRACK = (233, 17, 238, 110)
TRAY_Y = 112
ICON_WELL_C, ICON_WELL_R = (20, 136), 15
POCKET_NAME_CX = 168
POCKET_ARROWS = ((132, 8), (204, 8))   # sprite centres, left/right


def button_centres():
    cx, cy = WHEEL_C
    out = []
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        out.append((round(cx + BUTTON_R * math.cos(a)), round(cy + BUTTON_R * math.sin(a))))
    return out


def pill_rect(row):
    return PILL_X, LIST_Y + row * ROW_H + 1, PILL_W, PILL_H


# --- palette variants (same role layout, swapped faces) ----------------------
def variant(pal, kind):
    p = list(pal)
    if kind == "selected":
        p[PANEL], p[WHITE], p[PANEL_SHADE] = pal[SELECT], pal[SELECT_LIGHT], pal[SELECT_DARK]
    elif kind == "ghost":
        p[INK], p[PANEL], p[WHITE], p[PANEL_SHADE] = pal[ACCENT_LIGHT], pal[ACCENT_PALE], pal[ACCENT_PALE], pal[ACCENT_LIGHT]
    return p


# --- drawing -------------------------------------------------------------------
def draw_wheel(cv):
    cx, cy = WHEEL_C
    disc(cv, cx, cy, WHEEL_R_OUT, ACCENT_DARK, INK)
    # band: subtle inner light edge, outer shade
    ring(cv, cx, cy, WHEEL_R_OUT - 1, ACCENT, 1.0)
    ring(cv, cx, cy, WHEEL_R_IN + 2, ACCENT, 1.0)
    # inner face, Gen 3 3-step radial
    disc(cv, cx, cy, WHEEL_R_IN + 1, INK, None)
    disc(cv, cx, cy, WHEEL_R_IN, ACCENT_LIGHT, None)
    disc(cv, cx - 1, cy - 1, WHEEL_R_IN - 3, ACCENT_PALE, None)
    disc(cv, cx - 3, cy - 3, WHEEL_R_IN - 12, WHITE, None)
    # dither edge between pale and white so it isn't a hard step
    for y in range(cy - WHEEL_R_IN, cy + WHEEL_R_IN):
        for x in range(cx - WHEEL_R_IN, cx + WHEEL_R_IN):
            d = math.hypot(x + 0.5 - (cx - 3), y + 0.5 - (cy - 3))
            if WHEEL_R_IN - 12 < d <= WHEEL_R_IN - 10 and (x + y) % 2 == 0:
                cv.set(x, y, WHITE)
    # sockets the pocket buttons sit in (recessed ink dots, visible when buttons are small)
    for bx, by in button_centres():
        disc(cv, bx, by, 10.5, ACCENT_DARK, INK)


def draw_header(cv):
    x0, y0, x1, y1 = HEADER
    band(cv, x0, y0, x1, y1 - 1, ACCENT, ACCENT_LIGHT, ACCENT_DARK)
    cv.hline(x0, x1, y1, INK)
    # rounded bottom-left corner into the backdrop + left ink edge
    cv.vline(x0, y0, y1, INK)
    cv.set(x0, y1, 0)
    cv.set(x0 + 1, y1, INK)
    cv.set(x0, y1 - 1, INK)
    # little notch rivets (Gen 3 detailing)
    for x in (x0 + 6, x1 - 5):
        cv.set(x, 5, ACCENT_DARK)
        cv.set(x, 6, ACCENT_DARK)
        cv.set(x + 1, 5, ACCENT_LIGHT)


def draw_list(cv):
    for r in range(ROWS):
        x, y, w, h = pill_rect(r)
        pill(cv, x, y, w, h)


def draw_track(cv):
    x0, y0, x1, y1 = TRACK
    rounded_box(cv, x0, y0, x1 - x0 + 1, y1 - y0 + 1, 2, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
    # inner shadow on the top edge (recessed look)
    cv.hline(x0 + 2, x1 - 2, y0 + 1, INK_SOFT)


def draw_tray(cv):
    y = TRAY_Y
    cv.rect(0, y, W - 1, H - 1, PANEL)
    cv.hline(0, W - 1, y, INK)
    cv.hline(0, W - 1, y + 1, WHITE)
    cv.hline(0, W - 1, H - 1, PANEL_SHADE)
    # accent stitching line under the top edge (satchel seam motif)
    for x in range(2, W - 2):
        if x % 4 < 2:
            cv.set(x, y + 3, PANEL_SHADE)
    # icon well
    cx, cy = ICON_WELL_C
    disc(cv, cx, cy, ICON_WELL_R + 1, PANEL_SHADE, None)
    disc(cv, cx, cy, ICON_WELL_R, WHITE, INK)
    disc(cv, cx + 0.5, cy + 0.5, ICON_WELL_R - 2, PANEL, None)
    ring(cv, cx, cy, ICON_WELL_R - 1, PANEL_SHADE)
    # divider between well and text
    cv.vline(38, y + 6, H - 6, PANEL_SHADE)
    cv.vline(39, y + 6, H - 6, WHITE)


DESC_X, DESC_Y, DESC_LINE_H = 45, TRAY_Y + 2, 14   # 3 lines clear the stitch (y+3) and bottom edge


def build_bg(theme="male", pills=True):
    im = new_sheet(W, H, theme)
    cv = Canvas(im)
    # backdrop is the scrolling grid on BG3 — index 0 here is transparent
    draw_wheel(cv)
    draw_header(cv)
    if pills:
        draw_list(cv)
    draw_track(cv)
    draw_tray(cv)
    return im


if __name__ == "__main__":
    import sys
    im = build_bg(sys.argv[1] if len(sys.argv) > 1 else "male")
    tiles, tm = to_tiles(im)
    print("unique tiles (incl. blank):", len(tiles), "/ 320 budget")
