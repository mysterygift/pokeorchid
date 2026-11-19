"""Headless check: Sevii battle music. Harness ROM from hbuild.sh (debug Script 1 = callnative
PlayTrainerEncounterMusic for the poked TRAINER_BATTLE_PARAM.opponentA: Calvin (Male), Gabrielle (Female), Shelly (Aqua)). Run with the Pillow venv:
    <venv>/bin/python test_music.py <dir with h.gba/h.elf>
Song ids are read from gMPlayInfo_BGM.songHeader (looked up in gSongTable)."""
import struct
import sys

from e2e_lib import E2E, log

ROM = sys.argv[1] + "/h"
NAMES = {}
for line in open("../../../include/constants/songs.h"):
    p = line.split()
    if len(p) >= 3 and p[0] == "#define" and p[1].startswith("MUS_") and p[2].isdigit():
        NAMES.setdefault(int(p[2]), p[1])
RESULTS = []


class T(E2E):
    def sname(self):
        return NAMES.get(self.song(), self.song())

    def debug_menu(self, main_idx, sub_idx, poke=None):
        self.field()
        self.press("R", "START", after=60)
        for _ in range(main_idx):
            self.press("DOWN", after=6)
        self.press("A", after=40)
        if poke:
            poke()
        for _ in range(sub_idx):
            self.press("DOWN", after=6)
        self.press("A", after=10)

    def check(self, what, expect):
        got = self.sname()
        ok = got == expect
        RESULTS.append((what, expect, got, ok))
        log("  %-46s expect %-36s got %-36s %s" % (what, expect, got, "OK" if ok else "FAIL"))
        return ok

    def finish_battle(self, label):
        """win; log every song heard on the way out"""
        heard = []
        for _ in range(3):
            self.press("B", after=60)
        for _ in range(16):
            if not self.in_battle():
                break
            b1 = self.e.sym("gBattleMons") + 140
            ep = self.e.r32("gEnemyPartyPtr")
            for i in range(1, 6):
                self.e.write(ep + i * 100 + 0x56, b"\x00\x00")
            self.e.write(b1 + 0x28, b"\x01\x00")
            self.press("A", after=30)
            self.press("A", after=120)
            s = self.sname()
            if s not in heard:
                heard.append(s)
            for _ in range(8):
                if not self.in_battle():
                    break
                self.press("B", after=50)
                s = self.sname()
                if s not in heard:
                    heard.append(s)
        log("  %s songs while finishing: %s" % (label, heard))
        self.field(80)
        return heard


def session(fn):
    t = T(ROM)
    try:
        t.boot()
        t.prep_party()
        fn(t)
    except Exception as ex:          # keep going with the next scenario
        log("  !! scenario failed:", repr(ex))
    finally:
        t.close()


def to_sevii(t):
    t.warp(25, 0, 0)                            # One Island
    t.wait(120)
    t.field()
    log("warped", t.pos(), "mapsec", t.e.r8(t.e.sym("gMapHeader") + 0x14))


def control(t):
    log("boot at", t.pos(), "mapsec", t.e.r8(t.e.sym("gMapHeader") + 0x14))
    t.debug_menu(2, 13)
    t.wait_battle()
    t.wait(200)
    t.check("wild battle, boot map (control)", "MUS_VS_WILD")


def wild(t):
    to_sevii(t)
    t.snap("20_one_island")
    t.debug_menu(2, 13)
    t.wait_battle()
    t.wait(200)
    t.check("wild battle, One Island", "MUS_ORCHID_SEVII_VS_WILD")
    t.snap("21_sevii_wild_battle")
    t.force_win()
    log("  after win:", t.sname(), t.pos())


def try_battle(t):
    to_sevii(t)
    t.debug_menu(6, 5, poke=lambda: t.e.write(t.e.r32("sDebugMenuListData") + 736, struct.pack("<hh", 26, -1)))
    t.wait_battle()
    t.wait(250)
    t.check("Try Battle 26, One Island", "MUS_ORCHID_SEVII_VS_TRAINER")
    t.snap("22_sevii_try_battle")


TRAINERS = {}
for line in open("../../../include/constants/opponents.h"):
    q = line.split()
    if len(q) >= 3 and q[0] == "#define" and q[1].startswith("TRAINER_") and q[2].isdigit():
        TRAINERS[q[1]] = int(q[2])


def encounters(t):
    to_sevii(t)
    for i, (trainer, enc) in enumerate((("TRAINER_CALVIN_1", "MUS_ORCHID_SEVII_ENCOUNTER_BOY"),
                                        ("TRAINER_GABRIELLE_1", "MUS_ORCHID_SEVII_ENCOUNTER_GIRL"),
                                        ("TRAINER_SHELLY_WEATHER_INSTITUTE", "MUS_ORCHID_SEVII_ENCOUNTER_ROCKET"))):
        t.e.write(t.e.sym("gTrainerBattleParameter") + 2, struct.pack("<H", TRAINERS[trainer]))
        t.e.write(t.e.sym("gApproachingTrainerId"), b"\x00")
        t.debug_menu(5, 0)
        t.wait(90)
        t.check("approach music %s, One Island" % trainer, enc)
        t.until_idle()


def encounter_control(t):
    t.e.write(t.e.sym("gTrainerBattleParameter") + 2, struct.pack("<H", TRAINERS["TRAINER_CALVIN_1"]))
    t.e.write(t.e.sym("gApproachingTrainerId"), b"\x00")
    t.debug_menu(5, 0)
    t.wait(90)
    t.check("approach music TRAINER_CALVIN_1, boot map (control)", "MUS_ENCOUNTER_MALE")


for fn in (control, wild, try_battle, encounter_control, encounters):
    session(fn)
log("RESULT", sum(r[3] for r in RESULTS), "/", len(RESULTS), "passed")
