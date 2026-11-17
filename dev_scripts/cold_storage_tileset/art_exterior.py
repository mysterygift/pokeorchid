"""Exterior art for the Tosa Port Cold Storage: the FRLG Rocket Warehouse silhouette (corrugated
roof with scalloped eave, low ribbed wall with a vent band, sliding double door carrying an
emblem) redrawn as an insulated cold store in ice blue. One palette (Slateport slot 12)."""
from kit import Art, art, legend, tiled

EXT = legend(
    K=(64, 72, 104),      # outline (Slateport's building outline)
    n=(40, 48, 88),       # deep navy: vents, eave shadow, open doorway
    a=(64, 112, 160), b=(104, 160, 208), c=(152, 200, 232), e=(208, 232, 248),   # roof ramp
    s=(136, 144, 168), m=(184, 192, 208), l=(216, 224, 232), W=(248, 248, 248),  # panel wall
    d=(96, 104, 136),     # dark steel
    o=(232, 112, 64), y=(248, 208, 88),                                          # warning colours
    t=(56, 168, 192),     # emblem cyan
)
E = EXT

RIB = "abceeccb"                 # one roof corrugation (8 px)
WALL = "lm"                      # fine wall ribbing

SNOW7 = """
...t...
.t.t.t.
..ttt..
ttttttt
..ttt..
.t.t.t.
...t...
"""


def snowflake():
    return art(E, SNOW7, w=7, h=7)


def building(cells=3):
    """cells x 5 metatile canvas: 3 roof rows + 2 wall rows; column 0 = left end, last = right end."""
    w = cells * 16
    a = Art(w, 80)
    # ---- roof (rows 0-2)
    a.blit(tiled(E, [RIB], w, 41))
    a.rect(0, 0, w - 1, 0, E["K"])
    a.rect(0, 1, w - 1, 1, E["e"])
    a.rect(0, 2, w - 1, 2, E["c"])
    for x in range(w):                                   # ridge: grooves start a little lower
        if RIB[x % 8] in "a":
            a.put(x, 2, E["b"])
    for x in range(w):                                   # scalloped rib ends
        ch = RIB[x % 8]
        a.put(x, 41, E[ch] if ch in "ce" else E["n"])
        a.put(x, 42, E[ch] if ch == "e" else E["n"])
    a.rect(0, 43, w - 1, 43, E["n"])
    a.rect(0, 44, w - 1, 44, E["a"])
    a.rect(0, 45, w - 1, 45, E["b"])
    a.rect(0, 46, w - 1, 46, E["a"])
    a.rect(0, 47, w - 1, 47, E["K"])
    a.rect(0, 0, 0, 47, E["K"]), a.rect(w - 1, 0, w - 1, 47, E["K"])
    a.rect(1, 1, 1, 42, E["e"]), a.rect(w - 2, 1, w - 2, 42, E["a"])
    # ---- wall (rows 3-4)
    a.blit(tiled(E, [WALL], w, 32), 0, 48)
    a.rect(0, 48, w - 1, 52, E["s"])                     # vent band
    for cx in range(cells):
        a.rect(cx * 16 + 3, 49, cx * 16 + 12, 51, E["n"])
        a.rect(cx * 16 + 3, 49, cx * 16 + 12, 49, E["K"])
    a.rect(0, 53, w - 1, 53, E["W"])
    a.rect(0, 54, w - 1, 54, E["m"])
    y = 64 + 9                                           # plinth
    for dy, ch in enumerate("WmKsdsK"):
        a.rect(0, y + dy, w - 1, y + dy, E[ch])
    # corner posts
    for x, ch in ((0, "K"), (1, "W"), (2, "l"), (3, "s")):
        a.rect(x, 48, x, 79, E[ch])
    for x, ch in ((w - 1, "K"), (w - 2, "s"), (w - 3, "m"), (w - 4, "s")):
        a.rect(x, 48, x, 79, E[ch])
    a.rect(0, 79, w - 1, 79, E["K"])
    return a


def door(open_px=0):
    """16x32 door column (wall rows 3-4). open_px = how far each leaf has slid (0 closed, 7 open)."""
    a = building(3).crop(16, 48, 16, 32)
    top, bot = 7, 27                                     # door frame rows
    a.rect(0, top, 15, bot, E["K"])
    a.rect(1, top + 1, 14, bot, E["n"])                  # the dark interior behind the leaves
    leaf = Art(7, bot - top - 1)
    leaf.rect(0, 0, 6, leaf.h - 1, E["l"])
    leaf.rect(0, 0, 6, 0, E["W"])
    leaf.rect(0, leaf.h - 3, 6, leaf.h - 1, E["m"])
    leaf.rect(0, leaf.h - 1, 6, leaf.h - 1, E["s"])
    left, right = leaf.copy(), leaf.copy()
    left.rect(6, 0, 6, leaf.h - 1, E["d"])               # meeting edge
    right.rect(0, 0, 0, leaf.h - 1, E["W"])
    flake = snowflake()
    left.blit(flake.crop(0, 0, 4, 7), 3, 4)              # emblem split across the two leaves
    right.blit(flake.crop(4, 0, 3, 7), 0, 4)
    left.rect(4, 13, 5, 14, E["d"])                      # handles
    right.rect(1, 13, 2, 14, E["d"])
    lw, rw = 7 - open_px, 7 - open_px
    if lw > 0:
        a.blit(left.crop(open_px, 0, lw, leaf.h), 1, top + 1)
        a.blit(right.crop(0, 0, rw, leaf.h), 8 + open_px, top + 1)
    # threshold step
    for dy, ch in enumerate("KWlsK"):
        a.rect(0, bot + dy, 15, bot + dy, E[ch])
    if open_px:
        a.rect(1 + lw, bot + 1, 14 - rw, bot + 2, E["m"])
    return a


def sign():
    """Upper-wall metatile with the cold-store plate: white plate, cyan snowflake, blue bars."""
    a = building(3).crop(16, 48, 16, 16)
    a.rect(1, 6, 14, 15, E["K"])
    a.rect(2, 7, 13, 14, E["W"])
    a.rect(2, 14, 13, 14, E["l"])
    a.blit(snowflake(), 2, 7)
    a.rect(10, 8, 12, 8, E["a"]), a.rect(10, 10, 12, 10, E["b"]), a.rect(10, 12, 12, 12, E["a"])
    return a


def gauge():
    """Upper-wall metatile with a round thermometer dial and a warning lamp."""
    a = building(3).crop(16, 48, 16, 16)
    dial = art(E, """
..KKKK..
.KWWWWK.
KWWWtWWK
KWWtWWWK
KWoWWWWK
KWWWWWWK
.KWWWWK.
..KKKK..
""", w=8, h=8)
    a.blit(dial, 2, 7)
    a.rect(12, 8, 13, 9, E["o"]), a.rect(12, 7, 13, 7, E["K"]), a.rect(12, 10, 13, 10, E["K"])
    a.rect(11, 8, 11, 9, E["K"]), a.rect(14, 8, 14, 9, E["K"])
    return a


def roof_unit():
    """Roof metatile with a condenser box and fan."""
    a = building(3).crop(16, 16, 16, 16)
    box = art(E, """
.KKKKKKKKKKKK.
KWWWWWWWWWWWWK
KllKKKKlllldlK
KlKddddKlllllK
KlKdnndKlldllK
KlKdnndKlllllK
KlKddddKlldllK
KmmKKKKmmmmmmK
KssssssssssssK
.KKKKKKKKKKKK.
nnnnnnnnnnnnnn
""", w=14, h=11)
    a.blit(box, 1, 3)
    return a


def skylight():
    """Roof metatile with a frosted skylight."""
    a = building(3).crop(16, 16, 16, 16)
    a.rect(2, 3, 13, 12, E["K"])
    a.rect(3, 4, 12, 11, E["e"])
    a.rect(3, 4, 12, 4, E["W"])
    for i in range(6):
        a.put(4 + i, 10 - i, E["W"]), a.put(7 + i, 10 - i, E["c"])
    a.rect(2, 13, 13, 13, E["n"])
    return a


def shutter():
    """32x32 roller shutter (wall rows 3-4, two metatiles wide) for the loading bay."""
    a = building(4).crop(16, 48, 32, 32)
    top, bot = 6, 27
    a.rect(0, top, 31, bot, E["K"])
    a.rect(1, top + 1, 30, top + 2, E["d"])              # roller housing
    a.rect(1, top + 1, 30, top + 1, E["s"])
    for y in range(top + 3, bot + 1):
        ch = "lllm"[(y - top - 3) % 4]
        a.rect(2, y, 29, y, E[ch])
    a.rect(1, top + 3, 1, bot, E["d"]), a.rect(30, top + 3, 30, bot, E["d"])   # guide rails
    for x in range(2, 30):                               # hazard strip along the bottom slat
        for y in (bot - 2, bot - 1, bot):
            a.put(x, y, E["y"] if ((x + y) // 3) % 2 == 0 else E["K"])
    a.rect(13, bot - 6, 18, bot - 5, E["d"])             # lift handle
    for dy, ch in enumerate("KWlsK"):
        a.rect(0, bot + dy, 31, bot + dy, E[ch])
    return a
