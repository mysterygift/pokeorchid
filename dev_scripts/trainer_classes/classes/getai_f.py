"""GETAI SINGER (f) -- glamorous getai (Hungry Ghost Festival stage show) singer.
Front: beauty_frlg (pose, face, hair mass, arms). OW: reporter_f on npc_4.
Run from dev_scripts/trainer_classes/:  python classes/getai_f.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

ID = 'getai_f'
SKIN = (1, 2, 3, 4)

# ---------------------------------------------------------------- front pic
f = load_front('beauty_frlg')

# palette: 1-4 skin kept; 5-7 hair blue-black (5 doubles as mic grey); 8/D gold; 9/B/C gown
f.set_pal(5, (112, 112, 136))   # hair highlight / mic grille
f.set_pal(6, (56, 56, 72))      # hair mid
f.set_pal(7, (24, 24, 40))      # hair dark
f.set_pal(8, (200, 128, 24))    # gold dark
f.set_pal(9, (248, 128, 200))   # gown light
f.set_pal(11, (216, 40, 144))   # gown mid
f.set_pal(12, (128, 16, 88))    # gown dark
f.set_pal(13, (248, 224, 96))   # gold light

# eyes: lavender iris (B/D) -> hair blues so the gown slots don't tint them
f.remap({11: 6, 13: 5}, (27, 11, 37, 15))
# lips: magenta lipstick
f.remap({8: 11, 9: 12}, (31, 15, 35, 18))
f.put(34, 16, 9)
# hair: white gloss -> hair highlight
f.remap({14: 5}, (20, 2, 46, 12))
f.remap({14: 5}, (22, 13, 27, 13))

# halter top -> sequinned bodice (E light, D mid, B/A dark)
f.remap({14: 9, 13: 11, 11: 12, 12: 12, 10: 12}, (31, 18, 41, 33))
f.remap({5: 11, 6: 12, 7: 12}, (33, 30, 41, 33))     # gold belt bits

# ---- legs/skirt -> mermaid gown
for y in range(32, 63):
    for x in range(18, 48):
        if f.get(x, y) not in SKIN or y >= 34:
            f.put(x, y, 0)

PROFILE = {  # y: (left, right) outer silhouette
    32: (31, 41), 33: (30, 41), 34: (29, 42), 35: (28, 42), 36: (28, 43), 37: (28, 43),
    38: (28, 43), 39: (28, 43), 40: (28, 42), 41: (28, 42), 42: (29, 42), 43: (29, 42),
    44: (29, 41), 45: (29, 41), 46: (29, 41), 47: (29, 41), 48: (28, 41), 49: (28, 42),
    50: (27, 42), 51: (26, 42), 52: (25, 43), 53: (24, 43), 54: (23, 44), 55: (22, 44),
    56: (21, 45), 57: (20, 45), 58: (19, 46), 59: (19, 46), 60: (18, 47),
}
for y, (l, r) in PROFILE.items():
    lw = {35: 4, 36: 5, 37: 5, 38: 5, 39: 5, 40: 5, 41: 4, 49: 4, 50: 4, 51: 4, 52: 5, 53: 5, 54: 5}.get(y, 6 if y > 54 else 3)
    dw = 3 if y < 49 else 4
    for x in range(l, r + 1):
        if f.get(x, y) in SKIN:
            continue
        f.put(x, y, 9 if x <= l + lw else (12 if x > r - dw else 11))
    if f.get(l, y) not in SKIN:
        f.put(l, y, 12)
    f.put(r, y, 15)

# fold lines (dark) with a light edge on their left, running into the flare
def line(pts, v):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            f.put(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), v)

line([(37, 42), (36, 50), (35, 54), (34, 59)], 12)
line([(36, 42), (35, 50), (34, 54), (33, 59)], 11)
line([(30, 51), (28, 55), (26, 59)], 11)
line([(40, 50), (41, 55), (42, 59)], 12)
# hem: scalloped edge + one gold heel peeking out
f.patch(18, 60, '''
    DLLLDLLMMDMMMMMDMMMMDDDDDDDDDDK
    _KKKKKKKKKKKKKKKKKKKKKKKKKKKKK_
''', {'L': 9, 'M': 11, 'D': 12, 'K': 15})
f.patch(25, 61, 'GgK', {'G': 13, 'g': 8, 'K': 15})
f.patch(24, 62, '_KK', {'K': 15})

# sequins: a few 2px clumps on the lit side
for x, y in [(34, 25), (35, 25), (35, 37), (35, 38), (36, 38), (32, 46), (32, 47), (37, 55), (38, 55),
             (27, 57), (28, 57)]:
    f.put(x, y, 14)
for x, y in [(40, 28), (40, 29), (39, 44), (39, 45), (42, 57), (43, 57)]:   # glints in the shadow
    f.put(x, y, 9)

# ---- microphone in the raised hand (replaces the Poké Ball)
f.clear(44, 17, 53, 24)
f.clear(48, 25, 53, 27)
f.patch(45, 11, '''
    .KKKK.
    KEE55K
    KE556K
    K5566K
    K6667K
    .KKKK.
    ..KGgK
    ..KAK.
    .4444.
    41112K
    41223K
    42222K
    .4334K
    ..4KAK
    ...KK
''', {'K': 15, 'G': 13, 'g': 8, 'A': 10})
# bangles: right wrist, left wrist
f.patch(45, 25, 'Gg', {'G': 13, 'g': 8})
f.patch(44, 26, 'Gg', {'G': 13, 'g': 8})
f.patch(26, 29, 'G', {'G': 13})
f.patch(26, 30, 'Gg', {'G': 13, 'g': 8})
f.patch(27, 31, 'g', {'g': 8})

# ---- hair ornament: magenta flower with gold centre, top-left of the bouffant
f.patch(23, 4, '''
    .KK.
    KBBKK
    KL9GBK
    KBgGBK
    .KBBK
    ..KK
''', {'K': 15, 'B': 11, 'L': 9, 'G': 13, 'g': 8})
# earring
f.patch(39, 17, 'G', {'G': 13})
f.patch(39, 18, 'g', {'g': 8})

res = [f.save_front(ID)]

# ---------------------------------------------------------------- OW
# reporter_f (npc_4) already sings into a mic at her chin with blue-black hair and a magenta top.
# Keep head, face, arms and mic; turn the white skirt + legs into a floor-length magenta gown.
o = load_ow('reporter_f')
K = {'P': 8, 'M': 9, 'D': 10, 'W': 14, 'K': 15}

GOWN = {  # frame: (first row, rows); '.' keeps hands/arms, '_' clears
    0: (26, '''
        ...DPPPMM..MD...
        ....DPPPMMMD....
        ....DPPMMMMD....
        ...DPPPPMMMMD...
        ...DDDDDDDDDD...'''),
    1: (26, '''
        ...DPPPPMMMD....
        ....DPPPMMMD....
        ....DPPMMMMD....
        ...DPPPPMMMMD...
        ...DDDDDDDDDD...'''),
    3: (27, '''
        ...DPPPMM..MD...
        ....DPPPMMMD....
        ...DPPPMMMMD____
        ..DPPPPMMMMD____
        ..DDDDDDDDDD____'''),
    4: (27, '''
        ...DPPPMM..MD...
        ....DPPPMMMD....
        ____DPPPMMMMD...
        ____DPPPPMMMMD..
        ____DDDDDDDDDD..'''),
    2: (25, '''
        .........MD.....
        .........MD.....
        ....DPPMMMD.....
        ....DPPMMMD.....
        ...DPPPMMMMD....
        ...DDDDDDDDD....'''),
    7: (26, '''
        .........MD.....
        .........MD_____
        ___DPPPMMMD_____
        __DPPPPMMMMD____
        _DPPPPPMMMMD____
        _DDDDDDDDDDD____'''),
    8: (26, '''
        .........MD.....
        .........MD_____
        ___DPPPMMMD_____
        ___DPPPMMMMD____
        __DPPPPPMMMMD___
        __DDDDDDDDDDD___'''),
}
# back walk frames: same sway as the front walk frames
GOWN[5] = (27, '        ...DPPPPMMMD....\n' + GOWN[3][1].split('\n', 2)[2])
GOWN[6] = (27, '        ...DPPPPMMMD....\n' + GOWN[4][1].split('\n', 2)[2])
BOB = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}
for i in range(9):
    fr = o.frame(i)
    b = BOB[i]
    # leftover white skirt greys below the mic -> gown
    if i in (0, 3, 4):
        fr.remap({11: 8, 12: 9, 13: 10, 14: 8}, (0, 25 + b, 15, 31))
    elif i in (1, 5, 6):
        fr.remap({11: 9, 12: 10, 13: 10, 14: 8}, (0, 24 + b, 15, 31))
    else:
        fr.remap({11: 9, 12: 10, 14: 9}, (5, 25 + b, 15, 31))
    # bouffant: grow the hair mass 1px outward above the face, re-outline
    top = {0: 16, 1: 19, 2: 16}[i if i < 3 else (0 if i in (3, 4) else 1 if i in (5, 6) else 2)] + b
    src = fr.copy()
    for y in range(7, top + 1):
        for x in range(16):
            if src.px[y][x] != 0:
                continue
            dirs = ((0, 1),) if y > top - 3 else ((1, 0), (-1, 0), (0, 1))
            if any(0 <= x + dx < 16 and src.px[y + dy][x + dx] in (5, 6, 7) for dx, dy in dirs):
                fr.px[y][x] = 7
    for y in range(7, top + 1):
        for x in range(16):
            if src.px[y][x] == 7 and all(fr.px[y + dy][x + dx] != 0 for dx, dy in ((1, 0), (-1, 0), (0, -1))
                                         if 0 <= x + dx < 16):
                fr.px[y][x] = 6
    o.set_frame(i, fr)
for i, (y, art) in GOWN.items():
    o.patch_frame(i, 0, y, art, K)
# hair flower (magenta, like the front pic's) on the bouffant
FLOWER = '\n'.join(['PM', 'MD'])
for i, x, y in [(0, 3, 12), (3, 3, 13), (4, 3, 13), (1, 11, 12), (5, 11, 13), (6, 11, 13),
                (2, 10, 12), (7, 10, 13), (8, 10, 13)]:
    o.patch_frame(i, x, y, FLOWER, K)

res.append(o.save_ow(ID, 'npc_4'))
compare(ID, 'beauty_frlg', 'reporter_f')
report(ID, res)
