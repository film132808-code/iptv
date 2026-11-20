#!/usr/bin/env bash
# Rebuild EVERY playlist from scratch. Takes about 5-8 minutes.
# Usage:  bash update_all.sh
set -e
cd "$(dirname "$0")"

COUNTRIES="bd in pk us uk ca au nz ae sa qa kw om bh my sg id ph th vn np lk mv tr de fr it es nl be ch at se no dk fi pl ru ua ro gr pt ie br ar mx cl co pe za ng ke eg ma cn jp kr hk tw ir iq af mm kh al ba bg hr cz hu is lt lv rs sk si"
FAST="samsungtvplus_all samsungtvplus_at samsungtvplus_ca samsungtvplus_ch \
samsungtvplus_de samsungtvplus_es samsungtvplus_fr samsungtvplus_gb samsungtvplus_in \
samsungtvplus_it samsungtvplus_kr samsungtvplus_us plutotv_all plutotv_ar plutotv_br \
plutotv_ca plutotv_cl plutotv_de plutotv_dk plutotv_es plutotv_fr plutotv_gb plutotv_it \
plutotv_mx plutotv_no plutotv_se plutotv_us plex_all plex_au plex_ca plex_es plex_fr \
plex_gb plex_mx plex_nz plex_us roku_all tubi_all"
FAST_BASE="https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists"

mkdir -p src src/fast

echo "==> [1/9] downloading iptv-org country playlists"
for c in $COUNTRIES; do
  curl -s -m 60 -o "src/$c.m3u" "https://iptv-org.github.io/iptv/countries/$c.m3u" &
done
curl -s -m 120 -o src/index_full.m3u "https://iptv-org.github.io/iptv/index.m3u" &
curl -s -m 60  -o src/lang_ben.m3u  "https://iptv-org.github.io/iptv/languages/ben.m3u" &
wait
rm -f src/gb.m3u

echo "==> [2/9] downloading Free-TV + FAST platform playlists"
curl -s -m 120 -o src/freetv.m3u \
  "https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8" &
for f in $FAST; do curl -s -m 60 -o "src/fast/$f.m3u" "$FAST_BASE/$f.m3u" & done
wait

echo "==> [3/9] checking YouTube live status (optional, skipped if yt-dlp missing)"
if command -v yt-dlp >/dev/null 2>&1; then
  python3 check_youtube.py > /tmp/yt.log 2>&1 || echo "    (youtube check failed - keeping old data)"
  tail -1 /tmp/yt.log || true
else
  echo "    yt-dlp not installed - keeping existing yt_status.json"
fi

echo "==> [4/9] building country playlists + testing them"
python3 build_playlist.py | head -1
python3 check_streams.py IPTV_World_by_Country.m3u live_status.json | tail -1
python3 make_verified.py

echo "==> [5/9] building extra sources (Free-TV + index) + testing"
python3 build_extras.py | tail -1
python3 check_streams.py IPTV_Other_Sources.m3u live_extra.json | tail -1
python3 build_index_extra.py | tail -1
python3 check_streams.py IPTV_Index_Extra.m3u live_index.json | tail -1

echo "==> [6/9] building FAST services (Samsung/Plex/Pluto/Roku/Tubi) + testing"
python3 build_fast_services.py | tail -1
python3 check_streams.py IPTV_FAST_Services.m3u live_fast.json | tail -1
python3 make_fast_verified.py

echo "==> [7/9] building own Pluto TV playlist + testing"
python3 pluto_m3u.py us
python3 check_streams.py IPTV_PlutoTV.m3u live_pluto.json | tail -1
python3 make_pluto_verified.py

echo "==> [8/9] merging the master playlist"
python3 build_master.py

echo "==> [9/9] categories, curated popular list, Bangla list"
python3 build_categories.py | tail -1
python3 build_popular.py | tail -2
python3 build_bangla.py | head -1

echo ""
echo "DONE. Playlist sizes:"
python3 - <<'PY'
import glob, os
for f in sorted(glob.glob("IPTV_*.m3u")):
    n = sum(1 for l in open(f, encoding="utf-8", errors="replace")
            if l.startswith("#EXTINF"))
    print(f"  {f:38} {n:6} channels  ({os.path.getsize(f)//1024} KB)")
PY
