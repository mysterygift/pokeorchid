"""The Cold Storage test map: layout, puzzle solver, painter and previews.

One grid of characters is the single source for the collision map, the metatiles, the puzzle
check (--solve) and the setmetatile lists the map script needs (melt / refreeze / gate).

    X  wall (drawn automatically)      .  deck            ~  ice (MB_ICE)
    m  ice that thaws when the coolant is switched off     #  container (see CONTAINERS)
    c b o a  crate / ice block / barrel / cone on deck     C B O A  the same on ice
    f  fish boxes   w  wet-floor sign   h  hazard deck   r  frosty deck   d  drain
    G  locked gate  S  coolant console  E  exit mat (warp)
"""
import os
import struct
from collections import deque

from PIL import Image

import kit
from kit import ROOT, OUT

LAYOUT_DIR = os.path.join(ROOT, "data", "layouts", "ColdStorageTest")

GRID = """
XXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXX
Xff...............ccoX
Xf.................c.X
X....................X
X#####..........#####X
X#########h##########X
X#########G##########X
X~~~~~~~##.##~~~~~~~~X
X~~~~~~~##m#####~~~~~X
X~~B~~~~##m#####S~~~~X
X~~~~~~Cmmmmmmmm...~~X
X~~~~~##########...~~X
X~~~~~##########~~~~BX
X~~~~~~~~~~~~~~~~A~~~X
X###.################X
X###.################X
X....................X
X.######.##.#########X
X.######.##.#########X
X........##....c~~~C.X
X######..##.##..B~~~~X
X######.....##..~~O~~X
X.......###.##..#####X
X.......###.##..#####X
X##############.#####X
X##############.#####X
X~~C~~~~~B~~~~~~~~~~~X
X~~~~~~~~~~~~~~~~~~~~X
X~~~~~A~~~~~~~~~~~~~~X
X.~~~~~~~~B~~~~~~~~~~X
X~~C~~~~~~~~~~~~~~~~~X
X~~~~B~~~~~~~~~~A~~~~X
X#########hh#########X
X#########..#########X
Xcc....r....r.....ffoX
Xc...............w..fX
X....................X
XXXXXXXXXXEEXXXXXXXXXX
""".strip().split("\n")
W, H = len(GRID[0]), len(GRID)
assert all(len(r) == W for r in GRID), [len(r) for r in GRID]

# (colour, kind, x, y, size): kind H = lying east-west 2 rows deep, T = stacked (3 rows),
# V = lying north-south, 2 wide. size = width for H/T, height for V.
CONTAINERS = [
    ("Navy", "T", 1, 6, 5), ("Rust", "H", 6, 7, 4), ("Amber", "H", 11, 7, 5), ("Green", "T", 16, 6, 5),
    ("Green", "V", 8, 9, 3), ("Rust", "V", 11, 9, 3), ("Navy", "H", 13, 10, 3),
    ("Amber", "H", 6, 13, 5), ("Rust", "H", 11, 13, 5),
    ("Green", "H", 1, 16, 3), ("Navy", "H", 5, 16, 6), ("Amber", "H", 11, 16, 5), ("Rust", "H", 16, 16, 5),
    ("Rust", "H", 2, 19, 6), ("Amber", "V", 9, 19, 4), ("Green", "H", 12, 19, 5), ("Navy", "H", 17, 19, 4),
    ("Amber", "H", 1, 22, 6), ("Navy", "V", 12, 22, 4),
    ("Green", "H", 8, 24, 3), ("Rust", "H", 16, 24, 5),
    ("Navy", "H", 1, 26, 5), ("Green", "H", 6, 26, 4), ("Rust", "H", 10, 26, 5), ("Amber", "H", 16, 26, 5),
    ("Rust", "H", 1, 34, 5), ("Amber", "H", 6, 34, 4), ("Green", "H", 12, 34, 4), ("Navy", "H", 16, 34, 5),
]
FROSTED = {(3, 6), (18, 6), (7, 16), (13, 16), (4, 19), (14, 19), (3, 26), (12, 26), (18, 26),
           (3, 34), (13, 34), (8, 13), (13, 13)}                # H roof tiles with a snow crust
ICICLES = {(2, 8), (8, 8), (13, 8), (18, 8), (7, 14), (12, 14), (9, 17), (18, 17), (5, 20), (19, 20),
           (4, 27), (11, 27), (19, 27), (2, 35), (17, 35)}      # H face tiles with icicles
LABELLED = {(3, 8), (7, 8), (12, 8), (17, 8), (9, 14), (14, 14), (2, 17), (6, 17), (14, 17), (4, 20),
            (15, 20), (3, 23), (17, 25), (8, 27), (17, 27), (4, 35), (7, 35), (14, 35), (18, 35)}
WALL_RUN = ["Wall", "Wall_Pipes", "Wall_Pipes", "Wall_Frost", "Wall_Vent", None, "Wall", "Wall_Pipes",
            "Wall_Gauge", "Wall", "Wall", "Wall_Gauge", "Wall_Pipes", "Wall_Vent", None, "Wall_Frost",
            "Wall_Pipes", "Wall_Pipes", "Wall", "Wall_Frost"]

# ---- events (also read by gen_events.py) ------------------------------------------------
GATE, CONSOLE, GATE_STAND, CONSOLE_STAND = (10, 8), (16, 11), (10, 9), (16, 12)
TRIGGER = (10, 7)
KEY_BALL = (20, 21)
ITEM_BALLS = {KEY_BALL: "key", (1, 31): "field1", (1, 25): "maze"}
NPCS = {                                    # static people: block movement in the solver
    "aide": (8, 37), "grunt1": (11, 19), "grunt2": (3, 18), "grunt3": (4, 24), "grunt4": (18, 13),
    "leader": (10, 3), "admin": (11, 3), "haru": (11, 5),
}
ENTRY = (10, 38)
# trainer: (facing, sight range). After spotting the player a trainer walks up to them and stays
# there until the map reloads, so report() re-checks the puzzle with each trainer parked on every
# cell of its sight line. Grunt 2 only sees the tile in front of it: with a longer range it stops
# in the one-tile corridor that leads to the gap in the container row. Grunt 1 has range 2 so it
# can never park on the (11, 21) junction, the only link between the two halves of the maze.
TRAINERS = {"grunt1": ("DOWN", 2), "grunt2": ("RIGHT", 1), "grunt3": ("RIGHT", 3), "grunt4": ("LEFT", 2)}
FACING = {"DOWN": (0, 1), "UP": (0, -1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


def trainer_stops(name):
    """Cells the trainer can end up on: every walkable cell of its sight line except the last
    one in range (it stops one short of the player)."""
    (x, y), (facing, rng) = NPCS[name], TRAINERS[name]
    dx, dy = FACING[facing]
    out = []
    for i in range(1, rng):
        p = (x + dx * i, y + dy * i)
        if cell(*p) not in WALKABLE:
            break
        out.append(p)
    return out

PROPS = {"c": "Crate", "b": "IceBlock", "o": "Barrel", "a": "Cone",
         "C": "Crate_OnIce", "B": "IceBlock_OnIce", "O": "Barrel_OnIce", "A": "Cone_OnIce",
         "f": "FishBoxes", "w": "WetSign", "G": "Gate", "S": "Console_On"}
WALKABLE = set(".~mhrdE")
ICE = set("~m")


def cell(x, y):
    return GRID[y][x] if 0 <= x < W and 0 <= y < H else "X"


def container_cells():
    """{(x, y): metatile label} for every container tile; checks the list against the '#'s."""
    out = {}
    for colour, kind, x0, y0, size in CONTAINERS:
        if kind in "HT":
            rows = ("Top", "Mid", "Bot") if kind == "T" else ("Top", "Bot")
            for ry, row in enumerate(rows):
                for cx in range(size):
                    col = "L" if cx == 0 else "R" if cx == size - 1 else "M"
                    p = (x0 + cx, y0 + ry)
                    lab = f"{colour}_H_{row}_{col}"
                    if col == "M" and row == "Top" and p in FROSTED:
                        lab += "_Frost"
                    if col == "M" and row == "Bot" and p in ICICLES:
                        lab += "_Icicles"
                    elif col == "M" and row == "Bot" and p in LABELLED:
                        lab += "_Label"
                    assert p not in out, f"containers overlap at {p}"
                    out[p] = lab
        else:
            rows = ["Top"] + ["Mid"] * (size - 3) + ["FaceA", "FaceB"]
            for ry, row in enumerate(rows):
                for cx, col in enumerate("LR"):
                    p = (x0 + cx, y0 + ry)
                    assert p not in out, f"containers overlap at {p}"
                    out[p] = f"{colour}_V_{row}_{col}"
    marked = {(x, y) for y in range(H) for x in range(W) if GRID[y][x] == "#"}
    assert set(out) == marked, f"containers vs '#': only in list {sorted(set(out) - marked)}, " \
                               f"only in grid {sorted(marked - set(out))}"
    return out


def casts_shadow(x, y):
    ch = cell(x, y)
    return ch == "#" or (ch == "X" and y == 2)


def floor_label(x, y, base):
    n = casts_shadow(x, y - 1)
    w = cell(x - 1, y) == "#"
    suffix = {(False, False): "", (True, False): "_ShadeN", (False, True): "_ShadeW", (True, True): "_ShadeNW"}[(n, w)]
    if base == "Ice" and not suffix and (x * 7 + y * 3) % 5 == 0:
        return "Ice_B"
    return base + suffix


def build():
    """Returns (grid of metatile labels, grid of walkable flags)."""
    boxes = container_cells()
    g = [[None] * W for _ in range(H)]
    walk = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            ch = GRID[y][x]
            walk[y][x] = ch in WALKABLE
            if ch == "X":
                if y == 0:
                    lab = "Cap_NW" if x == 0 else "Cap_NE" if x == W - 1 else "Cap_N"
                elif y == H - 1:
                    lab = "Cap_SW" if x == 0 else "Cap_SE" if x == W - 1 else "Cap_S"
                elif x == 0:
                    lab = "Cap_W"
                elif x == W - 1:
                    lab = "Cap_E"
                else:
                    kind, side = WALL_RUN[x - 1], ""
                    if kind is None:
                        kind, side = WALL_RUN[x - 2], "_R"
                    elif kind == "Wall_Vent":
                        side = "_L"
                    lab = f"{kind}_{'Upper' if y == 1 else 'Lower'}{side}"
            elif ch == "#":
                lab = boxes[(x, y)]
            elif ch in PROPS:
                lab = PROPS[ch]
            elif ch in ICE:
                lab = floor_label(x, y, "Ice")
            elif ch == "h":
                lab = "Floor_Hazard"
            elif ch == "r":
                lab = "Floor_Frost"
            elif ch == "d":
                lab = "Floor_Drain"
            elif ch == "E":
                lab = "Exit"
            else:
                lab = floor_label(x, y, "Floor")
            g[y][x] = lab
    return g, walk


def melt_cells():
    """[(x, y, frozen label, thawed label)] for the 'm' cells."""
    out = []
    for y in range(H):
        for x in range(W):
            if GRID[y][x] == "m":
                frozen = floor_label(x, y, "Ice")
                frozen = "Ice" if frozen == "Ice_B" else frozen
                out.append((x, y, frozen, frozen.replace("Ice", "Wet")))
    return out


def paint_layout(ID):
    g, walk = build()
    os.makedirs(LAYOUT_DIR, exist_ok=True)
    blocks = [ID[lab] | (0x3000 if w else 0x0400) for row, wrow in zip(g, walk) for lab, w in zip(row, wrow)]
    with open(os.path.join(LAYOUT_DIR, "map.bin"), "wb") as f:
        f.write(struct.pack(f"<{W * H}H", *blocks))
    with open(os.path.join(LAYOUT_DIR, "border.bin"), "wb") as f:
        f.write(struct.pack("<4H", *([ID["Void"] | 0x0400] * 4)))


# ------------------------------------------------------------------ puzzle check
DIRS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}


def solve(moved=None):
    """BFS over (position, key?, thawed?, gate open?, bonus balls taken). Returns a dict of facts.
    `moved` = {npc name: cell} overrides where people stand."""
    npcs = set(dict(NPCS, **(moved or {})).values())

    def passable(p, st):
        _, key, thawed, gate, taken = st
        ch = cell(*p)
        if p in npcs:
            return False
        if p in ITEM_BALLS and ITEM_BALLS[p] not in taken:
            return False
        if p == GATE:
            return gate
        return ch in WALKABLE

    def slippery(p, st):
        ch = cell(*p)
        return ch == "~" or (ch == "m" and not st[2])

    def moves(st):
        pos, key, thawed, gate, taken = st
        for d, (dx, dy) in DIRS.items():
            p = (pos[0] + dx, pos[1] + dy)
            if not passable(p, st):
                continue
            while slippery(p, st):
                q = (p[0] + dx, p[1] + dy)
                if not passable(q, st):
                    break
                p = q
            yield d, (p, key, thawed, gate, taken)
        for b, name in ITEM_BALLS.items():                # pick up an adjacent ball
            if name not in taken and abs(b[0] - pos[0]) + abs(b[1] - pos[1]) == 1:
                yield f"[take {name}]", (pos, key or name == "key", thawed, gate, taken | {name})
        if pos == CONSOLE_STAND:
            yield "[console]", (pos, key, not thawed, gate, taken)
        if pos == GATE_STAND and key and not gate:
            yield "[unlock]", (pos, key, thawed, True, taken)

    start = (ENTRY, False, False, False, frozenset())
    prev, order = {start: None}, deque([start])
    while order:
        st = order.popleft()
        for label, nxt in moves(st):
            if nxt not in prev:
                prev[nxt] = (st, label)
                order.append(nxt)

    def route(st):
        out = []
        while prev[st]:
            st, label = prev[st]
            out.append(label)
        return out[::-1]

    goals = [st for st in prev if st[0] == TRIGGER]
    assert goals, f"the boss room cannot be reached (moved: {moved})"
    best = min(goals, key=lambda st: len(route(st)))
    # softlock check: from every reachable state the goal must still be reachable
    rev = {}
    for st in prev:
        for _, nxt in moves(st):
            rev.setdefault(nxt, []).append(st)
    good, order = set(goals), deque(goals)
    while order:
        st = order.popleft()
        for p in rev.get(st, []):
            if p not in good:
                good.add(p)
                order.append(p)
    stuck = [st for st in prev if st not in good]
    return dict(states=len(prev), route=route(best), stuck=stuck, prev=prev,
                first=lambda pred: route(min((s for s in prev if pred(s)), key=lambda s: len(route(s)))))


def compress(route):
    out, run = [], ""
    for step in route:
        if len(step) == 1:
            run += step
        else:
            if run:
                out.append(run)
            run = ""
            out.append(step)
    if run:
        out.append(run)
    return " ".join(out)


def report():
    r = solve()
    print(f"reachable states: {r['states']}; states with no way forward: {len(r['stuck'])}")
    for st in r["stuck"][:5]:
        print("   stuck:", st)
    print("shortest full route (each letter is one input; slides are one input):")
    print("  ", compress(r["route"]))
    print("to the key:        ", compress(r["first"](lambda s: s[1])))
    print("to the console:    ", compress(r["first"](lambda s: s[0] == CONSOLE_STAND)))
    for name in ("field1", "maze"):
        print(f"to the {name} item: ", compress(r["first"](lambda s, n=name: n in s[4])))
    for name in TRAINERS:
        for stop in trainer_stops(name):
            v = solve({name: stop})
            verdict = "ok" if not v["stuck"] else f"{len(v['stuck'])} STUCK STATES"
            print(f"{name} parked at {stop}: {verdict}, route {len(v['route'])} inputs")


# ------------------------------------------------------------------ previews
PEOPLE = "graphics/object_events/pics/people/"
PALS = "graphics/object_events/palettes/"


def render(packer, data, ID, thawed=False, people=None):
    g, _ = build()
    thaw = {(x, y): t for x, y, _, t in melt_cells()} if thawed else {}
    im = Image.new("RGBA", (W * 16, H * 16), (0, 0, 0, 255))
    for y in range(H):
        for x in range(W):
            lab = thaw.get((x, y), g[y][x])
            if thawed and lab == "Console_On":
                lab = "Console_Off"
            im.alpha_composite(packer.render_metatile(data[ID[lab] - kit.SECONDARY_METATILE_BASE]), (x * 16, y * 16))
    for png, pal, frame, (tx, ty), hf in sorted(people or [], key=lambda n: n[3][1]):
        try:
            s = kit.sprite(PEOPLE + png, PALS + pal, frame, hflip=hf)
        except FileNotFoundError as e:
            print("  (preview) missing sprite:", e.filename)
            continue
        im.alpha_composite(s, (tx * 16, ty * 16 - 16))
    return im


def previews(packer, data, ID):
    people = [
        ("team_aqua/aqua_member_m.png", "npc_4.pal", 0, NPCS["grunt1"], False),
        ("team_aqua/aqua_member_f.png", "npc_4.pal", 2, NPCS["grunt2"], True),
        ("team_aqua/aqua_member_m.png", "npc_4.pal", 2, NPCS["grunt3"], True),
        ("team_aqua/aqua_member_f.png", "npc_4.pal", 2, NPCS["grunt4"], False),
        ("scientist_1.png", "npc_4.pal", 1, NPCS["aide"], False),
        ("wally.png", "npc_2.pal", 1, NPCS["haru"], False),
        ("brendan/walking.png", "brendan.pal", 1, (10, 31), False),
    ]
    full = render(packer, data, ID, people=people)
    full.save(os.path.join(OUT, "cold_storage_test_1x.png"))
    kit.up(full, 2).save(os.path.join(OUT, "cold_storage_test_2x.png"))
    for name, (tx, ty), thawed in (("camera_entrance", (10, 36), False), ("camera_field1", (10, 30), False),
                                   ("camera_maze", (13, 22), False), ("camera_field2", (12, 12), False),
                                   ("camera_field2_thawed", (12, 12), True), ("camera_boss", (10, 5), False)):
        src = render(packer, data, ID, thawed=True, people=people) if thawed else full
        ox = max(0, min(W * 16 - 240, tx * 16 - 112))
        oy = max(0, min(H * 16 - 160, ty * 16 - 72))
        kit.up(src.crop((ox, oy, ox + 240, oy + 160))).save(os.path.join(OUT, f"{name}_3x.png"))
