#include "global.h"
#include "bg.h"
#include "decompress.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "main.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "random.h"
#include "scanline_effect.h"
#include "script.h"
#include "sound.h"
#include "m4a.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "trainer_pokemon_sprites.h"
#include "type_icons.h"
#include "type_rps_minigame.h"
#include "window.h"
#include "constants/characters.h"
#include "constants/pokemon.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/species.h"

static const u32 sCircleGfx[] = INCBIN_U32("graphics/type_rps/circle.4bpp.smol");
static const u16 sCirclePal[] = INCBIN_U16("graphics/type_rps/circle.gbapal");

#define TAG_CIRCLE_GFX 5000
#define TAG_CIRCLE_PAL 5001
#define TAG_ICON_GFX   5002
#define TAG_ICON_PAL   5003

#define WIN_COUNTDOWN 0

#define TYPE_RPS_TRI_CENTER_X (DISPLAY_WIDTH / 2)
/*
 * Vertically centre the triangle (64×64 circles, local offsets below) in the band above the text window.
 * Bbox of circle centres: top = CY−64, bottom = CY+48 → vertical centre = CY−8.
 * Window starts at tile row 15 (120px); leave 8px gap → play area bottom = 112px.
 * Solve CY−8 = 112/2 → CY = 64 (top of triangle flush with top of screen).
 */
#define TYPE_RPS_TEXT_WIN_TILE_TOP 15
#define TYPE_RPS_PLAY_AREA_BOTTOM_PX (TYPE_RPS_TEXT_WIN_TILE_TOP * TILE_HEIGHT - 8)
#define TYPE_RPS_TRI_CENTER_Y ((TYPE_RPS_PLAY_AREA_BOTTOM_PX / 2) + 8)

/* OBJ palette slots for mon pics; 0–1 used by circle + battle icon sprite palettes. */
#define TYPE_RPS_MON_PAL_TEPIG  3
#define TYPE_RPS_MON_PAL_MUDKIP 4
#define TYPE_RPS_MON_PAL_ROWLET 5

#define TYPE_RPS_MON_PIC_Y_OFFSET 6
#define TYPE_RPS_OUTCOME_ICON_TEXT_GAP 6

enum {
    PHASE_INIT,
    PHASE_SELECT,
    PHASE_COUNT_3,
    PHASE_COUNT_2,
    PHASE_COUNT_1,
    PHASE_RESULT_WAIT,
    PHASE_FADE_OUT,
};

enum {
    RPS_FIRE = 0,
    RPS_WATER = 1,
    RPS_GRASS = 2,
};

static EWRAM_DATA MainCallback sExitCallback = NULL;

static const struct OamData sOam_Circle = {
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 2,
};

static const struct OamData sOam_TypeIcon = {
    .affineMode = ST_OAM_AFFINE_OFF,
    .objMode = ST_OAM_OBJ_NORMAL,
    .shape = SPRITE_SHAPE(8x16),
    .size = SPRITE_SIZE(8x16),
    .priority = 1,
};

static const union AnimCmd sAnim_Fire[] = {
    ANIMCMD_FRAME(TYPE_ICON_2_FRAME(TYPE_FIRE), 0),
    ANIMCMD_END
};
static const union AnimCmd sAnim_Water[] = {
    ANIMCMD_FRAME(TYPE_ICON_2_FRAME(TYPE_WATER), 0),
    ANIMCMD_END
};
static const union AnimCmd sAnim_Grass[] = {
    ANIMCMD_FRAME(TYPE_ICON_2_FRAME(TYPE_GRASS), 0),
    ANIMCMD_END
};

static const union AnimCmd *const sAnims_TypeRps[] = {
    [RPS_FIRE] = sAnim_Fire,
    [RPS_WATER] = sAnim_Water,
    [RPS_GRASS] = sAnim_Grass,
};

static const struct SpriteTemplate sSpriteTemplate_Circle = {
    .tileTag = TAG_CIRCLE_GFX,
    .paletteTag = TAG_CIRCLE_PAL,
    .oam = &sOam_Circle,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct SpriteTemplate sSpriteTemplate_TypeIcon = {
    .tileTag = TAG_ICON_GFX,
    .paletteTag = TAG_ICON_PAL,
    .oam = &sOam_TypeIcon,
    .anims = sAnims_TypeRps,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

static const struct CompressedSpriteSheet sSpriteSheet_Circle = {
    .data = sCircleGfx,
    .size = 64 * 64 / 2,
    .tag = TAG_CIRCLE_GFX,
};

static const struct CompressedSpriteSheet sSpriteSheet_BattleIcons2 = {
    .data = gBattleIcons_Gfx2,
    .size = (8 * 16) * 9,
    .tag = TAG_ICON_GFX,
};

static const struct SpritePalette sSpritePal_Circle = {
    .data = sCirclePal,
    .tag = TAG_CIRCLE_PAL,
};

static const struct SpritePalette sSpritePal_Icons = {
    .data = gBattleIcons_Pal2,
    .tag = TAG_ICON_PAL,
};

static const struct BgTemplate sBgTemplates[] = {
    {
        .bg = 0,
        .charBaseIndex = 0,
        .mapBaseIndex = 29,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 3,
        .baseTile = 0,
    },
};

static const struct WindowTemplate sWindowTemplates[] = {
    {
        .bg = 0,
        .tilemapLeft = 2,
        .tilemapTop = 15,
        .width = 26,
        .height = 4,
        .paletteNum = 15,
        .baseBlock = 1,
    },
    DUMMY_WIN_TEMPLATE,
};

static const u8 sText_Instructions[] = _("LEFT/RIGHT: Choose type.\nA: Confirm  B: Quit");
static const u8 sText_Count3[] = _("3");
static const u8 sText_Count2[] = _("2");
static const u8 sText_Count1[] = _("1");
static const u8 sText_FireName[] = _("FIRE");
static const u8 sText_WaterName[] = _("WATER");
static const u8 sText_GrassName[] = _("GRASS");
static const u8 sText_OutcomeTie[] = _("Opponent chose {STR_VAR_1}!\nIt's a tie - you lose!");
static const u8 sText_OutcomeWin[] = _("Opponent chose {STR_VAR_1}!\nYou win!");
static const u8 sText_OutcomeLose[] = _("Opponent chose {STR_VAR_1}!\nYou lose!");

/* Offsets from triangle centroid (88, 56) in the pre-centering layout; anchor moves centroid to screen center. */
static const s16 sCircleLocalOffset[3][2] = {
    [RPS_FIRE] = {-48, 16},
    [RPS_WATER] = {0, -32},
    [RPS_GRASS] = {48, 16},
};

static const u16 sTypeRpsMonSpecies[3] = {
    [RPS_FIRE] = SPECIES_TEPIG,
    [RPS_WATER] = SPECIES_MUDKIP,
    [RPS_GRASS] = SPECIES_ROWLET,
};

static const u8 sTypeRpsMonPalSlot[3] = {
    [RPS_FIRE] = TYPE_RPS_MON_PAL_TEPIG,
    [RPS_WATER] = TYPE_RPS_MON_PAL_MUDKIP,
    [RPS_GRASS] = TYPE_RPS_MON_PAL_ROWLET,
};

static s16 sCirclePositions[3][2];
static u8 sCircleSpriteIds[3];
static u16 sMonPicSpriteIds[3];
static u8 sOpponentIconSpriteId;

static void CB2_LoadTypeRpsGfx(void);
static void CB2_TypeRpsMain(void);
static void Task_TypeRpsFadeIn(u8 taskId);
static void Task_TypeRpsRun(u8 taskId);

/* ReturnToField → MoveSaveBlocks_ResetHeap → InitHeap() resets the malloc arena; clear window/BG pointers
 * so nothing dereferences stale addresses before overworld InitWindows runs. */
/* PlayCry_Normal starts Task_DuckBGMForPokemonCry; stop cry alone leaves that task alive across SetMainCallback2. */
static void TypeRpsStopCryAndBgmDuckTask(void)
{
    u8 duckTask;

    StopCryAndClearCrySongs();
    duckTask = FindTaskIdByFunc(Task_DuckBGMForPokemonCry);
    if (duckTask != TASK_NONE)
    {
        m4aMPlayVolumeControl(&gMPlayInfo_BGM, TRACKS_ALL, 256);
        DestroyTask(duckTask);
    }
}

static void TypeRpsAbandonWindowStateForReturn(void)
{
    u32 i;

    UnsetBgTilemapBuffer(0);
    for (i = 0; i < NUM_BACKGROUNDS; i++)
        gWindowBgTilemapBuffers[i] = NULL;

    memset(gWindows, 0, WINDOWS_MAX * sizeof(struct Window));
    for (i = 0; i < WINDOWS_MAX; i++)
        gWindows[i].window.bg = 0xFF;
}

static void VBlankCB(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static bool32 TypeRpsPlayerWins(u8 player, u8 opponent)
{
    if (player == opponent)
        return FALSE;
    return opponent == ((player + 2) % 3);
}

static u16 TypeRpsGetFirstLineStringWidth(const u8 *str)
{
    u8 buf[0x80];
    u32 i;

    for (i = 0; i < sizeof(buf) - 1; i++)
    {
        u8 c = str[i];

        if (c == EOS || c == CHAR_NEWLINE)
            break;
        buf[i] = c;
    }
    buf[i] = EOS;
    return (u16)GetStringWidth(FONT_NORMAL, buf, 0);
}

/* Place 8×16 type icon to the right of the first outcome line, aligned with FONT_NORMAL at (4,4) in the window. */
static void TypeRpsLayoutOpponentTypeIconForOutcome(void)
{
    s16 winX, winY, textX, textY, iconX, iconY, maxRight;
    u16 lineW;

    if (sOpponentIconSpriteId >= MAX_SPRITES)
        return;

    winX = (s16)GetWindowAttribute(WIN_COUNTDOWN, WINDOW_TILEMAP_LEFT) * TILE_WIDTH;
    winY = (s16)GetWindowAttribute(WIN_COUNTDOWN, WINDOW_TILEMAP_TOP) * TILE_HEIGHT;
    textX = winX + 4;
    textY = winY + 4;
    lineW = TypeRpsGetFirstLineStringWidth(gStringVar4);
    iconX = textX + (s16)lineW + TYPE_RPS_OUTCOME_ICON_TEXT_GAP;
    /* Sprite x/y are the OAM anchor (centre for 8×16); +8 ≈ vertical centre of first text row vs icon height. */
    iconY = textY + 8;

    maxRight = winX + (s16)GetWindowAttribute(WIN_COUNTDOWN, WINDOW_WIDTH) * TILE_WIDTH - 4;
    if (iconX > maxRight)
        iconX = maxRight;

    gSprites[sOpponentIconSpriteId].x = iconX;
    gSprites[sOpponentIconSpriteId].y = iconY;
}

static void PrintCountdownWindow(const u8 *str)
{
    u8 colors[3] = {0, 1, 2};

    FillWindowPixelBuffer(WIN_COUNTDOWN, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_COUNTDOWN, FONT_NORMAL, 4, 4, 0, 0, colors, TEXT_SKIP_DRAW, str);
    PutWindowTilemap(WIN_COUNTDOWN);
    CopyWindowToVram(WIN_COUNTDOWN, COPYWIN_FULL);
}

static void PrintTypeRpsOutcome(u8 player, u8 opponent)
{
    u8 colors[3] = {0, 1, 2};

    if (opponent == RPS_FIRE)
        StringCopy(gStringVar1, sText_FireName);
    else if (opponent == RPS_WATER)
        StringCopy(gStringVar1, sText_WaterName);
    else
        StringCopy(gStringVar1, sText_GrassName);

    if (player == opponent)
        StringExpandPlaceholders(gStringVar4, sText_OutcomeTie);
    else if (TypeRpsPlayerWins(player, opponent))
        StringExpandPlaceholders(gStringVar4, sText_OutcomeWin);
    else
        StringExpandPlaceholders(gStringVar4, sText_OutcomeLose);

    FillWindowPixelBuffer(WIN_COUNTDOWN, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_COUNTDOWN, FONT_NORMAL, 4, 4, 0, 0, colors, TEXT_SKIP_DRAW, gStringVar4);
    PutWindowTilemap(WIN_COUNTDOWN);
    CopyWindowToVram(WIN_COUNTDOWN, COPYWIN_FULL);
    TypeRpsLayoutOpponentTypeIconForOutcome();
}

static void LoadTypeRpsSprites(void)
{
    u8 i;

    for (i = 0; i < 3; i++)
        sMonPicSpriteIds[i] = 0xFFFF;

    LoadCompressedSpriteSheet(&sSpriteSheet_Circle);
    LoadSpritePalette(&sSpritePal_Circle);
    LoadCompressedSpriteSheet(&sSpriteSheet_BattleIcons2);
    LoadSpritePalette(&sSpritePal_Icons);

    for (i = 0; i < 3; i++)
    {
        s16 cx, cy;

        cx = TYPE_RPS_TRI_CENTER_X + sCircleLocalOffset[i][0];
        cy = TYPE_RPS_TRI_CENTER_Y + sCircleLocalOffset[i][1];
        sCirclePositions[i][0] = cx;
        sCirclePositions[i][1] = cy;

        sCircleSpriteIds[i] = CreateSprite(&sSpriteTemplate_Circle, cx, cy, 0);

        sMonPicSpriteIds[i] = CreateMonPicSprite_Affine(
            sTypeRpsMonSpecies[i],
            FALSE,
            0,
            MON_PIC_AFFINE_FRONT,
            cx,
            cy + TYPE_RPS_MON_PIC_Y_OFFSET,
            sTypeRpsMonPalSlot[i],
            TAG_NONE);
        if (sMonPicSpriteIds[i] != 0xFFFF)
        {
            gSprites[sMonPicSpriteIds[i]].oam.priority = 0;
            gSprites[sMonPicSpriteIds[i]].subpriority = 1;
        }
    }

    sOpponentIconSpriteId = CreateSprite(&sSpriteTemplate_TypeIcon, 200, 200, 1);
    gSprites[sOpponentIconSpriteId].invisible = TRUE;
}

static void InitTypeRpsGfx(void)
{
    u32 i;
    u8 tilemap[0x800];

    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BG0CNT, 0);
    SetGpuReg(REG_OFFSET_BG1CNT, 0);
    SetGpuReg(REG_OFFSET_BG2CNT, 0);
    SetGpuReg(REG_OFFSET_BG3CNT, 0);
    DmaFill16(3, 0, VRAM, VRAM_SIZE);
    DmaFill32(3, 0, OAM, OAM_SIZE);
    DmaFill16(3, 0, PLTT, PLTT_SIZE);
    ScanlineEffect_Stop();
    /* ResetTasks() is not called here — run it from CB2_LoadTypeRpsGfx only, never from inside a task. */
    ResetSpriteData();
    ResetAllPicSprites();
    ResetPaletteFade();
    FreeAllSpritePalettes();
    gMain.state = 0;
    gSpecialVar_Result = TYPE_RPS_RESULT_LOSS;

    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    /* Same pattern as diploma.c: OBJ bits first, then ShowBg so BG visibility is merged into DISPCNT. */
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);

    {
        u32 tile[8];
        CpuFill32(0x11111111, tile, sizeof(tile));
        LoadBgTiles(0, (const void *)tile, sizeof(tile), 0);
    }

    LoadPalette(sCirclePal, BG_PLTT_ID(0), sizeof(sCirclePal));
    for (i = 0; i < ARRAY_COUNT(tilemap) / 2; i++)
        ((u16 *)tilemap)[i] = 0x0000;
    CopyToBgTilemapBufferRect(0, tilemap, 0, 0, 32, 32);
    CopyBgTilemapBufferToVram(0);
    ShowBg(0);

    InitWindows(sWindowTemplates);
    DeactivateAllTextPrinters();
    LoadPalette(gStandardMenuPalette, BG_PLTT_ID(15), PLTT_SIZE_4BPP);
    LoadMessageBoxGfx(0, 0x200, BG_PLTT_ID(14));
    DrawStdWindowFrame(WIN_COUNTDOWN, FALSE);
    PrintCountdownWindow(sText_Instructions);

    LoadTypeRpsSprites();

    BlendPalettes(PALETTES_ALL, 16, RGB_BLACK);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    EnableInterrupts(1);
    SetVBlankCallback(VBlankCB);
    SetMainCallback2(CB2_TypeRpsMain);
    CreateTask(Task_TypeRpsFadeIn, 0);
}

/* Field fade task must not call InitTypeRpsGfx directly: InitTypeRpsGfx used to ResetTasks() while still
 * inside RunTasks, corrupting task state (first entry often “works”, second entry black screen). */
static void CB2_LoadTypeRpsGfx(void)
{
    ResetTasks();
    InitTypeRpsGfx();
}

static void CB2_TypeRpsMain(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}
// Sets up the initial state of the minigame.
static void Task_TypeRpsFadeIn(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        gTasks[taskId].func = Task_TypeRpsRun;
        gTasks[taskId].data[0] = PHASE_SELECT;
        gTasks[taskId].data[1] = RPS_FIRE;
        gTasks[taskId].data[2] = 0;
        gTasks[taskId].data[3] = 0;
        gTasks[taskId].data[4] = 0;
        gTasks[taskId].data[5] = 0; // Bobbing timer for the circles.
    }
}
// Runs the minigame.
static void Task_TypeRpsRun(u8 taskId)
{
    u8 phase = gTasks[taskId].data[0];
    u8 *selection = (u8 *)&gTasks[taskId].data[1];
    s16 *timer = &gTasks[taskId].data[2];
    u8 playerChoice = gTasks[taskId].data[3];
    u8 opponentChoice = gTasks[taskId].data[4];
    u8 bobbingTimer = ++gTasks[taskId].data[5];
    u8 i;

    switch (phase)
    {
    case PHASE_SELECT:
        if (JOY_NEW(B_BUTTON))
        {
            gSpecialVar_Result = TYPE_RPS_RESULT_CANCEL;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            gTasks[taskId].data[0] = PHASE_FADE_OUT;
            break;
        }
        if (JOY_NEW(DPAD_LEFT))
        {
            *selection = (*selection + 2) % 3;
            PlaySE(SE_SELECT);
        }
        if (JOY_NEW(DPAD_RIGHT))
        {
            *selection = (*selection + 1) % 3;
            PlaySE(SE_SELECT);
        }
        bobbingTimer++;
        s16 bob = ((bobbingTimer / 12) & 1) ? -4 : -2; // Defined as a local variable, used to be declared outside the loop.
        for (i = 0; i < 3; i++)
        {
            s16 bounce = (i == *selection) ? bob : 0;

            if (sCircleSpriteIds[i] < MAX_SPRITES)
                gSprites[sCircleSpriteIds[i]].y2 = bounce;
            if (sMonPicSpriteIds[i] != 0xFFFF && sMonPicSpriteIds[i] < MAX_SPRITES)
                gSprites[sMonPicSpriteIds[i]].y2 = bounce;
        }
        if (JOY_NEW(A_BUTTON))
        {
            playerChoice = *selection;
            gTasks[taskId].data[3] = playerChoice;
            PlaySE(SE_SELECT);
            /*
             * Cries use the engine Pokémon cry player (gMPlay_PokemonCry); clear any prior cry state
             * so channels and ducking do not stack, then play the species for the confirmed circle.
             */
            StopCryAndClearCrySongs();
            PlayCry_Normal(SanitizeSpeciesId(sTypeRpsMonSpecies[playerChoice]), 0);
            *timer = 45;
            gTasks[taskId].data[0] = PHASE_COUNT_3;
            PrintCountdownWindow(sText_Count3);
            PlaySE(SE_SWITCH);
        }
        break;

    case PHASE_COUNT_3:
        if (--*timer == 0)
        {
            *timer = 45;
            gTasks[taskId].data[0] = PHASE_COUNT_2;
            PrintCountdownWindow(sText_Count2);
            PlaySE(SE_SWITCH);
        }
        break;

    case PHASE_COUNT_2:
        if (--*timer == 0)
        {
            *timer = 45;
            gTasks[taskId].data[0] = PHASE_COUNT_1;
            PrintCountdownWindow(sText_Count1);
            PlaySE(SE_SWITCH);
        }
        break;

    case PHASE_COUNT_1:
        if (--*timer == 0)
        {
            opponentChoice = Random() % 3;
            gTasks[taskId].data[4] = opponentChoice;
            gTasks[taskId].data[0] = PHASE_RESULT_WAIT;

            StartSpriteAnim(&gSprites[sOpponentIconSpriteId], opponentChoice);

            if (playerChoice == opponentChoice)
            {
                gSpecialVar_Result = TYPE_RPS_RESULT_LOSS;
                PlaySE(SE_BOO);
            }
            else if (TypeRpsPlayerWins(playerChoice, opponentChoice))
            {
                gSpecialVar_Result = TYPE_RPS_RESULT_WIN;
                PlaySE(SE_SUCCESS);
            }
            else
            {
                gSpecialVar_Result = TYPE_RPS_RESULT_LOSS;
                PlaySE(SE_BOO);
            }
            PrintTypeRpsOutcome(playerChoice, opponentChoice);
            gSprites[sOpponentIconSpriteId].invisible = FALSE;
        }
        break;

    case PHASE_RESULT_WAIT:
        if (JOY_NEW(A_BUTTON | B_BUTTON))
        {
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            gTasks[taskId].data[0] = PHASE_FADE_OUT;
        }
        break;

    case PHASE_FADE_OUT:
        if (!gPaletteFade.active)
        {
            MainCallback cb = sExitCallback;

            /* Per docs/dev/cb2_minigame_teardown.md: VBlank off before window/DMA teardown. */
            SetVBlankCallback(NULL);

            for (i = 0; i < 3; i++)
            {
                if (sMonPicSpriteIds[i] != 0xFFFF)
                {
                    FreeAndDestroyMonPicSprite(sMonPicSpriteIds[i]);
                    sMonPicSpriteIds[i] = 0xFFFF;
                }
            }

            gSpriteCoordOffsetX = 0;
            gSpriteCoordOffsetY = 0;
            SetGpuReg(REG_OFFSET_BLDCNT, 0);
            SetGpuReg(REG_OFFSET_BLDALPHA, 0);
            SetGpuReg(REG_OFFSET_BLDY, 0);

            TypeRpsStopCryAndBgmDuckTask();

            DeactivateAllTextPrinters();
            while (IsDma3ManagerBusyWithBgCopy())
                ;
            TypeRpsAbandonWindowStateForReturn();
            ResetBgsAndClearDma3BusyFlags(0);
            SetMainCallback2(cb);
        }
        break;
    }
}

static void Task_TypeRpsFadeToGame(u8 taskId)
{
    switch (gTasks[taskId].data[0])
    {
    case 0:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        gTasks[taskId].data[0]++;
        break;
    case 1:
        if (!gPaletteFade.active)
        {
            /* Hand off to CB2 so ResetTasks runs outside RunTasks (see CB2_LoadTypeRpsGfx). */
            SetMainCallback2(CB2_LoadTypeRpsGfx);
        }
        break;
    }
}

void PlayTypeRpsMinigame(MainCallback exitCallback)
{
    u8 taskId;

    sExitCallback = exitCallback;
    LockPlayerFieldControls();
    taskId = CreateTask(Task_TypeRpsFadeToGame, 0);
    gTasks[taskId].data[0] = 0;
}
