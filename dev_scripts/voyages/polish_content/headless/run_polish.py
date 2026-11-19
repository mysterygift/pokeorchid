"""Headless checks for the content polish (Pillow venv, harness ROM from hbuild.sh, hold /tmp/voyages_mgba.lock):
    <venv python> run_polish.py <outdir>/h [trainers swimmer tower rocks doors]
Shots -> ../shots/, log -> ../shots/run_polish.log."""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e2e_lib import E2E, log, LOG, SHOTS, FLAG_NO_SEE, FLAG_NO_WILD, FLAG_NO_COLLIDE, FLAG_SYS_GAME_CLEAR, MG  # noqa

sys.path.insert(0, os.path.join(HERE, ".."))
from trainers_spec import T, SLOTS  # noqa: E402

SEVII = MG["group_order"].index("gMapGroup_Sevii")
HOLON = MG["group_order"].index("gMapGroup_Holon")
NUM = {f: (SEVII, i) for i, f in enumerate(MG["gMapGroup_Sevii"])}
NUM.update({f: (HOLON, i) for i, f in enumerate(MG["gMapGroup_Holon"])})
SLOT = {tr["const"]: n for (n, _), tr in zip(SLOTS, T)}
FLAG_DOTTED, FLAG_TANOBY = 0x26B, 0x26C
RESULTS = []


def check(ok, what):
    RESULTS.append((bool(ok), what))
    log(("PASS " if ok else "FAIL ") + what)


g = E2E(sys.argv[1])


def warp(folder, w=0):
    gr, n = NUM[folder]
    g.warp(gr, n, w)
    g.until_idle()
    g.wait(30)
    return g.pos()


def at(folder):
    return tuple(g.pos()[2:]) == NUM[folder]


def grid(x, y):
    b = g.e.sym("gBackupMapLayout")
    w = g.e.r32(b)
    m = g.e.r32(b + 8)
    v = struct.unpack("<H", g.e.read(m + 2 * ((x + 7) + (y + 7) * w), 2))[0]
    return v & 0x3FF, (v >> 10) & 3


def object_at(x, y):
    """an active object event whose spawn cell is (x, y) (map coords)"""
    base = g.e.sym("gObjectEvents")
    raw = b"".join(g.e.read(base + off, 0x90) for off in range(0, 0x240, 0x90))
    for i in range(16):
        o = raw[i * 0x24:(i + 1) * 0x24]
        ix, iy = struct.unpack_from("<hh", o, 0x0C)
        if o[0] & 1 and (ix, iy) == (x + 7, y + 7):
            return True
    return False


def surf_go(x, y):
    """surfing moves two tiles per held press: tap one tile at a time along a BFS path"""
    from e2e_lib import grid_path, folder
    cx, cy, gr, n = g.pos()
    steps = grid_path(folder(gr, n), (cx, cy), (x, y)) or []
    for d in steps:
        p0 = g.pos()
        for _ in range(8):
            g.e.press(d, hold=3, after=10)
            if g.pos() != p0:
                break
        g.wait(6)
    return g.pos()[:2] == (x, y)


def opponent():
    return g.e.r16(g.e.sym("gTrainerBattleParameter") + 2)


def battle_wait(maxa=40):
    """advance the trainer's intro text with A until the battle screen runs"""
    for _ in range(maxa):
        if g.in_battle():
            return True
        g.press("A", after=40)
    return g.wait_battle(600)


def debug_flags(see=1, wild=1, collide=1):
    g.flag(FLAG_NO_SEE, see)
    g.flag(FLAG_NO_WILD, wild)
    g.flag(FLAG_NO_COLLIDE, collide)


def setup():
    g.boot()
    g.flag(FLAG_SYS_GAME_CLEAR, 1)
    for b in range(0x867, 0x86F):
        g.flag(b, 1)
    debug_flags()
    g.prep_party()


def battle_from_sight(folder, wslot, stand, step, const, name):
    """stand next to the sight line (debug no-sight on), then step into it with sight on: the trainer must spot."""
    warp(folder, wslot)
    ok = g.go(*stand)
    debug_flags(see=0, wild=1, collide=0)
    g.walk(step, 1)
    started = battle_wait()
    opp = opponent() if started else None
    g.snap("trainer_%s" % name)
    check(started and opp == SLOT[const], "%s: %s spots the player at %s -> battle vs trainer %s (expect %d)" % (
        folder, name, g.pos()[:2], opp, SLOT[const]))
    if started:
        g.force_win()
        g.until_idle()
    debug_flags()


def t_trainers():
    battle_from_sight("MtEmber_Exterior", 0, (14, 30), "RIGHT", "TRAINER_SEVII_LOGAN", "mt_ember_logan")
    battle_from_sight("SixIsland_RuinValley", 0, (13, 11), "RIGHT", "TRAINER_SEVII_DARYL", "ruin_valley_daryl")
    # talk-to battle on a Six Island route
    warp("SixIsland_RuinValley", 0)
    g.go(31, 12)          # below Stanly (32,11)? he faces down/left: approach from the left instead
    g.go(31, 11)
    debug_flags(see=0, wild=1, collide=0)
    g.face("RIGHT")
    g.press("A", after=60)
    started = battle_wait()
    opp = opponent() if started else None
    g.snap("trainer_ruin_valley_stanly")
    check(started and opp == SLOT["TRAINER_SEVII_STANLY"], "Ruin Valley: Stanly battle -> trainer %s" % opp)
    if started:
        g.force_win()
        g.until_idle()
    debug_flags()


def t_swimmer():
    """Surf (harness: every mon knows Surf) off Two Island into Sea Route A; swimmer Dylan battles."""
    warp("TwoIsland", 3)
    debug_flags(see=1, wild=1, collide=0)
    g.walk("LEFT", 1)
    g.face("LEFT")
    g.press("A", after=60)
    g.press("A", after=60)
    g.until_idle(key="A")
    g.wait(60)
    surfing = bool(g.e.r8("gPlayerAvatar") & 8)
    log("  surfing:", surfing, g.pos())
    debug_flags(see=1, wild=1, collide=1)
    g.cross("LEFT")                  # row 8 is open water west of the dock, straight into Sea Route A
    log("  sea route A?", at("SeviiSeaRouteA"), g.pos())
    surf_go(5, 5)
    debug_flags(see=0, wild=1, collide=0)
    g.walk("DOWN", 1)            # into Dylan's row (8,6), sight 3 to the left
    started = g.wait_battle(300) or (g.script_running() and battle_wait())
    how = "spotted"
    if not started:              # he was facing right: talk to him
        debug_flags(see=1, wild=1, collide=1)
        surf_go(7, 6)
        debug_flags(see=0, wild=1, collide=0)
        g.face("RIGHT")
        g.press("A", after=60)
        started = battle_wait()
        how = "talked to"
    opp = opponent() if started else None
    g.snap("trainer_sea_route_a_swimmer_dylan")
    check(started and at("SeviiSeaRouteA") and surfing and opp == SLOT["TRAINER_SEVII_DYLAN"],
          "Sea Route A: surfing, swimmer Dylan %s -> trainer %s" % (how, opp))
    if started:
        g.force_win()
        g.until_idle()
    debug_flags()


SPECIES_NAMES = {}


def species_name(sid):
    if not SPECIES_NAMES:
        import re
        txt = open(os.path.join(HERE, "..", "..", "..", "..", "include", "constants", "species.h")).read()
        for name, val in re.findall(r"(SPECIES_\w+)\s*=\s*(\d+),", txt):
            SPECIES_NAMES.setdefault(int(val), name)
    return SPECIES_NAMES.get(sid, str(sid))


def t_tower():
    warp("HolonResearchTower_2F", 0)
    g.go(8, 6)
    debug_flags(see=1, wild=0, collide=0)
    started = False
    for i in range(160):
        g.walk("RIGHT" if (i // 3) % 2 == 0 else "LEFT", 1)
        if g.in_battle() or g.wait_battle(40):
            started = True
            break
    if started:
        g.wait(400)
    sp = g.foe() if started else None
    g.snap("tower_2f_wild")
    check(started and at("HolonResearchTower_2F"), "Research Tower 2F lab floor: wild %s after %d steps" % (
        species_name(sp) if sp else None, i + 1))
    if started:
        g.force_win()
        g.until_idle()
    debug_flags()


def t_rocks():
    vil = json.load(open(os.path.join(HERE, "..", "..", "..", "..", "data", "maps", "HolonVillage", "map.json")))
    w = max(range(len(vil["warp_events"])), key=lambda k: vil["warp_events"][k]["y"])
    warp("HolonVillage", w)
    g.go(31, 70)
    g.cross("DOWN")
    log("  lake?", at("HolonLake"), g.pos())
    for rx, ry in [(9, 23), (27, 41)]:
        g.go(rx - 1, ry)
        present = object_at(rx, ry)
        debug_flags(see=1, wild=0, collide=0)
        g.face("RIGHT")
        g.press("A", after=60)
        g.snap("lake_rock_%d_%d_prompt" % (rx, ry))
        g.press("A", after=60)           # YES
        g.press("A", after=60)           # "... used Rock Smash!"
        enc = g.wait_battle(400)
        if not enc:
            g.until_idle(key="B")
            enc = g.in_battle()
        foe = None
        if enc:
            g.wait(400)
            foe = species_name(g.foe())
            g.snap("lake_rock_smash_encounter")
            g.force_win()
        g.until_idle(key="B")
        g.snap("lake_rock_%d_%d_after" % (rx, ry))
        gone = not object_at(rx, ry)
        check(at("HolonLake") and present and gone, "Holon Lake rock (%d,%d): object there before=%s, gone after "
              "Rock Smash=%s, encounter: %s" % (rx, ry, present, gone, foe))
        debug_flags()


def t_doors():
    debug_flags(see=1, wild=1, collide=0)
    # Ruin Valley, sealed (default)
    g.flag(FLAG_DOTTED, 0)
    warp("SixIsland_RuinValley", 0)
    mt, col = grid(24, 24)
    g.walk("UP", 1)
    g.walk("DOWN", 1)
    p = g.pos()
    g.snap("door_ruin_valley_sealed")
    check(at("SixIsland_RuinValley") and mt == 0x3C0 and col, "Ruin Valley sealed: door metatile 0x%03X collision %d, "
          "player stays on the valley %s" % (mt, col, p[:2]))
    # open
    g.flag(FLAG_DOTTED, 1)
    warp("SixIsland_RuinValley", 0)
    g.wait(60)
    mt, col = grid(24, 24)
    p = g.pos()
    g.snap("door_ruin_valley_open")
    check(mt == 0x3D7 and not col and p[:2] == (24, 25), "Ruin Valley open: door metatile 0x%03X collision %d, "
          "arrival walked out to %s" % (mt, col, p[:2]))
    g.walk("UP", 1)
    g.wait(150)
    g.until_idle()
    p = g.pos()
    g.snap("door_dotted_hole_1f")
    check(at("SixIsland_DottedHole_1F"), "walked into the open door -> Dotted Hole 1F %s" % (p[:2],))
    g.walk("DOWN", 1)
    g.wait(180)
    g.until_idle()
    p = g.pos()
    g.snap("door_dotted_hole_back")
    check(at("SixIsland_RuinValley") and p[:2] == (24, 25), "Dotted Hole 1F exit -> Ruin Valley %s" % (p[:2],))
    g.walk("DOWN", 1)
    g.face("UP")
    g.snap("door_ruin_valley_open_doorway")
    # Tanoby, sealed
    g.flag(FLAG_TANOBY, 0)
    warp("SevenIsland_TanobyRuins", 0)          # Monean door (120,10)
    mt, col = grid(120, 10)
    g.walk("DOWN", 1)
    g.walk("UP", 1)
    g.wait(60)
    p = g.pos()
    g.snap("door_tanoby_sealed")
    check(at("SevenIsland_TanobyRuins") and p[:2] == (120, 11) and col,
          "Tanoby sealed: door 0x%03X collision %d, UP from (120,11) stays at %s" % (mt, col, p[:2]))
    g.flag(FLAG_TANOBY, 1)
    warp("SevenIsland_TanobyRuins", 0)
    mt, col = grid(120, 10)
    g.walk("DOWN", 1)
    g.walk("UP", 1)
    g.wait(180)
    g.until_idle()
    p = g.pos()
    g.snap("door_tanoby_monean_chamber")
    check(at("SevenIsland_TanobyRuins_MoneanChamber") and not col,
          "Tanoby open: door collision %d, UP into the doorway -> Monean Chamber %s" % (col, p[:2]))
    g.walk("DOWN", 1)
    g.wait(180)
    g.until_idle()
    p = g.pos()
    check(at("SevenIsland_TanobyRuins") and p[:2] == (120, 10), "Monean Chamber exit -> Tanoby Ruins %s" % (p[:2],))
    # a second chamber: Dilford (44,11) = warp 3
    warp("SevenIsland_TanobyRuins", 3)
    g.walk("DOWN", 1)
    g.walk("UP", 1)
    g.wait(180)
    g.until_idle()
    check(at("SevenIsland_TanobyRuins_DilfordChamber"), "Tanoby open: Dilford door -> chamber %s" % (g.pos(),))
    g.snap("door_tanoby_dilford_chamber")
    debug_flags()


TESTS = dict(trainers=t_trainers, swimmer=t_swimmer, tower=t_tower, rocks=t_rocks, doors=t_doors)

if __name__ == "__main__":
    which = sys.argv[2:] or list(TESTS)
    try:
        setup()
        for t in which:
            try:
                TESTS[t]()
            except Exception as ex:
                check(False, "%s crashed: %r" % (t, ex))
    finally:
        g.close()
        os.makedirs(SHOTS, exist_ok=True)
        open(os.path.join(SHOTS, "run_polish_%s.log" % "_".join(which)), "w").write("\n".join(LOG) + "\n")
        print("%d/%d passed" % (sum(r[0] for r in RESULTS), len(RESULTS)))
