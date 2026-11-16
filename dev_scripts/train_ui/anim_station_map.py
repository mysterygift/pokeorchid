"""
Station map navigation GIF (GBA frames at 60 fps, GIF keeps every 2nd frame, 3x).

Sequence: open on MARIS BAY -> UP-RIGHT to VALE JUNCTION -> RIGHT toward greyed KORU CITY
(denied: ring shakes, grey ring blinks on KORU, tray message) -> UP to TELOK TOWN -> A -> YES/NO.

Timing (GBA frames, proposals):
    RING_TRAVEL  = 8    ring slides to the new node, ease-out; pill + tray update on arrival
    DENY_SHAKE   = 12   ring x offset +2,+2,0,-2,-2,0 (x2); grey ring on the target blinks 4 on / 4 off
    grid scroll  = 1px every 4 frames, diagonal (kit backdrop rule)

usage: python anim_station_map.py
"""
from common import *
import station_map as M

RING_TRAVEL = 8
DENY_SHAKE = 12
SHAKE = [2, 2, 0, -2, -2, 0] * 2


def ease_out(t, n):
    u = min(1.0, (t + 1) / n)
    return 1 - (1 - u) ** 2


def build():
    frames = []
    # (start frame, kind, arg)
    script = [(0, "at", "MARIS BAY"), (50, "move", "VALE JUNCTION"), (110, "deny", "KORU CITY"),
              (200, "move", "TELOK TOWN"), (260, "confirm", None)]
    end = 330
    cur, prev, since, deny_since, deny_target, msg = "MARIS BAY", None, 0, None, None, None
    for f in range(end):
        for s, kind, arg in script:
            if f == s:
                if kind == "move":
                    prev, cur, since, msg = cur, arg, f, None
                elif kind == "deny":
                    deny_since, deny_target = f, arg
                    msg = "You haven't been to %s yet.\nVisit it on foot first." % arg
        kw = dict(cursor=cur, scroll=f // 4, tray_msg=msg)
        if prev and f - since < RING_TRAVEL:
            (ax, ay), (bx, by) = M.STATIONS[prev][:2], M.STATIONS[cur][:2]
            k = ease_out(f - since, RING_TRAVEL)
            kw["ring_at"] = (ax + (bx - ax) * k, ay + (by - ay) * k)
        if deny_since is not None and f - deny_since < DENY_SHAKE + 24:
            t = f - deny_since
            if t < DENY_SHAKE:
                kw["ring_dx"] = SHAKE[t]
            if (t // 4) % 2 == 0:
                kw["deny"] = deny_target
        if f >= 260:
            kw["popup"] = lambda out: M.confirm_popup(out, cur)
        frames.append(M.render(**kw))
    return frames


if __name__ == "__main__":
    ensure_out()
    fr = build()
    n = save_gif(fr, os.path.join(OUT, "map_nav_3x.gif"), scale=3, step=2)
    print("map_nav_3x.gif", len(fr), "GBA frames,", n, "GIF frames")
