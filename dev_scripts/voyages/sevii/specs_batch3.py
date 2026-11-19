"""
Sailor's Voyages, batch 3 (Sevii Islands 4-7): design-review mockup specs, not real maps. See voyage_compose.py
for the spec format. Every cell is copied from a layout with the same primary + secondary pair (or is a
metatile that exists in that pair). No tileset is edited.

STATUS (2026-11-19): the town / landmark / sea-route layouts are ON HOLD while the user decides whether the
Sevii mockups should be faithful translations of the FRLG maps (ref/frlg/, frlg_ref.py batch3) rather than
hand-composed. This file only holds the Icefall Cave ice-room look comparison:

  icefall_ice_coldstorage   Building + ColdStorage  (Orchid's Cold Storage kit: deck, ice, ice blocks, caps)
  icefall_ice_shoal         General + Cave          (Emerald's Shoal Cave ice room set 0x377-0x38F; the same
                                                     ring Orchid's Frigo Cave already uses)

Both are painted from ONE puzzle grid (ICE_GRID, 14x14 interior), checked by ice_puzzle.solve(): the goal is
reachable and, from every reachable cell, both the goal and the entry stay reachable. Ice stays the COVERED
bottom-layer metatile in both sets (0x38D / 0x204-0x207, 0x20C), so the Cold Storage reflection gotcha does
not apply to any cell placed here.
"""
import voyage_compose as vc

CS = ("gTileset_Building", "gTileset_ColdStorage")
CAVE = ("gTileset_General", "gTileset_Cave")
CS_TEST = "LAYOUT_COLD_STORAGE_TEST"


def I(mid, *ce):
    return ("id", mid) + ce


ALL = {}

# ================================================================================ ICEFALL CAVE: ICE ROOM
# One 14x14 interior, found by a random search (scratch) that maximised the shortest solution under the
# no-softlock check, then fixed here. Entry at the bottom (E, on the safe floor strip), goal = the way on
# to the back of the cave (G, ladder / hatch) in a small floor patch against the north-east wall.
#   ~ ice  . floor  o single non-slip spot  B boulder (Shoal) / ice block (Cold Storage)
ICE_GRID = [
    "~~~~~~~~~~B..G",   # 0
    "~~~~~~~~~~~...",   # 1
    "~~~~B~~~~~~...",   # 2
    "~~~~~~~~B~~~~B",   # 3
    "~~~~~~~~~~~~~~",   # 4
    "~~~~~~~~~~~~~~",   # 5
    "~~~~~~~~~~~~B~",   # 6
    "~~~~~Bo~~~~~~~",   # 7
    "~~~~~~~~~~~~~~",   # 8
    "~~~B~~~~~~~~~B",   # 9
    "~~~~~~~o~B~~~~",   # 10
    "~B~~~~~~~~BB~~",   # 11
    "..............",   # 12
    "......E.......",   # 13
]
IW, IH = len(ICE_GRID[0]), len(ICE_GRID)
assert all(len(r) == IW for r in ICE_GRID)


def _interior(ox, oy, paint):
    """[(x, y, ref)] for every interior cell, paint(ch, ix, iy) -> ref."""
    return [(ox + ix, oy + iy, paint(ch, ix, iy)) for iy, row in enumerate(ICE_GRID) for ix, ch in enumerate(row)]


def _route_stops(ox, oy):
    """Solution polyline (map cells) for the review overlay."""
    import ice_puzzle as ip
    r = ip.solve(ICE_GRID)
    pos = ip.find(ICE_GRID, "E")[0]
    pts = [pos]
    for d in r["route"]:
        pos = dict(ip.moves(ICE_GRID, pos))[d]
        pts.append(pos)
    return [(x + ox, y + oy) for x, y in pts]


# ---------------------------------------------------------------- (b) Shoal Cave look, General + Cave
# Ring exactly as Shoal Cave's ice room / Orchid's Frigo Cave: 2 rows of 0x389 wall top (0x37B / 0x37C
# corners), 2 columns 0x382 west and 0x380 east, a 0x379 lip row (0x383 ends) and 0x381 fill below.
# Interior at (2,2). Ice 0x38D; boulders alternate 0x37D / 0x37E; single stopper 0x28F; floor strip = 0x38F
# (ice to the north) over 0x385; NE patch = 0x38E (ice to the west) / 0x387 (ice to the south) / 0x385.
# Entry: 0x386 (MB_SOUTH_ARROW_WARP, the blue twin of the brown cave exit mat; exists in gTileset_Cave but
# no layout uses it) in the lip. Goal: Shoal's ladder pair 0x377 (in the wall) over 0x37F (MB_LADDER).
SW, SH = IW + 4, IH + 4                       # 18 x 18


def _shoal_cell(ch, ix, iy):
    if ch == "~":
        return I(0x38D)
    if ch == "B":                             # 0x37D / 0x37E picked by vanilla adjacency (spec "auto")
        return I(0x37E)
    if ch == "o":
        return I(0x28F)
    if ch == "G":
        return I(0x37F)
    if iy >= IH - 2:                          # entry strip
        return I(0x38F if iy == IH - 2 else 0x385)
    # NE patch (cols 11-13, rows 0-2), ladder at its north-east corner as in Shoal (17,10)
    if iy == 2:
        return I(0x387)
    return I(0x38E if ix == 11 else 0x385)


_shoal_ring = ([(0, 0, I(0x37B))] + [(x, 0, I(0x389)) for x in range(1, SW - 1)] + [(SW - 1, 0, I(0x37C))]
               + [(0, 1, I(0x382)), (1, 1, I(0x37B))] + [(x, 1, I(0x389)) for x in range(2, SW - 2)]
               + [(SW - 2, 1, I(0x37C)), (SW - 1, 1, I(0x380))]
               + [(x, y, I(0x382)) for y in range(2, SH - 2) for x in (0, 1)]
               + [(x, y, I(0x380)) for y in range(2, SH - 2) for x in (SW - 2, SW - 1)]
               + [(x, SH - 2, I(0x383)) for x in (0, 1, SW - 2, SW - 1)]
               + [(x, SH - 2, I(0x379)) for x in range(2, SW - 2)]
               + [(x, SH - 1, I(0x381)) for x in range(SW)])
_SE = (2 + 6, 2 + 13)                          # entry floor cell (map); warp mat right below it
_SG = (2 + 13, 2 + 0)

ICEFALL_ICE_SHOAL = dict(
    name="Icefall Cave ice room (b) Shoal Cave look", size=(SW, SH), tileset=CAVE,
    ground=I(0x381),
    cells=_shoal_ring + _interior(2, 2, _shoal_cell)
    + [(_SG[0], _SG[1] - 1, I(0x377)), (_SE[0], _SE[1] + 1, ("raw", 0x3000 | 0x386))],
    auto=[(2 + x, 2 + y, [0x37D, 0x37E]) for x, y in __import__("ice_puzzle").find(ICE_GRID, "B")],
    post=[(12, 2, I(0x37E)), (15, 5, I(0x37E))],   # under the wall / the patch edge: Shoal only has 0x37E there
    marks=[(_SE[0], _SE[1] + 1, "from entrance", "warp"), (_SG[0], _SG[1] - 1, "to back", "warp")],
    route=_route_stops(2, 2),
)
ALL["icefall_ice_shoal"] = ICEFALL_ICE_SHOAL

# ---------------------------------------------------------------- (a) Cold Storage look, Building + ColdStorage
# Cold Storage's room ring: Cap row on top, the two-row panel wall copied from ColdStorageTest (x7-20, rows
# 1-2: pipes, frost, vents, gauges), Cap_W / Cap_E columns, Cap_S row with the 2-wide Exit mat. Interior at
# (1,3), with the generator's shading rule (ShadeN under the wall; Ice_B speckle every few cells). Ice blocks
# = IceBlock_OnIce 0x280; stopper = Floor_Frost 0x20D; goal = Floor_Drain 0x211 as a hatch stand-in (the
# kit has no ladder / stairs).
CW, CH = IW + 2, IH + 4                       # 16 x 18


def _cs_cell(ch, ix, iy):
    top = iy == 0
    if ch == "~":
        if top:
            return I(0x205)                                    # Ice_ShadeN
        return I(0x20C if (ix * 7 + iy * 3) % 5 == 0 else 0x204)   # Ice_B / Ice (test_map.floor_label)
    if ch == "B":
        return I(0x280)
    if ch == "o":
        return I(0x20D)
    if ch == "G":
        return ("raw", 0x3000 | 0x211)          # Floor_Drain: in the kit, placed by no layout yet
    return I(0x201 if top else 0x200)                          # Floor_ShadeN / Floor


_CE = (1 + 6, 3 + 13)
_CG = (1 + 13, 3 + 0)
ICEFALL_ICE_COLDSTORAGE = dict(
    name="Icefall Cave ice room (a) Cold Storage look", size=(CW, CH), tileset=CS,
    ground=I(0x214),
    cells=([(0, 0, I(0x218))] + [(x, 0, I(0x214)) for x in range(1, CW - 1)] + [(CW - 1, 0, I(0x219))]
           + [(0, y, I(0x216)) for y in range(1, CH - 1)] + [(CW - 1, y, I(0x217)) for y in range(1, CH - 1)]
           + [(0, CH - 1, I(0x21A))] + [(x, CH - 1, I(0x215)) for x in range(1, CW - 1)]
           + [(CW - 1, CH - 1, I(0x21B))]
           + _interior(1, 3, _cs_cell)
           + [(_CE[0], CH - 1, I(0x212)), (_CE[0] + 1, CH - 1, I(0x212))]),
    stamps=[(CS_TEST, 7, 1, IW, 2, 1, 1)],     # wall run x7-20: no vent split at either cap
    marks=[(_CE[0], CH - 1, "from entrance", "warp"), (_CG[0], _CG[1], "hatch: to back", "warp")],
    route=_route_stops(1, 3),
)
# stamps run before cells in build(); the wall rows must win over nothing else, so order is fine.
ALL["icefall_ice_coldstorage"] = ICEFALL_ICE_COLDSTORAGE
