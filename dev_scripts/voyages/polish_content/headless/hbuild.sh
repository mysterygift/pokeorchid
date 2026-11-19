#!/bin/bash
# polish_content harness ROM (copy of e2e/hbuild.sh): debug flags 0x29D (no trainer sight), 0x29E (no wild
# encounters), 0x29F (no collision) + every party mon "knows" Surf and Rock Smash (MonKnowsMove), then
# dev_scripts/mgba_headless/harness_build.sh. Config files and party_menu.c are restored afterwards.
# usage: hbuild.sh <outdir> <save.sav>    (output: <outdir>/h.gba + h.elf)   -- rebuild normally afterwards
set -e
WT=$(cd "$(dirname "$0")/../../../.." && pwd)
OUT=$(cd "$1" && pwd)
cd "$WT"
cp include/config/overworld.h "$OUT/overworld.h.bak"; cp include/config/wild_encounter.h "$OUT/wild_encounter.h.bak"
cp src/party_menu.c "$OUT/party_menu.c.bak"
restore() { cp "$OUT/overworld.h.bak" include/config/overworld.h; cp "$OUT/wild_encounter.h.bak" include/config/wild_encounter.h; cp "$OUT/party_menu.c.bak" src/party_menu.c; }
trap restore EXIT
sed -i '' 's/^#define OW_FLAG_NO_TRAINER_SEE      0 /#define OW_FLAG_NO_TRAINER_SEE      FLAG_UNUSED_0x29D /; s/^#define OW_FLAG_NO_COLLISION        0 /#define OW_FLAG_NO_COLLISION        FLAG_UNUSED_0x29F /' include/config/overworld.h
sed -i '' 's/^#define WE_FLAG_NO_ENCOUNTER        0 /#define WE_FLAG_NO_ENCOUNTER        FLAG_UNUSED_0x29E /' include/config/wild_encounter.h
python3 - <<'PY'
p='src/party_menu.c'; s=open(p).read()
a="bool8 MonKnowsMove(struct Pokemon *mon, enum Move move)\n{\n"
assert a in s
s=s.replace(a, a+"    if (move == MOVE_SURF || move == MOVE_ROCK_SMASH) return TRUE; // HARNESS ONLY\n",1)
open(p,'w').write(s)
PY
grep -c "FLAG_UNUSED_0x29" include/config/overworld.h include/config/wild_encounter.h
bash dev_scripts/mgba_headless/harness_build.sh "$WT" "$OUT/h" "$2"
