"""
Export the Orchid OPTION screen and the 8 kit FRAME types (approved mock_options.py) to game assets.
Every piece is drawn with the mockup's own code (mock_options.py / system_ext.py), so ROM art == mock art.

BG layout (src/option_menu.c):
  BG0  text windows: option rows, tray preview, DONE button          charblock 2   prio 0
  BG1  FRAME preview: the selected frame type 9-sliced in the tray   charblock 2   prio 1
  BG2  screen art: header tab + "OPTION", 6 pills, picture fields, tray, DONE pill
                                                                     charblock 0   prio 2
  BG3  scrolling grid                                                charblock 0   prio 3

BG palettes: 0 kit (orchid), 1 = focused-row swap of 0 (gold), 2/3 picture fields A/B, 4 grid,
5 = the previewed frame type's palette (loaded at runtime from the kit frames).

Writes (under the repo root):
  graphics/option_menu/orchid/bg_tiles.png   BG2 + BG3 tiles (flip-deduped) + grid 2x2
  graphics/option_menu/orchid/bg.bin         BG2 tilemap 32x32 (palette bits included)
  graphics/option_menu/orchid/bg.pal         BG palettes 0-4 (80 colours)
  graphics/option_menu/orchid/done.png       BG0 DONE window pixels (6x2 tiles): [0] resting, [1] focused (gold pill)
  graphics/option_menu/orchid/keypad.png     L / R keypad glyphs for the BUTTON MODE preview: L, L off, R, R off (16x8 each)
  graphics/option_menu/orchid/chevron.png    OBJ 8x16 x2 (left chevron; [1] = pressed flash) + 8x8 continue arrow
  graphics/option_menu/orchid/chevron.pal
  graphics/text_window/orchid_frame_1..8.png the 8 kit FRAME types (24x24 text_window layout, own palette)
  src/data/option_menu_orchid.h              layout constants

usage: export_options.py
"""
import os
from PIL import Image
from kit import *
import system_ext as X
import mock_options as MO
import windows as Wn
from backdrop import GRID_PAL, grid_tile_image
from gamefont import draw_text
from export_mart import Tiler, tiles_png, save_indexed, pad16

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "option_menu", "orchid")
HEADER = os.path.join(ROOT, "src", "data", "option_menu_orchid.h")

# BG0 windows (tile rects)
ROWS_WIN = (3, 2, 27, 12)
PREVIEW_WIN = (1, 14, 21, 6)
DONE_WIN = (23, 16, 6, 2)


def sel_palette():
    base = palette("orchid")
    sel = list(base)
    sel[PANEL], sel[WHITE], sel[PANEL_SHADE] = base[SELECT], base[SELECT_LIGHT], base[SELECT_DARK]
    return sel


# ---------------------------------------------------------------- BG2: art + picture fields + grid
def art_sheet():
    """One 'P' sheet, value = palette block * 16 + colour: block 0 kit art, 2/3 picture fields A/B."""
    base = MO.build_bg()
    draw_text(Canvas(base), 24, -1, "OPTION", WHITE, ACCENT_DARK)    # mock: header text (static)
    fields = MO.build_fields()
    out = Image.new("P", base.size, 0)
    op, bp = out.load(), base.load()
    fa, fb = fields["A"].load(), fields["B"].load()
    for y in range(base.size[1]):
        for x in range(base.size[0]):
            if fa[x, y]:
                op[x, y] = 32 + fa[x, y]
            elif fb[x, y]:
                op[x, y] = 48 + fb[x, y]
            else:
                op[x, y] = bp[x, y]
    return out


def cell(T, art, cx, cy):
    px = art.load()
    vals = [px[cx * 8 + x, cy * 8 + y] for y in range(8) for x in range(8)]
    blocks = {v // 16 for v in vals if v}
    if not blocks:
        return 0
    assert len(blocks) == 1, "cell (%d,%d) mixes palettes %s" % (cx, cy, blocks)
    blk = blocks.pop()
    return T.add(tuple(v % 16 for v in vals)) | (blk << 12)


def export_bg():
    T = Tiler()
    art = art_sheet()
    tm = [0] * (32 * 32)
    for cy in range(20):
        for cx in range(30):
            tm[cy * 32 + cx] = cell(T, art, cx, cy)
    n_art = len(T.tiles)
    grid_base = n_art
    g = grid_tile_image().load()
    for ty in range(2):
        for tx in range(2):
            T.tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(T.tiles) <= 512
    tiles_png(T.tiles, os.path.join(OUT, "bg_tiles.png"), palette("orchid"))
    with open(os.path.join(OUT, "bg.bin"), "wb") as f:
        for e in tm:
            f.write(bytes((e & 0xFF, e >> 8)))
    pals = pad16(palette("orchid")) + pad16(sel_palette()) + pad16(X.FIELD_PAL_A) + pad16(X.FIELD_PAL_B) + pad16(GRID_PAL)
    write_jasc(os.path.join(OUT, "bg.pal"), pals)
    return dict(n_art=n_art, grid_base=grid_base)


# ---------------------------------------------------------------- BG0 pixel pieces
def window_crop(fn, win):
    """Draw with fn on a full-screen kit sheet and return the window rect (asserting nothing spills)."""
    sheet = new_sheet(240, 160)
    fn(Canvas(sheet))
    tx, ty, tw, th = win
    px = sheet.load()
    for y in range(160):
        for x in range(240):
            if px[x, y]:
                assert tx * 8 <= x < (tx + tw) * 8 and ty * 8 <= y < (ty + th) * 8, (x, y)
    return sheet.crop((tx * 8, ty * 8, (tx + tw) * 8, (ty + th) * 8))


def export_done():
    x, yy, w = MO.CANCEL_PILL

    def resting(cv):
        X.b_disc(cv, x + 9, yy + 7)

    def focused(cv):
        Wn.selection_bar(cv, x, yy, w, 14)
        X.b_disc(cv, x + 9, yy + 7)
    a, b = window_crop(resting, DONE_WIN), window_crop(focused, DONE_WIN)
    out = new_sheet(a.size[0], a.size[1] * 2)
    out.paste(a, (0, 0))
    out.paste(b, (0, a.size[1]))
    save_indexed(out, os.path.join(OUT, "done.png"), palette("orchid"))


def export_keypad():
    out = new_sheet(16, 32)
    cv = Canvas(out)
    for k, (key, off) in enumerate((("L", False), ("L", True), ("R", False), ("R", True))):
        X.keypad(cv, 0, 8 * k, key, PANEL if off else WHITE, PANEL_DARK if off else INK)
    save_indexed(out, os.path.join(OUT, "keypad.png"), palette("orchid"))


# ---------------------------------------------------------------- OBJ: chevrons + continue arrow
def export_chevron():
    out = X.p_sheet(8, 40, X.ARROW_PAL)
    cv = Canvas(out)
    stamp(cv, 1, 3, SMALL_ARROW, {"O": 1, "F": 2})
    stamp(cv, 1, 16 + 3, SMALL_ARROW, {"O": 1, "F": 3})
    rows = ["XXXXXXX", "XRRRRRX", "XRRRRRX", "XRRRRRX", ".XRRRX.", "..XRX..", "...X..."]  # X.down_arrow
    stamp(cv, 0, 32, rows, {"X": 1, "R": 2})
    save_indexed(out, os.path.join(OUT, "chevron.png"), X.ARROW_PAL)
    write_jasc(os.path.join(OUT, "chevron.pal"), pad16(X.ARROW_PAL))


# ---------------------------------------------------------------- the 8 kit FRAME types
def export_frames():
    for n in range(1, MO.FRAME_COUNT + 1):
        sheet = X.frame_sheet(n)
        # centre tile = plain WHITE (the BG1 preview uses it as the window fill)
        c = sheet.crop((8, 8, 16, 16))
        assert set(c.tobytes()) == {WHITE}, "frame %d centre tile is not plain fill" % n
        save_indexed(sheet, os.path.join(ROOT, "graphics", "text_window", "orchid_frame_%d.png" % n),
                     pad16(X.frame_palette(n)))


# ---------------------------------------------------------------- header
def write_header(bg):
    L = []
    A = L.append
    A("// GENERATED by dev_scripts/orchid_ui/export_options.py - do not edit by hand.")
    A("// Orchid OPTION screen (mock_options.py).")
    A("#ifndef GUARD_DATA_OPTION_MENU_ORCHID_H")
    A("#define GUARD_DATA_OPTION_MENU_ORCHID_H")
    A("")
    A("#define OOPT_PAL_KIT        0")
    A("#define OOPT_PAL_SELECTED   1")
    A("#define OOPT_PAL_GRID       4")
    A("#define OOPT_PAL_FRAME      5   // previewed FRAME type")
    A("#define OOPT_NUM_BG_PALS    5   // in bg.pal")
    A("#define OOPT_GRID_TILE      %d  // BG3 grid tiles TL, TR, BL, BR" % bg["grid_base"])
    A("")
    A("// kit colour roles (BG palette 0)")
    for name in ("INK", "WHITE", "PANEL", "PANEL_SHADE", "PANEL_DARK", "ACCENT_DARK"):
        A("#define OOPT_%-16s %d" % (name, globals()[name]))
    A("")
    A("// rows: 16 px pitch from y = %d; the focused row swaps palette on cells x %d..29" % (MO.ROW_Y0, 4))
    A("#define OOPT_ROW_Y0         %d" % MO.ROW_Y0)
    A("#define OOPT_ROW_TILE0      %d" % (MO.ROW_Y0 // 8))
    A("#define OOPT_SWAP_COL0      4")
    A("#define OOPT_SWAP_COL1      29")
    for name, r in (("ROWS", ROWS_WIN), ("PREVIEW", PREVIEW_WIN), ("DONE", DONE_WIN)):
        A("#define OOPT_%s_WIN_X  %d" % (name, r[0]))
        A("#define OOPT_%s_WIN_Y  %d" % (name, r[1]))
        A("#define OOPT_%s_WIN_W  %d" % (name, r[2]))
        A("#define OOPT_%s_WIN_H  %d" % (name, r[3]))
    rx, ry = ROWS_WIN[0] * 8, ROWS_WIN[1] * 8
    A("#define OOPT_LABEL_X        %d  // rows window coords" % (MO.LABEL_X - rx))
    A("#define OOPT_INSET_X        %d" % (MO.INSET_X - rx))
    A("#define OOPT_INSET_W        %d" % MO.INSET_W)
    A("#define OOPT_CHEV_L_X       %d  // screen, sprite top-left (8x16; arrow at +1,+3)" % (MO.CHEV_L - 1))
    A("#define OOPT_CHEV_R_X       %d" % (MO.CHEV_R - 1))
    A("#define OOPT_CHEV_DY        %d  // sprite y = row top + this" % (4 - 3))
    px_, py_ = PREVIEW_WIN[0] * 8, PREVIEW_WIN[1] * 8
    A("#define OOPT_PREVIEW_X      %d  // preview window coords" % (MO.PREVIEW_X - px_))
    A("#define OOPT_PREVIEW_Y      %d" % (MO.PREVIEW_Y - py_))
    A("#define OOPT_PREVIEW_LINE_H %d" % MO.LINE_H)
    A("#define OOPT_PREVIEW_SCREEN_X %d" % MO.PREVIEW_X)
    A("#define OOPT_PREVIEW_SCREEN_Y %d" % MO.PREVIEW_Y)
    A("#define OOPT_KEYPAD_R_X     92  // screen x of the R glyph (mock_options.preview_buttons)")
    x, yy, w = MO.CANCEL_PILL
    dx, dy = DONE_WIN[0] * 8, DONE_WIN[1] * 8
    A("#define OOPT_DONE_TEXT_X    %d  // DONE window coords" % (x + 17 - dx))
    A("#define OOPT_DONE_TEXT_Y    %d" % (yy - 1 - dy))
    fx, fy, fw, fh = MO.FRAME_WIN
    A("#define OOPT_FRAME_WIN_X    %d  // FRAME preview text rect (tiles); frame drawn around it" % fx)
    A("#define OOPT_FRAME_WIN_Y    %d" % fy)
    A("#define OOPT_FRAME_WIN_W    %d" % fw)
    A("#define OOPT_FRAME_WIN_H    %d" % fh)
    A("#define OOPT_FRAME_TEXT_X   %d  // preview window coords" % (fx * 8 + 2 - px_))
    A("#define OOPT_FRAME_TEXT_Y   %d" % (fy * 8 - py_))
    A("#define OOPT_GEAR_X         4   // OPTION icon (start-menu icon sheet), sprite top-left")
    A("#define OOPT_GEAR_Y         0")
    A("#define OOPT_FLASH_FRAMES   8")
    A("")
    A("#endif // GUARD_DATA_OPTION_MENU_ORCHID_H")
    with open(HEADER, "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    bg = export_bg()
    export_done()
    export_keypad()
    export_chevron()
    export_frames()
    write_header(bg)
    print("BG2: %d art tiles, grid at %d" % (bg["n_art"], bg["grid_base"]))


if __name__ == "__main__":
    main()
