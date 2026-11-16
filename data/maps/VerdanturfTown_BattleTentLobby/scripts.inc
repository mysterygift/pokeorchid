# 1 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 2 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_MapScripts::
# 3 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, VerdanturfTown_BattleTentLobby_OnFrame
# 4 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, VerdanturfTown_BattleTentLobby_OnWarp
# 5 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.byte 0
# 6 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 7 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_OnWarp:
# 8 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, VerdanturfTown_BattleTentLobby_EventScript_TurnPlayerNorth
# 9 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.2byte 0
# 10 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 11 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_TurnPlayerNorth::
# 12 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_1, 1
# 13 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 14 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 15 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 16 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_OnFrame:
# 17 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, 0, VerdanturfTown_BattleTentLobby_EventScript_GetChallengeStatus
# 18 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING, VerdanturfTown_BattleTentLobby_EventScript_QuitWithoutSaving
# 19 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_PAUSED, VerdanturfTown_BattleTentLobby_EventScript_ResumeChallenge
# 20 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_WON, VerdanturfTown_BattleTentLobby_EventScript_WonChallenge
# 21 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST, VerdanturfTown_BattleTentLobby_EventScript_LostChallenge
# 22 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.2byte 0
# 23 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 24 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_GetChallengeStatus::
# 25 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_getstatus
# 26 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 27 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 28 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_QuitWithoutSaving::
# 29 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lockall
# 30 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_FailedToSaveBeforeEndingChallenge, MSGBOX_DEFAULT
# 31 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closemessage
# 32 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 33 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 34 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_50
# 35 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	releaseall
# 36 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 37 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 38 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_WonChallenge::
# 39 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lockall
# 40 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_AchievedThreeWinStreak, MSGBOX_DEFAULT
# 41 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	message VerdanturfTown_BattleTentLobby_Text_FeatWillBeRecorded
# 42 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 43 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_setrandomprize
# 44 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_50
# 45 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_save 0
# 46 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	playse SE_SAVE
# 47 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitse
# 48 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 49 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_GivePrize::
# 50 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_PresentYouWithPrize, MSGBOX_DEFAULT
# 51 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_giveprize
# 52 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 53 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case FALSE, VerdanturfTown_BattleTentLobby_EventScript_NoRoomForPrize
# 54 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 55 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	message BattleFrontier_BattleDomeLobby_Text_ReceivedPrize  @ Odd that it used Dome's copy instead of Palace's
# 56 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 57 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 58 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitfanfare
# 59 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_ReturnFortified, MSGBOX_DEFAULT
# 60 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closemessage
# 61 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 62 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	releaseall
# 63 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 64 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 65 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_NoRoomForPrize::
# 66 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_NoSpaceForPrize, MSGBOX_DEFAULT
# 67 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 68 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closemessage
# 69 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 70 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	releaseall
# 71 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 72 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 73 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_PrizeWaiting::
# 74 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lockall
# 75 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_AchievedThreeWinStreak, MSGBOX_DEFAULT
# 76 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_GivePrize
# 77 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 78 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 79 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_LostChallenge::
# 80 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lockall
# 81 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	message VerdanturfTown_BattleTentLobby_Text_ResultsWillBeRecorded
# 82 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 83 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_50
# 84 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_save 0
# 85 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	playse SE_SAVE
# 86 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitse
# 87 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_ReturnFortified, MSGBOX_DEFAULT
# 88 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closemessage
# 89 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 90 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	releaseall
# 91 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 92 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 93 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_ResumeChallenge::
# 94 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lockall
# 95 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_WeHaveBeenWaiting, MSGBOX_DEFAULT
# 96 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	message BattleFrontier_BattlePalaceLobby_Text_MustSaveBeforeChallenge
# 97 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 98 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_save CHALLENGE_STATUS_SAVING
# 99 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	playse SE_SAVE
# 100 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitse
# 101 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 102 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 103 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_EnterChallenge
# 104 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 105 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_Attendant::
# 106 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lock
# 107 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	faceplayer
# 108 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_getprize
# 109 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_ne VAR_RESULT, ITEM_NONE, VerdanturfTown_BattleTentLobby_EventScript_PrizeWaiting
# 110 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	special SavePlayerParty
# 111 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_WelcomeToBattleTent, MSGBOX_DEFAULT
# 112 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_AskEnterChallenge::
# 113 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	message VerdanturfTown_BattleTentLobby_Text_TakeChallenge
# 114 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 115 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 116 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 117 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 0, VerdanturfTown_BattleTentLobby_EventScript_TryEnterChallenge
# 118 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 1, VerdanturfTown_BattleTentLobby_EventScript_ExplainChallenge
# 119 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 2, VerdanturfTown_BattleTentLobby_EventScript_CancelChallenge
# 120 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case MULTI_B_PRESSED, VerdanturfTown_BattleTentLobby_EventScript_CancelChallenge
# 121 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 122 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_TryEnterChallenge::
# 123 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_PALACE
# 124 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES
# 125 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_RESULT, 2
# 126 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_checkineligible
# 127 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, VerdanturfTown_BattleTentLobby_EventScript_NotEnoughValidMons
# 128 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_TENT
# 129 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_SelectThreeMons, MSGBOX_DEFAULT
# 130 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 131 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_0x8004, 1
# 132 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_PARTY_SIZE
# 133 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 134 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, VerdanturfTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge
# 135 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_SaveBeforeChallenge, MSGBOX_YESNO
# 136 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 137 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case NO, VerdanturfTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge
# 138 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case YES, VerdanturfTown_BattleTentLobby_EventScript_SaveBeforeChallenge
# 139 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case MULTI_B_PRESSED, VerdanturfTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge
# 140 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 141 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_SaveBeforeChallenge::
# 142 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 143 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 144 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	verdanturftent_init
# 145 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING
# 146 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 147 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	special LoadPlayerParty
# 148 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closemessage
# 149 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	delay 2
# 150 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 151 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 152 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, VerdanturfTown_BattleTentLobby_EventScript_CancelChallengeSaveFailed
# 153 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_EnterChallenge::
# 154 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	special SavePlayerParty
# 155 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_setpartyorder FRONTIER_PARTY_SIZE
# 156 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_NowFollowMe, MSGBOX_DEFAULT
# 157 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closemessage
# 158 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	call VerdanturfTown_BattleTentLobby_EventScript_WalkToDoor
# 159 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	warp MAP_VERDANTURF_TOWN_BATTLE_TENT_CORRIDOR, 2, 7
# 160 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 161 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitstate
# 162 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 163 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 164 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_ExplainChallenge::
# 165 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_ExplainVerdanturfTent, MSGBOX_DEFAULT
# 166 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_AskEnterChallenge
# 167 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 168 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_NotEnoughValidMons::
# 169 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 170 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case FRONTIER_LVL_50, VerdanturfTown_BattleTentLobby_EventScript_NotEnoughValidMonsLv50
# 171 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case FRONTIER_LVL_OPEN, VerdanturfTown_BattleTentLobby_EventScript_NotEnoughValidMonsLvOpen
# 172 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 173 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_NotEnoughValidMonsLv50::
# 174 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_NotEnoughValidMonsLv50, MSGBOX_DEFAULT
# 175 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_EndCancelChallenge
# 176 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 177 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_NotEnoughValidMonsLvOpen::
# 178 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_NotEnoughValidMonsLvOpen, MSGBOX_DEFAULT
# 179 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_EndCancelChallenge
# 180 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 181 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_CancelChallengeSaveFailed::
# 182 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 183 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_CancelChallenge
# 184 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 185 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge::
# 186 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	special LoadPlayerParty
# 187 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_CancelChallenge::
# 188 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_ReturnFortified, MSGBOX_DEFAULT
# 189 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_EndCancelChallenge::
# 190 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 191 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 192 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 193 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_WalkToDoor::
# 194 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_VERDANTURF_TENT_ATTENDANT, VerdanturfTown_BattleTentLobby_Movement_WalkToDoor
# 195 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_PLAYER, VerdanturfTown_BattleTentLobby_Movement_WalkToDoor
# 196 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmovement 0
# 197 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	opendoor 6, 1
# 198 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitdooranim
# 199 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_VERDANTURF_TENT_ATTENDANT, VerdanturfTown_BattleTentLobby_Movement_AttendantEnterDoor
# 200 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_PLAYER, VerdanturfTown_BattleTentLobby_Movement_PlayerEnterDoor
# 201 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmovement 0
# 202 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	closedoor 6, 1
# 203 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitdooranim
# 204 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	return
# 205 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 206 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Movement_WalkToDoor:
# 207 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	walk_up
# 208 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	walk_up
# 209 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	walk_up
# 210 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	step_end
# 211 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 212 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Movement_AttendantEnterDoor:
# 213 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	walk_up
# 214 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	set_invisible
# 215 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	step_end
# 216 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 217 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Movement_PlayerEnterDoor:
# 218 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	walk_up
# 219 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	walk_up
# 220 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	set_invisible
# 221 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	step_end
# 222 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 223 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_AttractGiver::
# 224 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lock
# 225 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	faceplayer
# 226 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_set FLAG_RECEIVED_TM_ATTRACT, VerdanturfTown_BattleTentLobby_EventScript_ReceivedAttract
# 227 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_AttractionRunsDeep, MSGBOX_DEFAULT
# 228 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	giveitem ITEM_TM_ATTRACT
# 229 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, Common_EventScript_ShowBagIsFull
# 230 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setflag FLAG_RECEIVED_TM_ATTRACT
# 231 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_AttractionMutual, MSGBOX_DEFAULT
# 232 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 233 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 234 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 235 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_ReceivedAttract::
# 236 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_AttractionMutual, MSGBOX_DEFAULT
# 237 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 238 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 239 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 240 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_Boy1::
# 241 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_TaughtWhatKindsOfMoves, MSGBOX_NPC
# 242 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 243 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 244 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_Boy2::
# 245 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lock
# 246 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_MonsReluctantToUseDislikedMoves, MSGBOX_DEFAULT
# 247 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 248 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 249 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 250 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_Scott::
# 251 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lock
# 252 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	faceplayer
# 253 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto_if_set FLAG_MET_SCOTT_IN_VERDANTURF, VerdanturfTown_BattleTentLobby_EventScript_ScottAlreadySpokenTo
# 254 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_ScottCanMeetToughTrainers, MSGBOX_DEFAULT
# 255 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	addvar VAR_SCOTT_STATE, 1
# 256 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setflag FLAG_MET_SCOTT_IN_VERDANTURF
# 257 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 258 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 259 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 260 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_ScottAlreadySpokenTo::
# 261 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_ScottVisitRegularly, MSGBOX_DEFAULT
# 262 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 263 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 264 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 265 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_LittleBoy::
# 266 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lock
# 267 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_GentleMonsScaryIfAngry, MSGBOX_DEFAULT
# 268 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	release
# 269 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 270 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 271 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesBoard::
# 272 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	lockall
# 273 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox VerdanturfTown_BattleTentLobby_Text_RulesAreListed, MSGBOX_DEFAULT
# 274 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 275 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 276 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 277 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard::
# 278 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	message BattleFrontier_BattlePalaceLobby_Text_ReadWhichHeading
# 279 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	waitmessage
# 280 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	setvar VAR_0x8004, SCROLL_MULTI_BATTLE_TENT_RULES
# 281 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	special ShowScrollableMultichoice
# 282 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 283 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 0, VerdanturfTown_BattleTentLobby_EventScript_RulesLevel
# 284 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 1, VerdanturfTown_BattleTentLobby_EventScript_RulesBasics
# 285 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 2, VerdanturfTown_BattleTentLobby_EventScript_RulesNature
# 286 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 3, VerdanturfTown_BattleTentLobby_EventScript_RulesMoves
# 287 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 4, VerdanturfTown_BattleTentLobby_EventScript_RulesUnderpowered
# 288 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 5, VerdanturfTown_BattleTentLobby_EventScript_RulesWhenInDanger
# 289 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case 6, VerdanturfTown_BattleTentLobby_EventScript_ExitRules
# 290 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	case MULTI_B_PRESSED, VerdanturfTown_BattleTentLobby_EventScript_ExitRules
# 291 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 292 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 293 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesLevel::
# 294 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleTentLobby_Text_ExplainLevelRules, MSGBOX_DEFAULT
# 295 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 296 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 297 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 298 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesBasics::
# 299 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_ExplainRulesBasics, MSGBOX_DEFAULT
# 300 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 301 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 302 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 303 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesNature::
# 304 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_ExplainRulesNature, MSGBOX_DEFAULT
# 305 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 306 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 307 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 308 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesMoves::
# 309 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_ExplainRulesMoves, MSGBOX_DEFAULT
# 310 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 311 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 312 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 313 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesUnderpowered::
# 314 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_ExplainRulesUnderpowered, MSGBOX_DEFAULT
# 315 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 316 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 317 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 318 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_RulesWhenInDanger::
# 319 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattlePalaceLobby_Text_ExplainRulesWhenInDanger, MSGBOX_DEFAULT
# 320 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	goto VerdanturfTown_BattleTentLobby_EventScript_ReadRulesBoard
# 321 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 322 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 323 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_EventScript_ExitRules::
# 324 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	releaseall
# 325 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	end
# 326 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 327 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_MonsReluctantToUseDislikedMoves:
# 328 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "If it doesn't like a certain move,\n"
# 329 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "a POKéMON will be reluctant to use it.\p"
# 330 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "It doesn't matter how strong it is,\n"
# 331 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "either.\p"
# 332 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "For example, a POKéMON with a GENTLE\n"
# 333 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "nature probably won't enjoy hurting\l"
# 334 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "its opponents.\p"
# 335 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "If it can't seem to live up to its\n"
# 336 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "potential, it's probably failing at\l"
# 337 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "using a disliked move against its will.$"
# 338 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 339 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_GentleMonsScaryIfAngry:
# 340 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "My big sister is gentle usually.\n"
# 341 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "But when she gets angry,\l"
# 342 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "she's really, really scary!\p"
# 343 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "I bet a gentle POKéMON will be scary\n"
# 344 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "if it gets angry!$"
# 345 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 346 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_AttractionRunsDeep:
# 347 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "My feelings toward my POKéMON…\n"
# 348 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "The attraction runs deep…\p"
# 349 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "Oh, hi, you didn't see that, did you?\n"
# 350 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "Well, it doesn't matter.\p"
# 351 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "How would you like this TM for\n"
# 352 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "your POKéMON?$"
# 353 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 354 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_AttractionMutual:
# 355 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "My feelings toward my POKéMON…\n"
# 356 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "I'm sure the attraction is mutual!\p"
# 357 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "They battle exactly the way I want\n"
# 358 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "them to!$"
# 359 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 360 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_TaughtWhatKindsOfMoves:
# 361 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "What kind of moves have you taught\n"
# 362 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "your POKéMON?\p"
# 363 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "I think you would give yourself\n"
# 364 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "an advantage if they knew how to\l"
# 365 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "heal or protect themselves.$"
# 366 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 367 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_ScottCanMeetToughTrainers:
# 368 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "SCOTT: Hey there, {PLAYER}{KUN}!\n"
# 369 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "I thought I might see you here.\p"
# 370 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "A BATTLE TENT's a place where\n"
# 371 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "you can meet tough TRAINERS.\p"
# 372 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "It doesn't matter what the rules are,\n"
# 373 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "or how battles are waged, either.\p"
# 374 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "{PLAYER}{KUN}, I expect you to do\n"
# 375 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "the best you can!$"
# 376 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"

# 377 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
VerdanturfTown_BattleTentLobby_Text_ScottVisitRegularly:
# 378 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "SCOTT: I visit here regularly in hopes\n"
# 379 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "of seeing tough TRAINERS in action\l"
# 380 "data/maps/VerdanturfTown_BattleTentLobby/scripts.pory"
	.string "in whatever the situation.$"
