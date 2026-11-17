"""
Animated preview of the Orchid summary screen. Timeline in GBA frames (60 fps); one GIF
frame every 2 GBA frames (duration 33 ms), saved at 2x.

page_switch.gif — D-pad → twice (INFO → SKILLS → MOVES), then ← twice back to
INFO:
  * on the press the gold tab moves at once (tab cells swap palette 0 <-> 1) and the
    page's text windows + page OBJs (type icons) are cleared;
  * BG2 page art slides 148px over 12 frames, ease-out: the old page leaves to the left
    (→) / right (←), the new one follows it in; WIN0 clips BG2 to x >= 90 so the left
    column never moves;
  * new text + OBJs appear on the frame the slide lands (like vanilla printing after the
    BG scroll);
  * the Pokémon, its sockets, name / No. / item rows and the header never move; BG3 grid
    scrolls 1px / 4 frames throughout.

usage: anim_summary.py OUT_DIR
"""
import os
import sys
from PIL import Image
import mock_summary as M
import summary_ext as S

SLIDE, DIST = 12, 148


def ease(u):
    return 1 - (1 - u) ** 2


def save_gif(frames, path):
    fr = [f.convert("RGB").resize((M.W * 2, M.H * 2), Image.NEAREST) for f in frames]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=33, loop=0, optimize=False)
    print(os.path.basename(path), len(fr), "frames")


def page_switch(out_dir):
    mon = S.hero()
    seq = [0, 1, 2, 1, 0]
    holds = [40, 56, 56, 28, 50]
    events, f = [], 0
    for k, p in enumerate(seq):
        events.append((f, p))
        f += holds[k] + (SLIDE if k else 0)
    end = f
    pages = {}

    def page(p):
        if p not in pages:
            pages[p] = M.build_page(p, mon, "male")
        return pages[p]

    frames = []
    for t in range(0, end, 2):
        cur, prev, t0 = 0, None, 0
        for (ef, p) in events:
            if t >= ef:
                prev, cur, t0 = (cur if ef else None), p, ef
        dt = t - t0
        g = t // 4
        if prev is not None and dt < SLIDE:
            e = ease((dt + 1) / SLIDE)
            d = 1 if cur > prev else -1
            new_dx = int(round(d * DIST * (1 - e)))
            old_dx = int(round(-d * DIST * e))
            im = M.render(cur, mon, "male", grid_scroll=g, page_dx=new_dx, show_text=False,
                          other=page(prev), other_dx=old_dx)
        else:
            im = M.render(cur, mon, "male", grid_scroll=g)
        frames.append(im)
    save_gif(frames, os.path.join(out_dir, "page_switch.gif"))


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    page_switch(out)
