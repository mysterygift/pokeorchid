"""
Export the Orchid Trainer Card (approved, mock_card.py / card_ext.py) to game assets.
Every piece is drawn with the mockup's own code, so ROM art == mock art.

BG layout (src/trainer_card.c, Orchid path = the player's own card outside the Union Room):
  BG0  card art: shell, header tab + star pips, ID pill, nameplate, icon pills, dais,
       badge case + sockets / back rows + signature well          charblock 0   prio 2
  BG1  one text window over the card (card palette)                charblock 2   prio 0
  BG2  scrolling grid (grid tiles appended to the BG0 tiles)       charblock 0   prio 3
  BG3  earned badges (pre-shifted to their sockets) + trainer pic  charblock 1   prio 1
The flip writes the same per-scanline VOFS to BG0, BG1 and BG3, so the whole card folds.

The BG0 tilemaps are composed at runtime from:
  * a full front map (with / without the POKéDEX row) and a full back map (no stat rows),
    all drawn with 0 stars and no badges,
  * the header pip patch for 0-4 stars (same cells on both sides),
  * one "earned" patch per badge socket (the inner shadow ring goes away),
  * one 2-tile-row strip per back-row icon, placed at row slot k (tile rows 4 + 2k, 5 + 2k).
Tier and gender are palette-only (card.pal = 5 male tiers, 5 female tiers, then the grid).

Writes (under the repo root):
  graphics/trainer_card/orchid/tiles.png    BG0 tiles (all variants) + 4 grid tiles
  graphics/trainer_card/orchid/badges.png   BG3 tiles: badge k already shifted to socket k
                                            (badges.png palette)
  graphics/trainer_card/orchid/card.pal     11 BG palettes
  src/data/trainer_card_orchid.h            layout constants, tilemaps and patches

usage: export_card.py
"""
import os
from PIL import Image
from kit import *
import card_ext as C
import mock_card as M
from backdrop import GRID_PAL, grid_tile_image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "trainer_card", "orchid")
HEADER = os.path.join(ROOT, "src", "data", "trainer_card_orchid.h")
COLS, ROWS = 30, 20

# back-row icon strips, in the order trainer_card.c uses them (ORCHID_CARD_ROW_*)
ROW_ICONS = ["hof", "link", "trade", "union", "berry", "contest"]
ROW_KEYS = {"hof": ("hof", (31, 9, 46)), "link": ("link", (12, 5)), "trade": ("trades", 8),
            "union": ("union", 23), "berry": ("berry", 1250), "contest": ("contests", 3)}
NO_ROWS = dict(hof=None, link=None, trades=0, union=0, berry=0, contests=0)

# BG3: trainer pic window (tiles) - covers the pic of either gender (asserted below)
PIC_WIN = (18, 2, 9, 10)          # left, top, w, h
PIC_BASE_BLOCK = 0x60             # after the badge tiles (asserted)
TEXT_WIN = (1, 1)                 # BG1 card text window origin (tiles), 28x18 as vanilla


def pad16(p):
    return list(p) + [(0, 0, 0)] * (16 - len(p))


class Tiler:
    """Single-palette tile set with GBA flip dedupe."""

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

    def tilemap(self, im):
        px = im.load()
        tm = []
        for cy in range(ROWS):
            for cx in range(COLS):
                vals = tuple(px[cx * 8 + x, cy * 8 + y] for y in range(8) for x in range(8))
                assert max(vals) < 16, "cell (%d,%d) uses a colour outside the card palette" % (cx, cy)
                tm.append(self.add(vals))
        return tm


def save_indexed(tiles, path, pal):
    per_row = 16
    rows = (len(tiles) + per_row - 1) // per_row
    im = Image.new("P", (per_row * 8, rows * 8), 0)
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % per_row) * 8, (i // per_row) * 8
        for j, c in enumerate(t):
            px[ox + j % 8, oy + j // 8] = c
    im.save(path, transparency=0)


# ---------------------------------------------------------------- art renders (mock code)
def front(**kw):
    im = C.card_sheet(M.W, M.H)
    M.draw_front_art(Canvas(im), dict(M.HERO, **dict(dict(stars=0, badges=0), **kw)))
    return im


def back(**kw):
    im = C.card_sheet(M.W, M.H)
    M.draw_back_art(Canvas(im), dict(M.HERO, **dict(NO_ROWS, **dict(dict(stars=0), **kw))))
    return im


def diff_cells(a, b):
    return {i for i, (x, y) in enumerate(zip(a, b)) if x != y}


def rect_of(cells):
    xs = [i % COLS for i in cells]
    ys = [i // COLS for i in cells]
    return min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1


def rect_entries(tm, r):
    x, y, w, h = r
    return [[tm[(y + j) * COLS + x + i] for i in range(w)] for j in range(h)]


def in_rect(i, r):
    x, y, w, h = r
    return x <= i % COLS < x + w and y <= i // COLS < y + h


def export_bg0():
    T = Tiler()
    f_dex = T.tilemap(front(has_dex=True))
    f_nodex = T.tilemap(front(has_dex=False))
    b_base = T.tilemap(back())

    # star pips (header): one rect, an entry set per star count, identical on the back
    star_maps = [T.tilemap(front(has_dex=True, stars=s)) for s in range(5)]
    cells = set()
    for s in range(5):
        cells |= diff_cells(f_dex, star_maps[s])
    pip_rect = rect_of(cells)
    pips = []
    for s in range(5):
        bm = T.tilemap(back(stars=s))
        nd = T.tilemap(front(has_dex=False, stars=s))
        for other, base in ((bm, b_base), (nd, f_nodex)):
            for i in diff_cells(other, base):
                assert in_rect(i, pip_rect), "star change outside the pip rect"
            assert rect_entries(other, pip_rect) == rect_entries(star_maps[s], pip_rect)
        pips.append(rect_entries(star_maps[s], pip_rect))

    # badge sockets: badge k earned (others empty) -> rect + entries per socket
    sockets = []
    prev = f_dex
    for k in range(8):
        cur = T.tilemap(front(has_dex=True, badges=k + 1))
        d = diff_cells(prev, cur)
        r = rect_of(d)
        for (r2, _) in sockets:
            assert not (r[0] < r2[0] + r2[2] and r2[0] < r[0] + r[2] and r[1] < r2[1] + r2[3] and r2[1] < r[1] + r[3]), \
                "socket patches overlap"
        sockets.append((r, rect_entries(cur, r)))
        prev = cur
    # the case is identical without the POKéDEX row
    for (r, _) in sockets:
        assert rect_entries(f_nodex, r) == rect_entries(f_dex, r)

    # back rows: one strip per icon (tile rows 4, 5 of slot 0); slot-invariant
    row0 = (M.BACK_ROWS_Y0) // 8
    assert M.BACK_PITCH == 16 and (M.BACK_ROWS_Y0 % 8) + M.BACK_ROW_H <= 16
    for k in range(6):
        for c in range(COLS):
            for j in range(2):
                assert b_base[(row0 + 2 * k + j) * COLS + c] == b_base[(row0 + j) * COLS + c], "back face not uniform"
    strips = []
    for ic in ROW_ICONS:
        key, val = ROW_KEYS[ic]
        tm = T.tilemap(back(**{key: val}))
        for i in diff_cells(tm, b_base):
            assert row0 <= i // COLS < row0 + 2, "row %s spills outside its strip" % ic
        strips.append([[tm[(row0 + j) * COLS + c] for c in range(COLS)] for j in range(2)])
    champ = T.tilemap(back(**{k: v for k, v in ROW_KEYS.values()}))
    for k, ic in enumerate(ROW_ICONS):
        for j in range(2):
            assert [champ[(row0 + 2 * k + j) * COLS + c] for c in range(COLS)] == strips[k][j], "slot %d" % k
    # 6 rows end above the signature well
    assert row0 + 12 <= M.SIG[1] // 8

    n_art = len(T.tiles)
    grid_base = n_art
    g = grid_tile_image().load()
    for ty in range(2):
        for tx in range(2):
            T.tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    assert len(T.tiles) <= 512, "BG0 + grid must fit charblock 0"
    save_indexed(T.tiles, os.path.join(OUT, "tiles.png"), C.card_palette("male", 0))
    return dict(f_dex=f_dex, f_nodex=f_nodex, back=b_base, pip_rect=pip_rect, pips=pips,
                sockets=sockets, row0=row0, strips=strips, n_art=n_art, grid_base=grid_base,
                n_tiles=len(T.tiles))


# ---------------------------------------------------------------- BG3 badges
def export_badges():
    src = Image.open(G_("trainer_card", "badges.png"))
    pal = [snap(tuple(src.getpalette()[k * 3:k * 3 + 3])) for k in range(16)]
    T = Tiler()
    out = []
    for k in range(8):
        sheet = Image.new("P", (M.W, M.H), 0)
        cx, cy = M.SOCK_X0 + k * M.SOCK_PITCH, M.SOCK_Y
        x0, y0 = cx - 8, cy - 8
        sheet.paste(src.crop((k * 16, 0, k * 16 + 16, 16)), (x0, y0))
        px = sheet.load()
        r = (x0 // 8, y0 // 8, (x0 + 15) // 8 - x0 // 8 + 1, (y0 + 15) // 8 - y0 // 8 + 1)
        ent = []
        for j in range(r[3]):
            row = []
            for i in range(r[2]):
                ccx, ccy = r[0] + i, r[1] + j
                vals = tuple(px[ccx * 8 + x, ccy * 8 + y] for y in range(8) for x in range(8))
                row.append(T.add(vals) if any(vals) else 0)
            ent.append(row)
        out.append((r, ent))
    assert len(T.tiles) <= PIC_BASE_BLOCK, "badge tiles run into the trainer pic window"
    save_indexed(T.tiles, os.path.join(OUT, "badges.png"), pal)
    return out, len(T.tiles)


def G_(*p):
    return os.path.join(ROOT, "graphics", *p)


# ---------------------------------------------------------------- trainer pic placement
def pic_positions():
    stage = M.DAIS_C[1] + int(M.DAIS_IN * 0.55)
    wx, wy, ww, wh = PIC_WIN
    res = {}
    for g in ("male", "female"):
        pic, _ = C.trainer_pic(g)
        bb = pic.getbbox()
        x, y = M.DAIS_C[0] - 32, stage + 3 - bb[3]
        # the visible pixels must be inside the window
        assert wx * 8 <= x + bb[0] and x + bb[2] <= (wx + ww) * 8, (g, x, bb)
        assert wy * 8 <= y + bb[1] and y + bb[3] <= (wy + wh) * 8, (g, y, bb)
        res[g] = (x - wx * 8, y - wy * 8)
    # no overlap with the badges (BG3)
    assert wy + wh <= (M.SOCK_Y - 8) // 8
    return res


# ---------------------------------------------------------------- palettes
def export_pal():
    pals = []
    for theme in ("male", "female"):
        for t in range(5):
            pals += pad16(C.card_palette(theme, t))
    pals += pad16(GRID_PAL)
    write_jasc(os.path.join(OUT, "card.pal"), pals)


# ---------------------------------------------------------------- header
def arr2(rows):
    return "{" + ", ".join("{" + ", ".join("0x%04X" % e for e in r) + "}" for r in rows) + "}"


def write_header(bg, badges, n_badge_tiles, pics):
    L = []
    A = L.append
    tx, ty = TEXT_WIN
    ox, oy = tx * 8, ty * 8
    A("// GENERATED by dev_scripts/orchid_ui/export_card.py - do not edit by hand.")
    A("// Orchid Trainer Card (mock_card.py / card_ext.py).")
    A("#ifndef GUARD_DATA_TRAINER_CARD_ORCHID_H")
    A("#define GUARD_DATA_TRAINER_CARD_ORCHID_H")
    A("")
    A("// BG palettes (graphics/trainer_card/orchid/card.pal): [gender * 5 + stars], then the grid")
    A("#define OCARD_PAL_CARD        0")
    A("#define OCARD_PAL_BADGES      1")
    A("#define OCARD_PAL_GRID        2")
    A("#define OCARD_PAL_PIC         8")
    A("#define OCARD_NUM_TIERS       5")
    A("#define OCARD_GRID_PAL_INDEX  10   // palette index of the grid inside card.pal")
    A("")
    A("// BG0 tiles (tiles.png): %d art tiles, then the grid TL, TR, BL, BR" % bg["n_art"])
    A("#define OCARD_NUM_TILES       %d" % bg["n_tiles"])
    A("#define OCARD_GRID_TILE       %d" % bg["grid_base"])
    A("// BG3 tiles (badges.png): %d; the trainer pic window follows" % n_badge_tiles)
    A("#define OCARD_NUM_BADGE_TILES %d" % n_badge_tiles)
    wx, wy, ww, wh = PIC_WIN
    A("#define OCARD_PIC_WIN_X       %d" % wx)
    A("#define OCARD_PIC_WIN_Y       %d" % wy)
    A("#define OCARD_PIC_WIN_W       %d" % ww)
    A("#define OCARD_PIC_WIN_H       %d" % wh)
    A("#define OCARD_PIC_BASE_BLOCK  0x%X" % PIC_BASE_BLOCK)
    A("#define OCARD_PIC_X_MALE      %d   // 64x64 pic top-left inside the window" % pics["male"][0])
    A("#define OCARD_PIC_Y_MALE      %d" % pics["male"][1])
    A("#define OCARD_PIC_X_FEMALE    %d" % pics["female"][0])
    A("#define OCARD_PIC_Y_FEMALE    %d" % pics["female"][1])
    A("")
    A("// Text (BG1 window at tile %d,%d; coordinates are window pixels)" % TEXT_WIN)
    A("#define OCARD_TEXT_WIN_X      %d" % tx)
    A("#define OCARD_TEXT_WIN_Y      %d" % ty)
    A("#define OCARD_TITLE_X         %d" % (M.TITLE[0] - ox))
    A("#define OCARD_TITLE_Y         %d" % (M.TITLE[1] - oy))
    x, y, w, cap = M.ID_PILL
    A("#define OCARD_ID_X            %d   // pill left; label centred in the cap (+1), number in the rest" % (x - ox))
    A("#define OCARD_ID_Y            %d" % (y - 1 - oy))
    A("#define OCARD_ID_W            %d" % w)
    A("#define OCARD_ID_CAP          %d" % cap)
    A("#define OCARD_COL_X           %d" % (M.COL_X - ox))
    A("#define OCARD_COL_W           %d" % M.COL_W)
    A("#define OCARD_NAME_Y          %d" % (M.NAME_Y - oy))
    A("#define OCARD_VALUE_RIGHT     %d   // front values end here" % (M.COL_X + M.COL_W - 7 - ox))
    A("static const u8 sOrchidCardRowY[3] = {%s};" % ", ".join(str(v - oy) for v in M.ROWS_Y))
    A("#define OCARD_BACK_LABEL_X    %d" % (M.COL_X + 25 - ox))
    A("#define OCARD_BACK_VALUE_RIGHT %d" % (M.COL_X + M.SIG[2] - 7 - ox))
    A("#define OCARD_BACK_ROW_Y0     %d   // + k * OCARD_BACK_PITCH" % (M.BACK_ROWS_Y0 - 1 - oy))
    A("#define OCARD_BACK_PITCH      %d" % M.BACK_PITCH)
    A("#define OCARD_BACK_MAX_ROWS   6")
    A("#define OCARD_SIG_NAME_X      %d" % (M.SIG[0] + 26 - ox))
    A("#define OCARD_SIG_NAME_Y      %d" % (M.SIG[1] - 1 - oy))
    A("")
    A("// BG0 full maps (30x20), 0 stars, no badges")
    for name, tm in (("sOrchidCardFrontDex", bg["f_dex"]), ("sOrchidCardFrontNoDex", bg["f_nodex"]),
                     ("sOrchidCardBack", bg["back"])):
        A("static const u16 %s[20 * 30] = {" % name)
        for r in range(ROWS):
            A("    " + ", ".join("0x%04X" % e for e in tm[r * COLS:(r + 1) * COLS]) + ",")
        A("};")
    A("")
    px, py, pw, ph = bg["pip_rect"]
    A("// star pips: cells (%d,%d) %dx%d, per star count (both sides)" % bg["pip_rect"])
    A("#define OCARD_PIP_X %d" % px)
    A("#define OCARD_PIP_Y %d" % py)
    A("#define OCARD_PIP_W %d" % pw)
    A("#define OCARD_PIP_H %d" % ph)
    A("static const u16 sOrchidCardPips[OCARD_NUM_TIERS][OCARD_PIP_H][OCARD_PIP_W] = {")
    for p in bg["pips"]:
        A("    " + arr2(p) + ",")
    A("};")
    A("")
    A("// badge sockets: earned-socket patch (cells left, top, w, h + entries, up to 3x3)")
    A("struct OrchidCardPatch { u8 x, y, w, h; u16 map[3][3]; };")
    A("static const struct OrchidCardPatch sOrchidCardSockets[NUM_BADGES] = {")
    for r, ent in bg["sockets"]:
        assert r[2] <= 3 and r[3] <= 3
        full = [row + [0] * (3 - len(row)) for row in ent] + [[0, 0, 0]] * (3 - len(ent))
        A("    {%d, %d, %d, %d, %s}," % (r[0], r[1], r[2], r[3], arr2(full)))
    A("};")
    A("// BG3 badge k drawn over socket k (tile numbers in badges.png, palette OCARD_PAL_BADGES)")
    A("static const struct OrchidCardPatch sOrchidCardBadges[NUM_BADGES] = {")
    for r, ent in badges:
        assert r[2] <= 3 and r[3] <= 3
        full = [row + [0] * (3 - len(row)) for row in ent] + [[0, 0, 0]] * (3 - len(ent))
        A("    {%d, %d, %d, %d, %s}," % (r[0], r[1], r[2], r[3], arr2(full)))
    A("};")
    A("")
    A("// back rows: icon strip k goes on tile rows OCARD_ROW_TILE + 2 * slot, + 1 (all 30 columns)")
    A("enum { %s, OCARD_ROW_ICON_COUNT };" % ", ".join("OCARD_ICON_" + ic.upper() for ic in ROW_ICONS))
    A("#define OCARD_ROW_TILE %d" % bg["row0"])
    A("static const u16 sOrchidCardRowStrips[OCARD_ROW_ICON_COUNT][2][30] = {")
    for s in bg["strips"]:
        A("    " + arr2(s) + ",")
    A("};")
    A("")
    A("#endif // GUARD_DATA_TRAINER_CARD_ORCHID_H")
    with open(HEADER, "w") as f:
        f.write("\n".join(L) + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    bg = export_bg0()
    badges, nb = export_badges()
    pics = pic_positions()
    export_pal()
    write_header(bg, badges, nb, pics)
    print("BG0: %d art tiles (+4 grid = %d); pips rect %s; badges %d tiles; pic offsets %s"
          % (bg["n_art"], bg["n_tiles"], bg["pip_rect"], nb, pics))


if __name__ == "__main__":
    main()
