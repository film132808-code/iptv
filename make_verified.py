#!/usr/bin/env python3
"""Build verified-only playlists from the check results."""
import json, re
from collections import defaultdict

live = {u: v[0] for u, v in json.load(open("live_status.json")).items()}
EXTINF = re.compile(r'group-title="([^"]*)"')


def parse(path):
    out, pending = [], None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            s = line.strip()
            if s.startswith("#EXTINF"):
                pending = s
            elif s and not s.startswith("#") and pending:
                out.append((pending, s))
                pending = None
    return out


def write(path, entries, title, extra=()):
    counts = defaultdict(int)
    for extinf, _ in entries:
        m = EXTINF.search(extinf)
        counts[m.group(1) if m else "Other"] += 1
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("#EXTM3U\n")
        f.write(f"# {title} - {len(entries)} live channels - generated 2026-11-20\n")
        for e in extra:
            f.write(f"# {e}\n")
        cur = None
        for extinf, url in entries:
            m = EXTINF.search(extinf)
            g = m.group(1) if m else "Other"
            if g != cur:
                cur = g
                f.write(f"\n# ============ {cur} ({counts[cur]}) ============\n")
            f.write(extinf + "\n" + url + "\n")
    print(f"{path}: {len(entries)} channels")


allents = parse("IPTV_World_by_Country.m3u")
alive = [(e, u) for e, u in allents if live.get(u)]
write("IPTV_World_VERIFIED.m3u", alive,
      "World IPTV - ONLY channels confirmed responding at build time",
      ["Still, some streams are geo-blocked / temporary - retry later if one fails"])

reg = parse("IPTV_World_by_Region.m3u")
write("IPTV_World_by_Region_VERIFIED.m3u", [(e, u) for e, u in reg if live.get(u)],
      "World IPTV by region - verified live channels only")

sa = parse("IPTV_South_Asia.m3u")
write("IPTV_South_Asia_VERIFIED.m3u", [(e, u) for e, u in sa if live.get(u)],
      "South Asia IPTV - verified live channels only")
