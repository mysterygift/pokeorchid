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
@ The player arrives with their Rotom Phone (PHONE on the start menu, quests enabled). It stays
# 8 "data/maps/TosaPort/scripts.pory"
@ offline until Prof. Palm connects it in Palm Labs (FLAG_SYS_PHONE_ACTIVE).
# 9 "data/maps/TosaPort/scripts.pory"
TosaPort_OnTransition:
# 10 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_VISITED_TOSA_PORT
# 11 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_SYS_ROTOM_PHONE_GET
# 12 "data/maps/TosaPort/scripts.pory"
	end
# 13 "data/maps/TosaPort/scripts.pory"

# 14 "data/maps/TosaPort/scripts.pory"
@ After object events exist; RunScriptImmediately — use only instant cmds (turnobject is OK).
# 15 "data/maps/TosaPort/scripts.pory"
TosaPort_OnWarp:
# 16 "data/maps/TosaPort/scripts.pory"
	map_script_2 VAR_TEMP_0, 0, TosaPort_EventScript_WarpFaceNorthIfNoMon
# 17 "data/maps/TosaPort/scripts.pory"
	.2byte 0
# 18 "data/maps/TosaPort/scripts.pory"

# 19 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_WarpFaceNorthIfNoMon::
# 20 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_SYS_POKEMON_GET, TosaPort_EventScript_WarpFaceNorthIfNoMon_End
# 21 "data/maps/TosaPort/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 22 "data/maps/TosaPort/scripts.pory"

# 23 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_WarpFaceNorthIfNoMon_End::
# 24 "data/maps/TosaPort/scripts.pory"
	end
# 25 "data/maps/TosaPort/scripts.pory"

# 26 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_TownSign::
# 27 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TownSign, MSGBOX_SIGN
# 28 "data/maps/TosaPort/scripts.pory"
	end
# 29 "data/maps/TosaPort/scripts.pory"

# 30 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_TruckSign::
# 31 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_TruckSign, MSGBOX_SIGN
# 32 "data/maps/TosaPort/scripts.pory"
	end
# 33 "data/maps/TosaPort/scripts.pory"

# 34 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_ColdStorageSign::
# 35 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_ColdStorageSign, MSGBOX_SIGN
# 36 "data/maps/TosaPort/scripts.pory"
	end
# 37 "data/maps/TosaPort/scripts.pory"

# 38 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GatewaySign::
# 39 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GatewaySign, MSGBOX_SIGN
# 40 "data/maps/TosaPort/scripts.pory"
	end
# 41 "data/maps/TosaPort/scripts.pory"

# 42 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideTop::
# 43 "data/maps/TosaPort/scripts.pory"
	lockall
# 44 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 45 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideNoticePlayer
# 46 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkLeft
# 47 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 48 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideGiveStarter
# 49 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_WalkRight
# 50 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 51 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_EventScript_StarterGuideFinish
# 52 "data/maps/TosaPort/scripts.pory"

# 53 "data/maps/TosaPort/scripts.pory"
@ The tile below the aide (24,36) is off the jetty, so come round via (23,35).
# 54 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideBottom::
# 55 "data/maps/TosaPort/scripts.pory"
	lockall
# 56 "data/maps/TosaPort/scripts.pory"
	goto_if_set FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
# 57 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideNoticePlayer
# 58 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, TosaPort_Movement_AideToBottomRow
# 59 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 60 "data/maps/TosaPort/scripts.pory"
	call TosaPort_EventScript_StarterGuideGiveStarter
# 61 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, TosaPort_Movement_AideFromBottomRow
# 62 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 63 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_EventScript_StarterGuideFinish
# 64 "data/maps/TosaPort/scripts.pory"

# 65 "data/maps/TosaPort/scripts.pory"
@ Coord-triggered cutscene: use MSGBOX_DEFAULT + closemessage, never MSGBOX_NPC
# 66 "data/maps/TosaPort/scripts.pory"
@ (its faceplayer/release would turn a stale object and unfreeze every NPC mid-scene).
# 67 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideNoticePlayer::
# 68 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_FacePlayer
# 69 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 70 "data/maps/TosaPort/scripts.pory"
	playse SE_M_METRONOME
# 71 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_QuestionMark
# 72 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 73 "data/maps/TosaPort/scripts.pory"
	delay 16
# 74 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_YouMustBePlayer, MSGBOX_DEFAULT
# 75 "data/maps/TosaPort/scripts.pory"
	closemessage
# 76 "data/maps/TosaPort/scripts.pory"
	return
# 77 "data/maps/TosaPort/scripts.pory"

# 78 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideGiveStarter::
# 79 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_FaceRight
# 80 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 81 "data/maps/TosaPort/scripts.pory"
	playse SE_PIN
# 82 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_STARTER_AIDE, Common_Movement_ExclamationMark
# 83 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 84 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_GivePokemon, MSGBOX_DEFAULT
# 85 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_PeerInsideBag, MSGBOX_DEFAULT
# 86 "data/maps/TosaPort/scripts.pory"
	closemessage
# 87 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 88 "data/maps/TosaPort/scripts.pory"
	fadescreen FADE_TO_BLACK
# 89 "data/maps/TosaPort/scripts.pory"
	special ChooseStarterOverworld
# 90 "data/maps/TosaPort/scripts.pory"
	waitstate
# 91 "data/maps/TosaPort/scripts.pory"
	lockall
# 92 "data/maps/TosaPort/scripts.pory"
	bufferleadmonspeciesname STR_VAR_2
# 93 "data/maps/TosaPort/scripts.pory"
	playfanfare MUS_OBTAIN_TMHM
# 94 "data/maps/TosaPort/scripts.pory"
	message TosaPort_Text_ReceivedPokemon
# 95 "data/maps/TosaPort/scripts.pory"
	waitmessage
# 96 "data/maps/TosaPort/scripts.pory"
	waitfanfare
# 97 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_Nickname, MSGBOX_YESNO
# 98 "data/maps/TosaPort/scripts.pory"
	call_if_eq VAR_RESULT, 1, TosaPort_EventScript_GiveNickname
# 99 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG
# 100 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
# 101 "data/maps/TosaPort/scripts.pory"
	closemessage
# 102 "data/maps/TosaPort/scripts.pory"
	return
# 103 "data/maps/TosaPort/scripts.pory"

# 104 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuideFinish::
# 105 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE, 1
# 106 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 107 "data/maps/TosaPort/scripts.pory"
	releaseall
# 108 "data/maps/TosaPort/scripts.pory"
	end
# 109 "data/maps/TosaPort/scripts.pory"

# 110 "data/maps/TosaPort/scripts.pory"
@ ChangePokemonNickname reads the party slot from VAR_0x8004. The naming screen
# 111 "data/maps/TosaPort/scripts.pory"
@ pauses the script itself, so no waitstate (one here would hang forever).
# 112 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_GiveNickname::
# 113 "data/maps/TosaPort/scripts.pory"
	call Common_EventScript_GetGiftMonPartySlot
# 114 "data/maps/TosaPort/scripts.pory"
	call Common_EventScript_NameReceivedPartyMon
# 115 "data/maps/TosaPort/scripts.pory"
	lockall
# 116 "data/maps/TosaPort/scripts.pory"
	return
# 117 "data/maps/TosaPort/scripts.pory"

# 118 "data/maps/TosaPort/scripts.pory"
TosaPort_EventScript_StarterGuide_AfterStarter::
# 119 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 120 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
# 121 "data/maps/TosaPort/scripts.pory"
	releaseall
# 122 "data/maps/TosaPort/scripts.pory"
	end
# 123 "data/maps/TosaPort/scripts.pory"

# 124 "data/maps/TosaPort/scripts.pory"
TosaPort_Movement_AideToBottomRow:
# 125 "data/maps/TosaPort/scripts.pory"
	walk_left
# 126 "data/maps/TosaPort/scripts.pory"
	walk_down
# 127 "data/maps/TosaPort/scripts.pory"
	face_left
# 128 "data/maps/TosaPort/scripts.pory"
	step_end
# 129 "data/maps/TosaPort/scripts.pory"

# 130 "data/maps/TosaPort/scripts.pory"
TosaPort_Movement_AideFromBottomRow:
# 131 "data/maps/TosaPort/scripts.pory"
	walk_up
# 132 "data/maps/TosaPort/scripts.pory"
	walk_right
# 133 "data/maps/TosaPort/scripts.pory"
	step_end
# 134 "data/maps/TosaPort/scripts.pory"

# 135 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_YouMustBePlayer:
# 136 "data/maps/TosaPort/scripts.pory"
	.string "Ah! You must be {PLAYER}.\p"
# 137 "data/maps/TosaPort/scripts.pory"
	.string "Professor Palm sent me to meet you\n"
# 138 "data/maps/TosaPort/scripts.pory"
	.string "once the Seagallop-20 made port.$"
# 139 "data/maps/TosaPort/scripts.pory"

# 140 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GivePokemon:
# 141 "data/maps/TosaPort/scripts.pory"
	.string "I've brought you a little welcome\n"
# 142 "data/maps/TosaPort/scripts.pory"
	.string "present on behalf of the University.\p"
# 143 "data/maps/TosaPort/scripts.pory"
	.string "With the journey being so long from\n"
# 144 "data/maps/TosaPort/scripts.pory"
	.string "Galar, we figured you wouldn't bring\l"
# 145 "data/maps/TosaPort/scripts.pory"
	.string "your partners along.$"
# 146 "data/maps/TosaPort/scripts.pory"

# 147 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_PeerInsideBag:
# 148 "data/maps/TosaPort/scripts.pory"
	.string "You peer inside the bag.$"
# 149 "data/maps/TosaPort/scripts.pory"

# 150 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ReceivedPokemon:
# 151 "data/maps/TosaPort/scripts.pory"
	.string "You received a {STR_VAR_2}!$"
# 152 "data/maps/TosaPort/scripts.pory"

# 153 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_Nickname:
# 154 "data/maps/TosaPort/scripts.pory"
	.string "Would you like to give {STR_VAR_2} a\n"
# 155 "data/maps/TosaPort/scripts.pory"
	.string "nickname?$"
# 156 "data/maps/TosaPort/scripts.pory"

# 157 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_StarterGuideTelokHint:
# 158 "data/maps/TosaPort/scripts.pory"
	.string "The road to TELOK TOWN runs through\n"
# 159 "data/maps/TosaPort/scripts.pory"
	.string "the Tosa nature reserve to the north.\p"
# 160 "data/maps/TosaPort/scripts.pory"
	.string "You'll find Palm Labs there.$"
# 161 "data/maps/TosaPort/scripts.pory"

# 162 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TownSign:
# 163 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Tosa!\n"
# 164 "data/maps/TosaPort/scripts.pory"
	.string "- The Tosa Tourism Board$"
# 165 "data/maps/TosaPort/scripts.pory"

# 166 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_GatewaySign:
# 167 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Reserve Gateway\n"
# 168 "data/maps/TosaPort/scripts.pory"
	.string "Trainer passes strictly required$"
# 169 "data/maps/TosaPort/scripts.pory"

# 170 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_TruckSign:
# 171 "data/maps/TosaPort/scripts.pory"
	.string "Machamp Moving Co.\n"
# 172 "data/maps/TosaPort/scripts.pory"
	.string "No Load too Lumbersome!$"
# 173 "data/maps/TosaPort/scripts.pory"

# 174 "data/maps/TosaPort/scripts.pory"
TosaPort_Text_ColdStorageSign:
# 175 "data/maps/TosaPort/scripts.pory"
	.string "Tosa Port Cold Storage$"

TosaPort_PassAide::
# 180 "data/maps/TosaPort/scripts.pory"
	lockall
# 181 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_0, MSGBOX_AUTOCLOSE
# 182 "data/maps/TosaPort/scripts.pory"
	clearflag FLAG_HIDE_PASS_AIDE
# 183 "data/maps/TosaPort/scripts.pory"
	addobject LOCALID_PASS_AIDE
# 184 "data/maps/TosaPort/scripts.pory"
	showobjectat LOCALID_PASS_AIDE, MAP_TOSA_PORT
# 185 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PLAYER, TosaPort_PassAide_Movement_0
# 186 "data/maps/TosaPort/scripts.pory"
	playSE SE_M_METRONOME
# 187 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_1
# 190 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 191 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_1
# 192 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_TOSA_PASS
# 193 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_2
# 194 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_2
# 195 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 196 "data/maps/TosaPort/scripts.pory"
	delay 48
# 197 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_3
# 198 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 199 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_3
# 200 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_PassAide_Text_4
# 201 "data/maps/TosaPort/scripts.pory"
	closemessage
# 202 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_PASS_AIDE, TosaPort_PassAide_Movement_4
# 203 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 204 "data/maps/TosaPort/scripts.pory"
	hideobjectat LOCALID_PASS_AIDE, MAP_TOSA_PORT
# 205 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_RECEIVED_TOSA_PASS
# 206 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_HIDE_PASS_AIDE
# 207 "data/maps/TosaPort/scripts.pory"
	setvar VAR_TOSA_PORT_STATE, 2
# 208 "data/maps/TosaPort/scripts.pory"
	releaseall
	end


TosaPort_ScrubbingSailor::
# 213 "data/maps/TosaPort/scripts.pory"
	lock
# 214 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 215 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ScrubbingSailor_Text_0
# 217 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ShuntingSailor::
# 222 "data/maps/TosaPort/scripts.pory"
	lock
# 223 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 224 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ShuntingSailor_Text_0
# 226 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_VigorothCry::
# 231 "data/maps/TosaPort/scripts.pory"
	lock
# 232 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_VIGOROTH, CRY_MODE_NORMAL
# 233 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_VigorothCry_Text_0
# 234 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 235 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ChefStall::
# 240 "data/maps/TosaPort/scripts.pory"
	lock
# 241 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 242 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_CHEF_STALL_MET, TosaPort_ChefStall_2
# 259 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_2
# 261 "data/maps/TosaPort/scripts.pory"
	call TosaPort_ChefStall_GateauHint
# 262 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 263 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_3
# 264 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_ChefStall_2:
# 243 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_0
# 252 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_CHEF_STALL_MET
# 253 "data/maps/TosaPort/scripts.pory"
	call TosaPort_ChefStall_GateauHint
# 254 "data/maps/TosaPort/scripts.pory"
	pokemart ChefStallGoods
# 255 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_Text_1
# 256 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ChefStall_GateauHint::
# 271 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_TASTE_OF_HOME
# 272 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_ChefStall_GateauHint_3
TosaPort_ChefStall_GateauHint_1:
	return

TosaPort_ChefStall_GateauHint_2:
# 273 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ChefStall_GateauHint_Text_0
# 274 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_OLD_GATEAU
# 275 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_ChefStall_GateauHint_6
	goto TosaPort_ChefStall_GateauHint_1

TosaPort_ChefStall_GateauHint_3:
# 272 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_RECEIVED_CHEF_OLD_GATEAU, TosaPort_ChefStall_GateauHint_2
	goto TosaPort_ChefStall_GateauHint_1

TosaPort_ChefStall_GateauHint_6:
# 276 "data/maps/TosaPort/scripts.pory"
	setflag FLAG_RECEIVED_CHEF_OLD_GATEAU
	goto TosaPort_ChefStall_GateauHint_1


	.align 2
# 282 "data/maps/TosaPort/scripts.pory"
ChefStallGoods:
# 283 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_LAVA_COOKIE
# 284 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PEWTER_CRUNCHIES
# 285 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_OLD_GATEAU
# 286 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_BIG_MALASADA
# 287 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_SHALOUR_SABLE
	.2byte ITEM_NONE

TosaPort_GBAKid::
# 293 "data/maps/TosaPort/scripts.pory"
	lock
# 294 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 295 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_SYS_ROTOM_PHONE_GET, TosaPort_GBAKid_2
# 301 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_GBA_BATTERIES
# 302 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_GBAKid_5
# 307 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_GBA_BATTERIES
# 308 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_GBAKid_8
# 336 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_0
# 338 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_9
# 339 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_10, MSGBOX_YESNO
# 340 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, NO
	goto_if_eq TosaPort_GBAKid_11
# 345 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_12
# 346 "data/maps/TosaPort/scripts.pory"
	startquest QUEST_GBA_BATTERIES
# 347 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_2:
# 296 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_0
# 298 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_5:
# 303 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_1
# 304 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_8:
# 309 "data/maps/TosaPort/scripts.pory"
	subquestmenu QUEST_MENU_CHECK_COMPLETE, QUEST_GBA_BATTERIES, SUB_QUEST_1
# 310 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_GBAKid_14
# 332 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_8
# 333 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_11:
# 341 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_11
# 342 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_14:
# 311 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_2
# 312 "data/maps/TosaPort/scripts.pory"
	checkitem ITEM_CELL_BATTERY
# 313 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq TosaPort_GBAKid_17
# 318 "data/maps/TosaPort/scripts.pory"
	removeitem ITEM_CELL_BATTERY
# 319 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_4
# 320 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_5
# 321 "data/maps/TosaPort/scripts.pory"
	checkplayergender
# 322 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, MALE
	goto_if_eq TosaPort_GBAKid_20
# 325 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_7
TosaPort_GBAKid_19:
# 327 "data/maps/TosaPort/scripts.pory"
	subquestmenu QUEST_MENU_COMPLETE_QUEST, QUEST_GBA_BATTERIES, SUB_QUEST_2
# 328 "data/maps/TosaPort/scripts.pory"
	completequest QUEST_GBA_BATTERIES
# 329 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_17:
# 314 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_3
# 315 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_GBAKid_20:
# 323 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_GBAKid_Text_6
	goto TosaPort_GBAKid_19


TosaPort_StallDad::
# 352 "data/maps/TosaPort/scripts.pory"
	lock
# 353 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 354 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_GBA_BATTERIES
# 355 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_StallDad_2
# 374 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_GBA_BATTERIES
# 375 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_StallDad_5
# 380 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_5
# 381 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_2:
# 356 "data/maps/TosaPort/scripts.pory"
	subquestmenu QUEST_MENU_CHECK_COMPLETE, QUEST_GBA_BATTERIES, SUB_QUEST_1
# 357 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_StallDad_8
# 362 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_1
# 363 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_2
# 364 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_CELL_BATTERY
# 365 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq TosaPort_StallDad_11
# 369 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_3
# 370 "data/maps/TosaPort/scripts.pory"
	completesubquest QUEST_GBA_BATTERIES, SUB_QUEST_1
# 371 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_5:
# 376 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_4
# 377 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_8:
# 358 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_StallDad_Text_0
# 359 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_StallDad_11:
# 366 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_RepelGuy::
# 386 "data/maps/TosaPort/scripts.pory"
	lock
# 387 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 388 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_RepelGuy_Text_0
# 391 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_BreakTrucker::
# 396 "data/maps/TosaPort/scripts.pory"
	lock
# 397 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 398 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_BreakTrucker_Text_0
# 399 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_LoadingTrucker::
# 404 "data/maps/TosaPort/scripts.pory"
	lock
# 405 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 406 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_LoadingTrucker_Text_0
# 408 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldMan::
# 415 "data/maps/TosaPort/scripts.pory"
	lock
# 416 "data/maps/TosaPort/scripts.pory"
	goto_if_unset FLAG_SYS_ROTOM_PHONE_GET, TosaPort_OldMan_2
# 422 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_HEART_SCALE
# 423 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_5
# 428 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_HEART_SCALE
# 429 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_8
# 439 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_0
# 441 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 442 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_3
# 443 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_4
# 444 "data/maps/TosaPort/scripts.pory"
	startquest QUEST_HEART_SCALE
# 445 "data/maps/TosaPort/scripts.pory"
	checkitem ITEM_HEART_SCALE
# 446 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_11
TosaPort_OldMan_10:
# 449 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_2:
# 417 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_0
# 419 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_5:
# 424 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_1
# 425 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_8:
# 430 "data/maps/TosaPort/scripts.pory"
	checkitem ITEM_HEART_SCALE
# 431 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldMan_14
TosaPort_OldMan_13:
# 434 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 435 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_Text_2
# 436 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_11:
# 447 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_OldMan_ShowHeartScale
	goto TosaPort_OldMan_10

TosaPort_OldMan_14:
# 432 "data/maps/TosaPort/scripts.pory"
	goto TosaPort_OldMan_ShowHeartScale
	goto TosaPort_OldMan_13


TosaPort_OldMan_ShowHeartScale::
# 454 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 455 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_0, MSGBOX_YESNO
# 456 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, NO
	goto_if_eq TosaPort_OldMan_ShowHeartScale_2
# 461 "data/maps/TosaPort/scripts.pory"
	checkitemspace ITEM_SOOTHE_BELL
# 462 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq TosaPort_OldMan_ShowHeartScale_5
# 467 "data/maps/TosaPort/scripts.pory"
	removeitem ITEM_HEART_SCALE
# 468 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_3
# 469 "data/maps/TosaPort/scripts.pory"
	closemessage
# 470 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_MAN, TosaPort_PassAide_Movement_2
# 471 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_OldMan_ShowHeartScale_Movement_0
# 472 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 473 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_4
# 474 "data/maps/TosaPort/scripts.pory"
	closemessage
# 475 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_OldMan_ShowHeartScale_Movement_1
# 476 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 477 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_5
# 478 "data/maps/TosaPort/scripts.pory"
	closemessage
# 479 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_PassAide_Movement_3
# 480 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 481 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_6
# 482 "data/maps/TosaPort/scripts.pory"
	giveitem ITEM_SOOTHE_BELL
# 483 "data/maps/TosaPort/scripts.pory"
	completequest QUEST_HEART_SCALE
# 484 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_MAN, TosaPort_OldMan_ShowHeartScale_Movement_2
# 485 "data/maps/TosaPort/scripts.pory"
	applymovement LOCALID_TOSA_PORT_OLD_WOMAN, TosaPort_OldMan_ShowHeartScale_Movement_2
# 486 "data/maps/TosaPort/scripts.pory"
	waitmovement 0
# 487 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_ShowHeartScale_2:
# 457 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_1
# 458 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldMan_ShowHeartScale_5:
# 463 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldMan_ShowHeartScale_Text_2
# 464 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_OldWoman::
# 492 "data/maps/TosaPort/scripts.pory"
	lock
# 493 "data/maps/TosaPort/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_HEART_SCALE
# 494 "data/maps/TosaPort/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne TosaPort_OldWoman_2
# 499 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_1
# 501 "data/maps/TosaPort/scripts.pory"
	release
	end

TosaPort_OldWoman_2:
# 495 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_OldWoman_Text_0
# 496 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Skitty::
# 506 "data/maps/TosaPort/scripts.pory"
	lock
# 507 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 508 "data/maps/TosaPort/scripts.pory"
	playmoncry SPECIES_SKITTY, CRY_MODE_NORMAL
# 509 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Skitty_Text_0
# 510 "data/maps/TosaPort/scripts.pory"
	waitmoncry
# 511 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Fisherman::
# 516 "data/maps/TosaPort/scripts.pory"
	lock
# 517 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 518 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Fisherman_Text_0
# 520 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Tuber::
# 525 "data/maps/TosaPort/scripts.pory"
	lock
# 526 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 527 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Tuber_Text_0
# 531 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_ColdStorageGuard::
# 536 "data/maps/TosaPort/scripts.pory"
	lock
# 537 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 538 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_ColdStorageGuard_Text_0
# 540 "data/maps/TosaPort/scripts.pory"
	release
	end


TosaPort_Martin::
# 545 "data/maps/TosaPort/scripts.pory"
	lock
# 546 "data/maps/TosaPort/scripts.pory"
	faceplayer
# 547 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_0
# 549 "data/maps/TosaPort/scripts.pory"
	pokemart MartinsMartGoods
# 550 "data/maps/TosaPort/scripts.pory"
	msgbox TosaPort_Martin_Text_1
# 551 "data/maps/TosaPort/scripts.pory"
	release
	end


	.align 2
# 555 "data/maps/TosaPort/scripts.pory"
MartinsMartGoods:
# 556 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POTION
# 557 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_POKE_BALL
# 558 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 559 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 560 "data/maps/TosaPort/scripts.pory"
	.2byte ITEM_REPEL
	.2byte ITEM_NONE

# 185 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_0:
# 185 "data/maps/TosaPort/scripts.pory"
	emote_question_mark
# 185 "data/maps/TosaPort/scripts.pory"
	face_down
	step_end

# 187 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_1:
# 188 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 188 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 188 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 188 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
# 188 "data/maps/TosaPort/scripts.pory"
	walk_fast_up
	step_end

# 194 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_2:
# 194 "data/maps/TosaPort/scripts.pory"
	face_right
	step_end

# 197 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_3:
# 197 "data/maps/TosaPort/scripts.pory"
	face_player
	step_end

# 202 "data/maps/TosaPort/scripts.pory"
TosaPort_PassAide_Movement_4:
# 202 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 202 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 202 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 202 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
# 202 "data/maps/TosaPort/scripts.pory"
	walk_fast_down
	step_end

# 471 "data/maps/TosaPort/scripts.pory"
TosaPort_OldMan_ShowHeartScale_Movement_0:
# 471 "data/maps/TosaPort/scripts.pory"
	face_left
	step_end

# 475 "data/maps/TosaPort/scripts.pory"
TosaPort_OldMan_ShowHeartScale_Movement_1:
# 475 "data/maps/TosaPort/scripts.pory"
	emote_heart
	step_end

# 484 "data/maps/TosaPort/scripts.pory"
TosaPort_OldMan_ShowHeartScale_Movement_2:
# 484 "data/maps/TosaPort/scripts.pory"
	face_down
	step_end

TosaPort_PassAide_Text_0:
# 181 "data/maps/TosaPort/scripts.pory"
	.string "WAIT! {PLAYER}!$"

TosaPort_PassAide_Text_1:
# 191 "data/maps/TosaPort/scripts.pory"
	.string "I...I need to give you this as well.$"

TosaPort_PassAide_Text_2:
# 193 "data/maps/TosaPort/scripts.pory"
	.string "Without a Tosa Pass, you won't be\n"
	.string "allowed onto the reserve. Normally you\l"
	.string "could take the underground...$"

TosaPort_PassAide_Text_3:
# 199 "data/maps/TosaPort/scripts.pory"
	.string "One more thing, if you haven't already I\n"
	.string "recommend you check out the markets\l"
	.string "here in the port. There's all sorts of\l"
	.string "supplies a trainer might need.$"

TosaPort_PassAide_Text_4:
# 200 "data/maps/TosaPort/scripts.pory"
	.string "Anyway, that's all from me. You better\n"
	.string "get going, I wouldn't want to keep the\l"
	.string "Professor waiting!$"

TosaPort_ScrubbingSailor_Text_0:
# 215 "data/maps/TosaPort/scripts.pory"
	.string "Gotta keep this jetty looking ship-\n"
	.string "shape!$"

TosaPort_ShuntingSailor_Text_0:
# 224 "data/maps/TosaPort/scripts.pory"
	.string "It's a good thing I have my Vigoroth\n"
	.string "with me!$"

TosaPort_VigorothCry_Text_0:
# 233 "data/maps/TosaPort/scripts.pory"
	.string "Vigoroth: Urraw!$"

TosaPort_ChefStall_Text_0:
# 243 "data/maps/TosaPort/scripts.pory"
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
# 255 "data/maps/TosaPort/scripts.pory"
	.string "See you again, mon ami!$"

TosaPort_ChefStall_Text_2:
# 259 "data/maps/TosaPort/scripts.pory"
	.string "Good to see you mon ami!\n"
	.string "What can I get for you?$"

TosaPort_ChefStall_Text_3:
# 263 "data/maps/TosaPort/scripts.pory"
	.string "Always a pleasure, mon ami!$"

TosaPort_ChefStall_GateauHint_Text_0:
# 273 "data/maps/TosaPort/scripts.pory"
	.string "Quoi? Someone from Kalos is missing\n"
	.string "home? Bien sûr, they only need a taste\l"
	.string "of my delicious gateau! Bring this to\l"
	.string "ton ami, mon ami.$"

TosaPort_GBAKid_Text_0:
# 296 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, Dad's making me watch his stall.\n"
	.string "At least he let me bring my GBA.$"

TosaPort_GBAKid_Text_1:
# 303 "data/maps/TosaPort/scripts.pory"
	.string "I've been helping my Dad sell fruit we\n"
	.string "import from Hoenn.$"

TosaPort_GBAKid_Text_2:
# 311 "data/maps/TosaPort/scripts.pory"
	.string "You found Dad? Did he give you some\n"
	.string "batteries?$"

TosaPort_GBAKid_Text_3:
# 314 "data/maps/TosaPort/scripts.pory"
	.string "Huh? Dad said he gave you one. Did you\n"
	.string "lose it?$"

TosaPort_GBAKid_Text_4:
# 319 "data/maps/TosaPort/scripts.pory"
	.string "{PLAYER} handed over the Cell\n"
	.string "Battery.$"

TosaPort_GBAKid_Text_5:
# 320 "data/maps/TosaPort/scripts.pory"
	.string "A Cell Battery? I guess that'd work!$"

TosaPort_GBAKid_Text_6:
# 323 "data/maps/TosaPort/scripts.pory"
	.string "Thanks mister. Now that I've got some\n"
	.string "power again, do you fancy trading\l"
	.string "Pokémon with me? If you have a\l"
	.string "Magnemite I can trade you my Corsola.$"

TosaPort_GBAKid_Text_7:
# 325 "data/maps/TosaPort/scripts.pory"
	.string "Thanks miss. Now that I've got some\n"
	.string "power again, do you fancy trading\l"
	.string "Pokémon with me? If you have a\l"
	.string "Magnemite I can trade you my Corsola.$"

TosaPort_GBAKid_Text_8:
# 332 "data/maps/TosaPort/scripts.pory"
	.string "Did you find Dad yet? He said he was\n"
	.string "only getting a snack. That was ages\l"
	.string "ago…$"

TosaPort_GBAKid_Text_9:
# 338 "data/maps/TosaPort/scripts.pory"
	.string "…And now the batteries are flat! Dad\n"
	.string "wandered off for a snack ages ago.$"

TosaPort_GBAKid_Text_10:
# 339 "data/maps/TosaPort/scripts.pory"
	.string "Could you find him and ask him for some\n"
	.string "batteries?$"

TosaPort_GBAKid_Text_11:
# 341 "data/maps/TosaPort/scripts.pory"
	.string "Ugh, adults are so lame!$"

TosaPort_GBAKid_Text_12:
# 345 "data/maps/TosaPort/scripts.pory"
	.string "Thanks! Dad said he was in the mood for\n"
	.string "something sweet.$"

TosaPort_StallDad_Text_0:
# 358 "data/maps/TosaPort/scripts.pory"
	.string "Go on, take that battery to my boy. I'll\n"
	.string "be back… after one more gateau.$"

TosaPort_StallDad_Text_1:
# 362 "data/maps/TosaPort/scripts.pory"
	.string "Huh? My boy sent you? He wants\n"
	.string "batteries for that game of his?$"

TosaPort_StallDad_Text_2:
# 363 "data/maps/TosaPort/scripts.pory"
	.string "Hmm… All I've got is this. I picked it up\n"
	.string "at the market this morning. A battery's\l"
	.string "a battery, right?$"

TosaPort_StallDad_Text_3:
# 369 "data/maps/TosaPort/scripts.pory"
	.string "Tell him I'll be back once I've finished\n"
	.string "my Old Gateau. Or two.$"

TosaPort_StallDad_Text_4:
# 376 "data/maps/TosaPort/scripts.pory"
	.string "My boy runs that fruit stall better\n"
	.string "than I do! Shh… don't tell him I said\l"
	.string "that.$"

TosaPort_StallDad_Text_5:
# 380 "data/maps/TosaPort/scripts.pory"
	.string "Mmm! The Old Gateau at this stall is\n"
	.string "magnifique. Don't tell anyone you saw me\l"
	.string "here. I'm meant to be minding our fruit\l"
	.string "stall.$"

TosaPort_RepelGuy_Text_0:
# 388 "data/maps/TosaPort/scripts.pory"
	.string "I read in “Pokémon Garden” that\n"
	.string "spraying repel on your flowers can keep\l"
	.string "bug Pokémon at bay.$"

TosaPort_BreakTrucker_Text_0:
# 398 "data/maps/TosaPort/scripts.pory"
	.string "Buzz off, I'm on my break!$"

TosaPort_LoadingTrucker_Text_0:
# 406 "data/maps/TosaPort/scripts.pory"
	.string "I wish my Pokémon was strong enough to\n"
	.string "load this truck...$"

TosaPort_OldMan_Text_0:
# 417 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu...I met my wife at this very\n"
	.string "spot 10 years ago.$"

TosaPort_OldMan_Text_1:
# 424 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu-fu… I asked her again, and she\n"
	.string "said yes again. Some things never\l"
	.string "change.$"

TosaPort_OldMan_Text_2:
# 435 "data/maps/TosaPort/scripts.pory"
	.string "(Psst… When I was young, Heart Scales\n"
	.string "used to wash up on the riverbanks of\l"
	.string "the reserve, just north of here.)$"

TosaPort_OldMan_Text_3:
# 442 "data/maps/TosaPort/scripts.pory"
	.string "(Psst… I proposed to her right here,\n"
	.string "with a Heart Scale. I lost it years ago.)$"

TosaPort_OldMan_Text_4:
# 443 "data/maps/TosaPort/scripts.pory"
	.string "(I'd love to see one again… Fu-fu…)$"

TosaPort_OldMan_ShowHeartScale_Text_0:
# 455 "data/maps/TosaPort/scripts.pory"
	.string "Wh-what's that? A Heart Scale?! Could\n"
	.string "I… borrow it? There's something I'd like\l"
	.string "to do.$"

TosaPort_OldMan_ShowHeartScale_Text_1:
# 457 "data/maps/TosaPort/scripts.pory"
	.string "Fu-fu… I understand. It's a precious\n"
	.string "thing.$"

TosaPort_OldMan_ShowHeartScale_Text_2:
# 463 "data/maps/TosaPort/scripts.pory"
	.string "Hm? Your Bag looks awfully full, young\n"
	.string "one. Come back once you've made a little\l"
	.string "room.$"

TosaPort_OldMan_ShowHeartScale_Text_3:
# 468 "data/maps/TosaPort/scripts.pory"
	.string "{PLAYER} handed over the Heart Scale.$"

TosaPort_OldMan_ShowHeartScale_Text_4:
# 473 "data/maps/TosaPort/scripts.pory"
	.string "Dear… do you remember this? Will you\n"
	.string "marry me… again?$"

TosaPort_OldMan_ShowHeartScale_Text_5:
# 477 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha! You old romantic… Of course I\n"
	.string "will!$"

TosaPort_OldMan_ShowHeartScale_Text_6:
# 481 "data/maps/TosaPort/scripts.pory"
	.string "Thank you, dearie. Please, take this. It\n"
	.string "was a gift for our Pokémon we received\l"
	.string "on our wedding day. I hope it brings you\l"
	.string "and your Pokémon as much joy as it did\l"
	.string "for us.$"

TosaPort_OldWoman_Text_0:
# 495 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha… he proposed again! At our\n"
	.string "age! Life is too short, dearie.$"

TosaPort_OldWoman_Text_1:
# 499 "data/maps/TosaPort/scripts.pory"
	.string "Ha-ha-ha...we were so reckless back\n"
	.string "then...life is too short...$"

TosaPort_Skitty_Text_0:
# 509 "data/maps/TosaPort/scripts.pory"
	.string "Skitty: Meooow!$"

TosaPort_Fisherman_Text_0:
# 518 "data/maps/TosaPort/scripts.pory"
	.string "I came all this way from Pasira City to\n"
	.string "fish in the reserve.$"

TosaPort_Tuber_Text_0:
# 527 "data/maps/TosaPort/scripts.pory"
	.string "Awww...\n"
	.string "I was hoping to swim while visiting\l"
	.string "Daddy, but the current here is too\l"
	.string "strong!$"

TosaPort_ColdStorageGuard_Text_0:
# 538 "data/maps/TosaPort/scripts.pory"
	.string "The site's open, pal, but mind your\n"
	.string "step. The floor in there is solid ice.$"

TosaPort_Martin_Text_0:
# 547 "data/maps/TosaPort/scripts.pory"
	.string "Welcome to Martin's Mart!\n"
	.string "Trainer Supplies and Sundries.$"

TosaPort_Martin_Text_1:
# 550 "data/maps/TosaPort/scripts.pory"
	.string "Come back soon!$"
