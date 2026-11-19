#ifndef GUARD_TEXT_WINDOW_H
#define GUARD_TEXT_WINDOW_H

#define WINDOW_FRAMES_COUNT 8 // Orchid kit frames (vanilla had 20; older saves map safely, see text_window.c)

// Accent ramp slots: in a kit FRAME palette (kit.py roles) and in the Orchid window palette (message box,
// Orchid YES/NO frame band). See GetFrameTintedWindowPalette.
#define ORCHID_FRAME_PAL_ACCENT_DARK    7
#define ORCHID_FRAME_PAL_ACCENT         8
#define ORCHID_FRAME_PAL_ACCENT_LIGHT   9
#define ORCHID_WINDOW_PAL_ACCENT_DARK  13
#define ORCHID_WINDOW_PAL_ACCENT       14
#define ORCHID_WINDOW_PAL_ACCENT_LIGHT 15

struct TilesPal
{
    const u8 *tiles;
    const u16 *pal;
};

extern const u8 gTextWindowFrame1_Gfx[];
extern const u16 gTextWindowFrame1_Pal[];

const struct TilesPal *GetWindowFrameTilesPal(u8 id);
void LoadMessageBoxGfx(u8 windowId, u16 destOffset, u8 palOffset);
void LoadStdWindowGfx(u8 windowId, u16 tileStart, u8 palette);
void LoadSignBoxGfx(u8 windowId, u16 destOffset, u8 palOffset);
void LoadWindowGfx(u8 windowId, u8 frameId, u16 destOffset, u8 palOffset);
void LoadUserWindowBorderGfx(u8 windowId, u16 destOffset, u8 palOffset);
void LoadUserWindowBorderGfx_(u8 windowId, u16 destOffset, u8 palOffset);
void LoadUserWindowBorderGfxOnBg(u8 bg, u16 destOffset, u8 palOffset);
void DrawTextBorderOuter(u8 windowId, u16 tileNum, u8 palNum);
void DrawTextBorderInner(u8 windowId, u16 tileNum, u8 palNum);
void rbox_fill_rectangle(u8 windowId);
const u16 *GetTextWindowPalette(u8 id);
const u16 *GetOverworldTextboxPalettePtr(void);
const u16 *GetFrameTintedWindowPalette(const u16 *windowPal);
void LoadSignPostWindowFrameGfx(void);
void LoadDexNavWindowGfx(u8 windowId, u16 destOffset, u8 palOffset);

#endif // GUARD_TEXT_WINDOW_H
