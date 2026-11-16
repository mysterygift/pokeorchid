# 1 "data/maps/LilycoveCity/scripts.pory"

# 2 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_MapScripts::
# 3 "data/maps/LilycoveCity/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, LilycoveCity_OnTransition
# 4 "data/maps/LilycoveCity/scripts.pory"
	map_script MAP_SCRIPT_ON_LOAD, LilycoveCity_OnLoad
# 5 "data/maps/LilycoveCity/scripts.pory"
	.byte 0
# 6 "data/maps/LilycoveCity/scripts.pory"

# 7 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_OnTransition:
# 8 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_VISITED_LILYCOVE_CITY
# 9 "data/maps/LilycoveCity/scripts.pory"
	setvar VAR_CONTEST_HALL_STATE, 0
# 10 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_HIDE_LILYCOVE_CONTEST_HALL_REPORTER
# 11 "data/maps/LilycoveCity/scripts.pory"
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
# 12 "data/maps/LilycoveCity/scripts.pory"
	call Common_EventScript_SetupRivalGfxId
# 13 "data/maps/LilycoveCity/scripts.pory"
	end
# 14 "data/maps/LilycoveCity/scripts.pory"

# 15 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_OnLoad:
# 16 "data/maps/LilycoveCity/scripts.pory"
	call_if_unset FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, LilycoveCity_EventScript_SetWailmerMetatiles
# 17 "data/maps/LilycoveCity/scripts.pory"
	end
# 18 "data/maps/LilycoveCity/scripts.pory"

# 19 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_SetWailmerMetatiles::
# 20 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 76, 12, METATILE_Lilycove_Wailmer0, TRUE
# 21 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 77, 12, METATILE_Lilycove_Wailmer1, TRUE
# 22 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 76, 13, METATILE_Lilycove_Wailmer2, TRUE
# 23 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 77, 13, METATILE_Lilycove_Wailmer3, TRUE
# 24 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 76, 14, METATILE_Lilycove_Wailmer0_Alt, TRUE
# 25 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 77, 14, METATILE_Lilycove_Wailmer1_Alt, TRUE
# 26 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 76, 15, METATILE_Lilycove_Wailmer2, TRUE
# 27 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 77, 15, METATILE_Lilycove_Wailmer3, TRUE
# 28 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 77, 16, METATILE_Lilycove_Wailmer0_Alt, TRUE
# 29 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 78, 16, METATILE_Lilycove_Wailmer1_Alt, TRUE
# 30 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 77, 17, METATILE_Lilycove_Wailmer2, TRUE
# 31 "data/maps/LilycoveCity/scripts.pory"
	setmetatile 78, 17, METATILE_Lilycove_Wailmer3, TRUE
# 32 "data/maps/LilycoveCity/scripts.pory"
	return
# 33 "data/maps/LilycoveCity/scripts.pory"

# 34 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BerryGentleman::
# 35 "data/maps/LilycoveCity/scripts.pory"
	lock
# 36 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 37 "data/maps/LilycoveCity/scripts.pory"
	dotimebasedevents
# 38 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_DAILY_LILYCOVE_RECEIVED_BERRY, LilycoveCity_EventScript_ReceivedBerry
# 39 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BerrySuitsYou, MSGBOX_DEFAULT
# 40 "data/maps/LilycoveCity/scripts.pory"
	giverandomberry BERRY_ID_CHERI, BERRY_ID_SITRUS
# 41 "data/maps/LilycoveCity/scripts.pory"
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
# 42 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_DAILY_LILYCOVE_RECEIVED_BERRY
# 43 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BecauseYoureTrainer, MSGBOX_DEFAULT
# 44 "data/maps/LilycoveCity/scripts.pory"
	release
# 45 "data/maps/LilycoveCity/scripts.pory"
	end
# 46 "data/maps/LilycoveCity/scripts.pory"

# 47 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_ReceivedBerry::
# 48 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_PokeblocksSuitPokemon, MSGBOX_DEFAULT
# 49 "data/maps/LilycoveCity/scripts.pory"
	release
# 50 "data/maps/LilycoveCity/scripts.pory"
	end
# 51 "data/maps/LilycoveCity/scripts.pory"

# 52 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Man3::
# 53 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_ContestHallInTown, MSGBOX_NPC
# 54 "data/maps/LilycoveCity/scripts.pory"
	end
# 55 "data/maps/LilycoveCity/scripts.pory"

# 56 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Girl::
# 57 "data/maps/LilycoveCity/scripts.pory"
	lock
# 58 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 59 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_BADGE07_GET, LilycoveCity_EventScript_GirlAquaGone
# 60 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_StrangeCaveInCove, MSGBOX_DEFAULT
# 61 "data/maps/LilycoveCity/scripts.pory"
	release
# 62 "data/maps/LilycoveCity/scripts.pory"
	end
# 63 "data/maps/LilycoveCity/scripts.pory"

# 64 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_GirlAquaGone::
# 65 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_GoingToMoveDeleterForHMs, MSGBOX_DEFAULT
# 66 "data/maps/LilycoveCity/scripts.pory"
	release
# 67 "data/maps/LilycoveCity/scripts.pory"
	end
# 68 "data/maps/LilycoveCity/scripts.pory"

# 69 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_RichBoy::
# 70 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_ImFromKanto, MSGBOX_NPC
# 71 "data/maps/LilycoveCity/scripts.pory"
	end
# 72 "data/maps/LilycoveCity/scripts.pory"

# 73 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Sailor2::
# 74 "data/maps/LilycoveCity/scripts.pory"
	lock
# 75 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 76 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, LilycoveCity_EventScript_Sailor2AquaGone
# 77 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_TeamAquaBeenTrainingWailmer, MSGBOX_DEFAULT
# 78 "data/maps/LilycoveCity/scripts.pory"
	release
# 79 "data/maps/LilycoveCity/scripts.pory"
	end
# 80 "data/maps/LilycoveCity/scripts.pory"

# 81 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Sailor2AquaGone::
# 82 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_SomeonePuntedTeamAquaOut, MSGBOX_DEFAULT
# 83 "data/maps/LilycoveCity/scripts.pory"
	release
# 84 "data/maps/LilycoveCity/scripts.pory"
	end
# 85 "data/maps/LilycoveCity/scripts.pory"

# 86 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Woman2::
# 87 "data/maps/LilycoveCity/scripts.pory"
	lock
# 88 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 89 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE, LilycoveCity_EventScript_Woman2AquaGone
# 90 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_SomeoneStoleMyPokemon, MSGBOX_DEFAULT
# 91 "data/maps/LilycoveCity/scripts.pory"
	release
# 92 "data/maps/LilycoveCity/scripts.pory"
	end
# 93 "data/maps/LilycoveCity/scripts.pory"

# 94 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Woman2AquaGone::
# 95 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MissingPokemonCameBack, MSGBOX_DEFAULT
# 96 "data/maps/LilycoveCity/scripts.pory"
	release
# 97 "data/maps/LilycoveCity/scripts.pory"
	end
# 98 "data/maps/LilycoveCity/scripts.pory"

# 99 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Man2::
# 100 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_ImArtDealer, MSGBOX_NPC
# 101 "data/maps/LilycoveCity/scripts.pory"
	end
# 102 "data/maps/LilycoveCity/scripts.pory"

# 103 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_ExpertM1::
# 104 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_SeaRemainsForeverYoung, MSGBOX_SIGN
# 105 "data/maps/LilycoveCity/scripts.pory"
	end
# 106 "data/maps/LilycoveCity/scripts.pory"

# 107 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_ExpertF::
# 108 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_SixtyYearsAgoHusbandProposed, MSGBOX_SIGN
# 109 "data/maps/LilycoveCity/scripts.pory"
	end
# 110 "data/maps/LilycoveCity/scripts.pory"

# 111 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_ExpertM2::
# 112 "data/maps/LilycoveCity/scripts.pory"
	lock
# 113 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 114 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_BADGE07_GET, LilycoveCity_EventScript_ExpertM2AquaGone
# 115 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_TeamAquaRenovatedCavern, MSGBOX_DEFAULT
# 116 "data/maps/LilycoveCity/scripts.pory"
	release
# 117 "data/maps/LilycoveCity/scripts.pory"
	end
# 118 "data/maps/LilycoveCity/scripts.pory"

# 119 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_ExpertM2AquaGone::
# 120 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_TeamAquaLotGoneForGood, MSGBOX_DEFAULT
# 121 "data/maps/LilycoveCity/scripts.pory"
	release
# 122 "data/maps/LilycoveCity/scripts.pory"
	end
# 123 "data/maps/LilycoveCity/scripts.pory"

# 124 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Sailor1::
# 125 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_HeardTowerCalledSkyPillar, MSGBOX_NPC
# 126 "data/maps/LilycoveCity/scripts.pory"
	end
# 127 "data/maps/LilycoveCity/scripts.pory"

# 128 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_FatMan::
# 129 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_SawTallTowerOnRoute131, MSGBOX_NPC
# 130 "data/maps/LilycoveCity/scripts.pory"
	end
# 131 "data/maps/LilycoveCity/scripts.pory"

# 132 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Man1::
# 133 "data/maps/LilycoveCity/scripts.pory"
	lockall
# 134 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_JustArrivedAndSawRarePokemon, MSGBOX_NPC
# 135 "data/maps/LilycoveCity/scripts.pory"
	applymovement LOCALID_LILYCOVE_MAN_1, Common_Movement_FaceOriginalDirection
# 136 "data/maps/LilycoveCity/scripts.pory"
	end
# 137 "data/maps/LilycoveCity/scripts.pory"

# 138 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Woman1::
# 139 "data/maps/LilycoveCity/scripts.pory"
	lockall
# 140 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_HoneymoonVowToSeeRarePokemon, MSGBOX_NPC
# 141 "data/maps/LilycoveCity/scripts.pory"
	applymovement LOCALID_LILYCOVE_WOMAN_1, Common_Movement_FaceOriginalDirection
# 142 "data/maps/LilycoveCity/scripts.pory"
	end
# 143 "data/maps/LilycoveCity/scripts.pory"

# 144 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_CitySign::
# 145 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_CitySign, MSGBOX_SIGN
# 146 "data/maps/LilycoveCity/scripts.pory"
	end
# 147 "data/maps/LilycoveCity/scripts.pory"

# 148 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_ContestHallSign::
# 149 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_ContestHallSign, MSGBOX_SIGN
# 150 "data/maps/LilycoveCity/scripts.pory"
	end
# 151 "data/maps/LilycoveCity/scripts.pory"

# 152 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MotelSign::
# 153 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MotelSign, MSGBOX_SIGN
# 154 "data/maps/LilycoveCity/scripts.pory"
	end
# 155 "data/maps/LilycoveCity/scripts.pory"

# 156 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MuseumSign::
# 157 "data/maps/LilycoveCity/scripts.pory"
	lockall
# 158 "data/maps/LilycoveCity/scripts.pory"
	specialvar VAR_0x8004, CountPlayerMuseumPaintings
# 159 "data/maps/LilycoveCity/scripts.pory"
	switch VAR_0x8004
# 160 "data/maps/LilycoveCity/scripts.pory"
	case 0, LilycoveCity_EventScript_MuseumSignNoPaintings
# 161 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MuseumSignPlayersExhibit, MSGBOX_DEFAULT
# 162 "data/maps/LilycoveCity/scripts.pory"
	releaseall
# 163 "data/maps/LilycoveCity/scripts.pory"
	end
# 164 "data/maps/LilycoveCity/scripts.pory"

# 165 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MuseumSignNoPaintings::
# 166 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MuseumSign, MSGBOX_DEFAULT
# 167 "data/maps/LilycoveCity/scripts.pory"
	releaseall
# 168 "data/maps/LilycoveCity/scripts.pory"
	end
# 169 "data/maps/LilycoveCity/scripts.pory"

# 170 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_HarborSign::
# 171 "data/maps/LilycoveCity/scripts.pory"
	lockall
# 172 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_HarborSignFerryReady
# 173 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_HarborSignUnderConstruction, MSGBOX_DEFAULT
# 174 "data/maps/LilycoveCity/scripts.pory"
	releaseall
# 175 "data/maps/LilycoveCity/scripts.pory"
	end
# 176 "data/maps/LilycoveCity/scripts.pory"

# 177 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_HarborSignFerryReady::
# 178 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_HarborSign, MSGBOX_DEFAULT
# 179 "data/maps/LilycoveCity/scripts.pory"
	releaseall
# 180 "data/maps/LilycoveCity/scripts.pory"
	end
# 181 "data/maps/LilycoveCity/scripts.pory"

# 182 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_TrainerFanClubSign::
# 183 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_TrainerFanClubSign, MSGBOX_SIGN
# 184 "data/maps/LilycoveCity/scripts.pory"
	end
# 185 "data/maps/LilycoveCity/scripts.pory"

# 186 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_DepartmentStoreSign::
# 187 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_DepartmentStoreSign, MSGBOX_SIGN
# 188 "data/maps/LilycoveCity/scripts.pory"
	end
# 189 "data/maps/LilycoveCity/scripts.pory"

# 190 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MoveDeletersHouseSign::
# 191 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MoveDeletersHouseSign, MSGBOX_SIGN
# 192 "data/maps/LilycoveCity/scripts.pory"
	end
# 193 "data/maps/LilycoveCity/scripts.pory"

# 194 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_WailmerTrainerGrunt::
# 195 "data/maps/LilycoveCity/scripts.pory"
	lockall
# 196 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_MET_WAILMER_TRAINER, LilycoveCity_EventScript_MetWailmerTrainer
# 197 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_WailmerLeapOutOfWater, MSGBOX_DEFAULT
# 198 "data/maps/LilycoveCity/scripts.pory"
	applymovement VAR_LAST_TALKED, Common_Movement_FacePlayer
# 199 "data/maps/LilycoveCity/scripts.pory"
	waitmovement 0
# 200 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_GetLostMessingUpTraining, MSGBOX_DEFAULT
# 201 "data/maps/LilycoveCity/scripts.pory"
	applymovement VAR_LAST_TALKED, Common_Movement_FaceOriginalDirection
# 202 "data/maps/LilycoveCity/scripts.pory"
	waitmovement 0
# 203 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_MET_WAILMER_TRAINER
# 204 "data/maps/LilycoveCity/scripts.pory"
	releaseall
# 205 "data/maps/LilycoveCity/scripts.pory"
	end
# 206 "data/maps/LilycoveCity/scripts.pory"

# 207 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MetWailmerTrainer::
# 208 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_WailmerLeapOutOfWater, MSGBOX_DEFAULT
# 209 "data/maps/LilycoveCity/scripts.pory"
	releaseall
# 210 "data/maps/LilycoveCity/scripts.pory"
	end
# 211 "data/maps/LilycoveCity/scripts.pory"

# 212 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_AquaGrunt1::
# 213 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MovedLootIntoHideoutToday, MSGBOX_NPC
# 214 "data/maps/LilycoveCity/scripts.pory"
	end
# 215 "data/maps/LilycoveCity/scripts.pory"

# 216 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_AquaGrunt2::
# 217 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_ChanceToDoBigThings, MSGBOX_NPC
# 218 "data/maps/LilycoveCity/scripts.pory"
	end
# 219 "data/maps/LilycoveCity/scripts.pory"

# 220 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_AquaGrunt3::
# 221 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_DontGoNearCaveInCove, MSGBOX_NPC
# 222 "data/maps/LilycoveCity/scripts.pory"
	end
# 223 "data/maps/LilycoveCity/scripts.pory"

# 224 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_AquaGrunt4::
# 225 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_IfWorldBecomesOurs, MSGBOX_NPC
# 226 "data/maps/LilycoveCity/scripts.pory"
	end
# 227 "data/maps/LilycoveCity/scripts.pory"

# 228 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Rival::
# 229 "data/maps/LilycoveCity/scripts.pory"
	lock
# 230 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 231 "data/maps/LilycoveCity/scripts.pory"
	checkplayergender
# 232 "data/maps/LilycoveCity/scripts.pory"
	goto_if_eq VAR_RESULT, MALE, LilycoveCity_EventScript_May
# 233 "data/maps/LilycoveCity/scripts.pory"
	goto_if_eq VAR_RESULT, FEMALE, LilycoveCity_EventScript_Brendan
# 234 "data/maps/LilycoveCity/scripts.pory"
	end
# 235 "data/maps/LilycoveCity/scripts.pory"

# 236 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_May::
# 237 "data/maps/LilycoveCity/scripts.pory"
	playbgm MUS_ENCOUNTER_MAY, TRUE
# 238 "data/maps/LilycoveCity/scripts.pory"
	call_if_set FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_MayAskToBattleAgain
# 239 "data/maps/LilycoveCity/scripts.pory"
	call_if_unset FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_MayAskToBattle
# 240 "data/maps/LilycoveCity/scripts.pory"
	goto_if_eq VAR_RESULT, NO, LilycoveCity_EventScript_DeclineMayBattle
# 241 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayWontBeBeaten, MSGBOX_DEFAULT
# 242 "data/maps/LilycoveCity/scripts.pory"
	switch VAR_STARTER_MON
# 243 "data/maps/LilycoveCity/scripts.pory"
	case 0, LilycoveCity_EventScript_BattleMayTreecko
# 244 "data/maps/LilycoveCity/scripts.pory"
	case 1, LilycoveCity_EventScript_BattleMayTorchic
# 245 "data/maps/LilycoveCity/scripts.pory"
	case 2, LilycoveCity_EventScript_BattleMayMudkip
# 246 "data/maps/LilycoveCity/scripts.pory"
	end
# 247 "data/maps/LilycoveCity/scripts.pory"

# 248 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MayAskToBattleAgain::
# 249 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayBattleMe, MSGBOX_YESNO
# 250 "data/maps/LilycoveCity/scripts.pory"
	return
# 251 "data/maps/LilycoveCity/scripts.pory"

# 252 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MayAskToBattle::
# 253 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayShoppingLetsBattle, MSGBOX_YESNO
# 254 "data/maps/LilycoveCity/scripts.pory"
	return
# 255 "data/maps/LilycoveCity/scripts.pory"

# 256 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_DeclineMayBattle::
# 257 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE
# 258 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayNotRaisingPokemon, MSGBOX_DEFAULT
# 259 "data/maps/LilycoveCity/scripts.pory"
	savebgm MUS_DUMMY
# 260 "data/maps/LilycoveCity/scripts.pory"
	fadedefaultbgm
# 261 "data/maps/LilycoveCity/scripts.pory"
	release
# 262 "data/maps/LilycoveCity/scripts.pory"
	end
# 263 "data/maps/LilycoveCity/scripts.pory"

# 264 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_Brendan::
# 265 "data/maps/LilycoveCity/scripts.pory"
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
# 266 "data/maps/LilycoveCity/scripts.pory"
	call_if_set FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_BrendanAskToBattleAgain
# 267 "data/maps/LilycoveCity/scripts.pory"
	call_if_unset FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE, LilycoveCity_EventScript_BrendanAskToBattle
# 268 "data/maps/LilycoveCity/scripts.pory"
	goto_if_eq VAR_RESULT, NO, LilycoveCity_EventScript_DeclineBrendanBattle
# 269 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanWontBeBeaten, MSGBOX_DEFAULT
# 270 "data/maps/LilycoveCity/scripts.pory"
	switch VAR_STARTER_MON
# 271 "data/maps/LilycoveCity/scripts.pory"
	case 0, LilycoveCity_EventScript_BattleBrendanTreecko
# 272 "data/maps/LilycoveCity/scripts.pory"
	case 1, LilycoveCity_EventScript_BattleBrendanTorchic
# 273 "data/maps/LilycoveCity/scripts.pory"
	case 2, LilycoveCity_EventScript_BattleBrendanMudkip
# 274 "data/maps/LilycoveCity/scripts.pory"
	end
# 275 "data/maps/LilycoveCity/scripts.pory"

# 276 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BrendanAskToBattleAgain::
# 277 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanBattleMe, MSGBOX_YESNO
# 278 "data/maps/LilycoveCity/scripts.pory"
	return
# 279 "data/maps/LilycoveCity/scripts.pory"

# 280 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BrendanAskToBattle::
# 281 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanShoppingLetsBattle, MSGBOX_YESNO
# 282 "data/maps/LilycoveCity/scripts.pory"
	return
# 283 "data/maps/LilycoveCity/scripts.pory"

# 284 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_DeclineBrendanBattle::
# 285 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE
# 286 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanNoConfidence, MSGBOX_DEFAULT
# 287 "data/maps/LilycoveCity/scripts.pory"
	savebgm MUS_DUMMY
# 288 "data/maps/LilycoveCity/scripts.pory"
	fadedefaultbgm
# 289 "data/maps/LilycoveCity/scripts.pory"
	release
# 290 "data/maps/LilycoveCity/scripts.pory"
	end
# 291 "data/maps/LilycoveCity/scripts.pory"

# 292 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BattleMayTreecko::
# 293 "data/maps/LilycoveCity/scripts.pory"
	trainerbattle_no_intro TRAINER_MAY_LILYCOVE_TREECKO, LilycoveCity_Text_MayDefeat
# 294 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_DefeatedMay
# 295 "data/maps/LilycoveCity/scripts.pory"
	end
# 296 "data/maps/LilycoveCity/scripts.pory"

# 297 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BattleMayTorchic::
# 298 "data/maps/LilycoveCity/scripts.pory"
	trainerbattle_no_intro TRAINER_MAY_LILYCOVE_TORCHIC, LilycoveCity_Text_MayDefeat
# 299 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_DefeatedMay
# 300 "data/maps/LilycoveCity/scripts.pory"
	end
# 301 "data/maps/LilycoveCity/scripts.pory"

# 302 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BattleMayMudkip::
# 303 "data/maps/LilycoveCity/scripts.pory"
	trainerbattle_no_intro TRAINER_MAY_LILYCOVE_MUDKIP, LilycoveCity_Text_MayDefeat
# 304 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_DefeatedMay
# 305 "data/maps/LilycoveCity/scripts.pory"
	end
# 306 "data/maps/LilycoveCity/scripts.pory"

# 307 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BattleBrendanTreecko::
# 308 "data/maps/LilycoveCity/scripts.pory"
	trainerbattle_no_intro TRAINER_BRENDAN_LILYCOVE_TREECKO, LilycoveCity_Text_BrendanDefeat
# 309 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_DefeatedBrendan
# 310 "data/maps/LilycoveCity/scripts.pory"
	end
# 311 "data/maps/LilycoveCity/scripts.pory"

# 312 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BattleBrendanTorchic::
# 313 "data/maps/LilycoveCity/scripts.pory"
	trainerbattle_no_intro TRAINER_BRENDAN_LILYCOVE_TORCHIC, LilycoveCity_Text_BrendanDefeat
# 314 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_DefeatedBrendan
# 315 "data/maps/LilycoveCity/scripts.pory"
	end
# 316 "data/maps/LilycoveCity/scripts.pory"

# 317 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BattleBrendanMudkip::
# 318 "data/maps/LilycoveCity/scripts.pory"
	trainerbattle_no_intro TRAINER_BRENDAN_LILYCOVE_MUDKIP, LilycoveCity_Text_BrendanDefeat
# 319 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_DefeatedBrendan
# 320 "data/maps/LilycoveCity/scripts.pory"
	end
# 321 "data/maps/LilycoveCity/scripts.pory"

# 322 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_DefeatedMay::
# 323 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayGoingBackToLittleroot, MSGBOX_DEFAULT
# 324 "data/maps/LilycoveCity/scripts.pory"
	setvar VAR_RESULT, FALSE
# 325 "data/maps/LilycoveCity/scripts.pory"
	call_if_set FLAG_BADGE06_GET, LilycoveCity_EventScript_CheckFinalBadge
# 326 "data/maps/LilycoveCity/scripts.pory"
	call_if_eq VAR_RESULT, FALSE, LilycoveCity_EventScript_MayCollectBadges
# 327 "data/maps/LilycoveCity/scripts.pory"
	call_if_eq VAR_RESULT, TRUE, LilycoveCity_EventScript_MayPokemonLeague
# 328 "data/maps/LilycoveCity/scripts.pory"
	clearflag FLAG_HIDE_TOSA_PORT_MAYS_HOUSE_RIVAL_BEDROOM
# 329 "data/maps/LilycoveCity/scripts.pory"
	clearflag FLAG_HIDE_TOSA_PORT_MAYS_HOUSE_2F_PICHU_DOLL
# 330 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_RivalFlyAway
# 331 "data/maps/LilycoveCity/scripts.pory"
	end
# 332 "data/maps/LilycoveCity/scripts.pory"

# 333 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_CheckFinalBadge::
# 334 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_BADGE08_GET, LilycoveCity_EventScript_HasFinalBadge
# 335 "data/maps/LilycoveCity/scripts.pory"
	return
# 336 "data/maps/LilycoveCity/scripts.pory"

# 337 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_HasFinalBadge::
# 338 "data/maps/LilycoveCity/scripts.pory"
	setvar VAR_RESULT, TRUE
# 339 "data/maps/LilycoveCity/scripts.pory"
	return
# 340 "data/maps/LilycoveCity/scripts.pory"

# 341 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MayCollectBadges::
# 342 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayYouGoingToCollectBadges, MSGBOX_DEFAULT
# 343 "data/maps/LilycoveCity/scripts.pory"
	return
# 344 "data/maps/LilycoveCity/scripts.pory"

# 345 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MayPokemonLeague::
# 346 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_MayBattleFrontier
# 347 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayYouGoingToPokemonLeague, MSGBOX_DEFAULT
# 348 "data/maps/LilycoveCity/scripts.pory"
	return
# 349 "data/maps/LilycoveCity/scripts.pory"

# 350 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_MayBattleFrontier::
# 351 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_MayYouGoingToBattleFrontier, MSGBOX_DEFAULT
# 352 "data/maps/LilycoveCity/scripts.pory"
	return
# 353 "data/maps/LilycoveCity/scripts.pory"

# 354 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_DefeatedBrendan::
# 355 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanGoingBackToLittleroot, MSGBOX_DEFAULT
# 356 "data/maps/LilycoveCity/scripts.pory"
	setvar VAR_RESULT, FALSE
# 357 "data/maps/LilycoveCity/scripts.pory"
	call_if_set FLAG_BADGE06_GET, LilycoveCity_EventScript_CheckFinalBadge
# 358 "data/maps/LilycoveCity/scripts.pory"
	call_if_eq VAR_RESULT, FALSE, LilycoveCity_EventScript_BrendanCollectBadges
# 359 "data/maps/LilycoveCity/scripts.pory"
	call_if_eq VAR_RESULT, TRUE, LilycoveCity_EventScript_BrendanPokemonLeague
# 360 "data/maps/LilycoveCity/scripts.pory"
	clearflag FLAG_HIDE_TOSA_PORT_BRENDANS_HOUSE_RIVAL_BEDROOM
# 361 "data/maps/LilycoveCity/scripts.pory"
	clearflag FLAG_HIDE_TOSA_PORT_BRENDANS_HOUSE_2F_SWABLU_DOLL
# 362 "data/maps/LilycoveCity/scripts.pory"
	goto LilycoveCity_EventScript_RivalFlyAway
# 363 "data/maps/LilycoveCity/scripts.pory"
	end
# 364 "data/maps/LilycoveCity/scripts.pory"

# 365 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BrendanCollectBadges::
# 366 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanYouGoingToCollectBadges, MSGBOX_DEFAULT
# 367 "data/maps/LilycoveCity/scripts.pory"
	return
# 368 "data/maps/LilycoveCity/scripts.pory"

# 369 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BrendanPokemonLeague::
# 370 "data/maps/LilycoveCity/scripts.pory"
	goto_if_set FLAG_SYS_GAME_CLEAR, LilycoveCity_EventScript_BrendanBattleFrontier
# 371 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanYouGoingToPokemonLeague, MSGBOX_DEFAULT
# 372 "data/maps/LilycoveCity/scripts.pory"
	return
# 373 "data/maps/LilycoveCity/scripts.pory"

# 374 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_BrendanBattleFrontier::
# 375 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_BrendanYouGoingToBattleFrontier, MSGBOX_DEFAULT
# 376 "data/maps/LilycoveCity/scripts.pory"
	return
# 377 "data/maps/LilycoveCity/scripts.pory"

# 378 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_RivalFlyAway::
# 379 "data/maps/LilycoveCity/scripts.pory"
	closemessage
# 380 "data/maps/LilycoveCity/scripts.pory"
	applymovement VAR_LAST_TALKED, Common_Movement_WalkInPlaceFasterDown
# 381 "data/maps/LilycoveCity/scripts.pory"
	waitmovement 0
# 382 "data/maps/LilycoveCity/scripts.pory"
	delay 50
# 383 "data/maps/LilycoveCity/scripts.pory"
	setfieldeffectargument 0, 1
# 384 "data/maps/LilycoveCity/scripts.pory"
	dofieldeffect FLDEFF_NPCFLY_OUT
# 385 "data/maps/LilycoveCity/scripts.pory"
	delay 15
# 386 "data/maps/LilycoveCity/scripts.pory"
	removeobject VAR_LAST_TALKED
# 387 "data/maps/LilycoveCity/scripts.pory"
	waitfieldeffect FLDEFF_NPCFLY_OUT
# 388 "data/maps/LilycoveCity/scripts.pory"
	savebgm MUS_DUMMY
# 389 "data/maps/LilycoveCity/scripts.pory"
	fadedefaultbgm
# 390 "data/maps/LilycoveCity/scripts.pory"
	setflag FLAG_MET_RIVAL_LILYCOVE
# 391 "data/maps/LilycoveCity/scripts.pory"
	release
# 392 "data/maps/LilycoveCity/scripts.pory"
	end
# 393 "data/maps/LilycoveCity/scripts.pory"

# 394 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_SchoolKidM::
# 395 "data/maps/LilycoveCity/scripts.pory"
	lock
# 396 "data/maps/LilycoveCity/scripts.pory"
	faceplayer
# 397 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_DoYouKnowAboutBerryBlender, MSGBOX_YESNO
# 398 "data/maps/LilycoveCity/scripts.pory"
	call_if_eq VAR_RESULT, YES, LilycoveCity_EventScript_KnowAboutBerryBlender
# 399 "data/maps/LilycoveCity/scripts.pory"
	call_if_eq VAR_RESULT, NO, LilycoveCity_EventScript_DontKnowAboutBerryBlender
# 400 "data/maps/LilycoveCity/scripts.pory"
	release
# 401 "data/maps/LilycoveCity/scripts.pory"
	end
# 402 "data/maps/LilycoveCity/scripts.pory"

# 403 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_KnowAboutBerryBlender::
# 404 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_FasterSpinBetterPokeblocks, MSGBOX_DEFAULT
# 405 "data/maps/LilycoveCity/scripts.pory"
	return
# 406 "data/maps/LilycoveCity/scripts.pory"

# 407 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_EventScript_DontKnowAboutBerryBlender::
# 408 "data/maps/LilycoveCity/scripts.pory"
	msgbox LilycoveCity_Text_ExplainBerryBlender, MSGBOX_DEFAULT
# 409 "data/maps/LilycoveCity/scripts.pory"
	return
# 410 "data/maps/LilycoveCity/scripts.pory"

# 411 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayShoppingLetsBattle:
# 412 "data/maps/LilycoveCity/scripts.pory"
	.string "MAY: Oh, hey?\n"
# 413 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}{KUN}, are you shopping, too?\p"
# 414 "data/maps/LilycoveCity/scripts.pory"
	.string "I bought a whole bunch of DOLLS and\n"
# 415 "data/maps/LilycoveCity/scripts.pory"
	.string "POSTERS.\p"
# 416 "data/maps/LilycoveCity/scripts.pory"
	.string "Of course, I've also caught a lot of\n"
# 417 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéMON, and I'm raising them\l"
# 418 "data/maps/LilycoveCity/scripts.pory"
	.string "properly, too.\p"
# 419 "data/maps/LilycoveCity/scripts.pory"
	.string "Actually, I'm more worried if you're\n"
# 420 "data/maps/LilycoveCity/scripts.pory"
	.string "raising POKéMON properly, {PLAYER}{KUN}.\p"
# 421 "data/maps/LilycoveCity/scripts.pory"
	.string "I'll battle with you, so you can show\n"
# 422 "data/maps/LilycoveCity/scripts.pory"
	.string "me your POKéMON, {PLAYER}{KUN}.$"
# 423 "data/maps/LilycoveCity/scripts.pory"

# 424 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayNotRaisingPokemon:
# 425 "data/maps/LilycoveCity/scripts.pory"
	.string "MAY: Oh, why? {PLAYER}{KUN}, haven't you\n"
# 426 "data/maps/LilycoveCity/scripts.pory"
	.string "been raising your POKéMON?\p"
# 427 "data/maps/LilycoveCity/scripts.pory"
	.string "That's not a very good showing as a\n"
# 428 "data/maps/LilycoveCity/scripts.pory"
	.string "TRAINER…$"
# 429 "data/maps/LilycoveCity/scripts.pory"

# 430 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayBattleMe:
# 431 "data/maps/LilycoveCity/scripts.pory"
	.string "MAY: Come on, battle with me, so I can\n"
# 432 "data/maps/LilycoveCity/scripts.pory"
	.string "check out your POKéMON!$"
# 433 "data/maps/LilycoveCity/scripts.pory"

# 434 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayWontBeBeaten:
# 435 "data/maps/LilycoveCity/scripts.pory"
	.string "MAY: The POKéMON I raised won't be\n"
# 436 "data/maps/LilycoveCity/scripts.pory"
	.string "beaten by your POKéMON, {PLAYER}{KUN}!$"
# 437 "data/maps/LilycoveCity/scripts.pory"

# 438 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayDefeat:
# 439 "data/maps/LilycoveCity/scripts.pory"
	.string "… … … … … … … …\p"
# 440 "data/maps/LilycoveCity/scripts.pory"
	.string "I remember the battle I had with you,\n"
# 441 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}{KUN}, on ROUTE 103.\p"
# 442 "data/maps/LilycoveCity/scripts.pory"
	.string "That battle helped you become this\n"
# 443 "data/maps/LilycoveCity/scripts.pory"
	.string "strong, {PLAYER}{KUN}, didn't it?$"
# 444 "data/maps/LilycoveCity/scripts.pory"

# 445 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayGoingBackToLittleroot:
# 446 "data/maps/LilycoveCity/scripts.pory"
	.string "MAY: I'm thinking of going back to\n"
# 447 "data/maps/LilycoveCity/scripts.pory"
	.string "LITTLEROOT soon.\p"
# 448 "data/maps/LilycoveCity/scripts.pory"
	.string "I've caught a decent group of POKéMON,\n"
# 449 "data/maps/LilycoveCity/scripts.pory"
	.string "and my POKéDEX is coming along, so\l"
# 450 "data/maps/LilycoveCity/scripts.pory"
	.string "I'm going home to show my dad.$"
# 451 "data/maps/LilycoveCity/scripts.pory"

# 452 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayYouGoingToCollectBadges:
# 453 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}{KUN}, what are you going to do?\p"
# 454 "data/maps/LilycoveCity/scripts.pory"
	.string "Collect all the GYM BADGES and take\n"
# 455 "data/maps/LilycoveCity/scripts.pory"
	.string "the POKéMON LEAGUE challenge?\p"
# 456 "data/maps/LilycoveCity/scripts.pory"
	.string "Well, while you're collecting BADGES,\n"
# 457 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}{KUN}, I'm going to work on my\l"
# 458 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéDEX. I'll complete it before you!\p"
# 459 "data/maps/LilycoveCity/scripts.pory"
	.string "See you!$"
# 460 "data/maps/LilycoveCity/scripts.pory"

# 461 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayYouGoingToPokemonLeague:
# 462 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}{KUN}, what are you going to do?\p"
# 463 "data/maps/LilycoveCity/scripts.pory"
	.string "Are you taking the POKéMON LEAGUE\n"
# 464 "data/maps/LilycoveCity/scripts.pory"
	.string "challenge?\p"
# 465 "data/maps/LilycoveCity/scripts.pory"
	.string "Or, are you going to complete your\n"
# 466 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéDEX?\p"
# 467 "data/maps/LilycoveCity/scripts.pory"
	.string "I might've lost to you in battling,\n"
# 468 "data/maps/LilycoveCity/scripts.pory"
	.string "but I'll finish my POKéDEX before you!\p"
# 469 "data/maps/LilycoveCity/scripts.pory"
	.string "See you!$"
# 470 "data/maps/LilycoveCity/scripts.pory"

# 471 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MayYouGoingToBattleFrontier:
# 472 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}{KUN}, what are you going to do?\p"
# 473 "data/maps/LilycoveCity/scripts.pory"
	.string "Are you taking the BATTLE FRONTIER\n"
# 474 "data/maps/LilycoveCity/scripts.pory"
	.string "challenge?\p"
# 475 "data/maps/LilycoveCity/scripts.pory"
	.string "Or, are you going to complete your\n"
# 476 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéDEX?\p"
# 477 "data/maps/LilycoveCity/scripts.pory"
	.string "I might've lost to you in battling,\n"
# 478 "data/maps/LilycoveCity/scripts.pory"
	.string "but I'll finish my POKéDEX before you!\p"
# 479 "data/maps/LilycoveCity/scripts.pory"
	.string "See you!$"
# 480 "data/maps/LilycoveCity/scripts.pory"

# 481 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanShoppingLetsBattle:
# 482 "data/maps/LilycoveCity/scripts.pory"
	.string "BRENDAN: Oh, hey, it's {PLAYER}.\p"
# 483 "data/maps/LilycoveCity/scripts.pory"
	.string "I'm running an errand for my dad.\n"
# 484 "data/maps/LilycoveCity/scripts.pory"
	.string "No, I'm not buying any DOLLS.\p"
# 485 "data/maps/LilycoveCity/scripts.pory"
	.string "Anyways, it's been a while.\p"
# 486 "data/maps/LilycoveCity/scripts.pory"
	.string "Want to have a battle to see who's been\n"
# 487 "data/maps/LilycoveCity/scripts.pory"
	.string "raising POKéMON better?$"
# 488 "data/maps/LilycoveCity/scripts.pory"

# 489 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanNoConfidence:
# 490 "data/maps/LilycoveCity/scripts.pory"
	.string "BRENDAN: Oh, what's the matter?\n"
# 491 "data/maps/LilycoveCity/scripts.pory"
	.string "Don't have the confidence?$"
# 492 "data/maps/LilycoveCity/scripts.pory"

# 493 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanBattleMe:
# 494 "data/maps/LilycoveCity/scripts.pory"
	.string "BRENDAN: Want to battle to see who's\n"
# 495 "data/maps/LilycoveCity/scripts.pory"
	.string "been raising POKéMON better?$"
# 496 "data/maps/LilycoveCity/scripts.pory"

# 497 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanWontBeBeaten:
# 498 "data/maps/LilycoveCity/scripts.pory"
	.string "BRENDAN: Aww, but you know I'm not\n"
# 499 "data/maps/LilycoveCity/scripts.pory"
	.string "going to lose to no {PLAYER}.$"
# 500 "data/maps/LilycoveCity/scripts.pory"

# 501 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanDefeat:
# 502 "data/maps/LilycoveCity/scripts.pory"
	.string "Humph…\n"
# 503 "data/maps/LilycoveCity/scripts.pory"
	.string "You've done a lot of raising.\p"
# 504 "data/maps/LilycoveCity/scripts.pory"
	.string "That stings a bit--I had a head start\n"
# 505 "data/maps/LilycoveCity/scripts.pory"
	.string "on you as a TRAINER…$"
# 506 "data/maps/LilycoveCity/scripts.pory"

# 507 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanGoingBackToLittleroot:
# 508 "data/maps/LilycoveCity/scripts.pory"
	.string "BRENDAN: I…\n"
# 509 "data/maps/LilycoveCity/scripts.pory"
	.string "I plan on going home to LITTLEROOT.\p"
# 510 "data/maps/LilycoveCity/scripts.pory"
	.string "You know I'm helping out my dad on his\n"
# 511 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéDEX. It's coming together pretty\l"
# 512 "data/maps/LilycoveCity/scripts.pory"
	.string "decently, so I should go show him.$"
# 513 "data/maps/LilycoveCity/scripts.pory"

# 514 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanYouGoingToCollectBadges:
# 515 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}, what are you going to do?\p"
# 516 "data/maps/LilycoveCity/scripts.pory"
	.string "Collect all the GYM BADGES and take\n"
# 517 "data/maps/LilycoveCity/scripts.pory"
	.string "the POKéMON LEAGUE challenge?\p"
# 518 "data/maps/LilycoveCity/scripts.pory"
	.string "Maybe I'll do that, too…\p"
# 519 "data/maps/LilycoveCity/scripts.pory"
	.string "Well, anyway, hang in there!$"
# 520 "data/maps/LilycoveCity/scripts.pory"

# 521 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanYouGoingToPokemonLeague:
# 522 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}, what are you going to do?\p"
# 523 "data/maps/LilycoveCity/scripts.pory"
	.string "Since you're that strong, are you\n"
# 524 "data/maps/LilycoveCity/scripts.pory"
	.string "taking the POKéMON LEAGUE challenge?\p"
# 525 "data/maps/LilycoveCity/scripts.pory"
	.string "Heh, even me--if I trained my POKéMON\n"
# 526 "data/maps/LilycoveCity/scripts.pory"
	.string "a bit more, I should be stronger than\l"
# 527 "data/maps/LilycoveCity/scripts.pory"
	.string "you, {PLAYER}.\p"
# 528 "data/maps/LilycoveCity/scripts.pory"
	.string "Well, anyway, hang in there!$"
# 529 "data/maps/LilycoveCity/scripts.pory"

# 530 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_BrendanYouGoingToBattleFrontier:
# 531 "data/maps/LilycoveCity/scripts.pory"
	.string "{PLAYER}, what are you going to do?\p"
# 532 "data/maps/LilycoveCity/scripts.pory"
	.string "Are you taking the BATTLE FRONTIER\n"
# 533 "data/maps/LilycoveCity/scripts.pory"
	.string "challenge?\p"
# 534 "data/maps/LilycoveCity/scripts.pory"
	.string "Or, are you going to complete your\n"
# 535 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéDEX?\p"
# 536 "data/maps/LilycoveCity/scripts.pory"
	.string "Since you're that strong, you should\n"
# 537 "data/maps/LilycoveCity/scripts.pory"
	.string "consider the BATTLE FRONTIER.\p"
# 538 "data/maps/LilycoveCity/scripts.pory"
	.string "Heh, if I train my POKéMON a bit more,\n"
# 539 "data/maps/LilycoveCity/scripts.pory"
	.string "I'll get stronger than you, {PLAYER}.\p"
# 540 "data/maps/LilycoveCity/scripts.pory"
	.string "Maybe I should go to the BATTLE\n"
# 541 "data/maps/LilycoveCity/scripts.pory"
	.string "FRONTIER.\p"
# 542 "data/maps/LilycoveCity/scripts.pory"
	.string "Well, anyway, hang in there!$"
# 543 "data/maps/LilycoveCity/scripts.pory"

# 544 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MovedLootIntoHideoutToday:
# 545 "data/maps/LilycoveCity/scripts.pory"
	.string "Fufufu…\p"
# 546 "data/maps/LilycoveCity/scripts.pory"
	.string "We moved more loot into our secret\n"
# 547 "data/maps/LilycoveCity/scripts.pory"
	.string "HIDEOUT today…\p"
# 548 "data/maps/LilycoveCity/scripts.pory"
	.string "Wh-who are you?!\n"
# 549 "data/maps/LilycoveCity/scripts.pory"
	.string "I was just talking to myself!$"
# 550 "data/maps/LilycoveCity/scripts.pory"

# 551 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_ChanceToDoBigThings:
# 552 "data/maps/LilycoveCity/scripts.pory"
	.string "I'm just a GRUNT, so I don't know what\n"
# 553 "data/maps/LilycoveCity/scripts.pory"
	.string "the BOSS is thinking…\p"
# 554 "data/maps/LilycoveCity/scripts.pory"
	.string "But being on TEAM AQUA, I know I'll get\n"
# 555 "data/maps/LilycoveCity/scripts.pory"
	.string "the chance to do big things!\p"
# 556 "data/maps/LilycoveCity/scripts.pory"
	.string "Wh-who are you?!\n"
# 557 "data/maps/LilycoveCity/scripts.pory"
	.string "I was just talking to myself!$"
# 558 "data/maps/LilycoveCity/scripts.pory"

# 559 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_DontGoNearCaveInCove:
# 560 "data/maps/LilycoveCity/scripts.pory"
	.string "Hey, you!\p"
# 561 "data/maps/LilycoveCity/scripts.pory"
	.string "Don't go near the cave in the cove!\p"
# 562 "data/maps/LilycoveCity/scripts.pory"
	.string "Why? You don't need a reason why!\n"
# 563 "data/maps/LilycoveCity/scripts.pory"
	.string "I'm an adult, so you just listen to me!$"
# 564 "data/maps/LilycoveCity/scripts.pory"

# 565 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_IfWorldBecomesOurs:
# 566 "data/maps/LilycoveCity/scripts.pory"
	.string "If this whole wide world becomes ours,\n"
# 567 "data/maps/LilycoveCity/scripts.pory"
	.string "TEAM AQUA's, it will be a happier\l"
# 568 "data/maps/LilycoveCity/scripts.pory"
	.string "place for POKéMON, too.$"
# 569 "data/maps/LilycoveCity/scripts.pory"

# 570 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_WailmerLeapOutOfWater:
# 571 "data/maps/LilycoveCity/scripts.pory"
	.string "There! WAILMER!\n"
# 572 "data/maps/LilycoveCity/scripts.pory"
	.string "Leap out of the water now!$"
# 573 "data/maps/LilycoveCity/scripts.pory"

# 574 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_GetLostMessingUpTraining:
# 575 "data/maps/LilycoveCity/scripts.pory"
	.string "Hunh? What do you want?\p"
# 576 "data/maps/LilycoveCity/scripts.pory"
	.string "You're messing up our training,\n"
# 577 "data/maps/LilycoveCity/scripts.pory"
	.string "so can you, like, get lost?$"
# 578 "data/maps/LilycoveCity/scripts.pory"

# 579 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_ContestHallInTown:
# 580 "data/maps/LilycoveCity/scripts.pory"
	.string "There's a POKéMON CONTEST HALL\n"
# 581 "data/maps/LilycoveCity/scripts.pory"
	.string "right in this here town. \p"
# 582 "data/maps/LilycoveCity/scripts.pory"
	.string "That means well-raised POKéMON will\n"
# 583 "data/maps/LilycoveCity/scripts.pory"
	.string "come from all over the country.\p"
# 584 "data/maps/LilycoveCity/scripts.pory"
	.string "My heart swells with excitement!$"
# 585 "data/maps/LilycoveCity/scripts.pory"

# 586 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_StrangeCaveInCove:
# 587 "data/maps/LilycoveCity/scripts.pory"
	.string "Have you seen that strange cave in\n"
# 588 "data/maps/LilycoveCity/scripts.pory"
	.string "the cove at the edge of town?$"
# 589 "data/maps/LilycoveCity/scripts.pory"

# 590 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_GoingToMoveDeleterForHMs:
# 591 "data/maps/LilycoveCity/scripts.pory"
	.string "I'm going to teach my POKéMON some new\n"
# 592 "data/maps/LilycoveCity/scripts.pory"
	.string "moves for entering a CONTEST.\p"
# 593 "data/maps/LilycoveCity/scripts.pory"
	.string "So, I'm going to see the MOVE DELETER\n"
# 594 "data/maps/LilycoveCity/scripts.pory"
	.string "and make it forget HM moves.$"
# 595 "data/maps/LilycoveCity/scripts.pory"

# 596 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_ImFromKanto:
# 597 "data/maps/LilycoveCity/scripts.pory"
	.string "I came from KANTO.\p"
# 598 "data/maps/LilycoveCity/scripts.pory"
	.string "The HOENN region is beautiful with\n"
# 599 "data/maps/LilycoveCity/scripts.pory"
	.string "all its water and verdant nature.\p"
# 600 "data/maps/LilycoveCity/scripts.pory"
	.string "Hunh? Wait a second…\p"
# 601 "data/maps/LilycoveCity/scripts.pory"
	.string "Could there be rare POKéMON that live\n"
# 602 "data/maps/LilycoveCity/scripts.pory"
	.string "only in this area?$"
# 603 "data/maps/LilycoveCity/scripts.pory"

# 604 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_TeamAquaBeenTrainingWailmer:
# 605 "data/maps/LilycoveCity/scripts.pory"
	.string "TEAM AQUA's been training their\n"
# 606 "data/maps/LilycoveCity/scripts.pory"
	.string "WAILMER in the cove.\p"
# 607 "data/maps/LilycoveCity/scripts.pory"
	.string "We SAILORS can't get our boats out\n"
# 608 "data/maps/LilycoveCity/scripts.pory"
	.string "to sea with them in the way!$"
# 609 "data/maps/LilycoveCity/scripts.pory"

# 610 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_SomeonePuntedTeamAquaOut:
# 611 "data/maps/LilycoveCity/scripts.pory"
	.string "Ahoy, did you know?\p"
# 612 "data/maps/LilycoveCity/scripts.pory"
	.string "Someone punted TEAM AQUA out of\n"
# 613 "data/maps/LilycoveCity/scripts.pory"
	.string "the way for us!\p"
# 614 "data/maps/LilycoveCity/scripts.pory"
	.string "That got the WAILMER out of the cove,\n"
# 615 "data/maps/LilycoveCity/scripts.pory"
	.string "so we can get our boats out again.$"
# 616 "data/maps/LilycoveCity/scripts.pory"

# 617 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_SomeoneStoleMyPokemon:
# 618 "data/maps/LilycoveCity/scripts.pory"
	.string "I was taking a relaxing snooze at the\n"
# 619 "data/maps/LilycoveCity/scripts.pory"
	.string "seaside inn to the sound of waves…\p"
# 620 "data/maps/LilycoveCity/scripts.pory"
	.string "When someone stole my POKéMON!\p"
# 621 "data/maps/LilycoveCity/scripts.pory"
	.string "Who's the abductor?\n"
# 622 "data/maps/LilycoveCity/scripts.pory"
	.string "TEAM AQUA? Is it TEAM AQUA?$"
# 623 "data/maps/LilycoveCity/scripts.pory"

# 624 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MissingPokemonCameBack:
# 625 "data/maps/LilycoveCity/scripts.pory"
	.string "My missing POKéMON…\n"
# 626 "data/maps/LilycoveCity/scripts.pory"
	.string "It came back without me noticing!$"
# 627 "data/maps/LilycoveCity/scripts.pory"

# 628 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_ImArtDealer:
# 629 "data/maps/LilycoveCity/scripts.pory"
	.string "I'm an ART DEALER.\p"
# 630 "data/maps/LilycoveCity/scripts.pory"
	.string "I am a buyer and seller of fine art,\n"
# 631 "data/maps/LilycoveCity/scripts.pory"
	.string "especially paintings.\p"
# 632 "data/maps/LilycoveCity/scripts.pory"
	.string "I've heard that the MUSEUM here has\n"
# 633 "data/maps/LilycoveCity/scripts.pory"
	.string "magnificent works on exhibit…$"
# 634 "data/maps/LilycoveCity/scripts.pory"

# 635 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_SeaRemainsForeverYoung:
# 636 "data/maps/LilycoveCity/scripts.pory"
	.string "Even as we grow old and wrinkled,\n"
# 637 "data/maps/LilycoveCity/scripts.pory"
	.string "the sea remains forever young with\l"
# 638 "data/maps/LilycoveCity/scripts.pory"
	.string "the vivid brilliance of life…\p"
# 639 "data/maps/LilycoveCity/scripts.pory"
	.string "Fwohoho fwohohohoho…$"
# 640 "data/maps/LilycoveCity/scripts.pory"

# 641 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_SixtyYearsAgoHusbandProposed:
# 642 "data/maps/LilycoveCity/scripts.pory"
	.string "It was sixty years ago that my husband\n"
# 643 "data/maps/LilycoveCity/scripts.pory"
	.string "proposed to me here.\l"
# 644 "data/maps/LilycoveCity/scripts.pory"
	.string "The sea remains as beautiful as ever.\p"
# 645 "data/maps/LilycoveCity/scripts.pory"
	.string "Mufufufu mufufufufufu…$"
# 646 "data/maps/LilycoveCity/scripts.pory"

# 647 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_TeamAquaRenovatedCavern:
# 648 "data/maps/LilycoveCity/scripts.pory"
	.string "Hm, you know of the peculiar cavern\n"
# 649 "data/maps/LilycoveCity/scripts.pory"
	.string "in this cove?\p"
# 650 "data/maps/LilycoveCity/scripts.pory"
	.string "That had been a natural formation,\n"
# 651 "data/maps/LilycoveCity/scripts.pory"
	.string "but then that TEAM AQUA lot came\l"
# 652 "data/maps/LilycoveCity/scripts.pory"
	.string "along and made their renovations.\p"
# 653 "data/maps/LilycoveCity/scripts.pory"
	.string "They call themselves\n"
# 654 "data/maps/LilycoveCity/scripts.pory"
	.string "the “nature-loving TEAM AQUA”!\p"
# 655 "data/maps/LilycoveCity/scripts.pory"
	.string "But what they do and what they say\n"
# 656 "data/maps/LilycoveCity/scripts.pory"
	.string "don't match at all!$"
# 657 "data/maps/LilycoveCity/scripts.pory"

# 658 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_TeamAquaLotGoneForGood:
# 659 "data/maps/LilycoveCity/scripts.pory"
	.string "That cave in the cove…\p"
# 660 "data/maps/LilycoveCity/scripts.pory"
	.string "I didn't notice it right away,\n"
# 661 "data/maps/LilycoveCity/scripts.pory"
	.string "but it's completely empty now.\p"
# 662 "data/maps/LilycoveCity/scripts.pory"
	.string "That TEAM AQUA lot, they must\n"
# 663 "data/maps/LilycoveCity/scripts.pory"
	.string "have gone away for good.$"
# 664 "data/maps/LilycoveCity/scripts.pory"

# 665 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_CitySign:
# 666 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE CITY\p"
# 667 "data/maps/LilycoveCity/scripts.pory"
	.string "“Where the land ends and the\n"
# 668 "data/maps/LilycoveCity/scripts.pory"
	.string "sea begins.”$"
# 669 "data/maps/LilycoveCity/scripts.pory"

# 670 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_ContestHallSign:
# 671 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéMON CONTEST HALL\n"
# 672 "data/maps/LilycoveCity/scripts.pory"
	.string "“The gathering place for TRAINERS!”$"
# 673 "data/maps/LilycoveCity/scripts.pory"

# 674 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MotelSign:
# 675 "data/maps/LilycoveCity/scripts.pory"
	.string "COVE LILY MOTEL\p"
# 676 "data/maps/LilycoveCity/scripts.pory"
	.string "“Remember us as COVE LILY of\n"
# 677 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE.”$"
# 678 "data/maps/LilycoveCity/scripts.pory"

# 679 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MuseumSign:
# 680 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE MUSEUM\p"
# 681 "data/maps/LilycoveCity/scripts.pory"
	.string "“POKéMON Masterpiece Collection\n"
# 682 "data/maps/LilycoveCity/scripts.pory"
	.string "on exhibit!”$"
# 683 "data/maps/LilycoveCity/scripts.pory"

# 684 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MuseumSignPlayersExhibit:
# 685 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE MUSEUM\p"
# 686 "data/maps/LilycoveCity/scripts.pory"
	.string "“{PLAYER}'s POKéMON Collection\n"
# 687 "data/maps/LilycoveCity/scripts.pory"
	.string "on exhibit!”$"
# 688 "data/maps/LilycoveCity/scripts.pory"

# 689 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_HarborSignUnderConstruction:
# 690 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE CITY HARBOR\p"
# 691 "data/maps/LilycoveCity/scripts.pory"
	.string "“The ferry S.S. TIDAL is under\n"
# 692 "data/maps/LilycoveCity/scripts.pory"
	.string "construction in SLATEPORT CITY.\p"
# 693 "data/maps/LilycoveCity/scripts.pory"
	.string "“Service is scheduled to begin\n"
# 694 "data/maps/LilycoveCity/scripts.pory"
	.string "shortly.”$"
# 695 "data/maps/LilycoveCity/scripts.pory"

# 696 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_HarborSign:
# 697 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE CITY HARBOR\p"
# 698 "data/maps/LilycoveCity/scripts.pory"
	.string "“Enjoy a delightful cruise on\n"
# 699 "data/maps/LilycoveCity/scripts.pory"
	.string "the ferry S.S. TIDAL.”$"
# 700 "data/maps/LilycoveCity/scripts.pory"

# 701 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_TrainerFanClubSign:
# 702 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéMON TRAINER FAN CLUB\p"
# 703 "data/maps/LilycoveCity/scripts.pory"
	.string "The names of TRAINERS are scribbled\n"
# 704 "data/maps/LilycoveCity/scripts.pory"
	.string "all over the sign…$"
# 705 "data/maps/LilycoveCity/scripts.pory"

# 706 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_DepartmentStoreSign:
# 707 "data/maps/LilycoveCity/scripts.pory"
	.string "LILYCOVE DEPARTMENT STORE\p"
# 708 "data/maps/LilycoveCity/scripts.pory"
	.string "“Overflowing with great merchandise\n"
# 709 "data/maps/LilycoveCity/scripts.pory"
	.string "and excitement!\p"
# 710 "data/maps/LilycoveCity/scripts.pory"
	.string "“A great place to find that something\n"
# 711 "data/maps/LilycoveCity/scripts.pory"
	.string "you need!”$"
# 712 "data/maps/LilycoveCity/scripts.pory"

# 713 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_MoveDeletersHouseSign:
# 714 "data/maps/LilycoveCity/scripts.pory"
	.string "MOVE DELETER'S HOUSE\p"
# 715 "data/maps/LilycoveCity/scripts.pory"
	.string "“Unwanted POKéMON moves deleted.”$"
# 716 "data/maps/LilycoveCity/scripts.pory"

# 717 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_DoYouKnowAboutBerryBlender:
# 718 "data/maps/LilycoveCity/scripts.pory"
	.string "Do you know about the machine\n"
# 719 "data/maps/LilycoveCity/scripts.pory"
	.string "BERRY BLENDER?$"
# 720 "data/maps/LilycoveCity/scripts.pory"

# 721 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_FasterSpinBetterPokeblocks:
# 722 "data/maps/LilycoveCity/scripts.pory"
	.string "People have to work together to get it\n"
# 723 "data/maps/LilycoveCity/scripts.pory"
	.string "to spin faster.\p"
# 724 "data/maps/LilycoveCity/scripts.pory"
	.string "The faster you can make it spin, the\n"
# 725 "data/maps/LilycoveCity/scripts.pory"
	.string "better {POKEBLOCK}S you can get, I've heard.$"
# 726 "data/maps/LilycoveCity/scripts.pory"

# 727 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_ExplainBerryBlender:
# 728 "data/maps/LilycoveCity/scripts.pory"
	.string "It's used for making a kind of candy\n"
# 729 "data/maps/LilycoveCity/scripts.pory"
	.string "called a {POKEBLOCK}.\p"
# 730 "data/maps/LilycoveCity/scripts.pory"
	.string "If you give a good {POKEBLOCK} to a POKéMON,\n"
# 731 "data/maps/LilycoveCity/scripts.pory"
	.string "its condition will improve by a lot.$"
# 732 "data/maps/LilycoveCity/scripts.pory"

# 733 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_HeardTowerCalledSkyPillar:
# 734 "data/maps/LilycoveCity/scripts.pory"
	.string "I heard there's a tower somewhere out\n"
# 735 "data/maps/LilycoveCity/scripts.pory"
	.string "on the sea routes.\p"
# 736 "data/maps/LilycoveCity/scripts.pory"
	.string "It's called the SKY PILLAR, I hear.$"
# 737 "data/maps/LilycoveCity/scripts.pory"

# 738 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_SawTallTowerOnRoute131:
# 739 "data/maps/LilycoveCity/scripts.pory"
	.string "I saw this tall tower somewhere\n"
# 740 "data/maps/LilycoveCity/scripts.pory"
	.string "around ROUTE 131.\p"
# 741 "data/maps/LilycoveCity/scripts.pory"
	.string "Could that possibly be…?$"
# 742 "data/maps/LilycoveCity/scripts.pory"

# 743 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_JustArrivedAndSawRarePokemon:
# 744 "data/maps/LilycoveCity/scripts.pory"
	.string "We just arrived here on our\n"
# 745 "data/maps/LilycoveCity/scripts.pory"
	.string "honeymoon vacation.\p"
# 746 "data/maps/LilycoveCity/scripts.pory"
	.string "We happened to see a DRAGON-type\n"
# 747 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéMON flying way up in the sky.\p"
# 748 "data/maps/LilycoveCity/scripts.pory"
	.string "Do cool POKéMON like that live in\n"
# 749 "data/maps/LilycoveCity/scripts.pory"
	.string "the HOENN region?$"
# 750 "data/maps/LilycoveCity/scripts.pory"

# 751 "data/maps/LilycoveCity/scripts.pory"
LilycoveCity_Text_HoneymoonVowToSeeRarePokemon:
# 752 "data/maps/LilycoveCity/scripts.pory"
	.string "On our honeymoon, we vowed to see as\n"
# 753 "data/maps/LilycoveCity/scripts.pory"
	.string "many rare POKéMON as we can.\p"
# 754 "data/maps/LilycoveCity/scripts.pory"
	.string "So we were delighted to see a rare\n"
# 755 "data/maps/LilycoveCity/scripts.pory"
	.string "POKéMON as soon as we arrived.\p"
# 756 "data/maps/LilycoveCity/scripts.pory"
	.string "I mean, we are totally happy!$"
