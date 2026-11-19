#ifndef GUARD_REGIONS_H
#define GUARD_REGIONS_H

#include "global.h"
#include "constants/regions.h"

enum KantoSubRegion GetKantoSubregion(u32 mapSecId);

// Orchid: Tosa is REGION_HOENN (vanilla Hoenn sections, renamed). Tiksi reuses the vanilla Kanto/Sevii
// sections (Orchid has no Kanto), so REGION_KANTO never comes up and Kanto-only behaviour (FRLG battle
// music, Kanto/Sevii region maps) stays off.
#define REGION_TOSA REGION_HOENN

bool32 IsVoyageMapSec(u32 mapSecId); // src/voyages.c: Eon Island + the old Sevii block (Sevii, Holon, moons)

static inline bool32 IsTiksiMapSec(u32 sectionId)
{
    return sectionId >= KANTO_MAPSEC_START && sectionId < MAPSEC_SPECIAL_AREA && !IsVoyageMapSec(sectionId);
}

static inline enum Region GetRegionForSectionId(u32 sectionId)
{
    if (IsTiksiMapSec(sectionId))
        return REGION_TIKSI;
    return REGION_TOSA;
}

static inline enum Region GetCurrentRegion(void)
{
    return GetRegionForSectionId(gMapHeader.regionMapSectionId);
}

#endif // GUARD_REGIONS_H
