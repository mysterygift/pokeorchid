CorralCity_MapScripts::
# 2 "data/maps/CorralCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, CorralCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

CorralCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/CorralCity/scripts.pory"
	setflag FLAG_VISITED_SOOTOPOLIS_CITY
	return


CorralCity_EventScript_TownSign::
# 8 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


CorralCity_EventScript_GymSign::
# 12 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


CorralCity_EventScript_Npc1::
# 16 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


CorralCity_EventScript_Npc2::
# 20 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


CorralCity_EventScript_Npc3::
# 24 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


CorralCity_EventScript_Npc4::
# 28 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


CorralCity_EventScript_Npc5::
# 32 "data/maps/CorralCity/scripts.pory"
	msgbox CorralCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


CorralCity_EventScript_TownSign_Text_0:
# 8 "data/maps/CorralCity/scripts.pory"
	.string "Corral City\n"
	.string "“Sun, sea and Pokétopia.”$"

CorralCity_EventScript_GymSign_Text_0:
# 12 "data/maps/CorralCity/scripts.pory"
	.string "Corral City Pokémon Gym\n"
	.string "Leader: Marina. Water-type Pokémon.$"

CorralCity_EventScript_Npc1_Text_0:
# 16 "data/maps/CorralCity/scripts.pory"
	.string "Marina's Gym is right by the water. They\n"
	.string "say she's mastered the seas\l"
	.string "themselves.$"

CorralCity_EventScript_Npc2_Text_0:
# 20 "data/maps/CorralCity/scripts.pory"
	.string "I'm going to swim to the little islands!\n"
	.string "Mum says I need a boat first. And to\l"
	.string "learn to swim.$"

CorralCity_EventScript_Npc3_Text_0:
# 24 "data/maps/CorralCity/scripts.pory"
	.string "Boats leave the marina for the small\n"
	.string "islands around Pokétopia. Once they're\l"
	.string "running again, anyway.$"

CorralCity_EventScript_Npc4_Text_0:
# 28 "data/maps/CorralCity/scripts.pory"
	.string "The night safari opens after dark. You\n"
	.string "can see nocturnal Pokémon up close!$"

CorralCity_EventScript_Npc5_Text_0:
# 32 "data/maps/CorralCity/scripts.pory"
	.string "I came to Pokétopia for a quiet holiday.\n"
	.string "Then I found the ice cream stall.$"
