# 1 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 2 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_MapScripts::
# 3 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, BattleFrontier_BattlePyramidFloor_OnResume
# 4 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_BattlePyramidFloor_OnFrame
# 5 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_BattlePyramidFloor_OnTransition
# 6 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.byte 0
# 7 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 8 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_OnFrame:
# 9 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	map_script_2 VAR_TEMP_D, 1, BattleFrontier_BattlePyramidFloor_EventScript_UpdateLight
# 10 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	map_script_2 VAR_TEMP_PLAYING_PYRAMID_MUSIC, 0, BattleFrontier_BattlePyramidFloor_EventScript_PlayPyramidMusic
# 11 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	map_script_2 VAR_TEMP_F, 1, BattleFrontier_BattlePyramidFloor_EventScript_ShowMapName
# 12 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.2byte 0
# 13 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 14 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_UpdateLight::
# 15 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	lockall
# 16 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	@ pyramid_updatelight, cant use macro because it straddles the loop
# 17 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_0x8004, BATTLE_PYRAMID_FUNC_UPDATE_LIGHT
# 18 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_0x8005, 4
# 19 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_0x8006, PYRAMID_LIGHT_INCR_RADIUS
# 20 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_0x8007, SE_SAVE
# 21 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_RESULT, 0
# 22 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_UpdateLightLoop::
# 23 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	special CallBattlePyramidFunction
# 24 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	delay 2
# 25 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_ne VAR_RESULT, 2, BattleFrontier_BattlePyramidFloor_EventScript_UpdateLightLoop
# 26 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_TEMP_D, 0
# 27 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	releaseall
# 28 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 29 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 30 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_ShowMapName::
# 31 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	special ShowMapNamePopup
# 32 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_TEMP_F, 0
# 33 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 34 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 35 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_PlayPyramidMusic::
# 36 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	playbgm MUS_B_PYRAMID, FALSE
# 37 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_TEMP_PLAYING_PYRAMID_MUSIC, 1
# 38 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 39 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 40 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_OnResume:
# 41 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_setfloorpal
# 42 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_getstatus
# 43 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	switch VAR_TEMP_CHALLENGE_STATUS
# 44 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	case 0, BattleFrontier_BattlePyramidFloor_EventScript_ReadyChallenge
# 45 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	case CHALLENGE_STATUS_SAVING, BattleFrontier_BattlePyramid_EventScript_WarpToLobby
# 46 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	case CHALLENGE_STATUS_PAUSED, BattleFrontier_BattlePyramidFloor_EventScript_ReadyChallenge
# 47 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_get FRONTIER_DATA_BATTLE_OUTCOME
# 48 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, BattleFrontier_BattlePyramidFloor_EventScript_ResetParty
# 49 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, BattleFrontier_BattlePyramidFloor_EventScript_ResetParty
# 50 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, 0, BattleFrontier_BattlePyramidFloor_EventScript_ResetParty
# 51 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_LOST, BattleFrontier_BattlePyramid_EventScript_WarpToLobbyLost
# 52 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_DREW, BattleFrontier_BattlePyramid_EventScript_WarpToLobbyLost
# 53 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_FORFEITED, BattleFrontier_BattlePyramid_EventScript_WarpToLobbyLost
# 54 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_isbattletype BATTLE_TYPE_TRAINER  @ VAR_RESULT seems to be ignored here
# 55 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_TEMP_D, 1
# 56 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_ResetParty::
# 57 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_resetparty
# 58 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 59 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 60 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramid_EventScript_WarpToLobbyLost::
# 61 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST
# 62 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_set PYRAMID_DATA_TRAINER_FLAGS, 255
# 63 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramid_EventScript_WarpToLobby::
# 64 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_updatelight 0, PYRAMID_LIGHT_SET_RADIUS
# 65 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_clearhelditems
# 66 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	special HealPlayerParty
# 67 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	warpsilent MAP_BATTLE_FRONTIER_BATTLE_PYRAMID_LOBBY, 7, 13
# 68 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	waitstate
# 69 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 70 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 71 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_ReadyChallenge::
# 72 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_save CHALLENGE_STATUS_SAVING
# 73 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	special SavePlayerParty
# 74 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 75 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_settrainers
# 76 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_setpartyorder FRONTIER_PARTY_SIZE
# 77 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_TEMP_F, 1
# 78 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 79 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 80 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_OnTransition:
# 81 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	call BattleFrontier_BattlePyramidFloor_EventScript_SetLightRadius
# 82 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_TEMP_F, 1
# 83 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 84 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 85 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFrontier_BattlePyramidFloor_EventScript_SetLightRadius::
# 86 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_updatelight 32, PYRAMID_LIGHT_SET_RADIUS
# 87 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	return
# 88 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 89 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_WarpToNextFloor::
# 90 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	call BattleFrontier_EventScript_IncrementWinStreak
# 91 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_get FRONTIER_DATA_BATTLE_NUM  @ Floor number
# 92 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	addvar VAR_RESULT, 1
# 93 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_set FRONTIER_DATA_BATTLE_NUM, VAR_RESULT
# 94 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_RESULT, 7, BattlePyramid_WarpToTop
# 95 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_seedfloor
# 96 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	frontier_set FRONTIER_DATA_CHALLENGE_STATUS, 0
# 97 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	setvar VAR_RESULT, 0
# 98 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_PYRAMID_FLOOR, 1, 1
# 99 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	waitstate
# 100 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 101 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 102 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_WarpToTop::
# 103 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	warp MAP_BATTLE_FRONTIER_BATTLE_PYRAMID_TOP, 17, 17
# 104 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	waitstate
# 105 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 106 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 107 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_TrainerBattle::
# 108 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	facilitytrainerbattle FACILITY_BATTLE_PYRAMID
# 109 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_showhint
# 110 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	waitmessage
# 111 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	waitbuttonpress
# 112 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	closemessage
# 113 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	releaseall
# 114 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 115 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 116 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_FindItemBall::
# 117 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_setitem
# 118 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	callstd STD_FIND_ITEM
# 119 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto_if_eq VAR_0x8007, 0, BattlePyramid_FindItemBallEnd
# 120 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	pyramid_hideitem
# 121 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_FindItemBallEnd::
# 122 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	end
# 123 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 124 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Retire::
# 125 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	goto BattleFrontier_BattlePyramid_EventScript_WarpToLobbyLost
# 126 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 127 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
@ Also used by Trainer Hill
# 128 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattleFacility_TrainerBattle_PlaceholderText:
# 129 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is a sample message.$"
# 130 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 131 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
gText_BattlePyramidConfirmRest::
# 132 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Your BATTLE PYRAMID quest will be\n"
# 133 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "saved so that you may quit for now.\l"
# 134 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Is that okay?$"
# 135 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 136 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
gText_BattlePyramidConfirmRetire::
# 137 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you sure you want to quit your\n"
# 138 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "PYRAMID quest?$"
# 139 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 140 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintUp1::
# 141 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This floor's exit is in\n"
# 142 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that direction: {UP_ARROW}$"
# 143 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 144 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintLeft1::
# 145 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This floor's exit is in\n"
# 146 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that direction: {LEFT_ARROW}$"
# 147 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 148 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintRight1::
# 149 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This floor's exit is in\n"
# 150 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that direction: {RIGHT_ARROW}$"
# 151 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 152 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintDown1::
# 153 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This floor's exit is in\n"
# 154 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that direction: {DOWN_ARROW}$"
# 155 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 156 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintUp2::
# 157 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit on this floor is in\n"
# 158 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {UP_ARROW} direction.$"
# 159 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 160 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintLeft2::
# 161 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit on this floor is in\n"
# 162 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {LEFT_ARROW} direction.$"
# 163 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 164 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintRight2::
# 165 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit on this floor is in\n"
# 166 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {RIGHT_ARROW} direction.$"
# 167 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 168 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintDown2::
# 169 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit on this floor is in\n"
# 170 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {DOWN_ARROW} direction.$"
# 171 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 172 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintUp3::
# 173 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit is over\n"
# 174 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that {UP_ARROW} way.$"
# 175 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 176 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintLeft3::
# 177 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit is over\n"
# 178 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that {LEFT_ARROW} way.$"
# 179 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 180 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintRight3::
# 181 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit is over\n"
# 182 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that {RIGHT_ARROW} way.$"
# 183 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 184 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintDown3::
# 185 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit is over\n"
# 186 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "that {DOWN_ARROW} way.$"
# 187 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 188 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintUp4::
# 189 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor, the exit is somewhere\n"
# 190 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "in the {UP_ARROW} direction.$"
# 191 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 192 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintLeft4::
# 193 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor, the exit is somewhere\n"
# 194 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "in the {LEFT_ARROW} direction.$"
# 195 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 196 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintRight4::
# 197 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor, the exit is somewhere\n"
# 198 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "in the {RIGHT_ARROW} direction.$"
# 199 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 200 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintDown4::
# 201 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor, the exit is somewhere\n"
# 202 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "in the {DOWN_ARROW} direction.$"
# 203 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 204 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintUp5::
# 205 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit?\n"
# 206 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "It's that {UP_ARROW} way.$"
# 207 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 208 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintLeft5::
# 209 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit?\n"
# 210 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "It's that {LEFT_ARROW} way.$"
# 211 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 212 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintRight5::
# 213 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit?\n"
# 214 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "It's that {RIGHT_ARROW} way.$"
# 215 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 216 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintDown5::
# 217 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit?\n"
# 218 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "It's that {DOWN_ARROW} way.$"
# 219 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 220 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintUp6::
# 221 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit happens to be in\n"
# 222 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {UP_ARROW} direction.$"
# 223 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 224 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintLeft6::
# 225 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit happens to be in\n"
# 226 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {LEFT_ARROW} direction.$"
# 227 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 228 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintRight6::
# 229 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit happens to be in\n"
# 230 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {RIGHT_ARROW} direction.$"
# 231 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 232 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ExitHintDown6::
# 233 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "The exit happens to be in\n"
# 234 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the {DOWN_ARROW} direction.$"
# 235 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 236 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_EightItemsRemaining1::
# 237 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 238 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are eight items left to\n"
# 239 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 240 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 241 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenItemsRemaining1::
# 242 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 243 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are seven items left to\n"
# 244 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 245 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 246 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixItemsRemaining1::
# 247 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 248 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are six items left to\n"
# 249 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 250 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 251 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveItemsRemaining1::
# 252 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 253 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are five items left to\n"
# 254 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 255 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 256 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourItemsRemaining1::
# 257 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 258 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are four items left to\n"
# 259 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 260 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 261 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeItemsRemaining1::
# 262 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 263 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are three items left to\n"
# 264 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 265 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 266 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoItemsRemaining1::
# 267 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 268 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are two items left to\n"
# 269 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 270 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 271 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneItemRemaining1::
# 272 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 273 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There is one item left to\n"
# 274 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found.$"
# 275 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 276 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroItemsRemaining1::
# 277 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Are you looking for items?\p"
# 278 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There isn't anything left to\n"
# 279 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "be found!$"
# 280 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 281 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_EightItemsRemaining2::
# 282 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 283 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 284 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are eight items\n"
# 285 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 286 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 287 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenItemsRemaining2::
# 288 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 289 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 290 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are seven items left\n"
# 291 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 292 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 293 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixItemsRemaining2::
# 294 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 295 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 296 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are six items left\n"
# 297 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 298 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 299 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveItemsRemaining2::
# 300 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 301 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 302 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are five items left\n"
# 303 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 304 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 305 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourItemsRemaining2::
# 306 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 307 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 308 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are four items left\n"
# 309 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 310 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 311 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeItemsRemaining2::
# 312 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 313 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 314 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are three items left\n"
# 315 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 316 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 317 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoItemsRemaining2::
# 318 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 319 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 320 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are two items left\n"
# 321 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 322 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 323 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneItemRemaining2::
# 324 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 325 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 326 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There is just one item\n"
# 327 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 328 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 329 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroItemsRemaining2::
# 330 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Because you won, I'll tell you\n"
# 331 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a little secret!\p"
# 332 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There isn't anything left\n"
# 333 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "lying around here.$"
# 334 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 335 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_EightItemsRemaining3::
# 336 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 337 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are eight items left\n"
# 338 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 339 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 340 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenItemsRemaining3::
# 341 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 342 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are seven items left\n"
# 343 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 344 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 345 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixItemsRemaining3::
# 346 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 347 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are six items left\n"
# 348 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 349 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 350 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveItemsRemaining3::
# 351 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 352 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are five items left\n"
# 353 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 354 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 355 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourItemsRemaining3::
# 356 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 357 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are four items left\n"
# 358 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 359 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 360 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeItemsRemaining3::
# 361 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 362 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are three items left\n"
# 363 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 364 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 365 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoItemsRemaining3::
# 366 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 367 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are two items left\n"
# 368 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 369 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 370 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneItemRemaining3::
# 371 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 372 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there's but one item left\n"
# 373 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.$"
# 374 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 375 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroItemsRemaining3::
# 376 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "How's your stock of items holding up?\p"
# 377 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I reckon there are no more items\n"
# 378 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "waiting to be found on this floor.\l"
# 379 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You take care now!$"
# 380 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 381 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_EightItemsRemaining4::
# 382 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 383 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 384 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be eight more\n"
# 385 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 386 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 387 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenItemsRemaining4::
# 388 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 389 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 390 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be seven more\n"
# 391 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 392 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 393 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixItemsRemaining4::
# 394 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 395 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 396 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be six more\n"
# 397 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 398 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 399 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveItemsRemaining4::
# 400 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 401 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 402 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be five more\n"
# 403 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 404 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 405 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourItemsRemaining4::
# 406 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 407 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 408 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be four more\n"
# 409 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 410 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 411 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeItemsRemaining4::
# 412 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 413 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 414 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be three more\n"
# 415 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 416 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 417 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoItemsRemaining4::
# 418 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 419 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 420 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be two more\n"
# 421 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 422 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 423 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneItemRemaining4::
# 424 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 425 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 426 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appears to be only one more\n"
# 427 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "item on the ground.$"
# 428 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 429 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroItemsRemaining4::
# 430 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You're strong, so you've earned\n"
# 431 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "a hint!\p"
# 432 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There appear to be no more\n"
# 433 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on the ground.$"
# 434 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 435 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_EightItemsRemaining5::
# 436 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 437 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are eight items…$"
# 438 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 439 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenItemsRemaining5::
# 440 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 441 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are seven items…$"
# 442 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 443 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixItemsRemaining5::
# 444 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 445 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are six items…$"
# 446 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 447 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveItemsRemaining5::
# 448 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 449 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are five items…$"
# 450 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 451 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourItemsRemaining5::
# 452 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 453 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are four items…$"
# 454 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 455 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeItemsRemaining5::
# 456 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 457 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are three items…$"
# 458 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 459 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoItemsRemaining5::
# 460 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 461 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are two items…$"
# 462 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 463 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneItemRemaining5::
# 464 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 465 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there is one item…$"
# 466 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 467 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroItemsRemaining5::
# 468 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "On this floor of the PYRAMID,\n"
# 469 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I hear there are no items…$"
# 470 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 471 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_EightItemsRemaining6::
# 472 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 473 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are eight more\n"
# 474 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 475 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 476 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenItemsRemaining6::
# 477 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 478 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are seven more\n"
# 479 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 480 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 481 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixItemsRemaining6::
# 482 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 483 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are six more\n"
# 484 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 485 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 486 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveItemsRemaining6::
# 487 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 488 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are five more\n"
# 489 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 490 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 491 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourItemsRemaining6::
# 492 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 493 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are four more\n"
# 494 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 495 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 496 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeItemsRemaining6::
# 497 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 498 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are three more\n"
# 499 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 500 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 501 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoItemsRemaining6::
# 502 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 503 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are two more\n"
# 504 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 505 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 506 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneItemRemaining6::
# 507 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 508 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there is one more\n"
# 509 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "item on this floor.$"
# 510 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 511 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroItemsRemaining6::
# 512 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Have you collected any items?\p"
# 513 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I believe there are no more\n"
# 514 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "items on this floor.$"
# 515 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 516 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenTrainersRemaining1::
# 517 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 518 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are still seven tough\n"
# 519 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINERS other than me!$"
# 520 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 521 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixTrainersRemaining1::
# 522 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 523 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are still six tough\n"
# 524 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINERS other than me!$"
# 525 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 526 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveTrainersRemaining1::
# 527 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 528 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are still five tough\n"
# 529 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINERS other than me!$"
# 530 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 531 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourTrainersRemaining1::
# 532 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 533 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are still four tough\n"
# 534 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINERS other than me!$"
# 535 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 536 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeTrainersRemaining1::
# 537 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 538 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are still three tough\n"
# 539 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINERS other than me!$"
# 540 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 541 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoTrainersRemaining1::
# 542 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 543 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are still two tough\n"
# 544 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINERS other than me!$"
# 545 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 546 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneTrainersRemaining1::
# 547 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 548 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there's still one tough\n"
# 549 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "TRAINER other than me!$"
# 550 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 551 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroTrainersRemaining1::
# 552 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You were really awesome!\p"
# 553 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There's no one left that\n"
# 554 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "can beat you!$"
# 555 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 556 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenTrainersRemaining2::
# 557 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 558 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are seven TRAINERS left!\n"
# 559 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Someone will humble you!$"
# 560 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 561 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixTrainersRemaining2::
# 562 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 563 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are six TRAINERS left!\n"
# 564 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Someone will humble you!$"
# 565 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 566 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveTrainersRemaining2::
# 567 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 568 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are five TRAINERS left!\n"
# 569 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Someone will humble you!$"
# 570 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 571 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourTrainersRemaining2::
# 572 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 573 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are four TRAINERS left!\n"
# 574 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Someone will humble you!$"
# 575 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 576 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeTrainersRemaining2::
# 577 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 578 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are three TRAINERS left!\n"
# 579 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Someone will humble you!$"
# 580 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 581 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoTrainersRemaining2::
# 582 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 583 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are two TRAINERS left!\n"
# 584 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Someone will humble you!$"
# 585 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 586 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneTrainersRemaining2::
# 587 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 588 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there's one TRAINER left!\n"
# 589 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "I'm sure you will be humbled!$"
# 590 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 591 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroTrainersRemaining2::
# 592 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "This is so upsetting!\p"
# 593 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are no more TRAINERS\n"
# 594 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "who can engage you!$"
# 595 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 596 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenTrainersRemaining3::
# 597 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 598 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are seven more TRAINERS\n"
# 599 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you beat them all?$"
# 600 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 601 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixTrainersRemaining3::
# 602 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 603 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are six more TRAINERS\n"
# 604 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you beat them all?$"
# 605 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 606 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveTrainersRemaining3::
# 607 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 608 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are five more TRAINERS\n"
# 609 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you beat them all?$"
# 610 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 611 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourTrainersRemaining3::
# 612 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 613 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are four more TRAINERS\n"
# 614 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you beat them all?$"
# 615 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 616 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeTrainersRemaining3::
# 617 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 618 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are three more TRAINERS\n"
# 619 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you beat them all?$"
# 620 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 621 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoTrainersRemaining3::
# 622 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 623 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there are two more TRAINERS\n"
# 624 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you beat them both?$"
# 625 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 626 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneTrainersRemaining3::
# 627 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 628 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "But there's still one more TRAINER\n"
# 629 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor. Can you prevail?$"
# 630 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 631 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroTrainersRemaining3::
# 632 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "That's pretty impressive!\p"
# 633 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You've gone through all the TRAINERS\n"
# 634 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "on this floor.$"
# 635 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 636 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenTrainersRemaining4::
# 637 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could sweep through\n"
# 638 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the seven TRAINERS left on this floor.$"
# 639 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 640 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixTrainersRemaining4::
# 641 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could sweep through\n"
# 642 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the six TRAINERS left on this floor.$"
# 643 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 644 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveTrainersRemaining4::
# 645 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could sweep through\n"
# 646 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the five TRAINERS left on this floor.$"
# 647 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 648 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourTrainersRemaining4::
# 649 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could sweep through\n"
# 650 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the four TRAINERS left on this floor.$"
# 651 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 652 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeTrainersRemaining4::
# 653 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could sweep through\n"
# 654 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the three TRAINERS left on this floor.$"
# 655 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 656 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoTrainersRemaining4::
# 657 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could sweep through\n"
# 658 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the two TRAINERS left on this floor.$"
# 659 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 660 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneTrainersRemaining4::
# 661 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Maybe you could complete your sweep\n"
# 662 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "with the one TRAINER left on this floor.$"
# 663 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 664 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroTrainersRemaining4::
# 665 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There isn't a single person left who\n"
# 666 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "can defeat you now…$"
# 667 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 668 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenTrainersRemaining5::
# 669 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 670 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the seven expert TRAINERS who remain.$"
# 671 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 672 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixTrainersRemaining5::
# 673 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 674 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the six expert TRAINERS who remain.$"
# 675 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 676 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveTrainersRemaining5::
# 677 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 678 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the five expert TRAINERS who remain.$"
# 679 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 680 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourTrainersRemaining5::
# 681 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 682 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the four expert TRAINERS who remain.$"
# 683 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 684 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeTrainersRemaining5::
# 685 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 686 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the three expert TRAINERS who remain.$"
# 687 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 688 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoTrainersRemaining5::
# 689 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 690 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the two expert TRAINERS who remain.$"
# 691 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 692 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneTrainersRemaining5::
# 693 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "You may have what it takes to beat\n"
# 694 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the one expert TRAINER who remains.$"
# 695 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 696 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroTrainersRemaining5::
# 697 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Your skills are beyond reproach.\p"
# 698 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There are no more TRAINERS here\n"
# 699 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "who have any chance of beating you.$"
# 700 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 701 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SevenTrainersRemaining6::
# 702 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 703 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the seven remaining TRAINERS?$"
# 704 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 705 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_SixTrainersRemaining6::
# 706 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 707 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the six remaining TRAINERS?$"
# 708 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 709 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FiveTrainersRemaining6::
# 710 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 711 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the five remaining TRAINERS?$"
# 712 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 713 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_FourTrainersRemaining6::
# 714 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 715 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the four remaining TRAINERS?$"
# 716 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 717 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ThreeTrainersRemaining6::
# 718 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 719 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the three remaining TRAINERS?$"
# 720 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 721 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_TwoTrainersRemaining6::
# 722 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 723 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the two remaining TRAINERS?$"
# 724 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 725 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_OneTrainersRemaining6::
# 726 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "Can you keep winning against\n"
# 727 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "the last remaining TRAINER?$"
# 728 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"

# 729 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
BattlePyramid_Text_ZeroTrainersRemaining6::
# 730 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "There aren't any TRAINERS left that\n"
# 731 "data/maps/BattleFrontier_BattlePyramidFloor/scripts.pory"
	.string "can take you on now…$"
