ChanguCity_Cafe_MapScripts::
# 5 "data/maps/ChanguCity_Cafe/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 6 "data/maps/ChanguCity_Cafe/scripts.pory"
	goto_if_set FLAG_CYNTHIA_BEATEN_AT_LAKE, ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
# 9 "data/maps/ChanguCity_Cafe/scripts.pory"
	setflag FLAG_HIDE_CHANGU_CAFE_CYNTHIA
	return

ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 7 "data/maps/ChanguCity_Cafe/scripts.pory"
	clearflag FLAG_HIDE_CHANGU_CAFE_CYNTHIA
	return


ChanguCity_Cafe_EventScript_Barista::
# 15 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Barista_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Businessman::
# 19 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Businessman_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Businesswoman::
# 23 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Businesswoman_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Tourist::
# 27 "data/maps/ChanguCity_Cafe/scripts.pory"
	goto_if_set FLAG_CYNTHIA_BEATEN_AT_LAKE, ChanguCity_Cafe_EventScript_Tourist_1
# 30 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Tourist_Text_1, MSGBOX_NPC
	return

ChanguCity_Cafe_EventScript_Tourist_1:
# 28 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Tourist_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Barista_Text_0:
# 15 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Welcome to the Battle Café!$"

ChanguCity_Cafe_EventScript_Businessman_Text_0:
# 19 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "We flew in from Lumiose this morning. If\n"
	.string "this deal doesn't close by tonight, I'm\l"
	.string "on the red-eye home.$"

ChanguCity_Cafe_EventScript_Businesswoman_Text_0:
# 23 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Synergise, innovate, leverage… I just\n"
	.string "wanted a kaya toast in peace.$"

ChanguCity_Cafe_EventScript_Tourist_Text_0:
# 28 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "That blonde lady in the corner has been\n"
	.string "here every day since she came back from\l"
	.string "Holon Lake. Is she someone famous?$"

ChanguCity_Cafe_EventScript_Tourist_Text_1:
# 30 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "They call this place the Battle Café.\n"
	.string "Trainers come here between flights,\l"
	.string "hoping a strong opponent walks in.$"
