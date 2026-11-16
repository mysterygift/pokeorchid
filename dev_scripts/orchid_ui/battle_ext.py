"""
Battle-only helpers for the Orchid battle UI mockups (mock_battle.py / anim_battle.py).

* scene(): the vanilla battle environment (BG3 in vanilla, the Mode 7 floor on the
  engine branch) + the two battlers at the vanilla singles coordinates.
* Layout constants for the new UI, all inside the vanilla UI zones:
    - opponent healthbox  OBJ  top-left   (vanilla 13..112 x 16..43)
    - player healthbox    OBJ  right      (vanilla 127..230 x 74..111)
    - bottom tray         BG0  y 112..159 (vanilla textbox area, 30x6 tiles)
"""
import os
import struct
from PIL import Image
from kit import *
import kit_ext as K

W, H = 240, 160
G = K.G

# ------------------------------------------------------------------ vanilla coordinates
# sBattlerCoords (battle_anim_mons.c) + species pic Y offsets (GBA-style gfx).
PLAYER_C = (72, 80)
ENEMY_C = (176, 40)
SPECIES = {
    "grovyle": dict(front_y=4, back_y=8),
    "treecko": dict(front_y=13, back_y=11),
    "zigzagoon": dict(front_y=15, back_y=11),
    "poochyena": dict(front_y=12, back_y=9),
}
TRAY_Y = 112                    # textbox area = tile rows 14..19


def _tilemap(path):
    d = open(path, "rb").read()
    return struct.unpack("<%dH" % (len(d) // 2), d)


_ENV_CACHE = {}


def environment(name="tall_grass"):
    if name not in _ENV_CACHE:
        _ENV_CACHE[name] = _environment(name)
    return _ENV_CACHE[name].copy()


def _environment(name="tall_grass"):
    """Composite graphics/battle_environment/<name>/{tiles.png,map.bin,palette.pal} -> 240x160 RGBA.
    64x32 map (two 32x32 screens); the visible window starts at 0,0."""
    d = G("battle_environment", name)
    tiles = Image.open(os.path.join(d, "tiles.png"))
    tp = tiles.load()
    tw = tiles.size[0] // 8
    pal = [snap(c) for c in K.load_jasc(os.path.join(d, "palette.pal"))]   # BG rows 2..4
    tm = _tilemap(os.path.join(d, "map.bin"))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    op = out.load()
    for ty in range(H // 8):
        for tx in range(W // 8):
            e = tm[ty * 32 + tx]                # screen 0
            idx, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            sx, sy = (idx % tw) * 8, (idx // tw) * 8
            for y in range(8):
                for x in range(8):
                    v = tp[sx + (7 - x if hf else x), sy + (7 - y if vf else y)]
                    row = pn - 2
                    if v == 0 or row < 0:
                        c = (255, 0, 255)           # would show the backdrop colour (debug magenta)
                    else:
                        c = pal[row * 16 + v]
                    op[tx * 8 + x, ty * 8 + y] = c + (255,)
    return out


def scene(player="grovyle", enemy="zigzagoon", env="tall_grass", show_player=True, show_enemy=True,
          enemy_dx=0, player_dx=0, enemy_flash=False):
    out = environment(env)
    if show_enemy:
        spr = K.mon_front(enemy)
        if enemy_flash:
            spr = Image.new("RGBA", spr.size, (0, 0, 0, 0))
        K.place(out, spr, ENEMY_C[0] + enemy_dx, ENEMY_C[1] + SPECIES[enemy]["front_y"])
    if show_player:
        K.place(out, K.mon_back(player), PLAYER_C[0] + player_dx, PLAYER_C[1] + SPECIES[player]["back_y"])
    return out


# ------------------------------------------------------------------ big rounded shapes
def round_mask(w, h, r):
    """Filled rounded-rect mask with an arbitrary corner radius (pixel-circle corners)."""
    m = set()
    for y in range(h):
        for x in range(w):
            cx = min(max(x + 0.5, r), w - r)
            cy = min(max(y + 0.5, r), h - r)
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= r * r:
                m.add((x, y))
    return m


def mask_box(cv, x0, y0, mask, face, outline=INK, light=WHITE, shade=PANEL_SHADE):
    """Gen 3 shading for any filled mask: 1px ink outline, light inner edge top/left, shade bottom/right."""
    edge = {p for p in mask if any((p[0] + dx, p[1] + dy) not in mask
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    for (x, y) in mask:
        c = face
        if (x, y) in edge:
            c = outline
        elif any((x + dx, y + dy) in edge for dx, dy in ((0, -1), (-1, 0))):
            c = light
        elif any((x + dx, y + dy) in edge for dx, dy in ((0, 1), (1, 0))):
            c = shade
        cv.set(x0 + x, y0 + y, c)
    return edge


def big_round_box(cv, x0, y0, w, h, r, face, outline=INK, light=WHITE, shade=PANEL_SHADE):
    return mask_box(cv, x0, y0, round_mask(w, h, r), face, outline, light, shade)
