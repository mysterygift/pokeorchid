"""
Delta recolour proposals: normal vs Delta palette on the repo's own front pics (GBA-style
anim_front_gba.png + normal_gba.pal when present, as P_GBA_STYLE_SPECIES_GFX is TRUE).
Only palette entries change (same tiles, 15 colours), snapped to GBA 5-bit colour.

usage: palettes.py -> out/batch5_delta/palettes_2x.png + delta/palettes/<species>_delta.pal
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "out", "batch5_delta")

# species -> (Delta label, {palette index: new RGB}, note)
RECOLOURS = {
    "gyarados": ("Gyarados-δ  Electric/Steel", {
        4: (248, 232, 120), 5: (240, 200, 48), 6: (200, 152, 24), 7: (104, 72, 16),       # body: blue -> gold
        8: (224, 232, 240), 9: (176, 184, 200), 10: (96, 104, 120),                       # belly: cream -> steel
    }, "body gold, belly + fins steel; mouth kept"),
    "eevee": ("Eevee-δ  Steel", {
        11: (208, 216, 232), 12: (160, 168, 192), 13: (112, 120, 144), 14: (64, 72, 96),   # fur: brown -> steel
    }, "fur steel blue-grey, cream ruff kept"),
    "charizard": ("Charizard-δ  Electric/Steel", {
        10: (248, 240, 136), 11: (248, 216, 56), 12: (216, 168, 24), 13: (136, 96, 8),     # body orange -> yellow
        3: (176, 184, 208), 4: (128, 136, 160), 5: (64, 72, 96),                           # wing membrane teal -> steel
        1: (120, 200, 248), 2: (48, 120, 224),                                             # tail flame -> electric blue
    }, "body yellow, wings steel, tail flame blue"),
    "dragonite": ("Dragonite-δ  Electric", {
        2: (248, 248, 160), 3: (248, 232, 64), 4: (224, 192, 24), 5: (112, 88, 8),         # body -> electric yellow
        6: (120, 184, 248), 7: (72, 128, 232), 8: (40, 72, 160),                           # wings teal -> electric blue
        9: (248, 248, 248), 10: (208, 216, 224), 11: (144, 152, 168),                      # belly cream -> white/silver
    }, "lemon body, blue wings, white belly"),
    "gardevoir": ("Gardevoir-δ  Grass", {
        1: (232, 248, 208), 2: (192, 224, 168), 3: (152, 192, 128), 4: (112, 152, 96),     # gown white -> pale leaf
        11: (168, 232, 112), 12: (96, 184, 64), 13: (48, 136, 48), 14: (24, 80, 40),       # hair -> deeper leaf green
        7: (248, 176, 216), 8: (216, 80, 152), 5: (136, 64, 104),                          # chest horn red -> blossom pink
    }, "leaf gown, deep green hair, blossom-pink horn"),
    "klinklang": ("Klinklang-δ  Rock/Ice", {
        5: (224, 240, 248), 6: (168, 208, 232), 4: (96, 136, 176),                         # big gears grey -> ice
        13: (184, 160, 112), 10: (136, 112, 72),                                           # small gear -> rock brown
    }, "ice-blue gears, rocky small gear; core kept"),
}


def snap(c):
    return tuple((v & 0xF8) | (v >> 5) for v in c)


def load(sp):
    d = os.path.join(ROOT, "graphics", "pokemon", sp)
    fr = os.path.join(d, "anim_front_gba.png")
    pl = os.path.join(d, "normal_gba.pal")
    if not os.path.exists(fr):
        fr = os.path.join(d, "anim_front.png")
    if not os.path.exists(pl):
        pl = os.path.join(d, "normal.pal")
    im = Image.open(fr).crop((0, 0, 64, 64))
    pal = [tuple(map(int, l.split())) for l in open(pl).read().split("\n")[3:19]]
    return im, pal, os.path.relpath(fr, ROOT), os.path.relpath(pl, ROOT)


def paint(im, pal, k=2):
    out = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    px, op = im.load(), out.load()
    for y in range(64):
        for x in range(64):
            v = px[x, y]
            if v:
                op[x, y] = pal[v] + (255,)
    return out.resize((64 * k, 64 * k), Image.NEAREST)


def font(sz):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", sz)
    except OSError:
        return ImageFont.load_default()


def write_pal(path, pal):
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for c in pal:
            f.write("%d %d %d\n" % c)


def main():
    os.makedirs(OUT, exist_ok=True)
    pdir = os.path.join(HERE, "palettes")
    os.makedirs(pdir, exist_ok=True)
    k = 2
    cell_w = 64 * k * 2 + 30
    cols = 3
    rows = (len(RECOLOURS) + cols - 1) // cols
    cell_h = 64 * k + 70
    W, H = cols * cell_w + 20, rows * cell_h + 50
    sheet = Image.new("RGB", (W, H), (244, 242, 236))
    dr = ImageDraw.Draw(sheet)
    f, fs = font(14), font(11)
    dr.text((10, 8), "Delta recolours at 2x — left: normal palette, right: proposed Delta palette (same tiles, GBA 5-bit colours)",
            fill=(30, 30, 30), font=f)
    for i, (sp, (label, remap, note)) in enumerate(RECOLOURS.items()):
        im, pal, fr, pl = load(sp)
        new = list(pal)
        for idx, c in remap.items():
            new[idx] = snap(c)
        write_pal(os.path.join(pdir, sp + "_delta.pal"), new)
        x0 = 10 + (i % cols) * cell_w
        y0 = 34 + (i // cols) * cell_h
        dr.rectangle([x0, y0, x0 + cell_w - 12, y0 + cell_h - 10], fill=(214, 226, 214))
        sheet.paste(paint(im, pal, k), (x0 + 6, y0 + 4), paint(im, pal, k))
        sheet.paste(paint(im, new, k), (x0 + 6 + 64 * k + 10, y0 + 4), paint(im, new, k))
        dr.text((x0 + 6, y0 + 64 * k + 6), label, fill=(20, 20, 20), font=f)
        dr.text((x0 + 6, y0 + 64 * k + 24), note, fill=(70, 70, 70), font=fs)
        # swatches: old -> new for changed entries
        sx = x0 + 6
        for idx in sorted(remap):
            dr.rectangle([sx, y0 + 64 * k + 42, sx + 7, y0 + 64 * k + 49], fill=pal[idx])
            dr.rectangle([sx, y0 + 64 * k + 50, sx + 7, y0 + 64 * k + 57], fill=new[idx])
            sx += 9
        dr.text((sx + 6, y0 + 64 * k + 42), os.path.basename(fr) + " / " + os.path.basename(pl), fill=(110, 110, 110), font=fs)
    sheet.save(os.path.join(OUT, "palettes_2x.png"))


if __name__ == "__main__":
    main()
