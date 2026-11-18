"""TOURIST (female): holidaymaker in a straw sun hat, big sunglasses, white hibiscus sundress,
shopping bags. Front from lady, OW from woman_2. Pairs with tourist_m (straw + red hibiscus + shades).
Run from dev_scripts/trainer_classes: python classes/tourist_f.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

# ---------------------------------------------------------------- front pic
f = load_front('lady')

# feather on the hat goes; the hat brim is rebuilt under it below
f.remap({6: 0, 14: 0, 10: 0}, (36, 0, 47, 12))
# blonde hair -> brown (4 mid, 3 dark) on the head only
f.remap({7: 4, 8: 3}, (20, 12, 47, 21))
# hat green -> straw (7 light, 8 mid; 4 = dark straw / band shadow)
f.remap({11: 7, 12: 7, 13: 8}, (14, 0, 48, 19))
# green dress -> white sundress (E white, 6 light grey, A grey)
# (B lit -> white, D base -> light grey, C dither/fold accents -> grey)
f.remap({11: 14, 12: 10, 13: 6}, (10, 19, 56, 63))

PAL = {
    1: (255, 228, 212), 2: (240, 184, 160), 3: (168, 112, 88), 4: (128, 80, 48),
    5: (88, 56, 56), 6: (216, 224, 232), 7: (248, 224, 136), 8: (208, 160, 80),
    9: (232, 96, 120), 10: (152, 164, 184),
    11: (248, 112, 96), 12: (216, 48, 64), 13: (136, 24, 40),
    14: (255, 255, 255), 15: (0, 0, 16),
}
for k, v in PAL.items():
    f.set_pal(k, v)
K = {'s': 7, 'S': 8, 'T': 4, 'r': 11, 'R': 12, 'k': 13, 'w': 14, 'g': 6, 'G': 10, 'o': 5, 'p': 9}

# rebuild the right brim where the feather was
f.patch(36, 4, '''
    .o.......
    .So......
    sSSo.....
    sSSSo....
    sSSSSo...
    SSSSSSo..
    FFSSSSSo.
    ..FSSSSSo
    ...FFFSSo
''', K)
# red hibiscus on the crown (pairs with the red band on his hat)
f.patch(34, 2, '''
    ..ooo..
    .orrRo.
    orrRRRo
    orRkRRo
    .oRRRo.
    ..ooo..
''', K)

# the loose curl beside her cheek in hair browns (was blonde 7/8 + skin-shadow 3)
for (x, y), v in {(26, 15): 4, (25, 16): 4, (26, 16): 5, (25, 17): 4, (26, 17): 0, (25, 18): 5}.items():
    f.put(x, y, v)

# big round sunglasses: red frames, tinted lenses, grey glint
f.patch(26, 11, '''
    kRRRk..kRRRk
    RgooRkkRgooR
    RoooR..RoooR
    .kRk....kRk.
''', K)

# the skirt's left outline alternated two dark greens; as dark/grey it reads dotted -> solid
for y in range(19, 63):
    xs = [x for x in range(64) if f.px[y][x]]
    if xs and f.px[y][xs[0]] in (6, 10):
        f.px[y][xs[0]] = 5

# red hibiscus print on the skirt
# (off-centre blossoms with a leaf-dark heart, so they never read as red crosses)
FLOWERS = ['''
    rr.
    rkR
    .RR
''', '''
    .rr
    RkR
    RR.
''']
for n, (x, y) in enumerate(((22, 44), (29, 40), (25, 51), (33, 47), (40, 44), (38, 52), (19, 56), (45, 51), (31, 55))):
    f.patch(x, y, FLOWERS[n % 2], K)

# basket -> red shopping bag with a little white orchid, handles over the forearm
f.clear(26, 33, 43, 42)
f.patch(26, 33, '''
    ..5AAA5F.k..k.....
    .5AAAAA5.k..k.....
    5AAAAAAA5ok..ko...
    AEEE6AAkkkkkkkkko.
    5EEEE6orrrrrrRRkko
    AEEEEEowwwwwwggkkoF
    5EEEEEorrrrrrRRkkoAF
    AEEEEEorrrrrrRRkkoAAF
    5EEEEEorrrrrrRRkkoAAAF
    5EEEEEoooooooooooAAAAAF
''', K)

# kraft-paper bag hanging from the outstretched hand (rope handles gathered in the fist)
f.patch(9, 33, '''
    ......TT.....
    .....T..T....
    ....T....T...
    ...T......T..
    .ooooooooooo.
    .osSSSSSSSTo.
    .osSSSSSSTTo.
    .osSSSSSSTTo.
    .orrrrrrRRko.
    .osSSSSSSTTo.
    .osSSSSSSTTo.
    .osSSSSSSTTo.
    .osSSSSSTTTo.
    .ooooooooooo.
''', K)

# lift the shoe tip off the 64x64 edge (vanilla lady touches row 63)
f.clear(0, 63, 63, 63)
f.patch(24, 62, '5FFF5')

res = [f.save_front('tourist_f')]

# ---------------------------------------------------------------- overworld
# woman_2 (wavy hair, dress, carries a handbag in side view) moved from npc_3 to npc_2,
# the same shared palette as tourist_m: golden straw 5-7, red 8-A, brown hair B-D.
o = load_ow('woman_2')
o.pal = npc_pal('npc_2')
# green dress -> white sundress with red accents; lavender apron edge -> red trim
o.remap({8: 14, 9: 8, 5: 9})

HAT = '''
    .....777777.....
    ....75555567....
    ...7555555667...
    ...7999999997...
    .775555555566677
    7555555555566667
    .77777777777777.
'''
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
for i in range(9):
    fr, b = o.frame(i), BOB[i]
    dx = 1 if i in (2, 7, 8) else 0
    fr.clear(0, 0, 15, 14 + b)
    fr.patch(0, 9 + b, HAT)
    if i in (0, 3, 4):
        # sunglasses
        fr.patch(5, 18 + b, '''
            FFFFFF
            FF..FF
        ''')
        # little red shopping bag under the right hand (follows the arm swing)
        hy = max(y for y in range(22, 31) for x in range(12, 16) if fr.px[y][x] in (1, 2, 3, 4))
        fr.patch(12, hy + 1, '''
            .9..
            A88A
            A898
            .AA.
        ''')
    if i in (2, 7, 8):
        fr.patch(3, 18 + b, '''
            FFFF
            .FF.
        ''')
        # handbag in front -> red shopping bag
        fr.patch(2, 26 + b, '''
            .A9.
            A889
            A889
            .AA.
        ''')
    o.set_frame(i, fr)

res.append(o.save_ow('tourist_f', 'npc_2'))
compare('tourist_f', 'lady', 'woman_2')
report('tourist_f', res)
