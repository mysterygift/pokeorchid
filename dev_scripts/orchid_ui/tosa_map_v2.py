"""
Tosa region map v2 — built from the USER's art (dev_scripts/orchid_ui/ref/tosa_*.png, 240x160):
  tosa_terrain.png  base terrain (7 colours, Hoenn region-map palette)
  tosa_towns.png    + red 8x8 squares = town / landmark cells
  tosa_routes.png   + orange land routes, blue sea routes
Terrain and routes are used pixel for pixel. Screen pixel = map-art pixel (unzoomed), cell (x, y)
of the 28x15 cursor grid = 8x8 px at (8 + 8x, 16 + 8y), as region_map.c.

Mock sheet: Town Map, Fly map and dex AREA views in the Orchid frame, each red square numbered.
usage: tosa_map_v2.py OUT_DIR
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from kit import *
import kit_ext as KX
import dex_ext as D
import mock_dex as M
from gamefont import draw_text, text_width

W, H = 240, 160
GX, GY = 8, 16
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref")
RED = (255, 0, 0)
TOWN = ((32, 74, 197), (65, 106, 205))      # Hoenn region-map town pin colours


def load(name):
    return Image.open(os.path.join(REF, name)).convert("RGB")


def squares():
    """Red 8x8 squares of tosa_towns.png, numbered top-to-bottom, left-to-right -> [(n, cx, cy)]."""
    im = load("tosa_towns.png")
    px = im.load()
    out = []
    for y in range(0, H, 8):
        for x in range(0, W, 8):
            if px[x, y] == RED and px[x + 7, y + 7] == RED:
                out.append(((x - GX) // 8, (y - GY) // 8))
    return [(i + 1, cx, cy) for i, (cx, cy) in enumerate(out)]


def map_art(pins=True):
    """The ROM map art: tosa_routes.png; red squares -> Gen 3 town pins drawn over the user's
    background (pixels outside the pin keep the user's terrain/route)."""
    im = load("tosa_routes.png")
    bg = load("tosa_terrain.png").load()
    px = im.load()
    for n, cx, cy in squares():
        x0, y0 = GX + cx * 8, GY + cy * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = bg[x0 + x, y0 + y]       # the user's terrain under the square
                if pins:
                    d = math.hypot(x - 3.5, y - 3.5)
                    if d < 3.9:
                        px[x0 + x, y0 + y] = TOWN[0] if d > 2.6 else TOWN[1]
        if pins:
            px[x0 + 2, y0 + 2] = (255, 255, 255)
            px[x0 + 3, y0 + 2] = (255, 255, 255)
    return im


def tile_budget(im):
    px = im.load()
    rows = set()
    for ty in range(2, 17):            # tile rows 2..16 = y 16..135 (the cursor grid rows)
        for tx in range(30):
            rows.add(tuple(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)))
    return len(rows)


def frame(out, title, loc, desc, header_tabs=False):
    pal = D.dex_palette("orchid")
    art = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    cv = Canvas(art)
    D.header_band(cv, 0, W - 1, round_left=False)
    rounded_box(cv, 2, 17, 236, 118, 4, TRANSPARENT, INK, ACCENT_DARK, ACCENT_LIGHT)
    for y in range(17, 135):
        for x in (0, 1, 238, 239):
            cv.set(x, y, ACCENT)
    D.tray(cv, 136)
    rounded_box(cv, 6, 140, 104, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    out.alpha_composite(KX.sheet_rgba(art, pal))
    txt = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    tc = Canvas(txt)
    draw_text(tc, (W - text_width(title)) // 2, 0, title, WHITE, ACCENT_DARK)
    draw_text(tc, 12, 139, loc, INK, PANEL_SHADE)
    draw_text(tc, 116, 139, desc, INK, PANEL_SHADE, font="narrow")
    out.alpha_composite(KX.sheet_rgba(txt, pal))


def cursor(out, cell, head=True):
    cur = KX.sprite_rgba(KX.G("pokenav", "region_map", "cursor_small.png"), 0, 16,
                         pal=KX.load_jasc(KX.G("pokenav", "region_map", "cursor.pal")))
    x0, y0 = GX + cell[0] * 8, GY + cell[1] * 8
    out.alpha_composite(cur, (x0 - 4, y0 - 4))
    if head:
        out.alpha_composite(KX.sprite_rgba(KX.G("pokenav", "region_map", "brendan_icon.png")), (x0 - 4, y0 - 4))


def town_map_view(art):
    out = art.convert("RGBA")
    frame(out, "TOSA", "Tosa Port", "(names pending)")
    cursor(out, (4, 11))
    return out


def fly_view(art):
    out = art.convert("RGBA")
    frame(out, "FLY", "Tosa Port", "Fly here?")
    icons = KX.sprite_rgba(KX.G("pokenav", "region_map", "fly_target_icons.png"))
    ico = icons.crop((0, 0, 8, 8))
    for n, cx, cy in squares():
        out.alpha_composite(ico, (GX + cx * 8, GY + cy * 8))
    cursor(out, (4, 11), head=False)
    return out


def area_view(art, glow_cells):
    """Dex AREA tab: the map shows in the right-hand well (BG2 clipped to the well, panned to
    the habitats), vanilla-style glow on the habitat cells."""
    out = M.render_entry(entry_index=25, tab=1)          # Taillow AREA frame
    x0, y0, x1, y1 = M.AREA_WELL
    ww, wh = x1 - x0 - 3, y1 - y0 - 3
    cx = sum(GX + c[0] * 8 + 4 for c in glow_cells) // len(glow_cells)
    cy = sum(GY + c[1] * 8 + 4 for c in glow_cells) // len(glow_cells)
    sx = max(0, min(W - ww, cx - ww // 2))
    sy = max(GY, min(GY + 120 - wh, cy - wh // 2))
    m = art.copy().convert("RGBA")
    g = Image.new("RGBA", m.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for c in glow_cells:
        X, Y = GX + c[0] * 8, GY + c[1] * 8
        gd.rectangle([X - 1, Y - 1, X + 8, Y + 8], fill=(248, 120, 48, 150))
        gd.rectangle([X + 1, Y + 1, X + 6, Y + 6], fill=(248, 232, 96, 200))
    m.alpha_composite(g)
    out.paste(m.crop((sx, sy, sx + ww, sy + wh)), (x0 + 2, y0 + 2))
    return out, (sx - (x0 + 2), sy - (y0 + 2))


def number(im, scale, cells, offset=(0, 0), font=None, clip=None):
    d = ImageDraw.Draw(im, "RGBA")
    for n, cx, cy in cells:
        X = (GX + cx * 8 - offset[0]) * scale
        Y = (GY + cy * 8 - offset[1]) * scale
        if clip and not (clip[0] <= X / scale < clip[2] and clip[1] <= Y / scale < clip[3]):
            continue
        t = str(n)
        tw = d.textlength(t, font=font)
        d.rectangle([X + 8 * scale - 2, Y - 14, X + 8 * scale + tw + 3, Y + 6], fill=(0, 0, 0, 190))
        d.text((X + 8 * scale, Y - 14), t, font=font, fill=(255, 255, 255))


if __name__ == "__main__":
    out_dir = sys.argv[1]
    sq = squares()
    art = map_art(pins=True)
    f = ImageFont.load_default(size=16)
    fb = ImageFont.load_default(size=18)
    S = 3
    views = [("Town Map (field_region_map.c)", town_map_view(art), (0, 0), None),
             ("Fly map (region_map.c)", fly_view(art), (0, 0), None)]
    av, off = area_view(art, [(5, 11)])
    x0, y0, x1, y1 = M.AREA_WELL
    views.append(("Dex AREA tab (pokedex_area_screen.c), Reserve cell glowing", av, off, (x0 + 2, y0 + 2, x1 - 1, y1 - 1)))
    sheet = Image.new("RGB", (3 * (W * S + 16) + 16, 34 + H * S + 12 + 13 * 23 + 12), (24, 24, 32))
    d = ImageDraw.Draw(sheet)
    for i, (cap, im, off, clip) in enumerate(views):
        big = KX.upscale(im.convert("RGB"), S)
        number(big, S, sq, off, f, clip)
        x = 16 + i * (W * S + 16)
        sheet.paste(big, (x, 34))
        d.text((x, 8), cap, font=fb, fill=(230, 230, 240))
    lines = [
        "Squares (cell = 28x15 cursor grid; px = 8 + 8x, 16 + 8y):",
        "  " + "   ".join("%d:(%d,%d)" % s for s in sq[:10]),
        "  " + "   ".join("%d:(%d,%d)" % s for s in sq[10:]),
        "Proposed: #15 (4,11) = Tosa Port (its existing cell). South Tosa Reserve = the route cell (5,11), the only route out of Tosa Port.",
        "          Telok Town = #16 (6,11), the next square along that route (in game: Port -> Reserve -> Telok). All other squares: names needed.",
        "Routes: #15-(5,11)-#16; #16 north to #8 (6,7) and south to #19 (10,13); #13 (0,9) east to x=4 then north to #2 (4,3);",
        "        #8-#9 (row 7); #9-#6-#5 (rows 5-7); #14 (10,9) to #17 (12,11) to #18 (16,11); #3-#4-#7-#10-#11-#12 in the north-east;",
        "        sea route from #1 (12,1) east along row 1, then down column 24 to #12 (24,7).",
        "Petalburg: map.json puts it EAST of the Reserve; in this art nothing else joins the Reserve route (5,11), and the only",
        "        west square (#13, Petalburg's old spot) is not linked to Tosa Port. So the art doesn't place Petalburg; name for #13?",
        "ROM-art fit: the user's art is used as-is for tile rows 2-16 (y 16-135 = the cursor grid): 233 unique 8x8 tiles = vanilla's",
        "        -num_tiles 233 (affine BG, max 256, no flips). Rows 0-1 and 17-19 sit under the header / tray in every view and become",
        "        plain sea in the 512x512 affine map. Red squares -> Gen 3 blue town pins over the user's ground: %d tiles with pins." % tile_budget(art),
    ]
    for i, t in enumerate(lines):
        d.text((16, 34 + H * S + 12 + i * 23), t, font=f, fill=(230, 230, 240))
    sheet.save(os.path.join(out_dir, "tosa_map_mock_v2.png"))
    print("ok", sheet.size, "tiles", tile_budget(art), "squares", len(sq))
