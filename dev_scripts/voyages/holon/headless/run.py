"""Holon headless test: run with the Pillow venv from this folder (lock held by the caller)."""
import json
import os
import struct
import sys
import time
from collections import deque

WT = "/Users/arandavies/Development/pokemon-orchid/pokeorchid-voy-holon"
sys.path.insert(0, os.path.join(WT, "dev_scripts", "mgba_headless"))
sys.path.insert(0, os.path.join(WT, "dev_scripts", "voyages", "holon"))
os.chdir(WT)                                      # check_holon reads the data relative to the worktree
import check_holon as ch                          # noqa: E402
from boot import boot, warp, pos                  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(WT, "dev_scripts", "voyages", "holon", "shots")
os.makedirs(SHOTS, exist_ok=True)
MG = json.load(open("data/maps/map_groups.json"))
G = MG["group_order"].index("gMapGroup_Holon")
NUM = {f: i for i, f in enumerate(MG["gMapGroup_Holon"])}
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def sb1(e):
    return e.r32("gSaveBlock1Ptr")


def flag(e, n, on=True):
    a = sb1(e) + 0x1270 + (n >> 3)
    b = e.read(a, 1)[0]
    b = (b | (1 << (n & 7))) if on else (b & ~(1 << (n & 7)))
    e.write(a, bytes([b]))


def flag_get(e, n):
    return (e.read(sb1(e) + 0x1270 + (n >> 3), 1)[0] >> (n & 7)) & 1


def idle(e, maxf=900):
    for _ in range(maxf // 10):
        e.frames(10)
        if e.r8("sGlobalScriptContextStatus") == 2 and e.r8("sLockFieldControls") == 0:
            return True
    return False


def shot(e, name):
    e.frames(20)
    p = os.path.join(SHOTS, name + ".png")
    e.shot(p)
    log("shot", name, pos(e))


def folder_at(e):
    x, y, g, n = pos(e)
    if g != G:
        return None
    return MG["gMapGroup_Holon"][n]


DIRS = {(1, 0): "RIGHT", (-1, 0): "LEFT", (0, 1): "DOWN", (0, -1): "UP"}


def path(folder, start, goal, surf=False, ghost=False):
    lid = ch.mj(folder)["layout"]
    w, h, v, beh = ch.layout(lid)
    objs = {(o["x"], o["y"]) for o in ch.mj(folder)["object_events"]}
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        if c == goal:
            break
        for d in DIRS:
            n = (c[0] + d[0], c[1] + d[1])
            if not (0 <= n[0] < w and 0 <= n[1] < h) or n in prev:
                continue
            if not ghost and (n in objs or not ch.walk_ok(v, w, beh, c, n, surf)):
                continue
            prev[n] = c
            q.append(n)
    if goal not in prev:
        return None
    out, c = [], goal
    while prev[c] is not None:
        p = prev[c]
        out.append(DIRS[(c[0] - p[0], c[1] - p[1])])
        c = p
    return out[::-1]


def walk_to(e, goal, ghost=False):
    f = folder_at(e)
    x, y, _, _ = pos(e)
    steps = path(f, (x, y), goal, ghost=ghost)
    if steps is None:
        log("NO PATH", f, (x, y), "->", goal)
        return False
    for d in steps:
        before = pos(e)
        for _try in range(3):
            e.press(d, hold=16, after=6)
            if pos(e)[:2] != before[:2] or pos(e)[2:] != before[2:]:
                break
        idle(e, 300)
    ok = pos(e)[:2] == goal
    log("walk", f, "->", goal, "ok" if ok else "ENDED AT %s" % (pos(e),))
    return ok


def step(e, d, n=1):
    for _ in range(n):
        e.press(d, hold=16, after=8)
    idle(e, 400)


def face(e, d):
    e.press(d, hold=2, after=10)


def talk(e, presses=8, gap=40):
    e.press("A", after=gap)
    for _ in range(presses):
        if idle(e, 30):
            break
        e.press("A", after=gap)
    idle(e, 1200)


def party_hp(e):
    p = e.r32("gPlayerPartyPtr")
    hp, mx = struct.unpack("<HH", e.read(p + 0x56, 4))
    return hp, mx


def obj_pal(e, tag):
    """gPlttBufferUnfaded colours (RGB555) of the OBJ palette slot that holds `tag`, or None."""
    tags = e.read(e.syms["sSpritePaletteTags"], 32)
    tags = struct.unpack("<16H", tags)
    if tag not in tags:
        return None
    slot = tags.index(tag)
    raw = e.read(e.syms["gPlttBufferUnfaded"] + 0x200 + slot * 32, 32)
    return list(struct.unpack("<16H", raw))


def jasc555(path):
    rows = open(path).read().split("\n")[3:19]
    out = []
    for r in rows:
        rr, gg, bb = (int(v) for v in r.split())
        out.append((rr >> 3) | ((gg >> 3) << 5) | ((bb >> 3) << 10))
    return out


def main():
    os.system("true")
    e = boot(os.path.join(HERE, "h"))
    try:
        for k in ("B", "START", "A", "B", "B", "B", "B"):
            e.press(k, after=60)
        idle(e)
        log("boot pos", pos(e))
        flag(e, 0x29E)       # harness: no wild encounters
        flag(e, 0x29D)       # harness: trainers don't spot you
        # ---- village (debug warp to the Centre door) + Centre heal
        warp(e, G, NUM["HolonVillage"], 0)
        idle(e)
        log("village", pos(e), folder_at(e))
        shot(e, "01_village_centre")
        p = e.r32("gPlayerPartyPtr")
        hp0 = party_hp(e)
        e.write(p + 0x56, struct.pack("<H", 1))
        log("lead hp set 1 (was %s)" % (hp0,))
        x, y, _, _ = pos(e)
        step(e, "UP")
        idle(e, 600)
        log("after door", pos(e), folder_at(e))
        walk_to(e, (7, 4))
        face(e, "UP")
        talk(e, presses=12)
        hp1 = party_hp(e)
        log("Centre heal: hp after nurse = %s -> %s" % (hp1, "HEALED" if hp1[0] == hp1[1] else "NOT HEALED"))
        shot(e, "02_centre_after_heal")
        walk_to(e, (7, 8))
        step(e, "DOWN", 2)
        idle(e, 600)
        log("back out", pos(e), folder_at(e))
        # ---- village -> coast (walkway west edge)
        walk_to(e, (0, 38))
        step(e, "LEFT", 2)
        log("coast?", pos(e), folder_at(e))
        shot(e, "03_coast_east_edge")
        # long grass on the coast (meadow 28-38 x 9-17) for the field effect palette
        walk_to(e, (30, 14))
        step(e, "UP")
        e.frames(4)
        pal = obj_pal(e, 0x1005)
        want = jasc555(os.path.join(WT, "graphics/field_effects/palettes/general_1_holon.pal"))
        vivid = jasc555(os.path.join(WT, "graphics/field_effects/palettes/general_1.pal"))
        log("FLDEFF_PAL_TAG_GENERAL_1 loaded:", pal is not None,
            "matches holon copy:", pal[1:] == want[1:] if pal else None,
            "matches vivid:", pal[1:] == vivid[1:] if pal else None)
        shot(e, "04_coast_long_grass_rustle")
        walk_to(e, (21, 11))
        shot(e, "05_coast_ruins_rail_stones")
        walk_to(e, (8, 36))
        walk_to(e, (5, 36))
        shot(e, "06_coast_jetty_sailor_boat")
        face(e, "LEFT")
        talk(e)
        # ---- back to the village and on south to the lake
        walk_to(e, (43, 26))
        step(e, "RIGHT", 2)
        log("village?", pos(e), folder_at(e))
        walk_to(e, (30, 50))
        shot(e, "07_village_south_bridge")
        walk_to(e, (35, 38))
        shot(e, "08_village_research_tower_drained_ring")
        walk_to(e, (30, 71))
        step(e, "DOWN", 2)
        log("lake?", pos(e), folder_at(e))
        shot(e, "09_lake_north")
        walk_to(e, (24, 36))
        face(e, "UP")
        shot(e, "10_lake_cynthia_peninsula")
        talk(e)
        walk_to(e, (7, 10))
        face(e, "UP")
        shot(e, "11_lake_sealed_dome")
        # ---- island: harness no-collision flag, walk over the water to the sphere
        flag(e, 0x29F)
        walk_to(e, (24, 28), ghost=True)
        shot(e, "12_lake_sphere_dormant")
        dormant = obj_pal(e, 0x113A)
        flag(e, 0x285)        # FLAG_HOLON_SPHERE_GLOW: walk out of range and back so the sphere respawns
        walk_to(e, (24, 4), ghost=True)
        log("sphere palette while away:", obj_pal(e, 0x113A) is not None)
        walk_to(e, (24, 28), ghost=True)
        glow = obj_pal(e, 0x113A)
        log("sphere palette dormant[1:4]", dormant[1:4] if dormant else None, "glow[1:4]", glow[1:4] if glow else None,
            "expected glow", jasc555(os.path.join(WT, "graphics/object_events/palettes/holon_sphere_glow.pal"))[1:4])
        shot(e, "13_lake_sphere_glow")
        walk_to(e, (40, 43), ghost=True)
        shot(e, "14_lake_gyarados")
        flag(e, 0x29F, False)
        # ---- interiors via debug warp
        for f, wid, name in (("HolonResearchTower_1F", 0, "15_tower_1f"), ("HolonResearchTower_2F", 0, "16_tower_2f"),
                             ("HolonVillage_RuinsHouse", 0, "17_ruins_house"), ("HolonVillage_House1", 0, "18_house1"),
                             ("HolonVillage_Mart", 0, "19_mart")):
            warp(e, G, NUM[f], wid)
            idle(e)
            log("warp", f, pos(e), folder_at(e))
            shot(e, name)
        # Eevee gift (2F head of research at (2,6))
        warp(e, G, NUM["HolonResearchTower_2F"], 0)
        idle(e)
        n0 = e.r8("gPlayerPartyCount") if "gPlayerPartyCount" in e.syms else None
        walk_to(e, (2, 7))
        face(e, "UP")
        e.press("A", after=60)
        for _ in range(12):
            e.press("A", after=50)
        e.frames(120)
        shot(e, "20a_tower_2f_naming")
        e.press("START", after=30)      # naming screen: cursor to OK, confirm the default name
        e.press("A", after=200)
        for _ in range(4):
            e.press("A", after=60)
        idle(e, 1200)
        log("Eevee gift flag 0x283 =", flag_get(e, 0x283))
        shot(e, "20_tower_2f_after_gift")
    finally:
        try:
            e.proc.kill()
        except Exception:
            pass
        open(os.path.join(SHOTS, "headless_log.txt"), "w").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
