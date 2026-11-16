"""
Stills of the TOSA RAIL station map (1x + 3x into out/).

  map_a_default        cursor on the nearest accessible station (MARIS BAY)
  map_b_telok          cursor moved to TELOK TOWN
  map_c_confirm        "Take the train to TELOK TOWN?" + Orchid YES/NO with gold pill
  map_d_denied         player pushed toward greyed KORU CITY: ring shakes, grey flash ring, message
  map_alt_list         alternative layout: station list left + mini map right
  map_ab               A vs B side by side (3x)

usage: python mock_station_map.py
"""
from common import *
import station_map as M


def stills():
    S = []
    S.append(("map_a_default", "A. Default — cursor on the nearest station",
              "Opened from the attendant at TOSA PORT. The cursor starts on the nearest station "
              "you can travel to (MARIS BAY): gold ring on the node, gold pill on the name. "
              "The head marks where you are. KORU CITY and ASHEN PASS are greyed, and so is "
              "the track to them.",
              M.render(cursor="MARIS BAY")))
    S.append(("map_b_telok", "B. Cursor on another station",
              "D-pad moves to the nearest visited station in that direction (greyed ones are "
              "skipped). TELOK TOWN is on the RIDGE line (purple); the tray shows the line name.",
              M.render(cursor="TELOK TOWN", scroll=6)))
    S.append(("map_c_confirm", "C. Confirm",
              "A opens the standard Orchid dialogue box and YES/NO window. The gold pill marks "
              "YES; there is no arrow. The ring stays on TELOK TOWN behind the window.",
              M.render(cursor="TELOK TOWN", scroll=6,
                       popup=lambda out: M.confirm_popup(out, "TELOK TOWN"))))
    S.append(("map_d_denied", "D. Trying a greyed station",
              "Cursor on VALE JUNCTION, player presses RIGHT toward KORU CITY. The cursor stays: "
              "gold ring shakes (+/-2px, 3 swings), KORU's node flashes a grey ring, the failure "
              "buzzer plays, and the tray says why. The message clears on the next input.",
              M.render(cursor="VALE JUNCTION", ring_dx=2, deny="KORU CITY", scroll=10,
                       tray_msg="You haven't been to KORU CITY yet.\nVisit it on foot first.")))
    S.append(("map_alt_list", "Alternative: list + mini map",
              "Gen 5 pill list of every station (line-coloured cap, greyed rows for unvisited "
              "stations, head on your current stop) with a small line diagram in a well on the "
              "right. Up/Down walks the list in line order.",
              M.render_list(cursor="MARIS BAY")))
    return S


def ab_sheet(a, b, path):
    from PIL import ImageDraw
    k = 3
    sheet = Image.new("RGB", (240 * k * 2 + 72, 160 * k + 60), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    d.text((24, 14), "A - line diagram (recommended)", fill=(230, 230, 240))
    d.text((240 * k + 48, 14), "B - station list + mini map", fill=(230, 230, 240))
    sheet.paste(KX.upscale(a.convert("RGB"), k), (24, 40))
    sheet.paste(KX.upscale(b.convert("RGB"), k), (240 * k + 48, 40))
    sheet.save(path)


def budget():
    im = M.bg2_art_index_image()
    tiles, tm = to_tiles(im)
    return [
        "Station map BG2 art (lines + header + tray, flip-deduped): %d unique 4bpp tiles "
        "(incl. blank) = %d bytes" % (len(tiles), len(tiles) * 32),
        "BG palettes: 0 orchid (ridge line, header, tray), 1 sea (coast line), 2 grey "
        "(unvisited track), 3 grid; 13-15 text/frames as usual",
        "OBJ: 6 nodes + 1 ring + 1 grey ring + 1 head = 9 OAM (16x16 each); 2 OBJ palettes "
        "(kit orchid roles, region-map player icon)",
    ]


if __name__ == "__main__":
    ensure_out()
    S = stills()
    for name, _, _, im in S:
        save_still(im, name)
    ab_sheet(S[0][3], S[4][3], os.path.join(OUT, "map_ab_3x.png"))
    for l in budget():
        print(l)
    print("ok", len(S), "stills")
