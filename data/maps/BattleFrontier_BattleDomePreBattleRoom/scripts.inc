# 1 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 2 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_MapScripts::
# 3 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattleDomePreBattleRoom_OnFrame
# 4 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, BattleFrontier_BattleDomePreBattleRoom_OnWarp
# 5 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.byte 0
# 6 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 7 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_OnWarp:
# 8 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_TurnPlayerNorth
# 9 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.2byte 0
# 10 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 11 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_TurnPlayerNorth::
# 12 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setvar VAR_TEMP_1, 1
# 13 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 14 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	end
# 15 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 16 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_OnFrame:
# 17 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	map_script_2 VAR_TEMP_0, 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_EnterRoom
# 18 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.2byte 0
# 19 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 20 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_EnterRoom::
# 21 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto_if_eq VAR_0x8006, 1, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReturnFromBattle
# 22 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_set FRONTIER_DATA_RECORD_DISABLED, TRUE
# 23 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setvar VAR_TEMP_0, 1
# 24 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleDomePreBattleRoom_Movement_PlayerEnter
# 25 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmovement 0
# 26 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	lockall
# 27 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound::
# 28 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	call BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForNextRoundMessage
# 29 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmessage
# 30 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT  @ No case?
# 31 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	call BattleFrontier_EventScript_GetCantRecordBattle
# 32 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRoundNoRecord
# 33 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	multichoice 16, 0, MULTI_TOURNEY_WITH_RECORD, TRUE
# 34 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 35 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowOpponentInfo
# 36 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 1, BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowTourneyTree
# 37 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 2, BattleFrontier_BattleDomePreBattleRoom_EventScript_ContinueChallenge
# 38 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 3, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskRecordBattle
# 39 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 4, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskPauseChallenge
# 40 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 5, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskRetireChallenge
# 41 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 42 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 43 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRoundNoRecord::
# 44 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	multichoice 16, 2, MULTI_TOURNEY_NO_RECORD, TRUE
# 45 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 46 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowOpponentInfo
# 47 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 1, BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowTourneyTree
# 48 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 2, BattleFrontier_BattleDomePreBattleRoom_EventScript_ContinueChallenge
# 49 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 3, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskPauseChallenge
# 50 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 4, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskRetireChallenge
# 51 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 52 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 53 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_AskRecordBattle::
# 54 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_RecordLastMatch
# 55 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmessage
# 56 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	multichoicedefault 20, 8, MULTI_YESNO, 1, FALSE
# 57 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 58 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 1, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 59 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_RecordBattle
# 60 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 61 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 62 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_RecordBattle::
# 63 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	call BattleFrontier_EventScript_SaveBattle
# 64 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 65 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 66 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_AskPauseChallenge::
# 67 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_SaveAndQuitGame, MSGBOX_YESNO
# 68 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 69 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case NO, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 70 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case YES, BattleFrontier_BattleDomePreBattleRoom_EventScript_PauseChallenge
# 71 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 72 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 73 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_AskRetireChallenge::
# 74 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_RetireYourChallenge
# 75 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmessage
# 76 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	multichoicedefault 20, 8, MULTI_YESNO, 1, FALSE
# 77 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 78 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 1, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 79 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_RetireChallenge
# 80 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 81 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 82 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_RetireChallenge::
# 83 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_resolvewinners DOME_PLAYER_RETIRED
# 84 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto BattleFrontier_BattleDomeBattleRoom_EventScript_WarpToLobbyLost
# 85 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 86 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_PauseChallenge::
# 87 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_SavingDataPleaseWait
# 88 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmessage
# 89 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_save CHALLENGE_STATUS_PAUSED
# 90 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	playse SE_SAVE
# 91 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitse
# 92 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	fadescreen FADE_TO_BLACK
# 93 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_reset
# 94 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	end
# 95 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 96 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowOpponentInfo::
# 97 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_PlayersNextOpponentIsTrainer, MSGBOX_DEFAULT
# 98 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	fadescreen FADE_TO_BLACK
# 99 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_showopponentinfo
# 100 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitstate
# 101 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 102 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 103 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowTourneyTree::
# 104 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	call BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowRoundMessage
# 105 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	fadescreen FADE_TO_BLACK
# 106 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_showtourneytree
# 107 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitstate
# 108 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 109 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 110 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ShowRoundMessage::
# 111 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_get FRONTIER_DATA_BATTLE_NUM
# 112 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 113 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_ROUND1, BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInRound1
# 114 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_ROUND2, BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInRound2
# 115 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_SEMIFINAL, BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInSemifinals
# 116 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_FINAL, BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInFinals
# 117 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 118 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 119 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInRound1::
# 120 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInRound1, MSGBOX_DEFAULT
# 121 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 122 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 123 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInRound2::
# 124 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInRound2, MSGBOX_DEFAULT
# 125 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 126 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 127 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInSemifinals::
# 128 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInSemifinals, MSGBOX_DEFAULT
# 129 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 130 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 131 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_TourneyInFinals::
# 132 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInFinals, MSGBOX_DEFAULT
# 133 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 134 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 135 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ContinueChallenge::
# 136 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_ChooseTwoMons
# 137 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmessage
# 138 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitbuttonpress
# 139 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	fadescreen FADE_TO_BLACK
# 140 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 141 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 142 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setvar VAR_0x8005, DOME_BATTLE_PARTY_SIZE  @ 2 of the 3 party mons are selected for battle
# 143 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	special ChoosePartyForBattleFrontier
# 144 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_resetsketch
# 145 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 146 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_set DOME_DATA_SELECTED_MONS
# 147 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_reduceparty
# 148 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_setopponent
# 149 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_RightThisWay, MSGBOX_DEFAULT
# 150 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	closemessage
# 151 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	applymovement LOCALID_DOME_PRE_BATTLE_ATTENDANT, BattleFrontier_BattleDomePreBattleRoom_Movement_AttendantMoveAside
# 152 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmovement 0
# 153 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleDomePreBattleRoom_Movement_PlayerWalkToDoor
# 154 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmovement 0
# 155 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	opendoor 5, 1
# 156 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitdooranim
# 157 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleDomePreBattleRoom_Movement_PlayerEnterDoor
# 158 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitmovement 0
# 159 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	closedoor 5, 1
# 160 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitdooranim
# 161 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_DOME_BATTLE_ROOM, 9, 5
# 162 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setvar VAR_TEMP_0, 0
# 163 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitstate
# 164 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	end
# 165 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 166 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForNextRoundMessage::
# 167 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_get FRONTIER_DATA_BATTLE_NUM
# 168 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 169 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_ROUND1, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForRound1
# 170 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_ROUND2, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForRound2
# 171 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_SEMIFINAL, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForSemifinals
# 172 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_FINAL, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForFinals
# 173 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 174 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 175 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForRound1::
# 176 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForRound1
# 177 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 178 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 179 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForRound2::
# 180 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForRound2
# 181 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 182 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 183 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForSemifinals::
# 184 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForSemifinals
# 185 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 186 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 187 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForFinals::
# 188 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_getbrainstatus
# 189 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 190 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case FRONTIER_BRAIN_SILVER, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerSilver
# 191 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case FRONTIER_BRAIN_GOLD, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerGold
# 192 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case FRONTIER_BRAIN_STREAK, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerSilver
# 193 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case FRONTIER_BRAIN_STREAK_LONG, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerGold
# 194 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	message BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForFinals
# 195 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 196 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 197 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerSilver::
# 198 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto_if_set FLAG_TEMP_1, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerSilverShort
# 199 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerSilver, MSGBOX_DEFAULT
# 200 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setflag FLAG_TEMP_1
# 201 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 202 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 203 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerGold::
# 204 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto_if_set FLAG_TEMP_1, BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerGoldShort
# 205 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerGold, MSGBOX_DEFAULT
# 206 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setflag FLAG_TEMP_1
# 207 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 208 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 209 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerSilverShort::
# 210 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerSilverShort, MSGBOX_DEFAULT
# 211 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 212 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 213 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReadyForTuckerGoldShort::
# 214 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerGoldShort, MSGBOX_DEFAULT
# 215 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 216 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 217 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_ReturnFromBattle::
# 218 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	setvar VAR_TEMP_0, 1
# 219 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_RestoreMonsToFullHealth, MSGBOX_DEFAULT
# 220 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	special LoadPlayerParty
# 221 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_setpartyorder FRONTIER_PARTY_SIZE
# 222 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	playfanfare MUS_HEAL
# 223 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitfanfare
# 224 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	special HealPlayerParty
# 225 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	call BattleFrontier_BattleDomePreBattleRoom_EventScript_RoundCompleteMessage
# 226 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	fadescreen FADE_TO_BLACK
# 227 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	dome_showstatictourneytree
# 228 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	waitstate
# 229 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	goto BattleFrontier_BattleDomePreBattleRoom_EventScript_AskReadyForNextRound
# 230 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 231 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_RoundCompleteMessage::
# 232 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	frontier_get FRONTIER_DATA_BATTLE_NUM
# 233 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	switch VAR_RESULT
# 234 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_ROUND2, BattleFrontier_BattleDomePreBattleRoom_EventScript_Round1Complete
# 235 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_SEMIFINAL, BattleFrontier_BattleDomePreBattleRoom_EventScript_Round2Complete
# 236 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	case DOME_FINAL, BattleFrontier_BattleDomePreBattleRoom_EventScript_SemifinalsComplete
# 237 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 238 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 239 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_Round1Complete::
# 240 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_Round1Complete, MSGBOX_DEFAULT
# 241 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 242 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 243 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_Round2Complete::
# 244 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_Round2Complete, MSGBOX_DEFAULT
# 245 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 246 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 247 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_EventScript_SemifinalsComplete::
# 248 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	msgbox BattleFrontier_BattleDomePreBattleRoom_Text_SemifinalsComplete, MSGBOX_DEFAULT
# 249 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	return
# 250 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 251 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Movement_AttendantMoveAside:
# 252 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_right
# 253 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	face_left
# 254 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	step_end
# 255 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 256 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Movement_PlayerEnter:
# 257 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_up
# 258 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_up
# 259 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_up
# 260 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_up
# 261 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	step_end
# 262 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 263 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Movement_PlayerWalkToDoor:
# 264 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_up
# 265 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	step_end
# 266 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 267 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Movement_PlayerEnterDoor:
# 268 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	walk_up
# 269 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	set_invisible
# 270 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	step_end
# 271 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 272 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForRound1:
# 273 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Your 1st-round match is next.\n"
# 274 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 275 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 276 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForRound2:
# 277 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Your 2nd-round match is next.\n"
# 278 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 279 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 280 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForSemifinals:
# 281 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Your semifinal match is next.\n"
# 282 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 283 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 284 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForFinals:
# 285 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Your final match is next.\n"
# 286 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 287 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 288 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ChooseTwoMons:
# 289 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Please choose the two POKéMON\n"
# 290 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "that are to appear in battle.$"
# 291 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 292 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_RightThisWay:
# 293 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Right this way, please.$"
# 294 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 295 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_RestoreMonsToFullHealth:
# 296 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Thank you for competing!\p"
# 297 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "I'll restore your POKéMON to\n"
# 298 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "full health.$"
# 299 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 300 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_Round1Complete:
# 301 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "All 1st-round matches have been\n"
# 302 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "completed.\p"
# 303 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "These are the teams that advanced!$"
# 304 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 305 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_Round2Complete:
# 306 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "All 2nd-round matches have been\n"
# 307 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "completed.\p"
# 308 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "These are the teams that advanced!$"
# 309 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 310 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_SemifinalsComplete:
# 311 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "All semifinal matches have been\n"
# 312 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "completed.\p"
# 313 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "These are the teams that advanced!$"
# 314 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 315 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
@ Unused
# 316 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_CongratsReadyForRound2:
# 317 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Congratulations for getting through\n"
# 318 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "the 1st round.\p"
# 319 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "The 2nd round is next.\n"
# 320 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 321 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 322 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
@ Unused
# 323 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_CongratsReadyForSemifinals:
# 324 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Congratulations for advancing\n"
# 325 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "to the semifinals.\p"
# 326 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "The best four teams meet in this round.\n"
# 327 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 328 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 329 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
@ Unused
# 330 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_CongratsReadyForFinals:
# 331 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Congratulations for advancing\n"
# 332 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "to the final match.\p"
# 333 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "You're one win from the championship.\n"
# 334 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 335 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 336 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_PlayersNextOpponentIsTrainer:
# 337 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "{PLAYER}'s next opponent\n"
# 338 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "is this TRAINER.$"
# 339 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 340 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInRound1:
# 341 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "The tournament is in the 1st round.$"
# 342 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 343 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInRound2:
# 344 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "The tournament is in the 2nd round.$"
# 345 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 346 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInSemifinals:
# 347 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "The tournament is in the semifinals.$"
# 348 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 349 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_TourneyInFinals:
# 350 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "The tournament is up to the final.$"
# 351 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 352 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_SaveAndQuitGame:
# 353 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Would you like to save and\n"
# 354 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "quit the game?$"
# 355 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 356 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_RetireYourChallenge:
# 357 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Would you like to retire from your\n"
# 358 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Battle Tournament challenge?$"
# 359 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 360 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_SavingDataPleaseWait:
# 361 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "I am saving your data.\n"
# 362 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Please wait.$"
# 363 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 364 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_RecordLastMatch:
# 365 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Should I record your last match\n"
# 366 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "on your FRONTIER PASS?$"
# 367 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 368 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerSilver:
# 369 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Congratulations for advancing\n"
# 370 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "to the final match.\p"
# 371 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "For the final match, you will challenge\n"
# 372 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "the DOME ACE TUCKER.\p"
# 373 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 374 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 375 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
@ Identical to ReadyForTuckerSilver
# 376 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerGold:
# 377 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Congratulations for advancing\n"
# 378 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "to the final match.\p"
# 379 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "For the final match, you will challenge\n"
# 380 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "the DOME ACE TUCKER.\p"
# 381 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Are you ready?$"
# 382 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 383 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerSilverShort:
# 384 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Your final battle against TUCKER is\n"
# 385 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "next. Are you ready?$"
# 386 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"

# 387 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
@ Identical again
# 388 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
BattleFrontier_BattleDomePreBattleRoom_Text_ReadyForTuckerGoldShort:
# 389 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "Your final battle against TUCKER is\n"
# 390 "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.pory"
	.string "next. Are you ready?$"
