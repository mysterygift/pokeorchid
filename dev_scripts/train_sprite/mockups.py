"""
Mockups for the Tosa Rail train sprite review.

For each option in train_art.OPTIONS writes to out/:
    scene_<k>_shut_1x/3x.png   240x160 platform scene, door shut, player facing the door
    scene_<k>_open_1x/3x.png   door open, player half a step into the doorway
    sheet_<k>_3x.png           the four 64x64 pieces in engine order (0 rear, 1 shut, 2 loco, 3 open)
    board_<k>.png              one review board (scenes + pieces + door comparison)
    board_<k>.gif              arrive -> door opens -> player boards -> leaves (2x)
and compare_1x3.png (all options side by side at 1x and 3x).

Geometry matches src/train_travel.c: track row = one 16 px tile, piece bottoms on its bottom edge
(TRAIN_BOTTOM_DROP 0), door centre on the door tile centre (TRAIN_DOOR_X 88, width 16).
usage: python mockups.py
"""
import os
from PIL import Image, ImageDraw

import train_art as T

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
W, H = 240, 160
TRACK_Y = 64                 # track tile row (top); platform starts at 80
DOOR_TILE_X = 112            # door tile column (x of its left edge)
TRAIN_X = DOOR_TILE_X + 8 - (64 + 24) - 8   # door centre on tile centre -> 24
TRAIN_Y = TRACK_Y + 16 - 64  # piece bottoms on the track tile's bottom edge


def brendan(frame):
    im = Image.open(os.path.join(ROOT, "graphics/object_events/pics/people/brendan/walking.png"))
    key = tuple(im.getpalette()[:3])
    im = im.convert("RGBA").crop((frame * 16, 0, frame * 16 + 16, 32))
    px = im.load()
    for y in range(32):
        for x in range(16):
            if px[x, y][:3] == key:
                px[x, y] = (0, 0, 0, 0)
    return im


def background():
    """Plain Gen 3-ish station: back wall, track bed with one track row, platform."""
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    # back wall
    d.rectangle((0, 0, W, 27), fill=(88, 104, 128))
    for x in range(0, W, 32):
        d.rectangle((x + 4, 6, x + 27, 19), fill=(120, 144, 168))
        d.rectangle((x + 4, 6, x + 27, 7), fill=(160, 184, 200))
    d.rectangle((0, 24, W, 27), fill=(56, 64, 88))
    # far platform
    d.rectangle((0, 28, W, 43), fill=(208, 200, 184))
    d.rectangle((0, 28, W, 29), fill=(232, 224, 208))
    for x in range(0, W, 16):
        d.line((x, 30, x, 43), fill=(184, 176, 160))
    d.rectangle((0, 44, W, 47), fill=(152, 144, 128))
    # track bed rows 48..79
    d.rectangle((0, 48, W, 79), fill=(120, 104, 96))
    for x in range(0, W, 8):
        d.rectangle((x + 1, 50, x + 4, 61), fill=(144, 128, 112))   # sleepers (far track)
        d.rectangle((x + 1, 66, x + 4, 77), fill=(144, 128, 112))   # sleepers (our track)
    for y in (52, 59, 68, 75):                                      # rails
        d.rectangle((0, y, W, y + 1), fill=(176, 184, 200))
        d.rectangle((0, y + 2, W, y + 2), fill=(72, 72, 88))
    # near platform from row 80
    d.rectangle((0, 80, W, H), fill=(216, 208, 192))
    d.rectangle((0, 80, W, 81), fill=(240, 232, 216))
    d.rectangle((0, 84, W, 87), fill=(232, 192, 72))                 # tactile line
    for x in range(1, W, 4):
        d.point((x, 85), fill=(200, 152, 48))
    for x in range(0, W, 16):
        d.line((x, 88, x, H), fill=(192, 184, 168))
    for y in range(96, H, 16):
        d.line((0, y, W, y), fill=(192, 184, 168))
    return im


def scene(k, door_open, player_dy=0, player=True, train_dx=0, show_player_frame=1):
    im = background()
    im.alpha_composite(T.strip(k, door_open), (TRAIN_X + train_dx, TRAIN_Y))
    if player:
        im.alpha_composite(brendan(show_player_frame), (DOOR_TILE_X, TRACK_Y + 16 - 32 + 16 + player_dy))
    return im


def x3(im, s=3):
    return im.resize((im.width * s, im.height * s), Image.NEAREST)


def label(im, text, xy, fill=(40, 40, 56)):
    ImageDraw.Draw(im).text(xy, text, fill=fill)


def sheet_img(k):
    sh = T.sheet(k).convert("RGBA")
    return sh


def board(k):
    opt = T.OPTIONS[k]
    shut = scene(k, False)
    opn = scene(k, True, player_dy=-8)
    pieces = Image.new("RGBA", (64 * 4 + 3 * 8, 64), (0, 0, 0, 0))
    raw = T.sheet(k).convert("RGBA")
    for i in range(4):
        pieces.paste(raw.crop((0, i * 64, 64, i * 64 + 64)), (i * 72, 0))
    # door comparison crop at 4x
    door_cmp = Image.new("RGBA", (2 * 48 + 8, 64), (255, 255, 255, 255))
    st_s, st_o = T.strip(k, False), T.strip(k, True)
    door_cmp.alpha_composite(st_s.crop((64 + 8, 0, 64 + 56, 64)), (0, 0))
    door_cmp.alpha_composite(st_o.crop((64 + 8, 0, 64 + 56, 64)), (56, 0))

    pad = 16
    bw = 720 + 720 + pad * 3
    bh = 40 + 480 + pad + 24 + 64 * 3 + pad + 24
    b = Image.new("RGBA", (bw, bh), (236, 236, 240, 255))
    label(b, f"Option {k} - {opt['name']}   (left: door shut, right: door open + boarding; 3x)", (pad, 14))
    b.alpha_composite(x3(shut), (pad, 40))
    b.alpha_composite(x3(opn), (pad * 2 + 720, 40))
    y = 40 + 480 + pad
    label(b, "Sheet pieces 0 rear | 1 door shut | 2 loco | 3 door open (3x)", (pad, y))
    b.alpha_composite(x3(pieces), (pad, y + 16))
    label(b, "Door shut / open (3x)", (pad * 2 + 870, y))
    b.alpha_composite(x3(door_cmp), (pad * 2 + 870, y + 16))
    label(b, "1x", (pad * 2 + 870 + 330, y))
    b.alpha_composite(shut, (pad * 2 + 870 + 330, y + 16))
    return b


def ease_out(a, z, t, n):
    r = n - t
    return z - (z - a) * r * r // (n * n)


def gif(k):
    frames, durs = [], []
    start = -(TRAIN_X + 192 + 8)
    for t in range(0, 97, 4):                       # arrive (ease out)
        frames.append(scene(k, False, train_dx=ease_out(start, 0, t, 96))); durs.append(66)
    frames.append(scene(k, False)); durs.append(500)
    frames.append(scene(k, True)); durs.append(400)
    for dy in (-4, -8, -12, -16):                   # walk north into the door
        frames.append(scene(k, True, player_dy=dy)); durs.append(120)
    frames.append(scene(k, True, player=False)); durs.append(300)
    frames.append(scene(k, False, player=False)); durs.append(500)
    end = W + 8 - TRAIN_X
    for t in range(0, 81, 4):                       # depart (ease in)
        frames.append(scene(k, False, player=False, train_dx=end * t * t // (80 * 80))); durs.append(66)
    frames.append(background()); durs.append(800)
    big = [x3(f, 2).convert("RGB") for f in frames]
    big[0].save(os.path.join(OUT, f"board_{k}.gif"), save_all=True, append_images=big[1:],
                duration=durs, loop=0)


def main():
    os.makedirs(OUT, exist_ok=True)
    cmp_rows = []
    for k in T.OPTIONS:
        for nm, im in (("shut", scene(k, False)), ("open", scene(k, True, player_dy=-8))):
            im.save(os.path.join(OUT, f"scene_{k}_{nm}_1x.png"))
            x3(im).save(os.path.join(OUT, f"scene_{k}_{nm}_3x.png"))
        x3(T.sheet(k).convert("RGBA")).save(os.path.join(OUT, f"sheet_{k}_3x.png"))
        board(k).save(os.path.join(OUT, f"board_{k}.png"))
        gif(k)
        cmp_rows.append(scene(k, False))
    c = Image.new("RGBA", (W * 3 + 32, H + 24 + 64 * 9 + 48), (236, 236, 240, 255))
    for i, (k, im) in enumerate(zip(T.OPTIONS, cmp_rows)):
        c.alpha_composite(im, (8 + i * (W + 8), 20))
        label(c, f"{k} - {T.OPTIONS[k]['name']} (1x)", (8 + i * (W + 8), 4))
        st = T.strip(k)
        c.alpha_composite(x3(st), (8, H + 32 + i * (64 * 3 + 8)))
    c.save(os.path.join(OUT, "compare_1x3.png"))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
