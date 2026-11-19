"""Write data/layouts/ChanguCity_Cafe/{map.bin,border.bin} from the approved mock (mock_cafe.py INT_ROWS).

    python3 dev_scripts/voyages/trainers/cafe/build_cafe_layout.py

Every metatile is an existing LAYOUT_POKEMON_CENTER_1F metatile (Building + OrchidCentre, the same ids in
gTileset_ChanguCafe); collision + elevation for each id are copied from the Centre's own map.bin.
Border: the Centre's border.bin.
"""
import os
import shutil
import struct

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
CENTRE = os.path.join(ROOT, 'data/layouts/PokemonCenter_1F')
OUT = os.path.join(ROOT, 'data/layouts/ChanguCity_Cafe')

LEGEND = {
    "w": 0x201, "1": 0x202, "2": 0x203, "p": 0x205, "q": 0x206, "m": 0x207, "s": 0x208, "t": 0x209,
    "F": 0x20A, "a": 0x20B, "b": 0x20C, "_": 0x20E, "P": 0x211, "Q": 0x212, "S": 0x214, "T": 0x215,
    "f": 0x216, "-": 0x217, "E": 0x21E, "U": 0x21F, "g": 0x220, ".": 0x221, "<": 0x222,
    "A": 0x229, "B": 0x22A, "C": 0x22B, ",": 0x22C, "/": 0x22D, "o": 0x22E,
    "x": 0x243, "D": 0x244, "~": 0x234, "M": 0x248, "N": 0x249, "k": 0x247, "K": 0x24A,
}
ROWS = [
    "w12wpq12wmst",    # 0  two windows round the flower painting, menu board + cup shelf
    "Fab_PQab__ST",    # 1  wall trim (fern top at x0)
    "f--------E-U",    # 2  fern / wall foot / counter return 21E, urn 21F
    "g........ABC",    # 3  café counter 229 22A 22B
    ".........o,o",    # 4  counter stools
    ".xDx.xDx.~.~",    # 5  two tables (stool, table, stool)
    ".~~~.~~~....",    # 6  table shadows
    "........xDx.",    # 7  Cynthia's table
    "kxDx....~~~k",    # 8  third table, corner ferns
    "K~~~.MN....K",    # 9  exit mat
]


def main():
    d = open(os.path.join(CENTRE, 'map.bin'), 'rb').read()
    attrs = {}
    for x in struct.unpack('<%dH' % (len(d) // 2), d):
        attrs.setdefault(x & 0x3FF, x & 0xFC00)
    out = []
    for row in ROWS:
        assert len(row) == 12
        for ch in row:
            mid = LEGEND[ch]
            out.append(mid | attrs[mid])
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'map.bin'), 'wb').write(struct.pack('<%dH' % len(out), *out))
    shutil.copy2(os.path.join(CENTRE, 'border.bin'), os.path.join(OUT, 'border.bin'))
    print('wrote 12x10 ChanguCity_Cafe')


if __name__ == '__main__':
    main()
