"""
Export the Orchid Pokémon summary screen to game assets. Every art layer is built with the mockup's
own drawing code (mock_summary.py / summary_ext.py), so the ROM art is the mockup art pixel for pixel.

How the layers are cut: each layer is composed exactly like mock_summary.render() composes it (art
sheet + gold / moving / bar sheets with their own palettes), as a 240x160 image of exact colours.
Every 8x8 cell is then given ONE BG palette that holds all of its colours (preferring a palette that
reproduces an existing tile), and the pixels are re-indexed into it. So a cell that holds the bottom
of a gold (selected) move pill and the top of a normal one is still exact: it just uses the SELECT
roles of palette 0. The C code only swaps whole pre-cut tilemaps / rows; it never palette-swaps.

Writes (under the repo root):
  graphics/summary_screen/orchid/tiles.png        BG1 + BG2 + BG3 tile sheet (tile 0 blank, 1-4 grid)
  graphics/summary_screen/orchid/bars.png         base tiles of the runtime-painted bars (also in tiles.png)
  graphics/summary_screen/orchid/screen_male.pal  BG palettes 0-6 (see PAL_* below), male theme
  graphics/summary_screen/orchid/screen_female.pal
  graphics/summary_screen/orchid/category_tags.png  16x48 OBJ: physical / special / status tags
  src/data/pokemon_summary_orchid.h               tilemaps, row variants, bar table, layout constants

usage: export_summary.py
"""
import os
import struct
from PIL import Image
from kit import *
import kit_ext as KX
import dex_ext as D
import mock_battle as MB
import mock_summary as M
import summary_ext as S
from backdrop import GRID_PAL, grid_tile_image
from gamefont import draw_text, text_width

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "summary_screen", "orchid")
HEADER = os.path.join(ROOT, "src", "data", "pokemon_summary_orchid.h")
THEMES = ("male", "female")
W, H = 240, 160
COLS, ROWS = 30, 20

PAL_ART, PAL_SEL, PAL_MOV, PAL_TEXT, PAL_MOVE_TEXT, PAL_BARS, PAL_GRID = range(7)
PAGE_COL0 = 11                      # page art lives in tile columns 11..29 (x >= 88)
PAGE_COLS = COLS - PAGE_COL0
SLIDE_FRAMES = 12
SLIDE_DIST = 152                    # mock: 148 px; the page tilemaps need a whole number of tiles (19)


def pad16(p):
    return list(p) + [(0, 0, 0)] * (16 - len(p))


def bar_pal(theme):
    p = list(MB.HBAR_PAL)
    art = S.art_pal(theme)
    p[14], p[15] = art[PANEL], art[PANEL_SHADE]
    return p


def palettes(theme):
    art = S.art_pal(theme)
    return [pad16(art), pad16(S.selected(art)), pad16(S.moving(art)), pad16(S.txt_pal(theme)),
            pad16(S.move_txt_pal(theme)), pad16(bar_pal(theme)), pad16(GRID_PAL)]


PALS = {t: palettes(t) for t in THEMES}


# ---------------------------------------------------------------- symbolic layers
# A layer pixel is a "symbol" = (rgb in the male theme, rgb in the female theme), or None.
class Layer:
    def __init__(self):
        self.px = [[None] * W for _ in range(H)]

    def put(self, im, pal_of_theme, mask=None, at=(0, 0)):
        """im: P sheet; pal_of_theme(theme) -> 16 colours. Non-zero pixels overwrite."""
        ip = im.load()
        pm, pf = pal_of_theme("male"), pal_of_theme("female")
        ox, oy = at
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                v = ip[x, y]
                X, Y = x + ox, y + oy
                if v and 0 <= X < W and 0 <= Y < H and (mask is None or mask(X, Y)):
                    self.px[Y][X] = (pm[v], pf[v])
        return self


def P(i):
    return lambda t: PALS[t][i]


def sheet():
    return M.sheet("male")


# ---------------------------------------------------------------- tiler
class Tiler:
    def __init__(self):
        g = grid_tile_image().load()
        self.tiles = [tuple([0] * 64)]
        for ty in range(2):
            for tx in range(2):
                self.tiles.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
        self.lookup = {}
        for i, t in enumerate(self.tiles):
            self.lookup.setdefault(t, i)
        self.dedicated = {}          # bar cells: key -> tile index

    def _find(self, t):
        if t in self.lookup:
            return (self.lookup[t], 0, 0)
        for hf, vf in ((1, 0), (0, 1), (1, 1)):
            f = tuple(t[(7 - y if vf else y) * 8 + (7 - x if hf else x)] for y in range(8) for x in range(8))
            if f in self.lookup:
                return (self.lookup[f], hf, vf)
        return None

    @staticmethod
    def _index(sym, pal_id):
        pm, pf = PALS["male"][pal_id], PALS["female"][pal_id]
        for j in range(1, 16):
            if (pm[j], pf[j]) == sym:
                return j
        return None

    def cell(self, layer, cx, cy, cands, key=None):
        syms = [layer.px[cy * 8 + y][cx * 8 + x] for y in range(8) for x in range(8)]
        if all(s is None for s in syms):
            return 0
        options = []
        for p in cands:
            idx = [0 if s is None else self._index(s, p) for s in syms]
            if None not in idx:
                options.append((p, tuple(idx)))
        assert options, "cell (%d,%d): no palette in %s holds %s" % (cx, cy, cands, set(syms) - {None})
        if key is not None:                       # runtime-painted bar cell: own tile, the bar's palette
            want = PAL_ART if key[0].startswith("BAR_IV") else PAL_BARS
            p, t = next(o for o in options if o[0] == want)
            if key in self.dedicated:
                i, p0, t0 = self.dedicated[key]
                assert (p0, t0) == (p, t), key
            else:
                i = len(self.tiles)
                self.tiles.append(t)
                self.dedicated[key] = (i, p, t)
            return i | (p << 12)
        for p, t in options:
            f = self._find(t)
            if f:
                i, hf, vf = f
                return i | (hf << 10) | (vf << 11) | (p << 12)
        p, t = options[0]
        i = len(self.tiles)
        self.tiles.append(t)
        self.lookup[t] = i
        return i | (p << 12)

    def tilemap(self, layer, cands, rows=range(ROWS), cols=range(COLS), keys=None):
        tm = [[0] * COLS for _ in range(ROWS)]
        for cy in rows:
            for cx in cols:
                tm[cy][cx] = self.cell(layer, cx, cy, cands, (keys or {}).get((cx, cy)))
        return tm


T = Tiler()
BG1_CANDS = (PAL_ART, PAL_SEL)
BG2_CANDS = (PAL_ART, PAL_SEL, PAL_MOV, PAL_BARS)


# ---------------------------------------------------------------- BG1: header + left column (+ tray)
HDR_INFO, HDR_SKILLS, HDR_IVS, HDR_EVS, HDR_MOVES, HDR_TRAY, HDR_LEARN, HDR_EGG = range(8)
HDR_NAMES = ["INFO", "SKILLS", "IVS", "EVS", "MOVES", "MOVES_TRAY", "LEARN", "EGG"]


def tab_labels(page, skills_mode, rects):
    tl = sheet()
    tc = Canvas(tl)
    for i, r in enumerate(rects):
        if r is None:
            continue
        x0 = r[0]
        label = M.TABS[i]
        if i == 1 and page == 1 and skills_mode != "stats":
            label = skills_mode.upper()[:-1] + "s"
        fg, sh = (INK, SELECT_DARK) if i == page else (INK_SOFT, PANEL_SHADE)
        f = "normal" if text_width(label) <= M.TAB_W - 6 else "narrow"
        M.ctext(tc, x0, M.TAB_W, 1 if i == page else 2, label, fg, sh, f)
    return tl


def static_layer(kind):
    egg = kind == HDR_EGG
    learn = kind == HDR_LEARN
    tray = kind in (HDR_TRAY, HDR_LEARN)
    page = {HDR_INFO: 0, HDR_SKILLS: 1, HDR_IVS: 1, HDR_EVS: 1, HDR_MOVES: 2, HDR_TRAY: 2, HDR_LEARN: 2, HDR_EGG: 0}[kind]
    mode = {HDR_IVS: "ivs", HDR_EVS: "evs"}.get(kind, "stats")
    mon = S.egg_mon() if egg else S.hero()
    art = sheet()
    ac = Canvas(art)
    rects = M.draw_header(ac, page, "B", learn, egg)
    M.draw_left(ac, mon)
    if tray:
        S.move_tray(ac, M.TRAY_Y)
    L = Layer().put(art, P(PAL_ART))
    if rects and rects[page]:
        x0, y0, x1, y1 = rects[page]
        L.put(art, P(PAL_SEL), mask=lambda X, Y: x0 <= X <= x1 and y0 <= Y <= y1)
    # baked static text (same colours in the text palette)
    txt = sheet()
    tc = Canvas(txt)
    if learn:
        draw_text(tc, 8, -1, "Forget which move?", WHITE, ACCENT_DARK)
    elif rects:
        L.put(tab_labels(page, mode, rects), P(PAL_TEXT))
    if not egg and not tray:
        M.cap_text(tc, M.LX, M.NO_Y, M.NO_CAP, "No.")
    L.put(txt, P(PAL_TEXT))
    if learn:
        h = sheet()
        S.hint_tab(Canvas(h), 170, 2, "B", "CANCEL")
        L.put(h, P(PAL_ART))
    return L


# ---------------------------------------------------------------- BG1 hint patches (rows 18-19)
HINTS = [
    ("NONE", []),
    ("A_RENAME", [("A", "RENAME")]),
    ("A_CANCEL", [("A", "CANCEL")]),
    ("A_IVS", [("A", "IVs")]),
    ("A_EVS", [("A", "EVs")]),
    ("A_STATS", [("A", "STATS")]),
    ("A_INFO", [("A", "INFO")]),
    ("A_INFO_RELEARN", [("A", "INFO"), ("START", "RELEARN")]),
]
HINT_ROW0 = M.HINT_Y // 8


def hint_layer(items):
    h = sheet()
    hc = Canvas(h)
    xr = M.RX + M.RW
    for hb, lab in items:
        w = S.hint_w(hb, lab)
        assert xr - w >= PAGE_COL0 * 8, lab
        S.hint_tab(hc, xr - w, M.HINT_Y, hb, lab)
        xr -= w + 4
    return Layer().put(h, P(PAL_ART))


# ---------------------------------------------------------------- BG2 pages
def zero_mon(egg=False):
    if egg:
        return S.egg_mon()
    m = S.hero()
    return m.copy(hp=0, ivs={k: 0 for k in m.ivs}, evs={k: 0 for k in m.evs}, exp=m.exp_lv)


def page_layer(pg):
    L = Layer()
    L.put(pg.art, P(PAL_ART))
    L.put(pg.sel, P(PAL_SEL))
    L.put(pg.mov, P(PAL_MOV))
    L.put(pg.bars, P(PAL_BARS))
    return L


BAR_W = 48
STAT_KEYS = ["hp", "atk", "def_", "spa", "spd", "spe"]


def bar_rects(mode):
    """(name, x, y) of each runtime bar's outline (50 x 5 px) on the SKILLS page."""
    bx = M.RX + M.CAP + 6
    out = []
    if mode == "stats":
        out.append(("BAR_HP", bx, M.CONTENT_Y + 5))
    else:
        out.append(("BAR_IV_HP", bx, M.CONTENT_Y + 5))
        for k in range(5):
            out.append(("BAR_IV_%s" % STAT_KEYS[k + 1].rstrip("_").upper(), bx, M.STAT_Y0 + k * M.STAT_PITCH + 5))
    out.append(("BAR_EXP", bx, M.STAT_Y0 + 5 * M.STAT_PITCH + 3 + M.STAT_PITCH + 5))
    return out


def bar_cells(x, y):
    return [(cx, cy) for cy in range(y // 8, (y + 4) // 8 + 1) for cx in range(x // 8, (x + BAR_W + 1) // 8 + 1)]


def skills_tilemap(mode):
    pg = M.Page("male")
    M.skills_page(pg, zero_mon(), "stats" if mode == "stats" else "ivs")
    keys = {}
    for name, x, y in bar_rects(mode):
        for c in bar_cells(x, y):
            keys[c] = (name,) + c
    return T.tilemap(page_layer(pg), BG2_CANDS, keys=keys)


def info_tilemap(egg):
    pg = M.Page("male")
    M.info_page(pg, zero_mon(egg))
    return T.tilemap(page_layer(pg), BG2_CANDS)


# moves: pills drawn without notches (the PP notch is drawn in the BG0 move window at runtime)
ST_N, ST_S, ST_M = range(3)


def pill_y(i):
    return M.CONTENT_Y + i * M.MOVE_PITCH


def moves_layer(n, states):
    pg = M.Page("male")
    for i in range(n):
        cv = (pg.a, pg.s, pg.m)[states[i]]
        S.move_pill(cv, M.RX, pill_y(i), M.RW, M.MOVE_H)
        if i == 4:
            M._new_flag(cv, pg.mt, M.RX + M.RW - 29, pill_y(i))
    L = page_layer(pg)
    L.put(pg.mtxt, P(PAL_MOVE_TEXT))            # the baked "NEW" label
    return L


def pills_in_row(r, n):
    return [i for i in range(n) if pill_y(i) // 8 <= r <= (pill_y(i) + M.MOVE_H - 1) // 8]


MOVE_ROW0, MOVE_ROW1 = 2, 14


def moves_rows(n):
    """[row][variant] -> 19 cells (cols 11..29). variant = state(upper) * 3 + state(lower)."""
    out = []
    for r in range(MOVE_ROW0, MOVE_ROW1 + 1):
        ps = pills_in_row(r, n)
        vs = []
        for v in range(9):
            su, sl = v // 3, v % 3
            states = [ST_N] * n
            if ps:
                states[ps[0]] = su
            if len(ps) > 1:
                states[ps[1]] = sl
            tm = T.tilemap(moves_layer(n, states), BG2_CANDS, rows=[r], cols=range(PAGE_COL0, COLS))
            vs.append(tm[r][PAGE_COL0:])
        out.append((ps, vs))
    return out


# ---------------------------------------------------------------- OBJ: category tags
def category_sheet():
    im = Image.new("P", (16, 48), 0)
    flat = [c for rgb in S.CAT_PAL for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    for i, k in enumerate(("physical", "special", "status")):
        im.paste(S.cat_index(k), (0, 16 * i))
    return im


# ---------------------------------------------------------------- writers
def save_tiles(tiles, path):
    per = 16
    rows = (len(tiles) + per - 1) // per
    im = Image.new("P", (per * 8, rows * 8), 0)
    flat = [c for rgb in PALS["male"][PAL_ART] for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % per) * 8, (i // per) * 8
        for j, c in enumerate(t):
            px[ox + j % 8, oy + j // 8] = c
    im.save(path, transparency=0)


def c_rows(name, tm, comment=""):
    s = ["static const u16 %s[%d][%d] = {%s" % (name, len(tm), len(tm[0]), (" // " + comment) if comment else "")]
    for row in tm:
        s.append("    {" + ", ".join("0x%04X" % v for v in row) + "},")
    s.append("};")
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    # BG1 static bases
    bases = [T.tilemap(static_layer(k), BG1_CANDS) for k in range(len(HDR_NAMES))]
    hints = []
    for name, items in HINTS:
        tm = T.tilemap(hint_layer(items), BG1_CANDS, rows=range(HINT_ROW0, HINT_ROW0 + 2), cols=range(PAGE_COL0, COLS))
        hints.append([tm[r][PAGE_COL0:] for r in range(HINT_ROW0, HINT_ROW0 + 2)])
    # BG2 pages
    pages = {
        "INFO": info_tilemap(False),
        "EGG": info_tilemap(True),
        "SKILLS": skills_tilemap("stats"),
        "SKILLS_IVEV": skills_tilemap("ivev"),
    }
    rows4, rows5 = moves_rows(4), moves_rows(5)
    n_tiles = len(T.tiles)
    assert n_tiles <= 704, n_tiles            # charblock 2 + the part of charblock 3 below the maps
    save_tiles(T.tiles, os.path.join(OUT, "tiles.png"))

    # runtime bars: contiguous dedicated tiles per bar
    bars = []
    for mode in ("stats", "ivev"):
        for name, x, y in bar_rects(mode):
            if any(b[0] == name for b in bars):
                continue
            cells = bar_cells(x, y)
            idx = [T.dedicated[(name,) + c] for c in cells]
            first = idx[0][0]
            assert [i for i, _, _ in idx] == list(range(first, first + len(idx))), name
            pal = idx[0][1]
            assert all(p == pal for _, p, _ in idx), name
            c0, r0 = cells[0]
            ncols = len({c for c, _ in cells})
            bars.append((name, first, len(idx), c0, r0, ncols, x, y, pal))
    first_bar = min(b[1] for b in bars)
    last_bar = max(b[1] + b[2] for b in bars)
    save_tiles(T.tiles[first_bar:last_bar], os.path.join(OUT, "bars.png"))

    for t in THEMES:
        write_jasc(os.path.join(OUT, "screen_%s.pal" % t), [c for p in PALS[t] for c in p])
    category_sheet().save(os.path.join(OUT, "category_tags.png"), transparency=0)

    # slide offsets (ease-out 1 - (1 - u)^2, u = (f + 1) / 12), Python rounding like the mock
    ease = [int(round(SLIDE_DIST * (1 - (1 - (f + 1) / SLIDE_FRAMES) ** 2))) for f in range(SLIDE_FRAMES)]

    L = []
    a = L.append
    a("// GENERATED by dev_scripts/orchid_ui/export_summary.py - do not edit by hand.")
    a("// Orchid summary screen layout (mockups: dev_scripts/orchid_ui/mock_summary.py, anim_summary.py).")
    a("// Tilemap entries index graphics/summary_screen/orchid/tiles.png and carry their own BG palette.")
    a("#ifndef GUARD_DATA_POKEMON_SUMMARY_ORCHID_H")
    a("#define GUARD_DATA_POKEMON_SUMMARY_ORCHID_H")
    a("")
    a("#define OSUM_NUM_TILES        %d" % n_tiles)
    a("#define OSUM_GRID_TILE_BASE   1")
    for i, n in enumerate(["ART", "SEL", "MOV", "TEXT", "MOVE_TEXT", "BARS", "GRID"]):
        a("#define OSUM_PAL_%-14s%d" % (n, i))
    a("#define OSUM_NUM_PALS         7")
    a("#define OSUM_PAGE_COL0        %d   // page art occupies tile columns %d..29 (BG2, clipped at x %d)" % (PAGE_COL0, PAGE_COL0, M.PAGE_CLIP_X))
    a("#define OSUM_PAGE_COLS        %d" % PAGE_COLS)
    a("#define OSUM_PAGE_CLIP_X      %d" % M.PAGE_CLIP_X)
    a("#define OSUM_SLIDE_FRAMES     %d" % SLIDE_FRAMES)
    a("#define OSUM_SLIDE_TILES      %d   // page spacing during a slide (%d px)" % (SLIDE_DIST // 8, SLIDE_DIST))
    a("static const u8 sOSumSlideOffsets[OSUM_SLIDE_FRAMES] = {%s};" % ", ".join(map(str, ease)))
    a("")
    a("// ---- layout (px)")
    consts = dict(
        RX=M.RX, RW=M.RW, CAP=M.CAP, CONTENT_Y=M.CONTENT_Y, ROW=M.ROW, STAT_Y0=M.STAT_Y0, STAT_PITCH=M.STAT_PITCH,
        MOVE_H=M.MOVE_H, MOVE_PITCH=M.MOVE_PITCH, TRAY_Y=M.TRAY_Y, DESC_X=M.DESC_X, DESC_PITCH=M.DESC_PITCH,
        LX=M.LX, LW=M.LW, NAME_Y=M.NAME_Y, NO_Y=M.NO_Y, ITEM_Y=M.ITEM_Y,
        DAIS_X=M.DAIS_C[0], STAGE_Y=M.stage_y(), SOCK_BALL_X=M.SOCK_BALL[0], SOCK_BALL_Y=M.SOCK_BALL[1],
        SOCK_STATUS_X=M.SOCK_STATUS[0], SOCK_STATUS_Y=M.SOCK_STATUS[1],
        ARROW_L_X=M.TAB_ARROWS[0][0], ARROW_R_X=M.TAB_ARROWS[1][0], ARROW_Y=M.TAB_ARROWS[0][1] + 1,
        NEW_X=M.RX + M.RW - 29, NATURE_GAP=M.NATURE_GAP, HINT_Y=M.HINT_Y,
    )
    for k, v in consts.items():
        a("#define OSUM_%-20s %d" % (k, v))
    a("")
    a("// ---- BG1 static bases (header + left column [+ tray])")
    a("enum {%s, OSUM_HDR_COUNT};" % ", ".join("OSUM_HDR_" + n for n in HDR_NAMES))
    a("static const u16 sOSumStatic[OSUM_HDR_COUNT][%d][%d] = {" % (ROWS, COLS))
    for n, tm in zip(HDR_NAMES, bases):
        a("    [OSUM_HDR_%s] = {" % n)
        for row in tm:
            a("        {" + ", ".join("0x%04X" % v for v in row) + "},")
        a("    },")
    a("};")
    a("")
    a("// ---- BG1 button hints: rows %d-%d, columns %d..29" % (HINT_ROW0, HINT_ROW0 + 1, PAGE_COL0))
    a("#define OSUM_HINT_ROW0        %d" % HINT_ROW0)
    a("enum {%s, OSUM_HINT_COUNT};" % ", ".join("OSUM_HINT_" + n for n, _ in HINTS))
    a("static const u16 sOSumHints[OSUM_HINT_COUNT][2][%d] = {" % PAGE_COLS)
    for (n, _), tm in zip(HINTS, hints):
        a("    [OSUM_HINT_%s] = {" % n)
        for row in tm:
            a("        {" + ", ".join("0x%04X" % v for v in row) + "},")
        a("    },")
    a("};")
    a("")
    a("// ---- BG2 pages (full 30x20, art in columns %d..29)" % PAGE_COL0)
    a("enum {OSUM_PAGEART_INFO, OSUM_PAGEART_EGG, OSUM_PAGEART_SKILLS, OSUM_PAGEART_SKILLS_IVEV, OSUM_PAGEART_COUNT};")
    a("static const u16 sOSumPages[OSUM_PAGEART_COUNT][%d][%d] = {" % (ROWS, COLS))
    for n in ("INFO", "EGG", "SKILLS", "SKILLS_IVEV"):
        a("    [OSUM_PAGEART_%s] = {" % n)
        for row in pages[n]:
            a("        {" + ", ".join("0x%04X" % v for v in row) + "},")
        a("    },")
    a("};")
    a("")
    a("// ---- BG2 move pills: rows %d..%d, columns %d..29. Variant = state(upper pill) * 3 + state(lower pill)," % (MOVE_ROW0, MOVE_ROW1, PAGE_COL0))
    a("// state 0 normal / 1 cursor (gold) / 2 moving. sOSumMoveRowPills: pills crossing each row (0xFF = none).")
    a("#define OSUM_MOVE_ROW0        %d" % MOVE_ROW0)
    a("#define OSUM_MOVE_ROWS        %d" % (MOVE_ROW1 - MOVE_ROW0 + 1))
    for n, rows in ((4, rows4), (5, rows5)):
        a("static const u8 sOSumMoveRowPills%d[OSUM_MOVE_ROWS][2] = {" % n)
        for ps, _ in rows:
            pp = (ps + [0xFF, 0xFF])[:2]
            a("    {%s}," % ", ".join("0x%02X" % p for p in pp))
        a("};")
        a("static const u16 sOSumMoveRows%d[OSUM_MOVE_ROWS][9][%d] = {" % (n, PAGE_COLS))
        for _, vs in rows:
            a("    {")
            for v in vs:
                a("        {" + ", ".join("0x%04X" % c for c in v) + "},")
            a("    },")
        a("};")
    a("")
    a("// ---- runtime bars (outline %d x 5 px; fill rows y+1..y+3, light top row)" % (BAR_W + 2))
    a("#define OSUM_BAR_W            %d" % BAR_W)
    a("#define OSUM_BAR_TILES_FIRST  %d   // bars.png = tiles %d..%d of tiles.png" % (first_bar, first_bar, last_bar - 1))
    a("#define OSUM_BAR_TILES_COUNT  %d" % (last_bar - first_bar))
    a("enum {%s, OSUM_BAR_COUNT};" % ", ".join("OSUM_" + b[0] for b in bars))
    a("struct OSumBar { u16 tile; u8 count, col0, row0, cols, x, y, pal; };")
    a("static const struct OSumBar sOSumBars[OSUM_BAR_COUNT] = {")
    for name, first, cnt, c0, r0, ncols, x, y, pal in bars:
        a("    [OSUM_%s] = {%d, %d, %d, %d, %d, %d, %d, %d}," % (name, first, cnt, c0, r0, ncols, x, y, pal))
    a("};")
    a("")
    a("#endif // GUARD_DATA_POKEMON_SUMMARY_ORCHID_H")
    with open(HEADER, "w") as f:
        f.write("\n".join(L) + "\n")
    print("tiles %d (bars %d..%d), header %s" % (n_tiles, first_bar, last_bar - 1, os.path.relpath(HEADER, ROOT)))
    print("slide", ease)


if __name__ == "__main__":
    main()
