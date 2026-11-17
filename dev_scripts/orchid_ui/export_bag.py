"""
Export the satchel bag screen to game assets.

Writes (all under the repo root):
  graphics/bag/satchel_screen.png        BG2 + BG3 tiles (4bpp, kit palette indices)
  graphics/bag/satchel_screen.bin        BG2 tilemap, 32x32 (smolTM-compressed at build)
  graphics/bag/satchel_screen_male.pal   48 colours: pal 0 normal, pal 1 selected, pal 2 grid
  graphics/bag/satchel_screen_female.pal
  graphics/bag/satchel_hm.png            HM badge re-indexed to kit roles (blitted into list window)
  graphics/bag/satchel_ring.png          32x32 travelling gold ring   (pocket_icons palette)
  graphics/bag/satchel_thumb.png         8x16 scrollbar thumb         (pocket_icons palette)
  graphics/bag/satchel_arrow.png         8x16 small pocket arrow, points left (Gen 3 red)
  graphics/text_window/orchid.png        24x24 std window frame, Orchid theme
  src/data/item_menu_satchel.h           generated layout constants + pill row tilemap

usage: export_bag.py
"""
import os
from PIL import Image
from kit import *
import bag_screen as B
import windows as Wn
from backdrop import GRID_PAL, grid_tile_image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)


def save_indexed(im, path, pal):
    flat = [c for rgb in pal for c in rgb]
    out = im.copy()
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(path, transparency=0)


def pad16(pal):
    return list(pal) + [(0, 0, 0)] * (16 - len(pal))


def export_screen():
    # The tile layout is theme independent (indices are roles); export with male colours.
    bg = B.build_bg("male")
    tiles, tm = to_tiles(bg)
    n_screen = len(tiles)
    # BG3 grid: 16x16 -> 4 tiles appended, order TL TR BL BR
    g = grid_tile_image()
    gpx = g.load()
    grid_base = len(tiles)
    for ty in range(2):
        for tx in range(2):
            tiles.append(tuple(gpx[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(tiles) <= 256, "BG3 map at screenblock 28 overlaps tile 256+ of charblock 3"
    sheet = tiles_to_image(tiles, bg)
    save_indexed(sheet, P("graphics", "bag", "satchel_screen.png"), palette("male"))

    # 32x32 tilemap (30x20 visible)
    cells = [None] * (32 * 32)
    for i, item in enumerate(tm):
        cx, cy = i % 30, i // 30
        cells[cy * 32 + cx] = item
    write_tilemap(P("graphics", "bag", "satchel_screen.bin"), cells)

    for theme in ("male", "female"):
        base = palette(theme)
        pals = pad16(base) + pad16(B.variant(base, "selected")) + pad16(GRID_PAL)
        write_jasc(P("graphics", "bag", "satchel_screen_%s.pal" % theme), pals)

    # pill row: tilemap rows 2..3, cols PILL_COL..PILL_COL+PILL_COLS-1
    pill_col, pill_cols = B.PILL_X // 8, B.PILL_W // 8
    pill_row = []
    for ty in (2, 3):
        row = []
        for tx in range(pill_col, pill_col + pill_cols):
            idx, hf, vf = tm[ty * 30 + tx]
            row.append(idx | (hf << 10) | (vf << 11))
        pill_row.append(row)
    # sanity: every row identical
    for r in range(B.ROWS):
        for k, ty in enumerate((2 + 2 * r, 3 + 2 * r)):
            for j, tx in enumerate(range(pill_col, pill_col + pill_cols)):
                idx, hf, vf = tm[ty * 30 + tx]
                assert pill_row[k][j] == idx | (hf << 10) | (vf << 11), "pill rows differ"
    return n_screen, grid_base, pill_col, pill_cols, pill_row


def export_hm():
    src = Image.open(P("graphics", "bag", "hm.png"))
    remap = {1: INK, 10: TRANSPARENT, 11: INK_SOFT, 15: WHITE}
    out = Image.new("P", src.size, 0)
    sp, op = src.load(), out.load()
    for y in range(src.size[1]):
        for x in range(src.size[0]):
            op[x, y] = remap.get(sp[x, y], 0)
    save_indexed(out, P("graphics", "bag", "satchel_hm.png"), palette("male"))


def export_sprites():
    icons = Image.open(P("graphics", "bag", "pocket_icons.png"))
    ipal = [tuple(icons.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    # pocket_icons palette: 1 INK, 11 SELECT_DARK, 12 SELECT, 13 SELECT_LIGHT
    ring_im = Image.new("P", (32, 32), 0)
    rc = Canvas(ring_im)
    ring(rc, 16, 16, 12.5, 1)
    ring(rc, 16, 16, 11.5, 11)
    ring(rc, 16, 16, 10.5, 12)
    ring(rc, 16, 16, 9.5, 13)
    ring(rc, 16, 16, 8.5, 1)
    save_indexed(ring_im, P("graphics", "bag", "satchel_ring.png"), ipal)

    thumb = Image.new("P", (8, 16), 0)
    rounded_box(Canvas(thumb), 2, 0, 4, 12, 1, 12, 1, 13, 11)
    save_indexed(thumb, P("graphics", "bag", "satchel_thumb.png"), ipal)

    arrow = Image.new("P", (8, 16), 0)
    stamp(Canvas(arrow), 1, 3, SMALL_ARROW, {"F": 1, "O": 2})
    save_indexed(arrow, P("graphics", "bag", "satchel_arrow.png"), pad16([(0, 0, 0)] + [snap(c) for c in ARROW_RED]))


def export_frame():
    im = Wn.std_frame_tiles("orchid")
    save_indexed(im, P("graphics", "text_window", "orchid.png"), palette("orchid"))


def write_header(n_screen, grid_base, pill_col, pill_cols, pill_row):
    bc = B.button_centres()
    L = []
    L.append("// GENERATED by dev_scripts/orchid_ui/export_bag.py — do not edit by hand.")
    L.append("// Layout of the satchel bag screen (see dev_scripts/orchid_ui/DESIGN.md).")
    L.append("#ifndef GUARD_DATA_ITEM_MENU_SATCHEL_H")
    L.append("#define GUARD_DATA_ITEM_MENU_SATCHEL_H")
    L.append("")
    L.append("#define SATCHEL_SCREEN_NUM_TILES %d   // BG2 art tiles (incl. blank tile 0)" % n_screen)
    L.append("#define SATCHEL_GRID_TILE_BASE   %d   // BG3 grid: TL, TR, BL, BR" % grid_base)
    L.append("#define SATCHEL_PAL_NORMAL       0")
    L.append("#define SATCHEL_PAL_SELECTED     1")
    L.append("#define SATCHEL_PAL_GRID         2")
    L.append("")
    L.append("#define SATCHEL_LIST_ROWS        %d" % B.ROWS)
    L.append("#define SATCHEL_LIST_TOP_TILE    %d   // first tile row of the pill list" % (B.LIST_Y // 8))
    L.append("#define SATCHEL_PILL_COL         %d" % pill_col)
    L.append("#define SATCHEL_PILL_COLS        %d" % pill_cols)
    L.append("")
    L.append("#define SATCHEL_WHEEL_X          %d" % B.WHEEL_C[0])
    L.append("#define SATCHEL_WHEEL_Y          %d" % B.WHEEL_C[1])
    L.append("#define SATCHEL_BUTTON_RADIUS    %d" % B.BUTTON_R)
    L.append("#define SATCHEL_ICON_X           %d" % B.ICON_WELL_C[0])
    L.append("#define SATCHEL_ICON_Y           %d" % B.ICON_WELL_C[1])
    L.append("#define SATCHEL_ARROW_LEFT_X     %d" % B.POCKET_ARROWS[0][0])
    L.append("#define SATCHEL_ARROW_RIGHT_X    %d" % B.POCKET_ARROWS[1][0])
    L.append("#define SATCHEL_ARROW_Y          %d" % B.POCKET_ARROWS[0][1])
    x0, y0, x1, y1 = B.TRACK
    L.append("#define SATCHEL_TRACK_X          %d   // thumb sprite centre x" % ((x0 + x1 + 1) // 2))
    L.append("#define SATCHEL_TRACK_TOP        %d   // thumb top-most y (top edge)" % (y0 + 2))
    L.append("#define SATCHEL_TRACK_SPAN       %d   // thumb travel in px" % ((y1 - y0 - 3) - 12))
    L.append("")
    L.append("// Pocket button centres, POCKET_ITEMS .. POCKET_KEY_ITEMS, clockwise from the top.")
    L.append("// Angle (degrees, 0 = +x, clockwise on screen) of each button for the travelling ring.")
    L.append("static const s16 sSatchelButtonPos[][2] = {")
    for x, y in bc:
        L.append("    {%d, %d}," % (x, y))
    L.append("};")
    L.append("static const u16 sSatchelButtonAngle[] = {%s};" % ", ".join(str((270 + 72 * k) % 360) for k in range(5)))
    L.append("")
    L.append("// One pill row (2 tile rows) of BG2 tilemap entries, palette bits clear.")
    L.append("static const u16 sSatchelPillRow[2][SATCHEL_PILL_COLS] = {")
    for row in pill_row:
        L.append("    {" + ", ".join("0x%04X" % v for v in row) + "},")
    L.append("};")
    L.append("")
    L.append("#endif // GUARD_DATA_ITEM_MENU_SATCHEL_H")
    with open(P("src", "data", "item_menu_satchel.h"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    res = export_screen()
    export_hm()
    export_sprites()
    export_frame()
    write_header(*res)
    print("BG2 tiles: %d, grid base: %d, pill cols %d..%d" % (res[0], res[1], res[2], res[2] + res[3] - 1))
