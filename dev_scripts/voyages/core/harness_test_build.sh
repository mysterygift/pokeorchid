#!/bin/bash
# Test-only harness ROM for the voyage checks: dev_scripts/mgba_headless/harness_build.sh plus a temporary patch
# giving 5 Master Balls on every voyage arrival (to test catch -> mega stone). src/voyages.c is restored after.
# usage: harness_test_build.sh <outdir/outname> <save.sav>
set -e
WT=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$WT"
cp src/voyages.c /tmp/voyages.c.orig.$$
python3 - <<'PY'
p='src/voyages.c'; s=open(p).read()
s=s.replace('#include "voyages.h"\n','#include "voyages.h"\n#include "item.h"\n',1)
s=s.replace('    d = &sVoyageDestinations[dest];\n    SetWarpDestination(','    d = &sVoyageDestinations[dest];\n    AddBagItem(ITEM_MASTER_BALL, 5); // HARNESS ONLY\n    SetWarpDestination(',1)
open(p,'w').write(s)
PY
bash dev_scripts/mgba_headless/harness_build.sh "$WT" "$1" "$2" || { cp /tmp/voyages.c.orig.$$ src/voyages.c; exit 1; }
cp /tmp/voyages.c.orig.$$ src/voyages.c; rm /tmp/voyages.c.orig.$$
grep -c "HARNESS" src/voyages.c || true
