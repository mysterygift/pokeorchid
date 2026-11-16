# 1 "data/maps/MarineCave_End/scripts.pory"

# 2 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_MapScripts::
# 3 "data/maps/MarineCave_End/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, MarineCave_End_OnResume
# 4 "data/maps/MarineCave_End/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, MarineCave_End_OnTransition
# 5 "data/maps/MarineCave_End/scripts.pory"
	.byte 0
# 6 "data/maps/MarineCave_End/scripts.pory"

# 7 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_OnResume:
# 8 "data/maps/MarineCave_End/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, MarineCave_End_EventScript_TryRemoveKyogre
# 9 "data/maps/MarineCave_End/scripts.pory"
	end
# 10 "data/maps/MarineCave_End/scripts.pory"

# 11 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_EventScript_TryRemoveKyogre::
# 12 "data/maps/MarineCave_End/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/MarineCave_End/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/MarineCave_End/scripts.pory"
	removeobject LOCALID_MARINE_CAVE_KYOGRE
# 15 "data/maps/MarineCave_End/scripts.pory"
	return
# 16 "data/maps/MarineCave_End/scripts.pory"

# 17 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_OnTransition:
# 18 "data/maps/MarineCave_End/scripts.pory"
	call_if_unset FLAG_DEFEATED_KYOGRE, MarineCave_End_EventScript_ShowKyogre
# 19 "data/maps/MarineCave_End/scripts.pory"
	end
# 20 "data/maps/MarineCave_End/scripts.pory"

# 21 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_EventScript_ShowKyogre::
# 22 "data/maps/MarineCave_End/scripts.pory"
	clearflag FLAG_HIDE_MARINE_CAVE_KYOGRE
# 23 "data/maps/MarineCave_End/scripts.pory"
	setvar VAR_TEMP_1, 1
# 24 "data/maps/MarineCave_End/scripts.pory"
	return
# 25 "data/maps/MarineCave_End/scripts.pory"

# 26 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_EventScript_Kyogre::
# 27 "data/maps/MarineCave_End/scripts.pory"
	lockall
# 28 "data/maps/MarineCave_End/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
# 29 "data/maps/MarineCave_End/scripts.pory"
	waitmovement 0
# 30 "data/maps/MarineCave_End/scripts.pory"
	applymovement LOCALID_MARINE_CAVE_KYOGRE, MarineCave_End_Movement_KyogreApproach
# 31 "data/maps/MarineCave_End/scripts.pory"
	waitmovement 0
# 32 "data/maps/MarineCave_End/scripts.pory"
	waitse
# 33 "data/maps/MarineCave_End/scripts.pory"
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
# 34 "data/maps/MarineCave_End/scripts.pory"
	delay 40
# 35 "data/maps/MarineCave_End/scripts.pory"
	waitmoncry
# 36 "data/maps/MarineCave_End/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_MARINE_CAVE_KYOGRE
# 37 "data/maps/MarineCave_End/scripts.pory"
	setwildbattle SPECIES_KYOGRE, 70
# 38 "data/maps/MarineCave_End/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 39 "data/maps/MarineCave_End/scripts.pory"
	special BattleSetup_StartLegendaryBattle
# 40 "data/maps/MarineCave_End/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 41 "data/maps/MarineCave_End/scripts.pory"
	setvar VAR_TEMP_1, 0
# 42 "data/maps/MarineCave_End/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 43 "data/maps/MarineCave_End/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MarineCave_End_EventScript_DefeatedKyogre
# 44 "data/maps/MarineCave_End/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MarineCave_End_EventScript_RanFromKyogre
# 45 "data/maps/MarineCave_End/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MarineCave_End_EventScript_RanFromKyogre
# 46 "data/maps/MarineCave_End/scripts.pory"
	setvar VAR_SHOULD_END_ABNORMAL_WEATHER, 1
# 47 "data/maps/MarineCave_End/scripts.pory"
	setflag FLAG_DEFEATED_KYOGRE
# 48 "data/maps/MarineCave_End/scripts.pory"
	releaseall
# 49 "data/maps/MarineCave_End/scripts.pory"
	end
# 50 "data/maps/MarineCave_End/scripts.pory"

# 51 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_EventScript_DefeatedKyogre::
# 52 "data/maps/MarineCave_End/scripts.pory"
	setvar VAR_SHOULD_END_ABNORMAL_WEATHER, 1
# 53 "data/maps/MarineCave_End/scripts.pory"
	setflag FLAG_DEFEATED_KYOGRE
# 54 "data/maps/MarineCave_End/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 55 "data/maps/MarineCave_End/scripts.pory"
	end
# 56 "data/maps/MarineCave_End/scripts.pory"

# 57 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_EventScript_RanFromKyogre::
# 58 "data/maps/MarineCave_End/scripts.pory"
	setvar VAR_0x8004, SPECIES_KYOGRE
# 59 "data/maps/MarineCave_End/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 60 "data/maps/MarineCave_End/scripts.pory"
	end
# 61 "data/maps/MarineCave_End/scripts.pory"

# 62 "data/maps/MarineCave_End/scripts.pory"
MarineCave_End_Movement_KyogreApproach:
# 63 "data/maps/MarineCave_End/scripts.pory"
	init_affine_anim
# 64 "data/maps/MarineCave_End/scripts.pory"
	walk_down_start_affine
# 65 "data/maps/MarineCave_End/scripts.pory"
	delay_16
# 66 "data/maps/MarineCave_End/scripts.pory"
	delay_16
# 67 "data/maps/MarineCave_End/scripts.pory"
	walk_down_affine
# 68 "data/maps/MarineCave_End/scripts.pory"
	delay_16
# 69 "data/maps/MarineCave_End/scripts.pory"
	delay_16
# 70 "data/maps/MarineCave_End/scripts.pory"
	walk_down_affine
# 71 "data/maps/MarineCave_End/scripts.pory"
	step_end
