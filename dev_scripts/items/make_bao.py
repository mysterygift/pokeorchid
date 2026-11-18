"""Steamed bao icon: one bun on a square of baking paper set corner-on to the camera, the near
corner folded up against the bun. 3/4 view like the kopi / kaya toast icons; uses the existing
steamed_bao.pal. usage: make_bao.py REPO OUTDIR  (then copy OUTDIR/steamed_bao.png to graphics/items/icons)"""
import os
import sys
from PIL import Image, ImageDraw

repo, out = sys.argv[1], sys.argv[2]
pal = [tuple(int(v) for v in l.split()) for l in
       open(os.path.join(repo, "graphics/items/icon_palettes/steamed_bao.pal")).read().split("\n")[3:19]]
OUT, WHITE, CREAM, BEIGE, TAN, BROWN, DARK, STEAM = 1, 2, 3, 4, 5, 6, 7, 8
W = 24

# bun: the existing pleated dome (rows 5..14 of the old icon), extended into a rounded base
BUN = [
    ".........111111.........",
    ".......1122222211.......",
    "......122232232221......",
    ".....12222311322221.....",
    "....1222231331322221....",
    "....1222322112232221....",
    "...122223222222322221...",
    "...122222222222222231...",
    "...122222222222222331...",
    "...132222222222223341...",
    "...133222222222233341...",
    "....1332222222233341....",
    ".....11333333333411.....",
    ".......11111111111......",
]
BUN_Y = 6
STEAM_ROWS = {2: "..........8...8.........", 3: ".........8...8..........", 4: "..........8...8........."}

im = Image.new("P", (W, W), 0)
im.putpalette([c for rgb in pal for c in rgb] + [0] * (768 - 48))
px = im.load()
d = ImageDraw.Draw(im)

# 1) paper square, corner-on: side corners stick out past the bun, near corner points at the camera
Lc, Bc, Rc, Fc = (0, 17), (12, 13), (23, 17), (12, 23)
d.polygon([Lc, Bc, Rc, Fc], fill=BEIGE, outline=OUT)
for y in range(W):
    for x in range(W):
        if px[x, y] == BEIGE and x < 12:
            px[x, y] = CREAM          # lit left half of the paper

# 2) bun on top
for r, row in enumerate(BUN):
    for x, ch in enumerate(row):
        if ch != ".":
            px[x, BUN_Y + r] = int(ch, 16)
for y, row in STEAM_ROWS.items():
    for x, ch in enumerate(row):
        if ch != ".":
            px[x, y] = int(ch, 16)

# 3) soft shadow on the paper right under the bun
for x in range(7, 18):
    y = BUN_Y + len(BUN)
    if px[x, y] in (CREAM, BEIGE):
        px[x, y] = TAN
for x in (6, 17):
    y = BUN_Y + len(BUN) - 1
    if px[x, y] in (CREAM, BEIGE):
        px[x, y] = TAN

# 4) roundness (Gen 3 style): white top-left, cream bottom-right, a checker dither between them
#    along the dome's OUTER outline only (the pleats are left alone). Variant B also breaks up the
#    lit upper-left outline into an ink / beige checker instead of solid ink.
VARIANT = os.environ.get("BAO_VARIANT", "A")   # A chosen by the user (shading only)
dome = range(BUN_Y, BUN_Y + len(BUN) - 3)
outer = set()
for y in range(W):
    for x in range(W):
        if px[x, y] == OUT and any(not (0 <= x + dx < W and 0 <= y + dy < W) or px[x + dx, y + dy] in (0, STEAM)
                                   and (y + dy) < BUN_Y + 9
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            outer.add((x, y))
def dist_outer(x, y):
    best = 9
    for (ox, oy) in outer:
        dd = abs(ox - x) + abs(oy - y)
        if dd < best:
            best = dd
    return best
cx, cy = 11.5, BUN_Y + 6
for y in dome:
    for x in range(W):
        if px[x, y] != WHITE:
            continue
        dd, side = dist_outer(x, y), (x - cx) + (y - cy)
        if dd == 1 and (side > -2 or (x + y) % 2 == 0):
            px[x, y] = CREAM
        elif dd == 2 and side > 3 and (x + y) % 2 == 0:
            px[x, y] = CREAM
if VARIANT == "B":
    for (x, y) in outer:
        if y < cy and x < cx + 3 and (x + y) % 2 == 1:
            px[x, y] = BEIGE

os.makedirs(out, exist_ok=True)
im.save(os.path.join(out, "steamed_bao.png"), transparency=0)
rgb = Image.new("RGB", im.size)
for y in range(W):
    for x in range(W):
        rgb.putpixel((x, y), (232, 232, 224) if px[x, y] == 0 else pal[px[x, y]])
rgb.resize((240, 240), Image.NEAREST).save(os.path.join(out, "bao_big.png"))
