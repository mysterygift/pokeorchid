"""Shared helpers for the Wavebreak Voyages end-to-end headless run (Pillow venv). Built on core/emu_lib.py and
the core stream's scratch helpers (code entry via the naming screen, sailing, battles). The harness ROM comes from
hbuild.sh (debug flags 0x29D no trainer sight, 0x29E no wild encounters, 0x29F no collision)."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from emu_lib import Game, FLAGS, FLAG_SYS_GAME_CLEAR  # noqa: E402,F401

SHOTS = os.path.join(HERE, "..", "shots")
FLAG_NO_SEE, FLAG_NO_WILD, FLAG_NO_COLLIDE = 0x29D, 0x29E, 0x29F
FLAG_SYS_POKENAV_GET, FLAG_SYS_PHONE_ACTIVE = 0x862, 0x863
FLAG_VISITED_TIKSI = None          # looked up from the ELF-less constants below
MENU_ACTION_PHONE = 3
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def enc(s):
    out = []
    for c in s:
        if "A" <= c <= "Z":
            out.append(0xBB + ord(c) - 65)
        elif "a" <= c <= "z":
            out.append(0xD5 + ord(c) - 97)
    return bytes(out)


class E2E(Game):
    def __init__(self, rom):
        super().__init__(rom)
        self.shot_n = 0

    # ---- state
    def cb2(self):
        return self.e.r32(self.e.sym("gMain") + 4) & ~1

    def at_cb2(self, name):
        return self.cb2() == (self.e.sym(name) & ~1)

    def wait_cb2(self, name, maxf=1500):
        for _ in range(maxf // 10):
            if self.at_cb2(name):
                return True
            self.wait(10)
        return False

    def snap(self, name):
        self.wait(20)
        os.makedirs(SHOTS, exist_ok=True)
        p = self.e.shot(os.path.join(SHOTS, name + ".png"))
        log("  shot", name, self.pos())
        return p

    def until_text(self, sub, maxa=12, after=45):
        for _ in range(maxa):
            if sub in self.text():
                self.wait(40)
                return True
            self.press("A", after=after)
        return sub in self.text()

    def field(self, maxa=40):
        for _ in range(maxa):
            if self.at_cb2("CB2_Overworld") and not self.script_running():
                return True
            self.press("B", after=40)
        return False

    # ---- walking (no-collision harness: straight lines are fine)
    def walk_to(self, x, y):
        for _ in range(4):
            cx, cy, _, _ = self.pos()
            if (cx, cy) == (x, y):
                return True
            if cx != x:
                self.walk("RIGHT" if x > cx else "LEFT", abs(x - cx))
            cx, cy, _, _ = self.pos()
            if cy != y:
                self.walk("DOWN" if y > cy else "UP", abs(y - cy))
            self.wait(10)
        ok = self.pos()[:2] == (x, y)
        if not ok:
            log("  walk_to", (x, y), "ended at", self.pos())
        return ok

    # ---- sailor
    def menu_pick(self, n):
        for _ in range(n):
            self.press("DOWN", after=8)
        self.press("A", after=40)

    def to_menu(self):
        return self.until_text("Where are we headed")

    def enter_code(self, idx, code):
        self.menu_pick(idx)
        self.until_text("A passcode")
        self.wait(30)
        self.press("A", after=40)
        ok = self.wait_cb2("CB2_NamingScreen")
        self.wait(60)
        ns = self.e.r32("sNamingScreen")
        self.e.write(ns + 0x1800, enc(code) + b"\xff" * (16 - len(code)))
        self.press("START", after=20)
        self.press("A", after=20)
        self.wait_cb2("CB2_Overworld")
        self.wait(90)
        return ok, self.text()

    def sail(self, idx, shot=None, first_text="Where are we headed"):
        """already facing the Sailor: talk -> menu idx -> yes -> cutscene -> arrive"""
        self.press("A", after=60)
        self.until_text(first_text)
        if shot:
            self.snap(shot + "_menu")
        self.menu_pick(idx)
        self.wait(30)
        t = self.text()
        if "Set sail" not in t:
            log("  sail: unexpected text", repr(t[:60]))
            return None
        self.press("A", after=60)
        self.press("A", after=60)
        if not self.wait_cb2("MainCB2_SeaGallop"):
            log("  sail: no cutscene")
            return None
        self.wait(60)
        if shot:
            self.snap(shot + "_scene")
        self.wait_cb2("CB2_Overworld", 3000)
        self.wait(150)
        self.until_idle()
        return self.pos()

    # ---- phone MAP
    def open_phone_map(self, shot):
        """START -> PHONE -> MAP; screenshot; back to the field. Returns header info read from RAM."""
        self.field()
        self.press("START", after=40)
        n = self.e.r8("sNumStartMenuActions")
        acts = list(self.e.read(self.e.sym("sCurrentStartMenuActions"), n))
        if MENU_ACTION_PHONE not in acts:
            log("  phone not in start menu", acts)
            self.press("B", after=30)
            return False
        cur = self.e.r8("sStartMenuCursorPos")
        tgt = acts.index(MENU_ACTION_PHONE)
        for _ in range((tgt - cur) % n):
            self.press("DOWN", after=8)
        self.e.write(self.e.sym("sLastCursor"), b"\x00")
        self.press("A", after=90)
        self.wait(60)
        self.press("A", after=30)               # MAP app
        ok = self.wait_cb2("MCB2_FieldUpdateRegionMap", 900)
        self.wait(90)
        self.snap(shot)
        rm = self.e.r32("sFieldRegionMapHandler")
        # RegionMap is embedded; mapSecId is its first u16 (struct RegionMap at handler+? -> read via symbol below)
        info = {"ok": ok}
        try:
            info["viewed"] = self.e.r8("sViewedRegionMapType")
        except Exception:
            pass
        self.press("B", after=60)
        self.wait(60)
        for _ in range(6):
            if self.at_cb2("CB2_Overworld"):
                break
            self.press("B", after=60)
        self.field()
        return info

    # ---- battles
    def in_battle(self):
        return self.at_cb2("BattleMainCB2")

    def wait_battle(self, maxf=3000):
        for _ in range(maxf // 20):
            if self.in_battle():
                return True
            self.wait(20)
        return False

    def foe(self):
        b = self.e.sym("gBattleMons") + 140
        d = self.e.read(b, 0x30)
        return struct.unpack_from("<H", d, 0)[0]

    def song(self):
        """id of the song the BGM player is playing (gMPlayInfo_BGM.songHeader looked up in gSongTable)"""
        if not hasattr(self, "_songs"):
            base, self._songs = self.e.sym("gSongTable"), {}
            raw = b""
            for off in range(0, 700 * 8, 0x100):
                raw += self.e.read(base + off, 0x100)
            for i in range(len(raw) // 8):
                self._songs.setdefault(struct.unpack_from("<I", raw, i * 8)[0], i)
        return self._songs.get(self.e.r32("gMPlayInfo_BGM"))

    def win(self, maxrounds=12):
        """foe HP -> 1 each turn and use the first move until the battle ends"""
        for _ in range(3):
            self.press("B", after=60)
        for _ in range(maxrounds):
            if not self.in_battle():
                break
            for k in range(2):           # both foe slots (singles: slot 1)
                b = self.e.sym("gBattleMons") + 140 * (1 + 2 * k)
                hp = struct.unpack("<H", self.e.read(b + 0x28, 2))[0]
                if hp > 1:
                    self.e.write(b + 0x28, b"\x01\x00")
            self.press("A", after=30)
            self.press("A", after=200)
            for _ in range(8):
                if not self.in_battle():
                    break
                self.press("B", after=60)
        return self.field(60)


# ---------------------------------------------------------------- map-aware helpers (no-collision walking)
import json  # noqa: E402
from collections import deque  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
MG = json.load(open(os.path.join(ROOT, "data", "maps", "map_groups.json")))
LAYOUTS = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "data", "layouts", "layouts.json")))["layouts"]
           if "id" in l}
DELTA_FIRST, DELTA_LAST = 1578, 1634          # SPECIES_STANTLER_DELTA .. SPECIES_MILOTIC_DELTA (species.h enum)
MON_SIZE = 100                                 # sizeof(struct Pokemon); hp +0x56, maxHP +0x58, level +0x54


def folder(gr, n):
    return MG[MG["group_order"][gr]][n]


def mapjson(f):
    return json.load(open(os.path.join(ROOT, "data", "maps", f, "map.json")))


def blocked_cells(f):
    j = mapjson(f)
    return {(w["x"], w["y"]) for w in j["warp_events"]} | {(o["x"], o["y"]) for o in j["object_events"]} | \
        {(c["x"], c["y"]) for c in j.get("coord_events", [])}


def grid_path(f, start, goal):
    l = LAYOUTS[mapjson(f)["layout"]]
    w, h = l["width"], l["height"]
    bad = blocked_cells(f) - {goal}
    prev = {start: None}
    q = deque([start])
    D = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}
    while q:
        c = q.popleft()
        if c == goal:
            break
        for d in D:
            n = (c[0] + d[0], c[1] + d[1])
            if 0 <= n[0] < w and 0 <= n[1] < h and n not in prev and n not in bad:
                prev[n] = c
                q.append(n)
    if goal not in prev:
        return None
    out, c = [], goal
    while prev[c] is not None:
        p = prev[c]
        out.append(D[(c[0] - p[0], c[1] - p[1])])
        c = p
    return out[::-1]


def _go(self, x, y):
    """walk to (x, y) on the current map, never stepping on warps / objects / triggers (needs FLAG_NO_COLLIDE)"""
    cx, cy, gr, n = self.pos()
    steps = grid_path(folder(gr, n), (cx, cy), (x, y))
    if steps is None:
        log("  go: no path", folder(gr, n), (cx, cy), (x, y))
        return False
    for d in steps:
        self.walk(d, 1)
    ok = self.pos()[:2] == (x, y)
    if not ok:
        log("  go", (x, y), "ended at", self.pos())
    return ok


def _cross(self, direction, maxsteps=80):
    """walk off the map edge in `direction` until the map changes"""
    gr, n = self.pos()[2:]
    for _ in range(maxsteps):
        self.walk(direction, 1)
        if self.pos()[2:] != (gr, n):
            self.wait(30)
            return True
    return False


def _battle_offsets(self):
    p = self.e.r32("gPlayerPartyPtr")
    mx = struct.unpack("<H", self.e.read(p + 0x58, 2))[0]
    b0 = self.e.read(self.e.sym("gBattleMons"), 0x40)
    for off in range(0x20, 0x3E, 2):
        if struct.unpack_from("<H", b0, off)[0] == mx and struct.unpack_from("<H", b0, off - 4)[0] <= mx:
            return off - 4
    return 0x2A


def _prep_party(self):
    """lead party mons to level 100 in the party struct (no exp / move-learn prompts after big wins)"""
    p = self.e.r32("gPlayerPartyPtr")
    cnt = self.e.r8(self.e.r32("gPlayerPartyCountPtr")) if False else 6
    for i in range(cnt):
        self.e.write(p + i * MON_SIZE + 0x54, bytes([100]))


def _force_win(self, maxrounds=16):
    """win any battle: foe party slots 1-5 to 0 HP, active foe HP 1 and attack 1, our HP full and speed 999"""
    hp = self._battle_offsets()
    ep = self.e.r32("gEnemyPartyPtr")
    for i in range(1, 6):
        self.e.write(ep + i * MON_SIZE + 0x56, b"\x00\x00")
    for _ in range(3):
        self.press("B", after=60)
    for _ in range(maxrounds):
        if not self.in_battle():
            break
        b0, b1 = self.e.sym("gBattleMons"), self.e.sym("gBattleMons") + 140
        mx = struct.unpack("<H", self.e.read(b0 + hp + 4, 2))[0]
        self.e.write(b0 + hp, struct.pack("<H", mx))
        self.e.write(b0 + 6, struct.pack("<H", 999))
        self.e.write(b1 + hp, b"\x01\x00")
        self.e.write(b1 + 2, b"\x01\x00")
        self.e.write(b1 + 8, b"\x01\x00")
        self.press("A", after=30)
        self.press("A", after=200)
        for _ in range(10):
            if not self.in_battle():
                break
            self.press("B", after=60)
    return self.field(80)


def _battle_party_species(self):
    """species of every battler slot (0 = ours, 1 = foe)"""
    b = self.e.sym("gBattleMons")
    return [struct.unpack("<H", self.e.read(b + 140 * i, 2))[0] for i in range(2)]


E2E.go = _go
E2E.cross = _cross
E2E._battle_offsets = _battle_offsets
E2E.prep_party = _prep_party
E2E.force_win = _force_win
E2E.battlers = _battle_party_species
