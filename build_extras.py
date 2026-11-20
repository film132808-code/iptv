#!/usr/bin/env python3
"""Merge extra legal sources (Free-TV repo + official YouTube live) into playlists."""
import json, re, os
from collections import defaultdict, OrderedDict
from common import COUNTRY_NAMES, flag_of

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')



def parse(path, with_attrs=False):
    out, pending = [], None
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip().lstrip("\ufeff")
            if s.startswith("#EXTINF"):
                pending = s
            elif s and not s.startswith("#") and pending:
                attrs = dict(ATTR.findall(pending))
                name = pending.split('",')[-1] if '",' in pending else pending.rsplit(",", 1)[-1]
                name = name.strip(" \"")
                out.append({"attrs": attrs, "name": name, "url": s})
                pending = None
    return out


# ---------------------------------------------------------------- Free-TV ---
existing = set()
for fn in ("IPTV_World_by_Country.m3u", "IPTV_South_Asia.m3u"):
    for e in parse(fn):
        existing.add(e["url"])

ftv = parse("src/freetv.m3u")
seen = set()
extra = []
skipped_bad = 0
for e in ftv:
    u = e["url"]
    if u in existing or u in seen:
        continue
    if "twitch.tv" in u:            # not playable in IPTV players
        skipped_bad += 1
        continue
    if not u.lower().startswith(("http://", "https://")):
        skipped_bad += 1
        continue
    seen.add(u)
    a = e["attrs"]
    cc = (a.get("tvg-country") or "").upper()
    if not cc:
        tid = a.get("tvg-id", "")
        cc = tid.split(".")[-1].upper() if "." in tid else ""
    cname = COUNTRY_NAMES.get(cc, "Other / International")
    extra.append({
        "name": e["name"], "url": u, "logo": a.get("tvg-logo", ""),
        "tvg_id": a.get("tvg-id", ""), "cc": cc or "XX",
        "group": f"{flag_of(cc)} {cname}" if cc else "🌐 Other / International",
        "cat": a.get("group-title", ""),
    })

# ---------------------------------------------------------------- YouTube ---
yt = []
if os.path.exists("yt_status.json"):
    for r in json.load(open("yt_status.json")):
        cc = r["cc"]
        cname = COUNTRY_NAMES.get(cc, cc)
        yt.append({
            "name": r["name"], "url": r["url"], "tvg_id": f"yt-{r['cid']}",
            "logo": r.get("thumb", ""), "live": r["live"], "cat": r["cat"],
            "group": f"▶ {flag_of(cc)} YouTube Live · {cname}" if flag_of(cc)
                     else "▶ YouTube Live",
        })


def write(path, header, sections):
    """sections: list of (group_label, [entries])"""
    total = sum(len(v) for _, v in sections)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("#EXTM3U\n")
        for h in header:
            f.write(f"# {h}\n")
        f.write(f"# TOTAL CHANNELS: {total}\n")
        for g, ents in sections:
            if not ents:
                continue
            f.write(f"\n# ============ {g} ({len(ents)}) ============\n")
            for e in ents:
                f.write(f'#EXTINF:-1 tvg-id="{e["tvg_id"]}" '
                        f'tvg-name="{e["name"]}" tvg-logo="{e["logo"]}" '
                        f'group-title="{g}",{e["name"]}\n{e["url"]}\n')
    print(f"{path}: {total} channels")
    return total


# 1) other sources
by_group = defaultdict(list)
for e in extra:
    by_group[e["group"]].append(e)
secs = sorted(by_group.items(), key=lambda kv: (-len(kv[1]), kv[0]))
write("IPTV_Other_Sources.m3u",
      ["Extra legal free channels from the Free-TV open-source project",
       "(free-to-air streams published by broadcasters themselves)",
       "Run refresh_extras.sh to update"],
      secs)

# 2) youtube
ybygroup = defaultdict(list)
for e in yt:
    ybygroup[e["group"]].append(e)
ysечs = sorted(ybygroup.items(), key=lambda kv: (-len(kv[1]), kv[0]))
write("IPTV_YouTube_Live.m3u",
      ["Official YouTube live channels (broadcaster-owned, free)",
       "URL format: youtube.com/channel/<id>/live  - always points to the current live stream",
       "Needs a player with YouTube support (OTT Navigator / Kodi+YouTube plugin) or just open the link",
       "Run check_youtube.py to re-verify which channels are live"],
      ysечs)

print(f"free-tv new: {len(extra)}, skipped: {skipped_bad}, youtube: {len(yt)}")
