Route410_MapScripts::
	.byte 0


Route410_EventScript_Sign::
# 5 "data/maps/Route410/scripts.pory"
	msgbox Route410_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


Route410_EventScript_Npc1::
# 9 "data/maps/Route410/scripts.pory"
	msgbox Route410_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


Route410_EventScript_Sign_Text_0:
# 5 "data/maps/Route410/scripts.pory"
	.string "Route 410\n"
	.string "A well-concealed route only known by\l"
	.string "locals of Tiksi.$"

Route410_EventScript_Npc1_Text_0:
# 9 "data/maps/Route410/scripts.pory"
	.string "Hm? You found this path? Only us locals\n"
	.string "know about it. It leads down to the\l"
	.string "delta.$"
