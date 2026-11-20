#!/usr/bin/env python3
"""Build verified extras + one big MASTER playlist."""
import json, re

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')


def parse(path):
    out, pending = [], None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s.startswith("#EXTINF"):
                pending = s
            elif s and not s.startswith("#") and pending:
                out.append((pending, s))
                pending = None
    return out


def group_of(extinf):
    m = ATTR.search(extinf)
    d = dict(ATTR.findall(extinf))
    return d.get("group-title", "Other")


def write(path, header, rows):
    """rows: list of (group, extinf, url)"""
    from collections import defaultdict
    counts = defaultdict(int)
    for g, _, _ in rows:
        counts[g] += 1
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("#EXTM3U\n")
        for h in header:
            f.write(f"# {h}\n")
        f.write(f"# TOTAL CHANNELS: {len(rows)}\n")
        cur = None
        for g, e, u in rows:
            if g != cur:
                cur = g
                f.write(f"\n# ============ {g} ({counts[g]}) ============\n")
            f.write(e + "\n" + u + "\n")
    print(f"{path}: {len(rows)} channels")
    return len(rows)


# ---------- 1. verified index-extra ----------
livei = {u: v[0] for u, v in json.load(open("live_index.json")).items()}
idx = parse("IPTV_Index_Extra.m3u")
idx_alive = [(group_of(e), e, u) for e, u in idx if livei.get(u)]
write("IPTV_Index_Extra_VERIFIED.m3u",
      ["Extra channels from the full iptv-org index - only ones responding at build time"],
      idx_alive)

# ---------- 1. verified extras ----------
livex = {u: v[0] for u, v in json.load(open("live_extra.json")).items()}
ext = parse("IPTV_Other_Sources.m3u")
ext_alive = [(group_of(e), e, u) for e, u in ext if livex.get(u)]
write("IPTV_Other_Sources_VERIFIED.m3u",
      ["Extra legal free channels - only ones responding at build time",
       "Source: Free-TV open-source project"], ext_alive)

# ---------- 2. master ----------
master = []
# world (iptv-org) verified
for e, u in parse("IPTV_World_VERIFIED.m3u"):
    master.append((group_of(e), e, u))
# FAST platforms verified (Samsung / Pluto / Roku / Tubi / Plex)
for e, u in parse("IPTV_FAST_Services_VERIFIED.m3u"):
    master.append((group_of(e), e, u))
# extras verified
for g, e, u in ext_alive:
    master.append((g, e, u))
# index-extra verified
for g, e, u in idx_alive:
    master.append((g, e, u))
# youtube (all, they toggle on/off)
yt_rows = []
for e, u in parse("IPTV_YouTube_Live.m3u"):
    yt_rows.append((group_of(e), e, u))

# put YouTube group first so it's easy to find at the top
order = sorted(master, key=lambda r: 0)
final = yt_rows + master
write("IPTV_MASTER.m3u",
      ["COMPLETE WORLD IPTV PLAYLIST",
       f"Sources: iptv-org + Free-TV + official YouTube live channels",
       "Sections starting with ▶ are YouTube links (need a YouTube-capable player)",
       "Generated: 2026-11-20"],
      final)

# ---------- 3. Bd/In/Pk/US/UK/CA quick file ----------
KEY = ("Bangladesh", "India", "Pakistan", "United States", "United Kingdom",
       "Canada", "YouTube Live · Bangladesh", "YouTube Live · India",
       "YouTube Live · Pakistan", "YouTube Live · United States",
       "YouTube Live · United Kingdom", "YouTube Live · Canada")
big6 = [(g, e, u) for (g, e, u) in final if any(k in g for k in KEY)]
write("IPTV_BIG6.m3u",
      ["Bangladesh + India + Pakistan + USA + UK + Canada only",
       "Everything else stripped out - smallest file, fastest to load"],
      big6)
