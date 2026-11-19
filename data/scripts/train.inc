@ Tosa Rail — see src/train_travel.c.
@ Map scripts use the `usetrain` and `settrainstation` macros (asm/macros/event.inc).

@ Called by `usetrain` from an already-locked NPC/sign script. Returns on cancel; on departure the
@ field reloads at the destination, so the caller's script never resumes.
Common_EventScript_UseTrain::
	checkitem ITEM_RAIL_CARD
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_UseTrain_NoRailCard
	special TrainStation_CountDestinations
	goto_if_eq VAR_RESULT, 0, Common_EventScript_UseTrain_NoDestinations
	msgbox Common_Text_UseTrain_WhereTo, MSGBOX_DEFAULT
	closemessage
	special TrainStation_OpenMap     @ VAR_RESULT / VAR_0x8004 = chosen station
	waitstate
	goto_if_eq VAR_RESULT, TRAIN_STATION_NONE, Common_EventScript_UseTrain_Cancel
	hidefollower
	setvar VAR_0x8005, FALSE   @ TRUE = train pulls in first instead of waiting at the platform
	special TrainTravel_Depart
	waitstate
	end

Common_EventScript_UseTrain_NoRailCard::
	msgbox Common_Text_UseTrain_NoRailCard, MSGBOX_DEFAULT
	return

Common_EventScript_UseTrain_NoDestinations::
	msgbox Common_Text_UseTrain_NoDestinations, MSGBOX_DEFAULT
	return

Common_EventScript_UseTrain_Cancel::
	msgbox Common_Text_UseTrain_ComeAgain, MSGBOX_DEFAULT
	return

Common_Text_UseTrain_WhereTo:
	.string "Welcome to TOSA RAIL!\n"
	.string "Where would you like to go?$"

Common_Text_UseTrain_NoRailCard:
	.string "Welcome to TOSA RAIL!\p"
	.string "Passengers need a RAIL CARD to\n"
	.string "board the train. Sorry!$"

Common_Text_UseTrain_NoDestinations:
	.string "Welcome to TOSA RAIL!\p"
	.string "There aren't any stations you can\n"
	.string "travel to from here yet.$"

Common_Text_UseTrain_ComeAgain:
	.string "Please ride with us again!$"

@ ---------------------------------------------------------------------------------------------
@ Shared by the generated stations (dev_scripts/train_ui/tosa_stations.py). Their concourse fare
@ gates reuse TosaGateway_FareGateNorth / _South (same tiles as the Tosa Port gatehouse).
TosaRail_EventScript_Receptionist::
	lock
	faceplayer
	msgbox TosaRail_Text_Receptionist, MSGBOX_DEFAULT
	release
	end

TosaRail_EventScript_PlatformAttendant::
	lock
	faceplayer
	usetrain
	release
	end

@ TEMP (testing) / debug: open or lock every station. Called by the Tosa Port platform attendant
@ until the story opens stations, and by the station master in TrainTestEast.
TosaRail_EventScript_OpenAllStations::
	setvar VAR_0x8004, 0
TosaRail_EventScript_OpenAllStations_Loop::
	setvar VAR_0x8005, TRAIN_ACCESS_OPEN
	special TrainStation_SetAccess
	addvar VAR_0x8004, 1
	goto_if_lt VAR_0x8004, TRAIN_STATION_COUNT, TosaRail_EventScript_OpenAllStations_Loop
	return

TosaRail_EventScript_LockAllStations::
	setvar VAR_0x8004, 0
TosaRail_EventScript_LockAllStations_Loop::
	setvar VAR_0x8005, TRAIN_ACCESS_LOCKED
	special TrainStation_SetAccess
	addvar VAR_0x8004, 1
	goto_if_lt VAR_0x8004, TRAIN_STATION_COUNT, TosaRail_EventScript_LockAllStations_Loop
	return

TosaRail_Text_Receptionist:
	.string "Welcome to TOSA RAIL!\p"
	.string "Tap your RAIL CARD at the fare\n"
	.string "gates, then take the escalator\l"
	.string "down to the platform.$"
