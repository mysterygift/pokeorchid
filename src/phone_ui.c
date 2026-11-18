// Orchid UI kit primitives for Rotom Phone app windows (ports of dev_scripts/orchid_ui/kit.py), for the
// parts that change at runtime (pills sized to their text, rings). Colours are kit palette roles.
#include "global.h"
#include "phone_ui.h"
#include "bg.h"
#include "event_object_movement.h"
#include "decompress.h"
#include "malloc.h"
#include "sprite.h"
#include "window.h"

static void Px(u32 win, s32 x, s32 y, u8 c)
{
    struct Window *w = &gWindows[win];
    if (x < 0 || y < 0 || x >= w->window.width * 8 || y >= w->window.height * 8)
        return;
    FillWindowPixelRect(win, c, x, y, 1, 1);
}

static void HLine(u32 win, s32 x0, s32 x1, s32 y, u8 c)
{
    if (x1 < x0 || y < 0)
        return;
    if (x0 < 0)
        x0 = 0;
    FillWindowPixelRect(win, c, x0, y, x1 - x0 + 1, 1);
}

static u32 RoundInset(u32 r, s32 y, s32 h)
{
    static const u8 sTables[5][5] = { {0}, {1, 0}, {2, 1, 0}, {3, 1, 1, 0}, {4, 2, 1, 1, 0} };
    s32 e;
    if (r > 4)
        r = 4;
    if (y >= 0 && y < (s32)r)
        return sTables[r][y];
    e = h - 1 - y;
    if (e >= 0 && e < (s32)r)
        return sTables[r][e];
    return 0;
}

void PhoneUI_RoundBox(u32 win, s32 x0, s32 y0, s32 w, s32 h, u32 r, u8 face, u8 outline, u8 light, u8 shade, bool32 bevel)
{
    s32 y, x;
    u32 ins0 = RoundInset(r, 0, h);

    for (y = 0; y < h; y++)
    {
        u32 ins = RoundInset(r, y, h);
        HLine(win, x0 + ins, x0 + w - 1 - ins, y0 + y, face);
        Px(win, x0 + ins, y0 + y, outline);
        Px(win, x0 + w - 1 - ins, y0 + y, outline);
    }
    HLine(win, x0 + ins0, x0 + w - 1 - ins0, y0, outline);
    HLine(win, x0 + ins0, x0 + w - 1 - ins0, y0 + h - 1, outline);
    for (y = 1; y < h - 1; y++)
    {
        u32 ins = RoundInset(r, y, h), insp = RoundInset(r, y - 1, h);
        if (insp > ins + 1)
        {
            for (x = ins + 1; x < (s32)insp; x++)
            {
                s32 yy = (y <= h / 2) ? y0 + y - 1 : y0 + y;
                Px(win, x0 + x, yy, outline);
                Px(win, x0 + w - 1 - x, yy, outline);
            }
        }
    }
    for (y = h - 2; y > 0; y--)
    {
        u32 ins = RoundInset(r, y, h), insn = RoundInset(r, y + 1, h);
        if (insn > ins + 1)
        {
            for (x = ins + 1; x < (s32)insn; x++)
            {
                Px(win, x0 + x, y0 + y + 1, outline);
                Px(win, x0 + w - 1 - x, y0 + y + 1, outline);
            }
        }
    }
    if (!bevel)
        return;
    for (y = 1; y < h - 1; y++)
    {
        u32 ins = RoundInset(r, y, h);
        if (y == 1)
            HLine(win, x0 + ins + 1, x0 + w - 2 - ins, y0 + y, light);
        else if (y == h - 2)
            HLine(win, x0 + ins + 1, x0 + w - 2 - ins, y0 + y, shade);
        else
        {
            Px(win, x0 + ins + 1, y0 + y, light);
            Px(win, x0 + w - 2 - ins, y0 + y, shade);
        }
    }
}

// kit.ring(cx, cy, r): pixels whose centre lies in (r - 1, r] from the point (cx, cy), cx/cy whole pixels
void PhoneUI_Ring(u32 win, s32 cx, s32 cy, s32 r, u8 c)
{
    s32 x, y;
    s32 outer = 4 * r * r, inner = 4 * (r - 1) * (r - 1);

    for (y = -r - 1; y <= r + 1; y++)
    {
        for (x = -r - 1; x <= r + 1; x++)
        {
            s32 dx = 2 * x + 1, dy = 2 * y + 1;     // pixel centre, in half pixels from (cx, cy)
            s32 d2 = dx * dx + dy * dy;
            if (d2 > inner && d2 <= outer)
                Px(win, cx + x, cy + y, c);
        }
    }
}

// 16x16 head (rows 10-25 of frame 0, facing down) of an overworld sprite, as 4bpp OBJ tiles.
// Returns the palette tag to use (the object event's own palette, loaded).
u16 PhoneUI_BuildOwHead(u16 graphicsId, u8 *dest)
{
    const struct ObjectEventGraphicsInfo *info = GetObjectEventGraphicsInfo(graphicsId);
    const u8 *src;
    u8 *buf = NULL;
    u32 r, tx, frameW = info->width / 8;

    if (OW_GFX_COMPRESS && info->compressed)
    {
        buf = Alloc(GetDecompressedDataSize(info->images->data));
        if (buf == NULL)
            return TAG_NONE;
        DecompressDataWithHeaderWram(info->images->data, buf);
        src = buf;
    }
    else
    {
        src = info->images[0].data;
    }
    for (r = 0; r < 16; r++)
    {
        u32 s = r + 10;
        if (info->height < 32)
            s = r;
        for (tx = 0; tx < 2 && tx < frameW; tx++)
        {
            const u8 *srow = src + ((s / 8) * frameW + tx) * TILE_SIZE_4BPP + (s % 8) * 4;
            u8 *drow = dest + ((r / 8) * 2 + tx) * TILE_SIZE_4BPP + (r % 8) * 4;
            memcpy(drow, srow, 4);
        }
    }
    if (buf != NULL)
        Free(buf);
    if (info->paletteTag != TAG_NONE)
        LoadObjectEventPalette(info->paletteTag);
    return info->paletteTag;
}
