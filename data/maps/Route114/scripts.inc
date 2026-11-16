# 1 "data/maps/Route114/scripts.pory"

# 2 "data/maps/Route114/scripts.pory"
Route114_MapScripts::
# 3 "data/maps/Route114/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, Route114_OnTransition
# 4 "data/maps/Route114/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, Route114_OnLoad
# 5 "data/maps/Route114/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route114_OnFrame
# 6 "data/maps/Route114/scripts.pory"
	.byte 0
# 7 "data/maps/Route114/scripts.pory"

# 8 "data/maps/Route114/scripts.pory"
Route114_OnTransition:
# 9 "data/maps/Route114/scripts.pory"
	call_if_eq VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_HideMapNamePopup
# 10 "data/maps/Route114/scripts.pory"
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_114_NORTH, AbnormalWeather_StartGroudonWeather
# 11 "data/maps/Route114/scripts.pory"
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_114_SOUTH, AbnormalWeather_StartGroudonWeather
# 12 "data/maps/Route114/scripts.pory"
	end
# 13 "data/maps/Route114/scripts.pory"

# 14 "data/maps/Route114/scripts.pory"
Route114_OnLoad:
# 15 "data/maps/Route114/scripts.pory"
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_114_NORTH, AbnormalWeather_EventScript_PlaceTilesRoute114North
# 16 "data/maps/Route114/scripts.pory"
	call_if_eq VAR_ABNORMAL_WEATHER_LOCATION, ABNORMAL_WEATHER_ROUTE_114_SOUTH, AbnormalWeather_EventScript_PlaceTilesRoute114South
# 17 "data/maps/Route114/scripts.pory"
	end
# 18 "data/maps/Route114/scripts.pory"

# 19 "data/maps/Route114/scripts.pory"
Route114_OnFrame:
# 20 "data/maps/Route114/scripts.pory"
	map_script_2 VAR_SHOULD_END_ABNORMAL_WEATHER, 1, AbnormalWeather_EventScript_EndEventAndCleanup_1
# 21 "data/maps/Route114/scripts.pory"
	.2byte 0
# 22 "data/maps/Route114/scripts.pory"

# 23 "data/maps/Route114/scripts.pory"
Route114_EventScript_Man::
# 24 "data/maps/Route114/scripts.pory"
	lock
# 25 "data/maps/Route114/scripts.pory"
	faceplayer
# 26 "data/maps/Route114/scripts.pory"
	dotimebasedevents
# 27 "data/maps/Route114/scripts.pory"
	goto_if_set FLAG_DAILY_ROUTE_114_RECEIVED_BERRY, Route114_EventScript_ReceivedBerry
# 28 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_LoveUsingBerryCrushShareBerry, MSGBOX_DEFAULT
# 29 "data/maps/Route114/scripts.pory"
	giverandomberry BERRY_ID_RAZZ, BERRY_ID_PINAP
# 30 "data/maps/Route114/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 31 "data/maps/Route114/scripts.pory"
	setflag FLAG_DAILY_ROUTE_114_RECEIVED_BERRY
# 32 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_TryBerryCrushWithFriends, MSGBOX_DEFAULT
# 33 "data/maps/Route114/scripts.pory"
	release
# 34 "data/maps/Route114/scripts.pory"
	end
# 35 "data/maps/Route114/scripts.pory"

# 36 "data/maps/Route114/scripts.pory"
Route114_EventScript_ReceivedBerry::
# 37 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_FunToThinkAboutBerries, MSGBOX_DEFAULT
# 38 "data/maps/Route114/scripts.pory"
	release
# 39 "data/maps/Route114/scripts.pory"
	end
# 40 "data/maps/Route114/scripts.pory"

# 41 "data/maps/Route114/scripts.pory"
Route114_EventScript_RoarGentleman::
# 42 "data/maps/Route114/scripts.pory"
	lock
# 43 "data/maps/Route114/scripts.pory"
	faceplayer
# 44 "data/maps/Route114/scripts.pory"
	goto_if_set FLAG_RECEIVED_TM_ROAR, Route114_EventScript_ReceivedRoar
# 45 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_AllMyMonDoesIsRoarTakeThis, MSGBOX_DEFAULT
# 46 "data/maps/Route114/scripts.pory"
	giveitem ITEM_TM_ROAR
# 47 "data/maps/Route114/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 48 "data/maps/Route114/scripts.pory"
	setflag FLAG_RECEIVED_TM_ROAR
# 49 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_ExplainRoar, MSGBOX_DEFAULT
# 50 "data/maps/Route114/scripts.pory"
	release
# 51 "data/maps/Route114/scripts.pory"
	end
# 52 "data/maps/Route114/scripts.pory"

# 53 "data/maps/Route114/scripts.pory"
Route114_EventScript_ReceivedRoar::
# 54 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_ExplainRoar, MSGBOX_DEFAULT
# 55 "data/maps/Route114/scripts.pory"
	release
# 56 "data/maps/Route114/scripts.pory"
	end
# 57 "data/maps/Route114/scripts.pory"

# 58 "data/maps/Route114/scripts.pory"
Route114_EventScript_Poochyena::
# 59 "data/maps/Route114/scripts.pory"
	lock
# 60 "data/maps/Route114/scripts.pory"
	faceplayer
# 61 "data/maps/Route114/scripts.pory"
	waitse
# 62 "data/maps/Route114/scripts.pory"
	playmoncry SPECIES_POOCHYENA, CRY_MODE_ENCOUNTER
# 63 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_Poochyena, MSGBOX_DEFAULT
# 64 "data/maps/Route114/scripts.pory"
	waitmoncry
# 65 "data/maps/Route114/scripts.pory"
	release
# 66 "data/maps/Route114/scripts.pory"
	end
# 67 "data/maps/Route114/scripts.pory"

# 68 "data/maps/Route114/scripts.pory"
Route114_EventScript_MeteorFallsSign::
# 69 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_MeteorFallsSign, MSGBOX_SIGN
# 70 "data/maps/Route114/scripts.pory"
	end
# 71 "data/maps/Route114/scripts.pory"

# 72 "data/maps/Route114/scripts.pory"
Route114_EventScript_FossilManiacsHouseSign::
# 73 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_FossilManiacsHouseSign, MSGBOX_SIGN
# 74 "data/maps/Route114/scripts.pory"
	end
# 75 "data/maps/Route114/scripts.pory"

# 76 "data/maps/Route114/scripts.pory"
Route114_EventScript_LanettesHouseSign::
# 77 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_LanettesHouse, MSGBOX_SIGN
# 78 "data/maps/Route114/scripts.pory"
	end
# 79 "data/maps/Route114/scripts.pory"

# 80 "data/maps/Route114/scripts.pory"
Route114_EventScript_Lenny::
# 81 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_LENNY, Route114_Text_LennyIntro, Route114_Text_LennyDefeat
# 82 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_LennyPostBattle, MSGBOX_AUTOCLOSE
# 83 "data/maps/Route114/scripts.pory"
	end
# 84 "data/maps/Route114/scripts.pory"

# 85 "data/maps/Route114/scripts.pory"
Route114_EventScript_Lucas::
# 86 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_LUCAS_1, Route114_Text_LucasIntro, Route114_Text_LucasDefeat
# 87 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_LucasPostBattle, MSGBOX_AUTOCLOSE
# 88 "data/maps/Route114/scripts.pory"
	end
# 89 "data/maps/Route114/scripts.pory"

# 90 "data/maps/Route114/scripts.pory"
Route114_EventScript_Shane::
# 91 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_SHANE, Route114_Text_ShaneIntro, Route114_Text_ShaneDefeat
# 92 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_ShanePostBattle, MSGBOX_AUTOCLOSE
# 93 "data/maps/Route114/scripts.pory"
	end
# 94 "data/maps/Route114/scripts.pory"

# 95 "data/maps/Route114/scripts.pory"
Route114_EventScript_Nancy::
# 96 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_NANCY, Route114_Text_NancyIntro, Route114_Text_NancyDefeat
# 97 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_NancyPostBattle, MSGBOX_AUTOCLOSE
# 98 "data/maps/Route114/scripts.pory"
	end
# 99 "data/maps/Route114/scripts.pory"

# 100 "data/maps/Route114/scripts.pory"
Route114_EventScript_Steve::
# 101 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_STEVE_1, Route114_Text_SteveIntro, Route114_Text_SteveDefeat, Route114_EventScript_RegisterSteve
# 102 "data/maps/Route114/scripts.pory"
	specialvar VAR_RESULT, ShouldTryRematchBattle
# 103 "data/maps/Route114/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, Route114_EventScript_RematchSteve
# 104 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_StevePostBattle, MSGBOX_DEFAULT
# 105 "data/maps/Route114/scripts.pory"
	release
# 106 "data/maps/Route114/scripts.pory"
	end
# 107 "data/maps/Route114/scripts.pory"

# 108 "data/maps/Route114/scripts.pory"
Route114_EventScript_RegisterSteve::
# 109 "data/maps/Route114/scripts.pory"
	special PlayerFaceTrainerAfterBattle
# 110 "data/maps/Route114/scripts.pory"
	waitmovement 0
# 111 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_SteveRegister, MSGBOX_DEFAULT
# 112 "data/maps/Route114/scripts.pory"
	register_matchcall TRAINER_STEVE_1
# 113 "data/maps/Route114/scripts.pory"
	release
# 114 "data/maps/Route114/scripts.pory"
	end
# 115 "data/maps/Route114/scripts.pory"

# 116 "data/maps/Route114/scripts.pory"
Route114_EventScript_RematchSteve::
# 117 "data/maps/Route114/scripts.pory"
	trainerbattle_rematch TRAINER_STEVE_1, Route114_Text_SteveRematchIntro, Route114_Text_SteveRematchDefeat
# 118 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_StevePostRematch, MSGBOX_AUTOCLOSE
# 119 "data/maps/Route114/scripts.pory"
	end
# 120 "data/maps/Route114/scripts.pory"

# 121 "data/maps/Route114/scripts.pory"
Route114_EventScript_Bernie::
# 122 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_BERNIE_1, Route114_Text_BernieIntro, Route114_Text_BernieDefeat, Route114_EventScript_RegisterBernie
# 123 "data/maps/Route114/scripts.pory"
	specialvar VAR_RESULT, ShouldTryRematchBattle
# 124 "data/maps/Route114/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, Route114_EventScript_RematchBernie
# 125 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_BerniePostBattle, MSGBOX_DEFAULT
# 126 "data/maps/Route114/scripts.pory"
	release
# 127 "data/maps/Route114/scripts.pory"
	end
# 128 "data/maps/Route114/scripts.pory"

# 129 "data/maps/Route114/scripts.pory"
Route114_EventScript_RegisterBernie::
# 130 "data/maps/Route114/scripts.pory"
	special PlayerFaceTrainerAfterBattle
# 131 "data/maps/Route114/scripts.pory"
	waitmovement 0
# 132 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_BernieRegister, MSGBOX_DEFAULT
# 133 "data/maps/Route114/scripts.pory"
	register_matchcall TRAINER_BERNIE_1
# 134 "data/maps/Route114/scripts.pory"
	release
# 135 "data/maps/Route114/scripts.pory"
	end
# 136 "data/maps/Route114/scripts.pory"

# 137 "data/maps/Route114/scripts.pory"
Route114_EventScript_RematchBernie::
# 138 "data/maps/Route114/scripts.pory"
	trainerbattle_rematch TRAINER_BERNIE_1, Route114_Text_BernieRematchIntro, Route114_Text_BernieRematchDefeat
# 139 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_BerniePostRematch, MSGBOX_AUTOCLOSE
# 140 "data/maps/Route114/scripts.pory"
	end
# 141 "data/maps/Route114/scripts.pory"

# 142 "data/maps/Route114/scripts.pory"
Route114_EventScript_Claude::
# 143 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_CLAUDE, Route114_Text_ClaudeIntro, Route114_Text_ClaudeDefeat
# 144 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_ClaudePostBattle, MSGBOX_AUTOCLOSE
# 145 "data/maps/Route114/scripts.pory"
	end
# 146 "data/maps/Route114/scripts.pory"

# 147 "data/maps/Route114/scripts.pory"
Route114_EventScript_Nolan::
# 148 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_NOLAN, Route114_Text_NolanIntro, Route114_Text_NolanDefeat
# 149 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_NolanPostBattle, MSGBOX_AUTOCLOSE
# 150 "data/maps/Route114/scripts.pory"
	end
# 151 "data/maps/Route114/scripts.pory"

# 152 "data/maps/Route114/scripts.pory"
Route114_EventScript_Tyra::
# 153 "data/maps/Route114/scripts.pory"
	trainerbattle_double TRAINER_TYRA_AND_IVY, Route114_Text_TyraIntro, Route114_Text_TyraDefeat, Route114_Text_TyraNotEnoughMons
# 154 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_TyraPostBattle, MSGBOX_AUTOCLOSE
# 155 "data/maps/Route114/scripts.pory"
	end
# 156 "data/maps/Route114/scripts.pory"

# 157 "data/maps/Route114/scripts.pory"
Route114_EventScript_Ivy::
# 158 "data/maps/Route114/scripts.pory"
	trainerbattle_double TRAINER_TYRA_AND_IVY, Route114_Text_IvyIntro, Route114_Text_IvyDefeat, Route114_Text_IvyNotEnoughMons
# 159 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_IvyPostBattle, MSGBOX_AUTOCLOSE
# 160 "data/maps/Route114/scripts.pory"
	end
# 161 "data/maps/Route114/scripts.pory"

# 162 "data/maps/Route114/scripts.pory"
Route114_EventScript_Angelina::
# 163 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_ANGELINA, Route114_Text_AngelinaIntro, Route114_Text_AngelinaDefeat
# 164 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_AngelinaPostBattle, MSGBOX_AUTOCLOSE
# 165 "data/maps/Route114/scripts.pory"
	end
# 166 "data/maps/Route114/scripts.pory"

# 167 "data/maps/Route114/scripts.pory"
Route114_EventScript_Charlotte::
# 168 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_CHARLOTTE, Route114_Text_CharlotteIntro, Route114_Text_CharlotteDefeat
# 169 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_CharlottePostBattle, MSGBOX_AUTOCLOSE
# 170 "data/maps/Route114/scripts.pory"
	end
# 171 "data/maps/Route114/scripts.pory"

# 172 "data/maps/Route114/scripts.pory"
Route114_EventScript_Kai::
# 173 "data/maps/Route114/scripts.pory"
	trainerbattle_single TRAINER_KAI, Route114_Text_KaiIntro, Route114_Text_KaiDefeat
# 174 "data/maps/Route114/scripts.pory"
	msgbox Route114_Text_KaiPostBattle, MSGBOX_AUTOCLOSE
# 175 "data/maps/Route114/scripts.pory"
	end
# 176 "data/maps/Route114/scripts.pory"

# 177 "data/maps/Route114/scripts.pory"
Route114_Text_AllMyMonDoesIsRoarTakeThis:
# 178 "data/maps/Route114/scripts.pory"
	.string "All my POKéMON does is ROAR…\n"
# 179 "data/maps/Route114/scripts.pory"
	.string "No one dares to come near me…\p"
# 180 "data/maps/Route114/scripts.pory"
	.string "Sigh… If you would, please take\n"
# 181 "data/maps/Route114/scripts.pory"
	.string "this TM away…$"
# 182 "data/maps/Route114/scripts.pory"

# 183 "data/maps/Route114/scripts.pory"
Route114_Text_ExplainRoar:
# 184 "data/maps/Route114/scripts.pory"
	.string "TM05 contains ROAR.\n"
# 185 "data/maps/Route114/scripts.pory"
	.string "A ROAR sends POKéMON scurrying.$"
# 186 "data/maps/Route114/scripts.pory"

# 187 "data/maps/Route114/scripts.pory"
Route114_Text_Poochyena:
# 188 "data/maps/Route114/scripts.pory"
	.string "Bow! Bowwow!$"
# 189 "data/maps/Route114/scripts.pory"

# 190 "data/maps/Route114/scripts.pory"
Route114_Text_MeteorFallsSign:
# 191 "data/maps/Route114/scripts.pory"
	.string "METEOR FALLS\n"
# 192 "data/maps/Route114/scripts.pory"
	.string "RUSTBORO CITY THROUGH HERE$"
# 193 "data/maps/Route114/scripts.pory"

# 194 "data/maps/Route114/scripts.pory"
Route114_Text_FossilManiacsHouseSign:
# 195 "data/maps/Route114/scripts.pory"
	.string "FOSSIL MANIAC'S HOUSE\n"
# 196 "data/maps/Route114/scripts.pory"
	.string "“Fossils gratefully accepted!”$"
# 197 "data/maps/Route114/scripts.pory"

# 198 "data/maps/Route114/scripts.pory"
Route114_Text_LanettesHouse:
# 199 "data/maps/Route114/scripts.pory"
	.string "LANETTE'S HOUSE$"
