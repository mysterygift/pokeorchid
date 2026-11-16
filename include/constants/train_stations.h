#ifndef GUARD_CONSTANTS_TRAIN_STATIONS_H
#define GUARD_CONSTANTS_TRAIN_STATIONS_H

// Tosa Rail stations. Order = order in src/data/train_stations.h.
// Adding a station: add an id here, a row in src/data/train_stations.h, and a pair of
// FLAG_TRAIN_UNLOCK_* / FLAG_TRAIN_CLOSED_* flags in include/constants/flags.h.
#define TRAIN_STATION_TEST_WEST     0
#define TRAIN_STATION_TEST_EAST     1
#define TRAIN_STATION_TEST_NORTH    2
#define TRAIN_STATION_COUNT         3

#define TRAIN_STATION_NONE          0xFF

// settrainstation modes
#define TRAIN_ACCESS_LOCKED         0   // back to default: accessible only once its town is visited
#define TRAIN_ACCESS_OPEN           1   // accessible now, even if never visited (and not closed)
#define TRAIN_ACCESS_CLOSED         2   // greyed out as "closed" even if visited

// Station states, as shown on the station map
#define TRAIN_STATION_STATE_UNVISITED   0
#define TRAIN_STATION_STATE_OPEN        1
#define TRAIN_STATION_STATE_CLOSED      2

#endif // GUARD_CONSTANTS_TRAIN_STATIONS_H
