"""NYONYA (nyonya_f): Peranakan lady in kebaya + batik sarong, sanggul bun, holding a tingkat.
Front: aroma_lady (RSE) pose/face. OW: woman_2 (bun at the back) on npc_pink.
Run from dev_scripts/trainer_classes: python classes/nyonya_f.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

ID = 'nyonya_f'

# ------------------------------------------------------------------ front
f = load_front('aroma_lady')
T = 100  # temp index base for safe remaps

# clear the green sparkles (slots 9/E) outside the figure
for y in range(64):
    for x in range(64):
        if f.px[y][x] in (9, 14):
            # sparkles drawn over the sleeve become sleeve shade, the rest transparent
            f.px[y][x] = 13 if (33 <= x <= 38 and 28 <= y <= 30) else 0

# hair: 3-highlights in the hair mass become the blue-grey sheen (E)
for y in range(6, 13):
    for x in range(18, 38):
        if f.px[y][x] == 3 and not (24 <= x <= 31 and y >= 12):
            f.px[y][x] = T + 14
f.remap({T + 14: 14})

# kebaya: top C/D -> light/shade, its brown outline B -> mauve E
reg_top = (22, 22, 41, 36)
f.remap({12: T + 5, 13: T + 6}, reg_top)
f.remap({11: T + 14}, (23, 23, 37, 34))
f.remap({T + 5: 5, T + 6: 6, T + 14: 14})
f.remap({12: 7}, (26, 19, 31, 21))          # open mouth: pink tongue instead of gold
f.remap({6: 5}, (24, 23, 32, 29))           # pale kebaya: lit front, shade only on the right arm
f.remap({4: 14}, (33, 25, 34, 28))          # arm/torso fold in kebaya outline colour

# keep the slipper, then clear skirt/leg/ball: a slim ankle-length batik sarong replaces them
shoe = f.copy()
f.clear(20, 33, 47, 62)
f.blit(shoe, 28, 60, 35, 62, 28, 60)
f.remap({12: 7}, (28, 60, 35, 62))          # beaded slipper: pink with deep-pink sole


def L(y):
    return 29 if y <= 34 else 28 if y <= 41 else 27 if y <= 50 else 26


def R(y):
    return 39 if y <= 47 else 38 if y <= 51 else 39


for y in range(33, 59):
    l, r = L(y), R(y)
    f.put(l, y, 15)
    f.put(r, y, 15)
    for x in range(l + 1, r):
        f.put(x, y, 9 if x >= r - 2 else 8)
for x in range(L(59), R(58) + 1):
    f.put(x, 59, 15)
# front wrap: the overlapping edge runs down the front and the cloth flares a little at the hem
for y in range(44, 56):
    f.put(32 - (y - 44) // 6, y, 9)
# flower clumps (pink with deep-pink shade), staggered
FLOWERS = [(29, 41), (34, 43), (29, 47), (34, 49), (28, 52), (33, 53)]
for x, y in FLOWERS:
    f.patch(x, y, '''
        77
        7D
        ''')
# hem border: dark band + pink tumpal teeth
for x in range(L(56) + 1, R(56)):
    f.put(x, 56, 9)
    f.put(x, 57, 7 if (x % 3) else 13)
    f.put(x, 58, 9)

# kebaya hem (embroidered, dipping to a front point), right cuff, fist and the tingkat
f.patch(26, 30, '''
    ....E55566E77F
    .....F55566ED3F
    .....F55566EF23F
    ....F555566EF223F
    ...F55555666F323F
    ..F555556666EF44F
    ..F77D55666EFCFFCF
    ..F8877566EFCF..FCF
    ..F888775DFCFFFFFFCF
    ..F88887D9FC555566CF
    ..........FCDDDDDDCF
    ..........FC577566CF
    ..........FC55566ECF
    ..........FCDDDDDDCF
    ..........FC577566CF
    ..........FC55566ECF
    ..........FCDDDDDDCF
    ..........FC577566CF
    ..........FC55566ECF
    ...........FFFFFFFF
    ''')
# kerosang: three gold brooches down the front
for x, y in [(31, 25), (32, 28), (33, 31)]:
    f.put(x, y, 12)
    f.put(x + 1, y, 12)
    f.put(x + 1, y + 1, 4)

# hair sheen: keep only clumped highlights, isolated ones read as dirt
for y in range(6, 16):
    for x in range(18, 36):
        if f.px[y][x] == 14 and not any(f.px[y + dy][x + dx] == 14 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            f.px[y][x] = 10
f.put(40, 12, 0)                            # sparkle leftovers
f.put(48, 18, 0)
# left sleeve cuff embroidery
f.patch(27, 28, '77D')
# sanggul: loose side hair cut at the ear, bun at the back (right) with a gold pin
f.patch(21, 19, '''
    __
    ___
    ____F
    __F55
    _F555
    .F55
    ..E
    ''')
f.patch(35, 9, '''
    ......FF
    .....FCCF
    ....FCFF
    ..FFCF
    .BAECF
    BBEEAF
    BAAABBF
    BBBBBBF
    BBBBBF
    BFFFF
    F
    ''')

PAL = {
    0: BG,
    1: (255, 216, 176), 2: (240, 192, 144), 3: (208, 152, 112), 4: (120, 80, 64),
    5: (248, 240, 240), 6: (216, 192, 208),        # kebaya
    7: (232, 104, 144),                             # pink accent (embroidery, flowers, tingkat)
    8: (56, 144, 160), 9: (24, 80, 104),           # batik sarong ground / shade
    10: (64, 64, 88), 11: (32, 32, 48),           # black hair
    12: (240, 192, 72),                             # gold (kerosang, hairpin, tingkat frame)
    13: (176, 48, 96),                              # deep pink (embroidery shade, slippers)
    14: (136, 120, 152),                            # mauve: kebaya outline + hair sheen
    15: (0, 0, 0),
}
for k, v in PAL.items():
    f.set_pal(k, v)

if __name__ == '__main__' and 'dump' in sys.argv:
    print(f.dump(14, 4, 50, 63))

res = [f.save_front(ID)]

# ------------------------------------------------------------------ overworld
# woman_2 (npc_3) gives the head, face and the bun at the back; hair goes black (npc_4-style:
# F outline, A main, D sheen), side hair is pinned up, and the body is redrawn as a long-sleeved
# white kebaya (pink embroidered hem, front point) over a blue batik sarong with pink motifs.
base = load_ow('woman_2')
o = blank_ow('npc_pink')
HAIR = {12: 10, 11: 13, 13: 15}  # npc_3 brown hair C/B/D -> A/D/F
for y in range(32):
    for x in range(144):
        v = base.px[y][x]
        o.px[y][x] = HAIR.get(v, v) if v in (1, 2, 3, 4, 15, 0, 11, 12, 13) else 0

# Rows written per frame from `top` down (everything below is cleared). Walk frames repeat the
# stand frame 1px lower with one hand raised, the other lowered and a slipper peeking out.
FRONT = {
    0: (19, """
..4332F22F2334..
...4332222334...
..DEEC3333CEBD..
.DEEEEC33CEEBBD.
.DEECEEEEEBCBBD.
.D66CEEEEEBC66D.
433DEEEEEEBBD334
.44A66EEEB66A44.
...A996EB699A...
...A55966999A...
...A99995599A...
....AAAAAAAA....
"""),
    3: (20, """
..4332F22F2334..
...4332222334...
..DEEC3333CEBD..
.DEEEEC33CEEBBD.
.436CEEEEEBCBBD.
.44DEEEEEEBC66D.
...DEEEEEEBBD334
...A66EEEB66A44.
...A996EB699A...
...A55966999A...
...A99995599A...
....A77AAAAA....
"""),
    4: (20, """
..4332F22F2334..
...4332222334...
..DEEC3333CEBD..
.DEEEEC33CEEBBD.
.DEECEEEEEBC634.
.D66CEEEEEEBD44.
433DEEEEEEBBD...
.44A66EEEB66A...
...A996EB699A...
...A55966999A...
...A99995599A...
....AAAAA77A....
"""),
}
BACK = {
    1: (16, """
..FAAFDDAAFAAF..
.4FAAFDAAAFAAF4.
.4FAAAFFFFAAAF4.
..FFAAAAAAAAFF..
...FFA4334AFF...
..DEEEEEEEEBBD..
.DEEEEEEEEEEBBD.
.DEECEEEEEBCBBD.
.D66CEEEEEBC66D.
433DEEEEEEBBD334
.44A66666666A44.
...A99999999A...
...A55999999A...
...A99995599A...
....AAAAAAAA....
"""),
    5: (17, """
..FAAFDDAAFAAF..
.4FAAFDAAAFAAF4.
.4FAAAFFFFAAAF4.
..FFAAAAAAAAFF..
...FFA4334AFF...
..DEEEEEEEEBBD..
.DEEEEEEEEEEBBD.
.436CEEEEEBCBBD.
.44DEEEEEEBC66D.
...DEEEEEEBBD334
...A66666666A44.
...A99999999A...
...A55999999A...
...A99995599A...
....A77AAAAA....
"""),
    6: (17, """
..FAAFDDAAFAAF..
.4FAAFDAAAFAAF4.
.4FAAAFFFFAAAF4.
..FFAAAAAAAAFF..
...FFA4334AFF...
..DEEEEEEEEBBD..
.DEEEEEEEEEEBBD.
.DEECEEEEEBC634.
.D66CEEEEEEBD44.
433DEEEEEEBBD...
.44A66666666A...
...A99999999A...
...A55999999A...
...A99995599A...
....AAAAA77A....
"""),
}
SIDE = {
    2: (15, """
..FFFAAAAAAAAFF.
..411FFAAAAAFDDF
..41111FAAAAFAAF
..411F13FFFFAAAF
..422F23423FFFF.
...433334234F...
....443334FEBD..
.....44DEEEEBD..
....DECEEBCBD...
....DECEEBCBD...
....DEC66BCBD...
....D6643466D...
....A6944999A...
....A5599999A...
....A9999559A...
.....A77AAAA....
"""),
    7: (16, """
..FFFAAAAAAAAFF.
..411FFAAAAAFDDF
..41111FAAAAFAAF
..411F13FFFFAAAF
..422F23423FFFF.
...433334234F...
....443334FEBD..
.....44DEEEEBD..
....DECEEBCBD...
....DCEEBCBBD...
...D66CEEEBBD...
..434D666666D...
...44A699999A...
....A5599999A...
...7A9999559A...
...77AAAAAAA....
"""),
    8: (16, """
..FFFAAAAAAAAFF.
..411FFAAAAAFDDF
..41111FAAAAFAAF
..411F13FFFFAAAF
..422F23423FFFF.
...433334234F...
....443334FEBD..
.....44DEEEEBD..
....DECEEBCBD...
....DEECEBBCD...
....DEEEC66CD...
....D6666434D...
....A6999944A...
....A5599999A...
....A9999559A7..
....AAAAAAAA77..
"""),
}


def body(frame, top, rows):
    f = o.frame(frame)
    lines = rows.strip('\n').split('\n')
    for dy, line in enumerate(lines):
        assert len(line) == 16, (frame, dy, line)
        for x, ch in enumerate(line):
            f.px[top + dy][x] = 0 if ch == '.' else HEX.index(ch)
    for y in range(top + len(lines), 32):
        f.px[y] = [0] * 16
    o.set_frame(frame, f)


STAND_OF = {3: 0, 4: 0, 5: 1, 6: 1, 7: 2, 8: 2}
for table in (FRONT, BACK, SIDE):
    for fr, (top, rows) in sorted(table.items()):
        if fr in STAND_OF:   # walk frame: head = stand head bobbed down 1px
            st = o.frame(STAND_OF[fr])
            w = o.frame(fr)
            w.px = [[0] * 16] + [r[:] for r in st.px[:31]]
            o.set_frame(fr, w)
        body(fr, top, rows)
for fr, y in ((1, 15), (5, 16), (6, 16)):
    o.patch_frame(fr, 2, y, 'FAAAFFFFAAAF')
# silver hairpin through the bun (back view)
for fr, dy in ((1, 0), (5, 1), (6, 1)):
    o.patch_frame(fr, 10, 15 + dy, 'B')
    o.patch_frame(fr, 11, 14 + dy, 'B')

res.append(o.save_ow(ID, 'npc_pink'))
compare(ID, 'aroma_lady', 'woman_2')
report(ID, res)
