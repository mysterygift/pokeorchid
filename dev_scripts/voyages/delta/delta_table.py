"""
Delta Species (δ) master table — design review, batch 5.

Sources:
  user = dev_scripts/voyages/delta_requests.md (2026-11-19)
  TCG  = EX Delta Species (DS), Holon Phantoms (HP), Crystal Guardians (CG), Dragon Frontiers (DF)
         card types taken from the pkmncards.com "is:delta-species" listing (191 cards), cross-checked
         with Bulbapedia's Holon page (Magikarp δ Metal -> Gyarados δ Lightning/Metal; Anorith δ Metal ->
         Armaldo δ Fighting/Metal; Meowth δ dual Metal).
  extrap = no δ card for that stage; type extrapolated so the line stays Delta.

TCG -> game type mapping: Lightning=Electric, Metal=Steel, Darkness=Dark, Colorless=Normal,
Fighting=Fighting (Rock for Armaldo, whose normal TCG type is Fighting), Psychic/Grass/Fire/Water as-is.

usage: delta_table.py  -> delta/delta_table.csv, out/batch5_delta/delta_table.png, delta/summary.json
"""
import csv
import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "out", "batch5_delta")

# line, BASE, Name, type1, type2, evolves-from BASE (None = first stage), source, tier, TCG card, confidence, home map
#   confidence: high = δ card with that type exists; med = card exists but the game-type mapping is a judgement call;
#               extrap = no card for this stage; user = user's choice (TCG noted when it differs)
R = []


def L(line, tier, home, *rows):
    for r in rows:
        base, name, t1, t2, frm, src, card, conf = r
        R.append(dict(line=line, tier=tier, home=home, base=base, name=name, t1=t1, t2=t2 or "",
                      frm=frm or "", source=src, card=card, conf=conf))


# ------------------------------------------------------------------ user lines
L("Stantler", "A", "Village", ("STANTLER", "Stantler", "Psychic", None, None, "user", "-", "user"))
L("Ralts", "A", "Village",
  ("RALTS", "Ralts", "Grass", None, None, "user", "TCG DF Ralts δ = Fire", "user"),
  ("KIRLIA", "Kirlia", "Grass", None, "RALTS", "user", "TCG DF Kirlia δ = Fire", "user"),
  ("GARDEVOIR", "Gardevoir", "Grass", None, "KIRLIA", "user", "TCG DS Gardevoir δ Psychic/Metal; DF Gardevoir ex δ Fire", "user"),
  ("GALLADE", "Gallade", "Grass", None, "KIRLIA", "user (open pt 1)", "no card", "user"))
L("Dratini", "A", "Village",
  ("DRATINI", "Dratini", "Electric", None, None, "user", "DS Dratini δ Lightning", "high"),
  ("DRAGONAIR", "Dragonair", "Electric", None, "DRATINI", "user", "DS Dragonair δ Lightning", "high"),
  ("DRAGONITE", "Dragonite", "Electric", None, "DRAGONAIR", "user", "DS Dragonite δ Lightning/Metal (Q: add Steel?)", "user"))
L("Purrloin", "A", "Village",
  ("PURRLOIN", "Purrloin", "Fairy", None, None, "user", "-", "user"),
  ("LIEPARD", "Liepard", "Fairy", None, "PURRLOIN", "user (open pt 2)", "-", "user"))
L("Glameow", "A", "Village",
  ("GLAMEOW", "Glameow", "Fairy", None, None, "user", "-", "user"),
  ("PURUGLY", "Purugly", "Fairy", None, "GLAMEOW", "user (open pt 2)", "-", "user"))
L("Drifloon", "A", "Village",
  ("DRIFLOON", "Drifloon", "Flying", "Fire", None, "user", "-", "user"),
  ("DRIFBLIM", "Drifblim", "Flying", "Fire", "DRIFLOON", "user", "-", "user"))
L("Klink", "A", "Tower",
  ("KLINK", "Klink", "Rock", "Ice", None, "user", "-", "user"),
  ("KLANG", "Klang", "Rock", "Ice", "KLINK", "user", "-", "user"),
  ("KLINKLANG", "Klinklang", "Rock", "Ice", "KLANG", "user", "-", "user"))
L("Farfetch'd", "A", "Village", ("FARFETCHD", "Farfetch'd", "Steel", None, None, "user", "-", "user"))
L("Pancham", "A", "Village",
  ("PANCHAM", "Pancham", "Psychic", None, None, "user", "-", "user"),
  ("PANGORO", "Pangoro", "Psychic", None, "PANCHAM", "user", "-", "user"))
L("Relicanth", "A", "Coast", ("RELICANTH", "Relicanth", "Grass", "Ground", None, "user", "-", "user"))

# ------------------------------------------------------------------ EX Delta Species (Holon village / tower)
L("Larvitar", "A", "Village",
  ("LARVITAR", "Larvitar", "Fire", None, None, "TCG DS", "DS Larvitar δ Fire", "high"),
  ("PUPITAR", "Pupitar", "Fire", None, "LARVITAR", "TCG DS", "DS Pupitar δ Fire", "high"),
  ("TYRANITAR", "Tyranitar", "Fire", "Steel", "PUPITAR", "TCG DS", "DS Tyranitar δ Fire/Metal (DF ex δ = Lightning)", "high"))
L("Bagon", "A", "Village",
  ("BAGON", "Bagon", "Fire", None, None, "TCG DS", "DS Bagon δ Fire (DF = Water)", "high"),
  ("SHELGON", "Shelgon", "Fire", None, "BAGON", "TCG DS", "DS Shelgon δ Fire", "high"),
  ("SALAMENCE", "Salamence", "Fire", "Steel", "SHELGON", "TCG DS", "DS Salamence δ Fire/Metal (DF ex δ = Water)", "high"))
L("Beldum", "A", "Tower",
  ("BELDUM", "Beldum", "Electric", None, None, "TCG DS", "DS Beldum δ Lightning", "high"),
  ("METANG", "Metang", "Electric", None, "BELDUM", "TCG DS", "DS Metang δ Lightning", "high"),
  ("METAGROSS", "Metagross", "Electric", "Steel", "METANG", "TCG DS", "DS Metagross δ Lightning/Metal", "high"))
L("Eevee", "A", "Tower",
  ("EEVEE", "Eevee", "Steel", None, None, "TCG DS", "DS Eevee δ Metal", "high"),
  ("VAPOREON", "Vaporeon", "Water", "Steel", "EEVEE", "TCG DS", "DS Vaporeon δ Water/Metal", "high"),
  ("JOLTEON", "Jolteon", "Electric", "Steel", "EEVEE", "TCG DS", "DS Jolteon δ Lightning/Metal", "high"),
  ("FLAREON", "Flareon", "Fire", "Steel", "EEVEE", "TCG DS", "DS Flareon δ Fire/Metal", "high"),
  ("ESPEON", "Espeon", "Psychic", "Steel", "EEVEE", "TCG DS", "DS Espeon δ Psychic/Metal", "high"),
  ("UMBREON", "Umbreon", "Dark", "Steel", "EEVEE", "TCG DS", "DS Umbreon δ Darkness/Metal", "high"),
  ("LEAFEON", "Leafeon", "Grass", "Steel", "EEVEE", "extrap", "no card (Gen 4) - DS pattern: own type + Steel", "extrap"),
  ("GLACEON", "Glaceon", "Ice", "Steel", "EEVEE", "extrap", "no card (Gen 4) - DS pattern", "extrap"),
  ("SYLVEON", "Sylveon", "Fairy", "Steel", "EEVEE", "extrap", "no card (Gen 6) - DS pattern", "extrap"))

# ------------------------------------------------------------------ Holon Phantoms (Holon Lake)
L("Magikarp", "A", "Lake",
  ("MAGIKARP", "Magikarp", "Steel", None, None, "TCG HP", "HP Magikarp δ Metal", "high"),
  ("GYARADOS", "Gyarados", "Electric", "Steel", "MAGIKARP", "TCG HP", "HP Gyarados δ Lightning/Metal", "high"))
L("Pichu", "A", "Lake",
  ("PICHU", "Pichu", "Steel", None, None, "TCG HP", "HP Pichu δ Metal", "high"),
  ("PIKACHU", "Pikachu", "Steel", None, "PICHU", "TCG HP", "HP/LM Pikachu δ Metal", "high"),
  ("RAICHU", "Raichu", "Steel", None, "PIKACHU", "TCG HP", "HP Raichu δ Metal", "high"))
L("Horsea", "A", "Lake",
  ("HORSEA", "Horsea", "Fire", None, None, "TCG HP", "HP Horsea δ Fire (DF = Fighting)", "high"),
  ("SEADRA", "Seadra", "Fire", None, "HORSEA", "TCG HP", "HP Seadra δ Fire", "high"),
  ("KINGDRA", "Kingdra", "Fire", "Steel", "SEADRA", "TCG HP", "HP Kingdra δ Fire/Metal", "high"))
L("Trapinch", "A", "Lake",
  ("TRAPINCH", "Trapinch", "Grass", None, None, "TCG HP", "HP Trapinch δ Grass (DF = Psychic)", "high"),
  ("VIBRAVA", "Vibrava", "Grass", None, "TRAPINCH", "TCG HP", "HP Vibrava δ Grass", "high"),
  ("FLYGON", "Flygon", "Grass", "Steel", "VIBRAVA", "TCG HP", "HP Flygon δ Grass/Metal", "high"))
L("Meowth", "A", "Lake",
  ("MEOWTH", "Meowth", "Dark", "Steel", None, "TCG HP", "HP Meowth δ Darkness/Metal", "high"),
  ("PERSIAN", "Persian", "Dark", "Steel", "MEOWTH", "TCG HP", "HP Persian δ Darkness/Metal", "high"))
L("Pidgey", "B", "Lake",
  ("PIDGEY", "Pidgey", "Electric", None, None, "TCG HP", "HP Pidgey δ Lightning", "high"),
  ("PIDGEOTTO", "Pidgeotto", "Electric", None, "PIDGEY", "TCG HP", "HP Pidgeotto δ Lightning", "high"),
  ("PIDGEOT", "Pidgeot", "Electric", "Steel", "PIDGEOTTO", "TCG HP", "HP Pidgeot δ Lightning/Metal", "high"))
L("Psyduck", "B", "Lake",
  ("PSYDUCK", "Psyduck", "Electric", None, None, "TCG HP", "HP Psyduck δ Lightning", "high"),
  ("GOLDUCK", "Golduck", "Electric", None, "PSYDUCK", "TCG HP", "HP Golduck δ Lightning", "high"))
L("Oddish", "B", "Lake",
  ("ODDISH", "Oddish", "Water", None, None, "TCG HP", "HP Oddish δ Water", "high"),
  ("GLOOM", "Gloom", "Psychic", None, "ODDISH", "TCG HP", "HP Gloom δ Psychic (TCG Psychic also = Poison)", "med"),
  ("VILEPLUME", "Vileplume", "Psychic", "Steel", "GLOOM", "TCG HP", "HP Vileplume δ Psychic/Metal", "med"),
  ("BELLOSSOM", "Bellossom", "Water", None, "GLOOM", "TCG HP", "HP Bellossom δ Water", "high"))
L("Kabuto", "B", "Lake",
  ("KABUTO", "Kabuto", "Electric", None, None, "TCG HP", "HP Kabuto δ Lightning", "high"),
  ("KABUTOPS", "Kabutops", "Electric", None, "KABUTO", "TCG HP", "HP Kabutops δ Lightning", "high"))
L("Omanyte", "B", "Lake",
  ("OMANYTE", "Omanyte", "Psychic", None, None, "TCG HP", "HP Omanyte δ Psychic", "high"),
  ("OMASTAR", "Omastar", "Psychic", None, "OMANYTE", "TCG HP", "HP Omastar δ Psychic", "high"))
L("Anorith", "B", "Lake",
  ("ANORITH", "Anorith", "Steel", None, None, "TCG HP", "HP Anorith δ Metal", "high"),
  ("ARMALDO", "Armaldo", "Rock", "Steel", "ANORITH", "TCG HP", "HP Armaldo δ Fighting/Metal (Fighting read as Rock)", "med"))
L("Lileep", "B", "Lake",
  ("LILEEP", "Lileep", "Dark", None, None, "TCG HP", "HP Lileep δ Darkness", "high"),
  ("CRADILY", "Cradily", "Dark", "Steel", "LILEEP", "TCG HP", "HP Cradily δ Darkness/Metal", "high"))

# ------------------------------------------------------------------ Crystal Guardians (coast / island)
L("Charmander", "A", "Coast",
  ("CHARMANDER", "Charmander", "Electric", None, None, "TCG CG", "CG Charmander δ Lightning", "high"),
  ("CHARMELEON", "Charmeleon", "Electric", None, "CHARMANDER", "TCG CG", "CG Charmeleon δ Lightning", "high"),
  ("CHARIZARD", "Charizard", "Electric", "Steel", "CHARMELEON", "TCG CG", "CG Charizard δ Lightning/Metal", "high"))
L("Treecko", "B", "Coast",
  ("TREECKO", "Treecko", "Psychic", None, None, "TCG CG", "CG Treecko δ Psychic", "high"),
  ("GROVYLE", "Grovyle", "Psychic", None, "TREECKO", "TCG CG", "CG Grovyle δ Psychic", "high"),
  ("SCEPTILE", "Sceptile", "Psychic", None, "GROVYLE", "TCG CG", "CG Sceptile ex δ Psychic", "high"))
L("Krabby", "B", "Coast",
  ("KRABBY", "Krabby", "Fire", None, None, "extrap", "no card (CG: final stage only)", "extrap"),
  ("KINGLER", "Kingler", "Fire", "Steel", "KRABBY", "TCG CG", "CG Kingler δ Fire/Metal", "high"))
L("Wingull", "B", "Coast",
  ("WINGULL", "Wingull", "Electric", None, None, "extrap", "no card (CG: final stage only)", "extrap"),
  ("PELIPPER", "Pelipper", "Electric", None, "WINGULL", "TCG CG", "CG Pelipper δ Lightning", "high"))

# ------------------------------------------------------------------ Dragon Frontiers (no Steel)
L("Feebas", "A", "Lake",
  ("FEEBAS", "Feebas", "Fire", None, None, "TCG DF", "DF Feebas δ Fire", "high"),
  ("MILOTIC", "Milotic", "Fire", None, "FEEBAS", "TCG DF", "DF Milotic δ Fire", "high"))
L("Swablu", "B", "Coast",
  ("SWABLU", "Swablu", "Water", None, None, "TCG DF", "DF Swablu δ Water", "high"),
  ("ALTARIA", "Altaria", "Water", None, "SWABLU", "TCG DF", "DF Altaria ex δ Water", "high"))
L("Mareep", "B", "Coast",
  ("MAREEP", "Mareep", "Normal", None, None, "TCG DF", "DF Mareep δ Colorless", "med"),
  ("FLAAFFY", "Flaaffy", "Normal", None, "MAREEP", "TCG DF", "DF Flaaffy δ Colorless", "med"),
  ("AMPHAROS", "Ampharos", "Normal", None, "FLAAFFY", "TCG DF", "DF Ampharos δ Colorless", "med"))
L("Totodile", "B", "Coast",
  ("TOTODILE", "Totodile", "Electric", None, None, "TCG DF", "DF Totodile δ Lightning", "high"),
  ("CROCONAW", "Croconaw", "Electric", None, "TOTODILE", "TCG DF", "DF Croconaw δ Lightning", "high"),
  ("FERALIGATR", "Feraligatr", "Electric", None, "CROCONAW", "TCG DF", "DF Feraligatr δ Lightning", "high"))
L("Vulpix", "B", "Coast",
  ("VULPIX", "Vulpix", "Psychic", None, None, "TCG DF", "DF Vulpix δ Psychic", "high"),
  ("NINETALES", "Ninetales", "Psychic", None, "VULPIX", "TCG DF", "DF Ninetales δ Psychic", "high"))

TYPE_RGB = {
    "Normal": (168, 168, 120), "Fire": (240, 128, 48), "Water": (104, 144, 240), "Electric": (248, 208, 48),
    "Grass": (120, 200, 80), "Ice": (152, 216, 216), "Fighting": (192, 48, 40), "Poison": (160, 64, 160),
    "Ground": (224, 192, 104), "Flying": (168, 144, 240), "Psychic": (248, 88, 136), "Bug": (168, 184, 32),
    "Rock": (184, 160, 56), "Ghost": (112, 88, 152), "Dragon": (112, 56, 248), "Dark": (112, 88, 72),
    "Steel": (184, 184, 208), "Fairy": (238, 153, 172),
}


def species_consts():
    txt = open(os.path.join(ROOT, "include", "constants", "species.h")).read()
    ids = {}
    for m in re.finditer(r"SPECIES_([A-Z0-9_]+)\s*=\s*(\d+)", txt):
        ids[m.group(1)] = int(m.group(2))
    return ids, txt


def base_types():
    """speciesName -> types from species_info headers (first match per SPECIES_X)."""
    d = {}
    folder = os.path.join(ROOT, "src", "data", "pokemon", "species_info")
    for fn in sorted(os.listdir(folder)):
        txt = open(os.path.join(folder, fn)).read()
        for m in re.finditer(r"\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},", txt, re.S):
            if m.group(1) in d:
                continue
            t = re.search(r"\.types\s*=\s*MON_TYPES\(([^)]*)\)", m.group(2))
            if t:
                toks = []
                for x in t.group(1).split(","):
                    x = x.strip()
                    mm = re.search(r"#define " + x + r" \(.*?\? (TYPE_[A-Z]+) :", txt)
                    toks.append((mm.group(1) if mm else x).replace("TYPE_", "").title())
                d[m.group(1)] = toks
    return d


def main():
    os.makedirs(OUT, exist_ok=True)
    ids, sp_txt = species_consts()
    btypes = base_types()
    problems = []
    rows = []
    for r in R:
        if r["base"] not in ids:
            problems.append("missing SPECIES_%s" % r["base"])
        full = r["name"] + "-δ"
        r["delta_name"] = full
        r["len"] = len(full)
        if len(full) > 12:
            problems.append("%s is %d chars" % (full, len(full)))
        r["const"] = "SPECIES_%s_DELTA" % r["base"]
        r["frm_const"] = ("SPECIES_%s_DELTA" % r["frm"]) if r["frm"] else ""
        bt = btypes.get(r["base"], [])
        r["base_types"] = "/".join(dict.fromkeys(bt))
        if sorted(set(bt)) == sorted({r["t1"], r["t2"]} - {""}):
            problems.append("%s keeps its normal typing" % full)
        rows.append(r)
    with open(os.path.join(HERE, "delta_table.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["base_species", "delta_species", "delta_name", "chars", "type1", "type2", "evolves_from",
                    "base_types", "line", "tier", "home_map", "source", "tcg_card", "confidence"])
        for r in rows:
            w.writerow(["SPECIES_" + r["base"], r["const"], r["delta_name"], r["len"], r["t1"], r["t2"], r["frm_const"],
                        r["base_types"], r["line"], r["tier"], r["home"], r["source"], r["card"], r["conf"]])
    max_id = max(v for k, v in ids.items() if k not in ("SHINY_TAG",))
    custom = re.search(r"SPECIES_CUSTOM_START = SPECIES_GLIMMORA_MEGA,(.*?)SPECIES_CUSTOM_END,", sp_txt, re.S).group(1)
    n_custom = len(re.findall(r"SPECIES_[A-Z0-9_]+,", custom))
    laomeow = ids["GLIMMORA_MEGA"] + n_custom
    lines = {}
    for r in rows:
        lines.setdefault(r["line"], []).append(r)
    summ = {
        "species_total": len(rows),
        "lines_total": len(lines),
        "user_species": sum(1 for r in rows if r["source"].startswith("user")),
        "tcg_species": sum(1 for r in rows if r["source"].startswith("TCG")),
        "extrap_species": sum(1 for r in rows if r["source"] == "extrap"),
        "tierA_species": sum(1 for r in rows if r["tier"] == "A"),
        "tierB_species": sum(1 for r in rows if r["tier"] == "B"),
        "tierA_lines": sum(1 for v in lines.values() if v[0]["tier"] == "A"),
        "tierB_lines": sum(1 for v in lines.values() if v[0]["tier"] == "B"),
        "longest_names": sorted({(r["len"], r["delta_name"]) for r in rows}, reverse=True)[:6],
        "last_enum_species_id": {"SPECIES_GLIMMORA_MEGA": ids["GLIMMORA_MEGA"], "SPECIES_LAOMEOW": laomeow,
                                 "SPECIES_EGG/NUM_SPECIES": laomeow + 1},
        "after_all_deltas": {"last_delta_id": laomeow + len(rows), "NUM_SPECIES": laomeow + len(rows) + 1,
                             "headroom_to_2047": 2047 - (laomeow + len(rows) + 1)},
        "national_dex": {"NATIONAL_DEX_LAOMEOW": 1030, "last_delta": 1030 + len(rows)},
        "dex_flag_bytes_added_each_of_seen_caught": (1030 + len(rows) + 1 + 7) // 8 - (1030 + 1 + 7) // 8,
        "problems": problems,
    }
    json.dump(summ, open(os.path.join(HERE, "summary.json"), "w"), indent=1, ensure_ascii=False)
    render(rows, summ, os.path.join(OUT, "delta_table.png"))
    print(json.dumps(summ, indent=1, ensure_ascii=False))


def font(sz, bold=False):
    for p in ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf",):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def chip(dr, x, y, t, f):
    if not t:
        return
    c = TYPE_RGB.get(t, (128, 128, 128))
    dr.rounded_rectangle([x, y, x + 62, y + 17], 4, fill=c)
    dr.text((x + 31, y + 9), t.upper(), fill=(255, 255, 255) if sum(c) < 520 else (40, 40, 40), font=f, anchor="mm")


def render(rows, summ, path):
    f, fb, fs = font(13), font(14), font(10)
    cols = [("#", 34), ("Delta name", 116), ("Delta type", 132), ("Base type", 128), ("Evolves from", 120),
            ("Tier", 34), ("Home", 60), ("Source", 92), ("TCG card / note", 400), ("Conf", 52)]
    rh = 21
    half = (len(rows) + 1) // 2
    tw = sum(c[1] for c in cols)
    W = tw * 2 + 40
    H = 74 + half * rh + 20
    im = Image.new("RGB", (W, H), (250, 248, 244))
    dr = ImageDraw.Draw(im)
    dr.text((14, 10), "Delta Species (δ) — %d species in %d lines (tier A %d / B %d species). User %d, TCG %d, extrapolated %d."
            % (summ["species_total"], summ["lines_total"], summ["tierA_species"], summ["tierB_species"],
               summ["user_species"], summ["tcg_species"], summ["extrap_species"]), fill=(30, 30, 30), font=fb)
    dr.text((14, 30), "National #1031-#%d, after Laomeow. All names ≤ 12 chars (longest: %s). Grey rows = tier B (optional)."
            % (summ["national_dex"]["last_delta"], ", ".join("%s %d" % (n, l) for l, n in summ["longest_names"][:3])),
            fill=(80, 80, 80), font=f)
    conf_col = {"high": (40, 140, 60), "med": (190, 130, 0), "extrap": (170, 60, 160), "user": (40, 90, 190)}
    for half_i in range(2):
        x0 = 14 + half_i * (tw + 12)
        y = 52
        x = x0
        for name, w in cols:
            dr.text((x + 3, y), name, fill=(90, 90, 90), font=fs)
            x += w
        y += 16
        for i, r in enumerate(rows[half_i * half:(half_i + 1) * half]):
            n = half_i * half + i
            bg = (255, 255, 255) if r["tier"] == "A" else (232, 230, 226)
            if i and r["line"] != rows[n - 1]["line"]:
                dr.line([x0, y - 1, x0 + tw, y - 1], fill=(170, 160, 150))
            dr.rectangle([x0, y, x0 + tw, y + rh - 2], fill=bg)
            x = x0
            vals = [str(1031 + n), r["delta_name"], None, None, (r["frm"].title() + "-δ") if r["frm"] else "—",
                    r["tier"], r["home"], r["source"], r["card"], r["conf"]]
            for (cname, w), v in zip(cols, vals):
                if cname == "Delta type":
                    chip(dr, x + 2, y + 1, r["t1"], fs)
                    chip(dr, x + 66, y + 1, r["t2"], fs)
                elif cname == "Base type":
                    bt = r["base_types"].split("/")
                    chip(dr, x + 2, y + 1, bt[0] if bt else "", fs)
                    chip(dr, x + 64, y + 1, bt[1] if len(bt) > 1 else "", fs)
                else:
                    col = conf_col.get(v, (30, 30, 30)) if cname == "Conf" else (30, 30, 30)
                    dr.text((x + 3, y + 2), v, fill=col, font=f if cname != "TCG card / note" else fs)
                x += w
            y += rh
    im.save(path)


if __name__ == "__main__":
    main()
