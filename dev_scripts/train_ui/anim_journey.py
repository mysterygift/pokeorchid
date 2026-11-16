"""
Storyboard GIF of a train journey (240x160, GBA frames at 60 fps, GIF keeps every 2nd frame
= 30 fps, upscaled 3x). Camera is fixed for the whole sequence.

All timing below is in GBA frames so it can become C constants 1:1
(also written to out/journey_timing.txt).

Outputs: out/journey_3x.gif, out/journey_storyboard.png (key frames), out/journey_timing.txt
usage: python anim_journey.py
"""
from common import *
import journey_scene as S

# ------------------------------------------------------------------ phase lengths (GBA frames)
# Engine values (already in C on train-system): ARRIVE 96 ease-out, SETTLE 16, DOOR 12,
# player STEP 16, DEPART 80 ease-in. The rest are storyboard beats (proposals).
IDLE_START = 40          # train parked, player on the platform edge facing the door
DOOR_OPEN = 12           # engine: door 12f (shut frame -> open frame at the half-way point)
DOOR_HOLD = 8            # short beat before the player moves
BOARD_WALK = 16          # engine: player step 16f (1 px/frame)
BOARD_HIDE = 8           # player sprite invisible, door still open
DOOR_CLOSE = 12          # engine: door 12f
DEPART_WAIT = 24
DEPART = 80              # engine: 80f ease-in, parked -> train's left edge at x = 240
FADE_OUT = 16            # palette fade to black (16 steps)
BLACK = 16               # warp happens here
FADE_IN = 16
ARRIVE_WAIT = 20         # empty platform
ARRIVE = 96              # engine: 96f ease-out, left edge from -192 to the stop x
ARRIVE_SETTLE = 16       # engine: settle 16f
ALIGHT_APPEAR = 8        # player shown in the open door, facing down
ALIGHT_WALK = 16         # engine: player step 16f
LEAVE_WAIT = 30          # decided in round 1: the train leaves after you alight
LEAVE = 80               # same as DEPART
END_HOLD = 60

# layout
DEPART_COL = 7           # player's tile column at TOSA PORT (door column)
ARRIVE_COL = 8           # arrival tile column at TELOK TOWN
TRAIN_X_DEPART = DEPART_COL * 16 - S.TRAIN_DOOR_X        # 24
TRAIN_X_ARRIVE = ARRIVE_COL * 16 - S.TRAIN_DOOR_X        # 40


def depart_path(x0, n=DEPART):
    """Ease-in (quadratic — the C curve may differ) from x0 until the left edge reaches 240."""
    return [x0 + int((W - x0) * ((i + 1) / n) ** 2) for i in range(n)]


def arrive_path(stop, n=ARRIVE):
    """Ease-out (quadratic) from fully off-screen left (x = -192) to the stop x."""
    x0 = -S.TRAIN_W
    return [x0 + int(round((stop - x0) * (1 - (1 - (i + 1) / n) ** 2))) for i in range(n)]


# ------------------------------------------------------------------ actors
def player(frame, hflip=False):
    return brendan(frame, hflip)


def walk_frame(t, frames):
    """Gen 3 single step: walk frame for 8 frames, then standing frame."""
    return frames[0] if t < 8 else None


def compose(station, train_x=None, door="closed", ply=None, npcs=(), fade=0):
    out = S.scene(station)
    if train_x is not None:
        out.alpha_composite(S.train_rgba(door == "open"), (train_x, S.TRAIN_Y))
    for spr, x, y in npcs:
        out.alpha_composite(spr, (x, y))
    if ply is not None:
        spr, x, y = ply
        out.alpha_composite(spr, (x, y))
    if fade:
        k = fade / 16
        black = Image.new("RGBA", out.size, (0, 0, 0, 255))
        out = Image.blend(out, black, k)
    return out


def door_state(t, opening):
    """t frames into a 12-frame door phase. train.png has only shut/open frames: swap at 6."""
    if opening:
        return "open" if t >= DOOR_OPEN // 2 else "closed"
    return "closed" if t >= DOOR_CLOSE // 2 else "open"


# ------------------------------------------------------------------ timeline
def build():
    frames, marks = [], []
    attendant_a = (npc("clerk", F_LEFT, "npc_white", hflip=True), 3 * 16, 5 * 16 - 16)
    attendant_b = (npc("clerk", F_LEFT, "npc_white"), 12 * 16, 6 * 16 - 16)
    px_dep = DEPART_COL * 16
    px_arr = ARRIVE_COL * 16
    edge_y = S.EDGE_ROW * 16 - 16          # player sprite top on the platform edge row
    track_y = S.TRACK_ROW * 16 - 16        # ... on the track row (inside the door)

    def add(label, img):
        frames.append(img)
        if label:
            marks.append((label, len(frames) - 1))

    A, B = "TOSA PORT", "TELOK TOWN"
    stand_up = (player(F_UP), px_dep, edge_y)
    for t in range(IDLE_START):
        add("1 Parked, player faces the door" if t == 20 else None,
            compose(A, TRAIN_X_DEPART, "closed", stand_up, [attendant_a]))
    for t in range(DOOR_OPEN):
        add("2 Door opens" if t == 8 else None,
            compose(A, TRAIN_X_DEPART, door_state(t, True), stand_up, [attendant_a]))
    for t in range(DOOR_HOLD):
        add(None, compose(A, TRAIN_X_DEPART, "open", stand_up, [attendant_a]))
    for t in range(BOARD_WALK):
        f = F_WALK_UP[0] if t < 8 else F_UP
        add("3 Player steps into the door" if t == 10 else None,
            compose(A, TRAIN_X_DEPART, "open", (player(f), px_dep, edge_y - (t + 1)), [attendant_a]))
    for t in range(BOARD_HIDE):
        add(None, compose(A, TRAIN_X_DEPART, "open", None, [attendant_a]))
    for t in range(DOOR_CLOSE):
        add("4 Door closes" if t == 9 else None,
            compose(A, TRAIN_X_DEPART, door_state(t, False), None, [attendant_a]))
    for t in range(DEPART_WAIT):
        add(None, compose(A, TRAIN_X_DEPART, "closed", None, [attendant_a]))
    dep = depart_path(TRAIN_X_DEPART)
    for i, x in enumerate(dep):
        add("5 Accelerates right, camera fixed" if i == len(dep) // 2 else None,
            compose(A, x, "closed", None, [attendant_a]))
    for t in range(FADE_OUT):
        add("6 Fade to black" if t == 10 else None,
            compose(A, None, npcs=[attendant_a], fade=t + 1))
    for t in range(BLACK):
        add(None, Image.new("RGBA", (W, H), (0, 0, 0, 255)))
    for t in range(FADE_IN):
        add("7 New station, empty platform" if t == 14 else None,
            compose(B, None, npcs=[attendant_b], fade=16 - t - 1))
    for t in range(ARRIVE_WAIT):
        add(None, compose(B, None, npcs=[attendant_b]))
    arr = arrive_path(TRAIN_X_ARRIVE)
    for i, x in enumerate(arr):
        add("8 Enters from the left, brakes" if i == len(arr) - 20 else None,
            compose(B, x, "closed", None, [attendant_b]))
    for t in range(ARRIVE_SETTLE):
        add("9 Stops: door on the arrival tile" if t == 8 else None,
            compose(B, TRAIN_X_ARRIVE, "closed", None, [attendant_b]))
    for t in range(DOOR_OPEN):
        add(None, compose(B, TRAIN_X_ARRIVE, door_state(t, True), None, [attendant_b]))
    for t in range(ALIGHT_APPEAR):
        add(None, compose(B, TRAIN_X_ARRIVE, "open", (player(F_DOWN), px_arr, track_y), [attendant_b]))
    for t in range(ALIGHT_WALK):
        f = F_WALK_DOWN[0] if t < 8 else F_DOWN
        add("10 Player steps down" if t == 6 else None,
            compose(B, TRAIN_X_ARRIVE, "open", (player(f), px_arr, track_y + t + 1), [attendant_b]))
    stand_dn = (player(F_DOWN), px_arr, edge_y)
    for t in range(DOOR_CLOSE):
        add(None, compose(B, TRAIN_X_ARRIVE, door_state(t, False), stand_dn, [attendant_b]))
    for t in range(LEAVE_WAIT):
        add(None, compose(B, TRAIN_X_ARRIVE, "closed", stand_dn, [attendant_b]))
    lv = depart_path(TRAIN_X_ARRIVE)
    for i, x in enumerate(lv):
        add("11 Train leaves (decided)" if i == len(lv) // 2 else None,
            compose(B, x, "closed", stand_dn, [attendant_b]))
    for t in range(END_HOLD):
        add("12 Control returns" if t == 30 else None, compose(B, None, None, stand_dn, [attendant_b]))
    return frames, marks, len(dep), len(arr), len(lv)


def storyboard(frames, marks, path):
    from PIL import ImageDraw
    k, cols = 2, 4
    cw, ch = W * k, H * k
    rows = (len(marks) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 16) + 16, rows * (ch + 30) + 16), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    for i, (label, fi) in enumerate(marks):
        x, y = 16 + (i % cols) * (cw + 16), 16 + (i // cols) * (ch + 30)
        d.text((x, y), "%s  (frame %d)" % (label, fi), fill=(230, 230, 240))
        sheet.paste(KX.upscale(frames[fi].convert("RGB"), k), (x, y + 16))
    sheet.save(path)


def timing_text(n_dep, n_arr, n_lv):
    rows = [
        ("IDLE_START", IDLE_START, "storyboard beat"), ("DOOR_OPEN", DOOR_OPEN, "engine"),
        ("DOOR_HOLD", DOOR_HOLD, "storyboard beat"), ("BOARD_WALK", BOARD_WALK, "engine (player step)"),
        ("BOARD_HIDE", BOARD_HIDE, "storyboard beat"), ("DOOR_CLOSE", DOOR_CLOSE, "engine"),
        ("DEPART_WAIT", DEPART_WAIT, "storyboard beat"), ("DEPART", n_dep, "engine, ease-in"),
        ("FADE_OUT", FADE_OUT, "storyboard beat"), ("BLACK", BLACK, "storyboard beat (warp)"),
        ("FADE_IN", FADE_IN, "storyboard beat"), ("ARRIVE_WAIT", ARRIVE_WAIT, "storyboard beat"),
        ("ARRIVE", n_arr, "engine, ease-out"), ("ARRIVE_SETTLE", ARRIVE_SETTLE, "engine"),
        ("ALIGHT_APPEAR", ALIGHT_APPEAR, "storyboard beat"), ("ALIGHT_WALK", ALIGHT_WALK, "engine (player step)"),
        ("LEAVE_WAIT", LEAVE_WAIT, "storyboard beat"), ("LEAVE", n_lv, "engine, ease-in (= DEPART)"),
        ("END_HOLD", END_HOLD, "storyboard beat"),
    ]
    lines = ["// Tosa Rail journey storyboard timing (GBA frames @ 60 fps) — generated by anim_journey.py"]
    for n, v, note in rows:
        lines.append("%-16s %4d   // %s" % (n, v, note))
    lines.append("// door: train left edge -> door left edge = %d px; train top = track row y + 16 - 64" % S.TRAIN_DOOR_X)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ensure_out()
    frames, marks, n_dep, n_arr, n_lv = build()
    n = save_gif(frames, os.path.join(OUT, "journey_3x.gif"), scale=3, step=2)
    storyboard(frames, marks, os.path.join(OUT, "journey_storyboard.png"))
    open(os.path.join(OUT, "journey_timing.txt"), "w").write(timing_text(n_dep, n_arr, n_lv))
    print(timing_text(n_dep, n_arr, n_lv))
    print("GBA frames:", len(frames), "(%.1f s)" % (len(frames) / FPS), "GIF frames:", n)
