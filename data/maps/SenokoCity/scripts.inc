SenokoCity_MapScripts::
# 2 "data/maps/SenokoCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SenokoCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

SenokoCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/SenokoCity/scripts.pory"
	setflag FLAG_VISITED_MAUVILLE_CITY
	return


SenokoCity_EventScript_TownSign::
# 8 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


SenokoCity_EventScript_GymSign::
# 12 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


SenokoCity_EventScript_Sign3::
# 16 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_Sign3_Text_0, MSGBOX_SIGN
	return


SenokoCity_EventScript_Npc1::
# 20 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


SenokoCity_EventScript_Npc2::
# 24 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


SenokoCity_EventScript_Npc3::
# 28 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


SenokoCity_EventScript_Npc4::
# 32 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


SenokoCity_EventScript_Npc5::
# 36 "data/maps/SenokoCity/scripts.pory"
	msgbox SenokoCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


SenokoCity_EventScript_TownSign_Text_0:
# 8 "data/maps/SenokoCity/scripts.pory"
	.string "Senoko City\n"
	.string "“Powering Tosa, one turbine at a time.”$"

SenokoCity_EventScript_GymSign_Text_0:
# 12 "data/maps/SenokoCity/scripts.pory"
	.string "Senoko City Pokémon Gym\n"
	.string "Leader: Mo. Electric-type Pokémon.$"

SenokoCity_EventScript_Sign3_Text_0:
# 16 "data/maps/SenokoCity/scripts.pory"
	.string "TOSA NATIONAL GRID\n"
	.string "Senoko control office.$"

SenokoCity_EventScript_Npc1_Text_0:
# 20 "data/maps/SenokoCity/scripts.pory"
	.string "Mo runs the national power grid from\n"
	.string "Senoko. If the lights go out anywhere\l"
	.string "in Tosa, he's the one who gets the call.$"

SenokoCity_EventScript_Npc2_Text_0:
# 24 "data/maps/SenokoCity/scripts.pory"
	.string "The wind farms around town spin day and\n"
	.string "night. Electric Pokémon love napping by\l"
	.string "the turbines.$"

SenokoCity_EventScript_Npc3_Text_0:
# 28 "data/maps/SenokoCity/scripts.pory"
	.string "When the wind drops, Mo sends his\n"
	.string "Electric Pokémon to the Power Plant to\l"
	.string "help out. True story!$"

SenokoCity_EventScript_Npc4_Text_0:
# 32 "data/maps/SenokoCity/scripts.pory"
	.string "I counted forty turbines on the hill!\n"
	.string "Then I lost count.$"

SenokoCity_EventScript_Npc5_Text_0:
# 36 "data/maps/SenokoCity/scripts.pory"
	.string "Senoko was a sleepy place before the\n"
	.string "turbines. Now it powers the whole\l"
	.string "region.$"
