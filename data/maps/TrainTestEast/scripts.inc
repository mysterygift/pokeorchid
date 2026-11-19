TrainTestEast_MapScripts::
	.byte 0

@ Debug room for Tosa Rail (TrainTestEast/North, debug warp group gMapGroup_TrainTest). These maps
@ are no longer stations: the station master flips access on the real network so the greyed /
@ closed / open states can be tested from any station.
TrainTest_EventScript_Attendant::
	msgbox TrainTest_Text_NotAStation, MSGBOX_NPC
	end

TrainTest_EventScript_StationMaster::
	lock
	faceplayer
	checkitem ITEM_RAIL_CARD
	goto_if_eq VAR_RESULT, TRUE, TrainTest_EventScript_StationMasterMenu
	giveitem ITEM_RAIL_CARD
TrainTest_EventScript_StationMasterMenu::
	message TrainTest_Text_StationMaster
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, TrainTest_Text_OpenAll, TrainTest_Text_LockAll, TrainTest_Text_CloseChangu
	switch VAR_RESULT
	case 0, TrainTest_EventScript_OpenAll
	case 1, TrainTest_EventScript_LockAll
	case 2, TrainTest_EventScript_CloseChangu
	release
	end

TrainTest_EventScript_OpenAll::
	call TosaRail_EventScript_OpenAllStations
	goto TrainTest_EventScript_Done
TrainTest_EventScript_LockAll::
	call TosaRail_EventScript_LockAllStations
	goto TrainTest_EventScript_Done
TrainTest_EventScript_CloseChangu::
	settrainstation TRAIN_STATION_CHANGU_CITY, TRAIN_ACCESS_CLOSED
	goto TrainTest_EventScript_Done

TrainTest_EventScript_Done::
	msgbox TrainTest_Text_Done, MSGBOX_DEFAULT
	release
	end

TrainTest_Text_StationMaster:
	.string "STATION MASTER: What should I do\n"
	.string "with the stations?$"
TrainTest_Text_OpenAll:
	.string "OPEN ALL$"
TrainTest_Text_LockAll:
	.string "LOCK ALL$"
TrainTest_Text_CloseChangu:
	.string "CLOSE CHANGU$"
TrainTest_Text_Done:
	.string "Done! Ride from any station.$"
TrainTest_Text_NotAStation:
	.string "This test room isn't a station any\n"
	.string "more. Board at a real platform.$"
