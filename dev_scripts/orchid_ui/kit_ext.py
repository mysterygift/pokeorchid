"""
Orchid UI kit — PROPOSED additions for the battle / party / Pokédex mockups.

Kept separate from kit.py while the bag is being implemented; fold into kit.py
(or keep as its own module) once the user approves the next screens.

Compositing model used by every mockup: build a 240x160 RGBA frame bottom-up,
the same way the GBA does — BG3 grid (or battle scene) → BG art layers → text
→ OBJ sprites. Each art layer is drawn with kit role indices on a 'P' sheet and
composited with its own palette (index 0 = transparent).
"""
import os
from PIL import Image
from kit import *
from backdrop import GRID_PAL, grid_index

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
G = lambda *p: os.path.join(ROOT, "graphics", *p)
W, H = 240, 160

# ------------------------------------------------------------------ Gen 3 reference colours
# From graphics/battle_interface/hpbar.png (Gen 3's own HP ramps: light, dark).
HP_GREEN = ((112, 248, 168), (88, 208, 128))
HP_YELLOW = ((248, 224, 56), (200, 168, 8))
HP_RED = ((248, 88, 56), (168, 64, 72))
# From healthbox_singles_player.png (EXP fill).
EXP_BLUE = ((64, 200, 248), (40, 128, 208))
# Gender glyph colours (Gen 3 summary/party use these blues/reds).
MALE_BLUE = (64, 128, 248)
FEMALE_RED = (248, 88, 88)


def hp_ramp(frac):
    """Gen 3 thresholds: > 1/2 green, > 1/5 yellow, else red."""
    if frac > 0.5:
        return HP_GREEN
    if frac > 0.2:
        return HP_YELLOW
    return HP_RED


# ------------------------------------------------------------------ layers
def blank():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def grid_frame(scroll=0, w=W, h=H):
    """BG3 scrolling grid (diagonal down-right), as an opaque RGBA frame."""
    out = Image.new("RGBA", (w, h))
    px = out.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = GRID_PAL[grid_index(x - scroll, y - scroll)] + (255,)
    return out


def sheet_rgba(im, pal=None):
    """'P' sheet -> RGBA with index 0 transparent. pal = list of 16 RGB (default: sheet palette)."""
    if pal is not None:
        im = im.copy()
        flat = [c for rgb in pal for c in rgb]
        im.putpalette(flat + [0] * (768 - len(flat)))
    rgba = im.convert("RGBA")
    rp, ip = rgba.load(), im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if ip[x, y] == 0:
                rp[x, y] = (0, 0, 0, 0)
    return rgba


def layer(out, fn, theme="orchid", pal=None, size=None, at=(0, 0), **palkw):
    """Draw fn(Canvas) on a fresh P sheet (kit roles) and composite over `out`."""
    w, h = size or out.size
    im = new_sheet(w, h, theme, **palkw)
    fn(Canvas(im))
    out.alpha_composite(sheet_rgba(im, pal), at)
    return im


def upscale(im, k=3):
    return im.resize((im.size[0] * k, im.size[1] * k), Image.NEAREST)


# ------------------------------------------------------------------ ROM sprite loaders
def load_jasc(path):
    v = open(path).read().split()
    n = int(v[2])
    nums = list(map(int, v[3:3 + n * 3]))
    return [tuple(nums[i:i + 3]) for i in range(0, len(nums), 3)]


def sprite_rgba(png, frame=0, fh=None, pal=None, hflip=False):
    im = Image.open(png)
    fh = fh or im.size[1]
    im = im.crop((0, frame * fh, im.size[0], frame * fh + fh))
    out = sheet_rgba(im, pal)
    return out.transpose(Image.FLIP_LEFT_RIGHT) if hflip else out


def place(out, spr, cx, cy):
    out.alpha_composite(spr, (int(cx - spr.size[0] // 2), int(cy - spr.size[1] // 2)))


def mon_front(species, frame=0, shiny=False):
    """64x64 GBA-style front pic (P_GBA_STYLE_SPECIES_GFX is on)."""
    d = G("pokemon", species)
    png = next((os.path.join(d, f) for f in ("anim_front_gba.png", "anim_front.png", "front.png")
                if os.path.exists(os.path.join(d, f))))
    pal = os.path.join(d, ("shiny" if shiny else "normal") + "_gba.pal")
    if not os.path.exists(pal):   # Gen 4+ species ship only the modern palette
        pal = os.path.join(d, ("shiny" if shiny else "normal") + ".pal")
    return sprite_rgba(png, frame, 64, load_jasc(pal) if os.path.exists(pal) else None)


def mon_back(species):
    d = G("pokemon", species)
    png = os.path.join(d, "back_gba.png")
    if not os.path.exists(png):
        png = os.path.join(d, "back.png")
    pal = os.path.join(d, "normal_gba.pal")
    return sprite_rgba(png, 0, 64, load_jasc(pal) if os.path.exists(pal) else None)


def mon_icon(species, frame=0, pal_index=None):
    """32x32 party icon. P_GBA_STYLE_SPECIES_ICONS is FALSE in Orchid -> modern icon.png;
    pal_index = the species' non-GBA .iconPalIndex (0-5)."""
    d = G("pokemon", species)
    png = os.path.join(d, "icon.png")
    pal = None
    if pal_index is not None:
        pal = load_jasc(G("pokemon", "icon_palettes", "pal%d.pal" % pal_index))
    return sprite_rgba(png, frame, 32, pal)


def type_icon(t):
    """Gen 3 32x16 move-type icon, e.g. 'fire', 'water' (embedded palette)."""
    return sprite_rgba(G("types", t + ".png"))


def item_icon(name):
    png, pal = G("items", "icons", name + ".png"), G("items", "icon_palettes", name + ".pal")
    return sprite_rgba(png, pal=load_jasc(pal) if os.path.exists(pal) else None)


# ------------------------------------------------------------------ bar primitive
def bar(cv, x, y, w, frac, light, dark, trough=PANEL_DARK, outline=INK, h=3):
    """
    Gen 3 style stat bar on a P canvas: ink outline, recessed trough, fill with a
    light top row and darker body. Indices are palette roles of the sheet.
    Outer size = (w+2) x (h+2) px. Fill width is rounded to whole pixels like the ROM.
    """
    cv.rect(x, y, x + w + 1, y + h + 1, outline)
    cv.rect(x + 1, y + 1, x + w, y + h, trough)
    n = max(0, min(w, int(round(w * frac))))
    if frac > 0 and n == 0:
        n = 1
    if n:
        cv.rect(x + 1, y + 1, x + n, y + h, dark)
        cv.hline(x + 1, x + n, y + 1, light)
