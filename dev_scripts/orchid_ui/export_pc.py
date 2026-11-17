"""
Export the Orchid PC storage (Pokémon Storage System) to game assets. Every art layer is drawn with the
mockup's own code (pc_ext.py / mock_pc.py), so the ROM art is the mockup art pixel for pixel.

Layers are cut straight from kit ROLE-index sheets (no colour matching), so one tile works under every
palette that keeps the kit role layout: a gold cursor is a palette swap (dex_ext.selected), a box colour is
a palette swap of the slot recess, a party slot's HP colour is a palette swap of its text window.

BG layout (pokemon_storage_system.c):
  BG0  popups only (message, menus, YES/NO, jump-to-box, box colour picker)     charblock 0 (+1)
  BG1  screen art: info dais + pills, title tab, buttons (labels baked in), party panel; plus the
       dynamic-text windows (info, title, party slot Lv + HP bar) whose tiles start as a copy of the art
       under them, so text and art share tiles and slide together                 charblock 2
  BG2  box slot recesses (one 3x3-tile cell for all 30 slots), 512 px wide for the box slide
  BG3  scrolling grid                                                          BG2 + BG3: charblock 3

Writes (under the repo root):
  graphics/pokemon_storage/orchid/bg1_tiles.png    BG1 art tiles (tile 0 blank), uncompressed: C reads them
                                                   to give the text windows their art background
  graphics/pokemon_storage/orchid/box_tiles.png    BG2/BG3 tiles: blank, slot cell, grid (2x2)
  graphics/pokemon_storage/orchid/swatch_tiles.png BG0 tiles: the slot cell on the window's WHITE (colour picker)
  graphics/pokemon_storage/orchid/bg.pal           UI BG palettes (see OPC_PAL_* in the header)
  graphics/pokemon_storage/orchid/box_colours.pal  the six box colours (slot recess palettes)
  graphics/pokemon_storage/orchid/ui_obj.png       OBJ sheet: ring (2 frames), lift shadow, chevron (2), hold tag
  src/data/pokemon_storage_orchid.h                tilemaps, owners, panel variants, layout constants

usage: export_pc.py
"""
import os
from PIL import Image
from kit import *
import kit_ext as KX
import dex_ext as D
import pc_ext as P
import mock_pc as M
import battle_ext as BX
from backdrop import GRID_PAL, grid_tile_image
from gamefont import draw_text, text_width
from party_ext import draw_code

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "pokemon_storage", "orchid")
HEADER = os.path.join(ROOT, "src", "data", "pokemon_storage_orchid.h")
W, H = 240, 160
COLS, ROWS = 30, 20
PANEL_COL0, PANEL_COLS = 10, 13          # party panel: tile columns 10..22 (x 80..183)
PANEL_ROW0, PANEL_ROWS = 4, 16           # rows 4..19 when open (top edge at y 36)
PANEL_SLIDE = 18                         # mock: slide = round((1 - party) * 18) * 8 px
LIFT, LIFT_FRAMES, FLASH_FRAMES = 14, 8, 4

# ---------------------------------------------------------------- palettes (kit role layout)
SENT_A, SENT_B = (8, 248, 8), (248, 8, 248)      # never in the art (asserted); C writes the name colours


def pad16(p):
    return list(p) + [(0, 0, 0)] * (16 - len(p))


def ui_pal():
    p = palette("orchid", spare_a=(40, 40, 64), spare_b=(192, 192, 184))   # genderless name = default ink
    return p


def slot_pal(hp):
    """Party slot: SPARE_A = panel pit, ACCENT_PALE / SPARE_B = HP light / dark (painted at runtime)."""
    p = palette("orchid", spare_a=P.PIT_RGB, spare_b=hp[1])
    p[ACCENT_PALE] = snap(hp[0])
    return p


def title_pal():
    p = palette("orchid", spare_a=(248, 248, 248), spare_b=(192, 192, 184))   # SPARE_A = name text white
    return p


def amber_grid():
    g = list(GRID_PAL)
    g[2], g[3] = snap((56, 48, 40)), snap((120, 104, 56))          # pc_ext.grid_frame_tint defaults
    return g


HP = [KX.HP_GREEN, KX.HP_YELLOW, KX.HP_RED]
PALS = [
    ("UI", ui_pal()), ("UI_GOLD", D.selected(ui_pal())),
    ("SLOT_G", slot_pal(HP[0])), ("SLOT_Y", slot_pal(HP[1])), ("SLOT_R", slot_pal(HP[2])),
    ("SLOT_G_GOLD", D.selected(slot_pal(HP[0]))), ("SLOT_Y_GOLD", D.selected(slot_pal(HP[1]))),
    ("SLOT_R_GOLD", D.selected(slot_pal(HP[2]))),
    ("GRID", pad16(GRID_PAL)), ("GRID_ITEMS", pad16(amber_grid())),
    ("TITLE", title_pal()), ("TITLE_GOLD", D.selected(title_pal())),
] + [("BOX_" + n.upper(), P.box_pal_colour(n)) for n in P.BOX_COLOURS]
PAL_ID = {n: i for i, (n, _) in enumerate(PALS)}
BOX_COLOUR_NAMES = list(P.BOX_COLOURS)


# ---------------------------------------------------------------- tiler (role-index tiles, flips allowed)
class Tiler:
    def __init__(self, first=()):
        self.tiles = [tuple([0] * 64)] + list(first)
        self.lookup = {}
        for i, t in enumerate(self.tiles):
            self.lookup.setdefault(t, i)

    def add(self, t, flips=True):
        if t in self.lookup:
            return self.lookup[t]
        if flips:
            for hf, vf in ((1, 0), (0, 1), (1, 1)):
                f = tuple(t[(7 - y if vf else y) * 8 + (7 - x if hf else x)] for y in range(8) for x in range(8))
                if f in self.lookup:
                    return self.lookup[f] | (hf << 10) | (vf << 11)
        i = len(self.tiles)
        self.tiles.append(t)
        self.lookup[t] = i
        return i

    def cell(self, im, cx, cy, ox=0, oy=0):
        px = im.load()
        t = tuple(px[ox + cx * 8 + x, oy + cy * 8 + y] for y in range(8) for x in range(8))
        if not any(t):
            return 0
        return self.add(t)


def cell_roles(im, cx, cy):
    px = im.load()
    return {px[cx * 8 + x, cy * 8 + y] for y in range(8) for x in range(8)} - {0}


GOLD_ROLES = {PANEL, WHITE, PANEL_SHADE}


def opaque_mask(im):
    """L mask of a P sheet's non-zero pixels (Image.point on 'P' goes through the palette)."""
    m = Image.new("L", im.size, 0)
    m.putdata([255 if v else 0 for v in im.tobytes()])
    return m


# ---------------------------------------------------------------- BG1 static art
def sheet():
    return new_sheet(W, H, "orchid")


OWN_NONE, OWN_PARTY, OWN_CLOSE, OWN_TITLE = range(4)


def static_layers():
    """(full art, {owner: element-only art})"""
    def btn(rect, icon, label):
        im = sheet()
        cv = Canvas(im)
        P.button(cv, rect, icon)
        P.button_text(cv, rect, label, INK, PANEL_SHADE)
        return im

    def tab():
        im = sheet()
        P.header_tab(Canvas(im))
        return im

    info = sheet()
    P.info_art(Canvas(info))
    parts = {OWN_PARTY: btn(P.BTN_PARTY, "party", "PARTY POKéMON"),
             OWN_CLOSE: btn(P.BTN_CLOSE, "close", "CLOSE BOX"),
             OWN_TITLE: tab()}
    full = info.copy()
    for k in (OWN_TITLE, OWN_PARTY, OWN_CLOSE):
        full.paste(parts[k], (0, 0), opaque_mask(parts[k]))
    used = set(full.tobytes())
    assert not used & {SPARE_A, SPARE_B}, "static art uses the runtime name colours"
    return full, parts


def owners(parts, cols, rows, col0=0, row0=0):
    out = [[OWN_NONE] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            hits = [k for k, im in parts.items() if cell_roles(im, col0 + c, row0 + r) & GOLD_ROLES]
            assert len(hits) <= 1, ("two gold owners in a cell", c, r, hits)
            if hits:
                out[r][c] = hits[0]
    return out


# ---------------------------------------------------------------- BG1 party panel
def slot_xy(k):
    return P.party_slot_xy(k)


def panel_sheet(filled_mask):
    im = sheet()
    cv = Canvas(im)
    P.party_panel(cv, 0)
    for k in range(6):
        x, y = slot_xy(k)
        # filled: outline + trough of the mini HP bar only (the fill is painted at runtime)
        P.party_slot(cv, x, y, {"hp": 0, "maxhp": 1} if filled_mask >> k & 1 else None)
    cx, cy, cw, chh = P.PARTY_CANCEL
    rounded_box(cv, cx, cy, cw, chh, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, cx + (cw - text_width("CANCEL")) // 2, cy - 1, "CANCEL", INK, PANEL_SHADE)
    used = set(im.tobytes())
    assert not used & {ACCENT_PALE, SPARE_B}, "panel art uses the runtime HP colours"
    return im


def panel_parts():
    """Owner masks: slot k (filled) and CANCEL, to find which cells swap to gold."""
    parts = {}
    for k in range(6):
        im = sheet()
        x, y = slot_xy(k)
        P.party_slot(Canvas(im), x, y, {"hp": 0, "maxhp": 1})
        parts[k] = im
    im = sheet()
    cx, cy, cw, chh = P.PARTY_CANCEL
    rounded_box(Canvas(im), cx, cy, cw, chh, 4, PANEL, INK, WHITE, PANEL_SHADE)
    parts[6] = im
    return parts


def slot_bbox(k):
    x, y = slot_xy(k)
    return x, y, x + P.PSLOT_W - 1, y + P.PSLOT_H - 1


def cell_slots(c, r):
    """Slots whose box touches panel cell (c, r) (absolute tile coords)."""
    x0, y0 = c * 8, r * 8
    out = []
    for k in range(6):
        a, b, cc, d = slot_bbox(k)
        if a <= x0 + 7 and cc >= x0 and b <= y0 + 7 and d >= y0:
            out.append(k)
    return out


# ---------------------------------------------------------------- text windows on BG1 (geometry checks)
INFO_WIN = (0, 10, 10, 9)          # tiles: left, top, width, height
TITLE_WIN = (14, 2, 12, 2)


def slot_win(k):
    return (13 + 6 * (k % 2), 5 + 4 * (k // 2), 4, 3)


def bbox_in(im, win):
    bb = im.getbbox()
    if bb is None:
        return True
    l, t, w, h = win
    return bb[0] >= l * 8 and bb[1] >= t * 8 and bb[2] <= (l + w) * 8 and bb[3] <= (t + h) * 8


def check_text_windows():
    import pc_ext as PX
    # longest plausible info texts
    for name in ("Mudkip", "MMMMMMMMMMMM", "Wwwwwwwwwwww"):
        for item in ("Mystic Water", "Weakness Policy", "None"):
            m = dict(P.BOX1[7], name=name, item=item, lv=100, marks={0, 1, 2, 3})
            im = sheet()
            PX.info_text(Canvas(im), m)
            assert bbox_in(im, INFO_WIN), (name, item, im.getbbox())
    for nm in ("BOX 1", "BOX 14", "MMMMMMMM"):
        im = sheet()
        tc = Canvas(im)
        x, y, w, h = P.TAB
        draw_text(tc, x + (P.TAB_CAP - text_width(nm)) // 2 + 1, y - 1, nm, WHITE, ACCENT_DARK)
        cs = "30/30"
        draw_text(tc, x + P.TAB_CAP + (w - P.TAB_CAP - text_width(cs, "small")) // 2 + 1, y + 1, cs, INK,
                  PANEL_SHADE, font="small")
        assert bbox_in(im, TITLE_WIN), (nm, im.getbbox())
    for k in range(6):
        im = sheet()
        x, y = slot_xy(k)
        P.party_slot_text(Canvas(im), x, y, {"lv": 100})
        KX.bar(Canvas(im), x + 25, y + 16, 15, 1.0, SPARE_A, SPARE_B, trough=PANEL_DARK, outline=INK, h=2)
        assert bbox_in(im, slot_win(k)), (k, im.getbbox(), slot_win(k))


# ---------------------------------------------------------------- BG2 / BG3 / BG0 swatch tiles
def slot_cell_sheet(fill=0):
    im = new_sheet(24, 24, "orchid")
    if fill:
        Canvas(im).rect(0, 0, 23, 23, fill)
    P.slot(Canvas(im), 12, 12)
    return im


def grid_tiles():
    g = grid_tile_image().load()
    out = []
    for ty in range(2):
        for tx in range(2):
            out.append(tuple(g[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    return out


# ---------------------------------------------------------------- OBJ sheet
def ui_obj_sheet():
    """ring normal + flash (32x32 each), shadow 16x8, chevron normal + lit (8x16 each), hold tag 8x8.
    Laid out for 1D OBJ mapping: each frame is its own run of tiles (see OPC_OBJ_* tile offsets)."""
    frames = [
        ("RING", P.cursor_ring(False), 32, 32),
        ("RING_FLASH", P.cursor_ring(True), 32, 32),
        ("SHADOW", P.shadow(), 16, 8),
    ]
    # chevrons: the mock's 6x9 glyph, centred like D.chevron / M._chev_lit on an 8x16 OBJ (left-pointing)
    for name, cols in (("CHEVRON", ARROW_RED), ("CHEVRON_LIT", M.LIT)):
        im = Image.new("RGBA", (8, 16), (0, 0, 0, 0))
        px = im.load()
        for r, row in enumerate(SMALL_ARROW):
            for c, ch in enumerate(row):
                if ch in "OF":
                    px[1 + c, 4 + r] = (cols[0] if ch == "F" else cols[1]) + (255,)
        frames.append((name, im, 8, 16))
    tag = KX.sprite_rgba(KX.G("party_menu", "hold_icons.png"), 0, 8)
    frames.append(("HOLD_TAG", tag.crop((0, 0, 8, 8)), 8, 8))
    # palette: union of colours
    cols = []
    for _, im, _, _ in frames:
        px = im.load()
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                p = px[x, y]
                if p[3] and p[:3] not in cols:
                    cols.append(p[:3])
    assert len(cols) <= 15, cols
    pal = [(0, 0, 0)] + cols
    # 1D mapping: concatenate tiles of each frame (row-major tiles within a frame)
    tiles, offsets = [], {}
    for name, im, w, h in frames:
        offsets[name] = len(tiles)
        px = im.load()
        for ty in range(h // 8):
            for tx in range(w // 8):
                tiles.append(tuple(pal.index(px[tx * 8 + x, ty * 8 + y][:3]) if px[tx * 8 + x, ty * 8 + y][3] else 0
                                   for y in range(8) for x in range(8)))
    return tiles, offsets, pad16(pal)


# ---------------------------------------------------------------- writers
def save_tiles(tiles, path, pal, per=16):
    rows = (len(tiles) + per - 1) // per
    im = Image.new("P", (per * 8, rows * 8), 0)
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % per) * 8, (i // per) * 8
        for j, c in enumerate(t):
            px[ox + j % 8, oy + j // 8] = c
    im.save(path, transparency=0)


def c_array(L, decl, rows, fmt="0x%04X", per=None):
    L.append(decl + " = {")
    for row in rows:
        L.append("    {" + ", ".join(fmt % v for v in row) + "},")
    L.append("};")


def marks_bitmaps():
    im = Image.open(KX.G("interface", "mon_markings.png")).convert("RGB")
    px = im.load()
    out = []
    for k in range(4):
        rows = []
        for y in range(8):
            rows.append(sum(1 << (7 - x) for x in range(8) if sum(px[k * 8 + x, y]) < 400))
        out.append(rows)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    check_text_windows()

    # ---- BG1
    T = Tiler()
    full, parts = static_layers()
    static_map = [[T.cell(full, c, r) for c in range(COLS)] for r in range(ROWS)]
    static_own = owners(parts, COLS, ROWS)

    pparts = panel_parts()
    sheets = {}

    def psheet(mask):
        if mask not in sheets:
            sheets[mask] = panel_sheet(mask)
        return sheets[mask]

    # panel owners (gold swap): slots 0-5, CANCEL = 6
    p_own = [[0xFF] * PANEL_COLS for _ in range(PANEL_ROWS)]
    for r in range(PANEL_ROWS):
        for c in range(PANEL_COLS):
            hits = [k for k, im in pparts.items()
                    if cell_roles(im, PANEL_COL0 + c, PANEL_ROW0 + r) & GOLD_ROLES]
            assert len(hits) <= 1, ("panel cell with two owners", c, r, hits)
            if hits:
                p_own[r][c] = hits[0]
    # panel variants: per cell, one entry per filled-combination of the slots touching it
    p_slots = [[0] * PANEL_COLS for _ in range(PANEL_ROWS)]
    p_base = [[0] * PANEL_COLS for _ in range(PANEL_ROWS)]
    variants = []
    for r in range(PANEL_ROWS):
        for c in range(PANEL_COLS):
            ks = cell_slots(PANEL_COL0 + c, PANEL_ROW0 + r)
            p_slots[r][c] = sum(1 << k for k in ks)
            p_base[r][c] = len(variants)
            for combo in range(1 << len(ks)):
                mask = sum(1 << k for j, k in enumerate(ks) if combo >> j & 1)
                variants.append(T.cell(psheet(mask), PANEL_COL0 + c, PANEL_ROW0 + r))
    # row 4 with the panel fully open: the tab's bottom edge and the panel's top edge share cells
    comb = full.copy()
    p0 = psheet(0)
    comb.paste(p0, (0, 0), opaque_mask(p0))
    row4_combined = [T.cell(comb, PANEL_COL0 + c, PANEL_ROW0) for c in range(PANEL_COLS)]
    for c in range(PANEL_COLS):        # combined cells: no gold-role pixels from the panel (title gold never shows then)
        assert p_own[0][c] == 0xFF
    n_art = len(T.tiles)

    # window cells must sit on cells of one palette family
    l, t, w, h = INFO_WIN
    for r in range(t, t + h):
        for c in range(l, l + w):
            assert static_own[r][c] == OWN_NONE, ("info window over a gold cell", c, r)
    l, t, w, h = TITLE_WIN
    for r in range(t, t + h):
        for c in range(l, l + w):
            assert static_own[r][c] in (OWN_TITLE, OWN_NONE), ("title window", c, r)
    for k in range(6):
        l, t, w, h = slot_win(k)
        for r in range(t, t + h):
            for c in range(l, l + w):
                o = p_own[r - PANEL_ROW0][c - PANEL_COL0]
                assert o in (k, 0xFF), ("slot window over another slot's pill", k, c, r, o)
    win_tiles = INFO_WIN[2] * INFO_WIN[3] + TITLE_WIN[2] * TITLE_WIN[3] + 6 * 12
    assert n_art + win_tiles <= 512, (n_art, win_tiles)
    save_tiles(T.tiles, os.path.join(OUT, "bg1_tiles.png"), PALS[0][1])

    # ---- BG2 / BG3 (shared charblock): blank, slot cell, grid
    TB = Tiler()
    slot = slot_cell_sheet()
    slot_map = [[TB.cell(slot, c, r) for c in range(3)] for r in range(3)]
    grid_base = len(TB.tiles)
    TB.tiles += grid_tiles()
    save_tiles(TB.tiles, os.path.join(OUT, "box_tiles.png"), PALS[PAL_ID["BOX_ORCHID"]][1])

    # ---- BG0 swatches (slot cell on WHITE)
    sw = slot_cell_sheet(WHITE)
    swatch = []
    swatch_map = []
    for r in range(3):
        row = []
        for c in range(3):
            px = sw.load()
            t = tuple(px[c * 8 + x, r * 8 + y] for y in range(8) for x in range(8))
            if t not in swatch:
                swatch.append(t)
            row.append(swatch.index(t))
        swatch_map.append(row)
    save_tiles(swatch, os.path.join(OUT, "swatch_tiles.png"), PALS[PAL_ID["BOX_ORCHID"]][1])

    # ---- palettes
    n_ui = PAL_ID["BOX_ORCHID"]       # JASC files hold at most 256 colours: UI palettes, then the box colours
    write_jasc(os.path.join(OUT, "bg.pal"), [c for _, p in PALS[:n_ui] for c in pad16(p)])
    write_jasc(os.path.join(OUT, "box_colours.pal"), [c for _, p in PALS[n_ui:] for c in pad16(p)])

    # ---- OBJ
    otiles, ooffs, opal = ui_obj_sheet()
    save_tiles(otiles, os.path.join(OUT, "ui_obj.png"), opal)

    # ---- header
    L = []
    a = L.append
    a("// GENERATED by dev_scripts/orchid_ui/export_pc.py - do not edit by hand.")
    a("// Orchid PC storage layout (mockups: dev_scripts/orchid_ui/mock_pc.py, anim_pc.py, pc_ext.py).")
    a("#ifndef GUARD_DATA_POKEMON_STORAGE_ORCHID_H")
    a("#define GUARD_DATA_POKEMON_STORAGE_ORCHID_H")
    a("")
    a("// ---- palettes (16 colours each, kit role layout): bg.pal, then box_colours.pal (OPC_PAL_BOX_* - OPC_PAL_BOX_ORCHID)")
    for i, (n, _) in enumerate(PALS):
        a("#define OPC_PAL_%-14s %d" % (n, i))
    a("#define OPC_PAL_COUNT          %d" % len(PALS))
    a("#define OPC_BOX_COLOURS        %d   // %s" % (len(BOX_COLOUR_NAMES), ", ".join(BOX_COLOUR_NAMES)))
    a("#define OPC_ROLE_INK           %d" % INK)
    a("#define OPC_ROLE_INK_SOFT      %d" % INK_SOFT)
    a("#define OPC_ROLE_WHITE         %d" % WHITE)
    a("#define OPC_ROLE_PANEL         %d" % PANEL)
    a("#define OPC_ROLE_PANEL_SHADE   %d" % PANEL_SHADE)
    a("#define OPC_ROLE_PANEL_DARK    %d" % PANEL_DARK)
    a("#define OPC_ROLE_ACCENT_DARK   %d" % ACCENT_DARK)
    a("#define OPC_ROLE_ACCENT        %d" % ACCENT)
    a("#define OPC_ROLE_ACCENT_LIGHT  %d" % ACCENT_LIGHT)
    a("#define OPC_ROLE_ACCENT_PALE   %d   // slot palettes: HP light" % ACCENT_PALE)
    a("#define OPC_ROLE_SELECT_DARK   %d" % SELECT_DARK)
    a("#define OPC_ROLE_SPARE_A       %d   // UI: name fg; slot: panel pit; title: white" % SPARE_A)
    a("#define OPC_ROLE_SPARE_B       %d   // UI: name shadow; slot: HP dark" % SPARE_B)
    a("")
    a("// ---- BG1 (charblock 2): art tiles then the text windows")
    a("#define OPC_BG1_ART_TILES      %d" % n_art)
    a("#define OPC_INFO_WIN_LEFT      %d" % INFO_WIN[0])
    a("#define OPC_INFO_WIN_TOP       %d" % INFO_WIN[1])
    a("#define OPC_INFO_WIN_W         %d" % INFO_WIN[2])
    a("#define OPC_INFO_WIN_H         %d" % INFO_WIN[3])
    a("#define OPC_TITLE_WIN_LEFT     %d" % TITLE_WIN[0])
    a("#define OPC_TITLE_WIN_TOP      %d" % TITLE_WIN[1])
    a("#define OPC_TITLE_WIN_W        %d" % TITLE_WIN[2])
    a("#define OPC_TITLE_WIN_H        %d" % TITLE_WIN[3])
    a("#define OPC_SLOT_WIN_W         4")
    a("#define OPC_SLOT_WIN_H         3")
    a("enum {OPC_OWN_NONE, OPC_OWN_PARTY, OPC_OWN_CLOSE, OPC_OWN_TITLE};")
    c_array(L, "static const u16 sOPcStaticMap[%d][%d]" % (ROWS, COLS), static_map)
    c_array(L, "static const u8 sOPcStaticOwner[%d][%d]" % (ROWS, COLS), static_own, "%d")
    a("")
    a("// ---- party panel: tile columns %d..%d, rows %d..%d when open; slides %d tiles" % (
        PANEL_COL0, PANEL_COL0 + PANEL_COLS - 1, PANEL_ROW0, PANEL_ROW0 + PANEL_ROWS - 1, PANEL_SLIDE))
    a("// Cell entry = sOPcPanelVariants[base + combo], combo = filled bits of the cell's slots (sOPcPanelSlots,")
    a("// lowest slot = bit 0). Owner = slot whose pill is in the cell (gold swap), 6 = CANCEL, 0xFF = none.")
    a("#define OPC_PANEL_COL0         %d" % PANEL_COL0)
    a("#define OPC_PANEL_COLS         %d" % PANEL_COLS)
    a("#define OPC_PANEL_ROW0         %d" % PANEL_ROW0)
    a("#define OPC_PANEL_ROWS         %d" % PANEL_ROWS)
    a("#define OPC_PANEL_SLIDE        %d" % PANEL_SLIDE)
    a("#define OPC_PANEL_OWNER_CANCEL 6")
    c_array(L, "static const u8 sOPcPanelSlots[%d][%d]" % (PANEL_ROWS, PANEL_COLS), p_slots, "0x%02X")
    c_array(L, "static const u16 sOPcPanelBase[%d][%d]" % (PANEL_ROWS, PANEL_COLS), p_base, "%d")
    c_array(L, "static const u8 sOPcPanelOwner[%d][%d]" % (PANEL_ROWS, PANEL_COLS), p_own, "0x%02X")
    a("static const u16 sOPcPanelVariants[%d] = {" % len(variants))
    for i in range(0, len(variants), 16):
        a("    " + ", ".join("0x%04X" % v for v in variants[i:i + 16]) + ",")
    a("};")
    a("static const u16 sOPcPanelRow4Open[%d] = {%s};" % (PANEL_COLS, ", ".join("0x%04X" % v for v in row4_combined)))
    a("")
    a("// ---- BG2 / BG3 (charblock 3, shared): tile 0 blank, slot cell, grid 2x2 (TL, TR, BL, BR)")
    a("#define OPC_BOX_TILES          %d" % len(TB.tiles))
    a("#define OPC_GRID_TILE_BASE     %d" % grid_base)
    c_array(L, "static const u16 sOPcSlotCell[3][3]", slot_map)
    a("// ---- BG0 colour swatches: the slot cell on the window's white, tile indices relative to their base")
    a("#define OPC_SWATCH_TILES       %d" % len(swatch))
    c_array(L, "static const u8 sOPcSwatchCell[3][3]", swatch_map, "%d")
    a("")
    a("// ---- OBJ sheet ui_obj.png (tile offsets, 1D mapping)")
    for n, o in ooffs.items():
        a("#define OPC_OBJ_%-12s %d" % (n, o))
    a("#define OPC_OBJ_TILES          %d" % len(otiles))
    a("")
    a("// ---- geometry (px, mock_pc.py / pc_ext.py)")
    cx, cy, ro, ri = P.DAIS
    consts = dict(
        SLOT_X0=P.centre(0)[0], SLOT_Y0=P.centre(0)[1], SLOT_PITCH=24, SLOT_COL0=P.cell(0)[0] // 8,
        SLOT_ROW0=P.cell(0)[1] // 8,
        ICON_DY=-4,                                  # box / party icon sprite centre = slot centre + (0, -4)
        LIFT=LIFT, LIFT_FRAMES=LIFT_FRAMES, FLASH_FRAMES=FLASH_FRAMES, BOB_PERIOD=16,
        SHADOW_DY=3,
        DAIS_X=cx, STAGE_Y=cy + int(ri * 0.55) + 3,
        NAME_X=P.NAME_PILL[0], NAME_Y=P.NAME_PILL[1], NAME_W=P.NAME_PILL[2],
        LV_X=P.LV_PILL[0], LV_Y=P.LV_PILL[1], LV_W=P.LV_PILL[2],
        MARK_X=P.MARK_WELL[0] + 3, MARK_Y=P.MARK_WELL[1] + 4,
        TYPES_X=P.LV_PILL[0], TYPES_Y=P.TYPES_Y, TYPES_PITCH=36,
        ITEM_TEXT_X0=24, ITEM_TEXT_X1=P.ITEM_PILL[0] + P.ITEM_PILL[2] - 3, ITEM_Y=P.ITEM_PILL[1],
        ITEM_ICON_X=int(P.ITEM_DISC[0]) - 12 + 16, ITEM_ICON_Y=int(P.ITEM_DISC[1]) - 12 + 16,
        TAB_X=P.TAB[0], TAB_Y=P.TAB[1], TAB_W=P.TAB[2], TAB_CAP=P.TAB_CAP,
        CHEV_L_X=P.CHEVRONS[0][0], CHEV_R_X=P.CHEVRONS[1][0], CHEV_Y=P.CHEVRONS[0][1],
        CHEV_LIT_DX=2, CHEV_LIT_FRAMES=8,
        PSLOT_X0=slot_xy(0)[0], PSLOT_Y0=slot_xy(0)[1], PSLOT_DX=48, PSLOT_DY=29,
        PICON_DX=12, PICON_DY=13,                     # party ring centre = slot + (12, 13); icon = that - (0, 4)
        PCANCEL_X=P.PARTY_CANCEL[0] + P.PARTY_CANCEL[2] // 2, PCANCEL_Y=P.PARTY_CANCEL[1] + P.PARTY_CANCEL[3] // 2,
        PLV_DX=24, PLV_DY=4, PBAR_DX=25, PBAR_DY=16, PBAR_W=15,
        HOLD_TAG_DX=6, HOLD_TAG_DY=6,
        BOX_SLIDE_TILES=M.BOX_SLIDE // 8,
        SWATCH_X0=100, SWATCH_Y=68,                   # mock_pc.colour_swatches: centres (100 + 24k, 68)
        SWATCH_WIN_LEFT=11, SWATCH_WIN_TOP=7,
        JUMP_WIN_LEFT=13, JUMP_WIN_TOP=5, JUMP_WIN_W=12, JUMP_WIN_H=8,
        JUMP_CHEV_L_X=111, JUMP_CHEV_R_X=192, JUMP_CHEV_Y=48,
        GRID_SCROLL_FRAMES=4,
    )
    for k, v in consts.items():
        a("#define OPC_%-20s %d" % (k, v))
    a("")
    # anim_pc.pickup_gif: lift = round(14 * ease_out(t / 8)) after A, round(14 * (1 - ease_out(t / 8))) on the drop
    ease = lambda t: 1 - (1 - t) ** 2
    up = [int(round(LIFT * ease(t / LIFT_FRAMES))) for t in range(1, LIFT_FRAMES + 1)]
    down = [int(round(LIFT * (1 - ease(t / LIFT_FRAMES)))) for t in range(LIFT_FRAMES)]
    a("static const u8 sOPcLiftUp[OPC_LIFT_FRAMES] = {%s};" % ", ".join(map(str, up)))
    a("static const u8 sOPcLiftDown[OPC_LIFT_FRAMES] = {%s};" % ", ".join(map(str, down)))
    a("")
    a("// ---- marking shapes (graphics/interface/mon_markings.png): circle, square, triangle, heart; bit 7 = left")
    c_array(L, "static const u8 sOPcMarks[4][8]", marks_bitmaps(), "0x%02X")
    a("")
    a("#endif // GUARD_DATA_POKEMON_STORAGE_ORCHID_H")
    with open(HEADER, "w") as f:
        f.write("\n".join(L) + "\n")
    print("BG1 art tiles %d (+%d window tiles), panel variants %d, box tiles %d, swatch tiles %d, obj tiles %d"
          % (n_art, win_tiles, len(variants), len(TB.tiles), len(swatch), len(otiles)))


if __name__ == "__main__":
    main()
