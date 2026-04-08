# 1 "data/maps/TelokTown_Mart/scripts.pory"

# 2 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_MapScripts::
# 3 "data/maps/TelokTown_Mart/scripts.pory"
	.byte 0
# 4 "data/maps/TelokTown_Mart/scripts.pory"

# 5 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_EventScript_Clerk::
# 6 "data/maps/TelokTown_Mart/scripts.pory"
	lock
# 7 "data/maps/TelokTown_Mart/scripts.pory"
	faceplayer
# 8 "data/maps/TelokTown_Mart/scripts.pory"
	message gText_HowMayIServeYou
# 9 "data/maps/TelokTown_Mart/scripts.pory"
	waitmessage
# 10 "data/maps/TelokTown_Mart/scripts.pory"
	goto_if_set FLAG_ADVENTURE_STARTED, TelokTown_Mart_ExpandedItems
# 11 "data/maps/TelokTown_Mart/scripts.pory"
	pokemart TelokTown_Mart_Pokemart_Basic
# 12 "data/maps/TelokTown_Mart/scripts.pory"
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
# 13 "data/maps/TelokTown_Mart/scripts.pory"
	release
# 14 "data/maps/TelokTown_Mart/scripts.pory"
	end
# 15 "data/maps/TelokTown_Mart/scripts.pory"

# 16 "data/maps/TelokTown_Mart/scripts.pory"
	.align 2
# 17 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_Pokemart_Basic:
# 18 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_POTION
# 19 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 20 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 21 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_AWAKENING
# 22 "data/maps/TelokTown_Mart/scripts.pory"
	pokemartlistend
# 23 "data/maps/TelokTown_Mart/scripts.pory"

# 24 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_ExpandedItems::
# 25 "data/maps/TelokTown_Mart/scripts.pory"
	pokemart TelokTown_Mart_Pokemart_Expanded
# 26 "data/maps/TelokTown_Mart/scripts.pory"
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
# 27 "data/maps/TelokTown_Mart/scripts.pory"
	release
# 28 "data/maps/TelokTown_Mart/scripts.pory"
	end
# 29 "data/maps/TelokTown_Mart/scripts.pory"

# 30 "data/maps/TelokTown_Mart/scripts.pory"
	.align 2
# 31 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_Pokemart_Expanded:
# 32 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_POKE_BALL
# 33 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_POTION
# 34 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_ANTIDOTE
# 35 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_PARALYZE_HEAL
# 36 "data/maps/TelokTown_Mart/scripts.pory"
	.2byte ITEM_AWAKENING
# 37 "data/maps/TelokTown_Mart/scripts.pory"
	pokemartlistend
# 38 "data/maps/TelokTown_Mart/scripts.pory"

# 39 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_EventScript_Woman::
# 40 "data/maps/TelokTown_Mart/scripts.pory"
	lock
# 41 "data/maps/TelokTown_Mart/scripts.pory"
	faceplayer
# 42 "data/maps/TelokTown_Mart/scripts.pory"
	goto_if_set FLAG_ADVENTURE_STARTED, TelokTown_Mart_EventScript_PokeBallsInStock
# 43 "data/maps/TelokTown_Mart/scripts.pory"
	msgbox TelokTown_Mart_Text_PokeBallsAreSoldOut, MSGBOX_DEFAULT
# 44 "data/maps/TelokTown_Mart/scripts.pory"
	release
# 45 "data/maps/TelokTown_Mart/scripts.pory"
	end
# 46 "data/maps/TelokTown_Mart/scripts.pory"

# 47 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_EventScript_PokeBallsInStock::
# 48 "data/maps/TelokTown_Mart/scripts.pory"
	msgbox TelokTown_Mart_Text_ImGoingToBuyPokeBalls, MSGBOX_DEFAULT
# 49 "data/maps/TelokTown_Mart/scripts.pory"
	release
# 50 "data/maps/TelokTown_Mart/scripts.pory"
	end
# 51 "data/maps/TelokTown_Mart/scripts.pory"

# 52 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_EventScript_Boy::
# 53 "data/maps/TelokTown_Mart/scripts.pory"
	msgbox TelokTown_Mart_Text_RestoreHPWithPotion, MSGBOX_NPC
# 54 "data/maps/TelokTown_Mart/scripts.pory"
	end
# 55 "data/maps/TelokTown_Mart/scripts.pory"

# 56 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_Text_PokeBallsAreSoldOut:
# 57 "data/maps/TelokTown_Mart/scripts.pory"
	.string "The clerk says they're all sold out.\n"
# 58 "data/maps/TelokTown_Mart/scripts.pory"
	.string "I can't buy any POKé BALLS.$"
# 59 "data/maps/TelokTown_Mart/scripts.pory"

# 60 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_Text_ImGoingToBuyPokeBalls:
# 61 "data/maps/TelokTown_Mart/scripts.pory"
	.string "I'm going to buy a bunch of POKé BALLS\n"
# 62 "data/maps/TelokTown_Mart/scripts.pory"
	.string "and catch a bunch of POKéMON!$"
# 63 "data/maps/TelokTown_Mart/scripts.pory"

# 64 "data/maps/TelokTown_Mart/scripts.pory"
TelokTown_Mart_Text_RestoreHPWithPotion:
# 65 "data/maps/TelokTown_Mart/scripts.pory"
	.string "If a POKéMON gets hurt and loses its HP\n"
# 66 "data/maps/TelokTown_Mart/scripts.pory"
	.string "and faints, it won't be able to battle.\p"
# 67 "data/maps/TelokTown_Mart/scripts.pory"
	.string "To prevent your POKéMON from fainting,\n"
# 68 "data/maps/TelokTown_Mart/scripts.pory"
	.string "restore its HP with a POTION.$"
