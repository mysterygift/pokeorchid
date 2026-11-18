"""TOURIST (male): sunburnt holidaymaker. Front from hiker (hat, short sleeves, arms, face and
build kept pixel-for-pixel), OW from fat_man + hiker hat.
Run from dev_scripts/trainer_classes: python classes/tourist_m.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

# ---------------------------------------------------------------- front pic
BASE = 'hiker'
f = load_front(BASE)
V = load_front(BASE)            # untouched copy for the silhouette check

# Axes measured from the vanilla hiker with dump()
HEAD_CX = 33        # face centre: closed eyes at x30-31 / x35-37, teeth x32-35
EYE_Y = 11          # closed-eye row (brows at y9-10)
NOSE_X = 33
CHIN_Y = 18
BODY_CX = 33        # torso x23-44, bandana tip at x33-34
STERNUM_Y = 24
LEG_SPLIT_X = 34    # crotch column at y51
HEM_Y = 50          # new shorts hem (vanilla trousers end at y53, boots below)

# --- palette: hiker green shirt -> red aloha, grey sleeves -> red, khaki -> straw/khaki,
# bandana red merges into the shirt, freed slots 9/A/C become camera greys / sandal strap
f.remap({9: 5, 10: 6})                                  # grey sleeves -> shirt ramp
f.remap({12: 5}, (20, 14, 46, 30))                       # bandana light red -> shirt light
# vanilla D is also the reddish skin-shadow on hands and face; keep it skin before D turns dark red
f.remap({13: 3}, (22, 8, 44, 18))                        # brows / lip line -> skin shadow
f.remap({13: 3}, (8, 30, 26, 40))                        # left hand finger creases
f.remap({13: 3}, (45, 20, 54, 31))                       # right hand at the strap
f.remap({11: 13}, (26, 26, 45, 43))                      # khaki pocket seams on the shirt -> dark red
PAL = {
    1: (255, 216, 200), 2: (232, 164, 144), 3: (208, 120, 104), 4: (74, 56, 56),
    5: (248, 104, 80), 6: (200, 48, 48), 13: (128, 24, 40),
    7: (240, 208, 128), 8: (200, 160, 88), 11: (136, 104, 56),
    9: (200, 200, 216), 10: (88, 88, 104), 12: (232, 64, 64),
    14: (255, 255, 255), 15: (0, 0, 24),
}
for k, v in PAL.items():
    f.set_pal(k, v)
K = {'r': 5, 'R': 6, 'k': 13, 's': 7, 'S': 8, 'T': 11, 'g': 9, 'G': 10, 'w': 14, 'o': 4, 'x': 12}

# --- hat: drop the feather, close the brim top, hat band in red along the crown seam
f.clear(40, 0, 47, 5)
f.patch(40, 5, '444')
for x, y in ((28, 5), (29, 5), (30, 6), (31, 6), (32, 6), (33, 7), (34, 7), (35, 7), (36, 7)):
    f.put(x, y, 6)

# --- sunglasses on the closed-eye row; lenses centred on the eyes (x30, x36), bridge on the nose
GL = '''
    FFFFFF.FFFFFF
    .FgGGFFFgGGF.
    .FGGGF.FGGGF.
    ..FFF...FFF..
'''
f.patch(NOSE_X - 6, EYE_Y - 1, GL, K)

# --- bandana -> open camp collar of the aloha shirt, V of neck centred on the body axis
f.patch(BODY_CX - 6, CHIN_Y + 1, '''
    rrk32222223kRR
    rrrk322223kRRR
    rrrrk3223kRRRR
    rrrrrk33kRRRRR
    rrrrrrkkRRRRRR
''', K)

# --- camera on the sternum, strap symmetric from both collar edges
for y in range(CHIN_Y + 4, STERNUM_Y + 1):
    f.put(BODY_CX - 3, y, 10); f.put(BODY_CX + 4, y, 10)
f.patch(BODY_CX - 4, STERNUM_Y + 1, '''
    .FFFFFFFF.
    FggggggxgF
    FGGFFFFGGF
    FGFgwGFGGF
    FGFGGGFGGF
    FGGFFFFGGF
    .FFFFFFFF.
''', K)

# --- white hibiscus print, only painted onto shirt pixels
FLOWER = ['ww.', 'wxw', '.w.']
def flower(x0, y0):
    for dy, row in enumerate(FLOWER):
        for dx, ch in enumerate(row):
            if ch != '.' and f.px[y0 + dy][x0 + dx] in (5, 6):
                f.put(x0 + dx, y0 + dy, K[ch])
for x, y in ((16, 21), (19, 25), (47, 29), (45, 34), (25, 29), (40, 29), (27, 36), (37, 36), (32, 39)):
    flower(x, y)

# --- trousers -> knee-length cargo shorts (hem at HEM_Y), symmetric thigh pockets
for x in range(20, 47):
    if f.px[HEM_Y][x] not in (0, 15) and x != LEG_SPLIT_X:
        f.put(x, HEM_Y, 11)
for px in (BODY_CX - 10, BODY_CX + 7):
    f.patch(px, 46, '''
        TTTT
        TssT
        TssT
        TTTT
    ''', K)
# folded map tucked into the right pocket
f.patch(BODY_CX + 7, 43, '''
    .wwx
    .wgw
    .gwg
''', K)

# --- calves and sandals inside the old trouser/boot columns
f.clear(20, HEM_Y + 1, 48, 63)
LEG = '''
    .F1223F.
    .F1223F.
    .F1223F.
    .F1223F.
    ..F123F.
    ..F123F.
    ..F123F.
    .F12233F
'''
FOOT = '''
    F12xxx33F
    F1222233F
    FTTTTTTTF
    .FFFFFFF.
'''
f.patch(22, HEM_Y + 1, LEG, K)
f.patch(22, HEM_Y + 9, FOOT, K)
f.patch(37, HEM_Y + 1, LEG, K)
f.patch(38, HEM_Y + 8, FOOT, K)     # right boot sits a row higher in the vanilla

# --- hiking stick -> closed red umbrella (stays in the stick's 3 columns), tip off the edge
f.clear(16, 44, 20, 63)
f.patch(17, 44, '''
    .4.
    FSF
    FrF
    FrR
    FrR
    FwR
    FwR
    FrR
    FrR
    FrR
    FrR
    FrR
    .k.
    .F.
    .G.
    .G.
    .G.
    .F.
''', K)

res = [f.save_front('tourist_m')]


# --- silhouette check: body pixels outside the vanilla silhouette (props above y14 and
# the umbrella are exempt) are listed and drawn magenta in out/tourist_m_overlay.png
def overlay(new, ref, name, exempt):
    S = 6
    im = new.render(S, (232, 232, 232))
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    bad = []
    for y in range(64):
        for x in range(64):
            inside = ref.px[y][x] != 0
            if inside and any(not (0 <= x + ax < 64 and 0 <= y + ay < 64) or ref.px[y + ay][x + ax] == 0
                              for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                d.rectangle([x * S + 2, y * S + 2, x * S + 3, y * S + 3], fill=(0, 200, 255))
            if new.px[y][x] and not inside and not exempt(x, y):
                bad.append((x, y))
                d.rectangle([x * S, y * S, x * S + S - 1, y * S + S - 1], outline=(255, 0, 255))
    im.save(os.path.join(OUT, f'{name}_overlay.png'))
    return bad


bad = overlay(f, V, 'tourist_m', lambda x, y: y < 14)
print('outside vanilla silhouette:', bad)
# ---------------------------------------------------------------- overworld
# fat_man body (portly, like the hiker front) on npc_2: shirt 8-A -> red,
# hair/belt B-D -> brown, pants 6/7 -> brown shorts. Hat transplanted from hiker
# (its 5-7 hat ramp lands on npc_2's golden straw ramp).
o = load_ow('fat_man')
hk = load_ow('hiker')
o.pal = npc_pal('npc_2')
BOB = [0, 0, 0, 1, 1, 1, 1, 1, 1]
for i in range(9):
    fr, hf, b = o.frame(i), hk.frame(i), BOB[i]
    dx = 1 if i in (2, 7, 8) else 0           # side heads sit 1px further back on fat_man
    fr.clear(0, 0, 15, 13 + b)
    for y in range(10 + b, 17 + b):
        for x in range(16):
            v = hf.px[y][x]
            if v in (5, 6, 7):
                fr.put(x + dx, y - 2, v)
    # pants -> shorts (brown), lower legs -> skin
    fr.remap({6: 11, 7: 12}, (0, 22 + b, 15, 31))
    for y in range(29 + b, 32):
        for x in range(16):
            if fr.px[y][x] in (11, 12):
                fr.px[y][x] = 3 if fr.px[y][x] == 12 else 2
    if i in (0, 3, 4):        # front: sunglasses + camera on the belly
        fr.patch(4, 16 + b, '''
            FFFFFFFF
            FFF..FFF
        ''')
        fr.patch(5, 23 + b, '''
            .FFFF.
            FFEEFF
            .FFFF.
        ''')
    if i in (2, 7, 8):        # side: shades + camera nose poking forward
        fr.patch(4, 16 + b, '''
            FFFF
            FF..
        ''')
        fr.patch(2, 22 + b, '''
            FF
            EF
        ''')
    o.set_frame(i, fr)

res.append(o.save_ow('tourist_m', 'npc_2'))
compare('tourist_m', 'hiker', 'fat_man')
report('tourist_m', res)
