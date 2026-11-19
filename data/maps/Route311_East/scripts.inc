Route311_East_MapScripts::
	.byte 0


Route311_East_EventScript_PlaceholderSign::
# 4 "data/maps/Route311_East/scripts.pory"
	msgbox Route311_East_EventScript_PlaceholderSign_Text_0, MSGBOX_SIGN
	return


Route311_East_EventScript_Route1::
# 10 "data/maps/Route311_East/scripts.pory"
	msgbox Route311_East_EventScript_Route1_Text_0, MSGBOX_NPC
	return


Route311_East_EventScript_PlaceholderSign_Text_0:
# 4 "data/maps/Route311_East/scripts.pory"
	.string "Route 311 (east of the Damp Path)\n"
	.string "Placeholder map.$"

Route311_East_EventScript_Route1_Text_0:
# 10 "data/maps/Route311_East/scripts.pory"
	.string "You came through the Damp Path? Brave.\n"
	.string "Or foolish.$"
