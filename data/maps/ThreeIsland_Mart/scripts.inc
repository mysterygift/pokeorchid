ThreeIsland_Mart_MapScripts::
	.byte 0


# 3 "data/maps/ThreeIsland_Mart/scripts.pory"

# 4 "data/maps/ThreeIsland_Mart/scripts.pory"
ThreeIsland_Mart_EventScript_Clerk::
# 5 "data/maps/ThreeIsland_Mart/scripts.pory"
	lock
# 6 "data/maps/ThreeIsland_Mart/scripts.pory"
	faceplayer
# 7 "data/maps/ThreeIsland_Mart/scripts.pory"
	message gText_HowMayIServeYou
# 8 "data/maps/ThreeIsland_Mart/scripts.pory"
	waitmessage
# 9 "data/maps/ThreeIsland_Mart/scripts.pory"
	pokemart SeviiMart_Items
# 10 "data/maps/ThreeIsland_Mart/scripts.pory"
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
# 11 "data/maps/ThreeIsland_Mart/scripts.pory"
	release
# 12 "data/maps/ThreeIsland_Mart/scripts.pory"
	end
