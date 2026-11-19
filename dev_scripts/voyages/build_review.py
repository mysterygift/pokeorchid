#!/usr/bin/env python3
"""Assemble the single design-review page for Wavebreak Voyages.

Copies the chosen mockup PNGs into review/img/ and writes review/index.html (published as an Artifact
with review/img/* as supporting files). Re-run after any batch changes.
usage: python3 dev_scripts/voyages/build_review.py
"""
import glob, html, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
REV = os.path.join(HERE, "review")
IMG = os.path.join(REV, "img")

def g(*pats):
    res = []
    for p in pats:
        hits = sorted(glob.glob(os.path.join(OUT, p)))
        res += hits
    return res

def nice(path):
    b = os.path.basename(path).rsplit(".", 1)[0]
    for s in ("@2x", "@3x", "@4x", "_x3", "_vs_frlg"):
        b = b.replace(s, "")
    return b.replace("_", " ")

# (section id, title, intro html, [(image path, caption)], decisions list, open list)
SECTIONS = [
    ("voyage", "The voyage", """
<p>After the Champion is beaten (<code>FLAG_SYS_GAME_CLEAR</code>), the Sailor in the Wavebreak hut takes passcodes on the
<em>Enter code</em> naming screen. Each correct code unlocks a destination for good; his menu then lists every unlocked place.
The trip plays Emerald's ferry cutscene with Mr. Briney's boat in place of the ferry, and he waits at each destination's dock to sail you back.</p>
<table class="codes"><tr><th>Destination</th><th>Passcode</th><th>Highlights</th></tr>
<tr><td>Eon Island</td><td><code>SOULDEW</code></td><td>Latias by day, Latios by night; their Mega Stones appear only after a catch</td></tr>
<tr><td>Sevii Islands</td><td><code>SEAGALLOP</code></td><td>Islands 1–7, FRLG layouts in Emerald tiles</td></tr>
<tr><td>Holon</td><td><code>DELTA</code></td><td>Delta species, Holon Researchers, Cynthia at Holon Lake</td></tr>
<tr><td>Newmoon Island</td><td><code>NIGHTMARE</code></td><td>Darkrai</td></tr>
<tr><td>Fullmoon Island</td><td><code>LUNARWING</code></td><td>Cresselia</td></tr></table>
<p class="small">Codes are case-insensitive and live in one table. A fainted legendary returns on your next voyage.</p>""",
     [], ["Ferry cutscene with Briney's boat sprite", "Case-insensitive codes", "Fainted legendaries return next voyage"], []),
    ("wavebreak", "Wavebreak Town", "<p>Only the south-west corner of your hand-edited map changes. TosaPort gains 12 metatiles / 15 tiles (dock, fish crates, rods, buckets); no palette edits.</p>",
     [(p, c) for p, c in [
        (OUT + "/batch1/wavebreak_after@2x.png", "After: red-roof hut (the only red roof), Briney's wooden dock, fishermen"),
        (OUT + "/batch1/wavebreak_beach_3x.png", "Beach close-up: crates of fish, rods, buckets"),
        (OUT + "/batch1/tosaport_addition_closeup_4x.png", "New TosaPort pieces at 4x"),
        (OUT + "/batch1/sailor_hut_int@2x.png", "Hut interior: Mr. Briney's cottage, Sailor + Son"),
     ]], ["All three town houses purple; hut red", "Briney's wooden dock (Rustboro metatiles appended to TosaPort)", "Extra fishermen, crates, rods, 3/4-view buckets with blue water"], []),
    ("islands", "Eon, Newmoon and Fullmoon", "<p>Eon Island reuses Southern Island. Newmoon is General + Dewford with Shade weather; Fullmoon is General + Rustboro.</p>",
     [(OUT + "/batch1/eon_ext@2x.png", "Eon Island exterior"), (OUT + "/batch1/eon_int@2x.png", "Eon Island interior: Lati spot + both Mega Stone spots"),
      (OUT + "/batch1/newmoon_ext@2x.png", "Newmoon Island"), (OUT + "/batch1/newmoon_int@2x.png", "Newmoon interior: Darkrai"),
      (OUT + "/batch1/fullmoon_ext@2x.png", "Fullmoon Island"), (OUT + "/batch1/fullmoon_int@2x.png", "Fullmoon interior: Cresselia")],
     ["Latias/Latios by time of day, separate visits", "Newmoon never on Fallarbor tiles"], []),
    ("sevii13", "Sevii Islands 1–3", "<p>Faithful FRLG layouts re-tiled in Emerald (FRLG left, Emerald right, same size). Invented Sea Routes A/B link the islands, walled by sea rocks.</p>",
     [(OUT + "/batch2/overview.png", "Region-map geography and the translated maps")] + [(p, nice(p)) for p in g("batch2/*_vs_frlg.png")],
     ["Cape Brink uses Route 119's animated waterfall", "Lone rocks → General boulders; smash rocks → breakable-rock objects", "One Centre on One Island (= Net Center)", "Game Corner = flower shop exterior + Mauville Game Corner interior", "Mt. Ember terraces: you repaint later"], []),
    ("sevii47", "Sevii Islands 4–7", "<p>Same translation method. Sea Routes C/D link 4↔5 and 6↔7. Icefall Cave uses Shoal Cave ice; Tanoby Ruins keeps its name.</p>",
     [(OUT + "/batch3/overview.png", "Overview")] + [(p, nice(p)) for p in g("batch3/*_vs_frlg.png")] + [(OUT + "/batch3/icefall_ice_compare.png", "Icefall ice look (Shoal Cave chosen)")],
     ["Icefall Cave: Shoal Cave ice, exit mat 0x386", "Rocket Warehouse interior: New Mauville placeholder"], []),
    ("seviitiles", "gTileset_SeviiIslands", "<p>A Rustboro copy used only by Sevii maps, so Southern Island, Faraway Island and Route 104 are untouched.</p>",
     [(p, nice(p)) for p in g("batch3/tileset/*.png")], ["Cottage variants", "Market stall: rare items at high prices", "Onix tails, Dotted Hole door + pillars, Tanoby art reused from Tanoby Delta"], []),
    ("interiors", "Sevii interiors", "<p>Translated from FRLG like the outdoor maps.</p>",
     [(p, nice(p)) for p in g("interiors/*_vs_frlg.png")], [], []),
    ("holon", "Holon", "<p>All outdoor maps on gTileset_Holon (a Fortree copy) with a palettes-only General copy for the drained greens. The Research Tower is the Weather Institute.</p>",
     [(OUT + "/batch4/overview.png", "Mirage Forest coast, Holon Village, Holon Lake, Research Tower 1F/2F"),
      (OUT + "/batch4/holon_new_art_4x.png", "New art: blue-grey rock, sealed carved dome, lake pillar, carved stone, sphere, rail"),
      (OUT + "/batch4/holon_green_compare@2x.png", "Greens: primary + secondary desaturated (chosen, right)")],
     ["Desaturated greens with drained rings around the tower and pillar island", "Grass-rustle/footprint effects desaturated on Holon maps", "No dead trees; no three small domes"], []),
    ("delta", "Delta species", "<p>Separate species named <code>Name-δ</code>, appended after Laomeow. Tier A (57 species / 21 lines) ships first.</p>",
     [(OUT + "/batch5_delta/delta_table.png", "Delta table"), (OUT + "/batch5_delta/palettes_2x.png", "Recolours"),
      (OUT + "/batch5_delta/glyph_closeup.png", "δ at byte 0x18 in all 9 fonts"), (OUT + "/batch5_delta/ui_overview.png", "Names on battle, summary, party, PC, Pokédex"),
      (OUT + "/batch5_delta/wild_tables.png", "Holon wild tables")],
     ["All recommendations accepted (eggs, STAB moves, diploma exclusion, Eevee-δ gift, shiny Gyarados-δ)"], []),
    ("trainers", "Cynthia and the Holon Researcher", "<p>Cynthia's sprites are by lichen (credited). After Holon Lake she moves to the Battle Café in Changu City for rematches.</p>",
     [(OUT + "/batch5_trainers/cynthia_battle_intro_lake_x3.png", "Cynthia battle intro"), (OUT + "/batch5_trainers/cynthia_ow_palette_candidates.png", "OW palettes (npc_white chosen)"),
      (OUT + "/batch5_trainers/holon_researcher_compare.png", "Holon Researcher (brown slacks)"), (OUT + "/batch5_trainers/intro_textbox_sheet.png", "Battle intro text with the long class name")],
     ["Team: Spiritomb, Roserade, Togekiss (Life Orb), Lucario (King's Rock), Milotic, Mega Garchomp; Lv 70–74", "Champion mugshot", "Class name widened to 17"], []),
    ("regionmaps", "Region maps", "<p>Eon Island is the Hoenn map under Emerald's intro clouds; Sevii uses the FRLG art; Holon and the moons are placeholders.</p>",
     [(OUT + "/batch6_regionmap/eon_dense_screen@3x.png", "Eon Island"), (OUT + "/batch6_regionmap/sevii_screens.png", "Sevii Islands"),
      (OUT + "/batch6_regionmap/placeholders_screens.png", "Holon, Newmoon, Fullmoon placeholders")],
     ["No Eon place marker", "Fly only within the current Sevii cluster", "Phone R switch disabled on voyages"], []),
    ("cafe", "Battle Café", "<p>Changu City's café, on its own tileset copy (gTileset_ChanguCafe). The barista only welcomes you.</p>",
     [(OUT + "/batch7_cafe/changu_after@2x.png", "Changu City with the café"), (OUT + "/batch7_cafe/cafe_int_A@2x.png", "Interior, variant A")],
     ["Name: Battle Café", "Red roof", "Variant A: deep-red walls, charcoal floor"], []),
]

OPEN = [
 "<b>Extra Sevii dungeons.</b> The interior pass also translated Ruby Path B1F–B5F, Dotted Hole B1F–Sapphire Room and all seven Tanoby chambers. Keep them, or seal those entrances for now? <i>Recommend: keep the translated maps but seal Dotted Hole and the Tanoby chambers until there's content for them.</i>",
 "<b>Market stall prices.</b> Selling rare items at high prices needs a per-shop price multiplier. <i>Recommend: a small special that doubles/triples prices for this one shop.</i>",
 "<b>Rocket Warehouse grunts.</b> FRLG's Rocket sprites are invisible in Emerald, so they're exported as Team Aqua grunts for now. Keep Aqua, or use Orchid's own villain team when it exists?",
 "<b>Water Path's pale path.</b> Port it too? It costs no new tiles. <i>Recommend yes.</i>",
 "<b>Mt. Ember arrow warps.</b> They sit on the shared Lavaridge tileset, so adding arrow-warp tiles would touch other maps. <i>Recommend plain warps there.</i>",
 "<b>gTileset_SeviiIslands.</b> Approve the Sevii-only Rustboro copy: 164 new tiles (237 left), 471/512 metatiles, palette slots 6, 7, 12.",
]

CSS = """
:root{--bg:#f3f4f2;--panel:#ffffff;--ink:#1d2321;--muted:#5d6763;--line:#d7dcd8;--accent:#2f7a5b;--tag:#e6f1ec;
--display:'Space Grotesk',system-ui,sans-serif;--body:'Inter',system-ui,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141816;--panel:#1c211f;--ink:#e6ebe8;--muted:#9aa49f;--line:#2e3532;--accent:#6cc79f;--tag:#203229;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141816;--panel:#1c211f;--ink:#e6ebe8;--muted:#9aa49f;--line:#2e3532;--accent:#6cc79f;--tag:#203229;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:1180px;margin:0 auto;padding-block:28px 64px}
h1,h2{font-family:var(--display);text-wrap:balance;line-height:1.15}
h1{font-size:2rem;margin:0 0 6px}
h2{font-size:1.45rem;margin:0 0 8px}
.lede{color:var(--muted);max-width:68ch;margin:0}
nav{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);z-index:5;padding-block:10px;border-bottom:1px solid var(--line);margin:18px 0 8px;display:flex;flex-wrap:wrap;gap:6px}
nav a{font-size:.82rem;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:3px 10px;background:var(--panel)}
nav a:hover,nav a:focus-visible{border-color:var(--accent);outline:none}
section{padding-block:26px;border-bottom:1px solid var(--line)}
section p{max-width:72ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;margin-top:14px}
figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px;min-width:0}
figure img{display:block;width:100%;height:auto;image-rendering:pixelated;border-radius:3px;background:#000}
figure a{display:block}
figcaption{font-size:.82rem;color:var(--muted);margin-top:6px}
.wide{grid-column:1/-1}
ul.dec{list-style:none;padding:0;margin:12px 0 0;display:flex;flex-wrap:wrap;gap:6px}
ul.dec li{background:var(--tag);color:var(--ink);border-radius:4px;padding:3px 9px;font-size:.82rem}
ul.dec li::before{content:"✓ ";color:var(--accent);font-weight:600}
table.codes{border-collapse:collapse;margin:12px 0;font-size:.9rem;display:block;overflow-x:auto}
table.codes th,table.codes td{border-bottom:1px solid var(--line);padding:6px 12px 6px 0;text-align:left;vertical-align:top}
code{font-family:var(--mono);font-size:.88em}
.small{font-size:.85rem;color:var(--muted)}
.open{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 16px}
@media (prefers-reduced-motion:no-preference){figure{transition:border-color .15s}figure:hover{border-color:var(--accent)}}
"""

def main():
    if os.path.isdir(IMG):
        shutil.rmtree(IMG)
    os.makedirs(IMG)
    used = {}
    parts = []
    nav = []
    for sid, title, intro, imgs, decided, open_ in SECTIONS:
        nav.append(f'<a href="#{sid}">{html.escape(title)}</a>')
        figs = []
        for path, cap in imgs:
            if not os.path.exists(path):
                continue
            name = os.path.relpath(path, OUT).replace("/", "__")
            shutil.copy(path, os.path.join(IMG, name))
            used[name] = True
            wide = " wide" if any(k in name for k in ("overview", "compare", "table", "screens", "sheet", "_vs_frlg")) and "interiors" not in name else ""
            figs.append(f'<figure class="{wide.strip()}"><a href="img/{name}" target="_blank" rel="noopener"><img loading="lazy" src="img/{name}" alt="{html.escape(cap)}"></a><figcaption>{html.escape(cap)}</figcaption></figure>')
        dec = "".join(f"<li>{html.escape(d)}</li>" for d in decided)
        parts.append(f'<section id="{sid}"><h2>{html.escape(title)}</h2>{intro}'
                     + (f'<ul class="dec">{dec}</ul>' if dec else "")
                     + (f'<div class="grid">{"".join(figs)}</div>' if figs else "") + "</section>")
    openq = "".join(f"<li>{q}</li>" for q in OPEN) or "<li>None outstanding. Approve to start building.</li>"
    page = f"""<title>Wavebreak Voyages</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@500;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
<h1>Wavebreak Voyages</h1>
<p class="lede">Design review for Orchid's post-game boat trips: every mockup, the decisions taken so far, and what's left to decide before building. Click any image to open it full size.</p>
<nav>{''.join(nav)}<a href="#open">Open questions</a></nav>
{''.join(parts)}
<section id="open"><h2>Open questions</h2><div class="open"><ul>{openq}</ul></div></section>
</div>"""
    with open(os.path.join(REV, "index.html"), "w") as f:
        f.write(page)
    print(len(used), "images")

if __name__ == "__main__":
    main()
