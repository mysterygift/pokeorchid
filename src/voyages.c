// Orchid: the Sailor's voyages. After the Champion, the Sailor at Wavebreak Town's dock sails the player in
// Mr. Briney's small boat (Emerald/FRLG's Seagallop ferry cutscene, src/seagallop.c) to destinations unlocked
// by passcodes typed into the existing NAMING_SCREEN_CODE screen (special EnterCode -> gStringVar2).
//
// Adding a destination's maps later (Sevii, Holon): fill in .arrivalMap / .arrivalX / .arrivalY of its entry in
// sVoyageDestinations -- that is the only hook. Until then the Sailor says the seas are too rough.
#include "global.h"
#include "event_data.h"
#include "list_menu.h"
#include "malloc.h"
#include "overworld.h"
#include "script_menu.h"
#include "string_util.h"
#include "voyages.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/region_map_sections.h"
#include "constants/seagallop.h"

void DoSeagallopFerryScene(void);

struct VoyageDestination
{
    const u8 *name;
    const u8 *code;            // passcode, upper case (matched case-insensitively); NULL = always open
    u16 unlockFlag;            // 0 = always open (Wavebreak)
    u16 arrivalMap;            // MAP_UNDEFINED = no maps yet: "the seas are too rough"
    s8 arrivalX, arrivalY;     // where the boat leaves the player (next to the Sailor on the dock)
    // Legendaries that come back on every voyage until caught: hide flag cleared on departure unless caught.
    u16 hideFlags[2];
    u16 caughtFlags[2];
};

static const struct VoyageDestination sVoyageDestinations[VOYAGE_DEST_COUNT] =
{
    [VOYAGE_DEST_WAVEBREAK] =
    {
        .name = COMPOUND_STRING("Wavebreak Town"),
        .arrivalMap = MAP_WAVEBREAK_TOWN,
        .arrivalX = 5, .arrivalY = 29,
    },
    [VOYAGE_DEST_EON] =
    {
        .name = COMPOUND_STRING("Eon Island"),
        .code = COMPOUND_STRING("SOULDEW"),
        .unlockFlag = FLAG_VOYAGE_EON,
        .arrivalMap = MAP_SOUTHERN_ISLAND_EXTERIOR,
        .arrivalX = 14, .arrivalY = 23,
        .hideFlags = {FLAG_HIDE_EON_LATIAS, FLAG_HIDE_EON_LATIOS},
        .caughtFlags = {FLAG_CAUGHT_VOYAGE_LATIAS, FLAG_CAUGHT_VOYAGE_LATIOS},
    },
    [VOYAGE_DEST_SEVII] =
    {
        .name = COMPOUND_STRING("Sevii Islands"),
        .code = COMPOUND_STRING("SEAGALLOP"),
        .unlockFlag = FLAG_VOYAGE_SEVII,
        .arrivalMap = MAP_ONE_ISLAND_HARBOR,   // One Island harbour dock
        .arrivalX = 8,
        .arrivalY = 4,
    },
    [VOYAGE_DEST_HOLON] =
    {
        .name = COMPOUND_STRING("Holon"),
        .code = COMPOUND_STRING("DELTA"),
        .unlockFlag = FLAG_VOYAGE_HOLON,
        .arrivalMap = MAP_HOLON_MIRAGE_FOREST,   // the coast jetty (Sailor at 3,36, boat at 1,36)
        .arrivalX = 5,
        .arrivalY = 36,
    },
    [VOYAGE_DEST_NEWMOON] =
    {
        .name = COMPOUND_STRING("Newmoon Island"),
        .code = COMPOUND_STRING("NIGHTMARE"),
        .unlockFlag = FLAG_VOYAGE_NEWMOON,
        .arrivalMap = MAP_NEWMOON_ISLAND,
        .arrivalX = 17, .arrivalY = 15,
        .hideFlags = {FLAG_HIDE_NEWMOON_DARKRAI},
        .caughtFlags = {FLAG_CAUGHT_VOYAGE_DARKRAI},
    },
    [VOYAGE_DEST_FULLMOON] =
    {
        .name = COMPOUND_STRING("Fullmoon Island"),
        .code = COMPOUND_STRING("LUNARWING"),
        .unlockFlag = FLAG_VOYAGE_FULLMOON,
        .arrivalMap = MAP_FULLMOON_ISLAND,
        .arrivalX = 12, .arrivalY = 16,
        .hideFlags = {FLAG_HIDE_FULLMOON_CRESSELIA},
        .caughtFlags = {FLAG_CAUGHT_VOYAGE_CRESSELIA},
    },
};

static bool32 IsUnlocked(u32 dest)
{
    return sVoyageDestinations[dest].unlockFlag == 0 || FlagGet(sVoyageDestinations[dest].unlockFlag);
}

static bool32 IsBuilt(u32 dest)
{
    return sVoyageDestinations[dest].arrivalMap != MAP_UNDEFINED;
}

// The destination whose dock the player is standing on (the Sailor's map), Wavebreak otherwise.
static u32 GetVoyageOrigin(void)
{
    u32 i;
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;

    for (i = 0; i < VOYAGE_DEST_COUNT; i++)
    {
        if (IsBuilt(i) && sVoyageDestinations[i].arrivalMap == map)
            return i;
    }
    return VOYAGE_DEST_WAVEBREAK;
}

static u8 ToUpper(u8 c)
{
    if (c >= CHAR_a && c <= CHAR_z)
        return c - CHAR_a + CHAR_A;
    return c;
}

static bool32 CodeMatches(const u8 *typed, const u8 *code)
{
    while (*code != EOS)
    {
        if (ToUpper(*typed) != *code)
            return FALSE;
        typed++;
        code++;
    }
    return *typed == EOS;
}

// After `special EnterCode`: VAR_RESULT = the VOYAGE_DEST_* the code in gStringVar2 opens, or
// VOYAGE_DEST_NONE. VAR_0x8005 = TRUE if it was newly unlocked. gStringVar1 = the destination's name.
void Voyage_CheckCode(void)
{
    u32 i;

    gSpecialVar_Result = VOYAGE_DEST_NONE;
    gSpecialVar_0x8005 = FALSE;
    for (i = 0; i < VOYAGE_DEST_COUNT; i++)
    {
        if (sVoyageDestinations[i].code == NULL || !CodeMatches(gStringVar2, sVoyageDestinations[i].code))
            continue;
        gSpecialVar_Result = i;
        gSpecialVar_0x8005 = !FlagGet(sVoyageDestinations[i].unlockFlag);
        FlagSet(sVoyageDestinations[i].unlockFlag);
        StringCopy(gStringVar1, sVoyageDestinations[i].name);
        return;
    }
}

static void PushMenuItem(const u8 *name, u32 id)
{
    struct ListMenuItem item;
    u8 *buffer = Alloc(100);   // freed by the dynamic multichoice, like dynmultipush's

    StringCopy(buffer, name);
    item.name = buffer;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

// Pushes the Sailor's menu for `dynmultistack`: every unlocked destination except the one we're at
// (from an island only built destinations, plus home), "Enter a code" at Wavebreak, and "Cancel".
void Voyage_BuildMenu(void)
{
    u32 i, origin = GetVoyageOrigin();

    for (i = 0; i < VOYAGE_DEST_COUNT; i++)
    {
        if (i == origin || !IsUnlocked(i))
            continue;
        if (origin != VOYAGE_DEST_WAVEBREAK && !IsBuilt(i))
            continue;
        PushMenuItem(sVoyageDestinations[i].name, i);
    }
    if (origin == VOYAGE_DEST_WAVEBREAK)
        PushMenuItem(COMPOUND_STRING("Enter a code"), VOYAGE_MENU_ENTER_CODE);
    PushMenuItem(COMPOUND_STRING("Cancel"), VOYAGE_MENU_CANCEL);
}

// VAR_0x8006 = destination. VAR_RESULT = TRUE if it has maps to sail to; gStringVar1 = its name.
void Voyage_IsDestinationOpen(void)
{
    u32 dest = gSpecialVar_0x8006;

    gSpecialVar_Result = FALSE;
    if (dest >= VOYAGE_DEST_COUNT)
        return;
    StringCopy(gStringVar1, sVoyageDestinations[dest].name);
    gSpecialVar_Result = IsBuilt(dest);
}

// VAR_0x8006 = destination. Brings back the destination's legendaries that weren't caught, then runs the
// ferry cutscene with the small boat; the cutscene warps via Voyage_SetArrivalWarp. Use with waitstate.
void Voyage_Depart(void)
{
    u32 i, dest = gSpecialVar_0x8006;
    const struct VoyageDestination *d;

    if (dest >= VOYAGE_DEST_COUNT || !IsBuilt(dest))
        dest = VOYAGE_DEST_WAVEBREAK;
    d = &sVoyageDestinations[dest];
    for (i = 0; i < ARRAY_COUNT(d->hideFlags); i++)
    {
        if (d->hideFlags[i] != 0 && !FlagGet(d->caughtFlags[i]))
            FlagClear(d->hideFlags[i]);
    }
    gSpecialVar_0x8004 = dest == VOYAGE_DEST_WAVEBREAK ? SEAGALLOP_VOYAGE_INBOUND : SEAGALLOP_VOYAGE_OUTBOUND;
    gSpecialVar_0x8006 = dest;
    DoSeagallopFerryScene();
}

void Voyage_SetArrivalWarp(u32 dest)
{
    const struct VoyageDestination *d;

    if (dest >= VOYAGE_DEST_COUNT || !IsBuilt(dest))
        dest = VOYAGE_DEST_WAVEBREAK;
    d = &sVoyageDestinations[dest];
    SetWarpDestination(d->arrivalMap >> 8, d->arrivalMap & 0xFF, WARP_ID_NONE, d->arrivalX, d->arrivalY);
}

// Every map section used by the voyages (regionmap/IMPLEMENTATION.md: the old Sevii block plus Eon Island).
// They must not count as Tiksi (FLAG_VISITED_TIKSI, Tiksi region map).
bool32 IsVoyageMapSec(u32 mapSecId)
{
    return (mapSecId >= MAPSEC_ONE_ISLAND && mapSecId < MAPSEC_SPECIAL_AREA) || mapSecId == MAPSEC_EON_ISLAND;
}
