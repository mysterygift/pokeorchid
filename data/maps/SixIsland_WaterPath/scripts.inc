SixIsland_WaterPath_MapScripts::
	.byte 0


SixIsland_WaterPath_EventScript_Rose::
# 4 "data/maps/SixIsland_WaterPath/scripts.pory"
	trainerbattle_single TRAINER_SEVII_ROSE, SixIsland_WaterPath_Text_RoseIntro, SixIsland_WaterPath_Text_RoseDefeat
# 5 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_Text_RosePost, MSGBOX_AUTOCLOSE
	return


SixIsland_WaterPath_EventScript_Edward::
# 21 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_EventScript_Edward_Text_0, MSGBOX_NPC
	return


SixIsland_WaterPath_EventScript_Samir::
# 25 "data/maps/SixIsland_WaterPath/scripts.pory"
	trainerbattle_single TRAINER_SEVII_SAMIR, SixIsland_WaterPath_Text_SamirIntro, SixIsland_WaterPath_Text_SamirDefeat
# 26 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_Text_SamirPost, MSGBOX_AUTOCLOSE
	return


SixIsland_WaterPath_EventScript_Denise::
# 42 "data/maps/SixIsland_WaterPath/scripts.pory"
	trainerbattle_single TRAINER_SEVII_DENISE, SixIsland_WaterPath_Text_DeniseIntro, SixIsland_WaterPath_Text_DeniseDefeat
# 43 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_Text_DenisePost, MSGBOX_AUTOCLOSE
	return


SixIsland_WaterPath_EventScript_Miu::
# 59 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_EventScript_Miu_Text_0, MSGBOX_NPC
	return


SixIsland_WaterPath_EventScript_Mia::
# 63 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_EventScript_Mia_Text_0, MSGBOX_NPC
	return


SixIsland_WaterPath_EventScript_Earl::
# 67 "data/maps/SixIsland_WaterPath/scripts.pory"
	trainerbattle_single TRAINER_SEVII_EARL, SixIsland_WaterPath_Text_EarlIntro, SixIsland_WaterPath_Text_EarlDefeat
# 68 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_Text_EarlPost, MSGBOX_AUTOCLOSE
	return


SixIsland_WaterPath_EventScript_HornWantedSign::
# 84 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_EventScript_HornWantedSign_Text_0, MSGBOX_SIGN
	return


SixIsland_WaterPath_EventScript_RouteSign::
# 89 "data/maps/SixIsland_WaterPath/scripts.pory"
	msgbox SixIsland_WaterPath_EventScript_RouteSign_Text_0, MSGBOX_SIGN
	return


SixIsland_WaterPath_EventScript_Edward_Text_0:
# 21 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "Water Path winds between the sea and\n"
	.string "the hills.$"

SixIsland_WaterPath_EventScript_Miu_Text_0:
# 59 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "There's a house up the path with a\n"
	.string "horn-obsessed collector.$"

SixIsland_WaterPath_EventScript_Mia_Text_0:
# 63 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "My big brother lets me ride on his\n"
	.string "Lapras sometimes!$"

SixIsland_WaterPath_EventScript_HornWantedSign_Text_0:
# 84 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "Wanted: a HERACROSS with a magnificent\n"
	.string "horn.\n"
	.string "Enquire at the house up the path.$"

SixIsland_WaterPath_EventScript_RouteSign_Text_0:
# 89 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "WATER PATH\n"
	.string "Ruin Valley lies to the south.$"

SixIsland_WaterPath_Text_RoseIntro::
# 8 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "The flowers along Water Path smell\n"
	.string "lovely!$"

SixIsland_WaterPath_Text_RoseDefeat::
# 12 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "My petals wilted...$"

SixIsland_WaterPath_Text_RosePost::
# 16 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "A ferry hops between the islands from\n"
	.string "every harbour.$"

SixIsland_WaterPath_Text_SamirIntro::
# 29 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "Nobody swims Water Path faster than\n"
	.string "me!$"

SixIsland_WaterPath_Text_SamirDefeat::
# 33 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "Overtaken!$"

SixIsland_WaterPath_Text_SamirPost::
# 37 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "There's a house up the path with a\n"
	.string "horn-obsessed collector.$"

SixIsland_WaterPath_Text_DeniseIntro::
# 46 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "The water's so clear here! Battle?$"

SixIsland_WaterPath_Text_DeniseDefeat::
# 50 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "That light went out.$"

SixIsland_WaterPath_Text_DenisePost::
# 54 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "There's a house up the path with a\n"
	.string "horn-obsessed collector.$"

SixIsland_WaterPath_Text_EarlIntro::
# 71 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "Ruin Valley's hills keep me strong!$"

SixIsland_WaterPath_Text_EarlDefeat::
# 75 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "My knees gave out.$"

SixIsland_WaterPath_Text_EarlPost::
# 79 "data/maps/SixIsland_WaterPath/scripts.pory"
	.string "The ground here rumbles sometimes. Mt.\n"
	.string "Ember isn't fully asleep.$"
