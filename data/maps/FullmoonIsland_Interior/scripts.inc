# 1 "data/maps/FullmoonIsland_Interior/scripts.pory"

# 2 "data/maps/FullmoonIsland_Interior/scripts.pory"
FullmoonIsland_Interior_MapScripts::
# 3 "data/maps/FullmoonIsland_Interior/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, FullmoonIsland_Interior_OnResume
# 4 "data/maps/FullmoonIsland_Interior/scripts.pory"
	.byte 0
# 5 "data/maps/FullmoonIsland_Interior/scripts.pory"

# 6 "data/maps/FullmoonIsland_Interior/scripts.pory"
FullmoonIsland_Interior_OnResume:
# 7 "data/maps/FullmoonIsland_Interior/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, FullmoonIsland_Interior_EventScript_TryRemoveCresselia
# 8 "data/maps/FullmoonIsland_Interior/scripts.pory"
	end
# 9 "data/maps/FullmoonIsland_Interior/scripts.pory"

# 10 "data/maps/FullmoonIsland_Interior/scripts.pory"
FullmoonIsland_Interior_EventScript_TryRemoveCresselia::
# 11 "data/maps/FullmoonIsland_Interior/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 12 "data/maps/FullmoonIsland_Interior/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 13 "data/maps/FullmoonIsland_Interior/scripts.pory"
	removeobject LOCALID_FULLMOON_CRESSELIA
# 14 "data/maps/FullmoonIsland_Interior/scripts.pory"
	return
# 15 "data/maps/FullmoonIsland_Interior/scripts.pory"

# 16 "data/maps/FullmoonIsland_Interior/scripts.pory"
FullmoonIsland_Interior_EventScript_Cresselia::
# 17 "data/maps/FullmoonIsland_Interior/scripts.pory"
	lock
# 18 "data/maps/FullmoonIsland_Interior/scripts.pory"
	faceplayer
# 19 "data/maps/FullmoonIsland_Interior/scripts.pory"
	waitse
# 20 "data/maps/FullmoonIsland_Interior/scripts.pory"
	playmoncry SPECIES_CRESSELIA, CRY_MODE_ENCOUNTER
# 21 "data/maps/FullmoonIsland_Interior/scripts.pory"
	delay 40
# 22 "data/maps/FullmoonIsland_Interior/scripts.pory"
	waitmoncry
# 23 "data/maps/FullmoonIsland_Interior/scripts.pory"
	setwildbattle SPECIES_CRESSELIA, VOYAGE_LEGENDARY_LEVEL
# 24 "data/maps/FullmoonIsland_Interior/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 25 "data/maps/FullmoonIsland_Interior/scripts.pory"
	special BattleSetup_StartLegendaryBattle
# 26 "data/maps/FullmoonIsland_Interior/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 27 "data/maps/FullmoonIsland_Interior/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 28 "data/maps/FullmoonIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, FullmoonIsland_Interior_EventScript_CresseliaGone
# 29 "data/maps/FullmoonIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, FullmoonIsland_Interior_EventScript_CresseliaGone
# 30 "data/maps/FullmoonIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, FullmoonIsland_Interior_EventScript_CresseliaGone
# 31 "data/maps/FullmoonIsland_Interior/scripts.pory"
	setflag FLAG_CAUGHT_VOYAGE_CRESSELIA
# 32 "data/maps/FullmoonIsland_Interior/scripts.pory"
	release
# 33 "data/maps/FullmoonIsland_Interior/scripts.pory"
	end
# 34 "data/maps/FullmoonIsland_Interior/scripts.pory"

# 35 "data/maps/FullmoonIsland_Interior/scripts.pory"
@ Fainted or fled: its hide flag (the object's flag) stays set until the next voyage here (Voyage_Depart).
# 36 "data/maps/FullmoonIsland_Interior/scripts.pory"
FullmoonIsland_Interior_EventScript_CresseliaGone::
# 37 "data/maps/FullmoonIsland_Interior/scripts.pory"
	setvar VAR_0x8004, SPECIES_CRESSELIA
# 38 "data/maps/FullmoonIsland_Interior/scripts.pory"
	goto Voyage_EventScript_LegendaryGone
