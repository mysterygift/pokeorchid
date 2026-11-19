# 1 "data/maps/MtDrakeSummit/scripts.pory"

# 2 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_MapScripts::
# 3 "data/maps/MtDrakeSummit/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, MtDrakeSummit_OnResume
# 4 "data/maps/MtDrakeSummit/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, MtDrakeSummit_OnTransition
# 5 "data/maps/MtDrakeSummit/scripts.pory"
	.byte 0
# 6 "data/maps/MtDrakeSummit/scripts.pory"

# 7 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_OnResume:
# 8 "data/maps/MtDrakeSummit/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, MtDrakeSummit_EventScript_TryRemoveRegi
# 9 "data/maps/MtDrakeSummit/scripts.pory"
	end
# 10 "data/maps/MtDrakeSummit/scripts.pory"

# 11 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_EventScript_TryRemoveRegi::
# 12 "data/maps/MtDrakeSummit/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/MtDrakeSummit/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/MtDrakeSummit/scripts.pory"
	removeobject VAR_LAST_TALKED
# 15 "data/maps/MtDrakeSummit/scripts.pory"
	return
# 16 "data/maps/MtDrakeSummit/scripts.pory"

# 17 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_OnTransition:
# 18 "data/maps/MtDrakeSummit/scripts.pory"
	call_if_unset FLAG_DEFEATED_REGIDRAGO, MtDrakeSummit_EventScript_ShowRegi
# 19 "data/maps/MtDrakeSummit/scripts.pory"
	end
# 20 "data/maps/MtDrakeSummit/scripts.pory"

# 21 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_EventScript_ShowRegi::
# 22 "data/maps/MtDrakeSummit/scripts.pory"
	clearflag FLAG_HIDE_REGIDRAGO
# 23 "data/maps/MtDrakeSummit/scripts.pory"
	return
# 24 "data/maps/MtDrakeSummit/scripts.pory"

# 25 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_EventScript_Regi::
# 26 "data/maps/MtDrakeSummit/scripts.pory"
	lock
# 27 "data/maps/MtDrakeSummit/scripts.pory"
	faceplayer
# 28 "data/maps/MtDrakeSummit/scripts.pory"
	waitse
# 29 "data/maps/MtDrakeSummit/scripts.pory"
	playmoncry SPECIES_REGIDRAGO, CRY_MODE_ENCOUNTER
# 30 "data/maps/MtDrakeSummit/scripts.pory"
	delay 40
# 31 "data/maps/MtDrakeSummit/scripts.pory"
	waitmoncry
# 32 "data/maps/MtDrakeSummit/scripts.pory"
	setwildbattle SPECIES_REGIDRAGO, 40
# 33 "data/maps/MtDrakeSummit/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 34 "data/maps/MtDrakeSummit/scripts.pory"
	special StartRegiBattle
# 35 "data/maps/MtDrakeSummit/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 36 "data/maps/MtDrakeSummit/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 37 "data/maps/MtDrakeSummit/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MtDrakeSummit_EventScript_DefeatedRegi
# 38 "data/maps/MtDrakeSummit/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtDrakeSummit_EventScript_RanFromRegi
# 39 "data/maps/MtDrakeSummit/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtDrakeSummit_EventScript_RanFromRegi
# 40 "data/maps/MtDrakeSummit/scripts.pory"
	setflag FLAG_DEFEATED_REGIDRAGO
# 41 "data/maps/MtDrakeSummit/scripts.pory"
	release
# 42 "data/maps/MtDrakeSummit/scripts.pory"
	end
# 43 "data/maps/MtDrakeSummit/scripts.pory"

# 44 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_EventScript_DefeatedRegi::
# 45 "data/maps/MtDrakeSummit/scripts.pory"
	setflag FLAG_DEFEATED_REGIDRAGO
# 46 "data/maps/MtDrakeSummit/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 47 "data/maps/MtDrakeSummit/scripts.pory"
	end
# 48 "data/maps/MtDrakeSummit/scripts.pory"

# 49 "data/maps/MtDrakeSummit/scripts.pory"
MtDrakeSummit_EventScript_RanFromRegi::
# 50 "data/maps/MtDrakeSummit/scripts.pory"
	setvar VAR_0x8004, SPECIES_REGIDRAGO
# 51 "data/maps/MtDrakeSummit/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 52 "data/maps/MtDrakeSummit/scripts.pory"
	end
