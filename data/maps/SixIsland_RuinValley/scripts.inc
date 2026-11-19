SixIsland_RuinValley_MapScripts::
# 2 "data/maps/SixIsland_RuinValley/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_LOAD
# 7 "data/maps/SixIsland_RuinValley/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_LOAD:
# 3 "data/maps/SixIsland_RuinValley/scripts.pory"
	goto_if_set FLAG_SEVII_DOTTED_HOLE_OPEN, SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_LOAD_1
	return

SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_LOAD_1:
# 4 "data/maps/SixIsland_RuinValley/scripts.pory"
	setmetatile 24, 24, METATILE_SeviiIslands_DottedDoor_Open, FALSE
	return

SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 8 "data/maps/SixIsland_RuinValley/scripts.pory"
	goto_if_set FLAG_SEVII_DOTTED_HOLE_OPEN, SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
	return

SixIsland_RuinValley_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 9 "data/maps/SixIsland_RuinValley/scripts.pory"
	setobjectxyperm LOCALID_RUIN_VALLEY_SCIENTIST, 26, 25
# 10 "data/maps/SixIsland_RuinValley/scripts.pory"
	setobjectmovementtype LOCALID_RUIN_VALLEY_SCIENTIST, MOVEMENT_TYPE_FACE_LEFT
	return


SixIsland_RuinValley_EventScript_Scientist::
# 16 "data/maps/SixIsland_RuinValley/scripts.pory"
	goto_if_set FLAG_SEVII_DOTTED_HOLE_OPEN, SixIsland_RuinValley_EventScript_Scientist_1
# 19 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_EventScript_Scientist_Text_1, MSGBOX_NPC
	return

SixIsland_RuinValley_EventScript_Scientist_1:
# 17 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_EventScript_Scientist_Text_0, MSGBOX_NPC
	return


SixIsland_RuinValley_EventScript_Stanly::
# 24 "data/maps/SixIsland_RuinValley/scripts.pory"
	trainerbattle_single TRAINER_SEVII_STANLY, SixIsland_RuinValley_Text_StanlyIntro, SixIsland_RuinValley_Text_StanlyDefeat
# 25 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_Text_StanlyPost, MSGBOX_AUTOCLOSE
	return


SixIsland_RuinValley_EventScript_Foster::
# 41 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_EventScript_Foster_Text_0, MSGBOX_NPC
	return


SixIsland_RuinValley_EventScript_Larry::
# 45 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_EventScript_Larry_Text_0, MSGBOX_NPC
	return


SixIsland_RuinValley_EventScript_Daryl::
# 49 "data/maps/SixIsland_RuinValley/scripts.pory"
	trainerbattle_single TRAINER_SEVII_DARYL, SixIsland_RuinValley_Text_DarylIntro, SixIsland_RuinValley_Text_DarylDefeat
# 50 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_Text_DarylPost, MSGBOX_AUTOCLOSE
	return


SixIsland_RuinValley_EventScript_Hector::
# 66 "data/maps/SixIsland_RuinValley/scripts.pory"
	trainerbattle_single TRAINER_SEVII_HECTOR, SixIsland_RuinValley_Text_HectorIntro, SixIsland_RuinValley_Text_HectorDefeat
# 67 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_Text_HectorPost, MSGBOX_AUTOCLOSE
	return


SixIsland_RuinValley_EventScript_DottedHoleDoor::
# 83 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_EventScript_DottedHoleDoor_Text_0, MSGBOX_SIGN
	return


SixIsland_RuinValley_EventScript_Sealed::
# 88 "data/maps/SixIsland_RuinValley/scripts.pory"
	goto_if_set FLAG_SEVII_DOTTED_HOLE_OPEN, SixIsland_RuinValley_EventScript_Sealed_2
# 91 "data/maps/SixIsland_RuinValley/scripts.pory"
	msgbox SixIsland_RuinValley_EventScript_DottedHoleDoor_Text_0, MSGBOX_SIGN
	return

SixIsland_RuinValley_EventScript_Sealed_2:
	end


SixIsland_RuinValley_EventScript_Scientist_Text_0:
# 17 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "The dotted door finally opened! I only\n"
	.string "hope what's down there is friendly.$"

SixIsland_RuinValley_EventScript_Scientist_Text_1:
# 19 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "That dotted door is a puzzle from\n"
	.string "ancient times. I've studied it for years\l"
	.string "with no luck.$"

SixIsland_RuinValley_EventScript_Foster_Text_0:
# 41 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "The ground here rumbles sometimes. Mt.\n"
	.string "Ember isn't fully asleep.$"

SixIsland_RuinValley_EventScript_Larry_Text_0:
# 45 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "I've climbed every hill in the Sevii\n"
	.string "Islands. Some twice!$"

SixIsland_RuinValley_EventScript_DottedHoleDoor_Text_0:
# 83 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "The door is sealed with a dotted stone\n"
	.string "slab.\n"
	.string "It won't budge. Maybe it will open some\l"
	.string "day.$"

SixIsland_RuinValley_Text_StanlyIntro::
# 28 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "These ruins are mine to dig! Out of my\n"
	.string "way!$"

SixIsland_RuinValley_Text_StanlyDefeat::
# 32 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "Buried alive!$"

SixIsland_RuinValley_Text_StanlyPost::
# 36 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "Ruin Valley is full of ancient carvings.$"

SixIsland_RuinValley_Text_DarylIntro::
# 53 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "Is that a tree? No, it's my partner!$"

SixIsland_RuinValley_Text_DarylDefeat::
# 57 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "Timber!$"

SixIsland_RuinValley_Text_DarylPost::
# 61 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "I've climbed every hill in the Sevii\n"
	.string "Islands. Some twice!$"

SixIsland_RuinValley_Text_HectorIntro::
# 70 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "My rare Pokémon will crush you!$"

SixIsland_RuinValley_Text_HectorDefeat::
# 74 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "My collection!$"

SixIsland_RuinValley_Text_HectorPost::
# 78 "data/maps/SixIsland_RuinValley/scripts.pory"
	.string "Each island has its own character. Have\n"
	.string "you visited them all?$"
