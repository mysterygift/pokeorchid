ChallengerGate_MapScripts::
# 2 "data/maps/ChallengerGate/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, ChallengerGate_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

ChallengerGate_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/ChallengerGate/scripts.pory"
	setflag FLAG_VISITED_EVER_GRANDE_CITY
	return


ChallengerGate_EventScript_TownSign::
# 8 "data/maps/ChallengerGate/scripts.pory"
	msgbox ChallengerGate_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


ChallengerGate_EventScript_Npc1::
# 12 "data/maps/ChallengerGate/scripts.pory"
	msgbox ChallengerGate_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


ChallengerGate_EventScript_Npc2::
# 16 "data/maps/ChallengerGate/scripts.pory"
	msgbox ChallengerGate_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


ChallengerGate_EventScript_Npc3::
# 20 "data/maps/ChallengerGate/scripts.pory"
	msgbox ChallengerGate_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


ChallengerGate_EventScript_Npc4::
# 24 "data/maps/ChallengerGate/scripts.pory"
	msgbox ChallengerGate_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


ChallengerGate_EventScript_TownSign_Text_0:
# 8 "data/maps/ChallengerGate/scripts.pory"
	.string "Challenger Gate\n"
	.string "“The last stop before the Pokémon\l"
	.string "League.”$"

ChallengerGate_EventScript_Npc1_Text_0:
# 12 "data/maps/ChallengerGate/scripts.pory"
	.string "Only Trainers with every Badge in Tosa\n"
	.string "are allowed onto Challenger's Trail.$"

ChallengerGate_EventScript_Npc2_Text_0:
# 16 "data/maps/ChallengerGate/scripts.pory"
	.string "The Trail climbs right up the mountain\n"
	.string "to the Pokémon League. Plenty turn\l"
	.string "back.$"

ChallengerGate_EventScript_Npc3_Text_0:
# 20 "data/maps/ChallengerGate/scripts.pory"
	.string "Every Badge in Tosa, and I still got lost\n"
	.string "in that cave. Bring Repels.$"

ChallengerGate_EventScript_Npc4_Text_0:
# 24 "data/maps/ChallengerGate/scripts.pory"
	.string "One day I'll walk the Trail. Today I'm\n"
	.string "just here for the café.$"
