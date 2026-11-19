Route402_MapScripts::
	.byte 0


Route402_EventScript_Sign::
# 5 "data/maps/Route402/scripts.pory"
	msgbox Route402_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route402_EventScript_Npc1::
# 9 "data/maps/Route402/scripts.pory"
	msgbox Route402_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route402_EventScript_Sign_Text_0:
# 5 "data/maps/Route402/scripts.pory"
	.string "Route 402$"

Route402_EventScript_Npc1_Text_0:
# 9 "data/maps/Route402/scripts.pory"
	.string "Mt. Drake starts just north of here. Its\n"
	.string "peaks are higher than anything in Tosa.$"
