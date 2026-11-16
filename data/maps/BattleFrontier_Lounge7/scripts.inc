# 1 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 2 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_MapScripts::
# 3 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.byte 0
# 4 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 5 "data/maps/BattleFrontier_Lounge7/scripts.pory"
@special ChooseMonForMoveTutor
# 6 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_LeftMoveTutor::
# 7 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	lock
# 8 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	faceplayer
# 9 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_TEMP_C, SCROLL_MULTI_BF_MOVE_TUTOR_1
# 10 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto_if_set FLAG_MET_FRONTIER_BEAUTY_MOVE_TUTOR, BattleFrontier_Lounge7_EventScript_AlreadyMetLeftTutor
# 11 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_LeftTutorIntro, MSGBOX_DEFAULT
# 12 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setflag FLAG_MET_FRONTIER_BEAUTY_MOVE_TUTOR
# 13 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ChooseLeftTutorMove
# 14 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 15 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 16 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_AlreadyMetLeftTutor::
# 17 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_LeftTutorWelcomeBack, MSGBOX_DEFAULT
# 18 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ChooseLeftTutorMove
# 19 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 20 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 21 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ChooseLeftTutorMove::
# 22 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	message BattleFrontier_Lounge7_Text_TeachWhichMove
# 23 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	waitmessage
# 24 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special ShowBattlePointsWindow
# 25 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 0
# 26 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_1
# 27 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8006, 0
# 28 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special ShowScrollableMultichoice
# 29 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
# 30 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	switch VAR_RESULT
# 31 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 0, BattleFrontier_Lounge7_EventScript_Softboiled
# 32 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 1, BattleFrontier_Lounge7_EventScript_SeismicToss
# 33 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 2, BattleFrontier_Lounge7_EventScript_DreamEater
# 34 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 3, BattleFrontier_Lounge7_EventScript_MegaPunch
# 35 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 4, BattleFrontier_Lounge7_EventScript_MegaKick
# 36 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 5, BattleFrontier_Lounge7_EventScript_BodySlam
# 37 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 6, BattleFrontier_Lounge7_EventScript_RockSlide
# 38 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 7, BattleFrontier_Lounge7_EventScript_Counter
# 39 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 8, BattleFrontier_Lounge7_EventScript_ThunderWave
# 40 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 9, BattleFrontier_Lounge7_EventScript_SwordsDance
# 41 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 42 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 43 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 44 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 45 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ChooseNewLeftTutorMove::
# 46 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	message BattleFrontier_Lounge7_Text_TeachWhichMove
# 47 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	waitmessage
# 48 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 0
# 49 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_1
# 50 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8006, 1
# 51 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special ShowScrollableMultichoice
# 52 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
# 53 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	switch VAR_RESULT
# 54 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 0, BattleFrontier_Lounge7_EventScript_Softboiled
# 55 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 1, BattleFrontier_Lounge7_EventScript_SeismicToss
# 56 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 2, BattleFrontier_Lounge7_EventScript_DreamEater
# 57 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 3, BattleFrontier_Lounge7_EventScript_MegaPunch
# 58 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 4, BattleFrontier_Lounge7_EventScript_MegaKick
# 59 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 5, BattleFrontier_Lounge7_EventScript_BodySlam
# 60 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 6, BattleFrontier_Lounge7_EventScript_RockSlide
# 61 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 7, BattleFrontier_Lounge7_EventScript_Counter
# 62 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 8, BattleFrontier_Lounge7_EventScript_ThunderWave
# 63 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 9, BattleFrontier_Lounge7_EventScript_SwordsDance
# 64 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 65 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 66 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 67 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 68 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Softboiled::
# 69 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 16
# 70 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_SOFT_BOILED
# 71 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 72 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 73 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 74 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_SeismicToss::
# 75 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 76 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_SEISMIC_TOSS
# 77 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 78 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 79 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 80 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_DreamEater::
# 81 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 82 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_DREAM_EATER
# 83 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 84 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 85 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 86 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_MegaPunch::
# 87 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 88 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_MEGA_PUNCH
# 89 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 90 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 91 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 92 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_MegaKick::
# 93 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 94 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_MEGA_KICK
# 95 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 96 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 97 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 98 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_BodySlam::
# 99 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 100 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_BODY_SLAM
# 101 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 102 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 103 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 104 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_RockSlide::
# 105 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 106 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_ROCK_SLIDE
# 107 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 108 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 109 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 110 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Counter::
# 111 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 112 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_COUNTER
# 113 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 114 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 115 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 116 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ThunderWave::
# 117 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 118 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_THUNDER_WAVE
# 119 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 120 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 121 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 122 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_SwordsDance::
# 123 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 124 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_SWORDS_DANCE
# 125 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 126 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 127 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 128 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_RightMoveTutor::
# 129 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	lock
# 130 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	faceplayer
# 131 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_TEMP_C, SCROLL_MULTI_BF_MOVE_TUTOR_2
# 132 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto_if_set FLAG_MET_FRONTIER_SWIMMER_MOVE_TUTOR, BattleFrontier_Lounge7_EventScript_AlreadyMetRightTutor
# 133 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_RightTutorIntro, MSGBOX_DEFAULT
# 134 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setflag FLAG_MET_FRONTIER_SWIMMER_MOVE_TUTOR
# 135 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ChooseRightTutorMove
# 136 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 137 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 138 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_AlreadyMetRightTutor::
# 139 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_RightTutorWelcomeBack, MSGBOX_DEFAULT
# 140 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ChooseRightTutorMove
# 141 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 142 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 143 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ChooseRightTutorMove::
# 144 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	message BattleFrontier_Lounge7_Text_TeachWhichMove
# 145 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	waitmessage
# 146 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special ShowBattlePointsWindow
# 147 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 1
# 148 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_2
# 149 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8006, 0
# 150 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special ShowScrollableMultichoice
# 151 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
# 152 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	switch VAR_RESULT
# 153 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 0, BattleFrontier_Lounge7_EventScript_DefenseCurl
# 154 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 1, BattleFrontier_Lounge7_EventScript_Snore
# 155 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 2, BattleFrontier_Lounge7_EventScript_MudSlap
# 156 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 3, BattleFrontier_Lounge7_EventScript_Swift
# 157 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 4, BattleFrontier_Lounge7_EventScript_IcyWind
# 158 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 5, BattleFrontier_Lounge7_EventScript_Endure
# 159 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 6, BattleFrontier_Lounge7_EventScript_PsychUp
# 160 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 7, BattleFrontier_Lounge7_EventScript_IcePunch
# 161 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 8, BattleFrontier_Lounge7_EventScript_ThunderPunch
# 162 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 9, BattleFrontier_Lounge7_EventScript_FirePunch
# 163 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 164 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 165 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 166 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 167 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ChooseNewRightTutorMove::
# 168 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	message BattleFrontier_Lounge7_Text_TeachWhichMove
# 169 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	waitmessage
# 170 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_TEMP_FRONTIER_TUTOR_ID, 1
# 171 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8004, SCROLL_MULTI_BF_MOVE_TUTOR_2
# 172 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8006, 1
# 173 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special ShowScrollableMultichoice
# 174 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	copyvar VAR_TEMP_FRONTIER_TUTOR_SELECTION, VAR_RESULT
# 175 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	switch VAR_RESULT
# 176 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 0, BattleFrontier_Lounge7_EventScript_DefenseCurl
# 177 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 1, BattleFrontier_Lounge7_EventScript_Snore
# 178 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 2, BattleFrontier_Lounge7_EventScript_MudSlap
# 179 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 3, BattleFrontier_Lounge7_EventScript_Swift
# 180 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 4, BattleFrontier_Lounge7_EventScript_IcyWind
# 181 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 5, BattleFrontier_Lounge7_EventScript_Endure
# 182 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 6, BattleFrontier_Lounge7_EventScript_PsychUp
# 183 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 7, BattleFrontier_Lounge7_EventScript_IcePunch
# 184 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 8, BattleFrontier_Lounge7_EventScript_ThunderPunch
# 185 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 9, BattleFrontier_Lounge7_EventScript_FirePunch
# 186 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case 10, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 187 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	case MULTI_B_PRESSED, BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect
# 188 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 189 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 190 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_DefenseCurl::
# 191 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 16
# 192 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_DEFENSE_CURL
# 193 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 194 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 195 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 196 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Snore::
# 197 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 198 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_SNORE
# 199 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 200 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 201 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 202 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_MudSlap::
# 203 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 204 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_MUD_SLAP
# 205 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 206 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 207 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 208 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Swift::
# 209 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 210 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_SWIFT
# 211 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 212 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 213 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 214 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_IcyWind::
# 215 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 24
# 216 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_ICY_WIND
# 217 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 218 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 219 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 220 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Endure::
# 221 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 222 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_ENDURE
# 223 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 224 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 225 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 226 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_PsychUp::
# 227 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 228 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_PSYCH_UP
# 229 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 230 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 231 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 232 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_IcePunch::
# 233 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 234 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_ICE_PUNCH
# 235 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 236 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 237 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 238 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ThunderPunch::
# 239 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 240 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_THUNDER_PUNCH
# 241 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 242 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 243 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 244 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_FirePunch::
# 245 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8008, 48
# 246 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	setvar VAR_0x8005, MOVE_FIRE_PUNCH
# 247 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection
# 248 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 249 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 250 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ExitTutorMoveSelect::
# 251 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special CloseBattleFrontierTutorWindow
# 252 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special CloseBattlePointsWindow
# 253 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_YouDontWantTo, MSGBOX_DEFAULT
# 254 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	release
# 255 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 256 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 257 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_CancelChooseMon::
# 258 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_YouDontWantTo, MSGBOX_DEFAULT
# 259 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	release
# 260 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 261 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 262 "data/maps/BattleFrontier_Lounge7/scripts.pory"
@ VAR_0x8008 is the price
# 263 "data/maps/BattleFrontier_Lounge7/scripts.pory"
@ VAR_TEMP_C is the scroll multichoice ID
# 264 "data/maps/BattleFrontier_Lounge7/scripts.pory"
@ VAR_TEMP_FRONTIER_TUTOR_SELECTION is the move selection
# 265 "data/maps/BattleFrontier_Lounge7/scripts.pory"
@ VAR_TEMP_FRONTIER_TUTOR_ID is which move tutor was spoken to
# 266 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ConfirmMoveSelection::
# 267 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special BufferBattleFrontierTutorMoveName
# 268 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	buffernumberstring STR_VAR_2, VAR_0x8008
# 269 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_MoveWillBeXBattlePoints, MSGBOX_YESNO
# 270 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto_if_eq VAR_RESULT, NO, BattleFrontier_Lounge7_EventScript_ChooseNewMove
# 271 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	specialvar VAR_TEMP_1, GetFrontierBattlePoints
# 272 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto_if_ge VAR_TEMP_1, VAR_0x8008, BattleFrontier_Lounge7_EventScript_TeachTutorMove
# 273 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_HaventGotEnoughPoints, MSGBOX_DEFAULT
# 274 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ChooseNewMove
# 275 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 276 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 277 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 278 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_TeachTutorMove::
# 279 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_TeachMoveToWhichMon, MSGBOX_DEFAULT
# 280 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	fadescreen FADE_TO_BLACK
# 281 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special CloseBattlePointsWindow
# 282 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special CloseBattleFrontierTutorWindow
# 283 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	chooseboxmon SELECT_PC_MON_MOVE_TUTOR
# 284 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	waitstate
# 285 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, BattleFrontier_Lounge7_EventScript_CancelChooseMon
# 286 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_IllTakeBattlePoints, MSGBOX_DEFAULT
# 287 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	copyvar VAR_0x8004, VAR_0x8008
# 288 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	special TakeFrontierBattlePoints
# 289 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	release
# 290 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 291 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 292 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_ChooseNewMove::
# 293 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto_if_eq VAR_TEMP_FRONTIER_TUTOR_ID, 0, BattleFrontier_Lounge7_EventScript_ChooseNewLeftTutorMove
# 294 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	goto BattleFrontier_Lounge7_EventScript_ChooseNewRightTutorMove
# 295 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 296 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 297 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Sailor::
# 298 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_ThinkLadiesDontGetAlong, MSGBOX_NPC
# 299 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 300 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 301 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_EventScript_Gentleman::
# 302 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	msgbox BattleFrontier_Lounge7_Text_LadiesWereStrongAndBeautiful, MSGBOX_NPC
# 303 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	end
# 304 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 305 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_LeftTutorIntro:
# 306 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Buhahaha!\p"
# 307 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "You couldn't tell it from looking now,\n"
# 308 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "but I used to be one tough TRAINER.\p"
# 309 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I had a reputation as the toughest\n"
# 310 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "BEAUTY around, I tell you!\p"
# 311 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "… … … … … …\p"
# 312 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "What is it now?\n"
# 313 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "You don't believe me.\p"
# 314 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I'm not like that blowhard woman over\n"
# 315 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "there. I'm actually talented!\p"
# 316 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Let me prove it to you.\n"
# 317 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I can teach your POKéMON special and\l"
# 318 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "yet cute moves.\p"
# 319 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "But my lessons don't come free.\n"
# 320 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "How about paying for the moves I teach\l"
# 321 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "with a wee bit of Battle Points?$"
# 322 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 323 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_LeftTutorWelcomeBack:
# 324 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Buhahaha!\p"
# 325 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Are you back to learn special and\n"
# 326 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "yet cute POKéMON moves?$"
# 327 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 328 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_TeachWhichMove:
# 329 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Fine, fine, look here!\n"
# 330 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Which move should I teach?$"
# 331 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 332 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_MoveWillBeXBattlePoints:
# 333 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "The move {STR_VAR_1}, is it?\n"
# 334 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "That will be {STR_VAR_2} Battle Points, okay?$"
# 335 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 336 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_TeachMoveToWhichMon:
# 337 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Fine, fine, now pick the POKéMON\n"
# 338 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I should teach the move to.$"
# 339 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 340 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_HaventGotEnoughPoints:
# 341 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "What the…\n"
# 342 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "You haven't got enough Battle Points!$"
# 343 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 344 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_IllTakeBattlePoints:
# 345 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Do you see how skilled I am now?\n"
# 346 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I'll take your Battle Points, thanks!$"
# 347 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 348 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_YouDontWantTo:
# 349 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "What's that?\n"
# 350 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "You don't want to…\p"
# 351 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "If you want to see how skilled I am,\n"
# 352 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "you come see me anytime!$"
# 353 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 354 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_RightTutorIntro:
# 355 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Ihihihi!\p"
# 356 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I know it's hard to see now, but I used\n"
# 357 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "to be one fantastic TRAINER.\p"
# 358 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I had a reputation as the most\n"
# 359 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "invincible SWIMMER around, I tell you!\p"
# 360 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "… … … … … …\p"
# 361 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "What's wrong?\n"
# 362 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "You don't believe me.\p"
# 363 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I'm not like that buffoonish woman over\n"
# 364 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "there. I'm actually experienced!\p"
# 365 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I can prove it to you.\n"
# 366 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "I can teach your POKéMON hard and\l"
# 367 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "yet pretty moves.\p"
# 368 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "But my lessons don't come free.\n"
# 369 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "How about paying for the moves I teach\l"
# 370 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "with a wee bit of Battle Points?$"
# 371 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 372 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_RightTutorWelcomeBack:
# 373 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Ihihihi!\p"
# 374 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Have you come to learn hard and\n"
# 375 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "yet pretty POKéMON moves?$"
# 376 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 377 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_ThinkLadiesDontGetAlong:
# 378 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Those ladies, the way they bad-mouth\n"
# 379 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "each other, you probably think that\l"
# 380 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "they don't get along.\p"
# 381 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "But if that were true, they wouldn't\n"
# 382 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "stay out here together, would they?$"
# 383 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 384 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_LadiesWereStrongAndBeautiful:
# 385 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "When I was just a wee YOUNGSTER,\n"
# 386 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "those ladies were strong and beautiful.\p"
# 387 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "They were idols among us TRAINERS.\p"
# 388 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Even now, age hasn't dulled their\n"
# 389 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "abilities.\p"
# 390 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "In fact, their POKéMON moves have\n"
# 391 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "grown even more polished.\p"
# 392 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "But… For some reason, I can't help\n"
# 393 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "but feel this…\p"
# 394 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Time is so cruel…$"
# 395 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 396 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_SoftboiledDesc::
# 397 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Recovers up to\n"
# 398 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "half the user's\n"
# 399 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "maximum HP.$"
# 400 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 401 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_SeismicTossDesc::
# 402 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Inflicts damage\n"
# 403 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "identical to the\n"
# 404 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "user's level.$"
# 405 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 406 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_DreamEaterDesc::
# 407 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Recovers half the\n"
# 408 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "damage inflicted\n"
# 409 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "on a sleeping foe.$"
# 410 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 411 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_MegaPunchDesc::
# 412 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A strong punch\n"
# 413 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "thrown with\n"
# 414 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "incredible power.$"
# 415 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 416 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_MegaKickDesc::
# 417 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "An extremely\n"
# 418 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "powerful kick with\n"
# 419 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "intense force.$"
# 420 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 421 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_BodySlamDesc::
# 422 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A full-body slam\n"
# 423 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that may cause\n"
# 424 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "paralysis.$"
# 425 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 426 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_RockSlideDesc::
# 427 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Large boulders\n"
# 428 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "are hurled. May\n"
# 429 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "cause flinching.$"
# 430 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 431 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_CounterDesc::
# 432 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Retaliates any\n"
# 433 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "physical hit with\n"
# 434 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "double the power.$"
# 435 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 436 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_ThunderWaveDesc::
# 437 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A weak jolt of\n"
# 438 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "electricity that\n"
# 439 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "paralyzes the foe.$"
# 440 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 441 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_SwordsDanceDesc::
# 442 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A fighting dance\n"
# 443 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that sharply\n"
# 444 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "raises ATTACK.$"
# 445 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 446 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_DefenseCurlDesc::
# 447 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Curls up to con-\n"
# 448 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "ceal weak spots\n"
# 449 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "and raise DEFENSE.$"
# 450 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 451 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_SnoreDesc::
# 452 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A loud attack\n"
# 453 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that can be used\n"
# 454 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "only while asleep.$"
# 455 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 456 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_MudSlapDesc::
# 457 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Hurls mud in the\n"
# 458 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "foe's face to re-\n"
# 459 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "duce its accuracy.$"
# 460 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 461 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_SwiftDesc::
# 462 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Sprays star-\n"
# 463 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "shaped rays\n"
# 464 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that never miss.$"
# 465 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 466 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_IcyWindDesc::
# 467 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A chilling attack\n"
# 468 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that lowers the\n"
# 469 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "foe's SPEED.$"
# 470 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 471 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_EndureDesc::
# 472 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Endures any at-\n"
# 473 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "tack for 1 turn,\n"
# 474 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "leaving 1HP.$"
# 475 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 476 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_PsychUpDesc::
# 477 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "Copies the foe's\n"
# 478 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "effect(s) and\n"
# 479 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "gives to the user.$"
# 480 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 481 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_IcePunchDesc::
# 482 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "An icy punch\n"
# 483 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that may\n"
# 484 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "freeze the foe.$"
# 485 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 486 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_ThunderPunchDesc::
# 487 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "An electrified\n"
# 488 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "punch that may\n"
# 489 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "paralyze the foe.$"
# 490 "data/maps/BattleFrontier_Lounge7/scripts.pory"

# 491 "data/maps/BattleFrontier_Lounge7/scripts.pory"
BattleFrontier_Lounge7_Text_FirePunchDesc::
# 492 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "A fiery punch\n"
# 493 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "that may burn\n"
# 494 "data/maps/BattleFrontier_Lounge7/scripts.pory"
	.string "the foe.$"
