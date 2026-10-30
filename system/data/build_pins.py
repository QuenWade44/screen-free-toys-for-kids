import csv, json, os, re, datetime as dt
from data_posts import POSTS
from selected import SEL

TAG = "screenfreet0f-20"
START = dt.date(2026, 11, 2)
TIME = "23:00:00"  # UTC = 5pm Central / 6pm Eastern
MEDIA = "https://raw.githubusercontent.com/GITHUB-USER/GITHUB-REPO/main/videos/day{d:03d}.mp4"
OUT = "/home/claude/pins_out"
os.makedirs(OUT, exist_ok=True)
B = {b["key"]: b["name"] for b in json.load(open("/home/claude/assets_build/boards.json"))}
DISC = "Contains affiliate links. As an Amazon Associate I earn from qualifying purchases."

def link(a): return f"https://www.amazon.com/dp/{a}?tag={TAG}"
def tc(s):
    small = {"a","an","and","for","of","the","to","with","at","in","on","or","vs"}
    return " ".join(w if (i and w in small) else w[:1].upper()+w[1:] for i, w in enumerate(s.split(" ")))

rows, prod_days = [], {}
for i, p in enumerate(POSTS, 1):
    seo, kw, lts, board, *_ , promise, aud, printable = p
    sel = SEL[i]
    hero = sel[0]
    alt = sel[1]
    third = sel[2] if len(sel) > 2 else sel[1]
    cheap = min(sel, key=lambda x: x[2])
    kws = [kw, lts[0], lts[1], kw, lts[2], lts[0], kw]
    picks = [hero, hero, hero, hero, alt, cheap, third]
    for a in range(7):
        day = (i - 1) * 7 + a + 1
        asin, name, price, rating, nr, bought = picks[a]
        K = tc(kws[a])
        under = next(b for b in (10, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 300, 400) if price <= b)
        titles = [
            f"{K}: A School Psychologist's Pick",
            f"{K}: {tc(promise)}",
            f"{K}: Is the {name} Worth It?",
            f"{K}: How We Use the {name}",
            f"{K}: Skip the Mistake, Try the {name}",
            f"{K} Under ${under}: {name}",
            f"{K}: Save This Pick",
        ]
        t = titles[a]
        if len(t) > 100:
            t = f"{K}: {name}"[:100]
        openers = ["Looking for", "Want", "Wondering about", "Need ideas for", "Struggling with", "Shopping on a budget for", "Planning"]
        desc = (f"{openers[a]} {kws[a]}? I'm a Ph.D. school psychologist, and the {name} is my pick for {promise}. "
                f"Tap to see today's price and reviews on Amazon. {DISC}")
        assert len(t) <= 100 and len(desc) <= 500, (t, len(desc))
        date = START + dt.timedelta(days=day - 1)
        rows.append(dict(day=day, date=date, post=i, kw=kws[a], board=B[board], title=t, desc=desc, link=link(asin),
                         asin=asin, product=name, price=price, bought=bought,
                         keywords=", ".join(dict.fromkeys([kw] + lts))))
        prod_days.setdefault(asin, {"name": name, "price": price, "rating": rating, "nr": nr, "bought": bought, "days": [], "posts": set()})
        prod_days[asin]["days"].append(day)
        prod_days[asin]["posts"].add(i)
# day 365 bonus: repeat post 1 hero
h = SEL[1][0]
r = dict(rows[0]); r.update(day=365, date=START + dt.timedelta(days=364), title="Screen Free Christmas Gifts: This Year's Top Pick")
rows.append(r); prod_days[h[0]]["days"].append(365)
assert len(rows) == 365

# master file (with helper columns)
with open(f"{OUT}/365-pins-MASTER.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Day", "Date", "Search keyword", "Pinterest board", "Title", "Description", "Affiliate link", "Product", "ASIN", "Price (Oct 30)", "Bought last month (Oct 30)", "Keywords", "Video file name"])
    for r in rows:
        w.writerow([r["day"], r["date"].isoformat(), r["kw"], r["board"], r["title"], r["desc"], r["link"], r["product"], r["asin"], f"${r['price']:.2f}", r["bought"], r["keywords"], f"day{r['day']:03d}.mp4"])

# monthly Pinterest-format files
os.makedirs(f"{OUT}/monthly-upload-files", exist_ok=True)
by_month = {}
for r in rows:
    by_month.setdefault((r["date"].year, r["date"].month), []).append(r)
for n, ((y, m), rs) in enumerate(sorted(by_month.items()), 1):
    fn = f"{OUT}/monthly-upload-files/{n:02d}-{y}-{m:02d}-{dt.date(y, m, 1).strftime('%b')}-{len(rs)}pins.csv"
    with open(fn, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Title", "Media URL", "Pinterest board", "Thumbnail", "Description", "Link", "Publish date", "Keywords"])
        for r in rs:
            w.writerow([r["title"], MEDIA.format(d=r["day"]), r["board"], "00:01", r["desc"], r["link"], f"{r['date'].isoformat()}T{TIME}", r["keywords"]])

# product links
with open(f"{OUT}/amazon-affiliate-links.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ASIN", "Product", "Your affiliate link", "Price (Oct 30)", "Rating", "# Ratings", "Bought last month (Oct 30)", "Used in week #", "Pin days", "First pin date"])
    for a, d in sorted(prod_days.items(), key=lambda kv: min(kv[1]["days"])):
        w.writerow([a, d["name"], link(a), f"${d['price']:.2f}", d["rating"], d["nr"], d["bought"], " ".join(map(str, sorted(d["posts"]))), " ".join(map(str, d["days"])), (START + dt.timedelta(days=min(d["days"]) - 1)).isoformat()])
print(len(prod_days), "products;", len(by_month), "monthly files;", max(len(r["title"]) for r in rows), "max title")
