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


def fill_ellipse(px, cx, cy, rx, ry, c, only=None):
    """Solid ellipse; with only=set, recolour just those pixel values."""
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                if only is None or px[y % SIZE][x % SIZE] in only:
                    put(px, x, y, c)


def fill_rect(px, x0, y0, x1, y1, c, only=None):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if only is None or px[y % SIZE][x % SIZE] in only:
                put(px, x, y, c)


def stroke(px, pts, c, w=2, h=3):
    """Polyline drawn with a w x h pen (taller than wide: v is squashed ~3-4x
    on screen, so thin horizontal strokes would vanish in the distance)."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(max(abs(x1 - x0), abs(y1 - y0))))
        for t in range(n + 1):
            x = round(x0 + (x1 - x0) * t / n)
            y = round(y0 + (y1 - y0) * t / n)
            fill_rect(px, x, y, x + w, y + h, c)


def mark(px, x, y, c, w=2, h=4):
    """Smallest stable floor mark: 2 texels wide, 4 deep."""
    fill_rect(px, x, y, x + w, y + h, c)


def night_of(pal, glow=None, tint=(0.42, 0.50, 0.68), lift=(6, 12, 34), desat=0.3):
    """Night grade for a day palette: darker, desaturated, shifted blue. glow
    overrides individual indices (lamps, monitors, fireflies, glyphs...), which
    lets the same tiles show lit features only at night."""
    out = [(0, 0, 0)]
    for (r, g, b) in pal[1:]:
        lum = 0.3 * r + 0.59 * g + 0.11 * b
        rgb = [v * (1 - desat) + lum * desat for v in (r, g, b)]
        out.append(tuple(min(255, int(v * t + a)) for v, t, a in zip(rgb, tint, lift)))
    for i, col in (glow or {}).items():
        out[i] = col
    return out


def platform_seed():
    """Both platforms are stamped from the same random sequence (and sit at the
    same (x % 8, y % 8)), so their tiles are shared."""
    return random.Random(1987)


def tile_scatter(rng, n, area, keep_clear=40, align=8):
    """n tile-aligned points in area (u0, v0, u1, v1) clear of the platforms."""
    u0, v0, u1, v1 = area
    pts = []
    tries = 0
    while len(pts) < n and tries < n * 50:
        tries += 1
        x = rng.randrange(u0, u1) // align * align
        y = rng.randrange(v0, v1) // align * align
        if not near_platform(x, y, keep_clear):
            pts.append((x, y))
    return pts


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

    night = night_of(pal, {8: (168, 232, 238), 15: (200, 206, 214)})  # foam catches the moonlight
    return pal, W1, draw, night


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

    # void-deck fluorescent tubes keep the tiles readable; puddles mirror them
    night = night_of(pal, {14: (150, 172, 192), 15: (206, 220, 226)}, tint=(0.52, 0.60, 0.70), lift=(10, 16, 30))
    return pal, AS, draw, night


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

    night = night_of(pal, {13: (196, 104, 190), 12: (196, 204, 182)})
    return pal, G, draw, night


# --- Tosa set 2: cave, ruins, office, mall, jungle, lake --------------------
# Each theme also returns a night palette over the same tiles: the night grade
# darkens everything, and "glow" indices that are dull (or hidden) by day light
# up at night (moss, glyphs, monitors, neon, fireflies, lamp reflections).
#
# Tile budget (256 per floor): the two platforms cost ~170 tiles, leaving ~80
# for scenery. So:
#  * background patterns repeat in step with the offset between the platforms
#    (112, -192), so both platforms land on the same pattern and share tiles;
#  * scenery is drawn as stamps at 8-aligned origins on plain ground, so every
#    copy of a stamp reuses the same tiles;
#  * edges are tile-aligned wherever a straight edge looks right.

def blob(px, u0, v0, w, h, c, r=12, only=None):
    """Rounded rectangle (a cheap organic patch: only its corners cost tiles
    when u0, v0, w and h are multiples of 8)."""
    for y in range(v0, v0 + h):
        for x in range(u0, u0 + w):
            dx = max(u0 + r - x, 0, x - (u0 + w - 1 - r))
            dy = max(v0 + r - y, 0, y - (v0 + h - 1 - r))
            if dx * dx + dy * dy <= r * r and (only is None or px[y % SIZE][x % SIZE] in only):
                put(px, x, y, c)


def tile_plain(px, u, v, w, h, colour):
    """True if every 8x8 tile touched by the rect is entirely `colour`."""
    for ty in range(v // 8, (v + h - 1) // 8 + 1):
        for tx in range(u // 8, (u + w - 1) // 8 + 1):
            for y in range(8):
                row = px[(ty * 8 + y) % SIZE]
                for x in range(8):
                    if row[(tx * 8 + x) % SIZE] != colour:
                        return False
    return True


def decals_on_plain(px, rng, decals, density, area, colour, keep_clear=44):
    """Tile-aligned decals, only on tiles of plain `colour` (call after the
    scenery), so they never make one-off tiles by overlapping it."""
    u0, v0, u1, v1 = area
    for ty in range(v0 // 8, v1 // 8):
        for tx in range(u0 // 8, u1 // 8):
            if rng.random() >= density or near_platform(tx * 8 + 4, ty * 8 + 4, keep_clear):
                continue
            if not tile_plain(px, tx * 8, ty * 8, 8, 8, colour):
                continue
            for (x, y, c) in rng.choice(decals):
                put(px, tx * 8 + x, ty * 8 + y, c)


def theme_cave():
    """Tosa limestone cave: rock floor falling away into darkness, a row of
    stalagmites, a still pool, crystals and glow-moss, and a patch of light from
    a hole in the roof (a moonbeam at night, when the moss and crystals glow)."""
    pal = [(0, 0, 0),
           (118, 106, 98),   # 1 rock
           (138, 126, 114),  # 2 rock fleck
           (84, 74, 72),     # 3 crack / shadow
           (150, 138, 124),  # 4 dais fill
           (172, 160, 142),  # 5 dais light
           (126, 114, 104),  # 6 dais shade
           (198, 188, 168),  # 7 dais rim / stalagmite tip
           (64, 56, 58),     # 8 deep shadow / stalagmite shade
           (160, 146, 128),  # 9 stalagmite light
           (44, 82, 108),    # 10 pool deep
           (86, 138, 158),   # 11 pool light
           (98, 120, 78),    # 12 moss (glows at night)
           (176, 164, 134),  # 13 light from the roof (moonbeam at night)
           (148, 112, 186),  # 14 crystal (glows at night)
           (36, 30, 36)]     # 15 darkness
    R, RF, CR, F, FL, FS, RIM, SH, SL, P0, P1, MOSS, SHAFT, CRY, DARK = (C(i) for i in range(1, 16))
    night = night_of(pal, {12: (84, 226, 196), 13: (98, 118, 166), 14: (210, 156, 255)},
                     tint=(0.62, 0.66, 0.80), lift=(2, 6, 18))

    def stalagmite(px, x, base, h, w):
        for t in range(h):
            half = max(1, round(w * (0.2 + 0.8 * t / h)))
            for dx in range(-half, half):
                put(px, x + dx, base - h + t, SL if dx < -half // 3 else SH if dx >= half // 2 else R)
        fill_rect(px, x - 1, base - h, x + 1, base - h + 4, RIM)
        fill_rect(px, x - w, base, x + w + 2, base + 4, SH)

    def crystals(px, u, v):
        fill_rect(px, u, v + 16, u + 24, v + 24, MOSS)
        for (dx, h) in ((4, 12), (10, 20), (16, 14), (20, 8)):
            fill_rect(px, u + dx - 2, v + 20 - h, u + dx + 2, v + 20, CRY)
            fill_rect(px, u + dx - 2, v + 20 - h, u + dx, v + 24 - h, RIM)

    def draw(px, rng):
        fill_rect(px, 0, 0, SIZE, SIZE, R)
        # the back of the cave falls away into darkness (32-texel wobble)
        for u in range(SIZE):
            w = round(3 * math.sin(u * 2 * math.pi / 32))
            for v in range(0, 92 + w):
                px[v][u] = DARK if v < 64 + w else SH if v < 80 else CR
        for u in range(0, SIZE, 64):        # stalagmites along the back
            stalagmite(px, u + 16, 128, 44, 9)
            stalagmite(px, u + 48, 120, 24, 5)
        # light from a hole in the roof, left of the opponent
        fill_ellipse(px, 188, 214, 46, 36, SHAFT)
        for (u, v) in ((224, 136), (152, 296), (328, 320)):
            crystals(px, u, v)
        stalagmite(px, 268, 320, 32, 7)  # one in the open, between the platforms
        for (cx, cy) in (PLAYER, OPPONENT):
            s = platform_seed()
            dish(px, cx, cy, RADIUS, s, F, FL, FS, RIM, FL, shadow=CR, shadow_reach=8)
            for a, off in edge_points(s, 56, 0, 8, 2):
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                mark(px, x0, y0, s.choice((SH, RF, MOSS)), 2, 4)
        flecks = [[(2, 2, RF), (3, 2, RF), (2, 3, RF), (3, 3, RF), (2, 4, RF), (3, 4, RF), (2, 5, RF), (3, 5, RF)],
                  [(4, 1, CR), (5, 1, CR), (4, 2, CR), (5, 2, CR), (4, 3, CR), (5, 3, CR)]]
        decals_on_plain(px, rng, flecks, 0.05, (0, 136, SIZE, SIZE), R)
        px[HAZE[1]][HAZE[0]] = DARK

    return pal, DARK, draw, night


def theme_ruins():
    """Old Temasek temple ruins: long flagstones in running bond, steps up to a
    laterite terrace, a fallen column and drums, moss and roots; the platforms
    are carved daises whose rim and glyphs glow at night."""
    pal = [(0, 0, 0),
           (178, 166, 138),  # 1 flagstone
           (194, 184, 156),  # 2 flagstone alt
           (122, 110, 92),   # 3 grout / crack
           (204, 194, 168),  # 4 dais fill
           (222, 214, 188),  # 5 dais light
           (168, 156, 130),  # 6 dais shade
           (238, 230, 206),  # 7 dais bevel
           (108, 98, 84),    # 8 glyph groove / dais rim (glows at night)
           (74, 114, 62),    # 9 moss dark
           (120, 158, 80),   # 10 moss light
           (112, 82, 60),    # 11 root
           (160, 94, 70),    # 12 laterite
           (198, 128, 94),   # 13 laterite light
           (150, 134, 102),  # 14 dirt
           (246, 238, 226)]  # 15 frangipani
    FLAG, ALT, GR, F, FL, FS, BEV, GLY, M0, M1, ROOT, LAT, LATL, DIRT, FRA = (C(i) for i in range(1, 16))
    night = night_of(pal, {8: (96, 236, 214), 15: (196, 204, 226)})
    TERRACE = 104  # steps end here
    SW, SH_ = 56, 32  # stones: 2 stones x 6 rows = the platform offset

    def stone(u, v):
        row = v // SH_
        uu = u + (SW // 2 if row % 2 else 0)
        return uu // SW, row, uu % SW, v % SH_

    def draw(px, rng):
        for v in range(SIZE):
            for u in range(SIZE):
                col, row, x, y = stone(u, v)
                if x < 2 or y < 3:
                    mossy = (col + row) % 4 == 1 and y < 3
                    px[v][u] = M0 if mossy else GR
                else:
                    px[v][u] = ALT if (col + row) % 4 == 0 else FLAG
        # broken stones (even rows, so they stay tile-aligned): dirt and moss
        for (col, row) in ((2, 6), (8, 8), (7, 12), (1, 10), (5, 14)):
            u0, v0 = col * SW + 2, row * SH_ + 3
            fill_rect(px, u0, v0, u0 + SW - 2, v0 + SH_ - 3, DIRT)
            for (dx, dy, c) in ((6, 5, M1), (14, 13, M0), (30, 9, M1), (40, 17, M0), (22, 21, M1)):
                mark(px, u0 + dx, v0 + dy, c, 4, 4)
        # steps up to a laterite terrace with pillar bases
        for v in range(TERRACE):
            for u in range(SIZE):
                if v < 48:
                    px[v][u] = GR if v % 24 < 3 or u % 64 < 2 else LAT
                else:
                    step = (v - 48) % 14
                    px[v][u] = GR if step < 4 else ALT if step < 9 else FLAG
        for u in range(0, SIZE, 64):
            fill_rect(px, u + 16, 8, u + 48, 40, LATL)
            fill_rect(px, u + 16, 32, u + 48, 40, LAT)
            fill_ellipse(px, u + 32, 22, 11, 9, GR)
            fill_ellipse(px, u + 31, 21, 8, 6, LATL)
        # a fallen column left of the opponent, and loose drums
        u0, u1, v0 = 104, 232, 232
        fill_rect(px, u0, v0 + 16, u1 + 8, v0 + 24, GR)
        fill_rect(px, u0, v0, u1, v0 + 8, LATL)
        fill_rect(px, u0, v0 + 8, u1, v0 + 16, LAT)
        for x in range(u0 + 32, u1, 32):
            fill_rect(px, x, v0, x + 2, v0 + 16, GR)
        fill_rect(px, u1, v0, u1 + 8, v0 + 16, LATL)
        fill_rect(px, u1 + 2, v0 + 4, u1 + 6, v0 + 12, LAT)
        for (u, v) in ((136, 160),):
            fill_ellipse(px, u + 16, v + 18, 16, 12, GR)
            fill_ellipse(px, u + 16, v + 14, 15, 11, LATL)
            fill_ellipse(px, u + 16, v + 14, 9, 6, LAT)
        for (cx, cy) in (PLAYER, OPPONENT):
            s = platform_seed()
            dish(px, cx, cy, RADIUS, s, F, FL, FS, GLY, BEV, shadow=GR, shadow_reach=6)
            for k in range(8):  # glyphs just inside the rim
                a = 2 * math.pi * k / 8 + math.pi / 8
                gx, gy = cx + round(52 * math.cos(a)), cy + round(52 * math.sin(a))
                fill_rect(px, gx - 3, gy - 6, gx + 3, gy - 3, GLY)
                fill_rect(px, gx - 1, gy - 6, gx + 1, gy + 6, GLY)
                fill_rect(px, gx - 3, gy + 3, gx + 3, gy + 6, GLY)
            fill_ellipse(px, cx, cy, 8, 8, GLY)
            fill_ellipse(px, cx, cy, 4, 4, FL)
            for a, off in edge_points(s, 90, 0, 8, 2):
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                mark(px, x0, y0, s.choice((M0, M1, M0, DIRT)), 2, 4)
            for k in range(3):  # fallen frangipani
                a = s.uniform(0, 2 * math.pi)
                x0, y0 = cx + round((RADIUS + 3) * math.cos(a)), cy + round((RADIUS + 3) * math.sin(a))
                for (dx, dy) in ((-3, 0), (3, 0), (0, -5), (0, 5)):
                    fill_rect(px, x0 + dx - 1, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2, FRA)
                fill_rect(px, x0 - 1, y0 - 2, x0 + 1, y0 + 2, LATL)
        px[HAZE[1]][HAZE[0]] = LAT

    return pal, LAT, draw, night


def theme_office():
    """CBD office floor: quarter-turned carpet tiles, banks of desks with
    monitors, window light slanting across the carpet, potted plants and a
    walkway; the platforms are round meeting rugs. At night the monitors glow
    and the desk lamps pool warm light."""
    pal = [(0, 0, 0),
           (126, 136, 154),  # 1 carpet A
           (114, 124, 144),  # 2 carpet B
           (86, 94, 114),    # 3 seam / shadow
           (72, 122, 132),   # 4 rug fill
           (98, 152, 158),   # 5 rug light
           (54, 98, 110),    # 6 rug shade
           (214, 218, 210),  # 7 rug rim / white
           (226, 222, 208),  # 8 desk top
           (58, 62, 76),     # 9 desk edge / chair
           (150, 178, 206),  # 10 monitor (glows at night)
           (172, 182, 196),  # 11 window light (city glow at night)
           (86, 152, 92),    # 12 plant
           (178, 118, 80),   # 13 pot
           (150, 158, 172),  # 14 walkway vinyl
           (120, 130, 150)]  # 15 desk-lamp pool: carpet-ish by day, warm at night
    CA, CB, SEAM, F, FL, FS, RIM, DESK, DARK, MON, SUN, PLANT, POT, WALK, LAMP = (C(i) for i in range(1, 16))
    night = night_of(pal, {10: (120, 214, 255), 11: (70, 80, 122), 15: (150, 136, 108)})
    WALK_V = (296, 320)

    def desk_bank(px, u, v):
        """Desks face to face (48 x 40 texels at an 8-aligned origin)."""
        fill_rect(px, u - 8, v - 16, u + 56, v + 56, LAMP)
        fill_rect(px, u, v, u + 48, v + 16, DESK)
        fill_rect(px, u, v + 24, u + 48, v + 40, DESK)
        fill_rect(px, u, v + 16, u + 48, v + 24, DARK)
        for k in range(2):
            fill_rect(px, u + 6 + k * 24, v + 10, u + 20 + k * 24, v + 16, MON)
            fill_rect(px, u + 6 + k * 24, v + 24, u + 20 + k * 24, v + 30, MON)
            fill_rect(px, u + 8 + k * 24, v - 12, u + 18 + k * 24, v - 4, DARK)
            fill_rect(px, u + 8 + k * 24, v + 44, u + 18 + k * 24, v + 52, DARK)

    def plant(px, u, v):
        fill_rect(px, u + 4, v + 16, u + 20, v + 24, SEAM)
        fill_rect(px, u + 4, v + 8, u + 20, v + 20, POT)
        for (dx, dy) in ((0, 4), (8, 0), (16, 4), (4, 10), (12, 10)):
            fill_rect(px, u + dx, v + dy, u + dx + 8, v + dy + 6, PLANT)

    def draw(px, rng):
        for v in range(SIZE):
            for u in range(SIZE):
                px[v][u] = CA if ((u // 16) + (v // 64)) % 2 else CB
        # window light slanting across the carpet, left of the opponent
        for v in range(136, 288):
            for u in range(16, 232):
                if ((u - (v - 136) // 2) % 64) < 24:
                    px[v][u] = SUN
        # walkway between the platforms
        fill_rect(px, 0, WALK_V[0], SIZE, WALK_V[1], WALK)
        fill_rect(px, 0, WALK_V[0], SIZE, WALK_V[0] + 3, DARK)
        fill_rect(px, 0, WALK_V[1] - 3, SIZE, WALK_V[1], DARK)
        for u in range(0, SIZE, 32):
            fill_rect(px, u, WALK_V[0] + 10, u + 16, WALK_V[0] + 14, RIM)
        for u in range(0, SIZE, 64):  # desks along the back
            desk_bank(px, u + 8, 48)
        desk_bank(px, 400, 184)
        for (u, v) in ((232, 128), (440, 352), (128, 392), (56, 112)):
            plant(px, u, v)
        for (cx, cy) in (PLAYER, OPPONENT):
            s = platform_seed()
            dish(px, cx, cy, RADIUS, s, F, FL, FS, RIM, FS, shadow=SEAM, shadow_reach=4)
            for k in range(36):  # fringe
                a = 2 * math.pi * k / 36
                mark(px, cx + round((RADIUS + 1) * math.cos(a)), cy + round((RADIUS + 1) * math.sin(a)), RIM, 2, 4)
        px[HAZE[1]][HAZE[0]] = CB

    return pal, CB, draw, night


def theme_mall():
    """Mall atrium: large marble tiles, shopfronts along the back, a granite band
    with brass studs, planters and ceiling spotlights; the platforms are
    rose-marble compass medallions. At night the shop signs are neon and the
    spotlights pool on a dark floor."""
    pal = [(0, 0, 0),
           (228, 220, 206),  # 1 marble
           (212, 202, 190),  # 2 marble alt
           (176, 166, 156),  # 3 grout
           (186, 96, 96),    # 4 medallion rose
           (216, 132, 120),  # 5 medallion light
           (150, 72, 76),    # 6 medallion shade
           (226, 186, 94),   # 7 brass
           (74, 74, 86),     # 8 granite
           (214, 78, 92),    # 9 sign A (neon pink at night)
           (64, 166, 178),   # 10 sign B (neon cyan at night)
           (172, 200, 214),  # 11 shop glass / floor
           (90, 152, 92),    # 12 planter leaf
           (58, 102, 70),    # 13 planter dark
           (240, 234, 222),  # 14 spotlight pool
           (255, 255, 248)]  # 15 shine
    M, MA, GR, F, FL, FS, BR, GRAN, SA, SB, GLASS, LEAF, LEAFD, SPOT, SHINE = (C(i) for i in range(1, 16))
    night = night_of(pal, {9: (255, 96, 178), 10: (86, 240, 255), 7: (186, 154, 92), 11: (150, 138, 112),
                           14: (172, 158, 122), 15: (220, 216, 204)})
    SHOPS = 112
    BAND = (296, 320)
    TW, TH = 56, 48  # marble tiles: 2 x 4 tiles = the platform offset

    def planter(px, u, v):
        """A round granite planter with a palm-like shrub (drawn tall)."""
        fill_ellipse(px, u + 18, v + 30, 16, 6, GR)
        fill_ellipse(px, u + 16, v + 26, 15, 6, GRAN)
        fill_ellipse(px, u + 16, v + 25, 11, 4, LEAFD)
        for k in range(7):
            ang = math.pi * (0.1 + 0.8 * k / 6)
            tip = (u + 16 + round(16 * math.cos(ang)), v + 22 - round(24 * math.sin(ang)))
            stroke(px, [(u + 16, v + 22), tip], LEAF if k % 2 else LEAFD, 3, 4)

    def draw(px, rng):
        for v in range(SIZE):
            for u in range(SIZE):
                if u % TW < 2 or v % TH < 3:
                    px[v][u] = GR
                else:
                    px[v][u] = MA if ((u // TW) + (v // TH)) % 2 else M
        # spotlight pools, each inside one plain marble tile
        for (i, j) in ((1, 4), (2, 3), (8, 4), (8, 7), (0, 6), (5, 9), (3, 2)):
            if (i + j) % 2 == 0:
                blob(px, i * TW + 8, j * TH + 8, 40, 32, SPOT, r=12)
        # shopfronts along the back
        for u0 in range(0, SIZE, 64):
            sign = SA if (u0 // 64) % 2 else SB
            fill_rect(px, u0, 0, u0 + 64, 32, GRAN)
            fill_rect(px, u0 + 8, 16, u0 + 56, 32, sign)
            fill_rect(px, u0, 32, u0 + 64, SHOPS - 16, GLASS)
            for k in range(3):
                fill_rect(px, u0 + 8 + k * 16, 40, u0 + 16 + k * 16, 72, sign if k == 1 else MA)
            fill_rect(px, u0, SHOPS - 16, u0 + 64, SHOPS - 8, GRAN)
            fill_rect(px, u0 + 24, SHOPS - 8, u0 + 48, SHOPS, GRAN)
            fill_rect(px, u0, 0, u0 + 8, SHOPS - 8, GRAN)
        # granite band with brass between the platforms
        fill_rect(px, 0, BAND[0], SIZE, BAND[1], GRAN)
        fill_rect(px, 0, BAND[0] + 8, SIZE, BAND[0] + 12, BR)
        for u in range(0, SIZE, 32):
            fill_rect(px, u + 12, BAND[0] + 4, u + 16, BAND[1] - 4, BR)
        for (i, j) in ((2, 4), (5, 7)):
            planter(px, i * TW + 12, j * TH + 12)
        for (i, j) in ((0, 3), (3, 7), (7, 3), (1, 8), (6, 9)):  # shine
            fill_rect(px, i * TW + 16, j * TH + 8, i * TW + 18, j * TH + 16, SHINE)
            fill_rect(px, i * TW + 18, j * TH + 12, i * TW + 20, j * TH + 20, SHINE)
        for (cx, cy) in (PLAYER, OPPONENT):
            s = platform_seed()
            dish(px, cx, cy, RADIUS, s, F, FL, FS, BR, BR, shadow=GR, shadow_reach=4)
            for y in range(cy - RADIUS, cy + RADIUS + 1):  # inlaid ring of 8 segments
                for x in range(cx - RADIUS, cx + RADIUS + 1):
                    d = math.hypot(x - cx, y - cy)
                    if 30 <= d < 46:
                        seg = int((math.atan2(y - cy, x - cx) + math.pi) / (math.pi / 4)) % 2
                        put(px, x, y, BR if d >= 43 else (M if seg else FS))
            fill_ellipse(px, cx, cy, 7, 7, BR)
            fill_ellipse(px, cx, cy, 3, 3, FL)
        px[HAZE[1]][HAZE[0]] = GRAN

    return pal, GRAN, draw, night


def theme_jungle():
    """Bukit Tosa rainforest: leaf litter on dark soil, a raised boardwalk at the
    back, a tree's buttress roots, ferns and dappled sun; the platforms are mossy
    clearings. At night the dapples turn to moonlight and fireflies come out."""
    pal = [(0, 0, 0),
           (84, 70, 50),     # 1 soil
           (128, 102, 62),   # 2 leaf litter
           (58, 48, 36),     # 3 shadow
           (86, 124, 58),    # 4 moss fill
           (114, 154, 70),   # 5 moss light
           (64, 98, 48),     # 6 moss shade
           (150, 184, 86),   # 7 moss rim
           (108, 78, 54),    # 8 root
           (146, 110, 72),   # 9 root light
           (36, 84, 50),     # 10 fern dark
           (60, 126, 64),    # 11 fern mid
           (100, 168, 80),   # 12 fern light
           (156, 122, 82),   # 13 boardwalk plank
           (84, 70, 50),     # 14 firefly: soil by day, glowing at night
           (184, 174, 100)]  # 15 sun dapple (moonlight at night)
    S, LIT, SH, F, FL, FS, RIM, RT, RTL, F0, F1, F2, PLANK, FLY, SUN = (C(i) for i in range(1, 16))
    night = night_of(pal, {14: (232, 250, 120), 15: (62, 84, 104)}, tint=(0.40, 0.50, 0.66))
    WALK = (56, 96)

    def fern(px, x, y):
        """A fern stamp, fronds fanning up and out (drawn ~3x tall)."""
        for k in range(5):
            ang = math.pi * (0.15 + 0.7 * k / 4)
            tip = (x + round(10 * math.cos(ang)), y - round(26 * math.sin(ang)))
            stroke(px, [(x, y), tip], F0, 2, 3)
            for t in range(2, 7):
                bx = x + round(t / 6 * 10 * math.cos(ang))
                by = y - round(t / 6 * 26 * math.sin(ang))
                mark(px, bx - 3, by, F1, 2, 4)
                mark(px, bx + 2, by - 2, F2 if t % 2 else F1, 2, 4)

    def draw(px, rng):
        fill_rect(px, 0, 0, SIZE, SIZE, S)
        leaves = [[(2, 2, LIT), (3, 2, LIT), (2, 3, LIT), (3, 3, LIT), (4, 3, LIT), (3, 4, LIT), (4, 4, LIT), (4, 5, LIT), (5, 5, LIT)],
                  [(2, 1, FLY), (3, 1, FLY), (2, 2, FLY), (3, 2, FLY), (2, 3, FLY), (3, 3, FLY)]]
        for (u, v) in ((200, 264), (400, 136), (424, 400), (32, 168), (336, 368)):  # dappled sun
            blob(px, u, v, 24, 32, SUN, r=10, only={S})
            blob(px, u + 16, v + 16, 24, 24, SUN, r=10, only={S})
        # boardwalk at the back: planks across the walk, rails, posts
        fill_rect(px, 0, WALK[0] - 8, SIZE, WALK[1] + 8, SH)
        for u in range(SIZE):
            for v in range(WALK[0], WALK[1]):
                px[v][u] = SH if u % 8 < 2 else PLANK
        fill_rect(px, 0, WALK[0], SIZE, WALK[0] + 4, RT)
        fill_rect(px, 0, WALK[1] - 4, SIZE, WALK[1], RT)
        for u in range(0, SIZE, 64):
            fill_rect(px, u, WALK[0] - 8, u + 8, WALK[0] + 8, RTL)
            fill_rect(px, u, WALK[1] - 8, u + 8, WALK[1] + 8, RTL)
        for u in range(16, SIZE, 32):  # ferns spilling over the edges
            fern(px, u + 4, WALK[1] + 32)
        # a tree's buttress roots, left of the opponent
        tx, ty = 152, 200
        for (dx, dy) in ((-1, 0), (1, 0), (-1, 1), (1, 1)):  # straight fins tile cheaply
            n = 40 if dy == 0 else 30
            pts = [(tx, ty), (tx + dx * n, ty + dy * n)]
            stroke(px, pts, RT, 6, 6)
            stroke(px, pts, RTL, 2, 3)
        fill_ellipse(px, tx, ty, 18, 22, SH)
        fill_ellipse(px, tx - 2, ty - 2, 14, 18, RT)
        for (u, v) in ((320, 320), (448, 208), (128, 288), (88, 424)):
            fern(px, u + 4, v + 28)
        for (cx, cy) in (PLAYER, OPPONENT):
            s = platform_seed()
            dish(px, cx, cy, RADIUS, s, F, FL, FS, RIM, FL, shadow=SH, shadow_reach=8)
            for a, off in edge_points(s, 80, -2, 8, 2):
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                blade(px, x0, y0, s.randint(4, 8), (F0, F1, F2, RIM), s.choice((-0.25, 0, 0.25)))
            for k in range(8):
                a = s.uniform(0, 2 * math.pi)
                mark(px, cx + round((RADIUS + 4) * math.cos(a)), cy + round((RADIUS + 4) * math.sin(a)), FLY, 2, 4)
        decals_on_plain(px, rng, leaves, 0.22, (0, WALK[1] + 32, SIZE, SIZE), S)
        px[HAZE[1]][HAZE[0]] = SH

    return pal, SH, draw, night


def theme_lake():
    """Tosa Reservoir: open water with ripples and glitter, a reed-lined far bank
    with lamp posts, lily pads and lotus; the platforms are pale shallows. At
    night the glitter becomes a moon path and the lamps reflect in the water."""
    pal = [(0, 0, 0),
           (72, 142, 170),   # 1 water
           (112, 178, 202),  # 2 ripple light
           (54, 112, 146),   # 3 ripple dark
           (124, 190, 194),  # 4 shallows
           (158, 214, 208),  # 5 shallows light
           (94, 160, 176),   # 6 shallows shade
           (228, 244, 240),  # 7 foam / lamp
           (52, 112, 64),    # 8 lily dark
           (98, 166, 84),    # 9 lily light
           (236, 150, 190),  # 10 lotus
           (60, 96, 58),     # 11 reed dark / bank shade
           (128, 172, 92),   # 12 reed light
           (152, 190, 112),  # 13 bank grass
           (226, 242, 246),  # 14 glitter (moon path at night)
           (72, 142, 170)]   # 15 lamp reflection: water by day, warm at night
    W, RL, RD, F, FL, FS, FOAM, L0, L1, LOT, RE0, RE1, BANK, GLIT, LAMP = (C(i) for i in range(1, 16))
    night = night_of(pal, {14: (236, 230, 180), 15: (232, 180, 96), 7: (204, 204, 184)},
                     tint=(0.36, 0.46, 0.66), lift=(4, 10, 30))
    SHORE = 96

    def lily_clump(px, u, v):
        for (dx, dy, r) in ((4, 8, 7), (20, 4, 6), (14, 20, 8), (30, 18, 5)):
            fill_ellipse(px, u + dx + 1, v + dy + 2, r, r * 0.8, L0)
            fill_ellipse(px, u + dx, v + dy, r - 1, r * 0.8 - 1, L1)
            fill_rect(px, u + dx, v + dy - r // 2, u + dx + 2, v + dy + 1, W)
        fill_ellipse(px, u + 14, v + 12, 4, 6, LOT)
        fill_rect(px, u + 13, v + 10, u + 15, v + 14, FOAM)

    def draw(px, rng):
        fill_rect(px, 0, 0, SIZE, SIZE, W)
        # far bank with reeds (32-texel period) and lamp posts
        for u in range(SIZE):
            edge = SHORE + round(3 * math.sin(u * 2 * math.pi / 32))
            for v in range(0, edge):
                px[v][u] = BANK if v < edge - 16 else RE0
        for u in range(0, SIZE, 4):
            h = (14, 20, 16, 24, 12, 18, 22, 16)[(u // 4) % 8]
            base = SHORE + round(3 * math.sin(u * 2 * math.pi / 32)) + 2
            fill_rect(px, u, base - h, u + 2, base, RE1 if (u // 4) % 3 else RE0)
        for u in range(32, SIZE, 128):
            fill_rect(px, u, 24, u + 4, 64, RE0)
            fill_rect(px, u - 4, 16, u + 8, 24, FOAM)
            for k, v in enumerate(range(SHORE + 8, SHORE + 104, 8)):
                w = max(2, 8 - k // 2 * 2)
                fill_rect(px, u + 2 - w // 2, v, u + 2 + w // 2, v + 4, LAMP)
        # glitter / moon path down the middle, plus a few glints
        for v in range(SHORE + 8, SIZE, 8):
            for k in range(2):
                u = 256 + rng.randrange(-32, 32, 8)
                if not near_platform(u + 4, v, 6):
                    fill_rect(px, u, v + 2, u + 8, v + 6, GLIT)
        for (u, v) in tile_scatter(rng, 16, (0, SHORE + 8, SIZE, SIZE), keep_clear=20):
            fill_rect(px, u + 2, v + 2, u + 6, v + 6, GLIT)
        for (u, v) in ((136, 168), (96, 280), (424, 352), (440, 248), (336, 120), (168, 448)):
            lily_clump(px, u, v)
        # ripples: 16-texel dashes on an 8-aligned grid, on open water only
        for v0 in range(SHORE + 8, SIZE, 16):
            for u0 in range(0, SIZE, 32):
                du = 16 if (v0 // 16) % 2 else 0
                c = RL if (u0 // 32 + v0 // 16) % 3 else RD
                if tile_plain(px, u0 + du, v0, 16, 8, W) and not near_platform(u0 + du + 8, v0 + 2, 24):
                    fill_rect(px, u0 + du, v0 + 2, u0 + du + 16, v0 + 6, c)
        for (cx, cy) in (PLAYER, OPPONENT):
            s = platform_seed()
            dish(px, cx, cy, RADIUS, s, F, FL, FS, FOAM, FL, shadow=RD, shadow_reach=8)
            for a, off in edge_points(s, 40, 0, 6, 3):
                x0, y0 = cx + round((RADIUS + off) * math.cos(a)), cy + round((RADIUS + off) * math.sin(a))
                mark(px, x0, y0, RL, 4, 4)
            for k in range(2):
                a = s.uniform(0, 2 * math.pi)
                x0, y0 = cx + round((RADIUS + 2) * math.cos(a)), cy + round((RADIUS + 2) * math.sin(a))
                fill_ellipse(px, x0 + 1, y0 + 2, 6, 5, L0)
                fill_ellipse(px, x0, y0, 5, 4, L1)
            a = s.uniform(0, 2 * math.pi)
            lx, ly = cx + round((RADIUS + 4) * math.cos(a)), cy + round((RADIUS + 4) * math.sin(a))
            fill_ellipse(px, lx, ly - 4, 4, 6, LOT)
            fill_rect(px, lx - 1, ly - 6, lx + 1, ly - 2, FOAM)
        px[HAZE[1]][HAZE[0]] = BANK

    return pal, BANK, draw, night

THEMES = {
    # theme: (generator, original environment dir whose rows 3-4 are kept, C name)
    "grass": (theme_grass, "tall_grass", "OrchidGrass"),
    "beach": (theme_beach, "sand", "OrchidBeach"),
    "void_deck": (theme_void_deck, "plain", "OrchidVoidDeck"),
    "cave": (theme_cave, "cave", "OrchidCave"),
    "ruins": (theme_ruins, "rock", "OrchidRuins"),
    "office": (theme_office, "building", "OrchidOffice"),
    "mall": (theme_mall, "building", "OrchidMall"),
    "jungle": (theme_jungle, "long_grass", "OrchidJungle"),
    "lake": (theme_lake, "pond_water", "OrchidLake"),
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
    row2, haze_colour, draw, night = gen()
    orig_pal = read_jasc(os.path.join(ROOT, orig, "palette.pal"))
    rows34 = orig_pal[16:48] + [(0, 0, 0)] * max(0, 32 - len(orig_pal[16:48]))
    pal48 = row2 + rows34
    full = [(0, 0, 0)] * 32 + pal48 + [(0, 0, 0)] * (256 - 80)

    floor = [[haze_colour] * SIZE for _ in range(SIZE)]
    draw(floor, random.Random(f"orchid-{theme}"))
    bad = {v for r in floor for v in r if not 33 <= v <= 47}
    if bad:
        sys.exit(f"{theme}: floor uses colours outside palette row 2: {sorted(bad)}")
    write_indexed(os.path.join(out, "mode7_floor.png"), SIZE, SIZE, floor, full)
    m7.convert(os.path.join(out, "mode7_floor.png"), out)
    os.remove(os.path.join(out, "mode7_palette.pal"))  # palette.pal serves both

    for name, colours in (("palette.pal", pal48), ("palette_night.pal", night + rows34)):
        with open(os.path.join(out, name), "w", newline="\r\n") as f:
            f.write("JASC-PAL\n0100\n48\n")
            for r, g, b in colours:
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
            f"    .paletteNight = gBattleEnvironmentPaletteNight_{cname},",
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
