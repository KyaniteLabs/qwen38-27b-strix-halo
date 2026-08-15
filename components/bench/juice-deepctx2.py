import json, time, urllib.request, sys, random

# juice-deepctx2.py PORT — ~50k-token deep-context KV integrity probe.
# Unique-ish topics keyed by probe; probes by TOPIC NAME only.
PORT = sys.argv[1] if len(sys.argv) > 1 else "46381"
random.seed(3838)

TOPICS = ["harbor logistics","tidal patterns","salt corrosion","lamp mechanics",
 "fresnel optics","fog horns","ship registries","kelp harvesting","storm tracking",
 "battery chemistry","radio protocol","chart making","rope splicing","buoy painting",
 "gull counting","crate stacking","lamp oil viscosity","keeper rotations","rowboat repair",
 "signal flags","lighthouse paint","weather vane","winch greasing","bell polishing",
 "logbook binding","anchor chain","dock fenders","emergency rations","first aid kit",
 " lantern glass","brass fittings","cargo nets","tide gauge","barometer","wind gauge",
 "rope ladder","supply skiff","mail delivery","visitor log","fog diary","light spectrum",
 "mirror alignment","wick trimming","fuel reserves","generator belt","radio batteries",
 "storm shutters","helipad marking","whistle codes","beacon timing","shelf inventory",
 "boot drying","coat hooks","glove repair","thermos flasks","biscuit tins","tea inventory",
 "coffee grinder","chair repair","desk lamp","ink supply","pen nibs","paper stock",
 "seal sightings","whale migration","dolphin pods","pelican counts","cormorant nests"]
EXTRA = ["morning checklist","evening checklist","weekly supply count","monthly audit note",
 "quarterly inspection remark","seasonal preparation memo","drill record","visitor notice",
 "weather remark","maintenance log"]

msgs = [{"role":"user","content":"We are assembling a very long lighthouse keeper's logbook. I will give you hundreds of short entries. Just reply 'Logged.' to each."}]
msgs.append({"role":"assistant","content":"Understood. I'll keep track of every entry."})

probes = {}
n_entries = 420
for i in range(1, n_entries+1):
    t = f"{TOPICS[i % len(TOPICS)]} {EXTRA[i % len(EXTRA)]}"
    code = f"{random.randint(100,999)}-{random.randint(10,99)}"
    msgs.append({"role":"user","content":
        f"Entry {i}, {t}: the crew completed the standard routine, weather was noted, "
        f"supplies were checked against the manifest, the equipment was inspected and wiped down, "
        f"readings were taken twice and compared with yesterday's values, and the results were "
        f"filed in the cabinet under section {i}. Special note for this entry: the {t} ledger code is {code}."})
    msgs.append({"role":"assistant","content":f"Logged."})
    if i in (20, 210, 400):
        probes[t] = (i, code)

ptopic = list(probes.keys())
msgs.append({"role":"user","content":
    f"Without scrolling back: state the ledger code for (a) the {ptopic[0]}, (b) the {ptopic[1]}, "
    f"and (c) the {ptopic[2]}. Answer as three lines: 'topic: CODE'."})

body = json.dumps({"messages":msgs,"max_tokens":200,"stream":False,
                   "chat_template_kwargs":{"enable_thinking":False}}).encode()
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/chat/completions",
                             data=body, headers={"Content-Type":"application/json"})
t0=time.time()
with urllib.request.urlopen(req, timeout=1200) as r:
    j=json.load(r)
dt=time.time()-t0
print(f"prompt_tokens={j.get('usage',{}).get('prompt_tokens',-1)}  wall={dt:.1f}s")
print("MODEL ANSWER:"); print(j["choices"][0]["message"]["content"])
print("EXPECTED:")
for t,(i,c) in probes.items(): print(f"  {t} (entry {i}): {c}")
