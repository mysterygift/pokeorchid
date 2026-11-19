"""Install the approved Holon Leader Faba art into graphics/ (4-bit, 16-colour PNGs + the transition tilemap).

usage: <venv python> dev_scripts/voyages/faba/install_faba.py
- faba_front.png (pose A)  -> graphics/trainers/front_pics/holon_leader_faba.png   (64x64)
- faba_ow.png (npc_3)      -> graphics/object_events/pics/people/faba.png           (144x32, palette must equal npc_3)
- holon_logo.png/.bin      -> graphics/battle_transitions/holon.png/.bin            (64x96, indices drawn in evil_team.pal)
"""
import os
import shutil
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FRONT = os.path.join(ROOT, 'graphics/trainers/front_pics')
OW = os.path.join(ROOT, 'graphics/object_events/pics/people')
TRANS = os.path.join(ROOT, 'graphics/battle_transitions')
NPC_PAL = os.path.join(ROOT, 'graphics/object_events/palettes')


def rgb555(c):
    return tuple((v >> 3) << 3 for v in c[:3])


def read_jasc(path):
    lines = open(path).read().split()
    n = int(lines[2])
    return [tuple(int(v) for v in lines[3 + i * 3:6 + i * 3]) for i in range(n)]


def load16(path, size):
    im = Image.open(path)
    assert im.mode == 'P' and im.size == size, (path, im.mode, im.size)
    px = list(im.get_flattened_data())
    assert max(px) < 16, path
    flat = im.getpalette() + [0] * 48
    return px, [rgb555(tuple(flat[i * 3:i * 3 + 3])) for i in range(16)]


def write16(path, size, px, pal):
    im = Image.new('P', size)
    im.putdata(px)
    im.putpalette([v for c in pal for v in c])
    im.save(path, optimize=False, bits=4)


def main():
    err = []
    px, pal = load16(os.path.join(HERE, 'faba_front.png'), (64, 64))
    write16(os.path.join(FRONT, 'holon_leader_faba.png'), (64, 64), px, pal)

    px, pal = load16(os.path.join(HERE, 'faba_ow.png'), (144, 32))
    want = [rgb555(c) for c in read_jasc(os.path.join(NPC_PAL, 'npc_3.pal'))]
    if pal != want:
        err.append('faba_ow: palette != npc_3')
    write16(os.path.join(OW, 'faba.png'), (144, 32), px, pal)

    px, _ = load16(os.path.join(HERE, 'holon_logo.png'), (64, 96))
    used = sorted(set(px))
    if not set(used) <= {0, 1, 2, 3, 4, 5, 15}:
        err.append(f'holon_logo: indices outside evil_team.pal greys: {used}')
    evil = [rgb555(c) for c in read_jasc(os.path.join(TRANS, 'evil_team.pal'))]
    write16(os.path.join(TRANS, 'holon.png'), (64, 96), px, evil[:16])
    assert os.path.getsize(os.path.join(HERE, 'holon_logo.bin')) == 2048
    shutil.copyfile(os.path.join(HERE, 'holon_logo.bin'), os.path.join(TRANS, 'holon.bin'))
    print('installed holon_leader_faba.png, faba.png, holon.png/.bin; logo indices', used)
    if err:
        sys.exit('\n'.join(err))


if __name__ == '__main__':
    main()
