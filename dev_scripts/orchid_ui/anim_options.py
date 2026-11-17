"""
Animated Options preview. Timeline in GBA frames (60 fps), one GIF frame per 2 GBA frames.

  0    TEXT SPEED focused, MID: the tray sample prints at 4 frames / character
  80   press RIGHT: right chevron lights + pushes out for 8 frames, MID -> FAST,
       the sample clears and reprints at 1 frame / character; red continue arrow bobs when done
  190  DOWN x5 (every 25 frames): gold pill steps through BATTLE SCENE .. FRAME, tray swaps preview
  320  FRAME: RIGHT x4 (every 25 frames) -> TYPE 2..5, the preview reloads frame tiles + palette each press
  430  DOWN -> DONE button turns gold
Grid scrolls down-right 1px / 4 frames throughout.
usage: anim_options.py OUT.gif
"""
import sys
from PIL import Image
import mock_options as M

PRESS_LEN = 8
EVENTS = [(80, "R", 0), (320, "R", 5), (345, "R", 5), (370, "R", 5), (395, "R", 5)]
MOVES = [190, 215, 240, 265, 290, 430]
END = 480


def state_at(f):
    focus = sum(1 for m in MOVES if f >= m)
    values = list(M.DEFAULTS)
    flash, print_start = None, 0
    for (t, d, row) in EVENTS:
        if f >= t:
            if row == 0:
                values[0] = 2
                print_start = t
            else:
                n = values[5] + (1 if d == "R" else -1)
                values[5] = (n - 1) % M.FRAME_COUNT + 1
            if f < t + PRESS_LEN:
                flash = d
    delay = M.TEXT_DELAY[values[0]]
    chars = (f - print_start) // delay
    done = chars >= len(M.SAMPLE)
    bob = ((f // 16) % 2) if done else 0
    return focus, values, flash, (None if done else chars), bob


def main(path):
    frames = []
    for f in range(0, END, 2):
        focus, values, flash, chars, bob = state_at(f)
        im = M.render(focus, values, flash, chars, grid_scroll=f // 4, arrow_bob=bob)
        frames.append(M.K.upscale(im.convert("RGB"), 2))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=33, loop=0, optimize=False)
    print("frames:", len(frames))


if __name__ == "__main__":
    main(sys.argv[1])
