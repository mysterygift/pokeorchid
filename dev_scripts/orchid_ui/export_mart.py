"""
Export the Orchid Poké Mart buy screen (approved direction A, "Counter & awning") to game assets.
Every piece is drawn with the mockup's own code (mock_mart.py / mart_ext.py), so ROM art == mock art.

BG layout (src/shop.c):
  BG0  text windows (money, list, description, message, YES/NO)        charblock 2 (+3)   prio 1
  BG1  the hanging quantity tag: a window whose pixels start as the tag art, text printed on it
                                                                          charblock 2 (+3)   prio 0
  BG2  shop art: awning, money sign, wall shelf, counter, pill rows + price tags, track, card
                                                                          charblock 0        prio 2
  BG3  scrolling grid                                                     charblock 0        prio 3

BG palettes: 0 kit (SPARE_A/B = price-tag manila), 1 = selected-row swap of 0, 2 SHOP (wood / Mart blue /
brass), 3 grid, 4 GOODS (wall-shelf stock), 15 = Orchid window palette (message box + YES/NO; export_yesno).

Writes (under the repo root):
  graphics/shop/orchid/bg_tiles.png    BG2 + BG3 tiles: static art, pill-row variants, grid (2x2)
  graphics/shop/orchid/bg.bin          BG2 static tilemap 32x32 (pill area empty, rows drawn at runtime)
  graphics/shop/orchid/bg.pal          BG palettes 0-4 (80 colours)
  graphics/shop/orchid/qty_tag.png     BG1 window pixels (15x6 tiles, row-major): the quantity tag
  graphics/shop/orchid/msg_frame.png   BG0 tiles of the Orchid dialogue box frame (Orchid window palette)
  graphics/shop/orchid/thumb.png       OBJ 8x16 scroll thumb            \
  graphics/shop/orchid/chevrons.png    OBJ 16x8 x2: up, down             } one OBJ palette (obj.pal)
  graphics/shop/orchid/coin.png        OBJ 16x16 picker coin            /
  graphics/shop/orchid/obj.pal
  graphics/shop/orchid/tm_discs.png    OBJ 16x16 x6: TM disc for list row k drawn with colours 4+2k / 5+2k;
                                       shop.c builds the palette from each row's type (*_tm_hm.pal [6], [9])
  src/data/shop_orchid.h               layout constants, pill-row variants, message frame map

usage: export_mart.py
"""
import os
from PIL import Image
from kit import *
import mart_ext as M
import mock_mart as MM
import windows as Wn
from mart_ext import s, BRASS_DARK, BRASS, BRASS_LIGHT
from backdrop import GRID_PAL, grid_tile_image
from gamefont import text_width
import export_yesno as EY

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "shop", "orchid")
HEADER = os.path.join(ROOT, "src", "data", "shop_orchid.h")
COLS, ROWS = 30, 20

PILL_COL0, PILL_COLS = MM.A_LIST_X // 8, MM.A_PILL_W // 8          # 13, 16
LIST_ROW0 = MM.A_LIST_Y // 8                                        # 2
TAG_W_MIN = 44                                                      # mock_mart.a_tag_w
TAG_W_MAX = max(text_width("¥999999", "narrow"), text_width("SOLD OUT", "narrow")) + 18  # 6 digits / SOLD OUT

# BG1 quantity-tag window (covers the tag; the rest of the window is transparent)
QTY_WIN = (14, 8, 15, 6)                                            # tile x, y, w, h
# message box: Wn.dialogue_box(2, 15, 27, 4); the text window is one tile narrower (26) so the right
# end-cap, which reaches 1px into the 27th column, stays frame art
MSG_WIN = (2, 15, 26, 4)
MSG_FRAME_ROWS = (14, 19)


def save_indexed(im, path, pal):
    flat = [c for rgb in pal for c in rgb]
    out = im.copy()
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(path, transparency=0)


def pad16(p):
    return list(p) + [(0, 0, 0)] * (16 - len(p))


def rgb555(c):
    return "RGB(%d, %d, %d)" % (c[0] // 8, c[1] // 8, c[2] // 8)


# ---------------------------------------------------------------- tiler (flip dedupe, like export_pc)
class Tiler:
    def __init__(self):
        self.tiles = [tuple([0] * 64)]
        self.lookup = {self.tiles[0]: 0}

    def add(self, t):
        if t in self.lookup:
            return self.lookup[t]
        for hf, vf in ((1, 0), (0, 1), (1, 1)):
            f = tuple(t[(7 - y if vf else y) * 8 + (7 - x if hf else x)] for y in range(8) for x in range(8))
            if f in self.lookup:
                return self.lookup[f] | (hf << 10) | (vf << 11)
        i = len(self.tiles)
        self.tiles.append(t)
        self.lookup[t] = i
        return i

    def cell(self, art, cx, cy):
        """Tilemap entry for one cell of a two-palette art sheet (value = block * 16 + role)."""
        px = art.load()
        vals = [px[cx * 8 + x, cy * 8 + y] for y in range(8) for x in range(8)]
        blocks = {v // 16 for v in vals if v}
        if not blocks:
            return 0
        assert len(blocks) == 1, "cell (%d,%d) mixes palettes %s" % (cx, cy, blocks)
        blk = blocks.pop()
        assert blk in (0, 2, 4), "unexpected palette block %d" % blk
        return self.add(tuple(v % 16 for v in vals)) | (blk << 12)


def tiles_png(tiles, path, pal):
    per_row = 16
    rows = (len(tiles) + per_row - 1) // per_row
    im = Image.new("P", (per_row * 8, rows * 8), 0)
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % per_row) * 8, (i // per_row) * 8
        for j, c in enumerate(t):
            px[ox + j % 8, oy + j // 8] = c
    save_indexed(im, path, pal)


# ---------------------------------------------------------------- BG2: static art + pill rows + grid
def static_art():
    art = M.art_sheet()
    MM.a_art(Canvas(art), MM.st_defaults(), 0)          # no pill rows: drawn per row at runtime
    return art


def pill_art(tag_w):
    """One list row (row 0) as drawn by mock_mart: pill, plus the price tag when tag_w is set."""
    art = M.art_sheet()
    cv = Canvas(art)
    y = MM.A_LIST_Y + 1
    rounded_box(cv, MM.A_LIST_X, y, MM.A_PILL_W, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    if tag_w:
        M.price_tag(cv, MM.A_LIST_X + MM.A_PILL_W - tag_w - 2, y + 1, tag_w, 12)
    return art


def export_bg():
    T = Tiler()
    art = static_art()
    n_conf = len(M.check_tiles(art)[1])
    assert n_conf == 0
    tm = [0] * (32 * 32)
    for cy in range(ROWS):
        for cx in range(COLS):
            e = T.cell(art, cx, cy)
            if PILL_COL0 <= cx < PILL_COL0 + PILL_COLS and LIST_ROW0 <= cy < LIST_ROW0 + 2 * MM.A_ROWS:
                assert e == 0, "static art inside the pill area at (%d,%d)" % (cx, cy)
            tm[cy * 32 + cx] = e
    n_static = len(T.tiles)
    # pill rows: variant 0 = plain pill (CANCEL), variant k = pill + tag of width TAG_W_MIN + k - 1
    variants = []
    for w in [0] + list(range(TAG_W_MIN, TAG_W_MAX + 1)):
        a = pill_art(w)
        rows = []
        for cy in (LIST_ROW0, LIST_ROW0 + 1):
            rows.append([T.cell(a, cx, cy) for cx in range(PILL_COL0, PILL_COL0 + PILL_COLS)])
        variants.append(rows)
    n_art = len(T.tiles)
    grid_base = n_art
    g = grid_tile_image().load()
    for ty in range(2):
        for tx in range(2):
            T.tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(T.tiles) <= 512, "BG2/BG3 share charblock 0 (512 tiles)"
    tiles_png(T.tiles, os.path.join(OUT, "bg_tiles.png"), M.p0())
    with open(os.path.join(OUT, "bg.bin"), "wb") as f:
        for e in tm:
            f.write(bytes((e & 0xFF, e >> 8)))
    pals = pad16(M.p0()) + pad16(M.p1()) + pad16(M.shop_pal()) + pad16(GRID_PAL) + pad16(M.goods_pal())
    write_jasc(os.path.join(OUT, "bg.pal"), pals)
    return dict(n_static=n_static, n_art=n_art, grid_base=grid_base, variants=variants)


# ---------------------------------------------------------------- BG1: quantity tag window pixels
def export_qty_tag():
    art = M.art_sheet()
    cv = Canvas(art)
    q = MM.a_qty(None, cv, MM.st_defaults(cursor=0, mode="qty", qty=1))
    tx, ty, tw, th = QTY_WIN
    crop = art.crop((tx * 8, ty * 8, (tx + tw) * 8, (ty + th) * 8))
    px = crop.load()
    out = Image.new("P", crop.size, 0)
    op = out.load()
    for y in range(crop.size[1]):
        for x in range(crop.size[0]):
            v = px[x, y]
            assert v < 16, "quantity tag uses palette block %d" % (v // 16)
            op[x, y] = v
    # nothing of the tag outside the window
    full = art.load()
    for y in range(160):
        for x in range(240):
            if full[x, y]:
                assert tx * 8 <= x < (tx + tw) * 8 and ty * 8 <= y < (ty + th) * 8, (x, y)
    save_indexed(out, os.path.join(OUT, "qty_tag.png"), M.p0())
    return q


# ---------------------------------------------------------------- BG0: Orchid dialogue box frame
def export_msg_frame():
    sheet = new_sheet(240, 160)
    Wn.dialogue_box(Canvas(sheet), 2, 15, 27, 4)
    remap = dict(EY.REMAP)
    remap[PANEL_SHADE] = 3
    px = sheet.load()
    T = Tiler()
    wx, wy, ww, wh = MSG_WIN
    frame = []
    for cy in range(MSG_FRAME_ROWS[0], MSG_FRAME_ROWS[1] + 1):
        row = []
        for cx in range(COLS):
            vals = [remap[px[cx * 8 + x, cy * 8 + y]] for y in range(8) for x in range(8)]
            inside = wx <= cx < wx + ww and wy <= cy < wy + wh
            if inside:
                assert set(vals) == {1}, "message window cell (%d,%d) is not plain fill" % (cx, cy)
                row.append(None)
            else:
                row.append(T.add(tuple(vals)) if any(vals) else 0)
        frame.append(row)
    tiles_png(T.tiles, os.path.join(OUT, "msg_frame.png"), EY.window_palette())
    return len(T.tiles), frame


# ---------------------------------------------------------------- OBJ pieces
OBJ_PAL = pad16([(0, 0, 0)] + [snap(c) for c in (
    (40, 40, 64),                                          # 1 INK
    (216, 128, 32), (248, 208, 88), (248, 240, 168),       # 2-4 gold (thumb)
    M.ARROW_RED[1], M.ARROW_RED[0],                        # 5-6 chevron outline / fill
    (160, 104, 40), (216, 168, 72), (248, 224, 144),       # 7-9 brass (coin)
)])


def quantize(rgba, pal, size):
    """Mock RGBA piece -> indices of pal (exact colour match), placed top-left in a sheet of size."""
    out = Image.new("P", size, 0)
    op, ip = out.load(), rgba.load()
    look = {c: i for i, c in enumerate(pal) if i}
    for y in range(rgba.size[1]):
        for x in range(rgba.size[0]):
            r, g, b, a = ip[x, y]
            if a:
                assert (r, g, b) in look, "colour %s not in the OBJ palette" % ((r, g, b),)
                op[x, y] = look[(r, g, b)]
    return out


def export_obj():
    thumb = quantize(M.thumb(), OBJ_PAL, (8, 16))
    save_indexed(thumb, os.path.join(OUT, "thumb.png"), OBJ_PAL)
    chev = Image.new("P", (16, 16), 0)
    chev.paste(quantize(M.chevron("up"), OBJ_PAL, (16, 8)), (0, 0))
    chev.paste(quantize(M.chevron("down"), OBJ_PAL, (16, 8)), (0, 8))
    save_indexed(chev, os.path.join(OUT, "chevrons.png"), OBJ_PAL)
    c = M.art_sheet(16, 16)
    M.coin(Canvas(c), 6, 6)
    save_indexed(quantize(MM._rgba(c, MM.st_defaults()), OBJ_PAL, (16, 16)), os.path.join(OUT, "coin.png"), OBJ_PAL)
    write_jasc(os.path.join(OUT, "obj.pal"), OBJ_PAL)
    # TM discs: mart_ext.tm_disc drawn with row slot k's colour pair (4 + 2k, 5 + 2k)
    discs = Image.new("P", (16, 16 * 6), 0)
    for k in range(6):
        d = Image.new("P", (16, 16), 0)
        cv = Canvas(d)
        disc(cv, 6, 6, 5.5, 4 + 2 * k, 1, 2, 5 + 2 * k)
        disc(cv, 6, 6, 1.6, 2, 1)
        discs.paste(d, (0, 16 * k))
    save_indexed(discs, os.path.join(OUT, "tm_discs.png"), M.tm_disc_pal())


# ---------------------------------------------------------------- header
def write_header(bg, q, n_msg, msg_frame):
    L = []
    A = L.append
    A("// GENERATED by dev_scripts/orchid_ui/export_mart.py - do not edit by hand.")
    A("// Orchid Poké Mart buy screen (mock_mart.py direction A, 'Counter & awning').")
    A("#ifndef GUARD_DATA_SHOP_ORCHID_H")
    A("#define GUARD_DATA_SHOP_ORCHID_H")
    A("")
    A("#define OSHOP_PAL_KIT        0   // BG: Orchid kit, SPARE_A/B = price-tag manila")
    A("#define OSHOP_PAL_SELECTED   1   // BG: selected pill row (gold)")
    A("#define OSHOP_PAL_GRID       3")
    A("#define OSHOP_NUM_BG_PALS    5")
    A("#define OSHOP_GRID_TILE      %d  // BG3 grid tiles TL, TR, BL, BR" % bg["grid_base"])
    A("")
    A("// pill list (BG2 rows, BG0 text window on top)")
    A("#define OSHOP_LIST_ROWS      %d" % MM.A_ROWS)
    A("#define OSHOP_LIST_X         %d" % MM.A_LIST_X)
    A("#define OSHOP_LIST_Y         %d" % MM.A_LIST_Y)
    A("#define OSHOP_PILL_COL       %d" % PILL_COL0)
    A("#define OSHOP_PILL_COLS      %d" % PILL_COLS)
    A("#define OSHOP_LIST_ROW_TILE  %d" % LIST_ROW0)
    A("#define OSHOP_NAME_X         7   // name x in the list window")
    A("#define OSHOP_NAME_X_TM      21  // TM rows: after the type disc")
    A("#define OSHOP_PRICE_RIGHT    %d  // price right edge in the list window" % (MM.A_PILL_W - 2 - 6))
    A("#define OSHOP_TAG_W_MIN      %d" % TAG_W_MIN)
    A("#define OSHOP_TAG_W_MAX      %d" % TAG_W_MAX)
    A("#define OSHOP_TAG_PAD        18  // tag width = widest price + 18 (mock_mart.a_tag_w)")
    A("#define OSHOP_TM_DISC_X      %d  // disc sprite top-left x; y = row top + 2" % (MM.A_LIST_X + 5))
    x0, y0, x1, y1 = MM.A_TRACK
    A("#define OSHOP_THUMB_X        %d  // thumb sprite top-left x" % (x0 + 1))
    A("#define OSHOP_TRACK_Y0       %d" % y0)
    A("#define OSHOP_THUMB_SPAN     %d  // mart_ext.thumb_y" % ((y1 - y0 - 3) - 12))
    A("")
    A("// money sign (text right-aligned), item on the counter, clerk, description card")
    A("#define OSHOP_MONEY_RIGHT    80")
    A("#define OSHOP_MONEY_Y        21")
    A("#define OSHOP_ICON_X         %d  // visible centre of the item on the counter" % MM.A_ICON_C[0])
    A("#define OSHOP_ICON_Y         %d" % MM.A_ICON_C[1])
    A("#define OSHOP_BONUS_DX       16  // bonus Premier Ball beside it")
    A("#define OSHOP_BONUS_DY       2")
    A("#define OSHOP_CLERK_X        %d  // clerk sprite top-left (16x32)" % MM.A_CLERK[0])
    A("#define OSHOP_CLERK_BOTTOM   %d" % (MM.A_CLERK[1] + 32))
    A("#define OSHOP_DESC_X         %d" % MM.A_DESC[0])
    A("#define OSHOP_DESC_Y         %d" % MM.A_DESC[1])
    A("")
    tx, ty, tw, th = QTY_WIN
    A("// quantity tag (BG1 window at tile %d,%d, %dx%d)" % QTY_WIN)
    A("#define OSHOP_QTY_WIN_X      %d" % tx)
    A("#define OSHOP_QTY_WIN_Y      %d" % ty)
    A("#define OSHOP_QTY_WIN_W      %d" % tw)
    A("#define OSHOP_QTY_WIN_H      %d" % th)
    ox, oy = tx * 8, ty * 8
    A("#define OSHOP_QTY_CENTRE_X   %d  // window coords" % (q["q"][0] - ox))
    A("#define OSHOP_QTY_Y          %d" % (q["q"][1] - oy))
    A("#define OSHOP_QTY_RIGHT      %d" % (q["tot"][0] - ox))
    A("#define OSHOP_TOTAL_Y        %d" % (q["tot"][1] - oy))
    A("#define OSHOP_LEFT_Y         %d" % (q["left"][1] - oy))
    A("#define OSHOP_COIN_X         %d  // screen, sprite top-left" % q["coin"][0])
    A("#define OSHOP_COIN_Y         %d" % q["coin"][1])
    cx, yu, yd = q["chev"]
    A("#define OSHOP_CHEV_X         %d  // screen, sprite top-left" % (cx - 4))
    A("#define OSHOP_CHEV_UP_Y      %d" % yu)
    A("#define OSHOP_CHEV_DOWN_Y    %d" % yd)
    A("")
    A("// message box: Orchid dialogue frame over the text window at (%d,%d) %dx%d" % MSG_WIN)
    A("#define OSHOP_MSG_WIN_X      %d" % MSG_WIN[0])
    A("#define OSHOP_MSG_WIN_Y      %d" % MSG_WIN[1])
    A("#define OSHOP_MSG_WIN_W      %d" % MSG_WIN[2])
    A("#define OSHOP_MSG_WIN_H      %d" % MSG_WIN[3])
    A("#define OSHOP_MSG_FRAME_TOP  %d" % MSG_FRAME_ROWS[0])
    A("#define OSHOP_MSG_FRAME_ROWS %d" % (MSG_FRAME_ROWS[1] - MSG_FRAME_ROWS[0] + 1))
    A("#define OSHOP_MSG_FRAME_TILES %d" % n_msg)
    A("#define OSHOP_MSG_SKIP       0xFFFF  // text window cell")
    A("")
    A("// TM disc palette: neutrals; colours 4 + 2k / 5 + 2k come from list row k's *_tm_hm.pal [6] / [9]")
    A("static const u16 sOrchidShopTmDiscNeutrals[4] = {%s};" % ", ".join(rgb555(c) for c in M.tm_disc_pal()[:4]))
    A("")
    nv = len(bg["variants"])
    A("// BG2 pill rows (2 tile rows x %d), palette bits = OSHOP_PAL_KIT: [0] plain pill (CANCEL)," % PILL_COLS)
    A("// [1 + w - OSHOP_TAG_W_MIN] pill + price tag of width w")
    A("#define OSHOP_NUM_PILL_VARIANTS %d" % nv)
    A("static const u16 sOrchidShopPillRows[OSHOP_NUM_PILL_VARIANTS][2][OSHOP_PILL_COLS] = {")
    for v in bg["variants"]:
        A("    {")
        for row in v:
            A("        {" + ", ".join("0x%04X" % e for e in row) + "},")
        A("    },")
    A("};")
    A("")
    A("// Message frame tilemap (rows %d..%d, all 30 columns), tile numbers relative to the frame tiles" % MSG_FRAME_ROWS)
    A("static const u16 sOrchidShopMsgFrame[OSHOP_MSG_FRAME_ROWS][30] = {")
    for row in msg_frame:
        A("    {" + ", ".join("OSHOP_MSG_SKIP" if e is None else "0x%04X" % e for e in row) + "},")
    A("};")
    A("")
    A("#endif // GUARD_DATA_SHOP_ORCHID_H")
    with open(HEADER, "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    bg = export_bg()
    q = export_qty_tag()
    n_msg, frame = export_msg_frame()
    export_obj()
    write_header(bg, q, n_msg, frame)
    print("BG2: %d static tiles, %d with pill variants (%d variants, tag %d..%d px), grid at %d"
          % (bg["n_static"], bg["n_art"], len(bg["variants"]), TAG_W_MIN, TAG_W_MAX, bg["grid_base"]))
    print("message frame: %d tiles" % n_msg)


if __name__ == "__main__":
    main()
