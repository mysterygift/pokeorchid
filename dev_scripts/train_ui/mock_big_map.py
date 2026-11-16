"""
Round 2: bigger TOSA RAIL network on a scrolling canvas.

Stills (1x + 3x):  big_1_open, big_2_telok, big_3_koru, big_4_rule (dead-zone box shown),
                   big_5_minimap (option 2: header mini-map instead of the legend)
Sheets:            big_overview_2x.png (whole canvas + the three framings)
GIF:               big_nav_3x.gif — cursor walks the network; the diagram pans when the cursor
                   leaves the dead zone (16f ease-out re-centre), ring travels 8f ease-out,
                   one denied press toward greyed CINDER PEAK, then A -> YES/NO.
usage: python mock_big_map.py
"""
from common import *
import big_map as B
import station_map as M


def stills():
    c_open, c_telok, c_koru = B.centre_on("MARIS BAY"), B.centre_on("TELOK TOWN"), B.centre_on("KORU CITY")
    S = [
        ("big_1_open", "1. Opening framing",
         "The map opens centred on the cursor (MARIS BAY), clamped to the canvas edge, so TOSA PORT and the "
         "head sit in the bottom-left. Red chevrons sit on the tubes where the network leaves the screen: "
         "east along the RIDGE/FOREST branch and north up the RIDGE line.",
         B.render("MARIS BAY", c_open), c_open),
        ("big_2_telok", "2. Re-centred on TELOK TOWN",
         "Pressing UP from VALE JUNCTION puts TELOK TOWN outside the dead zone, so the camera eases 16 frames "
         "to centre it. Interchanges (TELOK, VALE, KORU) use a ringed node. Chevrons now point out on all four sides.",
         B.render("TELOK TOWN", c_telok, drift=6), c_telok),
        ("big_3_koru", "3. East side — KORU CITY",
         "Clamped at the canvas's right edge. Greyed FERN GATE, CORAL END and GALE POINT show where the rest of the "
         "network goes; their tubes are grey.",
         B.render("KORU CITY", c_koru, drift=11), c_koru),
    ]
    S.append(("big_4_rule", "Dead zone (debug view)",
              "The dashed box is the dead zone (48px in from the sides, 24 from the top, 32 from the bottom so the "
              "label below a node fits). While the cursor stays inside, the diagram doesn't move.",
              B.render("TELOK TOWN", c_telok, drift=6, show_safe=True), c_telok))
    S.append(("big_5_minimap", "Option 2 — header mini-map",
              "The legend is swapped for a 32x16 OBJ mini-map (canvas at 1/16) with a gold viewport box. "
              "It gives a sense of position, but at 1/16 the stations are single pixels.",
              B.render("TELOK TOWN", c_telok, drift=6, header="minimap"), c_telok))
    return S


def ease_out(t, n):
    u = min(1.0, t / n)
    return 1 - (1 - u) ** 2


SHAKE = [2, 2, 0, -2, -2, 0] * 2


def nav_frames():
    script = [(0, "MARIS BAY"), (40, "VALE JUNCTION"), (76, "TELOK TOWN"), (120, "ASHEN PASS"),
              (160, "deny:CINDER PEAK"), (216, "TELOK TOWN"), (258, "VALE JUNCTION"),
              (294, "SALT FLATS"), (330, "KORU CITY"), (384, "confirm")]
    end = 450
    cur, prev, since = "MARIS BAY", None, 0
    cam = B.centre_on(cur)
    cam_from, cam_to, cam_since = cam, cam, -999
    deny_since, deny_tgt, msg, popup = None, None, None, None
    frames = []
    for f in range(end):
        for s, ev in script:
            if f != s or s == 0:
                continue
            if ev.startswith("deny:"):
                deny_since, deny_tgt = f, ev[5:]
                msg = "You haven't been to %s yet.\nVisit it on foot first." % deny_tgt
            elif ev == "confirm":
                popup = (lambda c: (lambda out: M.confirm_popup(out, c)))(cur)
            else:
                prev, cur, since, msg = cur, ev, f, None
                tgt = B.next_cam(cur, cam_to)
                if tgt != cam_to:
                    cam_from, cam_to, cam_since = cam, tgt, f
        if f - cam_since <= B.CAM_EASE:
            k = ease_out(f - cam_since, B.CAM_EASE)
            cam = B.clamp_cam(cam_from[0] + (cam_to[0] - cam_from[0]) * k,
                              cam_from[1] + (cam_to[1] - cam_from[1]) * k)
        else:
            cam = cam_to
        if f % 2:
            frames.append(None)
            continue
        kw = dict(drift=f // 4, message=msg, popup=popup, bob=1 if (f // 16) % 2 else 0)
        if prev and f - since < B.RING_TRAVEL:
            (ax, ay), (bx, by) = B.STATIONS[prev][:2], B.STATIONS[cur][:2]
            k = ease_out(f - since + 1, B.RING_TRAVEL)
            kw["ring_at"] = (ax + (bx - ax) * k, ay + (by - ay) * k)
        if deny_since is not None and 0 <= f - deny_since < 36:
            t = f - deny_since
            if t < len(SHAKE):
                kw["ring_dx"] = SHAKE[t]
            if (t // 4) % 2 == 0:
                kw["deny"] = deny_tgt
        frames.append(B.render(cur, cam, **kw))
    return frames


if __name__ == "__main__":
    ensure_out()
    S = stills()
    for name, _, _, im, _ in S:
        save_still(im, name)
    B.overview([("1 open: MARIS BAY", S[0][4]), ("2 TELOK TOWN", S[1][4]), ("3 KORU CITY", S[2][4])],
               os.path.join(OUT, "big_overview_2x.png"))
    b = B.budget()
    print("BG2 unique tiles (tubes + baked labels, flip-deduped): %d; label cells %d; tilemap %d bytes; "
          "label/tube cell conflicts: %s" % (b["tiles"], b["label_cells"], b["map_bytes"], b["conflicts"] or "none"))
    fr = nav_frames()
    n = save_gif(fr, os.path.join(OUT, "big_nav_3x.gif"), scale=3, step=2)   # odd frames are None
    print("big_nav_3x.gif: %d GBA frames -> %d GIF frames" % (len(fr), n))
