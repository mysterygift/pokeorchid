# 1 "data/maps/SouthernIsland_Interior/scripts.pory"

# 2 "data/maps/SouthernIsland_Interior/scripts.pory"
@ Orchid: Eon Island (vanilla Southern Island). Voyage legendary: Latias by day, Latios at night (gettimeofday),
# 3 "data/maps/SouthernIsland_Interior/scripts.pory"
@ each until caught; a fainted/fled one returns on the next voyage (src/voyages.c clears its hide flag).
# 4 "data/maps/SouthernIsland_Interior/scripts.pory"
@ The mega stone item balls appear once their Lati is caught.
# 5 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_MapScripts::
# 6 "data/maps/SouthernIsland_Interior/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, SouthernIsland_Interior_OnResume
# 7 "data/maps/SouthernIsland_Interior/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SouthernIsland_Interior_OnTransition
# 8 "data/maps/SouthernIsland_Interior/scripts.pory"
	.byte 0
# 9 "data/maps/SouthernIsland_Interior/scripts.pory"

# 10 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_OnResume:
# 11 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, SouthernIsland_Interior_EventScript_TryRemoveLati
# 12 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 13 "data/maps/SouthernIsland_Interior/scripts.pory"

# 14 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_TryRemoveLati::
# 15 "data/maps/SouthernIsland_Interior/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 16 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 17 "data/maps/SouthernIsland_Interior/scripts.pory"
	removeobject LOCALID_SOUTHERN_ISLAND_LATI
# 18 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 19 "data/maps/SouthernIsland_Interior/scripts.pory"

# 20 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_OnTransition:
# 21 "data/maps/SouthernIsland_Interior/scripts.pory"
	gettimeofday
# 22 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_eq VAR_0x8000, TIME_NIGHT, SouthernIsland_Interior_EventScript_SetUpLatios
# 23 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_ne VAR_0x8000, TIME_NIGHT, SouthernIsland_Interior_EventScript_SetUpLatias
# 24 "data/maps/SouthernIsland_Interior/scripts.pory"
	call SouthernIsland_Interior_EventScript_SetUpPlayerGfx
# 25 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_unset FLAG_CAUGHT_VOYAGE_LATIAS, SouthernIsland_Interior_EventScript_HideLatiasite
# 26 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_set FLAG_ITEM_EON_ISLAND_LATIASITE, SouthernIsland_Interior_EventScript_HideLatiasite
# 27 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_unset FLAG_CAUGHT_VOYAGE_LATIOS, SouthernIsland_Interior_EventScript_HideLatiosite
# 28 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_set FLAG_ITEM_EON_ISLAND_LATIOSITE, SouthernIsland_Interior_EventScript_HideLatiosite
# 29 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 30 "data/maps/SouthernIsland_Interior/scripts.pory"

# 31 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_HideLatiasite::
# 32 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_TEMP_3
# 33 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 34 "data/maps/SouthernIsland_Interior/scripts.pory"

# 35 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_HideLatiosite::
# 36 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_TEMP_4
# 37 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 38 "data/maps/SouthernIsland_Interior/scripts.pory"

# 39 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetUpLatios::
# 40 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_OBJ_GFX_ID_1, OBJ_EVENT_GFX_LATIOS
# 41 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_TEMP_4, SPECIES_LATIOS
# 42 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 43 "data/maps/SouthernIsland_Interior/scripts.pory"

# 44 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetUpLatias::
# 45 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_OBJ_GFX_ID_1, OBJ_EVENT_GFX_LATIAS
# 46 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_TEMP_4, SPECIES_LATIAS
# 47 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 48 "data/maps/SouthernIsland_Interior/scripts.pory"

# 49 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetUpPlayerGfx::
# 50 "data/maps/SouthernIsland_Interior/scripts.pory"
	checkplayergender
# 51 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, MALE, SouthernIsland_Interior_EventScript_SetBrendanGfx
# 52 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, FEMALE, SouthernIsland_Interior_EventScript_SetMayGfx
# 53 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 54 "data/maps/SouthernIsland_Interior/scripts.pory"

# 55 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetBrendanGfx::
# 56 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
# 57 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 58 "data/maps/SouthernIsland_Interior/scripts.pory"

# 59 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetMayGfx::
# 60 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
# 61 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 62 "data/maps/SouthernIsland_Interior/scripts.pory"

# 63 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_TryLatiEncounter::
# 64 "data/maps/SouthernIsland_Interior/scripts.pory"
	lockall
# 65 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_set FLAG_TEMP_2, SouthernIsland_Interior_EventScript_Sign
# 66 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_CheckLatios
# 67 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_set FLAG_HIDE_EON_LATIAS, SouthernIsland_Interior_EventScript_Sign
# 68 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto SouthernIsland_Interior_EventScript_Lati
# 69 "data/maps/SouthernIsland_Interior/scripts.pory"

# 70 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_CheckLatios::
# 71 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_set FLAG_HIDE_EON_LATIOS, SouthernIsland_Interior_EventScript_Sign
# 72 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_Lati::
# 73 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_ENCOUNTERED_LATIAS_OR_LATIOS
# 74 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_TEMP_2
# 75 "data/maps/SouthernIsland_Interior/scripts.pory"
	special SpawnCameraObject
# 76 "data/maps/SouthernIsland_Interior/scripts.pory"
	applymovement LOCALID_CAMERA, SouthernIsland_Interior_Movement_CameraPanUp
# 77 "data/maps/SouthernIsland_Interior/scripts.pory"
	waitmovement 0
# 78 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay 50
# 79 "data/maps/SouthernIsland_Interior/scripts.pory"
	waitse
# 80 "data/maps/SouthernIsland_Interior/scripts.pory"
	playmoncry VAR_TEMP_4, CRY_MODE_NORMAL
# 81 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay 30
# 82 "data/maps/SouthernIsland_Interior/scripts.pory"
	waitmoncry
# 83 "data/maps/SouthernIsland_Interior/scripts.pory"
	addobject LOCALID_SOUTHERN_ISLAND_LATI
# 84 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay 30
# 85 "data/maps/SouthernIsland_Interior/scripts.pory"
	applymovement LOCALID_CAMERA, SouthernIsland_Interior_Movement_CameraPanDown
# 86 "data/maps/SouthernIsland_Interior/scripts.pory"
	applymovement LOCALID_SOUTHERN_ISLAND_LATI, SouthernIsland_Interior_Movement_LatiApproach
# 87 "data/maps/SouthernIsland_Interior/scripts.pory"
	waitmovement 0
# 88 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay 50
# 89 "data/maps/SouthernIsland_Interior/scripts.pory"
	special RemoveCameraObject
# 90 "data/maps/SouthernIsland_Interior/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_SOUTHERN_ISLAND_LATI
# 91 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_SetLatiosBattleVars
# 92 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_ne VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_SetLatiasBattleVars
# 93 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 94 "data/maps/SouthernIsland_Interior/scripts.pory"
	special BattleSetup_StartLegendaryBattle
# 95 "data/maps/SouthernIsland_Interior/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 96 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_LatiosGone
# 97 "data/maps/SouthernIsland_Interior/scripts.pory"
	call_if_ne VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_LatiasGone
# 98 "data/maps/SouthernIsland_Interior/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 99 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SouthernIsland_Interior_EventScript_LatiFlewAway
# 100 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, SouthernIsland_Interior_EventScript_LatiFlewAway
# 101 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, SouthernIsland_Interior_EventScript_LatiFlewAway
# 102 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_TEMP_4, SPECIES_LATIOS, SouthernIsland_Interior_EventScript_CaughtLatios
# 103 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_CAUGHT_VOYAGE_LATIAS
# 104 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_set FLAG_ITEM_EON_ISLAND_LATIASITE, SouthernIsland_Interior_EventScript_CaughtDone
# 105 "data/maps/SouthernIsland_Interior/scripts.pory"
	clearflag FLAG_TEMP_3
# 106 "data/maps/SouthernIsland_Interior/scripts.pory"
	addobject LOCALID_EON_LATIASITE
# 107 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto SouthernIsland_Interior_EventScript_CaughtDone
# 108 "data/maps/SouthernIsland_Interior/scripts.pory"

# 109 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_CaughtLatios::
# 110 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_CAUGHT_VOYAGE_LATIOS
# 111 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_set FLAG_ITEM_EON_ISLAND_LATIOSITE, SouthernIsland_Interior_EventScript_CaughtDone
# 112 "data/maps/SouthernIsland_Interior/scripts.pory"
	clearflag FLAG_TEMP_4
# 113 "data/maps/SouthernIsland_Interior/scripts.pory"
	addobject LOCALID_EON_LATIOSITE
# 114 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_CaughtDone::
# 115 "data/maps/SouthernIsland_Interior/scripts.pory"
	releaseall
# 116 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 117 "data/maps/SouthernIsland_Interior/scripts.pory"

# 118 "data/maps/SouthernIsland_Interior/scripts.pory"
@ Whatever the outcome, this Lati is gone until the next voyage (or for good once caught).
# 119 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_LatiasGone::
# 120 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_HIDE_EON_LATIAS
# 121 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 122 "data/maps/SouthernIsland_Interior/scripts.pory"

# 123 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_LatiosGone::
# 124 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_HIDE_EON_LATIOS
# 125 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 126 "data/maps/SouthernIsland_Interior/scripts.pory"

# 127 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_LatiFlewAway::
# 128 "data/maps/SouthernIsland_Interior/scripts.pory"
	copyvar VAR_0x8004, VAR_TEMP_4
# 129 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto Voyage_EventScript_LegendaryGone
# 130 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 131 "data/maps/SouthernIsland_Interior/scripts.pory"

# 132 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_Sign::
# 133 "data/maps/SouthernIsland_Interior/scripts.pory"
	msgbox SouthernIsland_Interior_Text_Sign, MSGBOX_DEFAULT
# 134 "data/maps/SouthernIsland_Interior/scripts.pory"
	releaseall
# 135 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 136 "data/maps/SouthernIsland_Interior/scripts.pory"

# 137 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetLatiosBattleVars::
# 138 "data/maps/SouthernIsland_Interior/scripts.pory"
	setwildbattle SPECIES_LATIOS, VOYAGE_LEGENDARY_LEVEL
# 139 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 140 "data/maps/SouthernIsland_Interior/scripts.pory"

# 141 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_SetLatiasBattleVars::
# 142 "data/maps/SouthernIsland_Interior/scripts.pory"
	setwildbattle SPECIES_LATIAS, VOYAGE_LEGENDARY_LEVEL
# 143 "data/maps/SouthernIsland_Interior/scripts.pory"
	return
# 144 "data/maps/SouthernIsland_Interior/scripts.pory"

# 145 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_Latiasite::
# 146 "data/maps/SouthernIsland_Interior/scripts.pory"
	finditem ITEM_LATIASITE
# 147 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_0x8007, FALSE, SouthernIsland_Interior_EventScript_ItemEnd
# 148 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_ITEM_EON_ISLAND_LATIASITE
# 149 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 150 "data/maps/SouthernIsland_Interior/scripts.pory"

# 151 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_Latiosite::
# 152 "data/maps/SouthernIsland_Interior/scripts.pory"
	finditem ITEM_LATIOSITE
# 153 "data/maps/SouthernIsland_Interior/scripts.pory"
	goto_if_eq VAR_0x8007, FALSE, SouthernIsland_Interior_EventScript_ItemEnd
# 154 "data/maps/SouthernIsland_Interior/scripts.pory"
	setflag FLAG_ITEM_EON_ISLAND_LATIOSITE
# 155 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_EventScript_ItemEnd::
# 156 "data/maps/SouthernIsland_Interior/scripts.pory"
	end
# 157 "data/maps/SouthernIsland_Interior/scripts.pory"

# 158 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_Movement_CameraPanUp:
# 159 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_up
# 160 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_up
# 161 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_up
# 162 "data/maps/SouthernIsland_Interior/scripts.pory"
	step_end
# 163 "data/maps/SouthernIsland_Interior/scripts.pory"

# 164 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_Movement_CameraPanDown:
# 165 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 166 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 167 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 168 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 169 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 170 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 171 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 172 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 173 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 174 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 175 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_in_place_faster_up
# 176 "data/maps/SouthernIsland_Interior/scripts.pory"
	step_end
# 177 "data/maps/SouthernIsland_Interior/scripts.pory"

# 178 "data/maps/SouthernIsland_Interior/scripts.pory"
SouthernIsland_Interior_Movement_LatiApproach:
# 179 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 180 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 181 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 182 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 183 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 184 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 185 "data/maps/SouthernIsland_Interior/scripts.pory"
	delay_16
# 186 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 187 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 188 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 189 "data/maps/SouthernIsland_Interior/scripts.pory"
	walk_down
# 190 "data/maps/SouthernIsland_Interior/scripts.pory"
	step_end
