"""
Sailor's Voyages, core stream: map.json events, map registration and scripts for the batch-1 maps.
Run after build_core_maps.py. Idempotent (re-running rewrites the new maps and re-merges the edits).

  * new group gMapGroup_Voyages (appended after gMapGroup_Tiksi): WavebreakTown_SailorsHut, NewmoonIsland,
    NewmoonIsland_Interior, FullmoonIsland, FullmoonIsland_Interior
  * WavebreakTown: hut door warp (13,29) = warp 6, dock Sailor + boat (shown after the Champion), three more
    fishermen with the NOTES.md flavour lines, ON_TRANSITION hiding the dock pair before FLAG_SYS_GAME_CLEAR
  * SouthernIsland_Exterior/Interior = Eon Island: boat + voyage Sailor; Latias by day / Latios by night;
    Latiasite / Latiosite item balls after each catch
usage: python3 dev_scripts/voyages/core/build_core_events.py
"""
import json
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)       # noqa: E731
GROUP = "gMapGroup_Voyages"
NEW_MAPS = ["WavebreakTown_SailorsHut", "NewmoonIsland", "NewmoonIsland_Interior", "FullmoonIsland",
            "FullmoonIsland_Interior"]


def load(path):
    return json.load(open(path), object_pairs_hook=OrderedDict)


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def obj(gfx, x, y, elev, move, script, flag="0", local_id=None, item=None):
    o = OrderedDict()
    if local_id:
        o["local_id"] = local_id
    o.update([("graphics_id", gfx), ("x", x), ("y", y), ("elevation", elev), ("movement_type", move),
              ("movement_range_x", 0), ("movement_range_y", 0), ("trainer_type", "TRAINER_TYPE_NONE"),
              ("trainer_sight_or_berry_tree_id", item or "0"), ("script", script), ("flag", flag)])
    return o


def warp(x, y, dest, wid, elev=0):
    return OrderedDict([("x", x), ("y", y), ("elevation", elev), ("dest_map", dest), ("dest_warp_id", str(wid))])


def header(mid, name, layout, music, sec, weather, mtype, indoor=False):
    return OrderedDict([
        ("id", mid), ("name", name), ("layout", layout), ("music", music), ("region", "REGION_HOENN"),
        ("region_map_section", sec), ("requires_flash", False), ("weather", weather), ("map_type", mtype),
        ("allow_cycling", not indoor), ("allow_escaping", False), ("allow_running", not indoor),
        ("show_map_name", not indoor), ("battle_scene", "MAP_BATTLE_SCENE_NORMAL"), ("connections", None)])


def trigger(x, y, script, elev=3):
    return OrderedDict([("type", "trigger"), ("x", x), ("y", y), ("elevation", elev), ("var", "VAR_TEMP_0"),
                        ("var_value", "0"), ("script", script)])


# General + Dewford has no sand / forest-gap metatile with a warp behaviour (only 0x024 grass arrow, 0x0A7 cave
# door, 0x354 Dewford door), so Newmoon's entrance and exit are coord triggers that `warp`; the warp events
# there are only the arrival cells, placed beside the triggers.
WARP_SCRIPT = "\n{label}::\n\tlockall\n\twarp {dest}, {wid}\n\twaitstate\n\treleaseall\n\tend\n"


def write_map(name, m, objects, warps, bgs, pory, coords=()):
    m["object_events"] = objects
    m["warp_events"] = warps
    m["coord_events"] = list(coords)
    m["bg_events"] = bgs
    save(P("data", "maps", name, "map.json"), m)
    with open(P("data", "maps", name, "scripts.pory"), "w") as f:
        f.write(pory)
    inc = P("data", "maps", name, "scripts.inc")
    if os.path.exists(inc):
        os.remove(inc)     # same-second mtimes can leave a stale scripts.inc


# ---------------------------------------------------------------------------------------------- hut
HUT_PORY = '''mapscripts WavebreakTown_SailorsHut_MapScripts {
    // After the Champion the Sailor waits at the dock with his boat (WavebreakTown), so he isn't home.
    MAP_SCRIPT_ON_TRANSITION {
        if (flag(FLAG_SYS_GAME_CLEAR)) {
            setflag(FLAG_TEMP_1)
        }
    }
}

script WavebreakTown_SailorsHut_EventScript_Son {
    lock
    faceplayer
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("Dad's down at the dock with the boat. He says you know the secret words now!"))
    } else {
        msgbox(format("My dad sailed to islands nobody's ever heard of. He says they only open up if you know the secret words."))
    }
    release
}
'''


# ---------------------------------------------------------------------------------------------- islands
def legendary_pory(prefix, species, caught_flag, local_id):
    return '''
{p}_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, {p}_EventScript_TryRemove{s}
	end

{p}_EventScript_TryRemove{s}::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject {lid}
	return

{p}_EventScript_{s}::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_{S}, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_{S}, VOYAGE_LEGENDARY_LEVEL
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {p}_EventScript_{s}Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {p}_EventScript_{s}Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {p}_EventScript_{s}Gone
	setflag {caught}
	release
	end

@ Fainted or fled: its hide flag (the object's flag) stays set until the next voyage here (Voyage_Depart).
{p}_EventScript_{s}Gone::
	setvar VAR_0x8004, SPECIES_{S}
	goto Voyage_EventScript_LegendaryGone
'''.format(p=prefix, s=species.capitalize(), S=species.upper(), caught=caught_flag, lid=local_id)


def island_pory(ext, intr, sign_text):
    return "mapscripts %s_MapScripts {}\n" % ext


def interior_pory(name, species, caught_flag, local_id, extra=""):
    return 'raw `\n{n}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_RESUME, {n}_OnResume\n\t.byte 0\n'.format(n=name) + \
        legendary_pory(name, species, caught_flag, local_id) + extra + '`\n'


# ---------------------------------------------------------------------------------------------- Eon
EON_INT_PORY = r'''raw `
@ Orchid: Eon Island (vanilla Southern Island). Voyage legendary: Latias by day, Latios at night (gettimeofday),
@ each until caught; a fainted/fled one returns on the next voyage (src/voyages.c clears its hide flag).
@ The mega stone item balls appear once their Lati is caught.
SouthernIsland_Interior_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, SouthernIsland_Interior_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, SouthernIsland_Interior_OnTransition
	.byte 0

SouthernIsland_Interior_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, SouthernIsland_Interior_EventScript_TryRemoveLati
	end

SouthernIsland_Interior_EventScript_TryRemoveLati::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject LOCALID_SOUTHERN_ISLAND_LATI
	return

SouthernIsland_Interior_OnTransition:
	gettimeofday
	call_if_eq VAR_0x8000, TIME_NIGHT, SouthernIsland_Interior_EventScript_SetUpLatios
	call_if_ne VAR_0x8000, TIME_NIGHT, SouthernIsland_Interior_EventScript_SetUpLatias
	call SouthernIsland_Interior_EventScript_SetUpPlayerGfx
	call_if_unset FLAG_CAUGHT_VOYAGE_LATIAS, SouthernIsland_Interior_EventScript_HideLatiasite
	call_if_set FLAG_ITEM_EON_ISLAND_LATIASITE, SouthernIsland_Interior_EventScript_HideLatiasite
	call_if_unset FLAG_CAUGHT_VOYAGE_LATIOS, SouthernIsland_Interior_EventScript_HideLatiosite
	call_if_set FLAG_ITEM_EON_ISLAND_LATIOSITE, SouthernIsland_Interior_EventScript_HideLatiosite
	end

SouthernIsland_Interior_EventScript_HideLatiasite::
	setflag FLAG_TEMP_3
	return

SouthernIsland_Interior_EventScript_HideLatiosite::
	setflag FLAG_TEMP_4
	return

SouthernIsland_Interior_EventScript_SetUpLatios::
	setvar VAR_OBJ_GFX_ID_1, OBJ_EVENT_GFX_LATIOS
	setvar VAR_TEMP_4, SPECIES_LATIOS
	return

SouthernIsland_Interior_EventScript_SetUpLatias::
	setvar VAR_OBJ_GFX_ID_1, OBJ_EVENT_GFX_LATIAS
	setvar VAR_TEMP_4, SPECIES_LATIAS
	return

SouthernIsland_Interior_EventScript_SetUpPlayerGfx::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, SouthernIsland_Interior_EventScript_SetBrendanGfx
	goto_if_eq VAR_RESULT, FEMALE, SouthernIsland_Interior_EventScript_SetMayGfx
	end

SouthernIsland_Interior_EventScript_SetBrendanGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	return

SouthernIsland_Interior_EventScript_SetMayGfx::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	return

SouthernIsland_Interior_EventScript_TryLatiEncounter::
	lockall
	goto_if_set FLAG_TEMP_2, SouthernIsland_Interior_EventScript_Sign
	goto_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_CheckLatios
	goto_if_set FLAG_HIDE_EON_LATIAS, SouthernIsland_Interior_EventScript_Sign
	goto SouthernIsland_Interior_EventScript_Lati

SouthernIsland_Interior_EventScript_CheckLatios::
	goto_if_set FLAG_HIDE_EON_LATIOS, SouthernIsland_Interior_EventScript_Sign
SouthernIsland_Interior_EventScript_Lati::
	setflag FLAG_ENCOUNTERED_LATIAS_OR_LATIOS
	setflag FLAG_TEMP_2
	special SpawnCameraObject
	applymovement LOCALID_CAMERA, SouthernIsland_Interior_Movement_CameraPanUp
	waitmovement 0
	delay 50
	waitse
	playmoncry VAR_TEMP_4, CRY_MODE_NORMAL
	delay 30
	waitmoncry
	addobject LOCALID_SOUTHERN_ISLAND_LATI
	delay 30
	applymovement LOCALID_CAMERA, SouthernIsland_Interior_Movement_CameraPanDown
	applymovement LOCALID_SOUTHERN_ISLAND_LATI, SouthernIsland_Interior_Movement_LatiApproach
	waitmovement 0
	delay 50
	special RemoveCameraObject
	setvar VAR_LAST_TALKED, LOCALID_SOUTHERN_ISLAND_LATI
	call_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_SetLatiosBattleVars
	call_if_ne VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_SetLatiasBattleVars
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	call_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_LatiosGone
	call_if_ne VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_LatiasGone
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SouthernIsland_Interior_EventScript_LatiFlewAway
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SouthernIsland_Interior_EventScript_LatiFlewAway
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SouthernIsland_Interior_EventScript_LatiFlewAway
	goto_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_CaughtLatios
	setflag FLAG_CAUGHT_VOYAGE_LATIAS
	goto_if_set FLAG_ITEM_EON_ISLAND_LATIASITE, SouthernIsland_Interior_EventScript_CaughtDone
	clearflag FLAG_TEMP_3
	addobject LOCALID_EON_LATIASITE
	goto SouthernIsland_Interior_EventScript_CaughtDone

SouthernIsland_Interior_EventScript_CaughtLatios::
	setflag FLAG_CAUGHT_VOYAGE_LATIOS
	goto_if_set FLAG_ITEM_EON_ISLAND_LATIOSITE, SouthernIsland_Interior_EventScript_CaughtDone
	clearflag FLAG_TEMP_4
	addobject LOCALID_EON_LATIOSITE
SouthernIsland_Interior_EventScript_CaughtDone::
	releaseall
	end

@ Whatever the outcome, this Lati is gone until the next voyage (or for good once caught).
SouthernIsland_Interior_EventScript_LatiasGone::
	setflag FLAG_HIDE_EON_LATIAS
	return

SouthernIsland_Interior_EventScript_LatiosGone::
	setflag FLAG_HIDE_EON_LATIOS
	return

SouthernIsland_Interior_EventScript_LatiFlewAway::
	copyvar VAR_0x8004, VAR_TEMP_4
	goto Voyage_EventScript_LegendaryGone
	end

SouthernIsland_Interior_EventScript_Sign::
	msgbox SouthernIsland_Interior_Text_Sign, MSGBOX_DEFAULT
	releaseall
	end

SouthernIsland_Interior_EventScript_SetLatiosBattleVars::
	setwildbattle SPECIES_LATIOS, VOYAGE_LEGENDARY_LEVEL
	return

SouthernIsland_Interior_EventScript_SetLatiasBattleVars::
	setwildbattle SPECIES_LATIAS, VOYAGE_LEGENDARY_LEVEL
	return

SouthernIsland_Interior_EventScript_Latiasite::
	finditem ITEM_LATIASITE
	goto_if_eq VAR_0x8007, FALSE, SouthernIsland_Interior_EventScript_ItemEnd
	setflag FLAG_ITEM_EON_ISLAND_LATIASITE
	end

SouthernIsland_Interior_EventScript_Latiosite::
	finditem ITEM_LATIOSITE
	goto_if_eq VAR_0x8007, FALSE, SouthernIsland_Interior_EventScript_ItemEnd
	setflag FLAG_ITEM_EON_ISLAND_LATIOSITE
SouthernIsland_Interior_EventScript_ItemEnd::
	end

SouthernIsland_Interior_Movement_CameraPanUp:
	walk_up
	walk_up
	walk_up
	step_end

SouthernIsland_Interior_Movement_CameraPanDown:
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	delay_16
	walk_down
	walk_down
	walk_down
	walk_in_place_faster_up
	step_end

SouthernIsland_Interior_Movement_LatiApproach:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	delay_16
	delay_16
	walk_down
	walk_down
	walk_down
	walk_down
	step_end
`
'''

EON_EXT_PORY = r'''raw `
@ Orchid: Eon Island (vanilla Southern Island). The voyage Sailor and his boat wait at the old ferry dock.
SouthernIsland_Exterior_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SouthernIsland_Exterior_OnTransition
	.byte 0

SouthernIsland_Exterior_OnTransition:
	setflag FLAG_LANDMARK_SOUTHERN_ISLAND
	end

@ Used by Common_EventScript_FerryDepartIsland (data/event_scripts.s).
Ferry_EventScript_DepartIslandSouth::
	applymovement LOCALID_PLAYER, Ferry_Movement_DepartIslandBoardSouth
	waitmovement 0
	return

Ferry_EventScript_DepartIslandWest::
	applymovement LOCALID_PLAYER, Ferry_Movement_DepartIslandBoardWest
	waitmovement 0
	return

Ferry_Movement_DepartIslandBoardSouth:
	walk_down
	step_end

Ferry_Movement_DepartIslandBoardWest:
	walk_left
	walk_in_place_faster_down
	step_end

SouthernIsland_Exterior_EventScript_Sign::
	msgbox SouthernIsland_Exterior_Text_Sign, MSGBOX_SIGN
	end
`
'''

FISHER_LINES = {
    "Npc5": "The fish bite best under these trees at the north end. Shade on the water, see?",
    "Npc6": "Left my spare rods by the Centre. If they're gone, so's my luck.",
    "Npc7": "That old sailor's boat goes places my line never reaches. Wonder what bites out there.",
}


def wavebreak():
    path = P("data", "maps", "WavebreakTown", "map.json")
    m = load(path)
    objs = [o for o in m["object_events"] if not str(o.get("script", "")).startswith(("Voyage_", "WavebreakTown_EventScript_Npc5", "WavebreakTown_EventScript_Npc6", "WavebreakTown_EventScript_Npc7"))
            and o.get("local_id") != "LOCALID_WAVEBREAK_BOAT"]
    objs += [
        obj("OBJ_EVENT_GFX_FISHERMAN", 11, 10, 3, "MOVEMENT_TYPE_FACE_LEFT", "WavebreakTown_EventScript_Npc5"),
        obj("OBJ_EVENT_GFX_FISHERMAN", 11, 17, 3, "MOVEMENT_TYPE_FACE_LEFT", "WavebreakTown_EventScript_Npc6"),
        obj("OBJ_EVENT_GFX_FISHERMAN", 8, 30, 3, "MOVEMENT_TYPE_FACE_DOWN", "WavebreakTown_EventScript_Npc7"),
        obj("OBJ_EVENT_GFX_SAILOR", 4, 29, 3, "MOVEMENT_TYPE_FACE_DOWN", "Voyage_EventScript_Sailor", "FLAG_TEMP_1",
            local_id="LOCALID_WAVEBREAK_VOYAGE_SAILOR"),
        obj("OBJ_EVENT_GFX_MR_BRINEYS_BOAT", 4, 31, 1, "MOVEMENT_TYPE_FACE_UP", "0x0", "FLAG_TEMP_1",
            local_id="LOCALID_WAVEBREAK_BOAT"),
    ]
    m["object_events"] = objs
    warps = [w for w in m["warp_events"] if w["dest_map"] != "MAP_WAVEBREAK_TOWN_SAILORS_HUT"]
    assert len(warps) == 6, len(warps)
    warps.append(warp(13, 29, "MAP_WAVEBREAK_TOWN_SAILORS_HUT", 0))
    m["warp_events"] = warps
    save(path, m)
    pory_path = P("data", "maps", "WavebreakTown", "scripts.pory")
    s = open(pory_path).read()
    old_ms = "mapscripts WavebreakTown_MapScripts {\n}\n"
    new_ms = ("mapscripts WavebreakTown_MapScripts {\n"
              "    // Orchid voyages: the Sailor and his boat wait at the dock only after the Champion.\n"
              "    MAP_SCRIPT_ON_TRANSITION {\n"
              "        if (!flag(FLAG_SYS_GAME_CLEAR)) {\n"
              "            setflag(FLAG_TEMP_1)\n"
              "        }\n"
              "    }\n"
              "}\n")
    if old_ms in s:
        s = s.replace(old_ms, new_ms)
    assert new_ms in s
    for k, line in FISHER_LINES.items():
        label = "WavebreakTown_EventScript_" + k
        if label not in s:
            s += '\nscript %s {\n    msgbox(format("%s"), MSGBOX_NPC)\n}\n' % (label, line)
    open(pory_path, "w").write(s)
    inc = P("data", "maps", "WavebreakTown", "scripts.inc")
    if os.path.exists(inc):
        os.remove(inc)


def eon():
    path = P("data", "maps", "SouthernIsland_Exterior", "map.json")
    m = load(path)
    m["region_map_section"] = "MAPSEC_EON_ISLAND"
    m["object_events"] = [
        obj("OBJ_EVENT_GFX_SAILOR", 13, 23, 3, "MOVEMENT_TYPE_FACE_DOWN", "Voyage_EventScript_Sailor",
            local_id="LOCALID_SOUTHERN_ISLAND_SAILOR"),
        obj("OBJ_EVENT_GFX_MR_BRINEYS_BOAT", 13, 25, 1, "MOVEMENT_TYPE_FACE_UP", "0x0", local_id="LOCALID_EON_ISLAND_BOAT"),
    ]
    save(path, m)
    open(P("data", "maps", "SouthernIsland_Exterior", "scripts.pory"), "w").write(EON_EXT_PORY)
    path = P("data", "maps", "SouthernIsland_Interior", "map.json")
    m = load(path)
    m["region_map_section"] = "MAPSEC_EON_ISLAND"
    keep = [o for o in m["object_events"] if o.get("local_id") not in ("LOCALID_EON_LATIASITE", "LOCALID_EON_LATIOSITE")]
    keep += [
        obj("OBJ_EVENT_GFX_ITEM_BALL", 8, 8, 3, "MOVEMENT_TYPE_LOOK_AROUND", "SouthernIsland_Interior_EventScript_Latiasite",
            "FLAG_TEMP_3", local_id="LOCALID_EON_LATIASITE"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", 18, 8, 3, "MOVEMENT_TYPE_LOOK_AROUND", "SouthernIsland_Interior_EventScript_Latiosite",
            "FLAG_TEMP_4", local_id="LOCALID_EON_LATIOSITE"),
    ]
    m["object_events"] = keep
    save(path, m)
    open(P("data", "maps", "SouthernIsland_Interior", "scripts.pory"), "w").write(EON_INT_PORY)
    for n in ("SouthernIsland_Exterior", "SouthernIsland_Interior"):
        inc = P("data", "maps", n, "scripts.inc")
        if os.path.exists(inc):
            os.remove(inc)


def new_maps():
    hut = header("MAP_WAVEBREAK_TOWN_SAILORS_HUT", "WavebreakTown_SailorsHut", "LAYOUT_WAVEBREAK_TOWN_SAILORS_HUT",
                 "MUS_DEWFORD", "MAPSEC_WAVEBREAK_TOWN", "WEATHER_NONE", "MAP_TYPE_INDOOR", indoor=True)
    write_map("WavebreakTown_SailorsHut", hut, [
        obj("OBJ_EVENT_GFX_SAILOR", 5, 4, 3, "MOVEMENT_TYPE_FACE_DOWN", "Voyage_EventScript_Sailor", "FLAG_TEMP_1",
            local_id="LOCALID_SAILORS_HUT_SAILOR"),
        obj("OBJ_EVENT_GFX_LITTLE_BOY", 9, 5, 3, "MOVEMENT_TYPE_FACE_LEFT", "WavebreakTown_SailorsHut_EventScript_Son",
            local_id="LOCALID_SAILORS_HUT_SON"),
    ], [warp(5, 8, "MAP_WAVEBREAK_TOWN", 6), warp(6, 8, "MAP_WAVEBREAK_TOWN", 6)], [], HUT_PORY)

    nm = header("MAP_NEWMOON_ISLAND", "NewmoonIsland", "LAYOUT_NEWMOON_ISLAND", "MUS_MT_PYRE_EXTERIOR",
                "MAPSEC_NEWMOON_ISLAND", "WEATHER_SHADE", "MAP_TYPE_ROUTE")
    write_map("NewmoonIsland", nm, [
        obj("OBJ_EVENT_GFX_SAILOR", 18, 15, 3, "MOVEMENT_TYPE_FACE_RIGHT", "Voyage_EventScript_Sailor",
            local_id="LOCALID_NEWMOON_SAILOR"),
        obj("OBJ_EVENT_GFX_MR_BRINEYS_BOAT", 20, 15, 1, "MOVEMENT_TYPE_FACE_LEFT", "0x0", local_id="LOCALID_NEWMOON_BOAT"),
    ], [warp(10, 7, "MAP_NEWMOON_ISLAND_INTERIOR", 0, 3), warp(11, 7, "MAP_NEWMOON_ISLAND_INTERIOR", 1, 3)], [],
        "raw `\nNewmoonIsland_MapScripts::\n\t.byte 0\n" +
        WARP_SCRIPT.format(label="NewmoonIsland_EventScript_EnterForest", dest="MAP_NEWMOON_ISLAND_INTERIOR", wid=0) +
        WARP_SCRIPT.format(label="NewmoonIsland_EventScript_EnterForest2", dest="MAP_NEWMOON_ISLAND_INTERIOR", wid=1) + "`\n",
        coords=[trigger(10, 6, "NewmoonIsland_EventScript_EnterForest"),
                trigger(11, 6, "NewmoonIsland_EventScript_EnterForest2")])
    nmi = header("MAP_NEWMOON_ISLAND_INTERIOR", "NewmoonIsland_Interior", "LAYOUT_NEWMOON_ISLAND_INTERIOR",
                 "MUS_MT_PYRE_EXTERIOR", "MAPSEC_NEWMOON_ISLAND", "WEATHER_SHADE", "MAP_TYPE_ROUTE")
    write_map("NewmoonIsland_Interior", nmi, [
        # (13,13): in the crater gap at the pond's edge, faced from (13,14). The mock's (13,10) sat in the middle
        # of the pond with no dry cell next to it, and an object on water takes the water's elevation, so it
        # can't be talked to from the shore
        obj("OBJ_EVENT_GFX_SPECIES(DARKRAI)", 13, 13, 3, "MOVEMENT_TYPE_FACE_DOWN",
            "NewmoonIsland_Interior_EventScript_Darkrai", "FLAG_HIDE_NEWMOON_DARKRAI", local_id="LOCALID_NEWMOON_DARKRAI"),
    ], [warp(13, 20, "MAP_NEWMOON_ISLAND", 0, 3), warp(14, 20, "MAP_NEWMOON_ISLAND", 1, 3)], [],
        interior_pory("NewmoonIsland_Interior", "darkrai", "FLAG_CAUGHT_VOYAGE_DARKRAI", "LOCALID_NEWMOON_DARKRAI",
                      WARP_SCRIPT.format(label="NewmoonIsland_Interior_EventScript_Leave", dest="MAP_NEWMOON_ISLAND", wid=0) +
                      WARP_SCRIPT.format(label="NewmoonIsland_Interior_EventScript_Leave2", dest="MAP_NEWMOON_ISLAND", wid=1)),
        coords=[trigger(13, 21, "NewmoonIsland_Interior_EventScript_Leave"),
                trigger(14, 21, "NewmoonIsland_Interior_EventScript_Leave2")])

    fm = header("MAP_FULLMOON_ISLAND", "FullmoonIsland", "LAYOUT_FULLMOON_ISLAND", "MUS_ABANDONED_SHIP",
                "MAPSEC_FULLMOON_ISLAND", "WEATHER_NONE", "MAP_TYPE_ROUTE")
    write_map("FullmoonIsland", fm, [
        obj("OBJ_EVENT_GFX_SAILOR", 11, 16, 3, "MOVEMENT_TYPE_FACE_DOWN", "Voyage_EventScript_Sailor",
            local_id="LOCALID_FULLMOON_SAILOR"),
        obj("OBJ_EVENT_GFX_MR_BRINEYS_BOAT", 11, 18, 1, "MOVEMENT_TYPE_FACE_UP", "0x0", local_id="LOCALID_FULLMOON_BOAT"),
    ], [warp(20, 6, "MAP_FULLMOON_ISLAND_INTERIOR", 0, 3), warp(21, 6, "MAP_FULLMOON_ISLAND_INTERIOR", 1, 3)], [],
        island_pory("FullmoonIsland", "FullmoonIsland_Interior", ""))
    fmi = header("MAP_FULLMOON_ISLAND_INTERIOR", "FullmoonIsland_Interior", "LAYOUT_FULLMOON_ISLAND_INTERIOR",
                 "MUS_ABANDONED_SHIP", "MAPSEC_FULLMOON_ISLAND", "WEATHER_NONE", "MAP_TYPE_ROUTE")
    write_map("FullmoonIsland_Interior", fmi, [
        obj("OBJ_EVENT_GFX_SPECIES(CRESSELIA)", 11, 7, 3, "MOVEMENT_TYPE_FACE_RIGHT",
            "FullmoonIsland_Interior_EventScript_Cresselia", "FLAG_HIDE_FULLMOON_CRESSELIA",
            local_id="LOCALID_FULLMOON_CRESSELIA"),
    ], [warp(12, 14, "MAP_FULLMOON_ISLAND", 0, 3), warp(13, 14, "MAP_FULLMOON_ISLAND", 1, 3)], [],
        interior_pory("FullmoonIsland_Interior", "cresselia", "FLAG_CAUGHT_VOYAGE_CRESSELIA",
                      "LOCALID_FULLMOON_CRESSELIA"))


def register():
    mg_path = P("data", "maps", "map_groups.json")
    mg = load(mg_path)
    if GROUP not in mg["group_order"]:
        i = mg["group_order"].index("gMapGroup_Tiksi")
        mg["group_order"].insert(i + 1, GROUP)
    lst = mg.setdefault(GROUP, [])
    for n in NEW_MAPS:
        if n not in lst:
            lst.append(n)
    # keep the group right after gMapGroup_Tiksi in the file too
    out = OrderedDict()
    for k, v in mg.items():
        if k == GROUP:
            continue
        out[k] = v
        if k == "gMapGroup_Tiksi":
            out[GROUP] = mg[GROUP]
    save(mg_path, out)
    es_path = P("data", "event_scripts.s")
    es = open(es_path).read()
    anchor = '\t.include "data/maps/FrigoCave_Exterior/scripts.inc" @ tiksi-routes\n'
    assert anchor in es
    add = "".join('\t.include "data/maps/%s/scripts.inc" @ voyages\n' % n for n in NEW_MAPS
                  if 'data/maps/%s/scripts.inc"' % n not in es)
    es = es.replace(anchor, anchor + add)
    if '"data/scripts/voyages.inc"' not in es:
        a2 = '\t.include "data/scripts/train.inc"\n'
        assert a2 in es
        es = es.replace(a2, a2 + '\t.include "data/scripts/voyages.inc"\n')
    if '"constants/voyages.h"' not in es:
        a3 = '#include "constants/seagallop.h"\n'
        es = es.replace(a3, a3 + '#include "constants/voyages.h"\n')
    open(es_path, "w").write(es)


if __name__ == "__main__":
    new_maps()
    wavebreak()
    eon()
    register()
    print("events written")
