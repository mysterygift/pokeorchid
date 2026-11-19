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


Route403_EventScript_Guardian1::
# 13 "data/maps/Route403/scripts.pory"
	msgbox Route403_EventScript_Guardian1_Text_0, MSGBOX_NPC
	return


Route403_EventScript_Sign_Text_0:
# 5 "data/maps/Route403/scripts.pory"
	.string "Route 403$"

Route403_EventScript_Npc1_Text_0:
# 9 "data/maps/Route403/scripts.pory"
	.string "The shrine up north sits in the middle\n"
	.string "of a desert. The locals won't go near it.$"

Route403_EventScript_Guardian1_Text_0:
# 13 "data/maps/Route403/scripts.pory"
	.string "This path leads to Regolis Shrine, in\n"
	.string "the heart of the desert. The rock giant\l"
	.string "sleeps there once more.\p"
	.string "I am its guardian. Go if you must.$"
