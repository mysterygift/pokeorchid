"""
Tosa region map — LAYOUT SKETCH for the user to correct (not final art).

Gen 3 region-map pixel style (colours taken from graphics/pokenav/region_map/map.png), on the
vanilla 28x15-cell grid (cell (x, y) = 8x8 px at screen (8 + 8x, 16 + 8y), as region_map.c),
inside the Orchid frame (header band, recessed map well, tray with the location pill).

KNOWN (from the game data, src/data/region_map/region_map_sections.json + map.json connections):
  Tosa Port            MAPSEC_TOSA_PORT          cell (4, 11)
  South Tosa Reserve   MAPSEC_SOUTH_TOSA_RESERVE cell (4, 10)   Tosa Port <-> Reserve <-> Telok Town (N-S)
  Telok Town           MAPSEC_OLDALE_TOWN        cell (4, 9)
  Petalburg City       (still vanilla)           map.json: EAST of the Reserve; region grid: cell (1, 9) = WEST
INVENTED (flagged orange on the annotated sheet): the coastline / island shape, the central
highlands, Timah Town's position (the name is from TODO.md), the route from Telok Town to Timah,
the Tosa Rail line, Petalburg's distance east of the Reserve, the islets.

usage: tosa_map.py OUT_DIR
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from kit import *
import kit_ext as KX
import dex_ext as D
from gamefont import draw_text, text_width

W, H = 240, 160
GX, GY = 8, 16                        # grid origin (cell 0, 0)

# Hoenn region-map colours (graphics/pokenav/region_map/map.png)
SEA_A, SEA_B = (156, 213, 255), (164, 180, 255)
SEA_LANE = ((74, 156, 230), (41, 131, 230))
LAND = [(0, 115, 0), (57, 172, 8), (98, 213, 0), (172, 238, 49), (213, 255, 123)]
ROUTE = ((230, 164, 0), (238, 189, 57), (246, 213, 82))
CITY = ((148, 0, 0), (255, 57, 16), (255, 172, 16))
TOWN = ((32, 74, 197), (65, 106, 205))
WHITE_ = (255, 255, 255)
RAIL = ((98, 98, 98), (205, 205, 205))

ISLAND = [(1.5, 7), (3, 4.5), (6, 3.4), (9, 2.6), (13, 2.0), (17, 2.4), (21, 3.4), (24, 5), (26.2, 7.4),
          (25.4, 9.6), (22, 10.6), (18, 11.0), (14, 11.5), (10, 12.0), (6.4, 12.3), (5.2, 12.4),
          (3.6, 12.3), (2.0, 10.6)]
ISLETS = [((8.5, 13.6), 0.9), ((20.5, 12.6), 0.7), ((27.0, 5.6), 0.6), ((12.0, 13.2), 0.5)]
HILL = (11.0, 6.2, 3.2)                # central highlands (invented): cx, cy, radius in cells

KNOWN = [("Tosa Port", (4, 11), "town"), ("South Tosa Reserve", (4, 10), "route"),
         ("Telok Town", (4, 9), "town")]
INVENTED = [("Petalburg City (still vanilla)", (7, 10), "city"), ("Timah Town (TODO.md)", (11, 6), "town")]


def cell_px(cx, cy):
    return GX + cx * 8, GY + cy * 8


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def noise(x, y):
    return (math.sin(x * 0.9 + y * 0.4) + math.sin(x * 0.37 - y * 1.1) * 0.8 + math.sin((x + y) * 0.23) * 0.6) / 2.4


def land_mask():
    poly = [(GX + x * 8, GY + y * 8) for x, y in ISLAND]
    m = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            j = noise(x, y) * 3.0
            if inside(poly, x + j, y - j * 0.6):
                m[y][x] = True
            for (cx, cy), r in ISLETS:
                px, py = cell_px(cx, cy)
                if math.hypot((x - px) / 1.4, y - py) < r * 8 + noise(x * 2, y * 2) * 2:
                    m[y][x] = True
    return m


def dist_to_sea(m, x, y, lim=7):
    for d in range(1, lim + 1):
        for dy in range(-d, d + 1):
            for dx in (-d, d) if abs(dy) != d else range(-d, d + 1):
                X, Y = x + dx, y + dy
                if not (0 <= X < W and 0 <= Y < H) or not m[Y][X]:
                    return d
    return lim + 1


def draw_route(px, cells, horizontal):
    """Hoenn route band: 8px wide, dark edge, lighter centre."""
    for cx, cy in cells:
        x0, y0 = cell_px(cx, cy)
        for y in range(y0, y0 + 8):
            for x in range(x0, x0 + 8):
                k = (y - y0) if horizontal else (x - x0)
                px[x, y] = ROUTE[0] if k in (0, 7) else (ROUTE[2] if k in (3, 4) else ROUTE[1])


def town_pin(px, cx, cy):
    x0, y0 = cell_px(cx, cy)
    for y in range(8):
        for x in range(8):
            d = math.hypot(x - 3.5, y - 3.5)
            if d < 3.9:
                px[x0 + x, y0 + y] = TOWN[0] if d > 2.6 else TOWN[1]
    px[x0 + 2, y0 + 2] = WHITE_
    px[x0 + 3, y0 + 2] = WHITE_


def city_pill(px, cx, cy, w=2):
    x0, y0 = cell_px(cx, cy)
    for y in range(8):
        for x in range(8 * w):
            edge = x in (0, 8 * w - 1) or y in (0, 7)
            corner = (x in (0, 8 * w - 1)) and (y in (0, 7))
            if corner:
                continue
            px[x0 + x, y0 + y] = CITY[0] if edge else (CITY[2] if y in (1, 2) else CITY[1])
    px[x0 + 2, y0 + 2] = WHITE_


def render_map(mark_invented=False):
    im = Image.new("RGB", (W, H))
    px = im.load()
    m = land_mask()
    hx, hy, hr = HILL
    hcx, hcy = cell_px(hx, hy)
    for y in range(H):
        for x in range(W):
            if not m[y][x]:
                px[x, y] = SEA_A if (y // 2) % 2 == 0 else SEA_B
                continue
            d = dist_to_sea(m, x, y)
            c = LAND[0] if d <= 1 else (LAND[1] if d <= 4 else LAND[2])
            h = math.hypot(x - hcx, (y - hcy) * 1.3) / (hr * 8) + noise(x * 1.7, y * 1.7) * 0.15
            if d > 4 and h < 0.75:
                c = LAND[3]
            if d > 4 and h < 0.35:
                c = LAND[4]
            px[x, y] = c
    # sea lane: ferry from Tosa Port south (where the player arrives by boat)
    x0, y0 = cell_px(4, 12)
    for y in range(y0 + 2, y0 + 16):
        for x in range(x0 + 2, x0 + 6):
            if not m[y][x]:
                px[x, y] = SEA_LANE[(x - x0) in (2, 5)]
    # routes: known (the Reserve), then invented
    draw_route(px, [(4, 10)], False)
    draw_route(px, [(5, 10), (6, 10)], True)                      # Reserve -> Petalburg (distance invented)
    draw_route(px, [(4, 8), (4, 7), (4, 6)], False)                # Telok north (invented)
    draw_route(px, [(5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6)], True)   # -> Timah (invented)
    # Tosa Rail (invented): grey/white dashed track from Tosa Port east along the south, up to Timah
    rail = [(5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (12, 10), (12, 9), (12, 8), (12, 7)]
    for i, (cx, cy) in enumerate(rail):
        x0, y0 = cell_px(cx, cy)
        horiz = cy == 11
        for k in range(8):
            X, Y = (x0 + k, y0 + 3) if horiz else (x0 + 3, y0 + k)
            px[X, Y] = RAIL[0]
            px[X + (0 if horiz else 1), Y + (1 if horiz else 0)] = RAIL[1] if (k // 2) % 2 else RAIL[0]
    town_pin(px, 4, 11)
    town_pin(px, 4, 9)
    city_pill(px, 7, 10, 1)
    town_pin(px, 11, 6)
    return im


def render_screen(cursor=(4, 11), loc="Tosa Port", desc="Harbour town, ferry pier"):
    """The map inside the Orchid frame (Town Map / Fly map / dex AREA would share the art)."""
    pal = D.dex_palette("orchid")
    out = render_map().convert("RGBA")
    art = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    cv = Canvas(art)
    D.header_band(cv, 0, W - 1, round_left=False)
    # map well rim (inside left transparent): ink + accent band + recess bevel
    rounded_box(cv, 2, 17, 236, 118, 4, TRANSPARENT, INK, ACCENT_DARK, ACCENT_LIGHT)
    for y in range(17, 135):
        for x in range(0, 2):
            cv.set(x, y, ACCENT)
        for x in range(238, 240):
            cv.set(x, y, ACCENT)
    D.tray(cv, 136)
    rounded_box(cv, 6, 140, 104, 14, 4, PANEL, INK, WHITE, PANEL_SHADE)
    out.alpha_composite(KX.sheet_rgba(art, pal))
    txt = new_sheet(W, H, "orchid", spare_a=D.BALL_RED)
    tc = Canvas(txt)
    draw_text(tc, (W - text_width("TOSA")) // 2, 0, "TOSA", WHITE, ACCENT_DARK)
    draw_text(tc, 12, 139, loc, INK, PANEL_SHADE)
    draw_text(tc, 116, 139, desc, INK, PANEL_SHADE, font="narrow")
    out.alpha_composite(KX.sheet_rgba(txt, pal))
    # Gen 3 cursor (cursor_small.png frame 0) + player head
    cur = KX.sprite_rgba(KX.G("pokenav", "region_map", "cursor_small.png"), 0, 16,
                         pal=KX.load_jasc(KX.G("pokenav", "region_map", "cursor.pal")))
    x0, y0 = cell_px(*cursor)
    out.alpha_composite(cur, (x0 - 4, y0 - 4))
    head = KX.sprite_rgba(KX.G("pokenav", "region_map", "brendan_icon.png"))
    out.alpha_composite(head, (x0 - 4, y0 - 4))
    return out


def annotated(scale=4):
    im = KX.upscale(render_map().convert("RGB"), scale)
    d = ImageDraw.Draw(im, "RGBA")
    f = ImageFont.load_default(size=15)
    fb = ImageFont.load_default(size=18)
    for cx in range(29):           # faint cell grid
        X = (GX + cx * 8) * scale
        d.line([(X, GY * scale), (X, (GY + 15 * 8) * scale)], fill=(255, 255, 255, 40))
    for cy in range(16):
        Y = (GY + cy * 8) * scale
        d.line([(GX * scale, Y), ((GX + 28 * 8) * scale, Y)], fill=(255, 255, 255, 40))

    def label(cx, cy, text, col, dx=10, dy=-6):
        x, y = (GX + cx * 8 + 8) * scale + dx, (GY + cy * 8) * scale + dy
        d.rectangle([x - 3, y - 2, x + d.textlength(text, font=f) + 3, y + 18], fill=(0, 0, 0, 170))
        d.text((x, y), text, font=f, fill=col)
    KN, INV = (255, 255, 255), (255, 170, 60)
    label(4, 11, "Tosa Port  (4,11) MAPSEC_TOSA_PORT", KN, dy=22)
    label(4, 10, "South Tosa Reserve  (4,10)", KN, dx=12 + 2 * 8 * scale, dy=-14)
    label(4, 9, "Telok Town  (4,9) [MAPSEC_OLDALE_TOWN]", KN, dy=-22)
    label(7, 10, "Petalburg City? - east of Reserve per map.json;", INV, dx=190, dy=-4)
    label(7, 10, "region grid has it at (1,9) WEST - which is right?", INV, dx=190, dy=16)
    label(11, 6, "Timah Town? (TODO.md: Bukit Timah) - position invented", INV, dy=-6)
    label(4, 7, "route Telok -> Timah: invented", INV, dx=10, dy=-6)
    label(12, 9, "Tosa Rail line: invented", INV, dx=6, dy=0)
    label(4, 13, "ferry lane (intro: arrive by boat)", INV, dx=10, dy=22)
    label(16, 4, "coastline, highlands, islets: invented (Singapore-like island)", INV, dx=0, dy=0)
    d.text((GX * scale, (GY + 15 * 8) * scale + 6), "white = from game data    orange = invented, please correct", font=fb, fill=(255, 255, 255))
    return im


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    scr = render_screen()
    ann = annotated(4)
    sheet = Image.new("RGB", (W * 3 + 36 + ann.size[0], max(H * 3 + 24 + 5 * 22 + 12, ann.size[1] + 24)), (24, 24, 32))
    sheet.paste(KX.upscale(scr.convert("RGB"), 3), (12, 12))
    sheet.paste(ann, (W * 3 + 24, 12))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.load_default(size=17)
    notes = ["Tosa region map - LAYOUT SKETCH (please correct)",
             "Left: in-frame look (Orchid header, map well, tray with location pill).",
             "Right: 4x annotated, cell grid = the game's 28x15 region grid.",
             "Only 3 Tosa places exist in the data (all at x=4); the rest is a guess.",
             "Used by: Town Map item, Fly map, PokeNav map, dex AREA page."]
    for i, t in enumerate(notes):
        d.text((12, H * 3 + 24 + i * 22), t, font=f, fill=(230, 230, 240))
    sheet.save(os.path.join(out, "tosa_map_mock.png"))
    print("ok", sheet.size)
