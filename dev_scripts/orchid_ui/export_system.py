"""
Export the Orchid save prompt and start menu polish (approved mock_system.py) to game assets.
Every piece is drawn with the mockup's own code (mock_system.py / system_ext.py), so ROM art == mock art.

Field windows (start menu, save card, chips) are std windows: the frame is the player's FRAME type
(BG palette 14, graphics/text_window/orchid_frame_N.png) and the window pixels use the Orchid window
palette in BG palette 13 (export_yesno.py), with four field extras patched in at runtime
(menu.c LoadOrchidFieldWindowPalette):

    0 transparent  1 WHITE  2 INK  3 PANEL_SHADE  4 PANEL  5 PANEL_DARK  6/7 player name colour (fg / shadow)
    8/9 (unused here)  10-12 gold pill  13-15 Orchid accent (dark / face / light)

Writes (under the repo root):
  graphics/start_menu/menu_icons_muted.pal  resting start-menu icons (system_ext.menu_icon muted=0.35)
  graphics/start_menu/saving_ball.png       OBJ 16x16 x5: the saving Poké Ball tilted -30, -15, 0, 15, 30 degrees
  graphics/start_menu/sparkles.png          OBJ 8x8 x2: big, small capture sparkle (menu-icon palette)
  graphics/start_menu/save_card.png         save card rows (14x2 tiles each): location band, PLAYER, BADGES, POKéDEX, TIME
  graphics/start_menu/chips.png             location chip pill (10x2), Safari well (11x4), Pyramid chip (12x4), pips
  src/data/start_menu_orchid.h              layout constants + the wobble frame table

usage: export_system.py
"""
import math
import os
from PIL import Image
from kit import *
import system_ext as X
import mock_system as MS
import menu_icons as MI
from battle_ext import silhouette
from gamefont import draw_text
from export_mart import save_indexed, pad16

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "start_menu")
HEADER = os.path.join(ROOT, "src", "data", "start_menu_orchid.h")

FIELD_REMAP = {TRANSPARENT: 0, WHITE: 1, INK: 2, PANEL_SHADE: 3, PANEL: 4, PANEL_DARK: 5, SPARE_A: 6, SPARE_B: 7,
               SELECT_DARK: 10, SELECT: 11, SELECT_LIGHT: 12, ACCENT_DARK: 13, ACCENT: 14, ACCENT_LIGHT: 15}
LOC_CHIP_WIN = (1, 1, 10, 2)
SAFARI_WIN = (1, 1, 11, 4)
PYRAMID_WIN = (1, 1, 12, 4)
PIP_CELL = 16


def field_palette():
    import export_yesno as EY
    p = EY.window_palette()
    k = palette("orchid")
    p[4], p[5] = k[PANEL], k[PANEL_DARK]
    p[6], p[7] = (0, 0, 0), (0, 0, 0)          # name colour: patched at runtime
    return p


def remap(im):
    """kit-role sheet -> field window palette indices."""
    out = Image.new("P", im.size, 0)
    ip, op = im.load(), out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            v = ip[x, y]
            assert v in FIELD_REMAP, "kit role %d has no field window colour" % v
            op[x, y] = FIELD_REMAP[v]
    return out


def window_crop(fn, win, allow_above=False):
    sheet = new_sheet(240, 160)
    fn(Canvas(sheet))
    tx, ty, tw, th = win
    px = sheet.load()
    for y in range(160):
        for x in range(240):
            if px[x, y]:
                assert tx * 8 <= x < (tx + tw) * 8 and ty * 8 <= y < (ty + th) * 8, (x, y)
    return sheet.crop((tx * 8, ty * 8, (tx + tw) * 8, (ty + th) * 8))


def quantize(rgba, pal, size, at=(0, 0)):
    out = Image.new("P", size, 0)
    op, ip = out.load(), rgba.load()
    look = {c: i for i, c in enumerate(pal) if i}
    for y in range(rgba.size[1]):
        for x in range(rgba.size[0]):
            r, g, b, a = ip[x, y]
            if a:
                assert (r, g, b) in look, "colour %s not in the palette" % ((r, g, b),)
                op[at[0] + x, at[1] + y] = look[(r, g, b)]
    return out


# ---------------------------------------------------------------- start menu icons (muted palette)
def export_icons():
    pal = list(MI.PALETTE)
    muted = [snap(tuple(int(v + (g - v) * 0.35) for v, g in zip(c, (184, 184, 200)))) for c in pal]
    muted[1] = MI.PALETTE[1]
    write_jasc(os.path.join(OUT, "menu_icons_muted.pal"), muted)


# ---------------------------------------------------------------- saving ball + sparkles
BALL_ANGLES = (-30, -15, 0, 15, 30)


def export_ball():
    out = Image.new("P", (16, 16 * len(BALL_ANGLES)), 0)
    for k, a in enumerate(BALL_ANGLES):
        out.paste(quantize(X.pokeball_frame(a), MI.PALETTE, (16, 16)), (0, 16 * k))
    save_indexed(out, os.path.join(OUT, "saving_ball.png"), MI.PALETTE)
    sp = Image.new("P", (8, 16), 0)
    for k, big in enumerate((True, False)):
        rgba = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
        X.sparkle(rgba, 0, 0, big)
        sp.paste(quantize(rgba, MI.PALETTE, (8, 8)), (0, 8 * k))
    save_indexed(sp, os.path.join(OUT, "sparkles.png"), MI.PALETTE)


def wobble_table():
    """One rock (mock_system.saving_gif): 24 frames at 30*sin, then a 10-frame rest; frame = angle index."""
    seq = []
    for f in range(24):
        ang = 30 * math.sin(f / 24 * 2 * math.pi)
        seq.append(BALL_ANGLES.index(round(ang / 15) * 15))
    seq += [BALL_ANGLES.index(0)] * 10
    return seq


# ---------------------------------------------------------------- save card rows
def export_card():
    tx, ty, tw, th = X.SAVE_WIN
    x0, y0, w = tx * 8, ty * 8, tw * 8
    sheet = new_sheet(240, 160)
    cv = Canvas(sheet)
    cv.rect(x0, y0, x0 + w - 1, y0 + 16 * 5 - 1, WHITE)       # std_frame fill
    # system_ext.save_card, minus the text (printed by the ROM)
    rounded_box(cv, x0 + 1, y0 + 1, w - 2, 14, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    silhouette(cv, x0 + 6, y0 + 3, X.SIL["pin"], WHITE, ACCENT_DARK)
    for i, key in enumerate(["player", "badge", "dex", "clock"]):
        X.label_pill(cv, x0 + 1, y0 + 16 * (i + 1) + 1, w - 2, key)
    card = sheet.crop((x0, y0, x0 + w, y0 + 16 * 5))
    save_indexed(remap(card), os.path.join(OUT, "save_card.png"), field_palette())


# ---------------------------------------------------------------- chips
def export_chips():
    def loc(cv):
        X.label_pill(cv, 8, 9, 80, "pin")                      # mock_system.chip_location

    def safari(cv):
        disc(cv, 20, 23.5, 12, PANEL, INK, PANEL_SHADE, WHITE)  # mock_system.chip_safari

    def pyramid(cv):
        draw_text(cv, 8, 6, "Battle Pyramid", INK, PANEL_SHADE)  # mock_system.chip_pyramid

    a = window_crop(loc, LOC_CHIP_WIN)
    b = window_crop(safari, SAFARI_WIN)
    c = window_crop(pyramid, PYRAMID_WIN)
    # pips (mock_system.chip_pyramid): cleared = gold, current = accent, ahead = recessed
    pips = new_sheet(PIP_CELL, 3 * PIP_CELL)
    pc = Canvas(pips)
    for k, (face, light, shade) in enumerate(((SELECT, SELECT_LIGHT, SELECT_DARK),
                                               (ACCENT, ACCENT_LIGHT, ACCENT_DARK),
                                               (PANEL_SHADE, PANEL_DARK, WHITE))):
        disc(pc, 4, k * PIP_CELL + 4.5, 3.6, face, INK, light, shade)
    W_ = 96
    out = new_sheet(W_, 16 + 32 + 32 + 3 * PIP_CELL)
    out.paste(a, (0, 0))
    out.paste(b, (0, 16))
    out.paste(c, (0, 48))
    out.paste(pips, (0, 80))
    save_indexed(remap(out), os.path.join(OUT, "chips.png"), field_palette())
    # check: chip + pips == the mock's chip for every floor
    for floor in range(1, 8):
        mock = new_sheet(240, 160)
        MS_cv = Canvas(mock)
        pyramid(MS_cv)
        for k in range(7):
            cx, cy = 12 + k * 9, 29.5
            if k < floor - 1:
                disc(MS_cv, cx, cy, 3.6, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
            elif k == floor - 1:
                disc(MS_cv, cx, cy, 3.6, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
            else:
                disc(MS_cv, cx, cy, 3.6, PANEL_SHADE, INK, PANEL_DARK, WHITE)
        mine = c.copy()
        mp, pp = mine.load(), pips.load()
        for k in range(7):
            kind = 0 if k < floor - 1 else (1 if k == floor - 1 else 2)
            ox, oy = 4 + 9 * k - 4, 17 + 4 - 4          # window coords of the pip cell origin
            for y in range(PIP_CELL):
                for x in range(9):
                    v = pp[x, kind * PIP_CELL + y]
                    if v and 0 <= ox + x < 96 and 0 <= oy + y < 32:
                        mp[ox + x, oy + y] = v
        assert mine.tobytes() == mock.crop((8, 8, 104, 40)).tobytes(), "pip layout differs (floor %d)" % floor


# ---------------------------------------------------------------- header
def write_header():
    L = []
    A = L.append
    A("// GENERATED by dev_scripts/orchid_ui/export_system.py - do not edit by hand.")
    A("// Orchid start menu polish + save card (mock_system.py).")
    A("#ifndef GUARD_DATA_START_MENU_ORCHID_H")
    A("#define GUARD_DATA_START_MENU_ORCHID_H")
    A("")
    A("// field window palette (BG 13) colours")
    A("#define OSM_WHITE        1")
    A("#define OSM_INK          2")
    A("#define OSM_PANEL_SHADE  3")
    A("#define OSM_NAME_FG      6")
    A("#define OSM_NAME_SHADOW  7")
    A("#define OSM_ACCENT_DARK  13")
    A("")
    A("// start menu (mock_system.start_menu): std window at tile (%d, 1), %d wide, rows 16 px" % (MS.MX, MS.MW))
    A("#define OSM_MENU_X       %d" % MS.MX)
    A("#define OSM_MENU_W       %d" % MS.MW)
    A("#define OSM_MENU_TEXT_X  22")
    A("#define OSM_ICON_X       %d  // screen, sprite top-left" % (MS.MX * 8 + 4))
    A("#define OSM_ICON_Y0      8")
    A("#define OSM_ICON_LIFT    1")
    A("")
    tx, ty, tw, th = X.SAVE_WIN
    A("// save card (system_ext.save_card): 16 px rows in the %dx%d save window" % (tw, th))
    A("#define OSM_CARD_W       %d" % (tw * 8))
    A("#define OSM_CARD_LABEL_X %d" % (X.CAP_W + 5))
    A("#define OSM_CARD_VALUE_R %d  // values right-aligned to this x" % (tw * 8 - 6))
    A("#define OSM_CARD_LOC_DX  4   // location text centred, then +4")
    A("")
    A("// chips (chips.png rows): location 10x2, Safari 11x4, Pyramid 12x4, then 3 pips (16x16 cells)")
    A("#define OSM_CHIP_SHEET_W     96")
    A("#define OSM_CHIP_LOC_Y       0")
    A("#define OSM_CHIP_SAFARI_Y    16")
    A("#define OSM_CHIP_PYRAMID_Y   48")
    A("#define OSM_CHIP_PIPS_Y      80")
    A("#define OSM_PIP_CELL         %d" % PIP_CELL)
    A("#define OSM_PIP_W            9")
    A("#define OSM_PIP_X0           0   // window coords of pip 0's cell; pips every 9 px")
    A("#define OSM_PIP_Y            17")
    A("#define OSM_LOC_TEXT_X       %d" % (8 + X.CAP_W + 4 - 8))
    A("#define OSM_SAFARI_TEXT_X    28")
    A("#define OSM_SAFARI_ICON_X    %d  // item icon sprite centre (32x32, icon in its top-left 24x24)" % (8 + 16))
    A("#define OSM_SAFARI_ICON_Y    %d" % (12 + 16))
    A("#define OSM_PYRAMID_FLOOR_X  67")
    A("#define OSM_PYRAMID_FLOOR_Y  14")
    A("")
    A("// saving ball: x = message text x + first line width + 4, y = %d (screen, sprite top-left)" % 119)
    A("#define OSM_BALL_DX      4")
    A("#define OSM_BALL_Y       119")
    A("#define OSM_BALL_REST    %d  // frame index of the upright ball" % BALL_ANGLES.index(0))
    A("#define OSM_ROCKS        3")
    A("#define OSM_CLICK_FRAMES 8")
    A("#define OSM_TWINKLE      8   // sparkles toggle every 8 frames")
    seq = wobble_table()
    A("#define OSM_ROCK_LEN     %d" % len(seq))
    A("static const u8 sOrchidSaveBallRock[OSM_ROCK_LEN] = {%s};" % ", ".join(str(v) for v in seq))
    A("// sparkles around the ball (mock_system.render_save): dx, dy, small")
    A("static const s8 sOrchidSaveSparkles[3][3] = {{-5, -2, 0}, {17, -1, 1}, {16, 9, 0}};")
    A("")
    A("#endif // GUARD_DATA_START_MENU_ORCHID_H")
    with open(HEADER, "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    export_icons()
    export_ball()
    export_card()
    export_chips()
    write_header()
    print("wrote start menu / save assets")


if __name__ == "__main__":
    main()
