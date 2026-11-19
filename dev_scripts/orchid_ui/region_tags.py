"""
Tosa region map data from the region map tagger (dev_scripts/region_map_tagger/tags.json).

tags.json is the source of truth for which cursor cells belong to which map section, each
section's id / in-game name / kind, train stations and rail lines. Everything here is derived
from its `grid` (area keys per cell) and `areas`, never from the per-area summary fields the tool
also writes (cells / bbox / maps), which go stale when areas are edited by hand.

Area kinds: town / city -> map node drawn as a disc; landmark / dungeon / other with a single cell
-> node drawn as a diamond; route / water and multi-cell landmarks -> no node (cursor name only).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TAGS = os.path.join(ROOT, "dev_scripts", "region_map_tagger", "tags.json")

TOWN_KINDS = {"town", "city"}
NO_NODE_KINDS = {"route", "water"}


class Area:
    def __init__(self, a, cells):
        self.key = a["key"]
        self.id = a["id"]
        self.original_id = a.get("originalId")
        self.name = a.get("name") or ""
        self.kind = a.get("kind") or "landmark"
        self.notes = a.get("notes") or ""
        self.station = bool(a.get("station"))
        self.kanto = bool(a.get("kanto"))
        self.cells = cells
        self._station_cell = a.get("stationCell")

    @property
    def bbox(self):
        xs = [c[0] for c in self.cells]
        ys = [c[1] for c in self.cells]
        return min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1

    @property
    def node_kind(self):
        """'town', 'landmark' or None."""
        if not self.cells or self.kind in NO_NODE_KINDS:
            return None
        if self.kind in TOWN_KINDS:
            return "town"
        return "landmark" if len(self.cells) == 1 else None

    @property
    def node_cell(self):
        """The station marker's cell if it's in the area, else the area cell nearest the centroid."""
        if self._station_cell and tuple(self._station_cell) in self.cells:
            return tuple(self._station_cell)
        cx = sum(c[0] for c in self.cells) / len(self.cells)
        cy = sum(c[1] for c in self.cells) / len(self.cells)
        return min(self.cells, key=lambda c: ((c[0] - cx) ** 2 + (c[1] - cy) ** 2, c[1], c[0]))


ALIASES = os.path.join(ROOT, "include", "constants", "region_map_section_aliases.h")


def resolve_alias(section_id):
    """The current id of a section that may have been renamed (follows region_map_section_aliases.h)."""
    aliases = {}
    if os.path.exists(ALIASES):
        for line in open(ALIASES):
            parts = line.split()
            if len(parts) == 3 and parts[0] == "#define" and parts[1].startswith("MAPSEC_"):
                aliases[parts[1]] = parts[2]
    while section_id in aliases:
        section_id = aliases[section_id]
    return section_id


class Tags:
    def __init__(self, path=TAGS, region=None):
        """region: None = every area; "tosa" = all but the Kanto/Sevii block; "tiksi" = only that block
        (Tiksi reuses it, tags_tiksi.json). The other region's areas, cells and map assignments are ignored,
        so each exporter only ever renames / places / reassigns its own sections."""
        d = json.load(open(path))
        cells = {}
        for y, row in enumerate(d["grid"]):
            for x, key in enumerate(row):
                if key:
                    cells.setdefault(key, []).append((x, y))
        areas = d["areas"]
        if region is not None:
            areas = [a for a in areas if bool(a.get("kanto")) == (region == "tiksi")]
        self.areas = [Area(a, sorted(cells.get(a["key"], []), key=lambda c: (c[1], c[0]))) for a in areas]
        self.by_key = {a.key: a for a in self.areas}
        self.grid = [[self.by_key[k].id if k in self.by_key else "MAPSEC_NONE" for k in row] for row in d["grid"]]
        self.map_assign = {f: k for f, k in d.get("mapAssign", {}).items()       # map folder -> area key
                           if region is None or k in self.by_key}
        self.lines = d.get("lines", [])
        ids = [a.id for a in self.areas]
        dup = {i for i in ids if ids.count(i) > 1}
        assert not dup, "duplicate section ids in tags.json: %s" % sorted(dup)

    def placed(self):
        return [a for a in self.areas if a.cells]

    def nodes(self):
        """[(area, (cx, cy), is_landmark)] in reading order."""
        out = [(a, a.node_cell, a.node_kind == "landmark") for a in self.areas if a.node_kind]
        return sorted(out, key=lambda n: (n[1][1], n[1][0]))

    def renames(self):
        """{original id: new id} for existing sections whose id changed."""
        return {a.original_id: a.id for a in self.areas if a.original_id and a.original_id != a.id}

    def map_sections(self):
        """{map folder: section id} from the Maps tab (keys resolved to the current ids)."""
        out = {}
        for folder, key in self.map_assign.items():
            a = self.by_key.get(key)
            out[folder] = a.id if a else key
        return out

    def rail_edges(self):
        """[(line name, line colour, station a id, station b id, [bend cells])], station to station."""
        out = []
        for line in self.lines:
            prev, via = None, []
            for p in line["points"]:
                if "area" in p:
                    a = self.by_key.get(p["area"])
                    if a is None:
                        continue
                    if prev is not None:
                        out.append((line["name"], line["color"], prev.id, a.id, via))
                    prev, via = a, []
                else:
                    via.append((p["x"], p["y"]))
        return out


def rebase(path=TAGS, section_ids=None):
    """After an export: make tags.json describe the repo as it now is. Area keys become the current
    section ids and originalId / origName the current id / name, so the tagger shows no pending
    changes and later renames start from here. Old ids live on in region_map_section_aliases.h."""
    d = json.load(open(path))
    if section_ids is not None:                # drop areas the export removed (unused placeholders)
        d["areas"] = [a for a in d["areas"] if a["id"] in section_ids]
    key_map = {a["key"]: a["id"] for a in d["areas"]}
    for a in d["areas"]:
        a["key"] = a["originalId"] = a["id"]
        a["origName"] = a.get("name") or ""
        for k in ("cells", "bbox", "maps", "changes", "stationPos"):   # derived; the tool rewrites them
            a.pop(k, None)
    d["grid"] = [[key_map.get(k, k) if k else None for k in row] for row in d["grid"]]
    d["mapAssign"] = {f: key_map.get(k, k) for f, k in d.get("mapAssign", {}).items()}
    for line in d.get("lines", []):
        for p in line["points"]:
            if "area" in p:
                p["area"] = key_map.get(p["area"], p["area"])
    d.pop("mapChanges", None)
    with open(path, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
