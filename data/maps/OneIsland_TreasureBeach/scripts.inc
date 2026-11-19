OneIsland_TreasureBeach_MapScripts::
	.byte 0


OneIsland_TreasureBeach_EventScript_Amara::
# 4 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	trainerbattle_single TRAINER_SEVII_AMARA, OneIsland_TreasureBeach_Text_AmaraIntro, OneIsland_TreasureBeach_Text_AmaraDefeat
# 5 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	msgbox OneIsland_TreasureBeach_Text_AmaraPost, MSGBOX_AUTOCLOSE
	return


OneIsland_TreasureBeach_EventScript_Boy::
# 21 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	msgbox OneIsland_TreasureBeach_EventScript_Boy_Text_0, MSGBOX_NPC
	return


OneIsland_TreasureBeach_EventScript_Boy_Text_0:
# 21 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	.string "The tide washes all kinds of things up\n"
	.string "on Treasure Beach. Look carefully in\l"
	.string "the sand!$"

OneIsland_TreasureBeach_Text_AmaraIntro::
# 8 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	.string "Looking for treasure? Get past me\n"
	.string "first!$"

OneIsland_TreasureBeach_Text_AmaraDefeat::
# 12 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	.string "You found my weak spot.$"

OneIsland_TreasureBeach_Text_AmaraPost::
# 16 "data/maps/OneIsland_TreasureBeach/scripts.pory"
	.string "The water around the Sevii Islands is\n"
	.string "so clear!$"
