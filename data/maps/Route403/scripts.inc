Route403_MapScripts::
	.byte 0


Route403_EventScript_Sign::
# 5 "data/maps/Route403/scripts.pory"
	msgbox Route403_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route403_EventScript_Npc1::
# 9 "data/maps/Route403/scripts.pory"
	msgbox Route403_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route403_EventScript_Sign_Text_0:
# 5 "data/maps/Route403/scripts.pory"
	.string "Route 403$"

Route403_EventScript_Npc1_Text_0:
# 9 "data/maps/Route403/scripts.pory"
	.string "The shrine up north sits in the middle\n"
	.string "of a desert. The locals won't go near it.$"
