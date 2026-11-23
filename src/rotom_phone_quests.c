// Rotom Phone QUESTS app (mock_quests.py, approved 2026-11-17): PSF's Unbound Quest Menu, reskinned.
// Data and save bits: src/quests.c. This file is only the screen: filter tabs (L/R: All / New / Active /
// Reward / Done), bag-style pill rows with pictogram state tags, ★ favourites (Select), hidden A–Z sort
// (Start), a tray with the quest's sprite and location, and the steps view (A) for quests with subquests.
// Locked quests are hidden; the header counts completed / unlocked.
// Orchid: a 6th tab, RESEARCH (Professor Palm's research tasks, src/research.c), appears once Palm has called
// after the first gym badge; its header shows the Research Rank (stars) and research points, A on a finished
// task sends the notes to Palm (reward + RP, rank-up gift), surveys have one step per habitat.
//
// Layers: BG3 grid, BG2 static art (export_quests.py), BG0 windows (pills, text, thumb, progress fill).
// OBJ: the selected filter tab, state tags, the quest sprite in the tray's icon well.
#include "global.h"
#include "quests.h"
#include "research.h"
#include "region_map.h"
#include "item.h"
#include "pokedex_habitats.h"
#include "rotom_phone.h"
#include "bg.h"
#include "decompress.h"
#include "event_object_movement.h"
#include "gpu_regs.h"
#include "item_icon.h"
#include "main.h"
#include "malloc.h"
#include "menu.h"
#include "palette.h"
#include "phone_ui.h"
#include "pokemon_icon.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "strings.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "data/rotom_phone_quests_layout.h"

static const u32 sQuestsBg_Gfx[] = INCGFX_U32("graphics/rotom_phone/quests_bg.png", ".4bpp.smol");
static const u32 sQuestsList_Tilemap[] = INCGFX_U32("graphics/rotom_phone/quests_list.bin", ".smolTM");
static const u32 sQuestsSteps_Tilemap[] = INCGFX_U32("graphics/rotom_phone/quests_steps.bin", ".smolTM");
static const u32 sQuestsList6_Tilemap[] = INCGFX_U32("graphics/rotom_phone/quests_list6.bin", ".smolTM");
static const u16 sQuestsBg_Pal[] = INCGFX_U16("graphics/rotom_phone/quests_bg.pal", ".gbapal");
static const u8 sTab_Gfx[] = INCGFX_U8("graphics/rotom_phone/quests_tab.png", ".4bpp");
static const u8 sTagsA_Gfx[] = INCGFX_U8("graphics/rotom_phone/quests_tags_a.png", ".4bpp");
static const u16 sTagsA_Pal[] = INCGFX_U16("graphics/rotom_phone/quests_tags_a.pal", ".gbapal");
static const u8 sTagsB_Gfx[] = INCGFX_U8("graphics/rotom_phone/quests_tags_b.png", ".4bpp");
static const u16 sTagsB_Pal[] = INCGFX_U16("graphics/rotom_phone/quests_tags_b.pal", ".gbapal");
static const u8 sGlyphs_Gfx[] = INCGFX_U8("graphics/rotom_phone/quests_glyphs.png", ".4bpp");

#define TAG_Q_KIT       0x7C00
#define TAG_Q_TAB       0x7C01
#define TAG_Q_TAGS_A    0x7C02
#define TAG_Q_TAGS_B    0x7C03
#define TAG_Q_ITEM      0x7C04

#define ROWS        5
#define ROW_Y       35
#define ROW_H       16
#define PILL_X      8
#define PILL_W      218
#define TRAY_Y      114
#define WELL_X      20
#define WELL_Y      137

enum { FILTER_ALL, FILTER_NEW, FILTER_ACTIVE, FILTER_REWARD, FILTER_DONE, FILTER_RESEARCH, FILTER_COUNT };
enum { POPUP_NONE, POPUP_CLAIM, POPUP_RANK, POPUP_BAG_FULL };
enum { STATE_NEW, STATE_ACTIVE, STATE_REWARD, STATE_DONE, STATE_LOCKED };
enum { WIN_TITLE, WIN_BAR, WIN_ROWS, WIN_TRAY };

static const struct WindowTemplate sWindows[] =
{
    [WIN_TITLE] = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 2, .paletteNum = 0, .baseBlock = 1 },
    [WIN_BAR]   = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 2, .width = 30, .height = 2, .paletteNum = 1, .baseBlock = 61 },
    [WIN_ROWS]  = { .bg = 0, .tilemapLeft = 1, .tilemapTop = 4, .width = 29, .height = 10, .paletteNum = 0, .baseBlock = 121 },
    [WIN_TRAY]  = { .bg = 0, .tilemapLeft = 0, .tilemapTop = 14, .width = 30, .height = 6, .paletteNum = 0, .baseBlock = 411 },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 28, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0 },
    { .bg = 2, .charBaseIndex = 2, .mapBaseIndex = 30, .screenSize = 0, .paletteMode = 0, .priority = 2, .baseTile = 0 },
    { .bg = 3, .charBaseIndex = 2, .mapBaseIndex = 31, .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0 },
};

static const u8 sColors_Title[] = {0, KIT_WHITE, KIT_ACCENT_DARK};
static const u8 sColors_Label[] = {0, KIT_WHITE, KIT_INK_SOFT};
static const u8 sColors_Ink[] = {0, KIT_INK, KIT_PANEL_SHADE};
static const u8 sColors_InkSel[] = {0, KIT_INK, KIT_SELECT_DARK};
static const u8 sColors_Soft[] = {0, KIT_INK_SOFT, KIT_PANEL_SHADE};
static const u8 sColors_SoftSel[] = {0, KIT_INK_SOFT, KIT_SELECT_DARK};

static const u8 *const sFilterNames[FILTER_COUNT] =
{
    COMPOUND_STRING("All"), COMPOUND_STRING("New"), COMPOUND_STRING("Active"), COMPOUND_STRING("Reward"), COMPOUND_STRING("Done"),
    COMPOUND_STRING("Research"),
};
static const u8 sText_Unknown[] = _("??????");

struct QuestsApp
{
    u16 bg2Tilemap[32 * 32];
    u16 bg3Tilemap[32 * 32];
    MainCallback exitCallback;
    u8 list[QUEST_ARRAY_COUNT];
    u8 count;
    u8 cursor;
    u8 top;
    u8 filter;
    bool8 alpha;
    bool8 steps;
    u8 parent;
    u8 listCursor;  // restored when leaving the steps view
    u8 listTop;
    u8 gridTimer;
    u8 exiting;
    u8 tabSpriteId;
    u8 tagSpriteIds[ROWS];
    u8 iconSpriteId;
    u8 iconType;
    u8 popup;           // POPUP_*: the claim / rank-up message over the rows
    u8 popupTask;
    u8 popupOldRank;
    mapsec_u16_t steps6[RESEARCH_MAX_STEPS];   // research survey steps (habitats)
    // research tasks are worked out from the dex: computed once per list build, not per row draw
    u8 rState[32];
    u16 rDone[32], rTotal[32];
    u8 stepState[RESEARCH_MAX_STEPS];
    u16 stepDone[RESEARCH_MAX_STEPS], stepTotal[RESEARCH_MAX_STEPS], stepSeen[RESEARCH_MAX_STEPS];
};

static EWRAM_DATA struct QuestsApp *sQ = NULL;
// remembered between visits (PSF kept scroll + row the same way)
static EWRAM_DATA u8 sSavedFilter = 0;
static EWRAM_DATA bool8 sSavedAlpha = FALSE;

static void CB2_SetupQuests(void);
static void Task_Quests(u8 taskId);
static void Redraw(bool32 rebuild);

// ---------------------------------------------------------------- data helpers
static bool32 IsUnlocked(u32 q)
{
    return QuestMenu_GetSetQuestState(q, FLAG_GET_UNLOCKED) != 0;
}

static u32 QuestState(u32 q)
{
    if (!IsUnlocked(q))
        return STATE_LOCKED;
    if (QuestMenu_GetSetQuestState(q, FLAG_GET_COMPLETED))
        return STATE_DONE;
    if (QuestMenu_GetSetQuestState(q, FLAG_GET_REWARD))
        return STATE_REWARD;
    if (QuestMenu_GetSetQuestState(q, FLAG_GET_ACTIVE))
        return STATE_ACTIVE;
    return STATE_NEW;   // PSF's INACTIVE
}

static bool32 IsFavorite(u32 q)
{
    return QuestMenu_GetSetQuestState(q, FLAG_GET_FAVORITE) != 0;
}

static u32 StepsDone(u32 q)
{
    u32 i, n = 0;
    for (i = 0; i < gSideQuests[q].numSubquests; i++)
        n += QuestMenu_GetSetSubquestState(q, FLAG_GET_COMPLETED, i) ? 1 : 0;
    return n;
}

// done steps, then the first open one is active, later ones locked (shown as ??????)
static u32 StepState(u32 q, u32 i)
{
    u32 k;
    if (QuestMenu_GetSetSubquestState(q, FLAG_GET_COMPLETED, i))
        return STATE_DONE;
    for (k = 0; k < i; k++)
    {
        if (!QuestMenu_GetSetSubquestState(q, FLAG_GET_COMPLETED, k))
            return STATE_LOCKED;
    }
    return QuestState(q) == STATE_DONE ? STATE_DONE : STATE_ACTIVE;
}

static bool32 HasSteps(u32 q)
{
    return gSideQuests[q].numSubquests != 0 && QuestState(q) != STATE_NEW && QuestState(q) != STATE_LOCKED;
}

static u32 NumFilters(void)
{
    return Research_IsUnlocked() ? FILTER_COUNT : FILTER_RESEARCH;
}

static bool32 IsResearch(void)
{
    return sQ->filter == FILTER_RESEARCH;
}

static bool32 MatchesFilter(u32 q, u32 filter)
{
    u32 st = QuestState(q);
    switch (filter)
    {
    case FILTER_NEW:    return st == STATE_NEW;
    case FILTER_ACTIVE: return st == STATE_ACTIVE;
    case FILTER_REWARD: return st == STATE_REWARD;
    case FILTER_DONE:   return st == STATE_DONE;
    case FILTER_RESEARCH: return FALSE;
    default:            return st != STATE_LOCKED;
    }
}

static u32 CountFilter(u32 filter)
{
    u32 q, n = 0;
    if (filter == FILTER_RESEARCH)
    {
        for (q = 0; q < Research_Count(); q++)
            n += Research_IsVisible(q) ? 1 : 0;
        return n;
    }
    for (q = 0; q < QUEST_COUNT; q++)
        n += MatchesFilter(q, filter) ? 1 : 0;
    return n;
}

static void BuildList(void)
{
    u32 q, i, j;

    sQ->count = 0;
    if (sQ->steps && IsResearch())
    {
        sQ->count = Research_GetSteps(sQ->parent, sQ->steps6);
        for (i = 0; i < sQ->count; i++)
        {
            struct HabitatCounts c;
            Habitats_CountSections(&sQ->steps6[i], 1, &c);
            sQ->list[i] = i;
            sQ->stepDone[i] = c.catalogued;
            sQ->stepTotal[i] = c.total;
            sQ->stepSeen[i] = c.seen;
            sQ->stepState[i] = (c.total && c.catalogued == c.total) ? STATE_DONE : (c.seen ? STATE_ACTIVE : STATE_NEW);
        }
        return;
    }
    if (sQ->steps)
    {
        for (i = 0; i < gSideQuests[sQ->parent].numSubquests; i++)
            sQ->list[sQ->count++] = i;
        return;
    }
    if (IsResearch())
    {
        for (q = 0; q < Research_Count(); q++)
        {
            if (Research_IsVisible(q))
            {
                sQ->list[sQ->count++] = q;
                sQ->rState[q] = Research_GetState(q);
                Research_GetProgress(q, &sQ->rDone[q], &sQ->rTotal[q]);
            }
        }
        return;
    }
    // favourites first, then quest order (or A–Z)
    for (j = 0; j < 2; j++)
    {
        for (q = 0; q < QUEST_COUNT; q++)
        {
            if (MatchesFilter(q, sQ->filter) && IsFavorite(q) == (j == 0))
                sQ->list[sQ->count++] = q;
        }
    }
    if (sQ->alpha)
    {
        for (i = 1; i < sQ->count; i++)     // insertion sort by name, favourites kept on top
        {
            u8 v = sQ->list[i];
            j = i;
            while (j > 0 && IsFavorite(sQ->list[j - 1]) == IsFavorite(v)
                   && StringCompare(gSideQuests[sQ->list[j - 1]].name, gSideQuests[v].name) > 0)
            {
                sQ->list[j] = sQ->list[j - 1];
                j--;
            }
            sQ->list[j] = v;
        }
    }
}

// ---------------------------------------------------------------- entry / setup
void QuestMenu_Init(u8 a0, MainCallback callback)
{
    sQ = AllocZeroed(sizeof(*sQ));
    sQ->exitCallback = callback;
    sQ->filter = sSavedFilter < NumFilters() ? sSavedFilter : 0;
    sQ->alpha = sSavedAlpha;
    gMain.state = 0;
    SetMainCallback2(CB2_SetupQuests);
}

static void VBlankCB_Quests(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void CB2_Quests(void)
{
    if ((++sQ->gridTimer & 3) == 0)
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

static const struct OamData sOam_32x16 = { .shape = SPRITE_SHAPE(32x16), .size = SPRITE_SIZE(32x16), .priority = 0 };   // over the BG0 row pills
static const union AnimCmd sAnim_Q0[] = { ANIMCMD_FRAME(0, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q1[] = { ANIMCMD_FRAME(8, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q2[] = { ANIMCMD_FRAME(16, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q3[] = { ANIMCMD_FRAME(24, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q4[] = { ANIMCMD_FRAME(32, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q5[] = { ANIMCMD_FRAME(40, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q6[] = { ANIMCMD_FRAME(48, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q7[] = { ANIMCMD_FRAME(56, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q8[] = { ANIMCMD_FRAME(64, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q9[] = { ANIMCMD_FRAME(72, 0), ANIMCMD_END };
static const union AnimCmd sAnim_Q10[] = { ANIMCMD_FRAME(80, 0), ANIMCMD_END };
static const union AnimCmd *const sAnims_Frames[] = { sAnim_Q0, sAnim_Q1, sAnim_Q2, sAnim_Q3, sAnim_Q4, sAnim_Q5,
                                                      sAnim_Q6, sAnim_Q7, sAnim_Q8, sAnim_Q9, sAnim_Q10 };

static const struct SpriteTemplate sTemplate_Tab =
{
    .tileTag = TAG_Q_TAB, .paletteTag = TAG_Q_KIT, .oam = &sOam_32x16, .anims = sAnims_Frames,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_TagA =
{
    .tileTag = TAG_Q_TAGS_A, .paletteTag = TAG_Q_TAGS_A, .oam = &sOam_32x16, .anims = sAnims_Frames,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_TagB =
{
    .tileTag = TAG_Q_TAGS_B, .paletteTag = TAG_Q_TAGS_B, .oam = &sOam_32x16, .anims = sAnims_Frames,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static void LoadGfx(void)
{
    u32 x, y;
    static const struct SpriteSheet sheets[] =
    {
        { sTab_Gfx, 32 * 16 / 2 * 11, TAG_Q_TAB },
        { sTagsA_Gfx, 32 * 16 / 2 * 3, TAG_Q_TAGS_A },
        { sTagsB_Gfx, 32 * 16 / 2 * 2, TAG_Q_TAGS_B },
        {}
    };
    static const struct SpritePalette pals[] =
    {
        { sQuestsBg_Pal, TAG_Q_KIT },
        { sTagsA_Pal, TAG_Q_TAGS_A },
        { sTagsB_Pal, TAG_Q_TAGS_B },
        {}
    };

    DecompressAndCopyTileDataToVram(2, sQuestsBg_Gfx, 0, 0, 0);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            sQ->bg3Tilemap[y * 32 + x] = (QUESTS_BG_TILES + (x & 1) + (y & 1) * 2) | (2 << 12);
    LoadPalette(sQuestsBg_Pal, BG_PLTT_ID(0), 3 * PLTT_SIZE_4BPP);
    LoadSpriteSheets(sheets);
    LoadSpritePalettes(pals);
    LoadMonIconPalettes();
}

static void CB2_SetupQuests(void)
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
        SetBgTilemapBuffer(2, sQ->bg2Tilemap);
        SetBgTilemapBuffer(3, sQ->bg3Tilemap);
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
        for (i = 0; i < ROWS; i++)
            sQ->tagSpriteIds[i] = MAX_SPRITES;
        sQ->iconSpriteId = MAX_SPRITES;
        sQ->tabSpriteId = CreateSprite(&sTemplate_Tab, 0, 18 + 8, 0);
        for (i = 0; i < 4; i++)
            PutWindowTilemap(i);
        Redraw(TRUE);
        ScheduleBgCopyTilemapToVram(0);
        ScheduleBgCopyTilemapToVram(3);
        gMain.state++;
        break;
    case 4:
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
        ShowBg(0);
        ShowBg(2);
        ShowBg(3);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB_Quests);
        SetMainCallback2(CB2_Quests);
        CreateTask(Task_Quests, 0);
        break;
    }
}

// ---------------------------------------------------------------- sprites
static void DestroyIcon(void)
{
    if (sQ->iconSpriteId == MAX_SPRITES)
        return;
    if (sQ->iconType == PKMN)
    {
        FreeAndDestroyMonIconSprite(&gSprites[sQ->iconSpriteId]);
    }
    else
    {
        DestroySprite(&gSprites[sQ->iconSpriteId]);
        if (sQ->iconType == ITEM)
        {
            FreeSpriteTilesByTag(TAG_Q_ITEM);
            FreeSpritePaletteByTag(TAG_Q_ITEM);
        }
    }
    sQ->iconSpriteId = MAX_SPRITES;
}

// the quest's sprite in the tray's icon well (PSF spritetype: object / item / Pokémon icon)
static void CreateIcon(u16 sprite, u8 type)
{
    DestroyIcon();
    sQ->iconType = type;
    switch (type)
    {
    case OBJECT:
        sQ->iconSpriteId = CreateObjectGraphicsSprite(sprite, SpriteCallbackDummy, WELL_X, WELL_Y - 4, 0);
        break;
    case ITEM:
        sQ->iconSpriteId = AddItemIconSprite(TAG_Q_ITEM, TAG_Q_ITEM, sprite);
        if (sQ->iconSpriteId != MAX_SPRITES)
        {
            gSprites[sQ->iconSpriteId].x = WELL_X;
            gSprites[sQ->iconSpriteId].y = WELL_Y;
        }
        break;
    case PKMN:
        sQ->iconSpriteId = CreateMonIcon(sprite, SpriteCallbackDummy, WELL_X, WELL_Y - 4, 0, 0);   // PSF's extra arg dropped
        break;
    default:
        sQ->iconSpriteId = MAX_SPRITES;
        break;
    }
    if (sQ->iconSpriteId != MAX_SPRITES)
        gSprites[sQ->iconSpriteId].oam.priority = 1;
}

static void SetTag(u32 row, s32 state)
{
    const struct SpriteTemplate *tmpl;
    u32 frame;

    if (sQ->tagSpriteIds[row] != MAX_SPRITES)
    {
        DestroySprite(&gSprites[sQ->tagSpriteIds[row]]);
        sQ->tagSpriteIds[row] = MAX_SPRITES;
    }
    if (state < 0)
        return;
    tmpl = state <= STATE_REWARD ? &sTemplate_TagA : &sTemplate_TagB;
    frame = state <= STATE_REWARD ? state : state - STATE_DONE;
    sQ->tagSpriteIds[row] = CreateSprite(tmpl, PILL_X + PILL_W - 22 + 16, ROW_Y + row * ROW_H + 1 + 8, 0);
    if (sQ->tagSpriteIds[row] != MAX_SPRITES)
        StartSpriteAnim(&gSprites[sQ->tagSpriteIds[row]], frame);
}

// ---------------------------------------------------------------- drawing
static void PrintHeader(void)
{
    const u8 *title;
    u32 a, b;

    FillWindowPixelBuffer(WIN_TITLE, PIXEL_FILL(0));
    if (IsResearch() && !sQ->steps)
    {
        // Research Rank: 5 stars (lit up to the rank) + research points
        u32 rank = Research_GetRank(), k, x;
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, 23, 0, 0, 0, sColors_Title, TEXT_SKIP_DRAW, COMPOUND_STRING("QUESTS"));
        ConvertIntToDecimalStringN(gStringVar1, Research_GetRP(), STR_CONV_MODE_LEFT_ALIGN, 4);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1} RP"));
        x = 236 - GetStringWidth(FONT_NARROW, gStringVar4, 0);
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NARROW, x, 0, 0, 0, sColors_Title, TEXT_SKIP_DRAW, gStringVar4);
        for (k = 0; k < 5; k++)
            BlitBitmapRectToWindow(WIN_TITLE, sGlyphs_Gfx, k <= rank ? 32 : 48, 0, 64, 16, x - 12 - (4 - k) * 10, 3, 9, 9);
        CopyWindowToVram(WIN_TITLE, COPYWIN_GFX);
        return;
    }
    if (sQ->steps && IsResearch())
    {
        title = Research_GetTask(sQ->parent)->name;
        a = sQ->rDone[sQ->parent];
        b = sQ->rTotal[sQ->parent];
    }
    else if (sQ->steps)
    {
        title = gSideQuests[sQ->parent].name;
        a = StepsDone(sQ->parent);
        b = gSideQuests[sQ->parent].numSubquests;
    }
    else
    {
        title = COMPOUND_STRING("QUESTS");
        a = Quests_CountInState(FLAG_GET_COMPLETED);
        b = Quests_CountInState(FLAG_GET_UNLOCKED);     // unlocked only: the total stays a surprise
    }
    AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, 23, 0, 0, 0, sColors_Title, TEXT_SKIP_DRAW, title);
    if (sQ->alpha && !sQ->steps)
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NARROW, 23 + GetStringWidth(FONT_NORMAL, title, 0) + 4, 0, 0, 0,
                                     sColors_Title, TEXT_SKIP_DRAW, COMPOUND_STRING("A-Z"));
    ConvertIntToDecimalStringN(gStringVar1, a, STR_CONV_MODE_LEFT_ALIGN, 3);
    ConvertIntToDecimalStringN(gStringVar2, b, STR_CONV_MODE_LEFT_ALIGN, 3);
    StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("{STR_VAR_1}/{STR_VAR_2}"));
    AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, 236 - GetStringWidth(FONT_NORMAL, gStringVar4, 0), 0, 0, 0,
                                 sColors_Title, TEXT_SKIP_DRAW, gStringVar4);
    CopyWindowToVram(WIN_TITLE, COPYWIN_GFX);
}

// list: the filter label ("All (6)"); steps: "Back" and the segmented progress fill (leaf palette)
static void PrintBar(void)
{
    FillWindowPixelBuffer(WIN_BAR, PIXEL_FILL(0));
    if (!sQ->steps)
    {
        ConvertIntToDecimalStringN(gStringVar1, CountFilter(sQ->filter), STR_CONV_MODE_LEFT_ALIGN, 3);
        StringCopy(gStringVar4, sFilterNames[sQ->filter]);
        StringAppend(gStringVar4, COMPOUND_STRING(" ("));
        StringAppend(gStringVar4, gStringVar1);
        StringAppend(gStringVar4, COMPOUND_STRING(")"));
        AddTextPrinterParameterized4(WIN_BAR, FONT_NARROW, 174, 17 - 16, 0, 0, sColors_Label, TEXT_SKIP_DRAW, gStringVar4);
    }
    else
    {
        u32 n = gSideQuests[sQ->parent].numSubquests, done = StepsDone(sQ->parent), k;
        if (IsResearch())
        {
            n = sQ->rTotal[sQ->parent] ? sQ->rTotal[sQ->parent] : 1;
            done = sQ->rDone[sQ->parent];
        }
        AddTextPrinterParameterized4(WIN_BAR, FONT_NARROW, 16, 17 - 16, 0, 0, sColors_Label, TEXT_SKIP_DRAW, COMPOUND_STRING("Back"));
        if (done > 0)
            PhoneUI_RoundBox(WIN_BAR, 54, 21 - 16, (180 * done + n / 2) / n, 8, 2,
                             KIT_ACCENT, KIT_INK, KIT_ACCENT_LIGHT, KIT_ACCENT_DARK, TRUE);
        for (k = 1; k < n; k++)
            FillWindowPixelRect(WIN_BAR, PIXEL_FILL(KIT_INK_SOFT), 54 + (180 * k + n / 2) / n, 21 - 16, 1, 8);
    }
    CopyWindowToVram(WIN_BAR, COPYWIN_GFX);
    gSprites[sQ->tabSpriteId].invisible = sQ->steps;
    if (Research_IsUnlocked())
    {
        gSprites[sQ->tabSpriteId].x = QUESTS_TAB6_X0 + sQ->filter * QUESTS_TAB6_PITCH + 16;
        StartSpriteAnim(&gSprites[sQ->tabSpriteId], FILTER_RESEARCH + sQ->filter);
    }
    else
    {
        gSprites[sQ->tabSpriteId].x = 22 + sQ->filter * 26 + 16;
        StartSpriteAnim(&gSprites[sQ->tabSpriteId], sQ->filter);
    }
}

static void PrintRow(u32 r)
{
    u32 i = sQ->top + r, y = ROW_Y + r * ROW_H - 32, state;
    bool32 sel = (i == sQ->cursor);
    const u8 *name;
    s32 total = -1, done = 0;

    FillWindowPixelRect(WIN_ROWS, PIXEL_FILL(0), 0, y, PILL_W + 2, ROW_H);
    if (i >= sQ->count)
    {
        SetTag(r, -1);
        return;
    }
    if (sel)
        PhoneUI_RoundBox(WIN_ROWS, 0, y, PILL_W, 14, 4, KIT_SELECT, KIT_INK, KIT_SELECT_LIGHT, KIT_SELECT_DARK, TRUE);
    else
        PhoneUI_RoundBox(WIN_ROWS, 0, y, PILL_W, 14, 4, KIT_PANEL, KIT_INK, KIT_WHITE, KIT_PANEL_SHADE, TRUE);

    if (sQ->steps && IsResearch())
    {
        u32 k = sQ->list[i];
        state = sQ->stepState[k];
        GetMapName(gStringVar3, sQ->steps6[k], 0);
        name = gStringVar3;
        total = sQ->stepTotal[k];
        done = sQ->stepDone[k];
    }
    else if (IsResearch())
    {
        u32 id = sQ->list[i];
        state = sQ->rState[id];
        name = Research_GetTask(id)->name;
        if (Research_GetTask(id)->type != RESEARCH_REQUEST && state != STATE_NEW)
        {
            total = sQ->rTotal[id];
            done = sQ->rDone[id];
        }
    }
    else if (sQ->steps)
    {
        const struct SubQuest *sub = &gSideQuests[sQ->parent].subquests[sQ->list[i]];
        state = StepState(sQ->parent, sQ->list[i]);
        name = state == STATE_LOCKED ? sText_Unknown : sub->name;
    }
    else
    {
        u32 q = sQ->list[i];
        state = QuestState(q);
        name = gSideQuests[q].name;
        if (IsFavorite(q))
            BlitBitmapRectToWindow(WIN_ROWS, sGlyphs_Gfx, 32, 0, 64, 16, 4, y + 2, 9, 9);
        if (gSideQuests[q].numSubquests != 0 && state != STATE_NEW)
        {
            total = gSideQuests[q].numSubquests;
            done = StepsDone(q);
        }
    }
    AddTextPrinterParameterized4(WIN_ROWS, FONT_NORMAL, 16, y - 1, 0, 0,
                                 state == STATE_LOCKED ? (sel ? sColors_SoftSel : sColors_Soft) : (sel ? sColors_InkSel : sColors_Ink),
                                 TEXT_SKIP_DRAW, name);
    if (total >= 0)
    {
        u8 *p = ConvertIntToDecimalStringN(gStringVar1, done, STR_CONV_MODE_LEFT_ALIGN, 2);
        *p++ = CHAR_SLASH;
        ConvertIntToDecimalStringN(p, total, STR_CONV_MODE_LEFT_ALIGN, 2);
        AddTextPrinterParameterized4(WIN_ROWS, FONT_SMALL, PILL_W - 26 - GetStringWidth(FONT_SMALL, gStringVar1, 0), y - 1, 0, 0,
                                     sel ? sColors_InkSel : sColors_Ink, TEXT_SKIP_DRAW, gStringVar1);
    }
    SetTag(r, state);
}

static void DrawScroll(void)
{
    s32 trackH = ROWS * ROW_H - 3 - 2, h, y = 0;
    bool32 show = sQ->count > ROWS;

    // the track is BG art (cols 28-29), blanked by Redraw when everything fits
    FillWindowPixelRect(WIN_ROWS, PIXEL_FILL(0), 230 - 8, 0, 7, 10 * 8);
    if (!show)
        return;
    h = trackH * ROWS / sQ->count;
    if (h < 6)
        h = 6;
    y = (trackH - h) * sQ->top / (sQ->count - ROWS);
    PhoneUI_RoundBox(WIN_ROWS, 231 - 8, ROW_Y + 1 - 32 + y, 5, h, 1, KIT_SELECT, KIT_INK, KIT_SELECT_LIGHT, KIT_SELECT_DARK, TRUE);
}

static EWRAM_DATA u8 sTrayText[64] = {0};
static EWRAM_DATA u8 sTrayRight[24] = {0};
static EWRAM_DATA u8 sTrayMap[24] = {0};

static void PrintTray(void)
{
    const u8 *map = NULL, *text = NULL, *right = NULL;
    u16 sprite = 0;
    u8 type = 0;
    bool32 stepsHint = FALSE, sendHint = FALSE;

    FillWindowPixelBuffer(WIN_TRAY, PIXEL_FILL(0));
    if (sQ->count == 0)
    {
        DestroyIcon();
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NORMAL, 47, 130 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW,
                                     COMPOUND_STRING("Nothing here yet, bzzt!"));
        CopyWindowToVram(WIN_TRAY, COPYWIN_GFX);
        return;
    }
    if (sQ->steps && IsResearch())
    {
        u32 k = sQ->list[sQ->cursor];
        mapsec_u16_t sec = sQ->steps6[k];
        const struct ResearchTask *task = Research_GetTask(sQ->parent);
        ConvertIntToDecimalStringN(gStringVar1, sQ->stepTotal[k], STR_CONV_MODE_LEFT_ALIGN, 3);
        ConvertIntToDecimalStringN(gStringVar3, sQ->stepDone[k], STR_CONV_MODE_LEFT_ALIGN, 3);
        StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("Catalogue all {STR_VAR_1} species,\nday and night: {STR_VAR_3} done."));
        StringCopy(sTrayText, gStringVar4);
        text = sTrayText;
        sprite = task->sprite;
        type = task->spriteType;
        ConvertIntToDecimalStringN(gStringVar1, sQ->cursor + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        ConvertIntToDecimalStringN(gStringVar3, sQ->count, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringCopy(gStringVar2, gStringVar3);
        StringExpandPlaceholders(sTrayRight, COMPOUND_STRING("Step {STR_VAR_1} of {STR_VAR_2}"));
        right = sTrayRight;
        map = sTrayMap;
        GetMapName(sTrayMap, sec, 0);
    }
    else if (IsResearch())
    {
        u32 id = sQ->list[sQ->cursor], st = sQ->rState[id];
        const struct ResearchTask *task = Research_GetTask(id);
        map = Research_GetLocationName(id, sTrayMap);
        sprite = task->sprite;
        type = task->spriteType;
        stepsHint = task->type == RESEARCH_SURVEY && st != STATE_NEW;
        if (st == STATE_REWARD)
        {
            text = COMPOUND_STRING("Send your notes to Palm\nto claim the reward.");
            right = COMPOUND_STRING("Send to Palm");
            sendHint = TRUE;
            stepsHint = FALSE;
        }
        else if (st == STATE_DONE)
        {
            text = COMPOUND_STRING("Filed in Palm's notes.\nThank you!");
        }
        else
        {
            text = task->desc;
            ConvertIntToDecimalStringN(gStringVar1, task->rp, STR_CONV_MODE_LEFT_ALIGN, 3);
            StringExpandPlaceholders(sTrayRight, COMPOUND_STRING("+{STR_VAR_1} RP"));
            if (!stepsHint)
                right = sTrayRight;
        }
    }
    else if (sQ->steps)
    {
        u32 i = sQ->list[sQ->cursor], st = StepState(sQ->parent, i);
        const struct SubQuest *sub = &gSideQuests[sQ->parent].subquests[i];
        map = st == STATE_LOCKED ? gText_ThreeQuestionMarks : sub->map;
        text = st == STATE_LOCKED ? NULL : sub->desc;
        sprite = gSideQuests[sQ->parent].sprite;
        type = gSideQuests[sQ->parent].spritetype;
        ConvertIntToDecimalStringN(gStringVar1, sQ->cursor + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
        ConvertIntToDecimalStringN(gStringVar2, sQ->count, STR_CONV_MODE_LEFT_ALIGN, 2);
        StringExpandPlaceholders(gStringVar3, COMPOUND_STRING("Step {STR_VAR_1} of {STR_VAR_2}"));
        right = gStringVar3;
    }
    else
    {
        u32 q = sQ->list[sQ->cursor];
        const struct SideQuest *quest = &gSideQuests[q];
        map = quest->map;
        sprite = quest->sprite;
        type = quest->spritetype;
        stepsHint = HasSteps(q);
        switch (QuestState(q))
        {
        case STATE_NEW:
            if (quest->newdesc != NULL)
                text = quest->newdesc;
            else
            {
                StringCopy(gStringVar2, quest->map);
                StringExpandPlaceholders(gStringVar3, COMPOUND_STRING("Talk to someone in\n{STR_VAR_2} to begin."));
                text = gStringVar3;
            }
            break;
        case STATE_ACTIVE:
            text = quest->desc;
            break;
        case STATE_REWARD:
            StringCopy(gStringVar2, quest->map);
            StringExpandPlaceholders(gStringVar3, COMPOUND_STRING("Return to {STR_VAR_2}\nto receive your reward!"));
            text = gStringVar3;
            break;
        default:
            text = quest->donedesc;
            break;
        }
    }
    // location pill (pin cap) sized to the name
    {
        u32 w = GetStringWidth(FONT_NARROW, map, 0);
        PhoneUI_RoundBox(WIN_TRAY, 46, 119 - 112, 10 + 16 + w, 14, 4, KIT_PANEL, KIT_INK, KIT_WHITE, KIT_PANEL_SHADE, TRUE);
        BlitBitmapRectToWindow(WIN_TRAY, sGlyphs_Gfx, 0, 0, 64, 16, 46, 119 - 112, 17, 14);
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 46 + 16 + 4, 118 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, map);
    }
    if (stepsHint)
    {
        const u8 *s = COMPOUND_STRING("Steps");
        u32 w = GetStringWidth(FONT_NARROW, s, 0);
        BlitBitmapRectToWindow(WIN_TRAY, sGlyphs_Gfx, 24, 0, 64, 16, 236 - w - 12, 122 - 112, 8, 8);
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 236 - w, 118 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, s);
    }
    else if (sendHint)
    {
        u32 w = GetStringWidth(FONT_NARROW, right, 0);
        BlitBitmapRectToWindow(WIN_TRAY, sGlyphs_Gfx, 24, 0, 64, 16, 236 - w - 12, 122 - 112, 8, 8);
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 236 - w, 118 - 112, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, right);
    }
    else if (right != NULL)
    {
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NARROW, 236 - GetStringWidth(FONT_NARROW, right, 0), 118 - 112, 0, 0,
                                     sColors_Soft, TEXT_SKIP_DRAW, right);
    }
    if (text != NULL)
    {
        u8 *nl;
        StringCopy(gStringVar4, text);
        for (nl = gStringVar4; *nl != EOS && *nl != CHAR_NEWLINE; nl++)
            ;
        if (*nl == CHAR_NEWLINE)
        {
            *nl = EOS;
            AddTextPrinterParameterized4(WIN_TRAY, FONT_NORMAL, 47, 130 - 112 + 14, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, nl + 1);
        }
        AddTextPrinterParameterized4(WIN_TRAY, FONT_NORMAL, 47, 130 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, gStringVar4);
    }
    CopyWindowToVram(WIN_TRAY, COPYWIN_GFX);
    CreateIcon(sprite, type);
}

static void Redraw(bool32 rebuild)
{
    u32 r;

    if (rebuild)
    {
        BuildList();
        if (sQ->cursor >= sQ->count)
            sQ->cursor = sQ->count ? sQ->count - 1 : 0;
        if (sQ->top > sQ->cursor)
            sQ->top = sQ->cursor;
        DecompressDataWithHeaderWram(sQ->steps ? sQuestsSteps_Tilemap
                                     : (Research_IsUnlocked() ? sQuestsList6_Tilemap : sQuestsList_Tilemap), sQ->bg2Tilemap);
        if (sQ->count <= ROWS)  // scrollbar hidden when everything fits
            for (r = 4; r <= 13; r++)
                sQ->bg2Tilemap[r * 32 + 28] = sQ->bg2Tilemap[r * 32 + 29] = 0;
        ScheduleBgCopyTilemapToVram(2);
        PrintHeader();
        PrintBar();
    }
    for (r = 0; r < ROWS; r++)
        PrintRow(r);
    DrawScroll();
    CopyWindowToVram(WIN_ROWS, COPYWIN_GFX);
    PrintTray();
}

// ---------------------------------------------------------------- research claim pop-ups (drawn over the rows)
static void ShowPopup(u32 kind, u32 taskId)
{
    const struct ResearchTask *t = Research_GetTask(taskId);
    const u8 *title, *l1 = NULL, *l2 = NULL, *l3 = NULL;
    u8 line1[48], line2[48];
    u32 r, y0 = 4, w = 196, x0 = (PILL_W - w) / 2;

    sQ->popup = kind;
    for (r = 0; r < ROWS; r++)
        SetTag(r, -1);
    FillWindowPixelBuffer(WIN_ROWS, PIXEL_FILL(0));
    switch (kind)
    {
    case POPUP_CLAIM:
        title = COMPOUND_STRING("FIELD NOTES");
        CopyItemNameHandlePlural(t->rewardItem, gStringVar2, t->rewardQty);
        ConvertIntToDecimalStringN(gStringVar1, t->rewardQty, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringExpandPlaceholders(line1, COMPOUND_STRING("Palm sent {STR_VAR_1} {STR_VAR_2}"));
        ConvertIntToDecimalStringN(gStringVar1, t->rp, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringExpandPlaceholders(line2, COMPOUND_STRING("and {STR_VAR_1} research points!"));
        l1 = line1;
        l2 = line2;
        l3 = t->name;
        break;
    case POPUP_RANK:
        title = COMPOUND_STRING("RANK UP");
        l1 = Research_GetRankName(Research_GetRank());
        CopyItemName(Research_GetRankGift(Research_GetRank()), gStringVar2);
        StringExpandPlaceholders(line2, COMPOUND_STRING("Palm sent you {STR_VAR_2}!"));
        l2 = line2;
        l3 = COMPOUND_STRING("“The habitat data is amazing!”");
        break;
    default:
        title = COMPOUND_STRING("FIELD NOTES");
        l1 = COMPOUND_STRING("Your Bag is full!");
        l2 = COMPOUND_STRING("Make room, then send");
        l3 = COMPOUND_STRING("your notes again.");
        break;
    }
    PhoneUI_RoundBox(WIN_ROWS, x0, y0 + 6, w, 66, 4, KIT_PANEL, KIT_INK, KIT_WHITE, KIT_PANEL_SHADE, TRUE);
    PhoneUI_RoundBox(WIN_ROWS, x0 + 6, y0, GetStringWidth(FONT_NORMAL, title, 0) + 14, 14, 4,
                     kind == POPUP_RANK ? KIT_SELECT : KIT_ACCENT, KIT_INK,
                     kind == POPUP_RANK ? KIT_SELECT_LIGHT : KIT_ACCENT_LIGHT,
                     kind == POPUP_RANK ? KIT_SELECT_DARK : KIT_ACCENT_DARK, TRUE);
    AddTextPrinterParameterized4(WIN_ROWS, FONT_NORMAL, x0 + 13, y0 - 1, 0, 0,
                                 kind == POPUP_RANK ? sColors_InkSel : sColors_Title, TEXT_SKIP_DRAW, title);
    if (kind == POPUP_RANK)
    {
        u32 k, rank = Research_GetRank();
        for (k = 0; k < 5; k++)
            BlitBitmapRectToWindow(WIN_ROWS, sGlyphs_Gfx, k <= rank ? 32 : 48, 0, 64, 16, x0 + 70 + k * 12, y0 + 17, 9, 9);
        AddTextPrinterParameterized4(WIN_ROWS, FONT_NORMAL, x0 + (w - GetStringWidth(FONT_NORMAL, l1, 0)) / 2, y0 + 27, 0, 0,
                                     sColors_Ink, TEXT_SKIP_DRAW, l1);
        AddTextPrinterParameterized4(WIN_ROWS, FONT_NARROW, x0 + 10, y0 + 43, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, l2);
        AddTextPrinterParameterized4(WIN_ROWS, FONT_NARROW, x0 + 10, y0 + 55, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, l3);
    }
    else
    {
        AddTextPrinterParameterized4(WIN_ROWS, FONT_NORMAL, x0 + 10, y0 + 15, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, l1);
        AddTextPrinterParameterized4(WIN_ROWS, FONT_NORMAL, x0 + 10, y0 + 31, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, l2);
        AddTextPrinterParameterized4(WIN_ROWS, FONT_NARROW, x0 + 10, y0 + 49, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, l3);
    }
    CopyWindowToVram(WIN_ROWS, COPYWIN_GFX);
}

static void TryClaim(void)
{
    u32 id = sQ->list[sQ->cursor];

    sQ->popupTask = id;
    sQ->popupOldRank = Research_GetRank();
    if (Research_Claim(id))
    {
        PlaySE(SE_EXP_MAX);
        ShowPopup(POPUP_CLAIM, id);
    }
    else
    {
        PlaySE(SE_FAILURE);
        ShowPopup(POPUP_BAG_FULL, id);
    }
}

// A / B on a pop-up: claim -> rank up (if the RP crossed a rank) -> back to the list
static void AdvancePopup(void)
{
    PlaySE(SE_SELECT);
    if (sQ->popup == POPUP_CLAIM && Research_GetRank() != sQ->popupOldRank)
    {
        ShowPopup(POPUP_RANK, sQ->popupTask);
        return;
    }
    sQ->popup = POPUP_NONE;
    Redraw(TRUE);
}

// ---------------------------------------------------------------- input
static void MoveCursor(s32 delta)
{
    s32 next = sQ->cursor + delta;
    if (next < 0 || next >= sQ->count)
        return;
    PlaySE(SE_SELECT);
    sQ->cursor = next;
    if (sQ->cursor < sQ->top)
        sQ->top = sQ->cursor;
    else if (sQ->cursor >= sQ->top + ROWS)
        sQ->top = sQ->cursor - ROWS + 1;
    Redraw(FALSE);
}

static void Task_Quests(u8 taskId)
{
    u32 i;

    if (gPaletteFade.active)
        return;
    if (sQ->exiting)
    {
        MainCallback cb = sQ->exitCallback;
        DestroyIcon();
        sSavedFilter = sQ->filter;
        sSavedAlpha = sQ->alpha;
        DestroyTask(taskId);
        FreeAllWindowBuffers();
        FREE_AND_SET_NULL(sQ);
        SetMainCallback2(cb);
        return;
    }
    if (sQ->popup != POPUP_NONE)
    {
        if (JOY_NEW(A_BUTTON | B_BUTTON))
            AdvancePopup();
        return;
    }
    if (JOY_REPEAT(DPAD_UP))
    {
        MoveCursor(-1);
    }
    else if (JOY_REPEAT(DPAD_DOWN))
    {
        MoveCursor(1);
    }
    else if (sQ->steps)
    {
        if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sQ->steps = FALSE;
            sQ->cursor = sQ->listCursor;
            sQ->top = sQ->listTop;
            Redraw(TRUE);
        }
    }
    else if (JOY_NEW(L_BUTTON | R_BUTTON))
    {
        PlaySE(SE_SELECT);
        sQ->filter = (sQ->filter + (JOY_NEW(R_BUTTON) ? 1 : NumFilters() - 1)) % NumFilters();
        sQ->cursor = sQ->top = 0;
        Redraw(TRUE);
    }
    else if (JOY_NEW(START_BUTTON) && !IsResearch())
    {
        PlaySE(SE_SELECT);
        sQ->alpha ^= 1;
        sQ->cursor = sQ->top = 0;
        Redraw(TRUE);
    }
    else if (JOY_NEW(SELECT_BUTTON) && sQ->count != 0 && !IsResearch())
    {
        u8 q = sQ->list[sQ->cursor];
        PlaySE(SE_SELECT);
        QuestMenu_GetSetQuestState(q, IsFavorite(q) ? FLAG_REMOVE_FAVORITE : FLAG_SET_FAVORITE);
        Redraw(TRUE);
        for (i = 0; i < sQ->count; i++)     // keep the cursor on the same quest
        {
            if (sQ->list[i] == q)
            {
                sQ->cursor = i;
                if (sQ->cursor < sQ->top)
                    sQ->top = sQ->cursor;
                else if (sQ->cursor >= sQ->top + ROWS)
                    sQ->top = sQ->cursor - ROWS + 1;
            }
        }
        Redraw(FALSE);
    }
    else if (JOY_NEW(A_BUTTON) && sQ->count != 0 && IsResearch() && !sQ->steps
          && sQ->rState[sQ->list[sQ->cursor]] == RESEARCH_ST_REWARD)
    {
        TryClaim();
    }
    else if (JOY_NEW(A_BUTTON) && sQ->count != 0 && IsResearch() && !sQ->steps
          && Research_GetTask(sQ->list[sQ->cursor])->type == RESEARCH_SURVEY)
    {
        PlaySE(SE_SELECT);
        sQ->listCursor = sQ->cursor;
        sQ->listTop = sQ->top;
        sQ->parent = sQ->list[sQ->cursor];
        sQ->steps = TRUE;
        sQ->cursor = sQ->top = 0;
        Redraw(TRUE);
    }
    else if (JOY_NEW(A_BUTTON) && sQ->count != 0 && !IsResearch() && HasSteps(sQ->list[sQ->cursor]))
    {
        PlaySE(SE_SELECT);
        sQ->listCursor = sQ->cursor;
        sQ->listTop = sQ->top;
        sQ->parent = sQ->list[sQ->cursor];
        sQ->steps = TRUE;
        sQ->cursor = sQ->top = 0;
        Redraw(TRUE);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        sQ->exiting = TRUE;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
}
