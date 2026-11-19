SixIsland_MapScripts::
# 2 "data/maps/SixIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

SixIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/SixIsland/scripts.pory"
	setflag FLAG_VISITED_SIX_ISLAND
	return


SixIsland_EventScript_Boy::
# 8 "data/maps/SixIsland/scripts.pory"
	msgbox SixIsland_EventScript_Boy_Text_0, MSGBOX_NPC
	return


SixIsland_EventScript_Hiker::
# 12 "data/maps/SixIsland/scripts.pory"
	msgbox SixIsland_EventScript_Hiker_Text_0, MSGBOX_NPC
	return


SixIsland_EventScript_IslandSign::
# 16 "data/maps/SixIsland/scripts.pory"
	msgbox SixIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


SixIsland_EventScript_Boy_Text_0:
# 8 "data/maps/SixIsland/scripts.pory"
	.string "Water Path runs from here all the way to\n"
	.string "Ruin Valley.$"

SixIsland_EventScript_Hiker_Text_0:
# 12 "data/maps/SixIsland/scripts.pory"
	.string "Ruin Valley has a strange sealed door.\n"
	.string "Nobody has ever opened it.$"

SixIsland_EventScript_IslandSign_Text_0:
# 16 "data/maps/SixIsland/scripts.pory"
	.string "SIX ISLAND\n"
	.string "Fortune Island. Water Path to the east.$"
