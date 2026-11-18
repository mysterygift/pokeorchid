"""ORCHID KEEPER (orchid_keeper_f): botanic-garden orchid grower. Straw sun hat with an orchid on the
band, gardening gloves, cream apron with a trowel in the pocket, holding a potted Vanda Miss Joaquim
(pink-violet blooms, magenta lip).
Front: lady (RSE) pose, face, hat and dress silhouette. OW: picnicker on npc_green.
Run from dev_scripts/trainer_classes: python classes/orchid_keeper_f.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

ID = 'orchid_keeper_f'

# ------------------------------------------------------------------ front
f = load_front('lady')
T = 100

PAL = {
    0: BG,
    1: (255, 230, 216), 2: (240, 184, 168), 3: (160, 120, 96),     # skin (3 also hair sheen)
    4: (112, 72, 48),                                               # brown hair / pot shade
    5: (72, 64, 32),                                                # dark olive outline (vanilla)
    6: (240, 184, 232),                                             # orchid petal light
    7: (248, 224, 136), 8: (208, 160, 88),                          # straw / canvas
    9: (208, 64, 160),                                              # orchid lip magenta
    10: (112, 40, 112),                                             # orchid deep purple, hat band
    11: (176, 232, 104), 12: (144, 208, 80), 13: (112, 176, 64),    # green work dress / leaves
    14: (255, 255, 255), 15: (0, 0, 24),
}

# hair: blonde -> dark brown (7 sheen -> 3, 8 main -> 4, 4 shade -> 5), face box untouched
for y in range(12, 28):
    for x in range(22, 47):
        if 27 <= x <= 36 and y <= 19:
            continue
        v = f.px[y][x]
        f.px[y][x] = {7: T + 3, 8: T + 4, 4: T + 5}.get(v, v)
f.remap({T + 3: 3, T + 4: 4, T + 5: 5})
# hat: green -> straw (region of the hat and brim)
HAT = [(19, 2, 36, 11), (31, 3, 37, 9), (36, 12, 49, 19)]
for r in HAT:
    f.remap({11: T + 7, 12: T + 8, 13: T + 8}, r)
f.remap({T + 7: 7, T + 8: 8})

# lace that used grey slots 6/A: bodice lace stays white with green shade, hem ruffle goes green
f.remap({6: 11, 10: 13}, (14, 19, 45, 34))
f.remap({14: 12, 6: 13, 10: 5}, (8, 49, 56, 62))

# ---- gardening gloves (canvas) on both hands, cuff at the wrist
f.remap({1: 7, 2: 7, 3: 8}, (12, 28, 21, 34))
f.remap({1: 7, 2: 7, 3: 8}, (31, 28, 39, 33))
for y in range(29, 33):
    if f.px[y][22] not in (0, 5, 15):
        f.put(22, y, 8)

# ---- the basket becomes a terracotta pot (dress filled in behind it first)
for y in range(33, 42):
    for x in range(29, 44):
        if f.px[y][x] in (4, 7, 8, 15) or (f.px[y][x] == 5 and x >= 30):
            f.px[y][x] = 13 if x >= 33 else 11
f.outline(15, (40, 33, 47, 42))
f.patch(30, 32, '''
    F33333333F.
    F44444444F.
    .F334444F..
    .F334445F..
    ..F34445F..
    ..F34455F..
    ..F34455F..
    ...FFFFF...
    ''')

# ---- canvas apron from the waist over the skirt front (behind the pot), pocket + trowel handle
APRON = {35: (24, 32), 36: (24, 32), 37: (23, 33), 38: (23, 33), 39: (23, 34), 40: (22, 34),
         41: (22, 35), 42: (22, 35), 43: (21, 35), 44: (21, 36), 45: (21, 36), 46: (21, 36),
         47: (20, 36), 48: (20, 37), 49: (20, 37), 50: (20, 37), 51: (19, 37), 52: (19, 38),
         53: (19, 38), 54: (19, 38)}
for y, (l, r) in APRON.items():
    l, r = l + 2, r + 2          # centred on the skirt front
    for x in range(l, r + 1):
        if f.px[y][x] in (0, 15):
            continue
        if f.px[y][x] in (4, 8) and 30 <= x <= 40 and y <= 40:   # leave the pot alone
            continue
        if x == l or y == 54:
            c = 5
        elif x == r:
            c = 5
        elif x <= l + 1:
            c = 7
        elif x >= r - 2:
            c = 4
        else:
            c = 8
        f.put(x, y, c)
f.patch(25, 43, '''
    ..33....
    ..34....
    4444444.
    4888884.
    4888884.
    4444444.
    ''')

# ---- Vanda Miss Joaquim: pale pink-violet upper petals, broad magenta lip, yellow column
BLOOM = '''
    .AA.AA.
    A66A66A
    A66766A
    .A999A.
    A99999A
    .AA9AA.
    '''
BUD = '''
    .A.
    A6A
    A9A
    .A.
    '''
# the hat bow becomes an orchid corsage on the band
for y in range(0, 13):
    for x in range(35, 49):
        if f.px[y][x] in (6, 10, 14):
            f.px[y][x] = 0
f.patch(36, 4, '''
    F7778
    57788
    .5788
    ..588
    ''')
f.patch(37, 1, BLOOM)
f.patch(42, 5, BUD)
# terete leaves and one flower spike rising out of the pot; blooms clear of the hat and hair
f.patch(34, 28, '''
    .5...........
    5D5.......5..
    5C5......5D5.
    .5D5....5D5..
    ..5D5..5D5...
    ''')
STEM = [(41, 31), (42, 30), (43, 29), (44, 28), (45, 27), (46, 26), (47, 25), (48, 24), (49, 23),
        (50, 22), (50, 21)]
for x, y in STEM:
    f.put(x, y, 13)
    if f.px[y + 1][x] == 0:
        f.put(x, y + 1, 5)
f.patch(49, 15, BUD)
f.patch(46, 18, BLOOM)
f.patch(49, 25, BLOOM)

if 'dump' in sys.argv:
    print(f.dump(10, 0, 58, 63))

for k, v in PAL.items():
    f.set_pal(k, v)
res = [f.save_front(ID)]

# ------------------------------------------------------------------ overworld
# picnicker (npc_3) recoloured onto npc_green: cap -> wide straw sun hat (5-7) with a purple band
# and an orchid (B/C) on it, auburn pigtails -> dark olive-brown hair (7 main, 6 sheen), white tee ->
# tan work shirt, green dungarees stay green, hands in canvas gloves.
base = load_ow('picnicker')
o = blank_ow('npc_green')
HAT_TOP = {0: 11, 1: 11, 2: 11, 3: 12, 4: 12, 5: 12, 6: 12, 7: 12, 8: 12}   # first cap row
FRONTAL = (0, 1, 3, 4, 5, 6)
for fr in range(9):
    src = base.frame(fr)
    dst = o.frame(fr)
    top = HAT_TOP[fr]
    body_y = top + 10            # first clothing row
    for y in range(32):
        for x in range(16):
            v = src.px[y][x]
            if v == 0:
                continue
            if y < body_y:
                if v in (1, 2, 3, 4, 15):
                    n = v
                elif v == 11:
                    n = 6
                elif v == 13:
                    edge = any(not (0 <= x + dx < 16) or src.px[y + dy][x + dx] == 0
                               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    n = 15 if edge else 7
                else:
                    n = 7
            else:
                n = {14: 5, 5: 6, 6: 6, 7: 7, 11: 6, 12: 7, 13: 7}.get(v, v)
                if fr in FRONTAL and v in (1, 2, 3) and (x <= 3 or x >= 12) and y >= body_y + 2:
                    n = 5 if v in (1, 2) else 6          # canvas gloves
            dst.px[y][x] = n
    o.set_frame(fr, dst)

HAT_FRONT = """
.....777777.....
....755555B7....
...7DDDDDBCB7...
.75555555555557.
.76666666666667.
"""
HAT_BACK = """
.....777777.....
....75555557....
...7DDDDDDDD7...
.75555555555557.
.76666666666667.
"""
HAT_SIDE = """
.....777777.....
....755555B7....
...7DDDDDBCB7...
755555555555557.
766666666666667.
"""
for fr in range(9):
    hat = HAT_BACK if fr in (1, 5, 6) else HAT_SIDE if fr in (2, 7, 8) else HAT_FRONT
    rows = hat.strip('\n').split('\n')
    d = o.frame(fr)
    top = HAT_TOP[fr]
    for y in range(0, top + len(rows)):
        if y < top:
            d.px[y] = [0] * 16
    for dy, line in enumerate(rows):
        d.px[top + dy] = [0 if ch == '.' else HEX.index(ch) for ch in line]
    o.set_frame(fr, d)

# pigtails pinned up under the hat: hair no wider than the brim (front/back views)
for fr in (0, 1, 3, 4, 5, 6):
    d = o.frame(fr)
    top = HAT_TOP[fr]
    for y in range(top + 5, top + 10):
        for x in (0, 15):
            d.px[y][x] = 0
        for x in (1, 14):
            if d.px[y][x] not in (0,):
                d.px[y][x] = 15
    o.set_frame(fr, d)

res.append(o.save_ow(ID, 'npc_green'))
compare(ID, 'lady', 'picnicker')
report(ID, res)
