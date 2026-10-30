import json, re, datetime as dt, csv, os, sys
from sl_data import P, BOARDS, board_for

TAG = sys.argv[1] if len(sys.argv) > 1 else "screenfreet0f-20"
RAW = "https://raw.githubusercontent.com/QuenWade44/screen-free-toys-for-kids/sideline-ready-2026-11/sideline-ready/pins/2026-11/"
DISC = "Contains affiliate links. As an Amazon Associate I earn from qualifying purchases."
BN = {k: n for k, n, d in BOARDS}
PROMISE = dict(bag="every practice and game", seat="long games on hard bleachers", cold="freezing bleachers and night games",
               wagon="hauling chairs, coolers and gear to the field", travel="tournament weekends", gifts="the sports mom on your list",
               coach="coaches and team moms", dad="dads at every game", hot="hot fields and long tournaments", gameday="game day")
ICONDESC = dict(bag="a sideline tote bag", seat="a stadium seat", cold="a snowflake and a hot drink", wagon="a sports wagon",
                travel="a cooler and a ball", gifts="a gift box", coach="a coach's whistle", dad="a folding chair",
                hot="a sun and a fan", gameday="a clear stadium bag")

def tc(s):
    small = {"a","an","and","for","of","the","to","with","at","in","on","or","vs"}
    return " ".join(w if (i and w in small) else w[:1].upper()+w[1:] for i, w in enumerate(s.split(" ")))

pins = []
for a in P:
    asin, name, price, rating, nr, bought, tier, kws = a
    for j, kw in enumerate(kws):
        b = board_for(kw)
        others = [k for k in kws if k != kw]
        pins.append(dict(asin=asin, name=name, price=price, bought=bought, tier=tier, kw=kw, bkey=b, board=BN[b], others=others, j=j))
assert len(pins) == 150

for n, p in enumerate(pins):
    K, N = tc(p["kw"]), p["name"]
    v = n % 5
    opts = [f"{K}: The {N}", f"{K} | The {N} Parents Love", f"{K}: {N}" if K.lower().startswith("best") else f"Best {K}: {N}",
            f"{K} You'll Actually Use: {N}", f"{K} Checklist Pick: {N}"]
    t = opts[v] if len(opts[v]) <= 100 else f"{K}: {N}"[:100]
    pr = PROMISE[p["bkey"]]
    d = (f"{K}? Add the {N} to your list. It's a top seller with sports parents on Amazon (1,000+ bought in a single month when we added it) "
         f"and makes {pr} easier. Also great for {p['others'][0]} and {p['others'][1]}. Tap to see today's price. {DISC}")
    if len(d) > 500:
        d = f"{K}? Add the {N} to your list. It's a top seller with sports parents on Amazon and makes {pr} easier. Tap to see today's price. {DISC}"
    alt = f"Pin graphic with the headline '{K}' and an illustration of {ICONDESC[p['bkey']]}. It recommends the {N} for {pr}, from Sideline Ready."
    p.update(title=t, desc=d, alt=alt, headline=K, promise=pr[0].upper() + pr[1:], variant=v,
             link=f"https://www.amazon.com/dp/{p['asin']}?tag={TAG}", keywords=", ".join([p["kw"]] + p["others"]))
    assert len(t) <= 100 and len(d) <= 500, (t, len(d))

SLOTS = [("8:00 AM", 14, 0), ("11:00 AM", 17, 0), ("3:00 PM", 21, 0), ("6:00 PM", 0, 1), ("9:00 PM", 3, 1)]
queue = sorted(pins, key=lambda p: (p["tier"], p["j"], P.index(next(x for x in P if x[0] == p["asin"]))))
start = dt.date(2026, 11, 1)
out = []
for d in range(30):
    today = []
    for _ in range(5):
        pick = next((q for q in queue if q["bkey"] not in {t["bkey"] for t in today} and q["asin"] not in {t["asin"] for t in today}), queue[0])
        queue.remove(pick); today.append(pick)
    for s, (label, uh, plus) in enumerate(SLOTS):
        p = today[s]
        local = start + dt.timedelta(days=d)
        utc = dt.datetime(local.year, local.month, local.day, uh) + dt.timedelta(days=plus)
        p.update(seq=d * 5 + s + 1, local_date=local.isoformat(), local_time=label, publish=utc.strftime("%Y-%m-%dT%H:%M:%S"),
                 file=f"sr{d*5+s+1:03d}-{re.sub(r'[^a-z0-9]+','-',p['kw'].lower()).strip('-')}.png")
        out.append(p)
assert len(out) == 150 and not queue
json.dump(out, open("/home/claude/sl_pins.json", "w"), indent=1)

os.makedirs("/home/claude/sl_out", exist_ok=True)
hdr = ["Title","Media URL","Pinterest board","Thumbnail","Description","Link","Publish date","Keywords"]
def row(p): return [p["title"], RAW + p["file"], p["board"], "", p["desc"], p["link"], p["publish"], p["keywords"]]
with open("/home/claude/sl_out/PINTEREST-IMPORT-Sideline-Ready-Nov-2026-150-pins.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(hdr); [w.writerow(row(p)) for p in out]
for n, (a, b, lab) in enumerate([(0, 70, "Nov01-14"), (70, 150, "Nov15-30")], 1):
    with open(f"/home/claude/sl_out/backup-split-{n}-{lab}-{b-a}-pins.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(hdr); [w.writerow(row(p)) for p in out[a:b]]
with open("/home/claude/sl_out/schedule-and-alt-text.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["#","Date","Time (Central)","Board","Search phrase","Title","Alt text","Product","ASIN","Affiliate link","Image file"])
    for p in out: w.writerow([p["seq"],p["local_date"],p["local_time"],p["board"],p["kw"],p["title"],p["alt"],p["name"],p["asin"],p["link"],p["file"]])
with open("/home/claude/sl_out/amazon-affiliate-links.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["ASIN","Product","Affiliate link","Price (Oct 30)","Rating","# Ratings","Bought last month (Oct 30)","Search phrases"])
    for a in P: w.writerow([a[0], a[1], f"https://www.amazon.com/dp/{a[0]}?tag={TAG}", f"${a[2]:.2f}", a[3], a[4], a[5], " / ".join(a[7])])
print("ok", TAG)
for p in out[:6]: print(p["seq"], p["local_time"], p["board"][:22], "|", p["title"])
