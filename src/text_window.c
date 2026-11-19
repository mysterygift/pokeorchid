#include "global.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "palette.h"
#include "bg.h"
#include "graphics.h"
#include "menu.h"

static const u16 sStdTextWindow_Gfx[]  = INCGFX_U16("graphics/text_window/std.png", ".4bpp");

const u8 gTextWindowFrame1_Gfx[] = INCGFX_U8("graphics/text_window/1.png", ".4bpp");

const u16 gTextWindowFrame1_Pal[] = INCGFX_U16("graphics/text_window/1.png", ".gbapal");

static const u16 sTextWindowPalettes[][16] =
{
    INCGFX_U16("graphics/text_window/message_box.png", ".gbapal"),
    INCGFX_U16("graphics/text_window/text_pal1.pal", ".gbapal"),
    INCGFX_U16("graphics/text_window/text_pal2.pal", ".gbapal"),
    INCGFX_U16("graphics/text_window/text_pal3.pal", ".gbapal"),
    INCGFX_U16("graphics/text_window/text_pal4.pal", ".gbapal")
};

// Orchid: the FRAME option picks one of the 8 kit frames (dev_scripts/orchid_ui/export_options.py), which
// replace vanilla's 20 types. Saves from before keep their index: types 1-8 map to kit frames 1-8, and any
// higher index (vanilla 9-20) falls back to TYPE 1 Orchid (GetWindowFrameTilesPal).
static const struct TilesPal sWindowFrames[WINDOW_FRAMES_COUNT] =
{
    {gOrchidFrame1_Gfx, gOrchidFrame1_Pal},
    {gOrchidFrame2_Gfx, gOrchidFrame2_Pal},
    {gOrchidFrame3_Gfx, gOrchidFrame3_Pal},
    {gOrchidFrame4_Gfx, gOrchidFrame4_Pal},
    {gOrchidFrame5_Gfx, gOrchidFrame5_Pal},
    {gOrchidFrame6_Gfx, gOrchidFrame6_Pal},
    {gOrchidFrame7_Gfx, gOrchidFrame7_Pal},
    {gOrchidFrame8_Gfx, gOrchidFrame8_Pal},
};

static const u16 sTextWindowDexNavFrame[] = INCGFX_U16("graphics/text_window/dexnav_pal.pal", ".gbapal");
static const struct TilesPal sDexNavWindowFrame = {gTextWindowFrame1_Gfx, sTextWindowDexNavFrame};

// code
const struct TilesPal *GetWindowFrameTilesPal(u8 id)
{
    if (id >= WINDOW_FRAMES_COUNT)
        return &sWindowFrames[0];
    else
        return &sWindowFrames[id];
}

void LoadMessageBoxGfx(u8 windowId, u16 destOffset, u8 palOffset)
{
    LoadBgTiles(GetWindowAttribute(windowId, WINDOW_BG), gMessageBox_Gfx, 0x1C0, destOffset);
    LoadPalette(GetOverworldTextboxPalettePtr(), palOffset, PLTT_SIZE_4BPP);
}

void LoadStdWindowGfx(u8 windowId, u16 destOffset, u8 palOffset)
{
    LoadBgTiles(GetWindowAttribute(windowId, WINDOW_BG), sStdTextWindow_Gfx, 0x120, destOffset);
    LoadPalette(GetTextWindowPalette(3), palOffset, PLTT_SIZE_4BPP);
}

void LoadSignBoxGfx(u8 windowId, u16 destOffset, u8 palOffset)
{
    LoadBgTiles(GetWindowAttribute(windowId, WINDOW_BG), gSignpostWindow_Gfx, 0x1C0, destOffset);
    LoadPalette(GetTextWindowPalette(1), palOffset, PLTT_SIZE_4BPP);
}

void LoadUserWindowBorderGfx_(u8 windowId, u16 destOffset, u8 palOffset)
{
    LoadUserWindowBorderGfx(windowId, destOffset, palOffset);
}

void LoadWindowGfx(u8 windowId, u8 frameId, u16 destOffset, u8 palOffset)
{
    const struct TilesPal *frame = GetWindowFrameTilesPal(frameId);

    LoadBgTiles(GetWindowAttribute(windowId, WINDOW_BG), frame->tiles, 0x120, destOffset);
    LoadPalette(frame->pal, palOffset, PLTT_SIZE_4BPP);
}

void LoadUserWindowBorderGfx(u8 windowId, u16 destOffset, u8 palOffset)
{
    LoadWindowGfx(windowId, gSaveBlock2Ptr->optionsWindowFrameType, destOffset, palOffset);
}

void DrawTextBorderOuter(u8 windowId, u16 tileNum, u8 palNum)
{
    u8 bgLayer = GetWindowAttribute(windowId, WINDOW_BG);
    u16 tilemapLeft = GetWindowAttribute(windowId, WINDOW_TILEMAP_LEFT);
    u16 tilemapTop = GetWindowAttribute(windowId, WINDOW_TILEMAP_TOP);
    u16 width = GetWindowAttribute(windowId, WINDOW_WIDTH);
    u16 height = GetWindowAttribute(windowId, WINDOW_HEIGHT);

    FillBgTilemapBufferRect(bgLayer, tileNum + 0, tilemapLeft - 1,      tilemapTop - 1,         1,      1,      palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 1, tilemapLeft,          tilemapTop - 1,         width,  1,      palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 2, tilemapLeft + width,  tilemapTop - 1,         1,      1,      palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 3, tilemapLeft - 1,      tilemapTop,             1,      height, palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 5, tilemapLeft + width,  tilemapTop,             1,      height, palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 6, tilemapLeft - 1,      tilemapTop + height,    1,      1,      palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 7, tilemapLeft,          tilemapTop + height,    width,  1,      palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 8, tilemapLeft + width,  tilemapTop + height,    1,      1,      palNum);
}

void DrawTextBorderInner(u8 windowId, u16 tileNum, u8 palNum)
{
    u8 bgLayer = GetWindowAttribute(windowId, WINDOW_BG);
    u16 tilemapLeft = GetWindowAttribute(windowId, WINDOW_TILEMAP_LEFT);
    u16 tilemapTop = GetWindowAttribute(windowId, WINDOW_TILEMAP_TOP);
    u16 width = GetWindowAttribute(windowId, WINDOW_WIDTH);
    u16 height = GetWindowAttribute(windowId, WINDOW_HEIGHT);

    FillBgTilemapBufferRect(bgLayer, tileNum + 0, tilemapLeft,              tilemapTop,                 1,          1,          palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 1, tilemapLeft + 1,          tilemapTop,                 width - 2,  1,          palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 2, tilemapLeft + width - 1,  tilemapTop,                 1,          1,          palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 3, tilemapLeft,              tilemapTop + 1,             1,          height - 2, palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 5, tilemapLeft + width - 1,  tilemapTop + 1,             1,          height - 2, palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 6, tilemapLeft,              tilemapTop + height - 1,    1,          1,          palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 7, tilemapLeft + 1,          tilemapTop + height - 1,    width -     2,  1,      palNum);
    FillBgTilemapBufferRect(bgLayer, tileNum + 8, tilemapLeft + width - 1,  tilemapTop + height - 1,    1,          1,          palNum);
}

void rbox_fill_rectangle(u8 windowId)
{
    u8 bgLayer = GetWindowAttribute(windowId, WINDOW_BG);
    u16 tilemapLeft = GetWindowAttribute(windowId, WINDOW_TILEMAP_LEFT);
    u16 tilemapTop = GetWindowAttribute(windowId, WINDOW_TILEMAP_TOP);
    u16 width = GetWindowAttribute(windowId, WINDOW_WIDTH);
    u16 height = GetWindowAttribute(windowId, WINDOW_HEIGHT);

    FillBgTilemapBufferRect(bgLayer, 0, tilemapLeft - 1, tilemapTop - 1, width + 2, height + 2, 0x11);
}

const u16 *GetTextWindowPalette(u8 id)
{
    switch (id)
    {
    case 0:
        id = 0x00;
        break;
    case 1:
        id = 0x10;
        break;
    case 2:
        id = 0x20;
        break;
    case 3:
        id = 0x30;
        break;
    case 4:
    default:
        id = 0x40;
        break;
    }

    return (const u16 *)(sTextWindowPalettes) + id;
}

// Orchid: windows drawn with their own art (the field message box, the Orchid YES/NO frame that the Mart
// and PC reuse) keep their frame band in the Orchid window palette's slots 13-15. Those take the selected
// FRAME type's accent ramp (the kit frames' role slots 7-9), so the boxes follow the FRAME option like the
// standard frames do. TYPE 1 Orchid's ramp is the original purple, so the default look is unchanged.
// Returns a shared buffer: load it straight away.
static EWRAM_DATA u16 sFrameTintedWindowPal[16] = {0};

const u16 *GetFrameTintedWindowPalette(const u16 *windowPal)
{
    const u16 *framePal = GetWindowFrameTilesPal(gSaveBlock2Ptr->optionsWindowFrameType)->pal;

    CpuCopy16(windowPal, sFrameTintedWindowPal, PLTT_SIZE_4BPP);
    sFrameTintedWindowPal[ORCHID_WINDOW_PAL_ACCENT_DARK] = framePal[ORCHID_FRAME_PAL_ACCENT_DARK];
    sFrameTintedWindowPal[ORCHID_WINDOW_PAL_ACCENT] = framePal[ORCHID_FRAME_PAL_ACCENT];
    sFrameTintedWindowPal[ORCHID_WINDOW_PAL_ACCENT_LIGHT] = framePal[ORCHID_FRAME_PAL_ACCENT_LIGHT];
    return sFrameTintedWindowPal;
}

const u16 *GetOverworldTextboxPalettePtr(void)
{
    return GetFrameTintedWindowPalette(gMessageBox_Pal);
}

// Effectively LoadUserWindowBorderGfx but specifying the bg directly instead of a window from that bg
void LoadUserWindowBorderGfxOnBg(u8 bg, u16 destOffset, u8 palOffset)
{
    LoadBgTiles(bg, GetWindowFrameTilesPal(gSaveBlock2Ptr->optionsWindowFrameType)->tiles, 0x120, destOffset);
    LoadPalette(GetWindowFrameTilesPal(gSaveBlock2Ptr->optionsWindowFrameType)->pal, palOffset, PLTT_SIZE_4BPP);
}

void LoadDexNavWindowGfx(u8 windowId, u16 destOffset, u8 palOffset)
{
    LoadBgTiles(GetWindowAttribute(windowId, WINDOW_BG), sDexNavWindowFrame.tiles, 0x120, destOffset);
    LoadPalette(sDexNavWindowFrame.pal, palOffset, 32);
}
