"""Floors, open sides, stall shell and furniture art (cuisine-neutral pieces)."""
from kit import Art, art, bands, FLOOR, SHELL, FURN

# ================================================================== floors (pal 6)
SHADE = {FLOOR["F"]: FLOOR["S"], FLOOR["H"]: FLOOR["S"], FLOOR["G"]: FLOOR["s"],
         FLOOR["T"]: FLOOR["D"], FLOOR["t"]: FLOOR["T"], FLOOR["D"]: FLOOR["E"]}


def dining_px(x, y):
    """Cream 16 px tiles with a small terracotta diamond inlaid at every corner."""
    dx = min((x + 1) % 16, 16 - (x + 1) % 16)
    dy = min((y + 1) % 16, 16 - (y + 1) % 16)
    if dx + dy <= 2:
        return FLOOR["T"]
    if x % 16 == 15 or y % 16 == 15:
        return FLOOR["G"]
    if x % 16 == 0 or y % 16 == 0:
        return FLOOR["H"]
    return FLOOR["F"]


def quarry_px(x, y):
    """Terracotta 8 px quarry tiles: the serving walkway in front of the stalls."""
    if x % 8 == 7 or y % 8 == 7:
        return FLOOR["D"]
    if (y % 8 == 0 and x % 8 < 2) or (x % 8 == 0 and y % 8 == 1):
        return FLOOR["t"]
    return FLOOR["T"]


def floor(fn, shade=None):
    """16x16 floor tile; `shade(x, y)` -> True where an object's shadow falls."""
    a = Art()
    for y in range(16):
        for x in range(16):
            c = fn(x, y)
            a.px[y][x] = SHADE[c] if shade and shade(x, y) else c
    return a


def edge(fn, side):
    """Open side of the hall: floor, kerb, covered drain, then the void. side in S, W, E, SW, SE."""
    a = Art()
    for y in range(16):
        for x in range(16):
            # distance past the kerb line, per axis (None = this axis has no edge)
            ds = y - 9 if "S" in side else None
            dw = 6 - x if "W" in side else (x - 9 if "E" in side else None)
            d = max(v for v in (ds, dw) if v is not None)
            along = x if d == ds else y
            if d < 0:
                c = fn(x, y)
            elif d == 0 or d == 3:
                c = FLOOR["K"]
            elif d in (1, 2):
                c = FLOOR["K"] if (d == 2 and along % 3 == 1) else FLOOR["S" if d == 1 else "s"]
            else:
                c = FLOOR["X"]
            a.px[y][x] = c
    return a


VOID = Art(fill=FLOOR["X"])

EXIT_STEPS = bands(FLOOR, "t T*2 D t T*2 D")   # rows 8-15 of the exit tile


# ================================================================== stall shell (pal 7)
FASCIA = bands(SHELL, "N*2 K W C*8 c x K n")


def back_wall(shelf=False):
    """White ceramic tiles (8 px) behind the hawker; optional steel shelf at y9."""
    a = Art()
    for y in range(16):
        for x in range(16):
            if y == 0:
                c = "x"
            elif y == 1:
                c = "c"
            elif y == 15:
                c = "K"
            elif y == 14:
                c = "x"
            elif y % 8 == 5 or x % 8 == 7:
                c = "c"
            else:
                c = "C"
            a.px[y][x] = SHELL[c]
    if shelf:
        a.rect(0, 9, 15, 9, SHELL["W"])
        a.rect(0, 10, 15, 10, SHELL["l"])
        a.rect(0, 11, 15, 11, SHELL["d"])
        a.rect(0, 12, 15, 12, SHELL["x"])
    return a


def kitchen_floor(wall=None):
    """Grey non-slip tiles inside a stall. wall='W'/'E' adds the stall's outer wall top."""
    a = Art()
    for y in range(16):
        for x in range(16):
            c = "o" if (x % 8 == 7 or y % 8 == 7 or y == 0) else "d"
            a.px[y][x] = SHELL[c]
    if wall:
        cols = (0, 1, 2) if wall == "W" else (15, 14, 13)
        for y in range(16):
            a.px[y][cols[0]] = SHELL["c"]
            a.px[y][cols[1]] = SHELL["C"]
            a.px[y][cols[2]] = SHELL["K"]
    return a


COUNTER = bands(SHELL, "K W l*4 M d M*6 d K")
for _y in range(8, 14):
    COUNTER.px[_y][0] = SHELL["l"]
    COUNTER.px[_y][15] = SHELL["d"]


def vcounter(part, side="W"):
    """Counter running north-south (side stalls), seen from above; the south end shows its
    front. side='W': stall on the west side of the hall, customers to the east ('E' = mirrored).
    The middle piece carries a pick-up tray."""
    a = Art()
    for y in range(16):
        a.px[y] = [SHELL[c] for c in "KWlllllllllllMdK"]
    if part == "top":
        a.rect(0, 0, 15, 0, SHELL["K"])
        a.rect(1, 1, 13, 1, SHELL["W"])
    if part in ("top", "mid"):
        a.rect(1, 15, 13, 15, SHELL["M"])
    if part == "mid":
        a.blit(art(SHELL, """
KKKKKKKKKK
KttttttttK
KTKKKKTTTK
KKWWWWKTTK
KKWllWKTTK
KTKKKKTTeK
KTTTTTTeeK
KKKKKKKKKK
""", w=10), 3, 4)
    if part == "bot":
        a.blit(bands(SHELL, "d M*3 d K"), 0, 10)
        for y in range(11, 14):
            a.px[y][0] = SHELL["l"]
            a.px[y][15] = SHELL["d"]
    return a.hflip() if side == "E" else a


PILLAR_COLS = "KWlllllllllMMMdK"


def pillar(part):
    """Concrete column between stalls: 'top' passes the fascia, 'mid', 'plate' (unit number),
    'base' (teal painted foot, sits in the counter row)."""
    a = Art()
    for y in range(16):
        a.px[y] = [SHELL[c] for c in PILLAR_COLS]
    if part == "top":
        a.blit(bands(SHELL, "N*2 K"), 0, 0)
        a.rect(1, 3, 14, 3, SHELL["W"])
        a.rect(1, 6, 14, 6, SHELL["d"])
        a.rect(1, 7, 14, 7, SHELL["M"])
    if part == "plate":
        a.blit(art(SHELL, """
KKKKKKKKKK
KeeeeeeeeK
KeWWeWeWeK
KeWeeWeWeK
KeWWeWWWeK
KeeeeeeeeK
KKKKKKKKKK
""", w=10), 3, 4)
    if part == "base":
        a.blit(bands(SHELL, "d t T*7 e e K", w=14), 1, 4)
        a.rect(0, 15, 15, 15, SHELL["K"])
    return a


LOW_WALL = bands(SHELL, "K W C*3 c K C*2 t T*3 e x K")

# Generic back-wall props (top layer, shell palette)
WALL_MENU = art(SHELL, """
................
................
.KKKKKKKKKKKKKK.
.KNNNNNNNNNNNNK.
.KNWWWNYYNWWWNK.
.KNNNNNNNNNNNNK.
.KNWWWWNYNWWNNK.
.KNNNNNNNNNNNNK.
.KNWWNNYYNWWWNK.
.KNNNNNNNNNNNNK.
.KKKKKKKKKKKKKK.
""")
WALL_BOWLS = art(SHELL, """
................
................
................
................
..KKKKK..KKKK...
..KWWWK..KttK...
..KlllK.KKTTKK..
.KKWWWKKKtttTK..
.KWWWWlKKTTTeK..
""")
WALL_UTENSILS = art(SHELL, """
................
................
KKKKKKKKKKKKKKKK
ddddddddddddddd.
.K...K...K...K..
.K..KlK..K..KMK.
.K..KlK.KlK.KMK.
KlK.KlK.KlK.KMK.
KlK..K..KlK..K..
KlK......K......
.K..............
""")

# Railings along the open sides (top layer)
RAIL_S = art(SHELL, """
................
llllllllllllllll
dddddddlKddddddd
.......lK.......
MMMMMMMlKMMMMMMM
.......lK.......
.......lK.......
.......lK.......
......KKKK......
""")
RAIL_W = Art()
for _y in range(16):
    RAIL_W.put(3, _y, SHELL["l"])
    RAIL_W.put(4, _y, SHELL["d"])
RAIL_W.blit(art(SHELL, """
KKKK
KllK
KldK
KKKK
""", w=4), 2, 6)
RAIL_E = RAIL_W.hflip()

# Roof column standing on the kerb of an open side: 16x32, feet on the edge tile.
ROOF_PILLAR = art(SHELL, """
................
................
................
................
................
................
...KKKKKKKKKK...
...KWllllllMK...
...KlMMMMMMdK...
....KKKKKKKK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KWllllMK....
....KtTTTTeK....
....KtTTTTeK....
...KKKKKKKKKK...
...KWllllllMK...
...KKKKKKKKKK...
""", h=32)

# ================================================================== furniture (pal 8, top layer)
STOOL = art(FURN, """
................
................
................
................
....KKKKKKKK....
...KppppppOOK...
..KpOOOOOOOOoK..
..KOOOOOOOOOoK..
..KoOOOOOOOooK..
...KooooooooK...
....KKKddKKK....
......KlMK......
......KlMK......
....KKKlMKKK....
....KlMMMMdK....
.....KKKKKK.....
""")
STOOL_TEAL = STOOL.recolour({FURN["o"]: FURN["e"], FURN["O"]: FURN["T"], FURN["p"]: FURN["t"]})


def stool_shadow(x, y):
    return (y in (14, 15) and 11 <= x <= 13) or (y == 15 and 4 <= x <= 13)


TABLE_ROUND = art(FURN, """
................
...KKKKKKKKKK...
..KWWWWWWWWWWK..
.KWWWWWWWWWWWWK.
.KWWWWWWWWWWWlK.
.KWWWWWWWWWWllK.
.KlWWWWWWWWlllK.
.KTllllllllllTK.
.KeTTTTTTTTTTeK.
..KeeeeeeeeeeK..
...KKKKddKKKK...
......KlMK......
......KlMK......
....KKKlMKKK....
...KlMMMMMMdK...
....KKKKKKKK....
""")


def table_shadow(x, y):
    return (y in (13, 14, 15) and 12 <= x <= 14) or (y == 15 and 3 <= x <= 14) or \
           (10 <= y <= 12 and 10 <= x <= 13)


def long_table(part):
    """Long table, any length: 'l' / 'm' / 'r'. Legs under the end pieces."""
    a = Art()
    a.blit(bands(FURN, "K W*5 l T e K"), 0, 1)
    if part in "lr":
        a.blit(art(FURN, """
KdMK
KdMK
KdMK
KKKK
""", w=4), 2, 11)
        for y in range(2, 10):
            a.px[y][0] = FURN["K"]
        a.px[1][0] = None
        a.px[10][0] = None
    return a.hflip() if part == "r" else a


def long_table_shadow(part):
    def f(x, y):
        if y == 11 or (y == 12 and x % 2 == 0):
            return True
        return False
    return f


# tableware stamps (pal 8)
BOWL_LAKSA = art(FURN, """
.KKKKKK.
KOROYOOK
KWOOOOWK
.KWWWWK.
..KKKK..
""", w=8)
BOWL_SOUP = BOWL_LAKSA.recolour({FURN["O"]: FURN["c"], FURN["R"]: FURN["T"], FURN["Y"]: FURN["c"]})
PLATE_RICE = art(FURN, """
..KKKKK..
.KWWcBBK.
KlWWWBcWK
.KlllllK.
..KKKKK..
""", w=9)
CUP_KOPI = art(FURN, """
KKKK.
KBBKK
KWWKK
KKKK.
""", w=5)
TISSUE = art(FURN, """
KKKKKK
KWTTWK
KWWWWK
KKKKKK
""", w=6)
CHOPSTICKS = art(FURN, """
KKKK
KooK
KMMK
KMMK
KKKK
""", w=4)

TRAY_RETURN = art(FURN, """
................
................
.KKKKKKKKKKKKKK.
.KllllllllllllK.
.KMMMMMMMMMMMMK.
.KKKKKKKKKKKKKK.
.KdTTTTTTTTTTdK.
.KdeeeeeeeeeedK.
.KdTTTTTTTTTTdK.
.KdeeeeeeeeeedK.
.KddddddddddddK.
.KKKKKKKKKKKKKK.
.KdOOOOOOOOOOdK.
.KdooooooooooodK
.KdOOOOOOOOOOdK.
.KdooooooooooodK
.KddddddddddddK.
.KKKKKKKKKKKKKK.
.KdWWWlWWWlWWdK.
.KdWWWlWWWlWWdK.
.KdlllMlllMlldK.
.KdTTTTTTTTTTdK.
.KdeeeeeeeeeedK.
.KddddddddddddK.
.KKKKKKKKKKKKKK.
.KlMMMMMMMMMMdK.
.KlMMMMMMMMMMdK.
.KKKKKKKKKKKKKK.
..Kd........dK..
..Kd........dK..
.KKKK......KKKK.
.KKKK......KKKK.
""", h=32)
for _y in (13, 15):
    TRAY_RETURN.px[_y][14] = FURN["K"]
    TRAY_RETURN.px[_y][15] = None

BIN = art(FURN, """
................
................
................
...KKKKKKKKKK...
..KttttttttttK..
..KTTKKKKKKTTK..
..KTTKddddKTTK..
..KKKKKKKKKKKK..
...KtTTTTTTeK...
...KtTTWWTTeK...
...KtTWTTWTeK...
...KtTTWWTTeK...
...KtTTTTTTeK...
...KtTTTTTTeK...
...KKeeeeeeKK...
....KKKKKKKK....
""")

BASIN = art(FURN, """
................
......KKKK......
.....KlKKdK.....
.....KK..KK.....
......K..Kl.....
.KKKKKKKKKKKKKK.
.KWWWWWWWWWWWlK.
.KWlMMMMMMMMWlK.
.KWlMddddddMWlK.
.KWWlMMMMMMWWlK.
.KlWWWWWWWWWllK.
..KKKKKKKKKKKK..
...KlllllllMK...
...KlllllllMK...
...KlllllllMK...
...KKKKKKKKKK...
""")


def box_shadow(x, y):
    return y == 15 and 4 <= x <= 14 or (x in (13, 14) and y in (13, 14))


def outer_wall(side):
    """Void with the top of a side stall's outer wall along the inner edge (floor-palette cream)."""
    a = VOID.copy()
    cols = (12, 13, 14, 15) if side == "W" else (3, 2, 1, 0)
    for y in range(16):
        for x, c in zip(cols, "KHFK"):
            a.px[y][x] = FLOOR[c]
    return a


POTTED_PALM = art(FLOOR, """
....V....V......
...VgV..VgV.VV..
.VVVgyVVgyVVgV..
VgyVVgyygVgyV...
.VVgyVgyVgVV....
...VVgyygyVVV...
..VgyVgVgVgyyV..
.VgVVVgyVVVVgV..
..V..VgV....V...
....KKKKKKK.....
....KtTTTDK.....
....KTTTTDK.....
.....KTTDK......
.....KTTDK......
.....KKKKK......
""", anchor="bottom")
