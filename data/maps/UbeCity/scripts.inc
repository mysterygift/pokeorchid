# 1 "data/maps/UbeCity/scripts.pory"

# 2 "data/maps/UbeCity/scripts.pory"
UbeCity_MapScripts::
# 3 "data/maps/UbeCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, UbeCity_OnTransition
# 4 "data/maps/UbeCity/scripts.pory"
	.byte 0
# 5 "data/maps/UbeCity/scripts.pory"

# 6 "data/maps/UbeCity/scripts.pory"
UbeCity_OnTransition:
# 7 "data/maps/UbeCity/scripts.pory"
	setflag FLAG_VISITED_UBE_CITY
# 8 "data/maps/UbeCity/scripts.pory"
	end
# 9 "data/maps/UbeCity/scripts.pory"

# 10 "data/maps/UbeCity/scripts.pory"
UbeCity_EventScript_Sign0::
# 11 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_Text_Sign0, MSGBOX_SIGN
# 12 "data/maps/UbeCity/scripts.pory"
	end
# 13 "data/maps/UbeCity/scripts.pory"

# 14 "data/maps/UbeCity/scripts.pory"
UbeCity_EventScript_Sign1::
# 15 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_Text_Sign1, MSGBOX_SIGN
# 16 "data/maps/UbeCity/scripts.pory"
	end
# 17 "data/maps/UbeCity/scripts.pory"

# 18 "data/maps/UbeCity/scripts.pory"
UbeCity_Text_Sign0:
# 19 "data/maps/UbeCity/scripts.pory"
	.string "UBE CITY\n"
# 20 "data/maps/UbeCity/scripts.pory"
	.string "TIKSI's only city.$"
# 21 "data/maps/UbeCity/scripts.pory"

# 22 "data/maps/UbeCity/scripts.pory"
UbeCity_Text_Sign1:
# 23 "data/maps/UbeCity/scripts.pory"
	.string "SILPH CO. TIKSI SALES OFFICE\n"
# 24 "data/maps/UbeCity/scripts.pory"
	.string "Closed today.$"

UbeCity_EventScript_TiksiNpc1::
# 31 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_EventScript_TiksiNpc1_Text_0, MSGBOX_NPC
	return


UbeCity_EventScript_TiksiNpc2::
# 35 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_EventScript_TiksiNpc2_Text_0, MSGBOX_NPC
	return


UbeCity_EventScript_TiksiNpc3::
# 39 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_EventScript_TiksiNpc3_Text_0, MSGBOX_NPC
	return


UbeCity_EventScript_TiksiNpc4::
# 43 "data/maps/UbeCity/scripts.pory"
	msgbox UbeCity_EventScript_TiksiNpc4_Text_0, MSGBOX_NPC
	return


UbeCity_EventScript_TiksiNpc1_Text_0:
# 31 "data/maps/UbeCity/scripts.pory"
	.string "Silph Co.'s Tiksi office! Well… it's more\n"
	.string "of a cupboard. Sales have been slow.$"

UbeCity_EventScript_TiksiNpc2_Text_0:
# 35 "data/maps/UbeCity/scripts.pory"
	.string "Ube's the only city in Tiksi. Which is why\n"
	.string "it's the only place with a decent cup of\l"
	.string "tea.$"

UbeCity_EventScript_TiksiNpc3_Text_0:
# 39 "data/maps/UbeCity/scripts.pory"
	.string "The guardians keep watch at the old\n"
	.string "shrines. If they're standing at the\l"
	.string "doors, something's very wrong.$"

UbeCity_EventScript_TiksiNpc4_Text_0:
# 43 "data/maps/UbeCity/scripts.pory"
	.string "My dad says Tosa people think we're\n"
	.string "backward. We've got a fountain! Have\l"
	.string "they got a fountain?$"
