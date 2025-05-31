LittlerootTown_MapScripts::
# 8 "data/maps/LittlerootTown/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, LittlerootTown_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

LittlerootTown_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 9 "data/maps/LittlerootTown/scripts.pory"
	compare VAR_PORT_TOSA_STATE, 0
	goto_if_eq LittlerootTown_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
	return

LittlerootTown_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 10 "data/maps/LittlerootTown/scripts.pory"
	setflag FLAG_HIDE_RESERVE_GATEKEEPER
	return


LittlerootTown_EventScript_ProfPalmSign::
# 16 "data/maps/LittlerootTown/scripts.pory"
	lockall
# 17 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_EventScript_ProfPalmSign_Text_0, MSGBOX_SIGN
# 18 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	return


LittlerootTown_EventScript_TrainerPermit::
# 22 "data/maps/LittlerootTown/scripts.pory"
	lockall
# 23 "data/maps/LittlerootTown/scripts.pory"
	setflag FLAG_ITEM_LITTLEROOT_TRAINER_PERMIT
# 24 "data/maps/LittlerootTown/scripts.pory"
	removeobject 3
# 25 "data/maps/LittlerootTown/scripts.pory"
	giveitem ITEM_TRAINER_PERMIT, 1
# 26 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end


LittlerootTown_EventScript_TestTrainer::
# 31 "data/maps/LittlerootTown/scripts.pory"
	trainerbattle_single TRAINER_TEST_TRAINER, Trainer_Intro, Trainer_Outro
# 32 "data/maps/LittlerootTown/scripts.pory"
	msgbox Trainer_PostBattle, MSGBOX_AUTOCLOSE
# 33 "data/maps/LittlerootTown/scripts.pory"
	waitmessage
	end


LittlerootTown_ProfPalmBag::
# 51 "data/maps/LittlerootTown/scripts.pory"
	lockall
# 52 "data/maps/LittlerootTown/scripts.pory"
	faceplayer
# 53 "data/maps/LittlerootTown/scripts.pory"
	goto_if_set FLAG_FOUNDSTARTER, LittlerootTown_ProfPalmBag_2
# 58 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_1, MSGBOX_DEFAULT
# 60 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_2, MSGBOX_YESNO
# 62 "data/maps/LittlerootTown/scripts.pory"
	compare VAR_RESULT, 1
	goto_if_eq LittlerootTown_ProfPalmBag_4
# 91 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_8
# 92 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end

LittlerootTown_ProfPalmBag_2:
# 54 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_0
# 55 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end

LittlerootTown_ProfPalmBag_4:
# 63 "data/maps/LittlerootTown/scripts.pory"
	playse SE_CONTEST_ICON_CLEAR
# 64 "data/maps/LittlerootTown/scripts.pory"
	waitse
# 65 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_3
# 66 "data/maps/LittlerootTown/scripts.pory"
	givemon SPECIES_FENNEKIN, 5, ITEM_ORAN_BERRY
# 67 "data/maps/LittlerootTown/scripts.pory"
	playfanfare MUS_OBTAIN_ITEM
# 68 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_4
# 69 "data/maps/LittlerootTown/scripts.pory"
	waitfanfare
# 70 "data/maps/LittlerootTown/scripts.pory"
	setflag FLAG_SYS_POKEMON_GET
# 71 "data/maps/LittlerootTown/scripts.pory"
	setflag FLAG_FOUNDSTARTER
# 73 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_5, MSGBOX_YESNO
# 74 "data/maps/LittlerootTown/scripts.pory"
	compare VAR_RESULT, 1
	goto_if_eq LittlerootTown_ProfPalmBag_7
# 85 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_7
# 86 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end

LittlerootTown_ProfPalmBag_7:
# 76 "data/maps/LittlerootTown/scripts.pory"
	setvar VAR_0x8004, 0
# 77 "data/maps/LittlerootTown/scripts.pory"
	fadescreen FADE_TO_BLACK
# 78 "data/maps/LittlerootTown/scripts.pory"
	special ChangePokemonNickname
# 79 "data/maps/LittlerootTown/scripts.pory"
	waitstate
# 80 "data/maps/LittlerootTown/scripts.pory"
	bufferpartymonnick 2, 0
# 81 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_ProfPalmBag_Text_6
# 82 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end


LittlerootTown_EventScript_Gatekeeper_CheckPermit::
# 99 "data/maps/LittlerootTown/scripts.pory"
	lockall
# 100 "data/maps/LittlerootTown/scripts.pory"
	faceplayer
# 104 "data/maps/LittlerootTown/scripts.pory"
	goto_if_set FLAG_RESERVE_GATE_OPEN, LittlerootTown_EventScript_Gatekeeper_CheckPermit_1
	checkitem ITEM_TRAINER_PERMIT
# 0 "data/maps/LittlerootTown/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq LittlerootTown_EventScript_Gatekeeper_CheckPermit_2
# 112 "data/maps/LittlerootTown/scripts.pory"
	goto_if_unset FLAG_SYS_POKEMON_GET, LittlerootTown_EventScript_Gatekeeper_CheckPermit_2
# 120 "data/maps/LittlerootTown/scripts.pory"
	setflag FLAG_RESERVE_GATE_OPEN
# 121 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_2, MSGBOX_AUTOCLOSE
# 122 "data/maps/LittlerootTown/scripts.pory"
	playse SE_PIN
# 123 "data/maps/LittlerootTown/scripts.pory"
	applymovement 4, LittlerootTown_EventScript_Gatekeeper_CheckPermit_Movement_0
# 126 "data/maps/LittlerootTown/scripts.pory"
	delay 20
# 127 "data/maps/LittlerootTown/scripts.pory"
	waitmovement 0
# 128 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_3, MSGBOX_AUTOCLOSE
# 130 "data/maps/LittlerootTown/scripts.pory"
	applymovement OBJ_EVENT_ID_PLAYER, LittlerootTown_EventScript_Gatekeeper_CheckPermit_Movement_1
# 134 "data/maps/LittlerootTown/scripts.pory"
	waitmovement 0
# 135 "data/maps/LittlerootTown/scripts.pory"
	applymovement 4, LittlerootTown_EventScript_Gatekeeper_CheckPermit_Movement_2
# 140 "data/maps/LittlerootTown/scripts.pory"
	waitmovement 4
# 141 "data/maps/LittlerootTown/scripts.pory"
	setvar VAR_PORT_TOSA_STATE, 1
# 142 "data/maps/LittlerootTown/scripts.pory"
	clearflag FLAG_HIDE_RESERVE_GATEKEEPER
# 144 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end

LittlerootTown_EventScript_Gatekeeper_CheckPermit_1:
# 105 "data/maps/LittlerootTown/scripts.pory"
	faceplayer
# 106 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_0
# 109 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end

LittlerootTown_EventScript_Gatekeeper_CheckPermit_2:
# 113 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_1, MSGBOX_DEFAULT
# 116 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end


LittlerootTown_EventScript_Gatekeeper_GateOpen::
# 151 "data/maps/LittlerootTown/scripts.pory"
	lockall
# 152 "data/maps/LittlerootTown/scripts.pory"
	faceplayer
# 153 "data/maps/LittlerootTown/scripts.pory"
	msgbox LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_0
# 156 "data/maps/LittlerootTown/scripts.pory"
	releaseall
	end


# 123 "data/maps/LittlerootTown/scripts.pory"
LittlerootTown_EventScript_Gatekeeper_CheckPermit_Movement_0:
# 124 "data/maps/LittlerootTown/scripts.pory"
	emote_exclamation_mark
	step_end

# 130 "data/maps/LittlerootTown/scripts.pory"
LittlerootTown_EventScript_Gatekeeper_CheckPermit_Movement_1:
# 131 "data/maps/LittlerootTown/scripts.pory"
	walk_right
# 132 "data/maps/LittlerootTown/scripts.pory"
	face_left
	step_end

# 135 "data/maps/LittlerootTown/scripts.pory"
LittlerootTown_EventScript_Gatekeeper_CheckPermit_Movement_2:
# 136 "data/maps/LittlerootTown/scripts.pory"
	walk_down
# 137 "data/maps/LittlerootTown/scripts.pory"
	walk_left
# 138 "data/maps/LittlerootTown/scripts.pory"
	face_down
	step_end

LittlerootTown_EventScript_ProfPalmSign_Text_0:
# 17 "data/maps/LittlerootTown/scripts.pory"
	.string "Professor Palm's Laboratory\n{COLOR LIGHT_GRAY}Driving Humans & Pokémon Forward$"

LittlerootTown_ProfPalmBag_Text_0:
# 54 "data/maps/LittlerootTown/scripts.pory"
	.string "There's nothing but empty papers in the\n"
	.string "bag.$"

LittlerootTown_ProfPalmBag_Text_1:
# 58 "data/maps/LittlerootTown/scripts.pory"
	.string "The professor has left a note on this\n"
	.string "bag...\p"
	.string "{COLOR GREEN}{PLAYER}, seeing as you won't have\n"
	.string "brought any Pokémon to Tosa with you\l"
	.string "I've left you with this Fennekin. I know\l"
	.string "that you'll take great care of it!$"

LittlerootTown_ProfPalmBag_Text_2:
# 60 "data/maps/LittlerootTown/scripts.pory"
	.string "You open the bag and find a Poké Ball.\p"
	.string "Do you want to take it?$"

LittlerootTown_ProfPalmBag_Text_3:
# 65 "data/maps/LittlerootTown/scripts.pory"
	.string "You take the Poké Ball.$"

LittlerootTown_ProfPalmBag_Text_4:
# 68 "data/maps/LittlerootTown/scripts.pory"
	.string "You received a Fennekin!$"

LittlerootTown_ProfPalmBag_Text_5:
# 73 "data/maps/LittlerootTown/scripts.pory"
	.string "Should I give Fennekin a nickname?$"

LittlerootTown_ProfPalmBag_Text_6:
# 81 "data/maps/LittlerootTown/scripts.pory"
	.string "{STR_VAR_2}...a perfect name.\p"
	.string "You close the bag.$"

LittlerootTown_ProfPalmBag_Text_7:
# 85 "data/maps/LittlerootTown/scripts.pory"
	.string "You decide not to give Fennekin a\n"
	.string "nickname and close the bag.$"

LittlerootTown_ProfPalmBag_Text_8:
# 91 "data/maps/LittlerootTown/scripts.pory"
	.string "You decide not to take the Poké Ball.$"

LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_0:
# 106 "data/maps/LittlerootTown/scripts.pory"
	.string "The Tosa Nature Reserve is a\n"
	.string "beautiful place, isn't it?\p"
	.string "Please take care of it while you're\n"
	.string "here!$"

LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_1:
# 113 "data/maps/LittlerootTown/scripts.pory"
	.string "Hey!\p"
	.string "You need a {COLOR GREEN}Trainer Permit{COLOR DARK_GRAY} to enter the\n"
	.string "nature reserve.$"

LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_2:
# 121 "data/maps/LittlerootTown/scripts.pory"
	.string "You flash your Trainer Permit...$"

LittlerootTown_EventScript_Gatekeeper_CheckPermit_Text_3:
# 128 "data/maps/LittlerootTown/scripts.pory"
	.string "Ah! That's a {COLOR GREEN}Trainer Permit{COLOR DARK_GRAY}!\n"
	.string "Go on through.$"

Trainer_Intro::
# 37 "data/maps/LittlerootTown/scripts.pory"
	.string "Ugh..I'm totally lost! Might as well stop\nfor a battle!$"

Trainer_Outro::
# 41 "data/maps/LittlerootTown/scripts.pory"
	.string "I've totally lost my way...$"

Trainer_PostBattle::
# 45 "data/maps/LittlerootTown/scripts.pory"
	.string "Make sure you pay close attention to\nyour map.\p"
	.string "The nature reserve is a big place!$"
