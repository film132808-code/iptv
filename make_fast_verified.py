#!/usr/bin/env python3
import json, re
from collections import Counter
live = {u: v[0] for u, v in json.load(open("live_fast.json")).items()}
lines = [l.strip() for l in open("IPTV_FAST_Services.m3u", encoding="utf-8")]
ent, pend = [], None
for l in lines:
    if l.startswith("#EXTINF"): pend = l
    elif l and not l.startswith("#") and pend: ent.append((pend, l)); pend = None
keep = [(e, u) for e, u in ent if live.get(u)]
cnt = Counter(re.search(r'group-title="([^"]*)"', e).group(1) for e, u in keep)
with open("IPTV_FAST_Services_VERIFIED.m3u", "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n# Free ad-supported (FAST) platforms - only channels verified live\n")
    f.write("# Samsung TV Plus / Plex / Pluto TV / Roku Channel / Tubi\n")
    f.write(f"# TOTAL CHANNELS: {len(keep)}\n")
    cur = None
    for gi in sorted(cnt, key=lambda k: (-cnt[k], k)):
        f.write(f"\n# ====== {gi} ({cnt[gi]}) ======\n")
        for e, u in keep:
            if re.search(r'group-title="([^"]*)"', e).group(1) == gi:
                f.write(e + "\n" + u + "\n")
print("IPTV_FAST_Services_VERIFIED.m3u:", len(keep))
