OneIsland_Harbor_MapScripts::
	.byte 0


# 3 "data/maps/OneIsland_Harbor/scripts.pory"

# 4 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_Sailor::
# 5 "data/maps/OneIsland_Harbor/scripts.pory"
	lock
# 6 "data/maps/OneIsland_Harbor/scripts.pory"
	faceplayer
# 7 "data/maps/OneIsland_Harbor/scripts.pory"
	message SeviiFerry_Text_WhereTo
# 8 "data/maps/OneIsland_Harbor/scripts.pory"
	waitmessage
# 9 "data/maps/OneIsland_Harbor/scripts.pory"
	dynmultichoice 0, 0, FALSE, 7, 0, DYN_MULTICHOICE_CB_NONE, SeviiFerry_Text_TwoIsland, SeviiFerry_Text_ThreeIsland, SeviiFerry_Text_FourIsland, SeviiFerry_Text_FiveIsland, SeviiFerry_Text_SixIsland, SeviiFerry_Text_SevenIsland, OneIsland_Harbor_Text_OtherVoyages, SeviiFerry_Text_Stay_Option
# 10 "data/maps/OneIsland_Harbor/scripts.pory"
	switch VAR_RESULT
# 11 "data/maps/OneIsland_Harbor/scripts.pory"
	case 0, OneIsland_Harbor_EventScript_ToTwoIsland
# 12 "data/maps/OneIsland_Harbor/scripts.pory"
	case 1, OneIsland_Harbor_EventScript_ToThreeIsland
# 13 "data/maps/OneIsland_Harbor/scripts.pory"
	case 2, OneIsland_Harbor_EventScript_ToFourIsland
# 14 "data/maps/OneIsland_Harbor/scripts.pory"
	case 3, OneIsland_Harbor_EventScript_ToFiveIsland
# 15 "data/maps/OneIsland_Harbor/scripts.pory"
	case 4, OneIsland_Harbor_EventScript_ToSixIsland
# 16 "data/maps/OneIsland_Harbor/scripts.pory"
	case 5, OneIsland_Harbor_EventScript_ToSevenIsland
# 17 "data/maps/OneIsland_Harbor/scripts.pory"
	case 6, OneIsland_Harbor_EventScript_OtherVoyages
# 18 "data/maps/OneIsland_Harbor/scripts.pory"
	msgbox SeviiFerry_Text_Stay, MSGBOX_DEFAULT
# 19 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 20 "data/maps/OneIsland_Harbor/scripts.pory"
	end
# 21 "data/maps/OneIsland_Harbor/scripts.pory"

# 22 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_OtherVoyages::
# 23 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 24 "data/maps/OneIsland_Harbor/scripts.pory"
	goto Voyage_EventScript_Sailor
# 25 "data/maps/OneIsland_Harbor/scripts.pory"

# 26 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_Text_OtherVoyages:
# 27 "data/maps/OneIsland_Harbor/scripts.pory"
	.string "Wavebreak & beyond$"
# 28 "data/maps/OneIsland_Harbor/scripts.pory"

# 29 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_ToTwoIsland::
# 30 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_ONE_ISLAND_HARBOR_BOAT
# 31 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_ONE_ISLAND_HARBOR_SAILOR
# 32 "data/maps/OneIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 33 "data/maps/OneIsland_Harbor/scripts.pory"
	warp MAP_TWO_ISLAND_HARBOR, 8, 4
# 34 "data/maps/OneIsland_Harbor/scripts.pory"
	waitstate
# 35 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 36 "data/maps/OneIsland_Harbor/scripts.pory"
	end
# 37 "data/maps/OneIsland_Harbor/scripts.pory"

# 38 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_ToThreeIsland::
# 39 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_ONE_ISLAND_HARBOR_BOAT
# 40 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_ONE_ISLAND_HARBOR_SAILOR
# 41 "data/maps/OneIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 42 "data/maps/OneIsland_Harbor/scripts.pory"
	warp MAP_THREE_ISLAND_HARBOR, 8, 4
# 43 "data/maps/OneIsland_Harbor/scripts.pory"
	waitstate
# 44 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 45 "data/maps/OneIsland_Harbor/scripts.pory"
	end
# 46 "data/maps/OneIsland_Harbor/scripts.pory"

# 47 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_ToFourIsland::
# 48 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_ONE_ISLAND_HARBOR_BOAT
# 49 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_ONE_ISLAND_HARBOR_SAILOR
# 50 "data/maps/OneIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 51 "data/maps/OneIsland_Harbor/scripts.pory"
	warp MAP_FOUR_ISLAND_HARBOR, 8, 4
# 52 "data/maps/OneIsland_Harbor/scripts.pory"
	waitstate
# 53 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 54 "data/maps/OneIsland_Harbor/scripts.pory"
	end
# 55 "data/maps/OneIsland_Harbor/scripts.pory"

# 56 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_ToFiveIsland::
# 57 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_ONE_ISLAND_HARBOR_BOAT
# 58 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_ONE_ISLAND_HARBOR_SAILOR
# 59 "data/maps/OneIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 60 "data/maps/OneIsland_Harbor/scripts.pory"
	warp MAP_FIVE_ISLAND_HARBOR, 8, 4
# 61 "data/maps/OneIsland_Harbor/scripts.pory"
	waitstate
# 62 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 63 "data/maps/OneIsland_Harbor/scripts.pory"
	end
# 64 "data/maps/OneIsland_Harbor/scripts.pory"

# 65 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_ToSixIsland::
# 66 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_ONE_ISLAND_HARBOR_BOAT
# 67 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_ONE_ISLAND_HARBOR_SAILOR
# 68 "data/maps/OneIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 69 "data/maps/OneIsland_Harbor/scripts.pory"
	warp MAP_SIX_ISLAND_HARBOR, 8, 4
# 70 "data/maps/OneIsland_Harbor/scripts.pory"
	waitstate
# 71 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 72 "data/maps/OneIsland_Harbor/scripts.pory"
	end
# 73 "data/maps/OneIsland_Harbor/scripts.pory"

# 74 "data/maps/OneIsland_Harbor/scripts.pory"
OneIsland_Harbor_EventScript_ToSevenIsland::
# 75 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_ONE_ISLAND_HARBOR_BOAT
# 76 "data/maps/OneIsland_Harbor/scripts.pory"
	setvar VAR_0x8005, LOCALID_ONE_ISLAND_HARBOR_SAILOR
# 77 "data/maps/OneIsland_Harbor/scripts.pory"
	call SeviiFerry_EventScript_Board
# 78 "data/maps/OneIsland_Harbor/scripts.pory"
	warp MAP_SEVEN_ISLAND_HARBOR, 8, 4
# 79 "data/maps/OneIsland_Harbor/scripts.pory"
	waitstate
# 80 "data/maps/OneIsland_Harbor/scripts.pory"
	release
# 81 "data/maps/OneIsland_Harbor/scripts.pory"
	end
