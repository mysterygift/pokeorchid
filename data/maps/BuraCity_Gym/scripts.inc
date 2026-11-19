BuraCity_Gym_MapScripts::
	.byte 0


BuraCity_Gym_EventScript_Leader::
# 4 "data/maps/BuraCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_MARIA, BuraCity_Gym_Text_Intro, BuraCity_Gym_Text_Defeat, BuraCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/BuraCity_Gym/scripts.pory"
	msgbox BuraCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


BuraCity_Gym_EventScript_Defeated::
# 9 "data/maps/BuraCity_Gym/scripts.pory"
	setflag FLAG_BADGE07_GET
# 10 "data/maps/BuraCity_Gym/scripts.pory"
	msgbox BuraCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/BuraCity_Gym/scripts.pory"
	release
	return


BuraCity_Gym_EventScript_Guide::
# 15 "data/maps/BuraCity_Gym/scripts.pory"
	msgbox BuraCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


BuraCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/BuraCity_Gym/scripts.pory"
	.string "{PLAYER} received the Maria Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

BuraCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/BuraCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of\n"
	.string "Maria, who uses Cat-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Maria and this empty hall!$"

BuraCity_Gym_Text_Intro::
# 18 "data/maps/BuraCity_Gym/scripts.pory"
	.string "Oh, a challenger! I only just got back\n"
	.string "from Juran. Don't mind the costumes, my\l"
	.string "darlings love dressing up!$"

BuraCity_Gym_Text_Defeat::
# 22 "data/maps/BuraCity_Gym/scripts.pory"
	.string "My poor kitties! Let's call it a draw and\n"
	.string "go for noodles?$"

BuraCity_Gym_Text_Post::
# 26 "data/maps/BuraCity_Gym/scripts.pory"
	.string "Win some, lose some. That's what I\n"
	.string "always say at the tables!$"
