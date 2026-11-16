"""
Animated previews of the Orchid Pokédex. Timeline in GBA frames (60 fps); one GIF
frame every 2 GBA frames (duration 33 ms), saved at 2x.

dex_scroll.gif — D-pad down held/tapped through the TOSA list:
  * a press every 12 frames; the gold cursor pill moves down a row instantly;
  * once the cursor is 2 rows from the bottom the list scrolls instead
    (BG2VOFS += 2px/frame, 8 frames per row) and the cursor stays put;
  * the dais pic swaps on every press: the new pic slides in from 16px left,
    ease-out over 6 frames (OBJ x only); unseen entries show the ink silhouette;
  * BG3 grid scrolls 1px / 4 frames throughout.
dex_open.gif — A on the list opens the INFO page, then B returns:
  * 4f gold row flash (SELECT -> SELECT_LIGHT palette swap);
  * 12f darken BG0-2 to black (BLDY, OBJ + BG3 untouched) while the pic glides
    to the entry dais; swap screens; 12f brighten. B reverses the same steps.

usage: anim_dex.py OUT_DIR
"""
import os
import sys
from PIL import Image
import mock_dex as M

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

PRESS_EVERY, SCROLL_LEN, SLIDE_LEN = 12, 8, 6


def ease(u):
    return 1 - (1 - u) ** 2


def save_gif(frames, name):
    fr = [f.convert("RGB").resize((M.W * 2, M.H * 2), Image.NEAREST) for f in frames]
    fr[0].save(os.path.join(OUT, name), save_all=True, append_images=fr[1:], duration=33, loop=0,
               optimize=False)
    print(name, len(fr), "frames")


def scroll_gif():
    start, presses, end_hold = 30, 14, 40
    events = []                    # (frame, cursor, top_before, top_after)
    cursor, top = 0, 0
    for k in range(presses):
        f = start + k * PRESS_EVERY
        nc = cursor + 1
        nt = M.first_visible(nc, top)
        events.append((f, nc, top, nt))
        cursor, top = nc, nt
    end = start + presses * PRESS_EVERY + end_hold
    frames = []
    for f in range(0, end, 2):
        cur, scroll_px, dx = 0, 0, 0
        for (ef, nc, t0, t1) in events:
            if f >= ef:
                cur = nc
                t = f - ef
                scroll_px = t0 * M.ROW_H + min(t * 2, (t1 - t0) * M.ROW_H) if t1 != t0 else t1 * M.ROW_H
                dx = -int(round(16 * (1 - ease(min(1.0, t / SLIDE_LEN)))))
        frames.append(M.render_list(cursor=cur, scroll_px=scroll_px, grid_scroll=f // 4, sprite_dx=dx))
    save_gif(frames, "dex_scroll.gif")


def open_gif():
    idx = 0                                     # Treecko
    list_pos = (M.DAIS_C[0], M.DAIS_C[1] + int(M.DAIS_IN * 0.55) + 3)
    ent_pos = (M.E_DAIS_C[0], M.E_DAIS_C[1] + int(M.E_DAIS_IN * 0.55) + 3)
    A, FLASH, FADE = 24, 4, 12
    B = A + FLASH + 2 * FADE + 70
    end = B + 2 * FADE + 40
    frames = []
    for f in range(0, end, 2):
        g = f // 4
        if f < A:
            im = M.render_list(cursor=idx, grid_scroll=g)
        elif f < A + FLASH:
            im = M.render_list(cursor=idx, grid_scroll=g, flash=(f - A) < 2)
        elif f < A + FLASH + FADE:
            u = (f - A - FLASH) / FADE
            e = ease(u)
            pos = (round(list_pos[0] + (ent_pos[0] - list_pos[0]) * e),
                   round(list_pos[1] + (ent_pos[1] - list_pos[1]) * e))
            im = M.render_list(cursor=idx, grid_scroll=g, fade=u, sprite_pos=pos)
        elif f < A + FLASH + 2 * FADE:
            u = (f - A - FLASH - FADE) / FADE
            im = M.render_entry(entry_index=idx, grid_scroll=g, fade=1 - u)
        elif f < B:
            im = M.render_entry(entry_index=idx, grid_scroll=g)
        elif f < B + FADE:
            u = (f - B) / FADE
            e = ease(u)
            im = M.render_entry(entry_index=idx, grid_scroll=g, fade=u, show_sprite=False)
            pos = (round(ent_pos[0] + (list_pos[0] - ent_pos[0]) * e),
                   round(ent_pos[1] + (list_pos[1] - ent_pos[1]) * e))
            spr = M.D.mon_pic("treecko")
            im.alpha_composite(spr, (pos[0] - 32, pos[1] - M.D.sprite_bottom(spr)))
        elif f < B + 2 * FADE:
            u = (f - B - FADE) / FADE
            im = M.render_list(cursor=idx, grid_scroll=g, fade=1 - u)
        else:
            im = M.render_list(cursor=idx, grid_scroll=g)
        frames.append(im)
    save_gif(frames, "dex_open.gif")


if __name__ == "__main__":
    which = sys.argv[2:] or ["scroll", "open"]
    if "scroll" in which:
        scroll_gif()
    if "open" in which:
        open_gif()
