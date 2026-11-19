"""
gTileset_SeviiIslands art additions (design-review mockup only; nothing is written to data/).
register(st) is called once by sevii_tileset.py at import time, in this fixed order:

  1. cottage variants      Mr. Briney's cottage (Route 104 x15-19 y47-50) + 3 slight variants
  2. market stall          Two Island's rare-item stall, Emerald 3/4 canopy + counter
  3. Onix tails            FRLG Memorial Pillar rock mounds ported (General_Frlg metatiles, Emerald rock palette)
  4. Rocket Warehouse      Cold Storage exterior kit (gTileset_TosaPort 0x396+) cropped to FRLG's 6x5, recoloured

Every function records what it spent in COST[name] = dict(tiles, metatiles, palette) for budget.txt.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc            # noqa: E402
import sevii_art_kit as K              # noqa: E402
from sevii_art_kit import E            # noqa: E402

COST = {}
PORTED = {}            # (FRLG tileset name, FRLG metatile id) -> raw    (the translator substitutes these)
PORTED_CELLS = {}      # (FRLG map, x, y) -> raw   every cell of the ported formations, shared ids included
NOTES = {}


class _Spend:
    def __init__(self, st, name, palette=None):
        self.st, self.name, self.palette = st, name, palette

    def __enter__(self):
        self.t0, self.m0 = len(self.st._TILES), len(self.st._META)
        return self

    def __exit__(self, *a):
        COST[self.name] = dict(tiles=len(self.st._TILES) - self.t0, metatiles=len(self.st._META) - self.m0,
                               palette=self.palette)


def _attr(sc, mid):
    """-> (8 entries, layer, behaviour name) of an Emerald metatile."""
    ts, i = (sc.p, mid) if mid < 0x200 else (sc.s, mid - 0x200)
    a = ts.attrs[i]
    return list(ts.metatiles[i]), (a >> 12) & 3, _MB()[a & 0xFF]


_MBL = None


def _MB():
    global _MBL
    if _MBL is None:
        import sevii_tileset
        _MBL = sevii_tileset.MB
    return _MBL


# ================================================================================================ 1. cottage
COTTAGE_AT = ("LAYOUT_ROUTE104@git", 15, 47)          # 5x4, door at +2,+3
ROOF_TILES = {0x20B, 0x20C, 0x20D, 0x21B, 0x21C, 0x21D, 0x22B, 0x22C, 0x22D, 0x23B, 0x23C, 0x23D}
ROOF_PAL = 6
# palette 6 = Rustboro palette 9 with the thatch ramp (1-4) swapped for old, weathered (darker, browner) thatch.
# Tried and rejected at 4x: General pal 3's rock ramp (reads pink), orange cedar (too saturated), slate blue (nice,
# but would need a second palette slot). Roof tiles use only indices 1-4, 6, 7, so 5 and 8-15 of slot 6 are free
# for other art (the market stall uses them).
OLD_THATCH = [(200, 160, 112), (168, 128, 88), (144, 104, 72), (112, 80, 64)]

# flower box hung under the window band (top layer, General palette 2: greens, reds, browns)
FLOWER_BOX = [
    "..AA.....AA..2..",
    ".A99B.2.A99B.AA.",
    ".BBB3223.BB32A9B",
    "8555555555555558",
    "8777777777777778",
    "8766777777776678",
    "8666666666666668",
    ".88888888888888.",
] + ["................"] * 8


def _cottage(st):
    sc = vc.scene(K.GEN_RB)
    lay, x0, y0 = COTTAGE_AT
    g = vc.raw_layout(lay)[1]
    orig = [[g[y0 + j][x0 + i] for i in range(5)] for j in range(4)]
    st.STAMPS["cottage"] = dict(cells=orig, door=(2, 3), note="Mr. Briney's cottage, Route 104 x15-19 y47-50 "
                                "(vanilla metatiles, unchanged)")
    pal9 = sc.pals[9]
    st._PALS.setdefault(ROOF_PAL, [pal9[0]] + OLD_THATCH + list(pal9[5:]))

    def weathered(raw):
        ents, layer, mb = _attr(sc, raw & 0x3FF)
        ents = [(e & 0x0FFF) | (ROOF_PAL << 12) if ((e & 0x3FF) in ROOF_TILES and e >> 12 == 9) else e
                for e in ents]
        return K.meta(st, "Cottage_OldThatch_%03X" % (raw & 0x3FF), ents, mb, layer) | (raw & 0xFC00)

    box = K.grid(FLOWER_BOX, {"A": 10, "B": 11})
    box_ents = K.quad(box, 2, st)

    def boxed(raw):
        ents, layer, mb = _attr(sc, raw & 0x3FF)
        assert not any(e & 0x3FF for e in ents[4:]), "flower box needs an empty top layer"
        return K.meta(st, "Cottage_FlowerBox_%03X" % (raw & 0x3FF), ents[:4] + box_ents, mb, layer) \
            | (raw & 0xFC00)

    W = orig[3]
    lft, brooms, door, plain, rgt = W
    eave_l, eave_m, eave_door, eave_m2, eave_r = orig[2]
    # v1: weathered thatch roof, same front
    v1 = [[weathered(v) for v in r] for r in orig[:3]] + [list(W)]
    # v2: thatch roof, door one cell left, brooms beside it, flower box under the right window
    v2 = [list(orig[0]), list(orig[1]), [eave_l, eave_door, eave_m, eave_m2, eave_r],
          [lft, door, brooms, boxed(plain), rgt]]
    # v3: weathered roof, door one cell right, flower box under the left window, brooms in the middle
    c2 = [weathered(v) for v in (eave_l, eave_m, eave_door, eave_m2, eave_r)]
    v3 = [[weathered(v) for v in orig[0]], [weathered(v) for v in orig[1]], [c2[0], c2[1], c2[1], c2[2], c2[4]],
          [lft, boxed(plain), brooms, door, rgt]]
    st.STAMPS["cottage_v1"] = dict(cells=v1, door=(2, 3), note="weathered brown thatch (palette 6), front as original")
    st.STAMPS["cottage_v2"] = dict(cells=v2, door=(1, 3), note="thatch roof, door moved left, flower box at +3")
    st.STAMPS["cottage_v3"] = dict(cells=v3, door=(3, 3), note="weathered roof, door moved right, flower box at +1")


# ================================================================================================ 2. market stall
# FRLG Two Island: the yellow awning at x27-30 y1-3 (SeviiIslands123 2A8-2AA / 2B0-2B2 / 2B8 0C6 0C6 2BA), clerk
# (28,4) standing in front of it; crates / pots / flowers around it are separate FRLG decor (x25-26, x31-32).
# Emerald version, same 4-wide footprint, 4 rows (x27-30 y1-4):
#   y1  striped awning in 3/4 view: back edge, light top, sloping front, fold line, valance   (layer normal, solid)
#   y2  scalloped valance (rows 0-5), poles at both front corners                            (layer normal, solid)
#   y3  poles reach the ground; open ground between them = where the clerk stands             (normal; poles solid)
#   y4  wooden counter with the rare goods on top: top surface, lip, plank front band, stubby legs
#       (layer covered, MB_COUNTER, solid: the player talks to the clerk across it from y5)
# Clerk: move FRLG's (28,4) to (28,3). Its head starts 11 px down the sprite, below the valance (no clipping).
# Palette 6 (shared with the cottage roof, which only uses 1-4, 6, 7): wood = the weathered-thatch ramp 1-4.
STALL_FRLG = ("TwoIsland", 27, 1)
STALL_PAL = 6
STALL_COLOURS = {5: (248, 248, 248), 8: (40, 48, 88), 9: (232, 72, 64), 10: (96, 152, 224), 11: (248, 240, 192),
                 12: (248, 208, 72), 13: (224, 168, 48), 14: (176, 112, 48), 15: (80, 176, 88)}
_SL = {".": 0, "w": 5, "s": 6, "o": 7, "d": 8, "r": 9, "b": 10, "C": 11, "Y": 12, "D": 13, "A": 14, "g": 15,
       "1": 1, "2": 2, "3": 3, "4": 4}
# one 8-px stripe period, symmetric so the right end can be the left end mirrored
AWNING = [            # rows of y1 (16) + y2 rows 0-5; cream / yellow stripes, light from above
    "oooooooo",       # back edge
    "wwCCCCww",       # top surface, seen from above (lighter)
    "wwCCCCww",
    "CCYYYYCC",       # slope
    "CCYYYYCC",
    "CCYYYYCC",
    "CCYYYYCC",
    "CCYYYYCC",
    "CCDDDDCC",
    "CCDDDDCC",
    "AAAAAAAA",       # fold
    "CCYYYYCC",       # valance
    "CCYYYYCC",
    "CCYYYYCC",
    "CCDDDDCC",
    "CCDDDDCC",
    "CCDDDDCC",       # y2 row 0
    "oCDDDDCo",
    ".oDDDDo.",
    ".oAAAAo.",
    "..oooo..",
    "........",
]
POLE = ["o34o", "o34o", "o23o", "o34o"]      # repeats down; foot below
POLE_FOOT = ["o34o", "o34o", "o34o", "oooo"]
COUNTER = [           # y4, 16 rows; ends drawn separately
    "oooooooo",       # back edge of the top
    "11111111",
    "11111111",
    "22222222",       # lip
    "33333333",       # shadow under the lip
    "22222222",       # front band
    "22222222",
    "33333333",       # plank seam
    "22222222",
    "22222222",
    "44444444",
    "oooooooo",
]
GOODS = [             # (x, y from the top of y3, art): two clusters, so they share few tiles
    (8, 13, [".ooo.", "owrro", "orrro", "oowoo", "owwwo", ".ooo."]),          # Poke Ball
    (14, 12, [".44.", ".oo.", "owbo", "owbo", "obbo", "obbo", ".oo."]),      # potion
    (19, 15, [".ooo.", "oCYDo", "oYDAo", ".ooo."]),                          # nugget
    (40, 13, ["g.g.g", "ggggg", ".ggg.", "..o..", ".o4o.", ".ooo."]),        # herbs
    (46, 12, [".44.", ".oo.", "owro", "owro", "orro", "orro", ".oo."]),      # red potion
    (51, 13, [".ooo.", "owbbo", "orbro", "oowoo", "owwwo", ".ooo."]),        # Great Ball
]


def _stall_image():
    """64x64 top-layer art (palette 6 indices) for the 4x4 stall, transparent = ground."""
    img = [[0] * 64 for _ in range(64)]

    def put(x, y, rows):
        for j, r in enumerate(rows):
            for i, c in enumerate(r):
                if c != "." and 0 <= y + j < 64 and 0 <= x + i < 64:
                    img[y + j][x + i] = _SL[c]

    # poles: front corners, from under the valance to the ground at the bottom of y3
    for x in (1, 59):
        for y in range(16, 44):
            put(x, y, [POLE[(y - 16) % 4]])
        put(x, 44, POLE_FOOT)
    # awning across 64 px, then its outline
    for j, r in enumerate(AWNING):
        for x in range(64):
            c = r[x % 8]
            if c != ".":
                img[j][x] = _SL[c]
    for y in range(1, 18):
        img[y][0] = img[y][63] = 7
    img[0][0] = img[0][63] = 0
    # counter (y4 = rows 48-63): top, front band, outline ends, stubby legs
    for j, r in enumerate(COUNTER):
        for x in range(1, 63):
            img[48 + j][x] = _SL[r[x % 8]]
    for y in range(48, 60):
        img[y][0] = img[y][63] = 7
    img[48][0] = img[48][63] = 0
    for lx in (2, 58):
        put(lx, 60, ["o34o", "o34o", "oooo"])
    for x, y, art in GOODS:
        put(x, 32 + y, art)
        for i, c in enumerate(art[-1]):                         # small contact shadow on the counter top
            if c != "." and 32 + y + len(art) < 52 and img[32 + y + len(art)][x + i] == 1:
                img[32 + y + len(art)][x + i] = 2
    return img


def _stall(st):
    sc = vc.scene(K.GEN_RB)
    pal = st._PALS[STALL_PAL]
    for i, c in STALL_COLOURS.items():
        pal[i] = c
    img = _stall_image()
    grass = list(sc.p.metatiles[0x001][:4])
    cells = []
    for cy in range(4):
        row = []
        for cx in range(4):
            q = [r[cx * 16:cx * 16 + 16] for r in img[cy * 16:cy * 16 + 16]]
            top = K.quad(q, STALL_PAL, st)
            open_ground = cy == 2 and cx in (1, 2)
            if cy == 3:
                v = K.meta(st, "MarketStall_Counter_%d" % cx, grass + top, "MB_COUNTER", 1, coll=1, elev=3)
            else:
                v = K.meta(st, "MarketStall_%d_%d" % (cx, cy), grass + top, "MB_NORMAL", 0,
                           coll=0 if open_ground else 1, elev=3)
            row.append(v)
        cells.append(row)
    st.STAMPS["market_stall"] = dict(cells=cells, door=None, note="FRLG TwoIsland top-left (27,1), 4x4 (x27-30 "
                                     "y1-4); clerk (28,4) -> (28,3) behind the MB_COUNTER row; grass under it")


# ================================================================================================ 3. Onix tails
# FRLG Five Isle Memorial Pillar: the two free-standing rock mounds on the south beach (x1-4 y49-51, x11-15
# y51-53). They are NOT SeviiIslands45 art: every cell is a gTileset_General_Frlg (primary) mountain metatile, top
# layer = rock (FRLG primary palette 1), bottom = FRLG sand. Ported: the rock tiles are copied and their colours
# remapped by nearest colour onto Emerald's own rock palette (gTileset_General palette 3, the Hoenn cliff ramp:
# FRLG 9-14 -> 9-14 almost 1:1, FRLG outline 5 -> 8), bottom layer = Emerald sand (General 0x124's tiles).
ONIX_MAP = "FiveIsland_MemorialPillar"
ONIX_FORMATIONS = [(1, 49, 4, 3), (11, 51, 5, 3)]            # x, y, w, h in the FRLG map
ONIX_PAL = 3
FRLG_SAND = (0x020, 0x021)
EM_SAND = [E(0x108, 5), E(0x118, 5), E(0x118, 5), E(0x108, 5)]


def _onix(st):
    import frlg_translate as ft
    fm = ft.load_map(ONIX_MAP)
    fs = fm.scene
    em = vc.scene(K.GEN_RB)
    ported = {}

    def port_entry(e):
        t, pal = e & 0x3FF, e >> 12
        if t == 0:
            return E(0, 0)
        assert t < 640, "formation art is expected in the FRLG primary"
        tile = [[fs.p.px[(t % fs.p.w) * 8 + x, (t // fs.p.w) * 8 + y] & 15 for x in range(8)] for y in range(8)]
        m = K.nearest_map(fs.pals[pal], em.pals[ONIX_PAL], allowed=range(1, 15))
        tile = K.remap(tile, m)
        e2 = K.ent(tile, ONIX_PAL, st)
        return e2 ^ ((e & 0xC00) if (e2 & 0x3FF) else 0)     # keep FRLG's flips on top of any re-use flip

    for fx, fy, w, h in ONIX_FORMATIONS:
        for y in range(fy, fy + h):
            for x in range(fx, fx + w):
                mid = fm.mid(x, y)
                a = fs.attr(mid)
                layer = (a >> 29) & 3
                ents = list(fs.p.meta[mid])
                if not any(t & 0x3FF for t in ents[4:]) and all((b & 0x3FF) in FRLG_SAND for b in ents[:4]):
                    PORTED_CELLS[(ONIX_MAP, x, y)] = vc.ref_value(("id", 0x124), K.GEN_RB)   # plain sand
                    continue
                if mid not in ported:
                    bottom = ents[:4]
                    if all((b & 0x3FF) in FRLG_SAND or (b & 0x3FF) == 0x013 for b in bottom):
                        bottom = EM_SAND                         # sand (or FRLG grass under opaque rock)
                    else:
                        bottom = [port_entry(b) for b in bottom]
                    top = [port_entry(t) for t in ents[4:]]
                    ported[mid] = K.meta(st, "OnixTail_%03X" % mid, bottom + top, "MB_NORMAL", layer) & 0x3FF
                raw = fm.raw[y][x]
                PORTED_CELLS[(ONIX_MAP, x, y)] = ported[mid] | (raw & 0xFC00)
    for mid, v in ported.items():
        PORTED[("General_Frlg", mid)] = v | (1 << 10)            # solid, elevation 0 (as the FRLG cells)
    rows = []
    for fx, fy, w, h in ONIX_FORMATIONS:
        rows.append([[PORTED_CELLS[(ONIX_MAP, x, y)] for x in range(fx, fx + w)] for y in range(fy, fy + h)])
    st.STAMPS["onix_tail_w"] = dict(cells=rows[0], door=None, note="FRLG Memorial Pillar x1-4 y49-51, on sand")
    st.STAMPS["onix_tail_e"] = dict(cells=rows[1], door=None, note="FRLG Memorial Pillar x11-15 y51-53, on sand")
    NOTES["Onix tails"] = ("ported FRLG ids (General_Frlg primary): " + " ".join("%03X" % m for m in sorted(ported))
                           + "\nthe ids shared with every FRLG cliff (071 079 0A0 0A8) are in PORTED too: substitute "
                           "by PORTED_CELLS (per cell) unless a map really wants the FRLG rock texture everywhere")


# ================================================================================================ 4. Rocket Warehouse
# Orchid's Cold Storage exterior (gTileset_TosaPort / gTileset_Slateport metatiles 0x396-0x3AA, palette 12,
# generated by dev_scripts/cold_storage_tileset/export_exterior.py) cropped to FRLG Five Isle Meadow's 6x5
# warehouse (x9-14 y17-21, door warp (12,21) = +3,+4): no shutter / roof unit / skylight / snowflake sign (FRLG has
# just the door). Same tiles, new palette 12; the snowflake on the door is replaced by a red Team Rocket "R".
CS_TS = ("gTileset_General", "gTileset_TosaPort")
CS = {"Roof_TL": 0x396, "Roof_T": 0x397, "Roof_TR": 0x398, "Roof_ML": 0x399, "Roof_M": 0x39A, "Roof_MR": 0x39B,
      "Roof_BL": 0x39C, "Roof_B": 0x39D, "Roof_BR": 0x39E, "Wall_TL": 0x39F, "Wall_T": 0x3A0, "Wall_TR": 0x3A1,
      "Wall_BL": 0x3A2, "Wall_B": 0x3A3, "Wall_BR": 0x3A4, "Door_Top": 0x3A9, "Door": 0x3AA}
ROCKET_LAYOUT = [["Roof_TL", "Roof_T", "Roof_T", "Roof_T", "Roof_T", "Roof_TR"],
                 ["Roof_ML", "Roof_M", "Roof_M", "Roof_M", "Roof_M", "Roof_MR"],
                 ["Roof_BL", "Roof_B", "Roof_B", "Roof_B", "Roof_B", "Roof_BR"],
                 ["Wall_TL", "Wall_T", "Wall_T", "Door_Top", "Wall_T", "Wall_TR"],
                 ["Wall_BL", "Wall_B", "Wall_B", "Door", "Wall_B", "Wall_BR"]]
ROCKET_DOOR = (3, 4)
ROCKET_PAL = 12
# Cold Storage palette 12 index roles: 1 outline, 2 dark, 3-6 roof (dark -> light), 7-10 wall greys (mid -> white),
# 11 slate, 12/13 hazard orange/yellow (shutter only: free here), 14 snowflake teal.
# Door: its glass (index 9, shared with the wall stripes) is moved to 13 so the door can stay light on any wall;
# 14 = Rocket red, 12 = its dark edge.
_ROOF_RUST = [(144, 80, 32), (168, 96, 48), (192, 112, 72), (224, 152, 104)]          # = FRLG's warehouse roof
ROCKET_PALETTES = {
    # registered: FRLG's rusty corrugated roof over dark-steel walls, red R
    "rust_steel": _ROOF_RUST + [(112, 120, 136), (144, 152, 168), (168, 176, 192), (208, 216, 224), (80, 88, 112)],
    # FRLG-faithful: rust roof, khaki walls
    "frlg": _ROOF_RUST + [(120, 120, 128), (152, 144, 104), (176, 168, 120), (200, 192, 144), (88, 88, 112)],
    # all steel: grey roof and walls
    "steel": [(72, 80, 96), (96, 104, 120), (128, 136, 152), (168, 176, 192),
              (104, 112, 128), (136, 144, 160), (160, 168, 184), (200, 208, 216), (72, 80, 104)],
}
ROCKET_CHOICE = "rust_steel"


def rocket_palette(choice=ROCKET_CHOICE):
    v = ROCKET_PALETTES[choice]
    return ([(0, 0, 0), (64, 72, 104), (40, 48, 88)] + v + [(152, 32, 40), (216, 224, 232), (232, 56, 48),
                                                             (0, 0, 0)])


# 6x7 Rocket "R" (Gen 3 style: 2-px stem, red with a dark right edge, counters plain glass), drawn over the door where the
# snowflake was (door rows 11-17 = Door_Top rows 11-15 + Door rows 0-1), x 5-10.
R_GLYPH = [
    "RRRRR.",
    "RR..Rd",
    "RR..Rd",
    "RRRRd.",
    "RR.Rd.",
    "RR..Rd",
    "RR..Rd",
]
R_AT = (5, 11)


def _rocket_door_images(sc):
    door = [K.entry_tile(sc, e) for e in sc.s.metatiles[CS["Door_Top"] - 0x200][:4] +
            sc.s.metatiles[CS["Door"] - 0x200][:4]]
    img = K.join16(door[:4]) + K.join16(door[4:])               # 16x32
    for y in range(32):
        for x in range(16):
            if img[y][x] == 14:                                 # snowflake out: glass / the leaves' divider back
                img[y][x] = 11 if x == 7 else 10 if x == 8 else 9
    for y in range(8, 32):                                      # door glass -> 13 (lintel rows 0-7 are wall)
        for x in range(1, 15):
            if img[y][x] == 9 and y < 27:
                img[y][x] = 13
    for j, r in enumerate(R_GLYPH):
        for i, c in enumerate(r):
            if c == "R":
                img[R_AT[1] + j][R_AT[0] + i] = 14
            elif c == "d":
                img[R_AT[1] + j][R_AT[0] + i] = 12
            else:                                               # counters: plain glass, no leaf divider
                img[R_AT[1] + j][R_AT[0] + i] = 13
    return img[:16], img[16:]


def _rocket(st):
    sc = vc.scene(CS_TS)
    st._PALS.setdefault(ROCKET_PAL, rocket_palette())
    top, bot = _rocket_door_images(sc)
    ids = {}
    for name, mid in CS.items():
        ents, layer, mb = _attr(sc, mid)
        if name == "Door_Top":
            new = K.quad(top, ROCKET_PAL, st)
        elif name == "Door":
            new = K.quad(bot, ROCKET_PAL, st)
        else:
            new = [K.ent(K.entry_tile(sc, e), ROCKET_PAL, st) if e & 0x3FF else E(0, 0) for e in ents[:4]]
        ids[name] = K.meta(st, "RocketWarehouse_" + name, new + [E(0, 0)] * 4, mb, layer)
    cells = [[ids[n] | (0x3000 if n == "Door" else 0x0400) for n in r] for r in ROCKET_LAYOUT]
    st.STAMPS["rocket_warehouse"] = dict(cells=cells, door=ROCKET_DOOR, note="FRLG Five Isle Meadow x9-14 y17-21, door "
                                         "(12,21) -> MAP_FIVE_ISLAND_ROCKET_WAREHOUSE; door metatile is "
                                         "MB_ANIMATED_DOOR: needs its own field_door.c entry (copy of the Cold "
                                         "Storage one, palette 12, frames with the R)")
    NOTES["Rocket Warehouse"] = (
        "palette 12 = rocket_palette('%s'); alternatives in ROCKET_PALETTES (same tiles): %s.\n"
        "door = MB_ANIMATED_DOOR copied from METATILE_Slateport_ColdStorage_Door: src/field_door.c needs a new "
        "sDoorAnimGraphicsTable entry for the Sevii door metatile (tiles = a 3-frame anim like "
        "graphics/door_anims/cold_storage.png but with the R and the moved glass index, palettes {12 x8})."
        % (ROCKET_CHOICE, ", ".join(ROCKET_PALETTES)))


# ================================================================================================ 5. FRLG ports (3b)
# Generic cell porter for the Sevii landmarks: every FRLG entry is copied tile by tile; its colours go to an Emerald
# palette by FRLG palette (PORT_PALS), FRLG ground under the art (grass / sand / sea / pond) becomes Emerald's own
# ground tiles, layer + behaviour + collision + elevation are kept. Identical results share one metatile.
FRLG_P5_SLOT = 7          # FRLG primary palette 5 copied verbatim (Tanoby bricks, pale plaza sand, plateau top)
# FRLG palette -> (Emerald slot, remap)  ("verbatim": same indices in FRLG_P5_SLOT)
# FRLG pal 0 (only Ruin Valley's pale path is ported from it: its 3 colours) -> slot 7, whose indices 12/13 are unused
# by the pal-5 art and become the path's two mints; FRLG's grass green 13 -> slot 7's 15 (= Emerald grass)
PATH_MINTS = {12: (136, 216, 184), 13: (160, 224, 192)}
PORT_PALS = {0: (FRLG_P5_SLOT, {8: 12, 12: 13, 13: 15}),
             1: (3, "nearest"),        # FRLG rock                      -> General pal 3 (Hoenn rock ramp)
             2: (5, "nearest"),        # FRLG blue-greys (Memorial Pillar) -> General pal 5 greys
             5: (FRLG_P5_SLOT, "verbatim"),
             10: (5, "nearest"),       # Ruin Valley stone posts (greys)
             11: (5, "nearest")}       # Memorial Pillar boulder (greys)
FRLG_GRASS = {0x013, 0x24C, 0x24D, 0x25C, 0x25D, 0x24E, 0x24F, 0x25E, 0x25F, 0x26E, 0x26F}
EM_GRASS = [E(0x002, 2), E(0x003, 2), E(0x003, 2), E(0x002, 2)]
EM_SEA = [E(0x1C6, 4), E(0x1C7, 4), E(0x1C7, 4), E(0x1C6, 4)]
EM_POND = [E(0x11E, 1)] * 4
_PORT_CACHE = {}


def _frlg_tile(fs, t):
    ts, i = (fs.p, t) if t < 640 else (fs.s, t - 640)
    return [[ts.px[(i % ts.w) * 8 + x, (i // ts.w) * 8 + y] & 15 for x in range(8)] for y in range(8)]


def _port_entry(st, fs, e, q, bottom):
    t, pal, fl = e & 0x3FF, e >> 12, e & 0xC00
    if t == 0:
        return E(0, 0)
    if bottom and pal == 0 and t in FRLG_GRASS:
        return EM_GRASS[q]
    if bottom and pal == 5 and t in FRLG_SAND:
        return EM_SAND[q]
    if bottom and pal == 4:
        return EM_SEA[q]
    if bottom and pal == 3:
        return EM_POND[q]
    slot, how = PORT_PALS[pal]
    tile = _frlg_tile(fs, t)
    if isinstance(how, dict):
        tile = K.remap(tile, {0: 0, **how})
    elif how != "verbatim":
        m = K.nearest_map(fs.pals[pal], vc.scene(K.GEN_RB).pals[slot], allowed=range(1, 15))
        tile = K.remap(tile, m)
    e2 = K.ent(tile, slot, st)
    return e2 ^ (fl if e2 & 0x3FF else 0)


def port_cell(st, fm, x, y):
    """Emerald raw value for FRLG map fm's cell (x, y), porting its metatile on first use."""
    fs, mid = fm.scene, fm.mid(x, y)
    key = fs.key(mid)
    if key not in _PORT_CACHE:
        ts, i = fs._ts(mid)
        ents, a = ts.meta[i], fs.attr(mid)
        new = [_port_entry(st, fs, e, k & 3, k < 4) for k, e in enumerate(ents)]
        mb = _frlg_mb(a)
        _PORT_CACHE[key] = K.meta(st, "Port_%s_%03X" % (key[0], mid), new, mb, (a >> 29) & 3) & 0x3FF
    return _PORT_CACHE[key] | (fm.raw[y][x] & 0xFC00)


def _frlg_mb(a):
    import frlg_translate as ft
    name = ft.MB[a & 0x1FF] if (a & 0x1FF) < len(ft.MB) else "MB_NORMAL"
    return name if name in _MB() and name not in ("MB_OCEAN_WATER", "MB_POND_WATER", "MB_SHALLOW_WATER") \
        else "MB_NORMAL"


def _port_cells(st, name, cells, ids=None):
    import frlg_translate as ft
    fm = ft.load_map(name)
    done = []
    for x, y in cells:
        if ids is None or fm.mid(x, y) in ids:
            PORTED_CELLS[(name, x, y)] = port_cell(st, fm, x, y)
            done.append((x, y))
    return fm, done


def _p5_palette(st):
    import frlg_translate as ft
    pal = list(ft.load_map("SevenIsland_TanobyRuins").scene.pals[5])
    pal[0] = (0, 0, 0)
    pal[15] = vc.scene(K.GEN_RB).pals[2][13]              # FRLG grass green -> Emerald's (112, 192, 160)
    for i, c in PATH_MINTS.items():
        pal[i] = c
    st._PALS.setdefault(FRLG_P5_SLOT, pal)


MEMORIAL_IDS = {0x2C0, 0x2C1, 0x2C8, 0x2C9, 0x2D0, 0x2D1, 0x2D8, 0x2D9, 0x2C2, 0x2CA,     # pillar + plaza sides
                0x0D0, 0x0D2, 0x0D8, 0x0DA, 0x0E0, 0x0E1, 0x0E2, 0x30A}                 # plaza edges, its boulder
TANOBY_WARPS = [(120, 10), (103, 10), (88, 8), (44, 11), (32, 9), (12, 15), (11, 6)]
TANOBY_IDS = ({0x2C8, 0x2C9, 0x2CA, 0x2D0, 0x2D1, 0x2D2, 0x2D8, 0x2D9, 0x2DA, 0x2E0, 0x2E1, 0x2E2,   # facade
               0x33C, 0x33D, 0x33E} |                                                         # chamber-1 base
              {0x098, 0x099, 0x09A, 0x0A0, 0x0A2, 0x0A8, 0x0AA, 0x0AF, 0x214, 0x215, 0x216} |  # mound, boulders
              {0x080, 0x081, 0x082, 0x088, 0x08A, 0x090, 0x092, 0x207, 0x349})              # chamber 1 plateau
RUIN_VALLEY_BOX = (22, 20, 5, 5)          # mound + posts + door (warp 24,24); pale path = every 0C4-0CF cell


def _memorial(st):
    fm, done = _port_cells(st, "FiveIsland_MemorialPillar",
                           [(x, y) for y in range(39, 46) for x in range(5, 12)], MEMORIAL_IDS)
    NOTES["Memorial Pillar"] = "PORTED_CELLS FiveIsland_MemorialPillar: " + " ".join("%d,%d" % c for c in done)


def _tanoby(st):
    cells = sorted({(x, y) for wx, wy in TANOBY_WARPS for y in range(wy - 6, wy + 2) for x in range(wx - 4, wx + 5)})
    fm, done = _port_cells(st, "SevenIsland_TanobyRuins", cells, TANOBY_IDS)
    for mid in sorted(TANOBY_IDS):
        if mid >= 0x2C8 and mid < 0x340:
            PORTED[("SeviiIslands67", mid)] = _PORT_CACHE[fm.scene.key(mid)] | (1 << 10 if mid != 0x2E1 and
                                                                                  mid != 0x33D else 0)
    NOTES["Tanoby Ruins"] = "PORTED_CELLS SevenIsland_TanobyRuins: %d cells around the 7 chamber warps" % len(done)


def _ruin_valley(st):
    import frlg_translate as ft
    fm = ft.load_map("SixIsland_RuinValley")
    x0, y0, w, h = RUIN_VALLEY_BOX
    box = [(x, y) for y in range(y0, y0 + h + 1) for x in range(x0, x0 + w)]
    path = [(x, y) for y in range(fm.h) for x in range(fm.w) if 0x0C4 <= fm.mid(x, y) <= 0x0CF]
    _, done = _port_cells(st, "SixIsland_RuinValley", sorted(set(box) | set(path)))
    NOTES["Ruin Valley"] = "PORTED_CELLS SixIsland_RuinValley: %d cells (mound x22-26 y20-25 + pale path)" % len(done)


KEEP_LAYOUTS = ("LAYOUT_ROUTE104@git", "LAYOUT_SOUTHERN_ISLAND_EXTERIOR@git", "LAYOUT_FARAWAY_ISLAND_ENTRANCE@git")
# Rustboro's tile animations write here every few frames (src/tileset_anims.c): windy water -> secondary tiles
# 128-159, fountain -> 448-451. Never put art there while the Sevii copy keeps Rustboro's anim callback.
ANIM_TILES = set(range(128, 160)) | set(range(448, 452))


def free_policy(st):
    """Sets st.FREE_TILES / st.DROPPED_METATILES (replaces the Rustboro-City-only rule of _free_tiles)."""
    sc = vc.scene(K.GEN_RB)
    keep = set()
    for lay in KEEP_LAYOUTS:
        keep |= {v & 0x3FF for r in vc.raw_layout(lay)[1] for v in r if v & 0x3FF >= 0x200}
    kept_tiles = {e & 0x3FF for m in keep for e in sc.s.metatiles[m - 0x200] if e & 0x3FF >= 512}
    st.DROPPED_METATILES = [0x200 + i for i in range(len(sc.s.metatiles)) if 0x200 + i not in keep]
    st.FREE_TILES = [i for i in range(1, 512) if 512 + i not in kept_tiles and i not in ANIM_TILES]
    NOTES["free policy"] = ("kept: every Rustboro metatile of %s (%d metatiles, %d tiles); free: %d tile slots "
                            "(tile 0 and the anim destinations 128-159, 448-451 excluded)"
                            % (", ".join(KEEP_LAYOUTS), len(keep), len(kept_tiles), len(st.FREE_TILES)))


def check_kept(st):
    """Every Rustboro secondary cell the Sevii specs draw must keep its metatile and tiles."""
    st._ensure_free()
    sc = vc.scene(K.GEN_RB)
    free, dropped = set(st.FREE_TILES), set(st.DROPPED_METATILES)
    used = [("LAYOUT_ROUTE104@git", 11, 51, 4, 3), ("LAYOUT_ROUTE104@git", 15, 47, 5, 4),
            ("LAYOUT_ROUTE104@git", 3, 15, 7, 4), ("LAYOUT_SOUTHERN_ISLAND_EXTERIOR", 10, 21, 9, 4)]
    bad, n = [], 0
    for lay, x0, y0, w, h in used:
        g = vc.raw_layout(lay)[1]
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                mid = g[y][x] & 0x3FF
                if mid < 0x200:
                    continue
                n += 1
                tiles = {e & 0x3FF for e in sc.s.metatiles[mid - 0x200] if e & 0x3FF >= 512}
                if mid in dropped or any(t - 512 in free for t in tiles):
                    bad.append((lay, x, y, hex(mid)))
    assert not bad, "Sevii spec cells lost art: %s" % bad
    return n


# User 2026-11-19: don't re-port the Tanoby facade -- Tiksi's gTileset_TanobyDelta (port_tanoby.py) already has it;
# Tanoby Ruins is built on General + TanobyDelta instead (frlg_translate PAIRS["tanoby"]). Kept for the record.
PORT_TANOBY = False


def register(st):
    with _Spend(st, "cottage variants", palette="6 (new: Rustboro pal 9 + weathered-thatch ramp)"):
        _cottage(st)
    with _Spend(st, "market stall", palette="6 (shared with the cottage roof: indices 5, 8-15)"):
        _stall(st)
    with _Spend(st, "Onix tails (port)", palette="3 (General, Emerald rock ramp; no new palette)"):
        _onix(st)
    with _Spend(st, "Rocket Warehouse", palette="12 (new: Cold Storage palette recoloured)"):
        _rocket(st)
    NOTES["kept cells"] = "verified: %d Rustboro secondary cells the Sevii specs use keep their metatiles + tiles" \
        % check_kept(st)
    _p5_palette(st)
    with _Spend(st, "Memorial Pillar (port)", palette="5 (General greys), 7 (new: FRLG primary pal 5 verbatim)"):
        _memorial(st)
    if PORT_TANOBY:
        with _Spend(st, "Tanoby chambers (port)", palette="7 (FRLG pal 5), 3 (rock), 4/5 (Emerald sea/sand)"):
            _tanoby(st)
    with _Spend(st, "Ruin Valley Dotted Hole (port)", palette="3 (rock), 5 (posts), 7 (pale path: mints 12-13), 1 (pond, Emerald)"):
        _ruin_valley(st)
