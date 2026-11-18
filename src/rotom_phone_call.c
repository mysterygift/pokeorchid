// Rotom Phone CALL app (mock_call.py, approved 2026-11-17): contact list, contact card, ringing, talking.
// Uses the PokéNav match-call data and logic unchanged (pokenav_match_call_data.c, match_call.c, the
// gMatchCallMessages / flavor texts); only the screens are new, drawn with the Orchid kit.
//
// Layers: BG3 grid, BG2 static art (export_call.py), BG1 card button chips / ringing rings,
// BG0 text windows. OBJ: gold selection pills, contact heads + tags, trainer portrait.
#include "global.h"
#include "rotom_phone.h"
#include "battle_setup.h"
#include "bg.h"
#include "data.h"
#include "decompress.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "gpu_regs.h"
#include "main.h"
#include "malloc.h"
#include "match_call.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "phone_ui.h"
#include "pokenav.h"
#include "region_map.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "strings.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "constants/event_objects.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "constants/trainers.h"
#include "data/rotom_phone_call_layout.h"

extern const u8 *const gMatchCallFlavorTexts[REMATCH_TABLE_ENTRIES][CHECK_PAGE_ENTRY_COUNT];

static const u32 sCallBg_Gfx[] = INCGFX_U32("graphics/rotom_phone/call_bg.png", ".4bpp.smol");
static const u32 sCallList_Tilemap[] = INCGFX_U32("graphics/rotom_phone/call_list.bin", ".smolTM");
static const u32 sCallCard_Tilemap[] = INCGFX_U32("graphics/rotom_phone/call_card.bin", ".smolTM");
static const u32 sCallCardStrip_Tilemap[] = INCGFX_U32("graphics/rotom_phone/call_card_strip.bin", ".smolTM");
static const u32 sCallChips_Tilemap[] = INCGFX_U32("graphics/rotom_phone/call_chips.bin", ".smolTM");
static const u32 sCallRing_Tilemap[] = INCGFX_U32("graphics/rotom_phone/call_ring.bin", ".smolTM");
static const u16 sCallBg_Pal[] = INCGFX_U16("graphics/rotom_phone/call_bg.pal", ".gbapal");
static const u8 sRowPill_Gfx[] = INCGFX_U8("graphics/rotom_phone/call_row_pill.png", ".4bpp");
static const u8 sBtnPill_Gfx[] = INCGFX_U8("graphics/rotom_phone/call_btn_pill.png", ".4bpp");
static const u8 sTags_Gfx[] = INCGFX_U8("graphics/rotom_phone/call_tags.png", ".4bpp");
static const u16 sTags_Pal[] = INCGFX_U16("graphics/rotom_phone/call_tags.pal", ".gbapal");
static const u8 sGlyphs_Gfx[] = INCGFX_U8("graphics/rotom_phone/call_glyphs.png", ".4bpp");

#define TAG_CALL_KIT        0x7B00      // OBJ copy of the kit palette (pills)
#define TAG_CALL_ROW_PILL   0x7B01
#define TAG_CALL_BTN_PILL   0x7B02
#define TAG_CALL_TAGS       0x7B03
#define TAG_CALL_HEAD       0x7B10      // + row (0-4), + 5 = big head on the card / ringing
#define TAG_CALL_PORTRAIT   0x7B20
#define TAG_CALL_PORTRAIT_PAL 0x7B21

#define ROWS        5
#define ROW_Y       20
#define ROW_H       18
#define MAX_CONTACTS (MC_HEADER_COUNT + REMATCH_TABLE_ENTRIES)
#define RING_CX     120
#define RING_CY     58
#define RING_FRAMES 100

// rematch dark / home dark (mock_call.py TAG), for the tray status line
#define KIT_TAG_REMATCH KIT_SPARE_A
#define KIT_TAG_HOME    KIT_SPARE_B
static const u16 sTagTextColours[] = { RGB(19, 5, 9), RGB(5, 13, 8) };

enum { SCREEN_LIST, SCREEN_CARD, SCREEN_RING, SCREEN_TALK };
enum { TAG_NONE_, TAG_REMATCH, TAG_HOME };

enum
{
    WIN_TITLE,
    WIN_A,      // list rows / card info / ringing name
    WIN_B,      // list tray / card buttons + hint / ringing hint
    WIN_RINGS,  // BG1, ringing only
    WIN_COUNT
};

static const struct WindowTemplate sTitleWindow[] =
{
    { .bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 2, .paletteNum = 0, .baseBlock = 1 },
    DUMMY_WIN_TEMPLATE
};
// per screen: WIN_A, WIN_B (BG0, tiles 61+; the dialogue frame owns 0x200-0x22F)
static const struct WindowTemplate sScreenWindows[][2] =
{
    [SCREEN_LIST] = {
        { .bg = 0, .tilemapLeft = 1, .tilemapTop = 2, .width = 29, .height = 12, .paletteNum = 0, .baseBlock = 61 },
        { .bg = 0, .tilemapLeft = 0, .tilemapTop = 14, .width = 30, .height = 6, .paletteNum = 0, .baseBlock = 0x240 },
    },
    [SCREEN_CARD] = {
        { .bg = 0, .tilemapLeft = 10, .tilemapTop = 2, .width = 20, .height = 12, .paletteNum = 0, .baseBlock = 61 },
        { .bg = 0, .tilemapLeft = 0, .tilemapTop = 14, .width = 30, .height = 6, .paletteNum = 0, .baseBlock = 0x240 },
    },
    [SCREEN_RING] = {
        { .bg = 0, .tilemapLeft = 0, .tilemapTop = 11, .width = 30, .height = 4, .paletteNum = 0, .baseBlock = 61 },
        { .bg = 0, .tilemapLeft = 0, .tilemapTop = 17, .width = 30, .height = 3, .paletteNum = 0, .baseBlock = 0x240 },
    },
    [SCREEN_TALK] = {
        { .bg = 0, .tilemapLeft = 0, .tilemapTop = 11, .width = 30, .height = 4, .paletteNum = 0, .baseBlock = 61 },
        { .bg = 0, .tilemapLeft = 2, .tilemapTop = 15, .width = 27, .height = 4, .paletteNum = DLG_WINDOW_PALETTE_NUM, .baseBlock = 0x240 },
    },
};
// rings: x 72-167, y 16-103 on BG1 (pixel (RING_CX, RING_CY) = window (48, 42))
static const struct WindowTemplate sRingWindow = { .bg = 1, .tilemapLeft = 9, .tilemapTop = 2, .width = 12, .height = 11, .paletteNum = 0, .baseBlock = 0x180 };

static const struct BgTemplate sBgTemplates[] =
{
    { .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 28, .screenSize = 0, .paletteMode = 0, .priority = 0, .baseTile = 0 },
    { .bg = 1, .charBaseIndex = 2, .mapBaseIndex = 29, .screenSize = 0, .paletteMode = 0, .priority = 1, .baseTile = 0 },
    { .bg = 2, .charBaseIndex = 2, .mapBaseIndex = 30, .screenSize = 0, .paletteMode = 0, .priority = 2, .baseTile = 0 },
    { .bg = 3, .charBaseIndex = 2, .mapBaseIndex = 31, .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0 },
};

static const u8 sColors_Title[] = {0, KIT_WHITE, KIT_ACCENT_DARK};
static const u8 sColors_Ink[] = {0, KIT_INK, KIT_PANEL_SHADE};
static const u8 sColors_InkSel[] = {0, KIT_INK, KIT_SELECT_DARK};
static const u8 sColors_Soft[] = {0, KIT_INK_SOFT, KIT_PANEL_SHADE};
static const u8 sColors_SoftSel[] = {0, KIT_INK_SOFT, KIT_SELECT_DARK};
static const u8 sColors_Calling[] = {0, KIT_WHITE, KIT_INK_SOFT};

struct PhoneCall
{
    u16 bg1Tilemap[32 * 32];
    u16 bg2Tilemap[32 * 32];
    u16 bg3Tilemap[32 * 32];
    struct PokenavMatchCallEntry contacts[MAX_CONTACTS];
    u8 headTiles[ROWS + 1][16 * 16 / 2];
    u8 portraitTiles[64 * 64 / 2];
    u8 count;
    u8 cursor;
    u8 top;
    u8 screen;
    u8 button;
    u8 state;
    u8 gridTimer;
    bool8 newRematchRequest;
    bool8 skipRing;
    u16 timer;
    u16 talkFrames;
    u8 rowPillIds[4];
    u8 btnPillIds[2];
    u8 headIds[ROWS + 1];
    u8 tagIds[ROWS];
    u8 portraitId;
    u8 dialogueWin;
    const u8 *message;
};

static EWRAM_DATA struct PhoneCall *sCall = NULL;

static void CB2_SetupCall(void);
static void CB2_Call(void);
static void VBlankCB_Call(void);
static void Task_Call(u8 taskId);
static void EnterScreen(u32 screen);

// ---------------------------------------------------------------- contacts (pokenav_match_call_list.c logic)
static void BuildContacts(void)
{
    u32 i;

    sCall->count = 0;
    for (i = 0; i < MC_HEADER_COUNT; i++)
    {
        if (MatchCall_GetEnabled(i))
        {
            sCall->contacts[sCall->count].headerId = i;
            sCall->contacts[sCall->count].isSpecialTrainer = TRUE;
            sCall->contacts[sCall->count].mapSec = MatchCall_GetMapSec(i);
            sCall->count++;
        }
    }
    for (i = 0; i < REMATCH_TABLE_ENTRIES; i++)
    {
        if (!MatchCall_HasRematchId(i) && IsRematchEntryRegistered(i))
        {
            sCall->contacts[sCall->count].headerId = i;
            sCall->contacts[sCall->count].isSpecialTrainer = FALSE;
            sCall->contacts[sCall->count].mapSec = GetMatchTableMapSectionId(i);
            sCall->count++;
        }
    }
}

u32 PhoneCall_CountContacts(void)
{
    u32 i, n = 0;
    for (i = 0; i < MC_HEADER_COUNT; i++)
        n += MatchCall_GetEnabled(i) ? 1 : 0;
    for (i = 0; i < REMATCH_TABLE_ENTRIES; i++)
        n += (!MatchCall_HasRematchId(i) && IsRematchEntryRegistered(i)) ? 1 : 0;
    return n;
}

static u32 RematchIdx(const struct PokenavMatchCallEntry *c)
{
    return c->isSpecialTrainer ? MatchCall_GetRematchTableIdx(c->headerId) : c->headerId;
}

static u32 ContactTag(const struct PokenavMatchCallEntry *c)
{
    u32 idx = RematchIdx(c);

    if (c->isSpecialTrainer && c->headerId == MC_HEADER_MOM)
        return TAG_HOME;
#if FREE_MATCH_CALL == FALSE
    if (idx != REMATCH_TABLE_ENTRIES && gSaveBlock1Ptr->trainerRematches[idx] != 0)
        return TAG_REMATCH;
#endif
    return TAG_NONE_;
}

static void ContactName(const struct PokenavMatchCallEntry *c, u8 *dest)
{
    if (!c->isSpecialTrainer)
    {
        u32 trainerId = GetTrainerIdxByRematchIdx(c->headerId);
        u8 *p = StringCopy(dest, GetTrainerClassNameFromId(trainerId));
        *p++ = CHAR_SPACE;
        StringCopy(p, GetTrainerNameFromId(trainerId));
    }
    else
    {
        const u8 *desc, *name;
        MatchCall_GetNameAndDesc(c->headerId, &desc, &name);
        StringCopy(dest, name != NULL ? name : gText_EmptyString2);
    }
}

static const u8 sText_MomProfile[] = _("Always happy to hear\nfrom you, dear!");

// two profile lines (the PokéNav check page's intro lines)
static void ContactProfile(const struct PokenavMatchCallEntry *c, u8 *dest)
{
    u32 idx = RematchIdx(c);
    const u8 *a = NULL, *b = NULL;
    u8 *p;

    if (idx != REMATCH_TABLE_ENTRIES)
    {
        a = gMatchCallFlavorTexts[idx][CHECK_PAGE_INTRO_1];
        b = gMatchCallFlavorTexts[idx][CHECK_PAGE_INTRO_2];
    }
    else if (MatchCall_HasCheckPage(c->headerId))
    {
        a = MatchCall_GetOverrideFlavorText(c->headerId, CHECK_PAGE_INTRO_1);
        b = MatchCall_GetOverrideFlavorText(c->headerId, CHECK_PAGE_INTRO_2);
    }
    else if (c->headerId == MC_HEADER_MOM)
    {
        StringCopy(dest, sText_MomProfile);
        return;
    }
    *dest = EOS;
    if (a == NULL)
        return;
    p = StringCopy(dest, a);
    if (b != NULL)
    {
        *p++ = CHAR_NEWLINE;
        StringCopy(p, b);
    }
}

static enum TrainerPicID ContactPic(const struct PokenavMatchCallEntry *c)
{
    u32 idx = RematchIdx(c);
    if (idx != REMATCH_TABLE_ENTRIES)
        return GetTrainerPicFromId(GetTrainerIdxByRematchIdx(idx));
    if (c->isSpecialTrainer && MatchCall_HasCheckPage(c->headerId))
        return gFacilityClassToPicIndex[MatchCall_GetOverrideFacilityClass(c->headerId)];
    return TRAINER_PIC_COUNT;   // none: the card shows the overworld head at 2x
}

// overworld sprite for the contact's head (the PokéNav has none; picked by person / trainer pic)
static const struct { u16 pic; u16 gfx; } sPicToOw[] =
{
    { TRAINER_PIC_HIKER, OBJ_EVENT_GFX_HIKER },
    { TRAINER_PIC_FISHERMAN, OBJ_EVENT_GFX_FISHERMAN },
    { TRAINER_PIC_LASS, OBJ_EVENT_GFX_LASS },
    { TRAINER_PIC_YOUNGSTER, OBJ_EVENT_GFX_YOUNGSTER },
    { TRAINER_PIC_PICNICKER, OBJ_EVENT_GFX_PICNICKER },
    { TRAINER_PIC_CAMPER, OBJ_EVENT_GFX_CAMPER },
    { TRAINER_PIC_BUG_CATCHER, OBJ_EVENT_GFX_BUG_CATCHER },
    { TRAINER_PIC_BEAUTY, OBJ_EVENT_GFX_BEAUTY },
    { TRAINER_PIC_BLACK_BELT, OBJ_EVENT_GFX_BLACK_BELT },
    { TRAINER_PIC_COOLTRAINER_M, OBJ_EVENT_GFX_COOLTRAINER_M },
    { TRAINER_PIC_COOLTRAINER_F, OBJ_EVENT_GFX_COOLTRAINER_F },
    { TRAINER_PIC_GENTLEMAN, OBJ_EVENT_GFX_GENTLEMAN },
    { TRAINER_PIC_EXPERT_M, OBJ_EVENT_GFX_EXPERT_M },
    { TRAINER_PIC_EXPERT_F, OBJ_EVENT_GFX_EXPERT_F },
    { TRAINER_PIC_CYCLING_TRIATHLETE_M, OBJ_EVENT_GFX_CYCLING_TRIATHLETE_M },
    { TRAINER_PIC_CYCLING_TRIATHLETE_F, OBJ_EVENT_GFX_CYCLING_TRIATHLETE_F },
    { TRAINER_PIC_LEADER_ROXANNE, OBJ_EVENT_GFX_ROXANNE },
    { TRAINER_PIC_LEADER_BRAWLY, OBJ_EVENT_GFX_BRAWLY },
    { TRAINER_PIC_LEADER_WATTSON, OBJ_EVENT_GFX_WATTSON },
    { TRAINER_PIC_LEADER_FLANNERY, OBJ_EVENT_GFX_FLANNERY },
    { TRAINER_PIC_LEADER_NORMAN, OBJ_EVENT_GFX_NORMAN },
    { TRAINER_PIC_LEADER_WINONA, OBJ_EVENT_GFX_WINONA },
    { TRAINER_PIC_LEADER_JUAN, OBJ_EVENT_GFX_JUAN },
    { TRAINER_PIC_STEVEN, OBJ_EVENT_GFX_STEVEN },
    { TRAINER_PIC_AROMA_LADY, OBJ_EVENT_GFX_WOMAN_2 },
    { TRAINER_PIC_RUIN_MANIAC, OBJ_EVENT_GFX_HIKER },
    { TRAINER_PIC_HEX_MANIAC, OBJ_EVENT_GFX_HEX_MANIAC },
    { TRAINER_PIC_POKEMANIAC, OBJ_EVENT_GFX_MANIAC },
    { TRAINER_PIC_POKEFAN_M, OBJ_EVENT_GFX_POKEFAN_M },
    { TRAINER_PIC_POKEFAN_F, OBJ_EVENT_GFX_POKEFAN_F },
    { TRAINER_PIC_POKEMON_RANGER_M, OBJ_EVENT_GFX_POKEMON_RANGER_M },
    { TRAINER_PIC_POKEMON_RANGER_F, OBJ_EVENT_GFX_POKEMON_RANGER_F },
    { TRAINER_PIC_PSYCHIC_M, OBJ_EVENT_GFX_PSYCHIC_M },
    { TRAINER_PIC_RICH_BOY, OBJ_EVENT_GFX_RICH_BOY },
    { TRAINER_PIC_SAILOR, OBJ_EVENT_GFX_SAILOR },
    { TRAINER_PIC_SCHOOL_KID_M, OBJ_EVENT_GFX_SCHOOL_KID_M },
    { TRAINER_PIC_SCHOOL_KID_F, OBJ_EVENT_GFX_SCHOOL_KID_F },
    { TRAINER_PIC_SWIMMER_M, OBJ_EVENT_GFX_SWIMMER_M_LAND },
    { TRAINER_PIC_SWIMMER_F, OBJ_EVENT_GFX_SWIMMER_F_LAND },
    { TRAINER_PIC_TUBER_M, OBJ_EVENT_GFX_TUBER_M_LAND },
    { TRAINER_PIC_TUBER_F, OBJ_EVENT_GFX_TUBER_F },
    { TRAINER_PIC_TWINS, OBJ_EVENT_GFX_TWIN },
    { TRAINER_PIC_NINJA_BOY, OBJ_EVENT_GFX_NINJA_BOY },
    { TRAINER_PIC_OLD_MAN, OBJ_EVENT_GFX_OLD_MAN },
    { TRAINER_PIC_WALLY, OBJ_EVENT_GFX_WALLY },
};

static u16 ContactOwGfx(const struct PokenavMatchCallEntry *c)
{
    u32 i;
    enum TrainerPicID pic;

    if (c->isSpecialTrainer)
    {
        switch (c->headerId)
        {
        case MC_HEADER_MOM:        return OBJ_EVENT_GFX_MOM;
        case MC_HEADER_PROF_BIRCH: return OBJ_EVENT_GFX_PROF_BIRCH;
        case MC_HEADER_BRENDAN:    return OBJ_EVENT_GFX_BRENDAN_NORMAL;
        case MC_HEADER_MAY:        return OBJ_EVENT_GFX_MAY_NORMAL;
        case MC_HEADER_WALLY:      return OBJ_EVENT_GFX_WALLY;
        case MC_HEADER_SCOTT:      return OBJ_EVENT_GFX_SCOTT;
        case MC_HEADER_MR_STONE:   return OBJ_EVENT_GFX_MAN_4;     // no Mr. Stone overworld sprite
        }
    }
    pic = ContactPic(c);
    for (i = 0; i < ARRAY_COUNT(sPicToOw); i++)
    {
        if (sPicToOw[i].pic == pic)
            return sPicToOw[i].gfx;
    }
    return OBJ_EVENT_GFX_BOY_1;
}

// ---------------------------------------------------------------- entry
void CB2_InitPhoneCall(void)
{
    sCall = AllocZeroed(sizeof(*sCall));
    gMain.state = 0;
    SetMainCallback2(CB2_SetupCall);
}

static void LoadGfx(void)
{
    u32 x, y;
    static const struct SpriteSheet sheets[] =
    {
        { sRowPill_Gfx, 64 * 32 / 2 * 4, TAG_CALL_ROW_PILL },
        { sBtnPill_Gfx, 64 * 32 / 2 * 2, TAG_CALL_BTN_PILL },
        { sTags_Gfx, 32 * 16 / 2 * 2, TAG_CALL_TAGS },
        {}
    };
    static const struct SpritePalette pals[] =
    {
        { sCallBg_Pal, TAG_CALL_KIT },
        { sTags_Pal, TAG_CALL_TAGS },
        {}
    };

    DecompressAndCopyTileDataToVram(2, sCallBg_Gfx, 0, 0, 0);
    for (y = 0; y < 32; y++)
        for (x = 0; x < 32; x++)
            sCall->bg3Tilemap[y * 32 + x] = (CALL_BG_TILES + (x & 1) + (y & 1) * 2) | (2 << 12);
    LoadPalette(sCallBg_Pal, BG_PLTT_ID(0), 3 * PLTT_SIZE_4BPP);
    LoadPalette(sTagTextColours, BG_PLTT_ID(0) + KIT_SPARE_A, sizeof(sTagTextColours));
    LoadSpriteSheets(sheets);
    LoadSpritePalettes(pals);
    LoadMessageBoxAndBorderGfx();
}

static void CB2_SetupCall(void)
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
        for (u32 bg = 0; bg < 4; bg++)
        {
            ChangeBgX(bg, 0, BG_COORD_SET);     // the phone's ticker leaves BG1 scrolled
            ChangeBgY(bg, 0, BG_COORD_SET);
        }
        SetBgTilemapBuffer(1, sCall->bg1Tilemap);
        SetBgTilemapBuffer(2, sCall->bg2Tilemap);
        SetBgTilemapBuffer(3, sCall->bg3Tilemap);
        InitWindows(sTitleWindow);
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
        u32 i;
        BuildContacts();
        for (i = 0; i < ARRAY_COUNT(sCall->headIds); i++)
            sCall->headIds[i] = MAX_SPRITES;
        for (i = 0; i < ROWS; i++)
            sCall->tagIds[i] = MAX_SPRITES;
        for (i = 0; i < 4; i++)
            sCall->rowPillIds[i] = MAX_SPRITES;
        for (i = 0; i < 2; i++)
            sCall->btnPillIds[i] = MAX_SPRITES;
        sCall->portraitId = MAX_SPRITES;
        sCall->dialogueWin = WINDOW_NONE;
        PutWindowTilemap(WIN_TITLE);
        EnterScreen(SCREEN_LIST);
        ScheduleBgCopyTilemapToVram(3);
        gMain.state++;
        break;
    }
    case 4:
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
        ShowBg(0);
        ShowBg(1);
        ShowBg(2);
        ShowBg(3);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB_Call);
        SetMainCallback2(CB2_Call);
        CreateTask(Task_Call, 0);
        break;
    }
}

static void CB2_Call(void)
{
    if ((++sCall->gridTimer & 3) == 0)
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

static void VBlankCB_Call(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

// ---------------------------------------------------------------- sprites
static const struct OamData sOam_64x32 = { .shape = SPRITE_SHAPE(64x32), .size = SPRITE_SIZE(64x32), .priority = 2 };
static const struct OamData sOam_32x16 = { .shape = SPRITE_SHAPE(32x16), .size = SPRITE_SIZE(32x16), .priority = 1 };
static const struct OamData sOam_16x16 = { .shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 1 };
static const struct OamData sOam_16x16Big = { .shape = SPRITE_SHAPE(16x16), .size = SPRITE_SIZE(16x16), .priority = 1, .affineMode = ST_OAM_AFFINE_DOUBLE };
static const struct OamData sOam_64x64 = { .shape = SPRITE_SHAPE(64x64), .size = SPRITE_SIZE(64x64), .priority = 1 };

static const union AnimCmd sAnim_F0[] = { ANIMCMD_FRAME(0, 0), ANIMCMD_END };
static const union AnimCmd sAnim_F1[] = { ANIMCMD_FRAME(32, 0), ANIMCMD_END };    // 64x32 = 32 tiles a frame
static const union AnimCmd sAnim_F2[] = { ANIMCMD_FRAME(64, 0), ANIMCMD_END };
static const union AnimCmd sAnim_F3[] = { ANIMCMD_FRAME(96, 0), ANIMCMD_END };
static const union AnimCmd *const sAnims_Pill[] = { sAnim_F0, sAnim_F1, sAnim_F2, sAnim_F3 };
static const union AnimCmd sAnim_T0[] = { ANIMCMD_FRAME(0, 0), ANIMCMD_END };
static const union AnimCmd sAnim_T1[] = { ANIMCMD_FRAME(8, 0), ANIMCMD_END };     // 32x16 = 8 tiles
static const union AnimCmd *const sAnims_Tags[] = { sAnim_T0, sAnim_T1 };
static const union AffineAnimCmd sAffine_Double[] = { AFFINEANIMCMD_FRAME(512, 512, 0, 0), AFFINEANIMCMD_END };
static const union AffineAnimCmd *const sAffines_Double[] = { sAffine_Double };

static const struct SpriteTemplate sTemplate_RowPill =
{
    .tileTag = TAG_CALL_ROW_PILL, .paletteTag = TAG_CALL_KIT, .oam = &sOam_64x32, .anims = sAnims_Pill,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_BtnPill =
{
    .tileTag = TAG_CALL_BTN_PILL, .paletteTag = TAG_CALL_KIT, .oam = &sOam_64x32, .anims = sAnims_Pill,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sTemplate_Tag =
{
    .tileTag = TAG_CALL_TAGS, .paletteTag = TAG_CALL_TAGS, .oam = &sOam_32x16, .anims = sAnims_Tags,
    .images = NULL, .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};

static void DestroySpriteIfAny(u8 *id)
{
    if (*id != MAX_SPRITES)
    {
        DestroySprite(&gSprites[*id]);
        *id = MAX_SPRITES;
    }
}

static void FreeHead(u32 slot)
{
    if (sCall->headIds[slot] != MAX_SPRITES)
    {
        u16 palTag = GetSpritePaletteTagByPaletteNum(gSprites[sCall->headIds[slot]].oam.paletteNum);
        DestroySpriteIfAny(&sCall->headIds[slot]);
        FreeSpriteTilesByTag(TAG_CALL_HEAD + slot);
        (void)palTag;   // object event palettes stay loaded (shared between heads)
    }
}

// slot 0-4 = list rows (16x16), slot ROWS = big head (2x, affine)
static void CreateHead(u32 slot, const struct PokenavMatchCallEntry *c, s16 x, s16 y)
{
    struct SpriteSheet sheet = { sCall->headTiles[slot], sizeof(sCall->headTiles[slot]), TAG_CALL_HEAD + slot };
    struct SpriteTemplate tmpl =
    {
        .tileTag = TAG_CALL_HEAD + slot, .oam = slot == ROWS ? &sOam_16x16Big : &sOam_16x16,
        .anims = gDummySpriteAnimTable, .images = NULL,
        .affineAnims = slot == ROWS ? sAffines_Double : gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
    };

    FreeHead(slot);
    tmpl.paletteTag = PhoneUI_BuildOwHead(ContactOwGfx(c), sCall->headTiles[slot]);
    LoadSpriteSheet(&sheet);
    sCall->headIds[slot] = CreateSprite(&tmpl, x, y, 0);
    if (slot == ROWS && sCall->headIds[slot] != MAX_SPRITES)
        StartSpriteAffineAnim(&gSprites[sCall->headIds[slot]], 0);
}

static void FreePortrait(void)
{
    DestroySpriteIfAny(&sCall->portraitId);
    FreeSpriteTilesByTag(TAG_CALL_PORTRAIT);
    FreeSpritePaletteByTag(TAG_CALL_PORTRAIT_PAL);
    FreeHead(ROWS);
}

// The contact's trainer front pic (card), cut to a circle for the ringing / talking screens.
static void CreatePortrait(bool32 round, s16 picX, s16 picY, s16 headX, s16 headY)
{
    const struct PokenavMatchCallEntry *c = &sCall->contacts[sCall->cursor];
    enum TrainerPicID pic = ContactPic(c);
    struct SpriteSheet sheet = { sCall->portraitTiles, sizeof(sCall->portraitTiles), TAG_CALL_PORTRAIT };
    struct SpritePalette pal = { NULL, TAG_CALL_PORTRAIT_PAL };
    static const struct SpriteTemplate tmpl =
    {
        .tileTag = TAG_CALL_PORTRAIT, .paletteTag = TAG_CALL_PORTRAIT_PAL, .oam = &sOam_64x64,
        .anims = gDummySpriteAnimTable, .images = NULL, .affineAnims = gDummySpriteAffineAnimTable,
        .callback = SpriteCallbackDummy,
    };

    FreePortrait();
    if (pic >= TRAINER_PIC_COUNT || gTrainerPicInfo[pic].frontPic == NULL)
    {
        CreateHead(ROWS, c, headX, headY);  // no trainer pic: overworld head at 2x (mock: Mom)
        return;
    }
    DecompressDataWithHeaderWram(gTrainerPicInfo[pic].frontPic->imageData, sCall->portraitTiles);
    if (round)
    {
        // mock: the pic's 48x48 window at (8, 2), cut to a circle of radius 24.5
        u32 x, y;
        for (y = 0; y < 64; y++)
        {
            for (x = 0; x < 64; x++)
            {
                s32 dx = 2 * (s32)x - 2 * 8 - 47, dy = 2 * (s32)y - 2 * 2 - 47;
                if (dx * dx + dy * dy > 49 * 49)
                {
                    u8 *b = &sCall->portraitTiles[((y / 8) * 8 + x / 8) * TILE_SIZE_4BPP + (y % 8) * 4 + (x % 8) / 2];
                    *b &= (x & 1) ? 0x0F : 0xF0;
                }
            }
        }
    }
    pal.data = gTrainerPicInfo[pic].frontPic->paletteData;
    LoadSpriteSheet(&sheet);
    LoadSpritePalette(&pal);
    sCall->portraitId = CreateSprite(&tmpl, picX + 32, picY + 32, 1);
}

static void DestroyListSprites(void)
{
    u32 i;
    for (i = 0; i < ROWS; i++)
    {
        FreeHead(i);
        DestroySpriteIfAny(&sCall->tagIds[i]);
    }
    for (i = 0; i < 4; i++)
        DestroySpriteIfAny(&sCall->rowPillIds[i]);
}

// ---------------------------------------------------------------- drawing
static void PrintTitle(const u8 *right)
{
    FillWindowPixelBuffer(WIN_TITLE, PIXEL_FILL(0));
    AddTextPrinterParameterized4(WIN_TITLE, FONT_NORMAL, 23, 0, 0, 0, sColors_Title, TEXT_SKIP_DRAW, COMPOUND_STRING("CALL"));
    if (right != NULL)
        AddTextPrinterParameterized4(WIN_TITLE, FONT_NARROW, 236 - GetStringWidth(FONT_NARROW, right, 0), 0, 0, 0,
                                     sColors_Title, TEXT_SKIP_DRAW, right);
    CopyWindowToVram(WIN_TITLE, COPYWIN_GFX);
}

// kit label pill with the pin cap, sized to the text (mock: 14 + cap + text width)
static void DrawLocationPill(u32 win, s32 x, s32 y, mapsec_u16_t mapSec)
{
    u32 w;
    GetMapName(gStringVar2, mapSec, 0);
    w = GetStringWidth(FONT_NARROW, gStringVar2, 0);
    PhoneUI_RoundBox(win, x, y, 14 + 16 + w, 14, 4, KIT_PANEL, KIT_INK, KIT_WHITE, KIT_PANEL_SHADE, TRUE);
    BlitBitmapRectToWindow(win, sGlyphs_Gfx, 0, 0, 40, 16, x, y, 17, 14);
    AddTextPrinterParameterized4(win, FONT_NARROW, x + 16 + 4, y - 1, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, gStringVar2);
}

static void DrawKeyHint(u32 win, s32 x, s32 y, bool32 bKey, const u8 *label)
{
    BlitBitmapRectToWindow(win, sGlyphs_Gfx, bKey ? 32 : 24, 0, 40, 16, x, y + 4, 8, 8);
    AddTextPrinterParameterized4(win, FONT_NARROW, x + 11, y, 0, 0, sColors_Soft, TEXT_SKIP_DRAW, label);
}

static void PrintProfile(u32 win, s32 x, s32 y, const struct PokenavMatchCallEntry *c)
{
    u8 *nl;
    ContactProfile(c, gStringVar4);
    for (nl = gStringVar4; *nl != EOS && *nl != CHAR_NEWLINE; nl++)
        ;
    if (*nl == CHAR_NEWLINE)
    {
        *nl = EOS;
        AddTextPrinterParameterized4(win, FONT_NORMAL, x, y + 14, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, nl + 1);
    }
    AddTextPrinterParameterized4(win, FONT_NORMAL, x, y, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, gStringVar4);
}

static void PrintRow(u32 r)
{
    u32 i = sCall->top + r, y = ROW_Y + r * ROW_H - 16;
    bool32 sel = (i == sCall->cursor);
    const struct PokenavMatchCallEntry *c;

    FillWindowPixelRect(WIN_A, PIXEL_FILL(0), 0, y, 29 * 8, 16);
    if (i >= sCall->count)
        return;
    c = &sCall->contacts[i];
    ContactName(c, gStringVar1);
    AddTextPrinterParameterized4(WIN_A, FONT_NORMAL, 33 - 8, y, 0, 0, sel ? sColors_InkSel : sColors_Ink, TEXT_SKIP_DRAW, gStringVar1);
    GetMapName(gStringVar2, c->mapSec, 0);
    AddTextPrinterParameterized4(WIN_A, FONT_NARROW, 200 - 8 - GetStringWidth(FONT_NARROW, gStringVar2, 0), y, 0, 0,
                                 sel ? sColors_SoftSel : sColors_Soft, TEXT_SKIP_DRAW, gStringVar2);
}

static void DrawScrollThumb(void)
{
    // track x 230-236, y 20-107 (BG art); thumb = gold kit pill sized by the visible fraction
    s32 trackH = ROWS * ROW_H - 3 - 2, h = trackH, y = 0;
    FillWindowPixelRect(WIN_A, PIXEL_FILL(0), 230 - 8, ROW_Y - 16, 7, ROWS * ROW_H);
    if (sCall->count > ROWS)
    {
        h = trackH * ROWS / sCall->count;
        y = (trackH - h) * sCall->top / (sCall->count - ROWS);
    }
    if (h < 6)
        h = 6;
    PhoneUI_RoundBox(WIN_A, 231 - 8, ROW_Y + 1 - 16 + y, 5, h, 1, KIT_SELECT, KIT_INK, KIT_SELECT_LIGHT, KIT_SELECT_DARK, TRUE);
}

static void PrintTray(void)
{
    const struct PokenavMatchCallEntry *c = &sCall->contacts[sCall->cursor];
    u32 tag = ContactTag(c);
    static const u8 sColors_Rematch[] = {0, KIT_TAG_REMATCH, KIT_PANEL_SHADE};
    static const u8 sColors_Home[] = {0, KIT_TAG_HOME, KIT_PANEL_SHADE};

    FillWindowPixelBuffer(WIN_B, PIXEL_FILL(0));
    if (sCall->count != 0)
    {
        DrawLocationPill(WIN_B, 8, 119 - 112, c->mapSec);
        if (tag == TAG_REMATCH)
        {
            const u8 *s = COMPOUND_STRING("Ready for a rematch!");
            AddTextPrinterParameterized4(WIN_B, FONT_NARROW, 236 - GetStringWidth(FONT_NARROW, s, 0), 118 - 112, 0, 0,
                                         sColors_Rematch, TEXT_SKIP_DRAW, s);
        }
        else if (tag == TAG_HOME)
        {
            const u8 *s = COMPOUND_STRING("Home");
            AddTextPrinterParameterized4(WIN_B, FONT_NARROW, 236 - GetStringWidth(FONT_NARROW, s, 0), 118 - 112, 0, 0,
                                         sColors_Home, TEXT_SKIP_DRAW, s);
        }
        PrintProfile(WIN_B, 8, 130 - 112, c);
    }
    else
    {
        AddTextPrinterParameterized4(WIN_B, FONT_NORMAL, 8, 130 - 112, 0, 0, sColors_Ink, TEXT_SKIP_DRAW,
                                     COMPOUND_STRING("No contacts yet, bzzt!"));
    }
    CopyWindowToVram(WIN_B, COPYWIN_GFX);
}

static void RefreshListSprites(void)
{
    u32 r, k;

    for (r = 0; r < ROWS; r++)
    {
        u32 i = sCall->top + r;
        s16 y = ROW_Y + r * ROW_H;
        FreeHead(r);
        DestroySpriteIfAny(&sCall->tagIds[r]);
        if (i >= sCall->count)
            continue;
        CreateHead(r, &sCall->contacts[i], 12 + 8, y + 8);
        switch (ContactTag(&sCall->contacts[i]))
        {
        case TAG_REMATCH:
            sCall->tagIds[r] = CreateSprite(&sTemplate_Tag, 204 + 16, y + 2 + 8, 0);
            break;
        case TAG_HOME:
            sCall->tagIds[r] = CreateSprite(&sTemplate_Tag, 204 + 16, y + 2 + 8, 0);
            if (sCall->tagIds[r] != MAX_SPRITES)
                StartSpriteAnim(&gSprites[sCall->tagIds[r]], 1);
            break;
        }
    }
    for (k = 0; k < 4; k++)
    {
        if (sCall->rowPillIds[k] == MAX_SPRITES)
        {
            sCall->rowPillIds[k] = CreateSprite(&sTemplate_RowPill, 8 + k * 64 + 32, 0, 5);
            StartSpriteAnim(&gSprites[sCall->rowPillIds[k]], k);
        }
        gSprites[sCall->rowPillIds[k]].y = ROW_Y + (sCall->cursor - sCall->top) * ROW_H + 16;
        gSprites[sCall->rowPillIds[k]].invisible = (sCall->count == 0);
    }
}

static void DrawList(void)
{
    u32 r;
    FillWindowPixelBuffer(WIN_A, PIXEL_FILL(0));
    for (r = 0; r < ROWS; r++)
        PrintRow(r);
    DrawScrollThumb();
    CopyWindowToVram(WIN_A, COPYWIN_GFX);
    PrintTray();
    RefreshListSprites();
}

static void DrawCard(void)
{
    const struct PokenavMatchCallEntry *c = &sCall->contacts[sCall->cursor];
    u32 i;
    static const u8 sColors_StripText[] = {0, KIT_WHITE, KIT_TAG_REMATCH};  // shadow = the strip's dark red

    FillWindowPixelBuffer(WIN_A, PIXEL_FILL(0));
    ContactName(c, gStringVar1);
    AddTextPrinterParameterized4(WIN_A, FONT_NORMAL, 92 - 80, 20 - 16, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, gStringVar1);
    DrawLocationPill(WIN_A, 92 - 80, 38 - 16, c->mapSec);
    PrintProfile(WIN_A, 92 - 80, 57 - 16, c);
    if (ContactTag(c) == TAG_REMATCH)
        AddTextPrinterParameterized4(WIN_A, FONT_NARROW, 98 - 80, 91 - 16, 0, 0, sColors_StripText, TEXT_SKIP_DRAW,
                                     COMPOUND_STRING("Wants a rematch!"));
    CopyWindowToVram(WIN_A, COPYWIN_GFX);

    FillWindowPixelBuffer(WIN_B, PIXEL_FILL(0));
    for (i = 0; i < 2; i++)
        AddTextPrinterParameterized4(WIN_B, FONT_NORMAL, 8 + i * 116 + 32, 121 - 112, 0, 0,
                                     i == sCall->button ? sColors_InkSel : sColors_Ink, TEXT_SKIP_DRAW,
                                     i == 0 ? COMPOUND_STRING("CALL") : COMPOUND_STRING("BACK"));
    DrawKeyHint(WIN_B, 8, 144 - 112, FALSE, COMPOUND_STRING("Select"));
    CopyWindowToVram(WIN_B, COPYWIN_GFX);
    for (i = 0; i < 2; i++)
    {
        gSprites[sCall->btnPillIds[i]].x = 8 + sCall->button * 116 + i * 64 + 32;
        gSprites[sCall->btnPillIds[i]].y = 118 + 16;
    }
}

static void DrawRingText(bool32 talking)
{
    const struct PokenavMatchCallEntry *c = &sCall->contacts[sCall->cursor];
    s32 nw;

    FillWindowPixelBuffer(WIN_A, PIXEL_FILL(0));
    ContactName(c, gStringVar1);
    nw = GetStringWidth(FONT_NORMAL, gStringVar1, 0);
    PhoneUI_RoundBox(WIN_A, RING_CX - nw / 2 - 8, 92 - 88, nw + 16, 14, 4, KIT_PANEL, KIT_INK, KIT_WHITE, KIT_PANEL_SHADE, TRUE);
    AddTextPrinterParameterized4(WIN_A, FONT_NORMAL, RING_CX - nw / 2, 91 - 88, 0, 0, sColors_Ink, TEXT_SKIP_DRAW, gStringVar1);
    if (!talking)
    {
        static const u8 *const sDots[] = { COMPOUND_STRING("Calling."), COMPOUND_STRING("Calling.."), COMPOUND_STRING("Calling...") };
        AddTextPrinterParameterized4(WIN_A, FONT_NARROW, RING_CX - GetStringWidth(FONT_NARROW, sDots[2], 0) / 2, 106 - 88, 0, 0,
                                     sColors_Calling, TEXT_SKIP_DRAW, sDots[(sCall->timer / 24) % 3]);
    }
    CopyWindowToVram(WIN_A, COPYWIN_GFX);
}

static void DrawRings(void)
{
    u32 k;
    FillWindowPixelBuffer(WIN_RINGS, PIXEL_FILL(0));
    // mock: r = 30 + ((phase * 2 + k * 8) % 24), shown while it clears the header (r < 41); 1 phase = 4 frames
    for (k = 0; k < 3; k++)
    {
        s32 r = 30 + (((sCall->timer / 4) * 2 + k * 8) % 24);
        if (RING_CY - r > 17)
            PhoneUI_Ring(WIN_RINGS, RING_CX - 72, RING_CY - 16, r, r < 40 ? KIT_ACCENT_LIGHT : KIT_ACCENT);
    }
    CopyWindowToVram(WIN_RINGS, COPYWIN_GFX);
}

static void PrintTalkTimer(void)
{
    u32 secs = sCall->talkFrames / 60;
    u8 *p = ConvertIntToDecimalStringN(gStringVar3, secs / 60, STR_CONV_MODE_LEFT_ALIGN, 2);
    *p++ = CHAR_COLON;
    ConvertIntToDecimalStringN(p, secs % 60, STR_CONV_MODE_LEADING_ZEROS, 2);
    PrintTitle(gStringVar3);
}

// ---------------------------------------------------------------- screens
static void LeaveScreen(void)
{
    u32 i;

    if (sCall->screen == SCREEN_LIST)
        DestroyListSprites();
    for (i = 0; i < 2; i++)
        DestroySpriteIfAny(&sCall->btnPillIds[i]);
    FreePortrait();
    if (sCall->dialogueWin != WINDOW_NONE)
    {
        ClearDialogWindowAndFrame(WIN_B, FALSE);
        sCall->dialogueWin = WINDOW_NONE;
    }
    RemoveWindow(WIN_A);
    RemoveWindow(WIN_B);
    if (sCall->screen == SCREEN_RING || sCall->screen == SCREEN_TALK)
        RemoveWindow(WIN_RINGS);
    FillBgTilemapBufferRect_Palette0(0, 0, 0, 2, 32, 30);
    FillBgTilemapBufferRect_Palette0(1, 0, 0, 0, 32, 32);
}

static void LoadScreenTilemap(const u32 *bg2)
{
    DecompressDataWithHeaderWram(bg2, sCall->bg2Tilemap);
    ScheduleBgCopyTilemapToVram(2);
}

static void EnterScreen(u32 screen)
{
    const struct PokenavMatchCallEntry *c = &sCall->contacts[sCall->cursor];
    u32 i;

    if (gMain.callback2 == CB2_Call)
        LeaveScreen();
    sCall->screen = screen;
    sCall->timer = 0;
    AddWindow(&sScreenWindows[screen][0]);
    AddWindow(&sScreenWindows[screen][1]);
    PutWindowTilemap(WIN_A);
    PutWindowTilemap(WIN_B);

    switch (screen)
    {
    case SCREEN_LIST:
        ConvertIntToDecimalStringN(gStringVar3, sCall->count, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringExpandPlaceholders(gStringVar4, sCall->count == 1 ? COMPOUND_STRING("1 contact") : COMPOUND_STRING("{STR_VAR_3} contacts"));
        StringCopy(gStringVar3, gStringVar4);
        PrintTitle(gStringVar3);
        LoadScreenTilemap(sCallList_Tilemap);
        DrawList();
        break;
    case SCREEN_CARD:
        PrintTitle(NULL);
        LoadScreenTilemap(ContactTag(c) == TAG_REMATCH ? sCallCardStrip_Tilemap : sCallCard_Tilemap);
        DecompressDataWithHeaderWram(sCallChips_Tilemap, sCall->bg1Tilemap);
        for (i = 0; i < 2; i++)
        {
            sCall->btnPillIds[i] = CreateSprite(&sTemplate_BtnPill, 0, 0, 5);
            StartSpriteAnim(&gSprites[sCall->btnPillIds[i]], i);
        }
        CreatePortrait(FALSE, 12, 28, 44, 62);
        DrawCard();
        break;
    case SCREEN_RING:
    case SCREEN_TALK:
        AddWindow(&sRingWindow);
        PutWindowTilemap(WIN_RINGS);
        LoadScreenTilemap(sCallRing_Tilemap);
        CreatePortrait(TRUE, 88, 32, RING_CX, RING_CY);
        if (screen == SCREEN_RING)
        {
            PrintTitle(COMPOUND_STRING("Calling…"));
            DrawRingText(FALSE);
            DrawRings();
            FillWindowPixelBuffer(WIN_B, PIXEL_FILL(0));
            DrawKeyHint(WIN_B, 96, 140 - 136, TRUE, COMPOUND_STRING("Hang up"));
            CopyWindowToVram(WIN_B, COPYWIN_GFX);
        }
        else
        {
            sCall->talkFrames = 0;
            PrintTalkTimer();
            DrawRingText(TRUE);
            FillWindowPixelBuffer(WIN_RINGS, PIXEL_FILL(0));
            CopyWindowToVram(WIN_RINGS, COPYWIN_GFX);
            FillWindowPixelBuffer(WIN_B, PIXEL_FILL(1));
            DrawDialogueFrame(WIN_B, FALSE);
            sCall->dialogueWin = WIN_B;
            AddTextPrinterParameterized(WIN_B, FONT_NORMAL, sCall->message, 0, 1, GetPlayerTextSpeedDelay(), NULL);
        }
        break;
    }
    ScheduleBgCopyTilemapToVram(0);
    ScheduleBgCopyTilemapToVram(1);
}

// ---------------------------------------------------------------- input
static void MoveListCursor(s32 delta)
{
    s32 next = sCall->cursor + delta;
    u32 oldTop = sCall->top;

    if (next < 0 || next >= sCall->count)
        return;
    PlaySE(SE_SELECT);
    sCall->cursor = next;
    if (sCall->cursor < sCall->top)
        sCall->top = sCall->cursor;
    else if (sCall->cursor >= sCall->top + ROWS)
        sCall->top = sCall->cursor - ROWS + 1;
    if (oldTop != sCall->top)
    {
        DrawList();
        return;
    }
    {
        u32 r;
        for (r = 0; r < ROWS; r++)
            PrintRow(r);
        CopyWindowToVram(WIN_A, COPYWIN_GFX);
        PrintTray();
        RefreshListSprites();
    }
}

static bool32 IsTrainerNearby(const struct PokenavMatchCallEntry *c)
{
    // pokenav_match_call_list.c ShouldDoNearbyMessage
#if FREE_MATCH_CALL == FALSE
    if (!c->isSpecialTrainer)
        return c->mapSec == gMapHeader.regionMapSectionId && !gSaveBlock1Ptr->trainerRematches[c->headerId];
    if (c->headerId == MC_HEADER_WATTSON)
        return c->mapSec == gMapHeader.regionMapSectionId && FlagGet(FLAG_BADGE05_GET) && !FlagGet(FLAG_WATTSON_REMATCH_AVAILABLE);
#endif
    return FALSE;
}

static void StartCall(void)
{
    const struct PokenavMatchCallEntry *c = &sCall->contacts[sCall->cursor];
    static const u8 sText_CantCall[] = _("A call can't be made from here.");
    static const u8 sText_CloseBy[] = _("That TRAINER is close by.\nTalk to the TRAINER in person!");

    sCall->newRematchRequest = FALSE;
    if (!Overworld_MapTypeAllowsTeleportAndFly(gMapHeader.mapType))
    {
        // no signal (Rotom in a cave): straight to the message
        sCall->message = sText_CantCall;
        PlaySE(SE_FAILURE);
        EnterScreen(SCREEN_TALK);
        return;
    }
    if (IsTrainerNearby(c))
    {
        sCall->message = sText_CloseBy;
        PlaySE(SE_SELECT);
        EnterScreen(SCREEN_TALK);
        return;
    }
    if (!c->isSpecialTrainer)
        sCall->newRematchRequest = SelectMatchCallMessage(GetTrainerIdxByRematchIdx(c->headerId), gStringVar4);
    else
        MatchCall_GetMessage(c->headerId, gStringVar4);
    sCall->message = gStringVar4;
    PlaySE(SE_POKENAV_CALL);
    EnterScreen(SCREEN_RING);
}

static void Task_Call(u8 taskId)
{
    sCall->timer++;
    if (gPaletteFade.active)
        return;

    switch (sCall->screen)
    {
    case SCREEN_LIST:
        if (sCall->state == 1)
        {
            if (!gPaletteFade.active)
            {
                DestroyTask(taskId);
                LeaveScreen();
                FreeAllWindowBuffers();
                FREE_AND_SET_NULL(sCall);
                SetMainCallback2(CB2_ReturnToRotomPhone);
            }
            return;
        }
        if (JOY_REPEAT(DPAD_UP))
            MoveListCursor(-1);
        else if (JOY_REPEAT(DPAD_DOWN))
            MoveListCursor(1);
        else if (JOY_NEW(A_BUTTON) && sCall->count != 0)
        {
            PlaySE(SE_SELECT);
            sCall->button = 0;      // CALL pre-selected: calling is still A, A
            EnterScreen(SCREEN_CARD);
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            sCall->state = 1;
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        }
        break;
    case SCREEN_CARD:
        if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        {
            PlaySE(SE_SELECT);
            sCall->button ^= 1;
            DrawCard();
        }
        else if (JOY_NEW(A_BUTTON))
        {
            if (sCall->button == 0)
                StartCall();
            else
            {
                PlaySE(SE_SELECT);
                EnterScreen(SCREEN_LIST);
            }
        }
        else if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_SELECT);
            EnterScreen(SCREEN_LIST);
        }
        break;
    case SCREEN_RING:
        if (sCall->timer % 4 == 0)
            DrawRings();
        if (sCall->timer % 24 == 0)
            DrawRingText(FALSE);
        if (JOY_NEW(B_BUTTON))
        {
            PlaySE(SE_POKENAV_HANG_UP);
            EnterScreen(SCREEN_CARD);
        }
        else if (sCall->timer >= RING_FRAMES)
        {
            EnterScreen(SCREEN_TALK);
        }
        break;
    case SCREEN_TALK:
        sCall->talkFrames++;
        if (sCall->talkFrames % 60 == 0)
            PrintTalkTimer();
        if (!IsTextPrinterActiveOnWindow(WIN_B) && JOY_NEW(A_BUTTON | B_BUTTON))
        {
            PlaySE(SE_POKENAV_HANG_UP);
            EnterScreen(SCREEN_CARD);   // a new rematch request now shows on the card (and the list tag)
        }
        break;
    }
}
