MtEmber_Summit_MapScripts::
	.byte 0


# 3 "data/maps/MtEmber_Summit/scripts.pory"

# 4 "data/maps/MtEmber_Summit/scripts.pory"
MtEmber_Summit_EventScript_EdgeWarp_9_15::
# 5 "data/maps/MtEmber_Summit/scripts.pory"
	specialvar VAR_RESULT, GetPlayerFacingDirection
# 6 "data/maps/MtEmber_Summit/scripts.pory"
	goto_if_ne VAR_RESULT, DIR_SOUTH, Sevii_EventScript_End
# 7 "data/maps/MtEmber_Summit/scripts.pory"
	warp MAP_MT_EMBER_EXTERIOR, 4
# 8 "data/maps/MtEmber_Summit/scripts.pory"
	waitstate
# 9 "data/maps/MtEmber_Summit/scripts.pory"
	end
