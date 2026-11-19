# 1 "data/maps/FrigoCave/scripts.pory"

# 2 "data/maps/FrigoCave/scripts.pory"
FrigoCave_MapScripts::
# 3 "data/maps/FrigoCave/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, FrigoCave_OnResume
# 4 "data/maps/FrigoCave/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FrigoCave_OnTransition
# 5 "data/maps/FrigoCave/scripts.pory"
	.byte 0
# 6 "data/maps/FrigoCave/scripts.pory"

# 7 "data/maps/FrigoCave/scripts.pory"
FrigoCave_OnResume:
# 8 "data/maps/FrigoCave/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, FrigoCave_EventScript_TryRemoveRegi
# 9 "data/maps/FrigoCave/scripts.pory"
	end
# 10 "data/maps/FrigoCave/scripts.pory"

# 11 "data/maps/FrigoCave/scripts.pory"
FrigoCave_EventScript_TryRemoveRegi::
# 12 "data/maps/FrigoCave/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/FrigoCave/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/FrigoCave/scripts.pory"
	removeobject VAR_LAST_TALKED
# 15 "data/maps/FrigoCave/scripts.pory"
	return
# 16 "data/maps/FrigoCave/scripts.pory"

# 17 "data/maps/FrigoCave/scripts.pory"
FrigoCave_OnTransition:
# 18 "data/maps/FrigoCave/scripts.pory"
	call_if_unset FLAG_DEFEATED_REGICE, FrigoCave_EventScript_ShowRegi
# 19 "data/maps/FrigoCave/scripts.pory"
	end
# 20 "data/maps/FrigoCave/scripts.pory"

# 21 "data/maps/FrigoCave/scripts.pory"
FrigoCave_EventScript_ShowRegi::
# 22 "data/maps/FrigoCave/scripts.pory"
	clearflag FLAG_HIDE_REGICE
# 23 "data/maps/FrigoCave/scripts.pory"
	return
# 24 "data/maps/FrigoCave/scripts.pory"

# 25 "data/maps/FrigoCave/scripts.pory"
FrigoCave_EventScript_Regi::
# 26 "data/maps/FrigoCave/scripts.pory"
	lock
# 27 "data/maps/FrigoCave/scripts.pory"
	faceplayer
# 28 "data/maps/FrigoCave/scripts.pory"
	waitse
# 29 "data/maps/FrigoCave/scripts.pory"
	playmoncry SPECIES_REGICE, CRY_MODE_ENCOUNTER
# 30 "data/maps/FrigoCave/scripts.pory"
	delay 40
# 31 "data/maps/FrigoCave/scripts.pory"
	waitmoncry
# 32 "data/maps/FrigoCave/scripts.pory"
	setwildbattle SPECIES_REGICE, 40
# 33 "data/maps/FrigoCave/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 34 "data/maps/FrigoCave/scripts.pory"
	special StartRegiBattle
# 35 "data/maps/FrigoCave/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 36 "data/maps/FrigoCave/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 37 "data/maps/FrigoCave/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, FrigoCave_EventScript_DefeatedRegi
# 38 "data/maps/FrigoCave/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, FrigoCave_EventScript_RanFromRegi
# 39 "data/maps/FrigoCave/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, FrigoCave_EventScript_RanFromRegi
# 40 "data/maps/FrigoCave/scripts.pory"
	setflag FLAG_DEFEATED_REGICE
# 41 "data/maps/FrigoCave/scripts.pory"
	release
# 42 "data/maps/FrigoCave/scripts.pory"
	end
# 43 "data/maps/FrigoCave/scripts.pory"

# 44 "data/maps/FrigoCave/scripts.pory"
FrigoCave_EventScript_DefeatedRegi::
# 45 "data/maps/FrigoCave/scripts.pory"
	setflag FLAG_DEFEATED_REGICE
# 46 "data/maps/FrigoCave/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 47 "data/maps/FrigoCave/scripts.pory"
	end
# 48 "data/maps/FrigoCave/scripts.pory"

# 49 "data/maps/FrigoCave/scripts.pory"
FrigoCave_EventScript_RanFromRegi::
# 50 "data/maps/FrigoCave/scripts.pory"
	setvar VAR_0x8004, SPECIES_REGICE
# 51 "data/maps/FrigoCave/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 52 "data/maps/FrigoCave/scripts.pory"
	end
