ChanguCity_MapScripts::
# 2 "data/maps/ChanguCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, ChanguCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

ChanguCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/ChanguCity/scripts.pory"
	setflag FLAG_VISITED_SLATEPORT_CITY
	return


ChanguCity_EventScript_TownSign::
# 8 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


ChanguCity_EventScript_GymSign::
# 12 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


ChanguCity_EventScript_Sign3::
# 16 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_Sign3_Text_0, MSGBOX_SIGN
	return


ChanguCity_EventScript_Npc1::
# 20 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


ChanguCity_EventScript_Npc2::
# 24 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


ChanguCity_EventScript_Npc3::
# 28 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


ChanguCity_EventScript_Npc4::
# 32 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


ChanguCity_EventScript_Npc5::
# 36 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


ChanguCity_EventScript_CafeSign::
# 40 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_CafeSign_Text_0, MSGBOX_SIGN
	return


ChanguCity_EventScript_CafeTerracePatron::
# 44 "data/maps/ChanguCity/scripts.pory"
	msgbox ChanguCity_EventScript_CafeTerracePatron_Text_0, MSGBOX_NPC
	return


ChanguCity_EventScript_TownSign_Text_0:
# 8 "data/maps/ChanguCity/scripts.pory"
	.string "Changu City\n"
	.string "“Gateway to the Tosa region.”$"

ChanguCity_EventScript_GymSign_Text_0:
# 12 "data/maps/ChanguCity/scripts.pory"
	.string "Changu City Pokémon Gym\n"
	.string "Leader: Larry. Normal-type Pokémon.$"

ChanguCity_EventScript_Sign3_Text_0:
# 16 "data/maps/ChanguCity/scripts.pory"
	.string "CHANGU BUSINESS PARK\n"
	.string "Offices to let.$"

ChanguCity_EventScript_Npc1_Text_0:
# 20 "data/maps/ChanguCity/scripts.pory"
	.string "Synergise! Innovate! Profit!\p"
	.string "Sorry, force of habit. I fly in every\n"
	.string "Monday for meetings.$"

ChanguCity_EventScript_Npc2_Text_0:
# 24 "data/maps/ChanguCity/scripts.pory"
	.string "The airport's just up Route 306. They\n"
	.string "call Changu the gateway to Tosa. So far\l"
	.string "it's mostly office blocks.$"

ChanguCity_EventScript_Npc3_Text_0:
# 28 "data/maps/ChanguCity/scripts.pory"
	.string "Our Gym Leader Larry was sent over from\n"
	.string "Paldea by their Champion. He seems…\l"
	.string "tired. Very, very tired.$"

ChanguCity_EventScript_Npc4_Text_0:
# 32 "data/maps/ChanguCity/scripts.pory"
	.string "I saw Larry at the hawker stall eating\n"
	.string "the same set lunch as yesterday. And\l"
	.string "the day before.$"

ChanguCity_EventScript_Npc5_Text_0:
# 36 "data/maps/ChanguCity/scripts.pory"
	.string "Customs has tightened up. Too many\n"
	.string "Pokémon have been coming in without\l"
	.string "import permits lately.$"

ChanguCity_EventScript_CafeSign_Text_0:
# 40 "data/maps/ChanguCity/scripts.pory"
	.string "BATTLE CAFÉ\n"
	.string "Kopi, kaya toast and a seat between\l"
	.string "flights.$"

ChanguCity_EventScript_CafeTerracePatron_Text_0:
# 44 "data/maps/ChanguCity/scripts.pory"
	.string "Best seat in Changu. You can watch the\n"
	.string "planes come in over the rooftops.$"
