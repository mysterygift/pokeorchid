SeviiSeaRouteA_MapScripts::
	.byte 0


SeviiSeaRouteA_EventScript_Swimmer1::
# 4 "data/maps/SeviiSeaRouteA/scripts.pory"
	trainerbattle_single TRAINER_SEVII_DYLAN, SeviiSeaRouteA_Text_Swimmer1Intro, SeviiSeaRouteA_Text_Swimmer1Defeat
# 5 "data/maps/SeviiSeaRouteA/scripts.pory"
	msgbox SeviiSeaRouteA_Text_Swimmer1Post, MSGBOX_AUTOCLOSE
	return


SeviiSeaRouteA_EventScript_Swimmer2::
# 21 "data/maps/SeviiSeaRouteA/scripts.pory"
	msgbox SeviiSeaRouteA_EventScript_Swimmer2_Text_0, MSGBOX_NPC
	return


SeviiSeaRouteA_EventScript_Swimmer2_Text_0:
# 21 "data/maps/SeviiSeaRouteA/scripts.pory"
	.string "This strait links One Island and Two\n"
	.string "Island.$"

SeviiSeaRouteA_Text_Swimmer1Intro::
# 8 "data/maps/SeviiSeaRouteA/scripts.pory"
	.string "Crossing the strait? Race you... in\n"
	.string "battle!$"

SeviiSeaRouteA_Text_Swimmer1Defeat::
# 12 "data/maps/SeviiSeaRouteA/scripts.pory"
	.string "You're faster than the current!$"

SeviiSeaRouteA_Text_Swimmer1Post::
# 16 "data/maps/SeviiSeaRouteA/scripts.pory"
	.string "This strait links One Island and Two\n"
	.string "Island.$"
