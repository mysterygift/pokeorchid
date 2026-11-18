#ifndef GUARD_PHONE_UI_H
#define GUARD_PHONE_UI_H

// Orchid kit palette roles (dev_scripts/orchid_ui/kit.py)
enum
{
    KIT_TRANSPARENT,
    KIT_INK,
    KIT_INK_SOFT,
    KIT_WHITE,
    KIT_PANEL,
    KIT_PANEL_SHADE,
    KIT_PANEL_DARK,
    KIT_ACCENT_DARK,
    KIT_ACCENT,
    KIT_ACCENT_LIGHT,
    KIT_ACCENT_PALE,
    KIT_SELECT_DARK,
    KIT_SELECT,
    KIT_SELECT_LIGHT,
    KIT_SPARE_A,
    KIT_SPARE_B,
};

void PhoneUI_RoundBox(u32 win, s32 x, s32 y, s32 w, s32 h, u32 r, u8 face, u8 outline, u8 light, u8 shade, bool32 bevel);
void PhoneUI_Ring(u32 win, s32 cx, s32 cy, s32 r, u8 c);
u16 PhoneUI_BuildOwHead(u16 graphicsId, u8 *dest);

#endif // GUARD_PHONE_UI_H
