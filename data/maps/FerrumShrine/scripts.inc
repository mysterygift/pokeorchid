# 1 "data/maps/FerrumShrine/scripts.pory"

# 2 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_MapScripts::
# 3 "data/maps/FerrumShrine/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, FerrumShrine_OnResume
# 4 "data/maps/FerrumShrine/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, FerrumShrine_OnTransition
# 5 "data/maps/FerrumShrine/scripts.pory"
	.byte 0
# 6 "data/maps/FerrumShrine/scripts.pory"

# 7 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_OnResume:
# 8 "data/maps/FerrumShrine/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, FerrumShrine_EventScript_TryRemoveRegi
# 9 "data/maps/FerrumShrine/scripts.pory"
	end
# 10 "data/maps/FerrumShrine/scripts.pory"

# 11 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_EventScript_TryRemoveRegi::
# 12 "data/maps/FerrumShrine/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/FerrumShrine/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/FerrumShrine/scripts.pory"
	removeobject VAR_LAST_TALKED
# 15 "data/maps/FerrumShrine/scripts.pory"
	return
# 16 "data/maps/FerrumShrine/scripts.pory"

# 17 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_OnTransition:
# 18 "data/maps/FerrumShrine/scripts.pory"
	call_if_unset FLAG_DEFEATED_REGISTEEL, FerrumShrine_EventScript_ShowRegi
# 19 "data/maps/FerrumShrine/scripts.pory"
	end
# 20 "data/maps/FerrumShrine/scripts.pory"

# 21 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_EventScript_ShowRegi::
# 22 "data/maps/FerrumShrine/scripts.pory"
	clearflag FLAG_HIDE_REGISTEEL
# 23 "data/maps/FerrumShrine/scripts.pory"
	return
# 24 "data/maps/FerrumShrine/scripts.pory"

# 25 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_EventScript_Regi::
# 26 "data/maps/FerrumShrine/scripts.pory"
	lock
# 27 "data/maps/FerrumShrine/scripts.pory"
	faceplayer
# 28 "data/maps/FerrumShrine/scripts.pory"
	waitse
# 29 "data/maps/FerrumShrine/scripts.pory"
	playmoncry SPECIES_REGISTEEL, CRY_MODE_ENCOUNTER
# 30 "data/maps/FerrumShrine/scripts.pory"
	delay 40
# 31 "data/maps/FerrumShrine/scripts.pory"
	waitmoncry
# 32 "data/maps/FerrumShrine/scripts.pory"
	setwildbattle SPECIES_REGISTEEL, 40
# 33 "data/maps/FerrumShrine/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 34 "data/maps/FerrumShrine/scripts.pory"
	special StartRegiBattle
# 35 "data/maps/FerrumShrine/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 36 "data/maps/FerrumShrine/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 37 "data/maps/FerrumShrine/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, FerrumShrine_EventScript_DefeatedRegi
# 38 "data/maps/FerrumShrine/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, FerrumShrine_EventScript_RanFromRegi
# 39 "data/maps/FerrumShrine/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, FerrumShrine_EventScript_RanFromRegi
# 40 "data/maps/FerrumShrine/scripts.pory"
	setflag FLAG_DEFEATED_REGISTEEL
# 41 "data/maps/FerrumShrine/scripts.pory"
	release
# 42 "data/maps/FerrumShrine/scripts.pory"
	end
# 43 "data/maps/FerrumShrine/scripts.pory"

# 44 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_EventScript_DefeatedRegi::
# 45 "data/maps/FerrumShrine/scripts.pory"
	setflag FLAG_DEFEATED_REGISTEEL
# 46 "data/maps/FerrumShrine/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 47 "data/maps/FerrumShrine/scripts.pory"
	end
# 48 "data/maps/FerrumShrine/scripts.pory"

# 49 "data/maps/FerrumShrine/scripts.pory"
FerrumShrine_EventScript_RanFromRegi::
# 50 "data/maps/FerrumShrine/scripts.pory"
	setvar VAR_0x8004, SPECIES_REGISTEEL
# 51 "data/maps/FerrumShrine/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 52 "data/maps/FerrumShrine/scripts.pory"
	end
