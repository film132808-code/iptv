#!/usr/bin/env bash
# Refresh the FAST platform playlists (Samsung TV Plus, Plex, Pluto, Roku, Tubi)
set -e
cd "$(dirname "$0")"
mkdir -p src/fast
BASE="https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/main/playlists"
for f in samsungtvplus_all samsungtvplus_at samsungtvplus_ca samsungtvplus_ch \
         samsungtvplus_de samsungtvplus_es samsungtvplus_fr samsungtvplus_gb \
         samsungtvplus_in samsungtvplus_it samsungtvplus_kr samsungtvplus_us \
         plutotv_all plutotv_ar plutotv_br plutotv_ca plutotv_cl plutotv_de \
         plutotv_dk plutotv_es plutotv_fr plutotv_gb plutotv_it plutotv_mx \
         plutotv_no plutotv_se plutotv_us plex_all plex_au plex_ca plex_es \
         plex_fr plex_gb plex_mx plex_nz plex_us roku_all tubi_all; do
  curl -sL -m 60 -o "src/fast/$f.m3u" "$BASE/$f.m3u" &
done
wait
python3 build_fast_services.py
python3 check_streams.py IPTV_FAST_Services.m3u live_fast.json | tail -1
python3 make_fast_verified.py
python3 build_master.py
python3 build_categories.py
echo "DONE"
