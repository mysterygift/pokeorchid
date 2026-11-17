"""Design-review sheets: bag states + Orchid window kit. usage: mock_review.py OUT_DIR"""
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import bag_screen as B
import windows as Wn
from gamefont import draw_text, text_width
from mock_bag import render, upscale, ITEMS

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def layer(out, theme, fn):
    """Draw with kit indices on a transparent P layer and composite over `out`."""
    im = new_sheet(out.size[0], out.size[1], theme)
    fn(Canvas(im))
    pal = palette(theme)
    px, opx = im.load(), out.load()
    for y in range(out.size[1]):
        for x in range(out.size[0]):
            if px[x, y]:
                opx[x, y] = pal[px[x, y]] + (255,)


def menu_text(cv, tx, ty, entries, cols, cursor, colw=56, font="narrow"):
    """Gold pill marks the selection (no arrow cursor)."""
    for i, e in enumerate(entries):
        x = tx * 8 + 8 + (i % cols) * colw
        y = ty * 8 + (i // cols) * 16
        if i == cursor:
            Wn.selection_bar(cv, x - 6, y + 1, colw - 2, 14)
        draw_text(cv, x, y, e, INK, PANEL_SHADE, font=font)


# ------------------------------------------------------------------ bag states
def ctx_menu(out, theme):
    def fn(cv):
        Wn.std_frame(cv, 15, 15, 14, 4)
        menu_text(cv, 15, 15, ["USE", "GIVE", "TOSS", "CANCEL"], 2, 0)
    layer(out, theme, fn)


def tray_text(text):
    def fn(out, theme):
        def f(cv):
            cv.rect(40, B.TRAY_Y + 4, 239, 158, PANEL)
            draw_text(cv, B.DESC_X, B.DESC_Y, text, INK, PANEL_SHADE, line_h=B.DESC_LINE_H)
        layer(out, theme, f)
    return fn


def both(*fns):
    def fn(out, theme):
        for f in fns:
            f(out, theme)
    return fn


def message(out, theme):
    def fn(cv):
        Wn.dialogue_box(cv, 2, 15, 27, 4)
        draw_text(cv, 16, 120, "Threw away 1 Potion.", INK, PANEL_SHADE)
    layer(out, theme, fn)


states = []
states.append(("1  Items pocket — browsing (male)", render("male", 0, cursor=1)))
balls = [("Poké Ball", 12, "poke_ball"), ("Great Ball", 4, "great_ball"), ("Ultra Ball", 1, "ultra_ball")]
states.append(("2  Poké Balls — 3 items, unused rows show backdrop (female)",
               render("female", 1, cursor=0, items=balls, desc="A device for catching\nwild Pokémon. It's\nthrown like a ball.")))
states.append(("3  Item selected — context menu",
               render("male", 0, cursor=0, popup=both(tray_text("Potion is\nselected."), ctx_menu))))
states.append(("4  Message box", render("male", 0, cursor=0, popup=message)))
tms = [("№01 Focus Punch", "", "tm"), ("№06 Toxic", "", "tm"), ("№28 Dig", "", "tm"), ("№45 Attract", "", "tm")]
states.append(("5  TMs & HMs pocket",
               render("male", 2, cursor=2, items=tms, desc="The user tunnels\nunderground, then\nattacks next turn.")))
keys = [("Bicycle", "SELECT", "bicycle"), ("Town Map", None, "town_map")]
states.append(("6  Key Items — registered item tag",
               render("female", 4, cursor=0, items=keys, desc="A folding bicycle\nthat is faster than\nrunning shoes.")))
states.append(("7  Scrolled list (thumb moved)", render("male", 0, cursor=5, scroll=2)))

# sheet: 2 columns at 2x with captions
SC = 2
cw, ch = B.W * SC, B.H * SC
cols = 2
rows = (len(states) + cols - 1) // cols
sheet = Image.new("RGBA", (cols * cw + (cols + 1) * 16, rows * (ch + 28) + 16), (28, 28, 36, 255))
d = ImageDraw.Draw(sheet)
for i, (cap, im) in enumerate(states):
    x = 16 + (i % cols) * (cw + 16)
    y = 16 + (i // cols) * (ch + 28)
    d.text((x, y), cap, fill=(230, 230, 240))
    sheet.paste(upscale(im, SC), (x, y + 14))
    upscale(im, 3).save(os.path.join(OUT, "bag_state_%d.png" % (i + 1)))
sheet.save(os.path.join(OUT, "review_bag_states.png"))


# ------------------------------------------------------------------ window kit
def field_scene(theme="orchid", kind="menu"):
    im = new_sheet(240, 160, theme, spare_a=(120, 184, 96), spare_b=(96, 152, 80))
    cv = Canvas(im)
    cv.rect(0, 0, 239, 159, SPARE_A)
    for y in range(0, 160, 8):
        for x in range((y // 8 % 2) * 8, 240, 16):
            cv.rect(x + 2, y + 3, x + 3, y + 4, SPARE_B)
    if kind == "dialogue":
        Wn.dialogue_box(cv, 2, 15, 27, 4)
        draw_text(cv, 16, 120, "Would you like to rest\nyour POKéMON here?", INK, PANEL_SHADE)
        Wn.std_frame(cv, 23, 9, 5, 4)
        Wn.selection_bar(cv, 23 * 8 + 2, 9 * 8 + 1, 36, 14)
        draw_text(cv, 23 * 8 + 8, 72, "YES", INK, PANEL_SHADE)
        draw_text(cv, 23 * 8 + 8, 88, "NO", INK, PANEL_SHADE)
        im._menu_icons = None
        return im
    # start menu: icon + label per row, gold pill on the selection, no arrow
    ents = ["POKéDEX", "POKéMON", "BAG", "POKéNAV", "JAXSON", "SAVE", "OPTION", "EXIT"]
    icon_idx = [0, 1, 2, 3, 4, 5, 6, 7]
    MX, MW = 20, 9
    Wn.std_frame(cv, MX, 1, MW, len(ents) * 2)
    for i, e in enumerate(ents):
        y = 8 + i * 16
        if i == 2:
            Wn.selection_bar(cv, MX * 8 + 2, y + 1, MW * 8 - 4, 14)
        draw_text(cv, MX * 8 + 22, y, e, INK, PANEL_SHADE)
    im._menu_icons = (MX * 8 + 4, 8, icon_idx)
    return im


def kit_sheet():
    themes = ["orchid", "male", "female", "leaf"]
    im = Image.new("RGBA", (16 + 4 * 200, 470), (28, 28, 36, 255))
    d = ImageDraw.Draw(im)
    for ti, th in enumerate(themes):
        ox = 16 + ti * 200
        d.text((ox, 6), "theme: " + th, fill=(230, 230, 240))
        pal = palette(th)
        for i, c in enumerate(pal):
            d.rectangle((ox + (i % 8) * 22, 22 + (i // 8) * 22, ox + (i % 8) * 22 + 20, 22 + (i // 8) * 22 + 20), fill=c)
        # parts on a small backdrop at 2x
        part = new_sheet(88, 136, th)
        cv = Canvas(part)
        from backdrop import backdrop, band, pill
        # backdrop = BW scrolling grid (own layer), composited below
        band(cv, 0, 0, 87, 14)
        cv.hline(0, 87, 15, INK)
        draw_text(cv, 24, -1, "HEADER", WHITE, ACCENT_DARK)
        pill(cv, 4, 20, 80)
        draw_text(cv, 11, 19, "Pill row", INK, PANEL_SHADE, font="narrow")
        Wn.selection_bar(cv, 4, 36, 80)
        draw_text(cv, 11, 35, "Selected", INK, PANEL_SHADE, font="narrow")
        Wn.std_frame(cv, 1, 8, 9, 2)
        draw_text(cv, 12, 64, "Std frame", INK, PANEL_SHADE)
        disc(cv, 20, 108, 11, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
        disc(cv, 46, 108, 9, PANEL, INK, WHITE, PANEL_SHADE)
        stamp(cv, 66, 104, SMALL_ARROW, {"O": INK, "F": ACCENT})
        stamp(cv, 75, 104, SMALL_ARROW, {"O": INK, "F": ACCENT}, hflip=True)
        from backdrop import GRID_PAL, grid_index
        rgba = part.convert("RGBA")
        rp, ip = rgba.load(), part.load()
        for yy in range(part.size[1]):
            for xx in range(part.size[0]):
                if ip[xx, yy] == 0:
                    rp[xx, yy] = GRID_PAL[grid_index(xx, yy)] + (255,)
        im.paste(upscale(rgba, 2), (ox, 72))
    # text_window frame tiles at 4x
    d.text((16, 352), "std frame tiles (graphics/text_window format, 24x24) — orchid / male / female / leaf", fill=(230, 230, 240))
    for ti, th in enumerate(themes):
        im.paste(upscale(Wn.std_frame_tiles(th).convert("RGBA"), 4), (16 + ti * 110, 370))
    return im


def with_menu_icons(im):
    out = im.convert("RGBA")
    if not im._menu_icons:
        return out
    x, y0, idx = im._menu_icons
    path = os.path.join(os.path.dirname(__file__), "..", "..", "graphics", "start_menu", "menu_icons.png")
    if os.path.exists(path):
        from mock_bag import sprite_rgba
        for i, k in enumerate(idx):
            out.alpha_composite(sprite_rgba(path, frame=k, fh=16), (x, y0 + i * 16))
    return out


fa, fb = with_menu_icons(field_scene(kind="menu")), with_menu_icons(field_scene(kind="dialogue"))
pair = Image.new("RGBA", (240 * 2 + 8, 160), (28, 28, 36, 255))
pair.paste(fa, (0, 0))
pair.paste(fb, (248, 0))
upscale(pair, 3).save(os.path.join(OUT, "review_field_windows.png"))
kit_sheet().save(os.path.join(OUT, "review_kit.png"))
print("ok")
