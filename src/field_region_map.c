#include "global.h"
#include "bg.h"
#include "decompress.h"
#include "event_data.h"
#include "graphics.h"
#include "field_effect.h"
#include "gpu_regs.h"
#include "international_string_util.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "region_map.h"
#include "rotom_phone.h"
#include "sound.h"
#include "strings.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"

/*
 *  This is the type of map shown when interacting with the metatiles for
 *  a wall-mounted Region Map (on the wall of the Pokemon Centers near the PC)
 *  It does not zoom, and pressing A or B closes the map
 *
 *  For the region map in the pokenav, see pokenav_region_map.c
 *  For the region map in the pokedex, see pokdex_area_screen.c/pokedex_area_region_map.c
 *  For the fly map, and utility functions all of the maps use, see region_map.c
 */

enum {
    WIN_MAPSEC_NAME,
    WIN_TITLE,
    WIN_PROMPT,
};

enum {
    TAG_PLAYER_ICON,
    TAG_CURSOR,
};

static EWRAM_DATA struct {
    MainCallback callback;
    u32 unused;
    struct RegionMap regionMap;
    u16 state;
} *sFieldRegionMapHandler = NULL;

static void MCB2_InitRegionMapRegisters(void);
static void VBCB_FieldUpdateRegionMap(void);
static void MCB2_FieldUpdateRegionMap(void);
static void FieldUpdateRegionMap(void);
static void PrintRegionMapSecName();
static bool32 CanFlyFromMap(void);
static bool32 CanSwitchRegionFromMap(void);
static void PrintTitleWindowText();

static const struct BgTemplate sFieldRegionMapBgTemplates[] = {
    {
        .bg = 0,
        .charBaseIndex = 0,
        .mapBaseIndex = 31,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 0,
        .baseTile = 0
    }, {
        // Orchid frame (header, map rim, tray + name pill): export_region_map.py
        .bg = 1,
        .charBaseIndex = 3,
        .mapBaseIndex = 30,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 1,
        .baseTile = 0
    }, {
        .bg = 2,
        .charBaseIndex = 2,
        .mapBaseIndex = 28,
        .screenSize = 2,
        .paletteMode = 1,
        .priority = 2,
        .baseTile = 0
    }
};

// Orchid: transparent text windows on the frame (palette 1 = the kit palette of the frame)
static const struct WindowTemplate sFieldRegionMapWindowTemplates[] =
{
    [WIN_MAPSEC_NAME] = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 17, .width = 15, .height = 3, .paletteNum = 1, .baseBlock = 1},
    [WIN_TITLE] = {.bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 2, .paletteNum = 1, .baseBlock = 46},
    [WIN_PROMPT] = {.bg = 0, .tilemapLeft = 16, .tilemapTop = 17, .width = 14, .height = 3, .paletteNum = 1, .baseBlock = 106},
    DUMMY_WIN_TEMPLATE
};

static const u8 sOrchidMapText_Ink[3] = {TEXT_COLOR_TRANSPARENT, 1, 5};    // INK on PANEL_SHADE
static const u8 sOrchidMapText_Label[3] = {TEXT_COLOR_TRANSPARENT, 3, 7};  // WHITE on ACCENT_DARK

void FieldInitRegionMap(MainCallback callback)
{
    SetVBlankCallback(NULL);
    sFieldRegionMapHandler = Alloc(sizeof(*sFieldRegionMapHandler));
    sFieldRegionMapHandler->state = 0;
    sFieldRegionMapHandler->callback = callback;
    RegionMap_ClearViewedRegionMapType();
    SetMainCallback2(MCB2_InitRegionMapRegisters);
}

static void MCB2_InitRegionMapRegisters(void)
{
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 0);
    SetGpuReg(REG_OFFSET_BG2HOFS, 0);
    SetGpuReg(REG_OFFSET_BG2VOFS, 0);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(1, sFieldRegionMapBgTemplates, ARRAY_COUNT(sFieldRegionMapBgTemplates));
    InitWindows(sFieldRegionMapWindowTemplates);
    DeactivateAllTextPrinters();
    ClearScheduledBgCopiesToVram();
    SetMainCallback2(MCB2_FieldUpdateRegionMap);
    SetVBlankCallback(VBCB_FieldUpdateRegionMap);
}

static void VBCB_FieldUpdateRegionMap(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void MCB2_FieldUpdateRegionMap(void)
{
    FieldUpdateRegionMap();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
    DoScheduledBgTilemapCopiesToVram();
}

static void FieldUpdateRegionMap(void)
{
    switch (sFieldRegionMapHandler->state)
    {
    case 0:
        InitRegionMap(&sFieldRegionMapHandler->regionMap, FALSE);
        RegionMap_LoadOrchidMapV2(FALSE);   // MAP v2 frame, route tubes, place nodes (BG1 + OBJ)
        CreateRegionMapPlayerIcon(TAG_PLAYER_ICON, TAG_PLAYER_ICON);
        CreateRegionMapCursor(TAG_CURSOR, TAG_CURSOR);
        sFieldRegionMapHandler->state++;
        break;
    case 1:
        PutWindowTilemap(WIN_TITLE);
        PutWindowTilemap(WIN_MAPSEC_NAME);
        PutWindowTilemap(WIN_PROMPT);
        PrintTitleWindowText();
        PrintRegionMapSecName();
        ScheduleBgCopyTilemapToVram(0);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        sFieldRegionMapHandler->state++;
        break;
    case 2:
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON);
        ShowBg(0);
        ShowBg(1);
        ShowBg(2);
        sFieldRegionMapHandler->state++;
        break;
    case 3:
        if (!gPaletteFade.active)
        {
            sFieldRegionMapHandler->state++;
        }
        break;
    case 4:
        if (JOY_NEW(R_BUTTON) && CanSwitchRegionFromMap())
        {
            // Orchid: phone MAP R flips between Tosa and Tiksi (once FLAG_VISITED_TIKSI is set)
            PlaySE(SE_SELECT);
            RegionMap_SetViewedRegionMapType(RegionMap_GetViewedRegionMapType() == REGION_MAP_TIKSI
                                             ? REGION_MAP_HOENN : REGION_MAP_TIKSI);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            sFieldRegionMapHandler->state = 7;
            break;
        }
        switch (DoRegionMapInputCallback())
        {
        case MAP_INPUT_MOVE_END:
                PrintRegionMapSecName();
                PrintTitleWindowText();
                RegionMap_UpdateOrchidTray();
                break;
        case MAP_INPUT_A_BUTTON:
        case MAP_INPUT_B_BUTTON:
                sFieldRegionMapHandler->state++;
                break;
        case MAP_INPUT_R_BUTTON:
                if (CanFlyFromMap())
                {
                    PlaySE(SE_SELECT);
                    SetFlyDestination(&sFieldRegionMapHandler->regionMap);
                    gSkipShowMonAnim = TRUE;
                    ReturnToFieldFromFlyMapSelect();
                }
        }
        break;
    case 5:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        sFieldRegionMapHandler->state++;
        break;
    case 6:
        if (!gPaletteFade.active)
        {
            FreeRegionMapIconResources();
            RegionMap_ClearViewedRegionMapType();
            SetMainCallback2(sFieldRegionMapHandler->callback);
            TRY_FREE_AND_SET_NULL(sFieldRegionMapHandler);
            FreeAllWindowBuffers();
        }
        break;
    case 7: // switching region: rebuild the map (state 0) behind the fade
        if (!gPaletteFade.active)
        {
            FreeRegionMapIconResources();
            sFieldRegionMapHandler->state = 0;
        }
        break;
    }
}

// Orchid: Tosa <-> Tiksi on R, only in the Rotom Phone's MAP app and once Tiksi has been visited
static bool32 CanSwitchRegionFromMap(void)
{
    // Wavebreak Voyages: on a voyage the map shows only where you are (no switch, no hint)
    return sFieldRegionMapHandler->callback == CB2_ReturnToRotomPhone && FlagGet(FLAG_VISITED_TIKSI)
        && !IsVoyageRegionMapType(GetRegionMapType(gMapHeader.regionMapSectionId));
}

// R = Fly (expansion's Poké Rider). Never from the Rotom Phone's MAP app: Orchid wants players on
// Tosa Rail and the ferries (user, 2026-11-18). The wall Town Map keeps it.
static bool32 CanFlyFromMap(void)
{
    return sFieldRegionMapHandler->callback != CB2_ReturnToRotomPhone
        && sFieldRegionMapHandler->regionMap.mapSecType == MAPSECTYPE_CITY_CANFLY
        && FlagGet(OW_FLAG_POKE_RIDER) && Overworld_MapTypeAllowsTeleportAndFly(gMapHeader.mapType) == TRUE;
}

// Orchid MAP v2: the place name sits on the tray (mock_map.py: x 8, y 138); a rail chip OBJ follows it
static void PrintRegionMapSecName(void)
{
    const u8 *name = sFieldRegionMapHandler->regionMap.mapSecName;

    FillWindowPixelBuffer(WIN_MAPSEC_NAME, PIXEL_FILL(0));
    if (sFieldRegionMapHandler->regionMap.mapSecType != MAPSECTYPE_NONE)
        AddTextPrinterParameterized4(WIN_MAPSEC_NAME, GetFontIdToFit(name, FONT_NORMAL, 0, 116), 0, 2, 0, 0,
                                     sOrchidMapText_Ink, TEXT_SKIP_DRAW, name);
    CopyWindowToVram(WIN_MAPSEC_NAME, COPYWIN_GFX);
}

// Orchid MAP v2: the region ("TOSA" / "TIKSI") in the header after the map pictogram; the R FLY prompt
// (when allowed) in the tray
static void PrintTitleWindowText(void)
{
    static const u8 FlyPromptText[] = _("{R_BUTTON} FLY");
    const u8 *region = IS_FRLG ? gText_Kanto : GetRegionMapRegionName();
    const u8 *subArea;

    FillWindowPixelBuffer(WIN_TITLE, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, 23, 0, 0, 0, sOrchidMapText_Label, TEXT_SKIP_DRAW, region);
    if (CanSwitchRegionFromMap())
        RegionMap_BlitOrchidSwitchHint(WIN_TITLE, DISPLAY_WIDTH - 40, 4);   // header top-right: R = switch map
    else if ((subArea = GetRegionMapSubAreaName()) != NULL)   // voyages: "ISLES 1-3" right-aligned
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NARROW, DISPLAY_WIDTH - 6 - GetStringWidth(FONT_NARROW, subArea, 0), 1,
                                     0, 0, sOrchidMapText_Label, TEXT_SKIP_DRAW, subArea);
    CopyWindowToVram(WIN_TITLE, COPYWIN_GFX);

    FillWindowPixelBuffer(WIN_PROMPT, PIXEL_FILL(0));
    if (CanFlyFromMap())
        AddTextPrinterParameterized4(WIN_PROMPT, FONT_NORMAL, 4, 3, 0, 0, sOrchidMapText_Ink, TEXT_SKIP_DRAW, FlyPromptText);
    CopyWindowToVram(WIN_PROMPT, COPYWIN_GFX);
}
