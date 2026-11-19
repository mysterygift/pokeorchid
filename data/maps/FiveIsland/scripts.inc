FiveIsland_MapScripts::
# 2 "data/maps/FiveIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FiveIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

FiveIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/FiveIsland/scripts.pory"
	setflag FLAG_VISITED_FIVE_ISLAND
	return


FiveIsland_EventScript_Fisher::
# 8 "data/maps/FiveIsland/scripts.pory"
	msgbox FiveIsland_EventScript_Fisher_Text_0, MSGBOX_NPC
	return


FiveIsland_EventScript_BugCatcher::
# 12 "data/maps/FiveIsland/scripts.pory"
	msgbox FiveIsland_EventScript_BugCatcher_Text_0, MSGBOX_NPC
	return


FiveIsland_EventScript_IslandSign::
# 16 "data/maps/FiveIsland/scripts.pory"
	msgbox FiveIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


FiveIsland_EventScript_Fisher_Text_0:
# 8 "data/maps/FiveIsland/scripts.pory"
	.string "The fishing off Five Island is the best\n"
	.string "in the Sevii Islands.$"

FiveIsland_EventScript_BugCatcher_Text_0:
# 12 "data/maps/FiveIsland/scripts.pory"
	.string "The meadow east of here is full of bug\n"
	.string "POKéMON. There's a creepy warehouse\l"
	.string "there too.$"

FiveIsland_EventScript_IslandSign_Text_0:
# 16 "data/maps/FiveIsland/scripts.pory"
	.string "FIVE ISLAND\n"
	.string "Chrono Island. The meadow is to the\l"
	.string "east.$"
