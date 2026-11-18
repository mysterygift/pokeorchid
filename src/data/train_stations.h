// Tosa Rail station table. Indexed by TRAIN_STATION_* (include/constants/train_stations.h).
//
//   name         shown on the station map / confirm prompt
//   mapGroup/Num the map the platform is on
//   trackX/Y     map tile (no MAP_OFFSET) where the boarding door stops on arrival. The player
//                is warped onto this tile hidden, then steps one tile south onto the platform.
//                When departing, the train's door lines up with the player's column and the player
//                walks north until reaching trackY.
//   visitedFlag  FLAG_VISITED_* of the town (0 = none). Visiting makes the station accessible.
//   unlockFlag   script override: accessible even if never visited (settrainstation ..., TRAIN_ACCESS_OPEN)
//   closedFlag   script override: greyed out even if visited (settrainstation ..., TRAIN_ACCESS_CLOSED)
//   (station map positions and lines live in dev_scripts/train_ui/network.json → src/data/train_station_map.h)

static const u8 sStationName_TosaPort[]  = _("TOSA PORT");
static const u8 sStationName_TestEast[]  = _("EAST TEST");
static const u8 sStationName_TestNorth[] = _("NORTH TEST");

static const struct TrainStation sTrainStations[TRAIN_STATION_COUNT] =
{
    // Platform under the Tosa Port gatehouse (MAP_TOSA_PORT_BRENDANS_HOUSE_2F, lifts from _1F)
    [TRAIN_STATION_TOSA_PORT] =
    {
        .name = sStationName_TosaPort,
        .mapGroup = MAP_GROUP(MAP_TOSA_PORT_BRENDANS_HOUSE_2F),
        .mapNum = MAP_NUM(MAP_TOSA_PORT_BRENDANS_HOUSE_2F),
        .trackX = 9,
        .trackY = 4,
        .visitedFlag = FLAG_VISITED_TOSA_PORT,
        .unlockFlag = FLAG_TRAIN_UNLOCK_TOSA_PORT,
        .closedFlag = FLAG_TRAIN_CLOSED_TOSA_PORT,
    },
    [TRAIN_STATION_TEST_EAST] =
    {
        .name = sStationName_TestEast,
        .mapGroup = MAP_GROUP(MAP_TRAIN_TEST_EAST),
        .mapNum = MAP_NUM(MAP_TRAIN_TEST_EAST),
        .trackX = 9,
        .trackY = 4,
        .visitedFlag = 0,
        .unlockFlag = FLAG_TRAIN_UNLOCK_TEST_EAST,
        .closedFlag = FLAG_TRAIN_CLOSED_TEST_EAST,
    },
    [TRAIN_STATION_TEST_NORTH] =
    {
        .name = sStationName_TestNorth,
        .mapGroup = MAP_GROUP(MAP_TRAIN_TEST_NORTH),
        .mapNum = MAP_NUM(MAP_TRAIN_TEST_NORTH),
        .trackX = 9,
        .trackY = 4,
        .visitedFlag = 0,
        .unlockFlag = FLAG_TRAIN_UNLOCK_TEST_NORTH,
        .closedFlag = FLAG_TRAIN_CLOSED_TEST_NORTH,
    },
};
