// Rotom Phone radio: field music override, song rotation and the now-playing toast.
// DESIGN.md "RADIO app" (approved 2026-11-17), mock_radio.py.
//
// Priority: battles / fanfares / cutscenes (never field music) > script music (playbgm, fadenewbgm,
// savebgm, savedMusic: the radio yields until fadedefaultbgm or the next map with nothing saved) >
// radio (replaces map, night and surf music) > map music. No signal underground or underwater.
// Rotation: each song plays its intro + loop twice, ~1s fade, then the next from a shuffle bag
// (no repeats until every song has played). The timer only runs while the radio song is playing;
// after a battle (anything else took over the music) the next song starts.
#include "global.h"
#include "radio.h"
#include "bg.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "map_name_popup.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "phone_ui.h"
#include "random.h"
#include "script.h"
#include "sound.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/map_types.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "data/radio_stations.h"

#define MAX_BAG 32

static EWRAM_DATA struct
{
    s8 bagStation;
    u8 bag[MAX_BAG];
    u8 bagLen;
    u8 bagPos;
    s8 songIdx;         // index into the station's songs, -1 = none chosen yet
    u32 playFrames;
    bool8 yield;
    u8 yieldMapGroup;
    u8 yieldMapNum;
    bool8 toastPending;
} sRadio = {0};

static void StartToast(void);

const struct RadioStation *Radio_GetStation(u32 id)
{
    return &sRadioStations[id < RADIO_STATION_COUNT ? id : 0];
}

const u16 *Radio_GetRamp(u32 id)
{
    return sStationRamps[Radio_GetStation(id)->ramp];
}

bool32 Radio_IsStationUnlocked(u32 id)
{
    const struct RadioStation *st = Radio_GetStation(id);
    if (st->count == 0 || st->unlockFlag == RADIO_UNLOCK_NEVER)
        return FALSE;
    return st->unlockFlag == 0 || FlagGet(st->unlockFlag);
}

s32 Radio_GetStationId(void)
{
    u16 v = VarGet(VAR_RADIO_STATION);
    if (v == 0 || v > RADIO_STATION_COUNT || !Radio_IsStationUnlocked(v - 1))
        return -1;
    return v - 1;
}

static bool32 MapTypeHasSignal(enum MapType type)
{
    return type != MAP_TYPE_UNDERGROUND && type != MAP_TYPE_UNDERWATER;
}

bool32 Radio_HasSignal(void)
{
    return MapTypeHasSignal(gMapHeader.mapType);
}

const struct RadioSong *Radio_GetCurrentSong(void)
{
    s32 st = Radio_GetStationId();
    if (st < 0 || sRadio.bagStation != st || sRadio.songIdx < 0)
        return NULL;
    return &Radio_GetStation(st)->songs[sRadio.songIdx];
}

static void FillBag(s32 st)
{
    u32 i, j, n = Radio_GetStation(st)->count;
    s8 last = (sRadio.bagStation == st) ? sRadio.songIdx : -1;

    if (n > MAX_BAG)
        n = MAX_BAG;
    for (i = 0; i < n; i++)
        sRadio.bag[i] = i;
    for (i = n; i > 1; i--)
    {
        u8 t;
        j = Random() % i;
        t = sRadio.bag[i - 1];
        sRadio.bag[i - 1] = sRadio.bag[j];
        sRadio.bag[j] = t;
    }
    if (n > 1 && sRadio.bag[0] == last)     // no repeat across refills
    {
        sRadio.bag[0] = sRadio.bag[n - 1];
        sRadio.bag[n - 1] = last;
    }
    sRadio.bagStation = st;
    sRadio.bagLen = n;
    sRadio.bagPos = 0;
}

static void NextSong(s32 st)
{
    if (sRadio.bagStation != st || sRadio.bagPos >= sRadio.bagLen)
        FillBag(st);
    sRadio.songIdx = sRadio.bag[sRadio.bagPos++];
    sRadio.playFrames = 0;
    sRadio.toastPending = TRUE;
}

u16 Radio_FieldMusic(u16 mapMusic, const struct MapHeader *map, bool32 connection)
{
    s32 st = Radio_GetStationId();
    const struct RadioSong *song;

    if (st < 0 || mapMusic == MUS_NONE || mapMusic == MUS_ABNORMAL_WEATHER)
        return mapMusic;
    if (connection)
    {
        sRadio.yield = FALSE;
    }
    else
    {
        if (gSaveBlock1Ptr->savedMusic != MUS_DUMMY && gSaveBlock1Ptr->savedMusic != MUS_NONE)
            return mapMusic;
        if (sRadio.yield)
        {
            if (gSaveBlock1Ptr->location.mapGroup == sRadio.yieldMapGroup
             && gSaveBlock1Ptr->location.mapNum == sRadio.yieldMapNum)
                return mapMusic;
            sRadio.yield = FALSE;   // next map, nothing saved: the radio is back
        }
    }
    if (!MapTypeHasSignal(map->mapType))
        return mapMusic;
    song = Radio_GetCurrentSong();
    if (song == NULL || (sRadio.playFrames != 0 && GetCurrentMapMusic() != song->song))
        NextSong(st);   // first song, or something (a battle) took over the music
    return Radio_GetCurrentSong()->song;
}

void Radio_YieldToScript(void)
{
    sRadio.yield = TRUE;
    sRadio.yieldMapGroup = gSaveBlock1Ptr->location.mapGroup;
    sRadio.yieldMapNum = gSaveBlock1Ptr->location.mapNum;
}

void Radio_ScriptDone(void)
{
    sRadio.yield = FALSE;
}

void Radio_SetStation(s32 id)
{
    VarSet(VAR_RADIO_STATION, id < 0 ? 0 : id + 1);
    sRadio.yield = FALSE;
    if (id >= 0)
    {
        sRadio.bagPos = sRadio.bagLen;  // a fresh shuffle for the new station
        sRadio.bagStation = -1;
        sRadio.songIdx = -1;
        if (Radio_HasSignal())
            NextSong(id);
    }
    FadeOutAndFadeInNewMapMusic(Overworld_GetFieldMusic(), 4, 4);
}

void Radio_Update(void)
{
    const struct RadioSong *song = Radio_GetCurrentSong();
    s32 st = Radio_GetStationId();

    if (song == NULL || sRadio.yield || !Radio_HasSignal())
        return;
    if (GetCurrentMapMusic() != song->song)
        return;
    if (sRadio.toastPending)
        StartToast();
    if (++sRadio.playFrames >= (u32)song->introFrames + 2 * song->loopFrames)
    {
        NextSong(st);
        FadeOutAndPlayNewMapMusic(Radio_GetCurrentSong()->song, 4);     // ~1 s fade
    }
}

// ---------------------------------------------------------------- now-playing toast
// mock_radio.field_toast: kit card top-left (the map-name popup's slot), station-coloured note tile,
// station name + song title; slides down, waits, slides back. Queued behind the map-name popup and
// dropped as soon as a script runs (both share BG0 with the message boxes).
#define TOAST_PAL       14      // the map-name popup's palette slot
#define TOAST_BASE      0x107   // ... and its tiles
#define TOAST_SLIDE     4
#define TOAST_HOLD      150

static const u16 sKitNeutral[16] =
{
    [KIT_INK] = RGB(5, 5, 8), [KIT_INK_SOFT] = RGB(14, 14, 17), [KIT_WHITE] = RGB(31, 31, 31),
    [KIT_PANEL] = RGB(29, 29, 28), [KIT_PANEL_SHADE] = RGB(24, 24, 23), [KIT_PANEL_DARK] = RGB(18, 18, 19),
};
static const u8 sColors_StationName[] = {0, KIT_INK_SOFT, KIT_PANEL_SHADE};
static const u8 sColors_Song[] = {0, KIT_INK, KIT_PANEL_SHADE};
static const char sNote[7][8] = { "...XXXX", "...XXXX", "...X..X", "...X..X", ".XXX.XX", "XXXX.XX", ".XX...." };

#define tState  data[0]
#define tTimer  data[1]
#define tWin    data[2]
#define tY      data[3]

static void Toast_Remove(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    if (tWin != WINDOW_NONE)
    {
        ClearWindowTilemap(tWin);
        CopyBgTilemapBufferToVram(0);
        RemoveWindow(tWin);
    }
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    DestroyTask(taskId);
}

static void Toast_Draw(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    const struct RadioSong *song = Radio_GetCurrentSong();
    const struct RadioStation *st = Radio_GetStation(Radio_GetStationId());
    const u16 *ramp = Radio_GetRamp(Radio_GetStationId());
    u16 pal[16];
    s32 w, x, y;

    memcpy(pal, sKitNeutral, sizeof(pal));
    pal[KIT_ACCENT_DARK] = ramp[0];
    pal[KIT_ACCENT] = ramp[1];
    pal[KIT_ACCENT_LIGHT] = ramp[2];
    LoadPalette(pal, BG_PLTT_ID(TOAST_PAL), PLTT_SIZE_4BPP);

    {
        static const struct WindowTemplate sToastWindow = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 17,
                                                            .height = 4, .paletteNum = TOAST_PAL, .baseBlock = TOAST_BASE };
        tWin = AddWindow(&sToastWindow);
    }
    FillWindowPixelBuffer(tWin, PIXEL_FILL(0));
    w = 12 + 26 + max(GetStringWidth(FONT_NARROW, st->name, 0), GetStringWidth(FONT_NORMAL, song->title, 0)) + 8;
    if (w > 17 * 8 - 2)
        w = 17 * 8 - 2;
    PhoneUI_RoundBox(tWin, 2, 2, w, 28, 4, KIT_PANEL, KIT_INK, KIT_WHITE, KIT_PANEL_SHADE, TRUE);
    PhoneUI_RoundBox(tWin, 6, 6, 20, 20, 3, KIT_ACCENT, KIT_INK, KIT_ACCENT_LIGHT, KIT_ACCENT_DARK, TRUE);
    for (y = 0; y < 7; y++)
        for (x = 0; x < 7; x++)
            if (sNote[y][x] == 'X')
                FillWindowPixelRect(tWin, PIXEL_FILL(KIT_WHITE), 11 + x, 9 + y, 1, 1);
    AddTextPrinterParameterized4(tWin, FONT_NARROW, 31, 1, 0, 0, sColors_StationName, TEXT_SKIP_DRAW, st->name);
    AddTextPrinterParameterized4(tWin, FONT_NORMAL, 31, 13, 0, 0, sColors_Song, TEXT_SKIP_DRAW, song->title);
    PutWindowTilemap(tWin);
    CopyWindowToVram(tWin, COPYWIN_FULL);
}

static bool32 ToastMustHide(void)
{
    return ScriptContext_IsEnabled() || ArePlayerFieldControlsLocked() || Radio_GetCurrentSong() == NULL;
}

static void Task_RadioToast(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    switch (tState)
    {
    case 0:     // queued behind the map-name popup / scripts
        if (Radio_GetCurrentSong() == NULL)
        {
            DestroyTask(taskId);
            return;
        }
        if (IsMapNamePopupActive() || ToastMustHide() || gPaletteFade.active)
            return;
        Toast_Draw(taskId);
        tY = 28;
        SetGpuReg(REG_OFFSET_BG0VOFS, tY);
        tState++;
        break;
    case 1:     // slide down
        if (ToastMustHide() || IsMapNamePopupActive())
        {
            Toast_Remove(taskId);
            return;
        }
        tY -= TOAST_SLIDE;
        if (tY <= 0)
        {
            tY = 0;
            tState++;
        }
        SetGpuReg(REG_OFFSET_BG0VOFS, tY);
        break;
    case 2:     // hold
        if (ToastMustHide() || IsMapNamePopupActive() || ++tTimer >= TOAST_HOLD)
            tState++;
        break;
    case 3:     // slide up
        tY += TOAST_SLIDE;
        SetGpuReg(REG_OFFSET_BG0VOFS, tY);
        if (tY >= 32 || ToastMustHide())
            Toast_Remove(taskId);
        break;
    }
}

static void StartToast(void)
{
    u8 taskId;

    sRadio.toastPending = FALSE;
    if (FuncIsActiveTask(Task_RadioToast))
        return;
    taskId = CreateTask(Task_RadioToast, 90);
    gTasks[taskId].tWin = WINDOW_NONE;
}

#undef tState
#undef tTimer
#undef tWin
#undef tY
