# 1 "data/maps/TelokTown/scripts.pory"

# 2 "data/maps/TelokTown/scripts.pory"
TelokTown_MapScripts::
# 3 "data/maps/TelokTown/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, TelokTown_OnTransition
# 4 "data/maps/TelokTown/scripts.pory"
	.byte 0
# 5 "data/maps/TelokTown/scripts.pory"

# 6 "data/maps/TelokTown/scripts.pory"
TelokTown_OnTransition:
# 7 "data/maps/TelokTown/scripts.pory"
	setflag FLAG_VISITED_TELOK_TOWN
# 8 "data/maps/TelokTown/scripts.pory"
	call_if_ne VAR_TELOK_TOWN_STATE, 0, TelokTown_EventScript_HideAide
# 9 "data/maps/TelokTown/scripts.pory"
	end
# 10 "data/maps/TelokTown/scripts.pory"

# 11 "data/maps/TelokTown/scripts.pory"
@ The aide has gone into Palm Labs; FLAG_TEMP_1 is the aide's hide flag (temp flags reset on every map load)
# 12 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_HideAide:
# 13 "data/maps/TelokTown/scripts.pory"
	setflag FLAG_TEMP_1
# 14 "data/maps/TelokTown/scripts.pory"
	return
# 15 "data/maps/TelokTown/scripts.pory"

# 16 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_TownSign::
# 17 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_Text_TownSign, MSGBOX_SIGN
# 18 "data/maps/TelokTown/scripts.pory"
	end
# 19 "data/maps/TelokTown/scripts.pory"

# 20 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_ExistentialMan::
# 21 "data/maps/TelokTown/scripts.pory"
	lock
# 22 "data/maps/TelokTown/scripts.pory"
	faceplayer
# 23 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_Text_SavingMyProgress, MSGBOX_NPC
# 24 "data/maps/TelokTown/scripts.pory"
	delay 60
# 25 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_Text_WaitWhat, MSGBOX_NPC
# 26 "data/maps/TelokTown/scripts.pory"
	release
# 27 "data/maps/TelokTown/scripts.pory"
	end
# 28 "data/maps/TelokTown/scripts.pory"

# 29 "data/maps/TelokTown/scripts.pory"
TelokTown_Text_SavingMyProgress:
# 30 "data/maps/TelokTown/scripts.pory"
	.string "I want to take a rest, so I'm saving my\n"
# 31 "data/maps/TelokTown/scripts.pory"
	.string "progress.$"
# 32 "data/maps/TelokTown/scripts.pory"

# 33 "data/maps/TelokTown/scripts.pory"
TelokTown_Text_WaitWhat:
# 34 "data/maps/TelokTown/scripts.pory"
	.string "Wait, what am I talking about?$"
# 35 "data/maps/TelokTown/scripts.pory"

# 36 "data/maps/TelokTown/scripts.pory"
TelokTown_Text_TownSign:
# 37 "data/maps/TelokTown/scripts.pory"
	.string "Telok Town\n"
# 38 "data/maps/TelokTown/scripts.pory"
	.string "“Where new journeys take root.”$"

TelokTown_EventScript_HideSeekBoy::
# 42 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_EventScript_HideSeekBoy_Text_0, MSGBOX_NPC
# 43 "data/maps/TelokTown/scripts.pory"
	release
	end


TelokTown_EventScript_HideSeekLady::
# 48 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_EventScript_HideSeekLady_Text_0, MSGBOX_NPC
# 49 "data/maps/TelokTown/scripts.pory"
	release
	end


TelokTown_EventScript_ProfessorGuy::
# 54 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_EventScript_ProfessorGuy_Text_0, MSGBOX_NPC
# 55 "data/maps/TelokTown/scripts.pory"
	release
	end


TelokTown_EventScript_AideTrigger_NoStep::
# 68 "data/maps/TelokTown/scripts.pory"
	lockall
# 69 "data/maps/TelokTown/scripts.pory"
	call TelokTown_EventScript_AideNotices
# 70 "data/maps/TelokTown/scripts.pory"
	goto TelokTown_EventScript_AideLeadsToLab
	return


TelokTown_EventScript_AideTrigger_StepUp::
# 74 "data/maps/TelokTown/scripts.pory"
	lockall
# 75 "data/maps/TelokTown/scripts.pory"
	call TelokTown_EventScript_AideNotices
# 76 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideTrigger_StepUp_Movement_0
# 77 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 78 "data/maps/TelokTown/scripts.pory"
	goto TelokTown_EventScript_AideLeadsToLab
	return


TelokTown_EventScript_Aide::
# 82 "data/maps/TelokTown/scripts.pory"
	lockall
# 83 "data/maps/TelokTown/scripts.pory"
	faceplayer
# 84 "data/maps/TelokTown/scripts.pory"
	playse SE_PIN
# 85 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_TELOK_AIDE, TelokTown_EventScript_Aide_Movement_0
# 86 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 87 "data/maps/TelokTown/scripts.pory"
	delay 24
# 88 "data/maps/TelokTown/scripts.pory"
	goto TelokTown_EventScript_AideLeadsToLab
	return


TelokTown_EventScript_AideNotices::
# 92 "data/maps/TelokTown/scripts.pory"
	playse SE_PIN
# 93 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideNotices_Movement_0
# 94 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_TELOK_AIDE, TelokTown_EventScript_AideNotices_Movement_1
# 95 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 96 "data/maps/TelokTown/scripts.pory"
	delay 24
	return


TelokTown_EventScript_AideLeadsToLab::
# 101 "data/maps/TelokTown/scripts.pory"
	msgbox TelokTown_EventScript_AideLeadsToLab_Text_0, MSGBOX_DEFAULT
# 102 "data/maps/TelokTown/scripts.pory"
	closemessage
# 105 "data/maps/TelokTown/scripts.pory"
	getplayerxy VAR_TEMP_1, VAR_TEMP_2
# 106 "data/maps/TelokTown/scripts.pory"
	compare VAR_TEMP_2, 8
	goto_if_eq TelokTown_EventScript_AideLeadsToLab_2
# 108 "data/maps/TelokTown/scripts.pory"
	compare VAR_TEMP_1, 18
	goto_if_eq TelokTown_EventScript_AideLeadsToLab_3
# 111 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideLeadsToLab_Movement_2
TelokTown_EventScript_AideLeadsToLab_1:
# 113 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 114 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_TELOK_AIDE, TelokTown_EventScript_AideLeadsToLab_Movement_1
# 115 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 118 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_TELOK_AIDE, TelokTown_EventScript_AideLeadsToLab_Movement_3
# 119 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideLeadsToLab_Movement_4
# 120 "data/maps/TelokTown/scripts.pory"
	waitmovement LOCALID_TELOK_AIDE
# 121 "data/maps/TelokTown/scripts.pory"
	waitmovement LOCALID_PLAYER
# 124 "data/maps/TelokTown/scripts.pory"
	opendoor 31, 6
# 125 "data/maps/TelokTown/scripts.pory"
	waitdooranim
# 126 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_TELOK_AIDE, TelokTown_EventScript_AideLeadsToLab_Movement_5
# 127 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 128 "data/maps/TelokTown/scripts.pory"
	removeobject LOCALID_TELOK_AIDE
# 129 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideLeadsToLab_Movement_6
# 130 "data/maps/TelokTown/scripts.pory"
	waitmovement 0
# 131 "data/maps/TelokTown/scripts.pory"
	closedoor 31, 6
# 132 "data/maps/TelokTown/scripts.pory"
	waitdooranim
# 133 "data/maps/TelokTown/scripts.pory"
	setvar VAR_TELOK_TOWN_STATE, 1
# 134 "data/maps/TelokTown/scripts.pory"
	warp MAP_TELOK_TOWN_PALM_LABS, 6, 12
	return

TelokTown_EventScript_AideLeadsToLab_2:
# 107 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideLeadsToLab_Movement_0
	goto TelokTown_EventScript_AideLeadsToLab_1

TelokTown_EventScript_AideLeadsToLab_3:
# 109 "data/maps/TelokTown/scripts.pory"
	applymovement LOCALID_PLAYER, TelokTown_EventScript_AideLeadsToLab_Movement_1
	goto TelokTown_EventScript_AideLeadsToLab_1


# 76 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideTrigger_StepUp_Movement_0:
# 76 "data/maps/TelokTown/scripts.pory"
	walk_up
	step_end

# 85 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_Aide_Movement_0:
# 85 "data/maps/TelokTown/scripts.pory"
	emote_exclamation_mark
	step_end

# 93 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideNotices_Movement_0:
# 93 "data/maps/TelokTown/scripts.pory"
	face_up
	step_end

# 94 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideNotices_Movement_1:
# 94 "data/maps/TelokTown/scripts.pory"
	emote_exclamation_mark
# 94 "data/maps/TelokTown/scripts.pory"
	face_down
	step_end

# 107 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_0:
# 107 "data/maps/TelokTown/scripts.pory"
	walk_left
# 107 "data/maps/TelokTown/scripts.pory"
	walk_down
# 107 "data/maps/TelokTown/scripts.pory"
	walk_down
# 107 "data/maps/TelokTown/scripts.pory"
	face_right
	step_end

# 109 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_1:
# 109 "data/maps/TelokTown/scripts.pory"
	walk_down
# 109 "data/maps/TelokTown/scripts.pory"
	face_right
	step_end

# 111 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_2:
# 111 "data/maps/TelokTown/scripts.pory"
	walk_left
# 111 "data/maps/TelokTown/scripts.pory"
	face_right
	step_end

# 118 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_3:
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_up
# 118 "data/maps/TelokTown/scripts.pory"
	walk_up
# 118 "data/maps/TelokTown/scripts.pory"
	walk_up
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
# 118 "data/maps/TelokTown/scripts.pory"
	walk_right
	step_end

# 119 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_4:
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_up
# 119 "data/maps/TelokTown/scripts.pory"
	walk_up
# 119 "data/maps/TelokTown/scripts.pory"
	walk_up
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
# 119 "data/maps/TelokTown/scripts.pory"
	walk_right
	step_end

# 126 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_5:
# 126 "data/maps/TelokTown/scripts.pory"
	walk_up
# 126 "data/maps/TelokTown/scripts.pory"
	set_invisible
	step_end

# 129 "data/maps/TelokTown/scripts.pory"
TelokTown_EventScript_AideLeadsToLab_Movement_6:
# 129 "data/maps/TelokTown/scripts.pory"
	walk_right
# 129 "data/maps/TelokTown/scripts.pory"
	walk_up
# 129 "data/maps/TelokTown/scripts.pory"
	set_invisible
	step_end

TelokTown_EventScript_HideSeekBoy_Text_0:
# 42 "data/maps/TelokTown/scripts.pory"
	.string "I'm playing hide and seek with a-ma!\n"
	.string "She's really good at hiding...$"

TelokTown_EventScript_HideSeekLady_Text_0:
# 48 "data/maps/TelokTown/scripts.pory"
	.string "I'm sure I left my glasses around here\n"
	.string "somewhere... I can't see a thing without\l"
	.string "them!$"

TelokTown_EventScript_ProfessorGuy_Text_0:
# 54 "data/maps/TelokTown/scripts.pory"
	.string "Other than researchers visiting the\n"
	.string "professor's lab, Telok Town is a\l"
	.string "peaceful place.$"

TelokTown_EventScript_AideLeadsToLab_Text_0:
# 101 "data/maps/TelokTown/scripts.pory"
	.string "Ah, you must be {PLAYER}. Professor\n"
	.string "Palm told me you were coming. If you\l"
	.string "just follow me...$"
