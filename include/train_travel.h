#ifndef GUARD_TRAIN_TRAVEL_H
#define GUARD_TRAIN_TRAVEL_H

#include "constants/train_stations.h"

struct TrainStation
{
    const u8 *name;
    u8 mapGroup;
    u8 mapNum;
    u8 trackX;      // door tile on arrival (map coords, no MAP_OFFSET)
    u8 trackY;
    u16 visitedFlag;
    u16 unlockFlag;
    u16 closedFlag;
};

const struct TrainStation *GetTrainStation(u32 stationId);
u32 GetCurrentTrainStation(void);
bool32 IsTrainStationAccessible(u32 stationId);
bool32 IsTrainStationVisited(u32 stationId);
u32 GetTrainStationState(u32 stationId);
void SetTrainStationAccess(u32 stationId, u32 mode);

// Specials (data/specials.inc)
void TrainStation_SetAccess(void);
void TrainStation_CountDestinations(void);
void TrainStation_BufferName(void);
void TrainTravel_Depart(void);
void TrainTravel_SpawnParkedTrain(void);
void TrainStation_OpenMap(void);

#endif // GUARD_TRAIN_TRAVEL_H
