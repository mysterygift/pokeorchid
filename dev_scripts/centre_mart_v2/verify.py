#!/usr/bin/env python3
"""Contact sheet of every new Centre / Mart, rendered from the repo's map data with the real
layer split: a player in front of the door (should draw over the facade), a player on the back
row (should be hidden behind the roof), and the Mart signpost.

    python verify.py         # out/verify.png
"""
import json
import os
import sys

from PIL import Image, ImageDraw

from common import HERE, ROOT, layouts, read_grid

sys.path.insert(0, os.path.join(HERE, "..", "centre_mart"))
import vanilla  # noqa: E402

PLAYER = os.path.join(ROOT, "graphics/object_events/pics/people/brendan/walking.png")
PLAYER_PAL = os.path.join(ROOT, "graphics/object_events/palettes/brendan.pal")
SIGN = os.path.join(ROOT, "graphics/object_events/pics/misc/mart_sign.png")
SIGN_PAL = os.path.join(ROOT, "graphics/object_events/palettes/npc_1.pal")


def sprite(path, pal_path, frame):
    im = Image.open(path)
    pal = vanilla.load_jasc(pal_path)
    out = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
    px, o = im.load(), out.load()
    for y in range(32):
        for x in range(16):
            c = px[frame * 16 + x, y] & 15
            if c:
                o[x, y] = pal[c] + (255,)
    return out


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    L = layouts()
    down, up = sprite(PLAYER, PLAYER_PAL, 0), sprite(PLAYER, PLAYER_PAL, 1)
    sign = sprite(SIGN, SIGN_PAL, 0)
    cache, shots = {}, []
    for p in plan:
        lid = p["layout"]
        if lid not in cache:
            cache[lid] = vanilla.render(lid, pad=0)
        sc, grid, under, over = cache[lid]
        g = read_grid(L[lid])
        nx, ny, w, h = p["new"]
        im = under.copy()
        sprites = []
        door_x = nx + 2 if p["kind"] == "centre" else nx + 1
        sprites.append((ny + h, door_x, up))
        # walkable back row?
        back = [x for x in range(nx, nx + w) if not ((g[ny][x] >> 10) & 3)]
        if back:
            sprites.append((ny, back[len(back) // 2], down))
        for q in plan:
            if q["layout"] == lid and q.get("sign"):
                sprites.append((q["sign"][1], q["sign"][0], sign))
        for ty, tx, s in sorted(sprites):
            im.alpha_composite(s, (tx * 16, ty * 16 - 16))
        im.alpha_composite(over)
        box = ((nx - 2) * 16, (ny - 2) * 16, (nx + w + 2) * 16, (ny + h + 2) * 16)
        crop = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 255))
        crop.paste(im.crop(box), (0, 0))
        tag = f"{lid[7:]} {'C' if p['kind'] == 'centre' else 'M'}{' FORCED' if p.get('forced') else ''}"
        shots.append((tag, crop))
    cols, cw, ch = 6, 9 * 16 * 2, 9 * 16 * 2 + 14
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 4), rows * (ch + 4)), (24, 24, 32))
    dr = ImageDraw.Draw(sheet)
    for i, (tag, crop) in enumerate(shots):
        ox, oy = (i % cols) * (cw + 4), (i // cols) * (ch + 4)
        c = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST).convert("RGB")
        sheet.paste(c.crop((0, 0, cw, ch - 14)), (ox, oy))
        dr.text((ox + 2, oy + ch - 13), tag[:40], fill=(232, 232, 232))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    path = os.path.join(HERE, "out", "verify.png")
    sheet.save(path)
    print(path, len(shots))


if __name__ == "__main__":
    main()
