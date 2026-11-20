#!/usr/bin/env bash
# Rebuild the curated popular playlist from the current verified sources.
set -e
cd "$(dirname "$0")"
python3 build_categories.py
python3 build_popular.py
echo "DONE - IPTV_POPULAR.m3u rebuilt"
python3 build_bangla.py
echo "DONE - IPTV_POPULAR.m3u + IPTV_Bangla_Bollywood.m3u rebuilt"
