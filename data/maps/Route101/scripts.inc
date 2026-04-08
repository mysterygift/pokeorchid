# 1 "data/maps/Route101/scripts.pory"

# 2 "data/maps/Route101/scripts.pory"
Route101_MapScripts::
# 3 "data/maps/Route101/scripts.pory"
	.byte 0
# 4 "data/maps/Route101/scripts.pory"

# 5 "data/maps/Route101/scripts.pory"
Route101_EventScript_RouteSign::
# 6 "data/maps/Route101/scripts.pory"
	msgbox Route101_Text_RouteSign, MSGBOX_SIGN
# 7 "data/maps/Route101/scripts.pory"
	end
# 8 "data/maps/Route101/scripts.pory"

# 9 "data/maps/Route101/scripts.pory"
Route101_EventScript_BirchsBag::
# 10 "data/maps/Route101/scripts.pory"
	@ lock
# 11 "data/maps/Route101/scripts.pory"
	@ faceplayer
# 12 "data/maps/Route101/scripts.pory"
	@ setflag FLAG_SYS_POKEMON_GET
# 13 "data/maps/Route101/scripts.pory"
	@ setflag FLAG_RESCUED_BIRCH
# 14 "data/maps/Route101/scripts.pory"
	@ fadescreen FADE_TO_BLACK
# 15 "data/maps/Route101/scripts.pory"
	@ removeobject LOCALID_ROUTE101_ZIGZAGOON
# 16 "data/maps/Route101/scripts.pory"
	@ setobjectxy LOCALID_PLAYER, 6, 13
# 17 "data/maps/Route101/scripts.pory"
	@ applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterLeft
# 18 "data/maps/Route101/scripts.pory"
	@ waitmovement 0
# 19 "data/maps/Route101/scripts.pory"
	@ special ChooseStarter
# 20 "data/maps/Route101/scripts.pory"
	@ waitstate
# 21 "data/maps/Route101/scripts.pory"
	@ applymovement LOCALID_ROUTE101_BIRCH, Route101_Movement_BirchApproachPlayer
# 22 "data/maps/Route101/scripts.pory"
	@ waitmovement 0
# 23 "data/maps/Route101/scripts.pory"
	@ msgbox Route101_Text_YouSavedMe, MSGBOX_DEFAULT
# 24 "data/maps/Route101/scripts.pory"
	@ special HealPlayerParty
# 25 "data/maps/Route101/scripts.pory"
	@ setflag FLAG_HIDE_ROUTE_101_BIRCH_ZIGZAGOON_BATTLE
# 26 "data/maps/Route101/scripts.pory"
	@ clearflag FLAG_HIDE_TOSA_PORT_BIRCHS_LAB_BIRCH
# 27 "data/maps/Route101/scripts.pory"
	@ setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
# 28 "data/maps/Route101/scripts.pory"
	@ setvar VAR_BIRCH_LAB_STATE, 2
# 29 "data/maps/Route101/scripts.pory"
	@ setvar VAR_ROUTE101_STATE, 3
# 30 "data/maps/Route101/scripts.pory"
	@ clearflag FLAG_HIDE_MAP_NAME_POPUP
# 31 "data/maps/Route101/scripts.pory"
	@ checkplayergender
# 32 "data/maps/Route101/scripts.pory"
	@ call_if_eq VAR_RESULT, MALE, Route101_EventScript_HideMayInBedroom
# 33 "data/maps/Route101/scripts.pory"
	@ call_if_eq VAR_RESULT, FEMALE, Route101_EventScript_HideBrendanInBedroom
# 34 "data/maps/Route101/scripts.pory"
	@ warp MAP_TOSA_PORT_PROFESSOR_BIRCHS_LAB, 6, 5
# 35 "data/maps/Route101/scripts.pory"
	@ waitstate
# 36 "data/maps/Route101/scripts.pory"
	@ release
# 37 "data/maps/Route101/scripts.pory"
	@ end
# 38 "data/maps/Route101/scripts.pory"
	end
# 39 "data/maps/Route101/scripts.pory"

# 40 "data/maps/Route101/scripts.pory"
Route101_Text_RouteSign:
# 41 "data/maps/Route101/scripts.pory"
	.string "Tosa Reserve South\n"
# 42 "data/maps/Route101/scripts.pory"
	.string "{DOWN_ARROW} Tosa Port$"
