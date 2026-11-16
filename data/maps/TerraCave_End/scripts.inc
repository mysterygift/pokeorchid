# 1 "data/maps/TerraCave_End/scripts.pory"

# 2 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_MapScripts::
# 3 "data/maps/TerraCave_End/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, TerraCave_End_OnResume
# 4 "data/maps/TerraCave_End/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TerraCave_End_OnTransition
# 5 "data/maps/TerraCave_End/scripts.pory"
	.byte 0
# 6 "data/maps/TerraCave_End/scripts.pory"

# 7 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_OnResume:
# 8 "data/maps/TerraCave_End/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, TerraCave_End_EventScript_TryRemoveGroudon
# 9 "data/maps/TerraCave_End/scripts.pory"
	end
# 10 "data/maps/TerraCave_End/scripts.pory"

# 11 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_EventScript_TryRemoveGroudon::
# 12 "data/maps/TerraCave_End/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/TerraCave_End/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/TerraCave_End/scripts.pory"
	removeobject LOCALID_TERRA_CAVE_GROUDON
# 15 "data/maps/TerraCave_End/scripts.pory"
	return
# 16 "data/maps/TerraCave_End/scripts.pory"

# 17 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_OnTransition:
# 18 "data/maps/TerraCave_End/scripts.pory"
	call_if_unset FLAG_DEFEATED_GROUDON, TerraCave_End_EventScript_ShowGroudon
# 19 "data/maps/TerraCave_End/scripts.pory"
	end
# 20 "data/maps/TerraCave_End/scripts.pory"

# 21 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_EventScript_ShowGroudon::
# 22 "data/maps/TerraCave_End/scripts.pory"
	clearflag FLAG_HIDE_TERRA_CAVE_GROUDON
# 23 "data/maps/TerraCave_End/scripts.pory"
	setvar VAR_TEMP_1, 1
# 24 "data/maps/TerraCave_End/scripts.pory"
	return
# 25 "data/maps/TerraCave_End/scripts.pory"

# 26 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_EventScript_Groudon::
# 27 "data/maps/TerraCave_End/scripts.pory"
	lockall
# 28 "data/maps/TerraCave_End/scripts.pory"
	applymovement LOCALID_PLAYER, Common_Movement_FaceUp
# 29 "data/maps/TerraCave_End/scripts.pory"
	waitmovement 0
# 30 "data/maps/TerraCave_End/scripts.pory"
	applymovement LOCALID_TERRA_CAVE_GROUDON, TerraCave_End_Movement_GroudonApproach
# 31 "data/maps/TerraCave_End/scripts.pory"
	waitmovement 0
# 32 "data/maps/TerraCave_End/scripts.pory"
	waitse
# 33 "data/maps/TerraCave_End/scripts.pory"
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
# 34 "data/maps/TerraCave_End/scripts.pory"
	delay 40
# 35 "data/maps/TerraCave_End/scripts.pory"
	waitmoncry
# 36 "data/maps/TerraCave_End/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_TERRA_CAVE_GROUDON
# 37 "data/maps/TerraCave_End/scripts.pory"
	setwildbattle SPECIES_GROUDON, 70
# 38 "data/maps/TerraCave_End/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 39 "data/maps/TerraCave_End/scripts.pory"
	special BattleSetup_StartLegendaryBattle
# 40 "data/maps/TerraCave_End/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 41 "data/maps/TerraCave_End/scripts.pory"
	setvar VAR_TEMP_1, 0
# 42 "data/maps/TerraCave_End/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 43 "data/maps/TerraCave_End/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, TerraCave_End_EventScript_DefeatedGroudon
# 44 "data/maps/TerraCave_End/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, TerraCave_End_EventScript_RanFromGroudon
# 45 "data/maps/TerraCave_End/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, TerraCave_End_EventScript_RanFromGroudon
# 46 "data/maps/TerraCave_End/scripts.pory"
	setvar VAR_SHOULD_END_ABNORMAL_WEATHER, 1
# 47 "data/maps/TerraCave_End/scripts.pory"
	setflag FLAG_DEFEATED_GROUDON
# 48 "data/maps/TerraCave_End/scripts.pory"
	releaseall
# 49 "data/maps/TerraCave_End/scripts.pory"
	end
# 50 "data/maps/TerraCave_End/scripts.pory"

# 51 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_EventScript_DefeatedGroudon::
# 52 "data/maps/TerraCave_End/scripts.pory"
	setvar VAR_SHOULD_END_ABNORMAL_WEATHER, 1
# 53 "data/maps/TerraCave_End/scripts.pory"
	setflag FLAG_DEFEATED_GROUDON
# 54 "data/maps/TerraCave_End/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 55 "data/maps/TerraCave_End/scripts.pory"
	end
# 56 "data/maps/TerraCave_End/scripts.pory"

# 57 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_EventScript_RanFromGroudon::
# 58 "data/maps/TerraCave_End/scripts.pory"
	setvar VAR_0x8004, SPECIES_GROUDON
# 59 "data/maps/TerraCave_End/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 60 "data/maps/TerraCave_End/scripts.pory"
	end
# 61 "data/maps/TerraCave_End/scripts.pory"

# 62 "data/maps/TerraCave_End/scripts.pory"
TerraCave_End_Movement_GroudonApproach:
# 63 "data/maps/TerraCave_End/scripts.pory"
	init_affine_anim
# 64 "data/maps/TerraCave_End/scripts.pory"
	walk_down_start_affine
# 65 "data/maps/TerraCave_End/scripts.pory"
	delay_16
# 66 "data/maps/TerraCave_End/scripts.pory"
	delay_16
# 67 "data/maps/TerraCave_End/scripts.pory"
	walk_down_affine
# 68 "data/maps/TerraCave_End/scripts.pory"
	delay_16
# 69 "data/maps/TerraCave_End/scripts.pory"
	delay_16
# 70 "data/maps/TerraCave_End/scripts.pory"
	walk_down_affine
# 71 "data/maps/TerraCave_End/scripts.pory"
	step_end
