.set TYPE_RPS_RESULT_LOSS,   0
.set TYPE_RPS_RESULT_WIN,    1
.set TYPE_RPS_RESULT_CANCEL, 2

Common_EventScript_TypeRpsMinigame::
	lockall
	faceplayer
	msgbox TypeRps_Text_Intro, MSGBOX_DEFAULT
	closemessage
	playtyperms
	goto_if_eq VAR_RESULT, TYPE_RPS_RESULT_CANCEL, TypeRps_EventScript_Cancelled
	goto_if_eq VAR_RESULT, TYPE_RPS_RESULT_WIN, TypeRps_EventScript_Won
TypeRps_EventScript_Lost::
	msgbox TypeRps_Text_Lost, MSGBOX_DEFAULT
	releaseall
	end

TypeRps_EventScript_Cancelled::
	msgbox TypeRps_Text_Cancelled, MSGBOX_DEFAULT
	releaseall
	end

TypeRps_EventScript_Won::
	checkitemspace ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, TypeRps_EventScript_NoRoom
	giveitem_msg TypeRps_Text_GotRareCandy, ITEM_RARE_CANDY, 1
	releaseall
	end

TypeRps_EventScript_NoRoom::
	msgbox TypeRps_Text_BagFull, MSGBOX_DEFAULT
	releaseall
	end

TypeRps_Text_Intro:
	.string "Let's play FIRE, WATER, GRASS!\n"
	.string "Same as rock-paper-scissors.\p"
	.string "Pick your type, then we'll count\n"
	.string "to three and reveal my pick.\p"
	.string "Beat me and I'll give you a treat!$"

TypeRps_Text_Cancelled:
	.string "Maybe next time!$"

TypeRps_Text_Lost:
	.string "Tough luck! Want to try again?$"

TypeRps_Text_GotRareCandy:
	.string "Amazing! Here's your prize!$"

TypeRps_Text_BagFull:
	.string "Your BAG is full. Make room and\n"
	.string "come back!$"
