#!/usr/bin/env python3
"""The rotating Poke Mart signpost (OBJ_EVENT_GFX_MART_SIGN): a 16x32 overworld object,
four frames (face, three-quarter, edge, other three-quarter) on the shared npc_1 palette.

    python sign.py      # graphics/object_events/pics/misc/mart_sign.png + out/mart_sign_x6.gif
"""
import os

from PIL import Image

from common import HERE, ROOT

PAL_PATH = os.path.join(ROOT, "graphics", "object_events", "palettes", "npc_1.pal")
OUT = os.path.join(ROOT, "graphics", "object_events", "pics", "misc", "mart_sign.png")

# npc_1 indices
T, LB, MB, NV, WH, BK = 0, 8, 9, 10, 14, 15
KEY = {".": T, "l": LB, "m": MB, "n": NV, "w": WH}

FACE = [  # 15 x 11: a Poke Ball (white top, navy band, light-blue bottom) on the blue board
    "nnnnnnnnnnnnnnn",
    "nllllllllllllln",
    "nmmmmmwwwmmmmmn",
    "nmmmmwwwwwmmmmn",
    "nmmmwwwwwwwmmmn",
    "nmmmnnnwnnnmmmn",
    "nmmmlllllllmmmn",
    "nmmmmlllllmmmmn",
    "nmmmmmlllmmmmmn",
    "nmmmmmmmmmmmmmn",
    "nnnnnnnnnnnnnnn",
]
THREE_Q = [  # 10 wide: 8 px of face + the board's 2 px edge
    "nnnnnnnnnn",
    "nllllllnll",
    "nmmwwwmnll",
    "nmwwwwwnlm",
    "nmnnwnnnmm",
    "nmllllln m".replace(" ", "m"),
    "nmmlllmnmm",
    "nmmmmmmnmm",
    "nmmmmmmnmm",
    "nmmmmmmnmm",
    "nnnnnnnnnn",
]
EDGE = ["nn", "ln", "ln", "ln", "mn", "mn", "mn", "mn", "mn", "mn", "nn"]


def frame(head, x0, flip=False):
    px = [[T] * 16 for _ in range(32)]
    rows = [r[::-1] if flip else r for r in head]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            px[2 + j][x0 + i] = KEY[ch]
    # pole: two px, white highlight + light blue, dark outline at the foot
    for y in range(13, 30):
        px[y][7], px[y][8] = WH, LB
    px[30][6:10] = [NV, MB, MB, NV]
    px[31][6:10] = [T, NV, NV, T]
    return px


def main():
    frames = [frame(FACE, 0), frame(THREE_Q, 3), frame(EDGE, 7), frame(THREE_Q, 3, flip=True)]
    pal = [tuple(int(v) for v in l.split()) for l in open(PAL_PATH).read().split("\n")[3:19]]
    im = Image.new("P", (64, 32), 0)
    im.putpalette([v for c in pal for v in c])
    for f, px in enumerate(frames):
        for y in range(32):
            for x in range(16):
                im.putpixel((f * 16 + x, y), px[y][x])
    im.save(OUT, bits=4, optimize=False)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    gif = []
    for f in range(4):
        g = Image.new("RGBA", (16, 32), (120, 184, 96, 255))
        g.alpha_composite(Image.frombytes("RGBA", (16, 32), bytes(
                              b for y in range(32) for x in range(16)
                              for b in ((*pal[frames[f][y][x]], 255) if frames[f][y][x] else (0, 0, 0, 0)))))
        gif.append(g.resize((96, 192), Image.NEAREST))
    gif[0].save(os.path.join(HERE, "out", "mart_sign_x6.gif"), save_all=True, append_images=gif[1:],
                duration=[400, 120, 120, 120], loop=0)
    im.resize((384, 192), Image.NEAREST).save(os.path.join(HERE, "out", "mart_sign_x6.png"))
    print(OUT)


if __name__ == "__main__":
    main()
