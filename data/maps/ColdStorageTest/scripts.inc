ColdStorageTest_MapScripts::
# 14 "data/maps/ColdStorageTest/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_TRANSITION
# 19 "data/maps/ColdStorageTest/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD
	.byte 0

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 15 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_COLD_STORAGE_STATE, 1
	goto_if_eq ColdStorageTest_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
	return

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 16 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_HIDE_COLD_STORAGE_HARU
	return

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD:
# 20 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_GATE_OPEN, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_2
ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_1:
# 23 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_THAWED, ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_4
	return

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_2:
# 21 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetGateOpen
	goto ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_1

ColdStorageTest_MapScripts_MAP_SCRIPT_ON_LOAD_4:
# 24 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetThawed
	return


ColdStorageTest_EventScript_TestAide::
# 32 "data/maps/ColdStorageTest/scripts.pory"
	lock
# 33 "data/maps/ColdStorageTest/scripts.pory"
	faceplayer
# 34 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_TestAide_Text_0, MSGBOX_YESNO
# 35 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, YES
	goto_if_eq ColdStorageTest_EventScript_TestAide_2
ColdStorageTest_EventScript_TestAide_1:
# 41 "data/maps/ColdStorageTest/scripts.pory"
	special HealPlayerParty
# 42 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_TestAide_Text_2
# 43 "data/maps/ColdStorageTest/scripts.pory"
	release
	end

ColdStorageTest_EventScript_TestAide_2:
# 36 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_GiveTestTeam
# 37 "data/maps/ColdStorageTest/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 38 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_TestAide_Text_1
# 39 "data/maps/ColdStorageTest/scripts.pory"
	waitfanfare
	goto ColdStorageTest_EventScript_TestAide_1


# 47 "data/maps/ColdStorageTest/scripts.pory"

# 48 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_GiveTestTeam::
# 49 "data/maps/ColdStorageTest/scripts.pory"
	callnative ZeroPlayerPartyMons
# 50 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_SERVINE, 30, ITEM_MIRACLE_SEED, move1=MOVE_MAGICAL_LEAF, move2=MOVE_MEGA_DRAIN, move3=MOVE_LEECH_SEED, move4=MOVE_SLAM
# 51 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_PIGNITE, 30, ITEM_CHARCOAL, move1=MOVE_ARM_THRUST, move2=MOVE_FLAME_CHARGE, move3=MOVE_EMBER, move4=MOVE_TAKE_DOWN
# 52 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_DEWOTT, 30, ITEM_MYSTIC_WATER, move1=MOVE_RAZOR_SHELL, move2=MOVE_WATER_PULSE, move3=MOVE_AERIAL_ACE, move4=MOVE_FURY_CUTTER
# 53 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_LUXIO, 30, ITEM_MAGNET, move1=MOVE_SPARK, move2=MOVE_BITE, move3=MOVE_THUNDER_SHOCK, move4=MOVE_CHARGE
# 54 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_STARAVIA, 30, ITEM_SHARP_BEAK, move1=MOVE_WING_ATTACK, move2=MOVE_AERIAL_ACE, move3=MOVE_QUICK_ATTACK, move4=MOVE_ENDEAVOR
# 55 "data/maps/ColdStorageTest/scripts.pory"
	givemon SPECIES_KIRLIA, 30, ITEM_TWISTED_SPOON, move1=MOVE_PSYBEAM, move2=MOVE_DRAINING_KISS, move3=MOVE_HYPNOSIS, move4=MOVE_LIFE_DEW
# 56 "data/maps/ColdStorageTest/scripts.pory"
	@ met at Lv. 5, so the team obeys even on a save with no badges
# 57 "data/maps/ColdStorageTest/scripts.pory"
	callnative Script_SetPartyMetLevel, requests_effects=1
# 58 "data/maps/ColdStorageTest/scripts.pory"
	.byte 5
# 59 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 60 "data/maps/ColdStorageTest/scripts.pory"
	return

ColdStorageTest_EventScript_ItemStorageKey::
# 66 "data/maps/ColdStorageTest/scripts.pory"
	finditem ITEM_STORAGE_KEY
	end


ColdStorageTest_EventScript_ItemNeverMeltIce::
# 71 "data/maps/ColdStorageTest/scripts.pory"
	finditem ITEM_NEVER_MELT_ICE
	end


ColdStorageTest_EventScript_ItemSuperPotion::
# 76 "data/maps/ColdStorageTest/scripts.pory"
	finditem ITEM_SUPER_POTION
	end


ColdStorageTest_EventScript_Gate::
# 83 "data/maps/ColdStorageTest/scripts.pory"
	lockall
# 84 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_GATE_OPEN, ColdStorageTest_EventScript_Gate_2
# 88 "data/maps/ColdStorageTest/scripts.pory"
	checkitem ITEM_STORAGE_KEY
# 89 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, FALSE
	goto_if_eq ColdStorageTest_EventScript_Gate_5
# 94 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Gate_Text_1
# 95 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 96 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_UNLOCK
# 97 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetGateOpen
# 98 "data/maps/ColdStorageTest/scripts.pory"
	special DrawWholeMapView
# 99 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_COLD_STORAGE_GATE_OPEN
# 100 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 101 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Gate_Text_2
# 102 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end

ColdStorageTest_EventScript_Gate_2:
# 85 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end

ColdStorageTest_EventScript_Gate_5:
# 90 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Gate_Text_0
# 91 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end


ColdStorageTest_EventScript_SetGateOpen::
# 107 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 8, METATILE_ColdStorage_Floor_Hazard, FALSE
	return


ColdStorageTest_EventScript_Console::
# 114 "data/maps/ColdStorageTest/scripts.pory"
	lockall
# 115 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_set FLAG_COLD_STORAGE_THAWED, ColdStorageTest_EventScript_Console_2
# 129 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_2, MSGBOX_YESNO
# 130 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, YES
	goto_if_eq ColdStorageTest_EventScript_Console_7
ColdStorageTest_EventScript_Console_1:
# 142 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end

ColdStorageTest_EventScript_Console_2:
# 116 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_0, MSGBOX_YESNO
# 117 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_RESULT, YES
	goto_if_eq ColdStorageTest_EventScript_Console_5
	goto ColdStorageTest_EventScript_Console_1

ColdStorageTest_EventScript_Console_5:
# 118 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 119 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_SWITCH
# 120 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 121 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetFrozen
# 122 "data/maps/ColdStorageTest/scripts.pory"
	special DrawWholeMapView
# 123 "data/maps/ColdStorageTest/scripts.pory"
	clearflag FLAG_COLD_STORAGE_THAWED
# 124 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_ICE_CRACK
# 125 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 126 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_1
	goto ColdStorageTest_EventScript_Console_1

ColdStorageTest_EventScript_Console_7:
# 131 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 132 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_SWITCH
# 133 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 134 "data/maps/ColdStorageTest/scripts.pory"
	call ColdStorageTest_EventScript_SetThawed
# 135 "data/maps/ColdStorageTest/scripts.pory"
	special DrawWholeMapView
# 136 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_COLD_STORAGE_THAWED
# 137 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_ICE_BREAK
# 138 "data/maps/ColdStorageTest/scripts.pory"
	waitse
# 139 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Console_Text_3
	goto ColdStorageTest_EventScript_Console_1


ColdStorageTest_EventScript_SetThawed::
# 147 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 10, METATILE_ColdStorage_Wet_ShadeW, FALSE
# 148 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 11, METATILE_ColdStorage_Wet_ShadeW, FALSE
# 149 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 8, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 150 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 9, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 151 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 12, METATILE_ColdStorage_Wet, FALSE
# 152 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 11, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 153 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 12, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 154 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 13, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 155 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 14, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 156 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 15, 12, METATILE_ColdStorage_Wet_ShadeN, FALSE
# 157 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 16, 11, METATILE_ColdStorage_Console_Off, TRUE
	return


ColdStorageTest_EventScript_SetFrozen::
# 162 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 10, METATILE_ColdStorage_Ice_ShadeW, FALSE
# 163 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 11, METATILE_ColdStorage_Ice_ShadeW, FALSE
# 164 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 8, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 165 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 9, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 166 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 10, 12, METATILE_ColdStorage_Ice, FALSE
# 167 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 11, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 168 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 12, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 169 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 13, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 170 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 14, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 171 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 15, 12, METATILE_ColdStorage_Ice_ShadeN, FALSE
# 172 "data/maps/ColdStorageTest/scripts.pory"
	setmetatile 16, 11, METATILE_ColdStorage_Console_On, TRUE
	return


ColdStorageTest_EventScript_Grunt1::
# 179 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_1, ColdStorageTest_Text_Grunt1Intro, ColdStorageTest_Text_Grunt1Defeat
# 180 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt1_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_Grunt2::
# 185 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_2, ColdStorageTest_Text_Grunt2Intro, ColdStorageTest_Text_Grunt2Defeat
# 186 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt2_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_Grunt3::
# 191 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_3, ColdStorageTest_Text_Grunt3Intro, ColdStorageTest_Text_Grunt3Defeat
# 192 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt3_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_Grunt4::
# 197 "data/maps/ColdStorageTest/scripts.pory"
	trainerbattle_single TRAINER_COLD_STORAGE_GRUNT_4, ColdStorageTest_Text_Grunt4Intro, ColdStorageTest_Text_Grunt4Defeat
# 198 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Grunt4_Text_0, MSGBOX_AUTOCLOSE
	end


ColdStorageTest_EventScript_BossTrigger::
# 237 "data/maps/ColdStorageTest/scripts.pory"
	lockall
# 238 "data/maps/ColdStorageTest/scripts.pory"
	playse SE_PIN
# 239 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_COLD_STORAGE_HARU, ColdStorageTest_EventScript_BossTrigger_Movement_0
# 240 "data/maps/ColdStorageTest/scripts.pory"
	waitmovement 0
# 241 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_0
# 242 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 243 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_PLAYER, ColdStorageTest_EventScript_BossTrigger_Movement_1
# 244 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_COLD_STORAGE_HARU, ColdStorageTest_EventScript_BossTrigger_Movement_2
# 245 "data/maps/ColdStorageTest/scripts.pory"
	waitmovement 0
# 246 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_1
# 247 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_2
# 248 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_BossTrigger_Text_3
# 249 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 250 "data/maps/ColdStorageTest/scripts.pory"
	goto ColdStorageTest_EventScript_ChoosePartyForMultiBattle
	return


# 253 "data/maps/ColdStorageTest/scripts.pory"

# 254 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_ChoosePartyForMultiBattle::
# 255 "data/maps/ColdStorageTest/scripts.pory"
	special SavePlayerParty
# 256 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_TO_BLACK
# 257 "data/maps/ColdStorageTest/scripts.pory"
	special ChooseHalfPartyForBattle
# 258 "data/maps/ColdStorageTest/scripts.pory"
	goto_if_ne VAR_RESULT, 0, ColdStorageTest_EventScript_DoMultiBattle
# 259 "data/maps/ColdStorageTest/scripts.pory"
	special LoadPlayerParty
# 260 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_Text_HaruNoBackingOut, MSGBOX_DEFAULT
# 261 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 262 "data/maps/ColdStorageTest/scripts.pory"
	goto ColdStorageTest_EventScript_ChoosePartyForMultiBattle
# 263 "data/maps/ColdStorageTest/scripts.pory"

# 264 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_DoMultiBattle::
# 265 "data/maps/ColdStorageTest/scripts.pory"
	multi_2_vs_2 TRAINER_COLD_STORAGE_LEADER, ColdStorageTest_Text_LeaderDefeat, TRAINER_COLD_STORAGE_ADMIN, ColdStorageTest_Text_AdminDefeat, PARTNER_HARU
# 266 "data/maps/ColdStorageTest/scripts.pory"
	switch VAR_RESULT
# 267 "data/maps/ColdStorageTest/scripts.pory"
	case 1, ColdStorageTest_EventScript_WonMultiBattle
# 268 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_TO_BLACK
# 269 "data/maps/ColdStorageTest/scripts.pory"
	special SetCB2WhiteOut
# 270 "data/maps/ColdStorageTest/scripts.pory"
	waitstate
# 271 "data/maps/ColdStorageTest/scripts.pory"
	end

ColdStorageTest_EventScript_WonMultiBattle::
# 275 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_WonMultiBattle_Text_0
# 276 "data/maps/ColdStorageTest/scripts.pory"
	closemessage
# 277 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_TO_BLACK
# 278 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_LEADER
# 279 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_ADMIN
# 280 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_HIDE_COLD_STORAGE_VILLAINS
# 282 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_GRUNT_1
# 283 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_GRUNT_2
# 284 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_GRUNT_3
# 285 "data/maps/ColdStorageTest/scripts.pory"
	removeobject LOCALID_COLD_STORAGE_GRUNT_4
# 286 "data/maps/ColdStorageTest/scripts.pory"
	setflag FLAG_HIDE_COLD_STORAGE_GRUNTS
# 287 "data/maps/ColdStorageTest/scripts.pory"
	setvar VAR_COLD_STORAGE_STATE, 1
# 288 "data/maps/ColdStorageTest/scripts.pory"
	fadescreen FADE_FROM_BLACK
# 289 "data/maps/ColdStorageTest/scripts.pory"
	applymovement LOCALID_COLD_STORAGE_HARU, ColdStorageTest_EventScript_WonMultiBattle_Movement_0
# 290 "data/maps/ColdStorageTest/scripts.pory"
	waitmovement 0
# 291 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_WonMultiBattle_Text_1
# 292 "data/maps/ColdStorageTest/scripts.pory"
	special HealPlayerParty
# 293 "data/maps/ColdStorageTest/scripts.pory"
	releaseall
	end


ColdStorageTest_EventScript_Haru::
# 298 "data/maps/ColdStorageTest/scripts.pory"
	lock
# 299 "data/maps/ColdStorageTest/scripts.pory"
	faceplayer
# 300 "data/maps/ColdStorageTest/scripts.pory"
	compare VAR_COLD_STORAGE_STATE, 0
	goto_if_eq ColdStorageTest_EventScript_Haru_2
# 303 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Haru_Text_1
ColdStorageTest_EventScript_Haru_1:
# 305 "data/maps/ColdStorageTest/scripts.pory"
	release
	end

ColdStorageTest_EventScript_Haru_2:
# 301 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Haru_Text_0
	goto ColdStorageTest_EventScript_Haru_1


ColdStorageTest_EventScript_Leader::
# 310 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Leader_Text_0, MSGBOX_NPC
	end


ColdStorageTest_EventScript_Admin::
# 315 "data/maps/ColdStorageTest/scripts.pory"
	msgbox ColdStorageTest_EventScript_Admin_Text_0, MSGBOX_NPC
	end


# 239 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_BossTrigger_Movement_0:
# 239 "data/maps/ColdStorageTest/scripts.pory"
	face_down
# 239 "data/maps/ColdStorageTest/scripts.pory"
	emote_exclamation_mark
# 239 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 239 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 239 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
	step_end

# 243 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_BossTrigger_Movement_1:
# 243 "data/maps/ColdStorageTest/scripts.pory"
	walk_up
# 243 "data/maps/ColdStorageTest/scripts.pory"
	walk_up
	step_end

# 244 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_BossTrigger_Movement_2:
# 244 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 244 "data/maps/ColdStorageTest/scripts.pory"
	delay_16
# 244 "data/maps/ColdStorageTest/scripts.pory"
	face_up
	step_end

# 289 "data/maps/ColdStorageTest/scripts.pory"
ColdStorageTest_EventScript_WonMultiBattle_Movement_0:
# 289 "data/maps/ColdStorageTest/scripts.pory"
	face_left
	step_end

ColdStorageTest_EventScript_TestAide_Text_0:
# 34 "data/maps/ColdStorageTest/scripts.pory"
	.string "I'm here for testing. I can swap your\n"
	.string "party for a Lv. 30 team that suits this\l"
	.string "place.\p"
	.string "Your current party would be released.\n"
	.string "Swap?$"

ColdStorageTest_EventScript_TestAide_Text_1:
# 38 "data/maps/ColdStorageTest/scripts.pory"
	.string "{PLAYER} received the test team!\p"
	.string "Servine, Pignite, Dewott, Luxio,\n"
	.string "Staravia and Kirlia.$"

ColdStorageTest_EventScript_TestAide_Text_2:
# 42 "data/maps/ColdStorageTest/scripts.pory"
	.string "Your Pokémon are fully healed.\p"
	.string "Talk to me again whenever you want them\n"
	.string "patched up.$"

ColdStorageTest_EventScript_Gate_Text_0:
# 90 "data/maps/ColdStorageTest/scripts.pory"
	.string "A heavy security gate. It's locked.\p"
	.string "The key must be somewhere in the\n"
	.string "warehouse.$"

ColdStorageTest_EventScript_Gate_Text_1:
# 94 "data/maps/ColdStorageTest/scripts.pory"
	.string "{PLAYER} used the Storage Key.$"

ColdStorageTest_EventScript_Gate_Text_2:
# 101 "data/maps/ColdStorageTest/scripts.pory"
	.string "The gate rattled open!$"

ColdStorageTest_EventScript_Console_Text_0:
# 116 "data/maps/ColdStorageTest/scripts.pory"
	.string "COOLANT LINE B: OFF\p"
	.string "The centre aisle has thawed out. Switch\n"
	.string "the coolant back on?$"

ColdStorageTest_EventScript_Console_Text_1:
# 126 "data/maps/ColdStorageTest/scripts.pory"
	.string "The centre aisle froze over again.$"

ColdStorageTest_EventScript_Console_Text_2:
# 129 "data/maps/ColdStorageTest/scripts.pory"
	.string "COOLANT LINE B: ON\p"
	.string "It feeds the centre aisle. Switch the\n"
	.string "coolant off?$"

ColdStorageTest_EventScript_Console_Text_3:
# 139 "data/maps/ColdStorageTest/scripts.pory"
	.string "The ice in the centre aisle melted into\n"
	.string "puddles!$"

ColdStorageTest_EventScript_Grunt1_Text_0:
# 180 "data/maps/ColdStorageTest/scripts.pory"
	.string "The boss is at the back, behind the\n"
	.string "gate. Not that a kid could get it open.$"

ColdStorageTest_EventScript_Grunt2_Text_0:
# 186 "data/maps/ColdStorageTest/scripts.pory"
	.string "The next hall is one big sheet of ice.\n"
	.string "Somebody left the coolant running full\l"
	.string "blast.$"

ColdStorageTest_EventScript_Grunt3_Text_0:
# 192 "data/maps/ColdStorageTest/scripts.pory"
	.string "I dropped the Storage Key somewhere on\n"
	.string "the ice between the containers. Good\l"
	.string "luck reaching it.$"

ColdStorageTest_EventScript_Grunt4_Text_0:
# 198 "data/maps/ColdStorageTest/scripts.pory"
	.string "That console runs the coolant for the\n"
	.string "centre aisle. Don't touch it! …Ugh, why\l"
	.string "did I say that.$"

ColdStorageTest_EventScript_BossTrigger_Text_0:
# 241 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: {PLAYER}! You found a way in\n"
	.string "too!\p"
	.string "These two are packing Pokémon into\n"
	.string "freezer containers to ship them out of\l"
	.string "Tosa. I can't stop them alone!$"

ColdStorageTest_EventScript_BossTrigger_Text_1:
# 246 "data/maps/ColdStorageTest/scripts.pory"
	.string "Shelly: Boss, another brat got past the\n"
	.string "gate.$"

ColdStorageTest_EventScript_BossTrigger_Text_2:
# 247 "data/maps/ColdStorageTest/scripts.pory"
	.string "Archie: …Two children. How tiresome.\p"
	.string "This cargo leaves on tonight's tide.\n"
	.string "Stand aside, or be put on ice with it.$"

ColdStorageTest_EventScript_BossTrigger_Text_3:
# 248 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: Two of them, two of us. Battle\n"
	.string "with me, {PLAYER}!$"

ColdStorageTest_EventScript_WonMultiBattle_Text_0:
# 275 "data/maps/ColdStorageTest/scripts.pory"
	.string "Archie: …Hmph. A cold reception indeed.\p"
	.string "Keep the cargo, children. There are\n"
	.string "other ports.$"

ColdStorageTest_EventScript_WonMultiBattle_Text_1:
# 291 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: We did it! We make a pretty good\n"
	.string "team, {PLAYER}.\p"
	.string "I'll get these containers open. Let's\n"
	.string "warm everybody up.$"

ColdStorageTest_EventScript_Haru_Text_0:
# 301 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: Careful, {PLAYER}! They're right\n"
	.string "there!$"

ColdStorageTest_EventScript_Haru_Text_1:
# 303 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: I'll look after the Pokémon here.\n"
	.string "Thanks for the help, {PLAYER}!$"

ColdStorageTest_EventScript_Leader_Text_0:
# 310 "data/maps/ColdStorageTest/scripts.pory"
	.string "Archie: …$"

ColdStorageTest_EventScript_Admin_Text_0:
# 315 "data/maps/ColdStorageTest/scripts.pory"
	.string "Shelly: Hands off the cargo!$"

ColdStorageTest_Text_Grunt1Intro::
# 202 "data/maps/ColdStorageTest/scripts.pory"
	.string "Hey! This warehouse is closed for…\n"
	.string "stocktaking. Scram!$"

ColdStorageTest_Text_Grunt1Defeat::
# 206 "data/maps/ColdStorageTest/scripts.pory"
	.string "Brr… My Pokémon are too cold to fight.$"

ColdStorageTest_Text_Grunt2Intro::
# 210 "data/maps/ColdStorageTest/scripts.pory"
	.string "You slid all the way in here? Then I'll\n"
	.string "send you sliding right back out!$"

ColdStorageTest_Text_Grunt2Defeat::
# 214 "data/maps/ColdStorageTest/scripts.pory"
	.string "I slipped up…$"

ColdStorageTest_Text_Grunt3Intro::
# 218 "data/maps/ColdStorageTest/scripts.pory"
	.string "Nothing to see in this corner! Certainly\n"
	.string "nothing I lost!$"

ColdStorageTest_Text_Grunt3Defeat::
# 222 "data/maps/ColdStorageTest/scripts.pory"
	.string "Frozen solid…$"

ColdStorageTest_Text_Grunt4Intro::
# 226 "data/maps/ColdStorageTest/scripts.pory"
	.string "Halt! Nobody goes near the coolant\n"
	.string "console!$"

ColdStorageTest_Text_Grunt4Defeat::
# 230 "data/maps/ColdStorageTest/scripts.pory"
	.string "You've put me on ice…$"

ColdStorageTest_Text_HaruNoBackingOut::
# 319 "data/maps/ColdStorageTest/scripts.pory"
	.string "Haru: We can't back out now, {PLAYER}!\n"
	.string "Pick your Pokémon!$"

ColdStorageTest_Text_LeaderDefeat::
# 323 "data/maps/ColdStorageTest/scripts.pory"
	.string "…So the ice cracks.$"

ColdStorageTest_Text_AdminDefeat::
# 327 "data/maps/ColdStorageTest/scripts.pory"
	.string "B-boss! These kids are tougher than\n"
	.string "they look!$"
