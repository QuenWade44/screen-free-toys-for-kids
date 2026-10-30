# Query list used for the $100+ exhaustive scan (same order as the browser loop), with category tags.
QX = ["pitching machine","softball pitching machine","batting cage","baseball hitting net","batting tee","pitching net","baseball rebounder","radar gun baseball","baseball bat usa youth","usssa baseball bat","bbcor bat","fastpitch softball bat","slowpitch softball bat","baseball glove","softball glove","catchers mitt","catchers gear set","baseball bat bag wheeled","softball bat bag","baseball cleats","softball cleats","batting helmet","baseball training aid","hitting trainer swing","basketball hoop portable","basketball hoop in ground","basketball rebounder return","basketball shooting machine","basketball shoes kids","basketball arcade game","soccer goal","soccer rebounder","soccer cleats","soccer training equipment","soccer goal portable large","football tackling dummy","football kicking net","football helmet youth","football shoulder pads youth","football cleats","volleyball net system","volleyball training equipment","volleyball shoes","volleyball rebounder","hockey skates","hockey stick","hockey goal","hockey bag","hockey shooting pad","hockey training","lacrosse stick","lacrosse goal","lacrosse rebounder","lacrosse gloves","tennis racket","tennis ball machine","pickleball paddle","pickleball net","golf net","golf hitting mat","golf launch monitor","golf clubs junior","gymnastics bar","balance beam","gymnastics mat","air track","cheer shoes","cheer bag","wrestling shoes","swim parka","track spikes","running shoes kids","weighted vest","adjustable dumbbells","squat rack","plyo box","agility training","resistance sled","massage gun","compression boots recovery","cold plunge","foam roller vibrating","heated stadium seat","stadium chair","sideline chair","rocking camping chair","zero gravity chair","camping chair heated","wagon collapsible","stroller wagon","electric wagon","beach wagon","sports wagon","pop up canopy","canopy with sidewalls","shade tent","sun shelter","patio heater portable","propane heater portable","heated jacket","heated vest","heated blanket battery","heated gloves","heated socks","winter coat women","puffer jacket women","rain jacket women","snow boots women","ugg boots","hunter boots","cooler","rolling cooler","soft cooler","cooler backpack","yeti cooler","portable ice maker","water jug","power station","portable generator","bluetooth speaker","action camera","sports camera ai tracking","camera for sports photography","camera lens telephoto","gimbal stabilizer","tripod video","binoculars","apple watch","garmin watch","fitness tracker kids","airpods","noise cancelling headphones","ipad","portable grill","griddle","camping stove","blender","rooftop cargo carrier","hitch cargo carrier","trunk organizer","garage storage system","sports equipment storage","ball cart","shoe rack","backpack sports","duffel bag","rolling duffel","tote bag women","crossbody bag","sunglasses polarized","sneakers women","first aid kit","golf cart","scooter electric teen"]

def tag(q):
    """(group, sport, board_key) for a query."""
    ql = q.lower()
    for sport in ["softball", "baseball", "basketball", "soccer", "football", "volleyball", "hockey", "lacrosse",
                  "tennis", "pickleball", "golf", "gymnastics", "cheer", "wrestling", "swim", "track"]:
        if sport in ql:
            break
    else:
        sport = ""
    if any(w in ql for w in ["pitching", "batting", "hitting", "rebounder", "radar", "training", "tee", "net", "goal",
                              "hoop", "shooting", "tackling", "kicking", "machine", "gymnastics", "balance beam",
                              "air track", "agility", "sled", "plyo", "squat", "dumbbell", "weighted", "launch monitor",
                              "pad", "cage", "mat"]):
        return ("Backyard & home training", sport or ("baseball" if "batting" in ql or "pitching" in ql else ""), "train")
    if any(w in ql for w in ["bat", "glove", "mitt", "catchers gear", "cleats", "helmet", "shoulder pads", "skates",
                              "stick", "racket", "paddle", "clubs", "spikes", "shoes", "parka"]) and "bag" not in ql:
        return ("Player gear (gift-worthy)", sport, "gifts")
    if any(w in ql for w in ["massage", "compression", "cold plunge", "foam roller"]):
        return ("Recovery", "", "gifts")
    if any(w in ql for w in ["heated stadium", "stadium chair", "sideline chair", "rocking", "zero gravity", "camping chair"]):
        return ("Seats & chairs", "", "seat")
    if "wagon" in ql:
        return ("Wagons", "", "wagon")
    if any(w in ql for w in ["canopy", "shade", "shelter"]):
        return ("Canopies & shade", "", "travel")
    if any(w in ql for w in ["heater", "heated", "winter", "puffer", "snow", "ugg"]):
        return ("Cold-weather gear", "", "cold")
    if any(w in ql for w in ["rain", "hunter"]):
        return ("Rain gear", "", "bag")
    if any(w in ql for w in ["cooler", "ice maker", "water jug"]):
        return ("Coolers & drinks", "", "travel")
    if any(w in ql for w in ["power station", "generator", "speaker", "grill", "griddle", "stove", "blender"]):
        return ("Tailgate & power", "", "dad")
    if any(w in ql for w in ["camera", "lens", "gimbal", "tripod", "binoculars"]):
        return ("Filming the game", "", "gifts")
    if any(w in ql for w in ["watch", "fitness tracker", "airpods", "headphones", "ipad"]):
        return ("Tech gifts", "", "gifts")
    if any(w in ql for w in ["cargo", "trunk", "garage", "storage", "ball cart", "shoe rack"]):
        return ("Car & garage storage", "", "store")
    if any(w in ql for w in ["bag", "backpack", "duffel", "tote", "crossbody"]):
        return ("Bags", sport, "gameday")
    if any(w in ql for w in ["sunglasses", "sneakers"]):
        return ("Mom style", "", "gifts")
    if "first aid" in ql:
        return ("Team mom & coach", "", "coach")
    return ("Other / stretch", "", "gifts")
