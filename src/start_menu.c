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
#include "constants/rgb.h"
#include "constants/songs.h"

// Menu actions
enum
{
    MENU_ACTION_POKEDEX,
    MENU_ACTION_POKEMON,
    MENU_ACTION_BAG,
    MENU_ACTION_POKENAV,
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
#define TAG_OSM_ICON_PAL     0x6E21 // menu_icons.png palette (also the saving ball + sparkles)
#define TAG_OSM_ICON_MUTED   0x6E22 // resting icons
#define TAG_OSM_BALL         0x6E23
#define TAG_OSM_SPARKLES     0x6E24
#define TAG_OSM_SAFARI_ICON  0x6E25

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
    ICON_POKENAV,
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
EWRAM_DATA static bool8 sOrchidIconsShown = FALSE;
EWRAM_DATA static u8 sOrchidIconSpriteIds[ARRAY_COUNT(sCurrentStartMenuActions)] = {0};
EWRAM_DATA static bool8 sOrchidBallShown = FALSE;
EWRAM_DATA static u8 sOrchidBallSpriteId = 0;
EWRAM_DATA static u8 sOrchidSparkleSpriteIds[3] = {0};

// Menu action callbacks
static bool8 StartMenuPokedexCallback(void);
static bool8 StartMenuPokemonCallback(void);
static bool8 StartMenuBagCallback(void);
static bool8 StartMenuPokeNavCallback(void);
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

static const struct WindowTemplate sWindowTemplate_LocationChip = {
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = 10,
    .height = 2,
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
    [MENU_ACTION_POKENAV]         = {gText_MenuPokenav, {.u8_void = StartMenuPokeNavCallback}},
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
    [MENU_ACTION_POKENAV]         = ICON_POKENAV,
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
        AddStartMenuAction(MENU_ACTION_POKENAV);

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
        AddStartMenuAction(MENU_ACTION_POKENAV);
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
        AddStartMenuAction(MENU_ACTION_POKENAV);
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
        AddStartMenuAction(MENU_ACTION_POKENAV);
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

// ---------------------------------------------------------------- Orchid start menu
// Rows (mock_system.start_menu): white window in the player's FRAME, gold pill on the selected row, the
// PLAYER row in the gender name colour. Icons are OBJ: resting ones muted, the selected one lifted 1 px.
static void OrchidStartMenu_DrawRows(u8 selected)
{
    u8 windowId = GetStartMenuWindowId();
    u32 width = GetWindowAttribute(windowId, WINDOW_WIDTH) * 8;
    u32 i;

    FillWindowPixelBuffer(windowId, PIXEL_FILL(OSM_WHITE));
    OrchidDrawRoundedBox(windowId, 2, selected * 16 + 1, width - 4, 14, 4, ORCHID_PILL_FACE, OSM_INK, ORCHID_PILL_LIGHT, ORCHID_PILL_SHADE);
    for (i = 0; i < sNumStartMenuActions; i++)
    {
        const struct MenuAction *action = &sStartMenuItems[sCurrentStartMenuActions[i]];
        bool32 isName = (action->func.u8_void == StartMenuPlayerNameCallback
                      || action->func.u8_void == StartMenuLinkModePlayerNameCallback);

        StringExpandPlaceholders(gStringVar4, action->text);
        AddTextPrinterParameterized4(windowId, FONT_NORMAL, OSM_MENU_TEXT_X, i * 16, 0, 0,
                                     isName ? sOrchidNameColors : sOrchidTextColors, TEXT_SKIP_DRAW, gStringVar4);
    }
    CopyWindowToVram(windowId, COPYWIN_GFX);

    if (sOrchidIconsShown)
    {
        u8 normalPal = IndexOfSpritePaletteTag(TAG_OSM_ICON_PAL);
        u8 mutedPal = IndexOfSpritePaletteTag(TAG_OSM_ICON_MUTED);

        for (i = 0; i < sNumStartMenuActions; i++)
        {
            struct Sprite *sprite = &gSprites[sOrchidIconSpriteIds[i]];

            sprite->oam.paletteNum = (i == selected || mutedPal == 0xFF) ? normalPal : mutedPal;
            sprite->y = OSM_ICON_Y0 + i * 16 + 8 - (i == selected ? OSM_ICON_LIFT : 0);
        }
    }
}

static void OrchidStartMenu_CreateIcons(void)
{
    struct SpriteSheet sheet = {gOrchidStartMenuIcons_Gfx, ICON_COUNT * 4 * TILE_SIZE_4BPP, TAG_OSM_ICONS};
    struct SpritePalette pal = {gOrchidStartMenuIcons_Pal, TAG_OSM_ICON_PAL};
    struct SpritePalette muted = {gOrchidStartMenuIconsMuted_Pal, TAG_OSM_ICON_MUTED};
    u32 i;

    if (sOrchidIconsShown)
        return;
    LoadSpriteSheet(&sheet);
    if (LoadSpritePalette(&pal) == 0xFF)
    {
        FreeSpriteTilesByTag(TAG_OSM_ICONS);
        return; // no free OBJ palette: the menu still works, without icons
    }
    LoadSpritePalette(&muted);
    for (i = 0; i < sNumStartMenuActions; i++)
    {
        u8 spriteId = CreateSprite(&sSpriteTemplate_OrchidIcon, OSM_ICON_X + 8, OSM_ICON_Y0 + i * 16 + 8, 0);

        sOrchidIconSpriteIds[i] = spriteId;
        if (spriteId != MAX_SPRITES)
            StartSpriteAnim(&gSprites[spriteId], sOrchidStartMenuIcons[sCurrentStartMenuActions[i]]);
    }
    sOrchidIconsShown = TRUE;
}

static void OrchidStartMenu_DestroyIcons(void)
{
    u32 i;

    if (!sOrchidIconsShown)
        return;
    for (i = 0; i < sNumStartMenuActions; i++)
    {
        if (sOrchidIconSpriteIds[i] != MAX_SPRITES)
            DestroySprite(&gSprites[sOrchidIconSpriteIds[i]]);
    }
    FreeSpriteTilesByTag(TAG_OSM_ICONS);
    FreeSpritePaletteByTag(TAG_OSM_ICON_PAL);
    FreeSpritePaletteByTag(TAG_OSM_ICON_MUTED);
    sOrchidIconsShown = FALSE;
}

static u8 OrchidStartMenu_AddChipWindow(const struct WindowTemplate *template, u8 chip)
{
    sOrchidChip = chip;
    sOrchidChipWindowId = AddWindow(template);
    DrawStdWindowFrame(sOrchidChipWindowId, FALSE);
    return sOrchidChipWindowId;
}

// Location chip (mock_system.chip_location): a label pill with the map pin and the map name.
static void ShowLocationChip(void)
{
    u8 windowId = OrchidStartMenu_AddChipWindow(&sWindowTemplate_LocationChip, ORCHID_CHIP_LOCATION);

    BlitBitmapRectToWindow(windowId, gOrchidStartChips_Gfx, 0, OSM_CHIP_LOC_Y, OSM_CHIP_SHEET_W, 128, 0, 0, 80, 16);
    GetMapNameGeneric(gStringVar4, gMapHeader.regionMapSectionId);
    AddTextPrinterParameterized4(windowId, FONT_NORMAL, OSM_LOC_TEXT_X, 0, 0, 0, sOrchidTextColors, TEXT_SKIP_DRAW, gStringVar4);
    CopyWindowToVram(windowId, COPYWIN_GFX);
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
        CopyWindowToVram(windowId, COPYWIN_GFX);
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
    CopyWindowToVram(sSafariBallsWindowId, COPYWIN_GFX);
}

// Orchid Pyramid chip (mock_system.chip_pyramid): "Battle Pyramid", 7 floor pips (cleared gold, current
// accent, ahead recessed) and the floor name.
static void ShowPyramidFloorWindow(void)
{
    u32 floor = gSaveBlock2Ptr->frontier.curChallengeBattleNum;
    u32 k;
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
    AddTextPrinterParameterized4(windowId, FONT_NARROW, OSM_PYRAMID_FLOOR_X, OSM_PYRAMID_FLOOR_Y, 0, 0, sOrchidTextColors,
                                 TEXT_SKIP_DRAW, sPyramidFloorNames[floor]);
    CopyWindowToVram(windowId, COPYWIN_GFX);
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
    ClearStdWindowAndFrameToTransparent(sOrchidChipWindowId, FALSE);
    CopyWindowToVram(sOrchidChipWindowId, COPYWIN_GFX);
    RemoveWindow(sOrchidChipWindowId);
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
        DrawStdWindowFrame(AddStartMenuWindow(sNumStartMenuActions), FALSE);
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
                ShowLocationChip();
        }
        sInitStartMenuData[0]++;
        break;
    case 4:
        // Orchid: the rows are drawn by OrchidStartMenu_DrawRows (with the cursor)
        sInitStartMenuData[0]++;
        break;
    case 5:
        OrchidStartMenu_CreateIcons();
        sStartMenuCursorPos = InitOrchidCustomMenu(GetStartMenuWindowId(), sNumStartMenuActions, sStartMenuCursorPos, OrchidStartMenu_DrawRows);
        CopyWindowToVram(GetStartMenuWindowId(), COPYWIN_FULL);
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
    sOrchidBallShown = FALSE;
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
        sStartMenuCursorPos = Menu_MoveCursor(-1);
    }

    if (JOY_NEW(DPAD_DOWN))
    {
        PlaySE(SE_SELECT);
        sStartMenuCursorPos = Menu_MoveCursor(1);
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
        RemoveExtraStartMenuWindows();
        HideStartMenu();
        return TRUE;
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

static bool8 StartMenuPokeNavCallback(void)
{
    if (!gPaletteFade.active)
    {
        PlayRainStoppingSoundEffect();
        RemoveExtraStartMenuWindows();
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_InitPokeNav);  // Display PokéNav

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

static bool8 StartMenuExitCallback(void)
{
    RemoveExtraStartMenuWindows();
    HideStartMenu(); // Hide start menu

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
    ClearStdWindowAndFrame(GetStartMenuWindowId(), TRUE);
    RemoveStartMenuWindow();
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
    ClearStdWindowAndFrame(GetStartMenuWindowId(), FALSE);
    RemoveStartMenuWindow();
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
    ClearStdWindowAndFrame(GetStartMenuWindowId(), FALSE);
    RemoveStartMenuWindow();
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
    ClearStdWindowAndFrame(GetStartMenuWindowId(), TRUE);
    RemoveStartMenuWindow();
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
