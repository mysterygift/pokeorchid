"""HAWKER (male) - hawker-centre stall uncle. Front: sailor (flex pose). OW: fat_man.
Run from dev_scripts/trainer_classes/:  python classes/hawker_m.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *


def rows(pic, x, y, lines, key=None):
    """One string per row, each starting at column x. '.'/' ' keep, '_' clear, hex = index."""
    key = key or {}
    for i, s in enumerate(lines):
        for j, ch in enumerate(s):
            if ch in ' .':
                continue
            v = 0 if ch == '_' else key[ch] if ch in key else HEX.index(ch)
            pic.put(x + j, y + i, v)


# ---------------------------------------------------------------- front
f = load_front('sailor')
base = load_front('sailor')
# palette: skin (slightly tanned), white singlet ramp E/9/5/A, blue apron B/6/7,
# red C/D (towel stripe, slippers), 8 dark grey (hair, shorts)
f.set_pal(1, (248, 216, 192))
f.set_pal(2, (232, 176, 136))
f.set_pal(3, (192, 128, 96))
f.set_pal(4, (104, 64, 64))
f.set_pal(6, (80, 128, 192))   # apron mid
f.set_pal(7, (48, 72, 128))    # apron dark
f.set_pal(11, (136, 184, 232))  # apron light
f.set_pal(8, (56, 56, 64))     # hair / shorts

# --- head: replace sailor cap with a short black crew cut, grey at the temple
f.remap({6: 8}, (28, 9, 38, 12))   # blue irises -> dark (slot 6 becomes apron blue)
f.clear(26, 0, 47, 8)
rows(f, 27, 2, [
    '......FFFFFFF......',
    '....FF8888888FF....',
    '...F8AA88888888F...',
    '..F8AA8888888888F..',
    '.F8AA888888888888F.',
    '.F8A1111222388888F.',
    '.F8211111122238888F',
])
rows(f, 28, 9, ['43'])
rows(f, 28, 10, ['4'])
rows(f, 40, 9, [
    '88888F',
    '83224F',
    '82143F',
    '3213F',
])

# --- spatula in the raised fist: steel blade top-left, dark handle into the fist
rows(f, 1, 1, [
    'FFFFFFF..............',
    'FEEEEE9F.............',
    'FEEEEEE5F............',
    'F9EEEEE55F...........',
    'F99EEE9555F..........',
    '.F9999555AF..........',
    '..FF5555AF...........',
    '....FFF5AFF..........',
'.........FA8FFF......',
    '..........FF888FFF...',
    '............FFF888F..',
    '...............FFF...',
])

# --- towel round the neck (was the sailor collar): white, red stripe near the hanging end
f.remap({14: 2, 5: 3, 9: 2}, (32, 20, 35, 24))     # undershirt V -> bare chest
f.remap({13: 5, 12: 9}, (26, 20, 38, 26))          # neckerchief knot -> towel folds
f.remap({6: 14, 11: 14, 7: 5}, (26, 16, 50, 31))
rows(f, 44, 23, ['FCCF', 'FDDDF'])

# --- singlet + bib apron + shorts, painted inside the vanilla sailor's silhouette (same 3/4 turn):
# the front centre line runs down x30 (vanilla fly/crotch), the side plane is x41-45, the far
# (viewer-right) leg is the vanilla right trouser leg.
CX = 30                         # torso front centre line
SIDE = 41                       # first column of the turned side plane
mask = [[base.px[y][x] != 0 for x in range(64)] for y in range(64)]


def inside(x, y):
    return 0 <= x < 64 and 0 <= y < 64 and mask[y][x]


def is_edge(x, y):
    return any(not inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


f.clear(18, 33, 48, 62)
for y in range(33, 54):
    for x in range(18, 49):
        if not inside(x, y):
            continue
        if y == 33 and x <= 23:                 # bottom of the flexed arm (vanilla outline)
            c = 15
        elif is_edge(x, y):
            c = 15
        elif y <= 40:                           # singlet with the bib over the front centre
            if CX - 6 <= x <= CX + 6:
                c = 7 if x in (CX - 6, CX + 6) else 11 if x <= CX - 4 else 6
            elif x < CX - 6:
                c = 10 if x == 21 else 14
            else:
                c = 14 if x < SIDE - 2 else 9 if x < 44 else 5
        elif y == 41:                           # apron ties round the waist
            c = 7
        elif y <= 50 and x <= SIDE - 1:         # apron front panel (stops where the side turns)
            if x == SIDE - 1 or y == 50:
                c = 7
            elif x <= 23:
                c = 11
            elif x >= SIDE - 3:
                c = 7 if x == SIDE - 2 else 6
            else:
                c = 6
        else:                                   # dark shorts: hip side + both legs under the hem
            c = 10 if (x == 22 and y > 50) or (x == 35 and y > 50) else 8
            if y == 53:
                c = 15
        f.put(x, y, c)
# apron details on the turned centre line: pocket, centre crease, side folds
for y in range(43, 47):
    for x in range(CX - 5, CX + 6):
        if y in (43, 46) or x in (CX - 5, CX + 5):
            f.put(x, y, 7)
for y in range(47, 50):
    for fx in ((CX,) if y < 48 else (CX - 5, CX, CX + 6)):
        f.put(fx, y, 7); f.put(fx - 1, y, 11 if fx < CX + 6 else 6)
f.put(32, 50, 15); f.put(33, 50, 15); f.put(34, 50, 15)    # hem over the crotch gap

# bare shins + red rubber slippers on the vanilla feet: near foot points camera-left like the
# vanilla shoe, far foot toward the viewer
key = {'r': 12, 'R': 13}
rows(f, 21, 54, [
    '..F112233F.......F112233F',
    '..F112233F.......F112233F',
    '..F112233F.......F122334F',
    '..F122334F.......F122334F',
    '...F12234F.......F122334F',
    'FrrrrRR23F.......F12234F',
    'F11222233F......FrrrrrRRF',
    'FRRRRRRRRF......F1122233F',
    '.................FRRRRRRF',
], key)

front_res = f.save_front('hawker_m')

# ---------------------------------------------------------------- OW
# fat_man (npc_1) -> npc_pink: blue ramp 8-A stays the apron, pink 5-7 slippers,
# grey B-D for hair, singlet shading and shorts.
o = load_ow('fat_man')
o.pal = npc_pal('npc_pink')
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
FRONT, BACK, SIDE = (0, 3, 4), (1, 5, 6), (2, 7, 8)


def ow_frame(i):
    fr = o.frame(i)
    b = BOB[i]
    neck, belt = 20 + b, 26 + b
    for y in range(32):
        for x in range(16):
            v = fr.px[y][x]
            if v == 0:
                continue
            if y < neck or (i in BACK and y < neck + 1):           # hair: olive -> dark grey
                v = {11: 12, 12: 13, 13: 10, 9: 11, 8: 14}.get(v, v)
            elif y < neck + 3 or (y == neck + 3 and i in FRONT and not 5 <= x <= 10):  # singlet + bib top
                bib = i in FRONT and 5 <= x <= 10 and y > neck
                if not bib:
                    v = {8: 14, 9: 11, 10: 13}.get(v, v)
                if i in FRONT and y == neck and v == 3 and 5 <= x <= 10:
                    v = 14 if x < 9 else 11                        # towel round the neck
            elif y < belt + 3:                                     # apron over the shorts
                front_panel = (i in FRONT and 3 <= x <= 12) or (i in SIDE and x <= 6)
                if i in BACK:
                    v = {8: 14, 9: 11, 10: 13}.get(v, v)
                    if y == belt:
                        v = {9: 9, 12: 9, 13: 10, 14: 9, 11: 9}.get(v, v)
                elif i in SIDE and x > 6:
                    v = {8: 14, 9: 11, 10: 13}.get(v, v)
                if front_panel and y >= belt:
                    v = {5: 8, 6: 8, 7: 9, 12: 9, 13: 10}.get(v, v)
                    if y == belt + 2:
                        v = {8: 9}.get(v, v)
                elif i in BACK or not front_panel:
                    v = {5: 11, 6: 12, 7: 13, 12: 12, 13: 13}.get(v, v)
                else:
                    v = {12: 9, 13: 10}.get(v, v)
            else:                                                  # bare feet in pink slippers
                sole = y + 1 < 32 and fr.px[y + 1][x] == 0
                v = ({13: 7, 7: 6, 6: 6} if sole else {13: 4, 7: 3, 6: 2, 5: 2})[v] if v in (5, 6, 7, 13) else v
            fr.px[y][x] = v
    return fr


for i in range(9):
    o.set_frame(i, ow_frame(i))

ow_res = o.save_ow('hawker_m', 'npc_pink')
compare('hawker_m', 'sailor', 'fat_man')
report('hawker_m', [front_res, ow_res])
