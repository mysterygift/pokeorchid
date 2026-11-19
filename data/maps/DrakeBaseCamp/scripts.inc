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


DrakeBaseCamp_EventScript_TiksiGuardianRegolisShrine::
# 35 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_EventScript_TiksiGuardianRegolisShrine_Text_0, MSGBOX_NPC
	return


DrakeBaseCamp_EventScript_TiksiGuardianMtDrakeSummit::
# 39 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_EventScript_TiksiGuardianMtDrakeSummit_Text_0, MSGBOX_NPC
	return


DrakeBaseCamp_EventScript_TiksiGuardianFerrumShrine::
# 43 "data/maps/DrakeBaseCamp/scripts.pory"
	msgbox DrakeBaseCamp_EventScript_TiksiGuardianFerrumShrine_Text_0, MSGBOX_NPC
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

DrakeBaseCamp_EventScript_TiksiGuardianRegolisShrine_Text_0:
# 35 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "This path leads to Regolis Shrine, in\n"
	.string "the heart of the desert. The rock giant\l"
	.string "sleeps there once more.\p"
	.string "I am its guardian. Go if you must.$"

DrakeBaseCamp_EventScript_TiksiGuardianMtDrakeSummit_Text_0:
# 39 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "Beyond here, the old trail climbs to the\n"
	.string "peak of Mt. Drake. They say the dragon\l"
	.string "giant waits at the top.\p"
	.string "I guard the way. Be ready.$"

DrakeBaseCamp_EventScript_TiksiGuardianFerrumShrine_Text_0:
# 43 "data/maps/DrakeBaseCamp/scripts.pory"
	.string "Ferrum Shrine lies at the core of Mt.\n"
	.string "Drake. The steel giant has returned to\l"
	.string "it.\p"
	.string "I am sworn to guard this door.$"
