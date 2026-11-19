"""Stage 1: Wavebreak dock Sailor, all 5 codes, Eon round trip + phone MAP on Eon and in Wavebreak."""
import sys
from e2e_lib import *

g = E2E(sys.argv[1])
try:
    g.boot()
    for f in (FLAG_SYS_GAME_CLEAR, FLAG_SYS_POKENAV_GET, FLAG_SYS_PHONE_ACTIVE, FLAG_NO_SEE, FLAG_NO_WILD, FLAG_NO_COLLIDE):
        g.flag(f, 1)
    for k in ("EON", "SEVII", "HOLON", "NEWMOON", "FULLMOON"):
        g.flag(FLAGS[k], 0)
    g.warp(23, 0, 0); g.walk("DOWN", 1); g.wait(150)      # Sailor's hut -> Wavebreak (temp flags reloaded)
    log("wavebreak", g.pos())
    g.walk_to(5, 29); g.face("LEFT")
    g.press("A", after=60); g.to_menu(); g.snap("01_wavebreak_menu_locked")
    n = 0
    for code in ("SOULDEW", "seagallop", "Delta", "NIGHTMARE", "LunarWing"):
        ok, t = g.enter_code(n, code)
        n += 1
        log("code", code, ok, repr(t[:50]))
        g.to_menu()
    log("unlocked", {k: g.flag(FLAGS[k]) for k in ("EON", "SEVII", "HOLON", "NEWMOON", "FULLMOON")})
    g.snap("02_wavebreak_menu_all_unlocked")
    g.press("B", after=40); g.field()
    g.open_phone_map("03_wavebreak_phone_map_tosa")
    g.face("LEFT")
    log("-> eon", g.sail(0, "04_to_eon"))
    g.snap("05_eon_arrival")
    log("FLAG_VISITED_TIKSI", g.flag(0x881))
    log("map", g.open_phone_map("06_eon_phone_map"))
    g.face("LEFT")
    log("-> home", g.sail(0, "07_eon_home"))
    g.snap("08_back_wavebreak")
finally:
    open(os.path.join(HERE, "run1.log"), "w").write("\n".join(LOG) + "\n")
    g.close()
