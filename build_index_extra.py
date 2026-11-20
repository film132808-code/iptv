#!/usr/bin/env python3
"""Extract channels from the full iptv-org index that our country files missed."""
import re, json, os
from collections import defaultdict

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')

from common import COUNTRY_NAMES, flag_of

SKIP_EXT = (".mpd",)


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
                a = dict(ATTR.findall(pending))
                name = pending.split('",')[-1] if '",' in pending else pending.rsplit(",", 1)[-1]
                out.append({"attrs": a, "name": name.strip(' "'), "url": s})
                pending = None
    return out


existing = set()
for fn in ("IPTV_World_by_Country.m3u", "IPTV_Other_Sources.m3u", "IPTV_PlutoTV.m3u"):
    for e in parse(fn):
        existing.add(e["url"])
print("already have:", len(existing), "urls")

full = parse("src/index_full.m3u")
print("full index:", len(full))

new, seen = [], set()
for e in full:
    u = e["url"]
    if u in existing or u in seen:
        continue
    if not u.lower().startswith(("http://", "https://")):
        continue
    seen.add(u)
    a = e["attrs"]
    tid = a.get("tvg-id", "")
    cc = ""
    base = tid.split("@")[0].strip()          # "123TV.ve@SD" -> "123TV.ve"
    if "." in base:
        cc = base.split(".")[-1].upper()
    QUALITY = {"SD", "HD", "FHD", "UHD", "4K", "LQ", "HQ"}
    if cc in QUALITY:
        cc = ""
    if not cc and "@" in tid:
        tail = tid.split("@")[-1].strip().upper()
        cc = "" if tail in QUALITY else tail
    if cc == "UK":
        cc = "GB"
    cname = COUNTRY_NAMES.get(cc, "Other / International")
    prov = ""
    for p in ("pluto", "samsung", "jmp2.uk/stvp", "roku", "jmp2.uk/rok", "xumo",
              "plex", "tubi", "distro", "stirr"):
        if p in u.lower():
            prov = p
            break
    new.append({
        "name": e["name"], "url": u,
        "logo": a.get("tvg-logo", ""), "tvg_id": tid,
        "cc": cc or "XX",
        "group": (f"{flag_of(cc)} {cname}" if cc else "🌐 Other / International"),
        "cat": a.get("group-title", ""),
        "prov": prov,
    })

print("new channels:", len(new))
print("by provider:", dict(sorted(defaultdict(int, {k: sum(1 for n in new if n['prov'] == k)
      for k in set(n['prov'] for n in new)}).items(), key=lambda x: -x[1])))


def write(path, header, sections):
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
            for e in sorted(ents, key=lambda x: x["name"].lower()):
                f.write(f'#EXTINF:-1 tvg-id="{e["tvg_id"]}" tvg-name="{e["name"]}" '
                        f'tvg-logo="{e["logo"]}" group-title="{g}",{e["name"]}\n{e["url"]}\n')
    print(f"{path}: {total}")


by = defaultdict(list)
for e in new:
    by[e["group"]].append(e)
write("IPTV_Index_Extra.m3u",
      ["Channels from the full iptv-org index that the country playlists missed",
       "Includes additional Pluto / Samsung TV Plus / Roku / Xumo / Plex / Tubi streams"],
      sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])))

# provider view
byp = defaultdict(list)
for e in new:
    if e["prov"]:
        nice = {"pluto": "Pluto TV", "jmp2.uk/stvp": "Samsung TV Plus",
                "samsung": "Samsung TV Plus", "roku": "The Roku Channel",
                "jmp2.uk/rok": "The Roku Channel", "xumo": "Xumo Play",
                "plex": "Plex Live TV", "tubi": "Tubi", "distro": "DistroTV",
                "stirr": "Stirr"}.get(e["prov"], e["prov"])
        byp[f"📡 {nice} · {COUNTRY_NAMES.get(e['cc'], 'World')}"].append(e)
write("IPTV_FAST_Extra.m3u",
      ["Extra free ad-supported (FAST) channels found in the iptv-org index",
       "Pluto TV / Samsung TV Plus / Roku Channel / Xumo / Plex / Tubi / DistroTV"],
      sorted(byp.items(), key=lambda kv: (-len(kv[1]), kv[0])))
