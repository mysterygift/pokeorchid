"""
Mockups of the five Tiksi Regi caves: one small room each, Regi in the centre, cave exit at the bottom.

Every cell is copied from an existing vanilla layout that uses the same primary+secondary tileset pair
(compose.py asserts this), so no tile or metatile is added or edited and no other map can change.

    python cave_specs.py OUT_DIR      -> OUT_DIR/cave_<n>_<slug>.png at scale 3
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compose  # noqa: E402

CAVE = ("gTileset_General", "gTileset_Cave")
METEOR = ("gTileset_General", "gTileset_MeteorFalls")

RUINS = "LAYOUT_DESERT_RUINS"
SHOAL = "LAYOUT_SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM"
ICE = "LAYOUT_SHOAL_CAVE_LOW_TIDE_ICE_ROOM"
OUTER = "LAYOUT_SEALED_CHAMBER_OUTER_ROOM"
INNER = "LAYOUT_SEALED_CHAMBER_INNER_ROOM"
ORIGIN_B1F = "LAYOUT_CAVE_OF_ORIGIN_B1F"
ORIGIN_1F = "LAYOUT_CAVE_OF_ORIGIN_1F"
MF_1F = "LAYOUT_METEOR_FALLS_1F_1R"
MF_B1F = "LAYOUT_METEOR_FALLS_B1F_1R"
MF_B1F2 = "LAYOUT_METEOR_FALLS_B1F_2R"


def put(rows, legend, ox=0, oy=0):
    """Char grid -> 1x1 stamps (applied in order after earlier stamps). '.' or ' ' = leave as is."""
    out = []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch not in ". ":
                lid, sx, sy = legend[ch]
                out.append((lid, sx, sy, 1, 1, ox + x, oy + y))
    return out


def remap(lid, cols, rows):
    """Stamps that rebuild a layout from a subset of its columns/rows (target = index in the lists)."""
    return [(lid, sx, sy, 1, 1, dx, dy) for dy, sy in enumerate(rows) for dx, sx in enumerate(cols)]


# ---------------------------------------------------------------------------------------------------
# 1. Regolis Shrine (Regirock): the vanilla Desert Ruins chamber, re-dressed as a sand-choked desert
#    shrine: a sand bed under Regirock, two braille tablets flanking it, rubble kept at the corners.
REGOLIS = {
    "name": "RegolisShrine", "title": "Regolis Shrine (Regirock)", "slug": "regolis_shrine",
    "size": (17, 14), "tileset": CAVE,
    "ground": (RUINS, 5, 5),
    "stamps": [(RUINS, 0, 0, 17, 14, 0, 0)] + put([
        ".................",
        ".................",
        ".................",
        ".................",
        "......f...f......",   # vanilla rubble at (6,4) (10,4) cleared off the sand bed
        "......7888[......",
        "...TUV<sss>UTV...",
        "...WXY<sss>WXY...",   # rubble at (4,7) (12,7) replaced by braille tablets
        "......1222]......",
        ".................",
        "......o...o......",   # rubble kept either side of the path
    ], {
        "f": (RUINS, 5, 5),                                   # plain chamber floor
        "o": (RUINS, 6, 10),                                  # rubble pile
        "7": (SHOAL, 18, 7), "8": (SHOAL, 14, 14), "[": (SHOAL, 19, 7),      # sand bed, top
        "<": (SHOAL, 12, 16), "s": (SHOAL, 18, 8), ">": (SHOAL, 20, 9),      # sand bed, sides
        "1": (SHOAL, 17, 9), "2": (SHOAL, 19, 10), "]": (SHOAL, 20, 10),     # sand bed, bottom
        "T": (OUTER, 15, 5), "U": (OUTER, 16, 5), "V": (OUTER, 17, 5),       # braille tablet
        "W": (OUTER, 15, 6), "X": (OUTER, 16, 6), "Y": (OUTER, 17, 6),
    }),
    "marks": [(8, 6, "Regirock", "regi"), (8, 11, "exit", "warp")],
    "sources": [RUINS, SHOAL, OUTER],
    "notes": "Desert Ruins shell (exit warp tile + mat unchanged); sand bed from Shoal Cave entrance room "
             "(sand on the same raised floor); 3-wide braille tablets from Sealed Chamber outer room.",
}

# ---------------------------------------------------------------------------------------------------
# 2. Frigo Cave (Regice): the blue ice set from Shoal Cave's ice room. Gen 3 has no blue cave-mouth
#    mat, so (like vanilla's ice room) the way in is the blue ladder, set in a rock outcrop at the
#    bottom middle. A dry path rings an ice dais; ice sheets with frozen boulders fill the sides.
FRIGO = {
    "name": "FrigoCave", "title": "Frigo Cave (Regice)", "slug": "frigo_cave",
    "size": (15, 15), "tileset": CAVE,
    "ground": (ICE, 11, 8),
    "rows": [
        "A-------------B",
        "LA-----------BR",
        "LLuufffffffuuRR",
        "LLiieptttqwiiRR",
        "LLiielsssrwiiRR",
        "LLoielsssrwOiRR",
        "LLiieghShkwiiRR",
        "LLiiefffffwiiRR",
        "LLioefffffwiiRR",
        "LLiiefffffwioRR",
        "LLiiefpTqfwiiRR",
        "LLvvffgHkffvvRR",
        "LLfffffFfffffRR",
        "cc___________dd",
        "###############",
    ],
    "legend": {
        "A": (ICE, 0, 0), "-": (ICE, 5, 0), "B": (ICE, 16, 0),          # wall face + its corners
        "L": (ICE, 0, 5), "R": (ICE, 18, 15),                           # side walls
        "c": (ICE, 0, 27), "_": (ICE, 5, 28), "d": (ICE, 18, 29), "#": (ICE, 0, 20),   # bottom edge
        "f": (ICE, 11, 8),                                              # dry floor
        "i": (ICE, 3, 2), "u": (ICE, 14, 12), "v": (ICE, 11, 7),        # ice, ice top / bottom edge
        "e": (ICE, 14, 11), "w": (ICE, 11, 12),                         # ice right / left edge
        "o": (ICE, 3, 3), "O": (ICE, 6, 2),                             # frozen boulders
        "p": (ICE, 6, 7), "t": (ICE, 7, 7), "q": (ICE, 10, 7),          # dais top edge
        "l": (ICE, 5, 9), "s": (ICE, 7, 9), "r": (ICE, 10, 8),          # dais sides + top
        "g": (ICE, 3, 13), "h": (ICE, 5, 13), "k": (ICE, 14, 23), "S": (ICE, 4, 13),   # dais face, steps
        "T": (ICE, 5, 28), "H": (ICE, 17, 9), "F": (ICE, 17, 10),       # outcrop + ladder
    },
    "marks": [(7, 4, "Regice", "regi"), (7, 12, "ladder", "warp")],
    "sources": [ICE],
    "notes": "All ice-room metatiles. Entrance is the ice-room ladder (the only blue warp metatile any "
             "layout uses); the dais is the ice room's raised plateau with its blue steps.",
}

# ---------------------------------------------------------------------------------------------------
# 3. Ferrum Shrine (Registeel): Sealed Chamber inner room, cut down. Registeel stands between the two
#    pillar pairs under the great braille tablet; dark grey-violet stone, symmetrical, tomb-like.
_FER_COLS = [0, 1, 2, 3, 5, 6, 7, 8, 10, 12, 13, 14, 15, 17, 18, 19, 20]
_FER_ROWS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 18, 19, 20, 21, 22]
FERRUM = {
    "name": "FerrumShrine", "title": "Ferrum Shrine (Registeel)", "slug": "ferrum_shrine",
    "size": (17, 15), "tileset": CAVE,
    "ground": (INNER, 9, 9),
    "stamps": remap(INNER, _FER_COLS, _FER_ROWS) + put([
        "....fff...fff....",   # row 10 = source row 18: drop the lower pillars' feet
        ".................",
        ".......<.>.......",   # exit mat ends (source x 9 / 11 were cut)
    ], {
        "f": (INNER, 9, 9), "<": (INNER, 9, 20), ">": (INNER, 11, 20),
    }, 0, 10),
    "marks": [(8, 7, "Registeel", "regi"), (8, 11, "exit", "warp")],
    "sources": [INNER],
    "notes": "Sealed Chamber inner room: columns 4/9/11/16 and rows 10-17 removed along plain-floor "
             "seams; the 5-wide wall tablet becomes 3 wide; bottom diagonal corners kept whole.",
}

# ---------------------------------------------------------------------------------------------------
# 4. Gavani Path (Regieleki): Cave of Origin B1F, the crystal-studded chamber (blue and red crystals in
#    the walls read as charged). Regieleki takes the centre of the boulder ring in the sunken basin; a
#    raised-floor causeway leads in from the south. Exit mat from Cave of Origin 1F.
_GAV = [(ORIGIN_B1F, 8, 2, 1, 1, 9, 2),     # ladder top -> wall face
        (ORIGIN_B1F, 7, 3, 1, 1, 9, 3),     # ladder foot -> floor
        (ORIGIN_B1F, 8, 9, 1, 1, 9, 9),     # centre boulder -> basin floor (Regieleki)
        (ORIGIN_B1F, 7, 3, 1, 1, 9, 10),    # causeway (raised-floor cells, elevation 3)
        (ORIGIN_B1F, 7, 3, 1, 1, 9, 11),
        (ORIGIN_B1F, 7, 3, 1, 1, 9, 12),    # south boulder of the ring -> causeway
        (ORIGIN_1F, 11, 17, 1, 1, 9, 14),   # exit warp floor
        (ORIGIN_1F, 10, 18, 3, 1, 8, 15)]   # exit mat in the bottom lip
GAVANI = {
    "name": "GavaniPath", "title": "Gavani Path (Regieleki)", "slug": "gavani_path",
    "size": (17, 16), "tileset": CAVE,
    "ground": (ORIGIN_B1F, 7, 3),
    "stamps": [(ORIGIN_B1F, 0, 0, 19, 19, 0, 0)] + _GAV,
    "marks": [(8, 8, "Regieleki", "regi"), (8, 13, "exit", "warp")],
    "sources": [ORIGIN_B1F, ORIGIN_1F],
    "notes": "Cave of Origin B1F cropped to x1-17, y1-16; ladder removed; boulder ring opened on the "
             "south; causeway cells copied from the raised floor so they sit at the ring's elevation.",
}
# crop: everything above was placed in B1F coordinates; shift by (-1, -1) into the 17x16 frame
GAVANI["stamps"] = [(l, sx, sy, w, h, dx - 1, dy - 1) for (l, sx, sy, w, h, dx, dy) in GAVANI["stamps"]]

# ---------------------------------------------------------------------------------------------------
# 5. Mt. Drake summit (Regidrago): Meteor Falls set. Stalactite wall with two of the gold light-columns,
#    meteor craters (the beam scars) either side, Regidrago on the tall stepped rock from B1F's west room.
REGIDRAGO = {
    "name": "MtDrakeSummit", "title": "Mt. Drake Summit (Regidrago)", "slug": "mt_drake_summit",
    "size": (17, 16), "tileset": METEOR,
    "ground": (MF_B1F2, 3, 3),
    "rows": [
        "xxxxxxxxxxxxx....",
        "x^^^^^^^^^^^^....",
        "1{WWWWWWWWWWW....",
        "12{WWWWWWWWWW....",
        "122{WWWWWWWWW....",
        "122a.........b889",
        "122...........889",
        "122...........889",
        "122...........889",
        "122...........889",
        "122...........889",
        "122...........889",
        "122...........889",
        "122.....E.....889",
        "12=====(+)====889",
        "x===============x",
    ],
    "legend": {
        "x": (MF_B1F2, 0, 0), "^": (MF_B1F, 14, 0), "/": (MF_B1F, 12, 1),
        "W": (MF_B1F, 13, 1), "<": (MF_B1F, 12, 2), "{": (MF_B1F, 7, 2),
        "1": (MF_B1F2, 0, 3), "2": (MF_B1F2, 1, 3), "8": (MF_B1F2, 8, 3), "9": (MF_B1F2, 10, 3),
        "=": (MF_B1F2, 3, 16), "(": (MF_B1F2, 4, 16), "+": (MF_B1F2, 5, 16), ")": (MF_B1F2, 6, 16),
        "E": (MF_B1F2, 5, 15),
        "a": (MF_B1F, 9, 4), "b": (MF_B1F, 22, 4),            # boulders
    },
    "stamps": [
        (MF_B1F, 24, 0, 4, 5, 13, 0),        # top-right corner: stalactite face stepping into the wall
        (MF_1F, 1, 0, 2, 3, 5, 2),           # gold light-column
        (MF_1F, 1, 0, 2, 3, 10, 2),          # gold light-column
        (MF_B1F, 5, 9, 5, 6, 6, 6),          # tall stepped rock (summit dais)
        (MF_B1F, 7, 12, 1, 1, 8, 7),         # its ladder -> plain dais top
        (MF_B1F, 7, 12, 1, 1, 8, 8),
        (MF_1F, 2, 5, 2, 2, 3, 7),           # meteor craters
        (MF_1F, 2, 5, 2, 2, 12, 7),
        (MF_1F, 2, 5, 2, 2, 3, 11),
        (MF_1F, 2, 5, 2, 2, 12, 11),
    ],
    "marks": [(8, 8, "Regidrago", "regi"), (8, 13, "exit", "warp")],
    "sources": [MF_B1F, MF_B1F2, MF_1F],
    "notes": "Wall + corner from Meteor Falls B1F 1R, gold columns and craters from 1F 1R, side walls / "
             "exit / bottom lip from B1F 2R; dais = B1F 1R west plateau with its ladder removed.",
}

CAVES = [REGOLIS, FRIGO, FERRUM, GAVANI, REGIDRAGO]


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for n, spec in enumerate(CAVES, 1):
        path = os.path.join(out_dir, "cave_%d_%s.png" % (n, spec["slug"]))
        compose.mockup(spec, path, 3)
        print(path, "%dx%d" % spec["size"], spec["title"])


if __name__ == "__main__":
    main(sys.argv[1])
