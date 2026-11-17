"""
Poké Mart helpers for the Orchid buy-screen mockups (mock_mart.py / anim_mart.py).

PROPOSED kit additions (kept here until the user approves the Mart):
  * SHOP palette (BG pal 2) on fixed roles: the 6 kit neutrals + wood / Mart blue / brass ramps.
  * Two-palette BG art: draw pal-0 (Orchid kit) roles as 0..15 and SHOP roles as 32..47 on one
    sheet; `check_tiles` proves every 8x8 tile uses one palette (GBA rule) and counts tiles.
  * awning, hanging chain, wood board, rivets, coin, price tag (pointed end + string hole),
    vertical chevrons, shelf cabinet, receipt strip with torn edge, cash register.
  * mart_field(): the real LAYOUT_MART map (building + shop tilesets) for the BUY/SELL/QUIT menu.

All colours: kit neutrals; wood = graphics/items/icon_palettes/wood_mail.pal; brass = battle_ext
HB_PAL brass (nugget-derived); Mart blue = the Poké Mart roof ramp in
data/tilesets/primary/general/palettes/04.pal; price-tag manila = wood_mail.pal face.
"""
import json
import os
import struct
from PIL import Image
from kit import *
import kit as KIT
import kit_ext as K
from battle_ext import chamfer_mask, mask_box, round_mask
from gamefont import draw_text, text_width

ROOT = K.ROOT
W, H = 240, 160

# ------------------------------------------------------------------ palettes
TAG_FACE, TAG_SHADE = (224, 208, 152), (176, 128, 72)     # wood_mail.pal face / grain

S = 32  # SHOP palette block offset in the art sheets
WOOD_DARK, WOOD, WOOD_LIGHT = 7, 8, 9
MART_DARK, MART, MART_LIGHT = 10, 11, 12
BRASS_DARK, BRASS, BRASS_LIGHT = 13, 14, 15
SHOP_RAMPS = {
    # Poké Mart roof blue (general/palettes/04.pal) — recommended
    "mart": [(40, 64, 136), (64, 88, 192), (136, 160, 224)],
    # Orchid purple instead (one-palette look)
    "orchid": [(96, 48, 128), (152, 88, 184), (200, 152, 224)],
}


def p0():
    return palette("orchid", spare_a=TAG_FACE, spare_b=TAG_SHADE)


def p1():
    """Selected-row variant of pal 0 (same swap as the bag)."""
    p, b = list(p0()), p0()
    p[PANEL], p[WHITE], p[PANEL_SHADE] = b[SELECT], b[SELECT_LIGHT], b[SELECT_DARK]
    return p


def shop_pal(accent="mart"):
    base = p0()
    ramp = SHOP_RAMPS[accent]
    cols = base[:7] + [(144, 104, 48), (176, 128, 72), (208, 160, 96)] + ramp + \
        [(160, 104, 40), (216, 168, 72), (248, 224, 144)]
    return [snap(c) for c in cols]


G4 = 64  # GOODS palette block (BG pal 4): shelf stock in Gen 3 item-icon colours
GOODS = {
    "I": 1, "W": 2, "g": 3,                       # ink, white, ball-bottom grey   (poke_ball.pal)
    "h": 4, "R": 5, "r": 6,                       # ball red light / face / dark   (poke_ball.pal)
    "l": 7, "P": 8, "p": 9, "C": 10,              # potion purple ramp + teal nozzle (potion.pal)
    "t": 11, "T": 12, "k": 13,                    # tan (wood_mail.pal) + dark wood (escape_rope.pal)
    "G": 14, "d": 15,                             # repel green / dark             (repel.pal)
}


def goods_pal():
    return [snap(c) for c in [
        (0, 0, 0), (40, 40, 64), (255, 255, 255), (164, 164, 197),
        (255, 148, 57), (222, 90, 57), (156, 74, 57),
        (164, 131, 205), (131, 98, 172), (90, 57, 131), (164, 205, 189),
        (222, 205, 148), (172, 131, 74), (123, 98, 16),
        (82, 180, 82), (49, 123, 49)]]


BALL7 = [".IIIII.",
         "IhRRRRI",
         "IRRRRrI",
         "IIIWIII",
         "IWWWWgI",
         "IWWWggI",
         ".IIIII."]
BOTTLE = ["..III..",
          "..ICI..",
          ".IIIII.",
          "IlPPPpI",
          "IlPPPpI",
          "IlWWPpI",
          "IlWWPpI",
          "IlPPPpI",
          "IlPPPpI",
          "IpppppI",
          ".IIIII."]
CAN = [".IIII.",
       "IWWWgI",
       "IIIIII",
       "IWGGdI",
       "IWGGdI",
       "IIIIII",
       "IWGGdI",
       "IWGGdI",
       ".IIII."]


def box(w, h):
    rows = []
    for y in range(h):
        row = ""
        for x in range(w):
            if y in (0, h - 1) or x in (0, w - 1):
                row += "I"
            elif y == 1:
                row += "t"
            elif x == w - 2:
                row += "k"
            elif x == w // 2:
                row += "t"          # tape stripe
            else:
                row += "T"
        rows.append(row)
    return rows


def gstamp(cv, x, y, rows):
    stamp(cv, x, y, rows, {k: G4 + v for k, v in GOODS.items()})


def wall_shelf(cv, x0, x1, plank_y):
    """Back-wall shelf: goods (pal 4, tile rows above plank_y) on a wood plank with brass brackets (pal 2).
    plank_y must be tile-aligned so goods and wood never share a tile."""
    by = plank_y - 1                              # goods sit on the plank
    # dark wood back panel (goods palette tan ramp) so the stock reads against the near-black grid
    top = plank_y - 15
    cv.rect(x0, top, x1, by, G4 + GOODS["k"])
    cv.hline(x0, x1, top, G4 + GOODS["I"])
    cv.hline(x0 + 1, x1 - 1, top + 1, G4 + GOODS["T"])
    cv.vline(x0, top, by, G4 + GOODS["I"])
    cv.vline(x1, top, by, G4 + GOODS["I"])
    cv.vline(x0 + 1, top + 1, by, G4 + GOODS["T"])
    # Poké Ball pyramid
    gstamp(cv, x0 + 3, by - 6, BALL7)
    gstamp(cv, x0 + 10, by - 6, BALL7)
    gstamp(cv, x0 + 6, by - 12, BALL7)
    # two potion bottles
    gstamp(cv, x0 + 22, by - 10, BOTTLE)
    gstamp(cv, x0 + 30, by - 10, BOTTLE)
    # cardboard boxes (two stacked, offset)
    gstamp(cv, x0 + 42, by - 6, box(15, 7))
    gstamp(cv, x0 + 44, by - 12, box(11, 7))
    # repel cans
    gstamp(cv, x0 + 62, by - 8, CAN)
    gstamp(cv, x0 + 69, by - 8, CAN)
    # second ball pyramid
    gstamp(cv, x1 - 16, by - 6, BALL7)
    gstamp(cv, x1 - 9, by - 6, BALL7)
    gstamp(cv, x1 - 13, by - 12, BALL7)
    # plank
    y = plank_y
    cv.hline(x0, x1, y, s(WOOD_LIGHT))
    cv.hline(x0, x1, y + 1, s(WOOD))
    cv.hline(x0, x1, y + 2, s(WOOD_DARK))
    cv.hline(x0, x1, y + 3, s(INK))
    cv.vline(x0, y, y + 3, s(INK))
    cv.vline(x1, y, y + 3, s(INK))
    # brass L-brackets under the plank
    for bx in (x0 + 5, x1 - 9):
        stamp(cv, bx, y + 4, ["IBBBI", "IBBI.", "IBI..", "II..."],
              {"I": s(INK), "B": s(BRASS)})
        cv.set(bx + 1, y + 4, s(BRASS_LIGHT))
        cv.set(bx + 1, y + 5, s(BRASS_LIGHT))


def s(role):
    """SHOP-palette index for a role (neutral roles 1..6 exist in both palettes)."""
    return S + role


def art_sheet(w=W, h=H, accent="mart"):
    im = Image.new("P", (w, h), 0)
    flat = []
    for c in p0() + p1() + shop_pal(accent) + [(0, 0, 0)] * 16 + goods_pal():
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im


# ------------------------------------------------------------------ compositing
def compose(art, cellpal=None, grid_scroll=0, accent="mart", base=None):
    """Art sheet -> RGBA over the BG3 grid. cellpal[(tx,ty)] = 1 renders that tile with pal 1."""
    cellpal = cellpal or {}
    pals = {0: p0(), 1: p1(), 2: shop_pal(accent), 4: goods_pal()}
    out = base.copy() if base is not None else K.grid_frame(grid_scroll, *art.size)
    op, ap = out.load(), art.load()
    for y in range(art.size[1]):
        for x in range(art.size[0]):
            v = ap[x, y]
            if not v:
                continue
            blk = v // 16
            if blk == 0 and cellpal.get((x // 8, y // 8)) == 1:
                blk = 1
            op[x, y] = pals[blk][v % 16] + (255,)
    return out


def overlay(out, sheet, accent="mart"):
    """Composite a text/window sheet (same index scheme, no cell swaps) over out."""
    pals = {0: p0(), 1: p1(), 2: shop_pal(accent), 4: goods_pal()}
    op, sp = out.load(), sheet.load()
    for y in range(sheet.size[1]):
        for x in range(sheet.size[0]):
            v = sp[x, y]
            if v:
                op[x, y] = pals[v // 16][v % 16] + (255,)


def check_tiles(art):
    """GBA rule: one palette per 8x8 tile. Returns (unique tiles incl. blank, conflicts, pal use)."""
    w, h = art.size
    ap = art.load()
    four = Image.new("P", (w, h), 0)
    fp = four.load()
    conflicts, use = [], {}
    for ty in range(h // 8):
        for tx in range(w // 8):
            blocks = set()
            for y in range(8):
                for x in range(8):
                    v = ap[tx * 8 + x, ty * 8 + y]
                    if v:
                        blocks.add(v // 16)
                        fp[tx * 8 + x, ty * 8 + y] = v % 16
            if len(blocks) > 1:
                conflicts.append((tx, ty))
            for b in blocks:
                use[b] = use.get(b, 0) + 1
    tiles, _ = to_tiles(four)
    return len(tiles), conflicts, use


# ------------------------------------------------------------------ small sprites
def p_sprite(w, h, fn, pal):
    im = Image.new("P", (w, h), 0)
    flat = [c for rgb in pal for c in rgb]
    im.putpalette(flat + [0] * (768 - len(flat)))
    fn(Canvas(im))
    return K.sheet_rgba(im)


def icon(name):
    """Item icon with the ROM's shared pic + per-item palette (items.h iconPic/iconPalette)."""
    pic = {"antidote": "status_heal", "paralyze_heal": "status_heal", "awakening": "status_heal",
           "burn_heal": "status_heal", "super_potion": "potion"}.get(name, name)
    if name.startswith("tm_"):
        return K.sprite_rgba(K.G("items", "icons", "tm.png"),
                             pal=K.load_jasc(K.G("items", "icon_palettes", name[3:] + "_tm_hm.pal")))
    return K.sprite_rgba(K.G("items", "icons", pic + ".png"),
                         pal=K.load_jasc(K.G("items", "icon_palettes", name + ".pal")))


def chevron(direction, pal=None):
    """Kit 6x9 red Gen 3 chevron; direction left/right/up/down (up/down = transposed, 9x6)."""
    rows = SMALL_ARROW
    if direction == "right":
        rows = [r[::-1] for r in rows]
    elif direction in ("up", "down"):
        rows = ["".join(rows[c][r] for c in range(9)) for r in range(6)]
        if direction == "down":
            rows = rows[::-1]
    w, h = len(rows[0]), len(rows)
    pal = [(0, 0, 0), ARROW_RED[1], ARROW_RED[0]]
    return p_sprite(w, h, lambda cv: stamp(cv, 0, 0, rows, {"O": 1, "F": 2}), pal + [(0, 0, 0)] * 13)


def thumb(h=12):
    return p_sprite(4, h, lambda cv: rounded_box(cv, 0, 0, 4, h, 1, SELECT, INK, SELECT_LIGHT, SELECT_DARK), p0())


def clerk(frame=0):
    pal = K.load_jasc(K.G("object_events", "palettes", "npc_1.pal"))
    return K.sprite_rgba(K.G("object_events", "pics", "people", "mart_employee.png"), frame, 32, pal) \
        .crop((0, 0, 16, 32)) if frame == 0 else \
        K.sheet_rgba(Image.open(K.G("object_events", "pics", "people", "mart_employee.png"))
                     .crop((frame * 16, 0, frame * 16 + 16, 32)), pal)


def obj_person(png, palname, frame):
    pal = K.load_jasc(K.G("object_events", "palettes", palname + ".pal"))
    im = Image.open(png)
    fw = 16
    return K.sheet_rgba(im.crop((frame * fw, 0, frame * fw + fw, 32)), pal)


# ------------------------------------------------------------------ shop primitives (indices passed in)
def rivet(cv, x, y):
    """2x2 brass rivet (SHOP palette)."""
    cv.set(x, y, s(BRASS_LIGHT))
    cv.set(x + 1, y, s(BRASS))
    cv.set(x, y + 1, s(BRASS))
    cv.set(x + 1, y + 1, s(BRASS_DARK))


def awning(cv, x0, x1, y0=0, stripe=16):
    """16px striped awning: brass rail, pleated stripes, round scalloped hem (index 0 between scallops)."""
    cv.hline(x0, x1, y0, s(BRASS_LIGHT))
    cv.hline(x0, x1, y0 + 1, s(BRASS))
    cv.hline(x0, x1, y0 + 2, s(BRASS_DARK))
    cv.hline(x0, x1, y0 + 3, s(INK))
    SC = ["FFFFFFFFFFFFFFFF",
          "FFFFFFFFFFFFFFFF",
          "IFFFFFFFFFFFFFFI",
          ".IIFFFFFFFFFFII.",
          "...IIFFFFFFII...",
          ".....IIIIII....."]
    for k, sx in enumerate(range(x0, x1 + 1, stripe)):
        blue = k % 2 == 0
        face = s(MART) if blue else s(WHITE)
        light = s(MART_LIGHT) if blue else s(WHITE)
        dark = s(MART_DARK) if blue else s(PANEL_SHADE)
        for r in range(12):
            row = "F" * stripe if r < 6 else SC[r - 6]
            y = y0 + 4 + r
            for dx, ch in enumerate(row):
                if ch == "I":
                    cv.set(sx + dx, y, s(INK))
                    continue
                if ch != "F":
                    continue
                c = face
                last = r == 11 or (r < 11 and (SC[r - 5][dx] != "F" if r >= 5 else False))
                if r == 0:
                    c = dark                      # shadow under the rail
                elif last:
                    c = dark                      # hem shade along the scallop
                elif dx <= 1:
                    c = light
                elif dx == stripe - 1:
                    c = dark
                cv.set(sx + dx, y, c)


def rod(cv, x, y0, y1):
    """Hanging brass rod: 2px with ink edges (reads on the near-black grid)."""
    for y in range(y0, y1 + 1):
        cv.set(x - 1, y, s(INK))
        cv.set(x, y, s(BRASS_LIGHT))
        cv.set(x + 1, y, s(BRASS_DARK))
        cv.set(x + 2, y, s(INK))


def wood_board(cv, x, y, w, h, r=3, grain=True):
    big_round = round_mask(w, h, r)
    mask_box(cv, x, y, big_round, s(WOOD), s(INK), s(WOOD_LIGHT), s(WOOD_DARK))
    if grain:
        # two long grain strokes (no lone pixels)
        for gy, a, b in ((y + h // 3, x + 6, x + w // 2 - 2), (y + 2 * h // 3, x + w // 2 + 4, x + w - 8)):
            cv.hline(a, b, gy, s(WOOD_DARK))


def coin(cv, cx, cy, r=5.5):
    """Gold coin (SHOP brass ramp) with an embossed ring."""
    disc(cv, cx, cy, r, s(BRASS), s(INK), s(BRASS_LIGHT), s(BRASS_DARK))
    ring(cv, cx, cy, r - 2.6, s(BRASS_DARK))
    cv.set(int(cx) - 1, int(cy) - 1, s(BRASS_LIGHT))


def coin_stack(cv, x, y):
    """Three stacked coins seen side-on (money pill picture), 12x10."""
    for k in range(3):
        yy = y + 6 - k * 3
        rounded_box(cv, x, yy, 12, 5, 2, s(BRASS), s(INK), s(BRASS_LIGHT), s(BRASS_DARK))


TAG_POINT = 5


def price_tag(cv, x, y, w, h=12, face=SPARE_A, light=WHITE, shade=SPARE_B, outline=INK, hole_bg=None):
    """Manila tag, pointed left end with a punched string hole. Indices of pal 0 by default."""
    m = chamfer_mask(w, h, tl=TAG_POINT, bl=TAG_POINT)
    mask_box(cv, x, y, m, face, outline, light, shade)
    hx, hy = x + 5, y + h // 2 - 2
    stamp(cv, hx, hy, [".II.", "IPPB", "IPPB", ".BB."], {"I": outline, "B": shade, "P": hole_bg if hole_bg is not None else PANEL})
    return hx, hy


def tag_string(cv, hx, hy, x_end, c=INK_SOFT):
    """String from the tag hole curling up-left to x_end (1px, no lone pixels)."""
    cv.hline(x_end + 2, hx - 1, hy, c)
    cv.set(x_end + 1, hy - 1, c)
    cv.set(x_end, hy - 2, c)
    cv.set(x_end, hy - 3, c)


def track(cv, x0, y0, x1, y1):
    rounded_box(cv, x0, y0, x1 - x0 + 1, y1 - y0 + 1, 2, PANEL_DARK, INK, PANEL_SHADE, PANEL_DARK)
    cv.hline(x0 + 2, x1 - 2, y0 + 1, INK_SOFT)


def thumb_y(y0, y1, scroll, total, rows, th=12):
    span = (y1 - y0 - 3) - th
    return y0 + 2 + (span * scroll // max(1, total - rows) if total > rows else 0)


# ------------------------------------------------------------------ the real Mart map (state 07 field)
def _u16(path):
    d = open(path, "rb").read()
    return struct.unpack("<%dH" % (len(d) // 2), d)


def mart_field(cam=(4, 5)):
    """LAYOUT_MART rendered from the building + shop tilesets, camera centred on metatile cam.
    Player stands at cam, so the view is the 15x10-metatile window around it (border fills outside)."""
    ts = lambda *p: os.path.join(ROOT, "data", "tilesets", *p)
    prim = Image.open(ts("primary", "building", "tiles.png"))
    sec = Image.open(ts("secondary", "shop", "tiles.png"))
    pals = []
    for i in range(16):
        f = ts("primary", "building", "palettes", "%02d.pal" % i) if i < 6 else ts("secondary", "shop", "palettes", "%02d.pal" % i)
        pals.append([snap(c) for c in K.load_jasc(f)])
    mt_p, mt_s = _u16(ts("primary", "building", "metatiles.bin")), _u16(ts("secondary", "shop", "metatiles.bin"))
    lay = os.path.join(ROOT, "data", "layouts", "Mart")
    blocks = _u16(os.path.join(lay, "map.bin"))
    border = _u16(os.path.join(lay, "border.bin"))
    MW, MH = 11, 8
    out = Image.new("RGBA", (W, H), pals[0][0] + (255,))
    op = out.load()
    pp, sp = prim.load(), sec.load()
    ptw, stw = prim.size[0] // 8, sec.size[0] // 8

    def tile(idx, hf, vf, pal, ox, oy, layer):
        src, tw, base = (pp, ptw, 0) if idx < 512 else (sp, stw, 512)
        idx -= base
        sx, sy = (idx % tw) * 8, (idx // tw) * 8
        for y in range(8):
            for x in range(8):
                v = src[sx + (7 - x if hf else x), sy + (7 - y if vf else y)]
                if v == 0 and layer:
                    continue
                X, Y = ox + x, oy + y
                if 0 <= X < W and 0 <= Y < H:
                    op[X, Y] = pals[pal][v] + (255,)

    # camera: player metatile drawn at screen (112, 72) like the overworld (sprite feet at y 88)
    ox0, oy0 = 112 - cam[0] * 16, 64 - cam[1] * 16
    for my in range(-6, MH + 6):
        for mx in range(-8, MW + 8):
            if 0 <= mx < MW and 0 <= my < MH:
                mid = blocks[my * MW + mx] & 0x3FF
            else:
                mid = border[(my % 2) * 2 + (mx % 2)] & 0x3FF
            src = mt_p if mid < 512 else mt_s
            base = (mid if mid < 512 else mid - 512) * 8
            for layer in (0, 1):
                for q in range(4):
                    e = src[base + layer * 4 + q]
                    tile(e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12,
                         ox0 + mx * 16 + (q % 2) * 8, oy0 + my * 16 + (q // 2) * 8, layer)
    m = json.load(open(os.path.join(ROOT, "data", "maps", "FallarborTown_Mart", "map.json")))
    people = os.path.join(ROOT, "graphics", "object_events", "pics", "people")
    # clerk behind the counter (faces right = frame 2 flipped... use the face-right frame)
    for o in m["object_events"]:
        if o["graphics_id"] == "OBJ_EVENT_GFX_MART_EMPLOYEE":
            spr = obj_person(os.path.join(people, "mart_employee.png"), "npc_1", 2).transpose(Image.FLIP_LEFT_RIGHT)
            out.alpha_composite(spr, (ox0 + o["x"] * 16, oy0 + o["y"] * 16 - 16))
    # player facing the clerk (left)
    pl = obj_person(os.path.join(people, "brendan", "walking.png"), "brendan", 2)
    out.alpha_composite(pl, (ox0 + cam[0] * 16, oy0 + cam[1] * 16 - 16))
    return out


# ------------------------------------------------------------------ TM discs (one shared OBJ palette)
TM_TYPES = ("ground", "poison", "water", "fire", "electric", "ice")


def tm_disc_pal():
    pal = [(0, 0, 0), (40, 40, 64), (248, 248, 248), (128, 128, 152)]
    for t in TM_TYPES:
        p = K.load_jasc(K.G("items", "icon_palettes", t + "_tm_hm.pal"))
        pal += [snap(p[6]), snap(p[9])]          # face / shade of the disc (icon's mid + dark)
    return pal[:16] + [(0, 0, 0)] * (16 - len(pal[:16]))


def tm_disc(t):
    """12x12 TM disc in the type's own *_tm_hm.pal colours; all six types share one OBJ palette."""
    k = TM_TYPES.index(t)
    light, dark = 4 + 2 * k, 5 + 2 * k
    pal = tm_disc_pal()

    def fn(cv):
        disc(cv, 6, 6, 5.5, light, 1, 2, dark)
        disc(cv, 6, 6, 1.6, 2, 1)
    return p_sprite(12, 12, fn, pal)
