MtEmber_Exterior_MapScripts::
	.byte 0


MtEmber_Exterior_EventScript_ExplosionTutor::
# 4 "data/maps/MtEmber_Exterior/scripts.pory"
	msgbox MtEmber_Exterior_EventScript_ExplosionTutor_Text_0, MSGBOX_NPC
	return


MtEmber_Exterior_EventScript_Grunt1::
# 8 "data/maps/MtEmber_Exterior/scripts.pory"
	msgbox MtEmber_Exterior_EventScript_Grunt1_Text_0, MSGBOX_NPC
	return


MtEmber_Exterior_EventScript_Grunt2::
# 12 "data/maps/MtEmber_Exterior/scripts.pory"
	msgbox MtEmber_Exterior_EventScript_Grunt2_Text_0, MSGBOX_NPC
	return


MtEmber_Exterior_EventScript_Jocelyn::
# 16 "data/maps/MtEmber_Exterior/scripts.pory"
	msgbox MtEmber_Exterior_EventScript_Grunt2_Text_0, MSGBOX_NPC
	return


MtEmber_Exterior_EventScript_Logan::
# 20 "data/maps/MtEmber_Exterior/scripts.pory"
	trainerbattle_single TRAINER_SEVII_LOGAN, MtEmber_Exterior_Text_LoganIntro, MtEmber_Exterior_Text_LoganDefeat
# 21 "data/maps/MtEmber_Exterior/scripts.pory"
	msgbox MtEmber_Exterior_Text_LoganPost, MSGBOX_AUTOCLOSE
	return


MtEmber_Exterior_EventScript_Beth::
# 37 "data/maps/MtEmber_Exterior/scripts.pory"
	trainerbattle_single TRAINER_SEVII_BETH, MtEmber_Exterior_Text_BethIntro, MtEmber_Exterior_Text_BethDefeat
# 38 "data/maps/MtEmber_Exterior/scripts.pory"
	msgbox MtEmber_Exterior_Text_BethPost, MSGBOX_AUTOCLOSE
	return


# 53 "data/maps/MtEmber_Exterior/scripts.pory"

# 54 "data/maps/MtEmber_Exterior/scripts.pory"
MtEmber_Exterior_EventScript_EdgeWarp_28_48::
# 55 "data/maps/MtEmber_Exterior/scripts.pory"
	specialvar VAR_RESULT, GetPlayerFacingDirection
# 56 "data/maps/MtEmber_Exterior/scripts.pory"
	goto_if_ne VAR_RESULT, DIR_SOUTH, Sevii_EventScript_End
# 57 "data/maps/MtEmber_Exterior/scripts.pory"
	warp MAP_ONE_ISLAND_KINDLE_ROAD, 0
# 58 "data/maps/MtEmber_Exterior/scripts.pory"
	waitstate
# 59 "data/maps/MtEmber_Exterior/scripts.pory"
	end
# 60 "data/maps/MtEmber_Exterior/scripts.pory"

# 61 "data/maps/MtEmber_Exterior/scripts.pory"
MtEmber_Exterior_EventScript_EdgeWarp_29_48::
# 62 "data/maps/MtEmber_Exterior/scripts.pory"
	specialvar VAR_RESULT, GetPlayerFacingDirection
# 63 "data/maps/MtEmber_Exterior/scripts.pory"
	goto_if_ne VAR_RESULT, DIR_SOUTH, Sevii_EventScript_End
# 64 "data/maps/MtEmber_Exterior/scripts.pory"
	warp MAP_ONE_ISLAND_KINDLE_ROAD, 1
# 65 "data/maps/MtEmber_Exterior/scripts.pory"
	waitstate
# 66 "data/maps/MtEmber_Exterior/scripts.pory"
	end
# 67 "data/maps/MtEmber_Exterior/scripts.pory"

# 68 "data/maps/MtEmber_Exterior/scripts.pory"
MtEmber_Exterior_EventScript_EdgeWarp_29_7::
# 69 "data/maps/MtEmber_Exterior/scripts.pory"
	specialvar VAR_RESULT, GetPlayerFacingDirection
# 70 "data/maps/MtEmber_Exterior/scripts.pory"
	goto_if_ne VAR_RESULT, DIR_NORTH, Sevii_EventScript_End
# 71 "data/maps/MtEmber_Exterior/scripts.pory"
	warp MAP_MT_EMBER_SUMMIT, 0
# 72 "data/maps/MtEmber_Exterior/scripts.pory"
	waitstate
# 73 "data/maps/MtEmber_Exterior/scripts.pory"
	end

MtEmber_Exterior_EventScript_ExplosionTutor_Text_0:
# 4 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "The ground here rumbles sometimes. Mt.\n"
	.string "Ember isn't fully asleep.$"

MtEmber_Exterior_EventScript_Grunt1_Text_0:
# 8 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "Mt. Ember is still smoking. Something\n"
	.string "lives at the very top...$"

MtEmber_Exterior_EventScript_Grunt2_Text_0:
# 12 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "It's so hot on this mountain! My\n"
	.string "Pokémon love it.$"

MtEmber_Exterior_Text_LoganIntro::
# 24 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "Rangers keep Mt. Ember safe. Show me\n"
	.string "your skill!$"

MtEmber_Exterior_Text_LoganDefeat::
# 28 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "You're the real deal.$"

MtEmber_Exterior_Text_LoganPost::
# 32 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "It's so hot on this mountain! My\n"
	.string "Pokémon love it.$"

MtEmber_Exterior_Text_BethIntro::
# 41 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "The mountain path is dangerous. Let me\n"
	.string "test you!$"

MtEmber_Exterior_Text_BethDefeat::
# 45 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "You can handle Mt. Ember.$"

MtEmber_Exterior_Text_BethPost::
# 49 "data/maps/MtEmber_Exterior/scripts.pory"
	.string "I came to the islands to camp under the\n"
	.string "stars.$"
