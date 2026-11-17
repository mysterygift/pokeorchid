"""A small outdoor backdrop made of real gTileset_General / Petalburg metatiles (grass, sandy
path, trees, flowers), for mocking up building exteriors in an in-game setting."""
import random

from PIL import Image

import vanilla
from mock import Stage

GRASS, FLOWER = 0x001, 0x004
PATH = ((0x118, 0x119, 0x11A), (0x120, 0x121, 0x122), (0x128, 0x129, 0x12A))
TREE = ((0x1CE, 0x1CF), (0x1D6, 0x1D7), (0x1E6, 0x1E7))


class Town:
    def __init__(self, w, h, seed=3):
        self.w, self.h = w, h
        self.sc = vanilla.Scene("gTileset_General", "gTileset_Petalburg")
        self.g = [[GRASS] * w for _ in range(h)]
        self.rng = random.Random(seed)

    def path(self, x0, y0, x1, y1):
        """Sandy path rectangle (inclusive tile coords); overlapping rectangles merge."""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if not (0 <= x < self.w and 0 <= y < self.h):
                    continue
                r = 0 if y == y0 else 2 if y == y1 else 1
                c = 0 if x == x0 else 2 if x == x1 else 1
                if y in (0, self.h - 1):
                    r = 1
                if x in (0, self.w - 1):
                    c = 1
                cur = self.g[y][x]
                is_path = any(cur in row for row in PATH)
                self.g[y][x] = PATH[1][1] if is_path else PATH[r][c]

    def tree(self, x, y):
        """2x3 tree with its top-left at (x, y)."""
        for dy, row in enumerate(TREE):
            for dx, mid in enumerate(row):
                if 0 <= x + dx < self.w and 0 <= y + dy < self.h:
                    self.g[y + dy][x + dx] = mid

    def flowers(self, cells):
        for x, y in cells:
            if self.g[y][x] == GRASS:
                self.g[y][x] = FLOWER

    def stage(self):
        under = Image.new("RGBA", (self.w * 16, self.h * 16))
        over = Image.new("RGBA", under.size, (0, 0, 0, 0))
        for y in range(self.h):
            for x in range(self.w):
                u, o = self.sc.metatile(self.g[y][x])
                under.paste(u, (x * 16, y * 16))
                over.paste(o, (x * 16, y * 16))
        return Stage(under, over)


if __name__ == "__main__":
    from mock import save
    t = Town(20, 12)
    for x in (0, 2, 9, 16, 18):
        t.tree(x, 0)
    t.path(0, 8, 19, 9)
    t.path(5, 9, 6, 11)
    t.flowers([(4, 5), (12, 4), (13, 6)])
    st = t.stage()
    st.npc("brendan/walking.png", "brendan.pal", 1, 6, 8)
    print(save(st.render(), "town_test.png", 2))
