#include "global.h"
#include "option_menu.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "international_string_util.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "string_util.h"
#include "strings.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "gba/m4a_internal.h"
#include "constants/rgb.h"

// Orchid OPTION screen (dev_scripts/orchid_ui/mock_options.py, assets from export_options.py):
// BG0 text windows, BG1 the FRAME preview, BG2 header / option pills / picture fields / tray, BG3 the
// scrolling grid. The focused pill turns gold by palette swap; red chevrons (OBJ) frame its value, and the
// tray previews the focused option. Every option and its save value work as in vanilla.
#include "data/option_menu_orchid.h"

#define tMenuSelection data[0]
#define tTextSpeed data[1]
#define tBattleSceneOff data[2]
#define tBattleStyle data[3]
#define tSound data[4]
#define tButtonMode data[5]
#define tWindowFrameType data[6]

enum
{
    MENUITEM_TEXTSPEED,
    MENUITEM_BATTLESCENE,
    MENUITEM_BATTLESTYLE,
    MENUITEM_SOUND,
    MENUITEM_BUTTONMODE,
    MENUITEM_FRAMETYPE,
    MENUITEM_CANCEL,
    MENUITEM_COUNT,
};

enum
{
    WIN_OPTIONS,
    WIN_PREVIEW,
    WIN_DONE,
};

#define TAG_OOPT_GEAR     0x6E10
#define TAG_OOPT_CHEVRON  0x6E11
#define TAG_OOPT_ICON_PAL 0x6E12

#define OOPT_FRAME_TILE   0x1E0 // BG1 (charblock 2): the previewed frame's 9 tiles, after the windows
#define OOPT_ICON_OPTION  6     // menu_icons.png frame

#define CHEVRON_LEFT  0
#define CHEVRON_RIGHT 1

struct OrchidOptions
{
    u16 bg1Tilemap[0x400];
    u16 bg2Tilemap[0x400];
    u16 bg3Tilemap[0x400];
    u8 gridTimer;
    u8 chevronSpriteIds[2];
    u8 arrowSpriteId;
    u8 flashTimer;
    u8 flashSide;
    u16 arrowTimer;
    bool8 samplePrinting;
};

static EWRAM_DATA struct OrchidOptions *sOptions = NULL;

static void Task_OptionMenuFadeIn(u8 taskId);
static void Task_OptionMenuProcessInput(u8 taskId);
static void Task_OptionMenuSave(u8 taskId);
static void Task_OptionMenuFadeOut(u8 taskId);
static void HighlightOptionMenuItem(u8 taskId);
static u8 TextSpeed_ProcessInput(u8 selection);
static u8 BattleScene_ProcessInput(u8 selection);
static u8 BattleStyle_ProcessInput(u8 selection);
static u8 Sound_ProcessInput(u8 selection);
static u8 FrameType_ProcessInput(u8 selection);
static u8 ButtonMode_ProcessInput(u8 selection);
static void DrawOptionValue(u8 row, u8 value);
static void DrawOptionMenuTexts(u8 taskId);
static void DrawPreview(u8 taskId);
static void DrawDoneButton(bool32 focused);
static void LoadFramePreview(u8 frameType);

EWRAM_DATA static bool8 sArrowPressed = FALSE;

static const u8 *const sOptionMenuItemsNames[MENUITEM_COUNT] =
{
    [MENUITEM_TEXTSPEED]   = COMPOUND_STRING("TEXT SPEED"),
    [MENUITEM_BATTLESCENE] = COMPOUND_STRING("BATTLE SCENE"),
    [MENUITEM_BATTLESTYLE] = COMPOUND_STRING("BATTLE STYLE"),
    [MENUITEM_SOUND]       = COMPOUND_STRING("SOUND"),
    [MENUITEM_BUTTONMODE]  = COMPOUND_STRING("BUTTON MODE"),
    [MENUITEM_FRAMETYPE]   = COMPOUND_STRING("FRAME"),
    [MENUITEM_CANCEL]      = COMPOUND_STRING("DONE"), // vanilla CANCEL: A here and B both keep the changes
};

static const u8 *const sTextSpeedNames[] = {COMPOUND_STRING("SLOW"), COMPOUND_STRING("MID"), COMPOUND_STRING("FAST")};
static const u8 *const sBattleSceneNames[] = {COMPOUND_STRING("ON"), COMPOUND_STRING("OFF")};
static const u8 *const sBattleStyleNames[] = {COMPOUND_STRING("SHIFT"), COMPOUND_STRING("SET")};
static const u8 *const sSoundNames[] = {COMPOUND_STRING("MONO"), COMPOUND_STRING("STEREO")};
static const u8 *const sButtonModeNames[] = {COMPOUND_STRING("NORMAL"), COMPOUND_STRING("LR"), COMPOUND_STRING("L=A")};
static const u8 sText_FrameType[] = _("TYPE ");

// Tray previews (mock_options.DESC / BUTTON_DESC)
static const u8 sText_TextSpeedSample[] = _("Welcome to the world of\nPOKéMON! Text will print\nat this speed.");
static const u8 sText_TextSpeedSampleLastLine[] = _("at this speed.");
static const u8 *const sBattleSceneDescs[] =
{
    COMPOUND_STRING("ON: moves play their\nanimations in battle."),
    COMPOUND_STRING("OFF: skip move animations\nfor faster battles."),
};
static const u8 *const sBattleStyleDescs[] =
{
    COMPOUND_STRING("SHIFT: you may switch\nPOKéMON when a foe faints."),
    COMPOUND_STRING("SET: no switch offer when\na foe faints."),
};
static const u8 *const sSoundDescs[] =
{
    COMPOUND_STRING("MONO: the same sound\nfrom both speakers."),
    COMPOUND_STRING("STEREO: music and cries\nuse both speakers."),
};
static const u8 sText_Off[] = _("Off");
static const struct {
    const u8 *lText;
    const u8 *rText;
    const u8 *desc;
} sButtonModeDescs[] =
{
    [OPTIONS_BUTTON_MODE_NORMAL]     = {sText_Off, sText_Off, COMPOUND_STRING("L and R do nothing\nspecial in menus.")},
    [OPTIONS_BUTTON_MODE_LR]         = {COMPOUND_STRING("Page up"), COMPOUND_STRING("Page down"), COMPOUND_STRING("Flip long lists a\npage at a time.")},
    [OPTIONS_BUTTON_MODE_L_EQUALS_A] = {COMPOUND_STRING("Same as A"), sText_Off, COMPOUND_STRING("Play one-handed:\nL works as A.")},
};
static const u8 sText_FramePreview[] = _("Menus look like this.");
static const u8 sText_DonePreview[] = _("Keep these settings and\nclose the OPTION menu.");

static const u8 sTextColors[3] = {TEXT_COLOR_TRANSPARENT, OOPT_INK, OOPT_PANEL_SHADE};
static const u8 sCaptionColors[3] = {TEXT_COLOR_TRANSPARENT, OOPT_ACCENT_DARK, OOPT_PANEL_SHADE};
static const u8 sCaptionOffColors[3] = {TEXT_COLOR_TRANSPARENT, OOPT_PANEL_DARK, OOPT_PANEL_SHADE};

static const struct WindowTemplate sOptionMenuWinTemplates[] =
{
    [WIN_OPTIONS] = {
        .bg = 0,
        .tilemapLeft = OOPT_ROWS_WIN_X,
        .tilemapTop = OOPT_ROWS_WIN_Y,
        .width = OOPT_ROWS_WIN_W,
        .height = OOPT_ROWS_WIN_H,
        .paletteNum = OOPT_PAL_KIT,
        .baseBlock = 1
    },
    [WIN_PREVIEW] = {
        .bg = 0,
        .tilemapLeft = OOPT_PREVIEW_WIN_X,
        .tilemapTop = OOPT_PREVIEW_WIN_Y,
        .width = OOPT_PREVIEW_WIN_W,
        .height = OOPT_PREVIEW_WIN_H,
        .paletteNum = OOPT_PAL_KIT,
        .baseBlock = 1 + OOPT_ROWS_WIN_W * OOPT_ROWS_WIN_H
    },
    [WIN_DONE] = {
        .bg = 0,
        .tilemapLeft = OOPT_DONE_WIN_X,
        .tilemapTop = OOPT_DONE_WIN_Y,
        .width = OOPT_DONE_WIN_W,
        .height = OOPT_DONE_WIN_H,
        .paletteNum = OOPT_PAL_KIT,
        .baseBlock = 1 + OOPT_ROWS_WIN_W * OOPT_ROWS_WIN_H + OOPT_PREVIEW_WIN_W * OOPT_PREVIEW_WIN_H
    },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sOptionMenuBgTemplates[] =
{
    {
        .bg = 0,
        .charBaseIndex = 2,
        .mapBaseIndex = 31,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 0,
        .baseTile = 0
    },
    {
        .bg = 1,
        .charBaseIndex = 2,
        .mapBaseIndex = 30,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 1,
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

// ---------------------------------------------------------------- OBJ: gear, chevrons, continue arrow
static const struct OamData sOam_Gear = {.shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 0};
static const struct OamData sOam_Chevron = {.shape = SPRITE_SHAPE(8x16), .size = SPRITE_SIZE(8x16), .priority = 0};
static const struct OamData sOam_Arrow = {.shape = SPRITE_SHAPE(8x8), .size = SPRITE_SIZE(8x8), .priority = 0};

static const union AnimCmd sAnim_ChevronLeft[] = {ANIMCMD_FRAME(0, 0), ANIMCMD_END};
static const union AnimCmd sAnim_ChevronLeftFlash[] = {ANIMCMD_FRAME(2, 0), ANIMCMD_END};
static const union AnimCmd sAnim_ChevronRight[] = {ANIMCMD_FRAME(0, 0, .hFlip = TRUE), ANIMCMD_END};
static const union AnimCmd sAnim_ChevronRightFlash[] = {ANIMCMD_FRAME(2, 0, .hFlip = TRUE), ANIMCMD_END};
static const union AnimCmd sAnim_Arrow[] = {ANIMCMD_FRAME(4, 0), ANIMCMD_END};
static const union AnimCmd *const sAnims_Chevron[] = {sAnim_ChevronLeft, sAnim_ChevronLeftFlash, sAnim_ChevronRight, sAnim_ChevronRightFlash};
static const union AnimCmd *const sAnims_Arrow[] = {sAnim_Arrow};

static const struct SpriteTemplate sSpriteTemplate_Gear =
{
    .tileTag = TAG_OOPT_GEAR,
    .paletteTag = TAG_OOPT_ICON_PAL,
    .oam = &sOam_Gear,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_Chevron =
{
    .tileTag = TAG_OOPT_CHEVRON,
    .paletteTag = TAG_OOPT_CHEVRON,
    .oam = &sOam_Chevron,
    .anims = sAnims_Chevron,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_Arrow =
{
    .tileTag = TAG_OOPT_CHEVRON,
    .paletteTag = TAG_OOPT_CHEVRON,
    .oam = &sOam_Arrow,
    .anims = sAnims_Arrow,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static void CreateOptionSprites(void)
{
    struct SpriteSheet gear = {gOrchidStartMenuIcons_Gfx + OOPT_ICON_OPTION * 4 * TILE_SIZE_4BPP, 4 * TILE_SIZE_4BPP, TAG_OOPT_GEAR};
    struct SpriteSheet chevron = {gOrchidOptionsChevron_Gfx, 5 * TILE_SIZE_4BPP, TAG_OOPT_CHEVRON};
    struct SpritePalette iconPal = {gOrchidStartMenuIcons_Pal, TAG_OOPT_ICON_PAL};
    struct SpritePalette chevronPal = {gOrchidOptionsChevron_Pal, TAG_OOPT_CHEVRON};

    LoadSpriteSheet(&gear);
    LoadSpriteSheet(&chevron);
    LoadSpritePalette(&iconPal);
    LoadSpritePalette(&chevronPal);
    CreateSprite(&sSpriteTemplate_Gear, OOPT_GEAR_X + 8, OOPT_GEAR_Y + 8, 0);
    sOptions->chevronSpriteIds[CHEVRON_LEFT] = CreateSprite(&sSpriteTemplate_Chevron, 0, 0, 0);
    sOptions->chevronSpriteIds[CHEVRON_RIGHT] = CreateSprite(&sSpriteTemplate_Chevron, 0, 0, 0);
    StartSpriteAnim(&gSprites[sOptions->chevronSpriteIds[CHEVRON_RIGHT]], 2);
    sOptions->arrowSpriteId = CreateSprite(&sSpriteTemplate_Arrow, 0, 0, 0);
    gSprites[sOptions->arrowSpriteId].invisible = TRUE;
}

// Chevrons sit either side of the focused row's value; a press lights one and pushes it out 1 px.
static void UpdateChevrons(u8 selection)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        struct Sprite *sprite = &gSprites[sOptions->chevronSpriteIds[i]];
        bool32 flash = (sOptions->flashTimer != 0 && sOptions->flashSide == i);
        s32 x = (i == CHEVRON_LEFT) ? OOPT_CHEV_L_X : OOPT_CHEV_R_X;

        if (flash)
            x += (i == CHEVRON_LEFT) ? -1 : 1;
        sprite->invisible = (selection >= MENUITEM_CANCEL);
        sprite->x = x + 4;
        sprite->y = OOPT_ROW_Y0 + selection * 16 + OOPT_CHEV_DY + 8;
        StartSpriteAnimIfDifferent(sprite, i * 2 + (flash ? 1 : 0));
    }
}

static void MainCB2(void)
{
    // Orchid grid backdrop (BG3) scrolls diagonally down-right, 1px every 4 frames
    if ((++sOptions->gridTimer & 3) == 0)
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

static void VBlankCB(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void LoadOptionsBgGraphics(void)
{
    u32 x, y;

    DecompressAndCopyTileDataToVram(2, gOrchidOptionsBg_Gfx, 0, 0, 0);
    DecompressDataWithHeaderWram(gOrchidOptionsBg_Tilemap, sOptions->bg2Tilemap);
    for (y = 0; y < 32; y++)
    {
        for (x = 0; x < 32; x++)
            sOptions->bg3Tilemap[y * 32 + x] = (OOPT_GRID_TILE + (x & 1) + (y & 1) * 2) | (OOPT_PAL_GRID << 12);
    }
    LoadPalette(gOrchidOptionsBg_Pal, BG_PLTT_ID(0), OOPT_NUM_BG_PALS * PLTT_SIZE_4BPP);
}

void CB2_InitOptionMenu(void)
{
    switch (gMain.state)
    {
    default:
    case 0:
        SetVBlankCallback(NULL);
        gMain.state++;
        break;
    case 1:
        DmaClearLarge16(3, (void *)(VRAM), VRAM_SIZE, 0x1000);
        DmaClear32(3, OAM, OAM_SIZE);
        DmaClear16(3, PLTT, PLTT_SIZE);
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        sOptions = AllocZeroed(sizeof(*sOptions));
        ResetBgsAndClearDma3BusyFlags(0);
        InitBgsFromTemplates(0, sOptionMenuBgTemplates, ARRAY_COUNT(sOptionMenuBgTemplates));
        SetBgTilemapBuffer(1, sOptions->bg1Tilemap);
        SetBgTilemapBuffer(2, sOptions->bg2Tilemap);
        SetBgTilemapBuffer(3, sOptions->bg3Tilemap);
        ChangeBgX(0, 0, BG_COORD_SET);
        ChangeBgY(0, 0, BG_COORD_SET);
        ChangeBgX(1, 0, BG_COORD_SET);
        ChangeBgY(1, 0, BG_COORD_SET);
        ChangeBgX(2, 0, BG_COORD_SET);
        ChangeBgY(2, 0, BG_COORD_SET);
        ChangeBgX(3, 0, BG_COORD_SET);
        ChangeBgY(3, 0, BG_COORD_SET);
        InitWindows(sOptionMenuWinTemplates);
        DeactivateAllTextPrinters();
        SetGpuReg(REG_OFFSET_WIN0H, 0);
        SetGpuReg(REG_OFFSET_WIN0V, 0);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, 0);
        SetGpuReg(REG_OFFSET_BLDY, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
        ShowBg(0);
        ShowBg(1);
        ShowBg(2);
        ShowBg(3);
        gMain.state++;
        break;
    case 2:
        ResetPaletteFade();
        ScanlineEffect_Stop();
        ResetTasks();
        ResetSpriteData();
        FreeAllSpritePalettes();
        ResetTempTileDataBuffers();
        gMain.state++;
        break;
    case 3:
        LoadOptionsBgGraphics();
        gMain.state++;
        break;
    case 4:
        if (!FreeTempTileDataBuffersIfPossible())
            gMain.state++;
        break;
    case 5:
        CreateOptionSprites();
        gMain.state++;
        break;
    case 6:
        PutWindowTilemap(WIN_OPTIONS);
        PutWindowTilemap(WIN_PREVIEW);
        PutWindowTilemap(WIN_DONE);
        gMain.state++;
        break;
    case 7:
    {
        u8 taskId = CreateTask(Task_OptionMenuFadeIn, 0);

        gTasks[taskId].tMenuSelection = 0;
        gTasks[taskId].tTextSpeed = gSaveBlock2Ptr->optionsTextSpeed;
        if (gTasks[taskId].tTextSpeed > OPTIONS_TEXT_SPEED_FAST)
            gTasks[taskId].tTextSpeed = OPTIONS_TEXT_SPEED_FAST;
        gTasks[taskId].tBattleSceneOff = gSaveBlock2Ptr->optionsBattleSceneOff;
        gTasks[taskId].tBattleStyle = gSaveBlock2Ptr->optionsBattleStyle;
        gTasks[taskId].tSound = gSaveBlock2Ptr->optionsSound;
        gTasks[taskId].tButtonMode = gSaveBlock2Ptr->optionsButtonMode;
        if (gTasks[taskId].tButtonMode > OPTIONS_BUTTON_MODE_L_EQUALS_A)
            gTasks[taskId].tButtonMode = OPTIONS_BUTTON_MODE_NORMAL;
        // Frames from a pre-Orchid save (vanilla types 9-20) show as TYPE 1, as the game draws them.
        gTasks[taskId].tWindowFrameType = gSaveBlock2Ptr->optionsWindowFrameType;
        if (gTasks[taskId].tWindowFrameType >= WINDOW_FRAMES_COUNT)
            gTasks[taskId].tWindowFrameType = 0;

        LoadFramePreview(gTasks[taskId].tWindowFrameType);
        DrawOptionMenuTexts(taskId);
        HighlightOptionMenuItem(taskId);
        gMain.state++;
        break;
    }
    case 8:
        ScheduleBgCopyTilemapToVram(0);
        ScheduleBgCopyTilemapToVram(1);
        ScheduleBgCopyTilemapToVram(2);
        ScheduleBgCopyTilemapToVram(3);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB);
        SetMainCallback2(MainCB2);
        return;
    }
}

static void Task_OptionMenuFadeIn(u8 taskId)
{
    if (!gPaletteFade.active)
        gTasks[taskId].func = Task_OptionMenuProcessInput;
}

static void UpdateTimers(u8 taskId)
{
    struct Sprite *arrow = &gSprites[sOptions->arrowSpriteId];

    if (sOptions->flashTimer != 0 && --sOptions->flashTimer == 0)
        UpdateChevrons(gTasks[taskId].tMenuSelection);

    // TEXT SPEED sample: the red continue arrow bobs after the sample has printed
    if (sOptions->samplePrinting && !IsTextPrinterActiveOnWindow(WIN_PREVIEW))
    {
        sOptions->samplePrinting = FALSE;
        sOptions->arrowTimer = 0;
        arrow->x = OOPT_PREVIEW_SCREEN_X + GetStringWidth(FONT_NORMAL, sText_TextSpeedSampleLastLine, 0) + 3 + 4;
        arrow->invisible = FALSE;
    }
    if (!arrow->invisible)
    {
        arrow->y = OOPT_PREVIEW_SCREEN_Y + OOPT_PREVIEW_LINE_H * 2 + 6 + 4 + ((sOptions->arrowTimer / 16) % 2);
        sOptions->arrowTimer++;
    }
}

static void Task_OptionMenuProcessInput(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    UpdateTimers(taskId);

    if (JOY_NEW(A_BUTTON))
    {
        if (tMenuSelection == MENUITEM_CANCEL)
            gTasks[taskId].func = Task_OptionMenuSave;
    }
    else if (JOY_NEW(B_BUTTON))
    {
        gTasks[taskId].func = Task_OptionMenuSave;
    }
    else if (JOY_NEW(DPAD_UP))
    {
        if (tMenuSelection > 0)
            tMenuSelection--;
        else
            tMenuSelection = MENUITEM_CANCEL;
        HighlightOptionMenuItem(taskId);
    }
    else if (JOY_NEW(DPAD_DOWN))
    {
        if (tMenuSelection < MENUITEM_CANCEL)
            tMenuSelection++;
        else
            tMenuSelection = 0;
        HighlightOptionMenuItem(taskId);
    }
    else
    {
        u8 previousOption;
        s16 *value;

        switch (tMenuSelection)
        {
        case MENUITEM_TEXTSPEED:
            value = &tTextSpeed;
            previousOption = *value;
            *value = TextSpeed_ProcessInput(*value);
            break;
        case MENUITEM_BATTLESCENE:
            value = &tBattleSceneOff;
            previousOption = *value;
            *value = BattleScene_ProcessInput(*value);
            break;
        case MENUITEM_BATTLESTYLE:
            value = &tBattleStyle;
            previousOption = *value;
            *value = BattleStyle_ProcessInput(*value);
            break;
        case MENUITEM_SOUND:
            value = &tSound;
            previousOption = *value;
            *value = Sound_ProcessInput(*value);
            break;
        case MENUITEM_BUTTONMODE:
            value = &tButtonMode;
            previousOption = *value;
            *value = ButtonMode_ProcessInput(*value);
            break;
        case MENUITEM_FRAMETYPE:
            value = &tWindowFrameType;
            previousOption = *value;
            *value = FrameType_ProcessInput(*value);
            break;
        default:
            return;
        }

        if (sArrowPressed)
        {
            sArrowPressed = FALSE;
            sOptions->flashSide = JOY_NEW(DPAD_LEFT) ? CHEVRON_LEFT : CHEVRON_RIGHT;
            sOptions->flashTimer = OOPT_FLASH_FRAMES;
            UpdateChevrons(tMenuSelection);
            if (previousOption != *value)
            {
                DrawOptionValue(tMenuSelection, *value);
                CopyWindowToVram(WIN_OPTIONS, COPYWIN_GFX);
                DrawPreview(taskId);
            }
        }
    }
}

static void Task_OptionMenuSave(u8 taskId)
{
    gSaveBlock2Ptr->optionsTextSpeed = gTasks[taskId].tTextSpeed;
    gSaveBlock2Ptr->optionsBattleSceneOff = gTasks[taskId].tBattleSceneOff;
    gSaveBlock2Ptr->optionsBattleStyle = gTasks[taskId].tBattleStyle;
    gSaveBlock2Ptr->optionsSound = gTasks[taskId].tSound;
    gSaveBlock2Ptr->optionsButtonMode = gTasks[taskId].tButtonMode;
    gSaveBlock2Ptr->optionsWindowFrameType = gTasks[taskId].tWindowFrameType;

    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    gTasks[taskId].func = Task_OptionMenuFadeOut;
}

static void Task_OptionMenuFadeOut(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        DestroyTask(taskId);
        FreeAllWindowBuffers();
        FREE_AND_SET_NULL(sOptions);
        SetMainCallback2(gMain.savedCallback);
    }
}

// Gold pill on the focused row (BG2 palette swap), chevrons, preview tray, DONE button.
static void HighlightOptionMenuItem(u8 taskId)
{
    u8 selection = gTasks[taskId].tMenuSelection;
    u32 row, y, x;

    for (row = 0; row < MENUITEM_CANCEL; row++)
    {
        u16 pal = (row == selection) ? OOPT_PAL_SELECTED : OOPT_PAL_KIT;

        for (y = OOPT_ROW_TILE0 + row * 2; y < OOPT_ROW_TILE0 + row * 2 + 2; y++)
        {
            for (x = OOPT_SWAP_COL0; x <= OOPT_SWAP_COL1; x++)
            {
                u16 *entry = &sOptions->bg2Tilemap[y * 32 + x];

                if ((*entry >> 12) <= OOPT_PAL_SELECTED)
                    *entry = (*entry & 0x0FFF) | (pal << 12);
            }
        }
    }
    ScheduleBgCopyTilemapToVram(2);
    sOptions->flashTimer = 0;
    UpdateChevrons(selection);
    DrawDoneButton(selection == MENUITEM_CANCEL);
    DrawPreview(taskId);
}

static void DrawOptionValue(u8 row, u8 value)
{
    u8 text[16];
    const u8 *str;
    s32 x;

    switch (row)
    {
    case MENUITEM_TEXTSPEED:
        str = sTextSpeedNames[value];
        break;
    case MENUITEM_BATTLESCENE:
        str = sBattleSceneNames[value];
        break;
    case MENUITEM_BATTLESTYLE:
        str = sBattleStyleNames[value];
        break;
    case MENUITEM_SOUND:
        str = sSoundNames[value];
        break;
    case MENUITEM_BUTTONMODE:
        str = sButtonModeNames[value];
        break;
    default:
        ConvertIntToDecimalStringN(StringCopy(text, sText_FrameType), value + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        str = text;
        break;
    }
    FillWindowPixelRect(WIN_OPTIONS, PIXEL_FILL(0), OOPT_INSET_X, row * 16, OOPT_INSET_W, 16);
    x = OOPT_INSET_X + (OOPT_INSET_W - GetStringWidth(FONT_NORMAL, str, 0)) / 2;
    AddTextPrinterParameterized4(WIN_OPTIONS, FONT_NORMAL, x, row * 16, 0, 0, sTextColors, TEXT_SKIP_DRAW, str);
}

static void DrawOptionMenuTexts(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    u32 i;

    FillWindowPixelBuffer(WIN_OPTIONS, PIXEL_FILL(0));
    for (i = 0; i < MENUITEM_CANCEL; i++)
        AddTextPrinterParameterized4(WIN_OPTIONS, FONT_NORMAL, OOPT_LABEL_X, i * 16, 0, 0, sTextColors, TEXT_SKIP_DRAW, sOptionMenuItemsNames[i]);
    DrawOptionValue(MENUITEM_TEXTSPEED, tTextSpeed);
    DrawOptionValue(MENUITEM_BATTLESCENE, tBattleSceneOff);
    DrawOptionValue(MENUITEM_BATTLESTYLE, tBattleStyle);
    DrawOptionValue(MENUITEM_SOUND, tSound);
    DrawOptionValue(MENUITEM_BUTTONMODE, tButtonMode);
    DrawOptionValue(MENUITEM_FRAMETYPE, tWindowFrameType);
    CopyWindowToVram(WIN_OPTIONS, COPYWIN_FULL);
}

// DONE (vanilla CANCEL row): a pill on the tray with the B-button disc; focused, the gold pill is drawn
// into its own text window so the tray never turns gold.
static void DrawDoneButton(bool32 focused)
{
    FillWindowPixelBuffer(WIN_DONE, PIXEL_FILL(0));
    BlitBitmapRectToWindow(WIN_DONE, gOrchidOptionsDone_Gfx, 0, focused ? 16 : 0, OOPT_DONE_WIN_W * 8, 32,
                           0, 0, OOPT_DONE_WIN_W * 8, 16);
    AddTextPrinterParameterized4(WIN_DONE, FONT_NARROW, OOPT_DONE_TEXT_X, OOPT_DONE_TEXT_Y, 0, 0, sTextColors, TEXT_SKIP_DRAW, sOptionMenuItemsNames[MENUITEM_CANCEL]);
    CopyWindowToVram(WIN_DONE, COPYWIN_GFX);
}

// Two-line tray text at the 14 px pitch (FONT_NORMAL is 16 px: line spacing -2, as the bag description).
static void PrintPreviewText(const u8 *str, u8 y, u8 speed)
{
    AddTextPrinterParameterized4(WIN_PREVIEW, FONT_NORMAL, OOPT_PREVIEW_X, y, 0, (u8)-2, sTextColors, speed, str);
}

static void LoadFramePreview(u8 frameType)
{
    const struct TilesPal *frame = GetWindowFrameTilesPal(frameType);

    LoadBgTiles(1, frame->tiles, 0x120, OOPT_FRAME_TILE);
    LoadPalette(frame->pal, BG_PLTT_ID(OOPT_PAL_FRAME), PLTT_SIZE_4BPP);
}

// The selected FRAME type 9-sliced around the preview text (as DrawStdFrameWithCustomTile), centre tile = fill.
static void DrawFramePreview(bool32 show)
{
    const u32 l = OOPT_FRAME_WIN_X - 1, t = OOPT_FRAME_WIN_Y - 1;
    const u32 r = OOPT_FRAME_WIN_X + OOPT_FRAME_WIN_W, b = OOPT_FRAME_WIN_Y + OOPT_FRAME_WIN_H;
    const u32 w = OOPT_FRAME_WIN_W, h = OOPT_FRAME_WIN_H, p = OOPT_PAL_FRAME, tile = OOPT_FRAME_TILE;

    FillBgTilemapBufferRect(1, 0, 0, 0, 32, 32, 0);
    if (show)
    {
        FillBgTilemapBufferRect(1, tile + 0, l, t, 1, 1, p);
        FillBgTilemapBufferRect(1, tile + 1, l + 1, t, w, 1, p);
        FillBgTilemapBufferRect(1, tile + 2, r, t, 1, 1, p);
        FillBgTilemapBufferRect(1, tile + 3, l, t + 1, 1, h, p);
        FillBgTilemapBufferRect(1, tile + 4, l + 1, t + 1, w, h, p);
        FillBgTilemapBufferRect(1, tile + 5, r, t + 1, 1, h, p);
        FillBgTilemapBufferRect(1, tile + 6, l, b, 1, 1, p);
        FillBgTilemapBufferRect(1, tile + 7, l + 1, b, w, 1, p);
        FillBgTilemapBufferRect(1, tile + 8, r, b, 1, 1, p);
    }
    ScheduleBgCopyTilemapToVram(1);
}

static void DrawButtonModePreview(u8 mode)
{
    u32 i;

    for (i = 0; i < 2; i++)
    {
        const u8 *caption = (i == 0) ? sButtonModeDescs[mode].lText : sButtonModeDescs[mode].rText;
        bool32 off = (caption == sText_Off);
        u32 x = (i == 0) ? OOPT_PREVIEW_X : OOPT_KEYPAD_R_X - OOPT_PREVIEW_WIN_X * 8;
        u32 glyph = i * 2 + (off ? 1 : 0); // keypad.png: L, L off, R, R off

        BlitBitmapRectToWindow(WIN_PREVIEW, gOrchidOptionsKeypad_Gfx, 0, glyph * 8, 16, 32, x, OOPT_PREVIEW_Y + 5, 16, 8);
        AddTextPrinterParameterized4(WIN_PREVIEW, FONT_NARROW, x + 16 + 3, OOPT_PREVIEW_Y + 1, 0, 0,
                                     off ? sCaptionOffColors : sCaptionColors, TEXT_SKIP_DRAW, caption);
    }
    PrintPreviewText(sButtonModeDescs[mode].desc, OOPT_PREVIEW_Y + OOPT_PREVIEW_LINE_H + 2, TEXT_SKIP_DRAW);
}

static void DrawPreview(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    // stop a TEXT SPEED sample still printing (only the preview ever prints over time on this screen)
    DeactivateAllTextPrinters();
    FillWindowPixelBuffer(WIN_PREVIEW, PIXEL_FILL(0));
    gSprites[sOptions->arrowSpriteId].invisible = TRUE;
    sOptions->samplePrinting = FALSE;
    DrawFramePreview(tMenuSelection == MENUITEM_FRAMETYPE);

    switch (tMenuSelection)
    {
    case MENUITEM_TEXTSPEED:
        // prints at the chosen speed (sTextSpeedFrameDelays: 8 / 4 / 1 frames per character)
        PrintPreviewText(sText_TextSpeedSample, OOPT_PREVIEW_Y, tTextSpeed == OPTIONS_TEXT_SPEED_SLOW ? 8 : (tTextSpeed == OPTIONS_TEXT_SPEED_MID ? 4 : 1));
        sOptions->samplePrinting = TRUE;
        break;
    case MENUITEM_BATTLESCENE:
        PrintPreviewText(sBattleSceneDescs[tBattleSceneOff], OOPT_PREVIEW_Y, TEXT_SKIP_DRAW);
        break;
    case MENUITEM_BATTLESTYLE:
        PrintPreviewText(sBattleStyleDescs[tBattleStyle], OOPT_PREVIEW_Y, TEXT_SKIP_DRAW);
        break;
    case MENUITEM_SOUND:
        PrintPreviewText(sSoundDescs[tSound], OOPT_PREVIEW_Y, TEXT_SKIP_DRAW);
        break;
    case MENUITEM_BUTTONMODE:
        DrawButtonModePreview(tButtonMode);
        break;
    case MENUITEM_FRAMETYPE:
        AddTextPrinterParameterized4(WIN_PREVIEW, FONT_NORMAL, OOPT_FRAME_TEXT_X, OOPT_FRAME_TEXT_Y, 0, 0, sTextColors, TEXT_SKIP_DRAW, sText_FramePreview);
        break;
    default:
        PrintPreviewText(sText_DonePreview, OOPT_PREVIEW_Y, TEXT_SKIP_DRAW);
        break;
    }
    CopyWindowToVram(WIN_PREVIEW, COPYWIN_GFX);
}

static u8 TextSpeed_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (selection <= 1)
            selection++;
        else
            selection = 0;

        sArrowPressed = TRUE;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (selection != 0)
            selection--;
        else
            selection = 2;

        sArrowPressed = TRUE;
    }
    return selection;
}

static u8 BattleScene_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        sArrowPressed = TRUE;
    }

    return selection;
}

static u8 BattleStyle_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        sArrowPressed = TRUE;
    }

    return selection;
}

static u8 Sound_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        SetPokemonCryStereo(selection);
        sArrowPressed = TRUE;
    }

    return selection;
}

static u8 FrameType_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (selection < WINDOW_FRAMES_COUNT - 1)
            selection++;
        else
            selection = 0;

        LoadFramePreview(selection);
        sArrowPressed = TRUE;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (selection != 0)
            selection--;
        else
            selection = WINDOW_FRAMES_COUNT - 1;

        LoadFramePreview(selection);
        sArrowPressed = TRUE;
    }
    return selection;
}

static u8 ButtonMode_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (selection <= 1)
            selection++;
        else
            selection = 0;

        sArrowPressed = TRUE;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (selection != 0)
            selection--;
        else
            selection = 2;

        sArrowPressed = TRUE;
    }
    return selection;
}
