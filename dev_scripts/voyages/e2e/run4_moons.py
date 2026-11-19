"""Stage 4: Newmoon and Fullmoon round trips with the phone MAP, plus Eon -> Holon island hop (island menus)."""
import sys
from e2e_lib import *

TIKSI = 0x881
g = E2E(sys.argv[1])
try:
    g.boot()
    for f in (FLAG_SYS_GAME_CLEAR, FLAG_SYS_POKENAV_GET, FLAG_SYS_PHONE_ACTIVE, FLAG_NO_SEE, FLAG_NO_WILD):
        g.flag(f, 1)
    for k in ("EON", "SEVII", "HOLON", "NEWMOON", "FULLMOON"):
        g.flag(FLAGS[k], 1)
    g.flag(TIKSI, 0)
    g.warp(23, 0, 0); g.walk("DOWN", 1); g.wait(150)
    g.walk_to(5, 29); g.face("LEFT")
    log("-> newmoon", g.sail(3, "50_to_newmoon"))
    g.snap("51_newmoon_arrival")
    g.open_phone_map("52_newmoon_map")
    g.face("RIGHT")
    log("-> home", g.sail(0, "53_newmoon_home"))
    g.face("LEFT")
    log("-> fullmoon", g.sail(4, "54_to_fullmoon"))
    g.snap("55_fullmoon_arrival")
    g.open_phone_map("56_fullmoon_map")
    g.face("LEFT")
    log("-> home", g.sail(0, "57_fullmoon_home"))
    log("FLAG_VISITED_TIKSI after moons", g.flag(TIKSI))
    g.flag(TIKSI, 1)
    g.open_phone_map("58_wavebreak_map_tiksi_switch_hint")
finally:
    open(os.path.join(HERE, "run4.log"), "w").write("\n".join(LOG) + "\n")
    g.close()
