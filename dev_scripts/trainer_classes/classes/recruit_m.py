"""RECRUIT (recruit_m): National Service recruit saluting. Plain olive-green field uniform (no camo),
olive jockey cap, black web belt, black boots, bare saluting hand.
Front: engineer_frlg (FRLG) pose/face/salute; helmet -> jockey cap, tool belt and toolbox removed.
OW: camper on npc_1 (olive ramp B-D).
Run from dev_scripts/trainer_classes: python classes/recruit_m.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

ID = 'recruit_m'

# ------------------------------------------------------------------ front
# engineer_frlg uses the FRLG layout: 1 black outline, 2-5 skin (5 = dark brown outline/hair),
# 6/8/9 blue-grey (gloves, boots), D/E/A/F the yellow ramp (helmet + overalls), B/C red (toolbox).
f = load_front('engineer_frlg')
PAL = {
    0: BG,
    1: (16, 16, 16),
    2: (255, 222, 205), 3: (238, 180, 148), 4: (197, 139, 106), 5: (96, 64, 56),
    6: (64, 64, 72), 8: (120, 120, 128), 9: (40, 40, 48),          # black boots / web belt
    7: (255, 255, 255),
    13: (160, 168, 96), 14: (120, 128, 72), 10: (88, 96, 48), 15: (56, 64, 32),   # olive No.4
    11: (176, 176, 168), 12: (200, 64, 64),                          # buckle, spare
}

# saluting hand: blue-grey glove -> bare skin
f.remap({6: 4, 9: 3, 8: 2}, (10, 7, 23, 17))

# helmet -> soft olive jockey cap: no white shine, dark peak over the brow
f.remap({7: 13, 2: 13}, (20, 4, 38, 9))
f.patch(20, 9, '''
    .EEEEEEEEEEEEEEE
    1DDDDDDDDDDDF
    ....1AAAAAAAAA1
    ''')

# tool belt + pliers -> plain uniform with a black web belt and buckle (centred on the torso)
f.clear(13, 28, 24, 38)
f.clear(13, 39, 20, 39)
f.patch(19, 34, '''
    ____1999999BB99999991..
    ____16666668B66666661..
    ___1EEDDDEAAAAAAFAAAA1.
    ___1EEDDDEAAAAAFFAAAA1.
    ___1EEEDDEAAAAFFFAAAAA1
    __1EED
    ''')
for y in range(29, 34):          # torso's own left edge closes the gap the pliers left
    for x in range(13, 25):
        f.put(x, y, 0)
    f.put(25, y, 15 if f.px[y][25] else 0)
# toolbox removed: right hand closed into a fist at the side
f.clear(42, 33, 60, 47)
f.patch(49, 32, '''
    .533331
    .534331
    .543441
    .154451
    ..1111.
    ''')

if 'dump' in sys.argv:
    print(f.dump(4, 0, 60, 63))

for k, v in PAL.items():
    f.set_pal(k, v)
res = [f.save_front(ID)]

# ------------------------------------------------------------------ overworld
# camper (npc_3) on npc_1: green cap + shirt -> olive B/C/D, brown hair -> near-black buzz cut
# (A/F), white undershirt -> olive, shorts + bare legs -> olive trousers bloused into black boots,
# black web belt with a light buckle.
base = load_ow('camper')
o = blank_ow('npc_1')
BOB = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}
CLOTH = {8: 12, 9: 12, 10: 13, 5: 12, 14: 11, 7: 13, 6: 12}   # mostly olive C, D shade
for fr in range(9):
    src = base.frame(fr)
    dst = o.frame(fr)
    b = BOB[fr]
    side = fr in (2, 7, 8)
    for y in range(32):
        for x in range(16):
            v = src.px[y][x]
            if v == 0:
                continue
            if y <= 21 + b:                       # head: cap (B top, C, D), hair C/D -> A/F
                n = {12: 10, 13: 15, 8: 11}.get(v, CLOTH.get(v, v))
                if fr in (1, 5, 6) and y >= 20 + b and v in (12, 13):
                    edge = x in (0, 15) or src.px[y][x - 1] == 0 or src.px[y][x + 1] == 0
                    n = 15 if edge else (3 if v == 12 else 4)   # shaved nape under the cap
            elif y >= 29 + b - (1 if side else 0):  # boots
                n = 15
            elif y >= 28 + b - (1 if side else 0) and v in (2, 3, 4, 13):   # trousers over the legs
                n = {2: 12, 3: 12, 4: 13, 13: 15}[v]
            else:
                n = {13: 15, 12: 13}.get(v, CLOTH.get(v, v))
            dst.px[y][x] = n
    o.set_frame(fr, dst)
# web belt (front/back views)
for fr in (0, 1, 3, 4, 5, 6):
    y = 26 + BOB[fr]
    d = o.frame(fr)
    for x in range(4, 12):
        if d.px[y][x] not in (0,):
            d.px[y][x] = 15
    if fr in (0, 3, 4):
        d.px[y][7] = d.px[y][8] = 14
    o.set_frame(fr, d)

res.append(o.save_ow(ID, 'npc_1'))
compare(ID, 'engineer_frlg', 'camper')
report(ID, res)
