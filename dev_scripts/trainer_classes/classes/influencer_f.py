"""INFLUENCER (female): filming herself on a selfie stick, posing with a bubble tea.
Front from cool_trainer_f_frlg, OW from cooltrainer_f.
Run from dev_scripts/trainer_classes: python classes/influencer_f.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

# ---------------------------------------------------------------- front pic
f = load_front('cool_trainer_f_frlg')

PAL = {
    5: (232, 232, 240), 6: (168, 176, 200), 7: (64, 72, 104),
    8: (112, 100, 120), 9: (64, 56, 80), 10: (32, 28, 44),
    11: (255, 184, 208), 12: (240, 120, 160), 13: (176, 56, 104),
}
for k, v in PAL.items():
    f.set_pal(k, v)
# the base's light-grey pixels (shoe/cuff highlights) -> white; slot 5 is left unused
f.remap({5: 14})
K = {'s': 5, 'g': 6, 'G': 7, 'p': 11, 'P': 12, 'k': 13, 'w': 14, 'h': 8, 'H': 9, 'd': 10}

# jacket -> oversized pink sweatshirt: zipper, cuffs and rib hem all in the pink ramp
f.remap({14: 12, 6: 12}, (26, 22, 30, 36))   # zipper line melts into the mid pink
f.remap({14: 11, 6: 12}, (12, 20, 36, 36))
f.remap({6: 12}, (12, 37, 35, 37))
f.remap({14: 11, 6: 12, 7: 13}, (17, 16, 24, 19))
f.remap({14: 11, 6: 12, 7: 13}, (38, 33, 44, 37))

# the hand at her chin stays exactly as the vanilla pose (no prop)

# lower hand: pokeball -> fist gripping a selfie stick
f.clear(44, 33, 49, 40)
f.patch(41, 33, '''
    ...gF....
    PP7gF44..
    kPF3gF33F
    .FkF2gF3F
    ..F3224gF
    ...F4324F
    ....F4F3F
    .....FFF.
''', K)
# the stick runs unbroken from the fist up to a clamp; grey highlight left, black right
y0, x0, y1, x1 = 33, 45, 11, 53
for y in range(y1, y0):
    x = x0 + round((y0 - y) * (x1 - x0) / (y0 - y1))
    f.put(x, y, 15); f.put(x - 1, y, 6)
# clamp on the stick end gripping the bottom of the phone; we see the phone's pink case
# and camera, its darker right edge turning it toward her face
f.patch(49, 1, '''
    .FFFFFF.
    FpppPPkF
    FpFwPPkF
    FpFFPPkF
    FppPPPkF
    FpPPPPkF
    FpPPPkkF
    .FFFFFF.
    ..FggF..
    ...FgF..
''', K)

# chunky white "dad" sneakers with a pink flash, white socks
SNEAKER = '''
    ..FwwF...
    ..FwwgF..
    .FwwwwgF.
    FwPPwwwgF
    FwwwwwwgF
    FggggggGF
    .FFFFFFF.
'''
for x in (18, 32):
    f.clear(x - 1, 56, x + 9, 62)
    f.patch(x, 56, SNEAKER, K)

# pink scrunchie at the root of the ponytail
f.patch(34, 3, '''
    .FFF.
    FpPPk
    FPPkF
    .Fkk.
''', K)

# little white heart on the sweatshirt
f.patch(30, 24, '''
    w.w
    www
    .w.
''', K)

res = [f.save_front('influencer_f')]

# ---------------------------------------------------------------- overworld
# cooltrainer_f (ponytail + hair tie, small body) moved from npc_blue to npc_pink:
# hair purple 8/9 -> dark grey C/D (A stays as the darkest navy), orange top B-D -> pink 5-7,
# shorts stay A (dark navy),
# hair tie -> pink, shoes -> chunky white.
o = load_ow('cooltrainer_f')


def line(pic, x0, y0, x1, y1, v, only_empty=False):
    """Straight 1px line; only_empty draws it behind the figure (gaps only)."""
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        x, y = round(x0 + (x1 - x0) * k / n), round(y0 + (y1 - y0) * k / n)
        if not only_empty or pic.px[y][x] == 0:
            pic.put(x, y, v)


PHONE = '''
    FFF
    F6F
    F5F
    FFF
'''
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
for i in range(9):
    fr, b = o.frame(i), BOB[i]
    fr.remap({8: 12, 9: 13, 12: 6}, (0, 0, 15, 23 + b))
    fr.remap({11: 5, 12: 6, 13: 7}, (0, 24 + b, 15, 31))
    fr.remap({6: 14}, (0, 29 + b, 15, 31))          # chunky white sneakers
    o.set_frame(i, fr)

# The stick arm holds steady: walk frames reuse the stand frame's stick arm, bobbed 1px.
# view: (stand frame, walk frames, arm columns, arm rows, hand grip, phone bottom-centre)
VIEWS = {
    'front': (0, (3, 4), (10, 15), (22, 27), (12, 24), (14, 11)),
    'back':  (1, (5, 6), (0, 5), (22, 27), (2, 24), (1, 11)),
    # side: a pole crossing her face reads as a scar, so here she holds it out in front at
    # chest height (phone seen edge-on); the pole only crosses her sleeve
    'side':  (2, (7, 8), (3, 10), (24, 28), (7, 27), (1, 24)),
}
PHONE_SIDE = '''
    FF
    F6
    F5
    FF
'''
for view, (st, walks, (ax0, ax1), (ay0, ay1), (gx, gy), (px_, py_)) in VIEWS.items():
    stand = o.frame(st)
    for w in walks:
        fr = o.frame(w)
        fr.clear(ax0, ay0 + 1, ax1, ay1 + 1)
        fr.blit(stand, ax0, ay0, ax1, ay1, ax0, ay0 + 1)
        o.set_frame(w, fr)
    for i in (st,) + walks:
        fr, b = o.frame(i), BOB[i]
        # light-grey pole drawn in front, unbroken from the grip to the phone's bottom edge
        line(fr, gx, gy - 1 + b, px_, py_ + b, 11)
        if view == 'side':
            fr.patch(px_ - 1, py_ - 4 + b, PHONE_SIDE)
        else:
            fr.patch(px_ - 1, py_ - 4 + b, PHONE)
        o.set_frame(i, fr)
o.pal = npc_pal('npc_pink')

res.append(o.save_ow('influencer_f', 'npc_pink'))
compare('influencer_f', 'cool_trainer_f_frlg', 'cooltrainer_f')
report('influencer_f', res)

