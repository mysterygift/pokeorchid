"""HAWKER (female) - hawker-centre stall auntie. Front: pokefan_f (Wailmers and handbag removed,
tray of kopi on the raised palm). OW: pokefan_f. Matching blue bib apron with HAWKER (male).
Run from dev_scripts/trainer_classes/:  python classes/hawker_f.py"""
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


def nbrs(pic, x, y):
    return [pic.px[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if 0 <= x + dx < pic.w and 0 <= y + dy < pic.h]


# ---------------------------------------------------------------- front
f = load_front('pokefan_f')
base = f.copy()
# 5/6/8 apron blue (same as HAWKER m), A/B black perm (B also trousers), C/D/7 pink floral blouse,
# 9 light grey (tray, cup shading)
f.set_pal(5, (136, 184, 232))
f.set_pal(6, (80, 128, 192))
f.set_pal(8, (48, 72, 128))
f.set_pal(10, (112, 104, 120))
f.set_pal(11, (48, 40, 56))
f.set_pal(12, (248, 192, 208))
f.set_pal(13, (216, 136, 168))
f.set_pal(7, (160, 72, 112))
f.set_pal(9, (192, 200, 208))

# remove the Wailmers, handbag and everything below the waist (redrawn)
f.clear(0, 38, 63, 63)
f.clear(32, 36, 47, 45)

# coat -> blouse: brown fold lines inside the cloth become deep rose
for y in range(23, 38):
    for x in range(10, 42):
        if base.px[y][x] == 4 and any(n in (12, 13) for n in nbrs(base, x, y)) \
                and not any(n in (1, 2, 3) for n in nbrs(base, x, y)):
            f.put(x, y, 7)
# wrist cuff (brown) -> blouse
f.remap({11: 13, 10: 12}, (10, 27, 22, 33))

# restore the forearm the handbag strap crossed (strap -> sleeve)
f.blit(base, 32, 36, 40, 37, 32, 36, transparent=False)
f.remap({9: 12}, (36, 34, 40, 37))
f.remap({11: 13, 10: 12}, (32, 36, 40, 37))

# shirt opening -> collar (top) + bib apron (from the chest down)
for y in range(24, 38):
    for x in range(23, 32):
        v = f.px[y][x]
        if v in (9, 14):
            if y < 28:
                f.put(x, y, 12 if v == 14 else 13)
            else:
                f.put(x, y, 5 if x <= 25 else 6)
rows(f, 24, 28, ['8888888'])                      # bib top edge
for y in range(29, 38):
    f.put(24, y, 8)

# apron skirt + waist tie
for y in range(38, 52):
    L = 21 if y < 41 else 22 if y == 41 else 23 if y < 45 else 22   # vanilla coat edge + 1
    R = 37 if y < 41 else 38 if y < 46 else 39
    f.put(L - 1, y, 15); f.put(R + 1, y, 15)
    for x in range(L, R + 1):
        c = 5 if x <= L + 1 else 8 if x >= R - 1 else 6
        f.put(x, y, c)
    if y == 39:
        for x in range(L, R + 1):
            f.put(x, y, 8)
    if y >= 47:
        for fx in ((27, 33) if y < 49 else (24, 27, 33)):
            f.put(fx, y, 8); f.put(fx - 1, y, 5)
    if 42 <= y <= 45:                # front pocket, same as HAWKER (male)
        for x in range(25, 35):
            if y in (42, 45) or x in (25, 34):
                f.put(x, y, 8)
rows(f, 19, 52, ['FF888888888FF8888888FF'])   # hem: dark blue over the legs, black at the gap
# forearm bottom edge over the apron top
rows(f, 30, 38, ['CCFFFFFF'], )
key = {'k': 11, 'K': 10, 'b': 5, 'm': 6, 'd': 8}
rows(f, 24, 53, [               # legs + slippers on the vanilla legs/feet (no wider)
    'FKkkkF..FKkkF',
    'FKkkkF..FKkkF',
    'FKkkkF...F122F',
    '.FKkF...FmmmmF',
    '.F122F..F1223F',
    'FmmmmmF..FddF',
    'F11223F',
    'FdddddF',
    '.FFFFF',
], key)

# floral print: small white blossoms with a rose centre, only where the blouse is solid
flowers = [(22, 27), (35, 26), (38, 31), (17, 33), (22, 34), (35, 35), (31, 25), (14, 34), (38, 36), (26, 25)]
for fx, fy in flowers:
    pts = [(fx, fy), (fx - 1, fy), (fx + 1, fy), (fx, fy - 1), (fx, fy + 1)]
    if f.px[fy][fx] in (12, 13):
        for x, y in pts[1:]:
            if f.px[y][x] in (12, 13, 7):
                f.put(x, y, 14)
        f.put(fx, fy, 7)

# palm-up supporting hand (replaces the vanilla gesturing hand): flat palm on top, fingers
# pointing out to camera-left, thumb toward the viewer, wrist dropping into the raised sleeve
f.clear(3, 14, 19, 29)
rows(f, 8, 26, [
    '4111111112F',
    '42211111223F',
    '.443311233F',
    '...F4112F4',
    '.....F4234F',
])
# small blue tray (14px) with two kopi cups: white cup, brown kopi top, little handle
rows(f, 6, 19, [
    '.FFFFF.FFFFF..',
    '.F344F.F344F..',
    '.FEEE9FFEEE9F.',
    '..FE9F..FE9F..',
    'F555555555556F',
    'F666666666668F',
    '.FFFFFFFFFFFF.',
])

front_res = f.save_front('hawker_f')

# ---------------------------------------------------------------- OW
o = load_ow('pokefan_f')            # npc_2 -> npc_pink
o.pal = npc_pal('npc_pink')
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
for i in range(9):
    fr = o.frame(i)
    b = BOB[i]
    for y in range(32):
        for x in range(16):
            v = fr.px[y][x]
            if not v:
                continue
            if y <= 20 + b:                 # perm: brown -> near-black; eye lashes dark
                v = {11: 12, 12: 10, 13: 15, 9: 10}.get(v, v)
            elif y < 29 + b:                # pink blouse, blue apron, dark grey skirt
                v = {8: 5, 9: 6, 10: 7, 14: 8, 5: 12, 6: 13, 7: 10}.get(v, v)
            else:                           # hem + blue slippers
                v = {7: 10, 11: 9, 13: 15, 12: 15, 5: 12, 6: 13}.get(v, v)
            if i in (0, 3, 4) and 24 + b <= y <= 26 + b and 5 <= x <= 10 and v in (5, 6):
                v = 9 if x in (5, 10) else 8          # bib of the apron
            fr.px[y][x] = v
    o.set_frame(i, fr)
ow_res = o.save_ow('hawker_f', 'npc_pink')
compare('hawker_f', 'pokefan_f', 'pokefan_f')
report('hawker_f', [front_res, ow_res])
