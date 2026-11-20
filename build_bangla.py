#!/usr/bin/env python3
"""Build a Bengali + Bollywood playlist using ONLY licensed free sources."""
import re, json, os
from collections import defaultdict

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')

# licensed FAST platforms: Samsung TV Plus India / Pluto / Roku / Tubi
FAST_PICK = {
    "News18 Bangla": ("📰 News", "🇮🇳"),
    "TV9 Bangla": ("📰 News", "🇮🇳"),
    "R Bangla": ("🎭 Entertainment", "🇮🇳"),
    "Sangeet Bangla": ("🎵 Music", "🇮🇳"),
    "B4U Movies": ("🎬 Movies", "🇮🇳"),
    "B4U Kadak": ("🎬 Movies", "🇮🇳"),
    "B4U Music": ("🎵 Music", "🇮🇳"),
    "Bollywood Masala": ("🎬 Movies", "🇮🇳"),
    "Sangeet Bhojpuri": ("🎵 Music", "🇮🇳"),
    "Star Central": ("🎭 Entertainment", "🇮🇳"),
}

# free Bengali channels already in our verified master
BENGALI_LOCAL = re.compile(
    r"(bangla vision|ntv|channel i|boishakhi|rtv|maasranga|deepto|ekushey|"
    r"ananda tv|aamar bangla|deshi tv|nexus tv|rajdhani|channel s|matribhumi|"
    r"azan tv|madani channel bangla|probashi|news 21 bangla|nan tv|movie bangla|"
    r"my tv|somoy|jamuna|ekattor|atn news|atn bangla|dbc news|independent|"
    r"channel 24|nagorik|shamol bangla|t sports)", re.I)


def parse(path):
    out, pending = [], None
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip().lstrip("\ufeff")
            if s.startswith("#EXTINF"):
                pending = s
            elif s and not s.startswith("#") and pending:
                out.append((pending, s))
                pending = None
    return out


rows = []

# 1) licensed FAST channels
for e, u in parse("IPTV_FAST_Services_VERIFIED.m3u"):
    name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
    if name in FAST_PICK:
        cat, flag = FAST_PICK[name]
        d = dict(ATTR.findall(e))
        rows.append({"name": name, "url": u, "logo": d.get("tvg-logo", ""),
                     "tvg_id": d.get("tvg-id", ""), "group": f"{flag} Bangla & Bollywood · {cat}",
                     "src": "Samsung TV Plus"})

# 2) Bengali channels from the curated master
seen = set()
for e, u in parse("IPTV_POPULAR.m3u"):
    name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
    d = dict(ATTR.findall(e))
    grp = d.get("group-title", "")
    if u in seen or "Bangladesh" not in grp:
        continue
    seen.add(u)
    cat = grp.split("· ")[-1] if "· " in grp else "📦 Other"
    rows.append({"name": name, "url": u, "logo": d.get("tvg-logo", ""),
                 "tvg_id": d.get("tvg-id", ""), "group": f"🇧🇩 Bangla & Bollywood · {cat}",
                 "src": "free-to-air"})

rows.sort(key=lambda r: (r["group"], r["name"].lower()))
with open("IPTV_Bangla_Bollywood.m3u", "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n")
    f.write("# Bangla + Bollywood channels from LICENSED free sources only\n")
    f.write("# - Samsung TV Plus India (licensed FAST platform)\n")
    f.write("# - free-to-air Bangladeshi channels\n")
    f.write("# Premium channels (Star Jalsha / Zee Bangla / Sony / HBO) are NOT here:\n")
    f.write("#   in Bangladesh they are legally available on Toffee (toffeelive.com)\n")
    f.write(f"# TOTAL CHANNELS: {len(rows)}\n")
    cur = None
    for r in rows:
        if r["group"] != cur:
            cur = r["group"]
            n = sum(1 for x in rows if x["group"] == cur)
            f.write(f"\n# ====== {cur} ({n}) ======\n")
        f.write(f'#EXTINF:-1 tvg-id="{r["tvg_id"]}" tvg-name="{r["name"]}" '
                f'tvg-logo="{r["logo"]}" group-title="{cur}",{r["name"]}\n{r["url"]}\n')
print("IPTV_Bangla_Bollywood.m3u:", len(rows))
for g in sorted(set(r["group"] for r in rows)):
    print("  ", g, sum(1 for r in rows if r["group"] == g))
