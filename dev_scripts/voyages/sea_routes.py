"""
Invented Surf routes between Sevii islands (user decision 2026-11-19: keep sea routes between the islands of
a cluster, short; walled on both long sides by sea rocks so the player can't Surf out of the corridor).

A route = open sea + a corridor (union of even-aligned rectangles) whose ring (2 cells thick) is filled with
Route 104's 2x2 sea rocks (General primary, impassable), so the only way on is along the corridor. The
corridor touches the map edge exactly where a neighbour connects; walls run to the edge either side of each
opening, so crossing the edge anywhere else is blocked by rock (or by the map edge where nothing connects).
Optional grassy islets (v1 style: rock rim, 2x2 trees) sit inside wide corridor stretches.

route_spec(name, size, corridor, islets, conns, marks) -> voyage_compose spec on the Sevii pair.
check(spec, grid, neighbours) -> list of problems: every corridor opening cell must be passable sea in the
route AND in the neighbour's rendered grid across the edge; every non-opening edge cell of the route must be
blocked (rock) or have no neighbour.
"""
import voyage_compose as vc
import specs_batch2_v1 as v1

SEVII = ("gTileset_General", "gTileset_SeviiIslands")
ROCKS = [("LAYOUT_ROUTE104@git", 7, 48, 2, 2), ("LAYOUT_ROUTE104@git", 5, 52, 2, 2)]   # small / big


def _cells(rects):
    out = set()
    for x, y, w, h in rects:
        out.update((x + i, y + j) for i in range(w) for j in range(h))
    return out


def route_spec(name, size, corridor, islets=(), conns=(), marks=()):
    """corridor / islets: [(x, y, w, h)] (even x, y, w, h for the corridor). conns: [(direction, offset, map,
    (a, b))] where (a, b) is the opening along that edge (route coordinates), used for labels / checks."""
    W, H = size
    vc.check_size(W, H)
    sea = _cells(corridor)
    wall = set()
    for x, y in sea:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                c = (x + dx, y + dy)
                if c not in sea and 0 <= c[0] < W and 0 <= c[1] < H:
                    wall.add(c)
    for d, off, m, (a, b) in conns:              # connected edges: rock all along except the opening
        for t in range(H if d in ("left", "right") else W):
            if a <= t <= b:
                continue
            for depth in (0, 1):
                c = {"left": (depth, t), "right": (W - 1 - depth, t), "up": (t, depth),
                     "down": (t, H - 1 - depth)}[d]
                if c not in sea:
                    wall.add(c)
    rocks, k = [], 0
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if all((x + i, y + j) in wall for i in (0, 1) for j in (0, 1)):
                lid, sx, sy, bw, bh = ROCKS[1 if (x * 7 + y * 3) % 5 == 0 else 0]
                rocks.append((lid, sx, sy, bw, bh, x, y))
                k += 1
    leftover = [c for c in wall if not any(r[5] <= c[0] < r[5] + 2 and r[6] <= c[1] < r[6] + 2 for r in rocks)]
    assert not leftover, "corridor not 2-aligned: %s" % sorted(leftover)[:6]
    grid = [["~"] * W for _ in range(H)]
    for x, y, w, h in islets:
        for j in range(h):
            for i in range(w):
                grid[y + j][x + i] = "G" if 0 < i < w - 1 and 0 < j < h - 1 and w >= 6 and h >= 4 else "."
    mask = ["".join(r) for r in grid]
    spec = dict(
        name=name, size=size, tileset=SEVII, ground=v1.SEA,
        mask=vc.ring_multi(mask, [(".G", "R", "W")]),
        mask_legend={"~": v1.SEA, ".": v1.I(v1.GRASS), "G": v1.I(v1.GRASS)},
        edges_list=v1.coast_edges(rock=False, shore=False),
        big_trees="G",
        pstamps=rocks,
        marks=list(marks),
        corridor=corridor, conns=list(conns),
    )
    for d, off, m, (a, b) in conns:
        lab = m.replace("MAP_", "").replace("_", " ").title()
        if d == "left":
            spec["marks"].append((0, a, "< " + lab, "conn"))
        elif d == "right":
            spec["marks"].append((max(0, W - 10), a, lab + " >", "conn"))
        elif d == "up":
            spec["marks"].append((a, 0, "^ " + lab, "conn"))
        else:
            spec["marks"].append((a, H - 1, "v " + lab, "conn"))
    return spec


def passable_sea(v, ts):
    return (v >> 10) & 3 == 0 and vc.is_water(v & 0x3FF, vc.real_pair(ts))


def check(spec, grid, neighbours):
    """neighbours: {map: (grid, tileset)} rendered island grids. -> list of problem strings."""
    W, H = spec["size"]
    ts = spec["tileset"]
    probs = []
    for d, off, m, (a, b) in spec["conns"]:
        ng, nts = neighbours[m]
        nh, nw = len(ng), len(ng[0])
        rng = range(H) if d in ("left", "right") else range(W)
        for t in rng:
            if d == "left":
                mine, theirs = grid[t][0], (ng[t - off][nw - 1] if 0 <= t - off < nh else None)
            elif d == "right":
                mine, theirs = grid[t][W - 1], (ng[t - off][0] if 0 <= t - off < nh else None)
            elif d == "up":
                mine, theirs = grid[0][t], (ng[nh - 1][t - off] if 0 <= t - off < nw else None)
            else:
                mine, theirs = grid[H - 1][t], (ng[0][t - off] if 0 <= t - off < nw else None)
            inside = a <= t <= b
            if inside and (not passable_sea(mine, ts) or theirs is None or not passable_sea(theirs, nts)):
                probs.append("%s %s edge cell %d: opening not open (route %03X, %s %s)" % (
                    spec["name"], d, t, mine & 0x3FF, m, "-" if theirs is None else "%03X" % (theirs & 0x3FF)))
            if not inside and theirs is not None and passable_sea(mine, ts) and passable_sea(theirs, nts):
                probs.append("%s %s edge cell %d: leak outside the corridor into %s" % (spec["name"], d, t, m))
    return probs


def autofit(spec, neighbours, search=16):
    """Shift each connection offset (nearest first) until every opening cell meets passable sea across the
    edge in the neighbour's rendered grid (islands keep their 2x2 sea rocks). Updates spec["conns"] and the
    conn labels in place; -> [(map, old offset, new offset)]."""
    W, H = spec["size"]
    out = []
    conns = []
    for d, off, m, (a, b) in spec["conns"]:
        ng, nts = neighbours[m]
        nh, nw = len(ng), len(ng[0])

        def ok(o):
            for t in range(a, b + 1):
                if d in ("left", "right"):
                    r = t - o
                    if not 0 <= r < nh:
                        return False
                    v = ng[r][nw - 1] if d == "left" else ng[r][0]
                else:
                    c = t - o
                    if not 0 <= c < nw:
                        return False
                    v = ng[nh - 1][c] if d == "up" else ng[0][c]
                if not passable_sea(v, nts):
                    return False
            return True
        for k in sorted(range(-search, search + 1), key=abs):
            if ok(off + k):
                conns.append((d, off + k, m, (a, b)))
                out.append((m, off, off + k))
                break
        else:
            conns.append((d, off, m, (a, b)))
            out.append((m, off, None))
    spec["conns"] = conns
    return out


_OPP = {"left": "right", "right": "left", "up": "down", "down": "up"}


def island_openings(routes):
    """{neighbour map const: [(island edge, lo, hi)]} = the stretch of each island edge a route opens onto
    (island coordinates)."""
    out = {}
    for spec in routes.values():
        for d, off, m, (a, b) in spec["conns"]:
            out.setdefault(m, []).append((_OPP[d], a - off, b - off))
    return out


def clear_edge_rocks(island_spec, openings, depth=3):
    """Drop the island's 2x2 sea-rock stamps that sit in front of a route opening (within `depth` cells of
    the edge, along lo-2 .. hi+2). -> list of removed rock positions."""
    W, H = island_spec["size"]
    keep, gone = [], []
    for st in island_spec.get("pstamps", []):
        lid, sx, sy, bw, bh, dx, dy = st
        is_rock = lid.startswith("LAYOUT_ROUTE104") and (sx, sy) in ((7, 48), (5, 52))
        hit = False
        if is_rock:
            for edge, lo, hi in openings:
                cells = [(dx + i, dy + j) for i in range(bw) for j in range(bh)]
                for x, y in cells:
                    along, dist = {"left": (y, x), "right": (y, W - 1 - x), "up": (x, y),
                                   "down": (x, H - 1 - y)}[edge]
                    if dist < depth and lo - 2 <= along <= hi + 2:
                        hit = True
        (gone if hit else keep).append(st)
    island_spec["pstamps"] = keep
    return [(s[5], s[6]) for s in gone]
