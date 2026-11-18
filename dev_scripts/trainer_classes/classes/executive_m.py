"""EXECUTIVE (male) - CBD office worker on lunch break: short-sleeved shirt, tie, ID lanyard, slacks,
iced kopi in a plastic takeaway bag with a string handle.
Front: cooltrainer_m (Poke Ball toss -> dangling kopi bag). OW: devon_employee.
Run from dev_scripts/trainer_classes/:  python classes/executive_m.py"""
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
f = load_front('cooltrainer_m')
base = f.copy()
# 9/B/A hair -> black; jacket ramp 5/6/7/8 + trim C/D -> white shirt (E/5/6), charcoal slacks (7/8);
# C red tie, D lanyard blue, 8 iced kopi
f.set_pal(9, (24, 24, 40))
f.set_pal(11, (56, 56, 72))
f.set_pal(10, (96, 96, 120))

# torso / arms (y < 37) -> shirt; legs (y >= 37) -> slacks. Do it by region before repaletting.
SHIRT = {5: 14, 6: 14, 7: 5, 8: 6, 12: 14, 13: 5}
SLACKS = {5: 7, 6: 7, 7: 11, 8: 11, 12: 7, 13: 11}
for y in range(64):
    for x in range(64):
        v = base.px[y][x]
        if v in SHIRT:
            if y < 36 or (y < 38 and x < 33 and v != 13):
                f.px[y][x] = SHIRT[v]
            else:
                f.px[y][x] = SLACKS[v]
f.set_pal(5, (208, 216, 232))   # shirt shade
f.set_pal(6, (144, 152, 184))   # shirt deep shade / outline on white
f.set_pal(7, (104, 104, 120))   # slacks
f.set_pal(8, (208, 136, 72))    # iced kopi (slacks shadow shares hair slot B)
f.set_pal(12, (200, 48, 64))    # tie (the kopi uses the skin ramp 2/3/4 + white plastic)
f.set_pal(13, (64, 104, 200))   # lanyard

# no more Poke Ball toss
f.clear(36, 15, 43, 22)

# short sleeves: hanging arm gets a bare forearm and fist, raised arm a bare wrist
# vanilla shoulder/upper-arm silhouette kept; sleeve hem mid-upper-arm (y26); bare arm below is
# 1px slimmer per side than the vanilla sleeved forearm (x21-26), ending in a small hand at the hip
rows(f, 21, 26, [
    '.66666',
    '_F1124',
    '_F1124',
    '_F1234_',
    '_F124_',
    '_F124_',
    '_F124_',
    '_F1234',
    '_F1234',
    '._F44F',
])
f.remap({14: 2, 5: 3, 6: 4}, (34, 30, 38, 33))

# belt where the shirt tucks into the slacks
for x in range(22, 36):
    if f.px[36][x] not in (0, 15) and x > 26:
        f.put(x, 36, 9)

# tie down the shirt front (knot at the collar), over whatever the jacket zip left there
f.remap({4: 5}, (28, 19, 31, 33))
rows(f, 28, 20, [
    '.CC',
    '.CC',
    'CCC',
    'CCC',
    'CCC',
    'CCC',
    'CCC',
    'CCC',
    'CCC',
    'CCC',
    '.C6',
    '.6.',
])

# ID lanyard: blue straps down both sides of the tie to a card hanging over it (on the torso,
# clear of the hanging arm)
rows(f, 27, 21, [
    'D...D',
    'D...D',
    'D...D',
    'D...D',
    'D...D',
    '6DDD6',
    '6E3E6',
    '6EEE6',
    '66666',
])

# iced kopi in a plastic bag hanging by its string from the raised hand (red straw, ice cubes)
rows(f, 41, 25, [
    '.....C..',
    '.....C..',
    '.66..C..',
    '...6FC..',
    '...FEF..',
    '..FEEF..',
    '.FE55EF.',
    '.FE888F.',
    'FE88888F',
    'FE88884F',
    'FE88884F',
    'F888844F',
    'F888844F',
    '.F8844F.',
    '..FFFF..',
])

# tame the spikes: rounder, neater office cut (keep fringe, face and back of head)
f.clear(19, 1, 37, 5)
f.remap({9: 10}, (26, 6, 28, 6))
f.clear(34, 6, 36, 6)
rows(f, 19, 4, [
    '....FFFFFFFFFFF...',
    '...FBAAAAAAAAAAF..',
    '..FB.............F',
])
f.put(35, 6, 15); f.put(34, 6, 11)
f.put(20, 7, 15)

front_res = f.save_front('executive_m')

# ---------------------------------------------------------------- OW
o = load_ow('devon_employee')        # npc_2 -> npc_white
o.pal = npc_pal('npc_white')
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
FRONT, BACK, SIDE = (0, 3, 4), (1, 5, 6), (2, 7, 8)
BAG = [            # iced kopi bag hanging under the hand: knot, string-tied neck, liquid
    '.E.',
    'F5F',
    'E55',
    'F56',
    '.F.',
]


def hand(fr, cols, y0):
    """Lowest skin pixel (2/3) in the given columns below row y0 -> (x, y)."""
    best = None
    for y in range(y0, 32):
        for x in cols:
            if fr.px[y][x] in (2, 3):
                best = (x, y)
    return best


def edge(fr, x, y):
    return any(not (0 <= x + dx < 16 and 0 <= y + dy < 32) or fr.px[y + dy][x + dx] == 0
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


for i in range(9):
    fr = o.frame(i)
    src = fr.copy()
    b = BOB[i]
    for y in range(32):
        for x in range(16):
            v = fr.px[y][x]
            if not v:
                continue
            if y <= 20 + b:                                  # hair -> black-grey
                v = {11: 12, 12: 13, 13: 15 if edge(src, x, y) else 7}.get(v, v)
            elif y <= 26 + b:                                # jacket off: white short-sleeved shirt
                v = {8: 14, 9: 14, 10: 12 if edge(src, x, y) else 11, 6: 8, 7: 9}.get(v, v)
            else:                                            # charcoal slacks, black shoes
                v = {8: 12, 9: 12, 10: 13, 12: 7, 13: 15, 11: 13}.get(v, v)
            fr.px[y][x] = v
    if i in FRONT:                                           # lanyard straps + ID card
        for (x, y, c) in ((5, 23, 13), (6, 24, 13), (10, 23, 13), (9, 24, 13), (9, 25, 12)):
            if fr.px[y + b][x] not in (0, 2, 3, 4):
                fr.px[y + b][x] = c
    cols = (12, 13, 14, 15) if i in FRONT else (0, 1, 2, 3) if i in BACK else range(3, 11)
    h = hand(fr, cols, 22 + b)
    if h:
        hx, hy = h
        hx = min(hx, 14)
        for dy, line in enumerate(BAG):
            for dx, ch in enumerate(line):
                if ch != '.' and 0 <= hx - 1 + dx < 16 and hy + 1 + dy < 32:
                    fr.px[hy + 1 + dy][hx - 1 + dx] = HEX.index(ch)
    o.set_frame(i, fr)
ow_res = o.save_ow('executive_m', 'npc_white')
compare('executive_m', 'cooltrainer_m', 'devon_employee')
report('executive_m', [front_res, ow_res])
