#!/usr/bin/env python3
"""The rotating Poke Mart signpost (OBJ_EVENT_GFX_MART_SIGN): a 16x32 overworld object on the
shared npc_1 palette.

The board is a small slab (14 x 10 x 4 px) turning on its pole, drawn in the overworld's 3/4
overhead projection so its top face always shows (widest when the board is edge-on). Eight frames
cover half a turn; the board and the Poke Ball emblem are symmetric, so the other half repeats.

    python sign.py      # graphics/object_events/pics/misc/mart_sign.png + out/mart_sign_x6.png/.gif
"""
import math
import os

from PIL import Image

from common import HERE, ROOT

PAL_PATH = os.path.join(ROOT, "graphics", "object_events", "palettes", "npc_1.pal")
OUT = os.path.join(ROOT, "graphics", "object_events", "pics", "misc", "mart_sign.png")

T_, LB, MB, NV, WH = 0, 8, 9, 10, 14            # npc_1: transparent, light / mid blue, navy, white
KEY = {"l": LB, "m": MB, "n": NV, "w": WH}

W, H, D = 14, 10, 4          # board width, height, thickness (px)
K = 0.8                      # depth -> screen-y factor of the overhead view
CX = 8.0                     # pole axis (between sprite columns 7 and 8)
BOARD_BOTTOM = 15.5          # screen y of the board's bottom edge at the pole
FRAMES = 8                   # half a turn

FACE = [                     # front / back face texture, W x H, top row first
    "mmmmmmmmmmmmmm",
    "mmmmmmmmmmmmmm",
    "mmmmmwwwwmmmmm",
    "mmmmwwwwwwmmmm",
    "mmmnnnwwnnnmmm",
    "mmmmllnnllmmmm",
    "mmmmmllllmmmmm",
    "mmmmmmmmmmmmmm",
    "mmmmmmmmmmmmmm",
    "mmmmmmmmmmmmmm",
]


def project(x, y, z):
    """board-space (x right, y up, z toward the viewer) -> screen (sx, sy)"""
    return CX + x, BOARD_BOTTOM - y + z * K


def texture(a, b):
    return KEY[FACE[min(int(b * H), H - 1)][min(int(a * W), W - 1)]]


def frame(theta):
    c, s = math.cos(theta), math.sin(theta)

    def world(u, t, y):          # u along the width, t through the thickness
        return u * c + t * s, y, -u * s + t * c

    faces = []                   # (origin, edge1, edge2, shader(a, b)) in screen space

    def face(p0, p1, p2, shade):
        a0, a1, a2 = (project(*world(*p)) for p in (p0, p1, p2))
        faces.append((a0, (a1[0] - a0[0], a1[1] - a0[1]), (a2[0] - a0[0], a2[1] - a0[1]), shade))

    hw, hd = W / 2, D / 2
    face((-hw, -hd, H), (hw, -hd, H), (-hw, hd, H), lambda a, b: WH)            # top: always seen
    if c >= 0:                                                                 # front or back face
        face((-hw, hd, H), (hw, hd, H), (-hw, hd, 0), texture)
    else:
        face((hw, -hd, H), (-hw, -hd, H), (hw, -hd, 0), texture)
    if s > 0.01:                                                               # the end facing us
        face((-hw, -hd, H), (-hw, hd, H), (-hw, -hd, 0), lambda a, b: LB)
    elif s < -0.01:
        face((hw, hd, H), (hw, -hd, H), (hw, hd, 0), lambda a, b: LB)

    px = [[T_] * 16 for _ in range(32)]
    owner = [[None] * 16 for _ in range(32)]
    for fi, (o, e1, e2, shade) in enumerate(faces):
        det = e1[0] * e2[1] - e1[1] * e2[0]
        if abs(det) < 1e-6:
            continue
        for y in range(32):
            for x in range(16):
                dx, dy = x + 0.5 - o[0], y + 0.5 - o[1]
                a = (dx * e2[1] - dy * e2[0]) / det
                b = (e1[0] * dy - e1[1] * dx) / det
                if -1e-6 <= a <= 1 + 1e-6 and -1e-6 <= b <= 1 + 1e-6:
                    px[y][x] = shade(min(max(a, 0), 0.999), min(max(b, 0), 0.999))
                    owner[y][x] = fi
    # navy silhouette outline, and a navy seam under the top face
    out = [row[:] for row in px]
    for y in range(32):
        for x in range(16):
            if px[y][x] == T_:
                continue
            edge = any(not (0 <= y + dy < 32 and 0 <= x + dx < 16) or px[y + dy][x + dx] == T_
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            seam = owner[y][x] != 0 and y > 0 and owner[y - 1][x] == 0
            if edge or seam:
                out[y][x] = NV
    # pole under the board: white highlight + light blue, navy foot
    top = max(y for y in range(32) for x in (7, 8) if out[y][x] != T_) + 1
    for y in range(top, 30):
        out[y][7], out[y][8] = WH, LB
    out[30][6:10] = [NV, MB, MB, NV]
    out[31][6:10] = [T_, NV, NV, T_]
    return out


def main():
    frames = [frame(math.pi * k / FRAMES) for k in range(FRAMES)]
    pal = [tuple(int(v) for v in l.split()) for l in open(PAL_PATH).read().split("\n")[3:19]]
    im = Image.new("P", (16 * FRAMES, 32), 0)
    im.putpalette([v for c in pal for v in c])
    for f, px in enumerate(frames):
        for y in range(32):
            for x in range(16):
                im.putpixel((f * 16 + x, y), px[y][x])
    im.save(OUT, bits=4, optimize=False)

    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    shots = []
    for px in frames:
        g = Image.new("RGBA", (16, 32), (120, 184, 96, 255))
        for y in range(32):
            for x in range(16):
                if px[y][x]:
                    g.putpixel((x, y), pal[px[y][x]] + (255,))
        shots.append(g.resize((96, 192), Image.NEAREST))
    sheet = Image.new("RGBA", (100 * FRAMES, 192), (40, 40, 40, 255))
    for i, s in enumerate(shots):
        sheet.paste(s, (i * 100, 0))
    sheet.save(os.path.join(HERE, "out", "mart_sign_x6.png"))
    seq = shots + shots
    shots[0].save(os.path.join(HERE, "out", "mart_sign_x6.gif"), save_all=True, append_images=seq[1:],
                  duration=[600] + [110] * (len(seq) - 1), loop=0)
    print(OUT)


if __name__ == "__main__":
    main()
