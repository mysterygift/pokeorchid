ThreeIsland_Harbor_MapScripts::
	.byte 0


# 3 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 4 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_Sailor::
# 5 "data/maps/ThreeIsland_Harbor/scripts.pory"
	lock
# 6 "data/maps/ThreeIsland_Harbor/scripts.pory"
	faceplayer
# 7 "data/maps/ThreeIsland_Harbor/scripts.pory"
	message SeviiFerry_Text_WhereTo
# 8 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitmessage
# 9 "data/maps/ThreeIsland_Harbor/scripts.pory"
	dynmultichoice 0, 0, FALSE, 7, 0, DYN_MULTICHOICE_CB_NONE, SeviiFerry_Text_OneIsland, SeviiFerry_Text_TwoIsland, SeviiFerry_Text_FourIsland, SeviiFerry_Text_FiveIsland, SeviiFerry_Text_SixIsland, SeviiFerry_Text_SevenIsland, SeviiFerry_Text_Stay_Option
# 10 "data/maps/ThreeIsland_Harbor/scripts.pory"
	switch VAR_RESULT
# 11 "data/maps/ThreeIsland_Harbor/scripts.pory"
	case 0, ThreeIsland_Harbor_EventScript_ToOneIsland
# 12 "data/maps/ThreeIsland_Harbor/scripts.pory"
	case 1, ThreeIsland_Harbor_EventScript_ToTwoIsland
# 13 "data/maps/ThreeIsland_Harbor/scripts.pory"
	case 2, ThreeIsland_Harbor_EventScript_ToFourIsland
# 14 "data/maps/ThreeIsland_Harbor/scripts.pory"
	case 3, ThreeIsland_Harbor_EventScript_ToFiveIsland
# 15 "data/maps/ThreeIsland_Harbor/scripts.pory"
	case 4, ThreeIsland_Harbor_EventScript_ToSixIsland
# 16 "data/maps/ThreeIsland_Harbor/scripts.pory"
	case 5, ThreeIsland_Harbor_EventScript_ToSevenIsland
# 17 "data/maps/ThreeIsland_Harbor/scripts.pory"
	msgbox SeviiFerry_Text_Stay, MSGBOX_DEFAULT
# 18 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 19 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
# 20 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 21 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_ToOneIsland::
# 22 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_THREE_ISLAND_HARBOR_BOAT
# 23 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_THREE_ISLAND_HARBOR_SAILOR
# 24 "data/maps/ThreeIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 25 "data/maps/ThreeIsland_Harbor/scripts.pory"
	warp MAP_ONE_ISLAND_HARBOR, 8, 4
# 26 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitstate
# 27 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 28 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
# 29 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 30 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_ToTwoIsland::
# 31 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_THREE_ISLAND_HARBOR_BOAT
# 32 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_THREE_ISLAND_HARBOR_SAILOR
# 33 "data/maps/ThreeIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 34 "data/maps/ThreeIsland_Harbor/scripts.pory"
	warp MAP_TWO_ISLAND_HARBOR, 8, 4
# 35 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitstate
# 36 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 37 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
# 38 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 39 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_ToFourIsland::
# 40 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_THREE_ISLAND_HARBOR_BOAT
# 41 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_THREE_ISLAND_HARBOR_SAILOR
# 42 "data/maps/ThreeIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 43 "data/maps/ThreeIsland_Harbor/scripts.pory"
	warp MAP_FOUR_ISLAND_HARBOR, 8, 4
# 44 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitstate
# 45 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 46 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
# 47 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 48 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_ToFiveIsland::
# 49 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_THREE_ISLAND_HARBOR_BOAT
# 50 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_THREE_ISLAND_HARBOR_SAILOR
# 51 "data/maps/ThreeIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 52 "data/maps/ThreeIsland_Harbor/scripts.pory"
	warp MAP_FIVE_ISLAND_HARBOR, 8, 4
# 53 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitstate
# 54 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 55 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
# 56 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 57 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_ToSixIsland::
# 58 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_THREE_ISLAND_HARBOR_BOAT
# 59 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_THREE_ISLAND_HARBOR_SAILOR
# 60 "data/maps/ThreeIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 61 "data/maps/ThreeIsland_Harbor/scripts.pory"
	warp MAP_SIX_ISLAND_HARBOR, 8, 4
# 62 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitstate
# 63 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 64 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
# 65 "data/maps/ThreeIsland_Harbor/scripts.pory"

# 66 "data/maps/ThreeIsland_Harbor/scripts.pory"
ThreeIsland_Harbor_EventScript_ToSevenIsland::
# 67 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_THREE_ISLAND_HARBOR_BOAT
# 68 "data/maps/ThreeIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_THREE_ISLAND_HARBOR_SAILOR
# 69 "data/maps/ThreeIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 70 "data/maps/ThreeIsland_Harbor/scripts.pory"
	warp MAP_SEVEN_ISLAND_HARBOR, 8, 4
# 71 "data/maps/ThreeIsland_Harbor/scripts.pory"
	waitstate
# 72 "data/maps/ThreeIsland_Harbor/scripts.pory"
	release
# 73 "data/maps/ThreeIsland_Harbor/scripts.pory"
	end
