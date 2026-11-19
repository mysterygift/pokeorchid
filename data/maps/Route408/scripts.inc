Route408_MapScripts::
	.byte 0


Route408_EventScript_Sign::
# 5 "data/maps/Route408/scripts.pory"
	msgbox Route408_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route408_EventScript_Npc1::
# 9 "data/maps/Route408/scripts.pory"
	msgbox Route408_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route408_EventScript_Sign_Text_0:
# 5 "data/maps/Route408/scripts.pory"
	.string "Route 408$"

Route408_EventScript_Npc1_Text_0:
# 9 "data/maps/Route408/scripts.pory"
	.string "This road follows the shore of the bay.\n"
	.string "On a calm day you can see right across\l"
	.string "the water.$"
