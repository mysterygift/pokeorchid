# 1 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 2 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_MapScripts::
# 3 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattlePikeLobby_OnFrame
# 4 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, BattleFrontier_BattlePikeLobby_OnWarp
# 5 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.byte 0
# 6 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 7 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_OnFrame:
# 8 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, 0, BattleFrontier_BattlePikeLobby_EventScript_GetChallengeStatus
# 9 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING, BattleFrontier_BattlePikeLobby_EventScript_QuitWithoutSaving
# 10 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_WON, BattleFrontier_BattlePikeLobby_EventScript_WonChallenge
# 11 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST, BattleFrontier_BattlePikeLobby_EventScript_LostChallenge
# 12 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.2byte 0
# 13 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 14 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_OnWarp:
# 15 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, BattleFrontier_BattlePikeLobby_EventScript_TurnPlayerNorth
# 16 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.2byte 0
# 17 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 18 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_TurnPlayerNorth::
# 19 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_1, 1
# 20 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 21 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 22 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 23 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_GetChallengeStatus::
# 24 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_getstatus
# 25 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 26 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 27 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_QuitWithoutSaving::
# 28 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special HealPlayerParty
# 29 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_resethelditems
# 30 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	lockall
# 31 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_FailedToSaveBeforeQuitting, MSGBOX_DEFAULT
# 32 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	closemessage
# 33 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_set PIKE_DATA_WIN_STREAK, 0
# 34 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_set PIKE_DATA_WIN_STREAK_ACTIVE, FALSE
# 35 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 36 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 37 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	releaseall
# 38 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 39 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 40 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_WonChallenge::
# 41 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	lockall
# 42 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_isbrain
# 43 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, BattleFrontier_BattlePikeLobby_EventScript_DefeatedQueen
# 44 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_PossessLuckInAbundance, MSGBOX_DEFAULT
# 45 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 46 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_GiveBattlePoints
# 47 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 48 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_DefeatedQueen::
# 49 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_SnatchedVictoryFromQueen, MSGBOX_DEFAULT
# 50 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 51 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_GiveBattlePoints::
# 52 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_AwardYouTheseBattlePoints, MSGBOX_DEFAULT
# 53 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_givepoints
# 54 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_Text_ObtainedXBattlePoints, MSGBOX_GETPOINTS
# 55 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_checkairshow
# 56 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_get PIKE_DATA_TOTAL_STREAKS
# 57 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	addvar VAR_RESULT, 1
# 58 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_set PIKE_DATA_TOTAL_STREAKS, VAR_RESULT
# 59 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special LoadPlayerParty
# 60 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special HealPlayerParty
# 61 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 62 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_resethelditems
# 63 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	message BattleFrontier_BattlePikeLobby_Text_ShallRecordResults
# 64 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 65 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_save 0
# 66 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	playse SE_SAVE
# 67 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitse
# 68 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_LookForwardToSeeingYou, MSGBOX_DEFAULT
# 69 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	closemessage
# 70 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 71 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	releaseall
# 72 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 73 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 74 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_LostChallenge::
# 75 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	lockall
# 76 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	message BattleFrontier_BattlePikeLobby_Text_ChallengeEndedRecordResults
# 77 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 78 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_checkairshow
# 79 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_BATTLE_NUM, 0
# 80 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_set PIKE_DATA_WIN_STREAK_ACTIVE, FALSE
# 81 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special LoadPlayerParty
# 82 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special HealPlayerParty
# 83 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 84 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_resethelditems
# 85 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_save 0
# 86 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	playse SE_SAVE
# 87 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitse
# 88 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_LookForwardToSeeingYou, MSGBOX_DEFAULT
# 89 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	closemessage
# 90 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 91 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	releaseall
# 92 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 93 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 94 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_Attendant::
# 95 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	lock
# 96 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	faceplayer
# 97 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_PIKE
# 98 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES
# 99 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special SavePlayerParty
# 100 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_WelcomeToBattlePike, MSGBOX_DEFAULT
# 101 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_AskTakeChallenge::
# 102 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	message BattleFrontier_BattlePikeLobby_Text_TakeChallenge
# 103 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 104 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 105 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	switch VAR_RESULT
# 106 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 0, BattleFrontier_BattlePikeLobby_EventScript_TryEnterChallenge
# 107 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 1, BattleFrontier_BattlePikeLobby_EventScript_ExplainChallenge
# 108 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 2, BattleFrontier_BattlePikeLobby_EventScript_CancelChallenge
# 109 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePikeLobby_EventScript_CancelChallenge
# 110 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 111 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_TryEnterChallenge::
# 112 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	message BattleFrontier_BattlePikeLobby_Text_WhichChallengeMode
# 113 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 114 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	multichoice 17, 6, MULTI_LEVEL_MODE, FALSE
# 115 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	switch VAR_RESULT
# 116 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case FRONTIER_LVL_TENT, BattleFrontier_BattlePikeLobby_EventScript_CancelChallenge
# 117 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePikeLobby_EventScript_CancelChallenge
# 118 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_checkineligible
# 119 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, BattleFrontier_BattlePikeLobby_EventScript_NotEnoughValidMons
# 120 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, VAR_RESULT
# 121 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_PleaseChooseThreeMons, MSGBOX_DEFAULT
# 122 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 123 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	callnative RemoveFollowingPokemon
# 124 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	call BattleFrontier_EventScript_GetLvlMode
# 125 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	copyvar VAR_0x8004, VAR_RESULT
# 126 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_PARTY_SIZE
# 127 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 128 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePikeLobby_EventScript_LoadPartyAndCancelChallenge
# 129 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_SaveBeforeChallenge, MSGBOX_YESNO
# 130 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	switch VAR_RESULT
# 131 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case NO, BattleFrontier_BattlePikeLobby_EventScript_LoadPartyAndCancelChallenge
# 132 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case YES, BattleFrontier_BattlePikeLobby_EventScript_SaveBeforeChallenge
# 133 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePikeLobby_EventScript_LoadPartyAndCancelChallenge
# 134 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 135 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_SaveBeforeChallenge::
# 136 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 137 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_1, 0
# 138 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 139 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_init
# 140 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING
# 141 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_set PIKE_DATA_WIN_STREAK_ACTIVE, TRUE
# 142 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_savehelditems
# 143 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 144 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special LoadPlayerParty
# 145 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	closemessage
# 146 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	delay 2
# 147 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 148 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 149 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	pike_savehelditems
# 150 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePikeLobby_EventScript_CancelChallengeSaveFailed
# 151 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special SavePlayerParty
# 152 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_setpartyorder FRONTIER_PARTY_SIZE
# 153 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_StepThisWay, MSGBOX_DEFAULT
# 154 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	closemessage
# 155 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_settrainers
# 156 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	call BattleFrontier_BattlePikeLobby_EventScript_WalkToCorridor
# 157 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special HealPlayerParty
# 158 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	call BattleFrontier_BattlePike_EventScript_CloseCurtain
# 159 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	warpsilent MAP_BATTLE_FRONTIER_BATTLE_PIKE_CORRIDOR, 6, 7
# 160 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 161 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitstate
# 162 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 163 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 164 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_ExplainChallenge::
# 165 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_ExplainBattlePike, MSGBOX_DEFAULT
# 166 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_AskTakeChallenge
# 167 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 168 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_NotEnoughValidMons::
# 169 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	switch VAR_RESULT
# 170 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case FRONTIER_LVL_50, BattleFrontier_BattlePikeLobby_EventScript_NotEnoughValidMonsLv50
# 171 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case FRONTIER_LVL_OPEN, BattleFrontier_BattlePikeLobby_EventScript_NotEnoughValidMonsLvOpen
# 172 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 173 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_NotEnoughValidMonsLv50::
# 174 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsLv50, MSGBOX_DEFAULT
# 175 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 176 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 177 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_EndCancelChallenge
# 178 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 179 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_NotEnoughValidMonsLvOpen::
# 180 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsLvOpen, MSGBOX_DEFAULT
# 181 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	call BattleFrontier_ShowCaughtBannedSpecies
# 182 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsEnd, MSGBOX_DEFAULT
# 183 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_EndCancelChallenge
# 184 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 185 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_CancelChallengeSaveFailed::
# 186 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 187 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_CancelChallenge
# 188 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 189 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_LoadPartyAndCancelChallenge::
# 190 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special LoadPlayerParty
# 191 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	callnative UpdateFollowingPokemon
# 192 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_CancelChallenge::
# 193 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_LookForwardToSeeingYou, MSGBOX_DEFAULT
# 194 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_EndCancelChallenge::
# 195 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	release
# 196 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 197 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 198 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_ShowResults::
# 199 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	lockall
# 200 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	frontier_results FRONTIER_FACILITY_PIKE
# 201 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitbuttonpress
# 202 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special RemoveRecordsWindow
# 203 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	releaseall
# 204 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 205 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 206 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_WalkToCorridor::
# 207 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	applymovement LOCALID_PIKE_LOBBY_ATTENDANT, BattleFrontier_BattlePikeLobby_Movement_AttendantWalkToCorridor
# 208 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_BattlePikeLobby_Movement_PlayerWalkToCorridor
# 209 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmovement 0
# 210 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	return
# 211 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 212 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Movement_PlayerWalkToCorridor:
# 213 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	walk_up
# 214 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Movement_AttendantWalkToCorridor:
# 215 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	walk_up
# 216 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	walk_up
# 217 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	set_invisible
# 218 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	step_end
# 219 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 220 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_Hiker::
# 221 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_OneRoomAwayFromGoal, MSGBOX_NPC
# 222 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 223 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 224 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_Twin::
# 225 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_NeverHadToBattleTrainer, MSGBOX_NPC
# 226 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 227 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 228 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_Beauty::
# 229 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_ThinkAbilitiesUsefulHere, MSGBOX_NPC
# 230 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 231 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 232 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_RulesBoard::
# 233 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	lockall
# 234 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_RulesAreListed, MSGBOX_DEFAULT
# 235 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_ReadRulesBoard
# 236 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 237 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 238 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_ReadRulesBoard::
# 239 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	message BattleFrontier_BattlePikeLobby_Text_ReadWhichHeading
# 240 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitmessage
# 241 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	multichoice 16, 4, MULTI_BATTLE_PIKE_RULES, FALSE
# 242 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	switch VAR_RESULT
# 243 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 0, BattleFrontier_BattlePikeLobby_EventScript_RulesPokenavBag
# 244 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 1, BattleFrontier_BattlePikeLobby_EventScript_RulesHeldItems
# 245 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 2, BattleFrontier_BattlePikeLobby_EventScript_RulesMonOrder
# 246 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case 3, BattleFrontier_BattlePikeLobby_EventScript_ExitRules
# 247 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_BattlePikeLobby_EventScript_ExitRules
# 248 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 249 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 250 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_RulesPokenavBag::
# 251 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_ExplainPokenavBagRules, MSGBOX_DEFAULT
# 252 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_ReadRulesBoard
# 253 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 254 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 255 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_RulesHeldItems::
# 256 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_ExplainHeldItemRules, MSGBOX_DEFAULT
# 257 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_ReadRulesBoard
# 258 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 259 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 260 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_RulesMonOrder::
# 261 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	msgbox BattleFrontier_BattlePikeLobby_Text_ExplainMonOrderRules, MSGBOX_DEFAULT
# 262 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	goto BattleFrontier_BattlePikeLobby_EventScript_ReadRulesBoard
# 263 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 264 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 265 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_EventScript_ExitRules::
# 266 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	releaseall
# 267 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	end
# 268 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 269 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePike_EventScript_CloseCurtain::
# 270 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	playse SE_PIKE_CURTAIN_CLOSE
# 271 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	special CloseBattlePikeCurtain
# 272 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	waitse
# 273 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	return
# 274 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 275 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_WelcomeToBattlePike:
# 276 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Where the luck of TRAINERS\n"
# 277 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "is put to the test…\p"
# 278 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Welcome to the BATTLE PIKE…\p"
# 279 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I am your guide to the BATTLE PIKE…$"
# 280 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 281 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_TakeChallenge:
# 282 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Would you like to take the Battle\n"
# 283 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Choice challenge?$"
# 284 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 285 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ExplainBattlePike:
# 286 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Here we conduct an event we call\n"
# 287 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "the Battle Choice.\p"
# 288 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "The Battle Choice rules are very\n"
# 289 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "simple…\p"
# 290 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Choose one of three paths and make\n"
# 291 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "your way to the goal room at the end\l"
# 292 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "of the BATTLE PIKE. It's that simple.\p"
# 293 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "However, what happens on the chosen\n"
# 294 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "path depends entirely on the luck\l"
# 295 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "of the challenger…\p"
# 296 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "If you reach the goal, you will be\n"
# 297 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "rewarded with Battle Points.\p"
# 298 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "If you want to interrupt your\n"
# 299 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "challenge, please have a word with\l"
# 300 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "our staff in the big rooms on the way.\p"
# 301 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "If you don't save before interrupting,\n"
# 302 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "you will be disqualified.$"
# 303 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 304 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_LookForwardToSeeingYou:
# 305 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "We look forward to seeing you\n"
# 306 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "on another occasion…$"
# 307 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 308 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_WhichChallengeMode:
# 309 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You have the choice of two courses,\n"
# 310 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Level 50 and Open Level.\l"
# 311 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Which will you challenge?$"
# 312 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 313 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsLv50:
# 314 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I beg your pardon, but…\p"
# 315 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You do not have three eligible\n"
# 316 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "POKéMON for the Battle Choice event.\p"
# 317 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You must have three different POKéMON\n"
# 318 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "of Level 50 or less to enter.\p"
# 319 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "They also must be holding different\n"
# 320 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "kinds of items.\p"
# 321 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 322 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 323 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsEnd:
# 324 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Please come see me when\n"
# 325 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "you are ready…$"
# 326 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 327 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_NotEnoughValidMonsLvOpen:
# 328 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I beg your pardon, but…\p"
# 329 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You do not have three eligible\n"
# 330 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "POKéMON for the Battle Choice event.\p"
# 331 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You must have three different\n"
# 332 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "POKéMON to enter.\p"
# 333 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "They also must be holding different\n"
# 334 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "kinds of items.\p"
# 335 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "EGGS{STR_VAR_1}.$"
# 336 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 337 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_PleaseChooseThreeMons:
# 338 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Please choose the three POKéMON\n"
# 339 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "you wish to enter in the challenge…$"
# 340 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 341 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_SaveBeforeChallenge:
# 342 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Before starting your Battle Choice\n"
# 343 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "challenge, I must save the game.\l"
# 344 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Is that acceptable?$"
# 345 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 346 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_StepThisWay:
# 347 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Please step this way…$"
# 348 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 349 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ChallengeEndedRecordResults:
# 350 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Your challenge has ended…\p"
# 351 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I shall record your results.\n"
# 352 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Please wait…$"
# 353 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 354 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_PossessLuckInAbundance:
# 355 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You have completed the challenge…\p"
# 356 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I must say… You seem to possess luck\n"
# 357 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "in abundance…$"
# 358 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 359 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ShallRecordResults:
# 360 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I shall record your results.\n"
# 361 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Please wait…$"
# 362 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 363 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
@ Unused
# 364 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_AwardYouTheseBattlePoints2:
# 365 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "To commemorate your completion of\n"
# 366 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "the Battle Choice challenge, we award\l"
# 367 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "you these Battle Point(s)…$"
# 368 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 369 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
@ Unused
# 370 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ReachedBattlePointLimit:
# 371 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You appear to have reached the limit\n"
# 372 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "for Battle Points…\p"
# 373 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Please exchange some Battle Points\n"
# 374 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "for prizes, then return…$"
# 375 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 376 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_FailedToSaveBeforeQuitting:
# 377 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I beg your pardon, but…\p"
# 378 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You failed to save before you quit\n"
# 379 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "your challenge the last time.\p"
# 380 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Because of that, your challenge so far\n"
# 381 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "has been disqualified. I am sorry…$"
# 382 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 383 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_SnatchedVictoryFromQueen:
# 384 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Congratulations…\p"
# 385 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "You have snatched victory from the\n"
# 386 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "PIKE QUEEN and cleared the event…$"
# 387 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 388 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_AwardYouTheseBattlePoints:
# 389 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "In recognition of your amazing luck,\n"
# 390 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "we award you these Battle Point(s)…$"
# 391 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 392 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_OneRoomAwayFromGoal:
# 393 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Arrgh! I blew my chance!\n"
# 394 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I was one room away from the goal!\p"
# 395 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "In this place, you'd better watch out\n"
# 396 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "for poison, freezing, and so on.$"
# 397 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 398 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_NeverHadToBattleTrainer:
# 399 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I've completed the challenge 10 times\n"
# 400 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "now, but I've never had to battle\l"
# 401 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "a TRAINER once.$"
# 402 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 403 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ThinkAbilitiesUsefulHere:
# 404 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Listen! Listen!\p"
# 405 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Don't you think that the special\n"
# 406 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "abilities of POKéMON will be useful\l"
# 407 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "here?$"
# 408 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 409 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
@ Unused
# 410 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_TrainersWhicheverPathIChoose:
# 411 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "What is this weird place?\n"
# 412 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I can't figure it out at all!\p"
# 413 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "I've taken the challenge a bunch\n"
# 414 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "of times, but all I ever do is run into\l"
# 415 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "TRAINERS whichever path I choose.$"
# 416 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 417 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_RulesAreListed:
# 418 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "The Battle Choice's rules are listed.$"
# 419 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 420 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ReadWhichHeading:
# 421 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "Which heading do you want to read?$"
# 422 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 423 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ExplainPokenavBagRules:
# 424 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "The BAG and POKéNAV may not be used\n"
# 425 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "during a Battle Choice challenge.$"
# 426 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 427 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ExplainHeldItemRules:
# 428 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "During a Battle Choice challenge,\n"
# 429 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "any BERRY or HERB held by POKéMON\l"
# 430 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "will be effective only once.$"
# 431 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"

# 432 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
BattleFrontier_BattlePikeLobby_Text_ExplainMonOrderRules:
# 433 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "During a Battle Choice challenge,\n"
# 434 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "the sequence of POKéMON cannot be\l"
# 435 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "changed.\p"
# 436 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "The sequence must be set before\n"
# 437 "data/maps/BattleFrontier_BattlePikeLobby/scripts.pory"
	.string "starting your challenge.$"
