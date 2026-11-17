"""Interior art for gTileset_ColdStorage: steel deck and ice floors, insulated panel walls,
shipping containers (one set of tiles, four palettes) and loose props to stop a slide against."""
from kit import Art, art, legend, tiled, BLACK

INK = (80, 80, 104)

# pal 6: everything the player walks on, plus the void
FLOOR = legend(
    K=INK,
    a=(112, 120, 144), b=(144, 152, 172), c=(164, 172, 190), e=(196, 204, 216),   # steel deck
    p=(88, 96, 124), q=(116, 124, 148),                                           # ... in shade
    y=(240, 200, 64), Y=(184, 136, 40),                                           # lane paint
    i=(104, 160, 216), j=(144, 196, 236), k=(188, 224, 248), l=(224, 244, 248),   # ice
    W=(248, 248, 248),
)
FLOOR["X"] = BLACK
# pal 7: walls, wall-mounted plant, frost
WALL = legend(
    K=INK,
    a=(120, 136, 168), b=(168, 184, 208), c=(208, 220, 232), e=(240, 244, 248),   # panels
    n=(56, 64, 88), N=(36, 40, 60),                                               # wall tops, grilles
    i=(160, 208, 240), I=(96, 160, 216),                                          # ice, coolant pipes
    r=(224, 72, 64), g=(88, 200, 120), y=(240, 200, 64),
)
WALL["X"] = BLACK


def container_pal(ramp):
    """Container palettes share slots, so all four colours are the same tiles."""
    d = legend(K=INK)
    d.update(zip("12345", (tuple(min(248, (v + 4) // 8 * 8) for v in c) for c in ramp)))
    d.update(legend(d=(96, 104, 128), M=(160, 168, 184), l=(216, 224, 232), W=(248, 248, 248),
                    y=(240, 200, 64), n=(48, 52, 76), f=(232, 244, 248), i=(160, 208, 240)))
    return d


RUST = ((112, 40, 40), (160, 56, 48), (200, 80, 56), (228, 116, 76), (248, 164, 124))
GREEN = ((24, 80, 72), (40, 112, 96), (64, 148, 112), (104, 180, 136), (160, 216, 168))
AMBER = ((128, 80, 24), (176, 120, 32), (216, 160, 48), (240, 196, 88), (248, 228, 152))
NAVY = ((40, 48, 104), (56, 72, 144), (80, 104, 176), (112, 140, 204), (160, 184, 232))
C_RUST, C_GREEN, C_AMBER, C_NAVY = (container_pal(r) for r in (RUST, GREEN, AMBER, NAVY))
CONTAINERS = {"Rust": C_RUST, "Green": C_GREEN, "Amber": C_AMBER, "Navy": C_NAVY}

# pal 12: loose props
PROP = legend(
    K=INK,
    u=(112, 72, 48), v=(160, 108, 64), w=(200, 152, 96), x=(232, 196, 144),       # timber
    d=(96, 104, 128), M=(160, 168, 184), l=(216, 224, 232), W=(248, 248, 248),    # steel
    i=(104, 168, 216), j=(160, 208, 240), k=(208, 236, 248),                      # ice
    r=(224, 72, 64), y=(240, 200, 64), n=(48, 52, 76),
)

LEGENDS = {6: FLOOR, 7: WALL, 8: C_RUST, 9: C_GREEN, 10: C_AMBER, 11: C_NAVY, 12: PROP}

F, Wl, P = FLOOR, WALL, PROP


# ------------------------------------------------------------------ floors
def deck():
    """Diamond-plate steel deck, one panel per tile."""
    a = Art(16, 16, F["b"])
    a.rect(0, 0, 15, 0, F["c"]), a.rect(0, 0, 0, 15, F["c"])
    a.rect(0, 15, 15, 15, F["a"]), a.rect(15, 0, 15, 15, F["a"])
    for j in range(3):
        for i in range(3):
            x, y = 3 + 4 * i + (1 if j == 1 else 0), 3 + 4 * j
            if (i + j) % 2 == 0:
                a.put(x, y, F["e"]), a.put(x + 1, y + 1, F["c"])
            else:
                a.put(x + 1, y, F["e"]), a.put(x, y + 1, F["c"])
    return a


def ice(variant=0):
    a = Art(16, 16, F["j"])
    for y in range(16):
        for x in range(16):
            t = (x + y + (5 if variant else 0)) % 16
            if t in (3, 4, 5):
                a.put(x, y, F["k"])
            if t == 4:
                a.put(x, y, F["l"])
            if t == 11 and variant == 0:
                a.put(x, y, F["k"])
    if variant == 0:
        a.put(9, 11, F["W"]), a.put(2, 2, F["W"])
        a.put(12, 5, F["i"]), a.put(13, 5, F["i"]), a.put(5, 13, F["i"])
    else:
        a.put(3, 8, F["W"]), a.put(12, 15, F["W"])
        a.put(6, 3, F["i"]), a.put(7, 4, F["i"]), a.put(13, 10, F["i"])
    return a


SHADE = {F["b"]: F["q"], F["c"]: F["q"], F["e"]: F["a"], F["a"]: F["p"],
         F["j"]: F["i"], F["k"]: F["j"], F["l"]: F["k"], F["W"]: F["k"],
         F["y"]: F["Y"]}


def shaded(a, north=False, west=False):
    """Bake the shadow of a wall/container to the north and/or west into a floor tile."""
    out = a.copy()
    for y in range(16):
        for x in range(16):
            if (north and y < 4) or (west and x < 3):
                out.px[y][x] = SHADE.get(a.px[y][x], a.px[y][x])
    return out


def wet():
    """Thawed deck: puddles of meltwater on the steel."""
    a = deck()
    blobs = art(F, """
................
....jjjj........
..jjkkkjjj......
.jjkkjjjjjj.....
..jjjjjjj.......
....jjj.....jj..
..........jjkjj.
.........jjkkjjj
..........jjjjj.
...jj.......j...
..jkjj..........
.jjkjjj.........
..jjjj..........
................
""")
    return a.blit(blobs)


def frosty():
    """Deck with a crust of frost creeping in (decor, not slippery)."""
    a = deck()
    return a.blit(art(F, """
lWl.........lWWl
Wl...........lWW
l.............ll
................
................
................
................
................
................
................
................
l...............
Wl...........l..
WWl.........lWl.
lWWl.......lWWWl
""", h=16))


def lane(vertical=False):
    a = deck()
    if vertical:
        a.rect(7, 0, 8, 15, F["y"]), a.rect(9, 0, 9, 15, F["Y"])
    else:
        a.rect(0, 7, 15, 8, F["y"]), a.rect(0, 9, 15, 9, F["Y"])
    return a


def hazard():
    """Yellow/dark chevrons across the top of a deck tile (in front of gates and doors)."""
    a = deck()
    for y in range(1, 6):
        for x in range(16):
            a.put(x, y, F["y"] if ((x + y) // 3) % 2 == 0 else F["p"])
    a.rect(0, 0, 15, 0, F["Y"]), a.rect(0, 6, 15, 6, F["Y"])
    return a


def drain():
    a = deck()
    a.rect(3, 4, 12, 11, F["K"])
    for y in range(5, 11):
        for x in range(4, 12):
            a.put(x, y, F["p"] if x % 2 == 0 else F["a"])
    return a


def void():
    return Art(16, 16, F["X"])


def exit_mat():
    """South doorway: deck running out under the door frame, light spilling in."""
    a = deck()
    a.rect(0, 10, 15, 15, F["e"])
    a.rect(0, 10, 15, 10, F["c"])
    for x in range(0, 16, 4):
        a.rect(x, 12, x + 1, 15, F["W"])
    a.rect(0, 0, 0, 15, F["K"]), a.rect(15, 0, 15, 15, F["K"])
    return a


# ------------------------------------------------------------------ walls
def cap(n=False, s=False, w=False, e=False, corner=None):
    """Top of a wall seen from above. Flags say which sides face the room (get a rim)."""
    a = Art(16, 16, Wl["n"])
    if s:
        a.rect(0, 14, 15, 14, Wl["a"]), a.rect(0, 15, 15, 15, Wl["K"])
    if n:
        a.rect(0, 1, 15, 1, Wl["a"]), a.rect(0, 0, 15, 0, Wl["K"])
    if e:
        a.rect(14, 0, 14, 15, Wl["a"]), a.rect(15, 0, 15, 15, Wl["K"])
    if w:
        a.rect(1, 0, 1, 15, Wl["a"]), a.rect(0, 0, 0, 15, Wl["K"])
    if corner == "se":      # room is to the south-east: rim turns the inside corner
        a.rect(14, 14, 15, 14, Wl["a"]), a.rect(14, 15, 14, 15, Wl["a"]), a.put(15, 15, Wl["K"])
    if corner == "sw":
        a.rect(0, 14, 1, 14, Wl["a"]), a.rect(1, 15, 1, 15, Wl["a"]), a.put(0, 15, Wl["K"])
    if corner == "ne":
        a.rect(14, 1, 15, 1, Wl["a"]), a.rect(14, 0, 14, 0, Wl["a"]), a.put(15, 0, Wl["K"])
    if corner == "nw":
        a.rect(0, 1, 1, 1, Wl["a"]), a.rect(1, 0, 1, 0, Wl["a"]), a.put(0, 0, Wl["K"])
    return a


def wall(cells=1):
    """cells x 2 canvas of insulated panel wall: one panel per tile, kick plate along the floor."""
    w = cells * 16
    a = Art(w, 32, Wl["c"])
    a.rect(0, 0, w - 1, 1, Wl["a"])                      # shadow under the wall top
    a.rect(0, 2, w - 1, 2, Wl["b"])
    for cx in range(cells):
        x = cx * 16
        a.rect(x, 3, x, 24, Wl["e"])                     # panel highlight
        a.rect(x + 15, 2, x + 15, 24, Wl["b"])           # panel seam
        for y in (6, 21):
            a.put(x + 2, y, Wl["a"]), a.put(x + 13, y, Wl["a"])   # rivets
    a.rect(0, 25, w - 1, 25, Wl["b"])
    a.rect(0, 26, w - 1, 26, Wl["K"])
    a.rect(0, 27, w - 1, 30, Wl["a"])                    # kick plate
    a.rect(0, 27, w - 1, 27, Wl["b"])
    a.rect(0, 31, w - 1, 31, Wl["K"])
    return a


def frost_line(w, seed=0):
    """Frost and icicles hanging off something `w` px wide (transparent art, 8 rows)."""
    a = Art(w, 8)
    lens = [3, 1, 5, 2, 1, 4, 2, 6, 1, 3, 2, 1, 5, 2, 4, 1]
    for x in range(w):
        a.put(x, 0, Wl["e"])
        n = lens[(x * 7 + seed * 5) % 16] if x % 2 == seed % 2 else 0
        for y in range(1, n + 1):
            a.put(x, y, Wl["i"] if y == n and n > 2 else Wl["e"])
    return a


def wall_pipes():
    """Coolant pipe run along the upper wall, rimed with frost."""
    a = wall(1)
    for y, ch in ((6, "K"), (7, "i"), (8, "I"), (9, "I"), (10, "K"), (13, "K"), (14, "i"), (15, "I"), (16, "K")):
        a.rect(0, y, 15, y, Wl[ch])
    a.rect(7, 5, 8, 17, Wl["K"])                         # bracket
    a.blit(frost_line(16, 1), 0, 17)
    a.rect(0, 6, 5, 6, Wl["e"]), a.rect(10, 6, 15, 6, Wl["e"])
    return a


def wall_vent():
    """Evaporator unit: grille, fan, frost and icicles underneath."""
    a = wall(2)
    a.rect(2, 4, 29, 19, Wl["K"])
    a.rect(3, 5, 28, 18, Wl["b"])
    a.rect(3, 5, 28, 5, Wl["e"])
    for fx in (5, 18):                                   # two fan grilles
        a.rect(fx, 7, fx + 8, 16, Wl["K"])
        a.rect(fx + 1, 8, fx + 7, 15, Wl["n"])
        for y in (9, 11, 13):
            a.rect(fx + 1, y, fx + 7, y, Wl["N"])
        a.rect(fx + 3, 11, fx + 5, 12, Wl["a"])
    a.put(15, 8, Wl["g"]), a.put(16, 8, Wl["g"])
    a.blit(frost_line(26, 0), 3, 20)
    return a


def wall_frost():
    """Plain panels with frost creeping up from the floor and down from the top."""
    a = wall(1)
    a.blit(frost_line(16, 2), 0, 2)
    a.blit(art(Wl, """
...e....ee......
.eeee..eeee..ee.
eeeeeeeeeeeeeeee
""", h=3), 0, 23)
    return a


def wall_gauge():
    """Temperature panel: dial, readout, warning lamp."""
    a = wall(1)
    a.rect(2, 6, 13, 19, Wl["K"])
    a.rect(3, 7, 12, 18, Wl["b"])
    a.blit(art(Wl, """
.KKKK.
KeeeeK
KeeIeK
KeIeeK
KeeeeK
.KKKK.
""", w=6, h=6), 4, 8)
    a.rect(4, 15, 9, 17, Wl["N"]), a.rect(5, 16, 6, 16, Wl["i"]), a.put(8, 16, Wl["i"])
    a.rect(11, 9, 11, 10, Wl["r"]), a.rect(11, 13, 11, 14, Wl["g"])
    return a


# ------------------------------------------------------------------ containers
def container_h(leg, cells=3, tall=False, label=False):
    """Container lying east-west: roof 13 px, long side below. cells x 2 (or x 3 when stacked)."""
    w, h = cells * 16, 48 if tall else 32
    a = Art(w, h)
    c = lambda ch: leg[ch]                               # noqa: E731
    a.rect(0, 0, w - 1, 0, c("K"))
    a.rect(0, 1, w - 1, 1, c("5"))
    for y in range(2, 13):
        for x in range(w):
            a.put(x, y, c("3") if x % 4 == 3 else c("4"))
    a.rect(0, 12, w - 1, 12, c("3"))
    a.rect(0, 13, w - 1, 13, c("K"))
    a.rect(0, 14, w - 1, 14, c("4"))                     # top rail
    a.rect(0, 15, w - 1, 15, c("2"))
    for y in range(16, h - 4):
        for x in range(w):
            a.put(x, y, c("3324"[x % 4]))
    if tall:                                             # seam between the two stacked boxes
        for y, ch in ((27, "2"), (28, "1"), (29, "K"), (30, "4"), (31, "2")):
            a.rect(0, y, w - 1, y, c(ch))
    a.rect(0, h - 4, w - 1, h - 4, c("2"))               # bottom rail
    a.rect(0, h - 3, w - 1, h - 3, c("1"))
    a.rect(0, h - 2, w - 1, h - 2, c("K"))
    a.rect(0, h - 1, w - 1, h - 1, c("n"))
    # ends
    a.rect(0, 0, 0, h - 2, c("K")), a.rect(w - 1, 0, w - 1, h - 2, c("K"))
    a.rect(1, 1, 1, 12, c("5")), a.rect(w - 2, 2, w - 2, 12, c("3"))
    a.rect(1, 14, 1, h - 3, c("4")), a.rect(2, 16, 2, h - 3, c("2"))
    a.rect(w - 2, 14, w - 2, h - 3, c("1")), a.rect(w - 3, 16, w - 3, h - 3, c("2"))
    for cy in ([14, h - 5] + ([24, 30] if tall else [])):      # corner castings
        a.rect(1, cy, 3, cy + 2, c("M")), a.rect(w - 4, cy, w - 2, cy + 2, c("d"))
        a.put(2, cy + 1, c("d")), a.put(w - 3, cy + 1, c("n"))
    if label:
        for cx in range(1, cells - 1):
            x, y = cx * 16 + 3, h - 14
            a.rect(x, y, x + 9, y + 6, c("K"))
            a.rect(x + 1, y + 1, x + 8, y + 5, c("W"))
            a.rect(x + 2, y + 2, x + 4, y + 4, c("i")), a.put(x + 3, y + 3, c("W"))
            a.rect(x + 6, y + 2, x + 7, y + 2, c("d")), a.rect(x + 6, y + 4, x + 7, y + 4, c("d"))
    return a


def container_v(leg, rows=4):
    """Container lying north-south, doors facing the camera: 2 wide, `rows` tall (>= 3)."""
    w, h = 32, rows * 16
    a = Art(w, h)
    c = lambda ch: leg[ch]                               # noqa: E731
    top = h - 20                                         # first row of the door face
    a.rect(0, 0, w - 1, 0, c("K"))
    for y in range(1, top - 1):
        a.rect(0, y, w - 1, y, c("3") if y % 4 == 3 else c("4"))
    a.rect(0, 1, w - 1, 1, c("5"))
    a.rect(0, top - 2, w - 1, top - 2, c("3"))
    a.rect(0, top - 1, w - 1, top - 1, c("K"))
    a.rect(1, 1, 1, top - 2, c("5")), a.rect(w - 2, 2, w - 2, top - 2, c("3"))
    # door end
    a.rect(0, top, w - 1, h - 3, c("3"))
    a.rect(0, top, w - 1, top, c("4")), a.rect(0, top + 1, w - 1, top + 1, c("2"))
    a.rect(0, h - 5, w - 1, h - 5, c("2")), a.rect(0, h - 4, w - 1, h - 3, c("1"))
    a.rect(15, top + 2, 15, h - 5, c("1")), a.rect(16, top + 2, 16, h - 5, c("4"))   # door seam
    for bx in (5, 10, 20, 25):                           # locking bars
        a.rect(bx, top + 1, bx, h - 4, c("l")), a.rect(bx + 1, top + 1, bx + 1, h - 4, c("d"))
    for bx in (4, 9, 19, 24):                            # handles
        a.rect(bx, top + 9, bx + 3, top + 9, c("M")), a.rect(bx, top + 10, bx + 3, top + 10, c("d"))
    a.rect(12, top + 4, 13, top + 6, c("y")), a.rect(22, top + 4, 23, top + 6, c("W"))   # tags
    a.rect(1, top, 1, h - 3, c("4")), a.rect(w - 2, top, w - 2, h - 3, c("1"))
    for cy in (top, h - 5):
        a.rect(1, cy, 3, cy + 2, c("M")), a.rect(w - 4, cy, w - 2, cy + 2, c("d"))
    a.rect(0, h - 2, w - 1, h - 2, c("K"))
    a.rect(0, h - 1, w - 1, h - 1, c("n"))
    a.rect(0, 0, 0, h - 2, c("K")), a.rect(w - 1, 0, w - 1, h - 2, c("K"))
    return a


def roof_frost(seed=0):
    """Snow crust on a container roof (top layer, wall palette)."""
    pats = ["""
................
................
....eeee........
..eeeeeeee..ee..
.eeeieeeeeeeeee.
..eeeeeeeeieee..
....eeeeeee.....
.......ee.......
""", """
................
...........ee...
.ee......eeeeee.
eeeee...eeeeieee
eeieeee..eeeeee.
.eeeee.....ee...
...e............
................
"""]
    return art(Wl, pats[seed % 2], h=16)


def face_icicles(seed=0):
    """Icicles hanging off a container's top rail (top layer for the *_Bot row)."""
    a = Art(16, 16)
    return a.blit(frost_line(16, seed), 0, 0)


# ------------------------------------------------------------------ props (16x16, transparent)
CRATE = art(P, """
.KKKKKKKKKKKKKK.
KxxxxxxxxxxxxxxK
KxwwwwwwwwwwwwxK
KxwwwwwwwwwwwwxK
KxxxxxxxxxxxxxxK
KKKKKKKKKKKKKKKK
KwvvvvvvvvvvvvwK
KwvwwvvvvvvwwvwK
KwvvwwvvvvwwvvwK
KwvvvvwwwwvvvvwK
KwvvvvwwwwvvvvwK
KwvvwwvvvvwwvvwK
KwvwwvvvvvvwwvwK
KwvvvvvvvvvvvvwK
KuuuuuuuuuuuuuuK
.KKKKKKKKKKKKKK.
""")
CRATE_FROST = CRATE.over(art(P, """
................
.WWWWkW.....kWW.
.WWkW.........W.
.W..............
""", h=4))
ICE_BLOCK = art(P, """
.KKKKKKKKKKKKKK.
KkkkkkkkkkkkkWWK
KkWWkkkkkkkkkkWK
KkWkkkkkkkkkkkkK
KkkkkkkkkkkkkkkK
KjjjjjjjjjjjjjjK
KjkjjjjjjjjjjjiK
KjkjjjMMMMjjjjiK
KjjjjMMdMMMjMjiK
KjjjMMMMMMMMMjiK
KjjjjMMMMMMjMjiK
KjjjjjMMMMjjjjiK
KjjjjjjjjjjjkjiK
KjiiiiiiiiiiiiiK
.KKKKKKKKKKKKKK.
""")
BARREL = art(P, """
....KKKKKKKK....
..KKllllllllKK..
.KllMMMMMMMMllK.
.KlMMddddddMMlK.
.KKllMMMMMMllKK.
.KMKKllllllKKdK.
.KMlMKKKKKKMddK.
.KMlMMMMMMMMddK.
.KrrrrrrrrrrrrK.
.KMlMMMMMMMMddK.
.KMlMMMMMMMMddK.
.KrrrrrrrrrrrrK.
.KMlMMMMMMMMddK.
.KMlMMMMMMMMddK.
..KKMMMMMMMdKK..
....KKKKKKKK....
""")
CONE = art(P, """
................
.......KK.......
......KrrK......
......KrrK......
.....KWWWWK.....
.....KWWWWK.....
....KrrrrrrK....
....KrrrrrrK....
...KWWWWWWWWK...
...KrrrrrrrrK...
..KrrrrrrrrrrK..
.KKKKKKKKKKKKKK.
.KrrrrrrrrrrrrK.
.KKKKKKKKKKKKKK.
................
""")
FISH_BOXES = art(P, """
.KKKKKKKKKKKKKK.
KWWWWWWWWWWWWWWK
KWjjjjjjjjjjjjWK
KWjMMMkjjMMMkjWK
KWjjMMMjjjMMMjWK
KWjjjjjjjjjjjjWK
KWWWWWWWWWWWWWWK
KKKKKKKKKKKKKKKK
KllllllllllllllK
KlllljjjjjjllllK
KllllllllllllllK
KMMMMMMMMMMMMMMK
KKKKKKKKKKKKKKKK
.KvK..KvvK..KvK.
.KKK..KKKK..KKK.
""")
GATE = art(P, """
KKKKKKKKKKKKKKKK
KllllllllllllllK
KMMMMMMMMMMMMMMK
KKKKKKKKKKKKKKKK
KlKnKlKnnKlKnKlK
KMKnKMKnnKMKnKMK
KlKnKKKKKKKKnKlK
KMKnKyyyyyyKnKMK
KlKnKyyKKyyKnKlK
KMKnKyyKKyyKnKMK
KlKnKYYYYYYKnKlK
KMKnKKKKKKKKnKMK
KlKnKlKnnKlKnKlK
KKKKKKKKKKKKKKKK
KddddddddddddddK
KKKKKKKKKKKKKKKK
""", subs={"Y": "v"})


def console(on=True):
    """Free-standing coolant control desk: lever and status lamp."""
    lamp, lever_up = ("j", True) if on else ("r", False)
    a = art(P, """
.KKKKKKKKKKKKKK.
KllllllllllllllK
KlKKKKKlKKKKKKlK
KlKnnnKlKddddKlK
KlKnnnKlKddddKlK
KlKKKKKlKddddKlK
KllllllllKddddlK
KMMMMMMMMKKKKKMK
KKKKKKKKKKKKKKKK
KMMMMMMMMMMMMMMK
KMdMMMMMMMMMMdMK
KMMMMyyyyyyMMMMK
KMMMMMMMMMMMMMMK
KddddddddddddddK
.KKKKKKKKKKKKKK.
""")
    a.rect(3, 3, 5, 4, P[lamp])                          # status lamp
    a.put(3, 3, P["W"])
    ly = 3 if lever_up else 5                            # lever knob
    a.rect(10, ly, 11, ly + 1, P["r"])
    return a


WET_SIGN = art(P, """
................
.....KKKKKK.....
....KyyyyyyK....
....KyyKKyyK....
....KyyKKyyK....
...KyyyKKyyyK...
...KyyyKKyyyK...
...KyyyyyyyyK...
..KyyyyKKyyyyK..
..KyyyyyyyyyyK..
..KKKKKKKKKKKK..
..Kd........dK..
.KK..........KK.
................
""")
