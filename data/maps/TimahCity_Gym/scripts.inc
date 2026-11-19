TimahCity_Gym_MapScripts::
	.byte 0


TimahCity_Gym_EventScript_Leader::
# 4 "data/maps/TimahCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_HANA, TimahCity_Gym_Text_Intro, TimahCity_Gym_Text_Defeat, TimahCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/TimahCity_Gym/scripts.pory"
	msgbox TimahCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


TimahCity_Gym_EventScript_Defeated::
# 9 "data/maps/TimahCity_Gym/scripts.pory"
	setflag FLAG_BADGE01_GET
# 10 "data/maps/TimahCity_Gym/scripts.pory"
	msgbox TimahCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/TimahCity_Gym/scripts.pory"
	release
	return


TimahCity_Gym_EventScript_Guide::
# 15 "data/maps/TimahCity_Gym/scripts.pory"
	msgbox TimahCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


TimahCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/TimahCity_Gym/scripts.pory"
	.string "{PLAYER} received the Hana Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

TimahCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/TimahCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of Hana,\n"
	.string "who uses Grass-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Hana and this empty hall!$"

TimahCity_Gym_Text_Intro::
# 18 "data/maps/TimahCity_Gym/scripts.pory"
	.string "Welcome to my garden. My orchids bloom\n"
	.string "nowhere else in the world, and neither\l"
	.string "does my battling style!$"

TimahCity_Gym_Text_Defeat::
# 22 "data/maps/TimahCity_Gym/scripts.pory"
	.string "Oh my… you pruned my team right back.$"

TimahCity_Gym_Text_Post::
# 26 "data/maps/TimahCity_Gym/scripts.pory"
	.string "Treat every living thing as gently as an\n"
	.string "orchid and it will grow strong for you.$"
