SixIsland_Harbor_MapScripts::
	.byte 0


# 3 "data/maps/SixIsland_Harbor/scripts.pory"

# 4 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_Sailor::
# 5 "data/maps/SixIsland_Harbor/scripts.pory"
	lock
# 6 "data/maps/SixIsland_Harbor/scripts.pory"
	faceplayer
# 7 "data/maps/SixIsland_Harbor/scripts.pory"
	message SeviiFerry_Text_WhereTo
# 8 "data/maps/SixIsland_Harbor/scripts.pory"
	waitmessage
# 9 "data/maps/SixIsland_Harbor/scripts.pory"
	dynmultichoice 0, 0, FALSE, 7, 0, DYN_MULTICHOICE_CB_NONE, SeviiFerry_Text_SevenIsland, SeviiFerry_Text_OneIsland, SeviiFerry_Text_TwoIsland, SeviiFerry_Text_ThreeIsland, SeviiFerry_Text_FourIsland, SeviiFerry_Text_FiveIsland, SeviiFerry_Text_Stay_Option
# 10 "data/maps/SixIsland_Harbor/scripts.pory"
	switch VAR_RESULT
# 11 "data/maps/SixIsland_Harbor/scripts.pory"
	case 0, SixIsland_Harbor_EventScript_ToSevenIsland
# 12 "data/maps/SixIsland_Harbor/scripts.pory"
	case 1, SixIsland_Harbor_EventScript_ToOneIsland
# 13 "data/maps/SixIsland_Harbor/scripts.pory"
	case 2, SixIsland_Harbor_EventScript_ToTwoIsland
# 14 "data/maps/SixIsland_Harbor/scripts.pory"
	case 3, SixIsland_Harbor_EventScript_ToThreeIsland
# 15 "data/maps/SixIsland_Harbor/scripts.pory"
	case 4, SixIsland_Harbor_EventScript_ToFourIsland
# 16 "data/maps/SixIsland_Harbor/scripts.pory"
	case 5, SixIsland_Harbor_EventScript_ToFiveIsland
# 17 "data/maps/SixIsland_Harbor/scripts.pory"
	msgbox SeviiFerry_Text_Stay, MSGBOX_DEFAULT
# 18 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 19 "data/maps/SixIsland_Harbor/scripts.pory"
	end
# 20 "data/maps/SixIsland_Harbor/scripts.pory"

# 21 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_ToSevenIsland::
# 22 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_SIX_ISLAND_HARBOR_BOAT
# 23 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_SIX_ISLAND_HARBOR_SAILOR
# 24 "data/maps/SixIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 25 "data/maps/SixIsland_Harbor/scripts.pory"
	warp MAP_SEVEN_ISLAND_HARBOR, 8, 4
# 26 "data/maps/SixIsland_Harbor/scripts.pory"
	waitstate
# 27 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 28 "data/maps/SixIsland_Harbor/scripts.pory"
	end
# 29 "data/maps/SixIsland_Harbor/scripts.pory"

# 30 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_ToOneIsland::
# 31 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_SIX_ISLAND_HARBOR_BOAT
# 32 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_SIX_ISLAND_HARBOR_SAILOR
# 33 "data/maps/SixIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 34 "data/maps/SixIsland_Harbor/scripts.pory"
	warp MAP_ONE_ISLAND_HARBOR, 8, 4
# 35 "data/maps/SixIsland_Harbor/scripts.pory"
	waitstate
# 36 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 37 "data/maps/SixIsland_Harbor/scripts.pory"
	end
# 38 "data/maps/SixIsland_Harbor/scripts.pory"

# 39 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_ToTwoIsland::
# 40 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_SIX_ISLAND_HARBOR_BOAT
# 41 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_SIX_ISLAND_HARBOR_SAILOR
# 42 "data/maps/SixIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 43 "data/maps/SixIsland_Harbor/scripts.pory"
	warp MAP_TWO_ISLAND_HARBOR, 8, 4
# 44 "data/maps/SixIsland_Harbor/scripts.pory"
	waitstate
# 45 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 46 "data/maps/SixIsland_Harbor/scripts.pory"
	end
# 47 "data/maps/SixIsland_Harbor/scripts.pory"

# 48 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_ToThreeIsland::
# 49 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_SIX_ISLAND_HARBOR_BOAT
# 50 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_SIX_ISLAND_HARBOR_SAILOR
# 51 "data/maps/SixIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 52 "data/maps/SixIsland_Harbor/scripts.pory"
	warp MAP_THREE_ISLAND_HARBOR, 8, 4
# 53 "data/maps/SixIsland_Harbor/scripts.pory"
	waitstate
# 54 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 55 "data/maps/SixIsland_Harbor/scripts.pory"
	end
# 56 "data/maps/SixIsland_Harbor/scripts.pory"

# 57 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_ToFourIsland::
# 58 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_SIX_ISLAND_HARBOR_BOAT
# 59 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_SIX_ISLAND_HARBOR_SAILOR
# 60 "data/maps/SixIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 61 "data/maps/SixIsland_Harbor/scripts.pory"
	warp MAP_FOUR_ISLAND_HARBOR, 8, 4
# 62 "data/maps/SixIsland_Harbor/scripts.pory"
	waitstate
# 63 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 64 "data/maps/SixIsland_Harbor/scripts.pory"
	end
# 65 "data/maps/SixIsland_Harbor/scripts.pory"

# 66 "data/maps/SixIsland_Harbor/scripts.pory"
SixIsland_Harbor_EventScript_ToFiveIsland::
# 67 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_SIX_ISLAND_HARBOR_BOAT
# 68 "data/maps/SixIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_SIX_ISLAND_HARBOR_SAILOR
# 69 "data/maps/SixIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 70 "data/maps/SixIsland_Harbor/scripts.pory"
	warp MAP_FIVE_ISLAND_HARBOR, 8, 4
# 71 "data/maps/SixIsland_Harbor/scripts.pory"
	waitstate
# 72 "data/maps/SixIsland_Harbor/scripts.pory"
	release
# 73 "data/maps/SixIsland_Harbor/scripts.pory"
	end
