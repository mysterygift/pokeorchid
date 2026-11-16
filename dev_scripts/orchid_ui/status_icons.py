"""
Orchid status icons — shared by the battle healthboxes and the party menu.

Pictogram tags instead of Gen 3's PSN / PAR / SLP / ... letter icons.

Each icon fills one 16x16 OBJ cell: a rounded tag (kit 1px ink outline, Gen 3 bevel:
light top/left, dark bottom/right) whose coloured FACE is the 12x12 area x 2..13,
y 2..13. Face colour = Gen 3 status hue (graphics/interface/status_icons.png,
BGR555-snapped). The white 8x8 (or 6x8) pictogram is centred exactly on that face:
equal left/right and top/bottom margins, >= 2px (no drop shadow, so nothing skews
the centring). tox = white skull with eye sockets / nose / teeth in the dark tone.

All kinds share ONE 16-colour OBJ palette (STATUS_PAL):
    0 transparent   1 ink   2 white (pictogram + top-left bevel)
    3/4  psn  face/dark      5/6  par  face/dark      7/8  slp  face/dark
    9/10 frz  face/dark     11/12 brn  face/dark     13/14 fnt  face/dark
    15   tox  face (shares psn dark)
    pkrs uses the psn ramp (as Gen 3 does), frb uses the frz ramp.

API
    KINDS                       tuple of supported kinds
    STATUS_PAL                  16 RGB tuples (the shared OBJ palette)
    status_index(kind) -> P     16x16 indexed image (palette = STATUS_PAL) for export
    status_icon(kind)  -> RGBA  16x16, index 0 transparent
    TAG_W, TAG_H                tag size (16x16 = the whole OBJ cell)
    FACE                        (x0, y0, x1, y1) of the coloured face inside the tag
    margins(kind) -> (L, R, T, B)   pictogram margins to the face edge
    status_sheet(scale=4)       review sheet: icons at scale + margin readout, 1x/2x strips, palette
"""
from PIL import Image, ImageDraw
from kit import snap, Canvas, rounded_box

CELL, TAG_W, TAG_H = 16, 16, 16
FACE = (2, 2, 13, 13)          # coloured face inside outline + bevel (12x12)
KINDS = ("psn", "tox", "par", "slp", "brn", "frz", "frb", "fnt", "pkrs")

INK_I, WHITE_I = 1, 2
_RAMP = {  # face (Gen 3 status_icons.png main colour), dark (bottom-right bevel + pictogram shadow)
    "psn": ((192, 96, 192), (128, 48, 136)),
    "par": ((184, 176, 24), (128, 112, 8)),
    "slp": ((160, 160, 136), (104, 104, 88)),
    "frz": ((120, 168, 224), (64, 104, 168)),
    "brn": ((232, 112, 80), (168, 56, 40)),
    "fnt": ((184, 40, 40), (112, 16, 32)),
}
TOX_FACE = (144, 56, 160)
STATUS_PAL = [snap(c) for c in
              [(0, 0, 0), (40, 40, 64), (248, 248, 248)]
              + [c for k in ("psn", "par", "slp", "frz", "brn", "fnt") for c in _RAMP[k]]
              + [TOX_FACE]]
_IDX = {k: (3 + 2 * i, 4 + 2 * i) for i, k in enumerate(("psn", "par", "slp", "frz", "brn", "fnt"))}
_IDX["tox"] = (15, _IDX["psn"][1])
_IDX["pkrs"] = _IDX["psn"]
_IDX["frb"] = _IDX["frz"]

# Pictograms: X = white, d = the tag's dark tone. Even sizes (8x8 / 6x8) so they centre
# exactly on the 12x12 face with equal margins (2 or 3 px).
_PICTO = {
    "psn": ["...XX...",       # droplet
            "...XX...",
            "..XXXX..",
            "..XXXX..",
            ".XXXXXX.",
            "XXXXXXXX",
            "XXXXXXXX",
            ".XXXXXX."],
    "tox": [".XXXXXX.",       # skull: badly poisoned
            "XXXXXXXX",
            "XddXXddX",
            "XddXXddX",
            "XXXddXXX",
            ".XXXXXX.",
            ".XdXXdX.",
            "..XXXX.."],
    "par": ["....XX",         # lightning bolt
            "...XX.",
            "..XX..",
            ".XXXXX",
            "XXXXX.",
            "..XX..",
            ".XX...",
            "XX...."],
    "slp": ["XXXXXX",         # Z
            "XXXXXX",
            "...XX.",
            "..XX..",
            ".XX...",
            "XX....",
            "XXXXXX",
            "XXXXXX"],
    "brn": ["...X....",       # flame
            "..XX....",
            "..XXX.X.",
            ".XXXXXX.",
            ".XXXXXXX",
            "XXXXXXXX",
            "XXXXXXXX",
            ".XXXXXX."],
    "frz": ["X..XX..X",       # snowflake
            ".X.XX.X.",
            "..XXXX..",
            "XXXXXXXX",
            "XXXXXXXX",
            "..XXXX..",
            ".X.XX.X.",
            "X..XX..X"],
    "frb": ["...XX...",       # ice crystal (frostbite)
            "..XXXX..",
            ".XXXXXX.",
            "XXX..XXX",
            "XXX..XXX",
            ".XXXXXX.",
            "..XXXX..",
            "...XX..."],
    "fnt": ["XX....XX",       # cross
            "XXX..XXX",
            ".XXXXXX.",
            "..XXXX..",
            "..XXXX..",
            ".XXXXXX.",
            "XXX..XXX",
            "XX....XX"],
    "pkrs": ["X......X",      # virus blob with spikes
             ".XXXXXX.",
             ".XXXXXX.",
             "XXX..XXX",
             "XXX..XXX",
             ".XXXXXX.",
             ".XXXXXX.",
             "X......X"],
}


def _new(w=CELL, h=CELL):
    im = Image.new("P", (w, h), 0)
    flat = [v for c in STATUS_PAL for v in c]
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


def status_index(kind):
    """16x16 'P' image on STATUS_PAL (index 0 transparent)."""
    kind = kind.lower()
    face, dark = _IDX[kind]
    im = _new()
    cv = Canvas(im)
    rounded_box(cv, 0, 0, TAG_W, TAG_H, 3, face, INK_I, WHITE_I, dark)
    pic = _PICTO[kind]
    pw, ph = len(pic[0]), len(pic)
    fw, fh = FACE[2] - FACE[0] + 1, FACE[3] - FACE[1] + 1
    assert (fw - pw) % 2 == 0 and (fh - ph) % 2 == 0, kind
    x0, y0 = FACE[0] + (fw - pw) // 2, FACE[1] + (fh - ph) // 2
    for r, row in enumerate(pic):
        for q, ch in enumerate(row):
            if ch == "X":
                cv.set(x0 + q, y0 + r, WHITE_I)
            elif ch == "d":
                cv.set(x0 + q, y0 + r, dark)
    return im


def margins(kind):
    """Measured margins (L, R, T, B) from the pictogram's own pixels to the face edge
    (pictogram drawn alone, so the bevel's corner pixels don't count)."""
    im = status_index(kind)
    ref = _new()
    rc = Canvas(ref)
    face, dark = _IDX[kind.lower()]
    rounded_box(rc, 0, 0, TAG_W, TAG_H, 3, face, INK_I, WHITE_I, dark)
    a, b = im.load(), ref.load()
    pts = [(x, y) for y in range(CELL) for x in range(CELL) if a[x, y] != b[x, y]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs) - FACE[0], FACE[2] - max(xs), min(ys) - FACE[1], FACE[3] - max(ys)


def status_icon(kind):
    """16x16 RGBA, transparent background."""
    im = status_index(kind)
    rgba = im.convert("RGBA")
    rp, ip = rgba.load(), im.load()
    for y in range(CELL):
        for x in range(CELL):
            if ip[x, y] == 0:
                rp[x, y] = (0, 0, 0, 0)
    return rgba


def status_sheet(scale=4, bg=(28, 28, 36)):
    """Review sheet: each icon at `scale`, then a 1x strip on light + dark, then the palette."""
    n = len(KINDS)
    pad = 12
    cw = max(CELL * scale, 76) + pad
    W = pad + n * cw
    Hh = pad + 14 + CELL * scale + 32 + 2 * (CELL * 2 + 8) + 20 + 40
    sheet = Image.new("RGBA", (W, Hh), bg + (255,))
    d = ImageDraw.Draw(sheet)
    y = pad
    for i, k in enumerate(KINDS):
        x = pad + i * cw
        d.text((x, y), k, fill=(230, 230, 240))
        ic = status_icon(k).resize((CELL * scale, CELL * scale), Image.NEAREST)
        sheet.alpha_composite(ic, (x, y + 14))
        d.text((x, y + 16 + CELL * scale), "L%d R%d T%d B%d" % margins(k), fill=(200, 200, 210))
    y += 14 + CELL * scale + 18 + 14
    # 1x and 2x on a light panel and on near-black, to judge readability at real size
    for k2, base in enumerate(((232, 232, 224), (24, 24, 32))):
        strip = Image.new("RGBA", (n * 20 + 4, CELL + 4), base + (255,))
        for i, k in enumerate(KINDS):
            strip.alpha_composite(status_icon(k), (2 + i * 20, 2))
        sheet.alpha_composite(strip, (pad, y))
        sheet.alpha_composite(strip.resize((strip.size[0] * 2, strip.size[1] * 2), Image.NEAREST),
                              (pad + strip.size[0] + 16, y))
        y += CELL * 2 + 8
    d.text((pad, y), "shared OBJ palette (STATUS_PAL)", fill=(230, 230, 240))
    y += 16
    for i, c in enumerate(STATUS_PAL):
        d.rectangle((pad + i * 24, y, pad + i * 24 + 20, y + 20), fill=c, outline=(70, 70, 80))
    return sheet


if __name__ == "__main__":
    import sys
    status_sheet().save(sys.argv[1] if len(sys.argv) > 1 else "status_icons.png")
