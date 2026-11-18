"""CLASSICAL DANCER (dancer_f): Bharatanatyam dancer in aramandi (half-sitting, knees out) with
arms stretched to the sides (natyarambhe), silk costume with a pleated fan, gold temple jewellery,
long braid with jasmine, ankle bells.
Front: psychic_f (RSE) head/face/torso, arms + hands from pokemon_breeder_f (pose B, picked) or
breeder + leader_erika_frlg chest hand (pose A); narrow aramandi legs and costume redrawn.
Writes out/dancer_f_pose_options.png (A | B at x4). OW: lass on npc_2 (darker skin).
Run from dev_scripts/trainer_classes: python classes/dancer_f.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from kit import *

ID = 'dancer_f'


def poly(pic, pts, idx):
    """Scanline-fill a polygon (list of (x, y)) with palette index idx."""
    ys = [p[1] for p in pts]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(pts)
        for i in range(n):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
            if y0 == y1:
                continue
            if min(y0, y1) <= y + 0.5 < max(y0, y1):
                xs.append(x0 + (y + 0.5 - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for a, b in zip(xs[::2], xs[1::2]):
            for x in range(int(round(a)), int(round(b))):
                pic.put(x, y, idx)


# ------------------------------------------------------------------ front
f = load_front('psychic_f')

# remove the psychic glow (7), the floating ball, the hair spike
f.remap({7: 0})
f.clear(14, 32, 25, 42)
f.clear(28, 4, 37, 9)

PAL = {
    0: BG,
    1: (232, 176, 128), 2: (200, 136, 96), 3: (160, 96, 64), 4: (96, 56, 40),   # warm brown skin
    5: (240, 88, 96), 6: (192, 32, 64), 7: (112, 16, 48),                        # red silk
    8: (248, 216, 96), 9: (192, 128, 40),                                         # temple gold
    10: (64, 56, 80), 11: (32, 32, 48), 12: (104, 96, 128),                      # black hair
    13: (208, 216, 184),                                                          # jasmine shade
    14: (255, 255, 255), 15: (0, 0, 0),
}

T = 100
# old indices -> new: clothing blue 5/6/8 -> silk 5/6/7; hair 9/A/B -> C/A/B; ball C/D -> silk
f.remap({5: T + 5, 6: T + 6, 8: T + 7, 9: T + 12, 10: T + 10, 11: T + 11, 12: T + 5, 13: T + 6})
f.remap({T + k: k for k in range(16)})
for k, v in PAL.items():
    f.set_pal(k, v)

# ---- head: centre-parted black hair, nethi chutti (gold along the parting + forehead pendant)
f.clear(24, 8, 41, 9)
f.patch(24, 9, '''
    .....FFFFFF.......
    ....FCC9ACCAAF....
    ..FACCA9ACCAAABF..
    .FACCAA9AACAAABF..
    FACAAAB9BAACAAABF.
    FACAAB292BAAAAABF.
    FAAAB21912BAAAABAF
    .BAB2118812BAAAAAF
    .BA31119112BBAAAAF
    ''', {})
# open, kohl-lined eyes (2px tall) in place of the closed ones
f.patch(27, 19, '''
    4F41114F42
    4F21112F42
    ''')
# jhumka earrings
f.patch(25, 21, '''
    8
    9
    ''')

HEAD = f.copy()          # psychic_f head, recoloured, before the body is rebuilt
BREEDER = load_front('pokemon_breeder_f')   # vanilla arms (shoulder-height, open hands)
ERIKA = load_front('leader_erika_frlg')     # vanilla hand raised at the chest


def arm_from(src, x0, y0, x1, y1, dx, dy, pic):
    """Copy only skin (1-4) and black pixels of a vanilla arm (same skin slot layout)."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = src.px[y][x]
            if v in (1, 2, 3, 4, 15):
                pic.put(x + dx, y + dy, v)


def sleeve(pic, x0, x1, y0, y1, border_x):
    """Paint an elbow-length silk sleeve inside the arm silhouette, zari border at border_x."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = pic.px[y][x]
            if v in (1, 2, 3, 4):
                pic.px[y][x] = 9 if x == border_x and v in (3, 4) else 8 if x == border_x else {1: 5, 2: 5, 3: 6, 4: 7}[v]


def build_front(option):
    f = HEAD.copy()
    # clear psychic arms and body (hair/face rows above 25 stay)
    f.clear(0, 14, 23, 31)
    f.clear(42, 14, 63, 31)
    f.clear(24, 25, 41, 31)
    f.clear(0, 32, 63, 62)

    # torso: blouse with gold-bordered hem, choker + V haram with pendant, oddiyanam belt
    f.patch(24, 25, """
        ....7554334667...
        ...755988896667..
        ..F55585566866F..
        ..F55558568667F..
        ..F5555588667F...
        ..F5555569667F...
        ..F5555666667F...
        ...F88888899F....
        ...F55568666F....
        ...9888868889....
        ...F99998999F....
        ..F5555696666F...
        .F555567576667F..
        """)

    # ---- narrow aramandi: knees just outside the hips, shins drawing in, small turned-out feet
    # thighs are foreshortened (they point out/forward), so the knee sits only 8 rows below the hip
    OL = {37: 26, 38: 25, 39: 24, 40: 24, 41: 23, 42: 23, 43: 22, 44: 22, 45: 22}
    FL = {39: 30, 40: 29, 41: 29, 42: 28, 43: 28, 44: 28, 45: 28, 46: 28, 47: 28, 48: 29}
    SH = {46: (22, 26), 47: (22, 26), 48: (22, 27), 49: (23, 27), 50: (23, 28), 51: (24, 28),
          52: (24, 28), 53: (25, 29), 54: (25, 29), 55: (25, 29), 56: (26, 29), 57: (26, 29),
          58: (26, 29)}
    FOOT = {59: (25, 29), 60: (24, 28), 61: (24, 27)}
    M = lambda x: 63 - x

    def both(x, y, c, cr=None):
        f.put(x, y, c)
        f.put(M(x), y, c if cr is None else cr)

    for y, ol in OL.items():
        fl = FL.get(y, 31)
        for x in range(ol, fl + 1):
            lit = x == ol and y < 44
            knee = y >= 44 and x - ol < 3
            both(x, y, 5 if lit else 7 if knee else 6,
                 6 if lit else 7 if (knee or x - ol >= 3) else 6)
    for x in range(OL[37], M(OL[37]) + 1):
        f.put(x, 37, 5 if x < 31 else 6)
    for y, (a, b) in SH.items():
        for x in range(a, b + 1):
            if y == 46:
                c, cr = 8, 9                                   # pyjama zari border below the knee
            elif y == 47:
                c, cr = 9, 9
            elif y == 57:
                c, cr = (8 if x % 2 else 9), (9 if x % 2 else 8)   # ankle bells
            elif y == 58:
                c, cr = 9, 9
            else:
                c = 1 if x == a else 3 if x == b else 2
                cr = 2 if x == a else 4 if x == b else 3
            both(x, y, c, cr)
    for y, (a, b) in FOOT.items():
        for x in range(a, b + 1):
            if x == a and y == 61:
                c, cr = 6, 6                                   # red alta on the toes
            else:
                c, cr = (1 if x == a and y < 61 else 2 if x < b else 3), (3 if x < b else 4)
            both(x, y, c, cr)
    # small pleated fan between the knees, zari edges and hem
    import math
    for y, fl in FL.items():
        for x in range(fl, M(fl) + 1):
            a = math.degrees(math.atan2(x - 31.5, y - 37.0))
            k = (a + 75) / 13.0
            c = 7 if (k - math.floor(k)) < 0.22 else (5 if int(k) % 2 or x < 31 else 6)
            if x in (fl, M(fl)):
                c = 9
            if y == 47:
                c = 8
            if y == 48:
                c = 9
            f.put(x, y, c)
    f.outline(15, (10, 32, 54, 63))

    # ---- arms (vanilla limbs, sleeves painted inside the silhouette)
    if option == 'B':
        # both arms out at shoulder height, open hands (pokemon_breeder_f), 3px narrower each side
        arm_from(BREEDER, 9, 24, 23, 32, 3, 0, f)
        arm_from(BREEDER, 40, 25, 56, 32, -3, 0, f)
        sleeve(f, 22, 28, 23, 32, 22)
        sleeve(f, 36, 41, 23, 32, 41)
    else:
        # A: left arm out to the side (breeder), right hand raised at the chest (erika)
        arm_from(BREEDER, 9, 24, 23, 32, 3, 0, f)
        sleeve(f, 22, 28, 23, 32, 22)
        f.patch(36, 25, """
            7777F
            6666F
            .666F
            .667F
            .667F
            .889F
            .FFF.
            """)
        arm_from(ERIKA, 36, 26, 43, 31, -4, 0, f)
    # tidy the shoulder line where the vanilla arm meets the new torso
    f.put(26, 24, 0)
    f.put(41, 24, 0)
    f.put(27, 25, 5)
    # one gold bangle on each bare forearm
    for y in range(20, 33):
        for x in (17, 45 if option == 'B' else -1):
            if 0 <= x < 64 and f.px[y][x] in (1, 2, 3):
                f.put(x, y, 8 if f.px[y][x] in (1, 2) else 9)

    # jasmine strand wrapped round the back of the head, continuing down the braid
    f.patch(38, 13, """
        .EF..
        .EDF.
        ..EDF
        ..DEF
        ..EEF
        ..DEF
        .EDF.
        .EF..
        DF...
        """)
    # braid hanging behind the right side of the torso, gold kunjalam tassel at the end
    BRAID = {30: 38, 31: 38, 32: 39, 33: 39, 34: 39, 35: 39}
    for y, x in BRAID.items():
        if f.px[y][x] not in (0, 15):
            continue
        top = y % 2 == 0
        jas = y <= 32
        f.put(x, y, (14 if top else 13) if jas else (12 if top else 10))
        f.put(x + 1, y, (13 if top else 14) if jas else (10 if top else 11))
        f.put(x + 2, y, 15)
        if f.px[y][x - 1] == 0:
            f.put(x - 1, y, 15)
    f.patch(39, 36, """
        F98F
        F66F
        F76F
        .FF.
        """)
    return f


OPTIONS = {k: build_front(k) for k in ('A', 'B')}
PICK = 'B'
f = OPTIONS[PICK]
# side-by-side of both pose options at x4 for the review
from PIL import Image as _I
_sheet = _I.new('RGBA', (64 * 4 * 2 + 8, 64 * 4), (70, 70, 70, 255))
for _k, _n in enumerate(('A', 'B')):
    _sheet.paste(OPTIONS[_n].render(4, (232, 232, 232)), (_k * (64 * 4 + 8), 0))
_sheet.save(os.path.join(OUT, f'{ID}_pose_options.png'))

if 'dump' in sys.argv:
    print(f.dump(4, 4, 59, 63))

res = [f.save_front(ID)]

# ------------------------------------------------------------------ overworld
# lass (npc_4) head/face/silhouette moved onto npc_2: skin uses the warm brown ramp
# (3 highlight, B base, C shade, D outline), black hair F/D with 4 sheen, red silk 8-A, gold 5-7,
# jasmine E. Pigtails become one braid with jasmine and a gold tassel; jhumkas at the ears;
# knees slightly bent, bare feet with ankle bells.
o = blank_ow('npc_2')

HEAD_FRONT = """
......FFFF......
....FF44644F....
...FD444644DF...
..FDDD4464DDDF..
..FFDDDF5DDDFF..
..FFD333333DFF..
.D3F33333BBBFBD.
.DBF3BFB3FBBFBD.
.6DCBBFBBFBBCD6.
...DCCBBBBCCD...
....DCCCCCCD....
"""
HEAD_BACK = """
......FFFF......
....FFDDFDFF....
...F4DDFDDD4F...
..FD44DDFD44DF..
..FDD44F444DDF..
..FDDDDDFDDDDF..
.DFFDDDEEDDDFFD.
.DCFFFEDDEFFFCD.
..6FFFFEEFFFF6..
...FCCFEDFCCF...
....DCFD4FCD....
"""
HEAD_SIDE = """
......FFFF......
....FFDDDDFF....
...FFDDDDDD4F...
..FFDDDDDD44DF..
..FFDDD4D4DDDEF.
..D3FFDFDDDDDEF.
..D33BFCFDDDDEF.
..D33F3CFFFFFEF.
..DBBFBCFBCFEF..
...DCCCCC6CDFDF.
....DDCCCCFFD4F.
"""
BODY = {
    0: """
..A88B6556B99A..
..A8888599999A..
.D3BA888999ABCD.
D3BA65595566ABCD
.DDA88A8A899ADD.
..A65A5555A56A..
..D3BD....DBCD..
.D3B6D....D6BCD.
.DDDD......DDDD.
""",
    3: """
..A88B6556B99A..
D3BA888599999A..
.DD.A888999ABCD.
...A65595566ABCD
...A88A8A899A3BD
..A65A5555A56ADD
..D3BD....DBCD..
.D3B6D....DDDD..
.DDDD...........
""",
    4: """
..A88B6556B99A..
..A888859999ABCD
.D3BA888999A.DD.
D3BA65595566A...
DB3A88A8A899A...
DDA65A5555A56A..
..D3BD....DBCD..
..DDDD....D6BCD.
...........DDDD.
""",
    2: """
.....DC88AFD4F..
....A88899A4DF..
....A83B99AD4F..
....A6B655A4DF..
....A83B89AD4F..
...A65C8A9A66F..
...D3BD.DBCD....
..D3B6D.D6BCD...
..DDDD...DDDD...
""",
    7: """
.....DC88AFD4F..
....A88899A4DF..
....A83B99AD4F..
....A6B655A4DF..
....A83B89AD4F..
...A65C8A9A66F..
..D3BD..DBCD....
.D3B6D...D6BCD..
.DDDD.....DDDD..
""",
    8: """
.....DC88AFD4F..
....A88899A4DF..
....A83B99AD4F..
....A6B655A4DF..
....A83B89AD4F..
...A65C8A9A66F..
....D3BDBCD.....
...D3B6D6BCD....
...DDDDDDDD.....
""",
}
# back views: the front body with the braid (and its gold tassel) hanging down the middle
BRAID = ['FD4F', 'F4DF', 'FD4F', 'F4DF', 'FD4F', 'F66F', 'F99F', '.FF.']


def back_body(front):
    rows = front.strip('\n').split('\n')
    out = []
    for k, r in enumerate(rows):
        r = list(r)
        if k < len(BRAID):
            for dx, ch in enumerate(BRAID[k]):
                if ch != '.':
                    r[6 + dx] = ch
        out.append(''.join(r))
    return '\n'.join(out)


BODY[1] = back_body(BODY[0])
BODY[5] = back_body(BODY[3])
BODY[6] = back_body(BODY[4])
HEADS = {0: HEAD_FRONT, 3: HEAD_FRONT, 4: HEAD_FRONT, 1: HEAD_BACK, 5: HEAD_BACK, 6: HEAD_BACK,
         2: HEAD_SIDE, 7: HEAD_SIDE, 8: HEAD_SIDE}
for fr in range(9):
    bob = 0 if fr in (0, 1, 2) else 1
    rows = HEADS[fr].strip('\n').split('\n') + BODY[fr].strip('\n').split('\n')
    f2 = o.frame(fr)
    for dy, line in enumerate(rows):
        assert len(line) == 16, (fr, dy, line)
        f2.px[11 + bob + dy] = [0 if ch == '.' else HEX.index(ch) for ch in line]
    o.set_frame(fr, f2)

res.append(o.save_ow(ID, 'npc_2'))
compare(ID, 'psychic_f', 'lass')
report(ID, res)
