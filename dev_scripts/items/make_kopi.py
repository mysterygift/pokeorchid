"""Kopi icon = tea.png with coffee-coloured liquid and a mug handle. usage: make_kopi.py REPO OUTDIR"""
import sys, os
from PIL import Image
repo, out = sys.argv[1], sys.argv[2]
im = Image.open(os.path.join(repo, "graphics/items/icons/tea.png")).copy()
pal = [tuple(int(v) for v in l.split()) for l in open(os.path.join(repo, "graphics/items/icon_palettes/tea.pal")).read().split("\n")[3:19]]
# liquid: tea greens -> coffee browns (index 5 light, 8 mid, B dark)
pal[5] = (208, 152, 96)
pal[8] = (152, 96, 56)
pal[11] = (104, 64, 40)
# handle on the right of the body (outline 1, fill 2 light / 4 shade), rows 10..17, cols 19..22
H = {
    10: "11..",
    11: "2241",
    12: "11.41",
    13: ".1.41",
    14: ".1.41",
    15: "11.41",
    16: "2241",
    17: "11..",
}
px = im.load()
for y, row in H.items():
    for i, ch in enumerate(row):
        if ch != ".":
            px[19 + i, y] = int(ch, 16)
os.makedirs(out, exist_ok=True)
im.save(os.path.join(out, "kopi.png"), transparency=0)
with open(os.path.join(out, "kopi.pal"), "w", newline="\r\n") as f:
    f.write("JASC-PAL\n0100\n16\n" + "".join("%d %d %d\n" % c for c in pal))
rgb = Image.new("RGB", im.size)
for y in range(im.size[1]):
    for x in range(im.size[0]):
        rgb.putpixel((x, y), pal[px[x, y]])
rgb.resize((240, 240), Image.NEAREST).save(os.path.join(out, "kopi_big.png"))
