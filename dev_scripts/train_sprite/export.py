"""
Export the approved Tosa Rail train art (option C) to the files the engine builds from:
    graphics/train/train.png   64x256, 4bpp indexed, four 64x64 pieces stacked (0 rear, 1 door shut,
                               2 loco, 3 door open); index 0 = transparent
    graphics/train/train.pal   JASC-PAL, 16 colours (all multiples of 8 -> exact in BGR555)
usage: python export.py [option]
"""
import os
import sys

import train_art as T

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DST = os.path.join(ROOT, "graphics", "train")


def main(k="C"):
    im = T.sheet(k)
    assert im.size == (64, 256) and max(im.getdata()) < 16
    pal = [T.snap(T.palette(k)[i]) for i in range(16)]
    im.putpalette([v for c in pal for v in c])
    im.save(os.path.join(DST, "train.png"), bits=4, optimize=False)
    with open(os.path.join(DST, "train.pal"), "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in pal:
            f.write("%d %d %d\n" % c)
    print("wrote", DST, "option", k)


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["C"]))
