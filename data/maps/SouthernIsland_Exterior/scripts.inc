# 1 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 2 "data/maps/SouthernIsland_Exterior/scripts.pory"
@ Orchid: Eon Island (vanilla Southern Island). The voyage Sailor and his boat wait at the old ferry dock.
# 3 "data/maps/SouthernIsland_Exterior/scripts.pory"
SouthernIsland_Exterior_MapScripts::
# 4 "data/maps/SouthernIsland_Exterior/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SouthernIsland_Exterior_OnTransition
# 5 "data/maps/SouthernIsland_Exterior/scripts.pory"
	.byte 0
# 6 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 7 "data/maps/SouthernIsland_Exterior/scripts.pory"
SouthernIsland_Exterior_OnTransition:
# 8 "data/maps/SouthernIsland_Exterior/scripts.pory"
	setflag FLAG_LANDMARK_SOUTHERN_ISLAND
# 9 "data/maps/SouthernIsland_Exterior/scripts.pory"
	end
# 10 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 11 "data/maps/SouthernIsland_Exterior/scripts.pory"
@ Used by Common_EventScript_FerryDepartIsland (data/event_scripts.s).
# 12 "data/maps/SouthernIsland_Exterior/scripts.pory"
Ferry_EventScript_DepartIslandSouth::
# 13 "data/maps/SouthernIsland_Exterior/scripts.pory"
	applymovement LOCALID_PLAYER, Ferry_Movement_DepartIslandBoardSouth
# 14 "data/maps/SouthernIsland_Exterior/scripts.pory"
	waitmovement 0
# 15 "data/maps/SouthernIsland_Exterior/scripts.pory"
	return
# 16 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 17 "data/maps/SouthernIsland_Exterior/scripts.pory"
Ferry_EventScript_DepartIslandWest::
# 18 "data/maps/SouthernIsland_Exterior/scripts.pory"
	applymovement LOCALID_PLAYER, Ferry_Movement_DepartIslandBoardWest
# 19 "data/maps/SouthernIsland_Exterior/scripts.pory"
	waitmovement 0
# 20 "data/maps/SouthernIsland_Exterior/scripts.pory"
	return
# 21 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 22 "data/maps/SouthernIsland_Exterior/scripts.pory"
Ferry_Movement_DepartIslandBoardSouth:
# 23 "data/maps/SouthernIsland_Exterior/scripts.pory"
	walk_down
# 24 "data/maps/SouthernIsland_Exterior/scripts.pory"
	step_end
# 25 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 26 "data/maps/SouthernIsland_Exterior/scripts.pory"
Ferry_Movement_DepartIslandBoardWest:
# 27 "data/maps/SouthernIsland_Exterior/scripts.pory"
	walk_left
# 28 "data/maps/SouthernIsland_Exterior/scripts.pory"
	walk_in_place_faster_down
# 29 "data/maps/SouthernIsland_Exterior/scripts.pory"
	step_end
# 30 "data/maps/SouthernIsland_Exterior/scripts.pory"

# 31 "data/maps/SouthernIsland_Exterior/scripts.pory"
SouthernIsland_Exterior_EventScript_Sign::
# 32 "data/maps/SouthernIsland_Exterior/scripts.pory"
	msgbox SouthernIsland_Exterior_Text_Sign, MSGBOX_SIGN
# 33 "data/maps/SouthernIsland_Exterior/scripts.pory"
	end
