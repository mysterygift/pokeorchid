// Orchid: Pokédex HABITATS ("Gen 5 layout, Gen 3 pixels").
//
// Opened with START from the dex list. Two pages:
//   MAP    the region map with its habitat zones (Northern / Eastern / Southern / Western Tosa); the cursor
//          hops from habitat to habitat (sections that have wild encounter tables), the hovered one glows
//          and its zone is lit while the rest of the land is dimmed. L / R switch region (Tiksi once
//          FLAG_VISITED_FURONG_VILLAGE is set), SELECT flips day / night, A opens the route page.
//   ROUTE  every species of one habitat for the chosen time, one row per method (grass, surfing, Rock
//          Smash, fishing), as party icons: not seen = black silhouette, seen = greyscale, captured once =
//          colour + grey ball, catalogued (captured twice) = colour + colour ball. Levels need one capture,
//          encounter rates need two. A on a seen species jumps to its dex entry.
//
// Mockups: dev_scripts/orchid_ui/mock_habitats.py. Art + layout + region tables: export_habitats.py
// (graphics/pokedex/orchid/habitats_*, hab_*.png, src/data/pokedex_habitats.h). Species come straight from
// gWildMonHeaders (day = the fallback table, night = the _Night table), so the view follows
// src/data/wild_encounters.json without regenerating anything.
//
// MAP    BG0 text window (prio 0)  BG1 frame (prio 1)  BG2 zone overlay, alpha-blended onto BG3 (prio 2)
//        BG3 the dex region map, 8bpp (prio 3)          OBJ: tab chevrons, habitat badges
// ROUTE  BG1 the dex grid (prio 3)  BG2 one full-screen window: wells, chips, text (prio 1)
//        BG3 header band + tray (prio 2)                OBJ: party icons, header chevrons
#include "global.h"
#include "bg.h"
#include "decompress.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "international_string_util.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "pokedex.h"
#include "pokedex_habitats.h"
#include "research.h"
#include "item.h"
#include "field_move.h"
#include "pokemon_icon.h"
#include "region_map.h"
#include "rtc.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "wild_encounter.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/region_map_sections.h"

struct OrchidHabitat
{
    mapsec_u16_t mapsec;
    u8 zone;          // 1-4 (Tosa) / 1 (Tiksi); 0 = none
    u8 nodeX, nodeY;  // cursor / badge cell on the 28x15 grid
    u16 cellStart;    // into sHabCells_*
    u8 cellCount;
};

#include "data/pokedex_habitats.h"

// ------------------------------------------------------------------ assets
static const u32 sHabMap_Gfx[] = INCGFX_U32("graphics/pokedex/orchid/habitats_map.png", ".4bpp.smol");
static const u32 sHabMapTosa1_Tilemap[] = INCGFX_U32("graphics/pokedex/orchid/habitats_map_tosa1.bin", ".smolTM");
static const u32 sHabMapTosa2_Tilemap[] = INCGFX_U32("graphics/pokedex/orchid/habitats_map_tosa2.bin", ".smolTM");
static const u32 sHabMapTiksi2_Tilemap[] = INCGFX_U32("graphics/pokedex/orchid/habitats_map_tiksi2.bin", ".smolTM");
static const u16 sHabOverlay_Pal[] = INCGFX_U16("graphics/pokedex/orchid/habitats_overlay.pal", ".gbapal");
static const u32 sHabRoute_Gfx[] = INCGFX_U32("graphics/pokedex/orchid/habitats_route.png", ".4bpp.smol");
static const u32 sHabRoute_Tilemap[] = INCGFX_U32("graphics/pokedex/orchid/habitats_route.bin", ".smolTM");
static const u8 sHabWell_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_well.png", ".4bpp");
static const u8 sHabWellSel_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_well_sel.png", ".4bpp");
static const u8 sHabChip_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_chip.png", ".4bpp");
static const u8 sHabPicGrass_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_p_grass.png", ".4bpp");
static const u8 sHabPicSurf_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_p_surf.png", ".4bpp");
static const u8 sHabPicRock_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_p_rock.png", ".4bpp");
static const u8 sHabPicFish_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_p_fish.png", ".4bpp");
static const u8 sHabPicSGrass_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_ps_grass.png", ".4bpp");
static const u8 sHabPicSSurf_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_ps_surf.png", ".4bpp");
static const u8 sHabPicSRock_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_ps_rock.png", ".4bpp");
static const u8 sHabPicSFish_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_ps_fish.png", ".4bpp");
static const u8 sHabEye_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_eye.png", ".4bpp");
static const u8 sHabABtn_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_a_btn.png", ".4bpp");
static const u8 sHabSun_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_sun.png", ".4bpp");
static const u8 sHabMoon_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_moon.png", ".4bpp");
static const u8 sHabSegDay_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_seg_day.png", ".4bpp");
static const u8 sHabSegNight_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_seg_night.png", ".4bpp");
static const u8 sHabDown_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_down.png", ".4bpp");
static const u8 sHabCompassNone_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_compass_none.png", ".4bpp");
static const u8 sHabCompassN_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_compass_north.png", ".4bpp");
static const u8 sHabCompassE_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_compass_east.png", ".4bpp");
static const u8 sHabCompassS_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_compass_south.png", ".4bpp");
static const u8 sHabCompassW_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_compass_west.png", ".4bpp");
static const u8 sHabBadge_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_badges.png", ".4bpp");
static const u8 sHabClip_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_clip.png", ".4bpp");
static const u8 sHabWellLock_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_well_lock.png", ".4bpp");
static const u8 sHabWellLockSel_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_well_lock_sel.png", ".4bpp");
static const u8 sHabChipLock_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_chip_lock.png", ".4bpp");
static const u8 sHabQMark_Gfx[] = INCGFX_U8("graphics/pokedex/orchid/hab_qmark.png", ".4bpp");

static const u8 *const sHabCompass[] = {sHabCompassNone_Gfx, sHabCompassN_Gfx, sHabCompassE_Gfx, sHabCompassS_Gfx, sHabCompassW_Gfx};
static const u8 *const sHabMethodPic[] = {sHabPicGrass_Gfx, sHabPicSurf_Gfx, sHabPicRock_Gfx, sHabPicFish_Gfx};
static const u8 *const sHabMethodPicSoft[] = {sHabPicSGrass_Gfx, sHabPicSSurf_Gfx, sHabPicSRock_Gfx, sHabPicSFish_Gfx};

// ------------------------------------------------------------------ constants
#define HAB_C_INK          1
#define HAB_C_INK_SOFT     2
#define HAB_C_WHITE        3
#define HAB_C_PANEL_SHADE  5
#define HAB_C_ACCENT_DARK  7
#define HAB_C_SELECT_DARK  11

#define TAG_HAB_ARROW      0x5DF0
#define TAG_HAB_BADGE      0x5DF1
#define TAG_HAB_UI_PAL     0x5DF2
#define TAG_HAB_GREY_PAL   0x5DF8   // + icon palette index 0-5
#define TAG_HAB_BLACK_PAL  0x5DFF

#define HAB_MAX_HABITATS   64
#define HAB_MAX_ROWS       12
#define HAB_MAX_ICONS      (HAB_ROWS_VISIBLE * HAB_SLOT_N)
#define HAB_METHODS        4

enum { HAB_PAGE_MAP, HAB_PAGE_ROUTE };
enum { HAB_DAY, HAB_NIGHT };
enum { HAB_ST_UNSEEN, HAB_ST_SEEN, HAB_ST_CAPTURED, HAB_ST_CATALOGUED };

struct HabRow
{
    u8 method;
    bool8 first;           // first row of its method (draws the chip)
    u8 count;
    u16 species[HAB_SLOT_N];
    u8 rate[HAB_SLOT_N];    // % (fishing: best rod)
    u8 rod[HAB_SLOT_N];     // fishing: 0 old, 1 good, 2 super
    u8 minLv[HAB_SLOT_N];
    u8 maxLv[HAB_SLOT_N];
    u8 rodMask[HAB_SLOT_N]; // fishing: rods it bites on (bit 0 old, 1 good, 2 super)
};

struct HabState
{
    u8 state;
    u8 page;
    u8 ownBgs;                    // BGs whose tilemap buffer this view allocated (bit per BG)
    bool8 resuming;               // reopened on the route page after a dex entry
    u8 region;
    u8 regions[HAB_REGION_COUNT];
    u8 numRegions;
    u8 time;
    u8 numValid;
    u8 valid[HAB_MAX_HABITATS];   // habitat indices (into the region table) that have wild tables
    u8 cur;                       // index into valid[]
    u8 glowTimer;
    u8 arrowSpriteIds[2];
    u8 badgeSpriteIds[HAB_MAX_HABITATS];
    u8 clipSpriteIds[HAB_MAX_HABITATS];
    // route page
    u8 numRows;
    struct HabRow rows[HAB_MAX_ROWS];
    u8 row, col, top;
    u8 iconSpriteIds[HAB_MAX_ICONS];
    u8 numIcons;
    u8 iconTimer;
    u16 jumpSpecies;
};

static EWRAM_DATA struct HabState *sHab = NULL;
// Where the route page was when A opened a dex entry, so B on that entry comes straight back
static EWRAM_DATA struct { bool8 valid; u8 region, cur, time, row, col, top; } sHabResume = {0};
EWRAM_DATA u16 gHabitatsJumpSpecies = SPECIES_NONE;   // read by pokedex.c after the view closes

static const u8 sHabText_Ink[3]     = {TEXT_COLOR_TRANSPARENT, HAB_C_INK, HAB_C_PANEL_SHADE};
static const u8 sHabText_InkSoft[3] = {TEXT_COLOR_TRANSPARENT, HAB_C_INK_SOFT, HAB_C_PANEL_SHADE};
static const u8 sHabText_Label[3]   = {TEXT_COLOR_TRANSPARENT, HAB_C_WHITE, HAB_C_ACCENT_DARK};
static const u8 sHabText_TabOn[3]   = {TEXT_COLOR_TRANSPARENT, HAB_C_INK, HAB_C_SELECT_DARK};

static const u8 sHabText_Habitats[] = _("HABITATS");
static const u8 sHabText_TosaHabitats[] = _("TOSA HABITATS");
static const u8 sHabText_RouteView[] = _("Route View");
static const u8 sHabText_Unknown[] = _("?????");
static const u8 sHabText_Species[] = _(" species");
static const u8 sHabText_Lv[] = _("Lv.");
static const u8 sHabText_Tiksi[] = _("Tiksi");
static const u8 *const sHabRegionNames[] = {COMPOUND_STRING("TOSA"), COMPOUND_STRING("TIKSI")};
static const u8 *const sHabMethodNames[] = {
    COMPOUND_STRING("Grass"), COMPOUND_STRING("Surfing"), COMPOUND_STRING("Rock Smash"), COMPOUND_STRING("Fishing"),
};
static const u8 *const sHabRodNames[] = {COMPOUND_STRING("Old Rod"), COMPOUND_STRING("Good Rod"), COMPOUND_STRING("Super Rod")};

// Gen 3 slot chances (the "fields" of src/data/wild_encounters.json)
static const u8 sHabLandRates[NUM_LAND_MONS_ENCOUNTER_SLOTS] = {20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1};
static const u8 sHabWaterRates[NUM_WATER_MONS_ENCOUNTER_SLOTS] = {60, 30, 5, 4, 1};
static const u8 sHabFishRates[NUM_FISHING_MONS_ENCOUNTER_SLOTS] = {70, 30, 60, 20, 20, 40, 40, 15, 4, 1};
static const u8 sHabFishRod[NUM_FISHING_MONS_ENCOUNTER_SLOTS] = {0, 0, 1, 1, 1, 2, 2, 2, 2, 2};

// ------------------------------------------------------------------ BG / window templates
static const struct BgTemplate sHabMap_BgTemplate[] =
{
    {.bg = 0, .charBaseIndex = 2, .mapBaseIndex = 12, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 13, .screenSize = 0, .paletteMode = 0, .priority = 1, .baseTile = 0},
    {.bg = 2, .charBaseIndex = 2, .mapBaseIndex = 14, .screenSize = 0, .paletteMode = 0, .priority = 2, .baseTile = 0},
    {.bg = 3, .charBaseIndex = 0, .mapBaseIndex = 15, .screenSize = 0, .paletteMode = 1, .priority = 3, .baseTile = 0},
};

static const struct WindowTemplate sHabMap_WindowTemplates[] =
{
    {.bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 20, .paletteNum = 0, .baseBlock = 0x80},
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sHabRoute_BgTemplate[] =
{
    {.bg = 1, .charBaseIndex = 0, .mapBaseIndex = 13, .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0},
    {.bg = 2, .charBaseIndex = 2, .mapBaseIndex = 14, .screenSize = 0, .paletteMode = 0, .priority = 1, .baseTile = 0},
    {.bg = 3, .charBaseIndex = 0, .mapBaseIndex = 15, .screenSize = 0, .paletteMode = 0, .priority = 2, .baseTile = 0},
};

static const struct WindowTemplate sHabRoute_WindowTemplates[] =
{
    {.bg = 2, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 20, .paletteNum = 0, .baseBlock = 1},
    DUMMY_WIN_TEMPLATE
};

// ------------------------------------------------------------------ sprites
static const struct OamData sHabOam_8x16 = {.shape = SPRITE_SHAPE(8x16), .size = SPRITE_SIZE(8x16), .priority = 0};
static const struct OamData sHabOam_8x8 = {.shape = SPRITE_SHAPE(8x8), .size = SPRITE_SIZE(8x8), .priority = 1};
static const struct SpriteSheet sHabArrowSheet = {gSatchelArrow_Gfx, 8 * 16 / 2, TAG_HAB_ARROW};
static const struct SpritePalette sHabArrowPal = {gSatchelArrow_Pal, TAG_HAB_ARROW};
static const struct SpriteSheet sHabBadgeSheet = {sHabBadge_Gfx, 3 * 8 * 8 / 2, TAG_HAB_BADGE};
static const struct SpritePalette sHabUiPal = {gOrchidDexScreen_Pal, TAG_HAB_UI_PAL};

static const union AnimCmd sHabAnim_Frame0[] = {ANIMCMD_FRAME(0, 0), ANIMCMD_END};
static const union AnimCmd sHabAnim_Frame1[] = {ANIMCMD_FRAME(1, 0), ANIMCMD_END};
static const union AnimCmd sHabAnim_Frame2[] = {ANIMCMD_FRAME(2, 0), ANIMCMD_END};
static const union AnimCmd *const sHabAnims_Badge[] = {sHabAnim_Frame0, sHabAnim_Frame1, sHabAnim_Frame2};
static const union AnimCmd *const sHabAnims_Arrow[] = {sHabAnim_Frame0};

static const struct SpriteTemplate sHabArrowTemplate =
{
    .tileTag = TAG_HAB_ARROW, .paletteTag = TAG_HAB_ARROW, .oam = &sHabOam_8x16, .anims = sHabAnims_Arrow,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sHabBadgeTemplate =
{
    .tileTag = TAG_HAB_BADGE, .paletteTag = TAG_HAB_UI_PAL, .oam = &sHabOam_8x8, .anims = sHabAnims_Badge,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

// ------------------------------------------------------------------ regions
struct HabRegionInfo
{
    const struct OrchidHabitat *habitats;
    u8 count;
    const u8 (*cells)[2];
    const u8 (*zones)[HAB_COLS];
    u8 mapType;
    u8 plateX, plateY;
};

static const struct HabRegionInfo sHabRegions[HAB_REGION_COUNT] =
{
    [HAB_REGION_TOSA] = {sHabitats_Tosa, ARRAY_COUNT(sHabitats_Tosa), sHabCells_Tosa, sHabZoneGrid_Tosa,
                         REGION_MAP_HOENN, HAB_PLATE_TOSA_X, HAB_PLATE_TOSA_Y},
    [HAB_REGION_TIKSI] = {sHabitats_Tiksi, ARRAY_COUNT(sHabitats_Tiksi), sHabCells_Tiksi, sHabZoneGrid_Tiksi,
                          REGION_MAP_TIKSI, HAB_PLATE_TIKSI_X, HAB_PLATE_TIKSI_Y},
};

static const struct OrchidHabitat *Hab_Cur(void)
{
    return &sHabRegions[sHab->region].habitats[sHab->valid[sHab->cur]];
}

// ------------------------------------------------------------------ species data
// The section of every wild header, worked out once (the tables are const): Habitats and Palm's research
// scan them a lot, and the map-header lookup is the slow part.
#define HAB_MAX_HEADERS 640
static EWRAM_DATA u16 sHabHeaderMapsec[HAB_MAX_HEADERS] = {0};
static EWRAM_DATA u8 sHabMapsecHasWild[(MAPSEC_COUNT + 7) / 8] = {0};
static EWRAM_DATA bool8 sHabHeaderCacheReady = FALSE;

static void Hab_InitHeaderCache(void)
{
    u32 i;

    if (sHabHeaderCacheReady)
        return;
    for (i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED) && i < HAB_MAX_HEADERS; i++)
    {
        mapsec_u16_t sec = Overworld_GetMapHeaderByGroupAndId(gWildMonHeaders[i].mapGroup, gWildMonHeaders[i].mapNum)->regionMapSectionId;
        sHabHeaderMapsec[i] = sec;
        if (sec < MAPSEC_COUNT)
            sHabMapsecHasWild[sec / 8] |= 1 << (sec % 8);
    }
    sHabHeaderCacheReady = TRUE;
}

static mapsec_u16_t Hab_MapsecOfHeader(u32 i)
{
    Hab_InitHeaderCache();
    if (i < HAB_MAX_HEADERS)
        return sHabHeaderMapsec[i];
    return Overworld_GetMapHeaderByGroupAndId(gWildMonHeaders[i].mapGroup, gWildMonHeaders[i].mapNum)->regionMapSectionId;
}

static bool32 Hab_SectionHasWild(mapsec_u16_t mapsec)
{
    Hab_InitHeaderCache();
    return mapsec < MAPSEC_COUNT && (sHabMapsecHasWild[mapsec / 8] & (1 << (mapsec % 8)));
}

static const struct WildPokemonInfo *Hab_Table(const struct WildEncounterTypes *types, u32 method)
{
    switch (method)
    {
    case 0: return types->landMonsInfo;
    case 1: return types->waterMonsInfo;
    case 2: return types->rockSmashMonsInfo;
    default: return types->fishingMonsInfo;
    }
}

static u32 Hab_SlotCount(u32 method)
{
    switch (method)
    {
    case 0: return NUM_LAND_MONS_ENCOUNTER_SLOTS;
    case 1: return NUM_WATER_MONS_ENCOUNTER_SLOTS;
    case 2: return NUM_ROCK_SMASH_MONS_ENCOUNTER_SLOTS;
    default: return NUM_FISHING_MONS_ENCOUNTER_SLOTS;
    }
}

static u32 Hab_SlotRate(u32 method, u32 slot)
{
    switch (method)
    {
    case 0: return sHabLandRates[slot];
    case 1:
    case 2: return sHabWaterRates[slot];
    default: return sHabFishRates[slot];
    }
}

// The table a map uses at this time of day: night = its _Night table, falling back to the day one
// (OW_TIME_OF_DAY_FALLBACK) exactly like GetTimeOfDayForEncounters.
static const struct WildPokemonInfo *Hab_TableAt(u32 header, u32 method, u32 time)
{
    const struct WildPokemonInfo *info = NULL;

    if (time == HAB_NIGHT)
        info = Hab_Table(&gWildMonHeaders[header].encounterTypes[TIME_NIGHT], method);
    if (info == NULL)
        info = Hab_Table(&gWildMonHeaders[header].encounterTypes[OW_TIME_OF_DAY_FALLBACK], method);
    return info;
}

#define HAB_RARE_PCT 5     // a species whose share is at or below this shows "?" until seen
#define HAB_NIGHT_LEVELS 2 // wild_encounter.c ORCHID_NIGHT_LEVEL_BONUS

static u32 Hab_OwnedRods(void)
{
    return (CheckBagHasItem(ITEM_OLD_ROD, 1) ? 1 : 0) | (CheckBagHasItem(ITEM_GOOD_ROD, 1) ? 2 : 0)
         | (CheckBagHasItem(ITEM_SUPER_ROD, 1) ? 4 : 0);
}

// a method the player can't use yet (Surf / Rock Smash not unlocked, no rod at all)
static bool32 Hab_MethodLocked(u32 method)
{
    switch (method)
    {
    case 1: return !IsFieldMoveUnlocked(FIELD_MOVE_SURF);
    case 2: return !IsFieldMoveUnlocked(FIELD_MOVE_ROCK_SMASH);
    case 3: return Hab_OwnedRods() == 0;
    default: return FALSE;
    }
}

static u32 Hab_SpeciesState(enum Species species);

static bool32 Hab_SlotLocked(const struct HabRow *row, u32 k)
{
    if (row->method == 3)
        return (row->rodMask[k] & Hab_OwnedRods()) == 0;
    return Hab_MethodLocked(row->method);
}

static bool32 Hab_SlotRareHidden(const struct HabRow *row, u32 k)
{
    return row->rate[k] <= HAB_RARE_PCT && Hab_SpeciesState(row->species[k]) == HAB_ST_UNSEEN;
}

static u32 Hab_SpeciesState(enum Species species)
{
    u32 num = SpeciesToNationalPokedexNum(species);

    if (IsSpeciesCatalogued(num))
        return HAB_ST_CATALOGUED;
    if (GetSetPokedexFlag(num, FLAG_GET_CAUGHT))
        return HAB_ST_CAPTURED;
    if (GetSetPokedexFlag(num, FLAG_GET_SEEN))
        return HAB_ST_SEEN;
    return HAB_ST_UNSEEN;
}

// Builds the route page rows for one section + time: species per method, most common first.
static void Hab_BuildRows(mapsec_u16_t mapsec, u32 time)
{
    u32 i, m, s, k, n;
    u16 species[NUM_LAND_MONS_ENCOUNTER_SLOTS * 4];
    u8 rate[ARRAY_COUNT(species)], rod[ARRAY_COUNT(species)], minLv[ARRAY_COUNT(species)], maxLv[ARRAY_COUNT(species)];
    u8 rodMask[ARRAY_COUNT(species)];

    sHab->numRows = 0;
    for (m = 0; m < HAB_METHODS; m++)
    {
        n = 0;
        for (i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
        {
            const struct WildPokemonInfo *info;
            u16 mapRate[ARRAY_COUNT(species)] = {0};

            if (Hab_MapsecOfHeader(i) != mapsec)
                continue;
            info = Hab_TableAt(i, m, time);
            if (info == NULL)
                continue;
            for (s = 0; s < Hab_SlotCount(m); s++)
            {
                const struct WildPokemon *mon = &info->wildPokemon[s];

                if (mon->species == SPECIES_NONE)
                    continue;
                for (k = 0; k < n && species[k] != mon->species; k++)
                    ;
                if (k == n)
                {
                    if (n == ARRAY_COUNT(species))
                        continue;
                    species[n] = mon->species;
                    rate[n] = 0;
                    rod[n] = 0;
                    rodMask[n] = 0;
                    minLv[n] = mon->minLevel;
                    maxLv[n] = mon->maxLevel;
                    n++;
                }
                minLv[k] = min(minLv[k], mon->minLevel);
                maxLv[k] = max(maxLv[k], mon->maxLevel);
                if (m == 3)
                    rodMask[k] |= 1 << sHabFishRod[s];
                if (m == 3)
                {
                    // fishing: the best rod's share
                    u32 r, rodRate = 0;
                    for (r = 0; r < NUM_FISHING_MONS_ENCOUNTER_SLOTS; r++)
                    {
                        if (sHabFishRod[r] == sHabFishRod[s] && info->wildPokemon[r].species == mon->species)
                            rodRate += sHabFishRates[r];
                    }
                    if (rodRate > rate[k])
                    {
                        rate[k] = rodRate;
                        rod[k] = sHabFishRod[s];
                    }
                }
                else
                {
                    mapRate[k] += Hab_SlotRate(m, s);
                }
            }
            if (m != 3)
            {
                // several maps on one section (cave floors): show the highest share
                for (k = 0; k < n; k++)
                    rate[k] = max(rate[k], mapRate[k]);
            }
        }
        if (n == 0)
            continue;
        // most common first (insertion sort)
        for (i = 1; i < n; i++)
        {
            for (k = i; k > 0 && rate[k] > rate[k - 1]; k--)
            {
                SWAP(species[k], species[k - 1], s);
                SWAP(rate[k], rate[k - 1], s);
                SWAP(rod[k], rod[k - 1], s);
                SWAP(minLv[k], minLv[k - 1], s);
                SWAP(maxLv[k], maxLv[k - 1], s);
                SWAP(rodMask[k], rodMask[k - 1], s);
            }
        }
        for (i = 0; i < n && sHab->numRows < HAB_MAX_ROWS; i += HAB_SLOT_N)
        {
            struct HabRow *row = &sHab->rows[sHab->numRows++];

            row->method = m;
            row->first = (i == 0);
            row->count = min(HAB_SLOT_N, n - i);
            for (k = 0; k < row->count; k++)
            {
                row->species[k] = species[i + k];
                row->rate[k] = rate[i + k];
                row->rod[k] = rod[i + k];
                row->minLv[k] = minLv[i + k];
                row->maxLv[k] = maxLv[i + k];
                row->rodMask[k] = rodMask[i + k];
            }
        }
    }
}

// Seen / captured / catalogued / total over the species of a set of sections (both times of day)
void Habitats_CountSections(const mapsec_u16_t *secs, u32 numSecs, struct HabitatCounts *c)
{
    u8 *bits = AllocZeroed(NUM_SPECIES / 8 + 1);
    u32 i, j, m, s, t;

    c->seen = c->captured = c->catalogued = c->total = 0;
    if (bits == NULL)
        return;
    for (i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
    {
        mapsec_u16_t sec = Hab_MapsecOfHeader(i);

        for (j = 0; j < numSecs && secs[j] != sec; j++)
            ;
        if (j == numSecs)
            continue;
        for (t = 0; t < 2; t++)
        {
            for (m = 0; m < HAB_METHODS; m++)
            {
                const struct WildPokemonInfo *info = Hab_TableAt(i, m, t);

                if (info == NULL)
                    continue;
                for (s = 0; s < Hab_SlotCount(m); s++)
                {
                    u32 sp = info->wildPokemon[s].species;

                    if (sp == SPECIES_NONE || sp >= NUM_SPECIES || (bits[sp / 8] & (1 << (sp % 8))))
                        continue;
                    bits[sp / 8] |= 1 << (sp % 8);
                    c->total++;
                    switch (Hab_SpeciesState(sp))
                    {
                    case HAB_ST_CATALOGUED: c->catalogued++; // fallthrough
                    case HAB_ST_CAPTURED:   c->captured++;   // fallthrough
                    case HAB_ST_SEEN:       c->seen++;
                    }
                }
            }
        }
    }
    Free(bits);
}


// ------------------------------------------------------------------ shared with Palm's research (research.c)
u32 Habitats_GetSections(u32 region, u32 zone, mapsec_u16_t *out, u32 max)
{
    const struct HabRegionInfo *r = &sHabRegions[region];
    u32 i, n = 0;

    for (i = 0; i < r->count && n < max; i++)
    {
        if (zone != HAB_ZONE_NONE && r->habitats[i].zone != zone)
            continue;
        if (Hab_SectionHasWild(r->habitats[i].mapsec))
            out[n++] = r->habitats[i].mapsec;
    }
    return n;
}

static bool32 Hab_InTables(u32 header, u32 time, u16 species)
{
    u32 m, s;

    for (m = 0; m < HAB_METHODS; m++)
    {
        const struct WildPokemonInfo *info = Hab_TableAt(header, m, time);
        if (info == NULL)
            continue;
        for (s = 0; s < Hab_SlotCount(m); s++)
        {
            if (info->wildPokemon[s].species == species)
                return TRUE;
        }
    }
    return FALSE;
}

bool32 Habitats_SectionHasSpecies(mapsec_u16_t mapsec, u16 species)
{
    u32 i;

    for (i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
    {
        if (Hab_MapsecOfHeader(i) == mapsec && (Hab_InTables(i, HAB_DAY, species) || Hab_InTables(i, HAB_NIGHT, species)))
            return TRUE;
    }
    return FALSE;
}

// Species found in a night table of the sections but in none of their day tables
void Habitats_CountNightOnly(const mapsec_u16_t *secs, u32 numSecs, struct HabitatCounts *c)
{
    u8 *night = AllocZeroed(NUM_SPECIES / 8 + 1), *day = AllocZeroed(NUM_SPECIES / 8 + 1);
    u32 i, j, m, s, t, sp;

    c->seen = c->captured = c->catalogued = c->total = 0;
    if (night != NULL && day != NULL)
    {
        for (i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
        {
            mapsec_u16_t sec = Hab_MapsecOfHeader(i);

            for (j = 0; j < numSecs && secs[j] != sec; j++)
                ;
            if (j == numSecs)
                continue;
            for (t = 0; t < 2; t++)
            {
                for (m = 0; m < HAB_METHODS; m++)
                {
                    const struct WildPokemonInfo *info = (t == HAB_NIGHT)
                        ? Hab_Table(&gWildMonHeaders[i].encounterTypes[TIME_NIGHT], m)
                        : Hab_Table(&gWildMonHeaders[i].encounterTypes[OW_TIME_OF_DAY_FALLBACK], m);
                    if (info == NULL)
                        continue;
                    for (s = 0; s < Hab_SlotCount(m); s++)
                    {
                        sp = info->wildPokemon[s].species;
                        if (sp != SPECIES_NONE && sp < NUM_SPECIES)
                            (t == HAB_NIGHT ? night : day)[sp / 8] |= 1 << (sp % 8);
                    }
                }
            }
        }
        for (sp = 1; sp < NUM_SPECIES; sp++)
        {
            if (!(night[sp / 8] & (1 << (sp % 8))) || (day[sp / 8] & (1 << (sp % 8))))
                continue;
            c->total++;
            switch (Hab_SpeciesState(sp))
            {
            case HAB_ST_CATALOGUED: c->catalogued++; // fallthrough
            case HAB_ST_CAPTURED:   c->captured++;   // fallthrough
            case HAB_ST_SEEN:       c->seen++;
            }
        }
    }
    Free(night);
    Free(day);
}

const u8 *Habitats_GetZoneName(u32 zone)
{
    return zone < ARRAY_COUNT(sHabZoneNames) ? sHabZoneNames[zone] : sHabZoneNames[0];
}

// ------------------------------------------------------------------ text helpers
static void Hab_Print(u8 fontId, const u8 *str, s32 x, s32 y, const u8 *color)
{
    AddTextPrinterParameterized4(0, fontId, x, y, 0, 0, color, TEXT_SKIP_DRAW, str);
}

static void Hab_PrintCentered(u8 fontId, const u8 *str, s32 cx, s32 y, const u8 *color)
{
    Hab_Print(fontId, str, cx - GetStringWidth(fontId, str, 0) / 2, y, color);
}

static void Hab_PrintRight(u8 fontId, const u8 *str, s32 right, s32 y, const u8 *color)
{
    Hab_Print(fontId, str, right - GetStringWidth(fontId, str, 0), y, color);
}

static s32 Hab_PrintNum(u32 num, s32 x, s32 y, const u8 *color)
{
    u8 str[8];

    ConvertIntToDecimalStringN(str, num, STR_CONV_MODE_LEFT_ALIGN, 4);
    Hab_Print(FONT_NARROW, str, x, y, color);
    return x + GetStringWidth(FONT_NARROW, str, 0);
}

// eye seen, grey ball captured, colour ball catalogued (+ "/total"); returns the end x
static s32 Hab_PrintCounts(const struct HabitatCounts *c, s32 x, s32 y, bool32 total)
{
    BlitBitmapToWindow(0, sHabEye_Gfx, x, y + 4, 16, 8);
    x = Hab_PrintNum(c->seen, x + 11, y, sHabText_Ink) + 5;
    BlitBitmapToWindow(0, gOrchidDexBallGrey_Gfx, x, y + 4, 8, 8);
    x = Hab_PrintNum(c->captured, x + 11, y, sHabText_Ink) + 5;
    BlitBitmapToWindow(0, gOrchidDexBall_Gfx, x, y + 4, 8, 8);
    x = Hab_PrintNum(c->catalogued, x + 11, y, sHabText_Ink) + 5;
    if (total)
    {
        u8 str[8];
        str[0] = CHAR_SLASH;
        ConvertIntToDecimalStringN(str + 1, c->total, STR_CONV_MODE_LEFT_ALIGN, 4);
        Hab_Print(FONT_NARROW, str, x - 2, y, sHabText_InkSoft);
        x += GetStringWidth(FONT_NARROW, str, 0);
    }
    return x;
}

// ------------------------------------------------------------------ setup / teardown
// Frees only what this view allocated: its own BG tilemaps, then the window buffers (FreeAllWindowBuffers
// frees the window BG's tilemap but leaves the BG pointing at it, and the dex list's buffers were already
// freed by pokedex.c), then ResetBgs drops every stale pointer.
static void Hab_FreeBgs(void)
{
    u32 bg;

    for (bg = 0; bg < 4; bg++)
    {
        if (sHab->ownBgs & (1 << bg))
            Free(GetBgTilemapBuffer(bg));
    }
    sHab->ownBgs = 0;
    FreeAllWindowBuffers();
    ResetBgsAndClearDma3BusyFlags(0);
}

static void Hab_AllocBg(u32 bg)
{
    SetBgTilemapBuffer(bg, AllocZeroed(BG_SCREEN_SIZE));
    sHab->ownBgs |= 1 << bg;
}

static void Hab_ResetVideo(void)
{
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ResetBgsAndClearDma3BusyFlags(0);
}

// BG scroll survives screen changes (the dex list scrolls BG2): zero every BG after InitBgsFromTemplates
static void Hab_ZeroBgOffsets(void)
{
    u32 bg;

    for (bg = 0; bg < 4; bg++)
    {
        ChangeBgX(bg, 0, BG_COORD_SET);
        ChangeBgY(bg, 0, BG_COORD_SET);
    }
}

static void Hab_DestroySprites(void)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        if (sHab->arrowSpriteIds[i] != SPRITE_NONE)
            DestroySprite(&gSprites[sHab->arrowSpriteIds[i]]);
        sHab->arrowSpriteIds[i] = SPRITE_NONE;
    }
    for (i = 0; i < HAB_MAX_HABITATS; i++)
    {
        if (sHab->badgeSpriteIds[i] != SPRITE_NONE)
            DestroySprite(&gSprites[sHab->badgeSpriteIds[i]]);
        sHab->badgeSpriteIds[i] = SPRITE_NONE;
        if (sHab->clipSpriteIds[i] != SPRITE_NONE && sHab->clipSpriteIds[i] != MAX_SPRITES)
            DestroySprite(&gSprites[sHab->clipSpriteIds[i]]);
        sHab->clipSpriteIds[i] = SPRITE_NONE;
    }
    for (i = 0; i < sHab->numIcons; i++)
    {
        if (sHab->iconSpriteIds[i] != SPRITE_NONE)
            FreeAndDestroyMonIconSprite(&gSprites[sHab->iconSpriteIds[i]]);
        sHab->iconSpriteIds[i] = SPRITE_NONE;
    }
    sHab->numIcons = 0;
}

static void Hab_LoadSpriteResources(void)
{
    ResetSpriteData();
    FreeAllSpritePalettes();
    gReservedSpritePaletteCount = 0;
    LoadSpriteSheet(&sHabArrowSheet);
    LoadSpritePalette(&sHabArrowPal);
    LoadSpriteSheet(&sHabBadgeSheet);
    LoadSpritePalette(&sHabUiPal);
}

// party icon palettes in colour (POKE_ICON_BASE_PAL_TAG + i), greyscale and an all-INK silhouette
static void Hab_LoadIconPalettes(void)
{
    struct SpritePalette sp;
    u16 pal[16];
    u32 i, j;

    LoadMonIconPalettes();
    for (i = 0; i < 6; i++)
    {
        const u16 *src = gMonIconPaletteTable[i].data;

        for (j = 0; j < 16; j++)
        {
            u32 r = GET_R(src[j]), g = GET_G(src[j]), b = GET_B(src[j]);
            u32 l = (r * 30 + g * 59 + b * 11) / 100;          // 0-31
            l = min(31, 5 + l * 82 / 100);                       // lifted like the mockup
            pal[j] = RGB(l, l, l);
        }
        sp.data = pal;
        sp.tag = TAG_HAB_GREY_PAL + i;
        LoadSpritePalette(&sp);
    }
    for (j = 0; j < 16; j++)
        pal[j] = RGB(3, 3, 5);
    sp.data = pal;
    sp.tag = TAG_HAB_BLACK_PAL;
    LoadSpritePalette(&sp);
}

// ------------------------------------------------------------------ MAP page
static u8 Hab_CellZone(u32 x, u32 y)
{
    return sHabRegions[sHab->region].zones[y][x];
}

static bool32 Hab_CellInHover(u32 x, u32 y)
{
    const struct OrchidHabitat *h = Hab_Cur();
    const u8 (*cells)[2] = sHabRegions[sHab->region].cells;
    u32 i;

    for (i = 0; i < h->cellCount; i++)
    {
        if (cells[h->cellStart + i][0] == x && cells[h->cellStart + i][1] == y)
            return TRUE;
    }
    return FALSE;
}

// BG2: dim the land outside the hovered habitat's zone, gold rim round the zone, glow on the habitat
static void Hab_DrawOverlay(void)
{
    u16 *map = GetBgTilemapBuffer(2);
    u8 zone = Hab_Cur()->zone;
    bool32 zoned = (sHab->region == HAB_REGION_TOSA);
    u32 x, y, tile;

    for (y = 0; y < 32 * 32; y++)
        map[y] = (HAB_OVERLAY_TILE_BASE) | (HAB_OVERLAY_PAL << 12);
    for (y = 0; y < HAB_ROWS; y++)
    {
        for (x = 0; x < HAB_COLS; x++)
        {
            u8 z = Hab_CellZone(x, y);
            u32 mask = 0;

            if (Hab_CellInHover(x, y))
            {
                if (y == 0 || !Hab_CellInHover(x, y - 1)) mask |= 1;
                if (x == HAB_COLS - 1 || !Hab_CellInHover(x + 1, y)) mask |= 2;
                if (y == HAB_ROWS - 1 || !Hab_CellInHover(x, y + 1)) mask |= 4;
                if (x == 0 || !Hab_CellInHover(x - 1, y)) mask |= 8;
                tile = 18 + mask;
            }
            else if (!zoned || z == 0)
            {
                tile = 0;
            }
            else if (z != zone)
            {
                tile = 1;
            }
            else
            {
                #define OTHER(xx, yy) ((xx) < 0 || (yy) < 0 || (xx) >= HAB_COLS || (yy) >= HAB_ROWS ? FALSE \
                    : (Hab_CellZone(xx, yy) != zone && Hab_CellZone(xx, yy) != 0))
                if (OTHER((s32)x, (s32)y - 1)) mask |= 1;
                if (OTHER((s32)x + 1, (s32)y)) mask |= 2;
                if (OTHER((s32)x, (s32)y + 1)) mask |= 4;
                if (OTHER((s32)x - 1, (s32)y)) mask |= 8;
                #undef OTHER
                tile = mask ? 2 + mask : 0;
            }
            map[(y + HAB_GRID_Y / 8) * 32 + x + HAB_GRID_X / 8] = (HAB_OVERLAY_TILE_BASE + tile) | (HAB_OVERLAY_PAL << 12);
        }
    }
    CopyBgTilemapBufferToVram(2);
}

static void Hab_MapSectionsOfZone(mapsec_u16_t *secs, u32 *num)
{
    const struct HabRegionInfo *r = &sHabRegions[sHab->region];
    u8 zone = Hab_Cur()->zone;
    u32 i;

    *num = 0;
    for (i = 0; i < sHab->numValid; i++)
    {
        const struct OrchidHabitat *h = &r->habitats[sHab->valid[i]];
        if (sHab->region != HAB_REGION_TOSA || h->zone == zone)
            secs[(*num)++] = h->mapsec;
    }
}

static void Hab_PrintMap(void)
{
    const struct HabRegionInfo *r = &sHabRegions[sHab->region];
    const struct OrchidHabitat *h = Hab_Cur();
    mapsec_u16_t secs[HAB_MAX_HABITATS];
    struct HabitatCounts c;
    u32 n, i, px = r->plateX, py = r->plateY;
    u8 name[32];

    FillWindowPixelBuffer(0, PIXEL_FILL(0));
    if (sHab->numRegions > 1)
    {
        for (i = 0; i < sHab->numRegions; i++)
            Hab_PrintCentered(FONT_NARROW, sHabRegionNames[sHab->regions[i]], HAB_TAB_X0 + i * HAB_TAB_PITCH + HAB_TAB_W / 2, 0,
                              sHab->regions[i] == sHab->region ? sHabText_TabOn : sHabText_Ink);
        Hab_PrintCentered(FONT_NORMAL, sHabText_Habitats, 156, 0, sHabText_Label);
    }
    else
    {
        Hab_PrintCentered(FONT_NORMAL, sHabText_TosaHabitats, 112, 0, sHabText_Label);
    }
    BlitBitmapToWindow(0, sHab->time == HAB_DAY ? sHabSun_Gfx : sHabMoon_Gfx, HAB_TIME_X + 7, HAB_TIME_Y + 2, 16, 16);

    // zone plate
    BlitBitmapToWindow(0, sHabCompass[sHab->region == HAB_REGION_TOSA ? h->zone : 0], px + 3, py + 2, 16, 16);
    Hab_Print(FONT_NORMAL, sHab->region == HAB_REGION_TOSA ? sHabZoneNames[h->zone] : sHabText_Tiksi, px + 16, py - 1, sHabText_Ink);
    Hab_MapSectionsOfZone(secs, &n);
    Habitats_CountSections(secs, n, &c);
    Hab_PrintCounts(&c, px + 4, py + 13, TRUE);

    // Ⓐ Route View
    BlitBitmapToWindow(0, sHabABtn_Gfx, HAB_CTA_X + 3, 124 + 2, 16, 16);
    Hab_Print(FONT_NARROW, sHabText_RouteView, HAB_CTA_X + 15, 124 - 2, sHabText_Label);

    // tray: habitat name + its counts
    GetMapName(name, h->mapsec, 0);
    Hab_Print(GetFontIdToFit(name, FONT_NORMAL, 0, HAB_NAME_W - 10), name, HAB_NAME_X + 6, HAB_NAME_Y - 1, sHabText_Ink);
    Habitats_CountSections(&h->mapsec, 1, &c);
    Hab_PrintCounts(&c, 128, 140, TRUE);
    CopyWindowToVram(0, COPYWIN_GFX);
}

// Badges on the map: grey ball where every species (day + night) is captured, colour ball where catalogued
static void Hab_CreateBadges(void)
{
    const struct HabRegionInfo *r = &sHabRegions[sHab->region];
    u32 i;

    for (i = 0; i < sHab->numValid; i++)
    {
        const struct OrchidHabitat *h = &r->habitats[sHab->valid[i]];
        struct HabitatCounts c;
        u8 spriteId;

        if (Research_IsSectionRequested(h->mapsec))
        {
            u8 clip = CreateSprite(&sHabBadgeTemplate, HAB_GRID_X + h->nodeX * 8 + 12, HAB_GRID_Y + h->nodeY * 8 - 3, 0);
            if (clip != MAX_SPRITES)
                StartSpriteAnim(&gSprites[clip], 2);
            sHab->clipSpriteIds[i] = clip;
        }
        Habitats_CountSections(&h->mapsec, 1, &c);
        if (c.total == 0 || c.captured < c.total)
            continue;
        spriteId = CreateSprite(&sHabBadgeTemplate, HAB_GRID_X + h->nodeX * 8 + 4, HAB_GRID_Y + h->nodeY * 8 + 1, 0);
        if (spriteId == MAX_SPRITES)
            continue;
        StartSpriteAnim(&gSprites[spriteId], c.catalogued == c.total ? 1 : 0);
        sHab->badgeSpriteIds[i] = spriteId;
    }
}

static void Hab_FindValid(void)
{
    const struct HabRegionInfo *r = &sHabRegions[sHab->region];
    u32 i;

    sHab->numValid = 0;
    for (i = 0; i < r->count && sHab->numValid < HAB_MAX_HABITATS; i++)
    {
        if (Hab_SectionHasWild(r->habitats[i].mapsec))
            sHab->valid[sHab->numValid++] = i;
    }
}

static void Hab_SetMapTilemap(void)
{
    const u32 *tm;
    u32 i;

    if (sHab->numRegions < 2)
        tm = sHabMapTosa1_Tilemap;
    else if (sHab->region == HAB_REGION_TOSA)
        tm = sHabMapTosa2_Tilemap;
    else
        tm = sHabMapTiksi2_Tilemap;
    CopyToBgTilemapBuffer(1, tm, 0, 0);
    if (sHab->numRegions > 1)
    {
        for (i = 0; i < sHab->numRegions; i++)
        {
            u16 *map = GetBgTilemapBuffer(1);
            u32 x, y, left = (HAB_TAB_X0 + i * HAB_TAB_PITCH) / 8, right = (HAB_TAB_X0 + i * HAB_TAB_PITCH + HAB_TAB_W - 1) / 8;

            for (y = 0; y < 2; y++)
                for (x = left; x <= right; x++)
                    map[y * 32 + x] = (map[y * 32 + x] & 0x0FFF) | ((sHab->regions[i] == sHab->region ? 1 : 0) << 12);
        }
    }
    CopyBgTilemapBufferToVram(1);
}

static void Hab_LoadRegionMap(void)
{
    const struct RegionMapInfo *info = &gRegionMapInfos[sHabRegions[sHab->region].mapType];

    DecompressAndLoadBgGfxUsingHeap(3, info->dexMapGfx, 0, 0, 0);
    CopyToBgTilemapBuffer(3, info->dexMapTilemap, 0, 0);
    CopyBgTilemapBufferToVram(3);
    LoadPalette(info->dexMapPalette, BG_PLTT_ID(7), info->dexMapPaletteSize);
}

static void Hab_ShowMapSprites(void)
{
    Hab_DestroySprites();
    if (sHab->numRegions > 1)
    {
        sHab->arrowSpriteIds[0] = CreateSprite(&sHabArrowTemplate, HAB_TAB_X0 - 6, 8, 0);
        sHab->arrowSpriteIds[1] = CreateSprite(&sHabArrowTemplate, HAB_TAB_X0 + sHab->numRegions * HAB_TAB_PITCH + 2, 8, 0);
        gSprites[sHab->arrowSpriteIds[1]].hFlip = TRUE;
    }
    Hab_CreateBadges();
}

static void Hab_RefreshMap(void)
{
    Hab_DrawOverlay();
    Hab_PrintMap();
}

// d-pad: the nearest habitat node in that direction (along-axis distance + 2x the sideways drift)
static bool32 Hab_MoveCursor(s32 dx, s32 dy)
{
    const struct HabRegionInfo *r = &sHabRegions[sHab->region];
    const struct OrchidHabitat *h = Hab_Cur();
    s32 best = -1, bestScore = 0x7FFF;
    u32 i;

    for (i = 0; i < sHab->numValid; i++)
    {
        const struct OrchidHabitat *o = &r->habitats[sHab->valid[i]];
        s32 ax = o->nodeX - h->nodeX, ay = o->nodeY - h->nodeY;
        s32 along = ax * dx + ay * dy, side = abs(ax * dy) + abs(ay * dx), score;

        if (i == sHab->cur || along <= 0)
            continue;
        score = along + side * 2;
        if (score < bestScore)
        {
            bestScore = score;
            best = i;
        }
    }
    if (best < 0)
        return FALSE;
    sHab->cur = best;
    return TRUE;
}

static void Hab_PulseGlow(void)
{
    // overlay colour 4 (glow) breathes between SELECT_LIGHT and SELECT; colour 3 is the route edge
    static const u16 sGlow[] = {RGB(31, 30, 21), RGB(31, 28, 17), RGB(31, 26, 11), RGB(31, 28, 17)};
    u16 c = sGlow[(sHab->glowTimer++ / 8) & 3];

    if (!gPaletteFade.active)
        LoadPalette(&c, BG_PLTT_ID(HAB_OVERLAY_PAL) + 4, PLTT_SIZEOF(1));
}

// ------------------------------------------------------------------ ROUTE page
static u32 Hab_RowY(u32 row)
{
    return HAB_ROW_Y0 + (row - sHab->top) * HAB_ROW_PITCH;
}

static void Hab_DestroyIcons(void)
{
    u32 i;

    for (i = 0; i < sHab->numIcons; i++)
    {
        if (sHab->iconSpriteIds[i] != SPRITE_NONE)
            FreeAndDestroyMonIconSprite(&gSprites[sHab->iconSpriteIds[i]]);
        sHab->iconSpriteIds[i] = SPRITE_NONE;
    }
    sHab->numIcons = 0;
}

static void Hab_CreateIcons(void)
{
    u32 r, k;

    Hab_DestroyIcons();
    for (r = sHab->top; r < sHab->numRows && r < sHab->top + HAB_ROWS_VISIBLE; r++)
    {
        const struct HabRow *row = &sHab->rows[r];

        for (k = 0; k < row->count; k++)
        {
            u32 st = Hab_SpeciesState(row->species[k]);
            if (Hab_SlotLocked(row, k) || Hab_SlotRareHidden(row, k))
                continue;
            s16 x = HAB_SLOT_X0 + k * HAB_SLOT_PITCH + 16;
            s16 y = Hab_RowY(r) + HAB_WELL_DY + HAB_WELL_H - 30 + 16;
            u8 spriteId = CreateMonIcon(row->species[k], st >= HAB_ST_CAPTURED ? SpriteCB_MonIcon : SpriteCallbackDummy,
                                        x, y, 0, 0);

            if (spriteId == MAX_SPRITES)
                continue;
            gSprites[spriteId].oam.priority = 0;
            if (st == HAB_ST_UNSEEN)
                gSprites[spriteId].oam.paletteNum = IndexOfSpritePaletteTag(TAG_HAB_BLACK_PAL);
            else if (st == HAB_ST_SEEN)
                gSprites[spriteId].oam.paletteNum = IndexOfSpritePaletteTag(TAG_HAB_GREY_PAL + GetValidMonIconPalIndex(row->species[k]));
            sHab->iconSpriteIds[sHab->numIcons++] = spriteId;
        }
    }
}

static void Hab_PrintRoute(void)
{
    const struct OrchidHabitat *h = Hab_Cur();
    const struct HabRow *row = &sHab->rows[sHab->row];
    u16 species = row->species[sHab->col];
    u32 st = Hab_SpeciesState(species), r, k;
    u8 name[32], str[48], *end;
    struct HabitatCounts c = {0};
    s32 x, tw;

    FillWindowPixelBuffer(0, PIXEL_FILL(0));
    // header: compass, title, [sun | moon]
    BlitBitmapToWindow(0, sHabCompass[sHab->region == HAB_REGION_TOSA ? h->zone : 0], 4, 2, 16, 16);
    GetMapName(name, h->mapsec, 0);
    tw = GetStringWidth(FONT_NORMAL, name, 0);
    Hab_PrintCentered(FONT_NORMAL, name, 106, 0, sHabText_Label);
    BlitBitmapToWindow(0, sHab->time == HAB_DAY ? sHabSegDay_Gfx : sHabSegNight_Gfx, HAB_SEG_X, HAB_SEG_Y, 40, 16);
    if (sHab->arrowSpriteIds[0] != SPRITE_NONE)
    {
        gSprites[sHab->arrowSpriteIds[0]].x = 106 - tw / 2 - 10;
        gSprites[sHab->arrowSpriteIds[1]].x = 106 + tw / 2 + 10;
    }

    // rows: chip on a method's first row, wells (gold under the cursor) with capture badges
    for (r = sHab->top; r < sHab->numRows && r < sHab->top + HAB_ROWS_VISIBLE; r++)
    {
        const struct HabRow *rw = &sHab->rows[r];
        u32 y = Hab_RowY(r);

        if (rw->first)
        {
            BlitBitmapToWindow(0, sHabChip_Gfx, HAB_CHIP_X, y + HAB_WELL_DY, 24, 24);
            BlitBitmapToWindow(0, sHabMethodPic[rw->method], HAB_CHIP_X + 4, y + HAB_WELL_DY + 6, 16, 16);
            if (Hab_MethodLocked(rw->method))
                BlitBitmapToWindow(0, sHabChipLock_Gfx, HAB_CHIP_X + 4, y + HAB_WELL_DY + HAB_WELL_H - 6, 16, 16);
        }
        for (k = 0; k < rw->count; k++)
        {
            u32 sx = HAB_SLOT_X0 + k * HAB_SLOT_PITCH;
            u32 s2 = Hab_SpeciesState(rw->species[k]);

            bool32 sel = (r == sHab->row && k == sHab->col);
            if (Hab_SlotLocked(rw, k))
            {
                BlitBitmapToWindow(0, sel ? sHabWellLockSel_Gfx : sHabWellLock_Gfx, sx, y + HAB_WELL_DY, 40, 24);
                continue;
            }
            BlitBitmapToWindow(0, sel ? sHabWellSel_Gfx : sHabWell_Gfx, sx, y + HAB_WELL_DY, 40, 24);
            if (Hab_SlotRareHidden(rw, k))
                BlitBitmapToWindow(0, sHabQMark_Gfx, sx + HAB_SLOT_W / 2 - 4, y + HAB_WELL_DY + HAB_WELL_H / 2 - 4, 8, 8);
            if (Research_IsSpeciesRequested(rw->species[k], Hab_Cur()->mapsec))
                BlitBitmapToWindow(0, sHabClip_Gfx, sx + 2, y + HAB_WELL_DY + 2, 8, 8);
            if (s2 == HAB_ST_CATALOGUED)
                BlitBitmapToWindow(0, gOrchidDexBall_Gfx, sx + HAB_SLOT_W - 10, y + HAB_WELL_DY + HAB_WELL_H - 10, 8, 8);
            else if (s2 == HAB_ST_CAPTURED)
                BlitBitmapToWindow(0, gOrchidDexBallGrey_Gfx, sx + HAB_SLOT_W - 10, y + HAB_WELL_DY + HAB_WELL_H - 10, 8, 8);
        }
    }
    if (sHab->top + HAB_ROWS_VISIBLE < sHab->numRows)
        BlitBitmapToWindow(0, sHabDown_Gfx, 228, HAB_TRAY_Y - 9, 16, 8);

    // tray: name + badge, method / rate / levels (gated by captures), counts
    if (st == HAB_ST_UNSEEN)
        StringCopy(name, sHabText_Unknown);
    else
        StringCopy(name, GetSpeciesName(species));
    Hab_Print(FONT_NORMAL, name, 8, HAB_TRAY_Y + 2, sHabText_Ink);
    x = 12 + GetStringWidth(FONT_NORMAL, name, 0);
    if (st == HAB_ST_CATALOGUED)
        BlitBitmapToWindow(0, gOrchidDexBall_Gfx, x, HAB_TRAY_Y + 7, 8, 8);
    else if (st == HAB_ST_CAPTURED)
        BlitBitmapToWindow(0, gOrchidDexBallGrey_Gfx, x, HAB_TRAY_Y + 7, 8, 8);

    BlitBitmapToWindow(0, sHabMethodPicSoft[row->method], 8, HAB_TRAY_Y + 18, 16, 16);
    if (Hab_SlotLocked(row, sHab->col))
    {
        static const u8 *const sNeeds[] = {
            COMPOUND_STRING(""), COMPOUND_STRING("Needs Surf"), COMPOUND_STRING("Needs Rock Smash"), COMPOUND_STRING("Needs a rod"),
        };
        const u8 *needs = sNeeds[row->method];
        if (row->method == 3)
            needs = (row->rodMask[sHab->col] & 1) ? COMPOUND_STRING("Needs an Old Rod")
                  : (row->rodMask[sHab->col] & 2) ? COMPOUND_STRING("Needs a Good Rod") : COMPOUND_STRING("Needs a Super Rod");
        Hab_Print(FONT_NARROW, needs, 22, HAB_TRAY_Y + 14, sHabText_InkSoft);
        goto counts;
    }
    if (Research_IsSpeciesRequested(species, h->mapsec))
    {
        BlitBitmapToWindow(0, sHabClip_Gfx, 8, HAB_TRAY_Y + 20, 8, 8);
        Hab_Print(FONT_NARROW, COMPOUND_STRING("Palm: catalogue this one"), 22, HAB_TRAY_Y + 14, sHabText_InkSoft);
        goto counts;
    }
    end = StringCopy(str, row->method == 3 ? sHabRodNames[row->rod[sHab->col]] : sHabMethodNames[row->method]);
    *end++ = CHAR_SPACE;
    if (st == HAB_ST_CATALOGUED)
        end = ConvertIntToDecimalStringN(end, row->rate[sHab->col], STR_CONV_MODE_LEFT_ALIGN, 3);
    else
        *end++ = CHAR_QUESTION_MARK;
    *end++ = CHAR_PERCENT;
    *end++ = CHAR_SPACE;
    *end++ = CHAR_SPACE;
    end = StringCopy(end, sHabText_Lv);
    if (st >= HAB_ST_CAPTURED)
    {
        // night: wild Pokémon are HAB_NIGHT_LEVELS higher (wild_encounter.c), shown with a moon
        u32 bonus = (sHab->time == HAB_NIGHT) ? HAB_NIGHT_LEVELS : 0;
        end = ConvertIntToDecimalStringN(end, min(MAX_LEVEL, row->minLv[sHab->col] + bonus), STR_CONV_MODE_LEFT_ALIGN, 3);
        if (row->maxLv[sHab->col] != row->minLv[sHab->col])
        {
            *end++ = CHAR_HYPHEN;
            end = ConvertIntToDecimalStringN(end, min(MAX_LEVEL, row->maxLv[sHab->col] + bonus), STR_CONV_MODE_LEFT_ALIGN, 3);
        }
    }
    else
    {
        *end++ = CHAR_QUESTION_MARK;
        *end = EOS;
    }
    Hab_Print(FONT_NARROW, str, 22, HAB_TRAY_Y + 14, sHabText_InkSoft);
    if (sHab->time == HAB_NIGHT && st >= HAB_ST_CAPTURED)
        BlitBitmapToWindow(0, sHabMoon_Gfx, 24 + GetStringWidth(FONT_NARROW, str, 0), HAB_TRAY_Y + 17, 16, 16);

counts:
    // this time of day's species counts
    for (r = 0; r < sHab->numRows; r++)
    {
        for (k = 0; k < sHab->rows[r].count; k++)
        {
            u32 i2, j2, dup = FALSE;
            // a species can sit on several method rows: count it once
            for (i2 = 0; i2 <= r && !dup; i2++)
                for (j2 = 0; j2 < (i2 == r ? k : sHab->rows[i2].count) && !dup; j2++)
                    dup = (sHab->rows[i2].species[j2] == sHab->rows[r].species[k]);
            if (dup)
                continue;
            c.total++;
            switch (Hab_SpeciesState(sHab->rows[r].species[k]))
            {
            case HAB_ST_CATALOGUED: c.catalogued++; // fallthrough
            case HAB_ST_CAPTURED:   c.captured++;   // fallthrough
            case HAB_ST_SEEN:       c.seen++;
            }
        }
    }
    Hab_PrintCounts(&c, 160, HAB_TRAY_Y + 2, FALSE);
    ConvertIntToDecimalStringN(str, c.total, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(str, sHabText_Species);
    Hab_PrintRight(FONT_NARROW, str, 234, HAB_TRAY_Y + 15, sHabText_InkSoft);
    CopyWindowToVram(0, COPYWIN_GFX);
}

static void Hab_ClampCursor(void)
{
    if (sHab->row >= sHab->numRows)
        sHab->row = sHab->numRows ? sHab->numRows - 1 : 0;
    if (sHab->numRows && sHab->col >= sHab->rows[sHab->row].count)
        sHab->col = sHab->rows[sHab->row].count - 1;
    if (sHab->row < sHab->top)
        sHab->top = sHab->row;
    if (sHab->row >= sHab->top + HAB_ROWS_VISIBLE)
        sHab->top = sHab->row - HAB_ROWS_VISIBLE + 1;
}

static void Hab_RebuildRoute(bool32 keepCursor)
{
    Hab_BuildRows(Hab_Cur()->mapsec, sHab->time);
    if (!keepCursor)
        sHab->row = sHab->col = sHab->top = 0;
    Hab_ClampCursor();
    Hab_PrintRoute();
    Hab_CreateIcons();     // the rows' species change with the habitat / time of day
}

// ------------------------------------------------------------------ tasks
static void Task_HabMapInput(u8 taskId);
static void Task_HabRouteInput(u8 taskId);
static void Task_HabLoadMap(u8 taskId);
static void Task_HabLoadRoute(u8 taskId);
static void Task_HabExit(u8 taskId);

static void Hab_FadeTo(u8 taskId, TaskFunc next)
{
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    sHab->state = 0;
    gTasks[taskId].func = next;
}

static void Task_HabLoadMap(u8 taskId)
{
    switch (sHab->state)
    {
    case 0:
        if (gPaletteFade.active)
            return;
        ODex_SetGridBg(0);
        Hab_DestroySprites();
        Hab_FreeBgs();
        Hab_ResetVideo();
        InitBgsFromTemplates(0, sHabMap_BgTemplate, ARRAY_COUNT(sHabMap_BgTemplate));
        Hab_ZeroBgOffsets();
        Hab_AllocBg(1);
        Hab_AllocBg(2);
        Hab_AllocBg(3);
        InitWindows(sHabMap_WindowTemplates);
        DeactivateAllTextPrinters();
        PutWindowTilemap(0);
        CopyBgTilemapBufferToVram(0);
        sHab->state++;
        break;
    case 1:
        DecompressAndLoadBgGfxUsingHeap(1, sHabMap_Gfx, HAB_MAP_SHEET_TILES * TILE_SIZE_4BPP, 0, 0);
        Hab_LoadRegionMap();
        LoadPalette(gOrchidDexScreen_Pal, BG_PLTT_ID(0), 3 * PLTT_SIZE_4BPP);
        LoadPalette(sHabOverlay_Pal, BG_PLTT_ID(HAB_OVERLAY_PAL), PLTT_SIZE_4BPP);
        sHab->state++;
        break;
    case 2:
        if (FreeTempTileDataBuffersIfPossible())
            return;
        Hab_LoadSpriteResources();
        Hab_SetMapTilemap();
        Hab_RefreshMap();
        Hab_ShowMapSprites();
        sHab->state++;
        break;
    case 3:
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG2 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG3);
        SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(8, 8));
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON);
        ShowBg(0);
        ShowBg(1);
        ShowBg(2);
        ShowBg(3);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        sHab->page = HAB_PAGE_MAP;
        sHab->state++;
        break;
    case 4:
        Hab_PulseGlow();
        if (!gPaletteFade.active)
        {
            sHab->state = 0;
            gTasks[taskId].func = Task_HabMapInput;
        }
        break;
    }
}

static void Hab_SwitchRegion(s32 delta)
{
    u32 i;

    for (i = 0; i < sHab->numRegions && sHab->regions[i] != sHab->region; i++)
        ;
    i = (i + sHab->numRegions + delta) % sHab->numRegions;
    sHab->region = sHab->regions[i];
    Hab_FindValid();
    sHab->cur = 0;
}

static void Task_HabMapInput(u8 taskId)
{
    Hab_PulseGlow();
    if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_PC_OFF);
        Hab_FadeTo(taskId, Task_HabExit);
        return;
    }
    if (JOY_NEW(A_BUTTON) && sHab->numValid)
    {
        PlaySE(SE_PIN);
        Hab_FadeTo(taskId, Task_HabLoadRoute);
        return;
    }
    if (JOY_NEW(SELECT_BUTTON))
    {
        PlaySE(SE_SELECT);
        sHab->time ^= 1;
        Hab_PrintMap();
        return;
    }
    if (JOY_NEW(L_BUTTON | R_BUTTON) && sHab->numRegions > 1)
    {
        PlaySE(SE_DEX_PAGE);
        Hab_SwitchRegion(JOY_NEW(L_BUTTON) ? -1 : 1);
        Hab_FadeTo(taskId, Task_HabLoadMap);
        return;
    }
    if (sHab->numValid)
    {
        s32 dx = 0, dy = 0;

        if (JOY_REPEAT(DPAD_UP)) dy = -1;
        else if (JOY_REPEAT(DPAD_DOWN)) dy = 1;
        else if (JOY_REPEAT(DPAD_LEFT)) dx = -1;
        else if (JOY_REPEAT(DPAD_RIGHT)) dx = 1;
        if ((dx || dy) && Hab_MoveCursor(dx, dy))
        {
            PlaySE(SE_SELECT);
            Hab_RefreshMap();
        }
    }
}

static void Task_HabLoadRoute(u8 taskId)
{
    switch (sHab->state)
    {
    case 0:
        if (gPaletteFade.active)
            return;
        Hab_DestroySprites();
        Hab_FreeBgs();
        Hab_ResetVideo();
        InitBgsFromTemplates(0, sHabRoute_BgTemplate, ARRAY_COUNT(sHabRoute_BgTemplate));
        Hab_ZeroBgOffsets();
        Hab_AllocBg(1);
        Hab_AllocBg(3);
        InitWindows(sHabRoute_WindowTemplates);
        DeactivateAllTextPrinters();
        PutWindowTilemap(0);
        CopyBgTilemapBufferToVram(2);
        sHab->state++;
        break;
    case 1:
        DecompressAndLoadBgGfxUsingHeap(3, sHabRoute_Gfx, HAB_ROUTE_TILES * TILE_SIZE_4BPP, 0, 0);
        CopyToBgTilemapBuffer(3, sHabRoute_Tilemap, 0, 0);
        CopyBgTilemapBufferToVram(3);
        LoadPalette(gOrchidDexScreen_Pal, BG_PLTT_ID(0), 3 * PLTT_SIZE_4BPP);
        sHab->state++;
        break;
    case 2:
        if (FreeTempTileDataBuffersIfPossible())
            return;
        ODex_FillGrid(1);
        Hab_LoadSpriteResources();
        Hab_LoadIconPalettes();
        sHab->arrowSpriteIds[0] = CreateSprite(&sHabArrowTemplate, 60, 8, 0);
        sHab->arrowSpriteIds[1] = CreateSprite(&sHabArrowTemplate, 150, 8, 0);
        gSprites[sHab->arrowSpriteIds[1]].hFlip = TRUE;
        Hab_RebuildRoute(sHab->resuming);
        sHab->resuming = FALSE;
        sHab->state++;
        break;
    case 3:
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON);
        ShowBg(1);
        ShowBg(2);
        ShowBg(3);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        sHab->page = HAB_PAGE_ROUTE;
        sHab->state++;
        break;
    case 4:
        if (!gPaletteFade.active)
        {
            sHab->state = 0;
            gTasks[taskId].func = Task_HabRouteInput;
        }
        break;
    }
}

static void Task_HabRouteInput(u8 taskId)
{
    bool32 moved = FALSE;

    if (sHab->numRows == 0)
    {
        if (JOY_NEW(B_BUTTON | A_BUTTON))
        {
            PlaySE(SE_SELECT);
            Hab_FadeTo(taskId, Task_HabLoadMap);
        }
        return;
    }
    if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        Hab_FadeTo(taskId, Task_HabLoadMap);
        return;
    }
    if (JOY_NEW(A_BUTTON))
    {
        u16 species = sHab->rows[sHab->row].species[sHab->col];

        if (Hab_SpeciesState(species) >= HAB_ST_SEEN)
        {
            PlaySE(SE_PIN);
            sHab->jumpSpecies = species;
            sHabResume.valid = TRUE;
            sHabResume.region = sHab->region;
            sHabResume.cur = sHab->cur;
            sHabResume.time = sHab->time;
            sHabResume.row = sHab->row;
            sHabResume.col = sHab->col;
            sHabResume.top = sHab->top;
            Hab_FadeTo(taskId, Task_HabExit);
        }
        else
        {
            PlaySE(SE_FAILURE);
        }
        return;
    }
    if (JOY_NEW(SELECT_BUTTON))
    {
        PlaySE(SE_SELECT);
        sHab->time ^= 1;
        Hab_RebuildRoute(TRUE);
        return;
    }
    if (JOY_NEW(L_BUTTON | R_BUTTON) && sHab->numValid > 1)
    {
        PlaySE(SE_DEX_PAGE);
        sHab->cur = (sHab->cur + sHab->numValid + (JOY_NEW(L_BUTTON) ? -1 : 1)) % sHab->numValid;
        Hab_RebuildRoute(FALSE);
        return;
    }
    if (JOY_REPEAT(DPAD_UP) && sHab->row > 0)
    {
        sHab->row--;
        moved = TRUE;
    }
    else if (JOY_REPEAT(DPAD_DOWN) && sHab->row + 1 < sHab->numRows)
    {
        sHab->row++;
        moved = TRUE;
    }
    else if (JOY_REPEAT(DPAD_LEFT) && sHab->col > 0)
    {
        sHab->col--;
        moved = TRUE;
    }
    else if (JOY_REPEAT(DPAD_RIGHT) && sHab->col + 1 < sHab->rows[sHab->row].count)
    {
        sHab->col++;
        moved = TRUE;
    }
    if (moved)
    {
        u8 oldTop = sHab->top;

        PlaySE(SE_SELECT);
        Hab_ClampCursor();
        Hab_PrintRoute();
        if (oldTop != sHab->top)
            Hab_CreateIcons();
    }
}

static void Task_HabExit(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    gHabitatsJumpSpecies = sHab->jumpSpecies;
    Hab_DestroySprites();
    FreeMonIconPalettes();
    Hab_FreeBgs();
    Hab_ResetVideo();
    FREE_AND_SET_NULL(sHab);
    DestroyTask(taskId);
}

// ------------------------------------------------------------------ entry
// Returns the task id; the caller waits for it to finish (gHabitatsJumpSpecies = species to open, or NONE).
u8 OpenPokedexHabitats(bool32 resumeRoutePage)
{
    u32 i;

    sHab = AllocZeroed(sizeof(*sHab));
    for (i = 0; i < 2; i++)
        sHab->arrowSpriteIds[i] = SPRITE_NONE;
    for (i = 0; i < HAB_MAX_HABITATS; i++)
        sHab->badgeSpriteIds[i] = sHab->clipSpriteIds[i] = SPRITE_NONE;
    for (i = 0; i < HAB_MAX_ICONS; i++)
        sHab->iconSpriteIds[i] = SPRITE_NONE;
    sHab->regions[sHab->numRegions++] = HAB_REGION_TOSA;
    if (FlagGet(FLAG_VISITED_FURONG_VILLAGE))
        sHab->regions[sHab->numRegions++] = HAB_REGION_TIKSI;
    sHab->region = HAB_REGION_TOSA;
    // open on the region and habitat the player is in, when it's one
    for (i = 0; i < sHab->numRegions; i++)
    {
        u32 j, k;
        const struct HabRegionInfo *r = &sHabRegions[sHab->regions[i]];

        for (j = 0; j < r->count; j++)
        {
            if (r->habitats[j].mapsec == gMapHeader.regionMapSectionId)
            {
                sHab->region = sHab->regions[i];
                Hab_FindValid();
                for (k = 0; k < sHab->numValid; k++)
                    if (sHab->valid[k] == j)
                        sHab->cur = k;
            }
        }
    }
    if (sHab->numValid == 0)
        Hab_FindValid();
    sHab->time = (GetTimeOfDay() == TIME_NIGHT) ? HAB_NIGHT : HAB_DAY;
    gHabitatsJumpSpecies = SPECIES_NONE;
    if (resumeRoutePage && sHabResume.valid)
    {
        sHabResume.valid = FALSE;
        sHab->region = sHabResume.region;
        Hab_FindValid();
        sHab->cur = min(sHabResume.cur, sHab->numValid ? sHab->numValid - 1 : 0);
        sHab->time = sHabResume.time;
        sHab->row = sHabResume.row;
        sHab->col = sHabResume.col;
        sHab->top = sHabResume.top;
        sHab->resuming = TRUE;
        return CreateTask(Task_HabLoadRoute, 0);
    }
    return CreateTask(Task_HabLoadMap, 0);
}
