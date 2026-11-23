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
	goto_if_set FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 42 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideNoticePlayer
# 43 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkLeft
# 44 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 45 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideGiveStarter
# 46 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkRight
# 47 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 48 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_EventScript_StarterGuideFinish
# 49 "data/maps/TosaPort/scripts.pory"

# 50 "data/maps/TosaPort/scripts.pory"
@ The tile below the aide (24,36) is off the jetty, so come round via (23,35).
# 51 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideBottom::
# 52 "data/maps/TosaPort/scripts.pory"
	lockall
# 53 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 54 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideNoticePlayer
# 55 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, TosaPort_Movement_AideToBottomRow
# 56 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 57 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideGiveStarter
# 58 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, TosaPort_Movement_AideFromBottomRow
# 59 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 60 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_EventScript_StarterGuideFinish
# 61 "data/maps/TosaPort/scripts.pory"

# 62 "data/maps/TosaPort/scripts.pory"
@ Coord-triggered cutscene: use MSGBOX_DEFAULT + closemessage, never MSGBOX_NPC
# 63 "data/maps/TosaPort/scripts.pory"
@ (its faceplayer/release would turn a stale object and unfreeze every NPC mid-scene).
# 64 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideNoticePlayer::
# 65 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_FacePlayer
# 66 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 67 "data/maps/TosaPort/scripts.pory"
	playse SE_M_METRONOME
# 68 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_QuestionMark
# 69 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 70 "data/maps/TosaPort/scripts.pory"
	delay 16
# 71 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_YouMustBePlayer, MSGBOX_DEFAULT
# 72 "data/maps/TosaPort/scripts.pory"
	closemessage
# 73 "data/maps/TosaPort/scripts.pory"
	return
# 74 "data/maps/TosaPort/scripts.pory"

# 75 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideGiveStarter::
# 76 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_FaceRight
# 77 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 78 "data/maps/TosaPort/scripts.pory"
	playse SE_PIN
# 79 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_ExclamationMark
# 80 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 81 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GivePokemon, MSGBOX_DEFAULT
# 82 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_PeerInsideBag, MSGBOX_DEFAULT
# 83 "data/maps/TosaPort/scripts.pory"
	closemessage
# 84 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 85 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 86 "data/maps/TosaPort/scripts.pory"
	special ChooseStarterOverworld
# 87 "data/maps/TosaPort/scripts.pory"
	waitstate
# 88 "data/maps/TosaPort/scripts.pory"
	lockall
# 89 "data/maps/TosaPort/scripts.pory"
	bufferleadmonspeciesname STR_VAR_2
# 90 "data/maps/TosaPort/scripts.pory"
	playfanfare MUS_OBTAIN_TMHM
# 91 "data/maps/TosaPort/scripts.pory"
	message TosaPort_Text_ReceivedPokemon
# 92 "data/maps/TosaPort/scripts.pory"
	waitmessage
# 93 "data/maps/TosaPort/scripts.pory"
	waitfanfare
# 94 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_Nickname, MSGBOX_YESNO
# 95 "data/maps/TosaPort/scripts.pory"
	call_if_eq VAR_RESULT, 1, TosaPort_EventScript_GiveNickname
# 96 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG
# 97 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
# 98 "data/maps/TosaPort/scripts.pory"
	closemessage
# 99 "data/maps/TosaPort/scripts.pory"
	return
# 100 "data/maps/TosaPort/scripts.pory"

# 101 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideFinish::
# 102 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE, 1
# 103 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 104 "data/maps/TosaPort/scripts.pory"
	releaseall
# 105 "data/maps/TosaPort/scripts.pory"
	end
# 106 "data/maps/TosaPort/scripts.pory"

# 107 "data/maps/TosaPort/scripts.pory"
@ ChangePokemonNickname reads the party slot from VAR_0x8004. The naming screen
# 108 "data/maps/TosaPort/scripts.pory"
@ pauses the script itself, so no waitstate (one here would hang forever).
# 109 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GiveNickname::
# 110 "data/maps/TosaPort/scripts.pory"
	call Common_EventScript_GetGiftMonPartySlot
# 111 "data/maps/TosaPort/scripts.pory"
	call Common_EventScript_NameReceivedPartyMon
# 112 "data/maps/TosaPort/scripts.pory"
	lockall
# 113 "data/maps/TosaPort/scripts.pory"
	return
# 114 "data/maps/TosaPort/scripts.pory"

# 115 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuide_AfterStarter::
# 116 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 117 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
# 118 "data/maps/TosaPort/scripts.pory"
	releaseall
# 119 "data/maps/TosaPort/scripts.pory"
	end
# 120 "data/maps/TosaPort/scripts.pory"

# 121 "data/maps/TosaPort/scripts.pory"
TosaPort_Movement_AideToBottomRow:
# 122 "data/maps/TosaPort/scripts.pory"
	walk_left
# 123 "data/maps/TosaPort/scripts.pory"
	walk_down
# 124 "data/maps/TosaPort/scripts.pory"
	face_left
# 125 "data/maps/TosaPort/scripts.pory"
	step_end
# 126 "data/maps/TosaPort/scripts.pory"

# 127 "data/maps/TosaPort/scripts.pory"
TosaPort_Movement_AideFromBottomRow:
# 128 "data/maps/TosaPort/scripts.pory"
	walk_up
# 129 "data/maps/TosaPort/scripts.pory"
	walk_right
# 130 "data/maps/TosaPort/scripts.pory"
	step_end
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
	.string "your partners along.$"
# 143 "data/maps/TosaPort/scripts.pory"

# 144 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_PeerInsideBag:
# 145 "data/maps/TosaPort/scripts.pory"
	.string "You peer inside the bag.$"
# 146 "data/maps/TosaPort/scripts.pory"

# 147 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ReceivedPokemon:
# 148 "data/maps/TosaPort/scripts.pory"
	.string "You received a {STR_VAR_2}!$"
# 149 "data/maps/TosaPort/scripts.pory"

# 150 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_Nickname:
# 151 "data/maps/TosaPort/scripts.pory"
	.string "Would you like to give {STR_VAR_2} a\n"
# 152 "data/maps/TosaPort/scripts.pory"
	.string "nickname?$"
# 153 "data/maps/TosaPort/scripts.pory"

# 154 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_StarterGuideTelokHint:
# 155 "data/maps/TosaPort/scripts.pory"
	.string "The road to TELOK TOWN runs through\n"
# 156 "data/maps/TosaPort/scripts.pory"
	.string "the Tosa nature reserve to the north.\p"
# 157 "data/maps/TosaPort/scripts.pory"
	.string "You'll find Palm Labs there.$"
# 158 "data/maps/TosaPort/scripts.pory"

# 159 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TownSign:
# 160 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Tosa!\n"
# 161 "data/maps/TosaPort/scripts.pory"
	.string "- The Tosa Tourism Board$"
# 162 "data/maps/TosaPort/scripts.pory"

# 163 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GatewaySign:
# 164 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Reserve Gateway\n"
# 165 "data/maps/TosaPort/scripts.pory"
	.string "Trainer passes strictly required$"
# 166 "data/maps/TosaPort/scripts.pory"

# 167 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TruckSign:
# 168 "data/maps/TosaPort/scripts.pory"
	.string "Machamp Moving Co.\n"
# 169 "data/maps/TosaPort/scripts.pory"
	.string "No Load too Lumbersome!$"
# 170 "data/maps/TosaPort/scripts.pory"

# 171 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ColdStorageSign:
# 172 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Port Cold Storage$"

TosaPort_PassAide::
# 177 "data/maps/TosaPort/scripts.pory"
	lockall
# 178 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_0, MSGBOX_AUTOCLOSE
# 179 "data/maps/TosaPort/scripts.pory"
	clearflag FLAG_HIDE_PASS_AIDE
# 180 "data/maps/TosaPort/scripts.pory"
	addobject LOCALID_PASS_AIDE
# 181 "data/maps/TosaPort/scripts.pory"
	showobjectat LOCALID_PASS_AIDE, MAP_TOSA_PORT
# 182 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PLAYER, TosaPort_PassAide_Movement_0
# 183 "data/maps/TosaPort/scripts.pory"
	playSE SE_M_METRONOME
# 184 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_1
# 187 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 188 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_1
# 189 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_TOSA_PASS
# 190 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_2
# 191 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_2
# 192 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 193 "data/maps/TosaPort/scripts.pory"
	delay 48
# 194 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_3
# 195 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 196 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_3
# 197 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_4
# 198 "data/maps/TosaPort/scripts.pory"
	closemessage
# 199 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_4
# 200 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 201 "data/maps/TosaPort/scripts.pory"
	hideobjectat LOCALID_PASS_AIDE, MAP_TOSA_PORT
# 202 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_RECEIVED_TOSA_PASS
# 203 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 204 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE, 2
# 205 "data/maps/TosaPort/scripts.pory"
	releaseall
	end


TosaPort_ScrubbingSailor::
# 210 "data/maps/TosaPort/scripts.pory"
	lock
# 211 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 212 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ScrubbingSailor_Text_0
# 214 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ShuntingSailor::
# 219 "data/maps/TosaPort/scripts.pory"
	lock
# 220 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 221 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ShuntingSailor_Text_0
# 223 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_VigorothCry::
# 228 "data/maps/TosaPort/scripts.pory"
	lock
# 229 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_VIGOROTH, CRY_MODE_NORMAL
# 230 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_VigorothCry_Text_0
# 231 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 232 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ChefStall::
# 237 "data/maps/TosaPort/scripts.pory"
	lock
# 238 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 239 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_CHEF_STALL_MET, TosaPort_ChefStall_2
# 255 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_2
# 257 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 258 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_3
# 259 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_ChefStall_2:
# 240 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_0
# 249 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_CHEF_STALL_MET
# 250 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 251 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_1
# 252 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 263 "data/maps/TosaPort/scripts.pory"
ChefStallGoods:
# 264 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_LAVA_COOKIE
# 265 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PEWTER_CRUNCHIES
# 266 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_OLD_GATEAU
# 267 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_BIG_MALASADA
# 268 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_SHALOUR_SABLE
	.2byte ITEM_NONE

TosaPort_PSPKid::
# 272 "data/maps/TosaPort/scripts.pory"
	lock
# 273 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 274 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_0
# 276 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_RepelGuy::
# 281 "data/maps/TosaPort/scripts.pory"
	lock
# 282 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 283 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_RepelGuy_Text_0
# 286 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_BreakTrucker::
# 291 "data/maps/TosaPort/scripts.pory"
	lock
# 292 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 293 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_BreakTrucker_Text_0
# 294 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_LoadingTrucker::
# 299 "data/maps/TosaPort/scripts.pory"
	lock
# 300 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 301 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_LoadingTrucker_Text_0
# 303 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldMan::
# 308 "data/maps/TosaPort/scripts.pory"
	lock
# 309 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_0
# 311 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldWoman::
# 316 "data/maps/TosaPort/scripts.pory"
	lock
# 317 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_0
# 319 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Skitty::
# 324 "data/maps/TosaPort/scripts.pory"
	lock
# 325 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 326 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
# 327 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Skitty_Text_0
# 328 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 329 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Fisherman::
# 334 "data/maps/TosaPort/scripts.pory"
	lock
# 335 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 336 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Fisherman_Text_0
# 338 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Tuber::
# 343 "data/maps/TosaPort/scripts.pory"
	lock
# 344 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 345 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Tuber_Text_0
# 349 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ColdStorageGuard::
# 354 "data/maps/TosaPort/scripts.pory"
	lock
# 355 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 356 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ColdStorageGuard_Text_0
# 358 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Martin::
# 363 "data/maps/TosaPort/scripts.pory"
	lock
# 364 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 365 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_0
# 367 "data/maps/TosaPort/scripts.pory"
	pokemart MartinsMartGoods
# 368 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_1
# 369 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 373 "data/maps/TosaPort/scripts.pory"
MartinsMartGoods:
# 374 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POTION
# 375 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POKE_BALL
# 376 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 377 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 378 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_REPEL
	.2byte ITEM_NONE

# 182 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_0:
# 182 "data/maps/TosaPort/scripts.pory"
	emote_question_mark
# 182 "data/maps/TosaPort/scripts.pory"
	face_down
	step_end

# 184 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_1:
# 185 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 185 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 185 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 185 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 185 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
	step_end

# 191 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_2:
# 191 "data/maps/TosaPort/scripts.pory"
	face_right
	step_end

# 194 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_3:
# 194 "data/maps/TosaPort/scripts.pory"
	face_player
	step_end

# 199 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_4:
# 199 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 199 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 199 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 199 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 199 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
	step_end

TosaPort_PassAide_Text_0:
# 178 "data/maps/TosaPort/scripts.pory"
	.string "WAIT! {PLAYER}!$"

TosaPort_PassAide_Text_1:
# 188 "data/maps/TosaPort/scripts.pory"
	.string "I...I need to give you this as well.$"

TosaPort_PassAide_Text_2:
# 190 "data/maps/TosaPort/scripts.pory"
	.string "Without a Tosa Pass, you won't be\n"
	.string "allowed onto the reserve. Normally you\l"
	.string "could take the underground...$"

TosaPort_PassAide_Text_3:
# 196 "data/maps/TosaPort/scripts.pory"
	.string "One more thing, if you haven't already I\n"
	.string "recommend you check out the markets\l"
	.string "here in the port. There's all sorts of\l"
	.string "supplies a trainer might need.$"

TosaPort_PassAide_Text_4:
# 197 "data/maps/TosaPort/scripts.pory"
	.string "Anyway, that's all from me. You better\n"
	.string "get going, I wouldn't want to keep the\l"
	.string "Professor waiting!$"

TosaPort_ScrubbingSailor_Text_0:
# 212 "data/maps/TosaPort/scripts.pory"
	.string "Gotta keep this jetty looking ship-\n"
	.string "shape!$"

TosaPort_ShuntingSailor_Text_0:
# 221 "data/maps/TosaPort/scripts.pory"
	.string "It's a good thing I have my Vigoroth\n"
	.string "with me!$"

TosaPort_VigorothCry_Text_0:
# 230 "data/maps/TosaPort/scripts.pory"
	.string "Vigoroth: Urraw!$"

TosaPort_ChefStall_Text_0:
# 240 "data/maps/TosaPort/scripts.pory"
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
# 251 "data/maps/TosaPort/scripts.pory"
	.string "See you again, mon ami!$"

TosaPort_ChefStall_Text_2:
# 255 "data/maps/TosaPort/scripts.pory"
	.string "Good to see you mon ami!\n"
	.string "What can I get for you?$"

TosaPort_ChefStall_Text_3:
# 258 "data/maps/TosaPort/scripts.pory"
	.string "Always a pleasure, mon ami!$"

TosaPort_PSPKid_Text_0:
# 274 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, Dad's making me watch his stall.\n"
	.string "At least he let me bring my PSP.$"

TosaPort_RepelGuy_Text_0:
# 283 "data/maps/TosaPort/scripts.pory"
	.string "I read in “Pokémon Garden” that\n"
	.string "spraying repel on your flowers can keep\l"
	.string "bug Pokémon at bay.$"

TosaPort_BreakTrucker_Text_0:
# 293 "data/maps/TosaPort/scripts.pory"
	.string "Buzz off, I'm on my break!$"

TosaPort_LoadingTrucker_Text_0:
# 301 "data/maps/TosaPort/scripts.pory"
	.string "I wish my Pokémon was strong enough to\n"
	.string "load this truck...$"

TosaPort_OldMan_Text_0:
# 309 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu...I met my wife at this very\n"
	.string "spot 10 years ago.$"

TosaPort_OldWoman_Text_0:
# 317 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha...we were so reckless back\n"
	.string "then...life is too short...$"

TosaPort_Skitty_Text_0:
# 327 "data/maps/TosaPort/scripts.pory"
	.string "Skitty: Meooow!$"

TosaPort_Fisherman_Text_0:
# 336 "data/maps/TosaPort/scripts.pory"
	.string "I came all this way from Pasira City to\n"
	.string "fish in the reserve.$"

TosaPort_Tuber_Text_0:
# 345 "data/maps/TosaPort/scripts.pory"
	.string "Awww...\n"
	.string "I was hoping to swim while visiting\l"
	.string "Daddy, but the current here is too\l"
	.string "strong!$"

TosaPort_ColdStorageGuard_Text_0:
# 356 "data/maps/TosaPort/scripts.pory"
	.string "The site's open, pal, but mind your\n"
	.string "step. The floor in there is solid ice.$"

TosaPort_Martin_Text_0:
# 365 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Martin's Mart!\n"
	.string "Trainer Supplies and Sundries.$"

TosaPort_Martin_Text_1:
# 368 "data/maps/TosaPort/scripts.pory"
	.string "Come back soon!$"
