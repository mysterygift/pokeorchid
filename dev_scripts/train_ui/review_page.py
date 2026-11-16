"""Build out/review.html — round 2 (self-contained: images embedded as data URIs). usage: python review_page.py"""
import base64
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def uri(name):
    mime = "image/gif" if name.endswith(".gif") else "image/png"
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(os.path.join(OUT, name), "rb").read()).decode())


def img(name, alt, cls="shot"):
    return '<img class="%s" src="%s" alt="%s" loading="lazy">' % (cls, uri(name), html.escape(alt))


def figs(items):
    return "\n".join(
        '<figure class="state">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>'
        % (img(f, t), html.escape(t), html.escape(d)) for f, t, d in items)


CHANGES = [
    "A bigger placeholder network: 13 stations on 3 lines with 3 interchanges, drawn on a 512×256 "
    "canvas (about 2 × 2.3 screens of diagram) that pans under a fixed header and tray.",
    "A proposed camera rule (dead zone + re-centre), stills of three framings, a debug view of the dead "
    "zone, and an animated walk across the network.",
    "Off-screen hints: Gen 3 red chevrons where a tube leaves the screen (recommended), plus a header "
    "mini-map as the alternative.",
    "A GBA budget for the scrolling version: BG2 64×32 map, labels baked into BG2 tiles, OBJs following "
    "the scroll, and canvas size limits.",
    "Interchange stations get a ringed node, and the tray names every line that stops there. A third, "
    "green FOREST line was added, and the header legend now lists all three lines.",
    "The journey storyboard was rebuilt with the final train art from <code>graphics/train/train.png</code> "
    "(used as-is). The train is parked at the start, and after you get off it leaves (now decided).",
    "Round 1 decisions are logged below and in <code>dev_scripts/train_ui/DESIGN.md</code>.",
]

DECISIONS = [
    ("Unvisited stations", "Names are shown greyed, not hidden as “???”."),
    ("After you get off", "The train leaves."),
    ("Map layout", "Layout A, the line diagram. This round answers the follow-up: what a bigger map looks "
     "like and how it frames the selected station."),
    ("Departure", "The train is always parked at your platform when you choose a station."),
    ("Greyed stations", "The cursor skips them. The shake and message appear only when nothing visited "
     "lies in that direction."),
    ("Cost", "Rides are free, but you need the RAIL CARD key item. The engine checks for it before the map "
     "opens, so the map itself doesn't change."),
]

FLOW = [
    "Talk to the station attendant. Without a RAIL CARD you get a dialogue line and nothing else. With "
    "one, the TOSA RAIL map opens.",
    "Move the cursor between visited stations with the D-pad; greyed stations are skipped. On a large "
    "network the diagram pans to keep the selected station framed.",
    "Press A, then YES. The map fades to the platform, where the train is already parked with its "
    "middle-car door on the tile in front of you.",
    "The door opens, you step in, the door shuts, and the train eases out to the right.",
    "Fade and warp. At the destination the train eases in from the left and stops with the door on your "
    "arrival tile. You step down, the door shuts, and the train leaves.",
]

BIG_STILLS = [
    ("big_1_open_3x.png", "1. Opening framing",
     "The map opens centred on the cursor (MARIS BAY), clamped to the canvas edge, so TOSA PORT and the head "
     "sit bottom-left. Chevrons on the tubes show the network continuing east and north."),
    ("big_2_telok_3x.png", "2. Re-centred on TELOK TOWN",
     "UP from VALE JUNCTION lands outside the dead zone, so the camera eases 16 frames to centre TELOK. "
     "Chevrons now point out on all four sides."),
    ("big_3_koru_3x.png", "3. East side: KORU CITY",
     "Clamped at the canvas's right edge. The grey tubes to FERN GATE and CORAL END show where you "
     "haven't been yet."),
]

FIND = [
    ("big_2_telok_3x.png", "Option 1 — chevrons on tube exits (recommended)",
     "A red Gen 3 chevron sits wherever a tube crosses the viewport edge, pointing outward and bobbing 1px. "
     "It tells you both that the map continues and which line goes there."),
    ("big_5_minimap_3x.png", "Option 2 — header mini-map",
     "A 32×16 OBJ in the header (the canvas at 1/16) with a gold viewport box. It replaces the line legend, "
     "and at this size stations are single pixels."),
]

BUDGET = [
    "<b>BG2 = the diagram</b>, a 512×256 text BG: a 64×32 tilemap in 2 screenblocks (4 KB), scrolled with "
    "<code>BG2HOFS = camX</code>, <code>BG2VOFS = camY − 16</code>. The header and tray move to BG1 and "
    "their text to BG0, both fixed, so anything scrolling under them is hidden.",
    "<b>Tiles: 187 unique 4bpp tiles</b> for tubes and labels together (flip-deduped); 176 of them are "
    "label cells, since text barely dedupes. That's well inside one BG's 1024-tile range. Budget about 14 "
    "tiles per station.",
    "<b>Labels are baked into BG2</b>, rendered once into BG2 tile VRAM when the map opens. "
    "They scroll for free. Greyed and selected labels are per-cell palette swaps: pal 3 grey "
    "has WHITE set to the INK_SOFT colour, and pal 4 selected has WHITE set to INK and INK to "
    "SELECT_DARK. The script checks that no label cell contains tube pixels: 0 conflicts.",
    "<b>Gold name pill = OBJ</b> (64×16 + 16×16) at priority 2, behind BG2 at priority 1, so the baked "
    "text draws on top. Nodes, ring and head are OBJs at priority 1, in front of the tubes.",
    "<b>OBJs follow the scroll:</b> <code>x = canvasX − camX</code>, <code>y = canvasY − camY + 16</code>, "
    "updated every frame during a pan. <b>WIN0 = the map viewport</b> (y 16–127), with OBJs allowed only "
    "inside it, so nodes never draw over the header or tray.",
    "<b>OAM:</b> 13 nodes + ring + grey ring + head + pill (2) + up to 6 chevrons + 3 legend tubes "
    "= about 27 of 128.",
    "<b>BG palettes:</b> 0 orchid (RIDGE tubes, white labels, chrome), 1 sea (COAST), 2 forest, 3 grey "
    "(tubes and labels), 4 selected label, 5 grid; 13–15 text and frames as usual.",
    "<b>Canvas limits:</b> a text BG tops out at 512×512 (a 64×64 map, 8 KB) without streaming. "
    "Anything larger needs overworld-style tilemap streaming, which isn't worth it here. 512×256 holds "
    "this 13-station network. 512×512 would hold about 40 stations at the same density.",
    "<b>BG3 grid</b> follows the pan 1:1 plus its 1px/4-frame drift, so the paper moves with the "
    "diagram.",
]

QUESTIONS = [
    ("Camera rule: dead zone + re-centre, or always centre the cursor?",
     "<b>Recommend dead zone + re-centre.</b> Hops between neighbouring stations don't move the diagram, "
     "so it stays readable while you browse a cluster. When the cursor leaves the box, a full re-centre "
     "(not a nudge) gives the new station context on every side, so you don't land on the edge again "
     "after the next press. Always-centre moves the whole map on every press, which is a lot of motion "
     "for a menu."),
    ("How to show there's more map: chevrons on tube exits, or a header mini-map?",
     "<b>Recommend chevrons.</b> They're the existing Gen 3 language, cost no screen space, and say which "
     "line continues and where. The mini-map is too small to read at 1/16 and pushes out the line legend. "
     "Revisit it only if the real network goes past 512×256."),
    ("Labels baked into BG2, or OBJ text sprites?",
     "<b>Recommend baked into BG2.</b> They scroll with the tubes at no cost, greyed and selected are palette "
     "swaps, and they need no OAM. OBJ labels would use about 30 OAM entries and need per-frame repositioning "
     "for no visual gain."),
    ("D-pad picking on a bigger network",
     "<b>Recommend: nearest visited station inside a 90° cone in the pressed direction, preferring "
     "stations on a line through the current one.</b> On a sparse grid, plain “nearest in that "
     "direction” can jump across the map unexpectedly. The cone plus same-line preference makes the cursor "
     "follow the tubes."),
    ("Canvas size for the real network",
     "<b>Recommend designing the real Tosa network to fit 512×256</b> (one 64×32 map, about 190 tiles). "
     "Go to 512×512 only if the region really needs it. Past that, the line map should be split into "
     "regions rather than streamed."),
]

R1 = [
    ("map_a_default_3x.png", "A. Default view", "Small network, cursor on the nearest station."),
    ("map_b_telok_3x.png", "B. Cursor on another station", "Gold ring + gold name pill."),
    ("map_c_confirm_3x.png", "C. Confirm", "Orchid dialogue + YES/NO with the gold pill."),
    ("map_d_denied_3x.png", "D. Greyed station", "Ring shake, grey blink on the target, tray message."),
    ("map_alt_list_3x.png", "Layout B (not chosen)", "List + mini map."),
]


def main():
    changes = "\n".join("<li>%s</li>" % c for c in CHANGES)
    decisions = "\n".join("<li><b>%s.</b> %s</li>" % (html.escape(a), html.escape(b)) for a, b in DECISIONS)
    flow = "\n".join("<li>%s</li>" % html.escape(s) for s in FLOW)
    qs = "\n".join("<li><b>%s</b><p>%s</p></li>" % (html.escape(t), d) for t, d in QUESTIONS)
    budget = "\n".join("<li>%s</li>" % b for b in BUDGET)
    rows = []
    for line in open(os.path.join(OUT, "journey_timing.txt")).read().splitlines():
        if line.startswith("//") or not line.strip():
            continue
        name, rest = line.split(None, 1)
        val, note = rest.split("//")
        rows.append("<tr><td><code>%s</code></td><td>%s</td><td>%s</td></tr>"
                    % (name, val.strip(), html.escape(note.strip())))
    timing_rows = "\n".join(rows)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tosa Rail Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen&family=Inter:wght@400;600&display=swap">
<style>
:root {{
  --bg: #f1eef4; --fg: #26243a; --muted: #65617a; --plate: #1d1b29; --line: #d6d0de; --accent: #8c58b8; --gold: #f0c850;
  --display: "Silkscreen", "Courier New", monospace; --body: "Inter", system-ui, sans-serif; color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; color-scheme: dark }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }}
main {{ max-width: 1120px; margin: 0 auto; padding: 32px 16px 64px; display: grid; gap: 44px; }}
h1, h2, h3 {{ font-family: var(--display); font-weight: 400; letter-spacing: .02em; margin: 0; text-wrap: balance; }}
h1 {{ font-size: clamp(26px, 4vw, 38px); }}
h2 {{ font-size: 20px; color: var(--accent); }}
p {{ margin: 0; max-width: 72ch; }}
.lede {{ color: var(--muted); }}
section {{ display: grid; gap: 16px; }}
.plate {{ background: var(--plate); border-radius: 6px; padding: 12px; overflow-x: auto; }}
img {{ image-rendering: pixelated; display: block; max-width: 100%; height: auto; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 340px), 1fr)); gap: 20px; }}
.two {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 380px), 1fr)); gap: 20px; }}
figure {{ margin: 0; display: grid; gap: 8px; align-content: start; }}
.state img {{ background: var(--plate); padding: 8px; border-radius: 6px; width: 100%; }}
figcaption {{ display: grid; gap: 2px; font-size: 14px; }}
figcaption span {{ color: var(--muted); }}
ul.list, ol.flow {{ margin: 0; padding-left: 22px; display: grid; gap: 6px; max-width: 80ch; }}
ul.decisions {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 8px; max-width: 80ch; }}
ul.decisions li {{ border-left: 3px solid var(--gold); padding-left: 12px; }}
ol.q {{ margin: 0; padding-left: 24px; display: grid; gap: 14px; max-width: 80ch; }}
ol.q li::marker {{ color: var(--accent); font-weight: 600; }}
ol.q p {{ color: var(--muted); margin-top: 2px; }}
ol.q p b {{ color: var(--fg); }}
.tag {{ justify-self: start; font-family: var(--display); font-size: 11px; padding: 2px 8px; border-radius: 999px; background: var(--gold); color: #26243a; }}
.rule {{ display: grid; grid-template-columns: minmax(0, 720px) minmax(0, 1fr); gap: 24px; align-items: start; }}
.rule ul {{ margin: 0; padding-left: 18px; display: grid; gap: 8px; }}
table {{ border-collapse: collapse; font-size: 14px; width: 100%; max-width: 640px; }}
td {{ border-bottom: 1px solid var(--line); padding: 4px 8px 4px 0; vertical-align: top; }}
td:nth-child(2) {{ text-align: right; font-variant-numeric: tabular-nums; padding-right: 16px; }}
td:nth-child(3) {{ color: var(--muted); }}
code {{ font-size: 13px; }}
details {{ border: 1px solid var(--line); border-radius: 6px; padding: 12px 16px; }}
details > summary {{ cursor: pointer; font-family: var(--display); font-size: 14px; }}
details[open] > summary {{ margin-bottom: 16px; }}
@media (max-width: 860px) {{ .rule {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>
</head>
<body>
<main>
  <header style="display:grid;gap:10px">
    <span class="tag">Design review · round 2</span>
    <h1>Tosa Rail Review</h1>
    <p class="lede">Train travel between visited stations. This round answers “what if the map was bigger,
    and would it move to frame the selected station?” Every plate is rendered at the GBA's 240×160 with
    the game's own fonts, in the Orchid UI kit (Gen 5 layout, Gen 3 pixels), then scaled 3×. Station names
    other than TOSA PORT and TELOK TOWN are placeholders.</p>
  </header>

  <section>
    <h2>Changes since round 1</h2>
    <ul class="list">{changes}</ul>
  </section>

  <section>
    <h2>Decisions</h2>
    <ul class="decisions">{decisions}</ul>
  </section>

  <section>
    <h2>How it works</h2>
    <ol class="flow">{flow}</ol>
  </section>

  <section>
    <h2>Bigger map</h2>
    <p>The whole virtual canvas, with the 240×112 map viewport of each framing below outlined. Lines: COAST
    (teal) along the south, RIDGE (purple) north from VALE JUNCTION, FOREST (green) from ELDER WOOD to KORU
    CITY. The interchanges are VALE JUNCTION, TELOK TOWN and KORU CITY.</p>
    <div class="plate">{img("big_overview_2x.png", "Whole network canvas with three viewport framings")}</div>
    <div class="grid">{figs(BIG_STILLS)}</div>
  </section>

  <section>
    <h2>Camera rule: dead zone + re-centre</h2>
    <div class="rule">
      <div class="plate">{img("big_4_rule_3x.png", "Dead zone debug view")}</div>
      <ul>
        <li><b>Dead zone</b> (dashed): 48px in from each side, 24 from the top, and 32 from the bottom, so a label under a node still fits. While the selected station stays inside it, the diagram holds still.</li>
        <li><b>Leaving it</b> re-centres on the new station: 16 frames, ease-out, clamped to the canvas. The ring travels at the same time (8 frames, ease-out), so the pan and the hop read as one move.</li>
        <li><b>On open</b> the camera centres on the cursor station, clamped to the canvas.</li>
        <li>Header and tray never move. The grid follows the pan, so the paper moves with the diagram.</li>
      </ul>
    </div>
    <p>The animation below walks the network: MARIS BAY → VALE (no pan) → TELOK (pan up) → ASHEN PASS (pan)
    → a press toward greyed CINDER PEAK (denied) → back to TELOK → VALE → SALT FLATS → KORU CITY (pan east) → A.</p>
    <div class="plate" style="max-width:744px">{img("big_nav_3x.gif", "Animated cursor walk with camera pans")}</div>
  </section>

  <section>
    <h2>Finding the rest of the map</h2>
    <div class="two">{figs(FIND)}</div>
  </section>

  <section>
    <h2>GBA budget (scrolling version)</h2>
    <ul class="list">{budget}</ul>
  </section>

  <section>
    <h2>Journey storyboard</h2>
    <p>Built with the final <code>graphics/train/train.png</code>, read as-is: pieces [rear car][boarding car][loco],
    with the door-open piece swapped in for the boarding car. The door is at x 88–103 from the train's left
    edge. The train is parked at the start, and after you get off it leaves. The camera is fixed.</p>
    <div class="plate" style="max-width:744px">{img("journey_3x.gif", "Journey storyboard animation")}</div>
    <div class="plate">{img("journey_storyboard.png", "Journey key frames")}</div>
    <p>Phase lengths in GBA frames. Rows marked “engine” match the C values; the rest are proposed beats.
    Ease curves here are quadratic.</p>
    <table>{timing_rows}</table>
  </section>

  <section>
    <h2>Open questions</h2>
    <ol class="q">{qs}</ol>
  </section>

  <details>
    <summary>Round 1 screens (layout A chosen)</summary>
    <div class="grid">{figs(R1)}</div>
    <div class="plate" style="max-width:744px;margin-top:16px">{img("map_nav_3x.gif", "Round 1 navigation animation")}</div>
  </details>
</main>
</body>
</html>
"""
    open(os.path.join(OUT, "review.html"), "w").write(page)
    print("wrote", os.path.join(OUT, "review.html"), "%.1f KB" % (len(page) / 1024))


if __name__ == "__main__":
    main()
