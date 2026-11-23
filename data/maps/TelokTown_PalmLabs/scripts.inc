# 1 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 2 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_MapScripts::
# 3 "data/maps/TelokTown_PalmLabs/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TelokTown_PalmLabs_OnTransition
# 4 "data/maps/TelokTown_PalmLabs/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TelokTown_PalmLabs_OnFrame
# 5 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.byte 0
# 6 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 7 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_OnTransition:
# 8 "data/maps/TelokTown_PalmLabs/scripts.pory"
	call Common_EventScript_SetupRivalGfxId
# 9 "data/maps/TelokTown_PalmLabs/scripts.pory"
	special FieldGrayscaleOff
# 10 "data/maps/TelokTown_PalmLabs/scripts.pory"
	call_if_eq VAR_TELOK_TOWN_STATE, 0, TelokTown_PalmLabs_EventScript_HideAide
# 11 "data/maps/TelokTown_PalmLabs/scripts.pory"
	call_if_eq VAR_TELOK_TOWN_STATE, 1, TelokTown_PalmLabs_EventScript_AideAtDoor
# 12 "data/maps/TelokTown_PalmLabs/scripts.pory"
	call_if_eq VAR_TELOK_TOWN_STATE, 3, TelokTown_PalmLabs_EventScript_ProfFacesPlayer
# 13 "data/maps/TelokTown_PalmLabs/scripts.pory"
	end
# 14 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 15 "data/maps/TelokTown_PalmLabs/scripts.pory"
@ Aide is still waiting outside in Telok Town
# 16 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_HideAide:
# 17 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setflag FLAG_TEMP_1
# 18 "data/maps/TelokTown_PalmLabs/scripts.pory"
	return
# 19 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 20 "data/maps/TelokTown_PalmLabs/scripts.pory"
@ Walking in with the player: aide starts just inside the door, one tile ahead
# 21 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_AideAtDoor:
# 22 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setobjectxyperm LOCALID_PALM_LABS_AIDE, 6, 11
# 23 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setobjectmovementtype LOCALID_PALM_LABS_AIDE, MOVEMENT_TYPE_FACE_UP
# 24 "data/maps/TelokTown_PalmLabs/scripts.pory"
	return
# 25 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 26 "data/maps/TelokTown_PalmLabs/scripts.pory"
@ Back from the flashback: the professor is still turned towards the player
# 27 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_ProfFacesPlayer:
# 28 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setobjectmovementtype LOCALID_PALM_LABS_PROF, MOVEMENT_TYPE_FACE_DOWN
# 29 "data/maps/TelokTown_PalmLabs/scripts.pory"
	return
# 30 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 31 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_OnFrame:
# 32 "data/maps/TelokTown_PalmLabs/scripts.pory"
	map_script_2 VAR_TELOK_TOWN_STATE, 1, TelokTown_PalmLabs_EventScript_AideIntro
# 33 "data/maps/TelokTown_PalmLabs/scripts.pory"
	map_script_2 VAR_TELOK_TOWN_STATE, 3, TelokTown_PalmLabs_EventScript_ProfBriefing
# 34 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.2byte 0
# 35 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 36 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_Machine::
# 37 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_Text_SeriousLookingMachine, MSGBOX_SIGN
# 38 "data/maps/TelokTown_PalmLabs/scripts.pory"
	end
# 39 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 40 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_PC::
# 41 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_Text_PCUsedForResearch, MSGBOX_SIGN
# 42 "data/maps/TelokTown_PalmLabs/scripts.pory"
	end
# 43 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 44 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_Bookshelf::
# 45 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_Text_CrammedWithBooksOnPokemon, MSGBOX_SIGN
# 46 "data/maps/TelokTown_PalmLabs/scripts.pory"
	end
# 47 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 48 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_Book::
# 49 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_Text_InterestingBook, MSGBOX_SIGN
# 50 "data/maps/TelokTown_PalmLabs/scripts.pory"
	end
# 51 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 52 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_Text_SeriousLookingMachine:
# 53 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "It's a serious-looking machine.\n"
# 54 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "The Professor must use this for research.$"
# 55 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 56 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_Text_PCUsedForResearch:
# 57 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "It's a PC used for research.\n"
# 58 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Best leave it be.$"
# 59 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 60 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_Text_CrammedWithBooksOnPokemon:
# 61 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "It's crammed with books on Pokémon habitats.$"
# 62 "data/maps/TelokTown_PalmLabs/scripts.pory"

# 63 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_Text_InterestingBook:
# 64 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "This book on Pokémon migration\n"
# 65 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "seems fascinating...$"

TelokTown_PalmLabs_EventScript_AideIntro::
# 76 "data/maps/TelokTown_PalmLabs/scripts.pory"
	lockall
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_AIDE, TelokTown_PalmLabs_EventScript_AideIntro_Movement_0
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_PalmLabs_EventScript_AideIntro_Movement_1
# 79 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement LOCALID_PALM_LABS_AIDE
# 80 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement LOCALID_PLAYER
# 82 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_AideIntro_Text_0, MSGBOX_DEFAULT
# 83 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 84 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playse SE_PIN
# 85 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_PROF, TelokTown_PalmLabs_EventScript_AideIntro_Movement_2
# 86 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 87 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_AIDE, TelokTown_PalmLabs_EventScript_AideIntro_Movement_3
# 88 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 89 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_AideIntro_Text_1, MSGBOX_DEFAULT
# 90 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_AIDE, TelokTown_PalmLabs_EventScript_AideIntro_Movement_4
# 92 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 93 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setobjectxyperm LOCALID_PALM_LABS_AIDE, 4, 9
# 94 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setobjectmovementtype LOCALID_PALM_LABS_AIDE, MOVEMENT_TYPE_FACE_DOWN
# 96 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_AideIntro_Text_2, MSGBOX_DEFAULT
# 97 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 98 "data/maps/TelokTown_PalmLabs/scripts.pory"
	delay 20
# 99 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setvar VAR_TELOK_TOWN_STATE, 2
# 100 "data/maps/TelokTown_PalmLabs/scripts.pory"
	warp MAP_TELOK_TOWN_PALM_LABS_FLASHBACK, 12, 14
	return


TelokTown_PalmLabs_EventScript_ProfBriefing::
# 105 "data/maps/TelokTown_PalmLabs/scripts.pory"
	lockall
# 106 "data/maps/TelokTown_PalmLabs/scripts.pory"
	delay 20
# 107 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_ProfBriefing_Text_0, MSGBOX_DEFAULT
# 109 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 110 "data/maps/TelokTown_PalmLabs/scripts.pory"
	message TelokTown_PalmLabs_EventScript_ProfBriefing_Text_1
# 111 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmessage
# 112 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitfanfare
# 113 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setflag FLAG_SYS_POKEDEX_GET
# 114 "data/maps/TelokTown_PalmLabs/scripts.pory"
	special SetUnlockedPokedexFlags
# 115 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setflag FLAG_RECEIVED_POKEDEX_FROM_BIRCH
# 116 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setvar VAR_CABLE_CLUB_TUTORIAL_STATE, 1
# 118 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_ProfBriefing_Text_2, MSGBOX_DEFAULT
# 119 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 122 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_PROF, TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_0
# 123 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playse SE_CLICK
# 124 "data/maps/TelokTown_PalmLabs/scripts.pory"
	delay 10
# 125 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playse SE_RG_BAG_POCKET
# 126 "data/maps/TelokTown_PalmLabs/scripts.pory"
	delay 14
# 127 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playse SE_SWITCH
# 128 "data/maps/TelokTown_PalmLabs/scripts.pory"
	delay 10
# 129 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playse SE_CLICK
# 130 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 131 "data/maps/TelokTown_PalmLabs/scripts.pory"
	delay 24
# 132 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playse SE_POKENAV_ON
# 133 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitse
# 134 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setflag FLAG_SYS_POKENAV_GET
# 135 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setflag FLAG_SYS_PHONE_ACTIVE
# 137 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_ProfBriefing_Text_3, MSGBOX_DEFAULT
# 138 "data/maps/TelokTown_PalmLabs/scripts.pory"
	playfanfare MUS_REGISTER_MATCH_CALL
# 139 "data/maps/TelokTown_PalmLabs/scripts.pory"
	message TelokTown_PalmLabs_EventScript_ProfBriefing_Text_4
# 140 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmessage
# 141 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitfanfare
# 142 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setflag FLAG_ENABLE_PROF_PALM_MATCH_CALL
# 143 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_1
# 147 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 148 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_PROF, TelokTown_PalmLabs_EventScript_AideIntro_Movement_3
# 149 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 150 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_ProfBriefing_Text_5, MSGBOX_DEFAULT
# 151 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 152 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_PROF, TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_2
# 153 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 154 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setobjectmovementtype LOCALID_PALM_LABS_PROF, MOVEMENT_TYPE_FACE_RIGHT
# 155 "data/maps/TelokTown_PalmLabs/scripts.pory"
	setvar VAR_TELOK_TOWN_STATE, 4
# 156 "data/maps/TelokTown_PalmLabs/scripts.pory"
	releaseall
	return


TelokTown_PalmLabs_EventScript_Prof::
# 160 "data/maps/TelokTown_PalmLabs/scripts.pory"
	lock
# 161 "data/maps/TelokTown_PalmLabs/scripts.pory"
	faceplayer
# 162 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Prof_Text_0, MSGBOX_DEFAULT
# 163 "data/maps/TelokTown_PalmLabs/scripts.pory"
	closemessage
# 164 "data/maps/TelokTown_PalmLabs/scripts.pory"
	applymovement LOCALID_PALM_LABS_PROF, TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_2
# 165 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmovement 0
# 166 "data/maps/TelokTown_PalmLabs/scripts.pory"
	release
	return


TelokTown_PalmLabs_EventScript_Aide::
# 171 "data/maps/TelokTown_PalmLabs/scripts.pory"
	lock
# 172 "data/maps/TelokTown_PalmLabs/scripts.pory"
	faceplayer
# 173 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Aide_Text_0, MSGBOX_DEFAULT
TelokTown_PalmLabs_EventScript_Aide_2:
# 175 "data/maps/TelokTown_PalmLabs/scripts.pory"
	message TelokTown_PalmLabs_EventScript_Aide_Text_1
# 176 "data/maps/TelokTown_PalmLabs/scripts.pory"
	waitmessage
# 177 "data/maps/TelokTown_PalmLabs/scripts.pory"
	dynmultichoice 19, 1, FALSE, 5, 0, DYN_MULTICHOICE_CB_NONE, TelokTown_PalmLabs_EventScript_Aide_Text_2, TelokTown_PalmLabs_EventScript_Aide_Text_3, TelokTown_PalmLabs_EventScript_Aide_Text_4, TelokTown_PalmLabs_EventScript_Aide_Text_5, TelokTown_PalmLabs_EventScript_Aide_Text_6
# 178 "data/maps/TelokTown_PalmLabs/scripts.pory"
	compare VAR_RESULT, 4
	goto_if_eq TelokTown_PalmLabs_EventScript_Aide_5
# 178 "data/maps/TelokTown_PalmLabs/scripts.pory"
	compare VAR_RESULT, MULTI_B_PRESSED
	goto_if_eq TelokTown_PalmLabs_EventScript_Aide_5
# 181 "data/maps/TelokTown_PalmLabs/scripts.pory"
	switch VAR_RESULT
# 182 "data/maps/TelokTown_PalmLabs/scripts.pory"
	case 0, TelokTown_PalmLabs_EventScript_Aide_10
# 184 "data/maps/TelokTown_PalmLabs/scripts.pory"
	case 1, TelokTown_PalmLabs_EventScript_Aide_11
# 186 "data/maps/TelokTown_PalmLabs/scripts.pory"
	case 2, TelokTown_PalmLabs_EventScript_Aide_12
# 188 "data/maps/TelokTown_PalmLabs/scripts.pory"
	case 3, TelokTown_PalmLabs_EventScript_Aide_13
	goto TelokTown_PalmLabs_EventScript_Aide_2

TelokTown_PalmLabs_EventScript_Aide_1:
# 192 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Aide_Text_11, MSGBOX_DEFAULT
# 193 "data/maps/TelokTown_PalmLabs/scripts.pory"
	release
	return

TelokTown_PalmLabs_EventScript_Aide_5:
	goto TelokTown_PalmLabs_EventScript_Aide_1

TelokTown_PalmLabs_EventScript_Aide_10:
# 183 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Aide_Text_7, MSGBOX_DEFAULT
	goto TelokTown_PalmLabs_EventScript_Aide_2

TelokTown_PalmLabs_EventScript_Aide_11:
# 185 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Aide_Text_8, MSGBOX_DEFAULT
	goto TelokTown_PalmLabs_EventScript_Aide_2

TelokTown_PalmLabs_EventScript_Aide_12:
# 187 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Aide_Text_9, MSGBOX_DEFAULT
	goto TelokTown_PalmLabs_EventScript_Aide_2

TelokTown_PalmLabs_EventScript_Aide_13:
# 189 "data/maps/TelokTown_PalmLabs/scripts.pory"
	msgbox TelokTown_PalmLabs_EventScript_Aide_Text_10, MSGBOX_DEFAULT
	goto TelokTown_PalmLabs_EventScript_Aide_2


# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_AideIntro_Movement_0:
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 77 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_up
	step_end

# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_AideIntro_Movement_1:
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_right
# 78 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_up
	step_end

# 85 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_AideIntro_Movement_2:
# 85 "data/maps/TelokTown_PalmLabs/scripts.pory"
	emote_exclamation_mark
# 85 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_down
	step_end

# 87 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_AideIntro_Movement_3:
# 87 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_left
	step_end

# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_AideIntro_Movement_4:
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_down
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 91 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_down
	step_end

# 122 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_0:
# 122 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_in_place_faster_down
	step_end

# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_1:
# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_left
# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
	walk_up
# 146 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_right
	step_end

# 152 "data/maps/TelokTown_PalmLabs/scripts.pory"
TelokTown_PalmLabs_EventScript_ProfBriefing_Movement_2:
# 152 "data/maps/TelokTown_PalmLabs/scripts.pory"
	face_right
	step_end

TelokTown_PalmLabs_EventScript_AideIntro_Text_0:
# 82 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Palm? {PLAYER} is here to see you.$"

TelokTown_PalmLabs_EventScript_AideIntro_Text_1:
# 89 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "{PLAYER}, this is the esteemed\n"
	.string "Professor Palm. I'll leave you both to\l"
	.string "it.$"

TelokTown_PalmLabs_EventScript_AideIntro_Text_2:
# 96 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Welcome to Tosa, {PLAYER}! It's great\n"
	.string "to see you again, it's been months since\l"
	.string "my conference back in Galar, hasn't it!\p"
	.string "I deeply appreciate you offering to\n"
	.string "come all the way out here to assist our\l"
	.string "work. People who share my enthusiasm\l"
	.string "for Pokémon habitats are few and far\l"
	.string "between these days...$"

TelokTown_PalmLabs_EventScript_ProfBriefing_Text_0:
# 107 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "I need you to travel the Tosa region\n"
	.string "and collect as much data as you can\l"
	.string "about species diversity across the\l"
	.string "region.\p"
	.string "My team here will analyse the data you\n"
	.string "send back, and hopefully we'll be able\l"
	.string "to help the Tosa League plan better for\l"
	.string "the future.\p"
	.string "I fear for what will happen if we don't\n"
	.string "strike while the iron's hot.\p"
	.string "Anyway, you know all of this so I'll cut\n"
	.string "right to it: we've prepared a\l"
	.string "customised Pokédex that'll interface\l"
	.string "with our servers here.$"

TelokTown_PalmLabs_EventScript_ProfBriefing_Text_1:
# 110 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "{PLAYER} received the Pokédex!$"

TelokTown_PalmLabs_EventScript_ProfBriefing_Text_2:
# 118 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Unlike Galar, we don't rely on Pokémon\n"
	.string "for transport, {PLAYER}. There's a\l"
	.string "metro station beneath Tosa Port that'll\l"
	.string "take you to Timah Town.\p"
	.string "You've brought your Rotom Phone with\n"
	.string "you, right? One second...$"

TelokTown_PalmLabs_EventScript_ProfBriefing_Text_3:
# 137 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "There, I've given you access to our\n"
	.string "research network. You should be able to\l"
	.string "make calls across the Tosa region.\p"
	.string "I'll also give you my number so you can\n"
	.string "call me anytime.$"

TelokTown_PalmLabs_EventScript_ProfBriefing_Text_4:
# 139 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Registered Prof. Palm in the Rotom\n"
	.string "Phone.$"

TelokTown_PalmLabs_EventScript_ProfBriefing_Text_5:
# 150 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "My assistant should be able to answer\n"
	.string "any questions you have, I've got to get\l"
	.string "back to work.\p"
	.string "We'll speak soon {PLAYER}, and thank\n"
	.string "you!$"

TelokTown_PalmLabs_EventScript_Prof_Text_0:
# 162 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "I've got to get back to work,\n"
	.string "{PLAYER}. My assistant can answer\l"
	.string "any questions you have!$"

TelokTown_PalmLabs_EventScript_Aide_Text_0:
# 173 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Palm has asked me to answer any\n"
	.string "questions you may have, so please do!$"

TelokTown_PalmLabs_EventScript_Aide_Text_1:
# 175 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "What would you like to know?$"

TelokTown_PalmLabs_EventScript_Aide_Text_2:
# 177 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Region$"

TelokTown_PalmLabs_EventScript_Aide_Text_3:
# 177 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "License$"

TelokTown_PalmLabs_EventScript_Aide_Text_4:
# 177 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Tosa Reserve$"

TelokTown_PalmLabs_EventScript_Aide_Text_5:
# 177 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Metro$"

TelokTown_PalmLabs_EventScript_Aide_Text_6:
# 177 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Bye!$"

TelokTown_PalmLabs_EventScript_Aide_Text_7:
# 183 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "The Tosa region is mostly tropical, with\n"
	.string "steep mountains to the north.\p"
	.string "Being so close to Hoenn, it used to be\n"
	.string "really popular with tourists from there.\l"
	.string "Over the years, though, their numbers\l"
	.string "have dwindled.$"

TelokTown_PalmLabs_EventScript_Aide_Text_8:
# 185 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Because of the dramatic changes in\n"
	.string "Pokémon populations, the Tosa League\l"
	.string "has put tiered restrictions on\l"
	.string "Trainers.\p"
	.string "Trainers can certify at eight different\n"
	.string "ranks, and each Badge you earn gives\l"
	.string "you a bit more flexibility.\p"
	.string "The hope is that it'll encourage more\n"
	.string "responsible, measured approaches to\l"
	.string "training Pokémon... though I don't have\l"
	.string "much hope, to be honest.$"

TelokTown_PalmLabs_EventScript_Aide_Text_9:
# 187 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "The Reserve has been part of the island\n"
	.string "since it was founded. It's meant to\l"
	.string "preserve the unique ecosystems of the\l"
	.string "region.\p"
	.string "Over the decades, though, development\n"
	.string "has slowly encroached on it and eroded\l"
	.string "it away.\p"
	.string "We're trying to prove that this will lead\n"
	.string "to the collapse of the Tosa region's\l"
	.string "delicate habitats. That's why you're\l"
	.string "here!$"

TelokTown_PalmLabs_EventScript_Aide_Text_10:
# 189 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "Very few people are certified to the\n"
	.string "level where they can ride their Pokémon,\l"
	.string "so everyone relies on public transport\l"
	.string "here.\p"
	.string "The metro will get you around most of\n"
	.string "the region in a flash. Trains run\l"
	.string "non-stop!$"

TelokTown_PalmLabs_EventScript_Aide_Text_11:
# 192 "data/maps/TelokTown_PalmLabs/scripts.pory"
	.string "If you need any clarification, you can\n"
	.string "ask me anytime, {PLAYER}.$"
