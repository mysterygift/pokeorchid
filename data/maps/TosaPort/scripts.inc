TosaPort_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TosaPort_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, TosaPort_OnWarp
	.byte 0

TosaPort_OnTransition:
	setflag FLAG_VISITED_TOSA_PORT
	end

@ After object events exist; RunScriptImmediately — use only instant cmds (turnobject is OK).
TosaPort_OnWarp:
	map_script_2 VAR_TEMP_0, 0, TosaPort_EventScript_WarpFaceNorthIfNoMon
	.2byte 0

TosaPort_EventScript_WarpFaceNorthIfNoMon::
	goto_if_set FLAG_SYS_POKEMON_GET, TosaPort_EventScript_WarpFaceNorthIfNoMon_End
	turnobject LOCALID_PLAYER, DIR_NORTH

TosaPort_EventScript_WarpFaceNorthIfNoMon_End::
	end

TosaPort_EventScript_TownSign::
	msgbox TosaPort_Text_TownSign, MSGBOX_SIGN
	end

TosaPort_EventScript_GatewaySign::
	msgbox TosaPort_Text_GatewaySign, MSGBOX_SIGN
	end

TosaPort_EventScript_StarterGuide::
	lock
	faceplayer
	goto_if_set FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG, TosaPort_EventScript_StarterGuide_AfterStarter
	msgbox TosaPort_Text_YouMustBePlayer, MSGBOX_NPC
	delay 48
	applymovement LOCALID_STARTER_AIDE, Common_Movement_ExclamationMark
	waitmovement 0
	playse SE_PIN
	msgbox TosaPort_Text_GivePokemon, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	setflag FLAG_SYS_POKEMON_GET
	special ChooseStarterOverworld
	waitstate
	bufferleadmonspeciesname STR_VAR_2
	playfanfare MUS_OBTAIN_TMHM
	msgbox TosaPort_Text_ReceivedPokemon, MSGBOX_AUTOCLOSE
	waitfanfare
	msgbox TosaPort_Text_Nickname, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, 1, TosaPort_EventScript_GiveNickname
	setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
	msgbox TosaPort_Text_TakeTosaPass, MSGBOX_DEFAULT
	release
	end

TosaPort_EventScript_GiveNickname::
	fadescreen FADE_TO_BLACK
	special ChangePokemonNickname
	waitstate
	setflag FLAG_HIDE_ROUTE_101_BIRCH_STARTERS_BAG
	msgbox TosaPort_Text_TakeTosaPass, MSGBOX_DEFAULT
	msgbox TosaPort_Text_StarterGuideTelokHint
	release
	end

TosaPort_EventScript_StarterGuide_AfterStarter::
	msgbox TosaPort_Text_StarterGuideTelokHint, MSGBOX_DEFAULT
	release
	end

TosaPort_Text_YouMustBePlayer:
	.string "Ah! You must be {PLAYER}.\p"
	.string "Professor Palm sent me to meet you\n"
	.string "once the Seagallop-20 made port.$"

TosaPort_Text_GivePokemon:
	.string "I've brought you a little welcome\n"
	.string "present on behalf of the University.\p"
	.string "With the journey being so long from\n"
	.string "Galar, we figured you wouldn't bring\l"
	.string "your partners along.\p"
	.string "You peer inside the bag.$"

TosaPort_Text_ReceivedPokemon:
	.string "You receieved a {STR_VAR_2}!$"

TosaPort_Text_Nickname:
	.string "Would you like to give {STR_VAR_2} a\n"
	.string "nickname?$"

TosaPort_Text_TakeTosaPass:
	.string "If you're going to reach Professsor Palm,\n"
	.string "you'll need this Tosa Pass.\p"
	.string "(Placeholder: TOSA PASS received.)$"

TosaPort_Text_StarterGuideTelokHint:
	.string "The road to TELOK TOWN runs through\n"
	.string "the Tosa nature reserve to the north.\p"
	.string "You'll find Palm Labs there.$"

TosaPort_Text_TownSign:
	.string "Welcome to Tosa!\n"
	.string "- The Tosa Tourism Board$"

TosaPort_Text_GatewaySign:
	.string "Tosa Reserve Gateway\n"
	.string "Trainer passes strictly required $"
