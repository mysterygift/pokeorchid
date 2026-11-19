"""
Holon wild-encounter proposal (design review, batch 5).

Four maps: Mirage Forest coast, Holon village, Holon Research Tower, Holon Lake.
Slots use the vanilla rate tables (land 12 / water 5 / rock smash 5 / fishing 2+3+5).
Names ending in "-δ" are Delta species; "H:" = Holon's Pokémon (plain species).
Time of day: OW_TIME_OF_DAY_ENCOUNTERS is TRUE; a table without a suffix is the TIME_MORNING
fallback, "_Night" tables override at night (base_label gHolonVillage_Night etc.).

usage: wild_tables.py -> delta/wild_tables.csv + out/batch5_delta/wild_tables.png (+ coverage check)
"""
import csv
import os
from PIL import Image, ImageDraw, ImageFont
import delta_table as DT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out", "batch5_delta")

RATES = {
    "land": [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1],
    "water": [60, 30, 5, 4, 1],
    "rock_smash": [60, 30, 5, 4, 1],
    "old_rod": [70, 30],
    "good_rod": [60, 20, 20],
    "super_rod": [40, 40, 15, 4, 1],
}

# map -> [(table, time, [(species, min, max), ...])]
MAPS = {
    "Mirage Forest coast (Lv 50-58)": [
        ("land", "day", [("Tropius", 52, 54), ("Wingull-δ", 50, 53), ("Pelipper", 54, 54), ("Swablu-δ", 50, 52),
                         ("Spinda", 52, 52), ("Exeggutor", 54, 54), ("Flaaffy-δ", 52, 54), ("Trapinch", 52, 52),
                         ("Treecko-δ", 50, 50), ("Altaria-δ", 55, 55), ("Charmander-δ", 50, 50), ("Totodile-δ", 50, 50)]),
        ("land", "night", [("Drifloon-δ", 52, 54), ("Shuppet", 52, 54), ("Pelipper", 54, 54), ("Vulpix-δ", 50, 52),
                           ("Spinda", 52, 52), ("Exeggutor", 54, 54), ("Flaaffy-δ", 52, 54), ("Banette", 55, 55),
                           ("Ninetales-δ", 56, 56), ("Altaria-δ", 55, 55), ("Charmander-δ", 50, 50), ("Totodile-δ", 50, 50)]),
        ("water", "any", [("Tentacruel", 50, 55), ("Pelipper-δ", 52, 55), ("Wailmer", 50, 52), ("Croconaw-δ", 52, 54),
                          ("Feraligatr-δ", 56, 56)]),
        ("old_rod", "any", [("Magikarp", 50, 50), ("Krabby-δ", 50, 50)]),
        ("good_rod", "any", [("Krabby-δ", 52, 52), ("Corsola", 52, 52), ("Luvdisc", 52, 52)]),
        ("super_rod", "any", [("Kingler-δ", 55, 55), ("Sharpedo", 55, 55), ("Relicanth-δ", 55, 55), ("Wailord", 58, 58),
                              ("Lapras", 58, 58)]),
    ],
    "Holon village (Lv 52-58)": [
        ("land", "day", [("Glameow-δ", 52, 54), ("Miltank", 53, 55), ("Farfetch'd-δ", 54, 54), ("Stantler-δ", 54, 54),
                         ("Furret", 53, 53), ("Tauros", 55, 55), ("Pancham-δ", 52, 52), ("Ralts-δ", 52, 52),
                         ("Kirlia-δ", 54, 54), ("Smeargle", 55, 55), ("Larvitar-δ", 52, 52), ("Bagon-δ", 52, 52)]),
        ("land", "night", [("Purrloin-δ", 52, 54), ("Noctowl", 53, 55), ("Drifloon-δ", 54, 54), ("Stantler-δ", 54, 54),
                           ("Mightyena", 53, 53), ("Misdreavus", 55, 55), ("Liepard-δ", 55, 55), ("Ralts-δ", 52, 52),
                           ("Drifblim-δ", 56, 56), ("Murkrow", 55, 55), ("Pupitar-δ", 55, 55), ("Shelgon-δ", 55, 55)]),
        ("water", "any", [("Azumarill", 52, 55), ("Golduck", 53, 55), ("Dragonair-δ", 55, 55), ("Quagsire", 54, 54),
                          ("Dragonite-δ", 58, 58)]),
        ("old_rod", "any", [("Magikarp-δ", 50, 50), ("Goldeen", 50, 50)]),
        ("good_rod", "any", [("Magikarp-δ", 52, 52), ("Seaking", 52, 52), ("Dratini-δ", 52, 52)]),
        ("super_rod", "any", [("Dratini-δ", 55, 55), ("Seaking", 55, 55), ("Dragonair-δ", 57, 57), ("Gyarados-δ", 58, 58),
                              ("Dragonite-δ", 60, 60)]),
    ],
    "Holon Research Tower (Lv 55-60)": [
        ("land", "any", [("H:Magneton", 55, 57), ("H:Voltorb", 55, 55), ("Klang-δ", 56, 56), ("Metang-δ", 56, 56),
                         ("H:Electrode", 57, 57), ("Klink-δ", 55, 55), ("H:Castform", 55, 55), ("H:Magnemite", 55, 55),
                         ("Beldum-δ", 55, 55), ("Porygon2", 58, 58), ("Eevee-δ", 55, 55), ("Klinklang-δ", 60, 60)]),
    ],
    "Holon Lake (Lv 55-65)": [
        ("land", "day", [("Pidgeotto-δ", 58, 60), ("Pikachu-δ", 58, 60), ("Vibrava-δ", 59, 59), ("Meowth-δ", 58, 58),
                         ("Gloom-δ", 58, 58), ("Trapinch-δ", 58, 58), ("Persian-δ", 61, 61), ("Raichu-δ", 61, 61),
                         ("Pidgeot-δ", 63, 63), ("Flygon-δ", 63, 63), ("H:Castform", 60, 60), ("Vileplume-δ", 63, 63)]),
        ("land", "night", [("Meowth-δ", 58, 60), ("Gloom-δ", 58, 60), ("Persian-δ", 61, 61), ("Pikachu-δ", 58, 58),
                           ("Oddish-δ", 58, 58), ("Vibrava-δ", 59, 59), ("Raichu-δ", 61, 61), ("Vileplume-δ", 63, 63),
                           ("Bellossom-δ", 63, 63), ("Flygon-δ", 63, 63), ("H:Castform", 60, 60), ("Pidgeot-δ", 63, 63)]),
        ("rock_smash", "any", [("Kabuto-δ", 58, 60), ("Omanyte-δ", 58, 60), ("Anorith-δ", 58, 58), ("Lileep-δ", 58, 58),
                               ("Kabutops-δ", 62, 62)]),
        ("water", "any", [("Psyduck-δ", 58, 60), ("Golduck-δ", 60, 62), ("Seadra-δ", 60, 60), ("Kingdra-δ", 63, 63),
                          ("Gyarados-δ", 63, 63)]),
        ("old_rod", "any", [("Magikarp-δ", 55, 55), ("Horsea-δ", 55, 55)]),
        ("good_rod", "any", [("Magikarp-δ", 58, 58), ("Horsea-δ", 58, 58), ("Feebas-δ", 58, 58)]),
        ("super_rod", "any", [("Gyarados-δ", 60, 60), ("Seadra-δ", 60, 60), ("Feebas-δ", 60, 60), ("Milotic-δ", 65, 65),
                              ("Kingdra-δ", 65, 65)]),
    ],
}

GIFTS = [  # not wild: suggested statics / gifts so nothing is a 1% grind
    ("Eevee-δ", 50, "Holon Research Tower: gift from a Holon Researcher (Eevee-δ has 8 evolutions; 1% wild alone is a grind)"),
    ("Gyarados-δ (shiny)", 65, "Holon Lake static, nod to the 'Shining Gyarados' of Holon Phantoms / Lake of Rage"),
]


def kind(sp):
    return "holon" if sp.startswith("H:") else "delta" if sp.endswith("-δ") else "normal"


def check():
    for m, tables in MAPS.items():
        for t, tod, slots in tables:
            assert len(slots) == len(RATES[t]), (m, t, len(slots))


def shares():
    res = {}
    for m, tables in MAPS.items():
        res[m] = {}
        for t, tod, slots in tables:
            d = {"delta": 0, "holon": 0, "normal": 0}
            for (sp, a, b), r in zip(slots, RATES[t]):
                d[kind(sp)] += r
            tot = sum(RATES[t])
            res[m][(t, tod)] = {k: round(100 * v / tot) for k, v in d.items()}
    return res


def coverage():
    """Every δ species must be wild, a gift, or reachable by evolving / breeding a wild δ."""
    names = {r["delta_name"]: r for r in DT.R if "delta_name" in r}
    fam_from = {r["name"] + "-δ": (r["frm"].title().replace("Farfetchd", "Farfetch'd") + "-δ" if r["frm"] else None) for r in DT.R}
    wild = {sp for tables in MAPS.values() for _, _, slots in tables for sp, _, _ in slots if sp.endswith("-δ")}
    wild |= {g[0].split(" ")[0] for g in GIFTS}

    def root(n):
        while fam_from.get(n):
            n = fam_from[n]
        return n
    have_family = {root(w) for w in wild}
    missing = [n for n in fam_from if root(n) not in have_family]
    not_wild = sorted(n for n in fam_from if n not in wild)
    return missing, not_wild, wild


def font(sz):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", sz)
    except OSError:
        return ImageFont.load_default()


def render(path):
    f, fs, fb = font(12), font(10), font(15)
    col_w = 470
    sh = shares()
    blocks = list(MAPS.items())
    colors = {"delta": (255, 236, 170), "holon": (200, 228, 255), "normal": (255, 255, 255)}
    # layout: 2 columns of maps
    heights = []
    for m, tables in blocks:
        h = 30
        for t, tod, slots in tables:
            h += 18 + len(slots) * 15 + 6
        heights.append(h)
    colH = [heights[0] + heights[2], heights[1] + heights[3]]
    W, H = col_w * 2 + 40, max(colH) + 150
    im = Image.new("RGB", (W, H), (250, 248, 244))
    dr = ImageDraw.Draw(im)
    dr.text((14, 8), "Holon wild tables — gold = Delta (δ), blue = Holon's Pokémon (plain species), white = normal", fill=(30, 30, 30), font=fb)
    pos = [(14, 34), (14 + col_w + 12, 34), (14, 34 + heights[0] + 10), (14 + col_w + 12, 34 + heights[1] + 10)]
    for (m, tables), (x0, y0) in zip(blocks, pos):
        dr.rectangle([x0, y0, x0 + col_w, y0 + 24], fill=(70, 60, 110))
        dr.text((x0 + 6, y0 + 4), m, fill=(255, 255, 255), font=fb)
        y = y0 + 30
        for t, tod, slots in tables:
            s = sh[m][(t, tod)]
            hdr = "%s%s   δ %d%%  ·  Holon's %d%%  ·  normal %d%%" % (t.replace("_", " "), "" if tod == "any" else " (%s)" % tod,
                                                                    s["delta"], s["holon"], s["normal"])
            dr.text((x0 + 4, y), hdr, fill=(90, 70, 40), font=f)
            y += 18
            for (sp, a, b), r in zip(slots, RATES[t]):
                k = kind(sp)
                dr.rectangle([x0 + 4, y, x0 + col_w - 4, y + 13], fill=colors[k])
                dr.text((x0 + 8, y), "%2d%%" % r, fill=(110, 110, 110), font=fs)
                dr.text((x0 + 44, y - 1), sp.replace("H:", ""), fill=(30, 30, 30), font=f)
                dr.text((x0 + 200, y - 1), "Lv %d" % a if a == b else "Lv %d-%d" % (a, b), fill=(60, 60, 60), font=f)
                y += 15
            y += 6
    y = max(colH) + 44
    missing, not_wild, wild = coverage()
    import textwrap
    lines = []
    for g in GIFTS:
        lines += textwrap.wrap("Gift / static: %s Lv %d — %s" % g, 165)
    lines += textwrap.wrap("Not wild (evolve / breed): " + ", ".join(not_wild), 165)
    for ln in lines:
        dr.text((14, y), ln, fill=(50, 50, 50), font=fs)
        y += 14
    dr.text((14, y + 4), "Coverage: %s" % ("every δ family has a wild or gift member" if not missing else "MISSING " + ", ".join(missing)),
            fill=(40, 120, 40) if not missing else (180, 30, 30), font=f)
    im.save(path)


def wrap_list(xs, n=14):
    return xs


def main():
    check()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(HERE, "wild_tables.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["map", "table", "time", "slot", "rate", "species", "min_lv", "max_lv", "kind"])
        for m, tables in MAPS.items():
            for t, tod, slots in tables:
                for i, ((sp, a, b), r) in enumerate(zip(slots, RATES[t])):
                    w.writerow([m, t, tod, i, r, sp.replace("H:", ""), a, b, kind(sp)])
    render(os.path.join(OUT, "wild_tables.png"))
    for m, d in shares().items():
        print(m, {"%s/%s" % k: v["delta"] for k, v in d.items()})
    missing, not_wild, wild = coverage()
    print("missing families:", missing)
    print("not wild:", len(not_wild), not_wild)


if __name__ == "__main__":
    DT.main.__globals__  # table module already populated R at import
    for r in DT.R:
        r.setdefault("delta_name", r["name"] + "-δ")
    main()
