# 1 "data/maps/Route111/scripts.pory"

# 2 "data/maps/Route111/scripts.pory"
Route111_MapScripts::
# 3 "data/maps/Route111/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, Route111_OnLoad
# 4 "data/maps/Route111/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, Route111_OnTransition
# 5 "data/maps/Route111/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Route111_OnWarp
# 6 "data/maps/Route111/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route111_OnFrame
# 7 "data/maps/Route111/scripts.pory"
	.byte 0
# 8 "data/maps/Route111/scripts.pory"

# 9 "data/maps/Route111/scripts.pory"
Route111_OnLoad:
# 10 "data/maps/Route111/scripts.pory"
	call_if_unset FLAG_REGI_DOORS_OPENED, Route111_EventScript_CloseDesertRuins
# 11 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_ShowTemporaryMirageTower
# 12 "data/maps/Route111/scripts.pory"
	end
# 13 "data/maps/Route111/scripts.pory"

# 14 "data/maps/Route111/scripts.pory"
Route111_EventScript_CloseDesertRuins::
# 15 "data/maps/Route111/scripts.pory"
	setmetatile 29, 86, METATILE_General_RockWall_RockBase, TRUE
# 16 "data/maps/Route111/scripts.pory"
	setmetatile 29, 87, METATILE_General_RockWall_SandBase, TRUE
# 17 "data/maps/Route111/scripts.pory"
	return
# 18 "data/maps/Route111/scripts.pory"

# 19 "data/maps/Route111/scripts.pory"
@ Show Mirage Tower just prior to disintegration. Mirage Tower is otherwise handled by the map layout
# 20 "data/maps/Route111/scripts.pory"
Route111_EventScript_ShowTemporaryMirageTower::
# 21 "data/maps/Route111/scripts.pory"
	setmetatile 18, 53, METATILE_Mauville_MirageTower_Tile0, FALSE
# 22 "data/maps/Route111/scripts.pory"
	setmetatile 19, 53, METATILE_Mauville_MirageTower_Tile1, FALSE
# 23 "data/maps/Route111/scripts.pory"
	setmetatile 20, 53, METATILE_Mauville_MirageTower_Tile2, FALSE
# 24 "data/maps/Route111/scripts.pory"
	setmetatile 18, 54, METATILE_Mauville_MirageTower_Tile3, FALSE
# 25 "data/maps/Route111/scripts.pory"
	setmetatile 19, 54, METATILE_Mauville_MirageTower_Tile4, FALSE
# 26 "data/maps/Route111/scripts.pory"
	setmetatile 20, 54, METATILE_Mauville_MirageTower_Tile5, FALSE
# 27 "data/maps/Route111/scripts.pory"
	setmetatile 18, 55, METATILE_Mauville_MirageTower_Tile6, FALSE
# 28 "data/maps/Route111/scripts.pory"
	setmetatile 19, 55, METATILE_Mauville_MirageTower_Tile7, FALSE
# 29 "data/maps/Route111/scripts.pory"
	setmetatile 20, 55, METATILE_Mauville_MirageTower_Tile8, FALSE
# 30 "data/maps/Route111/scripts.pory"
	setmetatile 18, 56, METATILE_Mauville_MirageTower_Tile9, FALSE
# 31 "data/maps/Route111/scripts.pory"
	setmetatile 19, 56, METATILE_Mauville_MirageTower_TileA, FALSE
# 32 "data/maps/Route111/scripts.pory"
	setmetatile 20, 56, METATILE_Mauville_MirageTower_TileB, FALSE
# 33 "data/maps/Route111/scripts.pory"
	setmetatile 18, 57, METATILE_Mauville_MirageTower_TileC, FALSE
# 34 "data/maps/Route111/scripts.pory"
	setmetatile 19, 57, METATILE_Mauville_MirageTower_TileD, FALSE
# 35 "data/maps/Route111/scripts.pory"
	setmetatile 20, 57, METATILE_Mauville_MirageTower_TileE, FALSE
# 36 "data/maps/Route111/scripts.pory"
	setmetatile 18, 58, METATILE_Mauville_MirageTower_TileF, FALSE
# 37 "data/maps/Route111/scripts.pory"
	setmetatile 19, 58, METATILE_Mauville_MirageTower_Tile10, FALSE
# 38 "data/maps/Route111/scripts.pory"
	setmetatile 20, 58, METATILE_Mauville_MirageTower_Tile11, FALSE
# 39 "data/maps/Route111/scripts.pory"
	return
# 40 "data/maps/Route111/scripts.pory"

# 41 "data/maps/Route111/scripts.pory"
Route111_OnTransition:
# 42 "data/maps/Route111/scripts.pory"
	setvar VAR_TRAINER_HILL_IS_ACTIVE, 0
# 43 "data/maps/Route111/scripts.pory"
	special SetMirageTowerVisibility
# 44 "data/maps/Route111/scripts.pory"
	call_if_unset FLAG_MIRAGE_TOWER_VISIBLE, Route111_EventScript_SetLayoutNoMirageTower
# 45 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_SetFallingPlayerGfx
# 46 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_MIRAGE_TOWER_STATE, 2, Route111_EventScript_SetMirageTowerGone
# 47 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CheckSetSandstorm
# 48 "data/maps/Route111/scripts.pory"
	call GabbyAndTy_EventScript_UpdateLocation
# 49 "data/maps/Route111/scripts.pory"
	goto_if_not_defeated TRAINER_VICKY, Route111_EventScript_SetWinstratesNotDefeated
# 50 "data/maps/Route111/scripts.pory"
	end
# 51 "data/maps/Route111/scripts.pory"

# 52 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetFallingPlayerGfx::
# 53 "data/maps/Route111/scripts.pory"
	checkplayergender
# 54 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, MALE, Route111_EventScript_SetFallingPlayerGfxMale
# 55 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, FEMALE, Route111_EventScript_SetFallingPlayerGfxFemale
# 56 "data/maps/Route111/scripts.pory"
	return
# 57 "data/maps/Route111/scripts.pory"

# 58 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetFallingPlayerGfxMale::
# 59 "data/maps/Route111/scripts.pory"
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
# 60 "data/maps/Route111/scripts.pory"
	return
# 61 "data/maps/Route111/scripts.pory"

# 62 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetFallingPlayerGfxFemale::
# 63 "data/maps/Route111/scripts.pory"
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
# 64 "data/maps/Route111/scripts.pory"
	return
# 65 "data/maps/Route111/scripts.pory"

# 66 "data/maps/Route111/scripts.pory"
Route111_EventScript_CheckSetSandstorm::
# 67 "data/maps/Route111/scripts.pory"
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
# 68 "data/maps/Route111/scripts.pory"
	goto_if_lt VAR_TEMP_1, 34, Route111_EventScript_EndCheckSetSandstorm
# 69 "data/maps/Route111/scripts.pory"
	goto_if_gt VAR_TEMP_1, 107, Route111_EventScript_EndCheckSetSandstorm
# 70 "data/maps/Route111/scripts.pory"
	goto_if_gt VAR_TEMP_1, 72, Route111_EventScript_SetSandstorm
# 71 "data/maps/Route111/scripts.pory"
	goto_if_gt VAR_TEMP_0, 2000, Route111_EventScript_EndCheckSetSandstorm
# 72 "data/maps/Route111/scripts.pory"
	goto_if_lt VAR_TEMP_0, 8, Route111_EventScript_EndCheckSetSandstorm
# 73 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetSandstorm::
# 74 "data/maps/Route111/scripts.pory"
	setweather WEATHER_SANDSTORM
# 75 "data/maps/Route111/scripts.pory"
Route111_EventScript_EndCheckSetSandstorm::
# 76 "data/maps/Route111/scripts.pory"
	return
# 77 "data/maps/Route111/scripts.pory"

# 78 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetWinstratesNotDefeated::
# 79 "data/maps/Route111/scripts.pory"
	clearflag FLAG_HIDE_ROUTE_111_VICTOR_WINSTRATE
# 80 "data/maps/Route111/scripts.pory"
	setflag FLAG_HIDE_ROUTE_111_VICTORIA_WINSTRATE
# 81 "data/maps/Route111/scripts.pory"
	setflag FLAG_HIDE_ROUTE_111_VIVI_WINSTRATE
# 82 "data/maps/Route111/scripts.pory"
	setflag FLAG_HIDE_ROUTE_111_VICKY_WINSTRATE
# 83 "data/maps/Route111/scripts.pory"
	cleartrainerflag TRAINER_VICTOR
# 84 "data/maps/Route111/scripts.pory"
	cleartrainerflag TRAINER_VICTORIA
# 85 "data/maps/Route111/scripts.pory"
	cleartrainerflag TRAINER_VIVI
# 86 "data/maps/Route111/scripts.pory"
	end
# 87 "data/maps/Route111/scripts.pory"

# 88 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetLayoutNoMirageTower::
# 89 "data/maps/Route111/scripts.pory"
	setmaplayoutindex LAYOUT_ROUTE111_NO_MIRAGE_TOWER
# 90 "data/maps/Route111/scripts.pory"
	return
# 91 "data/maps/Route111/scripts.pory"

# 92 "data/maps/Route111/scripts.pory"
Route111_EventScript_SetMirageTowerGone::
# 93 "data/maps/Route111/scripts.pory"
	setvar VAR_MIRAGE_TOWER_STATE, 3
# 94 "data/maps/Route111/scripts.pory"
	return
# 95 "data/maps/Route111/scripts.pory"

# 96 "data/maps/Route111/scripts.pory"
Route111_OnWarp:
# 97 "data/maps/Route111/scripts.pory"
	map_script_2 VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_HidePlayerForMirageTower
# 98 "data/maps/Route111/scripts.pory"
	.2byte 0
# 99 "data/maps/Route111/scripts.pory"

# 100 "data/maps/Route111/scripts.pory"
Route111_EventScript_HidePlayerForMirageTower::
# 101 "data/maps/Route111/scripts.pory"
	hideobjectat LOCALID_PLAYER, MAP_TOSA_PORT
# 102 "data/maps/Route111/scripts.pory"
	end
# 103 "data/maps/Route111/scripts.pory"

# 104 "data/maps/Route111/scripts.pory"
Route111_OnFrame:
# 105 "data/maps/Route111/scripts.pory"
	map_script_2 VAR_MIRAGE_TOWER_STATE, 1, Route111_EventScript_MirageTowerDisappear
# 106 "data/maps/Route111/scripts.pory"
	.2byte 0
# 107 "data/maps/Route111/scripts.pory"

# 108 "data/maps/Route111/scripts.pory"
Route111_EventScript_MirageTowerDisappear::
# 109 "data/maps/Route111/scripts.pory"
	lockall
# 110 "data/maps/Route111/scripts.pory"
	special StartMirageTowerShake
# 111 "data/maps/Route111/scripts.pory"
	delay 24
# 112 "data/maps/Route111/scripts.pory"
	playse SE_FALL
# 113 "data/maps/Route111/scripts.pory"
	addobject LOCALID_ROUTE111_PLAYER_FALLING
# 114 "data/maps/Route111/scripts.pory"
	special StartPlayerDescendMirageTower
# 115 "data/maps/Route111/scripts.pory"
	showobjectat LOCALID_PLAYER, MAP_TOSA_PORT
# 116 "data/maps/Route111/scripts.pory"
	removeobject LOCALID_ROUTE111_PLAYER_FALLING
# 117 "data/maps/Route111/scripts.pory"
	delay 16
# 118 "data/maps/Route111/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 119 "data/maps/Route111/scripts.pory"
	delay 16
# 120 "data/maps/Route111/scripts.pory"
	special StartMirageTowerDisintegration
# 121 "data/maps/Route111/scripts.pory"
	special StartMirageTowerFossilFallAndSink
# 122 "data/maps/Route111/scripts.pory"
	setvar VAR_MIRAGE_TOWER_STATE, 2
# 123 "data/maps/Route111/scripts.pory"
	clearflag FLAG_HIDE_DESERT_UNDERPASS_FOSSIL
# 124 "data/maps/Route111/scripts.pory"
	goto_if_set FLAG_CHOSE_CLAW_FOSSIL, Route111_EventScript_RootFossilDisappeared
# 125 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_ClawFossilDisappeared, MSGBOX_DEFAULT
# 126 "data/maps/Route111/scripts.pory"
	releaseall
# 127 "data/maps/Route111/scripts.pory"
	end
# 128 "data/maps/Route111/scripts.pory"

# 129 "data/maps/Route111/scripts.pory"
Route111_EventScript_RootFossilDisappeared::
# 130 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_RootFossilDisappeared, MSGBOX_DEFAULT
# 131 "data/maps/Route111/scripts.pory"
	releaseall
# 132 "data/maps/Route111/scripts.pory"
	end
# 133 "data/maps/Route111/scripts.pory"

# 134 "data/maps/Route111/scripts.pory"
@ Unused
# 135 "data/maps/Route111/scripts.pory"
Route111_Movement_PlayerFall::
# 136 "data/maps/Route111/scripts.pory"
	lock_anim
# 137 "data/maps/Route111/scripts.pory"
	walk_fast_down
# 138 "data/maps/Route111/scripts.pory"
	walk_fast_down
# 139 "data/maps/Route111/scripts.pory"
	walk_fast_down
# 140 "data/maps/Route111/scripts.pory"
	walk_fast_down
# 141 "data/maps/Route111/scripts.pory"
	walk_fast_down
# 142 "data/maps/Route111/scripts.pory"
	walk_fast_down
# 143 "data/maps/Route111/scripts.pory"
	step_end
# 144 "data/maps/Route111/scripts.pory"

# 145 "data/maps/Route111/scripts.pory"
Route111_EventScript_Girl::
# 146 "data/maps/Route111/scripts.pory"
	lock
# 147 "data/maps/Route111/scripts.pory"
	faceplayer
# 148 "data/maps/Route111/scripts.pory"
	dotimebasedevents
# 149 "data/maps/Route111/scripts.pory"
	goto_if_set FLAG_DAILY_ROUTE_111_RECEIVED_BERRY, Route111_EventScript_ReceivedBerry
# 150 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WateredPlantsEveryDayTakeBerry, MSGBOX_DEFAULT
# 151 "data/maps/Route111/scripts.pory"
	giveitem ITEM_RAZZ_BERRY
# 152 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 153 "data/maps/Route111/scripts.pory"
	setflag FLAG_DAILY_ROUTE_111_RECEIVED_BERRY
# 154 "data/maps/Route111/scripts.pory"
	special GetPlayerBigGuyGirlString
# 155 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_GoingToTryToMakeDifferentColorBerries, MSGBOX_DEFAULT
# 156 "data/maps/Route111/scripts.pory"
	release
# 157 "data/maps/Route111/scripts.pory"
	end
# 158 "data/maps/Route111/scripts.pory"

# 159 "data/maps/Route111/scripts.pory"
Route111_EventScript_ReceivedBerry::
# 160 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WhatColorBerriesToLookForToday, MSGBOX_DEFAULT
# 161 "data/maps/Route111/scripts.pory"
	release
# 162 "data/maps/Route111/scripts.pory"
	end
# 163 "data/maps/Route111/scripts.pory"

# 164 "data/maps/Route111/scripts.pory"
@ Unused
# 165 "data/maps/Route111/scripts.pory"
Route111_EventScript_ViciousSandstormTriggerUp::
# 166 "data/maps/Route111/scripts.pory"
	lockall
# 167 "data/maps/Route111/scripts.pory"
	setvar VAR_0x8004, 0
# 168 "data/maps/Route111/scripts.pory"
	goto Route111_EventScript_ViciousSandstormTrigger
# 169 "data/maps/Route111/scripts.pory"
	end
# 170 "data/maps/Route111/scripts.pory"

# 171 "data/maps/Route111/scripts.pory"
Route111_EventScript_ViciousSandstormTriggerDown::
# 172 "data/maps/Route111/scripts.pory"
	lockall
# 173 "data/maps/Route111/scripts.pory"
	setvar VAR_0x8004, 1
# 174 "data/maps/Route111/scripts.pory"
	goto Route111_EventScript_ViciousSandstormTrigger
# 175 "data/maps/Route111/scripts.pory"
	end
# 176 "data/maps/Route111/scripts.pory"

# 177 "data/maps/Route111/scripts.pory"
Route111_EventScript_ViciousSandstormTriggerLeft::
# 178 "data/maps/Route111/scripts.pory"
	lockall
# 179 "data/maps/Route111/scripts.pory"
	setvar VAR_0x8004, 2
# 180 "data/maps/Route111/scripts.pory"
	goto Route111_EventScript_ViciousSandstormTrigger
# 181 "data/maps/Route111/scripts.pory"
	end
# 182 "data/maps/Route111/scripts.pory"

# 183 "data/maps/Route111/scripts.pory"
@ Unused
# 184 "data/maps/Route111/scripts.pory"
Route111_EventScript_ViciousSandstormTriggerRight::
# 185 "data/maps/Route111/scripts.pory"
	lockall
# 186 "data/maps/Route111/scripts.pory"
	setvar VAR_0x8004, 3
# 187 "data/maps/Route111/scripts.pory"
	goto Route111_EventScript_ViciousSandstormTrigger
# 188 "data/maps/Route111/scripts.pory"
	end
# 189 "data/maps/Route111/scripts.pory"

# 190 "data/maps/Route111/scripts.pory"
Route111_EventScript_ViciousSandstormTrigger::
# 191 "data/maps/Route111/scripts.pory"
	checkitem ITEM_GO_GOGGLES
# 192 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Route111_EventScript_PreventRouteAccess
# 193 "data/maps/Route111/scripts.pory"
	setvar VAR_TEMP_3, 1
# 194 "data/maps/Route111/scripts.pory"
	releaseall
# 195 "data/maps/Route111/scripts.pory"
	end
# 196 "data/maps/Route111/scripts.pory"

# 197 "data/maps/Route111/scripts.pory"
Route111_EventScript_PreventRouteAccess::
# 198 "data/maps/Route111/scripts.pory"
	msgbox gText_SandstormIsVicious, MSGBOX_DEFAULT
# 199 "data/maps/Route111/scripts.pory"
	closemessage
# 200 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_0x8004, 0, Route111_EventScript_PushUpFromRoute
# 201 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_0x8004, 1, Route111_EventScript_PushDownFromRoute
# 202 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_0x8004, 2, Route111_EventScript_PushLeftFromRoute
# 203 "data/maps/Route111/scripts.pory"
	call_if_eq VAR_0x8004, 3, Route111_EventScript_PushRightFromRoute
# 204 "data/maps/Route111/scripts.pory"
	releaseall
# 205 "data/maps/Route111/scripts.pory"
	end
# 206 "data/maps/Route111/scripts.pory"

# 207 "data/maps/Route111/scripts.pory"
Route111_EventScript_PushUpFromRoute::
# 208 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_PushUpFromRoute
# 209 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 210 "data/maps/Route111/scripts.pory"
	return
# 211 "data/maps/Route111/scripts.pory"

# 212 "data/maps/Route111/scripts.pory"
Route111_EventScript_PushDownFromRoute::
# 213 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_PushDownFromRoute
# 214 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 215 "data/maps/Route111/scripts.pory"
	return
# 216 "data/maps/Route111/scripts.pory"

# 217 "data/maps/Route111/scripts.pory"
Route111_EventScript_PushLeftFromRoute::
# 218 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_PushLeftFromRoute
# 219 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 220 "data/maps/Route111/scripts.pory"
	return
# 221 "data/maps/Route111/scripts.pory"

# 222 "data/maps/Route111/scripts.pory"
Route111_EventScript_PushRightFromRoute::
# 223 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_PushRightFromRoute
# 224 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 225 "data/maps/Route111/scripts.pory"
	return
# 226 "data/maps/Route111/scripts.pory"

# 227 "data/maps/Route111/scripts.pory"
Route111_Movement_PushUpFromRoute:
# 228 "data/maps/Route111/scripts.pory"
	walk_up
# 229 "data/maps/Route111/scripts.pory"
	step_end
# 230 "data/maps/Route111/scripts.pory"

# 231 "data/maps/Route111/scripts.pory"
Route111_Movement_PushDownFromRoute:
# 232 "data/maps/Route111/scripts.pory"
	walk_down
# 233 "data/maps/Route111/scripts.pory"
	step_end
# 234 "data/maps/Route111/scripts.pory"

# 235 "data/maps/Route111/scripts.pory"
Route111_Movement_PushLeftFromRoute:
# 236 "data/maps/Route111/scripts.pory"
	walk_left
# 237 "data/maps/Route111/scripts.pory"
	step_end
# 238 "data/maps/Route111/scripts.pory"

# 239 "data/maps/Route111/scripts.pory"
Route111_Movement_PushRightFromRoute:
# 240 "data/maps/Route111/scripts.pory"
	walk_right
# 241 "data/maps/Route111/scripts.pory"
	step_end
# 242 "data/maps/Route111/scripts.pory"

# 243 "data/maps/Route111/scripts.pory"
Route111_EventScript_SunTrigger::
# 244 "data/maps/Route111/scripts.pory"
	setweather WEATHER_SUNNY
# 245 "data/maps/Route111/scripts.pory"
	fadenewbgm MUS_ROUTE110
# 246 "data/maps/Route111/scripts.pory"
	doweather
# 247 "data/maps/Route111/scripts.pory"
	setvar VAR_TEMP_3, 0
# 248 "data/maps/Route111/scripts.pory"
	end
# 249 "data/maps/Route111/scripts.pory"

# 250 "data/maps/Route111/scripts.pory"
Route111_EventScript_SandstormTrigger::
# 251 "data/maps/Route111/scripts.pory"
	setweather WEATHER_SANDSTORM
# 252 "data/maps/Route111/scripts.pory"
	fadenewbgm MUS_DESERT
# 253 "data/maps/Route111/scripts.pory"
	doweather
# 254 "data/maps/Route111/scripts.pory"
	end
# 255 "data/maps/Route111/scripts.pory"

# 256 "data/maps/Route111/scripts.pory"
Route111_EventScript_Victor::
# 257 "data/maps/Route111/scripts.pory"
	lock
# 258 "data/maps/Route111/scripts.pory"
	faceplayer
# 259 "data/maps/Route111/scripts.pory"
	setflag FLAG_LANDMARK_WINSTRATE_FAMILY
# 260 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BattleOurFamily, MSGBOX_YESNO
# 261 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, YES, Route111_EventScript_BattleWinstrates
# 262 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_IsThatSo, MSGBOX_DEFAULT
# 263 "data/maps/Route111/scripts.pory"
	release
# 264 "data/maps/Route111/scripts.pory"
	end
# 265 "data/maps/Route111/scripts.pory"

# 266 "data/maps/Route111/scripts.pory"
Route111_EventScript_BattleWinstrates::
# 267 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_VictorIntro, MSGBOX_DEFAULT
# 268 "data/maps/Route111/scripts.pory"
	trainerbattle_no_intro TRAINER_VICTOR, Route111_Text_VictorDefeat
# 269 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICTOR, Common_Movement_WalkInPlaceFasterUp
# 270 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 271 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 272 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_VictorPostBattle, MSGBOX_DEFAULT
# 273 "data/maps/Route111/scripts.pory"
	closemessage
# 274 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICTOR, Route111_Movement_WinstrateEnterHouse
# 275 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 276 "data/maps/Route111/scripts.pory"
	removeobject LOCALID_ROUTE111_VICTOR
# 277 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 278 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_WaitForNextWinstrate
# 279 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 280 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 281 "data/maps/Route111/scripts.pory"
	addobject LOCALID_ROUTE111_VICTORIA
# 282 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICTORIA, Route111_Movement_WinstrateExitHouse
# 283 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 284 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 285 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_VictoriaIntro, MSGBOX_DEFAULT
# 286 "data/maps/Route111/scripts.pory"
	trainerbattle_no_intro TRAINER_VICTORIA, Route111_Text_VictoriaDefeat
# 287 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICTORIA, Common_Movement_WalkInPlaceFasterUp
# 288 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 289 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 290 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_VictoriaPostBattle, MSGBOX_DEFAULT
# 291 "data/maps/Route111/scripts.pory"
	closemessage
# 292 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICTORIA, Route111_Movement_WinstrateEnterHouse
# 293 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 294 "data/maps/Route111/scripts.pory"
	removeobject LOCALID_ROUTE111_VICTORIA
# 295 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 296 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_WaitForNextWinstrate
# 297 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 298 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 299 "data/maps/Route111/scripts.pory"
	addobject LOCALID_ROUTE111_VIVI
# 300 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VIVI, Route111_Movement_WinstrateExitHouse
# 301 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 302 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 303 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_ViviIntro, MSGBOX_DEFAULT
# 304 "data/maps/Route111/scripts.pory"
	trainerbattle_no_intro TRAINER_VIVI, Route111_Text_ViviDefeat
# 305 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VIVI, Common_Movement_WalkInPlaceFasterUp
# 306 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 307 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 308 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_ViviPostBattle, MSGBOX_DEFAULT
# 309 "data/maps/Route111/scripts.pory"
	closemessage
# 310 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VIVI, Route111_Movement_WinstrateEnterHouse
# 311 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 312 "data/maps/Route111/scripts.pory"
	removeobject LOCALID_ROUTE111_VIVI
# 313 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 314 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_PLAYER, Route111_Movement_WaitForNextWinstrate
# 315 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 316 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 317 "data/maps/Route111/scripts.pory"
	addobject LOCALID_ROUTE111_VICKY
# 318 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICKY, Route111_Movement_WinstrateExitHouse
# 319 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 320 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 321 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_VickyIntro, MSGBOX_DEFAULT
# 322 "data/maps/Route111/scripts.pory"
	trainerbattle_no_intro TRAINER_VICKY, Route111_Text_VickyDefeat
# 323 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_VickyPostBattle, MSGBOX_DEFAULT
# 324 "data/maps/Route111/scripts.pory"
	closemessage
# 325 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICKY, Common_Movement_WalkInPlaceFasterUp
# 326 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 327 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_OpenWinstrateDoor
# 328 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_VICKY, Route111_Movement_WinstrateEnterHouse
# 329 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 330 "data/maps/Route111/scripts.pory"
	removeobject LOCALID_ROUTE111_VICKY
# 331 "data/maps/Route111/scripts.pory"
	call Route111_EventScript_CloseWinstrateDoor
# 332 "data/maps/Route111/scripts.pory"
	release
# 333 "data/maps/Route111/scripts.pory"
	end
# 334 "data/maps/Route111/scripts.pory"

# 335 "data/maps/Route111/scripts.pory"
Route111_EventScript_OpenWinstrateDoor::
# 336 "data/maps/Route111/scripts.pory"
	opendoor 13, 113
# 337 "data/maps/Route111/scripts.pory"
	waitdooranim
# 338 "data/maps/Route111/scripts.pory"
	return
# 339 "data/maps/Route111/scripts.pory"

# 340 "data/maps/Route111/scripts.pory"
Route111_EventScript_CloseWinstrateDoor::
# 341 "data/maps/Route111/scripts.pory"
	closedoor 13, 113
# 342 "data/maps/Route111/scripts.pory"
	waitdooranim
# 343 "data/maps/Route111/scripts.pory"
	return
# 344 "data/maps/Route111/scripts.pory"

# 345 "data/maps/Route111/scripts.pory"
Route111_Movement_WinstrateEnterHouse:
# 346 "data/maps/Route111/scripts.pory"
	walk_in_place_faster_up
# 347 "data/maps/Route111/scripts.pory"
	walk_up
# 348 "data/maps/Route111/scripts.pory"
	step_end
# 349 "data/maps/Route111/scripts.pory"

# 350 "data/maps/Route111/scripts.pory"
Route111_Movement_WinstrateExitHouse:
# 351 "data/maps/Route111/scripts.pory"
	walk_down
# 352 "data/maps/Route111/scripts.pory"
	step_end
# 353 "data/maps/Route111/scripts.pory"

# 354 "data/maps/Route111/scripts.pory"
Route111_Movement_WaitForNextWinstrate:
# 355 "data/maps/Route111/scripts.pory"
	delay_16
# 356 "data/maps/Route111/scripts.pory"
	delay_16
# 357 "data/maps/Route111/scripts.pory"
	delay_16
# 358 "data/maps/Route111/scripts.pory"
	step_end
# 359 "data/maps/Route111/scripts.pory"

# 360 "data/maps/Route111/scripts.pory"
Route111_EventScript_RouteSignMauville::
# 361 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_RouteSignMauville, MSGBOX_SIGN
# 362 "data/maps/Route111/scripts.pory"
	end
# 363 "data/maps/Route111/scripts.pory"

# 364 "data/maps/Route111/scripts.pory"
Route111_EventScript_WinstrateHouseSign::
# 365 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WinstrateHouseSign, MSGBOX_SIGN
# 366 "data/maps/Route111/scripts.pory"
	end
# 367 "data/maps/Route111/scripts.pory"

# 368 "data/maps/Route111/scripts.pory"
Route111_EventScript_RouteSign112::
# 369 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_RouteSign112, MSGBOX_SIGN
# 370 "data/maps/Route111/scripts.pory"
	end
# 371 "data/maps/Route111/scripts.pory"

# 372 "data/maps/Route111/scripts.pory"
Route111_EventScript_RouteSign113::
# 373 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_RouteSign113, MSGBOX_SIGN
# 374 "data/maps/Route111/scripts.pory"
	end
# 375 "data/maps/Route111/scripts.pory"

# 376 "data/maps/Route111/scripts.pory"
Route111_EventScript_OldLadysRestStopSign::
# 377 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_OldLadysRestStopSign, MSGBOX_SIGN
# 378 "data/maps/Route111/scripts.pory"
	end
# 379 "data/maps/Route111/scripts.pory"

# 380 "data/maps/Route111/scripts.pory"
Route111_EventScript_TrainerTipsSpAtkSpDef::
# 381 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_TrainerTipsSpAtkSpDef, MSGBOX_SIGN
# 382 "data/maps/Route111/scripts.pory"
	end
# 383 "data/maps/Route111/scripts.pory"

# 384 "data/maps/Route111/scripts.pory"
Route111_EventScript_Man1::
# 385 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_ToughToKeepWinningUpTheRanks, MSGBOX_NPC
# 386 "data/maps/Route111/scripts.pory"
	end
# 387 "data/maps/Route111/scripts.pory"

# 388 "data/maps/Route111/scripts.pory"
Route111_EventScript_Man2::
# 389 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WinstrateFamilyDestroyedMe, MSGBOX_NPC
# 390 "data/maps/Route111/scripts.pory"
	end
# 391 "data/maps/Route111/scripts.pory"

# 392 "data/maps/Route111/scripts.pory"
Route111_EventScript_Hiker::
# 393 "data/maps/Route111/scripts.pory"
	lock
# 394 "data/maps/Route111/scripts.pory"
	faceplayer
# 395 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_MIRAGE_TOWER_STATE, 3, Route111_EventScript_HikerMirageTowerGone
# 396 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_MIRAGE_TOWER_STATE, 2, Route111_EventScript_HikerMirageTowerDisintegrated
# 397 "data/maps/Route111/scripts.pory"
	goto_if_set FLAG_MIRAGE_TOWER_VISIBLE, Route111_EventScript_HikerMirageTowerVisible
# 398 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_ShouldBeMirageTowerAroundHere, MSGBOX_DEFAULT
# 399 "data/maps/Route111/scripts.pory"
	release
# 400 "data/maps/Route111/scripts.pory"
	end
# 401 "data/maps/Route111/scripts.pory"

# 402 "data/maps/Route111/scripts.pory"
Route111_EventScript_HikerMirageTowerGone::
# 403 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_MirageTowerHasntBeenSeenSince, MSGBOX_DEFAULT
# 404 "data/maps/Route111/scripts.pory"
	release
# 405 "data/maps/Route111/scripts.pory"
	end
# 406 "data/maps/Route111/scripts.pory"

# 407 "data/maps/Route111/scripts.pory"
Route111_EventScript_HikerMirageTowerDisintegrated::
# 408 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_ThatWasShockingSandRainedDown, MSGBOX_DEFAULT
# 409 "data/maps/Route111/scripts.pory"
	release
# 410 "data/maps/Route111/scripts.pory"
	end
# 411 "data/maps/Route111/scripts.pory"

# 412 "data/maps/Route111/scripts.pory"
Route111_EventScript_HikerMirageTowerVisible::
# 413 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_MirageTowerClearlyVisible, MSGBOX_DEFAULT
# 414 "data/maps/Route111/scripts.pory"
	release
# 415 "data/maps/Route111/scripts.pory"
	end
# 416 "data/maps/Route111/scripts.pory"

# 417 "data/maps/Route111/scripts.pory"
Route111_EventScript_RockSmashTipFatMan::
# 418 "data/maps/Route111/scripts.pory"
	lockall
# 419 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_FacePlayer
# 420 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 421 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_MauvilleUncleToldMeToTakeRockSmash, MSGBOX_DEFAULT
# 422 "data/maps/Route111/scripts.pory"
	closemessage
# 423 "data/maps/Route111/scripts.pory"
	applymovement LOCALID_ROUTE111_ROCK_SMASH_MAN, Common_Movement_FaceOriginalDirection
# 424 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 425 "data/maps/Route111/scripts.pory"
	releaseall
# 426 "data/maps/Route111/scripts.pory"
	end
# 427 "data/maps/Route111/scripts.pory"

# 428 "data/maps/Route111/scripts.pory"
Route111_EventScript_Drew::
# 429 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_DREW, Route111_Text_DrewIntro, Route111_Text_DrewDefeat
# 430 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_DrewPostBattle, MSGBOX_AUTOCLOSE
# 431 "data/maps/Route111/scripts.pory"
	end
# 432 "data/maps/Route111/scripts.pory"

# 433 "data/maps/Route111/scripts.pory"
Route111_EventScript_Heidi::
# 434 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_HEIDI, Route111_Text_HeidiIntro, Route111_Text_HeidiDefeat
# 435 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_HeidiPostBattle, MSGBOX_AUTOCLOSE
# 436 "data/maps/Route111/scripts.pory"
	end
# 437 "data/maps/Route111/scripts.pory"

# 438 "data/maps/Route111/scripts.pory"
Route111_EventScript_Beau::
# 439 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_BEAU, Route111_Text_BeauIntro, Route111_Text_BeauDefeat
# 440 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BeauPostBattle, MSGBOX_AUTOCLOSE
# 441 "data/maps/Route111/scripts.pory"
	end
# 442 "data/maps/Route111/scripts.pory"

# 443 "data/maps/Route111/scripts.pory"
Route111_EventScript_Becky::
# 444 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_BECKY, Route111_Text_BeckyIntro, Route111_Text_BeckyDefeat
# 445 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BeckyPostBattle, MSGBOX_AUTOCLOSE
# 446 "data/maps/Route111/scripts.pory"
	end
# 447 "data/maps/Route111/scripts.pory"

# 448 "data/maps/Route111/scripts.pory"
Route111_EventScript_Dusty::
# 449 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_DUSTY_1, Route111_Text_DustyIntro, Route111_Text_DustyDefeat, Route111_EventScript_RegisterDusty
# 450 "data/maps/Route111/scripts.pory"
	specialvar VAR_RESULT, ShouldTryRematchBattle
# 451 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, Route111_EventScript_RematchDusty
# 452 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_DustyPostBattle, MSGBOX_DEFAULT
# 453 "data/maps/Route111/scripts.pory"
	release
# 454 "data/maps/Route111/scripts.pory"
	end
# 455 "data/maps/Route111/scripts.pory"

# 456 "data/maps/Route111/scripts.pory"
Route111_EventScript_RegisterDusty::
# 457 "data/maps/Route111/scripts.pory"
	special PlayerFaceTrainerAfterBattle
# 458 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 459 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_DustyRegister, MSGBOX_DEFAULT
# 460 "data/maps/Route111/scripts.pory"
	register_matchcall TRAINER_DUSTY_1
# 461 "data/maps/Route111/scripts.pory"
	release
# 462 "data/maps/Route111/scripts.pory"
	end
# 463 "data/maps/Route111/scripts.pory"

# 464 "data/maps/Route111/scripts.pory"
Route111_EventScript_RematchDusty::
# 465 "data/maps/Route111/scripts.pory"
	trainerbattle_rematch TRAINER_DUSTY_1, Route111_Text_DustyRematchIntro, Route111_Text_DustyRematchDefeat
# 466 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_DustyPostRematch, MSGBOX_AUTOCLOSE
# 467 "data/maps/Route111/scripts.pory"
	end
# 468 "data/maps/Route111/scripts.pory"

# 469 "data/maps/Route111/scripts.pory"
Route111_EventScript_Travis::
# 470 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_TRAVIS, Route111_Text_TravisIntro, Route111_Text_TravisDefeat
# 471 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_TravisPostBattle, MSGBOX_AUTOCLOSE
# 472 "data/maps/Route111/scripts.pory"
	end
# 473 "data/maps/Route111/scripts.pory"

# 474 "data/maps/Route111/scripts.pory"
Route111_EventScript_Irene::
# 475 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_IRENE, Route111_Text_IreneIntro, Route111_Text_IreneDefeat
# 476 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_IrenePostBattle, MSGBOX_AUTOCLOSE
# 477 "data/maps/Route111/scripts.pory"
	end
# 478 "data/maps/Route111/scripts.pory"

# 479 "data/maps/Route111/scripts.pory"
Route111_EventScript_Daisuke::
# 480 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_DAISUKE, Route111_Text_DaisukeIntro, Route111_Text_DaisukeDefeat
# 481 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_DaisukePostBattle, MSGBOX_AUTOCLOSE
# 482 "data/maps/Route111/scripts.pory"
	end
# 483 "data/maps/Route111/scripts.pory"

# 484 "data/maps/Route111/scripts.pory"
Route111_EventScript_Wilton::
# 485 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_WILTON_1, Route111_Text_WiltonIntro, Route111_Text_WiltonDefeat, Route111_EventScript_RegisterWilton
# 486 "data/maps/Route111/scripts.pory"
	specialvar VAR_RESULT, ShouldTryRematchBattle
# 487 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, Route111_EventScript_RematchWilton
# 488 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WiltonPostBattle, MSGBOX_DEFAULT
# 489 "data/maps/Route111/scripts.pory"
	release
# 490 "data/maps/Route111/scripts.pory"
	end
# 491 "data/maps/Route111/scripts.pory"

# 492 "data/maps/Route111/scripts.pory"
Route111_EventScript_RegisterWilton::
# 493 "data/maps/Route111/scripts.pory"
	special PlayerFaceTrainerAfterBattle
# 494 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 495 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WiltonRegister, MSGBOX_DEFAULT
# 496 "data/maps/Route111/scripts.pory"
	register_matchcall TRAINER_WILTON_1
# 497 "data/maps/Route111/scripts.pory"
	release
# 498 "data/maps/Route111/scripts.pory"
	end
# 499 "data/maps/Route111/scripts.pory"

# 500 "data/maps/Route111/scripts.pory"
Route111_EventScript_RematchWilton::
# 501 "data/maps/Route111/scripts.pory"
	trainerbattle_rematch TRAINER_WILTON_1, Route111_Text_WiltonRematchIntro, Route111_Text_WiltonRematchDefeat
# 502 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_WiltonPostRematch, MSGBOX_AUTOCLOSE
# 503 "data/maps/Route111/scripts.pory"
	end
# 504 "data/maps/Route111/scripts.pory"

# 505 "data/maps/Route111/scripts.pory"
Route111_EventScript_Brooke::
# 506 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_BROOKE_1, Route111_Text_BrookeIntro, Route111_Text_BrookeDefeat, Route111_EventScript_RegisterBrooke
# 507 "data/maps/Route111/scripts.pory"
	specialvar VAR_RESULT, ShouldTryRematchBattle
# 508 "data/maps/Route111/scripts.pory"
	goto_if_eq VAR_RESULT, TRUE, Route111_EventScript_RematchBrooke
# 509 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BrookePostBattle, MSGBOX_DEFAULT
# 510 "data/maps/Route111/scripts.pory"
	release
# 511 "data/maps/Route111/scripts.pory"
	end
# 512 "data/maps/Route111/scripts.pory"

# 513 "data/maps/Route111/scripts.pory"
Route111_EventScript_RegisterBrooke::
# 514 "data/maps/Route111/scripts.pory"
	special PlayerFaceTrainerAfterBattle
# 515 "data/maps/Route111/scripts.pory"
	waitmovement 0
# 516 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BrookeRegister, MSGBOX_DEFAULT
# 517 "data/maps/Route111/scripts.pory"
	register_matchcall TRAINER_BROOKE_1
# 518 "data/maps/Route111/scripts.pory"
	release
# 519 "data/maps/Route111/scripts.pory"
	end
# 520 "data/maps/Route111/scripts.pory"

# 521 "data/maps/Route111/scripts.pory"
Route111_EventScript_RematchBrooke::
# 522 "data/maps/Route111/scripts.pory"
	trainerbattle_rematch TRAINER_BROOKE_1, Route111_Text_BrookeRematchIntro, Route111_Text_BrookeRematchDefeat
# 523 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BrookePostRematch, MSGBOX_AUTOCLOSE
# 524 "data/maps/Route111/scripts.pory"
	end
# 525 "data/maps/Route111/scripts.pory"

# 526 "data/maps/Route111/scripts.pory"
Route111_EventScript_Hayden::
# 527 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_HAYDEN, Route111_Text_HaydenIntro, Route111_Text_HaydenDefeat
# 528 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_HaydenPostBattle, MSGBOX_AUTOCLOSE
# 529 "data/maps/Route111/scripts.pory"
	end
# 530 "data/maps/Route111/scripts.pory"

# 531 "data/maps/Route111/scripts.pory"
Route111_EventScript_Bianca::
# 532 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_BIANCA, Route111_Text_BiancaIntro, Route111_Text_BiancaDefeat
# 533 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BiancaPostBattle, MSGBOX_AUTOCLOSE
# 534 "data/maps/Route111/scripts.pory"
	end
# 535 "data/maps/Route111/scripts.pory"

# 536 "data/maps/Route111/scripts.pory"
Route111_EventScript_Tyron::
# 537 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_TYRON, Route111_Text_TyronIntro, Route111_Text_TyronDefeat
# 538 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_TyronPostBattle, MSGBOX_AUTOCLOSE
# 539 "data/maps/Route111/scripts.pory"
	end
# 540 "data/maps/Route111/scripts.pory"

# 541 "data/maps/Route111/scripts.pory"
Route111_EventScript_Celina::
# 542 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_CELINA, Route111_Text_CelinaIntro, Route111_Text_CelinaDefeat
# 543 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_CelinaPostBattle, MSGBOX_AUTOCLOSE
# 544 "data/maps/Route111/scripts.pory"
	end
# 545 "data/maps/Route111/scripts.pory"

# 546 "data/maps/Route111/scripts.pory"
Route111_EventScript_Celia::
# 547 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_CELIA, Route111_Text_CeliaIntro, Route111_Text_CeliaDefeat
# 548 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_CeliaPostBattle, MSGBOX_AUTOCLOSE
# 549 "data/maps/Route111/scripts.pory"
	end
# 550 "data/maps/Route111/scripts.pory"

# 551 "data/maps/Route111/scripts.pory"
Route111_EventScript_Bryan::
# 552 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_BRYAN, Route111_Text_BryanIntro, Route111_Text_BryanDefeat
# 553 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BryanPostBattle, MSGBOX_AUTOCLOSE
# 554 "data/maps/Route111/scripts.pory"
	end
# 555 "data/maps/Route111/scripts.pory"

# 556 "data/maps/Route111/scripts.pory"
Route111_EventScript_Branden::
# 557 "data/maps/Route111/scripts.pory"
	trainerbattle_single TRAINER_BRANDEN, Route111_Text_BrandenIntro, Route111_Text_BrandenDefeat
# 558 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_BrandenPostBattle, MSGBOX_AUTOCLOSE
# 559 "data/maps/Route111/scripts.pory"
	end
# 560 "data/maps/Route111/scripts.pory"

# 561 "data/maps/Route111/scripts.pory"
Route111_EventScript_TrainerHillSign::
# 562 "data/maps/Route111/scripts.pory"
	msgbox Route111_Text_TrainerHillSign, MSGBOX_SIGN
# 563 "data/maps/Route111/scripts.pory"
	end
# 564 "data/maps/Route111/scripts.pory"

# 565 "data/maps/Route111/scripts.pory"
Route111_Text_BattleOurFamily:
# 566 "data/maps/Route111/scripts.pory"
	.string "Hello! I take it you're a traveler.\p"
# 567 "data/maps/Route111/scripts.pory"
	.string "How's this? What do you say to taking\n"
# 568 "data/maps/Route111/scripts.pory"
	.string "on our family of four in a series of\l"
# 569 "data/maps/Route111/scripts.pory"
	.string "POKéMON battles?$"
# 570 "data/maps/Route111/scripts.pory"

# 571 "data/maps/Route111/scripts.pory"
Route111_Text_IsThatSo:
# 572 "data/maps/Route111/scripts.pory"
	.string "Is that so?\n"
# 573 "data/maps/Route111/scripts.pory"
	.string "Drop in, if you change your mind!$"
# 574 "data/maps/Route111/scripts.pory"

# 575 "data/maps/Route111/scripts.pory"
Route111_Text_VictorIntro:
# 576 "data/maps/Route111/scripts.pory"
	.string "That's the spirit! I like you!$"
# 577 "data/maps/Route111/scripts.pory"

# 578 "data/maps/Route111/scripts.pory"
Route111_Text_VictorDefeat:
# 579 "data/maps/Route111/scripts.pory"
	.string "Aiyah!\n"
# 580 "data/maps/Route111/scripts.pory"
	.string "You're a lot tougher than I expected!$"
# 581 "data/maps/Route111/scripts.pory"

# 582 "data/maps/Route111/scripts.pory"
Route111_Text_VictorPostBattle:
# 583 "data/maps/Route111/scripts.pory"
	.string "Hey, all!\n"
# 584 "data/maps/Route111/scripts.pory"
	.string "I've found a pretty strong TRAINER!$"
# 585 "data/maps/Route111/scripts.pory"

# 586 "data/maps/Route111/scripts.pory"
Route111_Text_VictoriaIntro:
# 587 "data/maps/Route111/scripts.pory"
	.string "Oh, my goodness! Aren't you young?\p"
# 588 "data/maps/Route111/scripts.pory"
	.string "You must be quite the TRAINER to beat\n"
# 589 "data/maps/Route111/scripts.pory"
	.string "my husband, though.\p"
# 590 "data/maps/Route111/scripts.pory"
	.string "It's my turn to battle now!$"
# 591 "data/maps/Route111/scripts.pory"

# 592 "data/maps/Route111/scripts.pory"
Route111_Text_VictoriaDefeat:
# 593 "data/maps/Route111/scripts.pory"
	.string "Oh, gosh!\n"
# 594 "data/maps/Route111/scripts.pory"
	.string "I can't get over how strong you are!$"
# 595 "data/maps/Route111/scripts.pory"

# 596 "data/maps/Route111/scripts.pory"
Route111_Text_VictoriaPostBattle:
# 597 "data/maps/Route111/scripts.pory"
	.string "There's a strong TRAINER here!\n"
# 598 "data/maps/Route111/scripts.pory"
	.string "This one's really strong!$"
# 599 "data/maps/Route111/scripts.pory"

# 600 "data/maps/Route111/scripts.pory"
Route111_Text_ViviIntro:
# 601 "data/maps/Route111/scripts.pory"
	.string "You're stronger than Mommy? Wow!\p"
# 602 "data/maps/Route111/scripts.pory"
	.string "But I'm strong, too!\n"
# 603 "data/maps/Route111/scripts.pory"
	.string "Really! Honestly!$"
# 604 "data/maps/Route111/scripts.pory"

# 605 "data/maps/Route111/scripts.pory"
Route111_Text_ViviDefeat:
# 606 "data/maps/Route111/scripts.pory"
	.string "Huh? Did I just lose?$"
# 607 "data/maps/Route111/scripts.pory"

# 608 "data/maps/Route111/scripts.pory"
Route111_Text_ViviPostBattle:
# 609 "data/maps/Route111/scripts.pory"
	.string "This stinks…\p"
# 610 "data/maps/Route111/scripts.pory"
	.string "…Snivel… Grandma!$"
# 611 "data/maps/Route111/scripts.pory"

# 612 "data/maps/Route111/scripts.pory"
Route111_Text_VickyIntro:
# 613 "data/maps/Route111/scripts.pory"
	.string "How dare you make my granddaughter\n"
# 614 "data/maps/Route111/scripts.pory"
	.string "cry!\p"
# 615 "data/maps/Route111/scripts.pory"
	.string "For that, I'm going to smack you!\n"
# 616 "data/maps/Route111/scripts.pory"
	.string "Prepare to lose!$"
# 617 "data/maps/Route111/scripts.pory"

# 618 "data/maps/Route111/scripts.pory"
Route111_Text_VickyDefeat:
# 619 "data/maps/Route111/scripts.pory"
	.string "Kwah! You are strong…\n"
# 620 "data/maps/Route111/scripts.pory"
	.string "My granddaughter was right…$"
# 621 "data/maps/Route111/scripts.pory"

# 622 "data/maps/Route111/scripts.pory"
Route111_Text_VickyPostBattle:
# 623 "data/maps/Route111/scripts.pory"
	.string "If you're not in any hurry,\n"
# 624 "data/maps/Route111/scripts.pory"
	.string "visit with us awhile.$"
# 625 "data/maps/Route111/scripts.pory"

# 626 "data/maps/Route111/scripts.pory"
Route111_Text_ToughToKeepWinningUpTheRanks:
# 627 "data/maps/Route111/scripts.pory"
	.string "If you don't raise your POKéMON some\n"
# 628 "data/maps/Route111/scripts.pory"
	.string "more, it could be tough to keep winning\l"
# 629 "data/maps/Route111/scripts.pory"
	.string "up through the ranks.\p"
# 630 "data/maps/Route111/scripts.pory"
	.string "I've heard the POKéMON LEAGUE's\n"
# 631 "data/maps/Route111/scripts.pory"
	.string "ELITE FOUR are far stronger than\l"
# 632 "data/maps/Route111/scripts.pory"
	.string "any GYM LEADER.$"
# 633 "data/maps/Route111/scripts.pory"

# 634 "data/maps/Route111/scripts.pory"
Route111_Text_WinstrateFamilyDestroyedMe:
# 635 "data/maps/Route111/scripts.pory"
	.string "I challenged the WINSTRATE family,\n"
# 636 "data/maps/Route111/scripts.pory"
	.string "but four matches in a row is tough\l"
# 637 "data/maps/Route111/scripts.pory"
	.string "going… They destroyed me.$"
# 638 "data/maps/Route111/scripts.pory"

# 639 "data/maps/Route111/scripts.pory"
Route111_Text_RouteSignMauville:
# 640 "data/maps/Route111/scripts.pory"
	.string "ROUTE 111\n"
# 641 "data/maps/Route111/scripts.pory"
	.string "{DOWN_ARROW} MAUVILLE CITY$"
# 642 "data/maps/Route111/scripts.pory"

# 643 "data/maps/Route111/scripts.pory"
Route111_Text_WinstrateHouseSign:
# 644 "data/maps/Route111/scripts.pory"
	.string "“Our family's hearts beat as one!”\n"
# 645 "data/maps/Route111/scripts.pory"
	.string "THE WINSTRATE'S HOUSE$"
# 646 "data/maps/Route111/scripts.pory"

# 647 "data/maps/Route111/scripts.pory"
Route111_Text_RouteSign112:
# 648 "data/maps/Route111/scripts.pory"
	.string "ROUTE 111\n"
# 649 "data/maps/Route111/scripts.pory"
	.string "{LEFT_ARROW} ROUTE 112$"
# 650 "data/maps/Route111/scripts.pory"

# 651 "data/maps/Route111/scripts.pory"
Route111_Text_RouteSign113:
# 652 "data/maps/Route111/scripts.pory"
	.string "ROUTE 111\n"
# 653 "data/maps/Route111/scripts.pory"
	.string "{LEFT_ARROW} ROUTE 113$"
# 654 "data/maps/Route111/scripts.pory"

# 655 "data/maps/Route111/scripts.pory"
Route111_Text_OldLadysRestStopSign:
# 656 "data/maps/Route111/scripts.pory"
	.string "OLD LADY'S REST STOP\n"
# 657 "data/maps/Route111/scripts.pory"
	.string "“Come in and rest your tired bones.”$"
# 658 "data/maps/Route111/scripts.pory"

# 659 "data/maps/Route111/scripts.pory"
Route111_Text_TrainerTipsSpAtkSpDef:
# 660 "data/maps/Route111/scripts.pory"
	.string "TRAINER TIPS\p"
# 661 "data/maps/Route111/scripts.pory"
	.string "One of the indicators of a POKéMON's\n"
# 662 "data/maps/Route111/scripts.pory"
	.string "powerfulness is SP. ATK. It stands for\l"
# 663 "data/maps/Route111/scripts.pory"
	.string "“SPECIAL ATTACK.”\p"
# 664 "data/maps/Route111/scripts.pory"
	.string "Likewise, SP. DEF stands for “SPECIAL\n"
# 665 "data/maps/Route111/scripts.pory"
	.string "DEFENSE.”$"
# 666 "data/maps/Route111/scripts.pory"

# 667 "data/maps/Route111/scripts.pory"
Route111_Text_ShouldBeMirageTowerAroundHere:
# 668 "data/maps/Route111/scripts.pory"
	.string "There should be a tower made of sand\n"
# 669 "data/maps/Route111/scripts.pory"
	.string "around here somewhere.\p"
# 670 "data/maps/Route111/scripts.pory"
	.string "But for some reason, it can be seen\n"
# 671 "data/maps/Route111/scripts.pory"
	.string "sometimes, and sometimes not.\p"
# 672 "data/maps/Route111/scripts.pory"
	.string "That's why I call it the MIRAGE TOWER.$"
# 673 "data/maps/Route111/scripts.pory"

# 674 "data/maps/Route111/scripts.pory"
Route111_Text_MirageTowerClearlyVisible:
# 675 "data/maps/Route111/scripts.pory"
	.string "I see it!\n"
# 676 "data/maps/Route111/scripts.pory"
	.string "The tower of sand!\p"
# 677 "data/maps/Route111/scripts.pory"
	.string "The sand tower they called a mirage\n"
# 678 "data/maps/Route111/scripts.pory"
	.string "is clearly visible!\p"
# 679 "data/maps/Route111/scripts.pory"
	.string "But it looks so fragile…\n"
# 680 "data/maps/Route111/scripts.pory"
	.string "It could crumble away anytime…\p"
# 681 "data/maps/Route111/scripts.pory"
	.string "I want to go inside it, but I can't\n"
# 682 "data/maps/Route111/scripts.pory"
	.string "get my courage up for it…$"
# 683 "data/maps/Route111/scripts.pory"

# 684 "data/maps/Route111/scripts.pory"
Route111_Text_ThatWasShockingSandRainedDown:
# 685 "data/maps/Route111/scripts.pory"
	.string "Whoa…\n"
# 686 "data/maps/Route111/scripts.pory"
	.string "That was shocking.\p"
# 687 "data/maps/Route111/scripts.pory"
	.string "Sand rained down in chunks all of\n"
# 688 "data/maps/Route111/scripts.pory"
	.string "a sudden.\p"
# 689 "data/maps/Route111/scripts.pory"
	.string "What was it like inside?\n"
# 690 "data/maps/Route111/scripts.pory"
	.string "Were there sandy ghosts and such?$"
# 691 "data/maps/Route111/scripts.pory"

# 692 "data/maps/Route111/scripts.pory"
Route111_Text_MirageTowerHasntBeenSeenSince:
# 693 "data/maps/Route111/scripts.pory"
	.string "Since I spoke to you, the tower of sand\n"
# 694 "data/maps/Route111/scripts.pory"
	.string "hasn't been seen.\p"
# 695 "data/maps/Route111/scripts.pory"
	.string "Perhaps it really was\n"
# 696 "data/maps/Route111/scripts.pory"
	.string "the MIRAGE TOWER…$"
# 697 "data/maps/Route111/scripts.pory"

# 698 "data/maps/Route111/scripts.pory"
Route111_Text_ClawFossilDisappeared:
# 699 "data/maps/Route111/scripts.pory"
	.string "The CLAW FOSSIL disappeared into\n"
# 700 "data/maps/Route111/scripts.pory"
	.string "the sand…$"
# 701 "data/maps/Route111/scripts.pory"

# 702 "data/maps/Route111/scripts.pory"
Route111_Text_RootFossilDisappeared:
# 703 "data/maps/Route111/scripts.pory"
	.string "The ROOT FOSSIL disappeared into\n"
# 704 "data/maps/Route111/scripts.pory"
	.string "the sand…$"
# 705 "data/maps/Route111/scripts.pory"

# 706 "data/maps/Route111/scripts.pory"
Route111_Text_MauvilleUncleToldMeToTakeRockSmash:
# 707 "data/maps/Route111/scripts.pory"
	.string "Oh, no!\p"
# 708 "data/maps/Route111/scripts.pory"
	.string "My uncle in MAUVILLE told me to take\n"
# 709 "data/maps/Route111/scripts.pory"
	.string "ROCK SMASH with me if I was going to\l"
# 710 "data/maps/Route111/scripts.pory"
	.string "ROUTE 111!\p"
# 711 "data/maps/Route111/scripts.pory"
	.string "My uncle? He lives across from\n"
# 712 "data/maps/Route111/scripts.pory"
	.string "the bike shop in MAUVILLE.$"
# 713 "data/maps/Route111/scripts.pory"

# 714 "data/maps/Route111/scripts.pory"
Route111_Text_TrainerHillSign:
# 715 "data/maps/Route111/scripts.pory"
	.string "{RIGHT_ARROW} TRAINER HILL ENTRANCE\p"
# 716 "data/maps/Route111/scripts.pory"
	.string "“Scale the heights, you hot-blooded\n"
# 717 "data/maps/Route111/scripts.pory"
	.string "TRAINERS!”$"
