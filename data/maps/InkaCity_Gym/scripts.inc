InkaCity_Gym_MapScripts::
	.byte 0


InkaCity_Gym_EventScript_Leader::
# 4 "data/maps/InkaCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_FREA, InkaCity_Gym_Text_Intro, InkaCity_Gym_Text_Defeat, InkaCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/InkaCity_Gym/scripts.pory"
	msgbox InkaCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


InkaCity_Gym_EventScript_Defeated::
# 9 "data/maps/InkaCity_Gym/scripts.pory"
	setflag FLAG_BADGE06_GET
# 10 "data/maps/InkaCity_Gym/scripts.pory"
	msgbox InkaCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/InkaCity_Gym/scripts.pory"
	release
	return


InkaCity_Gym_EventScript_Guide::
# 15 "data/maps/InkaCity_Gym/scripts.pory"
	msgbox InkaCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


InkaCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/InkaCity_Gym/scripts.pory"
	.string "{PLAYER} received the Frea Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

InkaCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/InkaCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of Frea,\n"
	.string "who uses Ice-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Frea and this empty hall!$"

InkaCity_Gym_Text_Intro::
# 18 "data/maps/InkaCity_Gym/scripts.pory"
	.string "Every crate in Tosa goes through my\n"
	.string "cold store, on time and at the right\l"
	.string "temperature. You're next on my list.$"

InkaCity_Gym_Text_Defeat::
# 22 "data/maps/InkaCity_Gym/scripts.pory"
	.string "Hm. I'll have to note that down.$"

InkaCity_Gym_Text_Post::
# 26 "data/maps/InkaCity_Gym/scripts.pory"
	.string "Keep cool and stay organised. That's all\n"
	.string "there is to it.$"
