# 1 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"

# 2 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
TosaPort_BrendansHouse_1F_MapScripts::
# 3 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TosaPort_BrendansHouse_1F_OnFrame
# 4 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.byte 0
# 5 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"

# 6 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
@ ON_WARP_INTO_MAP_TABLE uses RunScriptImmediately(), which stops at the first cmd that returns TRUE
# 7 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
@ (e.g. lockall, waitmovement). That leaves the map stuck on a black screen. ON_FRAME_TABLE uses the
# 8 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
@ normal field script runner after the map has faded in.
# 9 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
@
# 10 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
@ VAR_TEMP_E is 0 on map load; set to 1 before running or suppressing so this only arms once per visit.
# 11 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
TosaPort_BrendansHouse_1F_OnFrame:
# 12 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	map_script_2 VAR_TEMP_E, 0, TosaPort_BrendansHouse_1F_EventScript_OnFrameTryRival
# 13 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.2byte 0
# 14 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"

# 15 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
TosaPort_BrendansHouse_1F_EventScript_OnFrameTryRival::
# 16 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	goto_if_set FLAG_HIDE_TOSA_GATEWAY_RIVAL, TosaPort_BrendansHouse_1F_EventScript_OnFrameTryRival_Suppress
# 17 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	setvar VAR_TEMP_E, 1
# 18 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	call TosaGateway_RivalEncounter
# 19 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	end
# 20 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"

# 21 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
TosaPort_BrendansHouse_1F_EventScript_OnFrameTryRival_Suppress::
# 22 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	setvar VAR_TEMP_E, 1
# 23 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	end

TosaGateway_RivalEncounter::
# 27 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lockall
# 28 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	applymovement LOCALID_RIVAL, TosaGateway_RivalEncounter_Movement_0
# 29 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	playse SE_PIN
# 30 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	waitmovement 0
# 31 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RivalEncounter_Text_0
# 32 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RivalEncounter_Text_1, MSGBOX_YESNO
# 33 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	compare VAR_RESULT, 1
	goto_if_ne TosaGateway_RivalEncounter_2
# 36 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RivalEncounter_Text_3
TosaGateway_RivalEncounter_1:
# 38 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	delay 24
# 39 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RivalEncounter_Text_4
# 40 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RivalEncounter_Text_5
# 41 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	trainerbattle_single TRAINER_HARU_GATEWAY, TosaGateway_Haru_Intro, TosaGateway_Haru_Defeat, TosaGateway_Haru_Defeated
	return

TosaGateway_RivalEncounter_2:
# 34 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RivalEncounter_Text_2, MSGBOX_NPC
	goto TosaGateway_RivalEncounter_1


TosaGateway_Haru_Defeated::
# 46 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lockall
# 47 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_Haru_Defeated_Text_0, MSGBOX_NPC
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	applymovement LOCALID_RIVAL, TosaGateway_Haru_Defeated_Movement_0
# 49 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	waitmovement 0
# 50 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	playse SE_EXIT
# 51 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	removeobject LOCALID_RIVAL, MAP_TOSA_PORT_BRENDANS_HOUSE_1F
# 52 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	setflag FLAG_HIDE_TOSA_GATEWAY_RIVAL
# 53 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	setvar VAR_TOSA_PORT_STATE, 3
# 54 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	releaseall
	return


TosaGateway_Receptionist::
# 67 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lock
# 68 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	faceplayer
# 69 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_Receptionist_Text_0, MSGBOX_NPC
# 70 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	release
	end


TosaGateway_RailwayGuard::
# 75 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lock
# 76 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	faceplayer
# 77 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_RailwayGuard_Text_0, MSGBOX_NPC
# 78 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	release
	end


TosaGateway_Gentleman::
# 83 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lock
# 84 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	faceplayer
# 85 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_Gentleman_Text_0, MSGBOX_NPC
# 86 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	release
	end


TosaGateway_Mum::
# 91 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lock
# 92 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	faceplayer
# 93 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_Mum_Text_0, MSGBOX_NPC
# 94 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	release
	end


TosaGateway_Kid::
# 99 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	lock
# 100 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	faceplayer
# 101 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	msgbox TosaGateway_Kid_Text_0, MSGBOX_NPC
# 102 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	release
	end


# 28 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
TosaGateway_RivalEncounter_Movement_0:
# 28 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	emote_exclamation_mark
# 28 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_left
# 28 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_down
# 28 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_down
	step_end

# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
TosaGateway_Haru_Defeated_Movement_0:
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_left
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_left
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
# 48 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	walk_up
	step_end

TosaGateway_RivalEncounter_Text_0:
# 31 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Hey pal. I hope you aren't looking to\n"
	.string "catch the underground, the trains are\l"
	.string "closed until further notice.$"

TosaGateway_RivalEncounter_Text_1:
# 32 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Are you heading to Telok as well?$"

TosaGateway_RivalEncounter_Text_2:
# 34 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Well I hope you like the look of this\n"
	.string "waiting room...$"

TosaGateway_RivalEncounter_Text_3:
# 36 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Oh cool! Are you off to visit Professor\n"
	.string "Palm? I remember studying his books on\l"
	.string "Pokémon Migration in University...$"

TosaGateway_RivalEncounter_Text_4:
# 39 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Haru: I'm Haru by the way, it's a\n"
	.string "pleasure to meet you. I'm travelling the\l"
	.string "Tosa region in search of the ultimate\l"
	.string "Pokémon.$"

TosaGateway_RivalEncounter_Text_5:
# 40 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Haru: What's the ultimate Pokémon?\p"
	.string "$"

TosaGateway_Haru_Defeated_Text_0:
# 47 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Haru: I'm sure I'll see you around,\n"
	.string "{PLAYER}. Safe travels!$"

TosaGateway_Receptionist_Text_0:
# 69 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "We apologise, but the train station is\n"
	.string "currently closed for maintenance.$"

TosaGateway_RailwayGuard_Text_0:
# 77 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "The train station's closed. My\n"
	.string "supervisor mentioned something about\l"
	.string "Koffing in the tunnels.$"

TosaGateway_Gentleman_Text_0:
# 85 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "I've re-read this newspaper five times.\n"
	.string "Maybe I should've bought myself a\l"
	.string "Rotom Phone after all...$"

TosaGateway_Mum_Text_0:
# 93 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "We're resting up before going for a walk\n"
	.string "in the reserve.$"

TosaGateway_Kid_Text_0:
# 101 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "I can't wait to catch a Mareep in the\n"
	.string "reserve! They're so fluffy!$"

TosaGateway_Haru_Intro::
# 58 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "Let's find out!$"

TosaGateway_Haru_Defeat::
# 62 "data/maps/TosaPort_BrendansHouse_1F/scripts.pory"
	.string "You floored me!$"
