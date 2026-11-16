# 1 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 2 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_MapScripts::
# 3 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattleTowerElevator_OnFrame
# 4 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, BattleFrontier_BattleTowerElevator_OnWarp
# 5 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	.byte 0
# 6 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 7 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_OnFrame:
# 8 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	map_script_2 VAR_TEMP_0, 0, BattleFrontier_BattleTowerElevator_EventScript_EnterElevator
# 9 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	.2byte 0
# 10 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 11 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_EnterElevator::
# 12 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	setvar VAR_TEMP_0, 1
# 13 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	applymovement LOCALID_TOWER_ELEVATOR_ATTENDANT, BattleFrontier_BattleTowerElevator_Movement_AttendantEnter
# 14 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleTowerElevator_Movement_PlayerEnter
# 15 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitmovement 0
# 16 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	special BufferBattleTowerElevatorFloors
# 17 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitse
# 18 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	special MoveElevator
# 19 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	delay 48
# 20 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	applymovement LOCALID_TOWER_ELEVATOR_ATTENDANT, BattleFrontier_BattleTowerElevator_Movement_AttendantExit
# 21 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleTowerElevator_Movement_PlayerExit
# 22 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitmovement 0
# 23 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	call BattleFrontier_BattleTowerElevator_EventScript_WarpToNextRoom
# 24 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	end
# 25 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 26 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_WarpToNextRoom::
# 27 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerElevator_EventScript_WarpToCorridor
# 28 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerElevator_EventScript_WarpToCorridor
# 29 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS, BattleFrontier_BattleTowerElevator_EventScript_WarpToNextRoomMulti
# 30 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS, BattleFrontier_BattleTowerElevator_EventScript_WarpToCorridorMulti
# 31 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	return
# 32 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 33 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_WarpToCorridor::
# 34 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_TOWER_CORRIDOR, 8, 1
# 35 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitstate
# 36 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	return
# 37 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 38 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_WarpToNextRoomMulti::
# 39 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	goto_if_unset FLAG_CHOSEN_MULTI_BATTLE_NPC_PARTNER, BattleFrontier_BattleTowerElevator_EventScript_WarpToPartnerRoom
# 40 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_TOWER_MULTI_CORRIDOR, 7, 2
# 41 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitstate
# 42 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	return
# 43 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 44 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_WarpToCorridorMulti::
# 45 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_TOWER_MULTI_CORRIDOR, 7, 2
# 46 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitstate
# 47 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	return
# 48 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 49 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_WarpToPartnerRoom::
# 50 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_TOWER_MULTI_PARTNER_ROOM, 10, 1
# 51 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	waitstate
# 52 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	return
# 53 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 54 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_Movement_AttendantEnter:
# 55 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_up
# 56 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_right
# 57 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	face_down
# 58 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	step_end
# 59 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 60 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_Movement_PlayerEnter:
# 61 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_up
# 62 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_up
# 63 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	face_down
# 64 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	step_end
# 65 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 66 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_Movement_AttendantExit:
# 67 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_down
# 68 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_down
# 69 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	set_invisible
# 70 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	step_end
# 71 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 72 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_Movement_PlayerExit:
# 73 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_right
# 74 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_down
# 75 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	walk_down
# 76 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	step_end
# 77 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 78 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_OnWarp:
# 79 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, BattleFrontier_BattleTowerElevator_EventScript_TurnPlayerNorth
# 80 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	.2byte 0
# 81 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"

# 82 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
BattleFrontier_BattleTowerElevator_EventScript_TurnPlayerNorth::
# 83 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	setvar VAR_TEMP_1, 1
# 84 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 85 "data/maps/BattleFrontier_BattleTowerElevator/scripts.pory"
	end
