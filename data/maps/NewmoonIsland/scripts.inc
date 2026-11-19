# 1 "data/maps/NewmoonIsland/scripts.pory"

# 2 "data/maps/NewmoonIsland/scripts.pory"
NewmoonIsland_MapScripts::
# 3 "data/maps/NewmoonIsland/scripts.pory"
	.byte 0
# 4 "data/maps/NewmoonIsland/scripts.pory"

# 5 "data/maps/NewmoonIsland/scripts.pory"
NewmoonIsland_EventScript_EnterForest::
# 6 "data/maps/NewmoonIsland/scripts.pory"
	lockall
# 7 "data/maps/NewmoonIsland/scripts.pory"
	warp MAP_NEWMOON_ISLAND_INTERIOR, 0
# 8 "data/maps/NewmoonIsland/scripts.pory"
	waitstate
# 9 "data/maps/NewmoonIsland/scripts.pory"
	releaseall
# 10 "data/maps/NewmoonIsland/scripts.pory"
	end
# 11 "data/maps/NewmoonIsland/scripts.pory"

# 12 "data/maps/NewmoonIsland/scripts.pory"
NewmoonIsland_EventScript_EnterForest2::
# 13 "data/maps/NewmoonIsland/scripts.pory"
	lockall
# 14 "data/maps/NewmoonIsland/scripts.pory"
	warp MAP_NEWMOON_ISLAND_INTERIOR, 1
# 15 "data/maps/NewmoonIsland/scripts.pory"
	waitstate
# 16 "data/maps/NewmoonIsland/scripts.pory"
	releaseall
# 17 "data/maps/NewmoonIsland/scripts.pory"
	end
