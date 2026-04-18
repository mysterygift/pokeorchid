# 1 "data/maps/SouthTosaReserve/scripts.pory"

# 2 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_MapScripts::
# 3 "data/maps/SouthTosaReserve/scripts.pory"
	.byte 0
# 4 "data/maps/SouthTosaReserve/scripts.pory"

# 5 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_EventScript_RouteSign::
# 6 "data/maps/SouthTosaReserve/scripts.pory"
	msgbox SouthTosaReserve_Text_RouteSign, MSGBOX_SIGN
# 7 "data/maps/SouthTosaReserve/scripts.pory"
	end
# 8 "data/maps/SouthTosaReserve/scripts.pory"

# 9 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_EventScript_BirchsBag::
# 10 "data/maps/SouthTosaReserve/scripts.pory"
	@ lock
# 11 "data/maps/SouthTosaReserve/scripts.pory"
	@ faceplayer
# 12 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_SYS_POKEMON_GET
# 13 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_RESCUED_BIRCH
# 14 "data/maps/SouthTosaReserve/scripts.pory"
	@ fadescreen FADE_TO_BLACK
# 15 "data/maps/SouthTosaReserve/scripts.pory"
	@ removeobject LOCALID_SOUTHTOSARESERVE_ZIGZAGOON
# 16 "data/maps/SouthTosaReserve/scripts.pory"
	@ setobjectxy LOCALID_PLAYER, 6, 13
# 17 "data/maps/SouthTosaReserve/scripts.pory"
	@ applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
# 18 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitmovement 0
# 19 "data/maps/SouthTosaReserve/scripts.pory"
	@ special ChooseStarter
# 20 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitstate
# 21 "data/maps/SouthTosaReserve/scripts.pory"
	@ applymovement LOCALID_SOUTHTOSARESERVE_BIRCH, SouthTosaReserve_Movement_BirchApproachPlayer
# 22 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitmovement 0
# 23 "data/maps/SouthTosaReserve/scripts.pory"
	@ msgbox SouthTosaReserve_Text_YouSavedMe, MSGBOX_DEFAULT
# 24 "data/maps/SouthTosaReserve/scripts.pory"
	@ special HealPlayerParty
# 25 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_ZIGZAGOON_BATTLE
# 26 "data/maps/SouthTosaReserve/scripts.pory"
	@ clearflag FLAG_HIDE_TOSA_PORT_BIRCHS_LAB_BIRCH
# 27 "data/maps/SouthTosaReserve/scripts.pory"
	@ setflag FLAG_HIDE_SOUTH_TOSA_RESERVE_BIRCH_STARTERS_BAG
# 28 "data/maps/SouthTosaReserve/scripts.pory"
	@ setvar VAR_BIRCH_LAB_STATE, 2
# 29 "data/maps/SouthTosaReserve/scripts.pory"
	@ setvar VAR_SOUTHTOSARESERVE_STATE, 3
# 30 "data/maps/SouthTosaReserve/scripts.pory"
	@ clearflag FLAG_HIDE_MAP_NAME_POPUP
# 31 "data/maps/SouthTosaReserve/scripts.pory"
	@ checkplayergender
# 32 "data/maps/SouthTosaReserve/scripts.pory"
	@ call_if_eq VAR_RESULT, MALE, SouthTosaReserve_EventScript_HideMayInBedroom
# 33 "data/maps/SouthTosaReserve/scripts.pory"
	@ call_if_eq VAR_RESULT, FEMALE, SouthTosaReserve_EventScript_HideBrendanInBedroom
# 34 "data/maps/SouthTosaReserve/scripts.pory"
	@ warp MAP_TOSA_PORT_PROFESSOR_BIRCHS_LAB, 6, 5
# 35 "data/maps/SouthTosaReserve/scripts.pory"
	@ waitstate
# 36 "data/maps/SouthTosaReserve/scripts.pory"
	@ release
# 37 "data/maps/SouthTosaReserve/scripts.pory"
	@ end
# 38 "data/maps/SouthTosaReserve/scripts.pory"
	end
# 39 "data/maps/SouthTosaReserve/scripts.pory"

# 40 "data/maps/SouthTosaReserve/scripts.pory"
SouthTosaReserve_Text_RouteSign:
# 41 "data/maps/SouthTosaReserve/scripts.pory"
	.string "Tosa Reserve South\n"
# 42 "data/maps/SouthTosaReserve/scripts.pory"
	.string "{DOWN_ARROW} Tosa Port$"
