"""
Animated preview of the Orchid Trainer Card flip. Timeline in GBA frames (60 fps);
one GIF frame every 2 GBA frames (duration 33 ms), saved at 2x.

flip.gif — A flips front -> back, B flips back -> front, on the scrolling grid.
Timing and maths are vanilla trainer_card.c:
  * Task_AnimateCardFlipDown: cardTop += 7 / frame up to CARD_FLIP_Y (77) = 11 frames;
    per-scanline BG VOFS squashes the card toward the centre line, WIN0V clips it,
    BLDY darkens it ((cardTop + 40) / 10, 0 while <= 4).
  * Task_DrawFlippedCardSide: the card stays a 6-line sliver while the other side is
    printed (~10 frames, one print step per frame) + Task_SetCardFlipped (1 frame).
  * Task_AnimateCardFlipUp: cardTop -= 5 / frame back to 0 = 16 frames.
  * Grid (BG2) scrolls down-right 1px / 4 frames throughout; it is never squashed.
  * TIME colon blinks every 61 frames on the front (BlinkTimeColon).
Orchid change (see notes): the same VOFS is written to every card layer (art, text,
badges + pic), so the whole card folds; vanilla hides text/pic/badges while flipping.

usage: anim_card.py OUT_DIR
"""
import os
import sys
from PIL import Image
import mock_card as M
import card_ext as C
import kit_ext as KX

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

DOWN_STEP, UP_STEP, DRAW_FRAMES = 7, 5, 11


def flip_track(start):
    """[(frame, card_top, phase)] for one flip starting at GBA frame `start`."""
    out, f, top = [], start + 1, 0
    while top < C.CARD_FLIP_Y:
        top = min(C.CARD_FLIP_Y, top + DOWN_STEP)
        out.append((f, top, "down"))
        f += 1
    for _ in range(DRAW_FRAMES):
        out.append((f, top, "hold"))
        f += 1
    while top > 0:
        top = 0 if top <= UP_STEP else top - UP_STEP
        out.append((f, top, "up"))
        f += 1
    return out, f


def save_gif(frames, name):
    fr = [f.convert("RGB").resize((M.W * 2, M.H * 2), Image.NEAREST) for f in frames]
    fr[0].save(os.path.join(OUT, name), save_all=True, append_images=fr[1:], duration=33, loop=0,
               optimize=False)
    print(name, len(fr), "frames")


def flip_gif(d=M.HERO):
    layers = {("front", True): M.card_layers(d, "front", True),
              ("front", False): M.card_layers(d, "front", False),
              ("back", True): M.card_layers(d, "back")}
    a_press = 40
    t1, end1 = flip_track(a_press)
    b_press = end1 + 70
    t2, end2 = flip_track(b_press)
    end = end2 + 50
    track = {f: (top, ph) for f, top, ph in t1 + t2}
    # Task_SetCardFlipped swaps the side at the end of the hold; the flip-up shows the new side
    sw1 = next(f for f, _, ph in t1 if ph == "up")
    sw2 = next(f for f, _, ph in t2 if ph == "up")
    frames = []
    for f in range(0, end, 2):
        top, ph = track.get(f, (0, None))
        side = "back" if sw1 <= f < sw2 else "front"
        colon = (f // 61) % 2 == 0
        card = layers[(side, colon if side == "front" else True)]
        if top:
            card = C.darken(C.squash(card, top, ph != "up"), C.blend_y(top))
        out = KX.grid_frame(f // 4)
        out.alpha_composite(card)
        frames.append(out)
    save_gif(frames, "flip.gif")
    return frames


if __name__ == "__main__":
    fr = flip_gif()
