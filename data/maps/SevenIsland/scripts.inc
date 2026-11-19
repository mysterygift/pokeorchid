SevenIsland_MapScripts::
# 2 "data/maps/SevenIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SevenIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

SevenIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/SevenIsland/scripts.pory"
	setflag FLAG_VISITED_SEVEN_ISLAND
	return


SevenIsland_EventScript_SwordsDanceTutor::
# 8 "data/maps/SevenIsland/scripts.pory"
	msgbox SevenIsland_EventScript_SwordsDanceTutor_Text_0, MSGBOX_NPC
	return


SevenIsland_EventScript_OldWoman::
# 12 "data/maps/SevenIsland/scripts.pory"
	msgbox SevenIsland_EventScript_OldWoman_Text_0, MSGBOX_NPC
	return


SevenIsland_EventScript_Scientist::
# 16 "data/maps/SevenIsland/scripts.pory"
	msgbox SevenIsland_EventScript_Scientist_Text_0, MSGBOX_NPC
	return


SevenIsland_EventScript_IslandSign::
# 20 "data/maps/SevenIsland/scripts.pory"
	msgbox SevenIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


SevenIsland_EventScript_SwordsDanceTutor_Text_0:
# 8 "data/maps/SevenIsland/scripts.pory"
	.string "Seven Island is the last stop. Past the\n"
	.string "canyon, there are only the old ruins.$"

SevenIsland_EventScript_OldWoman_Text_0:
# 12 "data/maps/SevenIsland/scripts.pory"
	.string "Tanoby Ruins hold chambers older than\n"
	.string "anyone remembers. They're all sealed\l"
	.string "now.$"

SevenIsland_EventScript_Scientist_Text_0:
# 16 "data/maps/SevenIsland/scripts.pory"
	.string "I study the Unown that live in the\n"
	.string "ruins. They're shy around visitors.$"

SevenIsland_EventScript_IslandSign_Text_0:
# 20 "data/maps/SevenIsland/scripts.pory"
	.string "SEVEN ISLAND\n"
	.string "Quest Island. Sevault Canyon to the\l"
	.string "south.$"
