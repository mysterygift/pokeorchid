# 1 "data/maps/TosaPort/scripts.pory"

# 2 "data/maps/TosaPort/scripts.pory"
TosaPort_MapScripts::
# 3 "data/maps/TosaPort/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TosaPort_OnTransition
# 4 "data/maps/TosaPort/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, TosaPort_OnWarp
# 5 "data/maps/TosaPort/scripts.pory"
	.byte 0
# 6 "data/maps/TosaPort/scripts.pory"

# 7 "data/maps/TosaPort/scripts.pory"
TosaPort_OnTransition:
# 8 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_VISITED_TOSA_PORT
# 9 "data/maps/TosaPort/scripts.pory"
	end
# 10 "data/maps/TosaPort/scripts.pory"

# 11 "data/maps/TosaPort/scripts.pory"
@ After object events exist; RunScriptImmediately — use only instant cmds (turnobject is OK).
# 12 "data/maps/TosaPort/scripts.pory"
TosaPort_OnWarp:
# 13 "data/maps/TosaPort/scripts.pory"
	map_script_2 VAR_TEMP_0, 0, TosaPort_EventScript_WarpFaceNorthIfNoMon
# 14 "data/maps/TosaPort/scripts.pory"
	.2byte 0
# 15 "data/maps/TosaPort/scripts.pory"

# 16 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_WarpFaceNorthIfNoMon::
# 17 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_SYS_POKEMON_GET, TosaPort_EventScript_WarpFaceNorthIfNoMon_End
# 18 "data/maps/TosaPort/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 19 "data/maps/TosaPort/scripts.pory"

# 20 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_WarpFaceNorthIfNoMon_End::
# 21 "data/maps/TosaPort/scripts.pory"
	end
# 22 "data/maps/TosaPort/scripts.pory"

# 23 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_TownSign::
# 24 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TownSign, MSGBOX_SIGN
# 25 "data/maps/TosaPort/scripts.pory"
	end
# 26 "data/maps/TosaPort/scripts.pory"

# 27 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_TruckSign::
# 28 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TruckSign, MSGBOX_SIGN
# 29 "data/maps/TosaPort/scripts.pory"
	end
# 30 "data/maps/TosaPort/scripts.pory"

# 31 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_ColdStorageSign::
# 32 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_ColdStorageSign, MSGBOX_SIGN
# 33 "data/maps/TosaPort/scripts.pory"
	end
# 34 "data/maps/TosaPort/scripts.pory"

# 35 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GatewaySign::
# 36 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GatewaySign, MSGBOX_SIGN
# 37 "data/maps/TosaPort/scripts.pory"
	end
# 38 "data/maps/TosaPort/scripts.pory"

# 39 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideTop::
# 40 "data/maps/TosaPort/scripts.pory"
	lockall
# 41 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 42 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_FacePlayer
# 43 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 44 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_QuestionMark
# 45 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 46 "data/maps/TosaPort/scripts.pory"
	playSE SE_M_METRONOME
# 47 "data/maps/TosaPort/scripts.pory"
	delay 24
# 48 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_YouMustBePlayer, MSGBOX_NPC
# 49 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkLeft
# 50 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 51 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_ExclamationMark
# 52 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 53 "data/maps/TosaPort/scripts.pory"
	playse SE_PIN
# 54 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GivePokemon, MSGBOX_NPC
# 55 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 56 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 57 "data/maps/TosaPort/scripts.pory"
	special ChooseStarterOverworld
# 58 "data/maps/TosaPort/scripts.pory"
	waitstate
# 59 "data/maps/TosaPort/scripts.pory"
	lockall
# 60 "data/maps/TosaPort/scripts.pory"
	bufferleadmonspeciesname STR_VAR_2
# 61 "data/maps/TosaPort/scripts.pory"
	playfanfare MUS_OBTAIN_TMHM
# 62 "data/maps/TosaPort/scripts.pory"
	message TosaPort_Text_ReceivedPokemon
# 63 "data/maps/TosaPort/scripts.pory"
	waitmessage
# 64 "data/maps/TosaPort/scripts.pory"
	waitfanfare
# 65 "data/maps/TosaPort/scripts.pory"
	closemessage
# 66 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_Nickname, MSGBOX_YESNO
# 67 "data/maps/TosaPort/scripts.pory"
	call_if_eq VAR_RESULT, 1, TosaPort_EventScript_GiveNickname
# 68 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
# 69 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint
# 70 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkRight
# 71 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 72 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE 1
# 73 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 74 "data/maps/TosaPort/scripts.pory"
	releaseall
# 75 "data/maps/TosaPort/scripts.pory"
	end
# 76 "data/maps/TosaPort/scripts.pory"

# 77 "data/maps/TosaPort/scripts.pory"
	TosaPort_EventScript_StarterGuideBottom::
# 78 "data/maps/TosaPort/scripts.pory"
	lockall
# 79 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 80 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_FacePlayer
# 81 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 82 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_QuestionMark
# 83 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 84 "data/maps/TosaPort/scripts.pory"
	playSE SE_M_METRONOME
# 85 "data/maps/TosaPort/scripts.pory"
	delay 24
# 86 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_YouMustBePlayer, MSGBOX_NPC
# 87 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkDown
# 88 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 89 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkLeft
# 90 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 91 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_ExclamationMark
# 92 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 93 "data/maps/TosaPort/scripts.pory"
	playse SE_PIN
# 94 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GivePokemon, MSGBOX_DEFAULT
# 95 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 96 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 97 "data/maps/TosaPort/scripts.pory"
	special ChooseStarterOverworld
# 98 "data/maps/TosaPort/scripts.pory"
	waitstate
# 99 "data/maps/TosaPort/scripts.pory"
	lockall
# 100 "data/maps/TosaPort/scripts.pory"
	bufferleadmonspeciesname STR_VAR_2
# 101 "data/maps/TosaPort/scripts.pory"
	playfanfare MUS_OBTAIN_TMHM
# 102 "data/maps/TosaPort/scripts.pory"
	message TosaPort_Text_ReceivedPokemon
# 103 "data/maps/TosaPort/scripts.pory"
	waitmessage
# 104 "data/maps/TosaPort/scripts.pory"
	waitfanfare
# 105 "data/maps/TosaPort/scripts.pory"
	closemessage
# 106 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_Nickname, MSGBOX_YESNO
# 107 "data/maps/TosaPort/scripts.pory"
	call_if_eq VAR_RESULT, 1, TosaPort_EventScript_GiveNickname
# 108 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
# 109 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_NPC
# 110 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkRight
# 111 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 112 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkUp
# 113 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 114 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE 1
# 115 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 116 "data/maps/TosaPort/scripts.pory"
	releaseall
# 117 "data/maps/TosaPort/scripts.pory"
	end
# 118 "data/maps/TosaPort/scripts.pory"

# 119 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GiveNickname::
# 120 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 121 "data/maps/TosaPort/scripts.pory"
	special ChangePokemonNickname
# 122 "data/maps/TosaPort/scripts.pory"
	waitstate
# 123 "data/maps/TosaPort/scripts.pory"
	return
# 124 "data/maps/TosaPort/scripts.pory"

# 125 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuide_AfterStarter::
# 126 "data/maps/TosaPort/scripts.pory"
	lock
# 127 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 128 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
# 129 "data/maps/TosaPort/scripts.pory"
	release
# 130 "data/maps/TosaPort/scripts.pory"
	end
# 131 "data/maps/TosaPort/scripts.pory"

# 132 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_YouMustBePlayer:
# 133 "data/maps/TosaPort/scripts.pory"
	.string "Ah! You must be {PLAYER}.\p"
# 134 "data/maps/TosaPort/scripts.pory"
	.string "Professor Palm sent me to meet you\n"
# 135 "data/maps/TosaPort/scripts.pory"
	.string "once the Seagallop-20 made port.$"
# 136 "data/maps/TosaPort/scripts.pory"

# 137 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GivePokemon:
# 138 "data/maps/TosaPort/scripts.pory"
	.string "I've brought you a little welcome\n"
# 139 "data/maps/TosaPort/scripts.pory"
	.string "present on behalf of the University.\p"
# 140 "data/maps/TosaPort/scripts.pory"
	.string "With the journey being so long from\n"
# 141 "data/maps/TosaPort/scripts.pory"
	.string "Galar, we figured you wouldn't bring\l"
# 142 "data/maps/TosaPort/scripts.pory"
	.string "your partners along.\p"
# 143 "data/maps/TosaPort/scripts.pory"
	.string "You peer inside the bag.$"
# 144 "data/maps/TosaPort/scripts.pory"

# 145 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ReceivedPokemon:
# 146 "data/maps/TosaPort/scripts.pory"
	.string "You received a {STR_VAR_2}!$"
# 147 "data/maps/TosaPort/scripts.pory"

# 148 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_Nickname:
# 149 "data/maps/TosaPort/scripts.pory"
	.string "Would you like to give {STR_VAR_2} a\n"
# 150 "data/maps/TosaPort/scripts.pory"
	.string "nickname?$"
# 151 "data/maps/TosaPort/scripts.pory"

# 152 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_StarterGuideTelokHint:
# 153 "data/maps/TosaPort/scripts.pory"
	.string "The road to TELOK TOWN runs through\n"
# 154 "data/maps/TosaPort/scripts.pory"
	.string "the Tosa nature reserve to the north.\p"
# 155 "data/maps/TosaPort/scripts.pory"
	.string "You'll find Palm Labs there.$"
# 156 "data/maps/TosaPort/scripts.pory"

# 157 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TownSign:
# 158 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Tosa!\n"
# 159 "data/maps/TosaPort/scripts.pory"
	.string "- The Tosa Tourism Board$"
# 160 "data/maps/TosaPort/scripts.pory"

# 161 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GatewaySign:
# 162 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Reserve Gateway\n"
# 163 "data/maps/TosaPort/scripts.pory"
	.string "Trainer passes strictly required$"
# 164 "data/maps/TosaPort/scripts.pory"

# 165 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TruckSign:
# 166 "data/maps/TosaPort/scripts.pory"
	.string "Machamp Moving Co.\n"
# 167 "data/maps/TosaPort/scripts.pory"
	.string "No Load too Lumbersome!$"
# 168 "data/maps/TosaPort/scripts.pory"

# 169 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ColdStorageSign:
# 170 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Port Cold Storage$"

TosaPort_PassAide::
# 175 "data/maps/TosaPort/scripts.pory"
	lockall
# 176 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_0, MSGBOX_AUTOCLOSE
# 177 "data/maps/TosaPort/scripts.pory"
	clearflag FLAG_HIDE_PASS_AIDE
# 178 "data/maps/TosaPort/scripts.pory"
	addobject LOCALID_PASS_AIDE
# 179 "data/maps/TosaPort/scripts.pory"
	showobjectat LOCALID_PASS_AIDE, MAP_TOSA_PORT
# 180 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PLAYER, TosaPort_PassAide_Movement_0
# 181 "data/maps/TosaPort/scripts.pory"
	playSE SE_M_METRONOME
# 182 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_1
# 185 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 186 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_1
# 187 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_TOSA_PASS
# 188 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_2
# 189 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_2
# 190 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 191 "data/maps/TosaPort/scripts.pory"
	delay 48
# 192 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_3
# 193 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 194 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_3
# 195 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_4, MSGBOX_NPC
# 196 "data/maps/TosaPort/scripts.pory"
	waitmessage
# 197 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_4
# 198 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 199 "data/maps/TosaPort/scripts.pory"
	hideobjectat LOCALID_PASS_AIDE, MAP_TOSA_PORT
# 200 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_RECEIVED_TOSA_PASS
# 201 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 202 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE, 2
# 203 "data/maps/TosaPort/scripts.pory"
	releaseall
	end


TosaPort_ScrubbingSailor::
# 208 "data/maps/TosaPort/scripts.pory"
	lock
# 209 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 210 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ScrubbingSailor_Text_0
# 212 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ShuntingSailor::
# 217 "data/maps/TosaPort/scripts.pory"
	lock
# 218 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 219 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ShuntingSailor_Text_0
# 221 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_VigorothCry::
# 226 "data/maps/TosaPort/scripts.pory"
	lock
# 227 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_VIGOROTH, CRY_MODE_NORMAL
# 228 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_VigorothCry_Text_0
# 229 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 230 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ChefStall::
# 235 "data/maps/TosaPort/scripts.pory"
	lock
# 236 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 237 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_CHEF_STALL_MET, TosaPort_ChefStall_2
# 253 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_2
# 255 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 256 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_3
# 257 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_ChefStall_2:
# 238 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_0
# 247 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_CHEF_STALL_MET
# 248 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 249 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_1
# 250 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 261 "data/maps/TosaPort/scripts.pory"
ChefStallGoods:
# 262 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_LAVA_COOKIE
# 263 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PEWTER_CRUNCHIES
# 264 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_OLD_GATEAU
# 265 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_BIG_MALASADA
# 266 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_SHALOUR_SABLE
	.2byte ITEM_NONE

TosaPort_PSPKid::
# 270 "data/maps/TosaPort/scripts.pory"
	lock
# 271 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 272 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_0
# 274 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_RepelGuy::
# 279 "data/maps/TosaPort/scripts.pory"
	lock
# 280 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 281 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_RepelGuy_Text_0
# 284 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_BreakTrucker::
# 289 "data/maps/TosaPort/scripts.pory"
	lock
# 290 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 291 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_BreakTrucker_Text_0
# 292 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_LoadingTrucker::
# 297 "data/maps/TosaPort/scripts.pory"
	lock
# 298 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 299 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_LoadingTrucker_Text_0
# 301 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldMan::
# 306 "data/maps/TosaPort/scripts.pory"
	lock
# 307 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_0
# 309 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldWoman::
# 314 "data/maps/TosaPort/scripts.pory"
	lock
# 315 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_0
# 317 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Skitty::
# 322 "data/maps/TosaPort/scripts.pory"
	lock
# 323 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 324 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
# 325 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Skitty_Text_0
# 326 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 327 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Fisherman::
# 332 "data/maps/TosaPort/scripts.pory"
	lock
# 333 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 334 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Fisherman_Text_0
# 336 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Tuber::
# 341 "data/maps/TosaPort/scripts.pory"
	lock
# 342 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 343 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Tuber_Text_0
# 347 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ColdStorageGuard::
# 352 "data/maps/TosaPort/scripts.pory"
	lock
# 353 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 354 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ColdStorageGuard_Text_0
# 356 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Martin::
# 361 "data/maps/TosaPort/scripts.pory"
	lock
# 362 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 363 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_0
# 365 "data/maps/TosaPort/scripts.pory"
	pokemart MartinsMartGoods
# 366 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_1
# 367 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 371 "data/maps/TosaPort/scripts.pory"
MartinsMartGoods:
# 372 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POTION
# 373 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POKE_BALL
# 374 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 375 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 376 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_REPEL
	.2byte ITEM_NONE

# 180 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_0:
# 180 "data/maps/TosaPort/scripts.pory"
	emote_question_mark
# 180 "data/maps/TosaPort/scripts.pory"
	face_down
	step_end

# 182 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_1:
# 183 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 183 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 183 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 183 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 183 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
	step_end

# 189 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_2:
# 189 "data/maps/TosaPort/scripts.pory"
	face_right
	step_end

# 192 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_3:
# 192 "data/maps/TosaPort/scripts.pory"
	face_player
	step_end

# 197 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_4:
# 197 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 197 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 197 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 197 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 197 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
	step_end

TosaPort_PassAide_Text_0:
# 176 "data/maps/TosaPort/scripts.pory"
	.string "WAIT! {PLAYER}!$"

TosaPort_PassAide_Text_1:
# 186 "data/maps/TosaPort/scripts.pory"
	.string "I...I need to give you this as well.$"

TosaPort_PassAide_Text_2:
# 188 "data/maps/TosaPort/scripts.pory"
	.string "Without a Tosa Pass, you won't be\n"
	.string "allowed onto the reserve. Normally you\l"
	.string "could take the underground...$"

TosaPort_PassAide_Text_3:
# 194 "data/maps/TosaPort/scripts.pory"
	.string "One more thing, if you haven't already I\n"
	.string "recommend you check out the markets\l"
	.string "here in the port. There's all sorts of\l"
	.string "supplies a trainer might need.$"

TosaPort_PassAide_Text_4:
# 195 "data/maps/TosaPort/scripts.pory"
	.string "Anyway, that's all from me. You better\n"
	.string "get going, I wouldn't want to keep the\l"
	.string "Professor waiting!$"

TosaPort_ScrubbingSailor_Text_0:
# 210 "data/maps/TosaPort/scripts.pory"
	.string "Gotta keep this jetty looking ship-\n"
	.string "shape!$"

TosaPort_ShuntingSailor_Text_0:
# 219 "data/maps/TosaPort/scripts.pory"
	.string "It's a good thing I have my Vigoroth\n"
	.string "with me!$"

TosaPort_VigorothCry_Text_0:
# 228 "data/maps/TosaPort/scripts.pory"
	.string "Vigoroth: Urraw!$"

TosaPort_ChefStall_Text_0:
# 238 "data/maps/TosaPort/scripts.pory"
	.string "Bonjour!\p"
	.string "I have travelled many miles from my\n"
	.string "home in Kalos...mais alors I have grown\l"
	.string "tired.\p"
	.string "I decided that it was time to share my\n"
	.string "love for la cuisine du monde avec the\l"
	.string "people!\p"
	.string "Have a look at my goods, see they are\n"
	.string "the most fresh, non?$"

TosaPort_ChefStall_Text_1:
# 249 "data/maps/TosaPort/scripts.pory"
	.string "See you again, mon ami!$"

TosaPort_ChefStall_Text_2:
# 253 "data/maps/TosaPort/scripts.pory"
	.string "Good to see you mon ami!\n"
	.string "What can I get for you?$"

TosaPort_ChefStall_Text_3:
# 256 "data/maps/TosaPort/scripts.pory"
	.string "Always a pleasure, mon ami!$"

TosaPort_PSPKid_Text_0:
# 272 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, Dad's making me watch his stall.\n"
	.string "At least he let me bring my PSP.$"

TosaPort_RepelGuy_Text_0:
# 281 "data/maps/TosaPort/scripts.pory"
	.string "I read in “Pokémon Garden” that\n"
	.string "spraying repel on your flowers can keep\l"
	.string "bug Pokémon at bay.$"

TosaPort_BreakTrucker_Text_0:
# 291 "data/maps/TosaPort/scripts.pory"
	.string "Buzz off, I'm on my break!$"

TosaPort_LoadingTrucker_Text_0:
# 299 "data/maps/TosaPort/scripts.pory"
	.string "I wish my Pokémon was strong enough to\n"
	.string "load this truck...$"

TosaPort_OldMan_Text_0:
# 307 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu...I met my wife at this very\n"
	.string "spot 10 years ago.$"

TosaPort_OldWoman_Text_0:
# 315 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha...we were so reckless back\n"
	.string "then...life is too short...$"

TosaPort_Skitty_Text_0:
# 325 "data/maps/TosaPort/scripts.pory"
	.string "Skitty: Meooow!$"

TosaPort_Fisherman_Text_0:
# 334 "data/maps/TosaPort/scripts.pory"
	.string "I came all this way from Pasira City to\n"
	.string "fish in the reserve.$"

TosaPort_Tuber_Text_0:
# 343 "data/maps/TosaPort/scripts.pory"
	.string "Awww...\n"
	.string "I was hoping to swim while visiting\l"
	.string "Daddy, but the current here is too\l"
	.string "strong!$"

TosaPort_ColdStorageGuard_Text_0:
# 354 "data/maps/TosaPort/scripts.pory"
	.string "Sorry pal, but the site's currently\n"
	.string "closed.$"

TosaPort_Martin_Text_0:
# 363 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Martin's Mart!\n"
	.string "Trainer Supplies and Sundries.$"

TosaPort_Martin_Text_1:
# 366 "data/maps/TosaPort/scripts.pory"
	.string "Come back soon!$"
