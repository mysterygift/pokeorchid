# 1 "data/maps/TimahCity/scripts.pory"

# 2 "data/maps/TimahCity/scripts.pory"
TimahCity_MapScripts::
# 3 "data/maps/TimahCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TimahCity_OnTransition
# 4 "data/maps/TimahCity/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TimahCity_OnFrame
# 5 "data/maps/TimahCity/scripts.pory"
	.byte 0
# 6 "data/maps/TimahCity/scripts.pory"

# 7 "data/maps/TimahCity/scripts.pory"
@ Orchid: Professor Palm calls once the first badge is won (VAR_ORCHID_RESEARCH 0 locked, 1 call pending,
# 8 "data/maps/TimahCity/scripts.pory"
@ 2 research unlocked - include/research.h). Arming it here too covers saves that already have the badge.
# 9 "data/maps/TimahCity/scripts.pory"
TimahCity_OnTransition:
# 10 "data/maps/TimahCity/scripts.pory"
	setflag FLAG_VISITED_PETALBURG_CITY
# 11 "data/maps/TimahCity/scripts.pory"
	goto_if_unset FLAG_BADGE01_GET, TimahCity_OnTransition_End
# 12 "data/maps/TimahCity/scripts.pory"
	goto_if_ne VAR_ORCHID_RESEARCH, 0, TimahCity_OnTransition_End
# 13 "data/maps/TimahCity/scripts.pory"
	setvar VAR_ORCHID_RESEARCH, 1
# 14 "data/maps/TimahCity/scripts.pory"
TimahCity_OnTransition_End:
# 15 "data/maps/TimahCity/scripts.pory"
	end
# 16 "data/maps/TimahCity/scripts.pory"

# 17 "data/maps/TimahCity/scripts.pory"
TimahCity_OnFrame:
# 18 "data/maps/TimahCity/scripts.pory"
	map_script_2 VAR_ORCHID_RESEARCH, 1, TimahCity_EventScript_PalmCall
# 19 "data/maps/TimahCity/scripts.pory"
	.2byte 0

TimahCity_EventScript_PalmCall::
# 23 "data/maps/TimahCity/scripts.pory"
	lockall
# 24 "data/maps/TimahCity/scripts.pory"
	playse SE_POKENAV_CALL
# 25 "data/maps/TimahCity/scripts.pory"
	waitse
# 26 "data/maps/TimahCity/scripts.pory"
	pokenavcall TimahCity_Text_PalmCall
# 27 "data/maps/TimahCity/scripts.pory"
	waitmessage
# 28 "data/maps/TimahCity/scripts.pory"
	closemessage
# 29 "data/maps/TimahCity/scripts.pory"
	setvar VAR_ORCHID_RESEARCH, 2
# 30 "data/maps/TimahCity/scripts.pory"
	questmenu QUEST_MENU_BUZZ, 0
# 31 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_PalmCall_Text_0
# 32 "data/maps/TimahCity/scripts.pory"
	releaseall
	return


TimahCity_EventScript_TownSign::
# 40 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_TownSign_Text_0, MSGBOX_SIGN
	return


TimahCity_EventScript_GymSign::
# 44 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_GymSign_Text_0, MSGBOX_SIGN
	return


TimahCity_EventScript_Npc1::
# 48 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc1_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc2::
# 52 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc2_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc3::
# 56 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc3_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc4::
# 60 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc4_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_Npc5::
# 64 "data/maps/TimahCity/scripts.pory"
	msgbox TimahCity_EventScript_Npc5_Text_0, MSGBOX_NPC
	return


TimahCity_EventScript_PalmCall_Text_0:
# 31 "data/maps/TimahCity/scripts.pory"
	.string "Bzzt! Palm's Research is now in the\n"
	.string "QUESTS app!$"

TimahCity_EventScript_TownSign_Text_0:
# 40 "data/maps/TimahCity/scripts.pory"
	.string "Timah City\n"
	.string "“The green heart of the Tosa Reserve.”$"

TimahCity_EventScript_GymSign_Text_0:
# 44 "data/maps/TimahCity/scripts.pory"
	.string "Timah City Pokémon Gym\n"
	.string "Leader: Hana. Grass-type Pokémon.$"

TimahCity_EventScript_Npc1_Text_0:
# 48 "data/maps/TimahCity/scripts.pory"
	.string "Hana grows orchids in her garden that\n"
	.string "bloom nowhere else in the world. She\l"
	.string "guards them better than her Gym Badge!$"

TimahCity_EventScript_Npc2_Text_0:
# 52 "data/maps/TimahCity/scripts.pory"
	.string "Timah sits right in the middle of the\n"
	.string "Tosa Reserve. Stick to the paths. The\l"
	.string "Rangers are watching for poachers.$"

TimahCity_EventScript_Npc3_Text_0:
# 56 "data/maps/TimahCity/scripts.pory"
	.string "It rains here every afternoon, like\n"
	.string "clockwork. Bring an umbrella. Or a Lotad.$"

TimahCity_EventScript_Npc4_Text_0:
# 60 "data/maps/TimahCity/scripts.pory"
	.string "This city grew up around the old rubber\n"
	.string "trees on the hill. Now look at it: trains,\l"
	.string "Pokémon Centres…$"

TimahCity_EventScript_Npc5_Text_0:
# 64 "data/maps/TimahCity/scripts.pory"
	.string "There are Pokémon up in the canopy\n"
	.string "that never come down to the ground.\l"
	.string "I've been waiting all week!$"

TimahCity_Text_PalmCall::
# 35 "data/maps/TimahCity/scripts.pory"
	.string "PALM: {PLAYER}! Professor\n"
	.string "Palm here. Word travels fast:\l"
	.string "you beat Hana! Congratulations!\p"
	.string "Now that you've proven\n"
	.string "yourself, I'd like your help with\l"
	.string "my research.\p"
	.string "Catalogue the Pokémon of each\n"
	.string "habitat, by day and by night.\l"
	.string "Catch each species twice so we\l"
	.string "can record everything about it.\p"
	.string "I've sent my field notes to your\n"
	.string "Rotom Phone. Look for Research\l"
	.string "in the QUESTS app!$"
