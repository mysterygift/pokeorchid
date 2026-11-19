# 1 "data/maps/GavaniPath/scripts.pory"

# 2 "data/maps/GavaniPath/scripts.pory"
GavaniPath_MapScripts::
# 3 "data/maps/GavaniPath/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, GavaniPath_OnResume
# 4 "data/maps/GavaniPath/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, GavaniPath_OnTransition
# 5 "data/maps/GavaniPath/scripts.pory"
	.byte 0
# 6 "data/maps/GavaniPath/scripts.pory"

# 7 "data/maps/GavaniPath/scripts.pory"
GavaniPath_OnResume:
# 8 "data/maps/GavaniPath/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, GavaniPath_EventScript_TryRemoveRegi
# 9 "data/maps/GavaniPath/scripts.pory"
	end
# 10 "data/maps/GavaniPath/scripts.pory"

# 11 "data/maps/GavaniPath/scripts.pory"
GavaniPath_EventScript_TryRemoveRegi::
# 12 "data/maps/GavaniPath/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/GavaniPath/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/GavaniPath/scripts.pory"
	removeobject VAR_LAST_TALKED
# 15 "data/maps/GavaniPath/scripts.pory"
	return
# 16 "data/maps/GavaniPath/scripts.pory"

# 17 "data/maps/GavaniPath/scripts.pory"
GavaniPath_OnTransition:
# 18 "data/maps/GavaniPath/scripts.pory"
	call_if_unset FLAG_DEFEATED_REGIELEKI, GavaniPath_EventScript_ShowRegi
# 19 "data/maps/GavaniPath/scripts.pory"
	end
# 20 "data/maps/GavaniPath/scripts.pory"

# 21 "data/maps/GavaniPath/scripts.pory"
GavaniPath_EventScript_ShowRegi::
# 22 "data/maps/GavaniPath/scripts.pory"
	clearflag FLAG_HIDE_REGIELEKI
# 23 "data/maps/GavaniPath/scripts.pory"
	return
# 24 "data/maps/GavaniPath/scripts.pory"

# 25 "data/maps/GavaniPath/scripts.pory"
GavaniPath_EventScript_Regi::
# 26 "data/maps/GavaniPath/scripts.pory"
	lock
# 27 "data/maps/GavaniPath/scripts.pory"
	faceplayer
# 28 "data/maps/GavaniPath/scripts.pory"
	waitse
# 29 "data/maps/GavaniPath/scripts.pory"
	playmoncry SPECIES_REGIELEKI, CRY_MODE_ENCOUNTER
# 30 "data/maps/GavaniPath/scripts.pory"
	delay 40
# 31 "data/maps/GavaniPath/scripts.pory"
	waitmoncry
# 32 "data/maps/GavaniPath/scripts.pory"
	setwildbattle SPECIES_REGIELEKI, 40
# 33 "data/maps/GavaniPath/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 34 "data/maps/GavaniPath/scripts.pory"
	special StartRegiBattle
# 35 "data/maps/GavaniPath/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 36 "data/maps/GavaniPath/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 37 "data/maps/GavaniPath/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, GavaniPath_EventScript_DefeatedRegi
# 38 "data/maps/GavaniPath/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, GavaniPath_EventScript_RanFromRegi
# 39 "data/maps/GavaniPath/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, GavaniPath_EventScript_RanFromRegi
# 40 "data/maps/GavaniPath/scripts.pory"
	setflag FLAG_DEFEATED_REGIELEKI
# 41 "data/maps/GavaniPath/scripts.pory"
	release
# 42 "data/maps/GavaniPath/scripts.pory"
	end
# 43 "data/maps/GavaniPath/scripts.pory"

# 44 "data/maps/GavaniPath/scripts.pory"
GavaniPath_EventScript_DefeatedRegi::
# 45 "data/maps/GavaniPath/scripts.pory"
	setflag FLAG_DEFEATED_REGIELEKI
# 46 "data/maps/GavaniPath/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 47 "data/maps/GavaniPath/scripts.pory"
	end
# 48 "data/maps/GavaniPath/scripts.pory"

# 49 "data/maps/GavaniPath/scripts.pory"
GavaniPath_EventScript_RanFromRegi::
# 50 "data/maps/GavaniPath/scripts.pory"
	setvar VAR_0x8004, SPECIES_REGIELEKI
# 51 "data/maps/GavaniPath/scripts.pory"
	goto Common_EventScript_LegendaryFlewAway
# 52 "data/maps/GavaniPath/scripts.pory"
	end
