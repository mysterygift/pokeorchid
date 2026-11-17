#!/usr/bin/env python3
"""Writes data/maps/ColdStorageTest/map.json and data/maps/ColdStorageTestOutside/map.json from the
positions in test_map.py, so the events can never drift from the layout the solver checked.
Re-running overwrites Porymap edits to those two files (scripts.pory is hand-written and untouched)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_map as T                                    # noqa: E402
import export_exterior as X                             # noqa: E402
from kit import ROOT                                    # noqa: E402


TOSA_PORT_DOOR_WARP = "4"      # index of the (27, 9) warp in data/maps/TosaPort/map.json


def obj(gfx, pos, script, facing="DOWN", flag="0", trainer=0, local_id=None):
    o = {}
    if local_id:
        o["local_id"] = local_id
    o.update({
        "graphics_id": gfx, "x": pos[0], "y": pos[1], "elevation": 3,
        "movement_type": f"MOVEMENT_TYPE_FACE_{facing}", "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NORMAL" if trainer else "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": str(trainer), "script": script, "flag": flag,
    })
    return o


def header(map_id, name, layout, music, map_type, show_name):
    return {
        "id": map_id, "name": name, "layout": layout, "music": music, "region": "REGION_HOENN",
        "region_map_section": "MAPSEC_TOSA_PORT", "requires_flash": False, "weather": "WEATHER_NONE",
        "map_type": map_type, "allow_cycling": False, "allow_escaping": False, "allow_running": True,
        "show_map_name": show_name, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None,
    }


def interior():
    n, p = T.NPCS, "ColdStorageTest_EventScript_"
    balls = {v: k for k, v in T.ITEM_BALLS.items()}
    m = header("MAP_COLD_STORAGE_TEST", "ColdStorageTest", "LAYOUT_COLD_STORAGE_TEST",
               "MUS_AQUA_MAGMA_HIDEOUT", "MAP_TYPE_INDOOR", False)
    m["object_events"] = [
        obj("OBJ_EVENT_GFX_SCIENTIST_1", n["aide"], p + "TestAide"),
        *(obj(f"OBJ_EVENT_GFX_AQUA_MEMBER_{'MF'[i % 2]}", n[f"grunt{i + 1}"], p + f"Grunt{i + 1}",
              T.TRAINERS[f"grunt{i + 1}"][0], "FLAG_HIDE_COLD_STORAGE_GRUNTS", T.TRAINERS[f"grunt{i + 1}"][1],
              f"LOCALID_COLD_STORAGE_GRUNT_{i + 1}") for i in range(4)),
        obj("OBJ_EVENT_GFX_ARCHIE", n["leader"], p + "Leader", "DOWN", "FLAG_HIDE_COLD_STORAGE_VILLAINS",
            local_id="LOCALID_COLD_STORAGE_LEADER"),
        obj("OBJ_EVENT_GFX_AQUA_MEMBER_F", n["admin"], p + "Admin", "DOWN", "FLAG_HIDE_COLD_STORAGE_VILLAINS",
            local_id="LOCALID_COLD_STORAGE_ADMIN"),
        obj("OBJ_EVENT_GFX_WALLY", n["haru"], p + "Haru", "UP", "FLAG_HIDE_COLD_STORAGE_HARU",
            local_id="LOCALID_COLD_STORAGE_HARU"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", balls["key"], p + "ItemStorageKey", flag="FLAG_ITEM_COLD_STORAGE_STORAGE_KEY"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", balls["field1"], p + "ItemNeverMeltIce", flag="FLAG_ITEM_COLD_STORAGE_NEVER_MELT_ICE"),
        obj("OBJ_EVENT_GFX_ITEM_BALL", balls["maze"], p + "ItemSuperPotion", flag="FLAG_ITEM_COLD_STORAGE_SUPER_POTION"),
    ]
    exits = [(x, T.H - 1) for x in range(T.W) if T.GRID[T.H - 1][x] == "E"]
    # out to the Cold Storage door on Tosa Port (warp 4 there, at 27,9)
    m["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": "MAP_TOSA_PORT",
                         "dest_warp_id": TOSA_PORT_DOOR_WARP} for x, y in exits]
    m["coord_events"] = [{"type": "trigger", "x": T.TRIGGER[0], "y": T.TRIGGER[1], "elevation": 3,
                          "var": "VAR_COLD_STORAGE_STATE", "var_value": "0", "script": p + "BossTrigger"}]
    m["bg_events"] = [
        {"type": "sign", "x": T.GATE[0], "y": T.GATE[1], "elevation": 0,
         "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": p + "Gate"},
        {"type": "sign", "x": T.CONSOLE[0], "y": T.CONSOLE[1], "elevation": 0,
         "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": p + "Console"},
    ]
    return m


def outside():
    m = header("MAP_COLD_STORAGE_TEST_OUTSIDE", "ColdStorageTestOutside", "LAYOUT_COLD_STORAGE_TEST_OUTSIDE",
               "MUS_TOSA_PORT", "MAP_TYPE_TOWN", False)
    m["weather"] = "WEATHER_SUNNY"
    m["allow_cycling"] = True
    m["object_events"] = []
    exits = [x for x in range(T.W) if T.GRID[T.H - 1][x] == "E"]
    m["warp_events"] = [{"x": X.DOOR_AT[0], "y": X.DOOR_AT[1], "elevation": 0,
                         "dest_map": "MAP_COLD_STORAGE_TEST", "dest_warp_id": "0"}]
    m["coord_events"] = []
    m["bg_events"] = [{"type": "sign", "x": 12, "y": 6, "elevation": 0,
                       "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                       "script": "ColdStorageTestOutside_EventScript_Sign"}]
    return m


for name, data in (("ColdStorageTest", interior()), ("ColdStorageTestOutside", outside())):
    d = os.path.join(ROOT, "data", "maps", name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "map.json"), "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print("wrote", os.path.join("data", "maps", name, "map.json"))
