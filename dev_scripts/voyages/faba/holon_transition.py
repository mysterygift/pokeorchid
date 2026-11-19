"""B_TRANSITION_HOLON mock: the Holon Energy logo (black six-pointed star in a white disc, crackling energy
ring; ref/holon_energy_card.png) as a battle-start transition built exactly like vanilla B_TRANSITION_AQUA.

Format = graphics/battle_transitions/team_aqua.png + team_aqua.bin:
  - tileset PNG 64x96 (8x12 = 96 tiles max), 4bpp indexed, drawn in the shared evil_team.pal indices
    (1 black, 2/3/4 greys, 5 dark grey, 15 white), so the Aqua/Magma palette load is reused unchanged
  - tilemap .bin: 32x32 u16 entries (2048 bytes), palette 15, tile 0 blank; the logo is mirror-symmetric
    on both axes, so one quadrant is drawn and the rest are h/v-flipped tile references
Animation = the PatternWeave states of src/battle_transition.c (Aqua_Init -> Aqua_SetGfx -> PatternWeave_Blend1
-> PatternWeave_Blend2 -> PatternWeave_FinishAppear -> FramesCountdown(60) -> PatternWeave_CircularMask),
preceded by the generic 3x grey-flash intro (CreateIntroTask(0, 0, 3, 2, 2)), simulated frame by frame over a
Holon field screenshot.

Outputs (faba/): holon_logo.png (64x96 tiles), holon_logo.bin (tilemap)
Renders (out/batch8_faba/): holon_transition.gif, holon_transition_keyframes_x2.png, holon_logo_sheet.png
"""
import math
import os
import random
import struct
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.abspath(os.path.join(HERE, '..', 'out', 'batch8_faba'))
os.makedirs(OUT, exist_ok=True)
W, H = 240, 160
CX, CY = 120, 80


def read_jasc(p):
    lines = open(p).read().split('\n')
    return [tuple(int(v) for v in lines[3 + i].split()) for i in range(int(lines[2]))]


PAL = read_jasc(os.path.join(ROOT, 'graphics/battle_transitions/evil_team.pal'))
BLACK, G_DARK, G_MID, G_LIGHT, G_DEEP, WHITE = 1, 2, 3, 4, 5, 15

# ------------------------------------------------------------------ logo geometry
R_DISC = 47          # white disc radius
R_STAR, R_STAR_IN = 38, 17
RING = (56, 72)      # crackle band


def star_contains(px, py):
    """6-point star, points straight up/down (as on the card). Point-in-polygon on the 12 vertices."""
    pts = []
    for k in range(12):
        a = math.radians(90 + 30 * k)
        r = R_STAR if k % 2 == 0 else R_STAR_IN
        pts.append((r * math.cos(a), r * math.sin(a)))
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def quadrant():
    """Top-left quadrant (120x80) of the logo; pixel (x, y) has centre offset (x+0.5-120, 80-(y+0.5))."""
    q = [[0] * CX for _ in range(CY)]
    for y in range(CY):
        for x in range(CX):
            dx, dy = x + 0.5 - CX, CY - (y + 0.5)
            d = math.hypot(dx, dy)
            if d <= R_DISC:
                q[y][x] = BLACK if star_contains(dx, dy) else (G_LIGHT if d > R_DISC - 3 else WHITE)
            elif d <= R_DISC + 2:
                q[y][x] = BLACK
    # crackle: lightning arcs wandering round the band, white core -> mid-grey glow -> dark rim
    rnd = random.Random(11)
    core = set()
    # arcs (start angle, end angle, start radius): jagged zigzags, short spurs flicking off the corners
    arcs = [(91, 131, 64), (112, 160, 59), (138, 179, 66), (150, 172, 70), (96, 118, 70)]

    def seg(p, q):
        n = int(max(abs(q[0] - p[0]), abs(q[1] - p[1]))) + 1
        for t in range(n + 1):
            core.add((round(p[0] + (q[0] - p[0]) * t / n), round(p[1] + (q[1] - p[1]) * t / n)))

    def pt(a, r):
        return (CX + r * math.cos(math.radians(a)) - 0.5, CY - r * math.sin(math.radians(a)) - 0.5)

    for a0, a1, r0 in arcs:
        r, a, prev, flip = r0, a0, None, 1
        while a <= a1:
            r += flip * rnd.uniform(1.5, 3.5)
            flip = -flip if rnd.random() < 0.8 else flip
            r = max(RING[0] + 1, min(RING[1] - 1, r))
            p = pt(a, r)
            if prev:
                seg(prev, p)
                if rnd.random() < 0.25:     # spur
                    seg(p, pt(a + rnd.uniform(-3, 3), r + rnd.choice((-4, 4))))
            prev = p
            a += rnd.uniform(2.5, 5)
    core = {(x, y) for x, y in core if 0 <= x < CX and 0 <= y < CY}
    for x, y in core:
        q[y][x] = WHITE
    glow = set()
    for x, y in core:
        for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + ax, y + ay
                if 0 <= nx < CX and 0 <= ny < CY and q[ny][nx] == 0:
                    glow.add((nx, ny))
    for x, y in glow:
        q[y][x] = G_MID
    rim = set()
    for x, y in glow:
        for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + ax, y + ay
            if 0 <= nx < CX and 0 <= ny < CY and q[ny][nx] == 0:
                rim.add((nx, ny))
    for x, y in rim:            # dark rim only on the outer/inner side of the glow, not between strands
        if sum(1 for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1))
               if 0 <= x + ax < CX and 0 <= y + ay < CY and q[y + ay][x + ax] in (G_MID, WHITE)) <= 1:
            q[y][x] = G_DEEP
    return q


def full_logo():
    q = quadrant()
    img = [[0] * W for _ in range(H)]
    for y in range(CY):
        for x in range(CX):
            v = q[y][x]
            img[y][x] = v
            img[y][W - 1 - x] = v
            img[H - 1 - y][x] = v
            img[H - 1 - y][W - 1 - x] = v
    return img


# ------------------------------------------------------------------ tiles + tilemap
def tile_at(img, tx, ty):
    return tuple(tuple(img[ty * 8 + y][tx * 8 + x] for x in range(8)) for y in range(8))


def flips(t):
    h = tuple(tuple(reversed(r)) for r in t)
    v = tuple(reversed(t))
    hv = tuple(reversed(h))
    return {(0, 0): t, (1, 0): h, (0, 1): v, (1, 1): hv}


def build_tiles(img):
    blank = tuple(tuple(0 for _ in range(8)) for _ in range(8))
    tiles = [blank]
    lookup = {blank: (0, 0, 0)}
    tmap = [0] * (32 * 32)
    for ty in range(H // 8):
        for tx in range(W // 8):
            t = tile_at(img, tx, ty)
            if t not in lookup:
                idx = len(tiles)
                tiles.append(t)
                for (hf, vf), ft in flips(t).items():
                    lookup.setdefault(ft, (idx, hf, vf))
            idx, hf, vf = lookup[t]
            tmap[ty * 32 + tx] = idx | (hf << 10) | (vf << 11) | (15 << 12) if idx else 0
    return tiles, tmap


def save_tiles(tiles, path):
    assert len(tiles) <= 96, f'{len(tiles)} tiles > 96 (team_aqua.png budget)'
    im = Image.new('P', (64, 96), 0)
    flat = []
    for c in PAL:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % 8) * 8, (i // 8) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = t[y][x]
    im.save(path)


def decode(tiles_png, bin_path):
    """Rebuild the 240x160 BG0 image from the saved files, the way the GBA would (proves the files)."""
    t = Image.open(tiles_png)
    tp = t.load()
    ents = struct.unpack('<1024H', open(bin_path, 'rb').read())
    img = [[0] * W for _ in range(H)]
    for ty in range(H // 8):
        for tx in range(W // 8):
            e = ents[ty * 32 + tx]
            ti, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
            sx, sy = (ti % 8) * 8, (ti // 8) * 8
            for y in range(8):
                for x in range(8):
                    img[ty * 8 + y][tx * 8 + x] = tp[sx + (7 - x if hf else x), sy + (7 - y if vf else y)]
    return img


# ------------------------------------------------------------------ animation (PatternWeave)
SINE = [round(256 * math.sin(2 * math.pi * i / 256)) for i in range(256)]


def c5(c):
    return tuple((v >> 3) for v in c)


def c8(c):
    return tuple(min(255, v << 3 | v >> 2) for v in c)


def frame(field, logo, eva, evb, sin_index, amp, radius=None, gray=0):
    """One GBA frame: BG0 logo (per-scanline HOFS sine weave) alpha-blended over the field, optional
    WIN0 circular mask (outside = black backdrop), optional intro grey blend."""
    out = Image.new('RGB', (W, H))
    op = out.load()
    fp = field.load()
    for y in range(H):
        hofs = (SINE[(sin_index + 132 * y) & 0xFF] * amp) >> 8
        if radius is not None:
            dy = abs(y + 0.5 - CY)
            half = math.sqrt(max(0, radius * radius - dy * dy)) if dy <= radius else -1
        for x in range(W):
            if radius is not None and (half < 0 or abs(x + 0.5 - CX) > half):
                op[x, y] = (0, 0, 0)
                continue
            f = c5(fp[x, y])
            if gray:
                f = tuple(v + ((11 - v) * gray >> 4) for v in f)
            v = logo[y][(x + hofs) % 256] if (x + hofs) % 256 < W else 0
            if v:
                l = c5(PAL[v])
                f = tuple(min(31, (a * eva + b * evb) >> 4) for a, b in zip(l, f))
            op[x, y] = c8(f)
    return out


def timeline():
    """(label, kwargs) per game frame, following the vanilla state functions."""
    fr = []
    # intro: 3 grey flashes, +2/frame to 16 then -2/frame back
    for _ in range(3):
        for g in list(range(2, 17, 2)) + list(range(14, -1, -2)):
            fr.append(('intro', dict(gray=g, eva=0, evb=16, sin_index=0, amp=0)))
    eva, evb, si, amp, delay = 0, 16, 0, 0x4000, 0
    fr.append(('init', dict(eva=eva, evb=evb, sin_index=si, amp=amp >> 8)))
    fr.append(('setgfx', dict(eva=eva, evb=evb, sin_index=si, amp=amp >> 8)))
    state = 'blend1'
    while True:
        if state == 'blend1':
            if delay == 0 or (delay := delay - 1) == 0:
                eva += 1; delay = 2
            if eva > 15:
                state = 'blend2'
        elif state == 'blend2':
            if delay == 0 or (delay := delay - 1) == 0:
                evb -= 1; delay = 2
            if evb == 0:
                state = 'finish'
        si += 8; amp -= 256
        fr.append((state, dict(eva=min(eva, 16), evb=evb, sin_index=si, amp=max(amp, 0) >> 8)))
        if state == 'finish' and amp <= 0:
            break
    for _ in range(60):
        fr.append(('hold', dict(eva=16, evb=0, sin_index=si, amp=0)))
    radius, delta = 160, 256
    while radius > 0:
        if delta < 4 << 8:
            delta += 128
        radius = max(0, radius - (delta >> 8))
        fr.append(('mask', dict(eva=16, evb=0, sin_index=si, amp=0, radius=radius)))
    return fr


def main():
    img = full_logo()
    tiles, tmap = build_tiles(img)
    tpng = os.path.join(HERE, 'holon_logo.png')
    tbin = os.path.join(HERE, 'holon_logo.bin')
    save_tiles(tiles, tpng)
    open(tbin, 'wb').write(struct.pack('<1024H', *tmap))
    logo = decode(tpng, tbin)
    assert logo == img, 'tilemap decode mismatch'
    print(f'tiles {len(tiles)}/96 (team_aqua uses 82, team_magma 116 of 128); tilemap 2048 bytes')

    shot = Image.open(os.path.join(HERE, '..', 'e2e', 'shots', '35b_sphere_before.png')).convert('RGB')
    field = shot.resize((W, H), Image.NEAREST)

    tl = timeline()
    print('frames', len(tl), f'= {len(tl) / 59.73:.2f} s')
    gif = []
    for k, (lab, kw) in enumerate(tl):
        if k % 3 == 0 or k == len(tl) - 1:
            gif.append(frame(field, logo, **kw))
    gif = [g.convert('P', palette=Image.ADAPTIVE, colors=64) for g in gif]
    gif[0].save(os.path.join(OUT, 'holon_transition.gif'), save_all=True, append_images=gif[1:] + [gif[-1]] * 10,
                duration=50, loop=0, optimize=True)

    # key frames (2x): intro grey, blend1 mid, blend2 mid, logo held, mask closing
    picks = []
    seen = {}
    for k, (lab, kw) in enumerate(tl):
        seen.setdefault(lab, []).append(k)
    for lab, pos in (('intro', 0.25), ('blend1', 0.5), ('blend2', 0.5), ('hold', 0.0), ('mask', 0.5)):
        ks = seen[lab]
        k = ks[int(pos * (len(ks) - 1))]
        picks.append((f'{lab} f{k}', frame(field, logo, **tl[k][1])))
    S = 2
    sheet = Image.new('RGB', (len(picks) * (W * S + 6) - 6, H * S + 14), (50, 50, 50))
    d = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(picks):
        sheet.paste(im.resize((W * S, H * S), Image.NEAREST), (i * (W * S + 6), 14))
        d.text((i * (W * S + 6) + 2, 1), lab, fill=(255, 255, 255))
    sheet.save(os.path.join(OUT, 'holon_transition_keyframes_x2.png'))

    # logo sheet: our tiles + screen vs vanilla Aqua, and the card
    def screen(lg):
        im = Image.new('RGB', (W, H), (255, 0, 255))
        p = im.load()
        for y in range(H):
            for x in range(W):
                if lg[y][x]:
                    p[x, y] = PAL[lg[y][x]]
        return im
    aqua = decode(os.path.join(ROOT, 'graphics/battle_transitions/team_aqua.png'),
                  os.path.join(ROOT, 'graphics/battle_transitions/team_aqua.bin'))
    tiles_im = Image.open(tpng).convert('RGB').resize((64 * 3, 96 * 3), Image.NEAREST)
    card = Image.open(os.path.join(HERE, '..', 'ref', 'holon_energy_card.png')).convert('RGB').crop((70, 40, 245, 215))
    parts = [('Holon BG0 (magenta = transparent) 2x', screen(logo).resize((W * 2, H * 2), Image.NEAREST)),
             ('vanilla team_aqua 2x', screen(aqua).resize((W * 2, H * 2), Image.NEAREST)),
             (f'holon_logo.png {len(tiles)} tiles 3x', tiles_im), ('card ref', card)]
    sw = sum(p.width for _, p in parts) + 8 * (len(parts) - 1)
    sh = max(p.height for _, p in parts) + 14
    out = Image.new('RGB', (sw, sh), (50, 50, 50))
    d = ImageDraw.Draw(out)
    x = 0
    for lab, p in parts:
        out.paste(p, (x, 14)); d.text((x + 2, 1), lab, fill=(255, 255, 255)); x += p.width + 8
    out.save(os.path.join(OUT, 'holon_logo_sheet.png'))


if __name__ == '__main__':
    main()
