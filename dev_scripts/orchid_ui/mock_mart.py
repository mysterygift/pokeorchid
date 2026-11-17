"""
Poké Mart buy screen — Orchid UI mockups, three directions (A counter & awning, B shelves,
C register / receipt) on the same data, + every state of the recommended direction (A).

Layers (GBA): BG3 grid (pal 3) -> BG2 shop art (pal 0 Orchid kit / pal 1 selected-row swap /
pal 2 SHOP: wood, Mart blue, brass) -> BG1 popups (quantity tag, register display) -> BG0 text
windows + std frames -> OBJ (item icons, clerk, chevrons, scroll thumb).

usage: mock_mart.py OUT_DIR
"""
import json
import os
import sys
from PIL import Image, ImageDraw
from kit import *
import kit_ext as K
import windows as Wn
import mart_ext as M
from mart_ext import s, S, WOOD_DARK, WOOD, WOOD_LIGHT, MART_DARK, MART, MART_LIGHT, \
    BRASS_DARK, BRASS, BRASS_LIGHT
from gamefont import draw_text, text_width

W, H = 240, 160
ITEMS = [("Poké Ball", 200, "poke_ball"), ("Potion", 300, "potion"), ("Antidote", 100, "antidote"),
         ("Paralyze Heal", 200, "paralyze_heal"), ("Escape Rope", 550, "escape_rope"),
         ("Repel", 350, "repel"), ("Super Potion", 700, "super_potion"), ("Great Ball", 600, "great_ball"),
         ("Awakening", 250, "awakening")]
TMS = [("TM28 Dig", 2000, "tm_ground"), ("TM06 Toxic", 3000, "tm_poison"), ("TM03 Water Pulse", 3000, "tm_water"),
       ("TM35 Flamethrower", 3000, "tm_fire"), ("TM24 Thunderbolt", 3000, "tm_electric"),
       ("TM13 Ice Beam", 3000, "tm_ice")]
DESC = {  # src/data/items.h
    "poke_ball": "A tool used for\ncatching wild\nPokémon.",
    "potion": "Restores the HP of\na Pokémon by\n20 points.",
    "antidote": "Heals a poisoned\nPokémon.",
    "paralyze_heal": "Heals a paralyzed\nPokémon.",
    "escape_rope": "Use to escape\ninstantly from a\ncave or a dungeon.",
    "repel": "Repels weak wild\nPokémon for 100\nsteps.",
    "super_potion": "Restores the HP of\na Pokémon by\n60 points.",
    "great_ball": "A good Ball with a\nhigher catch rate\nthan a Poké Ball.",
    "awakening": "Awakens a sleeping\nPokémon.",
    "tm_ground": "Digs underground\nthe 1st turn, then\nstrikes next turn.",
    None: "Quit shopping.",
}
CANCEL = ("CANCEL", None, None)
IN_BAG = {"poke_ball": 3, "potion": 5, "escape_rope": 1}


def money_str(v):
    return "¥%d" % v           # the ROM's ¥ glyph (0xB7) is drawn as the Pokédollar sign


def st_defaults(**kw):
    st = dict(items=ITEMS, cursor=0, scroll=0, money=3000, mode="list", qty=1, msg=None, yesno=0,
              accent="mart", grid=0, bonus=False, theme="orchid")
    st.update(kw)
    return st


def visible(st, rows):
    full = st["items"] + [CANCEL]
    return full[st["scroll"]:st["scroll"] + rows], len(full)


def selected(st):
    return (st["items"] + [CANCEL])[st["cursor"]]


def sheet():
    return M.art_sheet()


def put(out, spr, x, y):
    out.alpha_composite(spr, (int(x), int(y)))


# ---------------------------------------------------------------- shared popups (BG0 windows)
def msg_box(cv, text):
    Wn.dialogue_box(cv, 2, 15, 27, 4)
    draw_text(cv, 16, 120, text, INK, PANEL_SHADE)


def yesno(cv, cursor):
    Wn.std_frame(cv, 24, 9, 5, 4)
    for i, t in enumerate(("YES", "NO")):
        y = 72 + 16 * i
        if i == cursor:
            Wn.selection_bar(cv, 194, y + 1, 36, 14)
        draw_text(cv, 200, y, t, INK, PANEL_SHADE)


def qty_text(st):
    it = selected(st)
    total = it[1] * st["qty"]
    return "×%03d" % st["qty"], money_str(total), money_str(st["money"] - total)


def chevrons_v(out, cx, y_up, y_down):
    put(out, M.chevron("up"), cx - 4, y_up)
    put(out, M.chevron("down"), cx - 4, y_down)


def message_for(st):
    it = selected(st)
    if st["mode"] == "qty":
        return "%s? Certainly.\nHow many would you like?" % it[0]
    if st["mode"] == "confirm":
        return "%s? And you wanted %d?\nThat will be %s." % (it[0], st["qty"], money_str(it[1] * st["qty"]))
    return st["msg"]


# ================================================================== A: counter & awning
A_LIST_X, A_LIST_Y, A_ROWS, A_PILL_W = 104, 16, 6, 128
A_TAG_W = 42
A_TRACK = (233, 17, 238, 110)
A_ICON_C = (68, 77)          # item on the counter
A_CLERK = (20, 60)           # OBJ top-left
A_DESC = (10, 116)


def a_art(cv, st, rows_shown):
    M.awning(cv, 0, 239)
    # hanging money sign
    for x in (16, 78):
        M.rod(cv, x, 16, 19)
    M.wood_board(cv, 4, 20, 88, 20, r=3, grain=False)
    for x, y in ((7, 23), (85, 23), (7, 35), (85, 35)):
        M.rivet(cv, x, y)
    M.coin(cv, 17, 30, 6.5)
    rounded_box(cv, 28, 23, 54, 14, 3, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
    # back-wall shelf behind the clerk (goods on pal 4, plank + brackets on pal 2)
    M.wall_shelf(cv, 2, 93, 56)
    # counter (clerk side): top slab with a brass front lip
    cv.rect(0, 87, 95, 87, s(INK))
    cv.rect(0, 88, 95, 89, s(WOOD_LIGHT))
    cv.rect(0, 90, 95, 91, s(WOOD))
    cv.hline(0, 95, 92, s(BRASS_LIGHT))
    cv.hline(0, 95, 93, s(BRASS_DARK))
    cv.hline(0, 95, 94, s(INK))
    cv.vline(95, 87, 111, s(INK))
    cv.rect(0, 95, 94, 111, s(WOOD))
    cv.hline(0, 94, 95, s(WOOD_DARK))
    # Mart-blue band across the counter front, brass edged
    cv.hline(0, 94, 99, s(INK))
    cv.hline(0, 94, 100, s(BRASS))
    cv.hline(0, 94, 101, s(MART_LIGHT))
    cv.rect(0, 102, 94, 104, s(MART))
    cv.hline(0, 94, 105, s(MART_DARK))
    cv.hline(0, 94, 106, s(BRASS_DARK))
    cv.hline(0, 94, 107, s(INK))
    # list pills with price tags (pal 0 -> pal 1 swap on the selected row)
    for r in range(rows_shown):
        y = A_LIST_Y + r * 16 + 1
        rounded_box(cv, A_LIST_X, y, A_PILL_W, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    M.track(cv, *A_TRACK)
    # description tray = the counter front, with a cream card pinned on it
    cv.hline(0, 239, 112, s(INK))
    cv.rect(0, 113, 239, 159, s(WOOD))
    cv.hline(0, 239, 113, s(WOOD_LIGHT))
    cv.hline(0, 239, 114, s(WOOD_DARK))
    rounded_box(cv, 4, 115, 232, 48, 2, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
    for x, y in ((1, 120), (237, 120), (1, 150), (237, 150)):
        M.rivet(cv, x, y)


def a_tag_w(st):
    return max(44, max(text_width(money_str(i[1]), "narrow") for i in st["items"]) + 18)


def a_tags(cv, st, rows):
    """Price tags inside each pill's right end (pal 0 spares, so they stay manila when the row is gold)."""
    for r, it in enumerate(rows):
        if it[1] is None:
            continue
        y = A_LIST_Y + r * 16 + 1
        w = a_tag_w(st)
        M.price_tag(cv, A_LIST_X + A_PILL_W - w - 2, y + 1, w, 12)


def a_text(cv, st, rows, selected_row):
    draw_text(cv, 80 - text_width(money_str(st["money"])), 21, money_str(st["money"]), INK, PANEL_SHADE)
    for r, it in enumerate(rows):
        y = A_LIST_Y + r * 16
        tm = it[2] and it[2].startswith("tm_")
        name = it[0].split(" ", 1)[1] if tm else it[0]
        draw_text(cv, A_LIST_X + (21 if tm else 7), y, name, INK, PANEL_SHADE, font="narrow")
        if it[1] is not None:
            p = money_str(it[1])
            draw_text(cv, A_LIST_X + A_PILL_W - 2 - 6 - text_width(p, "narrow"), y, p, INK, SPARE_B, font="narrow")
    draw_text(cv, A_DESC[0], A_DESC[1], DESC.get(selected(st)[2], ""), INK, PANEL_SHADE, line_h=14)


def a_qty(out, cv, st):
    """Quantity picker = a big hanging price tag over the list (BG1)."""
    x, y, w, h = 116, 64, 116, 44
    m = M.chamfer_mask(w, h, tl=10, bl=10)
    M.mask_box(cv, x, y, m, SPARE_A, INK, WHITE, SPARE_B)
    # punched hole + string up to the awning
    hx, hy = x + 6, y + h // 2 - 2
    disc(cv, hx + 1.5, hy + 1.5, 2.5, SPARE_B, INK)
    cv.set(hx + 1, hy + 1, 0)
    cv.set(hx + 2, hy + 1, 0)
    cv.set(hx + 1, hy + 2, 0)
    cv.set(hx + 2, hy + 2, 0)
    # inner cream plates: quantity well + totals
    rounded_box(cv, x + 18, y + 4, 36, h - 8, 3, PANEL, INK, PANEL_SHADE, WHITE)    # recessed
    cv.vline(x + 60, y + 6, y + h - 7, SPARE_B)
    cv.vline(x + 61, y + 6, y + h - 7, WHITE)
    q, tot, left = qty_text(st)
    return dict(q=(x + 36, y + 14, q), tot=(x + w - 7, y + 4, tot), left=(x + w - 7, y + 22, left),
                coin=(x + 66, y + 25), chev=(x + 36, y + 7, y + h - 12))


def render_A(st):
    st = st_defaults(**st) if "items" not in st else st
    rows, total = visible(st, A_ROWS)
    sel_row = st["cursor"] - st["scroll"]
    art = sheet()
    cv = Canvas(art)
    a_art(cv, st, len(rows))
    a_tags(cv, st, rows)
    cellpal = {(tx, ty): 1 for ty in (2 + 2 * sel_row, 3 + 2 * sel_row) for tx in range(13, 29)} \
        if st["mode"] != "none" else {}
    # OBJ under BG2 (priority): clerk behind the counter
    clerk = M.clerk(0)
    tmp = K.grid_frame(st["grid"])
    tmp.alpha_composite(clerk, A_CLERK)
    out = M.compose(art, cellpal, st["grid"], st["accent"], base=tmp)
    # text (BG0)
    txt = sheet()
    a_text(Canvas(txt), st, rows, sel_row)
    M.overlay(out, txt, st["accent"])
    # OBJ: item on the counter, bonus Premier Ball, scrollbar thumb
    it = selected(st)
    ic = M.icon(it[2]) if it[2] else None
    if ic:
        K.place(out, ic, *A_ICON_C)
    tm_discs(out, rows)
    if st["bonus"]:
        K.place(out, M.icon("premier_ball"), A_ICON_C[0] + 16, A_ICON_C[1] + 2)
    if total > A_ROWS:
        put(out, M.thumb(), A_TRACK[0] + 1, M.thumb_y(A_TRACK[1], A_TRACK[3], st["scroll"], total, A_ROWS))
    popups(out, st, a_qty)
    return out


def popups(out, st, qty_fn):
    win = sheet()
    cv = Canvas(win)
    q = None
    if st["mode"] == "qty" and st.get("picker", True):
        q = qty_fn(out, cv, st)
    m = message_for(st)
    typing = False
    if m:
        n = st.get("chars")
        typing = n is not None and n < len(m)
        msg_box(cv, m[:n] if n is not None else m)
    if st["mode"] == "confirm" and not typing:
        yesno(cv, st["yesno"])
    if q and q.get("frame"):
        pass
    M.overlay(out, win, st["accent"])
    if q:
        t = sheet()
        tc = Canvas(t)
        qx, qy, qs = q["q"]
        draw_text(tc, qx - text_width(qs) // 2, qy, qs, INK, PANEL_SHADE)
        for key in ("tot", "left"):
            xr, yy, sv = q[key]
            draw_text(tc, xr - text_width(sv), yy, sv, INK, q.get("sh", SPARE_B) if key == "tot" else PANEL_SHADE)
        M.overlay(out, t, st["accent"])
        cx, yu, yd = q["chev"]
        chevrons_v(out, cx, yu, yd)
        if q.get("coin"):
            c = M.art_sheet(16, 16)
            M.coin(Canvas(c), 6, 6)
            out.alpha_composite(K.sheet_rgba(c, M.p0() + M.p1() + M.shop_pal(st["accent"])) if False else _rgba(c, st), q["coin"])


def _rgba(p_im, st):
    o = Image.new("RGBA", p_im.size, (0, 0, 0, 0))
    M.overlay(o, p_im, st["accent"])
    return o


# ================================================================== B: shelves
B_POSTS = (0, 40, 80, 120)
B_BACKS = (8, 48, 88)
B_SHELF_Y = (24, 64)           # back wall tops (32 tall)
B_LIST_X, B_LIST_W, B_LIST_Y, B_ROWS = 130, 100, 16, 6
B_TRACK = (233, 17, 238, 110)


def b_art(cv, st, rows_shown):
    # cornice: Mart-blue sign band with brass trim, full width
    cv.rect(0, 0, 239, 13, s(MART))
    cv.hline(0, 239, 0, s(MART_LIGHT))
    cv.hline(0, 239, 12, s(MART_DARK))
    cv.hline(0, 239, 13, s(BRASS))
    cv.hline(0, 239, 14, s(BRASS_DARK))
    cv.hline(0, 239, 15, s(INK))
    rounded_box(cv, 160, 1, 76, 12, 3, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
    M.coin(cv, 154, 7, 5)
    # cabinet: posts, beam, planks, base (pal 2); back walls (pal 0, gold when selected)
    cv.rect(0, 16, 127, 23, s(WOOD))
    cv.hline(0, 127, 16, s(WOOD_LIGHT))
    cv.hline(0, 127, 22, s(WOOD_DARK))
    cv.hline(0, 127, 23, s(INK))
    for py in (56, 96):
        cv.hline(0, 127, py, s(INK))
        cv.rect(0, py + 1, 127, py + 2, s(WOOD_LIGHT))
        cv.rect(0, py + 3, 127, py + 6, s(WOOD))
        cv.hline(0, 127, py + 6, s(WOOD_DARK))
        cv.hline(0, 127, py + 7, s(INK))
    cv.rect(0, 104, 127, 111, s(WOOD_DARK))
    cv.hline(0, 127, 104, s(WOOD))
    for px in B_POSTS:
        for (y0, y1) in ((24, 55), (64, 95)):
            cv.rect(px, y0, px + 7, y1, s(WOOD))
            cv.vline(px, y0, y1, s(INK) if px == 0 else s(INK))
            cv.vline(px + 1, y0, y1, s(WOOD_LIGHT))
            cv.vline(px + 6, y0, y1, s(WOOD_DARK))
            cv.vline(px + 7, y0, y1, s(INK))
            M.rivet(cv, px + 3, y0 + 3)
            M.rivet(cv, px + 3, y1 - 4)
    cv.vline(0, 16, 111, s(INK))
    cv.vline(127, 16, 111, s(INK))
    for k in range(min(6, rows_shown)):
        bx, by = B_BACKS[k % 3], B_SHELF_Y[k // 3]
        cv.rect(bx, by, bx + 31, by + 31, PANEL)
        cv.rect(bx, by, bx + 31, by + 2, PANEL_SHADE)      # shadow under the shelf above
        cv.vline(bx, by, by + 31, PANEL_SHADE)             # shadow beside the left post
        cv.vline(bx + 1, by + 3, by + 31, WHITE)
    # price list: compact pills
    for r in range(rows_shown):
        y = B_LIST_Y + r * 16 + 1
        rounded_box(cv, B_LIST_X, y, B_LIST_W, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    M.track(cv, *B_TRACK)
    # tray (bag style)
    y = 112
    cv.rect(0, y, 239, 159, PANEL)
    cv.hline(0, 239, y, INK)
    cv.hline(0, 239, y + 1, WHITE)
    cv.hline(0, 239, 159, PANEL_SHADE)
    for x in range(2, 238):
        if x % 4 < 2:
            cv.set(x, y + 3, PANEL_SHADE)


def b_qty(out, cv, st):
    Wn.std_frame(cv, 17, 9, 11, 4)
    q, tot, left = qty_text(st)
    x0, y0 = 136, 72
    rounded_box(cv, x0, y0 + 1, 34, 30, 3, PANEL, INK, PANEL_SHADE, WHITE)
    cv.vline(x0 + 38, y0 + 2, y0 + 29, PANEL_SHADE)
    return dict(q=(x0 + 17, y0 + 8, q), tot=(224, y0, tot), left=(224, y0 + 16, left), sh=PANEL_SHADE,
                coin=(x0 + 42, y0 + 19), chev=(x0 + 17, y0 + 3, y0 + 25))


def render_B(st):
    rows, total = visible(st, B_ROWS)
    sel_row = st["cursor"] - st["scroll"]
    art = sheet()
    cv = Canvas(art)
    b_art(cv, st, len(rows))
    cellpal = {}
    if st["mode"] in ("list", "qty", "confirm"):
        for ty in (2 + 2 * sel_row, 3 + 2 * sel_row):
            for tx in range(16, 29):
                cellpal[(tx, ty)] = 1
        if rows[sel_row][2]:
            bx, by = B_BACKS[sel_row % 3], B_SHELF_Y[sel_row // 3]
            for ty in range(by // 8, by // 8 + 4):
                for tx in range(bx // 8, bx // 8 + 4):
                    cellpal[(tx, ty)] = 1
    out = M.compose(art, cellpal, st["grid"], st["accent"])
    txt = sheet()
    tc = Canvas(txt)
    draw_text(tc, 8, -1, "POKé MART", s(WHITE), s(MART_DARK))
    m = money_str(st["money"])
    draw_text(tc, 230 - text_width(m), -1, m, INK, PANEL_SHADE)
    for r, it in enumerate(rows):
        y = B_LIST_Y + r * 16
        draw_text(tc, B_LIST_X + 6, y, it[0], INK, PANEL_SHADE, font="narrow")
        if it[1] is not None:
            p = money_str(it[1])
            draw_text(tc, B_LIST_X + B_LIST_W - 7 - text_width(p, "narrow"), y, p, INK, PANEL_SHADE, font="narrow")
    draw_text(tc, 8, 114, DESC.get(selected(st)[2], ""), INK, PANEL_SHADE, line_h=14)
    M.overlay(out, txt, st["accent"])
    for k, it in enumerate(rows[:6]):
        if it[2]:
            bx, by = B_BACKS[k % 3], B_SHELF_Y[k // 3]
            put(out, M.icon(it[2]), bx + 4, by + 32 - 24 + 1)
    if total > B_ROWS:
        put(out, M.thumb(), B_TRACK[0] + 1, M.thumb_y(B_TRACK[1], B_TRACK[3], st["scroll"], total, B_ROWS))
    popups(out, st, b_qty)
    return out


# ================================================================== C: register & receipt
C_RX, C_RW = 120, 110           # receipt x, width
C_ROW_Y, C_ROWS = 20, 5
C_TRACK = (233, 17, 238, 104)
C_KEYS = [(60 + 13 * c, 48 + 12 * r) for r in range(3) for c in range(3)]


def torn_edge(x0, x1, y, depth=3):
    """Zigzag bottom edge: for each column the last paper row."""
    return {x: y - abs(((x - x0) % (2 * depth)) - depth) for x in range(x0, x1 + 1)}


def c_art(cv, st, rows_shown, sel_row):
    # ---- receipt strip (pal 0): emerges from the top edge, torn bottom
    x0, x1 = C_RX, C_RX + C_RW - 1
    edge = torn_edge(x0, x1, 107, 3)
    for x in range(x0, x1 + 1):
        for y in range(0, edge[x] + 1):
            cv.set(x, y, PANEL)
        cv.set(x, edge[x] + 1, INK)
        cv.set(x, edge[x], PANEL_SHADE)
    cv.vline(x0, 0, edge[x0], INK)
    cv.vline(x1, 0, edge[x1], INK)
    cv.vline(x0 + 1, 0, edge[x0 + 1] - 1, WHITE)
    cv.vline(x1 - 1, 0, edge[x1 - 1] - 1, PANEL_SHADE)
    for y in (17, 98):                                   # dashed rules
        for x in range(x0 + 4, x1 - 3):
            if (x - x0) % 4 < 2:
                cv.set(x, y, PANEL_SHADE)
    if sel_row is not None and 0 <= sel_row < rows_shown:
        y = C_ROW_Y + sel_row * 15
        Wn.selection_bar(cv, x0 + 3, y + 1, C_RW - 6, 14)
    M.track(cv, *C_TRACK)
    # ---- cash register (pal 2)
    # display pod on a neck
    rounded_box(cv, 10, 2, 92, 26, 4, s(BRASS), s(INK), s(BRASS_LIGHT), s(BRASS_DARK))
    rounded_box(cv, 15, 6, 82, 18, 2, s(MART_DARK), s(INK), s(INK_SOFT), s(MART))
    cv.rect(44, 28, 67, 33, s(BRASS_DARK))
    cv.vline(44, 28, 33, s(INK))
    cv.vline(67, 28, 33, s(INK))
    cv.vline(45, 28, 33, s(BRASS))
    # body
    rounded_box(cv, 2, 34, 104, 62, 3, s(MART), s(INK), s(MART_LIGHT), s(MART_DARK))
    cv.rect(4, 36, 103, 39, s(BRASS))
    cv.hline(4, 103, 36, s(BRASS_LIGHT))
    cv.hline(4, 103, 39, s(BRASS_DARK))
    cv.hline(3, 104, 40, s(INK))
    for x in (8, 98):
        M.rivet(cv, x, 44)
        M.rivet(cv, x, 88)
    # key bed + round keys
    rounded_box(cv, 54, 43, 44, 42, 3, s(MART_DARK), s(INK), s(MART_DARK), s(MART))
    for (kx, ky) in C_KEYS:
        disc(cv, kx + 5.5, ky + 5.5, 5.5, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
    # receipt slot + paper stub on the body (left half): little brass plate with the logo bar
    # department keys: two rows of tall flag keys
    rounded_box(cv, 8, 43, 42, 42, 3, s(MART_DARK), s(INK), s(MART_DARK), s(MART))
    for r in range(2):
        for c in range(3):
            rounded_box(cv, 12 + 12 * c, 47 + 18 * r, 10, 15, 2, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
            cv.hline(14 + 12 * c, 19 + 12 * c, 51 + 18 * r, s(PANEL_SHADE))
    # drawer
    rounded_box(cv, 0, 94, 108, 18, 2, s(WOOD), s(INK), s(WOOD_LIGHT), s(WOOD_DARK))
    rounded_box(cv, 42, 100, 24, 6, 2, s(BRASS), s(INK), s(BRASS_LIGHT), s(BRASS_DARK))
    # crank handle
    cv.rect(107, 56, 110, 59, s(BRASS))
    cv.hline(107, 110, 56, s(BRASS_LIGHT))
    cv.hline(106, 111, 55, s(INK))
    cv.hline(106, 111, 60, s(INK))
    cv.vline(111, 55, 75, s(INK))
    cv.vline(110, 60, 74, s(BRASS_DARK))
    disc(cv, 110.5, 76.5, 3, s(WOOD), s(INK), s(WOOD_LIGHT), s(WOOD_DARK))
    # tray: bag style with icon well
    y = 112
    cv.rect(0, y, 239, 159, PANEL)
    cv.hline(0, 239, y, INK)
    cv.hline(0, 239, y + 1, WHITE)
    cv.hline(0, 239, 159, PANEL_SHADE)
    for x in range(2, 238):
        if x % 4 < 2:
            cv.set(x, y + 3, PANEL_SHADE)
    cx, cy = 20, 136
    disc(cv, cx, cy, 16, PANEL_SHADE, None)
    disc(cv, cx, cy, 15, WHITE, INK)
    disc(cv, cx + 0.5, cy + 0.5, 13, PANEL, None)
    ring(cv, cx, cy, 14, PANEL_SHADE)
    cv.vline(38, y + 6, 153, PANEL_SHADE)
    cv.vline(39, y + 6, 153, WHITE)


def c_qty(out, cv, st):
    # register display shows quantity + total; the up/down keys carry the chevrons
    return dict(register=True)


def render_C(st):
    full = st["items"] + [CANCEL]
    rows = full[st["scroll"]:st["scroll"] + C_ROWS]
    total = len(full)
    sel_row = st["cursor"] - st["scroll"] if st["mode"] in ("list", "qty", "confirm") else None
    art = sheet()
    cv = Canvas(art)
    c_art(cv, st, len(rows), sel_row)
    regq = st["mode"] == "qty"
    if regq:   # pressed keys: the up/down keys go gold (re-blit, pal 2 brass)
        for k in (1, 7):
            kx, ky = C_KEYS[k]
            disc(cv, kx + 5.5, ky + 5.5, 5.5, s(BRASS), s(INK), s(BRASS_LIGHT), s(BRASS_DARK))
    out = M.compose(art, {}, st["grid"], st["accent"])
    txt = sheet()
    tc = Canvas(txt)
    draw_text(tc, C_RX + C_RW // 2 - text_width("POKé MART", "small") // 2, 0, "POKé MART", INK, PANEL_SHADE, font="small")
    for r, it in enumerate(rows):
        y = C_ROW_Y + r * 15
        draw_text(tc, C_RX + 8, y, it[0], INK, PANEL_SHADE, font="narrow")
        if it[1] is not None:
            p = money_str(it[1])
            draw_text(tc, C_RX + C_RW - 9 - text_width(p, "narrow"), y, p, INK, PANEL_SHADE, font="narrow")
    if regq:
        q, tot, left = qty_text(st)
        draw_text(tc, 20, 6, q, s(MART_LIGHT), s(INK))
        draw_text(tc, 92 - text_width(tot), 6, tot, s(WHITE), s(INK))
    else:
        m = money_str(st["money"])
        draw_text(tc, 92 - text_width(m), 6, m, s(WHITE), s(INK))
    draw_text(tc, 45, 114, DESC.get(selected(st)[2], ""), INK, PANEL_SHADE, line_h=14)
    M.overlay(out, txt, st["accent"])
    it = selected(st)
    if it[2]:
        K.place(out, M.icon(it[2]), 20, 136)
    if not regq:
        c = M.art_sheet(16, 16)
        M.coin(Canvas(c), 6, 6)
        out.alpha_composite(_rgba(c, st), (19, 9))
    else:
        kx, ky = C_KEYS[1]
        put(out, M.chevron("up"), kx + 1, ky + 3)
        kx, ky = C_KEYS[7]
        put(out, M.chevron("down"), kx + 1, ky + 3)
        # money left on the display's second readout: a small paper chit from the slot
        t2 = sheet()
        c2 = Canvas(t2)
        rounded_box(c2, 4, 97, 34, 13, 2, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
        M.overlay(out, t2, st["accent"])
        t3 = sheet()
        _, _, left = qty_text(st)
        draw_text(Canvas(t3), 35 - text_width(left, "narrow"), 95, left, INK, PANEL_SHADE, font="narrow")
        M.overlay(out, t3, st["accent"])
    if total > C_ROWS:
        put(out, M.thumb(), C_TRACK[0] + 1, M.thumb_y(C_TRACK[1], C_TRACK[3], st["scroll"], total, C_ROWS))
    st2 = dict(st)
    if regq:
        st2["mode"] = "qtymsg"
        st2["msg"] = message_for(st)
    popups(out, st2, None)
    return out


RENDER = {"A": render_A, "B": render_B, "C": render_C}


def render(direction="A", **kw):
    return RENDER[direction](st_defaults(**kw))


# ================================================================== state 07: BUY / SELL / QUIT over the field
def render_menu(cursor=0, icons=False):
    out = M.mart_field((3, 3))
    win = sheet()
    cv = Canvas(win)
    Wn.std_frame(cv, 2, 1, 8 if icons else 6, 6)
    ents = ["BUY", "SELL", "QUIT"]
    for i, e in enumerate(ents):
        y = 8 + 16 * i
        if i == cursor:
            Wn.selection_bar(cv, 18, y + 1, (8 if icons else 6) * 8 - 4, 14)
        draw_text(cv, 40 if icons else 24, y, e, INK, PANEL_SHADE)
    msg_box(cv, "Welcome!\nHow may I serve you?")
    M.overlay(out, win)
    if icons:
        for i, name in enumerate(("poke_ball", "nugget", "escape_rope")):
            ic = M.icon(name) if name != "nugget" else K.item_icon("nugget")
            put(out, ic.crop((4, 4, 20, 20)), 21, 8 + 16 * i)
    return out


# ================================================================== sheets
def label_sheet(items, scale=2, cols=3, pad=16, title=None):
    cw, ch = W * scale, H * scale
    rows = (len(items) + cols - 1) // cols
    top = 28 if title else 0
    im = Image.new("RGBA", (cols * cw + (cols + 1) * pad, rows * (ch + 30) + pad + top), (28, 28, 36, 255))
    d = ImageDraw.Draw(im)
    if title:
        d.text((pad, 10), title, fill=(240, 240, 250))
    for i, (cap, fr) in enumerate(items):
        x = pad + (i % cols) * (cw + pad)
        y = top + pad + (i // cols) * (ch + 30)
        d.text((x, y), cap, fill=(230, 230, 240))
        im.paste(K.upscale(fr, scale), (x, y + 16))
    return im


def art_for(direction, st):
    """BG2 art sheet of a direction's browse screen (for tile/palette counts)."""
    art = sheet()
    cv = Canvas(art)
    rows, _ = visible(st, 6)
    if direction == "A":
        a_art(cv, st, A_ROWS)
        a_tags(cv, st, rows)
    elif direction == "B":
        b_art(cv, st, B_ROWS)
    else:
        c_art(cv, st, C_ROWS, None)
    return art


def states():
    """(file, title, desc, frame) for every state of the recommended direction (A) + pickers B/C."""
    S_ = []
    S_.append(("state_01.png", "01  Browsing — scrolled list",
               "Cursor on Super Potion after scrolling 3 rows: gold pill row, scroll thumb moved down the BW track, "
               "Super Potion now sits on the counter in front of the clerk and its description is pinned on the counter front.",
               render("A", cursor=6, scroll=3)))
    S_.append(("state_02.png", "02  Quantity — hanging price tag",
               "A on Poké Ball: the clerk asks how many; a big manila tag drops over the list. Quantity sits in a recessed "
               "well between small red up/down chevrons (×001 = the ROM's 3-digit format), total top-right, coin + money left below.",
               render("A", cursor=0, mode="qty", qty=1)))
    S_.append(("state_03.png", "03  Confirm — YES / NO",
               "ROM line 'Poké Ball? And you wanted 10? That will be ¥2000.' with the approved std-frame YES/NO (gold pill).",
               render("A", cursor=0, mode="confirm", qty=10)))
    S_.append(("state_04.png", "04  Bought — Premier Ball bonus",
               "After 'Here you go! Thank you very much.' the clerk adds the bonus: a Premier Ball pops onto the counter next "
               "to the Poké Ball and the money sign now reads ¥1000.",
               render("A", cursor=0, mode="msg", money=1000, bonus=True, msg="I'll throw in a PREMIER BALL, too.")))
    S_.append(("state_05.png", "05  Not enough money",
               "¥250 left, Escape Rope costs ¥550: ROM message, list stays on the item.",
               render("A", cursor=4, money=250, mode="msg", msg="You don't have enough money.")))
    S_.append(("state_06.png", "06  TM shop",
               "TM rows show a small disc in the move's type colour + the move name (one shared OBJ palette for all discs); "
               "the full Gen 3 TM icon in that type's palette sits on the counter.",
               render("A", items=TMS, cursor=0, money=8000)))
    S_.append(("state_07.png", "07  BUY / SELL / QUIT over the field",
               "The real LAYOUT_MART map with the clerk; std Orchid frame, gold pill, no icons (context-menu rule). "
               "The ROM's labels are BUY / SELL / QUIT.",
               render_menu(0)))
    S_.append(("state_08.png", "08  Quantity picker in B (shelves)",
               "Same picker as a shared std Orchid window: up/down chevrons around the quantity well, total, coin + money left.",
               render("B", cursor=0, mode="qty", qty=1)))
    S_.append(("state_09.png", "09  Quantity picker in C (register)",
               "The register display shows ×001 and the total; the up/down keys light brass with red chevrons, "
               "and a paper chit tucked on the cash drawer shows the money left.",
               render("C", cursor=0, mode="qty", qty=1)))
    return S_


def tm_discs(out, rows):
    for r, it in enumerate(rows):
        if it[2] and it[2].startswith("tm_"):
            put(out, M.tm_disc(it[2][3:]), A_LIST_X + 5, A_LIST_Y + r * 16 + 2)


def parts_sheet():
    """New pieces at 4x on the grid."""
    pieces = []
    def piece(w, h, fn, cap, objs=None):
        art = M.art_sheet(w, h)
        fn(Canvas(art))
        im = M.compose(art, {}, 0)
        if objs:
            objs(im)
        pieces.append((cap, im))
    piece(64, 16, lambda cv: M.awning(cv, 0, 63), "awning: brass rail, pleated stripes, round scallops (pal 2, 16x16 repeat)")
    def sign(cv):
        for x in (16, 78):
            M.rod(cv, x, 0, 5)
        M.wood_board(cv, 4, 5, 88, 20, r=3, grain=False)
        for x, y in ((7, 8), (85, 8), (7, 20), (85, 20)):
            M.rivet(cv, x, y)
        M.coin(cv, 17, 15, 6.5)
        rounded_box(cv, 28, 8, 54, 14, 3, s(PANEL), s(INK), s(WHITE), s(PANEL_SHADE))
        draw_text(cv, 80 - text_width("¥3000"), 6, "¥3000", INK, PANEL_SHADE)
    piece(96, 28, sign, "money sign: hanging wood board, brass rivets, coin + cream money pill")
    def tags(cv):
        rounded_box(cv, 0, 1, 128, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
        M.price_tag(cv, 128 - 44 - 2, 2, 44, 12)
        draw_text(cv, 7, 0, "Paralyze Heal", INK, PANEL_SHADE, font="narrow")
        draw_text(cv, 120 - text_width("¥200", "narrow"), 0, "¥200", INK, SPARE_B, font="narrow")
    piece(128, 16, tags, "list pill + price tag (pal 0 spares = manila, so it stays manila on the gold row)")
    def counter(cv):
        cv.rect(0, 0, 95, 0, s(INK))
        cv.rect(0, 1, 95, 2, s(WOOD_LIGHT))
        cv.rect(0, 3, 95, 5, s(WOOD))
        cv.hline(0, 95, 6, s(WOOD_DARK))
        cv.hline(0, 95, 7, s(INK))
        cv.rect(0, 8, 95, 24, s(WOOD))
        cv.hline(0, 95, 8, s(WOOD_DARK))
        for y, c in ((12, INK), (13, BRASS), (14, MART_LIGHT), (18, MART_DARK), (19, BRASS_DARK), (20, INK)):
            cv.hline(0, 95, y, s(c))
        cv.rect(0, 15, 95, 17, s(MART))
    piece(96, 25, counter, "counter: wood top + Mart-blue band with brass edges")
    piece(96, 32, lambda cv: M.wall_shelf(cv, 2, 93, 16), "back-wall shelf: goods on BG pal 4 (Gen 3 icon colours) above a tile-aligned plank + brass brackets (pal 2)")
    def qty(cv):
        st = st_defaults(cursor=0, mode="qty", qty=10)
        a_qty(None, cv, st)
    art = M.art_sheet(240, 112)
    q = a_qty(None, Canvas(art), st_defaults(cursor=0, mode="qty", qty=10))
    im = M.compose(art, {}, 0).crop((112, 60, 236, 112))
    pieces.append(("quantity tag (BG1), see state_02 for text", im))
    c = M.art_sheet(32, 16)
    cv = Canvas(c)
    M.coin(cv, 6, 6, 6.5)
    pieces.append(("coin (pal 2 brass)", M.compose(c, {}, 0)))
    d = Image.new("RGBA", (112, 16))
    d = K.grid_frame(0, 112, 16)
    for i, tname in enumerate(("ground", "poison", "water", "fire", "electric", "ice")):
        put(d, M.tm_disc(tname), 2 + i * 18, 2)
    pieces.append(("TM discs: 6 types, one shared OBJ palette", d))
    ch = K.grid_frame(0, 48, 16)
    for i, dname in enumerate(("up", "down", "left", "right")):
        spr = M.chevron(dname)
        put(ch, spr, 2 + i * 12, 3)
    pieces.append(("chevrons: kit 6x9 red, transposed for up/down", ch))
    SC = 4
    width = 16 + max(p[1].size[0] for p in pieces) * SC + 16
    height = sum(p[1].size[1] * SC + 30 for p in pieces) + 16
    sh = Image.new("RGBA", (max(width, 900), height), (28, 28, 36, 255))
    dr = ImageDraw.Draw(sh)
    y = 12
    for cap, im in pieces:
        dr.text((16, y), cap, fill=(230, 230, 240))
        sh.paste(K.upscale(im, SC), (16, y + 14))
        y += im.size[1] * SC + 30
    return sh


def budget():
    lines = []
    for d in "ABC":
        n, conf, use = M.check_tiles(art_for(d, st_defaults()))
        lines.append("%s BG2 shop art: %d unique tiles incl. blank (< 256 OK with the BG3 grid at screenblock 28), "
                     "palette conflicts per tile: %d; tiles on pal 0/1 (Orchid): %d, pal 2 (SHOP): %d."
                     % (d, n, len(conf), use.get(0, 0), use.get(2, 0)))
    return lines


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    base = dict(cursor=1)
    v = [("A  Counter & awning", render("A", **base)), ("B  Shelves", render("B", **base)),
         ("C  Register / receipt", render("C", **base))]
    label_sheet(v, 2, 3, title="Poke Mart buy screen - three directions, same data (cursor on Potion, P3000)").save(
        os.path.join(OUT, "variants.png"))
    K.upscale(render("A", **base), 3).save(os.path.join(OUT, "main.png"))
    for f, title, desc, fr in states():
        K.upscale(fr, 3).save(os.path.join(OUT, f))
    acc = [("Mart blue awning + counter band (recommended)", render("A", **base)),
           ("Orchid purple instead (one accent)", render("A", accent="orchid", **base))]
    label_sheet(acc, 2, 2).save(os.path.join(OUT, "accent_ab.png"))
    mn = [("No icons (recommended)", render_menu(0)), ("With small icons", render_menu(0, icons=True))]
    label_sheet(mn, 2, 2).save(os.path.join(OUT, "menu_ab.png"))
    pk = [("A  hanging price tag", render("A", cursor=0, mode="qty", qty=10)),
          ("B  std Orchid window", render("B", cursor=0, mode="qty", qty=10)),
          ("C  register display + keys", render("C", cursor=0, mode="qty", qty=10))]
    label_sheet(pk, 2, 3, title="Quantity picker - x010 Poke Balls in each direction").save(os.path.join(OUT, "pickers.png"))
    parts_sheet().save(os.path.join(OUT, "parts.png"))
    bl = budget()
    qa = M.art_sheet()
    a_qty(None, Canvas(qa), st_defaults(cursor=0, mode="qty"))
    nq, cq, _ = M.check_tiles(qa)
    bl += [
        "Layers: BG0 text windows + std frames/message box (pal 15 = Orchid kit, as vanilla), BG1 quantity tag "
        "(%d tiles, pal 0, conflicts %d), BG2 shop art, BG3 BW grid (pal 3). Emerald's live map view (BG1-3) is dropped." % (nq, len(cq)),
        "BG palettes: 0 Orchid kit with SPARE_A/B = price-tag manila (wood_mail.pal), 1 = selected-row swap of 0 (gold, "
        "as the bag), 2 = SHOP (kit neutrals + wood / Mart blue / brass), 3 = grid, 4 = GOODS (A's wall-shelf stock: Poké Ball, "
        "potion, repel, cardboard colours from their icon .pal files + a dark-wood back panel). 5 of 16 (+ text pal 15). "
        "The shelf plank sits on a tile boundary (y 56) so goods (pal 4) and wood (pal 2) never share a tile.",
        "Selection = per-cell palette swap 0->1 on the selected pill's 2 tile rows (tags keep manila because they use the spares).",
        "OBJ (A): item icon 32x32 x2 (vanilla double-buffered iconSlot) = 32 tiles, 2 pals; clerk 16x32 = 8 tiles, npc_1 pal "
        "(priority under BG2 so the counter hides his legs); scroll thumb 8x16 = 2 tiles; red chevrons 2x 16x8 = 4 tiles, 1 pal "
        "(Gen 3 red.pal) + the picker coin 16x16 (4 tiles) whose brass ramp shares that palette; TM discs 6x 16x16 = 24 tiles, ONE shared pal (6 type ramps); bonus Premier Ball 32x32 + pal. "
        "Peak 7 OBJ palettes of 16, ~70 OBJ tiles.",
        "B: 6 shelf icons = 6x 32x32 OBJ + 6 palettes (peak 9). C: 1 icon (tray well) + coin drawn on BG.",
    ]
    for l in bl:
        print(l)
    notes = {
        "title": "Poké Mart — buy screen (shared, Orchid + Mart-blue shop accent)",
        "main": {"file": "main.png", "zones": [
            ["Awning", "Brass rail + Mart-blue/white pleated stripes with round scallops (16px repeat, 2 tile rows, pal 2); the grid shows between scallops."],
            ["Money sign", "Wood board hanging from the awning on brass rods: rivets, a gold coin (picture instead of the MONEY label) and a cream money pill in the ROM's ¥ (Pokédollar) format."],
            ["Wall shelf", "Back-wall shelf behind the clerk: Poké Ball pyramids, potion bottles, cardboard boxes and repel cans in Gen 3 icon colours on a dark-wood panel, wood plank on brass brackets (BG2, pal 4 + pal 2)."],
            ["Clerk counter", "The real Mart-employee overworld sprite behind a wood counter with a brass front lip and a brass-edged Mart-blue band; the selected item sits on the counter in front of her."],
            ["Price-tag list", "6 pill rows as in the bag; each pill's right end is a manila price tag (pointed end, punched hole), sized from the widest price + 18px so the price clears the hole and the tag end by >= 2px. Selected row = gold pill, tag stays manila."],
            ["Scrollbar", "Bag's BW recessed track + gold thumb (OBJ)."],
            ["Description card", "Cream card pinned on the counter front (wood frame, brass rivets); 3 lines at 14px pitch from y 116."]]},
        "states": [{"file": f, "title": ti, "desc": de} for f, ti, de, _ in states()],
        "gifs": [{"file": "buy.gif", "title": "Buying 4 Super Potions",
                  "desc": "Six Down presses 12 frames apart (6th scrolls the list), A on Super Potion: clerk line prints at 1 char/frame, "
                          "tag drops in, three Up presses (×002-×004, total and money left update), A: confirm prints, YES/NO, A: money "
                          "sign drops to ¥200 and 'Here you go!' prints. 60 fps, 1 GIF frame per 2 GBA frames."}],
        "extras": [
            {"file": "variants.png", "title": "Directions A / B / C", "desc": "Same data at 2x. A counter & awning, B shelf cubbies + compact price list, C cash register + receipt strip."},
            {"file": "pickers.png", "title": "Quantity picker in each direction", "desc": "×010 Poké Balls: A hanging tag, B std Orchid window, C register display + lit keys."},
            {"file": "accent_ab.png", "title": "Shop accent: Mart blue vs Orchid purple", "desc": "Same screen, only pal 2's three accent colours swapped."},
            {"file": "menu_ab.png", "title": "BUY / SELL / QUIT: icons or not", "desc": "Left = recommended (no icons); right = 16x16 crops of Poké Ball / Nugget / Escape Rope."},
            {"file": "parts.png", "title": "New pieces at 4x", "desc": "Awning, money sign, pill + price tag, counter band, wall shelf, quantity tag, coin, TM discs, chevrons."}],
        "budget": bl,
        "kit_additions": [
            "mart_ext.shop_pal(): SHOP BG palette on fixed roles (7-9 wood from wood_mail.pal, 10-12 Mart blue from general/palettes/04.pal, 13-15 brass = battle_ext HB_PAL brass).",
            "mart_ext.art_sheet/compose/check_tiles: two-palette BG art (pal 0 roles 0-15, pal 2 roles 32-47) with a per-tile one-palette validator + tile count.",
            "mart_ext.price_tag(): manila tag with pointed end + punched hole (pal 0 spares) — reusable for any price/label.",
            "mart_ext.awning(), rod(), wood_board(), rivet(), coin(): shop dressing pieces.",
            "mart_ext.wall_shelf() + goods_pal(): back-wall shelf with stock sprites (BALL7, BOTTLE, CAN, box()) on a GOODS BG palette.",
            "mart_ext.chevron('up'|'down'): kit SMALL_ARROW transposed for vertical value pickers.",
            "mart_ext.tm_disc(type): 12x12 TM disc, six types on ONE shared OBJ palette (from *_tm_hm.pal).",
            "mart_ext.mart_field(): renders the real LAYOUT_MART map + clerk/player sprites for field-menu mockups."],
        "questions": [
            ["Which direction: A, B or C?",
             "A counter & awning reads as a shop at a glance (awning, clerk, counter, price tags) and keeps the bag's 6-row pill list; "
             "B shelves is the best for browsing by picture but repeats the names in a second list and needs 6 icon palettes; "
             "C register/receipt is charming but shows only 5 rows and the register eats the left half. **Recommendation: A** "
             "(B's shelf could come back for the Lilycove-style department store later)."],
            ["Shop accent colour",
             "Mart blue (Poké Mart roof ramp) as a second BG palette on the shop dressing only — awning, counter band — while every "
             "interactive piece (pills, gold selection, frames, message box) stays Orchid; or Orchid purple everywhere (accent_ab.png). "
             "Costs one BG palette, no extra tiles. **Recommendation: Mart blue** — it ties the screen to the building the player just walked into."],
            ["Quantity picker style",
             "A's hanging price tag (BG1), B's std Orchid window, or C's register keys (pickers.png). **Recommendation: the tag** — it "
             "matches the list's price tags and has room for total + coin/money-left; fall back to the std window if BG1 is needed elsewhere."],
            ["Money and quantity format",
             "The ROM prints ¥3000 with its Pokédollar glyph and no thousands separator, and ×001 (3 digits because MAX_BAG_ITEM_CAPACITY "
             "is 999). Messages use the ROM strings ('...And you wanted 10? That will be ¥2000.'). Note I_PRICE = GEN_LATEST will make some "
             "prices differ from these mockups (Potion ¥200, Repel ¥400). **Recommendation: keep the ROM formats** (no string/engine changes)."],
            ["Icons on BUY / SELL / QUIT?",
             "It is a context-style menu, and the item icons have to be cropped to 16x16 to fit (menu_ab.png). The ROM labels are BUY / SELL / QUIT. "
             "**Recommendation: no icons** — gold pill only, as the approved context-menu rule."]],
    }
    json.dump(notes, open(os.path.join(OUT, "notes.json"), "w"), indent=1, ensure_ascii=False)
