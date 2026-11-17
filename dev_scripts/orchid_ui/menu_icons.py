"""
Start menu icons — 12 x 16x16 frames stacked vertically, one shared 16-colour palette.

Gen 5 layout, Gen 3 pixels: each icon is drawn like a downsized R/S/E item icon
(slight top-down 3/4 view, ink outline, light from the top-left), with ramps taken
from graphics/items/icon_palettes/*.pal and snapped to BGR555.

usage: menu_icons.py   (writes graphics/start_menu/menu_icons.png, indexed, 16 colours)
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import kit  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "graphics", "start_menu", "menu_icons.png")

# ------------------------------------------------------------------ palette
# idx, char, colour, source
PAL = [
    (0, ".", (208, 232, 248), "transparent key (as sprites.icon_palette)"),
    (1, "k", kit.palette()[kit.INK], "INK outline"),
    (2, "w", kit.palette()[kit.WHITE], "white / glints"),
    (3, "l", (216, 216, 232), "grey light (poke_ball.pal 222,205,246 lavender-white, cooled)"),
    (4, "m", (160, 160, 184), "grey mid (poke_ball.pal 164,164,197)"),
    (5, "d", (96, 96, 120), "grey dark / ball band (poke_ball.pal 74,82,82 / 123,123,131)"),
    (6, "R", (176, 72, 56), "red dark (poke_ball.pal 180,82,57)"),
    (7, "r", (224, 88, 56), "red (poke_ball.pal 222,90,57)"),
    (8, "o", (248, 144, 56), "red light / orange (poke_ball.pal 255,148,57)"),
    (9, "B", (48, 80, 152), "blue dark (vs_seeker.pal 49,82,148)"),
    (10, "b", (64, 128, 224), "blue (vs_seeker.pal 65,131,230)"),
    (11, "c", (120, 200, 248), "blue light (vs_seeker.pal 115,205,255)"),
    (12, "n", (152, 96, 56), "brown (satchel dark leather 152,96,56; berry_pouch 139,106,57)"),
    (13, "t", (200, 136, 80), "tan leather (satchel 200,136,80)"),
    (14, "y", (248, 208, 72), "gold / yellow (poke_ball.pal 255,213,57; tm_case 246,230,41)"),
    (15, "g", (112, 176, 64), "green (devon_scope.pal 115,172,65)"),
]
PALETTE = [kit.snap(c) for _, _, c, _ in PAL]
CMAP = {ch: i for i, ch, _, _ in PAL}

NAMES = ["POKéDEX", "POKéMON", "BAG", "POKéNAV", "PLAYER", "SAVE",
         "OPTION", "EXIT", "RETIRE", "REST", "DEXNAV", "DEBUG"]

ICONS = {}

ICONS["POKéDEX"] = [
    "................",
    "..kkkkkkkkkkkk..",
    ".kookkkoooooook.",
    ".krkwcckryrgrRk.",
    ".krkccbkrrrrrRk.",
    ".krkcbBkrrrrrRk.",
    ".krrkkkrrrrrrRk.",
    ".kRRRRRRRRRRRRk.",
    ".kkkkkkkkkkkkkk.",
    ".kokkkkkkooooRk.",
    ".krkwgggkrrkrRk.",
    ".krkggggkrkkkRk.",
    ".krkkkkkkrrkrRk.",
    ".kRRRRRRRRRRRRk.",
    "..kkkkkkkkkkkk..",
    "................",
]

ICONS["POKéMON"] = [
    "................",
    ".....kkkkkk.....",
    "...kkoooorrkk...",
    "..koyyooorrrrk..",
    "..kywwooorrrrk..",
    ".koywwooorrrrRk.",
    ".kooooorrrrrrRk.",
    ".kRoooorrrrrrRk.",
    ".kdRRddRrrrRRdk.",
    ".kdddwldddddddk.",
    ".kwldlmdllllmmk.",
    "..kwlddllllmmk..",
    "..kllllllmmmmk..",
    "...kklmmmmmkk...",
    ".....kkkkkk.....",
    "................",
]

ICONS["BAG"] = [
    "................",
    ".....kkkkkk.....",
    "....k......k....",
    "....k......k....",
    "...kkkkkkkkkk...",
    "..kttttttttttk..",
    ".ktnnnnnnnnnnnk.",
    ".knnnnkkkknnnnk.",
    ".kkkkkkyykkkkkk.",
    ".knnnnkyyknnnnk.",
    ".kytttkkkktttnk.",
    ".kyttttttttttnk.",
    ".kttttttttttnnk.",
    ".knnnnnnnnnnnnk.",
    "..kkkkkkkkkkkk..",
    "................",
]

ICONS["POKéNAV"] = [
    "................",
    "...kkkkkkkkkk...",
    "..kwwwwwwwwwlk..",
    "..kwkkkkkkkkmk..",
    "..kwkwcgggkkmk..",
    "..kwkcgggbbkmk..",
    "..kwkggrgbbkmk..",
    "..kwkgggbbbkmk..",
    "..kwkkkkkkkkmk..",
    "..klllllllllmk..",
    "..kllllkklllmk..",
    "..klllkorkllmk..",
    "..klllkrRkllmk..",
    "..kmmmmkkmmmmk..",
    "...kkkkkkkkkk...",
    "................",
]

ICONS["PLAYER"] = [
    "................",
    "................",
    "................",
    "..kkkkkkkkkkkk..",
    ".kcccccccccccbk.",
    ".kbbbbbbbbbbbBk.",
    ".kwwwwwwwwwwwlk.",
    ".kwkkkkkwwwwwlk.",
    ".kwkrrrkwmmmmlk.",
    ".kwkctckwwwwwlk.",
    ".kwkbbbkwmmmwlk.",
    ".kwkkkkkwywywlk.",
    ".kllllllllllllk.",
    "..kkkkkkkkkkkk..",
    "................",
    "................",
]

ICONS["SAVE"] = [
    "................",
    "..kkkkkkkkkkkk..",
    "..kBccccccccbk..",
    "..kBbbbbbbbbBk..",
    "..kBbbwwwwwbBk..",
    "..kBbbwmmmlbBk..",
    "..kBbbllllbbBk..",
    "..kBbbbbbbbbBk..",
    "..kBbbbbbbbbBk..",
    "..kBbbbbbbbbBk..",
    "..kBBBBBBBBBBk..",
    "..kkkkkkkkkkkk..",
    "..kBwwwwwwrwlk..",
    "..kBllllllrllk..",
    "..kkkkkkkkrkkk..",
    "................",
]

ICONS["EXIT"] = [
    "................",
    ".kkkkkkkkk......",
    ".kyyyyyynk......",
    ".kytnnntnk......",
    ".kytnnntnk.k....",
    ".kytnnntnk.kk...",
    ".kytnnnkkkkkok..",
    ".kyttttkooooook.",
    ".kyttttkrrrrrRk.",
    ".kytnnnkkkkkRk..",
    ".kytnnntnk.kk...",
    ".kytnnntnk.k....",
    ".kytnnntnk......",
    ".kytttttnk......",
    ".kkkkkkkkk......",
    "................",
]

ICONS["RETIRE"] = [
    "................",
    "..kkk...........",
    "..kyk...........",
    "..knkkkkk..kkk..",
    "..knkwwwwkkwwwk.",
    "..knkwwwlwwwlmk.",
    "..knkwwwlwwwlmk.",
    "..knklwwlwwwlmk.",
    "..knkllllwwlmmk.",
    "..knkkkkklmkkk..",
    "..knk....kk.....",
    "..knk...........",
    "..knk...........",
    "..knk...........",
    "..kkk...........",
    "................",
]

ICONS["REST"] = [
    "................",
    ".........kkkk...",
    "............k...",
    "...........k....",
    "..........k.....",
    ".kkk.....kkkk...",
    ".kyk............",
    ".ktkkkkk........",
    ".ktkwwwlkkkkkkk.",
    ".ktkwllmkccccbk.",
    ".ktkkkkkkbbbbBk.",
    ".ktkwwwwkbbbBBk.",
    ".knnnnnnnnnnnnk.",
    ".kkkkkkkkkkkkkk.",
    ".kk..........kk.",
    "................",
]

ICONS["DEBUG"] = [
    "................",
    "....k......k....",
    ".....k....k.....",
    "......kkkk......",
    ".....kwddwk.....",
    "....kkkkkkkk....",
    "...kwggkkwggk...",
    ".kkwgggkkgggBkk.",
    "..kggggkkggggk..",
    ".kkggggkkgggBkk.",
    "..kggggkkgggBk..",
    ".kkgggBkkggBBkk.",
    "...kgBBkkgBBk...",
    "....kkkkkkkk....",
    "................",
    "................",
]


def icon_dexnav():
    """Round radar: metal bezel, dark screen with range ring, sweep and a blip."""
    import math
    g = [["."] * 16 for _ in range(16)]
    cx = cy = 8.0
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            r = math.hypot(dx, dy)
            lit = -(dx + dy)
            if r > 7.0:
                continue
            if r > 6.2:
                c = "k"
            elif r > 4.9:
                c = "w" if lit > 3 else ("m" if lit < -3 else "l")
            elif r > 4.1:
                c = "k"
            else:
                c = "B"
                if 2.0 < r <= 2.9:
                    c = "b"
            g[y][x] = c
    # sweep arm from the centre to the upper right, with a fading trail
    for (x, y), c in {(8, 7): "c", (9, 6): "c", (10, 5): "c", (8, 6): "b", (9, 5): "b",
                      (7, 7): "w"}.items():
        g[y][x] = c
    g[9][5] = "g"                     # blip
    return ["".join(r) for r in g]


ICONS["OPTION"] = [
    "................",
    ".......kk.......",
    "...kk.kwlk.kk...",
    "..kwwkkwlkklmk..",
    "..kwwwwlllllmk..",
    "...kwwlmmlllk...",
    "..kkwlmkkllmkk..",
    ".kwwlmk..kwmmmk.",
    ".kwllmk..kwmmdk.",
    "..kklllkkwmmkk..",
    "...klllwwmmdk...",
    "..klllmmmmdddk..",
    "..klmkkmdkkddk..",
    "...kk.kmdk.kk...",
    ".......kk.......",
    "................",
]
ICONS["DEXNAV"] = icon_dexnav()


def build():
    for n in NAMES:
        rows = ICONS[n]
        assert len(rows) == 16, (n, len(rows))
        for i, r in enumerate(rows):
            assert len(r) == 16, (n, i, len(r), r)
            for ch in r:
                assert ch in CMAP, (n, i, ch)
    im = Image.new("P", (16, 16 * len(NAMES)), 0)
    flat = []
    for c in PALETTE:
        flat += list(c)
    im.putpalette(flat)
    cv = kit.Canvas(im)
    for f, n in enumerate(NAMES):
        kit.stamp(cv, 0, f * 16, ICONS[n], {k: v for k, v in CMAP.items() if k != "."})
    return im


def main():
    im = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    im.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
