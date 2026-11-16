"""Build the design-review HTML page from rendered mockups. usage: review_page.py MOCK_DIR OUT_HTML"""
import base64
import os
import sys

MOCK, OUT = sys.argv[1], sys.argv[2]


def img_gif(name, alt):
    data = base64.b64encode(open(os.path.join(MOCK, name), "rb").read()).decode()
    return f'<img class="shot" src="data:image/gif;base64,{data}" alt="{alt}">'


def img(name, alt, cls="shot"):
    data = base64.b64encode(open(os.path.join(MOCK, name), "rb").read()).decode()
    return f'<img class="{cls}" src="data:image/png;base64,{data}" alt="{alt}">'


STATES = [
    ("Items pocket, browsing", "Male theme. Gold pill on the selected row; thumb at the top of the scrollbar."),
    ("Poké Balls, short pocket", "Female theme. Rows past the end show the backdrop."),
    ("Item selected", "Context menu uses the new Orchid frame; the tray shows the prompt."),
    ("Message", "Dialogue box variant with accent end-caps."),
    ("TMs & HMs", "Number + move name; no quantity."),
    ("Key Items", "Registered item shows a SELECT tag where the quantity would be."),
    ("Scrolled", "List scrolled by 2; thumb has moved down the track."),
]

QUESTIONS = []

CHANGES = [
    "Backdrop is now a Black/White-style scrolling grid: near-black with light 1px lines every 16px and faint lines at 8px, drifting diagonally on its own layer.",
    "Poké Ball centre button moved up so the black band runs through it.",
    "New animated preview below: the grid scroll and the pocket switch (gold ring slides to the new pocket, satchel shakes, rows wipe in).",
]


def main():
    states = "\n".join(
        f'<figure class="state">{img(f"bag_state_{i+1}.png", t)}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>'
        for i, (t, d) in enumerate(STATES))
    qs = "\n".join(f"<li><b>{t}.</b> {d}</li>" for t, d in QUESTIONS)
    changes = "\n".join(f"<li>{c}</li>" for c in CHANGES)
    html = f"""<title>Satchel Bag Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen&family=Inter:wght@400;600&display=swap">
<style>
/* Layout: one reading column of pixel-art plates; each plate is shown at an integer scale on a dark mat. */
:root {{
  --bg: #f1eef4; --fg: #26243a; --muted: #65617a; --plate: #1d1b29; --line: #d6d0de; --accent: #8c58b8; --gold: #f0c850;
  --display: "Silkscreen", "Courier New", monospace; --body: "Inter", system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; --gold: #f0c850; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; --gold: #f0c850; color-scheme: dark }}
body {{ background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }}
main {{ max-width: 1120px; margin: 0 auto; padding-block: 32px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 40px; }}
h1, h2 {{ font-family: var(--display); font-weight: 400; letter-spacing: .02em; text-wrap: balance; margin: 0; }}
h1 {{ font-size: clamp(26px, 4vw, 38px); }}
h2 {{ font-size: 20px; color: var(--accent); }}
p {{ margin: 0; max-width: 68ch; }}
.lede {{ color: var(--muted); }}
section {{ display: grid; gap: 16px; }}
.plate {{ background: var(--plate); border-radius: 6px; padding: 16px; overflow-x: auto; }}
img {{ image-rendering: pixelated; display: block; max-width: 100%; height: auto; }}
.hero {{ display: grid; grid-template-columns: minmax(0, 720px) minmax(0, 1fr); gap: 24px; align-items: start; }}
.zones {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }}
.zones li {{ border-left: 3px solid var(--line); padding-left: 12px; }}
.zones b {{ display: block; font-family: var(--display); font-weight: 400; font-size: 13px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
figure {{ margin: 0; display: grid; gap: 8px; }}
.state img {{ background: var(--plate); padding: 8px; border-radius: 6px; width: 100%; }}
figcaption {{ display: grid; gap: 2px; font-size: 14px; }}
figcaption span {{ color: var(--muted); }}
.changes {{ margin: 0; padding-left: 20px; display: grid; gap: 6px; max-width: 75ch; }}
ol.q {{ margin: 0; padding-left: 22px; display: grid; gap: 10px; max-width: 75ch; }}
ol.q li::marker {{ color: var(--accent); font-weight: 600; }}
.notes {{ display: grid; gap: 8px; max-width: 75ch; padding: 16px; border: 1px solid var(--line); border-radius: 6px; }}
.notes b {{ color: var(--accent); }}
.tag {{ display: inline-block; font-family: var(--display); font-size: 11px; padding: 2px 8px; border-radius: 999px; background: var(--gold); color: #26243a; }}
@media (max-width: 860px) {{ .hero {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>
<main>
  <header style="display:grid;gap:10px">
    <span class="tag">Design review · v4 mockups</span>
    <h1>Satchel Bag Review</h1>
    <p class="lede">Black/White's bag layout (pocket wheel, pill rows, scrolling grid backdrop) drawn with Gen 3 pixel rules: 1px ink outlines, top-left bevels, 3-step ramps, BGR555 colours. Every plate is rendered at the GBA's 240×160 with the game's own fonts and real tile and palette limits, then scaled 3×.</p>
  </header>

  <section>
    <h2>Changes since review 3</h2>
    <ul class="changes">{changes}</ul>
  </section>

  <section>
    <h2>Main screen</h2>
    <div class="hero">
      <div class="plate">{img("bag_state_1.png", "Bag screen, items pocket")}</div>
      <ul class="zones">
        <li><b>Pocket wheel</b>Satchel in the centre, five pocket buttons on the ring. Gold = current pocket.</li>
        <li><b>Header tab</b>Pocket name with small Gen 3 red chevrons for L/R.</li>
        <li><b>Pill rows</b>Six rows on BG art. The gold pill is the cursor; it's a palette swap, so it costs no tiles.</li>
        <li><b>Scrollbar</b>Recessed track, gold thumb sprite.</li>
        <li><b>Info tray</b>Item icon in a round well, three-line description, stitched seam.</li>
        <li><b>Budget</b>BG2: 124 of 320 tiles. BG palettes 0–2 (normal / selected / empty).</li>
      </ul>
    </div>
  </section>

  <section>
    <h2>In motion</h2>
    <p>Real game timing at 60 fps, shown at 2×. The grid drifts 1px every 4 frames. Pressing R twice, then L: the gold ring slides along the wheel to the new pocket, the satchel drops in closed with a Gen 3 wiggle and opens on that pocket's item, and the rows wipe in top to bottom before the text returns.</p>
    <div class="plate" style="max-width:512px">{img_gif("bag_anim.gif", "Animated bag: grid scroll and pocket switching")}</div>
  </section>

  <section>
    <h2>Satchel and pocket buttons</h2>
    <p>Frame 0 is closed; frames 1–5 show each pocket's item peeking out. Rows 1–2 are the male palette, rows 3–4 female. The bottom block compares each item with the real in-game icon.</p>
    <div class="plate">{img("satchel_sheet.png", "Satchel frames and pocket buttons")}</div>
  </section>

  <section>
    <h2>States</h2>
    <div class="grid">{states}</div>
  </section>

  <section>
    <h2>Orchid UI kit</h2>
    <p>The bag is the first screen built from a shared kit. Every 16-colour palette uses the same role layout (ink, panel, accent ramp, gold select), so any piece re-themes by palette swap alone. The four themes below are the starting set.</p>
    <div class="plate">{img("review_kit.png", "UI kit pieces across four themes")}</div>
    <p>The same pieces carried into field windows: the start menu with icons and a gold selection pill, and a dialogue box with a YES/NO box in the standard frame.</p>
    <div class="plate">{img("review_field_windows.png", "Field windows in the Orchid theme")}</div>
    <p>All twelve start-menu icons on normal and selected pills. One shared 16-colour palette, with ramps taken from Gen 3 item icons (reference strip at the bottom).</p>
    <div class="plate" style="max-width:680px">{img("menu_icons_sheet.png", "Start menu icons")}</div>
  </section>

  <section>
    <h2>Interaction notes</h2>
    <div class="notes">
      <p><b>Pocket switch (L/R, ←/→).</b> The satchel shakes, and the gold circle travels along the ring from the old pocket button to the new one. The new button lights up when it arrives. Repeated presses retarget it mid-move.</p>
      <p><b>Pocket change.</b> The satchel's flap shows that pocket's item peeking out. Rows wipe in top to bottom, the same way Emerald repaints its list.</p>
      <p><b>Cursor move.</b> The gold pill follows the cursor; the satchel gives its small Gen 3 wiggle.</p>
    </div>
  </section>

  <section>
    <h2>Status</h2>
    <p>Every open question from reviews 1 and 2 is answered. Once this version is approved, implementation starts on the <code>bag-satchel</code> branch.</p>
  </section>
</main>
"""
    open(OUT, "w").write(html)


main()
