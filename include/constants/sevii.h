#ifndef GUARD_CONSTANTS_SEVII_H
#define GUARD_CONSTANTS_SEVII_H

// Wavebreak Voyages: where a voyage to the Sevii Islands lands (dev_scripts/voyages/sevii/build_sevii.py).
// One Island's harbour dock, in front of the ferry sailor; warp id 1 is a landing-only warp event on that cell.
#define SEVII_ARRIVAL_MAP      MAP_ONE_ISLAND_HARBOR
#define SEVII_ARRIVAL_WARP_ID  1
#define SEVII_ARRIVAL_X        8
#define SEVII_ARRIVAL_Y        4

// Every island harbour (MAP_<N>_ISLAND_HARBOR, Three's is reached from Three Isle Port) uses the same landing
// cell and warp id; the ferry sailor stands at (8,5) and Mr. Briney's boat at (8,7).
#define SEVII_HARBOR_LANDING_WARP_ID  1

#endif // GUARD_CONSTANTS_SEVII_H
