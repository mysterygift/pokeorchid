#!/bin/sh
# Rebuild every Tosa Rail mockup, the ROM assets and the review page. Needs Python with Pillow:
#   PYTHON=/path/to/venv/bin/python ./build_all.sh
# The Orchid UI kit is imported from ORCHID_UI_KIT (default: the satchel worktree).
# Just the ROM assets: "$PYTHON" export_station_map.py
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
"$PY" export_station_map.py
"$PY" mock_station_map.py
"$PY" anim_station_map.py
"$PY" mock_big_map.py
"$PY" anim_journey.py
"$PY" review_page.py
