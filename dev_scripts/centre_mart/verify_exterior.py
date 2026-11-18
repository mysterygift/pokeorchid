#!/usr/bin/env python3
"""Contact sheet of every Centre / Mart exterior, rendered from the repo's map data.

    python verify_exterior.py      # writes out/verify_exterior.png
"""
import os

from PIL import Image, ImageDraw

import inventory
import vanilla
from mock import OUT, sprite, PEOPLE, OBJ_PALS

CENTRE_DOOR, MART_DOOR = 0x059, 0x041


def main():
    L = inventory.layouts()
    shots = []
    for lid, e in L.items():
        if e["primary_tileset"] != "gTileset_General" or inventory.blocks(e) is None:
            continue
        g = inventory.blocks(e)
        found = [(x, y, v & 0x3FF) for y, row in enumerate(g) for x, v in enumerate(row)
                 if (v & 0x3FF) in (CENTRE_DOOR, MART_DOOR)]
        if not found:
            continue
        sc, grid, under, over = vanilla.render(lid)
        player = sprite(PEOPLE + "brendan/walking.png", OBJ_PALS + "brendan.pal", 1)
        for x, y, m in found:
            by = y - 2 if m == CENTRE_DOOR else y - 3
            stand_y = by + 3 if m == CENTRE_DOOR else by + 4
            im = under.copy()
            im.alpha_composite(player, (x * 16, stand_y * 16 - 16))
            im.alpha_composite(over)
            box = ((x - 4) * 16, (by - 2) * 16, (x + 5) * 16, (by + 6) * 16)
            crop = Image.new("RGBA", (144, 128), (0, 0, 0, 255))
            crop.paste(im.crop(box), (0, 0))
            walk = sum(1 for cx in range(-1, 3) if not (g[by + 3][x + cx] >> 10) & 3)
            shots.append((f"{lid[7:]} {'C' if m == CENTRE_DOOR else 'M'} ({x},{y})", crop))
    cols = 5
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 292, rows * 274), (24, 24, 32))
    dr = ImageDraw.Draw(sheet)
    for i, (name, crop) in enumerate(shots):
        ox, oy = (i % cols) * 292 + 2, (i // cols) * 274 + 2
        sheet.paste(crop.resize((288, 256), Image.NEAREST).convert("RGB"), (ox, oy))
        dr.text((ox + 2, oy + 258), name[:44], fill=(232, 232, 232))
    p = os.path.join(OUT, "verify_exterior.png")
    sheet.save(p)
    print(p, len(shots), "buildings")


if __name__ == "__main__":
    main()
