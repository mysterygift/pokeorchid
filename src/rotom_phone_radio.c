// Rotom Phone RADIO app (mock_radio.py, approved 2026-11-17): teal theme, LCD tuner with a Gen 3 red
// needle, station card with the region plate, now-playing tray with EQ bars. ←/→ tune (eased needle,
// music crossfades), A on / off, B back. The music logic lives in src/radio.c.
//
// Layers: BG3 grid, BG2 static art (export_radio.py; pal 1 = LCD, pal 3 = station accent), BG0 windows.
// OBJ: needle, Tune chevrons.
#include "global.h"
#include "radio.h"
#include "rotom_phone.h"
#include "bg.h"
#include "decompress.h"
#include "gpu_regs.h"
#include "graphics.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "palette.h"
#include "phone_ui.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "data/rotom_phone_radio_layout.h"

static const u32 sRadioBg_Gfx[] = INCGFX_U32("graphics/rotom_phone/radio_bg.png", ".4bpp.smol");
static const u32 sRadioBg_Tilemap[] = INCGFX_U32("graphics/rotom_phone/radio_bg.bin", ".smolTM");
static const u16 sRadioBg_Pal[] = INCGFX_U16("graphics/rotom_phone/radio_bg.pal", ".gbapal");
static const u8 sNeedle_Gfx[] = INCGFX_U8("graphics/rotom_phone/radio_needle.png", ".4bpp");
static const u16 sNeedle_Pal[] = INCGFX_U16("graphics/rotom_phone/radio_needle.png", ".gbapal");
static const u8 sGlyphs_Gfx[] = INCGFX_U8("graphics/rotom_phone/quests_glyphs.png", ".4bpp");   // keypad A at x 24 (kit roles)

#define TAG_R_NEEDLE    0x7D00
#define TAG_R_CHEVRON   0x7D01

#define PAL_KIT     0
#define PAL_LCD     1
#define PAL_GRID    2
#define PAL_STATION 3
// LCD palette (export_radio.py LCD_PAL)
#define L_SCR_DEEP  3
#define L_INK       4
#define L_TICK      5
#define L_LCD       7
#define L_MHZ       8
#define L_DIM       9
#define L_DIM_MHZ   10
#define L_WHITE     11
#define L_NAME_DIM  12
#define L_DOT       13

#define TUNE_FRAMES 8

enum { WIN_TITLE, WIN_LCD, WIN_CARD, WIN_WELL, WIN_TRAY };

static const struct WindowTemplate sWindows[] =
{
    [WIN_TITLE] = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 2, .paletteNum = PAL_KIT, .baseBlock = 1 },
    [WIN_LCD]   = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 2, .width = 30, .height = 8, .paletteNum = PAL_LCD, .baseBlock = 61 },
    [WIN_CARD]  = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 10, .width = 30, .height = 4, .paletteNum = PAL_STATION, .baseBlock = 301 },
    [WIN_WELL]  = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 14, .width = 5, .height = 6, .paletteNum = PAL_STATION, .baseBlock = 421 },
    [WIN_TRAY]  = { .bg = 0, .tilemapLeft = 5, .tilemapTop = 14, .width = 25, .height = 6, .paletteNum = PAL_STATION, .baseBlock = 451 },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 28, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0 },
    { .bg = 2, .charBaseIndex = 2, .mapBaseIndex = 30, .screenSize = 0, .paletteMode = 0, .priority = 2, .baseTile = 0 },
    { .bg = 3, .charBaseIndex = 2, .mapBaseIndex = 31, .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0 },
};

static const u8 sColors_Title[] = {0, KIT_WHITE, KIT_ACCENT_DARK};
static const u8 sColors_Ink[] = {0, KIT_INK, KIT_PANEL_SHADE};
static const u8 sColors_InkSel[] = {0, KIT_INK, KIT_SELECT_DARK};
static const u8 sColors_Soft[] = {0, KIT_INK_SOFT, KIT_PANEL_SHADE};
static const u8 sColors_OnPlate[] = {0, KIT_WHITE, KIT_ACCENT_DARK};
static const u8 sColors_OffSwitch[] = {0, KIT_WHITE, KIT_INK_SOFT};

struct RadioApp
{
    u16 bg2Tilemap[32 * 32];
    u16 bg3Tilemap[32 * 32];
    u8 tuned;           // station on the dial
    bool8 on;
    u8 gridTimer;
    u8 needleSpriteId;
    u8 tuneFrame;       // < TUNE_FRAMES while the needle moves
    s16 needleFrom;
    s16 needleTo;
    u16 frame;
    bool8 exiting;
};

static EWRAM_DATA struct RadioApp *sR = NULL;
static EWRAM_DATA u8 sLastTuned = 0;

static void CB2_SetupRadio(void);
static void Task_Radio(u8 taskId);
static void DrawAll(void);

void CB2_InitPhoneRadio(void)
{
    s32 st = Radio_GetStationId();
    sR = AllocZeroed(sizeof(*sR));
    sR->on = (st >= 0);
    sR->tuned = st >= 0 ? st : (Radio_IsStationUnlocked(sLastTuned) ? sLastTuned : RADIO_TOSA_FM);
    sR->tuneFrame = TUNE_FRAMES;
    gMain.state = 0;
    SetMainCallback2(CB2_SetupRadio);
}

// ---------------------------------------------------------------- the phone home screen's RADIO line
void PhoneApp_RadioRotomText(u8 *dest)
{
    s32 st = Radio_GetStationId();
    const struct RadioSong *song = Radio_GetCurrentSong();

    if (st >= 0 && !Radio_HasSignal())
    {
        StringCopy(dest, COMPOUND_STRING("No signal down here…\nMap music only, bzzt."));
    }
    else if (st >= 0 && song != NULL)
    {
        StringCopy(gStringVar1, Radio_GetStation(st)->name);
        StringCopy(gStringVar2, song->title);
        StringExpandPlaceholders(dest, COMPOUND_STRING("{STR_VAR_1} is on, bzzt!\nNow: {STR_VAR_2}"));
    }
    else
    {
        StringCopy(dest, COMPOUND_STRING("Tune in to TOSA FM!\nNew hits every hour!"));
    }
}

// ---------------------------------------------------------------- setup
static void VBlankCB_Radio(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_Radio(void)
{
    if ((++sR->gridTimer & 3) == 0)
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

static const struct OamData sOam_8x32 = { .shape = SPRITE_SHAPE(8x32), .size = SPRITE_SIZE(8x32), .priority = 0 };
static const struct OamData sOam_8x16 = { .shape = SPRITE_SHAPE(8x16), .size = SPRITE_SIZE(8x16), .priority = 0 };
static const union AnimCmd sAnim_ChevronL[] = { ANIMCMD_FRAME(0, 0), ANIMCMD_END };
static const union AnimCmd sAnim_ChevronR[] = { ANIMCMD_FRAME(0, 0, .hFlip = TRUE), ANIMCMD_END };
static const union AnimCmd *const sAnims_Chevron[] = { sAnim_ChevronL, sAnim_ChevronR };

static const struct SpriteTemplate sTemplate_Needle =
{
    .tileTag = TAG_R_NEEDLE, .paletteTag = TAG_R_NEEDLE, .oam = &sOam_8x32, .anims = gDummySpriteAnimTable,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_Chevron =
{
    .tileTag = TAG_R_CHEVRON, .paletteTag = TAG_R_CHEVRON, .oam = &sOam_8x16, .anims = sAnims_Chevron,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static void LoadGfx(void)
{
    u32 x, y;
    static const struct SpriteSheet sheets[] =
    {
        { sNeedle_Gfx, 8 * 32 / 2, TAG_R_NEEDLE },
        { gSatchelArrow_Gfx, 8 * 16 / 2, TAG_R_CHEVRON },
        {}
    };
    static const struct SpritePalette pals[] =
    {
        { sNeedle_Pal, TAG_R_NEEDLE },
        { gSatchelArrow_Pal, TAG_R_CHEVRON },
        {}
    };

    DecompressAndCopyTileDataToVram(2, sRadioBg_Gfx, 0, 0, 0);
    DecompressDataWithHeaderWram(sRadioBg_Tilemap, sR->bg2Tilemap);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            sR->bg3Tilemap[y * 32 + x] = (RADIO_BG_TILES + (x & 1) + (y & 1) * 2) | (PAL_GRID << 12);
    LoadPalette(sRadioBg_Pal, BG_PLTT_ID(0), 4 * PLTT_SIZE_4BPP);
    LoadSpriteSheets(sheets);
    LoadSpritePalettes(pals);
}

static void CB2_SetupRadio(void)
{
    u32 i;

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
        for (i = 0; i < 4; i++)
        {
            ChangeBgX(i, 0, BG_COORD_SET);
            ChangeBgY(i, 0, BG_COORD_SET);
        }
        SetBgTilemapBuffer(2, sR->bg2Tilemap);
        SetBgTilemapBuffer(3, sR->bg3Tilemap);
        InitWindows(sWindows);
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
        LoadGfx();
        gMain.state++;
        break;
    case 2:
        if (!FreeTempTileDataBuffersIfPossible())
            gMain.state++;
        break;
    case 3:
    {
        // mock: Tune hint right-aligned at 236; chevrons at (x - 16, 126) and (x - 7, 126)
        s32 x = 236 - GetStringWidth(FONT_NARROW, COMPOUND_STRING("Tune"), 0);
        u8 id;
        sR->needleSpriteId = CreateSprite(&sTemplate_Needle, RADIO_FX(Radio_GetStation(sR->tuned)->freqTenths) - 3 + 4, 32 + 16, 0);
        CreateSprite(&sTemplate_Chevron, x - 16, 126 + 1, 0);
        id = CreateSprite(&sTemplate_Chevron, x - 7, 126 + 1, 0);
        StartSpriteAnim(&gSprites[id], 1);
        for (i = 0; i < 5; i++)
            PutWindowTilemap(i);
        DrawAll();
        ScheduleBgCopyTilemapToVram(0);
        ScheduleBgCopyTilemapToVram(2);
        ScheduleBgCopyTilemapToVram(3);
        gMain.state++;
        break;
    }
    case 4:
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
        ShowBg(0);
        ShowBg(2);
        ShowBg(3);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB_Radio);
        SetMainCallback2(CB2_Radio);
        CreateTask(Task_Radio, 0);
        break;
    }
}

// ---------------------------------------------------------------- drawing
static void PhoneUI_Disc(u32 win, s32 cx2, s32 cy2, s32 r2, u8 face, u8 outline)
{
    // centre and radius in half pixels; outline = the outermost ring of pixels
    s32 x, y;
    for (y = (cy2 - r2) / 2 - 1; y <= (cy2 + r2) / 2 + 1; y++)
    {
        for (x = (cx2 - r2) / 2 - 1; x <= (cx2 + r2) / 2 + 1; x++)
        {
            s32 dx = 2 * x + 1 - cx2, dy = 2 * y + 1 - cy2, d2 = dx * dx + dy * dy;
            if (d2 <= r2 * r2)
                FillWindowPixelRect(win, PIXEL_FILL(d2 > (r2 - 2) * (r2 - 2) && outline ? outline : face), x, y, 1, 1);
        }
    }
}

static void LoadStationColours(void)
{
    const u16 *ramp = Radio_GetRamp(sR->tuned);
    LoadPalette(&ramp[0], BG_PLTT_ID(PAL_STATION) + KIT_ACCENT_DARK, sizeof(u16));
    LoadPalette(&ramp[1], BG_PLTT_ID(PAL_STATION) + KIT_ACCENT, sizeof(u16));
    LoadPalette(&ramp[2], BG_PLTT_ID(PAL_STATION) + KIT_ACCENT_LIGHT, sizeof(u16));
    LoadPalette(&ramp[1], BG_PLTT_ID(PAL_LCD) + L_DOT, sizeof(u16));
}

static void DrawTitle(void)
{
    FillWindowPixelBuffer(WIN_TITLE, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, 23, 0, 0, 0, sColors_Title, TEXT_SKIP_DRAW, COMPOUND_STRING("RADIO"));
    // on / off switch pill
    if (sR->on)
    {
        PhoneUI_RoundBox(WIN_TITLE, 200, 2, 36, 12, 4, KIT_SELECT, KIT_INK, KIT_SELECT_LIGHT, KIT_SELECT_DARK, TRUE);
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NARROW, 210, -1 + 1, 0, 0, sColors_InkSel, TEXT_SKIP_DRAW, COMPOUND_STRING("ON"));
        PhoneUI_Disc(WIN_TITLE, 2 * 229, 2 * 7 + 1, 7, KIT_WHITE, KIT_INK);
    }
    else
    {
        PhoneUI_RoundBox(WIN_TITLE, 200, 2, 36, 12, 4, KIT_PANEL_DARK, KIT_INK, KIT_PANEL_SHADE, KIT_INK_SOFT, TRUE);
        PhoneUI_Disc(WIN_TITLE, 2 * 206, 2 * 7 + 1, 7, KIT_WHITE, KIT_INK);
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NARROW, 213, -1 + 1, 0, 0, sColors_OffSwitch, TEXT_SKIP_DRAW, COMPOUND_STRING("OFF"));
    }
    CopyWindowToVram(WIN_TITLE, COPYWIN_GFX);
}

static void DrawLcd(void)
{
    const struct RadioStation *st = Radio_GetStation(sR->tuned);
    static const u8 sColors_Freq[] = {0, L_LCD, L_SCR_DEEP};
    static const u8 sColors_FreqOff[] = {0, L_DIM, L_SCR_DEEP};
    static const u8 sColors_Mhz[] = {0, L_MHZ, 0};
    static const u8 sColors_MhzOff[] = {0, L_DIM_MHZ, 0};
    static const u8 sColors_Name[] = {0, L_WHITE, L_SCR_DEEP};
    static const u8 sColors_NameOff[] = {0, L_NAME_DIM, L_SCR_DEEP};
    u8 *p;
    u32 i, w;

    FillWindowPixelBuffer(WIN_LCD, PIXEL_FILL(0));
    p = ConvertIntToDecimalStringN(gStringVar1, st->freqTenths / 10, STR_CONV_MODE_LEFT_ALIGN, 3);
    *p++ = CHAR_PERIOD;
    ConvertIntToDecimalStringN(p, st->freqTenths % 10, STR_CONV_MODE_LEFT_ALIGN, 1);
    AddTextPrinterParameterized4(WIN_LCD, FONT_NORMAL, 12, 20 - 16, 0, 0, sR->on ? sColors_Freq : sColors_FreqOff, TEXT_SKIP_DRAW, gStringVar1);
    w = GetStringWidth(FONT_NORMAL, gStringVar1, 0);
    AddTextPrinterParameterized4(WIN_LCD, FONT_SMALL, 14 + w, 22 - 16, 0, 0, sR->on ? sColors_Mhz : sColors_MhzOff, TEXT_SKIP_DRAW, COMPOUND_STRING("MHz"));
    AddTextPrinterParameterized4(WIN_LCD, FONT_NORMAL, 228 - GetStringWidth(FONT_NORMAL, st->name, 0), 20 - 16, 0, 0,
                                 sR->on ? sColors_Name : sColors_NameOff, TEXT_SKIP_DRAW, st->name);
    // station markers (mock: disc r 2.5 at (fx, 47.5); the tuned one in its colour, outlined)
    for (i = 0; i < RADIO_STATION_COUNT; i++)
    {
        s32 x = RADIO_FX(Radio_GetStation(i)->freqTenths);
        if (i == sR->tuned)
            PhoneUI_Disc(WIN_LCD, 2 * x, 2 * (47 - 16) + 1, 5, L_DOT, L_INK);
        else
            PhoneUI_Disc(WIN_LCD, 2 * x, 2 * (47 - 16) + 1, 5, L_TICK, 0);
    }
    CopyWindowToVram(WIN_LCD, COPYWIN_GFX);
}

static void DrawCard(void)
{
    const struct RadioStation *st = Radio_GetStation(sR->tuned);

    FillWindowPixelBuffer(WIN_CARD, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_CARD, FONT_NARROW, 32 - GetStringWidth(FONT_NARROW, st->region, 0) / 2, 89 - 80, 0, 0,
                                 sColors_OnPlate, TEXT_SKIP_DRAW, st->region);
    AddTextPrinterParameterized4(WIN_CARD, FONT_NORMAL, 62, 81 - 80, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, st->name);
    AddTextPrinterParameterized4(WIN_CARD, FONT_NARROW, 62, 95 - 80, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, st->tagline);
    CopyWindowToVram(WIN_CARD, COPYWIN_GFX);
}

static bool32 IsPlaying(void)
{
    return sR->on && Radio_HasSignal() && Radio_GetCurrentSong() != NULL;
}

static void DrawEq(void)
{
    static const u8 sHeights[4][5] = { {4, 8, 6, 10, 5}, {7, 5, 10, 6, 8}, {9, 6, 4, 8, 10}, {5, 10, 7, 4, 6} };
    u32 k, set = (sR->frame / 6) % 4;

    FillWindowPixelRect(WIN_WELL, PIXEL_FILL(0), 11, 128 - 112, 20, 18);
    for (k = 0; k < 5; k++)
    {
        s32 x = 11 + k * 4, h = IsPlaying() ? sHeights[set][k] : 1;
        u8 face = IsPlaying() ? KIT_ACCENT : KIT_PANEL_SHADE, top = IsPlaying() ? KIT_ACCENT_LIGHT : KIT_PANEL_SHADE;
        FillWindowPixelRect(WIN_WELL, PIXEL_FILL(face), x, 145 - h - 112, 3, h + 1);
        FillWindowPixelRect(WIN_WELL, PIXEL_FILL(top), x, 145 - h - 112, 3, 1);
    }
    CopyWindowToVram(WIN_WELL, COPYWIN_GFX);
}

static void DrawTray(void)
{
    static const char sNote[7][7] = { "...XXX", "...XXX", "...X..", "...X..", ".XXX..", "XXXX..", ".XX..." };
    const struct RadioSong *song = Radio_GetCurrentSong();
    const u8 *s;
    s32 x, y, ox = 40;   // window starts at x 40

    FillWindowPixelBuffer(WIN_TRAY, PIXEL_FILL(0));
    if (sR->on && !Radio_HasSignal())
    {
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 47 - ox, 118 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, COMPOUND_STRING("No signal…"));
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NORMAL, 47 - ox, 132 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, COMPOUND_STRING("Map music plays."));
    }
    else if (sR->on && song != NULL)
    {
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 47 - ox, 118 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, COMPOUND_STRING("Now playing"));
        for (y = 0; y < 7; y++)
            for (x = 0; x < 6; x++)
                if (sNote[y][x] == 'X')
                    FillWindowPixelRect(WIN_TRAY, PIXEL_FILL(KIT_ACCENT), 47 - ox + x, 137 - 112 + y, 1, 1);
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NORMAL, 56 - ox, 132 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, song->title);
    }
    else
    {
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 47 - ox, 118 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, COMPOUND_STRING("Radio off"));
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NORMAL, 47 - ox, 132 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, COMPOUND_STRING("Map music plays."));
    }
    s = COMPOUND_STRING("Tune");
    AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 236 - ox - GetStringWidth(FONT_NARROW, s, 0), 118 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, s);
    s = COMPOUND_STRING("On/Off");
    x = 236 - ox - GetStringWidth(FONT_NARROW, s, 0);
    AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, x, 136 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, s);
    BlitBitmapRectToWindow(WIN_TRAY, sGlyphs_Gfx, 24, 0, 48, 16, x - 12, 140 - 112, 8, 8);
    CopyWindowToVram(WIN_TRAY, COPYWIN_GFX);
}

static void DrawAll(void)
{
    LoadStationColours();
    DrawTitle();
    DrawLcd();
    DrawCard();
    DrawEq();
    DrawTray();
}

// ---------------------------------------------------------------- input
static void Tune(s32 dir)
{
    s32 next = sR->tuned;
    u32 n;

    for (n = 0; n < RADIO_STATION_COUNT; n++)
    {
        next = (next + RADIO_STATION_COUNT + dir) % RADIO_STATION_COUNT;
        if (Radio_IsStationUnlocked(next))
            break;
    }
    if (next == sR->tuned)
    {
        PlaySE(SE_FAILURE);
        return;
    }
    PlaySE(SE_SELECT);
    sR->needleFrom = gSprites[sR->needleSpriteId].x;
    sR->needleTo = RADIO_FX(Radio_GetStation(next)->freqTenths) - 3 + 4;
    sR->tuneFrame = 0;
    sR->tuned = next;
    sLastTuned = next;
    if (sR->on)
        Radio_SetStation(next);     // the music crossfades to the new station
    DrawAll();
}

static void Task_Radio(u8 taskId)
{
    sR->frame++;
    if (sR->frame % 6 == 0)
        DrawEq();
    if (sR->tuneFrame < TUNE_FRAMES)
    {
        // ease-out: 1 - (1 - t)^2
        s32 t = ++sR->tuneFrame, left = TUNE_FRAMES - t;
        gSprites[sR->needleSpriteId].x = sR->needleTo - (sR->needleTo - sR->needleFrom) * left * left / (TUNE_FRAMES * TUNE_FRAMES);
    }
    if (gPaletteFade.active)
        return;
    if (sR->exiting)
    {
        DestroyTask(taskId);
        FreeAllWindowBuffers();
        FREE_AND_SET_NULL(sR);
        SetMainCallback2(CB2_ReturnToRotomPhone);
        return;
    }
    if (JOY_REPEAT(DPAD_LEFT))
    {
        Tune(-1);
    }
    else if (JOY_REPEAT(DPAD_RIGHT))
    {
        Tune(1);
    }
    else if (JOY_NEW(A_BUTTON))
    {
        PlaySE(SE_SELECT);
        sR->on = !sR->on;
        Radio_SetStation(sR->on ? sR->tuned : -1);
        DrawAll();
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sR->exiting = TRUE;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
}
