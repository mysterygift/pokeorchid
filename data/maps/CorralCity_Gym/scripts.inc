CorralCity_Gym_MapScripts::
	.byte 0


CorralCity_Gym_EventScript_Leader::
# 4 "data/maps/CorralCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_MARINA, CorralCity_Gym_Text_Intro, CorralCity_Gym_Text_Defeat, CorralCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/CorralCity_Gym/scripts.pory"
	msgbox CorralCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


CorralCity_Gym_EventScript_Defeated::
# 9 "data/maps/CorralCity_Gym/scripts.pory"
	setflag FLAG_BADGE02_GET
# 10 "data/maps/CorralCity_Gym/scripts.pory"
	msgbox CorralCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/CorralCity_Gym/scripts.pory"
	release
	return


CorralCity_Gym_EventScript_Guide::
# 15 "data/maps/CorralCity_Gym/scripts.pory"
	msgbox CorralCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


CorralCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/CorralCity_Gym/scripts.pory"
	.string "{PLAYER} received the Marina Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

CorralCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/CorralCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of\n"
	.string "Marina, who uses Water-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Marina and this empty\l"
	.string "hall!$"

CorralCity_Gym_Text_Intro::
# 18 "data/maps/CorralCity_Gym/scripts.pory"
	.string "I've swum every current around\n"
	.string "Pokétopia. Let's see if you can keep\l"
	.string "your head above water!$"

CorralCity_Gym_Text_Defeat::
# 22 "data/maps/CorralCity_Gym/scripts.pory"
	.string "You read the tide better than I did\n"
	.string "today.$"

CorralCity_Gym_Text_Post::
# 26 "data/maps/CorralCity_Gym/scripts.pory"
	.string "The sea always gives back what you put\n"
	.string "into it.$"
