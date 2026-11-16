# 1 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 2 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_MapScripts::
# 3 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattlePyramidLobby_OnFrame
# 4 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, BattleFrontier_BattleDomeLobby_OnWarp
# 5 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.byte 0
# 6 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 7 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Unused. Pyramid uses Dome's OnWarp (presumably by mistake). Their effects are identical
# 8 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_OnWarp:
# 9 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, BattleFrontier_BattlePyramidLobby_EventScript_TurnPlayerNorth
# 10 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.2byte 0
# 11 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 12 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_TurnPlayerNorth:
# 13 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_1, 1
# 14 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 15 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 16 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 17 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_OnFrame:
# 18 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, 0, BattleFrontier_BattlePyramidLobby_EventScript_GetChallengeStatus
# 19 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING, BattleFrontier_BattlePyramidLobby_EventScript_QuitWithoutSaving
# 20 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_PAUSED, BattleFrontier_BattlePyramidLobby_EventScript_ResumeChallenge
# 21 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_WON, BattleFrontier_BattlePyramidLobby_EventScript_WonChallenge
# 22 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST, BattleFrontier_BattlePyramidLobby_EventScript_LostChallenge
# 23 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.2byte 0
# 24 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 25 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GetChallengeStatus::
# 26 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_getstatus
# 27 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 28 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 29 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_QuitWithoutSaving::
# 30 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lockall
# 31 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_DidntSaveBeforeQuittingTakeBag
# 32 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 33 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	playse SE_EXP_MAX
# 34 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitse
# 35 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	closemessage
# 36 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_set PYRAMID_DATA_WIN_STREAK, 0
# 37 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_set PYRAMID_DATA_WIN_STREAK_ACTIVE, FALSE
# 38 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 39 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 40 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	releaseall
# 41 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 42 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 43 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_WonChallenge::
# 44 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lockall
# 45 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_isbrain
# 46 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattlePyramidLobby_EventScript_DefeatedKing
# 47 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_YouveConqueredPyramid, MSGBOX_DEFAULT
# 48 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_GiveBattlePoints
# 49 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 50 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_DefeatedKing::
# 51 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_YouveDefeatedPyramidKing, MSGBOX_DEFAULT
# 52 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GiveBattlePoints::
# 53 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special DoBattlePyramidMonsHaveHeldItem
# 54 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call_if_eq VAR_RESULT, TRUE, BattleFrontier_BattlePyramidLobby_EventScript_StoreHeldItemsInPyramidBag
# 55 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	clearflag FLAG_STORING_ITEMS_IN_PYRAMID_BAG
# 56 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_checkairshow
# 57 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special LoadPlayerParty
# 58 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_clearhelditems
# 59 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special HealPlayerParty
# 60 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 61 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_UsedBattleBagWillBeKept
# 62 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 63 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	playse SE_EXP_MAX
# 64 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitse
# 65 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_GiveYouTheseBattlePoints, MSGBOX_DEFAULT
# 66 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_givepoints
# 67 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_Text_ObtainedXBattlePoints, MSGBOX_GETPOINTS
# 68 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_RecordResultsWait
# 69 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 70 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_setprize
# 71 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_save 0
# 72 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	playse SE_SAVE
# 73 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitse
# 74 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_LookForwardToNextChallenge, MSGBOX_DEFAULT
# 75 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	closemessage
# 76 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 77 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	releaseall
# 78 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 79 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 80 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_LostChallenge::
# 81 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_checkairshow
# 82 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special LoadPlayerParty
# 83 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_clearhelditems
# 84 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special HealPlayerParty
# 85 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 86 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lockall
# 87 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_DisappointingHereIsBag
# 88 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 89 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	playse SE_EXP_MAX
# 90 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitse
# 91 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_RecordResultsWait
# 92 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 93 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_set PYRAMID_DATA_WIN_STREAK_ACTIVE, FALSE
# 94 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_save 0
# 95 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	playse SE_SAVE
# 96 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitse
# 97 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_LookForwardToNextChallenge, MSGBOX_DEFAULT
# 98 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	closemessage
# 99 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 100 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	releaseall
# 101 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 102 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 103 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ResumeChallenge::
# 104 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_EnterChallenge
# 105 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 106 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_Attendant::
# 107 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lock
# 108 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	faceplayer
# 109 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_PYRAMID
# 110 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES
# 111 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special SavePlayerParty
# 112 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_WelcomeToBattlePyramid, MSGBOX_DEFAULT
# 113 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_AskTakeChallenge::
# 114 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_EmbarkOnChallenge
# 115 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 116 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 117 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 118 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 0, BattleFrontier_BattlePyramidLobby_EventScript_TryEnterChallenge
# 119 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 1, BattleFrontier_BattlePyramidLobby_EventScript_ExplainChallenge
# 120 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 2, BattleFrontier_BattlePyramidLobby_EventScript_CancelChallenge
# 121 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePyramidLobby_EventScript_CancelChallenge
# 122 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 123 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_TryEnterChallenge::
# 124 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_WhichLevelMode
# 125 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 126 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 127 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 128 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattlePyramidLobby_EventScript_CancelChallenge
# 129 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePyramidLobby_EventScript_CancelChallenge
# 130 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_checkineligible
# 131 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, BattleFrontier_BattlePyramidLobby_EventScript_NotEnoughValidMons
# 132 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, VAR_RESULT
# 133 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_SelectThreeMons, MSGBOX_DEFAULT
# 134 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 135 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	callnative RemoveFollowingPokemon
# 136 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 137 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 138 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_PARTY_SIZE
# 139 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 140 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePyramidLobby_EventScript_LoadPartyAndCancelChallenge
# 141 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_OkayToSaveBeforeChallenge, MSGBOX_YESNO
# 142 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 143 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case NO, BattleFrontier_BattlePyramidLobby_EventScript_LoadPartyAndCancelChallenge
# 144 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case YES, BattleFrontier_BattlePyramidLobby_EventScript_SaveBeforeChallenge
# 145 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePyramidLobby_EventScript_LoadPartyAndCancelChallenge
# 146 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 147 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_SaveBeforeChallenge::
# 148 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 149 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 150 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_init
# 151 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_set PYRAMID_DATA_WIN_STREAK_ACTIVE, TRUE
# 152 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING
# 153 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 154 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_seedfloor
# 155 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_settrainers
# 156 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special LoadPlayerParty
# 157 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	closemessage
# 158 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	delay 2
# 159 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 160 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 161 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePyramidLobby_EventScript_CancelChallengeSaveFailed
# 162 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_EnterChallenge::
# 163 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special SavePlayerParty
# 164 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_setpartyorder FRONTIER_PARTY_SIZE
# 165 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_ShowYouIntoPyramid, MSGBOX_DEFAULT
# 166 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	closemessage
# 167 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call BattleFrontier_BattlePyramidLobby_EventScript_WalkToPanelAndReceiveBag
# 168 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 169 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_RESULT, 0
# 170 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special HealPlayerParty
# 171 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_PYRAMID_FLOOR, 1, 1
# 172 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 173 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitstate
# 174 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 175 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 176 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ExplainChallenge::
# 177 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_ExplainBattlePyramid, MSGBOX_DEFAULT
# 178 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_AskTakeChallenge
# 179 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 180 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_NotEnoughValidMons::
# 181 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 182 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case FRONTIER_LVL_50, BattleFrontier_BattlePyramidLobby_EventScript_NotEnoughValidMonsLv50
# 183 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case FRONTIER_LVL_OPEN, BattleFrontier_BattlePyramidLobby_EventScript_NotEnoughValidMonsLvOpen
# 184 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 185 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_NotEnoughValidMonsLv50::
# 186 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsLv50, MSGBOX_DEFAULT
# 187 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 188 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 189 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_EndCancelChallenge
# 190 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 191 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_NotEnoughValidMonsLvOpen::
# 192 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsLvOpen, MSGBOX_DEFAULT
# 193 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 194 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 195 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_EndCancelChallenge
# 196 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 197 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_CancelChallengeSaveFailed::
# 198 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 199 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_CancelChallenge
# 200 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 201 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_LoadPartyAndCancelChallenge::
# 202 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special LoadPlayerParty
# 203 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 204 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_CancelChallenge::
# 205 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_AwaitFutureChallenge, MSGBOX_DEFAULT
# 206 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_EndCancelChallenge::
# 207 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	release
# 208 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 209 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 210 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintGiver::
# 211 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lockall
# 212 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	applymovement LOCALID_PYRAMID_LOBBY_HINT_GIVER, Common_Movement_FacePlayer
# 213 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmovement 0
# 214 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_TellYouWhatMisfortunesAwait, MSGBOX_DEFAULT
# 215 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	call BattleFrontier_BattlePyramidLobby_EventScript_GiveHint
# 216 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_BelieveMyFortunesOrNot, MSGBOX_DEFAULT
# 217 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	releaseall
# 218 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 219 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 220 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GiveHint::
# 221 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 222 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 223 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case FRONTIER_LVL_50, BattleFrontier_BattlePyramidLobby_EventScript_GiveHintLv50
# 224 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case FRONTIER_LVL_OPEN, BattleFrontier_BattlePyramidLobby_EventScript_GiveHintLvOpen
# 225 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattlePyramidLobby_EventScript_NoHint
# 226 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePyramidLobby_EventScript_NoHint
# 227 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 228 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 229 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Shouldnt occur
# 230 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_NoHint::
# 231 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 232 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 233 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GiveHintLv50::
# 234 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_Aah, MSGBOX_DEFAULT
# 235 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_get PYRAMID_DATA_WIN_STREAK_ACTIVE_50
# 236 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_ne VAR_RESULT, FALSE, BattleFrontier_BattlePyramidLobby_EventScript_GiveHintGetLv50Streak
# 237 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_RESULT, 0
# 238 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_DoHintComment
# 239 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 240 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 241 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GiveHintGetLv50Streak::
# 242 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_get PYRAMID_DATA_WIN_STREAK_50
# 243 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_DoHintComment
# 244 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 245 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 246 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GiveHintLvOpen::
# 247 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_Aah, MSGBOX_DEFAULT
# 248 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_get PYRAMID_DATA_WIN_STREAK_ACTIVE_OPEN
# 249 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_ne VAR_RESULT, FALSE, BattleFrontier_BattlePyramidLobby_EventScript_GiveHintGetLvOpenStreak
# 250 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setvar VAR_RESULT, 0
# 251 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_DoHintComment
# 252 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 253 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 254 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_GiveHintGetLvOpenStreak::
# 255 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_get PYRAMID_DATA_WIN_STREAK_OPEN
# 256 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_DoHintComment
# 257 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 258 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 259 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_DoHintComment::
# 260 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 261 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special GetBattlePyramidHint
# 262 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 263 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 0, BattleFrontier_BattlePyramidLobby_EventScript_HintParalysis
# 264 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 1, BattleFrontier_BattlePyramidLobby_EventScript_HintPoison
# 265 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 2, BattleFrontier_BattlePyramidLobby_EventScript_HintBurn
# 266 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 3, BattleFrontier_BattlePyramidLobby_EventScript_HintPPWaste
# 267 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 4, BattleFrontier_BattlePyramidLobby_EventScript_HintLevitate
# 268 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 5, BattleFrontier_BattlePyramidLobby_EventScript_HintTrapAbility
# 269 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 6, BattleFrontier_BattlePyramidLobby_EventScript_HintIce
# 270 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 7, BattleFrontier_BattlePyramidLobby_EventScript_HintExplosion
# 271 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 8, BattleFrontier_BattlePyramidLobby_EventScript_HintPsychic
# 272 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 9, BattleFrontier_BattlePyramidLobby_EventScript_HintRock
# 273 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 10, BattleFrontier_BattlePyramidLobby_EventScript_HintFighting
# 274 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 11, BattleFrontier_BattlePyramidLobby_EventScript_HintWeather
# 275 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 12, BattleFrontier_BattlePyramidLobby_EventScript_HintBug
# 276 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 13, BattleFrontier_BattlePyramidLobby_EventScript_HintDark
# 277 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 14, BattleFrontier_BattlePyramidLobby_EventScript_HintWater
# 278 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 15, BattleFrontier_BattlePyramidLobby_EventScript_HintGhost
# 279 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 16, BattleFrontier_BattlePyramidLobby_EventScript_HintSteel
# 280 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 17, BattleFrontier_BattlePyramidLobby_EventScript_HintFlyingDragon
# 281 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 18, BattleFrontier_BattlePyramidLobby_EventScript_HintStoneEvolve
# 282 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 19, BattleFrontier_BattlePyramidLobby_EventScript_HintNormal
# 283 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 284 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 285 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintParalysis::
# 286 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintParalysis, MSGBOX_DEFAULT
# 287 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 288 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 289 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintPoison::
# 290 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintPoison, MSGBOX_DEFAULT
# 291 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 292 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 293 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintBurn::
# 294 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintBurn, MSGBOX_DEFAULT
# 295 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 296 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 297 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintPPWaste::
# 298 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintPPWaste, MSGBOX_DEFAULT
# 299 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 300 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 301 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintLevitate::
# 302 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintLevitate, MSGBOX_DEFAULT
# 303 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 304 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 305 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintTrapAbility::
# 306 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintTrapAbility, MSGBOX_DEFAULT
# 307 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 308 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 309 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintIce::
# 310 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintIce, MSGBOX_DEFAULT
# 311 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 312 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 313 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintExplosion::
# 314 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintExplosion, MSGBOX_DEFAULT
# 315 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 316 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 317 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintPsychic::
# 318 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintPsychic, MSGBOX_DEFAULT
# 319 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 320 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 321 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintRock::
# 322 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintRock, MSGBOX_DEFAULT
# 323 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 324 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 325 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintFighting::
# 326 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintFighting, MSGBOX_DEFAULT
# 327 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 328 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 329 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintWeather::
# 330 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintWeather, MSGBOX_DEFAULT
# 331 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 332 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 333 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintBug::
# 334 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintBug, MSGBOX_DEFAULT
# 335 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 336 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 337 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintDark::
# 338 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintDark, MSGBOX_DEFAULT
# 339 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 340 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 341 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintWater::
# 342 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintWater, MSGBOX_DEFAULT
# 343 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 344 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 345 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintGhost::
# 346 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintGhost, MSGBOX_DEFAULT
# 347 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 348 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 349 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintSteel::
# 350 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintSteel, MSGBOX_DEFAULT
# 351 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 352 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 353 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintFlyingDragon::
# 354 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintFlyingDragon, MSGBOX_DEFAULT
# 355 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 356 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 357 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintStoneEvolve::
# 358 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintStoneEvolve, MSGBOX_DEFAULT
# 359 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 360 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 361 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HintNormal::
# 362 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HintNormal, MSGBOX_DEFAULT
# 363 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 364 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 365 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ShowResults::
# 366 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lockall
# 367 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	frontier_results FRONTIER_FACILITY_PYRAMID
# 368 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitbuttonpress
# 369 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special RemoveRecordsWindow
# 370 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	releaseall
# 371 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 372 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 373 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_WalkToPanelAndReceiveBag::
# 374 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	applymovement LOCALID_PYRAMID_LOBBY_ATTENDANT, BattleFrontier_BattlePyramidLobby_Movement_AttendantWalkToPanel
# 375 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattlePyramidLobby_Movement_PlayerWalkToPanel
# 376 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmovement 0
# 377 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_WeWillHoldBagForSafekeeping, MSGBOX_DEFAULT
# 378 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	pyramid_get PYRAMID_DATA_WIN_STREAK
# 379 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePyramidLobby_EventScript_ReceiveNewBattleBag
# 380 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_PleaseTakePreviousBattleBag, MSGBOX_DEFAULT
# 381 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_ReceiveBattleBag
# 382 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 383 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ReceiveNewBattleBag::
# 384 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_PleaseTakeThisBattleBag, MSGBOX_DEFAULT
# 385 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ReceiveBattleBag::
# 386 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_ExchangedBagForBattleBag
# 387 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 388 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	playse SE_EXP_MAX
# 389 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitse
# 390 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_StepOnFloorPanel, MSGBOX_DEFAULT
# 391 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	closemessage
# 392 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	applymovement LOCALID_PYRAMID_LOBBY_ATTENDANT, BattleFrontier_BattlePyramidLobby_Movement_AttendantMoveAside
# 393 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmovement 0
# 394 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattlePyramidLobby_Movement_PlayerStepOnPanel
# 395 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmovement 0
# 396 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 397 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 398 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Movement_AttendantWalkToPanel:
# 399 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 400 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 401 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 402 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 403 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 404 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 405 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 406 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	face_down
# 407 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	step_end
# 408 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 409 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Movement_PlayerWalkToPanel:
# 410 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 411 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 412 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 413 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 414 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 415 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 416 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 417 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	step_end
# 418 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 419 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Movement_AttendantMoveAside:
# 420 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_right
# 421 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	face_left
# 422 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	step_end
# 423 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 424 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Movement_PlayerStepOnPanel:
# 425 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 426 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	walk_up
# 427 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	step_end
# 428 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 429 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_StoreHeldItemsInPyramidBag::
# 430 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_MonHoldingItemCannotTake, MSGBOX_DEFAULT
# 431 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	setflag FLAG_STORING_ITEMS_IN_PYRAMID_BAG
# 432 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special TryStoreHeldItemsInPyramidBag
# 433 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePyramidLobby_EventScript_HeldItemsStoredInPyramidBag
# 434 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_BagCannotHoldPickItemsToKeep
# 435 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 436 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_PickItemsToKeep
# 437 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 438 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 439 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_HeldItemsStoredInPyramidBag::
# 440 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_HeldItemsMovedToBag, MSGBOX_DEFAULT
# 441 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 442 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 443 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ When exiting Battle Pyramid with a full pyramid bag and held items the player must select to keep/toss party held items and make room for any kept items by tossing from the pyramid bag
# 444 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_PickItemsToKeep::
# 445 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	multichoice 17, 6, MULTI_FRONTIER_ITEM_CHOOSE, FALSE
# 446 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 447 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 0, BattleFrontier_BattlePyramidLobby_EventScript_PickItemsFromBag
# 448 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 1, BattleFrontier_BattlePyramidLobby_EventScript_PickItemsFromParty
# 449 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 2, BattleFrontier_BattlePyramidLobby_EventScript_ExitPickItems
# 450 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePyramidLobby_EventScript_ExitPickItems
# 451 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 452 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 453 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_PickItemsFromBag::
# 454 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special ChooseItemsToTossFromPyramidBag
# 455 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_PickItemsToKeep
# 456 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 457 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_PickItemsToKeep
# 458 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 459 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 460 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_PickItemsFromParty::
# 461 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special BattlePyramidChooseMonHeldItems
# 462 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_PickItemsToKeep
# 463 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 464 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_PickItemsToKeep
# 465 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 466 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 467 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ExitPickItems::
# 468 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	special DoBattlePyramidMonsHaveHeldItem
# 469 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattlePyramidLobby_EventScript_PartyStillHasHeldItems
# 470 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	return
# 471 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 472 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_PartyStillHasHeldItems::
# 473 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_LeastOneMonHoldingItem, MSGBOX_DEFAULT
# 474 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_PickItemsToKeep
# 475 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 476 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_PickItemsToKeep
# 477 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 478 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 479 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_Woman::
# 480 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_TrainersNoticeRunning, MSGBOX_NPC
# 481 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 482 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 483 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_FatMan::
# 484 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_LostLotOfItems, MSGBOX_NPC
# 485 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 486 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 487 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_RulesBoard::
# 488 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	lockall
# 489 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_RulesAreListed, MSGBOX_DEFAULT
# 490 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_ReadRulesBoard
# 491 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 492 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 493 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ReadRulesBoard::
# 494 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	message BattleFrontier_BattlePyramidLobby_Text_ReadWhichHeading
# 495 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	waitmessage
# 496 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	multichoice 15, 2, MULTI_BATTLE_PYRAMID_RULES, FALSE
# 497 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	switch VAR_RESULT
# 498 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 0, BattleFrontier_BattlePyramidLobby_EventScript_RulesPokemon
# 499 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 1, BattleFrontier_BattlePyramidLobby_EventScript_RulesTrainers
# 500 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 2, BattleFrontier_BattlePyramidLobby_EventScript_RulesMaze
# 501 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 3, BattleFrontier_BattlePyramidLobby_EventScript_RulesBag
# 502 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case 4, BattleFrontier_BattlePyramidLobby_EventScript_ExitRules
# 503 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePyramidLobby_EventScript_ExitRules
# 504 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 505 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 506 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_RulesPokemon::
# 507 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_ExplainMonRules, MSGBOX_DEFAULT
# 508 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_ReadRulesBoard
# 509 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 510 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 511 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_RulesTrainers::
# 512 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_ExplainTrainerRules, MSGBOX_DEFAULT
# 513 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_ReadRulesBoard
# 514 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 515 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 516 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_RulesMaze::
# 517 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_ExplainMazeRules, MSGBOX_DEFAULT
# 518 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_ReadRulesBoard
# 519 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 520 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 521 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_RulesBag::
# 522 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	msgbox BattleFrontier_BattlePyramidLobby_Text_ExplainBagRules, MSGBOX_DEFAULT
# 523 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	goto BattleFrontier_BattlePyramidLobby_EventScript_ReadRulesBoard
# 524 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 525 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 526 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_EventScript_ExitRules::
# 527 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	releaseall
# 528 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	end
# 529 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 530 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_WelcomeToBattlePyramid:
# 531 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Where the courage of TRAINERS\n"
# 532 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "is put to the test!\p"
# 533 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Welcome to the BATTLE PYRAMID!\p"
# 534 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I am your guide to\n"
# 535 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the Battle Quest.$"
# 536 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 537 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_EmbarkOnChallenge:
# 538 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Have you the courage to embark on\n"
# 539 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the Battle Quest challenge?$"
# 540 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 541 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_AwaitFutureChallenge:
# 542 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "We await your challenge in the future!$"
# 543 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 544 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ExplainBattlePyramid:
# 545 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The Battle Quest is a battling\n"
# 546 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "event in which you must explore\l"
# 547 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the PYRAMID and try to reach the top.\p"
# 548 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "In the PYRAMID are seven floors of\n"
# 549 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "mazes, all of them filled with not only\l"
# 550 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "skilled TRAINERS but also wild POKéMON.\p"
# 551 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You must enter with three POKéMON,\n"
# 552 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "none of them holding an item.\p"
# 553 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "On your ascent, you will be provided\n"
# 554 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "with a BATTLE BAG for items.\p"
# 555 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "If you fail in your challenge, any item\n"
# 556 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "placed in the BATTLE BAG disappears.\p"
# 557 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "If you want to interrupt your\n"
# 558 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "challenge, you must select “REST”\l"
# 559 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "and save the game.\p"
# 560 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "If you don't save before interrupting,\n"
# 561 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "you will be disqualified.$"
# 562 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 563 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_WhichLevelMode:
# 564 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The PYRAMID offers two courses,\n"
# 565 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Level 50 and Open Level.\l"
# 566 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Which will you enter?$"
# 567 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 568 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_SelectThreeMons:
# 569 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Very good. Now, please select the three\n"
# 570 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "POKéMON you wish to accompany you.$"
# 571 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 572 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsLvOpen:
# 573 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "A slight problem, adventurer!\p"
# 574 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You seem to not have the three\n"
# 575 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "POKéMON qualified for the challenge.\p"
# 576 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Please also remember to take all\n"
# 577 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "items from your POKéMON.\p"
# 578 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 579 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 580 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsLv50:
# 581 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "A slight problem, adventurer!\p"
# 582 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You seem to not have the three\n"
# 583 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "POKéMON qualified for the challenge.\p"
# 584 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The three POKéMON must be different\n"
# 585 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "and each no higher than Level 50.\p"
# 586 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Please also remember to take all\n"
# 587 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "items from your POKéMON.\p"
# 588 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 589 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 590 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_NotEnoughValidMonsEnd:
# 591 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "When you are ready, please have\n"
# 592 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "a word with me.$"
# 593 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 594 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_OkayToSaveBeforeChallenge:
# 595 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Before you enter the BATTLE PYRAMID,\n"
# 596 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the game must be saved. Is that okay?$"
# 597 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 598 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ShowYouIntoPyramid:
# 599 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Very good. I will now show you into\n"
# 600 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the BATTLE PYRAMID.$"
# 601 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 602 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_WeWillHoldBagForSafekeeping:
# 603 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "We will hold your BAG for safekeeping,\n"
# 604 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER}, while you are exploring.$"
# 605 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 606 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_PleaseTakePreviousBattleBag:
# 607 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "In exchange, please take this BATTLE\n"
# 608 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "BAG, the one you used previously.$"
# 609 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 610 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_PleaseTakeThisBattleBag:
# 611 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "In exchange, please take this\n"
# 612 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "BATTLE BAG.$"
# 613 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 614 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ExchangedBagForBattleBag:
# 615 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER} exchanged the BAG for\n"
# 616 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the BATTLE BAG.$"
# 617 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 618 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_StepOnFloorPanel:
# 619 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "When you step on this floor panel,\n"
# 620 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "you will be transported to a higher\l"
# 621 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "floor in the PYRAMID.\p"
# 622 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I hope for your sake that your\n"
# 623 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "quest goes safely!$"
# 624 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 625 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_DidntSaveBeforeQuittingTakeBag:
# 626 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "A major problem, explorer!\p"
# 627 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You did not save before ending\n"
# 628 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "your challenge the last time.\p"
# 629 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Consequently, your challenge has\n"
# 630 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "been disqualified, I'm sorry to say.\p"
# 631 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Here is the BAG we've been holding\n"
# 632 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "for you.\p"
# 633 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER} got the BAG back.$"
# 634 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 635 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_YouveConqueredPyramid:
# 636 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Excellent to see you back!\p"
# 637 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You've conquered the PYRAMID!\n"
# 638 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "How splendid!$"
# 639 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 640 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_MonHoldingItemCannotTake:
# 641 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Ah, a slight problem.\p"
# 642 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "At least one POKéMON is holding\n"
# 643 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "an item.\p"
# 644 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I'm sorry to say, items obtained in\n"
# 645 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the PYRAMID cannot be taken away.$"
# 646 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 647 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HeldItemsMovedToBag:
# 648 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "All items held by your POKéMON will be\n"
# 649 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "moved to your BATTLE BAG, {PLAYER}.$"
# 650 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 651 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_BagCannotHoldPickItemsToKeep:
# 652 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The BATTLE BAG cannot hold all your\n"
# 653 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "items, I'm sorry to say.\p"
# 654 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Please pick the items you'll keep in the\n"
# 655 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "BATTLE BAG, and with your POKéMON.$"
# 656 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 657 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_LeastOneMonHoldingItem:
# 658 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "At least one POKéMON is still\n"
# 659 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "holding an item.$"
# 660 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 661 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_PickItemsToKeep:
# 662 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Please pick the items you'll keep in the\n"
# 663 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "BATTLE BAG, and with your POKéMON.$"
# 664 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 665 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Unused
# 666 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ReturnedEverythingMonsHeld:
# 667 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER} returned everything that\n"
# 668 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the POKéMON held.$"
# 669 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 670 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_UsedBattleBagWillBeKept:
# 671 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The BATTLE BAG you used will be kept\n"
# 672 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "in readiness for your next challenge.\p"
# 673 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER} turned the BATTLE BAG over\n"
# 674 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "for the BAG's return.$"
# 675 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 676 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_RecordResultsWait:
# 677 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I must record your results.\n"
# 678 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Please wait.$"
# 679 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 680 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Unused
# 681 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ForConqueringPyramidTakeThis:
# 682 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "As a memento for conquering\n"
# 683 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the BATTLE PYRAMID, please take this.$"
# 684 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 685 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Unused
# 686 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ReceivedPrizeItem:
# 687 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER} received the prize\n"
# 688 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{STR_VAR_1}.$"
# 689 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 690 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Unused
# 691 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_BagIsFull:
# 692 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…Ah…\n"
# 693 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Your BAG appears to be filled.\p"
# 694 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Please return after you've organized\n"
# 695 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "your BAG's contents.$"
# 696 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 697 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_DisappointingHereIsBag:
# 698 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "How disappointing for you…\p"
# 699 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Here is the BAG we've been holding\n"
# 700 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "for you.\p"
# 701 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "{PLAYER} got the BAG back.$"
# 702 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 703 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_LookForwardToNextChallenge:
# 704 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "We look forward to your\n"
# 705 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "next challenge!$"
# 706 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 707 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
@ Unused
# 708 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HereIsPrize:
# 709 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "We have been looking forward to\n"
# 710 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "your arrival!\p"
# 711 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Here is your prize for conquering\n"
# 712 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the PYRAMID.$"
# 713 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 714 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_TellYouWhatMisfortunesAwait:
# 715 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Welcome…\p"
# 716 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I shall be pleased to tell you what\n"
# 717 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "misfortunes await in the PYRAMID…$"
# 718 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 719 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_Aah:
# 720 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "… … … … … …\n"
# 721 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "… … … … … …\p"
# 722 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "… … … … … …\n"
# 723 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Aah!$"
# 724 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 725 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintParalysis:
# 726 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see a shower of sparks…\p"
# 727 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And in it, I see your POKéMON\n"
# 728 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "struggling with paralysis…$"
# 729 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 730 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintPoison:
# 731 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see poison…\p"
# 732 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 733 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from the effects of poison…$"
# 734 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 735 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintBurn:
# 736 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see bright red flames…\p"
# 737 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 738 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from burns…$"
# 739 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 740 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintPPWaste:
# 741 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I sense the tremendous pressure of\n"
# 742 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "unrequited anger…\p"
# 743 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "It is a curse…\p"
# 744 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON drained of\n"
# 745 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Power Points and having no recourse\l"
# 746 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "but to use STRUGGLE…$"
# 747 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 748 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintLevitate:
# 749 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see POKéMON loftily airborne…\p"
# 750 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON frustrated\n"
# 751 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "by powerless GROUND-type moves…$"
# 752 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 753 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintTrapAbility:
# 754 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I sense terrific energy rising from\n"
# 755 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the ground below…\p"
# 756 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON unable to\n"
# 757 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "escape the power's clutches…$"
# 758 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 759 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintIce:
# 760 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see ICE-type POKéMON…\p"
# 761 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON fighting\n"
# 762 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the freezing effects of ice…$"
# 763 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 764 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintExplosion:
# 765 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see a flurry of moves that imperil\n"
# 766 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the user…\p"
# 767 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON falling\n"
# 768 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "to them…$"
# 769 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 770 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintPsychic:
# 771 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see PSYCHIC-type POKéMON…\p"
# 772 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON in torment\n"
# 773 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from PSYCHIC moves…$"
# 774 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 775 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintRock:
# 776 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see ROCK-type POKéMON…\p"
# 777 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 778 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from ROCK moves…$"
# 779 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 780 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintFighting:
# 781 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see FIGHTING-type POKéMON…\p"
# 782 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON pummeled\n"
# 783 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "by FIGHTING moves…$"
# 784 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 785 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintWeather:
# 786 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "RAIN DANCE… SUNNY DAY…\n"
# 787 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "SANDSTORM… HAIL…\p"
# 788 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see POKéMON that become stronger\n"
# 789 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "with the weather…\p"
# 790 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON confounded\n"
# 791 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "by different types of moves…$"
# 792 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 793 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintBug:
# 794 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see BUG-type POKéMON…\p"
# 795 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 796 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from different kinds of attacks…$"
# 797 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 798 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintDark:
# 799 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see DARK-type POKéMON…\p"
# 800 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 801 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from DARK-type moves…$"
# 802 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 803 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintWater:
# 804 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see WATER-type POKéMON…\p"
# 805 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 806 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from WATER-type moves…$"
# 807 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 808 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintGhost:
# 809 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see GHOST-type POKéMON…\p"
# 810 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 811 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from GHOST-type moves…$"
# 812 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 813 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintSteel:
# 814 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see STEEL-type POKéMON…\p"
# 815 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 816 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from enormously powerful moves…$"
# 817 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 818 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintFlyingDragon:
# 819 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see flying POKéMON…\p"
# 820 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 821 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from enormously powerful moves…$"
# 822 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 823 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintStoneEvolve:
# 824 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see those that have evolved from\n"
# 825 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the power of stones…\p"
# 826 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I also sense fire, water,\n"
# 827 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "and electricity…\p"
# 828 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 829 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from those three powers…$"
# 830 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 831 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_HintNormal:
# 832 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I see NORMAL-type POKéMON…\p"
# 833 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "…And, I see your POKéMON suffering\n"
# 834 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "from enormously powerful moves…$"
# 835 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 836 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_BelieveMyFortunesOrNot:
# 837 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Whether you believe my fortunes\n"
# 838 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "or not, the choice is yours…\p"
# 839 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The future can be changed anytime…\n"
# 840 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I wish you safe passage…$"
# 841 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 842 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_TrainersNoticeRunning:
# 843 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Did you know?\p"
# 844 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "If you run fast, TRAINERS may notice\n"
# 845 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "and come after you for a battle.\p"
# 846 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "So, if you want to avoid TRAINERS,\n"
# 847 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "don't catch their eyes, but sneak\l"
# 848 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "cautiously and quietly past them.$"
# 849 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 850 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_LostLotOfItems:
# 851 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Awaaaaaaarrrrgh!\p"
# 852 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "I had a whole lot of items, but I lost\n"
# 853 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "them all when I lost!\p"
# 854 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Awaaaaaaarrrrgh!$"
# 855 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 856 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_YouveDefeatedPyramidKing:
# 857 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Welcome back!\n"
# 858 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You've done the unthinkable!\p"
# 859 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You've defeated the PYRAMID KING\n"
# 860 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "and conquered the BATTLE PYRAMID!$"
# 861 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 862 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_GiveYouTheseBattlePoints:
# 863 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Young explorer!\n"
# 864 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "In commendation of your courage,\l"
# 865 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "we give you these Battle Point(s)!$"
# 866 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 867 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_RulesAreListed:
# 868 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The Battle Quest rules are listed.$"
# 869 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 870 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ReadWhichHeading:
# 871 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Which heading do you want to read?$"
# 872 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 873 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ExplainMonRules:
# 874 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "When the PYRAMID is conquered,\n"
# 875 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "the wild POKéMON that appear in it\l"
# 876 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "are replaced by different kinds.\p"
# 877 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Explore, observe, and learn what kinds\n"
# 878 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "of wild POKéMON you may encounter.$"
# 879 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 880 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ExplainTrainerRules:
# 881 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "TRAINERS are lying in wait for you\n"
# 882 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "inside the PYRAMID.\p"
# 883 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "On each floor, there are up to\n"
# 884 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "eight TRAINERS.\p"
# 885 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "When you defeat a TRAINER, you will\n"
# 886 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "get a helpful hint for your adventure.$"
# 887 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 888 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ExplainMazeRules:
# 889 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The mazes in the PYRAMID rearrange\n"
# 890 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "themselves every time you enter it.\p"
# 891 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The mazes are poorly lit.\n"
# 892 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "You must advance with caution.\p"
# 893 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The light grows brighter whenever you\n"
# 894 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "defeat a wild POKéMON or a TRAINER.$"
# 895 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"

# 896 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
BattleFrontier_BattlePyramidLobby_Text_ExplainBagRules:
# 897 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The BATTLE BAG serves as your BAG\n"
# 898 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "while in the PYRAMID.\p"
# 899 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "There are two separate BATTLE BAGS--\n"
# 900 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "one each for the Level 50 and\l"
# 901 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "Open Level adventures.\p"
# 902 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "They each can hold up to 99 pieces\n"
# 903 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "of ten kinds of items.\p"
# 904 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "The contents of the BATTLE BAG are\n"
# 905 "data/maps/BattleFrontier_BattlePyramidLobby/scripts.pory"
	.string "lost if you fail in your quest.$"
