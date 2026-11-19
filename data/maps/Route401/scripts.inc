Route401_MapScripts::
	.byte 0


Route401_EventScript_Sign::
# 5 "data/maps/Route401/scripts.pory"
	msgbox Route401_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route401_EventScript_Npc1::
# 9 "data/maps/Route401/scripts.pory"
	msgbox Route401_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route401_EventScript_Sign_Text_0:
# 5 "data/maps/Route401/scripts.pory"
	.string "Route 401$"

Route401_EventScript_Npc1_Text_0:
# 9 "data/maps/Route401/scripts.pory"
	.string "You came on that boat? Nobody comes to\n"
	.string "Tiksi on purpose. Furong's just east of\l"
	.string "here, if you need a bed.$"
