#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/apprentice.h"
#include "constants/apricorn_tree.h"
#include "constants/quests.h"
#include "constants/battle.h"
#include "constants/battle_arena.h"
#include "constants/battle_dome.h"
#include "constants/battle_factory.h"
#include "constants/battle_frontier.h"
#include "constants/battle_palace.h"
#include "constants/battle_pike.h"
#include "constants/battle_pyramid.h"
#include "constants/battle_special.h"
#include "constants/battle_tent.h"
#include "constants/battle_tower.h"
#include "constants/berry.h"
#include "constants/cable_club.h"
#include "constants/coins.h"
#include "constants/comparison_operators.h"
#include "constants/contest.h"
#include "constants/daycare.h"
#include "constants/decorations.h"
#include "constants/difficulty.h"
#include "constants/easy_chat.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/fame_checker.h"
#include "constants/field_effects.h"
#include "constants/field_move.h"
#include "constants/field_poison.h"
#include "constants/field_specials.h"
#include "constants/field_tasks.h"
#include "constants/field_weather.h"
#include "constants/flags.h"
#include "constants/follower_npc.h"
#include "constants/frontier_util.h"
#include "constants/game_stat.h"
#include "constants/item.h"
#include "constants/items.h"
#include "constants/heal_locations.h"
#include "constants/layouts.h"
#include "constants/lilycove_lady.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/mass_outbreak.h"
#include "constants/mauville_old_man.h"
#include "constants/metatile_labels.h"
#include "constants/move_relearner.h"
#include "constants/moves.h"
#include "constants/mystery_gift.h"
#include "constants/party_menu.h"
#include "constants/pokeball.h"
#include "constants/pokedex.h"
#include "constants/pokemon.h"
#include "constants/pokemon_size_record.h"
#include "constants/random_mon_generation.h"
#include "constants/rtc.h"
#include "constants/roulette.h"
#include "constants/script_menu.h"
#include "constants/seagallop.h"
#include "constants/voyages.h"
#include "constants/secret_bases.h"
#include "constants/siirtc.h"
#include "constants/songs.h"
#include "constants/sound.h"
#include "constants/species.h"
#include "constants/trade.h"
#include "constants/trainer_hill.h"
#include "constants/trainer_tower.h"
#include "constants/trainers.h"
#include "constants/train_stations.h"
#include "constants/train_sounds.h"
#include "constants/trainer_card.h"
#include "constants/tv.h"
#include "constants/union_room.h"
#include "constants/vars.h"
#include "constants/weather.h"
#include "constants/speaker_names.h"
#include "constants/holon.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.section script_data, "aw", %progbits

	.set ALLOCATE_SCRIPT_CMD_TABLE, 1
	.include "data/script_cmd_table.inc"

.align 2
gSpecialVars::
	.4byte gSpecialVar_0x8000
	.4byte gSpecialVar_0x8001
	.4byte gSpecialVar_0x8002
	.4byte gSpecialVar_0x8003
	.4byte gSpecialVar_0x8004
	.4byte gSpecialVar_0x8005
	.4byte gSpecialVar_0x8006
	.4byte gSpecialVar_0x8007
	.4byte gSpecialVar_0x8008
	.4byte gSpecialVar_0x8009
	.4byte gSpecialVar_0x800A
	.4byte gSpecialVar_0x800B
	.4byte gSpecialVar_Facing
	.4byte gSpecialVar_Result
	.4byte gSpecialVar_ItemId
	.4byte gSpecialVar_LastTalked
	.4byte gSpecialVar_ContestRank
	.4byte gSpecialVar_ContestCategory
	.4byte gSpecialVar_MonBoxId
	.4byte gSpecialVar_MonBoxPos
	.4byte gSpecialVar_Unused_0x8014
	.4byte gTrainerBattleParameter + 2 // gTrainerBattleParameter.params.opponentA

	.purgem def_special
	.set ALLOCATE_SPECIAL_TABLE, 1
	.include "data/specials.inc"

gStdScripts::
	.4byte Std_ObtainItem              @ STD_OBTAIN_ITEM
	.4byte Std_FindItem                @ STD_FIND_ITEM
	.4byte Std_MsgboxNPC               @ MSGBOX_NPC
	.4byte Std_MsgboxSign              @ MSGBOX_SIGN
	.4byte Std_MsgboxDefault           @ MSGBOX_DEFAULT
	.4byte Std_MsgboxYesNo             @ MSGBOX_YESNO
	.4byte Std_MsgboxAutoclose         @ MSGBOX_AUTOCLOSE
	.4byte Std_ObtainDecoration        @ STD_OBTAIN_DECORATION
	.4byte Std_RegisteredInMatchCall   @ STD_REGISTER_MATCH_CALL
	.4byte Std_MsgboxGetPoints         @ MSGBOX_GETPOINTS
	.4byte Std_MsgboxPokenav           @ MSGBOX_POKENAV
	.4byte Std_PutItemAway             @ STD_PUT_ITEM_AWAY
	.4byte Std_ReceivedItem            @ STD_RECEIVED_ITEM
gStdScripts_End::


	.include "data/maps/TosaPort/scripts.inc"
	.include "data/maps/TelokTown/scripts.inc"
	.include "data/maps/SouthTosaReserve/scripts.inc"
	.include "data/maps/TosaPort_BrendansHouse_1F/scripts.inc"
	.include "data/maps/TosaPort_BrendansHouse_2F/scripts.inc"
	.include "data/maps/TosaPort_MaysHouse_1F/scripts.inc"
	.include "data/maps/TosaPort_MaysHouse_2F/scripts.inc"
	.include "data/maps/TelokTown_PalmLabs/scripts.inc"
	.include "data/maps/TelokTown_PalmLabs_Flashback/scripts.inc"
	.include "data/maps/TelokTown_House1/scripts.inc"
	.include "data/maps/TrainTestEast/scripts.inc"
	.include "data/maps/TrainTestNorth/scripts.inc"
	.include "data/maps/MoongroveCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/MoongroveCity_Mart/scripts.inc"
	.include "data/maps/TimahCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/TimahCity_Mart/scripts.inc"
	.include "data/maps/FaberTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FaberTown_Mart/scripts.inc"
	.include "data/maps/ChanguCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/ChanguCity_Mart/scripts.inc"
	.include "data/maps/InkaCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/InkaCity_Mart/scripts.inc"
	.include "data/maps/BuraCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/BuraCity_Mart/scripts.inc"
	.include "data/maps/BuraCity_HawkerCentre/scripts.inc"
	.include "data/maps/JuranCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/JuranCity_Mart/scripts.inc"
	.include "data/maps/SenokoCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SenokoCity_Mart/scripts.inc"
	.include "data/maps/PokemonLeague_PokemonCenter_1F/scripts.inc"
	.include "data/maps/PokemonLeague_Mart/scripts.inc"
	.include "data/maps/CorralCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/CorralCity_Mart/scripts.inc"
	.include "data/maps/WavebreakTown/scripts.inc"
	.include "data/maps/WavebreakTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/WavebreakTown_Mart/scripts.inc"
	.include "data/maps/PinestampTown/scripts.inc"
	.include "data/maps/PinestampTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/PinestampTown_Mart/scripts.inc"
	.include "data/maps/ChallengerGate/scripts.inc"
	.include "data/maps/ChallengerGate_PokemonCenter_1F/scripts.inc"
	.include "data/maps/ChallengerGate_Mart/scripts.inc"
	.include "data/maps/Route302/scripts.inc"
	.include "data/maps/Route303/scripts.inc"
	.include "data/maps/Route304/scripts.inc"
	.include "data/maps/Route305/scripts.inc"
	.include "data/maps/Route306/scripts.inc"
	.include "data/maps/Route307/scripts.inc"
	.include "data/maps/Route308/scripts.inc"
	.include "data/maps/Route309/scripts.inc"
	.include "data/maps/Route310/scripts.inc"
	.include "data/maps/Route311_West/scripts.inc"
	.include "data/maps/Route311_East/scripts.inc"
	.include "data/maps/Route312/scripts.inc"
	.include "data/maps/Route313/scripts.inc"
	.include "data/maps/Route314/scripts.inc"
	.include "data/maps/MoongroveMarsh/scripts.inc"
	.include "data/maps/PowerPlant/scripts.inc"
	.include "data/maps/IndustrialPark/scripts.inc"
	.include "data/maps/AbandonedHouse/scripts.inc"
	.include "data/maps/GalangalForest/scripts.inc"
	.include "data/maps/KantuFalls/scripts.inc"
	.include "data/maps/RailwayTunnels/scripts.inc"
	.include "data/maps/DampPath/scripts.inc"
	.include "data/maps/SouthTosaReserve2/scripts.inc"
	.include "data/maps/SouthTosaReserve3/scripts.inc"
	.include "data/maps/SouthTosaReserve4/scripts.inc"
	.include "data/maps/NorthTosaReserve/scripts.inc"
	.include "data/maps/EastTosaReserve/scripts.inc"
	.include "data/maps/EastTosaReserve2/scripts.inc"
	.include "data/maps/EastTosaReserve3/scripts.inc"
	.include "data/maps/MtBatok_1F/scripts.inc"
	.include "data/maps/MtBatok_2F/scripts.inc"
	.include "data/maps/MtBatok_3F/scripts.inc"
	.include "data/maps/MtBatok_East_2F/scripts.inc"
	.include "data/maps/MtBatok_East_1F/scripts.inc"
	.include "data/maps/ChallengersTrail_1F/scripts.inc"
	.include "data/maps/ChallengersTrail_Cliffs/scripts.inc"
	.include "data/maps/ChallengersTrail_2F/scripts.inc"
	.include "data/maps/ChallengersTrail_3F/scripts.inc"
	.include "data/maps/MoongroveCity_Gym/scripts.inc"
	.include "data/maps/MoongroveCity_House1/scripts.inc"
	.include "data/maps/MoongroveCity_House2/scripts.inc"
	.include "data/maps/MoongroveCity_House3/scripts.inc"
	.include "data/maps/MoongroveCity_House4/scripts.inc"
	.include "data/maps/TimahCity_Gym/scripts.inc"
	.include "data/maps/TimahCity_House1/scripts.inc"
	.include "data/maps/TimahCity_House2/scripts.inc"
	.include "data/maps/TimahCity_House3/scripts.inc"
	.include "data/maps/TimahCity_House4/scripts.inc"
	.include "data/maps/FaberTown_Gym/scripts.inc"
	.include "data/maps/FaberTown_House1/scripts.inc"
	.include "data/maps/FaberTown_House2/scripts.inc"
	.include "data/maps/ChanguCity_Gym/scripts.inc"
	.include "data/maps/ChanguCity_House1/scripts.inc"
	.include "data/maps/ChanguCity_House2/scripts.inc"
	.include "data/maps/ChanguCity_House3/scripts.inc"
	.include "data/maps/ChanguCity_House4/scripts.inc"
	.include "data/maps/ChanguAirport_House1/scripts.inc"
	.include "data/maps/InkaCity_Gym/scripts.inc"
	.include "data/maps/InkaCity_House1/scripts.inc"
	.include "data/maps/InkaCity_House2/scripts.inc"
	.include "data/maps/InkaCity_House3/scripts.inc"
	.include "data/maps/InkaCity_House4/scripts.inc"
	.include "data/maps/BuraCity_Gym/scripts.inc"
	.include "data/maps/BuraCity_House1/scripts.inc"
	.include "data/maps/BuraCity_House2/scripts.inc"
	.include "data/maps/JuranCity_House1/scripts.inc"
	.include "data/maps/JuranCity_House2/scripts.inc"
	.include "data/maps/JuranCity_House3/scripts.inc"
	.include "data/maps/JuranCity_House4/scripts.inc"
	.include "data/maps/SenokoCity_Gym/scripts.inc"
	.include "data/maps/SenokoCity_House1/scripts.inc"
	.include "data/maps/SenokoCity_House2/scripts.inc"
	.include "data/maps/SenokoCity_House3/scripts.inc"
	.include "data/maps/PokemonLeague_House1/scripts.inc"
	.include "data/maps/PokemonLeague_House2/scripts.inc"
	.include "data/maps/PoketopiaGate_House1/scripts.inc"
	.include "data/maps/PoketopiaGate_House2/scripts.inc"
	.include "data/maps/CorralCity_Gym/scripts.inc"
	.include "data/maps/CorralCity_House1/scripts.inc"
	.include "data/maps/CorralCity_House2/scripts.inc"
	.include "data/maps/CorralCity_House3/scripts.inc"
	.include "data/maps/WavebreakTown_House1/scripts.inc"
	.include "data/maps/WavebreakTown_House2/scripts.inc"
	.include "data/maps/WavebreakTown_House3/scripts.inc"
	.include "data/maps/PinestampTown_House1/scripts.inc"
	.include "data/maps/PinestampTown_House2/scripts.inc"
	.include "data/maps/PinestampTown_House3/scripts.inc"
	.include "data/maps/ChallengerGate_House1/scripts.inc"
	.include "data/maps/ChallengerGate_House2/scripts.inc"
	.include "data/maps/AbandonedHouse_House1/scripts.inc"
	.include "data/maps/MoongroveCity/scripts.inc"
	.include "data/maps/MoongroveCity_Station/scripts.inc"
	.include "data/maps/MoongroveCity_StationPlatform/scripts.inc"
	.include "data/maps/TimahCity/scripts.inc"
	.include "data/maps/TimahCity_Station/scripts.inc"
	.include "data/maps/TimahCity_StationPlatform/scripts.inc"
	.include "data/maps/FaberTown/scripts.inc"
	.include "data/maps/FaberTown_Station/scripts.inc"
	.include "data/maps/FaberTown_StationPlatform/scripts.inc"
	.include "data/maps/ChanguCity/scripts.inc"
	.include "data/maps/ChanguCity_Station/scripts.inc"
	.include "data/maps/ChanguCity_StationPlatform/scripts.inc"
	.include "data/maps/ChanguAirport/scripts.inc"
	.include "data/maps/ChanguAirport_Station/scripts.inc"
	.include "data/maps/ChanguAirport_StationPlatform/scripts.inc"
	.include "data/maps/InkaCity/scripts.inc"
	.include "data/maps/InkaSeawall/scripts.inc"
	.include "data/maps/ChanguCity_Cafe/scripts.inc"
	.include "data/maps/InkaCity_Station/scripts.inc"
	.include "data/maps/InkaCity_StationPlatform/scripts.inc"
	.include "data/maps/BuraCity/scripts.inc"
	.include "data/maps/BuraCity_Station/scripts.inc"
	.include "data/maps/BuraCity_StationPlatform/scripts.inc"
	.include "data/maps/JuranCity/scripts.inc"
	.include "data/maps/JuranCity_Station/scripts.inc"
	.include "data/maps/JuranCity_StationPlatform/scripts.inc"
	.include "data/maps/SenokoCity/scripts.inc"
	.include "data/maps/SenokoCity_Station/scripts.inc"
	.include "data/maps/SenokoCity_StationPlatform/scripts.inc"
	.include "data/maps/PokemonLeague/scripts.inc"
	.include "data/maps/PokemonLeague_Station/scripts.inc"
	.include "data/maps/PokemonLeague_StationPlatform/scripts.inc"
	.include "data/maps/PoketopiaGate/scripts.inc"
	.include "data/maps/PoketopiaGate_Station/scripts.inc"
	.include "data/maps/PoketopiaGate_StationPlatform/scripts.inc"
	.include "data/maps/CorralCity/scripts.inc"
	.include "data/maps/CorralCity_Station/scripts.inc"
	.include "data/maps/CorralCity_StationPlatform/scripts.inc"
	.include "data/maps/HawkerCentreTest/scripts.inc"
	.include "data/maps/ColdStorageTest/scripts.inc"
	.include "data/maps/ColdStorageTestOutside/scripts.inc"
	.include "data/maps/FurongVillage/scripts.inc" @ tiksi-maps
	.include "data/maps/FurongVillage_PokemonCenter_1F/scripts.inc" @ tiksi-maps
	.include "data/maps/DrakeBaseCamp/scripts.inc" @ tiksi-maps
	.include "data/maps/DrakeBaseCamp_PokemonCenter_1F/scripts.inc" @ tiksi-maps
	.include "data/maps/UbeCity/scripts.inc" @ tiksi-maps
	.include "data/maps/UbeCity_PokemonCenter_1F/scripts.inc" @ tiksi-maps
	.include "data/maps/TanglynTown/scripts.inc" @ tiksi-maps
	.include "data/maps/TanglynTown_PokemonCenter_1F/scripts.inc" @ tiksi-maps
	.include "data/maps/RegolisShrine/scripts.inc" @ tiksi-maps
	.include "data/maps/FrigoCave/scripts.inc" @ tiksi-maps
	.include "data/maps/FerrumShrine/scripts.inc" @ tiksi-maps
	.include "data/maps/GavaniPath/scripts.inc" @ tiksi-maps
	.include "data/maps/MtDrakeSummit/scripts.inc" @ tiksi-maps
	.include "data/maps/MtDrake_WestFace/scripts.inc" @ mt-drake
	.include "data/maps/MtDrake_SouthFace/scripts.inc" @ mt-drake
	.include "data/maps/MtDrake_1F/scripts.inc" @ mt-drake
	.include "data/maps/MtDrake_2F/scripts.inc" @ mt-drake
	.include "data/maps/MtDrake_NorthFace/scripts.inc" @ mt-drake
	.include "data/maps/MtDrake_3F/scripts.inc" @ mt-drake
	.include "data/maps/MtDrake_Peak/scripts.inc" @ mt-drake
	.include "data/maps/FurongVillage_House1/scripts.inc" @ tiksi-people
	.include "data/maps/FurongVillage_House2/scripts.inc" @ tiksi-people
	.include "data/maps/DrakeBaseCamp_Mart/scripts.inc" @ tiksi-people
	.include "data/maps/DrakeBaseCamp_House1/scripts.inc" @ tiksi-people
	.include "data/maps/DrakeBaseCamp_House2/scripts.inc" @ tiksi-people
	.include "data/maps/UbeCity_Mart/scripts.inc" @ tiksi-people
	.include "data/maps/UbeCity_House1/scripts.inc" @ tiksi-people
	.include "data/maps/UbeCity_House2/scripts.inc" @ tiksi-people
	.include "data/maps/TanglynTown_House1/scripts.inc" @ tiksi-people
	.include "data/maps/TanglynTown_House2/scripts.inc" @ tiksi-people
	.include "data/maps/Route401/scripts.inc" @ tiksi-routes
	.include "data/maps/Route402/scripts.inc" @ tiksi-routes
	.include "data/maps/Route403/scripts.inc" @ tiksi-routes
	.include "data/maps/Route404/scripts.inc" @ tiksi-routes
	.include "data/maps/Route405/scripts.inc" @ tiksi-routes
	.include "data/maps/Route406/scripts.inc" @ tiksi-routes
	.include "data/maps/Route407/scripts.inc" @ tiksi-routes
	.include "data/maps/Route408/scripts.inc" @ tiksi-routes
	.include "data/maps/Route409/scripts.inc" @ tiksi-routes
	.include "data/maps/Route410/scripts.inc" @ tiksi-routes
	.include "data/maps/TanobyDelta/scripts.inc" @ tiksi-routes
	.include "data/maps/FrigoCave_Exterior/scripts.inc" @ tiksi-routes
	.include "data/maps/WavebreakTown_SailorsHut/scripts.inc" @ voyages
	.include "data/maps/NewmoonIsland/scripts.inc" @ voyages
	.include "data/maps/NewmoonIsland_Interior/scripts.inc" @ voyages
	.include "data/maps/FullmoonIsland/scripts.inc" @ voyages
	.include "data/maps/FullmoonIsland_Interior/scripts.inc" @ voyages
	.include "data/maps/TelokTown_House2/scripts.inc"
	.include "data/maps/TelokTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/TelokTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/TelokTown_Mart/scripts.inc"
	.include "data/maps/EverGrandeCity_SidneysRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_PhoebesRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_GlaciasRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_DrakesRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_ChampionsRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall1/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall2/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall3/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall4/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall5/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc"
	.include "data/maps/EverGrandeCity_HallOfFame/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonLeague_2F/scripts.inc"
	.include "data/scripts/shared_secret_base.inc"
	.include "data/maps/BattleColosseum_2P/scripts.inc"
	.include "data/maps/TradeCenter/scripts.inc"
	.include "data/maps/RecordCorner/scripts.inc"
	.include "data/maps/BattleColosseum_4P/scripts.inc"
	.include "data/maps/ContestHall/scripts.inc"
	.include "data/maps/InsideOfTruck/scripts.inc"
	.include "data/maps/SSTidalCorridor/scripts.inc"
	.include "data/maps/SSTidalLowerDeck/scripts.inc"
	.include "data/maps/SSTidalRooms/scripts.inc"
	.include "data/maps/BattlePyramidSquare01/scripts.inc"
	.include "data/maps/UnionRoom/scripts.inc"
	.include "data/maps/BattleFrontier_OutsideWest/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerElevator/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerBattleRoom/scripts.inc"
	.include "data/maps/SouthernIsland_Exterior/scripts.inc"
	.include "data/maps/SouthernIsland_Interior/scripts.inc"
	.include "data/maps/BattleFrontier_OutsideEast/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerMultiPartnerRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerMultiCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerMultiBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomeLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomeCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomeBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePalaceLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePalaceCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePalaceBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePyramidLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePyramidFloor/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePyramidTop/scripts.inc"
	.include "data/maps/BattleFrontier_BattleArenaLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleArenaCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleArenaBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleFactoryLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleFactoryPreBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleFactoryBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeThreePathRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeRoomNormal/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeRoomFinal/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeRoomWildMons/scripts.inc"
	.include "data/maps/BattleFrontier_RankingHall/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge1/scripts.inc"
	.include "data/maps/BattleFrontier_ExchangeServiceCorner/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge2/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge3/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge4/scripts.inc"
	.include "data/maps/BattleFrontier_ScottsHouse/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge5/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge6/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge7/scripts.inc"
	.include "data/maps/BattleFrontier_ReceptionGate/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge8/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge9/scripts.inc"
	.include "data/maps/BattleFrontier_PokemonCenter_1F/scripts.inc"
	.include "data/maps/BattleFrontier_PokemonCenter_2F/scripts.inc"
	.include "data/maps/BattleFrontier_Mart/scripts.inc"
	.include "data/maps/HolonMirageForest/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_PokemonCenter_1F/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_Mart/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House1/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House2/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House3/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House4/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House5/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House6/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_House7/scripts.inc" @ holon-maps
	.include "data/maps/HolonVillage_RuinsHouse/scripts.inc" @ holon-maps
	.include "data/maps/HolonResearchTower_1F/scripts.inc" @ holon-maps
	.include "data/maps/HolonResearchTower_2F/scripts.inc" @ holon-maps
	.include "data/maps/HolonLake/scripts.inc" @ holon-maps
	.include "data/maps/OneIsland/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_House1/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_House2/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_Meadow/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_MemorialPillar/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/maps/FiveIsland_RocketWarehouse/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_House1/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_House2/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_IcefallCave_1F/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_IcefallCave_B1F/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_IcefallCave_Back/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_IcefallCave_Entrance/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_LoreleisHouse/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_Mart/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/maps/FourIsland_PokemonDayCare/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_Exterior/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_1F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B1F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B1F_Stairs/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B2F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B2F_Stairs/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B3F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B4F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_RubyPath_B5F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_Summit/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_SummitPath_1F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_SummitPath_2F/scripts.inc" @ sevii-maps
	.include "data/maps/MtEmber_SummitPath_3F/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_House1/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_House2/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_KindleRoad/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_KindleRoad_EmberSpa/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/maps/OneIsland_TreasureBeach/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_House_Room1/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_House_Room2/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_Mart/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_SevaultCanyon/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_SevaultCanyon_Entrance/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_SevaultCanyon_House/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_SevaultCanyon_TanobyKey/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_DilfordChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_LiptooChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_MoneanChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_RixyChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_ScufibChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_ViapoisChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SevenIsland_TanobyRuins_WeepthChamber/scripts.inc" @ sevii-maps
	.include "data/maps/SeviiSeaRouteA/scripts.inc" @ sevii-maps
	.include "data/maps/SeviiSeaRouteB/scripts.inc" @ sevii-maps
	.include "data/maps/SeviiSeaRouteC/scripts.inc" @ sevii-maps
	.include "data/maps/SeviiSeaRouteD/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_DottedHole_1F/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_DottedHole_B1F/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_DottedHole_B2F/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_DottedHole_B3F/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_DottedHole_B4F/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_DottedHole_SapphireRoom/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_House/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_Mart/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_RuinValley/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_WaterPath/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_WaterPath_House1/scripts.inc" @ sevii-maps
	.include "data/maps/SixIsland_WaterPath_House2/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_BerryForest/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_BondBridge/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_DunsparceTunnel/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_House1/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_House2/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_House3/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_House4/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_House5/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_Mart/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/maps/ThreeIsland_Port/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland_CapeBrink/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland_CapeBrink_House/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland_Harbor/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland_House/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland_JoyfulGameCorner/scripts.inc" @ sevii-maps
	.include "data/maps/TwoIsland_PokemonCenter_1F/scripts.inc" @ sevii-maps
	.include "data/scripts/sevii.inc" @ sevii-maps

.if IS_FRLG

@ FRLG scripts

	.include "data/scripts/trainer_tower.inc"
	.include "data/scripts/fame_checker_frlg.inc"
	.include "data/text/fame_checker_frlg.inc"
	.include "data/scripts/item_ball_scripts_frlg.inc"
	.include "data/scripts/silphco_doors.inc"
	.include "data/scripts/move_tutors_frlg.inc"
	.include "data/scripts/cable_club_frlg.inc"
	.include "data/scripts/trainer_card_frlg.inc"
	.include "data/text/trainer_card_frlg.inc"
	.include "data/scripts/mystery_event_club.inc"
	.include "data/scripts/day_care_frlg.inc"
	.include "data/text/day_care_frlg.inc"
	.include "data/scripts/seagallop.inc"
	.include "data/scripts/static_pokemon.inc"
	.include "data/scripts/aide.inc"
	.include "data/scripts/pokemon_mansion.inc"
	.include "data/scripts/pokemon_league.inc"
	.include "data/scripts/route23.inc"
	.include "data/text/new_game_intro_frlg.inc"
	.include "data/scripts/trainers_frlg.inc"
	.include "data/text/trainers_frlg.inc"
	.include "data/text/ingame_trade_frlg.inc"
	.include "data/scripts/flavor_text.inc"
	.include "data/scripts/pkmn_center_nurse_frlg.inc"

.endif

	.include "data/scripts/std_msgbox.inc"
	.include "data/scripts/type_rps.inc"
	.include "data/scripts/trainer_battle.inc"
	.include "data/scripts/new_game.inc"
	.include "data/scripts/hall_of_fame.inc"
	.include "data/scripts/hall_of_fame_frlg.inc"

	.include "data/scripts/config.inc"
	.include "data/scripts/debug.inc"

EventScript_WhiteOut::
	call EverGrandeCity_HallOfFame_EventScript_ResetEliteFour
	goto EventScript_ResetMrBriney
	end

EventScript_AfterWhiteOutHeal::
	lockall
	msgbox gText_FirstShouldRestoreMonsHealth
	call EventScript_PkmnCenterNurse_TakeAndHealPkmn
	call_if_unset FLAG_DEFEATED_RUSTBORO_GYM, EventScript_AfterWhiteOutHealMsgPreFirstBoss
	call_if_set FLAG_DEFEATED_RUSTBORO_GYM, EventScript_AfterWhiteOutHealMsg
	applymovement VAR_LAST_TALKED, Movement_PkmnCenterNurse_Bow
	waitmovement 0
	fadedefaultbgm
	releaseall
	end

EventScript_AfterWhiteOutHealMsgPreFirstBoss::
	msgbox gText_MonsHealedShouldBuyPotions
	return

EventScript_AfterWhiteOutHealMsg::
	msgbox gText_MonsHealed
	return

@ EventScript_AfterWhiteOutMomHeal::
@	lockall
@	textcolor NPC_TEXT_COLOR_FEMALE
@	applymovement LOCALID_PLAYERS_HOUSE_1F_MOM, Common_Movement_WalkInPlaceFasterDown
@	waitmovement 0
@	msgbox gText_HadQuiteAnExperienceTakeRest
@	call Common_EventScript_OutOfCenterPartyHeal
@	msgbox gText_MomExplainHPGetPotions
@	fadedefaultbgm
@	releaseall
@	end

EventScript_ResetMrBriney::
	goto_if_eq VAR_BRINEY_LOCATION, 1, EventScript_MoveMrBrineyToHouse
	goto_if_eq VAR_BRINEY_LOCATION, 2, EventScript_MoveMrBrineyToDewford
	goto_if_eq VAR_BRINEY_LOCATION, 3, EventScript_MoveMrBrineyToRoute109
	end

EventScript_MoveMrBrineyToHouse::
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	clearflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	clearflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	clearflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	end

EventScript_MoveMrBrineyToDewford::
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	clearflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	clearflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	end

EventScript_MoveMrBrineyToRoute109::
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	end

EverGrandeCity_HallOfFame_EventScript_ResetEliteFour::
	clearflag FLAG_DEFEATED_ELITE_4_SIDNEY
	clearflag FLAG_DEFEATED_ELITE_4_PHOEBE
	clearflag FLAG_DEFEATED_ELITE_4_GLACIA
	clearflag FLAG_DEFEATED_ELITE_4_DRAKE
	setvar VAR_ELITE_4_STATE, 0
	return

Common_EventScript_UpdateBrineyLocation::
	goto_if_unset FLAG_RECEIVED_POKENAV, Common_EventScript_NopReturn
	goto_if_set FLAG_DEFEATED_PETALBURG_GYM, Common_EventScript_NopReturn
	goto_if_unset FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT, EventScript_SetBrineyLocation_House
	goto_if_unset FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN, EventScript_SetBrineyLocation_Dewford
	goto_if_unset FLAG_HIDE_ROUTE_109_MR_BRINEY, EventScript_SetBrineyLocation_Route109
	return

EventScript_SetBrineyLocation_House::
	setvar VAR_BRINEY_LOCATION, 1
	return

EventScript_SetBrineyLocation_Dewford::
	setvar VAR_BRINEY_LOCATION, 2
	return

EventScript_SetBrineyLocation_Route109::
	setvar VAR_BRINEY_LOCATION, 3
	return

	.include "data/scripts/pkmn_center_nurse.inc"
	.include "data/scripts/orchid_cafe.inc"
	.include "data/scripts/cynthia.inc"
	.include "data/scripts/obtain_item.inc"
	.include "data/scripts/record_mix.inc"
	.include "data/scripts/pc.inc"
	.include "data/scripts/move_relearner.inc"

@ scripts/notices.inc? signs.inc? See comment about text/notices.inc
Common_EventScript_ShowPokemartSign::
	msgbox gText_PokemartSign, MSGBOX_SIGN
	end

Common_EventScript_ShowPokemonCenterSign::
	msgbox gText_PokemonCenterSign, MSGBOX_SIGN
	end

Common_ShowEasyChatScreen::
	fadescreen FADE_TO_BLACK
	special ShowEasyChatScreen
	fadescreen FADE_FROM_BLACK
	return

Common_EventScript_ReadyPetalburgGymForBattle::
	clearflag FLAG_HIDE_PETALBURG_GYM_GREETER
	setflag FLAG_PETALBURG_MART_EXPANDED_ITEMS
	return

Common_EventScript_BufferTrendyPhrase::
	dotimebasedevents
	setvar VAR_0x8004, 0
	special BufferTrendyPhraseString
	return

EventScript_BackupMrBrineyLocation::
	copyvar VAR_0x8008, VAR_BRINEY_LOCATION
	setvar VAR_BRINEY_LOCATION, 0
	return

	.include "data/scripts/surf.inc"
	.include "data/scripts/rival_graphics.inc"
	.include "data/scripts/set_gym_trainers.inc"

EventScript_CancelMessageBox::
	special UseBlankMessageToCancelPokemonPic
	release
	end

Common_EventScript_ShowBagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	release
	end

Common_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	return

EventScript_BagIsFull::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	msgbox gText_TooBadBagIsFull
	release
	end

Common_EventScript_ShowNoRoomForDecor::
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	release
	end

Common_EventScript_NoRoomForDecor::
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	return

Common_EventScript_SetAbnormalWeather::
	setweather WEATHER_ABNORMAL
	return

Common_EventScript_PlayGymBadgeFanfare::
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	return

Common_EventScript_OutOfCenterPartyHeal::
	fadescreenswapbuffers FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	callnative UpdateFollowingPokemon
	fadescreenswapbuffers FADE_FROM_BLACK
	return

EventScript_RegionMap::
	lockall
	@ msgbox Common_Text_LookCloserAtMap, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	special FieldShowRegionMap
	releaseall
	end

Common_EventScript_PlayBrineysBoatMusic::
	setflag FLAG_DONT_TRANSITION_MUSIC
	playbgm MUS_SAILING, FALSE
	return

Common_EventScript_StopBrineysBoatMusic::
	clearflag FLAG_DONT_TRANSITION_MUSIC
	fadedefaultbgm
	return

	.include "data/scripts/prof_birch.inc"

@ Below could be split as ferry.inc aside from the Rusturf tunnel script
Common_EventScript_FerryDepart::
	delay 60
	applymovement VAR_0x8004, Movement_FerryDepart
	waitmovement 0
	return

Movement_FerryDepart:
	walk_slow_right
	walk_slow_right
	walk_slow_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

EventScript_HideMrBriney::
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	setvar VAR_BRINEY_LOCATION, 0
	return

RusturfTunnel_EventScript_SetRusturfTunnelOpen::
	removeobject LOCALID_RUSTURF_TUNNEL_WANDAS_BF
	removeobject LOCALID_RUSTURF_TUNNEL_WANDA
	clearflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDAS_BOYFRIEND
	clearflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDA
	setvar VAR_RUSTURF_TUNNEL_STATE, 6
	setflag FLAG_RUSTURF_TUNNEL_OPENED
	return

EventScript_UnusedBoardFerry::
	delay 30
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	showplayer
	delay 30
	applymovement LOCALID_PLAYER, Movement_UnusedBoardFerry
	waitmovement 0
	delay 30
	return

Movement_UnusedBoardFerry:
	walk_up
	step_end

Common_EventScript_FerryDepartIsland::
	call_if_eq VAR_FACING, DIR_SOUTH, Ferry_EventScript_DepartIslandSouth
	call_if_eq VAR_FACING, DIR_WEST, Ferry_EventScript_DepartIslandWest
	delay 30
	hideplayer
	call Common_EventScript_FerryDepart
	return

	.include "data/scripts/cave_of_origin.inc"
	.include "data/scripts/kecleon.inc"

Common_EventScript_NameReceivedPartyMon::
	fadescreen FADE_TO_BLACK
	special ChangePokemonNickname
	return

Common_EventScript_PlayerHandedOverTheItem::
	bufferitemname STR_VAR_1, VAR_0x8004
	playfanfare MUS_OBTAIN_TMHM
	message gText_PlayerHandedOverTheItem
	waitmessage
	waitfanfare
	removeitem VAR_0x8004
	return

	.include "data/scripts/elite_four.inc"
	.include "data/scripts/movement.inc"
	.include "data/scripts/check_furniture.inc"
	.include "data/scripts/mart_clerk.inc"
	.include "data/text/record_mix.inc"
	.include "data/text/pc.inc"
	.include "data/text/pkmn_center_nurse.inc"
	.include "data/text/obtain_item.inc"
	.include "data/text/move_relearner.inc"

@ The below and surf.inc could be split into some text/notices.inc
gText_PokemartSign::
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"

gText_PokemonCenterSign::
	.string "“Rejuvenate your tired partners!”\n"
	.string "POKéMON CENTER$"

gText_MomOrDadMightLikeThisProgram::
	.string "{STR_VAR_1} might like this program.\n"
	.string "… … … … … … … … … … … … … … … …\p"
	.string "Better get going!$"

gText_WhichFloorWouldYouLike::
	.string "Welcome to LILYCOVE DEPARTMENT STORE.\p"
	.string "Which floor would you like?$"

gText_SandstormIsVicious::
	.string "The sandstorm is vicious.\n"
	.string "It's impossible to keep going.$"

gText_SelectWithoutRegisteredItem::
	.string "An item in the BAG can be\n"
	.string "registered to SELECT for easy use.$"

gText_PokemonTrainerSchoolEmail::
	.string "There's an e-mail from POKéMON TRAINER\n"
	.string "SCHOOL.\p"
	.string "… … … … … …\p"
	.string "A POKéMON may learn up to four moves.\p"
	.string "A TRAINER's expertise is tested on the\n"
	.string "move sets chosen for POKéMON.\p"
	.string "… … … … … …$"

gText_PlayerHouseBootPC::
	.string "{PLAYER} booted up the PC.$"

gText_PokeblockLinkCanceled::
	.string "The link was canceled.$"

gText_UnusedNicknameReceivedPokemon::
	.string "Want to give a nickname to\n"
	.string "the {STR_VAR_2} you received?$"

gText_PlayerWhitedOut::
	.string "{PLAYER} is out of usable\n"
	.string "POKéMON!\p{PLAYER} whited out!$"

gText_FirstShouldRestoreMonsHealth::
	.string "First, you should restore your\n"
	.string "POKéMON to full health.$"

gText_MonsHealedShouldBuyPotions::
	.string "Your POKéMON have been healed\n"
	.string "to perfect health.\p"
	.string "If your POKéMON's energy, HP,\n"
	.string "is down, please come see us.\p"
	.string "If you're planning to go far in the\n"
	.string "field, you should buy some POTIONS\l"
	.string "at the POKéMON MART.\p"
	.string "We hope you excel!$"

gText_MonsHealed::
	.string "Your POKéMON have been healed\n"
	.string "to perfect health.\p"
	.string "We hope you excel!$"

gText_HadQuiteAnExperienceTakeRest::
	.string "MOM: {PLAYER}!\n"
	.string "Welcome home.\p"
	.string "It sounds like you had quite\n"
	.string "an experience.\p"
	.string "Maybe you should take a quick\n"
	.string "rest.$"

gText_MomExplainHPGetPotions::
	.string "MOM: Oh, good! You and your\n"
	.string "POKéMON are looking great.\p"
	.string "I just heard from {STR_VAR_1}.\p"
	.string "He said that POKéMON's energy is\n"
	.string "measured in HP.\p"
	.string "If your POKéMON lose their HP,\n"
	.string "you can restore them at any\l"
	.string "POKéMON CENTER.\p"
	.string "If you're going to travel far away,\n"
	.string "the smart TRAINER stocks up on\l"
	.string "POTIONS at the POKéMON MART.\p"
	.string "Make me proud, honey!\p"
	.string "Take care!$"

gText_RegisteredTrainerinPokeNav::
	.string "Registered {STR_VAR_1} {STR_VAR_2}\n"
	.string "in the POKéNAV.$"

gText_ComeBackWithSecretPower::
	.string "Do you know the TM SECRET POWER?\p"
	.string "Our group, we love the TM SECRET\n"
	.string "POWER.\p"
	.string "One of our members will give it to you.\n"
	.string "Come back and show me if you get it.\p"
	.string "We'll accept you as a member and sell\n"
	.string "you good stuff in secrecy.$"

gText_PokerusExplanation::
	.string "Your POKéMON may be infected with\n"
	.string "POKéRUS.\p"
	.string "Little is known about the POKéRUS\n"
	.string "except that they are microscopic life-\l"
	.string "forms that attach to POKéMON.\p"
	.string "While infected, POKéMON are said to\n"
	.string "grow exceptionally well.$"

	.include "data/text/surf.inc"

gText_DoorOpenedFarAway::
	.string "It sounded as if a door opened\n"
	.string "somewhere far away.$"

gText_BigHoleInTheWall::
	.string "There is a big hole in the wall.$"

gText_SorryWirelessClubAdjustments::
	.string "I'm terribly sorry.\n"
	.string "The POKéMON WIRELESS CLUB is\l"
	.string "undergoing adjustments now.$"

gText_UndergoingAdjustments::
	.string "It appears to be undergoing\n"
	.string "adjustments…$"

@ Unused
gText_SorryTradeCenterInspections::
	.string "I'm terribly sorry. The TRADE CENTER\n"
	.string "is undergoing inspections.$"

@ Unused
gText_SorryRecordCornerPreparation::
	.string "I'm terribly sorry. The RECORD CORNER\n"
	.string "is under preparation.$"

gText_PlayerHandedOverTheItem::
	.string "{PLAYER} handed over the\n"
	.string "{STR_VAR_1}.$"

gText_ThankYouForAccessingMysteryGift::
	.string "Thank you for accessing the\n"
	.string "MYSTERY GIFT System.$"

gText_PlayerFoundOneTMHM::
	.string "{PLAYER} found one {STR_VAR_1}\n"
	.string "{STR_VAR_2}!$"

gText_PlayerFoundTMHMs::
	.string "{PLAYER} found {STR_VAR_3} {STR_VAR_1}\n"
	.string "{STR_VAR_2}!$"

gText_Sudowoodo_Attacked::
	.string "The weird tree doesn't like the\n"
	.string "WAILMER PAIL!\p"
	.string "The weird tree attacked!$"

gText_LegendaryFlewAway::
	.string "The {STR_VAR_1} flew away!$"

gText_WantWhichFloor::
	.string "Which floor do you want?$"

	.include "data/text/pc_transfer.inc"
	.include "data/text/questionnaire.inc"
	.include "data/text/abnormal_weather.inc"

EventScript_GetInGameTradeSpeciesInfo::
	copyvar VAR_0x8005, VAR_0x8008
	specialvar VAR_0x8009, GetInGameTradeSpeciesInfo
	return

EventScript_ChooseMonForInGameTrade::
	special ChoosePartyMon
	lock
	faceplayer
	return

EventScript_GetInGameTradeSpecies::
	specialvar VAR_RESULT, GetTradeSpecies
	return

EventScript_DoInGameTrade::
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	lock
	faceplayer
	return

EventScript_SelectWithoutRegisteredItem::
	msgbox gText_SelectWithoutRegisteredItem, MSGBOX_SIGN
	end

	.include "data/scripts/field_poison.inc"

Common_EventScript_NopReturn::
	return

EventScript_SetResultTrue::
	setvar VAR_RESULT, TRUE
	return

EventScript_SetResultFalse::
	setvar VAR_RESULT, FALSE
	return

EventScript_GetElevatorFloor::
	special GetElevatorFloor
	return

@ Unused
EventScript_CableClub_SetVarResult1::
	setvar VAR_RESULT, 1
	return

EventScript_CableClub_SetVarResult0::
	setvar VAR_RESULT, 0
	return

Common_EventScript_UnionRoomAttendant::
#if IS_FRLG
	call CableClub_EventScript_UnionRoomAttendant_Frlg
#else
	call CableClub_EventScript_UnionRoomAttendant
#endif
	end

Common_EventScript_WirelessClubAttendant::
#if IS_FRLG
	call CableClub_EventScript_WirelessClubAttendant_Frlg
#else
	call CableClub_EventScript_WirelessClubAttendant
#endif
	end

Common_EventScript_DirectCornerAttendant::
#if IS_FRLG
	call CableClub_EventScript_DirectCornerAttendant_Frlg
#else
	call CableClub_EventScript_DirectCornerAttendant
#endif
	end

Common_EventScript_RemoveStaticPokemon::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

Common_EventScript_LegendaryFlewAway::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	bufferspeciesname STR_VAR_1, VAR_0x8004
	msgbox gText_LegendaryFlewAway, MSGBOX_DEFAULT
	release
	end

EventScript_VsSeekerChargingDone::
	special VsSeekerFreezeObjectsAfterChargeComplete
	waitstate
	special VsSeekerResetObjectMovementAfterChargeComplete
	releaseall
	end

@ FRLG scripts

EventScript_SetExitingCyclingRoad::
	lockall
	clearflag FLAG_SYS_ON_CYCLING_ROAD
	setvar VAR_MAP_SCENE_ROUTE16, 0
	releaseall
	end

EventScript_SetEnteringCyclingRoad::
	lockall
	setvar VAR_MAP_SCENE_ROUTE16, 1
	releaseall
	end

EventScript_TryDarkenRuins::
	goto_if_set FLAG_SYS_UNLOCKED_TANOBY_RUINS, Common_EventScript_NopReturn
	setweather WEATHER_SHADE
	doweather
	return

Text_MonFlewAway::
	.string "The {STR_VAR_1} flew away!$"

@ Call for legendary bird trio
Text_Gyaoo::
	.string "Gyaoo!$"

EventScript_BrailleCursorWaitButton::
	special BrailleCursorToggle
	waitbuttonpress
	closebraillemessage
	playse SE_SELECT
	setvar VAR_0x8006, 1
	special BrailleCursorToggle
	return

EventScript_PalletTown_PlayersHouse_2F_ShutDownPC::
	setvar VAR_0x8004, PC_LOCATION_PLAYER_HOUSE_FRLG
	playse SE_PC_OFF
	special DoPCTurnOffEffect
	releaseall
	end

EventScript_PalletTown_PlayersHouse_2F_TurnOnPC::
	lockall
	setvar VAR_0x8004, PC_LOCATION_PLAYER_HOUSE_FRLG
	special DoPCTurnOnEffect
	playse SE_PC_ON
	msgbox gText_PlayerHouseBootPC
	special BedroomPC
	releaseall
	end


	.include "data/scripts/pc_transfer.inc"
	.include "data/scripts/questionnaire.inc"
	.include "data/scripts/abnormal_weather.inc"
	.include "data/scripts/trainer_script.inc"
	.include "data/scripts/berry_tree.inc"
	.include "data/scripts/secret_base.inc"
	.include "data/scripts/cable_club.inc"
	.include "data/text/cable_club.inc"
	.include "data/scripts/contest_hall.inc"
	.include "data/scripts/tv.inc"
	.include "data/text/tv.inc"
	.include "data/scripts/interview.inc"
	.include "data/scripts/gabby_and_ty.inc"
	.include "data/text/pokemon_news.inc"
	.include "data/scripts/mauville_man.inc"
	.include "data/scripts/field_move_scripts.inc"
	.include "data/scripts/item_ball_scripts.inc"
	.include "data/scripts/profile_man.inc"
	.include "data/scripts/day_care.inc"
	.include "data/scripts/flash.inc"
	.include "data/scripts/players_house.inc"
	.include "data/scripts/berry_blender.inc"
	.include "data/text/mauville_man.inc"
	.include "data/text/trainers.inc"
	.include "data/scripts/repel.inc"
	.include "data/scripts/safari_zone.inc"
	.include "data/scripts/roulette.inc"
	.include "data/scripts/pokedex_rating.inc"
	.include "data/text/pokedex_rating.inc"
	.include "data/text/lottery_corner.inc"
	.include "data/text/event_ticket_1.inc"
	.include "data/text/braille.inc"
	.include "data/text/berries.inc"
	.include "data/text/shoal_cave.inc"
	.include "data/text/check_furniture.inc"
	.include "data/scripts/cave_hole.inc"
	.include "data/scripts/lilycove_lady.inc"
	.include "data/text/match_call.inc"
	.include "data/scripts/apprentice.inc"
	.include "data/text/apprentice.inc"
	.include "data/scripts/battle_pike.inc"
	.include "data/text/blend_master.inc"
	.include "data/text/battle_tent.inc"
	.include "data/text/event_ticket_2.inc"
	.include "data/text/move_tutors.inc"
	.include "data/scripts/move_tutors.inc"
	.include "data/scripts/trainer_hill.inc"
	.include "data/scripts/test_signpost.inc"
	.include "data/scripts/follower.inc"
	.include "data/text/save.inc"
	.include "data/text/birch_speech.inc"
	.include "data/scripts/dexnav.inc"
	.include "data/scripts/battle_frontier.inc"
	.include "data/scripts/apricorn_tree.inc"
	.include "data/scripts/wild_encounter.inc"
	.include "data/scripts/train.inc"
	.include "data/scripts/voyages.inc"
	.include "data/scripts/deleted_hoenn_stubs.inc"
