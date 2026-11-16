# 1 "data/maps/PetalburgCity/scripts.pory"

# 2 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_MapScripts::
# 3 "data/maps/PetalburgCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, PetalburgCity_OnTransition
# 4 "data/maps/PetalburgCity/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, PetalburgCity_OnFrame
# 5 "data/maps/PetalburgCity/scripts.pory"
	.byte 0
# 6 "data/maps/PetalburgCity/scripts.pory"

# 7 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_OnTransition:
# 8 "data/maps/PetalburgCity/scripts.pory"
	setflag FLAG_VISITED_PETALBURG_CITY
# 9 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_PETALBURG_CITY_STATE, 0, PetalburgCity_EventScript_MoveGymBoyToWestEntrance
# 10 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_PETALBURG_CITY_STATE, 2, PetalburgCity_EventScript_DisableMapNameAndMusic
# 11 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_PETALBURG_CITY_STATE, 4, PetalburgCity_EventScript_DisableMapNameAndMusic
# 12 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_PETALBURG_GYM_STATE, 8, PetalburgCity_EventScript_SetGymDoorsUnlocked
# 13 "data/maps/PetalburgCity/scripts.pory"
	end
# 14 "data/maps/PetalburgCity/scripts.pory"

# 15 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_MoveGymBoyToWestEntrance::
# 16 "data/maps/PetalburgCity/scripts.pory"
	setobjectxyperm LOCALID_GYM_BOY, 5, 11
# 17 "data/maps/PetalburgCity/scripts.pory"
	return
# 18 "data/maps/PetalburgCity/scripts.pory"

# 19 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_DisableMapNameAndMusic::
# 20 "data/maps/PetalburgCity/scripts.pory"
	setflag FLAG_HIDE_MAP_NAME_POPUP
# 21 "data/maps/PetalburgCity/scripts.pory"
	savebgm MUS_FOLLOW_ME
# 22 "data/maps/PetalburgCity/scripts.pory"
	return
# 23 "data/maps/PetalburgCity/scripts.pory"

# 24 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_SetGymDoorsUnlocked::
# 25 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_PETALBURG_GYM_STATE, 7
# 26 "data/maps/PetalburgCity/scripts.pory"
	return
# 27 "data/maps/PetalburgCity/scripts.pory"

# 28 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_OnFrame:
# 29 "data/maps/PetalburgCity/scripts.pory"
	map_script_2 VAR_PETALBURG_CITY_STATE, 2, PetalburgCity_EventScript_WallyTutorial
# 30 "data/maps/PetalburgCity/scripts.pory"
	map_script_2 VAR_PETALBURG_CITY_STATE, 4, PetalburgCity_EventScript_WalkToWallyHouse
# 31 "data/maps/PetalburgCity/scripts.pory"
	.2byte 0
# 32 "data/maps/PetalburgCity/scripts.pory"

# 33 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_WallyTutorial::
# 34 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 35 "data/maps/PetalburgCity/scripts.pory"
	special SavePlayerParty
# 36 "data/maps/PetalburgCity/scripts.pory"
	special LoadWallyZigzagoon
# 37 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_WALLY, PetalburgCity_Movement_WallyTutorialWally
# 38 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_WallyTutorialPlayer
# 39 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 40 "data/maps/PetalburgCity/scripts.pory"
	msgbox Route102_Text_WatchMeCatchPokemon, MSGBOX_DEFAULT
# 41 "data/maps/PetalburgCity/scripts.pory"
	special StartWallyTutorialBattle
# 42 "data/maps/PetalburgCity/scripts.pory"
	msgbox Route102_Text_WallyIDidIt, MSGBOX_DEFAULT
# 43 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_WALLY, Common_Movement_WalkInPlaceFasterLeft, MAP_PETALBURG_CITY
# 44 "data/maps/PetalburgCity/scripts.pory"
	waitmovement LOCALID_PETALBURG_WALLY, MAP_PETALBURG_CITY
# 45 "data/maps/PetalburgCity/scripts.pory"
	msgbox Route102_Text_LetsGoBack, MSGBOX_DEFAULT
# 46 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 47 "data/maps/PetalburgCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 48 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_PETALBURG_CITY_STATE, 3
# 49 "data/maps/PetalburgCity/scripts.pory"
	fadedefaultbgm
# 50 "data/maps/PetalburgCity/scripts.pory"
	clearflag FLAG_DONT_TRANSITION_MUSIC
# 51 "data/maps/PetalburgCity/scripts.pory"
	special LoadPlayerParty
# 52 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_PETALBURG_GYM_STATE, 1
# 53 "data/maps/PetalburgCity/scripts.pory"
	warp MAP_PETALBURG_CITY_GYM, 4, 108
# 54 "data/maps/PetalburgCity/scripts.pory"
	waitstate
# 55 "data/maps/PetalburgCity/scripts.pory"
	releaseall
# 56 "data/maps/PetalburgCity/scripts.pory"
	end
# 57 "data/maps/PetalburgCity/scripts.pory"

# 58 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_WalkToWallyHouse::
# 59 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 60 "data/maps/PetalburgCity/scripts.pory"
	setflag FLAG_HIDE_MAP_NAME_POPUP
# 61 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_WALLYS_DAD, PetalburgCity_Movement_WalkToWallyHouseWallysDad
# 62 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_WalkToWallyHousePlayer
# 63 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 64 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8004, 7
# 65 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8005, 5
# 66 "data/maps/PetalburgCity/scripts.pory"
	opendoor VAR_0x8004, VAR_0x8005
# 67 "data/maps/PetalburgCity/scripts.pory"
	waitdooranim
# 68 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_WALLYS_DAD, PetalburgCity_Movement_WalkInsideHouseWallysDad
# 69 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_WalkInsideHousePlayer
# 70 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 71 "data/maps/PetalburgCity/scripts.pory"
	setflag FLAG_HIDE_PETALBURG_CITY_WALLYS_DAD
# 72 "data/maps/PetalburgCity/scripts.pory"
	hideobjectat LOCALID_PLAYER, MAP_PETALBURG_CITY
# 73 "data/maps/PetalburgCity/scripts.pory"
	closedoor VAR_0x8004, VAR_0x8005
# 74 "data/maps/PetalburgCity/scripts.pory"
	waitdooranim
# 75 "data/maps/PetalburgCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 76 "data/maps/PetalburgCity/scripts.pory"
	fadedefaultbgm
# 77 "data/maps/PetalburgCity/scripts.pory"
	clearflag FLAG_DONT_TRANSITION_MUSIC
# 78 "data/maps/PetalburgCity/scripts.pory"
	warp MAP_PETALBURG_CITY_WALLYS_HOUSE, 2, 4
# 79 "data/maps/PetalburgCity/scripts.pory"
	waitstate
# 80 "data/maps/PetalburgCity/scripts.pory"
	releaseall
# 81 "data/maps/PetalburgCity/scripts.pory"
	end
# 82 "data/maps/PetalburgCity/scripts.pory"

# 83 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Boy::
# 84 "data/maps/PetalburgCity/scripts.pory"
	lock
# 85 "data/maps/PetalburgCity/scripts.pory"
	faceplayer
# 86 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_WaterReflection, MSGBOX_DEFAULT
# 87 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 88 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_BOY, Common_Movement_FaceOriginalDirection
# 89 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 90 "data/maps/PetalburgCity/scripts.pory"
	release
# 91 "data/maps/PetalburgCity/scripts.pory"
	end
# 92 "data/maps/PetalburgCity/scripts.pory"

# 93 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_WallysMom::
# 94 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_WhereIsWally, MSGBOX_NPC
# 95 "data/maps/PetalburgCity/scripts.pory"
	end
# 96 "data/maps/PetalburgCity/scripts.pory"

# 97 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_WalkToWallyHousePlayer:
# 98 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 99 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 100 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 101 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 102 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 103 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 104 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 105 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 106 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 107 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 108 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 109 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 110 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 111 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 112 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 113 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 114 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 115 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 116 "data/maps/PetalburgCity/scripts.pory"

# 117 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_WalkInsideHousePlayer:
# 118 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 119 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 120 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 121 "data/maps/PetalburgCity/scripts.pory"

# 122 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_WalkToWallyHouseWallysDad:
# 123 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 124 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 125 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 126 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 127 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 128 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 129 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 130 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 131 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 132 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 133 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 134 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 135 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 136 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 137 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 138 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 139 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 140 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 141 "data/maps/PetalburgCity/scripts.pory"

# 142 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_WalkInsideHouseWallysDad:
# 143 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 144 "data/maps/PetalburgCity/scripts.pory"
	set_invisible
# 145 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 146 "data/maps/PetalburgCity/scripts.pory"

# 147 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_WallyTutorialPlayer:
# 148 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 149 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 150 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 151 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 152 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 153 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 154 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 155 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 156 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 157 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 158 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 159 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 160 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 161 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 162 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 163 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 164 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 165 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 166 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 167 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 168 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 169 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 170 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 171 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 172 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 173 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 174 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 175 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 176 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 177 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 178 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 179 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_right
# 180 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 181 "data/maps/PetalburgCity/scripts.pory"

# 182 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_WallyTutorialWally:
# 183 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 184 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 185 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 186 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 187 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 188 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 189 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 190 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 191 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 192 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 193 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 194 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 195 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 196 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 197 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 198 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 199 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 200 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 201 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 202 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 203 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 204 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 205 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 206 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 207 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 208 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 209 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 210 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 211 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 212 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 213 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 214 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 215 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 216 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 217 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 218 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_right
# 219 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 220 "data/maps/PetalburgCity/scripts.pory"

# 221 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_GymSign::
# 222 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_GymSign, MSGBOX_SIGN
# 223 "data/maps/PetalburgCity/scripts.pory"
	end
# 224 "data/maps/PetalburgCity/scripts.pory"

# 225 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_CitySign::
# 226 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_CitySign, MSGBOX_SIGN
# 227 "data/maps/PetalburgCity/scripts.pory"
	end
# 228 "data/maps/PetalburgCity/scripts.pory"

# 229 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Gentleman::
# 230 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_FullPartyExplanation, MSGBOX_NPC
# 231 "data/maps/PetalburgCity/scripts.pory"
	end
# 232 "data/maps/PetalburgCity/scripts.pory"

# 233 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_WallyHouseSign::
# 234 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_WallyHouseSign, MSGBOX_SIGN
# 235 "data/maps/PetalburgCity/scripts.pory"
	end
# 236 "data/maps/PetalburgCity/scripts.pory"

# 237 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ShowGymToPlayer0::
# 238 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 239 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 0
# 240 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_ShowGymToPlayer
# 241 "data/maps/PetalburgCity/scripts.pory"
	end
# 242 "data/maps/PetalburgCity/scripts.pory"

# 243 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ShowGymToPlayer1::
# 244 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 245 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 1
# 246 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_ShowGymToPlayer
# 247 "data/maps/PetalburgCity/scripts.pory"
	end
# 248 "data/maps/PetalburgCity/scripts.pory"

# 249 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ShowGymToPlayer2::
# 250 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 251 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 2
# 252 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_ShowGymToPlayer
# 253 "data/maps/PetalburgCity/scripts.pory"
	end
# 254 "data/maps/PetalburgCity/scripts.pory"

# 255 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ShowGymToPlayer3::
# 256 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 257 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 3
# 258 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_ShowGymToPlayer
# 259 "data/maps/PetalburgCity/scripts.pory"
	end
# 260 "data/maps/PetalburgCity/scripts.pory"

# 261 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ShowGymToPlayer::
# 262 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, Common_Movement_FacePlayer
# 263 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 264 "data/maps/PetalburgCity/scripts.pory"
	playbgm MUS_FOLLOW_ME, FALSE
# 265 "data/maps/PetalburgCity/scripts.pory"
	playse SE_PIN
# 266 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, Common_Movement_ExclamationMark
# 267 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 268 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, Common_Movement_Delay48
# 269 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 270 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 0, PetalburgCity_EventScript_BoyApproachPlayer0
# 271 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 1, PetalburgCity_EventScript_BoyApproachPlayer1
# 272 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 2, PetalburgCity_EventScript_BoyApproachPlayer2
# 273 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 3, PetalburgCity_EventScript_BoyApproachPlayer3
# 274 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_AreYouRookieTrainer, MSGBOX_DEFAULT
# 275 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 276 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 0, PetalburgCity_EventScript_LeadPlayerToGym0
# 277 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 1, PetalburgCity_EventScript_LeadPlayerToGym1
# 278 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 2, PetalburgCity_EventScript_LeadPlayerToGym2
# 279 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 3, PetalburgCity_EventScript_LeadPlayerToGym3
# 280 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_ThisIsPetalburgGym, MSGBOX_DEFAULT
# 281 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, Common_Movement_WalkInPlaceFasterRight
# 282 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
# 283 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 284 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_ThisIsGymSign, MSGBOX_DEFAULT
# 285 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 286 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyWalkAway
# 287 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 288 "data/maps/PetalburgCity/scripts.pory"
	fadedefaultbgm
# 289 "data/maps/PetalburgCity/scripts.pory"
	releaseall
# 290 "data/maps/PetalburgCity/scripts.pory"
	end
# 291 "data/maps/PetalburgCity/scripts.pory"

# 292 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_BoyApproachPlayer0::
# 293 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyApproachPlayer0
# 294 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 295 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
# 296 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 297 "data/maps/PetalburgCity/scripts.pory"
	return
# 298 "data/maps/PetalburgCity/scripts.pory"

# 299 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_BoyApproachPlayer1::
# 300 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyApproachPlayer1
# 301 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 302 "data/maps/PetalburgCity/scripts.pory"
	return
# 303 "data/maps/PetalburgCity/scripts.pory"

# 304 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_BoyApproachPlayer2::
# 305 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyApproachPlayer2
# 306 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 307 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 308 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 309 "data/maps/PetalburgCity/scripts.pory"
	return
# 310 "data/maps/PetalburgCity/scripts.pory"

# 311 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_BoyApproachPlayer3::
# 312 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyApproachPlayer3
# 313 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 314 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
# 315 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 316 "data/maps/PetalburgCity/scripts.pory"
	return
# 317 "data/maps/PetalburgCity/scripts.pory"

# 318 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_LeadPlayerToGym0::
# 319 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyWalkToGym0
# 320 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWalkToGym0
# 321 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 322 "data/maps/PetalburgCity/scripts.pory"
	return
# 323 "data/maps/PetalburgCity/scripts.pory"

# 324 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_LeadPlayerToGym1::
# 325 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyWalkToGym1
# 326 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWalkToGym1
# 327 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 328 "data/maps/PetalburgCity/scripts.pory"
	return
# 329 "data/maps/PetalburgCity/scripts.pory"

# 330 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_LeadPlayerToGym2::
# 331 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyWalkToGym2
# 332 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWalkToGym2
# 333 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 334 "data/maps/PetalburgCity/scripts.pory"
	return
# 335 "data/maps/PetalburgCity/scripts.pory"

# 336 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_LeadPlayerToGym3::
# 337 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_GYM_BOY, PetalburgCity_Movement_BoyWalkToGym3
# 338 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWalkToGym3
# 339 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 340 "data/maps/PetalburgCity/scripts.pory"
	return
# 341 "data/maps/PetalburgCity/scripts.pory"

# 342 "data/maps/PetalburgCity/scripts.pory"
@ Unused
# 343 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_Delay48::
# 344 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 345 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 346 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 347 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 348 "data/maps/PetalburgCity/scripts.pory"

# 349 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyApproachPlayer0:
# 350 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 351 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 352 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 353 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 354 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 355 "data/maps/PetalburgCity/scripts.pory"

# 356 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyApproachPlayer1:
# 357 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 358 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 359 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 360 "data/maps/PetalburgCity/scripts.pory"

# 361 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyApproachPlayer2:
# 362 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 363 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 364 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 365 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_down
# 366 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 367 "data/maps/PetalburgCity/scripts.pory"

# 368 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyApproachPlayer3:
# 369 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 370 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 371 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 372 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 373 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_down
# 374 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 375 "data/maps/PetalburgCity/scripts.pory"

# 376 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyWalkToGym0:
# 377 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 378 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 379 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 380 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 381 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 382 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 383 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 384 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 385 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 386 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 387 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 388 "data/maps/PetalburgCity/scripts.pory"

# 389 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyWalkToGym1:
# 390 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 391 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 392 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 393 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 394 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 395 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 396 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 397 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 398 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 399 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 400 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 401 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 402 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 403 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 404 "data/maps/PetalburgCity/scripts.pory"

# 405 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyWalkToGym2:
# 406 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 407 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 408 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 409 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 410 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 411 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 412 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 413 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 414 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 415 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 416 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 417 "data/maps/PetalburgCity/scripts.pory"

# 418 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyWalkToGym3:
# 419 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 420 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 421 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 422 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 423 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 424 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 425 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 426 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 427 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 428 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 429 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 430 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 431 "data/maps/PetalburgCity/scripts.pory"

# 432 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_BoyWalkAway:
# 433 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 434 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 435 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 436 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 437 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 438 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 439 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 440 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 441 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 442 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 443 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 444 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 445 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 446 "data/maps/PetalburgCity/scripts.pory"

# 447 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWalkToGym0:
# 448 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 449 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 450 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 451 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 452 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 453 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 454 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 455 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 456 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 457 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 458 "data/maps/PetalburgCity/scripts.pory"

# 459 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWalkToGym1:
# 460 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 461 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 462 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 463 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 464 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 465 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 466 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 467 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 468 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 469 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 470 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 471 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 472 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 473 "data/maps/PetalburgCity/scripts.pory"

# 474 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWalkToGym2:
# 475 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 476 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 477 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 478 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 479 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 480 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 481 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 482 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 483 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 484 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 485 "data/maps/PetalburgCity/scripts.pory"

# 486 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWalkToGym3:
# 487 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 488 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 489 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 490 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 491 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 492 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 493 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 494 "data/maps/PetalburgCity/scripts.pory"
	walk_right
# 495 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 496 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 497 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 498 "data/maps/PetalburgCity/scripts.pory"

# 499 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Scott0::
# 500 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 501 "data/maps/PetalburgCity/scripts.pory"
	addobject LOCALID_PETALBURG_SCOTT
# 502 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 0
# 503 "data/maps/PetalburgCity/scripts.pory"
	setobjectxy LOCALID_PETALBURG_SCOTT, 13, 10
# 504 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_Scott
# 505 "data/maps/PetalburgCity/scripts.pory"
	end
# 506 "data/maps/PetalburgCity/scripts.pory"

# 507 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Scott1::
# 508 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 509 "data/maps/PetalburgCity/scripts.pory"
	addobject LOCALID_PETALBURG_SCOTT
# 510 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 1
# 511 "data/maps/PetalburgCity/scripts.pory"
	setobjectxy LOCALID_PETALBURG_SCOTT, 13, 11
# 512 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_Scott
# 513 "data/maps/PetalburgCity/scripts.pory"
	end
# 514 "data/maps/PetalburgCity/scripts.pory"

# 515 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Scott2::
# 516 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 517 "data/maps/PetalburgCity/scripts.pory"
	addobject LOCALID_PETALBURG_SCOTT
# 518 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 2
# 519 "data/maps/PetalburgCity/scripts.pory"
	setobjectxy LOCALID_PETALBURG_SCOTT, 13, 12
# 520 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_Scott
# 521 "data/maps/PetalburgCity/scripts.pory"
	end
# 522 "data/maps/PetalburgCity/scripts.pory"

# 523 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Scott3::
# 524 "data/maps/PetalburgCity/scripts.pory"
	lockall
# 525 "data/maps/PetalburgCity/scripts.pory"
	addobject LOCALID_PETALBURG_SCOTT
# 526 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_0x8008, 3
# 527 "data/maps/PetalburgCity/scripts.pory"
	setobjectxy LOCALID_PETALBURG_SCOTT, 13, 13
# 528 "data/maps/PetalburgCity/scripts.pory"
	goto PetalburgCity_EventScript_Scott
# 529 "data/maps/PetalburgCity/scripts.pory"
	end
# 530 "data/maps/PetalburgCity/scripts.pory"

# 531 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_Scott::
# 532 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, PetalburgCity_Movement_ScottStartWalkLeft
# 533 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 534 "data/maps/PetalburgCity/scripts.pory"
	playse SE_PIN
# 535 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, Common_Movement_ExclamationMark
# 536 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 537 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, Common_Movement_Delay48
# 538 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 539 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, PetalburgCity_Movement_ScottApproachPlayer
# 540 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 541 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
# 542 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 543 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_SCOTT_STATE, 1
# 544 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_AreYouATrainer, MSGBOX_DEFAULT
# 545 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 546 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, Common_Movement_WalkInPlaceFasterRight
# 547 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 548 "data/maps/PetalburgCity/scripts.pory"
	delay 30
# 549 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_WellMaybeNot, MSGBOX_DEFAULT
# 550 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 551 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, Common_Movement_WalkInPlaceFasterLeft
# 552 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 553 "data/maps/PetalburgCity/scripts.pory"
	delay 30
# 554 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_ImLookingForTalentedTrainers, MSGBOX_DEFAULT
# 555 "data/maps/PetalburgCity/scripts.pory"
	closemessage
# 556 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 0, PetalburgCity_EventScript_ScottExit0
# 557 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 1, PetalburgCity_EventScript_ScottExit1
# 558 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 2, PetalburgCity_EventScript_ScottExit2
# 559 "data/maps/PetalburgCity/scripts.pory"
	call_if_eq VAR_0x8008, 3, PetalburgCity_EventScript_ScottExit3
# 560 "data/maps/PetalburgCity/scripts.pory"
	setvar VAR_SCOTT_PETALBURG_ENCOUNTER, 1
# 561 "data/maps/PetalburgCity/scripts.pory"
	removeobject LOCALID_PETALBURG_SCOTT
# 562 "data/maps/PetalburgCity/scripts.pory"
	releaseall
# 563 "data/maps/PetalburgCity/scripts.pory"
	end
# 564 "data/maps/PetalburgCity/scripts.pory"

# 565 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ScottExit0::
# 566 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWatchScottExit0
# 567 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, PetalburgCity_Movement_ScottExit0
# 568 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 569 "data/maps/PetalburgCity/scripts.pory"
	return
# 570 "data/maps/PetalburgCity/scripts.pory"

# 571 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ScottExit1::
# 572 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWatchScottExit1
# 573 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, PetalburgCity_Movement_ScottExit1
# 574 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 575 "data/maps/PetalburgCity/scripts.pory"
	return
# 576 "data/maps/PetalburgCity/scripts.pory"

# 577 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ScottExit2::
# 578 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWatchScottExit2
# 579 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, PetalburgCity_Movement_ScottExit2
# 580 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 581 "data/maps/PetalburgCity/scripts.pory"
	return
# 582 "data/maps/PetalburgCity/scripts.pory"

# 583 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_ScottExit3::
# 584 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PLAYER, PetalburgCity_Movement_PlayerWatchScottExit3
# 585 "data/maps/PetalburgCity/scripts.pory"
	applymovement LOCALID_PETALBURG_SCOTT, PetalburgCity_Movement_ScottExit3
# 586 "data/maps/PetalburgCity/scripts.pory"
	waitmovement 0
# 587 "data/maps/PetalburgCity/scripts.pory"
	return
# 588 "data/maps/PetalburgCity/scripts.pory"

# 589 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_ScottStartWalkLeft:
# 590 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 591 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 592 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 593 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 594 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 595 "data/maps/PetalburgCity/scripts.pory"

# 596 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_ScottApproachPlayer:
# 597 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 598 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 599 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 600 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 601 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 602 "data/maps/PetalburgCity/scripts.pory"

# 603 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_ScottExit0:
# 604 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 605 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 606 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 607 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 608 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 609 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 610 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 611 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 612 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 613 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 614 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 615 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 616 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 617 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 618 "data/maps/PetalburgCity/scripts.pory"

# 619 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWatchScottExit0:
# 620 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 621 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_down
# 622 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 623 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 624 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 625 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_left
# 626 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 627 "data/maps/PetalburgCity/scripts.pory"

# 628 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_ScottExit1:
# 629 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 630 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 631 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 632 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 633 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 634 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 635 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 636 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 637 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 638 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 639 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 640 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 641 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 642 "data/maps/PetalburgCity/scripts.pory"

# 643 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWatchScottExit1:
# 644 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 645 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_down
# 646 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 647 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 648 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_left
# 649 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 650 "data/maps/PetalburgCity/scripts.pory"

# 651 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_ScottExit2:
# 652 "data/maps/PetalburgCity/scripts.pory"
	walk_down
# 653 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 654 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 655 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 656 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 657 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 658 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 659 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 660 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 661 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 662 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 663 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 664 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 665 "data/maps/PetalburgCity/scripts.pory"

# 666 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWatchScottExit2:
# 667 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 668 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_down
# 669 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 670 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 671 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_left
# 672 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 673 "data/maps/PetalburgCity/scripts.pory"

# 674 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_ScottExit3:
# 675 "data/maps/PetalburgCity/scripts.pory"
	walk_up
# 676 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 677 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 678 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 679 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 680 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 681 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 682 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 683 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 684 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 685 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 686 "data/maps/PetalburgCity/scripts.pory"
	walk_left
# 687 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 688 "data/maps/PetalburgCity/scripts.pory"

# 689 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Movement_PlayerWatchScottExit3:
# 690 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 691 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_up
# 692 "data/maps/PetalburgCity/scripts.pory"
	delay_16
# 693 "data/maps/PetalburgCity/scripts.pory"
	delay_8
# 694 "data/maps/PetalburgCity/scripts.pory"
	walk_in_place_faster_left
# 695 "data/maps/PetalburgCity/scripts.pory"
	step_end
# 696 "data/maps/PetalburgCity/scripts.pory"

# 697 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_EventScript_GymBoy::
# 698 "data/maps/PetalburgCity/scripts.pory"
	msgbox PetalburgCity_Text_AreYouRookieTrainer, MSGBOX_NPC
# 699 "data/maps/PetalburgCity/scripts.pory"
	end
# 700 "data/maps/PetalburgCity/scripts.pory"

# 701 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_WhereIsWally:
# 702 "data/maps/PetalburgCity/scripts.pory"
	.string "Where has our WALLY gone?\p"
# 703 "data/maps/PetalburgCity/scripts.pory"
	.string "We have to leave for VERDANTURF TOWN\n"
# 704 "data/maps/PetalburgCity/scripts.pory"
	.string "very soon…$"
# 705 "data/maps/PetalburgCity/scripts.pory"

# 706 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_AreYouRookieTrainer:
# 707 "data/maps/PetalburgCity/scripts.pory"
	.string "Hiya! Are you maybe…\n"
# 708 "data/maps/PetalburgCity/scripts.pory"
	.string "A rookie TRAINER?\p"
# 709 "data/maps/PetalburgCity/scripts.pory"
	.string "Do you know what POKéMON TRAINERS\n"
# 710 "data/maps/PetalburgCity/scripts.pory"
	.string "do when they reach a new town?\p"
# 711 "data/maps/PetalburgCity/scripts.pory"
	.string "They first check what kind of GYM\n"
# 712 "data/maps/PetalburgCity/scripts.pory"
	.string "is in the town.$"
# 713 "data/maps/PetalburgCity/scripts.pory"

# 714 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_ThisIsPetalburgGym:
# 715 "data/maps/PetalburgCity/scripts.pory"
	.string "See? This is PETALBURG CITY's GYM.$"
# 716 "data/maps/PetalburgCity/scripts.pory"

# 717 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_ThisIsGymSign:
# 718 "data/maps/PetalburgCity/scripts.pory"
	.string "This is the GYM's sign. Look for it\n"
# 719 "data/maps/PetalburgCity/scripts.pory"
	.string "whenever you're looking for a GYM.$"
# 720 "data/maps/PetalburgCity/scripts.pory"

# 721 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_WaterReflection:
# 722 "data/maps/PetalburgCity/scripts.pory"
	.string "My face is reflected in the water.\p"
# 723 "data/maps/PetalburgCity/scripts.pory"
	.string "It's a shining grin full of hope…\p"
# 724 "data/maps/PetalburgCity/scripts.pory"
	.string "Or it could be a look of somber silence\n"
# 725 "data/maps/PetalburgCity/scripts.pory"
	.string "struggling with fear…\p"
# 726 "data/maps/PetalburgCity/scripts.pory"
	.string "What do you see reflected in your face?$"
# 727 "data/maps/PetalburgCity/scripts.pory"

# 728 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_FullPartyExplanation:
# 729 "data/maps/PetalburgCity/scripts.pory"
	.string "Let's say you have six POKéMON.\n"
# 730 "data/maps/PetalburgCity/scripts.pory"
	.string "If you catch another one…\p"
# 731 "data/maps/PetalburgCity/scripts.pory"
	.string "It is automatically sent to a STORAGE\n"
# 732 "data/maps/PetalburgCity/scripts.pory"
	.string "BOX over a PC connection.$"
# 733 "data/maps/PetalburgCity/scripts.pory"

# 734 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_GymSign:
# 735 "data/maps/PetalburgCity/scripts.pory"
	.string "PETALBURG CITY POKéMON GYM\n"
# 736 "data/maps/PetalburgCity/scripts.pory"
	.string "LEADER: NORMAN\l"
# 737 "data/maps/PetalburgCity/scripts.pory"
	.string "“A man in pursuit of power!”$"
# 738 "data/maps/PetalburgCity/scripts.pory"

# 739 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_CitySign:
# 740 "data/maps/PetalburgCity/scripts.pory"
	.string "PETALBURG CITY\n"
# 741 "data/maps/PetalburgCity/scripts.pory"
	.string "“Where people mingle with nature.”$"
# 742 "data/maps/PetalburgCity/scripts.pory"

# 743 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_WallyHouseSign:
# 744 "data/maps/PetalburgCity/scripts.pory"
	.string "WALLY'S HOUSE$"
# 745 "data/maps/PetalburgCity/scripts.pory"

# 746 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_AreYouATrainer:
# 747 "data/maps/PetalburgCity/scripts.pory"
	.string "Excuse me!\p"
# 748 "data/maps/PetalburgCity/scripts.pory"
	.string "Let me guess, from the way you're\n"
# 749 "data/maps/PetalburgCity/scripts.pory"
	.string "dressed, are you a POKéMON TRAINER?$"
# 750 "data/maps/PetalburgCity/scripts.pory"

# 751 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_WellMaybeNot:
# 752 "data/maps/PetalburgCity/scripts.pory"
	.string "… … … … … …\p"
# 753 "data/maps/PetalburgCity/scripts.pory"
	.string "Well, maybe not.\n"
# 754 "data/maps/PetalburgCity/scripts.pory"
	.string "Your clothes aren't all that dirty.\p"
# 755 "data/maps/PetalburgCity/scripts.pory"
	.string "You're either a rookie TRAINER,\n"
# 756 "data/maps/PetalburgCity/scripts.pory"
	.string "or maybe you're just an ordinary kid.$"
# 757 "data/maps/PetalburgCity/scripts.pory"

# 758 "data/maps/PetalburgCity/scripts.pory"
PetalburgCity_Text_ImLookingForTalentedTrainers:
# 759 "data/maps/PetalburgCity/scripts.pory"
	.string "I'm roaming the land in search of\n"
# 760 "data/maps/PetalburgCity/scripts.pory"
	.string "talented TRAINERS.\p"
# 761 "data/maps/PetalburgCity/scripts.pory"
	.string "I'm sorry to have taken your time.$"
