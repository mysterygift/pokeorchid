"""
Proposed gTileset_ChanguCafe: a café-only COPY of gTileset_OrchidCentre (pairs with primary gTileset_Building),
with the floor and walls recoloured to charcoal grey + deep red. Nothing is written to data/: voyage_compose
draws it as a "virtual" secondary (OrchidCentre + these changes). Furniture keeps its colours.

What the copy changes (the same tiles.png; every metatile id keeps its meaning):
  * palette 6  (floor, floor shadows, exit-mat surround): indices 2-7 recoloured. In OrchidCentre pal 6 is used
    only by floor-type tiles and the red mat (mat reds 11-13 untouched), so editing it in the copy is safe.
  * palette 11 (free in OrchidCentre: all black, unused): a copy of pal 7 with the wall colours changed.
  * metatiles.bin: every entry that draws a wall tile (secondary tiles 2, 3 = wall face/ceiling band,
    32-35 = dado trim) with pal 7 now uses pal 11. Pal 7 itself is unchanged because the counter, stools,
    windows, menu board and shelf also use it.

Two colour variants for review: "A" = charcoal floor + deep-red walls, "B" = charcoal walls/floor with deep-red
accents (trim band + floor diamonds). The ROM would get one of them as gTileset_ChanguCafe.
"""
import os

BASE = "gTileset_OrchidCentre"
WALL_TILES = {2, 3, 32, 33, 34, 35}      # secondary-relative tile indices of the wall face / band / trim
WALL_SLOT = 11

# OrchidCentre originals, for reference:
#   pal 6: 2 (248,240,216) floor, 3 (240,224,192) diamond, 4 (232,192,160) diamond centre,
#          5 (216,208,192) 6 (208,192,168) 7 (200,168,144) floor shadows (light -> dark)
#   pal 7: 2 (248,248,248) trim band, 3 (248,240,224) wall, 4 (224,216,200) wall shade, 5/6 trim reds,
#          7 pink, 8/9 trim greens, 12 (168,112,72) / 13 (112,72,56) dado rail + ceiling band
VARIANTS = {
    "A": dict(   # charcoal floor, deep-red walls
        floor={2: (72, 72, 80), 3: (88, 88, 96), 4: (104, 104, 112),
               5: (56, 56, 64), 6: (48, 48, 56), 7: (40, 40, 48)},
        wall={3: (136, 32, 40), 4: (112, 24, 32), 13: (64, 32, 32),           # wall face, shade, ceiling band
              2: (232, 216, 192),                                            # trim band: warm cream
              12: (72, 72, 80)},                                             # dado rail: charcoal
    ),
    "B": dict(   # charcoal walls and floor, deep-red accents
        floor={2: (80, 80, 88), 3: (96, 96, 104), 4: (104, 32, 40),          # diamond centres deep red
               5: (64, 64, 72), 6: (56, 56, 64), 7: (48, 48, 56)},
        wall={3: (88, 88, 96), 4: (72, 72, 80), 13: (40, 40, 48),           # charcoal wall, darker band
              2: (144, 32, 40),                                              # trim band deep red
              5: (232, 216, 192), 6: (200, 176, 144),                        # trim dots/lines -> cream
              12: (112, 24, 32)},                                            # dado rail deep red-brown
    ),
}
VARIANT = os.environ.get("CAFE_VARIANT", "A")
NAMES = {"gTileset_ChanguCafe": "A", "gTileset_ChanguCafeB": "B"}


def _pals(variant):
    import voyage_compose as vc
    d = vc.vanilla.tileset_dir(BASE)
    p6 = vc.vanilla.load_jasc(os.path.join(d, "palettes", "06.pal"))
    p7 = vc.vanilla.load_jasc(os.path.join(d, "palettes", "07.pal"))
    v = VARIANTS[variant]
    p6 = [v["floor"].get(i, c) for i, c in enumerate(p6)]
    p11 = [v["wall"].get(i, c) for i, c in enumerate(p7)]
    return {6: p6, WALL_SLOT: p11}


def extras(variant=None):
    return dict(base=BASE, tiles={}, palettes=_pals(variant or VARIANT), metatiles=[])


def patch(scene):
    """Repoint the wall-tile entries from pal 7 to pal 11 in the scene's copy of the secondary metatiles.
    Returns the metatile ids changed."""
    changed = []
    for i, e in enumerate(scene.s.metatiles):
        new = tuple(((x & 0x0FFF) | (WALL_SLOT << 12))
                    if (x & 0x3FF) >= 512 and (x & 0x3FF) - 512 in WALL_TILES and x >> 12 == 7 else x
                    for x in e)
        if new != e:
            scene.s.metatiles[i] = new
            changed.append(0x200 + i)
    scene.cache.clear()
    return changed


def jasc(colours):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in colours)
