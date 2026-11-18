"""Contact sheet of the battle floors used by review.py."""
import os, subprocess, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
envs = ['orchid_beach', 'orchid_void_deck', 'orchid_office', 'orchid_mall', 'orchid_grass', 'orchid_ruins', 'orchid_jungle']
ims = []
for e in envs:
    dst = os.path.join(HERE, 'out/ref', f'env_{e}.png')
    subprocess.run([sys.executable, os.path.join(HERE, 'battle_mock.py'), os.path.join(HERE, '../../graphics/trainers/front_pics/lady.png'), e, e.upper(), dst], check=True)
    ims.append(Image.open(dst))
out = Image.new('RGB', (4 * 244, 2 * 164))
for i, im in enumerate(ims):
    out.paste(im, ((i % 4) * 244, (i // 4) * 164))
out.save(os.path.join(HERE, 'out/ref/envs.png'))
