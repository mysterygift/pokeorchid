# 1 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 2 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_MapScripts::
# 3 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, FallarborTown_BattleTentLobby_OnFrame
# 4 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, FallarborTown_BattleTentLobby_OnWarp
# 5 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.byte 0
# 6 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 7 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_OnWarp:
# 8 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_1, 0, FallarborTown_BattleTentLobby_EventScript_TurnPlayerNorth
# 9 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.2byte 0
# 10 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 11 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_TurnPlayerNorth::
# 12 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_1, 1
# 13 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 14 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 15 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 16 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_OnFrame:
# 17 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, 0, FallarborTown_BattleTentLobby_EventScript_GetChallengeStatus
# 18 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING, FallarborTown_BattleTentLobby_EventScript_QuitWithoutSaving
# 19 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_PAUSED, FallarborTown_BattleTentLobby_EventScript_ResumeChallenge
# 20 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_WON, FallarborTown_BattleTentLobby_EventScript_WonChallenge
# 21 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST, FallarborTown_BattleTentLobby_EventScript_LostChallenge
# 22 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.2byte 0
# 23 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 24 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_GetChallengeStatus::
# 25 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_getstatus
# 26 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 27 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 28 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_QuitWithoutSaving::
# 29 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lockall
# 30 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_DidntSaveBeforeQuitting, MSGBOX_DEFAULT
# 31 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closemessage
# 32 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 33 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 34 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_50
# 35 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	releaseall
# 36 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 37 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 38 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_WonChallenge::
# 39 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lockall
# 40 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_BeatThreeTrainers, MSGBOX_DEFAULT
# 41 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	message FallarborTown_BattleTentLobby_Text_WaitWhileSaveGame
# 42 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 43 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_setrandomprize
# 44 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_50
# 45 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_save 0
# 46 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	playse SE_SAVE
# 47 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitse
# 48 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 49 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_GivePrize::
# 50 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_PresentYouWithPrize, MSGBOX_DEFAULT
# 51 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_giveprize
# 52 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 53 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case FALSE, FallarborTown_BattleTentLobby_EventScript_NoRoomForPrize
# 54 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 55 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	message FallarborTown_BattleTentLobby_Text_ReceivedPrize
# 56 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 57 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 58 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitfanfare
# 59 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_AwaitAnotherChallenge2, MSGBOX_DEFAULT
# 60 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closemessage
# 61 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 62 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	releaseall
# 63 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 64 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 65 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_NoRoomForPrize::
# 66 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_BagFullReturnForPrize, MSGBOX_DEFAULT
# 67 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 68 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closemessage
# 69 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 70 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	releaseall
# 71 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 72 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 73 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_PrizeWaiting::
# 74 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lockall
# 75 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_BeatThreeTrainers, MSGBOX_DEFAULT
# 76 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_GivePrize
# 77 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 78 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 79 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_LostChallenge::
# 80 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lockall
# 81 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	message FallarborTown_BattleTentLobby_Text_ThankYouWaitWhileSaving
# 82 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 83 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_50
# 84 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_save 0
# 85 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	playse SE_SAVE
# 86 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitse
# 87 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_AwaitAnotherChallenge2, MSGBOX_DEFAULT
# 88 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closemessage
# 89 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 90 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	releaseall
# 91 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 92 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 93 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_ResumeChallenge::
# 94 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lockall
# 95 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	message FallarborTown_BattleTentLobby_Text_LookingForwardToArrival
# 96 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 97 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_save CHALLENGE_STATUS_SAVING
# 98 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	playse SE_SAVE
# 99 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitse
# 100 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 101 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 102 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_EnterChallenge
# 103 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 104 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_Attendant::
# 105 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lock
# 106 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	faceplayer
# 107 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_getprize
# 108 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto_if_ne VAR_RESULT, ITEM_NONE, FallarborTown_BattleTentLobby_EventScript_PrizeWaiting
# 109 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	special SavePlayerParty
# 110 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_WelcomeToBattleTent, MSGBOX_DEFAULT
# 111 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_AskEnterChallenge::
# 112 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	message FallarborTown_BattleTentLobby_Text_TakeChallenge
# 113 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 114 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	multichoice 17, 6, MULTI_CHALLENGEINFO, FALSE
# 115 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 116 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 0, FallarborTown_BattleTentLobby_EventScript_TryEnterChallenge
# 117 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 1, FallarborTown_BattleTentLobby_EventScript_ExplainChallenge
# 118 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 2, FallarborTown_BattleTentLobby_EventScript_CancelChallenge
# 119 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case MULTI_B_PRESSED, FallarborTown_BattleTentLobby_EventScript_CancelChallenge
# 120 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 121 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_TryEnterChallenge::
# 122 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_ARENA
# 123 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_FRONTIER_BATTLE_MODE, FRONTIER_MODE_SINGLES
# 124 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_RESULT, 2
# 125 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_checkineligible
# 126 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_0x8004, TRUE, FallarborTown_BattleTentLobby_EventScript_NotEnoughValidMons
# 127 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_LVL_MODE, FRONTIER_LVL_TENT
# 128 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_SelectThreeMons, MSGBOX_DEFAULT
# 129 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fadescreen FADE_TO_BLACK
# 130 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_0x8004, 2
# 131 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_0x8005, FRONTIER_PARTY_SIZE
# 132 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	special ChoosePartyForBattleFrontier
# 133 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, FallarborTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge
# 134 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_SaveBeforeChallenge, MSGBOX_YESNO
# 135 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 136 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case NO, FallarborTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge
# 137 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case YES, FallarborTown_BattleTentLobby_EventScript_SaveBeforeChallenge
# 138 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case MULTI_B_PRESSED, FallarborTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge
# 139 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 140 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_SaveBeforeChallenge::
# 141 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 142 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_SELECTED_MON_ORDER
# 143 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	fallarbortent_init
# 144 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING
# 145 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_PAUSED, FALSE
# 146 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	special LoadPlayerParty
# 147 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closemessage
# 148 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	delay 2
# 149 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	call Common_EventScript_SaveGame
# 150 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 255
# 151 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto_if_eq VAR_RESULT, 0, FallarborTown_BattleTentLobby_EventScript_CancelChallengeSaveFailed
# 152 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_EnterChallenge::
# 153 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	special SavePlayerParty
# 154 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_setpartyorder FRONTIER_PARTY_SIZE
# 155 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_GuideYouToBattleTent, MSGBOX_DEFAULT
# 156 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closemessage
# 157 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	call FallarborTown_BattleTentLobby_EventScript_WalkToDoor
# 158 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	warp MAP_FALLARBOR_TOWN_BATTLE_TENT_CORRIDOR, 2, 7
# 159 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setvar VAR_TEMP_CHALLENGE_STATUS, 0
# 160 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitstate
# 161 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 162 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 163 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_ExplainChallenge::
# 164 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_ExplainFallarborTent, MSGBOX_DEFAULT
# 165 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_AskEnterChallenge
# 166 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 167 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_NotEnoughValidMons::
# 168 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 169 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case FRONTIER_LVL_50, FallarborTown_BattleTentLobby_EventScript_NotEnoughValidMonsLv50
# 170 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case FRONTIER_LVL_OPEN, FallarborTown_BattleTentLobby_EventScript_NotEnoughValidMonsLvOpen
# 171 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_NotEnoughValidMonsLv50::
# 172 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_NotEnoughValidMonsLv50, MSGBOX_DEFAULT
# 173 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_EndCancelChallenge
# 174 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 175 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_NotEnoughValidMonsLvOpen::
# 176 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_NotEnoughValidMonsLvOpen, MSGBOX_DEFAULT
# 177 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_EndCancelChallenge
# 178 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 179 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_CancelChallengeSaveFailed::
# 180 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 181 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_CancelChallenge
# 182 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 183 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_LoadPartyCancelChallenge::
# 184 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	special LoadPlayerParty
# 185 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_CancelChallenge::
# 186 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_AwaitAnotherChallenge, MSGBOX_DEFAULT
# 187 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_EndCancelChallenge::
# 188 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	release
# 189 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 190 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 191 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_WalkToDoor::
# 192 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_FALLARBOR_TENT_ATTENDANT, FallarborTown_BattleTentLobby_Movement_AttendantWalkToDoor
# 193 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_PLAYER, FallarborTown_BattleTentLobby_Movement_PlayerWalkToDoor
# 194 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmovement 0
# 195 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	opendoor 6, 1
# 196 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitdooranim
# 197 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_FALLARBOR_TENT_ATTENDANT, FallarborTown_BattleTentLobby_Movement_AttendantEnterDoor
# 198 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	applymovement LOCALID_PLAYER, FallarborTown_BattleTentLobby_Movement_PlayerEnterDoor
# 199 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmovement 0
# 200 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	closedoor 6, 1
# 201 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitdooranim
# 202 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	return
# 203 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 204 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Movement_AttendantWalkToDoor:
# 205 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 206 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 207 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 208 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	step_end
# 209 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 210 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Movement_AttendantEnterDoor:
# 211 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 212 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	set_invisible
# 213 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	step_end
# 214 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 215 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Movement_PlayerWalkToDoor:
# 216 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 217 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 218 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 219 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	step_end
# 220 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 221 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Movement_PlayerEnterDoor:
# 222 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 223 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	walk_up
# 224 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	set_invisible
# 225 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	step_end
# 226 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 227 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_Hiker::
# 228 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_CameToCampOut, MSGBOX_NPC
# 229 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 230 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 231 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_LittleBoy::
# 232 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_MakeThinkImJustKid, MSGBOX_NPC
# 233 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 234 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 235 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_Lass::
# 236 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_FallarborTentMyFavorite, MSGBOX_NPC
# 237 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 238 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 239 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_Scott::
# 240 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lock
# 241 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	faceplayer
# 242 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto_if_set FLAG_MET_SCOTT_IN_FALLARBOR, FallarborTown_BattleTentLobby_EventScript_ScottAlreadySpokenTo
# 243 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_ScottLookingForSomeone, MSGBOX_DEFAULT
# 244 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	addvar VAR_SCOTT_STATE, 1
# 245 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	setflag FLAG_MET_SCOTT_IN_FALLARBOR
# 246 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	release
# 247 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 248 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 249 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_ScottAlreadySpokenTo::
# 250 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox FallarborTown_BattleTentLobby_Text_ScottMakeChallenge, MSGBOX_DEFAULT
# 251 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	release
# 252 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 253 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 254 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_RulesBoard::
# 255 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	lockall
# 256 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattleArenaLobby_Text_RulesAreListed, MSGBOX_DEFAULT
# 257 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard
# 258 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 259 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 260 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard::
# 261 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	message BattleFrontier_BattleArenaLobby_Text_ReadWhichHeading
# 262 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	waitmessage
# 263 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	multichoice 17, 0, MULTI_FALLARBOR_TENT_RULES, FALSE
# 264 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	switch VAR_RESULT
# 265 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 0, FallarborTown_BattleTentLobby_EventScript_RulesLevel
# 266 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 1, FallarborTown_BattleTentLobby_EventScript_RulesBattle
# 267 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 2, FallarborTown_BattleTentLobby_EventScript_RulesMind
# 268 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 3, FallarborTown_BattleTentLobby_EventScript_RulesSkill
# 269 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 4, FallarborTown_BattleTentLobby_EventScript_RulesBody
# 270 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case 5, FallarborTown_BattleTentLobby_EventScript_ExitRules
# 271 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	case MULTI_B_PRESSED, FallarborTown_BattleTentLobby_EventScript_ExitRules
# 272 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 273 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 274 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_RulesLevel::
# 275 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox BattleTentLobby_Text_ExplainLevelRules, MSGBOX_DEFAULT
# 276 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard
# 277 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 278 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 279 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_RulesBattle::
# 280 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattleArenaLobby_Text_ExplainBattleRules, MSGBOX_DEFAULT
# 281 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard
# 282 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 283 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 284 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_RulesMind::
# 285 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattleArenaLobby_Text_ExplainMindRules, MSGBOX_DEFAULT
# 286 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard
# 287 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 288 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 289 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_RulesSkill::
# 290 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattleArenaLobby_Text_ExplainSkillRules, MSGBOX_DEFAULT
# 291 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard
# 292 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 293 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 294 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_RulesBody::
# 295 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	msgbox BattleFrontier_BattleArenaLobby_Text_ExplainBodyRules, MSGBOX_DEFAULT
# 296 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	goto FallarborTown_BattleTentLobby_EventScript_ReadRulesBoard
# 297 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 298 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 299 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_EventScript_ExitRules::
# 300 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	releaseall
# 301 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	end
# 302 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 303 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Text_MakeThinkImJustKid:
# 304 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "Fufufufufu.\p"
# 305 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "I'm going to make everyone think\n"
# 306 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "I'm just a kid and let them play down.\p"
# 307 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "Then, I'll shock them and grab\n"
# 308 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "the title!$"
# 309 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 310 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Text_FallarborTentMyFavorite:
# 311 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "You know how BATTLE TENTS offer\n"
# 312 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "different events in different towns?\p"
# 313 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "My favorite is definitely the BATTLE\n"
# 314 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "TENT in FALLARBOR TOWN.\p"
# 315 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "I think it's fantastic how TRAINERS\n"
# 316 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "try to win with all their faith in\l"
# 317 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "their POKéMON.$"
# 318 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 319 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Text_CameToCampOut:
# 320 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "I heard something about some tent,\n"
# 321 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "so I came to camp out.\p"
# 322 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "I didn't know that tents these days\n"
# 323 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "are so luxurious!\p"
# 324 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "Since I'm here, I may as well try\n"
# 325 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "my hand at battling!$"
# 326 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 327 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Text_ScottLookingForSomeone:
# 328 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "SCOTT: Hi, {PLAYER}{KUN}!\n"
# 329 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "So you came out to this BATTLE TENT!\p"
# 330 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "The people in these parts tend to be\n"
# 331 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "easygoing and laid-back.\p"
# 332 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "But, you see, what I'm looking for are\n"
# 333 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "people with…\p"
# 334 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "How should I say this?\p"
# 335 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "Someone bursting with the desire\n"
# 336 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "and the drive to win.\p"
# 337 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "If there were a TRAINER like that,\n"
# 338 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "I'd immediately…\p"
# 339 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "Whoops! Never mind!\n"
# 340 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "Keep working at it!$"
# 341 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"

# 342 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
FallarborTown_BattleTentLobby_Text_ScottMakeChallenge:
# 343 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "SCOTT: Instead of wasting your\n"
# 344 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "time with the likes of me, why not\l"
# 345 "data/maps/FallarborTown_BattleTentLobby/scripts.pory"
	.string "make a challenge?$"
