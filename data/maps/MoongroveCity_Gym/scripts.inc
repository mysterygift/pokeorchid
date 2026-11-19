MoongroveCity_Gym_MapScripts::
	.byte 0


MoongroveCity_Gym_EventScript_Leader::
# 4 "data/maps/MoongroveCity_Gym/scripts.pory"
	trainerbattle_single TRAINER_LEADER_TORK, MoongroveCity_Gym_Text_Intro, MoongroveCity_Gym_Text_Defeat, MoongroveCity_Gym_EventScript_Defeated, NO_MUSIC
# 5 "data/maps/MoongroveCity_Gym/scripts.pory"
	msgbox MoongroveCity_Gym_Text_Post, MSGBOX_AUTOCLOSE
	return


MoongroveCity_Gym_EventScript_Defeated::
# 9 "data/maps/MoongroveCity_Gym/scripts.pory"
	setflag FLAG_BADGE05_GET
# 10 "data/maps/MoongroveCity_Gym/scripts.pory"
	msgbox MoongroveCity_Gym_EventScript_Defeated_Text_0
# 11 "data/maps/MoongroveCity_Gym/scripts.pory"
	release
	return


MoongroveCity_Gym_EventScript_Guide::
# 15 "data/maps/MoongroveCity_Gym/scripts.pory"
	msgbox MoongroveCity_Gym_EventScript_Guide_Text_0, MSGBOX_NPC
	return


MoongroveCity_Gym_EventScript_Defeated_Text_0:
# 10 "data/maps/MoongroveCity_Gym/scripts.pory"
	.string "{PLAYER} received the Tork Gym\n"
	.string "Badge!\p"
	.string "(Placeholder Gym: the badge flag is\n"
	.string "set.)$"

MoongroveCity_Gym_EventScript_Guide_Text_0:
# 15 "data/maps/MoongroveCity_Gym/scripts.pory"
	.string "Hey, Challenger! This is the Gym of Tork,\n"
	.string "who uses Ground-type Pokémon.\p"
	.string "The Gym's still being fitted out. For now\n"
	.string "it's just you, Tork and this empty hall!$"

MoongroveCity_Gym_Text_Intro::
# 18 "data/maps/MoongroveCity_Gym/scripts.pory"
	.string "I was up before dawn hunting catfish in\n"
	.string "the mudflats. You'll find my Pokémon\l"
	.string "just as slippery!$"

MoongroveCity_Gym_Text_Defeat::
# 22 "data/maps/MoongroveCity_Gym/scripts.pory"
	.string "Well, I'll be. The big one got away again.$"

MoongroveCity_Gym_Text_Post::
# 26 "data/maps/MoongroveCity_Gym/scripts.pory"
	.string "Patience, that's the secret. In fishing\n"
	.string "and in battle.$"
