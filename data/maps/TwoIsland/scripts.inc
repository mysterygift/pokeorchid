TwoIsland_MapScripts::
# 2 "data/maps/TwoIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TwoIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

TwoIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/TwoIsland/scripts.pory"
	setflag FLAG_VISITED_TWO_ISLAND
	return


TwoIsland_EventScript_Woman::
# 8 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_Woman_Text_0, MSGBOX_NPC
	return


TwoIsland_EventScript_Beauty::
# 12 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_Beauty_Text_0, MSGBOX_NPC
	return


TwoIsland_EventScript_Sailor::
# 16 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_Sailor_Text_0, MSGBOX_NPC
	return


TwoIsland_EventScript_SuperNerd::
# 20 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_SuperNerd_Text_0, MSGBOX_NPC
	return


TwoIsland_EventScript_LittleBoy::
# 24 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_LittleBoy_Text_0, MSGBOX_NPC
	return


TwoIsland_EventScript_Boy::
# 28 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_Boy_Text_0, MSGBOX_NPC
	return


TwoIsland_EventScript_IslandSign::
# 32 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


TwoIsland_EventScript_JoyfulGameCornerSign::
# 37 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_JoyfulGameCornerSign_Text_0, MSGBOX_SIGN
	return


TwoIsland_EventScript_FastCurrentSign::
# 42 "data/maps/TwoIsland/scripts.pory"
	msgbox TwoIsland_EventScript_FastCurrentSign_Text_0, MSGBOX_SIGN
	return


TwoIsland_EventScript_Woman_Text_0:
# 8 "data/maps/TwoIsland/scripts.pory"
	.string "The stall sells goods you can't find\n"
	.string "anywhere else. The prices, though...\l"
	.string "ouch.$"

TwoIsland_EventScript_Beauty_Text_0:
# 12 "data/maps/TwoIsland/scripts.pory"
	.string "The Game Corner here is run by a sweet\n"
	.string "old man. Everyone on the island plays\l"
	.string "there.$"

TwoIsland_EventScript_Sailor_Text_0:
# 16 "data/maps/TwoIsland/scripts.pory"
	.string "Cape Brink is north of here. They say a\n"
	.string "great teacher of moves lives at the\l"
	.string "very tip.$"

TwoIsland_EventScript_SuperNerd_Text_0:
# 20 "data/maps/TwoIsland/scripts.pory"
	.string "I came all the way from Tosa for the\n"
	.string "market. Worth every coin!$"

TwoIsland_EventScript_LittleBoy_Text_0:
# 24 "data/maps/TwoIsland/scripts.pory"
	.string "My big brother lets me ride on his\n"
	.string "Lapras sometimes!$"

TwoIsland_EventScript_Boy_Text_0:
# 28 "data/maps/TwoIsland/scripts.pory"
	.string "I found a pretty shell on the beach\n"
	.string "today!$"

TwoIsland_EventScript_IslandSign_Text_0:
# 32 "data/maps/TwoIsland/scripts.pory"
	.string "TWO ISLAND\n"
	.string "Boon Island for the market-minded.$"

TwoIsland_EventScript_JoyfulGameCornerSign_Text_0:
# 37 "data/maps/TwoIsland/scripts.pory"
	.string "JOYFUL GAME CORNER\n"
	.string "Play games, win prizes, make friends!$"

TwoIsland_EventScript_FastCurrentSign_Text_0:
# 42 "data/maps/TwoIsland/scripts.pory"
	.string "The currents around here used to be\n"
	.string "fierce.\n"
	.string "These days the sea is calm enough to\l"
	.string "Surf.$"
