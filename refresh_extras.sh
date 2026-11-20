#!/usr/bin/env bash
# Refresh the extra sources (Free-TV + YouTube) and rebuild the master lists.
set -e
cd "$(dirname "$0")"
mkdir -p src
echo "-> downloading Free-TV playlist"
curl -s -m 90 -o src/freetv.m3u https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8
echo "-> checking which YouTube channels are live"
python3 check_youtube.py | head -3
echo "-> building playlists"
python3 build_extras.py
echo "-> testing every new stream (about a minute)"
python3 check_streams.py IPTV_Other_Sources.m3u live_extra.json | tail -2
python3 build_master.py
echo "DONE"
