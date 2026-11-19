JuranCity_MapScripts::
# 2 "data/maps/JuranCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, JuranCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

JuranCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/JuranCity/scripts.pory"
	setflag FLAG_VISITED_LILYCOVE_CITY
	return


JuranCity_EventScript_TownSign::
# 8 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


JuranCity_EventScript_Sign2::
# 12 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_Sign2_Text_0, MSGBOX_SIGN
	return


JuranCity_EventScript_Npc1::
# 16 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


JuranCity_EventScript_Npc2::
# 20 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


JuranCity_EventScript_Npc3::
# 24 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


JuranCity_EventScript_Npc4::
# 28 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


JuranCity_EventScript_Npc5::
# 32 "data/maps/JuranCity/scripts.pory"
	msgbox JuranCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


JuranCity_EventScript_TownSign_Text_0:
# 8 "data/maps/JuranCity/scripts.pory"
	.string "Juran City\n"
	.string "“Shop, stay, play.”$"

JuranCity_EventScript_Sign2_Text_0:
# 12 "data/maps/JuranCity/scripts.pory"
	.string "GRAND JURAN HOTEL & CASINO\n"
	.string "Opening soon.$"

JuranCity_EventScript_Npc1_Text_0:
# 16 "data/maps/JuranCity/scripts.pory"
	.string "Shops, hotels, casinos… Juran has it all.\n"
	.string "Even its own train line to Pokétopia!$"

JuranCity_EventScript_Npc2_Text_0:
# 20 "data/maps/JuranCity/scripts.pory"
	.string "I won big at the casino last night.\n"
	.string "Strange, though. The same fellows seem\l"
	.string "to win every night.$"

JuranCity_EventScript_Npc3_Text_0:
# 24 "data/maps/JuranCity/scripts.pory"
	.string "Some men in suits came by my stall\n"
	.string "asking for “protection money”. The big\l"
	.string "chains never get visits like that.$"

JuranCity_EventScript_Npc4_Text_0:
# 28 "data/maps/JuranCity/scripts.pory"
	.string "I'm taking the train to Pokétopia\n"
	.string "tomorrow. The night safari is supposed\l"
	.string "to be amazing!$"

JuranCity_EventScript_Npc5_Text_0:
# 32 "data/maps/JuranCity/scripts.pory"
	.string "Keep your wallet close in Juran. Not\n"
	.string "everyone at the tables plays fair.$"
