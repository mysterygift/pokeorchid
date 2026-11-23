#!/usr/bin/env python3
"""Lit windows for towns outside the TosaPort tileset (Telok + the Tiksi towns).

Per town tileset (secondary), in this order:
  copy     glass drawn by the town tileset's own metatiles with a palette that has too few free indices (or a
           primary palette, which can't change): those 8x8 entries switch to a spare slot holding an exact copy
           of that palette, so the day look is unchanged and the copy has plenty of free indices
  native   windows.py's method on secondary palettes 6-12: glass pixels move to free light indices of their
           palette (tiles also used elsewhere are copied first)
  shared   Pokémon Center / Mart / General houses (primary metatiles): the lit copies TosaPort already has
           (lightpal.py tosa_windows) go into blank slots of the town tileset, drawn with a spare slot holding
           TosaPort's window palette (11.pal + .pla), and the town maps are repointed

    towns.py detect TOWN out.png     preview the town's own glass (magenta) on its map
    towns.py report TOWN|all
    towns.py apply TOWN|all          run once on clean tilesets (not re-entrant)

TosaPort's primary -> lit copy pairs come from git history (the map cells the DNS commit repointed).
"""
import json
import os
import struct
import subprocess
import sys

import dns_tool as T
import windows as W

ROOT = T.ROOT
PRE_DNS = "5c47ccf97a"          # last commit before the TosaPort window lights (e397b2d374)
TOSA = ("gTileset_General", "gTileset_TosaPort", 11)
IS_GLASS = W.is_glass

TOWNS = {
    # town: (secondary, layout, slot for the shared window palette, options)
    #   copy    {glass palette: spare slot for its copy}
    #   skip    pixel boxes on the town map whose metatiles are never glass (roofs, fountain water)
    #   always  pixel boxes whose metatiles light every glass-coloured pixel (light-framed panes)
    "telok": ("gTileset_Petalburg", "LAYOUT_OLDALE_TOWN", 11, {"copy": {8: 7}}),
    "furong": ("gTileset_Dewford", "LAYOUT_FURONG_VILLAGE", 11, {"copy": {5: 12}}),
    "drake": ("gTileset_Lavaridge", "LAYOUT_DRAKE_BASE_CAMP", 12, {}),
    "ube": ("gTileset_UbeCity", "LAYOUT_UBE_CITY", 12, {
        # no spare slot left for copies: the olive house (pal 11) and the street lamps (pal 5) stay dark
        "skip": [(224, 208, 271, 255)],                         # fountain
        # the big building's lavender frame shades: not glass (keeps its pane colours exact by day)
        "not_glass": [(200, 192, 216), (144, 136, 168)],
    }),
    "tanglyn": ("gTileset_Lilycove", "LAYOUT_TANGLYN_TOWN", 11, {
        "copy": {8: 10},
        # the houses' glass goes to a second copy (one copy has too few free indices for both buildings)
        "copy_boxes": {12: [(128, 336, 191, 367), (384, 240, 447, 271)]},
        "skip": [(128, 304, 191, 335), (384, 208, 447, 239),    # blue tiled roofs
                 (16, 112, 175, 127)],                          # mansion balustrade
    }),
}


def layouts():
    return json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"]


def layout(lid):
    return next(l for l in layouts() if l.get("id") == lid)


def cells(path):
    return [b for (b,) in struct.iter_unpack("<H", open(path, "rb").read())]


def git_show(rev, path):
    r = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def save_meta(ts, smeta):
    open(os.path.join(ts.sd, "metatiles.bin"), "wb").write(b"".join(struct.pack("<8H", *e) for e in smeta))


def pal_path(ts, p):
    return os.path.join(ts.pd if p < T.NUM_PALS_IN_PRIMARY else ts.sd, "palettes", f"{p:02d}")


def town_layouts(sec):
    return [l for l in layouts() if l.get("secondary_tileset") == sec and l.get("primary_tileset") == "gTileset_General"]


def placed(sec):
    used = set()
    for l in town_layouts(sec):
        p = os.path.join(ROOT, l["blockdata_filepath"])
        if os.path.exists(p):
            used.update(b & 0x3FF for b in cells(p))
    return used


def used_slots(ts):
    return {v >> 12 for e in ts.smeta for v in e if (v & 0x3FF) != 0}


# ------------------------------------------------------------------ glass detection (town map only)
def box_mids(lid, boxes):
    lay = layout(lid)
    c = cells(os.path.join(ROOT, lay["blockdata_filepath"]))
    out = set()
    for (x0, y0, x1, y1) in boxes:
        for my in range(y0 // 16, y1 // 16 + 1):
            for mx in range(x0 // 16, x1 // 16 + 1):
                out.add(c[my * lay["width"] + mx] & 0x3FF)
    return out


def setup(town):
    """Registers the town's windows.py config (its own metatiles on its own map) and returns its key."""
    sec, lid, slot, opts = TOWNS[town]
    lay = layout(lid)
    own = {b & 0x3FF for b in cells(os.path.join(ROOT, lay["blockdata_filepath"])) if (b & 0x3FF) >= 512}
    own -= box_mids(lid, opts.get("skip", []))
    always = box_mids(lid, opts.get("always", [])) & own
    key = f"town_{town}"
    W.CONFIG[key] = {"primary": "gTileset_General", "secondary": sec, "windows": sorted(own - always),
                     "always": sorted(always), "masks": []}
    W.layouts_of = lambda cfg, _lid=lid: [_lid]
    nots = set(map(tuple, opts.get("not_glass", [])))
    W.is_glass = lambda c, _n=nots: tuple(c) not in _n and IS_GLASS(c)
    return key


def glass_entries(town):
    """{(metatile, entry slot): pal} for the town tileset's own metatiles that draw glass."""
    sec = TOWNS[town][0]
    key = setup(town)
    ts = T.Tilesets("gTileset_General", sec)
    out = {}
    for m, pix in W.glass_by_metatile(W.CONFIG[key]).items():
        if m < 512:
            continue
        ent = ts.entries(m)
        for (x, y) in pix:
            r = W.tile_of(ts, ent, x, y)
            if r:
                out[(m, r[0])] = r[2]
    return ts, out


# ------------------------------------------------------------------ copy
def apply_copy(town):
    sec, lid, slot, opts = TOWNS[town]
    copy = opts.get("copy", {})
    if not copy:
        return
    ts, glass = glass_entries(town)
    taken = used_slots(ts)
    extra = {q: box_mids(lid, boxes) for q, boxes in opts.get("copy_boxes", {}).items()}
    for q in list(copy.values()) + list(extra):
        assert q not in taken and q != slot and 6 <= q < 13, f"{sec}: slot {q} isn't free"
    smeta = [list(e) for e in ts.smeta]
    n, src_of = 0, {}
    for (m, s), p in glass.items():
        if p in copy:
            q = next((q for q, mids in extra.items() if m in mids), copy[p])
            e = smeta[m - 512][s]
            smeta[m - 512][s] = (e & 0x0FFF) | (q << 12)
            src_of[q] = p
            n += 1
    save_meta(ts, smeta)
    for q, p in src_of.items():
        with open(pal_path(ts, p) + ".pal") as f, open(pal_path(ts, q) + ".pal", "w", newline="") as g:
            g.write(f.read())
    print(f"  copy: {n} glass entries -> palette copies {src_of} (copy slot <- source)")


# ------------------------------------------------------------------ native
ORIG_PLAN = W.plan


def plan_in_place(key):
    """windows.py's plan, but a glass shade that nothing else draws with that palette stays where it is (it
    just becomes a light), so only shades shared with walls / frames need a free index (fewer merges)."""
    ts, cfg, gm, glass_px, uses, shades, alloc, copies, notes = ORIG_PLAN(key)
    other = [set() for _ in range(16)]          # indices drawn at non-glass pixels, per palette
    for m in list(range(len(ts.pmeta))) + [512 + i for i in range(len(ts.smeta))]:
        for s, e in enumerate(ts.entries(m)):
            t, pal = e & 0x3FF, e >> 12
            tile = ts.ptiles[t] if t < 512 else (ts.stiles[t - 512] if t - 512 < len(ts.stiles) else None)
            if tile is None:
                continue
            gp = glass_px.get((t, pal), set()) if (m, s) in uses.get((t, pal), ()) else set()
            for y in range(8):
                for x in range(8):
                    c = tile[y][x]
                    if (x, y) not in gp and (c or s < 4):
                        other[pal].add(c)
    used = W.index_usage(cfg, ts)
    alloc, notes = {}, []
    for pal, idxs in sorted(shades.items()):
        if pal == 0 or pal >= 13:
            continue
        a = {i: i for i in idxs if i not in other[pal]}
        rest = sorted((i for i in idxs if i not in a), key=lambda i: W.lum(ts.pals[pal][i]))
        free = [i for i in range(1, 16) if i not in used[pal]]
        if rest and not free:
            notes.append(f"pal {pal}: no free index, {len(rest)} glass shade(s) left unlit")
        elif rest:
            k = min(len(free), len(rest))
            a.update({i: free[min(k - 1, n * k // len(rest))] for n, i in enumerate(rest)})
            if len(rest) > len(free):
                notes.append(f"pal {pal}: {len(rest)} shared glass shades merged into {k} light colour(s)")
        if a:
            alloc[pal] = a
    copies = {k: v for k, v in copies.items()
              if k[1] in alloc and any(alloc[k[1]].get(c) not in (None, c)
                                       for (x, y) in glass_px[k] for c in [(ts.ptiles[k[0]] if k[0] < 512 else ts.stiles[k[0] - 512])[y][x]])}
    return ts, cfg, gm, glass_px, uses, shades, alloc, copies, notes


def native_alloc(town):
    sec, lid, slot, opts = TOWNS[town]
    key = setup(town)
    plan = plan_in_place(key)
    copied_from = set(opts.get("copy", {}))
    keep = {p for p in plan[6] if 6 <= p < 13 and p != slot and p not in copied_from}
    return key, plan, keep


def apply_native(town):
    key, _, keep = native_alloc(town)

    def plan_kept(k):
        r = list(plan_in_place(k))
        r[6] = {p: v for p, v in r[6].items() if p in keep}       # alloc
        return tuple(r)
    W.plan = plan_kept
    try:
        W.apply(key)
    finally:
        W.plan = ORIG_PLAN


# ------------------------------------------------------------------ shared (primary) windows
def tosa_lit_copies():
    """{primary metatile: TosaPort secondary metatile id} for every window lightpal.py copied."""
    tp = T.Tilesets(TOSA[0], TOSA[1])
    lit = {512 + i for i, e in enumerate(tp.smeta) if any((v >> 12) == TOSA[2] for v in e)}
    out = {}
    for l in layouts():
        if l.get("secondary_tileset") != TOSA[1]:
            continue
        p = os.path.join(ROOT, l["blockdata_filepath"])
        old = git_show(PRE_DNS, l["blockdata_filepath"])
        if old is None or not os.path.exists(p):
            continue
        new = open(p, "rb").read()
        if len(old) != len(new):
            continue
        for (a,), (b,) in zip(struct.iter_unpack("<H", old), struct.iter_unpack("<H", new)):
            a, b = a & 0x3FF, b & 0x3FF
            if a != b and a < 512 and b in lit:
                assert out.get(a, b) == b, f"two lit copies for {a:03X}"
                out[a] = b
    return tp, out


def shared_plan(town):
    sec, lid, slot, _ = TOWNS[town]
    tp, copies = tosa_lit_copies()
    use = placed(sec)
    need = {m: s for m, s in copies.items() if m in use}
    ts = T.Tilesets("gTileset_General", sec)
    blank = [512 + i for i, e in enumerate(ts.smeta) if all((v & 0x3FF) == 0 for v in e) and (512 + i) not in use]
    return tp, ts, need, blank


def apply_shared(town):
    sec, lid, slot, _ = TOWNS[town]
    tp, ts, need, blank = shared_plan(town)
    assert slot not in used_slots(ts), f"{sec}: palette slot {slot} is in use"
    smeta = [list(e) for e in ts.smeta]
    attr_p = open(os.path.join(ts.pd, "metatile_attributes.bin"), "rb").read()
    attr_path = os.path.join(ts.sd, "metatile_attributes.bin")
    attr_s = bytearray(open(attr_path, "rb").read())
    asz = len(attr_s) // len(ts.smeta)
    remap = {}
    for m, src in sorted(need.items()):
        ent = []
        for v in tp.smeta[src - 512]:
            assert (v & 0x3FF) < 512, "a lit copy points at a TosaPort tile"
            ent.append((v & 0x0FFF) | (slot << 12) if (v >> 12) == TOSA[2] else v)
        if blank:
            new = blank.pop(0)
            smeta[new - 512] = ent
        else:                                   # append (secondaries hold up to 512 metatiles)
            new = 512 + len(smeta)
            assert new < 1024, "secondary metatile limit"
            smeta.append(ent)
            attr_s += bytes(asz)
        i = new - 512
        attr_s[i * asz:(i + 1) * asz] = attr_p[m * asz:(m + 1) * asz]
        remap[m] = new
    save_meta(ts, smeta)
    open(attr_path, "wb").write(attr_s)
    n = 0
    for l in town_layouts(sec):
        p = os.path.join(ROOT, l["blockdata_filepath"])
        if not os.path.exists(p):
            continue
        c = cells(p)
        out = [(b & ~0x3FF) | remap[b & 0x3FF] if (b & 0x3FF) in remap else b for b in c]
        if out != c:
            open(p, "wb").write(struct.pack(f"<{len(out)}H", *out))
            n += 1
    src, dst = pal_path(tp, TOSA[2]), pal_path(ts, slot)
    for ext in (".pal", ".pla"):
        with open(src + ext) as f, open(dst + ext, "w", newline="") as g:
            g.write(f.read())
    print(f"  shared: {len(remap)} lit Centre/Mart/house metatiles -> pal {slot}, {n} maps repointed")


# ------------------------------------------------------------------ commands
def report(town):
    sec, lid, slot, opts = TOWNS[town]
    print(f"{town} ({sec}, {lid}; free slots {sorted(set(range(6, 13)) - used_slots(T.Tilesets('gTileset_General', sec)))})")
    _, glass = glass_entries(town)
    per = {}
    for p in glass.values():
        per[p] = per.get(p, 0) + 1
    print(f"  glass entries per palette: {dict(sorted(per.items()))}; copies {opts.get('copy', {})}")
    key, plan, keep = native_alloc(town)
    ts = plan[0]
    for p, m in sorted(plan[6].items()):
        if p in keep:
            print(f"  native pal {p:2d}: " + ", ".join(f"{o}{ts.pals[p][o]}->{n}" for o, n in sorted(m.items())))
    for n in plan[8]:
        print("  NOTE", n)
    tp, tss, need, blank = shared_plan(town)
    print(f"  shared: {len(need)} metatiles; blank slots {len(blank)}"
          f"{'' if len(blank) >= len(need) else f' (appending {len(need) - len(blank)})'}")


def detect(town, png):
    sec, lid, slot, _ = TOWNS[town]
    key = setup(town)
    ts, info, blocks, w = T.load_layout(lid)
    hits = W.detect(ts, info, len(info[0]), len(info), blocks, w, W.CONFIG[key])
    im = T.image(ts, info)
    for (x, y) in hits:
        if info[y][x][0]:
            im.putpixel((x, y), (255, 0, 255))
    im.save(png)
    print(f"{len(hits)} glass pixels")


if __name__ == "__main__":
    cmd, town = sys.argv[1], sys.argv[2]
    names = list(TOWNS) if town == "all" else [town]
    if cmd == "detect":
        detect(town, sys.argv[3])
    elif cmd == "report":
        for t in names:
            report(t)
    elif cmd == "apply":
        for t in names:
            print(t)
            apply_copy(t)
            apply_native(t)
            apply_shared(t)
