"""
Orchid window pieces: std frame (3x3 tiles, text_window format), dialogue box, menu cursor.

All frames are drawn on the 8px tile border *outside* a window's text rect,
exactly where DrawStdFrameWithCustomTileAndPalette / DrawDialogFrame put them.
"""
from kit import *


def std_frame(cv, tx, ty, tw, th, fill=WHITE):
    """Frame around a window whose text area is tile rect (tx, ty, tw, th)."""
    x0, y0 = tx * 8 - 8, ty * 8 - 8
    w, h = tw * 8 + 16, th * 8 + 16
    # 2px transparent margin, then ink / light / accent / accent / ink, then fill
    rounded_box(cv, x0 + 2, y0 + 2, w - 4, h - 4, 3, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    rounded_box(cv, x0 + 6, y0 + 6, w - 12, h - 12, 1, fill, INK, fill, fill, bevel=False)
    # inner corners: fill the 1px notch so text area is a clean rectangle
    cv.rect(x0 + 7, y0 + 7, x0 + w - 8, y0 + h - 8, fill)


def std_frame_tiles(theme="orchid"):
    """24x24 sheet in graphics/text_window/N.png layout (TL T TR / L C R / BL B BR)."""
    im = new_sheet(24, 24, theme)
    std_frame(Canvas(im), 1, 1, 1, 1)
    return im


def dialogue_box(cv, tx, ty, tw, th, fill=WHITE):
    """Speech box: chunkier rounded panel with accent end-caps (Gen 3 message box shape)."""
    # Gen 3 dialogue frames take 2 tiles on the left and 1 on the right
    x0, y0 = tx * 8 - 16, ty * 8 - 8
    w, h = tw * 8 + 24, th * 8 + 16
    rounded_box(cv, x0 + 2, y0 + 2, w - 4, h - 4, 4, fill, INK, WHITE, PANEL_SHADE)
    # accent end-caps
    for side in (0, 1):
        cx = x0 + 5 if side == 0 else x0 + w - 9
        rounded_box(cv, cx, y0 + 6, 6 if side == 0 else 4, h - 12, 2 if side == 0 else 1, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    # inner hairline
    cv.hline(x0 + 12, x0 + w - 13, y0 + h - 5, PANEL_SHADE)


def selection_bar(cv, x, y, w, h=14):
    """Highlight used for the current row in custom screens (gold pill)."""
    rounded_box(cv, x, y, w, h, 4, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
