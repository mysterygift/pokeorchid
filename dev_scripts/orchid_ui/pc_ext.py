"""
Orchid PC storage (Pokémon Storage System) — geometry, art primitives and sample data
(PROPOSED, mockup only). Shared screen -> Orchid purple theme for every player.

Maps onto src/pokemon_storage_system.c (vanilla positions kept where practical):
    BG3  BW scrolling grid (replaces scrolling_bg.png; vanilla already scrolls BG3 diagonally)
    BG2  box "wallpaper" = 6x5 round slot recesses on a transparent field (grid shows through);
         512px wide (screenSize 1) so the box-switch slide is the vanilla BG2HOFS scroll, 6px/frame
    BG1  left info panel art (dais, pills) + top buttons + party panel (slides up, 1 tile/frame)
    BG0  text windows (info text, messages, context menu)
    OBJ  30 box icons + 6 party icons + held icon, front pic, type icons, cursor ring + shadow,
         box title tab text (vanilla: 2x 32x16 OBJ), red chevrons
Cell grid: slot i sits in the 3x3-tile cell (88 + 24*col, 40 + 24*row) -> identical tiles per slot.
"""
import math
import re
from PIL import Image
from kit import *
import kit_ext as KX
import dex_ext as D
import battle_ext as BX
from gamefont import draw_text, text_width
from party_ext import draw_code, safe_comp

W, H = 240, 160
G = KX.G

# ------------------------------------------------------------------ geometry
COLS, ROWS = 6, 5
SLOT_R, PIT_R = 11, 7.5


def cell(i):
    return 88 + 24 * (i % COLS), 40 + 24 * (i // COLS)


def centre(i):
    x, y = cell(i)
    return x + 12, y + 12


TAB = (112, 18, 96, 15)            # box title tab (x, y, w, h); accent name cap + count inset
TAB_CAP = 64
CHEVRONS = ((104, 25), (215, 25))  # vanilla arrows: x 92 / 228, y 28
BTN_PARTY = (82, 1, 86, 14)        # vanilla PARTY POKéMON button: tiles 10..21, row 0..1
BTN_CLOSE = (171, 1, 67, 14)       # vanilla CLOSE BOX: tiles 21..29
BTN_CAP = 15
DAIS = (40, 43, 36, 29)            # cx, cy, r_out, r_in  (vanilla display pic centre 40,48)
NAME_PILL = (2, 84, 76)
LV_PILL = (2, 100, 34, 15)
MARK_WELL = (38, 100, 40)
TYPES_Y = 117
ITEM_PILL = (12, 136, 66, 16)     # pill; the item icon disc overhangs its left end
ITEM_DISC = (12, 144, 10.5)
PARTY_PANEL = (80, 36, 104, 124)    # vanilla: 12-tile-wide map at tile x 10 slides up; Orchid stops under the title tab
MSG_WIN = (11, 17, 18, 2)          # vanilla WIN_MESSAGE


def party_slot_xy(k):
    """Top-left of small party slot k (2 columns x 3 rows, BW order: lead top-left)."""
    px, py, _, _ = PARTY_PANEL
    return px + 5 + 48 * (k % 2), py + 7 + 29 * (k // 2)


PARTY_CANCEL = (102, 132, 60, 14)
PSLOT_W, PSLOT_H = 46, 26


def party_icon_centre(k):
    x, y = party_slot_xy(k)
    return x + 12, y + 13


# ------------------------------------------------------------------ data
def pal_index(const):
    """Non-GBA iconPalIndex (Orchid uses modern icons)."""
    b = D._species_blocks()[const]
    m = re.search(r"\.iconPalIndex\s*=\s*([^,\n]+),", b).group(1)
    if "?" in m:
        m = m.split(":")[-1]
    return int(m.strip())


TYPES_FIX = {"RALTS": ["psychic", "fairy"], "AZURILL": ["normal", "fairy"], "MARILL": ["water", "fairy"],
             "MAWILE": ["steel", "fairy"]}


def mon(const, sex, lv, item=None, marks=(), nick=None, held=None):
    sp = D.species(const)
    import os
    types = TYPES_FIX.get(const) or [t for t in sp["types"] if os.path.exists(G("types", t + ".png"))]
    types = list(dict.fromkeys(types))
    sp["types"] = types
    return dict(const=const, folder=sp["folder"], name=nick or sp["name"], sex=sex, lv=lv,
                item=item, types=sp["types"], marks=set(marks), pal=pal_index(const))


def _box(spec):
    return {i: mon(*a) for i, a in spec.items()}


BOX1 = _box({
    0: ("POOCHYENA", "m", 6), 1: ("WURMPLE", "f", 4), 2: ("LOTAD", "m", 7),
    4: ("SEEDOT", "f", 6, "Oran Berry"), 6: ("ZIGZAGOON", "f", 5), 7: ("MUDKIP", "m", 14, "Mystic Water", (0, 2)),
    8: ("SHROOMISH", "m", 9), 9: ("WHISMUR", "f", 8), 12: ("SURSKIT", "f", 10),
    13: ("SKITTY", "f", 9, "Oran Berry", (3,)), 14: ("MAKUHITA", "m", 11), 16: ("ARON", "m", 12, "Hard Stone"),
    18: ("ELECTRIKE", "m", 10), 19: ("AZURILL", "f", 5), 21: ("NINCADA", "m", 12),
    24: ("SLAKOTH", "m", 13), 26: ("MARILL", "f", 12, None, (1,)), 27: ("WINGULL", "f", 9),
})
BOX2 = _box({
    0: ("TREECKO", "m", 5), 1: ("TORCHIC", "f", 5), 3: ("TAILLOW", "m", 8),
    5: ("NOSEPASS", "m", 13), 7: ("SABLEYE", "f", 15), 8: ("MAWILE", "f", 15),
    10: ("MEDITITE", "m", 14), 12: ("PLUSLE", "f", 12), 13: ("MINUN", "m", 12),
    15: ("VOLBEAT", "m", 14), 17: ("TRAPINCH", "f", 15), 20: ("SPINDA", "f", 13),
    22: ("RALTS", "m", 7), 25: ("LOTAD", "f", 6),
})
BOXES = [("BOX 1", BOX1), ("BOX 2", BOX2)]

PARTY = [
    dict(mon("GROVYLE", "m", 18, "Oran Berry"), hp=52, maxhp=52),
    dict(mon("TAILLOW", "f", 12), hp=29, maxhp=35),
    dict(mon("RALTS", "f", 10), hp=24, maxhp=29),
    dict(mon("ZIGZAGOON", "m", 9), hp=5, maxhp=31),
    dict(mon("WINGULL", "f", 11), hp=30, maxhp=31),
    None,
]


# ------------------------------------------------------------------ palettes
def name_colours(m):
    if m is None or m["sex"] is None:
        return None
    return BX.NAME_MALE if m["sex"] == "m" else BX.NAME_FEMALE


def text_pal(m=None, theme="orchid"):
    """BG0/BG1 info palette: SPARE_A/B = hovered mon's name colour (fg, shadow)."""
    nc = name_colours(m)
    if nc:
        return palette(theme, spare_a=nc[0], spare_b=nc[1])
    return palette(theme, spare_a=(40, 40, 64), spare_b=(192, 192, 184))


def gold(pal):
    return D.selected(pal)


# ------------------------------------------------------------------ BG2: slot recess
PIT = SPARE_A                     # BG2 palette: SPARE_A = deep pit colour
PIT_RGB = (64, 40, 88)


def box_pal(theme="orchid"):
    return palette(theme, spare_a=PIT_RGB)


def slot(cv, cx, cy):
    """Round recess: raised accent lip (Gen 3 bevel) around a dark pit with a cast shadow top-left."""
    disc(cv, cx, cy, SLOT_R, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    for y in range(int(cy - 9), int(cy + 10)):
        for x in range(int(cx - 9), int(cx + 10)):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= PIT_R + 1:
                cv.set(x, y, INK)
            if d <= PIT_R:
                ds = math.hypot(x + 0.5 - (cx + 1.5), y + 0.5 - (cy + 1.5))
                cv.set(x, y, PIT if ds <= PIT_R - 0.5 else INK)


def box_layer(cv, dx=0):
    for i in range(COLS * ROWS):
        cx, cy = centre(i)
        slot(cv, cx + dx, cy)


# ------------------------------------------------------------------ OBJ: cursor ring + shadow
def _ring_band(cv, cx, cy, r0, r1, face, light, dark, outline=INK):
    """Raised ring between radii r0 < r1: ink rims, light outer-top-left / inner-bottom-right."""
    for y in range(int(cy - r1 - 2), int(cy + r1 + 2)):
        for x in range(int(cx - r1 - 2), int(cx + r1 + 2)):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = math.hypot(dx, dy)
            up = dx + dy < 0
            if r1 < d <= r1 + 1 or r0 - 1 < d <= r0:
                cv.set(x, y, outline)
            elif r0 < d <= r1:
                c = face
                if d > r1 - 1:
                    c = light if up else dark
                elif d <= r0 + 1:
                    c = dark if up else light
                cv.set(x, y, c)


def cursor_ring(flash=False):
    """32x32 OBJ: gold ring hugging a slot's lip (SELECT ramp). flash = A-press frame."""
    im = new_sheet(32, 32)
    cv = Canvas(im)
    if flash:
        _ring_band(cv, 16, 16, 9.0, 12.0, SELECT_LIGHT, WHITE, SELECT)
    else:
        _ring_band(cv, 16, 16, 9.0, 12.0, SELECT, SELECT_LIGHT, SELECT_DARK)
    return KX.sheet_rgba(im)


def shadow(w=16, h=6):
    """16x8 OBJ: drop shadow under a lifted icon / item (INK oval)."""
    im = new_sheet(16, 8)
    cv = Canvas(im)
    cx, cy = 8, 4
    for y in range(8):
        for x in range(16):
            if ((x + 0.5 - cx) / (w / 2)) ** 2 + ((y + 0.5 - cy) / (h / 2)) ** 2 <= 1:
                cv.set(x, y, INK)
    return KX.sheet_rgba(im, palette("orchid")[:1] + [(16, 16, 24)] + palette("orchid")[2:])


def hand(frame=0):
    """Vanilla hand cursor (alternative B): 0 point, 1 open, 2 fist (graphics/pokemon_storage/hand_cursor.png)."""
    return KX.sprite_rgba(G("pokemon_storage", "hand_cursor.png"), frame, 32)


def hand_shadow():
    return KX.sprite_rgba(G("pokemon_storage", "hand_cursor_shadow.png"))


# ------------------------------------------------------------------ BG1: header tab + buttons
CLOSE_ICON = [          # box with its lid coming down
    "XXXXXXXXX",
    "XXXXXXXXX",
    ".........",
    ".XXXXXXX.",
    ".XXX.XXX.",
    ".XXXXXXX.",
    ".XXXXXXX.",
]


def header_tab(cv, x=TAB[0], y=TAB[1], w=TAB[2], h=TAB[3], cap=TAB_CAP):
    """Box name tab: accent name cap (left) + panel inset holding the mon count (right)."""
    D.label_pill(cv, x, y, w, cap, h)


def button(cv, rect, icon):
    x, y, w, h = rect
    D.label_pill(cv, x, y, w, BTN_CAP, h)
    rows = BX.SILHOUETTES["pokemon"] if icon == "party" else CLOSE_ICON
    iw, ih = len(rows[0]), len(rows)
    BX.silhouette(cv, x + (BTN_CAP - iw) // 2 + 1, y + (h - ih) // 2 - 1 + (icon != "party"), rows, WHITE, ACCENT_DARK)


def button_text(tc, rect, label, fg=INK, sh=PANEL_SHADE):
    x, y, w, h = rect
    tw = text_width(label, "narrow")
    draw_text(tc, x + BTN_CAP + (w - BTN_CAP - tw) // 2 + 1, y - 1, label, fg, sh, font="narrow")


# ------------------------------------------------------------------ BG1: left info panel
MARK_GLYPHS = None


def _marks():
    global MARK_GLYPHS
    if MARK_GLYPHS is None:
        im = Image.open(G("interface", "mon_markings.png")).convert("RGB")
        px = im.load()
        MARK_GLYPHS = []
        for k in range(4):
            g = [[sum(px[k * 8 + x, y]) < 400 for x in range(8)] for y in range(8)]
            MARK_GLYPHS.append(g)
    return MARK_GLYPHS


def markings(cv, x, y, marks, on=ACCENT_DARK, off=PANEL_SHADE):
    """The ROM's four marking shapes (circle, square, triangle, heart), 8x8 each, 9px pitch."""
    for k, g in enumerate(_marks()):
        for yy in range(8):
            for xx in range(8):
                if g[yy][xx]:
                    cv.set(x + 9 * k + xx, y + yy, on if k in marks else off)


def info_art(cv, m=None, item_mode=False):
    """Dais + info pills (BG1). Empty slot -> dais only, pills stay (blank)."""
    cx, cy, ro, ri = DAIS
    D.dais(cv, cx, cy, ro, ri)
    x, y, w = NAME_PILL
    rounded_box(cv, x, y, w, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    lx, ly, lw, lh = LV_PILL
    D.label_pill(cv, lx, ly, lw, 15, lh)
    mx, my, mw = MARK_WELL
    D.well(cv, mx, my, mw, 15, 3)
    ix, iy, iw, ih = ITEM_PILL
    rounded_box(cv, ix, iy, iw, ih, 4, PANEL, INK, WHITE, PANEL_SHADE)
    item_socket(cv, *ITEM_DISC)


def item_socket(cv, cx, cy, r):
    """Round recess the item icon sits in (accent lip, dark pit with a top-left cast shadow)."""
    disc(cv, cx, cy, r, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    pr = r - 3
    for y in range(int(cy - r), int(cy + r + 1)):
        for x in range(int(cx - r), int(cx + r + 1)):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= pr + 1:
                cv.set(x, y, INK)
            if d <= pr:
                ds = math.hypot(x + 0.5 - (cx + 1.5), y + 0.5 - (cy + 1.5))
                cv.set(x, y, ACCENT_DARK if ds <= pr - 0.5 else INK)


import gamefont as _GF
_GF._FONTS.setdefault("narrower", ("latin_narrower.png", "gFontNarrowerLatinGlyphWidths"))   # runtime only


def fit_font(s, w, fonts=("normal", "narrow", "narrower")):
    """Like the ROM's GetFontIdToFit: first font in which s fits in w px."""
    for f in fonts:
        if text_width(s, f) <= w:
            return f
    return fonts[-1]


def item_slug(name):
    return name.lower().replace(" ", "_").replace("é", "e")


def info_text(tc, m, item_name=None):
    """BG0 text for the info panel: name in gender colour, Lv, markings, item."""
    if m is None:
        return
    x, y, w = NAME_PILL
    font = "normal" if text_width(m["name"]) <= w - 10 else "narrow"
    draw_text(tc, x + (w - text_width(m["name"], font)) // 2, y - 1, m["name"], SPARE_A, SPARE_B, font=font)
    lx, ly, lw, lh = LV_PILL
    draw_code(tc, lx + 4, ly + 1, 0x34, WHITE, ACCENT_DARK)        # Lv ligature on the accent cap
    s = str(m["lv"])
    draw_text(tc, lx + lw - 5 - text_width(s, "small"), ly + 1, s, INK, PANEL_SHADE, font="small")
    mx, my, mw = MARK_WELL
    markings(tc, mx + 3, my + 4, m["marks"])
    ix, iy, iw, ih = ITEM_PILL
    it = item_name if item_name is not None else (m["item"] or "None")
    col = (INK, PANEL_SHADE) if (item_name or m["item"]) else (INK_SOFT, PANEL_SHADE)
    x0, x1 = 24, ix + iw - 3                     # text area right of the icon disc
    font = fit_font(it, x1 - x0)
    draw_text(tc, x0 + (x1 - x0 - text_width(it, font)) // 2 + 1, iy, it, col[0], col[1], font=font)


def item_cap_icon(out, m):
    """Real 24x24 item icon (OBJ) centred on the item disc; empty -> plain recess."""
    if not m or not m.get("item"):
        return
    cx, cy, r = ITEM_DISC
    out.alpha_composite(KX.item_icon(item_slug(m["item"])), (int(cx) - 12, int(cy) - 12))


# ------------------------------------------------------------------ BG1: party panel
def party_panel(cv, slide=0):
    """Party panel (BG1): chunky accent band (std frame language) around a deep accent face."""
    x, y, w, h = PARTY_PANEL
    y += slide
    rounded_box(cv, x, y, w, h + 8, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    rounded_box(cv, x + 3, y + 3, w - 6, h + 2, 2, SPARE_A, INK, ACCENT_DARK, SPARE_A)


def party_slot(cv, x, y, m):
    """Small party slot: icon dais disc at the left end of a short pill (Lv + mini HP bar)."""
    if m is None:
        cx, cy = x + 12, y + 13
        disc(cv, cx, cy, 11, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        disc(cv, cx, cy, 7.5, INK, None)
        disc(cv, cx + 0.5, cy + 0.5, 6.5, ACCENT_DARK, None)
        return
    rounded_box(cv, x + 10, y + 4, PSLOT_W - 10, 19, 4, PANEL, INK, WHITE, PANEL_SHADE)
    cx, cy = x + 12, y + 13
    disc(cv, cx, cy, 11.5, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    disc(cv, cx, cy + 0.5, 7.5, ACCENT_DARK, None)
    disc(cv, cx, cy - 0.5, 7, ACCENT, None)
    frac = m["hp"] / m["maxhp"]
    KX.bar(cv, x + 25, y + 16, 15, frac, SPARE_A, SPARE_B, trough=PANEL_DARK, outline=INK, h=2)


def party_slot_text(tc, x, y, m):
    if m is None:
        return
    xx = draw_code(tc, x + 24, y + 4, 0x34, INK, PANEL_SHADE)
    draw_text(tc, xx, y + 4, str(m["lv"]), INK, PANEL_SHADE, font="small")


def party_slot_pal(m, theme="orchid", sel=False):
    lt, dk = KX.hp_ramp(m["hp"] / m["maxhp"]) if m else KX.HP_GREEN
    p = palette(theme, spare_a=lt, spare_b=dk)
    return gold(p) if sel else p


def panel_pal(theme="orchid"):
    return palette(theme, spare_a=PIT_RGB)


# ------------------------------------------------------------------ popups
def box_minimap(cv, x, y, box, cur=None):
    """6x5 occupancy map: 5x5 dots, accent = occupied, recess = empty (jump-to-box popup)."""
    for i in range(COLS * ROWS):
        xx, yy = x + 7 * (i % COLS), y + 7 * (i // COLS)
        if i in box:
            rounded_box(cv, xx, yy, 6, 6, 1, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        else:
            rounded_box(cv, xx, yy, 6, 6, 1, PANEL_DARK, PANEL_SHADE, PANEL_DARK, WHITE, bevel=False)


# ------------------------------------------------------------------ field backdrop (top PC menu state)
def _jasc_pal(path):
    return KX.load_jasc(path)


def field_map(layout="PokemonCenter_1F", primary="building", secondary="pokemon_center", w=14, h=9):
    """Composite a real map layout from its tilesets (metatiles.bin, both layers) -> RGBA (w*16 x h*16)."""
    import struct
    R = KX.ROOT
    p = lambda *a: __import__("os").path.join(R, *a)
    blocks = open(p("data", "layouts", layout, "map.bin"), "rb").read()
    tsets = []
    for kind, name in (("primary", primary), ("secondary", secondary)):
        d = p("data", "tilesets", kind, name)
        tsets.append(dict(tiles=Image.open(d + "/tiles.png"), meta=open(d + "/metatiles.bin", "rb").read(),
                          pals=[_jasc_pal(d + "/palettes/%02d.pal" % i) for i in range(16)]))
    pals = tsets[0]["pals"][:6] + tsets[1]["pals"][6:13]
    out = Image.new("RGBA", (w * 16, h * 16), (0, 0, 0, 255))
    cache = {}

    def tile(idx, pal, hf, vf):
        key = (idx, pal, hf, vf)
        if key in cache:
            return cache[key]
        ts = tsets[0] if idx < 512 else tsets[1]
        ti = idx if idx < 512 else idx - 512
        im = ts["tiles"]
        per = im.size[0] // 8
        t = im.crop(((ti % per) * 8, (ti // per) * 8, (ti % per) * 8 + 8, (ti // per) * 8 + 8))
        t = KX.sheet_rgba(t, pals[pal] if pal < len(pals) else None)
        if hf:
            t = t.transpose(Image.FLIP_LEFT_RIGHT)
        if vf:
            t = t.transpose(Image.FLIP_TOP_BOTTOM)
        cache[key] = t
        return t

    for by in range(h):
        for bx in range(w):
            mid = struct.unpack_from("<H", blocks, 2 * (by * w + bx))[0] & 0x3FF
            ts = tsets[0] if mid < 512 else tsets[1]
            off = (mid if mid < 512 else mid - 512) * 16
            ents = struct.unpack_from("<8H", ts["meta"], off)
            for layer in range(2):
                for k in range(4):
                    e = ents[layer * 4 + k]
                    t = tile(e & 0x3FF, e >> 12, (e >> 10) & 1, (e >> 11) & 1)
                    if layer == 0:
                        t = t.copy()
                        bg = Image.new("RGBA", (8, 8), pals[0][0] + (255,))
                        bg.alpha_composite(t)
                        t = bg
                    out.alpha_composite(t, (bx * 16 + (k % 2) * 8, by * 16 + (k // 2) * 8))
    return out


def player_sprite(folder="brendan", frame=1):
    """Overworld player (16x32 frame; 0 down, 1 up, 2 left)."""
    import os
    base = G("object_events", "pics", "people", folder)
    png = os.path.join(base, "walking.png")
    im = Image.open(png)
    pal = None
    for cand in (G("object_events", "palettes", "brendan.pal"), G("object_events", "palettes", "player.pal")):
        if os.path.exists(cand):
            pal = KX.load_jasc(cand)
            break
    fr = im.crop((frame * 16, 0, frame * 16 + 16, 32))
    return KX.sheet_rgba(fr, pal)


def wallpaper(name="forest"):
    """Vanilla 20x18-tile wallpaper (tiles.4bpp + tilemap.bin, pals from frame.png / bg.png) -> RGBA 160x144."""
    import struct
    d = G("pokemon_storage", "wallpapers", name)
    raw = open(d + "/tiles.4bpp", "rb").read()
    tm = open(d + "/tilemap.bin", "rb").read()
    pals = []
    for f in ("frame.png", "bg.png"):
        p = Image.open(d + "/" + f).getpalette()[:48]
        pals.append([tuple(p[i:i + 3]) for i in range(0, 48, 3)])
    out = Image.new("RGBA", (160, 144), (0, 0, 0, 0))
    px = out.load()
    for cy in range(18):
        for cx in range(20):
            e = struct.unpack_from("<H", tm, 2 * (cy * 20 + cx))[0]
            ti, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            pal = pals[1 if pn >= 2 else 0]
            for y in range(8):
                for x in range(8):
                    b = raw[ti * 32 + y * 4 + x // 2] if ti * 32 + 32 <= len(raw) else 0
                    v = (b >> 4) if x % 2 else (b & 15)
                    if v:
                        sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                        px[cx * 8 + sx, cy * 8 + sy] = snap(pal[v]) + (255,)
    return out


def grid_frame_tint(scroll=0, major=(120, 104, 56), minor=(56, 48, 40)):
    """BG3 grid with a palette swap (MOVE ITEMS mode, like vanilla's scrolling_bg_move_items.pal)."""
    from backdrop import GRID_PAL, grid_index
    pal = [GRID_PAL[0], GRID_PAL[1], snap(minor), snap(major)]
    out = Image.new("RGBA", (W, H))
    p = out.load()
    for y in range(H):
        for x in range(W):
            p[x, y] = pal[grid_index(x - scroll, y - scroll)] + (255,)
    return out


BOX_COLOURS = {
    "orchid": THEMES["orchid"], "male": THEMES["male"], "female": THEMES["female"], "leaf": THEMES["leaf"],
    "teal": [(24, 96, 104), (56, 144, 152), (128, 200, 200), (208, 240, 232)],
    "amber": [(144, 80, 24), (208, 136, 48), (240, 192, 112), (248, 232, 192)],
}
for _k, _v in BOX_COLOURS.items():
    THEMES.setdefault("box_" + _k, _v)      # runtime only (kit.py untouched), like dex_ext's device theme


def box_pal_colour(colour="orchid"):
    return palette("box_" + colour, spare_a=PIT_RGB)
