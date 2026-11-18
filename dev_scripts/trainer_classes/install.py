"""Install the finished trainer-class sprites from out/ into graphics/ (the files the C tables INCGFX).

Run from dev_scripts/trainer_classes/:  python install.py

- New classes: out/<id>_front.png -> graphics/trainers/front_pics/<name>.png
               out/<id>_ow.png    -> graphics/object_events/pics/people/<name>.png
- Replacements (same job): the vanilla PNG is first copied to <name>-og.png (only if no -og exists yet),
  then overwritten in place.
- School Kid F: her OW palette out/npc_school_kid_f.pal -> graphics/object_events/palettes/.

Every PNG is written as a 4-bit, 16-colour indexed PNG (out/ files carry 256-entry palettes, which would
make gbagfx emit 512-byte .gbapal files). Checks: front pics 64x64, OW sheets 144x32 (9 frames of 16x32,
the vanilla sheet size for every base used here), pixel indices < 16, and OW palettes equal to the shared
NPC .pal the object event uses (the OW PNG palette itself is never loaded in game).
"""
import os
import shutil
import sys
from PIL import Image

from kit import ROOT, OUT, NPC_PAL_DIR, read_jasc, rgb555

FRONT_DIR = os.path.join(ROOT, 'graphics/trainers/front_pics')
OW_DIR = os.path.join(ROOT, 'graphics/object_events/pics/people')

# (out id, installed file name, 'new' | 'replace', OW palette name or None for no OW)
SPRITES = [
    ('tourist_m',         'tourist_m',    'new',     'npc_2'),
    ('tourist_f',         'tourist_f',    'new',     'npc_2'),
    ('hawker_m',          'hawker_m',     'new',     'npc_pink'),
    ('hawker_f',          'hawker_f',     'new',     'npc_pink'),
    ('delivery_m',        'rider',        'new',     'npc_blue'),
    ('executive_m',       'executive',    'new',     'npc_white'),
    ('influencer_f',      'influencer',   'new',     'npc_pink'),
    ('getai_f',           'singer',       'new',     'npc_4'),
    ('nyonya_f',          'nyonya',       'new',     'npc_pink'),
    ('dancer_f',          'dancer',       'new',     'npc_2'),
    ('orchid_keeper_f',   'orchidist',    'new',     'npc_green'),
    ('recruit_m',         'recruit',      'new',     'npc_1'),
    ('edit_sailor',       'port_worker',  'new',     'npc_blue'),
    ('edit_expert_m',     'expert_m',     'replace', 'npc_4'),
    ('edit_black_belt',   'black_belt',   'replace', 'npc_4'),
    ('edit_school_kid_m', 'school_kid_m', 'replace', 'npc_1'),
    # front pic replaces vanilla; the OW is new (vanilla has no School Kid F overworld)
    ('edit_school_kid_f', 'school_kid_f', 'replace', 'npc_school_kid_f'),
]
OWN_PALETTES = {'npc_school_kid_f'}


def npc_palette(name):
    path = os.path.join(OUT if name in OWN_PALETTES else NPC_PAL_DIR, name + '.pal')
    return [rgb555(c) for c in read_jasc(path)]


def load16(path, size):
    im = Image.open(path)
    assert im.mode == 'P', f'{path}: not indexed'
    assert im.size == size, f'{path}: {im.size}, expected {size}'
    px = list(im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata())
    assert max(px) < 16, f'{path}: pixel index {max(px)} >= 16'
    flat = im.getpalette()
    pal = [rgb555(tuple(flat[i * 3:i * 3 + 3])) for i in range(16)]
    return px, pal


def write16(path, size, px, pal):
    im = Image.new('P', size)
    im.putdata(px)
    im.putpalette([v for c in pal for v in c])  # 16 entries -> Pillow writes a 4-bit PNG
    im.save(path, optimize=False)


def backup(path):
    root, ext = os.path.splitext(path)
    og = root + '-og' + ext
    if os.path.exists(path) and not os.path.exists(og):
        shutil.copy2(path, og)
        print('  backup', os.path.relpath(og, ROOT))


def main():
    errors = []
    for sid, name, mode, npc in SPRITES:
        print(sid, '->', name, f'({mode})')
        # front pic
        px, pal = load16(os.path.join(OUT, sid + '_front.png'), (64, 64))
        dst = os.path.join(FRONT_DIR, name + '.png')
        if mode == 'replace':
            if not os.path.exists(dst):
                errors.append(f'{name}: no vanilla front pic to replace')
            backup(dst)
        write16(dst, (64, 64), px, pal)
        # overworld
        px, pal = load16(os.path.join(OUT, sid + '_ow.png'), (144, 32))
        want = npc_palette(npc)
        if pal != want:
            errors.append(f'{sid}: OW palette differs from {npc}')
        dst = os.path.join(OW_DIR, name + '.png')
        if mode == 'replace' and os.path.exists(dst):
            backup(dst)
            van = Image.open(dst.replace('.png', '-og.png'))
            if van.size != (144, 32):
                errors.append(f'{name}: vanilla OW is {van.size}, not 144x32')
        write16(dst, (144, 32), px, pal)
    shutil.copy2(os.path.join(OUT, 'npc_school_kid_f.pal'),
                 os.path.join(NPC_PAL_DIR, 'npc_school_kid_f.pal'))
    print('palette -> graphics/object_events/palettes/npc_school_kid_f.pal')
    if errors:
        print('\n'.join('ERROR ' + e for e in errors))
        sys.exit(1)
    print('ok')


if __name__ == '__main__':
    main()
