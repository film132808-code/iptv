#!/usr/bin/env python3
"""Split every channel we have into category-based playlists."""
import re, os, json, glob
from collections import defaultdict, Counter

ATTR = re.compile(r'([a-zA-Z0-9\-]+)="([^"]*)"')

# ---- category normalisation ------------------------------------------------
# iptv-org uses "A;B" style multi-categories. Map each to ONE clean bucket.
CAT_MAP = {
    "news": "News", "sports": "Sports", "movies": "Movies", "movie": "Movies",
    "kids": "Kids", "animation": "Kids", "cartoon": "Kids", "family": "Kids",
    "music": "Music", "documentary": "Documentary & Science",
    "science": "Documentary & Science", "education": "Documentary & Science",
    "religious": "Religious", "entertainment": "Entertainment",
    "comedy": "Entertainment", "series": "Entertainment", "general": "Entertainment",
    "lifestyle": "Lifestyle", "cooking": "Lifestyle", "travel": "Lifestyle",
    "outdoor": "Lifestyle", "auto": "Lifestyle", "shop": "Lifestyle",
    "culture": "Lifestyle", "business": "Business", "weather": "Weather",
    "relax": "Music", "classic": "Movies", "culture/cooking": "Lifestyle",
    # extra vocabulary used by FAST platforms (Samsung / Plex / Tubi)
    "reality": "Entertainment", "reality tv": "Entertainment",
    "crime": "Documentary & Science", "true crime": "Documentary & Science",
    "drama": "Entertainment", "action & drama": "Entertainment",
    "tv dramas": "Entertainment", "series": "Entertainment",
    "film": "Movies", "filme": "Movies", "filmes": "Movies", "film & tv": "Movies",
    "peliculas": "Movies", "películas": "Movies", "cinema": "Movies",
    "action": "Movies", "horror": "Movies", "romance": "Movies",
    "sci-fi": "Movies", "sci-fi & supernatural": "Movies", "mystery": "Movies",
    "western": "Movies", "thriller": "Movies",
    "sport": "Sports", "sports & outdoors": "Sports", "motor": "Sports",
    "auto & motorsports": "Sports", "pro wrestling": "Sports", "bowling": "Sports",
    "documentaries": "Documentary & Science", "documentary": "Documentary & Science",
    "science & nature": "Documentary & Science", "animals": "Documentary & Science",
    "history": "Documentary & Science", "paranormal": "Documentary & Science",
    "home & food": "Lifestyle", "cooking": "Lifestyle", "food": "Lifestyle",
    "travel": "Lifestyle", "home improvement": "Lifestyle", "auction": "Lifestyle",
    "shopping": "Lifestyle", "art": "Lifestyle",
    "faith & family": "Religious", "faith": "Religious",
    "kids & family": "Kids", "children": "Kids", "children-music": "Kids",
    "animated": "Kids", "anime": "Entertainment",
    "latino": "Entertainment", "espanol": "Entertainment", "español": "Entertainment",
    "national news": "News", "local news": "News", "global news": "News",
    "business news": "News", "weather": "Weather",
    "game show": "Entertainment", "games & competition": "Entertainment",
    "classic tv": "Entertainment", "pop culture": "Entertainment",
    "black entertainment": "Entertainment", "educational": "Documentary & Science",
    "gaming & tech": "Entertainment", "environment": "Documentary & Science",
    "health": "Lifestyle", "movie channels": "Movies", "tv & entertainment": "Entertainment",
    "good eats": "Lifestyle", "crime drama": "Movies", "card games": "Entertainment",
}

BUCKETS = ["News", "Sports", "Movies", "Entertainment", "Kids", "Music",
           "Documentary & Science", "Religious", "Lifestyle", "Business",
           "Weather", "Other"]

ICON = {
    "News": "📰 News", "Sports": "⚽ Sports", "Movies": "🎬 Movies",
    "Entertainment": "🎭 Entertainment", "Kids": "🧸 Kids",
    "Music": "🎵 Music", "Documentary & Science": "🔬 Documentary & Science",
    "Religious": "🕌 Religious", "Lifestyle": "🍳 Lifestyle & Travel",
    "Business": "💼 Business", "Weather": "🌦 Weather", "Other": "📦 Other",
}

# name-keyword fallback when the source gave no category
KEYWORDS = [
    (r"\bnews\b|24\/7 news|news24|ntv|aaj ?tak|abp|zee news|cnn|bbc news", "News"),
    (r"\bsport|sports\b|football|cricket|tennis|golf|nba|nfl|fifa|euro ?sport", "Sports"),
    (r"\bmovie|cinema|film|thriller|horror|bollywood|hollywood", "Movies"),
    (r"\bkids?\b|cartoon|junior|baby|toon|nick|disney", "Kids"),
    (r"\bmusic|hits|mtv|vevo|dance|radio|fm\b", "Music"),
    (r"\bdocu|discover|science|nature|history|wild|earth|space", "Documentary & Science"),
    (r"\bquran|islam|azan|islamic|masjid|deen|bhakti|church|gospel|dharm", "Religious"),
    (r"\bfood|cook|travel|life|style|fashion|home|garden|auto|car", "Lifestyle"),
    (r"\bbiz|business|market|finance|money|stock|bloomberg|cnbc", "Business"),
    (r"\bweather|meteo|climate", "Weather"),
    # extra patterns that were landing in "Other"
    (r"mubasher|al ?hurra|al ?jazeera|al ?arabiya|saudiya|iraqia|africanews|"
     r"sky news|france ?24|euronews|dw |nhk|trt |cna |wion|news ?18|"
     r"tv9|tv5|abp|aaj|republic|times now|firstpost|india today|ndtv", "News"),
    (r"crime|police|detective|investigat|forensic|murder", "Documentary & Science"),
    (r"reality|telenovela|novela|drama|soap", "Entertainment"),
    (r"bollywood|kollywood|tollywood|anime|classic tv", "Movies"),
    (r"quran|makkah|madina|noor|islam|imaan|taqwa", "Religious"),
]

ADULT = re.compile(r"\b(xxx|adult|porn|erotic|18\+|sex)\b", re.I)


def norm(cat):
    if not cat:
        return None
    parts = [p.strip().lower() for p in re.split(r"[;,/|]", cat)]
    for p in parts:
        if p in CAT_MAP:
            return CAT_MAP[p]
    for p in parts:
        for k, v in CAT_MAP.items():
            if k in p:
                return v
    return None


def from_name(name):
    n = name.lower()
    for pat, bucket in KEYWORDS:
        if re.search(pat, n):
            return bucket
    return None


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
                out.append((a, name.strip(' "'), s, s))
                pending = None
    return out


def parse_pairs(path):
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


# ---- 1. build a URL -> category map from every original source ------------
urlcat = {}

# iptv-org country + full index files: group-title IS the category
for fn in glob.glob("src/*.m3u"):
    for e, u in parse_pairs(fn):
        m = ATTR.findall(e)
        d = dict(m)
        c = norm(d.get("group-title", ""))
        if c and u not in urlcat:
            urlcat[u] = c

# Free-TV: no category, but names are descriptive -> handled by fallback
# Pluto: category lives in group-title
for e, u in parse_pairs("IPTV_PlutoTV_VERIFIED.m3u"):
    d = dict(ATTR.findall(e))
    c = norm(d.get("group-title", "").replace("🔴 Pluto TV · ", ""))
    if c:
        urlcat[u] = c

# FAST platforms, per-region files carry the real category in group-title
REGION_WORDS = {"United States", "United Kingdom", "Canada", "India", "Germany",
                "France", "Italy", "Spain", "Austria", "Switzerland", "Korea",
                "South Korea", "Australia", "NZ", "Mexico", "Argentina", "Brazil",
                "Chile", "Denmark", "Norway", "Sweden", "New Zealand"}
for fn in glob.glob("src/fast/*.m3u"):
    for e, u in parse_pairs(fn):
        d = dict(ATTR.findall(e))
        gt = d.get("group-title", "")
        if not gt or gt in REGION_WORDS:
            continue
        c = norm(gt)
        if c:
            urlcat[u] = c

# YouTube: explicit categories
if os.path.exists("yt_status.json"):
    for r in json.load(open("yt_status.json")):
        c = norm(r.get("cat", ""))
        if c:
            urlcat[r["url"]] = c

print(f"category map: {len(urlcat)} urls")

# ---- 2. take every channel we ship ---------------------------------------
sources = ["IPTV_MASTER.m3u", "IPTV_PlutoTV_VERIFIED.m3u"]
seen = set()
rows = []
for fn in sources:
    for e, u in parse_pairs(fn):
        if u in seen:
            continue
        seen.add(u)
        d = dict(ATTR.findall(e))
        name = e.split('",')[-1].strip(' "') if '",' in e else e.rsplit(",", 1)[-1]
        cat = urlcat.get(u) or from_name(name) or "Other"
        rows.append({"cat": cat, "name": name, "url": u, "extinf": e})

print("total channels:", len(rows))
print(Counter(r["cat"] for r in rows).most_common())

# ---- 3. write one file per category --------------------------------------
os.makedirs("categories", exist_ok=True)
written = {}
for bucket in BUCKETS:
    ents = [r for r in rows if r["cat"] == bucket]
    if not ents:
        continue
    ents.sort(key=lambda r: r["name"].lower())
    fn = f"categories/{bucket.replace(' ', '_').replace('&', 'and')}.m3u"
    with open(fn, "w", encoding="utf-8", newline="\n") as f:
        f.write("#EXTM3U\n")
        f.write(f"# {bucket} channels - {len(ents)} total\n")
        f.write(f"# group-title=\"{ICON[bucket]}\"\n")
        for r in ents:
            e = re.sub(r'group-title="[^"]*"', f'group-title="{ICON[bucket]}"', r["extinf"])
            f.write(e + "\n" + r["url"] + "\n")
    written[bucket] = len(ents)
    print(f"  {fn}: {len(ents)}")

# ---- 4. one combined file grouped by category ---------------------------
with open("IPTV_By_Category.m3u", "w", encoding="utf-8", newline="\n") as f:
    f.write("#EXTM3U\n")
    f.write("# All channels grouped by category\n")
    f.write(f"# TOTAL CHANNELS: {len(rows)}\n")
    for bucket in BUCKETS:
        ents = sorted([r for r in rows if r["cat"] == bucket],
                      key=lambda r: r["name"].lower())
        if not ents:
            continue
        f.write(f"\n# ====== {ICON[bucket]} ({len(ents)}) ======\n")
        for r in ents:
            e = re.sub(r'group-title="[^"]*"', f'group-title="{ICON[bucket]}"', r["extinf"])
            f.write(e + "\n" + r["url"] + "\n")
print(f"IPTV_By_Category.m3u: {len(rows)}")

json.dump(written, open("categories/summary.json", "w"), indent=2)
