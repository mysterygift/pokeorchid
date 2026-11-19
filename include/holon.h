#ifndef GUARD_HOLON_H
#define GUARD_HOLON_H

// Orchid Holon (Wavebreak Voyages): small engine hooks for the Holon maps.
struct ScriptContext;
struct SpritePalette;
bool32 IsHolonOverworld(void);
const struct SpritePalette *Holon_GetFieldEffectPalette(const struct SpritePalette *palette);
void Holon_SetSphereGlow(struct ScriptContext *ctx);
u8 Holon_LoadSpherePalette(void);
struct MapLayout;
void Holon_LoadHealedRingsPalette(const struct MapLayout *mapLayout, bool8 skipFaded);

#endif // GUARD_HOLON_H
