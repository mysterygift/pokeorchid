"""
Animated preview of the satchel bag: BG3 grid scroll + pocket switching.

Timeline is in GBA frames (60 fps); one GIF frame every 2 GBA frames.
Pocket switch (16 frames):
  * gold ring travels along the wheel from the old button to the new one (ease-out, 12f),
    then the new button shows its selected frame;
  * satchel shows the closed frame and rises from y-5, wiggling (Gen 3 shake), then opens
    on the new pocket;
  * list text/description clear and the pill rows wipe in top to bottom.
usage: anim_bag.py OUT.gif [theme]
"""
import math
import sys
from PIL import Image
import bag_screen as B
from mock_bag import render, ITEMS

THEME = sys.argv[2] if len(sys.argv) > 2 else "male"
BALLS = [("Poké Ball", 12, "poke_ball"), ("Great Ball", 4, "great_ball"), ("Ultra Ball", 1, "ultra_ball")]
TMS = [("№01 Focus Punch", "", "tm"), ("№06 Toxic", "", "tm"), ("№28 Dig", "", "tm"), ("№45 Attract", "", "tm")]
CONTENT = {
    0: dict(items=ITEMS, cursor=1, desc=None),
    1: dict(items=BALLS, cursor=0, desc="A device for catching\nwild Pokémon. It's\nthrown like a ball."),
    2: dict(items=TMS, cursor=2, desc="The user tunnels\nunderground, then\nattacks next turn."),
}
# (start frame, from pocket, to pocket, direction)
SWITCHES = [(70, 0, 1, +1), (170, 1, 2, +1), (270, 2, 1, -1)]
END = 350
SWITCH_LEN, RING_LEN = 16, 12


def ring_pos(a, b, d, u):
    cx, cy = B.WHEEL_C
    a0 = -90 + 72 * a
    a1 = a0 + 72 * d
    e = 1 - (1 - u) ** 2
    ang = math.radians(a0 + (a1 - a0) * e)
    return (cx + B.BUTTON_R * math.cos(ang), cy + B.BUTTON_R * math.sin(ang))


def state_at(f):
    pocket, ov = 0, {}
    for (s, a, b, d) in SWITCHES:
        if f >= s:
            pocket = b
            t = f - s
            if t < SWITCH_LEN:
                ov = {"hide_list_text": True, "rows_visible": t * B.ROWS // SWITCH_LEN}
                if t < RING_LEN:
                    ov["ring"] = ring_pos(a, b, d, t / RING_LEN)
                    ov["sel_button"] = -1
                if t < 6:
                    ov["satchel_frame"] = 0
                    ov["satchel_dy"] = -5 + t
                ov["satchel_rot"] = 5 * math.sin(t * math.pi / 3) * max(0.0, 1 - t / RING_LEN)
    return pocket, ov


def main():
    out = sys.argv[1]
    frames = []
    for f in range(0, END, 2):
        pocket, ov = state_at(f)
        c = CONTENT[pocket]
        im = render(THEME, pocket, cursor=c["cursor"], items=c["items"], desc=c["desc"],
                    grid_scroll=f // 4, overrides=ov)
        frames.append(im.convert("RGB").resize((B.W * 2, B.H * 2), Image.NEAREST))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=33, loop=0, optimize=False)
    print("frames:", len(frames))


main()
