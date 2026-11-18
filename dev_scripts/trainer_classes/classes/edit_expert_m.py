"""EDIT: Expert M -> TAI CHI UNCLE. White silk tai-chi suit with frog buttons, beard kept.
Front: vanilla expert_m; the blue hakama becomes loose white silk trousers in a wide stance
(leg split, gathered ankle cuffs, black cloth shoes) and the gi is lengthened into a hip-length
jacket with a centre seam and red frog-knot buttons. OW: vanilla expert_m sheet (npc_4); navy
suit -> white/grey silk, pink sash dropped, dark knot buttons, black shoes.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kit import *

ID = 'edit_expert_m'
A, E, F, N9, N5 = 10, 14, 15, 9, 5


def span(pic, y, l, r, lit_edge=A, dark_edge=F, hi=2, shade=1):
    """Fill one row of white silk from l to r: lit left edge, E highlight, 9 base, 5 shade, dark right edge."""
    for x in range(l, r + 1):
        if x == l:
            v = lit_edge
        elif x == r:
            v = dark_edge
        elif x <= l + hi:
            v = E
        elif x >= r - shade:
            v = N5
        else:
            v = N9
        pic.put(x, y, v)


# ---------------------------------------------------------------- front
f = load_front('expert_m')
f.set_pal(6, (232, 104, 96))    # knot highlight
f.set_pal(7, (176, 40, 48))     # knot body
f.set_pal(11, (112, 24, 40))    # knot shadow

# waist rows 33-38: the hakama ties become the jacket front (white), hand + sleeve untouched
f.remap({6: E, 7: N9, 8: N5}, (28, 33, 37, 38))
f.remap({6: E, 7: N9, 8: N5}, (38, 36, 46, 38))
f.put(31, 33, N9); f.put(30, 38, A)
f.clear(18, 39, 52, 63)

# jacket body y39-46 (hip length), slight flare
jacket = {39: (29, 46), 40: (29, 45), 41: (29, 45), 42: (28, 45), 43: (28, 46), 44: (28, 46),
          45: (27, 46), 46: (27, 47)}
for y, (l, r) in jacket.items():
    span(f, y, l, r, hi=3, shade=2)
# hem: shadow line under the jacket edge
for x in range(28, 47):
    f.put(x, 46, N5 if x < 44 else A)
f.put(27, 46, F); f.put(47, 46, F)

# trousers y47-59: wide tai-chi stance, crotch apex y50
legs = {
    47: [(28, 46)], 48: [(28, 46)], 49: [(27, 47)], 50: [(27, 47)],
    51: [(27, 36), (38, 47)], 52: [(26, 36), (39, 48)], 53: [(26, 35), (39, 48)],
    54: [(26, 35), (40, 48)], 55: [(25, 34), (40, 49)], 56: [(25, 34), (41, 49)],
    57: [(25, 33), (41, 49)],
}
for y, segs in legs.items():
    for i, (l, r) in enumerate(segs):
        if i == 0:
            span(f, y, l, r, hi=3, shade=2 if len(segs) == 1 else 1, dark_edge=F if len(segs) == 1 else A)
        else:
            span(f, y, l, r, lit_edge=N5, hi=0, shade=3)
            f.put(l, y, A)
# crease from the crotch on each leg + right-leg shading
for y in range(47, 51):
    f.put(37, y, N5)
f.put(37, 50, A)
for y, x in ((52, 31), (53, 31), (54, 30), (55, 30), (56, 30)):
    f.put(x, y, N5)
# gathered ankle cuffs (y58-59) and black cloth shoes (y60-61)
f.patch(24, 58, '''
    A9EE95595F.........F59955A5F
    F5995A5AFF.........FA5A55AFF
    F8888FFFFF.........FF8888FFF
    _FFFFFFFF...........FFFFFFF_
''')
# frog knots on the centre seam x37
for y in range(39, 46):
    f.put(37, y, N5)
for y in (40, 42, 44):
    f.patch(35, y, 'B767B')
res_f = f.save_front(ID)

# ---------------------------------------------------------------- OW (npc_4)
o = load_ow('expert_m')
# suit: navy 5 -> E highlight, 6 -> B light grey; darkest navy 7 -> black on the silhouette, C inside;
# pink sash 8/9/A dropped into the silk (tai-chi suits have no sash)
src = o.copy()
for y in range(32):
    for x in range(144):
        if src.px[y][x] == 7:
            fx = x % 16
            edge = any(not (0 <= fx + dx < 16 and 0 <= y + dy < 32) or src.px[y + dy][x + dx] == 0
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            o.px[y][x] = 15 if edge else 12
o.remap({5: 14, 6: 11, 8: 11, 9: 12, 10: 12})
# red-pink frog knots on the centre seam just under the beard (front stand + both walk frames)
for fr, dy in ((0, 0), (3, 1), (4, 1)):
    o.patch_frame(fr, 7, 26 + dy, '99')
res_o = o.save_ow(ID, 'npc_4')
compare(ID, 'expert_m', 'expert_m')
report(ID, [res_f, res_o])
