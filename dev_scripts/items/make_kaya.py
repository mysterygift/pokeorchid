"""Kaya toast icon draft: 3/4 top-down like the kopi/tea icons, ink outline, light from the top-left.
Uses the existing kaya_toast.pal. usage: make_kaya.py REPO OUTDIR  (then copy OUTDIR/kaya_toast.png to graphics/items/icons)"""
import os
import sys
from PIL import Image, ImageDraw

repo, out = sys.argv[1], sys.argv[2]
pal = [tuple(int(v) for v in l.split()) for l in
       open(os.path.join(repo, "graphics/items/icon_palettes/kaya_toast.pal")).read().split("\n")[3:19]]
OUT, CRUST, TAN, BREAD, KAYA_L, KAYA_D, BUTTER, CREAM, WHITE, PLATE_SH = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

W = 24
im = Image.new("P", (W, W), 0)
im.putpalette([c for rgb in pal for c in rgb] + [0] * (768 - 48))
d = ImageDraw.Draw(im)
px = im.load()

# plate: white ellipse, shaded lower rim, ink outline
d.ellipse((0, 12, 23, 22), fill=WHITE, outline=OUT)
for y in range(12, 23):
    for x in range(24):
        if px[x, y] == WHITE:
            # lower rim band (inside the outline, below centre) gets the shade colour
            if y >= 18 and (px[x, y + 1] == OUT or (y + 1 < 24 and px[x, min(y + 2, 23)] == OUT)):
                px[x, y] = PLATE_SH
# inner well line on the plate
d.arc((3, 14, 20, 21), 20, 160, fill=PLATE_SH)

# toast sandwich: rotated slice, top face + two side faces 4px deep
DY = 2                       # toast sits 2px lower on the plate
L, T, R, B = (4, 8 + DY), (12, 4 + DY), (20, 8 + DY), (12, 12 + DY)
DEPTH = 5
top = [L, T, R, B]
left_face = [L, B, (B[0], B[1] + DEPTH), (L[0], L[1] + DEPTH)]
right_face = [B, R, (R[0], R[1] + DEPTH), (B[0], B[1] + DEPTH)]

mask = Image.new("L", (W, W), 0)
md = ImageDraw.Draw(mask)
for poly in (top, left_face, right_face):
    md.polygon(poly, fill=255)
mp = mask.load()


def edge_y(face, x):
    """y of the top edge of a side face at column x."""
    (x0, y0), (x1, y1) = face[0], face[1]
    t = (x - x0) / max(1, (x1 - x0))
    return round(y0 + (y1 - y0) * t)


# side faces: layers by depth below the top edge
for x in range(W):
    for face, lit in ((left_face, True), (right_face, False)):
        if not (face[0][0] <= x <= face[1][0]):
            continue
        y0 = edge_y(face, x)
        layers = [BREAD if lit else TAN,            # top slice (crumb)
                  KAYA_L if lit else KAYA_D,         # kaya
                  BUTTER if lit else BREAD,          # cold butter slab
                  BREAD if lit else TAN,             # bottom slice
                  CRUST]                             # bottom crust
        for k, c in enumerate(layers):
            y = y0 + 1 + k
            if 0 <= y < W:
                px[x, y] = c
# kaya darkens at the outer corners; butter only in the middle stretch of each face
for face in (left_face, right_face):
    for x in range(face[0][0], face[1][0] + 1):
        y0 = edge_y(face, x)
        mid = abs(x - (face[0][0] + face[1][0]) / 2) <= 2.5
        if not mid:
            px[x, y0 + 3] = px[x, y0 + 2] if False else (KAYA_D if face is right_face else KAYA_L)

# top face: toasted tan with crust border, grill marks, top-left highlight
d.polygon(top, fill=TAN)
# front (lower) edges of the top slice: 1px crust
for x in range(L[0], R[0] + 1):
    face = left_face if x <= B[0] else right_face
    px[x, edge_y(face, x)] = CRUST
# upper edges catch the light (crumb colour), lower edges stay crust
for x in range(L[0] + 1, T[0] + 1):
    px[x, edge_y([L, T], x)] = BREAD
for x in range(T[0], R[0]):
    px[x, edge_y([T, R], x)] = CREAM if x == T[0] else TAN
# a few toast marks (sparse, darker) and a highlight
for (x, y) in ((9, 8), (10, 8), (14, 7), (13, 9), (14, 9)):
    px[x, y + DY] = BREAD
for (x, y) in ((10, 6), (11, 6), (9, 7)):
    px[x, y + DY] = CREAM

# ink outline around the toast (over the plate / transparency)
toast = {(x, y) for y in range(W) for x in range(W) if mp[x, y]}
for (x, y) in list(toast):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        q = (x + dx, y + dy)
        if q not in toast and 0 <= q[0] < W and 0 <= q[1] < W:
            px[q] = OUT

os.makedirs(out, exist_ok=True)
im.save(os.path.join(out, "kaya_toast.png"), transparency=0)
rgb = im.convert("RGB")
rgb.resize((240, 240), Image.NEAREST).save(os.path.join(out, "kaya_big.png"))
