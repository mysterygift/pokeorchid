"""
Eon Island region map (REGION_MAP_EON): the vanilla Emerald Hoenn region map with Hoenn hidden under the
Emerald intro's clouds, Southern Island (= Eon Island, vanilla cell (12,14)) and a bit of sea left clear.
MOCK + ROM preview only (nothing is written to graphics/ src/).

User direction (2026-11-19, 3rd round): "just use existing tiles" - no new cloud art.
  * source: graphics/intro/scene_2/clouds.png (32x64, the intro's passing-cloud OBJ sheet; palette = the
    PNG's own, = sClouds_Pal in src/intro_credits_graphics.c). Only indices 9/10/11 are used:
    (230,230,255) (246,255,255) (213,222,255).
  * its 8x8 tiles are copied AS-IS (no redraw) as four stamps: BIG (tiles cols 0-3 x rows 0-3, the big
    puffy cloud), WISP_A (cols 2-3, row 4), WISP_BC (cols 0-1, rows 4-5, two small wisps), WISP_D (cols 2-3,
    row 5). Stamps are placed on the 8 px tile grid of the region map BG tilemap; mirrored copies are
    allowed (pixels mirrored, nothing new).
  * baked into REGION_MAP_EON's own BG2 tiles + tilemap, loaded through gRegionMapInfos like every other
    region map. No sprites / OAM.
  * round 4 (user): "dense" - the vanilla Hoenn map as-is underneath, big clouds on a staggered lattice so
    they overlap into banks and hide most of Hoenn, a few left out as gaps, wisps on top (CHOSEN).
    "sky" (round 3: sparse clouds on the intro sky colour) is still rendered for reference.
  * the clear window round the island keeps the vanilla pixels (sea + island).
BG2 is an AFFINE 8bpp BG: u8 tilemap (<= 256 tiles), NO per-tile flips -> a mirrored cloud costs its own
tiles in the sheet (counted). Palette: the 48-colour slot at BG_PLTT_ID(7) (indices 112-159); the vanilla
map uses 112-140, the cloud colours + sky go in 141-144.

usage: <venv python> dev_scripts/voyages/regionmap/eon_clouds.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rm_common as C  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

ISLAND = (12, 14)                       # vanilla MAPSEC_SOUTHERN_ISLAND cell -> px (104..111, 128..135)
SRC = os.path.join(C.ROOT, "graphics", "intro", "scene_2", "clouds.png")
CLOUD_REMAP = {9: 141, 10: 142, 11: 143}           # intro index -> region-map palette index
SKY = (144, (136, 208, 248))            # intro sky (139,213,255) rounded to BGR555
STAMPS = {                              # name: (tile col0, row0, cols, rows) in the 4-tile-wide sheet
    "BIG": (0, 0, 4, 4),
    "WISP_A": (2, 4, 2, 1),
    "WISP_BC": (0, 4, 2, 2),
    "WISP_D": (2, 5, 2, 1),
}
# placements: (stamp, tile x, tile y, mirrored) on the 30x20 screen tile grid (map area = tile rows 2-16)
PLACE = [
    ("BIG", 0, 1, False), ("BIG", 7, 3, True), ("BIG", 15, 1, False), ("BIG", 23, 3, True),
    ("BIG", 2, 8, True), ("BIG", 19, 8, False), ("BIG", 10, 8, False), ("BIG", 25, 11, False),
    ("BIG", 0, 13, False),
    ("BIG", 7, 12, False), ("BIG", 17, 12, True),          # frame the clear window left / right
    ("WISP_A", 5, 6, False), ("WISP_A", 21, 6, True), ("WISP_A", 27, 8, False), ("WISP_A", 4, 16, True),
    ("WISP_BC", 13, 6, False), ("WISP_BC", 22, 15, True), ("WISP_BC", 28, 1, False),
    ("WISP_D", 4, 12, False), ("WISP_D", 13, 12, False), ("WISP_D", 15, 6, True),
]
WINDOW = (88, 112, 136, 136)            # clear sea round the island (px, x0 y0 x1 y1 exclusive)
WINDOW_CUT = (88, 112, 96, 120)         # ... minus its top corners (stepped, less box-like)
WINDOW_CUT2 = (128, 112, 136, 120)


def in_window(x, y):
    wx0, wy0, wx1, wy1 = WINDOW
    if not (wx0 <= x < wx1 and wy0 <= y < wy1):
        return False
    for cx0, cy0, cx1, cy1 in (WINDOW_CUT, WINDOW_CUT2):
        if cx0 <= x < cx1 and cy0 <= y < cy1:
            return False
    return True


def dense_place(step_x=3, step_y=2, gap_every=0, x0=-2, y0=0, salt=0):
    """Big clouds on a staggered lattice (every step_x tiles, rows every step_y tiles, odd rows shifted,
    alternate ones mirrored) so they overlap into banks; a deterministic few are left out (gaps); wisps go
    on top along the gaps. Stamps that would touch the clear window are dropped."""
    out, n = [], 0
    for row, ty in enumerate(range(y0, 16, step_y)):
        for tx in range(x0 + (row % 2) * (step_x // 2 + 1), 30, step_x):
            n += 1
            if gap_every and (n * 7 + row * 3 + salt) % gap_every == 0:
                continue
            out.append(("BIG", tx, ty, (tx // step_x + row) % 2 == 1))
    if salt:
        return out
    for i, (tx, ty) in enumerate([(3, 4), (11, 2), (19, 5), (26, 3), (6, 11), (15, 9), (23, 12), (1, 15), (27, 15)]):
        out.append((("WISP_A", "WISP_BC", "WISP_D")[i % 3], tx, ty, i % 2 == 1))
    return out


# two staggered lattices: the second (one tile right, one down, drawn first = behind) fills the slits the
# first leaves between its rows; its gaps are where bits of Hoenn show through
DENSE = dense_place(gap_every=4, x0=-1, y0=1, salt=5) + dense_place(gap_every=9)


def fits(name, tx, ty, mir):
    st = stamp_img(name, mir)
    sp = st.load()
    return not any(sp[x, y] in CLOUD_REMAP and in_window(tx * 8 + x, ty * 8 + y)
                   for y in range(st.height) for x in range(st.width))


def stamp_img(name, mirrored):
    src = Image.open(SRC)
    c0, r0, cw, rh = STAMPS[name]
    im = src.crop((c0 * 8, r0 * 8, (c0 + cw) * 8, (r0 + rh) * 8))
    return im.transpose(Image.FLIP_LEFT_RIGHT) if mirrored else im


def build(vanilla, look, place=None):
    im = vanilla.copy()
    pal = im.getpalette()
    src_pal = Image.open(SRC).getpalette()
    for s, d in CLOUD_REMAP.items():
        pal[d * 3:d * 3 + 3] = [v // 8 * 8 for v in src_pal[s * 3:s * 3 + 3]]
    pal[SKY[0] * 3:SKY[0] * 3 + 3] = list(SKY[1])
    im.putpalette(pal)
    p = im.load()
    wx0, wy0, wx1, wy1 = WINDOW
    if look == "sky":
        for y in range(C.H):
            for x in range(C.W):
                if not in_window(x, y):
                    p[x, y] = SKY[0]
    for name, tx, ty, mir in (place or PLACE):
        if not fits(name, tx, ty, mir):
            continue
        st = stamp_img(name, mir)
        sp = st.load()
        for y in range(st.height):
            for x in range(st.width):
                X, Y = tx * 8 + x, ty * 8 + y
                if 0 <= X < C.W and 0 <= Y < C.H and sp[x, y] in CLOUD_REMAP:
                    assert not in_window(X, Y), ("cloud in the window", name, tx, ty)
                    p[X, Y] = CLOUD_REMAP[sp[x, y]]
    return im


def to_rom(im, hide_rows=True):
    """8x8 tiles, exact dedupe (affine: no flips). Rows under the header (tile rows 0-1) / tray (17-19) are
    filled with the most common visible tile, so they cost nothing."""
    tiles, index, tmap = [], {}, bytearray(64 * 64)
    vis = [im.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)).tobytes() for ty in range(2, 17) for tx in range(30)]
    filler = max(set(vis), key=vis.count)
    for ty in range(20):
        for tx in range(30):
            key = im.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)).tobytes()
            if hide_rows and (ty < 2 or ty >= 17):
                key = filler
            if key not in index:
                index[key] = len(tiles)
                tiles.append(Image.frombytes("P", (8, 8), key))
            tmap[ty * 64 + tx] = index[key] & 0xFF          # (overflow reported by the caller)
    for i in range(64 * 64):
        if i % 64 >= 30 or i // 64 >= 20:
            tmap[i] = index[filler] & 0xFF
    return tiles, bytes(tmap)


def write_preview(tiles, tmap, pal, name):
    d = os.path.join(C.OUT, "eon_rom_preview")
    os.makedirs(d, exist_ok=True)
    rows = (len(tiles) + 15) // 16
    sheet = Image.new("P", (128, rows * 8))
    sheet.putpalette(pal)
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 16) * 8, (i // 16) * 8))
    sheet.save(os.path.join(d, name + ".png"))
    open(os.path.join(d, name + ".bin"), "wb").write(tmap)
    with open(os.path.join(d, name + ".pal"), "w") as f:      # the 48 colours loaded at BG_PLTT_ID(7)
        f.write("JASC-PAL\r\n0100\r\n48\r\n")
        for i in range(112, 160):
            f.write("%d %d %d\r\n" % tuple(pal[i * 3:i * 3 + 3]))
    sheet.convert("RGB").resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(
        os.path.join(d, name + "_sheet@3x.png"))
    return sheet


def source_panel():
    """The intro sheet as the game has it (own palette, transparent = black) with the stamp boxes."""
    src = Image.open(SRC).convert("RGB")
    S = 3
    big = src.resize((src.width * S, src.height * S), Image.NEAREST)
    d = ImageDraw.Draw(big)
    cols = {"BIG": (255, 80, 80), "WISP_A": (255, 200, 0), "WISP_BC": (80, 255, 120), "WISP_D": (80, 200, 255)}
    for n, (c0, r0, cw, rh) in STAMPS.items():
        d.rectangle([c0 * 8 * S, r0 * 8 * S, (c0 + cw) * 8 * S - 1, (r0 + rh) * 8 * S - 1], outline=cols[n])
    return big


def main():
    os.makedirs(C.OUT, exist_ok=True)
    for f in os.listdir(C.OUT):
        if f.startswith("eon_baked"):
            os.remove(os.path.join(C.OUT, f))
    pv = os.path.join(C.OUT, "eon_rom_preview")
    for f in os.listdir(pv) if os.path.isdir(pv) else []:
        if f.startswith("eon_baked"):
            os.remove(os.path.join(pv, f))
    sheet, tmap, rows = C.vanilla_hoenn()
    vanilla = C.bg2_from(sheet, tmap)
    assert C.sections_of(rows)["MAPSEC_SOUTHERN_ISLAND"] == [ISLAND]
    used_vanilla = len(set(tmap[y * 64 + x] for y in range(20) for x in range(30)))
    src_tiles = set()
    for name, _, _, mir in PLACE:
        st = stamp_img(name, mir)
        for ty in range(st.height // 8):
            for tx in range(st.width // 8):
                src_tiles.add(st.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)).tobytes())
    report = ["REGION_MAP_EON, intro scene_2 clouds baked into BG2 (affine 8bpp, u8 tilemap, no tile flips)",
              "  source: %s, %d distinct cloud tiles used incl. mirrored copies (sheet has 32)" % (
                  os.path.relpath(SRC, C.ROOT), len(src_tiles)),
              "  placements: %d BIG, %d wisps" % (sum(p[0] == "BIG" for p in PLACE), sum(p[0] != "BIG" for p in PLACE))]
    screens = {}
    looks = {"dense": ("map", DENSE), "sky": ("sky", PLACE)}
    for look, (bg, place) in looks.items():
        im = build(vanilla, bg, place)
        tiles, tm = to_rom(im)
        cols = sorted(set(b for t in tiles for b in t.tobytes()))
        report.append("  look '%s': %d unique tiles / 256 (vanilla Hoenn %d), %d B VRAM; colours %d of 48 (%s)" % (
            look, len(tiles), used_vanilla, len(tiles) * 64, len(cols), ",".join(map(str, cols))))
        if len(tiles) > 256:
            report.append("    -> OVER the 256-tile affine limit: would not fit without dropping clouds")
            shown = im
        else:
            write_preview(tiles, tm, im.getpalette(), "eon_%s" % look)
            shown = C.bg2_from(Image.open(os.path.join(C.OUT, "eon_rom_preview", "eon_%s.png" % look)), tm)
        C.save(shown, "eon_%s_bg2" % look)
        scr = C.screen(shown, "EON ISLAND", "Eon Island", [], cursor=ISLAND, here=ISLAND)
        C.save(scr, "eon_%s_screen" % look)
        screens[look] = scr.convert("RGB")
    kept = [p for p in DENSE if fits(*p)]
    report.insert(3, "  dense: %d BIG + %d wisps placed (%d dropped at the window)" % (
        sum(p[0] == "BIG" for p in kept), sum(p[0] != "BIG" for p in kept), len(DENSE) - len(kept)))
    report.append("  chosen (user, round 4): 'dense' = map as-is under dense intro clouds; 'sky' = round 3 for reference")
    # compare: source sheet | vanilla | sky (chosen) | map
    v = C.screen(vanilla, "HOENN (vanilla art)", "Southern Island", [], ISLAND, ISLAND).convert("RGB")
    src = source_panel()
    Wd = src.width + 8 + (C.W + 8) * 3
    strip = Image.new("RGB", (Wd, max(C.H, src.height) + 14), (40, 40, 48))
    d = ImageDraw.Draw(strip)
    strip.paste(src, (0, 14))
    d.text((0, 1), "intro clouds (3x)", fill=(255, 255, 255))
    x = src.width + 8
    for label, im in (("vanilla Hoenn", v), ("DENSE clouds over map (chosen)", screens["dense"]),
                      ("round 3: sky between clouds", screens["sky"])):
        strip.paste(im, (x, 14))
        d.text((x, 1), label, fill=(255, 255, 255))
        x += C.W + 8
    strip.save(os.path.join(C.OUT, "eon_compare.png"))
    C.K.upscale(strip, 3).save(os.path.join(C.OUT, "eon_compare@3x.png"))
    open(os.path.join(C.OUT, "eon_budget.txt"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))


if __name__ == "__main__":
    main()
