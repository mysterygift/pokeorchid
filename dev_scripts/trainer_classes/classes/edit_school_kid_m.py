"""EDIT: School Kid M -> Tosa primary-school uniform. White short-sleeve shirt with a school badge
on the chest, khaki shorts (vanilla trouser colours, cut above the knee), white socks, black shoes.
Front: vanilla school_kid_m (glasses, pose and bag kept; bag turned navy). OW: vanilla school_kid_m
sheet (npc_1); blue shirt -> white, olive trousers -> khaki shorts with skin knees, white socks.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kit import *

ID = 'edit_school_kid_m'

# ---------------------------------------------------------------- front
f = load_front('school_kid_m')
# index moves first (old colours), then new colours
f.remap({12: 13}, (24, 13, 44, 21))                   # hair highlight -> D (grey-blue)
f.remap({13: 6, 12: 9}, (18, 21, 41, 29))             # glasses: navy frame, pale lens
f.remap({13: 9, 6: 13}, (22, 29, 42, 43))             # shirt: D shade -> 9, navy edges -> D
f.remap({13: 6, 12: 13}, (36, 43, 50, 58))            # bag -> navy
f.set_pal(12, (240, 240, 248))   # shirt white
f.set_pal(9, (200, 200, 232))    # shirt mid / collar / lens
f.set_pal(13, (144, 152, 192))   # shirt shade, hair sheen

# school badge on the left chest (viewer's right): navy shield, yellow crest
f.patch(33, 34, '''
    666
    6A6
    .6.
''')
# shorts end at y50 (vanilla khaki); skin legs, white socks, black shoes.
# left leg x25-29; right leg is the far, stepping leg that runs down-right behind the bag.
f.clear(22, 51, 31, 63)
f.patch(23, 50, '''
    .855558F
    ..41234.
    ..41234.
    ..41234.
    ..41234.
    ..FEE9F.
    ..FEE9F.
    ..FEE9F.
    ..FEE9F.
    .F67777F
    F677777F
    .FFFFFF.
''')
f.clear(32, 51, 36, 53); f.clear(33, 54, 37, 55); f.clear(33, 56, 38, 58); f.clear(34, 59, 40, 63); f.clear(39, 57, 40, 58)
f.patch(31, 50, '''
    F855558F
    ..4234F.
    ..4234F.
    ..42334
    ...4234
    ...4234
    ...FEE9F
    ...FEE9F
    ...FEE9F
    ...F6777F
    ...F67777F
    ....FFFFF
''')
# belt and a lighter shirt tail (vanilla's dark tuck band read as a second garment)
f.remap({13: 7}, (26, 43, 34, 43))
for y in (39, 40, 41):
    for x in range(26, 34):
        if f.get(x, y) == 9 and x < 32:
            f.put(x, y, 12)
res_f = f.save_front(ID)

# ---------------------------------------------------------------- OW (npc_1)
o = load_ow('school_kid_m')
# shirt rows: light blue 8 -> white E, mid blue 9 -> light blue 8 (white shirt shaded blue)
o.remap({8: 14, 9: 8}, (0, 23, 143, 27))
# khaki shorts row (olive C -> khaki B, D -> C), then skin legs, white socks, dark shoes
SH = {0: 27, 1: 27, 2: 27, 3: 28, 4: 28, 5: 28, 6: 28, 7: 28, 8: 28}
for fr, y in SH.items():
    o.remap({12: 11, 13: 12}, (fr * 16, y, fr * 16 + 15, y))
legs = {
    0: (28, '''
        ....423..324....
        ...AEEA..AEEA...
    '''),
    1: (28, '''
        ....433..334....
        ...AEEA..AEEA...
    '''),
    2: (28, '''
        .....42334......
        ....AEEEE8A.....
    '''),
    3: (29, '''
        .....AA42334....
    '''),
    4: (29, '''
        ....43324AA.....
    '''),
    5: (29, '''
        ....43334AA.....
    '''),
    6: (29, '''
        .....AA43334....
    '''),
    7: (29, '''
        ...A433_42234A..
        ....AE...AEEA...
    '''),
    8: (29, '''
        ..A4334_43334A..
        ...AEE8...AAA...
    '''),
}
for fr, (y, art) in legs.items():
    o.patch_frame(fr, 0, y, art)
res_o = o.save_ow(ID, 'npc_1')
compare(ID, 'school_kid_m', 'school_kid_m')
report(ID, [res_f, res_o])
