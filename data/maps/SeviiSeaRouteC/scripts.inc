SeviiSeaRouteC_MapScripts::
	.byte 0


SeviiSeaRouteC_EventScript_Swimmer1::
# 4 "data/maps/SeviiSeaRouteC/scripts.pory"
	trainerbattle_single TRAINER_SEVII_RORY, SeviiSeaRouteC_Text_Swimmer1Intro, SeviiSeaRouteC_Text_Swimmer1Defeat
# 5 "data/maps/SeviiSeaRouteC/scripts.pory"
	msgbox SeviiSeaRouteC_Text_Swimmer1Post, MSGBOX_AUTOCLOSE
	return


SeviiSeaRouteC_EventScript_Swimmer2::
# 21 "data/maps/SeviiSeaRouteC/scripts.pory"
	trainerbattle_single TRAINER_SEVII_LANA, SeviiSeaRouteC_Text_Swimmer2Intro, SeviiSeaRouteC_Text_Swimmer2Defeat
# 22 "data/maps/SeviiSeaRouteC/scripts.pory"
	msgbox SeviiSeaRouteC_Text_Swimmer2Post, MSGBOX_AUTOCLOSE
	return


SeviiSeaRouteC_EventScript_Swimmer3::
# 38 "data/maps/SeviiSeaRouteC/scripts.pory"
	msgbox SeviiSeaRouteC_EventScript_Swimmer3_Text_0, MSGBOX_NPC
	return


SeviiSeaRouteC_EventScript_Swimmer3_Text_0:
# 38 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "Four Island is north and Five Island is\n"
	.string "east of here.$"

SeviiSeaRouteC_Text_Swimmer1Intro::
# 8 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "These waters are mine. Let's go!$"

SeviiSeaRouteC_Text_Swimmer1Defeat::
# 12 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "I'm sunk!$"

SeviiSeaRouteC_Text_Swimmer1Post::
# 16 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "The currents are gentle today. Perfect\n"
	.string "for a long swim.$"

SeviiSeaRouteC_Text_Swimmer2Intro::
# 25 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "Swimming between the islands builds\n"
	.string "stamina!$"

SeviiSeaRouteC_Text_Swimmer2Defeat::
# 29 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "I need a rest...$"

SeviiSeaRouteC_Text_Swimmer2Post::
# 33 "data/maps/SeviiSeaRouteC/scripts.pory"
	.string "Sometimes Lapras swim past these\n"
	.string "islands. It's beautiful.$"
