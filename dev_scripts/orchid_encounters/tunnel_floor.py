#!/usr/bin/env python3
"""Railway Tunnels: give the tunnel floor wild encounters (user, 2026-11-23).

The floor metatiles 0x20D / 0x20E of gTileset_UrbanPlatform have behaviour MB_NORMAL and are shared with
every Tosa Rail station platform. This appends copies of them to UrbanPlatform with behaviour
MB_INDOOR_ENCOUNTER (an encounter tile, like vanilla's indoor encounter floors) and points only
RailwayTunnels' passable floor cells at the copies. Idempotent (re-running finds the copies).

    tunnel_floor.py
"""
import json
import os
import re
import struct

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TS = os.path.join(ROOT, "data", "tilesets", "secondary", "urban_platform")
FLOORS = [0x20D, 0x20E]
LAYOUT = "LAYOUT_RAILWAY_TUNNELS"


def behaviour_value(name):
    src = open(os.path.join(ROOT, "include", "constants", "metatile_behaviors.h")).read()
    body = src[src.index("{", src.index("enum")) + 1:]
    names = re.findall(r"^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,", body, re.M)
    v = -1
    for n, explicit in names:
        v = int(explicit, 0) if explicit else v + 1
        if n == name:
            return v
    raise SystemExit(name + " not found")


def main():
    mb = behaviour_value("MB_INDOOR_ENCOUNTER")
    meta_p, attr_p = os.path.join(TS, "metatiles.bin"), os.path.join(TS, "metatile_attributes.bin")
    meta, attrs = bytearray(open(meta_p, "rb").read()), bytearray(open(attr_p, "rb").read())
    n = len(meta) // 16
    copies = {}
    for f in FLOORS:
        i = f - 512
        ent, at = meta[i * 16:(i + 1) * 16], struct.unpack_from("<H", attrs, i * 2)[0]
        want = (at & ~0xFF) | mb
        # reuse an existing copy (same tiles, encounter behaviour) if a previous run made one
        found = next((512 + j for j in range(n) if meta[j * 16:(j + 1) * 16] == ent
                      and struct.unpack_from("<H", attrs, j * 2)[0] == want), None)
        if found is None:
            meta += ent
            attrs += struct.pack("<H", want)
            found = 512 + n
            n += 1
        copies[f] = found
    open(meta_p, "wb").write(meta)
    open(attr_p, "wb").write(attrs)
    lay = next(l for l in json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]
               if l.get("id") == LAYOUT)
    p = os.path.join(ROOT, lay["blockdata_filepath"])
    cells = [b for (b,) in struct.iter_unpack("<H", open(p, "rb").read())]
    out = [(b & ~0x3FF) | copies[b & 0x3FF] if (b & 0x3FF) in copies and not (b >> 10) & 3 else b for b in cells]
    open(p, "wb").write(struct.pack(f"<{len(out)}H", *out))
    print("MB_INDOOR_ENCOUNTER =", mb, "; copies", {hex(a): hex(b) for a, b in copies.items()},
          "; cells repointed", sum(1 for a, b in zip(cells, out) if a != b))


if __name__ == "__main__":
    main()
