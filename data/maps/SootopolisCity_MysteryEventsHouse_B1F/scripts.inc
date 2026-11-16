# 1 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 2 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_MapScripts::
# 3 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SootopolisCity_MysteryEventsHouse_B1F_OnTransition
# 4 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SootopolisCity_MysteryEventsHouse_B1F_OnFrame
# 5 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	.byte 0
# 6 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 7 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_OnTransition:
# 8 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special SetEReaderTrainerGfxId
# 9 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	end
# 10 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 11 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_OnFrame:
# 12 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleVisitingTrainer
# 13 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	.2byte 0
# 14 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 15 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleVisitingTrainer::
# 16 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	lockall
# 17 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_MysteryEventsHouse_B1F_Movement_PlayerEnterBasement
# 18 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitmovement 0
# 19 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special CopyEReaderTrainerGreeting
# 20 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	msgbox gStringVar4, MSGBOX_DEFAULT
# 21 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	closemessage
# 22 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	setvar VAR_0x8004, SPECIAL_BATTLE_EREADER
# 23 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	setvar VAR_0x8005, 0
# 24 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special DoSpecialTrainerBattle
# 25 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	call_if_eq VAR_RESULT, B_OUTCOME_DREW, SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleTie
# 26 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleWon
# 27 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	call_if_eq VAR_RESULT, B_OUTCOME_LOST, SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleLost
# 28 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	closemessage
# 29 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special HealPlayerParty
# 30 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_MysteryEventsHouse_B1F_Movement_PlayerExitBasement
# 31 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitmovement 0
# 32 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special LoadPlayerParty
# 33 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	setvar VAR_TEMP_1, 1
# 34 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	warp MAP_SOOTOPOLIS_CITY_MYSTERY_EVENTS_HOUSE_1F, 3, 1
# 35 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitstate
# 36 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	releaseall
# 37 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	end
# 38 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 39 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleTie::
# 40 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	setvar VAR_SOOTOPOLIS_MYSTERY_EVENTS_STATE, 3
# 41 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	msgbox SootopolisCity_MysteryEventsHouse_B1F_Text_MatchEndedUpDraw, MSGBOX_DEFAULT
# 42 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	return
# 43 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 44 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleWon::
# 45 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	setvar VAR_SOOTOPOLIS_MYSTERY_EVENTS_STATE, 1
# 46 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special ShowFieldMessageStringVar4
# 47 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitmessage
# 48 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitbuttonpress
# 49 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	return
# 50 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 51 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_EventScript_BattleLost::
# 52 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	setvar VAR_SOOTOPOLIS_MYSTERY_EVENTS_STATE, 2
# 53 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	special ShowFieldMessageStringVar4
# 54 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitmessage
# 55 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	waitbuttonpress
# 56 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	return
# 57 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 58 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_Movement_PlayerEnterBasement:
# 59 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_down
# 60 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_down
# 61 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_down
# 62 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_right
# 63 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_right
# 64 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	step_end
# 65 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"

# 66 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
SootopolisCity_MysteryEventsHouse_B1F_Movement_PlayerExitBasement:
# 67 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_left
# 68 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_left
# 69 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_up
# 70 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_up
# 71 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_up
# 72 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	walk_up
# 73 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	delay_8
# 74 "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.pory"
	step_end
