"""
Animated previews of the Orchid party menu (GBA frames at 60 fps, one GIF frame per 2 GBA frames).

party_select.gif  cursor walks the slots (gold slot + bouncing icon), grid scrolls, A opens the popup.
party_swap.gif    SWITCH: Gen 3 slide — both slot windows move 1 tile (8px) per frame off-screen
                  (lead to the left, right-column slot to the right; Task_SlideSelectedSlotsOffscreen
                  stops when both tilemap x > 33 -> 22 frames), mons swap, and both slide back (22 frames).
usage: anim_party.py OUT_DIR
"""
import os
import sys
from PIL import Image
import mock_party as M
import party_ext as P

SCALE = 2


def save_gif(frames, path):
    fr = [f.convert("RGB").resize((240 * SCALE, 160 * SCALE), Image.NEAREST) for f in frames]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=33, loop=0, optimize=False)
    print(path, len(fr), "frames")


def select_gif(path, theme="male"):
    # (start frame, cursor) — D-pad presses; 6 = CANCEL
    moves = [(0, 0), (44, 1), (70, 2), (96, 3), (122, 4), (148, M.CANCEL), (196, 4), (222, 0)]
    a_press, end = 276, 372
    choose = M.message("Choose a POKéMON.")
    pop = [M.message("Do what with this Grovyle?", P.DOWHAT_WIN),
           M.action_menu(["CUT", "SUMMARY", "SWITCH", "ITEM", "CANCEL"], 1)]
    frames = []
    for f in range(0, end, 2):
        cur, since = 0, 0
        for s, c in moves:
            if f >= s:
                cur, since = c, s
        popups = pop if f >= a_press else [choose]
        frames.append(M.render(theme, M.PARTY5, cursor=cur, popups=popups, grid_scroll=f // 4,
                               t=f, sel_t=f - since))
    save_gif(frames, path)


def swap_gif(path, theme="female"):
    party = list(M.PARTY5)
    swapped = list(party)
    swapped[0], swapped[2] = party[2], party[0]
    acts = ["CUT", "SUMMARY", "SWITCH", "ITEM", "CANCEL"]
    pop = [M.message("Do what with this Grovyle?", P.DOWHAT_WIN), M.action_menu(acts, 2)]
    move = [M.message("Move to where?")]
    choose = [M.message("Choose a POKéMON.")]
    A_SWITCH, D1, D2, A_TARGET = 30, 64, 92, 130
    OUT_N = 22                                   # frames to clear the screen (12 + 22 > 33 tiles)
    BACK = A_TARGET + OUT_N
    DONE = BACK + OUT_N
    end = DONE + 70
    frames = []
    for f in range(0, end, 2):
        kw = dict(grid_scroll=f // 4, t=f)
        if f < A_SWITCH:
            im = M.render(theme, party, cursor=0, popups=pop, **kw)
        elif f < D1:
            im = M.render(theme, party, cursor=0, moving=0, popups=move, sel_t=f - A_SWITCH, **kw)
        elif f < D2:
            im = M.render(theme, party, cursor=1, moving=0, popups=move, sel_t=f - D1, **kw)
        elif f < A_TARGET:
            im = M.render(theme, party, cursor=2, moving=0, popups=move, sel_t=f - D2, **kw)
        elif f < BACK:
            k = f - A_TARGET + 1                    # tiles moved so far
            im = M.render(theme, party, cursor=2, moving=0, popups=move,
                          slide={0: -8 * k, 2: 8 * k}, **kw)
        elif f < DONE:
            k = DONE - f                             # tiles still to travel back
            im = M.render(theme, swapped, cursor=2, moving=0, popups=move,
                          slide={0: -8 * k, 2: 8 * k}, **kw)
        else:
            im = M.render(theme, swapped, cursor=2, popups=choose, sel_t=f - DONE, **kw)
        frames.append(im)
    save_gif(frames, path)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    select_gif(os.path.join(out, "party_select.gif"))
    swap_gif(os.path.join(out, "party_swap.gif"))
