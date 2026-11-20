#!/usr/bin/env python3
"""Merge iptv-org country playlists into clean, grouped M3U files."""
import os, re, glob, json
from collections import OrderedDict, defaultdict

SRC = "src"

COUNTRIES = {
    "bd": ("Bangladesh", "🇧🇩", "Asia"),
    "in": ("India", "🇮🇳", "Asia"),
    "pk": ("Pakistan", "🇵🇰", "Asia"),
    "us": ("United States", "🇺🇸", "North America"),
    "uk": ("United Kingdom", "🇬🇧", "Europe"),
    "ca": ("Canada", "🇨🇦", "North America"),
    "au": ("Australia", "🇦🇺", "Oceania"),
    "nz": ("New Zealand", "🇳🇿", "Oceania"),
    "ae": ("UAE", "🇦🇪", "Middle East"),
    "sa": ("Saudi Arabia", "🇸🇦", "Middle East"),
    "qa": ("Qatar", "🇶🇦", "Middle East"),
    "kw": ("Kuwait", "🇰🇼", "Middle East"),
    "om": ("Oman", "🇴🇲", "Middle East"),
    "bh": ("Bahrain", "🇧🇭", "Middle East"),
    "ir": ("Iran", "🇮🇷", "Middle East"),
    "iq": ("Iraq", "🇮🇶", "Middle East"),
    "tr": ("Turkey", "🇹🇷", "Middle East"),
    "af": ("Afghanistan", "🇦🇫", "Asia"),
    "my": ("Malaysia", "🇲🇾", "Asia"),
    "sg": ("Singapore", "🇸🇬", "Asia"),
    "id": ("Indonesia", "🇮🇩", "Asia"),
    "ph": ("Philippines", "🇵🇭", "Asia"),
    "th": ("Thailand", "🇹🇭", "Asia"),
    "vn": ("Vietnam", "🇻🇳", "Asia"),
    "np": ("Nepal", "🇳🇵", "Asia"),
    "lk": ("Sri Lanka", "🇱🇰", "Asia"),
    "mv": ("Maldives", "🇲🇻", "Asia"),
    "mm": ("Myanmar", "🇲🇲", "Asia"),
    "kh": ("Cambodia", "🇰🇭", "Asia"),
    "cn": ("China", "🇨🇳", "Asia"),
    "jp": ("Japan", "🇯🇵", "Asia"),
    "kr": ("South Korea", "🇰🇷", "Asia"),
    "hk": ("Hong Kong", "🇭🇰", "Asia"),
    "tw": ("Taiwan", "🇹🇼", "Asia"),
    "de": ("Germany", "🇩🇪", "Europe"),
    "fr": ("France", "🇫🇷", "Europe"),
    "it": ("Italy", "🇮🇹", "Europe"),
    "es": ("Spain", "🇪🇸", "Europe"),
    "pt": ("Portugal", "🇵🇹", "Europe"),
    "nl": ("Netherlands", "🇳🇱", "Europe"),
    "be": ("Belgium", "🇧🇪", "Europe"),
    "ch": ("Switzerland", "🇨🇭", "Europe"),
    "at": ("Austria", "🇦🇹", "Europe"),
    "ie": ("Ireland", "🇮🇪", "Europe"),
    "se": ("Sweden", "🇸🇪", "Europe"),
    "no": ("Norway", "🇳🇴", "Europe"),
    "dk": ("Denmark", "🇩🇰", "Europe"),
    "fi": ("Finland", "🇫🇮", "Europe"),
    "is": ("Iceland", "🇮🇸", "Europe"),
    "pl": ("Poland", "🇵🇱", "Europe"),
    "cz": ("Czechia", "🇨🇿", "Europe"),
    "sk": ("Slovakia", "🇸🇰", "Europe"),
    "hu": ("Hungary", "🇭🇺", "Europe"),
    "ro": ("Romania", "🇷🇴", "Europe"),
    "bg": ("Bulgaria", "🇧🇬", "Europe"),
    "gr": ("Greece", "🇬🇷", "Europe"),
    "hr": ("Croatia", "🇭🇷", "Europe"),
    "si": ("Slovenia", "🇸🇮", "Europe"),
    "rs": ("Serbia", "🇷🇸", "Europe"),
    "ba": ("Bosnia", "🇧🇦", "Europe"),
    "al": ("Albania", "🇦🇱", "Europe"),
    "lt": ("Lithuania", "🇱🇹", "Europe"),
    "lv": ("Latvia", "🇱🇻", "Europe"),
    "ru": ("Russia", "🇷🇺", "Europe"),
    "ua": ("Ukraine", "🇺🇦", "Europe"),
    "br": ("Brazil", "🇧🇷", "South America"),
    "ar": ("Argentina", "🇦🇷", "South America"),
    "mx": ("Mexico", "🇲🇽", "North America"),
    "cl": ("Chile", "🇨🇱", "South America"),
    "co": ("Colombia", "🇨🇴", "South America"),
    "pe": ("Peru", "🇵🇪", "South America"),
    "za": ("South Africa", "🇿🇦", "Africa"),
    "ng": ("Nigeria", "🇳🇬", "Africa"),
    "ke": ("Kenya", "🇰🇪", "Africa"),
    "eg": ("Egypt", "🇪🇬", "Africa"),
    "ma": ("Morocco", "🇲🇦", "Africa"),
}

# Priority order for the main playlist: user's requested countries first.
PRIORITY = ["bd", "in", "pk", "us", "uk", "ca"]
REGION_ORDER = ["Asia", "Middle East", "Europe", "North America", "South America", "Africa", "Oceania"]

EXTINF_RE = re.compile(r'^#EXTINF:\s*(-?\d+)(.*)$', re.I)
ATTR_RE = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')


def parse_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = [l.strip().lstrip("\ufeff") for l in f]
    out, pending = [], None
    for line in lines:
        if not line:
            continue
        if line.startswith("#EXTINF"):
            pending = line
        elif line.startswith("#"):
            continue
        elif pending:
            out.append((pending, line))
            pending = None
    return out


def split_extinf(extinf):
    m = EXTINF_RE.match(extinf)
    if not m:
        return {}, "Unknown"
    dur = m.group(1)
    rest = m.group(2)
    attrs = dict(ATTR_RE.findall(rest))
    name = rest.split('",')[-1] if '",' in rest else rest.rsplit(",", 1)[-1]
    name = name.strip(' "')
    attrs.pop("group-title", None)
    return attrs, name


def build():
    channels = []          # list of dicts
    seen_urls = set()
    seen_name = defaultdict(set)
    stats = {}

    for cc, (cname, flag, region) in COUNTRIES.items():
        path = os.path.join(SRC, f"{cc}.m3u")
        if not os.path.exists(path):
            continue
        entries = parse_file(path)
        kept = 0
        for extinf, url in entries:
            attrs, name = split_extinf(extinf)
            url = url.strip()
            if not url.lower().startswith(("http://", "https://")):
                continue
            if url in seen_urls:
                continue
            key = name.lower()
            # same channel name more than twice in one country -> skip dupes
            if key in seen_name[cc] and len(seen_name[cc]) > 0:
                pass
            seen_urls.add(url)
            seen_name[cc].add(key)
            channels.append({
                "name": name,
                "url": url,
                "logo": attrs.get("tvg-logo", ""),
                "tvg_id": attrs.get("tvg-id", ""),
                "tvg_name": attrs.get("tvg-name", ""),
                "country": cname,
                "code": cc,
                "flag": flag,
                "region": region,
            })
            kept += 1
        stats[cname] = kept

    # ---- extra: Bengali-language channels not already covered -----------
    ben = os.path.join(SRC, "lang_ben.m3u")
    if os.path.exists(ben):
        extra = 0
        for extinf, url in parse_file(ben):
            url = url.strip()
            if url in seen_urls or not url.lower().startswith(("http://", "https://")):
                continue
            attrs, name = split_extinf(extinf)
            tid = attrs.get("tvg-id", "")
            cc = "bd" if ".bd@" in tid or "bd@" in tid else ("in" if ".in@" in tid else "bd")
            cname, flag, region = COUNTRIES[cc]
            if cc != "bd":
                cname, flag = "Bangla Channels (Bengali)", "🇧🇩"
            seen_urls.add(url)
            channels.append({
                "name": name, "url": url,
                "logo": attrs.get("tvg-logo", ""), "tvg_id": tid,
                "tvg_name": attrs.get("tvg-name", ""),
                "country": cname, "code": cc, "flag": flag, "region": "Asia",
            })
            extra += 1
        stats["Bangla extra"] = extra

    # ---- ordering -------------------------------------------------------
    def sort_key(ch):
        if ch["code"] in PRIORITY:
            return (0, PRIORITY.index(ch["code"]), ch["name"].lower())
        return (1 + REGION_ORDER.index(ch["region"]), COUNTRIES[ch["code"]][0].lower(),
                ch["name"].lower())

    channels.sort(key=sort_key)
    return channels, stats


def esc(s):
    return s.replace('"', "'")


def write_m3u(path, header_extra, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("#EXTM3U\n")
        for line in header_extra:
            f.write(f"# {line}\n")
        cur = None
        for r in rows:
            if r["group"] != cur:
                cur = r["group"]
                f.write(f"\n# ==================== {cur} ({r['count']} channels) ====================\n")
            f.write(f'#EXTINF:-1 tvg-id="{esc(r["tvg_id"])}" '
                    f'tvg-name="{esc(r["tvg_name"] or r["name"])}" '
                    f'tvg-logo="{esc(r["logo"])}" group-title="{esc(cur)}",{r["name"]}\n')
            f.write(r["url"] + "\n")


def main():
    channels, stats = build()

    # --- playlist 1: grouped by COUNTRY (main deliverable) ---------------
    by_country = []
    prev = None
    counts = defaultdict(int)
    for ch in channels:
        label = f'{ch["flag"]} {ch["country"]}'.strip()
        counts[label] += 1
    for ch in channels:
        label = f'{ch["flag"]} {ch["country"]}'.strip()
        by_country.append({**ch, "group": label, "count": counts[label]})

    write_m3u("IPTV_World_by_Country.m3u",
              ["World IPTV playlist - grouped by country",
               f"Total channels: {len(channels)}",
               "Source: iptv-org open-source public channel database (github.com/iptv-org/iptv)",
               "Generated: 2026-11-20"],
              by_country)

    # --- playlist 2: grouped by REGION ----------------------------------
    reg_counts = defaultdict(int)
    for ch in channels:
        reg_counts[ch["region"]] += 1
    by_region = [{**ch, "group": ch["region"], "count": reg_counts[ch["region"]]} for ch in channels]
    by_region.sort(key=lambda r: (REGION_ORDER.index(r["region"]),
                                  COUNTRIES[r["code"]][0], r["name"].lower()))
    write_m3u("IPTV_World_by_Region.m3u",
              ["World IPTV playlist - grouped by region", f"Total channels: {len(channels)}"],
              by_region)

    # --- playlist 3: South Asia focus (BD / IN / PK / NP / LK / AF / MV / BT)
    south = [ch for ch in channels if ch["code"] in
             ("bd", "in", "pk", "np", "lk", "af", "mv", "mm", "bh")]
    scounts = defaultdict(int)
    for ch in south:
        scounts[f'{ch["flag"]} {ch["country"]}'] += 1
    south_rows = [{**ch, "group": f'{ch["flag"]} {ch["country"]}', "count": scounts[f'{ch["flag"]} {ch["country"]}']}
                  for ch in south]
    write_m3u("IPTV_South_Asia.m3u",
              ["South Asia + neighbourhood IPTV playlist", f"Total channels: {len(south)}"],
              south_rows)

    with open("stats.json", "w") as f:
        json.dump({"total": len(channels), "by_country": stats}, json.dumps and f, indent=2)

    print(f"TOTAL channels: {len(channels)}")
    top = sorted(stats.items(), key=lambda x: -x[1])[:15]
    for k, v in top:
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
