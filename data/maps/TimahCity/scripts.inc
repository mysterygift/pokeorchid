TimahCity_MapScripts::
# 2 "data/maps/TimahCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TimahCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

TimahCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/TimahCity/scripts.pory"
	setflag FLAG_VISITED_PETALBURG_CITY
	return


TimahCity_EventScript_TownSign::
# 8 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


TimahCity_EventScript_GymSign::
# 12 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


TimahCity_EventScript_Npc1::
# 16 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc2::
# 20 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc3::
# 24 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc4::
# 28 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc5::
# 32 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_TownSign_Text_0:
# 8 "data/maps/TimahCity/scripts.pory"
	.string "Timah City\n"
	.string "“The green heart of the Tosa Reserve.”$"

TimahCity_EventScript_GymSign_Text_0:
# 12 "data/maps/TimahCity/scripts.pory"
	.string "Timah City Pokémon Gym\n"
	.string "Leader: Hana. Grass-type Pokémon.$"

TimahCity_EventScript_Npc1_Text_0:
# 16 "data/maps/TimahCity/scripts.pory"
	.string "Hana grows orchids in her garden that\n"
	.string "bloom nowhere else in the world. She\l"
	.string "guards them better than her Gym Badge!$"

TimahCity_EventScript_Npc2_Text_0:
# 20 "data/maps/TimahCity/scripts.pory"
	.string "Timah sits right in the middle of the\n"
	.string "Tosa Reserve. Stick to the paths. The\l"
	.string "Rangers are watching for poachers.$"

TimahCity_EventScript_Npc3_Text_0:
# 24 "data/maps/TimahCity/scripts.pory"
	.string "It rains here every afternoon, like\n"
	.string "clockwork. Bring an umbrella. Or a Lotad.$"

TimahCity_EventScript_Npc4_Text_0:
# 28 "data/maps/TimahCity/scripts.pory"
	.string "This city grew up around the old rubber\n"
	.string "trees on the hill. Now look at it: trains,\l"
	.string "Pokémon Centres…$"

TimahCity_EventScript_Npc5_Text_0:
# 32 "data/maps/TimahCity/scripts.pory"
	.string "There are Pokémon up in the canopy\n"
	.string "that never come down to the ground.\l"
	.string "I've been waiting all week!$"
