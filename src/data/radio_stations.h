// Rotom Phone RADIO stations (DESIGN.md "RADIO app", mock_radio.py). Town / route themes only.
// Song lengths come from dev_scripts/radio/song_lengths.py (run it after adding songs here).
#include "radio_song_lengths.h"

#define RADIO_SONG(mus, title) { mus, COMPOUND_STRING(title), RADIO_INTRO_##mus, RADIO_LOOP_##mus }

static const struct RadioSong sSongs_Tosa[] =
{
    RADIO_SONG(MUS_TOSA_PORT, "Tosa Port"),
    RADIO_SONG(MUS_SOUTHTOSARESERVE, "South Tosa Reserve"),
};

static const struct RadioSong sSongs_Hoenn[] =
{
    RADIO_SONG(MUS_LITTLEROOT, "Littleroot Town"),
    RADIO_SONG(MUS_OLDALE, "Oldale Town"),
    RADIO_SONG(MUS_PETALBURG, "Petalburg City"),
    RADIO_SONG(MUS_ROUTE104, "Route 104"),
    RADIO_SONG(MUS_RUSTBORO, "Rustboro City"),
    RADIO_SONG(MUS_DEWFORD, "Dewford Town"),
    RADIO_SONG(MUS_SLATEPORT, "Slateport City"),
    RADIO_SONG(MUS_ROUTE110, "Route 110"),
    RADIO_SONG(MUS_VERDANTURF, "Verdanturf Town"),
    RADIO_SONG(MUS_ROUTE113, "Route 113"),
    RADIO_SONG(MUS_FALLARBOR, "Fallarbor Town"),
    RADIO_SONG(MUS_ROUTE119, "Route 119"),
    RADIO_SONG(MUS_FORTREE, "Fortree City"),
    RADIO_SONG(MUS_ROUTE120, "Route 120"),
    RADIO_SONG(MUS_LILYCOVE, "Lilycove City"),
    RADIO_SONG(MUS_SOOTOPOLIS, "Sootopolis City"),
    RADIO_SONG(MUS_EVER_GRANDE, "Ever Grande City"),
};

static const struct RadioSong sSongs_Kanto[] =
{
    RADIO_SONG(MUS_RG_PALLET, "Pallet Town"),
    RADIO_SONG(MUS_RG_ROUTE1, "Route 1"),
    RADIO_SONG(MUS_RG_PEWTER, "Pewter City"),
    RADIO_SONG(MUS_RG_ROUTE3, "Route 3"),
    RADIO_SONG(MUS_RG_ROUTE24, "Route 24"),
    RADIO_SONG(MUS_RG_VERMILLION, "Vermilion City"),
    RADIO_SONG(MUS_RG_ROUTE11, "Route 11"),
    RADIO_SONG(MUS_RG_LAVENDER, "Lavender Town"),
    RADIO_SONG(MUS_RG_CELADON, "Celadon City"),
    RADIO_SONG(MUS_RG_FUCHSIA, "Fuchsia City"),
    RADIO_SONG(MUS_RG_CINNABAR, "Cinnabar Island"),
    RADIO_SONG(MUS_RG_SEVII_123, "Sevii Islands"),
    RADIO_SONG(MUS_RG_SEVII_ROUTE, "Sevii Routes"),
};

#include "radio_songs.h"     // Sinnoh + Unova (dev_scripts/radio/songs.py, register_songs.py)

// accent ramps (dark, face, light) for the region plate, EQ and toast (mock_radio.py STATIONS)
static const u16 sStationRamps[][3] =
{
    [RADIO_RAMP_PURPLE] = { RGB(12, 6, 16), RGB(19, 11, 23), RGB(25, 19, 28) },
    [RADIO_RAMP_BLUE]   = { RGB(4, 10, 17), RGB(8, 16, 25), RGB(17, 23, 29) },
    [RADIO_RAMP_RED]    = { RGB(19, 5, 9), RGB(27, 11, 14), RGB(30, 19, 21) },
    [RADIO_RAMP_GREY]   = { RGB(5, 5, 8), RGB(12, 12, 15), RGB(20, 20, 23) },
    [RADIO_RAMP_GOLD]   = { RGB(17, 12, 3), RGB(25, 19, 6), RGB(30, 26, 15) },
    [RADIO_RAMP_PINK]   = { RGB(17, 7, 13), RGB(25, 13, 20), RGB(30, 21, 26) },
};

static const struct RadioStation sRadioStations[RADIO_STATION_COUNT] =
{
    [RADIO_TOSA_FM] = {
        .name = COMPOUND_STRING("TOSA FM"), .freqTenths = 884, .region = COMPOUND_STRING("Tosa"),
        .tagline = COMPOUND_STRING("Home of Tosa's hits!"), .ramp = RADIO_RAMP_PURPLE,
        .songs = sSongs_Tosa, .count = ARRAY_COUNT(sSongs_Tosa), .unlockFlag = 0,
    },
    [RADIO_HOENN_FM] = {
        .name = COMPOUND_STRING("HOENN FM"), .freqTenths = 913, .region = COMPOUND_STRING("Hoenn"),
        .tagline = COMPOUND_STRING("Sun, sea and Route 104."), .ramp = RADIO_RAMP_BLUE,
        .songs = sSongs_Hoenn, .count = ARRAY_COUNT(sSongs_Hoenn), .unlockFlag = 0,
    },
    [RADIO_KANTO_GOLD] = {
        .name = COMPOUND_STRING("KANTO GOLD"), .freqTenths = 981, .region = COMPOUND_STRING("Kanto"),
        .tagline = COMPOUND_STRING("The classics, all day."), .ramp = RADIO_RAMP_RED,
        .songs = sSongs_Kanto, .count = ARRAY_COUNT(sSongs_Kanto), .unlockFlag = 0,
    },
    [RADIO_SINNOH] = {
        .name = COMPOUND_STRING("SINNOH SOUND"), .freqTenths = 1016, .region = COMPOUND_STRING("Sinnoh"),
        .tagline = COMPOUND_STRING("Straight from Mt. Coronet."), .ramp = RADIO_RAMP_PINK,
        .songs = sSongs_Sinnoh, .count = ARRAY_COUNT(sSongs_Sinnoh), .unlockFlag = 0,
    },
    // TODO: quest unlock flags for Sinnoh / Unova / Galar (open from the start for now).
    [RADIO_UNOVA] = {
        .name = COMPOUND_STRING("RADIO UNOVA"), .freqTenths = 1052, .region = COMPOUND_STRING("Unova"),
        .tagline = COMPOUND_STRING("Big city sounds."), .ramp = RADIO_RAMP_GREY,
        .songs = sSongs_Unova, .count = ARRAY_COUNT(sSongs_Unova), .unlockFlag = 0,
    },
    // Galar has no songs yet (needs MIDI imports), so it stays locked and tuning skips it.
    [RADIO_GALAR] = {
        .name = COMPOUND_STRING("ABSOLUTE GALAR"), .freqTenths = 1077, .region = COMPOUND_STRING("Galar"),
        .tagline = COMPOUND_STRING("Galar's biggest anthems."), .ramp = RADIO_RAMP_GOLD,
        .songs = NULL, .count = 0, .unlockFlag = RADIO_UNLOCK_NEVER,
    },
};
