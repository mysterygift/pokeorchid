"""
Party menu follow-up mocks (review round after implementation):
  hp3_mock.png      3-digit HP on wide + lead slots: current vs narrower digits
  confirm_mock.png  choose-half CONFIRM + CANCEL pills: current vs spaced

usage: mock_party_fixes.py OUT_DIR
"""
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as KX
import gamefont as G
import party_ext as P
import mock_party as M

G._FONTS.setdefault("small_narrower", ("latin_small_narrower.png", "gFontSmallNarrowerLatinGlyphWidths"))
LABEL = (230, 230, 240)
BG = (28, 28, 36)


# ---------------------------------------------------------------- (a) HP numbers
def hp_numbers_font(font):
    """Replacement for party_ext.draw_hp_numbers: right-aligned '%3d/%3d', digit-wide padding, given font."""
    def draw(cv, xr, y, hp, maxhp):
        a, b = P.hp_text(hp, maxhp)
        s = a + b
        dw = G.text_width("0", font)
        x = xr - sum(dw if ch == " " else G.text_width(ch, font) for ch in s)
        for ch in s:
            if ch == " ":
                x += dw
                continue
            x = G.draw_text(cv, x, y, ch, INK, PANEL_SHADE, font=font)
    return draw


VARIANTS = [
    ("Current: FONT_SMALL digits (5px)", hp_numbers_font("small")),
    ("Proposed: FONT_SMALL_NARROWER digits (4px), same right edge", hp_numbers_font("small_narrower")),
]
VALUES = [(999, 999), (149, 149), (52, 52), (5, 31)]


def slot_frame(lead, mon, theme="male"):
    w, h = (80, 56) if lead else (144, 24)
    frame = KX.grid_frame(0, w + 8, h + 8)
    im = P.slot_sheet(theme, mon, lead)
    pal = P.slot_palette(theme, "normal", mon["sex"], mon["hp"] / mon["maxhp"])
    P.composite_sheet(frame, im, pal, (4, 4))
    g = P.LEAD if lead else P.WIDE
    frame.alpha_composite(P.mon_icon(mon["species"], 0, mon["pal"]), (4 + g["icon"][0] - 16, 4 + g["icon"][1] - 16))
    return frame


def tag_gap(lead, hp, maxhp, draw):
    """px between the HP tag's right edge and the first lit HP-number pixel on the same rows (wide slot)."""
    im = new_sheet(144, 24)
    cv = Canvas(im)
    draw(cv, P.WIDE["hpnum_r"], P.WIDE["hpnum_y"], hp, maxhp)
    px = im.load()
    xs = [x for x in range(144) for y in range(24) if px[x, y] in (INK, PANEL_SHADE)]
    tag_r = P.WIDE["hp_tag"][0] + 10
    return min(xs) - tag_r - 1


def hp3_sheet(path):
    k = 3
    base = dict(M.SKARMORY) if hasattr(M, "SKARMORY") else dict(species="skarmory", pal=0, name="Skarmory", sex="f", lv=43)
    cols = len(VALUES)
    cw, ch = 152 + 8, 64 + 8 + 30
    rows = len(VARIANTS)
    sheet = Image.new("RGB", ((cols * cw + 10) * k, (rows * (ch + 24) + 30) * k), BG)
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), "(a) 3-digit HP. Wide slot: tag ends x=103, numbers right-aligned to x=139. Lead slot: numbers under the bar, right edge x=74.", fill=LABEL)
    old = P.draw_hp_numbers
    for r, (title, draw) in enumerate(VARIANTS):
        y0 = 30 + r * (ch + 24)
        d.text((10, y0 * k - 2), title, fill=LABEL)
        P.draw_hp_numbers = draw
        for c, (hp, mx) in enumerate(VALUES):
            mon = dict(base, hp=hp, maxhp=mx)
            x0 = 5 + c * cw
            wide = slot_frame(False, mon)
            lead = slot_frame(True, dict(mon, name="Skarmory"))
            sheet.paste(KX.upscale(wide.convert("RGB"), k), (x0 * k, (y0 + 10) * k))
            sheet.paste(KX.upscale(lead.convert("RGB"), k), (x0 * k, (y0 + 10 + 34) * k))
            gap = tag_gap(False, hp, mx, draw)
            d.text(((x0 + 90) * k, (y0 + 10 + 34 + 20) * k), "%d/%d\nwide: %dpx\nfrom HP tag" % (hp, mx, gap), fill=LABEL)
    P.draw_hp_numbers = old
    sheet.save(path)


# ---------------------------------------------------------------- (b) CONFIRM + CANCEL
def button_sheet(theme, label, font="normal"):
    """= party_ext.cancel_sheet, with a selectable label font."""
    im = new_sheet(48, 16, theme)
    cv = Canvas(im)
    rounded_box(cv, 1, 1, 46, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    G.draw_text(cv, 24 - G.text_width(label, font) // 2, -1, label, INK, PANEL_SHADE, font=font)
    return im


def button(theme, label, selected, font="normal"):
    pal = P.slot_palette(theme, "selected") if selected else palette(theme)
    return KX.sheet_rgba(button_sheet(theme, label, font), pal)


def screen_with_buttons(confirm_y, cancel_y, cursor_confirm=True, confirm_font="normal"):
    old = P.cancel_sheet
    P.cancel_sheet = lambda theme, label="CANCEL": new_sheet(48, 16, theme)      # hide render()'s CANCEL
    im = M.render("male", M.PARTY6, cursor=None, popups=[M.message("Choose POKéMON and confirm.")])
    P.cancel_sheet = old
    im.alpha_composite(button("male", "CONFIRM", cursor_confirm, confirm_font), (192, confirm_y))
    im.alpha_composite(button("male", "CANCEL", not cursor_confirm), (192, cancel_y))
    return im


def confirm_sheet(path):
    k = 3
    # pill art occupies rows 1..14 of each 16px button cell
    variants = [
        ("Current: CONFIRM (24,16) + CANCEL (24,18): 2px gap; CONFIRM label 1px from the outline", 128, 144, "normal"),
        ("Proposed: 4px gap (CONFIRM 1px up, CANCEL 1px down); CONFIRM label in FONT_NARROW", 127, 145, "narrow"),
    ]
    sheet = Image.new("RGB", ((240 * 2 + 30) * k, (40 + 165) * k + 260), BG)
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), "(b) Choose-half (Battle Frontier / Union Room entry): CONFIRM + CANCEL. Slot 6 slab ends at y=126; screen ends at y=159.", fill=LABEL)
    for i, (title, cy, ky, cf) in enumerate(variants):
        x0 = 10 + i * (240 + 10)
        d.text((x0 * k, 24 * k), title, fill=LABEL)
        im = screen_with_buttons(cy, ky, confirm_font=cf)
        sheet.paste(KX.upscale(im.convert("RGB"), k), (x0 * k, 40 * k))
        # 6x zoom of the button stack
        crop = im.crop((184, 120, 240, 160)).convert("RGB")
        sheet.paste(KX.upscale(crop, 6), ((x0 + 4) * k, (40 + 165) * k))
    sheet.save(path)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    hp3_sheet(os.path.join(out, "hp3_mock.png"))
    confirm_sheet(os.path.join(out, "confirm_mock.png"))
    print("ok")
