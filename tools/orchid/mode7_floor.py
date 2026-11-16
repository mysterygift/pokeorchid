#!/usr/bin/env python3
"""Mode 7 battle floor tools for Pokémon Orchid.

A floor is a 512x512 top-down texture (mode7_floor.png, 8-bit indexed). Its
pixels must use palette indices 32-79 (BG palette rows 2-4); index 0 is
transparent. The runtime renders it as an affine BG2 plane in BG mode 1
(src/battle_mode7.c) and loads the PNG's rows 2-4 as the floor palette, so a
floor may use the environment's unused palette slots for extra colours.

Hardware/VRAM limits enforced here:
  * 8bpp tiles, no flips, deduplicated to at most 256 unique tiles (one full
    BG charblock, 16 KB);
  * map is 64x64 one-byte tile numbers (4 KB).
Tip: stamp identical detail at identical (x % 8, y % 8) alignment so tiles
are shared, e.g. the same platform design under both battlers.

Subcommands:
  convert <floor.png> <out_dir>   -> mode7_tiles.bin, mode7_map.bin, mode7_palette.pal
  grass   <env_dir> <out.png>     generate the procedural tall-grass floor

World layout shared with the C code (include/battle_mode7.h):
  player platform centre (204, 400), opponent platform centre (316, 208).
  Column 0 (x 0-7) must stay plain ground: the runtime samples texel (4, 8)
  for the distance haze.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pngio import read_indexed, write_indexed, read_jasc  # noqa: E402

SIZE = 512
MAX_TILES = 256
PLAYER_PLATFORM = (204, 400)
OPPONENT_PLATFORM = (316, 208)
PLATFORM_RADIUS = 64
HAZE_TEXEL = (4, 8)


def convert(png_path, out_dir):
    w, h, px, pal = read_indexed(png_path)
    if (w, h) != (SIZE, SIZE):
        sys.exit(f"{png_path}: floor must be {SIZE}x{SIZE}, got {w}x{h}")
    tiles, lookup, tmap = [], {}, bytearray()
    for ty in range(SIZE // 8):
        for tx in range(SIZE // 8):
            block = bytes(px[ty * 8 + y][tx * 8 + x] for y in range(8) for x in range(8))
            if block not in lookup:
                lookup[block] = len(tiles)
                tiles.append(block)
            tmap.append(lookup[block] if len(tiles) <= MAX_TILES else 0)
    if len(tiles) > MAX_TILES:
        sys.exit(f"{png_path}: {len(tiles)} unique tiles, limit is {MAX_TILES}")
    bad = {v for t in tiles for v in t if v and not 32 <= v < 80}
    if bad:
        sys.exit(f"{png_path}: pixel values {sorted(bad)} outside palette rows 2-4 (32-79)")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "mode7_tiles.bin"), "wb") as f:
        for t in tiles:
            f.write(t)
        f.write(bytes(64 * (MAX_TILES - len(tiles))))  # fixed 16 KB for a single fast copy
    with open(os.path.join(out_dir, "mode7_map.bin"), "wb") as f:
        f.write(tmap)
    pal = list(pal) + [(0, 0, 0)] * (256 - len(pal))
    with open(os.path.join(out_dir, "mode7_palette.pal"), "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n48\n")
        for r, g, b in pal[32:80]:
            f.write(f"{r} {g} {b}\n")
    print(f"{png_path}: {len(tiles)}/{MAX_TILES} tiles -> {out_dir}")


# ---------------------------------------------------------------------------
# Procedural tall-grass floor
# ---------------------------------------------------------------------------
GROUND = 47          # pale mint (environment colour)
GROUND_FLECK = 45
GROUND_FLECK_DARK = 44
SHADOW = 43          # soft ring around each platform
RIM = 35             # bright yellow-green rim (classic look)
BEVEL = 36
FILL = 34
FILL_LIGHT = 37
DOT = 39
DOT_LIGHT = 38
# extra colours in the environment's unused palette slots
EXTRA = {
    40: (98, 180, 98),     # platform shade
    41: (66, 140, 66),     # tuft base shadow
    42: (49, 115, 57),     # tuft darkest
    56: (82, 164, 74),     # tuft dark
    57: (106, 197, 90),    # tuft mid
    58: (139, 222, 106),   # tuft light
    68: (180, 238, 131),   # tuft tip
    69: (115, 189, 115),   # platform edge shade
}
SHADE, TUFT_SHADOW, TUFT_0, TUFT_1, TUFT_2, TUFT_3, TUFT_TIP, EDGE_SHADE = 40, 41, 42, 56, 57, 58, 68, 69


def _put(px, x, y, c):
    px[y % SIZE][x % SIZE] = c


def _platform(px, cx, cy, r, rng):
    for y in range(cy - r - 12, cy + r + 13):
        for x in range(cx - r - 12, cx + r + 13):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            if d >= r + 11:
                continue
            checker = (x + y) % 2 == 0
            if d >= r - 1:
                # shadow fades out with distance instead of ending in a hard ring
                fade = (d - (r - 1)) / 12.0
                if rng.random() > fade * fade * 1.4 and (checker or rng.random() > fade):
                    _put(px, x, y, SHADOW)
            elif d >= r - 4:
                # broken-up rim: grass blades drawn later fill the gaps
                n = rng.random()
                _put(px, x, y, RIM if n < 0.72 else BEVEL if n < 0.9 else FILL)
            elif d >= r - 6:
                _put(px, x, y, BEVEL if rng.random() < 0.8 else FILL_LIGHT)
            else:
                # light from the top-left: round highlight, crescent shade lower-right
                hl = math.hypot(dx + r * 0.18, dy + r * 0.18)
                sh = math.hypot(dx + r * 0.22, dy + r * 0.22)
                c = FILL
                if hl < r * 0.48 or (hl < r * 0.54 and checker):
                    c = FILL_LIGHT
                if sh > r * 1.04 or (sh > r * 0.98 and checker):
                    c = SHADE
                if d > r - 9 and sh > r * 0.98:
                    c = EDGE_SHADE
                # tile-aligned speckle so interior tiles stay shared
                if x % 8 == 2 and y % 8 == 3:
                    c = DOT
                elif x % 8 == 6 and y % 8 == 7 and c != SHADE:
                    c = DOT_LIGHT
                _put(px, x, y, c)


def _tuft(px, bx, by, rng, scale=1.0):
    """A clump of blades. Blades run toward -y (away from the camera) and are
    drawn ~3x long so the perspective squash leaves them looking upright."""
    for sx in range(-3, 4):
        if abs(sx) < 3 or rng.random() < 0.5:
            _put(px, bx + sx, by, TUFT_SHADOW)
            _put(px, bx + sx, by + 1, TUFT_SHADOW if abs(sx) < 2 else SHADOW)
    blades = rng.randint(4, 6)
    for i in range(blades):
        x0 = bx + (i - blades // 2) * 2 + rng.choice((-1, 0, 0, 1))
        length = int(rng.randint(10, 16) * scale)
        lean = rng.choice((-1, -0.5, 0, 0.5, 1)) / length * 3
        for t in range(length):
            x = round(x0 + lean * t)
            y = by - t
            f = t / length
            c = TUFT_0 if f < 0.25 else TUFT_1 if f < 0.5 else TUFT_2 if f < 0.75 else TUFT_3
            if t == length - 1:
                c = TUFT_TIP
            _put(px, x, y, c)
            if f < 0.4:
                _put(px, x + 1, y, TUFT_0 if f < 0.2 else TUFT_1)


def _blade(px, x0, y0, length, ramp, lean):
    for t in range(length):
        f = t / max(1, length - 1)
        c = ramp[min(len(ramp) - 1, int(f * len(ramp)))]
        _put(px, round(x0 + lean * t), y0 - t, c)


def _feathered_edge(px, cx, cy, r, rng):
    """Hundreds of short blades straddling the rim so the platform edge melts
    into the surrounding grass. Density and height peak at the rim and fall
    off both inward (onto the dish) and outward (onto the ground)."""
    inner_ramp = (FILL, DOT, FILL_LIGHT, RIM)                 # blades on the dish
    rim_ramp = (TUFT_1, TUFT_2, TUFT_3, RIM, TUFT_TIP)        # blades on the rim
    outer_ramp = (TUFT_0, TUFT_1, TUFT_2, TUFT_3, TUFT_TIP)   # blades on the ground
    for _ in range(420):
        a = rng.uniform(0, 2 * math.pi)
        # triangular distribution centred just outside the rim
        off = rng.triangular(-9, 14, 1)
        rad = r + off
        x0 = cx + round(rad * math.cos(a))
        y0 = cy + round(rad * math.sin(a))
        closeness = 1 - min(1.0, abs(off - 1) / 13)
        length = max(2, round((4 + 9 * closeness) * rng.uniform(0.6, 1.1)))
        ramp = inner_ramp if off < -3 else rim_ramp if off < 3 else outer_ramp
        if off > 8 and rng.random() < 0.5:
            continue  # thin out the far edge
        _blade(px, x0, y0, length, ramp, rng.choice((-0.25, 0, 0, 0.25)))


def grass(env_dir, out_png):
    rng = random.Random(1987)
    pal = read_jasc(os.path.join(env_dir, "palette.pal"))
    full = [(0, 0, 0)] * 32 + pal + [(0, 0, 0)] * (256 - 32 - len(pal))
    for i, c in EXTRA.items():
        if full[i] != (0, 0, 0):
            sys.exit(f"palette slot {i} is already used by the environment")
        full[i] = c

    px = [[GROUND] * SIZE for _ in range(SIZE)]

    # very sparse ground flecks, a perspective cue for the moving camera
    flecks = [[(3, 4), (4, 4)], [(2, 5), (3, 4), (4, 5)]]
    for ty in range(SIZE // 8):
        for tx in range(1, SIZE // 8):
            centre = (tx * 8 + 4, ty * 8 + 4)
            near = any(math.dist(centre, p) < PLATFORM_RADIUS + 26 for p in (PLAYER_PLATFORM, OPPONENT_PLATFORM))
            if not near and rng.random() < 0.05:
                shape = flecks[rng.randrange(len(flecks))]
                col = GROUND_FLECK if rng.random() < 0.7 else GROUND_FLECK_DARK
                for (x, y) in shape:
                    px[ty * 8 + y][tx * 8 + x] = col

    # Both platforms get the identical stamp (same tile alignment), so their tiles are shared.
    stamp_rng_seed = rng.random()
    for (cx, cy) in (PLAYER_PLATFORM, OPPONENT_PLATFORM):
        srng = random.Random(stamp_rng_seed)
        _platform(px, cx, cy, PLATFORM_RADIUS, srng)
        _feathered_edge(px, cx, cy, PLATFORM_RADIUS, srng)
        clumps = 12
        for k in range(clumps):
            a = 2 * math.pi * k / clumps + srng.uniform(-0.12, 0.12)
            rad = PLATFORM_RADIUS + srng.uniform(-1, 4)
            bx = cx + round(rad * math.cos(a))
            by = cy + round(rad * math.sin(a))
            _tuft(px, bx, by, srng, scale=1.15 if math.sin(a) < 0 else 0.9)
        # a few loose tufts further out
        for k in range(6):
            a = srng.uniform(0, 2 * math.pi)
            rad = PLATFORM_RADIUS + srng.uniform(10, 18)
            _tuft(px, cx + round(rad * math.cos(a)), cy + round(rad * math.sin(a)), srng, scale=0.7)

    px[HAZE_TEXEL[1]][HAZE_TEXEL[0]] = GROUND
    write_indexed(out_png, SIZE, SIZE, px, full)
    print(f"wrote {out_png}")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "convert":
        convert(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 4 and sys.argv[1] == "grass":
        grass(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
