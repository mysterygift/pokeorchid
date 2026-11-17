"""
Export the Orchid battle UI (mock_battle.py / battle_ext.py, healthbox direction B) to game assets.

Writes (repo root):
  graphics/battle_interface/orchid_healthbox_player.png     128x32 OBJ (2x 64x32), HB_PAL, no text
  graphics/battle_interface/orchid_healthbox_opponent.png   128x32 OBJ (2x 64x32), HB_PAL, no text
  graphics/battle_interface/orchid_healthbar_player.png     128x8  OBJ (2x 64x8), HBAR_PAL: HP tag, bar
                                                            frame + empty trough, empty EXP strip
  graphics/battle_interface/orchid_healthbar_opponent.png   same without the EXP strip
  src/data/battle_orchid_ui.h                               generated layout constants

The C side draws the text (name / Lv / HP numbers), the caught ball and the bar fills at the
positions exported here, with the same glyphs (graphics/fonts) the mockups use.

usage: export_battle.py
"""
import os
from PIL import Image
from kit import *
import kit_ext as K
import battle_ext as BX
import mock_battle as M
import windows as Wn
from gamefont import text_width, _font, draw_text

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = lambda *p: os.path.join(ROOT, *p)
W, H = 240, 160


def save_indexed(im, path, pal):
    flat = [c for rgb in pal for c in rgb]
    out = im.copy()
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(path, transparency=0)


def pad16(pal):
    return list(pal) + [(0, 0, 0)] * (16 - len(pal))


# ------------------------------------------------------------------ healthboxes
def _no_text(fn):
    """Run fn with BX's text/ball drawing stubbed out (frame-only art)."""
    saved = (BX.name_gender, BX.lv_text, BX.draw_text, BX.caught_ball)
    BX.name_gender = lambda *a, **k: 0
    BX.lv_text = lambda *a, **k: None
    BX.draw_text = lambda *a, **k: 0
    BX.caught_ball = lambda *a, **k: None
    try:
        return fn()
    finally:
        BX.name_gender, BX.lv_text, BX.draw_text, BX.caught_ball = saved


def export_healthboxes():
    info = {}
    for side, mon in (("plr", M.default_player()), ("opp", M.default_enemy())):
        x, y, w, h = BX.hb_rect("B", side)
        sheet = M.p_sheet(W, H, BX.HB_PAL)
        an = _no_text(lambda: BX.hb_B(Canvas(sheet), mon, side))
        box = sheet.crop((x, y, x + 128, y + 32))
        name = "player" if side == "plr" else "opponent"
        save_indexed(box, P("graphics", "battle_interface", "orchid_healthbox_%s.png" % name), BX.HB_PAL)

        # bars: HP tag + empty bar (+ empty EXP strip), healthbar palette, 128x8 from (x+24, y+23)
        bars = M.p_sheet(W, H, M.HBAR_PAL)
        M.draw_bars(Canvas(bars), mon, an, hp=0, exp=0.0)
        bx, by = x + 24, y + 23
        strip = bars.crop((bx, by, bx + 128, by + 8))
        save_indexed(strip, P("graphics", "battle_interface", "orchid_healthbar_%s.png" % name), M.HBAR_PAL)

        TAB_W = 72
        px0, py0 = x + 7 + 19, y + 8 + 2
        d = dict(x=x, y=y, w=w, h=h,
                 bar=(an["bar"][0] - bx, an["bar"][1] - by),
                 status=(an["status"][0] - x, an["status"][1] - y),
                 pill=(px0 - x, py0 - y, x + w - 5 - px0, 13),
                 tab=(w - TAB_W, 0, TAB_W, 12))
        if an["exp"]:
            ex0, ex1, ey, _ = an["exp"]
            d["exp"] = (ex0 - bx, ey - by, ex1 - ex0 + 1)
        info[side] = d
    return info


# ------------------------------------------------------------------ BG0 tray (all pages)
# BG0 tilemap is 32x64 (three 20-row pages, scrolled by gBattle_BG0_Y): page 0 = message,
# page 1 = action menu, page 2 = move select. Every interactive panel is a text WINDOW whose
# pixels are blitted from the raw panel images below (normal / selected variants), so the
# static tileset only holds the tray, panels outside windows, the back tab, the YES/NO dock
# and a std frame for HandleBattleWindow.
TRAY_STATIC_MAX = 0x90          # B_WIN_MSG starts at tile 0x90
TRAY_HOLE = (0x10, 0x30)        # reserved for the user window frame (see export_tray)
ACTION_WIN = (16, 14, 14, 6)    # tiles (x, y-in-page, w, h): FIGHT + side buttons
PROMPT_WIN = (2, 15, 13, 4)     # "What will X do?"
MOVE_WIN = [(0, 14, 15, 3), (15, 14, 15, 3), (0, 17, 15, 3), (15, 17, 15, 3)]
YESNO_WIN = (25, 15, 4, 4)
YESNO_DOCK = (23, 14, 7, 6)     # cells replaced while the YES/NO is docked


def page_base(mode):
    bg = M.p_sheet(W, H, M.UI_PAL)
    cv = Canvas(bg)
    M.draw_tray(cv)
    if mode == "msg":
        M.msg_panel(cv, 2, 237)
    elif mode == "action":
        M.msg_panel(cv, 2, 126)
    elif mode == "yesno":
        M.msg_panel(cv, 2, 189)
        Wn.std_frame(cv, *M.YESNO_T)
    elif mode == "moves":
        M.draw_back_tab(cv)
    return bg


def action_art(cursor):
    """Tray + FIGHT / side buttons without labels (labels are printed at runtime)."""
    bg = page_base("action")
    saved = M.draw_text
    M.draw_text = lambda *a, **k: 0
    try:
        M.draw_action(Canvas(bg), cursor)
    finally:
        M.draw_text = saved
    return bg


def move_art(selected_slot):
    bg = page_base("moves")
    cv = Canvas(bg)
    for i, (x, y) in enumerate(M.MOVE_POS):
        if i == selected_slot:
            Wn.selection_bar(cv, x, y, M.MOVE_W, M.MOVE_H)
        else:
            rounded_box(cv, x, y, M.MOVE_W, M.MOVE_H, 4, PANEL, INK, WHITE, PANEL_SHADE)
    return bg


def yesno_art(cursor):
    bg = page_base("yesno")
    cv = Canvas(bg)
    tx, ty, tw, th = M.YESNO_T
    y = ty * 8 + cursor * 16
    Wn.selection_bar(cv, tx * 8 + 2, y + 1, tw * 8 - 4, 14)
    return bg


def crop_cells(im, rect):
    x, y, w, h = rect
    return im.crop((x * 8, y * 8, (x + w) * 8, (y + h) * 8))


def stack(ims):
    w = ims[0].size[0]
    out = Image.new("P", (w, sum(i.size[1] for i in ims)), 0)
    out.putpalette(ims[0].getpalette())
    y = 0
    for im in ims:
        out.paste(im, (0, y))
        y += im.size[1]
    return out


def export_tray():
    gi = P("graphics", "battle_interface")
    # --- static tileset + 32x64 tilemap
    pages = {"msg": page_base("msg"), "action": page_base("action"), "moves": page_base("moves")}
    # cells under windows don't need art; page 1/2 windows cover the tray rows entirely
    tiles, tm0 = to_tiles(pages["msg"])
    tiles, tm1 = to_tiles(pages["action"], base=tiles)
    tiles, tm2 = to_tiles(pages["moves"], base=tiles)
    tiles, tmy = to_tiles(page_base("yesno"), base=tiles)
    frame = Wn.std_frame_tiles("orchid")
    tiles, tmf = to_tiles(frame, base=tiles)
    # BG0 tiles 0x10..0x2F are reserved: LoadBattleMenuWindowGfx copies the player's window
    # frame over 0x12..0x1A and 0x22..0x2A (vanilla HandleBattleWindow / level-up box frame).
    remap = lambda i: i if i < TRAY_HOLE[0] else i + (TRAY_HOLE[1] - TRAY_HOLE[0])
    blank = tuple([0] * 64)
    tiles = tiles[:TRAY_HOLE[0]] + [blank] * (TRAY_HOLE[1] - TRAY_HOLE[0]) + tiles[TRAY_HOLE[0]:]
    fix = lambda tm: [(remap(i), hf, vf) for (i, hf, vf) in tm]
    tm0, tm1, tm2, tmy, tmf = fix(tm0), fix(tm1), fix(tm2), fix(tmy), fix(tmf)
    assert len(tiles) <= TRAY_STATIC_MAX, "tray tileset %d tiles > 0x90" % len(tiles)
    sheet = tiles_to_image(tiles, pages["msg"])
    save_indexed(sheet, os.path.join(gi, "orchid_tray.png"), M.UI_PAL)

    cells = [None] * (32 * 64)
    for page, tm in enumerate((tm0, tm1, tm2)):
        for i, item in enumerate(tm):
            cells[(page * 20 + i // 30) * 32 + i % 30] = item
    write_tilemap(os.path.join(gi, "orchid_tray.bin"), cells)
    write_jasc(os.path.join(gi, "orchid_tray.pal"), pad16(M.UI_PAL))

    # move-select palette (BG pal 6): accents -> PP warning colours (text_pp.pal)
    used = set()
    for k in range(4):
        used |= set(crop_cells(move_art(k), (0, 14, 30, 6)).getdata())
    assert not used & {ACCENT_DARK, ACCENT, ACCENT_LIGHT}, used
    move_pal = list(M.UI_PAL)
    move_pal[ACCENT_DARK] = snap(M.PP_FG[0])     # <= 1/2   yellow
    move_pal[ACCENT] = snap(M.PP_FG[1])          # <= 1/4   orange
    move_pal[ACCENT_LIGHT] = snap(M.PP_FG[2])    # empty    red
    write_jasc(os.path.join(gi, "orchid_tray_moves.pal"), pad16(move_pal))

    # --- raw window panels (4bpp, window tile order = row-major of each crop)
    save_indexed(stack([crop_cells(action_art(c), ACTION_WIN) for c in range(4)]),
                 os.path.join(gi, "orchid_action_panels.png"), M.UI_PAL)
    mv = []
    for slot in range(4):
        mv.append(crop_cells(move_art(-1), MOVE_WIN[slot]))
        mv.append(crop_cells(move_art(slot), MOVE_WIN[slot]))
    save_indexed(stack(mv), os.path.join(gi, "orchid_move_panels.png"), move_pal)
    save_indexed(stack([crop_cells(yesno_art(c), YESNO_WIN) for c in range(2)]),
                 os.path.join(gi, "orchid_yesno_panels.png"), M.UI_PAL)

    # --- action icon fields (OBJ, BTN_PAL)
    fight = M.p_sheet(32, 32, M.BTN_PAL)
    M.draw_field(Canvas(fight), 0, 0, 32, 22, "red", "fight", r=4)
    save_indexed(fight, os.path.join(gi, "orchid_action_fight.png"), M.BTN_PAL)
    side = M.p_sheet(16, 48, M.BTN_PAL)
    for i in range(3):
        M.draw_field(Canvas(side), 0, i * 16, M.SIDE_FIELD_W, 14, M.BTN_COL[i + 1], M.BTN_ICON[i + 1])
    save_indexed(side, os.path.join(gi, "orchid_action_side.png"), M.BTN_PAL)

    def entries(tm, rect):
        x, y, w, h = rect
        out = []
        for ty in range(y, y + h):
            for tx in range(x, x + w):
                idx, hf, vf = tm[ty * 30 + tx]
                out.append(idx | (hf << 10) | (vf << 11))
        return out

    return dict(n_tiles=len(tiles), dock=entries(tmy, YESNO_DOCK), dock_base=entries(tm0, YESNO_DOCK),
                frame=[(i | (hf << 10) | (vf << 11)) for (i, hf, vf) in tmf])


def tray_header_lines(t):
    L = ["// ---- BG0 tray (pages: 0 message, 1 action menu, 2 move select)",
         "#define ORCHID_TRAY_NUM_TILES %d" % t["n_tiles"],
         "#define ORCHID_TRAY_BG_PAL    0   // BG palette of the tray / message / action / YES-NO",
         "#define ORCHID_MOVES_BG_PAL   6   // BG palette of the move pills (tray + PP colours), loaded on demand",
         "#define ORCHID_COL_INK        %d" % INK,
         "#define ORCHID_COL_WHITE      %d" % WHITE,
         "#define ORCHID_COL_PANEL      %d" % PANEL,
         "#define ORCHID_COL_SHADE      %d" % PANEL_SHADE,
         "#define ORCHID_COL_PANEL_DARK %d" % PANEL_DARK,
         "#define ORCHID_COL_SELECT     %d" % SELECT,
         "#define ORCHID_COL_PP_YELLOW  %d" % ACCENT_DARK,
         "#define ORCHID_COL_PP_ORANGE  %d" % ACCENT,
         "#define ORCHID_COL_PP_RED     %d" % ACCENT_LIGHT, ""]
    for name, r in (("ACTION", ACTION_WIN), ("PROMPT", PROMPT_WIN), ("YESNO", YESNO_WIN), ("DOCK", YESNO_DOCK)):
        L.append("#define ORCHID_%s_WIN_X %d" % (name, r[0]))
        L.append("#define ORCHID_%s_WIN_Y %d   // tile row within the page" % (name, r[1]))
        L.append("#define ORCHID_%s_WIN_W %d" % (name, r[2]))
        L.append("#define ORCHID_%s_WIN_H %d" % (name, r[3]))
    L.append("")
    ax, ay = ACTION_WIN[0] * 8, ACTION_WIN[1] * 8
    fx, fy, fw, fh = M.FIGHT_BTN
    L.append("// action labels (window px): FIGHT centred in the round button, side labels after the icon field")
    L.append("#define ORCHID_FIGHT_LABEL_CX %d   // centre x; label x = CX - width / 2 (+1 like the mockup)" % (fx - ax + fw // 2))
    L.append("#define ORCHID_FIGHT_LABEL_Y  %d" % (fy + 25 - ay))
    L.append("#define ORCHID_SIDE_LABEL_X   %d" % (M.SIDE_X + M.SIDE_FIELD_W + 3 - ax))
    L.append("UNUSED static const u8 sOrchidSideLabelY[3] = {%s};" % ", ".join(str(y - 1 - ay) for y in M.SIDE_Y))
    L.append("// icon fields (OBJ centres, screen)")
    ffx, ffy, _, _ = M.FIGHT_FIELD
    L.append("#define ORCHID_FIGHT_ICON_X %d" % (ffx + 16))
    L.append("#define ORCHID_FIGHT_ICON_Y %d" % (ffy + 16))
    L.append("#define ORCHID_SIDE_ICON_X  %d" % (M.SIDE_X + 8))
    L.append("UNUSED static const u8 sOrchidSideIconY[3] = {%s};" % ", ".join(str(y + 8) for y in M.SIDE_Y))
    L.append("")
    L.append("// move pills: window rects (tiles, page row) and pill origin inside the window (px)")
    L.append("UNUSED static const u8 sOrchidMoveWin[4][4] = {%s};" % ", ".join("{%d, %d, %d, %d}" % r for r in MOVE_WIN))
    L.append("UNUSED static const u8 sOrchidMovePillOrigin[4][2] = {%s};" % ", ".join(
        "{%d, %d}" % (x - MOVE_WIN[i][0] * 8, y - M.TRAY_Y if False else y - MOVE_WIN[i][1] * 8) for i, (x, y) in enumerate(M.MOVE_POS)))
    L.append("UNUSED static const u8 sOrchidMovePillScreen[4][2] = {%s};" % ", ".join("{%d, %d}" % p for p in M.MOVE_POS))
    L.append("#define ORCHID_MOVE_W %d" % M.MOVE_W)
    L.append("#define ORCHID_MOVE_H %d" % M.MOVE_H)
    L.append("#define ORCHID_MOVE_NAME_DX 38")
    L.append("#define ORCHID_MOVE_NAME_DY (-1)")
    L.append("#define ORCHID_MOVE_NAME_MAX %d  // wider names use FONT_NARROW" % (M.MOVE_W - 42))
    L.append("#define ORCHID_MOVE_ICON_DX 3   // type icon top-left in the pill")
    L.append("#define ORCHID_MOVE_ICON_DY 3")
    L.append("")
    L.append("// YES/NO text (window px)")
    L.append("#define ORCHID_YESNO_TEXT_X 8")
    L.append("#define ORCHID_YESNO_MSG_WIDTH %d  // message wrap width while the YES/NO is docked" % M.YESNO_MSG_W)
    L.append("")
    L.append("// YES/NO dock: BG0 page-0 tilemap cells (ORCHID_DOCK_WIN rect), docked / undocked")
    for nm, key in (("sOrchidDockTiles", "dock"), ("sOrchidDockBaseTiles", "dock_base")):
        L.append("UNUSED static const u16 %s[] = {" % nm)
        v = t[key]
        for i in range(0, len(v), YESNO_DOCK[2]):
            L.append("    " + ", ".join("0x%03X" % e for e in v[i:i + YESNO_DOCK[2]]) + ",")
        L.append("};")
    L.append("// std frame 3x3 (TL T TR / L C R / BL B BR) for HandleBattleWindow on BG0")
    L.append("UNUSED static const u16 sOrchidFrameTiles[9] = {%s};" % ", ".join("0x%03X" % e for e in t["frame"]))
    L.append("")
    return L


# ------------------------------------------------------------------ party lineup (trainer battles)
LINEUP_FRAMES = ["ok", "empty", "fnt", "psn", "par", "slp", "frz", "brn"]


def export_lineup():
    gi = P("graphics", "battle_interface")
    bars = M.p_sheet(96, 48, BX.HB_PAL)    # row 2, first 32x16 block: socket-free filler (exit drift)
    # player bar: left edge at LU_POS x; opponent bar: drawn from x-6, the sprite starts at -4
    big = M.p_sheet(W + 16, H, BX.HB_PAL)
    px, py = M.LU_POS["plr"]
    BX.lineup_bar(Canvas(big), px, py, "plr")
    bars.paste(big.crop((px, py, px + 96, py + 16)), (0, 0))
    big = M.p_sheet(W + 16, H, BX.HB_PAL)
    ox, oy = M.LU_POS["opp"]
    BX.lineup_bar(Canvas(big), ox + 8, oy, "opp")          # +8: keep the off-screen part on the canvas
    bars.paste(big.crop((ox + 4, oy, ox + 4 + 96, oy + 16)), (0, 16))
    long = M.p_sheet(200, 16, BX.HB_PAL)
    BX.mask_box(Canvas(long), 0, 0, BX.chamfer_mask(200, 16), BX.FRAME, INK, BX.BRASS, BX.FRAME_DARK)
    bars.paste(long.crop((80, 0, 112, 16)), (0, 32))
    save_indexed(bars, os.path.join(gi, "orchid_lineup_bars.png"), BX.HB_PAL)

    balls = M.p_sheet(16, 16 * len(LINEUP_FRAMES), BX.LINEUP_PAL)
    for i, st in enumerate(LINEUP_FRAMES):
        BX.lineup_ball(Canvas(balls), 0, i * 16, st)
    save_indexed(balls, os.path.join(gi, "orchid_lineup_balls.png"), BX.LINEUP_PAL)
    sx = [BX.lineup_socket(px, py, "plr", k)[0] for k in range(6)]
    so = [BX.lineup_socket(ox, oy, "opp", k)[0] for k in range(6)]
    return dict(plr=(px, py, sx[0] - px, sx[1] - sx[0], BX.lineup_socket(px, py, "plr", 0)[1] - py),
                opp=(ox - 4, oy, so[0] - (ox - 4), so[1] - so[0]))


def lineup_header_lines(lu):
    px, py, p0, pstep, sdy = lu["plr"]
    ox, oy, o0, ostep = lu["opp"]
    L = ["// ---- party lineup (trainer battles): bar = 3x 32x16 OBJ, balls = 16x16 OBJ (socket top-left)",
         "#define ORCHID_LINEUP_PLR_X       %d   // bar sprite left / top (singles)" % px,
         "#define ORCHID_LINEUP_PLR_Y       %d" % py,
         "#define ORCHID_LINEUP_OPP_X       %d" % ox,
         "#define ORCHID_LINEUP_OPP_Y       %d" % oy,
         "#define ORCHID_LINEUP_PLR_SOCKET0 %d   // socket k=0 (nearest the centre) x from the bar left" % p0,
         "#define ORCHID_LINEUP_OPP_SOCKET0 %d" % o0,
         "#define ORCHID_LINEUP_PITCH       %d   // socket step towards the screen edge" % abs(pstep),
         "#define ORCHID_LINEUP_SOCKET_DY   %d" % sdy,
         "#define ORCHID_LINEUP_VANILLA_DY  %d   // bar top = vanilla bar_Y + this" % (py - 96)]
    for i, f in enumerate(LINEUP_FRAMES):
        L.append("#define ORCHID_BALL_%-6s %d" % (f.upper(), i))
    L.append("")
    return L


# ------------------------------------------------------------------ doubles / multi + Safari boxes (phase 2)
import mock_battle_more as MB


def _no_text_more(fn):
    saved = (MB.draw_text,)
    MB.draw_text = lambda *a, **k: 0
    try:
        return _no_text(fn)
    finally:
        (MB.draw_text,) = saved


def export_more_boxes():
    """Compact doubles boxes (player / opponent) and the Safari player box."""
    info = {}
    for side, mon in (("plr", M.default_player()), ("opp", M.default_enemy())):
        sheet = M.p_sheet(W + 16, H, BX.HB_PAL)
        an = _no_text_more(lambda: MB.hb_compact(Canvas(sheet), mon, side, 0, 0))
        name = "player" if side == "plr" else "opponent"
        save_indexed(sheet.crop((0, 0, 128, 32)), P("graphics", "battle_interface", "orchid_healthbox_doubles_%s.png" % name), BX.HB_PAL)
        bars = M.p_sheet(W, H, M.HBAR_PAL)
        M.draw_bars(Canvas(bars), mon, an, hp=0, exp=0.0)
        bx, by = 24, 18
        save_indexed(bars.crop((bx, by, bx + 128, by + 8)), P("graphics", "battle_interface", "orchid_healthbar_doubles_%s.png" % name), M.HBAR_PAL)
        px0, py0 = an["status"][0] + 18, MB.C_BODY_Y + 1
        d = dict(status=an["status"], pill=(px0, py0, MB.CW - 5 - px0, 10), name=(px0 + 4, py0 - 2),
                 tab=(MB.CW - MB.C_TAB_W, MB.C_TAB_W, MB.C_TAB_H), right=MB.CW - 5,
                 strip=(bx, by), bar=(an["bar"][0] - bx, an["bar"][1] - by), exp=None)
        if an["exp"]:
            ex0, ex1, ey, _ = an["exp"]
            d["exp"] = (ex0 - bx, ey - by, ex1 - ex0 + 1)
        info["d" + side] = d

    # Safari: player box B frame, SAFARI BALLS baked into the pill, no HP / EXP
    x, y, w, h = BX.hb_rect("B", "plr")
    sheet = M.p_sheet(W, H, BX.HB_PAL)
    real_rect = BX.hb_rect
    BX.hb_rect = lambda v, side: real_rect(v, "plr")
    try:
        _no_text(lambda: BX.hb_B(Canvas(sheet), M.default_player(), "safari"))
    finally:
        BX.hb_rect = real_rect
    px0, py0 = x + 7 + 19, y + 8 + 2
    draw_text(Canvas(sheet), px0 + 5, py0 - 1, "SAFARI BALLS", INK, PANEL_SHADE, font="small")
    save_indexed(sheet.crop((x, y, x + 128, y + 32)), P("graphics", "battle_interface", "orchid_healthbox_safari.png"), BX.HB_PAL)
    return info


def more_header_lines(info):
    L = ["// ---- per-layout healthbox geometry (box px; bar strip px for BAR / EXP)",
         "struct OrchidBoxLayout",
         "{",
         "    u8 statusX, statusY;",
         "    u8 pillX, pillY, pillW, pillH, nameDX; s8 nameDY;",
         "    u8 tabX, tabW, tabH, textRight;",
         "    u8 stripDX, stripDY, barX, barY;",
         "    u8 expX, expY, expW;",
         "};",
         "enum { ORCHID_LAYOUT_PLR, ORCHID_LAYOUT_OPP, ORCHID_LAYOUT_DPLR, ORCHID_LAYOUT_DOPP, ORCHID_LAYOUT_SAFARI, ORCHID_LAYOUT_COUNT };",
         "UNUSED static const struct OrchidBoxLayout sOrchidBoxLayouts[ORCHID_LAYOUT_COUNT] =",
         "{"]
    def row(name, st, pill, ndx, ndy, tab, right, strip, bar, exp):
        e = exp or (0, 0, 0)
        L.append("    [%s] = {%d, %d,  %d, %d, %d, %d, %d, %d,  %d, %d, %d, %d,  %d, %d, %d, %d,  %d, %d, %d}," %
                 ((name,) + tuple(st) + tuple(pill) + (ndx, ndy) + tuple(tab) + (right,) + tuple(strip) + tuple(bar) + tuple(e)))
    for side, name in (("plr", "ORCHID_LAYOUT_PLR"), ("opp", "ORCHID_LAYOUT_OPP")):
        d = info["s" + side]
        row(name, d["status"], d["pill"], 5, -1, (d["tab"][0], d["tab"][2], d["tab"][3]), 123, (24, 23), d["bar"], d.get("exp"))
    for side, name in (("plr", "ORCHID_LAYOUT_DPLR"), ("opp", "ORCHID_LAYOUT_DOPP")):
        d = info["d" + side]
        row(name, d["status"], d["pill"], d["name"][0] - d["pill"][0], d["name"][1] - d["pill"][1], d["tab"], d["right"], d["strip"], d["bar"], d["exp"])
    d = info["splr"]
    row("ORCHID_LAYOUT_SAFARI", d["status"], d["pill"], 5, -1, (d["tab"][0], d["tab"][2], d["tab"][3]), 123, (24, 23), d["bar"], None)
    L.append("};")
    L.append("// doubles box top-left per B_POSITION (player left / opp left / player right / opp right)")
    pos = MB.C_POS
    L.append("UNUSED static const s16 sOrchidDoublesBoxPos[4][2] = {{%d, %d}, {%d, %d}, {%d, %d}, {%d, %d}};" %
             (pos["plr"][0] + pos["opp"][0] + pos["plr"][1] + pos["opp"][1]))
    L.append("// Safari Ball stamp before the ball count (mock_battle_more.SAFARI_BALL), healthbox palette")
    cmap = {"I": INK, "G": BX.BRASS, "g": BX.BRASS_DARK, "W": WHITE, ".": 0}
    L.append("UNUSED static const u8 sOrchidSafariBall[7][7] = {")
    for r in MB.SAFARI_BALL:
        L.append("    {" + ", ".join(str(cmap[c]) for c in r) + "},")
    L.append("};")
    L.append("")
    return L


def write_header(info, tray, lineup):
    L = ["// GENERATED by dev_scripts/orchid_ui/export_battle.py — do not edit by hand.",
         "// Orchid battle UI layout (healthbox direction B; see dev_scripts/orchid_ui/mock_battle.py).",
         "#ifndef GUARD_DATA_BATTLE_ORCHID_UI_H",
         "#define GUARD_DATA_BATTLE_ORCHID_UI_H", ""]
    L.append("// Healthbox palette roles (battle_ext.HB_PAL)")
    for k, v in (("INK", INK), ("FRAME_DARK", BX.FRAME_DARK), ("WHITE", WHITE), ("PANEL_SHADE", PANEL_SHADE),
                 ("MALE", BX.HB_MALE), ("MALE_SHADOW", BX.HB_MALE_SH), ("FEMALE", BX.HB_FEMALE),
                 ("FEMALE_SHADOW", BX.HB_FEMALE_SH), ("BRASS_LIGHT", BX.BRASS_LIGHT)):
        L.append("#define OHB_COL_%-14s %d" % (k, v))
    L.append("")
    L.append("// Healthbar palette roles (mock_battle.HBAR_PAL)")
    for k, v in M.HB_I.items():
        L.append("#define OHB_BAR_%-8s %d" % (k.upper(), v))
    L.append("")
    for side, tag in (("plr", "PLR"), ("opp", "OPP")):
        d = info[side]
        L.append("// %s box: screen rect (%d, %d) %dx%d" % ("Player" if side == "plr" else "Opponent", d["x"], d["y"], d["w"], d["h"]))
        L.append("#define OHB_%s_X            %d   // box left / top on screen" % (tag, d["x"]))
        L.append("#define OHB_%s_Y            %d" % (tag, d["y"]))
        L.append("#define OHB_%s_H            %d" % (tag, d["h"]))
        L.append("#define OHB_%s_STATUS_X     %d   // status icon top-left in the box" % (tag, d["status"][0]))
        L.append("#define OHB_%s_STATUS_Y     %d" % (tag, d["status"][1]))
        L.append("#define OHB_%s_PILL_X       %d   // name pill rect in the box" % (tag, d["pill"][0]))
        L.append("#define OHB_%s_PILL_Y       %d" % (tag, d["pill"][1]))
        L.append("#define OHB_%s_PILL_W       %d" % (tag, d["pill"][2]))
        L.append("#define OHB_%s_PILL_H       %d" % (tag, d["pill"][3]))
        L.append("#define OHB_%s_TAB_X        %d   // top tab rect in the box" % (tag, d["tab"][0]))
        L.append("#define OHB_%s_TAB_W        %d" % (tag, d["tab"][2]))
        L.append("#define OHB_%s_TAB_H        %d" % (tag, d["tab"][3]))
        L.append("#define OHB_%s_BAR_X        %d   // HP bar outline top-left in the 128x8 bar strip" % (tag, d["bar"][0]))
        L.append("#define OHB_%s_BAR_Y        %d" % (tag, d["bar"][1]))
        if "exp" in d:
            L.append("#define OHB_%s_EXP_X        %d   // EXP strip in the bar strip" % (tag, d["exp"][0]))
            L.append("#define OHB_%s_EXP_Y        %d" % (tag, d["exp"][1]))
            L.append("#define OHB_%s_EXP_W        %d" % (tag, d["exp"][2]))
        L.append("")
    L.append("#define OHB_BAR_STRIP_DX  24   // bar strip left / top relative to the box")
    L.append("#define OHB_BAR_STRIP_DY  23")
    L.append("#define OHB_HP_PIXELS     48")
    L.append("#define OHB_NAME_MAX_SMALL 50  // names wider than this in FONT_SMALL use FONT_NARROW")
    L.append("")
    L.append("// Caught ball stamp (battle_ext.CAUGHT), 7x7, healthbox palette indices, 0 = skip")
    cmap = {"I": INK, "R": BX.HB_FEMALE, "W": WHITE, ".": 0}
    L.append("UNUSED static const u8 sOrchidCaughtBall[7][7] = {")
    for row in BX.CAUGHT:
        L.append("    {" + ", ".join(str(cmap[c]) for c in row) + "},")
    L.append("};")
    L.append("")
    L += tray_header_lines(tray)
    L += lineup_header_lines(lineup)
    L += more_header_lines(dict(info, **{"s" + k: v for k, v in info.items() if k in ("plr", "opp")}))
    L.append("#endif // GUARD_DATA_BATTLE_ORCHID_UI_H")
    with open(P("src", "data", "battle_orchid_ui.h"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    info = export_healthboxes()
    info.update(export_more_boxes())
    tray = export_tray()
    lineup = export_lineup()
    write_header(info, tray, lineup)
    print("tray tiles:", tray["n_tiles"])
    print("healthboxes:", sorted(info))
