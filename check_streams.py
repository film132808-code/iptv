#!/usr/bin/env python3
"""Check which stream URLs in an M3U actually respond with a playable HLS/stream payload."""
import asyncio, sys, re, json, time
import aiohttp

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
SEM = 250
TIMEOUT = 12


def parse(path):
    out, pending = [], None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#EXTINF"):
                pending = line
            elif line and not line.startswith("#") and pending:
                out.append((pending, line))
                pending = None
    return out


async def check(session, sem, url):
    async with sem:
        for attempt in range(2):
            try:
                async with session.get(url, headers={"User-Agent": UA, "Referer": ""},
                                       timeout=aiohttp.ClientTimeout(total=TIMEOUT),
                                       allow_redirects=True, ssl=False) as r:
                    if r.status not in (200, 206):
                        return url, False, r.status
                    chunk = await r.content.read(2048)
                    ok = b"#EXTM3U" in chunk or b"#EXT-X" in chunk or len(chunk) > 200
                    return url, ok, r.status
            except Exception as e:
                if attempt:
                    return url, False, 0
                await asyncio.sleep(1.0)
        return url, False, 0


async def main(path, out_json):
    entries = parse(path)
    print(f"checking {len(entries)} urls ...", flush=True)
    sem = asyncio.Semaphore(SEM)
    conn = aiohttp.TCPConnector(limit=SEM * 2, ssl=False, force_close=True)
    t0 = time.time()
    res = {}
    async with aiohttp.ClientSession(connector=conn) as s:
        tasks = [asyncio.create_task(check(s, sem, u)) for _, u in entries]
        done = 0
        for coro in asyncio.as_completed(tasks):
            url, ok, st = await coro
            res[url] = (ok, st)
            done += 1
            if done % 500 == 0:
                live = sum(1 for v in res.values() if v[0])
                print(f"  {done}/{len(entries)}  live={live}  {time.time()-t0:.0f}s", flush=True)
    live = sum(1 for v in res.values() if v[0])
    print(f"DONE {live}/{len(entries)} live ({live/len(entries)*100:.0f}%) in {time.time()-t0:.0f}s")
    json.dump({u: [v[0], v[1]] for u, v in res.items()}, open(out_json, "w"))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))
