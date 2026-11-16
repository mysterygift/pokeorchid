"""Render text exactly like the ROM: glyphs from graphics/fonts/*.png, widths from src/fonts.c."""
import os
import re
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

_FONTS = {
    "normal": ("latin_normal.png", "gFontNormalLatinGlyphWidths"),
    "narrow": ("latin_narrow.png", "gFontNarrowLatinGlyphWidths"),
    "small": ("latin_small.png", "gFontSmallLatinGlyphWidths"),
}
_cache = {}


def _charmap():
    if "charmap" in _cache:
        return _cache["charmap"]
    cm = {}
    for line in open(os.path.join(ROOT, "charmap.txt"), encoding="utf-8"):
        m = re.match(r"^'(.+?)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m and len(m.group(1)) == 1 and m.group(1) not in cm:
            cm[m.group(1)] = int(m.group(2), 16)
    cm["'"] = 0xB4
    _cache["charmap"] = cm
    return cm


def _font(name):
    if name in _cache:
        return _cache[name]
    png, sym = _FONTS[name]
    im = Image.open(os.path.join(ROOT, "graphics", "fonts", png))
    src = open(os.path.join(ROOT, "src", "fonts.c")).read()
    body = re.search(sym + r"\[\]\s*=\s*\{(.*?)\};", src, re.S).group(1)
    widths = [int(v) for v in re.findall(r"\d+", body)]
    _cache[name] = (im.load(), widths)
    return _cache[name]


def text_width(s, font="normal", spacing=0):
    _, widths = _font(font)
    cm = _charmap()
    return sum(widths[cm.get(ch, 0)] + spacing for ch in s)


def draw_text(cv, x, y, s, fg, shadow, font="normal", spacing=0, line_h=16):
    """cv = kit.Canvas. fg/shadow are palette indices (None = skip)."""
    px, widths = _font(font)
    cm = _charmap()
    cx = x
    for ch in s:
        if ch == "\n":
            cx = x
            y += line_h
            continue
        code = cm.get(ch, 0)
        ox, oy = (code % 16) * 16, (code // 16) * 16
        w = widths[code]
        for gy in range(16):
            for gx in range(min(w, 16)):
                v = px[ox + gx, oy + gy]
                if v == 1:
                    cv.set(cx + gx, y + gy, fg)
                elif v == 2 and shadow is not None:
                    cv.set(cx + gx, y + gy, shadow)
        cx += w + spacing
    return cx
