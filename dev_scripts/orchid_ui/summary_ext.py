"""
Pokémon summary screen helpers for the Orchid UI mockups (PROPOSED kit additions
live here until the user approves them).

  * Sample data for the states (real species / ability / move data copied from the
    ROM source: species_info, abilities.h, moves_info.h, level_up_learnsets).
  * Palettes: art (kit roles, gender theme), text (nature up/down + gender names in
    the slots text never uses), move text (PP warning colours, as battle), category
    OBJ palette.
  * New primitives:
      tab_strip()      stepped, brass-trimmed tab header (+ flat dex variant A and
                       icon-button variant C for the comparison sheet)
      socket()         recessed round socket on the dais rim (Poké Ball / status)
      item_row()       party-row style disc well + slab for the held item
      stat_pill()      label pill with an optional bar slot between cap and value
      notch()          dark notch in a pill's bottom edge (PP / met level)
      move_pill()      summary move pill: type cap, name, PP notch (battle language)
      hint_tab()       A / B / START button hint (dark pill + white button disc)
      move_tray()      bottom detail tray: category well + POWER/ACC, description
      category tags    Orchid 16x16 physical / special / status tags (status_icons style)
"""
import os
from PIL import Image
from kit import *
import kit_ext as KX
import dex_ext as D
from gamefont import draw_text, text_width, _font
from battle_ext import NAME_MALE, NAME_FEMALE, draw_code

W, H = 240, 160
G = KX.G


# ================================================================== sample data
class Mon:
    def __init__(self, **kw):
        self.__dict__.update(dict(
            species="grovyle", name="Grovyle", dex=253, lv=18, gender="M", status=None,
            ball="poke", item="miracle_seed", item_name="Miracle Seed", types=["grass"],
            ot="KAITO", ot_gender="M", id_no="04721", nature="Adamant", up="atk", down="spa",
            ability="Overgrow", ability_desc="Ups Grass moves at low HP.",
            met_place="South Tosa Reserve", met_lv=5,
            hp=48, maxhp=52, stats=dict(atk=37, def_=26, spa=37, spd=33, spe=44),
            ivs=dict(hp=24, atk=31, def_=12, spa=8, spd=19, spe=27),
            evs=dict(hp=12, atk=40, def_=4, spa=0, spd=6, spe=28),
            exp=4280, exp_lv=3798, exp_next=4575, moves=None, egg=False, contest=None))
        self.__dict__.update(kw)

    def copy(self, **kw):
        d = dict(self.__dict__)
        d.update(kw)
        return Mon(**d)

    @property
    def exp_frac(self):
        return (self.exp - self.exp_lv) / max(1, self.exp_next - self.exp_lv)


# moves: name, type, pp, maxpp, category, power, accuracy, description (moves_info.h)
MV = {
    "absorb": ("Absorb", "grass", 23, 25, "special", 20, 100,
               "An attack that absorbs\nhalf the damage inflicted."),
    "quick_attack": ("Quick Attack", "normal", 6, 30, "physical", 40, 100,
                     "An extremely fast attack\nthat always strikes first."),
    "pursuit": ("Pursuit", "dark", 9, 20, "physical", 40, 100,
                "Inflicts double damage if\nused on a foe switching out."),
    "fury_cutter": ("Fury Cutter", "bug", 20, 20, "physical", 40, 95,
                    "An attack that intensifies\non each successive hit."),
    "leaf_blade": ("Leaf Blade", "grass", 15, 15, "physical", 90, 100,
                   "Slashes with a sharp leaf.\nHigh critical-hit ratio."),
    "confusion": ("Confusion", "psychic", 21, 25, "special", 50, 100,
                  "A psychic attack that may\ncause confusion."),
    "double_team": ("Double Team", "normal", 15, 15, "status", 0, 0,
                    "Creates illusory copies to\nraise evasiveness."),
    "teleport": ("Teleport", "psychic", 2, 20, "status", 0, 0,
                 "The user switches places\nwith another party Pokémon."),
    "disarming_voice": ("Disarming Voice", "fairy", 15, 15, "special", 40, 0,
                        "Lets out a charming cry\nthat cannot be evaded."),
}
# contest data for the CONTEST page (Gen 3 categories; appeal / jam in hearts)
CONTEST = {"absorb": ("smart", 1, 0), "quick_attack": ("cool", 2, 0),
           "pursuit": ("smart", 2, 0), "fury_cutter": ("cool", 2, 0)}


def hero():
    return Mon(moves=["absorb", "quick_attack", "pursuit", "fury_cutter"])


def heroine_mon():
    return Mon(species="kirlia", name="Kirlia", dex=281, lv=21, gender="F", status="par",
               ball="great", item="oran_berry", item_name="Oran Berry", types=["psychic", "fairy"],
               ot="MAY", ot_gender="F", id_no="31508", nature="Modest", up="spa", down="atk",
               ability="Synchronize", ability_desc="Passes on brn/par/psn.",
               met_place="Tosa Port", met_lv=8, hp=41, maxhp=55,
               stats=dict(atk=21, def_=23, spa=40, spd=33, spe=29),
               exp=8200, exp_lv=7389, exp_next=8721,
               moves=["confusion", "double_team", "teleport", "disarming_voice"])


def egg_mon():
    return Mon(species="egg", name="EGG", dex=None, lv=None, gender=None, item=None, item_name=None,
               ball="poke", egg=True, met_place="Tosa Port", moves=[])


# ================================================================== palettes
# Text palette (BG0): kit roles, plus colours text never needs in the accent slots.
NAT_UP_FG, NAT_DOWN_FG, NAT_UP_SH, NAT_DOWN_SH = SPARE_A, SPARE_B, ACCENT_LIGHT, ACCENT_PALE


def art_pal(theme):
    return palette(theme, spare_a=D.BALL_RED)


def txt_pal(theme):
    p = palette(theme)
    p[NAT_UP_FG], p[NAT_UP_SH] = snap(NAME_FEMALE[0]), snap(NAME_FEMALE[1])
    p[NAT_DOWN_FG], p[NAT_DOWN_SH] = snap(NAME_MALE[0]), snap(NAME_MALE[1])
    return p


def gender_ink(g):
    """(fg, shadow) text indices for a name: male = blue pair, female = rose pair, else INK."""
    return {"M": (NAT_DOWN_FG, NAT_DOWN_SH), "F": (NAT_UP_FG, NAT_UP_SH)}.get(g, (INK, PANEL_SHADE))


# Move text palette: PP warning colours (text_pp.pal) in the free slots, as the battle menu.
PP_FG = {3: (248, 248, 248), 0: (216, 200, 0), 1: (248, 128, 0), 2: (232, 24, 0)}
PP_INDEX = {3: WHITE, 0: ACCENT_PALE, 1: SPARE_A, 2: SPARE_B}


def move_txt_pal(theme):
    p = palette(theme, spare_a=PP_FG[1], spare_b=PP_FG[2])
    p[ACCENT_PALE] = snap(PP_FG[0])
    return p


def selected(pal):
    return D.selected(pal)


def moving(pal):
    """Party 'moving' language: accent face, accent-dark outline."""
    p = list(pal)
    p[PANEL], p[WHITE], p[PANEL_SHADE] = pal[ACCENT_LIGHT], pal[ACCENT_PALE], pal[ACCENT]
    p[INK] = pal[ACCENT_DARK]
    return p


def pp_state(pp, maxpp):
    """GetCurrentPPToMaxPPState: 3 normal, 0 <= 1/2, 1 <= 1/4, 2 empty."""
    if maxpp == pp:
        return 3
    if maxpp <= 2:
        return 3 if pp > 1 else 2 - pp
    if maxpp <= 7:
        return 3 if pp > 2 else 2 - pp
    if pp == 0:
        return 2
    if pp <= maxpp // 4:
        return 1
    if pp > maxpp // 2:
        return 3
    return 0


# ================================================================== category tags (OBJ, 16x16)
# Same construction as status_icons.py: rounded 16x16 tag, Gen 3 bevel, 8x8 pictogram
# centred on the 12x12 face (2px margins). One OBJ palette for all three.
CAT_PAL = [snap(c) for c in [
    (0, 0, 0), (40, 40, 64), (248, 248, 248),
    (216, 72, 48), (144, 32, 32), (248, 208, 72),        # physical: face, dark, burst
    (64, 112, 208), (32, 64, 136), (168, 208, 248),      # special: face, dark, rings
    (160, 160, 152), (96, 96, 104), (232, 232, 224),     # status: face, dark, swirl
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]]
_CAT = {"physical": (3, 4, 5), "special": (6, 7, 8), "status": (9, 10, 11)}
_CAT_PICTO = {
    "physical": ["X..XX..X",      # impact burst
                 ".XXXXXX.",
                 ".XXXXXX.",
                 "XXXXXXXX",
                 "XXXXXXXX",
                 ".XXXXXX.",
                 ".XXXXXX.",
                 "X..XX..X"],
    "special": ["..XXXX..",       # concentric rings
                ".X....X.",
                "X..XX..X",
                "X.X..X.X",
                "X.X..X.X",
                "X..XX..X",
                ".X....X.",
                "..XXXX.."],
    "status": ["..XXXX..",        # split disc (yin-yang)
               ".XXXX.X.",
               "XXXX...X",
               "XXX..X.X",
               "X.X..XXX",
               "X...XXXX",
               ".X.XXXX.",
               "..XXXX.."],
}


def cat_index(kind):
    im = Image.new("P", (16, 16), 0)
    flat = [v for c in CAT_PAL for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    cv = Canvas(im)
    face, dark, pic = _CAT[kind]
    rounded_box(cv, 0, 0, 16, 16, 3, face, 1, 2, dark)
    for r, row in enumerate(_CAT_PICTO[kind]):
        for q, ch in enumerate(row):
            if ch == "X":
                cv.set(4 + q, 4 + r, pic)
    return im


def cat_icon(kind):
    return KX.sheet_rgba(cat_index(kind))


def rom_cat_icon(kind):
    """Expansion's own graphics/interface/category_icons.png (16x16 frames), for comparison."""
    i = ["physical", "special", "status"].index(kind)
    return KX.sprite_rgba(G("interface", "category_icons.png"), i, 16)


# ================================================================== OBJ helpers
def ball_sprite(ball="poke"):
    """graphics/balls/<ball>.png frame 0 (16x16, embedded palette) = the summary's ball OBJ."""
    return KX.sprite_rgba(G("balls", ball + ".png"), 0, 16)


def hold_icon():
    return KX.sprite_rgba(G("party_menu", "hold_icons.png"), 0, 8)


# ================================================================== BG primitives
def socket(cv, cx, cy, r=10.5):
    """Recessed round socket set into the dais band: ink rim, dark well, light lower-right lip."""
    disc(cv, cx, cy, r, ACCENT_DARK, INK)
    ring(cv, cx, cy, r - 1, INK, 1.0)
    import math
    for y in range(int(cy - r), int(cy + r + 1)):
        for x in range(int(cx - r), int(cx + r + 1)):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if r - 2 < d <= r - 1 and (x + 0.5 - cx) + (y + 0.5 - cy) > 3:
                cv.set(x, y, ACCENT)


def tab_strip(cv, tabs, sel, x0, tab_w, gap, style="B", visible=None):
    """
    Header: accent band y 0..15, brass trim (SELECT ramp) y 16..17, ink y 18.
    style B (hero): stepped folder tabs — unselected tabs rise from the trim (y 3..16),
      the selected tab is 2px taller and cuts through the trim (y 1..18).
    style A: flat dex-style tab pills in the band (dex entry page).
    style C: drawn by tab_strip_icons().
    Returns the tab rects [(x, y0, x1, y1)].
    """
    from backdrop import band
    band(cv, 0, 0, W - 1, 15, ACCENT, ACCENT_LIGHT, ACCENT)
    if style == "A":
        cv.hline(0, W - 1, 15, INK)
        rects = []
        for i in range(len(tabs)):
            x = x0 + i * (tab_w + gap)
            rounded_box(cv, x, 1, tab_w, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
            rects.append((x, 1, x + tab_w - 1, 14))
        return rects
    cv.hline(0, W - 1, 16, SELECT)
    cv.hline(0, W - 1, 17, SELECT_DARK)
    cv.hline(0, W - 1, 18, INK)
    for rx in (2, W - 4):                       # brass rivets at the band ends
        cv.set(rx, 6, SELECT_LIGHT)
        cv.set(rx + 1, 6, SELECT)
        cv.set(rx, 7, SELECT)
        cv.set(rx + 1, 7, SELECT_DARK)
    rects = []
    for i in range(len(tabs)):
        if visible is not None and i not in visible:
            rects.append(None)
            continue
        x = x0 + i * (tab_w + gap)
        y0 = 1 if i == sel else 3
        y1 = 18 if i == sel else 16
        h = y1 - y0 + 1
        m = _tab_mask(tab_w, h)
        from battle_ext import mask_box
        mask_box(cv, x, y0, m, PANEL, INK, WHITE, PANEL_SHADE)
        if i != sel:                            # tab foot sits on the trim: reopen the trim under it
            cv.hline(x + 1, x + tab_w - 2, 16, PANEL_SHADE)
        else:                                   # selected tab: foot opens into the page below
            cv.hline(x, x + tab_w - 1, 18, INK)
            cv.hline(x + 1, x + tab_w - 2, 17, PANEL_SHADE)
        rects.append((x, y0, x + tab_w - 1, y1))
    return rects


def _tab_mask(w, h):
    """Folder tab: chunky rounded top corners (r 4), square foot."""
    m = set()
    ins = [4, 2, 1, 1]
    for y in range(h):
        i = ins[y] if y < len(ins) else 0
        for x in range(i, w - i):
            m.add((x, y))
    return m


# Tab pictograms for variant C (white on the tab face, 1px dark drop like the battle buttons).
TAB_ICONS = {
    "info": ["XXXXXXX.",           # ID card
             "X.....X.",
             "X.XX.XX.",
             "X.XX...X",
             "X....XXX",
             "XXXXXXX."],
    "skills": ["......XX",          # bar chart
               "......XX",
               "...XX.XX",
               "...XX.XX",
               "XX.XX.XX",
               "XX.XX.XX"],
    "moves": ["..XXXX..",            # boxing glove (battle FIGHT, simplified)
              ".XXXXXXX",
              "XXXXXXXX",
              "X.XXXXXX",
              ".XXXXXX.",
              "..XXXX.."],
    "contest": ["...X....",          # ribbon rosette
                "..XXX...",
                "XXXXXXX.",
                ".XXXXX..",
                ".XX.XX..",
                "XX...XX."],
}


_KEYPAD = {"A": (0, 7), "B": (8, 7), "START": (50, 14)}   # graphics/fonts/keypad_icons.png columns


def keypad(cv, x, y, button, fg=WHITE, shadow=INK):
    """The ROM's own keypad glyph (CHAR_KEYPAD_ICON), rows 4..11 of keypad_icons.png."""
    im = Image.open(G("fonts", "keypad_icons.png"))
    px = im.load()
    x0, w = _KEYPAD[button]
    for yy in range(4, 12):
        for xx in range(w):
            v = px[x0 + xx, yy]
            if v == 1:
                cv.set(x + xx, y + yy - 4, fg)
            elif v == 2 and shadow is not None:
                cv.set(x + xx, y + yy - 4, shadow)
    return w


def hint_w(button, label, font="small"):
    return 4 + _KEYPAD[button][1] + 3 + text_width(label, font) + 5


def hint_tab(cv, x, y, button, label, font="small"):
    """Button hint: dark accent pill (12 tall), the ROM keypad glyph in WHITE, WHITE label.
    button: 'A', 'B' or 'START'. Returns right edge."""
    w = hint_w(button, label, font)
    rounded_box(cv, x, y, w, 12, 3, ACCENT_DARK, INK, ACCENT, INK)
    gw = keypad(cv, x + 4, y + 2, button, WHITE, INK)
    draw_text(cv, x + 4 + gw + 3, y - 3, label, WHITE, INK, font=font)
    return x + w


def label_pill(cv, x, y, w, cap_w, h=14):
    D.label_pill(cv, x, y, w, cap_w, h)


def notch(cv, x0, x1, y_top, y_bot):
    """Dark ink notch cut into a pill's bottom edge (battle PP counter language)."""
    cv.rect(x0, y_top, x1, y_bot, INK)
    cv.set(x0, y_top, cv.get(x0 - 1, y_top) if cv.get(x0 - 1, y_top) else INK)
    cv.set(x1, y_top, cv.get(x1 + 1, y_top) if cv.get(x1 + 1, y_top) else INK)


def item_row(cv, x, y, w):
    """Held item: party-row disc well (r 11) holding the 24x24 item icon OBJ + slab pill."""
    rounded_box(cv, x + 10, y + 4, w - 10, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    disc(cv, x + 11, y + 11, 11, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    disc(cv, x + 11, y + 11, 8.5, ACCENT_PALE, INK, WHITE, ACCENT_LIGHT)
    return (x + 11, y + 11)


def move_tray(cv, y0, x0=0, x1=W - 1, split=88):
    """Detail tray (bag description tray): seam at y0+3, category well + stats left, desc right."""
    D.tray(cv, y0, H - 1, x0, x1)
    for yy in range(y0 + 5, H - 2):             # stitched divider
        if yy % 4 < 2:
            cv.set(split, yy, PANEL_SHADE)
    # round category well (bag tray item well, smaller)
    disc(cv, 15.5, y0 + 19.5, 11, PANEL, INK, PANEL_SHADE, WHITE)


def move_pill(cv, x, y, w, h=20):
    """Summary move pill art only (state colour comes from the cell palette swap)."""
    rounded_box(cv, x, y, w, h, 4, PANEL, INK, WHITE, PANEL_SHADE)


def pp_notch_rect(x, y, w, h, pp, mx):
    num = "%d/%d" % (pp, mx)
    tw = text_width("PP " + num, "small")
    px = x + w - 8 - tw
    return px - 4, x + w - 5, y + h - 9, y + h - 1, px, num


# ---------------------------------------------------------------- header variant C (icon tabs)
TAB_C_SEL, TAB_C_W, TAB_C_GAP = 72, 26, 3
TAB_KEYS = ["info", "skills", "moves", "contest"]


def tab_strip_icons(cv, sel, n=4):
    """Variant C: same stepped brass header; unselected tabs are icon-only, the selected
    tab widens to icon + label. Returns rects; caller prints only the selected label."""
    from battle_ext import mask_box
    tab_strip(cv, [], -1, 0, 0, 0, "B")          # band + trim + rivets only
    total = TAB_C_SEL + (n - 1) * TAB_C_W + (n - 1) * TAB_C_GAP
    x = (W - total) // 2
    rects = []
    for i in range(n):
        w = TAB_C_SEL if i == sel else TAB_C_W
        y0, y1 = (1, 18) if i == sel else (3, 16)
        mask_box(cv, x, y0, _tab_mask(w, y1 - y0 + 1), PANEL, INK, WHITE, PANEL_SHADE)
        if i != sel:
            cv.hline(x + 1, x + w - 2, 16, PANEL_SHADE)
        else:
            cv.hline(x, x + w - 1, 18, INK)
            cv.hline(x + 1, x + w - 2, 17, PANEL_SHADE)
        icon = TAB_ICONS[TAB_KEYS[i]]
        ix = x + 5 if i == sel else x + (w - 8) // 2
        iy = (y0 + y1) // 2 - 3 - (1 if i == sel else 0)
        stamp(cv, ix + 1, iy + 1, icon, {"X": PANEL_SHADE})
        stamp(cv, ix, iy, icon, {"X": INK if i == sel else INK_SOFT})
        rects.append((x, y0, x + w - 1, y1))
        x += w + TAB_C_GAP
    return rects
