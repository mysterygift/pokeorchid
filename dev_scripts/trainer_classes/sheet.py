"""Review sheet: vanilla base | new front (3x) and OW stand frames (3x) per id.
usage: sheet.py OUT.png id[:base_front] ..."""
import os, sys
from PIL import Image
import kit

out_path = sys.argv[1]
rows = []
for arg in sys.argv[2:]:
    id_, _, base = arg.partition(':')
    parts = []
    if base:
        parts.append(kit.load_front(base).render(3, (232, 232, 232)))
    f = os.path.join(kit.OUT, f'{id_}_front.png')
    if os.path.exists(f):
        parts.append(kit.Pic.from_png(f).render(3, (232, 232, 232)))
        parts.append(kit.Pic.from_png(f).render(1, (232, 232, 232)))
    o = os.path.join(kit.OUT, f'{id_}_ow.png')
    if os.path.exists(o):
        parts.append(kit.ow_preview(kit.Pic.from_png(o), 3))
    rows.append(parts)
W = max(sum(p.width + 6 for p in r) for r in rows)
H = sum(max(p.height for p in r) + 6 for r in rows)
out = Image.new('RGBA', (W, H), (70, 70, 70, 255))
y = 0
for r in rows:
    x = 0
    for p in r:
        out.paste(p, (x, y)); x += p.width + 6
    y += max(p.height for p in r) + 6
out.save(out_path)
print(out_path, out.size)
