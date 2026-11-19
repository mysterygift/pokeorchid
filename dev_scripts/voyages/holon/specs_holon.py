"""
Holon (batch 4): design-review mockup specs (not real maps). Spec format: see voyage_compose.py.

Decided (user, 2026-11-19):
  * all Holon outdoor maps are General + gTileset_Fortree, built from Route 119 / Route 120 pieces (tropical
    1-wide trees, MB_LONG_GRASS patches, rivers, Route 120 bridges / ponds / rock spikes);
  * Holon Research Tower = the vanilla Weather Institute (Route 119 exterior; ROUTE119_WEATHER_INSTITUTE_1F/2F
    interiors, Building + Lab).
Every cell is copied from a General + Fortree layout (Route 119 / 120 / Fortree City, vanilla, from git) or,
for General-primary ids, from any layout with the General primary (same art in every pair).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402
from holon_kit import (I, at, Grid, path9, paint_ring, thicken, block_dist, bridge_ew, soil_rows, fence_h, FORTREE, R119, R120,  # noqa: E402,F401
                       CENTRE, MART, HOUSE, POND, POND_TRAIN, SHORE, SHORE_TRAIN, ROCK_VOCAB, ROCK_TRAIN)

# Route 119 / 120 tropical forest: 1-wide trees, solved per cell from vanilla neighbour frequency
FOREST = [0x0C6, 0x0C7, 0x016, 0x017, 0x00E, 0x00F]
LONG = 0x015          # MB_LONG_GRASS (hides the player; Route 119/120 encounter grass)
LONG_S = 0x208        # its south edge (MB_LONG_GRASS_SOUTH_EDGE, Fortree)
MOUND = (R120, 3, 50, 2, 2)      # Route 120's 2x2 rock mound (230 232 / 240 242)
TOMB = (R120, 5, 52, 5, 4)       # Route 120's Ancient Tomb dome (door 0A7 at +2,+3)
BRIDGE_PIECES = {"first": (0x216, 0x21E), "mid": (0x210, 0x218), "last": (0x217, 0x21F), "end": (0x2FE, 0x306)}
WI = (R119, 1, 24, 11, 10)       # Weather Institute: cliff face rows 24-25 + building 26-33, door at +5,+8

ALL = {}

# ------------------------------------------------------------------ extra overworld sprites for the marks
_P = "graphics/object_events/pics/"
for _k, _v in {
    "researcher": (_P + "people/scientist_1.png", 16, 32, 0, False),      # Holon Researcher stand-in (Scientist1)
    "researcher_up": (_P + "people/scientist_1.png", 16, 32, 1, False),
    "researcher_left": (_P + "people/scientist_1.png", 16, 32, 2, False),
    "researcher_right": (_P + "people/scientist_1.png", 16, 32, 2, True),
    "farmer": (_P + "people/man_4.png", 16, 32, 0, False),
    "farmer_left": (_P + "people/man_4.png", 16, 32, 2, False),
    "farmer_w": (_P + "people/woman_5.png", 16, 32, 0, False),
    "mentor": (_P + "people/expert_m.png", 16, 32, 0, False),
    "girl": (_P + "people/girl_2.png", 16, 32, 0, False),
    "nurse": (_P + "people/nurse.png", 16, 32, 0, False),
    "berry": (_P + "berry_trees/oran.png", 16, 32, 4, False),             # berry tree object, fruiting stage
    "apricorn": (_P + "misc/apricorn_tree.png", 16, 16, 0, False),
    "sphere": (_P + "misc/pushable_boulder.png", 16, 16, 0, False),      # stand-in for the stone sphere
}.items():
    vc.SPRITES.setdefault(_k, _v)


def _pal_sprite(key, pal_file):
    """Pre-load an overworld sprite with its in-game palette (the PNG's own palette can differ)."""
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
                op[x, y] = tuple(pal[px[x, y]][:3]) + (255,)
    vc._SPR[key] = out.transpose(Image.FLIP_LEFT_RIGHT) if flip else out


for _k, _pf in (("sphere", "npc_1.pal"), ("researcher", "npc_3.pal"), ("researcher_up", "npc_3.pal"),
                ("researcher_left", "npc_3.pal"), ("researcher_right", "npc_3.pal"), ("farmer", "npc_4.pal"),
                ("farmer_left", "npc_4.pal"), ("mentor", "npc_4.pal"), ("girl", "npc_3.pal"),
                ("farmer_w", "npc_2.pal")):
    _pal_sprite(_k, _pf)


def _cynthia(frame, flip=False):
    """Cynthia's overworld frames by lichen (ref sheet; credit in NOTES): bottom row, 9 frames of 16x32."""
    from PIL import Image
    im = Image.open(os.path.join(HERE, "_draft", "ref", "cynthia_sheet_by_lichen.png")).convert("RGBA")
    bg = im.getpixel((0, 95))
    fr = im.crop((frame * 16, 64, frame * 16 + 16, 96))
    px = fr.load()
    for y in range(32):
        for x in range(16):
            if px[x, y][:3] == bg[:3]:
                px[x, y] = (0, 0, 0, 0)
    return fr.transpose(Image.FLIP_LEFT_RIGHT) if flip else fr


vc.SPRITES.setdefault("cynthia", ("", 16, 32, 0, False))
vc.SPRITES.setdefault("cynthia_up", ("", 16, 32, 1, False))
vc._SPR["cynthia"] = _cynthia(0)
vc._SPR["cynthia_up"] = _cynthia(1)
vc.SPRITE_KINDS.update({"trainer", "cynthia"})
vc.MARK_COLOURS.update({"trainer": (255, 60, 60), "cynthia": (255, 90, 200)})


def long_grass(mask, ch="L"):
    """Long grass: 0x015, with the Fortree south-edge cell where the cell below is not long grass."""
    out = []
    h = len(mask)
    for y, row in enumerate(mask):
        for x, c in enumerate(row):
            if c == ch:
                below = mask[y + 1][x] if y + 1 < h else ch
                out.append((x, y, I(LONG_S if below != ch else LONG)))
    return out


# ================================================================================================ village
VW, VH = 72, 72
CX = CY = 18                       # centre in 2x2-block units = cell (36, 36)
R_ISLAND, R_IN, R_PATH0, R_PATH1, R_OUT0, R_OUT, R_AREA = 5.6, 7.0, 7.6, 8.6, 9.2, 10.6, 17.2
CANAL_X = (34, 37)                 # the straight canal (river) runs north-south, x34-37
WALK_Y = 38                        # grand walkway rows 38-39 (east-west)


def village_mask():
    g = Grid(VW, VH, "T")
    paint_ring(g, CX, CY, 0, R_AREA, ".", k=0.76)       # inside the tree ring
    paint_ring(g, CX, CY, R_ISLAND, R_IN, "w")          # inner canal
    paint_ring(g, CX, CY, R_PATH0, R_PATH1, "p")        # cobbled ring path between the canals
    thicken(g, CX, CY, "p")
    paint_ring(g, CX, CY, R_OUT0, R_OUT, "w")           # outer canal
    # the straight canal: river in from the north edge, out of the south edge (to Holon Lake); it joins
    # both rings but not the island, where the tower stands
    for y in range(VH):
        for x in range(CANAL_X[0], CANAL_X[1] + 1):
            if g.c[y][x] != "w" and not (24 <= y <= 47):
                g.c[y][x] = "w"
            elif 24 <= y <= 47 and g.c[y][x] == "p":
                g.c[y][x] = "w"
    # the island's north half is a wooded knoll; the tower stands against its rock face (as on Route 119)
    for y in range(VH):
        for x in range(VW):
            if g.c[y][x] == "." and y <= 29 and block_dist(x // 2, y // 2, CX, CY) < R_ISLAND:
                g.c[y][x] = "T"
    # grand walkway: west gate (from the Mirage Forest) to the island, and on to the east quarter
    for x in range(0, VW):
        for y in (WALK_Y, WALK_Y + 1):
            if g.c[y][x] in ".T":
                g.c[y][x] = "p"
    # south road to Holon Lake, along the river's west bank
    for y in range(52, VH):
        for x in (30, 31):
            if g.c[y][x] in ".T":
                g.c[y][x] = "p"
    return g


# buildings (top-left corners) and their doors
V_BUILD = {
    "Centre": (CENTRE, 4, 31), "Mart": (MART, 9, 31),
    "H1": (HOUSE, 22, 4), "H2": (HOUSE, 14, 12), "H3": (HOUSE, 42, 4), "H4": (HOUSE, 4, 22),
    "H5": (HOUSE, 62, 24), "H6": (HOUSE, 58, 52), "H7": (HOUSE, 20, 60), "Ruins": (HOUSE, 54, 12),
}
V_DOORS = {"Centre": [(2, 4)], "Mart": [(1, 4), (2, 4)]}
V_LONG = [(49, 9, 4, 12), (58, 10, 3, 9), (53, 17, 5, 3), (44, 18, 6, 3)]     # long grass round the ruins house
V_FIELDS = [   # (x, y, n, rows): berry-soil crop rows (lip + soil, 1 grass row between), fence above
    (21, 11, 8, 2), (44, 11, 4, 2), (58, 41, 8, 3), (4, 42, 8, 3),
]


def _village():
    g = village_mask()
    for x, y, w, h in V_LONG:
        for j in range(h):
            for i in range(w):
                if g.get(x + i, y + j) == ".":
                    g.put(x + i, y + j, "L")
    m = g.rows()
    rim = vc.ring_classes(m, land_chars=".pTLf", sea_chars="w")
    # trees, path and long grass keep their own art; only grass rim cells get the pond lip
    rim = ["".join((r if (o == "." or r not in "R") else o) for o, r in zip(om, rm)) for om, rm in zip(m, rim)]
    post, marks, pst = [], [], []
    for x, y, n, rows in V_FIELDS:
        post += fence_h(x, y - 2, n)
        post += soil_rows(x, y, n, rows)
    # bridges: walkway over the outer / inner canals (west and east), the ring path over the straight canal
    # (north and south), and a footbridge over the river in the north quarter
    for x0, x1, y in ((14, 17, WALK_Y), (22, 23, WALK_Y), (48, 49, WALK_Y), (54, 57, WALK_Y), (34, 37, 18),
                      (34, 37, 52)):
        post += bridge_ew(x0, x1, y, ends=False)
    post += bridge_ew(34, 37, 8)
    for name, (chunk, x, y) in V_BUILD.items():
        pst.append(at(chunk, x, y))
        for dx, dy in V_DOORS.get(name, [(1, 3)]):
            marks.append((x + dx, y + dy, name, "warp"))
    # boulders and a broken fence by the abandoned house; flowers on the island
    post += [(x, y, I(0x0E0)) for x, y in ((52, 13), (59, 17), (53, 10))]
    post += [(x, y, I(0x004)) for x, y in ((27, 42), (28, 42), (27, 43), (44, 42), (43, 43), (44, 43),
                                           (30, 46), (41, 46), (6, 37), (12, 37), (3, 30))]
    # the tower's rock face ends at x40: square it off with plain cliff cells, grass right of the roof
    post += [(40, 28, (R119, 9, 24)), (40, 29, (R119, 9, 25)), (40, 30, I(0x001))]
    post += [(3, 36, I(0x003)), (29, 66, I(0x003)), (16, 9, I(0x003))]          # signs
    marks += [
        (35, 36, "Research Tower", "warp"),
        (0, 36, "<- Mirage Forest", "conn"), (24, 70, "v Holon Lake", "conn"), (38, 0, "^ river (off-map)", "conn"),
        (3, 36, "", "sign"), (29, 66, "", "sign"), (16, 9, "", "sign"),
        (36, 39, "researcher", "npc", "researcher"),
        (25, 14, "farmer", "npc", "farmer_left"), (62, 44, "farmer", "npc", "farmer_w"),
        (9, 37, "lass", "npc", "girl"), (56, 16, "mentor", "npc", "mentor"),
        (46, 7, "farmer", "npc", "farmer"),
    ]
    # fruit trees (berry-tree objects) on the soil rows of two fields
    marks += [(x, 43, "", "field", "berry") for x in (5, 7, 9)] + [(x, 46, "", "field", "berry") for x in (6, 8, 10)]
    marks += [(x, 12, "", "field", "berry") for x in (22, 24, 26)]
    spec = dict(
        name="Holon Village", size=(VW, VH), tileset=FORTREE, ground=I(0x001),
        mask=rim,
        mask_legend={".": I(0x001), "w": I(0x0A1), "p": I(0x121), "T": I(0x0C7), "L": I(LONG)},
        mask_auto={"T": FOREST},
        edges=dict(chars="RW", water_chars="wW", vocab=POND, layouts=POND_TRAIN),
        pstamps=pst, stamps=[at(WI, 30, 28)], cells=path9(m, "p") + long_grass(m), post=post, marks=marks,
        drained=[(36.0, 36.0, 9.5, 17.0)],      # Power Spot: the Research Tower island, fading over the rings
    )
    return spec


ALL["holon_village"] = _village()


# ================================================================================================ coast
# Mirage Forest coast (arrival), west of the village: its east edge rows 26-27 meet the village walkway
# (village rows 38-39), connection offset +12. The Sailor's boat lands at a short wooden jetty on the south-west
# beach; a path winds through Route 119-style jungle to the village, past the ruins clearing (old railway
# stretch + standing stones), a long-grass meadow and a rocky clearing.
CW, CH = 44, 48
C_OFFSET = 12           # coast y + 12 = village y on the shared edge


def coast_mask():
    g = Grid(CW, CH, "T")
    for y in range(CH):
        sea = 7 + (1 if y % 9 in (3, 4, 5) else 0) - (1 if y % 11 in (7, 8) else 0)
        if y >= 40:
            sea = 34
        g.rect(0, y, sea, 1, "~")
        if y < 40:
            g.rect(sea, y, 2 if y < 18 else 3, 1, "s")
    g.rect(0, 40, 36, 1, "s")             # south beach
    g.rect(0, 41, 34, 1, "s")
    g.rect(0, 42, 34, 6, "~")
    g.rect(34, 41, 2, 7, "T")
    g.rect(9, 30, 14, 10, "s")            # landing beach (south-west)
    g.rect(7, 36, 4, 2, "s")
    # clearings
    g.rect(12, 3, 15, 11, ".")            # ruins clearing (railway + standing stones)
    g.rect(14, 2, 10, 1, ".")
    g.rect(26, 7, 15, 13, ".")            # meadow
    g.rect(24, 30, 15, 9, ".")            # rocky clearing
    g.rect(26, 29, 10, 1, ".")
    # long grass (wild Delta Pokemon)
    g.rect(28, 9, 11, 9, "L")
    g.rect(26, 33, 6, 5, "L")
    g.rect(13, 16, 4, 6, ".")
    g.rect(13, 17, 4, 4, "L")
    # path: beach -> north -> east edge (village); spurs into the clearings
    g.rect(18, 14, 2, 16, "p")
    g.rect(18, 26, CW - 18, 2, "p")
    g.rect(33, 20, 2, 6, "p")
    g.rect(30, 28, 2, 2, "p")
    return g


C_RAILS = [(x, 9) for x in range(13, 26)]          # old track (Orchid rail kit in gTileset_Holon), buffer at x13
C_CARVINGS = [(15, 5), (23, 5), (15, 12), (23, 12)]   # diamond-carved standing stones (gTileset_Holon), bottom cells


def _coast():
    g = coast_mask()
    m = g.rows()
    rim = vc.ring_classes(m, land_chars="s", sea_chars="~")
    post = []
    # wooden jetty from Route 119's bridge planks over calm water (0x170), landing on the sand at x8
    for x in range(3, 8):
        piece = BRIDGE_PIECES["first"] if x == 3 else BRIDGE_PIECES["mid"]
        post += [(x, 36, I(piece[0])), (x, 37, I(piece[1]))]
    # Route 120 rock spikes (0x232 over 0x072) and 2x2 rock mounds in the rocky clearing; boulders
    spikes = [(33, 31), (36, 32), (35, 36), (24, 31), (38, 35)]
    for x, y in spikes:
        post += [(x, y, (R120, 7, 42)), (x, y + 1, (R120, 7, 43))]
    stamps = [at(MOUND, 28, 30), at(MOUND, 32, 36)]
    # standing stones round the ruins: Route 120 mounds
    stamps += [at(MOUND, 13, 3), at(MOUND, 24, 3)]
    post += [(x, y, I(0x0E0)) for x, y in ((30, 38), (37, 30), (12, 12), (25, 11), (21, 4), (40, 19))]
    post += [(x, y, I(0x0E2)) for x, y in ((12, 32), (21, 38), (10, 39), (16, 36))]
    post += [(x, y, I(0x004)) for x, y in ((14, 8), (15, 8), (22, 7), (23, 7), (27, 18), (40, 9))]
    post += [(20, 34, I(0x003))]
    marks = [
        (3, 36, "Sailor", "sailor", "sailor_left"),
        (1, 36, "boat", "boat", "boat_right"),
        (43, 26, "-> Holon Village", "conn"),
        (20, 34, "", "sign"),
        (21, 9, "Researcher", "trainer", "researcher_left"),
        (34, 22, "Researcher", "trainer", "researcher_left"),
        (16, 31, "", "npc", "girl"),
    ]
    holon = [("rail_HW" if x == C_RAILS[0][0] else "rail_HE" if x == C_RAILS[-1][0] else "rail_H", x, y, False)
             for x, y in C_RAILS]
    for x, y in C_CARVINGS:
        holon += [("stone_top", x, y - 1, False), ("stone_bottom", x, y, True)]
    return dict(
        name="Mirage Forest coast", size=(CW, CH), tileset=FORTREE, ground=I(0x001),
        mask=rim,
        mask_legend={".": I(0x001), "~": I(0x170), "s": I(0x124), "p": I(0x121), "T": I(0x0C7), "L": I(LONG)},
        mask_auto={"T": FOREST},
        edges=dict(kind="shore", chars="RW", water_chars="~W", vocab=SHORE, layouts=SHORE_TRAIN),
        stamps=stamps, cells=path9(m, "p") + long_grass(m), post=post, marks=marks,
        holon=holon,
    )


ALL["holon_coast"] = _coast()


# ================================================================================================ lake
# Holon Lake, south of the village (village south edge -> lake north edge, offset 0, both 72 wide: the river
# x34-37 and the road x30-31 run straight on). A big forest lake: marsh on the west shore (Route 120's marsh),
# long grass on the north-east and south shores, a rock range on an east peninsula that breaks up into
# scattered spikes on islets to the west; in the west half three pillar islets in a triangle round the
# sphere islet, faced by Cynthia on the south peninsula. Two carved stone domes (Route 120's Ancient Tomb
# dome) stand in the woods by the shore.
LW, LH = 72, 52
L_WATER = [(14, 16, 30, 22), (18, 38, 40, 8), (52, 14, 10, 26), (20, 12, 12, 4), (34, 0, 4, 16),
           (10, 20, 4, 12)]
L_STRIP = (44, 4, 8, 38)              # land under the rock range (north shore -> mid-lake)
RIDGE_TOP = (R120, 14, 42, 4, 8)      # Route 120's ridge: jagged north end ...
RIDGE_BOT = (R120, 13, 64, 5, 24)     # ... and its stepped, narrowing south end (cliff base rows 86-87)
L_ISLAND = (19, 21, 12, 10)          # the pillar island: sphere in the middle, three pillars in a triangle
L_SPHERE = (24, 25)                    # sphere object; its 3x2 plinth is at x23-25, y25-26
L_PILLARS = {"pillar N": (24, 19), "pillar SW": (16, 33), "pillar SE": (33, 33)}   # base cells, in the water
L_SPIKE_ISLETS = [(42, 42, 2, 2), (48, 42, 2, 2), (52, 40, 2, 2)]
L_PENINSULA = (22, 34, 6, 12)         # Cynthia's shore platform (south)
L_TOMBS = [(5, 6), (59, 42)]
L_PUDDLES = [(4, 30), (7, 34), (3, 36), (8, 40)]       # west-shore marsh: General 2x2 puddles (Route 120)


RIDGE_IDS = {0x075, 0x23A, 0x06A, 0x072, 0x0D4, 0x232, 0x074, 0x07D, 0x242, 0x07C, 0x091, 0x089, 0x0A9, 0x07B,
             0x073, 0x071, 0x07A}


def ridge_cells(chunk, dx, dy):
    """Only the rock cells of a Route 120 ridge chunk (its trees / long grass / puddles left out -> grass)."""
    lid, sx, sy, w, h = chunk
    g = vc.raw_layout(lid)[1]
    out = []
    for j in range(h):
        for i in range(w):
            v = g[sy + j][sx + i]
            out.append((dx + i, dy + j, ("raw", v) if v & 0x3FF in RIDGE_IDS else I(0x001)))
    return out


def lake_mask():
    g = Grid(LW, LH, "T")
    g.rect(2, 4, 66, 44, ".")
    g.rect(0, 0, LW, 2, "T")
    for r in L_WATER:
        g.rect(*r, "w")
    g.rect(*L_ISLAND, ".")
    for r in L_SPIKE_ISLETS:
        g.rect(*r, ".")
    g.rect(*L_PENINSULA, ".")
    g.rect(*L_STRIP, ".")
    # forest bits back in, so the shore is wooded
    g.rect(2, 4, 4, 14, "T")
    g.rect(62, 4, 6, 14, "T")
    g.rect(2, 42, 14, 8, "T")
    g.rect(0, 48, LW, 4, "T")
    g.rect(64, 40, 8, 12, "T")
    # long grass
    g.rect(38, 4, 6, 8, "L")
    g.rect(52, 4, 10, 6, "L")
    g.rect(30, 46, 14, 2, "L")
    g.rect(62, 20, 4, 18, "L")
    g.rect(2, 28, 8, 12, "L")              # marsh: long grass round the puddles
    for x, y in L_PUDDLES:
        g.rect(x, y, 2, 2, ".")
    # road from the village (x30-31) down to the north shore, then west along it
    g.rect(30, 0, 2, 10, "p")
    g.rect(12, 8, 20, 2, "p")
    g.rect(12, 8, 2, 12, "p")
    return g


def _lake():
    g = lake_mask()
    m = g.rows()
    rim = vc.ring_classes(m, land_chars=".pTLM", sea_chars="w")
    rim = ["".join((r if (o == "." or r not in "R") else o) for o, r in zip(om, rm)) for om, rm in zip(m, rim)]
    post, stamps, marks = [], [], []
    # three carved pillars (gTileset_Holon, 1x3) standing in the lake in a triangle round the island, and the
    # sphere object on its plinth in the middle of the island
    holon = []
    for name, (x, y) in L_PILLARS.items():
        holon += [("pillar_top", x, y - 2, False), ("pillar_mid", x, y - 1, False), ("pillar_base", x, y, True)]
        marks.append((x, y, name, "spot"))
    for cy in range(2):
        for cx in range(3):
            holon.append(("plinth_%d%d" % (cx, cy), 23 + cx, 25 + cy, True))
    sx, sy = L_SPHERE
    marks.append((sx, sy, "sphere (object)", "field", "sphere_holon"))
    # the rock range: Route 120's ridge (jagged north end + stepped south end) running down the strip into the
    # lake, breaking up into scattered spikes (0x232 over 0x072) on the grass below it and on islets
    post += ridge_cells(RIDGE_TOP, 47, 8) + ridge_cells(RIDGE_BOT, 46, 16)
    for x, y in ((45, 41), (50, 41), (43, 43), (49, 43), (53, 41), (45, 12), (50, 14)):
        post += [(x, y - 1, (R120, 7, 42)), (x, y, (R120, 7, 43))]
    stamps += [at(MOUND, 44, 30), at(MOUND, 49, 6)]
    # marsh puddles (General 2x2 pond, as on Route 120)
    for x, y in L_PUDDLES:
        post += [(x, y, (R120, 3, 28)), (x + 1, y, (R120, 4, 28)), (x, y + 1, (R120, 3, 29)),
                 (x + 1, y + 1, (R120, 4, 29))]
    # bridge over the river where it enters the lake (the road's east branch)
    post += bridge_ew(34, 37, 8)
    for x, y in L_TOMBS:
        stamps.append(at(TOMB, x, y))
        holon += [("door_arch", x + 2, y + 2, True), ("door_slab", x + 2, y + 3, True)]     # sealed
        marks.append((x + 2, y + 3, "sealed dome", "spot"))
    post += [(x, y, I(0x0E0)) for x, y in ((44, 18), (51, 26), (12, 44), (66, 38))]
    post += [(x, y, I(0x004)) for x, y in ((26, 40), (23, 41), (16, 12), (17, 12), (8, 18), (21, 23), (22, 23),
                                           (27, 23), (28, 28), (20, 28), (21, 29), (28, 22))]
    post += [(28, 6, I(0x003))]
    marks += [
        (24, 35, "Cynthia", "cynthia", "cynthia_up"),
        (30, 0, "^ Holon Village", "conn"),
        (28, 6, "", "sign"),
        (8, 36, "Researcher", "trainer", "researcher_right"),
        (40, 13, "Researcher", "trainer", "researcher_left"),
        (16, 45, "", "npc", "mentor"),

    ]
    return dict(
        name="Holon Lake", size=(LW, LH), tileset=FORTREE, ground=I(0x001),
        mask=rim,
        mask_legend={".": I(0x001), "w": I(0x0A1), "p": I(0x121), "T": I(0x0C7), "L": I(LONG)},
        mask_auto={"T": FOREST},
        edges=dict(chars="RW", water_chars="wW", vocab=POND, layouts=POND_TRAIN),
        stamps=stamps, cells=path9(m, "p") + long_grass(m), post=post, marks=marks, holon=holon,
        drained=[(25.0, 26.0, 6.5, 12.0)],      # Power Spot: the pillar island and the near shores
    )


ALL["holon_lake"] = _lake()


# ================================================================================================ tower
# Holon Research Tower = the vanilla Weather Institute interior (Building + Lab, decided). 1F unchanged
# (lobby: the old weather desks become the researchers' reception); 2F gets "glowing round machinery" by
# swapping the middle desk pair for the Lab tileset's own machines: Birch's round Poke Ball machine (2x2,
# from Orchid's Tosa Port lab, same pair) and the orange specimen tank from 1F. Gen 3 cannot glow a metatile
# without palette animation; see NOTES q6.
WI1 = "LAYOUT_ROUTE119_WEATHER_INSTITUTE_1F"
WI2 = "LAYOUT_ROUTE119_WEATHER_INSTITUTE_2F"
LAB = "LAYOUT_TOSA_PORT_PROFESSOR_BIRCHS_LAB"
TOWER_2F = dict(
    name="Holon Research Tower 2F", size=(20, 11), tileset=("gTileset_Building", "gTileset_Lab"), base=WI2,
    fill=[(7, 7, 4, 3, (WI2, 6, 6)), (12, 7, 4, 3, (WI2, 6, 6))],
    stamps=[(LAB, 10, 6, 2, 2, 8, 7), (LAB, 10, 6, 2, 2, 13, 7), (WI1, 0, 2, 2, 2, 10, 4)],
    marks=[
        (17, 1, "stairs 1F", "warp"),
        (18, 6, "Researcher", "trainer", "researcher_left"),
        (11, 9, "Researcher", "trainer", "researcher_up"),
        (6, 6, "", "npc", "researcher_right"),
        (2, 6, "Head of research", "npc", "mentor"),
    ],
)
ALL["holon_tower_2f"] = TOWER_2F
AS_IS = {
    "holon_tower_1f": (WI1, [
        (9, 12, "exit", "warp"), (10, 12, "exit", "warp"), (17, 1, "stairs 2F", "warp"),
        (14, 2, "reception", "npc", "researcher"),
        (5, 4, "", "npc", "researcher_right"), (15, 5, "", "npc", "researcher_left"),
        (2, 11, "", "npc", "girl"),
    ]),
}


# ================================================================================================ ruins house
# Holon Ruins (abandoned) house interior: vanilla LAYOUT_HOUSE1 (Building + GenericBuilding, shared by the
# 14 GenericBuilding layouts) stripped bare with existing metatiles only: rug, table and plants taken out
# (bare boards 0x223, wall 0x20D); only the dusty cabinet, the bookshelf and the window are left. A lore
# item lies where the table was. (GenericBuilding's chairs and jars carry rug / green-floor backgrounds, so
# they can't stand on the bare boards without new cells.)
H1 = "LAYOUT_HOUSE1"
RUINS_INT = dict(
    name="Holon Ruins house", size=(10, 9), tileset=("gTileset_Building", "gTileset_GenericBuilding"), base=H1,
    fill=[(1, 3, 8, 4, (H1, 1, 7)), (8, 1, 2, 1, (H1, 4, 1)), (8, 2, 2, 1, (H1, 4, 2)),
          (8, 3, 2, 6, (H1, 8, 7))],
    marks=[(3, 8, "exit", "warp"), (4, 8, "exit", "warp"), (4, 5, "lore item", "item", "item")],
)
ALL["holon_ruins_house"] = RUINS_INT
