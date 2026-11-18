"""EDIT: Sailor -> PORT WORKER (Tosa Port container terminal).
Front: vanilla sailor (flexing pose, face, arms kept). Sailor cap -> yellow hard hat adapted from
the FRLG Engineer's helmet (rounded dome, brim + forehead shadow, white highlight); sailor collar flaps -> hi-vis vest shoulders with reflective piping; striped shirt ->
orange hi-vis vest with a silver reflective band; white bell-bottoms -> navy work trousers;
brown work boots. OW: vanilla sailor sheet; cap -> redrawn hard hat, shirt -> orange vest with a silver band,
trousers -> navy.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from kit import *

ID = 'edit_sailor'

# ---------------------------------------------------------------- front
f = load_front('sailor')
# slot plan: 5/A (greys) -> hard-hat yellow; 9 stays as the only white shade; C/D -> vest orange;
# 6/7/B (blue) -> navy work trousers; 8 -> dark ochre-brown (hat brim edge, hair, boots).
HAT_HI, HAT, HAT_SH = 14, 5, 10
OR, OR_SH = 12, 13
TR_HI, TR, TR_SH = 11, 6, 7

# --- trousers y42-59: white -> navy
f.remap({14: TR_HI, 9: TR, 5: TR_SH, 10: TR_SH}, (8, 42, 56, 58))
# --- boots y59-62: grey bits -> dark
f.remap({5: 7, 10: 8, 9: 7}, (8, 59, 56, 62))
f.remap({14: TR_HI, 9: TR, 5: TR_SH, 10: TR_SH}, (8, 59, 56, 59))
# --- vest y33-41 (below the folded arms)
f.remap({14: OR, 9: OR, 5: OR_SH, 10: OR_SH, 13: OR_SH}, (8, 33, 56, 37))
# the two blue hem stripes become a double silver reflective band on the orange vest
f.remap({6: 14, 11: 14, 7: 9, 14: OR, 9: OR, 5: OR_SH, 10: OR_SH}, (8, 38, 56, 41))
# --- collar flaps y18-26 -> vest shoulders (orange) with reflective piping (white kept)
f.remap({11: OR, 6: OR, 7: OR_SH, 5: 9}, (24, 18, 50, 26))
# --- teeth shading 5 -> 9 (5 becomes yellow)
f.remap({5: 9}, (30, 13, 42, 17))
# --- side of the head under the hat: cap roll (left) -> hair, cap ribbon (right) -> hair
f.remap({5: 8, 6: 8, 14: 8, 11: 8}, (26, 7, 30, 10))
f.remap({9: 8, 7: 8, 6: 8, 10: 15, 5: 8}, (39, 7, 46, 12))

# shirt glimpsed under the right armpit -> vest
f.remap({5: OR_SH, 9: OR, 14: OR}, (38, 26, 46, 32))
f.set_pal(HAT, (248, 200, 32))
f.set_pal(HAT_SH, (200, 128, 24))
f.set_pal(OR, (248, 128, 32))
f.set_pal(OR_SH, (192, 72, 24))
f.set_pal(TR_HI, (104, 120, 160))
f.set_pal(TR, (72, 88, 128))
f.set_pal(TR_SH, (40, 52, 84))

# --- hard hat: the FRLG Engineer's helmet (engineer_frlg, x24-39 y4-13), whose head is turned the
# same way as the sailor's. Its dome is widened by 3 duplicated middle columns to fit the sailor's
# broader skull, then dropped 3 rows so the brim sits on the forehead above the brows. Engineer
# colours -> sailor slots; 8 becomes a dark ochre-brown (brim edge, hair, now brown work boots).
f.set_pal(HAT, (255, 216, 80))
f.set_pal(HAT_SH, (216, 176, 72))
f.set_pal(8, (120, 88, 40))
eng = load_front('engineer_frlg')
E2S = {1: 15, 2: 1, 3: 2, 4: 3, 5: 4, 7: 14, 13: HAT, 14: HAT_SH, 15: 8}
HAT_IDX = {1, 2, 7, 13, 14, 15}
SRC_COLS = list(range(24, 31)) + [30, 31, 32, 33, 33, 34, 35, 35] + list(range(36, 40))
DX, DY = 27, -3
f.clear(26, 1, 46, 6)
for y in range(4, 14):
    for i, sx in enumerate(SRC_COLS):
        v = eng.get(sx, y)
        if not v:
            continue
        hat = v in HAT_IDX
        if y <= 9 and not hat:
            continue
        if y == 10 and v not in HAT_IDX | {5}:       # brim + its shadow line
            continue
        if y >= 11 and not (hat and sx >= 33):        # only the helmet side over the ear
            if not (y == 11 and v in (4, 5)):         # forehead shading under the brim
                continue
        f.put(DX + i, y + DY, E2S[v])
res_f = f.save_front(ID)

# ---------------------------------------------------------------- OW: npc_1 -> npc_blue
# npc_blue ramps: 5-7 yellow (hard hat), 8-A indigo (work trousers), B-D orange (vest, hair brown)
o = load_ow('sailor')
src = o.copy()
o.pal = npc_pal('npc_blue')
ROWS = [  # (y0, y1, mapping) relative to the stand frames; walk frames 3-8 are bobbed 1px
    (11, 14, {8: 5, 9: 6, 10: 15, 12: 10, 13: 15}),                # hat dome, dark hair at the sides
    (15, 15, {8: 6, 10: 6, 12: 10, 13: 15}),                       # brim
    (16, 16, {14: 7, 8: 7, 10: 7, 12: 10, 13: 15}),                # brim shadow
    (17, 21, {12: 10, 13: 15, 7: 4, 10: 15, 8: 4, 9: 4, 6: 12}),   # head / hair
    (22, 26, {14: 11, 8: 11, 9: 11, 10: 12, 6: 12, 7: 4, 12: 12, 13: 13}),   # vest
    (27, 31, {12: 10, 13: 15, 14: 10, 8: 9, 10: 10, 7: 4, 6: 10}), # trousers + boots
]
for fr in range(9):
    b = 0 if fr < 3 else 1
    for y0, y1, m in ROWS:
        for y in range(y0 + b, min(31, y1 + b) + 1):
            for x in range(fr * 16, fr * 16 + 16):
                v = src.px[y][x]
                if v in m:
                    o.px[y][x] = m[v]
# silver reflective band round the vest (one row, front/back/side, bobbed on walk frames)
for fr in range(9):
    y = 25 + (0 if fr < 3 else 1)
    o.remap({11: 14}, (fr * 16 + 2, y, fr * 16 + 13, y))
# hard hat redrawn (the recoloured sailor cap read as a flat "funky hat"): rounded dome a little
# wider than the head, 2px white highlight upper-left, 1-row darker brim, skin/hair shadow row under
# it; hair hidden except sideburns (front) and a short nape (back); side view peak juts 1px past
# the face. Stand frames are drawn, walk frames reuse the same head 1px lower.
HEAD = {
    0: {10: '.....FFFFFF.....', 11: '...FFEE5555FF...', 12: '..F5555555566F..',
        13: '..F5555555566F..', 14: '.F555555555666F.', 15: '.F766666666667F.',
        16: '..FA33333333AF..'},
    1: {10: '.....FFFFFF.....', 11: '...FFEE5555FF...', 12: '..F5555555566F..',
        13: '..F5555555566F..', 14: '.F555555555666F.', 15: '.F766666666667F.',
        16: '..FDAAAAAAAADF..', 17: '..FAAAAAAAAAAF..', 18: '.4FAAAAAAAAAAF4.',
        19: '.4FDAAAAAAAADF4.', 20: '..FFDDAAAADDFF..', 21: '.41FF433334FF14.'},
    2: {10: '.....FFFFFF.....', 11: '...FFEE5555FF...', 12: '..F5555555566F..',
        13: '..F5555555566F..', 14: '..F55555555666F.', 15: 'F6666666666667F.',
        16: '..4333333AAAAF..'},
}
for fr, rows in HEAD.items():
    for y, row in rows.items():
        for wf in [fr] + {0: [3, 4], 1: [5, 6], 2: [7, 8]}[fr]:
            o.patch_frame(wf, 0, y + (0 if wf < 3 else 1), row)
res_o = o.save_ow(ID, 'npc_blue')
compare(ID, 'sailor', 'sailor')
report(ID, [res_f, res_o])
