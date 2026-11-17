#!/usr/bin/env python3
"""Both new exteriors side by side on a real grass / path / tree backdrop.

    python town_scene.py      # writes out/town_scene_3x.png
"""
import centre_exterior
import mart_exterior
from mock import save
from town import Town

W, H = 24, 12


def build():
    c, m = centre_exterior.build(), mart_exterior.build()
    t = Town(W, H)
    for x, y in ((0, 0), (0, 3), (9, 0), (11, 1), (21, 0), (22, 3)):
        t.tree(x, y)
    t.path(0, 6, W - 1, 8)
    t.path(10, 8, 11, H - 1)
    t.flowers([(2, 10), (3, 10), (7, 10), (15, 10), (16, 10), (20, 10), (9, 4), (12, 5)])
    st = t.stage()
    cx, cy = 3, 2                       # Centre: bottom row (cy + 3) is its covered walkway
    mx, my = 14, 2                      # Mart: bottom row is the storefront, props stand in front
    st.add(c["under"], cx * 16, cy * 16)
    st.add(c["over"], cx * 16, cy * 16, over=True)
    for dx in (0, 4):
        st.add(c["props"]["palm"], (cx + dx) * 16, (cy + 4) * 16 - 16)
    st.add(m["under"], mx * 16, my * 16)
    st.add(m["over"], mx * 16, my * 16, over=True)
    ground = my + 4
    st.add(m["props"]["ice_chest"], (mx + 0) * 16, ground * 16 - 16)
    st.add(m["props"]["bin"], (mx + 1) * 16, ground * 16 - 16)
    st.add(m["props"]["vending"], (mx + 4) * 16, ground * 16 - 16)
    st.npc("brendan/walking.png", "brendan.pal", 1, cx + c["door_col"], cy + 3)
    st.npc("woman_1.png", "npc_1.pal", 1, mx + m["door_col"], ground)
    st.npc("boy_1.png", "npc_3.pal", 2, 12, 7)
    st.npc("old_man.png", "npc_4.pal", 0, 9, 6)
    st.npc("little_girl.png", "npc_2.pal", 2, 21, 7)
    return st


if __name__ == "__main__":
    print(save(build().render(), "town_scene_3x.png"))
