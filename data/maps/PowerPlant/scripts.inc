PowerPlant_MapScripts::
	.byte 0


PowerPlant_EventScript_TownSign::
# 5 "data/maps/PowerPlant/scripts.pory"
	msgbox PowerPlant_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


PowerPlant_EventScript_Sign0::
# 9 "data/maps/PowerPlant/scripts.pory"
	msgbox PowerPlant_EventScript_Sign0_Text_0, MSGBOX_SIGN
	return


PowerPlant_EventScript_Npc1::
# 13 "data/maps/PowerPlant/scripts.pory"
	msgbox PowerPlant_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


PowerPlant_EventScript_Npc2::
# 17 "data/maps/PowerPlant/scripts.pory"
	msgbox PowerPlant_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


PowerPlant_EventScript_TownSign_Text_0:
# 5 "data/maps/PowerPlant/scripts.pory"
	.string "Power Plant\n"
	.string "“Senoko City Wind Power Plant.”$"

PowerPlant_EventScript_Sign0_Text_0:
# 9 "data/maps/PowerPlant/scripts.pory"
	.string "SENOKO WIND POWER PLANT\n"
	.string "Control building. Staff only.$"

PowerPlant_EventScript_Npc1_Text_0:
# 13 "data/maps/PowerPlant/scripts.pory"
	.string "The turbines feed straight into Mo's\n"
	.string "grid. When the wind drops, his Electric\l"
	.string "Pokémon pick up the slack.$"

PowerPlant_EventScript_Npc2_Text_0:
# 17 "data/maps/PowerPlant/scripts.pory"
	.string "Voltorb keep rolling in from the hills.\n"
	.string "We think the hum of the generators\l"
	.string "attracts them.$"
