"""
Icefall Cave (Four Island) FRLG -> Emerald cave translation, design-review mockups only (Sailor's Voyages,
batch 3). Nothing under data/, src/, include/ or graphics/ is touched; no tileset is edited.

Each FRLG room is redrawn cell for cell, at the same size, in gTileset_General + gTileset_Cave with Emerald's
blue ice-cave set (Shoal Cave ice room / Orchid's Frigo Cave, metatiles 0x377-0x38F). The user chose this look.

  1. classify  every FRLG cell (secondary gTileset_SeafoamIslands, primary General_Frlg) into a cave class from
               its behaviour, its collision and (for loose rocks) its look: CLASS_CHARS below.
  2. paint     walls with the blue set's plateau rules (wall_piece: lip 0x379 / face 0x389 / sides 0x380 0x382 /
               corners, 2-thick faces where the rock is thick, as the Shoal / Frigo room rings), floor 0x385 with
               the ice-edge pieces, ice 0x38D (COVERED, bottom layer), rocks 0x37D / 0x37E by vanilla adjacency,
               ladders, the blue arrow mat 0x386, General-primary water / waterfall, the blue south ledge.
  3. check     walk_check(): BFS over the translated grid (Emerald behaviours + collision; ice slides, ledges
               jump, water needs Surf, waterfalls Waterfall, warps end the walk). Every warp must stay reachable
               from every warp and no reachable state may be stuck. Each ice field gets the ice_puzzle-style
               report (inputs in / out, stuck states).
  4. outputs   out/batch3/four_island_icefall_cave_<room>.png, @2x.png, _vs_frlg.png (FRLG | Emerald),
               _spec.json; seams are printed (voyage_compose.seams).

usage: <venv python> dev_scripts/voyages/icefall_translate.py [entrance] [1f] [b1f] [back]   (default: all)
"""
import json
import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc            # noqa: E402
import frlg_translate as ft            # noqa: E402

CAVE = ("gTileset_General", "gTileset_Cave")
OUT = os.path.join(HERE, "out", "batch3")
ROOMS = {"entrance": "FourIsland_IcefallCave_Entrance", "1f": "FourIsland_IcefallCave_1F",
         "b1f": "FourIsland_IcefallCave_B1F", "back": "FourIsland_IcefallCave_Back"}
DEST = {"MAP_FOUR_ISLAND": "Four Island", "MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE": "Entrance",
        "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F": "1F", "MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F": "B1F",
        "MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK": "Back"}

# Emerald sprites for the FRLG-only people (mockup only; the real map needs these gfx decided, see report)
vc.SPRITES.setdefault("grunt", ("graphics/object_events/pics/people/team_aqua/aqua_member_m.png", 16, 32, 0, False))
vc.SPRITES.setdefault("glacia", ("graphics/object_events/pics/people/elite_four/glacia.png", 16, 32, 0, False))
PEOPLE = {"OBJ_EVENT_GFX_ROCKET_M": ("AQUA_MEMBER_M", "grunt", "Rocket"),
          "OBJ_EVENT_GFX_LORELEI": ("GLACIA", "glacia", "Lorelei")}

# ================================================================================================ classify
# class chars
#   #  rock / wall mass (and the snow outside the cave)      B  loose rock / ice boulder (impassable)
#   .  floor (non-slip)        ~  sliding ice (MB_ICE)        t  thin ice (MB_THIN_ICE, cracks -> hole to B1F)
#   w  water (pond / ocean)    f  waterfall
#   L  ladder against rock (rock cell above)                  H  free-standing ladder (FRLG hole + ladder)
#   D  cave mouth (MB_NON_ANIMATED_DOOR)                      v  south arrow warp mat
#   <  ledge, jump west        J  ledge, jump south
# FRLG metatiles that are loose rocks (looked at one by one on the id sheet; boulders, snow-capped rocks, ice
# crystals) -- the rest of the solid cells are rock rim / wall mass / snow.
BOULDER_IDS = {0x282, 0x283, 0x2A7, 0x33F, 0x342, 0x344, 0x347, 0x34F, 0x352, 0x354, 0x35C, 0x35E, 0x35F,
               0x362, 0x363, 0x370, 0x371, 0x372, 0x373}
MB_CLASS = {"MB_ICE": "~", "MB_THIN_ICE": "t", "MB_POND_WATER": "w", "MB_OCEAN_WATER": "w", "MB_WATERFALL": "f",
            "MB_SOUTH_ARROW_WARP": "v", "MB_NON_ANIMATED_DOOR": "D", "MB_JUMP_WEST": "<", "MB_JUMP_SOUTH": "J"}
HOLE_LADDERS = {0x2AF, 0x285}      # FRLG ladder drawn in a dark hole in the floor (not against rock)
OPEN = set(".~twfHv<JBR")           # everything that is not rock mass (for the wall rules); the ladder-in-rock
                                    # (L) and cave-mouth (D) cells are drawn inside the rock face, so they count
                                    # as rock: the face runs straight past them
SEA_ROCK = {0x110: 0x150, 0x111: 0x151, 0x118: 0x158, 0x119: 0x159}   # FRLG 2x2 sea rock -> Route 130's


def behaviour(fm, x, y):
    return ft.MB[fm.scene.attr(fm.mid(x, y)) & 0x1FF]


def classify(fm):
    W, H = fm.w, fm.h
    g = [["#"] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            b, solid, m = behaviour(fm, x, y), fm.coll(x, y), fm.mid(x, y)
            elev = fm.raw[y][x] >> 12
            if b in MB_CLASS and (not solid or b.startswith("MB_JUMP")):
                g[y][x] = MB_CLASS[b]
            elif b == "MB_LADDER":
                g[y][x] = "H" if m in HOLE_LADDERS or not (y > 0 and fm.coll(x, y - 1)) else "L"
            elif not solid:
                g[y][x] = "." if elev else "#"      # elev-0 passable snow outside the walls: unreachable, rock
            elif m in BOULDER_IDS:
                g[y][x] = "B"
            elif m in SEA_ROCK:
                g[y][x] = "R"
    # small detached rock lumps (1-2 cells, e.g. a rock drawn on ice) are boulders too
    seen = set()
    for y in range(H):
        for x in range(W):
            if g[y][x] != "#" or (x, y) in seen:
                continue
            comp, q, edge = [], deque([(x, y)]), False
            seen.add((x, y))
            while q:
                cx, cy = q.popleft()
                comp.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < W and 0 <= ny < H):
                        edge = True
                    elif g[ny][nx] == "#" and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            if not edge and len(comp) <= 2:
                for cx, cy in comp:
                    g[cy][cx] = "B"
    return ["".join(r) for r in g]


# ================================================================================================ paint
def I(m, *ce):
    return ("id", m) + ce


def wall_piece(cls, x, y):
    """Blue ice-cave plateau piece for a rock cell, from where the open cells are (Shoal ice room / Frigo Cave
    rings: 1-row lip 0x379 above open floor, 2-row face 0x389 below, 2-column sides 0x382 (open to the east) /
    0x380 (open to the west) where the rock is thick, outer corners 0x378 / 0x37A / 0x388 / 0x38A, inner corners
    0x37B / 0x37C at the top, 0x383 where the lip runs on under a side face)."""
    H, W = len(cls), len(cls[0])

    def op(dx, dy):
        nx, ny = x + dx, y + dy
        return 0 <= nx < W and 0 <= ny < H and cls[ny][nx] in OPEN

    def thick(dx, dy, n=3):      # rock continues n cells the other way (or reaches the map edge)
        return not any(op(dx * k, dy * k) for k in range(1, n + 1))

    if op(0, 1):                                   # face, open below
        if op(-1, 0) and not op(1, 0):
            return 0x388
        if op(1, 0) and not op(-1, 0):
            return 0x38A
        return 0x389
    if op(0, -1):                                  # lip, open above
        if op(-1, 0) and not op(1, 0):
            return 0x378
        if op(1, 0) and not op(-1, 0):
            return 0x37A
        return 0x379
    if op(1, 0):
        return 0x382
    if op(-1, 0):
        return 0x380
    if op(0, 2) and thick(0, -1):                  # second face row of a thick wall
        return 0x389
    if op(2, 0) and thick(-1, 0):
        return 0x382
    if op(-2, 0) and thick(1, 0):
        return 0x380
    # diagonal-only openings, nearest first (Shoal / Frigo ring corners: (1,1) and (2,2) inner corner 0x37B /
    # 0x37C, (1,2) second face row, (2,1) second side column, lip running on under a side face 0x383)
    for dx, dy, m in ((1, 1, 0x37B), (-1, 1, 0x37C), (1, -1, 0x383), (-1, -1, 0x383),
                      (1, 2, 0x389), (-1, 2, 0x389), (2, 1, 0x382), (-2, 1, 0x380),
                      (2, 2, 0x37B), (-2, 2, 0x37C), (2, -1, 0x383), (-2, -1, 0x383)):
        if op(dx, dy):
            return m
    return 0x381


def floor_piece(cls, x, y):
    """0x385 rough floor, with the ice-edge pieces where sliding ice touches it (0x38F ice N, 0x387 ice S,
    0x38E ice W, 0x38C ice E) -- the Shoal / Frigo usage."""
    H, W = len(cls), len(cls[0])

    def ice(dx, dy):
        nx, ny = x + dx, y + dy
        return 0 <= nx < W and 0 <= ny < H and cls[ny][nx] == "~"

    if ice(0, -1):
        return 0x38F
    if ice(0, 1):
        return 0x387
    if ice(-1, 0):
        return 0x38E
    if ice(1, 0):
        return 0x38C
    return 0x385


def water_piece(cls, x, y):
    """General-primary water 0x170 with Shoal Cave's deep-water edges (pale band inside the water cell) on the
    north / west / east sides. The south-side edges in Shoal (0x1AE / 0x19C / 0x19B) are MB_SHALLOW_WATER, i.e.
    walkable, so they are NOT used: the cell stays 0x170 and the walk path stays FRLG's."""
    H, W = len(cls), len(cls[0])

    def land(dx, dy):
        nx, ny = x + dx, y + dy
        return 0 <= nx < W and 0 <= ny < H and cls[ny][nx] not in "wfR"

    if land(0, -1):
        return 0x1A4 if land(-1, 0) else 0x1A3 if land(1, 0) else 0x1BE
    if land(-1, 0):
        return 0x1B7
    if land(1, 0):
        return 0x1B5
    if land(-1, -1):
        return 0x1BF
    if land(1, -1):
        return 0x1BD
    return 0x170


def waterfall_piece(cls, x, y):
    top = y == 0 or cls[y - 1][x] != "f"
    if top:
        left, right = cls[y][x - 1] != "f", cls[y][x + 1] != "f"
        return 0x0BB if left else 0x0BC if right else 0x0B3
    return 0x0B9


RAW_386 = 0x3000 | 0x386        # MB_SOUTH_ARROW_WARP, blue set; in gTileset_Cave but no layout places it
RAW_38B = 0x3000 | 0x38B        # MB_LADDER, free-standing blue ladder; in gTileset_Cave, no layout places it


def translate(fm, cls=None):
    cls = cls or classify(fm)
    W, H = fm.w, fm.h
    cells, auto, marks, notes = [], [], [], []
    for y in range(H):
        for x in range(W):
            c = cls[y][x]
            if c == "#":
                cells.append((x, y, I(wall_piece(cls, x, y), 1)))
            elif c in ".":
                cells.append((x, y, I(floor_piece(cls, x, y), 0, 3)))
            elif c == "~":
                cells.append((x, y, I(0x38D, 0, 3)))
            elif c == "t":
                cells.append((x, y, I(0x28F)))
                marks.append((x, y, "t", "note"))
            elif c == "B":
                auto.append((x, y, [0x37D, 0x37E]))
            elif c == "w":
                cells.append((x, y, I(water_piece(cls, x, y))))
            elif c == "R":
                cells.append((x, y, I(SEA_ROCK[fm.mid(x, y)], 1)))
            elif c == "f":
                cells.append((x, y, I(waterfall_piece(cls, x, y))))
            elif c == "L":
                cells.append((x, y, I(0x37F)))
                cells.append((x, y - 1, I(0x377)))
            elif c == "D":                         # no blue cave mouth: the ladder pair stands in
                cells.append((x, y, I(0x37F)))
                cells.append((x, y - 1, I(0x377)))
                notes.append("cave mouth (%d,%d) drawn as the blue ladder pair 0x377/0x37F" % (x, y))
            elif c == "H":
                cells.append((x, y, ("raw", RAW_38B)))
            elif c == "v":
                cells.append((x, y, ("raw", RAW_386)))
            elif c == "J":
                run_l = x > 0 and cls[y][x - 1] == "J"
                run_r = x + 1 < W and cls[y][x + 1] == "J"
                cells.append((x, y, I(0x287 if run_l and run_r else 0x27F if run_l else 0x277)))
            elif c == "<":                         # no blue west ledge: floor art + note
                cells.append((x, y, I(0x385, 0, 3)))
                marks.append((x, y, "<", "note"))
    # events
    for w in fm.json.get("warp_events", []):
        marks.append((w["x"], w["y"], DEST.get(w["dest_map"], w["dest_map"]), "warp"))
    objects = []
    for o in fm.json.get("object_events", []):
        gid = o.get("graphics_id", "")
        if gid in PEOPLE:
            eg, spr, lab = PEOPLE[gid]
            marks.append((o["x"], o["y"], lab, "npc", spr))
        elif "ITEM_BALL" in gid:
            eg = "ITEM_BALL"
            marks.append((o["x"], o["y"], "", "item", "item"))
        else:
            eg, spr = ft.swap_gfx(gid)
            fo = ft.FIELD_OBJECTS.get(eg)
            marks.append((o["x"], o["y"], "", "field", fo) if fo else (o["x"], o["y"], eg[:6].lower(), "npc", spr))
        objects.append(dict(graphics_id="OBJ_EVENT_GFX_" + eg, x=o["x"], y=o["y"], script=o.get("script"),
                            frlg_graphics_id=gid))
    for b in fm.json.get("bg_events", []):
        marks.append((b["x"], b["y"], "h" if b["type"] == "hidden_item" else "", "note" if b["type"] != "sign"
                      else "sign"))
    for c in fm.json.get("coord_events", []):
        marks.append((c["x"], c["y"], "", "spot"))
    spec = dict(name="Icefall Cave " + fm.name, size=(W, H), tileset=CAVE, ground=I(0x381, 1),
                cells=cells, auto=auto, marks=marks, object_events=objects,
                warps=[(w["x"], w["y"], w["dest_map"], w["dest_warp_id"]) for w in fm.json.get("warp_events", [])])
    fm.report = dict(pair=CAVE, classes=cls, notes=notes)
    return spec


WALL_VOCAB = [0x378, 0x379, 0x37A, 0x37B, 0x37C, 0x380, 0x381, 0x382, 0x383, 0x388, 0x389, 0x38A]


# sides (N, S, W, E) on which each blue rock piece may touch an open cell directly
PIECE_SIDES = {0x389: "S", 0x388: "SW", 0x38A: "SE", 0x379: "N", 0x378: "NW", 0x37A: "NE", 0x382: "E", 0x380: "W",
               0x37B: "", 0x37C: "", 0x383: "", 0x381: ""}
# open cells within 2 that make a piece with no open side plausible (second face row / column, inner corners)
PIECE_NEAR = {0x389: [(0, 2), (1, 2), (-1, 2)], 0x382: [(2, 0), (2, 1)], 0x380: [(-2, 0), (-2, 1)],
              0x37B: [(1, 1), (2, 2)], 0x37C: [(-1, 1), (-2, 2)], 0x383: [(1, -1), (-1, -1), (2, -1), (-2, -1)],
              0x381: None}


def wall_candidates(cls, x, y):
    """Rock pieces whose facing agrees with the open cells around (x, y): every directly adjacent open side
    must be one the piece shows; a piece with no adjacent open side needs its own 'near' opening."""
    H, W = len(cls), len(cls[0])

    def op(dx, dy):
        nx, ny = x + dx, y + dy
        return 0 <= nx < W and 0 <= ny < H and cls[ny][nx] in OPEN

    sides = {d for d, (dx, dy) in (("N", (0, -1)), ("S", (0, 1)), ("W", (-1, 0)), ("E", (1, 0))) if op(dx, dy)}
    out = []
    for m, ps in PIECE_SIDES.items():
        if sides:
            if sides <= set(ps) or (len(sides) > 1 and set(ps) & sides and len(ps) == len(sides) - 0):
                out.append(m)
        else:
            near = PIECE_NEAR.get(m, [])
            if near is None or not ps and any(op(*d) for d in near) or ps and any(op(*d) for d in near):
                out.append(m)
    return out


def seam_fix(spec, cls, rounds=3):
    """Second pass over rock cells that sit in a neighbour pair no vanilla layout uses: re-pick them from the
    blue wall vocabulary by vanilla neighbour frequency (voyage_compose.solve), keeping them solid. Written as
    spec["post"] cells; returns the changed cells."""
    g = vc.build(spec)
    changed = {}
    for _ in range(rounds):
        cells = set()
        for x, y, d, a, b in seam_report(g):
            if a in SEAM_BENIGN or b in SEAM_BENIGN:
                continue
            for c in ((x, y), (x + (d == "E"), y + (d == "S"))):
                if cls[c[1]][c[0]] == "#":
                    cells.add(c)
        if not cells:
            break
        before = len(seam_report(g))
        g2 = [r[:] for r in g]
        cand = {}
        for c in sorted(cells):
            cur = g[c[1]][c[0]] & 0x3FF
            cand[c] = [cur] + [m for m in wall_candidates(cls, *c) if m != cur]
        vc.solve(g2, cand, CAVE)
        if len(seam_report(g2)) >= before:
            break
        for (x, y) in cells:
            if g2[y][x] & 0x3FF != g[y][x] & 0x3FF:
                changed[(x, y)] = g2[y][x] & 0x3FF
        g = g2
    spec["post"] = spec.get("post", []) + [(x, y, I(m, 1)) for (x, y), m in sorted(changed.items())]
    return changed


# ================================================================================================ walk check
def em_behaviour(v):
    m = v & 0x3FF
    sc = vc.scene(CAVE)
    a = sc.p.attrs[m] if m < 0x200 else sc.s.attrs[m - 0x200]
    return ft.MB[a & 0xFF]


DIRS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
JUMP = {"MB_JUMP_WEST": "W", "MB_JUMP_SOUTH": "S", "MB_JUMP_EAST": "E", "MB_JUMP_NORTH": "N"}
WATER = {"MB_POND_WATER", "MB_OCEAN_WATER", "MB_DEEP_WATER", "MB_WATERFALL"}


class Walk:
    """Movement model on the translated grid (player has Surf + Waterfall, post-game). Collision bit and
    Emerald behaviour decide: ice slides until the next cell blocks, ledges jump two cells in their direction,
    water / waterfall need Surf, any warp cell ends the walk. Object events with `block` coords are obstacles
    (item balls until picked up). Extra: FRLG-only ledges (west ledge drawn as floor) from the class grid."""

    def __init__(self, g, cls, warps, block=(), holes=(), beh=None):
        self.g, self.cls, self.H, self.W = g, cls, len(g), len(g[0])
        self.beh_fn = beh
        self.warps = {(x, y) for x, y in warps}
        self.block = set(block)
        self.holes = set(holes)

    def beh(self, x, y):
        return self.beh_fn(x, y) if self.beh_fn else em_behaviour(self.g[y][x])

    def jump_dir(self, x, y):
        if self.cls[y][x] == "<":
            return "W"
        return JUMP.get(self.beh(x, y))

    def passable(self, x, y):
        if not (0 <= x < self.W and 0 <= y < self.H) or (x, y) in self.block:
            return False
        return not (self.g[y][x] >> 10) & 3 and self.cls[y][x] != "<"

    def is_ice(self, x, y):
        return self.beh(x, y) == "MB_ICE"

    def moves(self, pos):
        for d, (dx, dy) in DIRS.items():
            x, y = pos[0] + dx, pos[1] + dy
            if not (0 <= x < self.W and 0 <= y < self.H):
                continue
            jd = self.jump_dir(x, y)
            if jd:
                if jd == d and self.passable(x + dx, y + dy):
                    yield d, (x + dx, y + dy)
                continue
            if not self.passable(x, y):
                continue
            p = (x, y)
            while self.is_ice(*p) and p not in self.warps:
                q = (p[0] + dx, p[1] + dy)
                if not self.passable(*q) or self.jump_dir(*q):
                    break
                p = q
            yield d, p

    def bfs(self, start):
        prev, order = {start: None}, deque([start])
        while order:
            s = order.popleft()
            if s in self.warps and s != start or s in self.holes and s != start:
                continue                                  # walking onto a warp / hole leaves the room
            for d, n in self.moves(s):
                if n not in prev:
                    prev[n] = (s, d)
                    order.append(n)
        return prev

    @staticmethod
    def route(prev, t):
        out = []
        while prev.get(t):
            t, d = prev[t]
            out.append(d)
        return "".join(out[::-1])


def landings(key):
    """Cells you land on after falling through 1F's cracked ice (warphole keeps x, y): B1F's extra entries."""
    if key != "b1f":
        return []
    c1 = classify(ft.load_map(ROOMS["1f"]))
    return [(x, y) for y, r in enumerate(c1) for x, ch in enumerate(r) if ch == "t"]


def walk_check(g, cls, fm, block=(), frlg=False, extra=()):
    """-> dict: per warp (as entry) which other warps / holes are reachable; stuck states (reachable cells from
    which no exit at all can be reached, or from which some warp reachable from the start is lost for good)."""
    warps = [(w["x"], w["y"]) for w in fm.json.get("warp_events", [])]
    holes = [(x, y) for y, r in enumerate(cls) for x, c in enumerate(r) if c == "t"]
    wk = Walk(g, cls, warps, block, holes, beh=(lambda x, y: behaviour(fm, x, y)) if frlg else None)
    exits = set(warps) | set(holes)
    res = {}
    all_states = set()
    for e in list(warps) + list(extra):
        prev = wk.bfs(e)
        all_states |= set(prev)
        res[e] = dict(reach=sorted(t for t in exits if t in prev and t != e), prev=prev)
    # from every reachable state: which exits can still be reached
    lost = {}
    for s in sorted(all_states):
        if s in exits:
            continue
        r = wk.bfs(s)
        can = {t for t in exits if t in r}
        if not can:
            lost[s] = "STUCK (no exit)"
        else:
            # every warp that the start component could reach must stay reachable (no one-way loss) --
            # unless FRLG itself makes it one-way (ledges); reported, not failed
            missing = {t for t in warps if t not in can}
            if missing:
                lost[s] = "cannot reach " + ",".join("(%d,%d)" % t for t in sorted(missing))
    return wk, res, lost


def ice_fields(cls):
    """4-connected components of sliding ice cells."""
    H, W = len(cls), len(cls[0])
    seen, out = set(), []
    for y in range(H):
        for x in range(W):
            if cls[y][x] == "~" and (x, y) not in seen:
                comp, q = set(), deque([(x, y)])
                seen.add((x, y))
                while q:
                    c = q.popleft()
                    comp.add(c)
                    for dx, dy in DIRS.values():
                        n = (c[0] + dx, c[1] + dy)
                        if 0 <= n[0] < W and 0 <= n[1] < H and cls[n[1]][n[0]] == "~" and n not in seen:
                            seen.add(n)
                            q.append(n)
                out.append(comp)
    return out


ICE_GOALS = {"b1f": {(20, 7): "NeverMeltIce (stand W of the ball)"}}


def ice_report(wk, field, starts, goals, back_to):
    """ice_puzzle-style check for one ice field. route = shortest input string from any start to any goal,
    back = shortest from that goal to any of `back_to` (the room's ladders / warps). Over every reachable state
    on or next to the field: stuck = no warp reachable at all (softlock); no_goal = the goal is no longer
    reachable (informational: FRLG's one-way ledges / pockets)."""
    best = None
    reach = set()
    per_start = {}
    for s0 in starts:
        prev = wk.bfs(s0)
        reach |= set(prev)
        for gl in goals:
            if gl in prev:
                r = wk.route(prev, gl)
                if s0 not in per_start or len(r) < len(per_start[s0]):
                    per_start[s0] = r
                if best is None or len(r) < len(best[1]):
                    best = (s0, r, gl)
    near = {c for c in reach if c in field or any((c[0] + dx, c[1] + dy) in field for dx, dy in DIRS.values())}
    stuck, no_goal = [], []
    for c in sorted(near):
        if c in wk.warps:
            continue
        r2 = wk.bfs(c)
        if not any(b in r2 for b in back_to):
            stuck.append(c)
        if goals and not any(gl in r2 for gl in goals):
            no_goal.append(c)
    out = dict(states=len(near), stuck=stuck, no_goal=no_goal, route=None, back=None, per_start=per_start)
    if best:
        s0, r, gl = best
        p2 = wk.bfs(gl)
        backs = [wk.route(p2, b) for b in back_to if b in p2]
        out.update(start=s0, goal=gl, route=r, back=min(backs, key=len) if backs else None)
    return out


def path_cells(wk, start, route):
    pts, pos = [start], start
    for d in route:
        pos = dict(wk.moves(pos))[d]
        pts.append(pos)
    return pts


# ================================================================================================ run
def render_room(key, spec=None, suffix="", zoom=None):
    fm = ft.load_map(ROOMS[key])
    if spec is None:
        spec = translate(fm)
        fm.report["seam_fixed"] = len(seam_fix(spec, fm.report["classes"]))
    base = os.path.join(OUT, "four_island_icefall_cave_" + key + suffix)
    g = vc.render(spec, base)
    ft.side_by_side(fm, base, zoom=zoom)
    keep = {k: v for k, v in spec.items() if k != "cells"}
    keep["classes"] = fm.report["classes"]
    keep["notes"] = fm.report["notes"]
    keep["grid_raw"] = [" ".join("%04X" % v for v in row) for row in g]
    json.dump(keep, open(base + "_spec.json", "w"), indent=0, default=str)
    return fm, spec, g, base


def seam_report(g, ignore=(0x381,)):
    return vc.seams(g, CAVE, ignore=ignore)


SEAM_BENIGN = {0x37D, 0x37E, 0x28F, 0x386, RAW_38B & 0x3FF}   # boulders / spots / mats on plain floor


def check_room(fm, g, cls, block, extra=()):
    """FRLG and Emerald walk checks side by side; returns (same, lost_em, lost_frlg, wk_em, res_em)."""
    wk, res, lost = walk_check(g, cls, fm, block=block, extra=extra)
    _, res_f, lost_f = walk_check(fm.raw, cls, fm, block=block, frlg=True, extra=extra)
    same = all(set(res[e]["prev"]) == set(res_f[e]["prev"]) for e in res)
    return same, lost, lost_f, wk, res


def report_room(key, fm, g):
    cls = fm.report["classes"]
    print("== %s  %dx%d  %s + %s" % (fm.name, fm.w, fm.h, *CAVE))
    items = [(o["x"], o["y"]) for o in fm.json.get("object_events", []) if "ITEM_BALL" in o["graphics_id"]]
    extra = landings(key)
    same, lost, lost_f, wk, res = check_room(fm, g, cls, items, extra)
    print("  walk check (Surf + Waterfall, item balls block): reachable cells identical to FRLG from every"
          " entry: %s" % same)
    for e, r in res.items():
        print("    from %s %s reach %s" % ("landing" if e in extra else "warp", e, r["reach"]))
    stuck = [s for s, why in lost.items() if why.startswith("STUCK")]
    print("  stuck states (no exit at all): %d %s" % (len(stuck), stuck))
    print("  one-way states (a warp no longer reachable; identical in FRLG: %s): %d" % (set(lost) == set(lost_f),
                                                                                       len(lost)))
    warps = [(w["x"], w["y"]) for w in fm.json.get("warp_events", [])]
    out = dict(same_as_frlg=same, stuck=stuck, one_way=len(lost), ice=[])
    for f in ice_fields(cls):
        goals = ICE_GOALS.get(key, {})
        r = ice_report(wk, f, warps + list(extra), list(goals) or warps, warps)
        ok = not r["stuck"] and r["route"] is not None and r["back"] is not None
        print("  ice field %d cells, bbox x%d-%d y%d-%d: %s | states on/next to it %d | stuck %d %s | goal %s"
              " unreachable from %d states" % (
                  len(f), min(c[0] for c in f), max(c[0] for c in f), min(c[1] for c in f), max(c[1] for c in f),
                  "PASS" if ok else "FAIL", r["states"], len(r["stuck"]), r["stuck"],
                  list(goals.values()) or "any warp", len(r["no_goal"])))
        if r["route"] is not None:
            print("    in: from %s %s (%d inputs) -> %s | out: %s (%d inputs)" % (
                r["start"], r["route"], len(r["route"]), r["goal"], r["back"], len(r["back"] or "")))
            print("    goal reached from: %s" % {k: v for k, v in r["per_start"].items()})
        out["ice"].append(r)
    s = seam_report(g)
    hard = [t for t in s if t[3] not in SEAM_BENIGN and t[4] not in SEAM_BENIGN]
    print("  seams: %d (%d not involving a boulder / spot / mat; %d rock cells re-picked) %s" % (
        len(s), len(hard), fm.report.get("seam_fixed", 0), ["(%d,%d)%s %03X|%03X" % t for t in hard]))
    for n in fm.report["notes"]:
        print("  note:", n)
    return out


KEY_OF = {"MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE": "entrance", "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F": "1f",
          "MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F": "b1f", "MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK": "back"}


def cave_graph(rooms, frlg=False):
    """Whole-cave check over the four rooms as one state graph (room, x, y): warps join rooms (arriving on the
    destination warp cell), 1F's thin ice can also drop you to the same cell of B1F, Four Island = 'OUT'.
    Starts at the Entrance mat; returns (reachable states, states that can no longer get OUT, warps used)."""
    W = {}
    for k, (fm, g, cls) in rooms.items():
        items = [(o["x"], o["y"]) for o in fm.json.get("object_events", []) if "ITEM_BALL" in o["graphics_id"]]
        warps = [(w["x"], w["y"]) for w in fm.json.get("warp_events", [])]
        W[k] = (fm, Walk(fm.raw if frlg else g, cls, warps, items,
                         beh=(lambda x, y, fm=fm: behaviour(fm, x, y)) if frlg else None), cls)

    def succ(st):
        if st == "OUT":
            return
        k, x, y = st
        fm, wk, cls = W[k]
        for _, n in wk.moves((x, y)):
            if n in wk.warps:
                w = next(w for w in fm.json["warp_events"] if (w["x"], w["y"]) == n)
                dk = KEY_OF.get(w["dest_map"])
                if dk is None:
                    yield "OUT"
                elif dk in W:
                    dw = W[dk][0].json["warp_events"][int(w["dest_warp_id"])]
                    yield (dk, dw["x"], dw["y"])
                continue
            yield (k, n[0], n[1])
            if cls[n[1]][n[0]] == "t" and "b1f" in W:
                yield ("b1f", n[0], n[1])

    start = ("entrance", 17, 30)
    seen, q, used = {start}, deque([start]), set()
    edges = {}
    while q:
        st = q.popleft()
        for n in succ(st):
            edges.setdefault(n, set()).add(st)
            if isinstance(n, tuple) and isinstance(st, tuple) and n[0] != st[0]:
                used.add((st[0], n[0]))
            if n not in seen:
                seen.add(n)
                q.append(n)
    good, q = {"OUT"} & seen, deque({"OUT"} & seen)
    while q:
        st = q.popleft()
        for p in edges.get(st, ()):
            if p not in good:
                good.add(p)
                q.append(p)
    return seen, [st for st in seen if st not in good], used


def main(keys):
    built = {}
    for k in keys:
        fm, spec, g, base = render_room(k)
        report_room(k, fm, g)
        built[k] = (fm, g, fm.report["classes"])
    if set(built) == set(ROOMS):
        for frlg in (False, True):
            seen, stuck, used = cave_graph(built, frlg)
            print("== whole cave (%s): %d states reachable from the Entrance mat, %d cannot get back out %s;"
                  " NeverMeltIce spot reached: %s; Back (Lorelei) reached: %s; room links used: %s" % (
                      "FRLG" if frlg else "Emerald", len(seen), len(stuck), sorted(stuck)[:10],
                      ("b1f", 20, 7) in seen, any(s[0] == "back" for s in seen if s != "OUT"), sorted(used)))


if __name__ == "__main__":
    main(sys.argv[1:] or list(ROOMS))
