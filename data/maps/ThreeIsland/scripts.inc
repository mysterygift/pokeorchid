ThreeIsland_MapScripts::
# 2 "data/maps/ThreeIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, ThreeIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

ThreeIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/ThreeIsland/scripts.pory"
	setflag FLAG_VISITED_THREE_ISLAND
	return


ThreeIsland_EventScript_AntiBiker1::
# 8 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_AntiBiker1_Text_0, MSGBOX_NPC
	return


ThreeIsland_EventScript_AntiBiker2::
# 12 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_AntiBiker2_Text_0, MSGBOX_NPC
	return


ThreeIsland_EventScript_Biker::
# 16 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_Biker_Text_0, MSGBOX_NPC
	return


ThreeIsland_EventScript_Woman::
# 20 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_Woman_Text_0, MSGBOX_NPC
	return


ThreeIsland_EventScript_LittleBoy::
# 24 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_LittleBoy_Text_0, MSGBOX_NPC
	return


ThreeIsland_EventScript_Doduo::
# 28 "data/maps/ThreeIsland/scripts.pory"
	lock
# 29 "data/maps/ThreeIsland/scripts.pory"
	faceplayer
# 30 "data/maps/ThreeIsland/scripts.pory"
	waitse
# 31 "data/maps/ThreeIsland/scripts.pory"
	playmoncry SPECIES_DODUO, CRY_MODE_NORMAL
# 32 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_Doduo_Text_0
# 33 "data/maps/ThreeIsland/scripts.pory"
	waitmoncry
# 34 "data/maps/ThreeIsland/scripts.pory"
	release
	return


ThreeIsland_EventScript_Biker6::
# 38 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_Biker_Text_0, MSGBOX_NPC
	return


ThreeIsland_EventScript_IslandSign::
# 42 "data/maps/ThreeIsland/scripts.pory"
	msgbox ThreeIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


ThreeIsland_EventScript_AntiBiker1_Text_0:
# 8 "data/maps/ThreeIsland/scripts.pory"
	.string "The Sevii Islands are so peaceful. I\n"
	.string "could stay here forever.$"

ThreeIsland_EventScript_AntiBiker2_Text_0:
# 12 "data/maps/ThreeIsland/scripts.pory"
	.string "Each island has its own character. Have\n"
	.string "you visited them all?$"

ThreeIsland_EventScript_Biker_Text_0:
# 16 "data/maps/ThreeIsland/scripts.pory"
	.string "The roads on Three Island are short, so\n"
	.string "we ride in circles.$"

ThreeIsland_EventScript_Woman_Text_0:
# 20 "data/maps/ThreeIsland/scripts.pory"
	.string "A biker gang used to bother us here. Now\n"
	.string "they just ride up and down the island.$"

ThreeIsland_EventScript_LittleBoy_Text_0:
# 24 "data/maps/ThreeIsland/scripts.pory"
	.string "I found a pretty shell on the beach\n"
	.string "today!$"

ThreeIsland_EventScript_Doduo_Text_0:
# 32 "data/maps/ThreeIsland/scripts.pory"
	.string "DODUO: Gwaa gwaa!$"

ThreeIsland_EventScript_IslandSign_Text_0:
# 42 "data/maps/ThreeIsland/scripts.pory"
	.string "THREE ISLAND\n"
	.string "Kin Island. Bond Bridge to the west.$"
