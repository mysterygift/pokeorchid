FiveIsland_MemorialPillar_MapScripts::
	.byte 0


FiveIsland_MemorialPillar_EventScript_MemorialMan::
# 4 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	msgbox FiveIsland_MemorialPillar_EventScript_MemorialMan_Text_0, MSGBOX_NPC
	return


FiveIsland_MemorialPillar_EventScript_Milo::
# 8 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	trainerbattle_single TRAINER_SEVII_MILO, FiveIsland_MemorialPillar_Text_MiloIntro, FiveIsland_MemorialPillar_Text_MiloDefeat
# 9 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	msgbox FiveIsland_MemorialPillar_Text_MiloPost, MSGBOX_AUTOCLOSE
	return


FiveIsland_MemorialPillar_EventScript_Chaz::
# 25 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	trainerbattle_single TRAINER_SEVII_CHAZ, FiveIsland_MemorialPillar_Text_ChazIntro, FiveIsland_MemorialPillar_Text_ChazDefeat
# 26 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	msgbox FiveIsland_MemorialPillar_Text_ChazPost, MSGBOX_AUTOCLOSE
	return


FiveIsland_MemorialPillar_EventScript_Harold::
# 42 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	trainerbattle_single TRAINER_SEVII_HAROLD, FiveIsland_MemorialPillar_Text_HaroldIntro, FiveIsland_MemorialPillar_Text_HaroldDefeat
# 43 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	msgbox FiveIsland_MemorialPillar_Text_HaroldPost, MSGBOX_AUTOCLOSE
	return


FiveIsland_MemorialPillar_EventScript_Memorial::
# 59 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	msgbox FiveIsland_MemorialPillar_EventScript_Memorial_Text_0, MSGBOX_SIGN
	return


FiveIsland_MemorialPillar_EventScript_MemorialMan_Text_0:
# 4 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "I come every day to polish this pillar\n"
	.string "for my old partner. It helps me\l"
	.string "remember.$"

FiveIsland_MemorialPillar_EventScript_Memorial_Text_0:
# 59 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "In memory of a dear partner.\n"
	.string "The stone is clean and freshly polished.$"

FiveIsland_MemorialPillar_Text_MiloIntro::
# 12 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "My birds soar over Five Isle! Battle!$"

FiveIsland_MemorialPillar_Text_MiloDefeat::
# 16 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "Grounded!$"

FiveIsland_MemorialPillar_Text_MiloPost::
# 20 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "A ferry hops between the islands from\n"
	.string "every harbour.$"

FiveIsland_MemorialPillar_Text_ChazIntro::
# 29 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "The wind off the sea is perfect for\n"
	.string "flying!$"

FiveIsland_MemorialPillar_Text_ChazDefeat::
# 33 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "My birds lost their wind.$"

FiveIsland_MemorialPillar_Text_ChazPost::
# 37 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "People come here to remember POKéMON\n"
	.string "they've lost. It's very quiet.$"

FiveIsland_MemorialPillar_Text_HaroldIntro::
# 46 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "Hoo! Hoo! Battle me!$"

FiveIsland_MemorialPillar_Text_HaroldDefeat::
# 50 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "My owl saw that coming...$"

FiveIsland_MemorialPillar_Text_HaroldPost::
# 54 "data/maps/FiveIsland_MemorialPillar/scripts.pory"
	.string "A ferry hops between the islands from\n"
	.string "every harbour.$"
