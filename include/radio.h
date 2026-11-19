#ifndef GUARD_RADIO_H
#define GUARD_RADIO_H

// Rotom Phone radio (DESIGN.md "RADIO app"): VAR_RADIO_STATION = station + 1 (0 = off).
// Music priority: battles / fanfares / cutscenes > script music > radio > map music.

enum
{
    RADIO_TOSA_FM,
    RADIO_HOENN_FM,
    RADIO_KANTO_GOLD,
    RADIO_UNOVA,
    RADIO_GALAR,
    RADIO_STATION_COUNT
};

enum { RADIO_RAMP_PURPLE, RADIO_RAMP_BLUE, RADIO_RAMP_RED, RADIO_RAMP_GREY, RADIO_RAMP_GOLD };
#define RADIO_UNLOCK_NEVER 0xFFFF

struct RadioSong
{
    u16 song;
    const u8 *title;
    u16 introFrames;
    u16 loopFrames;
};

struct RadioStation
{
    const u8 *name;
    u16 freqTenths;
    const u8 *region;
    const u8 *tagline;
    u8 ramp;
    const struct RadioSong *songs;
    u8 count;
    u16 unlockFlag;     // 0 = from the start
};

const struct RadioStation *Radio_GetStation(u32 id);
const u16 *Radio_GetRamp(u32 id);           // dark, face, light
bool32 Radio_IsStationUnlocked(u32 id);
s32 Radio_GetStationId(void);               // -1 = off
bool32 Radio_HasSignal(void);
const struct RadioSong *Radio_GetCurrentSong(void);
void Radio_SetStation(s32 id);              // -1 = off; switches the music now (crossfade)

// overworld.c / scrcmd.c hooks
// The song the field should play instead of mapMusic on `map`. connection = walking into the next map
// (saved music is dropped there, so the radio comes back).
u16 Radio_FieldMusic(u16 mapMusic, const struct MapHeader *map, bool32 connection);
void Radio_YieldToScript(void);             // playbgm / fadenewbgm / savebgm: script music wins
void Radio_ScriptDone(void);                // fadedefaultbgm: the radio may come back
void Radio_Update(void);                    // every field frame: rotation + now-playing toast

#endif // GUARD_RADIO_H
