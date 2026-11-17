"""
Animated previews of the Orchid PC storage (GBA frames at 60 fps, one GIF frame per 2 GBA frames).

box_switch.gif  R: right chevron lights 8 frames; BG2 slots + icons scroll left 6px/frame x 32 frames
                (vanilla scrollSpeed/scrollTimer), BOX 2 slides in; title swaps at the halfway point; the ring
                hides during the slide. Then L slides back the other way.
pickup.gif      A: ring flashes, the mon rises 14px over 8 frames (ease-out) with its shadow; the cursor moves
                6 frames per slot (vanilla cursorMoveSteps) carrying it (1px bob every 16 frames); A drops it.
usage: anim_pc.py OUT_DIR
"""
import os
import sys
from PIL import Image
import mock_pc as M
import pc_ext as P

SCALE = 2


def save_gif(frames, path):
    fr = [f.convert("RGB").resize((240 * SCALE, 160 * SCALE), Image.NEAREST) for f in frames]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=33, loop=0, optimize=False)
    print(path, len(fr), "frames")


def ease_out(t):
    return 1 - (1 - t) ** 2


def box_switch_gif(path):
    R, L = 30, 112
    SLIDE = 32
    end = L + SLIDE + 40
    disp0, disp1 = P.BOX1[7], P.BOX2[7]
    frames = []
    for f in range(0, end, 2):
        kw = dict(grid_scroll=f // 4)
        if f < R:
            im = M.render(box=0, cursor=("box", 7), **kw)
        elif f < R + SLIDE:
            k = f - R + 1
            im = M.render(box=0, cursor=None, display=disp0, next_box=1, box_dx=-6 * k,
                          chev_flash=1 if f < R + 8 else None, **kw)
        elif f < L:
            im = M.render(box=1, cursor=("box", 7), **kw)
        elif f < L + SLIDE:
            k = f - L + 1
            im = M.render(box=1, cursor=None, display=disp1, next_box=0, box_dx=6 * k, next_dx=-M.BOX_SLIDE,
                          chev_flash=0 if f < L + 8 else None, **kw)
        else:
            im = M.render(box=0, cursor=("box", 7), **kw)
        frames.append(im)
    save_gif(frames, path)


def pickup_gif(path):
    B1 = P.BOX1
    mud = B1[7]
    A1, LIFT_N = 24, 8
    moves = [(48, 7, 8), (66, 8, 9), (84, 9, 10)]       # (start frame, from, to), 6 frames each
    A2 = 112
    end = A2 + LIFT_N + 50
    dropped = {k: v for k, v in B1.items() if k != 7}
    dropped[10] = mud
    frames = []
    for f in range(0, end, 2):
        kw = dict(grid_scroll=f // 4)
        if f < A1:
            im = M.render(cursor=("box", 7), **kw)
        elif f < A2:
            # carried: work out the cursor position
            pos = P.centre(7)
            slot = 7
            for s0, a, b in moves:
                if f >= s0 + 6:
                    pos, slot = P.centre(b), b
                elif f >= s0:
                    t = (f - s0) / 6
                    pa, pb = P.centre(a), P.centre(b)
                    pos = (pa[0] + (pb[0] - pa[0]) * ease_out(t), pa[1])
                    slot = b
            lift = int(round(14 * ease_out(min(1.0, (f - A1) / LIFT_N))))
            if f >= A1 + LIFT_N and ((f - A1 - LIFT_N) // 16) % 2:
                lift += 1
            im = M.render(cursor=("box", slot), cur_px=pos, held=mud, lift=lift, hide_slots=(7,),
                          ring_flash=f < A1 + 4, **kw)
        elif f < A2 + LIFT_N:
            lift = int(round(14 * (1 - ease_out((f - A2) / LIFT_N))))
            im = M.render(cursor=("box", 10), held=mud, lift=lift, hide_slots=(7,), **kw)
        else:
            im = M.render(cursor=("box", 10), contents_override=dropped, ring_flash=f < A2 + LIFT_N + 4, **kw)
        frames.append(im)
    save_gif(frames, path)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    box_switch_gif(os.path.join(out, "box_switch.gif"))
    pickup_gif(os.path.join(out, "pickup.gif"))
