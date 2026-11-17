"""
Animated Poké Mart buy flow (direction A). GBA frames at 60 fps, one GIF frame per 2 GBA frames.

  0- 19  browsing, cursor on Poké Ball
 20- 80  six Down presses, 12 frames apart (cursor walks the gold pill; the 6th scrolls the list
         one row and the thumb steps down); the item on the counter + description follow each move
 100     A on Super Potion: the clerk's line prints at 1 char/frame (fast text)
 +10     the quantity tag drops in (×001)
 +20..   three Up presses 12 frames apart: ×002, ×003, ×004; total and money-left update each press
 +70     A: confirm line prints, then YES/NO (gold pill on YES)
 +24     A on YES: money sign drops to ¥200, "Here you go! Thank you very much." prints, hold,
         then back to the list.
usage: anim_mart.py OUT.gif
"""
import sys
from PIL import Image
from mock_mart import render, message_for, st_defaults, money_str

THANKS = "Here you go!\nThank you very much."


def timeline():
    ev = []                                     # (start frame, state kwargs)
    f = 0
    ev.append((0, dict(cursor=0)))
    for k in range(1, 7):
        ev.append((8 + 12 * k, dict(cursor=k, scroll=max(0, k - 5))))
    base = dict(cursor=6, scroll=1)
    f = 100
    ask = message_for(st_defaults(mode="qty", **base))
    for c in range(0, len(ask) + 1):
        ev.append((f + c, dict(base, mode="qty", picker=False, chars=c)))
    f += len(ask) + 10
    for q in range(1, 5):
        ev.append((f + (q - 1) * 12 + (0 if q == 1 else 8), dict(base, mode="qty", qty=q)))
    f += 70
    conf = message_for(st_defaults(mode="confirm", qty=4, **base))
    for c in range(0, len(conf) + 1):
        ev.append((f + c, dict(base, mode="confirm", qty=4, chars=c)))
    f += len(conf) + 24
    for c in range(0, len(THANKS) + 1):
        ev.append((f + c, dict(base, mode="msg", msg=THANKS, chars=c, money=200)))
    f += len(THANKS) + 70
    ev.append((f, dict(base, money=200)))
    return ev, f + 40


def main():
    out = sys.argv[1]
    ev, end = timeline()
    frames = []
    for g in range(0, end, 2):
        kw = {}
        for (s0, k) in ev:
            if s0 <= g:
                kw = k
        im = render("A", grid=g // 4, **kw)
        frames.append(im.convert("RGB").resize((480, 320), Image.NEAREST))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=33, loop=0, optimize=False)
    print("gif frames:", len(frames), "GBA frames:", end)


main()
