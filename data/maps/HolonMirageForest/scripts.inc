HolonMirageForest_MapScripts::
	.byte 0


HolonMirageForest_EventScript_Sailor::
# 4 "data/maps/HolonMirageForest/scripts.pory"
	lock
# 5 "data/maps/HolonMirageForest/scripts.pory"
	faceplayer
# 7 "data/maps/HolonMirageForest/scripts.pory"
	call Holon_SailorReturnPlaceholder
# 8 "data/maps/HolonMirageForest/scripts.pory"
	release
	return


Holon_SailorReturnPlaceholder::
# 12 "data/maps/HolonMirageForest/scripts.pory"
	msgbox Holon_SailorReturnPlaceholder_Text_0, MSGBOX_DEFAULT
	return


HolonMirageForest_EventScript_Lass::
# 16 "data/maps/HolonMirageForest/scripts.pory"
	msgbox HolonMirageForest_EventScript_Lass_Text_0, MSGBOX_NPC
	return


HolonMirageForest_EventScript_Sign::
# 20 "data/maps/HolonMirageForest/scripts.pory"
	msgbox HolonMirageForest_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


HolonMirageForest_EventScript_Researcher1::
# 24 "data/maps/HolonMirageForest/scripts.pory"
	trainerbattle_single TRAINER_HOLON_IDO, HolonMirageForest_Text_Researcher1Intro, HolonMirageForest_Text_Researcher1Defeat
# 25 "data/maps/HolonMirageForest/scripts.pory"
	msgbox HolonMirageForest_Text_Researcher1Post, MSGBOX_AUTOCLOSE
	return


HolonMirageForest_EventScript_Researcher2::
# 41 "data/maps/HolonMirageForest/scripts.pory"
	trainerbattle_single TRAINER_HOLON_CHRISTOPHE, HolonMirageForest_Text_Researcher2Intro, HolonMirageForest_Text_Researcher2Defeat
# 42 "data/maps/HolonMirageForest/scripts.pory"
	msgbox HolonMirageForest_Text_Researcher2Post, MSGBOX_AUTOCLOSE
	return


Holon_SailorReturnPlaceholder_Text_0:
# 12 "data/maps/HolonMirageForest/scripts.pory"
	.string "Ahoy! Whenever you're ready to head\n"
	.string "home, just say the word.\p"
	.string "(Placeholder: the voyage return menu is\n"
	.string "added by the core voyage stream.)$"

HolonMirageForest_EventScript_Lass_Text_0:
# 16 "data/maps/HolonMirageForest/scripts.pory"
	.string "Folks call this the Mirage Forest. The\n"
	.string "trails twist so much they seem to move.\l"
	.string "Keep to the path east and you'll reach\l"
	.string "Holon Village.$"

HolonMirageForest_EventScript_Sign_Text_0:
# 20 "data/maps/HolonMirageForest/scripts.pory"
	.string "Mirage Forest\n"
	.string "Holon Village: follow the path east.$"

HolonMirageForest_Text_Researcher1Intro::
# 28 "data/maps/HolonMirageForest/scripts.pory"
	.string "These ruins sit on a Power Spot. You're\n"
	.string "standing right on my sensor line!$"

HolonMirageForest_Text_Researcher1Defeat::
# 32 "data/maps/HolonMirageForest/scripts.pory"
	.string "My readings... scrambled completely.$"

HolonMirageForest_Text_Researcher1Post::
# 36 "data/maps/HolonMirageForest/scripts.pory"
	.string "The old track here carried carved stone\n"
	.string "down to the lake, long before our tower\l"
	.string "was built.$"

HolonMirageForest_Text_Researcher2Intro::
# 45 "data/maps/HolonMirageForest/scripts.pory"
	.string "Delta Species gather wherever the\n"
	.string "Power Spot energy runs strong. Let me\l"
	.string "show you mine!$"

HolonMirageForest_Text_Researcher2Defeat::
# 49 "data/maps/HolonMirageForest/scripts.pory"
	.string "Fascinating. Your Pokémon adapt so\n"
	.string "quickly.$"

HolonMirageForest_Text_Researcher2Post::
# 53 "data/maps/HolonMirageForest/scripts.pory"
	.string "The energy changes a Pokémon's type,\n"
	.string "but never its heart. Or so we hope.$"
