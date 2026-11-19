# 1 "data/maps/RegolisShrine/scripts.pory"

# 2 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_MapScripts::
# 3 "data/maps/RegolisShrine/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, RegolisShrine_OnResume
# 4 "data/maps/RegolisShrine/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, RegolisShrine_OnTransition
# 5 "data/maps/RegolisShrine/scripts.pory"
	.byte 0
# 6 "data/maps/RegolisShrine/scripts.pory"

# 7 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_OnResume:
# 8 "data/maps/RegolisShrine/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, RegolisShrine_EventScript_TryRemoveRegi
# 9 "data/maps/RegolisShrine/scripts.pory"
	end
# 10 "data/maps/RegolisShrine/scripts.pory"

# 11 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_EventScript_TryRemoveRegi::
# 12 "data/maps/RegolisShrine/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/RegolisShrine/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/RegolisShrine/scripts.pory"
	removeobject VAR_LAST_TALKED
# 15 "data/maps/RegolisShrine/scripts.pory"
	return
# 16 "data/maps/RegolisShrine/scripts.pory"

# 17 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_OnTransition:
# 18 "data/maps/RegolisShrine/scripts.pory"
	call_if_unset FLAG_DEFEATED_REGIROCK, RegolisShrine_EventScript_ShowRegi
# 19 "data/maps/RegolisShrine/scripts.pory"
	end
# 20 "data/maps/RegolisShrine/scripts.pory"

# 21 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_EventScript_ShowRegi::
# 22 "data/maps/RegolisShrine/scripts.pory"
	clearflag FLAG_HIDE_REGIROCK
# 23 "data/maps/RegolisShrine/scripts.pory"
	return
# 24 "data/maps/RegolisShrine/scripts.pory"

# 25 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_EventScript_Regi::
# 26 "data/maps/RegolisShrine/scripts.pory"
	lock
# 27 "data/maps/RegolisShrine/scripts.pory"
	faceplayer
# 28 "data/maps/RegolisShrine/scripts.pory"
	waitse
# 29 "data/maps/RegolisShrine/scripts.pory"
	playmoncry SPECIES_REGIROCK, CRY_MODE_ENCOUNTER
# 30 "data/maps/RegolisShrine/scripts.pory"
	delay 40
# 31 "data/maps/RegolisShrine/scripts.pory"
	waitmoncry
# 32 "data/maps/RegolisShrine/scripts.pory"
	setwildbattle SPECIES_REGIROCK, 40
# 33 "data/maps/RegolisShrine/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 34 "data/maps/RegolisShrine/scripts.pory"
	special StartRegiBattle
# 35 "data/maps/RegolisShrine/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 36 "data/maps/RegolisShrine/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 37 "data/maps/RegolisShrine/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, RegolisShrine_EventScript_DefeatedRegi
# 38 "data/maps/RegolisShrine/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, RegolisShrine_EventScript_RanFromRegi
# 39 "data/maps/RegolisShrine/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, RegolisShrine_EventScript_RanFromRegi
# 40 "data/maps/RegolisShrine/scripts.pory"
	setflag FLAG_DEFEATED_REGIROCK
# 41 "data/maps/RegolisShrine/scripts.pory"
	release
# 42 "data/maps/RegolisShrine/scripts.pory"
	end
# 43 "data/maps/RegolisShrine/scripts.pory"

# 44 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_EventScript_DefeatedRegi::
# 45 "data/maps/RegolisShrine/scripts.pory"
	setflag FLAG_DEFEATED_REGIROCK
# 46 "data/maps/RegolisShrine/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 47 "data/maps/RegolisShrine/scripts.pory"
	end
# 48 "data/maps/RegolisShrine/scripts.pory"

# 49 "data/maps/RegolisShrine/scripts.pory"
RegolisShrine_EventScript_RanFromRegi::
# 50 "data/maps/RegolisShrine/scripts.pory"
	setvar VAR_0x8004, SPECIES_REGIROCK
# 51 "data/maps/RegolisShrine/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 52 "data/maps/RegolisShrine/scripts.pory"
	end
