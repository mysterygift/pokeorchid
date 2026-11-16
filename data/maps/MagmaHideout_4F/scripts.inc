# 1 "data/maps/MagmaHideout_4F/scripts.pory"

# 2 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_MapScripts::
# 3 "data/maps/MagmaHideout_4F/scripts.pory"
	.byte 0
# 4 "data/maps/MagmaHideout_4F/scripts.pory"

# 5 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_EventScript_Maxie::
# 6 "data/maps/MagmaHideout_4F/scripts.pory"
	lockall
# 7 "data/maps/MagmaHideout_4F/scripts.pory"
	playbgm MUS_ENCOUNTER_MAGMA, FALSE
# 8 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_MaxieAwakenGroudon, MSGBOX_DEFAULT
# 9 "data/maps/MagmaHideout_4F/scripts.pory"
	closemessage
# 10 "data/maps/MagmaHideout_4F/scripts.pory"
	delay 20
# 11 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_RESULT, 1
# 12 "data/maps/MagmaHideout_4F/scripts.pory"
	playse SE_M_DETECT
# 13 "data/maps/MagmaHideout_4F/scripts.pory"
	dofieldeffectsparkle 18, 42, 0
# 14 "data/maps/MagmaHideout_4F/scripts.pory"
	waitfieldeffect FLDEFF_SPARKLE
# 15 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_RESULT, 1
# 16 "data/maps/MagmaHideout_4F/scripts.pory"
	playfanfare MUS_AWAKEN_LEGEND
# 17 "data/maps/MagmaHideout_4F/scripts.pory"
	playse SE_ORB
# 18 "data/maps/MagmaHideout_4F/scripts.pory"
	special DoOrbEffect
# 19 "data/maps/MagmaHideout_4F/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 20 "data/maps/MagmaHideout_4F/scripts.pory"
	waitmovement 0
# 21 "data/maps/MagmaHideout_4F/scripts.pory"
	delay 150
# 22 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GROUDON_SLEEPING
# 23 "data/maps/MagmaHideout_4F/scripts.pory"
	addobject LOCALID_MAGMA_HIDEOUT_4F_GROUDON
# 24 "data/maps/MagmaHideout_4F/scripts.pory"
	waitstate
# 25 "data/maps/MagmaHideout_4F/scripts.pory"
	delay 60
# 26 "data/maps/MagmaHideout_4F/scripts.pory"
	applymovement LOCALID_MAGMA_HIDEOUT_4F_GROUDON, MagmaHideout_4F_Movement_GroudonApproach
# 27 "data/maps/MagmaHideout_4F/scripts.pory"
	waitmovement 0
# 28 "data/maps/MagmaHideout_4F/scripts.pory"
	special FadeOutOrbEffect
# 29 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 30 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 31 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 32 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 33 "data/maps/MagmaHideout_4F/scripts.pory"
	special ShakeCamera
# 34 "data/maps/MagmaHideout_4F/scripts.pory"
	waitstate
# 35 "data/maps/MagmaHideout_4F/scripts.pory"
	applymovement LOCALID_MAGMA_HIDEOUT_4F_GROUDON, MagmaHideout_4F_Movement_GroudonExit
# 36 "data/maps/MagmaHideout_4F/scripts.pory"
	waitmovement 0
# 37 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GROUDON
# 38 "data/maps/MagmaHideout_4F/scripts.pory"
	delay 4
# 39 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8004, 2  @ vertical pan
# 40 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8005, 2  @ horizontal pan
# 41 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 42 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 43 "data/maps/MagmaHideout_4F/scripts.pory"
	special ShakeCamera
# 44 "data/maps/MagmaHideout_4F/scripts.pory"
	waitstate
# 45 "data/maps/MagmaHideout_4F/scripts.pory"
	delay 30
# 46 "data/maps/MagmaHideout_4F/scripts.pory"
	applymovement LOCALID_MAGMA_HIDEOUT_4F_MAXIE, MagmaHideout_4F_Movement_MaxieLookAround
# 47 "data/maps/MagmaHideout_4F/scripts.pory"
	waitmovement 0
# 48 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_MaxieGroudonWhatsWrong, MSGBOX_DEFAULT
# 49 "data/maps/MagmaHideout_4F/scripts.pory"
	closemessage
# 50 "data/maps/MagmaHideout_4F/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
# 51 "data/maps/MagmaHideout_4F/scripts.pory"
	waitmovement 0
# 52 "data/maps/MagmaHideout_4F/scripts.pory"
	delay 30
# 53 "data/maps/MagmaHideout_4F/scripts.pory"
	applymovement LOCALID_MAGMA_HIDEOUT_4F_MAXIE, Common_Movement_FacePlayer
# 54 "data/maps/MagmaHideout_4F/scripts.pory"
	waitmovement 0
# 55 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_MaxieOhItWasYou, MSGBOX_DEFAULT
# 56 "data/maps/MagmaHideout_4F/scripts.pory"
	closemessage
# 57 "data/maps/MagmaHideout_4F/scripts.pory"
	trainerbattle_no_intro TRAINER_MAXIE_MAGMA_HIDEOUT, MagmaHideout_4F_Text_MaxieDefeat
# 58 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_MaxieImGoingAfterGroudon, MSGBOX_DEFAULT
# 59 "data/maps/MagmaHideout_4F/scripts.pory"
	closemessage
# 60 "data/maps/MagmaHideout_4F/scripts.pory"
	clearflag FLAG_HIDE_SLATEPORT_CITY_CAPTAIN_STERN
# 61 "data/maps/MagmaHideout_4F/scripts.pory"
	clearflag FLAG_HIDE_SLATEPORT_CITY_GABBY_AND_TY
# 62 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_SLATEPORT_CITY_STATE, 1
# 63 "data/maps/MagmaHideout_4F/scripts.pory"
	setflag FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT
# 64 "data/maps/MagmaHideout_4F/scripts.pory"
	setvar VAR_SLATEPORT_HARBOR_STATE, 1
# 65 "data/maps/MagmaHideout_4F/scripts.pory"
	fadescreen FADE_TO_BLACK
# 66 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_MAXIE
# 67 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GRUNT_1
# 68 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GRUNT_2
# 69 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_GRUNT_3
# 70 "data/maps/MagmaHideout_4F/scripts.pory"
	removeobject LOCALID_MAGMA_HIDEOUT_4F_TABITHA
# 71 "data/maps/MagmaHideout_4F/scripts.pory"
	setflag FLAG_HIDE_MAGMA_HIDEOUT_GRUNTS
# 72 "data/maps/MagmaHideout_4F/scripts.pory"
	fadescreen FADE_FROM_BLACK
# 73 "data/maps/MagmaHideout_4F/scripts.pory"
	releaseall
# 74 "data/maps/MagmaHideout_4F/scripts.pory"
	end
# 75 "data/maps/MagmaHideout_4F/scripts.pory"

# 76 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Movement_GroudonApproach:
# 77 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 78 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 79 "data/maps/MagmaHideout_4F/scripts.pory"
	walk_slow_down
# 80 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 81 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 82 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 83 "data/maps/MagmaHideout_4F/scripts.pory"
	walk_slow_down
# 84 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 85 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 86 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 87 "data/maps/MagmaHideout_4F/scripts.pory"
	step_end
# 88 "data/maps/MagmaHideout_4F/scripts.pory"

# 89 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Movement_GroudonExit:
# 90 "data/maps/MagmaHideout_4F/scripts.pory"
	slide_up
# 91 "data/maps/MagmaHideout_4F/scripts.pory"
	slide_up
# 92 "data/maps/MagmaHideout_4F/scripts.pory"
	step_end
# 93 "data/maps/MagmaHideout_4F/scripts.pory"

# 94 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Movement_MaxieLookAround:
# 95 "data/maps/MagmaHideout_4F/scripts.pory"
	face_left
# 96 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 97 "data/maps/MagmaHideout_4F/scripts.pory"
	face_right
# 98 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 99 "data/maps/MagmaHideout_4F/scripts.pory"
	face_left
# 100 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 101 "data/maps/MagmaHideout_4F/scripts.pory"
	face_right
# 102 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 103 "data/maps/MagmaHideout_4F/scripts.pory"
	face_up
# 104 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 105 "data/maps/MagmaHideout_4F/scripts.pory"
	delay_16
# 106 "data/maps/MagmaHideout_4F/scripts.pory"
	step_end
# 107 "data/maps/MagmaHideout_4F/scripts.pory"

# 108 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_EventScript_Grunt11::
# 109 "data/maps/MagmaHideout_4F/scripts.pory"
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_11, MagmaHideout_4F_Text_Grunt11Intro, MagmaHideout_4F_Text_Grunt11Defeat
# 110 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_Grunt11PostBattle, MSGBOX_AUTOCLOSE
# 111 "data/maps/MagmaHideout_4F/scripts.pory"
	end
# 112 "data/maps/MagmaHideout_4F/scripts.pory"

# 113 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_EventScript_Grunt12::
# 114 "data/maps/MagmaHideout_4F/scripts.pory"
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_12, MagmaHideout_4F_Text_Grunt12Intro, MagmaHideout_4F_Text_Grunt12Defeat
# 115 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_Grunt12PostBattle, MSGBOX_AUTOCLOSE
# 116 "data/maps/MagmaHideout_4F/scripts.pory"
	end
# 117 "data/maps/MagmaHideout_4F/scripts.pory"

# 118 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_EventScript_Grunt13::
# 119 "data/maps/MagmaHideout_4F/scripts.pory"
	trainerbattle_single TRAINER_GRUNT_MAGMA_HIDEOUT_13, MagmaHideout_4F_Text_Grunt13Intro, MagmaHideout_4F_Text_Grunt13Defeat
# 120 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_Grunt13PostBattle, MSGBOX_AUTOCLOSE
# 121 "data/maps/MagmaHideout_4F/scripts.pory"
	end
# 122 "data/maps/MagmaHideout_4F/scripts.pory"

# 123 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_EventScript_Tabitha::
# 124 "data/maps/MagmaHideout_4F/scripts.pory"
	trainerbattle_single TRAINER_TABITHA_MAGMA_HIDEOUT, MagmaHideout_4F_Text_TabithaIntro, MagmaHideout_4F_Text_TabithaDefeat
# 125 "data/maps/MagmaHideout_4F/scripts.pory"
	msgbox MagmaHideout_4F_Text_TabithaPostBattle, MSGBOX_AUTOCLOSE
# 126 "data/maps/MagmaHideout_4F/scripts.pory"
	end
# 127 "data/maps/MagmaHideout_4F/scripts.pory"

# 128 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt11Intro:
# 129 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I want to see GROUDON, too, but they\n"
# 130 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "won't let me see even its tail…\p"
# 131 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "It's got me feeling really frustrated.\p"
# 132 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Oh, no!\n"
# 133 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I blabbed about GROUDON!$"
# 134 "data/maps/MagmaHideout_4F/scripts.pory"

# 135 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt11Defeat:
# 136 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I guess it's impossible to win if one\n"
# 137 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "doesn't have a calm mind…$"
# 138 "data/maps/MagmaHideout_4F/scripts.pory"

# 139 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt11PostBattle:
# 140 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I wonder if GROUDON even has a tail?$"
# 141 "data/maps/MagmaHideout_4F/scripts.pory"

# 142 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt12Intro:
# 143 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Fuhahaha!\n"
# 144 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Soon! Very soon!\l"
# 145 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Our grand objective will be achieved!$"
# 146 "data/maps/MagmaHideout_4F/scripts.pory"

# 147 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt12Defeat:
# 148 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Grrr…\n"
# 149 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I've come so far, but now this?$"
# 150 "data/maps/MagmaHideout_4F/scripts.pory"

# 151 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt12PostBattle:
# 152 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE, sir!\n"
# 153 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "An intruder is headed your way!$"
# 154 "data/maps/MagmaHideout_4F/scripts.pory"

# 155 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt13Intro:
# 156 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "You're not finished yet!\n"
# 157 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "You're not getting by me easily!$"
# 158 "data/maps/MagmaHideout_4F/scripts.pory"

# 159 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt13Defeat:
# 160 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Was I that easy to knock down?$"
# 161 "data/maps/MagmaHideout_4F/scripts.pory"

# 162 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_Grunt13PostBattle:
# 163 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "C-come on, one more match…$"
# 164 "data/maps/MagmaHideout_4F/scripts.pory"

# 165 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_TabithaIntro:
# 166 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Hehehe!\n"
# 167 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "You made it this far, so I'll tell you!\p"
# 168 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "That's right!\n"
# 169 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Up ahead, GROUDON is sleeping!\p"
# 170 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE went to GROUDON just seconds\n"
# 171 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "ago!\p"
# 172 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "It's going to awaken real soon!\n"
# 173 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Hehe! Hehehe!$"
# 174 "data/maps/MagmaHideout_4F/scripts.pory"

# 175 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_TabithaDefeat:
# 176 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Taken down again…\n"
# 177 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Hehe…$"
# 178 "data/maps/MagmaHideout_4F/scripts.pory"

# 179 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_TabithaPostBattle:
# 180 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "…And while you wasted time with me,\n"
# 181 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE should have awakened GROUDON…$"
# 182 "data/maps/MagmaHideout_4F/scripts.pory"

# 183 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_MaxieAwakenGroudon:
# 184 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE: GROUDON…\p"
# 185 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Nothing could awaken you from your\n"
# 186 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "sleep bathed in magma…\p"
# 187 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "This BLUE ORB is what you sought.\n"
# 188 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Wasn't it?\p"
# 189 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I have brought you the BLUE ORB.\n"
# 190 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Let its shine awaken you!\p"
# 191 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "And show me…\n"
# 192 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Show me the full extent of your power!$"
# 193 "data/maps/MagmaHideout_4F/scripts.pory"

# 194 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_MaxieGroudonWhatsWrong:
# 195 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE: GROUDON!\n"
# 196 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "What's wrong?\p"
# 197 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Wasn't the BLUE ORB the key?\p"
# 198 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "GROUDON!\n"
# 199 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Where have you gone…$"
# 200 "data/maps/MagmaHideout_4F/scripts.pory"

# 201 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_MaxieOhItWasYou:
# 202 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE: Oh, so it was you?\p"
# 203 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I've seen you poking around uninvited\n"
# 204 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "here and there…\p"
# 205 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I get it now!\n"
# 206 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "You must have pulled a cheap stunt!$"
# 207 "data/maps/MagmaHideout_4F/scripts.pory"

# 208 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_MaxieDefeat:
# 209 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "What makes you so adept at handling\n"
# 210 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "POKéMON?$"
# 211 "data/maps/MagmaHideout_4F/scripts.pory"

# 212 "data/maps/MagmaHideout_4F/scripts.pory"
MagmaHideout_4F_Text_MaxieImGoingAfterGroudon:
# 213 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "MAXIE: There has to be some reason\n"
# 214 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "why GROUDON fled…\p"
# 215 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "That's what you're trying to say,\n"
# 216 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "aren't you?\p"
# 217 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "… … … … … …\n"
# 218 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "… … … … … …\p"
# 219 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "Humph…\n"
# 220 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "You think I didn't know that?\p"
# 221 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "With GROUDON gone, there is no longer\n"
# 222 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "any need for this blasted volcano.\p"
# 223 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "I am going after GROUDON, so this\n"
# 224 "data/maps/MagmaHideout_4F/scripts.pory"
	.string "is where we part!$"
