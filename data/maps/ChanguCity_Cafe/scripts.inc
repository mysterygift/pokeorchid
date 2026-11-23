ChanguCity_Cafe_MapScripts::
# 5 "data/maps/ChanguCity_Cafe/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION
	.byte 0

ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION:
# 6 "data/maps/ChanguCity_Cafe/scripts.pory"
	goto_if_set FLAG_CYNTHIA_BEATEN_AT_LAKE, ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION_1
# 9 "data/maps/ChanguCity_Cafe/scripts.pory"
	setflag FLAG_HIDE_CHANGU_CAFE_CYNTHIA
	return

ChanguCity_Cafe_MapScripts_MAP_SCRIPT_ON_TRANSITION_1:
# 7 "data/maps/ChanguCity_Cafe/scripts.pory"
	clearflag FLAG_HIDE_CHANGU_CAFE_CYNTHIA
	return


ChanguCity_Cafe_EventScript_Barista::
# 15 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Barista_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Businessman::
# 19 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Businessman_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Businesswoman::
# 23 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Businesswoman_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_Tourist::
# 27 "data/maps/ChanguCity_Cafe/scripts.pory"
	goto_if_set FLAG_CYNTHIA_BEATEN_AT_LAKE, ChanguCity_Cafe_EventScript_Tourist_1
# 30 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Tourist_Text_1, MSGBOX_NPC
	return

ChanguCity_Cafe_EventScript_Tourist_1:
# 28 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_Tourist_Text_0, MSGBOX_NPC
	return


ChanguCity_Cafe_EventScript_KalosArtist::
# 37 "data/maps/ChanguCity_Cafe/scripts.pory"
	lock
# 38 "data/maps/ChanguCity_Cafe/scripts.pory"
	faceplayer
# 39 "data/maps/ChanguCity_Cafe/scripts.pory"
	questmenu QUEST_MENU_CHECK_COMPLETE, QUEST_TASTE_OF_HOME
# 40 "data/maps/ChanguCity_Cafe/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_ne ChanguCity_Cafe_EventScript_KalosArtist_2
# 45 "data/maps/ChanguCity_Cafe/scripts.pory"
	questmenu QUEST_MENU_CHECK_ACTIVE, QUEST_TASTE_OF_HOME
# 46 "data/maps/ChanguCity_Cafe/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq ChanguCity_Cafe_EventScript_KalosArtist_5
ChanguCity_Cafe_EventScript_KalosArtist_4:
# 52 "data/maps/ChanguCity_Cafe/scripts.pory"
	checkitem ITEM_OLD_GATEAU
# 53 "data/maps/ChanguCity_Cafe/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq ChanguCity_Cafe_EventScript_KalosArtist_8
# 58 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_5, MSGBOX_YESNO
# 59 "data/maps/ChanguCity_Cafe/scripts.pory"
	compare VAR_RESULT, NO
	goto_if_eq ChanguCity_Cafe_EventScript_KalosArtist_11
# 64 "data/maps/ChanguCity_Cafe/scripts.pory"
	checkitemspace ITEM_STAR_PIECE
# 65 "data/maps/ChanguCity_Cafe/scripts.pory"
	compare VAR_RESULT, 0
	goto_if_eq ChanguCity_Cafe_EventScript_KalosArtist_14
# 70 "data/maps/ChanguCity_Cafe/scripts.pory"
	removeitem ITEM_OLD_GATEAU
# 71 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_8
# 72 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_9
# 73 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_10
# 74 "data/maps/ChanguCity_Cafe/scripts.pory"
	giveitem ITEM_STAR_PIECE
# 75 "data/maps/ChanguCity_Cafe/scripts.pory"
	completequest QUEST_TASTE_OF_HOME
# 76 "data/maps/ChanguCity_Cafe/scripts.pory"
	release
	end

ChanguCity_Cafe_EventScript_KalosArtist_2:
# 41 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_0
# 42 "data/maps/ChanguCity_Cafe/scripts.pory"
	release
	end

ChanguCity_Cafe_EventScript_KalosArtist_5:
# 47 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_1
# 48 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_2
# 49 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_3
# 50 "data/maps/ChanguCity_Cafe/scripts.pory"
	startquest QUEST_TASTE_OF_HOME
	goto ChanguCity_Cafe_EventScript_KalosArtist_4

ChanguCity_Cafe_EventScript_KalosArtist_8:
# 54 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_4
# 55 "data/maps/ChanguCity_Cafe/scripts.pory"
	release
	end

ChanguCity_Cafe_EventScript_KalosArtist_11:
# 60 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_6
# 61 "data/maps/ChanguCity_Cafe/scripts.pory"
	release
	end

ChanguCity_Cafe_EventScript_KalosArtist_14:
# 66 "data/maps/ChanguCity_Cafe/scripts.pory"
	msgbox ChanguCity_Cafe_EventScript_KalosArtist_Text_7
# 67 "data/maps/ChanguCity_Cafe/scripts.pory"
	release
	end


ChanguCity_Cafe_EventScript_Barista_Text_0:
# 15 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Welcome to the Battle Café!$"

ChanguCity_Cafe_EventScript_Businessman_Text_0:
# 19 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "We flew in from Lumiose this morning. If\n"
	.string "this deal doesn't close by tonight, I'm\l"
	.string "on the red-eye home.$"

ChanguCity_Cafe_EventScript_Businesswoman_Text_0:
# 23 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Synergise, innovate, leverage… I just\n"
	.string "wanted a kaya toast in peace.$"

ChanguCity_Cafe_EventScript_Tourist_Text_0:
# 28 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "That blonde lady in the corner has been\n"
	.string "here every day since she came back from\l"
	.string "Holon Lake. Is she someone famous?$"

ChanguCity_Cafe_EventScript_Tourist_Text_1:
# 30 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "They call this place the Battle Café.\n"
	.string "Trainers come here between flights,\l"
	.string "hoping a strong opponent walks in.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_0:
# 41 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Merci encore, mon ami! I wrote to the\n"
	.string "chef in Tosa Port. Now he posts me an\l"
	.string "Old Gateau every month!$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_1:
# 47 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Bonjour… Pardon, I am a little homesick\n"
	.string "today.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_2:
# 48 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "I came from Lumiose to paint the\n"
	.string "colours of Tosa. The light here is\l"
	.string "magnifique, but the food… it is not\l"
	.string "home.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_3:
# 49 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "What I would give for a taste of home…\n"
	.string "An Old Gateau, like the ones ma\l"
	.string "grand-mère bought every Sunday.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_4:
# 54 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "An Old Gateau, here in Tosa… It is only a\n"
	.string "dream, non?$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_5:
# 58 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Mon dieu… that smell! Is that an Old\n"
	.string "Gateau?! Would you let me have it?$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_6:
# 60 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Ah… I understand. It is too delicious to\n"
	.string "give away.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_7:
# 66 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "Ah, but your Bag is full! Make a little\n"
	.string "room, and I will repay you properly.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_8:
# 71 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "{PLAYER} handed over the Old Gateau.$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_9:
# 72 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "…Mmm! Oui, c'est ça! For a moment, I was\n"
	.string "back on the boulevards of Lumiose!$"

ChanguCity_Cafe_EventScript_KalosArtist_Text_10:
# 73 "data/maps/ChanguCity_Cafe/scripts.pory"
	.string "You must take this. It is not much, but\n"
	.string "it shines like Prism Tower at night.$"
