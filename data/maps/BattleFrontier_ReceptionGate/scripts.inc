# 1 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 2 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_MapScripts::
# 3 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, BattleFrontier_ReceptionGate_OnFrame
# 4 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_ReceptionGate_OnTransition
# 5 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.byte 0
# 6 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 7 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_OnTransition:
# 8 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	setflag FLAG_LANDMARK_BATTLE_FRONTIER
# 9 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 10 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 11 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_OnFrame:
# 12 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	map_script_2 VAR_HAS_ENTERED_BATTLE_FRONTIER, 0, BattleFrontier_ReceptionGate_EventScript_FirstTimeEntering
# 13 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.2byte 0
# 14 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 15 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_FirstTimeEntering::
# 16 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	lockall
# 17 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	setvar VAR_HAS_ENTERED_BATTLE_FRONTIER, 1
# 18 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	playse SE_PIN
# 19 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_ExclamationMark
# 20 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 21 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_Delay48
# 22 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 23 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay, MSGBOX_DEFAULT
# 24 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	closemessage
# 25 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_ReceptionGate_Movement_PlayerApproachCounter
# 26 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 27 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ScottScene
# 28 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 29 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 30 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ScottScene::
# 31 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier, MSGBOX_DEFAULT
# 32 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_IssueFrontierPass, MSGBOX_DEFAULT
# 33 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 34 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	message BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass
# 35 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitfanfare
# 36 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmessage
# 37 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass, MSGBOX_DEFAULT
# 38 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	setflag FLAG_SYS_FRONTIER_PASS
# 39 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
# 40 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame, MSGBOX_DEFAULT
# 41 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	closemessage
# 42 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_WalkInPlaceFasterUp
# 43 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, Common_Movement_WalkInPlaceFasterUp
# 44 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 45 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 46 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	playse SE_PIN
# 47 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, Common_Movement_ExclamationMark
# 48 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, Common_Movement_ExclamationMark
# 49 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
# 50 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 51 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay, MSGBOX_DEFAULT
# 52 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	closemessage
# 53 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GREETER, BattleFrontier_ReceptionGate_Movement_GreeterFaceScott
# 54 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_GUIDE, BattleFrontier_ReceptionGate_Movement_FacilityGuideFaceScott
# 55 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_PLAYER, BattleFrontier_ReceptionGate_Movement_PlayerFaceScott
# 56 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_SCOTT, BattleFrontier_ReceptionGate_Movement_ScottEnter
# 57 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 58 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere, MSGBOX_DEFAULT
# 59 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	closemessage
# 60 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	applymovement LOCALID_FRONTIER_RECEPTION_SCOTT, BattleFrontier_ReceptionGate_Movement_ScottExit
# 61 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmovement 0
# 62 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	removeobject LOCALID_FRONTIER_RECEPTION_SCOTT
# 63 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	releaseall
# 64 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 65 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 66 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_PlayerApproachCounter:
# 67 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 68 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 69 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_left
# 70 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_left
# 71 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 72 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 73 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_PlayerFaceScott:
# 74 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 75 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 76 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 77 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_8
# 78 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_in_place_faster_right
# 79 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 80 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 81 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
@ Unused
# 82 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_WalkDown:
# 83 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 84 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 85 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 86 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 87 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_ScottEnter:
# 88 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 89 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 90 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 91 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 92 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 93 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_down
# 94 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_left
# 95 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 96 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 97 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_ScottExit:
# 98 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_right
# 99 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 100 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 101 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 102 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 103 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 104 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_up
# 105 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 106 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 107 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_GreeterFaceScott:
# 108 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 109 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 110 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 111 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_8
# 112 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_in_place_faster_right
# 113 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 114 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 115 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Movement_FacilityGuideFaceScott:
# 116 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 117 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 118 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_16
# 119 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	delay_8
# 120 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	walk_in_place_faster_left
# 121 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	step_end
# 122 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 123 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_Greeter::
# 124 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	lock
# 125 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	faceplayer
# 126 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier, MSGBOX_DEFAULT
# 127 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
# 128 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	release
# 129 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 130 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 131 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_FacilityGuide::
# 132 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	lock
# 133 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	faceplayer
# 134 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToFacilities, MSGBOX_DEFAULT
# 135 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 136 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 137 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 138 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout::
# 139 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhich2
# 140 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmessage
# 141 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	setvar VAR_0x8004, SCROLL_MULTI_BF_RECEPTIONIST
# 142 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	special ShowScrollableMultichoice
# 143 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	switch VAR_RESULT
# 144 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 0, BattleFrontier_ReceptionGate_EventScript_BattleTower
# 145 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 1, BattleFrontier_ReceptionGate_EventScript_BattleDome
# 146 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 2, BattleFrontier_ReceptionGate_EventScript_BattlePalace
# 147 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 3, BattleFrontier_ReceptionGate_EventScript_BattleArena
# 148 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 4, BattleFrontier_ReceptionGate_EventScript_BattleFactory
# 149 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 5, BattleFrontier_ReceptionGate_EventScript_BattlePike
# 150 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 6, BattleFrontier_ReceptionGate_EventScript_BattlePyramid
# 151 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 7, BattleFrontier_ReceptionGate_EventScript_RankingHall
# 152 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 8, BattleFrontier_ReceptionGate_EventScript_ExchangeCorner
# 153 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 9, BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide
# 154 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide
# 155 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 156 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 157 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattleTower::
# 158 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattleTowerInfo, MSGBOX_DEFAULT
# 159 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 160 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 161 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 162 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattleDome::
# 163 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattleDomeInfo, MSGBOX_DEFAULT
# 164 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 165 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 166 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 167 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattlePalace::
# 168 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattlePalaceInfo, MSGBOX_DEFAULT
# 169 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 170 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 171 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 172 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattleArena::
# 173 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattleArenaInfo, MSGBOX_DEFAULT
# 174 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 175 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 176 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 177 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattleFactory::
# 178 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattleFactoryInfo, MSGBOX_DEFAULT
# 179 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 180 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 181 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 182 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattlePike::
# 183 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattlePikeInfo, MSGBOX_DEFAULT
# 184 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 185 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 186 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 187 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattlePyramid::
# 188 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattlePyramidInfo, MSGBOX_DEFAULT
# 189 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 190 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 191 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 192 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_RankingHall::
# 193 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_RankingHallInfo, MSGBOX_DEFAULT
# 194 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 195 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 196 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 197 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ExchangeCorner::
# 198 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo, MSGBOX_DEFAULT
# 199 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFacilityToLearnAbout
# 200 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 201 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 202 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ExitFacilityGuide::
# 203 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
# 204 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	release
# 205 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 206 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 207 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_RulesGuide::
# 208 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	lock
# 209 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	faceplayer
# 210 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToRules, MSGBOX_DEFAULT
# 211 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
# 212 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 213 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 214 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout::
# 215 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhat
# 216 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmessage
# 217 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	multichoice 15, 0, MULTI_FRONTIER_RULES, FALSE
# 218 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	switch VAR_RESULT
# 219 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 0, BattleFrontier_ReceptionGate_EventScript_LevelMode
# 220 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 1, BattleFrontier_ReceptionGate_EventScript_Level50
# 221 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 2, BattleFrontier_ReceptionGate_EventScript_OpenLevel
# 222 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 3, BattleFrontier_ReceptionGate_EventScript_MonEntry
# 223 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 4, BattleFrontier_ReceptionGate_EventScript_HoldItems
# 224 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 5, BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide
# 225 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide
# 226 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 227 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 228 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_LevelMode::
# 229 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_LevelModeInfo, MSGBOX_DEFAULT
# 230 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
# 231 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 232 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 233 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_Level50::
# 234 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_Level50Info, MSGBOX_DEFAULT
# 235 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
# 236 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 237 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 238 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_OpenLevel::
# 239 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_OpenLevelInfo, MSGBOX_DEFAULT
# 240 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
# 241 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 242 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 243 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_MonEntry::
# 244 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_MonEntryInfo, MSGBOX_DEFAULT
# 245 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
# 246 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 247 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 248 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_HoldItems::
# 249 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_HoldItemsInfo, MSGBOX_DEFAULT
# 250 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseRuleToLearnAbout
# 251 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 252 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 253 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ExitRulesGuide::
# 254 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
# 255 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	release
# 256 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 257 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 258 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_FrontierPassGuide::
# 259 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	lock
# 260 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	faceplayer
# 261 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass, MSGBOX_DEFAULT
# 262 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
# 263 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 264 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 265 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout::
# 266 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	message BattleFrontier_ReceptionGate_Text_LearnAboutWhich1
# 267 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	waitmessage
# 268 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	multichoice 16, 4, MULTI_FRONTIER_PASS_INFO, FALSE
# 269 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	switch VAR_RESULT
# 270 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 0, BattleFrontier_ReceptionGate_EventScript_Symbols
# 271 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 1, BattleFrontier_ReceptionGate_EventScript_RecordBattle
# 272 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 2, BattleFrontier_ReceptionGate_EventScript_BattlePoints
# 273 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case 3, BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide
# 274 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide
# 275 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 276 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 277 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_Symbols::
# 278 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_SymbolsInfo, MSGBOX_DEFAULT
# 279 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
# 280 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 281 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 282 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_RecordBattle::
# 283 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_RecordedBattleInfo, MSGBOX_DEFAULT
# 284 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
# 285 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 286 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 287 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_BattlePoints::
# 288 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_BattlePointsInfo, MSGBOX_DEFAULT
# 289 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	goto BattleFrontier_ReceptionGate_EventScript_ChooseFrontierPassInfoToLearnAbout
# 290 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 291 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 292 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_EventScript_ExitFrontierPassGuide::
# 293 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	msgbox BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier, MSGBOX_DEFAULT
# 294 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	release
# 295 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	end
# 296 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 297 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay:
# 298 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Is it your first time here?\n"
# 299 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Please step this way!$"
# 300 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 301 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier:
# 302 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The front lines of POKéMON battling!\n"
# 303 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Welcome to the BATTLE FRONTIER!$"
# 304 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 305 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_IssueFrontierPass:
# 306 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "For a first-time visitor, we issue\n"
# 307 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the FRONTIER PASS.\p"
# 308 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "It's for use at all the facilities\n"
# 309 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "in the BATTLE FRONTIER.\p"
# 310 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Here you are!$"
# 311 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 312 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass:
# 313 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "{PLAYER} obtained\n"
# 314 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the FRONTIER PASS.$"
# 315 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 316 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass:
# 317 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "{PLAYER} placed the TRAINER CARD\n"
# 318 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "in the FRONTIER PASS.$"
# 319 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 320 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier:
# 321 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "We hope you enjoy all that the BATTLE\n"
# 322 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "FRONTIER has to offer!$"
# 323 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 324 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame:
# 325 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "???: Well, if it isn't {PLAYER}{KUN}!\n"
# 326 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "You came out here!$"
# 327 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 328 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay:
# 329 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "GUIDE: Oh! MR. SCOTT, sir!\n"
# 330 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Good day to you, sir!$"
# 331 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 332 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere:
# 333 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "SCOTT: It's great to see you here,\n"
# 334 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "it really is!\p"
# 335 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "I hope you'll take your time and\n"
# 336 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "explore everywhere.\p"
# 337 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Naturally, I hope you'll also experience\n"
# 338 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the pure essence of battling.\p"
# 339 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "I also have my quarters here, so feel\n"
# 340 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "free to visit if you have time.$"
# 341 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 342 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_YourGuideToFacilities:
# 343 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "I'm your guide to the various facilities\n"
# 344 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "here in the BATTLE FRONTIER.$"
# 345 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 346 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_LearnAboutWhich2:
# 347 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Which would you like to learn about?$"
# 348 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 349 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattleTowerInfo:
# 350 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "It is the gigantic tower considered\n"
# 351 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "to be the BATTLE FRONTIER's symbol.\p"
# 352 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "There are four kinds of BATTLE ROOMS\n"
# 353 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "in the tower for SINGLE, DOUBLE, MULTI,\l"
# 354 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "and LINK MULTI BATTLES.$"
# 355 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 356 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattleDomeInfo:
# 357 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The BATTLE DOME is the large building\n"
# 358 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "shaped like a huge egg.\p"
# 359 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Events named Battle Tourneys are held\n"
# 360 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "in this facility.\p"
# 361 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The Battle Tourneys are offered in\n"
# 362 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "two courses--for SINGLE and DOUBLE\l"
# 363 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "BATTLES.$"
# 364 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 365 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattlePalaceInfo:
# 366 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The BATTLE PALACE is the red building\n"
# 367 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "on the right of the BATTLE FRONTIER.\p"
# 368 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "There are two kinds of BATTLE HALLS\n"
# 369 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "for SINGLE and DOUBLE BATTLES.$"
# 370 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 371 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattleArenaInfo:
# 372 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The BATTLE ARENA is the dojo-like\n"
# 373 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "building at the center-right of\l"
# 374 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE FRONTIER.\p"
# 375 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "An event called the Set KO Tourney\n"
# 376 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "takes place at the BATTLE ARENA.$"
# 377 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 378 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattleFactoryInfo:
# 379 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The BATTLE FACTORY is the large\n"
# 380 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "building that is the closest to us.\p"
# 381 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "An event called the Battle Swap\n"
# 382 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "is conducted there.\p"
# 383 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The Battle Swap event is offered in\n"
# 384 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "two courses for SINGLE and DOUBLE\l"
# 385 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "BATTLES.$"
# 386 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 387 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattlePikeInfo:
# 388 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The BATTLE PIKE is the building shaped\n"
# 389 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "like a POKéMON at the center-left of\l"
# 390 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE FRONTIER.\p"
# 391 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "An event called the Battle Choice\n"
# 392 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "is conducted there.$"
# 393 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 394 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattlePyramidInfo:
# 395 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The BATTLE PYRAMID is the enormous\n"
# 396 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "pyramid.\p"
# 397 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "An event called the Battle Quest\n"
# 398 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "is conducted there.$"
# 399 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 400 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_RankingHallInfo:
# 401 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The RANKING HALL is located near\n"
# 402 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE TOWER.\p"
# 403 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "There, you may see the most fantastic\n"
# 404 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "records left by the TRAINERS that\l"
# 405 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "took on the many challenges of\l"
# 406 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE FRONTIER.$"
# 407 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 408 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo:
# 409 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The EXCHANGE SERVICE CORNER is near\n"
# 410 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE TOWER.\p"
# 411 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The Battle Points you have earned in\n"
# 412 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE FRONTIER may be exchanged\l"
# 413 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "for fabulous prizes there.$"
# 414 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 415 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_YourGuideToRules:
# 416 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "I'm your guide to the basic rules that\n"
# 417 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "are common to all the challenges\l"
# 418 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "offered by the facilities in the BATTLE\l"
# 419 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "FRONTIER.$"
# 420 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 421 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_LearnAboutWhat:
# 422 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "What would you like to learn about?$"
# 423 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 424 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_LevelModeInfo:
# 425 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "All the challenges at the BATTLE\n"
# 426 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "FRONTIER's facilities come in\l"
# 427 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "two courses--Level 50 and Open Level.$"
# 428 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 429 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_Level50Info:
# 430 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The Level 50 course is open to POKéMON\n"
# 431 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "up to and including Level 50.\p"
# 432 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Please keep in mind, however, that\n"
# 433 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "no TRAINER you face will have any\l"
# 434 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "POKéMON below Level 50.\p"
# 435 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "This course is the entry level for\n"
# 436 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "battles at the BATTLE FRONTIER.\p"
# 437 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "To begin, we hope you will challenge\n"
# 438 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "this course.$"
# 439 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 440 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_OpenLevelInfo:
# 441 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The Open Level course places no limit\n"
# 442 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "on the levels of POKéMON entering\l"
# 443 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "challenges.\p"
# 444 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The levels of your opponents will\n"
# 445 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "be adjusted to match the levels of\l"
# 446 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "your POKéMON.\p"
# 447 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "However, no TRAINER you face will\n"
# 448 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "have any POKéMON below Level 60.$"
# 449 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 450 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_MonEntryInfo:
# 451 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Virtually any kind of POKéMON may take\n"
# 452 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "on the challenges at all facilities.\p"
# 453 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "EGGS and certain kinds of POKéMON,\n"
# 454 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "however, are not permitted.\p"
# 455 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "The numbers of POKéMON required for\n"
# 456 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "challenges will depend on the facility.\p"
# 457 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "At all facilities, however, two or more\n"
# 458 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "of the same kind of POKéMON are not\l"
# 459 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "permitted.$"
# 460 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 461 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_HoldItemsInfo:
# 462 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "When entering a challenge at a BATTLE\n"
# 463 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "FRONTIER facility, POKéMON may not\l"
# 464 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "be holding the same kind of item.\p"
# 465 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Please make sure that all POKéMON\n"
# 466 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "entering a challenge are holding\l"
# 467 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "different items.$"
# 468 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 469 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass:
# 470 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "I'm your guide to the FRONTIER PASS.$"
# 471 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 472 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_LearnAboutWhich1:
# 473 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Which would you like to learn about?$"
# 474 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 475 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_SymbolsInfo:
# 476 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "There are seven facilities at\n"
# 477 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE FRONTIER.\p"
# 478 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "TRAINERS who gain recognition for\n"
# 479 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "their abilities may be rewarded with\l"
# 480 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "symbols from each of the facilities.\p"
# 481 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "To earn a symbol, TRAINERS may need\n"
# 482 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "to defeat other TRAINERS in a row,\l"
# 483 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "and may need to win events repeatedly.\p"
# 484 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "It's certainly not easy to win symbols.\n"
# 485 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "I wish you the best of luck!$"
# 486 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 487 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_RecordedBattleInfo:
# 488 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "It is possible to record one battle\n"
# 489 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "on your FRONTIER PASS.\p"
# 490 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "You may record a battle you had with\n"
# 491 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "a friend or friends.\p"
# 492 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Or you may record a battle conducted\n"
# 493 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "at the BATTLE FRONTIER excluding\l"
# 494 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "matches at the BATTLE PIKE or\l"
# 495 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "the BATTLE PYRAMID.\p"
# 496 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "You may choose to record your match\n"
# 497 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "at the end of a battle.$"
# 498 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"

# 499 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
BattleFrontier_ReceptionGate_Text_BattlePointsInfo:
# 500 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "Battle Points are rewards given to\n"
# 501 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "TRAINERS who battled outstandingly\l"
# 502 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "at the BATTLE FRONTIER.\p"
# 503 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "You may trade in your Battle Points\n"
# 504 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "for prizes at the EXCHANGE SERVICE\l"
# 505 "data/maps/BattleFrontier_ReceptionGate/scripts.pory"
	.string "CORNER.$"
