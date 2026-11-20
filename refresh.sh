#!/usr/bin/env bash
# Re-download the source playlists and rebuild everything.
set -e
cd "$(dirname "$0")"
mkdir -p src
for c in bd in pk us uk ca au nz ae sa qa kw om bh my sg id ph th vn np lk mv tr de fr it es nl be ch at se no dk fi pl ru ua ro gr pt ie br ar mx cl co pe za ng ke eg ma cn jp kr hk tw ir iq af mm kh al ba bg hr cz hu is lt lv rs sk si; do
  curl -s -m 45 -o "src/$c.m3u" "https://iptv-org.github.io/iptv/countries/$c.m3u" &
done
curl -s -m 45 -o src/lang_ben.m3u https://iptv-org.github.io/iptv/languages/ben.m3u &
wait
rm -f src/gb.m3u
python3 build_playlist.py
python3 check_streams.py IPTV_World_by_Country.m3u live_status.json
python3 make_verified.py
echo "DONE - playlists refreshed"
