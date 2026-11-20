#!/usr/bin/env bash
# Rebuild the Pluto TV playlist (its JWT token expires about every 24 hours).
set -e
cd "$(dirname "$0")"
python3 pluto_m3u.py us
python3 check_streams.py IPTV_PlutoTV.m3u live_pluto.json | tail -1
python3 make_pluto_verified.py
echo "DONE - IPTV_PlutoTV.m3u refreshed"
