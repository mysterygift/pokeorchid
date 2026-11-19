FaberTown_Gym_MapScripts::
	.byte 0


FaberTown_Gym_EventScript_Leader::
# 4 "data/maps/FaberTown_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_MERU, FaberTown_Gym_Text_Intro, FaberTown_Gym_Text_Defeat, FaberTown_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/FaberTown_Gym/scripts.pory"
	msgbox FaberTown_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


FaberTown_Gym_EventScript_Defeated::
# 9 "data/maps/FaberTown_Gym/scripts.pory"
	setflag FLAG_BADGE04_GET
# 10 "data/maps/FaberTown_Gym/scripts.pory"
	msgbox FaberTown_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/FaberTown_Gym/scripts.pory"
	release
	return


FaberTown_Gym_EventScript_Guide::
# 15 "data/maps/FaberTown_Gym/scripts.pory"
	msgbox FaberTown_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


FaberTown_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/FaberTown_Gym/scripts.pory"
	.string "{PLAYER} received the Meru Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

FaberTown_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/FaberTown_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of Meru,\n"
	.string "who uses Fighting-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Meru and this empty hall!$"

FaberTown_Gym_Text_Intro::
# 18 "data/maps/FaberTown_Gym/scripts.pory"
	.string "I train alone in the mountains against\n"
	.string "wild Rock Pokémon. You climbed all the\l"
	.string "way up here? Then show me your\l"
	.string "strength!$"

FaberTown_Gym_Text_Defeat::
# 22 "data/maps/FaberTown_Gym/scripts.pory"
	.string "Hah! You hit harder than a rockslide!$"

FaberTown_Gym_Text_Post::
# 26 "data/maps/FaberTown_Gym/scripts.pory"
	.string "Strength comes from the climb, not the\n"
	.string "summit.$"
