"""Render an installed area kit from the tileset files on disk (what the game will load):
the picker block and two sample crossings (barriers lowered / raised)."""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsio import Pair  # noqa: E402


def render(sec, meta_base, n_rows, out, scale=3):
    os.makedirs(out, exist_ok=True)
    pair = Pair("primary/general", "secondary/" + sec)
    base = 0x200 + meta_base
    sheet = Image.new("RGB", (8 * 17 + 1, n_rows * 17 + 1), (255, 0, 255))
    for r in range(n_rows):
        for c in range(8):
            cell = Image.new("RGB", (16, 16), pair.pal(0)[0])
            pair.render_meta(cell, base + r * 8 + c, 0, 0)
            sheet.paste(cell, (1 + c * 17, 1 + r * 17))
    sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST).save(
        os.path.join(out, "%s_kit_metatiles.png" % sec))

    m = lambda r, c: base + r * 8 + c  # noqa: E731
    rail = {"H": m(0, 0), "HXs": m(1, 2)}
    sign_top, sign_bot = m(4, 0), m(5, 0)
    up = {"E": (m(4, 2), m(5, 2), m(6, 2)), "W": (m(4, 5), m(5, 5), m(6, 5))}
    down_e, down_w = m(7, 0), m(7, 7)
    arm_e = {g: [m(7 + gi, 1 + i) for i in range(3)] for gi, g in enumerate(("grass", "l", "m", "r"))}
    arm_w = {g: [m(7 + gi, 6 - i) for i in range(3)] for gi, g in enumerate(("grass", "l", "m", "r"))}

    def scene(lowered):
        W, H = 13, 10
        grid = [[0x001] * W for _ in range(H)]
        for y in range(H):
            grid[y][5], grid[y][6], grid[y][7] = 0x120, 0x121, 0x122
        for x in range(W):
            grid[4][x] = rail["HXs"] if 5 <= x <= 7 else rail["H"]
        grid[0][9], grid[1][9] = sign_top, sign_bot
        grid[7][3], grid[8][3] = sign_top, sign_bot
        # north barrier: cabinet west of the road, arm runs east over the path
        if lowered:
            grid[2][4] = down_e
            grid[2][5], grid[2][6], grid[2][7] = arm_e["l"][0], arm_e["m"][1], arm_e["r"][2]
            grid[7][8] = down_w
            grid[7][7], grid[7][6], grid[7][5] = arm_w["r"][0], arm_w["m"][1], arm_w["l"][2]
        else:
            t, mid, cab = up["E"]
            grid[0][4], grid[1][4], grid[2][4] = t, mid, cab
            t, mid, cab = up["W"]
            grid[5][8], grid[6][8], grid[7][8] = t, mid, cab
        img = Image.new("RGB", (W * 16, H * 16))
        for y in range(H):
            for x in range(W):
                pair.render_meta(img, grid[y][x], x * 16, y * 16)
        return img

    a, b = scene(True), scene(False)
    both = Image.new("RGB", (a.width * 2 + 8, a.height), (30, 30, 30))
    both.paste(a, (0, 0)); both.paste(b, (a.width + 8, 0))
    both.resize((both.width * scale, both.height * scale), Image.NEAREST).save(
        os.path.join(out, "%s_kit_sample.png" % sec))
