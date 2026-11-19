MoongroveCity_MapScripts::
# 2 "data/maps/MoongroveCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, MoongroveCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

MoongroveCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/MoongroveCity/scripts.pory"
	setflag FLAG_VISITED_MOSSDEEP_CITY
	return


MoongroveCity_EventScript_TownSign::
# 8 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


MoongroveCity_EventScript_GymSign::
# 12 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


MoongroveCity_EventScript_Npc1::
# 16 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


MoongroveCity_EventScript_Npc2::
# 20 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


MoongroveCity_EventScript_Npc3::
# 24 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


MoongroveCity_EventScript_Npc4::
# 28 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


MoongroveCity_EventScript_Npc5::
# 32 "data/maps/MoongroveCity/scripts.pory"
	msgbox MoongroveCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


MoongroveCity_EventScript_TownSign_Text_0:
# 8 "data/maps/MoongroveCity/scripts.pory"
	.string "Moongrove City\n"
	.string "“Roots in the mud, eyes on the tide.”$"

MoongroveCity_EventScript_GymSign_Text_0:
# 12 "data/maps/MoongroveCity/scripts.pory"
	.string "Moongrove City Pokémon Gym\n"
	.string "Leader: Tork. Ground-type Pokémon.$"

MoongroveCity_EventScript_Npc1_Text_0:
# 16 "data/maps/MoongroveCity/scripts.pory"
	.string "Tork, our Gym Leader, was out on the\n"
	.string "mudflats before dawn again.\p"
	.string "He swears the big catfish only bite\n"
	.string "when the tide turns.$"

MoongroveCity_EventScript_Npc2_Text_0:
# 20 "data/maps/MoongroveCity/scripts.pory"
	.string "The mangroves keep the sea from\n"
	.string "swallowing the town. Their roots hold\l"
	.string "this whole place together.$"

MoongroveCity_EventScript_Npc3_Text_0:
# 24 "data/maps/MoongroveCity/scripts.pory"
	.string "Have you seen the lights at the\n"
	.string "Abandoned House? My brother says it's\l"
	.string "a ghost.\p"
	.string "I say it's Mum looking for her keys.$"

MoongroveCity_EventScript_Npc4_Text_0:
# 28 "data/maps/MoongroveCity/scripts.pory"
	.string "Moongrove Marsh is a fisher's dream.\n"
	.string "Bring a rod, some patience… and bug\l"
	.string "spray.$"

MoongroveCity_EventScript_Npc5_Text_0:
# 32 "data/maps/MoongroveCity/scripts.pory"
	.string "The train's made Moongrove easy to\n"
	.string "reach. Shame half the visitors only\l"
	.string "come to gawk at the haunted house.$"
