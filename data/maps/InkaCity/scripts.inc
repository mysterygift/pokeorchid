InkaCity_MapScripts::
# 2 "data/maps/InkaCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, InkaCity_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

InkaCity_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 3 "data/maps/InkaCity/scripts.pory"
	setflag FLAG_VISITED_RUSTBORO_CITY
	return


InkaCity_EventScript_TownSign::
# 8 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


InkaCity_EventScript_GymSign::
# 12 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


InkaCity_EventScript_Sign3::
# 16 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Sign3_Text_0, MSGBOX_SIGN
	return


InkaCity_EventScript_Sign4::
# 20 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Sign4_Text_0, MSGBOX_SIGN
	return


InkaCity_EventScript_Npc1::
# 24 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


InkaCity_EventScript_Npc2::
# 28 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


InkaCity_EventScript_Npc3::
# 32 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


InkaCity_EventScript_Npc4::
# 36 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


InkaCity_EventScript_Npc5::
# 40 "data/maps/InkaCity/scripts.pory"
	msgbox InkaCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


InkaCity_EventScript_TownSign_Text_0:
# 8 "data/maps/InkaCity/scripts.pory"
	.string "Inka City\n"
	.string "“Tosa's logistics hub.”$"

InkaCity_EventScript_GymSign_Text_0:
# 12 "data/maps/InkaCity/scripts.pory"
	.string "Inka City Pokémon Gym\n"
	.string "Leader: Frea. Ice-type Pokémon.$"

InkaCity_EventScript_Sign3_Text_0:
# 16 "data/maps/InkaCity/scripts.pory"
	.string "INKA COLD DISTRIBUTION CENTRE\n"
	.string "Managed by Frea. Staff only.$"

InkaCity_EventScript_Sign4_Text_0:
# 20 "data/maps/InkaCity/scripts.pory"
	.string "MARLIN CO. SHIPPING\n"
	.string "Authorised personnel only.$"

InkaCity_EventScript_Npc1_Text_0:
# 24 "data/maps/InkaCity/scripts.pory"
	.string "Every crate of imported food in Tosa\n"
	.string "passes through Inka. Frea makes sure\l"
	.string "it's all kept cold and on time.$"

InkaCity_EventScript_Npc2_Text_0:
# 28 "data/maps/InkaCity/scripts.pory"
	.string "Marlin Co.? Shipping company. Keeps odd\n"
	.string "hours.\p"
	.string "Their trucks come and go at night with\n"
	.string "the lights off.$"

InkaCity_EventScript_Npc3_Text_0:
# 32 "data/maps/InkaCity/scripts.pory"
	.string "Frea runs the cold store and the Gym.\n"
	.string "I've never once seen her without a\l"
	.string "clipboard.$"

InkaCity_EventScript_Npc4_Text_0:
# 36 "data/maps/InkaCity/scripts.pory"
	.string "The warehouses never sleep. Forklifts\n"
	.string "at three in the morning, Ice types\l"
	.string "cooling the containers… It's noisy!$"

InkaCity_EventScript_Npc5_Text_0:
# 40 "data/maps/InkaCity/scripts.pory"
	.string "I tried to peek inside Marlin Co. A man in\n"
	.string "a blue bandana told me to scram!$"
