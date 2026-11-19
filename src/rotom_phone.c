// Rotom Phone home screen (replaces the PokéNav main menu).
// Design: dev_scripts/orchid_ui/DESIGN.md "Rotom Phone", mockup mock_phone.py, assets export_phone.py.
//
// Layers
//   BG0  text windows: clock, app labels, Rotom's line            (charblock 0, 256x512 so the slide-up never wraps)
//   BG1  news ticker: a 256px ring window scrolled with HOFS, clipped to the status strip by WIN0
//   BG2  coral shell, screen, glare, eye notch, status bar art     (charblock 1, 256x512)
//   BG3  Orchid grid backdrop                                      (charblock 1, after the shell tiles)
//   OBJ  gold selection pill (behind), 4 app tiles, quest badge
// Rotom's eye (left notch) glows by swapping two shell palette colours.
// Before FLAG_SYS_PHONE_ACTIVE the phone is "offline": X-eyed Rotom face, empty signal, clock only.
#include "global.h"
#include "rotom_phone.h"
#include "bg.h"
#include "decompress.h"
#include "event_data.h"
#include "fieldmap.h"
#include "gpu_regs.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "random.h"
#include "region_map.h"
#include "rtc.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/flags.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "data/rotom_phone_layout.h"
#include "data/rotom_phone_news.h"

static const u32 sShell_Gfx[] = INCGFX_U32("graphics/rotom_phone/shell.png", ".4bpp.smol");
static const u32 sShell_Tilemap[] = INCGFX_U32("graphics/rotom_phone/shell.bin", ".smolTM");
static const u32 sShellOffline_Tilemap[] = INCGFX_U32("graphics/rotom_phone/shell_off.bin", ".smolTM");
static const u16 sShell_Pal[] = INCGFX_U16("graphics/rotom_phone/shell.pal", ".gbapal");
static const u16 sText_Pal[] = INCGFX_U16("graphics/rotom_phone/text.pal", ".gbapal");
static const u8 sApps_Gfx[] = INCGFX_U8("graphics/rotom_phone/apps.png", ".4bpp");
static const u16 sApps_Pal[] = INCGFX_U16("graphics/rotom_phone/apps.pal", ".gbapal");
static const u8 sPill_Gfx[] = INCGFX_U8("graphics/rotom_phone/pill.png", ".4bpp");
static const u8 sBadge_Gfx[] = INCGFX_U8("graphics/rotom_phone/badge.png", ".4bpp");
static const u16 sUi_Pal[] = INCGFX_U16("graphics/rotom_phone/ui.pal", ".gbapal");

// BG palettes
#define PAL_SHELL       0
#define PAL_GRID        2
#define PAL_TEXT        15
// shell.pal colour indices that swap when Rotom's eye glows (export_phone.py S_PUPIL / S_HILITE)
#define SHELL_PUPIL     11
#define SHELL_HILITE    12

// text.pal
#define TXT_WHITE   1
#define TXT_SHADOW  2
#define TXT_GREY    3
#define TXT_DEEP    4
#define TXT_INK     5
#define TXT_GOLD_DK 6
#define TXT_GOLD    7

#define TAG_PHONE_APPS      0x7A10
#define TAG_PHONE_APPS_DIM  0x7A11
#define TAG_PHONE_PILL      0x7A12
#define TAG_PHONE_BADGE     0x7A13
#define TAG_PHONE_UI_PAL    0x7A14

#define SLIDE_FRAMES    14
#define NEWS_GAP        14      // px between headlines; the gold dot sits in the middle
#define TICKER_Y        31      // top of the ticker strip on screen
#define TICKER_BOTTOM   45
#define TICKER_FRAMES_PER_PX 2  // ticker speed: move 1px every N frames (1 = 60 px/s, 2 = 30 px/s)
#define EYE_BLINK       18      // frames on / off while quests are unread

enum
{
    WIN_CLOCK,
    WIN_LABELS,
    WIN_ROTOM,
    WIN_TICKER,
    WIN_SCRATCH_A,
    WIN_SCRATCH_B,
    WIN_COUNT
};

static const struct WindowTemplate sWindowTemplates[] =
{
    [WIN_CLOCK]     = { .bg = 0, .tilemapLeft = 21, .tilemapTop = 3, .width = 4, .height = 3, .paletteNum = PAL_TEXT, .baseBlock = 1 },
    [WIN_LABELS]    = { .bg = 0, .tilemapLeft = 4, .tilemapTop = 10, .width = 23, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 13 },
    [WIN_ROTOM]     = { .bg = 0, .tilemapLeft = 5, .tilemapTop = 12, .width = 21, .height = 4, .paletteNum = PAL_TEXT, .baseBlock = 59 },
    // BG1: the ticker ring (window row 0 shows at y TICKER_Y via VOFS) and two off-screen render buffers
    [WIN_TICKER]    = { .bg = 1, .tilemapLeft = 0, .tilemapTop = 4, .width = 32, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 1 },
    [WIN_SCRATCH_A] = { .bg = 1, .tilemapLeft = 0, .tilemapTop = 8, .width = 32, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 65 },
    [WIN_SCRATCH_B] = { .bg = 1, .tilemapLeft = 0, .tilemapTop = 10, .width = 32, .height = 2, .paletteNum = PAL_TEXT, .baseBlock = 129 },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 24, .screenSize = 2, .paletteMode = 0, .priority = 0, .baseTile = 0 },
    { .bg = 1, .charBaseIndex = 2, .mapBaseIndex = 28, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0 },
    { .bg = 2, .charBaseIndex = 1, .mapBaseIndex = 26, .screenSize = 2, .paletteMode = 0, .priority = 2, .baseTile = 0 },
    { .bg = 3, .charBaseIndex = 1, .mapBaseIndex = 29, .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0 },
};

static const u8 sColors_White[] = {0, TXT_WHITE, TXT_DEEP};
static const u8 sColors_Rotom[] = {0, TXT_WHITE, TXT_SHADOW};
static const u8 sColors_LabelSel[] = {0, TXT_INK, TXT_GOLD_DK};
static const u8 sColors_Label[] = {0, TXT_GREY, TXT_DEEP};

// ---------------------------------------------------------------- app table
struct PhoneApp
{
    const u8 *name;
    u8 iconFrame;
    void (*rotomText)(u8 *dest);    // Rotom's two lines ('\n' separated)
    bool32 (*isUnlocked)(void);
    void (*launch)(void);           // sets the next CB2; the app returns with CB2_ReturnToRotomPhone
};

static void RotomText_Map(u8 *dest);
static void RotomText_Call(u8 *dest);
static void RotomText_Quests(u8 *dest);
static void RotomText_Radio(u8 *dest);
static bool32 AlwaysUnlocked(void);
static void Launch_Map(void);

static const struct PhoneApp sPhoneApps[PHONE_APP_COUNT] =
{
    [PHONE_APP_MAP]    = { COMPOUND_STRING("MAP"),    0, RotomText_Map,    AlwaysUnlocked, Launch_Map },
    [PHONE_APP_CALL]   = { COMPOUND_STRING("CALL"),   1, RotomText_Call,   AlwaysUnlocked, PhoneApp_LaunchCall },
    [PHONE_APP_QUESTS] = { COMPOUND_STRING("QUESTS"), 2, RotomText_Quests, AlwaysUnlocked, PhoneApp_LaunchQuests },
    [PHONE_APP_RADIO]  = { COMPOUND_STRING("RADIO"),  3, RotomText_Radio,  AlwaysUnlocked, PhoneApp_LaunchRadio },
};
#define ICON_FRAME_LOCKED 4

static const u8 sText_Locked[] = _("Bzzt… this app isn't\ninstalled yet!");

// ---------------------------------------------------------------- state
struct RotomPhone
{
    u16 bg2Tilemap[32 * 64];
    u16 bg3Tilemap[32 * 32];
    bool8 offline;
    u8 cursor;
    u8 slideFrame;
    u8 state;
    u8 gridTimer;
    u8 lastMinute;
    u8 badge;
    bool8 eyeOn;
    u16 frameCounter;
    u8 appSpriteIds[PHONE_APP_COUNT];
    u8 pillSpriteId;
    u8 badgeSpriteId;
    // news ticker
    u8 newsOrder[ARRAY_COUNT(sPhoneNews)];
    u8 newsCount;
    u8 newsNext;            // index into newsOrder of the next headline to render
    u32 scroll;             // virtual px scrolled (virtual x 0 starts at the clip's right edge)
    u32 filledCol;          // ring columns (8px) written so far, in virtual columns
    u32 headStart[2];       // virtual px where the headline in scratch A / B starts
    u16 headEndCol[2];      // last virtual column (incl. the gold dot) of each scratch's headline
    u8 headScratch;         // which scratch holds the newest headline
    u32 nextHeadX;          // virtual px where the next headline will start
    u8 tickerWait;          // frames since the last 1px step (see TICKER_FRAMES_PER_PX)
    void (*exitCallback)(void);
};

static EWRAM_DATA struct RotomPhone *sPhone = NULL;
static EWRAM_DATA u8 sLastCursor = 0;

enum
{
    STATE_SLIDE_IN,
    STATE_INPUT,
    STATE_FADE_OUT,
};

static void InitPhone(bool32 slideIn);
static void CB2_SetupPhone(void);
static void CB2_Phone(void);
static void VBlankCB_Phone(void);
static void Task_Phone(u8 taskId);
static void PrintClock(void);
static void PrintLabels(void);
static void PrintRotomLine(void);
static void UpdateSprites(void);
static void Ticker_Init(void);
static void Ticker_Update(void);
static void SetPhoneYOffset(s32 dy);

void CB2_InitRotomPhone(void)
{
    InitPhone(TRUE);
}

void CB2_ReturnToRotomPhone(void)
{
    InitPhone(FALSE);
}

static void InitPhone(bool32 slideIn)
{
    sPhone = AllocZeroed(sizeof(*sPhone));
    sPhone->offline = !FlagGet(FLAG_SYS_PHONE_ACTIVE);
    sPhone->cursor = sLastCursor < PHONE_APP_COUNT ? sLastCursor : 0;
    sPhone->slideFrame = slideIn ? 0 : SLIDE_FRAMES;
    sPhone->lastMinute = 0xFF;
    gMain.state = 0;
    SetMainCallback2(CB2_SetupPhone);
}

static u32 CountBadges(void)
{
    u32 i, n = 0;
    for (i = FLAG_BADGE01_GET; i <= FLAG_BADGE08_GET; i++)
    {
        if (FlagGet(i))
            n++;
    }
    return n;
}

static void LoadPhoneGraphics(void)
{
    u32 x, y;
    static const struct SpriteSheet sheets[] =
    {
        { sApps_Gfx, 32 * 32 / 2 * 5, TAG_PHONE_APPS },
        { sPill_Gfx, 64 * 64 / 2, TAG_PHONE_PILL },
        { sBadge_Gfx, 16 * 16 / 2 * 9, TAG_PHONE_BADGE },
        {}
    };
    static const struct SpritePalette pals[] =
    {
        { sApps_Pal, TAG_PHONE_APPS },
        { sApps_Pal + 16, TAG_PHONE_APPS_DIM },
        { sUi_Pal, TAG_PHONE_UI_PAL },
        {}
    };

    DecompressAndCopyTileDataToVram(2, sShell_Gfx, 0, 0, 0);
    DecompressDataWithHeaderWram(sPhone->offline ? sShellOffline_Tilemap : sShell_Tilemap, sPhone->bg2Tilemap);
    for (y = 0; y < 32; y++)
    {
        for (x = 0; x < 32; x++)
            sPhone->bg3Tilemap[y * 32 + x] = (PHONE_SHELL_TILES + (x & 1) + (y & 1) * 2) | (PAL_GRID << 12);
    }
    LoadPalette(sShell_Pal, BG_PLTT_ID(0), 3 * PLTT_SIZE_4BPP);
    LoadPalette(sText_Pal, BG_PLTT_ID(PAL_TEXT), PLTT_SIZE_4BPP);
    LoadSpriteSheets(sheets);
    LoadSpritePalettes(pals);
}

// ---------------------------------------------------------------- sprites
static const struct OamData sOam_32 = { .shape = SPRITE_SHAPE(32x32), .size = SPRITE_SIZE(32x32), .priority = 1 };
static const struct OamData sOam_64 = { .shape = SPRITE_SHAPE(64x64), .size = SPRITE_SIZE(64x64), .priority = 1 };
static const struct OamData sOam_16 = { .shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 1 };

#define FRAME_ANIM(n, t) static const union AnimCmd sAnim_##n[] = { ANIMCMD_FRAME(t, 0), ANIMCMD_END };
FRAME_ANIM(F0, 0) FRAME_ANIM(F1, 16) FRAME_ANIM(F2, 32) FRAME_ANIM(F3, 48) FRAME_ANIM(F4, 64)
FRAME_ANIM(B0, 0) FRAME_ANIM(B1, 4) FRAME_ANIM(B2, 8) FRAME_ANIM(B3, 12) FRAME_ANIM(B4, 16)
FRAME_ANIM(B5, 20) FRAME_ANIM(B6, 24) FRAME_ANIM(B7, 28) FRAME_ANIM(B8, 32)
static const union AnimCmd *const sAnims_Apps[] = { sAnim_F0, sAnim_F1, sAnim_F2, sAnim_F3, sAnim_F4 };
static const union AnimCmd *const sAnims_Badge[] = { sAnim_B0, sAnim_B1, sAnim_B2, sAnim_B3, sAnim_B4, sAnim_B5, sAnim_B6, sAnim_B7, sAnim_B8 };

static const struct SpriteTemplate sTemplate_App =
{
    .tileTag = TAG_PHONE_APPS, .paletteTag = TAG_PHONE_APPS, .oam = &sOam_32, .anims = sAnims_Apps,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_Pill =
{
    .tileTag = TAG_PHONE_PILL, .paletteTag = TAG_PHONE_UI_PAL, .oam = &sOam_64, .anims = gDummySpriteAnimTable,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_Badge =
{
    .tileTag = TAG_PHONE_BADGE, .paletteTag = TAG_PHONE_UI_PAL, .oam = &sOam_16, .anims = sAnims_Badge,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static void CreatePhoneSprites(void)
{
    u32 i;

    if (sPhone->offline)
        return;
    for (i = 0; i < PHONE_APP_COUNT; i++)
    {
        u8 id = CreateSprite(&sTemplate_App, PHONE_APP_X(i) + 5 + 16, PHONE_APP_TILE_Y + 16, 5);
        sPhone->appSpriteIds[i] = id;
        if (sPhoneApps[i].isUnlocked())
        {
            StartSpriteAnim(&gSprites[id], sPhoneApps[i].iconFrame);
        }
        else
        {
            StartSpriteAnim(&gSprites[id], ICON_FRAME_LOCKED);
            gSprites[id].oam.paletteNum = IndexOfSpritePaletteTag(TAG_PHONE_APPS_DIM);
        }
    }
    sPhone->pillSpriteId = CreateSprite(&sTemplate_Pill, 0, PHONE_PILL_Y + 32, 10);
    // mock: badge disc at tile (+27, +2); sprite origin = tile (+20, -6)
    sPhone->badgeSpriteId = CreateSprite(&sTemplate_Badge, PHONE_APP_X(PHONE_APP_QUESTS) + 5 + 20 + 8,
                                         PHONE_APP_TILE_Y - 6 + 8, 0);
    sPhone->badge = PhoneApp_CountQuestRewards();
    if (sPhone->badge > 9)
        sPhone->badge = 9;
    StartSpriteAnim(&gSprites[sPhone->badgeSpriteId], sPhone->badge ? sPhone->badge - 1 : 0);
    UpdateSprites();
}

static s32 SlideOffset(void)
{
    s32 left = SLIDE_FRAMES - sPhone->slideFrame;
    // ease-out cubic: 160 * (1 - t)^3
    return DISPLAY_HEIGHT * left * left * left / (SLIDE_FRAMES * SLIDE_FRAMES * SLIDE_FRAMES);
}

static void UpdateSprites(void)
{
    u32 i;
    s32 dy = SlideOffset();
    s32 bob;

    if (sPhone->offline)
        return;
    // selected tile bobs 0,-1,-2,-1 (8 frames a step)
    bob = (sPhone->frameCounter >> 3) & 3;
    bob = (bob == 0) ? 0 : (bob == 2) ? -2 : -1;
    for (i = 0; i < PHONE_APP_COUNT; i++)
    {
        struct Sprite *s = &gSprites[sPhone->appSpriteIds[i]];
        s->y = PHONE_APP_TILE_Y + 16 + dy + (i == sPhone->cursor ? bob : 0);
        s->invisible = (PHONE_APP_TILE_Y + dy >= DISPLAY_HEIGHT);
    }
    gSprites[sPhone->pillSpriteId].x = PHONE_APP_X(sPhone->cursor) - 1 + 32;
    gSprites[sPhone->pillSpriteId].y = PHONE_PILL_Y + 32 + dy;
    gSprites[sPhone->pillSpriteId].invisible = (PHONE_PILL_Y + dy + 64 > 255);
    gSprites[sPhone->badgeSpriteId].y = PHONE_APP_TILE_Y - 6 + 8 + dy
                                        + (sPhone->cursor == PHONE_APP_QUESTS ? bob : 0);
    gSprites[sPhone->badgeSpriteId].invisible = (sPhone->badge == 0 || PHONE_APP_TILE_Y - 6 + dy >= DISPLAY_HEIGHT);
}

// ---------------------------------------------------------------- setup
static void CB2_SetupPhone(void)
{
    switch (gMain.state)
    {
    case 0:
        SetVBlankCallback(NULL);
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        DmaClearLarge16(3, (void *)(VRAM), VRAM_SIZE, 0x1000);
        DmaClear32(3, OAM, OAM_SIZE);
        DmaClear16(3, PLTT, PLTT_SIZE);
        ResetBgsAndClearDma3BusyFlags(0);
        InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
        SetBgTilemapBuffer(2, sPhone->bg2Tilemap);
        SetBgTilemapBuffer(3, sPhone->bg3Tilemap);
        InitWindows(sWindowTemplates);
        DeactivateAllTextPrinters();
        gMain.state++;
        break;
    case 1:
        ResetPaletteFade();
        ScanlineEffect_Stop();
        ResetTasks();
        ResetSpriteData();
        FreeAllSpritePalettes();
        ResetTempTileDataBuffers();
        LoadPhoneGraphics();
        gMain.state++;
        break;
    case 2:
        if (!FreeTempTileDataBuffersIfPossible())
            gMain.state++;
        break;
    case 3:
        CreatePhoneSprites();
        PutWindowTilemap(WIN_CLOCK);
        PrintClock();
        if (!sPhone->offline)
        {
            PutWindowTilemap(WIN_LABELS);
            PutWindowTilemap(WIN_ROTOM);
            PutWindowTilemap(WIN_TICKER);
            PrintLabels();
            PrintRotomLine();
            Ticker_Init();
        }
        gMain.state++;
        break;
    case 4:
        ChangeBgX(0, 0, BG_COORD_SET);
        ChangeBgX(2, 0, BG_COORD_SET);
        ChangeBgX(3, 0, BG_COORD_SET);
        ChangeBgY(3, 0, BG_COORD_SET);
        SetPhoneYOffset(SlideOffset());
        // WIN0 = ticker clip: inside shows everything, outside hides BG1
        SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(PHONE_TICK_L, PHONE_TICK_R + 1));
        SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(TICKER_Y, TICKER_BOTTOM));
        SetGpuReg(REG_OFFSET_WININ, WININ_WIN0_ALL);
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0 | WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP | DISPCNT_WIN0_ON);
        ShowBg(0);
        ShowBg(2);
        ShowBg(3);
        if (sPhone->slideFrame >= SLIDE_FRAMES && !sPhone->offline)
            ShowBg(1);
        CopyBgTilemapBufferToVram(0);
        CopyBgTilemapBufferToVram(1);
        CopyBgTilemapBufferToVram(2);
        CopyBgTilemapBufferToVram(3);
        gMain.state++;
        break;
    case 5:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB_Phone);
        SetMainCallback2(CB2_Phone);
        sPhone->state = sPhone->slideFrame < SLIDE_FRAMES ? STATE_SLIDE_IN : STATE_INPUT;
        CreateTask(Task_Phone, 0);
        if (sPhone->slideFrame < SLIDE_FRAMES)
            PlaySE(SE_POKENAV_ON);
        break;
    }
}

static void CB2_Phone(void)
{
    // Orchid grid backdrop: diagonal, 1px every 4 frames
    if ((++sPhone->gridTimer & 3) == 0)
    {
        ChangeBgX(3, 1 << 8, BG_COORD_SUB);
        ChangeBgY(3, 1 << 8, BG_COORD_SUB);
    }
    RunTasks();
    RunTextPrinters();
    AnimateSprites();
    BuildOamBuffer();
    DoScheduledBgTilemapCopiesToVram();
    UpdatePaletteFade();
}

static void VBlankCB_Phone(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void SetPhoneYOffset(s32 dy)
{
    // BG0 / BG2 are 512 tall, so rows above the phone come from the blank lower half
    ChangeBgY(0, ((512 - dy) & 511) << 8, BG_COORD_SET);
    ChangeBgY(2, ((512 - dy) & 511) << 8, BG_COORD_SET);
    ChangeBgY(1, ((1 - dy) & 255) << 8, BG_COORD_SET);   // window row 0 at y TICKER_Y (tile row 4 = y 32)
}

// ---------------------------------------------------------------- input
static void SetEye(bool32 on)
{
    if (sPhone->eyeOn == on)
        return;
    sPhone->eyeOn = on;
    LoadPalette(&sShell_Pal[(on ? 16 : 0) + SHELL_PUPIL], BG_PLTT_ID(PAL_SHELL) + SHELL_PUPIL, 2 * sizeof(u16));
}

static void MoveCursor(s32 delta)
{
    sPhone->cursor = (sPhone->cursor + PHONE_APP_COUNT + delta) % PHONE_APP_COUNT;
    sLastCursor = sPhone->cursor;
    PlaySE(SE_SELECT);
    PrintLabels();
    PrintRotomLine();
}

static void FreePhone(void)
{
    FreeAllWindowBuffers();
    Free(sPhone);
    sPhone = NULL;
}

static void Task_Phone(u8 taskId)
{
    sPhone->frameCounter++;
    if (sPhone->frameCounter % 32 == 0)
        PrintClock();
    if (!sPhone->offline)
    {
        Ticker_Update();
        SetEye(sPhone->badge != 0 && (sPhone->frameCounter / EYE_BLINK) % 2 == 0);
    }

    switch (sPhone->state)
    {
    case STATE_SLIDE_IN:
        sPhone->slideFrame++;
        SetPhoneYOffset(SlideOffset());
        if (sPhone->slideFrame >= SLIDE_FRAMES)
        {
            if (!sPhone->offline)
                ShowBg(1);
            sPhone->state = STATE_INPUT;
        }
        break;
    case STATE_INPUT:
        if (gPaletteFade.active)
            break;
        if (JOY_NEW(B_BUTTON | START_BUTTON))
        {
            PlaySE(SE_POKENAV_OFF);
            sPhone->exitCallback = CB2_ReturnToFieldWithOpenMenu;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            sPhone->state = STATE_FADE_OUT;
        }
        else if (sPhone->offline)
        {
            break;
        }
        else if (JOY_REPEAT(DPAD_LEFT))
        {
            MoveCursor(-1);
        }
        else if (JOY_REPEAT(DPAD_RIGHT))
        {
            MoveCursor(1);
        }
        else if (JOY_NEW(A_BUTTON))
        {
            const struct PhoneApp *app = &sPhoneApps[sPhone->cursor];
            if (!app->isUnlocked())
            {
                PlaySE(SE_FAILURE);
                break;
            }
            PlaySE(SE_SELECT);
            sPhone->exitCallback = app->launch;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            sPhone->state = STATE_FADE_OUT;
        }
        break;
    case STATE_FADE_OUT:
        if (!gPaletteFade.active)
        {
            void (*next)(void) = sPhone->exitCallback;
            DestroyTask(taskId);
            SetGpuReg(REG_OFFSET_DISPCNT, 0);
            FreePhone();
            if (next == CB2_ReturnToFieldWithOpenMenu)
                SetMainCallback2(next);
            else
                next();
            return;
        }
        break;
    }
    UpdateSprites();
}

// ---------------------------------------------------------------- text
static void PrintClock(void)
{
    u8 *p;

    RtcCalcLocalTime();
    if (gLocalTime.minutes == sPhone->lastMinute)
        return;
    sPhone->lastMinute = gLocalTime.minutes;
    p = ConvertIntToDecimalStringN(gStringVar4, gLocalTime.hours, STR_CONV_MODE_LEFT_ALIGN, 2);
    *p++ = CHAR_COLON;
    ConvertIntToDecimalStringN(p, gLocalTime.minutes, STR_CONV_MODE_LEADING_ZEROS, 2);
    FillWindowPixelBuffer(WIN_CLOCK, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_CLOCK, FONT_SMALL, 2, 7, 0, 0, sColors_White, TEXT_SKIP_DRAW, gStringVar4);
    CopyWindowToVram(WIN_CLOCK, COPYWIN_GFX);
}

static void PrintLabels(void)
{
    u32 i;

    FillWindowPixelBuffer(WIN_LABELS, PIXEL_FILL(0));
    for (i = 0; i < PHONE_APP_COUNT; i++)
    {
        const u8 *name = sPhoneApps[i].name;
        s32 x = PHONE_APP_X(i) + 19 - GetStringWidth(FONT_SMALL, name, 0) / 2 - 32;
        AddTextPrinterParameterized4(WIN_LABELS, FONT_SMALL, x, PHONE_LABEL_Y - 80, 0, 0,
                                     i == sPhone->cursor ? sColors_LabelSel : sColors_Label, TEXT_SKIP_DRAW, name);
    }
    CopyWindowToVram(WIN_LABELS, COPYWIN_GFX);
}

static void PrintRotomLine(void)
{
    u8 *nl;
    const struct PhoneApp *app = &sPhoneApps[sPhone->cursor];

    if (app->isUnlocked())
        app->rotomText(gStringVar4);
    else
        StringCopy(gStringVar4, sText_Locked);
    FillWindowPixelBuffer(WIN_ROTOM, PIXEL_FILL(0));
    // two lines at a 12px pitch (DESIGN.md: normal font, 12px pitch), printed separately
    nl = gStringVar4;
    while (*nl != EOS && *nl != CHAR_NEWLINE)
        nl++;
    if (*nl == CHAR_NEWLINE)
    {
        *nl = EOS;
        AddTextPrinterParameterized4(WIN_ROTOM, FONT_NORMAL, 0, 14, 0, 0, sColors_Rotom, TEXT_SKIP_DRAW, nl + 1);
    }
    AddTextPrinterParameterized4(WIN_ROTOM, FONT_NORMAL, 0, 2, 0, 0, sColors_Rotom, TEXT_SKIP_DRAW, gStringVar4);
    CopyWindowToVram(WIN_ROTOM, COPYWIN_GFX);
}

static void RotomText_Map(u8 *dest)
{
    StringCopy(gStringVar1, GetRegionMapRegionName());
    StringExpandPlaceholders(dest, COMPOUND_STRING("Bzzt! Where to? I'll pull\nup the {STR_VAR_1} map!"));
}

static void RotomText_Call(u8 *dest)
{
    ConvertIntToDecimalStringN(gStringVar1, PhoneApp_CountContacts(), STR_CONV_MODE_LEFT_ALIGN, 3);
    StringExpandPlaceholders(dest, COMPOUND_STRING("Want to ring someone?\nI've got {STR_VAR_1} contacts!"));
}

static void RotomText_Quests(u8 *dest)
{
    u32 n = PhoneApp_CountQuestRewards();
    if (n == 0)
    {
        StringCopy(dest, COMPOUND_STRING("Need something to do?\nLet's check your quests!"));
        return;
    }
    ConvertIntToDecimalStringN(gStringVar1, n, STR_CONV_MODE_LEFT_ALIGN, 2);
    StringExpandPlaceholders(dest, n == 1 ? COMPOUND_STRING("1 reward to collect! People\nare counting on you, bzzt!")
                                          : COMPOUND_STRING("{STR_VAR_1} rewards to collect! People\nare counting on you, bzzt!"));
}

static void RotomText_Radio(u8 *dest)
{
    PhoneApp_RadioRotomText(dest);
}

static bool32 AlwaysUnlocked(void)
{
    return TRUE;
}

static void Launch_Map(void)
{
    FieldInitRegionMap(CB2_ReturnToRotomPhone);
}

// ---------------------------------------------------------------- news ticker
// The ticker is a 256px ring window on BG1. Each headline is printed (pixel-aligned to its
// virtual x) into one of two off-screen scratch windows; 8px tile columns are OR-ed from the
// scratches into the ring just before they scroll into the clip. HOFS does the rest.

static void Ticker_Init(void)
{
    u32 i, j, n = 0, badges = CountBadges();

    for (i = 0; i < ARRAY_COUNT(sPhoneNews); i++)
    {
        const struct PhoneNews *news = &sPhoneNews[i];
        if (badges < news->minBadges || badges > news->maxBadges)
            continue;
        if (news->flag != 0 && FlagGet(news->flag) != news->flagState)
            continue;
        sPhone->newsOrder[n++] = i;
    }
    for (i = n; i > 1; i--)    // Fisher-Yates
    {
        u8 tmp;
        j = Random() % i;
        tmp = sPhone->newsOrder[i - 1];
        sPhone->newsOrder[i - 1] = sPhone->newsOrder[j];
        sPhone->newsOrder[j] = tmp;
    }
    sPhone->newsCount = n;
    sPhone->newsNext = 0;
    sPhone->scroll = PHONE_TICK_R - PHONE_TICK_L - 2;    // open with the strip already full (as mocked)
    sPhone->filledCol = 0;
    sPhone->nextHeadX = 0;
    sPhone->headEndCol[0] = sPhone->headEndCol[1] = 0;
    sPhone->headStart[0] = sPhone->headStart[1] = 0xFFFFFFFF;
    sPhone->headScratch = 1;
    FillWindowPixelBuffer(WIN_TICKER, PIXEL_FILL(0));
    Ticker_Update();
}

static void Ticker_RenderNext(void)
{
    const u8 *text;
    u32 win, x0, w;
    u8 k = sPhone->headScratch ^ 1;

    if (sPhone->newsCount == 0)
        text = sText_PhoneNoNews;
    else
        text = sPhoneNews[sPhone->newsOrder[sPhone->newsNext++ % sPhone->newsCount]].text;
    win = WIN_SCRATCH_A + k;
    x0 = sPhone->nextHeadX & 7;
    w = GetStringWidth(FONT_SMALL, text, 0);
    FillWindowPixelBuffer(win, PIXEL_FILL(0));
    AddTextPrinterParameterized4(win, FONT_SMALL, x0, 0, 0, 0, sColors_White, TEXT_SKIP_DRAW, text);
    // gold dot between headlines (mock: 2x2 at text end + 6, y 38-39 = row 7-8)
    FillWindowPixelRect(win, PIXEL_FILL(TXT_GOLD), x0 + w + NEWS_GAP / 2 - 1, 7, 2, 2);
    sPhone->headStart[k] = sPhone->nextHeadX & ~7;
    sPhone->headEndCol[k] = (sPhone->nextHeadX + w + NEWS_GAP / 2) / 8;
    sPhone->headScratch = k;
    sPhone->nextHeadX += w + NEWS_GAP;
}

static void Ticker_FillColumn(u32 col)
{
    u32 k, t, i;
    u8 *ring = gWindows[WIN_TICKER].tileData;
    u32 rc = col % 32;

    for (t = 0; t < 2; t++)
        CpuFill32(0, ring + (t * 32 + rc) * TILE_SIZE_4BPP, TILE_SIZE_4BPP);
    for (k = 0; k < 2; k++)
    {
        u32 startCol;
        u8 *src;

        if (sPhone->headStart[k] == 0xFFFFFFFF)
            continue;
        startCol = sPhone->headStart[k] / 8;
        if (col < startCol || col > sPhone->headEndCol[k] || col - startCol >= 32)
            continue;
        src = gWindows[WIN_SCRATCH_A + k].tileData;
        for (t = 0; t < 2; t++)
        {
            u32 *d = (u32 *)(ring + (t * 32 + rc) * TILE_SIZE_4BPP);
            u32 *s = (u32 *)(src + (t * 32 + col - startCol) * TILE_SIZE_4BPP);
            for (i = 0; i < TILE_SIZE_4BPP / 4; i++)
                d[i] |= s[i];     // headlines never share a pixel, so OR merges them
        }
    }
}

static void Ticker_Update(void)
{
    bool32 dirty = FALSE;
    // virtual x v shows at screen x (v - scroll + TICK_R); fill up to the clip's right edge + 1 column
    u32 needCol = sPhone->scroll / 8 + 1;

    while (sPhone->filledCol <= needCol)
    {
        // render the next headline once the column reaches where it starts
        while (sPhone->filledCol * 8 + 7 >= sPhone->nextHeadX)
            Ticker_RenderNext();
        Ticker_FillColumn(sPhone->filledCol);
        sPhone->filledCol++;
        dirty = TRUE;
    }
    if (dirty)
        CopyWindowToVram(WIN_TICKER, COPYWIN_GFX);
    ChangeBgX(1, ((sPhone->scroll - PHONE_TICK_R) & 255) << 8, BG_COORD_SET);
    if (++sPhone->tickerWait >= TICKER_FRAMES_PER_PX)
    {
        sPhone->tickerWait = 0;
        sPhone->scroll++;
    }
}
