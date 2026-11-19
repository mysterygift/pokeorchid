#!/bin/bash
# Test-only harness ROM for the Sevii checks: dev_scripts/mgba_headless/harness_build.sh plus a temporary patch so
# every party mon "knows" Surf (the test save has no Surf user). src/party_menu.c is restored afterwards; rebuild
# normally after running this.   usage: harness_test_build.sh <outdir/outname> <save.sav>
set -e
WT=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$WT"
cp src/party_menu.c /tmp/sevii_party_menu.c.$$
python3 - <<'PY'
p='src/party_menu.c'; s=open(p).read()
s=s.replace("bool8 MonKnowsMove(struct Pokemon *mon, enum Move move)\n{\n","bool8 MonKnowsMove(struct Pokemon *mon, enum Move move)\n{\n    if (move == MOVE_SURF) return TRUE; // HARNESS ONLY\n",1)
open(p,'w').write(s)
PY
bash dev_scripts/mgba_headless/harness_build.sh "$WT" "$1" "$2" || { cp /tmp/sevii_party_menu.c.$$ src/party_menu.c; exit 1; }
cp /tmp/sevii_party_menu.c.$$ src/party_menu.c; rm /tmp/sevii_party_menu.c.$$
grep -c "HARNESS" src/party_menu.c || true
