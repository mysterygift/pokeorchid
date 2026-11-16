"""
Orchid party menu — slot art, slot palettes and sprite loaders (PROPOSED, mockup only).

Maps onto src/party_menu.c (PARTY_LAYOUT_SINGLE):
    BG0  slot windows (art + text blitted into each window, per-slot palette 3..8),
         CANCEL text window             -> sSinglePartyMenuWindowTemplate, sCancelButtonWindowTemplate
    BG1  CANCEL button art (was bg.bin + cancel_button.bin; the old patterned bg is dropped)
    BG2  message / action / yes-no windows (std frame, palette 13/14/15)
    BG3  BW scrolling grid (unused by vanilla party_menu.c -> free)

Slot palette (one per window, swapped by LoadPartyBoxPalette) keeps the kit role layout
with three per-slot overrides:
    11 GENDER    gender glyph colour (blue / red)  (SELECT_DARK slot is free in a slot palette)
    14 HP_LIGHT  HP bar light row  (Gen 3 ramp, swapped green/yellow/red like sHPBar*PalIds)
    15 HP_DARK   HP bar body
States are pure palette swaps of the same tiles: normal / selected (gold) / moving (accent) /
moving+selected / fainted (rose) / fainted+selected.
"""
import os
from PIL import Image
from kit import *
import kit_ext as KX
from gamefont import draw_text, text_width, _font

GENDER, HP_LIGHT, HP_DARK = SELECT_DARK, SPARE_A, SPARE_B

W, H = 240, 160
# ---------------------------------------------------------------- window geometry (tiles)
LEAD_WIN = (1, 3, 10, 7)                       # sSinglePartyMenuWindowTemplate[0]
def RIGHT_WIN(k):                              # k = 0..4 -> party slots 2..6
    return (12, 1 + 3 * k, 18, 3)
CANCEL_WIN = (24, 17, 6, 2)                    # sCancelButtonWindowTemplate
MSG_WIN = (1, 17, 21, 2)                       # sDefaultPartyMsgWindowTemplate
DOWHAT_WIN = (1, 17, 18, 2)                    # sDoWhatWithMonMsgWindowTemplate (16 -> 18 wide)


def slot_win(i):
    return LEAD_WIN if i == 0 else RIGHT_WIN(i - 1)


def slot_px(i):
    tx, ty, tw, th = slot_win(i)
    return tx * 8, ty * 8, tw * 8, th * 8


# ---------------------------------------------------------------- slot geometry (window-relative px)
# wide slot 144x24: accent disc (icon dais) at the left end, slab behind it
WIDE = dict(disc=(12, 11.5, 11.0), slab=(10, 1, 132, 22),
            name=(27, 0), lv=(27, 9), sex_x=49, status=(58, 13),
            hp_tag=(83, 3), bar=(95, 4, 40), hpnum_r=139, hpnum_y=9,
            icon=(12, 7), hold=(20, 16), desc=(88, 0))
# lead slot 80x56: bigger disc top-left, name block right of it, HP row along the bottom
LEAD = dict(disc=(16, 19.5, 13.0), slab=(1, 5, 78, 50),
            name=(31, 5), lv=(31, 15), sex_x=54, status=(31, 28),
            hp_tag=(6, 38), bar=(19, 39, 48), hpnum_r=74, hpnum_y=40,
            icon=(16, 15), hold=(22, 29), desc=(8, 38))


# ---------------------------------------------------------------- palettes
ROSE = [(232, 224, 224), (208, 196, 200), (168, 152, 160)]          # fainted face: light / face / shade (greyed rose)
GREY = [(80, 80, 96), (136, 136, 152), (176, 176, 184), (208, 208, 216)]  # drained accent ramp


def slot_palette(theme="male", state="normal", gender=None, hp=1.0):
    """16 RGB for one slot window. state: normal|selected|moving|moving_sel|fainted|fainted_sel|empty."""
    base = palette(theme)
    p = list(base)
    p[GENDER] = KX.MALE_BLUE if gender == "m" else KX.FEMALE_RED if gender == "f" else base[INK_SOFT]
    lt, dk = KX.hp_ramp(hp)
    p[HP_LIGHT], p[HP_DARK] = lt, dk
    if state.startswith("fainted"):
        p[WHITE], p[PANEL], p[PANEL_SHADE] = ROSE
        p[ACCENT_DARK], p[ACCENT], p[ACCENT_LIGHT], p[ACCENT_PALE] = GREY
    if state in ("selected", "moving_sel", "fainted_sel"):
        p[PANEL], p[WHITE], p[PANEL_SHADE] = base[SELECT], base[SELECT_LIGHT], base[SELECT_DARK]
    if state == "moving":
        p[PANEL], p[WHITE], p[PANEL_SHADE] = base[ACCENT_LIGHT], base[ACCENT_PALE], base[ACCENT]
    if state in ("moving", "moving_sel"):
        p[INK] = base[ACCENT_DARK]           # outline turns accent: reads as "picked up"
    return [snap(c) for c in p]


# ---------------------------------------------------------------- small pixel stamps
HP_GLYPH = ["X.X.XX.",
            "X.X.X.X",
            "XXX.XX.",
            "X.X.X..",
            "X.X.X.."]


def hp_tag(cv, x, y):
    """11x7 'HP' plate in the theme accent (like Gen 3's HP label), letters WHITE."""
    rounded_box(cv, x, y, 11, 7, 1, ACCENT_DARK, ACCENT_DARK, ACCENT_DARK, ACCENT_DARK, bevel=False)
    stamp(cv, x + 2, y + 1, HP_GLYPH, {"X": WHITE})


def draw_code(cv, x, y, code, fg, shadow, font="small"):
    """Draw one raw charmap glyph (e.g. 0x34 = {LV})."""
    px, widths = _font(font)
    ox, oy = (code % 16) * 16, (code // 16) * 16
    w = widths[code]
    for gy in range(16):
        for gx in range(min(w, 16)):
            v = px[ox + gx, oy + gy]
            if v == 1:
                cv.set(x + gx, y + gy, fg)
            elif v == 2 and shadow is not None:
                cv.set(x + gx, y + gy, shadow)
    return x + w


def draw_lv(cv, x, y, level, fg=INK, sh=PANEL_SHADE):
    x = draw_code(cv, x, y, 0x34, fg, sh)
    return draw_text(cv, x, y, str(level), fg, sh, font="small")


def hp_text(hp, maxhp):
    """ROM style: '%3d/' then '%3d' (right-aligned, digit-wide spaces) -> ' 35/ 52'."""
    return "%3d/" % hp, "%3d" % maxhp


def sp_width(s, font="small"):
    # ConvertIntToDecimalStringN pads with CHAR_SPACER? party uses digit-width spaces; approximate
    return sum(text_width("0" if ch == " " else ch, font) for ch in s)


def draw_hp_numbers(cv, xr, y, hp, maxhp):
    a, b = hp_text(hp, maxhp)
    x = xr - sp_width(a + b)
    for ch in a + b:
        if ch == " ":
            x += text_width("0", "small")
            continue
        x = draw_text(cv, x, y, ch, INK, PANEL_SHADE, font="small")


# ---------------------------------------------------------------- slot art
def _dais(cv, g):
    cx, cy, r = g["disc"]
    disc(cv, cx, cy, r, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
    disc(cv, cx, cy + 0.5, r - 4, ACCENT_DARK, None)      # recessed socket the icon stands in
    disc(cv, cx, cy - 0.5, r - 4.5, ACCENT, None)


def draw_slot(cv, mon, lead=False, mode="hp"):
    """mon: dict(name, sex 'm'/'f'/None, lv, hp, maxhp, status, item). mode: hp | able | notable."""
    g = LEAD if lead else WIDE
    sx, sy, sw, sh = g["slab"]
    rounded_box(cv, sx, sy, sw, sh, 4, PANEL, INK, WHITE, PANEL_SHADE)
    _dais(cv, g)
    nx, ny = g["name"]
    draw_text(cv, nx, ny, mon["name"], INK, PANEL_SHADE, font="small")
    lx, ly = g["lv"]
    draw_lv(cv, lx, ly, mon["lv"])
    if mon.get("sex"):
        draw_code(cv, g["sex_x"], ly, 0xB5 if mon["sex"] == "m" else 0xB6, GENDER, PANEL_SHADE)
    if mode == "hp":
        hp_tag(cv, *g["hp_tag"])
        bx, by, bw = g["bar"]
        KX.bar(cv, bx, by, bw, mon["hp"] / mon["maxhp"], HP_LIGHT, HP_DARK, trough=PANEL_DARK, outline=INK, h=3)
        draw_hp_numbers(cv, g["hpnum_r"], g["hpnum_y"], mon["hp"], mon["maxhp"])
    else:
        able_tag(cv, g, mode == "able")


def able_tag(cv, g, able):
    """TM / evolution-stone check: replaces the HP row (vanilla prints ABLE / NOT ABLE text there)."""
    label = "ABLE" if able else "NOT ABLE"
    w = text_width(label, "small") + 10
    if g is LEAD:
        x, y = 40 - w // 2, 38
    else:
        x, y = 139 - w - 1, 5
    face, sh = (ACCENT, ACCENT_DARK) if able else (PANEL_DARK, INK_SOFT)
    rounded_box(cv, x, y, w, 13, 3, face, INK, ACCENT_LIGHT if able else PANEL_SHADE, sh)
    draw_text(cv, x + 5, y - 2, label, WHITE, sh, font="small")


def slot_sheet(theme, mon, lead=False, mode="hp"):
    w, h = (80, 56) if lead else (144, 24)
    im = new_sheet(w, h, theme)
    draw_slot(Canvas(im), mon, lead, mode)
    return im


def cancel_sheet(theme, label="CANCEL"):
    """BG1 button art + BG0 label for the 6x2-tile CANCEL window (x 192..239, y 136..151)."""
    im = new_sheet(48, 16, theme)
    cv = Canvas(im)
    rounded_box(cv, 1, 1, 46, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, 24 - text_width(label) // 2, -1, label, INK, PANEL_SHADE)
    return im


# ---------------------------------------------------------------- OBJ sprites (real ROM art)
G = KX.G


def mon_icon(species, frame=0, pal_index=0):
    """P_GBA_STYLE_SPECIES_ICONS is FALSE in this repo -> icon.png + the non-GBA iconPalIndex."""
    png = G("pokemon", species, "icon.png")
    pal = KX.load_jasc(G("pokemon", "icon_palettes", "pal%d.pal" % pal_index))
    return KX.sprite_rgba(png, frame, 32, pal)


STATUS_ROW = {"psn": 0, "par": 1, "slp": 2, "frz": 3, "brn": 4, "pkrs": 5, "fnt": 6, "frb": 7}


def status_icon(kind):
    """32x8 OBJ from graphics/interface/status_icons.png (embedded palette)."""
    return KX.sprite_rgba(G("interface", "status_icons.png"), STATUS_ROW[kind], 8)


def hold_icon(mail=False):
    """8x8 OBJ from graphics/party_menu/hold_icons.png (frame 0 item, 1 mail)."""
    return KX.sprite_rgba(G("party_menu", "hold_icons.png"), 1 if mail else 0, 8)


def composite_sheet(out, im, pal, at):
    out.alpha_composite(KX.sheet_rgba(im, pal), at)


def safe_comp(out, spr, x, y):
    """alpha_composite that clips sprites/windows hanging off the screen edge (slide animation)."""
    x, y = int(x), int(y)
    sx, sy = max(0, -x), max(0, -y)
    if sx >= spr.size[0] or sy >= spr.size[1] or x >= out.size[0] or y >= out.size[1]:
        return
    out.alpha_composite(spr, (x + sx, y + sy), (sx, sy))
