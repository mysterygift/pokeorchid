Route406_MapScripts::
	.byte 0


Route406_EventScript_Sign::
# 5 "data/maps/Route406/scripts.pory"
	msgbox Route406_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route406_EventScript_Npc1::
# 9 "data/maps/Route406/scripts.pory"
	msgbox Route406_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route406_EventScript_Sign_Text_0:
# 5 "data/maps/Route406/scripts.pory"
	.string "Route 406$"

Route406_EventScript_Npc1_Text_0:
# 9 "data/maps/Route406/scripts.pory"
	.string "Tanglyn Town is at the east end. Have\n"
	.string "you seen the murals there? They're\l"
	.string "older than Tosa!$"
