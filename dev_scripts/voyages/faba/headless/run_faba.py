"""Headless checks for Holon Leader Faba (Pillow venv, harness ROM from hbuild.sh, hold /tmp/voyages_mgba.lock):
    <venv python> run_faba.py <outdir>/h
Shots -> ../shots/, log -> ../shots/run_faba.log. Uses polish_content/headless/e2e_lib.py."""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "voyages", "polish_content", "headless"))
import e2e_lib  # noqa: E402
from e2e_lib import E2E, log, LOG, FLAG_NO_SEE, FLAG_NO_WILD, FLAG_NO_COLLIDE, FLAG_SYS_GAME_CLEAR, MG  # noqa: E402

SHOTS = os.path.join(HERE, "..", "shots")
e2e_lib.SHOTS = SHOTS
HOLON = MG["group_order"].index("gMapGroup_Holon")
NUM = {f: (HOLON, i) for i, f in enumerate(MG["gMapGroup_Holon"])}
FLAG_RECEIVED_EEVEE, FLAG_FABA, FLAG_HEALED = 0x283, 0x286, 0x287
TRAINER_FLAGS_START = 0x500


def const(path, name):
    return int(re.search(r"#define %s\s+(\w+)" % name, open(os.path.join(ROOT, path)).read()).group(1), 0)


def enum_index(path, name):
    txt = open(os.path.join(ROOT, path)).read()
    i = txt.index(name + ",")
    start = txt.rindex("{", 0, i)
    body = re.sub(r"//.*", "", txt[start + 1:i])
    return len([x for x in body.split(",") if x.strip()])


TRAINER_HOLON_FABA = const("include/constants/opponents.h", "TRAINER_HOLON_FABA")
TRAINER_HOLON_TOBIAS = const("include/constants/opponents.h", "TRAINER_HOLON_TOBIAS")
MUS_ENCOUNTER_AQUA = const("include/constants/songs.h", "MUS_ENCOUNTER_AQUA")
MUS_VS_AQUA_MAGMA_LEADER = const("include/constants/songs.h", "MUS_VS_AQUA_MAGMA_LEADER")
ENV_OFFICE = enum_index("include/constants/battle.h", "BATTLE_ENVIRONMENT_OFFICE")
SPECIES = {}
for n, v in re.findall(r"(SPECIES_\w+)\s*=\s*(\d+),", open(os.path.join(ROOT, "include/constants/species.h")).read()):
    SPECIES.setdefault(int(v), n)
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


def debug_flags(see=1, wild=1, collide=1):
    g.flag(FLAG_NO_SEE, see)
    g.flag(FLAG_NO_WILD, wild)
    g.flag(FLAG_NO_COLLIDE, collide)


def object_at(x, y):
    base = g.e.sym("gObjectEvents")
    raw = b"".join(g.e.read(base + off, 0x90) for off in range(0, 0x240, 0x90))
    for i in range(16):
        o = raw[i * 0x24:(i + 1) * 0x24]
        cx, cy = struct.unpack_from("<hh", o, 0x0C)
        if o[0] & 1 and (cx, cy) == (x + 7, y + 7):
            return True
    return False


def bg_pal(slot):
    return struct.unpack("<16H", g.e.read(g.e.sym("gPlttBufferUnfaded") + slot * 32, 32))


def jasc(path):
    v = open(os.path.join(ROOT, path)).read().split()[3:]
    return tuple(((int(v[i * 3]) >> 3) | ((int(v[i * 3 + 1]) >> 3) << 5) | ((int(v[i * 3 + 2]) >> 3) << 10))
                 for i in range(16))


def task_funcs():
    raw = b"".join(g.e.read(g.e.sym("gTasks") + off, 0x100) for off in range(0, 16 * 0x28, 0x100))
    return {struct.unpack_from("<I", raw, i * 0x28)[0] & ~1 for i in range(16) if raw[i * 0x28 + 4]}


def face(d):
    """turn toward an occupied cell: a held press bumps into the object and faces it (taps can be eaten while the
    follower is still moving)"""
    g.wait(30)
    g.flag(FLAG_NO_COLLIDE, 0)
    g.e.press(d, hold=12, after=20)
    g.flag(FLAG_NO_COLLIDE, 1)


def transition_shot(name):
    """the renderer has no blending and reads WIN0 from sGpuRegBuffer (the weave sets it per scanline), so render
    BG0 alone, windows off: the Holon logo tiles/tilemap/palette 15 exactly as loaded"""
    sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "mgba_headless"))
    from render import render
    e = g.e
    io = e.read(0x04000000, 0x60)
    reg = bytearray(e.read(e.sym("sGpuRegBuffer"), 0x60))
    dispcnt = struct.unpack_from("<H", reg, 0)[0]
    struct.pack_into("<H", reg, 0, (dispcnt & ~0xFF00) | 0x0100)
    img = render(io, bytes(reg), e.read(0x06000000, 0x18000), e.read(0x05000000, 0x400), e.read(0x07000000, 0x400))
    img.resize((480, 320), 0).save(os.path.join(SHOTS, name + ".png"))
    log("  shot", name, "(BG0 only)")


def opponent():
    return g.e.r16(g.e.sym("gTrainerBattleParameter") + 2)


def talk_battle(tag, want_trainer, enc_song=None):
    """talk (A) to the trainer in front, advance the intro with A while watching the music and the transition task"""
    holon = g.e.sym("Task_Holon") & ~1
    seen, shot_t, songs, text0 = False, False, [], None
    g.press("A", after=40)
    for step in range(120):
        if text0 is None and g.script_running():
            text0 = g.text()
            songs.append(g.song())
            g.snap("%s_1_intro_text" % tag)
        if holon in task_funcs():
            if not seen:
                seen = True
                g.wait(150)                      # the logo is fully woven in by ~150 frames
                transition_shot("%s_2_holon_transition" % tag)
                shot_t = True
        if g.in_battle():
            break
        if not seen:
            g.press("A", after=30)
        else:
            g.wait(20)
    started = g.in_battle() or g.wait_battle(600)
    check(seen, "%s: B_TRANSITION_HOLON task ran" % tag)
    if enc_song is not None:
        check(enc_song in songs, "%s: encounter music %s during the intro text (want %d)" % (tag, songs, enc_song))
    opp = opponent() if started else None
    check(started and opp == want_trainer, "%s: battle vs trainer %s (want %d)" % (tag, opp, want_trainer))
    if started:
        from emu_lib import decode
        s = ""
        for _ in range(60):
            g.wait(10)
            s = decode(g.e.read(g.e.sym("gDisplayedStringBattle"), 0x60)).replace("\n", " ")
            if "challenged" in s:
                break
        log("  battle text:", s)
        g.snap("%s_3_battle_intro" % tag)
        env = g.e.r8("gBattleEnvironment")
        check(env == ENV_OFFICE, "%s: battle environment %d (want office %d)" % (tag, env, ENV_OFFICE))
        return s
    return None


def main():
    g.boot()
    g.flag(FLAG_SYS_GAME_CLEAR, 1)
    debug_flags()
    g.prep_party()
    for f in (FLAG_RECEIVED_EEVEE, FLAG_FABA, FLAG_HEALED):
        g.flag(f, 0)
    for t in (TRAINER_HOLON_FABA, TRAINER_HOLON_TOBIAS):
        g.flag(TRAINER_FLAGS_START + t, 0)

    drained, healthy = jasc("data/tilesets/secondary/holon/palettes/07.pal"), \
        jasc("data/tilesets/primary/general_holon/palettes/02.pal")

    # 1. village rings before
    warp("HolonVillage", 11)
    g.walk("DOWN", 1)
    g.snap("01_village_rings_before")
    p7 = bg_pal(7)
    check(p7[1:] == drained[1:], "Village before Faba: BG palette 7 = drained foliage (07.pal)")

    # 2. Tower 2F: Eevee gift blocked before
    warp("HolonResearchTower_2F", 0)
    check(object_at(11, 6), "Tower 2F: Faba object present at (11,6) before his defeat")
    g.go(11, 4)
    g.snap("02_tower_2f_faba_ow")
    g.go(3, 6)
    face("LEFT")
    g.press("A", after=60)
    t = g.text()
    log("  head:", t[:120])
    g.snap("03_head_not_now")
    g.until_idle()
    check("Faba" in t and not g.flag(FLAG_RECEIVED_EEVEE), "Head of research before Faba: 'not now' line, no Eevee-delta")

    # 3. Researcher Tobias (18,6, facing left): Holon transition
    g.go(17, 6)
    face("RIGHT")
    s = talk_battle("04_tobias", TRAINER_HOLON_TOBIAS)
    check(s is not None and "Holon Researcher" in s.replace("?", " "), "Tobias intro text names the Holon Researcher class")
    if g.in_battle():
        g.force_win()
        g.until_idle()

    # 4. Faba (11,6, facing down): stand below him at (11,7), face up
    g.go(11, 7)
    face("UP")
    s = talk_battle("05_faba", TRAINER_HOLON_FABA, enc_song=MUS_ENCOUNTER_AQUA)
    check(s is not None and "Holon Leader Faba" in s.replace("?", " "), "Faba intro text: '%s'" % s)
    if g.in_battle():
        g.wait(200)
        foe = g.foe()
        lvl = g.e.r8(g.e.sym("gBattleMons") + 140 + 0x2A + 2) if False else None
        check(SPECIES.get(foe) == "SPECIES_HYPNO", "Faba lead gBattleMons[1].species = %s" % SPECIES.get(foe, foe))
        song = g.song()
        check(song == MUS_VS_AQUA_MAGMA_LEADER, "Faba battle music %s (want %d)" % (song, MUS_VS_AQUA_MAGMA_LEADER))
        g.snap("06_faba_battle")
        g.force_win()
        for _ in range(40):
            if not g.script_running():
                break
            if "remember Faba" in g.text():
                g.snap("07_faba_after_text")
            g.press("A", after=40)
        g.until_idle()
    g.wait(60)
    g.snap("08_faba_gone")
    check(g.flag(FLAG_FABA) and g.flag(FLAG_HEALED), "after the win: FLAG_HOLON_FABA_DEFEATED + FLAG_HOLON_POWER_SPOTS_HEALED set")
    check(not object_at(11, 6), "after the win: Faba removed from (11,6)")

    # 5. Eevee gift after
    g.go(3, 6)
    face("LEFT")
    g.press("A", after=60)
    t = g.text()
    log("  head:", t[:120])
    g.snap("09_head_offer")
    for _ in range(30):
        if not g.script_running():
            break
        if "nickname" in g.text():
            g.press("B", after=40)      # NO to the nickname prompt (never A: that opens the naming screen)
        else:
            if "received" in g.text():
                g.snap("09b_received_eevee")
            g.press("A", after=40)
    g.until_idle()
    check(g.flag(FLAG_RECEIVED_EEVEE), "Head of research after Faba: Eevee-delta given (FLAG_HOLON_RECEIVED_EEVEE)")

    # 6. Faba stays gone after re-entering
    warp("HolonResearchTower_2F", 0)
    check(not object_at(11, 6), "Tower 2F re-entered: Faba stays hidden")

    # 7. village + lake rings after
    warp("HolonVillage", 11)
    g.walk("DOWN", 1)
    g.snap("10_village_rings_after")
    p7 = bg_pal(7)
    check(p7[1:] == healthy[1:], "Village after Faba: BG palette 7 = General_Holon 02 (healthy)")
    crossed = g.cross("DOWN", 60)
    g.wait(60)
    log("  crossed to the lake:", crossed, g.pos())
    if crossed:
        g.go(25, 20)
        g.snap("11_lake_island_after")
    p7 = bg_pal(7)
    check(p7[1:] == healthy[1:], "Lake after Faba: BG palette 7 = General_Holon 02 (healthy)")

    open(os.path.join(SHOTS, "run_faba.log"), "w").write("\n".join(LOG) + "\n")
    n = sum(ok for ok, _ in RESULTS)
    log("%d/%d PASS" % (n, len(RESULTS)))
    open(os.path.join(SHOTS, "run_faba.log"), "w").write("\n".join(LOG) + "\n")
    g.close()


if __name__ == "__main__":
    main()
