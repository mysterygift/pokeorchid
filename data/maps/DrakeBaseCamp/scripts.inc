# 1 "data/maps/DrakeBaseCamp/scripts.pory"

# 2 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_MapScripts::
# 3 "data/maps/DrakeBaseCamp/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, DrakeBaseCamp_OnTransition
# 4 "data/maps/DrakeBaseCamp/scripts.pory"
	.byte 0
# 5 "data/maps/DrakeBaseCamp/scripts.pory"

# 6 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_OnTransition:
# 7 "data/maps/DrakeBaseCamp/scripts.pory"
	setflag FLAG_VISITED_DRAKE_BASE_CAMP
# 8 "data/maps/DrakeBaseCamp/scripts.pory"
	end
# 9 "data/maps/DrakeBaseCamp/scripts.pory"

# 10 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_EventScript_Sign0::
# 11 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_Text_Sign0, MSGBOX_SIGN
# 12 "data/maps/DrakeBaseCamp/scripts.pory"
	end
# 13 "data/maps/DrakeBaseCamp/scripts.pory"

# 14 "data/maps/DrakeBaseCamp/scripts.pory"
DrakeBaseCamp_Text_Sign0:
# 15 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "DRAKE BASE CAMP\n"
# 16 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "The last stop before MT. DRAKE.$"

DrakeBaseCamp_EventScript_TiksiNpc1::
# 23 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_EventScript_TiksiNpc1_Text_0, MSGBOX_NPC
	return


DrakeBaseCamp_EventScript_TiksiNpc2::
# 27 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_EventScript_TiksiNpc2_Text_0, MSGBOX_NPC
	return


DrakeBaseCamp_EventScript_TiksiNpc3::
# 31 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_EventScript_TiksiNpc3_Text_0, MSGBOX_NPC
	return


DrakeBaseCamp_EventScript_TiksiNpc1_Text_0:
# 23 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "The peak of Mt. Drake is said to be home\n"
	.string "to an ancient dragon Pokémon. Nobody's\l"
	.string "climbed high enough to check.$"

DrakeBaseCamp_EventScript_TiksiNpc2_Text_0:
# 27 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "The old stories say this mountain was\n"
	.string "carved by beams of light from the maw\l"
	.string "of an ancient Pokémon.$"

DrakeBaseCamp_EventScript_TiksiNpc3_Text_0:
# 31 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "Some strangers in blue came through\n"
	.string "last week, heading up the mountain.\l"
	.string "Didn't say hello.$"
