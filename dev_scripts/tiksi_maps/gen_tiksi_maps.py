"""
Tiksi maps from the approved round-1 designs (review: https://claude.ai/artifact/VqnifRPuMgLgHmUg7hf2Vw).

  towns  town_specs.py: Furong Village, Drake Base Camp, Ube City, Tanglyn Town (each + Pokémon Centre 1F)
  caves  cave_specs.py: Regolis Shrine, Frigo Cave, Ferrum Shrine, Gavani Path, Mt. Drake summit (one Regi each)

Layouts are composed only from metatiles that already exist in each tileset (compose.py), so no tileset
changes. Rerunning overwrites only what this script owns:
  data/layouts/<Map>/, LAYOUT_<MAP> entries in data/layouts/layouts.json
  data/maps/<Map>/ (map.json + scripts.pory), group gMapGroup_Tiksi in data/maps/map_groups.json
  HEAL_LOCATION_<TOWN> in src/data/heal_locations.json
  the "@ tiksi-maps" .include block in data/event_scripts.s
Town Centre doors / Centre + Mart signs are carried over from the vanilla maps the pieces come from; the
fly landing is two tiles below the door (as in every vanilla town). Other doors are scenery for now, and
there are no connections (no Tiksi routes yet). Cave exits lead to the nearest town's Centre door.

usage: python3 dev_scripts/tiksi_maps/gen_tiksi_maps.py   (needs a Python with Pillow: compose.py renders)
       python3 dev_scripts/tiksi_maps/town_specs.py OUT_DIR / cave_specs.py OUT_DIR   -> review mockups
"""
import glob
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compose        # noqa: E402
import town_specs     # noqa: E402
import cave_specs     # noqa: E402

ROOT = compose.ROOT
P = lambda *p: os.path.join(ROOT, *p)
GROUP = "gMapGroup_Tiksi"
MARK = "@ tiksi-maps"

# ---------------------------------------------------------------- per-map game data
SIGN = {"dew": ("LAYOUT_DEWFORD_TOWN", 10, 10), "lav": ("LAYOUT_LAVARIDGE_TOWN", 13, 8),
        "rus": ("LAYOUT_RUSTBORO_CITY", 19, 49), "lil": ("LAYOUT_LILYCOVE_CITY", 6, 15)}   # signpost metatiles

TOWNS = {
    "furong_village": dict(folder="FurongVillage", const="FURONG_VILLAGE", mapsec="MAPSEC_FURONG_VILLAGE",
                           music="MUS_DEWFORD", map_type="MAP_TYPE_TOWN",
                           signs=[((3, 12), SIGN["dew"], ["FURONG VILLAGE", "A fishing village on TIKSI's shore."])],
                           objects=[dict(graphics_id="OBJ_EVENT_GFX_MR_BRINEYS_BOAT", x=25, y=11,
                                         movement_type="MOVEMENT_TYPE_FACE_LEFT")]),
    "drake_base_camp": dict(folder="DrakeBaseCamp", const="DRAKE_BASE_CAMP", mapsec="MAPSEC_DRAKE_BASE_CAMP",
                            music="MUS_OLDALE", map_type="MAP_TYPE_TOWN",
                            signs=[((13, 21), SIGN["lav"], ["DRAKE BASE CAMP", "The last stop before MT. DRAKE."])]),
    "ube_city": dict(folder="UbeCity", const="UBE_CITY", mapsec="MAPSEC_UBE_CITY",
                     music="MUS_RUSTBORO", map_type="MAP_TYPE_CITY",
                     signs=[((14, 3), SIGN["rus"], ["UBE CITY", "TIKSI's only city."]),
                            ((23, 8), SIGN["rus"], ["SILPH CO. TIKSI SALES OFFICE", "Closed today."])]),
    "tanglyn_town": dict(folder="TanglynTown", const="TANGLYN_TOWN", mapsec="MAPSEC_TANGLYN_TOWN",
                         music="MUS_LILYCOVE", map_type="MAP_TYPE_TOWN",
                         signs=[((2, 14), SIGN["lil"], ["TANGLYN TOWN", "A quiet coastal town filled", "with ancient murals."]),
                                ((8, 9), SIGN["lil"], ["TANGLYN MURAL HALL", "Home of TIKSI's ancient murals.", "(Closed for restoration.)"])]),
}

CAVES = {
    "regolis_shrine": dict(folder="RegolisShrine", const="REGOLIS_SHRINE", mapsec="MAPSEC_REGOLIS_SHRINE",
                           species="REGIROCK", gfx="OBJ_EVENT_GFX_REGIROCK", hide="FLAG_HIDE_REGIROCK",
                           defeated="FLAG_DEFEATED_REGIROCK", exit_to="DRAKE_BASE_CAMP"),
    "frigo_cave": dict(folder="FrigoCave", const="FRIGO_CAVE", mapsec="MAPSEC_FRIGO_CAVE",
                       species="REGICE", gfx="OBJ_EVENT_GFX_REGICE", hide="FLAG_HIDE_REGICE",
                       defeated="FLAG_DEFEATED_REGICE", exit_to="TANGLYN_TOWN"),
    "ferrum_shrine": dict(folder="FerrumShrine", const="FERRUM_SHRINE", mapsec="MAPSEC_FERRUM_SHRINE",
                          species="REGISTEEL", gfx="OBJ_EVENT_GFX_REGISTEEL", hide="FLAG_HIDE_REGISTEEL",
                          defeated="FLAG_DEFEATED_REGISTEEL", exit_to="DRAKE_BASE_CAMP"),
    "gavani_path": dict(folder="GavaniPath", const="GAVANI_PATH", mapsec="MAPSEC_GAVANI_PATH",
                        species="REGIELEKI", gfx="OBJ_EVENT_GFX_SPECIES(REGIELEKI)", hide="FLAG_HIDE_REGIELEKI",
                        defeated="FLAG_DEFEATED_REGIELEKI", exit_to="FURONG_VILLAGE"),
    "mt_drake_summit": dict(folder="MtDrakeSummit", const="MT_DRAKE_SUMMIT", mapsec="MAPSEC_MT_DRAKE",
                            species="REGIDRAGO", gfx="OBJ_EVENT_GFX_SPECIES(REGIDRAGO)", hide="FLAG_HIDE_REGIDRAGO",
                            defeated="FLAG_DEFEATED_REGIDRAGO", exit_to="DRAKE_BASE_CAMP"),
}
REGI_LEVEL = 40


# ---------------------------------------------------------------- helpers
def maps_by_layout():
    out = {}
    for mj in glob.glob(P("data", "maps", "*", "map.json")):
        d = json.load(open(mj))
        out.setdefault(d["layout"], []).append(d)
    return out


def elevation(v):
    return (v >> 12) & 0xF


def obj(graphics_id, x, y, elev, movement_type="MOVEMENT_TYPE_FACE_DOWN", script="NULL", flag="0", local_id=None):
    o = {"graphics_id": graphics_id, "x": x, "y": y, "elevation": elev, "movement_type": movement_type,
         "movement_range_x": 0, "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
         "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}
    if local_id:
        o = {"local_id": local_id, **o}
    return o


def sign_text(label, lines):
    out = ["%s:" % label]
    for i, line in enumerate(lines):
        end = "$" if i == len(lines) - 1 else ("\\n" if i == 0 else "\\l")
        out.append('\t.string "%s%s"' % (line, end))
    return out


def write_layout(folder, const, spec, grid, layouts):
    h, w = len(grid), len(grid[0])
    os.makedirs(P("data", "layouts", folder), exist_ok=True)
    open(P("data", "layouts", folder, "map.bin"), "wb").write(struct.pack("<%dH" % (w * h), *[v for r in grid for v in r]))
    border_src = compose.raw_layout(spec["ground"][0] if "ground" in spec else spec["stamps"][0][0])[0]
    open(P("data", "layouts", folder, "border.bin"), "wb").write(open(P(border_src["border_filepath"]), "rb").read())
    entry = {"id": "LAYOUT_%s" % const, "name": "%s_Layout" % folder, "width": w, "height": h,
             "primary_tileset": spec["tileset"][0], "secondary_tileset": spec["tileset"][1],
             "border_filepath": "data/layouts/%s/border.bin" % folder,
             "blockdata_filepath": "data/layouts/%s/map.bin" % folder, "layout_version": "emerald"}
    layouts[entry["id"]] = entry
    return entry


def map_header(const, folder, layout_id, music, mapsec, map_type, weather="WEATHER_SUNNY"):
    return {"id": "MAP_%s" % const, "name": folder, "layout": layout_id, "music": music,
            "region": "REGION_HOENN",   # mapjson: emerald builds only take REGION_HOENN maps; Tiksi comes from the mapsec
            "region_map_section": mapsec, "requires_flash": False, "weather": weather, "map_type": map_type,
            "allow_cycling": True, "allow_escaping": map_type == "MAP_TYPE_UNDERGROUND", "allow_running": True,
            "show_map_name": True, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None,
            "object_events": [], "warp_events": [], "coord_events": [], "bg_events": []}


def write_map(folder, m, script_lines):
    os.makedirs(P("data", "maps", folder), exist_ok=True)
    json.dump(m, open(P("data", "maps", folder, "map.json"), "w"), indent=2)
    open(P("data", "maps", folder, "scripts.pory"), "w").write("\n".join(["raw `"] + script_lines + ["`"]) + "\n")


# ---------------------------------------------------------------- towns
def carried_events(spec, by_layout):
    """Centre door warps + Centre / Mart signs inside each stamp's source rect, in map coordinates."""
    doors, signs = [], []
    for lid, sx, sy, cw, chh, dx, dy in spec["stamps"]:
        for m in by_layout.get(lid, []):
            inside = lambda x, y: sx <= x < sx + cw and sy <= y < sy + chh
            for wv in m["warp_events"]:
                if wv["dest_map"].endswith("POKEMON_CENTER_1F") and inside(wv["x"], wv["y"]):
                    doors.append((wv["x"] - sx + dx, wv["y"] - sy + dy, wv["elevation"]))
            for b in m["bg_events"]:
                if b.get("type") == "sign" and inside(b["x"], b["y"]) and b.get("script") in (
                        "Common_EventScript_ShowPokemonCenterSign", "Common_EventScript_ShowPokemartSign"):
                    signs.append(dict(b, x=b["x"] - sx + dx, y=b["y"] - sy + dy))
    return doors, signs


def build_town(spec, meta, by_layout, layouts, heals, group):
    folder, const = meta["folder"], meta["const"]
    for (x, y), ref, _ in meta["signs"]:          # signposts are real metatiles: add them to the spec
        spec.setdefault("stamps", []).append((ref[0], ref[1], ref[2], 1, 1, x, y))
    grid, _, _ = compose.compose(spec)
    layout = write_layout(folder, const, spec, grid, layouts)
    doors, carried = carried_events(spec, by_layout)
    door = max(doors, key=lambda d: d[1])          # the front door (Lavaridge's Centre also has a back door)
    m = map_header(const, folder, layout["id"], meta["music"], meta["mapsec"], meta["map_type"])
    m["warp_events"] = [{"x": door[0], "y": door[1], "elevation": door[2],
                         "dest_map": "MAP_%s_POKEMON_CENTER_1F" % const, "dest_warp_id": "0"}]
    m["bg_events"] = carried + [{"type": "sign", "x": x, "y": y, "elevation": 0,
                                 "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                                 "script": "%s_EventScript_Sign%d" % (folder, i)}
                                for i, ((x, y), _, _) in enumerate(meta["signs"])]
    for o in meta.get("objects", []):
        m["object_events"].append(obj(o["graphics_id"], o["x"], o["y"], elevation(grid[o["y"]][o["x"]]),
                                      o.get("movement_type", "MOVEMENT_TYPE_FACE_DOWN")))
    L = ["%s_MapScripts::" % folder, "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % folder, "\t.byte 0", "",
         "%s_OnTransition:" % folder, "\tsetflag FLAG_VISITED_%s" % const, "\tend", ""]
    for i, (_, _, lines) in enumerate(meta["signs"]):
        L += ["%s_EventScript_Sign%d::" % (folder, i), "\tmsgbox %s_Text_Sign%d, MSGBOX_SIGN" % (folder, i), "\tend", ""]
    for i, (_, _, lines) in enumerate(meta["signs"]):
        L += sign_text("%s_Text_Sign%d" % (folder, i), lines) + [""]
    write_map(folder, m, L)
    heals["HEAL_LOCATION_%s" % const] = {"id": "HEAL_LOCATION_%s" % const, "map": "MAP_%s" % const,
                                         "x": door[0], "y": door[1] + 2,
                                         "respawn_map": "MAP_%s_POKEMON_CENTER_1F" % const,
                                         "respawn_npc": "LOCALID_%s_NURSE" % const}
    build_centre(meta)
    group += [folder, folder + "_PokemonCenter_1F"]
    return door


def build_centre(meta):
    folder, const = meta["folder"] + "_PokemonCenter_1F", meta["const"]
    nurse = "LOCALID_%s_NURSE" % const
    m = json.load(open(P("data", "maps", "TelokTown_PokemonCenter_1F", "map.json")))
    keep = [o for o in m["object_events"] if o.get("local_id", "").endswith("_NURSE")
            or o.get("script") == "Common_EventScript_OrchidCafe"]
    for o in keep:
        if o.get("local_id", "").endswith("_NURSE"):
            o["local_id"], o["script"] = nurse, "%s_EventScript_Nurse" % folder
    m.update(id="MAP_%s_POKEMON_CENTER_1F" % const, name=folder, region_map_section=meta["mapsec"],
             object_events=keep,
             warp_events=[dict(wv, dest_map="MAP_%s" % const, dest_warp_id="0")
                          for wv in m["warp_events"] if wv["dest_map"] == "MAP_OLDALE_TOWN"])
    write_map(folder, m, [
        "%s_MapScripts::" % folder,
        "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % folder,
        "\tmap_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume", "\t.byte 0", "",
        "%s_OnTransition:" % folder, "\tsetrespawn HEAL_LOCATION_%s" % const, "\tend", "",
        "%s_EventScript_Nurse::" % folder, "\tsetvar VAR_0x800B, %s" % nurse,
        "\tcall Common_EventScript_PkmnCenterNurse", "\twaitmessage", "\twaitbuttonpress", "\trelease", "\tend"])


# ---------------------------------------------------------------- caves
def build_cave(spec, meta, layouts, group):
    folder, const = meta["folder"], meta["const"]
    grid, _, _ = compose.compose(spec)
    regi = next((x, y) for x, y, _, kind in spec["marks"] if kind == "regi")
    # objects take their elevation from the tile under them, so the Regi's tile must match the tile the
    # player talks from (in Gavani Path the basin is 2, the causeway in front of Regieleki is 3)
    front = elevation(grid[regi[1] + 1][regi[0]])
    grid[regi[1]][regi[0]] = (grid[regi[1]][regi[0]] & 0x0FFF) | (front << 12)
    layout = write_layout(folder, const, spec, grid, layouts)
    exit_ = next((x, y) for x, y, _, kind in spec["marks"] if kind == "warp")
    m = map_header(const, folder, layout["id"], "MUS_SEALED_CHAMBER", meta["mapsec"], "MAP_TYPE_UNDERGROUND",
                   weather="WEATHER_NONE")
    # elevation = the tile the player talks from (just below the Regi): in Gavani Path the causeway is
    # elevation 3 while the basin under Regieleki is 2, and objects only interact on the same elevation
    m["object_events"] = [obj(meta["gfx"], regi[0], regi[1], elevation(grid[regi[1] + 1][regi[0]]),
                              script="%s_EventScript_Regi" % folder, flag=meta["hide"])]
    m["warp_events"] = [{"x": exit_[0], "y": exit_[1], "elevation": elevation(grid[exit_[1]][exit_[0]]),
                         "dest_map": "MAP_%s" % meta["exit_to"], "dest_warp_id": "0"}]
    sp, f = meta["species"], folder
    write_map(folder, m, [
        "%s_MapScripts::" % f,
        "\tmap_script MAP_SCRIPT_ON_RESUME, %s_OnResume" % f,
        "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % f, "\t.byte 0", "",
        "%s_OnResume:" % f, "\tcall_if_set FLAG_SYS_CTRL_OBJ_DELETE, %s_EventScript_TryRemoveRegi" % f, "\tend", "",
        "%s_EventScript_TryRemoveRegi::" % f, "\tspecialvar VAR_RESULT, GetBattleOutcome",
        "\tgoto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn",
        "\tremoveobject VAR_LAST_TALKED", "\treturn", "",
        "%s_OnTransition:" % f, "\tcall_if_unset %s, %s_EventScript_ShowRegi" % (meta["defeated"], f), "\tend", "",
        "%s_EventScript_ShowRegi::" % f, "\tclearflag %s" % meta["hide"], "\treturn", "",
        "%s_EventScript_Regi::" % f, "\tlock", "\tfaceplayer", "\twaitse",
        "\tplaymoncry SPECIES_%s, CRY_MODE_ENCOUNTER" % sp, "\tdelay 40", "\twaitmoncry",
        "\tsetwildbattle SPECIES_%s, %d" % (sp, REGI_LEVEL),
        "\tsetflag FLAG_SYS_CTRL_OBJ_DELETE", "\tspecial StartRegiBattle", "\tclearflag FLAG_SYS_CTRL_OBJ_DELETE",
        "\tspecialvar VAR_RESULT, GetBattleOutcome",
        "\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, %s_EventScript_DefeatedRegi" % f,
        "\tgoto_if_eq VAR_RESULT, B_OUTCOME_RAN, %s_EventScript_RanFromRegi" % f,
        "\tgoto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, %s_EventScript_RanFromRegi" % f,
        "\tsetflag %s" % meta["defeated"], "\trelease", "\tend", "",
        "%s_EventScript_DefeatedRegi::" % f, "\tsetflag %s" % meta["defeated"],
        "\tgoto Common_EventScript_RemoveStaticPokemon", "\tend", "",
        "%s_EventScript_RanFromRegi::" % f, "\tsetvar VAR_0x8004, SPECIES_%s" % sp,
        "\tgoto Common_EventScript_LegendaryFlewAway", "\tend"])
    group.append(folder)
    return regi, exit_


# ---------------------------------------------------------------- main
def main():
    by_layout = maps_by_layout()
    layouts_js = json.load(open(P("data", "layouts", "layouts.json")))
    heal_js = json.load(open(P("src", "data", "heal_locations.json")))
    groups = json.load(open(P("data", "maps", "map_groups.json")))
    layouts, heals, group = {}, {}, []
    for spec in town_specs.TOWNS:
        meta = TOWNS[spec["slug"]]
        door = build_town(dict(spec, stamps=list(spec["stamps"])), meta, by_layout, layouts, heals, group)
        print("%-16s door (%d,%d) lands (%d,%d)" % (meta["folder"], door[0], door[1], door[0], door[1] + 2))
    for spec in cave_specs.CAVES:
        meta = CAVES[spec["slug"]]
        regi, exit_ = build_cave(spec, meta, layouts, group)
        print("%-16s %s at %s, exit %s -> %s" % (meta["folder"], meta["species"], regi, exit_, meta["exit_to"]))
    layouts_js["layouts"] = [l for l in layouts_js["layouts"] if l.get("id") not in layouts] + list(layouts.values())
    json.dump(layouts_js, open(P("data", "layouts", "layouts.json"), "w"), indent=2)
    open(P("data", "layouts", "layouts.json"), "a").write("\n")
    heal_js["heal_locations"] = [h for h in heal_js["heal_locations"] if h["id"] not in heals] + list(heals.values())
    json.dump(heal_js, open(P("src", "data", "heal_locations.json"), "w"), indent=2)
    open(P("src", "data", "heal_locations.json"), "a").write("\n")
    groups[GROUP] = group
    if GROUP not in groups["group_order"]:
        groups["group_order"].append(GROUP)
    json.dump(groups, open(P("data", "maps", "map_groups.json"), "w"), indent=2)
    open(P("data", "maps", "map_groups.json"), "a").write("\n")
    path = P("data", "event_scripts.s")
    lines = [l for l in open(path).read().split("\n") if MARK not in l and "@ tiksi-placeholder" not in l]
    at = next(i for i, l in enumerate(lines) if "data/maps/ColdStorageTestOutside/scripts.inc" in l) + 1
    lines[at:at] = ['\t.include "data/maps/%s/scripts.inc" %s' % (m, MARK) for m in group]
    open(path, "w").write("\n".join(lines))


if __name__ == "__main__":
    main()
