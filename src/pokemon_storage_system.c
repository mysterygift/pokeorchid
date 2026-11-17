#include "global.h"
#include "malloc.h"
#include "bg.h"
#include "data.h"
#include "decompress.h"
#include "dma3.h"
#include "dynamic_placeholder_text_util.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_screen_effect.h"
#include "field_weather.h"
#include "fldeff_misc.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "international_string_util.h"
#include "item.h"
#include "item_icon.h"
#include "item_menu.h"
#include "mail.h"
#include "main.h"
#include "menu.h"
#include "mon_markings.h"
#include "naming_screen.h"
#include "overworld.h"
#include "palette.h"
#include "pc_screen_effect.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "pokemon_summary_screen.h"
#include "pokemon_storage_system.h"
#include "script.h"
#include "sound.h"
#include "string_util.h"
#include "strings.h"
#include "text.h"
#include "text_window.h"
#include "trig.h"
#include "walda_phrase.h"
#include "window.h"
#include "constants/form_change_types.h"
#include "constants/items.h"
#include "constants/party_menu.h"
#include "constants/moves.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/pokemon_icon.h"
#include "constants/orchid_ui.h"
#include "chooseboxmon.h"
#include "party_menu.h"
#include "data/pokemon_storage_orchid.h"
#include "battle_main.h"

/*
    NOTE: This file is large. Some general groups of functions have
          been labeled with commented headers to make navigation easier.
          Search for "SECTION:" to locate them. These sections are not
          hard and fast rules, but give a basic idea of where certain
          types of functions are likely located.
*/

// PC main menu options
enum {
#if OW_PC_MOVE_ORDER <= GEN_3
    OPTION_WITHDRAW,
    OPTION_DEPOSIT,
    OPTION_MOVE_MONS,
#elif OW_PC_MOVE_ORDER >= GEN_4 && OW_PC_MOVE_ORDER <= GEN_6_XY
    OPTION_DEPOSIT,
    OPTION_WITHDRAW,
    OPTION_MOVE_MONS,
#elif OW_PC_MOVE_ORDER >= GEN_7
    OPTION_MOVE_MONS,
    OPTION_DEPOSIT,
    OPTION_WITHDRAW,
#endif
    OPTION_MOVE_ITEMS,
    OPTION_EXIT,
    OPTIONS_COUNT,
    OPTION_SELECT_MON
};

// IDs for messages to print with PrintMessage
enum {
    MSG_EXIT_BOX,
    MSG_WHAT_YOU_DO,
    MSG_PICK_A_THEME,
    MSG_PICK_A_WALLPAPER,
    MSG_IS_SELECTED,
    MSG_JUMP_TO_WHICH_BOX,
    MSG_DEPOSIT_IN_WHICH_BOX,
    MSG_WAS_DEPOSITED,
    MSG_BOX_IS_FULL,
    MSG_RELEASE_POKE,
    MSG_WAS_RELEASED,
    MSG_BYE_BYE,
    MSG_MARK_POKE,
    MSG_LAST_POKE,
    MSG_PARTY_FULL,
    MSG_HOLDING_POKE,
    MSG_WHICH_ONE_WILL_TAKE,
    MSG_CANT_RELEASE_EGG,
    MSG_CONTINUE_BOX,
    MSG_CAME_BACK,
    MSG_WORRIED,
    MSG_SURPRISE,
    MSG_PLEASE_REMOVE_MAIL,
    MSG_IS_SELECTED2,
    MSG_GIVE_TO_MON,
    MSG_PLACED_IN_BAG,
    MSG_BAG_FULL,
    MSG_PUT_IN_BAG,
    MSG_ITEM_IS_HELD,
    MSG_CHANGED_TO_ITEM,
    MSG_CANT_STORE_MAIL,
};

// IDs for how to resolve variables in the above messages
enum {
    MSG_VAR_NONE,
    MSG_VAR_MON_NAME_1,
    MSG_VAR_MON_NAME_2, // Unused
    MSG_VAR_MON_NAME_3, // Unused
    MSG_VAR_RELEASE_MON_1,
    MSG_VAR_RELEASE_MON_2, // Unused
    MSG_VAR_RELEASE_MON_3,
    MSG_VAR_ITEM_NAME,
};

// IDs for menu selection items. See SetMenuText, HandleMenuInput, etc
enum {
    MENU_CANCEL,
    MENU_STORE,
    MENU_WITHDRAW,
    MENU_MOVE,
    MENU_SHIFT,
    MENU_PLACE,
    MENU_SUMMARY,
    MENU_RELEASE,
    MENU_MARK,
    MENU_JUMP,
    MENU_WALLPAPER,
    MENU_NAME,
    MENU_TAKE,
    MENU_GIVE,
    MENU_GIVE_2,
    MENU_SWITCH,
    MENU_BAG,
    MENU_INFO,
    MENU_SCENERY_1,
    MENU_SCENERY_2,
    MENU_SCENERY_3,
    MENU_ETCETERA,
    MENU_FRIENDS,
    MENU_FOREST,
    MENU_CITY,
    MENU_DESERT,
    MENU_SAVANNA,
    MENU_CRAG,
    MENU_VOLCANO,
    MENU_SNOW,
    MENU_CAVE,
    MENU_BEACH,
    MENU_SEAFLOOR,
    MENU_RIVER,
    MENU_SKY,
    MENU_POLKADOT,
    MENU_POKECENTER,
    MENU_MACHINE,
    MENU_SIMPLE,
    MENU_SELECT,
};
#define MENU_WALLPAPER_SETS_START MENU_SCENERY_1
#define MENU_WALLPAPERS_START MENU_FOREST
#define SPECIES_MASK 0x3FFF

// Return IDs for input handlers
enum {
    INPUT_NONE,
    INPUT_MOVE_CURSOR,
    INPUT_2, // Unused
    INPUT_3, // Unused
    INPUT_CLOSE_BOX,
    INPUT_SHOW_PARTY,
    INPUT_HIDE_PARTY,
    INPUT_BOX_OPTIONS,
    INPUT_IN_MENU,
    INPUT_SCROLL_RIGHT,
    INPUT_SCROLL_LEFT,
    INPUT_DEPOSIT,
    INPUT_WITHDRAW,
    INPUT_MOVE_MON,
    INPUT_SHIFT_MON,
    INPUT_PLACE_MON,
    INPUT_TAKE_ITEM,
    INPUT_GIVE_ITEM,
    INPUT_SWITCH_ITEMS,
    INPUT_PRESSED_B,
    INPUT_MULTIMOVE_START,
    INPUT_MULTIMOVE_CHANGE_SELECTION,
    INPUT_MULTIMOVE_SINGLE,
    INPUT_MULTIMOVE_GRAB_SELECTION,
    INPUT_MULTIMOVE_UNABLE,
    INPUT_MULTIMOVE_MOVE_MONS,
    INPUT_MULTIMOVE_PLACE_MONS,
    INPUT_SELECT_MON,
};

enum {
    SCREEN_CHANGE_EXIT_BOX,
    SCREEN_CHANGE_SUMMARY_SCREEN,
    SCREEN_CHANGE_NAME_BOX,
    SCREEN_CHANGE_ITEM_FROM_BAG,
};

enum {
    MODE_PARTY,
    MODE_BOX,
    MODE_MOVE,
};

enum {
    CURSOR_AREA_IN_BOX,
    CURSOR_AREA_IN_PARTY,
    CURSOR_AREA_BOX_TITLE,
    CURSOR_AREA_BUTTONS, // Party Pokémon and Close Box
};
#define CURSOR_AREA_IN_HAND CURSOR_AREA_BOX_TITLE // Alt name for cursor area used by Move Items

enum {
    CURSOR_ANIM_BOUNCE,
    CURSOR_ANIM_STILL,
    CURSOR_ANIM_OPEN,
    CURSOR_ANIM_FIST,
    CURSOR_ANIM_FLASH, // Orchid: the ring flashes when a Pokémon is picked up or put down
};

// Special box ids for the choose box menu
#define BOXID_NONE_CHOSEN 200
#define BOXID_CANCELED    201

enum {
    PALTAG_MON_ICON_0 = POKE_ICON_BASE_PAL_TAG,
    PALTAG_MON_ICON_1, // Used implicitly in CreateMonIconSprite
    PALTAG_MON_ICON_2, // Used implicitly in CreateMonIconSprite
    PALTAG_MON_ICON_3, // Used implicitly in CreateMonIconSprite
    PALTAG_MON_ICON_4, // Used implicitly in CreateMonIconSprite
    PALTAG_MON_ICON_5, // Used implicitly in CreateMonIconSprite
    PALTAG_DISPLAY_MON,
    PALTAG_MISC_1,
    PALTAG_MARKING_COMBO,
    PALTAG_BOX_TITLE,
    PALTAG_MISC_2,
    PALTAG_ITEM_ICON_0,
    PALTAG_ITEM_ICON_1, // Used implicitly in CreateItemIconSprites
    PALTAG_ITEM_ICON_2, // Used implicitly in CreateItemIconSprites
    PALTAG_MARKING_MENU,
    PALTAG_MARKING_MENU_2, // Used implicitly by the markings menu (basePaletteTag + 1)
    PALTAG_DISC_ITEM,      // Orchid: held item icon in the info panel's disc
    PALTAG_TYPE_0,         // Orchid: type icon palettes (gMoveTypes_Pal rows)
    PALTAG_TYPE_1,
    PALTAG_TYPE_2,
};

enum {
    GFXTAG_CURSOR,
    GFXTAG_CURSOR_SHADOW,
    GFXTAG_DISPLAY_MON,
    GFXTAG_BOX_TITLE,
    GFXTAG_BOX_TITLE_ALT,
    GFXTAG_WAVEFORM,
    GFXTAG_ARROW,
    GFXTAG_ITEM_ICON_0,
    GFXTAG_ITEM_ICON_1, // Used implicitly in CreateItemIconSprites
    GFXTAG_ITEM_ICON_2, // Used implicitly in CreateItemIconSprites
    GFXTAG_CHOOSE_BOX_MENU,
    GFXTAG_CHOOSE_BOX_MENU_SIDES, // Used implicitly in LoadChooseBoxMenuGfx
    GFXTAG_12, // Unused
    GFXTAG_MARKING_MENU,
    GFXTAG_14, // Unused
    GFXTAG_15, // Unused
    GFXTAG_MARKING_COMBO,
    GFXTAG_17, // Unused
    GFXTAG_HOLD_TAG,   // Orchid: MOVE ITEMS hold tags
    GFXTAG_TYPE_ICONS, // Orchid: two 32x16 type icons in the info panel
    GFXTAG_DISC_ITEM,  // Orchid: held item icon in the info panel's disc
    GFXTAG_MON_ICON,
};

// The maximum number of Pokémon icons that can appear on-screen.
// By default the limit is 40 (though in practice only 37 can be).
#define MAX_MON_ICONS max(IN_BOX_COUNT + PARTY_SIZE + 1, 40)

// The maximum number of item icons that can appear on-screen while
// moving held items. 1 in the cursor, and 2 more while switching
// between 2 Pokémon with held items
#define MAX_ITEM_ICONS 3

// IDs for the item icons affine anims
enum {
    ITEM_ANIM_NONE,
    ITEM_ANIM_APPEAR,
    ITEM_ANIM_DISAPPEAR,
    ITEM_ANIM_PICK_UP,
    ITEM_ANIM_PUT_DOWN,
    ITEM_ANIM_PUT_AWAY,
    ITEM_ANIM_LARGE,
};

// IDs for the item icon sprite callbacks
enum {
    ITEM_CB_WAIT_ANIM,
    ITEM_CB_TO_HAND,
    ITEM_CB_TO_MON,
    ITEM_CB_SWAP_TO_HAND,
    ITEM_CB_SWAP_TO_MON,
    ITEM_CB_UNUSED_1,
    ITEM_CB_UNUSED_2,
    ITEM_CB_HIDE_PARTY,
};

enum {
    RELEASE_ANIM_RELEASE,
    RELEASE_ANIM_CAME_BACK,
};

// IDs for InitMonPlaceChange
enum {
    CHANGE_GRAB,
    CHANGE_PLACE,
    CHANGE_SHIFT,
};

// Modes for selecting and moving Pokémon in the box.
// "MULTIPLE" mode allows up to an entire box to be
// picked up at once by pressing Select then holding
// down the A button. While holding A down, the player
// may move the cursor around to select multiple Pokémon.
// This is MOVE_MODE_MULTIPLE_SELECTING. After releasing A
// those Pokémon will be picked up and can be moved around
// as a single unit. This is MOVE_MODE_MULTIPLE_MOVING
enum {
    MOVE_MODE_NORMAL,
    MOVE_MODE_MULTIPLE_SELECTING,
    MOVE_MODE_MULTIPLE_MOVING,
};

// IDs for the main functions for moving multiple Pokémon.
// Given as arguments to MultiMove_SetFunction
enum {
    MULTIMOVE_START,
    MULTIMOVE_CANCEL, // If only 1 Pokémon is grabbed
    MULTIMOVE_CHANGE_SELECTION,
    MULTIMOVE_GRAB_SELECTION,
    MULTIMOVE_MOVE_MONS,
    MULTIMOVE_PLACE_MONS,
};

// IDs for TilemapUtil
enum {
    TILEMAPID_PKMN_DATA, // The "Pkmn Data" text at the top of the display
    TILEMAPID_PARTY_MENU,
    TILEMAPID_CLOSE_BUTTON,
    TILEMAPID_COUNT
};

// Window IDs for sWindowTemplates
enum {
    WIN_DISPLAY_INFO,
    WIN_MESSAGE,
    WIN_ITEM_DESC,
    WIN_TITLE,     // Orchid: box name + count on the title tab (BG1)
    WIN_PSLOT_0,   // Orchid: Lv + HP bar of each party slot (BG1), 6 windows
};

// Orchid BG palette slots (see dev_scripts/orchid_ui/export_pc.py)
#define OPC_BG_UI         0
#define OPC_BG_UI_GOLD    1
#define OPC_BG_SLOT       2   // 2..7: party slot G / Y / R, then their gold copies; the colour picker and
                              // the multi-move icon layer borrow them while the party panel is hidden
#define OPC_BG_BOX        8   // 8, 9: current / incoming box colour
#define OPC_BG_GRID       10
#define OPC_BG_TITLE      11
#define OPC_BG_TITLE_GOLD 12
#define OPC_BG_WINDOW     14  // Orchid window palette (frames, messages, menus, YES/NO)
#define OPC_BG_TEXTWIN    15  // vanilla text window palette (MOVE ITEMS item info)
#define OPC_FRAME_TILE    2   // BG0 tiles 2-10: Orchid std frame (tiles 0-1 stay blank: they are 8bpp tile 0 of the multi-move layer)
#define OPC_SWATCH_TILE   11  // BG0 tiles 11-19: colour picker swatches (below the multi-move window's tiles from 20)
#define OPC_BG1_WIN_BASE  OPC_BG1_ART_TILES
#define OPC_ICON_CLIP_X   92  // sliding box icons hide once they would cross x 80 (the BG2 clip)

struct Wallpaper
{
    const u32 *tiles;
    const u32 *tilemap;
    const u16 *palettes;
};

struct StorageMessage
{
    const u8 *text;
    u8 format;
};

struct StorageMenu
{
    const u8 *text;
    int textId;
};

struct ChooseBoxMenu
{
    u8 windowId; // Orchid: the popup is a BG0 window
    struct Sprite *menuSprite;
    struct Sprite *menuSideSprites[4];
    struct Sprite *arrowSprites[2];
    bool32 loadedPalette;
    u16 tileTag;
    u16 paletteTag;
    u8 curBox;
    u8 subpriority;
};

struct ItemIcon
{
    struct Sprite *sprite;
    u8 *tiles;
    u16 palIndex;
    u8 area;
    u8 pos;
    bool8 active;
};

struct PokemonStorageSystemData
{
    u8 state;
    u8 boxOption;
    u8 screenChangeType;
    bool8 isReopening;
    u8 taskId;
    u16 partyMenuTilemapBuffer[0x108];
    u16 partyMenuY;
    u8 partyMenuMoveTimer;
    u8 showPartyMenuState;
    bool8 closeBoxFlashing;
    u8 closeBoxFlashTimer;
    bool8 closeBoxFlashState;
    s16 newCurrBoxId;
    u16 bg2_X;
    s16 scrollSpeed;
    u16 scrollTimer;
    u8 wallpaperOffset;
    u8 ALIGNED(2) boxTitleTiles[1024];
    u8 boxTitleCycleId;
    u8 wallpaperLoadBoxId;
    s8 wallpaperLoadDir;
    u16 boxTitlePal[16];
    u16 boxTitlePalOffset;
    u16 boxTitleAltPalOffset;
    struct Sprite *curBoxTitleSprites[2];
    struct Sprite *nextBoxTitleSprites[2];
    struct Sprite *arrowSprites[2];
    u32 wallpaperPalBits;
    s16 wallpaperSetId;
    s16 wallpaperId;
    u16 wallpaperTilemap[360];
    u8 wallpaperChangeState;
    u8 scrollState;
    u8 scrollToBoxId;
    s8 scrollDirection;
    u8 *wallpaperTiles;
    struct Sprite *movingMonSprite;
    struct Sprite *partySprites[PARTY_SIZE];
    struct Sprite *boxMonsSprites[IN_BOX_COUNT];
    struct Sprite **shiftMonSpritePtr;
    struct Sprite **releaseMonSpritePtr;
    u16 numIconsPerSpecies[MAX_MON_ICONS];
    enum Species iconSpeciesList[MAX_MON_ICONS];
    enum Species boxSpecies[IN_BOX_COUNT];
    u32 boxPersonalities[IN_BOX_COUNT];
    bool8 boxIsEgg[IN_BOX_COUNT];
    u8 incomingBoxId;
    u8 shiftTimer;
    u8 numPartyToCompact;
    u16 iconScrollDistance;
    s16 iconScrollPos;
    s16 iconScrollSpeed;
    u16 iconScrollNumIncoming;
    u8 iconScrollCurColumn;
    s8 iconScrollDirection; // Unnecessary duplicate of scrollDirection
    u8 iconScrollState;
    struct WindowTemplate menuWindow;
    struct StorageMenu menuItems[7];
    u8 menuItemsCount;
    u8 menuWidth;
    u16 menuWindowId;
    struct Sprite *cursorSprite;
    struct Sprite *cursorShadowSprite;
    s32 cursorNewX;
    s32 cursorNewY;
    u32 cursorSpeedX;
    u32 cursorSpeedY;
    s16 cursorTargetX;
    s16 cursorTargetY;
    u16 cursorMoveSteps;
    s8 cursorVerticalWrap;
    s8 cursorHorizontalWrap;
    u8 newCursorArea;
    u8 newCursorPosition;
    u8 cursorPrevHorizPos;
    u8 cursorFlipTimer;
    u8 cursorPalNums[2];
    const u16 *displayMonPalette;
    u32 displayMonPersonality;
    enum Species displayMonSpecies;
    enum Item displayMonItemId;
    u16 displayUnusedVar;
    bool8 setMosaic;
    u8 displayMonMarkings;
    u8 displayMonLevel;
    bool8 displayMonIsEgg;
    u8 displayMonName[POKEMON_NAME_LENGTH + 1];
    u8 displayMonNameText[36];
    u8 displayMonSpeciesName[36];
    u8 displayMonGenderLvlText[36];
    u8 displayMonItemName[36];
    bool8 (*monPlaceChangeFunc)(void);
    u8 monPlaceChangeState;
    u8 shiftBoxId;
    struct Sprite *markingComboSprite;
    struct Sprite *waveformSprites[2];
    u16 *markingComboTilesPtr;
    struct MonMarkingsMenu markMenu;
    struct ChooseBoxMenu chooseBoxMenu;
    struct Pokemon movingMon;
    struct Pokemon tempMon;
    s8 canReleaseMon;
    bool8 releaseStatusResolved;
    s8 releaseCheckBoxId;
    s8 releaseCheckBoxPos;
    s8 releaseBoxId;
    s8 releaseBoxPos;
    u16 releaseCheckState;
    u16 restrictedReleaseMonMoves;
    u16 restrictedMoveList[8];
    u8 summaryMaxPos;
    u8 summaryStartPos;
    u8 summaryScreenMode;
    union
    {
        struct Pokemon *mon;
        struct BoxPokemon *box;
    } summaryMon;
    u8 messageText[40];
    u8 boxTitleText[40];
    u8 releaseMonName[POKEMON_NAME_LENGTH + 1];
    u8 itemName[20];
    u8 inBoxMovingMode;
    u16 multiMoveWindowId;
    struct ItemIcon itemIcons[MAX_ITEM_ICONS];
    enum Item movingItemId;
    u16 itemInfoWindowOffset;
    u16 displayMonPalOffset;
    u16 *displayMonTilePtr;
    struct Sprite *displayMonSprite;
    u8 ALIGNED(4) tileBuffer[MON_PIC_SIZE * MAX_MON_PIC_FRAMES];
    u8 ALIGNED(4) itemIconBuffer[0x800];
    u8 wallpaperBgTilemapBuffer[0x1000];
    u8 displayMenuTilemapBuffer[0x800];
    // Orchid UI
    u8 displayMonGender;
    s8 opcLift;          // px the held Pokémon floats above its slot (0..OPC_LIFT)
    u8 opcLiftTimer;
    u8 opcBobTimer;
    u8 opcFrame;
    u8 opcGoldOwner;     // OPC_OWN_* drawn gold
    u8 opcPartySel;      // party slot drawn gold (6 = CANCEL, 0xFF = none)
    u8 opcPartySlide;    // party panel offset in tiles (OPC_PANEL_SLIDE = hidden)
    u8 opcFilled;        // party slots holding a Pokémon (bit k)
    u8 opcSlotHp[PARTY_SIZE];
    u8 opcTitleBox;
    bool8 opcTitleDirty;
    bool8 opcTagsDirty;
    bool8 opcRingHidden; // forced off (box slide, popups)
    u8 opcColourSel;
    u8 opcColourWindow;
    u8 opcTypeSprites[2];
    u8 opcItemSprite;
    enum Item opcItemShown;
    u8 opcTagSprites[IN_BOX_COUNT + PARTY_SIZE];
    u8 *opcTypeSheet;
};

static u32 sItemIconGfxBuffer[98];

EWRAM_DATA static u8 sPreviousBoxOption = 0;
EWRAM_DATA static struct ChooseBoxMenu *sChooseBoxMenu = NULL;
EWRAM_DATA static struct PokemonStorageSystemData *sStorage = NULL;
EWRAM_DATA static bool8 sInPartyMenu = 0;
EWRAM_DATA static u8 sCurrentBoxOption = 0;
EWRAM_DATA static u8 sDepositBoxId = 0;
EWRAM_DATA static u8 sWhichToReshow = 0;
EWRAM_DATA static u8 sLastUsedBox = 0;
EWRAM_DATA static enum Item sMovingItemId = ITEM_NONE;
EWRAM_DATA static struct Pokemon sSavedMovingMon = {0};
EWRAM_DATA static s8 sCursorArea = 0;
EWRAM_DATA static s8 sCursorPosition = 0;
EWRAM_DATA static bool8 sIsMonBeingMoved = 0;
EWRAM_DATA static u8 sMovingMonOrigBoxId = 0;
EWRAM_DATA static u8 sMovingMonOrigBoxPos = 0;
EWRAM_DATA static bool8 sAutoActionOn = 0;
EWRAM_DATA static bool8 sJustOpenedBag = 0;
EWRAM_DATA static bool8 sRefreshDisplayMonGfx = FALSE;

// Main tasks
static void Task_InitPokeStorage(u8);
static void Task_PlaceMon(u8);
static void Task_ChangeScreen(u8);
static void Task_ShowPokeStorage(u8);
static void Task_OnBPressed(u8);
static void Task_HandleBoxOptions(u8);
static void Task_OnSelectedMon(u8);
static void Task_OnCloseBoxPressed(u8);
static void Task_HidePartyPokemon(u8);
static void Task_DepositMenu(u8);
static void Task_MoveMon(u8);
static void Task_GiveMovingItemToMon(u8);
static void Task_SwitchSelectedItem(u8);
static void Task_TakeItemForMoving(u8);
static void Task_WithdrawMon(u8);
static void Task_ShiftMon(u8);
static void Task_ShowPartyPokemon(u8);
static void Task_ShowItemInfo(u8);
static void Task_GiveItemFromBag(u8);
static void Task_ItemToBag(u8);
static void Task_TakeItemForMoving(u8);
static void Task_ShowMarkMenu(u8);
static void Task_ShowMonSummary(u8);
static void Task_ReleaseMon(u8);
static void Task_ReshowPokeStorage(u8);
static void Task_PokeStorageMain(u8);
static void Task_JumpBox(u8);
static void Task_HandleWallpapers(u8);
static void Task_NameBox(u8);
static void Task_PrintCantStoreMail(u8);
static void Task_HandleMovingMonFromParty(u8);

// Input handlers
static u8 InBoxInput_Normal(void);
static u8 InBoxInput_MovingMultiple(void);
static u8 InBoxInput_SelectingMultiple(void);
static u8 HandleInput(void);
static void AddBoxOptionsMenu(void);
static u8 SetSelectionMenuTexts(void);
static bool8 SetMenuTexts_Mon(void);
static bool8 SetMenuTexts_Item(void);

// Choose box menu
static void ChooseBoxMenu_CreateSprites(u8);
static void ChooseBoxMenu_DestroySprites(void);
static void ChooseBoxMenu_MoveLeft(void);
static void ChooseBoxMenu_MoveRight(void);
static void ChooseBoxMenu_PrintInfo(void);

// Options menus
static void InitMenu(void);
static void SetMenuText(u8);
static s8 GetMenuItemTextId(u8);
static void AddMenu(void);
static bool8 IsMenuLoading(void);
static s16 HandleMenuInput(void);
static void RemoveMenu(void);

// Pokémon sprites
static void InitMonIconFields(void);
static void SpriteCB_BoxMonIconScrollOut(struct Sprite *);
static void GetIncomingBoxMonData(u8);
static void CreatePartyMonSprite(u8, bool8);
static void CreatePartyMonsSprites(bool8);
static void CompactPartySprites(void);
static u8 GetNumPartySpritesCompacting(void);
static void MovePartySpriteToNextSlot(struct Sprite *, u16);
static void SpriteCB_MovePartyMonToNextSlot(struct Sprite *);
static void MovePartySprites(s16);
static void DestroyAllPartyMonIcons(void);
static void ReshowReleaseMon(void);
static bool8 ResetReleaseMonSpritePtr(void);
static void SetMovingMonPriority(u8);
static void SpriteCB_HeldMon(struct Sprite *);
static struct Sprite *CreateMonIconSprite(enum Species species, u32 personality, s16 x, s16 y, u8 oamPriority, u8 subpriority, bool32 isEgg);
static void DestroyBoxMonIcon(struct Sprite *);

// Pokémon data
static void MoveMon(void);
static void PlaceMon(void);
static void RefreshDisplayMon(void);
static void SetMovingMonData(u8, u8);
static void SetPlacedMonData(u8, u8);
static void PurgeMonOrBoxMon(u8, u8);
static void SetShiftedMonData(u8, u8);
static bool8 TryStorePartyMonInBox(u8);
static void ResetSelectionAfterDeposit(void);
static void InitReleaseMon(void);
static bool8 TryHideReleaseMon(void);
static void InitCanReleaseMonVars(void);
static void ReleaseMon(void);
static bool32 AtLeastThreeUsableMons(void);
static s8 RunCanReleaseMon(void);
static void SaveMovingMon(void);
static void LoadSavedMovingMon(void);
static void InitSummaryScreenData(void);
static void SetSelectionAfterSummaryScreen(void);
static void SetMonMarkings(u8);
static bool8 IsRemovingLastPartyMon(void);
static bool8 CanPlaceMon(void);
static bool8 CanShiftMon(void);
static bool8 IsMonBeingMoved(void);
static void TryRefreshDisplayMon(void);
static void ReshowDisplayMon(void);
static void SetDisplayMonData(void *, u8);

// Moving multiple Pokémon at once
static void MultiMove_Free(void);
static bool8 MultiMove_Init(void);
static bool8 MultiMove_RunFunction(void);
static bool8 MultiMove_TryMoveGroup(u8);
static bool8 MultiMove_CanPlaceSelection(void);
static void MultiMove_SetFunction(u8);
static u8 MultiMove_GetOrigin(void);
static bool8 MultiMove_Start(void);
static bool8 MultiMove_Cancel(void);
static bool8 MultiMove_ChangeSelection(void);
static bool8 MultiMove_GrabSelection(void);
static bool8 MultiMove_MoveMons(void);
static bool8 MultiMove_PlaceMons(void);
static void MultiMove_SetIconToBg(u8, u8);
static void MultiMove_ClearIconFromBg(u8, u8);
static void MultiMove_ResetBg(void);
static void MultiMove_UpdateSelectedIcons(void);
static void MultiMove_InitMove(u16, u16, u16);
static void MultiMove_GetMonsFromSelection(void);
static void MultiMove_RemoveMonsFromBox(void);
static void MultiMove_CreatePlacedMonIcons(void);
static void MultiMove_SetPlacedMonData(void);
static u8 MultiMove_UpdateMove(void);
static void MultiMove_DeselectRow(u8, u8, u8);
static void MultiMove_SelectRow(u8, u8, u8);
static void MultiMove_SelectColumn(u8, u8, u8);
static void MultiMove_DeselectColumn(u8, u8, u8);

// Move Items mode
static bool32 IsItemIconAtPosition(u8, u8);
static u8 GetNewItemIconIdx(void);
static void SetItemIconPosition(u8, u8, u8);
static void LoadItemIconGfx(u8 id, const u32 *itemTiles, const u16 *itemPal);
static void SetItemIconAffineAnim(u8, u8);
static void SetItemIconActive(u8, bool8);
static u8 GetItemIconIdxByPosition(u8, u8);
static void CreateItemIconSprites(void);
static void TryLoadItemIconAtPos(u8, u8);
static void TryHideItemIconAtPos(u8, u8);
static void TakeItemFromMon(u8, u8);
static void InitItemIconInCursor(enum Item);
static void SwapItemsWithMon(u8, u8);
static void GiveItemToMon(u8, u8);
static void MoveItemFromMonToBag(u8, u8);
static void MoveItemFromCursorToBag(void);
static void MoveHeldItemWithPartyMenu(void);
static bool8 IsItemIconAnimActive(void);
static bool8 IsMovingItem(void);
static const u8 *GetMovingItemName(void);
static enum Item GetMovingItemId(void);
static void PrintItemDescription(void);
static void InitItemInfoWindow(void);
static bool8 UpdateItemInfoWindowSlideIn(void);
static bool8 UpdateItemInfoWindowSlideOut(void);
static void DrawItemInfoWindow(u32);
static void SetItemIconCallback(u8, u8, u8, u8);
static void SpriteCB_ItemIcon_SetPosToCursor(struct Sprite *);
static void SpriteCB_ItemIcon_WaitAnim(struct Sprite *);
static void SpriteCB_ItemIcon_ToHand(struct Sprite *);
static void SpriteCB_ItemIcon_ToMon(struct Sprite *);
static void SpriteCB_ItemIcon_SwapToHand(struct Sprite *);
static void SpriteCB_ItemIcon_HideParty(struct Sprite *);
static void SpriteCB_ItemIcon_SwapToMon(struct Sprite *);

// Cursor
static void CreateCursorSprites(void);
static void ToggleCursorAutoAction(void);
static u8 GetCursorPosition(void);
static void StartCursorAnim(u8);
static void TryHideItemAtCursor(void);
static void TryShowItemAtCursor(void);
static void InitCursor(void);
static void InitCursorOnReopen(void);
static void GetCursorCoordsByPos(u8, u8, u16 *, u16 *);
static bool8 UpdateCursorPos(void);
static void DoCursorNewPosUpdate(void);
static void SetCursorInParty(void);
static void SetCursorBoxPosition(u8);
static void ClearSavedCursorPos(void);
static void SaveCursorPos(void);
static u8 GetSavedCursorPos(void);
static void InitMonPlaceChange(u8);
static bool8 DoMonPlaceChange(void);
static bool8 MonPlaceChange_Shift(void);
static bool8 MonPlaceChange_Grab(void);
static bool8 MonPlaceChange_Place(void);
static bool8 MultiMonPlaceChange_Up(void);
static bool8 MultiMonPlaceChange_Down(void);
static bool8 MonPlaceChange_CursorDown(void);
static bool8 MonPlaceChange_CursorUp(void);
static void TrySetCursorFistAnim(void);
static bool8 IsCursorOnCloseBox(void);
static bool8 IsCursorOnBoxTitle(void);

// Scroll arrows
static void CreateBoxScrollArrows(void);
static void StartBoxScrollArrowsSlide(s8);
static void StopBoxScrollArrowsSlide(void);
static void AnimateBoxScrollArrows(bool8);
static void SpriteCB_Arrow(struct Sprite *);
static struct Sprite *CreateChooseBoxArrows(u16, u16, u8, u8, u8);

// Box title
static void InitBoxTitle(u8);
static void CreateIncomingBoxTitle(u8, s8);
static void CycleBoxTitleSprites(void);

// Wallpaper
static void LoadWallpaperGfx(u8, s8);
static bool32 WaitForWallpaperGfxLoad(void);
static u8 GetBoxWallpaper(u8);
static void SetBoxWallpaper(u8, u8);

// General box
static void CreateInitBoxTask(u8);
static bool8 IsInitBoxActive(void);
static void Task_InitBox(u8);
static void SetUpScrollToBox(u8);
static bool8 ScrollToBox(void);
static s8 DetermineBoxScrollDirection(u8);
static void SetCurrentBox(u8);
static struct BoxPokemon *GetCursorBoxMon(void);

// Misc
static void CreateMainMenu(u8, s16 *);
static void EnterPokeStorage(u8 boxOption);
static u8 GetCurrentBoxOption(void);
static void ScrollBackground(void);
static void UpdateCloseBoxButtonFlash(void);
static void GiveChosenBagItem(void);
static void SetUpHidePartyMenu(void);
static void LoadPokeStorageMenuGfx(void);
static void LoadWaveformSpritePalette(void);
static void InitPokeStorageBg0(void);
static void SetScrollingBackground(void);
static void UpdateBoxToSendMons(void);
static void InitCursorItemIcon(void);
static void InitPalettesAndSprites(void);
static void RefreshDisplayMonData(void);
static void CreateDisplayMonSprite(void);
static void CreateMarkingComboSprite(void);
static void CreateWaveformSprites(void);
static void ClearBottomWindow(void);
static void InitSupplementalTilemaps(void);
static void PrintDisplayMonInfo(void);
static void UpdateWaveformAnimation(void);
static void SetPartySlotTilemaps(void);
static void StopFlashingCloseBoxButton(void);
static void FreePokeStorageData(void);
static void UpdatePartySlotColors(void);
static void StartFlashingCloseBoxButton(void);
static void SetUpDoShowPartyMenu(void);
static void StartDisplayMonMosaicEffect(void);
static bool8 InitPokeStorageWindows(void);
static bool8 DoShowPartyMenu(void);
static bool8 HidePartyMenu(void);
static bool8 IsDisplayMosaicActive(void);
static void ShowYesNoWindow(s8);
static void PrintMessage(u8 id);
static void LoadDisplayMonGfx(enum Species species, u32 pid, bool32 isEgg);
static void SpriteCB_DisplayMonMosaic(struct Sprite *);

// Tilemap utility

// Form changing
void SetMonFormPSS(struct BoxPokemon *boxMon, enum FormChanges method);
void SetMonFormPSS_ItemHold(struct BoxPokemon *boxMon);
void UpdateSpeciesSpritePSS(struct BoxPokemon *boxmon);

// Orchid UI (SECTION: Misc)
static void OrchidPC_SetBoxClip(bool32 on);
static void OrchidPC_UpdateRing(void);
static void OrchidPC_ContentsChanged(void);
static void OrchidPC_ColourPickerOpen(void);
static void OrchidPC_ColourPickerMove(s8 delta);
static void OrchidPC_ColourPickerClose(void);
static void OrchidPC_DestroyHoldTags(void);
static void OrchidPC_LoadSlotPalettes(void);
static void OrchidPC_LoadBoxColour(u8 colour, u8 bgPal);
static u8 OrchidPC_GetBoxColour(u8 boxId);
static void OrchidPC_ClearBoxSlotsExcept(s32 keepCol0, bool32 keep);
static void OrchidPC_DrawBoxSlots(u32 col0, u8 bgPal);
static void OrchidPC_PartyIconPos(u8 partyId, s16 *x, s16 *y);
static bool32 OrchidPC_IsRingArea(u8 area, u8 pos);
static void OrchidPC_SetSelection(u8 area, u8 pos);
static void OrchidPC_PrintTitle(u8 boxId);

static const u8 gText_JustOnePkmn[] = _("There is just one POKéMON with you.");
static const u8 gText_PartyFull[] = _("Your party is full!");
static const u8 gText_Box[] = _("BOX");

struct {
    const u8 *text;
    const u8 *desc;
} static const sMainMenuTexts[OPTIONS_COUNT] =
{
    [OPTION_WITHDRAW]   = {COMPOUND_STRING("WITHDRAW POKéMON"), COMPOUND_STRING("Move POKéMON stored in BOXES to\nyour party.")},
    [OPTION_DEPOSIT]    = {COMPOUND_STRING("DEPOSIT POKéMON"),  COMPOUND_STRING("Store POKéMON in your party in BOXES.")},
    [OPTION_MOVE_MONS]  = {COMPOUND_STRING("MOVE POKéMON"),     COMPOUND_STRING("Organize the POKéMON in BOXES and\nin your party.")},
    [OPTION_MOVE_ITEMS] = {COMPOUND_STRING("MOVE ITEMS"),       COMPOUND_STRING("Move items held by any POKéMON\nin a BOX or your party.")},
    [OPTION_EXIT]       = {COMPOUND_STRING("SEE YA!"),          COMPOUND_STRING("Return to the previous menu.")}
};

static const struct WindowTemplate sWindowTemplate_MainMenu =
{
    .bg = 0,
    .tilemapLeft = 1,
    .tilemapTop = 1,
    .width = 17,
    .height = 10,
    .paletteNum = 15,
    .baseBlock = 0x1,
};

static const union AnimCmd sAnim_ChooseBoxMenu_TopLeft[] =
{
    ANIMCMD_FRAME(0, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_ChooseBoxMenu_BottomLeft[] =
{
    ANIMCMD_FRAME(4, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_ChooseBoxMenu_TopRight[] =
{
    ANIMCMD_FRAME(6, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_ChooseBoxMenu_BottomRight[] =
{
    ANIMCMD_FRAME(10, 5),
    ANIMCMD_END
};

static const union AnimCmd *const sAnims_ChooseBoxMenu[] =
{
    sAnim_ChooseBoxMenu_TopLeft,
    sAnim_ChooseBoxMenu_BottomLeft,
    sAnim_ChooseBoxMenu_TopRight,
    sAnim_ChooseBoxMenu_BottomRight
};

static const union AffineAnimCmd sAffineAnim_ChooseBoxMenu[] =
{
    AFFINEANIMCMD_FRAME(0xE0, 0xE0, 0, 0),
    AFFINEANIMCMD_END
};

// Unused
static const union AffineAnimCmd *const sAffineAnims_ChooseBoxMenu[] =
{
    sAffineAnim_ChooseBoxMenu
};

static const u8 sChooseBoxMenu_TextColors[] = {TEXT_COLOR_RED, TEXT_DYNAMIC_COLOR_6, TEXT_DYNAMIC_COLOR_5};
static const u8 sText_OutOf30[] = _("/30");

static const u16 sChooseBoxMenu_Pal[]        = INCGFX_U16("graphics/pokemon_storage/box_selection_popup.pal", ".gbapal");
static const u8 sChooseBoxMenuCenter_Gfx[]   = INCGFX_U8("graphics/pokemon_storage/box_selection_popup_center.png", ".4bpp");
static const u8 sChooseBoxMenuSides_Gfx[]    = INCGFX_U8("graphics/pokemon_storage/box_selection_popup_sides.png", ".4bpp");
static const u32 sScrollingBg_Gfx[]          = INCGFX_U32("graphics/pokemon_storage/scrolling_bg.png", ".4bpp.smol");
static const u32 sScrollingBg_Tilemap[]      = INCGFX_U32("graphics/pokemon_storage/scrolling_bg.bin", ".smolTM");
static const u16 sDisplayMenu_Pal[]          = INCGFX_U16("graphics/pokemon_storage/display_menu.pal", ".gbapal"); // Unused
static const u32 sDisplayMenu_Tilemap[]      = INCGFX_U32("graphics/pokemon_storage/display_menu.bin", ".smolTM");
static const u16 sPkmnData_Tilemap[]         = INCBIN_U16("graphics/pokemon_storage/pkmn_data.bin");
// sInterface_Pal - parts of the display frame, "PkmnData"'s normal color, Close Box
static const u16 sInterface_Pal[]            = INCGFX_U16("graphics/pokemon_storage/interface.pal", ".gbapal");
static const u16 sPkmnDataGray_Pal[]         = INCGFX_U16("graphics/pokemon_storage/pkmn_data_gray.pal", ".gbapal");
static const u16 sScrollingBg_Pal[]          = INCGFX_U16("graphics/pokemon_storage/scrolling_bg.pal", ".gbapal");
static const u16 sScrollingBgMoveItems_Pal[] = INCGFX_U16("graphics/pokemon_storage/scrolling_bg_move_items.pal", ".gbapal");
static const u16 sCloseBoxButton_Tilemap[]   = INCBIN_U16("graphics/pokemon_storage/close_box_button.bin");
static const u16 sPartySlotFilled_Tilemap[]  = INCBIN_U16("graphics/pokemon_storage/party_slot_filled.bin");
static const u16 sPartySlotEmpty_Tilemap[]   = INCBIN_U16("graphics/pokemon_storage/party_slot_empty.bin");
static const u16 sWaveform_Pal[]             = INCGFX_U16("graphics/pokemon_storage/waveform.png", ".gbapal");
static const u32 sWaveform_Gfx[]             = INCGFX_U32("graphics/pokemon_storage/waveform.png", ".4bpp");
static const u16 sUnused_Pal[]               = INCGFX_U16("graphics/pokemon_storage/unused.pal", ".gbapal");
static const u16 sTextWindows_Pal[]          = INCGFX_U16("graphics/pokemon_storage/text_windows.pal", ".gbapal");

// Orchid: the info / title / party slot windows are on BG1 over the screen art; their tiles start as a
// copy of the art under them (OrchidPC_FillWindowFromArt), so text and art share tiles.
static const struct WindowTemplate sWindowTemplates[] =
{
    // The info panel below the currently displayed Pokémon (name, Lv, markings, item)
    [WIN_DISPLAY_INFO] = {
        .bg = 1,
        .tilemapLeft = OPC_INFO_WIN_LEFT,
        .tilemapTop = OPC_INFO_WIN_TOP,
        .width = OPC_INFO_WIN_W,
        .height = OPC_INFO_WIN_H,
        .paletteNum = OPC_BG_UI,
        .baseBlock = OPC_BG1_WIN_BASE,
    },
    [WIN_MESSAGE] = {
        .bg = 0,
        .tilemapLeft = 11,
        .tilemapTop = 17,
        .width = 18,
        .height = 2,
        .paletteNum = OPC_BG_WINDOW,
        .baseBlock = 0x14,
    },
    [WIN_ITEM_DESC] = {
        .bg = 0,
        .tilemapLeft = 0,
        .tilemapTop = 13,
        .width = 21,
        .height = 7,
        .paletteNum = OPC_BG_TEXTWIN,
        .baseBlock = 0x14,
    },
    [WIN_TITLE] = {
        .bg = 1,
        .tilemapLeft = OPC_TITLE_WIN_LEFT,
        .tilemapTop = OPC_TITLE_WIN_TOP,
        .width = OPC_TITLE_WIN_W,
        .height = OPC_TITLE_WIN_H,
        .paletteNum = OPC_BG_TITLE,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H,
    },
    [WIN_PSLOT_0 + 0] = {
        .bg = 1,
        .tilemapLeft = 13,
        .tilemapTop = 5,
        .width = OPC_SLOT_WIN_W,
        .height = OPC_SLOT_WIN_H,
        .paletteNum = OPC_BG_SLOT,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H + OPC_TITLE_WIN_W * OPC_TITLE_WIN_H + 0 * OPC_SLOT_WIN_W * OPC_SLOT_WIN_H,
    },
    [WIN_PSLOT_0 + 1] = {
        .bg = 1,
        .tilemapLeft = 19,
        .tilemapTop = 5,
        .width = OPC_SLOT_WIN_W,
        .height = OPC_SLOT_WIN_H,
        .paletteNum = OPC_BG_SLOT,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H + OPC_TITLE_WIN_W * OPC_TITLE_WIN_H + 1 * OPC_SLOT_WIN_W * OPC_SLOT_WIN_H,
    },
    [WIN_PSLOT_0 + 2] = {
        .bg = 1,
        .tilemapLeft = 13,
        .tilemapTop = 9,
        .width = OPC_SLOT_WIN_W,
        .height = OPC_SLOT_WIN_H,
        .paletteNum = OPC_BG_SLOT,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H + OPC_TITLE_WIN_W * OPC_TITLE_WIN_H + 2 * OPC_SLOT_WIN_W * OPC_SLOT_WIN_H,
    },
    [WIN_PSLOT_0 + 3] = {
        .bg = 1,
        .tilemapLeft = 19,
        .tilemapTop = 9,
        .width = OPC_SLOT_WIN_W,
        .height = OPC_SLOT_WIN_H,
        .paletteNum = OPC_BG_SLOT,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H + OPC_TITLE_WIN_W * OPC_TITLE_WIN_H + 3 * OPC_SLOT_WIN_W * OPC_SLOT_WIN_H,
    },
    [WIN_PSLOT_0 + 4] = {
        .bg = 1,
        .tilemapLeft = 13,
        .tilemapTop = 13,
        .width = OPC_SLOT_WIN_W,
        .height = OPC_SLOT_WIN_H,
        .paletteNum = OPC_BG_SLOT,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H + OPC_TITLE_WIN_W * OPC_TITLE_WIN_H + 4 * OPC_SLOT_WIN_W * OPC_SLOT_WIN_H,
    },
    [WIN_PSLOT_0 + 5] = {
        .bg = 1,
        .tilemapLeft = 19,
        .tilemapTop = 13,
        .width = OPC_SLOT_WIN_W,
        .height = OPC_SLOT_WIN_H,
        .paletteNum = OPC_BG_SLOT,
        .baseBlock = OPC_BG1_WIN_BASE + OPC_INFO_WIN_W * OPC_INFO_WIN_H + OPC_TITLE_WIN_W * OPC_TITLE_WIN_H + 5 * OPC_SLOT_WIN_W * OPC_SLOT_WIN_H,
    },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sBgTemplates[] =
{
    {
        .bg = 0,
        .charBaseIndex = 0,
        .mapBaseIndex = 29,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 0,
        .baseTile = 0
    },
    {
        .bg = 1,
        .charBaseIndex = 2, // Orchid: BG0 popups may use charblocks 0-1 (the multi-move layer does)
        .mapBaseIndex = 30,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 1,
        .baseTile = 0
    },
    {
        .bg = 2,
        .charBaseIndex = 3, // Orchid: shares charblock 3 with BG3 (slot cell + grid, 14 tiles)
        .mapBaseIndex = 27,
        .screenSize = 1,
        .paletteMode = 0,
        .priority = 2,
        .baseTile = 0
    },
    {
        .bg = 3,
        .charBaseIndex = 3,
        .mapBaseIndex = 31,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 3,
        .baseTile = 0
    },
};

// Orchid: PALTAG_MISC_2 is the UI OBJ palette (ring, shadow, chevrons, hold tags)
static const struct SpritePalette sWaveformSpritePalette =
{
    gOrchidPcObj_Pal, PALTAG_MISC_2
};

static const struct SpriteSheet sSpriteSheet_Waveform =
{
    sWaveform_Gfx, sizeof(sWaveform_Gfx), GFXTAG_WAVEFORM
};

static const struct OamData sOamData_DisplayMon;
static const struct SpriteTemplate sSpriteTemplate_DisplayMon =
{
    .tileTag = GFXTAG_DISPLAY_MON,
    .paletteTag = PALTAG_DISPLAY_MON,
    .oam = &sOamData_DisplayMon,
};

static const u8 gText_PkmnIsSelected[] = _("{DYNAMIC 0} is selected.");

static const struct StorageMessage sMessages[] =
{
    [MSG_EXIT_BOX]             = {COMPOUND_STRING("Exit from the BOX?"),         MSG_VAR_NONE},
    [MSG_WHAT_YOU_DO]          = {COMPOUND_STRING("What do you want to do?"),    MSG_VAR_NONE},
    [MSG_PICK_A_THEME]         = {COMPOUND_STRING("Please pick a theme."),       MSG_VAR_NONE},
    [MSG_PICK_A_WALLPAPER]     = {COMPOUND_STRING("Pick the box colour."),       MSG_VAR_NONE},
    [MSG_IS_SELECTED]          = {gText_PkmnIsSelected,                          MSG_VAR_MON_NAME_1},
    [MSG_JUMP_TO_WHICH_BOX]    = {COMPOUND_STRING("Jump to which BOX?"),         MSG_VAR_NONE},
    [MSG_DEPOSIT_IN_WHICH_BOX] = {COMPOUND_STRING("Deposit in which BOX?"),      MSG_VAR_NONE},
    [MSG_WAS_DEPOSITED]        = {COMPOUND_STRING("{DYNAMIC 0} was deposited."), MSG_VAR_MON_NAME_1},
    [MSG_BOX_IS_FULL]          = {COMPOUND_STRING("The BOX is full."),           MSG_VAR_NONE},
    [MSG_RELEASE_POKE]         = {COMPOUND_STRING("Release this POKéMON?"),      MSG_VAR_NONE},
    [MSG_WAS_RELEASED]         = {COMPOUND_STRING("{DYNAMIC 0} was released."),  MSG_VAR_RELEASE_MON_1},
    [MSG_BYE_BYE]              = {COMPOUND_STRING("Bye-bye, {DYNAMIC 0}!"),      MSG_VAR_RELEASE_MON_3},
    [MSG_MARK_POKE]            = {COMPOUND_STRING("Mark your POKéMON."),         MSG_VAR_NONE},
    [MSG_LAST_POKE]            = {COMPOUND_STRING("That's your last POKéMON!"),  MSG_VAR_NONE},
    [MSG_PARTY_FULL]           = {gText_YourPartysFull,                          MSG_VAR_NONE},
    [MSG_HOLDING_POKE]         = {COMPOUND_STRING("You're holding a POKéMON!"),  MSG_VAR_NONE},
    [MSG_WHICH_ONE_WILL_TAKE]  = {COMPOUND_STRING("Which one will you take?"),   MSG_VAR_NONE},
    [MSG_CANT_RELEASE_EGG]     = {COMPOUND_STRING("You can't release an EGG."),  MSG_VAR_NONE},
    [MSG_CONTINUE_BOX]         = {COMPOUND_STRING("Continue BOX operations?"),   MSG_VAR_NONE},
    [MSG_CAME_BACK]            = {COMPOUND_STRING("{DYNAMIC 0} came back!"),     MSG_VAR_MON_NAME_1},
    [MSG_WORRIED]              = {COMPOUND_STRING("Was it worried about you?"),  MSG_VAR_NONE},
    [MSG_SURPRISE]             = {COMPOUND_STRING("… … … … !"),                  MSG_VAR_NONE},
    [MSG_PLEASE_REMOVE_MAIL]   = {COMPOUND_STRING("Please remove the MAIL."),    MSG_VAR_NONE},
    [MSG_IS_SELECTED2]         = {gText_PkmnIsSelected,                          MSG_VAR_ITEM_NAME},
    [MSG_GIVE_TO_MON]          = {COMPOUND_STRING("GIVE to a POKéMON?"),         MSG_VAR_NONE},
    [MSG_PLACED_IN_BAG]        = {COMPOUND_STRING("Placed item in the BAG."),    MSG_VAR_ITEM_NAME},
    [MSG_BAG_FULL]             = {COMPOUND_STRING("The BAG is full."),           MSG_VAR_NONE},
    [MSG_PUT_IN_BAG]           = {COMPOUND_STRING("Put this item in the BAG?"),  MSG_VAR_NONE},
    [MSG_ITEM_IS_HELD]         = {COMPOUND_STRING("{DYNAMIC 0} is now held."),   MSG_VAR_ITEM_NAME},
    [MSG_CHANGED_TO_ITEM]      = {COMPOUND_STRING("Changed to {DYNAMIC 0}."),    MSG_VAR_ITEM_NAME},
    [MSG_CANT_STORE_MAIL]      = {COMPOUND_STRING("MAIL can't be stored!"),      MSG_VAR_NONE},
};

static const struct WindowTemplate sYesNoWindowTemplate =
{
    .bg = 0,
    .tilemapLeft = 24,
    .tilemapTop = 11,
    .width = 5,
    .height = 4,
    .paletteNum = OPC_BG_WINDOW,
    .baseBlock = 0x5C,
};

static const struct OamData sOamData_DisplayMon =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(64x64),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(64x64),
    .tileNum = 0,
    .priority = 1, // Orchid: under the BG0 popups
    .paletteNum = 0,
    .affineParam = 0
};

static const struct OamData sOamData_Waveform =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(16x8),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(16x8),
    .tileNum = 0,
    .priority = 0,
    .paletteNum = 0,
    .affineParam = 0
};

static const union AnimCmd sAnim_Waveform_LeftOff[] =
{
    ANIMCMD_FRAME(0, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_Waveform_LeftOn[] =
{
    ANIMCMD_FRAME(2, 8),
    ANIMCMD_FRAME(4, 8),
    ANIMCMD_FRAME(6, 8),
    ANIMCMD_JUMP(0)
};

static const union AnimCmd sAnim_Waveform_RightOff[] =
{
    ANIMCMD_FRAME(8, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_Waveform_RightOn[] =
{
    ANIMCMD_FRAME(10, 8),
    ANIMCMD_FRAME(4, 8),
    ANIMCMD_FRAME(12, 8),
    ANIMCMD_JUMP(0)
};

static const union AnimCmd *const sAnims_Waveform[] =
{
    sAnim_Waveform_LeftOff,
    sAnim_Waveform_LeftOn,
    sAnim_Waveform_RightOff,
    sAnim_Waveform_RightOn
};

static const struct SpriteTemplate sSpriteTemplate_Waveform =
{
    .tileTag = GFXTAG_WAVEFORM,
    .paletteTag = PALTAG_MISC_2,
    .oam = &sOamData_Waveform,
    .anims = sAnims_Waveform,
};

static const struct OamData sOamData_MonIcon;
static const struct SpriteTemplate sSpriteTemplate_MonIcon =
{
    .tileTag = GFXTAG_MON_ICON,
    .paletteTag = PALTAG_MON_ICON_0,
    .oam = &sOamData_MonIcon,
};

static const struct OamData sOamData_MonIcon =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(32x32),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(32x32),
    .tileNum = 0,
    .priority = 0,
    .paletteNum = 0,
    .affineParam = 0
};

static const union AffineAnimCmd sAffineAnim_ReleaseMon_Release[] =
{
    AFFINEANIMCMD_FRAME(-2, -2, 0, 120),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ReleaseMon_CameBack[] =
{
    AFFINEANIMCMD_FRAME(16, 16, 0, 0),
    AFFINEANIMCMD_FRAME(16, 16, 0, 15),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd *const sAffineAnims_ReleaseMon[] =
{
    [RELEASE_ANIM_RELEASE]   = sAffineAnim_ReleaseMon_Release,
    [RELEASE_ANIM_CAME_BACK] = sAffineAnim_ReleaseMon_CameBack
};

#include "data/wallpapers.h"

static const u16 sUnusedColor = RGB(26, 29, 8);

// Orchid: small red Gen 3 chevrons (8x16: normal, lit), from ui_obj.png
static const struct SpriteSheet sSpriteSheet_Arrow = {gOrchidPcObj_Gfx + OPC_OBJ_CHEVRON * TILE_SIZE_4BPP, 4 * TILE_SIZE_4BPP, GFXTAG_ARROW};

static const struct OamData sOamData_BoxTitle =
{
    .shape = SPRITE_SHAPE(32x16),
    .size = SPRITE_SIZE(32x16),
    .priority = 2
};

static const union AnimCmd sAnim_BoxTitle_Left[] =
{
    ANIMCMD_FRAME(0, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_BoxTitle_Right[] =
{
    ANIMCMD_FRAME(8, 5),
    ANIMCMD_END
};

static const union AnimCmd *const sAnims_BoxTitle[] =
{
    sAnim_BoxTitle_Left,
    sAnim_BoxTitle_Right
};

static const struct SpriteTemplate sSpriteTemplate_BoxTitle =
{
    .tileTag = GFXTAG_BOX_TITLE,
    .paletteTag = PALTAG_BOX_TITLE,
    .oam = &sOamData_BoxTitle,
    .anims = sAnims_BoxTitle,
};

static const struct OamData sOamData_Arrow =
{
    .shape = SPRITE_SHAPE(8x16),
    .size = SPRITE_SIZE(8x16),
    .priority = 2
};

static const union AnimCmd sAnim_Arrow_Left[] =
{
    ANIMCMD_FRAME(0, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_Arrow_Right[] =
{
    ANIMCMD_FRAME(0, 5, .hFlip = TRUE),
    ANIMCMD_END
};

static const union AnimCmd sAnim_Arrow_LeftLit[] =
{
    ANIMCMD_FRAME(2, 5),
    ANIMCMD_END
};

static const union AnimCmd sAnim_Arrow_RightLit[] =
{
    ANIMCMD_FRAME(2, 5, .hFlip = TRUE),
    ANIMCMD_END
};

// 0 left, 1 right, 2 left lit, 3 right lit
static const union AnimCmd *const sAnims_Arrow[] =
{
    sAnim_Arrow_Left,
    sAnim_Arrow_Right,
    sAnim_Arrow_LeftLit,
    sAnim_Arrow_RightLit,
};

static const struct SpriteTemplate sSpriteTemplate_Arrow =
{
    .tileTag = GFXTAG_ARROW,
    .paletteTag = PALTAG_MISC_2,
    .oam = &sOamData_Arrow,
    .anims = sAnims_Arrow,
    .callback = SpriteCB_Arrow
};

static const u16 sHandCursor_Pal[] = INCGFX_U16("graphics/pokemon_storage/hand_cursor.png", ".gbapal");
static const u8 sHandCursor_Gfx[] = INCGFX_U8("graphics/pokemon_storage/hand_cursor.png", ".4bpp");
static const u8 sHandCursorShadow_Gfx[] = INCGFX_U8("graphics/pokemon_storage/hand_cursor_shadow.png", ".4bpp");


//------------------------------------------------------------------------------
//  SECTION: Misc utility
//------------------------------------------------------------------------------


void DrawTextWindowAndBufferTiles(const u8 *string, void *dst, u8 zero1, u8 zero2, s32 bytesToBuffer)
{
    s32 i, tileBytesToBuffer, remainingBytes;
    u16 windowId;
    u8 txtColor[3];
    u8 *tileData1, *tileData2;
    struct WindowTemplate winTemplate = {0};

    winTemplate.width = 24;
    winTemplate.height = 2;
    windowId = AddWindow(&winTemplate);
    FillWindowPixelBuffer(windowId, PIXEL_FILL(zero2));
    tileData1 = (u8 *) GetWindowAttribute(windowId, WINDOW_TILE_DATA);
    tileData2 = (winTemplate.width * TILE_SIZE_4BPP) + tileData1;

    if (!zero1)
        txtColor[0] = TEXT_COLOR_TRANSPARENT;
    else
        txtColor[0] = zero2;
    txtColor[1] = TEXT_DYNAMIC_COLOR_6;
    txtColor[2] = TEXT_DYNAMIC_COLOR_5;
    AddTextPrinterParameterized4(windowId, FONT_NORMAL, 0, 1, 0, 0, txtColor, TEXT_SKIP_DRAW, string);

    tileBytesToBuffer = bytesToBuffer;
    if (tileBytesToBuffer > 6u)
        tileBytesToBuffer = 6;
    remainingBytes = bytesToBuffer - 6;
    if (tileBytesToBuffer > 0)
    {
        for (i = tileBytesToBuffer; i != 0; i--)
        {
            CpuCopy16(tileData1, dst, 0x80);
            CpuCopy16(tileData2, dst + 0x80, 0x80);
            tileData1 += 0x80;
            tileData2 += 0x80;
            dst += 0x100;
        }
    }

    // Never used. bytesToBuffer is always passed <= 6, so remainingBytes is always <= 0 here
    if (remainingBytes > 0)
        CpuFill16((zero2 << 4) | zero2, dst, (u32)(remainingBytes) * 0x100);

    RemoveWindow(windowId);
}

static void UNUSED UnusedDrawTextWindow(const u8 *string, void *dst, u16 offset, u8 bgColor, u8 fgColor, u8 shadowColor)
{
    u32 tilesSize;
    u8 windowId;
    u8 txtColor[3];
    u8 *tileData1, *tileData2;
    struct WindowTemplate winTemplate = {0};

    winTemplate.width = StringLength_Multibyte(string);
    winTemplate.height = 2;
    tilesSize = winTemplate.width * TILE_SIZE_4BPP;
    windowId = AddWindow(&winTemplate);
    FillWindowPixelBuffer(windowId, PIXEL_FILL(bgColor));
    tileData1 = (u8 *) GetWindowAttribute(windowId, WINDOW_TILE_DATA);
    tileData2 = (winTemplate.width * TILE_SIZE_4BPP) + tileData1;
    txtColor[0] = bgColor;
    txtColor[1] = fgColor;
    txtColor[2] = shadowColor;
    AddTextPrinterParameterized4(windowId, FONT_NORMAL, 0, 2, 0, 0, txtColor, TEXT_SKIP_DRAW, string);
    CpuCopy16(tileData1, dst, tilesSize);
    CpuCopy16(tileData2, dst + offset, tilesSize);
    RemoveWindow(windowId);
}

u8 CountMonsInBox(u8 boxId)
{
    u16 i, count;

    for (i = 0, count = 0; i < IN_BOX_COUNT; i++)
    {
        if (GetBoxMonDataAt(boxId, i, MON_DATA_SPECIES) != SPECIES_NONE)
            count++;
    }

    return count;
}

s16 GetFirstFreeBoxSpot(u8 boxId)
{
    u16 i;

    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        if (GetBoxMonDataAt(boxId, i, MON_DATA_SPECIES) == SPECIES_NONE)
            return i;
    }

    return -1; // all spots are taken
}

u32 CountPartyNonEggMons(void)
{
    u32 i, count;

    for (i = 0, count = 0; i < PARTY_SIZE; i++)
    {
        if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) != SPECIES_NONE
            && !GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_IS_EGG))
        {
            count++;
        }
    }

    return count;
}

u8 CountPartyAliveNonEggMonsExcept(u8 slotToIgnore)
{
    u16 i, count;

    for (i = 0, count = 0; i < PARTY_SIZE; i++)
    {
        if (i != slotToIgnore
            && GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) != SPECIES_NONE
            && !GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_IS_EGG)
            && GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_HP) != 0)
        {
            count++;
        }
    }

    return count;
}

u16 CountPartyAliveNonEggMons_IgnoreVar0x8004Slot(void)
{
    return CountPartyAliveNonEggMonsExcept(gSpecialVar_0x8004);
}

u8 CountPartyMons(void)
{
    u16 i, count;

    for (i = 0, count = 0; i < PARTY_SIZE; i++)
    {
        if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) != SPECIES_NONE)
        {
            count++;
        }
    }

    return count;
}

u8 *StringCopyAndFillWithSpaces(u8 *dst, const u8 *src, u16 n)
{
    u8 *str;

    for (str = StringCopy(dst, src); str < dst + n; str++)
        *str = CHAR_SPACE;

    *str = EOS;
    return str;
}

static void UNUSED UnusedWriteRectCpu(u16 *dest, u16 dest_left, u16 dest_top, const u16 *src, u16 src_left, u16 src_top, u16 dest_width, u16 dest_height, u16 src_width)
{
    u16 i;

    dest_width *= 2;
    dest += dest_top * 0x20 + dest_left;
    src += src_top * src_width + src_left;
    for (i = 0; i < dest_height; i++)
    {
        CpuCopy16(src, dest, dest_width);
        dest += 0x20;
        src += src_width;
    }
}

static void UNUSED UnusedWriteRectDma(u16 *dest, u16 dest_left, u16 dest_top, u16 width, u16 height)
{
    u16 i;

    dest += dest_top * 0x20 + dest_left;
    width *= 2;
    for (i = 0; i < height; dest += 0x20, i++)
        Dma3FillLarge16_(0, dest, width);
}


//------------------------------------------------------------------------------
//  SECTION: Main menu
//
//  The below functions generally handle the PC main menu where the main
//  options can be selected (Withdraw, Deposit, etc.), as well as exiting
//  Pokémon Storage back to this menu.
//------------------------------------------------------------------------------


enum {
    STATE_LOAD,
    STATE_FADE_IN,
    STATE_HANDLE_INPUT,
    STATE_ERROR_MSG,
    STATE_ENTER_PC,
};

#define tState          data[0]
#define tSelectedOption data[1]
#define tInput          data[2]
#define tNextOption     data[3]
#define tWindowId       data[15]

static void Task_PCMainMenu(u8 taskId)
{
    struct Task *task = &gTasks[taskId];

    switch (task->tState)
    {
    case STATE_LOAD:
        CreateMainMenu(task->tSelectedOption, &task->tWindowId);
        LoadMessageBoxAndBorderGfx();
        DrawDialogueFrame(0, FALSE);
        FillWindowPixelBuffer(0, PIXEL_FILL(1));
        AddTextPrinterParameterized2(0, FONT_NORMAL, sMainMenuTexts[task->tSelectedOption].desc, TEXT_SKIP_DRAW, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
        CopyWindowToVram(0, COPYWIN_FULL);
        CopyWindowToVram(task->tWindowId, COPYWIN_FULL);
        task->tState++;
        break;
    case STATE_FADE_IN:
        if (IsWeatherNotFadingIn())
            task->tState++;
        break;
    case STATE_HANDLE_INPUT:
        task->tInput = Menu_ProcessInput();
        switch (task->tInput)
        {
        case MENU_NOTHING_CHOSEN:
            task->tNextOption = task->tSelectedOption;
            if (JOY_NEW(DPAD_UP) && --task->tNextOption < 0)
                task->tNextOption = OPTIONS_COUNT - 1;
            if (JOY_NEW(DPAD_DOWN) && ++task->tNextOption > OPTIONS_COUNT - 1)
                task->tNextOption = 0;

            if (task->tSelectedOption != task->tNextOption)
            {
                task->tSelectedOption = task->tNextOption;
                FillWindowPixelBuffer(0, PIXEL_FILL(1));
                AddTextPrinterParameterized2(0, FONT_NORMAL, sMainMenuTexts[task->tSelectedOption].desc, 0, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
            }
            break;
        case MENU_B_PRESSED:
        case OPTION_EXIT:
            ClearStdWindowAndFrame(task->tWindowId, TRUE);
            UnlockPlayerFieldControls();
            ScriptContext_Enable();
            RemoveWindow(task->tWindowId);
            DestroyTask(taskId);
            break;
        default:
            if (task->tInput == OPTION_WITHDRAW && CountPartyMons() == PARTY_SIZE)
            {
                // Can't withdraw
                FillWindowPixelBuffer(0, PIXEL_FILL(1));
                AddTextPrinterParameterized2(0, FONT_NORMAL, gText_PartyFull, 0, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
                task->tState = STATE_ERROR_MSG;
            }
            else if (task->tInput == OPTION_DEPOSIT && CountPartyMons() == 1)
            {
                // Can't deposit
                FillWindowPixelBuffer(0, PIXEL_FILL(1));
                AddTextPrinterParameterized2(0, FONT_NORMAL, gText_JustOnePkmn, 0, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
                task->tState = STATE_ERROR_MSG;
            }
            else
            {
                // Enter PC
                FadeScreen(FADE_TO_BLACK, 0);
                task->tState = STATE_ENTER_PC;
            }
            break;
        }
        break;
    case STATE_ERROR_MSG:
        // Printed "can't do PC option message"
        // Wait for new input after message
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            FillWindowPixelBuffer(0, PIXEL_FILL(1));
            AddTextPrinterParameterized2(0, FONT_NORMAL, sMainMenuTexts[task->tSelectedOption].desc, 0, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
            task->tState = STATE_HANDLE_INPUT;
        }
        else if (JOY_NEW(DPAD_UP))
        {
            if (--task->tSelectedOption < 0)
                task->tSelectedOption = OPTIONS_COUNT - 1;
            Menu_MoveCursor(-1);
            task->tSelectedOption = Menu_GetCursorPos();
            FillWindowPixelBuffer(0, PIXEL_FILL(1));
            AddTextPrinterParameterized2(0, FONT_NORMAL, sMainMenuTexts[task->tSelectedOption].desc, 0, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
            task->tState = STATE_HANDLE_INPUT;
        }
        else if (JOY_NEW(DPAD_DOWN))
        {
            if (++task->tSelectedOption >= OPTIONS_COUNT - 1)
                task->tSelectedOption = 0;
            Menu_MoveCursor(1);
            task->tSelectedOption = Menu_GetCursorPos();
            FillWindowPixelBuffer(0, PIXEL_FILL(1));
            AddTextPrinterParameterized2(0, FONT_NORMAL, sMainMenuTexts[task->tSelectedOption].desc, 0, NULL, TEXT_COLOR_DARK_GRAY, TEXT_COLOR_WHITE, TEXT_COLOR_LIGHT_GRAY);
            task->tState = STATE_HANDLE_INPUT;
        }
        break;
    case STATE_ENTER_PC:
        if (!gPaletteFade.active)
        {
            CleanupOverworldWindowsAndTilemaps();
            EnterPokeStorage(task->tInput);
            RemoveWindow(task->tWindowId);
            DestroyTask(taskId);
        }
        break;
    }
}

void ShowPokemonStorageSystemPC(void)
{
    u8 taskId = CreateTask(Task_PCMainMenu, 80);
    gTasks[taskId].tState = 0;
    gTasks[taskId].tSelectedOption = 0;
    LockPlayerFieldControls();
}

static void FieldTask_ReturnToPcMenu(void)
{
    u8 taskId;
    MainCallback vblankCb = gMain.vblankCallback;

    SetVBlankCallback(NULL);
    taskId = CreateTask(Task_PCMainMenu, 80);
    gTasks[taskId].tState = 0;
    gTasks[taskId].tSelectedOption = sPreviousBoxOption;
    Task_PCMainMenu(taskId);
    SetVBlankCallback(vblankCb);
    FadeInFromBlack();
}

#undef tState
#undef tSelectedOption
#undef tInput
#undef tNextOption
#undef tWindowId

// Orchid (mock_pc.render_field_menu): the vanilla window at tile (1, 1) in the Orchid frame, sized to the
// longest option, a gold pill on the selected row. Frame + window palette in the field's free slots
// (ORCHID_YESNO_FIELD_TILE / _PAL, as the field YES/NO).
static void CreateMainMenu(u8 whichMenu, s16 *windowIdPtr)
{
    s16 windowId;
    struct WindowTemplate template = sWindowTemplate_MainMenu;
    template.width = GetOrchidPillMenuWidth((void *)sMainMenuTexts, OPTIONS_COUNT);
    template.paletteNum = ORCHID_YESNO_FIELD_PAL;
    windowId = AddWindow(&template);

    LoadOrchidYesNoFrame(template.bg, ORCHID_YESNO_FIELD_TILE);
    LoadOrchidYesNoColors(ORCHID_YESNO_FIELD_PAL, TRUE);
    DrawStdFrameWithCustomTileAndPalette(windowId, FALSE, ORCHID_YESNO_FIELD_TILE, ORCHID_YESNO_FIELD_PAL);
    InitOrchidPillMenu(windowId, OPTIONS_COUNT, (void *)sMainMenuTexts, whichMenu);
    *windowIdPtr = windowId;
}

static void CB2_ExitPokeStorage(void)
{
    sPreviousBoxOption = GetCurrentBoxOption();
    gFieldCallback = FieldTask_ReturnToPcMenu;
    SetMainCallback2(CB2_ReturnToField);
}

static s16 UNUSED StorageSystemGetNextMonIndex(struct BoxPokemon *box, s8 startIdx, u8 stopIdx, u8 mode)
{
    s16 i;
    s16 direction;
    if (mode == 0 || mode == 1)
    {
        direction = 1;
    }
    else
    {
        direction = -1;
    }
    if (mode == 1 || mode == 3)
    {
        for (i = startIdx + direction; i >= 0 && i <= stopIdx; i += direction)
        {
            if (GetBoxMonData(box + i, MON_DATA_SPECIES) != 0)
                return i;
        }
    }
    else
    {
        for (i = startIdx + direction; i >= 0 && i <= stopIdx; i += direction)
        {
            if (GetBoxMonData(box + i, MON_DATA_SPECIES) != 0 && !GetBoxMonData(box + i, MON_DATA_IS_EGG))
                return i;
        }
    }
    return -1;
}

void ResetPokemonStorageSystem(void)
{
    u16 boxId, boxPosition;

    SetCurrentBox(0);
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        for (boxPosition = 0; boxPosition < IN_BOX_COUNT; boxPosition++)
            ZeroBoxMonAt(boxId, boxPosition);
    }
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
    {
        u8 *dest = StringCopy(GetBoxNamePtr(boxId), gText_Box);
        ConvertIntToDecimalStringN(dest, boxId + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
    }

    // Orchid: the wallpaper byte holds the box colour (0 = Orchid purple)
    for (boxId = 0; boxId < TOTAL_BOXES_COUNT; boxId++)
        SetBoxWallpaper(boxId, 0);

    ResetWaldaWallpaper();
}


//------------------------------------------------------------------------------
//  SECTION: Choose Box menu
//
//  The below functions handle the popup menu that allows the player to cycle
//  through the boxes and select one. Used when storing Pokémon in Deposit mode
//  and for the Jump feature.
//------------------------------------------------------------------------------


// Orchid: the jump / deposit popup is a BG0 window over the box (mock_pc.jump_popup): the box name on an
// accent pill between red chevrons, a 6x5 occupancy map of the box and its count.
static void LightChevron(struct Sprite *sprite);

static void LoadChooseBoxMenuGfx(struct ChooseBoxMenu *menu, u16 tileTag, u16 palTag, u8 subpriority, bool32 loadPal)
{
    sChooseBoxMenu = menu;
    menu->tileTag = tileTag;
    menu->paletteTag = palTag;
    menu->subpriority = subpriority;
    menu->loadedPalette = FALSE;
}

static void FreeChooseBoxMenu(void)
{
}

static void CreateChooseBoxMenuSprites(u8 curBox)
{
    ChooseBoxMenu_CreateSprites(curBox);
}

static void DestroyChooseBoxMenuSprites(void)
{
    ChooseBoxMenu_DestroySprites();
}

// For the popout window when choosing a box to deposit in or jump to
static u8 HandleChooseBoxMenuInput(void)
{
    if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        return BOXID_CANCELED;
    }
    if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        return sChooseBoxMenu->curBox;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        PlaySE(SE_SELECT);
        LightChevron(sChooseBoxMenu->arrowSprites[0]);
        ChooseBoxMenu_MoveLeft();
    }
    else if (JOY_NEW(DPAD_RIGHT))
    {
        PlaySE(SE_SELECT);
        LightChevron(sChooseBoxMenu->arrowSprites[1]);
        ChooseBoxMenu_MoveRight();
    }
    return BOXID_NONE_CHOSEN;
}

static void ChooseBoxMenu_CreateSprites(u8 curBox)
{
    static const struct WindowTemplate sTemplate = {
        .bg = 0,
        .tilemapLeft = OPC_JUMP_WIN_LEFT,
        .tilemapTop = OPC_JUMP_WIN_TOP,
        .width = OPC_JUMP_WIN_W,
        .height = OPC_JUMP_WIN_H,
        .paletteNum = OPC_BG_UI,
        .baseBlock = 0xD0,
    };
    u16 i;

    sChooseBoxMenu->curBox = curBox;
    sChooseBoxMenu->menuSprite = NULL;
    for (i = 0; i < ARRAY_COUNT(sChooseBoxMenu->menuSideSprites); i++)
        sChooseBoxMenu->menuSideSprites[i] = NULL;
    sChooseBoxMenu->windowId = AddWindow(&sTemplate);
    DrawStdFrameWithCustomTileAndPalette(sChooseBoxMenu->windowId, FALSE, OPC_FRAME_TILE, OPC_BG_WINDOW);
    PutWindowTilemap(sChooseBoxMenu->windowId);
    for (i = 0; i < ARRAY_COUNT(sChooseBoxMenu->arrowSprites); i++)
        sChooseBoxMenu->arrowSprites[i] = CreateChooseBoxArrows(i == 0 ? OPC_JUMP_CHEV_L_X : OPC_JUMP_CHEV_R_X, OPC_JUMP_CHEV_Y, i, 0, sChooseBoxMenu->subpriority);
    ChooseBoxMenu_PrintInfo();
}

static void ChooseBoxMenu_DestroySprites(void)
{
    u16 i;

    ClearStdWindowAndFrameToTransparent(sChooseBoxMenu->windowId, FALSE);
    RemoveWindow(sChooseBoxMenu->windowId);
    ScheduleBgCopyTilemapToVram(0);
    for (i = 0; i < ARRAY_COUNT(sChooseBoxMenu->arrowSprites); i++)
    {
        if (sChooseBoxMenu->arrowSprites[i])
        {
            DestroySprite(sChooseBoxMenu->arrowSprites[i]);
            sChooseBoxMenu->arrowSprites[i] = NULL;
        }
    }
}

static void ChooseBoxMenu_MoveRight(void)
{
    if (++sChooseBoxMenu->curBox >= TOTAL_BOXES_COUNT)
        sChooseBoxMenu->curBox = 0;
    ChooseBoxMenu_PrintInfo();
}

static void ChooseBoxMenu_MoveLeft(void)
{
    sChooseBoxMenu->curBox = (sChooseBoxMenu->curBox == 0 ? TOTAL_BOXES_COUNT - 1 : sChooseBoxMenu->curBox - 1);
    ChooseBoxMenu_PrintInfo();
}

static void ChooseBoxMenu_PrintInfo(void)
{
    static const u8 sNameColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_WHITE, OPC_ROLE_ACCENT_DARK};
    static const u8 sCountColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_INK, OPC_ROLE_PANEL_SHADE};
    u8 windowId = sChooseBoxMenu->windowId;
    u8 boxId = sChooseBoxMenu->curBox;
    const u8 *boxName = GetBoxNamePtr(boxId);
    u8 text[16], *ptr;
    s32 width = OPC_JUMP_WIN_W * 8;
    s32 countX = 6 + 42 + 6;
    s32 w;
    u32 i;

    FillWindowPixelBuffer(windowId, PIXEL_FILL(OPC_ROLE_WHITE));
    OrchidDrawRoundedBox(windowId, 16, 1, width - 32, 14, 4, OPC_ROLE_ACCENT, OPC_ROLE_INK, OPC_ROLE_ACCENT_LIGHT, OPC_ROLE_ACCENT_DARK);
    w = GetStringWidth(FONT_NORMAL, boxName, 0);
    AddTextPrinterParameterized4(windowId, FONT_NORMAL, width / 2 - w / 2, 0, 0, 0, sNameColors, TEXT_SKIP_DRAW, boxName);

    // 6x5 occupancy map (pc_ext.box_minimap): accent dot = occupied, recess = empty
    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        s32 x = 6 + 7 * (i % IN_BOX_COLUMNS), y = 22 + 7 * (i / IN_BOX_COLUMNS);
        if (GetBoxMonDataAt(boxId, i, MON_DATA_SPECIES) != SPECIES_NONE)
            OrchidDrawRoundedBox(windowId, x, y, 6, 6, 1, OPC_ROLE_ACCENT, OPC_ROLE_INK, OPC_ROLE_ACCENT_LIGHT, OPC_ROLE_ACCENT_DARK);
        else
            OrchidDrawRoundedBox(windowId, x, y, 6, 6, 1, OPC_ROLE_PANEL_DARK, OPC_ROLE_PANEL_SHADE, OPC_ROLE_PANEL_DARK, OPC_ROLE_PANEL_DARK);
    }

    OrchidDrawRoundedBox(windowId, countX, 31, width - countX - 2, 14, 4, OPC_ROLE_PANEL, OPC_ROLE_INK, OPC_ROLE_WHITE, OPC_ROLE_PANEL_SHADE);
    ptr = ConvertIntToDecimalStringN(text, CountMonsInBox(boxId), STR_CONV_MODE_LEFT_ALIGN, 2);
    StringCopy(ptr, sText_OutOf30);
    w = GetStringWidth(FONT_SMALL, text, 0);
    AddTextPrinterParameterized4(windowId, FONT_SMALL, countX + (width - countX - 2 - w) / 2 + 1, 32, 0, 0, sCountColors, TEXT_SKIP_DRAW, text);
    CopyWindowToVram(windowId, COPYWIN_FULL);
    ScheduleBgCopyTilemapToVram(0);
}


//------------------------------------------------------------------------------
//  SECTION: Main tasks
//
//  Below are the main task callbacks that handle the primary actions the
//  player can take in the PC. The most 'important' of these tasks is the
//  primary one, Task_PokeStorageMain. Also included are some basic
//  initialization functions.
//------------------------------------------------------------------------------


static void VBlankCB_PokeStorage(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
    if (sStorage != NULL)
    {
        SetGpuReg(REG_OFFSET_BG2HOFS, sStorage->bg2_X);
    }
}

static void CB2_PokeStorage(void)
{
    RunTasks();
    DoScheduledBgTilemapCopiesToVram();
    ScrollBackground();
    UpdateCloseBoxButtonFlash();
    AnimateSprites();
    BuildOamBuffer();
}

static void EnterPokeStorage(u8 boxOption)
{
    ResetTasks();
    sCurrentBoxOption = boxOption;
    sStorage = Alloc(sizeof(*sStorage));
    if (sStorage == NULL)
    {
        if (boxOption == OPTION_SELECT_MON)
            SetMainCallback2(CB2_ReturnToFieldContinueScript);
        else
            SetMainCallback2(CB2_ExitPokeStorage);
    }
    else
    {
        sStorage->boxOption = boxOption;
        sStorage->isReopening = FALSE;
        sMovingItemId = ITEM_NONE;
        sStorage->state = 0;
        sStorage->taskId = CreateTask(Task_InitPokeStorage, 3);
        sLastUsedBox = StorageGetCurrentBox();
        SetMainCallback2(CB2_PokeStorage);
    }
}

static void CB2_ReturnToPokeStorage(void)
{
    ResetTasks();
    sStorage = Alloc(sizeof(*sStorage));
    if (sStorage == NULL)
    {
        if (sStorage->boxOption == OPTION_SELECT_MON)
            SetMainCallback2(CB2_ReturnToFieldContinueScript);
        else
            SetMainCallback2(CB2_ExitPokeStorage);
    }
    else
    {
        sStorage->boxOption = sCurrentBoxOption;
        sStorage->isReopening = TRUE;
        sStorage->state = 0;
        sStorage->taskId = CreateTask(Task_InitPokeStorage, 3);
        SetMainCallback2(CB2_PokeStorage);
    }
}

static void ResetAllBgCoords(void)
{
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 0);
    SetGpuReg(REG_OFFSET_BG2HOFS, 0);
    SetGpuReg(REG_OFFSET_BG2VOFS, 0);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
}

static void ResetForPokeStorage(void)
{
    ResetPaletteFade();
    ResetSpriteData();
    FreeSpriteTileRanges();
    FreeAllSpritePalettes();
    ClearDma3Requests();
    gReservedSpriteTileCount = 0x280;
    gKeyRepeatStartDelay = 20;
    ClearScheduledBgCopiesToVram();
    sStorage->closeBoxFlashing = FALSE;
}

static void InitStartingPosData(void)
{
    ClearSavedCursorPos();
    sInPartyMenu = (sStorage->boxOption == OPTION_DEPOSIT);
    sDepositBoxId = 0;
}

static void SetMonIconTransparency(void)
{
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT2_ALL);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(8, 8)); // Orchid: half-bright, like mock_pc._dim
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_BG_ALL_ON | DISPCNT_OBJ_1D_MAP);
}

static void SetPokeStorageTask(TaskFunc newFunc)
{
    gTasks[sStorage->taskId].func = newFunc;
    sStorage->state = 0;
}

static void Task_InitPokeStorage(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        SetVBlankCallback(NULL);
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        ResetForPokeStorage();
        if (sStorage->isReopening)
        {
            switch (sWhichToReshow)
            {
            case SCREEN_CHANGE_NAME_BOX - 1:
                // Return from naming box
                LoadSavedMovingMon();
                break;
            case SCREEN_CHANGE_SUMMARY_SCREEN - 1:
                // Return from summary screen
                SetSelectionAfterSummaryScreen();
                break;
            case SCREEN_CHANGE_ITEM_FROM_BAG - 1:
                // Return from bag menu
                GiveChosenBagItem();
                break;
            }
        }
        LoadPokeStorageMenuGfx();
        LoadWaveformSpritePalette();
        break;
    case 1:
        if (!InitPokeStorageWindows())
        {
            SetPokeStorageTask(Task_ChangeScreen);
            return;
        }
        break;
    case 2:
        ClearWindowTilemap(WIN_MESSAGE);
        CpuFill32(0, (void *)VRAM, 0x200);
        break;
    case 3:
        ResetAllBgCoords();
        if (!sStorage->isReopening)
            InitStartingPosData();
        break;
    case 4:
        InitMonIconFields();
        if (!sStorage->isReopening)
            InitCursor();
        else
            InitCursorOnReopen();
        break;
    case 5:
        if (!MultiMove_Init())
        {
            SetPokeStorageTask(Task_ChangeScreen);
            return;
        }
        else
        {
            SetScrollingBackground();
            InitPokeStorageBg0();
        }
        break;
    case 6:
        InitPalettesAndSprites();
        break;
    case 7:
        InitSupplementalTilemaps();
        break;
    case 8:
        CreateInitBoxTask(StorageGetCurrentBox());
        break;
    case 9:
        if (IsInitBoxActive())
            return;

        if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        {
            sStorage->markMenu.baseTileTag = GFXTAG_MARKING_MENU;
            sStorage->markMenu.basePaletteTag = PALTAG_MARKING_MENU;
            InitMonMarkingsMenu(&sStorage->markMenu);
            BufferMonMarkingsMenuTiles();
        }
        else
        {
            CreateItemIconSprites();
            InitCursorItemIcon();
        }
        break;
    case 10:
        SetMonIconTransparency();
        if (!sStorage->isReopening)
        {
            BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
            SetPokeStorageTask(Task_ShowPokeStorage);
        }
        else
        {
            BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
            SetPokeStorageTask(Task_ReshowPokeStorage);
        }
        SetVBlankCallback(VBlankCB_PokeStorage);
        return;
    default:
        return;
    }

    sStorage->state++;
}

static void Task_ShowPokeStorage(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PlaySE(SE_PC_LOGIN);
        ComputerScreenOpenEffect(20, 0, 1);
        sStorage->state++;
        break;
    case 1:
        if (!IsComputerScreenOpenEffectActive())
        {
            OrchidPC_SetBoxClip(TRUE);
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_ReshowPokeStorage(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        OrchidPC_SetBoxClip(TRUE);
        BeginNormalPaletteFade(PALETTES_ALL, -1, 0x10, 0, RGB_BLACK);
        sStorage->state++;
        break;
    case 1:
        if (!UpdatePaletteFade())
        {
            if (sWhichToReshow == SCREEN_CHANGE_ITEM_FROM_BAG - 1 && gSpecialVar_ItemId != ITEM_NONE)
            {
                PrintMessage(MSG_ITEM_IS_HELD);
                sStorage->state++;
            }
            else
            {
                SetPokeStorageTask(Task_PokeStorageMain);
            }
        }
        break;
    case 2:
        if (!IsDma3ManagerBusyWithBgCopy() && JOY_NEW(A_BUTTON | B_BUTTON))
        {
            ClearBottomWindow();
            sStorage->state++;
        }
        break;
    case 3:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

// States for the outer switch in Task_PokeStorageMain
enum {
    MSTATE_HANDLE_INPUT,
    MSTATE_MOVE_CURSOR,
    MSTATE_SCROLL_BOX,
    MSTATE_WAIT_MSG,
    MSTATE_ERROR_LAST_PARTY_MON,
    MSTATE_ERROR_HAS_MAIL,
    MSTATE_WAIT_ERROR_MSG,
    MSTATE_MULTIMOVE_RUN,
    MSTATE_MULTIMOVE_RUN_CANCEL,
    MSTATE_MULTIMOVE_RUN_MOVED,
    MSTATE_SCROLL_BOX_ITEM,
    MSTATE_WAIT_ITEM_ANIM,
};

static void Task_PokeStorageMain(u8 taskId)
{
    switch (sStorage->state)
    {
    case MSTATE_HANDLE_INPUT:
        switch (HandleInput())
        {
        case INPUT_MOVE_CURSOR:
            PlaySE(SE_SELECT);
            sStorage->state = MSTATE_MOVE_CURSOR;
            break;
        case INPUT_SHOW_PARTY:
            if (sStorage->boxOption != OPTION_MOVE_MONS && sStorage->boxOption != OPTION_MOVE_ITEMS && sStorage->boxOption != OPTION_SELECT_MON)
            {
                PrintMessage(MSG_WHICH_ONE_WILL_TAKE);
                sStorage->state = MSTATE_WAIT_MSG;
            }
            else
            {
                ClearSavedCursorPos();
                SetPokeStorageTask(Task_ShowPartyPokemon);
            }
            break;
        case INPUT_HIDE_PARTY:
            if (sStorage->boxOption == OPTION_MOVE_MONS || sStorage->boxOption == OPTION_SELECT_MON)
            {
                if (IsMonBeingMoved() && ItemIsMail(sStorage->displayMonItemId))
                    sStorage->state = MSTATE_ERROR_HAS_MAIL;
                else
                    SetPokeStorageTask(Task_HidePartyPokemon);
            }
            else if (sStorage->boxOption == OPTION_MOVE_ITEMS)
            {
                SetPokeStorageTask(Task_HidePartyPokemon);
            }
            break;
        case INPUT_CLOSE_BOX:
            SetPokeStorageTask(Task_OnCloseBoxPressed);
            break;
        case INPUT_PRESSED_B:
            SetPokeStorageTask(Task_OnBPressed);
            break;
        case INPUT_BOX_OPTIONS:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_HandleBoxOptions);
            break;
        case INPUT_IN_MENU:
            SetPokeStorageTask(Task_OnSelectedMon);
            break;
        case INPUT_SCROLL_RIGHT:
            PlaySE(SE_SELECT);
            sStorage->newCurrBoxId = StorageGetCurrentBox() + 1;
            if (sStorage->newCurrBoxId >= TOTAL_BOXES_COUNT)
                sStorage->newCurrBoxId = 0;
            if (sStorage->boxOption != OPTION_MOVE_ITEMS)
            {
                SetUpScrollToBox(sStorage->newCurrBoxId);
                sStorage->state = MSTATE_SCROLL_BOX;
            }
            else
            {
                TryHideItemAtCursor();
                sStorage->state = MSTATE_SCROLL_BOX_ITEM;
            }
            break;
        case INPUT_SCROLL_LEFT:
            PlaySE(SE_SELECT);
            sStorage->newCurrBoxId = StorageGetCurrentBox() - 1;
            if (sStorage->newCurrBoxId < 0)
                sStorage->newCurrBoxId = TOTAL_BOXES_COUNT - 1;
            if (sStorage->boxOption != OPTION_MOVE_ITEMS)
            {
                SetUpScrollToBox(sStorage->newCurrBoxId);
                sStorage->state = MSTATE_SCROLL_BOX;
            }
            else
            {
                TryHideItemAtCursor();
                sStorage->state = MSTATE_SCROLL_BOX_ITEM;
            }
            break;
        case INPUT_DEPOSIT:
            if (!IsRemovingLastPartyMon())
            {
                if (ItemIsMail(sStorage->displayMonItemId))
                {
                    sStorage->state = MSTATE_ERROR_HAS_MAIL;
                }
                else
                {
                    PlaySE(SE_SELECT);
                    SetPokeStorageTask(Task_DepositMenu);
                }
            }
            else
            {
                sStorage->state = MSTATE_ERROR_LAST_PARTY_MON;
            }
            break;
        case INPUT_MOVE_MON:
            if (IsRemovingLastPartyMon())
            {
                sStorage->state = MSTATE_ERROR_LAST_PARTY_MON;
            }
            else
            {
                PlaySE(SE_SELECT);
                SetPokeStorageTask(Task_MoveMon);
            }
            break;
        case INPUT_SHIFT_MON:
            if (!CanShiftMon())
            {
                sStorage->state = MSTATE_ERROR_LAST_PARTY_MON;
            }
            else
            {
                PlaySE(SE_SELECT);
                SetPokeStorageTask(Task_ShiftMon);
            }
            break;
        case INPUT_WITHDRAW:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_WithdrawMon);
            break;
        case INPUT_PLACE_MON:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_PlaceMon);
            break;
        case INPUT_TAKE_ITEM:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_TakeItemForMoving);
            break;
        case INPUT_GIVE_ITEM:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_GiveMovingItemToMon);
            break;
        case INPUT_SWITCH_ITEMS:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_SwitchSelectedItem);
            break;
        case INPUT_MULTIMOVE_START:
            PlaySE(SE_SELECT);
            MultiMove_SetFunction(MULTIMOVE_START);
            sStorage->state = MSTATE_MULTIMOVE_RUN;
            break;
        case INPUT_MULTIMOVE_SINGLE:
            MultiMove_SetFunction(MULTIMOVE_CANCEL);
            sStorage->state = MSTATE_MULTIMOVE_RUN_CANCEL;
            break;
        case INPUT_MULTIMOVE_CHANGE_SELECTION:
            PlaySE(SE_SELECT);
            MultiMove_SetFunction(MULTIMOVE_CHANGE_SELECTION);
            sStorage->state = MSTATE_MULTIMOVE_RUN_MOVED;
            break;
        case INPUT_MULTIMOVE_GRAB_SELECTION:
            MultiMove_SetFunction(MULTIMOVE_GRAB_SELECTION);
            sStorage->state = MSTATE_MULTIMOVE_RUN;
            break;
        case INPUT_MULTIMOVE_MOVE_MONS:
            PlaySE(SE_SELECT);
            MultiMove_SetFunction(MULTIMOVE_MOVE_MONS);
            sStorage->state = MSTATE_MULTIMOVE_RUN_MOVED;
            break;
        case INPUT_MULTIMOVE_PLACE_MONS:
            PlaySE(SE_SELECT);
            MultiMove_SetFunction(MULTIMOVE_PLACE_MONS);
            sStorage->state = MSTATE_MULTIMOVE_RUN;
            break;
        case INPUT_MULTIMOVE_UNABLE:
            // When selecting/moving multiple Pokémon the
            // cursor may not wrap around the edges.
            PlaySE(SE_FAILURE);
            break;
        }
        break;
    case MSTATE_MOVE_CURSOR:
        if (!UpdateCursorPos())
        {
            if (IsCursorOnCloseBox())
                StartFlashingCloseBoxButton();
            else
                StopFlashingCloseBoxButton();

            if (sStorage->setMosaic)
                StartDisplayMonMosaicEffect();
            sStorage->state = MSTATE_HANDLE_INPUT;
        }
        break;
    case MSTATE_SCROLL_BOX:
        if (!ScrollToBox())
        {
            SetCurrentBox(sStorage->newCurrBoxId);
            sStorage->opcRingHidden = FALSE;
            OrchidPC_UpdateRing();
            OrchidPC_ContentsChanged();
            if (!sInPartyMenu && !IsMonBeingMoved())
            {
                RefreshDisplayMon();
                StartDisplayMonMosaicEffect();
            }

            if (sStorage->boxOption == OPTION_MOVE_ITEMS)
            {
                TryShowItemAtCursor();
                sStorage->state = MSTATE_WAIT_ITEM_ANIM;
            }
            else
            {
                sStorage->state = MSTATE_HANDLE_INPUT;
            }
        }
        break;
    case MSTATE_WAIT_MSG:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            sStorage->state = MSTATE_HANDLE_INPUT;
        }
        break;
    case MSTATE_ERROR_LAST_PARTY_MON:
        PlaySE(SE_FAILURE);
        PrintMessage(MSG_LAST_POKE);
        sStorage->state = MSTATE_WAIT_ERROR_MSG;
        break;
    case MSTATE_ERROR_HAS_MAIL:
        PlaySE(SE_FAILURE);
        PrintMessage(MSG_PLEASE_REMOVE_MAIL);
        sStorage->state = MSTATE_WAIT_ERROR_MSG;
        break;
    case MSTATE_WAIT_ERROR_MSG:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    case MSTATE_MULTIMOVE_RUN:
        if (!MultiMove_RunFunction())
            sStorage->state = MSTATE_HANDLE_INPUT;
        break;
    case MSTATE_MULTIMOVE_RUN_CANCEL:
        // Began a multiple Pokémon selection but
        // ended up selecting a single Pokémon.
        // Wait for multi move to cancel, then
        // do a normal move.
        if (!MultiMove_RunFunction())
            SetPokeStorageTask(Task_MoveMon);
        break;
    case MSTATE_MULTIMOVE_RUN_MOVED:
        if (!MultiMove_RunFunction())
        {
            if (sStorage->setMosaic)
                StartDisplayMonMosaicEffect();
            sStorage->state = MSTATE_HANDLE_INPUT;
        }
        break;
    case MSTATE_SCROLL_BOX_ITEM:
        if (!IsItemIconAnimActive())
        {
            SetUpScrollToBox(sStorage->newCurrBoxId);
            sStorage->state = MSTATE_SCROLL_BOX;
        }
        break;
    case MSTATE_WAIT_ITEM_ANIM:
        if (!IsItemIconAnimActive())
            sStorage->state = MSTATE_HANDLE_INPUT;
        break;
    }
}

static void Task_ShowPartyPokemon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        SetUpDoShowPartyMenu();
        sStorage->state++;
        break;
    case 1:
        if (!DoShowPartyMenu())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

static void Task_HidePartyPokemon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PlaySE(SE_SELECT);
        SetUpHidePartyMenu();
        sStorage->opcRingHidden = TRUE; // Orchid: no ring over the box while the panel slides away
        OrchidPC_UpdateRing();
        sStorage->state++;
        break;
    case 1:
        if (!HidePartyMenu())
        {
            sStorage->opcRingHidden = FALSE;
            SetCursorBoxPosition(GetSavedCursorPos());
            sStorage->state++;
        }
        break;
    case 2:
        if (!UpdateCursorPos())
        {
            if (sStorage->setMosaic)
                StartDisplayMonMosaicEffect();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_OnSelectedMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (!IsDisplayMosaicActive())
        {
            PlaySE(SE_SELECT);
            if (sStorage->boxOption != OPTION_MOVE_ITEMS)
                PrintMessage(MSG_IS_SELECTED);
            else if (IsMovingItem() || sStorage->displayMonItemId != ITEM_NONE)
                PrintMessage(MSG_IS_SELECTED2);
            else
                PrintMessage(MSG_GIVE_TO_MON);

            AddMenu();
            sStorage->state = 1;
        }
        break;
    case 1:
        if (!IsMenuLoading())
            sStorage->state = 2;
        break;
    case 2:
        switch (HandleMenuInput())
        {
        case MENU_B_PRESSED:
        case MENU_CANCEL:
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        case MENU_MOVE:
            if (IsRemovingLastPartyMon())
            {
                sStorage->state = 3;
            }
            else
            {
                PlaySE(SE_SELECT);
                ClearBottomWindow();
                SetPokeStorageTask(Task_MoveMon);
            }
            break;
        case MENU_PLACE:
            PlaySE(SE_SELECT);
            ClearBottomWindow();
            SetPokeStorageTask(Task_PlaceMon);
            break;
        case MENU_SHIFT:
            if (!CanShiftMon())
            {
                sStorage->state = 3;
            }
            else
            {
                PlaySE(SE_SELECT);
                ClearBottomWindow();
                SetPokeStorageTask(Task_ShiftMon);
            }
            break;
        case MENU_WITHDRAW:
            PlaySE(SE_SELECT);
            ClearBottomWindow();
            SetPokeStorageTask(Task_WithdrawMon);
            break;
        case MENU_STORE:
            if (IsRemovingLastPartyMon())
            {
                sStorage->state = 3;
            }
            else if (ItemIsMail(sStorage->displayMonItemId))
            {
                sStorage->state = 4;
            }
            else
            {
                PlaySE(SE_SELECT);
                ClearBottomWindow();
                SetPokeStorageTask(Task_DepositMenu);
            }
            break;
        case MENU_RELEASE:
            if (IsRemovingLastPartyMon())
            {
                sStorage->state = 3;
            }
            else if (sStorage->displayMonIsEgg)
            {
                sStorage->state = 5; // Cannot release an Egg.
            }
            else if (ItemIsMail(sStorage->displayMonItemId))
            {
                sStorage->state = 4;
            }
            else
            {
                PlaySE(SE_SELECT);
                SetPokeStorageTask(Task_ReleaseMon);
            }
            break;
        case MENU_SUMMARY:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_ShowMonSummary);
            break;
        case MENU_MARK:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_ShowMarkMenu);
            break;
        case MENU_TAKE:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_TakeItemForMoving);
            break;
        case MENU_GIVE:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_GiveMovingItemToMon);
            break;
        case MENU_BAG:
            SetPokeStorageTask(Task_ItemToBag);
            break;
        case MENU_SWITCH:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_SwitchSelectedItem);
            break;
        case MENU_GIVE_2:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_GiveItemFromBag);
            break;
        case MENU_INFO:
            SetPokeStorageTask(Task_ShowItemInfo);
            break;
        case MENU_SELECT:
            PlaySE(SE_SELECT);
            struct BoxPokemon *boxmon = GetCursorBoxMon();
            if (sInPartyMenu)
            {
                gSpecialVar_0x8004 = sCursorPosition;
            }
            else
            {
                gSpecialVar_0x8004 = PC_MON_CHOSEN;
                gSpecialVar_MonBoxPos = sCursorPosition;
                gSpecialVar_MonBoxId = StorageGetCurrentBox();
            }
            if (IsBoxMonExcluded(boxmon))
                gSpecialVar_Result = FALSE;
            else
                gSpecialVar_Result = TRUE;
            sStorage->screenChangeType = SCREEN_CHANGE_EXIT_BOX;
            SetPokeStorageTask(Task_ChangeScreen);
            break;
        }
        break;
    case 3:
        PlaySE(SE_FAILURE);
        PrintMessage(MSG_LAST_POKE);
        sStorage->state = 6;
        break;
    case 5:
        PlaySE(SE_FAILURE);
        PrintMessage(MSG_CANT_RELEASE_EGG);
        sStorage->state = 6;
        break;
    case 4:
        PlaySE(SE_FAILURE);
        PrintMessage(MSG_PLEASE_REMOVE_MAIL);
        sStorage->state = 6;
        break;
    case 6:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_MoveMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        InitMonPlaceChange(CHANGE_GRAB);
        sStorage->state++;
        break;
    case 1:
        if (!DoMonPlaceChange())
        {
            if (sInPartyMenu)
                SetPokeStorageTask(Task_HandleMovingMonFromParty);
            else
                SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_PlaceMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        InitMonPlaceChange(CHANGE_PLACE);
        sStorage->state++;
        break;
    case 1:
        if (!DoMonPlaceChange())
        {
            if (sInPartyMenu)
                SetPokeStorageTask(Task_HandleMovingMonFromParty);
            else
                SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_ShiftMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        InitMonPlaceChange(CHANGE_SHIFT);
        sStorage->state++;
        break;
    case 1:
        if (!DoMonPlaceChange())
        {
            StartDisplayMonMosaicEffect();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_WithdrawMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (CalculatePlayerPartyCount() == PARTY_SIZE)
        {
            PrintMessage(MSG_PARTY_FULL);
            sStorage->state = 1;
        }
        else
        {
            SaveCursorPos();
            InitMonPlaceChange(CHANGE_GRAB);
            sStorage->state = 2;
        }
        break;
    case 1:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    case 2:
        if (!DoMonPlaceChange())
        {
            SetMovingMonPriority(1);
            SetUpDoShowPartyMenu();
            sStorage->state++;
        }
        break;
    case 3:
        if (!DoShowPartyMenu())
        {
            InitMonPlaceChange(CHANGE_PLACE);
            sStorage->state++;
        }
        break;
    case 4:
        if (!DoMonPlaceChange())
        {
            UpdatePartySlotColors();
            sStorage->state++;
        }
        break;
    case 5:
        SetPokeStorageTask(Task_HidePartyPokemon);
        break;
    }
}

static void Task_DepositMenu(u8 taskId)
{
    u8 boxId;

    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_DEPOSIT_IN_WHICH_BOX);
        LoadChooseBoxMenuGfx(&sStorage->chooseBoxMenu, GFXTAG_CHOOSE_BOX_MENU, PALTAG_MISC_1, 3, FALSE);
        CreateChooseBoxMenuSprites(sDepositBoxId);
        sStorage->state++;
        break;
    case 1:
        boxId = HandleChooseBoxMenuInput();
        switch (boxId)
        {
        case BOXID_NONE_CHOSEN:
            break;
        case BOXID_CANCELED:
            ClearBottomWindow();
            DestroyChooseBoxMenuSprites();
            FreeChooseBoxMenu();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        default:
            if (TryStorePartyMonInBox(boxId))
            {
                sDepositBoxId = boxId;
                ClearBottomWindow();
                DestroyChooseBoxMenuSprites();
                FreeChooseBoxMenu();
                sStorage->state = 2;
            }
            else
            {
                PrintMessage(MSG_BOX_IS_FULL);
                sStorage->state = 4;
            }
            break;
        }
        break;
    case 2:
        CompactPartySlots();
        CompactPartySprites();
        sStorage->state++;
        break;
    case 3:
        if (GetNumPartySpritesCompacting() == 0)
        {
            ResetSelectionAfterDeposit();
            StartDisplayMonMosaicEffect();
            UpdatePartySlotColors();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    case 4:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            PrintMessage(MSG_DEPOSIT_IN_WHICH_BOX);
            sStorage->state = 1;
        }
        break;
    }
}

static void Task_ReleaseMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_RELEASE_POKE);
        ShowYesNoWindow(1);
        sStorage->state++;
        // fallthrough
    case 1:
        switch (Menu_ProcessInputNoWrapClearOnChoose())
        {
        case MENU_B_PRESSED:
        case  1: // No
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        case  0: // Yes
            ClearBottomWindow();
            InitCanReleaseMonVars();
            InitReleaseMon();
            sStorage->state++;
            break;
        }
        break;
    case 2:
        RunCanReleaseMon();
        if (!TryHideReleaseMon())
        {
            while (1)
            {
                s8 canRelease = RunCanReleaseMon();
                if (canRelease == TRUE)
                {
                    sStorage->state++;
                    break;
                }
                else if (!canRelease)
                {
                    sStorage->state = 8;
                    break;
                }
            }
        }
        break;
    case 3:
        ReleaseMon();
        RefreshDisplayMonData();
        PrintMessage(MSG_WAS_RELEASED);
        sStorage->state++;
        break;
    case 4:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            PrintMessage(MSG_BYE_BYE);
            sStorage->state++;
        }
        break;
    case 5:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            if (sInPartyMenu)
            {
                CompactPartySlots();
                CompactPartySprites();
                sStorage->state++;
            }
            else
            {
                sStorage->state = 7;
            }
        }
        break;
    case 6:
        if (GetNumPartySpritesCompacting() == 0)
        {
            RefreshDisplayMon();
            StartDisplayMonMosaicEffect();
            UpdatePartySlotColors();
            sStorage->state++;
        }
        break;
    case 7:
        SetPokeStorageTask(Task_PokeStorageMain);
        break;
    case 8:
        // Start "can't release" sequence
        PrintMessage(MSG_WAS_RELEASED);
        sStorage->state++;
        break;
    case 9:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            PrintMessage(MSG_SURPRISE);
            sStorage->state++;
        }
        break;
    case 10:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            ReshowReleaseMon();
            sStorage->state++;
        }
        break;
    case 11:
        if (!ResetReleaseMonSpritePtr())
        {
            TrySetCursorFistAnim();
            PrintMessage(MSG_CAME_BACK);
            sStorage->state++;
        }
        break;
    case 12:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            PrintMessage(MSG_WORRIED);
            sStorage->state++;
        }
        break;
    case 13:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_ShowMarkMenu(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_MARK_POKE);
        sStorage->markMenu.markings = sStorage->displayMonMarkings;
        OpenMonMarkingsMenu(sStorage->displayMonMarkings, 0xb0, 0x10);
        sStorage->state++;
        break;
    case 1:
        if (!HandleMonMarkingsMenuInput())
        {
            FreeMonMarkingsMenu();
            ClearBottomWindow();
            SetMonMarkings(sStorage->markMenu.markings);
            RefreshDisplayMonData();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_TakeItemForMoving(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (!ItemIsMail(sStorage->displayMonItemId))
        {
            ClearBottomWindow();
            sStorage->state++;
        }
        else
        {
            SetPokeStorageTask(Task_PrintCantStoreMail);
        }
        break;
    case 1:
        StartCursorAnim(CURSOR_ANIM_OPEN);
        TakeItemFromMon(sInPartyMenu ? CURSOR_AREA_IN_PARTY : CURSOR_AREA_IN_BOX, GetCursorPosition());
        sStorage->state++;
        sJustOpenedBag = FALSE;
        break;
    case 2:
        if (!IsItemIconAnimActive())
        {
            StartCursorAnim(CURSOR_ANIM_FIST);
            ClearBottomWindow();
            RefreshDisplayMon();
            PrintDisplayMonInfo();
            sStorage->state++;
        }
        break;
    case 3:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

static void Task_GiveMovingItemToMon(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        ClearBottomWindow();
        sStorage->state++;
        break;
    case 1:
        StartCursorAnim(CURSOR_ANIM_OPEN);
        GiveItemToMon(sInPartyMenu ? CURSOR_AREA_IN_PARTY : CURSOR_AREA_IN_BOX, GetCursorPosition());
        sStorage->state++;
        break;
    case 2:
        if (!IsItemIconAnimActive())
        {
            StartCursorAnim(CURSOR_ANIM_BOUNCE);
            RefreshDisplayMon();
            PrintDisplayMonInfo();
            PrintMessage(MSG_ITEM_IS_HELD);
            sStorage->state++;
        }
        break;
    case 3:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            sStorage->state++;
        }
        break;
    case 4:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

static void Task_ItemToBag(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (!AddBagItem(sStorage->displayMonItemId, 1))
        {
            PlaySE(SE_FAILURE);
            PrintMessage(MSG_BAG_FULL);
            sStorage->state = 3;
        }
        else
        {
            PlaySE(SE_SELECT);
            MoveItemFromMonToBag(sInPartyMenu ? CURSOR_AREA_IN_PARTY : CURSOR_AREA_IN_BOX, GetCursorPosition());
            sStorage->state = 1;
        }
        break;
    case 1:
        if (!IsItemIconAnimActive())
        {
            PrintMessage(MSG_PLACED_IN_BAG);
            sStorage->state = 2;
        }
        break;
    case 2:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            RefreshDisplayMon();
            PrintDisplayMonInfo();
            sStorage->state = 4;
        }
        break;
    case 4:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    case 3:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_SwitchSelectedItem(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (!ItemIsMail(sStorage->displayMonItemId))
        {
            ClearBottomWindow();
            sStorage->state++;
        }
        else
        {
            SetPokeStorageTask(Task_PrintCantStoreMail);
        }
        break;
    case 1:
        StartCursorAnim(CURSOR_ANIM_OPEN);
        SwapItemsWithMon(sInPartyMenu ? CURSOR_AREA_IN_PARTY : CURSOR_AREA_IN_BOX, GetCursorPosition());
        sStorage->state++;
        break;
    case 2:
        if (!IsItemIconAnimActive())
        {
            StartCursorAnim(CURSOR_ANIM_FIST);
            RefreshDisplayMon();
            PrintDisplayMonInfo();
            PrintMessage(MSG_CHANGED_TO_ITEM);
            sStorage->state++;
        }
        break;
    case 3:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            sStorage->state++;
        }
        break;
    case 4:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

static void Task_ShowItemInfo(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        ClearBottomWindow();
        sStorage->state++;
        break;
    case 1:
        if (!IsDma3ManagerBusyWithBgCopy())
        {
            PlaySE(SE_WIN_OPEN);
            PrintItemDescription();
            InitItemInfoWindow();
            sStorage->state++;
        }
        break;
    case 2:
        if (!UpdateItemInfoWindowSlideIn())
            sStorage->state++;
        break;
    case 3:
        if (!IsDma3ManagerBusyWithBgCopy())
            sStorage->state++;
        break;
    case 4:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            PlaySE(SE_WIN_OPEN);
            sStorage->state++;
        }
        break;
    case 5:
        if (!UpdateItemInfoWindowSlideOut())
            sStorage->state++;
        break;
    case 6:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

static void Task_CloseBoxWhileHoldingItem(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PlaySE(SE_SELECT);
        PrintMessage(MSG_PUT_IN_BAG);
        ShowYesNoWindow(0);
        sStorage->state = 1;
        break;
    case 1:
        switch (Menu_ProcessInputNoWrapClearOnChoose())
        {
        case MENU_B_PRESSED:
        case 1: // No
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        case 0:// Yes
            if (AddBagItem(sStorage->movingItemId, 1) == TRUE)
            {
                ClearBottomWindow();
                sStorage->state = 3;
            }
            else
            {
                PrintMessage(MSG_BAG_FULL);
                sStorage->state = 2;
            }
            break;
        }
        break;
    case 2:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            sStorage->state = 5;
        }
        break;
    case 3:
        MoveItemFromCursorToBag();
        sStorage->state = 4;
        break;
    case 4:
        if (!IsItemIconAnimActive())
        {
            StartCursorAnim(CURSOR_ANIM_BOUNCE);
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    case 5:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

static void Task_HandleMovingMonFromParty(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        CompactPartySlots();
        CompactPartySprites();
        sStorage->state++;
        break;
    case 1:
        if (GetNumPartySpritesCompacting() == 0)
        {
            UpdatePartySlotColors();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_PrintCantStoreMail(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_CANT_STORE_MAIL);
        sStorage->state++;
        break;
    case 1:
        if (!IsDma3ManagerBusyWithBgCopy())
            sStorage->state++;
        break;
    case 2:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            sStorage->state++;
        }
        break;
    case 3:
        if (!IsDma3ManagerBusyWithBgCopy())
            SetPokeStorageTask(Task_PokeStorageMain);
        break;
    }
}

// Handle options menu that shows when the box title bar is selected
static void Task_HandleBoxOptions(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_WHAT_YOU_DO);
        AddMenu();
        sStorage->state++;
        break;
    case 1:
        if (IsMenuLoading())
            return;
        sStorage->state++;
    case 2:
        switch (HandleMenuInput())
        {
        case MENU_B_PRESSED:
        case MENU_CANCEL:
            AnimateBoxScrollArrows(TRUE);
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        case MENU_NAME:
            PlaySE(SE_SELECT);
            SetPokeStorageTask(Task_NameBox);
            break;
        case MENU_WALLPAPER:
            PlaySE(SE_SELECT);
            ClearBottomWindow();
            SetPokeStorageTask(Task_HandleWallpapers);
            break;
        case MENU_JUMP:
            PlaySE(SE_SELECT);
            ClearBottomWindow();
            SetPokeStorageTask(Task_JumpBox);
            break;
        }
        break;
    }
}

// Orchid: COLOUR picks one of the box colours (mock_pc state 10); left / right preview it live on the box.
static void Task_HandleWallpapers(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_PICK_A_WALLPAPER);
        OrchidPC_ColourPickerOpen();
        sStorage->state++;
        break;
    case 1:
        if (JOY_NEW(A_BUTTON))
        {
            PlaySE(SE_SELECT);
            SetBoxWallpaper(StorageGetCurrentBox(), sStorage->opcColourSel);
            OrchidPC_ColourPickerClose();
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            OrchidPC_ColourPickerClose();
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        else if (JOY_REPEAT(DPAD_LEFT))
        {
            PlaySE(SE_SELECT);
            OrchidPC_ColourPickerMove(-1);
        }
        else if (JOY_REPEAT(DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            OrchidPC_ColourPickerMove(1);
        }
        break;
    }
}

static void Task_JumpBox(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        PrintMessage(MSG_JUMP_TO_WHICH_BOX);
        LoadChooseBoxMenuGfx(&sStorage->chooseBoxMenu, GFXTAG_CHOOSE_BOX_MENU, PALTAG_MISC_1, 3, FALSE);
        CreateChooseBoxMenuSprites(StorageGetCurrentBox());
        sStorage->state++;
        break;
    case 1:
        sStorage->newCurrBoxId = HandleChooseBoxMenuInput();
        switch (sStorage->newCurrBoxId)
        {
        case BOXID_NONE_CHOSEN:
            break;
        default:
            ClearBottomWindow();
            DestroyChooseBoxMenuSprites();
            FreeChooseBoxMenu();
            if (sStorage->newCurrBoxId == BOXID_CANCELED || sStorage->newCurrBoxId == StorageGetCurrentBox())
            {
                AnimateBoxScrollArrows(TRUE);
                SetPokeStorageTask(Task_PokeStorageMain);
            }
            else
            {
                sStorage->state++;
            }
            break;
        }
        break;
    case 2:
        SetUpScrollToBox(sStorage->newCurrBoxId);
        sStorage->state++;
        break;
    case 3:
        if (!ScrollToBox())
        {
            SetCurrentBox(sStorage->newCurrBoxId);
            sStorage->opcRingHidden = FALSE;
            OrchidPC_UpdateRing();
            OrchidPC_ContentsChanged();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    }
}

static void Task_NameBox(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        SaveMovingMon();
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        sStorage->state++;
        break;
    case 1:
        if (!UpdatePaletteFade())
        {
            sWhichToReshow = SCREEN_CHANGE_NAME_BOX - 1;
            sStorage->screenChangeType = SCREEN_CHANGE_NAME_BOX;
            SetPokeStorageTask(Task_ChangeScreen);
        }
        break;
    }
}

static void Task_ShowMonSummary(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        InitSummaryScreenData();
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        sStorage->state++;
        break;
    case 1:
        if (!UpdatePaletteFade())
        {
            sWhichToReshow = SCREEN_CHANGE_SUMMARY_SCREEN - 1;
            sStorage->screenChangeType = SCREEN_CHANGE_SUMMARY_SCREEN;
            SetPokeStorageTask(Task_ChangeScreen);
        }
        break;
    }
}

static void Task_GiveItemFromBag(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        sStorage->state++;
        break;
    case 1:
        if (!UpdatePaletteFade())
        {
            sWhichToReshow = SCREEN_CHANGE_ITEM_FROM_BAG - 1;
            sStorage->screenChangeType = SCREEN_CHANGE_ITEM_FROM_BAG;
            SetPokeStorageTask(Task_ChangeScreen);
            sJustOpenedBag = TRUE;
        }
        break;
    }
}

static void Task_OnCloseBoxPressed(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (IsMonBeingMoved())
        {
            PlaySE(SE_FAILURE);
            PrintMessage(MSG_HOLDING_POKE);
            sStorage->state = 1;
        }
        else if (IsMovingItem())
        {
            SetPokeStorageTask(Task_CloseBoxWhileHoldingItem);
        }
        else
        {
            PlaySE(SE_SELECT);
            PrintMessage(MSG_EXIT_BOX);
            ShowYesNoWindow(0);
            sStorage->state = 2;
        }
        break;
    case 1:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    case 2:
        switch (Menu_ProcessInputNoWrapClearOnChoose())
        {
        case MENU_B_PRESSED:
        case 1:
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        case 0:
            PlaySE(SE_PC_OFF);
            ClearBottomWindow();
            sStorage->state++;
            break;
        }
        break;
    case 3:
        OrchidPC_SetBoxClip(FALSE);
        ComputerScreenCloseEffect(20, 0, 1);
        sStorage->state++;
        break;
    case 4:
        if (!IsComputerScreenCloseEffectActive())
        {
            UpdateBoxToSendMons();
            gPartiesCount[B_TRAINER_PLAYER] = CalculatePlayerPartyCount();
            if (sStorage->boxOption == OPTION_SELECT_MON)
            {
                gSpecialVar_0x8004 = PARTY_NOTHING_CHOSEN;
                gSpecialVar_Result = FALSE;
            }
            sStorage->screenChangeType = SCREEN_CHANGE_EXIT_BOX;
            SetPokeStorageTask(Task_ChangeScreen);
        }
        break;
    }
}

static void Task_OnBPressed(u8 taskId)
{
    switch (sStorage->state)
    {
    case 0:
        if (IsMonBeingMoved())
        {
            if (OW_PC_PRESS_B < GEN_4)
            {
                PlaySE(SE_FAILURE);
                PrintMessage(MSG_HOLDING_POKE);
                sStorage->state = 1;
            }
            else if (CanPlaceMon())
            {
                PlaySE(SE_SELECT);
                SetPokeStorageTask(Task_PlaceMon);
            }
            else
            {
                SetPokeStorageTask(Task_PokeStorageMain);
            }
        }
        else if (IsMovingItem())
        {
            SetPokeStorageTask(Task_CloseBoxWhileHoldingItem);
        }
        else
        {
            PlaySE(SE_SELECT);
            PrintMessage(MSG_CONTINUE_BOX);
            ShowYesNoWindow(0);
            sStorage->state = 2;
        }
        break;
    case 1:
        if (JOY_NEW(A_BUTTON | B_BUTTON | DPAD_ANY))
        {
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
        }
        break;
    case 2:
        switch (Menu_ProcessInputNoWrapClearOnChoose())
        {
        case 0:
            ClearBottomWindow();
            SetPokeStorageTask(Task_PokeStorageMain);
            break;
        case 1:
        case MENU_B_PRESSED:
            PlaySE(SE_PC_OFF);
            ClearBottomWindow();
            sStorage->state++;
            break;
        }
        break;
    case 3:
        OrchidPC_SetBoxClip(FALSE);
        ComputerScreenCloseEffect(20, 0, 0);
        sStorage->state++;
        break;
    case 4:
        if (!IsComputerScreenCloseEffectActive())
        {
            UpdateBoxToSendMons();
            gPartiesCount[B_TRAINER_PLAYER] = CalculatePlayerPartyCount();
            if (sStorage->boxOption == OPTION_SELECT_MON)
            {
                gSpecialVar_0x8004  = PARTY_NOTHING_CHOSEN;
                gSpecialVar_Result  = FALSE;
            }
            sStorage->screenChangeType = SCREEN_CHANGE_EXIT_BOX;
            SetPokeStorageTask(Task_ChangeScreen);
        }
        break;
    }
}

static void Task_ChangeScreen(u8 taskId)
{
    struct BoxPokemon *boxMons;
    u8 mode, monIndex, maxMonIndex;
    u8 screenChangeType = sStorage->screenChangeType;

    if (sStorage->boxOption == OPTION_MOVE_ITEMS && IsMovingItem() == TRUE)
        sMovingItemId = GetMovingItemId();
    else
        sMovingItemId = ITEM_NONE;

    switch (screenChangeType)
    {
    case SCREEN_CHANGE_EXIT_BOX:
    default:
        if (sStorage->boxOption == OPTION_SELECT_MON)
            SetMainCallback2(CB2_ReturnToFieldContinueScript);
        else
            SetMainCallback2(CB2_ExitPokeStorage);
        FreePokeStorageData();
        break;
    case SCREEN_CHANGE_SUMMARY_SCREEN:
        boxMons = sStorage->summaryMon.box;
        monIndex = sStorage->summaryStartPos;
        maxMonIndex = sStorage->summaryMaxPos;
        mode = sStorage->summaryScreenMode;
        FreePokeStorageData();
        ShowPokemonSummaryScreen(mode, boxMons, monIndex, maxMonIndex, CB2_ReturnToPokeStorage);
        break;
    case SCREEN_CHANGE_NAME_BOX:
        FreePokeStorageData();
        DoNamingScreen(NAMING_SCREEN_BOX, GetBoxNamePtr(StorageGetCurrentBox()), 0, 0, 0, CB2_ReturnToPokeStorage);
        break;
    case SCREEN_CHANGE_ITEM_FROM_BAG:
        FreePokeStorageData();
        GoToBagMenu(ITEMMENULOCATION_PCBOX, 0, CB2_ReturnToPokeStorage);
        break;
    }

    DestroyTask(taskId);
}

static void GiveChosenBagItem(void)
{
    enum Item itemId = gSpecialVar_ItemId;

    if (itemId != ITEM_NONE)
    {
        u8 pos = GetCursorPosition();
        if (sInPartyMenu)
        {
            struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][pos];
            SetMonData(&gParties[B_TRAINER_PLAYER][pos], MON_DATA_HELD_ITEM, &itemId);
            SetMonFormPSS_ItemHold(&mon->box);
        }
        else
        {
            SetCurrentBoxMonData(pos, MON_DATA_HELD_ITEM, &itemId);
            SetMonFormPSS_ItemHold(&gPokemonStoragePtr->boxes[StorageGetCurrentBox()][pos]);
        }

        RemoveBagItem(itemId, 1);
    }
}

static void FreePokeStorageData(void)
{
    TRY_FREE_AND_SET_NULL(sStorage->opcTypeSheet);
    MultiMove_Free();
    FREE_AND_SET_NULL(sStorage);
    FreeAllWindowBuffers();
}


//------------------------------------------------------------------------------
//  Orchid UI helpers (dev_scripts/orchid_ui/mock_pc.py, export_pc.py)
//
//  BG1 holds the screen art (sOPcStaticMap) plus the party panel (sOPcPanel*), both
//  rebuilt into the BG1 buffer by OrchidPC_RedrawBg1. A gold cursor is a palette swap
//  of the cells its element owns. The info / title / party slot text windows sit on
//  BG1 too: their tiles start as a copy of the art under them, then get text.
//------------------------------------------------------------------------------

static const u8 sText_OrchidLv[] = _("{LV}");
static const u8 sText_OrchidNone[] = _("None");

static void OrchidPC_RedrawBg1(void);
static void OrchidPC_PrintTitle(u8 boxId);

static u16 *OrchidPC_Bg1Map(void)
{
    return (u16 *)sStorage->displayMenuTilemapBuffer;
}

static bool32 OrchidPC_IsRingArea(u8 area, u8 pos)
{
    return area == CURSOR_AREA_IN_BOX || (area == CURSOR_AREA_IN_PARTY && pos < PARTY_SIZE);
}

// Copies one art tile (with its tilemap flips) into a 4bpp tile buffer.
static void OrchidPC_CopyArtTile(u8 *dst, u16 entry)
{
    const u8 *src = &gOrchidPcBg1_Gfx[(entry & 0x3FF) * TILE_SIZE_4BPP];
    bool32 hFlip = (entry & 0x400) != 0;
    bool32 vFlip = (entry & 0x800) != 0;
    u32 x, y;

    for (y = 0; y < 8; y++)
    {
        const u8 *row = src + (vFlip ? 7 - y : y) * 4;
        for (x = 0; x < 4; x++)
        {
            if (hFlip)
            {
                u8 b = row[3 - x];
                dst[y * 4 + x] = (b >> 4) | (b << 4);
            }
            else
            {
                dst[y * 4 + x] = row[x];
            }
        }
    }
}

static u16 OrchidPC_PanelEntry(u32 row, u32 col)
{
    u32 slots = sOPcPanelSlots[row][col];
    u32 combo = 0, bit = 0, k;

    for (k = 0; k < PARTY_SIZE; k++)
    {
        if (slots & (1 << k))
        {
            if (sStorage->opcFilled & (1 << k))
                combo |= 1 << bit;
            bit++;
        }
    }
    return sOPcPanelVariants[sOPcPanelBase[row][col] + combo];
}

// The art under a window (static art, or the open party panel for the slot windows).
static void OrchidPC_FillWindowFromArt(u8 windowId)
{
    u8 *tiles = (u8 *)GetWindowAttribute(windowId, WINDOW_TILE_DATA);
    u32 left = GetWindowAttribute(windowId, WINDOW_TILEMAP_LEFT);
    u32 top = GetWindowAttribute(windowId, WINDOW_TILEMAP_TOP);
    u32 width = GetWindowAttribute(windowId, WINDOW_WIDTH);
    u32 height = GetWindowAttribute(windowId, WINDOW_HEIGHT);
    bool32 panel = (windowId >= WIN_PSLOT_0);
    u32 x, y;

    for (y = 0; y < height; y++)
    {
        for (x = 0; x < width; x++)
        {
            u16 entry;
            if (panel)
                entry = OrchidPC_PanelEntry(top + y - OPC_PANEL_ROW0, left + x - OPC_PANEL_COL0);
            else
                entry = sOPcStaticMap[top + y][left + x];
            OrchidPC_CopyArtTile(&tiles[(y * width + x) * TILE_SIZE_4BPP], entry);
        }
    }
}

static void OrchidPC_SetWindowPixel(u8 windowId, u32 x, u32 y, u8 color)
{
    u8 *tiles = (u8 *)GetWindowAttribute(windowId, WINDOW_TILE_DATA);
    u32 width = GetWindowAttribute(windowId, WINDOW_WIDTH);
    u8 *b = &tiles[((y / 8) * width + x / 8) * TILE_SIZE_4BPP + (y % 8) * 4 + (x % 8) / 2];

    if (x & 1)
        *b = (*b & 0x0F) | (color << 4);
    else
        *b = (*b & 0xF0) | color;
}

// Writes a window's tiles into the BG1 buffer at (left, top) (rows from 20 down are skipped).
static void OrchidPC_PutBg1Window(u8 windowId, s32 left, s32 top, u8 palette)
{
    u16 *map = OrchidPC_Bg1Map();
    u32 base = GetWindowAttribute(windowId, WINDOW_BASE_BLOCK);
    u32 width = GetWindowAttribute(windowId, WINDOW_WIDTH);
    u32 height = GetWindowAttribute(windowId, WINDOW_HEIGHT);
    u32 x, y;

    for (y = 0; y < height; y++)
    {
        if (top + y >= DISPLAY_TILE_HEIGHT)
            break;
        for (x = 0; x < width; x++)
            map[(top + y) * 32 + left + x] = (base + y * width + x) | (palette << 12);
    }
}

static u8 OrchidPC_SlotHpPal(u8 slot, bool32 gold)
{
    return OPC_BG_SLOT + sStorage->opcSlotHp[slot] + (gold ? 3 : 0);
}

// ---- BG1: static art + windows + party panel
static void OrchidPC_RedrawBg1(void)
{
    u16 *map = OrchidPC_Bg1Map();
    u32 r, c, k;
    s32 slide = sStorage->opcPartySlide;

    for (r = 0; r < DISPLAY_TILE_HEIGHT; r++)
    {
        for (c = 0; c < DISPLAY_TILE_WIDTH; c++)
        {
            u8 own = sOPcStaticOwner[r][c];
            u8 pal = (own != OPC_OWN_NONE && own == sStorage->opcGoldOwner) ? OPC_BG_UI_GOLD : OPC_BG_UI;
            map[r * 32 + c] = sOPcStaticMap[r][c] | (pal << 12);
        }
    }
    OrchidPC_PutBg1Window(WIN_DISPLAY_INFO, OPC_INFO_WIN_LEFT, OPC_INFO_WIN_TOP, OPC_BG_UI);
    OrchidPC_PutBg1Window(WIN_TITLE, OPC_TITLE_WIN_LEFT, OPC_TITLE_WIN_TOP,
                          sStorage->opcGoldOwner == OPC_OWN_TITLE ? OPC_BG_TITLE_GOLD : OPC_BG_TITLE);

    if (slide < OPC_PANEL_SLIDE)
    {
        for (r = 0; r < OPC_PANEL_ROWS; r++)
        {
            s32 row = OPC_PANEL_ROW0 + r + slide;
            if (row >= DISPLAY_TILE_HEIGHT)
                break;
            for (c = 0; c < OPC_PANEL_COLS; c++)
            {
                u16 entry;
                if (r == 0 && slide == 0)
                {
                    // the tab's bottom edge and the panel's top edge share these cells
                    entry = sOPcPanelRow4Open[c] | (OPC_BG_UI << 12);
                }
                else
                {
                    u8 own = sOPcPanelOwner[r][c];
                    bool32 gold = (own != 0xFF && own == sStorage->opcPartySel);
                    entry = OrchidPC_PanelEntry(r, c) | ((gold ? OPC_BG_SLOT + 3 : OPC_BG_SLOT) << 12);
                }
                map[row * 32 + OPC_PANEL_COL0 + c] = entry;
            }
        }
        for (k = 0; k < PARTY_SIZE; k++)
        {
            u8 win = WIN_PSLOT_0 + k;
            if (!(sStorage->opcFilled & (1 << k)))
                continue;
            OrchidPC_PutBg1Window(win, GetWindowAttribute(win, WINDOW_TILEMAP_LEFT),
                                  GetWindowAttribute(win, WINDOW_TILEMAP_TOP) + slide,
                                  OrchidPC_SlotHpPal(k, sStorage->opcPartySel == k));
        }
    }
    ScheduleBgCopyTilemapToVram(1);
}

// Gold cursor art: buttons / title tab / party slot or CANCEL under the cursor.
static void OrchidPC_SetSelection(u8 area, u8 pos)
{
    u8 gold = OPC_OWN_NONE, partySel = 0xFF;

    switch (area)
    {
    case CURSOR_AREA_BUTTONS:
        gold = (pos == 0) ? OPC_OWN_PARTY : OPC_OWN_CLOSE;
        break;
    case CURSOR_AREA_BOX_TITLE:
        gold = OPC_OWN_TITLE;
        break;
    case CURSOR_AREA_IN_PARTY:
        partySel = pos;
        break;
    }
    if (gold != sStorage->opcGoldOwner || partySel != sStorage->opcPartySel)
    {
        sStorage->opcGoldOwner = gold;
        sStorage->opcPartySel = partySel;
        OrchidPC_RedrawBg1();
    }
}

// ---- party slot windows: Lv + mini HP bar (pc_ext.party_slot / party_slot_text)
static void OrchidPC_RefreshPartySlots(void)
{
    static const u8 sColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_INK, OPC_ROLE_PANEL_SHADE};
    u32 k;

    sStorage->opcFilled = 0;
    for (k = 0; k < PARTY_SIZE; k++)
    {
        if (GetMonData(&gParties[B_TRAINER_PLAYER][k], MON_DATA_SPECIES) != SPECIES_NONE)
            sStorage->opcFilled |= 1 << k;
    }

    for (k = 0; k < PARTY_SIZE; k++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][k];
        u8 win = WIN_PSLOT_0 + k;
        s32 slotX = OPC_PSLOT_X0 + OPC_PSLOT_DX * (k % 2);
        s32 slotY = OPC_PSLOT_Y0 + OPC_PSLOT_DY * (k / 2);
        s32 winX = GetWindowAttribute(win, WINDOW_TILEMAP_LEFT) * 8;
        s32 winY = GetWindowAttribute(win, WINDOW_TILEMAP_TOP) * 8;
        u32 hp, maxHp, fill, x;
        u8 text[16];

        sStorage->opcSlotHp[k] = 0;
        if (!(sStorage->opcFilled & (1 << k)))
            continue;
        OrchidPC_FillWindowFromArt(win);
        if (!GetMonData(mon, MON_DATA_IS_EGG))
        {
            u8 *ptr = StringCopy(text, sText_OrchidLv);
            ConvertIntToDecimalStringN(ptr, GetMonData(mon, MON_DATA_LEVEL), STR_CONV_MODE_LEFT_ALIGN, 3);
            AddTextPrinterParameterized4(win, FONT_SMALL, slotX + OPC_PLV_DX - winX, slotY + OPC_PLV_DY - winY, 0, 0, sColors, TEXT_SKIP_DRAW, text);

            // KX.bar(x + 25, y + 16, 15, frac, h=2): outline + trough are in the art; fill rows y+17 (light), y+18 (dark)
            hp = GetMonData(mon, MON_DATA_HP);
            maxHp = GetMonData(mon, MON_DATA_MAX_HP);
            if (maxHp == 0)
                maxHp = 1;
            if (hp * 2 > maxHp)
                sStorage->opcSlotHp[k] = 0;
            else if (hp * 5 > maxHp)
                sStorage->opcSlotHp[k] = 1;
            else
                sStorage->opcSlotHp[k] = 2;
            fill = (OPC_PBAR_W * hp * 2 + maxHp) / (maxHp * 2);
            if (hp > 0 && fill == 0)
                fill = 1;
            for (x = 0; x < fill; x++)
            {
                s32 px = slotX + OPC_PBAR_DX + 1 + x - winX;
                OrchidPC_SetWindowPixel(win, px, slotY + OPC_PBAR_DY + 1 - winY, OPC_ROLE_ACCENT_PALE);
                OrchidPC_SetWindowPixel(win, px, slotY + OPC_PBAR_DY + 2 - winY, OPC_ROLE_SPARE_B);
            }
        }
        CopyWindowToVram(win, COPYWIN_GFX);
    }
}

// ---- info panel: name (gender colour), Lv, markings, item (pc_ext.info_text)
static void OrchidPC_SetNameColors(u8 gender)
{
    u16 colors[2];

    if (gender == MON_MALE)
    {
        colors[0] = ORCHID_NAME_MALE_FG;
        colors[1] = ORCHID_NAME_MALE_SHADOW;
    }
    else if (gender == MON_FEMALE)
    {
        colors[0] = ORCHID_NAME_FEMALE_FG;
        colors[1] = ORCHID_NAME_FEMALE_SHADOW;
    }
    else
    {
        colors[0] = gOrchidPc_Pal[OPC_PAL_UI * 16 + OPC_ROLE_INK];
        colors[1] = gOrchidPc_Pal[OPC_PAL_UI * 16 + OPC_ROLE_PANEL_SHADE];
    }
    LoadPalette(colors, BG_PLTT_ID(OPC_BG_UI) + OPC_ROLE_SPARE_A, PLTT_SIZEOF(2));
}

static void OrchidPC_UpdateTypeIcons(enum Species species, bool32 show)
{
    enum Type types[2] = {TYPE_NONE, TYPE_NONE};
    u32 i, base = GetSpriteTileStartByTag(GFXTAG_TYPE_ICONS);

    if (show && species != SPECIES_NONE)
    {
        types[0] = GetSpeciesType(species, 0);
        types[1] = GetSpeciesType(species, 1);
        if (types[1] == types[0])
            types[1] = TYPE_NONE;
    }
    for (i = 0; i < 2; i++)
    {
        struct Sprite *sprite;
        if (sStorage->opcTypeSprites[i] == SPRITE_NONE)
            continue;
        sprite = &gSprites[sStorage->opcTypeSprites[i]];
        if (types[i] == TYPE_NONE || sStorage->opcTypeSheet == NULL || base == 0xFFFF)
        {
            sprite->invisible = TRUE;
        }
        else
        {
            u32 row = gTypesInfo[types[i]].palette - 13;
            struct SpritePalette pal = {gMoveTypes_Pal + row * 16, PALTAG_TYPE_0 + row};
            u8 palNum = LoadSpritePalette(&pal);

            CpuCopy32(sStorage->opcTypeSheet + types[i] * 8 * TILE_SIZE_4BPP,
                      (void *)(OBJ_VRAM0 + (base + i * 8) * TILE_SIZE_4BPP), 8 * TILE_SIZE_4BPP);
            sprite->invisible = (palNum == 0xFF);
            sprite->oam.paletteNum = palNum;
        }
    }
}

static void OrchidPC_UpdateItemIcon(enum Item item)
{
    if (item == sStorage->opcItemShown && (item == ITEM_NONE || sStorage->opcItemSprite != SPRITE_NONE))
        return;
    if (sStorage->opcItemSprite != SPRITE_NONE)
    {
        DestroySprite(&gSprites[sStorage->opcItemSprite]);
        FreeSpriteTilesByTag(GFXTAG_DISC_ITEM);
        FreeSpritePaletteByTag(PALTAG_DISC_ITEM);
        sStorage->opcItemSprite = SPRITE_NONE;
    }
    sStorage->opcItemShown = item;
    if (item != ITEM_NONE)
    {
        u8 spriteId = AddItemIconSprite(GFXTAG_DISC_ITEM, PALTAG_DISC_ITEM, item);
        if (spriteId != MAX_SPRITES)
        {
            gSprites[spriteId].x = OPC_ITEM_ICON_X;
            gSprites[spriteId].y = OPC_ITEM_ICON_Y;
            gSprites[spriteId].oam.priority = 1;
            sStorage->opcItemSprite = spriteId;
        }
    }
}

static void OrchidPC_PrintInfo(void)
{
    static const u8 sNameColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_SPARE_A, OPC_ROLE_SPARE_B};
    static const u8 sLvColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_WHITE, OPC_ROLE_ACCENT_DARK};
    static const u8 sInkColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_INK, OPC_ROLE_PANEL_SHADE};
    static const u8 sNoneColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_INK_SOFT, OPC_ROLE_PANEL_SHADE};
    u8 win = WIN_DISPLAY_INFO;
    s32 winX = OPC_INFO_WIN_LEFT * 8, winY = OPC_INFO_WIN_TOP * 8;
    bool32 hasMon = (sStorage->displayMonSpecies != SPECIES_NONE);
    u8 text[24];
    u32 fontId, w, k, x, y;

    OrchidPC_FillWindowFromArt(win);
    if (hasMon)
    {
        const u8 *name = sStorage->displayMonIsEgg ? sStorage->displayMonNameText : sStorage->displayMonName;
        u8 *end;

        // name: the ROM's nickname, trailing spaces trimmed
        end = StringCopy(text, name);
        while (end > text && end[-1] == CHAR_SPACE)
            end--;
        *end = EOS;
        OrchidPC_SetNameColors(sStorage->displayMonIsEgg ? MON_GENDERLESS : sStorage->displayMonGender);
        fontId = (GetStringWidth(FONT_NORMAL, text, 0) <= OPC_NAME_W - 10) ? FONT_NORMAL : FONT_NARROW;
        w = GetStringWidth(fontId, text, 0);
        AddTextPrinterParameterized4(win, fontId, OPC_NAME_X + (s32)(OPC_NAME_W - w) / 2 - winX, OPC_NAME_Y - 1 - winY, 0, 0, sNameColors, TEXT_SKIP_DRAW, text);

        if (!sStorage->displayMonIsEgg)
        {
            AddTextPrinterParameterized4(win, FONT_SMALL, OPC_LV_X + 4 - winX, OPC_LV_Y + 1 - winY, 0, 0, sLvColors, TEXT_SKIP_DRAW, sText_OrchidLv);
            ConvertIntToDecimalStringN(text, sStorage->displayMonLevel, STR_CONV_MODE_LEFT_ALIGN, 3);
            w = GetStringWidth(FONT_SMALL, text, 0);
            AddTextPrinterParameterized4(win, FONT_SMALL, OPC_LV_X + OPC_LV_W - 5 - w - winX, OPC_LV_Y + 1 - winY, 0, 0, sInkColors, TEXT_SKIP_DRAW, text);
        }

        // markings: the ROM's four shapes, ACCENT_DARK when set, PANEL_SHADE when not
        for (k = 0; k < 4; k++)
        {
            u8 color = (sStorage->displayMonMarkings & (1 << k)) ? OPC_ROLE_ACCENT_DARK : OPC_ROLE_PANEL_SHADE;
            for (y = 0; y < 8; y++)
            {
                for (x = 0; x < 8; x++)
                {
                    if (sOPcMarks[k][y] & (0x80 >> x))
                        OrchidPC_SetWindowPixel(win, OPC_MARK_X + 9 * k + x - winX, OPC_MARK_Y + y - winY, color);
                }
            }
        }

        if (!sStorage->displayMonIsEgg)
        {
            const u8 *itemName = (sStorage->displayMonItemId != ITEM_NONE) ? GetItemName(sStorage->displayMonItemId) : sText_OrchidNone;
            s32 width = OPC_ITEM_TEXT_X1 - OPC_ITEM_TEXT_X0;

            fontId = GetFontIdToFit(itemName, FONT_NORMAL, 0, width);
            w = GetStringWidth(fontId, itemName, 0);
            AddTextPrinterParameterized4(win, fontId, OPC_ITEM_TEXT_X0 + (width - (s32)w) / 2 + 1 - winX, OPC_ITEM_Y - winY, 0, 0,
                                         (sStorage->displayMonItemId != ITEM_NONE) ? sInkColors : sNoneColors, TEXT_SKIP_DRAW, itemName);
        }
    }
    CopyWindowToVram(win, COPYWIN_GFX);
    OrchidPC_UpdateTypeIcons(sStorage->displayMonSpecies, hasMon && !sStorage->displayMonIsEgg);
    OrchidPC_UpdateItemIcon(hasMon && !sStorage->displayMonIsEgg ? sStorage->displayMonItemId : ITEM_NONE);
}

// ---- title tab: box name on the accent cap, "n/30" in the inset (mock_pc.render)
static void OrchidPC_PrintTitle(u8 boxId)
{
    static const u8 sNameColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_SPARE_A, OPC_ROLE_ACCENT_DARK};
    static const u8 sCountColors[3] = {TEXT_COLOR_TRANSPARENT, OPC_ROLE_INK, OPC_ROLE_PANEL_SHADE};
    s32 winX = OPC_TITLE_WIN_LEFT * 8, winY = OPC_TITLE_WIN_TOP * 8;
    const u8 *name = GetBoxNamePtr(boxId);
    u8 text[16], *ptr;
    s32 w;

    sStorage->opcTitleBox = boxId;
    sStorage->opcTitleDirty = FALSE;
    OrchidPC_FillWindowFromArt(WIN_TITLE);
    w = GetStringWidth(FONT_NORMAL, name, 0);
    AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, OPC_TAB_X + (OPC_TAB_CAP - w) / 2 + 1 - winX, OPC_TAB_Y - 1 - winY, 0, 0, sNameColors, TEXT_SKIP_DRAW, name);
    ptr = ConvertIntToDecimalStringN(text, CountMonsInBox(boxId), STR_CONV_MODE_LEFT_ALIGN, 2);
    StringCopy(ptr, sText_OutOf30);
    w = GetStringWidth(FONT_SMALL, text, 0);
    AddTextPrinterParameterized4(WIN_TITLE, FONT_SMALL, OPC_TAB_X + OPC_TAB_CAP + (OPC_TAB_W - OPC_TAB_CAP - w) / 2 + 1 - winX, OPC_TAB_Y + 1 - winY, 0, 0, sCountColors, TEXT_SKIP_DRAW, text);
    CopyWindowToVram(WIN_TITLE, COPYWIN_GFX);
}

// ---- BG2: slot recesses (one 3x3-tile cell per slot), 512 px wide for the box slide
static u8 OrchidPC_GetBoxColour(u8 boxId)
{
    u8 colour = GetBoxWallpaper(boxId);
    return (colour < OPC_BOX_COLOURS) ? colour : 0;
}

static void OrchidPC_LoadBoxColour(u8 colour, u8 bgPal)
{
    LoadPalette(&gOrchidPcBoxColours_Pal[colour * 16], BG_PLTT_ID(bgPal), PLTT_SIZE_4BPP);
}

static void OrchidPC_SetBg2Entry(u32 x, u32 y, u16 entry)
{
    u16 *map = (u16 *)sStorage->wallpaperBgTilemapBuffer;
    x &= 63;
    map[(x >= 32 ? 0x400 : 0) + y * 32 + (x & 31)] = entry;
}

static void OrchidPC_DrawBoxSlots(u32 col0, u8 bgPal)
{
    u32 i, x, y;

    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        u32 cx = col0 + 3 * (i % IN_BOX_COLUMNS);
        u32 cy = OPC_SLOT_ROW0 + 3 * (i / IN_BOX_COLUMNS);
        for (y = 0; y < 3; y++)
            for (x = 0; x < 3; x++)
                OrchidPC_SetBg2Entry(cx + x, cy + y, sOPcSlotCell[y][x] | (bgPal << 12));
    }
}

static void OrchidPC_ClearBoxSlotsExcept(s32 keepCol0, bool32 keep)
{
    u32 x, y;

    for (x = 0; x < 64; x++)
    {
        if (keep && ((x - keepCol0) & 63) < IN_BOX_COLUMNS * 3)
            continue;
        for (y = 0; y < 32; y++)
            OrchidPC_SetBg2Entry(x, y, 0);
    }
}

// ---- BG1 window on/off for the box slide: BG2 only inside x 80..239 (WIN1; WIN0 is the PC open / close effect)
static void OrchidPC_SetBoxClip(bool32 on)
{
    if (on)
    {
        SetGpuReg(REG_OFFSET_WIN1H, WIN_RANGE(80, DISPLAY_WIDTH));
        SetGpuReg(REG_OFFSET_WIN1V, WIN_RANGE(0, DISPLAY_HEIGHT));
        SetGpuReg(REG_OFFSET_WININ, WININ_WIN1_ALL);
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0 | WINOUT_WIN01_BG1 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ | WINOUT_WIN01_CLR);
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN1_ON);
    }
    else
    {
        ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN1_ON);
    }
}

// ---- cursor ring visibility
static void OrchidPC_UpdateRing(void)
{
    if (sStorage->cursorSprite == NULL)
        return;
    sStorage->cursorSprite->invisible = sStorage->opcRingHidden || !OrchidPC_IsRingArea(sCursorArea, sCursorPosition);
    if (sCursorArea == CURSOR_AREA_IN_PARTY)
    {
        // above the party icons (mock_pc.render draws it after the panel layer)
        sStorage->cursorSprite->oam.priority = 1;
        sStorage->cursorSprite->subpriority = 10;
    }
    else if (sCursorArea == CURSOR_AREA_IN_BOX)
    {
        // under the box icons; over the multi-move layer while selecting several
        sStorage->cursorSprite->oam.priority = (sStorage->inBoxMovingMode != MOVE_MODE_NORMAL) ? 0 : 2;
        sStorage->cursorSprite->subpriority = 21;
    }
}

// ---- MOVE ITEMS: hold tags on the Pokémon that hold something (mock state 8)
static void OrchidPC_DestroyHoldTags(void)
{
    u32 i;

    for (i = 0; i < ARRAY_COUNT(sStorage->opcTagSprites); i++)
    {
        if (sStorage->opcTagSprites[i] != SPRITE_NONE)
        {
            DestroySprite(&gSprites[sStorage->opcTagSprites[i]]);
            sStorage->opcTagSprites[i] = SPRITE_NONE;
        }
    }
}

static const struct OamData sOamData_OrchidHoldTag =
{
    .shape = SPRITE_SHAPE(8x8),
    .size = SPRITE_SIZE(8x8),
    .priority = 2,
};

static const struct SpriteTemplate sSpriteTemplate_OrchidHoldTag =
{
    .tileTag = GFXTAG_HOLD_TAG,
    .paletteTag = PALTAG_MISC_2,
    .oam = &sOamData_OrchidHoldTag,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static void OrchidPC_RefreshHoldTags(void)
{
    u32 i;

    sStorage->opcTagsDirty = FALSE;
    OrchidPC_DestroyHoldTags();
    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;
    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        if (GetCurrentBoxMonData(i, MON_DATA_SPECIES) != SPECIES_NONE && GetCurrentBoxMonData(i, MON_DATA_HELD_ITEM) != ITEM_NONE)
        {
            u8 spriteId = CreateSprite(&sSpriteTemplate_OrchidHoldTag,
                                       OPC_SLOT_X0 + OPC_SLOT_PITCH * (i % IN_BOX_COLUMNS) + OPC_HOLD_TAG_DX,
                                       OPC_SLOT_Y0 + OPC_SLOT_PITCH * (i / IN_BOX_COLUMNS) + OPC_HOLD_TAG_DY, 13);
            sStorage->opcTagSprites[i] = (spriteId == MAX_SPRITES) ? SPRITE_NONE : spriteId;
        }
    }
    if (sInPartyMenu && sStorage->opcPartySlide == 0)
    {
        for (i = 0; i < PARTY_SIZE; i++)
        {
            struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][i];
            if (GetMonData(mon, MON_DATA_SPECIES) != SPECIES_NONE && GetMonData(mon, MON_DATA_HELD_ITEM) != ITEM_NONE)
            {
                u8 spriteId = CreateSprite(&sSpriteTemplate_OrchidHoldTag,
                                           OPC_PSLOT_X0 + OPC_PSLOT_DX * (i % 2) + OPC_PICON_DX + OPC_HOLD_TAG_DX,
                                           OPC_PSLOT_Y0 + OPC_PSLOT_DY * (i / 2) + OPC_PICON_DY + OPC_HOLD_TAG_DY, 11);
                if (spriteId != MAX_SPRITES)
                {
                    gSprites[spriteId].oam.priority = 1;
                    sStorage->opcTagSprites[IN_BOX_COUNT + i] = spriteId;
                }
            }
        }
    }
}

// Per-frame Orchid upkeep (CB2): title count after box contents change, hold tags.
static void OrchidPC_Update(void)
{
    if (sStorage == NULL)
        return;
    if (sStorage->opcTitleDirty)
        OrchidPC_PrintTitle(sStorage->opcTitleBox);
    if (sStorage->opcTagsDirty)
        OrchidPC_RefreshHoldTags();
}

static void OrchidPC_ContentsChanged(void)
{
    sStorage->opcTitleDirty = TRUE;
    sStorage->opcTagsDirty = TRUE;
}

static void OrchidPC_LoadSlotPalettes(void)
{
    LoadPalette(&gOrchidPc_Pal[OPC_PAL_SLOT_G * 16], BG_PLTT_ID(OPC_BG_SLOT), 6 * PLTT_SIZE_4BPP);
}

static void OrchidPC_PartyIconPos(u8 partyId, s16 *x, s16 *y)
{
    *x = OPC_PSLOT_X0 + OPC_PSLOT_DX * (partyId % 2) + OPC_PICON_DX;
    *y = OPC_PSLOT_Y0 + OPC_PSLOT_DY * (partyId / 2) + OPC_PICON_DY + OPC_ICON_DY;
}


//------------------------------------------------------------------------------
//  SECTION: Misc
//------------------------------------------------------------------------------

static void SetScrollingBackground(void)
{
    u16 *map = (u16 *)BG_SCREEN_ADDR(31);
    u32 x, y;

    // BW grid, 2x2 tiles repeated (backdrop.grid_tile_image)
    SetGpuReg(REG_OFFSET_BG3CNT, BGCNT_PRIORITY(3) | BGCNT_CHARBASE(3) | BGCNT_16COLOR | BGCNT_SCREENBASE(31));
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            map[y * 32 + x] = (OPC_GRID_TILE_BASE + (y & 1) * 2 + (x & 1)) | (OPC_BG_GRID << 12);
}

// The grid scrolls diagonally down-right, 1 px every 4 frames.
static void ScrollBackground(void)
{
    if (sStorage != NULL && (++sStorage->opcFrame % OPC_GRID_SCROLL_FRAMES) == 0)
    {
        ChangeBgX(3, 256, BG_COORD_SUB);
        ChangeBgY(3, 256, BG_COORD_SUB);
    }
}

static void LoadPokeStorageMenuGfx(void)
{
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    LoadBgTiles(1, gOrchidPcBg1_Gfx, OPC_BG1_ART_TILES * TILE_SIZE_4BPP, 0);
    LoadBgTiles(2, gOrchidPcBox_Gfx, OPC_BOX_TILES * TILE_SIZE_4BPP, 0); // BG2 + BG3 (charblock 3)
    sStorage->opcGoldOwner = OPC_OWN_NONE;
    sStorage->opcPartySel = 0xFF;
    sStorage->opcPartySlide = OPC_PANEL_SLIDE;
    sStorage->opcFilled = 0;
    sStorage->opcRingHidden = FALSE;
    sStorage->opcTitleDirty = FALSE;
    sStorage->opcTagsDirty = FALSE;
    sStorage->opcItemSprite = SPRITE_NONE;
    sStorage->opcItemShown = ITEM_NONE;
    sStorage->opcTypeSprites[0] = sStorage->opcTypeSprites[1] = SPRITE_NONE;
    sStorage->opcLift = OPC_LIFT;
    sStorage->opcTypeSheet = NULL;
    memset(sStorage->opcTagSprites, SPRITE_NONE, sizeof(sStorage->opcTagSprites));
    memset(sStorage->displayMenuTilemapBuffer, 0, sizeof(sStorage->displayMenuTilemapBuffer));
    SetBgTilemapBuffer(1, sStorage->displayMenuTilemapBuffer);
    ShowBg(1);
}

static bool8 InitPokeStorageWindows(void)
{
    if (!InitWindows(sWindowTemplates))
    {
        return FALSE;
    }
    else
    {
        DeactivateAllTextPrinters();
        return TRUE;
    }
}

static void LoadWaveformSpritePalette(void)
{
    LoadSpritePalette(&sWaveformSpritePalette);
}

static const struct OamData sOamData_OrchidTypeIcon =
{
    .shape = SPRITE_SHAPE(32x16),
    .size = SPRITE_SIZE(32x16),
    .priority = 1,
};

static void InitPalettesAndSprites(void)
{
    u32 i;

    LoadPalette(&gOrchidPc_Pal[OPC_PAL_UI * 16], BG_PLTT_ID(OPC_BG_UI), 2 * PLTT_SIZE_4BPP);
    OrchidPC_LoadSlotPalettes();
    LoadPalette(&gOrchidPc_Pal[OPC_PAL_TITLE * 16], BG_PLTT_ID(OPC_BG_TITLE), 2 * PLTT_SIZE_4BPP);
    LoadPalette(gOrchidYesNoFrame_Pal, BG_PLTT_ID(OPC_BG_WINDOW), PLTT_SIZE_4BPP);
    LoadPalette(sTextWindows_Pal, BG_PLTT_ID(OPC_BG_TEXTWIN), sizeof(sTextWindows_Pal));
    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        LoadPalette(&gOrchidPc_Pal[OPC_PAL_GRID * 16], BG_PLTT_ID(OPC_BG_GRID), PLTT_SIZE_4BPP);
    else
        LoadPalette(&gOrchidPc_Pal[OPC_PAL_GRID_ITEMS * 16], BG_PLTT_ID(OPC_BG_GRID), PLTT_SIZE_4BPP);

    SetGpuReg(REG_OFFSET_BG1CNT, BGCNT_PRIORITY(1) | BGCNT_CHARBASE(2) | BGCNT_16COLOR | BGCNT_SCREENBASE(30));

    // type icons: two 32x16 slots filled from the decompressed Gen 3 type sheet
    sStorage->opcTypeSheet = Alloc((NUMBER_OF_MON_TYPES + CONTEST_CATEGORIES_COUNT) * 0x100);
    if (sStorage->opcTypeSheet != NULL)
    {
        struct SpriteSheet sheet = {sStorage->opcTypeSheet, 2 * 8 * TILE_SIZE_4BPP, GFXTAG_TYPE_ICONS};
        struct SpriteTemplate template = {
            .tileTag = GFXTAG_TYPE_ICONS,
            .paletteTag = TAG_NONE,
            .oam = &sOamData_OrchidTypeIcon,
            .anims = gDummySpriteAnimTable,
            .affineAnims = gDummySpriteAffineAnimTable,
            .callback = SpriteCallbackDummy,
        };
        DecompressDataWithHeaderWram(gMoveTypes_Gfx, sStorage->opcTypeSheet);
        if (LoadSpriteSheet(&sheet) != 0)
        {
            for (i = 0; i < 2; i++)
            {
                u8 spriteId = CreateSprite(&template, OPC_TYPES_X + OPC_TYPES_PITCH * i + 16, OPC_TYPES_Y + 8, 1);
                if (spriteId != MAX_SPRITES)
                {
                    gSprites[spriteId].oam.tileNum += i * 8;
                    gSprites[spriteId].invisible = TRUE;
                    sStorage->opcTypeSprites[i] = spriteId;
                }
            }
        }
    }

    CreateDisplayMonSprite();
    CreateMarkingComboSprite();
    CreateWaveformSprites();
    RefreshDisplayMonData();
}

// Orchid: markings are drawn in the info window
static void CreateMarkingComboSprite(void)
{
}

// Orchid: no "Pkmn Data" waveform
static void CreateWaveformSprites(void)
{
}

static void RefreshDisplayMonData(void)
{
    LoadDisplayMonGfx(sStorage->displayMonSpecies, sStorage->displayMonPersonality, sStorage->displayMonIsEgg);
    PrintDisplayMonInfo();
    UpdateWaveformAnimation();
    ScheduleBgCopyTilemapToVram(0);
}

static void StartDisplayMonMosaicEffect(void)
{
    RefreshDisplayMonData();
    if (sStorage->displayMonSprite)
    {
        sStorage->displayMonSprite->oam.mosaic = TRUE;
        sStorage->displayMonSprite->data[0] = 10;
        sStorage->displayMonSprite->data[1] = 1;
        sStorage->displayMonSprite->callback = SpriteCB_DisplayMonMosaic;
        SetGpuReg(REG_OFFSET_MOSAIC, (sStorage->displayMonSprite->data[0] << 12) | (sStorage->displayMonSprite->data[0] << 8));
    }
}

static u8 IsDisplayMosaicActive(void)
{
    return sStorage->displayMonSprite->oam.mosaic;
}

static void SpriteCB_DisplayMonMosaic(struct Sprite *sprite)
{
    sprite->data[0] -= sprite->data[1];
    if (sprite->data[0] < 0)
        sprite->data[0] = 0;
    SetGpuReg(REG_OFFSET_MOSAIC, (sprite->data[0] << 12) | (sprite->data[0] << 8));
    if (sprite->data[0] == 0)
    {
        sprite->oam.mosaic = FALSE;
        sprite->callback = SpriteCallbackDummy;
    }
}

static void CreateDisplayMonSprite(void)
{
    u16 i;
    u16 tileStart;
    u8 palSlot;
    u8 spriteId;
    struct SpriteSheet sheet = {sStorage->tileBuffer, MON_PIC_SIZE, GFXTAG_DISPLAY_MON};
    struct SpritePalette palette = {sStorage->displayMonPalette, PALTAG_DISPLAY_MON};
    struct SpriteTemplate template = sSpriteTemplate_DisplayMon;

    for (i = 0; i < MON_PIC_SIZE; i++)
        sStorage->tileBuffer[i] = 0;

    sStorage->displayMonSprite = NULL;

    do
    {
        tileStart = LoadSpriteSheet(&sheet);
        if (tileStart == 0)
            break;

        palSlot = LoadSpritePalette(&palette);
        if (palSlot == 0xFF)
            break;

        spriteId = CreateSpriteUnchecked(&template, OPC_DAIS_X, OPC_STAGE_Y - 32, 0);
        if (spriteId == MAX_SPRITES)
            break;

        sStorage->displayMonSprite = &gSprites[spriteId];
        sStorage->displayMonPalOffset = OBJ_PLTT_ID(palSlot);
        sStorage->displayMonTilePtr = (void *) OBJ_VRAM0 + tileStart * TILE_SIZE_4BPP;
    } while (0);

    if (sStorage->displayMonSprite == NULL)
    {
        FreeSpriteTilesByTag(GFXTAG_DISPLAY_MON);
        FreeSpritePaletteByTag(PALTAG_DISPLAY_MON);
    }
}

static void LoadDisplayMonGfx(enum Species species, u32 pid, bool32 isEgg)
{
    if (sStorage->displayMonSprite == NULL)
        return;

    if (species != SPECIES_NONE)
    {
        // Orchid: the front pic stands on the dais stage (mock_pc: bottom row on OPC_STAGE_Y)
        enum Species picSpecies = isEgg ? SPECIES_EGG : SanitizeSpeciesId(species);
        LoadSpecialPokePicIsEgg(sStorage->tileBuffer, species, pid, TRUE, isEgg);
        CpuCopy32(sStorage->tileBuffer, sStorage->displayMonTilePtr, MON_PIC_SIZE);
        LoadPalette(sStorage->displayMonPalette, sStorage->displayMonPalOffset, PLTT_SIZE_4BPP);
        sStorage->displayMonSprite->y = OPC_STAGE_Y - 32 + gSpeciesInfo[picSpecies].frontPicYOffset;
        sStorage->displayMonSprite->invisible = FALSE;
    }
    else
    {
        sStorage->displayMonSprite->invisible = TRUE;
    }
}

static void PrintDisplayMonInfo(void)
{
    OrchidPC_PrintInfo();
}

// Orchid: no waveform / "Pkmn Data" header
static void UpdateWaveformAnimation(void)
{
}

static void InitSupplementalTilemaps(void)
{
    if (sInPartyMenu)
    {
        sStorage->opcPartySlide = 0;
        OrchidPC_RefreshPartySlots();
        CreatePartyMonsSprites(TRUE);
    }
    else
    {
        sStorage->opcPartySlide = OPC_PANEL_SLIDE;
    }
    OrchidPC_PrintTitle(StorageGetCurrentBox());
    OrchidPC_SetSelection(sCursorArea, sCursorPosition);
    OrchidPC_RedrawBg1();
    sStorage->opcTagsDirty = TRUE;
}

static void SetUpShowPartyMenu(void)
{
    sStorage->partyMenuY = 2;
    sStorage->partyMenuMoveTimer = 0;
    sStorage->opcPartySlide = OPC_PANEL_SLIDE;
    OrchidPC_LoadSlotPalettes();
    OrchidPC_RefreshPartySlots();
    CreatePartyMonsSprites(FALSE);
}

// Orchid: the panel slides up from the bottom, 1 tile per frame, icons with it
static bool8 ShowPartyMenu(void)
{
    if (sStorage->partyMenuMoveTimer == OPC_PANEL_SLIDE)
        return FALSE;

    sStorage->opcPartySlide--;
    OrchidPC_RedrawBg1();
    MovePartySprites(-8);
    if (++sStorage->partyMenuMoveTimer == OPC_PANEL_SLIDE)
    {
        sInPartyMenu = TRUE;
        sStorage->opcTagsDirty = TRUE;
        return FALSE;
    }
    else
    {
        return TRUE;
    }
}

static void SetUpHidePartyMenu(void)
{
    sStorage->partyMenuY = 22;
    sStorage->partyMenuMoveTimer = 0;
    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        MoveHeldItemWithPartyMenu();
        OrchidPC_DestroyHoldTags();
    }
}

static bool8 HidePartyMenu(void)
{
    if (sStorage->partyMenuMoveTimer != OPC_PANEL_SLIDE)
    {
        sStorage->opcPartySlide++;
        OrchidPC_RedrawBg1();
        MovePartySprites(8);
        if (++sStorage->partyMenuMoveTimer != OPC_PANEL_SLIDE)
            return TRUE;

        sInPartyMenu = FALSE;
        DestroyAllPartyMonIcons();
        CompactPartySlots();
        sStorage->opcTagsDirty = TRUE;
        return FALSE;
    }

    return FALSE;
}

// Orchid: the CLOSE BOX button turns gold under the cursor instead of flashing
static void StartFlashingCloseBoxButton(void)
{
}

static void StopFlashingCloseBoxButton(void)
{
}

static void UpdateCloseBoxButtonFlash(void)
{
    OrchidPC_Update();
}

static void SetPartySlotTilemaps(void)
{
    OrchidPC_RefreshPartySlots();
}

static void UpdatePartySlotColors(void)
{
    SetPartySlotTilemaps();
    OrchidPC_RedrawBg1();
}

static void SetUpDoShowPartyMenu(void)
{
    sStorage->showPartyMenuState = 0;
    PlaySE(SE_WIN_OPEN);
    SetUpShowPartyMenu();
}

static bool8 DoShowPartyMenu(void)
{
    switch (sStorage->showPartyMenuState)
    {
    case 0:
        if (!ShowPartyMenu())
        {
            SetCursorInParty();
            sStorage->showPartyMenuState++;
        }
        break;
    case 1:
        if (!UpdateCursorPos())
        {
            if (sStorage->setMosaic)
                StartDisplayMonMosaicEffect();
            sStorage->showPartyMenuState++;
        }
        break;
    case 2:
        return FALSE;
    }
    return TRUE;
}

static void UpdateBoxToSendMons(void)
{
    if (sLastUsedBox != StorageGetCurrentBox())
    {
        FlagClear(FLAG_SHOWN_BOX_WAS_FULL_MESSAGE);
        VarSet(VAR_PC_BOX_TO_SEND_MON, StorageGetCurrentBox());
    }
}

static void InitPokeStorageBg0(void)
{
    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(0) | BGCNT_CHARBASE(0) | BGCNT_SCREENBASE(29));
    LoadBgTiles(0, gOrchidYesNoFrame_Gfx, 9 * TILE_SIZE_4BPP, OPC_FRAME_TILE);
    LoadBgTiles(0, gOrchidPcSwatch_Gfx, OPC_SWATCH_TILES * TILE_SIZE_4BPP, OPC_SWATCH_TILE);
    FillBgTilemapBufferRect(0, 0, 0, 0, 32, 20, 17);
    CopyBgTilemapBufferToVram(0);
}

static void PrintMessage(u8 id)
{
    u8 *txtPtr;

    DynamicPlaceholderTextUtil_Reset();
    switch (sMessages[id].format)
    {
    case MSG_VAR_NONE:
        break;
    case MSG_VAR_MON_NAME_1:
    case MSG_VAR_MON_NAME_2:
    case MSG_VAR_MON_NAME_3:
        DynamicPlaceholderTextUtil_SetPlaceholderPtr(0, sStorage->displayMonName);
        break;
    case MSG_VAR_RELEASE_MON_1:
    case MSG_VAR_RELEASE_MON_2:
    case MSG_VAR_RELEASE_MON_3:
        DynamicPlaceholderTextUtil_SetPlaceholderPtr(0, sStorage->releaseMonName);
        break;
    case MSG_VAR_ITEM_NAME:
        if (IsMovingItem())
            txtPtr = StringCopy(sStorage->itemName, GetMovingItemName());
        else
            txtPtr = StringCopy(sStorage->itemName, sStorage->displayMonItemName);

        while (*(txtPtr - 1) == CHAR_SPACE)
            txtPtr--;

        *txtPtr = EOS;
        DynamicPlaceholderTextUtil_SetPlaceholderPtr(0, sStorage->itemName);
        break;
    }

    DynamicPlaceholderTextUtil_ExpandPlaceholders(sStorage->messageText, sMessages[id].text);
    FillWindowPixelBuffer(WIN_MESSAGE, PIXEL_FILL(1));
    AddTextPrinterParameterized(WIN_MESSAGE, FONT_NORMAL, sStorage->messageText, 0, 1, TEXT_SKIP_DRAW, NULL);
    DrawTextBorderOuter(WIN_MESSAGE, OPC_FRAME_TILE, OPC_BG_WINDOW);
    PutWindowTilemap(WIN_MESSAGE);
    CopyWindowToVram(WIN_MESSAGE, COPYWIN_GFX);
    ScheduleBgCopyTilemapToVram(0);
}

static void ShowYesNoWindow(s8 cursorPos)
{
    CreateOrchidYesNoMenu(&sYesNoWindowTemplate, OPC_FRAME_TILE, OPC_BG_WINDOW, 0);
    Menu_MoveCursorNoWrapAround(cursorPos);
}

static void ClearBottomWindow(void)
{
    ClearStdWindowAndFrameToTransparent(WIN_MESSAGE, FALSE);
    ScheduleBgCopyTilemapToVram(0);
}

// ---- Orchid box colour picker (replaces the wallpaper menus): six swatches over the box, gold ring
static void OrchidPC_ColourPickerOpen(void)
{
    static const struct WindowTemplate sTemplate = {
        .bg = 0,
        .tilemapLeft = OPC_SWATCH_WIN_LEFT,
        .tilemapTop = OPC_SWATCH_WIN_TOP,
        .width = OPC_BOX_COLOURS * 3,
        .height = 3,
        .paletteNum = OPC_BG_WINDOW,
        .baseBlock = 0xD0,
    };
    u32 k, x, y;

    sStorage->opcColourSel = OrchidPC_GetBoxColour(StorageGetCurrentBox());
    sStorage->opcColourWindow = AddWindow(&sTemplate);
    DrawStdFrameWithCustomTileAndPalette(sStorage->opcColourWindow, FALSE, OPC_FRAME_TILE, OPC_BG_WINDOW);
    for (k = 0; k < OPC_BOX_COLOURS; k++)
    {
        OrchidPC_LoadBoxColour(k, OPC_BG_SLOT + k);
        for (y = 0; y < 3; y++)
            for (x = 0; x < 3; x++)
                FillBgTilemapBufferRect(0, OPC_SWATCH_TILE + sOPcSwatchCell[y][x], OPC_SWATCH_WIN_LEFT + 3 * k + x, OPC_SWATCH_WIN_TOP + y, 1, 1, OPC_BG_SLOT + k);
    }
    ScheduleBgCopyTilemapToVram(0);
    sStorage->cursorSprite->x = OPC_SWATCH_X0 + OPC_SLOT_PITCH * sStorage->opcColourSel;
    sStorage->cursorSprite->y = OPC_SWATCH_Y;
    sStorage->cursorSprite->oam.priority = 0;
    sStorage->cursorSprite->subpriority = 0;
    sStorage->cursorSprite->invisible = FALSE;
}

static void OrchidPC_ColourPickerMove(s8 delta)
{
    sStorage->opcColourSel = (sStorage->opcColourSel + OPC_BOX_COLOURS + delta) % OPC_BOX_COLOURS;
    sStorage->cursorSprite->x = OPC_SWATCH_X0 + OPC_SLOT_PITCH * sStorage->opcColourSel;
    OrchidPC_LoadBoxColour(sStorage->opcColourSel, OPC_BG_BOX + sStorage->wallpaperOffset); // live preview
}

static void OrchidPC_ColourPickerClose(void)
{
    u16 x, y;

    ClearStdWindowAndFrameToTransparent(sStorage->opcColourWindow, FALSE);
    RemoveWindow(sStorage->opcColourWindow);
    OrchidPC_LoadSlotPalettes();
    OrchidPC_LoadBoxColour(OrchidPC_GetBoxColour(StorageGetCurrentBox()), OPC_BG_BOX + sStorage->wallpaperOffset);
    GetCursorCoordsByPos(sCursorArea, sCursorPosition, &x, &y);
    sStorage->cursorSprite->x = x;
    sStorage->cursorSprite->y = y;
    OrchidPC_UpdateRing();
    ScheduleBgCopyTilemapToVram(0);
}

static u8 GetCurrentBoxOption(void)
{
    return sCurrentBoxOption;
}

static void InitCursorItemIcon(void)
{
    if (!IsCursorOnBoxTitle())
    {
        if (sInPartyMenu)
            TryLoadItemIconAtPos(CURSOR_AREA_IN_PARTY, GetCursorPosition());
        else
            TryLoadItemIconAtPos(CURSOR_AREA_IN_BOX, GetCursorPosition());
    }

    if (sMovingItemId != ITEM_NONE)
    {
        InitItemIconInCursor(sMovingItemId);
        StartCursorAnim(CURSOR_ANIM_FIST);
    }
}


//------------------------------------------------------------------------------
//  SECTION: Pokémon sprites
//
//  The below functions generally handle the Pokémon icon sprites, including
//  moving them with a scrolling box, shifting the party sprites, and
//  animating released Pokémon.
//------------------------------------------------------------------------------


static void InitMonIconFields(void)
{
    u16 i;

    LoadMonIconPalettes();
    for (i = 0; i < MAX_MON_ICONS; i++)
        sStorage->numIconsPerSpecies[i] = 0;
    for (i = 0; i < MAX_MON_ICONS; i++)
        sStorage->iconSpeciesList[i] = SPECIES_NONE;
    for (i = 0; i < PARTY_SIZE; i++)
        sStorage->partySprites[i] = NULL;
    for (i = 0; i < IN_BOX_COUNT; i++)
        sStorage->boxMonsSprites[i] = NULL;

    sStorage->movingMonSprite = NULL;
}

// Orchid: the held Pokémon floats above the BG1 art (title tab, party panel) wherever the cursor is
static u8 GetMonIconPriorityByCursorPos(void)
{
    return 1;
}

static void CreateMovingMonIcon(void)
{
    u32 personality = GetMonData(&sStorage->movingMon, MON_DATA_PERSONALITY);
    enum Species species = GetMonData(&sStorage->movingMon, MON_DATA_SPECIES);
    u8 priority = GetMonIconPriorityByCursorPos();
    bool32 isEgg = GetMonData(&sStorage->movingMon, MON_DATA_IS_EGG);

    sStorage->movingMonSprite = CreateMonIconSprite(species, personality, 0, 0, priority, 7, isEgg);
    sStorage->movingMonSprite->callback = SpriteCB_HeldMon;
    sStorage->opcLift = OPC_LIFT;
}

static bool32 ShouldBoxmonSpriteBeTransparent(u32 boxId, u32 boxPosition)
{
    if (sStorage->boxOption == OPTION_MOVE_ITEMS
     && GetBoxMonDataAt(boxId, boxPosition, MON_DATA_HELD_ITEM) == ITEM_NONE)
        return TRUE;
    if (sStorage->boxOption == OPTION_SELECT_MON
     && IsBoxMonExcluded(GetBoxedMonPtr(boxId, boxPosition)))
        return TRUE;
    return FALSE;
}

static void InitBoxMonSprites(u8 boxId)
{
    u8 boxPosition;
    u16 i, j, count;
    enum Species species;
    u32 personality;

    count = 0;
    boxPosition = 0;

    // For each box slot, create a Pokémon icon if a species is present
    for (i = 0; i < IN_BOX_ROWS; i++)
    {
        for (j = 0; j < IN_BOX_COLUMNS; j++)
        {
            species = GetBoxMonDataAt(boxId, boxPosition, MON_DATA_SPECIES);
            bool32 isEgg = GetBoxMonDataAt(boxId, boxPosition, MON_DATA_IS_EGG);
            if (species != SPECIES_NONE)
            {
                personality = GetBoxMonDataAt(boxId, boxPosition, MON_DATA_PERSONALITY);
                sStorage->boxMonsSprites[count] = CreateMonIconSprite(species, personality, 8 * (3 * j) + OPC_SLOT_X0, 8 * (3 * i) + OPC_SLOT_Y0 + OPC_ICON_DY, 2, 19 - j, isEgg);

                if (ShouldBoxmonSpriteBeTransparent(boxId, boxPosition))
                    sStorage->boxMonsSprites[boxPosition]->oam.objMode = ST_OAM_OBJ_BLEND;
            }
            else
            {
                sStorage->boxMonsSprites[count] = NULL;
            }
            boxPosition++;
            count++;
        }
    }
}

static void CreateBoxMonIconAtPos(u8 boxPosition)
{
    enum Species species = GetCurrentBoxMonData(boxPosition, MON_DATA_SPECIES);
    bool32 isEgg = GetCurrentBoxMonData(boxPosition, MON_DATA_IS_EGG);

    if (species != SPECIES_NONE)
    {
        s16 x = 8 * (3 * (boxPosition % IN_BOX_COLUMNS)) + OPC_SLOT_X0;
        s16 y = 8 * (3 * (boxPosition / IN_BOX_COLUMNS)) + OPC_SLOT_Y0 + OPC_ICON_DY;
        u32 personality = GetCurrentBoxMonData(boxPosition, MON_DATA_PERSONALITY);

        sStorage->boxMonsSprites[boxPosition] = CreateMonIconSprite(species, personality, x, y, 2, 19 - (boxPosition % IN_BOX_COLUMNS), isEgg);
        if (ShouldBoxmonSpriteBeTransparent(StorageGetCurrentBox(), boxPosition))
            sStorage->boxMonsSprites[boxPosition]->oam.objMode = ST_OAM_OBJ_BLEND;
    }
}

#define sDistance      data[1]
#define sSpeed         data[2]
#define sScrollInDestX data[3]
#define sDelay         data[4]
#define sScrollOutX    data[5]

static void StartBoxMonIconsScrollOut(s16 speed)
{
    u16 i;

    for (i = 0; i < IN_BOX_COUNT; i++)
    {
        if (sStorage->boxMonsSprites[i] != NULL)
        {
            sStorage->boxMonsSprites[i]->sSpeed = speed;
            sStorage->boxMonsSprites[i]->sDelay = 1;
            sStorage->boxMonsSprites[i]->callback = SpriteCB_BoxMonIconScrollOut;
        }
    }
}

static void SpriteCB_BoxMonIconScrollIn(struct Sprite *sprite)
{
    if (sprite->sDistance != 0)
    {
        // Icon moving
        sprite->sDistance--;
        sprite->x += sprite->sSpeed;
        sprite->invisible = (sprite->x < OPC_ICON_CLIP_X); // Orchid: not over the info panel
    }
    else
    {
        // Icon arrived
        sStorage->iconScrollNumIncoming--;
        sprite->x = sprite->sScrollInDestX;
        sprite->invisible = FALSE;
        sprite->callback = SpriteCallbackDummy;
    }
}

static void SpriteCB_BoxMonIconScrollOut(struct Sprite *sprite)
{
    if (sprite->sDelay != 0)
    {
        sprite->sDelay--;
    }
    else
    {
        // Icon moving
        sprite->x += sprite->sSpeed;
        sprite->sScrollOutX = sprite->x + sprite->x2;
        sprite->invisible = (sprite->sScrollOutX < OPC_ICON_CLIP_X); // Orchid: not over the info panel

        // Check if icon offscreen
        if (sprite->sScrollOutX <= 68 || sprite->sScrollOutX >= 252)
            sprite->callback = SpriteCallbackDummy;
    }
}

// Sprites for Pokémon icons are destroyed during
// the box scroll once they've gone offscreen
static void DestroyBoxMonIconsInColumn(u8 column)
{
    u16 row;
    u8 boxPosition = column;

    for (row = 0; row < IN_BOX_ROWS; row++)
    {
        if (sStorage->boxMonsSprites[boxPosition] != NULL)
        {
            DestroyBoxMonIcon(sStorage->boxMonsSprites[boxPosition]);
            sStorage->boxMonsSprites[boxPosition] = NULL;
        }
        boxPosition += IN_BOX_COLUMNS;
    }
}

// Create the appearing icons for the incoming scrolling box
static u8 CreateBoxMonIconsInColumn(u8 column, u16 distance, s16 speed)
{
    s32 i;
    u16 y = OPC_SLOT_Y0 + OPC_ICON_DY;
    s16 xDest = 8 * (3 * column) + OPC_SLOT_X0;
    u16 x = xDest - ((distance + 1) * speed);
    u8 subpriority = 19 - column;
    u8 iconsCreated = 0;
    u8 boxPosition = column;

    for (i = 0; i < IN_BOX_ROWS; i++)
    {
        if (sStorage->boxSpecies[boxPosition] != SPECIES_NONE)
        {
            sStorage->boxMonsSprites[boxPosition] = CreateMonIconSprite(sStorage->boxSpecies[boxPosition],
                                                                        sStorage->boxPersonalities[boxPosition],
                                                                        x, y, 2, subpriority,
                                                                        sStorage->boxIsEgg[boxPosition]);
            if (sStorage->boxMonsSprites[boxPosition] != NULL)
            {
                sStorage->boxMonsSprites[boxPosition]->sDistance = distance;
                sStorage->boxMonsSprites[boxPosition]->sSpeed = speed;
                sStorage->boxMonsSprites[boxPosition]->sScrollInDestX = xDest;
                sStorage->boxMonsSprites[boxPosition]->callback = SpriteCB_BoxMonIconScrollIn;
                if (ShouldBoxmonSpriteBeTransparent(sStorage->incomingBoxId, boxPosition))
                    sStorage->boxMonsSprites[boxPosition]->oam.objMode = ST_OAM_OBJ_BLEND;
                iconsCreated++;
            }
        }
        boxPosition += IN_BOX_COLUMNS;
        y += 24;
    }

    return iconsCreated;
}

#undef sDistance
#undef sSpeed
#undef sScrollInDestX
#undef sDelay
#undef sScrollOutX

static void InitBoxMonIconScroll(u8 boxId, s8 direction)
{
    sStorage->iconScrollState = 0;
    sStorage->iconScrollDirection = direction;
    sStorage->iconScrollDistance = 32;
    sStorage->iconScrollSpeed = -(6 * direction);
    sStorage->iconScrollNumIncoming = 0;
    GetIncomingBoxMonData(boxId);
    if (direction > 0)
        sStorage->iconScrollCurColumn = 0;
    else
        sStorage->iconScrollCurColumn = IN_BOX_COLUMNS - 1;

    sStorage->iconScrollPos = (24 * sStorage->iconScrollCurColumn) + 100;
    StartBoxMonIconsScrollOut(sStorage->iconScrollSpeed);
}

static bool8 UpdateBoxMonIconScroll(void)
{
    if (sStorage->iconScrollDistance != 0)
        sStorage->iconScrollDistance--;

    switch (sStorage->iconScrollState)
    {
    case 0:
        sStorage->iconScrollPos += sStorage->iconScrollSpeed;
        if (sStorage->iconScrollPos <= 64 || sStorage->iconScrollPos >= 252)
        {
            // A column of icons has gone offscreen, destroy them
            DestroyBoxMonIconsInColumn(sStorage->iconScrollCurColumn);
            sStorage->iconScrollPos += sStorage->iconScrollDirection * 24;
            sStorage->iconScrollState++;
        }
        break;
    case 1:
        // Create the new incoming column of icons
        sStorage->iconScrollPos += sStorage->iconScrollSpeed;
        sStorage->iconScrollNumIncoming += CreateBoxMonIconsInColumn(sStorage->iconScrollCurColumn, sStorage->iconScrollDistance, sStorage->iconScrollSpeed);

        if ((sStorage->iconScrollDirection > 0 && sStorage->iconScrollCurColumn == IN_BOX_COLUMNS - 1)
         || (sStorage->iconScrollDirection < 0 && sStorage->iconScrollCurColumn == 0))
        {
            // Scroll has reached final column
            sStorage->iconScrollState++;
        }
        else
        {
            // Continue scrolling
            sStorage->iconScrollCurColumn += sStorage->iconScrollDirection;
            sStorage->iconScrollState = 0;
        }
        break;
    case 2:
        // Wait to make sure all icons have arrived
        if (sStorage->iconScrollNumIncoming == 0)
        {
            sStorage->iconScrollDistance++;
            return FALSE;
        }
        break;
    default:
        return FALSE;
    }

    return TRUE;
}

static void GetIncomingBoxMonData(u8 boxId)
{
    s32 i, j, boxPosition;

    boxPosition = 0;
    for (i = 0; i < IN_BOX_ROWS; i++)
    {
        for (j = 0; j < IN_BOX_COLUMNS; j++)
        {
            sStorage->boxSpecies[boxPosition] = GetBoxMonDataAt(boxId, boxPosition, MON_DATA_SPECIES);
            sStorage->boxIsEgg[boxPosition] = GetBoxMonDataAt(boxId, boxPosition, MON_DATA_IS_EGG);
            if (sStorage->boxSpecies[boxPosition] != SPECIES_NONE)
                sStorage->boxPersonalities[boxPosition] = GetBoxMonDataAt(boxId, boxPosition, MON_DATA_PERSONALITY);
            boxPosition++;
        }
    }

    sStorage->incomingBoxId = boxId;
}

static void DestroyBoxMonIconAtPosition(u8 boxPosition)
{
    if (sStorage->boxMonsSprites[boxPosition] != NULL)
    {
        DestroyBoxMonIcon(sStorage->boxMonsSprites[boxPosition]);
        sStorage->boxMonsSprites[boxPosition] = NULL;
    }
}

static void SetBoxMonIconObjMode(u8 boxPosition, u8 objMode)
{
    if (sStorage->boxMonsSprites[boxPosition] != NULL)
        sStorage->boxMonsSprites[boxPosition]->oam.objMode = objMode;
}

static void  CreatePartyMonSprite(u8 partyPosition, bool8 visible)
{
    struct Pokemon *partyPokemon = &gParties[B_TRAINER_PLAYER][partyPosition];

    enum Species species = GetMonData(partyPokemon, MON_DATA_SPECIES);
    bool32 isEgg = GetMonData(partyPokemon, MON_DATA_IS_EGG);
    u32 personality = GetMonData(partyPokemon, MON_DATA_PERSONALITY);

    s16 x, y;

    OrchidPC_PartyIconPos(partyPosition, &x, &y);
    sStorage->partySprites[partyPosition] = CreateMonIconSprite(species, personality, x, y, 1, 12, isEgg);

    struct Sprite *partySprite = sStorage->partySprites[partyPosition];

    if (partySprite == NULL)
        return;
    if (!visible)
    {
        // Orchid: the panel slides up from the bottom, the icons with it
        partySprite->y += OPC_PANEL_SLIDE * 8;
        partySprite->invisible = TRUE;
    }

    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        if (partySprite != NULL && GetMonData(partyPokemon, MON_DATA_HELD_ITEM) == ITEM_NONE)
            partySprite->oam.objMode = ST_OAM_OBJ_BLEND;
    }

    if (sStorage->boxOption == OPTION_SELECT_MON)
    {
        if (partySprite != NULL && IsBoxMonExcluded(&(partyPokemon->box)))
            partySprite->oam.objMode = ST_OAM_OBJ_BLEND;
    }
}

static void CreatePartyMonsSprites(bool8 visible)
{
    u16 i;
    enum Species species;
    bool32 isEgg;
    u32 personality;
    s16 x, y;

    for (i = 0; i < PARTY_SIZE; i++)
    {
        species = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES);
        isEgg = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_IS_EGG);
        sStorage->partySprites[i] = NULL;
        if (species != SPECIES_NONE)
        {
            personality = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_PERSONALITY);
            OrchidPC_PartyIconPos(i, &x, &y);
            sStorage->partySprites[i] = CreateMonIconSprite(species, personality, x, y, 1, 12, isEgg);
            if (sStorage->partySprites[i] != NULL && !visible)
            {
                // Orchid: the panel slides up from the bottom, the icons with it
                sStorage->partySprites[i]->y += OPC_PANEL_SLIDE * 8;
                sStorage->partySprites[i]->invisible = TRUE;
            }
        }
    }

    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        for (i = 0; i < PARTY_SIZE; i++)
        {
            if (sStorage->partySprites[i] != NULL && GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_HELD_ITEM) == ITEM_NONE)
                sStorage->partySprites[i]->oam.objMode = ST_OAM_OBJ_BLEND;
        }
    }

    if (sStorage->boxOption == OPTION_SELECT_MON)
    {
        for (i = 0; i < PARTY_SIZE; i++)
        {
            if (sStorage->partySprites[i] != NULL && IsBoxMonExcluded(&(gParties[B_TRAINER_PLAYER][i].box)))
                sStorage->partySprites[i]->oam.objMode = ST_OAM_OBJ_BLEND;
        }
    }
}

static void CompactPartySprites(void)
{
    u16 i, targetSlot;

    sStorage->numPartyToCompact = 0;
    for (i = 0, targetSlot = 0; i < PARTY_SIZE; i++)
    {
        if (sStorage->partySprites[i] != NULL)
        {
            if (i != targetSlot)
            {
                MovePartySpriteToNextSlot(sStorage->partySprites[i], targetSlot);
                sStorage->partySprites[i] = NULL;
                sStorage->numPartyToCompact++;
            }
            targetSlot++;
        }
    }
}

static u8 GetNumPartySpritesCompacting(void)
{
    return sStorage->numPartyToCompact;
}

#define sPartyId   data[1]
#define sMonX      data[2]
#define sMonY      data[3]
#define sSpeedX    data[4]
#define sSpeedY    data[5]
#define sMoveSteps data[6]

static void MovePartySpriteToNextSlot(struct Sprite *sprite, u16 partyId)
{
    s16 x, y;

    sprite->sPartyId = partyId;
    OrchidPC_PartyIconPos(partyId, &x, &y);

    sprite->sMonX = (u16)(sprite->x) * 8;
    sprite->sMonY = (u16)(sprite->y) * 8;
    sprite->sSpeedX = ((x * 8) - sprite->sMonX) / 8;
    sprite->sSpeedY = ((y * 8) - sprite->sMonY) / 8;
    sprite->sMoveSteps = 8;
    sprite->callback = SpriteCB_MovePartyMonToNextSlot;
}

static void SpriteCB_MovePartyMonToNextSlot(struct Sprite *sprite)
{
    if (sprite->sMoveSteps != 0)
    {
        s16 x = sprite->sMonX += sprite->sSpeedX;
        s16 y = sprite->sMonY += sprite->sSpeedY;
        sprite->x = x / 8u;
        sprite->y = y / 8u;
        sprite->sMoveSteps--;
    }
    else
    {
        s16 x, y;

        OrchidPC_PartyIconPos(sprite->sPartyId, &x, &y);
        sprite->x = x;
        sprite->y = y;
        sprite->callback = SpriteCallbackDummy;
        sStorage->partySprites[sprite->sPartyId] = sprite;
        sStorage->numPartyToCompact--;
    }
}

#undef sPartyId
#undef sMonX
#undef sMonY
#undef sSpeedX
#undef sSpeedY
#undef sMoveSteps

static void DestroyMovingMonIcon(void)
{
    if (sStorage->movingMonSprite != NULL)
    {
        DestroyBoxMonIcon(sStorage->movingMonSprite);
        sStorage->movingMonSprite = NULL;
    }
}

static void MovePartySprites(s16 yDelta)
{
    u16 i;

    for (i = 0; i < PARTY_SIZE; i++)
    {
        if (sStorage->partySprites[i] != NULL)
        {
            sStorage->partySprites[i]->y += yDelta;
            // Orchid: hidden while the icon's top edge is below the screen
            sStorage->partySprites[i]->invisible = (sStorage->partySprites[i]->y + sStorage->partySprites[i]->centerToCornerVecY >= DISPLAY_HEIGHT);
        }
    }
}

static void DestroyPartyMonIcon(u8 partyId)
{
    if (sStorage->partySprites[partyId] != NULL)
    {
        DestroyBoxMonIcon(sStorage->partySprites[partyId]);
        sStorage->partySprites[partyId] = NULL;
    }
}

static void DestroyAllPartyMonIcons(void)
{
    u16 i;

    for (i = 0; i < PARTY_SIZE; i++)
    {
        if (sStorage->partySprites[i] != NULL)
        {
            DestroyBoxMonIcon(sStorage->partySprites[i]);
            sStorage->partySprites[i] = NULL;
        }
    }
}

static void SetPartyMonIconObjMode(u8 partyId, u8 objMode)
{
    if (sStorage->partySprites[partyId] != NULL)
    {
        sStorage->partySprites[partyId]->oam.objMode = objMode;
    }
}

static void SetMovingMonSprite(u8 mode, u8 id)
{
    if (mode == MODE_PARTY)
    {
        sStorage->movingMonSprite = sStorage->partySprites[id];
        sStorage->partySprites[id] = NULL;
    }
    else if (mode == MODE_BOX)
    {
        sStorage->movingMonSprite = sStorage->boxMonsSprites[id];
        sStorage->boxMonsSprites[id] = NULL;
    }
    else
    {
        return;
    }

    sStorage->movingMonSprite->callback = SpriteCB_HeldMon;
    sStorage->movingMonSprite->oam.priority = GetMonIconPriorityByCursorPos();
    sStorage->movingMonSprite->subpriority = 7;
}

static void SetPlacedMonSprite(u8 boxId, u8 position)
{
    if (boxId == TOTAL_BOXES_COUNT) // party mon
    {
        sStorage->partySprites[position] = sStorage->movingMonSprite;
        sStorage->partySprites[position]->oam.priority = 1;
        sStorage->partySprites[position]->subpriority = 12;
    }
    else
    {
        sStorage->boxMonsSprites[position] = sStorage->movingMonSprite;
        sStorage->boxMonsSprites[position]->oam.priority = 2;
        sStorage->boxMonsSprites[position]->subpriority = 19 - (position % IN_BOX_COLUMNS);
    }
    sStorage->movingMonSprite->callback = SpriteCallbackDummy;
    sStorage->movingMonSprite = NULL;
}

static void SaveMonSpriteAtPos(u8 boxId, u8 position)
{
    if (boxId == TOTAL_BOXES_COUNT) // party mon
        sStorage->shiftMonSpritePtr = &sStorage->partySprites[position];
    else
        sStorage->shiftMonSpritePtr = &sStorage->boxMonsSprites[position];

    sStorage->movingMonSprite->callback = SpriteCallbackDummy;
    sStorage->shiftTimer = 0;
}

// Orchid: the held Pokémon sinks into the slot while the one there rises to the held height
static bool8 MoveShiftingMons(void)
{
    s32 rise;
    s16 restY;

    if (sStorage->shiftTimer == 16)
        return FALSE;

    sStorage->shiftTimer++;
    restY = sStorage->cursorSprite->y + OPC_ICON_DY;
    rise = sStorage->shiftTimer * OPC_LIFT / 16;
    (*sStorage->shiftMonSpritePtr)->y = restY - rise;
    sStorage->movingMonSprite->y = restY - (OPC_LIFT - rise);

    (*sStorage->shiftMonSpritePtr)->x2 = gSineTable[sStorage->shiftTimer * 8] / 16;
    sStorage->movingMonSprite->x2 = -(gSineTable[sStorage->shiftTimer * 8] / 16);
    if (sStorage->shiftTimer == 8)
    {
        sStorage->movingMonSprite->oam.priority = (*sStorage->shiftMonSpritePtr)->oam.priority;
        sStorage->movingMonSprite->subpriority = (*sStorage->shiftMonSpritePtr)->subpriority;
        (*sStorage->shiftMonSpritePtr)->oam.priority = GetMonIconPriorityByCursorPos();
        (*sStorage->shiftMonSpritePtr)->subpriority = 7;
    }

    if (sStorage->shiftTimer == 16)
    {
        struct Sprite *sprite = sStorage->movingMonSprite;
        sStorage->movingMonSprite = (*sStorage->shiftMonSpritePtr);
        *sStorage->shiftMonSpritePtr = sprite;

        sStorage->movingMonSprite->callback = SpriteCB_HeldMon;
        (*sStorage->shiftMonSpritePtr)->callback = SpriteCallbackDummy;
        sStorage->opcLift = OPC_LIFT;
    }

    return TRUE;
}

static void SetReleaseMon(u8 mode, u8 position)
{
    switch (mode)
    {
    case MODE_PARTY:
        sStorage->releaseMonSpritePtr = &sStorage->partySprites[position];
        break;
    case MODE_BOX:
        sStorage->releaseMonSpritePtr = &sStorage->boxMonsSprites[position];
        break;
    case MODE_MOVE:
        sStorage->releaseMonSpritePtr = &sStorage->movingMonSprite;
        break;
    default:
        return;
    }

    if (*sStorage->releaseMonSpritePtr != NULL)
    {
        InitSpriteAffineAnim(*sStorage->releaseMonSpritePtr);
        (*sStorage->releaseMonSpritePtr)->oam.affineMode = ST_OAM_AFFINE_NORMAL;
        (*sStorage->releaseMonSpritePtr)->affineAnims = sAffineAnims_ReleaseMon;
        StartSpriteAffineAnim(*sStorage->releaseMonSpritePtr, RELEASE_ANIM_RELEASE);
    }
}

static bool8 TryHideReleaseMonSprite(void)
{
    if (*sStorage->releaseMonSpritePtr == NULL
    || (*sStorage->releaseMonSpritePtr)->invisible)
        return FALSE;

    if ((*sStorage->releaseMonSpritePtr)->affineAnimEnded)
        (*sStorage->releaseMonSpritePtr)->invisible = TRUE;

    return TRUE;
}

static void DestroyReleaseMonIcon(void)
{
    if (*sStorage->releaseMonSpritePtr != NULL)
    {
        FreeOamMatrix((*sStorage->releaseMonSpritePtr)->oam.matrixNum);
        DestroyBoxMonIcon(*sStorage->releaseMonSpritePtr);
        *sStorage->releaseMonSpritePtr = NULL;
    }
}

static void ReshowReleaseMon(void)
{
    if (*sStorage->releaseMonSpritePtr != NULL)
    {
        (*sStorage->releaseMonSpritePtr)->invisible = FALSE;
        StartSpriteAffineAnim(*sStorage->releaseMonSpritePtr, RELEASE_ANIM_CAME_BACK);
    }
}

static bool8 ResetReleaseMonSpritePtr(void)
{
    if (sStorage->releaseMonSpritePtr == NULL)
        return FALSE;

    if ((*sStorage->releaseMonSpritePtr)->affineAnimEnded)
        sStorage->releaseMonSpritePtr = NULL;

    return TRUE;
}

static void SetMovingMonPriority(u8 priority)
{
    sStorage->movingMonSprite->oam.priority = GetMonIconPriorityByCursorPos();
}

// Orchid: the held Pokémon floats OPC_LIFT px above the ring with a 1 px bob every 16 frames
static void SpriteCB_HeldMon(struct Sprite *sprite)
{
    s32 bob = 0;

    if (sStorage->opcLift == OPC_LIFT)
        bob = (++sStorage->opcBobTimer / OPC_BOB_PERIOD) & 1;
    else
        sStorage->opcBobTimer = 0;
    sprite->x = sStorage->cursorSprite->x;
    sprite->y = sStorage->cursorSprite->y + OPC_ICON_DY - sStorage->opcLift - bob;
}

static u32 MakeIconIdFromSpeciesAndIconType(enum Species species, enum SpeciesIconType iconType)
{
    if (iconType == FEMALE_ICON)
        return (species | (1 << 15));
    if (iconType == EGG_ICON)
        return (species | (1 << 14));
    return species;
}

static u16 TryLoadMonIconTiles(enum Species species, enum SpeciesIconType iconType)
{
    u32 i, offset;
    u32 iconId = MakeIconIdFromSpeciesAndIconType(species, iconType);

    for (i = 0; i < MAX_MON_ICONS; i++)
    {
        if (sStorage->iconSpeciesList[i] == iconId)
            break;
    }

    if (i == MAX_MON_ICONS)
    {
        // Species not present in the list
        // Find first empty spot in the list to put it
        for (i = 0; i < MAX_MON_ICONS; i++)
        {
            if (sStorage->iconSpeciesList[i] == 0)
                break;
        }

        // Failed to find an empty spot
        if (i == MAX_MON_ICONS)
            return 0xFFFF;
    }

    // Add species to icon list and load tiles
    sStorage->iconSpeciesList[i] = iconId;
    sStorage->numIconsPerSpecies[i]++;
    offset = 16 * i;
    species &= SPECIES_MASK;
    CpuCopy32(GetMonIconTilesByIconType(species, iconType), (void *)(OBJ_VRAM0) + offset * TILE_SIZE_4BPP, 0x200);

    return offset;
}

static void RemoveSpeciesFromIconList(enum Species species, enum SpeciesIconType iconType)
{
    u32 iconId = MakeIconIdFromSpeciesAndIconType(species, iconType);

    for (u32 i = 0; i < MAX_MON_ICONS; i++)
    {
        if (sStorage->iconSpeciesList[i] == iconId)
        {
            if (--sStorage->numIconsPerSpecies[i] == 0)
                sStorage->iconSpeciesList[i] = SPECIES_NONE;
            break;
        }
    }
}

static struct Sprite *CreateMonIconSprite(enum Species species, u32 personality, s16 x, s16 y, u8 oamPriority, u8 subpriority, bool32 isEgg)
{
    u16 tileNum;
    u8 spriteId;
    struct SpriteTemplate template = sSpriteTemplate_MonIcon;
    u32 iconType = NORMAL_ICON;

    species = GetIconSpecies(species, personality);
    if (isEgg)
    {
        if (gSpeciesInfo[species].eggId != EGG_ID_NONE)
        {
            template.paletteTag = PALTAG_MON_ICON_0 + gEggDatas[gSpeciesInfo[species].eggId].eggIconPalIndex;
            iconType = EGG_ICON;
        }
        else
        {
            species = SPECIES_EGG;
            template.paletteTag = PALTAG_MON_ICON_0 + gSpeciesInfo[SPECIES_EGG].iconPalIndex;
        }
    }
#if P_GENDER_DIFFERENCES
    else if (gSpeciesInfo[species].iconSpriteFemale != NULL && IsPersonalityFemale(species, personality))
    {
        template.paletteTag = PALTAG_MON_ICON_0 + gSpeciesInfo[species].iconPalIndexFemale;
        iconType = FEMALE_ICON;
    }
#endif
    else
    {
        template.paletteTag = PALTAG_MON_ICON_0 + gSpeciesInfo[species].iconPalIndex;
    }

    tileNum = TryLoadMonIconTiles(species, iconType);
    if (tileNum == 0xFFFF)
        return NULL;

    spriteId = CreateSpriteUnchecked(&template, x, y, subpriority);
    if (spriteId == MAX_SPRITES)
    {
        RemoveSpeciesFromIconList(species, iconType);
        return NULL;
    }

    gSprites[spriteId].oam.tileNum = tileNum;
    gSprites[spriteId].oam.priority = oamPriority;
    gSprites[spriteId].data[0] = species;
    gSprites[spriteId].data[1] = iconType;

    return &gSprites[spriteId];
}

static void DestroyBoxMonIcon(struct Sprite *sprite)
{
    RemoveSpeciesFromIconList(sprite->data[0], sprite->data[1]);
    DestroySprite(sprite);
}


//------------------------------------------------------------------------------
//  SECTION: General box
//
//  Some basic box functions, including initializing the box and scrolling.
//------------------------------------------------------------------------------


#define tState  data[0]
#define tDmaIdx data[1]
#define tBoxId  data[2]

static void CreateInitBoxTask(u8 boxId)
{
    u8 taskId = CreateTask(Task_InitBox, 2);

    gTasks[taskId].tBoxId = boxId;
}

static bool8 IsInitBoxActive(void)
{
    return FuncIsActiveTask(Task_InitBox);
}

static void Task_InitBox(u8 taskId)
{
    struct Task *task = &gTasks[taskId];

    switch (task->tState)
    {
    case 0:
        sStorage->wallpaperOffset = 0;
        sStorage->bg2_X = 0;
        task->tDmaIdx = RequestDma3Fill(0, sStorage->wallpaperBgTilemapBuffer, sizeof(sStorage->wallpaperBgTilemapBuffer), 1);
        break;
    case 1:
        if (CheckForSpaceForDma3Request(task->tDmaIdx) == -1)
            return;

        SetBgTilemapBuffer(2, sStorage->wallpaperBgTilemapBuffer);
        ShowBg(2);
        break;
    case 2:
        LoadWallpaperGfx(task->tBoxId, 0);
        break;
    case 3:
        if (!WaitForWallpaperGfxLoad())
            return;

        InitBoxTitle(task->tBoxId);
        CreateBoxScrollArrows();
        InitBoxMonSprites(task->tBoxId);
        SetGpuReg(REG_OFFSET_BG2CNT, BGCNT_PRIORITY(2) | BGCNT_CHARBASE(3) | BGCNT_SCREENBASE(27) | BGCNT_TXT512x256);
        break;
    case 4:
        DestroyTask(taskId);
        break;
    default:
        task->tState = 0;
        return;
    }

    task->tState++;
}

#undef tState
#undef tDmaIdx
#undef tBoxId

static void SetUpScrollToBox(u8 boxId)
{
    s8 direction = DetermineBoxScrollDirection(boxId);

    sStorage->scrollSpeed = (direction > 0) ? 6 : -6;
    sStorage->scrollTimer = 32;

    sStorage->scrollToBoxId = boxId;
    sStorage->scrollDirection = direction;
    sStorage->scrollState = 0;
}

static bool8 ScrollToBox(void)
{
    bool8 iconsScrolling;

    switch (sStorage->scrollState)
    {
    case 0:
        LoadWallpaperGfx(sStorage->scrollToBoxId, sStorage->scrollDirection);
        sStorage->scrollState++;
    case 1:
        if (!WaitForWallpaperGfxLoad())
            return TRUE;

        InitBoxMonIconScroll(sStorage->scrollToBoxId, sStorage->scrollDirection);
        CreateIncomingBoxTitle(sStorage->scrollToBoxId, sStorage->scrollDirection);
        StartBoxScrollArrowsSlide(sStorage->scrollDirection);
        // Orchid: the ring hides during the slide and comes back on the same slot
        sStorage->opcRingHidden = TRUE;
        OrchidPC_UpdateRing();
        OrchidPC_DestroyHoldTags();
        break;
    case 2:
        iconsScrolling = UpdateBoxMonIconScroll();
        if (sStorage->scrollTimer != 0)
        {
            sStorage->bg2_X += sStorage->scrollSpeed;
            // Orchid: the title tab switches to the incoming box at the halfway point
            if (--sStorage->scrollTimer == 16)
                OrchidPC_PrintTitle(sStorage->scrollToBoxId);
            if (sStorage->scrollTimer != 0)
                return TRUE;
            CycleBoxTitleSprites();
            StopBoxScrollArrowsSlide();
        }
        return iconsScrolling;
    }

    sStorage->scrollState++;
    return TRUE;
}

static s8 DetermineBoxScrollDirection(u8 boxId)
{
    u8 i;
    u8 currentBox = StorageGetCurrentBox();

    for (i = 0; currentBox != boxId; i++)
    {
        currentBox++;
        if (currentBox >= TOTAL_BOXES_COUNT)
            currentBox = 0;
    }

    return (i < TOTAL_BOXES_COUNT / 2) ? 1 : -1;
}


//------------------------------------------------------------------------------
//  SECTION: Wallpaper gfx
//------------------------------------------------------------------------------


// Orchid: a box is 30 slot recesses on BG2 in its box colour (BG palette 8 / 9, alternating per slide
// like vanilla's wallpaperOffset). The incoming box is drawn 24 tiles along the 512 px map.
static void LoadWallpaperGfx(u8 boxId, s8 direction)
{
    s32 curCol0 = ((sStorage->bg2_X / 8) + OPC_SLOT_COL0) & 63;
    s32 col0 = (curCol0 + direction * OPC_BOX_SLIDE_TILES) & 63;
    u8 bgPal;

    sStorage->wallpaperLoadBoxId = boxId;
    sStorage->wallpaperLoadDir = direction;
    if (direction != 0)
        sStorage->wallpaperOffset = (sStorage->wallpaperOffset == 0);
    bgPal = OPC_BG_BOX + sStorage->wallpaperOffset;

    OrchidPC_LoadBoxColour(OrchidPC_GetBoxColour(boxId), bgPal);
    OrchidPC_ClearBoxSlotsExcept(curCol0, direction != 0);
    OrchidPC_DrawBoxSlots(col0, bgPal);
    CopyBgTilemapBufferToVram(2);
}

static bool32 WaitForWallpaperGfxLoad(void)
{
    if (IsDma3ManagerBusyWithBgCopy())
        return FALSE;

    return TRUE;
}


//------------------------------------------------------------------------------
//  SECTION: Box Title
//------------------------------------------------------------------------------


// Orchid: the title is BG1 text on the title tab (OrchidPC_PrintTitle); during a box slide it switches to
// the incoming box at the halfway point (ScrollToBox) instead of sliding.
static void InitBoxTitle(u8 boxId)
{
    OrchidPC_PrintTitle(boxId);
}

static void CreateIncomingBoxTitle(u8 boxId, s8 direction)
{
}

static void CycleBoxTitleSprites(void)
{
}


//------------------------------------------------------------------------------
//  SECTION: Scroll arrows
//------------------------------------------------------------------------------


// Orchid: two small red chevrons either side of the title tab. A box switch lights the one in the
// direction of travel for 8 frames, nudged 2 px outward (anim_pc.box_switch_gif).
#define sLitTimer data[0]
#define sSide     data[1]

static void CreateBoxScrollArrows(void)
{
    u16 i;

    LoadSpriteSheet(&sSpriteSheet_Arrow);
    for (i = 0; i < 2; i++)
    {
        u8 spriteId = CreateSpriteUnchecked(&sSpriteTemplate_Arrow, i == 0 ? OPC_CHEV_L_X : OPC_CHEV_R_X, OPC_CHEV_Y, 22);
        sStorage->arrowSprites[i] = NULL;
        if (spriteId != MAX_SPRITES)
        {
            struct Sprite *sprite = &gSprites[spriteId];
            StartSpriteAnim(sprite, i);
            sprite->oam.priority = 1;
            sprite->sSide = i;
            sprite->sLitTimer = 0;
            sStorage->arrowSprites[i] = sprite;
        }
    }
}

static void LightChevron(struct Sprite *sprite)
{
    if (sprite == NULL)
        return;
    sprite->sLitTimer = OPC_CHEV_LIT_FRAMES;
    StartSpriteAnim(sprite, 2 + sprite->sSide);
    sprite->x2 = sprite->sSide == 0 ? -OPC_CHEV_LIT_DX : OPC_CHEV_LIT_DX;
}

static void StartBoxScrollArrowsSlide(s8 direction)
{
    LightChevron(sStorage->arrowSprites[direction > 0 ? 1 : 0]);
}

static void StopBoxScrollArrowsSlide(void)
{
}

static void AnimateBoxScrollArrows(bool8 animate)
{
}

static void SpriteCB_Arrow(struct Sprite *sprite)
{
    if (sprite->sLitTimer != 0 && --sprite->sLitTimer == 0)
    {
        StartSpriteAnim(sprite, sprite->sSide);
        sprite->x2 = 0;
    }
}

// Chevrons either side of the jump / deposit popup's box name
static struct Sprite *CreateChooseBoxArrows(u16 x, u16 y, u8 animId, u8 priority, u8 subpriority)
{
    u8 spriteId = CreateSpriteUnchecked(&sSpriteTemplate_Arrow, x, y, subpriority);
    if (spriteId == MAX_SPRITES)
        return NULL;

    animId %= 2;
    StartSpriteAnim(&gSprites[spriteId], animId);
    gSprites[spriteId].oam.priority = priority;
    gSprites[spriteId].sSide = animId;
    gSprites[spriteId].sLitTimer = 0;
    return &gSprites[spriteId];
}

#undef sLitTimer
#undef sSide


//------------------------------------------------------------------------------
//  SECTION: Cursor movement
//
//  The functions below generally handle the cursor's movement, including
//  moving around the box and picking up/putting down Pokémon.
//------------------------------------------------------------------------------


static void InitCursor(void)
{
    if (sStorage->boxOption != OPTION_DEPOSIT)
        sCursorArea = CURSOR_AREA_IN_BOX;
    else
        sCursorArea = CURSOR_AREA_IN_PARTY;

    sCursorPosition = 0;
    sIsMonBeingMoved = FALSE;
    sMovingMonOrigBoxId = 0;
    sMovingMonOrigBoxPos = 0;
    sAutoActionOn = FALSE;
    ClearSavedCursorPos();
    CreateCursorSprites();
    sStorage->cursorPrevHorizPos = 1;
    sStorage->inBoxMovingMode = MOVE_MODE_NORMAL;
    TryRefreshDisplayMon();
}

static void InitCursorOnReopen(void)
{
    CreateCursorSprites();
    ReshowDisplayMon();
    sStorage->cursorPrevHorizPos = 1;
    sStorage->inBoxMovingMode = MOVE_MODE_NORMAL;
    if (sIsMonBeingMoved)
    {
        sStorage->movingMon = sSavedMovingMon;
        CreateMovingMonIcon();
    }
}

static void GetCursorCoordsByPos(u8 cursorArea, u8 cursorPosition, u16 *x, u16 *y)
{
    // Orchid: the cursor is the gold ring around a slot; its position is the slot centre. On the title tab
    // and the buttons (no ring, the art turns gold) it is where a held Pokémon floats (centre + lift).
    switch (cursorArea)
    {
    case CURSOR_AREA_IN_BOX:
        *x = (cursorPosition % IN_BOX_COLUMNS) * OPC_SLOT_PITCH + OPC_SLOT_X0;
        *y = (cursorPosition / IN_BOX_COLUMNS) * OPC_SLOT_PITCH + OPC_SLOT_Y0;
        break;
    case CURSOR_AREA_IN_PARTY:
        if (cursorPosition >= PARTY_SIZE)
        {
            *x = OPC_PCANCEL_X;
            *y = OPC_PCANCEL_Y;
        }
        else
        {
            *x = OPC_PSLOT_X0 + OPC_PSLOT_DX * (cursorPosition % 2) + OPC_PICON_DX;
            *y = OPC_PSLOT_Y0 + OPC_PSLOT_DY * (cursorPosition / 2) + OPC_PICON_DY;
        }
        break;
    case CURSOR_AREA_BOX_TITLE:
        *x = OPC_TAB_X + OPC_TAB_W / 2;
        *y = 16 - OPC_ICON_DY + OPC_LIFT;
        break;
    case CURSOR_AREA_BUTTONS:
        *y = 12 - OPC_ICON_DY + OPC_LIFT;
        *x = cursorPosition * 80 + 124;
        break;
    case 4:
        *x = 160;
        *y = 96;
        break;
    }
}

static u16 GetSpeciesAtCursorPosition(void)
{
    switch (sCursorArea)
    {
    case CURSOR_AREA_IN_PARTY:
        return GetMonData(&gParties[B_TRAINER_PLAYER][sCursorPosition], MON_DATA_SPECIES);
    case CURSOR_AREA_IN_BOX:
        return GetCurrentBoxMonData(sCursorPosition, MON_DATA_SPECIES);
    default:
        return SPECIES_NONE;
    }
}

static bool8 UpdateCursorPos(void)
{
    s16 tmp;

    if (sStorage->cursorMoveSteps == 0)
    {
        if (sStorage->boxOption != OPTION_MOVE_ITEMS)
            return FALSE;
        else
            return IsItemIconAnimActive();
    }
    else if (--sStorage->cursorMoveSteps != 0)
    {
        // Update position toward target
        sStorage->cursorNewX += sStorage->cursorSpeedX;
        sStorage->cursorNewY += sStorage->cursorSpeedY;
        sStorage->cursorSprite->x = sStorage->cursorNewX >> 8;
        sStorage->cursorSprite->y = sStorage->cursorNewY >> 8;

        // Limit cursor on right
        if (sStorage->cursorSprite->x > DISPLAY_WIDTH + 16)
        {
            tmp = sStorage->cursorSprite->x - (DISPLAY_WIDTH + 16);
            sStorage->cursorSprite->x = tmp + 64;
        }

        // Limit cursor on left
        if (sStorage->cursorSprite->x < 64)
        {
            tmp = 64 - sStorage->cursorSprite->x;
            sStorage->cursorSprite->x = DISPLAY_WIDTH + 16 - tmp;
        }

        // Limit cursor on bottom
        if (sStorage->cursorSprite->y > DISPLAY_HEIGHT + 16)
        {
            tmp = sStorage->cursorSprite->y - (DISPLAY_HEIGHT + 16);
            sStorage->cursorSprite->y = tmp - 16;
        }

        // Limit cursor on top
        if (sStorage->cursorSprite->y < -16)
        {
            tmp = -16 - sStorage->cursorSprite->y;
            sStorage->cursorSprite->y = DISPLAY_HEIGHT + 16 - tmp;
        }

        // Cursor flips vertically when moving on/off the top buttons
        if (sStorage->cursorFlipTimer && --sStorage->cursorFlipTimer == 0)
            sStorage->cursorSprite->vFlip = (sStorage->cursorSprite->vFlip == FALSE);
    }
    else
    {
        // Time is up for cursor movement, make sure it's exactly at target
        sStorage->cursorSprite->x = sStorage->cursorTargetX;
        sStorage->cursorSprite->y = sStorage->cursorTargetY;
        DoCursorNewPosUpdate();
    }

    return TRUE;
}

static void InitNewCursorPos(u8 newCursorArea, u8 newCursorPosition)
{
    u16 x = 0, y = 0;

    GetCursorCoordsByPos(newCursorArea, newCursorPosition, &x, &y);
    sStorage->newCursorArea = newCursorArea;
    sStorage->newCursorPosition = newCursorPosition;
    sStorage->cursorTargetX = x;
    sStorage->cursorTargetY = y;
}

static void InitCursorMove(void)
{
    int yDistance, xDistance;

    if (sStorage->cursorVerticalWrap != 0 || sStorage->cursorHorizontalWrap != 0)
        sStorage->cursorMoveSteps = 12;
    else
        sStorage->cursorMoveSteps = 6;

    if (sStorage->cursorFlipTimer)
        sStorage->cursorFlipTimer = sStorage->cursorMoveSteps >> 1;

    switch (sStorage->cursorVerticalWrap)
    {
    default: // No wrap
        yDistance = sStorage->cursorTargetY - sStorage->cursorSprite->y;
        break;
    case -1: // Wrap from top to bottom
        yDistance = sStorage->cursorTargetY - 192 - sStorage->cursorSprite->y;
        break;
    case 1: // Wrap from bottom to top
        yDistance = sStorage->cursorTargetY + 192 - sStorage->cursorSprite->y;
        break;
    }

    switch (sStorage->cursorHorizontalWrap)
    {
    default: // No Wrap
        xDistance = sStorage->cursorTargetX - sStorage->cursorSprite->x;
        break;
    case -1: // Wrap from left to right
        xDistance = sStorage->cursorTargetX - 192 - sStorage->cursorSprite->x;
        break;
    case 1: // Wrap from right to left
        xDistance = sStorage->cursorTargetX + 192 - sStorage->cursorSprite->x;
        break;
    }

    yDistance <<= 8;
    xDistance <<= 8;
    sStorage->cursorSpeedX = xDistance / sStorage->cursorMoveSteps;
    sStorage->cursorSpeedY = yDistance / sStorage->cursorMoveSteps;
    sStorage->cursorNewX = sStorage->cursorSprite->x << 8;
    sStorage->cursorNewY = sStorage->cursorSprite->y << 8;
}

static void SetCursorPosition(u8 newCursorArea, u8 newCursorPosition)
{
    InitNewCursorPos(newCursorArea, newCursorPosition);
    InitCursorMove();
    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
    {
        if (sStorage->inBoxMovingMode == MOVE_MODE_NORMAL && !sIsMonBeingMoved)
            StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_STILL);
    }
    else
    {
        if (!IsMovingItem())
            StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_STILL);
    }

    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        if (sCursorArea == CURSOR_AREA_IN_BOX)
            TryHideItemIconAtPos(CURSOR_AREA_IN_BOX, sCursorPosition);
        else if (sCursorArea == CURSOR_AREA_IN_PARTY)
            TryHideItemIconAtPos(CURSOR_AREA_IN_PARTY, sCursorPosition);

        if (newCursorArea == CURSOR_AREA_IN_BOX)
            TryLoadItemIconAtPos(newCursorArea, newCursorPosition);
        else if (newCursorArea == CURSOR_AREA_IN_PARTY)
            TryLoadItemIconAtPos(newCursorArea, newCursorPosition);
    }

    if (newCursorArea == CURSOR_AREA_IN_PARTY && sCursorArea != CURSOR_AREA_IN_PARTY)
    {
        sStorage->cursorPrevHorizPos = 1;
        sStorage->cursorShadowSprite->invisible = TRUE;
    }

    switch (newCursorArea)
    {
    case CURSOR_AREA_IN_PARTY:
    case CURSOR_AREA_BOX_TITLE:
    case CURSOR_AREA_BUTTONS:
        sStorage->cursorSprite->oam.priority = 1;
        sStorage->cursorShadowSprite->invisible = TRUE;
        sStorage->cursorShadowSprite->oam.priority = 1;
        break;
    case CURSOR_AREA_IN_BOX:
        if (sStorage->inBoxMovingMode != MOVE_MODE_NORMAL)
        {
            sStorage->cursorSprite->oam.priority = 0;
            sStorage->cursorShadowSprite->invisible = TRUE;
        }
        else
        {
            sStorage->cursorSprite->oam.priority = 2;
            if (sCursorArea == CURSOR_AREA_IN_BOX && sIsMonBeingMoved)
                SetMovingMonPriority(2);
        }
        break;
    }

    // Orchid: gold art follows the cursor at once; the ring only shows between two ring places
    OrchidPC_SetSelection(newCursorArea, newCursorPosition);
    if (!OrchidPC_IsRingArea(sCursorArea, sCursorPosition) || !OrchidPC_IsRingArea(newCursorArea, newCursorPosition))
        sStorage->cursorSprite->invisible = TRUE;
    if (newCursorArea == CURSOR_AREA_IN_PARTY)
        sStorage->cursorSprite->subpriority = 10;
    else if (newCursorArea == CURSOR_AREA_IN_BOX)
        sStorage->cursorSprite->subpriority = 21;
}

static void DoCursorNewPosUpdate(void)
{
    sCursorArea = sStorage->newCursorArea;
    sCursorPosition = sStorage->newCursorPosition;
    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
    {
        if (sStorage->inBoxMovingMode == MOVE_MODE_NORMAL && !sIsMonBeingMoved)
            StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_BOUNCE);
    }
    else
    {
        if (!IsMovingItem())
            StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_BOUNCE);
    }

    TryRefreshDisplayMon();
    switch (sCursorArea)
    {
    case CURSOR_AREA_BUTTONS:
        SetMovingMonPriority(1);
        break;
    case CURSOR_AREA_BOX_TITLE:
        AnimateBoxScrollArrows(TRUE);
        break;
    case CURSOR_AREA_IN_PARTY:
        sStorage->cursorShadowSprite->subpriority = 13;
        SetMovingMonPriority(1);
        break;
    case CURSOR_AREA_IN_BOX:
        if (sStorage->inBoxMovingMode == MOVE_MODE_NORMAL)
        {
            sStorage->cursorSprite->oam.priority = 1;
            sStorage->cursorShadowSprite->oam.priority = 2;
            sStorage->cursorShadowSprite->subpriority = 21;
            sStorage->cursorShadowSprite->invisible = FALSE;
            SetMovingMonPriority(2);
        }
        break;
    }
    OrchidPC_UpdateRing();
}

static void SetCursorInParty(void)
{
    u8 partyCount;

    if (!sIsMonBeingMoved)
    {
        partyCount = 0;
    }
    else
    {
        partyCount = CalculatePlayerPartyCount();
        if (partyCount >= PARTY_SIZE)
            partyCount = PARTY_SIZE - 1;
    }
    if (sStorage->cursorSprite->vFlip)
        sStorage->cursorFlipTimer = 1;
    SetCursorPosition(CURSOR_AREA_IN_PARTY, partyCount);
}

static void SetCursorBoxPosition(u8 cursorBoxPosition)
{
    SetCursorPosition(CURSOR_AREA_IN_BOX, cursorBoxPosition);
}

EWRAM_DATA static u8 sSavedCursorPosition = 0;

static void ClearSavedCursorPos(void)
{
    sSavedCursorPosition = 0;
}

static void SaveCursorPos(void)
{
    sSavedCursorPosition = sCursorPosition;
}

static u8 GetSavedCursorPos(void)
{
    return sSavedCursorPosition;
}

static void InitMonPlaceChange(u8 type)
{
    static bool8 (*const placeChangeFuncs[])(void) =
    {
        [CHANGE_GRAB]  = MonPlaceChange_Grab,
        [CHANGE_PLACE] = MonPlaceChange_Place,
        [CHANGE_SHIFT] = MonPlaceChange_Shift,
    };

    sStorage->monPlaceChangeFunc = placeChangeFuncs[type];
    sStorage->monPlaceChangeState = 0;
}

// No Shift while moving multiple Pokémon, only grab and place
// For both grab/place, the cursor moves down, then up
static void InitMultiMonPlaceChange(bool8 up)
{
    if (!up)
        sStorage->monPlaceChangeFunc = MultiMonPlaceChange_Down;
    else
        sStorage->monPlaceChangeFunc = MultiMonPlaceChange_Up;
    sStorage->opcLiftTimer = up ? 8 : 0;

    sStorage->monPlaceChangeState = 0;
}

static bool8 DoMonPlaceChange(void)
{
    return sStorage->monPlaceChangeFunc();
}

// Orchid (anim_pc.pickup_gif): A flashes the ring and the Pokémon rises OPC_LIFT px over 8 frames (ease-out);
// putting it down sinks it over 8 frames, then it is placed and the ring flashes.
static bool8 MonPlaceChange_Grab(void)
{
    switch (sStorage->monPlaceChangeState)
    {
    case 0:
        if (sIsMonBeingMoved)
            return FALSE;
        StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_FLASH);
        sStorage->opcLift = 0;
        sStorage->opcLiftTimer = 0;
        MoveMon();
        sStorage->monPlaceChangeState++;
        break;
    case 1:
        sStorage->opcLift = sOPcLiftUp[sStorage->opcLiftTimer];
        if (++sStorage->opcLiftTimer == OPC_LIFT_FRAMES)
            sStorage->monPlaceChangeState++;
        break;
    case 2:
        return FALSE;
    }

    return TRUE;
}

static bool8 MonPlaceChange_Place(void)
{
    switch (sStorage->monPlaceChangeState)
    {
    case 0:
        sStorage->opcLiftTimer = 0;
        sStorage->monPlaceChangeState++;
        // fallthrough
    case 1:
        if (sStorage->opcLiftTimer < OPC_LIFT_FRAMES)
        {
            sStorage->opcLift = sOPcLiftDown[sStorage->opcLiftTimer++];
        }
        else
        {
            PlaceMon();
            sStorage->opcLift = OPC_LIFT;
            StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_FLASH);
            sStorage->monPlaceChangeState++;
        }
        break;
    case 2:
        return FALSE;
    }

    return TRUE;
}

static bool8 MonPlaceChange_Shift(void)
{
    switch (sStorage->monPlaceChangeState)
    {
    case 0:
        switch (sCursorArea)
        {
        case CURSOR_AREA_IN_PARTY:
            sStorage->shiftBoxId = TOTAL_BOXES_COUNT;
            break;
        case CURSOR_AREA_IN_BOX:
            sStorage->shiftBoxId = StorageGetCurrentBox();
            break;
        default:
            return FALSE;
        }
        StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_OPEN);
        SaveMonSpriteAtPos(sStorage->shiftBoxId, sCursorPosition);
        sStorage->monPlaceChangeState++;
        break;
    case 1:
        if (!MoveShiftingMons())
        {
            StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_FIST);
            SetShiftedMonData(sStorage->shiftBoxId, sCursorPosition);
            sStorage->monPlaceChangeState++;
        }
        break;
    case 2:
        return FALSE;
    }

    return TRUE;
}

static bool8 MultiMonPlaceChange_Down(void)
{
    return MonPlaceChange_CursorDown();
}

static bool8 MultiMonPlaceChange_Up(void)
{
    return MonPlaceChange_CursorUp();
}

// Orchid: the multi-move grab / place keep vanilla's 8 + 8 frame timing; the ring stays put (no hand dip)
static bool8 MonPlaceChange_CursorDown(void)
{
    if (sStorage->opcLiftTimer == 8)
        return FALSE;
    sStorage->opcLiftTimer++;
    return TRUE;
}

static bool8 MonPlaceChange_CursorUp(void)
{
    if (sStorage->opcLiftTimer == 0)
        return FALSE;
    sStorage->opcLiftTimer--;
    return TRUE;
}


//------------------------------------------------------------------------------
//  SECTION: Pokémon data
//
//  The functions below handle moving Pokémon data around while using the PC,
//  including changing the positions of Pokémon, releasing Pokémon, viewing the
//  summary screen, and updating the display of the currently selected Pokémon.
//------------------------------------------------------------------------------


static void MoveMon(void)
{
    switch (sCursorArea)
    {
    case CURSOR_AREA_IN_PARTY:
        SetMovingMonData(TOTAL_BOXES_COUNT, sCursorPosition);
        SetMovingMonSprite(MODE_PARTY, sCursorPosition);
        break;
    case CURSOR_AREA_IN_BOX:
        if (sStorage->inBoxMovingMode == MOVE_MODE_NORMAL)
        {
            SetMovingMonData(StorageGetCurrentBox(), sCursorPosition);
            SetMovingMonSprite(MODE_BOX, sCursorPosition);
        }
        break;
    default:
        return;
    }

    sIsMonBeingMoved = TRUE;
}

static void PlaceMon(void)
{
    u8 boxId;

    switch (sCursorArea)
    {
    case CURSOR_AREA_IN_PARTY:
        SetPlacedMonData(TOTAL_BOXES_COUNT, sCursorPosition);
        SetPlacedMonSprite(TOTAL_BOXES_COUNT, sCursorPosition);
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][sCursorPosition];
        UpdateSpeciesSpritePSS(&mon->box);
        break;
    case CURSOR_AREA_IN_BOX:
        boxId = StorageGetCurrentBox();
        SetPlacedMonData(boxId, sCursorPosition);
        SetPlacedMonSprite(boxId, sCursorPosition);
        UpdateSpeciesSpritePSS(&gPokemonStoragePtr->boxes[boxId][sCursorPosition]);
        break;
    default:
        return;
    }

    sIsMonBeingMoved = FALSE;
}

static void RefreshDisplayMon(void)
{
    TryRefreshDisplayMon();
}

static void SetMovingMonData(u8 boxId, u8 position)
{
    if (boxId == TOTAL_BOXES_COUNT)
    {
        sStorage->movingMon = gParties[B_TRAINER_PLAYER][sCursorPosition];
        if (&gParties[B_TRAINER_PLAYER][sCursorPosition] == GetFirstLiveMon())
            gFollowerSteps = 0;
    }
    else
    {
        BoxMonAtToMon(boxId, position, &sStorage->movingMon);
    }

    PurgeMonOrBoxMon(boxId, position);
    sMovingMonOrigBoxId = boxId;
    sMovingMonOrigBoxPos = position;
}

static void SetPlacedMonData(u8 boxId, u8 position)
{
    OrchidPC_ContentsChanged();
    if (OW_PC_HEAL <= GEN_7)
        HealPokemon(&sStorage->movingMon);

    if (boxId == TOTAL_BOXES_COUNT)
    {
        gParties[B_TRAINER_PLAYER][position] = sStorage->movingMon;
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][position];
        if (mon == GetFirstLiveMon())
            gFollowerSteps = 0;
        SetMonFormPSS(&mon->box, FORM_CHANGE_WITHDRAW);
    }
    else
    {
        SetBoxMonAt(boxId, position, &sStorage->movingMon.box);
        SetMonFormPSS(&gPokemonStoragePtr->boxes[boxId][position], FORM_CHANGE_DEPOSIT);
    }
}

static void PurgeMonOrBoxMon(u8 boxId, u8 position)
{
    OrchidPC_ContentsChanged();
    if (boxId == TOTAL_BOXES_COUNT)
        ZeroMonData(&gParties[B_TRAINER_PLAYER][position]);
    else
        ZeroBoxMonAt(boxId, position);
}

static void SetShiftedMonData(u8 boxId, u8 position)
{
    if (boxId == TOTAL_BOXES_COUNT)
        sStorage->tempMon = gParties[B_TRAINER_PLAYER][position];
    else
        BoxMonAtToMon(boxId, position, &sStorage->tempMon);

    SetPlacedMonData(boxId, position);
    sStorage->movingMon = sStorage->tempMon;
    SetDisplayMonData(&sStorage->movingMon, MODE_PARTY);
    sMovingMonOrigBoxId = boxId;
    sMovingMonOrigBoxPos = position;
}

static bool8 TryStorePartyMonInBox(u8 boxId)
{
    s16 boxPosition = GetFirstFreeBoxSpot(boxId);
    if (boxPosition == -1)
        return FALSE;

    if (sIsMonBeingMoved)
    {
        SetPlacedMonData(boxId, boxPosition);
        DestroyMovingMonIcon();
        sIsMonBeingMoved = FALSE;
    }
    else
    {
        SetMovingMonData(TOTAL_BOXES_COUNT, sCursorPosition);
        SetPlacedMonData(boxId, boxPosition);
        DestroyPartyMonIcon(sCursorPosition);
    }

    if (boxId == StorageGetCurrentBox())
        CreateBoxMonIconAtPos(boxPosition);

    StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_STILL);
    return TRUE;
}

static void ResetSelectionAfterDeposit(void)
{
    StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_BOUNCE);
    TryRefreshDisplayMon();
}

static void InitReleaseMon(void)
{
    u8 mode;

    if (sIsMonBeingMoved)
        mode = MODE_MOVE;
    else if (sCursorArea == CURSOR_AREA_IN_PARTY)
        mode = MODE_PARTY;
    else
        mode = MODE_BOX;

    SetReleaseMon(mode, sCursorPosition);
    StringCopy(sStorage->releaseMonName, sStorage->displayMonName);
}

static bool8 TryHideReleaseMon(void)
{
    if (!TryHideReleaseMonSprite())
    {
        StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_BOUNCE);
        return FALSE;
    }
    else
    {
        return TRUE;
    }
}

static void ReleaseMon(void)
{
    u8 boxId;
    enum Item item = ITEM_NONE;

    DestroyReleaseMonIcon();
    if (sIsMonBeingMoved)
    {
        sIsMonBeingMoved = FALSE;
    }
    else
    {
        if (sCursorArea == CURSOR_AREA_IN_PARTY)
        {
            boxId = TOTAL_BOXES_COUNT;
            if (OW_PC_RELEASE_ITEM >= GEN_8)
                item = GetMonData(&gParties[B_TRAINER_PLAYER][sCursorPosition], MON_DATA_HELD_ITEM);
        }
        else
        {
            boxId = StorageGetCurrentBox();
            if (OW_PC_RELEASE_ITEM >= GEN_8)
                item = GetBoxMonDataAt(boxId, sCursorPosition, MON_DATA_HELD_ITEM);
        }

        PurgeMonOrBoxMon(boxId, sCursorPosition);
        if (item != ITEM_NONE)
            AddBagItem(item, 1);
    }
    TryRefreshDisplayMon();
}

static void TrySetCursorFistAnim(void)
{
    if (sIsMonBeingMoved)
        StartSpriteAnim(sStorage->cursorSprite, CURSOR_ANIM_FIST);
}

// If the player is on the listed map (or any map, if none is specified),
// they may not release their last Pokémon that knows the specified move.
// This is to stop the player from softlocking themselves by not having
// a Pokémon that knows a required field move.
struct
{
    s8 mapGroup;
    s8 mapNum;
    u16 move;
} static const sRestrictedReleaseMoves[] =
{
    {MAP_GROUPS_COUNT, 0, MOVE_SURF},
    {MAP_GROUPS_COUNT, 0, MOVE_DIVE},
    {MAP_GROUP(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F), MAP_NUM(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F), MOVE_STRENGTH},
    {MAP_GROUP(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F), MAP_NUM(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_1F), MOVE_ROCK_SMASH},
    {MAP_GROUP(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_2F), MAP_NUM(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_2F), MOVE_STRENGTH},
    {MAP_GROUP(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_2F), MAP_NUM(MAP_EVER_GRANDE_CITY_POKEMON_LEAGUE_2F), MOVE_ROCK_SMASH},
};

static void GetRestrictedReleaseMoves(u16 *moves)
{
    s32 i;

    for (i = 0; i < ARRAY_COUNT(sRestrictedReleaseMoves); i++)
    {
        if (sRestrictedReleaseMoves[i].mapGroup == MAP_GROUPS_COUNT
        || (sRestrictedReleaseMoves[i].mapGroup == gSaveBlock1Ptr->location.mapGroup
         && sRestrictedReleaseMoves[i].mapNum == gSaveBlock1Ptr->location.mapNum))
        {
            *moves = sRestrictedReleaseMoves[i].move;
            moves++;
        }
    }
    *moves = MOVES_COUNT;
}

static void InitCanReleaseMonVars(void)
{
    if (!AtLeastThreeUsableMons())
    {
        // The player only has 1 or 2 usable
        // Pokémon, this one can't be released
        sStorage->releaseStatusResolved = TRUE;
        sStorage->canReleaseMon = FALSE;
        return;
    }

    if (sIsMonBeingMoved)
    {
        sStorage->tempMon = sStorage->movingMon;
        sStorage->releaseBoxId = -1;
        sStorage->releaseBoxPos = -1;
    }
    else
    {
        if (sCursorArea == CURSOR_AREA_IN_PARTY)
        {
            sStorage->tempMon = gParties[B_TRAINER_PLAYER][sCursorPosition];
            sStorage->releaseBoxId = TOTAL_BOXES_COUNT;
        }
        else
        {
            BoxMonAtToMon(StorageGetCurrentBox(), sCursorPosition, &sStorage->tempMon);
            sStorage->releaseBoxId = StorageGetCurrentBox();
        }
        sStorage->releaseBoxPos = sCursorPosition;
    }

    GetRestrictedReleaseMoves(sStorage->restrictedMoveList);
    sStorage->restrictedReleaseMonMoves = GetMonData(&sStorage->tempMon, MON_DATA_KNOWN_MOVES, (u8 *)sStorage->restrictedMoveList);
    if (sStorage->restrictedReleaseMonMoves != 0)
    {
        // Pokémon knows at least one restricted release move
        // Need to check if another Pokémon has this move first
        sStorage->releaseStatusResolved = FALSE;
    }
    else
    {
        // Pokémon knows no restricted moves, can be released
        sStorage->releaseStatusResolved = TRUE;
        sStorage->canReleaseMon = TRUE;
    }

    sStorage->releaseCheckState = 0;
}

static bool32 AtLeastThreeUsableMons(void)
{
    s32 i, j;
    s32 count = (sIsMonBeingMoved != FALSE);

    // Check party for usable Pokémon
    for (j = 0; j < PARTY_SIZE; j++)
    {
        if (GetMonData(&gParties[B_TRAINER_PLAYER][j], MON_DATA_SANITY_HAS_SPECIES))
            count++;
    }

    if (count >= 3)
        return TRUE;

    // Check PC for usable Pokémon
    for (i = 0; i < TOTAL_BOXES_COUNT; i++)
    {
        for (j = 0; j < IN_BOX_COUNT; j++)
        {
            if (CheckBoxMonSanityAt(i, j))
            {
                if (++count >= 3)
                    return TRUE;
            }
        }
    }

    return FALSE;
}

static s8 RunCanReleaseMon(void)
{
    u16 i;
    u16 knownMoves;

    if (sStorage->releaseStatusResolved)
        return sStorage->canReleaseMon;

    switch (sStorage->releaseCheckState)
    {
    case 0:
        // Check party for other Pokémon that know any restricted
        // moves the release Pokémon knows
        for (i = 0; i < PARTY_SIZE; i++)
        {
            // Make sure party Pokémon isn't the one we're releasing first
            if (sStorage->releaseBoxId != TOTAL_BOXES_COUNT || sStorage->releaseBoxPos != i)
            {
                knownMoves = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_KNOWN_MOVES, (u8 *)sStorage->restrictedMoveList);
                sStorage->restrictedReleaseMonMoves &= ~(knownMoves);
            }
        }
        if (sStorage->restrictedReleaseMonMoves == 0)
        {
            // No restricted moves on release Pokémon that
            // aren't resolved by the party, it can be released.
            sStorage->releaseStatusResolved = TRUE;
            sStorage->canReleaseMon = TRUE;
        }
        else
        {
            // Release Pokémon has restricted moves not resolved by the party.
            // Continue and check the PC next
            sStorage->releaseCheckBoxId = 0;
            sStorage->releaseCheckBoxPos = 0;
            sStorage->releaseCheckState++;
        }
        break;
    case 1:
        // Check PC for other Pokémon that know any restricted
        // moves the release Pokémon knows
        for (i = 0; i < IN_BOX_COUNT; i++)
        {
            knownMoves = GetAndCopyBoxMonDataAt(sStorage->releaseCheckBoxId, sStorage->releaseCheckBoxPos, MON_DATA_KNOWN_MOVES, (u8 *)sStorage->restrictedMoveList);
            if (knownMoves != 0 && !(sStorage->releaseBoxId == sStorage->releaseCheckBoxId
                                  && sStorage->releaseBoxPos == sStorage->releaseCheckBoxPos))
            {
                // Found PC Pokémon with restricted move, clear move from list
                sStorage->restrictedReleaseMonMoves &= ~(knownMoves);
                if (sStorage->restrictedReleaseMonMoves == 0)
                {
                    // No restricted moves on release Pokémon that
                    // aren't resolved, it can be released.
                    sStorage->releaseStatusResolved = TRUE;
                    sStorage->canReleaseMon = TRUE;
                    break;
                }
            }
            if (++sStorage->releaseCheckBoxPos >= IN_BOX_COUNT)
            {
                sStorage->releaseCheckBoxPos = 0;
                if (++sStorage->releaseCheckBoxId >= TOTAL_BOXES_COUNT)
                {
                    // Checked every Pokémon in the PC, release Pokémon is
                    // the sole owner of at least one restricted move.
                    // It cannot be released.
                    sStorage->releaseStatusResolved = TRUE;
                    sStorage->canReleaseMon = FALSE;
                }
            }
        }
        break;
    }

    return -1;
}

static void SaveMovingMon(void)
{
    if (sIsMonBeingMoved)
        sSavedMovingMon = sStorage->movingMon;
}

static void LoadSavedMovingMon(void)
{
    if (sIsMonBeingMoved)
    {
        // If it came from the party load a struct Pokemon,
        // otherwise load a BoxPokemon
        if (sMovingMonOrigBoxId == TOTAL_BOXES_COUNT)
            sStorage->movingMon = sSavedMovingMon;
        else
            sStorage->movingMon.box = sSavedMovingMon.box;
    }
}

static void InitSummaryScreenData(void)
{
    if (sIsMonBeingMoved)
    {
        SaveMovingMon();
        sStorage->summaryMon.mon = &sSavedMovingMon;
        sStorage->summaryStartPos = 0;
        sStorage->summaryMaxPos = 0;
        sStorage->summaryScreenMode = SUMMARY_MODE_BOX_CURSOR;
    }
    else if (sCursorArea == CURSOR_AREA_IN_PARTY)
    {
        sStorage->summaryMon.mon = gParties[B_TRAINER_PLAYER];
        sStorage->summaryStartPos = sCursorPosition;
        sStorage->summaryMaxPos = CountPartyMons() - 1;
        sStorage->summaryScreenMode = SUMMARY_MODE_NORMAL;
    }
    else
    {
        sStorage->summaryMon.box = GetBoxedMonPtr(StorageGetCurrentBox(), 0);
        sStorage->summaryStartPos = sCursorPosition;
        sStorage->summaryMaxPos = IN_BOX_COUNT - 1;
        sStorage->summaryScreenMode = SUMMARY_MODE_BOX;
    }
}

static void SetSelectionAfterSummaryScreen(void)
{
    if (sIsMonBeingMoved)
        LoadSavedMovingMon();
    else
        sCursorPosition = gLastViewedMonIndex;
}

s16 CompactPartySlots(void)
{
    s16 retVal = -1;
    u16 i, last;

    for (i = 0, last = 0; i < PARTY_SIZE; i++)
    {
        enum Species species = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES);
        if (species != SPECIES_NONE)
        {
            if (i != last)
                gParties[B_TRAINER_PLAYER][last] = gParties[B_TRAINER_PLAYER][i];
            last++;
        }
        else if (retVal == -1)
        {
            retVal = i;
        }
    }
    for (; last < PARTY_SIZE; last++)
        ZeroMonData(&gParties[B_TRAINER_PLAYER][last]);

    return retVal;
}

static void SetMonMarkings(u8 markings)
{
    sStorage->displayMonMarkings = markings;
    if (sIsMonBeingMoved)
    {
        SetMonData(&sStorage->movingMon, MON_DATA_MARKINGS, &markings);
    }
    else
    {
        if (sCursorArea == CURSOR_AREA_IN_PARTY)
            SetMonData(&gParties[B_TRAINER_PLAYER][sCursorPosition], MON_DATA_MARKINGS, &markings);
        if (sCursorArea == CURSOR_AREA_IN_BOX)
            SetCurrentBoxMonData(sCursorPosition, MON_DATA_MARKINGS, &markings);
    }
}

static bool8 IsRemovingLastPartyMon(void)
{
    if (sCursorArea == CURSOR_AREA_IN_PARTY && !sIsMonBeingMoved && CountPartyAliveNonEggMonsExcept(sCursorPosition) == 0)
        return TRUE;
    else
        return FALSE;
}

static bool8 CanPlaceMon(void)
{
    if (sIsMonBeingMoved)
    {
        if (sCursorArea == CURSOR_AREA_IN_PARTY && GetMonData(&gParties[B_TRAINER_PLAYER][sCursorPosition], MON_DATA_SPECIES) == SPECIES_NONE)
            return TRUE;
        else if (sCursorArea == CURSOR_AREA_IN_BOX && GetBoxMonDataAt(StorageGetCurrentBox(), sCursorPosition, MON_DATA_SPECIES_OR_EGG) == SPECIES_NONE)
            return TRUE;
        else
            return FALSE;
    }
    return FALSE;
}

static bool8 CanShiftMon(void)
{
    if (sIsMonBeingMoved)
    {
        if (sCursorArea == CURSOR_AREA_IN_PARTY && CountPartyAliveNonEggMonsExcept(sCursorPosition) == 0)
        {
            if (sStorage->displayMonIsEgg || GetMonData(&sStorage->movingMon, MON_DATA_HP) == 0)
                return FALSE;
        }
        return TRUE;
    }
    return FALSE;
}

static bool8 IsMonBeingMoved(void)
{
    return sIsMonBeingMoved;
}

static bool8 IsCursorOnBoxTitle(void)
{
    return (sCursorArea == CURSOR_AREA_BOX_TITLE);
}

static bool8 IsCursorOnCloseBox(void)
{
    return (sCursorArea == CURSOR_AREA_BUTTONS && sCursorPosition == 1);
}


static void TryRefreshDisplayMon(void)
{
    // If a Pokémon is currently being moved, don't start
    // mosaic or update display. Keep displaying the
    // currently held Pokémon.
    sStorage->setMosaic = (sIsMonBeingMoved == FALSE);
    if (!sIsMonBeingMoved)
    {
        // Update display Pokémon
        switch (sCursorArea)
        {
        case CURSOR_AREA_IN_PARTY:
            if (sCursorPosition < PARTY_SIZE)
            {
                SetDisplayMonData(&gParties[B_TRAINER_PLAYER][sCursorPosition], MODE_PARTY);
                break;
            }
            // fallthrough
        case CURSOR_AREA_BUTTONS:
        case CURSOR_AREA_BOX_TITLE:
            SetDisplayMonData(NULL, MODE_MOVE);
            break;
        case CURSOR_AREA_IN_BOX:
            SetDisplayMonData(GetBoxedMonPtr(StorageGetCurrentBox(), sCursorPosition), MODE_BOX);
            break;
        }
    }
}

static void ReshowDisplayMon(void)
{
    if (sIsMonBeingMoved)
        SetDisplayMonData(&sSavedMovingMon, MODE_PARTY);
    else
        TryRefreshDisplayMon();
}

void SetMonFormPSS(struct BoxPokemon *boxMon, enum FormChanges method)
{
    if (TryBoxMonFormChange(boxMon, method))
        sRefreshDisplayMonGfx = TRUE;
}

void SetMonFormPSS_ItemHold(struct BoxPokemon *boxMon)
{
    if (TryBoxMonFormChange(boxMon, FORM_CHANGE_ITEM_HOLD))
        sRefreshDisplayMonGfx = TRUE;
    UpdateSpeciesSpritePSS(boxMon);
}

static void SetDisplayMonData(void *pokemon, u8 mode)
{
    u8 *txtPtr;
    u16 gender;
    bool8 sanityIsBadEgg;

    sStorage->displayMonItemId = ITEM_NONE;
    gender = MON_MALE;
    sanityIsBadEgg = FALSE;
    if (mode == MODE_PARTY)
    {
        struct Pokemon *mon = (struct Pokemon *)pokemon;

        sStorage->displayMonSpecies = GetMonData(mon, MON_DATA_SPECIES);
        if (sStorage->displayMonSpecies != SPECIES_NONE)
        {
            sanityIsBadEgg = GetMonData(mon, MON_DATA_SANITY_IS_BAD_EGG);
            if (sanityIsBadEgg)
                sStorage->displayMonIsEgg = TRUE;
            else
                sStorage->displayMonIsEgg = GetMonData(mon, MON_DATA_IS_EGG);

            GetMonData(mon, MON_DATA_NICKNAME, sStorage->displayMonName);
            StringGet_Nickname(sStorage->displayMonName);
            sStorage->displayMonLevel = GetMonData(mon, MON_DATA_LEVEL);
            sStorage->displayMonMarkings = GetMonData(mon, MON_DATA_MARKINGS);
            sStorage->displayMonPersonality = GetMonData(mon, MON_DATA_PERSONALITY);
            sStorage->displayMonPalette = GetMonFrontSpritePal(mon);
            gender = GetMonGender(mon);
            sStorage->displayMonItemId = GetMonData(mon, MON_DATA_HELD_ITEM);
        }
    }
    else if (mode == MODE_BOX)
    {
        struct BoxPokemon *boxMon = (struct BoxPokemon *)pokemon;

        sStorage->displayMonSpecies = GetBoxMonData(pokemon, MON_DATA_SPECIES);
        if (sStorage->displayMonSpecies != SPECIES_NONE)
        {
            bool32 isShiny = GetBoxMonData(boxMon, MON_DATA_IS_SHINY);
            sanityIsBadEgg = GetBoxMonData(boxMon, MON_DATA_SANITY_IS_BAD_EGG);
            if (sanityIsBadEgg)
                sStorage->displayMonIsEgg = TRUE;
            else
                sStorage->displayMonIsEgg = GetBoxMonData(boxMon, MON_DATA_IS_EGG);

            GetBoxMonData(boxMon, MON_DATA_NICKNAME, sStorage->displayMonName);
            StringGet_Nickname(sStorage->displayMonName);
            sStorage->displayMonLevel = GetLevelFromBoxMonExp(boxMon);
            sStorage->displayMonMarkings = GetBoxMonData(boxMon, MON_DATA_MARKINGS);
            sStorage->displayMonPersonality = GetBoxMonData(boxMon, MON_DATA_PERSONALITY);
            sStorage->displayMonIsEgg = GetBoxMonData(boxMon, MON_DATA_IS_EGG);
            sStorage->displayMonPalette = GetMonSpritePalFromSpeciesAndPersonalityIsEgg(sStorage->displayMonSpecies, isShiny, sStorage->displayMonPersonality, sStorage->displayMonIsEgg);
            gender = GetGenderFromSpeciesAndPersonality(sStorage->displayMonSpecies, sStorage->displayMonPersonality);
            sStorage->displayMonItemId = GetBoxMonData(boxMon, MON_DATA_HELD_ITEM);
        }
    }
    else
    {
        sStorage->displayMonSpecies = SPECIES_NONE;
        sStorage->displayMonItemId = ITEM_NONE;
    }

    sStorage->displayMonGender = (sStorage->displayMonSpecies == SPECIES_NONE) ? MON_GENDERLESS : gender;
    if (sStorage->displayMonSpecies == SPECIES_NONE)
    {
        StringFill(sStorage->displayMonName, CHAR_SPACE, 5);
        StringFill(sStorage->displayMonNameText, CHAR_SPACE, 8);
        StringFill(sStorage->displayMonSpeciesName, CHAR_SPACE, 8);
        StringFill(sStorage->displayMonGenderLvlText, CHAR_SPACE, 8);
        StringFill(sStorage->displayMonItemName, CHAR_SPACE, 8);
    }
    else if (sStorage->displayMonIsEgg)
    {
        if (sanityIsBadEgg)
            StringCopyPadded(sStorage->displayMonNameText, sStorage->displayMonName, CHAR_SPACE, 5);
        else
            StringCopyPadded(sStorage->displayMonNameText, gText_EggNickname, CHAR_SPACE, 8);

        StringFill(sStorage->displayMonSpeciesName, CHAR_SPACE, 8);
        StringFill(sStorage->displayMonGenderLvlText, CHAR_SPACE, 8);
        StringFill(sStorage->displayMonItemName, CHAR_SPACE, 8);
    }
    else
    {
        if (sStorage->displayMonSpecies == SPECIES_NIDORAN_F || sStorage->displayMonSpecies == SPECIES_NIDORAN_M)
            gender = MON_GENDERLESS;

        StringCopyPadded(sStorage->displayMonNameText, sStorage->displayMonName, CHAR_SPACE, 5);

        txtPtr = sStorage->displayMonSpeciesName;
        *(txtPtr++) = CHAR_SLASH;
        StringCopyPadded(txtPtr, GetSpeciesName(sStorage->displayMonSpecies), CHAR_SPACE, 5);

        txtPtr = sStorage->displayMonGenderLvlText;
        *(txtPtr++) = EXT_CTRL_CODE_BEGIN;
        *(txtPtr++) = EXT_CTRL_CODE_BACKGROUND;
        *(txtPtr++) = TEXT_COLOR_WHITE;
        *(txtPtr++) = EXT_CTRL_CODE_BEGIN;
        *(txtPtr++) = EXT_CTRL_CODE_TEXT_COLORS;
        switch (gender)
        {
        case MON_MALE:
            *(txtPtr++) = TEXT_COLOR_RED;
            *(txtPtr++) = TEXT_COLOR_LIGHT_RED;
            *(txtPtr++) = TEXT_COLOR_WHITE;
            *(txtPtr++) = CHAR_MALE;
            break;
        case MON_FEMALE:
            *(txtPtr++) = TEXT_COLOR_GREEN;
            *(txtPtr++) = TEXT_COLOR_LIGHT_GREEN;
            *(txtPtr++) = TEXT_COLOR_WHITE;
            *(txtPtr++) = CHAR_FEMALE;
            break;
        default:
            *(txtPtr++) = TEXT_COLOR_DARK_GRAY;
            *(txtPtr++) = TEXT_COLOR_LIGHT_GRAY;
            *(txtPtr++) = TEXT_COLOR_WHITE;
            *(txtPtr++) = CHAR_SPACER; // Genderless
            break;
        }

        *(txtPtr++) = EXT_CTRL_CODE_BEGIN;
        *(txtPtr++) = EXT_CTRL_CODE_TEXT_COLORS;
        *(txtPtr++) = TEXT_COLOR_DARK_GRAY;
        *(txtPtr++) = TEXT_COLOR_LIGHT_GRAY;
        *(txtPtr++) = TEXT_COLOR_WHITE;
        *(txtPtr++) = CHAR_SPACE;
        *(txtPtr++) = CHAR_EXTRA_SYMBOL;
        *(txtPtr++) = CHAR_LV_2;

        txtPtr = ConvertIntToDecimalStringN(txtPtr, sStorage->displayMonLevel, STR_CONV_MODE_LEFT_ALIGN, 3);
        txtPtr[0] = CHAR_SPACE;
        txtPtr[1] = EOS;

        if (sStorage->displayMonItemId != ITEM_NONE)
            StringCopyPadded(sStorage->displayMonItemName, GetItemName(sStorage->displayMonItemId), CHAR_SPACE, 8);
        else
            StringFill(sStorage->displayMonItemName, CHAR_SPACE, 8);
    }
}


//------------------------------------------------------------------------------
//  SECTION: Input handlers
//
//  The functions below process context-dependent input
//------------------------------------------------------------------------------


static u8 HandleInput_InBox(void)
{
    switch (sStorage->inBoxMovingMode)
    {
    case MOVE_MODE_NORMAL:
    default:
        return InBoxInput_Normal();
    case MOVE_MODE_MULTIPLE_SELECTING:
        return InBoxInput_SelectingMultiple();
    case MOVE_MODE_MULTIPLE_MOVING:
        return InBoxInput_MovingMultiple();
    }
}

static u8 InBoxInput_Normal(void)
{
    u8 retVal;
    s8 cursorArea;
    s8 cursorPosition;

    do
    {
        cursorArea = sCursorArea;
        cursorPosition = sCursorPosition;
        sStorage->cursorVerticalWrap = 0;
        sStorage->cursorHorizontalWrap = 0;
        sStorage->cursorFlipTimer = 0;

        if (JOY_REPEAT(DPAD_UP))
        {
            retVal = INPUT_MOVE_CURSOR;
            if (sCursorPosition >= IN_BOX_COLUMNS)
            {
                cursorPosition -= IN_BOX_COLUMNS;
            }
            else
            {
                cursorArea = CURSOR_AREA_BOX_TITLE;
                cursorPosition = 0;
            }
            break;
        }
        else if (JOY_REPEAT(DPAD_DOWN))
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorPosition += IN_BOX_COLUMNS;
            if (cursorPosition >= IN_BOX_COUNT)
            {
                cursorArea = CURSOR_AREA_BUTTONS;
                cursorPosition -= IN_BOX_COUNT;
                cursorPosition /= 3;
                sStorage->cursorVerticalWrap = 1;
                sStorage->cursorFlipTimer = 1;
            }
            break;
        }
        else if (JOY_REPEAT(DPAD_LEFT))
        {
            retVal = INPUT_MOVE_CURSOR;
            if (sCursorPosition % IN_BOX_COLUMNS != 0)
            {
                cursorPosition--;
            }
            else
            {
                sStorage->cursorHorizontalWrap = -1;
                cursorPosition += (IN_BOX_COLUMNS - 1);
            }
            break;
        }
        else if (JOY_REPEAT(DPAD_RIGHT))
        {
            retVal = INPUT_MOVE_CURSOR;
            if ((sCursorPosition + 1) % IN_BOX_COLUMNS != 0)
            {
                cursorPosition++;
            }
            else
            {
                sStorage->cursorHorizontalWrap = 1;
                cursorPosition -= (IN_BOX_COLUMNS - 1);
            }
            break;
        }
        else if (JOY_NEW(START_BUTTON))
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorArea = CURSOR_AREA_BOX_TITLE;
            cursorPosition = 0;
            break;
        }

        if ((JOY_NEW(A_BUTTON)) && SetSelectionMenuTexts())
        {
            if (!sAutoActionOn)
                return INPUT_IN_MENU;

            if (sStorage->boxOption != OPTION_MOVE_MONS || sIsMonBeingMoved == TRUE)
            {
                switch (GetMenuItemTextId(0))
                {
                case MENU_STORE:
                    return INPUT_DEPOSIT;
                case MENU_WITHDRAW:
                    return INPUT_WITHDRAW;
                case MENU_MOVE:
                    return INPUT_MOVE_MON;
                case MENU_SHIFT:
                    return INPUT_SHIFT_MON;
                case MENU_PLACE:
                    return INPUT_PLACE_MON;
                case MENU_TAKE:
                    return INPUT_TAKE_ITEM;
                case MENU_GIVE:
                    return INPUT_GIVE_ITEM;
                case MENU_SWITCH:
                    return INPUT_SWITCH_ITEMS;
                case MENU_SELECT:
                    return INPUT_SELECT_MON;
                }
            }
            else
            {
                sStorage->inBoxMovingMode = MOVE_MODE_MULTIPLE_SELECTING;
                return INPUT_MULTIMOVE_START;
            }
        }

        if (JOY_NEW(B_BUTTON))
            return INPUT_PRESSED_B;

        if (gSaveBlock2Ptr->optionsButtonMode == OPTIONS_BUTTON_MODE_LR)
        {
            if (JOY_HELD(L_BUTTON))
                return INPUT_SCROLL_LEFT;
            if (JOY_HELD(R_BUTTON))
                return INPUT_SCROLL_RIGHT;
        }

        if (JOY_NEW(SELECT_BUTTON))
        {
            ToggleCursorAutoAction();
            return INPUT_NONE;
        }

        retVal = INPUT_NONE;

    } while (0);

    if (retVal)
        SetCursorPosition(cursorArea, cursorPosition);

    return retVal;
}

static u8 InBoxInput_SelectingMultiple(void)
{
    if (JOY_HELD(A_BUTTON))
    {
        if (JOY_REPEAT(DPAD_UP))
        {
            if (sCursorPosition / IN_BOX_COLUMNS != 0)
            {
                SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition - IN_BOX_COLUMNS);
                return INPUT_MULTIMOVE_CHANGE_SELECTION;
            }
            else
            {
                return INPUT_MULTIMOVE_UNABLE;
            }
        }
        else if (JOY_REPEAT(DPAD_DOWN))
        {
            if (sCursorPosition + IN_BOX_COLUMNS < IN_BOX_COUNT)
            {
                SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition + IN_BOX_COLUMNS);
                return INPUT_MULTIMOVE_CHANGE_SELECTION;
            }
            else
            {
                return INPUT_MULTIMOVE_UNABLE;
            }
        }
        else if (JOY_REPEAT(DPAD_LEFT))
        {
            if (sCursorPosition % IN_BOX_COLUMNS != 0)
            {
                SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition - 1);
                return INPUT_MULTIMOVE_CHANGE_SELECTION;
            }
            else
            {
                return INPUT_MULTIMOVE_UNABLE;
            }
        }
        else if (JOY_REPEAT(DPAD_RIGHT))
        {
            if ((sCursorPosition + 1) % IN_BOX_COLUMNS != 0)
            {
                SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition + 1);
                return INPUT_MULTIMOVE_CHANGE_SELECTION;
            }
            else
            {
                return INPUT_MULTIMOVE_UNABLE;
            }
        }
        else
        {
            return INPUT_NONE;
        }
    }
    else
    {
        if (MultiMove_GetOrigin() == sCursorPosition)
        {
            // Doing a multiple mon selection but only chose 1 mon
            sStorage->inBoxMovingMode = MOVE_MODE_NORMAL;
            sStorage->cursorShadowSprite->invisible = FALSE;
            return INPUT_MULTIMOVE_SINGLE;
        }
        else
        {
            sIsMonBeingMoved = (sStorage->displayMonSpecies != SPECIES_NONE);
            sStorage->inBoxMovingMode = MOVE_MODE_MULTIPLE_MOVING;
            sMovingMonOrigBoxId = StorageGetCurrentBox();
            return INPUT_MULTIMOVE_GRAB_SELECTION;
        }
    }
}

static u8 InBoxInput_MovingMultiple(void)
{
    if (JOY_REPEAT(DPAD_UP))
    {
        if (MultiMove_TryMoveGroup(0))
        {
            SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition - IN_BOX_COLUMNS);
            return INPUT_MULTIMOVE_MOVE_MONS;
        }
        else
        {
            return INPUT_MULTIMOVE_UNABLE;
        }
    }
    else if (JOY_REPEAT(DPAD_DOWN))
    {
        if (MultiMove_TryMoveGroup(1))
        {
            SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition + IN_BOX_COLUMNS);
            return INPUT_MULTIMOVE_MOVE_MONS;
        }
        else
        {
            return INPUT_MULTIMOVE_UNABLE;
        }
    }
    else if (JOY_REPEAT(DPAD_LEFT))
    {
        if (MultiMove_TryMoveGroup(2))
        {
            SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition - 1);
            return INPUT_MULTIMOVE_MOVE_MONS;
        }
        else
        {
            return INPUT_SCROLL_LEFT;
        }
    }
    else if (JOY_REPEAT(DPAD_RIGHT))
    {
        if (MultiMove_TryMoveGroup(3))
        {
            SetCursorPosition(CURSOR_AREA_IN_BOX, sCursorPosition + 1);
            return INPUT_MULTIMOVE_MOVE_MONS;
        }
        else
        {
            return INPUT_SCROLL_RIGHT;
        }
    }
    else if (JOY_NEW(A_BUTTON))
    {
        if (MultiMove_CanPlaceSelection())
        {
            sIsMonBeingMoved = FALSE;
            sStorage->inBoxMovingMode = MOVE_MODE_NORMAL;
            return INPUT_MULTIMOVE_PLACE_MONS;
        }
        else
        {
            return INPUT_MULTIMOVE_UNABLE;
        }
    }
    else if (JOY_NEW(B_BUTTON))
    {
        return INPUT_MULTIMOVE_UNABLE;
    }
    else
    {
        if (gSaveBlock2Ptr->optionsButtonMode == OPTIONS_BUTTON_MODE_LR)
        {
            if (JOY_HELD(L_BUTTON))
                return INPUT_SCROLL_LEFT;
            if (JOY_HELD(R_BUTTON))
                return INPUT_SCROLL_RIGHT;
        }

        return INPUT_NONE;
    }
}

static u8 HandleInput_InParty(void)
{
    u8 retVal;
    bool8 gotoBox;
    s8 cursorArea;
    s8 cursorPosition;

    do
    {
        cursorArea = sCursorArea;
        cursorPosition = sCursorPosition;
        sStorage->cursorHorizontalWrap = 0;
        sStorage->cursorVerticalWrap = 0;
        sStorage->cursorFlipTimer = 0;
        gotoBox = FALSE;
        retVal = INPUT_NONE;

        // Orchid: 2x3 party grid (lead top-left, BW order) with CANCEL below
        if (JOY_REPEAT(DPAD_UP))
        {
            if (cursorPosition == PARTY_SIZE)
                cursorPosition = PARTY_SIZE - 2;
            else if (cursorPosition < 2)
                cursorPosition = PARTY_SIZE;
            else
                cursorPosition -= 2;
            if (cursorPosition != sCursorPosition)
                retVal = INPUT_MOVE_CURSOR;
            break;
        }
        else if (JOY_REPEAT(DPAD_DOWN))
        {
            if (cursorPosition == PARTY_SIZE)
                cursorPosition = 0;
            else if (cursorPosition >= PARTY_SIZE - 2)
                cursorPosition = PARTY_SIZE;
            else
                cursorPosition += 2;
            if (cursorPosition != sCursorPosition)
                retVal = INPUT_MOVE_CURSOR;
            break;
        }
        else if (JOY_REPEAT(DPAD_LEFT) && sCursorPosition < PARTY_SIZE && (sCursorPosition % 2) == 1)
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorPosition = sCursorPosition - 1;
            break;
        }
        else if (JOY_REPEAT(DPAD_RIGHT))
        {
            if (sCursorPosition < PARTY_SIZE && (sCursorPosition % 2) == 0)
            {
                retVal = INPUT_MOVE_CURSOR;
                cursorPosition = sCursorPosition + 1;
            }
            else
            {
                retVal = INPUT_HIDE_PARTY;
                cursorArea = CURSOR_AREA_IN_BOX;
                cursorPosition = 0;
            }
            break;
        }

        if (JOY_NEW(A_BUTTON))
        {
            if (sCursorPosition == PARTY_SIZE)
            {
                if (sStorage->boxOption == OPTION_DEPOSIT)
                    return INPUT_CLOSE_BOX;

                gotoBox = TRUE;
            }
            else if (SetSelectionMenuTexts())
            {
                if (!sAutoActionOn)
                    return INPUT_IN_MENU;

                switch (GetMenuItemTextId(0))
                {
                case MENU_STORE:
                    return INPUT_DEPOSIT;
                case MENU_WITHDRAW:
                    return INPUT_WITHDRAW;
                case MENU_MOVE:
                    return INPUT_MOVE_MON;
                case MENU_SHIFT:
                    return INPUT_SHIFT_MON;
                case MENU_PLACE:
                    return INPUT_PLACE_MON;
                case MENU_TAKE:
                    return INPUT_TAKE_ITEM;
                case MENU_GIVE:
                    return INPUT_GIVE_ITEM;
                case MENU_SWITCH:
                    return INPUT_SWITCH_ITEMS;
                case MENU_SELECT:
                    return INPUT_SELECT_MON;
                }
            }
        }

        if (JOY_NEW(B_BUTTON))
        {
            if (sStorage->boxOption == OPTION_DEPOSIT)
                return INPUT_PRESSED_B;

            gotoBox = TRUE;
        }

        if (gotoBox)
        {
            retVal = INPUT_HIDE_PARTY;
            cursorArea = CURSOR_AREA_IN_BOX;
            cursorPosition = 0;
        }
        else if (JOY_NEW(SELECT_BUTTON))
        {
            ToggleCursorAutoAction();
            return INPUT_NONE;
        }

    } while (0);

    if (retVal != INPUT_NONE)
    {
        if (retVal != INPUT_HIDE_PARTY)
            SetCursorPosition(cursorArea, cursorPosition);
    }

    return retVal;
}

static u8 HandleInput_OnBox(void)
{
    u8 retVal;
    s8 cursorArea;
    s8 cursorPosition;

    do
    {
        sStorage->cursorHorizontalWrap = 0;
        sStorage->cursorVerticalWrap = 0;
        sStorage->cursorFlipTimer = 0;

        if (JOY_REPEAT(DPAD_UP))
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorArea = CURSOR_AREA_BUTTONS;
            cursorPosition = 0;
            sStorage->cursorFlipTimer = 1;
            break;
        }
        else if (JOY_REPEAT(DPAD_DOWN))
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorArea = CURSOR_AREA_IN_BOX;
            cursorPosition = 2;
            break;
        }

        if (JOY_HELD(DPAD_LEFT))
            return INPUT_SCROLL_LEFT;
        if (JOY_HELD(DPAD_RIGHT))
            return INPUT_SCROLL_RIGHT;

        if (gSaveBlock2Ptr->optionsButtonMode == OPTIONS_BUTTON_MODE_LR)
        {
            if (JOY_HELD(L_BUTTON))
                return INPUT_SCROLL_LEFT;
            if (JOY_HELD(R_BUTTON))
                return INPUT_SCROLL_RIGHT;
        }

        if (JOY_NEW(A_BUTTON))
        {
            AnimateBoxScrollArrows(FALSE);
            AddBoxOptionsMenu();
            return INPUT_BOX_OPTIONS;
        }

        if (JOY_NEW(B_BUTTON))
            return INPUT_PRESSED_B;

        if (JOY_NEW(SELECT_BUTTON))
        {
            ToggleCursorAutoAction();
            return INPUT_NONE;
        }

        retVal = INPUT_NONE;

    } while (0);

    if (retVal != INPUT_NONE)
    {
        if (cursorArea != CURSOR_AREA_BOX_TITLE)
            AnimateBoxScrollArrows(FALSE);
        SetCursorPosition(cursorArea, cursorPosition);
    }

    return retVal;
}

static u8 HandleInput_OnButtons(void)
{
    u8 retVal;
    s8 cursorArea;
    s8 cursorPosition;

    do
    {
        cursorArea = sCursorArea;
        cursorPosition = sCursorPosition;
        sStorage->cursorHorizontalWrap = 0;
        sStorage->cursorVerticalWrap = 0;
        sStorage->cursorFlipTimer = 0;

        if (JOY_REPEAT(DPAD_UP))
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorArea = CURSOR_AREA_IN_BOX;
            sStorage->cursorVerticalWrap = -1;
            if (sCursorPosition == 0)
                cursorPosition = IN_BOX_COUNT - 1 - 5;
            else
                cursorPosition = IN_BOX_COUNT - 1;
            sStorage->cursorFlipTimer = 1;
            break;
        }

        if (JOY_REPEAT(DPAD_DOWN | START_BUTTON))
        {
            retVal = INPUT_MOVE_CURSOR;
            cursorArea = CURSOR_AREA_BOX_TITLE;
            cursorPosition = 0;
            sStorage->cursorFlipTimer = 1;
            break;
        }

        if (JOY_REPEAT(DPAD_LEFT))
        {
            retVal = INPUT_MOVE_CURSOR;
            if (--cursorPosition < 0)
                cursorPosition = 1;
            break;
        }
        else if (JOY_REPEAT(DPAD_RIGHT))
        {
            retVal = INPUT_MOVE_CURSOR;
            if (++cursorPosition > 1)
                cursorPosition = 0;
            break;
        }

        // Button was pressed, determine which
        if (JOY_NEW(A_BUTTON))
            return (cursorPosition == 0) ? INPUT_SHOW_PARTY : INPUT_CLOSE_BOX;

        if (JOY_NEW(B_BUTTON))
            return INPUT_PRESSED_B;

        if (JOY_NEW(SELECT_BUTTON))
        {
            ToggleCursorAutoAction();
            return INPUT_NONE;
        }

        retVal = INPUT_NONE;
    } while (0);

    if (retVal != INPUT_NONE)
        SetCursorPosition(cursorArea, cursorPosition);

    return retVal;
}

static u8 HandleInput(void)
{
    struct
    {
        u8 (*func)(void);
        s8 area;
    } static const inputFuncs[] =
    {
        {HandleInput_InBox,     CURSOR_AREA_IN_BOX},
        {HandleInput_InParty,   CURSOR_AREA_IN_PARTY},
        {HandleInput_OnBox,     CURSOR_AREA_BOX_TITLE},
        {HandleInput_OnButtons, CURSOR_AREA_BUTTONS},
        {},
    };

    u16 i = 0;
    while (inputFuncs[i].func != NULL)
    {
        if (inputFuncs[i].area == sCursorArea)
            return inputFuncs[i].func();
        i++;
    }

    return INPUT_NONE;
}

static void AddBoxOptionsMenu(void)
{
    InitMenu();
    SetMenuText(MENU_JUMP);
    SetMenuText(MENU_WALLPAPER);
    SetMenuText(MENU_NAME);
    SetMenuText(MENU_CANCEL);
}

static u8 SetSelectionMenuTexts(void)
{
    InitMenu();
    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return SetMenuTexts_Mon();
    else
        return SetMenuTexts_Item();
}

static bool8 SetMenuTexts_Mon(void)
{
    enum Species species = GetSpeciesAtCursorPosition();

    switch (sStorage->boxOption)
    {
    case OPTION_DEPOSIT:
        if (species != SPECIES_NONE)
            SetMenuText(MENU_STORE);
        else
            return FALSE;
        break;
    case OPTION_WITHDRAW:
        if (species != SPECIES_NONE)
            SetMenuText(MENU_WITHDRAW);
        else
            return FALSE;
        break;
    case OPTION_MOVE_MONS:
        if (sIsMonBeingMoved)
        {
            if (species != SPECIES_NONE)
                SetMenuText(MENU_SHIFT);
            else
                SetMenuText(MENU_PLACE);
        }
        else
        {
            if (species != SPECIES_NONE)
                SetMenuText(MENU_MOVE);
            else
                return FALSE;
        }
        break;
    case OPTION_SELECT_MON:
        if (species != SPECIES_NONE && CanBoxMonBeSelected(GetCursorBoxMon()))
            SetMenuText(MENU_SELECT);
        else
            return FALSE;
        break;
    case OPTION_MOVE_ITEMS:
    default:
        return FALSE;
    }

    SetMenuText(MENU_SUMMARY);
    if (sStorage->boxOption == OPTION_MOVE_MONS)
    {
        if (sCursorArea == CURSOR_AREA_IN_BOX)
            SetMenuText(MENU_WITHDRAW);
        else
            SetMenuText(MENU_STORE);
    }

    SetMenuText(MENU_MARK);
    if (sStorage->boxOption != OPTION_SELECT_MON)
        SetMenuText(MENU_RELEASE);
    SetMenuText(MENU_CANCEL);
    return TRUE;
}

static bool8 SetMenuTexts_Item(void)
{
    if (sStorage->displayMonSpecies == SPECIES_EGG)
        return FALSE;

    if (!IsMovingItem())
    {
        if (sStorage->displayMonItemId == ITEM_NONE)
        {
            if (sStorage->displayMonSpecies == SPECIES_NONE)
                return FALSE;

            SetMenuText(MENU_GIVE_2);
        }
        else
        {
            if (!ItemIsMail(sStorage->displayMonItemId))
            {
                SetMenuText(MENU_TAKE);
                SetMenuText(MENU_BAG);
            }
            SetMenuText(MENU_INFO);
        }
    }
    else
    {
        if (sStorage->displayMonItemId == ITEM_NONE)
        {
            if (sStorage->displayMonSpecies == SPECIES_NONE)
                return FALSE;

            SetMenuText(MENU_GIVE);
        }
        else
        {
            if (ItemIsMail(sStorage->displayMonItemId) == TRUE)
                return FALSE;

            SetMenuText(MENU_SWITCH);
        }
    }

    SetMenuText(MENU_CANCEL);
    return TRUE;
}


//------------------------------------------------------------------------------
//  SECTION: Cursor
//
//  The functions below handle a few of the generic cursor features.
//------------------------------------------------------------------------------


// Orchid: the lift shadow under a held Pokémon / item, in the slot's recess (mock_pc: 16x8 at (cx - 8, cy - 1))
static void SpriteCB_CursorShadow(struct Sprite *sprite)
{
    bool32 holding = sIsMonBeingMoved || IsMovingItem();

    sprite->x = sStorage->cursorSprite->x;
    sprite->y = sStorage->cursorSprite->y + OPC_SHADOW_DY;
    sprite->invisible = !holding || sStorage->cursorSprite->invisible || sStorage->inBoxMovingMode != MOVE_MODE_NORMAL;
    if (sCursorArea == CURSOR_AREA_IN_PARTY)
    {
        sprite->oam.priority = 1;
        sprite->subpriority = 9;
    }
    else
    {
        sprite->oam.priority = 2;
        sprite->subpriority = 22;
    }
}

// Orchid: the cursor is a gold ring (32x32: normal, flash) hugging the slot lip, plus the lift shadow
static void CreateCursorSprites(void)
{
    u16 x, y;
    u8 spriteId;
    struct SpriteSheet spriteSheets[] =
    {
        {gOrchidPcObj_Gfx + OPC_OBJ_RING * TILE_SIZE_4BPP, 32 * TILE_SIZE_4BPP, GFXTAG_CURSOR},
        {gOrchidPcObj_Gfx + OPC_OBJ_SHADOW * TILE_SIZE_4BPP, 2 * TILE_SIZE_4BPP, GFXTAG_CURSOR_SHADOW},
        {gOrchidPcObj_Gfx + OPC_OBJ_HOLD_TAG * TILE_SIZE_4BPP, TILE_SIZE_4BPP, GFXTAG_HOLD_TAG},
        {}
    };

    static const struct OamData sOamData_Cursor =
    {
        .shape = SPRITE_SHAPE(32x32),
        .size = SPRITE_SIZE(32x32),
        .priority = 2,
    };
    static const struct OamData sOamData_CursorShadow =
    {
        .shape = SPRITE_SHAPE(16x8),
        .size = SPRITE_SIZE(16x8),
        .priority = 2,
    };

    static const union AnimCmd sAnim_Cursor_Still[] =
    {
        ANIMCMD_FRAME(0, 5),
        ANIMCMD_END
    };
    static const union AnimCmd sAnim_Cursor_Flash[] =
    {
        ANIMCMD_FRAME(16, OPC_FLASH_FRAMES),
        ANIMCMD_FRAME(0, 5),
        ANIMCMD_END
    };

    static const union AnimCmd *const sAnims_Cursor[] =
    {
        [CURSOR_ANIM_BOUNCE] = sAnim_Cursor_Still,
        [CURSOR_ANIM_STILL]  = sAnim_Cursor_Still,
        [CURSOR_ANIM_OPEN]   = sAnim_Cursor_Still,
        [CURSOR_ANIM_FIST]   = sAnim_Cursor_Still,
        [CURSOR_ANIM_FLASH]  = sAnim_Cursor_Flash,
    };

    static const struct SpriteTemplate sSpriteTemplate_Cursor =
    {
        .tileTag = GFXTAG_CURSOR,
        .paletteTag = PALTAG_MISC_2,
        .oam = &sOamData_Cursor,
        .anims = sAnims_Cursor,
        .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable,
        .callback = SpriteCallbackDummy,
    };

    static const struct SpriteTemplate sSpriteTemplate_CursorShadow =
    {
        .tileTag = GFXTAG_CURSOR_SHADOW,
        .paletteTag = PALTAG_MISC_2,
        .oam = &sOamData_CursorShadow,
        .anims = gDummySpriteAnimTable,
        .images = NULL,
        .affineAnims = gDummySpriteAffineAnimTable,
        .callback = SpriteCB_CursorShadow,
    };

    LoadSpriteSheets(spriteSheets);
    sStorage->cursorPalNums[0] = IndexOfSpritePaletteTag(PALTAG_MISC_2);
    sStorage->cursorPalNums[1] = sStorage->cursorPalNums[0];

    GetCursorCoordsByPos(sCursorArea, sCursorPosition, &x, &y);
    spriteId = CreateSpriteUnchecked(&sSpriteTemplate_Cursor, x, y, 21);
    if (spriteId != MAX_SPRITES)
    {
        sStorage->cursorSprite = &gSprites[spriteId];
        OrchidPC_UpdateRing();
    }
    else
    {
        sStorage->cursorSprite = NULL;
    }

    spriteId = CreateSpriteUnchecked(&sSpriteTemplate_CursorShadow, 0, 0, 22);
    if (spriteId != MAX_SPRITES)
    {
        sStorage->cursorShadowSprite = &gSprites[spriteId];
        sStorage->cursorShadowSprite->invisible = TRUE;
    }
    else
    {
        sStorage->cursorShadowSprite = NULL;
    }
}

static void ToggleCursorAutoAction(void)
{
    sAutoActionOn = !sAutoActionOn;
    sStorage->cursorSprite->oam.paletteNum = sStorage->cursorPalNums[sAutoActionOn];
}

static u8 GetCursorPosition(void)
{
    return sCursorPosition;
}

static void GetCursorBoxColumnAndRow(u8 *column, u8 *row)
{
    if (sCursorArea == CURSOR_AREA_IN_BOX)
    {
        *column = sCursorPosition % IN_BOX_COLUMNS;
        *row = sCursorPosition / IN_BOX_COLUMNS;
    }
    else
    {
        *column = 0;
        *row = 0;
    }
}

static void StartCursorAnim(u8 animNum)
{
    StartSpriteAnim(sStorage->cursorSprite, animNum);
}

static void SetCursorPriorityTo1(void)
{
    sStorage->cursorSprite->oam.priority = 1;
}

static void TryHideItemAtCursor(void)
{
    if (sCursorArea == CURSOR_AREA_IN_BOX)
        TryHideItemIconAtPos(CURSOR_AREA_IN_BOX, sCursorPosition);
}

static void TryShowItemAtCursor(void)
{
    if (sCursorArea == CURSOR_AREA_IN_BOX)
        TryLoadItemIconAtPos(CURSOR_AREA_IN_BOX, sCursorPosition);
}


//------------------------------------------------------------------------------
//  SECTION: Menu
//
//  The functions below handle the generic options menu that comes up whenever
//  something in the PC is selected.
//------------------------------------------------------------------------------


static void InitMenu(void)
{
    sStorage->menuItemsCount = 0;
    sStorage->menuWidth = 0;
    sStorage->menuWindow.bg = 0;
    sStorage->menuWindow.paletteNum = OPC_BG_WINDOW;
    sStorage->menuWindow.baseBlock = 92;
}

static const u8 gPCText_Give[] = _("GIVE");

static const u8 *const sMenuTexts[] =
{
    [MENU_CANCEL]     = COMPOUND_STRING("CANCEL"),
    [MENU_STORE]      = COMPOUND_STRING("STORE"),
    [MENU_WITHDRAW]   = COMPOUND_STRING("WITHDRAW"),
    [MENU_MOVE]       = COMPOUND_STRING("MOVE"),
    [MENU_SHIFT]      = COMPOUND_STRING("SHIFT"),
    [MENU_PLACE]      = COMPOUND_STRING("PLACE"),
    [MENU_SUMMARY]    = COMPOUND_STRING("SUMMARY"),
    [MENU_RELEASE]    = COMPOUND_STRING("RELEASE"),
    [MENU_MARK]       = COMPOUND_STRING("MARK"),
    [MENU_JUMP]       = COMPOUND_STRING("JUMP"),
    [MENU_WALLPAPER]  = COMPOUND_STRING("COLOUR"), // Orchid: box colours replace wallpapers
    [MENU_NAME]       = COMPOUND_STRING("NAME"),
    [MENU_TAKE]       = COMPOUND_STRING("TAKE"),
    [MENU_GIVE]       = gPCText_Give,
    [MENU_GIVE_2]     = gPCText_Give,
    [MENU_SWITCH]     = COMPOUND_STRING("SWITCH"),
    [MENU_BAG]        = COMPOUND_STRING("BAG"),
    [MENU_INFO]       = COMPOUND_STRING("INFO"),
    [MENU_SCENERY_1]  = COMPOUND_STRING("SCENERY 1"),
    [MENU_SCENERY_2]  = COMPOUND_STRING("SCENERY 2"),
    [MENU_SCENERY_3]  = COMPOUND_STRING("SCENERY 3"),
    [MENU_ETCETERA]   = COMPOUND_STRING("ETCETERA"),
    [MENU_FRIENDS]    = COMPOUND_STRING("FRIENDS"),
    [MENU_FOREST]     = COMPOUND_STRING("FOREST"),
    [MENU_CITY]       = COMPOUND_STRING("CITY"),
    [MENU_DESERT]     = COMPOUND_STRING("DESERT"),
    [MENU_SAVANNA]    = COMPOUND_STRING("SAVANNA"),
    [MENU_CRAG]       = COMPOUND_STRING("CRAG"),
    [MENU_VOLCANO]    = COMPOUND_STRING("VOLCANO"),
    [MENU_SNOW]       = COMPOUND_STRING("SNOW"),
    [MENU_CAVE]       = COMPOUND_STRING("CAVE"),
    [MENU_BEACH]      = COMPOUND_STRING("BEACH"),
    [MENU_SEAFLOOR]   = COMPOUND_STRING("SEAFLOOR"),
    [MENU_RIVER]      = COMPOUND_STRING("RIVER"),
    [MENU_SKY]        = COMPOUND_STRING("SKY"),
    [MENU_POLKADOT]   = COMPOUND_STRING("POLKA-DOT"),
    [MENU_POKECENTER] = COMPOUND_STRING("POKéCENTER"),
    [MENU_MACHINE]    = COMPOUND_STRING("MACHINE"),
    [MENU_SIMPLE]     = COMPOUND_STRING("SIMPLE"),
    [MENU_SELECT]     = COMPOUND_STRING("SELECT"),
};

static void SetMenuText(u8 textId)
{
    if (sStorage->menuItemsCount < ARRAY_COUNT(sStorage->menuItems))
    {
        u8 len;
        struct StorageMenu *menu = &sStorage->menuItems[sStorage->menuItemsCount];

        menu->text = sMenuTexts[textId];
        menu->textId = textId;
        len = StringLength(menu->text);
        if (len > sStorage->menuWidth)
            sStorage->menuWidth = len;

        sStorage->menuItemsCount++;
    }
}

static s8 GetMenuItemTextId(u8 menuIdx)
{
    if (menuIdx >= sStorage->menuItemsCount)
        return -1;
    else
        return sStorage->menuItems[menuIdx].textId;
}

// Orchid (mock_pc.menu): std Orchid frame anchored like vanilla (right edge tile 29, bottom tile 15), sized
// to the widest text in pixels; the gold pill marks the row, no ▶.
static void AddMenu(void)
{
    sStorage->menuWindow.width = GetOrchidPillMenuWidth((void *)sStorage->menuItems, sStorage->menuItemsCount);
    sStorage->menuWindow.height = 2 * sStorage->menuItemsCount;
    sStorage->menuWindow.tilemapLeft = 29 - sStorage->menuWindow.width;
    sStorage->menuWindow.tilemapTop = 15 - sStorage->menuWindow.height;
    sStorage->menuWindowId = AddWindow(&sStorage->menuWindow);
    ClearWindowTilemap(sStorage->menuWindowId);
    DrawStdFrameWithCustomTileAndPalette(sStorage->menuWindowId, FALSE, OPC_FRAME_TILE, OPC_BG_WINDOW);
    InitOrchidPillMenu(sStorage->menuWindowId, sStorage->menuItemsCount, (void *)sStorage->menuItems, 0);
    PutWindowTilemap(sStorage->menuWindowId);
    ScheduleBgCopyTilemapToVram(0);
}

// Called after AddMenu to determine whether or not the handler callback should
// wait to move on to the next state. Evidently there was no need to wait, and
// now it always returns FALSE
static bool8 IsMenuLoading(void)
{
    return FALSE;
}

static s16 HandleMenuInput(void)
{
    s32 input = MENU_NOTHING_CHOSEN;

    do
    {
        if (JOY_NEW(A_BUTTON))
        {
            input = Menu_GetCursorPos();
            break;
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            input = MENU_B_PRESSED;
        }

        if (JOY_NEW(DPAD_UP))
        {
            PlaySE(SE_SELECT);
            Menu_MoveCursor(-1);
        }
        else if (JOY_NEW(DPAD_DOWN))
        {
            PlaySE(SE_SELECT);
            Menu_MoveCursor(1);
        }
    } while (0);

    if (input != MENU_NOTHING_CHOSEN)
        RemoveMenu();

    if (input >= 0)
        input = sStorage->menuItems[input].textId;

    return input;
}

static void RemoveMenu(void)
{
    ClearStdWindowAndFrameToTransparent(sStorage->menuWindowId, TRUE);
    RemoveWindow(sStorage->menuWindowId);
}


//------------------------------------------------------------------------------
//  SECTION: MultiMove
//
//  The functions below handle moving and selecting multiple Pokémon at once.
//  The icon sprites are moved to bg 0, and this bg is manipulated to move
//  them as a group.
//------------------------------------------------------------------------------


static const struct WindowTemplate sWindowTemplate_MultiMove =
{
    .bg = 0,
    .tilemapLeft = 10,
    .tilemapTop = 3,
    .width = 20,
    .height = 18,
    .paletteNum = 9,
    .baseBlock = 0xA,
};

EWRAM_DATA static struct
{
    u8 funcId;
    u8 state;
    u8 fromColumn;
    u8 fromRow;
    u8 toColumn;
    u8 toRow;
    u8 cursorColumn;
    u8 cursorRow;
    u8 minColumn;
    u8 minRow;
    u8 columnsTotal;
    u8 rowsTotal;
    u16 bgX;
    u16 bgY;
    u16 bgMoveSteps;
    struct BoxPokemon boxMons[IN_BOX_COUNT];
} *sMultiMove = NULL;

static bool8 MultiMove_Init(void)
{
    sMultiMove = Alloc(sizeof(*sMultiMove));
    if (sMultiMove != NULL)
    {
        sStorage->multiMoveWindowId = AddWindow8Bit(&sWindowTemplate_MultiMove);
        if (sStorage->multiMoveWindowId != WINDOW_NONE)
        {
            FillWindowPixelBuffer(sStorage->multiMoveWindowId, PIXEL_FILL(0));
            return TRUE;
        }
    }

    return FALSE;
}

static void MultiMove_Free(void)
{
    if (sMultiMove != NULL)
        Free(sMultiMove);
}

static void MultiMove_SetFunction(u8 id)
{
    sMultiMove->funcId = id;
    sMultiMove->state = 0;
}

// Returns TRUE if the called function has more to do, FALSE otherwise
static bool8 MultiMove_RunFunction(void)
{
    switch (sMultiMove->funcId)
    {
    case MULTIMOVE_START:
        return MultiMove_Start();
    case MULTIMOVE_CANCEL:
        return MultiMove_Cancel();
    case MULTIMOVE_CHANGE_SELECTION:
        return MultiMove_ChangeSelection();
    case MULTIMOVE_GRAB_SELECTION:
        return MultiMove_GrabSelection();
    case MULTIMOVE_MOVE_MONS:
        return MultiMove_MoveMons();
    case MULTIMOVE_PLACE_MONS:
        return MultiMove_PlaceMons();
    }
    return FALSE;
}

static bool8 MultiMove_Start(void)
{
    switch (sMultiMove->state)
    {
    case 0:
        HideBg(0);
        // Orchid: the icon palettes borrow the party slot palettes (the panel is hidden in the box)
        TryLoadAllMonIconPalettesAtOffset(BG_PLTT_ID(OPC_BG_SLOT));
        sMultiMove->state++;
        break;
    case 1:
        GetCursorBoxColumnAndRow(&sMultiMove->fromColumn, &sMultiMove->fromRow);
        sMultiMove->toColumn = sMultiMove->fromColumn;
        sMultiMove->toRow = sMultiMove->fromRow;
        ChangeBgX(0, -1024, BG_COORD_SET);
        ChangeBgY(0, -2048, BG_COORD_SET); // Orchid: box icons sit 4 px lower than vanilla (y 48)
        FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, 0x20, 0x20);
        FillWindowPixelBuffer8Bit(sStorage->multiMoveWindowId, PIXEL_FILL(0));
        MultiMove_SetIconToBg(sMultiMove->fromColumn, sMultiMove->fromRow);
        SetBgAttribute(0, BG_ATTR_PALETTEMODE, 1);
        PutWindowTilemap(sStorage->multiMoveWindowId);
        CopyWindowToVram8Bit(sStorage->multiMoveWindowId, COPYWIN_FULL);
        BlendPalettes(0x3F << OPC_BG_SLOT, 8, RGB_WHITE);
        StartCursorAnim(CURSOR_ANIM_OPEN);
        SetGpuRegBits(REG_OFFSET_BG0CNT, BGCNT_256COLOR);
        sMultiMove->state++;
        break;
    case 2:
        if (!IsDma3ManagerBusyWithBgCopy())
        {
            ShowBg(0);
            return FALSE;
        }
        break;
    }

    return TRUE;
}

static bool8 MultiMove_Cancel(void)
{
    switch (sMultiMove->state)
    {
    case 0:
        HideBg(0);
        sMultiMove->state++;
        break;
    case 1:
        MultiMove_ResetBg();
        StartCursorAnim(CURSOR_ANIM_BOUNCE);
        sMultiMove->state++;
        break;
    case 2:
        if (!IsDma3ManagerBusyWithBgCopy())
        {
            SetCursorPriorityTo1();
            OrchidPC_UpdateRing();
            LoadPalette(GetTextWindowPalette(3), BG_PLTT_ID(13), PLTT_SIZE_4BPP);
            ShowBg(0);
            return FALSE;
        }
        break;
    }

    return TRUE;
}

static bool8 MultiMove_ChangeSelection(void)
{
    switch (sMultiMove->state)
    {
    case 0:
        if (!UpdateCursorPos())
        {
            GetCursorBoxColumnAndRow(&sMultiMove->cursorColumn, &sMultiMove->cursorRow);
            MultiMove_UpdateSelectedIcons();
            sMultiMove->toColumn = sMultiMove->cursorColumn;
            sMultiMove->toRow = sMultiMove->cursorRow;
            CopyWindowToVram8Bit(sStorage->multiMoveWindowId, COPYWIN_GFX);
            sMultiMove->state++;
        }
        break;
    case 1:
        return IsDma3ManagerBusyWithBgCopy();
    }

    return TRUE;
}

static bool8 MultiMove_GrabSelection(void)
{
    bool8 movingBg, movingMon;

    switch (sMultiMove->state)
    {
    case 0:
        MultiMove_GetMonsFromSelection();
        MultiMove_RemoveMonsFromBox();
        InitMultiMonPlaceChange(FALSE);
        sMultiMove->state++;
        break;
    case 1:
        if (!DoMonPlaceChange())
        {
            StartCursorAnim(CURSOR_ANIM_FIST);
            MultiMove_InitMove(0, Q_8_8(1), 8);
            InitMultiMonPlaceChange(TRUE);
            sMultiMove->state++;
        }
        break;
    case 2:
        movingBg = MultiMove_UpdateMove();
        movingMon = DoMonPlaceChange();
        if (!movingBg && !movingMon)
            return FALSE; // Finished
        break;
    }

    return TRUE;
}

static bool8 MultiMove_MoveMons(void)
{
    bool8 movingCursor = UpdateCursorPos();
    bool8 movingBg = MultiMove_UpdateMove();

    if (!movingCursor && !movingBg)
        return FALSE;
    else
        return TRUE;
}

static bool8 MultiMove_PlaceMons(void)
{
    switch (sMultiMove->state)
    {
    case 0:
        MultiMove_SetPlacedMonData();
        MultiMove_InitMove(0, Q_8_8(-1), 8);
        InitMultiMonPlaceChange(FALSE);
        sMultiMove->state++;
        break;
    case 1:
        if (!DoMonPlaceChange() && !MultiMove_UpdateMove())
        {
            MultiMove_CreatePlacedMonIcons();
            StartCursorAnim(CURSOR_ANIM_OPEN);
            InitMultiMonPlaceChange(TRUE);
            HideBg(0);
            sMultiMove->state++;
        }
        break;
    case 2:
        if (!DoMonPlaceChange())
        {
            StartCursorAnim(CURSOR_ANIM_BOUNCE);
            MultiMove_ResetBg();
            sMultiMove->state++;
        }
        break;
    case 3:
        if (!IsDma3ManagerBusyWithBgCopy())
        {
            LoadPalette(GetTextWindowPalette(3), BG_PLTT_ID(13), PLTT_SIZE_4BPP);
            SetCursorPriorityTo1();
            OrchidPC_UpdateRing();
            ShowBg(0);
            return FALSE;
        }
        break;
    }
    return TRUE;
}

// Returns TRUE if the movement was successful, FALSE otherwise
static bool8 MultiMove_TryMoveGroup(u8 dir)
{
    switch (dir)
    {
    case 0: // Up
        if (sMultiMove->minRow == 0)
            return FALSE;
        sMultiMove->minRow--;
        MultiMove_InitMove(0, Q_8_8(4), 6);
        break;
    case 1: // Down
        if (sMultiMove->minRow + sMultiMove->rowsTotal >= IN_BOX_ROWS)
            return FALSE;
        sMultiMove->minRow++;
        MultiMove_InitMove(0, Q_8_8(-4), 6);
        break;
    case 2: // Left
        if (sMultiMove->minColumn == 0)
            return FALSE;
        sMultiMove->minColumn--;
        MultiMove_InitMove(Q_8_8(4), 0, 6);
        break;
    case 3: // Right
        if (sMultiMove->minColumn + sMultiMove->columnsTotal >= IN_BOX_COLUMNS)
            return FALSE;
        sMultiMove->minColumn++;
        MultiMove_InitMove(Q_8_8(-4), 0, 6);
        break;
    }
    return TRUE;
}

static void MultiMove_UpdateSelectedIcons(void)
{
    s16 columnChange = (abs(sMultiMove->fromColumn - sMultiMove->cursorColumn)) - (abs(sMultiMove->fromColumn - sMultiMove->toColumn));
    s16 rowChange = (abs(sMultiMove->fromRow - sMultiMove->cursorRow)) - (abs(sMultiMove->fromRow - sMultiMove->toRow));

    if (columnChange > 0)
        MultiMove_SelectColumn(sMultiMove->cursorColumn, sMultiMove->fromRow, sMultiMove->toRow);

    if (columnChange < 0)
    {
        MultiMove_DeselectColumn(sMultiMove->toColumn, sMultiMove->fromRow, sMultiMove->toRow);
        MultiMove_SelectColumn(sMultiMove->cursorColumn, sMultiMove->fromRow, sMultiMove->toRow);
    }

    if (rowChange > 0)
        MultiMove_SelectRow(sMultiMove->cursorRow, sMultiMove->fromColumn, sMultiMove->toColumn);

    if (rowChange < 0)
    {
        MultiMove_DeselectRow(sMultiMove->toRow, sMultiMove->fromColumn, sMultiMove->toColumn);
        MultiMove_SelectRow(sMultiMove->cursorRow, sMultiMove->fromColumn, sMultiMove->toColumn);
    }
}

static void MultiMove_SelectColumn(u8 column, u8 minRow, u8 maxRow)
{
    if (minRow > maxRow)
    {
        u8 temp;
        SWAP(minRow, maxRow, temp);
    }

    while (minRow <= maxRow)
        MultiMove_SetIconToBg(column, minRow++);
}

static void MultiMove_SelectRow(u8 row, u8 minColumn, u8 maxColumn)
{
    if (minColumn > maxColumn)
    {
        u8 temp;
        SWAP(minColumn, maxColumn, temp);
    }

    while (minColumn <= maxColumn)
        MultiMove_SetIconToBg(minColumn++, row);
}

static void MultiMove_DeselectColumn(u8 column, u8 minRow, u8 maxRow)
{
    if (minRow > maxRow)
    {
        u8 temp;
        SWAP(minRow, maxRow, temp);
    }

    while (minRow <= maxRow)
        MultiMove_ClearIconFromBg(column, minRow++);
}

static void MultiMove_DeselectRow(u8 row, u8 minColumn, u8 maxColumn)
{
    if (minColumn > maxColumn)
    {
        u8 temp;
        SWAP(minColumn, maxColumn, temp);
    }

    while (minColumn <= maxColumn)
        MultiMove_ClearIconFromBg(minColumn++, row);
}

static void MultiMove_SetIconToBg(u8 x, u8 y)
{
    u8 position = x + (IN_BOX_COLUMNS * y);
    enum Species species = GetCurrentBoxMonData(position, MON_DATA_SPECIES);
    u32 personality = GetCurrentBoxMonData(position, MON_DATA_PERSONALITY);
    bool32 isEgg = GetCurrentBoxMonData(position, MON_DATA_IS_EGG);

    if (species != SPECIES_NONE)
    {
        const u8 *iconGfx = GetMonIconPtrIsEgg(species, personality, isEgg);
        u8 index = GetValidMonIconPalIndex(species) + OPC_BG_SLOT;

        BlitBitmapRectToWindow4BitTo8Bit(sStorage->multiMoveWindowId,
                                         iconGfx,
                                         0,
                                         0,
                                         32,
                                         32,
                                         24 * x,
                                         24 * y,
                                         32,
                                         32,
                                         index);
    }
}

static void MultiMove_ClearIconFromBg(u8 x, u8 y)
{
    u8 position = x + (IN_BOX_COLUMNS * y);
    enum Species species = GetCurrentBoxMonData(position, MON_DATA_SPECIES_OR_EGG);

    if (species != SPECIES_NONE)
    {
        FillWindowPixelRect8Bit(sStorage->multiMoveWindowId,
                                PIXEL_FILL(0),
                                24 * x,
                                24 * y,
                                32,
                                32);
    }
}

static void MultiMove_InitMove(u16 x, u16 y, u16 moveSteps)
{
    sMultiMove->bgX = x;
    sMultiMove->bgY = y;
    sMultiMove->bgMoveSteps = moveSteps;
}

static u8 MultiMove_UpdateMove(void)
{
    if (sMultiMove->bgMoveSteps != 0)
    {
        ChangeBgX(0, sMultiMove->bgX, BG_COORD_ADD);
        ChangeBgY(0, sMultiMove->bgY, BG_COORD_ADD);
        sMultiMove->bgMoveSteps--;
    }

    return sMultiMove->bgMoveSteps;
}

// Store the Pokémon that the player is picking up
static void MultiMove_GetMonsFromSelection(void)
{
    s32 i, j;
    s32 columnCount, rowCount;
    u8 boxId;
    u8 monArrayId;

    sMultiMove->minColumn = min(sMultiMove->fromColumn, sMultiMove->toColumn);
    sMultiMove->minRow = min(sMultiMove->fromRow, sMultiMove->toRow);
    sMultiMove->columnsTotal = abs(sMultiMove->fromColumn - sMultiMove->toColumn) + 1;
    sMultiMove->rowsTotal = abs(sMultiMove->fromRow - sMultiMove->toRow) + 1;
    boxId = StorageGetCurrentBox();
    monArrayId = 0;
    columnCount = sMultiMove->minColumn + sMultiMove->columnsTotal;
    rowCount = sMultiMove->minRow + sMultiMove->rowsTotal;
    for (i = sMultiMove->minRow; i < rowCount; i++)
    {
        u8 boxPosition = (IN_BOX_COLUMNS * i) + sMultiMove->minColumn;
        for (j = sMultiMove->minColumn; j < columnCount; j++)
        {
            struct BoxPokemon *boxMon = GetBoxedMonPtr(boxId, boxPosition);
            // UB: possible null dereference
#ifdef UBFIX
            if (boxMon != NULL)
#endif
                sMultiMove->boxMons[monArrayId] = *boxMon;

            monArrayId++;
            boxPosition++;
        }
    }
}

// The Pokémon the player has picked up have been stored, now delete
// them from their original positions
static void MultiMove_RemoveMonsFromBox(void)
{
    s32 i, j;
    s32 columnCount = sMultiMove->minColumn + sMultiMove->columnsTotal;
    s32 rowCount = sMultiMove->minRow + sMultiMove->rowsTotal;
    u8 boxId = StorageGetCurrentBox();

    for (i = sMultiMove->minRow; i < rowCount; i++)
    {
        u8 boxPosition = (IN_BOX_COLUMNS * i) + sMultiMove->minColumn;
        for (j = sMultiMove->minColumn; j < columnCount; j++)
        {
            DestroyBoxMonIconAtPosition(boxPosition);
            ZeroBoxMonAt(boxId, boxPosition);
            boxPosition++;
        }
    }
}

static void MultiMove_CreatePlacedMonIcons(void)
{
    s32 i, j;
    s32 columnCount = sMultiMove->minColumn + sMultiMove->columnsTotal;
    s32 rowCount = sMultiMove->minRow + sMultiMove->rowsTotal;
    u8 monArrayId = 0;

    for (i = sMultiMove->minRow; i < rowCount; i++)
    {
        u8 boxPosition = (IN_BOX_COLUMNS * i) + sMultiMove->minColumn;
        for (j = sMultiMove->minColumn; j < columnCount; j++)
        {
            if (GetBoxMonData(&sMultiMove->boxMons[monArrayId], MON_DATA_SANITY_HAS_SPECIES))
                CreateBoxMonIconAtPos(boxPosition);
            monArrayId++;
            boxPosition++;
        }
    }
}

static void MultiMove_SetPlacedMonData(void)
{
    s32 i, j;
    s32 columnCount = sMultiMove->minColumn + sMultiMove->columnsTotal;
    s32 rowCount = sMultiMove->minRow + sMultiMove->rowsTotal;
    u8 boxId = StorageGetCurrentBox();
    u8 monArrayId = 0;

    for (i = sMultiMove->minRow; i < rowCount; i++)
    {
        u8 boxPosition = (IN_BOX_COLUMNS * i) + sMultiMove->minColumn;
        for (j = sMultiMove->minColumn; j < columnCount; j++)
        {
            if (OW_PC_HEAL <= GEN_7)
                HealBoxPokemon(&sMultiMove->boxMons[monArrayId]);
            if (GetBoxMonData(&sMultiMove->boxMons[monArrayId], MON_DATA_SANITY_HAS_SPECIES))
                SetBoxMonAt(boxId, boxPosition, &sMultiMove->boxMons[monArrayId]);
            boxPosition++;
            monArrayId++;
        }
    }
}

static void MultiMove_ResetBg(void)
{
    ChangeBgX(0, 0, BG_COORD_SET);
    ChangeBgY(0, 0, BG_COORD_SET);
    SetBgAttribute(0, BG_ATTR_PALETTEMODE, 0);
    ClearGpuRegBits(REG_OFFSET_BG0CNT, BGCNT_256COLOR);
    FillBgTilemapBufferRect_Palette0(0, 0, 0, 0, 32, 32);
    CopyBgTilemapBufferToVram(0);
    OrchidPC_LoadSlotPalettes();
    OrchidPC_ContentsChanged();
}

static u8 MultiMove_GetOrigin(void)
{
    return (IN_BOX_COLUMNS * sMultiMove->fromRow) + sMultiMove->fromColumn;
}

static bool8 MultiMove_CanPlaceSelection(void)
{
    s32 i, j;
    s32 columnCount = sMultiMove->minColumn + sMultiMove->columnsTotal;
    s32 rowCount = sMultiMove->minRow + sMultiMove->rowsTotal;
    u8 monArrayId = 0;

    for (i = sMultiMove->minRow; i < rowCount; i++)
    {
        u8 boxPosition = (IN_BOX_COLUMNS * i) + sMultiMove->minColumn;
        for (j = sMultiMove->minColumn; j < columnCount; j++)
        {
            if (GetBoxMonData(&sMultiMove->boxMons[monArrayId], MON_DATA_SANITY_HAS_SPECIES)
                && GetCurrentBoxMonData(boxPosition, MON_DATA_SANITY_HAS_SPECIES))
                return FALSE;

            monArrayId++;
            boxPosition++;
        }
    }
    return TRUE;
}


//------------------------------------------------------------------------------
//  SECTION: Item mode
//
//  The functions below handle the Move Items mode
//------------------------------------------------------------------------------


static const u32 sItemInfoFrame_Gfx[] = INCGFX_U32("graphics/pokemon_storage/item_info_frame.png", ".4bpp");

static const struct OamData sOamData_ItemIcon =
{
    .y = 0,
    .affineMode = ST_OAM_AFFINE_NORMAL,
    .objMode = ST_OAM_OBJ_NORMAL,
    .mosaic = FALSE,
    .bpp = ST_OAM_4BPP,
    .shape = SPRITE_SHAPE(32x32),
    .x = 0,
    .matrixNum = 0,
    .size = SPRITE_SIZE(32x32),
    .tileNum = 0,
    .priority = 1,
    .paletteNum = 0,
    .affineParam = 0
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_Small[] =
{
    AFFINEANIMCMD_FRAME(128, 128, 0, 0),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_Appear[] =
{
    AFFINEANIMCMD_FRAME(88, 88, 0, 0),
    AFFINEANIMCMD_FRAME(5, 5, 0, 8),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_Disappear[] =
{
    AFFINEANIMCMD_FRAME(128, 128, 0, 0),
    AFFINEANIMCMD_FRAME(-5, -5, 0, 8),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_PickUp[] =
{
    AFFINEANIMCMD_FRAME(128, 128, 0, 0),
    AFFINEANIMCMD_FRAME(10, 10, 0, 12),
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_PutDown[] =
{
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_FRAME(-10, -10, 0, 12),
    AFFINEANIMCMD_FRAME(128, 128, 0, 0),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_PutAway[] =
{
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_FRAME(-5, -5, 0, 16),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd sAffineAnim_ItemIcon_Large[] =
{
    AFFINEANIMCMD_FRAME(256, 256, 0, 0),
    AFFINEANIMCMD_END
};

static const union AffineAnimCmd *const sAffineAnims_ItemIcon[] =
{
    [ITEM_ANIM_NONE] = sAffineAnim_ItemIcon_Small,
    [ITEM_ANIM_APPEAR] = sAffineAnim_ItemIcon_Appear,
    [ITEM_ANIM_DISAPPEAR] = sAffineAnim_ItemIcon_Disappear,
    [ITEM_ANIM_PICK_UP] = sAffineAnim_ItemIcon_PickUp,
    [ITEM_ANIM_PUT_DOWN] = sAffineAnim_ItemIcon_PutDown,
    [ITEM_ANIM_PUT_AWAY] = sAffineAnim_ItemIcon_PutAway,
    [ITEM_ANIM_LARGE] = sAffineAnim_ItemIcon_Large
};

static const struct SpriteTemplate sSpriteTemplate_ItemIcon =
{
    .tileTag = GFXTAG_ITEM_ICON_0,
    .paletteTag = PALTAG_ITEM_ICON_0,
    .oam = &sOamData_ItemIcon,
    .affineAnims = sAffineAnims_ItemIcon,
};

static void CreateItemIconSprites(void)
{
    s32 i;
    u8 spriteId;
    struct CompressedSpriteSheet spriteSheet;
    struct SpriteTemplate spriteTemplate;

    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        spriteSheet.data = sItemIconGfxBuffer;
        spriteSheet.size = 0x200;
        spriteTemplate = sSpriteTemplate_ItemIcon;

        for (i = 0; i < MAX_ITEM_ICONS; i++)
        {
            spriteSheet.tag = GFXTAG_ITEM_ICON_0 + i;
            LoadCompressedSpriteSheet(&spriteSheet);
            sStorage->itemIcons[i].tiles = GetSpriteTileStartByTag(spriteSheet.tag) * TILE_SIZE_4BPP + (void *)(OBJ_VRAM0);
            sStorage->itemIcons[i].palIndex = AllocSpritePalette(PALTAG_ITEM_ICON_0 + i);
            sStorage->itemIcons[i].palIndex = OBJ_PLTT_ID(sStorage->itemIcons[i].palIndex);
            spriteTemplate.tileTag = GFXTAG_ITEM_ICON_0 + i;
            spriteTemplate.paletteTag = PALTAG_ITEM_ICON_0 + i;
            spriteId = CreateSprite(&spriteTemplate, 0, 0, 11);
            sStorage->itemIcons[i].sprite = &gSprites[spriteId];
            sStorage->itemIcons[i].sprite->invisible = TRUE;
            sStorage->itemIcons[i].active = FALSE;
        }
    }
    sStorage->movingItemId = ITEM_NONE;
}

static void TryLoadItemIconAtPos(u8 cursorArea, u8 cursorPos)
{
    enum Item heldItem;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    // If we've already loaded the item here, stop
    if (IsItemIconAtPosition(cursorArea, cursorPos))
        return;

    switch (cursorArea)
    {
    case CURSOR_AREA_IN_BOX:
        if (!GetCurrentBoxMonData(cursorPos, MON_DATA_SANITY_HAS_SPECIES))
            return;
        heldItem = GetCurrentBoxMonData(cursorPos, MON_DATA_HELD_ITEM);
        break;
    case CURSOR_AREA_IN_PARTY:
        if (cursorPos >= PARTY_SIZE || !GetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_SANITY_HAS_SPECIES))
            return;
        heldItem = GetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_HELD_ITEM);
        break;
    default:
        return;
    }

    if (heldItem != ITEM_NONE)
    {
        const u32 *tiles = GetItemIconPic(heldItem);
        const u16 *pal = GetItemIconPalette(heldItem);
        u8 id = GetNewItemIconIdx();

        SetItemIconPosition(id, cursorArea, cursorPos);
        LoadItemIconGfx(id, tiles, pal);
        SetItemIconAffineAnim(id, ITEM_ANIM_APPEAR);
        SetItemIconActive(id, TRUE);
        // Orchid: an item resting on a Pokémon shows as its hold tag + the info disc, not as an icon
        if (id < MAX_ITEM_ICONS)
            sStorage->itemIcons[id].sprite->invisible = TRUE;
    }
}

static void TryHideItemIconAtPos(u8 cursorArea, u8 cursorPos)
{
    u8 id;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    id = GetItemIconIdxByPosition(cursorArea, cursorPos);
    SetItemIconAffineAnim(id, ITEM_ANIM_DISAPPEAR);
    SetItemIconCallback(id, ITEM_CB_WAIT_ANIM, cursorArea, cursorPos);
}

static void TakeItemFromMon(u8 cursorArea, u8 cursorPos)
{
    u8 id;
    enum Item itemId;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    id = GetItemIconIdxByPosition(cursorArea, cursorPos);
    itemId = ITEM_NONE;
    SetItemIconAffineAnim(id, ITEM_ANIM_PICK_UP);
    SetItemIconCallback(id, ITEM_CB_TO_HAND, cursorArea, cursorPos);
    SetItemIconPosition(id, CURSOR_AREA_IN_HAND, 0);
    if (cursorArea == CURSOR_AREA_IN_BOX)
    {
        SetCurrentBoxMonData(cursorPos, MON_DATA_HELD_ITEM, &itemId);
        SetBoxMonIconObjMode(cursorPos, ST_OAM_OBJ_BLEND);
        SetMonFormPSS_ItemHold(&gPokemonStoragePtr->boxes[StorageGetCurrentBox()][cursorPos]);
    }
    else
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][cursorPos];
        SetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_HELD_ITEM, &itemId);
        SetPartyMonIconObjMode(cursorPos, ST_OAM_OBJ_BLEND);
        SetMonFormPSS_ItemHold(&mon->box);
    }

    sStorage->movingItemId = sStorage->displayMonItemId;
    OrchidPC_ContentsChanged();
}

static void InitItemIconInCursor(enum Item itemId)
{
    const u32 *tiles = GetItemIconPic(itemId);
    const u16 *pal = GetItemIconPalette(itemId);
    u8 id = GetNewItemIconIdx();
    LoadItemIconGfx(id, tiles, pal);
    SetItemIconAffineAnim(id, ITEM_ANIM_LARGE);
    SetItemIconCallback(id, ITEM_CB_TO_HAND, CURSOR_AREA_IN_BOX, 0);
    SetItemIconPosition(id, CURSOR_AREA_IN_HAND, 0);
    SetItemIconActive(id, TRUE);
    sStorage->movingItemId = itemId;
}

static void SwapItemsWithMon(u8 cursorArea, u8 cursorPos)
{
    u8 id;
    enum Item itemId;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    id = GetItemIconIdxByPosition(cursorArea, cursorPos);
    SetItemIconAffineAnim(id, ITEM_ANIM_PICK_UP);
    SetItemIconCallback(id, ITEM_CB_SWAP_TO_HAND, CURSOR_AREA_IN_HAND, 0);
    if (cursorArea == CURSOR_AREA_IN_BOX)
    {
        itemId = GetCurrentBoxMonData(cursorPos, MON_DATA_HELD_ITEM);
        SetCurrentBoxMonData(cursorPos, MON_DATA_HELD_ITEM, &sStorage->movingItemId);
        sStorage->movingItemId = itemId;
        SetMonFormPSS_ItemHold(&gPokemonStoragePtr->boxes[StorageGetCurrentBox()][cursorPos]);
    }
    else
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][cursorPos];
        itemId = GetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_HELD_ITEM);
        SetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_HELD_ITEM, &sStorage->movingItemId);
        sStorage->movingItemId = itemId;
        SetMonFormPSS_ItemHold(&mon->box);
    }

    id = GetItemIconIdxByPosition(CURSOR_AREA_IN_HAND, 0);
    SetItemIconAffineAnim(id, ITEM_ANIM_PUT_DOWN);
    SetItemIconCallback(id, ITEM_CB_SWAP_TO_MON, cursorArea, cursorPos);
    OrchidPC_ContentsChanged();
}

static void GiveItemToMon(u8 cursorArea, u8 cursorPos)
{
    u8 id;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    id = GetItemIconIdxByPosition(CURSOR_AREA_IN_HAND, 0);
    SetItemIconAffineAnim(id, ITEM_ANIM_PUT_DOWN);
    SetItemIconCallback(id, ITEM_CB_TO_MON, cursorArea, cursorPos);
    if (cursorArea == CURSOR_AREA_IN_BOX)
    {
        SetCurrentBoxMonData(cursorPos, MON_DATA_HELD_ITEM, &sStorage->movingItemId);
        SetBoxMonIconObjMode(cursorPos, ST_OAM_OBJ_NORMAL);
        SetMonFormPSS_ItemHold(&gPokemonStoragePtr->boxes[StorageGetCurrentBox()][cursorPos]);
    }
    else
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][cursorPos];
        SetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_HELD_ITEM, &sStorage->movingItemId);
        SetPartyMonIconObjMode(cursorPos, ST_OAM_OBJ_NORMAL);
        SetMonFormPSS_ItemHold(&mon->box);
    }
    OrchidPC_ContentsChanged();
}

static void MoveItemFromMonToBag(u8 cursorArea, u8 cursorPos)
{
    u8 id;
    enum Item itemId;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    itemId = ITEM_NONE;
    id = GetItemIconIdxByPosition(cursorArea, cursorPos);
    SetItemIconAffineAnim(id, ITEM_ANIM_DISAPPEAR);
    SetItemIconCallback(id, ITEM_CB_WAIT_ANIM, cursorArea, cursorPos);
    if (cursorArea == CURSOR_AREA_IN_BOX)
    {
        SetCurrentBoxMonData(cursorPos, MON_DATA_HELD_ITEM, &itemId);
        SetBoxMonIconObjMode(cursorPos, ST_OAM_OBJ_BLEND);
        SetMonFormPSS_ItemHold(&gPokemonStoragePtr->boxes[StorageGetCurrentBox()][cursorPos]);
    }
    else
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][cursorPos];
        SetMonData(&gParties[B_TRAINER_PLAYER][cursorPos], MON_DATA_HELD_ITEM, &itemId);
        SetPartyMonIconObjMode(cursorPos, ST_OAM_OBJ_BLEND);
        SetMonFormPSS_ItemHold(&mon->box);
    }
    OrchidPC_ContentsChanged();
}

static void MoveItemFromCursorToBag(void)
{
    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        u8 id = GetItemIconIdxByPosition(CURSOR_AREA_IN_HAND, 0);
        SetItemIconAffineAnim(id, ITEM_ANIM_PUT_AWAY);
        SetItemIconCallback(id, ITEM_CB_WAIT_ANIM, CURSOR_AREA_IN_HAND, 0);
    }
}

// The party menu is being closed, if the cursor is on
// a Pokémon that has a held item make sure it slides
// up along with the closing menu.
static void MoveHeldItemWithPartyMenu(void)
{
    s32 i;

    if (sStorage->boxOption != OPTION_MOVE_ITEMS)
        return;

    for (i = 0; i < MAX_ITEM_ICONS; i++)
    {
        if (sStorage->itemIcons[i].active
         && sStorage->itemIcons[i].area == CURSOR_AREA_IN_PARTY)
            SetItemIconCallback(i, ITEM_CB_HIDE_PARTY, CURSOR_AREA_IN_HAND, 0);
    }
}

static bool8 IsItemIconAnimActive(void)
{
    s32 i;

    for (i = 0; i < MAX_ITEM_ICONS; i++)
    {
        if (sStorage->itemIcons[i].active)
        {
            if (!sStorage->itemIcons[i].sprite->affineAnimEnded
              && sStorage->itemIcons[i].sprite->affineAnimBeginning)
                return TRUE;
            if (sStorage->itemIcons[i].sprite->callback != SpriteCallbackDummy
             && sStorage->itemIcons[i].sprite->callback != SpriteCB_ItemIcon_SetPosToCursor)
                return TRUE;
        }
    }
    return FALSE;
}

static bool8 IsMovingItem(void)
{
    s32 i;

    if (sStorage->boxOption == OPTION_MOVE_ITEMS)
    {
        for (i = 0; i < MAX_ITEM_ICONS; i++)
        {
            if (sStorage->itemIcons[i].active
             && sStorage->itemIcons[i].area == CURSOR_AREA_IN_HAND)
                return TRUE;
        }
    }
    return FALSE;
}

static const u8 *GetMovingItemName(void)
{
    return GetItemName(sStorage->movingItemId);
}

static enum Item GetMovingItemId(void)
{
    return sStorage->movingItemId;
}

static u8 GetNewItemIconIdx(void)
{
    u8 i;

    for (i = 0; i < MAX_ITEM_ICONS; i++)
    {
        if (!sStorage->itemIcons[i].active)
        {
            sStorage->itemIcons[i].active = TRUE;
            return i;
        }
    }
    return MAX_ITEM_ICONS;
}

static bool32 IsItemIconAtPosition(u8 cursorArea, u8 cursorPos)
{
    s32 i;

    for (i = 0; i < MAX_ITEM_ICONS; i++)
    {
        if (sStorage->itemIcons[i].active
         && sStorage->itemIcons[i].area == cursorArea
         && sStorage->itemIcons[i].pos == cursorPos)
            return TRUE;
    }
    return FALSE;
}

static u8 GetItemIconIdxByPosition(u8 cursorArea, u8 cursorPos)
{
    u8 i;

    for (i = 0; i < MAX_ITEM_ICONS; i++)
    {
        if (sStorage->itemIcons[i].active
         && sStorage->itemIcons[i].area == cursorArea
         && sStorage->itemIcons[i].pos == cursorPos)
            return i;
    }
    return MAX_ITEM_ICONS;
}

static u8 GetItemIconIdxBySprite(struct Sprite *sprite)
{
    u8 i;

    for (i = 0; i < MAX_ITEM_ICONS; i++)
    {
        if (sStorage->itemIcons[i].active
         && sStorage->itemIcons[i].sprite == sprite)
            return i;
    }
    return MAX_ITEM_ICONS;
}

static void SetItemIconPosition(u8 id, u8 cursorArea, u8 cursorPos)
{
    u8 x, y;

    if (id >= MAX_ITEM_ICONS)
        return;

    // Orchid: resting spots are hidden (hold tag + info disc instead); they are where the pick-up / put-down
    // flight starts or ends, 12 frames of (10, 21) / 16 px away from the carried spot (cursor + (4, -10)).
    switch (cursorArea)
    {
    case CURSOR_AREA_IN_BOX:
        x = cursorPos % IN_BOX_COLUMNS;
        y = cursorPos / IN_BOX_COLUMNS;
        sStorage->itemIcons[id].sprite->x = (OPC_SLOT_PITCH * x) + OPC_SLOT_X0 + 12;
        sStorage->itemIcons[id].sprite->y = (OPC_SLOT_PITCH * y) + OPC_SLOT_Y0 + 6;
        sStorage->itemIcons[id].sprite->oam.priority = 2;
        sStorage->itemIcons[id].sprite->invisible = TRUE;
        break;
    case CURSOR_AREA_IN_PARTY:
        sStorage->itemIcons[id].sprite->x = OPC_PSLOT_X0 + OPC_PSLOT_DX * (cursorPos % 2) + OPC_PICON_DX + 12;
        sStorage->itemIcons[id].sprite->y = OPC_PSLOT_Y0 + OPC_PSLOT_DY * (cursorPos / 2) + OPC_PICON_DY + 6;
        sStorage->itemIcons[id].sprite->oam.priority = 1;
        sStorage->itemIcons[id].sprite->invisible = TRUE;
        break;
    }

    sStorage->itemIcons[id].area = cursorArea;
    sStorage->itemIcons[id].pos = cursorPos;
}

static void LoadItemIconGfx(u8 id, const u32 *itemTiles, const u16 *itemPal)
{
    s32 i;

    if (id >= MAX_ITEM_ICONS)
        return;

    CpuFastFill(0, sStorage->itemIconBuffer, 0x200);
    DecompressDataWithHeaderWram(itemTiles, sStorage->tileBuffer);
    for (i = 0; i < 3; i++)
        CpuFastCopy(&sStorage->tileBuffer[i * 0x60], &sStorage->itemIconBuffer[i * 0x80], 0x60);

    CpuFastCopy(sStorage->itemIconBuffer, sStorage->itemIcons[id].tiles, 0x200);
    LoadPalette(itemPal, sStorage->itemIcons[id].palIndex, PLTT_SIZE_4BPP);
}

static void SetItemIconAffineAnim(u8 id, u8 animNum)
{
    if (id >= MAX_ITEM_ICONS)
        return;

    StartSpriteAffineAnim(sStorage->itemIcons[id].sprite, animNum);
}

#define sItemIconId data[0]
#define sState      data[0]
#define sCursorArea data[6]
#define sCursorPos  data[7]

static void SetItemIconCallback(u8 id, u8 callbackId, u8 cursorArea, u8 cursorPos)
{
    if (id >= MAX_ITEM_ICONS)
        return;

    switch (callbackId)
    {
    case ITEM_CB_WAIT_ANIM:
        sStorage->itemIcons[id].sprite->sItemIconId = id;
        sStorage->itemIcons[id].sprite->callback = SpriteCB_ItemIcon_WaitAnim;
        break;
    case ITEM_CB_TO_HAND:
        sStorage->itemIcons[id].sprite->sState = 0;
        sStorage->itemIcons[id].sprite->callback = SpriteCB_ItemIcon_ToHand;
        break;
    case ITEM_CB_TO_MON:
        sStorage->itemIcons[id].sprite->sState = 0;
        sStorage->itemIcons[id].sprite->sCursorArea = cursorArea;
        sStorage->itemIcons[id].sprite->sCursorPos = cursorPos;
        sStorage->itemIcons[id].sprite->callback = SpriteCB_ItemIcon_ToMon;
        break;
    case ITEM_CB_SWAP_TO_HAND:
        sStorage->itemIcons[id].sprite->sState = 0;
        sStorage->itemIcons[id].sprite->callback = SpriteCB_ItemIcon_SwapToHand;
        sStorage->itemIcons[id].sprite->sCursorArea = cursorArea;
        sStorage->itemIcons[id].sprite->sCursorPos = cursorPos;
        break;
    case ITEM_CB_SWAP_TO_MON:
        sStorage->itemIcons[id].sprite->sState = 0;
        sStorage->itemIcons[id].sprite->sCursorArea = cursorArea;
        sStorage->itemIcons[id].sprite->sCursorPos = cursorPos;
        sStorage->itemIcons[id].sprite->callback = SpriteCB_ItemIcon_SwapToMon;
        break;
    case ITEM_CB_HIDE_PARTY:
        // If cursor is on a Pokémon with a held item and
        // the player closes the party menu, have the held
        // item follow the Pokémon as the menu slides out
        sStorage->itemIcons[id].sprite->callback = SpriteCB_ItemIcon_HideParty;
        break;
    }
}

static void SetItemIconActive(u8 id, bool8 active)
{
    if (id >= MAX_ITEM_ICONS)
        return;

    sStorage->itemIcons[id].active = active;
    sStorage->itemIcons[id].sprite->invisible = (active == FALSE);
}

static void PrintItemDescription(void)
{
    const u8 *description;

    if (IsMovingItem())
        description = GetItemDescription(sStorage->movingItemId);
    else
        description = GetItemDescription(sStorage->displayMonItemId);

    FillWindowPixelBuffer(WIN_ITEM_DESC, PIXEL_FILL(1));
    AddTextPrinterParameterized5(WIN_ITEM_DESC, FONT_NORMAL, description, 4, 0, 0, NULL, 0, 1);
}

static void InitItemInfoWindow(void)
{
    sStorage->itemInfoWindowOffset = 21;
    LoadBgTiles(0, sItemInfoFrame_Gfx, 0x80, 0x13A);
    DrawItemInfoWindow(0);
}

static bool8 UpdateItemInfoWindowSlideIn(void)
{
    s32 i, pos;

    if (sStorage->itemInfoWindowOffset == 0)
        return FALSE;

    sStorage->itemInfoWindowOffset--;
    pos = 21 - sStorage->itemInfoWindowOffset;
    for (i = 0; i < pos; i++)
        WriteSequenceToBgTilemapBuffer(0, GetBgAttribute(0, BG_ATTR_BASETILE) + 0x14 + sStorage->itemInfoWindowOffset + i, i, 13, 1, 7, 15, 21);

    DrawItemInfoWindow(pos);
    return (sStorage->itemInfoWindowOffset != 0);
}

static bool8 UpdateItemInfoWindowSlideOut(void)
{
    s32 i, pos;

    if (sStorage->itemInfoWindowOffset == 22)
        return FALSE;

    if (sStorage->itemInfoWindowOffset == 0)
        FillBgTilemapBufferRect(0, 0, 21, 12, 1, 9, 17);

    sStorage->itemInfoWindowOffset++;
    pos = 21 - sStorage->itemInfoWindowOffset;
    for (i = 0; i < pos; i++)
    {
        WriteSequenceToBgTilemapBuffer(0, GetBgAttribute(0, BG_ATTR_BASETILE) + 0x14 + sStorage->itemInfoWindowOffset + i, i, 13, 1, 7, 15, 21);
    }

    if (pos >= 0)
        DrawItemInfoWindow(pos);

    FillBgTilemapBufferRect(0, 0, pos + 1, 12, 1, 9, 17);
    ScheduleBgCopyTilemapToVram(0);
    return TRUE;
}

static void DrawItemInfoWindow(u32 x)
{
    if (x != 0)
    {
        FillBgTilemapBufferRect(0, 0x13A, 0, 0xC, x, 1, 15);
        FillBgTilemapBufferRect(0, 0x93A, 0, 0x14, x, 1, 15);
    }
    FillBgTilemapBufferRect(0, 0x13B, x, 0xD, 1, 7, 15);
    FillBgTilemapBufferRect(0, 0x13C, x, 0xC, 1, 1, 15);
    FillBgTilemapBufferRect(0, 0x13D, x, 0x14, 1, 1, 15);
    ScheduleBgCopyTilemapToVram(0);
}

static void SpriteCB_ItemIcon_WaitAnim(struct Sprite *sprite)
{
    if (sprite->affineAnimEnded)
    {
        SetItemIconActive(sprite->sItemIconId, FALSE);
        sprite->callback = SpriteCallbackDummy;
    }
}

static void SpriteCB_ItemIcon_ToHand(struct Sprite *sprite)
{
    switch (sprite->sState)
    {
    case 0:
        sprite->data[1] = sprite->x << 4;
        sprite->data[2] = sprite->y << 4;
        sprite->data[3] = 10;
        sprite->data[4] = 21;
        sprite->data[5] = 0;
        sprite->sState++;
    case 1:
        sprite->invisible = FALSE;
        sprite->data[1] -= sprite->data[3];
        sprite->data[2] -= sprite->data[4];
        sprite->x = sprite->data[1] >> 4;
        sprite->y = sprite->data[2] >> 4;
        if (++sprite->data[5] > 11)
            sprite->callback = SpriteCB_ItemIcon_SetPosToCursor;
        break;
    }
}

// Orchid: the carried item floats OPC_LIFT px above the cursor slot, like a held Pokémon (mock state 8)
static void SpriteCB_ItemIcon_SetPosToCursor(struct Sprite *sprite)
{
    sprite->invisible = FALSE;
    sprite->x = sStorage->cursorSprite->x + 4;
    sprite->y = sStorage->cursorSprite->y + 4 - OPC_LIFT;
    sprite->oam.priority = 1;
}

static void SpriteCB_ItemIcon_ToMon(struct Sprite *sprite)
{
    switch (sprite->sState)
    {
    case 0:
        sprite->data[1] = sprite->x << 4;
        sprite->data[2] = sprite->y << 4;
        sprite->data[3] = 10;
        sprite->data[4] = 21;
        sprite->data[5] = 0;
        sprite->sState++;
    case 1:
        sprite->invisible = FALSE;
        sprite->data[1] += sprite->data[3];
        sprite->data[2] += sprite->data[4];
        sprite->x = sprite->data[1] >> 4;
        sprite->y = sprite->data[2] >> 4;
        if (++sprite->data[5] > 11)
        {
            SetItemIconPosition(GetItemIconIdxBySprite(sprite), sprite->sCursorArea, sprite->sCursorPos);
            sprite->callback = SpriteCallbackDummy;
        }
        break;
    }
}

static void SpriteCB_ItemIcon_SwapToHand(struct Sprite *sprite)
{
    switch (sprite->sState)
    {
    case 0:
        sprite->data[1] = sprite->x << 4;
        sprite->data[2] = sprite->y << 4;
        sprite->data[3] = 10;
        sprite->data[4] = 21;
        sprite->data[5] = 0;
        sprite->sState++;
    case 1:
        sprite->data[1] -= sprite->data[3];
        sprite->data[2] -= sprite->data[4];
        sprite->x = sprite->data[1] >> 4;
        sprite->y = sprite->data[2] >> 4;
        sprite->x2 = gSineTable[sprite->data[5] * 8] >> 4;
        sprite->invisible = FALSE;
        if (++sprite->data[5] > 11)
        {
            SetItemIconPosition(GetItemIconIdxBySprite(sprite), sprite->sCursorArea, sprite->sCursorPos);
            sprite->x2 = 0;
            sprite->callback = SpriteCB_ItemIcon_SetPosToCursor;
        }
        break;
    }
}

static void SpriteCB_ItemIcon_SwapToMon(struct Sprite *sprite)
{
    switch (sprite->sState)
    {
    case 0:
        sprite->data[1] = sprite->x << 4;
        sprite->data[2] = sprite->y << 4;
        sprite->data[3] = 10;
        sprite->data[4] = 21;
        sprite->data[5] = 0;
        sprite->sState++;
    case 1:
        sprite->data[1] += sprite->data[3];
        sprite->data[2] += sprite->data[4];
        sprite->x = sprite->data[1] >> 4;
        sprite->y = sprite->data[2] >> 4;
        sprite->x2 = -(gSineTable[sprite->data[5] * 8] >> 4);
        sprite->invisible = FALSE;
        if (++sprite->data[5] > 11)
        {
            SetItemIconPosition(GetItemIconIdxBySprite(sprite), sprite->sCursorArea, sprite->sCursorPos);
            sprite->callback = SpriteCallbackDummy;
            sprite->x2 = 0;
        }
        break;
    }
}

// Orchid: the party panel slides down to close
static void SpriteCB_ItemIcon_HideParty(struct Sprite *sprite)
{
    sprite->y += 8;
    if (sprite->y + sprite->y2 > DISPLAY_HEIGHT + 16)
    {
        sprite->callback = SpriteCallbackDummy;
        SetItemIconActive(GetItemIconIdxBySprite(sprite), FALSE);
    }
}

#undef sState
#undef sItemIconId
#undef sCursorArea
#undef sCursorPos


//------------------------------------------------------------------------------
//  SECTION: General utility
//------------------------------------------------------------------------------

// Functions here are general utility functions.
u8 StorageGetCurrentBox(void)
{
    return gPokemonStoragePtr->currentBox;
}

static void SetCurrentBox(u8 boxId)
{
    if (boxId < TOTAL_BOXES_COUNT)
        gPokemonStoragePtr->currentBox = boxId;
}

static struct BoxPokemon *GetCursorBoxMon(void)
{
    struct BoxPokemon *boxmon;
    if (sInPartyMenu)
        boxmon = &(gParties[B_TRAINER_PLAYER][sCursorPosition].box);
    else
        boxmon = GetBoxedMonPtr(StorageGetCurrentBox(), sCursorPosition);
    return boxmon;
}

u32 GetBoxMonDataAt(u8 boxId, u8 boxPosition, s32 request)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        return GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], request);
    else
        return 0;
}

void SetBoxMonDataAt(u8 boxId, u8 boxPosition, s32 request, const void *value)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        SetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], request, value);
}

u32 GetCurrentBoxMonData(u8 boxPosition, s32 request)
{
    return GetBoxMonDataAt(gPokemonStoragePtr->currentBox, boxPosition, request);
}

void SetCurrentBoxMonData(u8 boxPosition, s32 request, const void *value)
{
    SetBoxMonDataAt(gPokemonStoragePtr->currentBox, boxPosition, request, value);
}

u32 GetAndCopyBoxMonDataAt(u8 boxId, u8 boxPosition, s32 request, void *dst)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        return GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], request, dst);
    else
        return 0;
}

void SetBoxMonAt(u8 boxId, u8 boxPosition, struct BoxPokemon *src)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        gPokemonStoragePtr->boxes[boxId][boxPosition] = *src;
}

void ZeroBoxMonAt(u8 boxId, u8 boxPosition)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        ZeroBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition]);
}

void BoxMonAtToMon(u8 boxId, u8 boxPosition, struct Pokemon *dst)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        BoxMonToMon(&gPokemonStoragePtr->boxes[boxId][boxPosition], dst);
}

struct BoxPokemon *GetBoxedMonPtr(u8 boxId, u8 boxPosition)
{
    if (boxId < TOTAL_BOXES_COUNT && boxPosition < IN_BOX_COUNT)
        return &gPokemonStoragePtr->boxes[boxId][boxPosition];
    else
        return NULL;
}

u8 *GetBoxNamePtr(u8 boxId)
{
    if (boxId < TOTAL_BOXES_COUNT)
        return gPokemonStoragePtr->boxNames[boxId];
    else
        return NULL;
}

static u8 GetBoxWallpaper(u8 boxId)
{
    if (boxId < TOTAL_BOXES_COUNT)
        return gPokemonStoragePtr->boxWallpapers[boxId];
    else
        return 0;
}

static void SetBoxWallpaper(u8 boxId, u8 wallpaperId)
{
    if (boxId < TOTAL_BOXES_COUNT && wallpaperId < WALLPAPER_COUNT)
        gPokemonStoragePtr->boxWallpapers[boxId] = wallpaperId;
}

// For moving to the next Pokémon while viewing the summary screen
s16 AdvanceStorageMonIndex(struct BoxPokemon *boxMons, u8 currIndex, u8 maxIndex, u8 mode)
{
    s16 i;
    s16 direction = -1;

    if (mode == 0 || mode == 1)
        direction = 1;

    if (mode == 1 || mode == 3)
    {
        for (i = (s8)currIndex + direction; i >= 0 && i <= maxIndex; i += direction)
        {
            if (GetBoxMonData(&boxMons[i], MON_DATA_SPECIES) != SPECIES_NONE)
                return i;
        }
    }
    else
    {
        for (i = (s8)currIndex + direction; i >= 0 && i <= maxIndex; i += direction)
        {
            if (GetBoxMonData(&boxMons[i], MON_DATA_SPECIES) != SPECIES_NONE
                && !GetBoxMonData(&boxMons[i], MON_DATA_IS_EGG))
                return i;
        }
    }

    return -1;
}

bool8 CheckFreePokemonStorageSpace(void)
{
    s32 i, j;

    for (i = 0; i < TOTAL_BOXES_COUNT; i++)
    {
        for (j = 0; j < IN_BOX_COUNT; j++)
        {
            if (!GetBoxMonData(&gPokemonStoragePtr->boxes[i][j], MON_DATA_SANITY_HAS_SPECIES))
                return TRUE;
        }
    }

    return FALSE;
}

bool32 CheckBoxMonSanityAt(u32 boxId, u32 boxPosition)
{
    if (boxId < TOTAL_BOXES_COUNT
        && boxPosition < IN_BOX_COUNT
        && GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SANITY_HAS_SPECIES)
        && !GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SANITY_IS_EGG)
        && !GetBoxMonData(&gPokemonStoragePtr->boxes[boxId][boxPosition], MON_DATA_SANITY_IS_BAD_EGG))
        return TRUE;
    else
        return FALSE;
}

u32 CountStorageNonEggMons(void)
{
    s32 i, j;
    u32 count = 0;

    for (i = 0; i < TOTAL_BOXES_COUNT; i++)
    {
        for (j = 0; j < IN_BOX_COUNT; j++)
        {
            if (GetBoxMonData(&gPokemonStoragePtr->boxes[i][j], MON_DATA_SANITY_HAS_SPECIES)
                && !GetBoxMonData(&gPokemonStoragePtr->boxes[i][j], MON_DATA_SANITY_IS_EGG))
                count++;
        }
    }

    return count;
}

bool32 AnyStorageMonWithMove(enum Move move)
{
    enum Move moves[] = {move, MOVES_COUNT};
    s32 i, j;

    for (i = 0; i < TOTAL_BOXES_COUNT; i++)
    {
        for (j = 0; j < IN_BOX_COUNT; j++)
        {
            if (GetBoxMonData(&gPokemonStoragePtr->boxes[i][j], MON_DATA_SANITY_HAS_SPECIES)
                && !GetBoxMonData(&gPokemonStoragePtr->boxes[i][j], MON_DATA_SANITY_IS_EGG)
                && GetBoxMonData(&gPokemonStoragePtr->boxes[i][j], MON_DATA_KNOWN_MOVES, (u8 *)moves))
                return TRUE;
        }
    }

    return FALSE;
}


//------------------------------------------------------------------------------
//  SECTION: Walda
//------------------------------------------------------------------------------


void ResetWaldaWallpaper(void)
{
    gSaveBlock1Ptr->waldaPhrase.iconId = 0;
    gSaveBlock1Ptr->waldaPhrase.patternId = 0;
    gSaveBlock1Ptr->waldaPhrase.patternUnlocked = FALSE;
    gSaveBlock1Ptr->waldaPhrase.colors[0] = RGB(21, 25, 30);
    gSaveBlock1Ptr->waldaPhrase.colors[1] = RGB(6, 12, 24);
    gSaveBlock1Ptr->waldaPhrase.text[0] = EOS;
}

void SetWaldaWallpaperLockedOrUnlocked(bool32 unlocked)
{
    gSaveBlock1Ptr->waldaPhrase.patternUnlocked = unlocked;
}

bool32 IsWaldaWallpaperUnlocked(void)
{
    return gSaveBlock1Ptr->waldaPhrase.patternUnlocked;
}

u32 GetWaldaWallpaperPatternId(void)
{
    return gSaveBlock1Ptr->waldaPhrase.patternId;
}

void SetWaldaWallpaperPatternId(u8 id)
{
    if (id < ARRAY_COUNT(sWaldaWallpapers))
        gSaveBlock1Ptr->waldaPhrase.patternId = id;
}

u32 GetWaldaWallpaperIconId(void)
{
    return gSaveBlock1Ptr->waldaPhrase.iconId;
}

void SetWaldaWallpaperIconId(u8 id)
{
    if (id < ARRAY_COUNT(sWaldaWallpaperIcons))
        gSaveBlock1Ptr->waldaPhrase.iconId = id;
}

u16 *GetWaldaWallpaperColorsPtr(void)
{
    return gSaveBlock1Ptr->waldaPhrase.colors;
}

void SetWaldaWallpaperColors(u16 color1, u16 color2)
{
    gSaveBlock1Ptr->waldaPhrase.colors[0] = color1;
    gSaveBlock1Ptr->waldaPhrase.colors[1] = color2;
}

u8 *GetWaldaPhrasePtr(void)
{
    return gSaveBlock1Ptr->waldaPhrase.text;
}

void SetWaldaPhrase(const u8 *src)
{
    StringCopy(gSaveBlock1Ptr->waldaPhrase.text, src);
}

bool32 IsWaldaPhraseEmpty(void)
{
    return (gSaveBlock1Ptr->waldaPhrase.text[0] == EOS);
}


//------------------------------------------------------------------------------
//  SECTION: UnkUtil
//
//  Some data transfer utility that goes functionally unused.
//  It gets initialized with UnkUtil_Init, and run every vblank in Pokémon
//  Storage with UnkUtil_Run, but neither of the Add functions are ever used,
//  so UnkUtil_Run performs no actions.
//------------------------------------------------------------------------------

void UpdateSpeciesSpritePSS(struct BoxPokemon *boxMon)
{
    enum Species species = GetBoxMonData(boxMon, MON_DATA_SPECIES);
    bool32 isShiny = GetBoxMonData(boxMon, MON_DATA_IS_SHINY);
    u32 pid = GetBoxMonData(boxMon, MON_DATA_PERSONALITY);
    bool32 isEgg = GetBoxMonData(boxMon, MON_DATA_IS_EGG);

    // Update front sprite
    sStorage->displayMonSpecies = species;
    sStorage->displayMonPalette = GetMonSpritePalFromSpeciesAndPersonalityIsEgg(species, isShiny, pid, isEgg);
    sStorage->displayMonIsEgg = isEgg;
    if (!sJustOpenedBag)
    {
        if (sRefreshDisplayMonGfx)
        {
            LoadDisplayMonGfx(species, pid, isEgg);
            StartDisplayMonMosaicEffect();
            sRefreshDisplayMonGfx = FALSE;
        }

        // Recreate icon sprite
        if (sInPartyMenu)
        {
            DestroyPartyMonIcon(sCursorPosition);
            CreatePartyMonSprite(sCursorPosition, TRUE);
        }
        else
        {
            DestroyBoxMonIconAtPosition(sCursorPosition);
            CreateBoxMonIconAtPos(sCursorPosition);
        }
    }
    sJustOpenedBag = FALSE;
}

void ChooseMonFromStorage(void)
{
    EnterPokeStorage(OPTION_SELECT_MON);
}

void RemoveSelectedPcMon(struct Pokemon *mon)
{
    struct BoxPokemon *boxmon = GetBoxedMonPtr(gSpecialVar_MonBoxId, gSpecialVar_MonBoxPos);
    BoxMonToMon(boxmon, mon);
    ZeroBoxMonData(boxmon);
}
