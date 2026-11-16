#!/usr/bin/env python3
"""Orchid battle environments (Singapore set) - procedural pixel art + build.

  python3 tools/orchid/battle_envs.py <theme> [<theme> ...]
  python3 tools/orchid/battle_envs.py all

For each theme this writes graphics/battle_environment/orchid_<theme>/:
  mode7_floor.png      512x512 top-down floor (editable source art)
  mode7_tiles.bin      \\
  mode7_map.bin         > runtime Mode 7 data (via mode7_floor.convert)
  tiles.png, map.bin   classic flat 4bpp background, rendered from the floor
                       through the Mode 7 rest camera (used by the fallback,
                       e.g. while move backgrounds play)
  palette.pal          48 colours: row 2 = the theme, rows 3-4 = the original
                       environment rows (keeps the intro "entry" art coloured)
and regenerates src/data/battle_mode7_floors.h (floor data).

Every theme draws its floor only with palette row 2 (indices 33-47), so one
16-colour palette serves both the 8bpp floor and the 4bpp classic background.
Floor detail is built from tile-aligned decals and repeating bands so the
floor stays within 256 unique 8x8 tiles. Camera constants must match
src/battle_mode7.c.
"""
import math
import os
import random
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
from pngio import write_indexed, read_jasc  # noqa: E402
import mode7_floor as m7  # noqa: E402

SIZE = m7.SIZE
PLAYER, OPPONENT, RADIUS = m7.PLAYER_PLATFORM, m7.OPPONENT_PLATFORM, m7.PLATFORM_RADIUS
# Mode 7 rest camera (src/battle_mode7.c)
HORIZON, HEIGHT, FOCAL, MAX_DEPTH = -328, 418, 1470, 1740
REST_U, REST_V = 256, 1780
HAZE = (4, 8)

ROOT = "graphics/battle_environment"
HEADER = "src/data/battle_mode7_floors.h"


def C(i):
    """Palette row 2 colour i (1-15) as an 8bpp pixel value."""
    return 32 + i


def put(px, x, y, c):
    px[y % SIZE][x % SIZE] = c


def blade(px, x0, y0, length, ramp, lean=0.0):
    for t in range(length):
        f = t / max(1, length - 1)
        put(px, round(x0 + lean * t), y0 - t, ramp[min(len(ramp) - 1, int(f * len(ramp)))])


def world_from_screen(sx, sy):
    """Rest-camera inverse projection: where on the floor a screen point lands."""
    lam = HEIGHT / (sy - HORIZON)
    return round(REST_U + (sx - 120) * lam), round(REST_V - lam * FOCAL)


def dish(px, cx, cy, r, rng, fill, light, shade, rim, bevel, dot=None, dot2=None,
         shadow=None, shadow_reach=12, rim_break=0.72):
    """Round platform lit from the top-left with a soft shadow ring.

    Shading is in solid bands: Mode 7 samples the nearest texel, so single-pixel
    speckle and checker dithers shimmer as the camera moves. (dot, dot2 and
    rim_break are accepted for compatibility and ignored.)"""
    for y in range(cy - r - shadow_reach, cy + r + shadow_reach + 1):
        for x in range(cx - r - shadow_reach, cx + r + shadow_reach + 1):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            if d >= r - 1:
                if shadow is None:
                    continue
                wobble = 1.5 * math.sin(math.atan2(dy, dx) * 5)
                if d < r - 1 + shadow_reach * 0.5 + wobble:
                    put(px, x, y, shadow)
                continue
            if d >= r - 4:
                put(px, x, y, rim)
                continue
            if d >= r - 6:
                put(px, x, y, bevel)
                continue
            hl = math.hypot(dx + r * 0.18, dy + r * 0.18)
            sh = math.hypot(dx + r * 0.22, dy + r * 0.22)
            c = fill
            if hl < r * 0.5:
                c = light
            if sh > r * 1.0:
                c = shade
            put(px, x, y, c)


def put2(px, x, y, c):
    """2x2 mark: the smallest detail that stays stable under Mode 7 sampling."""
    for oy in (0, 1):
        for ox in (0, 1):
            put(px, x + ox, y + oy, c)


def near_platform(x, y, extra):
    return any(math.hypot(x - cx, y - cy) < RADIUS + extra for (cx, cy) in (PLAYER, OPPONENT))


def edge_points(rng, n, lo, hi, mode):
    for _ in range(n):
        yield rng.uniform(0, 2 * math.pi), rng.triangular(lo, hi, mode)


def scatter_decals(px, rng, decals, density, v_range=(0, SIZE), keep_clear=52):
    """Stamp decals (lists of (dx, dy, colour)) at tile-aligned origins so
    every copy of a decal reuses the same 8x8 tiles."""
    for ty in range(v_range[0] // 8, v_range[1] // 8):
        for tx in range(1, SIZE // 8):
            if near_platform(tx * 8 + 4, ty * 8 + 4, keep_clear) or rng.random() >= density:
                continue
            for (x, y, c) in rng.choice(decals):
                put(px, tx * 8 + x, ty * 8 + y, c)


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

def theme_beach():
    """East Coast Park: sand, shoreline and sea; coconut palms, casuarina, park lamp."""
    pal = [(0, 0, 0),
           (247, 234, 189),  # 1 sand
           (234, 214, 165),  # 2 sand fleck / footprint
           (214, 189, 140),  # 3 sand shadow
           (226, 201, 150),  # 4 dish (packed sand)
           (240, 220, 170),  # 5 dish light
           (196, 168, 120),  # 6 dish shade / driftwood
           (206, 194, 160),  # 7 wet sand  } cycled: the wave washes in and out
           (255, 255, 247),  # 8 foam      }
           (57, 123, 74),    # 9 vine
           (107, 173, 90),   # 10 leaf
           (181, 107, 206),  # 11 morning glory
           (66, 140, 198),   # 12 sea deep   }
           (99, 181, 222),   # 13 sea mid     } cycled: shimmer
           (156, 214, 239),  # 14 sea light  }
           (255, 247, 222)]  # 15 dry crust / shell
    S, SF, SS, F, FL, FS, WET, FOAM, V, L, MG, W0, W1, W2, PALE = (C(i) for i in range(1, 16))
    SHORE = 128  # sea for v < SHORE

    def draw(px, rng):
        # sea: horizontal swell bands, 8-row period, so the tiles repeat
        for v in range(SHORE):
            for u in range(SIZE):
                band = (v + (2 if (u // 16) % 2 else 0)) % 8
                px[v][u] = W1 if band < 3 else W0 if band < 6 else W2
        # breaking foam with a 32-texel wobble, then wet sand fading into dry
        for u in range(SIZE):
            edge = SHORE + round(1.5 * math.sin(u * 2 * math.pi / 32))
            for v in range(SHORE - 3, edge + 1):
                px[v][u] = FOAM if v >= edge - 1 or (u + v) % 3 == 0 else px[v][u]
            for v in range(edge + 1, edge + 12):
                t = (v - edge) / 11
                px[v][u] = WET if (t < 0.45 or ((u * 3 + v * 5) % 8) / 8 > t) else S  # 8-periodic dither
        for v in range(SHORE + 12, SIZE):
            for u in range(SIZE):
                px[v][u] = S
        shell = [(3, 3, PALE), (4, 3, PALE), (3, 4, PALE), (4, 4, FS), (2, 4, FS)]
        flecks = [[(3, 4, SF), (4, 4, SF), (3, 5, SF), (4, 5, SF)], [(2, 3, SF), (3, 3, SF), (2, 4, SF), (3, 4, SF)]]
        footprint = [(2, 2, SF), (2, 3, SS), (2, 4, SS), (5, 5, SF), (5, 6, SS), (5, 7, SS)]
        driftwood = [(1, 4, FS), (2, 4, FS), (3, 4, FS), (4, 5, FS), (5, 5, FS), (6, 5, SS), (2, 5, SS), (3, 5, SS)]
        scatter_decals(px, rng, flecks, 0.05, (SHORE + 16, SIZE))
        scatter_decals(px, rng, [shell, driftwood], 0.012, (SHORE + 16, SIZE))
        # a trail of footprints wandering from the water's edge
        u, v = 404, SHORE + 16
        while v < SIZE - 8:
            if not near_platform(u, v, 20):
                for (x, y, c) in footprint:
                    put(px, u // 8 * 8 + x, v // 8 * 8 + y, c)
            v += 16
            u += 8 if (v // 16) % 3 else -8
        seed = 1987  # fixed: the platform stamp doesn't shift when decals change
        for (cx, cy) in (PLAYER, OPPONENT):
            s = random.Random(seed)
            dish(px, cx, cy, RADIUS, s, F, FL, FS, PALE, FL, dot=SS, shadow=SS, rim_break=0.6)
            for a, off in edge_points(s, 160, -6, 12, 0):
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                put2(px, x0, y0, s.choice((F, SS, SF, FS)) if off > 0 else s.choice((SF, S, PALE)))
            for k in range(5):  # beach morning glory creeping round the rim
                a = s.uniform(0, 2 * math.pi)
                span = s.uniform(0.5, 0.9)
                for t in range(60):
                    aa = a + span * t / 60
                    rad = RADIUS + 2 + 4 * math.sin(t * 0.35 + k)
                    x0, y0 = cx + round(rad * math.cos(aa)), cy + round(rad * math.sin(aa))
                    put(px, x0, y0, V)
                    if t % 7 == 3:
                        for oy in range(-5, 1):
                            put(px, x0 + 1, y0 + oy, L)
                            put(px, x0 + 2, y0 + oy + 1, L if oy > -4 else V)
                    if t % 19 == 11:
                        for oy in range(-3, 4):
                            put(px, x0 - 1, y0 - 4 + oy, MG)
                        put(px, x0 - 1, y0 - 4, PALE)
        px[HAZE[1]][HAZE[0]] = W1

    return pal, W1, draw


def theme_void_deck():
    """HDB void deck: tiled floor, yellow kerb line, drain, driveway; pillars,
    a stone chess table and potted plants."""
    pal = [(0, 0, 0),
           (222, 216, 200),  # 1 floor tile
           (206, 198, 181),  # 2 grout / stain
           (160, 152, 136),  # 3 crack / asphalt speck
           (206, 99, 74),    # 4 mat fill (EPDM rubber)
           (231, 132, 99),   # 5 mat light
           (165, 74, 57),    # 6 mat shade
           (247, 214, 148),  # 7 painted rim
           (239, 173, 123),  # 8 rubber speck
           (189, 181, 165),  # 9 floor shadow
           (66, 132, 66),    # 10 weed dark
           (132, 189, 90),   # 11 weed light
           (239, 206, 82),   # 12 yellow kerb paint
           (105, 107, 115),  # 13 asphalt / drain
           (190, 205, 214),  # 14 puddle  } cycled: shimmer
           (222, 232, 236)]  # 15 puddle  }
    T, ST, CR, F, FL, FS, RIM, SP, SH, W0, W1, YL, AS, P0, P1 = (C(i) for i in range(1, 16))
    GRID = 16  # platform offsets (112, 192) are multiples of 16, so both mats share tiles
    KERB = 120  # driveway for v < KERB

    def draw(px, rng):
        for v in range(SIZE):
            for u in range(SIZE):
                if v < KERB - 12:
                    px[v][u] = CR if (u * 5 + v * 3) % 16 == 0 else AS  # driveway asphalt (16-periodic)
                elif v < KERB - 4:
                    px[v][u] = YL if v >= KERB - 8 else AS                # yellow kerb line
                elif v < KERB + 4:
                    px[v][u] = AS if u % 4 == 0 or v in (KERB - 4, KERB + 3) else CR  # drain grate
                elif near_platform(u, v, -2):
                    continue
                elif u % GRID == 0 or v % GRID == 0:
                    px[v][u] = ST
                else:
                    px[v][u] = T
        stains = [[(3, 3, ST), (4, 3, ST), (3, 4, ST), (4, 4, ST)], [(2, 5, ST), (3, 5, ST), (2, 6, ST), (3, 6, ST)]]
        crack = [(1, 4, CR), (2, 4, CR), (3, 5, CR), (4, 5, CR), (5, 4, CR), (6, 4, CR)]
        scatter_decals(px, rng, stains, 0.02, (KERB + 8, SIZE))
        for (u0, v0) in ((96, 200), (440, 330)):  # puddles that shimmer
            for v in range(v0 - 6, v0 + 7):
                for u in range(u0 - 14, u0 + 15):
                    d = ((u - u0) / 14) ** 2 + ((v - v0) / 6) ** 2
                    if d <= 1 and not near_platform(u, v, 12):
                        put(px, u, v, P1 if (u + v // 2) % 5 == 0 else P0)
        seed = 1987  # fixed: the platform stamp doesn't shift when decals change
        for (cx, cy) in (PLAYER, OPPONENT):
            s = random.Random(seed)
            dish(px, cx, cy, RADIUS, s, F, FL, FS, RIM, RIM, dot=SP, dot2=FS, shadow=SH,
                 shadow_reach=8, rim_break=0.9)
            for a, off in edge_points(s, 110, 0, 16, 2):
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                put2(px, x0, y0, FS if s.random() < 0.35 else SH)
            for k in range(14):  # weeds where the mat meets the floor
                a = 2 * math.pi * k / 14 + s.uniform(-0.2, 0.2)
                bx = cx + round((RADIUS + s.uniform(0, 4)) * math.cos(a))
                by = cy + round((RADIUS + s.uniform(0, 4)) * math.sin(a))
                if s.random() < 0.55:
                    for i in range(s.randint(2, 4)):
                        blade(px, bx + (i - 1) * 2, by, s.randint(5, 11), (W0, W0, W1), s.choice((-0.3, 0, 0.3)))
        px[HAZE[1]][HAZE[0]] = AS

    return pal, AS, draw


def theme_grass():
    """South Tosa Reserve: lalang meadow, a stream, Vanda Miss Joaquim orchids;
    a tembusu tree, a reserve signpost and bird's nest ferns."""
    pal = [(0, 0, 0),
           (214, 234, 165),  # 1 ground
           (197, 222, 148),  # 2 ground fleck
           (165, 205, 123),  # 3 ground shadow / bank
           (115, 189, 90),   # 4 dish fill
           (148, 214, 107),  # 5 dish light
           (82, 156, 74),    # 6 dish shade
           (181, 230, 115),  # 7 rim
           (148, 115, 74),   # 8 earth / stepping stones
           (49, 115, 57),    # 9 blade dark
           (74, 148, 66),    # 10 blade mid
           (132, 197, 90),   # 11 blade light
           (236, 239, 189),  # 12 lalang tip / orchid lip
           (206, 82, 181),   # 13 orchid
           (90, 165, 189),   # 14 stream  } cycled: flowing water
           (140, 206, 222)]  # 15 stream  }
    G, GF, GS, F, FL, FS, RIM, E, B0, B1, B2, TIP, OR, WA, WB = (C(i) for i in range(1, 16))
    STREAM = (40, 92)  # far side, clear of the opponent platform's tallest lalang

    def draw(px, rng):
        for v in range(SIZE):
            for u in range(SIZE):
                px[v][u] = G
        # a stream across the far side: ripples run along u, 16-texel period
        for u in range(SIZE):
            wob = round(1.5 * math.sin(u * 2 * math.pi / 16))
            top, bot = STREAM[0] + wob, STREAM[1] - wob
            for v in range(top - 3, bot + 4):
                if v < top or v > bot:
                    px[v][u] = GS if (u + v) % 2 else B1
                else:
                    px[v][u] = WB if (u + 2 * v) % 16 < 5 else WA
        clump = [(2, 6, B0), (3, 5, B1), (3, 4, B1), (4, 6, B0), (5, 3, B2), (5, 4, B1), (5, 5, B1), (6, 6, B0), (6, 4, TIP)]
        clump2 = [(1, 6, B0), (2, 4, B1), (2, 5, B1), (4, 6, B0), (4, 2, TIP), (4, 3, B2), (4, 4, B1), (4, 5, B1)]
        flecks = [[(3, 4, GF), (4, 4, GF), (3, 5, GF), (4, 5, GF)], [(2, 3, GF), (3, 3, GF), (2, 4, GF), (3, 4, GF)]]
        orchid = [(3, 2, OR), (3, 3, OR), (3, 4, OR), (2, 3, OR), (4, 3, OR), (3, 3, TIP), (3, 5, B1), (3, 6, B1)]
        scatter_decals(px, rng, flecks, 0.05, (STREAM[1] + 6, SIZE))
        scatter_decals(px, rng, [clump, clump2], 0.06, (STREAM[1] + 6, SIZE))
        scatter_decals(px, rng, [orchid], 0.008, (STREAM[1] + 6, SIZE))
        seed = 1987  # fixed: the platform stamp doesn't shift when decals change
        for (cx, cy) in (PLAYER, OPPONENT):
            s = random.Random(seed)
            dish(px, cx, cy, RADIUS, s, F, FL, FS, RIM, FL, dot=B1, shadow=GS)
            for a, off in edge_points(s, 320, -9, 14, 1):
                if off > 8 and s.random() < 0.5:
                    continue
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                close = 1 - min(1.0, abs(off - 1) / 13)
                length = max(2, round((4 + 9 * close) * s.uniform(0.6, 1.1)))
                ramp = (F, B1, FL, RIM) if off < -3 else (B1, B2, RIM, TIP) if off < 3 else (B0, B1, B2, TIP)
                blade(px, x0, y0, length, ramp, s.choice((-0.25, 0, 0, 0.25)))
            for k in range(9):  # tall lalang with pale feathery tips
                a = 2 * math.pi * k / 9 + s.uniform(-0.15, 0.15)
                bx = cx + round((RADIUS + s.uniform(0, 5)) * math.cos(a))
                by = cy + round((RADIUS + s.uniform(0, 5)) * math.sin(a))
                for i in range(s.randint(4, 6)):
                    blade(px, bx + (i - 2) * 2 + s.choice((-1, 0, 1)), by, s.randint(12, 19),
                          (B0, B0, B1, B2, TIP, TIP), s.choice((-0.2, 0, 0.2)))
            for k in range(7):  # Vanda Miss Joaquim on short stems
                a = s.uniform(0, 2 * math.pi)
                rad = RADIUS + s.uniform(2, 10)
                x, y = cx + round(rad * math.cos(a)), cy + round(rad * math.sin(a))
                for t in range(7):
                    put(px, x, y - t, B1)
                for oy in range(-4, 5):
                    put(px, x, y - 7 + oy, OR)
                for ox in (-1, 1):
                    for oy in range(-2, 3):
                        put(px, x + ox, y - 7 + oy, OR)
                put(px, x, y - 7, TIP)
        px[HAZE[1]][HAZE[0]] = G

    return pal, G, draw


THEMES = {
    # theme: (generator, original environment dir whose rows 3-4 are kept, C name)
    "grass": (theme_grass, "tall_grass", "OrchidGrass"),
    "beach": (theme_beach, "sand", "OrchidBeach"),
    "void_deck": (theme_void_deck, "plain", "OrchidVoidDeck"),
}


# ---------------------------------------------------------------------------
# Classic background rendered through the Mode 7 rest camera
# ---------------------------------------------------------------------------

def render_classic(floor, haze_colour):
    """Project the floor to a 512x256 BG3 image. Only the left 240x160 is the
    battle view; the right 256 px repeat the left for the intro slide, which
    keeps the unique tile count under the 512-tile charblock limit."""
    img = [[haze_colour] * 512 for _ in range(256)]
    for y in range(160):
        d = y - HORIZON
        lam = HEIGHT / d
        z = lam * FOCAL
        if z > MAX_DEPTH:
            continue
        v = int(math.floor(REST_V - z)) % SIZE
        for x in range(256):
            u = int(math.floor(REST_U + (x - 120) * lam)) % SIZE
            img[y][x] = img[y][x + 256] = floor[v][u]
    for y in range(160, 256):
        img[y] = list(img[159])
    return img


def tiles_and_map(img):
    """4bpp tiles (with flip dedupe) and a 64x32 BG map using palette row 2."""
    tiles, lookup, entries = [], {}, {}
    for ty in range(32):
        for tx in range(64):
            block = tuple(tuple(img[ty * 8 + y][tx * 8 + x] - 32 if img[ty * 8 + y][tx * 8 + x] else 0
                                for x in range(8)) for y in range(8))
            found = None
            for hf in (0, 1):
                for vf in (0, 1):
                    b = block
                    if hf:
                        b = tuple(tuple(reversed(r)) for r in b)
                    if vf:
                        b = tuple(reversed(b))
                    if b in lookup:
                        found = (lookup[b], hf, vf)
                        break
                if found:
                    break
            if not found:
                lookup[block] = len(tiles)
                tiles.append(block)
                found = (len(tiles) - 1, 0, 0)
            t, hf, vf = found
            entries[(tx, ty)] = (2 << 12) | (vf << 11) | (hf << 10) | t
    if len(tiles) > 512:
        sys.exit(f"classic background needs {len(tiles)} tiles (max 512)")
    data = bytearray()
    for sb in (0, 1):
        for ty in range(32):
            for tx in range(32):
                data += struct.pack("<H", entries[(sb * 32 + tx, ty)])
    return tiles, bytes(data)


def build(theme):
    gen, orig, cname = THEMES[theme]
    out = os.path.join(ROOT, f"orchid_{theme}")
    os.makedirs(out, exist_ok=True)
    row2, haze_colour, draw = gen()
    orig_pal = read_jasc(os.path.join(ROOT, orig, "palette.pal"))
    pal48 = row2 + orig_pal[16:48] + [(0, 0, 0)] * max(0, 32 - len(orig_pal[16:48]))
    full = [(0, 0, 0)] * 32 + pal48 + [(0, 0, 0)] * (256 - 80)

    floor = [[haze_colour] * SIZE for _ in range(SIZE)]
    draw(floor, random.Random(f"orchid-{theme}"))
    bad = {v for r in floor for v in r if not 33 <= v <= 47}
    if bad:
        sys.exit(f"{theme}: floor uses colours outside palette row 2: {sorted(bad)}")
    write_indexed(os.path.join(out, "mode7_floor.png"), SIZE, SIZE, floor, full)
    m7.convert(os.path.join(out, "mode7_floor.png"), out)
    os.remove(os.path.join(out, "mode7_palette.pal"))  # palette.pal serves both

    with open(os.path.join(out, "palette.pal"), "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n48\n")
        for r, g, b in pal48:
            f.write(f"{r} {g} {b}\n")

    tiles, mapdata = tiles_and_map(render_classic(floor, haze_colour))
    rows = (len(tiles) + 15) // 16
    sheet = [[0] * 128 for _ in range(rows * 8)]
    for i, t in enumerate(tiles):
        for y in range(8):
            for x in range(8):
                sheet[(i // 16) * 8 + y][(i % 16) * 8 + x] = t[y][x]
    write_indexed(os.path.join(out, "tiles.png"), 128, rows * 8, sheet, row2)
    with open(os.path.join(out, "map.bin"), "wb") as f:
        f.write(mapdata)

    print(f"{theme}: classic background {len(tiles)}/512 tiles -> {out}")
    return cname, out


def write_header(results):
    lines = ["// Generated by tools/orchid/battle_envs.py - do not edit by hand.",
             "// Included by src/battle_mode7.c.", ""]
    for cname, out in results:
        lines += [
            f"static const u32 sFloorTiles_{cname}[] = INCBIN_U32(\"{out}/mode7_tiles.bin\");",
            f"static const u8 sFloorMap_{cname}[] = INCBIN_U8(\"{out}/mode7_map.bin\");",
            "",
            f"static const struct Mode7Floor sFloor_{cname} =",
            "{",
            f"    .tiles = sFloorTiles_{cname},",
            f"    .map = sFloorMap_{cname},",
            f"    .palette = gBattleEnvironmentPalette_{cname},",
            "};", ""]
    with open(HEADER, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {HEADER}")


if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = list(THEMES)
    if not names or any(n not in THEMES for n in names):
        sys.exit(__doc__ + "\nthemes: " + ", ".join(THEMES))
    # the header always covers every theme, so build them all
    write_header([build(n) for n in THEMES])
