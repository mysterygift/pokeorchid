#!/bin/bash
# Harness ROM for the phone/music checks: dev_scripts/mgba_headless/harness_build.sh plus debug Script 1
# (R+START -> Scripts -> Script 1) = callnative PlayTrainerEncounterMusic, so the Sevii encounter themes go through
# the normal approach-music path for whatever trainer the test pokes into TRAINER_BATTLE_PARAM.opponentA. data/scripts/debug.inc is restored
# from a copy afterwards. usage: hbuild.sh <outdir> <save.sav>   (output: <outdir>/h.gba + h.elf)
set -e
WT=$(cd "$(dirname "$0")/../../.." && pwd)
OUT=$(cd "$1" && pwd)
cd "$WT"
cp data/scripts/debug.inc "$OUT/debug.inc.bak"
trap 'cp "$OUT/debug.inc.bak" data/scripts/debug.inc' EXIT
python3 - <<'PY'
p = 'data/scripts/debug.inc'; s = open(p).read()
old = "Debug_EventScript_Script_1::\n\trelease\n\tend\n"
assert old in s
# PlayTrainerEncounterMusic for TRAINER_BATTLE_PARAM.opponentA (poked by the test: gTrainerBattleParameter+2).
# A real trainerbattle needs an object event (battle_setup.c asserts when run from the player).
s = s.replace(old, "Debug_EventScript_Script_1::\n\tcallnative PlayTrainerEncounterMusic\n\trelease\n\tend\n")
open(p, 'w').write(s)
PY
bash dev_scripts/mgba_headless/harness_build.sh "$WT" "$OUT/h" "$2"
