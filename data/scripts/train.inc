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
