"""
δ (Delta Species) glyph for every Latin ROM font — design-review only.

Builds the glyph from each font's own 'o' (bowl) plus an S-hook rising to the
'd' ascender line, then recomputes the drop shadow (right / down / diagonal,
the rule the vanilla glyphs use). Writes PATCHED COPIES of the fonts into
dev_scripts/voyages/delta/fonts/ (never touches graphics/fonts/).

usage: glyph.py [OUT_DIR]   (default ../out/batch5_delta)
  -> glyph_closeup.png  (δ next to o d 6 a e in all 9 fonts, 4x)
  -> fonts/*.png + fonts/widths.json (patched copies, δ at DELTA_CODE)
"""
import json
import os
import re
import sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "out", "batch5_delta")

DELTA_CODE = 0x18          # recommended free byte (see NOTES.md §5)

FONTS = {   # file -> (width table symbol, nominal ascender top row)
    "latin_normal":         "gFontNormalLatinGlyphWidths",
    "latin_short":          "gFontShortLatinGlyphWidths",
    "latin_narrow":         "gFontNarrowLatinGlyphWidths",
    "latin_narrower":       "gFontNarrowerLatinGlyphWidths",
    "latin_small":          "gFontSmallLatinGlyphWidths",
    "latin_small_narrow":   "gFontSmallNarrowLatinGlyphWidths",
    "latin_small_narrower": "gFontSmallNarrowerLatinGlyphWidths",
    "latin_short_narrow":   "gFontShortNarrowLatinGlyphWidths",
    "latin_short_narrower": "gFontShortNarrowerLatinGlyphWidths",
}
FONT_ID = {"latin_normal": "FONT_NORMAL", "latin_short": "FONT_SHORT (+COPY_1..3)", "latin_narrow": "FONT_NARROW",
           "latin_narrower": "FONT_NARROWER", "latin_small": "FONT_SMALL", "latin_small_narrow": "FONT_SMALL_NARROW",
           "latin_small_narrower": "FONT_SMALL_NARROWER", "latin_short_narrow": "FONT_SHORT_NARROW",
           "latin_short_narrower": "FONT_SHORT_NARROWER"}


def charmap():
    cm = {}
    for line in open(os.path.join(ROOT, "charmap.txt"), encoding="utf-8"):
        m = re.match(r"^'(.+?)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m and len(m.group(1)) == 1 and m.group(1) not in cm:
            cm[m.group(1)] = int(m.group(2), 16)
    cm["'"] = 0xB4
    return cm


def widths(sym):
    src = open(os.path.join(ROOT, "src", "fonts.c")).read()
    body = re.search(sym + r"\[\]\s*=\s*\{(.*?)\};", src, re.S).group(1)
    return [int(v) for v in re.findall(r"\d+", body)]


def cell(px, code):
    ox, oy = (code % 16) * 16, (code // 16) * 16
    return [[px[ox + x, oy + y] for x in range(16)] for y in range(16)]


def ink_of(c):
    return {(x, y) for y in range(16) for x in range(16) if c[y][x] == 1}


def build_delta(px, cm, w_o):
    """Return 16x16 cell for δ in this font, built from its 'o' and 'd'."""
    o = cell(px, cm["o"])
    d = cell(px, cm["d"])
    o_ink = ink_of(o)
    bowl_top = min(y for _, y in o_ink)
    asc_top = min(y for _, y in ink_of(d))
    xs = [x for x, _ in o_ink]
    x0, x1 = min(xs), max(xs)              # ink columns of the bowl
    hook_rows = bowl_top - asc_top
    ink = set(o_ink)
    r = asc_top
    if hook_rows >= 3:
        for x in range(x0 + 1, x1 + 1):     # top bar, reaching the right edge
            ink.add((x, r))
        ink.add((x0, r + 1))                # curl back to the left
        ink.add((x0 + 1, r + 2))            # stroke heading into the bowl top
    else:
        for x in range(x0 + 1, x1 + 1):
            ink.add((x, r))
        ink.add((x0, r + 1))                # diagonal into the bowl top
    # background: the 'o' cell's box (index 3 inside the width, 0 outside)
    out = [[(3 if o[y][x] in (1, 2, 3) else o[y][x]) for x in range(16)] for y in range(16)]
    for (x, y) in ink:
        out[y][x] = 1
    for (x, y) in ink:
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            sx, sy = x + dx, y + dy
            if sx < w_o and sy < 16 and (sx, sy) not in ink and out[sy][sx] != 0:
                out[sy][sx] = 2
    return out


def patched_fonts():
    """{font: (PIL image with δ, widths list with δ)} — in memory."""
    cm = charmap()
    res = {}
    for f, sym in FONTS.items():
        im = Image.open(os.path.join(ROOT, "graphics", "fonts", f + ".png")).copy()
        px = im.load()
        W = widths(sym)
        w_o = W[cm["o"]]
        dc = build_delta(px, cm, w_o)
        ox, oy = (DELTA_CODE % 16) * 16, (DELTA_CODE // 16) * 16
        for y in range(16):
            for x in range(16):
                px[ox + x, oy + y] = dc[y][x] if x < w_o else (0 if dc[y][x] == 0 else 0)
        W = list(W)
        W[DELTA_CODE] = w_o
        res[f] = (im, W)
    return res


COL = {0: (144, 200, 255), 1: (56, 56, 56), 2: (216, 216, 216), 3: (255, 255, 255)}
LABEL_TTF = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def label_font(size=13):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(LABEL_TTF, size)
    except OSError:
        return ImageFont.load_default()


def render_text(res, font, s, fg=(56, 56, 56), sh=(216, 216, 216), bg=(255, 255, 255), cm=None):
    """String -> RGB image (height 16) in a patched ROM font."""
    cm = cm or dict(charmap(), **{"δ": DELTA_CODE})
    im, W = res[font]
    px = im.load()
    w = sum(W[cm.get(ch, 0)] for ch in s)
    out = Image.new("RGB", (max(1, w), 16), bg)
    op = out.load()
    x = 0
    for ch in s:
        code = cm.get(ch, 0)
        c = cell(px, code)
        for gy in range(16):
            for gx in range(min(W[code], 16)):
                v = c[gy][gx]
                if v == 1:
                    op[x + gx, gy] = fg
                elif v == 2 and sh is not None:
                    op[x + gx, gy] = sh
        x += W[code]
    return out


def closeup(res, path, k=6):
    cm = dict(charmap(), **{"δ": DELTA_CODE})
    chars = ["δ", "o", "d", "a", "e", "6", "D"]
    lf = label_font(14)
    lfs = label_font(12)
    label_w = 190
    row_h = 16 * k + 16
    words = ["Gyarados-δ", "Farfetch'd-δ"]
    glyph_area = len(chars) * (6 * k + 2 * k)
    sheet = Image.new("RGB", (label_w + glyph_area + 520, len(res) * row_h + 44), (36, 36, 44))
    dr = ImageDraw.Draw(sheet)
    dr.text((label_w, 8), "  ".join(chars) + "   (δ = new glyph at 0x%02X, gold cell)" % DELTA_CODE, fill=(235, 235, 235), font=lf)
    dr.text((label_w + glyph_area + 10, 8), "words at 3x (ROM widths)", fill=(235, 235, 235), font=lf)
    y = 36
    for f, (im, W) in res.items():
        px = im.load()
        dr.text((8, y + 6 * k - 14), f, fill=(235, 235, 235), font=lf)
        dr.text((8, y + 6 * k + 4), FONT_ID[f], fill=(160, 160, 200), font=lfs)
        x = label_w
        for ch in chars:
            code = cm[ch]
            c = cell(px, code)
            w = W[code]
            for gy in range(16):
                for gx in range(w):
                    v = c[gy][gx]
                    col = COL.get(v, (255, 0, 255))
                    if ch == "δ" and v == 3:
                        col = (255, 240, 190)
                    dr.rectangle([x + gx * k, y + gy * k, x + gx * k + k - 1, y + gy * k + k - 1], fill=col)
            x += w * k + 2 * k
        x = label_w + glyph_area + 10
        for wd in words:
            t = render_text(res, f, wd, cm=cm)
            t = t.resize((t.width * 3, t.height * 3), Image.NEAREST)
            sheet.paste(t, (x, y + 12))
            dr.text((x, y + 12 + 50), "%d px" % (t.width // 3), fill=(170, 170, 170), font=lfs)
            x += t.width + 16
        y += row_h
    sheet.save(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    res = patched_fonts()
    fdir = os.path.join(HERE, "fonts")
    os.makedirs(fdir, exist_ok=True)
    wj = {}
    for f, (im, W) in res.items():
        im.save(os.path.join(fdir, f + ".png"))
        wj[f] = W[DELTA_CODE]
    json.dump({"code": "0x%02X" % DELTA_CODE, "widths": wj}, open(os.path.join(fdir, "widths.json"), "w"), indent=1)
    closeup(res, os.path.join(OUT, "glyph_closeup.png"))
    for f, w in wj.items():
        print(f, "δ width", w)


if __name__ == "__main__":
    main()
