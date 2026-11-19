"""
Sailor's Voyages, batch 1: design-review mockup specs (not real maps). See voyage_compose.py for the spec
format. Every cell is copied from a layout with the same primary+secondary pair, so no tileset changes.

Post-game: a Sailor and his Son live in a fisherman's hut on Wavebreak Town's beach. After the Champion
he sails the player in his small boat (OBJ_EVENT_GFX_MR_BRINEYS_BOAT) to passcode islands; at each island
he and the boat wait at a dock to take the player home.
"""
import voyage_compose as vc

TP = ("gTileset_General", "gTileset_TosaPort")
WB = "LAYOUT_WAVEBREAK_TOWN"
TOSA = "LAYOUT_TOSA_PORT"


def I(mid, *ce):
    return ("id", mid) + ce


# ---------------------------------------------------------------------------------------------- Wavebreak
# Untouched today: x0-9 sea (0x170) with sea rocks, x10 shore (0x123), x11 sand strip (0x124).
WAVEBREAK_BEFORE_MARKS = [
    (11, 26, "fisher", "npc", "fisherman"), (12, 18, "sailor NPC", "npc", "sailor"),
    (14, 23, "Centre", "warp"), (26, 23, "Mart", "warp"), (20, 13, "H1", "warp"), (14, 15, "H2", "warp"),
    (28, 15, "H3", "warp"), (19, 30, "", "sign"),
]

SEA = I(0x170, 0, 1)
# fisherman frames: 0 down, 1 up, 2 left (right = flipped); registered here so voyage_compose stays untouched
vc.SPRITES.setdefault("fisherman_left", ("graphics/object_events/pics/people/fisherman.png", 16, 32, 2, False))


def _npc_pal_sprite(key, pal_file):
    """Pre-load an overworld sprite with its in-game palette (the PNG's own palette differs)."""
    import os
    from PIL import Image
    path, fw, fh, fi, flip = vc.SPRITES[key]
    im = Image.open(os.path.join(vc.ROOT, path)).crop((fi * fw, 0, fi * fw + fw, fh))
    pal = vc.vanilla.load_jasc(os.path.join(vc.ROOT, "graphics/object_events/palettes", pal_file))
    px = im.load()
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    op = out.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y]:
                op[x, y] = pal[px[x, y]] + (255,)
    vc._SPR[key] = out.transpose(Image.FLIP_LEFT_RIGHT) if flip else out


for _k in ("fisherman", "fisherman_left"):
    _npc_pal_sprite(_k, "npc_2.pal")      # OBJ_EVENT_PAL_TAG_NPC_2, as gObjectEventGraphicsInfo_Fisherman

# Mr. Briney's wooden dock (Route 104) needs metatiles appended to gTileset_TosaPort (approved addition, not
# applied yet: see tileset_addition_batch1.py); here it is drawn as an overlay of the Rustboro metatiles.
# Cells: (x, y, name in tileset_addition_batch1 / "dock_<id>"). Underneath, the grid keeps sea / sand.
DOCK = [(3, 28, "dock_33D"), (3, 29, "dock_345"), (3, 30, "dock_335")] + \
       [(x, 28, "dock_26E") for x in (4, 5, 6)] + [(x, 29, "dock_26D") for x in (4, 5, 6)] + \
       [(x, 30, "dock_276") for x in (4, 5, 6)]
BEACH_PROPS = [
    (11, 27, "fish_crate_sand"), (11, 28, "crates_stacked_sand"),   # by the fisherman at (11,26)
    (11, 11, "fish_crate_sand"),                                     # by the fisherman at (11,10)
    (11, 18, "rods_top"), (11, 19, "rods_base"), (11, 20, "bucket_sand"),   # by the fisherman at (11,17)
    (9, 29, "rods_top"), (9, 30, "rods_base"), (10, 30, "bucket_sand"),     # by the beach fisherman at (8,30)
]

WAVEBREAK_AFTER = dict(
    name="Wavebreak Town (patched)", size=(36, 34), tileset=TP, base=WB,
    fill=[
        # clear the sea-rock clumps that sit on the dock / boat berth
        (0, 28, 2, 2, SEA), (0, 30, 2, 2, SEA), (2, 30, 2, 2, SEA),
        # the beach: x7-10, y28-30 sand, on top of the old 1-tile strip at x11
        (7, 28, 4, 3, I(0x124)),
        (6, 28, 1, 3, I(0x123)),
        (7, 27, 3, 1, I(0x11C)), (8, 31, 2, 1, I(0x12C)),
    ],
    cells=[
        (6, 27, I(0x11B)), (10, 27, I(0x13D)),     # shore steps out (top)
        (7, 30, I(0x145)),                          # the water under the dock's face reaches the beach
        (7, 31, SEA), (6, 31, SEA),
        (10, 31, I(0x145)),                         # and back in at y31; y32-33 stay as they are
    ],
    stamps=[
        # the hut: Wavebreak's red-roof General house (same 4x4 as House 1), door at (13,29)
        (WB, 19, 10, 4, 4, 12, 26),
        # House 1 (x19-22) and House 3 (x27-30) repainted as House 2's purple TosaPort house, so the hut is
        # the only red roof; all three keep the door in column 1 (warps 20,13 and 28,15 unchanged)
        (WB, 13, 12, 4, 4, 19, 10),
        (WB, 13, 12, 4, 4, 27, 12),
    ],
    post=[
        (16, 27, (TOSA, 15, 27)), (16, 28, (TOSA, 15, 28)),   # Tosa Port's crates beside the hut (on grass)
    ],
    proposed=DOCK + BEACH_PROPS,     # drawn by mock_batch1 from tileset_addition_batch1.render()
    marks=[
        (4, 31, "boat", "boat", "boat_up"),          # as on Route 104: below the 2nd plank column, bow up
        (4, 29, "Sailor", "sailor", "sailor"),
        (13, 29, "hut", "warp"),
        (11, 26, "fisher", "npc", "fisherman_left"),
        (11, 10, "fisher2", "npc", "fisherman_left"),
        (11, 17, "fisher3", "npc", "fisherman_left"),
        (8, 30, "fisher4", "npc", "fisherman"),
        (12, 18, "sailor NPC", "npc", "sailor"),
        (14, 23, "Centre", "warp"), (26, 23, "Mart", "warp"), (20, 13, "H1", "warp"), (14, 15, "H2", "warp"),
        (28, 15, "H3", "warp"), (19, 30, "", "sign"),
    ],
)

ALL = {"wavebreak_after": WAVEBREAK_AFTER}


# ---------------------------------------------------------------------------------------------- Fullmoon
# Remake of Platinum's Fullmoon Island (ref/fullmoon_ext.png, ~30x21 Gen 4 tiles) in General + Rustboro:
# the Southern Island / Faraway Island rock rim (rock face straight into the sea), 1-wide General forest,
# Route 104's wooden pier, Southern Island's forest-gap entrance.
RB = ("gTileset_General", "gTileset_Rustboro")
R104 = "LAYOUT_ROUTE104"
SI_EXT = "LAYOUT_SOUTHERN_ISLAND_EXTERIOR"

RIM = [0x002, 0x073, 0x075, 0x07B, 0x07C, 0x07D, 0x089, 0x074, 0x07A, 0x0A9, 0x079]
SEA_EDGE = [0x170, 0x180, 0x181, 0x189, 0x190, 0x192, 0x198, 0x19A, 0x15A, 0x15B, 0x171, 0x172, 0x174]
FOREST = [0x0C6, 0x0C7, 0x016, 0x017, 0x00E, 0x00F]


def mask_ok(rows, w, h):
    assert len(rows) == h, len(rows)
    for i, r in enumerate(rows):
        assert len(r) == w, (i, len(r), r)
    return rows


#                       x: 0123456789012345678901234567890 1
FULLMOON_EXT_MASK = mask_ok([
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 0
    "~~~~~~~~~~................~~~~~~",   # 1
    "~~~~~~~~~..TTTTTTTTTTTTTT..~~~~~",   # 2
    "~~~~~~~~~..TTTTTTTTTTTTTT..~~~~~",   # 3
    "~~~~~.....TTTTTTTTTTTTTTTTT..~~~",   # 4
    "~~~~~..TTTTTTTTTTTTTTTTTTTT...~~",   # 5
    "~~~~~..TTTTTTTTTTTTTTTTTTTTTT.~~",   # 6
    "~~.....TTTTTTTTTTTTTTTTTTTTTT.~~",   # 7
    "~..TT..TTTT..f.TTTT....TTTTTT.~~",   # 8
    "~..TT...........f.f.....TTTTT.~~",   # 9
    "~..TT...TT...........TT.TT..f.~~",   # 10
    "~.f.....TT.ffff....TTTTTTTT.ff.~",   # 11
    "~.f...........TTTTTTTTTTTTT..f.~",   # 12
    "~.f.TT........TTTTTTTTTTTT..ff.~",   # 13
    "~.f.TT..~~~~~..TTTTTTTTTTT.....~",   # 14
    "~...TT..~~~~~.ffff.TTTT.......~~",   # 15
    "~...TT..~~~~~.ffff.TTTT......~~~",   # 16
    "~.......~~~~~................~~~",   # 17
    "~~......~~~~~....ffff.......~~~~",   # 18
    "~~~.....~~~~~...............~~~~",   # 19
    "~~~~...~~~~~~..............~~~~~",   # 20
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 21
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 22
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 23
], 32, 24)

FULLMOON_EXT = dict(
    name="Fullmoon Island", size=(32, 24), tileset=RB,
    ground=I(0x170),
    mask=vc.ring_classes(FULLMOON_EXT_MASK, land_chars=".fT"),
    mask_legend={"~": I(0x170), ".": I(0x001), "f": I(0x004)},
    mask_auto={"T": FOREST},
    edges=dict(chars="RW", water_chars="~W", vocab=RIM + SEA_EDGE,
               layouts=[SI_EXT, "LAYOUT_FARAWAY_ISLAND_ENTRANCE"]),
    stamps=[
        (SI_EXT, 13, 4, 4, 3, 19, 5),     # forest gap + dark path = warp into the interior (as Southern Island)
        (R104, 11, 51, 4, 3, 10, 15),     # wooden pier, land end at x13
    ],
    # one-way ledge (0D5 / 087 / 0D6): the flower meadow south of it is a step lower, like Platinum's
    # inner terrace; walk back up through the gap at x25-27
    fill=[(16, 17, 8, 1, I(0x087))],
    cells=[(15, 17, I(0x0D5)), (24, 17, I(0x0D6))],
    marks=[
        (20, 6, "to int", "warp"), (21, 6, "to int", "warp"),
        (11, 18, "boat", "boat", "boat_up"),
        (11, 16, "Sailor", "sailor", "sailor"),
    ],
)
ALL["fullmoon_ext"] = FULLMOON_EXT

SI_INT = "LAYOUT_SOUTHERN_ISLAND_INTERIOR"
# Southern Island's pond set: edges drawn inside the water cells (0C8 0C9 0CA / 0D0 0D1 0D2 / 0D8 0D9 0DA)
POND = [0x0C8, 0x0C9, 0x0CA, 0x0D0, 0x0D1, 0x0D2, 0x0D8, 0x0D9, 0x0DA]
POND_TRAIN = [SI_INT]

FULLMOON_INT_MASK = mask_ok([
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 0
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 1
    "TTTTTTTTTT....TTTTTTTTTT",   # 2
    "TTTTTTTTTT.f..TTTTTTTTTT",   # 3
    "TTTTTTTT.f......f.TTTTTT",   # 4
    "TTTTTTTT.....wwww.TTTTTT",   # 5
    "TTTTTT.f....wwwwww..TTTT",   # 6
    "TTTTTT......wwwwwww.TTTT",   # 7
    "TTTTTT.f....wwwwwww.TTTT",   # 8
    "TTTTTT.......wwwww.fTTTT",   # 9
    "TTTTTT..f.....www...TTTT",   # 10
    "TTTTTT.f............TTTT",   # 11
    "TTTTTTTT..f....f..TTTTTT",   # 12
    "TTTTTTTT..........TTTTTT",   # 13
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 14  exit stamp at x10-15
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 15
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 16
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 17
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 18
    "TTTTTTTTTTTTTTTTTTTTTTTT",   # 19
], 24, 20)

FULLMOON_INT = dict(
    name="Fullmoon Island interior", size=(24, 20), tileset=RB,
    ground=I(0x001),
    mask=vc.ring_classes(FULLMOON_INT_MASK, land_chars=".f", sea_chars="w"),
    mask_legend={".": I(0x001), "f": I(0x004), "R": I(0x001), "w": I(0x0D1)},
    edges=dict(chars="W", water_chars="wW", vocab=POND, layouts=POND_TRAIN),
    big_trees="T",
    stamps=[(SI_INT, 11, 18, 6, 6, 10, 14)],   # Southern Island interior's exit path through the trees
    marks=[
        (12, 14, "exit", "warp"), (13, 14, "exit", "warp"),
        (11, 7, "Cresselia", "legendary", "cresselia_right"),
    ],
)
ALL["fullmoon_int"] = FULLMOON_INT


# ---------------------------------------------------------------------------------------------- Newmoon
# Remake of Platinum's Newmoon Island (ref/newmoon_ext.png, ~32x25 Gen 4 tiles) in General + Dewford
# (not Fallarbor, per the user): Dewford's sand ground and dark 1-wide coastal trees, Dewford's wooden pier,
# General boulders (0E2) and the General rock massif (Southern / Faraway Island) for the rocky plateaus,
# the same rock rim into the sea as Fullmoon. Eerier than Fullmoon by content (bare sand, rock, dark trees,
# no flowers) plus a header weather (WEATHER_SHADE or fog) -- palettes are never edited.
DEW_PAIR = ("gTileset_General", "gTileset_Dewford")
DEW = "LAYOUT_DEWFORD_TOWN@git"            # vanilla Dewford (the working-tree one is Orchid's)
FARAWAY = "LAYOUT_FARAWAY_ISLAND_ENTRANCE"
DEW_TREES = [0x243, 0x239, 0x23A]          # Dewford's trees: crowns 243/239, trunk-on-sand bottom 23A
ROCK_VOCAB = sorted(vc.ROCK_IDS)
RIM_NOLIP = [m for m in RIM if m != 0x002]    # 0x002 carries a green grass lip
ROCK_TRAIN = [SI_EXT, FARAWAY, "LAYOUT_ROUTE120"]
# beach shore (water cells with sand drawn in) for a pond sunk in sand
SHORE = [0x170, 0x11B, 0x11C, 0x11D, 0x123, 0x125, 0x12B, 0x12C, 0x12D, 0x13D, 0x13E, 0x145, 0x146, 0x124]
SHORE_TRAIN = [R104, DEW, "LAYOUT_ROUTE105", "LAYOUT_ROUTE107"]

NEWMOON_EXT_MASK = mask_ok([
    # The General rock rim has no north-facing edge for non-grass ground (Faraway's lip 0x002 is green), so
    # like Southern Island the island runs off the top of the map and its coast only recedes going south.
    "~.TTTTTTTTTTTTTT.MMMMMMM.......~",   # 0
    "~.TTTTTTTTTTTTTT.MMMMMMM.......~",   # 1
    "~.TTTTTTTTTTTTTT.MMMMMMM...b...~",   # 2
    "~.TTTTTTTTTTTTTT.MMMMMMM.......~",   # 3
    "~.TTTTTTTTTTTTTT.MMMMMMM.....b.~",   # 4
    "~.TTTTTTTTTTTTTT..MMMMM........~",   # 5
    "~.TTTTTTTT..TTTT...............~",   # 6
    "~.TTTTTTTT..TTTT.........b.....~",   # 7
    "~.TTTTTT......TT..........b....~",   # 8
    "~.TTTTTT......TT...b.......b...~",   # 9
    "~.TTTTTT......TTb..............~",   # 10
    "~.TTTTTT......TT......b........~",   # 11
    "~.b.TTTT..............b.....b..~",   # 12
    "~...TTTT.......b...........b...~",   # 13
    "~...b............~~~~~~~.......~",   # 14
    "~.........MMMMMM.~~~~~~~...b...~",   # 15
    "~.........MMMMMM.~~~~~~~.....~~~",   # 16
    "~~~.......MMMMMM.~~~~~~~.....~~~",   # 17
    "~~~~~~~~..b......~~~~~~~..b..~~~",   # 18
    "~~~~~~~~.........~~~~~~~.....~~~",   # 19
    "~~~~~~~~~......~~~~~~~~~....~~~~",   # 20
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 21
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 22
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 23
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 24
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",   # 25
], 32, 26)

NEWMOON_EXT = dict(
    name="Newmoon Island", size=(32, 26), tileset=DEW_PAIR,
    ground=I(0x170),
    mask=vc.ring_classes(NEWMOON_EXT_MASK, land_chars=".TbM"),
    mask_legend={"~": I(0x170), ".": I(0x124), "b": I(0x0E2), "T": I(0x243)},
    edges_list=[
        dict(chars="RW", water_chars="~W", vocab=RIM_NOLIP + SEA_EDGE, layouts=[SI_EXT, FARAWAY]),
        dict(kind="rock", chars="M", water_chars="M", vocab=ROCK_VOCAB, layouts=ROCK_TRAIN),
    ],
    # Dewford's pier (land end + 3 planks, 2 rows), land end on the bay's west wall
    stamps=[(DEW, 11, 9, 4, 2, 16, 15)],
    cells=vc.small_trees(NEWMOON_EXT_MASK, "T", 0x243, 0x239, 0x23A),
    post=[(19, 16, I(0x170, 0, 1))],     # drop the stamped sand corner beyond the pier tip
    marks=[
        (10, 6, "to int", "warp"), (11, 6, "to int", "warp"),
        (20, 15, "boat", "boat", "boat_left"),
        (18, 15, "Sailor", "sailor", "sailor_right"),
    ],
)
ALL["newmoon_ext"] = NEWMOON_EXT

NEWMOON_INT_MASK = mask_ok([
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTT",   # 0
    "TTTTTTTTTTTTTTTTTTTTTTTTTTTT",   # 1
    "TTTTTTTTTT........TTTTTTTTTT",   # 2
    "TTTTTTTT.....b......TTTTTTTT",   # 3
    "TTTTTT....MMMMMMMM....b.TTTT",   # 4
    "TTTTTT...MMMMMMMMMM.....TTTT",   # 5
    "TTTTTT..MMM......MMM....TTTT",   # 6
    "TTTTTT..MM...ww...MM....TTTT",   # 7
    "TTTTTT..MM..wwww..MM....TTTT",   # 8
    "TTTTTT..MM.wwwwww.MM....TTTT",   # 9
    "TTTTTT..MM.wwwwww.MM....TTTT",   # 10
    "TTTTTT..MM..wwww..MM....TTTT",   # 11
    "TTTTTT..MMM..ww..MMM....TTTT",   # 12
    "TTTTTT...MMMM..MMMM.....TTTT",   # 13  gap at x13-14 = the way down into the crater
    "TTTTTT....MMM..MMM......TTTT",   # 14
    "TTTTTT..b...........b...TTTT",   # 15
    "TTTTTTTT..............TTTTTT",   # 16
    "TTTTTTTTTT..........TTTTTTTT",   # 17
    "TTTTTTTTTTTT....TTTTTTTTTTTT",   # 18
    "TTTTTTTTTTTT....TTTTTTTTTTTT",   # 19
    "TTTTTTTTTTTT....TTTTTTTTTTTT",   # 20
    "TTTTTTTTTTTT....TTTTTTTTTTTT",   # 21
], 28, 22)

NEWMOON_INT = dict(
    name="Newmoon Island interior", size=(28, 22), tileset=DEW_PAIR,
    ground=I(0x124),
    mask=vc.ring_classes(NEWMOON_INT_MASK, land_chars=".b", sea_chars="w"),
    mask_legend={".": I(0x124), "b": I(0x0E2), "w": I(0x170), "T": I(0x243)},
    cells=vc.small_trees(NEWMOON_INT_MASK, "T", 0x243, 0x239, 0x23A),
    edges_list=[
        dict(kind="shore", chars="RW", water_chars="wW", vocab=SHORE, layouts=SHORE_TRAIN),
        dict(kind="rock", chars="M", water_chars="M", vocab=ROCK_VOCAB, layouts=ROCK_TRAIN),
    ],
    marks=[
        (13, 21, "exit", "warp"), (14, 21, "exit", "warp"),
        (13, 10, "Darkrai", "legendary", "darkrai"),
    ],
)
ALL["newmoon_int"] = NEWMOON_INT


# ---------------------------------------------------------------------------------------------- as-is maps
# Rendered unchanged with marks: the hut interior (vanilla Mr. Briney's cottage, deleted from the working
# tree with the Hoenn maps, read from git) and Southern Island = Eon Island.
AS_IS = {
    "sailor_hut_int": ("LAYOUT_ROUTE104_MR_BRINEYS_HOUSE", [
        (5, 4, "Sailor", "sailor", "sailor"),
        (9, 5, "Son", "son", "son"),
        (5, 8, "exit", "warp"), (6, 8, "exit", "warp"),
    ]),
    "eon_ext": ("LAYOUT_SOUTHERN_ISLAND_EXTERIOR", [
        (13, 25, "boat", "boat", "boat_up"),          # replaces the S.S. Tidal object at the same spot
        (13, 23, "Sailor", "sailor", "sailor"),        # = the vanilla Sailor's spot on the gangway
        (14, 5, "to int", "warp"), (15, 5, "to int", "warp"),
        (16, 7, "", "sign"),
    ]),
    "eon_int": ("LAYOUT_SOUTHERN_ISLAND_INTERIOR", [
        (13, 11, "Lati", "legendary", "latias"),       # lands over the Eon stone (LatiApproach ends here)
        (8, 8, "Latiasite", "item", "item"),           # flower patches on the west and east banks
        (18, 8, "Latiosite", "item", "item"),
        (13, 18, "exit", "warp"), (14, 18, "exit", "warp"),
    ]),
}
SHADE_PREVIEW = ("newmoon_ext", "newmoon_int")
