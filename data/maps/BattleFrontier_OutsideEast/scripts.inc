# 1 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 2 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_MapScripts::
# 3 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	map_script MAP_SCRIPT_ON_RESUME, BattleFrontier_OutsideEast_OnResume
# 4 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	map_script MAP_SCRIPT_ON_TRANSITION, BattleFrontier_OutsideEast_OnTransition
# 5 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.byte 0
# 6 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 7 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_OnResume:
# 8 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, BattleFrontier_OutsideEast_EventScript_TryRemoveSudowoodo
# 9 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 10 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 11 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_TryRemoveSudowoodo::
# 12 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 13 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
# 14 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	removeobject VAR_LAST_TALKED
# 15 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	return
# 16 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 17 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_OnTransition:
# 18 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setvar VAR_BRAVO_TRAINER_BATTLE_TOWER_ON, 0
# 19 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setflag FLAG_HIDE_BATTLE_TOWER_REPORTER
# 20 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	call_if_unset FLAG_DEFEATED_SUDOWOODO, BattleFrontier_OutsideEast_EventScript_ShowSudowoodo
# 21 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 22 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 23 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_ShowSudowoodo::
# 24 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	clearflag FLAG_HIDE_BATTLE_FRONTIER_SUDOWOODO
# 25 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	return
# 26 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 27 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_BattleTowerSign::
# 28 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BattleTowerSign, MSGBOX_SIGN
# 29 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 30 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 31 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_BattlePalaceSign::
# 32 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BattlePalaceSign, MSGBOX_SIGN
# 33 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 34 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 35 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_BattleArenaSign::
# 36 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BattleArenaSign, MSGBOX_SIGN
# 37 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 38 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 39 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_BattlePyramidSign::
# 40 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BattlePyramidSign, MSGBOX_SIGN
# 41 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 42 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 43 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_NinjaBoy::
# 44 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BattleTowerFeelsSpecial, MSGBOX_NPC
# 45 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 46 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 47 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Man1::
# 48 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_ConquerLeagueAndFrontier, MSGBOX_NPC
# 49 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 50 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 51 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Hiker::
# 52 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_PyramidTooHarsh, MSGBOX_NPC
# 53 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 54 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 55 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_HexManiac::
# 56 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_ThriveInDarkness, MSGBOX_NPC
# 57 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 58 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 59 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_BlackBelt1::
# 60 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_PutTogetherUltimateTeam, MSGBOX_NPC
# 61 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 62 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 63 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Cook::
# 64 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 65 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BelieveInYouBuddy, MSGBOX_DEFAULT
# 66 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 67 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 68 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 69 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Zigzagoon::
# 70 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 71 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	faceplayer
# 72 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitse
# 73 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	playmoncry SPECIES_ZIGZAGOON, CRY_MODE_NORMAL
# 74 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_ZigzagoonLooksVacant, MSGBOX_DEFAULT
# 75 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitmoncry
# 76 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 77 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 78 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 79 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_RichBoy::
# 80 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_PeopleCallMeBusybody, MSGBOX_NPC
# 81 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 82 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 83 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_ExpertF::
# 84 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_OnceBeatGymLeader, MSGBOX_NPC
# 85 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 86 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 87 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_TriathleteF::
# 88 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_FastOnBikeAndBattles, MSGBOX_NPC
# 89 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 90 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 91 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Twin::
# 92 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_BetterThanDaddyAtPokemon, MSGBOX_NPC
# 93 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 94 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 95 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Man2::
# 96 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 97 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_GoRackUpSomeWinsForDaddy, MSGBOX_DEFAULT
# 98 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 99 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 100 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 101 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_TriathleteM::
# 102 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_DidScottBringYouHere, MSGBOX_NPC
# 103 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 104 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 105 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Sudowoodo::
# 106 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 107 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	faceplayer
# 108 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitse
# 109 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	playse SE_SUDOWOODO_SHAKE
# 110 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	applymovement LOCALID_FRONTIER_SUDOWOODO, BattleFrontier_OutsideEast_Movement_SudowoodoShake
# 111 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitmovement 0
# 112 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 113 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 114 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 115 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_WaterSudowoodo::
# 116 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 117 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	faceplayer
# 118 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	special DoWateringBerryTreeAnim
# 119 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitse
# 120 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	playse SE_SUDOWOODO_SHAKE
# 121 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	applymovement LOCALID_FRONTIER_SUDOWOODO, BattleFrontier_OutsideEast_Movement_SudowoodoShake
# 122 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitmovement 0
# 123 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox gText_Sudowoodo_Attacked, MSGBOX_DEFAULT
# 124 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	closemessage
# 125 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitse
# 126 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	playmoncry SPECIES_SUDOWOODO, CRY_MODE_ENCOUNTER
# 127 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay 40
# 128 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	waitmoncry
# 129 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setvar VAR_LAST_TALKED, LOCALID_FRONTIER_SUDOWOODO
# 130 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setwildbattle SPECIES_SUDOWOODO, 40
# 131 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setflag FLAG_SYS_CTRL_OBJ_DELETE
# 132 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	dowildbattle
# 133 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
# 134 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	specialvar VAR_RESULT, GetBattleOutcome
# 135 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo
# 136 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo
# 137 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo
# 138 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setflag FLAG_DEFEATED_SUDOWOODO
# 139 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 140 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 141 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 142 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_DefeatedSudowoodo::
# 143 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	setflag FLAG_DEFEATED_SUDOWOODO
# 144 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	goto Common_EventScript_RemoveStaticPokemon
# 145 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 146 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 147 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Movement_SudowoodoShake:
# 148 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_right
# 149 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 150 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_down
# 151 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 152 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_left
# 153 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 154 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_down
# 155 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 156 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_right
# 157 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 158 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_down
# 159 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 160 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_left
# 161 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	delay_8
# 162 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	face_down
# 163 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	step_end
# 164 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 165 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Maniac1::
# 166 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_HeardPrettyGirlAtBattleArena, MSGBOX_NPC
# 167 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 168 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 169 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Girl::
# 170 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_SometimesImportantOldManInThere, MSGBOX_NPC
# 171 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 172 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 173 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_PsychicM::
# 174 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_LegendOfBattlePyramid, MSGBOX_NPC
# 175 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 176 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 177 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Man3::
# 178 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_GotWipedOut, MSGBOX_NPC
# 179 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 180 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 181 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Woman1::
# 182 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_ToughTrainerInBattleTower, MSGBOX_NPC
# 183 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 184 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 185 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Woman2::
# 186 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_EnoughBattlePointsForDoll, MSGBOX_NPC
# 187 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 188 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 189 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_BlackBelt2::
# 190 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_LikeToHaveNameRecordedHere, MSGBOX_NPC
# 191 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 192 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 193 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Maniac2::
# 194 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 195 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_CanDoAnythingWithYou, MSGBOX_DEFAULT
# 196 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 197 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 198 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 199 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Woman3::
# 200 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 201 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_PowerOfOurLoveWillOvercome, MSGBOX_DEFAULT
# 202 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 203 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 204 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 205 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_RankingHallSign::
# 206 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_RankingHallSign, MSGBOX_SIGN
# 207 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 208 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 209 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_ExchangeCornerSign::
# 210 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_ExchangeCornerSign, MSGBOX_SIGN
# 211 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 212 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 213 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Gentleman::
# 214 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_FrontierNotExclusivelyForToughTrainers, MSGBOX_NPC
# 215 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 216 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 217 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_OldWoman::
# 218 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	lock
# 219 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	faceplayer
# 220 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	goto_if_set FLAG_DEFEATED_SUDOWOODO, BattleFrontier_OutsideEast_EventScript_OldWomanSudowoodoGone
# 221 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_OddTreeHereSeemsToWiggle, MSGBOX_DEFAULT
# 222 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 223 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 224 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 225 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_OldWomanSudowoodoGone::
# 226 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_OnceAnOddTreePastHere, MSGBOX_DEFAULT
# 227 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	release
# 228 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 229 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 230 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_EventScript_Camper::
# 231 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	msgbox BattleFrontier_OutsideEast_Text_StickyMonWithLongTail, MSGBOX_NPC
# 232 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	end
# 233 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 234 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BattleTowerSign:
# 235 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "This is the BATTLE TOWER!\n"
# 236 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Keep the win streak as the toughest\l"
# 237 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "TRAINER!$"
# 238 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 239 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BattlePalaceSign:
# 240 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "This is the BATTLE PALACE!\n"
# 241 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Keep your eyes on POKéMON battles!$"
# 242 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 243 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BattleArenaSign:
# 244 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "This is the BATTLE ARENA!\n"
# 245 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Let the toughest teams gather!$"
# 246 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 247 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BattlePyramidSign:
# 248 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "This is the BATTLE PYRAMID!\n"
# 249 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Advance through the Battle Quest!$"
# 250 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 251 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_RankingHallSign:
# 252 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "BATTLE FRONTIER RANKING HALL\n"
# 253 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Set your sights on new records!$"
# 254 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 255 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_ExchangeCornerSign:
# 256 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "BATTLE POINT EXCHANGE SERVICE CORNER\n"
# 257 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Exchange your Battle Points!$"
# 258 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 259 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BattleTowerFeelsSpecial:
# 260 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Wow!\n"
# 261 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "It's huge!\p"
# 262 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "The BATTLE TOWER feels special.\n"
# 263 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "It's different from the others.$"
# 264 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 265 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_ConquerLeagueAndFrontier:
# 266 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "My grand ambition is to conquer both\n"
# 267 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "the BATTLE FRONTIER and the POKéMON\l"
# 268 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "LEAGUE.\p"
# 269 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "And if my dream comes true…\p"
# 270 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I… I'm going to ask MIMI next door\n"
# 271 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "if she will be friends with me!$"
# 272 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 273 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_PyramidTooHarsh:
# 274 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "The BATTLE PYRAMID's too harsh!\n"
# 275 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I just can't make it to the top!\p"
# 276 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Since I'm out of options, maybe I can\n"
# 277 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "climb the outside…$"
# 278 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 279 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_ThriveInDarkness:
# 280 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I thrive in darkness…\n"
# 281 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Yes… What is worthy of me?\l"
# 282 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "None other than the BATTLE PYRAMID…\p"
# 283 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "What say you to wandering in darkness\n"
# 284 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "and in utter and total desperation?$"
# 285 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 286 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_PutTogetherUltimateTeam:
# 287 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I didn't sleep for a week, but then\n"
# 288 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I put together the ultimate team!\p"
# 289 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I can't see myself losing, no joke.\n"
# 290 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "We're storming the BATTLE ARENA!$"
# 291 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 292 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_DidScottBringYouHere:
# 293 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Did SCOTT bring you here, too?\n"
# 294 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "What is it with that guy?\p"
# 295 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "It sounds like he really does know\n"
# 296 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "how to spot talented TRAINERS, but…\p"
# 297 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I've never seen him battling in person\n"
# 298 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "ever.$"
# 299 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 300 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BelieveInYouBuddy:
# 301 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "ZIGG!\n"
# 302 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I believe in you, little buddy!\p"
# 303 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I'll make my little ZIGG any favorite\n"
# 304 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "tasty treats you like if you win!$"
# 305 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 306 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_ZigzagoonLooksVacant:
# 307 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "ZIGZAGOON looks vacant…$"
# 308 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 309 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_PeopleCallMeBusybody:
# 310 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "People call me a busybody,\n"
# 311 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "but I can't help it.\p"
# 312 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Your hat's on crooked!\n"
# 313 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Oh, no, trash on the ground!\l"
# 314 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Oops, it's almost dinnertime!\p"
# 315 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I don't know if I can stand to just\n"
# 316 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "watch at the BATTLE PALACE…$"
# 317 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 318 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_OnceBeatGymLeader:
# 319 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I may not look that impressive now,\n"
# 320 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "but I once beat a GYM LEADER.\p"
# 321 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Who knows, maybe I should give it\n"
# 322 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "another shot at glory.$"
# 323 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 324 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_FastOnBikeAndBattles:
# 325 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I'm fast on my BIKE, and that goes for\n"
# 326 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "the way I battle, too.\p"
# 327 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I win matches in the blink of\n"
# 328 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "an eye!$"
# 329 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 330 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_BetterThanDaddyAtPokemon:
# 331 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I'm better than my daddy\n"
# 332 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "at POKéMON.$"
# 333 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 334 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_GoRackUpSomeWinsForDaddy:
# 335 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Go on, my baby sweetie!\n"
# 336 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Go rack up some wins for Daddy!\p"
# 337 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "You're just like your mother,\n"
# 338 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "so you'll be dominating!$"
# 339 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 340 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_HeardPrettyGirlAtBattleArena:
# 341 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "It wasn't easy getting here,\n"
# 342 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "but I'd heard about this knockout\l"
# 343 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "pretty girl at the BATTLE ARENA.\p"
# 344 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Instead of her, do you know what\n"
# 345 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I found?\p"
# 346 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "A whole teeming mob of sweaty,\n"
# 347 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "stinky, and primitive martial artists!$"
# 348 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 349 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_SometimesImportantOldManInThere:
# 350 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I sometimes see this really important-\n"
# 351 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "looking old man going in there.\p"
# 352 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "He has these really awesome POKéMON.\n"
# 353 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "He seems really nice, though.$"
# 354 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 355 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_LegendOfBattlePyramid:
# 356 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Do you know it?\n"
# 357 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "The legend of the BATTLE PYRAMID?\p"
# 358 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "When there comes a confident TRAINER\n"
# 359 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "reaching for the golden pinnacle,\l"
# 360 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "there shall appear a man among men.\p"
# 361 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Don't know that legend?\n"
# 362 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Well, of course not!\l"
# 363 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I just made it up!\p"
# 364 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "What's it supposed to mean?\n"
# 365 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "That, my friend, I can't say!$"
# 366 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 367 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_GotWipedOut:
# 368 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Man! Oh man!\n"
# 369 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I've never lost once before!\p"
# 370 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "But I got wiped out with no saving\n"
# 371 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "grace at all!\p"
# 372 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "And then I'm told I don't have any\n"
# 373 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "talent?! Man!$"
# 374 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 375 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_ToughTrainerInBattleTower:
# 376 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "This guy ran into a horribly tough\n"
# 377 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "TRAINER while he was on the BATTLE\l"
# 378 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "TOWER challenge.\p"
# 379 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Now look at him…\p"
# 380 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "You need to be cautious if you ever\n"
# 381 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "decide to go to the BATTLE TOWER.$"
# 382 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 383 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_EnoughBattlePointsForDoll:
# 384 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Yes!\n"
# 385 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I've finally got enough Battle Points!\p"
# 386 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I guess I'll trade for another giant\n"
# 387 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "plush DOLL!$"
# 388 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 389 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_LikeToHaveNameRecordedHere:
# 390 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Oh, yeah, okay!\n"
# 391 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "So this is the RANKING HALL!\p"
# 392 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I'd like to go down in history as\n"
# 393 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "a super champ and have my name\l"
# 394 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "recorded here for posterity.$"
# 395 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 396 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_CanDoAnythingWithYou:
# 397 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "With you by my side, I can do anything.$"
# 398 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 399 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_PowerOfOurLoveWillOvercome:
# 400 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Ooh, darling, you are so wonderful!\p"
# 401 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Ooh, I just can't wait anymore!\p"
# 402 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Let's go to a MULTI BATTLE ROOM\n"
# 403 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "right this instant!\p"
# 404 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "If we get together in the BATTLE SALON,\n"
# 405 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "the power of our love will overcome\l"
# 406 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "everyone we meet.\p"
# 407 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Why, before us, darling, everything\n"
# 408 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "will topple like dominoes!$"
# 409 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 410 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_FrontierNotExclusivelyForToughTrainers:
# 411 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "The BATTLE FRONTIER isn't exclusively\n"
# 412 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "for tough TRAINERS.\p"
# 413 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Many people with special abilities\n"
# 414 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "have been invited, it seems.\p"
# 415 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "That man SCOTT…\p"
# 416 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "He may have built this place to serve\n"
# 417 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "a bigger objective…$"
# 418 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 419 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_OddTreeHereSeemsToWiggle:
# 420 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Excuse me, young one.\n"
# 421 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Have you good eyesight?\p"
# 422 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "There is an odd tree past here, and to\n"
# 423 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "my tired eyes it seems to wiggle.$"
# 424 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 425 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_OnceAnOddTreePastHere:
# 426 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Excuse me, young one.\n"
# 427 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "Have you a good memory?\p"
# 428 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I have this feeling there once was\n"
# 429 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "an odd tree past here.$"
# 430 "data/maps/BattleFrontier_OutsideEast/scripts.pory"

# 431 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
BattleFrontier_OutsideEast_Text_StickyMonWithLongTail:
# 432 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I…\n"
# 433 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "I saw it!\p"
# 434 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "There was a sticky sort of a POKéMON\n"
# 435 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "with a long tail up ahead!\p"
# 436 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "It was hiding under a boulder, and\n"
# 437 "data/maps/BattleFrontier_OutsideEast/scripts.pory"
	.string "it kept staring at me!$"
