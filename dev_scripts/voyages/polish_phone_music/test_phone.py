"""Headless check: Cynthia in the Rotom Phone CALL list before/after FLAG_CYNTHIA_BEATEN_AT_LAKE, her card, and two
calls (today's cafe rematch open / already done). Harness ROM from hbuild.sh. Run with the Pillow venv:
    <venv>/bin/python test_phone.py <dir with h.gba/h.elf>"""
import struct
import sys

from e2e_lib import E2E, log, MENU_ACTION_PHONE

ROM = sys.argv[1] + "/h"
FLAG_SYS_PHONE_ACTIVE = 0x863
FLAG_CYNTHIA_BEATEN_AT_LAKE, FLAG_CYNTHIA_CAFE_REMATCHED, VAR_CYNTHIA_CAFE_REMATCH_DAY = 0x1AA, 0x1DA, 0x4091
MC_HEADER_CYNTHIA, MAPSEC_CHANGU_CITY = 21, 8
CONTACTS_OFF = 3 * 32 * 32 * 2        # struct PhoneCall: 3 tilemaps, then contacts[]


class T(E2E):
    def contacts(self, n=80):
        base = self.e.r32("sCall") + CONTACTS_OFF
        raw = b"".join(self.e.read(base + o, 0x100) for o in range(0, n * 4, 0x100))
        out = []
        for i in range(n):
            special, mapsec, hid = struct.unpack_from("<BBH", raw, i * 4)
            if special == 0 and mapsec == 0 and hid == 0 and i > 0:
                break
            out.append((special, mapsec, hid))
        return out

    def open_call(self):
        self.field()
        self.press("START", after=40)
        n = self.e.r8("sNumStartMenuActions")
        acts = list(self.e.read(self.e.sym("sCurrentStartMenuActions"), n))
        cur = self.e.r8("sStartMenuCursorPos")
        for _ in range((acts.index(MENU_ACTION_PHONE) - cur) % n):
            self.press("DOWN", after=8)
        self.e.write(self.e.sym("sLastCursor"), b"\x01")          # CALL tile
        self.press("A", after=90)
        self.wait(60)
        self.press("A", after=30)
        ok = self.wait_cb2("CB2_Call", 900)
        self.wait(90)
        return ok

    def close_call(self):
        for _ in range(8):
            if self.at_cb2("CB2_Overworld"):
                break
            self.press("B", after=60)
        self.field()


t = T(ROM)
try:
    t.boot()
    t.flag(FLAG_SYS_PHONE_ACTIVE, 1)
    t.flag(FLAG_CYNTHIA_BEATEN_AT_LAKE, 0)
    log("open CALL before the flag:", t.open_call())
    before = t.contacts()
    log("  contacts", before, "cynthia listed:", any(c[0] == 1 and c[2] == MC_HEADER_CYNTHIA for c in before))
    t.snap("01_call_list_before_flag")
    t.close_call()

    t.flag(FLAG_CYNTHIA_BEATEN_AT_LAKE, 1)
    t.flag(FLAG_CYNTHIA_CAFE_REMATCHED, 0)
    log("open CALL after the flag:", t.open_call())
    after = t.contacts()
    idx = next(i for i, c in enumerate(after) if c[0] == 1 and c[2] == MC_HEADER_CYNTHIA)
    log("  contacts", after, "cynthia at", idx, after[idx])
    for _ in range(idx):
        t.press("DOWN", after=12)
    t.wait(30)
    t.snap("02_call_list_after_flag_cynthia_selected")
    t.press("A", after=60)
    t.snap("03_card_rematch_open")
    t.press("A", after=40)                      # CALL
    t.wait(30)
    t.snap("04_ringing")
    t.wait(160)
    log("  message:", repr(t.text()))
    t.wait(200)
    t.snap("05_talk_page1")
    for k in range(2):
        t.press("A", after=200)
        t.snap("06_talk_page%d" % (k + 2))
    t.press("A", after=60)                      # hang up -> card
    t.press("B", after=60)                      # -> list

    # already battled today
    t.e.frames(1)
    day = struct.unpack("<h", t.e.read(t.e.sym("gLocalTime"), 2))[0]
    t.flag(FLAG_CYNTHIA_CAFE_REMATCHED, 1)
    t.var(VAR_CYNTHIA_CAFE_REMATCH_DAY, day & 0xFFFF)
    log("  rtc day", day)
    t.close_call()
    log("reopen CALL (rematch done today):", t.open_call())
    for _ in range(idx):
        t.press("DOWN", after=12)
    t.wait(30)
    t.snap("07_call_list_rematch_done")
    t.press("A", after=60)
    t.snap("08_card_rematch_done")
    t.press("A", after=40)
    t.wait(360)
    log("  message:", repr(t.text()))
    t.snap("09_talk2_page1")
    for k in range(2):
        t.press("A", after=200)
        t.snap("10_talk2_page%d" % (k + 2))
finally:
    t.close()
