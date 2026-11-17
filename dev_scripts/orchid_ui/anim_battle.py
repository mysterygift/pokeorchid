"""
Animated previews of the Orchid battle UI (2x GIFs, GBA frames at 60 fps,
one GIF frame every 2 GBA frames -> duration 33 ms).

  action_menu.gif  gold pill FIGHT -> BAG -> POKéMON -> RUN -> FIGHT, A opens move select,
                   cursor walks the moves, B returns.
  hp_drain.gif     'Grovyle used Absorb!' prints (MID text speed, 4 f/char), the foe blinks,
                   its HP bar drains 1 HP/frame (max HP < 48 -> Gen 3 moves 1 HP per frame),
                   colour steps at 24 / 9 bar pixels; crit message; the drain heals Grovyle
                   1 bar pixel per frame (max HP >= 48), then the drain message prints.
  exp_levelup.gif  EXP strip fills 1 px/frame, the player box flashes, Lv 18 -> 19.
  lineup.gif       trainer-battle party lineups: bars slide in (5 px/frame, 20 f), balls zip in one by
                   one (vanilla delays 10/17 + 7 f per ball, accelerating), message prints, then bars
                   and balls drift toward the centre while alpha-fading out (32 f), as vanilla.

usage: anim_battle.py OUT_DIR
"""
import os
import sys
from PIL import Image
import mock_battle as M

TEXT_SPEED = 4          # MID: frames per character
_cache = {}


def frame(key, fn):
    if key not in _cache:
        _cache[key] = fn().convert("RGB").resize((M.W * 2, M.H * 2), Image.NEAREST)
    return _cache[key]


def save(frames, path):
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=33, loop=0, optimize=False)
    print(os.path.basename(path), len(frames), "frames")


def printed(msg, f0, f):
    """Characters of msg (as wrapped for the window) printed by GBA frame f."""
    text = "\n".join(M.wrap(msg, M.MSG_W)[-2:])
    return text, max(0, min(len(text), (f - f0) // TEXT_SPEED + 1))


# ------------------------------------------------------------------ action menu
def action_menu(out):
    # (start frame, mode, cursor)
    script = [(0, "action", 0), (30, "action", 1), (54, "action", 2), (78, "action", 3), (102, "action", 0),
              (132, "moves", 0), (162, "moves", 1), (186, "moves", 3), (210, "moves", 2), (234, "moves", 0),
              (264, "action", 0)]
    end = 300
    frames = []
    for f in range(0, end, 2):
        mode, cur = [(m, c) for (s, m, c) in script if f >= s][-1]
        frames.append(frame(("am", mode, cur), lambda: M.render(mode, cur)))
    save(frames, os.path.join(out, "action_menu.gif"))


# ------------------------------------------------------------------ hit + HP drain
def hp_drain(out):
    P = M.default_player().copy(hp=30)
    E = M.default_enemy()
    m1, m2, m3 = "Grovyle used Absorb!", "A critical hit!", "The wild Zigzagoon had its energy drained!"
    t_m1 = 0
    t_blink = t_m1 + len(m1) * TEXT_SPEED + 24
    t_drain = t_blink + 32
    e_from, e_to = 24, 3
    t_m2 = t_drain + (e_from - e_to) + 16
    t_heal = t_m2 + len(m2) * TEXT_SPEED + 30
    p_from, p_to = 30, 40                       # Absorb heals half of the 21 damage
    px_from, px_to = p_from * 48 // P.maxhp, p_to * 48 // P.maxhp
    t_m3 = t_heal + (px_to - px_from) + 12
    end = t_m3 + len(m3) * TEXT_SPEED + 60
    frames = []
    for f in range(0, end, 2):
        e_hp = e_from if f < t_drain else max(e_to, e_from - (f - t_drain))
        if f < t_heal:
            p_hp = p_from
        else:
            # 1 bar pixel per frame; shown HP follows the bar
            px = min(px_to, px_from + (f - t_heal))
            p_hp = p_to if px >= px_to else max(p_from, -(-px * P.maxhp // 48))
        visible = not (t_blink <= f < t_drain and ((f - t_blink) // 4) % 2 == 0)
        if f < t_m2:
            msg, f0 = m1, t_m1
        elif f < t_m3:
            msg, f0 = m2, t_m2
        else:
            msg, f0 = m3, t_m3
        text, n = printed(msg, f0, f)
        key = ("hp", e_hp, p_hp, visible, msg, n)
        frames.append(frame(key, lambda: M.render(
            "msg", msg=msg, chars=n, player=P.copy(hp=p_hp), enemy=E.copy(hp=e_hp), enemy_visible=visible)))
    save(frames, os.path.join(out, "hp_drain.gif"))


# ------------------------------------------------------------------ EXP + level up
def exp_levelup(out):
    P = M.default_player()
    strip = M.exp_strip_px()                                   # EXP strip pixels
    m1, m2 = "Grovyle gained 64 Exp. Points!", "Grovyle grew to Lv. 19!"
    px0 = int(round(strip * P.exp))
    t_fill = 30
    t_full = t_fill + (strip - px0)
    t_flash = t_full + 4
    flash_len = 8
    t_lv = t_flash + flash_len
    t_m2 = t_lv + 6
    px_after = int(round(strip * 0.15))
    end = t_m2 + len(m2) * TEXT_SPEED + 60
    frames = []
    for f in range(0, end, 2):
        if f < t_lv:
            mon = P.copy()
            exp = min(strip, px0 + max(0, f - t_fill)) / strip
        else:
            mon = P.copy(lv=19, hp=51, maxhp=55)
            exp = min(px_after, f - t_lv) / strip
        fl = 0.0
        if t_flash <= f < t_flash + flash_len:
            u = (f - t_flash) / flash_len
            fl = 0.75 * (1 - abs(2 * u - 1))
        if f < t_m2:
            msg, n = m1, len(m1)
        else:
            msg, n = printed(m2, t_m2, f)[0].replace("\n", " "), printed(m2, t_m2, f)[1]
        key = ("xp", mon.lv, round(exp * strip), round(fl, 3), msg, n)
        frames.append(frame(key, lambda: M.render("msg", msg=msg, chars=n, player=mon, exp=exp,
                                                  flash={"plr": fl})))
    save(frames, os.path.join(out, "exp_levelup.gif"))


# ------------------------------------------------------------------ trainer-battle lineup
def _ball_track(delay, start, n, exit_dir=None):
    """Vanilla SpriteCB_StatusSummaryBalls_Enter/_Exit: after `delay` frames the ball moves with
    accelerating speed (data3 += 56, step = data3 >> 4). Returns per-frame x offsets."""
    xs, x2, d3 = [], start, 0
    for f in range(n):
        if f >= delay:
            v = d3 + 56
            d3 = v & 0xFFF0
            step = v >> 4
            if exit_dir is None:
                x2 = min(0, x2 + step) if start < 0 else max(0, x2 - step)
            else:
                x2 += step * exit_dir
        xs.append(x2)
    return xs


def lineup(out):
    msg = "You are challenged by Youngster Calvin!"
    ENTER, EXIT = 0, 210            # bars enter at once (with SE_BALL_TRAY_ENTER); exit after the message
    END = EXIT + 48
    sides = {"opp": (M.LINEUP_OPP, -100, 5, 17, -120), "plr": (M.LINEUP_PLR, 100, -5, 10, 120)}
    tracks = {}
    for side, (slots, b0, bv, d0, s0) in sides.items():
        enter = [_ball_track(d0 + 7 * k, s0, EXIT) for k in range(6)]
        ex_dir = 1 if side == "opp" else -1          # vanilla: both drift toward the screen centre
        leave = [_ball_track(7 * k, 0, END - EXIT, ex_dir) for k in range(6)]
        tracks[side] = (enter, leave)
    frames = []
    for f in range(0, END, 2):
        lus = {}
        alpha = 1.0
        if f >= EXIT:
            t = f - EXIT
            alpha = max(0.0, (16 - (t + 1) // 2) / 16)        # BLDALPHA 16 -> 0, one step / 2 frames
        for side, (slots, b0, bv, d0, s0) in sides.items():
            enter, leave = tracks[side]
            if f < EXIT:
                bar_dx = b0 + bv * min(f - ENTER, abs(b0 // bv)) if f < 20 else 0
                bdx = [enter[k][f] for k in range(6)]
            else:
                t = f - EXIT
                bar_dx = 2 * t * (1 if side == "opp" else -1)
                bdx = [leave[k][t] for k in range(6)]
            bdx = [None if abs(v) > 130 else v for v in bdx]
            lus[side] = (slots, dict(bar_dx=bar_dx, ball_dx=bdx, alpha=alpha))
        text, n = printed(msg, 24, f)
        key = ("lu", f)
        frames.append(frame(key, lambda: M.render("msg", msg=msg, chars=n if f >= 24 else 0,
                                                  intro=True, lineups=lus if alpha > 0 else None)))
    save(frames, os.path.join(out, "lineup.gif"))


if __name__ == "__main__":
    OUT = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    action_menu(OUT)
    hp_drain(OUT)
    exp_levelup(OUT)
    lineup(OUT)
