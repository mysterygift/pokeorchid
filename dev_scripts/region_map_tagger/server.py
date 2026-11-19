#!/usr/bin/env python3
"""Region map tagger: a tiny local web tool for assigning region map cells and
game maps to map sections (routes, towns, landmarks).

    python3 dev_scripts/region_map_tagger/server.py   # then open http://localhost:8765
    python3 dev_scripts/region_map_tagger/server.py 8766 --region tiksi   # Tiksi (2nd region)

It only reads the repo. Saving writes dev_scripts/region_map_tagger/tags.json, which
is then applied to region_map_layout.h / region_map_sections.json / map.json.
"""
import json
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REGION = sys.argv[sys.argv.index("--region") + 1] if "--region" in sys.argv else "tosa"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8765

# Per region: terrain art, cursor-grid layout (+ its C array name), tags file, the user's route art and
# whether that art is rotated 180 deg relative to the ROM (Tosa yes, Tiksi no). Tiksi reuses the vanilla
# Kanto/Sevii map sections (dev_scripts/orchid_ui/export_region_map_tiksi.py).
REGIONS = {
    "tosa": dict(png="map.png", bin="map.bin", layout="region_map_layout.h", array="sRegionMap_MapSectionLayout",
                 tags="tags.json", routes="tosa_routes.png", rotated=True),
    "tiksi": dict(png="map_tiksi.png", bin="map_tiksi.bin", layout="region_map_layout_tiksi.h",
                  array="sRegionMapSections_Tiksi", tags="tags_tiksi.json", routes="tiksi_towns_routes.png",
                  rotated=False),
}
R = REGIONS[REGION]
MAP_PNG = ROOT / "graphics/pokenav/region_map" / R["png"]
MAP_BIN = ROOT / "graphics/pokenav/region_map" / R["bin"]
SECTIONS = ROOT / "src/data/region_map/region_map_sections.json"
LAYOUT = ROOT / "src/data/region_map" / R["layout"]
MAPS_DIR = ROOT / "data/maps"
TAGS = HERE / R["tags"]
REF = ROOT / "dev_scripts/orchid_ui/ref"   # the user's source art (240x160, stored unrotated)

MAP_WIDTH, MAP_HEIGHT = 28, 15   # src/region_map.c
GRID_X, GRID_Y = 1, 2            # MAPCURSOR_X_MIN / MAPCURSOR_Y_MIN (in 8px tiles)


def parse_layout():
    text = LAYOUT.read_text()
    body = text.split(R["array"], 1)[1]
    rows = re.findall(r"\{([^{}]*)\}", body)
    grid = [[c.strip() for c in r.split(",") if c.strip()] for r in rows[:MAP_HEIGHT]]
    assert len(grid) == MAP_HEIGHT and all(len(r) == MAP_WIDTH for r in grid), "unexpected layout shape"
    return grid


def load_maps():
    maps = []
    for mj in sorted(MAPS_DIR.glob("*/map.json")):
        try:
            d = json.loads(mj.read_text())
        except json.JSONDecodeError:
            continue
        maps.append({
            "folder": mj.parent.name,
            "id": d.get("id"),
            "name": d.get("name"),
            "mapsec": d.get("region_map_section"),
            "type": d.get("map_type"),
        })
    return maps


def kanto_start_id():
    """First section of the Kanto/Sevii block (= Tiksi), following renames in region_map_section_aliases.h."""
    aliases = {}
    path = ROOT / "include/constants/region_map_section_aliases.h"
    if path.is_file():
        for line in path.read_text().splitlines():
            parts = line.split()
            if len(parts) == 3 and parts[0] == "#define" and parts[1].startswith("MAPSEC_"):
                aliases[parts[1]] = parts[2]
    sid = "MAPSEC_PALLET_TOWN"
    while sid in aliases:
        sid = aliases[sid]
    return sid


def repo_state():
    return {
        "grid": parse_layout(),
        "sections": json.loads(SECTIONS.read_text())["map_sections"],
        "maps": load_maps(),
        "tilemap": list(MAP_BIN.read_bytes()),
        "gridOrigin": [GRID_X, GRID_Y],
        "size": [MAP_WIDTH, MAP_HEIGHT],
        "routeArt": R["routes"] if (REF / R["routes"]).is_file() else None,
        "routeRotated": R["rotated"],
        "region": REGION,
        "kantoStartId": kanto_start_id(),
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, str):
            body = body.encode()
        elif not isinstance(body, bytes):
            body = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif path == "/map.png":
            self._send(200, MAP_PNG.read_bytes(), "image/png")
        elif path.startswith("/ref/") and (REF / path[5:]).is_file() and "/" not in path[5:]:
            self._send(200, (REF / path[5:]).read_bytes(), "image/png")
        elif path == "/api/repo":
            self._send(200, repo_state())
        elif path == "/api/tags":
            self._send(200, json.loads(TAGS.read_text()) if TAGS.exists() else None)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/tags":
            return self._send(404, {"error": "not found"})
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        TAGS.write_text(json.dumps(data, indent=2) + "\n")
        self._send(200, {"ok": True, "path": str(TAGS.relative_to(ROOT))})

    def log_message(self, fmt, *args):
        if "POST" in (args[0] if args else ""):
            sys.stderr.write("saved %s\n" % TAGS.name)


if __name__ == "__main__":
    print(f"Region map tagger ({REGION}) on http://localhost:{PORT}  (saves to {TAGS.relative_to(ROOT)})")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
