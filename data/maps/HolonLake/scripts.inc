# 1 "data/maps/HolonLake/scripts.pory"

# 2 "data/maps/HolonLake/scripts.pory"
HolonLake_MapScripts::
# 3 "data/maps/HolonLake/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, HolonLake_OnResume
# 4 "data/maps/HolonLake/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, HolonLake_OnTransition
# 5 "data/maps/HolonLake/scripts.pory"
	.byte 0
# 6 "data/maps/HolonLake/scripts.pory"

# 7 "data/maps/HolonLake/scripts.pory"
HolonLake_OnTransition:
# 8 "data/maps/HolonLake/scripts.pory"
	setflag FLAG_VISITED_HOLON_LAKE
# 9 "data/maps/HolonLake/scripts.pory"
	end
# 10 "data/maps/HolonLake/scripts.pory"

# 11 "data/maps/HolonLake/scripts.pory"
HolonLake_OnResume:
# 12 "data/maps/HolonLake/scripts.pory"
	call_if_set HOLON_SPHERE_GLOW_FLAG, HolonLake_EventScript_SphereGlowOn
# 13 "data/maps/HolonLake/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, HolonLake_EventScript_TryRemoveGyarados
# 14 "data/maps/HolonLake/scripts.pory"
	end
# 15 "data/maps/HolonLake/scripts.pory"

# 16 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_SphereGlowOn::
# 17 "data/maps/HolonLake/scripts.pory"
	callnative Holon_SetSphereGlow
# 18 "data/maps/HolonLake/scripts.pory"
	return
# 19 "data/maps/HolonLake/scripts.pory"

# 20 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_TryRemoveGyarados::
# 21 "data/maps/HolonLake/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 22 "data/maps/HolonLake/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 23 "data/maps/HolonLake/scripts.pory"
	removeobject VAR_LAST_TALKED
# 24 "data/maps/HolonLake/scripts.pory"
	return
# 25 "data/maps/HolonLake/scripts.pory"

# 26 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_Sphere::
# 27 "data/maps/HolonLake/scripts.pory"
	lock
# 28 "data/maps/HolonLake/scripts.pory"
	goto_if_set HOLON_SPHERE_GLOW_FLAG, HolonLake_EventScript_SphereAwake
# 29 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_Text_SphereDormant, MSGBOX_DEFAULT
# 30 "data/maps/HolonLake/scripts.pory"
	release
# 31 "data/maps/HolonLake/scripts.pory"
	end
# 32 "data/maps/HolonLake/scripts.pory"

# 33 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_SphereAwake::
# 34 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_Text_SphereAwake, MSGBOX_DEFAULT
# 35 "data/maps/HolonLake/scripts.pory"
	release
# 36 "data/maps/HolonLake/scripts.pory"
	end
# 37 "data/maps/HolonLake/scripts.pory"

# 38 "data/maps/HolonLake/scripts.pory"
@ Called once Cynthia is beaten (trainers stream): the sphere's OBJ palette swaps to the glow copy.
# 39 "data/maps/HolonLake/scripts.pory"
Holon_EventScript_AwakenSphere::
# 40 "data/maps/HolonLake/scripts.pory"
	setflag HOLON_SPHERE_GLOW_FLAG
# 41 "data/maps/HolonLake/scripts.pory"
	callnative Holon_SetSphereGlow
# 42 "data/maps/HolonLake/scripts.pory"
	playse SE_M_DETECT
# 43 "data/maps/HolonLake/scripts.pory"
	waitse
# 44 "data/maps/HolonLake/scripts.pory"
	return
# 45 "data/maps/HolonLake/scripts.pory"

# 46 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_Cynthia::
# 47 "data/maps/HolonLake/scripts.pory"
	lock
# 48 "data/maps/HolonLake/scripts.pory"
	faceplayer
# 49 "data/maps/HolonLake/scripts.pory"
	@ TODO(trainers): replace with Cynthia's battle script (encounter music, trainerbattle, then
# 50 "data/maps/HolonLake/scripts.pory"
	@ call Holon_EventScript_AwakenSphere and hide her here / move her to the Changu Battle Cafe)
# 51 "data/maps/HolonLake/scripts.pory"
	goto Common_EventScript_CynthiaHolonLake
# 52 "data/maps/HolonLake/scripts.pory"
	release
# 53 "data/maps/HolonLake/scripts.pory"
	end
# 54 "data/maps/HolonLake/scripts.pory"

# 55 "data/maps/HolonLake/scripts.pory"
Holon_CynthiaPlaceholder::
# 56 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_Text_CynthiaPlaceholder, MSGBOX_DEFAULT
# 57 "data/maps/HolonLake/scripts.pory"
	return
# 58 "data/maps/HolonLake/scripts.pory"

# 59 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_Gyarados::
# 60 "data/maps/HolonLake/scripts.pory"
	lock
# 61 "data/maps/HolonLake/scripts.pory"
	faceplayer
# 62 "data/maps/HolonLake/scripts.pory"
	@ TODO(delta): SPECIES_GYARADOS_DELTA -> SPECIES_GYARADOS_DELTA (shiny Gyarados-delta static, Lv 65)
# 63 "data/maps/HolonLake/scripts.pory"
	waitse
# 64 "data/maps/HolonLake/scripts.pory"
	playmoncry SPECIES_GYARADOS_DELTA, CRY_MODE_ENCOUNTER
# 65 "data/maps/HolonLake/scripts.pory"
	delay 40
# 66 "data/maps/HolonLake/scripts.pory"
	waitmoncry
# 67 "data/maps/HolonLake/scripts.pory"
	setwildbattle SPECIES_GYARADOS_DELTA, 65
# 68 "data/maps/HolonLake/scripts.pory"
	createmon 1, 0, SPECIES_GYARADOS_DELTA, 65, shinyMode=SHINY_MODE_ALWAYS
# 69 "data/maps/HolonLake/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 70 "data/maps/HolonLake/scripts.pory"
	dowildbattle
# 71 "data/maps/HolonLake/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 72 "data/maps/HolonLake/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 73 "data/maps/HolonLake/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, HolonLake_EventScript_GyaradosGone
# 74 "data/maps/HolonLake/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, HolonLake_EventScript_GyaradosStays
# 75 "data/maps/HolonLake/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, HolonLake_EventScript_GyaradosStays
# 76 "data/maps/HolonLake/scripts.pory"
	setflag FLAG_HOLON_HIDE_GYARADOS
# 77 "data/maps/HolonLake/scripts.pory"
	release
# 78 "data/maps/HolonLake/scripts.pory"
	end
# 79 "data/maps/HolonLake/scripts.pory"

# 80 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_GyaradosGone::
# 81 "data/maps/HolonLake/scripts.pory"
	setflag FLAG_HOLON_HIDE_GYARADOS
# 82 "data/maps/HolonLake/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 83 "data/maps/HolonLake/scripts.pory"
	end
# 84 "data/maps/HolonLake/scripts.pory"

# 85 "data/maps/HolonLake/scripts.pory"
HolonLake_EventScript_GyaradosStays::
# 86 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_Text_GyaradosDived, MSGBOX_DEFAULT
# 87 "data/maps/HolonLake/scripts.pory"
	release
# 88 "data/maps/HolonLake/scripts.pory"
	end

HolonLake_EventScript_Mentor::
# 108 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_EventScript_Mentor_Text_0, MSGBOX_NPC
	return


HolonLake_EventScript_Researcher1::
# 112 "data/maps/HolonLake/scripts.pory"
	trainerbattle_single TRAINER_HOLON_MATEO, HolonLake_Text_Researcher1Intro, HolonLake_Text_Researcher1Defeat
# 113 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_Text_Researcher1Post, MSGBOX_AUTOCLOSE
	return


HolonLake_EventScript_Researcher2::
# 129 "data/maps/HolonLake/scripts.pory"
	trainerbattle_single TRAINER_HOLON_HENRIK, HolonLake_Text_Researcher2Intro, HolonLake_Text_Researcher2Defeat
# 130 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_Text_Researcher2Post, MSGBOX_AUTOCLOSE
	return


HolonLake_EventScript_Sign::
# 146 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_EventScript_Sign_Text_0, MSGBOX_SIGN
	return


HolonLake_EventScript_SealedDome::
# 150 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_EventScript_SealedDome_Text_0, MSGBOX_SIGN
	return


HolonLake_EventScript_Pillar::
# 154 "data/maps/HolonLake/scripts.pory"
	msgbox HolonLake_EventScript_Pillar_Text_0, MSGBOX_SIGN
	return


HolonLake_EventScript_Mentor_Text_0:
# 108 "data/maps/HolonLake/scripts.pory"
	.string "Those stone domes by the shore have\n"
	.string "been sealed since before my\l"
	.string "grandmother's time. Whatever's inside is\l"
	.string "meant to stay there.$"

HolonLake_EventScript_Sign_Text_0:
# 146 "data/maps/HolonLake/scripts.pory"
	.string "Holon Lake\n"
	.string "Please do not disturb the stone pillars.$"

HolonLake_EventScript_SealedDome_Text_0:
# 150 "data/maps/HolonLake/scripts.pory"
	.string "The doorway is sealed with a carved\n"
	.string "stone slab. A diamond is cut into its\l"
	.string "face.$"

HolonLake_EventScript_Pillar_Text_0:
# 154 "data/maps/HolonLake/scripts.pory"
	.string "A tall carved pillar rising out of the\n"
	.string "lake. It hums faintly.$"

HolonLake_Text_SphereDormant::
# 91 "data/maps/HolonLake/scripts.pory"
	.string "A great stone sphere rests in the\n"
	.string "plinth's socket. Diamonds are carved all\l"
	.string "over it. It feels cold.$"

HolonLake_Text_SphereAwake::
# 95 "data/maps/HolonLake/scripts.pory"
	.string "The stone sphere is glowing with a soft\n"
	.string "blue light. The air around it hums.$"

HolonLake_Text_CynthiaPlaceholder::
# 99 "data/maps/HolonLake/scripts.pory"
	.string "...\p"
	.string "(Placeholder: Cynthia's battle script is\n"
	.string "added by the trainers stream.)$"

HolonLake_Text_GyaradosDived::
# 103 "data/maps/HolonLake/scripts.pory"
	.string "The Gyarados dived back under the\n"
	.string "surface...$"

HolonLake_Text_Researcher1Intro::
# 116 "data/maps/HolonLake/scripts.pory"
	.string "The marsh readings are off the charts!\n"
	.string "Don't trample my instruments!$"

HolonLake_Text_Researcher1Defeat::
# 120 "data/maps/HolonLake/scripts.pory"
	.string "I'll have to recalibrate everything...$"

HolonLake_Text_Researcher1Post::
# 124 "data/maps/HolonLake/scripts.pory"
	.string "The pillars channel the lake's energy\n"
	.string "into that sphere. We just collect what\l"
	.string "spills over.$"

HolonLake_Text_Researcher2Intro::
# 133 "data/maps/HolonLake/scripts.pory"
	.string "A visitor? This part of the shore is\n"
	.string "closed for research!$"

HolonLake_Text_Researcher2Defeat::
# 137 "data/maps/HolonLake/scripts.pory"
	.string "Hmph. Fine, look around. Just don't\n"
	.string "touch the pillars.$"

HolonLake_Text_Researcher2Post::
# 141 "data/maps/HolonLake/scripts.pory"
	.string "The domes by the shore? Sealed. We've\n"
	.string "never found a way in, and the elders\l"
	.string "won't say.$"
