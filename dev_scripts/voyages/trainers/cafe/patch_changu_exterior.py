"""Apply the approved Battle Café exterior patch to data/layouts/ChanguCity/map.bin (mock_cafe.py exterior_spec
'red'). Only cells inside x30-38, y25-31 change (the user hand-edits the rest of this map in Porymap).

    python3 dev_scripts/voyages/trainers/cafe/patch_changu_exterior.py [--check]

Every cell is copied (metatile + collision + elevation) from an existing General+TosaPort layout:
- x31-34 y26-29: Changu House 3 (18,18) 4x4, the red-roof house; door (metatile 021) at (32,29)
- x35-38 y25-29: Bura City market stall (4,7) 4x5: awning, posts, pots, flower boxes, cobbles
- x35-37 y30-31: road (Changu (30,30)/(30,31)); x38 y30-31: road east end (Changu (35,30)/(35,31))
- (30,29): sign post 0x003 (Bura City (9,11))
The script refuses to run if the target box no longer holds the expected plain grass/road (i.e. the user has
edited it since), so it can't clobber hand edits.
"""
import json
import os
import struct
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
LAYOUTS = {l['id']: l for l in json.load(open(os.path.join(ROOT, 'data/layouts/layouts.json')))['layouts'] if 'id' in l}


def load(lid):
    l = LAYOUTS[lid]
    d = open(os.path.join(ROOT, l['blockdata_filepath']), 'rb').read()
    return l, list(struct.unpack('<%dH' % (len(d) // 2), d))


def main():
    cl, c = load('LAYOUT_CHANGU_CITY')
    _bl, b = load('LAYOUT_BURA_CITY')
    W, BW = cl['width'], LAYOUTS['LAYOUT_BURA_CITY']['width']
    orig = list(c)
    road_top, road_bot = orig[30 * W + 30], orig[31 * W + 30]
    end_top, end_bot = orig[30 * W + 35], orig[31 * W + 35]
    # sanity: the box is untouched grass (0x001) + the road end at x35
    for y in range(25, 30):
        for x in range(30, 39):
            assert orig[y * W + x] & 0x3FF == 0x001, ('box already edited', x, y, hex(orig[y * W + x]))
    assert end_top & 0x3FF == 0x20A and end_bot & 0x3FF == 0x21A, 'road end moved'
    new = {}
    for dy in range(4):
        for dx in range(4):
            new[(31 + dx, 26 + dy)] = orig[(18 + dy) * W + 18 + dx]
    for dy in range(5):
        for dx in range(4):
            new[(35 + dx, 25 + dy)] = b[(7 + dy) * BW + 4 + dx]
    for x in range(35, 38):
        new[(x, 30)], new[(x, 31)] = road_top, road_bot
    new[(38, 30)], new[(38, 31)] = end_top, end_bot
    new[(30, 29)] = b[11 * BW + 9]
    for (x, y), v in new.items():
        assert 30 <= x <= 38 and 25 <= y <= 31
        c[y * W + x] = v
    if '--check' in sys.argv:
        print('ok (dry run)', len(new), 'cells')
        return
    open(os.path.join(ROOT, cl['blockdata_filepath']), 'wb').write(struct.pack('<%dH' % len(c), *c))
    print('patched', sum(1 for i in range(len(c)) if c[i] != orig[i]), 'cells')


if __name__ == '__main__':
    main()
