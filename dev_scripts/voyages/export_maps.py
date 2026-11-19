"""
Export the Sevii translations as REAL map data (implementation input, not mockups): for every map the batch-2/3
scripts, icefall_translate, frlg_interiors and rocket_warehouse_interior build, write

  <out>/layouts/<Folder>/map.bin + border.bin      raw u16 blocks exactly as rendered (metatile|coll|elev)
  <out>/layouts.json                              layouts.json entries for those layouts (FRLG layout ids reused)
  <out>/maps/<MapFolder>/map.json                 FRLG map.json made Emerald-ready: FRLG-only graphics swapped,
                                                  moved objects applied, invented sea-route connections added
                                                  (both directions), sea-route maps created from scratch
  <out>/tilesets/sevii_islands/                   the proposed gTileset_SeviiIslands written out for real
                                                  (Rustboro copy + sevii_tileset additions + arrow duplicates)
  <out>/manifest.json                             what was written, per map: source, layout, pair, notes

Nothing under data/ is touched: copy the folders in when building (see out/batch3/NOTES.md, "Implementation").
usage: <venv python> dev_scripts/voyages/frlg_translate.py export [--out DIR]
       (= this module's main(); default DIR dev_scripts/voyages/out/export)
"""
import json
import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc       # noqa: E402
import frlg_translate as ft       # noqa: E402

OUT = os.path.join(HERE, "out", "export")
CAPTURE = {}                      # rendered base name -> (spec, grid)


def _capture():
    orig_vc, orig_ft = vc.render, ft.render

    def vrender(spec, base, *a, **k):
        g = orig_vc(spec, base, *a, **k)
        CAPTURE[os.path.basename(base)] = (spec, g)
        return g

    def frender(spec, base):
        g = orig_ft(spec, base)
        CAPTURE[os.path.basename(base)] = (spec, g)
        return g
    vc.render, ft.render = vrender, frender


_FOLDERS = None


def frlg_folder(const):
    """MAP_FOUR_ISLAND_HOUSE1 / FOUR_ISLAND_HOUSE1 -> FRLG map folder name without _Frlg (FourIsland_House1)."""
    global _FOLDERS
    if _FOLDERS is None:
        out = subprocess.run(["git", "-C", vc.ROOT, "ls-tree", "--name-only", ft.FRLG_REF, "data/maps/"],
                             capture_output=True, text=True).stdout.split()
        _FOLDERS = {}
        for p in out:
            n = os.path.basename(p)
            if n.endswith("_Frlg"):
                _FOLDERS[ft.snake(n[:-5]).upper()] = n[:-5]
    return _FOLDERS[const.replace("MAP_", "")]


def write_layout(out, layout_id, folder, grid, ts, border=None):
    d = os.path.join(out, "layouts", folder)
    os.makedirs(d, exist_ok=True)
    h, w = len(grid), len(grid[0])
    open(os.path.join(d, "map.bin"), "wb").write(struct.pack("<%dH" % (w * h), *[v for r in grid for v in r]))
    b = border if border is not None else grid[0][0]
    open(os.path.join(d, "border.bin"), "wb").write(struct.pack("<4H", *([b] * 4)))
    return dict(id=layout_id, name=folder + "_Layout", width=w, height=h, primary_tileset=ts[0],
                secondary_tileset=ts[1], border_filepath="data/layouts/%s/border.bin" % folder,
                blockdata_filepath="data/layouts/%s/map.bin" % folder, layout_version="emerald")


_FRLG_ONLY, _SPECIES = None, None
# more FRLG-only gfx -> Emerald stand-ins for the exported map.json (Team Rocket = Team Aqua placeholder until
# Orchid's Sevii villain team is decided; Emerald has no Cooltrainer overworld)
EXPORT_SWAP = {"OBJ_EVENT_GFX_ROCKET_M": "OBJ_EVENT_GFX_AQUA_MEMBER_M", "OBJ_EVENT_GFX_ROCKET_F": "OBJ_EVENT_GFX_AQUA_MEMBER_F",
               "OBJ_EVENT_GFX_BUG_CATCHER_FRLG": "OBJ_EVENT_GFX_BUG_CATCHER",
               "OBJ_EVENT_GFX_COOLTRAINER_M": "OBJ_EVENT_GFX_MAN_4", "OBJ_EVENT_GFX_COOLTRAINER_F": "OBJ_EVENT_GFX_WOMAN_5"}


def _gfx(gid, script=""):
    """FRLG graphics id -> an Emerald-visible one. FRLG-only Pokemon sprites -> OBJ_EVENT_GFX_SPECIES(X);
    anything still FRLG-only is returned with a trailing '?' (listed in the map's _export_notes)."""
    global _FRLG_ONLY, _SPECIES
    if _FRLG_ONLY is None:
        import re
        _FRLG_ONLY = ft.frlg_only_gfx()
        _SPECIES = set(re.findall(r"\b(SPECIES_\w+)\b", open(os.path.join(
            vc.ROOT, "include", "constants", "species.h")).read()))
    try:
        import frlg_interiors as fi
        eg = fi.emerald_gfx(gid, script)[0]
    except Exception:
        eg = ft.swap_gfx(gid)[0]
    eg = eg if eg.startswith("OBJ_EVENT_GFX_") else "OBJ_EVENT_GFX_" + eg
    eg = EXPORT_SWAP.get(eg, eg)
    if eg in _FRLG_ONLY:
        name = eg[len("OBJ_EVENT_GFX_"):]
        if "SPECIES_" + name in _SPECIES:
            return "OBJ_EVENT_GFX_SPECIES(%s)" % name
        return eg + "?"
    return eg


def map_json(folder, layout_id, frlg_json, moves=None, extra_conns=(), notes=()):
    j = json.loads(json.dumps(frlg_json))
    j["name"] = folder
    j["layout"] = layout_id
    moves = moves or {}
    bad = []
    for o in j.get("object_events", []):
        if "graphics_id" in o:
            o["graphics_id"] = _gfx(o["graphics_id"], o.get("script", ""))
            if o["graphics_id"].endswith("?"):
                o["graphics_id"] = o["graphics_id"][:-1]
                bad.append("%s at (%d,%d)" % (o["graphics_id"], o["x"], o["y"]))
    if bad:
        notes = list(notes) + ["FRLG-only graphics left (invisible in Emerald, pick a stand-in): " + ", ".join(bad)]
        if (o.get("x"), o.get("y")) in moves:
            o["x"], o["y"] = moves[(o["x"], o["y"])]
    conns = list(j.get("connections") or [])
    for d, off, m in extra_conns:
        conns.append(dict(map=m, offset=off, direction=d))
    j["connections"] = conns or 0
    if notes:
        j["_export_notes"] = list(notes)
    return j


def write_map(out, folder, j):
    d = os.path.join(out, "maps", folder)
    os.makedirs(d, exist_ok=True)
    json.dump(j, open(os.path.join(d, "map.json"), "w"), indent=2)


_OPP = {"left": "right", "right": "left", "up": "down", "down": "up"}


def route_json(key, spec, music):
    const = "MAP_" + key.upper()
    folder = "".join(p.title() for p in key.split("_"))
    objs, n_item, n_npc = [], 0, 0
    for m in spec.get("marks", []):
        x, y, label, kind = m[:4]
        if kind == "item":
            n_item += 1
            objs.append(dict(type="object", graphics_id="OBJ_EVENT_GFX_ITEM_BALL", x=x, y=y, elevation=1,
                             movement_type="MOVEMENT_TYPE_LOOK_AROUND", movement_range_x=0, movement_range_y=0,
                             trainer_type="TRAINER_TYPE_NONE", trainer_sight_or_berry_tree_id="ITEM_NONE",
                             script="Common_EventScript_FindItem",
                             flag="FLAG_ITEM_%s_%d" % (key.upper(), n_item)))
        elif kind == "npc":
            n_npc += 1
            objs.append(dict(type="object", graphics_id="OBJ_EVENT_GFX_SWIMMER_M" if n_npc % 2 else
                             "OBJ_EVENT_GFX_SWIMMER_F", x=x, y=y, elevation=1,
                             movement_type="MOVEMENT_TYPE_WANDER_AROUND", movement_range_x=2, movement_range_y=1,
                             trainer_type="TRAINER_TYPE_NONE", trainer_sight_or_berry_tree_id="0",
                             script="%s_EventScript_Swimmer%d" % (folder, n_npc), flag="0"))
    j = dict(id=const, name=folder, layout="LAYOUT_" + key.upper(), music=music, region="REGION_KANTO",
             region_map_section="MAPSEC_" + key.upper(), requires_flash=False, weather="WEATHER_SUNNY",
             map_type="MAP_TYPE_ROUTE", allow_cycling=False, allow_escaping=False, allow_running=True,
             show_map_name=True, floor_number=0, battle_scene="MAP_BATTLE_SCENE_NORMAL",
             connections=[dict(map=m, offset=off, direction=d) for d, off, m, _ab in spec["conns"]],
             object_events=objs, warp_events=[], coord_events=[], bg_events=[],
             _export_notes=["invented Surf route (user decision); MAPSEC_%s is a NEW region-map section to add; "
                            "item flags are placeholders (reuse unreachable vanilla item flags, see memory)"
                            % key.upper()])
    return folder, j


def write_tileset(out):
    """gTileset_SeviiIslands as real files: Rustboro's tiles.png with the new tiles written into their slots,
    Rustboro's palettes with the filled slots, metatiles.bin / metatile_attributes.bin + the new metatiles
    (arrow duplicates included -- export after every map has been built)."""
    import sevii_tileset as st
    from PIL import Image
    src = st.BASE_DIR
    d = os.path.join(out, "tilesets", "sevii_islands")
    os.makedirs(os.path.join(d, "palettes"), exist_ok=True)
    im = Image.open(os.path.join(src, "tiles.png"))
    cols = im.width // 8
    need = max([im.width // 8 * (im.height // 8)] + [k + 1 for k in st._TILES])
    rows = (need + cols - 1) // cols
    new = Image.new("P", (im.width, rows * 8))
    new.putpalette(im.getpalette())
    new.paste(im, (0, 0))
    px = new.load()
    for k, t in st._TILES.items():
        ox, oy = (k % cols) * 8, (k // cols) * 8
        for y in range(8):
            for x in range(8):
                px[ox + x, oy + y] = t[y][x]
    new.save(os.path.join(d, "tiles.png"))
    for i in range(16):
        p = os.path.join(src, "palettes", "%02d.pal" % i)
        txt = open(p).read()
        if i in st._PALS:
            txt = "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % tuple(c) for c in st._PALS[i])
        open(os.path.join(d, "palettes", "%02d.pal" % i), "w").write(txt)
    meta = open(os.path.join(src, "metatiles.bin"), "rb").read()
    attrs = open(os.path.join(src, "metatile_attributes.bin"), "rb").read()
    for _lab, entries, attr in st._META:
        meta += struct.pack("<8H", *entries)
        attrs += struct.pack("<H", attr)
    open(os.path.join(d, "metatiles.bin"), "wb").write(meta)
    open(os.path.join(d, "metatile_attributes.bin"), "wb").write(attrs)
    labels = {lab: "0x%03X" % st.LABELS[lab] for lab, _e, _a in st._META}
    json.dump(dict(labels=labels, budget=st.budget(), copy_of="gTileset_Rustboro (anim: Rustboro's water / "
                   "fountain animations must be registered for the copy too)"),
              open(os.path.join(d, "labels.json"), "w"), indent=1, default=str)
    return d


def main(args):
    out = OUT
    if "--out" in args:
        out = args[args.index("--out") + 1]
    os.makedirs(out, exist_ok=True)
    _capture()
    import mock_batch2 as m2
    import mock_batch3 as m3
    import icefall_translate as it
    import frlg_interiors as fi
    import rocket_warehouse_interior as rw
    m2.main([])
    m3.main(["maps", "routes"])
    it.main(list(it.ROOMS))
    fi.main([])
    rw.main()
    layouts, manifest = [], {}
    route_conns = {}                     # island map const -> [(dir, offset, route const)]
    for routes in (m2.SEA_ROUTES, m3.SEA_ROUTES):
        for key, spec in routes.items():
            for d, off, m, _ab in spec["conns"]:
                route_conns.setdefault(m, []).append((_OPP[d], -off, "MAP_" + key.upper()))
    sea = None

    def outdoor(n, moves=None):
        nonlocal sea
        spec, g = CAPTURE[ft.snake(n)]
        fm = ft.load_map(n)
        ts = tuple(spec["tileset"])
        sea = vc.ref_value(("id", 0x170, 0, 1), vc.real_pair(ts))
        e = ft.frlg_layouts()[fm.json["layout"]]
        folder = os.path.basename(os.path.dirname(e["blockdata_filepath"])).replace("_Frlg", "")
        layouts.append(write_layout(out, fm.json["layout"], folder, g, ts, border=sea))
        const = fm.json["id"]
        j = map_json(n, fm.json["layout"], fm.json, moves, route_conns.get(const, ()))
        write_map(out, n, j)
        manifest[n] = dict(kind="outdoor", layout=fm.json["layout"], pair=ts, size=(len(g[0]), len(g)))
    for n in m2.MAPS:
        outdoor(n, m2.MOVE_MARKS.get(n))
    for n in m3.MAPS:
        outdoor(n)
    for routes, music in ((m2.SEA_ROUTES, "MUS_RG_SEVII_123"), (m3.SEA_ROUTES, None)):
        for key, spec in routes.items():
            mus = music or ("MUS_RG_SEVII_45" if key.endswith("_c") else "MUS_RG_SEVII_67")
            _spec, g = CAPTURE[key]
            folder, j = route_json(key, spec, mus)
            layouts.append(write_layout(out, "LAYOUT_" + key.upper(), folder, g, spec["tileset"],
                                        border=vc.ref_value(("id", 0x170, 0, 1), vc.real_pair(spec["tileset"]))))
            write_map(out, folder, j)
            manifest[folder] = dict(kind="sea route (new)", layout="LAYOUT_" + key.upper(), pair=spec["tileset"])
    # Icefall Cave
    for key, n in it.ROOMS.items():
        spec, g = CAPTURE["four_island_icefall_cave_" + key]
        fm = ft.load_map(n)
        e = ft.frlg_layouts()[fm.json["layout"]]
        folder = os.path.basename(os.path.dirname(e["blockdata_filepath"])).replace("_Frlg", "")
        layouts.append(write_layout(out, fm.json["layout"], folder, g, spec["tileset"]))
        write_map(out, n, map_json(n, fm.json["layout"], fm.json))
        manifest[n] = dict(kind="cave (icefall_translate)", layout=fm.json["layout"], pair=spec["tileset"])
    # houses: one layout, many maps
    for key, r in fi.ROOMS.items():
        spec, g = CAPTURE[r["out"]]
        fm = ft.load_map(r["frlg"])
        e = ft.frlg_layouts().get(r["layout"])
        folder = (os.path.basename(os.path.dirname(e["blockdata_filepath"])).replace("_Frlg", "") if e
                  else r["layout"][7:].title().replace("_", ""))
        layouts.append(write_layout(out, r["layout"], folder, g, spec["tileset"]))
        for const in r.get("maps") or [ft.snake(r["frlg"]).upper()]:
            n = frlg_folder(const)
            m = ft.load_map(n)
            notes = []
            if (m.w, m.h) != (len(g[0]), len(g)):
                notes.append("room size differs from FRLG: check event positions")
            notes += ["Emerald exit mat is 2 wide: add a 2nd warp on the other mat half (see "
                      "out/interiors/%s_spec.json)" % r["out"]] if r.get("mat") else []
            write_map(out, n, map_json(n, r["layout"], m.json, notes=notes))
            manifest[n] = dict(kind="interior (frlg_interiors)", layout=r["layout"], pair=spec["tileset"])
    for key, (n, _set, base) in fi.CAVES.items():
        if base not in CAPTURE:
            continue
        if "_alt_" in base:              # alternative look (Rusturf / ruins set): review only, not exported
            manifest[base] = dict(kind="alternative look, not exported", source=key)
            continue
        spec, g = CAPTURE[base]
        n, _, lay = n.partition("@")     # "Map@LAYOUT_X" = an alternative layout of that map (e.g. dug-out tunnel)
        fm = ft.load_map(n)
        lay = lay or fm.json["layout"]
        e = ft.frlg_layouts()[lay]
        folder = os.path.basename(os.path.dirname(e["blockdata_filepath"])).replace("_Frlg", "")
        layouts.append(write_layout(out, lay, folder, g, spec["tileset"]))
        if lay == fm.json["layout"]:
            write_map(out, n, map_json(n, lay, fm.json))
        manifest[folder if lay != fm.json["layout"] else n] = dict(kind="cave (frlg_interiors)", layout=lay,
                                                                   pair=spec["tileset"])
    # the other 6 Tanoby chambers: FRLG gives each its own 23x17 layout; only Monean is translated -> placeholder
    mon = "LAYOUT_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER"
    for c in ("Liptoo", "Weepth", "Dilford", "Scufib", "Rixy", "Viapois"):
        n = "SevenIsland_TanobyRuins_%sChamber" % c
        if n in manifest:                # translated in its own right (frlg_interiors CAVES)
            continue
        m = ft.load_map(n)
        write_map(out, n, map_json(n, mon, m.json, notes=["placeholder: uses the translated Monean chamber layout; "
                                                          "FRLG's own %s layout differs in the Unown text wall "
                                                          "only (translate later)" % m.json["layout"]]))
        manifest[n] = dict(kind="chamber (Monean layout placeholder)", layout=mon)
    # harbours: the existing LAYOUT_ISLAND_HARBOR, sailor / boat moved to Birth Island's cells
    for n in fi.HARBOR_MAPS:
        m = ft.load_map(n)
        write_map(out, n, map_json(n, "LAYOUT_ISLAND_HARBOR", m.json, moves={(8, 6): (8, 5), (8, 9): (8, 7)},
                                   notes=["boat = Mr. Briney's boat (decision 1)"]))
        manifest[n] = dict(kind="harbour (existing LAYOUT_ISLAND_HARBOR)", layout="LAYOUT_ISLAND_HARBOR")
    # Rocket Warehouse interior (New Mauville tiles, 30x28: FRLG 29x27 padded)
    spec, g = CAPTURE[os.path.basename(rw.BASE)]
    fm = rw.frlg_map()
    layouts.append(write_layout(out, "LAYOUT_FIVE_ISLAND_ROCKET_WAREHOUSE", "FiveIsland_RocketWarehouse", g,
                                spec["tileset"]))
    write_map(out, "FiveIsland_RocketWarehouse", map_json(
        "FiveIsland_RocketWarehouse", "LAYOUT_FIVE_ISLAND_ROCKET_WAREHOUSE", fm.json,
        notes=["room is 30x28 (FRLG 29x27): exit mat moved to (24,27)/(25,27); Admin 2 moved to (26,11); see "
               "out/batch3/five_island_rocket_warehouse_spec.json"]))
    manifest["FiveIsland_RocketWarehouse"] = dict(kind="interior (New Mauville tiles)",
                                                  layout="LAYOUT_FIVE_ISLAND_ROCKET_WAREHOUSE", pair=spec["tileset"])
    # connections / warps to maps this export does not build (Water Labyrinth, Trainer Tower, Green Path, Lost
    # Cave ...): connections are dropped (an unknown map breaks the build), warps are kept and listed
    mdir = os.path.join(out, "maps")
    ids = {json.load(open(os.path.join(mdir, f, "map.json")))["id"] for f in os.listdir(mdir)}
    ids |= {"MAP_" + ft.snake(k).upper() for k in ("TelokTown_PokemonCenter_1F",)}
    for f in sorted(os.listdir(mdir)):
        p_ = os.path.join(mdir, f, "map.json")
        j = json.load(open(p_))
        conns = j.get("connections") or []
        keep = [c for c in conns if c["map"] in ids]
        gone = [c["map"] for c in conns if c["map"] not in ids]
        missing = sorted({w["dest_map"] for w in j.get("warp_events", []) if w["dest_map"] not in ids})
        notes = j.get("_export_notes", [])
        if gone:
            j["connections"] = keep or 0
            notes.append("connections dropped (map not built yet): " + ", ".join(gone))
        if missing:
            notes.append("warps to maps not in this export (Centres/Marts = TelokTown clones, or out of scope): "
                         + ", ".join(missing))
        if notes:
            j["_export_notes"] = notes
        json.dump(j, open(p_, "w"), indent=2)
        manifest.setdefault(f, {})["notes"] = notes
    json.dump(dict(layouts=layouts), open(os.path.join(out, "layouts.json"), "w"), indent=2)
    tsd = write_tileset(out)
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1, default=str)
    print("exported %d maps, %d layouts, tileset -> %s" % (len(manifest), len(layouts), tsd))
    return manifest


if __name__ == "__main__":
    main(sys.argv[1:])
