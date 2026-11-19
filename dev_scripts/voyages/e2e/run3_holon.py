"""Stage 3: Holon. Sail there, phone MAP, Researcher battle (Delta team), walk coast -> village -> lake, wild Delta,
Cynthia at the lake (encounter + vs music), sphere glow, sail home, Changu Battle Cafe shows Cynthia."""
import sys
from e2e_lib import *

TIKSI, CYN_BEATEN, CAFE_HIDE = 0x881, 0x1AA, 0x1AB
MUS_ENC_CYN, MUS_VS_CYN = 563, 564
g = E2E(sys.argv[1])


def is_delta(sp):
    return DELTA_FIRST <= sp <= DELTA_LAST


def obj_pal(tag):
    tags = struct.unpack("<16H", g.e.read(g.e.sym("sSpritePaletteTags"), 32))
    if tag not in tags:
        return None
    raw = g.e.read(g.e.sym("gPlttBufferUnfaded") + 0x200 + tags.index(tag) * 32, 32)
    return list(struct.unpack("<16H", raw))


def jasc555(path):
    rows = open(path).read().split("\n")[3:19]
    return [(int(r.split()[0]) >> 3) | ((int(r.split()[1]) >> 3) << 5) | ((int(r.split()[2]) >> 3) << 10) for r in rows]


try:
    g.boot()
    for f in (FLAG_SYS_GAME_CLEAR, FLAG_SYS_POKENAV_GET, FLAG_SYS_PHONE_ACTIVE, FLAG_NO_SEE, FLAG_NO_WILD):
        g.flag(f, 1)
    for k in ("EON", "SEVII", "HOLON", "NEWMOON", "FULLMOON"):
        g.flag(FLAGS[k], 1)
    g.flag(TIKSI, 0)
    log("cynthia flags at start", g.flag(CYN_BEATEN), g.flag(CAFE_HIDE))
    g.prep_party()
    g.warp(23, 0, 0); g.walk("DOWN", 1); g.wait(150)
    g.walk_to(5, 29); g.face("LEFT")
    log("-> holon", g.sail(2, "30_to_holon"))
    g.snap("31_holon_jetty")
    g.open_phone_map("32_holon_map_jetty")

    # Holon Researcher (Mirage Forest, 21,9): talk from below
    g.flag(FLAG_NO_COLLIDE, 1); g.go(21, 10); g.flag(FLAG_NO_COLLIDE, 0)
    log("  trainer flag TRAINER_HOLON_IDO (0x519) in save:", g.flag(0x519))
    g.face("UP"); g.press("A", after=60)
    for _ in range(10):
        if g.in_battle():
            break
        g.press("A", after=60)
    log("researcher battle", g.wait_battle(1500))
    g.wait(240)
    sp = g.battlers(); log("  battlers", sp, "foe is Delta:", is_delta(sp[1]), "song", g.song())
    g.snap("33_researcher_battle")
    log("  won ->", g.force_win())

    # walk: coast -> village -> lake
    g.flag(FLAG_NO_COLLIDE, 1)
    g.go(43, 20); g.cross("RIGHT"); log("village", g.pos(), folder(*g.pos()[2:]))
    g.open_phone_map("34_holon_village_map")
    g.go(23, 71); g.cross("DOWN"); log("lake", g.pos(), folder(*g.pos()[2:]), "VISITED_LAKE", g.flag(0x281))
    g.open_phone_map("35_holon_lake_map")

    # wild encounter in the lake grass
    g.go(24, 28); g.wait(30)
    pal = obj_pal(0x113A)
    log("sphere before Cynthia: loaded", pal is not None, "= plain pal:", pal == jasc555(os.path.join(ROOT, "graphics/object_events/palettes/holon_sphere.pal")))
    g.snap("35b_sphere_before")
    for attempt in range(6):
        g.flag(FLAG_NO_COLLIDE, 1); g.go(38, 4); g.flag(FLAG_NO_WILD, 0)
        for i in range(300):
            g.walk("RIGHT" if i % 2 == 0 else "LEFT", 1)
            if g.in_battle() or g.wait_battle(20):
                break
        g.wait(300)
        sp = g.battlers()
        log("wild battle", attempt, g.in_battle(), "battlers", sp, "foe is Delta:", is_delta(sp[1]), "song", g.song())
        g.flag(FLAG_NO_WILD, 1)
        if is_delta(sp[1]):
            g.snap("36_wild_delta")
        log("  won ->", g.force_win())
        if is_delta(sp[1]):
            break

    # Cynthia at (24,35): talk from above
    g.go(24, 34); g.flag(FLAG_NO_COLLIDE, 0); g.face("DOWN")
    g.snap("37_lake_cynthia_before")
    g.press("A", after=90)
    log("  encounter song", g.song(), "(want %d)" % MUS_ENC_CYN, repr(g.text()[:50]))
    g.snap("38_cynthia_encounter")
    for _ in range(25):
        if g.in_battle():
            break
        g.press("A", after=60)
    g.wait_battle(600); g.wait(300)
    sp = g.battlers(); log("cynthia battle", g.in_battle(), "battlers", sp, "song", g.song(), "(want %d)" % MUS_VS_CYN)
    g.snap("39_cynthia_battle")
    log("  won ->", g.force_win(30))
    g.until_idle(60); g.wait(120)
    log("after: FLAG_CYNTHIA_BEATEN_AT_LAKE", g.flag(CYN_BEATEN), "cafe hide", g.flag(CAFE_HIDE), "pos", g.pos())
    g.snap("40_lake_after_cynthia_gone")
    g.flag(FLAG_NO_COLLIDE, 1); g.go(24, 28); g.face("UP"); g.wait(30)
    pal = obj_pal(0x113A)
    log("sphere palette loaded:", pal is not None, "= glow pal:", pal == jasc555(os.path.join(ROOT, "graphics/object_events/palettes/holon_sphere_glow.pal")),
        "= plain pal:", pal == jasc555(os.path.join(ROOT, "graphics/object_events/palettes/holon_sphere.pal")))
    g.snap("40b_sphere_glowing")

    # home: lake -> village -> coast -> jetty Sailor
    g.flag(FLAG_NO_COLLIDE, 1)
    g.go(23, 0); g.cross("UP"); log("village", g.pos())
    x, y = g.pos()[:2]; g.go(0, y if 13 <= y <= 50 else 30); g.cross("LEFT"); log("coast", g.pos())
    g.go(4, 36); g.flag(FLAG_NO_COLLIDE, 0); g.face("LEFT")
    log("-> home", g.sail(0, "41_holon_home"))
    log("FLAG_VISITED_TIKSI after Holon", g.flag(TIKSI))

    # Changu City Battle Cafe
    g.warp(21, 121, 0); g.wait(60); log("cafe", g.pos(), "cafe hide flag", g.flag(CAFE_HIDE))
    g.snap("42_changu_cafe_cynthia")
finally:
    open(os.path.join(HERE, "run3.log"), "w").write("\n".join(LOG) + "\n")
    g.close()
