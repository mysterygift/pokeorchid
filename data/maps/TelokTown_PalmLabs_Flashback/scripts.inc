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
# 23 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	lockall
# 24 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special UnfreezeObjectsKeepLock
# 25 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 60
# 26 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special TextAutoScrollOn
# 27 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_0
# 28 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 29 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 30 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_1
# 31 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 32 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 33 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_2
# 34 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 35 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	message TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_3
# 37 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	waitmessage
# 38 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 150
# 39 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	closemessage
# 40 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	special TextAutoScrollOff
# 41 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	delay 30
# 42 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	setvar VAR_TELOK_TOWN_STATE, 3
# 43 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	warp MAP_TELOK_TOWN_PALM_LABS, 9, 8
	return


TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_0:
# 27 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "It's dire times in the Tosa region. We've\n"
	.string "seen unprecedented changes in Pokémon\l"
	.string "populations across the region.$"

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_1:
# 30 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "In all my 20 years living in Tosa I've\n"
	.string "never seen such dramatic changes in\l"
	.string "species, and it's no coincidence that as\l"
	.string "the region has developed, Pokémon\l"
	.string "numbers have dwindled.$"

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_2:
# 33 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "The League have had to crack down on\n"
	.string "Trainer licensing and imports. The\l"
	.string "entire ecosystem is on the cusp of\l"
	.string "collapse.$"

TelokTown_PalmLabs_Flashback_EventScript_Narration_Text_3:
# 36 "data/maps/TelokTown_PalmLabs_Flashback/scripts.pory"
	.string "That's why I'm so glad you're here. There\n"
	.string "is simply too much data to collect and\l"
	.string "analyse...$"
