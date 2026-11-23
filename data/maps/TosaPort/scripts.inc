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
# 256 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_2
# 258 "data/maps/TosaPort/scripts.pory"
	call TosaPort_ChefStall_GateauHint
# 259 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 260 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_3
# 261 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_ChefStall_2:
# 240 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_0
# 249 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_CHEF_STALL_MET
# 250 "data/maps/TosaPort/scripts.pory"
	call TosaPort_ChefStall_GateauHint
# 251 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 252 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_1
# 253 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ChefStall_GateauHint::
# 268 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_TASTE_OF_HOME
# 269 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_ChefStall_GateauHint_3
TosaPort_ChefStall_GateauHint_1:
	return

TosaPort_ChefStall_GateauHint_2:
# 270 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_GateauHint_Text_0
# 271 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_OLD_GATEAU
# 272 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_ChefStall_GateauHint_6
	goto TosaPort_ChefStall_GateauHint_1

TosaPort_ChefStall_GateauHint_3:
# 269 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_RECEIVED_CHEF_OLD_GATEAU, TosaPort_ChefStall_GateauHint_2
	goto TosaPort_ChefStall_GateauHint_1

TosaPort_ChefStall_GateauHint_6:
# 273 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_RECEIVED_CHEF_OLD_GATEAU
	goto TosaPort_ChefStall_GateauHint_1


	.align 2
# 279 "data/maps/TosaPort/scripts.pory"
ChefStallGoods:
# 280 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_LAVA_COOKIE
# 281 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PEWTER_CRUNCHIES
# 282 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_OLD_GATEAU
# 283 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_BIG_MALASADA
# 284 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_SHALOUR_SABLE
	.2byte ITEM_NONE

TosaPort_PSPKid::
# 290 "data/maps/TosaPort/scripts.pory"
	lock
# 291 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 292 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_PSP_BATTERIES
# 293 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_PSPKid_2
# 298 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_PSP_BATTERIES
# 299 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_PSPKid_5
# 327 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_8
# 329 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_9
# 330 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_10, MSGBOX_YESNO
# 331 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, NO
	goto_if_eq TosaPort_PSPKid_8
# 336 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_12
# 337 "data/maps/TosaPort/scripts.pory"
	startquest QUEST_PSP_BATTERIES
# 338 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_PSPKid_2:
# 294 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_0
# 295 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_PSPKid_5:
# 300 "data/maps/TosaPort/scripts.pory"
	subquestmenu QUEST_MENU_CHECK_COMPLETE, QUEST_PSP_BATTERIES, SUB_QUEST_1
# 301 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_PSPKid_11
# 323 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_7
# 324 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_PSPKid_8:
# 332 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_11
# 333 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_PSPKid_11:
# 302 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_1
# 303 "data/maps/TosaPort/scripts.pory"
	checkitem ITEM_CELL_BATTERY
# 304 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq TosaPort_PSPKid_14
# 309 "data/maps/TosaPort/scripts.pory"
	removeitem ITEM_CELL_BATTERY
# 310 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_3
# 311 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_4
# 312 "data/maps/TosaPort/scripts.pory"
	checkplayergender
# 313 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, MALE
	goto_if_eq TosaPort_PSPKid_17
# 316 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_6
TosaPort_PSPKid_16:
# 318 "data/maps/TosaPort/scripts.pory"
	subquestmenu QUEST_MENU_COMPLETE_QUEST, QUEST_PSP_BATTERIES, SUB_QUEST_2
# 319 "data/maps/TosaPort/scripts.pory"
	completequest QUEST_PSP_BATTERIES
# 320 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_PSPKid_14:
# 305 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_2
# 306 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_PSPKid_17:
# 314 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PSPKid_Text_5
	goto TosaPort_PSPKid_16


TosaPort_StallDad::
# 343 "data/maps/TosaPort/scripts.pory"
	lock
# 344 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 345 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_PSP_BATTERIES
# 346 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_StallDad_2
# 365 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_PSP_BATTERIES
# 366 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_StallDad_5
# 371 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_5
# 372 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_2:
# 347 "data/maps/TosaPort/scripts.pory"
	subquestmenu QUEST_MENU_CHECK_COMPLETE, QUEST_PSP_BATTERIES, SUB_QUEST_1
# 348 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_StallDad_8
# 353 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_1
# 354 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_2
# 355 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_CELL_BATTERY
# 356 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq TosaPort_StallDad_11
# 360 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_3
# 361 "data/maps/TosaPort/scripts.pory"
	completesubquest QUEST_PSP_BATTERIES, SUB_QUEST_1
# 362 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_5:
# 367 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_4
# 368 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_8:
# 349 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_0
# 350 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_11:
# 357 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_RepelGuy::
# 377 "data/maps/TosaPort/scripts.pory"
	lock
# 378 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 379 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_RepelGuy_Text_0
# 382 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_BreakTrucker::
# 387 "data/maps/TosaPort/scripts.pory"
	lock
# 388 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 389 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_BreakTrucker_Text_0
# 390 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_LoadingTrucker::
# 395 "data/maps/TosaPort/scripts.pory"
	lock
# 396 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 397 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_LoadingTrucker_Text_0
# 399 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldMan::
# 406 "data/maps/TosaPort/scripts.pory"
	lock
# 407 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_HEART_SCALE
# 408 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_2
# 413 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_HEART_SCALE
# 414 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_5
# 424 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_2
# 426 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 427 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_3
# 428 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_4
# 429 "data/maps/TosaPort/scripts.pory"
	startquest QUEST_HEART_SCALE
# 430 "data/maps/TosaPort/scripts.pory"
	checkitem ITEM_HEART_SCALE
# 431 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_8
TosaPort_OldMan_7:
# 434 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_2:
# 409 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_0
# 410 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_5:
# 415 "data/maps/TosaPort/scripts.pory"
	checkitem ITEM_HEART_SCALE
# 416 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_11
TosaPort_OldMan_10:
# 419 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 420 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_1
# 421 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_8:
# 432 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_OldMan_ShowHeartScale
	goto TosaPort_OldMan_7

TosaPort_OldMan_11:
# 417 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_OldMan_ShowHeartScale
	goto TosaPort_OldMan_10


TosaPort_OldMan_ShowHeartScale::
# 439 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 440 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_0, MSGBOX_YESNO
# 441 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, NO
	goto_if_eq TosaPort_OldMan_ShowHeartScale_2
# 446 "data/maps/TosaPort/scripts.pory"
	checkitemspace ITEM_SOOTHE_BELL
# 447 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq TosaPort_OldMan_ShowHeartScale_5
# 452 "data/maps/TosaPort/scripts.pory"
	removeitem ITEM_HEART_SCALE
# 453 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_3
# 454 "data/maps/TosaPort/scripts.pory"
	closemessage
# 455 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_MAN, TosaPort_PassAide_Movement_2
# 456 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_OldMan_ShowHeartScale_Movement_0
# 457 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 458 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_4
# 459 "data/maps/TosaPort/scripts.pory"
	closemessage
# 460 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_OldMan_ShowHeartScale_Movement_1
# 461 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 462 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_5
# 463 "data/maps/TosaPort/scripts.pory"
	closemessage
# 464 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_PassAide_Movement_3
# 465 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 466 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_6
# 467 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_SOOTHE_BELL
# 468 "data/maps/TosaPort/scripts.pory"
	completequest QUEST_HEART_SCALE
# 469 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_MAN, TosaPort_OldMan_ShowHeartScale_Movement_2
# 470 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_OldMan_ShowHeartScale_Movement_2
# 471 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 472 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_ShowHeartScale_2:
# 442 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_1
# 443 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_ShowHeartScale_5:
# 448 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_2
# 449 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldWoman::
# 477 "data/maps/TosaPort/scripts.pory"
	lock
# 478 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_HEART_SCALE
# 479 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldWoman_2
# 484 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_1
# 486 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldWoman_2:
# 480 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_0
# 481 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Skitty::
# 491 "data/maps/TosaPort/scripts.pory"
	lock
# 492 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 493 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
# 494 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Skitty_Text_0
# 495 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 496 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Fisherman::
# 501 "data/maps/TosaPort/scripts.pory"
	lock
# 502 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 503 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Fisherman_Text_0
# 505 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Tuber::
# 510 "data/maps/TosaPort/scripts.pory"
	lock
# 511 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 512 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Tuber_Text_0
# 516 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ColdStorageGuard::
# 521 "data/maps/TosaPort/scripts.pory"
	lock
# 522 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 523 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ColdStorageGuard_Text_0
# 525 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Martin::
# 530 "data/maps/TosaPort/scripts.pory"
	lock
# 531 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 532 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_0
# 534 "data/maps/TosaPort/scripts.pory"
	pokemart MartinsMartGoods
# 535 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_1
# 536 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 540 "data/maps/TosaPort/scripts.pory"
MartinsMartGoods:
# 541 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POTION
# 542 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POKE_BALL
# 543 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 544 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 545 "data/maps/TosaPort/scripts.pory"
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

# 456 "data/maps/TosaPort/scripts.pory"
TosaPort_OldMan_ShowHeartScale_Movement_0:
# 456 "data/maps/TosaPort/scripts.pory"
	face_left
	step_end

# 460 "data/maps/TosaPort/scripts.pory"
TosaPort_OldMan_ShowHeartScale_Movement_1:
# 460 "data/maps/TosaPort/scripts.pory"
	emote_heart
	step_end

# 469 "data/maps/TosaPort/scripts.pory"
TosaPort_OldMan_ShowHeartScale_Movement_2:
# 469 "data/maps/TosaPort/scripts.pory"
	face_down
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
# 252 "data/maps/TosaPort/scripts.pory"
	.string "See you again, mon ami!$"

TosaPort_ChefStall_Text_2:
# 256 "data/maps/TosaPort/scripts.pory"
	.string "Good to see you mon ami!\n"
	.string "What can I get for you?$"

TosaPort_ChefStall_Text_3:
# 260 "data/maps/TosaPort/scripts.pory"
	.string "Always a pleasure, mon ami!$"

TosaPort_ChefStall_GateauHint_Text_0:
# 270 "data/maps/TosaPort/scripts.pory"
	.string "Quoi? Someone from Kalos is missing\n"
	.string "home? Bien sûr, they only need a taste\l"
	.string "of my delicious gateau! Bring this to\l"
	.string "ton ami, mon ami.$"

TosaPort_PSPKid_Text_0:
# 294 "data/maps/TosaPort/scripts.pory"
	.string "I've been helping my Dad sell fruit we\n"
	.string "import from Hoenn.$"

TosaPort_PSPKid_Text_1:
# 302 "data/maps/TosaPort/scripts.pory"
	.string "You found Dad? Did he give you some\n"
	.string "batteries?$"

TosaPort_PSPKid_Text_2:
# 305 "data/maps/TosaPort/scripts.pory"
	.string "Huh? Dad said he gave you one. Did you\n"
	.string "lose it?$"

TosaPort_PSPKid_Text_3:
# 310 "data/maps/TosaPort/scripts.pory"
	.string "{PLAYER} handed over the Cell\n"
	.string "Battery.$"

TosaPort_PSPKid_Text_4:
# 311 "data/maps/TosaPort/scripts.pory"
	.string "A Cell Battery? I guess that'd work!$"

TosaPort_PSPKid_Text_5:
# 314 "data/maps/TosaPort/scripts.pory"
	.string "Thanks mister. Now that I've got some\n"
	.string "power again, do you fancy trading\l"
	.string "Pokémon with me? If you have a\l"
	.string "Magnemite I can trade you my Corsola.$"

TosaPort_PSPKid_Text_6:
# 316 "data/maps/TosaPort/scripts.pory"
	.string "Thanks miss. Now that I've got some\n"
	.string "power again, do you fancy trading\l"
	.string "Pokémon with me? If you have a\l"
	.string "Magnemite I can trade you my Corsola.$"

TosaPort_PSPKid_Text_7:
# 323 "data/maps/TosaPort/scripts.pory"
	.string "Did you find Dad yet? He said he was\n"
	.string "only getting a snack. That was ages\l"
	.string "ago…$"

TosaPort_PSPKid_Text_8:
# 327 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, Dad's making me watch his stall.\n"
	.string "At least he let me bring my GBA.$"

TosaPort_PSPKid_Text_9:
# 329 "data/maps/TosaPort/scripts.pory"
	.string "…And now the batteries are flat! Dad\n"
	.string "wandered off for a snack ages ago.$"

TosaPort_PSPKid_Text_10:
# 330 "data/maps/TosaPort/scripts.pory"
	.string "Could you find him and ask him for some\n"
	.string "batteries?$"

TosaPort_PSPKid_Text_11:
# 332 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, adults are so lame!$"

TosaPort_PSPKid_Text_12:
# 336 "data/maps/TosaPort/scripts.pory"
	.string "Thanks! Dad said he was in the mood for\n"
	.string "something sweet.$"

TosaPort_StallDad_Text_0:
# 349 "data/maps/TosaPort/scripts.pory"
	.string "Go on, take that battery to my boy. I'll\n"
	.string "be back… after one more gateau.$"

TosaPort_StallDad_Text_1:
# 353 "data/maps/TosaPort/scripts.pory"
	.string "Huh? My boy sent you? He wants\n"
	.string "batteries for that game of his?$"

TosaPort_StallDad_Text_2:
# 354 "data/maps/TosaPort/scripts.pory"
	.string "Hmm… All I've got is this. I picked it up\n"
	.string "at the market this morning. A battery's\l"
	.string "a battery, right?$"

TosaPort_StallDad_Text_3:
# 360 "data/maps/TosaPort/scripts.pory"
	.string "Tell him I'll be back once I've finished\n"
	.string "my Old Gateau. Or two.$"

TosaPort_StallDad_Text_4:
# 367 "data/maps/TosaPort/scripts.pory"
	.string "My boy runs that fruit stall better\n"
	.string "than I do! Shh… don't tell him I said\l"
	.string "that.$"

TosaPort_StallDad_Text_5:
# 371 "data/maps/TosaPort/scripts.pory"
	.string "Mmm! The Old Gateau at this stall is\n"
	.string "magnifique. Don't tell anyone you saw me\l"
	.string "here. I'm meant to be minding our fruit\l"
	.string "stall.$"

TosaPort_RepelGuy_Text_0:
# 379 "data/maps/TosaPort/scripts.pory"
	.string "I read in “Pokémon Garden” that\n"
	.string "spraying repel on your flowers can keep\l"
	.string "bug Pokémon at bay.$"

TosaPort_BreakTrucker_Text_0:
# 389 "data/maps/TosaPort/scripts.pory"
	.string "Buzz off, I'm on my break!$"

TosaPort_LoadingTrucker_Text_0:
# 397 "data/maps/TosaPort/scripts.pory"
	.string "I wish my Pokémon was strong enough to\n"
	.string "load this truck...$"

TosaPort_OldMan_Text_0:
# 409 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu… I asked her again, and she\n"
	.string "said yes again. Some things never\l"
	.string "change.$"

TosaPort_OldMan_Text_1:
# 420 "data/maps/TosaPort/scripts.pory"
	.string "(Psst… When I was young, Heart Scales\n"
	.string "used to wash up on the riverbanks of\l"
	.string "the reserve, just north of here.)$"

TosaPort_OldMan_Text_2:
# 424 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu...I met my wife at this very\n"
	.string "spot 10 years ago.$"

TosaPort_OldMan_Text_3:
# 427 "data/maps/TosaPort/scripts.pory"
	.string "(Psst… I proposed to her right here,\n"
	.string "with a Heart Scale. I lost it years ago.)$"

TosaPort_OldMan_Text_4:
# 428 "data/maps/TosaPort/scripts.pory"
	.string "(I'd love to see one again… Fu-fu…)$"

TosaPort_OldMan_ShowHeartScale_Text_0:
# 440 "data/maps/TosaPort/scripts.pory"
	.string "Wh-what's that? A Heart Scale?! Could\n"
	.string "I… borrow it? There's something I'd like\l"
	.string "to do.$"

TosaPort_OldMan_ShowHeartScale_Text_1:
# 442 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu… I understand. It's a precious\n"
	.string "thing.$"

TosaPort_OldMan_ShowHeartScale_Text_2:
# 448 "data/maps/TosaPort/scripts.pory"
	.string "Hm? Your Bag looks awfully full, young\n"
	.string "one. Come back once you've made a little\l"
	.string "room.$"

TosaPort_OldMan_ShowHeartScale_Text_3:
# 453 "data/maps/TosaPort/scripts.pory"
	.string "{PLAYER} handed over the Heart Scale.$"

TosaPort_OldMan_ShowHeartScale_Text_4:
# 458 "data/maps/TosaPort/scripts.pory"
	.string "Dear… do you remember this? Will you\n"
	.string "marry me… again?$"

TosaPort_OldMan_ShowHeartScale_Text_5:
# 462 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha! You old romantic… Of course I\n"
	.string "will!$"

TosaPort_OldMan_ShowHeartScale_Text_6:
# 466 "data/maps/TosaPort/scripts.pory"
	.string "Thank you, dearie. Please, take this. It\n"
	.string "was a gift for our Pokémon we received\l"
	.string "on our wedding day. I hope it brings you\l"
	.string "and your Pokémon as much joy as it did\l"
	.string "for us.$"

TosaPort_OldWoman_Text_0:
# 480 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha… he proposed again! At our\n"
	.string "age! Life is too short, dearie.$"

TosaPort_OldWoman_Text_1:
# 484 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha...we were so reckless back\n"
	.string "then...life is too short...$"

TosaPort_Skitty_Text_0:
# 494 "data/maps/TosaPort/scripts.pory"
	.string "Skitty: Meooow!$"

TosaPort_Fisherman_Text_0:
# 503 "data/maps/TosaPort/scripts.pory"
	.string "I came all this way from Pasira City to\n"
	.string "fish in the reserve.$"

TosaPort_Tuber_Text_0:
# 512 "data/maps/TosaPort/scripts.pory"
	.string "Awww...\n"
	.string "I was hoping to swim while visiting\l"
	.string "Daddy, but the current here is too\l"
	.string "strong!$"

TosaPort_ColdStorageGuard_Text_0:
# 523 "data/maps/TosaPort/scripts.pory"
	.string "The site's open, pal, but mind your\n"
	.string "step. The floor in there is solid ice.$"

TosaPort_Martin_Text_0:
# 532 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Martin's Mart!\n"
	.string "Trainer Supplies and Sundries.$"

TosaPort_Martin_Text_1:
# 535 "data/maps/TosaPort/scripts.pory"
	.string "Come back soon!$"
