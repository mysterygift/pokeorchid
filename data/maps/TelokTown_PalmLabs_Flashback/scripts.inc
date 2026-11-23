TelokTown_PalmLabs_Flashback_MapScripts::
# 5 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_TRANSITION
# 8 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE
# 15 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_FRAME_TABLE
	.byte 0

TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 6 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special FieldGrayscaleOn
	return

TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE:
# 9 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE_0
	.2byte 0

TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE_0:
# 10 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	hideobjectat LOCALID_PLAYER, MAP_TELOK_TOWN_PALM_LABS_FLASHBACK
# 11 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	hideobjectat OBJ_EVENT_ID_FOLLOWER, MAP_TELOK_TOWN_PALM_LABS_FLASHBACK
# 12 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	setvar VAR_TEMP_1, 1
	return

TelokTown_PalmLabs_Flashback_MapScripts_MAP_SCRIPT_ON_FRAME_TABLE:
# 16 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	map_script_2 VAR_TELOK_TOWN_STATE, 2, TelokTown_PalmLabs_Flashback_EventScript_Narration
	.2byte 0


TelokTown_PalmLabs_Flashback_EventScript_Narration::
# 30 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	lockall
# 31 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special UnfreezeObjectsKeepLock
# 32 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special SpawnCameraObject
# 33 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 60
# 34 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special TextAutoScrollOn
# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	applymovement LOCALID_CAMERA, TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_0
# 37 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_0
# 38 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 39 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 40 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmovement LOCALID_CAMERA
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	applymovement LOCALID_CAMERA, TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_1
# 43 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_1
# 44 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 45 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 46 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmovement LOCALID_CAMERA
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	applymovement LOCALID_CAMERA, TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_2
# 49 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_2
# 50 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 51 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 52 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmovement LOCALID_CAMERA
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	applymovement LOCALID_CAMERA, TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_3
# 55 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_3
# 56 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 57 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 58 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmovement LOCALID_CAMERA
# 60 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	closemessage
# 61 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special TextAutoScrollOff
# 62 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 30
# 63 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	fadescreen FADE_TO_BLACK
# 64 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special RemoveCameraObject
# 65 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	setvar VAR_TELOK_TOWN_STATE, 3
# 66 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	warp MAP_TELOK_TOWN_PALM_LABS, 9, 8
	return


# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_0:
# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
	step_end

# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_1:
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_northwest
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_northwest
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_northwest
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_northwest
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_northwest
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_northwest
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_left
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_right
	step_end

# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_2:
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southeast
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_right
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_right
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_right
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_right
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_right
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_right
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
# 48 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
	step_end

# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
TelokTown_PalmLabs_Flashback_EventScript_Narration_Movement_3:
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_diag_southwest
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_fast_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
# 54 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	walk_slow_down
	step_end

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_0:
# 37 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "It's dire times in the Tosa region. We've\n"
	.string "seen unprecedented changes in Pokémon\l"
	.string "populations across the region.$"

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_1:
# 43 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "In all my 20 years living in Tosa I've\n"
	.string "never seen such dramatic changes in\l"
	.string "species, and it's no coincidence that as\l"
	.string "the region has developed, Pokémon\l"
	.string "numbers have dwindled.$"

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_2:
# 49 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "The League have had to crack down on\n"
	.string "Trainer licensing and imports. The\l"
	.string "entire ecosystem is on the cusp of\l"
	.string "collapse.$"

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_3:
# 55 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "That's why I'm so glad you're here. There\n"
	.string "is simply too much data to collect and\l"
	.string "analyse...$"
