OneIsland_KindleRoad_MapScripts::
	.byte 0


OneIsland_KindleRoad_EventScript_Maria::
# 4 "data/maps/OneIsland_KindleRoad/scripts.pory"
	trainerbattle_single TRAINER_SEVII_MARIA, OneIsland_KindleRoad_Text_MariaIntro, OneIsland_KindleRoad_Text_MariaDefeat
# 5 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_Text_MariaPost, MSGBOX_AUTOCLOSE
	return


OneIsland_KindleRoad_EventScript_Abigail::
# 21 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Abigail_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_Finn::
# 25 "data/maps/OneIsland_KindleRoad/scripts.pory"
	trainerbattle_single TRAINER_SEVII_FINN, OneIsland_KindleRoad_Text_FinnIntro, OneIsland_KindleRoad_Text_FinnDefeat
# 26 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_Text_FinnPost, MSGBOX_AUTOCLOSE
	return


OneIsland_KindleRoad_EventScript_Garrett::
# 42 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Garrett_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_Tommy::
# 46 "data/maps/OneIsland_KindleRoad/scripts.pory"
	trainerbattle_single TRAINER_SEVII_TOMMY, OneIsland_KindleRoad_Text_TommyIntro, OneIsland_KindleRoad_Text_TommyDefeat
# 47 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_Text_TommyPost, MSGBOX_AUTOCLOSE
	return


OneIsland_KindleRoad_EventScript_Sharon::
# 63 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Sharon_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_Tanya::
# 67 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Tanya_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_Shea::
# 71 "data/maps/OneIsland_KindleRoad/scripts.pory"
	trainerbattle_single TRAINER_SEVII_SHEA, OneIsland_KindleRoad_Text_SheaIntro, OneIsland_KindleRoad_Text_SheaDefeat
# 72 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_Text_SheaPost, MSGBOX_AUTOCLOSE
	return


OneIsland_KindleRoad_EventScript_Hugh::
# 88 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Hugh_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_Bryce::
# 92 "data/maps/OneIsland_KindleRoad/scripts.pory"
	trainerbattle_single TRAINER_SEVII_BRYCE, OneIsland_KindleRoad_Text_BryceIntro, OneIsland_KindleRoad_Text_BryceDefeat
# 93 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_Text_BrycePost, MSGBOX_AUTOCLOSE
	return


OneIsland_KindleRoad_EventScript_Claire::
# 109 "data/maps/OneIsland_KindleRoad/scripts.pory"
	trainerbattle_single TRAINER_SEVII_CLAIRE, OneIsland_KindleRoad_Text_ClaireIntro, OneIsland_KindleRoad_Text_ClaireDefeat
# 110 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_Text_ClairePost, MSGBOX_AUTOCLOSE
	return


OneIsland_KindleRoad_EventScript_Mik::
# 126 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Tanya_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_Kia::
# 130 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_Sharon_Text_0, MSGBOX_NPC
	return


OneIsland_KindleRoad_EventScript_EmberSpaSign::
# 134 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_EmberSpaSign_Text_0, MSGBOX_SIGN
	return


OneIsland_KindleRoad_EventScript_RouteSign::
# 139 "data/maps/OneIsland_KindleRoad/scripts.pory"
	msgbox OneIsland_KindleRoad_EventScript_RouteSign_Text_0, MSGBOX_SIGN
	return


OneIsland_KindleRoad_EventScript_Abigail_Text_0:
# 21 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The spa halfway up the road is the best\n"
	.string "rest stop around.$"

OneIsland_KindleRoad_EventScript_Garrett_Text_0:
# 42 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The water around the Sevii Islands is\n"
	.string "so clear!$"

OneIsland_KindleRoad_EventScript_Sharon_Text_0:
# 63 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The hot springs here are the best for\n"
	.string "sore muscles.$"

OneIsland_KindleRoad_EventScript_Tanya_Text_0:
# 67 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Kindle Road leads all the way up to Mt.\n"
	.string "Ember.$"

OneIsland_KindleRoad_EventScript_Hugh_Text_0:
# 88 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "A true fighter trains wherever the road\n"
	.string "takes them.$"

OneIsland_KindleRoad_EventScript_EmberSpaSign_Text_0:
# 134 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "EMBER SPA\n"
	.string "Rest your weary feet in volcanic hot\l"
	.string "water.$"

OneIsland_KindleRoad_EventScript_RouteSign_Text_0:
# 139 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "KINDLE ROAD\n"
	.string "Mt. Ember ahead. Mind the hot rocks.$"

OneIsland_KindleRoad_Text_MariaIntro::
# 8 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The sea off Kindle Road is my training\n"
	.string "pool!$"

OneIsland_KindleRoad_Text_MariaDefeat::
# 12 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "I swallowed seawater...$"

OneIsland_KindleRoad_Text_MariaPost::
# 16 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The currents are gentle today. Perfect\n"
	.string "for a long swim.$"

OneIsland_KindleRoad_Text_FinnIntro::
# 29 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Surfing past me? Not without a battle!$"

OneIsland_KindleRoad_Text_FinnDefeat::
# 33 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Washed right out.$"

OneIsland_KindleRoad_Text_FinnPost::
# 37 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The spa halfway up the road is the best\n"
	.string "rest stop around.$"

OneIsland_KindleRoad_Text_TommyIntro::
# 50 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Shh! You'll scare the fish! Fine, let's\n"
	.string "battle.$"

OneIsland_KindleRoad_Text_TommyDefeat::
# 54 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "My line snapped...$"

OneIsland_KindleRoad_Text_TommyPost::
# 58 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "A Gyarados nearly pulled me in\n"
	.string "yesterday!$"

OneIsland_KindleRoad_Text_SheaIntro::
# 75 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Kindle Road is my training ground!\n"
	.string "Hiyah!$"

OneIsland_KindleRoad_Text_SheaDefeat::
# 79 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "My stance was off!$"

OneIsland_KindleRoad_Text_SheaPost::
# 83 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The hot springs here are the best for\n"
	.string "sore muscles.$"

OneIsland_KindleRoad_Text_BryceIntro::
# 96 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "I'm camping by the hot springs. Want to\n"
	.string "battle?$"

OneIsland_KindleRoad_Text_BryceDefeat::
# 100 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Back to my tent...$"

OneIsland_KindleRoad_Text_BrycePost::
# 104 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "Kindle Road leads all the way up to Mt.\n"
	.string "Ember.$"

OneIsland_KindleRoad_Text_ClaireIntro::
# 113 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "A picnic and a battle! The perfect day\n"
	.string "out!$"

OneIsland_KindleRoad_Text_ClaireDefeat::
# 117 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "My picnic is ruined!$"

OneIsland_KindleRoad_Text_ClairePost::
# 121 "data/maps/OneIsland_KindleRoad/scripts.pory"
	.string "The spa halfway up the road is the best\n"
	.string "rest stop around.$"
