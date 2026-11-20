#!/usr/bin/env bash
# Rebuild the category playlists from the current master + Pluto files.
set -e
cd "$(dirname "$0")"
python3 build_categories.py
echo "DONE - see the categories/ folder"
