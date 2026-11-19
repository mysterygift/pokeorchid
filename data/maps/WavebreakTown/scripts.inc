WavebreakTown_MapScripts::
# 3 "data/maps/WavebreakTown/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, WavebreakTown_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

WavebreakTown_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 4 "data/maps/WavebreakTown/scripts.pory"
	goto_if_unset FLAG_SYS_GAME_CLEAR, WavebreakTown_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
	return

WavebreakTown_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 5 "data/maps/WavebreakTown/scripts.pory"
	setflag FLAG_TEMP_1
	return


WavebreakTown_EventScript_TownSign::
# 11 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


WavebreakTown_EventScript_Npc1::
# 15 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_Npc2::
# 19 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_Npc3::
# 23 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_Npc4::
# 27 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_Npc5::
# 31 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_Npc6::
# 35 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc6_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_Npc7::
# 39 "data/maps/WavebreakTown/scripts.pory"
	msgbox WavebreakTown_EventScript_Npc7_Text_0, MSGBOX_NPC
	return


WavebreakTown_EventScript_TownSign_Text_0:
# 11 "data/maps/WavebreakTown/scripts.pory"
	.string "Wavebreak Town\n"
	.string "“Tosa's first harbour.”$"

WavebreakTown_EventScript_Npc1_Text_0:
# 15 "data/maps/WavebreakTown/scripts.pory"
	.string "Wavebreak was Tosa's first port, you\n"
	.string "know. Then Tosa Port opened and the\l"
	.string "ships stopped coming.$"

WavebreakTown_EventScript_Npc2_Text_0:
# 19 "data/maps/WavebreakTown/scripts.pory"
	.string "Nobody's left to scare the Pokémon off,\n"
	.string "so the fishing's never been better.$"

WavebreakTown_EventScript_Npc3_Text_0:
# 23 "data/maps/WavebreakTown/scripts.pory"
	.string "My husband worked the docks here for\n"
	.string "forty years. Now the only thing that\l"
	.string "washes in is seaweed.$"

WavebreakTown_EventScript_Npc4_Text_0:
# 27 "data/maps/WavebreakTown/scripts.pory"
	.string "Smugglers love a quiet harbour. Just\n"
	.string "saying.$"

WavebreakTown_EventScript_Npc5_Text_0:
# 31 "data/maps/WavebreakTown/scripts.pory"
	.string "The fish bite best under these trees at\n"
	.string "the north end. Shade on the water, see?$"

WavebreakTown_EventScript_Npc6_Text_0:
# 35 "data/maps/WavebreakTown/scripts.pory"
	.string "Left my spare rods by the Centre. If\n"
	.string "they're gone, so's my luck.$"

WavebreakTown_EventScript_Npc7_Text_0:
# 39 "data/maps/WavebreakTown/scripts.pory"
	.string "That old sailor's boat goes places my\n"
	.string "line never reaches. Wonder what bites\l"
	.string "out there.$"
