"""Install the approved Holon Researcher + Cynthia sprites (design/) into graphics/ as 4-bit, 16-colour PNGs.

usage: <venv python> dev_scripts/voyages/trainers/install_sprites.py
Checks: front pics 64x64, OW sheets 144x32 (9 frames of 16x32), indices < 16, and each OW sheet's palette equals
the shared NPC palette its object event loads (npc_3 for the researcher, npc_white for Cynthia).
Cynthia's sprites are by lichen (credited in CREDITS.md).
"""
import os
import sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DESIGN = os.path.join(HERE, 'design')
FRONT = os.path.join(ROOT, 'graphics/trainers/front_pics')
OW = os.path.join(ROOT, 'graphics/object_events/pics/people')
NPC_PAL = os.path.join(ROOT, 'graphics/object_events/palettes')

SPRITES = [  # design stem, installed name, OW shared palette
    ('holon_researcher', 'holon_researcher', 'npc_3'),
    ('cynthia', 'cynthia', 'npc_white'),
]


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
    flat = im.getpalette()
    return px, [rgb555(tuple(flat[i * 3:i * 3 + 3])) for i in range(16)]


def write16(path, size, px, pal):
    im = Image.new('P', size)
    im.putdata(px)
    im.putpalette([v for c in pal for v in c])
    im.save(path, optimize=False)


def main():
    err = []
    for stem, name, npc in SPRITES:
        px, pal = load16(os.path.join(DESIGN, stem + '_front.png'), (64, 64))
        write16(os.path.join(FRONT, name + '.png'), (64, 64), px, pal)
        px, pal = load16(os.path.join(DESIGN, stem + '_ow.png'), (144, 32))
        want = [rgb555(c) for c in read_jasc(os.path.join(NPC_PAL, npc + '.pal'))]
        if pal != want:
            err.append(f'{stem}: OW palette != {npc}')
        write16(os.path.join(OW, name + '.png'), (144, 32), px, pal)
        print('installed', name)
    if err:
        sys.exit('\n'.join(err))


if __name__ == '__main__':
    main()
