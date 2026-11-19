Route405_MapScripts::
	.byte 0


Route405_EventScript_Sign::
# 5 "data/maps/Route405/scripts.pory"
	msgbox Route405_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route405_EventScript_Npc1::
# 9 "data/maps/Route405/scripts.pory"
	msgbox Route405_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route405_EventScript_Sign_Text_0:
# 5 "data/maps/Route405/scripts.pory"
	.string "Route 405$"

Route405_EventScript_Npc1_Text_0:
# 9 "data/maps/Route405/scripts.pory"
	.string "Ube City is south of here. It's the only\n"
	.string "city in Tiksi. Silph Co. even has an\l"
	.string "office there!$"
