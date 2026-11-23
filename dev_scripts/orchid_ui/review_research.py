"""Design-review page: Palm's research tasks + Habitats round 4. usage: review_research.py MOCK_DIR OUT_HTML"""
import base64
import os
import sys

MOCK, OUT = sys.argv[1], sys.argv[2]


def img(name, alt):
    data = base64.b64encode(open(os.path.join(MOCK, name), "rb").read()).decode()
    return f'<img class="shot" src="data:image/png;base64,{data}" alt="{alt}">'


def fig(name, title, desc):
    return (f'<figure class="card"><div class="mat">{img(name, title)}</div>'
            f'<figcaption><b>{title}</b><span>{desc}</span></figcaption></figure>')


RESEARCH = [
    ("r1_list.png", "QUESTS: new Research tab",
     "Research tasks sit beside story quests (L/R tabs; a clipboard icon marks the new tab). The header swaps the quest "
     "count for your Research Rank (stars) and research points (RP). Progress counts sit on each row; the usual "
     "tags apply (new / active / reward / done / locked)."),
    ("r3_steps.png", "Zone survey steps",
     "A zone survey has one step per habitat. A step completes when every species there is catalogued, day and "
     "night. The tray shows that habitat's progress."),
    ("r2_request.png", "Palm's requests",
     "Short one-off tasks Palm asks for: catalogue one particular species, often a rare or night-only one."),
    ("r4_reward.png", "Ready to claim", "A finished task shows the gift tag; the tray says Ⓐ Send to Palm."),
    ("r5_claim.png", "Claimed in the app", "Palm sends the reward straight away: items plus research points. No trip back to the lab."),
    ("r6_rank.png", "Rank up", "Research points raise your rank (5 ranks). Each rank-up comes with a line from Palm."),
    ("r7_hab_map.png", "Habitats map: request markers", "A clipboard sits on habitats where Palm has an open request."),
    ("r8_hab_route.png", "Habitats route: requested species",
     "The requested species' well gets a clipboard, and the tray says what Palm wants."),
    ("r9_buzz.png", "In the field: Rotom buzzes",
     "Finishing a task triggers the existing Rotom buzz with the task name. You claim it whenever you next open QUESTS."),
]
HABITATS = [
    ("h1_locked.png", "Locked rows",
     "Methods you can't use yet get a padlock tab on the chip and greyed wells with a padlock. The tray says what's "
     "needed (Needs Surf / Needs a Super Rod)."),
    ("h2_rare.png", "Rare slots as \"?\"",
     "An unseen species whose share is 5% or less shows \"?\" instead of its silhouette, so you know something rare is "
     "there without seeing what it is."),
]
DONE = [
    "<b>Back navigation (built + tested):</b> A on a species opens its entry; B now goes straight back to the same "
    "route page with the cursor where it was. Then B → map → list as before.",
    "<b>Delta Glaceon / Leafeon (built):</b> their location evolutions now happen at Holon Lake (Glaceon) and Holon "
    "Mirage Forest (Leafeon); Ice Stone / Leaf Stone still work anywhere. If you meant wild encounters on the Holon map "
    "instead, say so and I'll add them to its tables.",
    "<b>DexNav:</b> dropped, as you asked.",
]
QUESTIONS = [
    ("Task set",
     "Each zone gets a <b>survey</b> (catalogue every route, day and night) and a <b>night watch</b> (catalogue the zone's "
     "night-only species), plus about 10 hand-written <b>Palm requests</b> to start with. <b>Recommendation:</b> this set; "
     "I write placeholder request text, and you rewrite it later."),
    ("Rewards",
     "<b>Recommendation:</b> claimed in the app (Send to Palm). Surveys give a ball bundle and an evolution item scaled "
     "to the zone; night watches a Moon Stone or Dusk Balls; requests a small item; all tasks give RP."),
    ("Research Rank",
     "Five ranks (Field Assistant → Junior Researcher → Researcher → Senior Researcher → Palm's Partner) at set RP. "
     "<b>Recommendation:</b> each rank-up comes with a gift from Palm and no other unlocks for now."),
    ("When it appears",
     "<b>Recommendation:</b> the Research tab appears once you get the Pokédex (FLAG_SYS_POKEDEX_GET)."),
    ("Night behaviour",
     "<b>Recommendation:</b> at night every wild slot is +2 levels, and wild Pokémon have a 1-in-10 chance of their "
     "Hidden Ability (none by day). The route tray shows a small moon when a species behaves differently at night."),
    ("What locks a row",
     "<b>Recommendation:</b> Surfing rows locked until you can use Surf; Rock Smash until you can use Rock Smash; "
     "fishing wells locked per rod (Old / Good / Super) until you own that rod."),
    ("Rare threshold",
     "<b>Recommendation:</b> 5% or less (the 4% / 1% grass slots, and rod slots of 4% / 1%)."),
]


def main():
    grid = lambda items: '<div class="grid">' + "".join(fig(*i) for i in items) + "</div>"
    html = f"""<title>Palm's Research Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Silkscreen&family=Inter:wght@400;600&display=swap">
<style>
/* Layout: one reading column of pixel-art plates on dark mats, then decisions and questions. */
:root {{ --bg: #f1eef4; --fg: #26243a; --muted: #65617a; --plate: #1d1b29; --line: #d6d0de; --accent: #8c58b8;
  --display: "Silkscreen", "Courier New", monospace; --body: "Inter", system-ui, sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg: #15131d; --fg: #ece8f2; --muted: #a39db5; --plate: #0c0b12; --line: #2f2b3d; --accent: #c49ae6; color-scheme: dark }}
body {{ background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }}
main {{ max-width: 1120px; margin: 0 auto; padding-block: 32px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 44px; }}
h1, h2 {{ font-family: var(--display); font-weight: 400; letter-spacing: .02em; margin: 0; text-wrap: balance; }}
h1 {{ font-size: 28px; }} h2 {{ font-size: 19px; color: var(--accent); }}
header p, section > p {{ color: var(--muted); max-width: 70ch; margin: 8px 0 0; }}
section {{ display: grid; gap: 16px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 440px), 1fr)); gap: 24px; }}
.card {{ margin: 0; display: grid; gap: 10px; min-width: 0; align-content: start; }}
.mat {{ background: var(--plate); border-radius: 6px; padding: 10px; }}
.shot {{ display: block; width: 100%; height: auto; image-rendering: pixelated; }}
figcaption {{ display: grid; gap: 2px; }} figcaption span {{ color: var(--muted); font-size: 14px; }}
ol, ul {{ margin: 0; padding-left: 1.3em; display: grid; gap: 10px; max-width: 80ch; }}
</style>
<main>
<header><h1>Palm's Research · round 1</h1>
<p>Professor Palm's field notes, built on Habitats. Tasks are worked out from the dex (seen / captured / catalogued
per habitat, day and night), so they track themselves; the save only records claimed rewards and your rank. Mockups are
240×160 at 3× in the Orchid kit; species and habitats come from the real tables, catch states from a sample save.</p></header>
<section><h2>Done since round 3</h2><ul>{"".join(f"<li>{d}</li>" for d in DONE)}</ul></section>
<section><h2>Research tasks</h2>{grid(RESEARCH)}</section>
<section><h2>Habitats additions</h2>{grid(HABITATS)}</section>
<section><h2>Open questions</h2><p>Each has a recommendation; "use your suggestions" accepts them all.</p>
<ol>{"".join(f"<li><b>{t}.</b> {d}</li>" for t, d in QUESTIONS)}</ol></section>
</main>
"""
    open(OUT, "w").write(html)


if __name__ == "__main__":
    main()
