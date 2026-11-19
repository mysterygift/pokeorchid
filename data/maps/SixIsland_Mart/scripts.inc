SixIsland_Mart_MapScripts::
	.byte 0


# 3 "data/maps/SixIsland_Mart/scripts.pory"

# 4 "data/maps/SixIsland_Mart/scripts.pory"
SixIsland_Mart_EventScript_Clerk::
# 5 "data/maps/SixIsland_Mart/scripts.pory"
	lock
# 6 "data/maps/SixIsland_Mart/scripts.pory"
	faceplayer
# 7 "data/maps/SixIsland_Mart/scripts.pory"
	message gText_HowMayIServeYou
# 8 "data/maps/SixIsland_Mart/scripts.pory"
	waitmessage
# 9 "data/maps/SixIsland_Mart/scripts.pory"
	pokemart SeviiMart_Items
# 10 "data/maps/SixIsland_Mart/scripts.pory"
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
# 11 "data/maps/SixIsland_Mart/scripts.pory"
	release
# 12 "data/maps/SixIsland_Mart/scripts.pory"
	end
