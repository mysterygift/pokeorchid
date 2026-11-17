"""
Options screen mockup (shared screen -> Orchid theme).

Layout (240x160, 30x20 tiles):
    header   y 0..15     stepped tab "OPTION" (+ gear icon OBJ) and a thin rail
    rows     y 16..111   6 option pills, 16px pitch (vanilla YPOS_* = index * 16)
                         [icon field | label ............ < value > ]
    tray     y 112..159  live preview of the focused option + DONE button (vanilla CANCEL row)

BG2  : header, pills, tray (kit palette; focused row = palette swap to the gold variant)
BG2  : icon fields (2 field palettes, never swap)          BG3: scrolling grid
BG0  : text windows (labels, values, tray preview, DONE label + its gold pill when focused)
OBJ  : gear icon (start-menu icon sheet), 2 red chevrons on the focused row

usage: mock_options.py OUT_DIR
"""
import os
import sys
from PIL import Image
from kit import *
import kit_ext as K
import windows as Wn
import system_ext as X
from gamefont import draw_text, text_width

W, H = 240, 160
ROWS = ["TEXT SPEED", "BATTLE SCENE", "BATTLE STYLE", "SOUND", "BUTTON MODE", "FRAME"]
VALUES = [["SLOW", "MID", "FAST"], ["ON", "OFF"], ["SHIFT", "SET"], ["MONO", "STEREO"],
          ["NORMAL", "LR", "L=A"], None]
ICONS = ["text", "scene", "style", "sound", "button", "frame"]
COLOURS = ["blue", "red", "yellow", "green", "purple", "teal"]
DEFAULTS = [1, 0, 0, 0, 0, 1]          # MID, ON, SHIFT, MONO, NORMAL, TYPE 1 (vanilla defaults)
CANCEL = 6
TEXT_DELAY = [8, 4, 1]                  # frames per character (vanilla sTextSpeedFrameDelays)

# --- geometry ---------------------------------------------------------------------
TAB_X1, RAIL_Y1 = 79, 9                 # header tab right edge, rail bottom (ink)
ROW_Y0, ROW_H = 16, 16
PILL_X, PILL_W = 8, 224
FIELD_W = 24                            # icon field = tiles 1..3 of each row
LABEL_X = PILL_X + FIELD_W + 5
INSET_X, INSET_W = 152, 68
CHEV_L, CHEV_R = 144, 222
TRAY_Y = 112
DIV_X = 178
CANCEL_PILL = (187, 129, 44)            # x, y, w (h 14)
PREVIEW_X, PREVIEW_Y, LINE_H = 10, TRAY_Y + 2, 14
SAMPLE = "Welcome to the world of\nPOKéMON! Text will print\nat this speed."
FRAME_WIN = (2, 16, 18, 2)              # tray frame-preview text rect (tiles)

DESC = {
    (1, 0): "ON: moves play their\nanimations in battle.",
    (1, 1): "OFF: skip move animations\nfor faster battles.",
    (2, 0): "SHIFT: you may switch\nPOKéMON when a foe faints.",
    (2, 1): "SET: no switch offer when\na foe faints.",
    (3, 0): "MONO: the same sound\nfrom both speakers.",
    (3, 1): "STEREO: music and cries\nuse both speakers.",
}
BUTTON_DESC = {
    0: ("L", "Off", "R", "Off", "L and R do nothing\nspecial in menus."),
    1: ("L", "Page up", "R", "Page down", "Flip long lists a\npage at a time."),
    2: ("L", "Same as A", "R", "Off", "Play one-handed:\nL works as A."),
}


def row_y(i):
    return ROW_Y0 + i * ROW_H


def value_text(i, v):
    return "TYPE %d" % v if VALUES[i] is None else VALUES[i][v]


FRAME_COUNT = 8


# ================================================================== BG art
def draw_header(cv):
    for x in range(W):
        bot = 15 if x <= TAB_X1 else max(RAIL_Y1, 15 - (x - TAB_X1))
        cv.vline(x, 0, bot - 1, ACCENT)
        cv.set(x, 0, ACCENT_LIGHT)
        cv.set(x, bot - 1, ACCENT_DARK)
        cv.set(x, bot, INK)
    # the chamfer gets a doubled ink step so the diagonal reads as an edge, not a staircase
    for k in range(1, 15 - RAIL_Y1):
        cv.set(TAB_X1 + k, 15 - k + 1, INK)
    # brass rivets on the rail
    for x in (226, 233):
        X.brass_rivet(cv, x, 3)


def draw_pill(cv, i):
    y = row_y(i) + 1
    rounded_box(cv, PILL_X, y, PILL_W, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    # recessed value inset: shade on top/left, light bottom/right
    ix, iy, iw, ih = INSET_X, y + 2, INSET_W, 10
    cv.rect(ix, iy, ix + iw - 1, iy + ih - 1, WHITE)
    cv.hline(ix + 1, ix + iw - 2, iy, PANEL_SHADE)
    cv.vline(ix, iy + 1, iy + ih - 2, PANEL_SHADE)
    cv.hline(ix + 1, ix + iw - 2, iy + ih - 1, WHITE)
    for (x, yy) in ((ix, iy), (ix + iw - 1, iy), (ix, iy + ih - 1), (ix + iw - 1, iy + ih - 1)):
        cv.set(x, yy, PANEL)                       # rounded inset corners


def draw_tray(cv):
    y = TRAY_Y
    cv.rect(0, y, W - 1, H - 1, PANEL)
    cv.hline(0, W - 1, y, INK)
    cv.hline(0, W - 1, y + 1, WHITE)
    cv.hline(0, W - 1, H - 1, PANEL_SHADE)
    for x in range(2, W - 2):
        if x % 4 < 2:
            cv.set(x, y + 3, PANEL_SHADE)
    cv.vline(DIV_X, y + 6, H - 6, PANEL_SHADE)
    cv.vline(DIV_X + 1, y + 6, H - 6, WHITE)
    x, yy, w = CANCEL_PILL
    rounded_box(cv, x, yy, w, 14, 4, WHITE, INK, WHITE, PANEL_SHADE)


def build_bg(rows=True):
    im = new_sheet(W, H, "orchid")
    cv = Canvas(im)
    draw_header(cv)
    if rows:
        for i in range(len(ROWS)):
            draw_pill(cv, i)
    draw_tray(cv)
    return im


def build_fields(icons=True):
    """Icon fields: the left 16px of each pill, own palettes (A: red/yellow/green/blue, B: purple/teal)."""
    sheets = {"A": X.p_sheet(W, H, X.FIELD_PAL_A), "B": X.p_sheet(W, H, X.FIELD_PAL_B)}
    for i in range(len(ROWS)):
        y = row_y(i) + 1
        which, face = X.field_pal_idx(COLOURS[i], 1)
        _, light = X.field_pal_idx(COLOURS[i], 0)
        _, dark = X.field_pal_idx(COLOURS[i], 2)
        cv = Canvas(sheets[which])
        if not icons:
            continue
        rounded_box(cv, PILL_X, y, FIELD_W + 4, 14, 4, face, 1, light, dark)
        for yy in range(y, y + 14):                  # square the right side, ink divider
            for xx in range(PILL_X + FIELD_W, PILL_X + FIELD_W + 4):
                cv.set(xx, yy, 0)
            cv.set(PILL_X + FIELD_W - 1, yy, 1)
        cv.hline(PILL_X + 4, PILL_X + FIELD_W - 1, y, 1)
        cv.hline(PILL_X + 4, PILL_X + FIELD_W - 1, y + 13, 1)
        cv.hline(PILL_X + 2, PILL_X + FIELD_W - 2, y + 1, light)
        cv.hline(PILL_X + 2, PILL_X + FIELD_W - 2, y + 12, dark)
        X.centred_sil(cv, PILL_X + 1, y + 1, FIELD_W - 2, 12, ICONS[i], 2, dark)
    return sheets


def composite_bg(bg, focus, grid_scroll, base_pal, sel_pal):
    out = Image.new("RGBA", (W, H))
    from backdrop import GRID_PAL, grid_index
    opx, bpx = out.load(), bg.load()
    sel_cells = set()
    if focus < len(ROWS):
        for ty in (2 + 2 * focus, 3 + 2 * focus):
            for tx in range(4, 30):
                sel_cells.add((tx, ty))
    for y in range(H):
        for x in range(W):
            v = bpx[x, y]
            if v == 0:
                opx[x, y] = GRID_PAL[grid_index(x - grid_scroll, y - grid_scroll)] + (255,)
            else:
                pal = sel_pal if (x // 8, y // 8) in sel_cells else base_pal
                opx[x, y] = pal[v] + (255,)
    return out


# ================================================================== tray previews (BG0 text window)
def preview_text(cv, chars, speed):
    s = SAMPLE if chars is None else SAMPLE[:chars]
    draw_text(cv, PREVIEW_X, PREVIEW_Y, s, INK, PANEL_SHADE, line_h=LINE_H)


def preview_desc(cv, text):
    draw_text(cv, PREVIEW_X, PREVIEW_Y, text, INK, PANEL_SHADE, line_h=LINE_H)


def preview_buttons(cv, mode):
    l, lt, r, rt, d = BUTTON_DESC[mode]
    y = PREVIEW_Y + 3
    for x, key, cap in ((PREVIEW_X, l, lt), (92, r, rt)):
        off = cap == "Off"                     # unused buttons are drawn greyed
        w = X.keypad(cv, x, y + 2, key, PANEL if off else WHITE, PANEL_DARK if off else INK)
        draw_text(cv, x + w + 3, y - 2, cap, PANEL_DARK if off else ACCENT_DARK, PANEL_SHADE, font="narrow")
    draw_text(cv, PREVIEW_X, PREVIEW_Y + LINE_H + 2, d, INK, PANEL_SHADE, line_h=LINE_H)


def render(focus=0, values=None, flash=None, chars=None, grid_scroll=0, icons=True, arrow_bob=0,
           theme="orchid"):
    """flash: None | 'L' | 'R' (chevron pressed on the focused row). chars: text-speed sample progress."""
    values = list(DEFAULTS if values is None else values)
    base = palette(theme)
    sel = list(base)
    sel[PANEL], sel[WHITE], sel[PANEL_SHADE] = base[SELECT], base[SELECT_LIGHT], base[SELECT_DARK]
    out = composite_bg(build_bg(), focus, grid_scroll, base, sel)
    for k, sh in build_fields(icons).items():
        X.comp(out, sh, X.FIELD_PAL_A if k == "A" else X.FIELD_PAL_B)

    # ---- BG0 text
    def text(cv):
        draw_text(cv, 24, -1, "OPTION", WHITE, ACCENT_DARK)
        for i, name in enumerate(ROWS):
            y = row_y(i)
            draw_text(cv, LABEL_X if icons else PILL_X + 8, y, name, INK, PANEL_SHADE)
            v = value_text(i, values[i])
            draw_text(cv, INSET_X + (INSET_W - text_width(v)) // 2, y, v, INK, PANEL_SHADE)
        # DONE button (vanilla CANCEL row; gold pill blitted by the window when focused)
        x, yy, w = CANCEL_PILL
        if focus == CANCEL:
            Wn.selection_bar(cv, x, yy, w, 14)
        X.b_disc(cv, x + 9, yy + 7)
        draw_text(cv, x + 17, yy - 1, "DONE", INK, PANEL_SHADE, font="narrow")
        # tray preview
        if focus == 0:
            preview_text(cv, chars, values[0])
        elif focus in (1, 2, 3):
            preview_desc(cv, DESC[(focus, values[focus])])
        elif focus == 4:
            preview_buttons(cv, values[4])
        elif focus == CANCEL:
            preview_desc(cv, "Keep these settings and\nclose the OPTION menu.")
    K.layer(out, text, theme)

    if focus == 5:
        tx, ty, tw, th = FRAME_WIN
        X.draw_frame_type(out, values[5], tx, ty, tw, th)

        def ft(cv):
            draw_text(cv, tx * 8 + 2, ty * 8, "Menus look like this.", INK, PANEL_SHADE)
        K.layer(out, ft, theme)

    # ---- OBJ
    out.alpha_composite(X.menu_icon("OPTION"), (4, 0))
    if focus < len(ROWS):
        y = row_y(focus) + 4
        X.chevron(out, CHEV_L, y, left=True, flash=(flash == "L"))
        X.chevron(out, CHEV_R, y, left=False, flash=(flash == "R"))
    if focus == 0 and (chars is None or chars >= len(SAMPLE)):
        lines = SAMPLE.split("\n")
        X.down_arrow(out, PREVIEW_X + text_width(lines[-1]) + 3, PREVIEW_Y + LINE_H * 2 + 6, arrow_bob)
    return out


# ================================================================== parts sheet
def parts():
    from PIL import ImageDraw
    sc = 4
    out = Image.new("RGBA", (1000, 1000), (28, 28, 36, 255))
    d = ImageDraw.Draw(out)
    full = render(0, grid_scroll=0)
    y = 10

    def put(img, x, yy, cap):
        d.text((x, yy), cap, fill=(230, 230, 240))
        out.paste(K.upscale(img, sc), (x, yy + 14))
        return yy + 14 + img.size[1] * sc + 14

    y = put(full.crop((0, 16, 236, 48)), 10, y,
            "Option pill: icon field (BG, field palette) + label + recessed value inset; focused = gold palette swap + red chevrons (OBJ)")
    f2 = render(0, flash="R", grid_scroll=0)
    y = put(f2.crop((136, 16, 236, 32)), 10, y, "Chevron pressed: lit fill + 1px push outward for 8 frames, value swaps on the press frame")
    # icon fields alone
    fields = Image.new("RGBA", (6 * 28, 16), (0, 0, 0, 0))
    full_f = render(5)
    for i in range(6):
        fields.alpha_composite(full_f.crop((8, row_y(i) + 1, 32, row_y(i) + 15)), (i * 28, 1))
    y2 = put(fields, 10, y, "Icon fields: text speed / battle scene / battle style / sound / button mode / frame")
    hdr = render(0).crop((0, 0, 120, 16))
    y = put(hdr, 10, y2, "Header tab + rail (gear = start-menu OPTION icon, OBJ)")
    # frame-type swatches
    sw = Image.new("RGBA", (8 * 28, 28), (0, 0, 0, 0))
    for n in range(1, 9):
        sw.alpha_composite(X.frame_tiles(n), ((n - 1) * 28, 0))
    put(sw, 10, y, "FRAME types 1-8 (kit-built, 24x24 text_window tile sets) as loaded into the preview")
    return out


# ================================================================== frames sheet
def frames_sheet(sc=3):
    """TYPE 1-8: each frame 9-sliced around a 14x4-tile window on the grid, plus its 24x24 tile set."""
    from PIL import ImageDraw
    from backdrop import GRID_PAL, grid_index
    pw, ph = 168, 56
    cols, rows = 2, 4
    cap = 18
    out = Image.new("RGBA", (cols * pw * sc + 3 * 16, rows * (ph * sc + cap) + 5 * 12), (28, 28, 36, 255))
    d = ImageDraw.Draw(out)
    for n in range(1, FRAME_COUNT + 1):
        panel = K.grid_frame(0, pw, ph)
        win = Image.new("RGBA", (128, 48), (0, 0, 0, 0))
        X.draw_frame_type(win, n, 1, 1, 14, 4)

        def txt(cv, n=n):
            draw_text(cv, 8, 8, "TYPE %d  %s" % (n, X.FRAME_NAMES[n - 1]), INK, PANEL_SHADE)
            draw_text(cv, 8, 24, "Menus look like this.", INK, PANEL_SHADE)
        K.layer(win, txt, "orchid")
        panel.alpha_composite(win, (4, 4))
        # tile set, spread 1px apart so the 9 tiles read
        t = X.frame_tiles(n)
        for j in range(3):
            for i in range(3):
                panel.alpha_composite(t.crop((i * 8, j * 8, i * 8 + 8, j * 8 + 8)), (138 + i * 9, 14 + j * 9))
        x = 16 + ((n - 1) % cols) * (pw * sc + 16)
        y = 12 + ((n - 1) // cols) * (ph * sc + cap + 12)
        d.text((x, y), "TYPE %d  %s  -  %d tiles (8 frame + 1 fill), 1 palette" % (
            n, X.FRAME_NAMES[n - 1].replace("é", "e"), X.frame_tile_count(n)), fill=(230, 230, 240))
        out.paste(K.upscale(panel, sc), (x, y + cap))
    return out


# ================================================================== main
def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    up = lambda im, name: K.upscale(im, 3).save(os.path.join(out_dir, name))
    main_im = render(0, grid_scroll=3)
    up(main_im, "main.png")
    up(main_im, "state_01.png")
    up(render(5, values=[1, 0, 0, 0, 0, 5], grid_scroll=3), "state_02.png")
    frames_sheet().save(os.path.join(out_dir, "frames.png"))
    up(render(0, values=[2, 0, 0, 0, 0, 1], flash="R", chars=9, grid_scroll=3), "state_03.png")
    up(render(4, values=[1, 0, 0, 0, 1, 1], grid_scroll=3), "state_04.png")
    # A/B: icon fields vs text-only labels
    sheet = X.sheet_grid([("A  icon fields (recommended)", render(0, grid_scroll=3)),
                          ("B  text-only labels", render(0, grid_scroll=3, icons=False))], 2)
    sheet.save(os.path.join(out_dir, "variants_options.png"))
    # tile budget
    t1, _ = to_tiles(build_bg())
    fa, fb = build_fields().values()
    ta, _ = to_tiles(fa)
    tb, _ = to_tiles(fb)
    print("options BG2 art tiles:", len(t1), " icon fields:", len(ta) - 1 + len(tb) - 1)


if __name__ == "__main__":
    main(sys.argv[1])
