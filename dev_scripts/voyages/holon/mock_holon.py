"""
Render the Holon (batch 4, round 2) mockups into dev_scripts/voyages/out/batch4/ (1x + @2x, with marks).

The outdoor maps are composed in General + Fortree (every cell copied from a vanilla Fortree layout), then
converted to General + gTileset_Holon (the DRAFT Holon-only Fortree copy written by holon_tileset.py to
out/batch4/gTileset_Holon/): rock cells -> their blue-grey copies, spec["holon"] cells -> the new Holon
metatiles. They are rendered from the draft tileset files, i.e. what the game would load.

usage: <venv python> dev_scripts/voyages/holon/mock_holon.py [name ...] [--grid] [--seams]
  names: holon_coast holon_village holon_lake holon_tower_1f holon_tower_2f holon_ruins_house overview art
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402
import specs_holon as sp      # noqa: E402
import holon_tileset as ht    # noqa: E402
from PIL import Image, ImageDraw   # noqa: E402

OUT = os.path.join(HERE, "_draft", "mock")
HOLON = ("gTileset_General", "gTileset_Holon")
VARIANTS = {"current": ("gTileset_General", "gTileset_Holon"),
            "secondary": ("gTileset_General", "gTileset_HolonDesat"),
            "full": ("gTileset_GeneralHolon", "gTileset_HolonDesat")}
MAIN = VARIANTS["full"]                 # recommended look: primary + secondary greens desaturated
INFO = ht.build(write=True)            # (re)write the draft tileset first
GREEN_CHANGES = ht.write_green_variants()
IDS = INFO["metatiles"]
ROCK = {int(k[5:], 16): v for k, v in IDS.items() if k.startswith("rock_")}
DRAIN = {int(k[6:], 16): v for k, v in IDS.items() if k.startswith("drain_")}
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
DRAFTS = {"gTileset_Holon": ht.OUT,
          "gTileset_HolonDesat": os.path.join(os.path.dirname(ht.OUT), "gTileset_HolonDesat"),
          "gTileset_GeneralHolon": os.path.join(os.path.dirname(ht.OUT), "gTileset_GeneralHolon")}

_orig_dir = vc.vanilla.tileset_dir


def _tileset_dir(sym):
    return DRAFTS[sym] if sym in DRAFTS else _orig_dir(sym)


vc.vanilla.tileset_dir = _tileset_dir
vc._SPR["sphere_holon"] = ht.sphere_sprite(False)
vc._SPR["sphere_holon_on"] = ht.sphere_sprite(True)
vc.SPRITES.setdefault("sphere_holon", ("", 32, 32, 0, False))
vc.SPRITES.setdefault("sphere_holon_on", ("", 32, 32, 0, False))
_GRIDS = {}


def to_holon(g, spec):
    """Fortree-pair grid -> Holon-pair grid (rock -> blue-grey copies, new pieces placed)."""
    out = [row[:] for row in g]
    for row in out:
        for x, v in enumerate(row):
            if v & 0x3FF in ROCK:
                row[x] = (v & ~0x3FF) | ROCK[v & 0x3FF]
    # drained rings round the Power Spots: foliage within r_full -> palette-07 copies; between r_full and
    # r_fade a 4x4 ordered (Bayer) dither of drained / normal cells thins the effect out
    for cx, cy, r_full, r_fade in spec.get("drained", []):
        for y, row in enumerate(out):
            for x, v in enumerate(row):
                m = v & 0x3FF
                if m not in DRAIN:
                    continue
                d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5
                f = (d - r_full) / (r_fade - r_full)
                if d <= r_full or (f < 1 and BAYER[y % 4][x % 4] / 16 >= f):
                    row[x] = (v & ~0x3FF) | DRAIN[m]
    drained_cells = set()
    for cx, cy, r_full, r_fade in spec.get("drained", []):
        for y, row in enumerate(out):
            for x in range(len(row)):
                if ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5 <= r_full:
                    drained_cells.add((x, y))
    for name, x, y, solid in spec.get("holon", []):
        if (x, y) in drained_cells and name + "_drained" in IDS:
            name += "_drained"
        v = (out[y][x] & ~0x3FF) | IDS[name]
        out[y][x] = (v & ~0x0C00) | (0x0400 if solid else 0)
    return out


def render(name, spec, grid=False):
    g = vc.build(spec)
    ts = tuple(spec["tileset"])
    if ts == sp.FORTREE:
        g, ts = to_holon(g, spec), MAIN
    _GRIDS[name] = (g, ts)
    base = os.path.join(OUT, name)
    for scale, suffix in ((1, ""), (2, "@2x")):
        vc.picture(g, ts, spec.get("marks", []), scale, grid).convert("RGB").save(base + suffix + ".png")
    return g, ts


# ------------------------------------------------------------------ 4x art sheet: new pieces vs vanilla
def art_sheet():
    hol = vc.scene(MAIN)
    ftr = vc.scene(sp.FORTREE)

    def block(sc, ids, w):
        h = (len(ids) + w - 1) // w
        im = Image.new("RGBA", (w * 16, h * 16), (0, 0, 0, 0))
        for k, m in enumerate(ids):
            u, o = sc.metatile(m)
            c = u.copy()
            c.alpha_composite(o)
            im.paste(c, ((k % w) * 16, (k // w) * 16))
        return im

    def chunk(sc, lid, sx, sy, w, h, remap=False):
        g = vc.raw_layout(lid)[1]
        ids = [g[sy + j][sx + i] & 0x3FF for j in range(h) for i in range(w)]
        return block(sc, [ROCK.get(m, m) for m in ids] if remap else ids, w)

    tomb_ids = [vc.raw_layout(sp.R120)[1][52 + j][5 + i] & 0x3FF for j in range(4) for i in range(5)]
    sealed = [ROCK.get(m, m) for m in tomb_ids]
    sealed[2 * 5 + 2] = IDS["door_arch"]
    sealed[3 * 5 + 2] = IDS["door_slab"]
    soot = vc.scene(("gTileset_General", "gTileset_Sootopolis"))
    tanoby = vc.scene(("gTileset_General", "gTileset_TanobyDelta"))
    plin = block(hol, [IDS["plinth_%d%d" % (cx, cy)] for cy in range(2) for cx in range(3)], 3)
    s_off, s_on = plin.copy(), plin.copy()
    s_off.alpha_composite(ht.sphere_sprite(False), (8, -4))
    s_on.alpha_composite(ht.sphere_sprite(True), (8, -4))
    s_off = _pad_top(s_off, 8, hol)
    s_on = _pad_top(s_on, 8, hol)
    pond = block(hol, [0x0A1, IDS["pillar_top"], 0x0A1, 0x0A1, IDS["pillar_mid"], 0x0A1, 0x0A1,
                       IDS["pillar_base"], 0x0A1], 3)
    stone = block(hol, [0x001, IDS["stone_top"], 0x001, 0x001, IDS["stone_bottom"], 0x001], 3)
    rails = block(hol, [IDS["rail_HW"], IDS["rail_H"], IDS["rail_H"], IDS["rail_HE"]], 4)
    boulder = block(ftr, [0x001], 1)
    boulder.alpha_composite(vc.sprite("sphere"), (0, 0))
    rows = [
        [("Route 120 ridge + spikes (vanilla, brown)", chunk(ftr, sp.R120, 13, 40, 5, 6)),
         ("same cells, gTileset_Holon palette 06", chunk(hol, sp.R120, 13, 40, 5, 6, True)),
         ("Ancient Tomb dome (vanilla)", block(ftr, tomb_ids, 5)),
         ("sealed carved dome (Holon)", block(hol, sealed, 5))],
        [("lake pillar 1x3 in water (new)", pond),
         ("ref: Tanoby pillar (TanobyDelta)", chunk(tanoby, "LAYOUT_TANOBY_DELTA", 18, 8, 3, 3)),
         ("carved standing stone 1x2 (new)", stone),
         ("ref: Sootopolis carved block", chunk(soot, "LAYOUT_SOOTOPOLIS_CITY@git", 2, 7, 3, 3))],
        [("sphere object on plinth: dormant", s_off), ("sphere: glowing (OBJ palette swap)", s_on),
         ("ref: Strength boulder object", boulder),
         ("old railway: Orchid rail kit (HW H H HE)", rails)],
    ]
    S = 4
    W = max(sum(max(p.width * S, 250) + 24 for _, p in r) for r in rows) + 24
    H = sum(max(p.height for _, p in r) * S + 44 for r in rows) + 24
    out = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(out)
    y = 12
    for r in rows:
        x = 12
        for label, p in r:
            big = p.resize((p.width * S, p.height * S), Image.NEAREST)
            d.text((x, y), label, fill=(0, 0, 0))
            bg = Image.new("RGBA", big.size, (255, 255, 255, 255))
            bg.alpha_composite(big)
            out.paste(bg.convert("RGB"), (x, y + 16))
            x += max(big.width, 250) + 24
        y += max(p.height for _, p in r) * S + 44
    out.save(os.path.join(OUT, "holon_new_art_4x.png"))


def _pad_top(im, n, sc):
    """Add n px of grass above (so a sprite poking above its cells is not cut)."""
    u, o = sc.metatile(0x001)
    out = Image.new("RGBA", (im.width, im.height + n))
    for x in range(0, im.width, 16):
        out.paste(u.crop((0, 16 - n, 16, 16)), (x, 0))
    out.paste(im, (0, n))
    return out


def palette_strip():
    g3 = ht.load_pal(os.path.join(ht.GENERAL, "palettes", "03.pal"))
    p6 = ht.load_pal(os.path.join(ht.OUT, "palettes", "06.pal"))
    S = 24
    im = Image.new("RGB", (16 * S + 140, 2 * S + 30), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for row, (lab, p) in enumerate((("General 03", g3), ("Holon 06", p6))):
        d.text((4, 14 + row * (S + 4) + 6), lab, fill=(0, 0, 0))
        for i, c in enumerate(p):
            d.rectangle([130 + i * S, 14 + row * (S + 4), 130 + i * S + S - 2, 14 + row * (S + 4) + S], fill=c)
    for i in range(16):
        d.text((130 + i * S + 4, 0), str(i), fill=(0, 0, 0))
    im.save(os.path.join(OUT, "holon_palette06.png"))


def green_compare():
    """Village and lake @2x three ways (current / secondary-only / primary + secondary desaturated), plus a
    side-by-side of GBA-camera-sized crops (15x10 tiles) round the two Power Spots."""
    crops = []
    for name, (cx, cy) in (("holon_village", (12, 30)), ("holon_lake", (44, 10))):
        g, _ = _GRIDS[name]
        marks = sp.ALL[name]["marks"]
        row = []
        for vname, ts in VARIANTS.items():
            im = vc.picture(g, ts, marks, 2)
            im.convert("RGB").save(os.path.join(OUT, "%s_green_%s@2x.png" % (name, vname)))
            x0, y0 = (cx - 7) * 32, (cy - 5) * 32
            row.append((vname, im.crop((x0, y0, x0 + 15 * 32, y0 + 10 * 32))))
        crops.append(row)
    W = 3 * (15 * 32 + 12) + 12
    H = 2 * (10 * 32 + 30) + 12
    out = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(out)
    labels = {"current": "current (vanilla greens)", "secondary": "secondary-only desaturated",
              "full": "primary + secondary desaturated (recommended)"}
    for r, row in enumerate(crops):
        for c, (vname, im) in enumerate(row):
            x, y = 12 + c * (15 * 32 + 12), 12 + r * (10 * 32 + 30)
            d.text((x, y), labels[vname], fill=(0, 0, 0))
            out.paste(im.convert("RGB"), (x, y + 16))
    out.save(os.path.join(OUT, "holon_green_compare@2x.png"))


def sphere_glow_crop():
    g, ts = _GRIDS["holon_lake"]
    for on in (False, True):
        marks = [m for m in sp.ALL["holon_lake"]["marks"] if m[3] not in ("field", "spot")]
        marks.append((sp.L_SPHERE[0], sp.L_SPHERE[1], "", "field", "sphere_holon_on" if on else "sphere_holon"))
        im = vc.picture(g, ts, marks, 2).crop((12 * 32, 14 * 32, 38 * 32, 38 * 32))
        im.convert("RGB").save(os.path.join(OUT, "holon_lake_pillars_%s@2x.png" % ("glow" if on else "dormant")))


# ------------------------------------------------------------------ overview
def overview():
    names = ("holon_coast", "holon_village", "holon_lake", "holon_tower_1f", "holon_tower_2f", "holon_ruins_house")
    ims = {n: Image.open(os.path.join(OUT, n + ".png")) for n in names}
    T = 16
    vx, vy = sp.CW * T, 0
    cx, cy = 0, sp.C_OFFSET * T
    lx, ly = vx, sp.VH * T
    side = max(ims[k].width for k in names[3:])
    W = vx + sp.VW * T + 20 + max(side, 330) + 10
    H = max(ly + sp.LH * T, cy + sp.CH * T) + 30
    out = Image.new("RGB", (W, H), (30, 30, 40))
    out.paste(ims["holon_coast"], (cx, cy))
    out.paste(ims["holon_village"], (vx, vy))
    out.paste(ims["holon_lake"], (lx, ly))
    d = ImageDraw.Draw(out)
    lab = lambda x, y, t: d.text((x, y), t, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))  # noqa
    tx, ty = vx + sp.VW * T + 20, 24
    for n, title in (("holon_tower_1f", "Research Tower 1F (Weather Institute 1F)"),
                     ("holon_tower_2f", "Research Tower 2F (+ Lab machines)"),
                     ("holon_ruins_house", "Holon Ruins house (HOUSE1, abandoned)")):
        lab(tx, ty, title)
        out.paste(ims[n], (tx, ty + 16))
        ty += ims[n].height + 40
    lab(tx, ty, "outdoor maps: General + gTileset_Holon")
    lab(cx + 4, cy + 4, "Mirage Forest coast 44x48 (arrival)")
    lab(vx + 4, vy + 4, "Holon Village 72x72")
    lab(lx + 4, ly + 4, "Holon Lake 72x52")
    d.line([(vx, cy), (vx, cy + sp.CH * T)], fill=(255, 140, 0), width=2)
    d.line([(lx, ly), (lx + sp.LW * T, ly)], fill=(255, 140, 0), width=2)
    out.save(os.path.join(OUT, "overview.png"))


def main(args):
    names = [a for a in args if not a.startswith("--")]
    os.makedirs(OUT, exist_ok=True)
    for name, spec in sp.ALL.items():
        if names and name not in names:
            continue
        if "base" not in spec:
            vc.check_size(*spec["size"])
        g, ts = render(name, spec, grid="--grid" in args)
        print("%-22s %2dx%-2d %s/%s  %d metatiles" % (name, spec["size"][0], spec["size"][1], ts[0][9:], ts[1][9:],
                                                     len(vc.metatile_ids(g))))
    for name, (lid, marks) in sp.AS_IS.items():
        if names and name not in names:
            continue
        vc.render_layout(lid, os.path.join(OUT, name), marks)
        print("%-22s (as is) %s" % (name, lid))
    if not names or "art" in names:
        art_sheet()
        palette_strip()
    if not names or "holon_lake" in names:
        sphere_glow_crop()
    if not names or "green" in names:
        if "holon_village" not in _GRIDS:
            render("holon_village", sp.ALL["holon_village"])
        if "holon_lake" not in _GRIDS:
            render("holon_lake", sp.ALL["holon_lake"])
        green_compare()
    if not names or "overview" in names:
        overview()


if __name__ == "__main__":
    main(sys.argv[1:])
