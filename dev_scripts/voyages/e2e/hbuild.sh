#!/bin/bash
# e2e harness ROM: debug flags 0x29D (no trainer sight), 0x29E (no wild encounters), 0x29F (no collision), then
# dev_scripts/mgba_headless/harness_build.sh. The two config files are restored from copies afterwards.
# usage: hbuild.sh <outdir> <save.sav>    (output: <outdir>/h.gba + h.elf)
set -e
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=$(cd "$1" && pwd)
cd "$WT"
cp include/config/overworld.h "$OUT/overworld.h.bak"; cp include/config/wild_encounter.h "$OUT/wild_encounter.h.bak"
restore() { cp "$OUT/overworld.h.bak" include/config/overworld.h; cp "$OUT/wild_encounter.h.bak" include/config/wild_encounter.h; }
trap restore EXIT
sed -i '' 's/^#define OW_FLAG_NO_TRAINER_SEE      0 /#define OW_FLAG_NO_TRAINER_SEE      FLAG_UNUSED_0x29D /; s/^#define OW_FLAG_NO_COLLISION        0 /#define OW_FLAG_NO_COLLISION        FLAG_UNUSED_0x29F /' include/config/overworld.h
sed -i '' 's/^#define WE_FLAG_NO_ENCOUNTER        0 /#define WE_FLAG_NO_ENCOUNTER        FLAG_UNUSED_0x29E /' include/config/wild_encounter.h
grep -c "FLAG_UNUSED_0x29" include/config/overworld.h include/config/wild_encounter.h
bash dev_scripts/mgba_headless/harness_build.sh "$WT" "$OUT/h" "$2"
