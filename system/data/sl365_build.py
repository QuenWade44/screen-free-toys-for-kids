"""Sideline Ready 365: one anchor product per day (Dec 1 2026 - Nov 30 2027),
exact Pinterest search phrases, pin metadata drafts and a $100+ Amazon bundle per post."""
import re, random, datetime as dt, json, sys
sys.path.insert(0, "/home/claude")
from sl_data import P as P1, BOARDS
from sl_data2 import P2
from sl_data3 import P3

TAG = "screenfreet0f-20"
BOARD_NAMES = {k: n for k, n, _ in BOARDS}
BOARD_NAMES["train"] = "Backyard Sports Training Equipment"
BOARD_NAMES["store"] = "Sports Equipment Storage & Garage Organization"
BOARD_NAMES["fuel"] = "Teen Athlete Meals, Snacks & Meal Prep"
NEW_BOARDS = {
 "train": "Backyard sports training equipment for young athletes: pitching machines, batting cages, hitting nets, batting tees, basketball hoops, soccer goals, rebounders and volleyball training equipment at home. Contains affiliate links.",
 "fuel": "Teen athlete meals, teen athlete snacks, athlete meal prep and travel ball food ideas: blenders, shaker bottles, lunch boxes, meal prep containers and grab-and-go snacks for busy sports families. Contains affiliate links.",
 "store": "Sports equipment storage ideas for the garage, mudroom and car: ball storage racks, garage sports organization, trunk organizers and sports bag storage. Contains affiliate links.",
}

def price(p):
    return float(re.sub(r"[^\d.]", "", p) or 0) if isinstance(p, str) else float(p)

def norm(rec, src):
    if src == 1:
        a, n, pr, r, nr, b, t, kws = rec
        from sl_data import board_for
        bd = board_for(kws[0])
    else:
        a, n, pr, r, nr, b, t, kws, bd = rec
    return dict(asin=a, name=n, price=price(pr), rating=float(r), ratings=nr, bought=b, tier=t,
                kws=list(kws), board=bd, src={1: "Nov 2026 list", 2: "Oct 30 list", 3: "New (365 build)"}[src])

EXCLUDE = {"B0BMQ85B31"}  # bobby pins: too small to anchor a post
PROD = [p for p in [norm(r, 1) for r in P1] + [norm(r, 2) for r in P2] + [norm(r, 3) for r in P3] if p["asin"] not in EXCLUDE]
SPORTS = ["baseball", "softball", "soccer", "football", "basketball", "volleyball", "hockey", "cheer",
          "track", "wrestling", "swim", "lacrosse", "gymnastics", "tumbling", "golf", "pickleball", "tee ball", "batting", "pitching", "catcher"]
SPORT_ALIAS = {"tumbling": "gymnastics", "batting": "baseball", "pitching": "baseball", "catcher": "baseball", "tee ball": "baseball"}
def sports_of(p):
    txt = (" ".join(p["kws"]) + " " + p["name"]).lower()
    s = {SPORT_ALIAS.get(w, w) for w in SPORTS if w in txt}
    if "baseball" in s or "softball" in s:
        s |= {"baseball", "softball"}
    return s
THEMES = [
 ("cold", ["cold", "winter", "hockey", "blanket", "fall ", "heated", "hand warmer"]),
 ("hot", ["summer", "hot ", "florida", "spring", "cooling", "fan"]),
 ("travel", ["travel", "tournament", "tailgate", "cooler", "wagon", "pop up tent", "canopy"]),
 ("team", ["team mom", "coach", "team snack", "snacks", "concession", "party", "end of season", "team gift", "first aid", "team player"]),
 ("practice", ["training", "batting", "pitching", "hitting", "backyard", "agility", "speed", "rebounder", "catchers gear", "drills"]),
 ("storage", ["storage", "garage", "organization", "trunk"]),
 ("film", ["filming", "camera", "photography", "tripod"]),
 ("bag", ["bag", "must haves", "essentials", "hacks", "laundry", "stain", "smell", "cleat"]),
 ("seat", ["stadium seat", "bleacher", "chair", "seat cushion"]),
 ("fuel", ["teen athlete", "meal", "breakfast", "lunch", "protein", "blender", "food"]),
 ("recovery", ["recovery", "athlete gifts", "massage", "foam roller", "kinesiology"]),
]
TYPES = ["golf net","gymnastics","balance beam","tumbling","exercise mat","dumbbell","griddle","grill","stove","pitching machine","batting cage","batting tee","practice net","rebounder","hoop","soccer goal","pop up soccer","agility ladder",
 "tackling dummy","volleyball training","camera","tripod","power station","cooler","wagon","canopy","shade","heater","heated jacket","heated vest",
 "heated stadium seat","stadium seat","heated socks","heated gloves","hand warmer","blanket","boot","fleece","jacket","chair","massage gun","theragun",
 "foam roller","first aid","sunscreen","umbrella","fan","tote","backpack","duffel","bag","water bottle","jug","catcher","glove","soccer ball","basketball",
 "volleyball","football","trunk organizer","storage","ball cart","socks","leggings","vest","whistle","clipboard","pump","cones","pinnies","speed gun","radar"]
def type_of(p):
    n = p["name"].lower()
    for t in TYPES:
        if t in n:
            return t
    return n.split()[-1]
def gift_targets(phrase):
    k = phrase.lower()
    if not any(w in k for w in ("gift", "christmas", "stocking")):
        return set()
    if "mom" in k or "mother" in k:
        return {"gift_mom"}
    if "dad" in k or "father" in k or "for men" in k:
        return {"gift_dad"}
    if "coach" in k:
        return {"gift_coach"}
    if "team" in k or "end of season" in k:
        return {"gift_team"}
    return {"gift_kid"}
def themes_of(p, primary=False):
    phrases = p["kws"][:1] if primary else p["kws"]
    txt = (" ".join(phrases) + " " + p["name"]).lower() + " "
    out = {t for t, ws in THEMES if any(w in txt for w in ws)}
    for ph in phrases:
        out |= gift_targets(ph)
    return out
for p in PROD:
    p["sports"] = sports_of(p)
    p["themes"] = themes_of(p)
    p["pthemes"] = themes_of(p, True) or p["themes"]
    p["type"] = type_of(p)

# ---------- calendar ----------
start = dt.date(2026, 12, 1)
days = [start + dt.timedelta(i) for i in range(365)]
def season(d):
    return "winter" if d.month in (11, 12, 1, 2) else "summer" if 3 <= d.month <= 8 else "fall"

random.seed(365)
pool = {1: [p for p in PROD if p["tier"] == 1], 2: [p for p in PROD if p["tier"] == 2], 3: [p for p in PROD if p["tier"] == 3]}
for t in pool:
    random.shuffle(pool[t])
# gifts and big-ticket items first in December (shipping before Christmas)
pool[1].sort(key=lambda p: (0 if p["board"] in ("gifts", "train", "dad") else 1, -p["price"]))

def pick(prefs, recent):
    for t in prefs:
        for i, p in enumerate(pool[t]):
            if p["board"] not in recent:
                return pool[t].pop(i)
    for t in prefs:
        if pool[t]:
            return pool[t].pop(0)
    for t in (1, 2, 3):
        if pool[t]:
            return pool[t].pop(0)

sched = []
recent = []
# reserve: count slots per season so tier-2 is spread rather than used up early
for d in days:
    s = season(d)
    if s == "winter":
        prefs = (1, 2) if d.month in (12, 1) or d.month == 11 else (1, 2, 3)
    elif s == "summer":
        prefs = (3, 2)
    else:
        prefs = (2, 1, 3) if d.month == 9 else (1, 2)
    # mix: every 3rd day use tier 2 so year-round items spread across the year
    if d.toordinal() % 3 == 0:
        prefs = (2,) + tuple(x for x in prefs if x != 2)
    p = pick(prefs, recent[-2:])
    if p is None:
        break
    sched.append((d, p))
    recent.append(p["board"])

# ---------- bundles ----------
RELATED = {
 "train": ["train", "gifts", "bag", "coach", "store"], "cold": ["cold", "seat", "gameday", "bag"],
 "seat": ["seat", "cold", "gameday", "bag"], "hot": ["hot", "bag", "travel", "wagon"],
 "travel": ["travel", "wagon", "bag", "hot", "seat"], "wagon": ["wagon", "travel", "bag", "hot", "seat"],
 "gifts": ["gifts", "train", "cold", "dad"], "coach": ["coach", "bag", "train", "travel"],
 "dad": ["dad", "travel", "seat", "cold"], "gameday": ["gameday", "bag", "seat", "cold"],
 "bag": ["bag", "gameday", "travel", "hot"], "fuel": ["fuel", "travel", "coach", "bag"], "store": ["store", "train", "bag", "travel"],
}
def season_ok(anchor_season, q):
    if anchor_season == "winter":
        return q["tier"] in (1, 2)
    if anchor_season == "summer":
        return q["tier"] in (2, 3)
    return q["tier"] in (1, 2)

def bundle(d, a, used_counts):
    s = season(d)
    rng = random.Random(d.toordinal())
    def gather(level):
        out = []
        for q in PROD:
            if q["asin"] == a["asin"] or not season_ok(s, q) or q["type"] == a["type"]:
                continue
            if a["sports"] and q["sports"] and not (a["sports"] & q["sports"]):
                continue
            if level == 0:
                shared = a["pthemes"] & q["themes"]
            elif level == 1:
                shared = a["themes"] & q["themes"]
            else:
                shared = {"board"} if q["board"] in RELATED[a["board"]] else set()
            if not shared:
                continue
            sc = 2 * len(shared) + (3 if (a["sports"] & q["sports"]) else 0) + (1 if q["board"] != a["board"] else 0)
            sc -= used_counts.get(q["asin"], 0) * 1.2
            sc += rng.random()
            out.append((sc, q))
        out.sort(key=lambda x: -x[0])
        return out
    n_extra = 4 if a["price"] >= 300 else 5
    picked, per_board, types = [], {}, set()
    cands = []
    for level in (0, 1, 2):
        lv = gather(level)
        cands += [c for c in lv if c[1] not in [x[1] for x in cands]]
        for _, q in lv:
            if len(picked) == n_extra:
                break
            if q in picked or per_board.get(q["board"], 0) >= 2 or q["type"] in types:
                continue
            picked.append(q); types.add(q["type"]); per_board[q["board"]] = per_board.get(q["board"], 0) + 1
        total = a["price"] + sum(q["price"] for q in picked)
        if len(picked) == n_extra and total >= 100:
            break
        # lift to $100+ using the best-matching pricier items found so far
        top = cands[: max(12, len(cands) // 3)]
        pricier = [q for _, q in top if q not in picked and q["price"] >= 25 and q["type"] not in types]
        while total < 100 and pricier and picked:
            cheap = min(picked, key=lambda q: q["price"])
            better = [q for q in pricier if q["price"] > cheap["price"] + 10]
            if not better:
                break
            best = better[0]
            picked.remove(cheap); picked.append(best); pricier.remove(best)
            types.discard(cheap["type"]); types.add(best["type"])
            pricier = [q for q in pricier if q["type"] not in types]
            total = a["price"] + sum(q["price"] for q in picked)
        if len(picked) == n_extra and total >= 100:
            break
    for q in picked:
        used_counts[q["asin"]] = used_counts.get(q["asin"], 0) + 1
    return picked, round(a["price"] + sum(q["price"] for q in picked), 2)

# ---------- copy ----------
def tc(s):
    small = {"for", "and", "of", "to", "a", "the", "in", "on", "vs", "with"}
    w = s.split()
    return " ".join(x if (i and x in small) else x[:1].upper() + x[1:] for i, x in enumerate(w))

HOOK = {
 "train": "the practice gear that gets real reps in at home between practices",
 "cold": "so you stay warm from kickoff to the final whistle on cold bleachers",
 "seat": "so your back makes it through back-to-back games on hard bleachers",
 "hot": "for hot ball fields and long summer tournament days",
 "travel": "for long tournament weekends away from home",
 "wagon": "to haul chairs, coolers and gear from the parking lot in one trip",
 "gifts": "a gift young athletes can use all season",
 "coach": "to make team mom and coach duties easier",
 "dad": "a sports dad pick for long game days",
 "gameday": "to make game day easier (and louder)",
 "bag": "a small item that earns its spot in the sports mom bag",
 "store": "to get cleats, bats and balls off the garage floor",
 "fuel": "to keep a hungry athlete fueled between school, practice and games",
}
CONTEXT = {
 "train": "home practice setup", "cold": "cold game day kit", "seat": "bleacher comfort kit",
 "hot": "hot weather sideline kit", "travel": "tournament weekend kit", "wagon": "sports wagon setup",
 "gifts": "gift bundle", "coach": "team mom and coach kit", "dad": "sports dad setup",
 "gameday": "game day bag", "bag": "sports mom bag", "store": "gear storage setup", "fuel": "athlete fuel kit",
}
def short(n, k=38):
    n = re.sub(r"\s*\(.*?\)", "", n)
    if len(n) > k:
        n = n[:k].rsplit(" ", 1)[0]
    return re.sub(r"\s+(&|with|and|for|of|the|a)$", "", n.strip(" ,-"))

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]

rows, used = [], {}
for i, (d, a) in enumerate(sched, 1):
    extra, total = bundle(d, a, used)
    k1, k2, k3 = a["kws"][:3]
    n_items = 1 + len(extra)
    title = f"{tc(k1)}: {short(a['name'])} + {n_items-1} More"
    if len(title) > 100:
        title = f"{tc(k1)}: {short(a['name'], 30)} + {n_items-1} More"
    names = ", ".join(short(q["name"], 30) for q in extra[:3])
    desc = (f"{k1[:1].upper()+k1[1:]}: start with the {short(a['name'])}, {HOOK[a['board']]}. "
            f"This {n_items}-item {CONTEXT[a['board']]} adds {names} and more, all on Amazon. "
            f"Also for anyone searching {k2} or {k3}. As an Amazon Associate I earn from qualifying purchases.")
    if len(desc) > 500:
        desc = desc[:497].rsplit(" ", 1)[0] + "..."
    alt = (f"Pin graphic for {k1}: the {short(a['name'])} shown with {names}, "
           f"a {n_items}-item {CONTEXT[a['board']]} from Sideline Ready.")
    post = f"{tc(k1)}: The {n_items}-Item {tc(CONTEXT[a['board']])} Built Around the {short(a['name'], 34)}"
    rows.append(dict(
        day=i, date=d.isoformat(), month=d.strftime("%b %Y"), season=season(d).title(),
        product=a["name"], price=a["price"], rating=a["rating"], ratings=a["ratings"], bought=a["bought"],
        phrase1=k1, phrase2=k2, phrase3=k3, board=BOARD_NAMES[a["board"]], board_key=a["board"],
        pin_title=title, pin_desc=desc, alt=alt, post_title=post, slug=slugify(f"{k1} {short(a['name'], 30)}"),
        bundle=" | ".join(f"{q['name']} (${q['price']:.2f})" for q in extra),
        bundle_asins=",".join([a["asin"]] + [q["asin"] for q in extra]),
        items=n_items, cart_total=total, asin=a["asin"],
        link=f"https://www.amazon.com/dp/{a['asin']}?tag={TAG}",
        cart_link="https://www.amazon.com/gp/aws/cart/add.html?AssociateTag=" + TAG + "".join(
            f"&ASIN.{j}={x}&Quantity.{j}=1" for j, x in enumerate([a["asin"]] + [q["asin"] for q in extra], 1)),
        source=a["src"]))

if __name__ == "__main__":
    print(len(PROD), len(rows))
    from collections import Counter
    print(Counter(r["season"] for r in rows), Counter(p["tier"] for p in PROD))
    print("min cart", min(r["cart_total"] for r in rows), "max", max(r["cart_total"] for r in rows))
    print("under 100:", sum(r["cart_total"] < 100 for r in rows))
    print(max(len(r["pin_title"]) for r in rows), max(len(r["pin_desc"]) for r in rows))
    for r in rows[::37]:
        print(r["date"], r["product"], "|", r["phrase1"], "\n   ->", r["bundle"], r["cart_total"])
