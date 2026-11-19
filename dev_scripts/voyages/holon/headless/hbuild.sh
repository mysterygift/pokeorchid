#!/bin/bash
# Holon harness build: debug flags for no-collision / no-encounters / no trainer sight, then the shared harness.
set -e
WT=/Users/arandavies/Development/pokemon-orchid/pokeorchid-voy-holon
OUT=$(cd "$(dirname "$0")" && pwd)
cd $WT
sed -i '' 's/^#define OW_FLAG_NO_TRAINER_SEE      0 /#define OW_FLAG_NO_TRAINER_SEE      FLAG_UNUSED_0x29D /; s/^#define OW_FLAG_NO_COLLISION        0 /#define OW_FLAG_NO_COLLISION        FLAG_UNUSED_0x29F /' include/config/overworld.h
sed -i '' 's/^#define WE_FLAG_NO_ENCOUNTER        0 /#define WE_FLAG_NO_ENCOUNTER        FLAG_UNUSED_0x29E /' include/config/wild_encounter.h
grep -n "FLAG_UNUSED_0x29" include/config/overworld.h include/config/wild_encounter.h
bash dev_scripts/mgba_headless/harness_build.sh $WT $OUT/h $OUT/test.sav || { git checkout include/config/overworld.h include/config/wild_encounter.h; exit 1; }
git checkout include/config/overworld.h include/config/wild_encounter.h
