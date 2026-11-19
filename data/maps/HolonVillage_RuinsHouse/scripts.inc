HolonVillage_RuinsHouse_MapScripts::
	.byte 0


HolonVillage_RuinsHouse_EventScript_LoreItem::
# 4 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	lock
# 5 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	msgbox HolonVillage_RuinsHouse_EventScript_LoreItem_Text_0, MSGBOX_DEFAULT
# 6 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	finditem ITEM_STAR_PIECE
# 7 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	release
	return


HolonVillage_RuinsHouse_EventScript_Bookshelf::
# 11 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	msgbox HolonVillage_RuinsHouse_EventScript_Bookshelf_Text_0, MSGBOX_SIGN
	return


HolonVillage_RuinsHouse_EventScript_LoreItem_Text_0:
# 5 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	.string "There's a scrap of paper tucked under a\n"
	.string "loose board...\p"
	.string "'The Power Spots must never be tapped.\n"
	.string "What the land gives freely, it can take\l"
	.string "back.'$"

HolonVillage_RuinsHouse_EventScript_Bookshelf_Text_0:
# 11 "data/maps/HolonVillage_RuinsHouse/scripts.pory"
	.string "Dusty old books about stone carving.\n"
	.string "The pages have gone brittle.$"
