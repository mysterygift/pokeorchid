FourIsland_MapScripts::
# 2 "data/maps/FourIsland/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FourIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

FourIsland_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/FourIsland/scripts.pory"
	setflag FLAG_VISITED_FOUR_ISLAND
	return


FourIsland_EventScript_DaycareMan::
# 8 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_DaycareMan_Text_0, MSGBOX_NPC
	return


FourIsland_EventScript_Doduo::
# 12 "data/maps/FourIsland/scripts.pory"
	lock
# 13 "data/maps/FourIsland/scripts.pory"
	faceplayer
# 14 "data/maps/FourIsland/scripts.pory"
	waitse
# 15 "data/maps/FourIsland/scripts.pory"
	playmoncry SPECIES_DODUO, CRY_MODE_NORMAL
# 16 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_Doduo_Text_0
# 17 "data/maps/FourIsland/scripts.pory"
	waitmoncry
# 18 "data/maps/FourIsland/scripts.pory"
	release
	return


FourIsland_EventScript_NidoranF::
# 22 "data/maps/FourIsland/scripts.pory"
	lock
# 23 "data/maps/FourIsland/scripts.pory"
	faceplayer
# 24 "data/maps/FourIsland/scripts.pory"
	waitse
# 25 "data/maps/FourIsland/scripts.pory"
	playmoncry SPECIES_NIDORAN_F, CRY_MODE_NORMAL
# 26 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_NidoranF_Text_0
# 27 "data/maps/FourIsland/scripts.pory"
	waitmoncry
# 28 "data/maps/FourIsland/scripts.pory"
	release
	return


FourIsland_EventScript_NidoranM::
# 32 "data/maps/FourIsland/scripts.pory"
	lock
# 33 "data/maps/FourIsland/scripts.pory"
	faceplayer
# 34 "data/maps/FourIsland/scripts.pory"
	waitse
# 35 "data/maps/FourIsland/scripts.pory"
	playmoncry SPECIES_NIDORAN_M, CRY_MODE_NORMAL
# 36 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_NidoranM_Text_0
# 37 "data/maps/FourIsland/scripts.pory"
	waitmoncry
# 38 "data/maps/FourIsland/scripts.pory"
	release
	return


FourIsland_EventScript_Psyduck::
# 42 "data/maps/FourIsland/scripts.pory"
	lock
# 43 "data/maps/FourIsland/scripts.pory"
	faceplayer
# 44 "data/maps/FourIsland/scripts.pory"
	waitse
# 45 "data/maps/FourIsland/scripts.pory"
	playmoncry SPECIES_PSYDUCK, CRY_MODE_NORMAL
# 46 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_Psyduck_Text_0
# 47 "data/maps/FourIsland/scripts.pory"
	waitmoncry
# 48 "data/maps/FourIsland/scripts.pory"
	release
	return


FourIsland_EventScript_OldWoman::
# 52 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_OldWoman_Text_0, MSGBOX_NPC
	return


FourIsland_EventScript_FatMan::
# 56 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_FatMan_Text_0, MSGBOX_NPC
	return


FourIsland_EventScript_LittleGirl::
# 60 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_LittleGirl_Text_0, MSGBOX_NPC
	return


FourIsland_EventScript_IslandSign::
# 64 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_IslandSign_Text_0, MSGBOX_SIGN
	return


FourIsland_EventScript_LoreleisHouseSign::
# 69 "data/maps/FourIsland/scripts.pory"
	msgbox FourIsland_EventScript_LoreleisHouseSign_Text_0, MSGBOX_SIGN
	return


FourIsland_EventScript_DaycareMan_Text_0:
# 8 "data/maps/FourIsland/scripts.pory"
	.string "We look after POKéMON while their\n"
	.string "trainers explore the islands.$"

FourIsland_EventScript_Doduo_Text_0:
# 16 "data/maps/FourIsland/scripts.pory"
	.string "DODUO: Mrrrr!$"

FourIsland_EventScript_NidoranF_Text_0:
# 26 "data/maps/FourIsland/scripts.pory"
	.string "NIDORAN: Gyaoo!$"

FourIsland_EventScript_NidoranM_Text_0:
# 36 "data/maps/FourIsland/scripts.pory"
	.string "NIDORAN: Grrr!$"

FourIsland_EventScript_Psyduck_Text_0:
# 46 "data/maps/FourIsland/scripts.pory"
	.string "PSYDUCK: Pii-pii!$"

FourIsland_EventScript_OldWoman_Text_0:
# 52 "data/maps/FourIsland/scripts.pory"
	.string "The ice cave across the water stays\n"
	.string "frozen all year round. Strange, isn't it?$"

FourIsland_EventScript_FatMan_Text_0:
# 56 "data/maps/FourIsland/scripts.pory"
	.string "Lorelei lives on this island. She's\n"
	.string "terribly strong, but kind to the\l"
	.string "children.$"

FourIsland_EventScript_LittleGirl_Text_0:
# 60 "data/maps/FourIsland/scripts.pory"
	.string "I'm building a snow POKéMON from the\n"
	.string "cave ice! It keeps melting...$"

FourIsland_EventScript_IslandSign_Text_0:
# 64 "data/maps/FourIsland/scripts.pory"
	.string "FOUR ISLAND\n"
	.string "Floe Island. The ice cave lies across\l"
	.string "the water.$"

FourIsland_EventScript_LoreleisHouseSign_Text_0:
# 69 "data/maps/FourIsland/scripts.pory"
	.string "LORELEI'S HOUSE$"
