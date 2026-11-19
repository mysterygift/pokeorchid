"""
Placeholder region maps for Holon, Newmoon Island and Fullmoon Island (REGION_MAP_HOLON / _NEWMOON /
_FULLMOON). MOCK + ROM preview only.

Deliberately plain and obviously temporary: the vanilla region map's own sea tile (striped), a flat island
silhouette per place in the vanilla map greens with a dark coast line, and a small baked "PLACEHOLDER" tag
bottom-right. The three maps share ONE 8bpp tile sheet + ONE palette (the vanilla 48-colour map.pal), so
they cost one sheet in ROM and three 4 KB tilemaps.

Cells (28x15 grid, same as every region map):
  Holon:    Holon Village (town disc), Mirage Forest (coast + dock, SW), Research Tower (N of the village),
            Holon Lake (S) - landmark diamonds; one big irregular island
  Newmoon:  Newmoon Island - one crescent island (Platinum's shape, dark forest)
  Fullmoon: Fullmoon Island - one round island
usage: <venv python> dev_scripts/voyages/regionmap/placeholders.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rm_common as C  # noqa: E402
from PIL import Image  # noqa: E402

LAND, LAND_HI, COAST, SAND = 124, 123, 126, 127          # vanilla map.pal indices (greens / sand)
TAG_INK = 132

MAPS = {
    "holon": dict(
        title="HOLON",
        # island = union of ellipses (cx, cy, rx, ry) in px
        blobs=[(120, 76, 56, 34), (84, 92, 30, 22), (150, 98, 30, 22), (124, 112, 26, 16), (100, 56, 22, 14)],
        places=[("Holon Village", (14, 6), False), ("Mirage Forest", (9, 9), True),
                ("Research Tower", (14, 4), True), ("Holon Lake", (15, 10), True)],
        cursor=0, here=1),
    "newmoon": dict(
        title="NEWMOON ISLAND",
        blobs=[(120, 80, 30, 30)], cut=[(134, 72, 24, 26)],          # crescent = disc minus disc
        places=[("Newmoon Island", (12, 7), True)], cursor=0, here=0),
    "fullmoon": dict(
        title="FULLMOON ISLAND",
        blobs=[(120, 78, 28, 26)],
        places=[("Fullmoon Island", (13, 7), True)], cursor=0, here=0),
}


def inside(blobs, x, y):
    return any(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0 for cx, cy, rx, ry in blobs)


def render(spec, sea):
    im = Image.new("P", (C.W, C.H))
    im.putpalette(sea["pal"])
    p = im.load()
    cut = spec.get("cut", [])
    land = set()
    for y in range(C.H):
        for x in range(C.W):
            p[x, y] = sea["px"][(y % 8) * 8 + x % 8]
            if inside(spec["blobs"], x, y) and not inside(cut, x, y):
                land.add((x, y))
    # quantise the coast to 2 px steps so it reads as map art, not a vector shape
    land = {(x, y) for (x, y) in land if ((x // 2) * 2, (y // 2) * 2) in land}
    for (x, y) in land:
        edge = any((x + dx, y + dy) not in land for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        p[x, y] = COAST if edge else (LAND_HI if (x + y) % 7 == 0 else LAND)
    # baked tag (8 px tall, bottom-right of the visible map)
    def fn(cv):
        C.draw_text(cv, C.W - 6 - C.text_width("PLACEHOLDER", "narrow"), 120, "PLACEHOLDER", 3, None, font="narrow")
    tag = Image.new("P", (C.W, C.H), 0)
    tag.putpalette([0, 0, 0] * 3 + [255, 255, 255] + [0, 0, 0] * 252)
    fn(C.Canvas(tag))
    tp = tag.load()
    for y in range(C.H):
        for x in range(C.W):
            if tp[x, y]:
                p[x, y] = TAG_INK
    return im


def main():
    sheet, tmap, _ = C.vanilla_hoenn()
    vanilla = C.bg2_from(sheet, tmap)
    # a pure sea tile from the vanilla art
    sea_px = None
    for ty in range(19, -1, -1):
        for tx in range(29, -1, -1):
            t = vanilla.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)).tobytes()
            if set(t) == {113, 114}:
                sea_px = t
                break
        if sea_px:
            break
    sea = {"px": sea_px, "pal": vanilla.getpalette()}
    tiles, index = [], {}
    shots = []
    for key, spec in MAPS.items():
        im = render(spec, sea)
        for ty in range(20):
            for tx in range(30):
                k = im.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)).tobytes()
                if k not in index:
                    index[k] = len(tiles)
                    tiles.append(k)
        C.save(im, "%s_bg2" % key)
        nodes = [(cell, lm, True) for _, cell, lm in spec["places"]]
        cur = spec["places"][spec["cursor"]]
        scr = C.screen(im, spec["title"], cur[0], nodes, cursor=cur[1], here=spec["places"][spec["here"]][1])
        C.save(scr, "%s_screen" % key)
        shots.append(scr.convert("RGB"))
    strip = Image.new("RGB", (C.W * 3 + 16, C.H), (40, 40, 48))
    for i, im in enumerate(shots):
        strip.paste(im, (i * (C.W + 8), 0))
    C.save(strip, "placeholders_screens")
    cols = sorted(set(b for t in tiles for b in t))
    msg = ("placeholders: one shared sheet, %d unique tiles / 256 for all three maps, %d colours of the vanilla "
           "48-colour map.pal (%s)" % (len(tiles), len(cols), ",".join(map(str, cols))))
    open(os.path.join(C.OUT, "placeholders_budget.txt"), "w").write(msg + "\n")
    print(msg)


if __name__ == "__main__":
    main()
