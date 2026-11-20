#!/usr/bin/env python3
"""Contact sheet of every 5x5 Mart from the repo's map data, with the real layer split: a player in
front of the door (draws over the facade), one on the back row (hidden by the roof), the signposts.

    python verify.py         # out/verify.png
"""
import json
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "centre_mart_v2"))
sys.path.insert(0, os.path.join(HERE, "..", "centre_mart"))
from common import layouts, maps, read_grid  # noqa: E402
from verify import sprite, PLAYER, PLAYER_PAL, SIGN, SIGN_PAL  # noqa: E402
import vanilla  # noqa: E402


def main():
    inst = json.load(open(os.path.join(HERE, "installed.json")))
    L, M = layouts(), maps()
    down, up = sprite(PLAYER, PLAYER_PAL, 0), sprite(PLAYER, PLAYER_PAL, 1)
    sign = sprite(SIGN, SIGN_PAL, 0)
    shots = []
    for m in inst["marts"]:
        lid = m["layout"]
        nx, ny = m["new"]
        sc, grid, under, over = vanilla.render(lid, pad=0)
        g = read_grid(L[lid])
        im = under.copy()
        sprites = [(ny + 5, nx + 2, up)]
        back = [x for x in range(nx, nx + 5) if not ((g[ny][x] >> 10) & 3)]
        if back:
            sprites.append((ny, back[len(back) // 2], down))
        for _, (p, js) in M.items():
            if js["layout"] == lid:
                for o in js.get("object_events") or []:
                    if o.get("graphics_id") == "OBJ_EVENT_GFX_MART_SIGN":
                        sprites.append((o["y"], o["x"], sign))
        for ty, tx, s in sorted(sprites):
            im.alpha_composite(s, (tx * 16, ty * 16 - 16))
        im.alpha_composite(over)
        box = ((nx - 2) * 16, (ny - 2) * 16, (nx + 7) * 16, (ny + 7) * 16)
        crop = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 255))
        crop.paste(im.crop(box), (0, 0))
        shots.append((f"{lid[7:]} {m['side']}{' FORCED' if m['forced'] else ''}", crop))
    cols, cw, ch = 5, 9 * 16 * 2, 9 * 16 * 2 + 14
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 4), rows * (ch + 4)), (24, 24, 32))
    dr = ImageDraw.Draw(sheet)
    for i, (tag, crop) in enumerate(shots):
        ox, oy = (i % cols) * (cw + 4), (i // cols) * (ch + 4)
        sheet.paste(crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST).convert("RGB"), (ox, oy))
        dr.text((ox + 2, oy + ch - 13), tag[:44], fill=(232, 232, 232))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    path = os.path.join(HERE, "out", "verify.png")
    sheet.save(path)
    print(path, len(shots))


if __name__ == "__main__":
    main()
