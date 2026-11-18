#include "global.h"
#include "battle_main.h"
#include "bg.h"
#include "data.h"
#include "decompress.h"
#include "decoration.h"
#include "decoration_inventory.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "field_screen_effect.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "international_string_util.h"
#include "item.h"
#include "item_icon.h"
#include "item_menu.h"
#include "list_menu.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "menu_helpers.h"
#include "money.h"
#include "move.h"
#include "overworld.h"
#include "palette.h"
#include "party_menu.h"
#include "scanline_effect.h"
#include "script.h"
#include "shop.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "strings.h"
#include "text_window.h"
#include "tv.h"
#include "shop_criteria.h"
#include "constants/decorations.h"
#include "constants/event_objects.h"
#include "constants/items.h"
#include "constants/metatile_behaviors.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#include "data/shop_orchid.h"

#define TAG_ITEM_ICON_BASE 9110 // immune to time blending
#define TAG_ITEM_ICON_BONUS (TAG_ITEM_ICON_BASE + 2)
#define TAG_OSHOP_OBJ_PAL   2100 // thumb, chevrons, coin
#define TAG_OSHOP_THUMB     2101
#define TAG_OSHOP_CHEVRONS  2102
#define TAG_OSHOP_COIN      2103
#define TAG_OSHOP_TM_DISCS  2104 // tiles + palette

#define MAX_ITEMS_SHOWN OSHOP_LIST_ROWS

// Orchid kit palette roles (dev_scripts/orchid_ui/kit.py) used by the text on BG palette 0
#define OSHOP_INK         1
#define OSHOP_PANEL_SHADE 5
#define OSHOP_SPARE_B     15 // price-tag manila shade

// BG0 tiles (charblock 2): tile 0 blank + the Orchid message frame, then the YES/NO frame, then windows
#define OSHOP_MSG_FRAME_BASE   0
#define ORCHID_SHOP_YESNO_FRAME_TILE 0x10
#define OSHOP_WINDOW_PAL       15 // Orchid window palette (message box, YES/NO)

enum {
    WIN_BUY_SELL_QUIT,
    WIN_BUY_QUIT,
};

enum {
    WIN_MONEY,
    WIN_ITEM_LIST,
    WIN_ITEM_DESCRIPTION,
    WIN_QUANTITY, // BG1: the hanging quantity tag
    WIN_MESSAGE,
};

enum {
    COLORID_NORMAL, // ink with the panel shade (money, descriptions, quantity, money left)
    COLORID_PRICE,  // ink with the manila tag shade (prices in the list, quantity total)
};

enum {
    MART_TYPE_NORMAL,
    MART_TYPE_DECOR,
    MART_TYPE_DECOR2,
};

struct MartInfo
{
    void (*callback)(void);
    const struct MenuAction *menuActions;
    const u16 *itemList;
    u16 itemCount;
    u8 windowId;
    u8 martType;
};

struct ShopData
{
    u16 tilemapBuffers[4][0x400]; // BG0..BG3
    u32 totalCost;
    u16 itemsShowed;
    u16 selectedRow;
    u16 scrollOffset;
    u16 maxQuantity;
    u8 iconSlot;
    u8 itemSpriteIds[2];
    // Orchid
    u8 pillVariant;   // sOrchidShopPillRows entry for the item rows (price tag width)
    u8 gridTimer;
    u8 thumbSpriteId;
    u8 clerkSpriteId;
    u8 bonusSpriteId;
    u8 coinSpriteId;
    u8 chevronSpriteIds[2];
    u8 discSpriteIds[OSHOP_LIST_ROWS];
    TaskFunc messageNextTask;
};

static EWRAM_DATA struct MartInfo sMartInfo = {0};
static EWRAM_DATA struct ShopData *sShopData = NULL;
static EWRAM_DATA struct ListMenuItem *sListMenuItems = NULL;
static EWRAM_DATA u8 (*sItemNames)[ITEM_NAME_LENGTH + 2] = {0};
static EWRAM_DATA u8 sPurchaseHistoryId = 0;
EWRAM_DATA struct ItemSlot gMartPurchaseHistory[SMARTSHOPPER_NUM_ITEMS] = {0};

static void Task_ShopMenu(u8 taskId);
static void Task_HandleShopMenuQuit(u8 taskId);
static void CB2_InitBuyMenu(void);
static void Task_GoToBuyOrSellMenu(u8 taskId);
static void MapPostLoadHook_ReturnToShopMenu(void);
static void Task_ReturnToShopMenu(u8 taskId);
static void ShowShopMenuAfterExitingBuyOrSellMenu(u8 taskId);
static void BuyMenuDrawGraphics(void);
static void Task_BuyMenu(u8 taskId);
static void BuyMenuBuildListMenuTemplate(void);
static void BuyMenuInitBgs(void);
static void BuyMenuInitWindows(void);
static void BuyMenuDecompressBgGraphics(void);
static void BuyMenuSetListEntry(struct ListMenuItem *, enum Item, u8 *);
static void BuyMenuAddItemIcon(enum Item, u8);
static void BuyMenuRemoveItemIcon(enum Item, u8);
static void BuyMenuPrint(u8 windowId, const u8 *text, u8 x, u8 y, s8 speed, u8 colorSet);
static void ExitBuyMenu(u8 taskId);
static void Task_ExitBuyMenu(u8 taskId);
static void BuyMenuTryMakePurchase(u8 taskId);
static void BuyMenuReturnToItemList(u8 taskId);
static void Task_BuyHowManyDialogueInit(u8 taskId);
static void BuyMenuConfirmPurchase(u8 taskId);
static void BuyMenuPrintItemQuantityAndPrice(u8 taskId);
static void Task_BuyHowManyDialogueHandleInput(u8 taskId);
static void BuyMenuSubtractMoney(u8 taskId);
static void RecordItemPurchase(u8 taskId);
static void Task_ReturnToItemListAfterItemPurchase(u8 taskId);
static void Task_ReturnToItemListAfterDecorationPurchase(u8 taskId);
static void Task_HandleShopMenuBuy(u8 taskId);
static void Task_HandleShopMenuSell(u8 taskId);
static void BuyMenuPrintItemDescriptionAndShowItemIcon(s32 item, bool8 onInit, struct ListMenu *list);
static void BuyMenuPrintPriceInList(u8 windowId, u32 itemId, u8 y);
static void OrchidShop_CreateSprites(void);
static void OrchidShop_DrawRows(u16 scroll, u16 selectedRow);
static void OrchidShop_PrintMoney(void);
static void OrchidShop_ShowQuantityTag(bool32 show);
static void OrchidShop_ShowBonusBall(bool32 show);

static const struct YesNoFuncTable sShopPurchaseYesNoFuncs =
{
    BuyMenuTryMakePurchase,
    BuyMenuReturnToItemList
};

static const struct MenuAction sShopMenuActions_BuySellQuit[] =
{
    { gText_ShopBuy, {.void_u8=Task_HandleShopMenuBuy} },
    { gText_ShopSell, {.void_u8=Task_HandleShopMenuSell} },
    { gText_ShopQuit, {.void_u8=Task_HandleShopMenuQuit} }
};

static const struct MenuAction sShopMenuActions_BuyQuit[] =
{
    { gText_ShopBuy, {.void_u8=Task_HandleShopMenuBuy} },
    { gText_ShopQuit, {.void_u8=Task_HandleShopMenuQuit} }
};

// Orchid (mock_mart.render_menu): BUY / SELL / QUIT in the Orchid frame at tile (2, 1), 6 tiles wide, gold pill
// rows like the YES/NO. Frame + window palette in the field's free slots (ORCHID_YESNO_FIELD_TILE / _PAL).
static const struct WindowTemplate sShopMenuWindowTemplates[] =
{
    [WIN_BUY_SELL_QUIT] = {
        .bg = 0,
        .tilemapLeft = 2,
        .tilemapTop = 1,
        .width = 6,
        .height = 6,
        .paletteNum = ORCHID_YESNO_FIELD_PAL,
        .baseBlock = 0x0008,
    },
    // Separate shop menu window for decorations, which can't be sold
    [WIN_BUY_QUIT] = {
        .bg = 0,
        .tilemapLeft = 2,
        .tilemapTop = 1,
        .width = 6,
        .height = 4,
        .paletteNum = ORCHID_YESNO_FIELD_PAL,
        .baseBlock = 0x0008,
    }
};

// The gold pill rows on BG2 are the cursor (OrchidShop_DrawRows), so no ▶.
static const struct ListMenuTemplate sShopBuyMenuListTemplate =
{
    .items = NULL,
    .moveCursorFunc = BuyMenuPrintItemDescriptionAndShowItemIcon,
    .itemPrintFunc = BuyMenuPrintPriceInList,
    .totalItems = 0,
    .maxShowed = 0,
    .windowId = WIN_ITEM_LIST,
    .header_X = 0,
    .item_X = OSHOP_NAME_X,
    .cursor_X = 0,
    .upText_Y = 0,
    .cursorPal = OSHOP_INK,
    .fillValue = 0,
    .cursorShadowPal = OSHOP_PANEL_SHADE,
    .lettersSpacing = 0,
    .itemVerticalPadding = 0,
    .scrollMultiple = LIST_NO_MULTIPLE_SCROLL,
    .fontId = FONT_NARROW,
    .cursorKind = CURSOR_INVISIBLE,
    .textNarrowWidth = 84, // set from the price tag width in BuyMenuBuildListMenuTemplate
};

// Orchid (export_mart.py): BG0 text, BG1 quantity tag (in front), BG2 shop art, BG3 scrolling grid.
static const struct BgTemplate sShopBuyMenuBgTemplates[] =
{
    {
        .bg = 0,
        .charBaseIndex = 2,
        .mapBaseIndex = 31,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 1,
        .baseTile = 0
    },
    {
        .bg = 1,
        .charBaseIndex = 2,
        .mapBaseIndex = 30,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 0,
        .baseTile = 0
    },
    {
        .bg = 2,
        .charBaseIndex = 0,
        .mapBaseIndex = 29,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 2,
        .baseTile = 0
    },
    {
        .bg = 3,
        .charBaseIndex = 0,
        .mapBaseIndex = 28,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 3,
        .baseTile = 0
    }
};

// BG0 and BG1 share charblock 2 (tiles may run on into charblock 3 below the maps at screenblock 28).
static const struct WindowTemplate sShopBuyMenuWindowTemplates[] =
{
    [WIN_MONEY] = { // the cream pill on the hanging money sign
        .bg = 0,
        .tilemapLeft = 3,
        .tilemapTop = 2,
        .width = 8,
        .height = 3,
        .paletteNum = OSHOP_PAL_KIT,
        .baseBlock = 0x0020,
    },
    [WIN_ITEM_LIST] = {
        .bg = 0,
        .tilemapLeft = OSHOP_PILL_COL,
        .tilemapTop = OSHOP_LIST_ROW_TILE,
        .width = OSHOP_PILL_COLS,
        .height = 2 * OSHOP_LIST_ROWS,
        .paletteNum = OSHOP_PAL_KIT,
        .baseBlock = 0x0038,
    },
    [WIN_ITEM_DESCRIPTION] = { // the card pinned on the counter front
        .bg = 0,
        .tilemapLeft = 1,
        .tilemapTop = 14,
        .width = 28,
        .height = 6,
        .paletteNum = OSHOP_PAL_KIT,
        .baseBlock = 0x00F8,
    },
    [WIN_QUANTITY] = {
        .bg = 1,
        .tilemapLeft = OSHOP_QTY_WIN_X,
        .tilemapTop = OSHOP_QTY_WIN_Y,
        .width = OSHOP_QTY_WIN_W,
        .height = OSHOP_QTY_WIN_H,
        .paletteNum = OSHOP_PAL_KIT,
        .baseBlock = 0x01A0,
    },
    [WIN_MESSAGE] = {
        .bg = 0,
        .tilemapLeft = OSHOP_MSG_WIN_X,
        .tilemapTop = OSHOP_MSG_WIN_Y,
        .width = OSHOP_MSG_WIN_W,
        .height = OSHOP_MSG_WIN_H,
        .paletteNum = OSHOP_WINDOW_PAL,
        .baseBlock = 0x01FA,
    },
    DUMMY_WIN_TEMPLATE
};

// mock_mart.yesno: std frame at tile (24, 9), 5x4
static const struct WindowTemplate sShopBuyMenuYesNoWindowTemplates =
{
    .bg = 0,
    .tilemapLeft = 24,
    .tilemapTop = 9,
    .width = 5,
    .height = 4,
    .paletteNum = OSHOP_WINDOW_PAL,
    .baseBlock = 0x0262,
};

static const u8 sShopBuyMenuTextColors[][3] =
{
    [COLORID_NORMAL] = {TEXT_COLOR_TRANSPARENT, OSHOP_INK, OSHOP_PANEL_SHADE},
    [COLORID_PRICE]  = {TEXT_COLOR_TRANSPARENT, OSHOP_INK, OSHOP_SPARE_B},
};

// Orchid OBJ: scroll thumb, quantity chevrons + coin (one palette), TM discs (palette built per list page)
static const struct OamData sOamData_OrchidShop8x16 = {.shape = SPRITE_SHAPE(8x16), .size = SPRITE_SIZE(8x16), .priority = 2};
static const struct OamData sOamData_OrchidShop16x8 = {.shape = SPRITE_SHAPE(16x8), .size = SPRITE_SIZE(16x8), .priority = 0};
static const struct OamData sOamData_OrchidShop16x16 = {.shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 0};
static const struct OamData sOamData_OrchidShopDisc = {.shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 1};

static const union AnimCmd sAnim_OrchidShop_Frame0[] = {ANIMCMD_FRAME(0, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidShop_Frame1[] = {ANIMCMD_FRAME(2, 0), ANIMCMD_END};
static const union AnimCmd *const sAnims_OrchidShopChevrons[] = {sAnim_OrchidShop_Frame0, sAnim_OrchidShop_Frame1};
static const union AnimCmd sAnim_OrchidShopDisc0[] = {ANIMCMD_FRAME(0, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidShopDisc1[] = {ANIMCMD_FRAME(4, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidShopDisc2[] = {ANIMCMD_FRAME(8, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidShopDisc3[] = {ANIMCMD_FRAME(12, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidShopDisc4[] = {ANIMCMD_FRAME(16, 0), ANIMCMD_END};
static const union AnimCmd sAnim_OrchidShopDisc5[] = {ANIMCMD_FRAME(20, 0), ANIMCMD_END};
static const union AnimCmd *const sAnims_OrchidShopDiscs[OSHOP_LIST_ROWS] =
{
    sAnim_OrchidShopDisc0, sAnim_OrchidShopDisc1, sAnim_OrchidShopDisc2,
    sAnim_OrchidShopDisc3, sAnim_OrchidShopDisc4, sAnim_OrchidShopDisc5,
};

static const struct SpriteSheet sOrchidShopSpriteSheets[] =
{
    {gOrchidShopThumb_Gfx, 2 * TILE_SIZE_4BPP, TAG_OSHOP_THUMB},
    {gOrchidShopChevrons_Gfx, 4 * TILE_SIZE_4BPP, TAG_OSHOP_CHEVRONS},
    {gOrchidShopCoin_Gfx, 4 * TILE_SIZE_4BPP, TAG_OSHOP_COIN},
    {gOrchidShopTmDiscs_Gfx, 4 * OSHOP_LIST_ROWS * TILE_SIZE_4BPP, TAG_OSHOP_TM_DISCS},
    {0}
};

static const struct SpritePalette sOrchidShopObjPalette = {gOrchidShopObj_Pal, TAG_OSHOP_OBJ_PAL};

static const struct SpriteTemplate sSpriteTemplate_OrchidShopThumb =
{
    .tileTag = TAG_OSHOP_THUMB,
    .paletteTag = TAG_OSHOP_OBJ_PAL,
    .oam = &sOamData_OrchidShop8x16,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_OrchidShopChevron =
{
    .tileTag = TAG_OSHOP_CHEVRONS,
    .paletteTag = TAG_OSHOP_OBJ_PAL,
    .oam = &sOamData_OrchidShop16x8,
    .anims = sAnims_OrchidShopChevrons,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_OrchidShopCoin =
{
    .tileTag = TAG_OSHOP_COIN,
    .paletteTag = TAG_OSHOP_OBJ_PAL,
    .oam = &sOamData_OrchidShop16x16,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_OrchidShopDisc =
{
    .tileTag = TAG_OSHOP_TM_DISCS,
    .paletteTag = TAG_OSHOP_TM_DISCS,
    .oam = &sOamData_OrchidShopDisc,
    .anims = sAnims_OrchidShopDiscs,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const enum Item sShopItemsListDummy[] = { ITEM_NONE };

static u8 CreateShopMenu(u8 martType)
{
    int numMenuItems;

    LockPlayerFieldControls();
    sMartInfo.martType = martType;

    if (martType == MART_TYPE_NORMAL)
    {
        sMartInfo.windowId = AddWindow(&sShopMenuWindowTemplates[WIN_BUY_SELL_QUIT]);
        sMartInfo.menuActions = sShopMenuActions_BuySellQuit;
        numMenuItems = ARRAY_COUNT(sShopMenuActions_BuySellQuit);
    }
    else
    {
        sMartInfo.windowId = AddWindow(&sShopMenuWindowTemplates[WIN_BUY_QUIT]);
        sMartInfo.menuActions = sShopMenuActions_BuyQuit;
        numMenuItems = ARRAY_COUNT(sShopMenuActions_BuyQuit);
    }

    LoadOrchidYesNoFrame(0, ORCHID_YESNO_FIELD_TILE);
    LoadOrchidYesNoColors(ORCHID_YESNO_FIELD_PAL, TRUE);
    DrawStdFrameWithCustomTileAndPalette(sMartInfo.windowId, FALSE, ORCHID_YESNO_FIELD_TILE, ORCHID_YESNO_FIELD_PAL);
    InitOrchidPillMenuYesNoStyle(sMartInfo.windowId, numMenuItems, sMartInfo.menuActions, 0);
    PutWindowTilemap(sMartInfo.windowId);
    CopyWindowToVram(sMartInfo.windowId, COPYWIN_FULL);

    return CreateTask(Task_ShopMenu, 8);
}

static void SetShopMenuCallback(void (*callback)(void))
{
    sMartInfo.callback = callback;
}

static void SetShopItemsForSale(const u16 *items)
{
    u16 i = 0;

    sMartInfo.itemList = items;
    sMartInfo.itemCount = 0;

    assertf(items != NULL, "Shop items list should never be set as NULL")
    {
        sMartInfo.itemList = sShopItemsListDummy;
        return;
    }

    // Read items until ITEM_NONE / DECOR_NONE is reached
    while (sMartInfo.itemList[i])
    {
        sMartInfo.itemCount++;
        i++;
    }
}

static void Task_ShopMenu(u8 taskId)
{
    s8 inputCode = Menu_ProcessInputNoWrap();
    switch (inputCode)
    {
    case MENU_NOTHING_CHOSEN:
        break;
    case MENU_B_PRESSED:
        PlaySE(SE_SELECT);
        Task_HandleShopMenuQuit(taskId);
        break;
    default:
        sMartInfo.menuActions[inputCode].func.void_u8(taskId);
        break;
    }
}

#define tItemCount  data[1]
#define tItemId     data[5]
#define tListTaskId data[7]
#define tCallbackHi data[8]
#define tCallbackLo data[9]

static void Task_HandleShopMenuBuy(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    tCallbackHi = (u32)CB2_InitBuyMenu >> 16;
    tCallbackLo = (u32)CB2_InitBuyMenu;
    gTasks[taskId].func = Task_GoToBuyOrSellMenu;
    FadeScreen(FADE_TO_BLACK, 0);
}

static void Task_HandleShopMenuSell(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    tCallbackHi = (u32)CB2_GoToSellMenu >> 16;
    tCallbackLo = (u32)CB2_GoToSellMenu;
    gTasks[taskId].func = Task_GoToBuyOrSellMenu;
    FadeScreen(FADE_TO_BLACK, 0);
}

void CB2_ExitSellMenu(void)
{
    gFieldCallback = MapPostLoadHook_ReturnToShopMenu;
    SetMainCallback2(CB2_ReturnToField);
}

static void Task_HandleShopMenuQuit(u8 taskId)
{
    ClearStdWindowAndFrameToTransparent(sMartInfo.windowId, 2); // Incorrect use, making it not copy it to vram.
    RemoveWindow(sMartInfo.windowId);
    TryPutSmartShopperOnAir();
    UnlockPlayerFieldControls();
    DestroyTask(taskId);

    if (sMartInfo.callback)
        sMartInfo.callback();
}

static void Task_GoToBuyOrSellMenu(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    if (!gPaletteFade.active)
    {
        DestroyTask(taskId);
        SetMainCallback2((MainCallback)((u16)tCallbackHi << 16 | (u16)tCallbackLo));
    }
}

static void MapPostLoadHook_ReturnToShopMenu(void)
{
    FadeInFromBlack();
    CreateTask(Task_ReturnToShopMenu, 8);
}

static void Task_ReturnToShopMenu(u8 taskId)
{
    if (IsWeatherNotFadingIn() == TRUE)
    {
        if (sMartInfo.martType == MART_TYPE_DECOR2)
            DisplayItemMessageOnField(taskId, gText_CanIHelpWithAnythingElse, ShowShopMenuAfterExitingBuyOrSellMenu);
        else
            DisplayItemMessageOnField(taskId, gText_AnythingElseICanHelp, ShowShopMenuAfterExitingBuyOrSellMenu);
    }
}

static void ShowShopMenuAfterExitingBuyOrSellMenu(u8 taskId)
{
    CreateShopMenu(sMartInfo.martType);
    DestroyTask(taskId);
}

static void CB2_BuyMenu(void)
{
    // Orchid grid backdrop (BG3) scrolls diagonally down-right, 1px every 4 frames (as the bag)
    if ((++sShopData->gridTimer & 3) == 0)
    {
        ChangeBgX(3, 1 << 8, BG_COORD_SUB);
        ChangeBgY(3, 1 << 8, BG_COORD_SUB);
    }
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void VBlankCB_BuyMenu(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_InitBuyMenu(void)
{
    u8 taskId;

    switch (gMain.state)
    {
    case 0:
        SetVBlankHBlankCallbacksToNull();
        CpuFastFill(0, (void *)OAM, OAM_SIZE);
        ScanlineEffect_Stop();
        ResetTempTileDataBuffers();
        FreeAllSpritePalettes();
        ResetPaletteFade();
        ResetSpriteData();
        ResetTasks();
        ClearScheduledBgCopiesToVram();
        DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
        sShopData = AllocZeroed(sizeof(struct ShopData));
        sShopData->itemSpriteIds[0] = SPRITE_NONE;
        sShopData->itemSpriteIds[1] = SPRITE_NONE;
        sShopData->thumbSpriteId = SPRITE_NONE;
        sShopData->clerkSpriteId = SPRITE_NONE;
        sShopData->bonusSpriteId = SPRITE_NONE;
        if (sMartInfo.martType == MART_TYPE_NORMAL)
            TryBuildDynamicShopItemList(&sMartInfo.itemList, &sMartInfo.itemCount);
        BuyMenuBuildListMenuTemplate();
        BuyMenuInitBgs();
        FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, 0x20, 0x20);
        FillBgTilemapBufferRect_Palette0(1, 0, 0, 0, 0x20, 0x20);
        FillBgTilemapBufferRect_Palette0(2, 0, 0, 0, 0x20, 0x20);
        FillBgTilemapBufferRect_Palette0(3, 0, 0, 0, 0x20, 0x20);
        BuyMenuInitWindows();
        BuyMenuDecompressBgGraphics();
        gMain.state++;
        break;
    case 1:
        if (!FreeTempTileDataBuffersIfPossible())
            gMain.state++;
        break;
    default:
        OrchidShop_CreateSprites();
        BuyMenuDrawGraphics();
        taskId = CreateTask(Task_BuyMenu, 8);
        gTasks[taskId].tListTaskId = ListMenuInit(&gMultiuseListMenuTemplate, 0, 0);
        BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB_BuyMenu);
        SetMainCallback2(CB2_BuyMenu);
        break;
    }
}

static void BuyMenuFreeMemory(void)
{
    if (sMartInfo.martType == MART_TYPE_NORMAL)
        TryFreeDynamicShopItemList(&sMartInfo.itemList);

    Free(sShopData);
    Free(sListMenuItems);
    Free(sItemNames);
    FreeAllWindowBuffers();
}

static bool32 OrchidShop_IsTM(u32 itemId)
{
    return sMartInfo.martType == MART_TYPE_NORMAL && itemId != LIST_CANCEL && GetItemPocket(itemId) == POCKET_TM_HM;
}

// The text in an item row's price tag: the price, or SOLD OUT (as vanilla).
static void OrchidShop_GetPriceString(u32 itemId, u8 *dst)
{
    if (sMartInfo.martType == MART_TYPE_NORMAL)
        ConvertIntToDecimalStringN(gStringVar1, GetItemPrice(itemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT), STR_CONV_MODE_LEFT_ALIGN, 6);
    else
        ConvertIntToDecimalStringN(gStringVar1, gDecorations[itemId].price, STR_CONV_MODE_LEFT_ALIGN, 6);

    if (GetItemImportance(itemId) && (CheckBagHasItem(itemId, 1) || CheckPCHasItem(itemId, 1)))
        StringCopy(dst, gText_SoldOut);
    else
        StringExpandPlaceholders(dst, gText_PokedollarVar1);
}

static void BuyMenuBuildListMenuTemplate(void)
{
    u16 i;
    u32 width, tagWidth = 0;
    bool32 hasTM = FALSE;
    u8 price[16];

    sListMenuItems = Alloc((sMartInfo.itemCount + 1) * sizeof(*sListMenuItems));
    sItemNames = Alloc((sMartInfo.itemCount + 1) * sizeof(*sItemNames));
    for (i = 0; i < sMartInfo.itemCount; i++)
        BuyMenuSetListEntry(&sListMenuItems[i], sMartInfo.itemList[i], sItemNames[i]);

    StringCopy(sItemNames[i], gText_Cancel2);
    sListMenuItems[i].name = sItemNames[i];
    sListMenuItems[i].id = LIST_CANCEL;

    gMultiuseListMenuTemplate = sShopBuyMenuListTemplate;
    gMultiuseListMenuTemplate.items = sListMenuItems;
    gMultiuseListMenuTemplate.totalItems = sMartInfo.itemCount + 1;

    // Price tags: one width for the whole list, widest price + 18 px (mock_mart.a_tag_w)
    for (i = 0; i < sMartInfo.itemCount; i++)
    {
        OrchidShop_GetPriceString(sMartInfo.itemList[i], price);
        width = GetStringWidth(FONT_NARROW, price, 0) + OSHOP_TAG_PAD;
        if (width > tagWidth)
            tagWidth = width;
        if (OrchidShop_IsTM(sMartInfo.itemList[i]))
            hasTM = TRUE;
    }
    if (tagWidth < OSHOP_TAG_W_MIN)
        tagWidth = OSHOP_TAG_W_MIN;
    if (tagWidth > OSHOP_TAG_W_MAX)
        tagWidth = OSHOP_TAG_W_MAX;
    sShopData->pillVariant = 1 + tagWidth - OSHOP_TAG_W_MIN;
    // names squeeze to a narrower font rather than run into the tag
    gMultiuseListMenuTemplate.textNarrowWidth = (OSHOP_PILL_COLS * 8 - 2 - tagWidth) - OSHOP_NAME_X - 2;
    if (hasTM)
        gMultiuseListMenuTemplate.textNarrowWidth -= OSHOP_NAME_X_TM - OSHOP_NAME_X;
    if (gMultiuseListMenuTemplate.totalItems > MAX_ITEMS_SHOWN)
        gMultiuseListMenuTemplate.maxShowed = MAX_ITEMS_SHOWN;
    else
        gMultiuseListMenuTemplate.maxShowed = gMultiuseListMenuTemplate.totalItems;

    sShopData->itemsShowed = gMultiuseListMenuTemplate.maxShowed;
}

static void BuyMenuSetListEntry(struct ListMenuItem *menuItem, enum Item item, u8 *name)
{
    if (OrchidShop_IsTM(item))
    {
        // TM rows: the move name after the type disc (OBJ), mock_mart state_06
        name[0] = EXT_CTRL_CODE_BEGIN;
        name[1] = EXT_CTRL_CODE_SHIFT_RIGHT;
        name[2] = OSHOP_NAME_X_TM - OSHOP_NAME_X;
        StringCopy(&name[3], GetMoveName(ItemIdToBattleMoveId(item)));
    }
    else if (sMartInfo.martType == MART_TYPE_NORMAL)
        CopyItemName(item, name);
    else
        StringCopy(name, gDecorations[item].name);

    menuItem->name = name;
    menuItem->id = item;
}

static void BuyMenuPrintItemDescriptionAndShowItemIcon(s32 item, bool8 onInit, struct ListMenu *list)
{
    const u8 *description;
    if (onInit != TRUE)
        PlaySE(SE_SELECT);

    // the selected item sits on the counter (none for CANCEL, mock_mart)
    if (item != LIST_CANCEL)
        BuyMenuAddItemIcon(item, sShopData->iconSlot);

    BuyMenuRemoveItemIcon(item, sShopData->iconSlot ^ 1);
    sShopData->iconSlot ^= 1;
    if (item != LIST_CANCEL)
    {
        if (sMartInfo.martType == MART_TYPE_NORMAL)
            description = GetItemDescription(item);
        else
            description = gDecorations[item].description;
    }
    else
    {
        description = gText_QuitShopping;
    }

    // 3 lines at a 14 px pitch on the card (FONT_NORMAL is 16: the u8 line advance wraps, as in the bag)
    FillWindowPixelBuffer(WIN_ITEM_DESCRIPTION, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_ITEM_DESCRIPTION, FONT_NORMAL, OSHOP_DESC_X - 8, OSHOP_DESC_Y - 112, 0, (u8)-2,
                                 sShopBuyMenuTextColors[COLORID_NORMAL], 0, description);

    OrchidShop_DrawRows(list->scrollOffset, list->selectedRow);
}

static void BuyMenuPrintPriceInList(u8 windowId, u32 itemId, u8 y)
{
    u8 x;

    if (itemId != LIST_CANCEL)
    {
        OrchidShop_GetPriceString(itemId, gStringVar4);
        x = GetStringRightAlignXOffset(FONT_NARROW, gStringVar4, OSHOP_PRICE_RIGHT);
        AddTextPrinterParameterized4(windowId, FONT_NARROW, x, y, 0, 0, sShopBuyMenuTextColors[COLORID_PRICE], TEXT_SKIP_DRAW, gStringVar4);
    }
}

// ---------------------------------------------------------------- Orchid screen pieces
// Pill rows on BG2 (gold = the cursor), the TM type discs and the scroll thumb for the visible page.
static void OrchidShop_DrawRows(u16 scroll, u16 selectedRow)
{
    u16 *map = sShopData->tilemapBuffers[2];
    u16 discPal[16];
    u32 r, k, c, index, variant, palBits, total = sMartInfo.itemCount + 1;
    bool32 anyDisc = FALSE;

    CpuCopy16(sOrchidShopTmDiscNeutrals, discPal, sizeof(sOrchidShopTmDiscNeutrals));
    for (r = 0; r < OSHOP_LIST_ROWS; r++)
    {
        index = scroll + r;
        palBits = ((r == selectedRow) ? OSHOP_PAL_SELECTED : OSHOP_PAL_KIT) << 12;
        variant = (index == sMartInfo.itemCount) ? 0 : sShopData->pillVariant; // CANCEL: plain pill
        for (k = 0; k < 2; k++)
        {
            u16 *dst = &map[(OSHOP_LIST_ROW_TILE + 2 * r + k) * 32 + OSHOP_PILL_COL];
            for (c = 0; c < OSHOP_PILL_COLS; c++)
            {
                u16 e = sOrchidShopPillRows[variant][k][c];
                dst[c] = (index < total && e != 0) ? (e | palBits) : 0;
            }
        }

        if (sShopData->discSpriteIds[r] != SPRITE_NONE)
        {
            struct Sprite *disc = &gSprites[sShopData->discSpriteIds[r]];
            if (index < sMartInfo.itemCount && OrchidShop_IsTM(sMartInfo.itemList[index]))
            {
                const u16 *typePal = gTypesInfo[GetMoveType(GetItemTMHMMoveId(sMartInfo.itemList[index]))].paletteTMHM;
                discPal[4 + 2 * r] = typePal[6];
                discPal[5 + 2 * r] = typePal[9];
                disc->invisible = FALSE;
                anyDisc = TRUE;
            }
            else
            {
                disc->invisible = TRUE;
            }
        }
    }
    if (anyDisc)
        LoadPalette(discPal, OBJ_PLTT_ID(IndexOfSpritePaletteTag(TAG_OSHOP_TM_DISCS)), PLTT_SIZE_4BPP);
    ScheduleBgCopyTilemapToVram(2);

    if (sShopData->thumbSpriteId != SPRITE_NONE)
        gSprites[sShopData->thumbSpriteId].y = OSHOP_TRACK_Y0 + 2 + OSHOP_THUMB_SPAN * scroll / (total - OSHOP_LIST_ROWS) + 8;
}

static u16 OrchidShop_GetClerkGraphicsId(void)
{
    u8 objectEventId = GetObjectEventIdByLocalIdAndMap(gSpecialVar_LastTalked, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);

    if (objectEventId < OBJECT_EVENTS_COUNT && gObjectEvents[objectEventId].active
     && !(gObjectEvents[objectEventId].graphicsId & OBJ_EVENT_MON))
        return gObjectEvents[objectEventId].graphicsId;
    return OBJ_EVENT_GFX_MART_EMPLOYEE;
}

static void OrchidShop_CreateSprites(void)
{
    u32 i;
    u16 graphicsId;
    const struct ObjectEventGraphicsInfo *graphicsInfo;
    u8 spriteId;

    LoadSpriteSheets(sOrchidShopSpriteSheets);
    LoadSpritePalette(&sOrchidShopObjPalette);

    // clerk behind the counter (OBJ priority 3: under the BG2 counter, over the BG3 grid), facing the player
    graphicsId = OrchidShop_GetClerkGraphicsId();
    graphicsInfo = GetObjectEventGraphicsInfo(graphicsId);
    spriteId = CreateObjectGraphicsSprite(graphicsId, SpriteCallbackDummy, OSHOP_CLERK_X + 8, OSHOP_CLERK_BOTTOM - graphicsInfo->height / 2, 2);
    if (spriteId != MAX_SPRITES)
    {
        sShopData->clerkSpriteId = spriteId;
        gSprites[spriteId].oam.priority = 3;
        StartSpriteAnim(&gSprites[spriteId], ANIM_STD_FACE_SOUTH);
    }

    // scroll thumb on the track (only when the list scrolls)
    if (sMartInfo.itemCount + 1 > MAX_ITEMS_SHOWN)
    {
        spriteId = CreateSprite(&sSpriteTemplate_OrchidShopThumb, OSHOP_THUMB_X + 4, OSHOP_TRACK_Y0 + 2 + 8, 0);
        if (spriteId != MAX_SPRITES)
            sShopData->thumbSpriteId = spriteId;
    }

    // quantity tag: chevrons + coin (hidden until the tag drops in)
    for (i = 0; i < 2; i++)
    {
        spriteId = CreateSprite(&sSpriteTemplate_OrchidShopChevron, OSHOP_CHEV_X + 8, (i == 0 ? OSHOP_CHEV_UP_Y : OSHOP_CHEV_DOWN_Y) + 4, 0);
        sShopData->chevronSpriteIds[i] = spriteId;
        if (spriteId != MAX_SPRITES)
        {
            StartSpriteAnim(&gSprites[spriteId], i);
            gSprites[spriteId].invisible = TRUE;
        }
    }
    spriteId = CreateSprite(&sSpriteTemplate_OrchidShopCoin, OSHOP_COIN_X + 8, OSHOP_COIN_Y + 8, 0);
    sShopData->coinSpriteId = spriteId;
    if (spriteId != MAX_SPRITES)
        gSprites[spriteId].invisible = TRUE;

    // TM type discs, one per list row; palette rebuilt per page in OrchidShop_DrawRows
    for (i = 0; i < OSHOP_LIST_ROWS; i++)
        sShopData->discSpriteIds[i] = SPRITE_NONE;
    if (sMartInfo.martType == MART_TYPE_NORMAL)
    {
        bool32 hasTM = FALSE;
        for (i = 0; i < sMartInfo.itemCount; i++)
        {
            if (OrchidShop_IsTM(sMartInfo.itemList[i]))
                hasTM = TRUE;
        }
        if (hasTM)
        {
            struct SpritePalette discPal = {sOrchidShopTmDiscNeutrals, TAG_OSHOP_TM_DISCS};
            LoadSpritePalette(&discPal);
            for (i = 0; i < OSHOP_LIST_ROWS; i++)
            {
                spriteId = CreateSprite(&sSpriteTemplate_OrchidShopDisc, OSHOP_TM_DISC_X + 8, OSHOP_LIST_Y + 16 * i + 2 + 8, 0);
                if (spriteId != MAX_SPRITES)
                {
                    sShopData->discSpriteIds[i] = spriteId;
                    StartSpriteAnim(&gSprites[spriteId], i);
                    gSprites[spriteId].invisible = TRUE;
                }
            }
        }
    }
}

static void OrchidShop_PrintMoney(void)
{
    u8 str[16];

    ConvertIntToDecimalStringN(gStringVar1, GetMoney(&gSaveBlock1Ptr->money), STR_CONV_MODE_LEFT_ALIGN, MAX_MONEY_DIGITS);
    StringExpandPlaceholders(str, gText_PokedollarVar1);
    FillWindowPixelBuffer(WIN_MONEY, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_MONEY, FONT_NORMAL, GetStringRightAlignXOffset(FONT_NORMAL, str, OSHOP_MONEY_RIGHT - 24),
                                 OSHOP_MONEY_Y - 16, 0, 0, sShopBuyMenuTextColors[COLORID_NORMAL], TEXT_SKIP_DRAW, str);
    CopyWindowToVram(WIN_MONEY, COPYWIN_GFX);
}

static void OrchidShop_ShowQuantityTag(bool32 show)
{
    u32 i;

    if (show)
        PutWindowTilemap(WIN_QUANTITY);
    else
        ClearWindowTilemap(WIN_QUANTITY);
    ScheduleBgCopyTilemapToVram(1);
    for (i = 0; i < 2; i++)
    {
        if (sShopData->chevronSpriteIds[i] != MAX_SPRITES)
            gSprites[sShopData->chevronSpriteIds[i]].invisible = !show;
    }
    if (sShopData->coinSpriteId != MAX_SPRITES)
        gSprites[sShopData->coinSpriteId].invisible = !show;
}

// The bonus Premier Ball pops onto the counter beside the bought balls (mock_mart state_04).
static void OrchidShop_ShowBonusBall(bool32 show)
{
    u8 spriteId;

    if (sShopData->bonusSpriteId != SPRITE_NONE)
    {
        FreeSpriteTilesByTag(TAG_ITEM_ICON_BONUS);
        FreeSpritePaletteByTag(TAG_ITEM_ICON_BONUS);
        DestroySprite(&gSprites[sShopData->bonusSpriteId]);
        sShopData->bonusSpriteId = SPRITE_NONE;
    }
    if (show)
    {
        spriteId = AddItemIconSprite(TAG_ITEM_ICON_BONUS, TAG_ITEM_ICON_BONUS, ITEM_PREMIER_BALL);
        if (spriteId != MAX_SPRITES)
        {
            sShopData->bonusSpriteId = spriteId;
            gSprites[spriteId].x2 = OSHOP_ICON_X + OSHOP_BONUS_DX + (32 - 24) / 2;
            gSprites[spriteId].y2 = OSHOP_ICON_Y + OSHOP_BONUS_DY + (32 - 24) / 2;
            gSprites[spriteId].oam.priority = 2;
        }
    }
}

static void BuyMenuAddItemIcon(enum Item item, u8 iconSlot)
{
    u8 spriteId;
    u8 *spriteIdPtr = &sShopData->itemSpriteIds[iconSlot];
    if (*spriteIdPtr != SPRITE_NONE)
        return;

    // on the counter in front of the clerk; item icons are 24x24 art in the top-left of a 32x32 sprite
    if (sMartInfo.martType == MART_TYPE_NORMAL || item == ITEM_LIST_END)
    {
        spriteId = AddItemIconSprite(iconSlot + TAG_ITEM_ICON_BASE, iconSlot + TAG_ITEM_ICON_BASE, item);
        if (spriteId != MAX_SPRITES)
        {
            *spriteIdPtr = spriteId;
            gSprites[spriteId].x2 = OSHOP_ICON_X + (32 - 24) / 2;
            gSprites[spriteId].y2 = OSHOP_ICON_Y + (32 - 24) / 2;
            gSprites[spriteId].oam.priority = 2;
        }
    }
    else
    {
        spriteId = AddDecorationIconObject(item, OSHOP_ICON_X, OSHOP_ICON_Y, 2, iconSlot + TAG_ITEM_ICON_BASE, iconSlot + TAG_ITEM_ICON_BASE);
        if (spriteId != MAX_SPRITES)
            *spriteIdPtr = spriteId;
    }
}

static void BuyMenuRemoveItemIcon(enum Item item, u8 iconSlot)
{
    u8 *spriteIdPtr = &sShopData->itemSpriteIds[iconSlot];
    if (*spriteIdPtr == SPRITE_NONE)
        return;

    FreeSpriteTilesByTag(iconSlot + TAG_ITEM_ICON_BASE);
    FreeSpritePaletteByTag(iconSlot + TAG_ITEM_ICON_BASE);
    DestroySprite(&gSprites[*spriteIdPtr]);
    *spriteIdPtr = SPRITE_NONE;
}

static void BuyMenuInitBgs(void)
{
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sShopBuyMenuBgTemplates, ARRAY_COUNT(sShopBuyMenuBgTemplates));
    SetBgTilemapBuffer(0, sShopData->tilemapBuffers[0]);
    SetBgTilemapBuffer(1, sShopData->tilemapBuffers[1]);
    SetBgTilemapBuffer(2, sShopData->tilemapBuffers[2]);
    SetBgTilemapBuffer(3, sShopData->tilemapBuffers[3]);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 0);
    SetGpuReg(REG_OFFSET_BG2HOFS, 0);
    SetGpuReg(REG_OFFSET_BG2VOFS, 0);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    ChangeBgX(3, 0, BG_COORD_SET);
    ChangeBgY(3, 0, BG_COORD_SET);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    ShowBg(0);
    ShowBg(1);
    ShowBg(2);
    ShowBg(3);
}

// Orchid art (export_mart.py): BG2 shop art + BG3 grid tiles, BG palettes 0-4, the Orchid window palette
// (message box + YES/NO) in 15, and the message / YES/NO frame tiles at the start of BG0's tiles.
static void BuyMenuDecompressBgGraphics(void)
{
    u32 x, y;
    u16 *grid = sShopData->tilemapBuffers[3];

    DecompressAndCopyTileDataToVram(2, gOrchidShopBg_Gfx, 0, 0, 0);
    DecompressDataWithHeaderWram(gOrchidShopBg_Tilemap, sShopData->tilemapBuffers[2]);
    for (y = 0; y < 32; y++)
    {
        for (x = 0; x < 32; x++)
            grid[y * 32 + x] = (OSHOP_GRID_TILE + (x & 1) + (y & 1) * 2) | (OSHOP_PAL_GRID << 12);
    }
    LoadPalette(gOrchidShopBg_Pal, BG_PLTT_ID(0), OSHOP_NUM_BG_PALS * PLTT_SIZE_4BPP);
    LoadPalette(gOrchidYesNoFrame_Pal, BG_PLTT_ID(OSHOP_WINDOW_PAL), PLTT_SIZE_4BPP);
    LoadBgTiles(0, gOrchidShopMsgFrame_Gfx, OSHOP_MSG_FRAME_TILES * TILE_SIZE_4BPP, OSHOP_MSG_FRAME_BASE);
    LoadOrchidYesNoFrame(0, ORCHID_SHOP_YESNO_FRAME_TILE);
}

static void BuyMenuInitWindows(void)
{
    InitWindows(sShopBuyMenuWindowTemplates);
    DeactivateAllTextPrinters();
    PutWindowTilemap(WIN_MONEY);
    PutWindowTilemap(WIN_ITEM_LIST);
    PutWindowTilemap(WIN_ITEM_DESCRIPTION);
}

static void BuyMenuPrint(u8 windowId, const u8 *text, u8 x, u8 y, s8 speed, u8 colorSet)
{
    AddTextPrinterParameterized4(windowId, FONT_NORMAL, x, y, 0, 0, sShopBuyMenuTextColors[colorSet], speed, text);
}

// The Orchid dialogue box (windows.dialogue_box): the std message routine draws the vanilla frame, which is
// then replaced by the Orchid frame's tilemap (the text window keeps its own cells).
static void OrchidShop_DrawMessageFrame(void)
{
    u16 *map = GetBgTilemapBuffer(0);
    u32 r, c;

    for (r = 0; r < OSHOP_MSG_FRAME_ROWS; r++)
    {
        for (c = 0; c < 30; c++)
        {
            u16 e = sOrchidShopMsgFrame[r][c];
            if (e == OSHOP_MSG_SKIP)
                continue;
            map[(OSHOP_MSG_FRAME_TOP + r) * 32 + c] = e ? ((e & 0xC00) | ((e & 0x3FF) + OSHOP_MSG_FRAME_BASE) | (OSHOP_WINDOW_PAL << 12)) : 0;
        }
    }
    // the std routine turns the window's last column into message-box frame art (DrawDialogueFrameRightEdge);
    // this window is narrower and keeps its own cells
    PutWindowTilemap(WIN_MESSAGE);
}

static const u8 sOrchidShopMessageColors[3] = {TEXT_COLOR_WHITE, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_LIGHT_GRAY};

static void Task_OrchidShopContinueAfterMessage(u8 taskId)
{
    if (!RunTextPrintersRetIsActive(WIN_MESSAGE))
        sShopData->messageNextTask(taskId);
}

// As DisplayMessageAndContinueTask, but the text starts on the window's top row (mock_mart.msg_box, y 120)
// rather than 1 px lower.
static void BuyMenuDisplayMessage(u8 taskId, const u8 *text, TaskFunc callback)
{
    DrawDialogFrameWithCustomTileAndPalette(WIN_MESSAGE, TRUE, OSHOP_MSG_FRAME_BASE, OSHOP_WINDOW_PAL);
    OrchidShop_DrawMessageFrame();
    if (text != gStringVar4)
        StringExpandPlaceholders(gStringVar4, text);
    gTextFlags.canABSpeedUpPrint = 1;
    AddTextPrinterParameterized4(WIN_MESSAGE, FONT_NORMAL, 0, 0, 0, 0, sOrchidShopMessageColors, GetPlayerTextSpeedDelay(), gStringVar4);
    sShopData->messageNextTask = callback;
    gTasks[taskId].func = Task_OrchidShopContinueAfterMessage;
    ScheduleBgCopyTilemapToVram(0);
}

static void BuyMenuDrawGraphics(void)
{
    OrchidShop_PrintMoney();
    ScheduleBgCopyTilemapToVram(0);
    ScheduleBgCopyTilemapToVram(1);
    ScheduleBgCopyTilemapToVram(2);
    ScheduleBgCopyTilemapToVram(3);
}

static void Task_BuyMenu(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    if (!gPaletteFade.active)
    {
        s32 itemId = ListMenu_ProcessInput(tListTaskId);
        ListMenuGetScrollAndRow(tListTaskId, &sShopData->scrollOffset, &sShopData->selectedRow);

        switch (itemId)
        {
        case LIST_NOTHING_CHOSEN:
            break;
        case LIST_CANCEL:
            PlaySE(SE_SELECT);
            ExitBuyMenu(taskId);
            break;
        default:
            PlaySE(SE_SELECT);
            tItemId = itemId;
            ClearWindowTilemap(WIN_ITEM_DESCRIPTION); // the message box covers the card; the row stays gold

            if (sMartInfo.martType == MART_TYPE_NORMAL)
                sShopData->totalCost = (GetItemPrice(itemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT));
            else
                sShopData->totalCost = gDecorations[itemId].price;

            if (GetItemImportance(itemId) && (CheckBagHasItem(itemId, 1) || CheckPCHasItem(itemId, 1)))
                BuyMenuDisplayMessage(taskId, gText_ThatItemIsSoldOut, BuyMenuReturnToItemList);
            else if (!IsEnoughMoney(&gSaveBlock1Ptr->money, sShopData->totalCost))
            {
                BuyMenuDisplayMessage(taskId, gText_YouDontHaveMoney, BuyMenuReturnToItemList);
            }
            else
            {
                if (sMartInfo.martType == MART_TYPE_NORMAL)
                {
                    CopyItemName(itemId, gStringVar1);
                    if (GetItemImportance(itemId))
                    {
                        ConvertIntToDecimalStringN(gStringVar2, sShopData->totalCost, STR_CONV_MODE_LEFT_ALIGN, 6);
                        StringExpandPlaceholders(gStringVar4, gText_YouWantedVar1ThatllBeVar2);
                        tItemCount = 1;
                        sShopData->totalCost = (GetItemPrice(tItemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT)) * tItemCount;
                        BuyMenuDisplayMessage(taskId, gStringVar4, BuyMenuConfirmPurchase);
                    }
                    else if (GetItemPocket(itemId) == POCKET_TM_HM)
                    {
                        StringCopy(gStringVar2, GetMoveName(ItemIdToBattleMoveId(itemId)));
                        BuyMenuDisplayMessage(taskId, gText_Var1CertainlyHowMany2, Task_BuyHowManyDialogueInit);
                    }
                    else
                    {
                        BuyMenuDisplayMessage(taskId, gText_Var1CertainlyHowMany, Task_BuyHowManyDialogueInit);
                    }
                }
                else
                {
                    StringCopy(gStringVar1, gDecorations[itemId].name);
                    ConvertIntToDecimalStringN(gStringVar2, sShopData->totalCost, STR_CONV_MODE_LEFT_ALIGN, MAX_MONEY_DIGITS);

                    if (sMartInfo.martType == MART_TYPE_DECOR)
                        StringExpandPlaceholders(gStringVar4, gText_Var1IsItThatllBeVar2);
                    else // MART_TYPE_DECOR2
                        StringExpandPlaceholders(gStringVar4, gText_YouWantedVar1ThatllBeVar2);

                    BuyMenuDisplayMessage(taskId, gStringVar4, BuyMenuConfirmPurchase);
                }
            }
            break;
        }
    }
}

static void Task_BuyHowManyDialogueInit(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    u16 maxQuantity;

    // Orchid: the hanging price tag drops over the list (quantity, total, coin + money left)
    tItemCount = 1;
    BuyMenuPrintItemQuantityAndPrice(taskId);
    OrchidShop_ShowQuantityTag(TRUE);

    // Avoid division by zero in-case something costs 0 pokedollars.
    if (sShopData->totalCost == 0)
        maxQuantity = MAX_BAG_ITEM_CAPACITY;
    else
        maxQuantity = GetMoney(&gSaveBlock1Ptr->money) / sShopData->totalCost;

    if (maxQuantity > MAX_BAG_ITEM_CAPACITY)
        sShopData->maxQuantity = MAX_BAG_ITEM_CAPACITY;
    else
        sShopData->maxQuantity = maxQuantity;

    gTasks[taskId].func = Task_BuyHowManyDialogueHandleInput;
}

static void Task_BuyHowManyDialogueHandleInput(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    if (AdjustQuantityAccordingToDPadInput(&tItemCount, sShopData->maxQuantity) == TRUE)
    {
        sShopData->totalCost = (GetItemPrice(tItemId) >> IsPokeNewsActive(POKENEWS_SLATEPORT)) * tItemCount;
        BuyMenuPrintItemQuantityAndPrice(taskId);
    }
    else
    {
        if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            OrchidShop_ShowQuantityTag(FALSE);
            PutWindowTilemap(WIN_ITEM_LIST);
            CopyItemName(tItemId, gStringVar1);
            ConvertIntToDecimalStringN(gStringVar2, tItemCount, STR_CONV_MODE_LEFT_ALIGN, MAX_ITEM_DIGITS);
            ConvertIntToDecimalStringN(gStringVar3, sShopData->totalCost, STR_CONV_MODE_LEFT_ALIGN, MAX_MONEY_DIGITS);
            BuyMenuDisplayMessage(taskId, gText_Var1AndYouWantedVar2, BuyMenuConfirmPurchase);
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            OrchidShop_ShowQuantityTag(FALSE);
            BuyMenuReturnToItemList(taskId);
        }
    }
}

static void BuyMenuConfirmPurchase(u8 taskId)
{
    // Orchid YES/NO: frame tiles and the Orchid window palette were loaded with the screen
    CreateOrchidYesNoMenuWithCallbacks(taskId, &sShopBuyMenuYesNoWindowTemplates, ORCHID_SHOP_YESNO_FRAME_TILE, OSHOP_WINDOW_PAL, &sShopPurchaseYesNoFuncs);
}

static void BuyMenuTryMakePurchase(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    PutWindowTilemap(WIN_ITEM_LIST);

    if (sMartInfo.martType == MART_TYPE_NORMAL)
    {
        if (AddBagItem(tItemId, tItemCount) == TRUE)
        {
            GetSetItemObtained(tItemId, FLAG_SET_ITEM_OBTAINED);
            RecordItemPurchase(taskId);
            BuyMenuDisplayMessage(taskId, gText_HereYouGoThankYou, BuyMenuSubtractMoney);
        }
        else
        {
            BuyMenuDisplayMessage(taskId, gText_NoMoreRoomForThis, BuyMenuReturnToItemList);
        }
    }
    else
    {
        if (DecorationAdd(tItemId))
        {
            if (sMartInfo.martType == MART_TYPE_DECOR)
                BuyMenuDisplayMessage(taskId, gText_ThankYouIllSendItHome, BuyMenuSubtractMoney);
            else // MART_TYPE_DECOR2
                BuyMenuDisplayMessage(taskId, gText_ThanksIllSendItHome, BuyMenuSubtractMoney);
        }
        else
        {
            BuyMenuDisplayMessage(taskId, gText_SpaceForVar1Full, BuyMenuReturnToItemList);
        }
    }
}

static void BuyMenuSubtractMoney(u8 taskId)
{
    IncrementGameStat(GAME_STAT_SHOPPED);
    RemoveMoney(&gSaveBlock1Ptr->money, sShopData->totalCost);
    PlaySE(SE_SHOP);
    OrchidShop_PrintMoney();

    if (sMartInfo.martType == MART_TYPE_NORMAL)
        gTasks[taskId].func = Task_ReturnToItemListAfterItemPurchase;
    else
        gTasks[taskId].func = Task_ReturnToItemListAfterDecorationPurchase;
}

static void Task_ReturnToItemListAfterItemPurchase(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    if (JOY_NEW(A_BUTTON | B_BUTTON))
    {
        u16 premierBallsToAdd = tItemCount / 10;
        if (premierBallsToAdd >= 1
         && ((I_PREMIER_BALL_BONUS <= GEN_7 && tItemId == ITEM_POKE_BALL)
          || (I_PREMIER_BALL_BONUS >= GEN_8 && (GetItemPocket(tItemId) == POCKET_POKE_BALLS))))
        {
            u32 spaceAvailable = GetFreeSpaceForItemInBag(ITEM_PREMIER_BALL);
            if (spaceAvailable < premierBallsToAdd)
                premierBallsToAdd = spaceAvailable;
        }
        else
        {
            premierBallsToAdd = 0;
        }

        PlaySE(SE_SELECT);
        AddBagItem(ITEM_PREMIER_BALL, premierBallsToAdd);
        if (premierBallsToAdd > 0)
        {
            OrchidShop_ShowBonusBall(TRUE);
            ConvertIntToDecimalStringN(gStringVar1, premierBallsToAdd, STR_CONV_MODE_LEFT_ALIGN, MAX_ITEM_DIGITS);
            BuyMenuDisplayMessage(taskId, (premierBallsToAdd >= 2 ? gText_ThrowInPremierBalls : gText_ThrowInPremierBall), BuyMenuReturnToItemList);
        }
        else
        {
            BuyMenuReturnToItemList(taskId);
        }
    }
}

static void Task_ReturnToItemListAfterDecorationPurchase(u8 taskId)
{
    if (JOY_NEW(A_BUTTON | B_BUTTON))
    {
        PlaySE(SE_SELECT);
        BuyMenuReturnToItemList(taskId);
    }
}

static void BuyMenuReturnToItemList(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    ClearDialogWindowAndFrameToTransparent(WIN_MESSAGE, FALSE);
    OrchidShop_ShowBonusBall(FALSE);
    RedrawListMenu(tListTaskId);
    PutWindowTilemap(WIN_ITEM_LIST);
    PutWindowTilemap(WIN_ITEM_DESCRIPTION);
    ScheduleBgCopyTilemapToVram(0);
    gTasks[taskId].func = Task_BuyMenu;
}

// The hanging tag (mock_mart.a_qty): ×NNN in the recessed well, the total top-right, money left below it.
static void BuyMenuPrintItemQuantityAndPrice(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    u8 str[24];

    CopyToWindowPixelBuffer(WIN_QUANTITY, gOrchidShopQtyTag_Gfx, OSHOP_QTY_WIN_W * OSHOP_QTY_WIN_H * TILE_SIZE_4BPP, 0);

    ConvertIntToDecimalStringN(gStringVar1, tItemCount, STR_CONV_MODE_LEADING_ZEROS, MAX_ITEM_DIGITS);
    StringExpandPlaceholders(str, gText_xVar1);
    BuyMenuPrint(WIN_QUANTITY, str, OSHOP_QTY_CENTRE_X - GetStringWidth(FONT_NORMAL, str, 0) / 2, OSHOP_QTY_Y, TEXT_SKIP_DRAW, COLORID_NORMAL);

    ConvertIntToDecimalStringN(gStringVar1, sShopData->totalCost, STR_CONV_MODE_LEFT_ALIGN, MAX_MONEY_DIGITS);
    StringExpandPlaceholders(str, gText_PokedollarVar1);
    BuyMenuPrint(WIN_QUANTITY, str, GetStringRightAlignXOffset(FONT_NORMAL, str, OSHOP_QTY_RIGHT), OSHOP_TOTAL_Y, TEXT_SKIP_DRAW, COLORID_PRICE);

    ConvertIntToDecimalStringN(gStringVar1, GetMoney(&gSaveBlock1Ptr->money) - sShopData->totalCost, STR_CONV_MODE_LEFT_ALIGN, MAX_MONEY_DIGITS);
    StringExpandPlaceholders(str, gText_PokedollarVar1);
    BuyMenuPrint(WIN_QUANTITY, str, GetStringRightAlignXOffset(FONT_NORMAL, str, OSHOP_QTY_RIGHT), OSHOP_LEFT_Y, TEXT_SKIP_DRAW, COLORID_NORMAL);

    CopyWindowToVram(WIN_QUANTITY, COPYWIN_GFX);
}

static void ExitBuyMenu(u8 taskId)
{
    gFieldCallback = MapPostLoadHook_ReturnToShopMenu;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    gTasks[taskId].func = Task_ExitBuyMenu;
}

static void Task_ExitBuyMenu(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        BuyMenuFreeMemory();
        SetMainCallback2(CB2_ReturnToField);
        DestroyTask(taskId);
    }
}

static void ClearItemPurchases(void)
{
    sPurchaseHistoryId = 0;
    memset(gMartPurchaseHistory, 0, sizeof(gMartPurchaseHistory));
}

static void RecordItemPurchase(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    u16 i;

    for (i = 0; i < ARRAY_COUNT(gMartPurchaseHistory); i++)
    {
        if (gMartPurchaseHistory[i].itemId == tItemId && gMartPurchaseHistory[i].quantity != 0)
        {
            if (gMartPurchaseHistory[i].quantity + tItemCount > 255)
                gMartPurchaseHistory[i].quantity = 255;
            else
                gMartPurchaseHistory[i].quantity += tItemCount;
            return;
        }
    }

    if (sPurchaseHistoryId < ARRAY_COUNT(gMartPurchaseHistory))
    {
        gMartPurchaseHistory[sPurchaseHistoryId].itemId = tItemId;
        gMartPurchaseHistory[sPurchaseHistoryId].quantity = tItemCount;
        sPurchaseHistoryId++;
    }
}

#undef tItemCount
#undef tItemId
#undef tListTaskId
#undef tCallbackHi
#undef tCallbackLo

void CreatePokemartMenu(const u16 *itemsForSale)
{
    CreateShopMenu(MART_TYPE_NORMAL);
    SetShopItemsForSale(itemsForSale);
    ClearItemPurchases();
    SetShopMenuCallback(ScriptContext_Enable);
}

void CreateDecorationShop1Menu(const u16 *itemsForSale)
{
    CreateShopMenu(MART_TYPE_DECOR);
    SetShopItemsForSale(itemsForSale);
    SetShopMenuCallback(ScriptContext_Enable);
}

void CreateDecorationShop2Menu(const u16 *itemsForSale)
{
    CreateShopMenu(MART_TYPE_DECOR2);
    SetShopItemsForSale(itemsForSale);
    SetShopMenuCallback(ScriptContext_Enable);
}
