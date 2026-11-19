# 1 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 2 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_MapScripts::
# 3 "data/maps/NewmoonIsland_Interior/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, NewmoonIsland_Interior_OnResume
# 4 "data/maps/NewmoonIsland_Interior/scripts.pory"
	.byte 0
# 5 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 6 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_OnResume:
# 7 "data/maps/NewmoonIsland_Interior/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, NewmoonIsland_Interior_EventScript_TryRemoveDarkrai
# 8 "data/maps/NewmoonIsland_Interior/scripts.pory"
	end
# 9 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 10 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_EventScript_TryRemoveDarkrai::
# 11 "data/maps/NewmoonIsland_Interior/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 12 "data/maps/NewmoonIsland_Interior/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 13 "data/maps/NewmoonIsland_Interior/scripts.pory"
	removeobject LOCALID_NEWMOON_DARKRAI
# 14 "data/maps/NewmoonIsland_Interior/scripts.pory"
	return
# 15 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 16 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_EventScript_Darkrai::
# 17 "data/maps/NewmoonIsland_Interior/scripts.pory"
	lock
# 18 "data/maps/NewmoonIsland_Interior/scripts.pory"
	faceplayer
# 19 "data/maps/NewmoonIsland_Interior/scripts.pory"
	waitse
# 20 "data/maps/NewmoonIsland_Interior/scripts.pory"
	playmoncry SPECIES_DARKRAI, CRY_MODE_ENCOUNTER
# 21 "data/maps/NewmoonIsland_Interior/scripts.pory"
	delay 40
# 22 "data/maps/NewmoonIsland_Interior/scripts.pory"
	waitmoncry
# 23 "data/maps/NewmoonIsland_Interior/scripts.pory"
	setwildbattle SPECIES_DARKRAI, VOYAGE_LEGENDARY_LEVEL
# 24 "data/maps/NewmoonIsland_Interior/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 25 "data/maps/NewmoonIsland_Interior/scripts.pory"
	special BattleSetup_StartLegendaryBattle
# 26 "data/maps/NewmoonIsland_Interior/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 27 "data/maps/NewmoonIsland_Interior/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 28 "data/maps/NewmoonIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, NewmoonIsland_Interior_EventScript_DarkraiGone
# 29 "data/maps/NewmoonIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, NewmoonIsland_Interior_EventScript_DarkraiGone
# 30 "data/maps/NewmoonIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, NewmoonIsland_Interior_EventScript_DarkraiGone
# 31 "data/maps/NewmoonIsland_Interior/scripts.pory"
	setflag FLAG_CAUGHT_VOYAGE_DARKRAI
# 32 "data/maps/NewmoonIsland_Interior/scripts.pory"
	release
# 33 "data/maps/NewmoonIsland_Interior/scripts.pory"
	end
# 34 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 35 "data/maps/NewmoonIsland_Interior/scripts.pory"
@ Fainted or fled: its hide flag (the object's flag) stays set until the next voyage here (Voyage_Depart).
# 36 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_EventScript_DarkraiGone::
# 37 "data/maps/NewmoonIsland_Interior/scripts.pory"
	setvar VAR_0x8004, SPECIES_DARKRAI
# 38 "data/maps/NewmoonIsland_Interior/scripts.pory"
	goto Voyage_EventScript_LegendaryGone
# 39 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 40 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_EventScript_Leave::
# 41 "data/maps/NewmoonIsland_Interior/scripts.pory"
	lockall
# 42 "data/maps/NewmoonIsland_Interior/scripts.pory"
	warp MAP_NEWMOON_ISLAND, 0
# 43 "data/maps/NewmoonIsland_Interior/scripts.pory"
	waitstate
# 44 "data/maps/NewmoonIsland_Interior/scripts.pory"
	releaseall
# 45 "data/maps/NewmoonIsland_Interior/scripts.pory"
	end
# 46 "data/maps/NewmoonIsland_Interior/scripts.pory"

# 47 "data/maps/NewmoonIsland_Interior/scripts.pory"
NewmoonIsland_Interior_EventScript_Leave2::
# 48 "data/maps/NewmoonIsland_Interior/scripts.pory"
	lockall
# 49 "data/maps/NewmoonIsland_Interior/scripts.pory"
	warp MAP_NEWMOON_ISLAND, 1
# 50 "data/maps/NewmoonIsland_Interior/scripts.pory"
	waitstate
# 51 "data/maps/NewmoonIsland_Interior/scripts.pory"
	releaseall
# 52 "data/maps/NewmoonIsland_Interior/scripts.pory"
	end
