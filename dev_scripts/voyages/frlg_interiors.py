"""
Sevii interiors: FRLG -> Emerald design-review mockups (Sailor's Voyages; user decision 8 "translate the FRLG
layouts the same way"). Nothing under data/ src/ include/ graphics/ is touched; no tileset is edited.

Every FRLG room is redrawn cell for cell at the SAME size in an Emerald tileset pair (FRLG cells need the FRLG
primary, so they cannot be used). Houses are hand-translated by furniture class (wall, base row, floor, strip,
plant, shelf, cabinet, sink, fridge, table + chairs, rug, bed, exit mat, black bottom row) into real vanilla
Emerald metatiles of the pair (collision taken from the vanilla cells, forced where FRLG's walk layout needs
it); warps stay on FRLG's cells, objects keep FRLG's cells (FRLG-only gfx swapped for Emerald look-alikes).

  harbours  ONE..SEVEN_ISLAND_HARBOR = FRLG LAYOUT_ISLAND_HARBOR_FRLG, which is the room Emerald already ships
            as LAYOUT_ISLAND_HARBOR (Birth Island / Navel Rock harbour, General + IslandHarbor, 17x13): rendered
            as-is with the Sevii warps / sailor / boat (clone, nothing to translate).
  houses    ROOMS below (one render per distinct FRLG layout; LAYOUT_HOUSE3_FRLG serves 13 maps).
  caves     interiors_caves.py (Ember Spa, Mt. Ember paths, Dunsparce Tunnel, Dotted Hole, Tanoby).

Each output: out/interiors/<snake>.png, @2x.png, _vs_frlg.png (FRLG | Emerald), _spec.json (spec + report:
pair, size, warps, objects with Emerald gfx, walk diff vs FRLG, seams, layouts sharing the secondary).

usage: <venv python> dev_scripts/voyages/frlg_interiors.py [harbor] [ROOMKEY ...]   (default: everything)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc            # noqa: E402
import frlg_translate as ft            # noqa: E402

OUT = os.path.join(HERE, "out", "interiors")
HOUSE = ("gTileset_Building", "gTileset_GenericBuilding")
DAYCARE = ("gTileset_Building", "gTileset_PokemonDayCare")
HARBOR = ("gTileset_General", "gTileset_IslandHarbor")

# FRLG people -> Emerald gfx (mockup sprite key, Emerald OBJ_EVENT_GFX_*). ft.swap_gfx covers the *_FRLG ones.
_PEOPLE = "graphics/object_events/pics/people/"
_DOLL = "graphics/object_events/pics/dolls/"
for _k, _v in {
        "glacia": (_PEOPLE + "elite_four/glacia.png", 16, 32, 0, False),
        "old_woman_l": (_PEOPLE + "old_woman.png", 16, 32, 2, False),
        "old_woman_r": (_PEOPLE + "old_woman.png", 16, 32, 2, True),
        "old_man_r": (_PEOPLE + "old_man.png", 16, 32, 2, True),
        "fat_man": (_PEOPLE + "fat_man.png", 16, 32, 0, False),
        "hex_maniac": (_PEOPLE + "hex_maniac.png", 16, 32, 0, False),
        "guitarist": (_PEOPLE + "man_5.png", 16, 32, 0, False),
        "gentleman": (_PEOPLE + "gentleman.png", 16, 32, 0, False),
        "scientist": (_PEOPLE + "scientist_1.png", 16, 32, 0, False),
        "black_belt": (_PEOPLE + "black_belt.png", 16, 32, 0, False),
        "pikachu_doll": (_DOLL + "pikachu_doll.png", 16, 16, 0, False),
        "jigglypuff_doll": (_DOLL + "jigglypuff_doll.png", 16, 16, 0, False),
        "meowth_doll": (_DOLL + "meowth_doll.png", 16, 16, 0, False)}.items():
    vc.SPRITES.setdefault(_k, _v)
# FRLG-only gfx (invisible in this build) -> (Emerald OBJ_EVENT_GFX_ suffix, mockup sprite)
EXTRA_GFX = {"LORELEI": ("GLACIA", "glacia"), "CHANNELER": ("HEX_MANIAC", "hex_maniac"),
             "OLD_WOMAN_FRLG": ("OLD_WOMAN", "old_woman"), "LASS_FRLG": ("LASS", "lass"),
             "FAT_MAN_FRLG": ("FAT_MAN", "fat_man"), "ROCKER": ("MAN_5", "guitarist"),
             "GENTLEMAN_FRLG": ("GENTLEMAN", "gentleman"), "SCIENTIST": ("SCIENTIST_1", "scientist"),
             "BLACKBELT": ("BLACK_BELT", "black_belt"), "SEAGALLOP": ("MR_BRINEYS_BOAT (decision 1)", "boat"),
             "VAR_0": ("VAR_0 (e-Reader trainer)", "man"), "CHANSEY": ("CHANSEY (FRLG-only: needs gfx)", None),
             "RUBY": ("RUBY (FRLG-only: needs gfx)", None), "SAPPHIRE": ("SAPPHIRE (FRLG-only: needs gfx)", None)}
# Lorelei's dolls: Emerald has Pikachu / Jigglypuff / Meowth dolls (and BIG_LAPRAS_DOLL, 32x32); the rest have no
# Emerald doll gfx (open question).
DOLLS = {"PIKACHU_FRLG": ("PIKACHU_DOLL", "pikachu_doll"), "JIGGLYPUFF": ("JIGGLYPUFF_DOLL", "jigglypuff_doll"),
         "MEOWTH": ("MEOWTH_DOLL", "meowth_doll"), "LAPRAS_DOLL": ("BIG_LAPRAS_DOLL? (32x32)", None)}
DOLL_NONE = {"WIGGLYTUFF", "SEEL", "SLOWPOKE", "SLOWBRO", "PSYDUCK", "CHANSEY", "NIDORAN_F", "NIDORAN_M", "PIDGEOT",
             "FEAROW"}


# ================================================================================================ cells
def raw(mid, ts, coll=None):
    """Raw block value of metatile `mid` as some vanilla same-pair cell has it (most common collision /
    elevation), collision forced to `coll` when given (mockup: the walk layout is FRLG's)."""
    v = vc.ref_value(("id", mid), ts)
    if coll is not None:
        v = (v & ~0xC00) | (coll << 10)
    return v


def parse_grid(text, ts):
    """Rows of tokens: 3-hex-digit metatile id, '*' suffix = force solid, '.' suffix = force passable."""
    rows = [r.split() for r in text.strip("\n").splitlines() if r.strip()]
    g = []
    for r in rows:
        out = []
        for t in r:
            coll = 1 if t.endswith("*") else 0 if t.endswith(".") else None
            out.append(raw(int(t.rstrip("*."), 16), ts, coll))
        g.append(out)
    return g


def grid_spec(g, ts):
    """A voyage_compose spec that reproduces grid g exactly (one ('raw', v) cell per position)."""
    return dict(size=(len(g[0]), len(g)), tileset=ts, ground=("raw", g[0][0]),
                cells=[(x, y, ("raw", v)) for y, row in enumerate(g) for x, v in enumerate(row)])


def walk_diff(fm, g):
    """Cells whose passability differs from FRLG's (collision bit only)."""
    out = []
    for y in range(fm.h):
        for x in range(fm.w):
            a, b = bool(fm.coll(x, y)), bool((g[y][x] >> 10) & 3)
            if a != b:
                out.append(dict(x=x, y=y, frlg="solid" if a else "open", emerald="solid" if b else "open"))
    return out


# ================================================================================================ events
def emerald_gfx(gid, script=""):
    """FRLG graphics id -> (Emerald OBJ_EVENT_GFX_ suffix, mockup mark kind, sprite key or None)."""
    base = gid.replace("OBJ_EVENT_GFX_", "")
    if "Doll" in (script or ""):
        if base in DOLLS:
            eg, spr = DOLLS[base]
            return eg, ("npc" if spr else "note"), spr
        return base + " doll (no Emerald gfx)", "note", None
    if base in EXTRA_GFX:
        eg, spr = EXTRA_GFX[base]
        return eg, ("npc" if spr else "note"), spr
    if "ITEM_BALL" in gid:
        return "ITEM_BALL", "item", "item"
    eg, spr = ft.swap_gfx(gid)
    fo = ft.FIELD_OBJECTS.get(eg)
    if fo:
        return eg, "field", fo
    return eg, "npc", spr or "man"


def events(fm, dest_names=None, warps=None):
    """FRLG events -> (marks, warps, objects) at the same cells. `warps` overrides the warp list (e.g. both
    halves of an Emerald 2-cell exit mat)."""
    marks, objs = [], []
    ws = warps if warps is not None else [dict(x=w["x"], y=w["y"], dest_map=w["dest_map"],
                                               dest_warp_id=w["dest_warp_id"]) for w in fm.json.get("warp_events", [])]
    for w in ws:
        marks.append((w["x"], w["y"], (dest_names or {}).get(w["dest_map"], w["dest_map"].replace("MAP_", "")
                                                             .split("_")[-1][:8]), "warp"))
    for o in fm.json.get("object_events", []):
        gid = o.get("graphics_id", "")
        eg, kind, spr = emerald_gfx(gid, o.get("script"))
        lab = (o.get("script") or "").split("EventScript_")[-1][:10]
        if kind == "note":                         # no Emerald gfx: labelled box only
            marks.append((o["x"], o["y"], eg.split(" ")[0].split("_")[0][:7].lower(), "note"))
        elif "doll" in (spr or ""):
            marks.append((o["x"], o["y"], "", "npc", spr))
        elif kind == "field":
            marks.append((o["x"], o["y"], "", "field", spr))
        else:
            marks.append((o["x"], o["y"], lab, kind, spr))
        objs.append(dict(x=o["x"], y=o["y"], frlg_gfx=gid, emerald_gfx="OBJ_EVENT_GFX_" + eg,
                         movement=o.get("movement_type"), script=o.get("script")))
    for b in fm.json.get("bg_events", []):
        if b["type"] == "hidden_item":
            marks.append((b["x"], b["y"], "h:" + b.get("item", "")[5:9].lower(), "note"))
        else:
            marks.append((b["x"], b["y"], (b.get("script") or "").split("EventScript_")[-1][:8], "sign"))
    for c in fm.json.get("coord_events", []):
        marks.append((c["x"], c["y"], (c.get("script") or "").split("EventScript_")[-1][:8], "note"))
    return marks, ws, objs


# ================================================================================================ rooms
# Emerald pieces used (gTileset_GenericBuilding unless noted; ids from LAYOUT_HOUSE2 / HOUSE1 / HOUSE_WITH_BED /
# RUSTBORO_CITY_HOUSE / LILYCOVE_CITY_COVE_LILY_MOTEL_1F):
#   wall 205 / 20D, base row 224, floor 223, left strip 239, black 001 (Building primary, the house border)
#   drawer 205/268/270, green cabinet 205/269/271, yellow glass cabinet 286 287/28E 28F/296 297,
#   curtain window 206/20E, shutter window 207/20F, sink 26C 26D/274 275, fridge 278/280/288,
#   green bookshelf 26E 26F/276 277/27E 27F, brown shelf 279 27A/281 282/289 28A,
#   strip plant 291/299, floor plant 222/22A, table 24A 24B/252 253 + chairs 22B/22C,
#   orange rug 235 236 237/23D 23E 23F/245 246 247 + table 248 249/250 251 + rug chairs 2E1/2E2,
#   yellow table 24C 24D/254 255, bed 25A 25B/262 263, exit mat 208 209, motel stairs 213/20B.
ROOMS = {
    # ---------------------------------------------------------------------------------------- 13 maps
    "house3": dict(
        frlg="OneIsland_House1", layout="LAYOUT_HOUSE3_FRLG", pair=HOUSE, out="sevii_house3",
        maps=["ONE_ISLAND_HOUSE1", "ONE_ISLAND_HOUSE2", "TWO_ISLAND_HOUSE", "TWO_ISLAND_CAPE_BRINK_HOUSE",
              "THREE_ISLAND_HOUSE2", "THREE_ISLAND_HOUSE3", "THREE_ISLAND_HOUSE4", "THREE_ISLAND_HOUSE5",
              "FOUR_ISLAND_HOUSE1", "FOUR_ISLAND_HOUSE2", "FIVE_ISLAND_HOUSE1", "FIVE_ISLAND_HOUSE2",
              "SIX_ISLAND_HOUSE", "SIX_ISLAND_WATER_PATH_HOUSE2", "SEVEN_ISLAND_SEVAULT_CANYON_HOUSE"],
        method="hand class map; = vanilla LAYOUT_HOUSE2 furniture set + FRLG's plant column and black row",
        grid="""
            205 205 286 287 207 205 205 205 205 205 278
            268 269 28E 28F 20F 20D 20D 20D 26C 26D 280
            270 271 296 297 224 224 224 224 274 275 288
            291 223 223 223 223 223 223 223 223 223 223
            299 223 223 223 22B 24A 24B 22C 223 223 223
            239 223 223 223 22B 252 253 22C 223 223 223
            291 223 223 223 223 223 223 223 223 223 223
            299 223 223 208 209 223 223 223 223 223 223
            001 001 001 001 001 001 001 001 001 001 001
        """,
        mat=[(3, 7), (4, 7)],
        notes=["FRLG wall row (plant | blue shelf | yellow glass cabinet | picture | sink | fridge) -> drawer | "
               "green cabinet | the same yellow glass cabinet | shutter window | sink | fridge (Emerald puts "
               "plants one row lower, which would stack on the strip plant below).",
               "3-wide FRLG mat (x3-5, warp x4) -> Emerald 2-wide mat x3-4, both halves warp (vanilla habit)."]),
    "house4": dict(
        frlg="SixIsland_WaterPath_House1", layout="LAYOUT_HOUSE4_FRLG", pair=HOUSE, out="six_island_water_path_house1",
        maps=["SIX_ISLAND_WATER_PATH_HOUSE1"],
        method="hand class map (HOUSE3 kit, windows + size-record board)",
        grid="""
            205 286 287 205 206 205 206 205 205 207 205
            268 28E 28F 20D 20E 20D 20E 20D 20D 20F 20D
            270 296 297 224 224 224 224 224 224 224 224
            239 223 223 223 223 223 223 223 223 223 223
            291 223 223 223 22B 24A 24B 22C 223 223 223
            299 223 223 223 22B 252 253 22C 223 223 223
            291 223 223 223 223 223 223 223 223 223 223
            299 223 208 209 223 223 223 223 223 223 223
            001 001 001 001 001 001 001 001 001 001 001
        """,
        mat=[(2, 7), (3, 7)],
        notes=["FRLG size-record notice (bg (9,1)) -> shutter window 207/20F (GenericBuilding has no notice "
               "board); sign event kept on (9,1)."]),
    "three1": dict(
        frlg="ThreeIsland_House1", layout="LAYOUT_THREE_ISLAND_HOUSE1", pair=HOUSE, out="three_island_house1",
        maps=["THREE_ISLAND_HOUSE1"],
        method="hand class map; FRLG Lab_Frlg display case -> yellow glass cabinet (same walk cells)",
        grid="""
            26E 26F 286 287 206 205 205 205 205 205 278
            276 277 28E 28F 20E 20D 20D 20D 26C 26D 280
            27E 27F 296 297 224 224 224 224 274 275 288
            239 223 223 223 223 223 223 223 223 223 223
            291 223 223 223 22B 24A 24B 223 223 223 223
            299 223 223 223 22B 252 253 223 223 223 223
            291 223 223 223 223 223 223 223 223 223 223
            299 223 223 208 209 223 223 223 223 223 223
            001 001 001 001 001 001 001 001 001 001 001
        """,
        mat=[(3, 7), (4, 7)],
        notes=["Lostelle's display case (sign (2,1)) -> the yellow glass-front cabinet x2-3; FRLG x3 was wall "
               "(solid rows 0-1, open base row) so the walk cells are unchanged."]),
    "lorelei": dict(
        frlg="FourIsland_LoreleisHouse", layout="LAYOUT_FOUR_ISLAND_LORELEIS_HOUSE", pair=HOUSE,
        out="four_island_loreleis_house", maps=["FOUR_ISLAND_LORELEIS_HOUSE"],
        method="hand class map; FRLG carpet room -> wood floor + vanilla orange rug (HOUSE1) with rug chairs, "
               "bed (HOUSE_WITH_BED), green bookshelf, yellow table",
        grid="""
            205 205 205 286 287 206 205 205 205 26E 26F
            20D 20D 20D 28E 28F 20E 20D 20D 268 276 277
            25A 25B 224 296 297 224 224 224 270 27E 27F
            262 263 223 235 236 236 236 236 237 24C 24D
            239 223 223 23D 2E1 248 249 2E2 23F 254 255
            239 223 223 23D 23E 250 251 23E 23F 223 223
            239 223 223 245 246 246 246 246 247 223 223
            239 223 223 208 209 223 223 223 223 223 223
            001 001 001 001 001 001 001 001 001 001 001
        """,
        mat=[(3, 7), (4, 7)],
        notes=["FRLG 1-wide bed (x1) -> Emerald 2-wide bed x0-1: (0,2)/(0,3) become solid, but FRLG has the "
               "Wigglytuff / Jigglypuff dolls standing there anyway (object cells).",
               "Dolls: FRLG uses Pokemon OW gfx (several FRLG-only). Emerald has the same dolls as decorations; "
               "the room needs doll OW gfx (marked 'note' here) -- see open questions."]),
    "daycare": dict(
        frlg="FourIsland_PokemonDayCare", layout="LAYOUT_FOUR_ISLAND_POKEMON_DAY_CARE", pair=DAYCARE,
        out="four_island_pokemon_day_care", maps=["FOUR_ISLAND_POKEMON_DAY_CARE"],
        method="vanilla LAYOUT_ROUTE117_POKEMON_DAY_CARE (same 12x9 room) rows 0-3 + FRLG's lower half: "
               "rug zone -> Emerald's indoor lawn with the vanilla table + stools",
        grid="""
            208 235 236 237 209 209 20C 20D 209 209 20A 20F
            210 23D 23E* 23F 213 21C 224 215 211 211 004 217
            218 226 219 226 21B 207 206 206 206 206 20B 21F
            220 22E 221 22E 223 207 206 21E 201 201 201 201
            21D* 206 228 206 206 233 204 230 229 22A 230 204
            225 201 201 201 201 201 204 230 231 232 230 204
            21D* 201 201 201 201 201 204 204 204 204 204 204
            225 201 201 23B 23C 201 201 201 201 201 201 201
            001 001 001 001 001 001 001 001 001 001 001 001
        """,
        mat=[(3, 7), (4, 7)],
        notes=["Back door x2 (rows 0-1), counter L x0-4 rows 2-3, window x6-7, PC x10: Emerald's Route 117 Day "
               "Care has them on the same cells (copied).",
               "FRLG purple rug x6-11 rows 3-6 -> Emerald's indoor lawn (204) which is where the vanilla Day Care "
               "puts its table and stools; FRLG egg-incubator shelves x0 -> Emerald's potted plants (same cells).",
               "Back door (2,1) and plant tops forced solid as in FRLG (FRLG blocks the whole shelf / door cell)."]),
    "seven_room1": dict(
        frlg="SevenIsland_House_Room1", layout="LAYOUT_SEVEN_ISLAND_HOUSE_ROOM1", pair=HOUSE,
        out="seven_island_house_room1", maps=["SEVEN_ISLAND_HOUSE_ROOM1"],
        method="hand class map; FRLG box stack hiding the e-Reader door -> brown shelf + drawer",
        grid="""
            26E 26F 205 279 27A 205 207 205 205 26E 26F
            276 277 20D 281 282 268 20F 20D 20D 276 277
            27E 27F 224 289 28A 270 224 224 224 27E 27F
            291 223 223 223 223 223 223 223 223 223 223
            299 223 223 223 22B 24A 24B 22C 223 223 223
            239 223 223 223 22B 252 253 22C 223 223 223
            291 223 223 223 223 223 223 223 223 223 223
            299 223 223 208 209 223 223 223 223 223 223
            001 001 001 001 001 001 001 001 001 001 001
        """,
        mat=[(3, 7), (4, 7)],
        extra_warps=[dict(x=4, y=1, dest_map="MAP_SEVEN_ISLAND_HOUSE_ROOM2", dest_warp_id="0")],
        notes=["Warp (4,1) -> Room2 sits behind FRLG's boxes and only opens via setmaplayoutindex "
               "LAYOUT_SEVEN_ISLAND_HOUSE_ROOM1_DOOR_OPEN when a valid e-Reader trainer exists."]),
    "seven_room2": dict(
        frlg="SevenIsland_House_Room2", layout="LAYOUT_SEVEN_ISLAND_HOUSE_ROOM2", pair=HOUSE,
        out="seven_island_house_room2", maps=["SEVEN_ISLAND_HOUSE_ROOM2"],
        method="hand class map; FRLG dark doorway -> Lilycove motel stairs (only GenericBuilding way out "
               "through a back wall); blue rug -> vanilla orange rug",
        grid="""
            205 207 205 213 205 207 206 205 206 205 205 207
            20D 20F 20D 20B 20D 20F 20E 20D 20E 20D 20D 20F
            290 224 224 224 224 224 224 224 224 224 224 290
            298 223 223 223 223 223 223 223 223 223 223 298
            239 223 223 235 236 236 236 236 237 223 223 223
            239 223 223 23D 23E 23E 23E 23E 23F 223 223 223
            291 223 223 245 246 246 246 246 247 223 223 222
            299 223 223 223 223 223 223 223 223 223 223 22A
            239 223 223 223 223 223 223 223 223 223 223 223
        """,
        mat=[],
        notes=["e-Reader trainer room: reached only through Room1's DOOR_OPEN layout. FRLG pictures x1/x5/x11 "
               "-> shutter windows, 2-wide pictures x6-7/x8-9 -> curtain windows."]),
}


# ================================================================================================ build
def render_room(key):
    r = ROOMS[key]
    fm = ft.load_map(r["frlg"])
    ts = r["pair"]
    g = parse_grid(r["grid"], ts)
    assert (len(g[0]), len(g)) == (fm.w, fm.h), (key, len(g[0]), len(g), fm.w, fm.h)
    fw = fm.json.get("warp_events", [])
    # warps: FRLG's, plus the second half of the Emerald exit mat (same destination)
    ws = []
    exit_w = next((w for w in fw if (w["x"], w["y"]) in r["mat"]), None)
    for w in fw:
        ws.append(dict(x=w["x"], y=w["y"], dest_map=w["dest_map"], dest_warp_id=w["dest_warp_id"], frlg=True))
    for c in r["mat"]:
        if exit_w and c != (exit_w["x"], exit_w["y"]):
            ws.append(dict(x=c[0], y=c[1], dest_map=exit_w["dest_map"], dest_warp_id=exit_w["dest_warp_id"],
                           frlg=False, note="2nd half of the Emerald exit mat"))
    marks, ws, objs = events(fm, warps=ws)
    spec = grid_spec(g, ts)
    spec["marks"] = marks
    base = os.path.join(OUT, r["out"])
    g2 = vc.render(spec, base)
    assert g2 == g
    fm.report = dict(pair=ts)
    ft.side_by_side(fm, base, scale=2)
    seams = vc.seams(g, ts, ignore=(0x223, 0x001))
    rep = dict(frlg_map=r["frlg"], frlg_layout=r["layout"],
               frlg_pair=(fm.layout["primary_tileset"], fm.layout["secondary_tileset"]),
               maps=r["maps"], pair=ts, size=(fm.w, fm.h), method=r["method"],
               warps=ws, objects=objs,
               bg_events=fm.json.get("bg_events", []), coord_events=fm.json.get("coord_events", []),
               walk_diff=walk_diff(fm, g),
               seams=[(x, y, d, "0x%03X" % a, "0x%03X" % b) for x, y, d, a, b in seams],
               secondary_users=vc.sharing(ts[1]), notes=r.get("notes", []),
               metatiles=["0x%03X" % m for m in vc.metatile_ids(g)])
    keep = {k: v for k, v in spec.items() if k != "cells"}
    keep["grid_raw"] = [" ".join("%04X" % v for v in row) for row in g]
    keep["report"] = rep
    json.dump(keep, open(base + "_spec.json", "w"), indent=1, default=str)
    print("%-28s %-34s %2dx%-2d walkdiff=%d seams=%d %s" % (key, r["frlg"], fm.w, fm.h, len(rep["walk_diff"]),
                                                         len(seams), ["(%d,%d)%s %s|%s" % s for s in rep["seams"]]))
    return rep


# ================================================================================================ harbour
HARBOR_MAPS = ["OneIsland_Harbor", "TwoIsland_Harbor", "ThreeIsland_Harbor", "FourIsland_Harbor",
               "FiveIsland_Harbor", "SixIsland_Harbor", "SevenIsland_Harbor"]


def render_harbor():
    """FRLG Island Harbor == Emerald LAYOUT_ISLAND_HARBOR (the R/S/E port of the same room). Rendered as-is;
    the FRLG sailor (8,6) / Seagallop (8,9) sit on water / pier cells in the Emerald room, so they move to the
    vanilla Birth Island cells (8,5) / (8,7)."""
    e, g = vc.raw_layout("LAYOUT_ISLAND_HARBOR")
    spec = vc.layout_spec("LAYOUT_ISLAND_HARBOR")
    spec["marks"] = [(8, 2, "EXIT", "warp"), (8, 5, "Sailor", "sailor"), (8, 7, "", "boat")]
    base = os.path.join(OUT, "sevii_harbor")
    vc.render(spec, base)
    fm = ft.load_map("OneIsland_Harbor")
    fm.report = dict(pair=HARBOR)
    ft.side_by_side(fm, base, scale=2)
    bi = json.load(open(os.path.join(vc.ROOT, "data", "maps", "BirthIsland_Harbor", "map.json")))
    per_map = []
    for n in HARBOR_MAPS:
        m = ft.load_map(n)
        w = m.json["warp_events"][0]
        per_map.append(dict(map="MAP_" + ft.snake(n).upper(), layout="LAYOUT_ISLAND_HARBOR (shared, unchanged)",
                            warp=dict(x=w["x"], y=w["y"], dest_map=w["dest_map"], dest_warp_id=w["dest_warp_id"]),
                            objects=[dict(x=8, y=5, gfx="OBJ_EVENT_GFX_SAILOR", frlg=(8, 6),
                                          script=m.json["object_events"][1]["script"]),
                                     dict(x=8, y=7, gfx="Briney's boat (decision 1; vanilla OBJ_EVENT_GFX_SS_TIDAL "
                                                        "slot)", frlg=(8, 9))]))
    walk = walk_diff(fm, g)
    rep = dict(pair=HARBOR, size=(17, 13), method="clone: maps point at the existing LAYOUT_ISLAND_HARBOR",
               frlg_layout="LAYOUT_ISLAND_HARBOR_FRLG (General_Frlg / IslandHarbor_Frlg, 17x13)",
               same_room=("Same room: same 17x13 size, building with the door on (8,2), walkway row 3 x1-15, "
                          "railed pier south of the door, sea, railing on the bottom row. Emerald's pier is wider "
                          "at the top (x6-10 on row 4) and solid below; FRLG's jetty runs on to (8,6)."),
               birth_island_events=dict(warps=bi["warp_events"],
                                        objects=[(o["x"], o["y"], o["graphics_id"]) for o in bi["object_events"]]),
               maps=per_map, walk_diff=walk, secondary_users=vc.sharing(HARBOR[1]))
    keep = dict(spec)
    keep["report"] = rep
    json.dump(keep, open(base + "_spec.json", "w"), indent=1, default=str)
    print("harbor  LAYOUT_ISLAND_HARBOR clone  walkdiff=%d  shares: %s" % (len(walk), rep["secondary_users"]))
    return rep




# ================================================================================================ caves
import interiors_caves as icv          # noqa: E402

CAVES = {   # key: (FRLG map, cave set, out name)
    "ember_spa": ("OneIsland_KindleRoad_EmberSpa", "lava", "one_island_kindle_road_ember_spa"),
    "summit_1f": ("MtEmber_SummitPath_1F", "lava", "mt_ember_summit_path_1f"),
    "summit_2f": ("MtEmber_SummitPath_2F", "lava", "mt_ember_summit_path_2f"),
    "summit_3f": ("MtEmber_SummitPath_3F", "lava", "mt_ember_summit_path_3f"),
    "ruby_1f": ("MtEmber_RubyPath_1F", "lava", "mt_ember_ruby_path_1f"),
    "ruby_b1f": ("MtEmber_RubyPath_B1F", "lava", "mt_ember_ruby_path_b1f"),
    "ruby_b1f_stairs": ("MtEmber_RubyPath_B1F_Stairs", "lava", "mt_ember_ruby_path_b1f_stairs"),
    "ruby_b2f": ("MtEmber_RubyPath_B2F", "lava", "mt_ember_ruby_path_b2f"),
    "ruby_b2f_stairs": ("MtEmber_RubyPath_B2F_Stairs", "lava", "mt_ember_ruby_path_b2f_stairs"),
    "ruby_b3f": ("MtEmber_RubyPath_B3F", "lava", "mt_ember_ruby_path_b3f"),
    "ruby_b4f": ("MtEmber_RubyPath_B4F", "lava", "mt_ember_ruby_path_b4f"),
    "ruby_b5f": ("MtEmber_RubyPath_B5F", "lava", "mt_ember_ruby_path_b5f"),
    "dunsparce": ("ThreeIsland_DunsparceTunnel", "cave", "three_island_dunsparce_tunnel"),
    "dunsparce_dug": ("ThreeIsland_DunsparceTunnel@LAYOUT_THREE_ISLAND_DUNSPARCE_TUNNEL_DUG_OUT", "cave",
                      "three_island_dunsparce_tunnel_dug_out"),
    "dunsparce_dug_rusturf": ("ThreeIsland_DunsparceTunnel@LAYOUT_THREE_ISLAND_DUNSPARCE_TUNNEL_DUG_OUT", "rusturf",
                              "three_island_dunsparce_tunnel_dug_out_alt_rusturf"),
    "dotted_1f": ("SixIsland_DottedHole_1F", "navel", "six_island_dotted_hole_1f"),
    "dotted_b1f": ("SixIsland_DottedHole_B1F", "navel", "six_island_dotted_hole_b1f"),
    "dotted_b2f": ("SixIsland_DottedHole_B2F", "navel", "six_island_dotted_hole_b2f"),
    "dotted_b3f": ("SixIsland_DottedHole_B3F", "navel", "six_island_dotted_hole_b3f"),
    "dotted_b4f": ("SixIsland_DottedHole_B4F", "navel", "six_island_dotted_hole_b4f"),
    "dotted_sapphire": ("SixIsland_DottedHole_SapphireRoom", "navel", "six_island_dotted_hole_sapphire_room"),
    "tanoby_key": ("SevenIsland_SevaultCanyon_TanobyKey", "cave", "seven_island_sevault_canyon_tanoby_key"),
    "tanoby_key_rusturf": ("SevenIsland_SevaultCanyon_TanobyKey", "rusturf",
                           "seven_island_sevault_canyon_tanoby_key_alt_rusturf"),
    "tanoby_monean": ("SevenIsland_TanobyRuins_MoneanChamber", "cave", "seven_island_tanoby_ruins_monean_chamber"),
    "tanoby_monean_ruins": ("SevenIsland_TanobyRuins_MoneanChamber", "ruins",
                            "seven_island_tanoby_ruins_monean_chamber_alt_ruins"),
}
TANOBY_OTHERS = ["Liptoo", "Weepth", "Dilford", "Scufib", "Rixy", "Viapois"]
for _t in TANOBY_OTHERS:
    CAVES["tanoby_" + _t.lower()] = ("SevenIsland_TanobyRuins_%sChamber" % _t, "cave",
                                     "seven_island_tanoby_ruins_%s_chamber" % _t.lower())


def load_variant(name):
    """'Map@LAYOUT_X' -> the FRLG map with an alternative layout (setmaplayoutindex states)."""
    import copy
    import struct
    base, _, lid = name.partition("@")
    fm = ft.load_map(base)
    if not lid:
        return fm
    v = copy.copy(fm)
    e = ft.frlg_layouts()[lid]
    v.layout, v.w, v.h = e, e["width"], e["height"]
    vals = struct.unpack("<%dH" % (v.w * v.h), ft._git(e["blockdata_filepath"])[:2 * v.w * v.h])
    v.raw = [list(vals[y * v.w:(y + 1) * v.w]) for y in range(v.h)]
    v.json = dict(fm.json, layout=lid)
    v.name = base + " (" + lid.replace("LAYOUT_", "") + ")"
    return v


def render_cave(key):
    name, sk, outn = CAVES[key]
    fm = load_variant(name)
    g = icv.paint(fm, sk)
    cls = fm.report["classes"]
    seams0 = len(vc.seams(g, icv.SETS[sk]["pair"]))
    g, fixed = icv.seam_fix(g, cls, sk)
    ts = icv.SETS[sk]["pair"]
    marks, ws, objs = events(fm)
    spec = grid_spec(g, ts)
    spec["marks"] = marks
    base = os.path.join(OUT, outn)
    vc.render(spec, base)
    rep = dict(fm.report)
    ft.side_by_side(fm, base, scale=1 if fm.w * fm.h > 600 else 2)
    ign = set(icv.SETS[sk]["floor"]) | set(icv.SETS[sk]["detail"]) | set(icv.SETS[sk]["boulder"])
    seams = vc.seams(g, ts, ignore=ign)
    rep.update(frlg_map=name.split("@")[0], frlg_layout=fm.json["layout"],
               frlg_pair=(fm.layout["primary_tileset"], fm.layout["secondary_tileset"]),
               maps=["MAP_" + ft.snake(name.split("@")[0]).upper()], size=(fm.w, fm.h),
               method="learned cave autotiler (interiors_caves.py), set '%s'" % sk,
               warps=ws, objects=objs, bg_events=fm.json.get("bg_events", []),
               coord_events=fm.json.get("coord_events", []), walk_diff=walk_diff(fm, g),
               seams_before_fix=seams0, seam_cells_repicked=fixed,
               seams=[(x, y, d, "0x%03X" % a, "0x%03X" % b) for x, y, d, a, b in seams],
               secondary_users=vc.sharing(ts[1]), metatiles=["0x%03X" % m for m in vc.metatile_ids(g)])
    keep = {k: v for k, v in spec.items() if k != "cells"}
    keep["grid_raw"] = [" ".join("%04X" % v for v in row) for row in g]
    keep["report"] = rep
    json.dump(keep, open(base + "_spec.json", "w"), indent=1, default=str)
    print("%-16s %-36s %2dx%-2d %-6s walkdiff=%d seams %d->%d levels=%s" % (
        key, name, fm.w, fm.h, sk, len(rep["walk_diff"]), seams0, len(seams), rep["sig_levels"]))
    return rep


def main(keys):
    os.makedirs(OUT, exist_ok=True)
    if not keys or "harbor" in keys:
        render_harbor()
    for k in (keys or list(ROOMS) + list(CAVES)):
        if k in ROOMS:
            render_room(k)
        elif k in CAVES:
            render_cave(k)


if __name__ == "__main__":
    main(sys.argv[1:])
