"""Headless check for MUS_ORCHID_ENCOUNTER_HOLON (Pillow venv, voyages lock held by the caller):
    <venv python> t_holon_music.py <outdir>/h
Harness ROM = faba/headless/hbuild.sh (sight / wild / collision debug flags, key injection, embedded save) built
with data/scripts/debug.inc's Script 1 temporarily = `callnative PlayTrainerEncounterMusic` (as in
polish_phone_music/hbuild.sh). Checks, reading gMPlayInfo_BGM.songHeader:
  1. Researcher Tobias (Tower 2F, 18,6, facing left, sight 3) spots the player walking into row 6 -> new song
  2. talking to Faba (11,6) -> new song
  3. approach music through PlayTrainerEncounterMusic for other trainers is unchanged (Calvin = MALE,
     an Aqua grunt = AQUA, a Black Belt = INTENSE) and Holon Researcher Ido gets the new song
  4. gTrainerApproachMusicStyles in ROM: the 17 vanilla entries unchanged, entry 17 = MUS_ORCHID_ENCOUNTER_HOLON
"""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "voyages", "polish_content", "headless"))
import e2e_lib  # noqa: E402
from e2e_lib import E2E, log, LOG, FLAG_NO_SEE, FLAG_NO_WILD, FLAG_NO_COLLIDE, FLAG_SYS_GAME_CLEAR, MG  # noqa: E402

OUT = os.path.join(HERE, "..", "shots")
e2e_lib.SHOTS = OUT
HOLON = MG["group_order"].index("gMapGroup_Holon")
TOWER_2F = (HOLON, MG["gMapGroup_Holon"].index("HolonResearchTower_2F"))
FLAG_FABA = 0x286
TRAINER_FLAGS_START = 0x500


def consts(path, prefix):
    return {n: int(v, 0) for n, v in re.findall(r"#define (%s\w*)\s+(\w+)" % prefix, open(os.path.join(ROOT, path)).read())
            if re.match(r"^(0x[0-9a-fA-F]+|\d+)$", v)}


SONG = consts("include/constants/songs.h", "MUS_")
TRAINER = consts("include/constants/opponents.h", "TRAINER_")
SONG_NAME = {}
for k, v in SONG.items():
    SONG_NAME.setdefault(v, k)
NEW = SONG["MUS_ORCHID_ENCOUNTER_HOLON"]
RESULTS = []
g = E2E(sys.argv[1])


def check(ok, what):
    RESULTS.append(bool(ok))
    log(("PASS " if ok else "FAIL ") + what)


def header_is_new():
    return g.e.r32("gMPlayInfo_BGM") == g.e.sym("mus_orchid_encounter_holon")


def name(song):
    return SONG_NAME.get(song, song)


def face(d):
    g.wait(30)
    g.flag(FLAG_NO_COLLIDE, 0)
    g.e.press(d, hold=12, after=20)
    g.flag(FLAG_NO_COLLIDE, 1)


def watch_songs(frames, step=10, stop_battle=True):
    """songs heard over `frames` (in order of first appearance) and whether the header ever equalled the new song"""
    heard, hit = [], False
    for _ in range(frames // step):
        s = g.song()
        if s not in heard:
            heard.append(s)
        hit = hit or header_is_new()
        if stop_battle and g.in_battle():
            break
        g.wait(step)
    return heard, hit


def finish_intro_and_battle():
    for _ in range(40):
        if g.in_battle():
            break
        g.press("A", after=30)
    if g.in_battle() or g.wait_battle(600):
        g.wait(200)
        log("  battle song:", name(g.song()))
        g.force_win()
    g.until_idle()
    g.wait(60)


def debug_script1(trainer):
    g.e.write(g.e.sym("gTrainerBattleParameter") + 2, struct.pack("<H", TRAINER[trainer]))
    g.e.write(g.e.sym("gApproachingTrainerId"), b"\x00")
    g.field()
    g.press("R", "START", after=60)
    for _ in range(5):                          # main debug menu index 5 = Scripts
        g.press("DOWN", after=6)
    g.press("A", after=40)
    g.press("A", after=10)                      # Script 1
    g.wait(90)
    s = g.song()
    g.until_idle()
    return s


def main():
    g.boot()
    g.field()
    g.flag(FLAG_SYS_GAME_CLEAR, 1)
    g.flag(FLAG_NO_SEE, 1)
    g.flag(FLAG_NO_WILD, 1)
    g.flag(FLAG_NO_COLLIDE, 1)
    g.prep_party()
    g.flag(FLAG_FABA, 0)
    for t in ("TRAINER_HOLON_TOBIAS", "TRAINER_HOLON_KENJI", "TRAINER_HOLON_FABA"):
        g.flag(TRAINER_FLAGS_START + TRAINER[t], 0)

    # 4. table in ROM
    tbl = struct.unpack("<18H", g.e.read(g.e.sym("gTrainerApproachMusicStyles"), 36))
    vanilla = ["MUS_ENCOUNTER_MALE", "MUS_ENCOUNTER_FEMALE", "MUS_ENCOUNTER_GIRL", "MUS_ENCOUNTER_SUSPICIOUS",
               "MUS_ENCOUNTER_INTENSE", "MUS_ENCOUNTER_COOL", "MUS_ENCOUNTER_AQUA", "MUS_ENCOUNTER_MAGMA",
               "MUS_ENCOUNTER_SWIMMER", "MUS_ENCOUNTER_TWINS", "MUS_ENCOUNTER_ELITE_FOUR", "MUS_ENCOUNTER_HIKER",
               "MUS_ENCOUNTER_INTERVIEWER", "MUS_ENCOUNTER_RICH", "MUS_RG_ENCOUNTER_GIRL", "MUS_RG_ENCOUNTER_BOY",
               "MUS_RG_ENCOUNTER_ROCKET"]
    check(list(tbl[:17]) == [SONG[n] for n in vanilla] and tbl[17] == NEW,
          "gTrainerApproachMusicStyles: 17 vanilla entries unchanged, [HOLON] = %s" % name(tbl[17]))

    # 3. approach music through the normal function, boot map (not Sevii)
    for trainer, want in (("TRAINER_CALVIN_1", "MUS_ENCOUNTER_MALE"),
                          ("TRAINER_GRUNT_AQUA_HIDEOUT_7", "MUS_ENCOUNTER_AQUA"),
                          ("TRAINER_TAKAO", "MUS_ENCOUNTER_INTENSE"),
                          ("TRAINER_HOLON_IDO", "MUS_ORCHID_ENCOUNTER_HOLON")):
        s = debug_script1(trainer)
        check(s == SONG[want], "PlayTrainerEncounterMusic %s -> %s (want %s)" % (trainer, name(s), want))

    # 1. Tobias spots the player
    g.warp(*TOWER_2F, 0)
    g.until_idle()
    g.wait(30)
    log("  tower 2F", g.pos(), "map song", name(g.song()))
    g.go(14, 6)
    g.flag(FLAG_NO_SEE, 0)
    g.flag(FLAG_NO_COLLIDE, 0)
    g.walk("RIGHT", 1)
    heard, hit = watch_songs(240, stop_battle=False)
    g.snap("holon_music_1_tobias_spots")
    log("  pos", g.pos(), "text:", g.text()[:60])
    check(hit and NEW in heard, "Tobias spotting the player: songs %s, header == mus_orchid_encounter_holon: %s"
          % ([name(s) for s in heard], hit))
    opp = None
    for _ in range(40):
        if g.in_battle():
            break
        g.press("A", after=30)
    if g.in_battle() or g.wait_battle(600):
        opp = g.e.r16(g.e.sym("gTrainerBattleParameter") + 2)
        g.wait(200)
        log("  battle vs", opp, "song", name(g.song()))
        g.force_win()
    check(opp == TRAINER["TRAINER_HOLON_TOBIAS"], "the spotting battle is vs Tobias (%s)" % opp)
    g.until_idle()
    g.wait(60)
    g.flag(FLAG_NO_SEE, 1)
    g.flag(FLAG_NO_COLLIDE, 1)
    log("  map song after the battle:", name(g.song()))

    # 2. Faba
    g.go(11, 7)
    face("UP")
    g.press("A", after=40)
    heard, hit = [], False
    for _ in range(60):
        s = g.song()
        if s not in heard:
            heard.append(s)
        hit = hit or header_is_new()
        if g.in_battle():
            break
        if hit:
            g.snap("holon_music_2_faba_talk")
            break
        g.press("A", after=30)
    check(hit, "Faba's talk: songs %s, header == mus_orchid_encounter_holon: %s" % ([name(s) for s in heard], hit))
    finish_intro_and_battle()

    log("%d/%d PASS" % (sum(RESULTS), len(RESULTS)))
    open(os.path.join(OUT, "holon_music.log"), "w").write("\n".join(LOG) + "\n")
    g.close()


if __name__ == "__main__":
    main()
