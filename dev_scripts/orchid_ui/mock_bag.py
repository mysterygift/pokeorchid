"""
Pixel-accurate mockups of the satchel bag screen.

Composites exactly what the GBA will show: BG2 art (with per-cell palette
variants for the highlighted / empty pill rows), BG0 text drawn with the real
font, and OBJ sprites (satchel, pocket buttons, item icon, Gen 3 arrows).

usage: mock_bag.py OUT_DIR
"""
import os
import sys
from PIL import Image
from kit import *
import bag_screen as B
from gamefont import draw_text, text_width

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
G = lambda *p: os.path.join(ROOT, "graphics", *p)


def load_jasc(path):
    lines = open(path).read().split()
    n = int(lines[2])
    v = list(map(int, lines[3:3 + n * 3]))
    return [tuple(v[i:i + 3]) for i in range(0, len(v), 3)]


def sprite_rgba(png, frame=0, fh=None, pal=None, hflip=False, vflip=False):
    im = Image.open(png)
    fh = fh or im.size[1]
    im = im.crop((0, frame * fh, im.size[0], frame * fh + fh))
    if pal:
        flat = [c for rgb in pal for c in rgb]
        im.putpalette(flat + [0] * (768 - len(flat)))
    rgba = im.convert("RGBA")
    px, ipx = rgba.load(), im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if ipx[x, y] == 0:
                px[x, y] = (0, 0, 0, 0)
    if hflip:
        rgba = rgba.transpose(Image.FLIP_LEFT_RIGHT)
    if vflip:
        rgba = rgba.transpose(Image.FLIP_TOP_BOTTOM)
    return rgba


def place(canvas, spr, cx, cy):
    canvas.alpha_composite(spr, (int(cx - spr.size[0] // 2), int(cy - spr.size[1] // 2)))


POCKETS = ["ITEMS", "POKé BALLS", "TMs & HMs", "BERRIES", "KEY ITEMS"]
ITEMS = [("Potion", 5, "potion"), ("Super Potion", 2, "super_potion"), ("Antidote", 3, "antidote"),
         ("Escape Rope", 1, "escape_rope"), ("Repel", 4, "repel"), ("Rare Candy", 1, "rare_candy"),
         ("Max Repel", 2, "max_repel")]
DESC = {"potion": "Restores the HP of\na Pokémon by\n20 points.",
        "super_potion": "Restores the HP of\na Pokémon by\n60 points."}


ICON_ALIAS = {"super_potion": "potion", "max_repel": "repel", "great_ball": "poke_ball", "ultra_ball": "poke_ball"}


def item_icon(name):
    png = G("items", "icons", ICON_ALIAS.get(name, name) + ".png")
    if not os.path.exists(png):
        png = G("items", "icons", name + ".png")
    pal = G("items", "icon_palettes", name + ".pal")
    if not os.path.exists(png):
        return None
    return sprite_rgba(png, pal=load_jasc(pal) if os.path.exists(pal) else None)


def render(theme="male", pocket=0, cursor=0, scroll=0, items=None, desc=None, popup=None, note=None,
           cursor_glyph=False, grid_scroll=0, overrides=None):
    items = ITEMS if items is None else items
    ov = overrides or {}
    rows_visible = ov.get("rows_visible", B.ROWS)
    base_pal = palette(theme)
    pals = {0: base_pal, 1: B.variant(base_pal, "selected"), 2: B.variant(base_pal, "ghost")}

    bg = B.build_bg(theme)
    bare = B.build_bg(theme, pills=False)   # unused rows show the backdrop
    rows = items[scroll:scroll + B.ROWS] + [None]
    shown = min(len(items) + 1 - scroll, B.ROWS)        # +1 for CLOSE BAG
    rows = (items[scroll:] + [("CLOSE BAG", None, None)])[:B.ROWS]

    # per-cell palette numbers for the pill rows (tile rows 2..13, cols 12..29 incl. gutter/track)
    cellpal = {}
    for r in range(B.ROWS):
        kind = 3 if (r >= shown or r >= rows_visible) else (1 if r == cursor else 0)
        for ty in (2 + 2 * r, 3 + 2 * r):
            for tx in range(13, 29):
                cellpal[(tx, ty)] = kind

    out = Image.new("RGBA", (B.W, B.H))
    from backdrop import GRID_PAL, grid_index
    opx, bpx, npx = out.load(), bg.load(), bare.load()
    for y in range(B.H):
        for x in range(B.W):
            k = cellpal.get((x // 8, y // 8), 0)
            v = npx[x, y] if k == 3 else bpx[x, y]
            if v == 0:   # transparent: BG3 grid shows through, scrolling down-right
                opx[x, y] = GRID_PAL[grid_index(x - grid_scroll, y - grid_scroll)] + (255,)
            else:
                opx[x, y] = pals[0 if k == 3 else k][v] + (255,)

    # --- BG0 text layer (always palette 0) ---------------------------------
    txt = new_sheet(B.W, B.H, theme)
    tc = Canvas(txt)
    # pocket name, white on accent with dark-accent shadow, centred in the header
    name = POCKETS[pocket]
    draw_text(tc, B.POCKET_NAME_CX - text_width(name) // 2, 0, name, WHITE, ACCENT_DARK)
    for r, it in enumerate(rows):
        if r >= rows_visible or ov.get("hide_list_text"):
            continue
        y = B.LIST_Y + r * B.ROW_H
        label, qty, _ = it
        draw_text(tc, B.PILL_X + 7, y, label, INK, PANEL_SHADE, font="narrow")
        if isinstance(qty, str):
            draw_text(tc, B.PILL_X + B.PILL_W - 9 - text_width(qty, "narrow"), y, qty, ACCENT_DARK, PANEL_SHADE, font="narrow")
        elif qty is not None:
            q = "×%2d" % qty
            draw_text(tc, B.PILL_X + B.PILL_W - 9 - text_width(q, "narrow"), y, q, INK, PANEL_SHADE, font="narrow")
    # Gen 3 black arrow cursor in the gutter
    if cursor_glyph:
        draw_text(tc, B.LIST_X, B.LIST_Y + cursor * B.ROW_H, "▶", INK, WHITE)
    sel = rows[cursor]
    d = desc if desc is not None else (DESC.get(sel[2], "A useful item.") if sel[2] else "Close the BAG and\nreturn to the field.")
    if not ov.get("hide_list_text"):
        draw_text(tc, B.DESC_X, B.DESC_Y, d, INK, PANEL_SHADE, line_h=B.DESC_LINE_H)
    tpx, tcol = txt.load(), base_pal
    for y in range(B.H):
        for x in range(B.W):
            if tpx[x, y]:
                opx[x, y] = tcol[tpx[x, y]] + (255,)

    # --- OBJ layer ---------------------------------------------------------
    satchel = G("bag", "satchel_%s.png" % theme)
    if os.path.exists(satchel):
        spr = sprite_rgba(satchel, frame=ov.get("satchel_frame", pocket + 1), fh=64)
        if ov.get("satchel_rot"):
            spr = spr.rotate(ov["satchel_rot"], resample=Image.NEAREST)
        place(out, spr, B.WHEEL_C[0], B.WHEEL_C[1] + ov.get("satchel_dy", 0))
    else:
        place(out, sprite_rgba(G("bag", "bag_%s.png" % theme), frame=1, fh=64), *B.WHEEL_C)
    icons = G("bag", "pocket_icons.png")
    for k, (bx, by) in enumerate(B.button_centres()):
        if os.path.exists(icons):
            selk = ov.get("sel_button", pocket)
            place(out, sprite_rgba(icons, frame=k + (5 if k == selk else 0), fh=32), bx, by)
    if ov.get("ring"):
        # travelling gold selection ring (OBJ), drawn over the buttons
        rim = new_sheet(32, 32, theme)
        rc = Canvas(rim)
        ring(rc, 16, 16, 12.5, INK)
        ring(rc, 16, 16, 11.5, SELECT_DARK)
        ring(rc, 16, 16, 10.5, SELECT)
        ring(rc, 16, 16, 9.5, SELECT_LIGHT)
        ring(rc, 16, 16, 8.5, INK)
        rr = rim.convert("RGBA")
        rp, ip = rr.load(), rim.load()
        for yy in range(32):
            for xx in range(32):
                if ip[xx, yy] == 0:
                    rp[xx, yy] = (0, 0, 0, 0)
        place(out, rr, *ov["ring"])
    # scrollbar thumb
    total = len(items) + 1
    tx0, ty0, tx1, ty1 = B.TRACK
    span = (ty1 - ty0 - 3) - 12
    ty = ty0 + 2 + (span * scroll // max(1, total - B.ROWS) if total > B.ROWS else 0)
    thumb = new_sheet(4, 12, theme)
    rounded_box(Canvas(thumb), 0, 0, 4, 12, 1, SELECT, INK, SELECT_LIGHT, SELECT_DARK)
    th = thumb.convert("RGBA")
    tp, ip = th.load(), thumb.load()
    for yy in range(12):
        for xx in range(4):
            if ip[xx, yy] == 0:
                tp[xx, yy] = (0, 0, 0, 0)
    if total > B.ROWS:
        out.alpha_composite(th, (tx0 + 1, ty))
    # small Gen 3 red pocket arrows (6x9 chevrons)
    from kit import SMALL_ARROW, ARROW_RED
    for i, (ax, ay) in enumerate(B.POCKET_ARROWS):
        for r, row in enumerate(SMALL_ARROW):
            row = row[::-1] if i == 1 else row
            for c, ch in enumerate(row):
                if ch in "OF":
                    opx[ax - 3 + c, ay - 4 + r] = (ARROW_RED[0] if ch == "F" else ARROW_RED[1]) + (255,)
    # item icon
    if sel[2] and not ov.get("hide_list_text"):
        ic = item_icon(sel[2])
        if ic:
            place(out, ic, *B.ICON_WELL_C)
    else:
        pass
    if popup:
        popup(out, theme)
    return out


def upscale(im, k=3):
    return im.resize((im.size[0] * k, im.size[1] * k), Image.NEAREST)


if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    a = render("male", 0, cursor=1)
    b = render("female", 0, cursor=0)
    sheet = Image.new("RGBA", (B.W * 3 * 2 + 24, B.H * 3), (32, 32, 40, 255))
    sheet.paste(upscale(a), (0, 0))
    sheet.paste(upscale(b), (B.W * 3 + 24, 0))
    sheet.save(os.path.join(outdir, "mock_bag_v1.png"))
    tiles, _ = to_tiles(B.build_bg("male"))
    print("BG2 unique tiles:", len(tiles), "/ 320")
