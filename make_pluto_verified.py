#!/usr/bin/env python3
import json, re
from collections import Counter
live = {u: v[0] for u, v in json.load(open("live_pluto.json")).items()}
lines = [l.strip() for l in open("IPTV_PlutoTV.m3u", encoding="utf-8")]
ent, pend = [], None
for l in lines:
    if l.startswith("#EXTINF"): pend = l
    elif l and not l.startswith("#") and pend: ent.append((pend, l)); pend = None
keep = [(e, u) for e, u in ent if live.get(u)]
cnt = Counter(re.search(r'group-title="([^"]*)"', e).group(1) for e, u in keep)
with open("IPTV_PlutoTV_VERIFIED.m3u", "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n# Pluto TV - official free live channels, verified working\n")
    f.write("# JWT expires ~24h - run: bash refresh_pluto.sh\n# TOTAL: %d\n" % len(keep))
    cur = None
    for e, u in keep:
        g = re.search(r'group-title="([^"]*)"', e).group(1)
        if g != cur:
            cur = g; f.write(f"\n# ====== {g} ({cnt[g]}) ======\n")
        f.write(e + "\n" + u + "\n")
print("IPTV_PlutoTV_VERIFIED.m3u:", len(keep))
