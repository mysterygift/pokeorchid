#include "global.h"
#include "config/save.h"
#include "battle_pike.h"
#include "battle_pyramid.h"
#include "battle_pyramid_bag.h"
#include "bg.h"
#include "debug.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "event_object_lock.h"
#include "event_scripts.h"
#include "fieldmap.h"
#include "field_effect.h"
#include "field_player_avatar.h"
#include "field_specials.h"
#include "field_weather.h"
#include "field_screen_effect.h"
#include "frontier_pass.h"
#include "frontier_util.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "international_string_util.h"
#include "item_icon.h"
#include "item_menu.h"
#include "link.h"
#include "load_save.h"
#include "main.h"
#include "menu.h"
#include "new_game.h"
#include "option_menu.h"
#include "overworld.h"
#include "palette.h"
#include "party_menu.h"
#include "pokedex.h"
#include "pokenav.h"
#include "rotom_phone.h"
#include "region_map.h"
#include "safari_zone.h"
#include "save.h"
#include "scanline_effect.h"
#include "script.h"
#include "sound.h"
#include "start_menu.h"
#include "strings.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "trainer_card.h"
#include "window.h"
#include "union_room.h"
#include "dexnav.h"
#include "wild_encounter.h"
#include "constants/battle_frontier.h"
#include "constants/items.h"
#include "constants/map_types.h"
#include "constants/weather.h"
#include "constants/orchid_ui.h"
#include "constants/rgb.h"
#include "constants/songs.h"

// Menu actions
enum
{
    MENU_ACTION_POKEDEX,
    MENU_ACTION_POKEMON,
    MENU_ACTION_BAG,
    MENU_ACTION_PHONE,
    MENU_ACTION_PLAYER,
    MENU_ACTION_SAVE,
    MENU_ACTION_OPTION,
    MENU_ACTION_EXIT,
    MENU_ACTION_RETIRE_SAFARI,
    MENU_ACTION_PLAYER_LINK,
    MENU_ACTION_REST_FRONTIER,
    MENU_ACTION_RETIRE_FRONTIER,
    MENU_ACTION_PYRAMID_BAG,
    MENU_ACTION_DEBUG,
    MENU_ACTION_DEXNAV,
};

// Orchid start menu + save card (dev_scripts/orchid_ui/mock_system.py, assets from export_system.py)
#include "data/start_menu_orchid.h"

#define TAG_OSM_ICONS        0x6E20
#define TAG_OSM_ICON_PAL     (0x6E21 | BLEND_IMMUNE_FLAG) // menu_icons.png palette (also the saving ball + sparkles)
#define TAG_OSM_ICON_MUTED   (0x6E22 | BLEND_IMMUNE_FLAG) // resting icons
#define TAG_OSM_BALL         0x6E23
#define TAG_OSM_SPARKLES     0x6E24
#define TAG_OSM_SAFARI_ICON  0x6E25
#define TAG_OSM_BANNER       0x6E26 // start menu v2: banner body
#define TAG_OSM_TAB          0x6E27 // gold tab with the option name (drawn at runtime)
#define TAG_OSM_PILL         0x6E28 // location pill (drawn at runtime)
#define TAG_OSM_OBJ_PAL      (0x6E29 | BLEND_IMMUNE_FLAG) // start_obj.pal: banner, tab
#define TAG_OSM_PILL_PAL     (0x6E2A | BLEND_IMMUNE_FLAG) // start_obj.pal with the cap ramp of the current weather: location pill

// Start menu v2: the tab and the location pill are drawn into an off-screen window, then copied to OBJ tiles.
#define OSM2_CANVAS_W        16 // tiles
#define OSM2_CANVAS_H        4
#define OSM2_TAB_SPRITE_X    (DISPLAY_WIDTH - OSM2_CANVAS_W * 8) // screen x of the canvas' left edge

// Which info chip shows beside the start menu (top-left)
enum
{
    ORCHID_CHIP_NONE,
    ORCHID_CHIP_LOCATION,
    ORCHID_CHIP_SAFARI,
    ORCHID_CHIP_PYRAMID,
};

// menu_icons.png frames (dev_scripts/orchid_ui/menu_icons.py NAMES)
enum
{
    ICON_POKEDEX,
    ICON_POKEMON,
    ICON_BAG,
    ICON_PHONE,
    ICON_PLAYER,
    ICON_SAVE,
    ICON_OPTION,
    ICON_EXIT,
    ICON_RETIRE,
    ICON_REST,
    ICON_DEXNAV,
    ICON_DEBUG,
    ICON_COUNT,
};

// Save status
enum
{
    SAVE_IN_PROGRESS,
    SAVE_SUCCESS,
    SAVE_CANCELED,
    SAVE_ERROR
};

// IWRAM common
COMMON_DATA bool8 (*gMenuCallback)(void) = NULL;

// EWRAM
EWRAM_DATA static u8 sSafariBallsWindowId = 0;
EWRAM_DATA static u8 sBattlePyramidFloorWindowId = 0;
EWRAM_DATA static u8 sStartMenuCursorPos = 0;
EWRAM_DATA static u8 sNumStartMenuActions = 0;
EWRAM_DATA static u8 sCurrentStartMenuActions[9] = {0};
EWRAM_DATA static s8 sInitStartMenuData[2] = {0};

EWRAM_DATA static u8 (*sSaveDialogCallback)(void) = NULL;
EWRAM_DATA static u8 sSaveDialogTimer = 0;
EWRAM_DATA static bool8 sSavingComplete = FALSE;
EWRAM_DATA static u8 sSaveInfoWindowId = 0;

// Orchid
EWRAM_DATA static u8 sOrchidChip = ORCHID_CHIP_NONE;
EWRAM_DATA static u8 sOrchidChipWindowId = 0;
EWRAM_DATA static u8 sOrchidSafariIconSpriteId = 0;
EWRAM_DATA static bool8 sOrchidIconsShown = FALSE; // start menu sprites (banner, tab, icons, pill) exist
EWRAM_DATA static u8 sOrchidIconSpriteIds[ARRAY_COUNT(sCurrentStartMenuActions)] = {0};
EWRAM_DATA static u8 sOrchidBannerSpriteIds[3] = {0};
EWRAM_DATA static u8 sOrchidBannerCount = 0;
EWRAM_DATA static u8 sOrchidTabSpriteIds[2] = {0};
EWRAM_DATA static u8 sOrchidPillSpriteIds[2] = {0};
EWRAM_DATA static bool8 sOrchidPillShown = FALSE;
EWRAM_DATA static s16 sOrchidBannerY = 0;
EWRAM_DATA static u8 sOrchidSlideTaskId = 0;
EWRAM_DATA static bool8 sOrchidSlideIn = FALSE; // slide in on the next open (a fresh START press)
EWRAM_DATA static bool8 sOrchidBallShown = FALSE;
EWRAM_DATA static u8 sOrchidBallSpriteId = 0;
EWRAM_DATA static u8 sOrchidSparkleSpriteIds[3] = {0};

// Menu action callbacks
static bool8 StartMenuPokedexCallback(void);
static bool8 StartMenuPokemonCallback(void);
static bool8 StartMenuBagCallback(void);
static bool8 StartMenuPhoneCallback(void);
static bool8 StartMenuPlayerNameCallback(void);
static bool8 StartMenuSaveCallback(void);
static bool8 StartMenuOptionCallback(void);
static bool8 StartMenuExitCallback(void);
static bool8 StartMenuSafariZoneRetireCallback(void);
static bool8 StartMenuLinkModePlayerNameCallback(void);
static bool8 StartMenuBattlePyramidRetireCallback(void);
static bool8 StartMenuBattlePyramidBagCallback(void);
static bool8 StartMenuDebugCallback(void);
static bool8 StartMenuDexNavCallback(void);

// Menu callbacks
static bool8 SaveStartCallback(void);
static bool8 SaveCallback(void);
static bool8 BattlePyramidRetireStartCallback(void);
static bool8 BattlePyramidRetireReturnCallback(void);
static bool8 BattlePyramidRetireCallback(void);
static bool8 HandleStartMenuInput(void);
static bool8 HandleStartMenuClose(void);

// Save dialog callbacks
static u8 SaveConfirmSaveCallback(void);
static u8 SaveYesNoCallback(void);
static u8 SaveConfirmInputCallback(void);
static u8 SaveFileExistsCallback(void);
static u8 SaveConfirmOverwriteDefaultNoCallback(void);
static u8 SaveConfirmOverwriteCallback(void);
static u8 SaveOverwriteInputCallback(void);
static u8 SaveSavingMessageCallback(void);
static u8 SaveDoSaveCallback(void);
static u8 SaveClickCallback(void);
static u8 SaveSuccessCallback(void);
static u8 SaveReturnSuccessCallback(void);
static u8 SaveErrorCallback(void);
static u8 SaveReturnErrorCallback(void);
static u8 BattlePyramidConfirmRetireCallback(void);
static u8 BattlePyramidRetireYesNoCallback(void);
static u8 BattlePyramidRetireInputCallback(void);

// Task callbacks
static void StartMenuTask(u8 taskId);
static void SaveGameTask(u8 taskId);
static void Task_SaveAfterLinkBattle(u8 taskId);
static void Task_WaitForBattleTowerLinkSave(u8 taskId);
static bool8 FieldCB_ReturnToFieldStartMenu(void);

// Orchid chips (mock_system.chip_*): std windows in the Orchid field window palette
static const struct WindowTemplate sWindowTemplate_SafariBalls = {
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = 11,
    .height = 4,
    .paletteNum = ORCHID_YESNO_FIELD_PAL,
    .baseBlock = 0x8
};

static const u8 *const sPyramidFloorNames[FRONTIER_STAGES_PER_CHALLENGE + 1] =
{
    gText_Floor1,
    gText_Floor2,
    gText_Floor3,
    gText_Floor4,
    gText_Floor5,
    gText_Floor6,
    gText_Floor7,
    gText_Peak
};

static const struct WindowTemplate sWindowTemplate_PyramidFloor = {
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = 12,
    .height = 4,
    .paletteNum = ORCHID_YESNO_FIELD_PAL,
    .baseBlock = 0x8
};

static const u8 sText_MenuDebug[] = _("DEBUG");

static const struct MenuAction sStartMenuItems[] =
{
    [MENU_ACTION_POKEDEX]         = {gText_MenuPokedex, {.u8_void = StartMenuPokedexCallback}},
    [MENU_ACTION_POKEMON]         = {gText_MenuPokemon, {.u8_void = StartMenuPokemonCallback}},
    [MENU_ACTION_BAG]             = {gText_MenuBag,     {.u8_void = StartMenuBagCallback}},
    [MENU_ACTION_PHONE]         = {gText_MenuPhone, {.u8_void = StartMenuPhoneCallback}},
    [MENU_ACTION_PLAYER]          = {gText_MenuPlayer,  {.u8_void = StartMenuPlayerNameCallback}},
    [MENU_ACTION_SAVE]            = {gText_MenuSave,    {.u8_void = StartMenuSaveCallback}},
    [MENU_ACTION_OPTION]          = {gText_MenuOption,  {.u8_void = StartMenuOptionCallback}},
    [MENU_ACTION_EXIT]            = {gText_MenuExit,    {.u8_void = StartMenuExitCallback}},
    [MENU_ACTION_RETIRE_SAFARI]   = {gText_MenuRetire,  {.u8_void = StartMenuSafariZoneRetireCallback}},
    [MENU_ACTION_PLAYER_LINK]     = {gText_MenuPlayer,  {.u8_void = StartMenuLinkModePlayerNameCallback}},
    [MENU_ACTION_REST_FRONTIER]   = {gText_MenuRest,    {.u8_void = StartMenuSaveCallback}},
    [MENU_ACTION_RETIRE_FRONTIER] = {gText_MenuRetire,  {.u8_void = StartMenuBattlePyramidRetireCallback}},
    [MENU_ACTION_PYRAMID_BAG]     = {gText_MenuBag,     {.u8_void = StartMenuBattlePyramidBagCallback}},
    [MENU_ACTION_DEBUG]           = {sText_MenuDebug,   {.u8_void = StartMenuDebugCallback}},
    [MENU_ACTION_DEXNAV]          = {gText_MenuDexNav,  {.u8_void = StartMenuDexNavCallback}},
};

static const struct BgTemplate sBgTemplates_LinkBattleSave[] =
{
    {
        .bg = 0,
        .charBaseIndex = 2,
        .mapBaseIndex = 31,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 0,
        .baseTile = 0
    }
};

static const struct WindowTemplate sWindowTemplates_LinkBattleSave[] =
{
    {
        .bg = 0,
        .tilemapLeft = 2,
        .tilemapTop = 15,
        .width = 26,
        .height = 4,
        .paletteNum = 15,
        .baseBlock = 0x194
    },
    DUMMY_WIN_TEMPLATE
};

static const struct WindowTemplate sSaveInfoWindowTemplate = {
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = 14,
    .height = 10,
    .paletteNum = ORCHID_YESNO_FIELD_PAL, // Orchid save card
    .baseBlock = 8
};

static const u8 sOrchidStartMenuIcons[] =
{
    [MENU_ACTION_POKEDEX]         = ICON_POKEDEX,
    [MENU_ACTION_POKEMON]         = ICON_POKEMON,
    [MENU_ACTION_BAG]             = ICON_BAG,
    [MENU_ACTION_PHONE]         = ICON_PHONE,
    [MENU_ACTION_PLAYER]          = ICON_PLAYER,
    [MENU_ACTION_SAVE]            = ICON_SAVE,
    [MENU_ACTION_OPTION]          = ICON_OPTION,
    [MENU_ACTION_EXIT]            = ICON_EXIT,
    [MENU_ACTION_RETIRE_SAFARI]   = ICON_RETIRE,
    [MENU_ACTION_PLAYER_LINK]     = ICON_PLAYER,
    [MENU_ACTION_REST_FRONTIER]   = ICON_REST,
    [MENU_ACTION_RETIRE_FRONTIER] = ICON_RETIRE,
    [MENU_ACTION_PYRAMID_BAG]     = ICON_BAG,
    [MENU_ACTION_DEBUG]           = ICON_DEBUG,
    [MENU_ACTION_DEXNAV]          = ICON_DEXNAV,
};

static const u8 sOrchidTextColors[3] = {TEXT_COLOR_TRANSPARENT, OSM_INK, OSM_PANEL_SHADE};
static const u8 sOrchidNameColors[3] = {TEXT_COLOR_TRANSPARENT, OSM_NAME_FG, OSM_NAME_SHADOW};
static const u8 sOrchidLocationColors[3] = {TEXT_COLOR_TRANSPARENT, OSM_WHITE, OSM_ACCENT_DARK};
static const u8 sText_OrchidSafariBalls[] = _("SAFARI BALLS");
static const u8 sText_OrchidSafariStock[] = _("×{STR_VAR_1}");

static const struct OamData sOam_OrchidIcon = {.shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 0};
static const struct OamData sOam_OrchidSparkle = {.shape = SPRITE_SHAPE(8x8), .size = SPRITE_SIZE(8x8), .priority = 0};

#define ANIM_FRAME_16(n) static const union AnimCmd sAnim_OrchidIcon##n[] = {ANIMCMD_FRAME(n * 4, 0), ANIMCMD_END}
ANIM_FRAME_16(0); ANIM_FRAME_16(1); ANIM_FRAME_16(2); ANIM_FRAME_16(3); ANIM_FRAME_16(4); ANIM_FRAME_16(5);
ANIM_FRAME_16(6); ANIM_FRAME_16(7); ANIM_FRAME_16(8); ANIM_FRAME_16(9); ANIM_FRAME_16(10); ANIM_FRAME_16(11);
#undef ANIM_FRAME_16
static const union AnimCmd *const sAnims_OrchidIcons[ICON_COUNT] =
{
    sAnim_OrchidIcon0, sAnim_OrchidIcon1, sAnim_OrchidIcon2, sAnim_OrchidIcon3, sAnim_OrchidIcon4, sAnim_OrchidIcon5,
    sAnim_OrchidIcon6, sAnim_OrchidIcon7, sAnim_OrchidIcon8, sAnim_OrchidIcon9, sAnim_OrchidIcon10, sAnim_OrchidIcon11,
};
static const union AnimCmd sAnim_OrchidSparkleBig[] = {ANIMCMD_FRAME(0, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidSparkleSmall[] = {ANIMCMD_FRAME(1, 0), ANIMCMD_END};
static const union AnimCmd *const sAnims_OrchidSparkles[] = {sAnim_OrchidSparkleBig, sAnim_OrchidSparkleSmall};

static void SpriteCB_OrchidSaveBall(struct Sprite *sprite);
static void SpriteCB_OrchidSparkle(struct Sprite *sprite);

static const struct SpriteTemplate sSpriteTemplate_OrchidIcon =
{
    .tileTag = TAG_OSM_ICONS,
    .paletteTag = TAG_OSM_ICON_PAL,
    .oam = &sOam_OrchidIcon,
    .anims = sAnims_OrchidIcons,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

// the saving ball's 5 tilt frames use the same 16x16 anim table layout (frame k = tiles 4k)
static const struct SpriteTemplate sSpriteTemplate_OrchidSaveBall =
{
    .tileTag = TAG_OSM_BALL,
    .paletteTag = TAG_OSM_ICON_PAL,
    .oam = &sOam_OrchidIcon,
    .anims = sAnims_OrchidIcons,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_OrchidSaveBall,
};

static const struct SpriteTemplate sSpriteTemplate_OrchidSparkle =
{
    .tileTag = TAG_OSM_SPARKLES,
    .paletteTag = TAG_OSM_ICON_PAL,
    .oam = &sOam_OrchidSparkle,
    .anims = sAnims_OrchidSparkles,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCB_OrchidSparkle,
};

// Local functions
static void BuildStartMenuActions(void);
static void AddStartMenuAction(u8 action);
static void BuildNormalStartMenu(void);
static void BuildDebugStartMenu(void);
static void BuildSafariZoneStartMenu(void);
static void BuildLinkModeStartMenu(void);
static void BuildUnionRoomStartMenu(void);
static void BuildBattlePikeStartMenu(void);
static void BuildBattlePyramidStartMenu(void);
static void BuildMultiPartnerRoomStartMenu(void);
static void ShowSafariBallsWindow(void);
static void ShowPyramidFloorWindow(void);
static void RemoveExtraStartMenuWindows(void);
static bool32 InitStartMenuStep(void);
static void InitStartMenu(void);
static void CreateStartMenuTask(TaskFunc followupFunc);
static void InitSave(void);
static u8 RunSaveCallback(void);
static void ShowSaveMessage(const u8 *message, u8 (*saveCallback)(void));
static void HideSaveMessageWindow(void);
static void HideSaveInfoWindow(void);
static void SaveStartTimer(void);
static bool8 SaveSuccesTimer(void);
static bool8 SaveErrorTimer(void);
static void InitBattlePyramidRetire(void);
static void VBlankCB_LinkBattleSave(void);
static bool32 InitSaveWindowAfterLinkBattle(u8 *par1);
static void CB2_SaveAfterLinkBattle(void);
static void ShowSaveInfoWindow(void);
static void RemoveSaveInfoWindow(void);
static void HideStartMenuWindow(void);
static void HideStartMenuDebug(void);

static void BuildStartMenuActions(void)
{
    sNumStartMenuActions = 0;

    if (IsOverworldLinkActive() == TRUE)
    {
        BuildLinkModeStartMenu();
    }
    else if (InUnionRoom() == TRUE)
    {
        BuildUnionRoomStartMenu();
    }
    else if (GetSafariZoneFlag() == TRUE)
    {
        BuildSafariZoneStartMenu();
    }
    else if (InBattlePike())
    {
        BuildBattlePikeStartMenu();
    }
    else if (CurrentBattlePyramidLocation() != PYRAMID_LOCATION_NONE)
    {
        BuildBattlePyramidStartMenu();
    }
    else if (InMultiPartnerRoom())
    {
        BuildMultiPartnerRoomStartMenu();
    }
    else
    {
        if (DEBUG_OVERWORLD_MENU == TRUE && DEBUG_OVERWORLD_IN_MENU == TRUE)
            BuildDebugStartMenu();
        else
            BuildNormalStartMenu();
    }
}

static void AddStartMenuAction(u8 action)
{
    AppendToList(sCurrentStartMenuActions, &sNumStartMenuActions, action);
}

static void BuildNormalStartMenu(void)
{
    if (FlagGet(FLAG_SYS_POKEDEX_GET) == TRUE)
        AddStartMenuAction(MENU_ACTION_POKEDEX);

    if (DN_FLAG_DEXNAV_GET != 0 && FlagGet(DN_FLAG_DEXNAV_GET))
        AddStartMenuAction(MENU_ACTION_DEXNAV);

    if (FlagGet(FLAG_SYS_POKEMON_GET) == TRUE)
        AddStartMenuAction(MENU_ACTION_POKEMON);

    AddStartMenuAction(MENU_ACTION_BAG);

    if (FlagGet(FLAG_SYS_POKENAV_GET) == TRUE)
        AddStartMenuAction(MENU_ACTION_PHONE);

    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_SAVE);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

static void BuildDebugStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_DEBUG);
    if (FlagGet(FLAG_SYS_POKEDEX_GET) == TRUE)
        AddStartMenuAction(MENU_ACTION_POKEDEX);
    if (FlagGet(FLAG_SYS_POKEMON_GET) == TRUE)
        AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_BAG);
    if (FlagGet(FLAG_SYS_POKENAV_GET) == TRUE)
        AddStartMenuAction(MENU_ACTION_PHONE);
    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_SAVE);
    AddStartMenuAction(MENU_ACTION_OPTION);
}

static void BuildSafariZoneStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_RETIRE_SAFARI);
    AddStartMenuAction(MENU_ACTION_POKEDEX);
    AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_BAG);
    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

static void BuildLinkModeStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_BAG);

    if (FlagGet(FLAG_SYS_POKENAV_GET) == TRUE)
    {
        AddStartMenuAction(MENU_ACTION_PHONE);
    }

    AddStartMenuAction(MENU_ACTION_PLAYER_LINK);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

static void BuildUnionRoomStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_BAG);

    if (FlagGet(FLAG_SYS_POKENAV_GET) == TRUE)
    {
        AddStartMenuAction(MENU_ACTION_PHONE);
    }

    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

static void BuildBattlePikeStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_POKEDEX);
    AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

static void BuildBattlePyramidStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_PYRAMID_BAG);
    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_REST_FRONTIER);
    AddStartMenuAction(MENU_ACTION_RETIRE_FRONTIER);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

static void BuildMultiPartnerRoomStartMenu(void)
{
    AddStartMenuAction(MENU_ACTION_POKEMON);
    AddStartMenuAction(MENU_ACTION_PLAYER);
    AddStartMenuAction(MENU_ACTION_OPTION);
    AddStartMenuAction(MENU_ACTION_EXIT);
}

// ---------------------------------------------------------------- Orchid start menu v2
// mock_start_v2.py, variant B: a slim ink banner flush with the right edge holds the icons (resting ones
// muted); the selected row is a gold tab poking out to the left with the option's name (the PLAYER row in the
// gender name colour). The banner slides in from the right as the location pill slides in from the left.
// Everything is OBJ, so the slide moves banner, tab, icons and pill together (sprite x2). The tab and the
// pill hold text: they are drawn into an off-screen window and its tiles are copied into their OBJ tiles.
enum
{
    SLIDE_NONE,
    SLIDE_OPEN,
    SLIDE_CLOSE,
};

#define tSlideMode  data[0]
#define tSlideFrame data[1]

static const struct OamData sOam_OrchidBanner = {.shape = SPRITE_SHAPE(32x64), .size = SPRITE_SIZE(32x64), .priority = 0};
static const struct OamData sOam_OrchidTab = {.shape = SPRITE_SHAPE(64x32), .size = SPRITE_SIZE(64x32), .priority = 0};
static const union AnimCmd sAnim_OrchidPiece0[] = {ANIMCMD_FRAME(0, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidBanner1[] = {ANIMCMD_FRAME(32, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidBanner2[] = {ANIMCMD_FRAME(64, 0), ANIMCMD_END};
static const union AnimCmd *const sAnims_OrchidBanner[] = {sAnim_OrchidPiece0, sAnim_OrchidBanner1, sAnim_OrchidBanner2};
static const union AnimCmd *const sAnims_OrchidTab[] = {sAnim_OrchidPiece0, sAnim_OrchidBanner1};    // tiles 0 / 32

static const struct SpriteTemplate sSpriteTemplate_OrchidBanner =
{
    .tileTag = TAG_OSM_BANNER, .paletteTag = TAG_OSM_OBJ_PAL, .oam = &sOam_OrchidBanner, .anims = sAnims_OrchidBanner,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sSpriteTemplate_OrchidTab =
{
    .tileTag = TAG_OSM_TAB, .paletteTag = TAG_OSM_OBJ_PAL, .oam = &sOam_OrchidTab, .anims = sAnims_OrchidTab,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sSpriteTemplate_OrchidPill =
{
    .tileTag = TAG_OSM_PILL, .paletteTag = TAG_OSM_PILL_PAL, .oam = &sOam_OrchidTab, .anims = sAnims_OrchidTab,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static const struct WindowTemplate sOrchidCanvasTemplate =
{
    .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = OSM2_CANVAS_W, .height = OSM2_CANVAS_H,
    .paletteNum = 0, .baseBlock = 0x8, // never put on the tilemap or copied to VRAM
};

static const u8 sOrchidTabColors[3] = {TEXT_COLOR_TRANSPARENT, OSM2_INK, OSM2_SELECT_DARK};
static const u8 sOrchidTabNameColors[3] = {TEXT_COLOR_TRANSPARENT, OSM2_SPARE_A, OSM2_SPARE_B};
static const u8 sOrchidPillColors[3] = {TEXT_COLOR_TRANSPARENT, OSM2_INK, OSM2_PANEL_SHADE};

static s32 OrchidStartMenu_BannerX(void)
{
    return OSM2_X0;
}

// Copy a block of canvas tiles (cols col0.., rows 0..rows-1) to a sprite's tiles, in 1D OBJ order.
static void OrchidCanvasToObj(u8 canvas, u16 tileTag, u32 tileOffset, u32 col0, u32 cols, u32 rows)
{
    u8 *src = gWindows[canvas].tileData;
    u8 *dst = (u8 *)(OBJ_VRAM0) + (GetSpriteTileStartByTag(tileTag) + tileOffset) * TILE_SIZE_4BPP;
    u32 r, c;

    for (r = 0; r < rows; r++)
    {
        for (c = 0; c < cols; c++)
            CpuCopy32(src + (r * OSM2_CANVAS_W + col0 + c) * TILE_SIZE_4BPP, dst + (r * cols + c) * TILE_SIZE_4BPP, TILE_SIZE_4BPP);
    }
}

static bool32 OrchidStartMenu_IsNameRow(u32 row)
{
    u8 (*func)(void) = sStartMenuItems[sCurrentStartMenuActions[row]].func.u8_void;

    return func == StartMenuPlayerNameCallback || func == StartMenuLinkModePlayerNameCallback;
}

// Selected row: the gold tab (mock_start_v2.draw_tab) with the option's name, icons muted except the selected
// one, which moves 4 px left and 1 px up.
static void OrchidStartMenu_Select(void)
{
    u8 canvas;
    s32 x0 = OrchidStartMenu_BannerX();
    s32 ty = sOrchidBannerY + 3 + sStartMenuCursorPos * OSM2_PITCH;
    s32 labelW, tx;
    u8 normalPal, mutedPal;
    u32 i;

    if (!sOrchidIconsShown)
        return;

    StringExpandPlaceholders(gStringVar4, sStartMenuItems[sCurrentStartMenuActions[sStartMenuCursorPos]].text);
    labelW = GetStringWidth(FONT_NORMAL, gStringVar4, 0);
    tx = x0 - (labelW + 10) - 4;
    canvas = AddWindow(&sOrchidCanvasTemplate);
    if (canvas != WINDOW_NONE)
    {
        FillWindowPixelBuffer(canvas, PIXEL_FILL(0));
        OrchidDrawRoundedBox(canvas, tx - OSM2_TAB_SPRITE_X, 0, (x0 + OSM2_TAB_TAIL) - tx, OSM2_TAB_H, 4,
                             OSM2_SELECT, OSM2_INK, OSM2_SELECT_LIGHT, OSM2_SELECT_DARK);
        AddTextPrinterParameterized4(canvas, FONT_NORMAL, tx - OSM2_TAB_SPRITE_X + OSM2_TAB_TEXT_DX, 1, 0, 0,
                                     OrchidStartMenu_IsNameRow(sStartMenuCursorPos) ? sOrchidTabNameColors : sOrchidTabColors,
                                     TEXT_SKIP_DRAW, gStringVar4);
        OrchidCanvasToObj(canvas, TAG_OSM_TAB, 0, 0, 8, 4);
        OrchidCanvasToObj(canvas, TAG_OSM_TAB, 32, 8, 8, 4);
        RemoveWindow(canvas);
    }
    for (i = 0; i < 2; i++)
        gSprites[sOrchidTabSpriteIds[i]].y = ty + 16;

    normalPal = IndexOfSpritePaletteTag(TAG_OSM_ICON_PAL);
    mutedPal = IndexOfSpritePaletteTag(TAG_OSM_ICON_MUTED);
    for (i = 0; i < sNumStartMenuActions; i++)
    {
        struct Sprite *sprite = &gSprites[sOrchidIconSpriteIds[i]];
        bool32 sel = (i == sStartMenuCursorPos);

        sprite->oam.paletteNum = (sel || mutedPal == 0xFF) ? normalPal : mutedPal;
        sprite->x = x0 + OSM2_ICON_DX - (sel ? 4 : 0) + 8;
        sprite->y = sOrchidBannerY + OSM2_ICON_DY + i * OSM2_PITCH - (sel ? OSM_ICON_LIFT : 0) + 8;
    }
}

// The pill's cap follows the overworld weather (mock_weather_pill.STYLES); indoor / underground maps keep
// the pin. Cycling weathers (Route 119 / 123, abnormal, dynamic) show the weather running right now.
static u32 OrchidStartMenu_WeatherCap(void)
{
    if (gMapHeader.mapType == MAP_TYPE_INDOOR || gMapHeader.mapType == MAP_TYPE_UNDERGROUND
     || gMapHeader.mapType == MAP_TYPE_SECRET_BASE)
        return ORCHID_WXCAP_INDOOR;

    switch (GetCurrentWeather())
    {
    case WEATHER_DROUGHT:
        return ORCHID_WXCAP_SUN;
    case WEATHER_RAIN:
    case WEATHER_DOWNPOUR:
        return ORCHID_WXCAP_RAIN;
    case WEATHER_RAIN_THUNDERSTORM:
        return ORCHID_WXCAP_STORM;
    case WEATHER_SNOW:
        return ORCHID_WXCAP_SNOW;
    case WEATHER_FOG_HORIZONTAL:
    case WEATHER_FOG_DIAGONAL:
    case WEATHER_FOG:
        return ORCHID_WXCAP_FOG;
    case WEATHER_THICK_SMOG:
        return ORCHID_WXCAP_SMOG;
    case WEATHER_SANDSTORM:
        return ORCHID_WXCAP_SAND;
    case WEATHER_VOLCANIC_ASH:
        return ORCHID_WXCAP_ASH;
    case WEATHER_SHADE:
        return ORCHID_WXCAP_CLOUD;
    case WEATHER_UNDERWATER:
    case WEATHER_UNDERWATER_BUBBLES:
        return ORCHID_WXCAP_WATER;
    default: // NONE, SUNNY, SUNNY_CLOUDS
        return ORCHID_WXCAP_CLEAR;
    }
}

// Location pill straight on the field (mock_start_v2.chip_bare) with the weather cap (mock_weather_pill).
// Its own copy of start_obj.pal: only the 3 cap ramp colours change with the weather.
static void OrchidStartMenu_CreatePill(void)
{
    struct SpriteSheet sheet;
    struct SpritePalette pal = {gOrchidStartObj_Pal, TAG_OSM_PILL_PAL};
    u32 cap = OrchidStartMenu_WeatherCap();
    u8 canvas, palSlot;
    u32 i;

    palSlot = LoadSpritePalette(&pal);
    if (palSlot == 0xFF)
        return;
    LoadPalette(sOrchidWeatherCapRamps[cap], OBJ_PLTT_ID(palSlot) + OSM2_ACCENT_DARK, sizeof(sOrchidWeatherCapRamps[cap]));
    canvas = AddWindow(&sOrchidCanvasTemplate);
    if (canvas == WINDOW_NONE)
    {
        FreeSpritePaletteByTag(TAG_OSM_PILL_PAL);
        return;
    }
    GetMapNameGeneric(gStringVar4, gMapHeader.regionMapSectionId);
    FillWindowPixelBuffer(canvas, PIXEL_FILL(0));
    OrchidDrawRoundedBox(canvas, 0, OSM2_PILL_Y - 8, GetStringWidth(FONT_NORMAL, gStringVar4, 0) + OSM2_PILL_PAD, 14, 4,
                         OSM2_PANEL, OSM2_INK, OSM2_WHITE, OSM2_PANEL_SHADE);
    BlitBitmapRectToWindow(canvas, gOrchidWeatherCaps_Gfx, 0, cap * 16, 24, ORCHID_WXCAP_COUNT * 16, 0, 0, 17, 16);
    AddTextPrinterParameterized4(canvas, FONT_NORMAL, OSM2_PILL_TEXT_DX, 0, 0, 0, sOrchidPillColors, TEXT_SKIP_DRAW, gStringVar4);
    sheet.data = gWindows[canvas].tileData;
    sheet.size = 64 * TILE_SIZE_4BPP; // 2 x 64x32 OBJs (the pill uses the top 16 px)
    sheet.tag = TAG_OSM_PILL;
    LoadSpriteSheet(&sheet);
    OrchidCanvasToObj(canvas, TAG_OSM_PILL, 0, 0, 8, 4);
    OrchidCanvasToObj(canvas, TAG_OSM_PILL, 32, 8, 8, 4);
    RemoveWindow(canvas);
    for (i = 0; i < 2; i++)
    {
        sOrchidPillSpriteIds[i] = CreateSprite(&sSpriteTemplate_OrchidPill, OSM2_PILL_X + 64 * i + 32, 8 + 16, 2);
        if (sOrchidPillSpriteIds[i] != MAX_SPRITES)
            StartSpriteAnim(&gSprites[sOrchidPillSpriteIds[i]], i);
    }
    sOrchidPillShown = TRUE;
}

static void OrchidStartMenu_DestroyPill(void)
{
    u32 i;

    if (!sOrchidPillShown)
        return;
    for (i = 0; i < 2; i++)
    {
        if (sOrchidPillSpriteIds[i] != MAX_SPRITES)
            DestroySprite(&gSprites[sOrchidPillSpriteIds[i]]);
    }
    FreeSpriteTilesByTag(TAG_OSM_PILL);
    FreeSpritePaletteByTag(TAG_OSM_PILL_PAL);
    sOrchidPillShown = FALSE;
}

static void OrchidStartMenu_SetSlide(s32 bannerDx, s32 pillDx)
{
    u32 i;

    if (!sOrchidIconsShown)
        return;
    for (i = 0; i < sOrchidBannerCount; i++)
        gSprites[sOrchidBannerSpriteIds[i]].x2 = bannerDx;
    for (i = 0; i < 2; i++)
        gSprites[sOrchidTabSpriteIds[i]].x2 = bannerDx;
    for (i = 0; i < sNumStartMenuActions; i++)
        gSprites[sOrchidIconSpriteIds[i]].x2 = bannerDx;
    if (sOrchidPillShown)
    {
        for (i = 0; i < 2; i++)
            gSprites[sOrchidPillSpriteIds[i]].x2 = -pillDx;
    }
}

static void Task_OrchidStartMenuSlide(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    if (tSlideMode == SLIDE_OPEN)
    {
        OrchidStartMenu_SetSlide(sOrchidSlideOpen[tSlideFrame][0], sOrchidSlideOpen[tSlideFrame][1]);
        if (tSlideFrame < OSM2_OPEN_FRAMES)
            tSlideFrame++;
        else
            tSlideMode = SLIDE_NONE;
    }
    else if (tSlideMode == SLIDE_CLOSE)
    {
        OrchidStartMenu_SetSlide(sOrchidSlideClose[tSlideFrame][0], sOrchidSlideClose[tSlideFrame][1]);
        if (tSlideFrame < OSM2_CLOSE_FRAMES)
            tSlideFrame++;
    }
}

static void OrchidStartMenu_StartClose(void)
{
    if (!sOrchidIconsShown)
        return;
    gTasks[sOrchidSlideTaskId].tSlideMode = SLIDE_CLOSE;
    gTasks[sOrchidSlideTaskId].tSlideFrame = 0;
}

static bool32 OrchidStartMenu_CloseDone(void)
{
    struct Task *task = &gTasks[sOrchidSlideTaskId];

    return !sOrchidIconsShown || (task->tSlideMode == SLIDE_CLOSE && task->tSlideFrame >= OSM2_CLOSE_FRAMES);
}

// Sprites the field can still create (weather, field effects) beside the menu art; the menu art and the
// saving ball only show when this many slots stay free after them, so they can never starve the field.
#define ORCHID_SPRITE_RESERVE 8

static u32 CountFreeSpriteSlots(void)
{
    u32 i, count = 0;

    for (i = 0; i < MAX_SPRITES; i++)
    {
        if (!gSprites[i].inUse)
            count++;
    }
    return count;
}

static void OrchidStartMenu_CreateIcons(void)
{
    struct SpriteSheet icons = {gOrchidStartMenuIcons_Gfx, ICON_COUNT * 4 * TILE_SIZE_4BPP, TAG_OSM_ICONS};
    struct SpritePalette pal = {gOrchidStartMenuIcons_Pal, TAG_OSM_ICON_PAL};
    struct SpritePalette muted = {gOrchidStartMenuIconsMuted_Pal, TAG_OSM_ICON_MUTED};
    struct SpritePalette objPal = {gOrchidStartObj_Pal, TAG_OSM_OBJ_PAL};
    struct SpriteSheet banner, tab;
    u16 nameColors[2];
    u32 n = sNumStartMenuActions, i, objPalSlot, h;
    s32 x0 = OrchidStartMenu_BannerX();

    if (sOrchidIconsShown || n == 0)
        return;
    if (n > OSM2_MAX_ENTRIES)
        n = OSM2_MAX_ENTRIES;
    // banner (up to 3) + tab (2) + icons + location pill (2)
    if (CountFreeSpriteSlots() < n + sOrchidBannerLayout[n - 1][1] + 2 + 2 + ORCHID_SPRITE_RESERVE)
        return; // the menu still works (and closes), without its art
    if (LoadSpritePalette(&objPal) == 0xFF || LoadSpritePalette(&pal) == 0xFF)
    {
        FreeSpritePaletteByTag(TAG_OSM_OBJ_PAL);
        return; // no free OBJ palette: the menu still works, without its art
    }
    LoadSpritePalette(&muted);
    // the gold tab prints the player's name in the gender name colour (SPARE_A / SPARE_B)
    objPalSlot = IndexOfSpritePaletteTag(TAG_OSM_OBJ_PAL);
    nameColors[0] = (gSaveBlock2Ptr->playerGender == MALE) ? ORCHID_NAME_MALE_FG : ORCHID_NAME_FEMALE_FG;
    nameColors[1] = (gSaveBlock2Ptr->playerGender == MALE) ? ORCHID_NAME_MALE_SHADOW : ORCHID_NAME_FEMALE_SHADOW;
    LoadPalette(nameColors, OBJ_PLTT_ID(objPalSlot) + OSM2_SPARE_A, sizeof(nameColors));

    // banner body for n entries, centred vertically
    h = n * OSM2_PITCH + 6;
    sOrchidBannerY = ((s32)DISPLAY_HEIGHT - (s32)h) / 2;
    sOrchidBannerCount = sOrchidBannerLayout[n - 1][1];
    banner.data = gOrchidStartBanner_Gfx + sOrchidBannerLayout[n - 1][0] * TILE_SIZE_4BPP;
    banner.size = sOrchidBannerCount * 32 * TILE_SIZE_4BPP;
    banner.tag = TAG_OSM_BANNER;
    LoadSpriteSheet(&banner);
    for (i = 0; i < sOrchidBannerCount; i++)
    {
        sOrchidBannerSpriteIds[i] = CreateSprite(&sSpriteTemplate_OrchidBanner, x0 + 16, sOrchidBannerY + 64 * i + 32, 3);
        StartSpriteAnim(&gSprites[sOrchidBannerSpriteIds[i]], i);
    }

    // gold tab: 2 x 64x32 OBJs over the right 128 px, tiles filled by OrchidStartMenu_Select
    tab.data = gOrchidStartBanner_Gfx; // placeholder contents, overwritten before it shows
    tab.size = 64 * TILE_SIZE_4BPP;
    tab.tag = TAG_OSM_TAB;
    LoadSpriteSheet(&tab);
    for (i = 0; i < 2; i++)
    {
        sOrchidTabSpriteIds[i] = CreateSprite(&sSpriteTemplate_OrchidTab, OSM2_TAB_SPRITE_X + 64 * i + 32, 0, 2);
        StartSpriteAnim(&gSprites[sOrchidTabSpriteIds[i]], i);
    }

    LoadSpriteSheet(&icons);
    for (i = 0; i < n; i++)
    {
        u8 spriteId = CreateSprite(&sSpriteTemplate_OrchidIcon, x0 + OSM2_ICON_DX + 8, 0, 1);

        sOrchidIconSpriteIds[i] = spriteId;
        if (spriteId != MAX_SPRITES)
            StartSpriteAnim(&gSprites[spriteId], sOrchidStartMenuIcons[sCurrentStartMenuActions[i]]);
    }
    sOrchidIconsShown = TRUE;

    if (sOrchidChip == ORCHID_CHIP_LOCATION)
        OrchidStartMenu_CreatePill();

    sOrchidSlideTaskId = CreateTask(Task_OrchidStartMenuSlide, 0x50);
    if (sOrchidSlideIn)
    {
        gTasks[sOrchidSlideTaskId].tSlideMode = SLIDE_OPEN;
        OrchidStartMenu_SetSlide(sOrchidSlideOpen[0][0], sOrchidSlideOpen[0][1]);
    }
    sOrchidSlideIn = FALSE;
    OrchidStartMenu_Select();
}

static void OrchidStartMenu_DestroyIcons(void)
{
    u32 i;

    if (!sOrchidIconsShown)
        return;
    for (i = 0; i < sNumStartMenuActions && i < OSM2_MAX_ENTRIES; i++)
    {
        if (sOrchidIconSpriteIds[i] != MAX_SPRITES)
            DestroySprite(&gSprites[sOrchidIconSpriteIds[i]]);
    }
    for (i = 0; i < sOrchidBannerCount; i++)
        DestroySprite(&gSprites[sOrchidBannerSpriteIds[i]]);
    for (i = 0; i < 2; i++)
        DestroySprite(&gSprites[sOrchidTabSpriteIds[i]]);
    OrchidStartMenu_DestroyPill();
    DestroyTask(sOrchidSlideTaskId);
    FreeSpriteTilesByTag(TAG_OSM_ICONS);
    FreeSpriteTilesByTag(TAG_OSM_BANNER);
    FreeSpriteTilesByTag(TAG_OSM_TAB);
    FreeSpritePaletteByTag(TAG_OSM_ICON_PAL);
    FreeSpritePaletteByTag(TAG_OSM_ICON_MUTED);
    FreeSpritePaletteByTag(TAG_OSM_OBJ_PAL);
    sOrchidIconsShown = FALSE;
}

#undef tSlideMode
#undef tSlideFrame

static u8 OrchidStartMenu_AddChipWindow(const struct WindowTemplate *template, u8 chip)
{
    sOrchidChip = chip;
    sOrchidChipWindowId = AddWindow(template);
    DrawStdWindowFrame(sOrchidChipWindowId, FALSE);
    return sOrchidChipWindowId;
}

static void ShowSafariBallsWindow(void)
{
    if (!IS_FRLG)
    {
        // Orchid Safari chip (mock_system.chip_safari): the real SAFARI BALL item icon in a well
        u8 windowId = OrchidStartMenu_AddChipWindow(&sWindowTemplate_SafariBalls, ORCHID_CHIP_SAFARI);

        sSafariBallsWindowId = windowId;
        BlitBitmapRectToWindow(windowId, gOrchidStartChips_Gfx, 0, OSM_CHIP_SAFARI_Y, OSM_CHIP_SHEET_W, 128, 0, 0, 88, 32);
        AddTextPrinterParameterized4(windowId, FONT_NARROW, OSM_SAFARI_TEXT_X, 0, 0, 0, sOrchidTextColors, TEXT_SKIP_DRAW, sText_OrchidSafariBalls);
        ConvertIntToDecimalStringN(gStringVar1, gNumSafariBalls, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringExpandPlaceholders(gStringVar4, sText_OrchidSafariStock);
        AddTextPrinterParameterized4(windowId, FONT_NORMAL, OSM_SAFARI_TEXT_X, 14, 0, 0, sOrchidTextColors, TEXT_SKIP_DRAW, gStringVar4);
        CopyWindowToVram(windowId, COPYWIN_FULL);
        sOrchidSafariIconSpriteId = AddItemIconSprite(TAG_OSM_SAFARI_ICON, TAG_OSM_SAFARI_ICON, ITEM_SAFARI_BALL);
        if (sOrchidSafariIconSpriteId != MAX_SPRITES)
        {
            gSprites[sOrchidSafariIconSpriteId].x = OSM_SAFARI_ICON_X;
            gSprites[sOrchidSafariIconSpriteId].y = OSM_SAFARI_ICON_Y;
            gSprites[sOrchidSafariIconSpriteId].oam.priority = 0;
        }
        return;
    }

    sSafariBallsWindowId = AddWindow(&sWindowTemplate_SafariBalls);
    sOrchidChip = ORCHID_CHIP_SAFARI;
    sOrchidChipWindowId = sSafariBallsWindowId;
    sOrchidSafariIconSpriteId = MAX_SPRITES;
    PutWindowTilemap(sSafariBallsWindowId);
    DrawStdWindowFrame(sSafariBallsWindowId, FALSE);
    if (IS_FRLG)
    {
        ConvertIntToDecimalStringN(gStringVar1, gSafariZoneStepCounter, STR_CONV_MODE_RIGHT_ALIGN, 3);
        ConvertIntToDecimalStringN(gStringVar2, 600, STR_CONV_MODE_RIGHT_ALIGN, 3);
        ConvertIntToDecimalStringN(gStringVar3, gNumSafariBalls, STR_CONV_MODE_RIGHT_ALIGN, 2);
        StringExpandPlaceholders(gStringVar4, gText_MenuSafariStats);
        AddTextPrinterParameterized(sSafariBallsWindowId, FONT_NORMAL, gStringVar4, 4, 3, 0xFF, NULL);
    }
    else
    {
        ConvertIntToDecimalStringN(gStringVar1, gNumSafariBalls, STR_CONV_MODE_RIGHT_ALIGN, 2);
        StringExpandPlaceholders(gStringVar4, gText_SafariBallStock);
        AddTextPrinterParameterized(sSafariBallsWindowId, FONT_NORMAL, gStringVar4, 0, 1, TEXT_SKIP_DRAW, NULL);
    }
    CopyWindowToVram(sSafariBallsWindowId, COPYWIN_FULL);
}

// Orchid Pyramid chip (mock_system.chip_pyramid): "Battle Pyramid", 7 floor pips (cleared gold, current
// accent, ahead recessed) and the floor name.
static void ShowPyramidFloorWindow(void)
{
    u32 floor = gSaveBlock2Ptr->frontier.curChallengeBattleNum;
    u32 k;
    s32 floorX;
    u8 windowId;

    if (floor > FRONTIER_STAGES_PER_CHALLENGE)
        floor = FRONTIER_STAGES_PER_CHALLENGE;
    windowId = OrchidStartMenu_AddChipWindow(&sWindowTemplate_PyramidFloor, ORCHID_CHIP_PYRAMID);
    sBattlePyramidFloorWindowId = windowId;
    BlitBitmapRectToWindow(windowId, gOrchidStartChips_Gfx, 0, OSM_CHIP_PYRAMID_Y, OSM_CHIP_SHEET_W, 128, 0, 0, 96, 32);
    for (k = 0; k < FRONTIER_STAGES_PER_CHALLENGE; k++)
    {
        u32 kind = (k < floor) ? 0 : (k == floor ? 1 : 2);

        BlitBitmapRectToWindow(windowId, gOrchidStartChips_Gfx, 0, OSM_CHIP_PIPS_Y + kind * OSM_PIP_CELL, OSM_CHIP_SHEET_W, 128,
                               OSM_PIP_X0 + 9 * k, OSM_PIP_Y, OSM_PIP_W, 10);
    }
    // the mock's "Floor N" runs 2 px into the frame; keep it inside the 96 px window
    floorX = 96 - GetStringWidth(FONT_NARROW, sPyramidFloorNames[floor], 0);
    if (floorX > OSM_PYRAMID_FLOOR_X)
        floorX = OSM_PYRAMID_FLOOR_X;
    AddTextPrinterParameterized4(windowId, FONT_NARROW, floorX, OSM_PYRAMID_FLOOR_Y, 0, 0, sOrchidTextColors,
                                 TEXT_SKIP_DRAW, sPyramidFloorNames[floor]);
    CopyWindowToVram(windowId, COPYWIN_FULL);
}

// Removes the info chip (location / Safari / Pyramid) and the menu icons; safe to call more than once.
static void RemoveExtraStartMenuWindows(void)
{
    OrchidStartMenu_DestroyIcons();
    if (sOrchidChip == ORCHID_CHIP_NONE)
        return;
    if (sOrchidChip == ORCHID_CHIP_SAFARI && !IS_FRLG && sOrchidSafariIconSpriteId != MAX_SPRITES)
    {
        FreeSpriteTilesByTag(TAG_OSM_SAFARI_ICON);
        FreeSpritePaletteByTag(TAG_OSM_SAFARI_ICON);
        DestroySprite(&gSprites[sOrchidSafariIconSpriteId]);
    }
    if (sOrchidChip != ORCHID_CHIP_LOCATION) // the location pill is OBJ (gone with the icons)
    {
        ClearStdWindowAndFrameToTransparent(sOrchidChipWindowId, FALSE);
        CopyWindowToVram(sOrchidChipWindowId, COPYWIN_FULL);
        RemoveWindow(sOrchidChipWindowId);
    }
    sOrchidChip = ORCHID_CHIP_NONE;
}

static bool32 InitStartMenuStep(void)
{
    s8 state = sInitStartMenuData[0];

    switch (state)
    {
    case 0:
        sInitStartMenuData[0]++;
        break;
    case 1:
        BuildStartMenuActions();
        sInitStartMenuData[0]++;
        break;
    case 2:
        LoadMessageBoxAndBorderGfx();
        LoadOrchidFieldWindowPalette();
        sInitStartMenuData[1] = 0;
        sInitStartMenuData[0]++;
        break;
    case 3:
        if (sOrchidChip == ORCHID_CHIP_NONE)
        {
            if (GetSafariZoneFlag())
                ShowSafariBallsWindow();
            else if (CurrentBattlePyramidLocation() != PYRAMID_LOCATION_NONE)
                ShowPyramidFloorWindow();
            else
                sOrchidChip = ORCHID_CHIP_LOCATION; // the pill is OBJ, made with the banner
        }
        sInitStartMenuData[0]++;
        break;
    case 4:
        sInitStartMenuData[0]++;
        break;
    case 5:
        // Orchid start menu v2: no window, the banner / tab / icons are OBJ
        if (sStartMenuCursorPos >= sNumStartMenuActions)
            sStartMenuCursorPos = 0;
        OrchidStartMenu_CreateIcons();
        return TRUE;
    }

    return FALSE;
}

static void InitStartMenu(void)
{
    sInitStartMenuData[0] = 0;
    sInitStartMenuData[1] = 0;
    while (!InitStartMenuStep())
        ;
}

static void StartMenuTask(u8 taskId)
{
    if (InitStartMenuStep() == TRUE)
        SwitchTaskToFollowupFunc(taskId);
}

static void CreateStartMenuTask(TaskFunc followupFunc)
{
    u8 taskId;

    sInitStartMenuData[0] = 0;
    sInitStartMenuData[1] = 0;
    taskId = CreateTask(StartMenuTask, 0x50);
    SetTaskFuncWithFollowupFunc(taskId, StartMenuTask, followupFunc);
}

static bool8 FieldCB_ReturnToFieldStartMenu(void)
{
    if (InitStartMenuStep() == FALSE)
    {
        return FALSE;
    }

    ReturnToFieldOpenStartMenu();
    return TRUE;
}

// Orchid: nothing of an earlier start menu / save can still be on screen when one opens afresh (field reload,
// soft reset), so forget any chip / icon / ball state left behind.
static void OrchidStartMenu_ResetState(void)
{
    sOrchidChip = ORCHID_CHIP_NONE;
    sOrchidIconsShown = FALSE;
    sOrchidPillShown = FALSE;
    sOrchidBallShown = FALSE;
    sOrchidSlideIn = FALSE;
}

void ShowReturnToFieldStartMenu(void)
{
    OrchidStartMenu_ResetState();
    sInitStartMenuData[0] = 0;
    sInitStartMenuData[1] = 0;
    gFieldCallback2 = FieldCB_ReturnToFieldStartMenu;
}

void Task_ShowStartMenu(u8 taskId)
{
    struct Task *task = &gTasks[taskId];

    switch (task->data[0])
    {
    case 0:
        if (InUnionRoom() == TRUE)
            SetUsingUnionRoomStartMenu();

        gMenuCallback = HandleStartMenuInput;
        task->data[0]++;
        break;
    case 1:
        if (gMenuCallback() == TRUE)
            DestroyTask(taskId);
        break;
    }
}

void ShowStartMenu(void)
{
    OrchidStartMenu_ResetState();
    sOrchidSlideIn = TRUE;
    if (!IsOverworldLinkActive())
    {
        FreezeObjectEvents();
        PlayerFreeze();
        StopPlayerAvatar();
    }
    CreateStartMenuTask(Task_ShowStartMenu);
    LockPlayerFieldControls();
}

static bool8 HandleStartMenuInput(void)
{
    if (JOY_NEW(DPAD_UP))
    {
        PlaySE(SE_SELECT);
        sStartMenuCursorPos = (sStartMenuCursorPos == 0) ? sNumStartMenuActions - 1 : sStartMenuCursorPos - 1;
        OrchidStartMenu_Select();
    }

    if (JOY_NEW(DPAD_DOWN))
    {
        PlaySE(SE_SELECT);
        sStartMenuCursorPos = (sStartMenuCursorPos + 1 >= sNumStartMenuActions) ? 0 : sStartMenuCursorPos + 1;
        OrchidStartMenu_Select();
    }

    if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        if (sStartMenuItems[sCurrentStartMenuActions[sStartMenuCursorPos]].func.u8_void == StartMenuPokedexCallback)
        {
            if (GetNationalPokedexCount(FLAG_GET_SEEN) == 0)
                return FALSE;
        }
        if (sCurrentStartMenuActions[sStartMenuCursorPos] == MENU_ACTION_DEXNAV
          && MapHasNoEncounterData())
            return FALSE;

        gMenuCallback = sStartMenuItems[sCurrentStartMenuActions[sStartMenuCursorPos]].func.u8_void;

        if (gMenuCallback != StartMenuSaveCallback
            && gMenuCallback != StartMenuExitCallback
            && gMenuCallback != StartMenuDebugCallback
            && gMenuCallback != StartMenuSafariZoneRetireCallback
            && gMenuCallback != StartMenuBattlePyramidRetireCallback)
        {
           FadeScreen(FADE_TO_BLACK, 0);
        }

        return FALSE;
    }

    if (JOY_NEW(START_BUTTON | B_BUTTON))
    {
        PlaySE(SE_SELECT);
        OrchidStartMenu_StartClose();
        gMenuCallback = HandleStartMenuClose;
        return FALSE;
    }

    return FALSE;
}

bool8 StartMenuPokedexCallback(void)
{
    if (!gPaletteFade.active)
    {
        IncrementGameStat(GAME_STAT_CHECKED_POKEDEX);
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_OpenPokedex);

        return TRUE;
    }

    return FALSE;
}

static bool8 StartMenuPokemonCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_PartyMenuFromStartMenu); // Display party menu

        return TRUE;
    }

    return FALSE;
}

static bool8 StartMenuBagCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_BagMenuFromStartMenu); // Display bag menu

        return TRUE;
    }

    return FALSE;
}

static bool8 StartMenuPhoneCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_InitRotomPhone);  // Display the Rotom Phone

        return TRUE;
    }

    return FALSE;
}

static bool8 StartMenuPlayerNameCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();

        if (IsOverworldLinkActive() || InUnionRoom())
            ShowPlayerTrainerCard(CB2_ReturnToFieldWithOpenMenu); // Display trainer card
        else if (FlagGet(FLAG_SYS_FRONTIER_PASS))
            ShowFrontierPass(CB2_ReturnToFieldWithOpenMenu); // Display frontier pass
        else
            ShowPlayerTrainerCard(CB2_ReturnToFieldWithOpenMenu); // Display trainer card

        return TRUE;
    }

    return FALSE;
}

static bool8 StartMenuSaveCallback(void)
{
    if (CurrentBattlePyramidLocation() != PYRAMID_LOCATION_NONE)
        RemoveExtraStartMenuWindows();

    gMenuCallback = SaveStartCallback; // Display save menu

    return FALSE;
}

static bool8 StartMenuOptionCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_InitOptionMenu); // Display option menu
        gMain.savedCallback = CB2_ReturnToFieldWithOpenMenu;

        return TRUE;
    }

    return FALSE;
}

// Orchid: EXIT slides the menu out like START / B (A already played the select sound)
static bool8 StartMenuExitCallback(void)
{
    OrchidStartMenu_StartClose();
    gMenuCallback = HandleStartMenuClose;
    return FALSE;
}

// Orchid: the banner and the pill slide out (8 frames), then the menu closes as vanilla's START / B
static bool8 HandleStartMenuClose(void)
{
    if (!OrchidStartMenu_CloseDone())
        return FALSE;
    RemoveExtraStartMenuWindows();
    HideStartMenuWindow();
    return TRUE;
}

static bool8 StartMenuDebugCallback(void)
{
    RemoveExtraStartMenuWindows();
    HideStartMenuDebug(); // Hide start menu without enabling movement

    if (DEBUG_OVERWORLD_MENU)
    {
        FreezeObjectEvents();
        Debug_ShowMainMenu();
    }

return TRUE;
}

static bool8 StartMenuSafariZoneRetireCallback(void)
{
    RemoveExtraStartMenuWindows();
    HideStartMenu();
    SafariZoneRetirePrompt();

    return TRUE;
}

static void HideStartMenuDebug(void)
{
    OrchidStartMenu_DestroyIcons();
    PlaySE(SE_SELECT);
}

static bool8 StartMenuLinkModePlayerNameCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        ShowTrainerCardInLink(gLocalLinkPlayerId, CB2_ReturnToFieldWithOpenMenu);

        return TRUE;
    }

    return FALSE;
}

static bool8 StartMenuBattlePyramidRetireCallback(void)
{
    gMenuCallback = BattlePyramidRetireStartCallback; // Confirm retire

    return FALSE;
}

// Functionally unused
void ShowBattlePyramidStartMenu(void)
{
    ClearDialogWindowAndFrameToTransparent(0, FALSE);
    ScriptUnfreezeObjectEvents();
    CreateStartMenuTask(Task_ShowStartMenu);
    LockPlayerFieldControls();
}

static bool8 StartMenuBattlePyramidBagCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_PyramidBagMenuFromStartMenu);

        return TRUE;
    }

    return FALSE;
}

static bool8 SaveStartCallback(void)
{
    InitSave();
    gMenuCallback = SaveCallback;

    return FALSE;
}

static bool8 SaveCallback(void)
{
    switch (RunSaveCallback())
    {
    case SAVE_IN_PROGRESS:
        return FALSE;
    case SAVE_CANCELED: // Back to start menu
        ClearDialogWindowAndFrameToTransparent(0, FALSE);
        InitStartMenu();
        gMenuCallback = HandleStartMenuInput;
        return FALSE;
    case SAVE_SUCCESS:
    case SAVE_ERROR:    // Close start menu
        ClearDialogWindowAndFrameToTransparent(0, TRUE);
        ScriptUnfreezeObjectEvents();
        UnlockPlayerFieldControls();
        SoftResetInBattlePyramid();
        return TRUE;
    }

    return FALSE;
}

static bool8 BattlePyramidRetireStartCallback(void)
{
    InitBattlePyramidRetire();
    gMenuCallback = BattlePyramidRetireCallback;

    return FALSE;
}

static bool8 BattlePyramidRetireReturnCallback(void)
{
    InitStartMenu();
    gMenuCallback = HandleStartMenuInput;

    return FALSE;
}

static bool8 BattlePyramidRetireCallback(void)
{
    switch (RunSaveCallback())
    {
    case SAVE_SUCCESS: // No (Stay in battle pyramid)
        RemoveExtraStartMenuWindows();
        gMenuCallback = BattlePyramidRetireReturnCallback;
        return FALSE;
    case SAVE_IN_PROGRESS:
        return FALSE;
    case SAVE_CANCELED: // Yes (Retire from battle pyramid)
        ClearDialogWindowAndFrameToTransparent(0, TRUE);
        ScriptUnfreezeObjectEvents();
        UnlockPlayerFieldControls();
        ScriptContext_SetupScript(BattlePyramid_Retire);
        return TRUE;
    }

    return FALSE;
}

static void InitSave(void)
{
    sOrchidBallShown = FALSE;
    SaveMapView();
    sSaveDialogCallback = SaveConfirmSaveCallback;
    sSavingComplete = FALSE;
}

static u8 RunSaveCallback(void)
{
    // True if text is still printing
    if (RunTextPrintersAndIsPrinter0Active() == TRUE)
    {
        return SAVE_IN_PROGRESS;
    }

    sSavingComplete = FALSE;
    return sSaveDialogCallback();
}

void SaveGame(void)
{
    InitSave();
    CreateTask(SaveGameTask, 0x50);
}

static void ShowSaveMessage(const u8 *message, u8 (*saveCallback)(void))
{
    StringExpandPlaceholders(gStringVar4, message);
    LoadMessageBoxAndFrameGfx(0, TRUE);
    AddTextPrinterForMessage(TRUE);
    sSavingComplete = TRUE;
    sSaveDialogCallback = saveCallback;
}

static void SaveGameTask(u8 taskId)
{
    u8 status = RunSaveCallback();

    switch (status)
    {
    case SAVE_CANCELED:
    case SAVE_ERROR:
        gSpecialVar_Result = 0;
        break;
    case SAVE_SUCCESS:
        gSpecialVar_Result = status;
        break;
    case SAVE_IN_PROGRESS:
        return;
    }

    DestroyTask(taskId);
    ScriptContext_Enable();
}

static void HideSaveMessageWindow(void)
{
    ClearDialogWindowAndFrame(0, TRUE);
}

static void HideSaveInfoWindow(void)
{
    RemoveSaveInfoWindow();
}

static void SaveStartTimer(void)
{
    sSaveDialogTimer = 60;
}

static bool8 SaveSuccesTimer(void)
{
    sSaveDialogTimer--;

    if (JOY_HELD(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        return TRUE;
    }
    if (sSaveDialogTimer == 0)
    {
        return TRUE;
    }

    return FALSE;
}

static bool8 SaveErrorTimer(void)
{
    if (sSaveDialogTimer != 0)
    {
        sSaveDialogTimer--;
    }
    else if (JOY_HELD(A_BUTTON))
    {
        return TRUE;
    }

    return FALSE;
}

static u8 SaveConfirmSaveCallback(void)
{
    RemoveExtraStartMenuWindows(); // Orchid: the info chip sits where the save card goes; icons go with the menu
    OrchidStartMenu_DestroyIcons();
    ShowSaveInfoWindow();

    if (CurrentBattlePyramidLocation() != PYRAMID_LOCATION_NONE)
    {
        ShowSaveMessage(gText_BattlePyramidConfirmRest, SaveYesNoCallback);
    }
    else
    {
        ShowSaveMessage(gText_ConfirmSave, SaveYesNoCallback);
    }

    return SAVE_IN_PROGRESS;
}

static u8 SaveYesNoCallback(void)
{
    DisplayYesNoMenuDefaultYes(); // Show Yes/No menu
    sSaveDialogCallback = SaveConfirmInputCallback;
    return SAVE_IN_PROGRESS;
}

static u8 SaveConfirmInputCallback(void)
{
    switch (Menu_ProcessInputNoWrapClearOnChoose())
    {
    case 0: // Yes
        switch (gSaveFileStatus)
        {
        case SAVE_STATUS_EMPTY:
        case SAVE_STATUS_CORRUPT:
            if (gDifferentSaveFile == FALSE && !SKIP_SAVE_CONFIRMATION)
            {
                sSaveDialogCallback = SaveFileExistsCallback;
                return SAVE_IN_PROGRESS;
            }

            sSaveDialogCallback = SaveSavingMessageCallback;
            return SAVE_IN_PROGRESS;
        default:
            if (SKIP_SAVE_CONFIRMATION)
                sSaveDialogCallback = SaveSavingMessageCallback;
            else
                sSaveDialogCallback = SaveFileExistsCallback;
            return SAVE_IN_PROGRESS;
        }
    case MENU_B_PRESSED:
    case 1: // No
        HideSaveInfoWindow();
        HideSaveMessageWindow();
        return SAVE_CANCELED;
    }

    return SAVE_IN_PROGRESS;
}

// A different save file exists
static u8 SaveFileExistsCallback(void)
{
    if (gDifferentSaveFile == TRUE)
    {
        ShowSaveMessage(gText_DifferentSaveFile, SaveConfirmOverwriteDefaultNoCallback);
    }
    else
    {
        ShowSaveMessage(gText_AlreadySavedFile, SaveConfirmOverwriteCallback);
    }

    return SAVE_IN_PROGRESS;
}

static u8 SaveConfirmOverwriteDefaultNoCallback(void)
{
    DisplayYesNoMenuWithDefault(1); // Show Yes/No menu (No selected as default)
    sSaveDialogCallback = SaveOverwriteInputCallback;
    return SAVE_IN_PROGRESS;
}

static u8 SaveConfirmOverwriteCallback(void)
{
    DisplayYesNoMenuDefaultYes(); // Show Yes/No menu
    sSaveDialogCallback = SaveOverwriteInputCallback;
    return SAVE_IN_PROGRESS;
}

static u8 SaveOverwriteInputCallback(void)
{
    switch (Menu_ProcessInputNoWrapClearOnChoose())
    {
    case 0: // Yes
        sSaveDialogCallback = SaveSavingMessageCallback;
        return SAVE_IN_PROGRESS;
    case MENU_B_PRESSED:
    case 1: // No
        HideSaveInfoWindow();
        HideSaveMessageWindow();
        return SAVE_CANCELED;
    }

    return SAVE_IN_PROGRESS;
}

// ---------------------------------------------------------------- Orchid saving ball
// A small Poké Ball after "SAVING…" rocks like a capture wobble (3 rocks, mock_system.saving_gif), then the
// save runs; it clicks with sparkles and sits after "<PLAYER> saved the game." with twinkling sparkles.
enum
{
    BALL_ROCK,
    BALL_CLICK,
    BALL_SAVED,
};

#define sBallState   data[0]
#define sBallCounter data[1]
#define sBallRocks   data[2]

static u32 GetMessageFirstLineWidth(const u8 *str)
{
    u8 line[64];
    u32 i;

    for (i = 0; i < ARRAY_COUNT(line) - 1 && str[i] != EOS && str[i] != CHAR_NEWLINE
                && str[i] != CHAR_PROMPT_SCROLL && str[i] != CHAR_PROMPT_CLEAR; i++)
        line[i] = str[i];
    line[i] = EOS;
    return GetStringWidth(FONT_NORMAL, line, 0);
}

// Ball top-left x after the first line of the message in gStringVar4 (field message text starts at x 16)
static s32 OrchidSaveBall_X(void)
{
    return 16 + GetMessageFirstLineWidth(gStringVar4) + OSM_BALL_DX;
}

static void OrchidSaveBall_PlaceSparkles(s32 ballX)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sOrchidSparkleSpriteIds); i++)
    {
        struct Sprite *sparkle = &gSprites[sOrchidSparkleSpriteIds[i]];

        sparkle->x = ballX + sOrchidSaveSparkles[i][0] + 4;
        sparkle->y = OSM_BALL_Y + sOrchidSaveSparkles[i][1] + 4;
    }
}

static void SpriteCB_OrchidSaveBall(struct Sprite *sprite)
{
    switch (sprite->sBallState)
    {
    case BALL_ROCK:
        StartSpriteAnimIfDifferent(sprite, sOrchidSaveBallRock[sprite->sBallCounter]);
        if (++sprite->sBallCounter >= OSM_ROCK_LEN)
        {
            sprite->sBallCounter = 0;
            sprite->sBallRocks++;
        }
        break;
    default:
        StartSpriteAnimIfDifferent(sprite, OSM_BALL_REST);
        sprite->sBallCounter++;
        break;
    }
}

static void SpriteCB_OrchidSparkle(struct Sprite *sprite)
{
    struct Sprite *ball = &gSprites[sOrchidBallSpriteId];

    if (ball->sBallState == BALL_CLICK)
        sprite->invisible = FALSE;
    else if (ball->sBallState == BALL_SAVED)
        sprite->invisible = ((ball->sBallCounter / OSM_TWINKLE) % 2) != 0;
    else
        sprite->invisible = TRUE;
}

static void OrchidSaveBall_Create(void)
{
    struct SpriteSheet ball = {gOrchidSaveBall_Gfx, 5 * 4 * TILE_SIZE_4BPP, TAG_OSM_BALL};
    struct SpriteSheet sparkles = {gOrchidSaveSparkles_Gfx, 2 * TILE_SIZE_4BPP, TAG_OSM_SPARKLES};
    struct SpritePalette pal = {gOrchidStartMenuIcons_Pal, TAG_OSM_ICON_PAL};
    s32 x = OrchidSaveBall_X();
    u32 i;

    if (sOrchidBallShown)
        return;
    if (CountFreeSpriteSlots() < 1 + ARRAY_COUNT(sOrchidSparkleSpriteIds) + ORCHID_SPRITE_RESERVE)
        return; // save without the ball
    if (LoadSpritePalette(&pal) == 0xFF)
        return; // no free OBJ palette: save without the ball
    LoadSpriteSheet(&ball);
    LoadSpriteSheet(&sparkles);
    sOrchidBallSpriteId = CreateSprite(&sSpriteTemplate_OrchidSaveBall, x + 8, OSM_BALL_Y + 8, 0);
    for (i = 0; i < ARRAY_COUNT(sOrchidSparkleSpriteIds); i++)
    {
        sOrchidSparkleSpriteIds[i] = CreateSprite(&sSpriteTemplate_OrchidSparkle, 0, 0, 0);
        StartSpriteAnim(&gSprites[sOrchidSparkleSpriteIds[i]], sOrchidSaveSparkles[i][2]);
        gSprites[sOrchidSparkleSpriteIds[i]].invisible = TRUE;
    }
    OrchidSaveBall_PlaceSparkles(x);
    sOrchidBallShown = TRUE;
}

static void OrchidSaveBall_Destroy(void)
{
    u32 i;

    if (!sOrchidBallShown)
        return;
    DestroySprite(&gSprites[sOrchidBallSpriteId]);
    for (i = 0; i < ARRAY_COUNT(sOrchidSparkleSpriteIds); i++)
        DestroySprite(&gSprites[sOrchidSparkleSpriteIds[i]]);
    FreeSpriteTilesByTag(TAG_OSM_BALL);
    FreeSpriteTilesByTag(TAG_OSM_SPARKLES);
    FreeSpritePaletteByTag(TAG_OSM_ICON_PAL);
    sOrchidBallShown = FALSE;
}

// The save waits for 3 full rocks, and runs while the ball is upright.
static bool32 OrchidSaveBall_ReadyToSave(void)
{
    struct Sprite *ball = &gSprites[sOrchidBallSpriteId];

    if (!sOrchidBallShown)
        return TRUE;
    return ball->sBallRocks >= OSM_ROCKS && (ball->sBallCounter == 0 || sOrchidSaveBallRock[ball->sBallCounter] == OSM_BALL_REST);
}

static void OrchidSaveBall_SetState(u32 state)
{
    if (sOrchidBallShown)
    {
        gSprites[sOrchidBallSpriteId].sBallState = state;
        gSprites[sOrchidBallSpriteId].sBallCounter = 0;
    }
}

static bool32 OrchidSaveBall_ClickDone(void)
{
    return !sOrchidBallShown || gSprites[sOrchidBallSpriteId].sBallCounter >= OSM_CLICK_FRAMES;
}

// Saved: the ball moves after the new message's first line, sparkles twinkle around it.
static void OrchidSaveBall_Saved(void)
{
    s32 x = OrchidSaveBall_X();

    if (!sOrchidBallShown)
        return;
    OrchidSaveBall_SetState(BALL_SAVED);
    gSprites[sOrchidBallSpriteId].x = x + 8;
    OrchidSaveBall_PlaceSparkles(x);
}

#undef sBallState
#undef sBallCounter
#undef sBallRocks

static u8 SaveSavingMessageCallback(void)
{
    ShowSaveMessage(gText_SavingDontTurnOff, SaveDoSaveCallback);
    OrchidSaveBall_Create();
    return SAVE_IN_PROGRESS;
}

static u8 SaveDoSaveCallback(void)
{
    u8 saveStatus;

    if (!OrchidSaveBall_ReadyToSave())
        return SAVE_IN_PROGRESS;

    IncrementGameStat(GAME_STAT_SAVED_GAME);
    PausePyramidChallenge();

    if (gDifferentSaveFile == TRUE)
    {
        saveStatus = TrySavingData(SAVE_OVERWRITE_DIFFERENT_FILE);
        gDifferentSaveFile = FALSE;
    }
    else
    {
        saveStatus = TrySavingData(SAVE_NORMAL);
    }

    if (saveStatus == SAVE_STATUS_OK)
    {
        OrchidSaveBall_SetState(BALL_CLICK);
        sSaveDialogCallback = SaveClickCallback;
    }
    else
    {
        OrchidSaveBall_Destroy();
        ShowSaveMessage(gText_SaveError, SaveErrorCallback);
    }

    SaveStartTimer();
    return SAVE_IN_PROGRESS;
}

// Orchid: the ball clicks (sparkles) for a moment before "<PLAYER> saved the game."
static u8 SaveClickCallback(void)
{
    if (!OrchidSaveBall_ClickDone())
        return SAVE_IN_PROGRESS;
    ShowSaveMessage(gText_PlayerSavedGame, SaveSuccessCallback);
    OrchidSaveBall_Saved();
    return SAVE_IN_PROGRESS;
}

static u8 SaveSuccessCallback(void)
{
    if (!IsTextPrinterActiveOnWindow(0))
    {
        PlaySE(SE_SAVE);
        sSaveDialogCallback = SaveReturnSuccessCallback;
    }

    return SAVE_IN_PROGRESS;
}

static u8 SaveReturnSuccessCallback(void)
{
    if (!IsSEPlaying() && SaveSuccesTimer())
    {
        HideSaveInfoWindow();
        return SAVE_SUCCESS;
    }
    else
    {
        return SAVE_IN_PROGRESS;
    }
}

static u8 SaveErrorCallback(void)
{
    if (!IsTextPrinterActiveOnWindow(0))
    {
        PlaySE(SE_BOO);
        sSaveDialogCallback = SaveReturnErrorCallback;
    }

    return SAVE_IN_PROGRESS;
}

static u8 SaveReturnErrorCallback(void)
{
    if (!SaveErrorTimer())
    {
        return SAVE_IN_PROGRESS;
    }
    else
    {
        HideSaveInfoWindow();
        return SAVE_ERROR;
    }
}

static void InitBattlePyramidRetire(void)
{
    sSaveDialogCallback = BattlePyramidConfirmRetireCallback;
    sSavingComplete = FALSE;
}

static u8 BattlePyramidConfirmRetireCallback(void)
{
    OrchidStartMenu_DestroyIcons();
    OrchidStartMenu_DestroyIcons();
    ShowSaveMessage(gText_BattlePyramidConfirmRetire, BattlePyramidRetireYesNoCallback);

    return SAVE_IN_PROGRESS;
}

static u8 BattlePyramidRetireYesNoCallback(void)
{
    DisplayYesNoMenuWithDefault(1); // Show Yes/No menu (No selected as default)
    sSaveDialogCallback = BattlePyramidRetireInputCallback;

    return SAVE_IN_PROGRESS;
}

static u8 BattlePyramidRetireInputCallback(void)
{
    switch (Menu_ProcessInputNoWrapClearOnChoose())
    {
    case 0: // Yes
        return SAVE_CANCELED;
    case MENU_B_PRESSED:
    case 1: // No
        HideSaveMessageWindow();
        return SAVE_SUCCESS;
    }

    return SAVE_IN_PROGRESS;
}

static void VBlankCB_LinkBattleSave(void)
{
    TransferPlttBuffer();
}

static bool32 InitSaveWindowAfterLinkBattle(u8 *state)
{
    switch (*state)
    {
    case 0:
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0);
        SetVBlankCallback(NULL);
        ScanlineEffect_Stop();
        DmaClear16(3, PLTT, PLTT_SIZE);
        DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
        break;
    case 1:
        ResetSpriteData();
        ResetTasks();
        ResetPaletteFade();
        ScanlineEffect_Clear();
        break;
    case 2:
        ResetBgsAndClearDma3BusyFlags(0);
        InitBgsFromTemplates(0, sBgTemplates_LinkBattleSave, ARRAY_COUNT(sBgTemplates_LinkBattleSave));
        InitWindows(sWindowTemplates_LinkBattleSave);
        LoadUserWindowBorderGfx_(0, 8, BG_PLTT_ID(14));
        Menu_LoadStdPalAt(BG_PLTT_ID(15));
        break;
    case 3:
        ShowBg(0);
        BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
        SetVBlankCallback(VBlankCB_LinkBattleSave);
        EnableInterrupts(1);
        break;
    case 4:
        return TRUE;
    }

    (*state)++;
    return FALSE;
}

void CB2_SetUpSaveAfterLinkBattle(void)
{
    if (InitSaveWindowAfterLinkBattle(&gMain.state))
    {
        CreateTask(Task_SaveAfterLinkBattle, 0x50);
        SetMainCallback2(CB2_SaveAfterLinkBattle);
    }
}

static void CB2_SaveAfterLinkBattle(void)
{
    RunTasks();
    UpdatePaletteFade();
}

static void Task_SaveAfterLinkBattle(u8 taskId)
{
    s16 *state = gTasks[taskId].data;

    if (!gPaletteFade.active)
    {
        switch (*state)
        {
        case 0:
            FillWindowPixelBuffer(0, PIXEL_FILL(1));
            AddTextPrinterParameterized2(0,
                                        FONT_NORMAL,
                                        gText_SavingDontTurnOffPower,
                                        TEXT_SKIP_DRAW,
                                        NULL,
                                        TEXT_COLOR_DARK_GRAY,
                                        TEXT_COLOR_WHITE,
                                        TEXT_COLOR_LIGHT_GRAY);
            DrawTextBorderOuter(0, 8, 14);
            PutWindowTilemap(0);
            CopyWindowToVram(0, COPYWIN_FULL);
            BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);

            if (gWirelessCommType != 0 && InUnionRoom())
            {
                if (Link_AnyPartnersPlayingFRLG_JP())
                {
                    *state = 1;
                }
                else
                {
                    *state = 5;
                }
            }
            else
            {
                gSoftResetDisabled = TRUE;
                *state = 1;
            }
            break;
        case 1:
            SetContinueGameWarpStatusToDynamicWarp();
            WriteSaveBlock2();
            *state = 2;
            break;
        case 2:
            if (WriteSaveBlock1Sector())
            {
                ClearContinueGameWarpStatus2();
                *state = 3;
                gSoftResetDisabled = FALSE;
            }
            break;
        case 3:
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            *state = 4;
            break;
        case 4:
            FreeAllWindowBuffers();
            SetMainCallback2(gMain.savedCallback);
            DestroyTask(taskId);
            break;
        case 5:
            CreateTask(Task_LinkFullSave, 5);
            *state = 6;
            break;
        case 6:
            if (!FuncIsActiveTask(Task_LinkFullSave))
            {
                *state = 3;
            }
            break;
        }
    }
}

// Orchid save card (system_ext.save_card): purple location band with a pin, then label pills with white
// pictograms (player, badges, caught, time). The player name uses the gender name colour.
static void ShowSaveInfoWindow(void)
{
    struct WindowTemplate saveInfoWindow = sSaveInfoWindowTemplate;
    static const u8 sValueIds[] = {SAVE_MENU_NAME, SAVE_MENU_BADGES, SAVE_MENU_CAUGHT, SAVE_MENU_PLAY_TIME};
    const u8 *const labels[] = {gText_SavingPlayer, gText_SavingBadges, gText_SavingPokedex, gText_SavingTime};
    bool32 hasDex = FlagGet(FLAG_SYS_POKEDEX_GET);
    u32 i, row;

    if (!hasDex)
        saveInfoWindow.height -= 2;

    LoadOrchidFieldWindowPalette();
    sSaveInfoWindowId = AddWindow(&saveInfoWindow);
    DrawStdWindowFrame(sSaveInfoWindowId, FALSE);

    // location band (save_card.png row 0)
    BlitBitmapRectToWindow(sSaveInfoWindowId, gOrchidSaveCard_Gfx, 0, 0, OSM_CARD_W, 80, 0, 0, OSM_CARD_W, 16);
    GetMapNameGeneric(gStringVar4, gMapHeader.regionMapSectionId);
    AddTextPrinterParameterized4(sSaveInfoWindowId, FONT_NORMAL,
                                 (OSM_CARD_W - GetStringWidth(FONT_NORMAL, gStringVar4, 0)) / 2 + OSM_CARD_LOC_DX, 0,
                                 0, 0, sOrchidLocationColors, TEXT_SKIP_DRAW, gStringVar4);

    // PLAYER / BADGES / POKéDEX / TIME rows (save_card.png rows 1-4)
    for (i = 0, row = 1; i < ARRAY_COUNT(sValueIds); i++)
    {
        if (sValueIds[i] == SAVE_MENU_CAUGHT && !hasDex)
            continue;
        BlitBitmapRectToWindow(sSaveInfoWindowId, gOrchidSaveCard_Gfx, 0, (i + 1) * 16, OSM_CARD_W, 80, 0, row * 16, OSM_CARD_W, 16);
        AddTextPrinterParameterized4(sSaveInfoWindowId, FONT_NARROW, OSM_CARD_LABEL_X, row * 16, 0, 0, sOrchidTextColors, TEXT_SKIP_DRAW, labels[i]);
        BufferSaveMenuText(sValueIds[i], gStringVar4, (sValueIds[i] == SAVE_MENU_NAME) ? OSM_NAME_FG : OSM_INK);
        AddTextPrinterParameterized4(sSaveInfoWindowId, FONT_NORMAL, OSM_CARD_VALUE_R - GetStringWidth(FONT_NORMAL, gStringVar4, 0),
                                     row * 16, 0, 0, sOrchidTextColors, TEXT_SKIP_DRAW, gStringVar4);
        row++;
    }

    CopyWindowToVram(sSaveInfoWindowId, COPYWIN_GFX);
}

static void RemoveSaveInfoWindow(void)
{
    OrchidSaveBall_Destroy();
    ClearStdWindowAndFrame(sSaveInfoWindowId, FALSE);
    RemoveWindow(sSaveInfoWindowId);
}

static void Task_WaitForBattleTowerLinkSave(u8 taskId)
{
    if (!FuncIsActiveTask(Task_LinkFullSave))
    {
        DestroyTask(taskId);
        ScriptContext_Enable();
    }
}

#define tInBattleTower data[2]

void SaveForBattleTowerLink(void)
{
    u8 taskId = CreateTask(Task_LinkFullSave, 5);
    gTasks[taskId].tInBattleTower = TRUE;
    gTasks[CreateTask(Task_WaitForBattleTowerLinkSave, 6)].data[1] = taskId;
}

#undef tInBattleTower

static void HideStartMenuWindow(void)
{
    OrchidStartMenu_DestroyIcons();
    ScriptUnfreezeObjectEvents();
    UnlockPlayerFieldControls();
}

void HideStartMenu(void)
{
    PlaySE(SE_SELECT);
    HideStartMenuWindow();
}

void AppendToList(u8 *list, u8 *pos, u8 newEntry)
{
    list[*pos] = newEntry;
    (*pos)++;
}

static bool8 StartMenuDexNavCallback(void)
{
    RemoveExtraStartMenuWindows();
    CreateTask(Task_OpenDexNavFromStartMenu, 0);
    return TRUE;
}

void Script_ForceSaveGame(struct ScriptContext *ctx)
{
    SaveGame();
    ShowSaveInfoWindow();
    gMenuCallback = SaveCallback;
    sSaveDialogCallback = SaveSavingMessageCallback;
}
