TosaPort_BrendansHouse_2F_MapScripts::
	.byte 0


TosaPortStation_Attendant::
# 10 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	lock
# 11 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	faceplayer
# 12 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	settrainstation TRAIN_STATION_TEST_EAST, TRAIN_ACCESS_OPEN
# 13 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	usetrain
# 14 "data/maps/TosaPort_BrendansHouse_2F/scripts.pory"
	release
	end

