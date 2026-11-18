"""
Station concourse kit for gTileset_UrbanInterior (imported by export_tileset.py).

Adds, from metatile 0x2B0 on (after the escalator block):
  * concourse back wall (2 rows), granite floor (A/B), tactile guide strips (V, H, blister pad)
  * fare gates for a north-south gate line: cabinet, gate passage (walk east-west), and a glass
    fence for an east-west run
  * ticket booth 3x4 (a building in the building): roof L/M/R over the lower wall row, roof
    front + fascia L/M/R, facade L/M/R (service window in the middle), counter L/M/R
  * waiting seat (the Battle Tent seat art, top layer, on the granite floor)
  * 2-wide exit mat (south arrow warp)
  * rear exit arch, 2 wide x 2 rows (north arrow warps on the bottom row)
  * station sign (single tile, train front on a navy plate, upper wall row)

Props follow Gen 3's 3/4 view: a tall lit top surface, a 2-3 row front band one shade darker,
blue-grey outline (80,80,104), and a 2-row floor shadow baked in.

The paid side of the gate line is floored with platform paving so the stock escalator metatiles
(0x280-0x2AD, also on the platform) sit on matching floor.

Palettes: 11 = wall fixtures (wall + steel + navy/amber/white), 12 = floor fixtures
(granite + tactile yellow + steel + seat blue + green). Plain concourse wall uses palette 6.
"""

INK = (40, 40, 56)
CDD, CD = (16, 24, 48), (32, 40, 64)                 # Tosa canopy_dd / canopy_d (ceiling band)
WD, W, WL = (48, 96, 120), (72, 128, 152), (112, 168, 184)
SDK, SMD, SLT = (96, 104, 120), (160, 168, 184), (208, 216, 224)
AMBER, WHITE, NAVY = (248, 200, 72), (248, 248, 248), (40, 56, 112)
GREEN = (72, 176, 96)
OUT = (80, 80, 104)                                  # vanilla interior outline
S1, S2, S3 = (120, 128, 144), (160, 168, 184), (208, 216, 224)   # steel: dark / mid / lit top
FHI, FL, FD, GROUT = (224, 224, 216), (200, 200, 192), (176, 176, 168), (144, 144, 136)
SHADOW = (160, 160, 152)
YEL, YEL_D = (248, 216, 80), (216, 168, 48)
BLUE, BLUE_D = (112, 184, 240), (96, 160, 216)       # Battle Tent seat blue (also acrylic/glass)

BLACK = (0, 0, 0)
PAL_FIXTURE = [BLACK, INK, CDD, CD, WD, W, WL, SDK, SMD, SLT, AMBER, WHITE, NAVY, OUT]
PAL_CONCOURSE = [BLACK, OUT, FHI, FL, FD, GROUT, YEL, YEL_D, S1, S2, S3, WHITE, GREEN, BLUE, BLUE_D,
                 SHADOW]

MB_NORMAL = 0x00
MB_NORTH_ARROW_WARP = 0x64
MB_SOUTH_ARROW_WARP = 0x65
MB_COUNTER = 0x80
LAYER_NORMAL, LAYER_COVERED = 0, 1

FIRST_ID = 0x2B0


class Tall:
    """16 x 32 canvas (two stacked metatiles)."""

    def __init__(self, h=32):
        self.h = h
        self.px = [[None] * 16 for _ in range(h)]

    def put(self, x, y, c):
        if 0 <= x < 16 and 0 <= y < self.h:
            self.px[y][x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def half(self, Block, i):
        b = Block()
        for y in range(16):
            for x in range(16):
                b.px[y][x] = self.px[i * 16 + y][x]
        return b


# ------------------------------------------------------------------ wall
def wall_px(x, y):
    """Concourse back wall, y = 0..31 over the two wall rows."""
    if y <= 1:
        return CDD
    if y == 2:
        return CD
    if y >= 28:
        return INK if y == 28 else CD                      # skirting
    yy = y - 3
    if yy % 4 == 3:
        return WD
    if (x + (4 if (yy // 4) % 2 else 0)) % 8 == 7:
        return WD
    return WL if yy % 4 == 0 else W


def wall_tall():
    t = Tall()
    for y in range(32):
        for x in range(16):
            t.put(x, y, wall_px(x, y))
    return t


def sign_upper(Block):
    """Single-tile station sign on the upper wall row: navy plate, white train front."""
    t = wall_tall()
    t.rect(2, 4, 13, 14, NAVY)
    for x, y in ((2, 4), (13, 4), (2, 14), (13, 14)):
        t.put(x, y, wall_px(x, y))
    t.rect(3, 15, 12, 15, WD)                              # shadow under the plate
    t.rect(5, 5, 10, 5, WHITE)                             # rounded roof
    t.rect(4, 6, 11, 11, WHITE)                            # body
    t.rect(5, 7, 6, 8, SLT)                                # two front windows
    t.rect(9, 7, 10, 8, SLT)
    t.put(5, 10, AMBER)
    t.put(10, 10, AMBER)                                   # headlights
    t.rect(5, 12, 10, 12, WHITE)                           # skirt
    t.rect(3, 13, 12, 13, SLT)                             # rail
    return t.half(Block, 0)


def arch_piece(Block, side, row):
    """Rear exit, 2 tiles wide x 2 rows (as wide as the front mats). side "L"/"R", row 0 top / 1 exit."""
    px = [[wall_px(x % 16, y) for x in range(32)] for y in range(32)]

    def rect(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px[y][x] = c

    rect(1, 4, 30, 31, SMD)                                # frame
    rect(2, 5, 29, 31, SDK)
    rect(3, 6, 29, 10, WHITE)                              # daylight at the far end
    rect(3, 11, 29, 13, SLT)
    rect(3, 14, 29, 31, SMD)                               # passage floor
    rect(3, 14, 29, 14, SDK)
    b = Block()
    off = 0 if side == "L" else 16
    for y in range(16):
        for x in range(16):
            b.put(x, y, px[row * 16 + y][off + x])
    return b


# ------------------------------------------------------------------ floor
SPECKS = {
    "A": {(4, 5), (11, 3), (7, 11), (2, 12), (13, 9)},
    "B": {(6, 3), (12, 12), (3, 8), (9, 7), (13, 4)},
}


def floor_px(x, y, v="A"):
    if y == 15 or x == 15:
        return GROUT
    if y == 0 or x == 0:
        return FHI
    return FD if (x, y) in SPECKS[v] else FL


def floor(Block, v="A"):
    b = Block()
    for y in range(16):
        for x in range(16):
            b.put(x, y, floor_px(x, y, v))
    return b


def shade(b, x0, y0, x1, y1):
    """Baked floor shadow: darken whatever floor tone is there."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if b.px[y][x] in (FHI, FL, FD):
                b.put(x, y, SHADOW)


def guide(Block, vertical):
    b = floor(Block)
    for y in range(16):
        for x in range(4, 12):
            a, c = (x, y) if vertical else (y, x)
            b.put(a, c, YEL_D if x in (4, 6, 9, 11) else YEL)
    return b


def blister(Block):
    """Warning pad: fills the whole tile so pads and strips run together; dots tile seamlessly."""
    b = Block()
    for y in range(16):
        for x in range(16):
            b.put(x, y, YEL_D if (x % 4 in (1, 2) and y % 4 == 1) else YEL)
    return b


# ------------------------------------------------------------------ fare gates
def gate_cabinet(Block):
    """Waist-high gate cabinet, 3/4 view: 9-row lit top, 3-row front band, floor shadow."""
    b = floor(Block)
    shade(b, 2, 14, 12, 15)                                # shadow falls straight down
    # silhouette x2..12, y0..13
    b.rect(3, 0, 11, 0, OUT)
    b.rect(2, 1, 2, 12, OUT)
    b.rect(12, 1, 12, 12, OUT)
    b.rect(3, 13, 11, 13, OUT)
    b.rect(3, 1, 11, 9, S3)                                # lit top
    b.rect(3, 1, 11, 1, WHITE)
    b.rect(3, 1, 3, 8, WHITE)
    b.rect(5, 3, 9, 6, BLUE_D)                             # card reader pad
    b.rect(6, 4, 8, 5, BLUE)
    b.put(10, 3, GREEN)                                    # go light
    b.put(10, 4, GREEN)
    b.rect(3, 10, 11, 10, S1)                              # lip
    b.rect(3, 11, 10, 12, S2)                              # front band
    b.rect(11, 11, 11, 12, S1)
    return b


def gate_passage(Block):
    """Gate between two cabinets stacked north-south; the player walks through east-west.
    Acrylic flaps reach in from the cabinets above and below (seen from above)."""
    b = floor(Block)
    for y0, y1 in ((0, 4), (11, 14)):
        b.rect(5, y0, 9, y1, BLUE)
        b.rect(5, y0, 5, y1, WHITE)
        b.rect(10, y0, 10, y1, OUT)
    b.rect(5, 15, 10, 15, SHADOW)
    b.rect(5, 5, 10, 5, SHADOW)
    return b


def fence_h(Block):
    """Glass barrier running east-west: lit rail on top, glass front, base, shadow."""
    b = floor(Block)
    b.rect(0, 0, 15, 0, OUT)
    b.rect(0, 1, 15, 2, S3)                                # rail top
    b.rect(0, 1, 15, 1, WHITE)
    b.rect(0, 3, 15, 3, S1)                                # lip
    b.rect(0, 4, 15, 10, BLUE)                             # glass
    for i in range(4):
        b.put(3 + i, 9 - i, WHITE)                         # glint
        b.put(9 + i, 9 - i, BLUE_D)
    b.rect(0, 11, 15, 12, S2)                              # base band
    b.rect(0, 13, 15, 13, OUT)
    shade(b, 0, 14, 15, 15)
    return b


# ------------------------------------------------------------------ ticket booth
# A small building against the back wall, 3 wide x 4 tall:
#   row 1 (over the lower wall)  flat roof, running back to the wall
#   row 2                        rest of the roof, lip, navy fascia (ticket pictograms on L and R).
#                                Also drawn in the TOP layer (LAYER_NORMAL) so it covers the top of
#                                the clerk standing in the window below
#   row 3                        facade: glass panels L/R, open service window M (clerk stands here)
#   row 4                        counter (MB_COUNTER), talked across from the row below
def booth_roof(part, rows):
    """Roof top surface for the given local rows; outer outline on the end tiles."""
    def draw(b):
        for y in rows:
            for x in range(16):
                b.put(x, y, SLT)
        if part == "L":
            for y in rows:
                b.put(0, y, OUT)
                b.put(1, y, WHITE)
        if part == "R":
            for y in rows:
                b.put(15, y, OUT)
                b.put(14, y, SMD)
    return draw


def booth_roof_back(Block, part):
    b = Block()
    booth_roof(part, range(0, 16))(b)
    b.rect(0, 0, 15, 0, SMD)                               # meets the wall: shadow line
    for y in (5, 11):                                      # roof panel seams
        b.rect(1 if part == "L" else 0, y, 14 if part == "R" else 15, y, SMD)
    return b


def booth_roof_front(Block, part):
    b = Block()
    booth_roof(part, range(0, 5))(b)
    b.rect(0, 5, 15, 5, WHITE)                             # front edge of the roof catches the light
    b.rect(0, 6, 15, 6, OUT)
    b.rect(0, 7, 15, 14, NAVY)                             # fascia
    b.rect(0, 15, 15, 15, OUT)
    if part == "L":
        b.rect(0, 0, 0, 15, OUT)
    if part == "R":
        b.rect(15, 0, 15, 15, OUT)
    if part in "LR":                                       # ticket pictogram
        b.rect(4, 8, 11, 13, WHITE)
        b.rect(4, 11, 11, 11, AMBER)                       # stripe
        for y in (8, 10, 12):
            b.put(9, y, NAVY)                              # perforation
        b.rect(5, 9, 7, 9, SLT)                            # print
    return b


def booth_facade(Block, part):
    """Front wall of the booth. L/R: steel frame with a glass panel; M: open service window."""
    b = Block()
    b.rect(0, 0, 15, 15, S2)
    b.rect(0, 0, 15, 0, S1)                                # under the fascia
    if part == "M":
        b.rect(0, 1, 15, 15, S1)                           # inside the booth
        b.rect(0, 1, 15, 2, OUT)
        b.rect(0, 1, 0, 15, S2)
        b.rect(15, 1, 15, 15, S2)
        return b
    x0, x1 = (3, 13) if part == "L" else (2, 12)
    b.rect(x0, 2, x1, 13, BLUE)                            # glass
    b.rect(x0, 2, x1, 2, OUT)
    b.rect(x0, 2, x0, 13, OUT)
    for i in range(4):
        b.put(x0 + 2 + i, 10 - i, WHITE)                   # glint
    b.rect(0, 14, 15, 15, S1)                              # plinth
    if part == "L":
        b.rect(0, 0, 0, 15, OUT)
    if part == "R":
        b.rect(15, 0, 15, 15, OUT)
    return b


def booth_counter(Block, part):
    """Counter facing the concourse: tall lit top, lip, 2-row front band, floor shadow."""
    b = floor(Block)
    b.rect(0, 0, 15, 0, OUT)
    b.rect(0, 1, 15, 8, S3)                                # top surface
    b.rect(0, 1, 15, 1, WHITE)
    b.rect(0, 9, 15, 9, S1)                                # lip
    b.rect(0, 10, 15, 11, S2)                              # front band
    b.rect(0, 12, 15, 12, OUT)
    shade(b, 0, 13, 15, 14)
    if part == "L":
        b.rect(0, 0, 0, 12, OUT)
        b.rect(1, 1, 1, 8, WHITE)
    if part == "R":
        b.rect(15, 0, 15, 12, OUT)
        b.rect(14, 10, 14, 11, S1)                         # right end one shade darker
    if part == "M":
        b.rect(4, 3, 11, 6, S1)                            # ticket tray
        b.rect(4, 3, 11, 3, OUT)
        b.rect(6, 4, 9, 5, WHITE)                          # ticket
        b.put(9, 5, YEL)
    return b


# ------------------------------------------------------------------ seat + mat
SEAT_ART = [                       # Battle Tent seat (gTileset_BattleTent 0x29F top layer)
    "................",
    "................",
    "................",
    "...aaaaaaaaaa...",
    ".aabbbbbbbbbbaa.",
    "abbbbbbbbbbbbbba",
    "abbbbbbbbbbbbbba",
    "abbbbbbccbbbbbba",
    "abbbbbbbbbbbbbba",
    "adbbbbbbbbbbbbda",
    "adddddddddddddda",
    "eeddddddddddddee",
    "fghhhhhhhhhhhhgf",
    "afaaaaaaaaaaaafa",
    "af............fa",
    "af............fa",
]
SEAT_COLOURS = {"a": OUT, "b": BLUE, "c": S3, "d": BLUE_D, "e": S3, "f": S2, "g": S1, "h": S3}


def seat_top(Block):
    b = Block()
    for y, row in enumerate(SEAT_ART):
        for x, ch in enumerate(row):
            if ch != ".":
                b.put(x, y, SEAT_COLOURS[ch])
    return b


def exit_mat(Block, part):
    b = floor(Block)
    x0, x1 = (1, 15) if part == "L" else (0, 14)
    b.rect(x0, 1, x1, 14, OUT)
    b.rect(x0 + (1 if part == "L" else 0), 2, x1 - (0 if part == "L" else 1), 13, S1)
    b.rect(7, 4, 8, 8, WHITE)
    b.rect(4, 8, 11, 8, WHITE)
    b.rect(5, 9, 10, 9, WHITE)
    b.rect(6, 10, 9, 10, WHITE)
    b.rect(7, 11, 8, 11, WHITE)
    return b


# ------------------------------------------------------------------ list
def concourse_defs(Block):
    """(label, palettes, bottom(), top() or None, behaviour, layer). Order = id from FIRST_ID."""
    F, X = (12,), (11,)
    wallp = (6, 11)
    wt = wall_tall()
    return [
        ("Concourse_Wall_Upper", wallp, lambda: wt.half(Block, 0), None, MB_NORMAL, LAYER_COVERED),
        ("Concourse_Wall_Lower", wallp, lambda: wt.half(Block, 1), None, MB_NORMAL, LAYER_COVERED),
        ("Concourse_Floor_A", F, lambda: floor(Block, "A"), None, MB_NORMAL, LAYER_NORMAL),
        ("Concourse_Floor_B", F, lambda: floor(Block, "B"), None, MB_NORMAL, LAYER_NORMAL),
        ("Concourse_Guide_V", F, lambda: guide(Block, True), None, MB_NORMAL, LAYER_NORMAL),
        ("Concourse_Guide_H", F, lambda: guide(Block, False), None, MB_NORMAL, LAYER_NORMAL),
        ("Concourse_Guide_Blister", F, lambda: blister(Block), None, MB_NORMAL, LAYER_NORMAL),
        ("Concourse_Seat", F, lambda: floor(Block, "A"), lambda: seat_top(Block), MB_NORMAL, LAYER_COVERED),
        ("FareGate_Cabinet", F, lambda: gate_cabinet(Block), None, MB_NORMAL, LAYER_COVERED),
        ("FareGate_Gate", F, lambda: gate_passage(Block), None, MB_NORMAL, LAYER_COVERED),
        ("FareGate_Fence_H", F, lambda: fence_h(Block), None, MB_NORMAL, LAYER_COVERED),
        ("Concourse_ExitMat_L", F, lambda: exit_mat(Block, "L"), None, MB_SOUTH_ARROW_WARP, LAYER_NORMAL),
        ("Concourse_ExitMat_R", F, lambda: exit_mat(Block, "R"), None, MB_SOUTH_ARROW_WARP, LAYER_NORMAL),
        ("Concourse_Arch_Top_L", X, lambda: arch_piece(Block, "L", 0), None, MB_NORMAL, LAYER_COVERED),
        ("Concourse_Arch_Top_R", X, lambda: arch_piece(Block, "R", 0), None, MB_NORMAL, LAYER_COVERED),
        ("Concourse_Arch_Exit_L", X, lambda: arch_piece(Block, "L", 1), None, MB_NORTH_ARROW_WARP, LAYER_COVERED),
        ("Concourse_Arch_Exit_R", X, lambda: arch_piece(Block, "R", 1), None, MB_NORTH_ARROW_WARP, LAYER_COVERED),
        ("Booth_Roof_L", X, lambda: booth_roof_back(Block, "L"), None, MB_NORMAL, LAYER_COVERED),
        ("Booth_Roof_M", X, lambda: booth_roof_back(Block, "M"), None, MB_NORMAL, LAYER_COVERED),
        ("Booth_Roof_R", X, lambda: booth_roof_back(Block, "R"), None, MB_NORMAL, LAYER_COVERED),
        ("Booth_Fascia_L", X, lambda: booth_roof_front(Block, "L"), lambda: booth_roof_front(Block, "L"), MB_NORMAL, LAYER_NORMAL),
        ("Booth_Fascia_M", X, lambda: booth_roof_front(Block, "M"), lambda: booth_roof_front(Block, "M"), MB_NORMAL, LAYER_NORMAL),
        ("Booth_Fascia_R", X, lambda: booth_roof_front(Block, "R"), lambda: booth_roof_front(Block, "R"), MB_NORMAL, LAYER_NORMAL),
        ("Booth_Facade_L", F, lambda: booth_facade(Block, "L"), None, MB_NORMAL, LAYER_COVERED),
        ("Booth_Facade_M", F, lambda: booth_facade(Block, "M"), None, MB_NORMAL, LAYER_COVERED),
        ("Booth_Facade_R", F, lambda: booth_facade(Block, "R"), None, MB_NORMAL, LAYER_COVERED),
        ("Booth_Counter_L", F, lambda: booth_counter(Block, "L"), None, MB_COUNTER, LAYER_COVERED),
        ("Booth_Counter_M", F, lambda: booth_counter(Block, "M"), None, MB_COUNTER, LAYER_COVERED),
        ("Booth_Counter_R", F, lambda: booth_counter(Block, "R"), None, MB_COUNTER, LAYER_COVERED),
        ("StationSign", X, lambda: sign_upper(Block), None, MB_NORMAL, LAYER_COVERED),
    ]
