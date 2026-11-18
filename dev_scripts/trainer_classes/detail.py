"""Zoom vanilla front pics side by side with their palette strip. usage: detail.py out.png name1 name2 ..."""
import sys, os
from PIL import Image, ImageDraw

SRC = os.path.join(os.path.dirname(__file__), '../../graphics/trainers/front_pics')
S = 6
out_path = sys.argv[1]
names = sys.argv[2:]
W = 64 * S
out = Image.new('RGB', (len(names) * (W + 8), W + 40), (60, 60, 60))
d = ImageDraw.Draw(out)
for i, n in enumerate(names):
    p = n if n.endswith('.png') else n + '.png'
    im = Image.open(os.path.join(SRC, p))
    pal = im.getpalette()[:48]
    rgb = im.convert('RGB')
    bg = tuple(pal[0:3])
    rgb = Image.eval(rgb, lambda v: v)
    px = rgb.load()
    for y in range(64):
        for x in range(64):
            if px[x, y] == bg:
                px[x, y] = (232, 232, 232)
    out.paste(rgb.resize((W, W), Image.NEAREST), (i * (W + 8), 0))
    for k in range(16):
        c = tuple(pal[k*3:k*3+3])
        d.rectangle([i * (W + 8) + k * 24, W + 8, i * (W + 8) + k * 24 + 22, W + 30], fill=c)
out.save(out_path)
print(out_path)
