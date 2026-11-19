SenokoCity_Gym_MapScripts::
	.byte 0


SenokoCity_Gym_EventScript_Leader::
# 4 "data/maps/SenokoCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_MO, SenokoCity_Gym_Text_Intro, SenokoCity_Gym_Text_Defeat, SenokoCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/SenokoCity_Gym/scripts.pory"
	msgbox SenokoCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


SenokoCity_Gym_EventScript_Defeated::
# 9 "data/maps/SenokoCity_Gym/scripts.pory"
	setflag FLAG_BADGE08_GET
# 10 "data/maps/SenokoCity_Gym/scripts.pory"
	msgbox SenokoCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/SenokoCity_Gym/scripts.pory"
	release
	return


SenokoCity_Gym_EventScript_Guide::
# 15 "data/maps/SenokoCity_Gym/scripts.pory"
	msgbox SenokoCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


SenokoCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/SenokoCity_Gym/scripts.pory"
	.string "{PLAYER} received the Mo Gym Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

SenokoCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/SenokoCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of Mo,\n"
	.string "who uses Electric-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Mo and this empty hall!$"

SenokoCity_Gym_Text_Intro::
# 18 "data/maps/SenokoCity_Gym/scripts.pory"
	.string "I keep the lights on across the whole\n"
	.string "of Tosa. Let's see if you can handle the\l"
	.string "full voltage!$"

SenokoCity_Gym_Text_Defeat::
# 22 "data/maps/SenokoCity_Gym/scripts.pory"
	.string "Wahahah! You've short-circuited me!$"

SenokoCity_Gym_Text_Post::
# 26 "data/maps/SenokoCity_Gym/scripts.pory"
	.string "Every turbine on the hill turns a little\n"
	.string "faster when a good battle's going on.$"
