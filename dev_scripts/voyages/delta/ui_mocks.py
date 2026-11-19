"""
δ names on the real Orchid UI mocks (dev_scripts/orchid_ui renderers, ROM fonts patched in memory
with the proposed δ glyph from glyph.py). Font choice copies the ROM's own fit rules:

  battle healthbox  GetFontIdToFit(FONT_SMALL, 55px)  small -> small_narrow -> small_narrower   (battle_interface.c)
  party slot        GetFontIdToFit(FONT_SMALL, 50px)                                           (party_menu.c)
  summary name      GetFontIdToFit(FONT_NORMAL, nameRight - 7)  normal -> narrow -> narrower   (pokemon_summary_screen.c)
  PC info name      FONT_NORMAL if <= OPC_NAME_W - 10 (66px) else FONT_NARROW (no 3rd step)   (pokemon_storage_system.c)
  Pokédex list      GetFontIdToFit(FONT_NARROW, ODEX_ROW_BALL_X - ODEX_ROW_NAME_X - 2 = 85px)  (pokedex.c)

usage: ui_mocks.py -> out/batch5_delta/ui_*.png + ui_fit_report.json
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "..", "out", "batch5_delta")
UI = os.path.join(ROOT, "dev_scripts", "orchid_ui")
sys.path.insert(0, UI)
sys.path.insert(0, HERE)

import glyph                                   # noqa: E402
import gamefont                                # noqa: E402

# ------------------------------------------------------------------ patch the ROM fonts with δ
_PATCHED = glyph.patched_fonts()
_KEEP = []
for fname, (im, W) in _PATCHED.items():
    short = fname.replace("latin_", "")
    _KEEP.append(im)
    gamefont._cache[short] = (im.load(), W)
cm = gamefont._charmap()
cm["δ"] = glyph.DELTA_CODE

CHAIN = {"small": "small_narrow", "small_narrow": "small_narrower", "normal": "narrow", "narrow": "narrower"}
REPORT = []


def fit(s, font, maxw):
    while True:
        nxt = CHAIN.get(font)
        if nxt is None or gamefont.text_width(s, font) <= maxw:
            return font
        font = nxt


def log(screen, s, font, maxw):
    w = gamefont.text_width(s, font)
    REPORT.append(dict(screen=screen, name=s, font=font, width=w, limit=maxw, clipped=w > maxw))


import mock_battle as MB                       # noqa: E402
import battle_ext as BX                        # noqa: E402
import mock_summary as MS                      # noqa: E402
import summary_ext as S                        # noqa: E402
import mock_party as MP                        # noqa: E402
import party_ext as PE                         # noqa: E402
import mock_pc as MPC                          # noqa: E402
import pc_ext as PC                            # noqa: E402
import mock_dex as MD                          # noqa: E402
import dex_ext as D                            # noqa: E402

# ------------------------------------------------------------------ fit-rule patches (mock -> ROM rule)
_orig_name_gender = BX.name_gender


def _name_gender(cv, x, y, mon, fg=BX.INK, sh=BX.PANEL_SHADE):
    font = fit(mon.name, "small", 55)
    log("battle healthbox", mon.name, font, 55)
    if mon.gender == "M":
        fg, sh = BX.HB_MALE, BX.HB_MALE_SH
    elif mon.gender == "F":
        fg, sh = BX.HB_FEMALE, BX.HB_FEMALE_SH
    return gamefont.draw_text(cv, x, y, mon.name, fg, sh, font=font)


BX.name_gender = _name_gender


def _wrap(screen, start, maxw_fn, names):
    def draw(cv, x, y, s, fg, shadow, font="normal", spacing=0, line_h=16):
        if s in names:
            maxw = maxw_fn()
            font = fit(s, start, maxw)
            log(screen, s, font, maxw)
        return gamefont.draw_text(cv, x, y, s, fg, shadow, font=font, spacing=spacing, line_h=line_h)
    return draw


NAMES = set()
_SUM_LV = [60]


def _summary_maxw():
    # nameRight = OSUM_LX + OSUM_LW - 5 - width(FONT_SMALL, "{LV}nn") - 2 ; limit = nameRight - (OSUM_LX + 5)
    _, widths = gamefont._font("small")
    lvw = widths[0x34] + gamefont.text_width(str(_SUM_LV[0]), "small")
    return (2 + 84 - 5 - lvw - 2) - (2 + 5)


MS.draw_text = _wrap("summary header", "normal", _summary_maxw, NAMES)
PE.draw_text = _wrap("party slot", "small", lambda: 50, NAMES)
MD.draw_text = _wrap("pokédex list", "narrow", lambda: 120 - 33 - 2, NAMES)

_orig_pc_info = PC.info_text


def _pc_info(tc, m, item_name=None):
    if m is not None:
        f = "normal" if gamefont.text_width(m["name"]) <= 76 - 10 else "narrow"
        log("PC box info", m["name"], f, 66 if f == "normal" else 76)
    return _orig_pc_info(tc, m, item_name)


PC.info_text = _pc_info
MPC.P.info_text = _pc_info

# ------------------------------------------------------------------ sprite offsets + Delta palettes
import re as _re                               # noqa: E402
import kit_ext as KX                           # noqa: E402


def _offsets(const):
    folder = os.path.join(ROOT, "src", "data", "pokemon", "species_info")
    for fn in sorted(os.listdir(folder)):
        txt = open(os.path.join(folder, fn)).read()
        m = _re.search(r"\[SPECIES_" + const + r"\]\s*=\s*\{(.*?)\n    \},", txt, _re.S)
        if m:
            def val(k):
                v = _re.search(r"\." + k + r"\s*=\s*([^,\n]+),", m.group(1)).group(1)
                t = _re.match(r"P_GBA_STYLE_SPECIES_GFX \? (\d+) : (\d+)", v.strip())
                return int(t.group(1)) if t else int(v)
            return dict(front_y=val("frontPicYOffset"), back_y=val("backPicYOffset"))
    return dict(front_y=8, back_y=8)


for _sp in ("gyarados", "kingdra", "charmeleon", "farfetchd"):
    BX.SPECIES[_sp] = _offsets(_sp.upper())

_DPAL = os.path.join(HERE, "palettes")
_orig_front, _orig_back = KX.mon_front, KX.mon_back


def _dpal(species):
    p = os.path.join(_DPAL, species + "_delta.pal")
    return KX.load_jasc(p) if os.path.exists(p) else None


def _front(species, frame=0, shiny=False):
    pal = _dpal(species)
    if pal is None or shiny:
        return _orig_front(species, frame, shiny)
    d = KX.G("pokemon", species)
    png = next(os.path.join(d, f) for f in ("anim_front_gba.png", "anim_front.png") if os.path.exists(os.path.join(d, f)))
    return KX.sprite_rgba(png, frame, 64, pal)


def _back(species):
    pal = _dpal(species)
    if pal is None:
        return _orig_back(species)
    d = KX.G("pokemon", species)
    png = os.path.join(d, "back_gba.png")
    if not os.path.exists(png):
        png = os.path.join(d, "back.png")
    return KX.sprite_rgba(png, 0, 64, pal)


KX.mon_front, KX.mon_back = _front, _back
BX.K.mon_front, BX.K.mon_back = _front, _back


# ------------------------------------------------------------------ Delta data
DELTAS = {   # name -> (folder/const, types, gender, level)
    "Gyarados-δ": ("gyarados", ["electric", "steel"], "M", 60),
    "Charmeleon-δ": ("charmeleon", ["electric"], "F", 36),
    "Farfetch'd-δ": ("farfetchd", ["steel"], "M", 55),
    "Kingdra-δ": ("kingdra", ["fire", "steel"], "F", 63),
}
NAMES.update(DELTAS)
NAMES.update({"Charizard-δ", "Dragonite-δ", "Pikachu-δ", "Eevee-δ", "Meowth-δ", "Klinklang-δ", "Gardevoir-δ"})


def save(im, name, k=3):
    im = im.convert("RGB")
    im.save(os.path.join(OUT, name + "_1x.png"))
    im.resize((im.width * k, im.height * k), Image.NEAREST).save(os.path.join(OUT, name + "_3x.png"))
    return im


def battle(player, enemy):
    p = DELTAS[player]
    e = DELTAS[enemy]
    pm = MB.Mon(p[0], player, p[3], 150, 182, p[2], exp=0.4)
    em = MB.Mon(e[0], enemy, e[3], 120, 140, e[2], caught=True)
    return MB.render(mode="action", player=pm, enemy=em)


def summary(name):
    sp, types, g, lv = DELTAS[name]
    _SUM_LV[0] = lv
    mon = S.Mon(species=sp, name=name, dex=1071, lv=lv, gender=g, types=types, item=None, item_name=None,
                ability="Intimidate", ability_desc="Lowers the foe's Attack.", met_place="Holon Lake", met_lv=lv)
    return MS.render_info(mon=mon)


def party(names):
    party = []
    for i, n in enumerate(names):
        sp, types, g, lv = DELTAS[n]
        party.append(dict(species=sp, pal=PC.pal_index(sp.upper()) if hasattr(PC, "pal_index") else 0, name=n,
                          sex=g.lower(), lv=lv, hp=100 - i * 20, maxhp=120))
    party += [MP.GROVYLE, MP.TAILLOW]
    while len(party) < 6:
        party.append(None)
    return MP.render(party=party[:6], cursor=0)


def pc(name):
    sp, types, g, lv = DELTAS[name]
    m = PC.mon(sp.upper(), g.lower(), lv, None, (), name)
    m["types"] = types
    contents = dict(PC.BOX1)
    contents[7] = m
    return MPC.render(box=0, cursor=("box", 7), contents_override=contents)


def dex(cursor_name):
    order = D.hoenn_order()
    base = len(order)
    tail = order[-4:]
    entries = [dict(num=base - 3 + i, const=c, seen=True, caught=True) for i, c in enumerate(tail)]
    for i, (n, (sp, types, g, lv)) in enumerate(
            [("Gyarados-δ", DELTAS["Gyarados-δ"]), ("Kingdra-δ", DELTAS["Kingdra-δ"]),
             ("Charmeleon-δ", DELTAS["Charmeleon-δ"]), ("Farfetch'd-δ", DELTAS["Farfetch'd-δ"]),
             ("Pikachu-δ", ("pikachu", ["steel"], None, 0))]):
        entries.append(dict(num=base + 1 + i, const=sp.upper(), seen=True, caught=i != 3, delta=n, types=types))
    _orig_info = D.species

    def info(e):
        try:
            sp = dict(_orig_info(e["const"]))
        except (KeyError, AttributeError):  # Orchid customs live in orchid_families.h (not parsed by dex_ext)
            sp = dict(name=e["const"].title(), types=["normal"], folder=e["const"].lower())
        if e.get("delta"):
            sp["name"] = e["delta"]
            sp["types"] = e["types"]
        return sp
    MD.info = info
    MD.ENTRIES = entries
    MD.LIST_LEN = len(entries)
    cur = next(i for i, e in enumerate(entries) if e.get("delta") == cursor_name)
    return MD.render_list(cursor=cur, top=0)


def font(sz):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", sz)
    except OSError:
        return ImageFont.load_default()


def overview(shots, path):
    """All screens at 1x (left) with a 3x zoom of the name area (right)."""
    f = font(13)
    rows = []
    for title, im, box in shots:
        z = im.crop(box)
        z = z.resize((z.width * 3, z.height * 3), Image.NEAREST)
        rows.append((title, im, z))
    W = 20 + 240 + 20 + max(z.width for _, _, z in rows) + 20
    H = 10 + sum(max(160, z.height) + 30 for _, _, z in rows)
    sheet = Image.new("RGB", (W, H), (34, 34, 42))
    dr = ImageDraw.Draw(sheet)
    y = 10
    for title, im, z in rows:
        dr.text((20, y), title, fill=(235, 235, 235), font=f)
        sheet.paste(im.convert("RGB"), (20, y + 20))
        sheet.paste(z.convert("RGB"), (280, y + 20))
        y += max(160, z.height) + 30
    sheet.save(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    shots = []
    b1 = save(battle("Gyarados-δ", "Kingdra-δ"), "ui_battle_gyarados")
    shots.append(("Battle healthboxes: Gyarados-δ (player) vs Kingdra-δ", b1, (0, 0, 240, 112)))
    b2 = save(battle("Charmeleon-δ", "Farfetch'd-δ"), "ui_battle_12char")
    shots.append(("Battle healthboxes, 12-char worst case: Charmeleon-δ vs Farfetch'd-δ", b2, (0, 0, 240, 112)))
    s1 = save(summary("Gyarados-δ"), "ui_summary_gyarados")
    shots.append(("Summary (INFO): Gyarados-δ", s1, (0, 96, 90, 120)))
    s2 = save(summary("Charmeleon-δ"), "ui_summary_12char")
    shots.append(("Summary (INFO): Charmeleon-δ", s2, (0, 96, 90, 120)))
    p1 = save(party(["Gyarados-δ", "Charmeleon-δ", "Farfetch'd-δ", "Kingdra-δ"]), "ui_party")
    shots.append(("Party: Gyarados-δ (lead), Charmeleon-δ, Farfetch'd-δ, Kingdra-δ", p1, (0, 0, 240, 112)))
    c1 = save(pc("Gyarados-δ"), "ui_pc_gyarados")
    shots.append(("PC box info: Gyarados-δ", c1, (0, 70, 80, 110)))
    c2 = save(pc("Charmeleon-δ"), "ui_pc_12char")
    shots.append(("PC box info: Charmeleon-δ", c2, (0, 70, 80, 110)))
    d1 = save(dex("Gyarados-δ"), "ui_dex_list")
    shots.append(("Pokédex list (Tosa order, Deltas appended after Laomeow)", d1, (100, 14, 240, 160)))
    overview(shots, os.path.join(OUT, "ui_overview.png"))
    seen = {}
    for r in REPORT:
        seen[(r["screen"], r["name"])] = r
    rep = sorted(seen.values(), key=lambda r: (r["screen"], r["name"]))
    json.dump(rep, open(os.path.join(HERE, "ui_fit_report.json"), "w"), indent=1, ensure_ascii=False)
    for r in rep:
        print("%-18s %-14s %-15s %3d/%3d %s" % (r["screen"], r["name"], r["font"], r["width"], r["limit"],
                                               "CLIPPED" if r["clipped"] else ""))


if __name__ == "__main__":
    main()
