TrainTestWest_MapScripts::
	.byte 0

@ Shared by all three Tosa Rail test stations (TrainTestWest/East/North).
TrainTest_EventScript_Attendant::
	lock
	faceplayer
	usetrain
	release
	end

@ Debug helper: flips station access so the greyed / closed / open states can be tested.
TrainTest_EventScript_StationMaster::
	lock
	faceplayer
	checkitem ITEM_RAIL_CARD
	goto_if_eq VAR_RESULT, TRUE, TrainTest_EventScript_StationMasterMenu
	giveitem ITEM_RAIL_CARD
TrainTest_EventScript_StationMasterMenu::
	message TrainTest_Text_StationMaster
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, TrainTest_Text_OpenEast, TrainTest_Text_LockEast, TrainTest_Text_OpenNorth, TrainTest_Text_CloseNorth, TrainTest_Text_LockNorth
	switch VAR_RESULT
	case 0, TrainTest_EventScript_OpenEast
	case 1, TrainTest_EventScript_LockEast
	case 2, TrainTest_EventScript_OpenNorth
	case 3, TrainTest_EventScript_CloseNorth
	case 4, TrainTest_EventScript_LockNorth
	release
	end

TrainTest_EventScript_OpenEast::
	settrainstation TRAIN_STATION_TEST_EAST, TRAIN_ACCESS_OPEN
	goto TrainTest_EventScript_Done
TrainTest_EventScript_LockEast::
	settrainstation TRAIN_STATION_TEST_EAST, TRAIN_ACCESS_LOCKED
	goto TrainTest_EventScript_Done
TrainTest_EventScript_OpenNorth::
	settrainstation TRAIN_STATION_TEST_NORTH, TRAIN_ACCESS_OPEN
	goto TrainTest_EventScript_Done
TrainTest_EventScript_CloseNorth::
	settrainstation TRAIN_STATION_TEST_NORTH, TRAIN_ACCESS_CLOSED
	goto TrainTest_EventScript_Done
TrainTest_EventScript_LockNorth::
	settrainstation TRAIN_STATION_TEST_NORTH, TRAIN_ACCESS_LOCKED
	goto TrainTest_EventScript_Done

TrainTest_EventScript_Done::
	msgbox TrainTest_Text_Done, MSGBOX_DEFAULT
	release
	end

TrainTest_Text_StationMaster:
	.string "STATION MASTER: Which line should\n"
	.string "I change?$"
TrainTest_Text_OpenEast:
	.string "OPEN EAST$"
TrainTest_Text_LockEast:
	.string "LOCK EAST$"
TrainTest_Text_OpenNorth:
	.string "OPEN NORTH$"
TrainTest_Text_CloseNorth:
	.string "CLOSE NORTH$"
TrainTest_Text_LockNorth:
	.string "LOCK NORTH$"
TrainTest_Text_Done:
	.string "Done! Ask the attendant.$"
