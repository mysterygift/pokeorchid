"""DELIVERY RIDER (male) - food-delivery cyclist with a square insulated backpack.
Front: cycling_triathlete_m (helmet + bike kept). OW: youngster.
Brand: original "orchid purple" box/jersey with an orange-and-white bowl logo.
Run from dev_scripts/trainer_classes/:  python classes/delivery_m.py"""
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
f = load_front('cycling_triathlete_m')
base = f.copy()
# blue ramp 7/8/9/A -> brand purple (helmet, jersey, box, shoes); B/C orange-red stay (bike, logo)
f.set_pal(10, (224, 208, 255))
f.set_pal(7, (184, 144, 240))
f.set_pal(8, (136, 96, 208))
f.set_pal(9, (96, 56, 160))

# black cycling shorts (were red)
f.remap({11: 5, 12: 4, 13: 4, 10: 6}, (40, 22, 50, 33))

# phone instead of the Poke Ball in the outstretched fist
f.clear(7, 16, 10, 22)
rows(f, 6, 10, [
    'FFFFF',
    'FEEAF',
    'FEAAF',
    'FA77F',
    'FBB7F',
    'FA77F',
    'FAA7F2',
    'F9993',
    '.FFF4',
    '....4',
    '....4',
    '....4',
])

# square insulated delivery box strapped to his back, drawn as a cube in the rider's 3/4 view and
# composited BEHIND him (only into empty pixels): narrow forward face on the left (lit, toward
# camera-left), wide side face toward the viewer with the bowl logo skewed along its perspective,
# top face above. Edges recede: side face rises 1px per 4px to the right, forward face 1px per 2px.
def in_poly(px, py, poly):
    sign = 0
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        c = (x1 - x0) * (py - y0) - (y1 - y0) * (px - x0)
        if c:
            if sign and (c > 0) != (sign > 0):
                return False
            sign = c
    return True


NX, TOP, BOT = 41.5, 9.0, 26.5                 # near vertical edge (x) and its top/bottom (y)
SW, FW = 11.0, 4.5                             # side-face width, forward-face width
A, A2 = (NX, TOP), (NX, BOT)
R, R2 = (NX + SW, TOP - SW / 4), (NX + SW, BOT - SW / 4)
L, L2 = (NX - FW, TOP - FW / 2), (NX - FW, BOT - FW / 2)
FAR = (R[0] + L[0] - A[0], R[1] + L[1] - A[1])
FACES = [([A, R, R2, A2], 8), ([L, A, A2, L2], 7), ([A, L, FAR, R], 10)]
box = {}
for y in range(64):
    for x in range(64):
        for poly, c in FACES:
            if in_poly(x + 0.5, y + 0.5, poly):
                box[(x, y)] = c
                break


def side_top(x):                               # first side-face row in column x
    return min(y for (bx, y), c in box.items() if bx == x and c == 8)


LOGO = [               # bowl + chopsticks on the side face; right half 1px higher (face skew)
    '......EE',
    '.....EE.',
    '...EEEEE',
    'EEEEBBBE',
    'EBBBBBE.',
    '.EBBBE..',
    '..EEE...',
]
for v, line in enumerate(LOGO):
    for u, ch in enumerate(line):
        if ch != '.' and (43 + u, 10 + v) in box:
            box[(43 + u, 10 + v)] = HEX.index(ch)
# outline the cube, darker seam where the side face meets the forward face
for (x, y) in list(box):
    if any((x + dx, y + dy) not in box for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        box[(x, y)] = 15
    elif x == int(NX) and box[(x, y)] in (7, 8):
        box[(x, y)] = 9
for (x, y), c in box.items():
    if f.px[y][x] == 0:                        # the rider stays in front of the box
        f.put(x, y, c)
# shoulder strap over the upper arm
rows(f, 37, 15, [
    '....4F',
    '...44F',
    '..44F',
    '.44F',
])

front_res = f.save_front('delivery_m')

# ---------------------------------------------------------------- OW
o = load_ow('youngster')            # npc_1 -> npc_blue (8-A purple, B-D orange-red)
o.pal = npc_pal('npc_blue')
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
FRONT, BACK, SIDE = (0, 3, 4), (1, 5, 6), (2, 7, 8)
BOX_BACK = [          # back face of the box (no logo): lid band on top, zip seam, shaded base
    '.FFFFFFFF.',
    'F88888888F',
    'FAAAAAAAAF',
    'F99999999F',
    'F99999999F',
    'F99999999F',
    'F99999999F',
    'FA999999AF',
    '.FFFFFFFF.',
]
BOX_SIDE = [
    '.FFFFF',          # side face with the bowl logo (chopstick, rim, orange bowl, foot)
    'F8888F',
    'F999EF',
    'FEEEEF',
    'FEBBEF',
    'F9EE9F',
    'F9999F',
    'FA99AF',
    '.FFFF.',
]
for i in range(9):
    fr = o.frame(i)
    src = fr.copy()
    b = BOB[i]
    for y in range(32):
        for x in range(16):
            v = fr.px[y][x]
            if not v:
                continue
            if y <= 18 + b:                          # helmet: cap brim -> shell, hair stays dark
                v = {12: 9, 11: 8}.get(v, v)
            elif y <= 28 + b:                        # white tee -> purple jersey, navy shorts -> black
                v = {14: 8, 8: 9, 9: 10}.get(v, v)
            else:                                    # orange-red trainers
                v = {12: 12, 11: 11}.get(v, v)
            fr.px[y][x] = v
    # white vent stripe along the helmet
    if i in FRONT or i in BACK:
        for y in (13 + b, 14 + b, 15 + b):
            fr.px[y][7] = fr.px[y][8] = 14 if fr.px[y][7] in (8, 9) else fr.px[y][7]
    else:
        for y in (13 + b, 14 + b):
            if fr.px[y][8] in (8, 9):
                fr.px[y][8] = 14
    if i in FRONT:                                   # backpack straps over the shoulders
        for y in range(23 + b, 27 + b):
            for x in (5, 10):
                if fr.px[y][x] in (8, 9):
                    fr.px[y][x] = 10
    if i in BACK:
        for dy, line in enumerate(BOX_BACK):
            for dx, ch in enumerate(line):
                if ch != '.':
                    fr.px[19 + b + dy][3 + dx] = HEX.index(ch)
    if i in SIDE:
        for y in (18 + b, 19 + b):                   # drop the cap's back strap
            for x in range(12, 16):
                if src.px[y][x] in (14, 10) and x >= 13:
                    fr.px[y][x] = 0
                    src.px[y][x] = 0
        for dy, line in enumerate(BOX_SIDE):
            for dx, ch in enumerate(line):
                y, x = 19 + b + dy, 10 + dx
                if ch == '.' or x > 15:
                    continue
                under = src.px[y][x]
                if y <= 21 + b and under:            # head stays in front of the box
                    continue
                if under in (1, 2, 3):               # so does the arm
                    continue
                fr.px[y][x] = HEX.index(ch)
    o.set_frame(i, fr)
ow_res = o.save_ow('delivery_m', 'npc_blue')
compare('delivery_m', 'cycling_triathlete_m', 'youngster')
report('delivery_m', [front_res, ow_res])
