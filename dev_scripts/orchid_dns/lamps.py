#!/usr/bin/env python3
"""Night lamps: the little bulb under each Tosa Port jetty streetlamp turns yellow at night.

The bulbs use TosaPort palette 6 colours that walls also use, so they can't be lit there. The lamp-head
tiles (top layer, used only by the two streetlamps) are moved to palette 12 instead: their pixels are
remapped to palette 12's matching greys, and the bulb pixels go to palette 12 slots 12 / 15, which no
placed metatile uses. Those two slots get the bulb's own day colours and are listed in 12.pla, so by
day the lamps look as before and at night the bulbs blend toward colour 0 (lamp yellow).

Also strips any OBJ_EVENT_GFX_LIGHT_SPRITE glows an earlier version placed (the user asked for the
bulb, not a glow).  Idempotent.

    lamps.py
"""
import json
import os
import struct

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TS = os.path.join(ROOT, "data", "tilesets", "secondary", "tosa_port")
LAMP = (248, 200, 40)
LIGHT_PAL = 12
# lamp-head metatile -> entry slots drawing the head (top layer); all tiles here are used only by lamps
HEADS = {0x3C4: (4, 6), 0x3C6: (5, 7), 0x3C9: (4, 6), 0x3BE: (5,)}
# palette 6 index -> palette 12 index (nearest greys); bulb colours go to the two spare light slots
REMAP = {1: 15, 9: 12, 2: 9, 3: 8, 7: 1, 8: 2, 13: 7, 4: 8, 5: 7, 6: 11, 11: 9, 12: 7}
BULB = {15: (255, 255, 255), 12: (205, 205, 148)}
MAPS_WITH_OLD_GLOWS = ["TosaPort"]


def load_pal(p):
    v = open(p).read().split()
    vals = list(map(int, v[3:3 + 48]))
    return [tuple(vals[j * 3:j * 3 + 3]) for j in range(16)]


def main():
    meta_p = os.path.join(TS, "metatiles.bin")
    meta = [list(struct.unpack_from("<8H", open(meta_p, "rb").read(), i))
            for i in range(0, os.path.getsize(meta_p), 16)]
    img = Image.open(os.path.join(TS, "tiles.png"))
    cols = img.size[0] // 8
    done_tiles = set()
    changed = 0
    for m, slots in HEADS.items():
        ent = meta[m - 512]
        for s in slots:
            e = ent[s]
            t, pal = e & 0x3FF, e >> 12
            if pal == LIGHT_PAL:
                continue                                  # already moved
            assert pal == 6, (hex(m), s, pal)
            if t not in done_tiles:
                i = t - 512
                ox, oy = (i % cols) * 8, (i // cols) * 8
                for y in range(8):
                    for x in range(8):
                        v = img.getpixel((ox + x, oy + y)) & 15
                        if v:
                            img.putpixel((ox + x, oy + y), REMAP[v])
                done_tiles.add(t)
            ent[s] = (e & 0x0FFF) | (LIGHT_PAL << 12)
            changed += 1
    img.save(os.path.join(TS, "tiles.png"))
    open(meta_p, "wb").write(b"".join(struct.pack("<8H", *e) for e in meta))
    p = os.path.join(TS, "palettes", f"{LIGHT_PAL:02d}.pal")
    pal = load_pal(p)
    pal[0] = LAMP
    for i, c in BULB.items():
        pal[i] = c
    with open(p, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in pal))
    with open(p[:-4] + ".pla", "w") as f:
        f.write("# lamp bulbs (orchid_dns/lamps.py)\n0\n" + "".join(f"{i}\n" for i in sorted(BULB)))
    for folder in MAPS_WITH_OLD_GLOWS:
        mp = os.path.join(ROOT, "data", "maps", folder, "map.json")
        d = json.load(open(mp))
        objs = [o for o in d["object_events"] if o.get("graphics_id") != "OBJ_EVENT_GFX_LIGHT_SPRITE"]
        if len(objs) != len(d["object_events"]):
            d["object_events"] = objs
            with open(mp, "w") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
    print(f"moved {changed} lamp-head entries ({len(done_tiles)} tiles) to palette {LIGHT_PAL}")


if __name__ == "__main__":
    main()
