"""
Overworld sprites for the café mockups, drawn with their in-game palette (the PNG's own palette can differ).
Registers keys in voyage_compose.SPRITES / _SPR without editing voyage_compose.

key -> (png name under graphics/object_events/pics/people, frame index, hflip, palette file)
Frames for 16x32 people: 0 down, 1 up, 2 left (right = left flipped). 48-px-wide sheets have only these 3.
"""
import os
import re

import voyage_compose as vc
from PIL import Image

PEOPLE = "graphics/object_events/pics/people"
INFO = "src/data/object_events/object_event_graphics_info.h"
TAG_FILE = {"OBJ_EVENT_PAL_TAG_NPC_1": "npc_1.pal", "OBJ_EVENT_PAL_TAG_NPC_2": "npc_2.pal",
            "OBJ_EVENT_PAL_TAG_NPC_3": "npc_3.pal", "OBJ_EVENT_PAL_TAG_NPC_4": "npc_4.pal",
            "OBJ_EVENT_PAL_TAG_NPC_WHITE": "npc_white.pal", "OBJ_EVENT_PAL_TAG_NPC_PINK": "npc_pink.pal",
            "OBJ_EVENT_PAL_TAG_NPC_BLUE": "npc_blue.pal", "OBJ_EVENT_PAL_TAG_NPC_GREEN": "npc_green.pal"}
_TAGS = None


def pal_tag(info_name):
    """gObjectEventGraphicsInfo_<info_name> -> its paletteTag."""
    global _TAGS
    if _TAGS is None:
        src = open(os.path.join(vc.ROOT, INFO)).read()
        _TAGS = dict(re.findall(r"gObjectEventGraphicsInfo_(\w+) = \{\s*\.tileTag[^;]*?\.paletteTag = (\w+)",
                                src, re.S))
        if not _TAGS:
            _TAGS = {m.group(1): m.group(2) for m in re.finditer(
                r"gObjectEventGraphicsInfo_(\w+) = \{.*?\.paletteTag = (\w+)", src, re.S)}
    return _TAGS[info_name]


def register(key, png, info_name, frame=0, flip=False):
    path = os.path.join(vc.ROOT, PEOPLE, png + ".png")
    im = Image.open(path)
    im = im.crop((frame * 16, 0, frame * 16 + 16, 32))
    pal = vc.vanilla.load_jasc(os.path.join(vc.ROOT, "graphics/object_events/palettes",
                                            TAG_FILE[pal_tag(info_name)]))
    px = im.load()
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    op = out.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y]:
                op[x, y] = tuple(pal[px[x, y]]) + (255,)
    if flip:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)
    vc.SPRITES[key] = (os.path.join(PEOPLE, png + ".png"), 16, 32, frame, flip)
    vc._SPR[key] = out
    return key


# (png, info name) for the people used in the café mockups
CAST = {
    "executive": ("executive", "Executive"), "clerk": ("clerk", "Clerk"), "man_4": ("man_4", "Man4"),
    "woman_5": ("woman_5", "Woman5"), "gentleman": ("gentleman", "Gentleman"), "beauty": ("beauty", "Beauty"),
    "tourist_m": ("tourist_m", "TouristM"), "influencer": ("influencer", "Influencer"),
    "nyonya": ("nyonya", "Nyonya"), "old_man": ("old_man", "OldMan"), "woman_2": ("woman_2", "Woman2"),
    "man_3": ("man_3", "Man3"), "cook": ("cook", "Cook"), "woman_4": ("woman_4", "Woman4"),
    "tourist_f": ("tourist_f", "TouristF"), "lass": ("lass", "Lass"),
}
DIRS = {"down": (0, False), "up": (1, False), "left": (2, False), "right": (2, True)}


def key(name, facing="down"):
    """Register (once) and return the sprite key for CAST[name] facing a direction."""
    k = "cafe_%s_%s" % (name, facing)
    if k not in vc._SPR:
        png, info = CAST[name]
        fr, fl = DIRS[facing]
        register(k, png, info, fr, fl)
    return k


def contact_sheet(path, scale=4):
    names = list(CAST)
    im = Image.new("RGBA", (len(names) * 20 * scale, 44 * scale), (200, 200, 200, 255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    for i, n in enumerate(names):
        s = vc._SPR[key(n)]
        im.alpha_composite(s.resize((16 * scale, 32 * scale), Image.NEAREST), (i * 20 * scale, 0))
        d.text((i * 20 * scale, 33 * scale), n, fill=(0, 0, 0, 255))
    im.convert("RGB").save(path)


def silhouette(name="woman_5", facing="left", colour=(40, 30, 60)):
    """Placeholder for an OW that does not exist yet (Cynthia): a dark silhouette of a stand-in sprite."""
    k = "cafe_sil_%s_%s" % (name, facing)
    if k not in vc._SPR:
        src = vc._SPR[key(name, facing)]
        out = Image.new("RGBA", src.size, (0, 0, 0, 0))
        sp, op = src.load(), out.load()
        for y in range(src.height):
            for x in range(src.width):
                if sp[x, y][3]:
                    op[x, y] = colour + (255,)
        vc.SPRITES[k] = vc.SPRITES[key(name, facing)]
        vc._SPR[k] = out
    return k
