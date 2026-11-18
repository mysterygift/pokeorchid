"""Zoom OW sheets (first 9 frames) stacked. usage: owview.py out.png path1 path2 ..."""
import sys, os
from PIL import Image
S = 6
out_path = sys.argv[1]
paths = sys.argv[2:]
ims = []
for p in paths:
    im = Image.open(p)
    pal = im.getpalette()[:3]
    rgb = im.convert('RGB').crop((0, 0, min(im.width, 144), 32))
    px = rgb.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            if px[x, y] == tuple(pal):
                px[x, y] = (232, 232, 232)
    ims.append(rgb.resize((rgb.width * S, rgb.height * S), Image.NEAREST))
W = max(i.width for i in ims)
out = Image.new('RGB', (W, sum(i.height + 6 for i in ims)), (60, 60, 60))
y = 0
for i in ims:
    out.paste(i, (0, y)); y += i.height + 6
out.save(out_path)
print(out_path)
