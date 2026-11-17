"""
Tosa region map v3 mock: the user's art rotated 180 deg (export_region_map.py does the ROM art),
square numbers kept, #4 = Tosa Port, #10 = Telok Town, South Tosa Reserve = the route between.
Views: Town Map, Fly map (cursor on Tosa Port), dex AREA (Reserve glowing).
usage: tosa_map_v3.py OUT_DIR
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import kit_ext as KX
import mock_dex as M
import tosa_map_v2 as V2
import export_region_map as X

W, H, GX, GY = 240, 160, 8, 16


def main(out_dir):
    sq = X.squares()
    cells = [(n, c[0], c[1]) for n, c in sorted(sq.items())]
    reserve = X.route_cells_between(sq[X.TOSA_PORT], sq[X.TELOK])
    art = X.map_art()
    port = sq[X.TOSA_PORT]
    names = {n: X.place_name(n) for n in sq}
    names[X.TOSA_PORT], names[X.TELOK] = "Tosa Port", "Telok Town"

    town = art.convert("RGBA")
    V2.frame(town, "TOSA", "Tosa Port", "")
    V2.cursor(town, port)
    fly = art.convert("RGBA")
    V2.frame(fly, "FLY", "Tosa Port", "Fly here?")
    ico = KX.sprite_rgba(KX.G("pokenav", "region_map", "fly_target_icons.png")).crop((0, 0, 8, 8))
    for n in (X.TOSA_PORT, X.TELOK):
        cx, cy = sq[n]
        fly.alpha_composite(ico, (GX + cx * 8, GY + cy * 8))
    V2.cursor(fly, port, head=False)
    area, off = V2.area_view(art, reserve)
    x0, y0, x1, y1 = M.AREA_WELL

    S = 3
    f = ImageFont.load_default(size=16)
    fb = ImageFont.load_default(size=18)
    views = [("Town Map", town, (0, 0), None), ("Fly map", fly, (0, 0), None),
             ("Dex AREA tab: South Tosa Reserve glowing", area, off, (x0 + 2, y0 + 2, x1 - 1, y1 - 1))]
    rows = [
        "Rotated 180 deg (user: 'I meant a 180 rotation'). Left strip: original -> rotated. Numbers are the user's, kept.",
        "#4 (7,12) = Tosa Port   #10 (7,8) = Telok Town   South Tosa Reserve = route (7,9)-(7,11)",
        "Red block = city/town marker; red dot on yellow = landmark. 249/256 tiles, 17 colours.",
    ]
    sheet = Image.new("RGB", (3 * (W * S + 16) + 16, 34 + H * S + 16 + 260 + len(rows) * 22 + 160), (24, 24, 32))
    d = ImageDraw.Draw(sheet)
    for i, (cap, im, o, clip) in enumerate(views):
        big = KX.upscale(im.convert("RGB"), S)
        V2.number(big, S, cells, o, f, clip)
        x = 16 + i * (W * S + 16)
        sheet.paste(big, (x, 34))
        d.text((x, 8), cap, font=fb, fill=(230, 230, 240))
    y = 34 + H * S + 16
    orig = Image.open(os.path.join(X.REF, "tosa_towns.png")).convert("RGB")
    rot = orig.rotate(180)
    sheet.paste(orig.resize((360, 240)), (16, y))
    d.text((390, y + 110), "->  180 deg  ->", font=fb, fill=(230, 230, 240))
    sheet.paste(rot.resize((360, 240)), (560, y))
    tx = 950
    d.text((tx, y), "Places (number, cell, name):", font=f, fill=(230, 230, 240))
    for k, (n, cx, cy) in enumerate(cells):
        col, row = k // 10, k % 10
        d.text((tx + col * 330, y + 24 + row * 22), "#%d (%d,%d) %s" % (n, cx, cy, names[n]), font=f, fill=(230, 230, 240))
    y += 260
    for i, t in enumerate(rows):
        d.text((16, y + i * 22), t, font=f, fill=(230, 230, 240))
    sheet = sheet.crop((0, 0, sheet.size[0], y + len(rows) * 22 + 12))
    sheet.save(os.path.join(out_dir, "tosa_map_mock_v3.png"))
    print("ok", sheet.size)


if __name__ == "__main__":
    main(sys.argv[1])
