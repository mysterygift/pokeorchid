"""Headless helpers for the voyage checks (wraps dev_scripts/mgba_headless). Run with the Pillow venv."""
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "dev_scripts", "mgba_headless"))
from gba import Emu   # noqa: E402

SHOTS = os.path.join(HERE, "shots")
FLAG_SYS_GAME_CLEAR = 0x864
FLAGS = dict(EON=0x2B, SEVII=0x2C, HOLON=0x2D, NEWMOON=0x2E, FULLMOON=0x2F,
             CAUGHT_LATIAS=0x3A, CAUGHT_LATIOS=0x3B, CAUGHT_DARKRAI=0x3C, CAUGHT_CRESSELIA=0x3D,
             HIDE_LATIAS=0x3E, HIDE_LATIOS=0x3F, HIDE_DARKRAI=0x68, HIDE_CRESSELIA=0xE9,
             ITEM_LATIASITE=0x450, ITEM_LATIOSITE=0x451)

CHARS = {0x00: " ", 0xFE: "\n", 0xFA: "\n", 0xFB: "\n\n", 0xAD: ".", 0xB8: ",", 0xAB: "!", 0xAC: "?", 0xB4: "'",
         0xB0: "…", 0xBA: "/", 0xAE: "-", 0xF0: ":"}
for i in range(26):
    CHARS[0xBB + i] = chr(65 + i)
    CHARS[0xD5 + i] = chr(97 + i)
for i in range(10):
    CHARS[0xA1 + i] = chr(48 + i)


def decode(b):
    out = ""
    for c in b:
        if c == 0xFF:
            break
        out += CHARS.get(c, "?")
    return out


class Game:
    def __init__(self, rom):
        self.e = Emu(rom + ".gba", rom + ".elf")

    # ---- memory
    def sb1(self):
        return self.e.r32("gSaveBlock1Ptr")

    def flag(self, fid, value=None):
        a = self.sb1() + 0x1270 + fid // 8
        b = self.e.read(a, 1)[0]
        if value is None:
            return (b >> (fid % 8)) & 1
        b = (b | (1 << (fid % 8))) if value else (b & ~(1 << (fid % 8)))
        self.e.write(a, bytes([b & 0xFF]))

    def var(self, vid, value=None):
        a = self.sb1() + 0x139C + (vid - 0x4000) * 2
        if value is None:
            return struct.unpack("<H", self.e.read(a, 2))[0]
        self.e.write(a, struct.pack("<H", value))

    def pos(self):
        sb1 = self.sb1()
        x, y = struct.unpack("<hh", self.e.read(sb1, 4))
        g, n = self.e.read(sb1 + 4, 2)
        return (x, y, g, n)

    def text(self):
        return decode(self.e.read(self.e.sym("gStringVar4"), 0x100)).strip()

    def special_var(self, name):
        return self.e.r16(name)

    def script_running(self):
        return self.e.r8("sGlobalScriptContextStatus") != 2 or self.e.r8("sLockFieldControls") != 0

    def cb2(self):
        return self.e.r32("gMain") if False else self.e.r32(self.e.sym("gMain") + 4)

    # ---- input
    def press(self, *k, after=12, hold=4):
        self.e.press(*k, after=after, hold=hold)

    def wait(self, n):
        self.e.frames(n)

    def walk(self, d, n=1):
        for _ in range(n):
            self.e.press(d, hold=16, after=6)

    def face(self, d):
        self.e.press(d, hold=2, after=8)

    def until_idle(self, maxpress=40, key="B"):
        for _ in range(maxpress):
            if not self.script_running():
                return True
            self.press(key, after=20)
        return not self.script_running()

    def shot(self, name):
        os.makedirs(SHOTS, exist_ok=True)
        return self.e.shot(os.path.join(SHOTS, name + ".png"))

    def close(self):
        self.e.close()

    # ---- boot / warp
    def boot(self):
        e = self.e
        e.frames(400)
        e.press("START", after=120)
        e.press("A", after=240)
        e.press("A", after=300)
        # the user's save lands in a nickname prompt (memory: reference-mgba-headless)
        e.press("B", after=40)
        e.press("START", after=40)
        e.press("A", after=60)
        for _ in range(4):
            e.press("B", after=30)
        self.until_idle()

    def warp(self, group, num, warp=0):
        e = self.e
        e.press("R", "START", after=60)
        e.press("A", after=30)
        e.press("DOWN")
        e.press("A", after=30)
        for _ in range(group):
            e.press("UP", after=6)
        e.press("A", after=20)
        for _ in range(num):
            e.press("UP", after=6)
        e.press("A", after=20)
        for _ in range(warp):
            e.press("UP", after=6)
        e.press("A", after=240)

    def set_hour(self, hour):
        """Shift the RTC so the local clock reads `hour` (Saveblock2 localTimeOffset)."""
        raise NotImplementedError
