"""
Pixel-accurate mockups of the Orchid Pokédex ("Gen 5 layout, Gen 3 pixels").

LIST SCREEN layers (bottom-up, like the GBA):
    BG3  scrolling BW grid (own palette)
    BG2  list window: pill rows + number + name + caught ball, scrolls vertically
         (BG2VOFS); cursor row cells use palette 1 (gold variant)
    BG1  static art: header band, SEEN/OWN pills, dais, scrollbar track
    BG0  text: header title, counts
    OBJ  species pic (64x64) on the dais, type icons, scroll thumb, red chevrons
ENTRY SCREEN (INFO tab): BG3 grid, BG1 art (tabs, dais, pills, footprint well,
    tray), BG0 text, OBJ pic + type icons + chevrons. BG2 is free.

usage: mock_dex.py OUT_DIR
"""
import os
import sys
import json
from PIL import Image
from kit import *
import kit_ext as KX
import dex_ext as D
from gamefont import draw_text, text_width

W, H = 240, 160

# ------------------------------------------------------------------ layout: list
HEADER = (96, 0, 239, 15)
TITLE_CX = 166
HEADER_ARROWS = ((130, 8), (202, 8))
LIST_Y, ROW_H, ROWS = 16, 16, 9
PILL_X, PILL_W, PILL_H = 101, 130, 14
TRACK = (233, 17, 238, 158)
CURSOR_MARGIN = 2              # list scrolls when the cursor gets this close to the edge
COUNT_PILLS = ((4, 3), (4, 20))
COUNT_W, COUNT_CAP = 88, 36
DAIS_C, DAIS_R, DAIS_IN = (48, 86), 42, 32
TYPES_Y = 137

# ------------------------------------------------------------------ layout: entry
TABS = ["INFO", "AREA", "CRY", "SIZE"]
TAB_W, TAB_GAP = 44, 4
TAB_X0 = (W - (4 * TAB_W + 3 * TAB_GAP)) // 2
TAB_ARROWS = ((12, 8), (227, 8))
E_DAIS_C, E_DAIS_R, E_DAIS_IN = (45, 58), 39, 31
E_X, E_W = 92, 144
E_NAME_Y, E_CAT_Y, E_TYPES_Y, E_HW_Y = 20, 38, 57, 79
E_NUM_CAP = 30
HW_CAP = 24
FOOT_WELL = (210, 54, 25, 22)
AREA_WELL = (E_X, 38, E_X + E_W - 1, 93)
E_TRAY_Y = 100
DESC_X, DESC_Y, DESC_PITCH = 7, E_TRAY_Y + 2, 14

# ------------------------------------------------------------------ sample save data
# TOSA dex stand-in: the ROM's current regional (Hoenn-order) list + real species data.
# c = caught, s = seen, else unseen.
STATUS = ("c c . s . . s . . c s c c . c s . c s c s . c . . c s c s c . "
          "s c . . c s . . c . s . . s c . . c . s . . . c . . s").split()
LIST_LEN = len(STATUS)                 # vanilla: the list ends at the last seen entry


def dex_entries():
    order = D.hoenn_order()
    out = []
    for i, st in enumerate(STATUS):
        out.append({"num": i + 1, "const": order[i], "seen": st in "cs", "caught": st == "c"})
    return out


ENTRIES = dex_entries()
SEEN = 87      # whole-dex totals shown in the header pills
OWN = 41


def info(entry):
    return D.species(entry["const"])


# ------------------------------------------------------------------ helpers
def compose(out, im, pal):
    out.alpha_composite(KX.sheet_rgba(im, pal))


def sheet(theme):
    return new_sheet(W, H, theme, spare_a=D.BALL_RED)


def first_visible(cursor, top, n=LIST_LEN):
    """BW-style: cursor moves freely; the list scrolls when it nears the edge."""
    if cursor < top + CURSOR_MARGIN:
        top = cursor - CURSOR_MARGIN
    if cursor > top + ROWS - 1 - CURSOR_MARGIN:
        top = cursor - (ROWS - 1 - CURSOR_MARGIN)
    return max(0, min(top, max(0, n - ROWS)))


# ------------------------------------------------------------------ list screen
def draw_list_art(cv):
    """BG1: header band, count pills, dais, scrollbar track."""
    D.header_band(cv, *HEADER[0::2])
    for x, y in COUNT_PILLS:
        D.label_pill(cv, x, y, COUNT_W, COUNT_CAP)
    D.dais(cv, DAIS_C[0], DAIS_C[1], DAIS_R, DAIS_IN)
    D.track(cv, *TRACK)


def draw_row(cv, y, e, theme_info=None):
    """One BG2 list row (pill + text) with its cell top at y."""
    rounded_box(cv, PILL_X, y + 1, PILL_W, PILL_H, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, PILL_X + 6, y, "%03d" % e["num"], INK, PANEL_SHADE, font="narrow")
    if e["seen"]:
        draw_text(cv, PILL_X + 28, y, info(e)["name"], INK, PANEL_SHADE, font="narrow")
    else:
        draw_text(cv, PILL_X + 28, y, "-----", INK_SOFT, PANEL_SHADE, font="narrow")
    if e["caught"]:
        D.caught_ball(cv, PILL_X + PILL_W - 15, y + 4)


def render_list(theme="orchid", cursor=0, top=None, scroll_px=None, grid_scroll=0, sprite_dx=0,
                hide_sprite=False, flash=False, list_dx=0, fade=0.0, sprite_pos=None, extra=None):
    """
    cursor = entry index; top = first visible entry (auto if None); scroll_px overrides the
    BG2 vertical offset for in-between scroll frames. fade darkens BG0-2 (BLDY) for transitions.
    """
    pal = D.dex_palette(theme)
    sel = D.selected(pal)
    if flash:
        sel = list(sel)
        sel[SELECT] = sel[SELECT_LIGHT]
    if top is None:
        top = first_visible(cursor, 0)
    if scroll_px is None:
        scroll_px = top * ROW_H
    out = KX.grid_frame(grid_scroll)
    ui = KX.blank()

    # BG2 list window (normal rows, then the cursor row with the gold palette)
    rows, cur = sheet(theme), sheet(theme)
    rc, cc = Canvas(rows), Canvas(cur)
    for i, e in enumerate(ENTRIES):
        y = LIST_Y + i * ROW_H - scroll_px
        if -ROW_H < y < H:
            draw_row(cc if i == cursor else rc, y, e)
    lay = KX.sheet_rgba(rows, pal)
    lay.alpha_composite(KX.sheet_rgba(cur, sel))
    ui.alpha_composite(lay, (list_dx, 0))

    # BG1 art + BG0 text
    art = sheet(theme)
    draw_list_art(Canvas(art))
    compose(ui, art, pal)
    txt = sheet(theme)
    tc = Canvas(txt)
    title = "TOSA"
    draw_text(tc, TITLE_CX - text_width(title) // 2, 0, title, WHITE, ACCENT_DARK)
    for (x, y), lab, n in zip(COUNT_PILLS, ("SEEN", "OWN"), (SEEN, OWN)):
        draw_text(tc, x + (COUNT_CAP - text_width(lab)) // 2 + 1, y - 1, lab, WHITE, ACCENT_DARK)
        s = "%d" % n
        draw_text(tc, x + COUNT_W - 7 - text_width(s), y - 1, s, INK, PANEL_SHADE)
    compose(ui, txt, pal)
    if fade:
        ui = darken(ui, fade)
    out.alpha_composite(ui)

    # OBJ
    e = ENTRIES[cursor]
    if not hide_sprite:
        spr = D.mon_pic(info(e)["folder"])
        if not e["seen"]:
            spr = D.silhouette(spr)
        cx, stage = sprite_pos or (DAIS_C[0], DAIS_C[1] + int(DAIS_IN * 0.55) + 3)
        bottom = D.sprite_bottom(spr)
        out.alpha_composite(spr, (cx - 32 + sprite_dx, stage - bottom))
    if e["seen"] and not fade:
        types_obj(out, info(e)["types"], DAIS_C[0], TYPES_Y)
    if LIST_LEN > ROWS and not fade:
        tx0, ty0, tx1, ty1 = TRACK
        span = (ty1 - ty0 - 3) - 12
        D.thumb(out, tx0 + 1, ty0 + 2 + span * scroll_px // ((LIST_LEN - ROWS) * ROW_H), theme)
    for i, (ax, ay) in enumerate(HEADER_ARROWS if not fade else ()):
        D.chevron(out, ax, ay, right=i == 1)
    if extra:
        extra(out, theme)
    return out


def types_obj(out, types, cx, y):
    icons = [KX.type_icon(t) for t in types]
    total = 32 * len(icons) + 4 * (len(icons) - 1)
    x = cx - total // 2
    for ic in icons:
        out.alpha_composite(ic, (x, y))
        x += 36


def darken(im, k):
    """GBA BLDY darken on the UI layers (k 0..1, snapped to 1/16 steps)."""
    k = round(k * 16) / 16
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (int(r * (1 - k)) // 8 * 8, int(g * (1 - k)) // 8 * 8, int(b * (1 - k)) // 8 * 8, a)
    return im


# ------------------------------------------------------------------ entry screen
def draw_entry_art(cv, tab=0):
    """BG1: full-width header with tab pills, dais, info pills, footprint well, tray."""
    D.header_band(cv, 0, W - 1, round_left=False)
    for i in range(4):
        D.tab_pill(cv, TAB_X0 + i * (TAB_W + TAB_GAP), 1, TAB_W)
    D.dais(cv, E_DAIS_C[0], E_DAIS_C[1], E_DAIS_R, E_DAIS_IN)
    D.label_pill(cv, E_X, E_NAME_Y, E_W, E_NUM_CAP)
    if tab == 1:                       # AREA: one big map well replaces the info pills
        x0, y0, x1, y1 = AREA_WELL
        D.well(cv, x0, y0, x1 - x0 + 1, y1 - y0 + 1, r=4)
        D.tray(cv, E_TRAY_Y)
        return
    rounded_box(cv, E_X, E_CAT_Y, E_W, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    D.label_pill(cv, E_X, E_HW_Y, 70, HW_CAP)
    D.label_pill(cv, E_X + E_W - 70, E_HW_Y, 70, HW_CAP)
    fx, fy, fw, fh = FOOT_WELL
    D.well(cv, fx, fy, fw, fh)
    D.tray(cv, E_TRAY_Y)


def tab_cells_selected(tab):
    x = TAB_X0 + tab * (TAB_W + TAB_GAP)
    return (x, 1, x + TAB_W - 1, 14)


def render_entry(theme="orchid", entry_index=0, tab=0, grid_scroll=0, fade=0.0, sprite_dx=0,
                 body=None, show_sprite=True):
    pal = D.dex_palette(theme)
    sel = D.selected(pal)
    e = ENTRIES[entry_index]
    sp = info(e)
    out = KX.grid_frame(grid_scroll)
    ui = KX.blank()

    art = sheet(theme)
    ac = Canvas(art)
    draw_entry_art(ac, tab)
    a = KX.sheet_rgba(art, pal)
    # selected tab: its cells use palette 1 (gold variant); the pill fills its cells' PANEL pixels only
    x0, y0, x1, y1 = tab_cells_selected(tab)
    a.alpha_composite(KX.sheet_rgba(art.crop((x0, y0, x1 + 1, y1 + 1)), sel), (x0, y0))
    ui.alpha_composite(a)

    txt = sheet(theme)
    tc = Canvas(txt)
    for i, name in enumerate(TABS):
        x = TAB_X0 + i * (TAB_W + TAB_GAP)
        fg, sh = (INK, SELECT_DARK) if i == tab else (INK_SOFT, PANEL_SHADE)
        draw_text(tc, x + (TAB_W - text_width(name)) // 2, 0, name, fg, sh)
    num = "%03d" % e["num"]
    draw_text(tc, E_X + (E_NUM_CAP - text_width(num)) // 2 + 1, E_NAME_Y - 1, num, WHITE, ACCENT_DARK)
    draw_text(tc, E_X + E_NUM_CAP + 6, E_NAME_Y - 1, sp["name"], INK, PANEL_SHADE)
    if e["caught"]:
        D.caught_ball(tc, E_X + E_W - 15, E_NAME_Y + 3)
    if tab == 1:
        x0, y0, x1, y1 = AREA_WELL
        for k, line in enumerate(("Region map", "(BG2, own palette)")):
            draw_text(tc, (x0 + x1) // 2 - text_width(line, "narrow") // 2, (y0 + y1) // 2 - 16 + k * 14,
                      line, INK_SOFT, None, font="narrow")
        (body or area_body)(tc, ac, sp)
    else:
        info_text(tc, sp, body, e["caught"])
    compose(ui, txt, pal)
    if fade:
        ui = darken(ui, fade)
    out.alpha_composite(ui)

    if show_sprite:
        spr = D.mon_pic(sp["folder"])
        stage = E_DAIS_C[1] + int(E_DAIS_IN * 0.55) + 3
        out.alpha_composite(spr, (E_DAIS_C[0] - 32 + sprite_dx, stage - D.sprite_bottom(spr)))
    if not fade and tab != 1:
        icons = [KX.type_icon(t) for t in sp["types"]]
        for k, ic in enumerate(icons):
            out.alpha_composite(ic, (E_X + 2 + 36 * k, E_TYPES_Y))
    for i, (ax, ay) in enumerate(TAB_ARROWS if not fade else ()):
        D.chevron(out, ax, ay, right=i == 1)
    return out


def info_text(tc, sp, body=None, caught=True):
    """Gen 3 rule: seen-but-not-caught shows ????? category, unknown HT/WT, no description."""
    cat = (sp["category"] if caught else "?????") + " POKéMON"
    draw_text(tc, E_X + (E_W - text_width(cat, "narrow")) // 2, E_CAT_Y - 1, cat, INK, PANEL_SHADE, font="narrow")
    ht, wt = (D.fmt_height(sp["height"]), D.fmt_weight(sp["weight"])) if caught else ("???.? m", "???.? kg")
    for k, (lab, val) in enumerate((("HT", ht), ("WT", wt))):
        x = E_X + k * (E_W - 70)
        draw_text(tc, x + (HW_CAP - text_width(lab)) // 2 + 1, E_HW_Y - 1, lab, WHITE, ACCENT_DARK)
        draw_text(tc, x + 70 - 7 - text_width(val, "narrow"), E_HW_Y - 1, val, INK, PANEL_SHADE, font="narrow")
    fx, fy, fw, fh = FOOT_WELL
    m = D.footprint_mask(sp["folder"])
    for yy in range(16):
        for xx in range(16):
            if m[yy][xx]:
                tc.set(fx + (fw - 16) // 2 + xx, fy + (fh - 16) // 2 + yy, INK)
    if body:
        body(tc, None, sp)
    elif caught:
        draw_text(tc, DESC_X, DESC_Y, sp["desc"], INK, PANEL_SHADE, line_h=DESC_PITCH)


# ------------------------------------------------------------------ AREA tab placeholder
def area_body(tc, ac, sp):
    draw_text(tc, DESC_X, DESC_Y, "%s lives in:\nSouth Tosa Reserve (grass)\nTosa Port (fishing)" % sp["name"],
              INK, PANEL_SHADE, line_h=DESC_PITCH)


# ------------------------------------------------------------------ search menu (std-window style)
SEARCH_ROWS = [("ORDER", "Numerical"), ("NAME", "ABC"), ("TYPE", None), ("MODE", "TOSA")]
S_X, S_W, S_CAP, S_Y0, S_PITCH = 16, 208, 56, 24, 20
S_BTN_X, S_BTN_Y, S_BTN_W = (40, 128), 112, 72
S_TRAY_Y = 136
# TYPE row: two fixed recessed sockets (always drawn, so the row reads as two fields), centred in
# the pill's value area (x 73-222). A set slot shows its 32x16 icon centred in the socket; an
# unset slot shows a quiet "ANY" in INK_SOFT. The sockets fill the row's two tile rows (y 64-79,
# 2px below the 14px pill) so the gold row swap never touches the NAME / MODE rows.
SOCKET_W, SOCKET_H, SOCKET_GAP = 36, 16, 12
SOCKET_Y = S_Y0 + 2 * S_PITCH


def socket_x(k):
    x0, x1 = S_X + S_CAP + 1, S_X + S_W - 2
    total = 2 * SOCKET_W + SOCKET_GAP
    return (x0 + x1 + 1) // 2 - total // 2 + k * (SOCKET_W + SOCKET_GAP)


def search_row_art(cv, i):
    D.label_pill(cv, S_X, S_Y0 + i * S_PITCH, S_W, S_CAP)
    if i == 2:
        for k in range(2):
            D.well(cv, socket_x(k), SOCKET_Y, SOCKET_W, SOCKET_H)


def search_art(cv, cur=None, cursor=-1):
    """BG art of the search page; the cursor row / button goes on `cur` (gold palette)."""
    D.header_band(cv, 0, W - 1, round_left=False)
    for i in range(4):
        search_row_art(cur if (cur is not None and i == cursor) else cv, i)
    for k, xx in enumerate(S_BTN_X):
        c = cur if (cur is not None and cursor == 4 + k) else cv
        rounded_box(c, xx, S_BTN_Y, S_BTN_W, 18, 4, PANEL, INK, WHITE, PANEL_SHADE)
    D.tray(cv, S_TRAY_Y)


def render_search(theme="orchid", cursor=0, grid_scroll=0, types=("grass", "water"), slot=0):
    pal = D.dex_palette(theme)
    sel = D.selected(pal)
    out = KX.grid_frame(grid_scroll)
    art, cur, txt = sheet(theme), sheet(theme), sheet(theme)
    ac, cc, tc = Canvas(art), Canvas(cur), Canvas(txt)
    search_art(ac, cc, cursor)
    draw_text(tc, (W - text_width("SEARCH")) // 2, 0, "SEARCH", WHITE, ACCENT_DARK)
    for i, (lab, val) in enumerate(SEARCH_ROWS):
        y = S_Y0 + i * S_PITCH
        draw_text(tc, S_X + (S_CAP - text_width(lab)) // 2 + 1, y - 1, lab, WHITE, ACCENT_DARK)
        if val:
            draw_text(tc, S_X + S_CAP + (S_W - S_CAP - text_width(val)) // 2, y - 1, val, INK, PANEL_SHADE)
    for k in range(2):
        if not types[k]:
            sx = socket_x(k)
            draw_text(tc, sx + (SOCKET_W - text_width("ANY", "narrow")) // 2, SOCKET_Y, "ANY", INK_SOFT, None, font="narrow")
    for i, (xx, lab) in enumerate(zip(S_BTN_X, ("SEARCH", "CANCEL"))):
        draw_text(tc, xx + (S_BTN_W - text_width(lab)) // 2, S_BTN_Y + 1, lab, INK, PANEL_SHADE)
    hint = ["Pick the order the list is sorted in.", "List POKéMON by their first letter.",
            "Show POKéMON of up to two types. A: slot", "Switch TOSA / NATIONAL listings."][min(cursor, 3)]
    draw_text(tc, DESC_X, S_TRAY_Y + 2, hint, INK, PANEL_SHADE, line_h=DESC_PITCH)
    a = KX.sheet_rgba(art, pal)
    a.alpha_composite(KX.sheet_rgba(cur, sel))
    a.alpha_composite(KX.sheet_rgba(txt, pal))
    out.alpha_composite(a)
    # OBJ: type icons centred in their sockets, value chevrons on the selected row
    for k in range(2):
        if types[k]:
            out.alpha_composite(KX.type_icon(types[k]), (socket_x(k) + 2, SOCKET_Y))
    if cursor < 4:
        y = S_Y0 + cursor * S_PITCH + 7
        if cursor == 2:     # chevrons flank the socket being edited, 3px clear
            sx = socket_x(slot)
            D.chevron(out, sx - 6, y)
            D.chevron(out, sx + SOCKET_W + 6, y, right=True)
        else:
            D.chevron(out, S_X + S_CAP + 12, y)
            D.chevron(out, S_X + S_W - 12, y, right=True)
    return out


# ------------------------------------------------------------------ parts sheet
def parts_sheet(theme="orchid"):
    pal = D.dex_palette(theme)
    sel = D.selected(pal)
    cw, ch = 304, 150
    out = Image.new("RGBA", (cw, ch), (24, 24, 32, 255))
    out.alpha_composite(KX.grid_frame(0, cw, ch))
    s, cur = sheet(theme), sheet(theme)
    s = new_sheet(cw, ch, theme, spare_a=D.BALL_RED)
    cur = new_sheet(cw, ch, theme, spare_a=D.BALL_RED)
    c, cc = Canvas(s), Canvas(cur)
    D.dais(c, 46, 48, DAIS_R, DAIS_IN)
    rows = [ENTRIES[0], ENTRIES[3], ENTRIES[2]]
    for k, e in enumerate(rows):
        global PILL_X
        draw_row_at(cc if k == 0 else c, 98, 4 + k * 18, e)
    D.label_pill(c, 98, 62, COUNT_W, COUNT_CAP)
    D.label_pill(c, 98, 80, 70, HW_CAP)
    D.tab_pill(c, 98, 100, TAB_W)
    D.tab_pill(cc, 146, 100, TAB_W)
    D.well(c, 196, 98, 25, 22)
    D.track(c, 230, 4, 235, 60)
    D.tray(c, 124, 147, 4, 299)
    draw_text(c, 104 - 2, 61, "SEEN", WHITE, ACCENT_DARK)
    draw_text(c, 98 + COUNT_W - 7 - text_width("87"), 61, "87", INK, PANEL_SHADE)
    draw_text(c, 98 + (HW_CAP - text_width("HT")) // 2 + 1, 79, "HT", WHITE, ACCENT_DARK)
    draw_text(c, 98 + 70 - 7 - text_width("0.5 m", "narrow"), 79, "0.5 m", INK, PANEL_SHADE, font="narrow")
    draw_text(c, 98 + (TAB_W - text_width("AREA")) // 2, 99, "AREA", INK_SOFT, PANEL_SHADE)
    draw_text(cc, 146 + (TAB_W - text_width("INFO")) // 2, 99, "INFO", INK, SELECT_DARK)
    m = D.footprint_mask("treecko")
    for yy in range(16):
        for xx in range(16):
            if m[yy][xx]:
                c.set(200 + xx, 101 + yy, INK)
    draw_text(c, 10, 128, "Tray: seam at y+3, text y+2, 14px pitch", INK, PANEL_SHADE, font="narrow")
    out.alpha_composite(KX.sheet_rgba(s, pal))
    out.alpha_composite(KX.sheet_rgba(cur, sel))
    spr = D.mon_pic("treecko")
    out.alpha_composite(spr, (46 - 32, 48 + int(DAIS_IN * 0.55) + 3 - D.sprite_bottom(spr)))
    out.alpha_composite(D.silhouette(D.mon_pic("kirlia")), (236, 50))
    D.thumb(out, 231, 10, theme)
    D.chevron(out, 258, 22)
    D.chevron(out, 270, 22, right=True)
    big = KX.upscale(out, 4)
    # palette strips: UI pal 0, selected pal 1, grid pal
    sw = 24
    strip = Image.new("RGBA", (big.size[0], 3 * (sw + 6) + 6), (24, 24, 32, 255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(strip)
    from backdrop import GRID_PAL
    for r, p in enumerate((pal, sel, list(GRID_PAL) + [(0, 0, 0)] * 12)):
        for i, col in enumerate(p[:16]):
            x, y = 6 + i * (sw + 4), 6 + r * (sw + 6)
            d.rectangle((x, y, x + sw - 1, y + sw - 1), fill=col + (255,), outline=(255, 255, 255, 255) if i == 0 else None)
    full = Image.new("RGBA", (big.size[0], big.size[1] + strip.size[1]))
    full.paste(big, (0, 0))
    full.paste(strip, (0, big.size[1]))
    return full


def draw_row_at(cv, x, y, e):
    rounded_box(cv, x, y + 1, PILL_W, PILL_H, 4, PANEL, INK, WHITE, PANEL_SHADE)
    draw_text(cv, x + 6, y, "%03d" % e["num"], INK, PANEL_SHADE, font="narrow")
    if e["seen"]:
        draw_text(cv, x + 28, y, info(e)["name"], INK, PANEL_SHADE, font="narrow")
    else:
        draw_text(cv, x + 28, y, "-----", INK_SOFT, PANEL_SHADE, font="narrow")
    if e["caught"]:
        D.caught_ball(cv, x + PILL_W - 15, y + 4)


# ------------------------------------------------------------------ budget
def budget():
    lines = []
    art = sheet("orchid")
    draw_list_art(Canvas(art))
    t, _ = to_tiles(art)
    lines.append(t)
    art = sheet("orchid")
    draw_entry_art(Canvas(art))
    t2, _ = to_tiles(art)
    lines.append(t2)
    row = sheet("orchid")
    rounded_box(Canvas(row), 0, 1, PILL_W, PILL_H, 4, PANEL, INK, WHITE, PANEL_SHADE)
    t3, _ = to_tiles(row.crop((0, 0, 136, 16)))
    return len(t), len(t2), len(t3)


def save(im, path, k=3):
    KX.upscale(im.convert("RGB"), k).save(path)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    idx = lambda n: n - 1
    s1 = render_list(cursor=idx(1))                                   # Treecko, caught
    s2 = render_list(cursor=idx(21), top=16)                          # Lombre, seen
    s3 = render_list(cursor=idx(31), top=27)                          # Kirlia, unseen
    s4 = render_entry(entry_index=idx(1))                             # Treecko INFO
    s5 = render_entry(entry_index=idx(20))                            # Lotad, Water/Grass
    s6 = render_search(cursor=0)
    # TYPE row sockets: zero / one / two types, cursor on the TYPE row (editing slot 1 / 2)
    s6t = [render_search(cursor=2, types=(None, None)), render_search(cursor=2, types=("grass", None)),
           render_search(cursor=2, types=("grass", "water"), slot=1), render_search(cursor=1, types=("grass", None))]
    s7 = render_entry(entry_index=idx(26), tab=1)
    s8 = render_entry(entry_index=idx(21))                            # Lombre, seen only: ????? rule     # Taillow AREA placeholder
    save(s1, os.path.join(out, "main.png"))
    for i, im in enumerate((s1, s2, s3, s4, s5, s6, s7, s8), 1):
        save(im, os.path.join(out, "state_%02d.png" % i))
    for k, im in enumerate(s6t):
        save(im, os.path.join(out, "state_06%s.png" % "abcd"[k]))
    parts_sheet().convert("RGB").save(os.path.join(out, "parts.png"))
    # theme A/B
    D.ensure_device_theme()
    a, b = render_list(cursor=idx(1)), render_list("dex_red", cursor=idx(1))
    c, d = render_entry(entry_index=idx(1)), render_entry("dex_red", entry_index=idx(1))
    ab = Image.new("RGB", (W * 4 + 12, H * 4 + 12), (16, 16, 20))
    for k, im in enumerate((a, b, c, d)):
        ab.paste(KX.upscale(im.convert("RGB"), 2), ((k % 2) * (W * 2 + 12), (k // 2) * (H * 2 + 12)))
    ab.save(os.path.join(out, "theme_ab.png"))
    print("BG1 tiles list/entry, row tiles:", budget())
