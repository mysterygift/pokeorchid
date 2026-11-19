"""Scene-sized boat for the voyage ferry cutscene: Mr. Briney's boat overworld frame 2 (side view, bow left),
scaled 2x into a 64x64 4bpp sprite (art at the top, like ferry_sprite.png), NPC_3 palette (the PNG's own)."""
import os
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
src = Image.open(os.path.join(ROOT, "graphics/object_events/pics/misc/mr_brineys_boat.png"))
frame = src.crop((64, 0, 96, 32))
x0, y0, x1, y1 = frame.getbbox()
art = frame.crop((0, y0, 32, y1)).resize((64, (y1 - y0) * 2), Image.NEAREST)
out = Image.new("P", (64, 64), 0)
out.putpalette(src.getpalette()[:48])
out.paste(art, (0, 0))
out.save(os.path.join(ROOT, "graphics/seagallop/briney_boat.png"), bits=4, optimize=False)
print("art rows 0-%d" % (art.height - 1))
