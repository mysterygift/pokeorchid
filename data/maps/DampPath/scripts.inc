DampPath_MapScripts::
	.byte 0


DampPath_EventScript_PlaceholderSign::
# 4 "data/maps/DampPath/scripts.pory"
	msgbox DampPath_EventScript_PlaceholderSign_Text_0, MSGBOX_SIGN
	return


DampPath_EventScript_Route1::
# 10 "data/maps/DampPath/scripts.pory"
	msgbox DampPath_EventScript_Route1_Text_0, MSGBOX_NPC
	return


DampPath_EventScript_PlaceholderSign_Text_0:
# 4 "data/maps/DampPath/scripts.pory"
	.string "Damp Path: a wet, abandoned path\n"
	.string "through the hills of West Tosa. Filled\l"
	.string "with rowdy thugs and ne'er-do-wells\l"
	.string "now. And Zubat. Placeholder map.$"

DampPath_EventScript_Route1_Text_0:
# 10 "data/maps/DampPath/scripts.pory"
	.string "Oi, this is our path! Pay the toll or turn\n"
	.string "back!\p"
	.string "…Just kidding. The Zubat are the real\n"
	.string "problem down here.$"
