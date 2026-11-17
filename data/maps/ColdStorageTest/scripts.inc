ColdStorageTest_MapScripts::
# 11 "data/maps/ColdStorageTest/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD
	.byte 0

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD:
# 12 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_GATE_OPEN, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_2
ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_1:
# 15 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_THAWED, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_4
	return

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_2:
# 13 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetGateOpen
	goto ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_1

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_4:
# 16 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetThawed
	return


ColdStorageTest_EventScript_TestAide::
# 24 "data/maps/ColdStorageTest/scripts.pory"
	lock
# 25 "data/maps/ColdStorageTest/scripts.pory"
	faceplayer
# 26 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_TestAide_Text_0, MSGBOX_YESNO
# 27 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, YES
	goto_if_eq ColdStorageTest_EventScript_TestAide_2
ColdStorageTest_EventScript_TestAide_1:
# 33 "data/maps/ColdStorageTest/scripts.pory"
	special HealPlayerParty
# 34 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_TestAide_Text_2
# 35 "data/maps/ColdStorageTest/scripts.pory"
	release
	end

ColdStorageTest_EventScript_TestAide_2:
# 28 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_GiveTestTeam
# 29 "data/maps/ColdStorageTest/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 30 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_TestAide_Text_1
# 31 "data/maps/ColdStorageTest/scripts.pory"
	waitfanfare
	goto ColdStorageTest_EventScript_TestAide_1


# 39 "data/maps/ColdStorageTest/scripts.pory"

# 40 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_GiveTestTeam::
# 41 "data/maps/ColdStorageTest/scripts.pory"
	callnative ZeroPlayerPartyMons
# 42 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_SERVINE, 30, ITEM_MIRACLE_SEED, move1=MOVE_MAGICAL_LEAF, move2=MOVE_MEGA_DRAIN, move3=MOVE_LEECH_SEED, move4=MOVE_SLAM
# 43 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_PIGNITE, 30, ITEM_CHARCOAL, move1=MOVE_ARM_THRUST, move2=MOVE_FLAME_CHARGE, move3=MOVE_EMBER, move4=MOVE_TAKE_DOWN
# 44 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_DEWOTT, 30, ITEM_MYSTIC_WATER, move1=MOVE_RAZOR_SHELL, move2=MOVE_WATER_PULSE, move3=MOVE_AERIAL_ACE, move4=MOVE_FURY_CUTTER
# 45 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_LUXIO, 30, ITEM_MAGNET, move1=MOVE_SPARK, move2=MOVE_BITE, move3=MOVE_THUNDER_SHOCK, move4=MOVE_CHARGE
# 46 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_STARAVIA, 30, ITEM_SHARP_BEAK, move1=MOVE_WING_ATTACK, move2=MOVE_AERIAL_ACE, move3=MOVE_QUICK_ATTACK, move4=MOVE_ENDEAVOR
# 47 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_KIRLIA, 30, ITEM_TWISTED_SPOON, move1=MOVE_PSYBEAM, move2=MOVE_DRAINING_KISS, move3=MOVE_HYPNOSIS, move4=MOVE_LIFE_DEW
# 48 "data/maps/ColdStorageTest/scripts.pory"
	@ met at Lv. 5, so the team obeys even on a save with no badges
# 49 "data/maps/ColdStorageTest/scripts.pory"
	callnative Script_SetPartyMetLevel, requests_effects=1
# 50 "data/maps/ColdStorageTest/scripts.pory"
	.byte 5
# 51 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 52 "data/maps/ColdStorageTest/scripts.pory"
	return

ColdStorageTest_EventScript_ItemStorageKey::
# 58 "data/maps/ColdStorageTest/scripts.pory"
	finditem ITEM_STORAGE_KEY
	end


ColdStorageTest_EventScript_ItemNeverMeltIce::
# 63 "data/maps/ColdStorageTest/scripts.pory"
	finditem ITEM_NEVER_MELT_ICE
	end


ColdStorageTest_EventScript_ItemSuperPotion::
# 68 "data/maps/ColdStorageTest/scripts.pory"
	finditem ITEM_SUPER_POTION
	end


ColdStorageTest_EventScript_Gate::
# 75 "data/maps/ColdStorageTest/scripts.pory"
	lockall
# 76 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_GATE_OPEN, ColdStorageTest_EventScript_Gate_2
# 80 "data/maps/ColdStorageTest/scripts.pory"
	checkitem ITEM_STORAGE_KEY
# 81 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, FALSE
	goto_if_eq ColdStorageTest_EventScript_Gate_5
# 86 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Gate_Text_1
# 87 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 88 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_UNLOCK
# 89 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetGateOpen
# 90 "data/maps/ColdStorageTest/scripts.pory"
	special DrawWholeMapView
# 91 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_COLD_STORAGE_GATE_OPEN
# 92 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 93 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Gate_Text_2
# 94 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end

ColdStorageTest_EventScript_Gate_2:
# 77 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end

ColdStorageTest_EventScript_Gate_5:
# 82 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Gate_Text_0
# 83 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end


ColdStorageTest_EventScript_SetGateOpen::
# 99 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 8, METATILE_ColdStorage_Floor_Hazard, FALSE
	return


ColdStorageTest_EventScript_Console::
# 106 "data/maps/ColdStorageTest/scripts.pory"
	lockall
# 107 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_THAWED, ColdStorageTest_EventScript_Console_2
# 121 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_2, MSGBOX_YESNO
# 122 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, YES
	goto_if_eq ColdStorageTest_EventScript_Console_7
ColdStorageTest_EventScript_Console_1:
# 134 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end

ColdStorageTest_EventScript_Console_2:
# 108 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_0, MSGBOX_YESNO
# 109 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, YES
	goto_if_eq ColdStorageTest_EventScript_Console_5
	goto ColdStorageTest_EventScript_Console_1

ColdStorageTest_EventScript_Console_5:
# 110 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 111 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_SWITCH
# 112 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 113 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetFrozen
# 114 "data/maps/ColdStorageTest/scripts.pory"
	special DrawWholeMapView
# 115 "data/maps/ColdStorageTest/scripts.pory"
	clearflag FLAG_COLD_STORAGE_THAWED
# 116 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_ICE_CRACK
# 117 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 118 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_1
	goto ColdStorageTest_EventScript_Console_1

ColdStorageTest_EventScript_Console_7:
# 123 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 124 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_SWITCH
# 125 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 126 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetThawed
# 127 "data/maps/ColdStorageTest/scripts.pory"
	special DrawWholeMapView
# 128 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_COLD_STORAGE_THAWED
# 129 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_ICE_BREAK
# 130 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 131 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_3
	goto ColdStorageTest_EventScript_Console_1


ColdStorageTest_EventScript_SetThawed::
# 139 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 10, METATILE_ColdStorage_Wet_ShadeW, FALSE
# 140 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 11, METATILE_ColdStorage_Wet_ShadeW, FALSE
# 141 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 8, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 142 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 9, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 143 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 12, METATILE_ColdStorage_Wet, FALSE
# 144 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 11, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 145 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 12, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 146 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 13, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 147 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 14, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 148 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 15, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 149 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 16, 11, METATILE_ColdStorage_Console_Off, TRUE
	return


ColdStorageTest_EventScript_SetFrozen::
# 154 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 10, METATILE_ColdStorage_Ice_ShadeW, FALSE
# 155 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 11, METATILE_ColdStorage_Ice_ShadeW, FALSE
# 156 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 8, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 157 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 9, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 158 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 12, METATILE_ColdStorage_Ice, FALSE
# 159 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 11, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 160 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 12, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 161 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 13, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 162 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 14, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 163 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 15, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 164 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 16, 11, METATILE_ColdStorage_Console_On, TRUE
	return


ColdStorageTest_EventScript_Grunt1::
# 171 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_1, ColdStorageTest_Text_Grunt1Intro, ColdStorageTest_Text_Grunt1Defeat
# 172 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt1_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_Grunt2::
# 177 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_2, ColdStorageTest_Text_Grunt2Intro, ColdStorageTest_Text_Grunt2Defeat
# 178 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt2_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_Grunt3::
# 183 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_3, ColdStorageTest_Text_Grunt3Intro, ColdStorageTest_Text_Grunt3Defeat
# 184 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt3_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_Grunt4::
# 189 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_4, ColdStorageTest_Text_Grunt4Intro, ColdStorageTest_Text_Grunt4Defeat
# 190 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt4_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_BossTrigger::
# 229 "data/maps/ColdStorageTest/scripts.pory"
	lockall
# 230 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_PIN
# 231 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_COLD_STORAGE_HARU, ColdStorageTest_EventScript_BossTrigger_Movement_0
# 232 "data/maps/ColdStorageTest/scripts.pory"
	waitmovement 0
# 233 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_0
# 234 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 235 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_PLAYER, ColdStorageTest_EventScript_BossTrigger_Movement_1
# 236 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_COLD_STORAGE_HARU, ColdStorageTest_EventScript_BossTrigger_Movement_2
# 237 "data/maps/ColdStorageTest/scripts.pory"
	waitmovement 0
# 238 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_1
# 239 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_2
# 240 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_3
# 241 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 242 "data/maps/ColdStorageTest/scripts.pory"
	goto ColdStorageTest_EventScript_ChoosePartyForMultiBattle
	return


# 245 "data/maps/ColdStorageTest/scripts.pory"

# 246 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_ChoosePartyForMultiBattle::
# 247 "data/maps/ColdStorageTest/scripts.pory"
	special SavePlayerParty
# 248 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_TO_BLACK
# 249 "data/maps/ColdStorageTest/scripts.pory"
	special ChooseHalfPartyForBattle
# 250 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_ne VAR_RESULT, 0, ColdStorageTest_EventScript_DoMultiBattle
# 251 "data/maps/ColdStorageTest/scripts.pory"
	special LoadPlayerParty
# 252 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_Text_HaruNoBackingOut, MSGBOX_DEFAULT
# 253 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 254 "data/maps/ColdStorageTest/scripts.pory"
	goto ColdStorageTest_EventScript_ChoosePartyForMultiBattle
# 255 "data/maps/ColdStorageTest/scripts.pory"

# 256 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_DoMultiBattle::
# 257 "data/maps/ColdStorageTest/scripts.pory"
	multi_2_vs_2 TRAINER_COLD_STORAGE_LEADER, ColdStorageTest_Text_LeaderDefeat, TRAINER_COLD_STORAGE_ADMIN, ColdStorageTest_Text_AdminDefeat, PARTNER_HARU
# 258 "data/maps/ColdStorageTest/scripts.pory"
	switch VAR_RESULT
# 259 "data/maps/ColdStorageTest/scripts.pory"
	case 1, ColdStorageTest_EventScript_WonMultiBattle
# 260 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_TO_BLACK
# 261 "data/maps/ColdStorageTest/scripts.pory"
	special SetCB2WhiteOut
# 262 "data/maps/ColdStorageTest/scripts.pory"
	waitstate
# 263 "data/maps/ColdStorageTest/scripts.pory"
	end

ColdStorageTest_EventScript_WonMultiBattle::
# 267 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_WonMultiBattle_Text_0
# 268 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 269 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_TO_BLACK
# 270 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_LEADER
# 271 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_ADMIN
# 272 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_HIDE_COLD_STORAGE_VILLAINS
# 273 "data/maps/ColdStorageTest/scripts.pory"
	setvar VAR_COLD_STORAGE_STATE, 1
# 274 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_FROM_BLACK
# 275 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_COLD_STORAGE_HARU, ColdStorageTest_EventScript_WonMultiBattle_Movement_0
# 276 "data/maps/ColdStorageTest/scripts.pory"
	waitmovement 0
# 277 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_WonMultiBattle_Text_1
# 278 "data/maps/ColdStorageTest/scripts.pory"
	special HealPlayerParty
# 279 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end


ColdStorageTest_EventScript_Haru::
# 284 "data/maps/ColdStorageTest/scripts.pory"
	lock
# 285 "data/maps/ColdStorageTest/scripts.pory"
	faceplayer
# 286 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_COLD_STORAGE_STATE, 0
	goto_if_eq ColdStorageTest_EventScript_Haru_2
# 289 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Haru_Text_1
ColdStorageTest_EventScript_Haru_1:
# 291 "data/maps/ColdStorageTest/scripts.pory"
	release
	end

ColdStorageTest_EventScript_Haru_2:
# 287 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Haru_Text_0
	goto ColdStorageTest_EventScript_Haru_1


ColdStorageTest_EventScript_Leader::
# 296 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Leader_Text_0, MSGBOX_NPC
	end


ColdStorageTest_EventScript_Admin::
# 301 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Admin_Text_0, MSGBOX_NPC
	end


# 231 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_BossTrigger_Movement_0:
# 231 "data/maps/ColdStorageTest/scripts.pory"
	face_down
# 231 "data/maps/ColdStorageTest/scripts.pory"
	emote_exclamation_mark
# 231 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 231 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 231 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
	step_end

# 235 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_BossTrigger_Movement_1:
# 235 "data/maps/ColdStorageTest/scripts.pory"
	walk_up
# 235 "data/maps/ColdStorageTest/scripts.pory"
	walk_up
	step_end

# 236 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_BossTrigger_Movement_2:
# 236 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 236 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 236 "data/maps/ColdStorageTest/scripts.pory"
	face_up
	step_end

# 275 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_WonMultiBattle_Movement_0:
# 275 "data/maps/ColdStorageTest/scripts.pory"
	face_left
	step_end

ColdStorageTest_EventScript_TestAide_Text_0:
# 26 "data/maps/ColdStorageTest/scripts.pory"
	.string "I'm here for testing. I can swap your\n"
	.string "party for a Lv. 30 team that suits this\l"
	.string "place.\p"
	.string "Your current party would be released.\n"
	.string "Swap?$"

ColdStorageTest_EventScript_TestAide_Text_1:
# 30 "data/maps/ColdStorageTest/scripts.pory"
	.string "{PLAYER} received the test team!\p"
	.string "Servine, Pignite, Dewott, Luxio,\n"
	.string "Staravia and Kirlia.$"

ColdStorageTest_EventScript_TestAide_Text_2:
# 34 "data/maps/ColdStorageTest/scripts.pory"
	.string "Your Pokémon are fully healed.\p"
	.string "Talk to me again whenever you want them\n"
	.string "patched up.$"

ColdStorageTest_EventScript_Gate_Text_0:
# 82 "data/maps/ColdStorageTest/scripts.pory"
	.string "A heavy security gate. It's locked.\p"
	.string "The key must be somewhere in the\n"
	.string "warehouse.$"

ColdStorageTest_EventScript_Gate_Text_1:
# 86 "data/maps/ColdStorageTest/scripts.pory"
	.string "{PLAYER} used the Storage Key.$"

ColdStorageTest_EventScript_Gate_Text_2:
# 93 "data/maps/ColdStorageTest/scripts.pory"
	.string "The gate rattled open!$"

ColdStorageTest_EventScript_Console_Text_0:
# 108 "data/maps/ColdStorageTest/scripts.pory"
	.string "COOLANT LINE B: OFF\p"
	.string "The centre aisle has thawed out. Switch\n"
	.string "the coolant back on?$"

ColdStorageTest_EventScript_Console_Text_1:
# 118 "data/maps/ColdStorageTest/scripts.pory"
	.string "The centre aisle froze over again.$"

ColdStorageTest_EventScript_Console_Text_2:
# 121 "data/maps/ColdStorageTest/scripts.pory"
	.string "COOLANT LINE B: ON\p"
	.string "It feeds the centre aisle. Switch the\n"
	.string "coolant off?$"

ColdStorageTest_EventScript_Console_Text_3:
# 131 "data/maps/ColdStorageTest/scripts.pory"
	.string "The ice in the centre aisle melted into\n"
	.string "puddles!$"

ColdStorageTest_EventScript_Grunt1_Text_0:
# 172 "data/maps/ColdStorageTest/scripts.pory"
	.string "The boss is at the back, behind the\n"
	.string "gate. Not that a kid could get it open.$"

ColdStorageTest_EventScript_Grunt2_Text_0:
# 178 "data/maps/ColdStorageTest/scripts.pory"
	.string "The next hall is one big sheet of ice.\n"
	.string "Somebody left the coolant running full\l"
	.string "blast.$"

ColdStorageTest_EventScript_Grunt3_Text_0:
# 184 "data/maps/ColdStorageTest/scripts.pory"
	.string "I dropped the Storage Key somewhere on\n"
	.string "the ice between the containers. Good\l"
	.string "luck reaching it.$"

ColdStorageTest_EventScript_Grunt4_Text_0:
# 190 "data/maps/ColdStorageTest/scripts.pory"
	.string "That console runs the coolant for the\n"
	.string "centre aisle. Don't touch it! …Ugh, why\l"
	.string "did I say that.$"

ColdStorageTest_EventScript_BossTrigger_Text_0:
# 233 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: {PLAYER}! You found a way in\n"
	.string "too!\p"
	.string "These two are packing Pokémon into\n"
	.string "freezer containers to ship them out of\l"
	.string "Tosa. I can't stop them alone!$"

ColdStorageTest_EventScript_BossTrigger_Text_1:
# 238 "data/maps/ColdStorageTest/scripts.pory"
	.string "Shelly: Boss, another brat got past the\n"
	.string "gate.$"

ColdStorageTest_EventScript_BossTrigger_Text_2:
# 239 "data/maps/ColdStorageTest/scripts.pory"
	.string "Archie: …Two children. How tiresome.\p"
	.string "This cargo leaves on tonight's tide.\n"
	.string "Stand aside, or be put on ice with it.$"

ColdStorageTest_EventScript_BossTrigger_Text_3:
# 240 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: Two of them, two of us. Battle\n"
	.string "with me, {PLAYER}!$"

ColdStorageTest_EventScript_WonMultiBattle_Text_0:
# 267 "data/maps/ColdStorageTest/scripts.pory"
	.string "Archie: …Hmph. A cold reception indeed.\p"
	.string "Keep the cargo, children. There are\n"
	.string "other ports.$"

ColdStorageTest_EventScript_WonMultiBattle_Text_1:
# 277 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: We did it! We make a pretty good\n"
	.string "team, {PLAYER}.\p"
	.string "I'll get these containers open. Let's\n"
	.string "warm everybody up.$"

ColdStorageTest_EventScript_Haru_Text_0:
# 287 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: Careful, {PLAYER}! They're right\n"
	.string "there!$"

ColdStorageTest_EventScript_Haru_Text_1:
# 289 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: I'll look after the Pokémon here.\n"
	.string "Thanks for the help, {PLAYER}!$"

ColdStorageTest_EventScript_Leader_Text_0:
# 296 "data/maps/ColdStorageTest/scripts.pory"
	.string "Archie: …$"

ColdStorageTest_EventScript_Admin_Text_0:
# 301 "data/maps/ColdStorageTest/scripts.pory"
	.string "Shelly: Hands off the cargo!$"

ColdStorageTest_Text_Grunt1Intro::
# 194 "data/maps/ColdStorageTest/scripts.pory"
	.string "Hey! This warehouse is closed for…\n"
	.string "stocktaking. Scram!$"

ColdStorageTest_Text_Grunt1Defeat::
# 198 "data/maps/ColdStorageTest/scripts.pory"
	.string "Brr… My Pokémon are too cold to fight.$"

ColdStorageTest_Text_Grunt2Intro::
# 202 "data/maps/ColdStorageTest/scripts.pory"
	.string "You slid all the way in here? Then I'll\n"
	.string "send you sliding right back out!$"

ColdStorageTest_Text_Grunt2Defeat::
# 206 "data/maps/ColdStorageTest/scripts.pory"
	.string "I slipped up…$"

ColdStorageTest_Text_Grunt3Intro::
# 210 "data/maps/ColdStorageTest/scripts.pory"
	.string "Nothing to see in this corner! Certainly\n"
	.string "nothing I lost!$"

ColdStorageTest_Text_Grunt3Defeat::
# 214 "data/maps/ColdStorageTest/scripts.pory"
	.string "Frozen solid…$"

ColdStorageTest_Text_Grunt4Intro::
# 218 "data/maps/ColdStorageTest/scripts.pory"
	.string "Halt! Nobody goes near the coolant\n"
	.string "console!$"

ColdStorageTest_Text_Grunt4Defeat::
# 222 "data/maps/ColdStorageTest/scripts.pory"
	.string "You've put me on ice…$"

ColdStorageTest_Text_HaruNoBackingOut::
# 305 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: We can't back out now, {PLAYER}!\n"
	.string "Pick your Pokémon!$"

ColdStorageTest_Text_LeaderDefeat::
# 309 "data/maps/ColdStorageTest/scripts.pory"
	.string "…So the ice cracks.$"

ColdStorageTest_Text_AdminDefeat::
# 313 "data/maps/ColdStorageTest/scripts.pory"
	.string "B-boss! These kids are tougher than\n"
	.string "they look!$"
