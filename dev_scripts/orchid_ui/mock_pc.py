"""
Pixel-accurate mockups of the Orchid PC storage ("Gen 5 layout, Gen 3 pixels").

Layers composited bottom-up like the GBA:
    BG3 grid -> BG2 slot recesses (box area only, WIN0 x 80..239) -> box icon OBJs (priority 2)
    -> BG1 art (dais, info pills, buttons, title tab, party panel) -> BG0 text
    -> OBJ (front pic, type icons, party icons, cursor ring, held icon + shadow, chevrons)
    -> BG0 popups (message, context menu)

usage: mock_pc.py OUT_DIR
"""
import json
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as KX
import dex_ext as D
import windows as Wn
import pc_ext as P
from gamefont import draw_text, text_width

W, H = 240, 160
BOX_SLIDE = 192          # vanilla: next wallpaper drawn 24 tiles along BG2, scrolled 6px x 32 frames


# ------------------------------------------------------------------ popups (BG0, orchid)
def message(text, win=P.MSG_WIN):
    def fn(cv):
        tx, ty, tw, th = win
        Wn.std_frame(cv, tx, ty, tw, th)
        draw_text(cv, tx * 8, ty * 8 + 1, text, INK, PANEL_SHADE)
    return fn


def menu(entries, cursor, right=29, bottom=15, width=None):
    """Vanilla box menu: tilemapLeft = 29 - width, tilemapTop = 15 - height. Gold pill, no icons."""
    def fn(cv):
        tw = width or (max(text_width(e) for e in entries) + 7) // 8 + 1
        th = 2 * len(entries)
        tx, ty = right - tw, bottom - th
        Wn.std_frame(cv, tx, ty, tw, th)
        for i, e in enumerate(entries):
            y = ty * 8 + i * 16
            if i == cursor:
                Wn.selection_bar(cv, tx * 8 + 1, y + 1, tw * 8 - 2, 14)
            draw_text(cv, tx * 8 + 5, y, e, INK, SELECT_DARK if i == cursor else PANEL_SHADE)
    return fn


# ------------------------------------------------------------------ frame renderer
def render(box=0, cursor=("box", 7), held=None, lift=0, party=0.0, popups=(), grid_scroll=0, t=0,
           box_dx=0, next_box=None, chev_flash=None, held_item=None, item_mode=False,
           style="ring", ring_flash=False, display=None, hide_slots=(), extra_obj=None, theme="orchid",
           colours=None, wallpaper=None, contents_override=None, party_override=None, top_obj=None,
           cur_px=None, next_dx=BOX_SLIDE):
    """
    cursor: ('box', i) | ('party', k 0..5, 6 = CANCEL) | ('btn', 0 PARTY / 1 CLOSE) | ('title',) | None
    held: mon dict being carried (floats `lift` px above the cursor slot).  party: 0..1 panel slide.
    box_dx: BG2 scroll for the box switch (negative = moving left); next_box drawn at +BOX_SLIDE.
    chev_flash: 0 left / 1 right chevron lit.  held_item: item icon name carried in MOVE ITEMS.
    """
    name, contents = P.BOXES[box]
    if contents_override is not None:
        contents = contents_override
    contents = {k: v for k, v in contents.items() if k not in hide_slots}
    colours = colours or {}
    pal = palette(theme)
    out = P.grid_frame_tint(grid_scroll) if item_mode else KX.grid_frame(grid_scroll)
    if wallpaper:
        out.alpha_composite(P.wallpaper(wallpaper), (80 + box_dx, 16))

    # ---- BG2 slots + box icons (clipped to the box area: WIN0 x 80..239)
    boxl = KX.blank()
    KX.layer(boxl, lambda cv: P.box_layer(cv, box_dx), theme, pal=P.box_pal_colour(colours.get(box, "orchid")))
    if next_box is not None:
        KX.layer(boxl, lambda cv: P.box_layer(cv, box_dx + next_dx), theme,
                 pal=P.box_pal_colour(colours.get(next_box, "orchid")))
    if cursor and cursor[0] == "box" and style == "ring":      # ring OBJ sits under the icons
        cx, cy = cur_px or P.centre(cursor[1])
        boxl.alpha_composite(P.cursor_ring(ring_flash), (int(cx) - 16, int(cy) - 16))
        if held is not None or held_item:                       # lift shadow: under the slot's icon too
            boxl.alpha_composite(P.shadow(), (int(cx) - 8, int(cy) - 1))
    icons = [(contents, box_dx)]
    if next_box is not None:
        icons.append((P.BOXES[next_box][1], box_dx + next_dx))
    for cont, dx in icons:
        for i, m in cont.items():
            cx, cy = P.centre(i)
            if 72 < cx + dx < W + 8:                         # vanilla hides icons outside x 72..248
                spr = KX.mon_icon(m["folder"], 0, m["pal"])
                if item_mode and not m["item"]:
                    spr = _dim(spr)
                P.safe_comp(boxl, spr, cx + dx - 16, cy - 20)
                if item_mode and m["item"]:
                    P.safe_comp(boxl, KX.sprite_rgba(KX.G("party_menu", "hold_icons.png"), 0, 8), cx + dx + 2, cy + 2)
    clip = Image.new("L", (W, H), 0)
    ImageDraw.Draw(clip).rectangle((80, 0, W - 1, H - 1), 255)
    out.paste(boxl, (0, 0), _and(boxl, clip))

    # ---- display mon (held mon wins, like vanilla)
    hov = None
    if cursor and cursor[0] == "box":
        hov = contents.get(cursor[1])
    elif cursor and cursor[0] == "party" and cursor[1] < 6:
        hov = (party_override or P.PARTY)[cursor[1]]
    disp = display if display is not None else (held or hov)
    if display == "none":
        disp = None

    # ---- BG1 art
    ui = KX.blank()
    tpal = P.text_pal(disp, theme)
    art = new_sheet(W, H, theme)
    ac = Canvas(art)
    P.info_art(ac, disp)
    P.header_tab(ac)
    P.button(ac, P.BTN_PARTY, "party")
    P.button(ac, P.BTN_CLOSE, "close")
    a = KX.sheet_rgba(art, tpal)
    for k, rect in enumerate((P.BTN_PARTY, P.BTN_CLOSE)):
        if cursor == ("btn", k):
            x, y, w, h = rect
            a.alpha_composite(KX.sheet_rgba(art.crop((x, y, x + w, y + h)), P.gold(tpal)), (x, y))
    if cursor == ("title",):
        x, y, w, h = P.TAB
        a.alpha_composite(KX.sheet_rgba(art.crop((x, y, x + w, y + h)), P.gold(tpal)), (x, y))
    ui.alpha_composite(a)

    txt = new_sheet(W, H, theme)
    tc = Canvas(txt)
    P.info_text(tc, disp)
    x, y, w, h = P.TAB
    shown = name if not (next_box is not None and abs(box_dx) >= BOX_SLIDE // 2) else P.BOXES[next_box][0]
    cnt_box = contents if shown == name else P.BOXES[next_box][1]
    title_on_gold = cursor == ("title",)
    draw_text(tc, x + (P.TAB_CAP - text_width(shown)) // 2 + 1, y - 1, shown, WHITE, ACCENT_DARK)
    cs = "%d/30" % len(cnt_box)
    draw_text(tc, x + P.TAB_CAP + (w - P.TAB_CAP - text_width(cs, "small")) // 2 + 1, y + 1, cs, INK,
              SELECT_DARK if title_on_gold else PANEL_SHADE, font="small")
    P.button_text(tc, P.BTN_PARTY, "PARTY POKéMON", INK, SELECT_DARK if cursor == ("btn", 0) else PANEL_SHADE)
    P.button_text(tc, P.BTN_CLOSE, "CLOSE BOX", INK, SELECT_DARK if cursor == ("btn", 1) else PANEL_SHADE)
    ui.alpha_composite(KX.sheet_rgba(txt, tpal))
    out.alpha_composite(ui)

    # ---- OBJ: front pic + types + item cap icon
    if disp:
        spr = KX.mon_front(disp["folder"])
        cx, cy, ro, ri = P.DAIS
        stage = cy + int(ri * 0.55) + 3
        out.alpha_composite(spr, (cx - 32, stage - D.sprite_bottom(spr)))
        icons_t = [KX.type_icon(tp) for tp in disp["types"]]
        tot = 32 * len(icons_t) + 4 * (len(icons_t) - 1)
        for k, ic in enumerate(icons_t):
            out.alpha_composite(ic, (P.LV_PILL[0] + 36 * k, P.TYPES_Y))     # left edge = Lv pill
    if disp:
        P.item_cap_icon(out, disp)

    # ---- party panel (BG1 slides up from the bottom, 1 tile / frame) + party icons (OBJ)
    if party > 0:
        slide = int(round((1 - party) * 18)) * 8
        pl = KX.blank()
        KX.layer(pl, lambda cv: P.party_panel(cv, slide), theme, pal=P.panel_pal(theme))
        PT = party_override or P.PARTY
        for k, m in enumerate(PT):
            sx, sy = P.party_slot_xy(k)
            sel = cursor == ("party", k)
            im = new_sheet(P.PSLOT_W, P.PSLOT_H, theme)
            P.party_slot(Canvas(im), 0, 0, m)
            P.party_slot_text(Canvas(im), 0, 0, m)
            pl.alpha_composite(KX.sheet_rgba(im, P.party_slot_pal(m, theme, sel)), (sx, sy + slide))
        cx, cy, cw, chh = P.PARTY_CANCEL
        im = new_sheet(cw, chh, theme)
        cc = Canvas(im)
        rounded_box(cc, 0, 0, cw, chh, 4, PANEL, INK, WHITE, PANEL_SHADE)
        sel = cursor == ("party", 6)
        draw_text(cc, (cw - text_width("CANCEL")) // 2, -1, "CANCEL", INK, SELECT_DARK if sel else PANEL_SHADE)
        pl.alpha_composite(KX.sheet_rgba(im, P.gold(pal) if sel else pal), (cx, cy + slide))
        for k, m in enumerate(PT):
            if m is None:
                continue
            ix, iy = P.party_icon_centre(k)
            P.safe_comp(pl, KX.mon_icon(m["folder"], 0, m["pal"]), ix - 16, iy + slide - 20)
        out.alpha_composite(pl)

    # ---- cursor
    cpos = None
    if cursor and cursor[0] == "box":
        cpos = tuple(map(int, cur_px)) if cur_px else P.centre(cursor[1])
    elif cursor and cursor[0] == "party" and cursor[1] < 6:
        cpos = P.party_icon_centre(cursor[1])
    if cpos and style == "ring" and cursor[0] == "party":
        out.alpha_composite(P.cursor_ring(ring_flash), (cpos[0] - 16, cpos[1] - 16))
    if held is not None or held_item:
        hx, hy = cpos if cpos else (P.BTN_PARTY[0] + 40, 30)
        if style == "ring" and cursor and cursor[0] == "party":
            out.alpha_composite(P.shadow(), (hx - 8, hy - 1))
        if held is not None:
            spr = KX.mon_icon(held["folder"], 0, held["pal"])
            P.safe_comp(out, spr, hx - 16, hy - 20 - lift)
        else:
            P.safe_comp(out, KX.item_icon(held_item), hx - 12, hy - 12 - lift)   # same lift as a held mon
    if cpos and style == "hand":                     # vanilla: hand 12px above the icon, shadow on the slot
        fr = 2 if held is not None else 0
        out.alpha_composite(P.hand_shadow(), (cpos[0] - 8, cpos[1] - 6))
        P.safe_comp(out, P.hand(fr), cpos[0] - 16, cpos[1] - 34 - (lift if held is not None else 0))
    if extra_obj:
        extra_obj(out)

    # ---- chevrons (OBJ)
    for k, (ax, ay) in enumerate(P.CHEVRONS):
        if chev_flash == k:
            _chev_lit(out, ax, ay, right=k == 1)
        else:
            D.chevron(out, ax, ay, right=k == 1)

    for fn in popups:
        KX.layer(out, fn, theme)
    if top_obj:
        top_obj(out)
    return out


def _and(layer_rgba, clip):
    from PIL import ImageChops
    return ImageChops.multiply(layer_rgba.split()[3], clip)


def _dim(spr):
    """MOVE ITEMS: mons with nothing to hold drawn at half brightness (OBJ blend)."""
    px = spr.copy()
    p = px.load()
    for y in range(px.size[1]):
        for x in range(px.size[0]):
            r, g, b, a = p[x, y]
            if a:
                p[x, y] = snap(((r + 40) // 2, (g + 40) // 2, (b + 56) // 2)) + (a,)
    return px


LIT = ((248, 216, 120), (184, 80, 0))


def _chev_lit(out, cx, cy, right=False):
    px = out.load()
    for r, row in enumerate(SMALL_ARROW):
        row = row[::-1] if right else row
        for c, ch in enumerate(row):
            if ch in "OF":
                px[cx - 3 + c + (2 if right else -2), cy - 4 + r] = (LIT[0] if ch == "F" else LIT[1]) + (255,)


def save3(im, path):
    KX.upscale(im, 3).save(path)


BOX_MENU = ["MOVE", "SUMMARY", "WITHDRAW", "MARK", "RELEASE", "ITEM", "CANCEL"]
TITLE_MENU = ["JUMP", "COLOUR", "NAME", "CANCEL"]
PC_MENU = [("WITHDRAW POKéMON", "Move POKéMON stored in BOXES to\nyour party."),
           ("DEPOSIT POKéMON", "Store POKéMON in your party in BOXES."),
           ("MOVE POKéMON", "Organize the POKéMON in BOXES and\nin your party."),
           ("MOVE ITEMS", "Move items held by any POKéMON\nin a BOX or your party."),
           ("SEE YA!", "Return to the previous menu.")]


# ------------------------------------------------------------------ top PC menu (field)
def render_field_menu(cursor=0):
    """Vanilla CreateMainMenu: std window at tile (1,1), width = longest option; description in the field
    message box. Backdrop = the real Pokémon Center 1F map, player at the PC (camera like the overworld)."""
    out = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    m = P.field_map()
    px, py = 10, 3                                   # player block, facing the PC
    ox, oy = 112 - px * 16, 64 - py * 16
    out.alpha_composite(m, (max(0, ox), oy), (max(0, -ox), 0))
    out.alpha_composite(P.player_sprite("brendan", 1), (112, 48))

    def fn(cv):
        tw = (max(text_width(t) for t, _ in PC_MENU) + 7) // 8 + 1
        Wn.std_frame(cv, 1, 1, tw, 10)
        for i, (t, _) in enumerate(PC_MENU):
            y = 8 + 16 * i
            if i == cursor:
                Wn.selection_bar(cv, 9, y + 1, tw * 8 - 2, 14)
            draw_text(cv, 13, y, t, INK, SELECT_DARK if i == cursor else PANEL_SHADE)
        Wn.dialogue_box(cv, 2, 15, 27, 4)
        draw_text(cv, 16, 120 + 1, PC_MENU[cursor][1], INK, PANEL_SHADE)
    KX.layer(out, fn, "orchid")
    return out


# ------------------------------------------------------------------ popups on the box screen
def jump_popup(box_index):
    """Jump to which BOX? — std frame over the box: name between chevrons, 6x5 occupancy map, count."""
    name, cont = P.BOXES[box_index]

    def fn(cv):
        tx, ty, tw, th = 13, 5, 12, 8
        Wn.std_frame(cv, tx, ty, tw, th)
        x0, y0 = tx * 8, ty * 8
        rounded_box(cv, x0 + 16, y0 + 1, tw * 8 - 32, 14, 4, ACCENT, INK, ACCENT_LIGHT, ACCENT_DARK)
        draw_text(cv, x0 + tw * 4 - text_width(name) // 2, y0, name, WHITE, ACCENT_DARK)
        P.box_minimap(cv, x0 + 6, y0 + 22, cont)
        cx = x0 + 6 + 42 + 6
        rounded_box(cv, cx, y0 + 31, tw * 8 - (cx - x0) - 2, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
        c = "%d/30" % len(cont)
        draw_text(cv, cx + (tw * 8 - (cx - x0) - 2 - text_width(c, "small")) // 2 + 1, y0 + 32, c, INK, PANEL_SHADE, font="small")
    return fn


def jump_chevrons(out):
    for k, (ax, ay) in enumerate(((111, 48), (192, 48))):
        D.chevron(out, ax, ay, right=k == 1)


def colour_popup(sel):
    """COLOUR (replaces WALLPAPER): a row of box-colour swatch discs, gold ring on the pick."""
    names = list(P.BOX_COLOURS)

    def fn(cv):
        Wn.std_frame(cv, 11, 7, 18, 3)
    return fn, names


def colour_swatches(out, sel):
    names = list(P.BOX_COLOURS)
    for k, n in enumerate(names):
        cx, cy = 100 + 24 * k, 68
        im = new_sheet(24, 24)
        P.slot(Canvas(im), 12, 12)
        out.alpha_composite(KX.sheet_rgba(im, P.box_pal_colour(n)), (cx - 12, cy - 12))
        if k == sel:
            out.alpha_composite(P.cursor_ring(), (cx - 16, cy - 16))


# ------------------------------------------------------------------ states
def states():
    B1 = P.BOX1
    S = []
    S.append(("Box view — hovering a Pokémon",
              "Gold ring under Mudkip's icon; the dais shows its front pic, name in the male blue (no glyph), Lv, markings, type and held item.",
              render(cursor=("box", 7))))
    S.append(("Hovering an empty slot",
              "Just the recess under the ring. The dais empties and the pills stay but clear, so nothing jumps around as the cursor moves.",
              render(cursor=("box", 10), grid_scroll=3)))
    S.append(("Pokémon picked up (moving)",
              "Mudkip lifts out of its slot and floats 14px above the cursor slot with a dark shadow in the recess; its old slot is empty. The dais keeps showing the held mon (vanilla rule).",
              render(cursor=("box", 10), held=B1[7], lift=14, hide_slots=(7,), grid_scroll=6)))
    S.append(("Party panel open",
              "The panel slides up over the left four columns (vanilla spot, but stopping under the title tab). 2x3 small slots: icon disc + short pill with Lv and a mini HP bar. Cursor on Ralts (female red name).",
              render(cursor=("party", 2), party=1.0, grid_scroll=9)))
    S.append(("Context menu",
              "Std Orchid frame anchored like vanilla (right edge tile 29, bottom tile 15); gold pill, no icons. Message in the std frame below.",
              render(cursor=("box", 7), popups=[message("Mudkip is selected."), menu(BOX_MENU, 1)])))
    S.append(("Box switch (R) — mid-slide",
              "Right chevron lit; BOX 1's slots and icons scroll left on BG2 (6px/frame, vanilla) while BOX 2 slides in behind them; the tab already reads BOX 2.",
              render(cursor=None, display=P.BOX1[7], next_box=1, box_dx=-102, chev_flash=1, grid_scroll=12)))
    S.append(("Top PC menu (field)",
              "Vanilla window at tile (1,1) sized to the longest option, gold pill, no icons; the option's description in the Orchid dialogue box. Over the real Pokémon Center map.",
              render_field_menu(cursor=2)))
    # MOVE ITEMS: Seedot's Oran Berry is being carried; mons with nothing to hold are dimmed
    B1i = dict(B1)
    B1i[4] = dict(B1[4], item=None)
    S.append(("MOVE ITEMS — carrying an item",
              "The Oran Berry (real 24x24 icon) floats 14px above Mudkip's slot with the same shadow as a held mon; A swaps it with Mystic Water (shown in the item pill). Grid lines turn amber (BG3 palette swap, like vanilla); mons without items are dimmed, the rest wear hold tags.",
              render(cursor=("box", 7), held_item="oran_berry", lift=14, item_mode=True, contents_override=B1i,
                     popups=[message("Oran Berry is selected.")], grid_scroll=4)))
    S.append(("Jump to which BOX?",
              "Std frame over the box: name between red chevrons, a 6x5 occupancy map (picture instead of vanilla's 'N POKéMON' line) and the count.",
              render(box=1, cursor=("title",), popups=[message("Jump to which BOX?"), jump_popup(0)],
                     top_obj=jump_chevrons, grid_scroll=8)))
    fn, names = colour_popup(3)
    S.append(("Box colour (replaces wallpapers)",
              "Title-tab menu COLOUR: six swatches sit exactly on the slot columns (each is the slot recess in that colour), gold ring on Leaf; the box previews it live. One BG palette per box colour.",
              render(box=1, cursor=("title",), colours={1: "leaf"}, popups=[message("Pick the box colour."), fn],
                     top_obj=lambda o: colour_swatches(o, 3), grid_scroll=2)))
    return S


# ------------------------------------------------------------------ parts sheet (4x)
def _cellbg(w, h):
    return KX.grid_frame(0, w, h)


def parts_sheet(path):
    k = 4
    items = []
    # slot states
    def slot_img(state):
        im = _cellbg(32, 44)
        sh = new_sheet(32, 44)
        P.slot(Canvas(sh), 16, 28)
        im.alpha_composite(KX.sheet_rgba(sh, P.box_pal()))
        m = P.BOX1[7]
        if state in ("hover", "holding"):
            im.alpha_composite(P.cursor_ring(), (0, 12))
        if state in ("occupied", "hover"):
            im.alpha_composite(KX.mon_icon(m["folder"], 0, m["pal"]), (0, 8))
        if state == "holding":
            im.alpha_composite(P.shadow(), (8, 27))
            P.safe_comp(im, KX.mon_icon(m["folder"], 0, m["pal"]), 0, -6)
        return im
    row1 = [("slot: empty", slot_img("empty")), ("occupied", slot_img("occupied")),
            ("hover (ring OBJ)", slot_img("hover")), ("holding (lift+shadow)", slot_img("holding")),
            ("ring 32x32 OBJ", _on(_cellbg(32, 32), P.cursor_ring())), ("A-press flash", _on(_cellbg(32, 32), P.cursor_ring(True)))]
    # header tab normal / gold
    def tab_img(gold_):
        x, y, w, h = P.TAB
        im = _cellbg(w + 24, h + 4)
        sh = new_sheet(w + 24, h + 4)
        P.header_tab(Canvas(sh), 12, 2, w, h)
        pal = P.text_pal()
        im.alpha_composite(KX.sheet_rgba(sh, P.gold(pal) if gold_ else pal))
        t = new_sheet(w + 24, h + 4)
        tc = Canvas(t)
        draw_text(tc, 12 + (P.TAB_CAP - text_width("BOX 1")) // 2 + 1, 1, "BOX 1", WHITE, ACCENT_DARK)
        draw_text(tc, 12 + P.TAB_CAP + 6, 3, "18/30", INK, SELECT_DARK if gold_ else PANEL_SHADE, font="small")
        im.alpha_composite(KX.sheet_rgba(t, pal))
        D.chevron(im, 4, 9)
        D.chevron(im, w + 19, 9, right=True)
        return im
    def btn_img(rect, icon, label, gold_):
        x, y, w, h = rect
        im = _cellbg(w + 4, h + 4)
        sh = new_sheet(w + 4, h + 4)
        P.button(Canvas(sh), (2, 2, w, h), icon)
        P.button_text(Canvas(sh), (2, 2, w, h), label, INK, SELECT_DARK if gold_ else PANEL_SHADE)
        pal = P.text_pal()
        im.alpha_composite(KX.sheet_rgba(sh, P.gold(pal) if gold_ else pal))
        return im
    row2 = [("title tab", tab_img(False)), ("title tab: cursor", tab_img(True))]
    row3 = [("PARTY button", btn_img(P.BTN_PARTY, "party", "PARTY POKéMON", False)),
            ("CLOSE BOX", btn_img(P.BTN_CLOSE, "close", "CLOSE BOX", False)),
            ("CLOSE BOX: cursor", btn_img(P.BTN_CLOSE, "close", "CLOSE BOX", True))]
    def pslot(m, sel):
        im = _cellbg(P.PSLOT_W + 4, P.PSLOT_H + 4)
        sh = new_sheet(P.PSLOT_W + 4, P.PSLOT_H + 4)
        P.party_slot(Canvas(sh), 2, 2, m)
        P.party_slot_text(Canvas(sh), 2, 2, m)
        im.alpha_composite(KX.sheet_rgba(sh, P.party_slot_pal(m, "orchid", sel)))
        if m:
            im.alpha_composite(KX.mon_icon(m["folder"], 0, m["pal"]), (-2, -5))
        if sel:
            im.alpha_composite(P.cursor_ring(), (-2, -1))
        return im
    row4 = [("party slot", pslot(P.PARTY[0], False)), ("party slot: cursor", pslot(P.PARTY[2], True)),
            ("party slot: low HP", pslot(P.PARTY[3], False)), ("party slot: empty", pslot(None, False))]
    def marks_img():
        im = _cellbg(44, 18)
        sh = new_sheet(44, 18)
        D.well(Canvas(sh), 2, 1, 40, 15, 3)
        P.markings(Canvas(sh), 5, 5, {0, 2})
        im.alpha_composite(KX.sheet_rgba(sh))
        return im
    def sw():
        im = _cellbg(24 * 6 + 4, 28)
        for j, n in enumerate(P.BOX_COLOURS):
            sh = new_sheet(24, 24)
            P.slot(Canvas(sh), 12, 12)
            im.alpha_composite(KX.sheet_rgba(sh, P.box_pal_colour(n)), (2 + 24 * j, 2))
        return im
    row5 = [("markings well (ROM shapes)", marks_img()), ("box colours", sw()),
            ("shadow 16x8 OBJ", _on(_cellbg(20, 12), P.shadow(), (2, 2)))]
    rows = [row1, row2, row3, row4, row5]
    pad = 10
    Wd = max(sum(im.size[0] + pad for _, im in r) for r in rows) + pad
    Ht = sum(max(im.size[1] for _, im in r) + 16 for r in rows) + 24
    sheet = Image.new("RGBA", (Wd * k, Ht * k), (28, 28, 36, 255))
    d = ImageDraw.Draw(sheet)
    d.text((pad * k, 8), "PC storage parts (4x). Slot recess = BG2 tiles (one 3x3-tile cell, identical for all 30); ring, shadow, icons = OBJ.", fill=(230, 230, 240))
    y = 24
    for r in rows:
        x = pad
        for lab, im in r:
            d.text((x * k, (y - 2) * k - 26), lab, fill=(230, 230, 240))
            sheet.paste(KX.upscale(im, k), (x * k, (y + 4) * k))
            x += im.size[0] + pad
        y += max(im.size[1] for _, im in r) + 16
    sheet.save(path)


def _on(bg, spr, at=(0, 0)):
    bg.alpha_composite(spr, at)
    return bg


# ------------------------------------------------------------------ variants
def variants(path):
    B1 = P.BOX1
    cells = [
        ("A (recommended): gold ring, hover", render(cursor=("box", 7))),
        ("A: holding - mon lifts 14px, shadow in the recess", render(cursor=("box", 10), held=B1[7], lift=14, hide_slots=(7,))),
        ("B: vanilla hand cursor, hover", render(cursor=("box", 7), style="hand")),
        ("B: hand holding (fist)", render(cursor=("box", 10), held=B1[7], lift=6, hide_slots=(7,), style="hand")),
        ("Wallpaper C (recommended): grid + box colours", render(cursor=("box", 7), colours={0: "teal"})),
        ("Wallpaper D: vanilla Forest wallpaper kept under the slots", render(cursor=("box", 7), wallpaper="forest")),
    ]
    k = 3
    sheet = Image.new("RGB", (2 * 240 * k + 3 * 24, 3 * (160 * k + 40) + 16), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(cells):
        x, y = 24 + (i % 2) * (240 * k + 24), 16 + (i // 2) * (160 * k + 40)
        d.text((x, y), lab, fill=(230, 230, 240))
        sheet.paste(KX.upscale(im, k).convert("RGB"), (x, y + 22))
    sheet.save(path)


# ------------------------------------------------------------------ budget
def budget():
    lines = []
    box = new_sheet(160, 144)
    for i in range(30):
        cx, cy = P.centre(i)
        P.slot(Canvas(box), cx - 80, cy - 16)
    t_box, _ = to_tiles(box)
    art = new_sheet(W, H)
    ac = Canvas(art)
    P.info_art(ac)
    P.header_tab(ac)
    P.button(ac, P.BTN_PARTY, "party")
    P.button(ac, P.BTN_CLOSE, "close")
    t_art, _ = to_tiles(art)
    pan = new_sheet(W, H)
    pc = Canvas(pan)
    P.party_panel(pc)
    for kk, m in enumerate(P.PARTY):
        x, y = P.party_slot_xy(kk)
        P.party_slot(pc, x, y, m)
    cx, cy, cw, chh = P.PARTY_CANCEL
    rounded_box(pc, cx, cy, cw, chh, 4, PANEL, INK, WHITE, PANEL_SHADE)
    t_pan, _ = to_tiles(pan)
    lines.append("BG2 box slots: %d unique tiles incl. blank (all 30 recesses share one 3x3-tile cell; vanilla wallpapers use up to ~150 each)" % len(t_box))
    lines.append("BG1 static art (dais, info pills, title tab, 2 buttons): %d unique tiles; party panel + 6 slot shapes + CANCEL: %d tiles -> %d total (< 256, fits charblock 1 like vanilla's display/party menu)" % (len(t_art), len(t_pan), len(t_art) + len(t_pan) - 1))
    lines.append("BG3 grid: 4 tiles, 1 palette (replaces scrolling_bg; MOVE ITEMS = palette swap to amber, like vanilla's scrolling_bg_move_items.pal)")
    lines.append("BG palettes: 0 UI (orchid roles, SPARE = hovered name colour), 1 gold copy (button/tab/party-slot cursor), 2-4 party-slot HP variants (green/yellow/red in SPARE) + 1 gold copy for the party slot under the cursor, 6 box slots (SPARE_A = pit), 7 next-box colour during slides, 8 grid, 13-15 std frame/text (vanilla). 11 of 16.")
    lines.append("OBJ: 30 box icons (32x32, vanilla) + up to 6 party + 1 held icon = 37 icons; display pic 64x64; 2 type icons 32x16; cursor ring 32x32 + shadow 16x8; title text 2x 32x16 (vanilla) or BG0; 2 chevrons 8x16. ~46 OAM entries of 128.")
    lines.append("OBJ palettes: icon palettes 0-5 (6, shared, vanilla), display pic 1, type icons 1-2, UI (ring/shadow/chevron/hold tag) 1 -> 10-11 of 16. Ring = SELECT ramp of the UI OBJ palette.")
    lines.append("Clipping: WIN0 x 80..239 keeps BG2 (sliding boxes) out of the info panel; box icons hide outside x 72..248 like vanilla.")
    return lines


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    S = states()
    for n, (title, desc, im) in enumerate(S, 1):
        save3(im, os.path.join(out, "state_%02d.png" % n))
    save3(S[0][2], os.path.join(out, "main.png"))
    parts_sheet(os.path.join(out, "parts.png"))
    variants(os.path.join(out, "variants.png"))
    B = budget()
    for l in B:
        print(l)
    notes = {
        "title": "PC storage (Pokémon Storage System) — shared screen, Orchid purple",
        "main": {"file": "main.png", "zones": [
            ["Top buttons", "PARTY POKéMON and CLOSE BOX as label pills with picture caps (ball / closing box), in vanilla's top-row spot; cursor = gold palette swap."],
            ["Title tab", "Box name on an accent cap + a count inset (18/30), small red Gen 3 chevrons either side; L/R or the chevrons switch boxes."],
            ["Box", "6x5 round recesses on the scrolling grid (BG2, one shared 3x3-tile cell). Occupied slots just hold the real ROM icon."],
            ["Cursor", "Gold ring OBJ hugging the slot lip, under the icon. No hand, no arrow. Picking up lifts the mon above the ring with a shadow."],
            ["Info dais", "Hovered (or held) mon's front pic on the dex dais, name in gender colour (no glyph), Lv cap, ROM markings, type icons left-aligned to the Lv pill, held item as its real icon in a round recess overhanging the item pill (empty recess + 'None' when nothing is held)."],
        ]},
        "states": [{"file": "state_%02d.png" % n, "title": t, "desc": d} for n, (t, d, _) in enumerate(S, 1)],
        "gifs": [
            {"file": "box_switch.gif", "title": "Box switch (press R)", "desc": "Right chevron lights for 8 frames and nudges out; slots + icons scroll left 6px/frame for 32 frames (vanilla speed) while BOX 2 slides in; the tab swaps to BOX 2 at the halfway point; the ring hides during the slide and returns on the same slot. Then L back."},
            {"file": "pickup.gif", "title": "Pick up and drop a Pokémon", "desc": "A: ring flashes, Mudkip rises 14px over 8 frames (ease-out) with a shadow fading in; cursor moves 6 frames per slot (vanilla) with the mon floating and bobbing 1px; A drops it (8 frames down), ring flashes."},
        ],
        "extras": [
            {"file": "parts.png", "title": "Parts at 4x", "desc": "Slot states (empty / occupied / hover / holding), ring + flash, title tab normal and on cursor, both buttons, small party slots (normal / cursor / low HP / empty), markings well, box colours, shadow."},
            {"file": "variants.png", "title": "Cursor and wallpaper options", "desc": "A gold ring vs B vanilla hand; C grid + box colours vs D vanilla wallpaper under the slots."},
        ],
        "budget": B,
        "kit_additions": [
            "pc_ext.slot(): round recess (raised accent lip + dark pit with top-left cast shadow); SPARE_A = pit colour. Reusable for any 'socket' (daycare, PC party, trade).",
            "pc_ext.cursor_ring(): 32x32 gold ring OBJ (SELECT ramp, raised bevel) — the round twin of windows.selection_bar for grid/slot cursors.",
            "pc_ext.shadow(): 16x8 lift shadow OBJ for anything picked up (mons, items).",
            "pc_ext.party_slot(): small party slot (icon dais + short pill with Lv + mini HP bar), party_ext language at 46x26.",
            "pc_ext.item_socket() + fit_font(): round item recess that overhangs a pill (real 24x24 item icon OBJ on top); text falls back normal -> narrow -> narrower like GetFontIdToFit.",
            "pc_ext.markings(): the ROM's four marking shapes (interface/mon_markings.png) in kit roles, inside dex_ext.well().",
            "Box colour palettes (BOX_COLOURS: orchid / blue / red / leaf / teal / amber) registered at runtime as box_* themes.",
        ],
        "questions": [
            ["Cursor: ring or hand?", "Vanilla grabs mons with a hand (it's not an arrow, so it's allowed). Options: A gold ring under the icon + the mon floats when held; B keep the vanilla hand over the gold ring-less slot. **Recommendation: A** — same gold language as every other screen, reads at a glance on the dark grid, and the floating mon + shadow says 'picked up' without the hand covering the row above."],
            ["Wallpapers", "Vanilla has 16 painted wallpapers. Options: keep them under the slots (D: clashes with the grid and the purple slots, ~150 tiles + 2 palettes each); drop them; replace with box colours (C). **Recommendation: replace WALLPAPER with COLOUR** — 6 palette swaps of the slot lip, 0 extra tiles, keeps boxes tellable apart."],
            ["Party panel shape", "Vanilla: lead + 5 in a column. Options: keep that; BW-style 2x3 equal slots. **Recommendation: 2x3** (state 04) — matches the box's round slots, fits 13 tiles, and the panel can stop under the title tab so BOX name stays visible."],
            ["Hover info", "Vanilla shows nickname, /SPECIES, Lv + gender glyph and item. **Recommendation:** name (gender colour), Lv, markings, type icons, item — species line dropped (the front pic shows it); nicknames still fit with the narrow-font fallback."],
            ["Jump-to-box popup", "Vanilla shows name + 'N POKéMON'. **Recommendation:** name + a 6x5 occupancy mini-map + count (state 09): a picture of the box, cheap BG0 art."],
        ],
    }
    json.dump(notes, open(os.path.join(out, "notes.json"), "w"), indent=1, ensure_ascii=False)
    print("ok", len(S))
