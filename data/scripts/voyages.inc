@ Orchid: the Sailor's voyages (src/voyages.c). One Sailor script for every dock: Wavebreak Town (after the
@ Champion), Eon Island, Newmoon Island and Fullmoon Island. The menu lists only unlocked destinations.

Voyage_EventScript_Sailor::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, Voyage_EventScript_SailorNotYet
	msgbox Voyage_Text_SailorGreeting, MSGBOX_DEFAULT
Voyage_EventScript_SailorMenu::
	message Voyage_Text_WhereTo
	waitmessage
	special Voyage_BuildMenu
	dynmultistack 0, 0, FALSE, 6, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	switch VAR_RESULT
	case VOYAGE_MENU_ENTER_CODE, Voyage_EventScript_EnterCode
	case VOYAGE_MENU_CANCEL, Voyage_EventScript_Cancel
	case MULTI_B_PRESSED, Voyage_EventScript_Cancel
	copyvar VAR_0x8006, VAR_RESULT
	special Voyage_IsDestinationOpen
	goto_if_eq VAR_RESULT, FALSE, Voyage_EventScript_SeasTooRough
	msgbox Voyage_Text_SetSailFor, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Voyage_EventScript_Cancel
	msgbox Voyage_Text_CastOff, MSGBOX_DEFAULT
	closemessage
	delay 20
	fadescreen FADE_TO_BLACK
	special Voyage_Depart
	release
	end

Voyage_EventScript_EnterCode::
	msgbox Voyage_Text_WhatsTheCode, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	special EnterCode
	waitstate
	special Voyage_CheckCode
	goto_if_eq VAR_RESULT, VOYAGE_DEST_NONE, Voyage_EventScript_WrongCode
	goto_if_eq VAR_0x8005, FALSE, Voyage_EventScript_KnownCode
	playfanfare MUS_OBTAIN_ITEM
	message Voyage_Text_NewCourse
	waitmessage
	waitfanfare
	msgbox Voyage_Text_AnyTime, MSGBOX_DEFAULT
	goto Voyage_EventScript_SailorMenu

Voyage_EventScript_KnownCode::
	msgbox Voyage_Text_KnownCode, MSGBOX_DEFAULT
	goto Voyage_EventScript_SailorMenu

Voyage_EventScript_WrongCode::
	msgbox Voyage_Text_WrongCode, MSGBOX_DEFAULT
	goto Voyage_EventScript_SailorMenu

Voyage_EventScript_SeasTooRough::
	msgbox Voyage_Text_SeasTooRough, MSGBOX_DEFAULT
	goto Voyage_EventScript_SailorMenu

Voyage_EventScript_Cancel::
	msgbox Voyage_Text_Cancel, MSGBOX_DEFAULT
	release
	end

Voyage_EventScript_SailorNotYet::
	msgbox Voyage_Text_SailorNotYet, MSGBOX_DEFAULT
	release
	end

Voyage_Text_SailorGreeting:
	.string "Ahoy! You're the new Champion, eh?\n"
	.string "The old boat's ready when you are.$"

Voyage_Text_WhereTo:
	.string "Where are we headed?$"

Voyage_Text_SetSailFor:
	.string "Set sail for {STR_VAR_1}?$"

Voyage_Text_CastOff:
	.string "Right! Hop in and hold on tight.$"

Voyage_Text_WhatsTheCode:
	.string "A passcode, eh? The sea keeps its\n"
	.string "secrets for those who know the words.$"

Voyage_Text_NewCourse:
	.string "{STR_VAR_1}…\n"
	.string "Now that's a course I know!$"

Voyage_Text_AnyTime:
	.string "I'll take you to {STR_VAR_1}\n"
	.string "whenever you like.$"

Voyage_Text_KnownCode:
	.string "That's the way to {STR_VAR_1}.\n"
	.string "We've charted that one already!$"

Voyage_Text_WrongCode:
	.string "Hmm… That doesn't ring a bell.\n"
	.string "No course I know answers to that.$"

Voyage_Text_SeasTooRough:
	.string "{STR_VAR_1}? The seas out that way\n"
	.string "are too rough just now.\p"
	.string "Come back later and we'll see\n"
	.string "if they've calmed down.$"

Voyage_Text_Cancel:
	.string "Fair winds, then. I'll be here.$"

Voyage_Text_SailorNotYet:
	.string "I used to sail to all sorts of\n"
	.string "strange islands, you know.\p"
	.string "Places you won't find on any map…\p"
	.string "But the open sea's no place for a\n"
	.string "rookie. Come back when you've\l"
	.string "beaten the Champion.$"

@ A voyage legendary fainted or fled (VAR_0x8004 = species, VAR_LAST_TALKED = its object): it disappears, and
@ Voyage_Depart brings it back on the next voyage to its island unless it was caught.
Voyage_EventScript_LegendaryGone::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	bufferspeciesname STR_VAR_1, VAR_0x8004
	msgbox Voyage_Text_LegendaryGone, MSGBOX_DEFAULT
	releaseall
	end

Voyage_Text_LegendaryGone:
	.string "{STR_VAR_1} vanished…\p"
	.string "Maybe it will be back on another\n"
	.string "voyage.$"
