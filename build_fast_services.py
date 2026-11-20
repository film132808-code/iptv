#!/usr/bin/env python3
"""Merge FAST platform playlists (Samsung, Plex, Pluto, Roku, Tubi) into one file."""
import re, os, glob
from collections import defaultdict

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')

SERVICES = [
    ("samsungtvplus_all.m3u", "Samsung TV Plus", "🟦"),
    ("plex_all.m3u", "Plex Live TV", "🟨"),
    ("plutotv_all.m3u", "Pluto TV", "🟪"),
    ("roku_all.m3u", "The Roku Channel", "🟥"),
    ("tubi_all.m3u", "Tubi", "🟧"),
]

REGION = {"us": "United States", "gb": "United Kingdom", "ca": "Canada",
          "in": "India", "de": "Germany", "fr": "France", "it": "Italy",
          "es": "Spain", "at": "Austria", "ch": "Switzerland", "kr": "Korea",
          "au": "Australia", "nz": "New Zealand", "mx": "Mexico",
          "ar": "Argentina", "br": "Brazil", "cl": "Chile", "dk": "Denmark",
          "no": "Norway", "se": "Sweden"}


def parse(path):
    out, pending = [], None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip().lstrip("\ufeff")
            if s.startswith("#EXTINF"):
                pending = s
            elif s and not s.startswith("#") and pending:
                out.append((pending, s))
                pending = None
    return out


# Reference set = sources that do NOT already contain FAST output.
# (Never dedupe against IPTV_MASTER.m3u - it already includes this playlist,
#  which would silently shrink the FAST list on every rebuild.)
existing = set()
for fn in ("IPTV_World_by_Country.m3u", "IPTV_Other_Sources.m3u",
           "IPTV_Index_Extra.m3u", "IPTV_PlutoTV.m3u"):
    if os.path.exists(fn):
        for _, u in parse(fn):
            existing.add(u)
print("already have:", len(existing))

rows, seen = [], set()
stats = defaultdict(int)
for fn, nice, icon in SERVICES:
    path = os.path.join("src/fast", fn)
    if not os.path.exists(path):
        continue
    got = 0
    for e, u in parse(path):
        if u in existing or u in seen:
            continue
        seen.add(u)
        d = dict(ATTR.findall(e))
        name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
        # region: channel-id like "GB800002OP-gb", or group-title, or tvg-id
        region = ""
        cid = d.get("channel-id", "")
        if "-" in cid:
            tail = cid.rsplit("-", 1)[-1].lower()
            if tail in REGION:
                region = REGION[tail]
        if not region:
            gt = d.get("group-title", "")
            if gt in REGION.values():
                region = gt
        if not region:
            tid = d.get("tvg-id", "")
            pre = tid[:2].upper() if len(tid) > 2 else ""
            reg2 = {"US": "United States", "GB": "United Kingdom", "CA": "Canada",
                    "IN": "India", "DE": "Germany", "FR": "France", "IT": "Italy",
                    "ES": "Spain", "KR": "Korea", "AT": "Austria", "CH": "Switzerland"}
            region = reg2.get(pre, "International")
        grp = f"{icon} {nice} · {region}"
        rows.append({"group": grp, "name": name, "url": u, "extinf": e,
                     "cat": d.get("group-title", "")})
        got += 1
    stats[nice] = got
    print(f"  {nice}: {got} new")

print("total new:", len(rows))

with open("IPTV_FAST_Services.m3u", "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n")
    f.write("# Free ad-supported (FAST) platforms - official free channels\n")
    f.write("# Samsung TV Plus / Plex Live TV / Pluto TV / Roku Channel / Tubi\n")
    f.write("# All are free, ad-supported services - no subscription involved\n")
    f.write(f"# TOTAL CHANNELS: {len(rows)}\n")
    by = defaultdict(list)
    for r in rows:
        by[r["group"]].append(r)
    for g in sorted(by, key=lambda k: (-len(by[k]), k)):
        ents = sorted(by[g], key=lambda r: r["name"].lower())
        f.write(f"\n# ====== {g} ({len(ents)}) ======\n")
        for r in ents:
            e = re.sub(r'group-title="[^"]*"', f'group-title="{g}"', r["extinf"])
            if 'group-title' not in e:
                e = e.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{g}"', 1)
            f.write(e + "\n" + r["url"] + "\n")
print("IPTV_FAST_Services.m3u written")

import json
json.dump(stats, open("fast_stats.json", "w"), indent=2)
