# 1 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 2 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_MapScripts::
# 3 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, BattleFrontier_BattleTowerLobby_OnResume
# 4 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_BattleTowerLobby_OnTransition
# 5 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattleTowerLobby_OnFrame
# 6 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, BattleFrontier_BattleTowerLobby_OnWarp
# 7 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.byte 0
# 8 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 9 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_OnResume:
# 10 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special TryHideBattleTowerReporter
# 11 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 12 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 13 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_OnTransition:
# 14 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_ShowOrHideReporter
# 15 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	apprentice_shouldcheckgone
# 16 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_0x8004, FALSE, BattleFrontier_BattleTowerLobby_EventScript_ShowApprentice  @ VAR_0x8004 always TRUE here
# 17 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_set FLAG_DAILY_APPRENTICE_LEAVES, BattleFrontier_BattleTowerLobby_EventScript_HideApprentice
# 18 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowApprentice::
# 19 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	clearflag FLAG_HIDE_APPRENTICE
# 20 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	apprentice_setgfx
# 21 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_EndShowOrHideApprentice::
# 22 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 23 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 24 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_HideApprentice::
# 25 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setflag FLAG_HIDE_APPRENTICE
# 26 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndShowOrHideApprentice
# 27 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 28 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_OnWarp:
# 29 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, BattleFrontier_BattleTowerLobby_EventScript_PlayerFaceNorth
# 30 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.2byte 0
# 31 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 32 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_PlayerFaceNorth::
# 33 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_1, 1
# 34 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 35 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 36 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 37 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_OnFrame:
# 38 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, 0, BattleFrontier_BattleTowerLobby_EventScript_GetChallengeStatus
# 39 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING, BattleFrontier_BattleTowerLobby_EventScript_QuitWithoutSaving
# 40 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_PAUSED, BattleFrontier_BattleTowerLobby_EventScript_ResumeChallenge
# 41 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_WON, BattleFrontier_BattleTowerLobby_EventScript_WonChallenge
# 42 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST, BattleFrontier_BattleTowerLobby_EventScript_LostChallenge
# 43 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.2byte 0
# 44 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 45 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetChallengeStatus::
# 46 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_getstatus
# 47 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 48 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 49 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_QuitWithoutSaving::
# 50 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 51 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 52 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_DidntSaveBeforeQuitting, MSGBOX_DEFAULT
# 53 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 54 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK, 0
# 55 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK_ACTIVE, FALSE
# 56 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 57 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 58 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 59 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 60 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 61 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_WonChallenge::
# 62 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 63 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 64 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_isbrain
# 65 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattleTowerLobby_EventScript_DefeatedMaiden
# 66 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_CongratsBeatenSeven
# 67 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 68 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_GiveRibbons
# 69 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 70 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_DefeatedMaiden::
# 71 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_CongratsDefeatedMaiden, MSGBOX_DEFAULT
# 72 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GiveRibbons::
# 73 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_giveribbons
# 74 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_BattleTowerLobby_EventScript_GiveBattlePoints
# 75 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_HereAreSomeRibbons
# 76 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 77 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 78 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitfanfare
# 79 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_PutRibbonOnMons, MSGBOX_DEFAULT
# 80 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GiveBattlePoints::
# 81 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_AwardYouTheseBattlePoints, MSGBOX_DEFAULT
# 82 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_givepoints
# 83 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_Text_ObtainedXBattlePoints, MSGBOX_GETPOINTS
# 84 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_AskSaveBattle
# 85 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_get TOWER_DATA_WIN_STREAK
# 86 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_ne VAR_RESULT, 49, BattleFrontier_BattleTowerLobby_EventScript_LookForwardToChallenge
# 87 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_AboutToFace50thTrainer, MSGBOX_DEFAULT
# 88 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_LookForwardToChallenge::
# 89 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_LookForwardToAnotherChallenge, MSGBOX_DEFAULT
# 90 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 91 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 92 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 93 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 94 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 95 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 96 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_LostChallenge::
# 97 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_ne VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_CancelWinStreak
# 98 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_set FLAG_CHOSEN_MULTI_BATTLE_NPC_PARTNER, BattleFrontier_BattleTowerLobby_EventScript_CancelWinStreak
# 99 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_get TOWER_DATA_WIN_STREAK
# 100 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_ne VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_LostThanksForPlaying
# 101 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_CancelWinStreak::
# 102 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK_ACTIVE, FALSE
# 103 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_LostThanksForPlaying::
# 104 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 105 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 106 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_ThankYouForPlaying
# 107 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 108 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_AskSaveBattle
# 109 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_LookForwardToAnotherChallenge, MSGBOX_DEFAULT
# 110 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 111 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 112 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 113 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 114 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 115 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 116 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AskSaveBattle::
# 117 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_RecordWillBeSaved
# 118 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 119 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_checkairshow
# 120 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special LoadPlayerParty
# 121 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special HealPlayerParty
# 122 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_save 0
# 123 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	playse SE_SAVE
# 124 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitse
# 125 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_EventScript_GetCantRecordBattle
# 126 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattleTowerLobby_EventScript_EndSaveBattle
# 127 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_RecordLastMatch
# 128 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 129 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoicedefault 20, 8, MULTI_YESNO, 1, FALSE
# 130 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 131 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_EndSaveBattle
# 132 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_EventScript_SaveBattle
# 133 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_EndSaveBattle
# 134 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 135 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_EventScript_SaveBattle::
# 136 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_savebattle
# 137 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_EventScript_BattleSaveFailed
# 138 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	playse SE_SAVE
# 139 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_BattleRecordedOnPass, MSGBOX_DEFAULT
# 140 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndSaveBattle
# 141 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 142 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_EventScript_BattleSaveFailed::
# 143 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerBattleRoom_Text_RecordCouldntBeSaved, MSGBOX_DEFAULT
# 144 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_EndSaveBattle::
# 145 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 146 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 147 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_EventScript_GetCantRecordBattle::
# 148 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_get FRONTIER_DATA_RECORD_DISABLED
# 149 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 150 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 151 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ResumeChallenge::
# 152 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 153 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 154 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_SetBravoTrainerOn
# 155 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_WeveBeenWaitingForYou
# 156 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 157 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_ProgressWillBeSaved
# 158 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 159 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_save CHALLENGE_STATUS_SAVING
# 160 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	playse SE_SAVE
# 161 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitse
# 162 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 163 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EnterElevator
# 164 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 165 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 166 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SetBravoTrainerOn::
# 167 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, TRUE
# 168 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 169 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 170 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SinglesAttendant::
# 171 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 172 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 173 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_TOWER
# 174 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SavePlayerParty
# 175 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_WelcomSingleBattle, MSGBOX_DEFAULT
# 176 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AskEnterSinglesChallenge::
# 177 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_TakeSinglesChallenge
# 178 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 179 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 180 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 181 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_TryEnterSinglesChallenge
# 182 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_ExplainSinglesChallenge
# 183 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 184 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 185 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 186 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryEnterSinglesChallenge::
# 187 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES
# 188 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_WhichLevelMode
# 189 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 190 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 191 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 192 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 193 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 194 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_checkineligible
# 195 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMons
# 196 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, VAR_RESULT
# 197 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_SelectThreeMons, MSGBOX_DEFAULT
# 198 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 199 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative RemoveFollowingPokemon
# 200 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 201 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 202 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_PARTY_SIZE
# 203 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 204 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 205 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_OkayToSaveBeforeEntering, MSGBOX_YESNO
# 206 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 207 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case NO, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 208 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case YES, BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeSinglesChallenge
# 209 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 210 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 211 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeSinglesChallenge::
# 212 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 213 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 214 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_init
# 215 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK_ACTIVE, TRUE
# 216 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 217 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special LoadPlayerParty
# 218 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 219 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	delay 2
# 220 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 221 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 222 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_CancelChallengeSaveFailed
# 223 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	incrementgamestat GAME_STAT_ENTERED_BATTLE_TOWER
# 224 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, TRUE
# 225 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EnterElevator
# 226 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 227 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 228 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ExplainSinglesChallenge::
# 229 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainSinglesChallenge, MSGBOX_DEFAULT
# 230 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_AskEnterSinglesChallenge
# 231 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 232 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 233 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_DoublesAttendant::
# 234 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 235 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 236 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_TOWER
# 237 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SavePlayerParty
# 238 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_WelcomeDoubleBattle, MSGBOX_DEFAULT
# 239 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AskEnterDoublesChallenge::
# 240 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_TakeDoublesChallenge
# 241 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 242 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 243 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 244 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_TryEnterDoublesChallenge
# 245 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_ExplainDoublesChallenge
# 246 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 247 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 248 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 249 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryEnterDoublesChallenge::
# 250 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_DOUBLES
# 251 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_WhichLevelMode
# 252 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 253 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 254 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 255 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 256 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 257 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_checkineligible
# 258 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMons
# 259 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, VAR_RESULT
# 260 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_PleaseSelectFourMons, MSGBOX_DEFAULT
# 261 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 262 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative RemoveFollowingPokemon
# 263 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 264 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 265 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_DOUBLES_PARTY_SIZE
# 266 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 267 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 268 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_OkayToSaveBeforeEntering, MSGBOX_YESNO
# 269 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 270 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case NO, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 271 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case YES, BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeDoublesChallenge
# 272 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 273 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 274 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeDoublesChallenge::
# 275 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 276 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 277 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_init
# 278 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK_ACTIVE, TRUE
# 279 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 280 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special LoadPlayerParty
# 281 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 282 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	delay 2
# 283 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 284 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 285 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_CancelChallengeSaveFailed
# 286 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	incrementgamestat GAME_STAT_ENTERED_BATTLE_TOWER
# 287 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, FALSE
# 288 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EnterElevator
# 289 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 290 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 291 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ExplainDoublesChallenge::
# 292 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainDoublesChallenge, MSGBOX_DEFAULT
# 293 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_AskEnterDoublesChallenge
# 294 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 295 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 296 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_MultisAttendant::
# 297 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 298 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 299 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_TOWER
# 300 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	clearflag FLAG_CHOSEN_MULTI_BATTLE_NPC_PARTNER
# 301 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SavePlayerParty
# 302 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_WelcomeMultiBattle, MSGBOX_DEFAULT
# 303 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AskEnterMultisChallenge::
# 304 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_TakeMultisChallenge
# 305 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 306 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 307 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 308 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_TryEnterMultisChallenge
# 309 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_ExplainMultisChallenge
# 310 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 311 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 312 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 313 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryEnterMultisChallenge::
# 314 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS
# 315 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_WhichLevelMode
# 316 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 317 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 318 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 319 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 320 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 321 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_checkineligible
# 322 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMons
# 323 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, VAR_RESULT
# 324 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_PleaseSelectTwoMons, MSGBOX_DEFAULT
# 325 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 326 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative RemoveFollowingPokemon
# 327 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 328 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 329 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_MULTI_PARTY_SIZE
# 330 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 331 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 332 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_OkayToSaveBeforeEntering, MSGBOX_YESNO
# 333 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 334 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case NO, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 335 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case YES, BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeMultisChallenge
# 336 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 337 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 338 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeMultisChallenge::
# 339 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 340 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 341 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_init
# 342 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK_ACTIVE, TRUE
# 343 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 344 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special LoadPlayerParty
# 345 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 346 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	delay 2
# 347 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 348 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 349 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_CancelChallengeSaveFailed
# 350 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	incrementgamestat GAME_STAT_ENTERED_BATTLE_TOWER
# 351 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, FALSE
# 352 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EnterElevator
# 353 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 354 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 355 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ExplainMultisChallenge::
# 356 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainMultisChallenge, MSGBOX_DEFAULT
# 357 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_AskEnterMultisChallenge
# 358 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 359 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 360 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_LinkMultisAttendant::
# 361 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 362 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 363 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_TOWER
# 364 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SavePlayerParty
# 365 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_WelcomeLinkMultiBattle, MSGBOX_DEFAULT
# 366 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AskEnterLinkMultisChallenge::
# 367 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_TakeLinkMultisChallenge
# 368 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 369 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 370 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 371 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_TryEnterLinkMultisChallenge
# 372 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_ExplainLinkMultisChallenge
# 373 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 374 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 375 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 376 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryEnterLinkMultisChallenge::
# 377 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS
# 378 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_WhichLevelMode
# 379 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 380 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 381 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 382 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 383 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 384 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_checkineligible
# 385 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMons
# 386 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, VAR_RESULT
# 387 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_PleaseSelectTwoMons2, MSGBOX_DEFAULT
# 388 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 389 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative RemoveFollowingPokemon
# 390 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 391 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 392 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_MULTI_PARTY_SIZE
# 393 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 394 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 395 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_OkayToSaveBeforeEntering, MSGBOX_YESNO
# 396 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 397 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case NO, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 398 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case YES, BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeLinkMultisChallenge
# 399 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge
# 400 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 401 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SaveBeforeLinkMultisChallenge::
# 402 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 403 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 404 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_init
# 405 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_set TOWER_DATA_WIN_STREAK_ACTIVE, TRUE
# 406 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 407 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special LoadPlayerParty
# 408 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 409 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	delay 2
# 410 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ The command tower_save ultimately calls TrySavingData(SAVE_LINK), which writes data in SaveBlock1 and SaveBlock2
# 411 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ to the flash, but not data in PokemonStorage. The SaveGame script that follows asks the player to do a full save,
# 412 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ which they can opt out of. As a result the player can save their party and quit without having saved the PC.
# 413 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ This allows players to clone pokemon and their held items by withdrawing them (or erase them by despositing).
# 414 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
#ifndef BUGFIX
# 415 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_save 0
# 416 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
#endif
# 417 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 418 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 419 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_CancelChallengeSaveFailed
# 420 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ GAME_STAT_ENTERED_BATTLE_TOWER should not be incremented here, for two reasons:
# 421 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ 1. It is incremented again in BattleFrontier_BattleTowerLobby_EventScript_CableLinkSuccessful or BattleFrontier_BattleTowerLobby_EventScript_WirelessLinkSuccessful
# 422 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ 2. If the player tries to connect, but fails, the counter will still be incremented even if the player never enters the tower.
# 423 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
#ifndef BUGFIX
# 424 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	incrementgamestat GAME_STAT_ENTERED_BATTLE_TOWER
# 425 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
#endif
# 426 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	specialvar VAR_RESULT, IsWirelessAdapterConnected
# 427 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattleTowerLobby_EventScript_TryWirelessLink
# 428 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_TryCableLink
# 429 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 430 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 431 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FeelingsMan::
# 432 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 433 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 434 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_DescribeFeelingsAboutBattleTower
# 435 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 436 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 16, 4, MULTI_BATTLE_TOWER_FEELINGS, FALSE
# 437 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 438 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_FeelingsBattleNow
# 439 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_FeelingsIWon
# 440 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_FeelingsILost
# 441 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 3, BattleFrontier_BattleTowerLobby_EventScript_FeelingsWontTell
# 442 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_FeelingsWontTell
# 443 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 444 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 445 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 446 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FeelingsBattleNow::
# 447 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FeelWhatWhenYouBegin, MSGBOX_DEFAULT
# 448 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, EASY_CHAT_TYPE_BATTLE_START
# 449 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_ShowEasyChatScreen
# 450 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 451 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 452 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_CheckFeelings
# 453 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 454 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 455 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FeelingsIWon::
# 456 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FeelWhatWhenYouveWon, MSGBOX_DEFAULT
# 457 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, EASY_CHAT_TYPE_BATTLE_WON
# 458 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_ShowEasyChatScreen
# 459 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 460 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 461 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_CheckFeelings
# 462 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 463 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 464 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FeelingsILost::
# 465 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FeelWhatWhenYouveLost, MSGBOX_DEFAULT
# 466 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, EASY_CHAT_TYPE_BATTLE_LOST
# 467 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call Common_ShowEasyChatScreen
# 468 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lock
# 469 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	faceplayer
# 470 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_CheckFeelings
# 471 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 472 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 473 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FeelingsWontTell::
# 474 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_DontThinkMuchAboutIt, MSGBOX_DEFAULT
# 475 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 476 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 477 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 478 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_CheckFeelings::
# 479 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattleTowerLobby_EventScript_CanceledEasyChat
# 480 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 1, BattleFrontier_BattleTowerLobby_EventScript_SubmittedFeelings
# 481 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 482 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 483 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_CanceledEasyChat::
# 484 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ChangedYourMind, MSGBOX_DEFAULT
# 485 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 486 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 487 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 488 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SubmittedFeelings::
# 489 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ThatsHowYouFeel, MSGBOX_DEFAULT
# 490 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 491 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 492 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 493 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_Woman::
# 494 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_WinsInRowRecorded, MSGBOX_NPC
# 495 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 496 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 497 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_Boy::
# 498 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_CanLeaveUntilLossOrSevenWins, MSGBOX_NPC
# 499 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 500 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 501 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowSinglesResults::
# 502 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lockall
# 503 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_results FRONTIER_FACILITY_TOWER, FRONTIER_MODE_SINGLES
# 504 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitbuttonpress
# 505 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special RemoveRecordsWindow
# 506 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	releaseall
# 507 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 508 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 509 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowDoublesResults::
# 510 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lockall
# 511 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_results FRONTIER_FACILITY_TOWER, FRONTIER_MODE_DOUBLES
# 512 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitbuttonpress
# 513 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special RemoveRecordsWindow
# 514 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	releaseall
# 515 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 516 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 517 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowMultisResults::
# 518 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lockall
# 519 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_results FRONTIER_FACILITY_TOWER, FRONTIER_MODE_MULTIS
# 520 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitbuttonpress
# 521 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special RemoveRecordsWindow
# 522 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	releaseall
# 523 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 524 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 525 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowLinkMultisResults::
# 526 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lockall
# 527 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_results FRONTIER_FACILITY_TOWER, FRONTIER_MODE_LINK_MULTIS
# 528 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitbuttonpress
# 529 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special RemoveRecordsWindow
# 530 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	releaseall
# 531 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 532 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 533 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMons::
# 534 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 535 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_LVL_50, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLv50
# 536 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_LVL_OPEN, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLvOpen
# 537 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 538 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLv50::
# 539 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_FRONTIER_BATTLE_MODE
# 540 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLv50Singles
# 541 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLv50Doubles
# 542 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50Multis, MSGBOX_DEFAULT
# 543 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 544 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 545 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge
# 546 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 547 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 548 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLv50Singles::
# 549 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50Singles, MSGBOX_DEFAULT
# 550 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 551 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 552 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge
# 553 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 554 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 555 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLv50Doubles::
# 556 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50Doubles, MSGBOX_DEFAULT
# 557 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 558 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 559 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge
# 560 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 561 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 562 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLvOpen::
# 563 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_FRONTIER_BATTLE_MODE
# 564 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLvOpenSingles
# 565 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLvOpenDoubles
# 566 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpenMultis, MSGBOX_DEFAULT
# 567 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 568 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 569 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge
# 570 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 571 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 572 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLvOpenSingles::
# 573 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpenSingles, MSGBOX_DEFAULT
# 574 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 575 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 576 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge
# 577 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 578 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 579 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_NotEnoughValidMonsLvOpenDoubles::
# 580 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpenDoubles, MSGBOX_DEFAULT
# 581 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 582 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 583 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge
# 584 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 585 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 586 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_CancelChallengeSaveFailed::
# 587 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS  @ No status provided, so it relies on VAR_0x8006 being 0 already
# 588 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 589 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 590 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 591 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_LoadPartyCancelChallenge::
# 592 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special LoadPlayerParty
# 593 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 594 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge::
# 595 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special CloseLink
# 596 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_LookForwardToAnotherChallenge, MSGBOX_DEFAULT
# 597 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_EndCancelChallenge::
# 598 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 599 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 600 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 601 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_EnterElevator::
# 602 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SavePlayerParty
# 603 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, FRONTIER_UTIL_FUNC_SET_PARTY_ORDER
# 604 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_GetPartySize
# 605 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special CallFrontierUtilFunc
# 606 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_RESULT, 0
# 607 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_WaitForLinkOpponentLoad::
# 608 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_loadlinkopponents
# 609 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	delay 1
# 610 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_ne VAR_RESULT, 6, BattleFrontier_BattleTowerLobby_EventScript_WaitForLinkOpponentLoad
# 611 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_ShowYouToBattleRoom
# 612 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	clearflag FLAG_CANCEL_BATTLE_ROOM_CHALLENGE
# 613 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_TOWER_ELEVATOR, 1, 6
# 614 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 615 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitstate
# 616 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 617 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 618 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowYouToBattleRoom::
# 619 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_BufferModeText
# 620 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_ShowYouToLinkMultiBattleRoom
# 621 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ShowYouToBattleRoom, MSGBOX_DEFAULT
# 622 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_WalkToElevator
# 623 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 624 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ShowYouToLinkMultiBattleRoom::
# 625 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	messageautoscroll BattleFrontier_BattleTowerLobby_Text_ShowYouToBattleRoom
# 626 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 627 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	delay 48
# 628 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_WalkToElevator::
# 629 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closemessage
# 630 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_SetAttendantTalkedTo
# 631 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoord
# 632 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	applymovement VAR_LAST_TALKED, BattleFrontier_BattleTowerLobby_Movement_WalkToElevator
# 633 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleTowerLobby_Movement_WalkToElevator
# 634 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmovement 0
# 635 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	opendoor VAR_0x8004, 1
# 636 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitdooranim
# 637 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	applymovement VAR_LAST_TALKED, BattleFrontier_BattleTowerLobby_Movement_AttendantEnterElevator
# 638 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattleTowerLobby_Movement_PlayerEnterElevator
# 639 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmovement 0
# 640 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	closedoor VAR_0x8004, 1
# 641 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitdooranim
# 642 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 643 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 644 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Movement_WalkToElevator:
# 645 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_up
# 646 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_up
# 647 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_up
# 648 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	step_end
# 649 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 650 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Movement_AttendantEnterElevator:
# 651 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_up
# 652 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	set_invisible
# 653 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	step_end
# 654 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 655 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Movement_PlayerEnterElevator:
# 656 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_up
# 657 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_up
# 658 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	set_invisible
# 659 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	step_end
# 660 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 661 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 662 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Movement_UnusedEnterElevator:
# 663 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_fast_up
# 664 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_fast_up
# 665 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_fast_up
# 666 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_fast_up
# 667 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	walk_fast_up
# 668 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	set_invisible
# 669 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	step_end
# 670 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 671 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_BufferModeText::
# 672 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_BufferTextSingle
# 673 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerLobby_EventScript_BufferTextDouble
# 674 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_BufferTextMulti
# 675 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_BufferTextLinkMulti
# 676 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 677 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 678 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_BufferTextSingle::
# 679 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	bufferstdstring STR_VAR_1, STDSTRING_SINGLE
# 680 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 681 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 682 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_BufferTextDouble::
# 683 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	bufferstdstring STR_VAR_1, STDSTRING_DOUBLE
# 684 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 685 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 686 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_BufferTextMulti::
# 687 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	bufferstdstring STR_VAR_1, STDSTRING_MULTI
# 688 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 689 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 690 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_BufferTextLinkMulti::
# 691 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	bufferstdstring STR_VAR_1, STDSTRING_MULTI_LINK
# 692 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 693 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 694 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_SetAttendantTalkedTo::
# 695 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_TalkedToSinglesAttendant
# 696 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerLobby_EventScript_TalkedToDoublesAttendant
# 697 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_TalkedToMultisAttendant
# 698 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_TalkedToLinkMultisAttendant
# 699 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 700 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 701 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TalkedToSinglesAttendant::
# 702 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_TOWER_ATTENDANT_SINGLES
# 703 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 704 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 705 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TalkedToDoublesAttendant::
# 706 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_TOWER_ATTENDANT_DOUBLES
# 707 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 708 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 709 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TalkedToMultisAttendant::
# 710 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_TOWER_ATTENDANT_MULTIS
# 711 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 712 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 713 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TalkedToLinkMultisAttendant::
# 714 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_TOWER_ATTENDANT_LINK_MULTIS
# 715 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 716 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 717 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoord::
# 718 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordSingles
# 719 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordDoubles
# 720 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordMultis
# 721 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordLinkMultis
# 722 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 723 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 724 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordSingles::
# 725 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, 6
# 726 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 727 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 728 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordDoubles::
# 729 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, 10
# 730 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 731 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 732 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordMultis::
# 733 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, 14
# 734 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 735 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 736 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetDoorXCoordLinkMultis::
# 737 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, 18
# 738 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 739 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 740 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetPartySize::
# 741 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES, BattleFrontier_BattleTowerLobby_EventScript_GetSinglesPartySize
# 742 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_DOUBLES, BattleFrontier_BattleTowerLobby_EventScript_GetDoublesPartySize
# 743 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_GetMultisPartySize
# 744 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_LINK_MULTIS, BattleFrontier_BattleTowerLobby_EventScript_GetLinkMultisPartySize
# 745 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 746 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 747 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetSinglesPartySize::
# 748 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_PARTY_SIZE
# 749 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 750 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 751 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetDoublesPartySize::
# 752 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_DOUBLES_PARTY_SIZE
# 753 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 754 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 755 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetMultisPartySize::
# 756 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_MULTI_PARTY_SIZE
# 757 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 758 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 759 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_GetLinkMultisPartySize::
# 760 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_MULTI_PARTY_SIZE
# 761 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 762 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 763 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_EventScript_GetLvlMode::
# 764 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	frontier_get FRONTIER_DATA_LVL_MODE
# 765 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 766 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 767 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryCableLink::
# 768 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, USING_BATTLE_TOWER
# 769 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message gText_PleaseWaitForLink
# 770 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 771 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8005, 0
# 772 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special TryBattleLinkup
# 773 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_SUCCESS, BattleFrontier_BattleTowerLobby_EventScript_CableLinkSuccessful
# 774 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_SOMEONE_NOT_READY, CableClub_EventScript_AbortLinkSomeoneNotReady
# 775 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_DIFF_SELECTIONS, BattleFrontier_BattleTowerLobby_EventScript_AbortLinkDifferentSelections
# 776 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_WRONG_NUM_PLAYERS, BattleFrontier_BattleTowerLobby_EventScript_AbortLinkIncorrectNumberOfPlayers
# 777 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_FAILED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 778 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_CONNECTION_ERROR, CableClub_EventScript_AbortLinkConnectionError
# 779 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_FAILED_BATTLE_TOWER, BattleFrontier_BattleTowerLobby_EventScript_AbortLink
# 780 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 781 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 782 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AbortLinkDifferentSelections::
# 783 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special CloseLink
# 784 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_0x8005, 3, BattleFrontier_BattleTowerLobby_EventScript_FriendDifferentSelection
# 785 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox Text_PlayersMadeDifferentSelections, MSGBOX_DEFAULT
# 786 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 787 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 788 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 789 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FriendDifferentSelection::
# 790 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FriendChoseDifferentLvlMode, MSGBOX_DEFAULT
# 791 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ChooseDifferentMonsMatchLvlMode, MSGBOX_DEFAULT
# 792 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 793 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 794 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 795 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AbortLinkIncorrectNumberOfPlayers::
# 796 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_LinkMultiOnlyForTwoPlayers, MSGBOX_DEFAULT
# 797 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special CloseLink
# 798 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox CableClub_Text_IncorrectNumberOfParticipants, MSGBOX_DEFAULT
# 799 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 800 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 801 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 802 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_AbortLink::
# 803 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special CloseLink
# 804 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_0x8005, 0, BattleFrontier_BattleTowerLobby_EventScript_FriendChoseDifferentLvlMode
# 805 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_0x8005, 1, BattleFrontier_BattleTowerLobby_EventScript_FriendAlsoSelectedMon
# 806 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call_if_eq VAR_0x8005, 2, BattleFrontier_BattleTowerLobby_EventScript_FriendAlsoSelectedMons
# 807 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ChooseDifferentMonsMatchLvlMode, MSGBOX_DEFAULT
# 808 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 809 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 810 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 811 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FriendChoseDifferentLvlMode::
# 812 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FriendChoseDifferentLvlMode, MSGBOX_DEFAULT
# 813 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 814 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 815 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FriendAlsoSelectedMon::
# 816 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FriendAlsoSelectedMon, MSGBOX_DEFAULT
# 817 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 818 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 819 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_FriendAlsoSelectedMons::
# 820 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_FriendAlsoSelectedMons, MSGBOX_DEFAULT
# 821 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 822 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 823 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_CableLinkSuccessful::
# 824 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	incrementgamestat GAME_STAT_ENTERED_BATTLE_TOWER
# 825 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, FALSE
# 826 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_SaveGameBeforeShowingIn
# 827 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 828 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_save CHALLENGE_STATUS_SAVING
# 829 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SaveForBattleTowerLink
# 830 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	playse SE_SAVE
# 831 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitse
# 832 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special TrySetBattleTowerLinkType
# 833 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EnterElevator
# 834 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 835 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 836 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ExplainLinkMultisChallenge::
# 837 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainLinkMultisChallenge, MSGBOX_DEFAULT
# 838 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_AskEnterLinkMultisChallenge
# 839 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 840 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 841 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryWirelessLink::
# 842 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_0x8004, LINK_GROUP_BATTLE_TOWER
# 843 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_ChooseLeader
# 844 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 845 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 846 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ChooseLeader::
# 847 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message CableClub_Text_ChooseGroupLeaderOfTwo
# 848 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 849 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 16, 6, MULTI_LINK_LEADER, FALSE
# 850 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 851 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_TryJoinGroup
# 852 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_TryBecomeLeader
# 853 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 854 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_CancelChallenge
# 855 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 856 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 857 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryBecomeLeader::
# 858 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call CableClub_EventScript_TryBecomeLinkLeader
# 859 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_SUCCESS, BattleFrontier_BattleTowerLobby_EventScript_WirelessLinkSuccessful
# 860 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_FAILED, BattleFrontier_BattleTowerLobby_EventScript_ChooseLeader
# 861 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_RETRY_ROLE_ASSIGN, BattleFrontier_BattleTowerLobby_EventScript_TryBecomeLeader
# 862 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_FAILED_BATTLE_TOWER, BattleFrontier_BattleTowerLobby_EventScript_AbortLink
# 863 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 864 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 865 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 866 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_TryJoinGroup::
# 867 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	call CableClub_EventScript_TryJoinLinkGroup
# 868 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_SUCCESS, BattleFrontier_BattleTowerLobby_EventScript_WirelessLinkSuccessful
# 869 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_FAILED, BattleFrontier_BattleTowerLobby_EventScript_ChooseLeader
# 870 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_RETRY_ROLE_ASSIGN, BattleFrontier_BattleTowerLobby_EventScript_TryJoinGroup
# 871 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto_if_eq VAR_RESULT, LINKUP_FAILED_BATTLE_TOWER, BattleFrontier_BattleTowerLobby_EventScript_AbortLink
# 872 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	release
# 873 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	return
# 874 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 875 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_WirelessLinkSuccessful::
# 876 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	incrementgamestat GAME_STAT_ENTERED_BATTLE_TOWER
# 877 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, FALSE
# 878 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_SaveGameBeforeShowingIn
# 879 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 880 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	tower_save CHALLENGE_STATUS_SAVING
# 881 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	special SaveForBattleTowerLink
# 882 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	playse SE_SAVE
# 883 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitse
# 884 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_EnterElevator
# 885 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 886 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 887 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_RulesBoard::
# 888 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	lockall
# 889 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_RulesAreListed, MSGBOX_DEFAULT
# 890 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_ReadRulesBoard
# 891 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 892 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 893 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ReadRulesBoard::
# 894 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	message BattleFrontier_BattleTowerLobby_Text_ReadWhichHeading
# 895 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	waitmessage
# 896 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	multichoice 17, 2, MULTI_BATTLE_TOWER_RULES, FALSE
# 897 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	switch VAR_RESULT
# 898 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 0, BattleFrontier_BattleTowerLobby_EventScript_RulesTower
# 899 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 1, BattleFrontier_BattleTowerLobby_EventScript_RulesMons
# 900 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 2, BattleFrontier_BattleTowerLobby_EventScript_RulesSalon
# 901 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 3, BattleFrontier_BattleTowerLobby_EventScript_RulesMultiLink
# 902 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case 4, BattleFrontier_BattleTowerLobby_EventScript_ExitRules
# 903 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattleTowerLobby_EventScript_ExitRules
# 904 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 905 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 906 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_RulesTower::
# 907 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainTowerRules, MSGBOX_DEFAULT
# 908 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_ReadRulesBoard
# 909 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 910 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 911 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_RulesMons::
# 912 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainMonRules, MSGBOX_DEFAULT
# 913 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_ReadRulesBoard
# 914 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 915 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 916 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_RulesSalon::
# 917 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainSalonRules, MSGBOX_DEFAULT
# 918 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_ReadRulesBoard
# 919 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 920 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 921 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_RulesMultiLink::
# 922 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	msgbox BattleFrontier_BattleTowerLobby_Text_ExplainMultiLinkRules, MSGBOX_DEFAULT
# 923 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	goto BattleFrontier_BattleTowerLobby_EventScript_ReadRulesBoard
# 924 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 925 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 926 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_EventScript_ExitRules::
# 927 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	releaseall
# 928 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	end
# 929 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 930 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 931 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_DirectYouToBattleRoom:
# 932 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I'll direct you to your BATTLE ROOM now.$"
# 933 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 934 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_DidntSaveBeforeQuitting:
# 935 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 936 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You didn't save before you quit your\n"
# 937 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "challenge last time.\p"
# 938 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Because of that, your challenge so far\n"
# 939 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "has been disqualified. Sorry!$"
# 940 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 941 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_CongratsBeatenSeven:
# 942 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Congratulations!\n"
# 943 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You've beaten all seven TRAINERS!\p"
# 944 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "$"
# 945 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 946 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 947 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_EarnedFabulousPrize:
# 948 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "For beating seven TRAINERS in a row,\n"
# 949 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you have earned this fabulous prize!\p"
# 950 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "$"
# 951 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 952 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ReceivedPrize:
# 953 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "{PLAYER} received the prize\n"
# 954 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "{STR_VAR_1}.$"
# 955 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 956 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 957 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_BagFullMakeRoom:
# 958 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Oh, your BAG appears to be full.\p"
# 959 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please make room in your BAG, then come\n"
# 960 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "see me.$"
# 961 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 962 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ThankYouForPlaying:
# 963 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Thank you for playing!\p"
# 964 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "$"
# 965 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 966 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_RecordWillBeSaved:
# 967 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your record will be saved.\n"
# 968 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please wait.$"
# 969 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 970 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WeveBeenWaitingForYou:
# 971 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "We've been waiting for you!\p"
# 972 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "$"
# 973 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 974 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ProgressWillBeSaved:
# 975 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Before entering a BATTLE ROOM, your\n"
# 976 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "progress will be saved. Please wait.$"
# 977 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 978 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_AboutToFace50thTrainer:
# 979 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You're finally about to face the\n"
# 980 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "50th TRAINER.\p"
# 981 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "From here on, every time you beat seven\n"
# 982 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "TRAINERS in a row, your POKéMON will\l"
# 983 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "receive a commemorative RIBBON.\p"
# 984 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Good luck!$"
# 985 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 986 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_HereAreSomeRibbons:
# 987 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Here are some RIBBONS for beating\n"
# 988 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "seven tough TRAINERS in a row.\p"
# 989 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "{PLAYER} received some RIBBONS!$"
# 990 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 991 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_PutRibbonOnMons:
# 992 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "{PLAYER} put the RIBBONS on\n"
# 993 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the challenger POKéMON.$"
# 994 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 995 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_DescribeFeelingsAboutBattleTower:
# 996 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me, do you have a moment?\p"
# 997 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Can you describe your feelings when\n"
# 998 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you're about to begin a BATTLE TOWER\l"
# 999 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "match, or when you've either won or\l"
# 1000 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "lost a match?$"
# 1001 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1002 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FeelWhatWhenYouBegin:
# 1003 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Okay, what are your feelings when\n"
# 1004 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you're about to begin a match?$"
# 1005 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1006 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FeelWhatWhenYouveWon:
# 1007 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "What do you feel when you've won\n"
# 1008 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "a match?$"
# 1009 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1010 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FeelWhatWhenYouveLost:
# 1011 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Can I hear about your feelings when\n"
# 1012 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you have lost a match?$"
# 1013 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1014 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_DontThinkMuchAboutIt:
# 1015 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Oh, so you don't think much about it?\n"
# 1016 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You're one cool customer.$"
# 1017 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1018 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ChangedYourMind:
# 1019 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Hunh? You changed your mind?\n"
# 1020 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I guess you're fickle.$"
# 1021 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1022 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ThatsHowYouFeel:
# 1023 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Okay, so that's how you feel?\n"
# 1024 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "That's quite original.\p"
# 1025 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Thanks!$"
# 1026 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1027 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WinsInRowRecorded:
# 1028 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The number of matches you win in a row\n"
# 1029 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "is recorded.\p"
# 1030 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I'd better not get beaten in\n"
# 1031 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "an embarrassing way!$"
# 1032 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1033 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_CanLeaveUntilLossOrSevenWins:
# 1034 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Once you've entered the BATTLE TOWER,\n"
# 1035 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you can't leave until you either lose\l"
# 1036 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "or you beat seven TRAINERS in a row.\p"
# 1037 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You'd best be certain that you're up\n"
# 1038 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to the challenge.$"
# 1039 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1040 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1041 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_DoubleBattleRoomConstruction:
# 1042 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Welcome to the BATTLE TOWER\n"
# 1043 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "DOUBLE BATTLE CORNER!\p"
# 1044 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Unfortunately, the BATTLE ROOMS\n"
# 1045 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "are still under construction.\p"
# 1046 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please come back when the work\n"
# 1047 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "is completed.$"
# 1048 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1049 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1050 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_MultiBattleRoomConstruction:
# 1051 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Welcome to the BATTLE TOWER\n"
# 1052 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "MULTI BATTLE CORNER!\p"
# 1053 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Unfortunately, the BATTLE ROOMS\n"
# 1054 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "are still under construction.\p"
# 1055 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please come back when the work\n"
# 1056 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "is completed.$"
# 1057 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1058 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_LookForwardToAnotherChallenge:
# 1059 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "We look forward to seeing you on\n"
# 1060 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "another challenge!$"
# 1061 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1062 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WhichLevelMode:
# 1063 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE ROOM offers two levels\n"
# 1064 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "of challenge, Level 50 and Open Level.\l"
# 1065 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Which is your choice?$"
# 1066 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1067 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1068 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_PleaseSelectMons:
# 1069 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please select the POKéMON you wish\n"
# 1070 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to enter.$"
# 1071 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1072 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_OkayToSaveBeforeEntering:
# 1073 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Before entering a BATTLE ROOM, your\n"
# 1074 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "progress must be saved. Is that okay?$"
# 1075 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1076 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ShowYouToBattleRoom:
# 1077 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I will now show you to the\n"
# 1078 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "{STR_VAR_1} BATTLE ROOM.$"
# 1079 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1080 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_RecordLastMatch:
# 1081 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Shall I record your last BATTLE TOWER\n"
# 1082 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "match on your FRONTIER PASS?$"
# 1083 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1084 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1085 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50:
# 1086 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1087 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have {STR_VAR_2} eligible POKéMON.\p"
# 1088 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have {STR_VAR_2} different POKéMON\n"
# 1089 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "of Level 50 or less to enter.\p"
# 1090 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1091 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1092 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1093 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1094 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsEnd:
# 1095 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please come see me when you are ready.$"
# 1096 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1097 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1098 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpen:
# 1099 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1100 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have {STR_VAR_2} eligible POKéMON.\p"
# 1101 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have {STR_VAR_2} different POKéMON\n"
# 1102 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to enter.\p"
# 1103 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1104 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1105 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1106 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1107 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50Singles:
# 1108 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1109 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have three eligible POKéMON.\p"
# 1110 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have three different POKéMON\n"
# 1111 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "of Level 50 or less to enter.\p"
# 1112 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1113 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1114 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1115 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1116 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpenSingles:
# 1117 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1118 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have three eligible POKéMON.\p"
# 1119 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have three different POKéMON\n"
# 1120 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to enter.\p"
# 1121 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1122 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1123 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1124 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1125 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50Doubles:
# 1126 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1127 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have four eligible POKéMON.\p"
# 1128 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have four different POKéMON\n"
# 1129 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "of Level 50 or less to enter.\p"
# 1130 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1131 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1132 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1133 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1134 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpenDoubles:
# 1135 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1136 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have four eligible POKéMON.\p"
# 1137 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have four different POKéMON\n"
# 1138 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to enter.\p"
# 1139 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1140 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1141 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1142 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1143 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLv50Multis:
# 1144 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1145 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have two eligible POKéMON.\p"
# 1146 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have two different POKéMON\n"
# 1147 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "of Level 50 or less to enter.\p"
# 1148 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1149 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1150 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1151 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1152 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_NotEnoughValidMonsLvOpenMultis:
# 1153 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Excuse me!\p"
# 1154 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You don't have two eligible POKéMON.\p"
# 1155 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must have two different POKéMON\n"
# 1156 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to enter.\p"
# 1157 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "They also must be holding different\n"
# 1158 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "kinds of items.\p"
# 1159 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 1160 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1161 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WelcomSingleBattle:
# 1162 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Where the talents of TRAINERS\n"
# 1163 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "are put to the test!\p"
# 1164 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Welcome to the BATTLE TOWER!\p"
# 1165 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I am your guide to the SINGLE\n"
# 1166 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOMS.$"
# 1167 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1168 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_TakeSinglesChallenge:
# 1169 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Would you like to take the SINGLE\n"
# 1170 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOM challenge?$"
# 1171 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1172 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainSinglesChallenge:
# 1173 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE TOWER's SINGLE BATTLE\n"
# 1174 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "ROOMS are facilities for conducting\l"
# 1175 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "SINGLE BATTLES with three POKéMON.\p"
# 1176 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "There are many SINGLE BATTLE ROOMS\n"
# 1177 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "in the BATTLE TOWER for team battles.\p"
# 1178 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "In each of the SINGLE BATTLE ROOMS,\n"
# 1179 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "seven TRAINERS await your challenge.\p"
# 1180 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you manage to defeat all seven,\n"
# 1181 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you will earn Battle Points.\p"
# 1182 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you want to interrupt your\n"
# 1183 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "challenge, please save the game.\p"
# 1184 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you don't save before interrupting,\n"
# 1185 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you will be disqualified.$"
# 1186 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1187 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_SelectThreeMons:
# 1188 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Now please select the three POKéMON\n"
# 1189 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "that are to be entered.$"
# 1190 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1191 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WelcomeDoubleBattle:
# 1192 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Where the talents of TRAINERS\n"
# 1193 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "are put to the test!\p"
# 1194 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Welcome to the BATTLE TOWER!\p"
# 1195 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I am your guide to the DOUBLE\n"
# 1196 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOMS.$"
# 1197 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1198 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_TakeDoublesChallenge:
# 1199 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Would you like to take the DOUBLE\n"
# 1200 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOM challenge?$"
# 1201 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1202 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainDoublesChallenge:
# 1203 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE TOWER's DOUBLE BATTLE\n"
# 1204 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "ROOMS are facilities for conducting\l"
# 1205 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "DOUBLE BATTLES with four POKéMON.\p"
# 1206 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "There are many DOUBLE BATTLE ROOMS\n"
# 1207 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "in the BATTLE TOWER for team battles.\p"
# 1208 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "In each of the DOUBLE BATTLE ROOMS,\n"
# 1209 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "seven TRAINERS await your challenge.\p"
# 1210 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you manage to defeat all seven,\n"
# 1211 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you will earn Battle Points.\p"
# 1212 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you want to interrupt your\n"
# 1213 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "challenge, please save the game.\p"
# 1214 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you don't save before interrupting,\n"
# 1215 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you will be disqualified.$"
# 1216 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1217 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_PleaseSelectFourMons:
# 1218 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Now please select the four POKéMON\n"
# 1219 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "that are to be entered.$"
# 1220 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1221 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WelcomeMultiBattle:
# 1222 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Where the talents of TRAINERS\n"
# 1223 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "are put to the test!\p"
# 1224 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Welcome to the BATTLE TOWER!\p"
# 1225 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I am your guide to the MULTI\n"
# 1226 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOMS.$"
# 1227 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1228 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_TakeMultisChallenge:
# 1229 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Would you like to take the MULTI\n"
# 1230 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOM challenge?$"
# 1231 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1232 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainMultisChallenge:
# 1233 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE TOWER's MULTI BATTLE\n"
# 1234 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "ROOMS are facilities for conducting\l"
# 1235 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "MULTI BATTLES.\p"
# 1236 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "For MULTI BATTLES, you must partner\n"
# 1237 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "with a TRAINER in the TOWER and enter\l"
# 1238 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "with two POKéMON each.\p"
# 1239 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Inside the TOWER is a room named\n"
# 1240 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the BATTLE SALON where you may meet\l"
# 1241 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "other TRAINERS.\p"
# 1242 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "There, you must find a TRAINER to act\n"
# 1243 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "as your partner in MULTI BATTLES.\p"
# 1244 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Once you have partnered up, you will\n"
# 1245 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "be shown to a MULTI BATTLE ROOM.\p"
# 1246 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "In the MULTI BATTLE ROOM, seven\n"
# 1247 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "tag teams await your challenge.\p"
# 1248 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you manage to defeat all seven\n"
# 1249 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "teams, you will earn Battle Points.\p"
# 1250 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you want to interrupt your\n"
# 1251 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "challenge, please save the game.\p"
# 1252 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you don't save before interrupting,\n"
# 1253 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you will be disqualified.$"
# 1254 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1255 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_PleaseSelectTwoMons:
# 1256 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Now please select the two POKéMON\n"
# 1257 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "that are to be entered.$"
# 1258 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1259 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_WelcomeLinkMultiBattle:
# 1260 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Where the talents of TRAINERS\n"
# 1261 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "are put to the test!\p"
# 1262 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Welcome to the BATTLE TOWER!\p"
# 1263 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I am your guide to the LINK MULTI\n"
# 1264 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOMS.$"
# 1265 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1266 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_TakeLinkMultisChallenge:
# 1267 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Would you like to take the LINK MULTI\n"
# 1268 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE ROOM challenge?$"
# 1269 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1270 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainLinkMultisChallenge:
# 1271 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE TOWER's MULTI BATTLE\n"
# 1272 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "ROOMS are facilities for conducting\l"
# 1273 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "MULTI BATTLES with a friend.\p"
# 1274 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must link with your friend using\n"
# 1275 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Wireless Adapters or a Game Boy\l"
# 1276 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Advance Game Link cable.\p"
# 1277 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must partner with your friend and\n"
# 1278 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "enter two different kinds of POKéMON.\p"
# 1279 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "There are many MULTI BATTLE ROOMS\n"
# 1280 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "in the BATTLE TOWER for team battles.\p"
# 1281 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "In a MULTI BATTLE ROOM, seven\n"
# 1282 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "tag teams await you and your friend\l"
# 1283 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "to make a tag-team challenge.\p"
# 1284 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "If you manage to defeat all seven\n"
# 1285 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "teams, you will earn Battle Points.\p"
# 1286 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please beware that unlike other ROOMS,\n"
# 1287 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you may not interrupt your challenge.\p"
# 1288 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Once you start, you must battle seven\n"
# 1289 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "MULTI BATTLES in a row nonstop.$"
# 1290 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1291 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_PleaseSelectTwoMons2:
# 1292 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Now please select the two POKéMON\n"
# 1293 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "that are to be entered.$"
# 1294 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1295 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1296 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ChoseSameMonAsFriend:
# 1297 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You have chosen the same kind of\n"
# 1298 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "POKéMON as your friend.\p"
# 1299 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please choose two POKéMON different\n"
# 1300 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "from your friend's, match the level\l"
# 1301 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you wish to enter, and register again.$"
# 1302 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1303 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_LinkMultiOnlyForTwoPlayers:
# 1304 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The LINK MULTI BATTLE ROOM challenge\n"
# 1305 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "is only for two linked players.$"
# 1306 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1307 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FriendAlsoSelectedMon:
# 1308 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has also selected\n"
# 1309 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the POKéMON {STR_VAR_1}.$"
# 1310 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1311 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FriendAlsoSelectedMons:
# 1312 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has also selected the\n"
# 1313 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "POKéMON {STR_VAR_1} and {STR_VAR_2}.$"
# 1314 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1315 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FriendChoseDifferentLvlMode:
# 1316 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has chosen a different\n"
# 1317 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "battle level.$"
# 1318 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1319 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1320 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FriendChoseDifferentLvlModeSameMon:
# 1321 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has chosen a different\n"
# 1322 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "battle level.\p"
# 1323 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has also selected\n"
# 1324 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the POKéMON {STR_VAR_1}.$"
# 1325 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1326 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
@ Unused
# 1327 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_FriendChoseDifferentLvlModeSameMons:
# 1328 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has chosen a different\n"
# 1329 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "battle level.\p"
# 1330 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Your friend has also selected the\n"
# 1331 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "POKéMON {STR_VAR_1} and {STR_VAR_2}.$"
# 1332 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1333 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ChooseDifferentMonsMatchLvlMode:
# 1334 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please choose two POKéMON different\n"
# 1335 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "from your friend's, match the level\l"
# 1336 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "you wish to enter, and register again.$"
# 1337 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1338 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_SaveGameBeforeShowingIn:
# 1339 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "I will save the game before\n"
# 1340 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "showing you in. Please wait.$"
# 1341 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1342 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_CongratsDefeatedMaiden:
# 1343 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Congratulations!\n"
# 1344 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You have defeated the SALON MAIDEN\l"
# 1345 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "and swept seven TRAINERS!$"
# 1346 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1347 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_AwardYouTheseBattlePoints:
# 1348 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "In recognition of your infinite talent,\n"
# 1349 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "we award you these Battle Point(s).$"
# 1350 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1351 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_Text_ObtainedXBattlePoints:
# 1352 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "{PLAYER} obtained {STR_VAR_1} Battle Point(s).$"
# 1353 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1354 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_RulesAreListed:
# 1355 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE TOWER rules are listed.$"
# 1356 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1357 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ReadWhichHeading:
# 1358 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Which heading do you want to read?$"
# 1359 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1360 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainTowerRules:
# 1361 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE TOWER is a facility where\n"
# 1362 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "four types of battles are waged--\l"
# 1363 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "SINGLE BATTLE, DOUBLE BATTLE, MULTI\l"
# 1364 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "BATTLE, and LINK MULTI BATTLE.\p"
# 1365 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "For each of these types, there are\n"
# 1366 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "separate BATTLE ROOMS.\p"
# 1367 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Please speak with a guide offering\n"
# 1368 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the type of battle you wish to enter.$"
# 1369 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1370 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainMonRules:
# 1371 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Depending on the BATTLE ROOM you are\n"
# 1372 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "entering, you will be required to take\l"
# 1373 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "a certain number of POKéMON.\p"
# 1374 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The SINGLE BATTLE mode requires\n"
# 1375 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "three POKéMON.\p"
# 1376 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The DOUBLE BATTLE mode requires four,\n"
# 1377 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "and the MULTI modes both require two.$"
# 1378 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1379 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainSalonRules:
# 1380 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The BATTLE SALON is where you must\n"
# 1381 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "find a partner to form a tag team for\l"
# 1382 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the MULTI BATTLE ROOM challenge.\p"
# 1383 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Choose the best partner for you by\n"
# 1384 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "examining other TRAINERS'\l"
# 1385 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "POKéMON and their moves.\p"
# 1386 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You may choose a new tag partner\n"
# 1387 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "after winning seven straight matches.$"
# 1388 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"

# 1389 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
BattleFrontier_BattleTowerLobby_Text_ExplainMultiLinkRules:
# 1390 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "The LINK MULTI BATTLE Mode is for two\n"
# 1391 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "friends to mount a challenge together.\p"
# 1392 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You and your friend must be linked with\n"
# 1393 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "Wireless Adapters or a GBA Game Link\l"
# 1394 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "cable.\p"
# 1395 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You must choose two POKéMON at\n"
# 1396 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "the registration counter.\p"
# 1397 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "These POKéMON must be different\n"
# 1398 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "from those of your friend.\p"
# 1399 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "You may not interrupt this challenge\n"
# 1400 "data/maps/BattleFrontier_BattleTowerLobby/scripts.pory"
	.string "in the middle, unlike other modes.$"
