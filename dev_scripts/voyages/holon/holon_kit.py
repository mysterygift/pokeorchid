"""
Helpers for the Holon design-review mockups (batch 4). Only builds on voyage_compose (not edited).

  I(mid, ...)            ("id", mid[, coll, elev]) ref
  at(chunk, dx, dy)      (LAYOUT, sx, sy, w, h) + destination -> stamp tuple
  grid(w, h, ch)         mutable char grid; put()/rect()/to_rows()
  path9(mask, ch)        9-slice General dirt road for the `ch` cells -> spec['cells'] entries
  octagon_rings(...)     2x2-quantised round shapes (canal rings) on a char grid
  bridge_ew(...)         Route 119's wooden bridge (walk east-west over a north-south channel)
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
import voyage_compose as vc   # noqa: E402

G = "gTileset_General"
FORTREE = (G, "gTileset_Fortree")
RUSTBORO = (G, "gTileset_Rustboro")
R119 = "LAYOUT_ROUTE119@git"
R120 = "LAYOUT_ROUTE120@git"
R104 = "LAYOUT_ROUTE104"
LAVA_TOWN = "LAYOUT_LAVARIDGE_TOWN"      # Orchid's: new Centre / Mart / red-roof house, all General primary

# Orchid Centre / Mart / red-roof house (General primary -> pstamps in any pair)
CENTRE = (LAVA_TOWN, 8, 3, 5, 5)          # door at +2,+4
MART = (LAVA_TOWN, 14, 2, 4, 5)           # doors at +1,+4 and +2,+4
HOUSE = (LAVA_TOWN, 11, 12, 4, 4)         # door at +1,+3

DIRT = {"TL": 0x118, "T": 0x119, "TR": 0x11A, "L": 0x120, "C": 0x121, "R": 0x122, "BL": 0x128, "B": 0x129,
        "BR": 0x12A}
POND = [0x0A1, 0x0B0, 0x0B1, 0x0B2, 0x0B3, 0x0B8, 0x0B9, 0x0BA, 0x0BB, 0x0C0, 0x0C2, 0x0C3, 0x0C4, 0x002,
        0x001]
POND_TRAIN = [R120, "LAYOUT_ROUTE117@git", "LAYOUT_PETALBURG_CITY@git", "LAYOUT_SAFARI_ZONE_SOUTHWEST@git",
              "LAYOUT_ROUTE111@git", R104]
ROCK_VOCAB = sorted(vc.ROCK_IDS)
ROCK_TRAIN = ["LAYOUT_SOUTHERN_ISLAND_EXTERIOR", "LAYOUT_FARAWAY_ISLAND_ENTRANCE", R120]
SHORE = [0x170, 0x11B, 0x11C, 0x11D, 0x123, 0x125, 0x12B, 0x12C, 0x12D, 0x13D, 0x13E, 0x145, 0x146, 0x124]
SHORE_TRAIN = [R104, "LAYOUT_DEWFORD_TOWN@git", "LAYOUT_ROUTE105", "LAYOUT_ROUTE107"]


def I(mid, *ce):
    return ("id", mid) + ce


def at(chunk, dx, dy):
    return chunk + (dx, dy)


class Grid:
    def __init__(self, w, h, ch="."):
        self.w, self.h = w, h
        self.c = [[ch] * w for _ in range(h)]

    def get(self, x, y):
        return self.c[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def put(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = ch

    def rect(self, x, y, w, h, ch):
        for j in range(h):
            for i in range(w):
                self.put(x + i, y + j, ch)

    def rows(self):
        return ["".join(r) for r in self.c]


def path9(mask, ch, kit=DIRT, off_map_is_road=True):
    """9-slice dirt road for the `ch` cells (roads 2+ wide) -> [(x, y, ref)]."""
    h, w = len(mask), len(mask[0])
    p = lambda x, y: 0 <= x < w and 0 <= y < h and mask[y][x] == ch   # noqa: E731
    pe = lambda x, y: (off_map_is_road and not (0 <= x < w and 0 <= y < h)) or p(x, y)   # noqa: E731
    out = []
    for y in range(h):
        for x in range(w):
            if not p(x, y):
                continue
            n, s, wv, e = pe(x, y - 1), pe(x, y + 1), pe(x - 1, y), pe(x + 1, y)
            k = ("T" if not n else "B" if not s else "") + ("L" if not wv else "R" if not e else "")
            out.append((x, y, I(kit[k or "C"])))
    return out


def block_dist(bx, by, cx, cy, k=0.72):
    """Octagonal distance of a 2x2 block's centre from (cx, cy) in block units: straight sides with 45-degree
    corners, which the 2x2-squared pond edges draw cleanly (k = how far the corners are cut)."""
    dx, dy = abs(bx + 0.5 - cx), abs(by + 0.5 - cy)
    return max(dx, dy, (dx + dy) * k)


def thicken(g, cx, cy, ch, over="."):
    """Make a 1-block diagonal staircase of `ch` 4-connected: where two `ch` blocks touch only at a corner,
    the outer of their two shared neighbours (if it is `over`) becomes `ch` too."""
    B = lambda bx, by: g.c[by * 2][bx * 2] if 0 <= bx < g.w // 2 and 0 <= by < g.h // 2 else None  # noqa
    add = []
    for by in range(g.h // 2 - 1):
        for bx in range(g.w // 2 - 1):
            for (ax, ay), (bx2, by2), n1, n2 in (((bx, by), (bx + 1, by + 1), (bx + 1, by), (bx, by + 1)),
                                                 ((bx + 1, by), (bx, by + 1), (bx, by), (bx + 1, by + 1))):
                if B(ax, ay) == ch and B(bx2, by2) == ch and B(*n1) != ch and B(*n2) != ch:
                    out = max((n1, n2), key=lambda n: block_dist(n[0], n[1], cx, cy))
                    if B(*out) in over:
                        add.append(out)
    for bx, by in add:
        for j in (0, 1):
            for i in (0, 1):
                g.c[by * 2 + j][bx * 2 + i] = ch


def paint_ring(g, cx, cy, r0, r1, ch, only=None, k=0.72):
    """Paint 2x2 blocks whose centre lies at r0 <= d < r1 blocks from the block-grid point (cx, cy)."""
    for by in range(g.h // 2):
        for bx in range(g.w // 2):
            d = block_dist(bx, by, cx, cy, k)
            if r0 <= d < r1:
                for j in (0, 1):
                    for i in (0, 1):
                        if only is None or g.c[by * 2 + j][bx * 2 + i] in only:
                            g.c[by * 2 + j][bx * 2 + i] = ch


# Route 119's wooden bridge (walk east-west): grass end 2FE/306, first plank 216/21E, planks 210/218,
# last plank 217/21F (top row / bottom row)
BRIDGE_END = (0x2FE, 0x306)
BRIDGE_FIRST = (0x216, 0x21E)
BRIDGE_MID = (0x210, 0x218)
BRIDGE_LAST = (0x217, 0x21F)


def bridge_ew(x0, x1, y, ends=True):
    """Bridge rows y, y+1 over water cells x0..x1 (inclusive); grass ends at x0-1 and x1+1 -> spec post cells.
    Raw values come from Route 119 (same pair)."""
    out = []
    for x in range(x0, x1 + 1):
        piece = BRIDGE_FIRST if x == x0 else BRIDGE_LAST if x == x1 else BRIDGE_MID
        out += [(x, y, I(piece[0])), (x, y + 1, I(piece[1]))]
    if ends:
        for x in (x0 - 1, x1 + 1):
            out += [(x, y, I(BRIDGE_END[0])), (x, y + 1, I(BRIDGE_END[1]))]
    return out


def soil_rows(x, y, n, rows=1, gap=1):
    """Berry-soil crop rows as on Route 120: General soil lip 103/104/105 above, Fortree soil 29B/293/294/29C.
    Each row is 2 cells tall; `gap` grass rows between rows. -> post cells."""
    out = []
    for r in range(rows):
        yy = y + r * (2 + gap)
        for i in range(n):
            top = 0x103 if i == 0 else 0x105 if i == n - 1 else 0x104
            bot = 0x29B if i == 0 else 0x29C if i == n - 1 else (0x293 if i % 2 else 0x294)
            out += [(x + i, yy, I(top)), (x + i, yy + 1, I(bot))]
    return out


def fence_h(x, y, n):
    """General white fence row on grass: 0x148 left end, 0x149 middle, 0x14A right end (vanilla order;
    0x14B-0x14D next to them are the berry-soil strip, not fence)."""
    return [(x + i, y, I(0x148 if i == 0 else 0x14A if i == n - 1 else 0x149)) for i in range(n)]


def check_mask(rows, w, h):
    assert len(rows) == h, len(rows)
    for i, r in enumerate(rows):
        assert len(r) == w, (i, len(r))
    return rows
