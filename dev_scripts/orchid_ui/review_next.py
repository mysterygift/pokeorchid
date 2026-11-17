"""
Build the design-review page for the next Orchid screens (summary, PC, Mart, options/save/start, trainer card).
usage: review_next.py OUT_ROOT OUT_HTML
OUT_ROOT holds one folder per area (summary/, pc/, mart/, options/, card/), each with notes.json + renders
(see the mockup brief for the notes.json schema), plus an optional OUT_ROOT/page.json:
{"round": 1, "changes": [...], "decisions": [...], "cross_questions": [[area, title, text], ...]}.
"""
import base64
import html
import json
import os
import sys

ROOT, OUT = sys.argv[1], sys.argv[2]
AREAS = [("summary", "Summary"), ("pc", "PC storage"), ("mart", "Poké Mart"), ("options", "Options, Save & Start"),
         ("card", "Trainer card")]
E = html.escape

PAGE = {}
_pj = os.path.join(ROOT, "page.json")
if os.path.exists(_pj):
    PAGE = json.load(open(_pj))
ROUND = PAGE.get("round", 1)


def data_uri(path):
    ext = os.path.splitext(path)[1][1:]
    return "data:image/%s;base64,%s" % (ext, base64.b64encode(open(path, "rb").read()).decode())


def img(area, f, alt, cls="shot"):
    p = os.path.join(ROOT, area, f)
    if not os.path.exists(p):
        return '<p class="missing">missing: %s</p>' % E(f)
    return '<img class="%s" src="%s" alt="%s" loading="lazy">' % (cls, data_uri(p), E(alt))


def area_section(key, name, n, qstart):
    p = os.path.join(ROOT, key, "notes.json")
    if not os.path.exists(p):
        return "", []
    N = json.load(open(p))
    zones = "".join("<li><b>%s</b>%s</li>" % (E(z), E(d)) for z, d in N.get("main", {}).get("zones", []))
    gifs = "".join(
        '<figure class="anim"><div class="plate">%s</div><figcaption><b>%s</b><span>%s</span></figcaption></figure>'
        % (img(key, g["file"], g["title"]), E(g["title"]), E(g["desc"])) for g in N.get("gifs", []))
    states = "".join(
        '<figure class="state">%s<figcaption><b>%s</b><span>%s</span></figcaption></figure>'
        % (img(key, s["file"], s["title"]), E(s["title"]), E(s["desc"])) for s in N.get("states", []))
    extras = "".join(
        '<figure class="extra"><div class="plate">%s</div><figcaption><b>%s</b><span>%s</span></figcaption></figure>'
        % (img(key, x["file"], x["title"]), E(x["title"]), E(x["desc"])) for x in N.get("extras", []))
    budget = "".join("<li>%s</li>" % E(b) for b in N.get("budget", []))
    kit = "".join("<li>%s</li>" % E(b) for b in N.get("kit_additions", []))
    qs = N.get("questions", [])
    qlinks = ", ".join('<a href="#q%d">%d</a>' % (qstart + i, qstart + i) for i in range(len(qs)))
    main_file = N.get("main", {}).get("file", "main.png")
    out = f"""
  <section class="area" id="{key}">
    <div class="area-head"><span class="num">{n}</span><h2>{E(N.get("title", name))}</h2></div>
    <div class="hero">
      <div class="plate">{img(key, main_file, name + " main screen")}</div>
      <ul class="zones">{zones}</ul>
    </div>
    {"<h3>In motion</h3><p class='hint'>Real game timing at 60 fps, shown at 2×.</p><div class='anims'>" + gifs + "</div>" if gifs else ""}
    <h3>States</h3>
    <div class="grid">{states}</div>
    {"<div class='extras'>" + extras + "</div>" if extras else ""}
    <div class="notes-row">
      <div class="notes"><h4>Hardware budget</h4><ul>{budget}</ul></div>
      <div class="notes"><h4>Proposed kit additions</h4><ul>{kit}</ul></div>
    </div>
    {"<p class='hint'>Open questions for this screen: " + qlinks + "</p>" if qs else ""}
  </section>"""
    return out, [(name, t, d) for t, d in qs]


CROSS_QUESTIONS = [tuple(q) for q in PAGE.get("cross_questions", [])]

CHANGES = PAGE.get("changes", [])

DECISIONS = PAGE.get("decisions", [
    "Carried over from the battle / party / Pokédex review: gold pill selection only (no ▶ arrow), Orchid purple on shared screens and gender themes on player-owned ones, near-black scrolling grid backdrop, small red Gen 3 chevrons, Gen 3 item-icon colours, pictogram status icons, gender shown by name colour, Tosa instead of HOENN, layered detail like healthbox B.",
])


def main():
    sections, questions = [], list(CROSS_QUESTIONS)
    for n, (key, name) in enumerate(AREAS, 1):
        s, qs = area_section(key, name, n, len(questions) + 1)
        sections.append(s)
        questions += qs
    qhtml = "".join('<li id="q%d"><span class="qa">%s</span><b>%s.</b> %s</li>' % (i + 1, E(a), E(t), E(d))
                    for i, (a, t, d) in enumerate(questions))
    toc = "".join('<a href="#%s">%s</a>' % (k, E(nm)) for k, nm in AREAS) + '<a href="#questions">Questions</a>'
    page = f"""<title>Orchid Summary, PC &amp; Mart</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen&family=Inter:wght@400;600&display=swap">
<style>
/* Layout: one reading column of pixel-art plates per screen area; plates sit on a dark mat at integer scale. */
:root {{
  --bg: #f1eef4; --fg: #26243a; --muted: #65617a; --plate: #1d1b29; --line: #d6d0de; --accent: #8c58b8; --gold: #f0c850; --chip-fg: #26243a;
  --display: "Silkscreen", "Courier New", monospace; --body: "Inter", system-ui, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; --gold: #f0c850; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; --gold: #f0c850; color-scheme: dark }}
body {{ background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }}
main {{ max-width: 1120px; margin: 0 auto; padding-block: 32px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 48px; }}
h1, h2, h3, h4 {{ font-family: var(--display); font-weight: 400; letter-spacing: .02em; text-wrap: balance; margin: 0; }}
h1 {{ font-size: clamp(26px, 4vw, 38px); }}
h2 {{ font-size: 22px; }}
h3 {{ font-size: 15px; color: var(--accent); margin-top: 8px; }}
h4 {{ font-size: 12px; color: var(--accent); }}
p {{ margin: 0; max-width: 68ch; }}
a {{ color: var(--accent); }}
.lede, .hint {{ color: var(--muted); }}
nav.toc {{ display: flex; flex-wrap: wrap; gap: 8px; }}
nav.toc a {{ font-family: var(--display); font-size: 12px; text-decoration: none; padding: 4px 12px; border: 1px solid var(--line); border-radius: 999px; color: var(--fg); }}
nav.toc a:hover, nav.toc a:focus-visible {{ border-color: var(--accent); outline: none; }}
section {{ display: grid; gap: 16px; }}
.area {{ border-top: 1px solid var(--line); padding-top: 24px; }}
.area-head {{ display: flex; align-items: center; gap: 12px; }}
.num {{ font-family: var(--display); font-size: 13px; width: 28px; height: 28px; display: grid; place-items: center; border-radius: 50%; background: var(--gold); color: var(--chip-fg); }}
.plate {{ background: var(--plate); border-radius: 6px; padding: 16px; overflow-x: auto; }}
img {{ image-rendering: pixelated; display: block; max-width: 100%; height: auto; }}
.hero {{ display: grid; grid-template-columns: minmax(0, 720px) minmax(0, 1fr); gap: 24px; align-items: start; }}
.zones {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }}
.zones li {{ border-left: 3px solid var(--line); padding-left: 12px; }}
.zones b {{ display: block; font-family: var(--display); font-weight: 400; font-size: 13px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
.anims, .extras {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 500px), 1fr)); gap: 20px; }}
figure {{ margin: 0; display: grid; gap: 8px; align-content: start; }}
.state img {{ background: var(--plate); padding: 8px; border-radius: 6px; width: 100%; }}
figcaption {{ display: grid; gap: 2px; font-size: 14px; min-width: 0; }}
figcaption span {{ color: var(--muted); }}
.notes-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 16px; }}
.notes {{ display: grid; gap: 8px; padding: 16px; border: 1px solid var(--line); border-radius: 6px; align-content: start; min-width: 0; }}
.notes ul {{ margin: 0; padding-left: 18px; display: grid; gap: 4px; font-size: 14px; }}
ol.q {{ margin: 0; padding-left: 26px; display: grid; gap: 12px; max-width: 80ch; }}
ol.q li::marker {{ color: var(--accent); font-weight: 600; }}
.qa {{ display: inline-block; font-family: var(--display); font-size: 10px; padding: 1px 8px; margin-right: 8px; border-radius: 999px; border: 1px solid var(--line); color: var(--muted); vertical-align: 2px; }}
.changes {{ margin: 0; padding-left: 20px; display: grid; gap: 6px; max-width: 80ch; }}
.next {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; max-width: 80ch; }}
.next li {{ border-left: 3px solid var(--line); padding-left: 12px; }}
.next b {{ display: block; font-family: var(--display); font-weight: 400; font-size: 13px; }}
.tag {{ display: inline-block; font-family: var(--display); font-size: 11px; padding: 2px 8px; border-radius: 999px; background: var(--gold); color: var(--chip-fg); justify-self: start; }}
.missing {{ color: var(--muted); font-style: italic; }}
code {{ font-size: 13px; }}
@media (max-width: 860px) {{ .hero {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>
<main>
  <header style="display:grid;gap:12px">
    <span class="tag">Design review · round {ROUND}</span>
    <h1>Orchid Summary, PC &amp; Mart</h1>
    <p class="lede">The next screens built from the approved Orchid UI kit: summary, PC storage, Poké Mart, options, save, start menu and trainer card, in Black/White structure drawn with Gen 3 pixel rules. Every plate is rendered at the GBA's 240×160 with the game's own fonts, real ROM sprites and real tile and palette limits, then scaled 3×. These are mockups only; nothing is implemented yet.</p>
    <nav class="toc">{toc}</nav>
  </header>
  <section>
    {"<h2>Changes since round %d</h2><ul class='changes'>%s</ul>" % (ROUND - 1, "".join("<li>%s</li>" % E(c) for c in CHANGES)) if CHANGES else ""}
    <h3>Settled so far</h3>
    <ul class="changes">{"".join("<li>%s</li>" % E(c) for c in DECISIONS)}</ul>
  </section>
  {"".join(sections)}
  <section id="questions">
    <h2>Open questions</h2>
    {"<p class='hint'>Answer by number. Each one names my recommendation.</p><ol class='q'>" + qhtml + "</ol>" if questions else "<p>None open. Every question from the previous round is answered; see Settled so far.</p>"}
  </section>
  <section>
    <h2>Status</h2>
    <p>Mockup scripts live beside the bag's in <code>dev_scripts/orchid_ui/</code> on the <code>bag-satchel</code> worktree (<code>mock_summary.py</code>, <code>mock_pc.py</code>, <code>mock_mart.py</code>, <code>mock_options.py</code>, <code>mock_system.py</code>, <code>mock_card.py</code>, each with its own <code>*_ext.py</code> helpers; nothing in the shared kit files changed). All screens on this page are approved; implementation follows on its own branch when you start it.</p>
  </section>
</main>
"""
    open(OUT, "w").write(page)
    print("questions:", len(questions), "bytes:", len(page))


main()
