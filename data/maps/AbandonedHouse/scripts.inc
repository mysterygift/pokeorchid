AbandonedHouse_MapScripts::
	.byte 0


AbandonedHouse_EventScript_TownSign::
# 5 "data/maps/AbandonedHouse/scripts.pory"
	msgbox AbandonedHouse_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


AbandonedHouse_EventScript_Npc1::
# 9 "data/maps/AbandonedHouse/scripts.pory"
	msgbox AbandonedHouse_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


AbandonedHouse_EventScript_TownSign_Text_0:
# 5 "data/maps/AbandonedHouse/scripts.pory"
	.string "Abandoned House\n"
	.string "“…”$"

AbandonedHouse_EventScript_Npc1_Text_0:
# 9 "data/maps/AbandonedHouse/scripts.pory"
	.string "People in Moongrove see lights in that\n"
	.string "house at night.\p"
	.string "Nobody has lived there since the early\n"
	.string "days of Tosa…$"
