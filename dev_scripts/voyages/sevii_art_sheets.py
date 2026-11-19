"""
Review sheets for the gTileset_SeviiIslands art additions -> out/batch3/tileset/ (4x close-ups + budget.txt).

    venv/bin/python dev_scripts/voyages/sevii_art_sheets.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc            # noqa: E402
import frlg_translate as ft            # noqa: E402
from PIL import Image, ImageDraw       # noqa: E402

OUT = os.path.join(HERE, "out", "batch3", "tileset")
SV = ("gTileset_General", "gTileset_SeviiIslands")
st = vc.virtual("gTileset_SeviiIslands")
art = sys.modules["sevii_art_pieces"]
GRASS = 0x3001
SAND = vc.ref_value(("id", 0x124), ("gTileset_General", "gTileset_Rustboro"))


def patch(cells, w, h, at=(1, 1), ground=GRASS, extra=()):
    g = [[ground] * w for _ in range(h)]
    for j, row in enumerate(cells):
        for i, v in enumerate(row):
            if v is not None:
                g[at[1] + j][at[0] + i] = v
    for x, y, v in extra:
        g[y][x] = v
    return g


def label(im, text, scale=4):
    bar = Image.new("RGBA", (im.width, 14 + 4 * scale), (24, 24, 32, 255))
    d = ImageDraw.Draw(bar)
    d.text((6, 4), text, fill=(255, 255, 255, 255))
    out = Image.new("RGBA", (im.width, im.height + bar.height), (0, 0, 0, 255))
    out.paste(bar, (0, 0))
    out.paste(im, (0, bar.height))
    return out


def row(images, gap=8, bg=(40, 40, 48, 255)):
    w = sum(i.width for i in images) + gap * (len(images) - 1)
    h = max(i.height for i in images)
    out = Image.new("RGBA", (w, h), bg)
    x = 0
    for i in images:
        out.paste(i, (x, 0))
        x += i.width + gap
    return out


def col(images, gap=8, bg=(40, 40, 48, 255)):
    w = max(i.width for i in images)
    h = sum(i.height for i in images) + gap * (len(images) - 1)
    out = Image.new("RGBA", (w, h), bg)
    y = 0
    for i in images:
        out.paste(i, (0, y))
        y += i.height + gap
    return out


def door_mark(g, door, at, scale):
    return [(at[0] + door[0], at[1] + door[1], "", "warp")] if door else []


def cottage_sheet():
    tiles = []
    for name in ("cottage", "cottage_v1", "cottage_v2", "cottage_v3"):
        s = st.STAMPS[name]
        g = patch(s["cells"], 7, 6)
        im = vc.picture(g, SV, scale=4)
        tiles.append(label(im, "%s  door %s  -- %s" % (name, s["door"], s["note"][:44])))
    # in context: all four side by side on one street at 2x, as they would sit in a town
    g = [[GRASS] * 25 for _ in range(6)]
    for k, name in enumerate(("cottage", "cottage_v1", "cottage_v2", "cottage_v3")):
        for j, r in enumerate(st.STAMPS[name]["cells"]):
            for i, v in enumerate(r):
                g[1 + j][1 + k * 6 + i] = v
    ctx = label(vc.picture(g, SV, scale=2), "1x-ish context (2x): original | v1 | v2 | v3")
    out = col([row(tiles[:2]), row(tiles[2:]), ctx])
    out.convert("RGB").save(os.path.join(OUT, "cottage_variants@4x.png"))


def frlg_crop(name, x, y, w, h, scale=4):
    fm = ft.load_map(name)
    im = fm.picture(1).crop((x * 16, y * 16, (x + w) * 16, (y + h) * 16)).convert("RGBA")
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def onix_sheet():
    m = art.ONIX_MAP
    x0, y0, w, h = 0, 47, 17, 9                    # both formations + the plateau edge above them
    fr = label(frlg_crop(m, x0, y0, w, h), "FRLG %s x%d-%d y%d-%d (original)" % (m, x0, x0 + w - 1, y0, y0 + h - 1))
    # Emerald: Emerald sand everywhere, the ported formations at their FRLG cells, Emerald sea beyond the beach
    g = [[SAND] * w for _ in range(h)]
    for (mm, x, y), v in art.PORTED_CELLS.items():
        if x0 <= x < x0 + w and y0 <= y < y0 + h:
            g[y - y0][x - x0] = v
    em = label(vc.picture(g, SV, scale=4), "ported into gTileset_SeviiIslands (General palette 3), on Emerald sand")
    # FRLG rock vs Emerald rock (same palette): a vanilla Emerald cliff beside the port, 4x
    rb = ("gTileset_General", "gTileset_Rustboro")
    cliff = [[vc.ref_value(("id", i), rb) for i in r] for r in ((0x07C, 0x07C, 0x07C), (0x07C, 0x07C, 0x07C))]
    stamp = st.STAMPS["onix_tail_w"]["cells"]
    g2 = [[SAND] * 10 for _ in range(5)]
    for j, r in enumerate(stamp):
        for i, v in enumerate(r):
            g2[1 + j][1 + i] = v
    for j, r in enumerate(cliff):
        for i, v in enumerate(r):
            g2[1 + j][6 + i] = v
    cmp_ = label(vc.picture(g2, SV, scale=4), "palette check: ported mound | vanilla Emerald rock 0x07C")
    col([row([fr, em]), cmp_]).convert("RGB").save(os.path.join(OUT, "onix_tails@4x.png"))


def rocket_sheet():
    tos = ("gTileset_General", "gTileset_TosaPort")
    e, g = vc.raw_layout("LAYOUT_TOSA_PORT")
    cs = [r[20:30] for r in g[4:11]]
    a = label(vc.picture(cs, tos, scale=4), "Cold Storage (Tosa Port x21-28 y5-9, original)")
    s = st.STAMPS["rocket_warehouse"]
    gg = patch(s["cells"], 8, 7)
    b = label(vc.picture(gg, SV, [(1 + s["door"][0], 1 + s["door"][1], "", "warp")], scale=4),
              "Rocket Warehouse (6x5, door %s) palette '%s'" % (s["door"], art.ROCKET_CHOICE))
    c = label(frlg_crop("FiveIsland_Meadow", 8, 16, 8, 7), "FRLG Five Isle Meadow x8-15 y16-22")
    alts = []
    sc = vc.scene(SV)
    keep = sc.pals[art.ROCKET_PAL]
    for name in art.ROCKET_PALETTES:
        sc.pals[art.ROCKET_PAL] = art.rocket_palette(name)
        sc.cache.clear()
        alts.append(label(vc.picture(gg, SV, scale=2), "alt palette '%s' (2x)" % name))
    sc.pals[art.ROCKET_PAL] = keep
    sc.cache.clear()
    one = label(vc.picture(gg, SV, scale=1), "1x")
    col([row([a, b, c]), row(alts + [one])]).convert("RGB").save(os.path.join(OUT, "rocket_warehouse@4x.png"))


vc.SPRITES.setdefault("clerk_m", ("graphics/object_events/pics/people/mart_employee.png", 16, 32, 0, False))
vc.SPRITES.setdefault("player_up", ("graphics/object_events/pics/people/brendan/walking.png", 16, 32, 1, False))


def stall_sheet():
    m, fx, fy = art.STALL_FRLG
    x0, y0, w, h = fx - 3, fy - 1, 10, 7
    fr = label(frlg_crop(m, x0, y0, w, h), "FRLG TwoIsland x%d-%d y%d-%d (clerk at 28,4)" % (x0, x0 + w - 1, y0,
                                                                                         y0 + h - 1))
    s = st.STAMPS["market_stall"]
    g = patch(s["cells"], w, h, at=(fx - x0, fy - y0))
    cx, cy = fx - x0 + 1, fy - y0 + 2
    marks = [(cx, cy, "", "npc", "clerk_m"), (cx, cy + 2, "", "npc", "player_up")]
    em = vc.picture(g, SV, scale=4)
    vc._overlay(em, [mk for mk in marks], 4)
    em = label(em, "Emerald stall 4x4 (FRLG 27,1); clerk (28,3) behind the counter, player talks from (28,5)")
    plain = label(vc.picture(g, SV, scale=4), "same, no sprites")
    # next to an Emerald house (Briney's cottage) at 2x for scale
    g2 = [[GRASS] * 12 for _ in range(6)]
    for j, r in enumerate(st.STAMPS["cottage"]["cells"]):
        for i, v in enumerate(r):
            g2[1 + j][1 + i] = v
    for j, r in enumerate(s["cells"]):
        for i, v in enumerate(r):
            g2[1 + j][7 + i] = v
    ctx = vc.picture(g2, SV, scale=2)
    vc._overlay(ctx, [(8, 3, "", "npc", "clerk_m")], 2)
    ctx = label(ctx, "2x beside Mr. Briney's cottage")
    col([row([fr, em]), row([plain, ctx])]).convert("RGB").save(os.path.join(OUT, "market_stall@4x.png"))


RB = ("gTileset_General", "gTileset_Rustboro")


def ported_window(name, x0, y0, w, h, ground):
    """Emerald picture of an FRLG window: ported cells as PORTED_CELLS, other cells = Emerald ground / sea
    (stand-ins for whatever the translator puts there)."""
    fm = ft.load_map(name)
    sea = vc.ref_value(("id", 0x170), RB)
    pond = vc.ref_value(("id", 0x0A1), RB)
    g = []
    for y in range(y0, y0 + h):
        r = []
        for x in range(x0, x0 + w):
            v = art.PORTED_CELLS.get((name, x, y))
            if v is None:
                mb = ft.MB[fm.scene.attr(fm.mid(x, y)) & 0x1FF]
                v = pond if mb == "MB_POND_WATER" else sea if "WATER" in mb else ground
            r.append(v)
        g.append(r)
    return vc.picture(g, SV, scale=4)


def port_sheet(fname, title, name, wins, ground):
    rows = []
    for x0, y0, w, h in wins:
        a = label(frlg_crop(name, x0, y0, w, h), "FRLG %s x%d-%d y%d-%d" % (name, x0, x0 + w - 1, y0, y0 + h - 1))
        b = label(ported_window(name, x0, y0, w, h, ground), "%s: ported cells (others = Emerald stand-in ground)"
                  % title)
        rows.append(row([a, b]))
    col(rows).convert("RGB").save(os.path.join(OUT, fname))


def memorial_sheet():
    port_sheet("memorial_pillar@4x.png", "Memorial Pillar", "FiveIsland_MemorialPillar", [(3, 37, 11, 9)], GRASS)


def tanoby_sheet():
    wins = [(116, 3, 9, 9), (99, 4, 9, 8), (40, 5, 9, 8), (8, 1, 9, 8)]
    port_sheet("tanoby_chambers@4x.png", "Tanoby", "SevenIsland_TanobyRuins", wins, SAND)


def ruin_valley_sheet():
    port_sheet("ruin_valley_dotted_hole@4x.png", "Ruin Valley", "SixIsland_RuinValley", [(19, 17, 11, 16)], GRASS)


SHEETS = {"cottage": cottage_sheet, "memorial": memorial_sheet, "tanoby": tanoby_sheet, "ruin": ruin_valley_sheet, "stall": stall_sheet, "onix": onix_sheet, "rocket": rocket_sheet}


def main(argv):
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SHEETS.items():
        if len(argv) > 1 and name not in argv[1:]:
            continue
        fn()
    budget_txt()


def budget_txt():
    b = st.budget()
    lines = ["gTileset_SeviiIslands budget (proposed secondary = gTileset_Rustboro copy + additions)", ""]
    lines.append("base: Rustboro uses %d/512 tiles, %d/512 metatiles" % (b["base_tiles"], b["base_metatiles"]))
    lines.append("free tile slots: %d (art.free_policy: tiles no metatile of %s references; tile 0 and "
                 "Rustboro's anim destinations 128-159 / 448-451 excluded); %d Rustboro metatiles dropped (ids kept, "
                 "blanked)" % (len(st.FREE_TILES), ", ".join(art.KEEP_LAYOUTS), len(st.DROPPED_METATILES)))
    lines.append("")
    lines.append("%-32s %6s %10s  %s" % ("addition", "tiles", "metatiles", "palette slot"))
    for k, v in art.COST.items():
        lines.append("%-32s %6d %10d  %s" % (k, v["tiles"], v["metatiles"], v["palette"] or "-"))
    lines.append("%-32s %6d %10d" % ("TOTAL", b["new_tiles"], b["new_metatiles"]))
    lines.append("")
    lines.append("tiles left: %d   metatiles left: %d   secondary palette slots filled: %s (6, 7, 12 were unused "
                 "by every kept Rustboro metatile; 8-11 stay Rustboro's)" % (b["tiles_left"], b["metatiles_left"],
                                                                           b["palettes_changed"]))
    lines.append("")
    lines.append("metatiles are now the tight limit (%d left). If more are needed: the %d dropped Rustboro ids are "
                 "blank in the Sevii copy and could be re-used for new metatiles (no Sevii spec places them; "
                 "check_kept() guards the ones they do)." % (b["metatiles_left"], len(st.DROPPED_METATILES)))
    for k, v in art.NOTES.items():
        lines += ["", k + ":", v]
    open(os.path.join(OUT, "budget.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv)
