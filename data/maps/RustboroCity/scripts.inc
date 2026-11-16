# 1 "data/maps/RustboroCity/scripts.pory"

# 2 "data/maps/RustboroCity/scripts.pory"
RustboroCity_MapScripts::
# 3 "data/maps/RustboroCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, RustboroCity_OnTransition
# 4 "data/maps/RustboroCity/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, RustboroCity_OnFrame
# 5 "data/maps/RustboroCity/scripts.pory"
	.byte 0
# 6 "data/maps/RustboroCity/scripts.pory"

# 7 "data/maps/RustboroCity/scripts.pory"
RustboroCity_OnTransition:
# 8 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_VISITED_RUSTBORO_CITY
# 9 "data/maps/RustboroCity/scripts.pory"
	call Common_EventScript_SetupRivalGfxId
# 10 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_RUSTBORO_CITY_STATE, 6, RustboroCity_EventScript_HideMapNamePopup
# 11 "data/maps/RustboroCity/scripts.pory"
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
# 12 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RUSTBORO_CITY_STATE, 6, RustboroCity_EventScript_PositionScientistForExit
# 13 "data/maps/RustboroCity/scripts.pory"
	end
# 14 "data/maps/RustboroCity/scripts.pory"

# 15 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_PositionScientistForExit::
# 16 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_TEMP_0, 11, RustboroCity_EventScript_PositionScientistLeftExit
# 17 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_SCIENTIST, 12, 15
# 18 "data/maps/RustboroCity/scripts.pory"
	end
# 19 "data/maps/RustboroCity/scripts.pory"

# 20 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_PositionScientistLeftExit::
# 21 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_SCIENTIST, 11, 15
# 22 "data/maps/RustboroCity/scripts.pory"
	end
# 23 "data/maps/RustboroCity/scripts.pory"

# 24 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_HideMapNamePopup::
# 25 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_HIDE_MAP_NAME_POPUP
# 26 "data/maps/RustboroCity/scripts.pory"
	return
# 27 "data/maps/RustboroCity/scripts.pory"

# 28 "data/maps/RustboroCity/scripts.pory"
RustboroCity_OnFrame:
# 29 "data/maps/RustboroCity/scripts.pory"
	map_script_2 VAR_RUSTBORO_CITY_STATE, 6, RustboroCity_EventScript_ScientistAddMatchCall
# 30 "data/maps/RustboroCity/scripts.pory"
	.2byte 0
# 31 "data/maps/RustboroCity/scripts.pory"

# 32 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ScientistAddMatchCall::
# 33 "data/maps/RustboroCity/scripts.pory"
	lockall
# 34 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_ROUTE104_STATE, 1
# 35 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, RustboroCity_Movement_PlayerWalkDown
# 36 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 37 "data/maps/RustboroCity/scripts.pory"
	playse SE_EXIT
# 38 "data/maps/RustboroCity/scripts.pory"
	delay 10
# 39 "data/maps/RustboroCity/scripts.pory"
	addobject LOCALID_RUSTBORO_SCIENTIST
# 40 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, RustboroCity_Movement_ScientistApproachPlayer
# 41 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 42 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 43 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, Common_Movement_ExclamationMark
# 44 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 45 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, Common_Movement_Delay48
# 46 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 47 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 48 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 49 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, RustboroCity_Movement_ScientistWalkInPlaceDown
# 50 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 51 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_DevelopedNewPokenavFeature, MSGBOX_DEFAULT
# 52 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 53 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_HAS_MATCH_CALL
# 54 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, Common_Movement_WalkInPlaceFasterLeft
# 55 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 56 "data/maps/RustboroCity/scripts.pory"
	playse SE_CLICK
# 57 "data/maps/RustboroCity/scripts.pory"
	delay 10
# 58 "data/maps/RustboroCity/scripts.pory"
	playse SE_CLICK
# 59 "data/maps/RustboroCity/scripts.pory"
	delay 10
# 60 "data/maps/RustboroCity/scripts.pory"
	playse SE_CLICK
# 61 "data/maps/RustboroCity/scripts.pory"
	delay 10
# 62 "data/maps/RustboroCity/scripts.pory"
	playse SE_CLICK
# 63 "data/maps/RustboroCity/scripts.pory"
	delay 20
# 64 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, Common_Movement_WalkInPlaceFasterDown
# 65 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 66 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_AddedMatchCallPleaseCallMrStone, MSGBOX_DEFAULT
# 67 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 68 "data/maps/RustboroCity/scripts.pory"
	delay 20
# 69 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_MatchCallTutorial
# 70 "data/maps/RustboroCity/scripts.pory"

# 71 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_PleaseSelectPokenav::
# 72 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_PleaseSelectPokenav, MSGBOX_DEFAULT
# 73 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 74 "data/maps/RustboroCity/scripts.pory"
	delay 10
# 75 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_MatchCallTutorial
# 76 "data/maps/RustboroCity/scripts.pory"

# 77 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_MatchCallTutorial::
# 78 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_ADDED_MATCH_CALL_TO_POKENAV
# 79 "data/maps/RustboroCity/scripts.pory"
	special ScriptMenu_CreateStartMenuForPokenavTutorial
# 80 "data/maps/RustboroCity/scripts.pory"
	switch VAR_RESULT
# 81 "data/maps/RustboroCity/scripts.pory"
	case 0, RustboroCity_EventScript_PleaseSelectPokenav
# 82 "data/maps/RustboroCity/scripts.pory"
	case 1, RustboroCity_EventScript_PleaseSelectPokenav
# 83 "data/maps/RustboroCity/scripts.pory"
	case 2, RustboroCity_EventScript_PleaseSelectPokenav
# 84 "data/maps/RustboroCity/scripts.pory"
	case 4, RustboroCity_EventScript_PleaseSelectPokenav
# 85 "data/maps/RustboroCity/scripts.pory"
	case 5, RustboroCity_EventScript_PleaseSelectPokenav
# 86 "data/maps/RustboroCity/scripts.pory"
	case 6, RustboroCity_EventScript_PleaseSelectPokenav
# 87 "data/maps/RustboroCity/scripts.pory"
	case 7, RustboroCity_EventScript_PleaseSelectPokenav
# 88 "data/maps/RustboroCity/scripts.pory"
	case MULTI_B_PRESSED, RustboroCity_EventScript_PleaseSelectPokenav
# 89 "data/maps/RustboroCity/scripts.pory"
	special OpenPokenavForTutorial
# 90 "data/maps/RustboroCity/scripts.pory"
	delay 20
# 91 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_IdBetterGetBackToWork, MSGBOX_DEFAULT
# 92 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 93 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_SCIENTIST, RustboroCity_Movement_ScientistLeave
# 94 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 95 "data/maps/RustboroCity/scripts.pory"
	playse SE_EXIT
# 96 "data/maps/RustboroCity/scripts.pory"
	removeobject LOCALID_RUSTBORO_SCIENTIST
# 97 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_HIDE_RUSTBORO_CITY_SCIENTIST
# 98 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTBORO_CITY_STATE, 7
# 99 "data/maps/RustboroCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 100 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 101 "data/maps/RustboroCity/scripts.pory"
	end
# 102 "data/maps/RustboroCity/scripts.pory"

# 103 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_ScientistWalkInPlaceDown:
# 104 "data/maps/RustboroCity/scripts.pory"
	walk_in_place_down
# 105 "data/maps/RustboroCity/scripts.pory"
	step_end
# 106 "data/maps/RustboroCity/scripts.pory"

# 107 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_PlayerWalkDown:
# 108 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 109 "data/maps/RustboroCity/scripts.pory"
	step_end
# 110 "data/maps/RustboroCity/scripts.pory"

# 111 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_ScientistApproachPlayer:
# 112 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 113 "data/maps/RustboroCity/scripts.pory"
	delay_16
# 114 "data/maps/RustboroCity/scripts.pory"
	step_end
# 115 "data/maps/RustboroCity/scripts.pory"

# 116 "data/maps/RustboroCity/scripts.pory"
@ Unused
# 117 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_ScientistWalkAroundPlayer:
# 118 "data/maps/RustboroCity/scripts.pory"
	delay_16
# 119 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 120 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 121 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 122 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 123 "data/maps/RustboroCity/scripts.pory"
	walk_in_place_faster_up
# 124 "data/maps/RustboroCity/scripts.pory"
	delay_16
# 125 "data/maps/RustboroCity/scripts.pory"
	step_end
# 126 "data/maps/RustboroCity/scripts.pory"

# 127 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_ScientistLeave:
# 128 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 129 "data/maps/RustboroCity/scripts.pory"
	step_end
# 130 "data/maps/RustboroCity/scripts.pory"

# 131 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_FatMan::
# 132 "data/maps/RustboroCity/scripts.pory"
	lock
# 133 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 134 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_DEVON_GOODS_STOLEN, RustboroCity_EventScript_FatManSawGrunt
# 135 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_WeShortenItToDevon, MSGBOX_DEFAULT
# 136 "data/maps/RustboroCity/scripts.pory"
	release
# 137 "data/maps/RustboroCity/scripts.pory"
	end
# 138 "data/maps/RustboroCity/scripts.pory"

# 139 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_FatManSawGrunt::
# 140 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_SneakyLookingManWentAroundCorner, MSGBOX_DEFAULT
# 141 "data/maps/RustboroCity/scripts.pory"
	release
# 142 "data/maps/RustboroCity/scripts.pory"
	end
# 143 "data/maps/RustboroCity/scripts.pory"

# 144 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_DevonEmployee2::
# 145 "data/maps/RustboroCity/scripts.pory"
	lock
# 146 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 147 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_YoureNewAroundHere, MSGBOX_DEFAULT
# 148 "data/maps/RustboroCity/scripts.pory"
	release
# 149 "data/maps/RustboroCity/scripts.pory"
	end
# 150 "data/maps/RustboroCity/scripts.pory"

# 151 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Woman::
# 152 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_GymLeaderIsntEasyWithFire, MSGBOX_NPC
# 153 "data/maps/RustboroCity/scripts.pory"
	end
# 154 "data/maps/RustboroCity/scripts.pory"

# 155 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Man1::
# 156 "data/maps/RustboroCity/scripts.pory"
	lock
# 157 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 158 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_BADGE01_GET, RustboroCity_EventScript_Man1HaveBadge
# 159 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_HaveYouChallengedGym, MSGBOX_DEFAULT
# 160 "data/maps/RustboroCity/scripts.pory"
	release
# 161 "data/maps/RustboroCity/scripts.pory"
	end
# 162 "data/maps/RustboroCity/scripts.pory"

# 163 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Man1HaveBadge::
# 164 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_HeyThatsRustborosGymBadge, MSGBOX_DEFAULT
# 165 "data/maps/RustboroCity/scripts.pory"
	release
# 166 "data/maps/RustboroCity/scripts.pory"
	end
# 167 "data/maps/RustboroCity/scripts.pory"

# 168 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Boy2::
# 169 "data/maps/RustboroCity/scripts.pory"
	lock
# 170 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 171 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_RECEIVED_POKENAV, RustboroCity_EventScript_Boy2BrineyLeftTunnel
# 172 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MrBrineyWalksInTheTunnel, MSGBOX_DEFAULT
# 173 "data/maps/RustboroCity/scripts.pory"
	release
# 174 "data/maps/RustboroCity/scripts.pory"
	end
# 175 "data/maps/RustboroCity/scripts.pory"

# 176 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Boy2BrineyLeftTunnel::
# 177 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MrBrineyLovesPeeko, MSGBOX_DEFAULT
# 178 "data/maps/RustboroCity/scripts.pory"
	release
# 179 "data/maps/RustboroCity/scripts.pory"
	end
# 180 "data/maps/RustboroCity/scripts.pory"

# 181 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Twin::
# 182 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_WowYouHavePokemon, MSGBOX_NPC
# 183 "data/maps/RustboroCity/scripts.pory"
	end
# 184 "data/maps/RustboroCity/scripts.pory"

# 185 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_NinjaBoy::
# 186 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_CatchRarePokemonIfIGoToSchool, MSGBOX_SIGN
# 187 "data/maps/RustboroCity/scripts.pory"
	end
# 188 "data/maps/RustboroCity/scripts.pory"

# 189 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_TunnelSign::
# 190 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_TunnelNearingCompletion, MSGBOX_SIGN
# 191 "data/maps/RustboroCity/scripts.pory"
	end
# 192 "data/maps/RustboroCity/scripts.pory"

# 193 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_DevonCorpSign::
# 194 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_DevonCorpSign, MSGBOX_SIGN
# 195 "data/maps/RustboroCity/scripts.pory"
	end
# 196 "data/maps/RustboroCity/scripts.pory"

# 197 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_GymSign::
# 198 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_GymSign, MSGBOX_SIGN
# 199 "data/maps/RustboroCity/scripts.pory"
	end
# 200 "data/maps/RustboroCity/scripts.pory"

# 201 "data/maps/RustboroCity/scripts.pory"
@ Unused
# 202 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_DevonCorpBranchOfficeSign::
# 203 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_DevonCorpBranchOfficeSign, MSGBOX_SIGN
# 204 "data/maps/RustboroCity/scripts.pory"
	end
# 205 "data/maps/RustboroCity/scripts.pory"

# 206 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_CitySign::
# 207 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_CitySign, MSGBOX_SIGN
# 208 "data/maps/RustboroCity/scripts.pory"
	end
# 209 "data/maps/RustboroCity/scripts.pory"

# 210 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_TrainersSchoolSign::
# 211 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_TrainersSchoolSign, MSGBOX_SIGN
# 212 "data/maps/RustboroCity/scripts.pory"
	end
# 213 "data/maps/RustboroCity/scripts.pory"

# 214 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_CuttersHouseSign::
# 215 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_CuttersHouse, MSGBOX_SIGN
# 216 "data/maps/RustboroCity/scripts.pory"
	end
# 217 "data/maps/RustboroCity/scripts.pory"

# 218 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_LittleBoy::
# 219 "data/maps/RustboroCity/scripts.pory"
	lock
# 220 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 221 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_PokemonCanChangeLookFromExp, MSGBOX_DEFAULT
# 222 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_LITTLE_BOY, Common_Movement_FaceOriginalDirection
# 223 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 224 "data/maps/RustboroCity/scripts.pory"
	release
# 225 "data/maps/RustboroCity/scripts.pory"
	end
# 226 "data/maps/RustboroCity/scripts.pory"

# 227 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_LittleGirl::
# 228 "data/maps/RustboroCity/scripts.pory"
	lock
# 229 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 230 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_PokemonChangeShape, MSGBOX_DEFAULT
# 231 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_LITTLE_GIRL, Common_Movement_FaceOriginalDirection
# 232 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 233 "data/maps/RustboroCity/scripts.pory"
	release
# 234 "data/maps/RustboroCity/scripts.pory"
	end
# 235 "data/maps/RustboroCity/scripts.pory"

# 236 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Man2::
# 237 "data/maps/RustboroCity/scripts.pory"
	lock
# 238 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 239 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_TradePokemonGrowFast, MSGBOX_DEFAULT
# 240 "data/maps/RustboroCity/scripts.pory"
	release
# 241 "data/maps/RustboroCity/scripts.pory"
	end
# 242 "data/maps/RustboroCity/scripts.pory"

# 243 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_StolenGoodsTrigger0::
# 244 "data/maps/RustboroCity/scripts.pory"
	lockall
# 245 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_DEVON_EMPLOYEE, 14, 21
# 246 "data/maps/RustboroCity/scripts.pory"
	setobjectmovementtype LOCALID_RUSTBORO_DEVON_EMPLOYEE, MOVEMENT_TYPE_FACE_RIGHT
# 247 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8004, 0
# 248 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_StolenGoodsScene
# 249 "data/maps/RustboroCity/scripts.pory"
	end
# 250 "data/maps/RustboroCity/scripts.pory"

# 251 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_StolenGoodsTrigger1::
# 252 "data/maps/RustboroCity/scripts.pory"
	lockall
# 253 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_DEVON_EMPLOYEE, 14, 21
# 254 "data/maps/RustboroCity/scripts.pory"
	setobjectmovementtype LOCALID_RUSTBORO_DEVON_EMPLOYEE, MOVEMENT_TYPE_FACE_RIGHT
# 255 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8004, 1
# 256 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_StolenGoodsScene
# 257 "data/maps/RustboroCity/scripts.pory"
	end
# 258 "data/maps/RustboroCity/scripts.pory"

# 259 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_StolenGoodsTrigger2::
# 260 "data/maps/RustboroCity/scripts.pory"
	lockall
# 261 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_DEVON_EMPLOYEE, 14, 21
# 262 "data/maps/RustboroCity/scripts.pory"
	setobjectmovementtype LOCALID_RUSTBORO_DEVON_EMPLOYEE, MOVEMENT_TYPE_FACE_RIGHT
# 263 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8004, 2
# 264 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_StolenGoodsScene
# 265 "data/maps/RustboroCity/scripts.pory"
	end
# 266 "data/maps/RustboroCity/scripts.pory"

# 267 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_StolenGoodsTrigger3::
# 268 "data/maps/RustboroCity/scripts.pory"
	lockall
# 269 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_DEVON_EMPLOYEE, 14, 21
# 270 "data/maps/RustboroCity/scripts.pory"
	setobjectmovementtype LOCALID_RUSTBORO_DEVON_EMPLOYEE, MOVEMENT_TYPE_FACE_RIGHT
# 271 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8004, 3
# 272 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_StolenGoodsScene
# 273 "data/maps/RustboroCity/scripts.pory"
	end
# 274 "data/maps/RustboroCity/scripts.pory"

# 275 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_StolenGoodsTrigger4::
# 276 "data/maps/RustboroCity/scripts.pory"
	lockall
# 277 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_DEVON_EMPLOYEE, 14, 21
# 278 "data/maps/RustboroCity/scripts.pory"
	setobjectmovementtype LOCALID_RUSTBORO_DEVON_EMPLOYEE, MOVEMENT_TYPE_FACE_RIGHT
# 279 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8004, 4
# 280 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_StolenGoodsScene
# 281 "data/maps/RustboroCity/scripts.pory"
	end
# 282 "data/maps/RustboroCity/scripts.pory"

# 283 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_StolenGoodsScene::
# 284 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_OutOfTheWay, MSGBOX_DEFAULT
# 285 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 286 "data/maps/RustboroCity/scripts.pory"
	playbgm MUS_ENCOUNTER_AQUA, FALSE
# 287 "data/maps/RustboroCity/scripts.pory"
	addobject LOCALID_RUSTBORO_GRUNT
# 288 "data/maps/RustboroCity/scripts.pory"
	addobject LOCALID_RUSTBORO_DEVON_EMPLOYEE
# 289 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_GRUNT, RustboroCity_Movement_GruntEscape
# 290 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 291 "data/maps/RustboroCity/scripts.pory"
	removeobject LOCALID_RUSTBORO_GRUNT
# 292 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeChaseGrunt1
# 293 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 294 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_WaitDontTakeMyGoods, MSGBOX_DEFAULT
# 295 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 296 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeChaseGrunt2
# 297 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 298 "data/maps/RustboroCity/scripts.pory"
	fadedefaultbgm
# 299 "data/maps/RustboroCity/scripts.pory"
	removeobject LOCALID_RUSTBORO_DEVON_EMPLOYEE
# 300 "data/maps/RustboroCity/scripts.pory"
	setobjectxyperm LOCALID_RUSTBORO_DEVON_EMPLOYEE, 30, 10
# 301 "data/maps/RustboroCity/scripts.pory"
	clearflag FLAG_HIDE_RUSTBORO_CITY_DEVON_EMPLOYEE_1
# 302 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEVON_GOODS_STOLEN
# 303 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTBORO_CITY_STATE, 2
# 304 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTURF_TUNNEL_STATE, 2
# 305 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_ROUTE116_STATE, 1
# 306 "data/maps/RustboroCity/scripts.pory"
	clearflag FLAG_HIDE_ROUTE_116_MR_BRINEY
# 307 "data/maps/RustboroCity/scripts.pory"
	clearflag FLAG_HIDE_RUSTURF_TUNNEL_PEEKO
# 308 "data/maps/RustboroCity/scripts.pory"
	clearflag FLAG_HIDE_RUSTURF_TUNNEL_AQUA_GRUNT
# 309 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
# 310 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
# 311 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 312 "data/maps/RustboroCity/scripts.pory"
	end
# 313 "data/maps/RustboroCity/scripts.pory"

# 314 "data/maps/RustboroCity/scripts.pory"
@ Unused
# 315 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ShadyCharacterTookOff::
# 316 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_ShadyCharacterTookOffTowardsTunnel, MSGBOX_DEFAULT
# 317 "data/maps/RustboroCity/scripts.pory"
	return
# 318 "data/maps/RustboroCity/scripts.pory"

# 319 "data/maps/RustboroCity/scripts.pory"
@ Unused
# 320 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_YouGotItThankYou::
# 321 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_YouGotItThankYou, MSGBOX_DEFAULT
# 322 "data/maps/RustboroCity/scripts.pory"
	return
# 323 "data/maps/RustboroCity/scripts.pory"

# 324 "data/maps/RustboroCity/scripts.pory"
@ Unknown, unused employee movements. Based on the differences in movement theyre for approaching an object (probably the player) in different positions
# 325 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachUp::
# 326 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachUp
# 327 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 328 "data/maps/RustboroCity/scripts.pory"
	return
# 329 "data/maps/RustboroCity/scripts.pory"

# 330 "data/maps/RustboroCity/scripts.pory"
@ Unused, see above
# 331 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachLeft::
# 332 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachLeft
# 333 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 334 "data/maps/RustboroCity/scripts.pory"
	return
# 335 "data/maps/RustboroCity/scripts.pory"

# 336 "data/maps/RustboroCity/scripts.pory"
@ Unused, see above
# 337 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachRight::
# 338 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachRight
# 339 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 340 "data/maps/RustboroCity/scripts.pory"
	return
# 341 "data/maps/RustboroCity/scripts.pory"

# 342 "data/maps/RustboroCity/scripts.pory"
@ Unused, see above
# 343 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachDown::
# 344 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachDown
# 345 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 346 "data/maps/RustboroCity/scripts.pory"
	return
# 347 "data/maps/RustboroCity/scripts.pory"

# 348 "data/maps/RustboroCity/scripts.pory"
@ Unused, similar movement to the above scripts
# 349 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachPlayerFar::
# 350 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachPlayerFar
# 351 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 352 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 353 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 354 "data/maps/RustboroCity/scripts.pory"
	return
# 355 "data/maps/RustboroCity/scripts.pory"

# 356 "data/maps/RustboroCity/scripts.pory"
@ Unused
# 357 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_GruntEscapeExtended:
# 358 "data/maps/RustboroCity/scripts.pory"
	walk_faster_right
# 359 "data/maps/RustboroCity/scripts.pory"
	walk_faster_right
# 360 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 361 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 362 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 363 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 364 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 365 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 366 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 367 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 368 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 369 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 370 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 371 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 372 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 373 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 374 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 375 "data/maps/RustboroCity/scripts.pory"
	step_end
# 376 "data/maps/RustboroCity/scripts.pory"

# 377 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_GruntEscape:
# 378 "data/maps/RustboroCity/scripts.pory"
	walk_faster_right
# 379 "data/maps/RustboroCity/scripts.pory"
	walk_faster_right
# 380 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 381 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 382 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 383 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 384 "data/maps/RustboroCity/scripts.pory"
	walk_fast_right
# 385 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 386 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 387 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 388 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 389 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 390 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 391 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 392 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 393 "data/maps/RustboroCity/scripts.pory"
	walk_fast_up
# 394 "data/maps/RustboroCity/scripts.pory"
	step_end
# 395 "data/maps/RustboroCity/scripts.pory"

# 396 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeChaseGrunt1:
# 397 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 398 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 399 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 400 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 401 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 402 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 403 "data/maps/RustboroCity/scripts.pory"
	walk_in_place_faster_up
# 404 "data/maps/RustboroCity/scripts.pory"
	step_end
# 405 "data/maps/RustboroCity/scripts.pory"

# 406 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeChaseGrunt2:
# 407 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 408 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 409 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 410 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 411 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 412 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 413 "data/maps/RustboroCity/scripts.pory"
	walk_up
# 414 "data/maps/RustboroCity/scripts.pory"
	step_end
# 415 "data/maps/RustboroCity/scripts.pory"

# 416 "data/maps/RustboroCity/scripts.pory"
@ Functionally unused
# 417 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeApproachUp:
# 418 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 419 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 420 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 421 "data/maps/RustboroCity/scripts.pory"
	step_end
# 422 "data/maps/RustboroCity/scripts.pory"

# 423 "data/maps/RustboroCity/scripts.pory"
@ Functionally unused
# 424 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeApproachLeft:
# 425 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 426 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 427 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 428 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 429 "data/maps/RustboroCity/scripts.pory"
	step_end
# 430 "data/maps/RustboroCity/scripts.pory"

# 431 "data/maps/RustboroCity/scripts.pory"
@ Functionally unused
# 432 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeApproachRight:
# 433 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 434 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 435 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 436 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 437 "data/maps/RustboroCity/scripts.pory"
	step_end
# 438 "data/maps/RustboroCity/scripts.pory"

# 439 "data/maps/RustboroCity/scripts.pory"
@ Functionally unused
# 440 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeApproachDown:
# 441 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 442 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 443 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 444 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 445 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 446 "data/maps/RustboroCity/scripts.pory"
	step_end
# 447 "data/maps/RustboroCity/scripts.pory"

# 448 "data/maps/RustboroCity/scripts.pory"
@ Functionally unused
# 449 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeApproachPlayerFar:
# 450 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 451 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 452 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 453 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 454 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 455 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 456 "data/maps/RustboroCity/scripts.pory"
	walk_in_place_faster_down
# 457 "data/maps/RustboroCity/scripts.pory"
	step_end
# 458 "data/maps/RustboroCity/scripts.pory"

# 459 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_DevonEmployee1::
# 460 "data/maps/RustboroCity/scripts.pory"
	lock
# 461 "data/maps/RustboroCity/scripts.pory"
	faceplayer
# 462 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_RECOVERED_DEVON_GOODS, RustboroCity_EventScript_ReturnGoodsSpokeToEmployee
# 463 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_ShadyCharacterTookOffTowardsTunnel, MSGBOX_DEFAULT
# 464 "data/maps/RustboroCity/scripts.pory"
	release
# 465 "data/maps/RustboroCity/scripts.pory"
	end
# 466 "data/maps/RustboroCity/scripts.pory"

# 467 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ReturnGoodsSpokeToEmployee::
# 468 "data/maps/RustboroCity/scripts.pory"
	waitse
# 469 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 4
# 470 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_ReturnGoods
# 471 "data/maps/RustboroCity/scripts.pory"
	end
# 472 "data/maps/RustboroCity/scripts.pory"

# 473 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_HelpGetGoodsTrigger0::
# 474 "data/maps/RustboroCity/scripts.pory"
	lockall
# 475 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 0
# 476 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_EmployeeAskToGetGoods
# 477 "data/maps/RustboroCity/scripts.pory"
	end
# 478 "data/maps/RustboroCity/scripts.pory"

# 479 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_HelpGetGoodsTrigger1::
# 480 "data/maps/RustboroCity/scripts.pory"
	lockall
# 481 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 1
# 482 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_EmployeeAskToGetGoods
# 483 "data/maps/RustboroCity/scripts.pory"
	end
# 484 "data/maps/RustboroCity/scripts.pory"

# 485 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_HelpGetGoodsTrigger2::
# 486 "data/maps/RustboroCity/scripts.pory"
	lockall
# 487 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 2
# 488 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_EmployeeAskToGetGoods
# 489 "data/maps/RustboroCity/scripts.pory"
	end
# 490 "data/maps/RustboroCity/scripts.pory"

# 491 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_HelpGetGoodsTrigger3::
# 492 "data/maps/RustboroCity/scripts.pory"
	lockall
# 493 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 3
# 494 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_EmployeeAskToGetGoods
# 495 "data/maps/RustboroCity/scripts.pory"
	end
# 496 "data/maps/RustboroCity/scripts.pory"

# 497 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeAskToGetGoods::
# 498 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 0, RustboroCity_EventScript_EmployeeFacePlayerUp1
# 499 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 1, RustboroCity_EventScript_EmployeeFacePlayerLeft1
# 500 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 2, RustboroCity_EventScript_EmployeeFacePlayerDown1
# 501 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 3, RustboroCity_EventScript_EmployeeApproachPlayerDown1
# 502 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_INTERACTED_WITH_DEVON_EMPLOYEE_GOODS_STOLEN
# 503 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTBORO_CITY_STATE, 3
# 504 "data/maps/RustboroCity/scripts.pory"
	copyobjectxytoperm LOCALID_RUSTBORO_DEVON_EMPLOYEE
# 505 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_HelpMeIWasRobbed, MSGBOX_DEFAULT
# 506 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 507 "data/maps/RustboroCity/scripts.pory"
	end
# 508 "data/maps/RustboroCity/scripts.pory"

# 509 "data/maps/RustboroCity/scripts.pory"
@ The below movement scripts are either partially or fully duplicated by the movement scripts when the player returns the goods
# 510 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerUp1::
# 511 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterUp
# 512 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 513 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 514 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 515 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 516 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 517 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 518 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
# 519 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 520 "data/maps/RustboroCity/scripts.pory"
	return
# 521 "data/maps/RustboroCity/scripts.pory"

# 522 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerLeft1::
# 523 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterLeft
# 524 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 525 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 526 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 527 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 528 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 529 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 530 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_FaceRight
# 531 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 532 "data/maps/RustboroCity/scripts.pory"
	return
# 533 "data/maps/RustboroCity/scripts.pory"

# 534 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerDown1::
# 535 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterDown
# 536 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 537 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 538 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 539 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 540 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 541 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 542 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 543 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 544 "data/maps/RustboroCity/scripts.pory"
	return
# 545 "data/maps/RustboroCity/scripts.pory"

# 546 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachPlayerDown1::
# 547 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterDown
# 548 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 549 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 550 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 551 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 552 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 553 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 554 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachPlayerDown
# 555 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 556 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 557 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 558 "data/maps/RustboroCity/scripts.pory"
	return
# 559 "data/maps/RustboroCity/scripts.pory"

# 560 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_EmployeeApproachPlayerDown:
# 561 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 562 "data/maps/RustboroCity/scripts.pory"
	step_end
# 563 "data/maps/RustboroCity/scripts.pory"

# 564 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ReturnGoodsTrigger0::
# 565 "data/maps/RustboroCity/scripts.pory"
	lockall
# 566 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 0
# 567 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_ReturnGoods
# 568 "data/maps/RustboroCity/scripts.pory"
	end
# 569 "data/maps/RustboroCity/scripts.pory"

# 570 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ReturnGoodsTrigger1::
# 571 "data/maps/RustboroCity/scripts.pory"
	lockall
# 572 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 1
# 573 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_ReturnGoods
# 574 "data/maps/RustboroCity/scripts.pory"
	end
# 575 "data/maps/RustboroCity/scripts.pory"

# 576 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ReturnGoodsTrigger2::
# 577 "data/maps/RustboroCity/scripts.pory"
	lockall
# 578 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 2
# 579 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_ReturnGoods
# 580 "data/maps/RustboroCity/scripts.pory"
	end
# 581 "data/maps/RustboroCity/scripts.pory"

# 582 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ReturnGoodsTrigger3::
# 583 "data/maps/RustboroCity/scripts.pory"
	lockall
# 584 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_TEMP_1, 3
# 585 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_ReturnGoods
# 586 "data/maps/RustboroCity/scripts.pory"
	end
# 587 "data/maps/RustboroCity/scripts.pory"

# 588 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_ReturnGoods::
# 589 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 0, RustboroCity_EventScript_EmployeeFacePlayerUp2
# 590 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 1, RustboroCity_EventScript_EmployeeFacePlayerLeft2
# 591 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 2, RustboroCity_EventScript_EmployeeFacePlayerDown2
# 592 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 3, RustboroCity_EventScript_EmployeeApproachPlayerDown2
# 593 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_TEMP_1, 4, RustboroCity_EventScript_EmployeeFacePlayerRight
# 594 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_YouGotItThankYou, MSGBOX_DEFAULT
# 595 "data/maps/RustboroCity/scripts.pory"
	giveitem ITEM_GREAT_BALL
# 596 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_RESULT, FALSE, RustboroCity_EventScript_BagFull
# 597 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_PleaseComeWithMe, MSGBOX_DEFAULT
# 598 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 599 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_RETURNED_DEVON_GOODS
# 600 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_HIDE_RUSTBORO_CITY_DEVON_EMPLOYEE_1
# 601 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTBORO_CITY_STATE, 5
# 602 "data/maps/RustboroCity/scripts.pory"
	delay 30
# 603 "data/maps/RustboroCity/scripts.pory"
	warp MAP_RUSTBORO_CITY_DEVON_CORP_3F, 2, 2
# 604 "data/maps/RustboroCity/scripts.pory"
	waitstate
# 605 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 606 "data/maps/RustboroCity/scripts.pory"
	end
# 607 "data/maps/RustboroCity/scripts.pory"

# 608 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BagFull::
# 609 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_YoureLoadedWithItems, MSGBOX_DEFAULT
# 610 "data/maps/RustboroCity/scripts.pory"
	return
# 611 "data/maps/RustboroCity/scripts.pory"

# 612 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerUp2::
# 613 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterUp
# 614 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 615 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 616 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 617 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 618 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 619 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 620 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
# 621 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 622 "data/maps/RustboroCity/scripts.pory"
	return
# 623 "data/maps/RustboroCity/scripts.pory"

# 624 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerLeft2::
# 625 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterRight
# 626 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 627 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 628 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 629 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 630 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 631 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 632 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_FaceLeft
# 633 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 634 "data/maps/RustboroCity/scripts.pory"
	return
# 635 "data/maps/RustboroCity/scripts.pory"

# 636 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerDown2::
# 637 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterDown
# 638 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 639 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 640 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 641 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 642 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 643 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 644 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 645 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 646 "data/maps/RustboroCity/scripts.pory"
	return
# 647 "data/maps/RustboroCity/scripts.pory"

# 648 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeApproachPlayerDown2::
# 649 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterDown
# 650 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 651 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 652 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 653 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 654 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 655 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 656 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, RustboroCity_Movement_EmployeeApproachPlayerDown
# 657 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 658 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 659 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 660 "data/maps/RustboroCity/scripts.pory"
	return
# 661 "data/maps/RustboroCity/scripts.pory"

# 662 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_EmployeeFacePlayerRight::
# 663 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_WalkInPlaceFasterLeft
# 664 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 665 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 666 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_ExclamationMark
# 667 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 668 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_DEVON_EMPLOYEE, Common_Movement_Delay48
# 669 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 670 "data/maps/RustboroCity/scripts.pory"
	return
# 671 "data/maps/RustboroCity/scripts.pory"

# 672 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Rival::
# 673 "data/maps/RustboroCity/scripts.pory"
	lockall
# 674 "data/maps/RustboroCity/scripts.pory"
	call_if_unset FLAG_MET_RIVAL_RUSTBORO, RustboroCity_EventScript_PlayRivalMusic
# 675 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_FacePlayer
# 676 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 677 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 678 "data/maps/RustboroCity/scripts.pory"

# 679 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_PlayRivalMusic::
# 680 "data/maps/RustboroCity/scripts.pory"
	checkplayergender
# 681 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, MALE, RustboroCity_EventScript_PlayMayMusic
# 682 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, FEMALE, RustboroCity_EventScript_PlayBrendanMusic
# 683 "data/maps/RustboroCity/scripts.pory"
	return
# 684 "data/maps/RustboroCity/scripts.pory"

# 685 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_PlayMayMusic::
# 686 "data/maps/RustboroCity/scripts.pory"
	playbgm MUS_ENCOUNTER_MAY, TRUE
# 687 "data/maps/RustboroCity/scripts.pory"
	return
# 688 "data/maps/RustboroCity/scripts.pory"

# 689 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_PlayBrendanMusic::
# 690 "data/maps/RustboroCity/scripts.pory"
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
# 691 "data/maps/RustboroCity/scripts.pory"
	return
# 692 "data/maps/RustboroCity/scripts.pory"

# 693 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger0::
# 694 "data/maps/RustboroCity/scripts.pory"
	lockall
# 695 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 696 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 697 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 698 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 699 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 700 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 701 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 702 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 703 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer0
# 704 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 705 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 706 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 707 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 708 "data/maps/RustboroCity/scripts.pory"

# 709 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger1::
# 710 "data/maps/RustboroCity/scripts.pory"
	lockall
# 711 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 712 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 713 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 714 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 715 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 716 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 717 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 718 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 719 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer1
# 720 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 721 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 722 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 723 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 724 "data/maps/RustboroCity/scripts.pory"

# 725 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger2::
# 726 "data/maps/RustboroCity/scripts.pory"
	lockall
# 727 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 728 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 729 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 730 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 731 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 732 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 733 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 734 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 735 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer2
# 736 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 737 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 738 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 739 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 740 "data/maps/RustboroCity/scripts.pory"

# 741 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger3::
# 742 "data/maps/RustboroCity/scripts.pory"
	lockall
# 743 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 744 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 745 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 746 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 747 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 748 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 749 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 750 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 751 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer3
# 752 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 753 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 754 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 755 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 756 "data/maps/RustboroCity/scripts.pory"

# 757 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger4::
# 758 "data/maps/RustboroCity/scripts.pory"
	lockall
# 759 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 760 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 761 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 762 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 763 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 764 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 765 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 766 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 767 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer4
# 768 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 769 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 770 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 771 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 772 "data/maps/RustboroCity/scripts.pory"

# 773 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger5::
# 774 "data/maps/RustboroCity/scripts.pory"
	lockall
# 775 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 776 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 777 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 778 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 779 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 780 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 781 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 782 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 783 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer5
# 784 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 785 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 786 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 787 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 788 "data/maps/RustboroCity/scripts.pory"

# 789 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger6::
# 790 "data/maps/RustboroCity/scripts.pory"
	lockall
# 791 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 792 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 793 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 794 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 795 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 796 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 797 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 798 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 799 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer6
# 800 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 801 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 802 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 803 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 804 "data/maps/RustboroCity/scripts.pory"

# 805 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalTrigger7::
# 806 "data/maps/RustboroCity/scripts.pory"
	lockall
# 807 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_PlayRivalMusic
# 808 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_WalkInPlaceFasterDown
# 809 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 810 "data/maps/RustboroCity/scripts.pory"
	playse SE_PIN
# 811 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_ExclamationMark
# 812 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 813 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, Common_Movement_Delay48
# 814 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 815 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_RUSTBORO_RIVAL, RustboroCity_Movement_RivalApproachPlayer7
# 816 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 817 "data/maps/RustboroCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 818 "data/maps/RustboroCity/scripts.pory"
	waitmovement 0
# 819 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_RivalEncounter
# 820 "data/maps/RustboroCity/scripts.pory"

# 821 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RivalEncounter::
# 822 "data/maps/RustboroCity/scripts.pory"
	checkplayergender
# 823 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, MALE, RustboroCity_EventScript_MayEncounter
# 824 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, FEMALE, RustboroCity_EventScript_BrendanEncounter
# 825 "data/maps/RustboroCity/scripts.pory"
	end
# 826 "data/maps/RustboroCity/scripts.pory"

# 827 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_MayEncounter::
# 828 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_DEFEATED_RIVAL_RUSTBORO, RustboroCity_EventScript_MayBrineyHint
# 829 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_MET_RIVAL_RUSTBORO, RustboroCity_EventScript_MayAskToBattle
# 830 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_MET_RIVAL_RUSTBORO
# 831 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayHiLetsRegister, MSGBOX_DEFAULT
# 832 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 833 "data/maps/RustboroCity/scripts.pory"
	delay 30
# 834 "data/maps/RustboroCity/scripts.pory"
	playfanfare MUS_REGISTER_MATCH_CALL
# 835 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_RegisteredMay, MSGBOX_DEFAULT
# 836 "data/maps/RustboroCity/scripts.pory"
	waitfanfare
# 837 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 838 "data/maps/RustboroCity/scripts.pory"
	delay 30
# 839 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_ENABLE_RIVAL_MATCH_CALL
# 840 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTBORO_CITY_STATE, 8
# 841 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_ROUTE104_STATE, 2
# 842 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8008, 0
# 843 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayPassedBrineyWantToBattle, MSGBOX_YESNO
# 844 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, YES, RustboroCity_EventScript_BattleMay
# 845 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayOhHaventRaisedPokemonEnough, MSGBOX_DEFAULT
# 846 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_RestoreBgm
# 847 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 848 "data/maps/RustboroCity/scripts.pory"
	end
# 849 "data/maps/RustboroCity/scripts.pory"

# 850 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_MayAskToBattle::
# 851 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_0x8008, 1
# 852 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayWantToBattle, MSGBOX_YESNO
# 853 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, YES, RustboroCity_EventScript_BattleMay
# 854 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayOhHaventRaisedPokemonEnough, MSGBOX_DEFAULT
# 855 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 856 "data/maps/RustboroCity/scripts.pory"
	end
# 857 "data/maps/RustboroCity/scripts.pory"

# 858 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleMay::
# 859 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayImNotGoingToLose, MSGBOX_DEFAULT
# 860 "data/maps/RustboroCity/scripts.pory"
	switch VAR_STARTER_MON
# 861 "data/maps/RustboroCity/scripts.pory"
	case 0, RustboroCity_EventScript_BattleMayTreecko
# 862 "data/maps/RustboroCity/scripts.pory"
	case 1, RustboroCity_EventScript_BattleMayTorchic
# 863 "data/maps/RustboroCity/scripts.pory"
	case 2, RustboroCity_EventScript_BattleMayMudkip
# 864 "data/maps/RustboroCity/scripts.pory"
	end
# 865 "data/maps/RustboroCity/scripts.pory"

# 866 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_MayBrineyHint::
# 867 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_MayMrBrineyHint, MSGBOX_DEFAULT
# 868 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_0x8008, 0, RustboroCity_EventScript_RestoreBgm
# 869 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 870 "data/maps/RustboroCity/scripts.pory"
	end
# 871 "data/maps/RustboroCity/scripts.pory"

# 872 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_RestoreBgm::
# 873 "data/maps/RustboroCity/scripts.pory"
	savebgm MUS_DUMMY
# 874 "data/maps/RustboroCity/scripts.pory"
	fadedefaultbgm
# 875 "data/maps/RustboroCity/scripts.pory"
	return
# 876 "data/maps/RustboroCity/scripts.pory"

# 877 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleMayTreecko::
# 878 "data/maps/RustboroCity/scripts.pory"
	trainerbattle_no_intro TRAINER_MAY_RUSTBORO_TREECKO, RustboroCity_Text_MayDefeat
# 879 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEFEATED_RIVAL_RUSTBORO
# 880 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_MayBrineyHint
# 881 "data/maps/RustboroCity/scripts.pory"
	end
# 882 "data/maps/RustboroCity/scripts.pory"

# 883 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleMayTorchic::
# 884 "data/maps/RustboroCity/scripts.pory"
	trainerbattle_no_intro TRAINER_MAY_RUSTBORO_TORCHIC, RustboroCity_Text_MayDefeat
# 885 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEFEATED_RIVAL_RUSTBORO
# 886 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_MayBrineyHint
# 887 "data/maps/RustboroCity/scripts.pory"
	end
# 888 "data/maps/RustboroCity/scripts.pory"

# 889 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleMayMudkip::
# 890 "data/maps/RustboroCity/scripts.pory"
	trainerbattle_no_intro TRAINER_MAY_RUSTBORO_MUDKIP, RustboroCity_Text_MayDefeat
# 891 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEFEATED_RIVAL_RUSTBORO
# 892 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_MayBrineyHint
# 893 "data/maps/RustboroCity/scripts.pory"
	end
# 894 "data/maps/RustboroCity/scripts.pory"

# 895 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BrendanEncounter::
# 896 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_DEFEATED_RIVAL_RUSTBORO, RustboroCity_EventScript_BrendanBrineyHint
# 897 "data/maps/RustboroCity/scripts.pory"
	goto_if_set FLAG_MET_RIVAL_RUSTBORO, RustboroCity_EventScript_BrendanAskToBattle
# 898 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_MET_RIVAL_RUSTBORO
# 899 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanHiLetsRegister, MSGBOX_DEFAULT
# 900 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 901 "data/maps/RustboroCity/scripts.pory"
	delay 30
# 902 "data/maps/RustboroCity/scripts.pory"
	playfanfare MUS_REGISTER_MATCH_CALL
# 903 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_RegisteredBrendan, MSGBOX_DEFAULT
# 904 "data/maps/RustboroCity/scripts.pory"
	waitfanfare
# 905 "data/maps/RustboroCity/scripts.pory"
	closemessage
# 906 "data/maps/RustboroCity/scripts.pory"
	delay 30
# 907 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_ENABLE_RIVAL_MATCH_CALL
# 908 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_RUSTBORO_CITY_STATE, 8
# 909 "data/maps/RustboroCity/scripts.pory"
	setvar VAR_ROUTE104_STATE, 2
# 910 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanPassedBrineyWantToBattle, MSGBOX_YESNO
# 911 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, YES, RustboroCity_EventScript_BattleBrendan
# 912 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanNoConfidenceInPokemon, MSGBOX_DEFAULT
# 913 "data/maps/RustboroCity/scripts.pory"
	call RustboroCity_EventScript_RestoreBgm
# 914 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 915 "data/maps/RustboroCity/scripts.pory"
	end
# 916 "data/maps/RustboroCity/scripts.pory"

# 917 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BrendanAskToBattle::
# 918 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanWantToBattle, MSGBOX_YESNO
# 919 "data/maps/RustboroCity/scripts.pory"
	goto_if_eq VAR_RESULT, YES, RustboroCity_EventScript_BattleBrendan
# 920 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanNoConfidenceInPokemon, MSGBOX_DEFAULT
# 921 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 922 "data/maps/RustboroCity/scripts.pory"
	end
# 923 "data/maps/RustboroCity/scripts.pory"

# 924 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleBrendan::
# 925 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanIWontGoEasy, MSGBOX_DEFAULT
# 926 "data/maps/RustboroCity/scripts.pory"
	switch VAR_STARTER_MON
# 927 "data/maps/RustboroCity/scripts.pory"
	case 0, RustboroCity_EventScript_BattleBrendanTreecko
# 928 "data/maps/RustboroCity/scripts.pory"
	case 1, RustboroCity_EventScript_BattleBrendanTorchic
# 929 "data/maps/RustboroCity/scripts.pory"
	case 2, RustboroCity_EventScript_BattleBrendanMudkip
# 930 "data/maps/RustboroCity/scripts.pory"
	end
# 931 "data/maps/RustboroCity/scripts.pory"

# 932 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BrendanBrineyHint::
# 933 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_BrendanMrBrineyHint, MSGBOX_DEFAULT
# 934 "data/maps/RustboroCity/scripts.pory"
	call_if_eq VAR_0x8008, 0, RustboroCity_EventScript_RestoreBgm
# 935 "data/maps/RustboroCity/scripts.pory"
	releaseall
# 936 "data/maps/RustboroCity/scripts.pory"
	end
# 937 "data/maps/RustboroCity/scripts.pory"

# 938 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleBrendanTreecko::
# 939 "data/maps/RustboroCity/scripts.pory"
	trainerbattle_no_intro TRAINER_BRENDAN_RUSTBORO_TREECKO, RustboroCity_Text_BrendanDefeat
# 940 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEFEATED_RIVAL_RUSTBORO
# 941 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_BrendanBrineyHint
# 942 "data/maps/RustboroCity/scripts.pory"
	end
# 943 "data/maps/RustboroCity/scripts.pory"

# 944 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleBrendanTorchic::
# 945 "data/maps/RustboroCity/scripts.pory"
	trainerbattle_no_intro TRAINER_BRENDAN_RUSTBORO_TORCHIC, RustboroCity_Text_BrendanDefeat
# 946 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEFEATED_RIVAL_RUSTBORO
# 947 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_BrendanBrineyHint
# 948 "data/maps/RustboroCity/scripts.pory"
	end
# 949 "data/maps/RustboroCity/scripts.pory"

# 950 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_BattleBrendanMudkip::
# 951 "data/maps/RustboroCity/scripts.pory"
	trainerbattle_no_intro TRAINER_BRENDAN_RUSTBORO_MUDKIP, RustboroCity_Text_BrendanDefeat
# 952 "data/maps/RustboroCity/scripts.pory"
	setflag FLAG_DEFEATED_RIVAL_RUSTBORO
# 953 "data/maps/RustboroCity/scripts.pory"
	goto RustboroCity_EventScript_BrendanBrineyHint
# 954 "data/maps/RustboroCity/scripts.pory"
	end
# 955 "data/maps/RustboroCity/scripts.pory"

# 956 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer0:
# 957 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 958 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 959 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 960 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 961 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 962 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 963 "data/maps/RustboroCity/scripts.pory"
	step_end
# 964 "data/maps/RustboroCity/scripts.pory"

# 965 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer1:
# 966 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 967 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 968 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 969 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 970 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 971 "data/maps/RustboroCity/scripts.pory"
	step_end
# 972 "data/maps/RustboroCity/scripts.pory"

# 973 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer2:
# 974 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 975 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 976 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 977 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 978 "data/maps/RustboroCity/scripts.pory"
	step_end
# 979 "data/maps/RustboroCity/scripts.pory"

# 980 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer3:
# 981 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 982 "data/maps/RustboroCity/scripts.pory"
	walk_left
# 983 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 984 "data/maps/RustboroCity/scripts.pory"
	step_end
# 985 "data/maps/RustboroCity/scripts.pory"

# 986 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer4:
# 987 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 988 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 989 "data/maps/RustboroCity/scripts.pory"
	step_end
# 990 "data/maps/RustboroCity/scripts.pory"

# 991 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer5:
# 992 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 993 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 994 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 995 "data/maps/RustboroCity/scripts.pory"
	step_end
# 996 "data/maps/RustboroCity/scripts.pory"

# 997 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer6:
# 998 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 999 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 1000 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 1001 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 1002 "data/maps/RustboroCity/scripts.pory"
	step_end
# 1003 "data/maps/RustboroCity/scripts.pory"

# 1004 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Movement_RivalApproachPlayer7:
# 1005 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 1006 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 1007 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 1008 "data/maps/RustboroCity/scripts.pory"
	walk_right
# 1009 "data/maps/RustboroCity/scripts.pory"
	walk_down
# 1010 "data/maps/RustboroCity/scripts.pory"
	step_end
# 1011 "data/maps/RustboroCity/scripts.pory"

# 1012 "data/maps/RustboroCity/scripts.pory"
RustboroCity_EventScript_Boy1::
# 1013 "data/maps/RustboroCity/scripts.pory"
	msgbox RustboroCity_Text_YouCanHave2On2Battle, MSGBOX_NPC
# 1014 "data/maps/RustboroCity/scripts.pory"
	end
# 1015 "data/maps/RustboroCity/scripts.pory"

# 1016 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_WeShortenItToDevon:
# 1017 "data/maps/RustboroCity/scripts.pory"
	.string "The DEVON CORPORATION…\n"
# 1018 "data/maps/RustboroCity/scripts.pory"
	.string "We all just shorten it to DEVON.\p"
# 1019 "data/maps/RustboroCity/scripts.pory"
	.string "That company makes all sorts of\n"
# 1020 "data/maps/RustboroCity/scripts.pory"
	.string "convenient products.$"
# 1021 "data/maps/RustboroCity/scripts.pory"

# 1022 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_SneakyLookingManWentAroundCorner:
# 1023 "data/maps/RustboroCity/scripts.pory"
	.string "Hm? A sneaky-looking man?\p"
# 1024 "data/maps/RustboroCity/scripts.pory"
	.string "Come to think of it, yes, a shady-\n"
# 1025 "data/maps/RustboroCity/scripts.pory"
	.string "looking guy went around the corner.$"
# 1026 "data/maps/RustboroCity/scripts.pory"

# 1027 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_HaveYouChallengedGym:
# 1028 "data/maps/RustboroCity/scripts.pory"
	.string "Have you taken the POKéMON GYM\n"
# 1029 "data/maps/RustboroCity/scripts.pory"
	.string "challenge?\p"
# 1030 "data/maps/RustboroCity/scripts.pory"
	.string "When you get that shiny GYM BADGE\n"
# 1031 "data/maps/RustboroCity/scripts.pory"
	.string "in hand, I guess TRAINERS begin to\l"
# 1032 "data/maps/RustboroCity/scripts.pory"
	.string "realize what is required of them.$"
# 1033 "data/maps/RustboroCity/scripts.pory"

# 1034 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_HeyThatsRustborosGymBadge:
# 1035 "data/maps/RustboroCity/scripts.pory"
	.string "Hey, that's RUSTBORO's GYM BADGE!\p"
# 1036 "data/maps/RustboroCity/scripts.pory"
	.string "Out of all the POKéMON GYM BADGES,\n"
# 1037 "data/maps/RustboroCity/scripts.pory"
	.string "RUSTBORO's is the coolest, I'd say.$"
# 1038 "data/maps/RustboroCity/scripts.pory"

# 1039 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_YoureNewAroundHere:
# 1040 "data/maps/RustboroCity/scripts.pory"
	.string "Oh? Who might you be?\n"
# 1041 "data/maps/RustboroCity/scripts.pory"
	.string "You're a new face around these parts.\p"
# 1042 "data/maps/RustboroCity/scripts.pory"
	.string "Have you just transferred into the\n"
# 1043 "data/maps/RustboroCity/scripts.pory"
	.string "POKéMON TRAINER'S SCHOOL?$"
# 1044 "data/maps/RustboroCity/scripts.pory"

# 1045 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_GymLeaderIsntEasyWithFire:
# 1046 "data/maps/RustboroCity/scripts.pory"
	.string "I challenged the GYM LEADER, but…\p"
# 1047 "data/maps/RustboroCity/scripts.pory"
	.string "It's not going to be easy winning with\n"
# 1048 "data/maps/RustboroCity/scripts.pory"
	.string "my FIRE-type POKéMON…\p"
# 1049 "data/maps/RustboroCity/scripts.pory"
	.string "FIRE-type POKéMON don't match up\n"
# 1050 "data/maps/RustboroCity/scripts.pory"
	.string "well against ROCK-type POKéMON…$"
# 1051 "data/maps/RustboroCity/scripts.pory"

# 1052 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MrBrineyWalksInTheTunnel:
# 1053 "data/maps/RustboroCity/scripts.pory"
	.string "The old sailor MR. BRINEY lives in\n"
# 1054 "data/maps/RustboroCity/scripts.pory"
	.string "a cottage by the sea.\p"
# 1055 "data/maps/RustboroCity/scripts.pory"
	.string "He goes for walks in the tunnel every\n"
# 1056 "data/maps/RustboroCity/scripts.pory"
	.string "so often.$"
# 1057 "data/maps/RustboroCity/scripts.pory"

# 1058 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MrBrineyLovesPeeko:
# 1059 "data/maps/RustboroCity/scripts.pory"
	.string "The old sailor MR. BRINEY lives in\n"
# 1060 "data/maps/RustboroCity/scripts.pory"
	.string "a cottage by the sea.\p"
# 1061 "data/maps/RustboroCity/scripts.pory"
	.string "He said he was going shopping in\n"
# 1062 "data/maps/RustboroCity/scripts.pory"
	.string "SLATEPORT for his pet, PEEKO.\p"
# 1063 "data/maps/RustboroCity/scripts.pory"
	.string "That old sea dog, he must really love\n"
# 1064 "data/maps/RustboroCity/scripts.pory"
	.string "that PEEKO.$"
# 1065 "data/maps/RustboroCity/scripts.pory"

# 1066 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_WowYouHavePokemon:
# 1067 "data/maps/RustboroCity/scripts.pory"
	.string "Wow, you have POKéMON with you, too.\p"
# 1068 "data/maps/RustboroCity/scripts.pory"
	.string "When I get bigger, I'm going to go\n"
# 1069 "data/maps/RustboroCity/scripts.pory"
	.string "places with POKéMON, too.$"
# 1070 "data/maps/RustboroCity/scripts.pory"

# 1071 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_CatchRarePokemonIfIGoToSchool:
# 1072 "data/maps/RustboroCity/scripts.pory"
	.string "POKéMON TRAINER'S SCHOOL!\p"
# 1073 "data/maps/RustboroCity/scripts.pory"
	.string "If I go to this school, will I be able\n"
# 1074 "data/maps/RustboroCity/scripts.pory"
	.string "to catch rare POKéMON easily?$"
# 1075 "data/maps/RustboroCity/scripts.pory"

# 1076 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_PokemonCanChangeLookFromExp:
# 1077 "data/maps/RustboroCity/scripts.pory"
	.string "If a POKéMON gains experience in\n"
# 1078 "data/maps/RustboroCity/scripts.pory"
	.string "battles, it can sometimes change in\l"
# 1079 "data/maps/RustboroCity/scripts.pory"
	.string "the way it looks.$"
# 1080 "data/maps/RustboroCity/scripts.pory"

# 1081 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_PokemonChangeShape:
# 1082 "data/maps/RustboroCity/scripts.pory"
	.string "A POKéMON changes shape?\n"
# 1083 "data/maps/RustboroCity/scripts.pory"
	.string "If one did that, I would be shocked!$"
# 1084 "data/maps/RustboroCity/scripts.pory"

# 1085 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_TradePokemonGrowFast:
# 1086 "data/maps/RustboroCity/scripts.pory"
	.string "A POKéMON you get in a trade from\n"
# 1087 "data/maps/RustboroCity/scripts.pory"
	.string "someone grows fast.\p"
# 1088 "data/maps/RustboroCity/scripts.pory"
	.string "But if you don't have certain GYM\n"
# 1089 "data/maps/RustboroCity/scripts.pory"
	.string "BADGES, it may not obey you…$"
# 1090 "data/maps/RustboroCity/scripts.pory"

# 1091 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_OutOfTheWay:
# 1092 "data/maps/RustboroCity/scripts.pory"
	.string "Get out!\n"
# 1093 "data/maps/RustboroCity/scripts.pory"
	.string "Out of the way!$"
# 1094 "data/maps/RustboroCity/scripts.pory"

# 1095 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_WaitDontTakeMyGoods:
# 1096 "data/maps/RustboroCity/scripts.pory"
	.string "Wait! Pleeeaaase!\p"
# 1097 "data/maps/RustboroCity/scripts.pory"
	.string "Don't take my GOODS!$"
# 1098 "data/maps/RustboroCity/scripts.pory"

# 1099 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_HelpMeIWasRobbed:
# 1100 "data/maps/RustboroCity/scripts.pory"
	.string "Oh, it's you!\p"
# 1101 "data/maps/RustboroCity/scripts.pory"
	.string "You're that fantastic TRAINER who\n"
# 1102 "data/maps/RustboroCity/scripts.pory"
	.string "helped me in PETALBURG WOODS!\p"
# 1103 "data/maps/RustboroCity/scripts.pory"
	.string "Help me! I was robbed by TEAM AQUA!\n"
# 1104 "data/maps/RustboroCity/scripts.pory"
	.string "I have to get the DEVON GOODS back!\p"
# 1105 "data/maps/RustboroCity/scripts.pory"
	.string "If I don't…\n"
# 1106 "data/maps/RustboroCity/scripts.pory"
	.string "I'm going to be in serious trouble.$"
# 1107 "data/maps/RustboroCity/scripts.pory"

# 1108 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_ShadyCharacterTookOffTowardsTunnel:
# 1109 "data/maps/RustboroCity/scripts.pory"
	.string "That shady character, I think he took\n"
# 1110 "data/maps/RustboroCity/scripts.pory"
	.string "off towards the tunnel over there.$"
# 1111 "data/maps/RustboroCity/scripts.pory"

# 1112 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_YouGotItThankYou:
# 1113 "data/maps/RustboroCity/scripts.pory"
	.string "Oh! How did it go?\n"
# 1114 "data/maps/RustboroCity/scripts.pory"
	.string "The DEVON GOODS?\p"
# 1115 "data/maps/RustboroCity/scripts.pory"
	.string "You did!\n"
# 1116 "data/maps/RustboroCity/scripts.pory"
	.string "You got them back!\p"
# 1117 "data/maps/RustboroCity/scripts.pory"
	.string "You really are a great TRAINER!\p"
# 1118 "data/maps/RustboroCity/scripts.pory"
	.string "I know! As my thanks, I'll give you\n"
# 1119 "data/maps/RustboroCity/scripts.pory"
	.string "another GREAT BALL!$"
# 1120 "data/maps/RustboroCity/scripts.pory"

# 1121 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_YoureLoadedWithItems:
# 1122 "data/maps/RustboroCity/scripts.pory"
	.string "You're loaded with items.\n"
# 1123 "data/maps/RustboroCity/scripts.pory"
	.string "I can't give you this GREAT BALL.$"
# 1124 "data/maps/RustboroCity/scripts.pory"

# 1125 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_PleaseComeWithMe:
# 1126 "data/maps/RustboroCity/scripts.pory"
	.string "Excuse me, please!\n"
# 1127 "data/maps/RustboroCity/scripts.pory"
	.string "Please come with me!$"
# 1128 "data/maps/RustboroCity/scripts.pory"

# 1129 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayHiLetsRegister:
# 1130 "data/maps/RustboroCity/scripts.pory"
	.string "MAY: Oh, hi, {PLAYER}{KUN}!\p"
# 1131 "data/maps/RustboroCity/scripts.pory"
	.string "You had a MATCH CALL feature put\n"
# 1132 "data/maps/RustboroCity/scripts.pory"
	.string "on your POKéNAV!\p"
# 1133 "data/maps/RustboroCity/scripts.pory"
	.string "Let's register each other so we can\n"
# 1134 "data/maps/RustboroCity/scripts.pory"
	.string "contact one another anytime!\p"
# 1135 "data/maps/RustboroCity/scripts.pory"
	.string "… … … … … …$"
# 1136 "data/maps/RustboroCity/scripts.pory"

# 1137 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_RegisteredMay:
# 1138 "data/maps/RustboroCity/scripts.pory"
	.string "Registered MAY\n"
# 1139 "data/maps/RustboroCity/scripts.pory"
	.string "in the POKéNAV.$"
# 1140 "data/maps/RustboroCity/scripts.pory"

# 1141 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayPassedBrineyWantToBattle:
# 1142 "data/maps/RustboroCity/scripts.pory"
	.string "MAY: Oh, by the way, I passed\n"
# 1143 "data/maps/RustboroCity/scripts.pory"
	.string "MR. BRINEY in PETALBURG WOODS.\p"
# 1144 "data/maps/RustboroCity/scripts.pory"
	.string "I guess he's on his way home to his\n"
# 1145 "data/maps/RustboroCity/scripts.pory"
	.string "cottage by the sea.\p"
# 1146 "data/maps/RustboroCity/scripts.pory"
	.string "How's your POKéDEX coming along,\n"
# 1147 "data/maps/RustboroCity/scripts.pory"
	.string "{PLAYER}{KUN}? Mine's looking pretty decent!\p"
# 1148 "data/maps/RustboroCity/scripts.pory"
	.string "So…\n"
# 1149 "data/maps/RustboroCity/scripts.pory"
	.string "How about a little battle?$"
# 1150 "data/maps/RustboroCity/scripts.pory"

# 1151 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayOhHaventRaisedPokemonEnough:
# 1152 "data/maps/RustboroCity/scripts.pory"
	.string "MAY: Oh, what's the matter?\p"
# 1153 "data/maps/RustboroCity/scripts.pory"
	.string "Haven't you caught or raised your\n"
# 1154 "data/maps/RustboroCity/scripts.pory"
	.string "POKéMON very much?\p"
# 1155 "data/maps/RustboroCity/scripts.pory"
	.string "That's not very good for a TRAINER!$"
# 1156 "data/maps/RustboroCity/scripts.pory"

# 1157 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayWantToBattle:
# 1158 "data/maps/RustboroCity/scripts.pory"
	.string "MAY: So, what do you think?\n"
# 1159 "data/maps/RustboroCity/scripts.pory"
	.string "How about a little battle here?$"
# 1160 "data/maps/RustboroCity/scripts.pory"

# 1161 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayImNotGoingToLose:
# 1162 "data/maps/RustboroCity/scripts.pory"
	.string "MAY: You just became a TRAINER,\n"
# 1163 "data/maps/RustboroCity/scripts.pory"
	.string "{PLAYER}{KUN}. I'm not going to lose!$"
# 1164 "data/maps/RustboroCity/scripts.pory"

# 1165 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayDefeat:
# 1166 "data/maps/RustboroCity/scripts.pory"
	.string "Yikes!\n"
# 1167 "data/maps/RustboroCity/scripts.pory"
	.string "You're better than I expected!$"
# 1168 "data/maps/RustboroCity/scripts.pory"

# 1169 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_MayMrBrineyHint:
# 1170 "data/maps/RustboroCity/scripts.pory"
	.string "MAY: Oh, by the way, MR. BRINEY, who\n"
# 1171 "data/maps/RustboroCity/scripts.pory"
	.string "I just passed…\p"
# 1172 "data/maps/RustboroCity/scripts.pory"
	.string "{PLAYER}{KUN}, you just moved here so you\n"
# 1173 "data/maps/RustboroCity/scripts.pory"
	.string "might not know this, but MR. BRINEY\l"
# 1174 "data/maps/RustboroCity/scripts.pory"
	.string "was once a revered seafarer.$"
# 1175 "data/maps/RustboroCity/scripts.pory"

# 1176 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanHiLetsRegister:
# 1177 "data/maps/RustboroCity/scripts.pory"
	.string "BRENDAN: Oh, hey, {PLAYER}!\p"
# 1178 "data/maps/RustboroCity/scripts.pory"
	.string "You had a MATCH CALL feature put\n"
# 1179 "data/maps/RustboroCity/scripts.pory"
	.string "on your POKéNAV! Cool!\p"
# 1180 "data/maps/RustboroCity/scripts.pory"
	.string "Let's register each other so we can\n"
# 1181 "data/maps/RustboroCity/scripts.pory"
	.string "get in touch anytime!\p"
# 1182 "data/maps/RustboroCity/scripts.pory"
	.string "… … … … … …$"
# 1183 "data/maps/RustboroCity/scripts.pory"

# 1184 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_RegisteredBrendan:
# 1185 "data/maps/RustboroCity/scripts.pory"
	.string "Registered BRENDAN\n"
# 1186 "data/maps/RustboroCity/scripts.pory"
	.string "in the POKéNAV.$"
# 1187 "data/maps/RustboroCity/scripts.pory"

# 1188 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanPassedBrineyWantToBattle:
# 1189 "data/maps/RustboroCity/scripts.pory"
	.string "BRENDAN: By the way, {PLAYER}, I walked\n"
# 1190 "data/maps/RustboroCity/scripts.pory"
	.string "by MR. BRINEY in PETALBURG WOODS.\p"
# 1191 "data/maps/RustboroCity/scripts.pory"
	.string "I bet he was on his way home to his\n"
# 1192 "data/maps/RustboroCity/scripts.pory"
	.string "cottage by the sea.\p"
# 1193 "data/maps/RustboroCity/scripts.pory"
	.string "{PLAYER}, how's your POKéDEX?\n"
# 1194 "data/maps/RustboroCity/scripts.pory"
	.string "Have you filled in any pages yet?\p"
# 1195 "data/maps/RustboroCity/scripts.pory"
	.string "Mine rules.\p"
# 1196 "data/maps/RustboroCity/scripts.pory"
	.string "Want to have a battle to test how\n"
# 1197 "data/maps/RustboroCity/scripts.pory"
	.string "far you've progressed?$"
# 1198 "data/maps/RustboroCity/scripts.pory"

# 1199 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanNoConfidenceInPokemon:
# 1200 "data/maps/RustboroCity/scripts.pory"
	.string "BRENDAN: What's the matter? Don't have\n"
# 1201 "data/maps/RustboroCity/scripts.pory"
	.string "any confidence in your POKéMON?$"
# 1202 "data/maps/RustboroCity/scripts.pory"

# 1203 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanWantToBattle:
# 1204 "data/maps/RustboroCity/scripts.pory"
	.string "BRENDAN: What's up?\n"
# 1205 "data/maps/RustboroCity/scripts.pory"
	.string "Want to have a battle with me?$"
# 1206 "data/maps/RustboroCity/scripts.pory"

# 1207 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanIWontGoEasy:
# 1208 "data/maps/RustboroCity/scripts.pory"
	.string "BRENDAN: I know you just became\n"
# 1209 "data/maps/RustboroCity/scripts.pory"
	.string "a TRAINER, but I won't go easy!$"
# 1210 "data/maps/RustboroCity/scripts.pory"

# 1211 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanDefeat:
# 1212 "data/maps/RustboroCity/scripts.pory"
	.string "Hmm…\n"
# 1213 "data/maps/RustboroCity/scripts.pory"
	.string "You're pretty good.$"
# 1214 "data/maps/RustboroCity/scripts.pory"

# 1215 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_BrendanMrBrineyHint:
# 1216 "data/maps/RustboroCity/scripts.pory"
	.string "BRENDAN: By the way, you know\n"
# 1217 "data/maps/RustboroCity/scripts.pory"
	.string "MR. BRINEY? The guy I just passed?\p"
# 1218 "data/maps/RustboroCity/scripts.pory"
	.string "I bet you didn't know this, since you\n"
# 1219 "data/maps/RustboroCity/scripts.pory"
	.string "just moved here, {PLAYER}, but\l"
# 1220 "data/maps/RustboroCity/scripts.pory"
	.string "MR. BRINEY was once a great sailor.$"
# 1221 "data/maps/RustboroCity/scripts.pory"

# 1222 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_TunnelNearingCompletion:
# 1223 "data/maps/RustboroCity/scripts.pory"
	.string "“Timesaving tunnel nearing\n"
# 1224 "data/maps/RustboroCity/scripts.pory"
	.string "completion!”\p"
# 1225 "data/maps/RustboroCity/scripts.pory"
	.string "…Is what it says on the sign, but\n"
# 1226 "data/maps/RustboroCity/scripts.pory"
	.string "there's also a big “X” splashed\l"
# 1227 "data/maps/RustboroCity/scripts.pory"
	.string "across it in red paint…$"
# 1228 "data/maps/RustboroCity/scripts.pory"

# 1229 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_DevonCorpSign:
# 1230 "data/maps/RustboroCity/scripts.pory"
	.string "DEVON CORPORATION\p"
# 1231 "data/maps/RustboroCity/scripts.pory"
	.string "“For all your living needs, we make\n"
# 1232 "data/maps/RustboroCity/scripts.pory"
	.string "it all.”$"
# 1233 "data/maps/RustboroCity/scripts.pory"

# 1234 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_GymSign:
# 1235 "data/maps/RustboroCity/scripts.pory"
	.string "RUSTBORO CITY POKéMON GYM\n"
# 1236 "data/maps/RustboroCity/scripts.pory"
	.string "LEADER: ROXANNE\p"
# 1237 "data/maps/RustboroCity/scripts.pory"
	.string "“The ROCK-loving honors student!”$"
# 1238 "data/maps/RustboroCity/scripts.pory"

# 1239 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_DevonCorpBranchOfficeSign:
# 1240 "data/maps/RustboroCity/scripts.pory"
	.string "DEVON CORP. BRANCH OFFICE\p"
# 1241 "data/maps/RustboroCity/scripts.pory"
	.string "“Access limited to DEVON employees\n"
# 1242 "data/maps/RustboroCity/scripts.pory"
	.string "and authorized personnel.”$"
# 1243 "data/maps/RustboroCity/scripts.pory"

# 1244 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_CitySign:
# 1245 "data/maps/RustboroCity/scripts.pory"
	.string "RUSTBORO CITY\p"
# 1246 "data/maps/RustboroCity/scripts.pory"
	.string "“The city probing the integration of\n"
# 1247 "data/maps/RustboroCity/scripts.pory"
	.string "nature and science.”$"
# 1248 "data/maps/RustboroCity/scripts.pory"

# 1249 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_TrainersSchoolSign:
# 1250 "data/maps/RustboroCity/scripts.pory"
	.string "POKéMON TRAINER'S SCHOOL\p"
# 1251 "data/maps/RustboroCity/scripts.pory"
	.string "“We'll teach you anything about\n"
# 1252 "data/maps/RustboroCity/scripts.pory"
	.string "POKéMON!”$"
# 1253 "data/maps/RustboroCity/scripts.pory"

# 1254 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_CuttersHouse:
# 1255 "data/maps/RustboroCity/scripts.pory"
	.string "CUTTER'S HOUSE$"
# 1256 "data/maps/RustboroCity/scripts.pory"

# 1257 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_DevelopedNewPokenavFeature:
# 1258 "data/maps/RustboroCity/scripts.pory"
	.string "I've been developing an added feature\n"
# 1259 "data/maps/RustboroCity/scripts.pory"
	.string "for the POKéNAV…\p"
# 1260 "data/maps/RustboroCity/scripts.pory"
	.string "And it turned out great!\p"
# 1261 "data/maps/RustboroCity/scripts.pory"
	.string "{PLAYER}, may I see that POKéNAV?\n"
# 1262 "data/maps/RustboroCity/scripts.pory"
	.string "The one our PRESIDENT gave you?$"
# 1263 "data/maps/RustboroCity/scripts.pory"

# 1264 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_AddedMatchCallPleaseCallMrStone:
# 1265 "data/maps/RustboroCity/scripts.pory"
	.string "There you go, {PLAYER}!\p"
# 1266 "data/maps/RustboroCity/scripts.pory"
	.string "I added a new feature named\n"
# 1267 "data/maps/RustboroCity/scripts.pory"
	.string "MATCH CALL to your POKéNAV.\p"
# 1268 "data/maps/RustboroCity/scripts.pory"
	.string "Using the MATCH CALL feature,\n"
# 1269 "data/maps/RustboroCity/scripts.pory"
	.string "you can chat with people who have\l"
# 1270 "data/maps/RustboroCity/scripts.pory"
	.string "been registered in your POKéNAV.\p"
# 1271 "data/maps/RustboroCity/scripts.pory"
	.string "{PLAYER}, our PRESIDENT STONE should\n"
# 1272 "data/maps/RustboroCity/scripts.pory"
	.string "be registered in your POKéNAV.\p"
# 1273 "data/maps/RustboroCity/scripts.pory"
	.string "Test it out.\n"
# 1274 "data/maps/RustboroCity/scripts.pory"
	.string "Please give our PRESIDENT a call.$"
# 1275 "data/maps/RustboroCity/scripts.pory"

# 1276 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_PleaseSelectPokenav:
# 1277 "data/maps/RustboroCity/scripts.pory"
	.string "Please select the POKéNAV.$"
# 1278 "data/maps/RustboroCity/scripts.pory"

# 1279 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_IdBetterGetBackToWork:
# 1280 "data/maps/RustboroCity/scripts.pory"
	.string "Okay, I'd better get back to work.\n"
# 1281 "data/maps/RustboroCity/scripts.pory"
	.string "Please take care, {PLAYER}!$"
# 1282 "data/maps/RustboroCity/scripts.pory"

# 1283 "data/maps/RustboroCity/scripts.pory"
RustboroCity_Text_YouCanHave2On2Battle:
# 1284 "data/maps/RustboroCity/scripts.pory"
	.string "Did you know this?\p"
# 1285 "data/maps/RustboroCity/scripts.pory"
	.string "You can have a 2-on-2 battle even\n"
# 1286 "data/maps/RustboroCity/scripts.pory"
	.string "if you're not with another TRAINER.\p"
# 1287 "data/maps/RustboroCity/scripts.pory"
	.string "If you catch the eyes of two TRAINERS\n"
# 1288 "data/maps/RustboroCity/scripts.pory"
	.string "when you have two or more POKéMON,\l"
# 1289 "data/maps/RustboroCity/scripts.pory"
	.string "they'll both challenge you.\p"
# 1290 "data/maps/RustboroCity/scripts.pory"
	.string "Don't you think it'd be cool if you\n"
# 1291 "data/maps/RustboroCity/scripts.pory"
	.string "could beat two TRAINERS by yourself?$"
