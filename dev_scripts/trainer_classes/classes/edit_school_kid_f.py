"""EDIT: School Kid F -> Tosa primary-school uniform: white short-sleeve blouse, teal pinafore,
white socks, black shoes. Same school as edit_school_kid_m.
Front: vanilla school_kid_f; pink top -> white blouse (sleeve over the upper arm, collar), the navy
skirt becomes the pinafore (bib visible beside the arm), legs get white socks, shoes turn black.
OW: no vanilla school_kid_f OW exists, so it is a clone of girl_2 (same size as school_kid_m, long
hair, hair tie) with its OWN palette out/npc_school_kid_f.pal: caramel hair ramp from the front pic
(+ dark hair-outline slot), the front pic's teal pinafore, white blouse with light-grey shade,
orange bobble, white socks, black shoes. Needs its own OBJ palette tag in game.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kit import *

ID = 'edit_school_kid_f'

f = load_front('school_kid_f')
# pink top slots -> blouse shades
f.set_pal(5, (208, 208, 224))    # blouse shade
f.set_pal(6, (136, 136, 168))    # blouse outline / crease
# skirt ramp -> teal pinafore (vanilla two-tone kept)
f.set_pal(7, (120, 192, 200))
f.set_pal(8, (64, 144, 160))
f.set_pal(9, (32, 88, 112))

# blouse + pinafore bib. The near arm crosses the body from the right shoulder (x30-33) down-left
# to the bag: its upper part gets a white short sleeve; the chest left of it gets the teal bib with
# the white blouse/collar above; the torso side below the armpit is pinafore in shadow.
f.patch(25, 31, '''
    ...4F3EE5F.
    ..6E56EE56.
    ..9786EE5F.
    ...786E55F.
    ...86556F..
    ........8..
    .......8...
    ......8....
    .....89....
    ....88.8...
''')
# pinafore skirt lengthened 2px towards the knee (school length), shadow on the legs below the hem
f.patch(27, 49, '''
    F999988889F
    F99998889F
    _4333F3F__
''')
f.put(34, 48, 8)
# white socks (folded cuff) and black shoes on the standing leg
f.patch(29, 57, '''
    .6EE6
    .6E5F
    .6E55F
    .6EE56
    F9899F
    F9FFFF
    .FFFF.
''')
res_f = f.save_front(ID)

# ---------------------------------------------------------------- OW (girl_2 clone, own palette)
v = load_ow('girl_2')            # vanilla is on npc_3; indices kept, palette replaced below
o = v.copy()
P, p, Q, K, W, w = 9, 10, 8, 15, 14, 5   # pinafore mid/dark/light, black, white, blouse shade
for fr in range(9):
    b = 0 if fr < 3 else 1
    for y in range(32):
        for x in range(fr * 16, fr * 16 + 16):
            c = v.px[y][x]
            if c == 5: o.px[y][x] = P          # lavender dress -> green pinafore
            elif c == 6: o.px[y][x] = p
            elif c == 7: o.px[y][x] = K
            elif c in (8, 9, 10):
                if y <= 19 + b:                 # hair tie -> orange bobble (own slot 6), black elastic ring
                    o.px[y][x] = 6 if c in (8, 9) else K
                elif y >= 28 + b:               # shoes
                    o.px[y][x] = K
                else:                           # green collar/bow -> pinafore bib
                    o.px[y][x] = {8: P, 9: P, 10: p}[c]
# uniform rows per frame ('.' keeps the mapped pixel): white blouse shoulders + collar (lavender
# shade, neck shadow kept), white blouse peeking beside the bib, upper-left pinafore highlight,
# white socks on the legs, black shoes. Back views show white shoulders with the pinafore straps.
ROWS = {
    0: {23: 'DDFEEE5445EEEFDD', 24: '.4224E9999E4224.', 26: '..44A999999A44..',
        29: '....FEEFFE5F....'},
    1: {25: '.43FE9EEEE9EF34.', 29: '....FEEFFE5F....'},
    2: {23: '.....44EEFFDDDDD', 24: '....FEE54AFFF...', 29: '.....FEE5EE5F...'},
    3: {24: '.DFEEE5445EEFD..', 25: '..44FE9999E44...', 27: '..FAA9999A4334..',
        30: '.....FEEF.......'},
    4: {24: '..DFEE5445EEEFD.', 25: '...44E9999EF44..', 27: '..4334A999AAAF..',
        30: '.......FEEF.....'},
    5: {26: '...FE9EE9EF224..', 30: '.....FEEF.......'},
    6: {26: '..422FE9EE9EF...', 30: '.......FEEF.....'},
    7: {24: '.....44EEFFDDD..', 25: '....AEE544FF....', 29: '...FFE999AAFF...',
        30: '....FFEAAAFF....'},
    8: {24: '.....44EEFFDDD..', 25: '....AEE549AF....', 30: '....FFFAA9EFF...'},
}
for fr, rows in ROWS.items():
    for y, row in rows.items():
        o.patch_frame(fr, 0, y, row)
# own OBJ palette (cloned NPC, matches the front pic): shared skin 1-4 / white / black, blouse grey,
# orange bobble, caramel hair ramp sampled from the front pic, the front pic's teal pinafore ramp.
# The vanilla hair is mostly its darkest tone, so the ramp is shifted one step lighter and the
# silhouette edge of the hair gets its own dark-brown outline slot (7).
PAL = [BG] + npc_pal('npc_3')[1:5] + [
    (208, 208, 216),   # 5 blouse / sock shade (light grey)
    (232, 88, 48),     # 6 orange bobble
    (96, 56, 24),      # 7 hair outline
    (120, 192, 200),   # 8 teal light
    (64, 144, 160),    # 9 teal (pinafore)
    (32, 88, 112),     # A teal dark
    (232, 176, 104),   # B hair highlight
    (200, 136, 64),    # C hair caramel (front pic mid)
    (152, 96, 40),     # D hair base
    (255, 255, 255), (0, 0, 0)]
src = o.copy()
for fr in range(9):
    for y in range(32):
        for x in range(fr * 16, fr * 16 + 16):
            if src.px[y][x] == 13:
                fx = x - fr * 16
                if any(not (0 <= fx + dx < 16 and 0 <= y + dy < 32) or src.px[y + dy][x + dx] == 0
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    o.px[y][x] = 7
o.pal = PAL
write_jasc(os.path.join(OUT, 'npc_school_kid_f.pal'), PAL)
res_o = o.save_ow(ID, 'npc_school_kid_f')
compare(ID, 'school_kid_f', 'girl_2')
report(ID, [res_f, res_o])
