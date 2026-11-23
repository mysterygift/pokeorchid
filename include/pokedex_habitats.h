#ifndef GUARD_POKEDEX_HABITATS_H
#define GUARD_POKEDEX_HABITATS_H

// Orchid: Pokédex HABITATS (src/pokedex_habitats.c) - helpers shared with Palm's research (src/research.c)

enum { HAB_REGION_TOSA, HAB_REGION_TIKSI, HAB_REGION_COUNT };
enum { HAB_ZONE_NONE, HAB_ZONE_NORTH, HAB_ZONE_EAST, HAB_ZONE_SOUTH, HAB_ZONE_WEST, HAB_ZONE_COUNT };

struct HabitatCounts { u16 seen, captured, catalogued, total; };

// Sections of a region / zone that have wild tables (zone HAB_ZONE_NONE = the whole region). Returns the count.
u32 Habitats_GetSections(u32 region, u32 zone, mapsec_u16_t *out, u32 max);
// Seen / captured / catalogued / total over the species of those sections, day + night
void Habitats_CountSections(const mapsec_u16_t *secs, u32 numSecs, struct HabitatCounts *c);
// ... over the species that appear only in their night tables
void Habitats_CountNightOnly(const mapsec_u16_t *secs, u32 numSecs, struct HabitatCounts *c);
bool32 Habitats_SectionHasSpecies(mapsec_u16_t mapsec, u16 species);
const u8 *Habitats_GetZoneName(u32 zone);

#endif // GUARD_POKEDEX_HABITATS_H
