"""Create data/tilesets/secondary/changu_cafe (gTileset_ChanguCafe): a café-only COPY of gTileset_OrchidCentre
with the approved recolour variant A (deep-red walls, charcoal floor). See changu_cafe_tileset.py for the design.

    python3 dev_scripts/voyages/trainers/cafe/install_cafe_tileset.py

- tiles.png, metatile_attributes.bin, palettes 00-15: copied unchanged from orchid_centre,
- palettes/06.pal (floor) and 11.pal (walls; free/black in OrchidCentre): the approved variant-A palettes
  (gTileset_ChanguCafe_A_palettes/, written by mock_cafe.py),
- metatiles.bin: every entry that draws a wall tile (secondary tiles 2, 3, 32-35) with palette 7 now uses 11.
gTileset_OrchidCentre itself is not touched.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'data/tilesets/secondary/orchid_centre')
DST = os.path.join(ROOT, 'data/tilesets/secondary/changu_cafe')
PALS = os.path.join(HERE, 'gTileset_ChanguCafe_A_palettes')
WALL_TILES = {2, 3, 32, 33, 34, 35}
WALL_SLOT = 11


def main():
    os.makedirs(os.path.join(DST, 'palettes'), exist_ok=True)
    for f in ('tiles.png', 'metatile_attributes.bin'):
        shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))
    for i in range(16):
        n = '%02d.pal' % i
        src = os.path.join(PALS, n) if os.path.exists(os.path.join(PALS, n)) else os.path.join(SRC, 'palettes', n)
        shutil.copy2(src, os.path.join(DST, 'palettes', n))
    raw = open(os.path.join(SRC, 'metatiles.bin'), 'rb').read()
    ent = list(struct.unpack('<%dH' % (len(raw) // 2), raw))
    changed = set()
    for i, x in enumerate(ent):
        tile = x & 0x3FF
        if tile >= 512 and tile - 512 in WALL_TILES and x >> 12 == 7:
            ent[i] = (x & 0x0FFF) | (WALL_SLOT << 12)
            changed.add(0x200 + i // 8)
    open(os.path.join(DST, 'metatiles.bin'), 'wb').write(struct.pack('<%dH' % len(ent), *ent))
    print('wall metatiles repointed to pal %d:' % WALL_SLOT, ' '.join('%03X' % m for m in sorted(changed)))


if __name__ == '__main__':
    main()
