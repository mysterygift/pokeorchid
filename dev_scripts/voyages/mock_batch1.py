"""
Render the batch-1 Sailor's Voyages mockups into dev_scripts/voyages/out/batch1/ (1x + @2x, with marks).

usage: <venv python> dev_scripts/voyages/mock_batch1.py [name ...]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import voyage_compose as vc   # noqa: E402
import specs_batch1 as sp     # noqa: E402
from PIL import Image, ImageEnhance   # noqa: E402

OUT = os.path.join(HERE, "out", "batch1")


def render_with_proposed(spec, out_base):
    """Like vc.render, but cells listed in spec['proposed'] are drawn from tileset_addition_batch1 (metatiles
    proposed for gTileset_TosaPort, not in the repo yet) before the marks go on top."""
    import tileset_addition_batch1 as add
    g = vc.build(spec)
    ts = tuple(spec["tileset"])
    for scale, suffix in ((1, ""), (2, "@2x")):
        im = vc.picture(g, ts, (), scale)
        T = 16 * scale
        for x, y, nm in spec["proposed"]:
            u, o = add.render(nm)
            c = u.copy()
            c.alpha_composite(o)
            im.paste(c.resize((T, T), Image.NEAREST), (x * T, y * T))
        vc._overlay(im, spec.get("marks", []), scale)
        im.convert("RGB").save(out_base + suffix + ".png")
    return g


def main(names):
    os.makedirs(OUT, exist_ok=True)
    if not names or "wavebreak_before" in names:
        vc.render_layout(sp.WB, os.path.join(OUT, "wavebreak_before"), sp.WAVEBREAK_BEFORE_MARKS)
    for name, spec in sp.ALL.items():
        if names and name not in names:
            continue
        vc.check_size(*spec["size"])
        g = render_with_proposed(spec, os.path.join(OUT, name)) if spec.get("proposed") else             vc.render(spec, os.path.join(OUT, name))
        print("%-22s %2dx%-2d %s/%s  %d metatiles" % (name, spec["size"][0], spec["size"][1],
                                                     spec["tileset"][0][9:], spec["tileset"][1][9:],
                                                     len(vc.metatile_ids(g))))
    if not names or "wavebreak_after" in names:
        # beach close-up at 3x (the @2x render, x0-17 y8-33, scaled by 1.5)
        im = Image.open(os.path.join(OUT, "wavebreak_after@2x.png"))
        im = im.crop((0, 8 * 32, 18 * 32, 34 * 32))
        im.resize((im.width * 3 // 2, im.height * 3 // 2), Image.NEAREST).save(
            os.path.join(OUT, "wavebreak_beach_3x.png"))
    for name in getattr(sp, "SHADE_PREVIEW", ()):
        if names and name not in names:
            continue
        # rough stand-in for WEATHER_SHADE (the game darkens the palettes at run time; nothing is edited)
        im = Image.open(os.path.join(OUT, name + "@2x.png")).convert("RGB")
        im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.8)).enhance(0.72)
        im.save(os.path.join(OUT, name + "_shade_sim@2x.png"))
    for name, (lid, marks) in getattr(sp, "AS_IS", {}).items():
        if names and name not in names:
            continue
        vc.render_layout(lid, os.path.join(OUT, name), marks)
        print("%-22s (as is) %s" % (name, lid))


if __name__ == "__main__":
    main(sys.argv[1:])
