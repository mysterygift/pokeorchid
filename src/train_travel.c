// Tosa Rail: station access rules and the train journey cutscene.
//
// Script side (data/scripts/train.inc):
//   usetrain                         -> pick a destination, board, travel, arrive
//   settrainstation STATION, MODE    -> TRAIN_ACCESS_OPEN / _CLOSED / _LOCKED
//
// Journey:
//   Depart  (Task_TrainDepart, started by special TrainTravel_Depart with VAR_0x8004 = station)
//     train is waiting with its door on the player's column (or, with VAR_0x8005 = TRUE, pulls in
//     from the left first) -> door opens ->
//     player walks north into the door and vanishes -> door closes -> train pulls out to the right
//     (camera stays put) -> fade to black -> warp to the destination's track tile.
//   Arrive  (FieldCB_TrainArrive -> Task_TrainArrive)
//     fade in on an empty platform with the player hidden on the track tile -> train pulls in from
//     the left -> door opens -> player steps south onto the platform -> door closes -> train leaves.
//
// The train is one sprite built from 64x64 subsprites so it can be wider than a single OBJ.
// Its position is anchored to the map (coordOffsetEnabled), and movement is done with x2.

#include "global.h"
#include "train_travel.h"
#include "decompress.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_screen_effect.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "malloc.h"
#include "overworld.h"
#include "palette.h"
#include "script.h"
#include "script_menu.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "strings.h"
#include "task.h"
#include "constants/event_object_movement.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/songs.h"

#include "data/train_stations.h"

// ---------------------------------------------------------------------------------------------
// Train graphics + geometry. graphics/train/train.png is a 64-px-wide sheet of 64x64 pieces
// stacked vertically (so each piece's tiles are contiguous):
//   0 = rear carriage, 1 = boarding carriage (door shut), 2 = locomotive,
//   3 = boarding carriage with the door open.
// The train faces right (locomotive leads when travelling left -> right).
// ---------------------------------------------------------------------------------------------

#define TAG_TRAIN               0x5A70

#define TRAIN_PIECE_SIZE        64
#define TRAIN_PIECE_TILES       ((TRAIN_PIECE_SIZE / 8) * (TRAIN_PIECE_SIZE / 8))
#define TRAIN_NUM_PIECES        3
#define TRAIN_NUM_PIECE_GFX     4
#define TRAIN_LENGTH            (TRAIN_PIECE_SIZE * TRAIN_NUM_PIECES)

// Boarding door: left edge in pixels from the train's left edge, and its width.
#define TRAIN_DOOR_X            (TRAIN_PIECE_SIZE + 24)
#define TRAIN_DOOR_WIDTH        16
// Pixels between the bottom of the 64x64 pieces and the bottom of the track tile
// (positive = train art sits lower than the tile's bottom edge).
#define TRAIN_BOTTOM_DROP       0

// Timings (frames). Mirrors dev_scripts/train_ui storyboard.
#define TRAIN_ARRIVE_FRAMES     96
#define TRAIN_DEPART_FRAMES     80
#define TRAIN_DOOR_FRAMES       12
#define TRAIN_SETTLE_FRAMES     16

static const u32 sTrain_Gfx[] = INCBIN_U32("graphics/train/train.4bpp.smol");
static const u16 sTrain_Pal[] = INCBIN_U16("graphics/train/train.gbapal");

static const struct CompressedSpriteSheet sTrainSpriteSheet =
{
    .data = sTrain_Gfx,
    .size = TRAIN_PIECE_TILES * TRAIN_NUM_PIECE_GFX * TILE_SIZE_4BPP,
    .tag = TAG_TRAIN,
};

static const struct SpritePalette sTrainSpritePalette =
{
    .data = sTrain_Pal,
    .tag = TAG_TRAIN,
};

static const struct OamData sTrainOam =
{
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 2,
};

// Subsprite x/y are relative to the sprite's centre (the 64x64 "main" OBJ is centred on x/y).
#define TRAIN_PIECE(i, gfx)                                     \
{                                                               \
    .x = -TRAIN_PIECE_SIZE / 2 + (i) * TRAIN_PIECE_SIZE,        \
    .y = -TRAIN_PIECE_SIZE / 2,                                 \
    .shape = SPRITE_SHAPE(64x64),                               \
    .size = SPRITE_SIZE(64x64),                                 \
    .tileOffset = (gfx) * TRAIN_PIECE_TILES,                    \
    .priority = 2,                                              \
}

static const struct Subsprite sTrainSubsprites_DoorShut[] =
{
    TRAIN_PIECE(0, 0),
    TRAIN_PIECE(1, 1),
    TRAIN_PIECE(2, 2),
};

static const struct Subsprite sTrainSubsprites_DoorOpen[] =
{
    TRAIN_PIECE(0, 0),
    TRAIN_PIECE(1, 3),
    TRAIN_PIECE(2, 2),
};

enum { TRAIN_DOOR_SHUT, TRAIN_DOOR_OPEN };

static const struct SubspriteTable sTrainSubspriteTables[] =
{
    [TRAIN_DOOR_SHUT] = { ARRAY_COUNT(sTrainSubsprites_DoorShut), sTrainSubsprites_DoorShut },
    [TRAIN_DOOR_OPEN] = { ARRAY_COUNT(sTrainSubsprites_DoorOpen), sTrainSubsprites_DoorOpen },
};

static const struct SpriteTemplate sTrainSpriteTemplate =
{
    .tileTag = TAG_TRAIN,
    .paletteTag = TAG_TRAIN,
    .oam = &sTrainOam,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

// ---------------------------------------------------------------------------------------------
// Station access
// ---------------------------------------------------------------------------------------------

const struct TrainStation *GetTrainStation(u32 stationId)
{
    if (stationId >= TRAIN_STATION_COUNT)
        return NULL;
    return &sTrainStations[stationId];
}

u32 GetCurrentTrainStation(void)
{
    u32 i;
    for (i = 0; i < TRAIN_STATION_COUNT; i++)
    {
        if (sTrainStations[i].mapGroup == gSaveBlock1Ptr->location.mapGroup
         && sTrainStations[i].mapNum == gSaveBlock1Ptr->location.mapNum)
            return i;
    }
    return TRAIN_STATION_NONE;
}

bool32 IsTrainStationVisited(u32 stationId)
{
    const struct TrainStation *st = GetTrainStation(stationId);
    if (st == NULL)
        return FALSE;
    return (st->visitedFlag != 0 && FlagGet(st->visitedFlag))
        || (st->unlockFlag != 0 && FlagGet(st->unlockFlag));
}

u32 GetTrainStationState(u32 stationId)
{
    const struct TrainStation *st = GetTrainStation(stationId);
    if (st == NULL)
        return TRAIN_STATION_STATE_UNVISITED;
    if (st->closedFlag != 0 && FlagGet(st->closedFlag))
        return TRAIN_STATION_STATE_CLOSED;
    if (IsTrainStationVisited(stationId))
        return TRAIN_STATION_STATE_OPEN;
    return TRAIN_STATION_STATE_UNVISITED;
}

bool32 IsTrainStationAccessible(u32 stationId)
{
    return GetTrainStationState(stationId) == TRAIN_STATION_STATE_OPEN;
}

void SetTrainStationAccess(u32 stationId, u32 mode)
{
    const struct TrainStation *st = GetTrainStation(stationId);
    if (st == NULL)
        return;

    switch (mode)
    {
    case TRAIN_ACCESS_OPEN:
        if (st->unlockFlag)
            FlagSet(st->unlockFlag);
        if (st->closedFlag)
            FlagClear(st->closedFlag);
        break;
    case TRAIN_ACCESS_CLOSED:
        if (st->closedFlag)
            FlagSet(st->closedFlag);
        break;
    case TRAIN_ACCESS_LOCKED:
        if (st->unlockFlag)
            FlagClear(st->unlockFlag);
        if (st->closedFlag)
            FlagClear(st->closedFlag);
        break;
    }
}

static void MarkTrainStationVisited(u32 stationId)
{
    const struct TrainStation *st = GetTrainStation(stationId);
    if (st != NULL && st->unlockFlag)
        FlagSet(st->unlockFlag);
}

// special: VAR_0x8004 = station, VAR_0x8005 = TRAIN_ACCESS_*
void TrainStation_SetAccess(void)
{
    SetTrainStationAccess(gSpecialVar_0x8004, gSpecialVar_0x8005);
}

// special: STR_VAR_1 = name of station VAR_0x8004
void TrainStation_BufferName(void)
{
    const struct TrainStation *st = GetTrainStation(gSpecialVar_0x8004);
    StringCopy(gStringVar1, st != NULL ? st->name : gText_EmptyString2);
}

// special: VAR_RESULT = number of stations you can travel to from here (also marks this
// station as visited).
void TrainStation_CountDestinations(void)
{
    u32 i, count = 0;
    u32 here = GetCurrentTrainStation();

    if (here != TRAIN_STATION_NONE)
        MarkTrainStationVisited(here);
    for (i = 0; i < TRAIN_STATION_COUNT; i++)
        if (i != here && IsTrainStationAccessible(i))
            count++;
    gSpecialVar_Result = count;
}

// ---------------------------------------------------------------------------------------------
// Train sprite
// ---------------------------------------------------------------------------------------------

// Creates the train parked with its door centred on map tile (x, y) (MAP_OFFSET coords).
// Returns the sprite id, or MAX_SPRITES on failure.
static u8 CreateTrainSprite(s16 x, s16 y)
{
    u8 spriteId;
    s16 sx = x, sy = y;
    struct Sprite *sprite;

    LoadCompressedSpriteSheet(&sTrainSpriteSheet);
    LoadSpritePalette(&sTrainSpritePalette);
    UpdateSpritePaletteWithWeather(IndexOfSpritePaletteTag(TAG_TRAIN), FALSE);

    // Tile centre in sprite space
    SetSpritePosToOffsetMapCoords(&sx, &sy, 8, 8);
    // Door centre on the tile centre -> train left edge -> sprite centre (first piece's centre)
    sx = sx - TRAIN_DOOR_X - TRAIN_DOOR_WIDTH / 2 + TRAIN_PIECE_SIZE / 2;
    // Piece bottoms on the tile's bottom edge
    sy = sy + 8 + TRAIN_BOTTOM_DROP - TRAIN_PIECE_SIZE / 2;

    spriteId = CreateSprite(&sTrainSpriteTemplate, sx, sy, 0xFF);
    if (spriteId == MAX_SPRITES)
        return MAX_SPRITES;

    sprite = &gSprites[spriteId];
    sprite->coordOffsetEnabled = TRUE;
    sprite->subpriority = 0xFF; // behind people on the same priority
    SetSubspriteTables(sprite, sTrainSubspriteTables);
    sprite->subspriteTableNum = TRAIN_DOOR_SHUT;
    sprite->subspriteMode = SUBSPRITES_ON;
    return spriteId;
}

static void DestroyTrainSprite(u8 spriteId)
{
    if (spriteId < MAX_SPRITES && gSprites[spriteId].inUse)
        DestroySprite(&gSprites[spriteId]);
    FreeSpriteTilesByTag(TAG_TRAIN);
    FreeSpritePaletteByTag(TAG_TRAIN);
}

static inline s32 TrainScreenLeft(struct Sprite *sprite)
{
    return sprite->x - TRAIN_PIECE_SIZE / 2 + gSpriteCoordOffsetX;
}

// x2 to start from so the whole train is just off the left edge of the screen
static s16 TrainOffscreenLeftX2(struct Sprite *sprite)
{
    return -(TrainScreenLeft(sprite) + TRAIN_LENGTH + 8);
}

// x2 at which the whole train is just past the right edge of the screen
static s16 TrainOffscreenRightX2(struct Sprite *sprite)
{
    return DISPLAY_WIDTH + 8 - TrainScreenLeft(sprite);
}

// Ease-out: fast at t=0, stopped at t=n
static s16 EaseOut(s32 from, s32 to, s32 t, s32 n)
{
    s32 r = n - t;
    return to - ((to - from) * r * r) / (n * n);
}

// Ease-in: stopped at t=0, fast at t=n
static s16 EaseIn(s32 from, s32 to, s32 t, s32 n)
{
    return from + ((to - from) * t * t) / (n * n);
}

// ---------------------------------------------------------------------------------------------
// Departure
// ---------------------------------------------------------------------------------------------

#define tState      data[0]
#define tTimer      data[1]
#define tSpriteId   data[2]
#define tSteps      data[3]
#define tStation    data[4]
#define tFrom       data[5]
#define tTo         data[6]

enum
{
    DEPART_TRAIN_ARRIVES,
    DEPART_DOOR_OPENS,
    DEPART_START_STEP,
    DEPART_WAIT_STEP,
    DEPART_DOOR_CLOSES,
    DEPART_TRAIN_LEAVES,
    DEPART_FADE,
    DEPART_WARP,
};

static void Task_TrainDepart(u8 taskId);
static void FieldCB_TrainArrive(void);

// special: VAR_0x8004 = destination station. Called from a locked script followed by waitstate;
// the script never resumes (the warp reloads the field).
// Track row the player boards through: the current station's track row, or the tile directly
// north of the player if this map isn't a station. Returns the number of steps north.
static s16 GetBoardingTrackY(s16 *steps)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    u32 here = GetCurrentTrainStation();
    s16 trackY;

    if (here != TRAIN_STATION_NONE)
        trackY = sTrainStations[here].trackY + MAP_OFFSET;
    else
        trackY = player->currentCoords.y - 1;

    *steps = player->currentCoords.y - trackY;
    if (*steps < 1)
    {
        *steps = 1;
        trackY = player->currentCoords.y - 1;
    }
    return trackY;
}

// The train parked at the platform while the station map was open (see FieldCB_ReturnFromTrainMap).
static EWRAM_DATA u8 sParkedTrainSpriteId = 0;
static EWRAM_DATA bool8 sHasParkedTrain = FALSE;

void TrainTravel_SpawnParkedTrain(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 steps;
    s16 trackY = GetBoardingTrackY(&steps);

    sParkedTrainSpriteId = CreateTrainSprite(player->currentCoords.x, trackY);
    sHasParkedTrain = (sParkedTrainSpriteId != MAX_SPRITES);
}

static u8 TakeParkedTrain(void)
{
    u8 spriteId = MAX_SPRITES;
    if (sHasParkedTrain && gSprites[sParkedTrainSpriteId].inUse
     && gSprites[sParkedTrainSpriteId].template->tileTag == TAG_TRAIN)
        spriteId = sParkedTrainSpriteId;
    sHasParkedTrain = FALSE;
    return spriteId;
}

// special: VAR_0x8004 = destination station. Called from a locked script followed by waitstate;
// the script never resumes (the warp reloads the field).
void TrainTravel_Depart(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s16 steps;
    s16 trackY = GetBoardingTrackY(&steps);
    u8 taskId = CreateTask(Task_TrainDepart, 10);
    struct Task *task = &gTasks[taskId];

    task->tSteps = steps;
    task->tStation = gSpecialVar_0x8004;
    task->tTimer = 0;
    task->tSpriteId = TakeParkedTrain();
    if (task->tSpriteId == MAX_SPRITES)
        task->tSpriteId = CreateTrainSprite(player->currentCoords.x, trackY);

    if (task->tSpriteId != MAX_SPRITES && gSpecialVar_0x8005)
    {
        // VAR_0x8005 = TRUE: the train pulls in first (for story moments).
        struct Sprite *sprite = &gSprites[task->tSpriteId];
        task->tFrom = TrainOffscreenLeftX2(sprite);
        task->tTo = 0;
        sprite->x2 = task->tFrom;
        task->tState = DEPART_TRAIN_ARRIVES;
        PlaySE(SE_TRUCK_MOVE);
    }
    else
    {
        // Default: the train is already waiting at the platform.
        task->tState = task->tSpriteId != MAX_SPRITES ? DEPART_DOOR_OPENS : DEPART_START_STEP;
    }
}

static void Task_TrainDepart(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    struct Sprite *train = task->tSpriteId != MAX_SPRITES ? &gSprites[task->tSpriteId] : NULL;
    const struct TrainStation *dest;

    switch (task->tState)
    {
    case DEPART_TRAIN_ARRIVES:
        if (train == NULL)
        {
            task->tState = DEPART_START_STEP;
            break;
        }
        train->x2 = EaseOut(task->tFrom, task->tTo, ++task->tTimer, TRAIN_ARRIVE_FRAMES);
        if (task->tTimer >= TRAIN_ARRIVE_FRAMES)
        {
            PlaySE(SE_TRUCK_STOP);
            task->tTimer = 0;
            task->tState = DEPART_DOOR_OPENS;
        }
        break;
    case DEPART_DOOR_OPENS:
        if (++task->tTimer == TRAIN_SETTLE_FRAMES)
        {
            PlaySE(SE_TRUCK_DOOR);
            train->subspriteTableNum = TRAIN_DOOR_OPEN;
        }
        else if (task->tTimer >= TRAIN_SETTLE_FRAMES + TRAIN_DOOR_FRAMES)
        {
            task->tTimer = 0;
            task->tState = DEPART_START_STEP;
        }
        break;
    case DEPART_START_STEP:
        UnfreezeObjectEvent(player);
        ObjectEventClearHeldMovementIfActive(player);
        ObjectEventSetHeldMovement(player, MOVEMENT_ACTION_WALK_NORMAL_UP);
        task->tState = DEPART_WAIT_STEP;
        break;
    case DEPART_WAIT_STEP:
        if (ObjectEventClearHeldMovementIfFinished(player))
        {
            if (--task->tSteps > 0)
            {
                task->tState = DEPART_START_STEP;
            }
            else
            {
                player->invisible = TRUE;
                task->tTimer = 0;
                task->tState = DEPART_DOOR_CLOSES;
            }
        }
        break;
    case DEPART_DOOR_CLOSES:
        if (train == NULL)
        {
            task->tState = DEPART_FADE;
            break;
        }
        if (++task->tTimer == TRAIN_DOOR_FRAMES)
        {
            PlaySE(SE_TRUCK_DOOR);
            train->subspriteTableNum = TRAIN_DOOR_SHUT;
        }
        else if (task->tTimer >= TRAIN_DOOR_FRAMES + TRAIN_SETTLE_FRAMES)
        {
            PlaySE(SE_TRUCK_MOVE);
            task->tTimer = 0;
            task->tFrom = 0;
            task->tTo = TrainOffscreenRightX2(train);
            task->tState = DEPART_TRAIN_LEAVES;
        }
        break;
    case DEPART_TRAIN_LEAVES:
        train->x2 = EaseIn(task->tFrom, task->tTo, ++task->tTimer, TRAIN_DEPART_FRAMES);
        if (task->tTimer >= TRAIN_DEPART_FRAMES)
        {
            train->invisible = TRUE;
            task->tState = DEPART_FADE;
        }
        break;
    case DEPART_FADE:
        dest = GetTrainStation(task->tStation);
        if (dest == NULL)
        {
            // Bad destination: put everything back and give control back.
            player->invisible = FALSE;
            DestroyTrainSprite(task->tSpriteId);
            ScriptContext_Enable();
            DestroyTask(taskId);
            break;
        }
        MarkTrainStationVisited(task->tStation);
        SetWarpDestination(dest->mapGroup, dest->mapNum, WARP_ID_NONE, dest->trackX, dest->trackY);
        TryFadeOutOldMapMusic();
        WarpFadeOutScreen();
        task->tState = DEPART_WARP;
        break;
    case DEPART_WARP:
        if (!gPaletteFade.active && BGMusicStopped())
        {
            WarpIntoMap();
            gFieldCallback = FieldCB_TrainArrive;
            SetMainCallback2(CB2_LoadMap);
            DestroyTask(taskId);
        }
        break;
    }
}

// ---------------------------------------------------------------------------------------------
// Arrival
// ---------------------------------------------------------------------------------------------

enum
{
    ARRIVE_WAIT_FADE,
    ARRIVE_TRAIN_ARRIVES,
    ARRIVE_DOOR_OPENS,
    ARRIVE_PLAYER_STEPS_OUT,
    ARRIVE_WAIT_STEP,
    ARRIVE_DOOR_CLOSES,
    ARRIVE_TRAIN_LEAVES,
    ARRIVE_END,
};

static void Task_TrainArrive(u8 taskId);

static void FieldCB_TrainArrive(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    u8 taskId;

    Overworld_PlaySpecialMapMusic();
    player->invisible = TRUE;
    ObjectEventTurn(player, DIR_SOUTH);
    LockPlayerFieldControls();
    FreezeObjectEvents();
    FadeInFromBlack();

    taskId = CreateTask(Task_TrainArrive, 10);
    gTasks[taskId].tSpriteId = CreateTrainSprite(player->currentCoords.x, player->currentCoords.y);
    if (gTasks[taskId].tSpriteId != MAX_SPRITES)
    {
        struct Sprite *train = &gSprites[gTasks[taskId].tSpriteId];
        gTasks[taskId].tFrom = TrainOffscreenLeftX2(train);
        gTasks[taskId].tTo = 0;
        train->x2 = gTasks[taskId].tFrom;
    }
    gFieldCallback = NULL;
}

static void Task_TrainArrive(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    struct Sprite *train = task->tSpriteId != MAX_SPRITES ? &gSprites[task->tSpriteId] : NULL;

    switch (task->tState)
    {
    case ARRIVE_WAIT_FADE:
        if (IsWeatherNotFadingIn())
        {
            PlaySE(SE_TRUCK_MOVE);
            task->tTimer = 0;
            task->tState = train != NULL ? ARRIVE_TRAIN_ARRIVES : ARRIVE_PLAYER_STEPS_OUT;
        }
        break;
    case ARRIVE_TRAIN_ARRIVES:
        train->x2 = EaseOut(task->tFrom, task->tTo, ++task->tTimer, TRAIN_ARRIVE_FRAMES);
        if (task->tTimer >= TRAIN_ARRIVE_FRAMES)
        {
            PlaySE(SE_TRUCK_STOP);
            task->tTimer = 0;
            task->tState = ARRIVE_DOOR_OPENS;
        }
        break;
    case ARRIVE_DOOR_OPENS:
        if (++task->tTimer == TRAIN_SETTLE_FRAMES)
        {
            PlaySE(SE_TRUCK_DOOR);
            train->subspriteTableNum = TRAIN_DOOR_OPEN;
        }
        else if (task->tTimer >= TRAIN_SETTLE_FRAMES + TRAIN_DOOR_FRAMES)
        {
            task->tTimer = 0;
            task->tState = ARRIVE_PLAYER_STEPS_OUT;
        }
        break;
    case ARRIVE_PLAYER_STEPS_OUT:
        player->invisible = FALSE;
        UnfreezeObjectEvent(player);
        ObjectEventClearHeldMovementIfActive(player);
        ObjectEventSetHeldMovement(player, MOVEMENT_ACTION_WALK_NORMAL_DOWN);
        task->tState = ARRIVE_WAIT_STEP;
        break;
    case ARRIVE_WAIT_STEP:
        if (ObjectEventClearHeldMovementIfFinished(player))
        {
            task->tTimer = 0;
            task->tState = train != NULL ? ARRIVE_DOOR_CLOSES : ARRIVE_END;
        }
        break;
    case ARRIVE_DOOR_CLOSES:
        if (++task->tTimer == TRAIN_DOOR_FRAMES)
        {
            PlaySE(SE_TRUCK_DOOR);
            train->subspriteTableNum = TRAIN_DOOR_SHUT;
        }
        else if (task->tTimer >= TRAIN_DOOR_FRAMES + TRAIN_SETTLE_FRAMES)
        {
            PlaySE(SE_TRUCK_MOVE);
            task->tTimer = 0;
            task->tFrom = 0;
            task->tTo = TrainOffscreenRightX2(train);
            task->tState = ARRIVE_TRAIN_LEAVES;
        }
        break;
    case ARRIVE_TRAIN_LEAVES:
        train->x2 = EaseIn(task->tFrom, task->tTo, ++task->tTimer, TRAIN_DEPART_FRAMES);
        if (task->tTimer >= TRAIN_DEPART_FRAMES)
            task->tState = ARRIVE_END;
        break;
    case ARRIVE_END:
        DestroyTrainSprite(task->tSpriteId);
        UnfreezeObjectEvents();
        UnlockPlayerFieldControls();
        DestroyTask(taskId);
        break;
    }
}
