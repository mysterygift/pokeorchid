# 1 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 2 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_MapScripts::
# 3 "data/maps/LilycoveCity_Harbor/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_Harbor_OnTransition
# 4 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.byte 0
# 5 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 6 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_OnTransition:
# 7 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setescapewarp MAP_LILYCOVE_CITY, 12, 33
# 8 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 9 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 10 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_FerryAttendant::
# 11 "data/maps/LilycoveCity_Harbor/scripts.pory"
	lock
# 12 "data/maps/LilycoveCity_Harbor/scripts.pory"
	faceplayer
# 13 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_unset FLAG_SYS_GAME_CLEAR, LilycoveCity_Harbor_EventScript_FerryUnavailable
# 14 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetEonTicketState
# 15 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetAuroraTicketState
# 16 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetOldSeaMapState
# 17 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetMysticTicketState
# 18 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetFirstTimeShowingTicket
# 19 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetHasTicketsState
# 20 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_TEMP_C, 2, LilycoveCity_Harbor_EventScript_OldSeaMapFirstTime
# 21 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_TEMP_B, 1, LilycoveCity_Harbor_EventScript_EonTicketFirstTime
# 22 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_TEMP_B, 2, LilycoveCity_Harbor_EventScript_AuroraTicketFirstTime
# 23 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_TEMP_B, 4, LilycoveCity_Harbor_EventScript_OldSeaMapFirstTime
# 24 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_TEMP_B, 8, LilycoveCity_Harbor_EventScript_MysticTicketFirstTime
# 25 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_ne VAR_TEMP_B, 0, LilycoveCity_Harbor_EventScript_MultipleEventTicketsFirstTime
# 26 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_NoFirstTimeEventTickets
# 27 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 28 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 29 "data/maps/LilycoveCity_Harbor/scripts.pory"
@ First goto_if_eq is unnecessary; identical scripts
# 30 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_NoFirstTimeEventTickets::
# 31 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_TEMP_A, 0, LilycoveCity_Harbor_EventScript_NoEventTickets
# 32 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_MayISeeYourTicket, MSGBOX_DEFAULT
# 33 "data/maps/LilycoveCity_Harbor/scripts.pory"
	message LilycoveCity_Harbor_Text_FlashTicketWhereTo
# 34 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmessage
# 35 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_FerryRegularLocationSelect
# 36 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 37 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 38 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_FerryRegularLocationSelect::
# 39 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_0x8004, 0
# 40 "data/maps/LilycoveCity_Harbor/scripts.pory"
	special ScriptMenu_CreateLilycoveSSTidalMultichoice
# 41 "data/maps/LilycoveCity_Harbor/scripts.pory"
	special GetLilycoveSSTidalSelection
# 42 "data/maps/LilycoveCity_Harbor/scripts.pory"
	switch VAR_RESULT
# 43 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 0, LilycoveCity_Harbor_EventScript_GoToSlateport
# 44 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 1, LilycoveCity_Harbor_EventScript_GoToBattleFrontier
# 45 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 2, LilycoveCity_Harbor_EventScript_GoToSouthernIsland
# 46 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 3, LilycoveCity_Harbor_EventScript_GoToNavelRock
# 47 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 4, LilycoveCity_Harbor_EventScript_GoToBirthIsland
# 48 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 5, LilycoveCity_Harbor_EventScript_GoToFarawayIsland
# 49 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 6, LilycoveCity_Harbor_EventScript_ExitSailSelect
# 50 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case MULTI_B_PRESSED, LilycoveCity_Harbor_EventScript_ExitSailSelect
# 51 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 52 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 53 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToSouthernIsland::
# 54 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 55 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_SOUTHERN_ISLAND_EXTERIOR, 13, 22
# 56 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 57 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 58 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 59 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 60 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToNavelRock::
# 61 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 62 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_NAVEL_ROCK_HARBOR, 8, 4
# 63 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 64 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 65 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 66 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 67 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToBirthIsland::
# 68 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 69 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_BIRTH_ISLAND_HARBOR, 8, 4
# 70 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 71 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 72 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 73 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 74 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToFarawayIsland::
# 75 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 76 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_FARAWAY_ISLAND_ENTRANCE, 13, 38
# 77 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 78 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 79 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 80 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 81 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToSlateport::
# 82 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_SlateportItIs, MSGBOX_YESNO
# 83 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, NO, LilycoveCity_Harbor_EventScript_FerryDestinationChangeMind
# 84 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_BOARD_LILYCOVE
# 85 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 86 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_SS_TIDAL_CORRIDOR, 1, 10
# 87 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 88 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 89 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 90 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 91 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToBattleFrontier::
# 92 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_BattleFrontierItIs, MSGBOX_YESNO
# 93 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, NO, LilycoveCity_Harbor_EventScript_FerryDestinationChangeMind
# 94 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 95 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_BATTLE_FRONTIER_OUTSIDE_WEST, 19, 67
# 96 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 97 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 98 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 99 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 100 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetEonTicketState::
# 101 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_E, 0
# 102 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_unset FLAG_ENABLE_SHIP_SOUTHERN_ISLAND, Common_EventScript_NopReturn
# 103 "data/maps/LilycoveCity_Harbor/scripts.pory"
	checkitem ITEM_EON_TICKET
# 104 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
# 105 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_E, 1
# 106 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_set FLAG_SHOWN_EON_TICKET, Common_EventScript_NopReturn
# 107 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_E, 2
# 108 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 109 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 110 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetAuroraTicketState::
# 111 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_D, 0
# 112 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_unset FLAG_ENABLE_SHIP_BIRTH_ISLAND, Common_EventScript_NopReturn
# 113 "data/maps/LilycoveCity_Harbor/scripts.pory"
	checkitem ITEM_AURORA_TICKET
# 114 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
# 115 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_D, 1
# 116 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_set FLAG_SHOWN_AURORA_TICKET, Common_EventScript_NopReturn
# 117 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_D, 2
# 118 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 119 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 120 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetOldSeaMapState::
# 121 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_C, 0
# 122 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_unset FLAG_ENABLE_SHIP_FARAWAY_ISLAND, Common_EventScript_NopReturn
# 123 "data/maps/LilycoveCity_Harbor/scripts.pory"
	checkitem ITEM_OLD_SEA_MAP
# 124 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
# 125 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_C, 1
# 126 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_set FLAG_SHOWN_OLD_SEA_MAP, Common_EventScript_NopReturn
# 127 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_C, 2
# 128 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 129 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 130 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetMysticTicketState::
# 131 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_9, 0
# 132 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_unset FLAG_ENABLE_SHIP_NAVEL_ROCK, Common_EventScript_NopReturn
# 133 "data/maps/LilycoveCity_Harbor/scripts.pory"
	checkitem ITEM_MYSTIC_TICKET
# 134 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn
# 135 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_9, 1
# 136 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_set FLAG_SHOWN_MYSTIC_TICKET, Common_EventScript_NopReturn
# 137 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_9, 2
# 138 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 139 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 140 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetFirstTimeShowingTicket::
# 141 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_B, 0
# 142 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_E, 2, LilycoveCity_Harbor_EventScript_SetFirstTimeShowingEonTicket
# 143 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_D, 2, LilycoveCity_Harbor_EventScript_SetFirstTimeShowingAuroraTicket
# 144 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_C, 2, LilycoveCity_Harbor_EventScript_SetFirstTimeShowingOldSeaMap
# 145 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_9, 2, LilycoveCity_Harbor_EventScript_SetFirstTimeShowingMysticTicket
# 146 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 147 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 148 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetFirstTimeShowingEonTicket::
# 149 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_B, 1
# 150 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 151 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 152 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetFirstTimeShowingAuroraTicket::
# 153 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_B, 2
# 154 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 155 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 156 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetFirstTimeShowingOldSeaMap::
# 157 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_B, 4
# 158 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 159 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 160 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetFirstTimeShowingMysticTicket::
# 161 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_B, 8
# 162 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 163 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 164 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetHasTicketsState::
# 165 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_TEMP_A, 0
# 166 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_E, 1, LilycoveCity_Harbor_EventScript_SetHasEonTicket
# 167 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_D, 1, LilycoveCity_Harbor_EventScript_SetHasAuroraTicket
# 168 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_C, 1, LilycoveCity_Harbor_EventScript_SetHasOldSeaMap
# 169 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_TEMP_9, 1, LilycoveCity_Harbor_EventScript_SetHasMysticTicket
# 170 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 171 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 172 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetHasEonTicket::
# 173 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_A, 1
# 174 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 175 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 176 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetHasAuroraTicket::
# 177 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_A, 2
# 178 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 179 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 180 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetHasOldSeaMap::
# 181 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_A, 4
# 182 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 183 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 184 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SetHasMysticTicket::
# 185 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addvar VAR_TEMP_A, 8
# 186 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 187 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 188 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_EonTicketFirstTime::
# 189 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setflag FLAG_SHOWN_EON_TICKET
# 190 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_ThatPass, MSGBOX_DEFAULT
# 191 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 192 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetEventTicketSailor
# 193 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_ShowEonTicket, MSGBOX_DEFAULT
# 194 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_GoToSouthernIslandFirstTime
# 195 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 196 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 197 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToSouthernIslandFirstTime::
# 198 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 199 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerryWithSailor
# 200 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_SOUTHERN_ISLAND_EXTERIOR, 13, 22
# 201 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 202 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 203 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 204 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 205 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_AuroraTicketFirstTime::
# 206 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setflag FLAG_SHOWN_AURORA_TICKET
# 207 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_ThatPass, MSGBOX_DEFAULT
# 208 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 209 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetEventTicketSailor
# 210 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_OddTicketGetOnBoard, MSGBOX_DEFAULT
# 211 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_GoToBirthIslandFirstTime
# 212 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 213 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 214 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToBirthIslandFirstTime::
# 215 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 216 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerryWithSailor
# 217 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_BIRTH_ISLAND_HARBOR, 8, 4
# 218 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 219 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 220 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 221 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 222 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_OldSeaMapFirstTime::
# 223 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setflag FLAG_SHOWN_OLD_SEA_MAP
# 224 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_ShowOldSeaMap, MSGBOX_DEFAULT
# 225 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 226 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetEventTicketSailor
# 227 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_OldSeaMapTooFar, MSGBOX_DEFAULT
# 228 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 229 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, Common_Movement_WalkInPlaceFasterUp
# 230 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 231 "data/maps/LilycoveCity_Harbor/scripts.pory"
	playse SE_PIN
# 232 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, Common_Movement_ExclamationMark
# 233 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 234 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, Common_Movement_Delay48
# 235 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 236 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, LilycoveCity_Harbor_EventScript_MoveSailorOutOfWayNorth
# 237 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, LilycoveCity_Harbor_EventScript_MoveSailorOutOfWayEast
# 238 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addobject LOCALID_LILYCOVE_HARBOR_BRINEY
# 239 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, LilycoveCity_Harbor_EventScript_BrineyFaceSailorNorth
# 240 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, LilycoveCity_Harbor_EventScript_BrineyFaceSailorEast
# 241 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_BrineyHoldOnASecond, MSGBOX_DEFAULT
# 242 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, LilycoveCity_Harbor_EventScript_BrineyFacePlayerNorth
# 243 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, LilycoveCity_Harbor_EventScript_BrineyFacePlayerEast
# 244 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_BrineyLetsSail, MSGBOX_DEFAULT
# 245 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 246 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, LilycoveCity_Harbor_EventScript_BoardFerryWithBrineyAndSailorNorth
# 247 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, LilycoveCity_Harbor_EventScript_BoardFerryWithBrineyAndSailorEast
# 248 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_LILYCOVE_HARBOR_SS_TIDAL
# 249 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call Common_EventScript_FerryDepart
# 250 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_FARAWAY_ISLAND_ENTRANCE, 13, 38
# 251 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 252 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 253 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 254 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 255 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToFarawayIslandFirstTime::
# 256 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 257 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerryWithSailor
# 258 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_FARAWAY_ISLAND_ENTRANCE, 13, 38
# 259 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 260 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 261 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 262 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 263 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_MysticTicketFirstTime::
# 264 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setflag FLAG_SHOWN_MYSTIC_TICKET
# 265 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_ThatPass, MSGBOX_DEFAULT
# 266 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 267 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetEventTicketSailor
# 268 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_OddTicketGetOnBoard, MSGBOX_DEFAULT
# 269 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_GoToNavelRockFirstTime
# 270 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 271 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 272 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToNavelRockFirstTime::
# 273 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 274 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerryWithSailor
# 275 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_NAVEL_ROCK_HARBOR, 8, 4
# 276 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 277 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 278 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 279 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 280 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_MultipleEventTicketsFirstTime::
# 281 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_ThatPass, MSGBOX_DEFAULT
# 282 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 283 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_GetEventTicketSailor
# 284 "data/maps/LilycoveCity_Harbor/scripts.pory"
	message EventTicket_Text_OddTicketsWhereTo
# 285 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmessage
# 286 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_0x8004, 1
# 287 "data/maps/LilycoveCity_Harbor/scripts.pory"
	special ScriptMenu_CreateLilycoveSSTidalMultichoice
# 288 "data/maps/LilycoveCity_Harbor/scripts.pory"
	special GetLilycoveSSTidalSelection
# 289 "data/maps/LilycoveCity_Harbor/scripts.pory"
	switch VAR_RESULT
# 290 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 2, LilycoveCity_Harbor_EventScript_GoToSouthernIslandFirstTime
# 291 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 3, LilycoveCity_Harbor_EventScript_GoToNavelRockFirstTime
# 292 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 4, LilycoveCity_Harbor_EventScript_GoToBirthIslandFirstTime
# 293 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 5, LilycoveCity_Harbor_EventScript_GoToFarawayIslandFirstTime
# 294 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case 6, LilycoveCity_Harbor_EventScript_ExitFirstTimeTicketSailSelect
# 295 "data/maps/LilycoveCity_Harbor/scripts.pory"
	case MULTI_B_PRESSED, LilycoveCity_Harbor_EventScript_ExitFirstTimeTicketSailSelect
# 296 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 297 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 298 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 299 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_ExitFirstTimeTicketSailSelect::
# 300 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox EventTicket_Text_AsYouLike, MSGBOX_DEFAULT
# 301 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 302 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, Common_Movement_WalkInPlaceFasterUp
# 303 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 304 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 305 "data/maps/LilycoveCity_Harbor/scripts.pory"
	removeobject LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR
# 306 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 307 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_ATTENDANT, Common_Movement_WalkInPlaceFasterDown
# 308 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 309 "data/maps/LilycoveCity_Harbor/scripts.pory"
	showobjectat LOCALID_LILYCOVE_HARBOR_ATTENDANT, MAP_LILYCOVE_CITY_HARBOR
# 310 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 311 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_SailAnotherTime, MSGBOX_DEFAULT
# 312 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 313 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 314 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 315 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GetEventTicketSailor::
# 316 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterUp
# 317 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 318 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 319 "data/maps/LilycoveCity_Harbor/scripts.pory"
	hideobjectat VAR_LAST_TALKED, MAP_LILYCOVE_CITY_HARBOR
# 320 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 60
# 321 "data/maps/LilycoveCity_Harbor/scripts.pory"
	addobject LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR
# 322 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 323 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, Common_Movement_FacePlayer
# 324 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 325 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 326 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 327 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BoardFerryWithSailor::
# 328 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, Common_Movement_WalkInPlaceFasterUp
# 329 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 330 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 331 "data/maps/LilycoveCity_Harbor/scripts.pory"
	removeobject LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR
# 332 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, LilycoveCity_Harbor_EventScript_PlayerBoardFerryNorth
# 333 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, LilycoveCity_Harbor_EventScript_PlayerBoardFerryEast
# 334 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 335 "data/maps/LilycoveCity_Harbor/scripts.pory"
	hideplayer
# 336 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_LILYCOVE_HARBOR_SS_TIDAL
# 337 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call Common_EventScript_FerryDepart
# 338 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 339 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 340 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_FerryUnavailable::
# 341 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_FerryUnavailable, MSGBOX_DEFAULT
# 342 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 343 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 344 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 345 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_NoEventTickets::
# 346 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_MayISeeYourTicket, MSGBOX_DEFAULT
# 347 "data/maps/LilycoveCity_Harbor/scripts.pory"
	message LilycoveCity_Harbor_Text_FlashTicketWhereTo
# 348 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmessage
# 349 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_FerryRegularLocationSelect
# 350 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 351 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 352 "data/maps/LilycoveCity_Harbor/scripts.pory"
@ Unused
# 353 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_NoTicket::
# 354 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_NoTicket, MSGBOX_DEFAULT
# 355 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 356 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 357 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 358 "data/maps/LilycoveCity_Harbor/scripts.pory"
@ Unused
# 359 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToSlateportUnused::
# 360 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_SlateportItIs, MSGBOX_YESNO
# 361 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, NO, LilycoveCity_Harbor_EventScript_FerryDestinationChangeMind
# 362 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_SS_TIDAL_STATE, SS_TIDAL_BOARD_LILYCOVE
# 363 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 364 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_SS_TIDAL_CORRIDOR, 1, 10
# 365 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 366 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 367 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 368 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 369 "data/maps/LilycoveCity_Harbor/scripts.pory"
@ Unused
# 370 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_GoToBattleFrontierUnused::
# 371 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_BattleFrontierItIs, MSGBOX_YESNO
# 372 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_eq VAR_RESULT, NO, LilycoveCity_Harbor_EventScript_FerryDestinationChangeMind
# 373 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call LilycoveCity_Harbor_EventScript_BoardFerry
# 374 "data/maps/LilycoveCity_Harbor/scripts.pory"
	warp MAP_BATTLE_FRONTIER_OUTSIDE_WEST, 19, 67
# 375 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitstate
# 376 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 377 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 378 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 379 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_FerryDestinationChangeMind::
# 380 "data/maps/LilycoveCity_Harbor/scripts.pory"
	message LilycoveCity_Harbor_Text_WhereWouldYouLikeToGo
# 381 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmessage
# 382 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto LilycoveCity_Harbor_EventScript_FerryRegularLocationSelect
# 383 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 384 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 385 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BoardFerry::
# 386 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_PleaseBoard, MSGBOX_DEFAULT
# 387 "data/maps/LilycoveCity_Harbor/scripts.pory"
	closemessage
# 388 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterUp
# 389 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 390 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 391 "data/maps/LilycoveCity_Harbor/scripts.pory"
	hideobjectat VAR_LAST_TALKED, MAP_LILYCOVE_CITY_HARBOR
# 392 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, LilycoveCity_Harbor_EventScript_PlayerBoardFerryNorth
# 393 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, LilycoveCity_Harbor_EventScript_PlayerBoardFerryEast
# 394 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay 30
# 395 "data/maps/LilycoveCity_Harbor/scripts.pory"
	hideplayer
# 396 "data/maps/LilycoveCity_Harbor/scripts.pory"
	setvar VAR_0x8004, LOCALID_LILYCOVE_HARBOR_SS_TIDAL
# 397 "data/maps/LilycoveCity_Harbor/scripts.pory"
	call Common_EventScript_FerryDepart
# 398 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 399 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 400 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_PlayerBoardFerryEast::
# 401 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_PLAYER, LilycoveCity_Harbor_Movement_PlayerBoardFerryEast
# 402 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 403 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 404 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 405 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_PlayerBoardFerryNorth::
# 406 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_PLAYER, LilycoveCity_Harbor_Movement_PlayerBoardFerryNorth
# 407 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 408 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 409 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 410 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_ExitSailSelect::
# 411 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_SailAnotherTime, MSGBOX_DEFAULT
# 412 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 413 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 414 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 415 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_PlayerBoardFerryEast:
# 416 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_right
# 417 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_in_place_faster_up
# 418 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 419 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 420 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_PlayerBoardFerryNorth:
# 421 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_up
# 422 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 423 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 424 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_UnusedBoardFerry:
# 425 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_up
# 426 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 427 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 428 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_Sailor::
# 429 "data/maps/LilycoveCity_Harbor/scripts.pory"
	lock
# 430 "data/maps/LilycoveCity_Harbor/scripts.pory"
	faceplayer
# 431 "data/maps/LilycoveCity_Harbor/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_Harbor_EventScript_SailorFerryAvailable
# 432 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_SailorFerryUnavailable, MSGBOX_DEFAULT
# 433 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 434 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 435 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 436 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_SailorFerryAvailable::
# 437 "data/maps/LilycoveCity_Harbor/scripts.pory"
	msgbox LilycoveCity_Harbor_Text_SailorFerryAvailable, MSGBOX_DEFAULT
# 438 "data/maps/LilycoveCity_Harbor/scripts.pory"
	release
# 439 "data/maps/LilycoveCity_Harbor/scripts.pory"
	end
# 440 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 441 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_MoveSailorOutOfWayNorth::
# 442 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, LilycoveCity_Harbor_Movement_SailorOutOfWayNorth
# 443 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 444 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 445 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 446 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_MoveSailorOutOfWayEast::
# 447 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, LilycoveCity_Harbor_Movement_SailorOutOfWayEast
# 448 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 449 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 450 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 451 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_SailorOutOfWayNorth:
# 452 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_in_place_faster_right
# 453 "data/maps/LilycoveCity_Harbor/scripts.pory"
	lock_facing_direction
# 454 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_left
# 455 "data/maps/LilycoveCity_Harbor/scripts.pory"
	unlock_facing_direction
# 456 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 457 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 458 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_SailorOutOfWayEast:
# 459 "data/maps/LilycoveCity_Harbor/scripts.pory"
	lock_facing_direction
# 460 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_down
# 461 "data/maps/LilycoveCity_Harbor/scripts.pory"
	unlock_facing_direction
# 462 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 463 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 464 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BrineyFaceSailorNorth::
# 465 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_BRINEY, Common_Movement_WalkInPlaceFasterLeft
# 466 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 467 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 468 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 469 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BrineyFaceSailorEast::
# 470 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_BRINEY, Common_Movement_WalkInPlaceFasterDown
# 471 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 472 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 473 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 474 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BrineyFacePlayerNorth::
# 475 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_BRINEY, Common_Movement_WalkInPlaceFasterDown
# 476 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 477 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 478 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 479 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BrineyFacePlayerEast::
# 480 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_BRINEY, Common_Movement_WalkInPlaceFasterLeft
# 481 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 482 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 483 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 484 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BoardFerryWithBrineyAndSailorNorth::
# 485 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_BRINEY, LilycoveCity_Harbor_Movement_BrineyBoardFerry
# 486 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_PLAYER, LilycoveCity_Harbor_Movement_PlayerBoardWithBrineyNorth
# 487 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, LilycoveCity_Harbor_Movement_SailorBoardWithBrineyNorth
# 488 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 489 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 490 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 491 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_EventScript_BoardFerryWithBrineyAndSailorEast::
# 492 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_BRINEY, LilycoveCity_Harbor_Movement_BrineyBoardFerry
# 493 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_PLAYER, LilycoveCity_Harbor_Movement_PlayerBoardWithBrineyEast
# 494 "data/maps/LilycoveCity_Harbor/scripts.pory"
	applymovement LOCALID_LILYCOVE_HARBOR_FERRY_SAILOR, LilycoveCity_Harbor_Movement_SailorBoardWithBrineyEast
# 495 "data/maps/LilycoveCity_Harbor/scripts.pory"
	waitmovement 0
# 496 "data/maps/LilycoveCity_Harbor/scripts.pory"
	return
# 497 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 498 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_BrineyBoardFerry:
# 499 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_in_place_faster_up
# 500 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_8
# 501 "data/maps/LilycoveCity_Harbor/scripts.pory"
	set_invisible
# 502 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 503 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 504 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_PlayerBoardWithBrineyNorth:
# 505 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 506 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_up
# 507 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 508 "data/maps/LilycoveCity_Harbor/scripts.pory"
	set_invisible
# 509 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 510 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 511 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_SailorBoardWithBrineyNorth:
# 512 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 513 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 514 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 515 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_right
# 516 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_in_place_faster_up
# 517 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 518 "data/maps/LilycoveCity_Harbor/scripts.pory"
	set_invisible
# 519 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 520 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 521 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_PlayerBoardWithBrineyEast:
# 522 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 523 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_right
# 524 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_in_place_faster_up
# 525 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 526 "data/maps/LilycoveCity_Harbor/scripts.pory"
	set_invisible
# 527 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 528 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 529 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Movement_SailorBoardWithBrineyEast:
# 530 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 531 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 532 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 533 "data/maps/LilycoveCity_Harbor/scripts.pory"
	walk_up
# 534 "data/maps/LilycoveCity_Harbor/scripts.pory"
	delay_16
# 535 "data/maps/LilycoveCity_Harbor/scripts.pory"
	set_invisible
# 536 "data/maps/LilycoveCity_Harbor/scripts.pory"
	step_end
# 537 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 538 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_FerryUnavailable:
# 539 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "I beg your pardon?\n"
# 540 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "You're looking for a ship?\p"
# 541 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "I'm sorry, the ferry service isn't\n"
# 542 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "available at present…$"
# 543 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 544 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_MayISeeYourTicket:
# 545 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Hello, are you here for the ferry?\n"
# 546 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "May I see your TICKET?$"
# 547 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 548 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_NoTicket:
# 549 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "{PLAYER} doesn't have the TICKET…\p"
# 550 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "I'm terribly sorry.\p"
# 551 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "You must have a TICKET to board\n"
# 552 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "the ferry.$"
# 553 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 554 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_FlashTicketWhereTo:
# 555 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "{PLAYER} flashed the TICKET.\p"
# 556 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Perfect! That's all you need!\p"
# 557 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "And where would you like to go?$"
# 558 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 559 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_SailAnotherTime:
# 560 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Please sail with us another time!$"
# 561 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 562 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_SlateportItIs:
# 563 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "SLATEPORT CITY it is, then!$"
# 564 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 565 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_BattleFrontierItIs:
# 566 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "BATTLE FRONTIER it is, then!$"
# 567 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 568 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_PleaseBoard:
# 569 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Please board the ferry and wait for\n"
# 570 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "departure.$"
# 571 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 572 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_WhereWouldYouLikeToGo:
# 573 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Then, where would you like to go?$"
# 574 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 575 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_SailorFerryUnavailable:
# 576 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Until they finish making the ferry,\n"
# 577 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "we sailors have nothing to do…\p"
# 578 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "I wish they'd get a move on, the folks\n"
# 579 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "at the SHIPYARD in SLATEPORT.$"
# 580 "data/maps/LilycoveCity_Harbor/scripts.pory"

# 581 "data/maps/LilycoveCity_Harbor/scripts.pory"
LilycoveCity_Harbor_Text_SailorFerryAvailable:
# 582 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "The ferry S.S. TIDAL is finally in\n"
# 583 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "operation.\p"
# 584 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "The folks at the SHIPYARD in SLATEPORT\n"
# 585 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "must've worked extra hard.\p"
# 586 "data/maps/LilycoveCity_Harbor/scripts.pory"
	.string "Well, it's my turn to get busy now!$"
