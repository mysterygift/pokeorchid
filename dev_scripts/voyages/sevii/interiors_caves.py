"""
Sevii cave interiors: FRLG -> Emerald, design-review mockups (helper of frlg_interiors.py). Nothing under data/,
src/, include/ or graphics/ is touched; no tileset is edited.

Generalises icefall_translate.py: instead of hand-written plateau rules for one colour set, the rock pieces are
LEARNT from vanilla Emerald rooms of the target set, so any cave set works:

  1. classify  FRLG cells -> classes: '#' rock mass, '.' floor ('*' = floor with a FRLG detail metatile), 'B'
               loose rock (solid lump of <= 4 cells inside open floor), 'v' exit mat, 'D' cave door, 'U' ladder
               against rock (up), 'H' ladder in a floor hole (down), 'S' rock stairs, 'w' water / hot spring,
               'f' waterfall, 'J' / '<' ledges, 'h' fall hole, 'b' floor switch. Open cells no warp can reach
               are rock.
  2. learn     every vanilla cell of the set's training rooms is split rock / open (collision, or
               MB_MOUNTAIN_TOP plateau tops; decoration ids count as open). For each rock id, counts per
               neighbourhood signature at 4 levels: 5x5, 3x3 + the four cells two away, blob-reduced 3x3,
               orthogonal 4. Floors are learnt the same way over the set's floor ids (shadowed floor under faces).
  3. paint     each rock / floor cell takes the most frequent id of the most specific signature seen in vanilla;
               specials use the set's pieces. Collision + elevation are FRLG's (walk layout kept exactly).
  4. seams     rock cells in a neighbour pair no vanilla room has are re-picked by voyage_compose.solve among the
               ids seen with the same blob signature (2 rounds; kept only if seams go down).

Sets: lava (General + Lavaridge = Fiery Path / Magma Hideout + Lavaridge hot springs), cave (General + Cave
brown = Granite Cave), navel (General + NavelRock = Emerald Navel Rock), ruins (General + Cave = Sealed
Chamber / Desert Ruins / Island Cave / Ancient Tomb).
"""
import os
import sys
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc            # noqa: E402
import frlg_translate as ft            # noqa: E402

G = "gTileset_General"
_MH = ["LAYOUT_MAGMA_HIDEOUT_1F", "LAYOUT_MAGMA_HIDEOUT_2F_1R", "LAYOUT_MAGMA_HIDEOUT_2F_2R",
       "LAYOUT_MAGMA_HIDEOUT_2F_3R", "LAYOUT_MAGMA_HIDEOUT_3F_1R", "LAYOUT_MAGMA_HIDEOUT_3F_2R",
       "LAYOUT_MAGMA_HIDEOUT_3F_3R", "LAYOUT_MAGMA_HIDEOUT_4F"]
SETS = {
    "lava": dict(
        pair=(G, "gTileset_Lavaridge"), train=["LAYOUT_FIERY_PATH"] + _MH,
        floor=[0x308], detail=[0x310, 0x311], mat=0x309, door=0x25E, up=0x2AE, down=0x2AE, hole=0x25E,
        stairs=0x2AF, boulder=[0x30D], ledge_s=0x2EA, ledge_w=0x2E8, button=0x30D,
        water=0x2AB, water_top=0x2A3,
        exclude=set(range(0x2B6, 0x2D0)) | set(range(0x2D6, 0x2E8)) | {0x30D, 0x312, 0x313, 0x2AF, 0x256}
        | set(range(0x36D, 0x3A2)) | set(range(0x20D, 0x210)),
        look="Fiery Path / Magma Hideout red rock (Mt. Chimney's volcano cave), Lavaridge hot-spring water"),
    "cave": dict(
        pair=(G, "gTileset_Cave"), train=["LAYOUT_GRANITE_CAVE_1F", "LAYOUT_GRANITE_CAVE_B1F",
                                          "LAYOUT_GRANITE_CAVE_B2F", "LAYOUT_GRANITE_CAVE_STEVENS_ROOM",
                                          "LAYOUT_ARTISAN_CAVE_1F", "LAYOUT_ARTISAN_CAVE_B1F"],
        floor=[0x201, 0x211], detail=[0x221], mat=0x23C, door=0x214, up=0x217, up_top=0x20F, down=0x23F, hole=0x206,
        stairs=0x204, boulder=[0x202, 0x203], ledge_s=0x252, ledge_w=0x23A, button=0x22F,
        water=0x170, water_top=0x170,
        exclude={0x202, 0x203, 0x22F, 0x204, 0x250, 0x253, 0x258, 0x259, 0x25A, 0x262} | set(range(0x298, 0x2AB)),
        look="Granite Cave brown"),
    "rusturf": dict(
        pair=(G, "gTileset_RusturfTunnel"), train=["LAYOUT_RUSTURF_TUNNEL"],
        floor=[0x201], detail=[0x202], mat=0x207, door=0x209, up=0x21F, down=0x21F, hole=0x201,
        stairs=0x21F, boulder=[0x203], ledge_s=0x23C, ledge_w=0x23C, button=0x202,
        water=0x170, water_top=0x170,
        exclude={0x203, 0x21F, 0x250, 0x251, 0x252},
        look="Rusturf Tunnel (Emerald's dug-through tunnel; grey-green)"),
    "navel": dict(
        pair=(G, "gTileset_NavelRock"), train=["LAYOUT_NAVEL_ROCK_ENTRANCE", "LAYOUT_NAVEL_ROCK_LADDER_ROOM1",
                                               "LAYOUT_NAVEL_ROCK_LADDER_ROOM2", "LAYOUT_NAVEL_ROCK_B1F",
                                               "LAYOUT_NAVEL_ROCK_FORK"],
        alias=["LAYOUT_GRANITE_CAVE_1F", "LAYOUT_GRANITE_CAVE_B1F", "LAYOUT_GRANITE_CAVE_B2F",
               "LAYOUT_GRANITE_CAVE_STEVENS_ROOM"],     # gTileset_Cave: same metatile arrangement as NavelRock
        floor=[0x211, 0x201], detail=[0x201], mat=0x23C, door=0x214, up=0x217, up_top=0x20F, down=0x23F, hole=0x206,
        stairs=0x204, boulder=[0x202, 0x203], ledge_s=0x252, ledge_w=0x23A, button=0x22F,
        water=0x170, water_top=0x170,
        exclude={0x202, 0x203, 0x258, 0x259, 0x25A} | set(range(0x2D0, 0x2E3)),
        look="Emerald Navel Rock (the R/S/E version of the tileset Dotted Hole uses in FRLG)"),
    "ruins": dict(
        pair=(G, "gTileset_Cave"), train=["LAYOUT_SEALED_CHAMBER_OUTER_ROOM", "LAYOUT_SEALED_CHAMBER_INNER_ROOM",
                                          "LAYOUT_DESERT_RUINS", "LAYOUT_ISLAND_CAVE", "LAYOUT_ANCIENT_TOMB"],
        floor=[0x201], detail=[0x201], mat=0x23C, door=0x233, up=0x217, up_top=0x20F, down=0x23F, hole=0x206,
        stairs=0x204, boulder=[0x202, 0x203], ledge_s=0x252, ledge_w=0x23A, button=0x22F,
        water=0x170, water_top=0x170,
        exclude=set(range(0x170, 0x1A0)) | {0x147, 0x156, 0x233, 0x229, 0x22A, 0x22B, 0x22C, 0x232, 0x234,
                                             0x2D1, 0x2D9, 0x2E1, 0x308, 0x309, 0x311, 0x302, 0x303},
        look="Sealed Chamber / Regi-tomb ruins (raised stone slabs)"),
}

SPECIAL_MB = {"MB_SOUTH_ARROW_WARP", "MB_NON_ANIMATED_DOOR", "MB_LADDER", "MB_ROCK_STAIRS", "MB_HOT_SPRINGS",
              "MB_POND_WATER", "MB_OCEAN_WATER", "MB_WATERFALL", "MB_JUMP_SOUTH", "MB_JUMP_WEST", "MB_JUMP_EAST",
              "MB_MT_PYRE_HOLE", "MB_STRENGTH_BUTTON", "MB_NORTH_ARROW_WARP", "MB_CRACKED_FLOOR_HOLE",
              "MB_DEEP_WATER", "MB_SHALLOW_WATER", "MB_JUMP_SOUTHWEST", "MB_JUMP_SOUTHEAST"}
OPEN_CLASSES = set(".*BvSwfJ<hbH")      # for the rock signature: everything but rock mass ('#', 'D', 'U')


# ================================================================================================ FRLG side
def behaviour(fm, x, y):
    return ft.MB[fm.scene.attr(fm.mid(x, y)) & 0x1FF]


def classify(fm):
    W, H = fm.w, fm.h
    g = [["#"] * W for _ in range(H)]
    floor_ids = Counter()
    for y in range(H):
        for x in range(W):
            b, solid, m = behaviour(fm, x, y), fm.coll(x, y), fm.mid(x, y)
            if b == "MB_SOUTH_ARROW_WARP":
                g[y][x] = "v"
            elif b == "MB_NON_ANIMATED_DOOR":
                g[y][x] = "D"
            elif b == "MB_LADDER":
                g[y][x] = "U" if (y > 0 and fm.coll(x, y - 1)) else "H"
            elif b == "MB_ROCK_STAIRS":
                g[y][x] = "S"
            elif b in ("MB_HOT_SPRINGS", "MB_POND_WATER", "MB_OCEAN_WATER", "MB_DEEP_WATER"):
                g[y][x] = "w"
            elif b == "MB_WATERFALL":
                g[y][x] = "f"
            elif b == "MB_JUMP_SOUTH":
                g[y][x] = "J"
            elif b == "MB_JUMP_WEST":
                g[y][x] = "<"
            elif b == "MB_MT_PYRE_HOLE":
                g[y][x] = "h"
            elif b == "MB_STRENGTH_BUTTON":
                g[y][x] = "b"
            elif not solid:
                g[y][x] = "."
                floor_ids[m] += 1
    # open cells that no warp reaches (outside the walls) are rock
    warps = [(w["x"], w["y"]) for w in fm.json.get("warp_events", [])]
    seen, q = set(warps), deque(warps)
    while q:
        cx, cy = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and g[ny][nx] in ".vSwfJ<hbHUD":
                seen.add((nx, ny))
                q.append((nx, ny))
    for y in range(H):
        for x in range(W):
            if g[y][x] in ".bh" and (x, y) not in seen:
                g[y][x] = "#"
    # detail floor: FRLG floor cells whose metatile is not the room's main floor id
    main = floor_ids.most_common(1)[0][0] if floor_ids else None
    for y in range(H):
        for x in range(W):
            if g[y][x] == "." and fm.mid(x, y) != main and floor_ids[fm.mid(x, y)] <= 6 \
                    and all(g[y + dy][x + dx] in ".*" for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0))
                            if 0 <= x + dx < W and 0 <= y + dy < H):   # not edge / shadow cells
                g[y][x] = "*"
    # loose rocks: solid lumps of <= 4 cells that do not touch the map edge and are walled by open cells
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
                    elif g[ny][nx] in "#DU" and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        q.append((nx, ny))
            if not edge and len(comp) <= 4:
                for cx, cy in comp:
                    g[cy][cx] = "B"
    # the same rock metatiles drawn against a wall are loose rocks too: FRLG ids that are mostly (>= 60%) seen as
    # free-standing lumps above
    lump, total = Counter(), Counter()
    for y in range(H):
        for x in range(W):
            if g[y][x] in "#B":
                total[fm.mid(x, y)] += 1
                if g[y][x] == "B":
                    lump[fm.mid(x, y)] += 1
    rocky = {m for m in lump if lump[m] >= 0.6 * total[m]}
    for y in range(H):
        for x in range(W):
            if g[y][x] == "#" and fm.mid(x, y) in rocky:
                g[y][x] = "B"
    return ["".join(r) for r in g]


# ================================================================================================ learning
_OFF5 = [(dx, dy) for dy in range(-2, 3) for dx in range(-2, 3)]
_OFF1 = [(0, 0), (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, -2), (0, 2), (-2, 0),
         (2, 0)]


def _at(R, x, y):
    return R[y][x] if 0 <= y < len(R) and 0 <= x < len(R[0]) else True


def sigs(R, x, y):
    s5 = tuple(_at(R, x + dx, y + dy) for dx, dy in _OFF5)
    s1 = tuple(_at(R, x + dx, y + dy) for dx, dy in _OFF1)
    s2 = vc._reduce(vc._sig(R, x, y))
    s3 = (R[y][x], _at(R, x, y - 1), _at(R, x - 1, y), _at(R, x + 1, y), _at(R, x, y + 1))
    return (("5", s5), ("1", s1), ("2", s2), ("3", s3))


_LEARN = {}


def learn(key):
    if key in _LEARN:
        return _LEARN[key]
    st = SETS[key]
    ts = st["pair"]
    rock_t, floor_t, vocab = {}, {}, Counter()
    for lid in st["train"] + st.get("alias", []):
        e, g = vc.raw_layout(lid)
        lts = (e["primary_tileset"], e["secondary_tileset"])
        assert lts == ts or lid in st.get("alias", []), (lid, lts, ts)
        sc = vc.scene(lts)

        def mb(m):
            a = sc.p.attrs[m] if m < 0x200 else sc.s.attrs[m - 0x200]
            return ft.MB[a & 0xFF]

        R = []
        for row in g:
            r = []
            for v in row:
                m, b = v & 0x3FF, mb(v & 0x3FF)
                rock = ((v >> 10) & 3 or b == "MB_MOUNTAIN_TOP") and b not in SPECIAL_MB and m not in st["exclude"] \
                    and m >= 0x200
                r.append(bool(rock))
            R.append(r)
        for y, row in enumerate(g):
            for x, v in enumerate(row):
                m = v & 0x3FF
                if R[y][x]:
                    vocab[m] += 1
                    tab = rock_t
                elif m in st["floor"] and not (v >> 10) & 3:
                    tab = floor_t
                else:
                    continue
                for lev, s in sigs(R, x, y):
                    tab.setdefault((lev, s), Counter())[m] += 1
    _LEARN[key] = (rock_t, floor_t, vocab)
    return _LEARN[key]


def pick(tab, R, x, y, default):
    for lev, s in sigs(R, x, y):
        c = tab.get((lev, s))
        if c:
            return c.most_common(1)[0][0], lev
    return default, "-"


# ================================================================================================ paint
def raw_of(mid, coll, elev, ts):
    sc = vc.scene(ts)
    assert (mid < len(sc.p.metatiles)) if mid < 0x200 else (mid - 0x200 < len(sc.s.metatiles)), hex(mid)
    return (elev << 12) | (coll << 10) | mid


def waterfall_piece(cls, x, y):
    top = y == 0 or cls[y - 1][x] != "f"
    if top:
        left = x == 0 or cls[y][x - 1] != "f"
        right = x + 1 >= len(cls[0]) or cls[y][x + 1] != "f"
        return 0x0BB if left else 0x0BC if right else 0x0B3
    return 0x0B9


def paint(fm, key, cls=None):
    st = SETS[key]
    ts = st["pair"]
    cls = cls or classify(fm)
    rock_t, floor_t, vocab = learn(key)
    W, H = fm.w, fm.h
    R = [[c not in OPEN_CLASSES for c in row] for row in cls]
    g = [[0] * W for _ in range(H)]
    levels = Counter()
    notes = []
    k_b = 0
    for y in range(H):
        for x in range(W):
            c = cls[y][x]
            coll, elev = fm.coll(x, y), fm.raw[y][x] >> 12
            if c in "#DU":
                m, lev = pick(rock_t, R, x, y, vocab.most_common(1)[0][0])
                levels[lev] += 1
            else:
                m, lev = pick(floor_t, R, x, y, st["floor"][0])
                if c == "*" and m == st["floor"][0]:
                    m = st["detail"][(x * 7 + y * 3) % len(st["detail"])]
            if c == "v":
                m = st["mat"]
            elif c == "D":
                m = st["door"]
            elif c == "U":
                m = st["up"]
            elif c == "H":
                m = st["down"]
            elif c == "S":
                m = st["stairs"]
            elif c == "B":
                m = st["boulder"][k_b % len(st["boulder"])]
                k_b += 1
            elif c == "J":
                m = st["ledge_s"]
            elif c == "<":
                m = st["ledge_w"]
            elif c == "h":
                m = st["hole"]
            elif c == "b":
                m = st["button"]
            elif c == "w":
                m = st["water_top"] if y > 0 and R[y - 1][x] else st["water"]
            elif c == "f":
                m = waterfall_piece(cls, x, y)
            g[y][x] = raw_of(m, coll, elev, ts)
    for y in range(1, H):                          # ladder against rock: its top piece in the face above
        for x in range(W):
            if cls[y][x] == "U" and st.get("up_top") and cls[y - 1][x] in "#DU":
                g[y - 1][x] = raw_of(st["up_top"], fm.coll(x, y - 1), fm.raw[y - 1][x] >> 12, ts)
    fm.report = dict(pair=ts, set=key, look=st["look"], classes=cls, sig_levels=dict(levels), notes=notes)
    return g


def seam_fix(g, cls, key, rounds=3):
    st = SETS[key]
    ts = st["pair"]
    rock_t, _f, vocab = learn(key)
    R = [[c not in OPEN_CLASSES for c in row] for row in cls]
    ignore = set(st["floor"]) | set(st["detail"]) | set(st["boulder"])
    changed = 0
    for _ in range(rounds):
        bad = vc.seams(g, ts, ignore=ignore)
        cells = set()
        for x, y, d, a, b in bad:
            for c in ((x, y), (x + (d == "E"), y + (d == "S"))):
                if cls[c[1]][c[0]] == "#":
                    cells.add(c)
        if not cells:
            break
        cand = {}
        cells = {c for c in cells if (g[c[1]][c[0]] & 0x3FF) in vc.uses(ts)}
        for (x, y) in cells:
            s2 = dict(sigs(R, x, y))
            pool = Counter()
            for lev in ("2", "3"):
                pool.update(rock_t.get((lev, s2[lev]), Counter()))
                if pool:
                    break
            cur = g[y][x] & 0x3FF
            used = vc.uses(ts)
            cand[(x, y)] = [cur] + [m for m, _ in pool.most_common(8) if m != cur and m in used]
        g2 = [r[:] for r in g]
        vc.solve(g2, cand, ts)
        for (x, y) in cells:                      # keep FRLG collision / elevation
            g2[y][x] = (g2[y][x] & 0x3FF) | (g[y][x] & ~0x3FF)
        if len(vc.seams(g2, ts, ignore=ignore)) >= len(bad):
            break
        changed += sum(1 for (x, y) in cells if g2[y][x] != g[y][x])
        g = g2
    return g, changed
