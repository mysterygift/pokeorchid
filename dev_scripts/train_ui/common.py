"""
Shared helpers for the Tosa Rail mockups.

Imports the Orchid UI kit from the satchel worktree (override with ORCHID_UI_KIT) — the kit
files are NOT copied here. Game graphics (Brendan, NPCs, keypad glyphs) are read from THIS
worktree's graphics/ folder.

Needs Pillow:  python3 -m venv .venv && .venv/bin/pip install pillow
"""
import os
import sys

KIT = os.environ.get(
    "ORCHID_UI_KIT",
    "/Users/arandavies/Development/pokemon-orchid/pokeorchid-satchel/dev_scripts/orchid_ui")
if KIT not in sys.path:
    sys.path.insert(0, KIT)

from PIL import Image                     # noqa: E402
from kit import *                         # noqa: E402,F401  (palette roles + primitives)
import kit as K                           # noqa: E402
import kit_ext as KX                      # noqa: E402
import windows as Wn                      # noqa: E402
from gamefont import draw_text, text_width  # noqa: E402,F401

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
G = lambda *p: os.path.join(ROOT, "graphics", *p)
W, H = 240, 160
FPS = 60          # GBA frames per second (all timing constants below are GBA frames)


def ensure_out():
    os.makedirs(OUT, exist_ok=True)
    return OUT


def save_still(im, name):
    """Every still at 1x and 3x (nearest neighbour)."""
    ensure_out()
    im = im.convert("RGB")
    im.save(os.path.join(OUT, name + "_1x.png"))
    KX.upscale(im, 3).save(os.path.join(OUT, name + "_3x.png"))


def save_gif(frames, path, scale=3, step=2):
    """frames = one RGBA image per GBA frame; GIF keeps every `step`-th frame (60/step fps)."""
    fr = [f.convert("RGB").resize((f.size[0] * scale, f.size[1] * scale), Image.NEAREST)
          for f in frames[::step]]
    fr[0].save(path, save_all=True, append_images=fr[1:], duration=int(1000 * step / FPS),
               loop=0, optimize=False, disposal=1)
    return len(fr)


# ------------------------------------------------------------------ ROM palettes / sprites
def load_jasc(path):
    return KX.load_jasc(path)


def load_gbapal(path):
    import struct
    data = open(path, "rb").read()
    out = []
    for i in range(0, len(data), 2):
        v = struct.unpack("<H", data[i:i + 2])[0]
        out.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3))
    return out


def obj_frame(png, frame, fw=16, fh=32, pal=None, hflip=False):
    """One frame of a horizontal object-event strip (Gen 3 layout), index 0 transparent."""
    im = Image.open(png)
    im = im.crop((frame * fw, 0, frame * fw + fw, fh))
    out = KX.sheet_rgba(im, pal)
    return out.transpose(Image.FLIP_LEFT_RIGHT) if hflip else out


# Gen 3 object-event frame order for 9-frame people strips (walking.png, clerk.png ...).
F_DOWN, F_UP, F_LEFT = 0, 1, 2
F_WALK_DOWN = (3, 4)
F_WALK_UP = (5, 6)
F_WALK_LEFT = (7, 8)


def brendan(frame, hflip=False):
    return obj_frame(G("object_events", "pics", "people", "brendan", "walking.png"), frame,
                     pal=load_jasc(G("object_events", "palettes", "brendan.pal")), hflip=hflip)


def npc(name, frame, palname, hflip=False):
    return obj_frame(G("object_events", "pics", "people", name + ".png"), frame,
                     pal=load_jasc(G("object_events", "palettes", palname + ".pal")), hflip=hflip)


def player_map_icon():
    """16x16 region-map player head (graphics/pokenav/region_map/brendan_icon.png)."""
    d = G("pokenav", "region_map")
    pal = load_gbapal(os.path.join(d, "brendan_icon.gbapal"))[:16]
    return KX.sheet_rgba(Image.open(os.path.join(d, "brendan_icon.png")), pal)


# ------------------------------------------------------------------ button glyphs
def keypad_glyph(which="A"):
    """
    The ROM's own {A_BUTTON}/{B_BUTTON} glyph (graphics/fonts/keypad_icons.png, 8x12 cells),
    returned as an index mask: 1 = face, 2 = shadow/outline, 3 = letter.
    """
    im = Image.open(G("fonts", "keypad_icons.png"))
    x0 = {"A": 0, "B": 8}[which]
    px = im.load()
    return [[px[x0 + x, 4 + y] for x in range(8)] for y in range(8)]


def draw_button(cv, x, y, which, face=ACCENT, letter=WHITE, shadow=INK, aa=ACCENT_LIGHT):
    """
    Kit-coloured keypad glyph (8x8). In the ROM glyph index 2 is both the letter and the
    bottom drop shadow; the last row is the shadow, so it is split by position here.
    """
    m = keypad_glyph(which)
    for yy, row in enumerate(m):
        for xx, v in enumerate(row):
            if v == 1:
                cv.set(x + xx, y + yy, face)
            elif v == 2:
                cv.set(x + xx, y + yy, shadow if (yy in (0, 6, 7) or xx in (0, 6)) else letter)
            elif v == 3:
                cv.set(x + xx, y + yy, aa)
    return x + 8
