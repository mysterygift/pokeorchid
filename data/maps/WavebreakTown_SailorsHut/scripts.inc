WavebreakTown_SailorsHut_MapScripts::
# 3 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, WavebreakTown_SailorsHut_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

WavebreakTown_SailorsHut_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 4 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, WavebreakTown_SailorsHut_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
	return

WavebreakTown_SailorsHut_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 5 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	setflag FLAG_TEMP_1
	return


WavebreakTown_SailorsHut_EventScript_Son::
# 11 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	lock
# 12 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	faceplayer
# 13 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, WavebreakTown_SailorsHut_EventScript_Son_2
# 16 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	msgbox WavebreakTown_SailorsHut_EventScript_Son_Text_1
WavebreakTown_SailorsHut_EventScript_Son_1:
# 18 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	release
	return

WavebreakTown_SailorsHut_EventScript_Son_2:
# 14 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	msgbox WavebreakTown_SailorsHut_EventScript_Son_Text_0
	goto WavebreakTown_SailorsHut_EventScript_Son_1


WavebreakTown_SailorsHut_EventScript_Son_Text_0:
# 14 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	.string "Dad's down at the dock with the boat. He\n"
	.string "says you know the secret words now!$"

WavebreakTown_SailorsHut_EventScript_Son_Text_1:
# 16 "data/maps/WavebreakTown_SailorsHut/scripts.pory"
	.string "My dad sailed to islands nobody's ever\n"
	.string "heard of. He says they only open up if\l"
	.string "you know the secret words.$"
