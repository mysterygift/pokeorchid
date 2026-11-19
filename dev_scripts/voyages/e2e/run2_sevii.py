"""Stage 2: Sevii. Sail Wavebreak -> One Island harbour, phone MAP on the three clusters + two straits, then home via
the harbour ferryman's "Wavebreak & beyond"."""
import sys
from e2e_lib import *

TIKSI = 0x881
g = E2E(sys.argv[1])


def setup():
    g.boot()
    for f in (FLAG_SYS_GAME_CLEAR, FLAG_SYS_POKENAV_GET, FLAG_SYS_PHONE_ACTIVE, FLAG_NO_SEE, FLAG_NO_WILD, FLAG_NO_COLLIDE):
        g.flag(f, 1)
    for k in ("EON", "SEVII", "HOLON", "NEWMOON", "FULLMOON"):
        g.flag(FLAGS[k], 1)
    log("save had FLAG_VISITED_TIKSI =", g.flag(TIKSI), "-> cleared for the run")
    g.flag(TIKSI, 0)


def into_route(direction, steps_after):
    x, y, gr, n = g.pos()
    for _ in range(60):
        g.walk(direction, 1)
        if g.pos()[2:] != (gr, n):
            break
    g.walk(direction, steps_after)
    g.wait(30)
    log("  in route", g.pos())


try:
    setup()
    g.warp(23, 0, 0); g.walk("DOWN", 1); g.wait(150)
    g.walk_to(5, 29); g.face("LEFT")
    log("-> sevii", g.sail(1, "10_to_sevii"))
    g.snap("11_one_island_harbour")
    log("map", g.open_phone_map("12_sevii123_harbour_map"))
    g.walk("UP", 2); g.wait(150); log("one island town", g.pos(), "VISITED_ONE_ISLAND", g.flag(0x264))
    g.open_phone_map("13_sevii123_one_island_map")
    g.warp(25, 1, 0); log("two island", g.pos(), "VISITED_TWO", g.flag(0x265))
    g.walk("DOWN", 1)                    # row 10: no door between here and the west edge
    into_route("LEFT", 18)
    g.open_phone_map("14_one_two_strait_map")
    g.warp(25, 4, 0); log("five island", g.pos())
    g.walk("UP", 4)                      # row 10 -> route C row 16
    into_route("LEFT", 6)
    g.open_phone_map("15_four_five_strait_five_end")
    g.walk_to(20, 11); g.open_phone_map("16_four_five_strait_middle")
    g.warp(25, 3, 0); log("four island", g.pos())
    g.open_phone_map("17_sevii45_four_island_map")
    g.warp(25, 6, 0); log("seven island", g.pos())
    g.open_phone_map("18_sevii67_seven_island_map")
    g.walk_to(11, 12)                    # row 12 -> route D row 6
    into_route("RIGHT", 10)
    g.open_phone_map("19_six_seven_strait_map")
    g.flag(FLAG_NO_COLLIDE, 0)           # facing the Sailor must not walk through him
    g.warp(25, 38, 1); log("harbour again", g.pos())
    g.face("DOWN"); g.press("A", after=60); g.wait(40)
    g.snap("20_harbour_ferry_menu")
    g.menu_pick(6)
    g.until_text("Where are we headed", maxa=6)
    g.snap("21_wavebreak_and_beyond_menu")
    g.menu_pick(0); g.wait(30); log("  text", repr(g.text()[:40]))
    g.press("A", after=60); g.press("A", after=60)
    log("  cutscene", g.wait_cb2("MainCB2_SeaGallop"))
    g.wait_cb2("CB2_Overworld", 3000); g.wait(150); g.until_idle()
    log("home", g.pos())
    g.snap("22_sevii_home_wavebreak")
    log("FLAG_VISITED_TIKSI after Sevii", g.flag(TIKSI))
finally:
    open(os.path.join(HERE, "run2.log"), "w").write("\n".join(LOG) + "\n")
    g.close()
