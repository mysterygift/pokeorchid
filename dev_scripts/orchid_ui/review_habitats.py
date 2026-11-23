"""Design-review page for the dex HABITATS view + day/night pass (round 2).
usage: review_habitats.py MOCK_DIR OUT_HTML"""
import base64
import json
import os
import sys

MOCK, OUT = sys.argv[1], sys.argv[2]


def img(name, alt):
    kind = "gif" if name.endswith(".gif") else "png"
    data = base64.b64encode(open(os.path.join(MOCK, name), "rb").read()).decode()
    return f'<img class="shot" src="data:image/{kind};base64,{data}" alt="{alt}">'


def figure(name, title, desc):
    return (f'<figure class="shot-card"><div class="mat">{img(name, title)}</div>'
            f'<figcaption><b>{title}</b><span>{desc}</span></figcaption></figure>')


CHANGES = [
    "<b>Built and running in the ROM</b> (screenshots below): START on the dex list opens Habitats.",
    "Badges: first catch = <b>grey Poké Ball</b>, catalogued = <b>colour Poké Ball</b>, everywhere (icons, counts, "
    "dex list rows, entry name pill, map badges).",
    "Dex entry: one capture shows category, height, weight and the AREA tab; the description needs the second capture.",
    "Wild tables: Railway Tunnels floor now triggers encounters; Telok Town and Drake Base Camp grass have tables.",
    "Night: house windows, gym door, Pokémon Center upper windows + door, Mart door only, station glass. "
    "Jetty streetlamps: the bulb under the lamp turns yellow (no glow sprite).",
    "227 leftover Hoenn maps deleted to make room (towns, routes 115-134, dungeons, Safari Zone, Navel Rock, "
    "Birth / Faraway Island, Trainer Hill). Battle Frontier, link rooms, contests and secret bases kept.",
]

MAP_SHOTS = [
    ("map_south.png", "Southern Tosa, Moongrove Marsh", "The Route View prompt is above the route name. Zone and route counts show seen / captured / catalogued / total."),
    ("map_west_night.png", "Night view selected", "The moon chip in the header means the route pages will open on their night lists."),
    ("map_single.png", "Only Tosa unlocked", "No tabs and no L / R chevrons."),
    ("map_tiksi.png", "Tiksi tab", "Appears only after the first landing at Furong Village."),
]
ROUTE_SHOTS = [
    ("route_seen.png", "Seen", "Greyscale icon. Name shown, 0 of 2 pips, rate and levels \"?\"."),
    ("route_captured.png", "Captured once", "Colour icon with a ball badge, 1 of 2 pips, levels shown, rate still \"?\"."),
    ("route_catalogued.png", "Catalogued", "Colour icon with a gold book badge, 2 of 2 pips, rate and levels shown."),
    ("route_unseen.png", "Not seen", "Black silhouette, ?????, method only."),
    ("route_night.png", "Night list", "The same marsh at night, with Spinarak, Gastly and Hoothoot among the night-only species."),
]
ENTRY_SHOTS = [
    ("entry_0.png", "Dex entry: seen", "????? category, no measurements, no description (unchanged)."),
    ("entry_1.png", "Dex entry: captured once", "Category, height and weight unlocked. The description area says how to finish."),
    ("entry_2.png", "Dex entry: catalogued", "Full description."),
]

QUESTIONS = [
    ("Delta evolutions", "Delta Glaceon evolved at Shoal Cave's ice room and Delta Leafeon at Petalburg Woods; both maps "
     "are now deleted, so those evolutions can't happen. <b>Recommendation:</b> point them at Frigo Cave (Tiksi) and "
     "Galangal Forest."),
    ("Telok and Tiksi windows", "Lights are on the TosaPort tileset (17 Tosa towns). Telok Town (Petalburg) and the four "
     "Tiksi towns need the same pass. <b>Recommendation:</b> do them next, same rules (Centre upper windows + door, "
     "Mart door, house windows)."),
    ("Mart door colour", "The Mart door glass borrows the shared window palette's blues, so by day it is a touch "
     "brighter than before. <b>Recommendation:</b> keep it; it is hard to spot."),
]

DAYNIGHT = [
    "OW_ENABLE_DNS is on. Towns, cities and routes tint toward blue at night, warm at dawn and dusk. "
    "Caves and interiors are untouched.",
    "Lit windows: house windows (yellow and purple houses) and the gym door in all 17 towns on the TosaPort "
    "tileset. They use a palette-swap trick that changes no art: TosaPort palette 11 is now an exact copy of the "
    "house palette with the glass colours marked as lights. By day they look identical. At night they glow "
    "amber instead of darkening.",
    "Tosa Port jetty: both streetlamps get a soft glow sprite at night (the engine's light objects). The round "
    "mooring posts are left dark.",
    "The start-menu banner, tab, location pill and icons are excluded from the tint, so the UI stays true-colour.",
    "Not lit yet: Centre / Mart / station windows (question 4), Telok Town (Petalburg tileset) and the Tiksi "
    "towns. Those tilesets need the same palette-swap pass, one per tileset.",
]


def main():
    rows = json.load(open(os.path.join(MOCK, "habitats.json")))
    trs = "".join(
        f'<tr><td>{r["name"]}</td><td class="num">{r["species"]}</td><td>{", ".join(r["day_only"][:6]) or "—"}</td>'
        f'<td>{", ".join(r["night_only"][:6]) or "—"}</td></tr>' for r in sorted(rows, key=lambda r: r["name"]))
    sec = lambda title, inner, intro="": (f'<section><h2>{title}</h2>{f"<p>{intro}</p>" if intro else ""}{inner}</section>')
    grid = lambda items: '<div class="grid">' + "".join(figure(*s) for s in items) + "</div>"
    html = f"""<title>Dex Habitats Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen&family=Inter:wght@400;600&display=swap">
<style>
/* Layout: one reading column of pixel-art plates on dark mats, then questions and data. */
:root {{
  --bg: #f1eef4; --fg: #26243a; --muted: #65617a; --plate: #1d1b29; --line: #d6d0de; --accent: #8c58b8; --gold: #c8901c;
  --display: "Silkscreen", "Courier New", monospace; --body: "Inter", system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; --gold: #f0c850; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; --gold: #f0c850; color-scheme: dark }}
body {{ background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }}
main {{ max-width: 1120px; margin: 0 auto; padding-block: 32px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 44px; }}
h1, h2 {{ font-family: var(--display); font-weight: 400; letter-spacing: .02em; text-wrap: balance; margin: 0; }}
h1 {{ font-size: 28px; }} h2 {{ font-size: 19px; color: var(--accent); }}
header p, section > p {{ color: var(--muted); max-width: 70ch; margin: 8px 0 0; }}
section {{ display: grid; gap: 16px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 440px), 1fr)); gap: 24px; }}
.shot-card {{ margin: 0; display: grid; gap: 10px; min-width: 0; align-content: start; }}
.mat {{ background: var(--plate); border-radius: 6px; padding: 10px; }}
.shot {{ display: block; width: 100%; height: auto; image-rendering: pixelated; }}
figcaption {{ display: grid; gap: 2px; }} figcaption span {{ color: var(--muted); font-size: 14px; }}
ol, ul {{ margin: 0; padding-left: 1.3em; display: grid; gap: 10px; max-width: 80ch; }}
.tw {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
th, td {{ text-align: left; padding: 5px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ color: var(--muted); font-weight: 600; }} .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
code {{ font-size: 13px; }}
</style>
<main>
<header>
  <h1>Dex Habitats · round 3</h1>
  <p>Habitats with your round 1 notes applied, plus the first time-of-day pass: night tint, lit windows, jetty lamps,
  and day / night encounter tables for every Tosa and Tiksi map. Mockups are 240×160 at 3×, built from the real
  tables on the <code>dex-habitats</code> branch. Catch states come from a made-up sample save.</p>
</header>
{sec("Changes since round 2", "<ul>" + "".join(f"<li>{c}</li>" for c in CHANGES) + "</ul>")}
{sec("Built: in the ROM", grid([
    ("ingame_habitats.png", "Headless mGBA: map (day / night) and route page (night / day)",
     "Sample save with Starly + Lotad catalogued, Mareep + Wurmple caught once, Dewpider / Tyrogue / Pikipek seen. "
     "The screenshot tool skips alpha blending, so the dimmed land shows solid here; in game it is a 50% blend."),
    ("ingame_jump.png", "A on Starly opens its entry", "Catalogued: rate + levels in the tray, full description; B returns to the list."),
    ("windows_night.png", "Changu City, day vs night (tileset render)", "Centre: upper windows + door. Mart: door only. Houses, gym door, station."),
    ("bulbs.png", "Tosa Port jetty lamps", "The bulb under each streetlamp turns yellow at night."),
]))}
{sec("Region map", grid([("map_cursor.gif", "Motion: browsing routes", "Route glow and the Ⓐ prompt pulse together.")] + MAP_SHOTS))}
{sec("Route page", grid([("route_daynight.gif", "Motion: SELECT flips day → night", "The rows change to the night list; captured icons bob.")] + ROUTE_SHOTS))}
{sec("Dex entry by capture count", grid(ENTRY_SHOTS))}
{sec("Day / night in game", grid([("ingame_daynight.png", "Headless mGBA: Changu City and the Tosa Port jetty, day and night",
     "This screenshot tool doesn't do alpha blending, so the lamp glows look solid here. In game they're translucent.")]) +
     "<ul>" + "".join(f"<li>{d}</li>" for d in DAYNIGHT) + "</ul>")}
{sec("Open questions", "<ol>" + "".join(f"<li><b>{t}.</b> {d}</li>" for t, d in QUESTIONS) + "</ol>",
     "Each has a recommendation; \"use your suggestions\" accepts them all.")}
{sec("Wild tables (placeholders)", '<div class="tw"><table><thead><tr><th>Habitat</th><th class="num">Species</th><th>Day only</th><th>Night only</th></tr></thead><tbody>' + trs + "</tbody></table></div>",
     "68 maps got a day table and a night table (46 Tosa, 22 Tiksi). Levels rise with travel distance from Telok, and Tiksi runs Lv 50–65. "
     "Every species family is enabled; Regi shrines have themed tables but no Regis. Retune in "
     "<code>dev_scripts/orchid_encounters/encounters.py</code> and re-run it. Its README has a theme line for every map.")}
</main>
"""
    open(OUT, "w").write(html)


if __name__ == "__main__":
    main()
