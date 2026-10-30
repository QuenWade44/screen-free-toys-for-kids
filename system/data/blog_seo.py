"""SEO blog titles, meta descriptions and customer-journey fields for the 365 Sideline Ready posts."""
import re, sys
sys.path.insert(0, "/home/claude")
from sl365_build import rows, PROD, tc, short, CONTEXT
from blog_desc import DESC

P = {p["asin"]: p for p in PROD}

def cls(kw):
    k = kw.lower()
    if k.startswith("how to") or any(w in k for w in ("hack", "fix", "solution", "smell", "stain")):
        return "howto"
    if any(w in k for w in ("gift", "christmas", "stocking", "party favors", "end of season")):
        return "gift"
    if any(w in k for w in ("snack", "food", "meal", "cocoa", "breakfast", "lunch", "nutrition", "concession", "recipes")):
        return "food"
    if any(w in k for w in ("storage", "organization", "organizer")):
        return "storage"
    if any(w in k for w in ("fits", "outfit", "what to wear")):
        return "outfit"
    if any(w in k for w in ("cold", "winter", "hockey mom", "blanket")):
        return "cold"
    if any(w in k for w in ("summer", "hot ", "florida", "cooling")):
        return "hot"
    if any(w in k for w in ("filming", "camera", "photography")):
        return "film"
    if any(w in k for w in ("training", "drills", "equipment", "batting", "pitching", "hitting", "rebounder", "agility",
                            "speed", "backyard", "home gym", "garage gym", "kip", "balance beam", "tumbling", "catchers gear",
                            "gymnastics", "physique", "workout", "exercises")):
        return "train"
    if any(w in k for w in ("team mom", "coach", "duties")):
        return "team"
    if any(w in k for w in ("must haves", "essentials", "packing list", "checklist", "bag")):
        return "list"
    if "ideas" in k or "setup" in k:
        return "ideas"
    return "buy"

STAGE = {  # where the mom is in her journey when she types this
 "howto": ("Problem", "Informational", "How-to"),
 "cold": ("Problem", "Informational", "Survival guide"),
 "hot": ("Problem", "Informational", "Survival guide"),
 "outfit": ("Problem", "Informational", "What to wear"),
 "food": ("Planning", "Informational", "Ideas list"),
 "ideas": ("Planning", "Informational", "Ideas list"),
 "team": ("Planning", "Commercial", "Checklist"),
 "list": ("Planning", "Commercial", "Checklist"),
 "train": ("Comparing", "Commercial", "Setup guide"),
 "storage": ("Comparing", "Commercial", "Setup guide"),
 "film": ("Comparing", "Commercial", "Setup guide"),
 "buy": ("Comparing", "Commercial", "Buying guide"),
 "gift": ("Ready to buy", "Transactional", "Gift guide"),
}

def desc_of(p):
    return DESC[p["asin"]]

def art(d):
    """'a hoop', 'an AirTag', 'AirPods 5' (plural / brand-plural gets no article)."""
    if "AirPods" in d or "UGG" in d.split()[0]:
        return d
    w = d.split()[-1]
    if (w.endswith("s") and not w.endswith("ss")) or w[0].isdigit() and len(d.split()) == 1:
        return d
    if d.split()[0][0].isdigit():
        return "a " + d
    return ("an " if d[0].lower() in "aeiou" else "a ") + d

def item_names(asins, k=2):
    return [DESC[a] for a in asins[:k]]

used_primary = set()
used_titles = set()
out = []
for r in rows:
    a = P[r["asin"]]
    kws = [r["phrase1"], r["phrase2"], r["phrase3"]]
    month = int(r["date"][5:7])
    def fits_season(k):
        k = k.lower()
        if any(w in k for w in ("christmas", "stocking")) and month not in (11, 12):
            return False
        if any(w in k for w in ("winter", "cold ", "cold football")) and month in (4, 5, 6, 7, 8):
            return False
        if any(w in k for w in ("summer", "spring")) and month in (11, 12, 1):
            return False
        return True
    ordered = [k for k in kws if fits_season(k)] + [k for k in kws if not fits_season(k)]
    primary = next((k for k in ordered if k not in used_primary and fits_season(k)), None)
    if primary is None:
        primary = next((k for k in ordered if k not in used_primary), None)
    long_tail = False
    if primary is None:
        primary = ordered[0]
        long_tail = True
    if not fits_season(primary) and "christmas" in primary:
        primary = re.sub(r"\s*christmas\s*", " ", primary).strip()
    used_primary.add(primary)
    secondary = [k for k in kws if k != primary]
    c = cls(primary)
    stage, intent, ptype = STAGE[c]
    KW = tc(primary)
    d = desc_of(a)
    D = " ".join(x[:1].upper() + x[1:] if x.islower() else x for x in d.split())
    n = r["items"]
    adds = r["bundle_asins"].split(",")[1:]
    i1, i2 = (item_names(adds) + ["", ""])[:2]
    total = r["cart_total"]
    v = r["day"] % 3  # rotate wording so titles don't all read the same

    if c == "gift":
        titles = [f"{KW}: {n} Ideas, Starting With {art(D)}", f"{KW}: The {D} Gift Bundle", f"{KW}: {n} Picks They'll Use All Season"]
        h1 = f"{KW}: A {n}-Item Gift Bundle Built Around the {D}"
        meta = f"{primary[:1].upper()+primary[1:]}: start with the {d}, then add the {i1} and {i2}. A {n}-item gift bundle you can add to your cart in one click."
        kl = primary.lower()
        if "christmas" in kl or "stocking" in kl:
            hook = f"It's December, the list is long, and you want a gift that gets used after the wrapping paper is gone. Start with the {d}."
        elif "birthday" in kl:
            hook = f"The birthday is coming up and they already have a closet full of stuff. Here's a gift they'll use at practice, starting with the {d}."
        elif "team" in kl or "end of season" in kl or "senior" in kl:
            hook = f"The season is wrapping up and you need something for the whole team. Here's the plan, starting with the {d}."
        elif "mom" in kl or "mother" in kl:
            hook = f"She spends every weekend in the bleachers. Here's a gift that makes those weekends easier, starting with the {d}."
        elif "dad" in kl or "coach" in kl or "men" in kl:
            hook = f"He's at every practice and every game. Here's a gift he'll actually reach for, starting with the {d}."
        else:
            hook = f"You want a gift they'll use, not another thing in the closet. Start with the {d}."
    elif c == "howto":
        titles = [f"{KW} (What Actually Helps)", f"{KW}: Step-by-Step + Supply List", f"{KW}: The Easy Way"]
        h1 = f"{KW}: Step-by-Step, Plus the {n} Supplies to Keep on Hand"
        meta = f"{primary[:1].upper()+primary[1:]}: a simple step-by-step plan, plus the {n} supplies that make it easier, starting with the {d}."
        hook = f"Another game, another mess. Here's the routine that fixes it, and the {d} that does most of the work."
    elif c == "cold":
        titles = [f"{KW}: How to Stay Warm in the Bleachers", f"{KW}: The Warm-Bleacher Checklist", f"{KW}: {n} Things to Bring"]
        h1 = f"{KW}: How to Stay Warm From Kickoff to Final Whistle"
        meta = f"{primary[:1].upper()+primary[1:]}: how to stay warm on cold bleachers, plus a {n}-item kit starting with the {d}. Add the whole kit to your cart in one click."
        hook = f"Third quarter, 34 degrees, and the bleachers are metal. Here's how to stay warm, starting with the {d}."
    elif c == "hot":
        titles = [f"{KW}: How to Beat the Heat at the Field", f"{KW}: The Hot-Field Checklist", f"{KW}: {n} Things That Keep You Cool"]
        h1 = f"{KW}: How to Stay Cool Through Doubleheaders and Tournament Days"
        meta = f"{primary[:1].upper()+primary[1:]}: how to stay cool at hot ball fields, plus a {n}-item kit starting with the {d}. Add it all to your cart in one click."
        hook = f"It's 95 degrees, game two starts in 20 minutes, and there's no shade. Here's what to bring, starting with the {d}."
    elif c == "outfit":
        titles = [f"{KW}: What to Wear to Stay Warm", f"{KW}: Layer-by-Layer Guide", f"{KW}: Warm, Easy Game Day Layers"]
        h1 = f"{KW}: What to Wear (Layer by Layer) for Long Games"
        meta = f"{primary[:1].upper()+primary[1:]}: a layer-by-layer guide for long games, starting with the {d}, plus the {i1} and {i2}."
        hook = f"You can be cute or you can be warm, unless you layer it right. Here's the plan, starting with the {d}."
    elif c == "food":
        titles = [f"{KW}: Easy Ideas for Busy Game Days", f"{KW}: Grab-and-Go Ideas + Supply List", f"{KW}: What to Pack for Long Days"]
        h1 = f"{KW}: Easy Ideas, Plus the {n} Supplies That Make It Simple"
        meta = f"{primary[:1].upper()+primary[1:]}: easy ideas for practice and game days, plus a {n}-item kit starting with the {d}. One-click add to cart."
        hook = f"Practice ends at 7, there's a game at 8 a.m., and everyone is starving. Here's the plan, starting with the {d}."
    elif c == "storage":
        titles = [f"{KW}: Get the Gear Off the Floor", f"{KW}: A Simple Setup That Works", f"{KW} on a Weekend Budget"]
        h1 = f"{KW}: A Simple Setup for Balls, Bats, Bags and Cleats"
        meta = f"{primary[:1].upper()+primary[1:]}: a simple setup for balls, bats, bags and cleats, built around the {d}. See the {n}-item setup."
        hook = f"If you've tripped over a bat bag in your own garage this week, this one's for you. It starts with the {d}."
    elif c == "film":
        titles = [f"{KW}: How to Film Your Kid's Games", f"{KW}: Easy Setup for Sports Parents", f"{KW}: What You Need to Start"]
        h1 = f"{KW}: How to Film Your Kid's Games Without Missing the Moment"
        meta = f"{primary[:1].upper()+primary[1:]}: how to film your kid's games without missing the moment, plus a {n}-item setup built around the {d}."
        hook = f"You want the highlight and you want to actually watch the game. Here's the setup, built around the {d}."
    elif c == "train":
        titles = [f"{KW}: Build a Home Setup Around {art(D)}", f"{KW}: What to Buy for Practice at Home", f"{KW}: {n}-Piece Home Practice Setup"]
        h1 = f"{KW}: A Home Practice Setup Built Around the {D}"
        meta = f"{primary[:1].upper()+primary[1:]}: how to set up practice at home, starting with the {d}, plus the {i1} and {i2}. See the full {n}-piece setup."
        hook = f"Practice is twice a week, but the reps happen at home. Here's the setup, starting with the {d}."
    elif c == "team":
        titles = [f"{KW}: The Season Checklist", f"{KW}: What to Buy and Bring", f"{KW}: Your Easy Season Plan"]
        h1 = f"{KW}: A Season Checklist, Plus the {n} Supplies to Buy Once"
        meta = f"{primary[:1].upper()+primary[1:]}: a simple season checklist and the {n} supplies to buy once, starting with the {d}."
        hook = f"You said yes to team mom (or coach). Here's the checklist, starting with the {d}."
    elif c == "list":
        titles = [f"{KW}: {n}-Item Checklist", f"{KW}: What to Pack (Printable List)", f"{KW}: The No-Forget Packing List"]
        h1 = f"{KW}: The {n}-Item List, Starting With the {D}"
        meta = f"{primary[:1].upper()+primary[1:]}: a {n}-item checklist for long game days, starting with the {d}, plus the {i1} and {i2}. One-click add to cart."
        hook = f"You're halfway to the field when you realize what you forgot. Here's the list, starting with the {d}."
    elif c == "ideas":
        titles = [f"{KW}: Simple Setup + What to Buy", f"{KW}: {n} Things to Start With", f"{KW}: An Easy Plan That Works"]
        h1 = f"{KW}: A Simple Setup Built Around the {D}"
        meta = f"{primary[:1].upper()+primary[1:]}: simple ideas and the {n} things to start with, built around the {d}. See the full list."
        hook = f"You've saved 40 pins about this. Here's the simple version, built around the {d}."
    else:  # buy
        titles = [f"{KW}: What to Look For (+ {n}-Item Kit)", f"{KW}: How to Choose + Our Pick", f"{KW}: A Simple Buying Guide"]
        h1 = f"{KW}: What to Look For, and the {D} Kit"
        meta = f"{primary[:1].upper()+primary[1:]}: what to look for, why the {d} fits, and the {n}-item kit to go with it. One-click add to cart."
        hook = f"There are a hundred options and you need one that works this weekend. Here's how to choose, and the {d} kit."

    titles = [t for t in titles if not (d.lower() in primary.lower() or primary.lower() in d.lower()) or "Around" not in t] or titles
    title = titles[v % len(titles)]
    if title in used_titles:
        title = f"{KW}: Start With {art(D)}"
    used_titles.add(title)
    if long_tail:
        # this keyword already has a post; make this one a distinct long-tail angle
        title = f"{KW}: Start With {art(D)}"
        h1 = f"{KW}: Why We Start With {art(D)}, Plus {n-1} Add-Ons"
    if len(title) > 60:
        for t in titles + [f"{KW}: {n}-Item Kit", f"{KW}"]:
            if len(t) <= 60:
                title = t
                break
        else:
            title = KW[:60]
    if len(meta) > 155:
        meta = re.sub(r",? (then add|plus) [^.]*? and [^.]*?(\.|,)", r"\2", meta)
    if len(meta) > 155:
        meta = re.sub(r" (One-click add to cart\.|Add (the whole kit|it all) to your cart in one click\.|See the full .*?\.)$", "", meta)
    if len(meta) > 155:
        meta = meta[:152].rsplit(" ", 1)[0].rstrip(",") + "..."
    slug = re.sub(r"[^a-z0-9]+", "-", (primary + " " + d).lower()).strip("-")[:75].rstrip("-")
    pin_title = h1 if len(h1) <= 100 else title
    ctx = CONTEXT[a["board"]]
    pin_desc = (f"{primary[:1].upper()+primary[1:]}: {hook} The full {n}-item {ctx} adds the {i1} and {i2}, "
                f"with one-click add to cart. Also helpful if you're searching {secondary[0]} or {secondary[1]}. As an Amazon Associate I earn from qualifying purchases.")
    if len(pin_desc) > 500:
        pin_desc = pin_desc[:497].rsplit(" ", 1)[0] + "..."
    alt = f"Pin for {primary}: the {d} with the {i1} and {i2}, part of a {n}-item {ctx} from Sideline Ready."
    cta = f"Shop the full {n}-item {CONTEXT[a['board']]} (about ${total:,.0f}) - add everything to your Amazon cart in one click."
    out.append(dict(asin=r["asin"], day=r["day"], date=r["date"], product=r["product"], primary=primary,
                    secondary="; ".join(secondary), stage=stage, intent=intent, ptype=ptype,
                    seo_title=title, h1=h1, meta=meta, slug=slug, hook=hook, cta=cta, long_tail=long_tail, pin_title=pin_title, pin_desc=pin_desc, alt=alt))

# final pass: no two posts share an SEO title
from collections import Counter as _C
_seen = set()
for o in out:
    if o["seo_title"] in _seen:
        D = " ".join(x[:1].upper() + x[1:] if x.islower() else x for x in DESC[P[o["asin"]]["asin"]].split()) if "asin" in o else ""
        alt_t = f"{tc(o['primary'])}: Start With {art(D)}"
        o["seo_title"] = alt_t if len(alt_t) <= 60 and alt_t not in _seen else f"{tc(o['primary'])}: The {D} Pick"[:60]
    _seen.add(o["seo_title"])

if __name__ == "__main__":
    from collections import Counter
    print(len(out), "dup titles:", sum(v > 1 for v in Counter(o["seo_title"] for o in out).values()),
          "dup slugs:", sum(v > 1 for v in Counter(o["slug"] for o in out).values()),
          "long-tail:", sum(o["long_tail"] for o in out))
    print("title len max", max(len(o["seo_title"]) for o in out), "meta max", max(len(o["meta"]) for o in out),
          "meta min", min(len(o["meta"]) for o in out))
    print(Counter(o["ptype"] for o in out))
    for o in out[::29]:
        print(f"\n{o['date']} [{o['ptype']}/{o['stage']}] {o['product'][:40]}\n  T: {o['seo_title']}\n  H1: {o['h1']}\n  M: {o['meta']}\n  hook: {o['hook']}")
