"""EDIT: vanilla BLACK BELT (Emerald karate guy) -- recoloured gi, red headband removed.
Replaces the vanilla Black Belt graphics (same class), so the pose, face, fist and belt stay as-is.
Front: black_belt. OW: black_belt sheet moved onto a shared NPC palette with the gi ramp.
Run from dev_scripts/trainer_classes/:  python classes/edit_black_belt.py [--options]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *
from PIL import Image

ID = 'edit_black_belt'
FACE = (23, 17, 31, 25)          # eyes + shouting mouth keep their white (E) and red (D)

# gi ramps, lightest -> darkest, written into slots C, 9, A, B, 5, 6
# (vanilla order: E 246,230,230 > 9 > A > B > 5 > 6 106,90,82)
GI = {
    'navy':   [(104, 128, 192), (72, 96, 160), (64, 84, 144), (48, 68, 120), (40, 56, 104), (24, 32, 64)],
    'maroon': [(216, 104, 104), (184, 64, 72), (168, 56, 64), (136, 40, 56), (120, 32, 48), (80, 24, 32)],
    'teal':   [(104, 200, 184), (64, 160, 152), (56, 144, 136), (40, 120, 120), (32, 104, 104), (16, 64, 72)],
    'black':  [(128, 128, 144), (88, 88, 104), (72, 72, 88), (56, 56, 72), (48, 48, 64), (24, 24, 32)],
}
CHOICE = 'navy'


def front(option):
    f = load_front('black_belt')
    # ---- headband removal: hair mass continues to row 15, forehead skin on rows 16-17
    f.patch(23, 15, '''
        .F778888F
        FF843223F
        FFF322123
    ''')
    # ---- gi recolour: the gi's white (E) moves to the free slot C; E stays white in eyes/teeth
    for y in range(64):
        for x in range(64):
            if f.px[y][x] == 14 and not (FACE[0] <= x <= FACE[2] and FACE[1] <= y <= FACE[3]):
                f.px[y][x] = 12
    for slot, rgb in zip((12, 9, 10, 11, 5, 6), GI[option]):
        f.set_pal(slot, rgb)
    if option == 'black':     # coloured belt so a black gi still reads (belt 7 -> red D)
        f.remap({7: 13}, (24, 38, 36, 43))
    assert not any(f.px[y][x] == 13 for y in range(14, 18) for x in range(22, 34)), 'band pixels left'
    return f


if '--options' in sys.argv:
    tiles = [front(k).render(4, (232, 232, 232)) for k in GI]
    sheet = Image.new('RGBA', (len(tiles) * 264, 256), (70, 70, 70, 255))
    for i, t in enumerate(tiles):
        sheet.paste(t, (i * 264, 0))
    sheet.save(os.path.join(OUT, ID + '_options.png'))
    print('options:', list(GI))

f = front(CHOICE)
res = [f.save_front(ID)]

# ---------------------------------------------------------------- OW
# vanilla OW (npc_3): red-brown hair B-D, white headband E/5/7 on rows 15-18, white gi E/5/7,
# green belt 8-A.  -> npc_4: navy 5-7 = gi, greys B-D + F = black hair (matches the front pic)
# and the black belt.  Headband rows are repainted in the vanilla indices first, then remapped.
o = load_ow('black_belt')
HB = {  # direction: rows 15.. replacement in vanilla indices ('.' keeps); C = hair mid, D = outline
    'front': '''
        ..DCCBCCCCBCCD..
        ..DCCDCCDCCCCD..
        ..DD21111112DD..
        .41D2D2112D2D14.''',
    'back': '''
        ..DCBCCCCCCBCD..
        ..DCCCCBCCCCCD..
        ..DCCDCCDCCDCD..
        .41DDCCCCCCDD14.
        .42DD233332DD24.
        ..4F533333354F..''',
    'side': '''
        ..DCCBCCCCBCCD..
        ..D2DCCCCCBCCD..
        ..21112DCCCCCD..
        ..42212112DCDD..''',
}
for i in range(9):
    b = 1 if i >= 3 else 0
    d = ('front', 'back', 'side', 'front', 'front', 'back', 'back', 'side', 'side')[i]
    o.patch_frame(i, 0, 15 + b, HB[d])
o.pal = npc_pal('npc_4')
o.remap({14: 5, 5: 6, 7: 6,          # gi: white -> navy, grey shade + lavender outline -> deep navy
         11: 12, 12: 13, 13: 15,     # hair: red-brown -> grey highlight / charcoal / black
         8: 13, 9: 15, 10: 15})      # belt: green -> black
res.append(o.save_ow(ID, 'npc_4'))
compare(ID, 'black_belt', 'black_belt')
report(ID, res)
