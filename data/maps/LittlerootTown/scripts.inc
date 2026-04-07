LittlerootTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TosaPort_OnTransition
	.byte 0

TosaPort_OnTransition:
	setflag FLAG_VISITED_TOSA_PORT
	call Common_EventScript_SetupRivalGfxId
	end

TosaPort_EventScript_TownSign::
	msgbox TosaPort_Text_TownSign, MSGBOX_SIGN
	end

TosaPort_EventScript_GatewaySign::
	msgbox TosaPort_Text_GatewaySign, MSGBOX_SIGN
	end

TosaPort_Text_TownSign:
	.string "Welcome to Tosa!\n"
	.string "- The Tosa Tourism Board$"

TosaPort_Text_GatewaySign:
	.string "Tosa Reserve Gateway\n"
	.string "Trainer passes strictly required $"
