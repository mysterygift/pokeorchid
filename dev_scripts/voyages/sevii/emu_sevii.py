#!/usr/bin/env python3
"""
Headless checks for the Sevii maps (dev_scripts/mgba_headless; run with the Pillow venv, holding the voyages lock):

  while ! mkdir /tmp/voyages_mgba.lock 2>/dev/null; do sleep 5; done; trap 'rmdir /tmp/voyages_mgba.lock' EXIT
  bash dev_scripts/mgba_headless/harness_build.sh $PWD <dir>/h <copy of the user's save>   # then rebuild normally
  <venv python> dev_scripts/voyages/sevii/emu_sevii.py <dir>/h [test ...]

tests: towns centre ferry ice surf (default all). Screenshots -> dev_scripts/voyages/sevii/shots/.
"""
import json
import os
import struct
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mtattr as MA         # noqa: E402
import check_sevii as C     # noqa: E402
sys.path.insert(0, MA.P("dev_scripts", "mgba_headless"))
from gba import Emu         # noqa: E402

SHOTS = os.path.join(HERE, "shots")
GROUPS = json.load(open(MA.P("data", "maps", "map_groups.json")))
GROUP = GROUPS["group_order"].index("gMapGroup_Sevii")
NUM = {f: i for i, f in enumerate(GROUPS["gMapGroup_Sevii"])}
CHARS = {0x00: " ", 0xFE: "\n", 0xFA: "\n", 0xFB: "\n", 0xAD: ".", 0xB8: ",", 0xAB: "!", 0xAC: "?", 0xB4: "'",
         0xAE: "-", 0x1B: "e"}
for i in range(26):
    CHARS[0xBB + i] = chr(65 + i)
    CHARS[0xD5 + i] = chr(97 + i)
for i in range(10):
    CHARS[0xA1 + i] = chr(48 + i)
RESULTS = []


def log(ok, what):
    RESULTS.append((bool(ok), what))
    print(("PASS " if ok else "FAIL ") + what, flush=True)


class Game:
    def __init__(self, rom):
        self.e = Emu(rom + ".gba", rom + ".elf")

    def sb1(self):
        return self.e.r32("gSaveBlock1Ptr")

    def flag(self, fid):
        return (self.e.read(self.sb1() + 0x1270 + fid // 8, 1)[0] >> (fid % 8)) & 1

    def pos(self):
        x, y = struct.unpack("<hh", self.e.read(self.sb1(), 4))
        g, n = self.e.read(self.sb1() + 4, 2)
        return (x, y, g, n)

    def text(self):
        out = ""
        for c in self.e.read(self.e.sym("gStringVar4"), 0x100):
            if c == 0xFF:
                break
            out += CHARS.get(c, "?")
        return out

    def busy(self):
        return self.e.r8("sGlobalScriptContextStatus") != 2 or self.e.r8("sLockFieldControls") != 0

    def press(self, *k, after=12, hold=4):
        self.e.press(*k, after=after, hold=hold)

    def wait(self, n):
        self.e.frames(n)

    def step(self, d):
        self.e.press(d, hold=16, after=6)

    def step1(self, d):
        """exactly one tile (surfing moves 2 tiles per long hold): tap until the position changes"""
        p0 = self.pos()
        for _ in range(8):
            self.e.press(d, hold=3, after=10)
            if self.pos() != p0:
                break
        self.wait(6)

    def face(self, d):
        self.e.press(d, hold=2, after=8)

    def idle(self, maxpress=40, key="B"):
        for _ in range(maxpress):
            if not self.busy():
                return True
            self.press(key, after=20)
        return not self.busy()

    def shot(self, name):
        os.makedirs(SHOTS, exist_ok=True)
        self.e.shot(os.path.join(SHOTS, name + ".png"))

    def boot(self):
        e = self.e
        e.frames(400)
        e.press("START", after=120)
        e.press("A", after=240)
        e.press("A", after=300)
        e.press("B", after=40)
        e.press("START", after=40)
        e.press("A", after=60)
        for _ in range(4):
            e.press("B", after=30)
        self.idle()

    def warp(self, folder, warp=0):
        e = self.e
        e.press("R", "START", after=60)
        e.press("A", after=30)
        e.press("DOWN")
        e.press("A", after=30)
        for _ in range(GROUP):
            e.press("UP", after=4)
        e.press("A", after=20)
        for _ in range(NUM[folder]):
            e.press("UP", after=4)
        e.press("A", after=20)
        for _ in range(warp):
            e.press("UP", after=4)
        e.press("A", after=260)
        self.idle()
        return self.pos()


def path(folder, start, goal, surf=False):
    """BFS on the layout (collision, elevation, objects); water only with surf. Returns directions."""
    m = json.load(open(MA.P("data", "maps", folder, "map.json")))
    L = MA.Layout(m["layout"])
    objs = {(o["x"], o["y"]) for o in m["object_events"]}
    prev = {start: None}
    q = deque([start])
    D = {(0, -1): "UP", (0, 1): "DOWN", (-1, 0): "LEFT", (1, 0): "RIGHT"}
    while q:
        c = q.popleft()
        if c == goal:
            break
        for (dx, dy), name in D.items():
            n = (c[0] + dx, c[1] + dy)
            if n in prev or not L.inside(*n) or L.coll(*n) or n in objs:
                continue
            w1, w2 = C.is_water(L.beh(*c)), C.is_water(L.beh(*n))
            if w2 and not surf:
                continue
            e1, e2 = L.elev(*c), L.elev(*n)
            if not (e1 == e2 or e1 in (0, 15) or e2 in (0, 15) or w1 != w2):
                continue
            prev[n] = (c, name)
            q.append(n)
    if goal not in prev:
        return None
    out, c = [], goal
    while prev[c]:
        c, name = prev[c][0], prev[c][1]
        out.append(name)
    return out[::-1]


def walk_to(g, folder, goal, surf=False):
    x, y, _, _ = g.pos()
    p = path(folder, (x, y), goal, surf)
    if p is None:
        return False
    for d in p:
        g.step(d)
    return g.pos()[:2] == goal


# ------------------------------------------------------------------ tests
def t_towns(g):
    for i, (folder, const) in enumerate([("OneIsland", 0x264), ("TwoIsland", 0x265), ("ThreeIsland", 0x266),
                                         ("FourIsland", 0x267), ("FiveIsland", 0x268), ("SixIsland", 0x269),
                                         ("SevenIsland", 0x26A)]):
        p = g.warp(folder, 0)
        g.wait(30)
        g.shot("town_%d_%s" % (i + 1, folder))
        log(p[2:] == (GROUP, NUM[folder]) and g.flag(const), "%s: warped in at %s, FLAG_VISITED set=%d" % (
            folder, p[:2], g.flag(const)))


def t_centre(g):
    p = g.warp("OneIsland_PokemonCenter_1F", 0)
    party = g.e.r32("gPlayerPartyPtr")
    g.e.write(party + 0x56, b"\x01\x00")
    hp0 = g.e.r16(party + 0x56)
    ok = walk_to(g, "OneIsland_PokemonCenter_1F", (7, 4))
    g.face("UP")
    g.shot("centre_one_island_net_center")
    g.press("A", after=80)
    for _ in range(30):
        if not g.busy():
            break
        g.press("A", after=40)
    hp1 = g.e.r16(party + 0x56)
    log(ok and hp1 > hp0, "Net Center nurse heals: lead HP %d -> %d (walked to counter: %s)" % (hp0, hp1, ok))
    g.idle()
    # leave through the door: back on One Island in front of the Centre
    walk_to(g, "OneIsland_PokemonCenter_1F", (7, 9))
    g.step("DOWN")
    g.wait(120)
    g.idle()
    q = g.pos()
    log(q[2:] == (GROUP, NUM["OneIsland"]) and q[:2] == (14, 6), "Centre exit lands on One Island %s" % (q[:2],))
    g.shot("centre_exit_one_island")


def t_ferry(g):
    p = g.warp("OneIsland_Harbor", 1)
    log(p[:2] == (8, 4), "arrival point MAP_ONE_ISLAND_HARBOR warp 1 = %s" % (p[:2],))
    g.shot("ferry_0_one_island_dock")
    g.face("DOWN")
    g.press("A", after=90)
    g.shot("ferry_1_menu")
    for _ in range(2):                       # Two, Three, [Four]
        g.press("DOWN", after=10)
    g.press("A", after=60)
    for _ in range(40):
        x, y, gg, n = g.pos()
        if (gg, n) == (GROUP, NUM["FourIsland_Harbor"]):
            break
        g.press("A", after=30)
    g.wait(120)
    g.idle()
    q = g.pos()
    g.shot("ferry_2_arrived_four_island")
    log(q == (8, 4, GROUP, NUM["FourIsland_Harbor"]), "ferry One -> Four Island harbour: %s" % (q,))
    # walk out onto Four Island
    walk_to(g, "FourIsland_Harbor", (8, 3))
    g.step("UP")
    g.wait(120)
    g.idle()
    r = g.pos()
    g.shot("ferry_3_four_island")
    log(r[2:] == (GROUP, NUM["FourIsland"]), "harbour door -> Four Island %s" % (r[:2],))


def t_ice(g):
    p = g.warp("FourIsland_IcefallCave_B1F", 2)
    ok = walk_to(g, "FourIsland_IcefallCave_B1F", (17, 14))
    g.shot("icefall_b1f_0_before")
    g.press("UP", hold=4, after=90)
    q = g.pos()
    g.shot("icefall_b1f_1_slid")
    log(ok and q[:2] == (17, 10), "Icefall B1F: one UP from (17,14) slides to %s (expect (17,10))" % (q[:2],))


def t_surf(g):
    """Harness ROM from harness_test_build.sh (party 'knows' Surf); badge 5 set in memory. Surf off Two Island's
    dock and west across the connection into Sevii Sea Route A (One-Two Strait)."""
    p = g.warp("TwoIsland", 3)                  # harbour door (10,8) on the dock
    # no wild battles on the crossing (encounters themselves are checked by the shot wild_*.png): lead level 100
    # + Repel steps
    party = g.e.r32("gPlayerPartyPtr")
    g.e.w8(party + 0x54, 100)
    g.e.write(g.sb1() + 0x139C + (0x4021 - 0x4000) * 2, struct.pack("<H", 250))
    a = g.sb1() + 0x1270 + 0x86B // 8
    g.e.w8(a, g.e.r8(a) | (1 << (0x86B % 8)))
    g.step1("LEFT")                              # (9,8), water to the west
    g.face("LEFT")
    g.press("A", after=60)
    g.shot("surf_0_prompt")
    g.press("A", after=60)                      # yes
    for _ in range(10):
        if not g.busy():
            break
        g.press("A", after=40)
    g.wait(60)
    surfing = bool(g.e.r8("gPlayerAvatar") & 8)
    log(surfing, "Surf started off Two Island's dock at %s" % (g.pos()[:2],))
    x, y = g.pos()[:2]
    full = path("TwoIsland", (x, y), (0, 4), surf=True)
    for d in full or []:
        g.step1(d)
    g.shot("surf_1_two_island_west")
    for _ in range(4):
        g.step1("LEFT")
    g.wait(60)
    q = g.pos()
    g.shot("surf_2_sea_route_a")
    log(q[2:] == (GROUP, NUM["SeviiSeaRouteA"]), "Surf west from Two Island into One-Two Strait (Sea Route A): %s" % (q,))
    # sail the whole strait to Kindle Road's east coast (route is walled by sea rocks)
    m = json.load(open(MA.P("data", "maps", "SeviiSeaRouteA", "map.json")))
    L = MA.Layout(m["layout"])
    x, y = q[:2]
    goals = [(0, yy) for yy in range(L.h) if not L.coll(0, yy)]
    for _ in range(6):                          # swimmers wander: re-plan from wherever we are
        x, y, gg, n = g.pos()
        if (gg, n) != (GROUP, NUM["SeviiSeaRouteA"]) or x == 0:
            break
        route = next((r for r in (path("SeviiSeaRouteA", (x, y), gl, surf=True) for gl in goals) if r), None)
        for d in route or []:
            g.step1(d)
    for _ in range(3):
        g.step1("LEFT")
    g.wait(60)
    r = g.pos()
    g.shot("surf_3_kindle_road")
    log(r[2:] == (GROUP, NUM["OneIsland_KindleRoad"]), "...and on across the strait to Kindle Road: %s" % (r,))


def t_ember(g):
    """Mt. Ember's FRLG arrow warps are coord triggers on shared Lavaridge ash (facing-checked)."""
    p = g.warp("OneIsland_KindleRoad", 0)       # arrow N (11,6)
    g.face("UP")
    g.press("UP", hold=16, after=150)
    g.idle()
    q = g.pos()
    g.shot("ember_0_arrived_from_kindle_road")
    log(q[2:] == (GROUP, NUM["MtEmber_Exterior"]), "Kindle Road arrow N -> Mt. Ember %s" % (q,))
    g.step("UP")
    g.step("DOWN")                               # back onto (28,48) facing south: trigger
    g.wait(150)
    g.idle()
    r = g.pos()
    log(r[2:] == (GROUP, NUM["OneIsland_KindleRoad"]), "Mt. Ember (28,48) heading south -> Kindle Road %s" % (r,))


def t_stall(g):
    p = g.warp("TwoIsland", 2)                  # Centre door (21,7)
    ok = walk_to(g, "TwoIsland", (28, 5))
    g.face("UP")
    g.press("A", after=60)
    for _ in range(3):
        g.press("A", after=60)                  # welcome -> BUY
    g.wait(60)
    mult = g.e.r16(g.e.r32("gSaveBlock1Ptr") + 0x139C + (0x409B - 0x4000) * 2)
    g.shot("stall_two_island_market")
    log(ok and mult == 3, "Two Island market stall open, VAR_SHOP_PRICE_MULTIPLIER=%d" % mult)
    for _ in range(6):
        g.press("B", after=40)
    g.idle()
    mult = g.e.r16(g.e.r32("gSaveBlock1Ptr") + 0x139C + (0x409B - 0x4000) * 2)
    log(mult == 0, "multiplier reset after the stall closes (%d)" % mult)


def t_gamecorner(g):
    p = g.warp("TwoIsland_JoyfulGameCorner", 0)
    g.wait(30)
    g.shot("joyful_game_corner")
    log(p[2:] == (GROUP, NUM["TwoIsland_JoyfulGameCorner"]), "Joyful Game Corner interior %s" % (p,))
    g.step("DOWN")
    g.step("DOWN")
    g.wait(120)
    g.idle()
    q = g.pos()
    log(q[2:] == (GROUP, NUM["TwoIsland"]), "Game Corner exit -> Two Island %s" % (q,))
    g.shot("joyful_game_corner_exterior")


def t_warehouse(g):
    """Rocket Warehouse: the Sevii-only animated door (field_door.c entry for gTileset_SeviiIslands)."""
    p = g.warp("FiveIsland_Meadow", 0)
    g.step("DOWN")
    g.wait(20)
    g.shot("warehouse_0_door")
    for _ in range(4):
        if g.pos()[2:] != (GROUP, NUM["FiveIsland_Meadow"]):
            break
        g.e.press("UP", hold=12, after=10)
        if g.pos()[1] == 22:
            g.shot("warehouse_1_door_opening")
    g.wait(150)
    g.idle()
    q = g.pos()
    g.shot("warehouse_2_inside")
    log(q[2:] == (GROUP, NUM["FiveIsland_RocketWarehouse"]), "Rocket Warehouse door -> interior %s" % (q,))


TESTS = {"towns": t_towns, "centre": t_centre, "ferry": t_ferry, "ice": t_ice, "surf": t_surf, "ember": t_ember, "stall": t_stall, "gamecorner": t_gamecorner, "warehouse": t_warehouse}


def main():
    rom = sys.argv[1]
    which = sys.argv[2:] or list(TESTS)
    g = Game(rom)
    try:
        g.boot()
        for t in which:
            try:
                TESTS[t](g)
            except Exception as ex:          # keep going, report
                log(False, "%s crashed: %r" % (t, ex))
    finally:
        g.e.close()
    json.dump(RESULTS, open(os.path.join(SHOTS, "results_%s.json" % "_".join(which)), "w"), indent=1)
    print("%d/%d passed" % (sum(r[0] for r in RESULTS), len(RESULTS)))


if __name__ == "__main__":
    main()
