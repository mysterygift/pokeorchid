# 1 "data/maps/Route112_CableCarStation/scripts.pory"

# 2 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_MapScripts::
# 3 "data/maps/Route112_CableCarStation/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, Route112_CableCarStation_OnTransition
# 4 "data/maps/Route112_CableCarStation/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route112_CableCarStation_OnFrame
# 5 "data/maps/Route112_CableCarStation/scripts.pory"
	.byte 0
# 6 "data/maps/Route112_CableCarStation/scripts.pory"

# 7 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_OnTransition:
# 8 "data/maps/Route112_CableCarStation/scripts.pory"
	setescapewarp MAP_ROUTE112, 28, 28
# 9 "data/maps/Route112_CableCarStation/scripts.pory"
	call_if_eq VAR_CABLE_CAR_STATION_STATE, 2, Route112_CableCarStation_EventScript_MoveAttendantAside
# 10 "data/maps/Route112_CableCarStation/scripts.pory"
	end
# 11 "data/maps/Route112_CableCarStation/scripts.pory"

# 12 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_EventScript_MoveAttendantAside::
# 13 "data/maps/Route112_CableCarStation/scripts.pory"
	setobjectxyperm LOCALID_ROUTE112_CABLE_CAR_ATTENDANT, 7, 4
# 14 "data/maps/Route112_CableCarStation/scripts.pory"
	setobjectmovementtype LOCALID_ROUTE112_CABLE_CAR_ATTENDANT, MOVEMENT_TYPE_FACE_LEFT
# 15 "data/maps/Route112_CableCarStation/scripts.pory"
	return
# 16 "data/maps/Route112_CableCarStation/scripts.pory"

# 17 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_OnFrame:
# 18 "data/maps/Route112_CableCarStation/scripts.pory"
	map_script_2 VAR_CABLE_CAR_STATION_STATE, 2, Route112_CableCarStation_EventScript_ExitCableCar
# 19 "data/maps/Route112_CableCarStation/scripts.pory"
	.2byte 0
# 20 "data/maps/Route112_CableCarStation/scripts.pory"

# 21 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_EventScript_ExitCableCar::
# 22 "data/maps/Route112_CableCarStation/scripts.pory"
	lockall
# 23 "data/maps/Route112_CableCarStation/scripts.pory"
	applymovement LOCALID_PLAYER, Route112_CableCarStation_Movement_ExitCableCar
# 24 "data/maps/Route112_CableCarStation/scripts.pory"
	applymovement LOCALID_ROUTE112_CABLE_CAR_ATTENDANT, Route112_CableCarStation_Movement_FollowPlayerOutFromCableCar
# 25 "data/maps/Route112_CableCarStation/scripts.pory"
	waitmovement 0
# 26 "data/maps/Route112_CableCarStation/scripts.pory"
	setvar VAR_CABLE_CAR_STATION_STATE, 0
# 27 "data/maps/Route112_CableCarStation/scripts.pory"
	setobjectxyperm LOCALID_ROUTE112_CABLE_CAR_ATTENDANT, 6, 7
# 28 "data/maps/Route112_CableCarStation/scripts.pory"
	setobjectmovementtype LOCALID_ROUTE112_CABLE_CAR_ATTENDANT, MOVEMENT_TYPE_FACE_DOWN
# 29 "data/maps/Route112_CableCarStation/scripts.pory"
	releaseall
# 30 "data/maps/Route112_CableCarStation/scripts.pory"
	end
# 31 "data/maps/Route112_CableCarStation/scripts.pory"

# 32 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_EventScript_Attendant::
# 33 "data/maps/Route112_CableCarStation/scripts.pory"
	lock
# 34 "data/maps/Route112_CableCarStation/scripts.pory"
	faceplayer
# 35 "data/maps/Route112_CableCarStation/scripts.pory"
	msgbox Route112_CableCarStation_Text_CableCarReadyGetOn, MSGBOX_YESNO
# 36 "data/maps/Route112_CableCarStation/scripts.pory"
	goto_if_eq VAR_RESULT, YES, Route112_CableCarStation_EventScript_RideCableCar
# 37 "data/maps/Route112_CableCarStation/scripts.pory"
	goto_if_eq VAR_RESULT, NO, Route112_CableCarStation_EventScript_DeclineRide
# 38 "data/maps/Route112_CableCarStation/scripts.pory"
	end
# 39 "data/maps/Route112_CableCarStation/scripts.pory"

# 40 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_EventScript_RideCableCar::
# 41 "data/maps/Route112_CableCarStation/scripts.pory"
	msgbox Route112_CableCarStation_Text_StepThisWay, MSGBOX_DEFAULT
# 42 "data/maps/Route112_CableCarStation/scripts.pory"
	closemessage
# 43 "data/maps/Route112_CableCarStation/scripts.pory"
	applymovement LOCALID_ROUTE112_CABLE_CAR_ATTENDANT, Route112_CableCarStation_Movement_LeadPlayerToCableCar
# 44 "data/maps/Route112_CableCarStation/scripts.pory"
	applymovement LOCALID_PLAYER, Route112_CableCarStation_Movement_BoardCableCar
# 45 "data/maps/Route112_CableCarStation/scripts.pory"
	waitmovement 0
# 46 "data/maps/Route112_CableCarStation/scripts.pory"
	setvar VAR_0x8004, FALSE  @ Going up
# 47 "data/maps/Route112_CableCarStation/scripts.pory"
	setvar VAR_CABLE_CAR_STATION_STATE, 1
# 48 "data/maps/Route112_CableCarStation/scripts.pory"
	incrementgamestat GAME_STAT_RODE_CABLE_CAR
# 49 "data/maps/Route112_CableCarStation/scripts.pory"
	special CableCarWarp
# 50 "data/maps/Route112_CableCarStation/scripts.pory"
	special CableCar
# 51 "data/maps/Route112_CableCarStation/scripts.pory"
	release
# 52 "data/maps/Route112_CableCarStation/scripts.pory"
	end
# 53 "data/maps/Route112_CableCarStation/scripts.pory"

# 54 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_EventScript_DeclineRide::
# 55 "data/maps/Route112_CableCarStation/scripts.pory"
	msgbox Route112_CableCarStation_Text_RideAnotherTime, MSGBOX_DEFAULT
# 56 "data/maps/Route112_CableCarStation/scripts.pory"
	release
# 57 "data/maps/Route112_CableCarStation/scripts.pory"
	end
# 58 "data/maps/Route112_CableCarStation/scripts.pory"

# 59 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Movement_LeadPlayerToCableCar:
# 60 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_up
# 61 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_up
# 62 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_right
# 63 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_in_place_faster_left
# 64 "data/maps/Route112_CableCarStation/scripts.pory"
	step_end
# 65 "data/maps/Route112_CableCarStation/scripts.pory"

# 66 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Movement_FollowPlayerOutFromCableCar:
# 67 "data/maps/Route112_CableCarStation/scripts.pory"
	delay_16
# 68 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_left
# 69 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_down
# 70 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_down
# 71 "data/maps/Route112_CableCarStation/scripts.pory"
	step_end
# 72 "data/maps/Route112_CableCarStation/scripts.pory"

# 73 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Movement_BoardCableCar:
# 74 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_up
# 75 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_up
# 76 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_up
# 77 "data/maps/Route112_CableCarStation/scripts.pory"
	delay_16
# 78 "data/maps/Route112_CableCarStation/scripts.pory"
	step_end
# 79 "data/maps/Route112_CableCarStation/scripts.pory"

# 80 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Movement_ExitCableCar:
# 81 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_down
# 82 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_down
# 83 "data/maps/Route112_CableCarStation/scripts.pory"
	walk_down
# 84 "data/maps/Route112_CableCarStation/scripts.pory"
	delay_16
# 85 "data/maps/Route112_CableCarStation/scripts.pory"
	step_end
# 86 "data/maps/Route112_CableCarStation/scripts.pory"

# 87 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Text_CableCarReadyGetOn:
# 88 "data/maps/Route112_CableCarStation/scripts.pory"
	.string "The CABLE CAR is ready to go up.\n"
# 89 "data/maps/Route112_CableCarStation/scripts.pory"
	.string "Would you like to be on it?$"
# 90 "data/maps/Route112_CableCarStation/scripts.pory"

# 91 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Text_StepThisWay:
# 92 "data/maps/Route112_CableCarStation/scripts.pory"
	.string "Please step this way.$"
# 93 "data/maps/Route112_CableCarStation/scripts.pory"

# 94 "data/maps/Route112_CableCarStation/scripts.pory"
Route112_CableCarStation_Text_RideAnotherTime:
# 95 "data/maps/Route112_CableCarStation/scripts.pory"
	.string "Please ride with us another time.$"
