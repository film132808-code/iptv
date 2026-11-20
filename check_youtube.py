#!/usr/bin/env python3
"""Verify YouTube channels have a live stream, grab title + thumbnail."""
import json, subprocess, concurrent.futures as cf

chans = json.load(open("yt_channels.json"))


def probe(entry):
    name, cc, cat, cid = entry
    url = f"https://www.youtube.com/channel/{cid}/live"
    try:
        r = subprocess.run(
            ["yt-dlp", "--no-warnings", "--simulate", "--print",
             "%(is_live)s\t%(title)s\t%(thumbnail)s\t%(channel_follower_count)s",
             url],
            capture_output=True, text=True, timeout=90)
        out = r.stdout.strip().splitlines()
        if not out:
            return dict(name=name, cc=cc, cat=cat, cid=cid, url=url, live=False, title="")
        parts = out[-1].split("\t")
        live = parts[0].strip() == "True"
        title = parts[1] if len(parts) > 1 else ""
        thumb = parts[2] if len(parts) > 2 else ""
        return dict(name=name, cc=cc, cat=cat, cid=cid, url=url, live=live,
                    title=title, thumb=thumb)
    except Exception as e:
        return dict(name=name, cc=cc, cat=cat, cid=cid, url=url, live=False, title="", err=str(e))


with cf.ThreadPoolExecutor(max_workers=10) as ex:
    res = list(ex.map(probe, chans))

ok = [r for r in res if r["live"]]
bad = [r for r in res if not r["live"]]
print(f"LIVE: {len(ok)} / {len(res)}")
for r in ok:
    print(f"  OK  {r['name']:24} | {r['title'][:50]}")
for r in bad:
    print(f"  --  {r['name']:24} | NOT LIVE NOW ({r['title'][:40]})")
json.dump(res, open("yt_status.json", "w"), indent=1)
