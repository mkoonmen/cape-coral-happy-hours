#!/usr/bin/env python3
"""Builds data/restaurants.json.
Inputs: scripts/state_license_extract.json (Cape Coral rows from Florida DBPR food-service license/inspection
records), EXTRA (licensed places missing from that extract + bars that hold no food license),
HH (researched happy hours, keyed by a lowercase name fragment + optional address fragment)."""
import json, re, sys, datetime
TODAY = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
raw = json.load(open('scripts/state_license_extract.json'))
rows = [(r['n'], r['a'], r['z'], r.get('p',''), r['ln'][:3]) for r in raw if r['ln'][:3] in ('SEA','NOS')]
EXTRA = [  # name, address, zip, phone, kind
 ("CUBATALY","2555 NE PINE ISLAND RD","","","NOS"),("EAST OF CHICAGO PIZZA","1306 SANTA BARBARA BLVD STE 7","","","SEA"),
 ("EL SITIO BAR RESTAURANT","924 DEL PRADO BLVD S","","","SEA"),("FIRST ROUND DRAFT SPORTS BAR & GRILLE","1217 DEL PRADO BLVD S","","","SEA"),
 ("GANDULES GRILL","303 NE 3RD ST","","","SEA"),("GINO'S PIZZERIA","3108 SANTA BARBARA BLVD 109","","","SEA"),
 ("GRADOS PIZZA","1242 SW PINE ISLAND RD STE 17","","","SEA"),("JESSIE JAYS OFF THE BONE BBQ","450 ANDALUSIA BLVD","","","NOS"),
 ("JET'S PIZZA","643 CAPE CORAL PKWY E STE F","","","SEA"),("LA NORTENITA II","1541 DEL PRADO BLVD N","","","SEA"),
 ("LE PETIT PASTRY AND TEA","2301 DEL PRADO BLVD S STE 620","","","SEA"),("LENNY'S GRILL & SUBS","2301 DEL PRADO BLVD #665","","","SEA"),
 ("MISTO BAR & GRILL","231 DEL PRADO BLVD S UNIT 1","","","SEA"),("MOE'S SOUTHWEST GRILL","1631 DEL PRADO BLVD STE 412","","","SEA"),
 ("NEW ENGLAND MOORINGS SEAFOOD RESTAURANT","1326 SE 16 PL","","","SEA"),("ON FIRE GRILL","1310 NE PINE ISLAND RD","","","NOS"),
 ("PAPA JOHN'S PIZZA","1338 DEL PRADO BLVD STE 1","","","SEA"),("TITO'S CANTINA TEQUILA BAR AND GRILLE","1334 CAPE CORAL PKWY E","","","SEA"),
 ("WENDY'S","1601 DEL PRADO BLVD S","","","SEA"),("WINGNUTS","231 DEL PRADO BLVD S STE 8","","","SEA"),
 # bars/venues named on happy-hour listing sites that are not in the food-license extract
 ("THE NAUTI MERMAID DOCKSIDE BAR & GRILL","5951 SILVER KING BLVD","33914","","BAR"),("DIXIE ROADHOUSE","1023 SE 47TH TER","33904","239-541-7900","BAR"),
 ("BOTANICAL BREWING TAPROOM","839 MIRAMAR ST","33904","","BAR"),("SCOTTY'S BIERWERKS","901 E INDUSTRIAL CIR","","","BAR"),
 ("NO.3 CRAFT BREWS & BEER BAR","1319 CAPE CORAL PKWY E","33904","","BAR"),("PADDYWAGON IRISH PUB","","","","BAR"),
 ("PALACE PUB & WINE BAR","","","","BAR"),("WICKED DOLPHIN RUM DISTILLERY","","","","BAR"),("RACK'EM SPIRITS & TIMES","","","","BAR"),
 ("MERMAID LIQUOR BAR","","","","BAR"),("EIGHT-FOOT BREWING","","","","BAR"),("OLLIE'S PUB RECORDS AND BEER","","","","BAR"),
 ("AMY'S WINEHOUSE","","","","BAR"),("THE WORLD FAMOUS CIGAR BAR","","","","BAR"),("THE LION'S DEN BAR AND GRILL","","","","BAR"),
 ("THE O BAR","","","","BAR"),("MARTIN'S PUB","","","","BAR"),("LATITUDE 78 BAR & GRILLE","","","","BAR"),
 ("THE DUGOUT SPORTS BAR & GRILL","","","","BAR"),("WICKED! TIKI BAR","","","","BAR"),("CALOOSA CLUB","","","","BAR"),
 ("CHORONI BAKERY CAFE & WINE BAR","","","","BAR"),("LUIS BAKERY BAR & GRILL","","","","BAR"),("WINDOWS ON THE GREEN","","","","BAR"),
]
rows += EXTRA
DROP = re.compile(r"WESTIN CAPE CORAL RESORT|FAIRFIELD BY|HAMPTON INN|HOLIDAY INN|GALLERY AT CAPE|PERSONAL TOUCH CATERING|BINGO|SUN SPLASH|RACQUET|DINO SCOOPS")
NO_BAR = re.compile(r"ARBY|BURGER KING|MCDONALD|WENDY|TACO BELL|SUBWAY|DUNKIN|DOMINO|PAPA JOHN|LITTLE C|PIZZA HUT|JET'S|MARCO'S|CHECKERS|CHICK-FIL|CHIPOTLE|CULVER|DAIRY QUEEN|DQ |KFC|KENTUCKY FRIED|POPEYES|POLLO TROPICAL|FIVE GUYS|FIREHOUSE|JERSEY MIKE|JIMMY JOHN|JASON'S DELI|PANERA|EINSTEIN|STEAKNSHAKE|WAFFLE HOUSE|WING ?STOP|QDOBA|PEI WEI|HUEY MAGOO|CAPRIOTTI|TROPICAL SMOOTHIE|COLD STONE|MENCHIE|ICE CREAM|ICE S+ ?CREAM|CREAMERY|SCOOPS|YONUTZ|GELATO|PRETZEL|COFFEE|LATTE|AROMA JOE|BAGEL|BAKERY|JUICERY|PURE GREEN|PURA BLISS|BAHIA BOWLS|SALAD KING|CHICKEN SALAD CHICK|BUBBAKOO|MOE'S|LENNY'S|CICIS|FIRST WATCH|KEKE|BOB EVANS|DENNY|PERKINS|METRO DINER|LET'S WAFFLE|MISSION BBQ|EAST OF CHICAGO|ZIRILLI|SWEET SPOT|SIDECAR TREATS|TRULY TROPICAL|GRAZING HAUS|PLAY CAFE|SNACK BAR|ENGLUNDS|PARKWAY SUBS|CHINA|WOK|LION KING|BUDDHA-BACHI|SEED & BEAN|LE PETIT|LOVE BOAT|CUBATALY|ON FIRE GRILL|JESSIE JAYS")
SMALL = {'AND','OF','THE','BY','AT','ON','DE','DEL','Y','IN'}
KEEP = {'BBQ','II','KFC','DQ','FL','BIG8','CRAFTED','J&P','J','P','OT'}
def title(n):
    n = re.sub(r"\s*(#\s*\d+|\b\d{3,6}\b|,? ?\b(INC|LLC|CORP)\b\.?|OPERATED BY TICE| FSU)", "", n)
    n = re.sub(r"^(.*) \(THE\)$", r"The \1", n).strip(" ,-")
    out = []
    for i, w in enumerate(n.split()):
        if w in KEEP: out.append(w)
        elif w in SMALL and i: out.append(w.lower())
        else: out.append(re.sub(r"(^|[\s\-/(&.])([a-zà-ÿ])", lambda m: m.group(1)+m.group(2).upper(), w.lower()))
    return " ".join(out).replace("Mcdonald","McDonald").replace("'S","'s")
def addr(a):
    a = re.sub(r"\s+", " ", a).strip(" ,")
    t = " ".join(w if re.fullmatch(r"(N|S|E|W|NE|NW|SE|SW|[A-Z]?\d+[A-Z]?|[A-Z]-?\d+.*)", w) else w.capitalize() for w in a.split())
    return re.sub(r" And ", " & ", t)
def phone(p):
    d = re.sub(r"\D", "", p)
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 and d[:3] in ('239','941') else ""
def category(n, kind):
    for pat, c in [(r"SUSHI|JAPANESE|HIBACHI|KOTO|KUMO|SAKURA|TAKUMI|YELLOWFIN","Japanese"),(r"PHO|THAI|GINGER|ASIA|YUMMY|FUSION","Asian"),
      (r"MEXIC|TACO|CANTINA|BURRITO|TARASCO|TORO|JALISCO|MONARCA|IGUANA|CASAMIGOS|FONDITA|NORTENITA|AZUL|MAZORCAZO","Mexican"),
      (r"CUBAN|CUBAY|RINCON|TROPICAL|MAMBO|HI CUBANS|DOMINICAN|BRAZIL|PERUAN|AJI LIMON|DETODITOS|SAZON|COLLADOS|VLADY|GANDULES|ROCA|CITANOS|MI MANERA|SITIO","Latin"),
      (r"PIZZ|ITALIAN|TRATTORIA|RISTORANTE|MEATBALL|CARRABBA|OLIVE GARDEN|GUSTO|ARIANI|BUON|MANGIA|SPAGHY|PAPA JOE|MELLOW|LELULO|LEONI|UNABELLA|NICE GUYS|AMORE","Italian & pizza"),
      (r"SEAFOOD|LOBSTER|CRAB|FISH|OYSTER|RAW BAR|BONEFISH|PINCHERS|FINS|BIMINI|HOOKED|RUMRUNNERS|MOORINGS|AQUA","Seafood"),
      (r"STEAK|OUTBACK|LONGHORN|PRIME|RIB CITY|BBQ|BARBECUE|ROADHOUSE","Steak & BBQ"),
      (r"SPORTS|BILLIARD|PUB|TAVERN|LOUNGE|BAR\b|TIKI|BREW|DEK|DIVE|CABARET|SALOON|HOOTERS|WINGS|WING HOUSE|DUFFY|BEEF 'O'|WALK ON|CORK|WINE|DISTILLERY|RACK'EM|CIGAR|CLUB|TORCHED|KEG|STONES THROW|NEVERMIND|RALPH|CLASS SIX|CROOKED COW|BOWLERO","Bar & grill"),
      (r"DINER|OMELET|BRUNCH|CAFE|BREAKFAST|WAFFLE|FRENCH PRESS|PERK","Breakfast & cafe"),(r"INDIAN|MASALA","Indian"),(r"GREEK|MEDITERRANEAN","Mediterranean")]:
        if re.search(pat, n): return c
    return "Bar & grill" if kind == "BAR" else "Restaurant"
# Researched happy hours: (name fragment, address fragment or '', times, deals, source, confidence)
S1="swflhappyhour.com (checked Nov 2026)"; S2="discoverhappyhours.com"; S3="whereat.io listing"
HH = [
 ("BACKSTREETS","", "Mon–Fri 4–6 PM; Tue late 10 PM–12 AM","Half-price drinks, shots, bottled beer and drafts",S1,"medium"),
 ("BIMINI BASIN","", "Daily 2–6:30 PM (food until 5)","$2 oysters, $8–9 small plates, $6–9 cocktails, $4 drafts, $6 wine",S1,"medium"),
 ("BUBBA'S ROADHOUSE","", "Daily open–7 PM; Sun–Thu 9 PM–close","2-for-1 well drinks, $1 off beer",S1,"medium"),
 ("CAPE CABARET","", "Tue–Sat 5–6 PM","Half-price house wine, well cocktails, domestic drafts",S1,"medium"),
 ("FORDS GARAGE","", "Mon–Fri 2–6 PM","$2 off drinks and drafts, premium wells $4, bar bites from $7",S1,"medium"),
 ("GATHER","", "Tue–Fri 5–6 PM; Sat–Sun 3–6 PM","Food $8–14, drinks $5–10, $1 off domestic beer","gathercape.com (official)","high"),
 ("HOOKED ISLAND GRILL","", "Drinks 2–6 PM; food 2–5 PM","House wine and wells $4–7, domestic drafts $3",S1,"medium"),
 ("JUNGLE BIRD","", "Daily 2–6 PM (Mon from 4 PM); Sun brunch 10 AM–2 PM","$3 domestic beer, $7 wells/signature cocktails/wine, $9 food; half-price tiki cocktails Tue",S1,"medium"),
 ("MARKER 92","", "Daily 3–6 PM","Drink and food specials","marriott.com (Westin, official)","high"),
 ("NAUTI MERMAID","", "Daily 3–6 PM","Drink and food specials","marriott.com (Westin, official)","high"),
 ("OAK & STONE","", "Mon–Fri 2–6 PM and 9 PM–close","25% off tap wall, wine and whiskey; $6–9 bites and drinks","oakandstone.com (official)","high"),
 ("OVERTIME PIZZA","", "Mon–Fri 11 AM–6 PM","$4 wells and wine, $3.50 domestic drafts",S1,"medium"),
 ("PINCHERS","", "2-for-1 all day, every day; food specials 3–6 PM","2-for-1 wine, beer and well cocktails",S1,"medium"),
 ("POINT 57","", "Mon–Fri 3–6 PM","Discounted beer, wine, cocktails and small plates (bar only)",S1,"medium"),
 ("RUSTY'S RAW BAR","", "Daily 11 AM–7 PM","Daily food and drink specials","rustysraw.com (official)","high"),
 ("SAGE ON 47TH","", "Tue–Fri 4–6 PM","Bar happy hour; specials vary",S1,"medium"),
 ("DEK","4704", "Mon–Fri 1–3 PM; Mon all day; late-night windows Tue–Sat","Half-price drink windows, themed nights",S1,"medium"),
 ("LOBSTER LADY","", "Daily 11 AM–5 PM; 10 PM–12 AM","Drink specials",S2,"medium"),
 ("IGUANA MIA","", "Daily 2–6 PM; Fri–Sat 9–10 PM","Discounted margaritas and premium wells",S2,"medium"),
 ("BONEFISH","", "Daily 3–6:30 PM","$1 off drafts, $5–6 house wine, $7 cocktails, $7 appetizers",S2,"medium"),
 ("MEXICO LINDO","", "Mon–Fri 3–5 PM","$3 house margaritas and wells, 2-for-1 drafts, 50% off wine",S2,"medium"),
 ("FATHOMS","", "Tue–Sun 11:30 AM–6 PM","$1 off beer and liquor, $5 wells/house wine, $15 buckets (one source says Tue–Fri 2–5 PM)",S2,"low"),
 ("RUMRUNNERS","", "Daily 3–6:30 PM","$1.50 oysters and shrimp, $6 light bites, drink specials",S2,"medium"),
 ("AQUA SEAFOOD","", "Daily 3–6 PM","",S2,"medium"),
 ("CARRABBA","", "Daily 4–6 PM","$5–9 cocktails, sangria and wine; $3 Bud Light and Peroni drafts",S2,"medium"),
 ("CLASE AZUL","", "Mon–Fri 11 AM–5 PM","",S2,"low"),
 ("PARADISE PIZZA","", "Daily 2–5 PM","",S2,"medium"),
 ("CENO GRILLE","", "Mon–Sat 3–6 PM","$1 off all glasses of wine and beer",S2,"medium"),
 ("TWO MEATBALLS","", "Daily 12–6 PM","",S2,"medium"),
 ("SOUTH CAPE DINER","", "Mon–Fri 1–3 PM","",S2,"low"),
 ("FRONT PORCH SOCIAL","", "Tue–Sun 3–6 PM","Happy hour cocktails $8","menupedia.us / whereat.io","medium"),
 ("STONES THROW","", "Daily 4–6 PM","Happy hour menu","stonesthrowcc.com (official)","high"),
 ("DUFFY'S","", "2-for-1 drinks all day, every day","","come-to-cape-coral.com","medium"),
 ("MONKEY BAR","", "Daily open–8 PM","Half-price liquor, house wine and well drinks","mapquest.com listing / Cape Coral Living","medium"),
 ("10 TWENTY FIVE","", "Mon–Fri 4–7 PM","","Yelp review snippet","low"),
 ("TWISTED LOBSTER","", "Tue–Fri from 4 PM","",S3,"low"),
 ("BUFFALO WILD WINGS","", "Mon–Fri 3–6 PM","",S3,"low"),
 ("CHILIS","", "Mon–Fri 3–6 PM","",S3,"low"),
 ("BOTANICAL BREWING","", "Mon–Fri 2–5 PM","",S3,"low"),
 ("BUON APPETITO","", "Tue–Sun 3–6 PM","",S3,"low"),
 ("KEG AND COW","", "Mon–Fri 3–6 PM","$1 off pints and wine (older listing)","come-to-cape-coral.com","low"),
 ("FINS SEAFOOD","", "Weekdays from 3 PM","","come-to-cape-coral.com","low"),
 ("RALPH'S PLACE","", "4–6 PM (days vary)","Discounted drinks","thehappyhourfinder.com","low"),
]
RENAME = {"DEK":"The Dek Bar","DIVE":"The Dive","FORDS GARAGE":"Ford's Garage","CHILIS GRILL & BAR":"Chili's Grill & Bar",
 "GATHER/NEXT DOOR":"Gather","PRIME 239 STEAKHOUSE":"Prime 239 Steakhouse","10 TWENTY FIVE":"10 Twenty Five","CAFE (THE)":"The Cafe",
 "ANTHONYS ON THE BLVD":"Anthony's on the Blvd","NICE GUYS":"Nice Guys Pizza, Beer & Cocktails","DOLPHIN KEY RESORT LLC":"Tiki Hut Bar & Grill (Dolphin Key Resort)"}
seen, out, used = set(), [], set()
for n, a, z, p, kind in rows:
    if DROP.search(n): continue
    key = (re.sub(r"\W", "", n)[:14], re.sub(r"\D", "", a)[:5])
    if key in seen: continue
    seen.add(key)
    hh = dict(status="unconfirmed", times="", deals="", source="", confidence="")
    if NO_BAR.search(n) and kind != "BAR" and "AZUCAR" not in n: hh["status"] = "none_expected"
    for i, (frag, af, t, d, src, conf) in enumerate(HH):
        if frag in n and af in a:
            hh = dict(status="listed", times=t, deals=d, source=src, confidence=conf); used.add(i); break
    nm = RENAME.get(n, title(n))
    out.append(dict(id=re.sub(r"[^a-z0-9]+", "-", (nm + " " + a.split(" ")[0]).lower()).strip("-"), name=nm,
        address=(addr(a) + ", Cape Coral, FL " + z).strip(", ") if a else "Cape Coral, FL", phone=phone(p),
        category=category(n, kind), happyHour=hh, lastChecked=TODAY))
missing = [HH[i][0] for i in range(len(HH)) if i not in used]
assert not missing, missing
assert len({r["id"] for r in out}) == len(out)
out.sort(key=lambda r: r["name"].lower())
json.dump(dict(city="Cape Coral, FL", updated=TODAY, restaurants=out), open("data/restaurants.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(out), Counter(r["happyHour"]["status"] for r in out))
