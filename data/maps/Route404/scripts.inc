Route404_MapScripts::
	.byte 0


Route404_EventScript_Sign::
# 5 "data/maps/Route404/scripts.pory"
	msgbox Route404_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route404_EventScript_Npc1::
# 9 "data/maps/Route404/scripts.pory"
	msgbox Route404_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route404_EventScript_Sign_Text_0:
# 5 "data/maps/Route404/scripts.pory"
	.string "Route 404$"

Route404_EventScript_Npc1_Text_0:
# 9 "data/maps/Route404/scripts.pory"
	.string "Drake Base Camp is where climbers rest\n"
	.string "before Mt. Drake. Warm stew, cold\l"
	.string "nights.$"
