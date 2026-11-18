"""Survey vanilla Gen 3 trainer front pics: size, palette use, bbox, and build contact sheets."""
import sys, os, glob
from PIL import Image

SRC = os.path.join(os.path.dirname(__file__), '../../graphics/trainers/front_pics')
OUT = os.path.join(os.path.dirname(__file__), 'out/ref')
os.makedirs(OUT, exist_ok=True)

files = sorted(f for f in glob.glob(os.path.join(SRC, '*.png')) if '-og' not in f)
rows = []
for f in files:
    im = Image.open(f)
    mode = im.mode
    if im.mode != 'P':
        rows.append((os.path.basename(f), im.size, mode, '-', '-'))
        continue
    px = im.load()
    w, h = im.size
    used = set()
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            v = px[x, y]
            used.add(v)
            if v != 0:
                xs.append(x); ys.append(y)
    bbox = (min(xs), min(ys), max(xs), max(ys)) if xs else None
    rows.append((os.path.basename(f), im.size, mode, len(used), bbox))

for r in rows:
    print(*r)

def sheet(names, path, scale=3, cols=8):
    ims = [Image.open(os.path.join(SRC, n)).convert('RGBA') for n in names]
    W = 64 * scale; H = 64 * scale
    rows_ = (len(ims) + cols - 1) // cols
    out = Image.new('RGBA', (cols * (W + 4), rows_ * (H + 4)), (200, 200, 200, 255))
    for i, im in enumerate(ims):
        # replace transparent bg colour with light grey
        bg = im.getpixel((0, 0))
        im2 = Image.new('RGBA', im.size, (235, 235, 235, 255))
        data = [(235, 235, 235, 255) if p == bg else p for p in im.getdata()]
        im2.putdata(data)
        im2 = im2.resize((W, H), Image.NEAREST)
        out.paste(im2, ((i % cols) * (W + 4), (i // cols) * (H + 4)))
    out.save(path)

if __name__ == '__main__':
    groups = {
        'rse_a': ['youngster.png', 'lass.png', 'hiker.png', 'fisherman.png', 'sailor.png', 'gentleman.png', 'lady.png', 'beauty.png'],
        'rse_b': ['tuber_m.png', 'tuber_f.png', 'pokefan_m.png', 'pokefan_f.png', 'expert_m.png', 'expert_f.png', 'collector.png', 'guitarist.png'],
        'rse_c': ['cooltrainer_m.png', 'cooltrainer_f.png', 'psychic_m.png', 'psychic_f.png', 'ninja_boy.png', 'parasol_lady.png', 'interviewer.png', 'rich_boy.png'],
        'rse_d': ['camper.png', 'picnicker.png', 'bug_catcher.png', 'school_kid_m.png', 'school_kid_f.png', 'black_belt.png', 'battle_girl.png', 'aroma_lady.png'],
        'frlg_a': ['super_nerd_frlg.png', 'engineer_frlg.png', 'gamer_frlg.png', 'biker_frlg.png', 'burglar_frlg.png', 'scientist_frlg.png', 'painter_frlg.png', 'juggler_frlg.png'],
    }
    for k, v in groups.items():
        sheet(v, os.path.join(OUT, k + '.png'))
