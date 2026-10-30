import json, re, datetime as dt, csv, os
from data_posts import POSTS
from selected import SEL

TAG = "screenfreet0f-20"
B = {b["key"]: b for b in json.load(open("/home/claude/assets_build/boards.json"))}
DISC = "Contains affiliate links. As an Amazon Associate I earn from qualifying purchases."

def tc(s):
    small = {"a","an","and","for","of","the","to","with","at","in","on","or","vs"}
    return " ".join(w if (i and w in small) else w[:1].upper()+w[1:] for i, w in enumerate(s.split(" ")))

# keyword (what the parent types) per product, from Pinterest autocomplete phrases
OVR = {(1,1):"screen free gifts for kids",(1,2):"screen free toys for kids",(2,1):"gift ideas for 3 year boy",(2,2):"educational toys for 3 year",
       (5,1):"play couch ideas",(5,2):"play couch reading nook",(6,0):"yoto player",(6,1):"toniebox",(6,2):"yoto player cards",
       (7,1):"travel tray for kids",(10,1):"hatch rest",(10,2):"sound machine kids",(11,1):"visual timers for kids",
       (13,1):"balance board games for kids",(13,2):"balance board kids exercises",(14,2):"sensory bins",(15,1):"feelings chart preschool",
       (21,2):"visual timer for classroom",(24,1):"bug catcher kit for kids",(24,2):"bug catcher kit for kids",
       (27,1):"play kitchen accessories",(27,2):"play kitchen ideas",(28,2):"summer schedule for kids daily checklist",
       (30,2):"road trip with kids activities",(36,2):"kids alarm clock with night light",(42,1):"after school routine for kids",
       (42,2):"after school routine for kids",(47,1):"halloween activities for kids",(49,1):"basement playroom storage",
       (49,2):"basement playroom organization"}
REPEAT = [(1,0,"christmas gifts for kids ideas"),(33,0,"screen free gifts for kids"),(2,0,"gift ideas for 3 year girl"),
          (19,0,"daily routine chart for kids"),(6,0,"screen free christmas gifts"),(3,0,"gift ideas for 7 year olds")]
# November relevance: 1 = gift/holiday/indoor-winter, 2 = evergreen, 3 = off-season
TIER1 = {1,2,3,4,5,6,7,8,12,13,14,22,30,31,32,33,46,48,50,51,52}
TIER3 = {20,23,24,25,26,28,29,35,38,45,47}

def kwfor(i, j):
    if (i, j) in OVR: return OVR[(i, j)]
    kw, lts = POSTS[i-1][1], POSTS[i-1][2]
    c = [kw] + [l for l in lts if not re.search("printable|diy|free |ikea|pdf", l)]
    return c[j] if j < len(c) else c[-1]

pins = []
def add(i, j, kw, rep=False):
    p = POSTS[i-1]
    asin, name, price, rating, nr, bought = SEL[i][j]
    board = B[p[3]]
    promise, aud = p[7], p[8]
    others = [k for k in dict.fromkeys([p[1]] + p[2]) if k != kw and not re.search("printable|diy|free |ikea|pdf", k)][:2]
    pins.append(dict(post=i, idx=j, kw=kw, asin=asin, name=name, price=price, bought=bought, board=board["name"], bkey=p[3],
                     icon=board["icon"], accent=board["accent"], bg=board["bg"], promise=promise, aud=aud, others=others,
                     tier=1 if i in TIER1 else 3 if i in TIER3 else 2, rep=rep))
seen = set()
for i in range(1, 53):
    for j in range(len(SEL[i])):
        if SEL[i][j][0] in seen: continue
        seen.add(SEL[i][j][0]); add(i, j, kwfor(i, j))
for i, j, kw in REPEAT:
    add(i, j, kw, rep=True)
assert len(pins) == 150, len(pins)

# ---- copy ----
for n, p in enumerate(pins):
    K, N = tc(p["kw"]), p["name"]
    v = n % 5
    opts = [f"{K}: The {N} Parents Love",
            f"{K} (School Psychologist Pick): {N}",
            f"{K}: {N}" if K.lower().startswith("best") else f"Best {K}: {N}",
            f"{K}: Why the {N} Works",
            f"{K} Idea: {N}"]
    t = opts[v]
    if len(t) > 100: t = f"{K}: {N}"
    if len(t) > 100: t = t[:100]
    alt_kw = " and ".join(p["others"]) if p["others"] else p["kw"]
    d = (f"{K}? As a Ph.D. school psychologist, the {N} is my top pick for {p['promise']}. "
         f"Great for {p['aud']}. Parents searching {alt_kw} love this one too. "
         f"Tap to shop it on Amazon and see today's price. {DISC}")
    if len(d) > 500:
        d = (f"{K}? As a Ph.D. school psychologist, the {N} is my top pick for {p['promise']}. Tap to shop it on Amazon. {DISC}")
    alt = (f"Pinterest graphic with the headline '{K}' and a simple illustration of {dict(routine='a checklist chart', timer='a visual timer', sensory='a sensory bin full of colorful balls', screenfree='a crossed-out screen with toy blocks', calm='a heart with soft circles', active='foam play shapes and a ball', gifts='a wrapped gift box', travel='a family car', montessori='a wooden rainbow stacker', outdoor='a sprouting plant and sun')[p['icon']]}. "
           f"Text recommends the {N} for {p['promise']}, picked by Dr. Q, a school psychologist.")
    p.update(title=t, desc=d, alt=alt[:500], link=f"https://www.amazon.com/dp/{p['asin']}?tag={TAG}",
             headline=K, keywords=", ".join(dict.fromkeys([p["kw"]] + p["others"])), variant=v)
    assert len(t) <= 100 and len(d) <= 500

# ---- schedule: 5/day, Nov 1-30, no repeat board in a day ----
SLOTS = [("8:00 AM", 14, 0), ("11:00 AM", 17, 0), ("3:00 PM", 21, 0), ("6:00 PM", 0, 1), ("9:00 PM", 3, 1)]  # Central (UTC-6) -> UTC hour, +day
queue = sorted(pins, key=lambda p: (p["tier"], p["rep"], p["post"], p["idx"]))
start = dt.date(2026, 11, 1)
scheduled = []
for d in range(30):
    day_boards, today = set(), []
    for _ in range(5):
        pick = next((q for q in queue if q["bkey"] not in day_boards and q["post"] not in {t["post"] for t in today}), queue[0])
        queue.remove(pick); day_boards.add(pick["bkey"]); today.append(pick)
    for s, (label, uh, plus) in enumerate(SLOTS):
        p = today[s]
        local = start + dt.timedelta(days=d)
        utc = dt.datetime(local.year, local.month, local.day, uh) + dt.timedelta(days=plus)
        p.update(seq=d * 5 + s + 1, local_date=local.isoformat(), local_time=label, publish=utc.strftime("%Y-%m-%dT%H:%M:%S"))
        p["file"] = f"pin{p['seq']:03d}-{re.sub(r'[^a-z0-9]+','-',p['kw'].lower()).strip('-')}.png"
        scheduled.append(p)
assert not queue and len(scheduled) == 150
json.dump(scheduled, open("/home/claude/pins150.json", "w"), indent=1)
print("ok", max(len(p["title"]) for p in scheduled), max(len(p["desc"]) for p in scheduled))
for p in scheduled[:10]: print(p["seq"], p["local_date"], p["local_time"], p["board"][:20], "|", p["title"])
