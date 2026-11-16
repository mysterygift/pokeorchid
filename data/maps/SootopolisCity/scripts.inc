# 1 "data/maps/SootopolisCity/scripts.pory"

# 2 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_MapScripts::
# 3 "data/maps/SootopolisCity/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, SootopolisCity_OnLoad
# 4 "data/maps/SootopolisCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, SootopolisCity_OnTransition
# 5 "data/maps/SootopolisCity/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, SootopolisCity_OnResume
# 6 "data/maps/SootopolisCity/scripts.pory"
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SootopolisCity_OnFrame
# 7 "data/maps/SootopolisCity/scripts.pory"
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SootopolisCity_OnWarp
# 8 "data/maps/SootopolisCity/scripts.pory"
	.byte 0
# 9 "data/maps/SootopolisCity/scripts.pory"

# 10 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_OnLoad:
# 11 "data/maps/SootopolisCity/scripts.pory"
	call_if_unset FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_LockGymDoor
# 12 "data/maps/SootopolisCity/scripts.pory"
	goto_if_unset FLAG_KYOGRE_ESCAPED_SEAFLOOR_CAVERN, SootopolisCity_EventScript_LegendariesNotArrived
# 13 "data/maps/SootopolisCity/scripts.pory"
	call_if_unset FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_LockHouseDoors
# 14 "data/maps/SootopolisCity/scripts.pory"
	end
# 15 "data/maps/SootopolisCity/scripts.pory"

# 16 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_LegendariesNotArrived::
# 17 "data/maps/SootopolisCity/scripts.pory"
	end
# 18 "data/maps/SootopolisCity/scripts.pory"

# 19 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_LockHouseDoors::
# 20 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 9, 6, METATILE_Sootopolis_Door_Closed, TRUE
# 21 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 9, 17, METATILE_Sootopolis_Door_Closed, TRUE
# 22 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 9, 26, METATILE_Sootopolis_Door_Closed, TRUE
# 23 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 44, 17, METATILE_Sootopolis_Door_Closed, TRUE
# 24 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 8, 35, METATILE_Sootopolis_Door_Closed, TRUE
# 25 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 53, 28, METATILE_Sootopolis_Door_Closed, TRUE
# 26 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 45, 6, METATILE_Sootopolis_Door_Closed, TRUE
# 27 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 48, 25, METATILE_Sootopolis_Door_Closed, TRUE
# 28 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 51, 36, METATILE_Sootopolis_Door_Closed, TRUE
# 29 "data/maps/SootopolisCity/scripts.pory"
	return
# 30 "data/maps/SootopolisCity/scripts.pory"

# 31 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_LockGymDoor::
# 32 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 31, 32, METATILE_Sootopolis_GymDoor_Closed, TRUE
# 33 "data/maps/SootopolisCity/scripts.pory"
	return
# 34 "data/maps/SootopolisCity/scripts.pory"

# 35 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_OnTransition:
# 36 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_VISITED_SOOTOPOLIS_CITY
# 37 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_HideMapNamePopup
# 38 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_HideMapNamePopup
# 39 "data/maps/SootopolisCity/scripts.pory"
	call SootopolisCity_EventScript_SetWeather
# 40 "data/maps/SootopolisCity/scripts.pory"
	call SootopolisCity_EventScript_SetLayout
# 41 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_SetBattleSpectators
# 42 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_SetBattleSpectators
# 43 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_SetBattleSpectators
# 44 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_SetBattleSpectators
# 45 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_SetBattleSpectators
# 46 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_CheckSetEnterCaveOfOriginObjPos
# 47 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_CheckSetEnterCaveOfOriginObjPos
# 48 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_SetExitCaveOfOriginObjPos
# 49 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_SetOutsideGymObjPos
# 50 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_SetExpertBlockCaveEntrance
# 51 "data/maps/SootopolisCity/scripts.pory"
	end
# 52 "data/maps/SootopolisCity/scripts.pory"

# 53 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_HideMapNamePopup::
# 54 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_HIDE_MAP_NAME_POPUP
# 55 "data/maps/SootopolisCity/scripts.pory"
	return
# 56 "data/maps/SootopolisCity/scripts.pory"

# 57 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetBattleSpectators::
# 58 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_KIRI, 13, 48
# 59 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_BOY_1, 46, 32
# 60 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_NINJA_BOY, 48, 41
# 61 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_WOMAN_1, 45, 43
# 62 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_KIRI, MOVEMENT_TYPE_FACE_UP
# 63 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_SOOTOPOLIS_BOY_1, MOVEMENT_TYPE_FACE_LEFT
# 64 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_SOOTOPOLIS_NINJA_BOY, MOVEMENT_TYPE_FACE_LEFT
# 65 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_SOOTOPOLIS_WOMAN_1, MOVEMENT_TYPE_FACE_LEFT
# 66 "data/maps/SootopolisCity/scripts.pory"
	return
# 67 "data/maps/SootopolisCity/scripts.pory"

# 68 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetLayout::
# 69 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 0, SootopolisCity_EventScript_SetNormalLayout
# 70 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_SetNormalLayout
# 71 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_SetLegendariesLayout
# 72 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_SetLegendariesLayout
# 73 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_SetLegendariesLayout
# 74 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_SetLegendariesLayout
# 75 "data/maps/SootopolisCity/scripts.pory"
	goto_if_le VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_SetLegendariesLayout
# 76 "data/maps/SootopolisCity/scripts.pory"
	return
# 77 "data/maps/SootopolisCity/scripts.pory"

# 78 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetNormalLayout::
# 79 "data/maps/SootopolisCity/scripts.pory"
	return
# 80 "data/maps/SootopolisCity/scripts.pory"

# 81 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetLegendariesLayout::
# 82 "data/maps/SootopolisCity/scripts.pory"
	setmaplayoutindex LAYOUT_SOOTOPOLIS_CITY_LEGENDS_BATTLE
# 83 "data/maps/SootopolisCity/scripts.pory"
	return
# 84 "data/maps/SootopolisCity/scripts.pory"

# 85 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetWeather::
# 86 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 0, SootopolisCity_EventScript_SetNormalWeather
# 87 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_SetNormalWeather
# 88 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_SetDownpour
# 89 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_SetDownpour
# 90 "data/maps/SootopolisCity/scripts.pory"
	goto_if_le VAR_SKY_PILLAR_STATE, 1, Common_EventScript_SetAbnormalWeather
# 91 "data/maps/SootopolisCity/scripts.pory"
	return
# 92 "data/maps/SootopolisCity/scripts.pory"

# 93 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetNormalWeather::
# 94 "data/maps/SootopolisCity/scripts.pory"
	return
# 95 "data/maps/SootopolisCity/scripts.pory"

# 96 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetDownpour::
# 97 "data/maps/SootopolisCity/scripts.pory"
	setweather WEATHER_DOWNPOUR
# 98 "data/maps/SootopolisCity/scripts.pory"
	return
# 99 "data/maps/SootopolisCity/scripts.pory"

# 100 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_CheckSetEnterCaveOfOriginObjPos::
# 101 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN, SootopolisCity_EventScript_SetEnterCaveOfOriginObjPos
# 102 "data/maps/SootopolisCity/scripts.pory"
	return
# 103 "data/maps/SootopolisCity/scripts.pory"

# 104 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetEnterCaveOfOriginObjPos::
# 105 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 30, 18
# 106 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_STEVEN, 32, 18
# 107 "data/maps/SootopolisCity/scripts.pory"
	return
# 108 "data/maps/SootopolisCity/scripts.pory"

# 109 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetExitCaveOfOriginObjPos::
# 110 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 30, 18
# 111 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 31, 18
# 112 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_STEVEN, 32, 18
# 113 "data/maps/SootopolisCity/scripts.pory"
	end
# 114 "data/maps/SootopolisCity/scripts.pory"

# 115 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetOutsideGymObjPos::
# 116 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 31, 18
# 117 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_STEVEN, 29, 33
# 118 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_MAXIE, 33, 35
# 119 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_ARCHIE, 34, 35
# 120 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_WALLACE_STATE, 0, SootopolisCity_EventScript_SetWallaceMiddle
# 121 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_WALLACE_STATE, 1, SootopolisCity_EventScript_SetWallaceRight
# 122 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SOOTOPOLIS_WALLACE_STATE, 2, SootopolisCity_EventScript_SetWallaceLeft
# 123 "data/maps/SootopolisCity/scripts.pory"
	return
# 124 "data/maps/SootopolisCity/scripts.pory"

# 125 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetWallaceMiddle::
# 126 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 31, 33
# 127 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_SOOTOPOLIS_WALLACE, MOVEMENT_TYPE_FACE_DOWN
# 128 "data/maps/SootopolisCity/scripts.pory"
	return
# 129 "data/maps/SootopolisCity/scripts.pory"

# 130 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetWallaceRight::
# 131 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 32, 33
# 132 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_SOOTOPOLIS_WALLACE, MOVEMENT_TYPE_FACE_DOWN
# 133 "data/maps/SootopolisCity/scripts.pory"
	return
# 134 "data/maps/SootopolisCity/scripts.pory"

# 135 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetWallaceLeft::
# 136 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_WALLACE, 30, 33
# 137 "data/maps/SootopolisCity/scripts.pory"
	setobjectmovementtype LOCALID_SOOTOPOLIS_WALLACE, MOVEMENT_TYPE_FACE_DOWN
# 138 "data/maps/SootopolisCity/scripts.pory"
	return
# 139 "data/maps/SootopolisCity/scripts.pory"

# 140 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetExpertBlockCaveEntrance::
# 141 "data/maps/SootopolisCity/scripts.pory"
	setobjectxyperm LOCALID_SOOTOPOLIS_EXPERT, 31, 18
# 142 "data/maps/SootopolisCity/scripts.pory"
	return
# 143 "data/maps/SootopolisCity/scripts.pory"

# 144 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_OnWarp:
# 145 "data/maps/SootopolisCity/scripts.pory"
	map_script_2 VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_PlayerFaceLegendaries
# 146 "data/maps/SootopolisCity/scripts.pory"
	.2byte 0
# 147 "data/maps/SootopolisCity/scripts.pory"

# 148 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_PlayerFaceLegendaries::
# 149 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_PlayerFaceLegendaries1
# 150 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_SKY_PILLAR_STATE, 2, SootopolisCity_EventScript_PlayerFaceLegendaries2
# 151 "data/maps/SootopolisCity/scripts.pory"
	end
# 152 "data/maps/SootopolisCity/scripts.pory"

# 153 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_PlayerFaceLegendaries1::
# 154 "data/maps/SootopolisCity/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 155 "data/maps/SootopolisCity/scripts.pory"
	return
# 156 "data/maps/SootopolisCity/scripts.pory"

# 157 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_PlayerFaceLegendaries2::
# 158 "data/maps/SootopolisCity/scripts.pory"
	turnobject LOCALID_PLAYER, DIR_NORTH
# 159 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SKY_PILLAR_STATE, 3
# 160 "data/maps/SootopolisCity/scripts.pory"
	return
# 161 "data/maps/SootopolisCity/scripts.pory"

# 162 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_OnResume:
# 163 "data/maps/SootopolisCity/scripts.pory"
	setdivewarp MAP_UNDERWATER_SOOTOPOLIS_CITY, 9, 6
# 164 "data/maps/SootopolisCity/scripts.pory"
	end
# 165 "data/maps/SootopolisCity/scripts.pory"

# 166 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_OnFrame:
# 167 "data/maps/SootopolisCity/scripts.pory"
	map_script_2 VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_StartLegendariesScene
# 168 "data/maps/SootopolisCity/scripts.pory"
	map_script_2 VAR_SKY_PILLAR_STATE, 1, SootopolisCity_EventScript_StartRayquazaScene
# 169 "data/maps/SootopolisCity/scripts.pory"
	.2byte 0
# 170 "data/maps/SootopolisCity/scripts.pory"

# 171 "data/maps/SootopolisCity/scripts.pory"
@ If not at PokeCenter, assumed to have arrived via Dive
# 172 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StartLegendariesScene::
# 173 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 174 "data/maps/SootopolisCity/scripts.pory"
	special StorePlayerCoordsInVars
# 175 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ne VAR_0x8004, 43, SootopolisCity_EventScript_LegendariesSceneFromDive
# 176 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ne VAR_0x8005, 32, SootopolisCity_EventScript_LegendariesSceneFromDive
# 177 "data/maps/SootopolisCity/scripts.pory"
	goto SootopolisCity_EventScript_LegendariesSceneFromPokeCenter
# 178 "data/maps/SootopolisCity/scripts.pory"
	end
# 179 "data/maps/SootopolisCity/scripts.pory"

# 180 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_LegendariesSceneFromPokeCenter::
# 181 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 182 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 183 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromPokeCenter
# 184 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 185 "data/maps/SootopolisCity/scripts.pory"
	special RemoveCameraObject
# 186 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 187 "data/maps/SootopolisCity/scripts.pory"
	fadescreenspeed FADE_TO_BLACK, 8
# 188 "data/maps/SootopolisCity/scripts.pory"
	setweather WEATHER_ABNORMAL
# 189 "data/maps/SootopolisCity/scripts.pory"
	doweather
# 190 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, FALSE @ Just do Groudon/Kyogre fight scene
# 191 "data/maps/SootopolisCity/scripts.pory"
	special Script_DoRayquazaScene
# 192 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, Common_Movement_WalkInPlaceFasterLeft
# 193 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, Common_Movement_WalkInPlaceFasterRight
# 194 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 195 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 196 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 197 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
# 198 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
# 199 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
# 200 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 201 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 202 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 203 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 204 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 205 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 206 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 207 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
# 208 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
# 209 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 210 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 211 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
# 212 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreDefend
# 213 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonAttack
# 214 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 215 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 216 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 217 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 218 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 219 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 220 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 221 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
# 222 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
# 223 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 224 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 225 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
# 226 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
# 227 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
# 228 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 229 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 230 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 231 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 232 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 233 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 234 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 235 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
# 236 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
# 237 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 238 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 239 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreIdle
# 240 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonIdle
# 241 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanBackToPokeCenter
# 242 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 243 "data/maps/SootopolisCity/scripts.pory"
	special RemoveCameraObject
# 244 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SOOTOPOLIS_CITY_STATE, 2
# 245 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 246 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 247 "data/maps/SootopolisCity/scripts.pory"
	end
# 248 "data/maps/SootopolisCity/scripts.pory"

# 249 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PanToActionFromPokeCenter:
# 250 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 251 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 252 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 253 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 254 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 255 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 256 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 257 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 258 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 259 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 260 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 261 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 262 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 263 "data/maps/SootopolisCity/scripts.pory"

# 264 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PanBackToPokeCenter:
# 265 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 266 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 267 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 268 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 269 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 270 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 271 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 272 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 273 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 274 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 275 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 276 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 277 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 278 "data/maps/SootopolisCity/scripts.pory"

# 279 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_LegendariesSceneFromDive::
# 280 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 281 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 282 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromDive
# 283 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 284 "data/maps/SootopolisCity/scripts.pory"
	special RemoveCameraObject
# 285 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 286 "data/maps/SootopolisCity/scripts.pory"
	fadescreenspeed FADE_TO_BLACK, 8
# 287 "data/maps/SootopolisCity/scripts.pory"
	setweather WEATHER_ABNORMAL
# 288 "data/maps/SootopolisCity/scripts.pory"
	doweather
# 289 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, FALSE @ Just do Groudon/Kyogre fight scene
# 290 "data/maps/SootopolisCity/scripts.pory"
	special Script_DoRayquazaScene
# 291 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, Common_Movement_WalkInPlaceFasterLeft
# 292 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, Common_Movement_WalkInPlaceFasterRight
# 293 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 294 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 295 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 296 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
# 297 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
# 298 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
# 299 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 300 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 301 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 302 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 303 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 304 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 305 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 306 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
# 307 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
# 308 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 309 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 310 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
# 311 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreDefend
# 312 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonAttack
# 313 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 314 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 315 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 316 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 317 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 318 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 319 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 320 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
# 321 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
# 322 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 323 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 324 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_KYOGRE, CRY_MODE_ENCOUNTER
# 325 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreAttack
# 326 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonDefend
# 327 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 328 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 329 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 330 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 331 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 332 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 333 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 334 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreMoveBack
# 335 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonMoveBack
# 336 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 337 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 338 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_KYOGRE, SootopolisCity_Movement_KyogreIdle
# 339 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GROUDON, SootopolisCity_Movement_GroudonIdle
# 340 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanBackToDive
# 341 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 342 "data/maps/SootopolisCity/scripts.pory"
	special RemoveCameraObject
# 343 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SOOTOPOLIS_CITY_STATE, 2
# 344 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 345 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 346 "data/maps/SootopolisCity/scripts.pory"
	end
# 347 "data/maps/SootopolisCity/scripts.pory"

# 348 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PanToActionFromDive:
# 349 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 350 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 351 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 352 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 353 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 354 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 355 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 356 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 357 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 358 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 359 "data/maps/SootopolisCity/scripts.pory"

# 360 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PanBackToDive:
# 361 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 362 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 363 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 364 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 365 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 366 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 367 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 368 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 369 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 370 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 371 "data/maps/SootopolisCity/scripts.pory"

# 372 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_KyogreAttack:
# 373 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 374 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 375 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 376 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 377 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 378 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 379 "data/maps/SootopolisCity/scripts.pory"
	init_affine_anim
# 380 "data/maps/SootopolisCity/scripts.pory"
	walk_left_affine
# 381 "data/maps/SootopolisCity/scripts.pory"
	clear_affine_anim
# 382 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 383 "data/maps/SootopolisCity/scripts.pory"

# 384 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_KyogreDefend:
# 385 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 386 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 387 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 388 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 389 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 390 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 391 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 392 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 393 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 394 "data/maps/SootopolisCity/scripts.pory"
	init_affine_anim
# 395 "data/maps/SootopolisCity/scripts.pory"
	walk_left_affine
# 396 "data/maps/SootopolisCity/scripts.pory"
	clear_affine_anim
# 397 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 398 "data/maps/SootopolisCity/scripts.pory"

# 399 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_KyogreMoveBack:
# 400 "data/maps/SootopolisCity/scripts.pory"
	lock_facing_direction
# 401 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 402 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 403 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 404 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 405 "data/maps/SootopolisCity/scripts.pory"
	unlock_facing_direction
# 406 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 407 "data/maps/SootopolisCity/scripts.pory"

# 408 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_KyogreIdle:
# 409 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 410 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 411 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 412 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 413 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 414 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_left
# 415 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 416 "data/maps/SootopolisCity/scripts.pory"

# 417 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_GroudonAttack:
# 418 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 419 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 420 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 421 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 422 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 423 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 424 "data/maps/SootopolisCity/scripts.pory"
	walk_fast_right
# 425 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 426 "data/maps/SootopolisCity/scripts.pory"

# 427 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_GroudonDefend:
# 428 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 429 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 430 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 431 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 432 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 433 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 434 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 435 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 436 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 437 "data/maps/SootopolisCity/scripts.pory"
	walk_fast_right
# 438 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 439 "data/maps/SootopolisCity/scripts.pory"

# 440 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_GroudonMoveBack:
# 441 "data/maps/SootopolisCity/scripts.pory"
	lock_facing_direction
# 442 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 443 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 444 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 445 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 446 "data/maps/SootopolisCity/scripts.pory"
	unlock_facing_direction
# 447 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 448 "data/maps/SootopolisCity/scripts.pory"

# 449 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_GroudonIdle:
# 450 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 451 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 452 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 453 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 454 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 455 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_slow_right
# 456 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 457 "data/maps/SootopolisCity/scripts.pory"

# 458 "data/maps/SootopolisCity/scripts.pory"
@ If not at PokeCenter, assumed to have arrived via Dive
# 459 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StartRayquazaScene::
# 460 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 461 "data/maps/SootopolisCity/scripts.pory"
	special StorePlayerCoordsInVars
# 462 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ne VAR_0x8004, 43, SootopolisCity_EventScript_RayquazaSceneFromDive
# 463 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ne VAR_0x8005, 32, SootopolisCity_EventScript_RayquazaSceneFromDive
# 464 "data/maps/SootopolisCity/scripts.pory"
	goto SootopolisCity_EventScript_RayquazaSceneFromPokeCenter
# 465 "data/maps/SootopolisCity/scripts.pory"
	end
# 466 "data/maps/SootopolisCity/scripts.pory"

# 467 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_RayquazaSceneFromPokeCenter::
# 468 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 469 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 470 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromPokeCenter
# 471 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 472 "data/maps/SootopolisCity/scripts.pory"
	special RemoveCameraObject
# 473 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 474 "data/maps/SootopolisCity/scripts.pory"
	fadescreenspeed FADE_TO_BLACK, 8
# 475 "data/maps/SootopolisCity/scripts.pory"
	call SootopolisCity_EventScript_SetRoughWater
# 476 "data/maps/SootopolisCity/scripts.pory"
	removeobject LOCALID_SOOTOPOLIS_GROUDON
# 477 "data/maps/SootopolisCity/scripts.pory"
	removeobject LOCALID_SOOTOPOLIS_KYOGRE
# 478 "data/maps/SootopolisCity/scripts.pory"
	addobject LOCALID_SOOTOPOLIS_RAYQUAZA
# 479 "data/maps/SootopolisCity/scripts.pory"
	hideobjectat LOCALID_SOOTOPOLIS_RAYQUAZA, MAP_SOOTOPOLIS_CITY
# 480 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, TRUE
# 481 "data/maps/SootopolisCity/scripts.pory"
	special Script_DoRayquazaScene
# 482 "data/maps/SootopolisCity/scripts.pory"
	playse SE_THUNDER
# 483 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 484 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanUp
# 485 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 486 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 487 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
# 488 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 489 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 490 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 491 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 3  @ shake delay
# 492 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 493 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 494 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 495 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
# 496 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 497 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 2  @ horizontal pan
# 498 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 499 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 500 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 501 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 502 "data/maps/SootopolisCity/scripts.pory"
	waitmoncry
# 503 "data/maps/SootopolisCity/scripts.pory"
	setweather WEATHER_NONE
# 504 "data/maps/SootopolisCity/scripts.pory"
	doweather
# 505 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_RAYQUAZA, SootopolisCity_Movement_RayquazaFlyOff
# 506 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 507 "data/maps/SootopolisCity/scripts.pory"
	removeobject LOCALID_SOOTOPOLIS_RAYQUAZA
# 508 "data/maps/SootopolisCity/scripts.pory"
	special WaitWeather
# 509 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_SYS_WEATHER_CTRL
# 510 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SKY_PILLAR_STATE, 3
# 511 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_LEGENDARIES_IN_SOOTOPOLIS
# 512 "data/maps/SootopolisCity/scripts.pory"
	fadenewbgm MUS_SOOTOPOLIS
# 513 "data/maps/SootopolisCity/scripts.pory"
	delay 120
# 514 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 515 "data/maps/SootopolisCity/scripts.pory"
	warpwhitefade MAP_SOOTOPOLIS_CITY, 43, 32
# 516 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 517 "data/maps/SootopolisCity/scripts.pory"
	end
# 518 "data/maps/SootopolisCity/scripts.pory"

# 519 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_RayquazaSceneFromDive::
# 520 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 521 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 522 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanToActionFromDive
# 523 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 524 "data/maps/SootopolisCity/scripts.pory"
	special RemoveCameraObject
# 525 "data/maps/SootopolisCity/scripts.pory"
	delay 60
# 526 "data/maps/SootopolisCity/scripts.pory"
	fadescreenspeed FADE_TO_BLACK, 8
# 527 "data/maps/SootopolisCity/scripts.pory"
	call SootopolisCity_EventScript_SetRoughWater
# 528 "data/maps/SootopolisCity/scripts.pory"
	removeobject LOCALID_SOOTOPOLIS_GROUDON
# 529 "data/maps/SootopolisCity/scripts.pory"
	removeobject LOCALID_SOOTOPOLIS_KYOGRE
# 530 "data/maps/SootopolisCity/scripts.pory"
	addobject LOCALID_SOOTOPOLIS_RAYQUAZA
# 531 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, TRUE
# 532 "data/maps/SootopolisCity/scripts.pory"
	special Script_DoRayquazaScene
# 533 "data/maps/SootopolisCity/scripts.pory"
	special SpawnCameraObject
# 534 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_CAMERA, SootopolisCity_Movement_PanUp
# 535 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerApproachLegendaries
# 536 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 537 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 538 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
# 539 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 540 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 1  @ horizontal pan
# 541 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 542 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 3  @ shake delay
# 543 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 544 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 545 "data/maps/SootopolisCity/scripts.pory"
	waitse
# 546 "data/maps/SootopolisCity/scripts.pory"
	playmoncry SPECIES_RAYQUAZA, CRY_MODE_ENCOUNTER
# 547 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8004, 1  @ vertical pan
# 548 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8005, 2  @ horizontal pan
# 549 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8006, 8  @ num shakes
# 550 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_0x8007, 5  @ shake delay
# 551 "data/maps/SootopolisCity/scripts.pory"
	special ShakeCamera
# 552 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 553 "data/maps/SootopolisCity/scripts.pory"
	waitmoncry
# 554 "data/maps/SootopolisCity/scripts.pory"
	setweather WEATHER_NONE
# 555 "data/maps/SootopolisCity/scripts.pory"
	doweather
# 556 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_RAYQUAZA, SootopolisCity_Movement_RayquazaFlyOff
# 557 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 558 "data/maps/SootopolisCity/scripts.pory"
	removeobject LOCALID_SOOTOPOLIS_RAYQUAZA
# 559 "data/maps/SootopolisCity/scripts.pory"
	special WaitWeather
# 560 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_SYS_WEATHER_CTRL
# 561 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SKY_PILLAR_STATE, 2
# 562 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_LEGENDARIES_IN_SOOTOPOLIS
# 563 "data/maps/SootopolisCity/scripts.pory"
	fadenewbgm MUS_SURF
# 564 "data/maps/SootopolisCity/scripts.pory"
	delay 120
# 565 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_HIDE_MAP_NAME_POPUP
# 566 "data/maps/SootopolisCity/scripts.pory"
	warpwhitefade MAP_SOOTOPOLIS_CITY, 29, 53
# 567 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 568 "data/maps/SootopolisCity/scripts.pory"
	end
# 569 "data/maps/SootopolisCity/scripts.pory"

# 570 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_SetRoughWater::
# 571 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 27, 43, METATILE_Sootopolis_RoughWater, FALSE
# 572 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 28, 43, METATILE_Sootopolis_RoughWater, FALSE
# 573 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 29, 43, METATILE_Sootopolis_RoughWater, FALSE
# 574 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 30, 43, METATILE_Sootopolis_RoughWater, FALSE
# 575 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 27, 44, METATILE_Sootopolis_RoughWater, FALSE
# 576 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 28, 44, METATILE_Sootopolis_RoughWater, FALSE
# 577 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 29, 44, METATILE_Sootopolis_RoughWater, FALSE
# 578 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 30, 44, METATILE_Sootopolis_RoughWater, FALSE
# 579 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 27, 45, METATILE_Sootopolis_RoughWater, FALSE
# 580 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 28, 45, METATILE_Sootopolis_RoughWater, FALSE
# 581 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 29, 45, METATILE_Sootopolis_RoughWater, FALSE
# 582 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 30, 45, METATILE_Sootopolis_RoughWater, FALSE
# 583 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 32, 43, METATILE_Sootopolis_RoughWater, FALSE
# 584 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 33, 43, METATILE_Sootopolis_RoughWater, FALSE
# 585 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 34, 43, METATILE_Sootopolis_RoughWater, FALSE
# 586 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 35, 43, METATILE_Sootopolis_RoughWater, FALSE
# 587 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 32, 44, METATILE_Sootopolis_RoughWater, FALSE
# 588 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 33, 44, METATILE_Sootopolis_RoughWater, FALSE
# 589 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 34, 44, METATILE_Sootopolis_RoughWater, FALSE
# 590 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 35, 44, METATILE_Sootopolis_RoughWater, FALSE
# 591 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 32, 45, METATILE_Sootopolis_RoughWater, FALSE
# 592 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 33, 45, METATILE_Sootopolis_RoughWater, FALSE
# 593 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 34, 45, METATILE_Sootopolis_RoughWater, FALSE
# 594 "data/maps/SootopolisCity/scripts.pory"
	setmetatile 35, 45, METATILE_Sootopolis_RoughWater, FALSE
# 595 "data/maps/SootopolisCity/scripts.pory"
	return
# 596 "data/maps/SootopolisCity/scripts.pory"

# 597 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_RayquazaFlyOff:
# 598 "data/maps/SootopolisCity/scripts.pory"
	walk_fast_up
# 599 "data/maps/SootopolisCity/scripts.pory"
	walk_faster_up
# 600 "data/maps/SootopolisCity/scripts.pory"
	walk_faster_up
# 601 "data/maps/SootopolisCity/scripts.pory"
	walk_faster_up
# 602 "data/maps/SootopolisCity/scripts.pory"
	walk_faster_up
# 603 "data/maps/SootopolisCity/scripts.pory"
	walk_faster_up
# 604 "data/maps/SootopolisCity/scripts.pory"
	walk_faster_up
# 605 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 606 "data/maps/SootopolisCity/scripts.pory"

# 607 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PanUp:
# 608 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 609 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 610 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 611 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 612 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 613 "data/maps/SootopolisCity/scripts.pory"

# 614 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerApproachLegendaries:
# 615 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 616 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 617 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 618 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 619 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 620 "data/maps/SootopolisCity/scripts.pory"

# 621 "data/maps/SootopolisCity/scripts.pory"
@ Unused
# 622 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerApproachLegendariesDown:
# 623 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 624 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 625 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 626 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 627 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 628 "data/maps/SootopolisCity/scripts.pory"

# 629 "data/maps/SootopolisCity/scripts.pory"
@ Unused
# 630 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_UnusedPanUp:
# 631 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 632 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 633 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 634 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 635 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 636 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 637 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 638 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_northeast
# 639 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 640 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 641 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 642 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 643 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 644 "data/maps/SootopolisCity/scripts.pory"

# 645 "data/maps/SootopolisCity/scripts.pory"
@ Unused
# 646 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_UnusedPanBack:
# 647 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 648 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 649 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 650 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 651 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 652 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 653 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 654 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 655 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 656 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 657 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 658 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 659 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_diag_southwest
# 660 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 661 "data/maps/SootopolisCity/scripts.pory"

# 662 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_CaveOfOriginExpert::
# 663 "data/maps/SootopolisCity/scripts.pory"
	lock
# 664 "data/maps/SootopolisCity/scripts.pory"
	faceplayer
# 665 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_ExpertPostLegendaries
# 666 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_ExpertLegendaries
# 667 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_ExpertLeadToCave
# 668 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_CaveOfOriginPleaseLeave, MSGBOX_DEFAULT
# 669 "data/maps/SootopolisCity/scripts.pory"
	release
# 670 "data/maps/SootopolisCity/scripts.pory"
	end
# 671 "data/maps/SootopolisCity/scripts.pory"

# 672 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_ExpertLeadToCave::
# 673 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_LeadSuperiorTrainerToCave, MSGBOX_DEFAULT
# 674 "data/maps/SootopolisCity/scripts.pory"
	release
# 675 "data/maps/SootopolisCity/scripts.pory"
	end
# 676 "data/maps/SootopolisCity/scripts.pory"

# 677 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_ExpertPostLegendaries::
# 678 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_CaveOfOriginSleepsToo, MSGBOX_DEFAULT
# 679 "data/maps/SootopolisCity/scripts.pory"
	release
# 680 "data/maps/SootopolisCity/scripts.pory"
	end
# 681 "data/maps/SootopolisCity/scripts.pory"

# 682 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_ExpertLegendaries::
# 683 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_AwakenedPokemonClash, MSGBOX_DEFAULT
# 684 "data/maps/SootopolisCity/scripts.pory"
	release
# 685 "data/maps/SootopolisCity/scripts.pory"
	end
# 686 "data/maps/SootopolisCity/scripts.pory"

# 687 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Kiri::
# 688 "data/maps/SootopolisCity/scripts.pory"
	lock
# 689 "data/maps/SootopolisCity/scripts.pory"
	faceplayer
# 690 "data/maps/SootopolisCity/scripts.pory"
	goto_if_le VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_KiriGiveBerry
# 691 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_KiriGiveBerry
# 692 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_KiriRayquaza
# 693 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_BigPokemonFighting, MSGBOX_DEFAULT
# 694 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 695 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_KIRI, Common_Movement_FaceOriginalDirection
# 696 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 697 "data/maps/SootopolisCity/scripts.pory"
	release
# 698 "data/maps/SootopolisCity/scripts.pory"
	end
# 699 "data/maps/SootopolisCity/scripts.pory"

# 700 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_KiriRayquaza::
# 701 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_PrettyMonCameFromSky, MSGBOX_DEFAULT
# 702 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 703 "data/maps/SootopolisCity/scripts.pory"
	release
# 704 "data/maps/SootopolisCity/scripts.pory"
	end
# 705 "data/maps/SootopolisCity/scripts.pory"

# 706 "data/maps/SootopolisCity/scripts.pory"
@ Gives 2 berries daily. First ranges from BERRY_ID_POMEG to BERRY_ID_NOMEL, second is always Figy or Iapapa
# 707 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_KiriGiveBerry::
# 708 "data/maps/SootopolisCity/scripts.pory"
	dotimebasedevents
# 709 "data/maps/SootopolisCity/scripts.pory"
	special GetPlayerBigGuyGirlString
# 710 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY, SootopolisCity_EventScript_KiriReceivedBerry
# 711 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_NameIsKiriHaveOneOfThese, MSGBOX_DEFAULT
# 712 "data/maps/SootopolisCity/scripts.pory"
	giverandomberry BERRY_ID_POMEG, BERRY_ID_NOMEL
# 713 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 714 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY
# 715 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GiveYouThisBerryToo, MSGBOX_DEFAULT
# 716 "data/maps/SootopolisCity/scripts.pory"
	random 2
# 717 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_RESULT, 0, SootopolisCity_EventScript_GiveFigyBerry
# 718 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_RESULT, 1, SootopolisCity_EventScript_GiveIapapaBerry
# 719 "data/maps/SootopolisCity/scripts.pory"
	end
# 720 "data/maps/SootopolisCity/scripts.pory"

# 721 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GiveFigyBerry::
# 722 "data/maps/SootopolisCity/scripts.pory"
	giveitem ITEM_FIGY_BERRY
# 723 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 724 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_WhatKindOfWishInYourName, MSGBOX_DEFAULT
# 725 "data/maps/SootopolisCity/scripts.pory"
	release
# 726 "data/maps/SootopolisCity/scripts.pory"
	end
# 727 "data/maps/SootopolisCity/scripts.pory"

# 728 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GiveIapapaBerry::
# 729 "data/maps/SootopolisCity/scripts.pory"
	giveitem ITEM_IAPAPA_BERRY
# 730 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 731 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_WhatKindOfWishInYourName, MSGBOX_DEFAULT
# 732 "data/maps/SootopolisCity/scripts.pory"
	release
# 733 "data/maps/SootopolisCity/scripts.pory"
	end
# 734 "data/maps/SootopolisCity/scripts.pory"

# 735 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_KiriReceivedBerry::
# 736 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_LikeSeasonBornIn, MSGBOX_YESNO
# 737 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_RESULT, YES, SootopolisCity_EventScript_KiriLikeSeasonBornIn
# 738 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_OhDoesntMatter, MSGBOX_DEFAULT
# 739 "data/maps/SootopolisCity/scripts.pory"
	release
# 740 "data/maps/SootopolisCity/scripts.pory"
	end
# 741 "data/maps/SootopolisCity/scripts.pory"

# 742 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_KiriLikeSeasonBornIn::
# 743 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_ThenILoveAutumn, MSGBOX_DEFAULT
# 744 "data/maps/SootopolisCity/scripts.pory"
	release
# 745 "data/maps/SootopolisCity/scripts.pory"
	end
# 746 "data/maps/SootopolisCity/scripts.pory"

# 747 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Woman2::
# 748 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 749 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_WOMAN_2, Common_Movement_FacePlayer
# 750 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 751 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Woman2Rayquaza
# 752 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_WeatherWentWild, MSGBOX_DEFAULT
# 753 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 754 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_WOMAN_2, Common_Movement_FaceOriginalDirection
# 755 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 756 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 757 "data/maps/SootopolisCity/scripts.pory"
	end
# 758 "data/maps/SootopolisCity/scripts.pory"

# 759 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Woman2Rayquaza::
# 760 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_YouBroughtFlyingMon, MSGBOX_DEFAULT
# 761 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 762 "data/maps/SootopolisCity/scripts.pory"
	end
# 763 "data/maps/SootopolisCity/scripts.pory"

# 764 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Man::
# 765 "data/maps/SootopolisCity/scripts.pory"
	lock
# 766 "data/maps/SootopolisCity/scripts.pory"
	faceplayer
# 767 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_ManPostLegendaries
# 768 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_NoOrdinaryTourist, MSGBOX_DEFAULT
# 769 "data/maps/SootopolisCity/scripts.pory"
	release
# 770 "data/maps/SootopolisCity/scripts.pory"
	end
# 771 "data/maps/SootopolisCity/scripts.pory"

# 772 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_ManPostLegendaries::
# 773 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_CityRegainedCalm, MSGBOX_DEFAULT
# 774 "data/maps/SootopolisCity/scripts.pory"
	release
# 775 "data/maps/SootopolisCity/scripts.pory"
	end
# 776 "data/maps/SootopolisCity/scripts.pory"

# 777 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Woman1::
# 778 "data/maps/SootopolisCity/scripts.pory"
	lock
# 779 "data/maps/SootopolisCity/scripts.pory"
	faceplayer
# 780 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_Woman1PostLegendaries
# 781 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Woman1Rayquaza
# 782 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_Woman1Legendaries
# 783 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_SootopolisSkyBeautiful, MSGBOX_DEFAULT
# 784 "data/maps/SootopolisCity/scripts.pory"
	release
# 785 "data/maps/SootopolisCity/scripts.pory"
	end
# 786 "data/maps/SootopolisCity/scripts.pory"

# 787 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Woman1Legendaries::
# 788 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GiganticPokemonFight, MSGBOX_DEFAULT
# 789 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 790 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_WOMAN_1, Common_Movement_FaceOriginalDirection
# 791 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 792 "data/maps/SootopolisCity/scripts.pory"
	release
# 793 "data/maps/SootopolisCity/scripts.pory"
	end
# 794 "data/maps/SootopolisCity/scripts.pory"

# 795 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Woman1PostLegendaries::
# 796 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_NightSkyFavoriteScenery, MSGBOX_DEFAULT
# 797 "data/maps/SootopolisCity/scripts.pory"
	release
# 798 "data/maps/SootopolisCity/scripts.pory"
	end
# 799 "data/maps/SootopolisCity/scripts.pory"

# 800 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Woman1Rayquaza::
# 801 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_FearedWorstWhenPokemonFlewDown, MSGBOX_DEFAULT
# 802 "data/maps/SootopolisCity/scripts.pory"
	release
# 803 "data/maps/SootopolisCity/scripts.pory"
	end
# 804 "data/maps/SootopolisCity/scripts.pory"

# 805 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_NinjaBoy::
# 806 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 807 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_NINJA_BOY, Common_Movement_FacePlayer
# 808 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 809 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_NinjaBoyRayquaza
# 810 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_NinjaBoyNormal
# 811 "data/maps/SootopolisCity/scripts.pory"
	goto_if_le VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_NinjaBoyNormal
# 812 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_ThisIsWicked, MSGBOX_DEFAULT
# 813 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 814 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_NINJA_BOY, Common_Movement_FaceOriginalDirection
# 815 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 816 "data/maps/SootopolisCity/scripts.pory"
	release
# 817 "data/maps/SootopolisCity/scripts.pory"
	end
# 818 "data/maps/SootopolisCity/scripts.pory"

# 819 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_NinjaBoyNormal::
# 820 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_WonderWhatWorldIsLike, MSGBOX_DEFAULT
# 821 "data/maps/SootopolisCity/scripts.pory"
	release
# 822 "data/maps/SootopolisCity/scripts.pory"
	end
# 823 "data/maps/SootopolisCity/scripts.pory"

# 824 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_NinjaBoyRayquaza::
# 825 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_ThatWasWicked, MSGBOX_DEFAULT
# 826 "data/maps/SootopolisCity/scripts.pory"
	release
# 827 "data/maps/SootopolisCity/scripts.pory"
	end
# 828 "data/maps/SootopolisCity/scripts.pory"

# 829 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Boy1::
# 830 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 831 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BOY_1, Common_Movement_FacePlayer
# 832 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 833 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Boy1Rayquaza
# 834 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, SootopolisCity_EventScript_Boy1GameClear
# 835 "data/maps/SootopolisCity/scripts.pory"
	goto_if_ge VAR_SOOTOPOLIS_CITY_STATE, 6, SootopolisCity_EventScript_Boy1Normal
# 836 "data/maps/SootopolisCity/scripts.pory"
	goto_if_le VAR_SOOTOPOLIS_CITY_STATE, 1, SootopolisCity_EventScript_Boy1Normal
# 837 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GiantPokemonSuddenlyAppeared, MSGBOX_DEFAULT
# 838 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 839 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BOY_1, Common_Movement_FaceOriginalDirection
# 840 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 841 "data/maps/SootopolisCity/scripts.pory"
	release
# 842 "data/maps/SootopolisCity/scripts.pory"
	end
# 843 "data/maps/SootopolisCity/scripts.pory"

# 844 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Boy1Rayquaza::
# 845 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_WhatIsThatGreenPokemon, MSGBOX_DEFAULT
# 846 "data/maps/SootopolisCity/scripts.pory"
	release
# 847 "data/maps/SootopolisCity/scripts.pory"
	end
# 848 "data/maps/SootopolisCity/scripts.pory"

# 849 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Boy1GameClear::
# 850 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_WhereDidLegendariesGo, MSGBOX_DEFAULT
# 851 "data/maps/SootopolisCity/scripts.pory"
	release
# 852 "data/maps/SootopolisCity/scripts.pory"
	end
# 853 "data/maps/SootopolisCity/scripts.pory"

# 854 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Boy1Normal::
# 855 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_PhysicallyFitLivingHere, MSGBOX_DEFAULT
# 856 "data/maps/SootopolisCity/scripts.pory"
	release
# 857 "data/maps/SootopolisCity/scripts.pory"
	end
# 858 "data/maps/SootopolisCity/scripts.pory"

# 859 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GymSign::
# 860 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GymSign, MSGBOX_SIGN
# 861 "data/maps/SootopolisCity/scripts.pory"
	end
# 862 "data/maps/SootopolisCity/scripts.pory"

# 863 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_CitySign::
# 864 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_CitySign, MSGBOX_SIGN
# 865 "data/maps/SootopolisCity/scripts.pory"
	end
# 866 "data/maps/SootopolisCity/scripts.pory"

# 867 "data/maps/SootopolisCity/scripts.pory"
EventScript_ClosedSootopolisDoor::
# 868 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_DoorIsClosed, MSGBOX_SIGN
# 869 "data/maps/SootopolisCity/scripts.pory"
	end
# 870 "data/maps/SootopolisCity/scripts.pory"

# 871 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Steven::
# 872 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 873 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_STEVEN, Common_Movement_FacePlayer
# 874 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 875 "data/maps/SootopolisCity/scripts.pory"
	call_if_unset FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN, SootopolisCity_EventScript_StevenLeadPlayerCaveOfOrigin
# 876 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 2, SootopolisCity_EventScript_StevenHelpWallace
# 877 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 3, SootopolisCity_EventScript_StevenHelpedWallace
# 878 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_StevenHelpedWallace
# 879 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_StevenMaxieArchieLeft
# 880 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_SoThatsRayquaza, MSGBOX_DEFAULT
# 881 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 882 "data/maps/SootopolisCity/scripts.pory"
	end
# 883 "data/maps/SootopolisCity/scripts.pory"

# 884 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StevenHelpWallace::
# 885 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_KnowWhatsNeededToHelpHim, MSGBOX_DEFAULT
# 886 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 887 "data/maps/SootopolisCity/scripts.pory"
	end
# 888 "data/maps/SootopolisCity/scripts.pory"

# 889 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StevenMaxieArchieLeft::
# 890 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_MaxieArchieLeft, MSGBOX_DEFAULT
# 891 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 892 "data/maps/SootopolisCity/scripts.pory"
	end
# 893 "data/maps/SootopolisCity/scripts.pory"

# 894 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StevenHelpedWallace::
# 895 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_NeverBeenToSkyPillar, MSGBOX_DEFAULT
# 896 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 897 "data/maps/SootopolisCity/scripts.pory"
	end
# 898 "data/maps/SootopolisCity/scripts.pory"

# 899 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StevenLeadPlayerCaveOfOrigin::
# 900 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_InvolvedWithCrisisComeWithMe, MSGBOX_DEFAULT
# 901 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 902 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_FACING, DIR_WEST, SootopolisCity_EventScript_StartWalkToCaveOfOriginWest
# 903 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, SootopolisCity_EventScript_StartWalkToCaveOfOriginNorth
# 904 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_DoesThisMakeYourFearPokemon, MSGBOX_DEFAULT
# 905 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 906 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenWalkToCaveOfOrigin
# 907 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerWalkToCaveOfOrigin
# 908 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 909 "data/maps/SootopolisCity/scripts.pory"
	delay 120
# 910 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_EXPERT, SootopolisCity_Movement_ExpertMoveAside
# 911 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 912 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenArriveCaveEntrance
# 913 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerArriveCaveEntrance
# 914 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 915 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_HereWereAreHelpWallace, MSGBOX_DEFAULT
# 916 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 917 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN
# 918 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerEnterCaveOfOrigin
# 919 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 920 "data/maps/SootopolisCity/scripts.pory"
	warp MAP_CAVE_OF_ORIGIN_ENTRANCE, 9, 20
# 921 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 922 "data/maps/SootopolisCity/scripts.pory"
	end
# 923 "data/maps/SootopolisCity/scripts.pory"

# 924 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StartWalkToCaveOfOriginWest::
# 925 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenStartWalkToCaveOfOrigin
# 926 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginWest
# 927 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 928 "data/maps/SootopolisCity/scripts.pory"
	return
# 929 "data/maps/SootopolisCity/scripts.pory"

# 930 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_StartWalkToCaveOfOriginNorth::
# 931 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_STEVEN, SootopolisCity_Movement_StevenStartWalkToCaveOfOrigin
# 932 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_PLAYER, SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginNorth
# 933 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 934 "data/maps/SootopolisCity/scripts.pory"
	return
# 935 "data/maps/SootopolisCity/scripts.pory"

# 936 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_StevenStartWalkToCaveOfOrigin:
# 937 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 938 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 939 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 940 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 941 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 942 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 943 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 944 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 945 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 946 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 947 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 948 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 949 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 950 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 951 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 952 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 953 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 954 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 955 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 956 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 957 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 958 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 959 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 960 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 961 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 962 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 963 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 964 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 965 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 966 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 967 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 968 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 969 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 970 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 971 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 972 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_down
# 973 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 974 "data/maps/SootopolisCity/scripts.pory"

# 975 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginWest:
# 976 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 977 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 978 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 979 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 980 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 981 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 982 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 983 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 984 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 985 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 986 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 987 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 988 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 989 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 990 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 991 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 992 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 993 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 994 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 995 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 996 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 997 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 998 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 999 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1000 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1001 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1002 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1003 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1004 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1005 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1006 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1007 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1008 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1009 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1010 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1011 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1012 "data/maps/SootopolisCity/scripts.pory"

# 1013 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerStartWalkToCaveOfOriginNorth:
# 1014 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1015 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1016 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1017 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1018 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1019 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1020 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1021 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1022 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1023 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1024 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1025 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1026 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1027 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1028 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1029 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1030 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1031 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1032 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1033 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1034 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1035 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1036 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1037 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1038 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1039 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1040 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1041 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1042 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1043 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1044 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1045 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1046 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1047 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1048 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1049 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1050 "data/maps/SootopolisCity/scripts.pory"

# 1051 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_StevenWalkToCaveOfOrigin:
# 1052 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1053 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1054 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1055 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1056 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1057 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1058 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1059 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1060 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1061 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1062 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1063 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1064 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1065 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1066 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1067 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1068 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1069 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1070 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1071 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1072 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1073 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1074 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1075 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1076 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1077 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1078 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1079 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1080 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1081 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1082 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1083 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1084 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1085 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1086 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1087 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1088 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1089 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1090 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1091 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1092 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1093 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1094 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1095 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1096 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1097 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1098 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1099 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1100 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1101 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1102 "data/maps/SootopolisCity/scripts.pory"
	delay_4
# 1103 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_left
# 1104 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 1105 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 1106 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1107 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1108 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1109 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1110 "data/maps/SootopolisCity/scripts.pory"

# 1111 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerWalkToCaveOfOrigin:
# 1112 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1113 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1114 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1115 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1116 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1117 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1118 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1119 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1120 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1121 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1122 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1123 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1124 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1125 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1126 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1127 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1128 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1129 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1130 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1131 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1132 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1133 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1134 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1135 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1136 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1137 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1138 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1139 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1140 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1141 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1142 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1143 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1144 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1145 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1146 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1147 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1148 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1149 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1150 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1151 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1152 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1153 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1154 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1155 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1156 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1157 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1158 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1159 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1160 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1161 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1162 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1163 "data/maps/SootopolisCity/scripts.pory"

# 1164 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_ExpertMoveAside:
# 1165 "data/maps/SootopolisCity/scripts.pory"
	walk_slow_left
# 1166 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_right
# 1167 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1168 "data/maps/SootopolisCity/scripts.pory"

# 1169 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_StevenArriveCaveEntrance:
# 1170 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1171 "data/maps/SootopolisCity/scripts.pory"
	walk_down
# 1172 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1173 "data/maps/SootopolisCity/scripts.pory"
	delay_8
# 1174 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1175 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1176 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1177 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1178 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1179 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_left
# 1180 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1181 "data/maps/SootopolisCity/scripts.pory"

# 1182 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerArriveCaveEntrance:
# 1183 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 1184 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 1185 "data/maps/SootopolisCity/scripts.pory"
	delay_16
# 1186 "data/maps/SootopolisCity/scripts.pory"
	delay_8
# 1187 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1188 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1189 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1190 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1191 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1192 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_right
# 1193 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1194 "data/maps/SootopolisCity/scripts.pory"

# 1195 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_PlayerEnterCaveOfOrigin:
# 1196 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1197 "data/maps/SootopolisCity/scripts.pory"
	walk_up
# 1198 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1199 "data/maps/SootopolisCity/scripts.pory"

# 1200 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Boy2::
# 1201 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 1202 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BOY_2, Common_Movement_FacePlayer
# 1203 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1204 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_Boy2Rayquaza
# 1205 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_TwoPokemonArentAngry, MSGBOX_DEFAULT
# 1206 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1207 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BOY_2, Common_Movement_FaceOriginalDirection
# 1208 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1209 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1210 "data/maps/SootopolisCity/scripts.pory"
	end
# 1211 "data/maps/SootopolisCity/scripts.pory"

# 1212 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Boy2Rayquaza::
# 1213 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_FlyingMonStoppedRampage, MSGBOX_DEFAULT
# 1214 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1215 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1216 "data/maps/SootopolisCity/scripts.pory"
	end
# 1217 "data/maps/SootopolisCity/scripts.pory"

# 1218 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_BlackBelt::
# 1219 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 1220 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_BlackBeltRayquaza
# 1221 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GoRedAndBlueMon, MSGBOX_DEFAULT
# 1222 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1223 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BLACK_BELT, Common_Movement_FacePlayer
# 1224 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1225 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_DoYouKnowMonNames, MSGBOX_DEFAULT
# 1226 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1227 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BLACK_BELT, Common_Movement_FaceOriginalDirection
# 1228 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1229 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1230 "data/maps/SootopolisCity/scripts.pory"
	end
# 1231 "data/maps/SootopolisCity/scripts.pory"

# 1232 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_BlackBeltRayquaza::
# 1233 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_BLACK_BELT, Common_Movement_FacePlayer
# 1234 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1235 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GreenOneSettlesThings, MSGBOX_DEFAULT
# 1236 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1237 "data/maps/SootopolisCity/scripts.pory"
	end
# 1238 "data/maps/SootopolisCity/scripts.pory"

# 1239 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Girl::
# 1240 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 1241 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GIRL, Common_Movement_FacePlayer
# 1242 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1243 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_GirlRayquaza
# 1244 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_SootopolisWillBeWrecked, MSGBOX_DEFAULT
# 1245 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1246 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_GIRL, Common_Movement_FaceOriginalDirection
# 1247 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1248 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1249 "data/maps/SootopolisCity/scripts.pory"
	end
# 1250 "data/maps/SootopolisCity/scripts.pory"

# 1251 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GirlRayquaza::
# 1252 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_SootopolisDidntGetWrecked, MSGBOX_DEFAULT
# 1253 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1254 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1255 "data/maps/SootopolisCity/scripts.pory"
	end
# 1256 "data/maps/SootopolisCity/scripts.pory"

# 1257 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Maniac::
# 1258 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 1259 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_MANIAC, Common_Movement_FacePlayer
# 1260 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1261 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_ManiacRayquaza
# 1262 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_SeeingLegendWithOwnEyes, MSGBOX_DEFAULT
# 1263 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1264 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_MANIAC, Common_Movement_FaceOriginalDirection
# 1265 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1266 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1267 "data/maps/SootopolisCity/scripts.pory"
	end
# 1268 "data/maps/SootopolisCity/scripts.pory"

# 1269 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_ManiacRayquaza::
# 1270 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_SawLegendWithOwnEyes, MSGBOX_DEFAULT
# 1271 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1272 "data/maps/SootopolisCity/scripts.pory"
	end
# 1273 "data/maps/SootopolisCity/scripts.pory"

# 1274 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Wallace::
# 1275 "data/maps/SootopolisCity/scripts.pory"
	lock
# 1276 "data/maps/SootopolisCity/scripts.pory"
	faceplayer
# 1277 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 4, SootopolisCity_EventScript_GoToSkyPillar
# 1278 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_RECEIVED_HM_WATERFALL, SootopolisCity_EventScript_GoToGym
# 1279 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, SootopolisCity_EventScript_GiveWaterfall
# 1280 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_AquaMagmaDidntMeanHarm, MSGBOX_DEFAULT
# 1281 "data/maps/SootopolisCity/scripts.pory"
	release
# 1282 "data/maps/SootopolisCity/scripts.pory"
	end
# 1283 "data/maps/SootopolisCity/scripts.pory"

# 1284 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GiveWaterfall::
# 1285 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_ThankYouForHelpAcceptThis, MSGBOX_DEFAULT
# 1286 "data/maps/SootopolisCity/scripts.pory"
	giveitem ITEM_HM_WATERFALL
# 1287 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_RECEIVED_HM_WATERFALL
# 1288 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_ExplainWaterfallGoToGym, MSGBOX_DEFAULT
# 1289 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1290 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_FACING, DIR_NORTH, SootopolisCity_EventScript_WallaceMoveFromGym
# 1291 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_FACING, DIR_EAST, SootopolisCity_EventScript_WallaceMoveFromGym
# 1292 "data/maps/SootopolisCity/scripts.pory"
	call_if_eq VAR_FACING, DIR_WEST, SootopolisCity_EventScript_WallaceMoveFromGymWest
# 1293 "data/maps/SootopolisCity/scripts.pory"
	release
# 1294 "data/maps/SootopolisCity/scripts.pory"
	end
# 1295 "data/maps/SootopolisCity/scripts.pory"

# 1296 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_WallaceMoveFromGym::
# 1297 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_WALLACE, SootopolisCity_Movement_WallaceMoveFromGym
# 1298 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1299 "data/maps/SootopolisCity/scripts.pory"
	copyobjectxytoperm LOCALID_SOOTOPOLIS_WALLACE
# 1300 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SOOTOPOLIS_WALLACE_STATE, 1
# 1301 "data/maps/SootopolisCity/scripts.pory"
	return
# 1302 "data/maps/SootopolisCity/scripts.pory"

# 1303 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_WallaceMoveFromGymWest::
# 1304 "data/maps/SootopolisCity/scripts.pory"
	applymovement LOCALID_SOOTOPOLIS_WALLACE, SootopolisCity_Movement_WallaceMoveFromGymWest
# 1305 "data/maps/SootopolisCity/scripts.pory"
	waitmovement 0
# 1306 "data/maps/SootopolisCity/scripts.pory"
	copyobjectxytoperm LOCALID_SOOTOPOLIS_WALLACE
# 1307 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_SOOTOPOLIS_WALLACE_STATE, 2
# 1308 "data/maps/SootopolisCity/scripts.pory"
	return
# 1309 "data/maps/SootopolisCity/scripts.pory"

# 1310 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GoToSkyPillar::
# 1311 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_HaventYouScaledSkyPillar, MSGBOX_DEFAULT
# 1312 "data/maps/SootopolisCity/scripts.pory"
	release
# 1313 "data/maps/SootopolisCity/scripts.pory"
	end
# 1314 "data/maps/SootopolisCity/scripts.pory"

# 1315 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_GoToGym::
# 1316 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_DazzledByMentor, MSGBOX_DEFAULT
# 1317 "data/maps/SootopolisCity/scripts.pory"
	release
# 1318 "data/maps/SootopolisCity/scripts.pory"
	end
# 1319 "data/maps/SootopolisCity/scripts.pory"

# 1320 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_WallaceMoveFromGym:
# 1321 "data/maps/SootopolisCity/scripts.pory"
	walk_right
# 1322 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_down
# 1323 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1324 "data/maps/SootopolisCity/scripts.pory"

# 1325 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_WallaceMoveFromGymWest:
# 1326 "data/maps/SootopolisCity/scripts.pory"
	walk_left
# 1327 "data/maps/SootopolisCity/scripts.pory"
	walk_in_place_faster_down
# 1328 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1329 "data/maps/SootopolisCity/scripts.pory"

# 1330 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Maxie::
# 1331 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 1332 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_MaxieRayquaza
# 1333 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_GroudonPleaseStop, MSGBOX_DEFAULT
# 1334 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1335 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1336 "data/maps/SootopolisCity/scripts.pory"
	end
# 1337 "data/maps/SootopolisCity/scripts.pory"

# 1338 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_MaxieRayquaza::
# 1339 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_AfterAllOurScheming, MSGBOX_DEFAULT
# 1340 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_MET_MAXIE_SOOTOPOLIS
# 1341 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_MET_ARCHIE_SOOTOPOLIS, SootopolisCity_EventScript_MaxieArchieLeave
# 1342 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1343 "data/maps/SootopolisCity/scripts.pory"
	end
# 1344 "data/maps/SootopolisCity/scripts.pory"

# 1345 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_Archie::
# 1346 "data/maps/SootopolisCity/scripts.pory"
	lockall
# 1347 "data/maps/SootopolisCity/scripts.pory"
	goto_if_eq VAR_SOOTOPOLIS_CITY_STATE, 5, SootopolisCity_EventScript_ArchieRayquaza
# 1348 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_KyogreCalmDown, MSGBOX_DEFAULT
# 1349 "data/maps/SootopolisCity/scripts.pory"
	closemessage
# 1350 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1351 "data/maps/SootopolisCity/scripts.pory"
	end
# 1352 "data/maps/SootopolisCity/scripts.pory"

# 1353 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_ArchieRayquaza::
# 1354 "data/maps/SootopolisCity/scripts.pory"
	msgbox SootopolisCity_Text_TryingMeaninglessToPokemon, MSGBOX_DEFAULT
# 1355 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_MET_ARCHIE_SOOTOPOLIS
# 1356 "data/maps/SootopolisCity/scripts.pory"
	goto_if_set FLAG_MET_MAXIE_SOOTOPOLIS, SootopolisCity_EventScript_MaxieArchieLeave
# 1357 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1358 "data/maps/SootopolisCity/scripts.pory"
	end
# 1359 "data/maps/SootopolisCity/scripts.pory"

# 1360 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_EventScript_MaxieArchieLeave::
# 1361 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_MAXIE
# 1362 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_HIDE_SOOTOPOLIS_CITY_ARCHIE
# 1363 "data/maps/SootopolisCity/scripts.pory"
	setflag FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE
# 1364 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_HIDE_MT_PYRE_SUMMIT_MAXIE
# 1365 "data/maps/SootopolisCity/scripts.pory"
	clearflag FLAG_HIDE_MT_PYRE_SUMMIT_ARCHIE
# 1366 "data/maps/SootopolisCity/scripts.pory"
	setvar VAR_MT_PYRE_STATE, 2
# 1367 "data/maps/SootopolisCity/scripts.pory"
	warpsilent MAP_SOOTOPOLIS_CITY, 31, 34
# 1368 "data/maps/SootopolisCity/scripts.pory"
	waitstate
# 1369 "data/maps/SootopolisCity/scripts.pory"
	releaseall
# 1370 "data/maps/SootopolisCity/scripts.pory"
	end
# 1371 "data/maps/SootopolisCity/scripts.pory"

# 1372 "data/maps/SootopolisCity/scripts.pory"
@ Unused
# 1373 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_Levitate::
# 1374 "data/maps/SootopolisCity/scripts.pory"
	levitate
# 1375 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1376 "data/maps/SootopolisCity/scripts.pory"

# 1377 "data/maps/SootopolisCity/scripts.pory"
@ Unused
# 1378 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Movement_DestroyTask::
# 1379 "data/maps/SootopolisCity/scripts.pory"
	destroy_extra_task
# 1380 "data/maps/SootopolisCity/scripts.pory"
	step_end
# 1381 "data/maps/SootopolisCity/scripts.pory"

# 1382 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_GymSign:
# 1383 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS CITY POKéMON GYM\n"
# 1384 "data/maps/SootopolisCity/scripts.pory"
	.string "LEADER: JUAN\p"
# 1385 "data/maps/SootopolisCity/scripts.pory"
	.string "“The GYM LEADER with the beauty\n"
# 1386 "data/maps/SootopolisCity/scripts.pory"
	.string "of pure water!”$"
# 1387 "data/maps/SootopolisCity/scripts.pory"

# 1388 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_CitySign:
# 1389 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS CITY\p"
# 1390 "data/maps/SootopolisCity/scripts.pory"
	.string "“The mystical city where history\n"
# 1391 "data/maps/SootopolisCity/scripts.pory"
	.string "slumbers.”$"
# 1392 "data/maps/SootopolisCity/scripts.pory"

# 1393 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_DoorIsClosed:
# 1394 "data/maps/SootopolisCity/scripts.pory"
	.string "The door is closed.$"
# 1395 "data/maps/SootopolisCity/scripts.pory"

# 1396 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_PhysicallyFitLivingHere:
# 1397 "data/maps/SootopolisCity/scripts.pory"
	.string "Diving in the sea. Climbing up and\n"
# 1398 "data/maps/SootopolisCity/scripts.pory"
	.string "down stairs all the time…\p"
# 1399 "data/maps/SootopolisCity/scripts.pory"
	.string "If you live in this town, you end up\n"
# 1400 "data/maps/SootopolisCity/scripts.pory"
	.string "getting physically fit.$"
# 1401 "data/maps/SootopolisCity/scripts.pory"

# 1402 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_GiantPokemonSuddenlyAppeared:
# 1403 "data/maps/SootopolisCity/scripts.pory"
	.string "These giant POKéMON suddenly appeared\n"
# 1404 "data/maps/SootopolisCity/scripts.pory"
	.string "in the middle of the city!\p"
# 1405 "data/maps/SootopolisCity/scripts.pory"
	.string "And, I've never seen them before!\p"
# 1406 "data/maps/SootopolisCity/scripts.pory"
	.string "Why are they smashing into each\n"
# 1407 "data/maps/SootopolisCity/scripts.pory"
	.string "other like that?\p"
# 1408 "data/maps/SootopolisCity/scripts.pory"
	.string "Why can't they be friends, those\n"
# 1409 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON?$"
# 1410 "data/maps/SootopolisCity/scripts.pory"

# 1411 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_WhatIsThatGreenPokemon:
# 1412 "data/maps/SootopolisCity/scripts.pory"
	.string "What? What? What?\n"
# 1413 "data/maps/SootopolisCity/scripts.pory"
	.string "What is that green POKéMON?!$"
# 1414 "data/maps/SootopolisCity/scripts.pory"

# 1415 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_WhereDidLegendariesGo:
# 1416 "data/maps/SootopolisCity/scripts.pory"
	.string "GROUDON and KYOGRE…\n"
# 1417 "data/maps/SootopolisCity/scripts.pory"
	.string "Where did they go?\p"
# 1418 "data/maps/SootopolisCity/scripts.pory"
	.string "Will they cause droughts or downpours\n"
# 1419 "data/maps/SootopolisCity/scripts.pory"
	.string "somewhere else?$"
# 1420 "data/maps/SootopolisCity/scripts.pory"

# 1421 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_TwoPokemonArentAngry:
# 1422 "data/maps/SootopolisCity/scripts.pory"
	.string "I just get this sense somehow that\n"
# 1423 "data/maps/SootopolisCity/scripts.pory"
	.string "the two POKéMON aren't angry.\p"
# 1424 "data/maps/SootopolisCity/scripts.pory"
	.string "I think… They probably can't control\n"
# 1425 "data/maps/SootopolisCity/scripts.pory"
	.string "their own power…$"
# 1426 "data/maps/SootopolisCity/scripts.pory"

# 1427 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_FlyingMonStoppedRampage:
# 1428 "data/maps/SootopolisCity/scripts.pory"
	.string "That flying POKéMON came down from\n"
# 1429 "data/maps/SootopolisCity/scripts.pory"
	.string "the sky and stopped the rampaging\l"
# 1430 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON…$"
# 1431 "data/maps/SootopolisCity/scripts.pory"

# 1432 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_WonderWhatWorldIsLike:
# 1433 "data/maps/SootopolisCity/scripts.pory"
	.string "I… I've never been out of this city.\p"
# 1434 "data/maps/SootopolisCity/scripts.pory"
	.string "I wonder what the world is like on\n"
# 1435 "data/maps/SootopolisCity/scripts.pory"
	.string "the other side of this round sky?$"
# 1436 "data/maps/SootopolisCity/scripts.pory"

# 1437 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_ThisIsWicked:
# 1438 "data/maps/SootopolisCity/scripts.pory"
	.string "Wow!\n"
# 1439 "data/maps/SootopolisCity/scripts.pory"
	.string "This is wicked!$"
# 1440 "data/maps/SootopolisCity/scripts.pory"

# 1441 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_ThatWasWicked:
# 1442 "data/maps/SootopolisCity/scripts.pory"
	.string "Wow!\n"
# 1443 "data/maps/SootopolisCity/scripts.pory"
	.string "That was wicked!$"
# 1444 "data/maps/SootopolisCity/scripts.pory"

# 1445 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_GoRedAndBlueMon:
# 1446 "data/maps/SootopolisCity/scripts.pory"
	.string "Go for it, red POKéMON!\n"
# 1447 "data/maps/SootopolisCity/scripts.pory"
	.string "Don't back off, blue POKéMON!$"
# 1448 "data/maps/SootopolisCity/scripts.pory"

# 1449 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_DoYouKnowMonNames:
# 1450 "data/maps/SootopolisCity/scripts.pory"
	.string "… … … … … …\p"
# 1451 "data/maps/SootopolisCity/scripts.pory"
	.string "Hi, do you know the names of those\n"
# 1452 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON fighting over there?$"
# 1453 "data/maps/SootopolisCity/scripts.pory"

# 1454 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_GreenOneSettlesThings:
# 1455 "data/maps/SootopolisCity/scripts.pory"
	.string "I was wondering which one would win,\n"
# 1456 "data/maps/SootopolisCity/scripts.pory"
	.string "the red one or the blue one, but, oh no,\l"
# 1457 "data/maps/SootopolisCity/scripts.pory"
	.string "it's the green one that settles things!\p"
# 1458 "data/maps/SootopolisCity/scripts.pory"
	.string "Talk about a huge turn of events!$"
# 1459 "data/maps/SootopolisCity/scripts.pory"

# 1460 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_SeeingLegendWithOwnEyes:
# 1461 "data/maps/SootopolisCity/scripts.pory"
	.string "There's an ancient legend that claims\n"
# 1462 "data/maps/SootopolisCity/scripts.pory"
	.string "the land and sea were shaped by\l"
# 1463 "data/maps/SootopolisCity/scripts.pory"
	.string "a colossal battle between POKéMON.\p"
# 1464 "data/maps/SootopolisCity/scripts.pory"
	.string "Well, I'm seeing that happen with\n"
# 1465 "data/maps/SootopolisCity/scripts.pory"
	.string "my very own eyes!\p"
# 1466 "data/maps/SootopolisCity/scripts.pory"
	.string "Whoa! I never expected to be\n"
# 1467 "data/maps/SootopolisCity/scripts.pory"
	.string "witness to something this huge!$"
# 1468 "data/maps/SootopolisCity/scripts.pory"

# 1469 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_SawLegendWithOwnEyes:
# 1470 "data/maps/SootopolisCity/scripts.pory"
	.string "There's an ancient legend that claims\n"
# 1471 "data/maps/SootopolisCity/scripts.pory"
	.string "the land and sea were shaped by\l"
# 1472 "data/maps/SootopolisCity/scripts.pory"
	.string "a colossal battle between POKéMON.\p"
# 1473 "data/maps/SootopolisCity/scripts.pory"
	.string "Well, I saw that happen with\n"
# 1474 "data/maps/SootopolisCity/scripts.pory"
	.string "my very own eyes!\p"
# 1475 "data/maps/SootopolisCity/scripts.pory"
	.string "Whoa! I never expected to be\n"
# 1476 "data/maps/SootopolisCity/scripts.pory"
	.string "witness to something this huge!$"
# 1477 "data/maps/SootopolisCity/scripts.pory"

# 1478 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_BigPokemonFighting:
# 1479 "data/maps/SootopolisCity/scripts.pory"
	.string "A big POKéMON is fighting with\n"
# 1480 "data/maps/SootopolisCity/scripts.pory"
	.string "another big POKéMON!\p"
# 1481 "data/maps/SootopolisCity/scripts.pory"
	.string "Please, someone make them stop!$"
# 1482 "data/maps/SootopolisCity/scripts.pory"

# 1483 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_PrettyMonCameFromSky:
# 1484 "data/maps/SootopolisCity/scripts.pory"
	.string "A pretty POKéMON came down from\n"
# 1485 "data/maps/SootopolisCity/scripts.pory"
	.string "the sky…$"
# 1486 "data/maps/SootopolisCity/scripts.pory"

# 1487 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_SootopolisWillBeWrecked:
# 1488 "data/maps/SootopolisCity/scripts.pory"
	.string "Oh, no!\n"
# 1489 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS CITY will get wrecked!$"
# 1490 "data/maps/SootopolisCity/scripts.pory"

# 1491 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_SootopolisDidntGetWrecked:
# 1492 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS CITY didn't get wrecked!$"
# 1493 "data/maps/SootopolisCity/scripts.pory"

# 1494 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_NoOrdinaryTourist:
# 1495 "data/maps/SootopolisCity/scripts.pory"
	.string "Hm!\n"
# 1496 "data/maps/SootopolisCity/scripts.pory"
	.string "You've come all the way to SOOTOPOLIS?\l"
# 1497 "data/maps/SootopolisCity/scripts.pory"
	.string "You're no ordinary tourist.\p"
# 1498 "data/maps/SootopolisCity/scripts.pory"
	.string "But I suppose that doesn't make you\n"
# 1499 "data/maps/SootopolisCity/scripts.pory"
	.string "an extraordinary tourist, either.$"
# 1500 "data/maps/SootopolisCity/scripts.pory"

# 1501 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_CityRegainedCalm:
# 1502 "data/maps/SootopolisCity/scripts.pory"
	.string "The city has regained its calm…$"
# 1503 "data/maps/SootopolisCity/scripts.pory"

# 1504 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_CaveOfOriginPleaseLeave:
# 1505 "data/maps/SootopolisCity/scripts.pory"
	.string "Who might you be?\p"
# 1506 "data/maps/SootopolisCity/scripts.pory"
	.string "This is the CAVE OF ORIGIN.\p"
# 1507 "data/maps/SootopolisCity/scripts.pory"
	.string "The spirits of POKéMON, becalmed at\n"
# 1508 "data/maps/SootopolisCity/scripts.pory"
	.string "MT. PYRE, are said to be revived here.\p"
# 1509 "data/maps/SootopolisCity/scripts.pory"
	.string "Please leave.$"
# 1510 "data/maps/SootopolisCity/scripts.pory"

# 1511 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_LeadSuperiorTrainerToCave:
# 1512 "data/maps/SootopolisCity/scripts.pory"
	.string "A person with a strong will and\n"
# 1513 "data/maps/SootopolisCity/scripts.pory"
	.string "superior talent…\p"
# 1514 "data/maps/SootopolisCity/scripts.pory"
	.string "A TRAINER who has knowledge and\n"
# 1515 "data/maps/SootopolisCity/scripts.pory"
	.string "experience of many kinds of POKéMON…\p"
# 1516 "data/maps/SootopolisCity/scripts.pory"
	.string "If such a person were to appear, I was\n"
# 1517 "data/maps/SootopolisCity/scripts.pory"
	.string "instructed by WALLACE to lead that\l"
# 1518 "data/maps/SootopolisCity/scripts.pory"
	.string "TRAINER to this CAVE.$"
# 1519 "data/maps/SootopolisCity/scripts.pory"

# 1520 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_AwakenedPokemonClash:
# 1521 "data/maps/SootopolisCity/scripts.pory"
	.string "Oh, my…\p"
# 1522 "data/maps/SootopolisCity/scripts.pory"
	.string "The clash between the two awakened\n"
# 1523 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON was quelled by the awakening\l"
# 1524 "data/maps/SootopolisCity/scripts.pory"
	.string "of a third POKéMON…$"
# 1525 "data/maps/SootopolisCity/scripts.pory"

# 1526 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_CaveOfOriginSleepsToo:
# 1527 "data/maps/SootopolisCity/scripts.pory"
	.string "This is the CAVE OF ORIGIN…\p"
# 1528 "data/maps/SootopolisCity/scripts.pory"
	.string "With the passing of the crisis,\n"
# 1529 "data/maps/SootopolisCity/scripts.pory"
	.string "the cave, too, shall sleep…$"
# 1530 "data/maps/SootopolisCity/scripts.pory"

# 1531 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_SootopolisSkyBeautiful:
# 1532 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS sprang up as a town in\n"
# 1533 "data/maps/SootopolisCity/scripts.pory"
	.string "the crater of a volcano.\p"
# 1534 "data/maps/SootopolisCity/scripts.pory"
	.string "If you look up at the sky, the lip of\n"
# 1535 "data/maps/SootopolisCity/scripts.pory"
	.string "the crater is also visible.\l"
# 1536 "data/maps/SootopolisCity/scripts.pory"
	.string "So, all you see is the sky in a circle.\p"
# 1537 "data/maps/SootopolisCity/scripts.pory"
	.string "But that's what makes the sky above\n"
# 1538 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS the most beautiful.$"
# 1539 "data/maps/SootopolisCity/scripts.pory"

# 1540 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_GiganticPokemonFight:
# 1541 "data/maps/SootopolisCity/scripts.pory"
	.string "When two POKéMON that gigantic\n"
# 1542 "data/maps/SootopolisCity/scripts.pory"
	.string "are fighting that savagely, there's\l"
# 1543 "data/maps/SootopolisCity/scripts.pory"
	.string "not much that we can do.$"
# 1544 "data/maps/SootopolisCity/scripts.pory"

# 1545 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_FearedWorstWhenPokemonFlewDown:
# 1546 "data/maps/SootopolisCity/scripts.pory"
	.string "When that third POKéMON flew down,\n"
# 1547 "data/maps/SootopolisCity/scripts.pory"
	.string "I feared the worst.$"
# 1548 "data/maps/SootopolisCity/scripts.pory"

# 1549 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_NightSkyFavoriteScenery:
# 1550 "data/maps/SootopolisCity/scripts.pory"
	.string "A circle of a night sky framed by\n"
# 1551 "data/maps/SootopolisCity/scripts.pory"
	.string "the crater of a volcano…\p"
# 1552 "data/maps/SootopolisCity/scripts.pory"
	.string "And in that ring, stars flicker and\n"
# 1553 "data/maps/SootopolisCity/scripts.pory"
	.string "blink as if they were alive…\l"
# 1554 "data/maps/SootopolisCity/scripts.pory"
	.string "It's my favorite scenery.$"
# 1555 "data/maps/SootopolisCity/scripts.pory"

# 1556 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_WeatherWentWild:
# 1557 "data/maps/SootopolisCity/scripts.pory"
	.string "The weather was clear this morning,\n"
# 1558 "data/maps/SootopolisCity/scripts.pory"
	.string "but…\p"
# 1559 "data/maps/SootopolisCity/scripts.pory"
	.string "All of a sudden, dark clouds brewed up,\n"
# 1560 "data/maps/SootopolisCity/scripts.pory"
	.string "rain started falling in sheets, and\l"
# 1561 "data/maps/SootopolisCity/scripts.pory"
	.string "there was thunder and lightning, too.\p"
# 1562 "data/maps/SootopolisCity/scripts.pory"
	.string "The weather just went completely\n"
# 1563 "data/maps/SootopolisCity/scripts.pory"
	.string "wild!\p"
# 1564 "data/maps/SootopolisCity/scripts.pory"
	.string "Is all of this because of those\n"
# 1565 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON?$"
# 1566 "data/maps/SootopolisCity/scripts.pory"

# 1567 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_YouBroughtFlyingMon:
# 1568 "data/maps/SootopolisCity/scripts.pory"
	.string "Oh?\p"
# 1569 "data/maps/SootopolisCity/scripts.pory"
	.string "It was you who brought that flying\n"
# 1570 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON here?\p"
# 1571 "data/maps/SootopolisCity/scripts.pory"
	.string "Well, aren't you amazing!$"
# 1572 "data/maps/SootopolisCity/scripts.pory"

# 1573 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_GroudonPleaseStop:
# 1574 "data/maps/SootopolisCity/scripts.pory"
	.string "MAXIE: G… GROUDON…\n"
# 1575 "data/maps/SootopolisCity/scripts.pory"
	.string "Please! Stop what you're doing!\p"
# 1576 "data/maps/SootopolisCity/scripts.pory"
	.string "I know the extent of your power now!\p"
# 1577 "data/maps/SootopolisCity/scripts.pory"
	.string "If you keep going, all HOENN, not just\n"
# 1578 "data/maps/SootopolisCity/scripts.pory"
	.string "SOOTOPOLIS, will be utterly ruined!$"
# 1579 "data/maps/SootopolisCity/scripts.pory"

# 1580 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_AfterAllOurScheming:
# 1581 "data/maps/SootopolisCity/scripts.pory"
	.string "MAXIE: So the super-ancient POKéMON\n"
# 1582 "data/maps/SootopolisCity/scripts.pory"
	.string "weren't only GROUDON and KYOGRE…\p"
# 1583 "data/maps/SootopolisCity/scripts.pory"
	.string "After all our fruitless scheming and\n"
# 1584 "data/maps/SootopolisCity/scripts.pory"
	.string "frantic efforts, that one POKéMON's\l"
# 1585 "data/maps/SootopolisCity/scripts.pory"
	.string "simple action puts everything right\l"
# 1586 "data/maps/SootopolisCity/scripts.pory"
	.string "again as if nothing had happened…\p"
# 1587 "data/maps/SootopolisCity/scripts.pory"
	.string "Fu…\n"
# 1588 "data/maps/SootopolisCity/scripts.pory"
	.string "Fuhahaha…$"
# 1589 "data/maps/SootopolisCity/scripts.pory"

# 1590 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_KyogreCalmDown:
# 1591 "data/maps/SootopolisCity/scripts.pory"
	.string "ARCHIE: KYOGRE! What's wrong?!\n"
# 1592 "data/maps/SootopolisCity/scripts.pory"
	.string "Look over here! It's the RED ORB!\l"
# 1593 "data/maps/SootopolisCity/scripts.pory"
	.string "Calm down! KYOGRE!\p"
# 1594 "data/maps/SootopolisCity/scripts.pory"
	.string "… … … … … …\n"
# 1595 "data/maps/SootopolisCity/scripts.pory"
	.string "… … … … … …\p"
# 1596 "data/maps/SootopolisCity/scripts.pory"
	.string "It's no good!\n"
# 1597 "data/maps/SootopolisCity/scripts.pory"
	.string "It's not responding at all!$"
# 1598 "data/maps/SootopolisCity/scripts.pory"

# 1599 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_TryingMeaninglessToPokemon:
# 1600 "data/maps/SootopolisCity/scripts.pory"
	.string "ARCHIE: KYOGRE and GROUDON both\n"
# 1601 "data/maps/SootopolisCity/scripts.pory"
	.string "flew off to who knows where.\p"
# 1602 "data/maps/SootopolisCity/scripts.pory"
	.string "The weather in HOENN has returned\n"
# 1603 "data/maps/SootopolisCity/scripts.pory"
	.string "to its normal state…\p"
# 1604 "data/maps/SootopolisCity/scripts.pory"
	.string "Haha…\n"
# 1605 "data/maps/SootopolisCity/scripts.pory"
	.string "Hahaha…\p"
# 1606 "data/maps/SootopolisCity/scripts.pory"
	.string "Maybe what we were trying to do was\n"
# 1607 "data/maps/SootopolisCity/scripts.pory"
	.string "something small, even meaningless,\l"
# 1608 "data/maps/SootopolisCity/scripts.pory"
	.string "to POKéMON…$"
# 1609 "data/maps/SootopolisCity/scripts.pory"

# 1610 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_InvolvedWithCrisisComeWithMe:
# 1611 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: Those POKéMON fighting…\n"
# 1612 "data/maps/SootopolisCity/scripts.pory"
	.string "GROUDON… And KYOGRE…\p"
# 1613 "data/maps/SootopolisCity/scripts.pory"
	.string "The two super-ancient POKéMON\n"
# 1614 "data/maps/SootopolisCity/scripts.pory"
	.string "were awakened from a long sleep…\p"
# 1615 "data/maps/SootopolisCity/scripts.pory"
	.string "And now they are smashing each other\n"
# 1616 "data/maps/SootopolisCity/scripts.pory"
	.string "with their uncontrollable energy…\p"
# 1617 "data/maps/SootopolisCity/scripts.pory"
	.string "…{PLAYER}{KUN}.\p"
# 1618 "data/maps/SootopolisCity/scripts.pory"
	.string "You being here now I'll take to mean\n"
# 1619 "data/maps/SootopolisCity/scripts.pory"
	.string "that you're prepared to become\l"
# 1620 "data/maps/SootopolisCity/scripts.pory"
	.string "involved in this crisis.\p"
# 1621 "data/maps/SootopolisCity/scripts.pory"
	.string "Well, then, there's someone that\n"
# 1622 "data/maps/SootopolisCity/scripts.pory"
	.string "I'd like you to meet.\p"
# 1623 "data/maps/SootopolisCity/scripts.pory"
	.string "Come with me, please.$"
# 1624 "data/maps/SootopolisCity/scripts.pory"

# 1625 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_DoesThisMakeYourFearPokemon:
# 1626 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: Listen, {PLAYER}{KUN}.\p"
# 1627 "data/maps/SootopolisCity/scripts.pory"
	.string "Does seeing GROUDON and KYOGRE make\n"
# 1628 "data/maps/SootopolisCity/scripts.pory"
	.string "you think POKéMON are to be feared?\p"
# 1629 "data/maps/SootopolisCity/scripts.pory"
	.string "But that's not true.\n"
# 1630 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON are really more…\p"
# 1631 "data/maps/SootopolisCity/scripts.pory"
	.string "…Why am I asking you this?\n"
# 1632 "data/maps/SootopolisCity/scripts.pory"
	.string "You already know.$"
# 1633 "data/maps/SootopolisCity/scripts.pory"

# 1634 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_HereWereAreHelpWallace:
# 1635 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: Okay, here we are!\p"
# 1636 "data/maps/SootopolisCity/scripts.pory"
	.string "Inside here you'll find someone named\n"
# 1637 "data/maps/SootopolisCity/scripts.pory"
	.string "WALLACE.\p"
# 1638 "data/maps/SootopolisCity/scripts.pory"
	.string "I think you have what's needed to\n"
# 1639 "data/maps/SootopolisCity/scripts.pory"
	.string "help him…$"
# 1640 "data/maps/SootopolisCity/scripts.pory"

# 1641 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_KnowWhatsNeededToHelpHim:
# 1642 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: I think you have what's\n"
# 1643 "data/maps/SootopolisCity/scripts.pory"
	.string "needed to help him…$"
# 1644 "data/maps/SootopolisCity/scripts.pory"

# 1645 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_NeverBeenToSkyPillar:
# 1646 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: The SKY PILLAR…\p"
# 1647 "data/maps/SootopolisCity/scripts.pory"
	.string "I've never been there.\n"
# 1648 "data/maps/SootopolisCity/scripts.pory"
	.string "I wonder where it could be?$"
# 1649 "data/maps/SootopolisCity/scripts.pory"

# 1650 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_SoThatsRayquaza:
# 1651 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: So that's RAYQUAZA…\p"
# 1652 "data/maps/SootopolisCity/scripts.pory"
	.string "It's incredible how the two rampaging\n"
# 1653 "data/maps/SootopolisCity/scripts.pory"
	.string "POKéMON would flee from it in fear…$"
# 1654 "data/maps/SootopolisCity/scripts.pory"

# 1655 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_MaxieArchieLeft:
# 1656 "data/maps/SootopolisCity/scripts.pory"
	.string "STEVEN: It looks like both MAXIE and\n"
# 1657 "data/maps/SootopolisCity/scripts.pory"
	.string "ARCHIE have gone away somewhere.\p"
# 1658 "data/maps/SootopolisCity/scripts.pory"
	.string "Perhaps they've gone to MT. PYRE to\n"
# 1659 "data/maps/SootopolisCity/scripts.pory"
	.string "return those ORBS…$"
# 1660 "data/maps/SootopolisCity/scripts.pory"

# 1661 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_HaventYouScaledSkyPillar:
# 1662 "data/maps/SootopolisCity/scripts.pory"
	.string "WALLACE: Oh?\n"
# 1663 "data/maps/SootopolisCity/scripts.pory"
	.string "{PLAYER}{KUN}?\p"
# 1664 "data/maps/SootopolisCity/scripts.pory"
	.string "Haven't you scaled the SKY PILLAR\n"
# 1665 "data/maps/SootopolisCity/scripts.pory"
	.string "yet?\p"
# 1666 "data/maps/SootopolisCity/scripts.pory"
	.string "I'm sure that you can make it to\n"
# 1667 "data/maps/SootopolisCity/scripts.pory"
	.string "the top of the SKY PILLAR…$"
# 1668 "data/maps/SootopolisCity/scripts.pory"

# 1669 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_AquaMagmaDidntMeanHarm:
# 1670 "data/maps/SootopolisCity/scripts.pory"
	.string "WALLACE: {PLAYER}{KUN}…\p"
# 1671 "data/maps/SootopolisCity/scripts.pory"
	.string "The leaders of TEAM MAGMA and AQUA,\n"
# 1672 "data/maps/SootopolisCity/scripts.pory"
	.string "I don't think they meant harm.\p"
# 1673 "data/maps/SootopolisCity/scripts.pory"
	.string "It wouldn't hurt to hear what they\n"
# 1674 "data/maps/SootopolisCity/scripts.pory"
	.string "have to say for themselves.$"
# 1675 "data/maps/SootopolisCity/scripts.pory"

# 1676 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_ThankYouForHelpAcceptThis:
# 1677 "data/maps/SootopolisCity/scripts.pory"
	.string "WALLACE: {PLAYER}{KUN}…\n"
# 1678 "data/maps/SootopolisCity/scripts.pory"
	.string "My eyes didn't deceive me.\p"
# 1679 "data/maps/SootopolisCity/scripts.pory"
	.string "Thanks to your help, SOOTOPOLIS…\n"
# 1680 "data/maps/SootopolisCity/scripts.pory"
	.string "No, all of HOENN was saved.\p"
# 1681 "data/maps/SootopolisCity/scripts.pory"
	.string "On behalf of the people, I thank you.\p"
# 1682 "data/maps/SootopolisCity/scripts.pory"
	.string "This is a gift from me.\n"
# 1683 "data/maps/SootopolisCity/scripts.pory"
	.string "Please accept it.$"
# 1684 "data/maps/SootopolisCity/scripts.pory"

# 1685 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_ExplainWaterfallGoToGym:
# 1686 "data/maps/SootopolisCity/scripts.pory"
	.string "That HIDDEN MACHINE contains\n"
# 1687 "data/maps/SootopolisCity/scripts.pory"
	.string "WATERFALL.\p"
# 1688 "data/maps/SootopolisCity/scripts.pory"
	.string "If you have the RAIN BADGE, a POKéMON\n"
# 1689 "data/maps/SootopolisCity/scripts.pory"
	.string "that has learned that HM move can\l"
# 1690 "data/maps/SootopolisCity/scripts.pory"
	.string "force its way up waterfalls.\p"
# 1691 "data/maps/SootopolisCity/scripts.pory"
	.string "And where does one get the RAIN BADGE?\n"
# 1692 "data/maps/SootopolisCity/scripts.pory"
	.string "You know, don't you?\p"
# 1693 "data/maps/SootopolisCity/scripts.pory"
	.string "That's right! You have to beat\n"
# 1694 "data/maps/SootopolisCity/scripts.pory"
	.string "the SOOTOPOLIS GYM LEADER.\p"
# 1695 "data/maps/SootopolisCity/scripts.pory"
	.string "When you're all set to go, step through\n"
# 1696 "data/maps/SootopolisCity/scripts.pory"
	.string "that door.$"
# 1697 "data/maps/SootopolisCity/scripts.pory"

# 1698 "data/maps/SootopolisCity/scripts.pory"
SootopolisCity_Text_DazzledByMentor:
# 1699 "data/maps/SootopolisCity/scripts.pory"
	.string "WALLACE: I'm sure that you will be\n"
# 1700 "data/maps/SootopolisCity/scripts.pory"
	.string "dazzled by my mentor's breathtakingly\l"
# 1701 "data/maps/SootopolisCity/scripts.pory"
	.string "elegant battle style.$"
