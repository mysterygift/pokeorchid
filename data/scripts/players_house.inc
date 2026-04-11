@ TosaPort_MaysHouse_2F_EventScript_WallClock::
@ 	lockall
@ 	setvar VAR_0x8004, FEMALE
@ 	goto PlayersHouse_2F_EventScript_WallClock
@ 	end

@ PlayersHouse_2F_EventScript_WallClock::
@ 	goto_if_set FLAG_SET_WALL_CLOCK, PlayersHouse_2F_EventScript_CheckWallClock
@ 	msgbox PlayersHouse_2F_Text_ClockIsStopped, MSGBOX_DEFAULT
@ 	call PlayersHouse_2F_EventScript_SetWallClock
@ 	delay 30
@ 	setvar VAR_LITTLEROOT_INTRO_STATE, 6
@ 	setflag FLAG_SET_WALL_CLOCK
@ 	setflag FLAG_HIDE_TOSA_PORT_PLAYERS_HOUSE_VIGOROTH_1
@ 	setflag FLAG_HIDE_TOSA_PORT_PLAYERS_HOUSE_VIGOROTH_2
@ 	checkplayergender
@ 	playse SE_EXIT
@ 	removeobject VAR_0x8008
@ 	releaseall
@ 	end
