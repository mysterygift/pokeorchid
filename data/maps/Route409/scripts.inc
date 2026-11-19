Route409_MapScripts::
	.byte 0


Route409_EventScript_Sign::
# 5 "data/maps/Route409/scripts.pory"
	msgbox Route409_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route409_EventScript_Npc1::
# 9 "data/maps/Route409/scripts.pory"
	msgbox Route409_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route409_EventScript_Sign_Text_0:
# 5 "data/maps/Route409/scripts.pory"
	.string "Route 409\n"
	.string "A strangely frozen route, despite\l"
	.string "Tiksi's generally warm arid climate.$"

Route409_EventScript_Npc1_Text_0:
# 9 "data/maps/Route409/scripts.pory"
	.string "Feel that chill? Tiksi is warm\n"
	.string "everywhere else. The cold comes from\l"
	.string "the cave at the end of this route…$"
