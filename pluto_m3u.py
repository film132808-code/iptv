#!/usr/bin/env python3
"""Build an M3U playlist of Pluto TV's own free live channels (pluto.tv)."""
import json, uuid, urllib.request, urllib.parse, urllib.error, sys

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def boot():
    cid = str(uuid.uuid4())
    p = {"appName": "web", "appVersion": "5.0.0", "clientID": cid,
         "clientModelNumber": "1.0.0", "deviceId": cid, "deviceType": "web",
         "deviceModel": "web", "deviceVersion": "124.0.0",
         "deviceMake": "Chrome", "osName": "Windows",
         "osVersion": "10", "serverSideAds": "false",
         "notificationVersion": "1", "appLaunchCount": "1",
         "drmCapabilities": "playready"}
    url = "https://boot.pluto.tv/v4/start?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Origin": "https://pluto.tv",
        "Referer": "https://pluto.tv/"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def channels(region="us"):
    url = f"https://api.pluto.tv/v2/channels?region={region}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(req, timeout=60))


def build(region="us", out="IPTV_PlutoTV.m3u"):
    b = boot()
    token = b["sessionToken"]
    stitcher = b["servers"]["stitcher"].rstrip("/")
    sparams = b.get("stitcherParams", "").lstrip("?")
    chans = channels(region)
    rows = []
    for ch in chans:
        cid, name = ch.get("_id"), ch.get("name")
        if not cid or not name:
            continue
        logo = ""
        for k in ("colorLogoPNG", "solidColorLogoPNG", "logo"):
            if isinstance(ch.get(k), dict):
                logo = ch[k].get("path", "")
                if logo:
                    break
        cat = (ch.get("category") or ch.get("hash") or "Pluto TV").lstrip("#")
        num = ch.get("number", 9999)
        url = (f"{stitcher}/v2/stitch/hls/channel/{cid}/master.m3u8"
               f"?jwt={token}&masterJWTPassthrough=true&{sparams}")
        rows.append((cat, name, num, logo, f"pluto-{cid}", url, ch.get("summary", "")))

    rows.sort(key=lambda r: (r[0].lower(), r[2]))
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("#EXTM3U\n")
        f.write("# Pluto TV - official free live channels (pluto.tv)\n")
        f.write("# JWT token inside the URLs expires - re-run pluto_m3u.py to refresh\n")
        f.write(f"# Region: {region.upper()} | TOTAL CHANNELS: {len(rows)}\n")
        cur = None
        for cat, name, num, logo, tid, url, _ in rows:
            g = f"🔴 Pluto TV · {cat}"
            if g != cur:
                cur = g
                n = sum(1 for r in rows if f"🔴 Pluto TV · {r[0]}" == g)
                f.write(f"\n# ============ {g} ({n}) ============\n")
            f.write(f'#EXTINF:-1 tvg-id="{tid}" tvg-name="{name}" tvg-logo="{logo}" '
                    f'group-title="{g}",{name}\n{url}\n')
    print(f"{out}: {len(rows)} channels (region {region})")
    return rows


if __name__ == "__main__":
    region = sys.argv[1] if len(sys.argv) > 1 else "us"
    build(region)
