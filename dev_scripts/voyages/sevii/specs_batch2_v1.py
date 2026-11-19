"""
Sailor's Voyages, batch 2 (Sevii Islands 1-3): design-review mockup specs, not real maps. See
voyage_compose.py for the spec format. Every cell is copied from a layout with the same primary +
secondary pair, or (pstamps / ("id", m) with m < 0x200) is a General-primary metatile, which is the same
art in every General pair. No tileset is edited.

Post-game: the Sailor's small boat (OBJ_EVENT_GFX_MR_BRINEYS_BOAT) brings the player from Wavebreak Town to
One Island's harbour and waits there. Islands inside a cluster are joined by Surf sea routes (One <-> Two
<-> Three); a harbour ferry hops between clusters (1-3 / 4-5 / 6-7). Generic NPCs only.

Geography follows the FRLG Sevii 1-2-3 region map (graphics/pokenav/region_map/map_sevii_123.*, sections in
src/data/region_map/region_map_layout_sevii123.h): Kindle Road runs north from One Island (cell 1,8) up
column 2 to Mt. Ember; Two Island (9,9) with Cape Brink (9,7-8) north of it; Bond Bridge (14-17,12) runs west
from Three Island (18,12). Reference renders of the deleted FRLG layouts: ref/frlg/ (frlg_ref.py).

Tileset pairs (one secondary per cluster, so connected maps share edges):
  One Island, Kindle Road .......... General + Rustboro  (Route 104 coast, Briney's pier, Southern Island dock)
  Mt. Ember exterior + summit ...... General + Lavaridge (Jagged Pass terraces, Mt. Chimney crater)
  Two Island, Cape Brink,
  Sevii Sea Routes A + B ........... General + Dewford   (Dewford houses / hall / pier, Routes 105-107 sea)
  Three Island, Bond Bridge,
  Berry Forest ..................... General + Fortree  (Route 119 / 120 log bridges, forest)
Where two pairs meet (Kindle Road / Mt. Ember, Sea Route B / Bond Bridge) the cells along the shared edge
are General-primary only (sand, grass, sea), so the seam is identical on both sides.
"""
import voyage_compose as vc

G = "gTileset_General"
RB = (G, "gTileset_Rustboro")
LAV = (G, "gTileset_Lavaridge")
DEW = (G, "gTileset_Dewford")
FOR = (G, "gTileset_Fortree")

R104 = "LAYOUT_ROUTE104@git"
SI_EXT = "LAYOUT_SOUTHERN_ISLAND_EXTERIOR"
FARAWAY = "LAYOUT_FARAWAY_ISLAND_ENTRANCE"
LAVA_TOWN = "LAYOUT_LAVARIDGE_TOWN"        # Orchid's (new Centre / Mart art, all General primary)
JAGGED = "LAYOUT_JAGGED_PASS@git"
CHIMNEY = "LAYOUT_MT_CHIMNEY@git"
DEW_TOWN = "LAYOUT_DEWFORD_TOWN"           # Orchid's (new Centre); houses / hall / pier are vanilla Dewford
DEW_GIT = "LAYOUT_DEWFORD_TOWN@git"
R119 = "LAYOUT_ROUTE119@git"
R120 = "LAYOUT_ROUTE120@git"
FORTREE = "LAYOUT_FORTREE_CITY@git"


def I(mid, *ce):
    return ("id", mid) + ce


def mask_ok(rows, w, h):
    assert len(rows) == h, (len(rows), h)
    for i, r in enumerate(rows):
        assert len(r) == w, (i, len(r), r)
    return rows


# ------------------------------------------------------------------ shared vocabularies (General primary)
SEA = I(0x170, 0, 1)
SAND, GRASS, TALL, FLOWER, BOULDER, SIGN = 0x124, 0x001, 0x00D, 0x004, 0x0E2, 0x003
RIM = [0x002, 0x073, 0x075, 0x07B, 0x07C, 0x07D, 0x089, 0x074, 0x07A, 0x0A9, 0x079]
SEA_EDGE = [0x170, 0x180, 0x181, 0x189, 0x190, 0x192, 0x198, 0x19A, 0x15A, 0x15B, 0x171, 0x172, 0x174]
RIM_TRAIN = [SI_EXT, FARAWAY]
SHORE = [0x170, 0x11B, 0x11C, 0x11D, 0x123, 0x125, 0x12B, 0x12C, 0x12D, 0x13D, 0x13E, 0x145, 0x146, 0x124]
SHORE_TRAIN = [R104, DEW_GIT, "LAYOUT_ROUTE105", "LAYOUT_ROUTE107"]
ROCK_VOCAB = sorted(vc.ROCK_IDS)
ROCK_TRAIN = [SI_EXT, FARAWAY, "LAYOUT_ROUTE120"]
DIRT = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122, "BL": 0x128, "B": 0x129,
        "BR": 0x12A}
LEDGE = (0x0D5, 0x087, 0x0D6)

# 2x2 sea rocks (Route 104), primary: small rock with foam, big brown rock
SEA_ROCK = (R104, 7, 48, 2, 2)
SEA_ROCK_BIG = (R104, 5, 52, 2, 2)

# Orchid Centre / Mart / red-roof house: General primary, copied from Orchid's Lavaridge Town
CENTRE = (LAVA_TOWN, 8, 3, 5, 5)        # door at +2,+4
MART = (LAVA_TOWN, 14, 2, 4, 5)         # doors at +1,+4 and +2,+4
HOUSE = (LAVA_TOWN, 11, 12, 4, 4)       # door at +1,+3


def at(chunk, dx, dy):
    """(LAYOUT, sx, sy, w, h) + destination -> a stamp tuple."""
    return chunk + (dx, dy)


def path9(mask, ch, kit=DIRT):
    """9-slice dirt road for the `ch` cells (keep roads 2+ wide): -> [(x, y, ref)] for spec['cells']."""
    h, w = len(mask), len(mask[0])
    p = lambda x, y: 0 <= x < w and 0 <= y < h and mask[y][x] == ch   # noqa: E731
    pe = lambda x, y: (not (0 <= x < w and 0 <= y < h)) or mask[y][x] == ch   # off-map counts as road
    out = []
    for y in range(h):
        for x in range(w):
            if not p(x, y):
                continue
            n, s, wv, e = pe(x, y - 1), pe(x, y + 1), pe(x - 1, y), pe(x + 1, y)
            k = ("T" if not n else "B" if not s else "") + ("L" if not wv else "R" if not e else "")
            out.append((x, y, I(kit[k or "C"])))
    return out


def R(*segs):
    """Mask row from run-length segments: R("M4", "s10", "~14") -> "MMMMssssssssss~~~~~~~~~~~~~~"."""
    out = ""
    for sg in segs:
        out += sg[0] * int(sg[1:]) if sg[1:].isdigit() else sg      # "pp" / "s" = literal
    return out


def paint(w, h, base, rects):
    """Mask of w x h filled with `base`, then rects [(x, y, rw, rh, ch)] painted in order."""
    g = [[base] * w for _ in range(h)]
    for x, y, rw, rh, ch in rects:
        for j in range(rh):
            for i in range(rw):
                if 0 <= x + i < w and 0 <= y + j < h:
                    g[y + j][x + i] = ch
    return ["".join(r) for r in g]


def ledges(x0, x1, y):
    """One-way south ledge from x0 to x1 (inclusive) on row y."""
    return [(x0, y, I(LEDGE[0]))] + [(x, y, I(LEDGE[1])) for x in range(x0 + 1, x1)] + [(x1, y, I(LEDGE[2]))]


def coast_edges(rock=True, shore=True, rim=True):
    """Edge autotilers for masks made with vc.ring_multi(mask, [('.fgT', 'R', 'W'), ('s', 'S', 'w')]):
    rock rim into the sea for grass land, beach shore for sand, rock massif for 'M'."""
    out = []
    if rim:
        out.append(dict(chars="RW", water_chars="~Ww", vocab=RIM + SEA_EDGE, layouts=RIM_TRAIN))
    if shore:
        out.append(dict(kind="shore", chars="Sw", water_chars="~Ww", vocab=SHORE, layouts=SHORE_TRAIN))
    if rock:
        out.append(dict(kind="rock", chars="M", water_chars="M", vocab=ROCK_VOCAB, layouts=ROCK_TRAIN))
    return out


COAST_LEGEND = {"~": SEA, ".": I(GRASS), "f": I(FLOWER), "g": I(TALL), "s": I(SAND), "S": I(SAND),
                "b": I(BOULDER), "p": I(GRASS), "T": I(GRASS)}

ALL = {}

# =================================================================================================== ONE
# One Island (FRLG 24x20, ref/frlg/one_island.png). Town on a grass plateau ringed by rock: Pokemon Net
# Center (a second Centre exterior, as asked) at the top like FRLG's big building, the Centre, Briney-style
# cottage + red-roof house, a beach on the east that runs into Sea Route A, and the harbour on the south
# rim: Southern Island's concrete ferry dock (the S.S. Tidal berth = Seagallop stand-in) + Route 104's
# wooden pier where the Sailor's boat waits.
#                     x: 0         1         2         3
#                        01234567890123456789012345678901
ONE_MASK = mask_ok([
    "MMMMMMMMTTTTTT..pp..TTTTTTMMMMMM",   # 0  north edge -> Kindle Road (x16-17)
    "MMMMMMMMTTTTTT..pp..TTTTTTMMMMMM",   # 1
    "MMMMMMTTTT......pp......TTTTMMMM",   # 2
    "MMMMMMTTTT......pp......TTTTMMMM",   # 3
    "MMMMMMTT........pp........TTMMMM",   # 4
    "MMMMMMTT........pp........TTMMMM",   # 5
    "MMMMMMTT........pp........TTMMMM",   # 6
    "MMMMMMTT........pp.........TTMMM",   # 7
    "MMMMMM....pppppppppppppppp.TTMMM",   # 8
    "MMMMMM....pppppppppppppppp..ss~~",   # 9
    "MMMMTT.........pp..........sss~~",   # 10
    "MMMMTT.........pp..........sss~~",   # 11
    "MMMMTT.........pp..........sss~~",   # 12
    "MMMMTT.........pp.........ssss~~",   # 13
    "MMMM...........pp........ssss~~~",   # 14
    "MMMM.....pppppppppppppp..ssss~~~",   # 15
    "MMMM.f...pppppppppppppp..sss~~~~",   # 16
    "MMMMff.........pp.......ssss~~~~",   # 17
    "~MMM..f........pp......sss~~~~~~",   # 18
    "~~~....................ss~~~~~~~",   # 19  south rim (dock gangway stamped at x16-17)
    "~~~~~.......~~~~~~~~~~~~~~~~~~~~",   # 20
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 21
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 22
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 23
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 24
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 25
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 26
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 27
], 32, 28)

ONE_ISLAND = dict(
    name="One Island", size=(32, 28), tileset=RB,
    ground=SEA,
    mask=vc.ring_multi(ONE_MASK, [(".fgTpb", "R", "W"), ("s", "S", "w")]),
    mask_legend=COAST_LEGEND,
    edges_list=coast_edges(),
    big_trees="T",
    stamps=[
        (SI_EXT, 9, 18, 11, 8, 10, 19),     # Southern Island ferry dock: gangway stairs at (16-17,19)
        (R104, 15, 47, 5, 4, 9, 11),        # Briney-style cottage (Route 104), door (11,14)
    ],
    pstamps=[
        at(CENTRE, 18, 3),                  # Pokemon Net Center (second Centre exterior), door (20,7)
        at(CENTRE, 18, 10),                 # Pokemon Centre, door (20,14)
        at(HOUSE, 9, 3),                    # red-roof house, door (10,6)
    ],
    cells=path9(ONE_MASK, "p") + [(14, 7, I(SIGN)), (14, 16, I(SIGN))],
    marks=[
        (20, 7, "Net Ctr", "warp"), (20, 14, "Centre", "warp"), (10, 6, "house", "warp"),
        (11, 14, "house", "warp"), (14, 7, "", "sign"), (14, 16, "", "sign"),
        (16, 0, "^ Kindle Road", "conn"),
        (27, 22, "Sea Route A >", "conn"),
        (1, 26, "v Treasure Beach?", "conn"),
        (14, 26, "ferry", "ferry", "ss_tidal"), (16, 21, "berth", "warp"),
        (12, 23, "Sailor", "sailor", "sailor_left"), (9, 23, "boat", "boat", "boat_right"),
        (6, 12, "", "npc", "old_man"), (22, 16, "", "npc", "woman"), (28, 12, "", "npc", "boy"),
    ],
)
ALL["one_island"] = ONE_ISLAND


# ============================================================================================ KINDLE ROAD
# FRLG Kindle Road (24x140, ref/frlg/one_island_kindle_road.png): a long coastal route north from One Island
# to Mt. Ember -- rock wall on the west, beach strips and sea on the east, one stretch that needs Surf, a
# grassy terrace with tall grass, and the Ember Spa (a red-roof house + sign) at the north end on the sandy
# foot of Mt. Ember. 28x96. Its bottom two rows repeat One Island's top rows (x4-31) so the edge matches;
# its top rows are General sand / grass only, matching Mt. Ember's south edge (different secondary).
KINDLE_MASK = mask_ok(
    [R("M3", "T4", "s14", "T4", "M3")] * 2                                   # 0-1   -> Mt. Ember
    + [R("M3", ".7", "s15", "M3")] * 2                                        # 2-3
    + [R("M3", ".7", "s13", "~5")]                                            # 4
    + [R("M3", ".7", "s12", "~6")] * 3                                        # 5-7   Ember Spa x4-7 y3-6
    + [R("M3", ".1", "g5", ".1", "s11", "~7")] * 2                            # 8-9
    + [R("M4", "g4", ".1", "s11", "~8")] * 2                                  # 10-11
    + [R("M5", "s14", "~9")]                                                  # 12
    + [R("M6", "s13", "~9")]                                                  # 13
    + [R("M7", "s11", "~10")] * 4                                             # 14-17
    + [R("M7", "s2", "b", "s8", "~10")]                                       # 18
    + [R("M7", "s12", "~9")] * 4                                              # 19-22
    + [R("M8", "s10", "~10")] * 3                                             # 23-25
    + [R("M8", "s5", "b", "s3", "~11")]                                       # 26
    + [R("M8", "s7", "~13")] * 2                                              # 27-28
    + [R("M7", "s6", "~15")]                                                  # 29
    + [R("M7", "s3", "~18")]                                                  # 30
    + [R("M7", "~21")] * 6                                                    # 31-36  Surf
    + [R("M6", "~22")] * 8                                                    # 37-44  Surf
    + [R("M6", "s4", "~18")]                                                  # 45
    + [R("M6", "s8", "~14")]                                                  # 46
    + [R("M6", ".2", "s9", "~11")]                                            # 47
    + [R("M5", "T2", ".2", "g6", ".2", "s5", "~6")] * 8                       # 48-55
    + [R("M5", "T2", ".11", "s4", "~6")]                                      # 56  ledge x7-15
    + [R("M5", "T2", ".1", "g4", ".1", "g3", ".2", "s4", "~6")] * 6           # 57-62
    + [R("M5", "T2", ".11", "s4", "~6")]                                      # 63  ledge x9-17
    + [R("M5", "T2", ".11", "s4", "~6")] * 4                                  # 64-67
    + [R("M6", ".12", "s4", "~6")] * 2                                        # 68-69
    + [R("M7", ".3", "s11", "~7")]                                            # 70
    + [R("M8", "s10", "~10")] * 4                                             # 71-74
    + [R("M8", "s4", "b", "s5", "~10")]                                       # 75
    + [R("M8", "s10", "~10")] * 6                                             # 76-81
    + [R("M7", "s11", "~10")] * 3                                             # 82-84
    + [R("M6", ".2", "s10", "~10")] * 3                                       # 85-87
    + [R("M4", "T6", ".2", "s7", "~9")] * 2                                   # 88-89
    + [R("M4", "T6", ".2", "s6", "T4", "M6")] * 2                             # 90-91
    + [R("M4", "T6", ".2", "pp", ".2", "T6", "M6")] * 2                       # 92-93
    + [R("M4", "T6", "..", "pp", "..", "T6", "M6")] * 2,                      # 94-95  = One Island x4-31
    28, 96)

KINDLE_ROCKS = [(20, 16), (24, 20), (21, 26), (14, 33), (22, 35), (10, 39), (18, 41), (25, 52), (24, 60),
                (21, 76), (25, 84)]

KINDLE_ROAD = dict(
    name="Kindle Road", size=(28, 96), tileset=RB,
    ground=SEA,
    mask=vc.ring_multi(KINDLE_MASK, [(".fgTpb", "R", "W"), ("s", "S", "w")]),
    mask_legend=COAST_LEGEND,
    edges_list=coast_edges(),
    big_trees="T",
    pstamps=[at(HOUSE, 4, 3)] + [at(SEA_ROCK if i % 3 else SEA_ROCK_BIG, x, y)
                                for i, (x, y) in enumerate(KINDLE_ROCKS)],
    cells=path9(KINDLE_MASK, "p") + ledges(7, 15, 56) + ledges(9, 17, 63) + [(8, 6, I(SIGN))],
    marks=[
        (5, 6, "Ember Spa", "warp"), (8, 6, "", "sign"),
        (8, 0, "^ Mt. Ember", "conn"), (10, 94, "v One Island", "conn"),
        (12, 36, "Surf", "note"),
        (12, 20, "", "npc", "fisherman"), (14, 10, "", "npc", "old_woman"), (10, 52, "", "npc", "camper"),
        (13, 60, "", "npc", "picnicker"), (19, 40, "", "npc", "swimmer"), (12, 79, "", "npc", "hiker"),
    ],
)
ALL["kindle_road"] = KINDLE_ROAD


# ============================================================================================== MT. EMBER
# Mt. Ember exterior (FRLG 57x54, ref/frlg/mt_ember_exterior.png): Jagged Pass rows 0-39 as the volcano
# slope (ash-dusted terraces, ash trees, stairs, a cave mouth = Ruby Path), then a forest-flanked foot that
# opens onto Kindle Road's sand (rows 46-47 = Kindle Road's top row with one rock column each side, so the
# General-only edge matches across the Lavaridge / Rustboro seam). The stairs at the top (13-14,5) warp to
# the summit, exactly as Jagged Pass's stairs warp to Mt. Chimney (no map connection).
EMBER_BASE_MASK = mask_ok(
    [R("x30")] * 40
    + [R("T12", ".6", "T12")] * 2                                             # 40-41
    + [R("T8", ".2", "s10", ".2", "T8")] * 2                                  # 42-43
    + [R("M2", "T6", "s14", "T6", "M2")] * 2                                  # 44-45
    + [R("M4", "T4", "s14", "T4", "M4")] * 2,                                 # 46-47  = Kindle Road row 0
    30, 48)

MT_EMBER = dict(
    name="Mt. Ember", size=(30, 48), tileset=LAV,
    ground=I(SAND),
    mask=EMBER_BASE_MASK,
    mask_legend={"x": I(SAND), ".": I(GRASS), "s": I(SAND), "T": I(GRASS)},
    edges_list=[dict(kind="rock", chars="M", water_chars="M", vocab=ROCK_VOCAB, layouts=ROCK_TRAIN)],
    big_trees="T",
    stamps=[(JAGGED, 0, 0, 30, 40, 0, 0)],
    marks=[
        (13, 5, "to summit", "warp"), (14, 5, "", "warp"),
        (16, 18, "Ruby Path (closed)", "warp"),
        (9, 46, "v Kindle Road", "conn"),
        (20, 30, "", "npc", "hiker"), (8, 20, "", "npc", "expert"),
    ],
)
ALL["mt_ember"] = MT_EMBER

# Mt. Ember summit (FRLG 19x22, ref/frlg/mt_ember_summit.png): Mt. Chimney's crater top (x8-31, y0-23) -- the
# lava crater, the ash rim terraces and the stairs at (17,22) that come up from the exterior. The meteorite
# machine is cleared. No legendary in scope: the spot in front of the crater is marked and left empty.
EMBER_SUMMIT = dict(
    name="Mt. Ember summit", size=(24, 24), tileset=LAV,
    ground=I(SAND),
    stamps=[(CHIMNEY, 8, 0, 24, 24, 0, 0),
            (CHIMNEY, 12, 6, 1, 1, 6, 6), (CHIMNEY, 13, 4, 1, 1, 6, 5)],   # clear the meteorite machine
    marks=[
        (12, 12, "legendary spot (empty)", "spot"),
        (17, 22, "to Mt. Ember", "warp"),
    ],
)
ALL["mt_ember_summit"] = EMBER_SUMMIT


# ============================================================================================= TWO ISLAND
# FRLG Two Island (48x20, ref/frlg/two_island.png): harbour, Centre, Joyful Game Corner, Mart, a house, and
# the way north to Cape Brink. Built like vanilla Dewford (sand town, Dewford's 1-wide trees, blue-roof
# houses): the Game Corner is Dewford Town Hall (5x4, the biggest Dewford house) with a sign; the harbour is
# Dewford's wooden pier on the east beach, where Sea Route B leaves; Sea Route A arrives on the west beach.
DEW_TREES = (0x243, 0x239, 0x23A)        # body, crown over sand, trunk on sand
HALL = (DEW_TOWN, 1, 0, 5, 4)            # Dewford Town Hall, door +2,+3
DHOUSE4B = (DEW_TOWN, 7, 5, 4, 4)        # door +1,+3
DHOUSE4 = (DEW_TOWN, 16, 11, 4, 4)       # door +1,+3
DPIER = (DEW_TOWN, 11, 9, 4, 2)          # land end on the west

TWO_MASK = mask_ok(
    [R("~2", "T14", "s6", "T10", "M8")] * 2                                   # 0-1  -> Cape Brink x16-21
    + [R("~2", "T4", "s26", "T4", "M4")]                                      # 2
    + [R("~2", "T2", "s13", ".13", "s4", "T2", "M4")] * 3                     # 3-5   lawn x17-29
    + [R("~2", "T2", "s13", ".13", "s5", "T1", "~4")] * 2                     # 6-7
    + [R("~3", "s14", ".13", "s5", "~5")]                                     # 8
    + [R("~3", "s32", "~5")] * 8                                              # 9-16
    + [R("~3", "s4", "b", "s19", "b", "s7", "~5")]                                  # 17
    + [R("~3", "s32", "~5")] * 2                                              # 18-19
    + [R("~3", "s3", "T4", "s20", "T4", "s1", "~5")] * 2                      # 20-21
    + [R("~4", "T8", "s4", "T14", "~10")] * 2,                                # 22-23
    40, 24)

TWO_ISLAND = dict(
    name="Two Island", size=(40, 24), tileset=DEW,
    ground=SEA,
    mask=vc.ring_multi(TWO_MASK, [("sb", "S", "w")]),
    mask_legend={"~": SEA, "s": I(SAND), "S": I(SAND), "b": I(BOULDER), "T": I(0x243), ".": I(GRASS)},
    edges_list=coast_edges(rim=False),
    cells=vc.small_trees(TWO_MASK, "T", *DEW_TREES) + [(15, 5, I(SIGN)), (16, 19, I(SIGN)), (23, 7, I(SIGN))],
    stamps=[
        at(HALL, 9, 2),                    # Joyful Game Corner, door (11,5)
        at(DHOUSE4B, 9, 11),               # house, door (10,14)
        at(DHOUSE4, 27, 12),               # house, door (28,15)
        at(DPIER, 35, 16),                 # harbour pier, east beach
    ],
    pstamps=[
        at(CENTRE, 18, 3),                 # door (20,7)
        at(MART, 25, 3),                   # doors (26,7) (27,7)
    ],
    post=[(38, 17, SEA), (38, 16, SEA)],
    marks=[
        (11, 5, "Game Corner", "warp"), (15, 5, "", "sign"), (20, 7, "Centre", "warp"),
        (26, 7, "Mart", "warp"), (27, 7, "", "warp"), (10, 14, "house", "warp"), (28, 15, "house", "warp"),
        (16, 19, "", "sign"),
        (17, 0, "^ Cape Brink", "conn"), (0, 12, "< Sea Route A", "conn"), (33, 21, "Sea Route B >", "conn"),
        (37, 16, "pier", "note"),
        (13, 8, "", "npc", "man"), (22, 12, "", "npc", "lass"), (34, 17, "", "npc", "fisherman"),
        (5, 15, "", "npc", "boy"),
    ],
)
ALL["two_island"] = TWO_ISLAND


# ============================================================================================= CAPE BRINK
# FRLG Cape Brink (24x40, ref/frlg/two_island_cape_brink.png): the cape north of Two Island, a house at the
# tip and a pond below it. 24x32, General + Dewford like Two Island. Pond = the General pond set (Route
# 120 / 104 banks, 0x002 lip), learnt by the edge autotiler; the cape's coast = the rock rim into the sea.
# Bottom rows = Two Island's top row x8-31 (trees / sand x8-13 / trees), so the connection offset is +8.
POND_VOCAB = [0x0A1, 0x0B0, 0x0B1, 0x0B2, 0x0B3, 0x0B8, 0x0B9, 0x0BA, 0x0BB, 0x0C0, 0x0C2, 0x0C3, 0x0C4]
POND_TRAIN = [R120, R104, R119]
CAPE_MASK = mask_ok(
    [R("~24")] * 4                                                            # 0-3
    + [R("~8", ".8", "~8")]                                                   # 4
    + [R("~6", ".12", "~6")]                                                  # 5
    + [R("~4", ".16", "~4")] * 4                                              # 6-9   house x10-13 y6-9
    + [R("~3", ".18", "~3")] * 2                                              # 10-11
    + [R("~3", ".5", "q8", ".5", "~3")] * 2                                   # 12-13 pond
    + [R("~3", ".3", "q12", ".3", "~3")] * 4                                  # 14-17
    + [R("~3", ".5", "q8", ".5", "~3")] * 2                                   # 18-19
    + [R("~3", "G2", ".14", "G2", "~3")] * 2                                  # 20-21
    + [R("~2", "G4", ".2", "g6", ".2", "G4", "~4")] * 2                       # 22-23
    + [R("~2", "G4", ".2", "g6", ".2", "G4", "~4")] * 2                       # 24-25
    + [R("~1", "T7", ".1", "s5", "T8", "~2")] * 2                             # 26-27
    + [R("T8", "s6", "T10")] * 4,                                             # 28-31 = Two Island row 0
    24, 32)
_cape = vc.ring_multi(CAPE_MASK, [(".gGTs", "R", "W")])
_cape = vc.ring_multi(_cape, [(".gG", "L", "Q")], sea_chars="q")

CAPE_BRINK = dict(
    name="Cape Brink", size=(24, 32), tileset=DEW,
    ground=SEA,
    mask=_cape,
    mask_legend={"~": SEA, ".": I(GRASS), "g": I(TALL), "s": I(SAND), "T": I(0x243), "G": I(GRASS),
                 "q": I(0x0A1, 0, 1), "L": I(GRASS)},
    edges_list=[dict(chars="RW", water_chars="~W", vocab=RIM + SEA_EDGE, layouts=RIM_TRAIN),
                dict(chars="LQ", water_chars="qQ", vocab=POND_VOCAB + [0x001, 0x002], layouts=POND_TRAIN)],
    big_trees="G",
    cells=vc.small_trees(CAPE_MASK, "T", *DEW_TREES),
    stamps=[at(DHOUSE4, 10, 6)],            # door (11,9)
    marks=[
        (11, 9, "house", "warp"),
        (9, 30, "v Two Island", "conn"),
        (8, 11, "", "npc", "old_woman"), (14, 21, "", "npc", "picnicker"),
    ],
)
ALL["cape_brink"] = CAPE_BRINK


# =========================================================================================== THREE ISLAND
# FRLG Three Island (24x40, ref/frlg/three_island.png): a forest-ringed town (Centre, Mart, houses). In
# General + Fortree it becomes a small Fortree-style forest town: 1-wide Fortree forest around it, two
# Fortree treehouses up in the trees (ladders down), red-roof houses (General primary, as on Route 119),
# Centre + Mart, dirt roads. Bond Bridge comes in on the west road (rows 13-14); the south road would lead
# to Three Isle Port (out of scope).
FOREST = [0x0C6, 0x0C7, 0x016, 0x017, 0x00E, 0x00F]
TREEHOUSE = (FORTREE, 8, 0, 5, 7)         # door +2,+3 ; ladder down to +2,+6
THREE_MASK = mask_ok(
    [R("F4", "h5", "F13", "h5", "F5")] * 7                                  # 0-6  treehouses
    + [R("F2", ".26", "F4")] * 6                                              # 7-12
    + [R("p28", "F4")] * 2                                                    # 13-14 -> Bond Bridge (west)
    + [R("F2", ".12", "pp", ".12", "F4")] * 7                                 # 15-21
    + [R("F2", ".1", "F4", ".7", "pp", ".8", "F4", "F4")] * 4                 # 22-25
    + [R("F2", ".12", "pp", ".12", "F4")] * 3                                 # 26-28
    + [R("F14", "pp", "F16")] * 3,                                            # 29-31 -> Three Isle Port
    32, 32)

THREE_ISLAND = dict(
    name="Three Island", size=(32, 32), tileset=FOR,
    ground=I(GRASS),
    mask=THREE_MASK,
    mask_legend={".": I(GRASS), "p": I(GRASS), "h": I(0x0C7), "f": I(FLOWER)},
    mask_auto={"F": FOREST},
    cells=path9(THREE_MASK, "p") + [(12, 12, I(SIGN)), (16, 16, I(SIGN))],
    stamps=[at(TREEHOUSE, 4, 0), at(TREEHOUSE, 22, 0)],
    pstamps=[
        at(CENTRE, 13, 8),                 # door (15,12)
        at(MART, 20, 8),                   # doors (21,12) (22,12)
        at(HOUSE, 4, 16),                  # door (5,19)
        at(HOUSE, 20, 17),                 # door (21,20)
    ],
    marks=[
        (6, 3, "treehouse", "warp"), (24, 3, "treehouse", "warp"),
        (15, 12, "Centre", "warp"), (21, 12, "Mart", "warp"), (22, 12, "", "warp"),
        (5, 19, "house", "warp"), (21, 20, "house", "warp"), (12, 12, "", "sign"), (16, 16, "", "sign"),
        (0, 12, "< Bond Bridge", "conn"), (14, 30, "v Three Isle Port?", "conn"),
        (9, 10, "", "npc", "woman"), (18, 15, "", "npc", "old_man"), (10, 25, "", "npc", "boy"),
    ],
)
ALL["three_island"] = THREE_ISLAND


# ============================================================================================ BOND BRIDGE
# FRLG Bond Bridge (96x20, ref/frlg/three_island_bond_bridge.png): a long wooden bridge over the sea west of
# Three Island. 64x20, General + Fortree: Route 119's log bridge (2 rows; 210/218 are the over-water
# pieces, 211/219 and 215/21D the land ends). West landing: a sandy islet with the Berry Forest entrance (a
# gap in the forest, warp) and Sea Route B arriving on the west edge (Surf). East end: the road into Three
# Island (connection offset -4, so rows 9-10 meet Three Island's road at rows 13-14).
BOND_MASK = mask_ok(
    [R("~2", "s1", "F12", "s1", "~32", "s2", "F14")] * 4                       # 0-3
    + [R("~2", "s1", "F5", "e2", "F5", "s1", "~32", "s2", "F14")] * 3          # 4-6  Berry Forest gap x8-9
    + [R("~2", "s2", ".11", "s1", "~32", "s2", "F14")] * 2                     # 7-8
    + [R("~2", "s2", "p12", "~32", "s2", "p14")] * 2                           # 9-10 bridge x15-48
    + [R("~2", "s2", ".11", "s1", "~32", "s2", "F14")] * 2                     # 11-12
    + [R("~3", "s12", "~33", "s2", "F14")] * 2                                 # 13-14
    + [R("~5", "s8", "~35", "s2", "F14")] * 2                                  # 15-16
    + [R("~48", "s2", "F14")] * 3,                                             # 17-19
    64, 20)


def _bridge(x0, x1, y):
    out = [(x0, y, (R119, 7, 84)), (x0, y + 1, (R119, 7, 85)), (x1, y, (R119, 32, 84)), (x1, y + 1, (R119, 32, 85))]
    for x in range(x0 + 1, x1):
        out += [(x, y, (R119, 22, 84)), (x, y + 1, (R119, 22, 85))]
    return out


BOND_ROCKS = [(20, 2), (27, 5), (35, 1), (43, 4), (23, 15), (31, 13), (39, 16), (45, 13)]
BOND_BRIDGE = dict(
    name="Bond Bridge", size=(64, 20), tileset=FOR,
    ground=SEA,
    mask=vc.ring_multi(BOND_MASK, [("s", "S", "w"), (".pe", "R", "W")]),
    mask_legend={"~": SEA, ".": I(GRASS), "p": I(GRASS), "e": I(GRASS), "s": I(SAND), "S": I(SAND),
                 "F": I(0x0C7)},
    mask_auto={"F": FOREST},
    edges_list=coast_edges(rock=False),
    pstamps=[at(SEA_ROCK if i % 2 else SEA_ROCK_BIG, x, y) for i, (x, y) in enumerate(BOND_ROCKS)],
    cells=path9(BOND_MASK, "p") + _bridge(15, 48, 9) + [(13, 7, I(SIGN))],
    marks=[
        (8, 4, "Berry Forest", "warp"), (9, 4, "", "warp"), (13, 7, "", "sign"),
        (0, 9, "< Sea Route B (Surf)", "conn"), (58, 8, "Three Island >", "conn"),
        (24, 9, "", "npc", "swimmer"), (40, 10, "", "npc", "fisherman"), (6, 12, "", "npc", "lass"),
    ],
)
ALL["bond_bridge"] = BOND_BRIDGE


# =========================================================================================== BERRY FOREST
# FRLG Berry Forest (57x47, ref/frlg/three_island_berry_forest.png): a forest maze off Bond Bridge. 36x36,
# General + Fortree: 2x2 Petalburg Woods trees (General primary) on a 2x2 block grid, tall-grass pockets,
# flower patches, a General pond (Route 120 banks). Entrance / exit at the bottom (warp back to Bond
# Bridge's forest gap). Berry trees would be objects (OBJ_EVENT_GFX_BERRY_TREE on soft soil) -- marked only.
BERRY_BLOCKS = [
    "TTTTTTTTTTTTTTTTTT",   # 0
    "T....gggT..f....TT",   # 1
    "T.TTT.ggT.TTTT..TT",   # 2
    "T.T...TTT.T..g...T",   # 3
    "T.T.ggg...T.TTT..T",   # 4
    "T.TTTTTTT.T.T....T",   # 5
    "T...f...T...T.TTTT",   # 6
    "TTTTT.T.TTTTT.T..T",   # 7
    "Tgg...T.....T....T",   # 8
    "Tgg.TTTTTT.TTTTT.T",   # 9
    "T...T....T...f.T.T",   # 10
    "T.TTT.qq.T.TTT.T.T",   # 11
    "T.....qq.T...T...T",   # 12
    "TTTT.TTTTTTT.TTT.T",   # 13
    "T.gg.....f....gg.T",   # 14
    "T.TTTTTT.TTTT.TT.T",   # 15
    "T......T.........T",   # 16
    "TTTTTTTT..TTTTTTTT",   # 17  exit x16-19
]
BERRY_MASK = mask_ok([("".join(c * 2 for c in row)) for row in BERRY_BLOCKS for _ in (0, 1)], 36, 36)
_berry = vc.ring_multi(BERRY_MASK, [(".gfT", "L", "Q")], sea_chars="q")

BERRY_FOREST = dict(
    name="Berry Forest", size=(36, 36), tileset=FOR,
    ground=I(GRASS),
    mask=_berry,
    mask_legend={".": I(GRASS), "g": I(TALL), "f": I(FLOWER), "T": I(GRASS), "q": I(0x0A1, 0, 1),
                 "L": I(GRASS)},
    edges_list=[dict(chars="LQ", water_chars="qQ", vocab=POND_VOCAB + [0x001, 0x002], layouts=POND_TRAIN)],
    big_trees="T",
    marks=[
        (17, 35, "exit", "warp"), (18, 35, "", "warp"),
        (3, 3, "berry", "item", "item"), (22, 2, "berry", "item", "item"), (33, 16, "", "item", "item"),
        (10, 24, "", "item", "item"),
        (24, 20, "berry tree?", "note"), (6, 32, "", "npc", "camper"), (28, 28, "", "npc", "picnicker"),
    ],
)
ALL["berry_forest"] = BERRY_FOREST


# ============================================================================================= SEA ROUTES
# Surf routes between the islands of the cluster (no FRLG equivalent: FRLG only had the Seagallop). Sized
# from the region map (~24 tiles per section cell, as FRLG's Sevii maps) but kept short: open sea with sea
# rocks, sandbars and a grassy islet, like Routes 105-107 (General + Dewford; nearly all General primary,
# so either neighbour's edge matches). Generic swimmers only.
#
# Sea Route A: One Island (1,8) -> Two Island (9,9). West edge = One Island's east edge (offset 0: rows 0-8
# rock, the rest sea); east edge = Two Island's west edge (offset +4, all sea).
SEA_A_MASK = paint(80, 28, "~", [
    (0, 0, 4, 9, "M"), (4, 0, 2, 7, "M"),                       # One Island's NE headland runs on
    (18, 18, 8, 4, "."), (20, 17, 4, 1, "."),                   # small islets
    (20, 19, 2, 2, "G"),
    (40, 6, 10, 8, "."), (42, 5, 6, 1, "."), (42, 14, 6, 1, "."),   # grassy islet
    (42, 7, 4, 4, "G"),                                         # its trees
    (60, 19, 8, 4, "."), (62, 18, 4, 1, "."),
    (70, 3, 6, 4, "."), (72, 4, 2, 2, "G"),
])
SEA_A_ROCKS = [(10, 12), (14, 4), (30, 10), (33, 22), (52, 18), (56, 3), (66, 12), (74, 22), (28, 2)]
SEA_ROUTE_A = dict(
    name="Sevii Sea Route A", size=(80, 28), tileset=DEW,
    ground=SEA,
    mask=vc.ring_multi(SEA_A_MASK, [(".G", "R", "W"), ("s", "S", "w")]),
    mask_legend={"~": SEA, ".": I(GRASS), "G": I(GRASS), "s": I(SAND), "S": I(SAND)},
    edges_list=coast_edges(),
    big_trees="G",
    pstamps=[at(SEA_ROCK if i % 3 else SEA_ROCK_BIG, x, y) for i, (x, y) in enumerate(SEA_A_ROCKS)],
    marks=[
        (1, 14, "< One Island", "conn"), (72, 14, "Two Island >", "conn"),
        (23, 19, "", "item", "item"), (46, 12, "", "npc", "fisherman"),
        (12, 18, "", "npc", "swimmer"), (36, 8, "", "npc", "swimmer"), (58, 14, "", "npc", "swimmer"),
    ],
)
ALL["sea_route_a"] = SEA_ROUTE_A

# Sea Route B: Two Island (9,9) -> Bond Bridge's west end (14,12), a diagonal: west edge = Two Island's
# east edge (offset 0: rows 0-5 rock, the rest sea), east edge = Bond Bridge's west edge (offset +28, all
# sea). The islet south-east of Two Island on the region map (10-11,11) is the grassy island here.
SEA_B_MASK = paint(64, 48, "~", [
    (0, 0, 6, 6, "M"), (6, 0, 4, 4, "M"),                       # Two Island's NE rock runs on
    (16, 22, 12, 10, "."), (18, 21, 8, 1, "."), (18, 32, 8, 1, "."),   # the islet
    (18, 23, 4, 4, "G"), (22, 27, 4, 2, "G"),
    (40, 7, 8, 4, "."), (42, 8, 2, 2, "G"),                     # small islets
    (44, 38, 8, 4, "."),
])
SEA_B_ROCKS = [(12, 10), (20, 4), (30, 14), (34, 26), (50, 18), (56, 26), (8, 38), (32, 42), (54, 4),
               (60, 12)]
SEA_ROUTE_B = dict(
    name="Sevii Sea Route B", size=(64, 48), tileset=DEW,
    ground=SEA,
    mask=vc.ring_multi(SEA_B_MASK, [(".G", "R", "W"), ("s", "S", "w")]),
    mask_legend={"~": SEA, ".": I(GRASS), "G": I(GRASS), "s": I(SAND), "S": I(SAND)},
    edges_list=coast_edges(),
    big_trees="G",
    pstamps=[at(SEA_ROCK if i % 3 else SEA_ROCK_BIG, x, y) for i, (x, y) in enumerate(SEA_B_ROCKS)],
    marks=[
        (1, 12, "< Two Island", "conn"), (54, 37, "Bond Bridge >", "conn"),
        (24, 26, "", "item", "item"), (22, 30, "", "npc", "picnicker"),
        (14, 16, "", "npc", "swimmer"), (40, 30, "", "npc", "swimmer"), (46, 14, "", "npc", "swimmer"),
    ],
)
ALL["sea_route_b"] = SEA_ROUTE_B

# Overview: each map's top-left in a shared tile grid (connection offsets above; Mt. Ember / summit /
# Cape Brink / Berry Forest placed by their region-map cells). Berry Forest is entered by a warp, so it is
# drawn north of Bond Bridge's west landing where FRLG has it.
OVERVIEW = {
    "one_island": (0, 0),
    "kindle_road": (4, -96),           # Kindle x0 = One Island x4; its bottom row meets One Island's top
    "mt_ember": (3, -144),             # Mt. Ember x = Kindle Road x - 1
    "mt_ember_summit": (-1, -168),     # warp only; drawn above Mt. Ember's top stairs
    "sea_route_a": (32, 0),
    "two_island": (112, 4),            # Sea Route A east edge, offset +4
    "cape_brink": (120, -28),          # Two Island north edge, offset +8
    "sea_route_b": (152, 4),
    "bond_bridge": (216, 32),          # Sea Route B east edge, offset +28
    "three_island": (280, 28),         # Bond Bridge east edge, offset -4
    "berry_forest": (216, -4),         # warp only; drawn north of Bond Bridge's west landing
}
