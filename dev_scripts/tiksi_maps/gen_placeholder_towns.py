"""
Placeholder town maps for the Tiksi region (user, 2026-11-18: "placeholder maps ... take some inspo from
the notes I left on each map in the tagger"). Each town is cut from a vanilla town that fits the user's
tagger note, with the bits that don't fit removed, and gets a working Pokémon Centre so Tiksi has fly
points. Replace them with real maps whenever; rerunning this script overwrites only what it made.

  Furong Village   "A fishing village near the route the player lands on"    <- Dewford, gym -> fisher's house
  Drake Base Camp  base camp for Mt. Drake (no note)                          <- Lavaridge, gym removed
  Ube City         "Tiksi's only city. Home to Silph Co.'s Tiksi branch"     <- Rustboro (Devon tower = Silph branch), gym removed
  Tanglyn Town     "A quiet coastal town filled with ancient murals"          <- Slateport's north-west quarter

Per town it writes:
  data/layouts/<Town>/map.bin + border.bin, a LAYOUT_<TOWN> entry in data/layouts/layouts.json
  data/maps/<Town>/map.json + scripts.pory            (sets FLAG_VISITED_<TOWN>; town / Centre / Mart signs)
  data/maps/<Town>_PokemonCenter_1F/map.json + scripts.pory   (nurse + café; setrespawn HEAL_LOCATION_<TOWN>)
  HEAL_LOCATION_<TOWN> in src/data/heal_locations.json (lands outside the Centre)
  group gMapGroup_Tiksi in data/maps/map_groups.json
Only the Centre door is a warp; other doors are scenery for now. No connections (no Tiksi routes yet).

usage: python3 dev_scripts/tiksi_maps/gen_placeholder_towns.py
"""
import collections
import json
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
GROUP = "gMapGroup_Tiksi"

TOWNS = [
    dict(folder="FurongVillage", const="FURONG_VILLAGE", mapsec="MAPSEC_FURONG_VILLAGE", src="DewfordTown",
         crop=(0, 0, 20, 20), map_type="MAP_TYPE_TOWN",
         # gym (x4-10, y12-17) -> sand, then a copy of the fisher's house (x7-10, y4-7)
         fills=[(4, 12, 7, 6)], stamps=[((7, 4, 4, 4), (5, 13))],
         sign=["FURONG VILLAGE", "A fishing village on TIKSI's shore."]),
    dict(folder="DrakeBaseCamp", const="DRAKE_BASE_CAMP", mapsec="MAPSEC_DRAKE_BASE_CAMP", src="LavaridgeTown",
         crop=(0, 0, 20, 20), map_type="MAP_TYPE_TOWN",
         fills=[(1, 10, 7, 7)], stamps=[],
         sign=["DRAKE BASE CAMP", "The last stop before MT. DRAKE."]),
    dict(folder="UbeCity", const="UBE_CITY", mapsec="MAPSEC_UBE_CITY", src="RustboroCity",
         crop=(4, 5, 35, 46), map_type="MAP_TYPE_CITY",
         fills=[(18, 8, 10, 9)], stamps=[],          # gym + its statue
         sign=["UBE CITY", "Home of SILPH CO.'s TIKSI branch."],
         extra_signs=[((17, 20), ["SILPH CO. TIKSI BRANCH", "Closed to visitors."])]),
    dict(folder="TanglynTown", const="TANGLYN_TOWN", mapsec="MAPSEC_TANGLYN_TOWN", src="SlateportCity",
         crop=(0, 6, 24, 27), map_type="MAP_TYPE_TOWN",
         fills=[], stamps=[],
         sign=["TANGLYN TOWN", "A quiet coastal town filled", "with ancient murals."],
         # the old Battle Tent dome stands in for the mural hall (sign spot of the Battle Tent sign)
         extra_signs=[((7, 13), ["TANGLYN MURAL HALL", "Home of TIKSI's ancient murals.", "(Closed for restoration.)"])]),
]


def read_layout(layout_id):
    js = json.load(open(P("data", "layouts", "layouts.json")))
    for e in js["layouts"]:
        if e.get("id") == layout_id:
            w, h = e["width"], e["height"]
            raw = open(P(e["blockdata_filepath"]), "rb").read()
            vals = struct.unpack("<%dH" % (w * h), raw[:2 * w * h])
            return e, [list(vals[y * w:(y + 1) * w]) for y in range(h)], open(P(e["border_filepath"]), "rb").read()
    raise KeyError(layout_id)


def build_grid(t, src_grid):
    x0, y0, w, h = t["crop"]
    g = [row[x0:x0 + w] for row in src_grid[y0:y0 + h]]
    # ground = the most common walkable metatile of the crop (collision bits 10-11 clear)
    ground = collections.Counter(v for row in g for v in row if (v >> 10) & 3 == 0).most_common(1)[0][0]
    for fx, fy, fw, fh in t["fills"]:
        for y in range(fy, fy + fh):
            for x in range(fx, fx + fw):
                g[y][x] = ground
    for (sx, sy, sw, sh), (dx, dy) in t["stamps"]:          # source coords are crop-relative too
        chunk = [row[x0 + sx:x0 + sx + sw] for row in src_grid[y0 + sy:y0 + sy + sh]]
        for j in range(sh):
            for i in range(sw):
                g[dy + j][dx + i] = chunk[j][i]
    return g


def town_events(t, src_map, w, h):
    x0, y0 = t["crop"][:2]
    inside = lambda x, y: 0 <= x - x0 < w and 0 <= y - y0 < h
    centre = [wv for wv in src_map["warp_events"] if wv["dest_map"].endswith("POKEMON_CENTER_1F")]
    door = min(centre, key=lambda wv: -wv["y"])               # the front door (lowest on the map)
    warps = [{"x": door["x"] - x0, "y": door["y"] - y0, "elevation": door["elevation"],
              "dest_map": "MAP_%s_POKEMON_CENTER_1F" % t["const"], "dest_warp_id": "0"}]
    signs = []
    for b in src_map["bg_events"]:
        if b.get("type") != "sign" or not inside(b["x"], b["y"]):
            continue
        s = b.get("script", "")
        if s.endswith(("TownSign", "CitySign")):
            s = "%s_EventScript_TownSign" % t["folder"]
        elif s not in ("Common_EventScript_ShowPokemonCenterSign", "Common_EventScript_ShowPokemartSign"):
            continue
        signs.append(dict(b, x=b["x"] - x0, y=b["y"] - y0, script=s))
    for i, ((x, y), _) in enumerate(t.get("extra_signs", [])):
        signs.append({"type": "sign", "x": x - x0, "y": y - y0, "elevation": 0,
                      "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                      "script": "%s_EventScript_Sign%d" % (t["folder"], i)})
    return warps, signs


def heal_spot(t, src_map_id):
    x0, y0 = t["crop"][:2]
    for e in json.load(open(P("src", "data", "heal_locations.json")))["heal_locations"]:
        if e["map"] == src_map_id:
            return e["x"] - x0, e["y"] - y0
    raise KeyError(src_map_id)


def sign_text(label, lines):
    out = ["%s:" % label]
    for i, line in enumerate(lines):
        end = "$" if i == len(lines) - 1 else ("\\n" if i == 0 else "\\l")
        out.append('\t.string "%s%s"' % (line, end))
    return out


def write_town(t, grid, border, src_entry, src_map):
    folder, const = t["folder"], t["const"]
    h, w = len(grid), len(grid[0])
    os.makedirs(P("data", "layouts", folder), exist_ok=True)
    open(P("data", "layouts", folder, "map.bin"), "wb").write(struct.pack("<%dH" % (w * h), *[v for r in grid for v in r]))
    open(P("data", "layouts", folder, "border.bin"), "wb").write(border)
    layout = {"id": "LAYOUT_%s" % const, "name": "%s_Layout" % folder, "width": w, "height": h,
              "primary_tileset": src_entry["primary_tileset"], "secondary_tileset": src_entry["secondary_tileset"],
              "border_filepath": "data/layouts/%s/border.bin" % folder,
              "blockdata_filepath": "data/layouts/%s/map.bin" % folder, "layout_version": "emerald"}
    warps, signs = town_events(t, src_map, w, h)
    m = {"id": "MAP_%s" % const, "name": folder, "layout": layout["id"], "music": src_map["music"],
         "region": "REGION_HOENN",   # mapjson: emerald builds only take REGION_HOENN maps; Tiksi comes from the mapsec
         "region_map_section": t["mapsec"], "requires_flash": False, "weather": "WEATHER_SUNNY",
         "map_type": t["map_type"], "allow_cycling": True, "allow_escaping": False, "allow_running": True,
         "show_map_name": True, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None,
         "object_events": [], "warp_events": warps, "coord_events": [], "bg_events": signs}
    os.makedirs(P("data", "maps", folder), exist_ok=True)
    json.dump(m, open(P("data", "maps", folder, "map.json"), "w"), indent=2)
    L = ["raw `",
         "%s_MapScripts::" % folder,
         "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % folder,
         "\t.byte 0", "",
         "%s_OnTransition:" % folder,
         "\tsetflag FLAG_VISITED_%s" % const,
         "\tend", "",
         "%s_EventScript_TownSign::" % folder,
         "\tmsgbox %s_Text_TownSign, MSGBOX_SIGN" % folder,
         "\tend", ""]
    for i, (_, lines) in enumerate(t.get("extra_signs", [])):
        L += ["%s_EventScript_Sign%d::" % (folder, i), "\tmsgbox %s_Text_Sign%d, MSGBOX_SIGN" % (folder, i), "\tend", ""]
    L += sign_text("%s_Text_TownSign" % folder, t["sign"]) + [""]
    for i, (_, lines) in enumerate(t.get("extra_signs", [])):
        L += sign_text("%s_Text_Sign%d" % (folder, i), lines) + [""]
    L.append("`")
    open(P("data", "maps", folder, "scripts.pory"), "w").write("\n".join(L) + "\n")
    return layout, warps[0]


def write_centre(t):
    folder, const = t["folder"] + "_PokemonCenter_1F", t["const"]
    town = t["folder"]
    nurse = "LOCALID_%s_NURSE" % const
    m = json.load(open(P("data", "maps", "TelokTown_PokemonCenter_1F", "map.json")))
    keep = [o for o in m["object_events"] if o.get("local_id", "").endswith("_NURSE")
            or o.get("script") == "Common_EventScript_OrchidCafe"]
    for o in keep:
        if o.get("local_id", "").endswith("_NURSE"):
            o["local_id"], o["script"] = nurse, "%s_EventScript_Nurse" % folder
    m.update(id="MAP_%s_POKEMON_CENTER_1F" % const, name=folder, region_map_section=t["mapsec"],
             object_events=keep,
             warp_events=[dict(wv, dest_map="MAP_%s" % const, dest_warp_id="0")
                          for wv in m["warp_events"] if wv["dest_map"] == "MAP_OLDALE_TOWN"])
    os.makedirs(P("data", "maps", folder), exist_ok=True)
    json.dump(m, open(P("data", "maps", folder, "map.json"), "w"), indent=2)
    L = ["raw `",
         "%s_MapScripts::" % folder,
         "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % folder,
         "\tmap_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume",
         "\t.byte 0", "",
         "%s_OnTransition:" % folder,
         "\tsetrespawn HEAL_LOCATION_%s" % const,
         "\tend", "",
         "%s_EventScript_Nurse::" % folder,
         "\tsetvar VAR_0x800B, %s" % nurse,
         "\tcall Common_EventScript_PkmnCenterNurse",
         "\twaitmessage",
         "\twaitbuttonpress",
         "\trelease",
         "\tend",
         "`"]
    open(P("data", "maps", folder, "scripts.pory"), "w").write("\n".join(L) + "\n")
    return nurse


def main():
    layouts_js = json.load(open(P("data", "layouts", "layouts.json")))
    heal_js = json.load(open(P("src", "data", "heal_locations.json")))
    groups = json.load(open(P("data", "maps", "map_groups.json")))
    group_maps, new_layouts, new_heals = [], [], []
    for t in TOWNS:
        src_map = json.load(open(P("data", "maps", t["src"], "map.json")))
        src_entry, src_grid, border = read_layout(src_map["layout"])
        grid = build_grid(t, src_grid)
        layout, door = write_town(t, grid, border, src_entry, src_map)
        nurse = write_centre(t)
        hx, hy = heal_spot(t, src_map["id"])
        new_layouts.append(layout)
        new_heals.append({"id": "HEAL_LOCATION_%s" % t["const"], "map": "MAP_%s" % t["const"], "x": hx, "y": hy,
                          "respawn_map": "MAP_%s_POKEMON_CENTER_1F" % t["const"], "respawn_npc": nurse})
        group_maps += [t["folder"], t["folder"] + "_PokemonCenter_1F"]
        print("%-16s %dx%d  door (%d,%d)  lands (%d,%d)" % (t["folder"], layout["width"], layout["height"],
                                                          door["x"], door["y"], hx, hy))
    ids = {l["id"] for l in new_layouts}
    layouts_js["layouts"] = [l for l in layouts_js["layouts"] if l.get("id") not in ids] + new_layouts
    json.dump(layouts_js, open(P("data", "layouts", "layouts.json"), "w"), indent=2)
    open(P("data", "layouts", "layouts.json"), "a").write("\n")
    hids = {h["id"] for h in new_heals}
    heal_js["heal_locations"] = [h for h in heal_js["heal_locations"] if h["id"] not in hids] + new_heals
    json.dump(heal_js, open(P("src", "data", "heal_locations.json"), "w"), indent=2)
    open(P("src", "data", "heal_locations.json"), "a").write("\n")
    groups[GROUP] = group_maps
    if GROUP not in groups["group_order"]:
        groups["group_order"].append(GROUP)
    json.dump(groups, open(P("data", "maps", "map_groups.json"), "w"), indent=2)
    open(P("data", "maps", "map_groups.json"), "a").write("\n")
    # map scripts are .included by hand in data/event_scripts.s: one marked block, after ColdStorageTestOutside
    path = P("data", "event_scripts.s")
    lines = open(path).read().split("\n")
    lines = [l for l in lines if "@ tiksi-placeholder" not in l]
    at = next(i for i, l in enumerate(lines) if "data/maps/ColdStorageTestOutside/scripts.inc" in l) + 1
    lines[at:at] = ['\t.include "data/maps/%s/scripts.inc" @ tiksi-placeholder' % m for m in group_maps]
    open(path, "w").write("\n".join(lines))


if __name__ == "__main__":
    main()
