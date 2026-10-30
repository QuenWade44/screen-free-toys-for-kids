"""Pinterest bulk-upload CSV validator. Every file must pass before it is delivered.

Usage: python3 validate_csv.py FILE.csv --boards "Board A|Board B" [--check-urls]
"""
import csv, sys, re, argparse, datetime as dt, urllib.request
from collections import Counter

HEADER = ["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"]
MAX_ROWS = 80          # Pinterest allows 100 scheduled pins per account; stay under it with room to spare
MAX_PER_DAY = 5

def validate(path, boards, check_urls=False):
    errs = []
    with open(path, newline="", encoding="utf-8") as f:
        raw = f.read()
    if raw.startswith("﻿"):
        errs.append("File has a BOM; save as plain UTF-8")
    rows = list(csv.reader(raw.splitlines()))
    if rows[0] != HEADER:
        errs.append(f"Header must be exactly: {','.join(HEADER)}")
    data = [dict(zip(HEADER, r)) for r in rows[1:] if any(r)]
    if len(data) > MAX_ROWS:
        errs.append(f"{len(data)} rows; max {MAX_ROWS} per file (Pinterest 100-scheduled-pin cap)")
    titles = Counter(r["Title"] for r in data)
    for t, n in titles.items():
        if n > 1: errs.append(f"Duplicate title x{n}: {t}")
    days = Counter()
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    for i, r in enumerate(data, 2):
        if not r["Title"] or len(r["Title"]) > 100: errs.append(f"Row {i}: title empty or over 100 chars")
        if len(r["Description"]) > 500: errs.append(f"Row {i}: description over 500 chars")
        if boards and r["Pinterest board"] not in boards: errs.append(f"Row {i}: unknown board '{r['Pinterest board']}'")
        if not re.match(r"^https://\S+\.(png|jpg|jpeg|mp4)$", r["Media URL"], re.I): errs.append(f"Row {i}: Media URL must be a direct https link to .png/.jpg/.mp4")
        if not r["Link"].startswith("https://"): errs.append(f"Row {i}: Link must start with https://")
        if "amazon.com" in r["Link"] and "tag=" not in r["Link"]: errs.append(f"Row {i}: Amazon link missing ?tag=")
        try:
            d = dt.datetime.strptime(r["Publish date"], "%Y-%m-%dT%H:%M:%S")
            if d <= now: errs.append(f"Row {i}: publish date is in the past")
            days[d.date()] += 1
        except ValueError:
            errs.append(f"Row {i}: publish date must look like 2026-12-01T14:00:00 (UTC)")
        if not r["Keywords"]: errs.append(f"Row {i}: keywords empty")
    if check_urls:
        for i, r in enumerate(data, 2):
            try:
                code = urllib.request.urlopen(urllib.request.Request(r["Media URL"], method="HEAD"), timeout=20).status
                if code != 200: errs.append(f"Row {i}: image returns {code}")
            except Exception as e:
                errs.append(f"Row {i}: image not reachable ({e})")
    return data, errs

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--boards", default=""); ap.add_argument("--check-urls", action="store_true")
    a = ap.parse_args()
    data, errs = validate(a.file, set(b for b in a.boards.split("|") if b), a.check_urls)
    print(f"{a.file}: {len(data)} rows, {'PASS' if not errs else 'FAIL'}")
    for e in errs[:50]: print("  -", e)
    sys.exit(1 if errs else 0)
