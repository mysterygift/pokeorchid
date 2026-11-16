# 1 "data/maps/SSTidalCorridor/scripts.pory"

# 2 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_MapScripts::
# 3 "data/maps/SSTidalCorridor/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SSTidalCorridor_OnFrame
# 4 "data/maps/SSTidalCorridor/scripts.pory"
	.byte 0
# 5 "data/maps/SSTidalCorridor/scripts.pory"

# 6 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_OnFrame:
# 7 "data/maps/SSTidalCorridor/scripts.pory"
	map_script_2 VAR_SS_TIDAL_SCOTT_STATE, 0, SSTidalCorridor_EventScript_ScottScene
# 8 "data/maps/SSTidalCorridor/scripts.pory"
	map_script_2 VAR_SS_TIDAL_STATE, SS_TIDAL_BOARD_SLATEPORT, SSTidalCorridor_EventScript_DepartSlateportForLilycove
# 9 "data/maps/SSTidalCorridor/scripts.pory"
	map_script_2 VAR_SS_TIDAL_STATE, SS_TIDAL_BOARD_LILYCOVE, SSTidalCorridor_EventScript_DepartLilycoveForSlateport
# 10 "data/maps/SSTidalCorridor/scripts.pory"
	map_script_2 VAR_SS_TIDAL_STATE, SS_TIDAL_EXIT_CURRENTS_RIGHT, SSTidalCorridor_EventScript_HalfwayToLilycove
# 11 "data/maps/SSTidalCorridor/scripts.pory"
	map_script_2 VAR_SS_TIDAL_STATE, SS_TIDAL_EXIT_CURRENTS_LEFT, SSTidalCorridor_EventScript_ArrivedInSlateport
# 12 "data/maps/SSTidalCorridor/scripts.pory"
	.2byte 0
# 13 "data/maps/SSTidalCorridor/scripts.pory"

# 14 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_DepartSlateportForLilycove::
# 15 "data/maps/SSTidalCorridor/scripts.pory"
	special SetSSTidalFlag
# 16 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_DEPART_SLATEPORT
# 17 "data/maps/SSTidalCorridor/scripts.pory"
	lockall
# 18 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 19 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_FastCurrentsHopeYouEnjoyVoyage, MSGBOX_DEFAULT
# 20 "data/maps/SSTidalCorridor/scripts.pory"
	releaseall
# 21 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 22 "data/maps/SSTidalCorridor/scripts.pory"

# 23 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_DepartLilycoveForSlateport::
# 24 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_DEPART_LILYCOVE
# 25 "data/maps/SSTidalCorridor/scripts.pory"
	lockall
# 26 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 27 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_HopeYouEnjoyVoyage, MSGBOX_DEFAULT
# 28 "data/maps/SSTidalCorridor/scripts.pory"
	releaseall
# 29 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 30 "data/maps/SSTidalCorridor/scripts.pory"

# 31 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalRooms_EventScript_HalfwayToSlateport::
# 32 "data/maps/SSTidalCorridor/scripts.pory"
	special SetSSTidalFlag
# 33 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_HALFWAY_SLATEPORT
# 34 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 35 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_FastCurrentsHopeYouEnjoyVoyage, MSGBOX_DEFAULT
# 36 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 37 "data/maps/SSTidalCorridor/scripts.pory"

# 38 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalRooms_EventScript_ArrivedInLilycove::
# 39 "data/maps/SSTidalCorridor/scripts.pory"
	special ResetSSTidalFlag
# 40 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_LAND_LILYCOVE
# 41 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 42 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_MadeLandInLilycove, MSGBOX_DEFAULT
# 43 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 44 "data/maps/SSTidalCorridor/scripts.pory"

# 45 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_ReachedStepCount::
# 46 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_eq VAR_SS_TIDAL_STATE, SS_TIDAL_DEPART_SLATEPORT, SSTidalCorridor_EventScript_HalfwayToLilycove
# 47 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_eq VAR_SS_TIDAL_STATE, SS_TIDAL_HALFWAY_SLATEPORT, SSTidalCorridor_EventScript_ArrivedInSlateport
# 48 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 49 "data/maps/SSTidalCorridor/scripts.pory"

# 50 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_HalfwayToLilycove::
# 51 "data/maps/SSTidalCorridor/scripts.pory"
	special ResetSSTidalFlag
# 52 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_HALFWAY_LILYCOVE
# 53 "data/maps/SSTidalCorridor/scripts.pory"
	lockall
# 54 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 55 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_HopeYouEnjoyVoyage, MSGBOX_DEFAULT
# 56 "data/maps/SSTidalCorridor/scripts.pory"
	releaseall
# 57 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 58 "data/maps/SSTidalCorridor/scripts.pory"

# 59 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_ArrivedInSlateport::
# 60 "data/maps/SSTidalCorridor/scripts.pory"
	special ResetSSTidalFlag
# 61 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_LAND_SLATEPORT
# 62 "data/maps/SSTidalCorridor/scripts.pory"
	lockall
# 63 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 64 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_MadeLandInSlateport, MSGBOX_DEFAULT
# 65 "data/maps/SSTidalCorridor/scripts.pory"
	releaseall
# 66 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 67 "data/maps/SSTidalCorridor/scripts.pory"

# 68 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalRooms_EventScript_ArrivedInSlateport::
# 69 "data/maps/SSTidalCorridor/scripts.pory"
	special ResetSSTidalFlag
# 70 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_LAND_SLATEPORT
# 71 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_DING_DONG
# 72 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidal_Text_MadeLandInSlateport, MSGBOX_DEFAULT
# 73 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 74 "data/maps/SSTidalCorridor/scripts.pory"

# 75 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalRooms_EventScript_ProgessCruiseAfterBed::
# 76 "data/maps/SSTidalCorridor/scripts.pory"
	switch VAR_SS_TIDAL_STATE
# 77 "data/maps/SSTidalCorridor/scripts.pory"
	case SS_TIDAL_DEPART_SLATEPORT, SSTidalRooms_EventScript_ArrivedInLilycove
# 78 "data/maps/SSTidalCorridor/scripts.pory"
	case SS_TIDAL_HALFWAY_LILYCOVE, SSTidalRooms_EventScript_ArrivedInLilycove
# 79 "data/maps/SSTidalCorridor/scripts.pory"
	case SS_TIDAL_DEPART_LILYCOVE, SSTidalRooms_EventScript_HalfwayToSlateport
# 80 "data/maps/SSTidalCorridor/scripts.pory"
	case SS_TIDAL_HALFWAY_SLATEPORT, SSTidalRooms_EventScript_ArrivedInSlateport
# 81 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 82 "data/maps/SSTidalCorridor/scripts.pory"

# 83 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Briney::
# 84 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_BrineyWelcomeAboard, MSGBOX_NPC
# 85 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 86 "data/maps/SSTidalCorridor/scripts.pory"

# 87 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Peeko::
# 88 "data/maps/SSTidalCorridor/scripts.pory"
	lock
# 89 "data/maps/SSTidalCorridor/scripts.pory"
	faceplayer
# 90 "data/maps/SSTidalCorridor/scripts.pory"
	waitse
# 91 "data/maps/SSTidalCorridor/scripts.pory"
	playmoncry SPECIES_WINGULL, CRY_MODE_NORMAL
# 92 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_Peeko, MSGBOX_DEFAULT
# 93 "data/maps/SSTidalCorridor/scripts.pory"
	waitmoncry
# 94 "data/maps/SSTidalCorridor/scripts.pory"
	release
# 95 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 96 "data/maps/SSTidalCorridor/scripts.pory"

# 97 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Cabin1Sign::
# 98 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_Cabin1, MSGBOX_SIGN
# 99 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 100 "data/maps/SSTidalCorridor/scripts.pory"

# 101 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Cabin2Sign::
# 102 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_Cabin2, MSGBOX_SIGN
# 103 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 104 "data/maps/SSTidalCorridor/scripts.pory"

# 105 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Cabin3Sign::
# 106 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_Cabin3, MSGBOX_SIGN
# 107 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 108 "data/maps/SSTidalCorridor/scripts.pory"

# 109 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Cabin4Sign::
# 110 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_Cabin4, MSGBOX_SIGN
# 111 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 112 "data/maps/SSTidalCorridor/scripts.pory"

# 113 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_ExitSailor::
# 114 "data/maps/SSTidalCorridor/scripts.pory"
	lock
# 115 "data/maps/SSTidalCorridor/scripts.pory"
	faceplayer
# 116 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_eq VAR_SS_TIDAL_STATE, SS_TIDAL_LAND_LILYCOVE, SSTidalCorridor_EventScript_ExitLilycove
# 117 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_eq VAR_SS_TIDAL_STATE, SS_TIDAL_LAND_SLATEPORT, SSTidalCorridor_EventScript_ExitSlateport
# 118 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_CanRestInCabin2, MSGBOX_DEFAULT
# 119 "data/maps/SSTidalCorridor/scripts.pory"
	release
# 120 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 121 "data/maps/SSTidalCorridor/scripts.pory"

# 122 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_ExitLilycove::
# 123 "data/maps/SSTidalCorridor/scripts.pory"
	setrespawn HEAL_LOCATION_LILYCOVE_CITY
# 124 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_WeveArrived, MSGBOX_DEFAULT
# 125 "data/maps/SSTidalCorridor/scripts.pory"
	call_if_set FLAG_RECEIVED_TM_SNATCH, SSTidalCorridor_EventScript_HideSnatchGiver
# 126 "data/maps/SSTidalCorridor/scripts.pory"
	warp MAP_LILYCOVE_CITY_HARBOR, 8, 11
# 127 "data/maps/SSTidalCorridor/scripts.pory"
	waitstate
# 128 "data/maps/SSTidalCorridor/scripts.pory"
	release
# 129 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 130 "data/maps/SSTidalCorridor/scripts.pory"

# 131 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_ExitSlateport::
# 132 "data/maps/SSTidalCorridor/scripts.pory"
	setrespawn HEAL_LOCATION_SLATEPORT_CITY
# 133 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_WeveArrived, MSGBOX_DEFAULT
# 134 "data/maps/SSTidalCorridor/scripts.pory"
	call_if_set FLAG_RECEIVED_TM_SNATCH, SSTidalCorridor_EventScript_HideSnatchGiver
# 135 "data/maps/SSTidalCorridor/scripts.pory"
	warp MAP_SLATEPORT_CITY_HARBOR, 8, 11
# 136 "data/maps/SSTidalCorridor/scripts.pory"
	waitstate
# 137 "data/maps/SSTidalCorridor/scripts.pory"
	release
# 138 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 139 "data/maps/SSTidalCorridor/scripts.pory"

# 140 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_HideSnatchGiver::
# 141 "data/maps/SSTidalCorridor/scripts.pory"
	setflag FLAG_HIDE_SS_TIDAL_ROOMS_SNATCH_GIVER
# 142 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 143 "data/maps/SSTidalCorridor/scripts.pory"

# 144 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Porthole::
# 145 "data/maps/SSTidalCorridor/scripts.pory"
	lockall
# 146 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_eq VAR_SS_TIDAL_STATE, SS_TIDAL_DEPART_SLATEPORT, SSTidalCorridor_EventScript_LookThroughPorthole
# 147 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_eq VAR_SS_TIDAL_STATE, SS_TIDAL_HALFWAY_SLATEPORT, SSTidalCorridor_EventScript_LookThroughPorthole
# 148 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_HorizonSpreadsBeyondPorthole, MSGBOX_DEFAULT
# 149 "data/maps/SSTidalCorridor/scripts.pory"
	releaseall
# 150 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 151 "data/maps/SSTidalCorridor/scripts.pory"

# 152 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_LookThroughPorthole::
# 153 "data/maps/SSTidalCorridor/scripts.pory"
	special LookThroughPorthole
# 154 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 155 "data/maps/SSTidalCorridor/scripts.pory"

# 156 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_Sailor::
# 157 "data/maps/SSTidalCorridor/scripts.pory"
	lock
# 158 "data/maps/SSTidalCorridor/scripts.pory"
	faceplayer
# 159 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_set FLAG_DEFEATED_SS_TIDAL_TRAINERS, SSTidalCorridor_EventScript_EnjoyYourCruise
# 160 "data/maps/SSTidalCorridor/scripts.pory"
	call SSTidalCorridor_EventScript_CheckIfTrainersDefeated
# 161 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_VisitOtherCabins, MSGBOX_DEFAULT
# 162 "data/maps/SSTidalCorridor/scripts.pory"
	release
# 163 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 164 "data/maps/SSTidalCorridor/scripts.pory"

# 165 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_EnjoyYourCruise::
# 166 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_EnjoyYourCruise, MSGBOX_DEFAULT
# 167 "data/maps/SSTidalCorridor/scripts.pory"
	release
# 168 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 169 "data/maps/SSTidalCorridor/scripts.pory"

# 170 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_CheckIfTrainersDefeated::
# 171 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_PHILLIP, SSTidalCorridor_EventScript_TrainerNotDefeated
# 172 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_LEONARD, SSTidalCorridor_EventScript_TrainerNotDefeated
# 173 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_COLTON, SSTidalCorridor_EventScript_TrainerNotDefeated
# 174 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_MICAH, SSTidalCorridor_EventScript_TrainerNotDefeated
# 175 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_THOMAS, SSTidalCorridor_EventScript_TrainerNotDefeated
# 176 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_LEA_AND_JED, SSTidalCorridor_EventScript_TrainerNotDefeated
# 177 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_GARRET, SSTidalCorridor_EventScript_TrainerNotDefeated
# 178 "data/maps/SSTidalCorridor/scripts.pory"
	goto_if_not_defeated TRAINER_NAOMI, SSTidalCorridor_EventScript_TrainerNotDefeated
# 179 "data/maps/SSTidalCorridor/scripts.pory"
	setflag FLAG_DEFEATED_SS_TIDAL_TRAINERS
# 180 "data/maps/SSTidalCorridor/scripts.pory"
	goto SSTidalCorridor_EventScript_EnjoyYourCruise
# 181 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 182 "data/maps/SSTidalCorridor/scripts.pory"

# 183 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_TrainerNotDefeated::
# 184 "data/maps/SSTidalCorridor/scripts.pory"
	return
# 185 "data/maps/SSTidalCorridor/scripts.pory"

# 186 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_EventScript_ScottScene::
# 187 "data/maps/SSTidalCorridor/scripts.pory"
	lockall
# 188 "data/maps/SSTidalCorridor/scripts.pory"
	applymovement LOCALID_SS_TIDAL_SCOTT, SSTidalCorridor_Movement_ScottApproachPlayer
# 189 "data/maps/SSTidalCorridor/scripts.pory"
	waitmovement 0
# 190 "data/maps/SSTidalCorridor/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
# 191 "data/maps/SSTidalCorridor/scripts.pory"
	waitmovement 0
# 192 "data/maps/SSTidalCorridor/scripts.pory"
	msgbox SSTidalCorridor_Text_ScottBattleFrontierInvite, MSGBOX_DEFAULT
# 193 "data/maps/SSTidalCorridor/scripts.pory"
	closemessage
# 194 "data/maps/SSTidalCorridor/scripts.pory"
	applymovement LOCALID_PLAYER, SSTidalCorridor_Movement_PlayerWatchScottExit
# 195 "data/maps/SSTidalCorridor/scripts.pory"
	applymovement LOCALID_SS_TIDAL_EXIT_SAILOR, SSTidalCorridor_Movement_SailorMoveForScott
# 196 "data/maps/SSTidalCorridor/scripts.pory"
	applymovement LOCALID_SS_TIDAL_SCOTT, SSTidalCorridor_Movement_ScottExit
# 197 "data/maps/SSTidalCorridor/scripts.pory"
	waitmovement 0
# 198 "data/maps/SSTidalCorridor/scripts.pory"
	playse SE_EXIT
# 199 "data/maps/SSTidalCorridor/scripts.pory"
	waitse
# 200 "data/maps/SSTidalCorridor/scripts.pory"
	removeobject LOCALID_SS_TIDAL_SCOTT
# 201 "data/maps/SSTidalCorridor/scripts.pory"
	applymovement LOCALID_SS_TIDAL_EXIT_SAILOR, SSTidalCorridor_Movement_SailorReturn
# 202 "data/maps/SSTidalCorridor/scripts.pory"
	waitmovement 0
# 203 "data/maps/SSTidalCorridor/scripts.pory"
	delay 30
# 204 "data/maps/SSTidalCorridor/scripts.pory"
	setflag FLAG_MET_SCOTT_ON_SS_TIDAL
# 205 "data/maps/SSTidalCorridor/scripts.pory"
	setvar VAR_SS_TIDAL_SCOTT_STATE, 1
# 206 "data/maps/SSTidalCorridor/scripts.pory"
	releaseall
# 207 "data/maps/SSTidalCorridor/scripts.pory"
	end
# 208 "data/maps/SSTidalCorridor/scripts.pory"

# 209 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Movement_ScottApproachPlayer:
# 210 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 211 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 212 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 213 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 214 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 215 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 216 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 217 "data/maps/SSTidalCorridor/scripts.pory"
	step_end
# 218 "data/maps/SSTidalCorridor/scripts.pory"

# 219 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Movement_ScottExit:
# 220 "data/maps/SSTidalCorridor/scripts.pory"
	walk_in_place_faster_down
# 221 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 222 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 223 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 224 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 225 "data/maps/SSTidalCorridor/scripts.pory"
	walk_down
# 226 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 227 "data/maps/SSTidalCorridor/scripts.pory"
	step_end
# 228 "data/maps/SSTidalCorridor/scripts.pory"

# 229 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Movement_PlayerWatchScottExit:
# 230 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 231 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 232 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 233 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 234 "data/maps/SSTidalCorridor/scripts.pory"
	delay_8
# 235 "data/maps/SSTidalCorridor/scripts.pory"
	walk_in_place_faster_down
# 236 "data/maps/SSTidalCorridor/scripts.pory"
	step_end
# 237 "data/maps/SSTidalCorridor/scripts.pory"

# 238 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Movement_SailorMoveForScott:
# 239 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 240 "data/maps/SSTidalCorridor/scripts.pory"
	walk_right
# 241 "data/maps/SSTidalCorridor/scripts.pory"
	walk_right
# 242 "data/maps/SSTidalCorridor/scripts.pory"
	walk_in_place_faster_up
# 243 "data/maps/SSTidalCorridor/scripts.pory"
	delay_16
# 244 "data/maps/SSTidalCorridor/scripts.pory"
	walk_in_place_faster_left
# 245 "data/maps/SSTidalCorridor/scripts.pory"
	step_end
# 246 "data/maps/SSTidalCorridor/scripts.pory"

# 247 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Movement_SailorReturn:
# 248 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 249 "data/maps/SSTidalCorridor/scripts.pory"
	walk_left
# 250 "data/maps/SSTidalCorridor/scripts.pory"
	walk_in_place_faster_up
# 251 "data/maps/SSTidalCorridor/scripts.pory"
	step_end
# 252 "data/maps/SSTidalCorridor/scripts.pory"

# 253 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_ScottBattleFrontierInvite:
# 254 "data/maps/SSTidalCorridor/scripts.pory"
	.string "SCOTT: Well, hi, hi!\n"
# 255 "data/maps/SSTidalCorridor/scripts.pory"
	.string "{PLAYER}{KUN}, {PLAYER}{KUN}!\p"
# 256 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Something's come up, so I have to\n"
# 257 "data/maps/SSTidalCorridor/scripts.pory"
	.string "disembark, but am I glad to see you!\p"
# 258 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Congratulations, LEAGUE CHAMPION!\p"
# 259 "data/maps/SSTidalCorridor/scripts.pory"
	.string "There's a place I'd like to invite\n"
# 260 "data/maps/SSTidalCorridor/scripts.pory"
	.string "someone like you.\p"
# 261 "data/maps/SSTidalCorridor/scripts.pory"
	.string "It's the…\n"
# 262 "data/maps/SSTidalCorridor/scripts.pory"
	.string "BATTLE FRONTIER!\p"
# 263 "data/maps/SSTidalCorridor/scripts.pory"
	.string "What's the place like?\n"
# 264 "data/maps/SSTidalCorridor/scripts.pory"
	.string "You'll understand when you see it!\p"
# 265 "data/maps/SSTidalCorridor/scripts.pory"
	.string "I've spoken with the ship's CAPTAIN\n"
# 266 "data/maps/SSTidalCorridor/scripts.pory"
	.string "about this.\p"
# 267 "data/maps/SSTidalCorridor/scripts.pory"
	.string "The next time you take a ferry,\n"
# 268 "data/maps/SSTidalCorridor/scripts.pory"
	.string "you should be able to sail to\l"
# 269 "data/maps/SSTidalCorridor/scripts.pory"
	.string "the BATTLE FRONTIER.\p"
# 270 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Okay, {PLAYER}{KUN}, I'll be waiting for you\n"
# 271 "data/maps/SSTidalCorridor/scripts.pory"
	.string "at the BATTLE FRONTIER!$"
# 272 "data/maps/SSTidalCorridor/scripts.pory"

# 273 "data/maps/SSTidalCorridor/scripts.pory"
SSTidal_Text_FastCurrentsHopeYouEnjoyVoyage:
# 274 "data/maps/SSTidalCorridor/scripts.pory"
	.string "This ferry is built to plow through\n"
# 275 "data/maps/SSTidalCorridor/scripts.pory"
	.string "fast-running currents.\p"
# 276 "data/maps/SSTidalCorridor/scripts.pory"
	.string "We hope you enjoy your voyage with us.\n"
# 277 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Feel free to explore the ship.$"
# 278 "data/maps/SSTidalCorridor/scripts.pory"

# 279 "data/maps/SSTidalCorridor/scripts.pory"
SSTidal_Text_HopeYouEnjoyVoyage:
# 280 "data/maps/SSTidalCorridor/scripts.pory"
	.string "We hope you enjoy your voyage on\n"
# 281 "data/maps/SSTidalCorridor/scripts.pory"
	.string "our ferry.$"
# 282 "data/maps/SSTidalCorridor/scripts.pory"

# 283 "data/maps/SSTidalCorridor/scripts.pory"
SSTidal_Text_MadeLandInSlateport:
# 284 "data/maps/SSTidalCorridor/scripts.pory"
	.string "We have made land in SLATEPORT CITY.\n"
# 285 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Thank you for sailing with us.$"
# 286 "data/maps/SSTidalCorridor/scripts.pory"

# 287 "data/maps/SSTidalCorridor/scripts.pory"
SSTidal_Text_MadeLandInLilycove:
# 288 "data/maps/SSTidalCorridor/scripts.pory"
	.string "We have made land in LILYCOVE CITY.\n"
# 289 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Thank you for sailing with us.$"
# 290 "data/maps/SSTidalCorridor/scripts.pory"

# 291 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_CanRestInCabin2:
# 292 "data/maps/SSTidalCorridor/scripts.pory"
	.string "It'll be some time before we make land,\n"
# 293 "data/maps/SSTidalCorridor/scripts.pory"
	.string "I reckon.\p"
# 294 "data/maps/SSTidalCorridor/scripts.pory"
	.string "You can rest up in your cabin if you'd\n"
# 295 "data/maps/SSTidalCorridor/scripts.pory"
	.string "like. Your cabin's No. 2.\p"
# 296 "data/maps/SSTidalCorridor/scripts.pory"
	.string "The bed in there is soft and plushy.\n"
# 297 "data/maps/SSTidalCorridor/scripts.pory"
	.string "I can attest to how comfy it is!$"
# 298 "data/maps/SSTidalCorridor/scripts.pory"

# 299 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_WeveArrived:
# 300 "data/maps/SSTidalCorridor/scripts.pory"
	.string "We've arrived!$"
# 301 "data/maps/SSTidalCorridor/scripts.pory"

# 302 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_VisitOtherCabins:
# 303 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Go visit other cabins.\n"
# 304 "data/maps/SSTidalCorridor/scripts.pory"
	.string "TRAINERS bored of the boat trip will\l"
# 305 "data/maps/SSTidalCorridor/scripts.pory"
	.string "be itching to battle.$"
# 306 "data/maps/SSTidalCorridor/scripts.pory"

# 307 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_EnjoyYourCruise:
# 308 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Enjoy your cruise!$"
# 309 "data/maps/SSTidalCorridor/scripts.pory"

# 310 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_HorizonSpreadsBeyondPorthole:
# 311 "data/maps/SSTidalCorridor/scripts.pory"
	.string "The horizon spreads beyond\n"
# 312 "data/maps/SSTidalCorridor/scripts.pory"
	.string "the porthole.$"
# 313 "data/maps/SSTidalCorridor/scripts.pory"

# 314 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_BrineyWelcomeAboard:
# 315 "data/maps/SSTidalCorridor/scripts.pory"
	.string "MR. BRINEY: Welcome aboard, {PLAYER}{KUN}!\p"
# 316 "data/maps/SSTidalCorridor/scripts.pory"
	.string "They made me honorary captain of\n"
# 317 "data/maps/SSTidalCorridor/scripts.pory"
	.string "the S.S. TIDAL!\p"
# 318 "data/maps/SSTidalCorridor/scripts.pory"
	.string "You can call me CAPTAIN BRINEY now!\p"
# 319 "data/maps/SSTidalCorridor/scripts.pory"
	.string "You know, I retired once before,\n"
# 320 "data/maps/SSTidalCorridor/scripts.pory"
	.string "but when I saw this majestic ship…\p"
# 321 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Let me just say, it stirred my sleeping\n"
# 322 "data/maps/SSTidalCorridor/scripts.pory"
	.string "soul as a sailor!$"
# 323 "data/maps/SSTidalCorridor/scripts.pory"

# 324 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_Peeko:
# 325 "data/maps/SSTidalCorridor/scripts.pory"
	.string "PEEKO: Pihyo pihyohyo…$"
# 326 "data/maps/SSTidalCorridor/scripts.pory"

# 327 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_Cabin1:
# 328 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Cabin 1$"
# 329 "data/maps/SSTidalCorridor/scripts.pory"

# 330 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_Cabin2:
# 331 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Cabin 2$"
# 332 "data/maps/SSTidalCorridor/scripts.pory"

# 333 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_Cabin3:
# 334 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Cabin 3$"
# 335 "data/maps/SSTidalCorridor/scripts.pory"

# 336 "data/maps/SSTidalCorridor/scripts.pory"
SSTidalCorridor_Text_Cabin4:
# 337 "data/maps/SSTidalCorridor/scripts.pory"
	.string "Cabin 4$"
