#!/usr/bin/env python3
"""Build a compact curated master: filters by country AND category, keeps the
most widely-carried / well-known channels, and prefers real HLS over YouTube."""
import re, os, glob, json
from collections import defaultdict, Counter

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')

COUNTRIES = [
    ("United States", "🇺🇸"), ("United Kingdom", "🇬🇧"), ("India", "🇮🇳"),
    ("Bangladesh", "🇧🇩"), ("Pakistan", "🇵🇰"), ("Canada", "🇨🇦"),
    ("Australia", "🇦🇺"), ("Germany", "🇩🇪"), ("France", "🇫🇷"),
    ("Italy", "🇮🇹"), ("Spain", "🇪🇸"), ("Turkey", "🇹🇷"), ("UAE", "🇦🇪"),
    ("Saudi Arabia", "🇸🇦"), ("Qatar", "🇶🇦"), ("Brazil", "🇧🇷"),
    ("Mexico", "🇲🇽"), ("Argentina", "🇦🇷"), ("Netherlands", "🇳🇱"),
    ("Switzerland", "🇨🇭"), ("Austria", "🇦🇹"), ("South Korea", "🇰🇷"),
    ("Japan", "🇯🇵"), ("Indonesia", "🇮🇩"), ("Malaysia", "🇲🇾"),
    ("Philippines", "🇵🇭"), ("Thailand", "🇹🇭"), ("Nepal", "🇳🇵"),
    ("Sri Lanka", "🇱🇰"), ("Iran", "🇮🇷"), ("Iraq", "🇮🇶"), ("Egypt", "🇪🇬"),
    ("Nigeria", "🇳🇬"), ("South Africa", "🇿🇦"), ("Kenya", "🇰🇪"),
    ("Russia", "🇷🇺"), ("Ukraine", "🇺🇦"), ("Poland", "🇵🇱"), ("Sweden", "🇸🇪"),
    ("Norway", "🇳🇴"), ("Denmark", "🇩🇰"), ("Finland", "🇫🇮"), ("Ireland", "🇮🇪"),
    ("Portugal", "🇵🇹"), ("Greece", "🇬🇷"), ("Romania", "🇷🇴"), ("Czechia", "🇨🇿"),
    ("Hungary", "🇭🇺"), ("New Zealand", "🇳🇿"), ("Israel", "🇮🇱"),
    ("China", "🇨🇳"), ("Taiwan", "🇹🇼"), ("Hong Kong", "🇭🇰"),
    ("Vietnam", "🇻🇳"), ("Afghanistan", "🇦🇫"), ("Myanmar", "🇲🇲"),
    ("Korea", "🇰🇷"),
]
FLAG = dict(COUNTRIES)

CAT_ICON = {"News": "📰", "Sports": "⚽", "Movies": "🎬",
            "Entertainment": "🎭", "Kids": "🧸", "Music": "🎵",
            "Documentary & Science": "🔬", "Religious": "🕌",
            "Lifestyle": "🍳", "Business": "💼", "Weather": "🌦", "Other": "📦"}

BRANDS = (r"bbc|cnn|sky news|al jazeera|france 24|deutsche welle|dw news|euronews|"
          r"nhk|trt world|cna |arirang|abc news|nbc news|cbs news|fox news|msnbc|"
          r"cnbc|bloomberg|pbs newshour|ndtv|aaj tak|india today|zee news|abp news|"
          r"republic|times now|wion|news18|india tv|dd news|dd india|firstpost|"
          r"cnbc-tv18|et now|somoy|jamuna|atn news|atn bangla|channel i|channel 24|"
          r"ntv|rtv news|ekattor|dbc news|news24|bangla vision|maasranga|nagorik|"
          r"gtv|global tv|deepto|t sports|shamol bangla|boishakhi|independent tel|"
          r"desh tv|ekushey|asian tv|my tv|bijoy|geo news|ary news|dunya|express news|"
          r"samaa|hum news|ptv|aaj news|bol news|sky sports|eurosport|bein|"
          r"supersport|espn|nfl|nba|mlb|nhl|discovery|national geographic|nat geo|"
          r"history|animal planet|bbc earth|cartoon network|nickelodeon|nick |disney|"
          r"boomerang|pogo|baby tv|pbs kids|mtv|vh1|vevo|4music|kiss tv|now 80s|"
          r"amc|starz|showtime|cinemax|paramount|sony movie|star movies|weathernation|"
          r"weather channel|accuweather|usa network|tnt|tbs|tcm|comedy central|syfy|"
          r"bravo|e! |cbsn|abc |nbc |fox |al arabiya|bbc arabic|rt |cgtn|i24")


# Pay-TV / subscription brands. A free stream of these is almost always a pirate
# restream - we only keep them when they arrive via a licensed FAST platform.
PAY_TV = (r"star plus|star jalsha|star sports|star movies|star gold|star utsav|"
          r"star vijay|star maa|star pravah|star bharat|jalsha movies|"
          r"zee tv|zee bangla|zee cinema|zee anmol|zee classic|&tv|&pictures|&flix|"
          r"sony entertainment|sony sab|sony max|sony pix|sony ten|sony sports|"
          r"sony bbc|colors tv|colors bangla|rishtey|viacom18|"
          r"hbo|cinemax|showtime|starz|amc |starzplay|"
          r"sky sports|bt sport|tnt sports|bein sport|espn|fox sports|"
          r"ten sports|ptv sports|geo super|dsport|supersport|"
          r"cartoon network|nickelodeon|disney channel|disney junior|disney xd|"
          r"national geographic|nat geo|discovery channel|animal planet|"
          r"star movies|movies now|mn+ |hbo max|paramount network")
FAST_SOURCES = {"IPTV_PlutoTV_VERIFIED.m3u", "IPTV_FAST_Services_VERIFIED.m3u"}


def is_paytv(name):
    return bool(re.search(PAY_TV, " " + name.lower() + " "))


def is_brand(name):
    return bool(re.search(BRANDS, " " + name.lower() + " "))


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


def norm_name(n):
    n = re.sub(r"\(.*?\)|\[.*?\]", "", n)
    n = re.sub(r"\b(hd|fhd|uhd|sd|4k|1080p|720p|480p|360p)\b", "", n, flags=re.I)
    n = re.sub(r"[^a-z0-9 ]", " ", n.lower())
    return re.sub(r"\s+", " ", n).strip()


# ------------------------------------------------ 1. popularity = carriers
carriers = defaultdict(set)
for fn in glob.glob("src/*.m3u") + glob.glob("src/fast/*.m3u"):
    base = os.path.basename(fn)
    for e, u in parse(fn):
        name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
        carriers[norm_name(name)].add(base)
POP = {k: len(v) for k, v in carriers.items()}
print("distinct names in sources:", len(POP))

# ------------------------------------------------ 2. url -> category
urlcat = {}
for fn in glob.glob("categories/*.m3u"):
    cat = os.path.basename(fn)[:-4].replace("_and_", " & ").replace("_", " ")
    cat = {"Documentary & Science": "Documentary & Science"}.get(cat, cat)
    for e, u in parse(fn):
        urlcat[u] = cat
print("categorised urls:", len(urlcat))

# ------------------------------------------------ 3. candidate pool
SOURCES = ["IPTV_World_VERIFIED.m3u", "IPTV_Other_Sources_VERIFIED.m3u",
           "IPTV_Index_Extra_VERIFIED.m3u", "IPTV_FAST_Services_VERIFIED.m3u",
           "IPTV_PlutoTV_VERIFIED.m3u"]

globals()["seen_url"] = set()
cands, youtube = [], []


def country_from(group):
    for cname, flag in COUNTRIES:
        if cname in group:
            return cname, flag
    return "International", "🌐"


for fn in SOURCES:
    for e, u in parse(fn):
        if u in seen_url:
            continue
        seen_url.add(u)
        d = dict(ATTR.findall(e))
        name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
        grp = d.get("group-title", "")
        cname, flag = country_from(grp)
        cat = urlcat.get(u) or "Other"
        cands.append({"name": name, "url": u, "logo": d.get("tvg-logo", ""),
                      "tvg_id": d.get("tvg-id", ""), "country": cname, "flag": flag,
                      "cat": cat, "extinf": e, "yt": False,
                      "fast": fn in FAST_SOURCES})

for e, u in parse("IPTV_YouTube_Live.m3u"):
    d = dict(ATTR.findall(e))
    name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
    grp = d.get("group-title", "")
    cname, flag = country_from(grp)
    youtube.append({"name": name, "url": u, "logo": d.get("tvg-logo", ""),
                    "tvg_id": d.get("tvg-id", ""), "country": cname, "flag": flag,
                    "cat": urlcat.get(u) or ("News" if "News" in grp else "Other"),
                    "extinf": e, "yt": True})

print("candidates:", len(cands), "| youtube:", len(youtube))

# ------------------------------------------------ 4. YouTube -> HLS replacement
by_key = defaultdict(list)
for c in cands:
    by_key[norm_name(c["name"])].append(c)

replaced, orphan = [], []
for y in youtube:
    k = norm_name(y["name"])
    ALIAS = {
        "al jazeera english": "al jazeera", "al jazeera arabic": "al jazeera العربية",
        "dw news": "dw english", "bbc news": "bbc news",
        "cnbc television": "cnbc", "bloomberg television": "bloomberg tv",
        "cna": "cna singapore", "arirang news": "arirang tv",
        "pbs newshour": "pbs", "abc news": "abc news",
        "atn bangla news": "atn bangla", "channel i": "channel i",
        "maasranga news": "maasranga tv", "gtv news": "gtv",
        "global tv": "global tv", "channel 24": "channel 24",
        "jamuna tv": "jamuna television", "somoy tv": "somoy news",
    }
    hit = by_key.get(k)
    if not hit and k in ALIAS:
        hit = by_key.get(ALIAS[k])
    if hit:
        replaced.append((y["name"], hit[0]["name"]))
    else:
        orphan.append(y)

print(f"\nYouTube -> HLS replaced: {len(replaced)}/{len(youtube)}")
for a, b in replaced:
    print(f"   ✔ {a:26} -> {b}")
print("no HLS alternative:", len(orphan))
for y in orphan:
    print(f"   ✘ {y['name']}")

# drop pay-TV brands unless they came from a licensed FAST platform
before = len(cands)
cands = [c for c in cands if (not is_paytv(c["name"])) or c.get("fast")]
print(f"pay-TV filter: removed {before - len(cands)} channels")

# ------------------------------------------------ 5. score & select
for c in cands:
    k = norm_name(c["name"])
    c["pop"] = POP.get(k, 0)
    c["brand"] = is_brand(c["name"])
    c["score"] = c["pop"] * 2 + (25 if c["brand"] else 0) + (2 if c["logo"] else 0)

# best entry per (country, name)
best = {}
for c in cands:
    key = (c["country"], norm_name(c["name"]))
    if key not in best or c["score"] > best[key]["score"]:
        best[key] = c
uniq = list(best.values())
print("\nafter name-dedupe:", len(uniq))

TARGET = 2600
PER_COUNTRY = {"United States": 260, "United Kingdom": 160, "India": 200,
               "Bangladesh": 60, "Pakistan": 60, "Canada": 90, "Germany": 90,
               "Italy": 80, "Spain": 70, "France": 80, "Mexico": 60, "Brazil": 60}
DEFAULT_CAP = 35

picked, per_country = [], Counter()
for c in sorted(uniq, key=lambda x: (-x["brand"], -x["score"])):
    cap = PER_COUNTRY.get(c["country"], DEFAULT_CAP)
    if per_country[c["country"]] >= cap:
        continue
    picked.append(c)
    per_country[c["country"]] += 1
    if len(picked) >= TARGET:
        break

# make sure the orphan YouTube channels that are big names are still included,
# clearly marked as YouTube-only
for y in orphan:
    if is_brand(y["name"]):
        y["yt_only"] = True
        y.setdefault("score", 0)
        y.setdefault("pop", 0)
        y.setdefault("brand", True)
        picked.append(y)

print("picked:", len(picked))
print("by country:", per_country.most_common(12))

# ------------------------------------------------ 6. write
def group_of(c):
    cat = c["cat"] if c["cat"] in CAT_ICON else "Other"
    return f"{c['flag']} {c['country']} · {CAT_ICON[cat]} {cat}"


order_c = {c[0]: i for i, c in enumerate(COUNTRIES)}
picked.sort(key=lambda c: (order_c.get(c["country"], 99), c["country"],
                           c["cat"], -c["score"], c["name"].lower()))

with open("IPTV_POPULAR.m3u", "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n")
    f.write("# POPULAR / CURATED playlist - the channels people actually watch\n")
    f.write("# Group format:  <flag> <Country> . <category icon> <category>\n")
    f.write("#   so you can filter by COUNTRY or by CATEGORY in your player\n")
    f.write("# YouTube-only entries are marked [YT] in the name\n")
    f.write(f"# TOTAL CHANNELS: {len(picked)}\n")
    cur = None
    for c in picked:
        g = group_of(c)
        if g != cur:
            cur = g
            n = sum(1 for x in picked if group_of(x) == g)
            f.write(f"\n# ====== {g} ({n}) ======\n")
        name = c["name"]
        tvg_id = c["tvg_id"]
        if c.get("yt_only"):
            name = name + " [YT]"
            tvg_id = tvg_id or "yt"
        f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{name}" '
                f'tvg-logo="{c["logo"]}" group-title="{g}",{name}\n{c["url"]}\n')

print("IPTV_POPULAR.m3u written")

json.dump({"total": len(picked),
           "by_country": dict(per_country),
           "youtube_replaced": replaced,
           "youtube_only": [y["name"] for y in picked if y.get("yt_only")]},
          open("popular_stats.json", "w"), indent=1)
