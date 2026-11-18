"""Silhouette audit: where does the new front pic grow past (red) or shrink inside (blue) its vanilla base?
usage: silhouette.py OUT.png id:base ...   (prints growth/shrink pixel counts; props legitimately grow)"""
import os, sys
from PIL import Image
import kit

S = 4
out_path = sys.argv[1]
tiles = []
for arg in sys.argv[2:]:
    id_, base = arg.split(':')
    b = kit.load_front(base)
    n = kit.Pic.from_png(os.path.join(kit.OUT, f'{id_}_front.png'))
    im = n.render(1, (240, 240, 240)).convert('RGB')
    px = im.load()
    grow = shrink = 0
    for y in range(64):
        for x in range(64):
            bo, no = b.px[y][x] != 0, n.px[y][x] != 0
            if no and not bo:
                grow += 1
                r, g, bl = px[x, y]
                px[x, y] = (255, (g + 40) // 3, (bl + 40) // 3)
            elif bo and not no:
                shrink += 1
                px[x, y] = (120, 160, 255)
    print(f'{id_:18s} base {base:22s} grow {grow:4d}  shrink {shrink:4d}')
    tiles.append(im.resize((64 * S, 64 * S), Image.NEAREST))
out = Image.new('RGB', (len(tiles) * (64 * S + 6), 64 * S), (60, 60, 60))
for i, t in enumerate(tiles):
    out.paste(t, (i * (64 * S + 6), 0))
out.save(out_path)
