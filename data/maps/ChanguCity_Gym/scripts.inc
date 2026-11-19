ChanguCity_Gym_MapScripts::
	.byte 0


ChanguCity_Gym_EventScript_Leader::
# 4 "data/maps/ChanguCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_LARRY, ChanguCity_Gym_Text_Intro, ChanguCity_Gym_Text_Defeat, ChanguCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/ChanguCity_Gym/scripts.pory"
	msgbox ChanguCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


ChanguCity_Gym_EventScript_Defeated::
# 9 "data/maps/ChanguCity_Gym/scripts.pory"
	setflag FLAG_BADGE03_GET
# 10 "data/maps/ChanguCity_Gym/scripts.pory"
	msgbox ChanguCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/ChanguCity_Gym/scripts.pory"
	release
	return


ChanguCity_Gym_EventScript_Guide::
# 15 "data/maps/ChanguCity_Gym/scripts.pory"
	msgbox ChanguCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


ChanguCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/ChanguCity_Gym/scripts.pory"
	.string "{PLAYER} received the Larry Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

ChanguCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/ChanguCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of\n"
	.string "Larry, who uses Normal-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Larry and this empty hall!$"

ChanguCity_Gym_Text_Intro::
# 18 "data/maps/ChanguCity_Gym/scripts.pory"
	.string "I'm Larry. Paldea's Champion sent me\n"
	.string "here to build bridges with the Tosa\l"
	.string "League. Normal battle, normal Pokémon.\l"
	.string "Let's get this over with.$"

ChanguCity_Gym_Text_Defeat::
# 22 "data/maps/ChanguCity_Gym/scripts.pory"
	.string "…Well. That's that, then.$"

ChanguCity_Gym_Text_Post::
# 26 "data/maps/ChanguCity_Gym/scripts.pory"
	.string "I'd like to go home and have a nap now.\n"
	.string "That's normal, isn't it?$"
