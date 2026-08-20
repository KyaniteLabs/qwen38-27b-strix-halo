#!/usr/bin/env python3
"""s8807 second-seed remap claims verifier (staged BEFORE results land — verifier-first).
Run from results/needle-format-2026-08-19/: python3 verify_s8807.py
Checks: 6 cells present, all six stations with the byte-identical s8807 codewords,
ROWS sentinel, per-cell fr=stop, and prints the curve tally. Exit 0 = structurally
valid; the SCIENTIFIC verdict (hits) is printed, not asserted — any MISS is a
finding to halt-and-report per the pre-registration, not a script failure.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECT = {
    10: ("AURA", "MARBLE-8821-TANGO"),
    25: ("NOVA", "COPPER-6104-DELTA"),
    35: ("VEGA", "SLATE-9350-BRAVO"),
    50: ("LIMA", "ONYX-2268-ECHO"),
    75: ("ORION", "QUARTZ-7742-FOX"),
    90: ("MIKE", "AMBER-4486-TANGO"),
}

src = open(os.path.join(HERE, "depth-remap-s8807-results.log")).read()
lines = src.splitlines()
fail = []

rows = [l for l in lines if l.startswith("[remap s8807] depth")]
if len(rows) != 6: fail.append(f"expected 6 cells, got {len(rows)}")

hits = 0
seen = set()
for l in rows:
    try:
        depth = int(l.split("depth ")[1].split("%")[0])
        verdict = l.split(": ")[1].split()[0]
        fr = l.split("fr=")[1].split()[0]
        ans = l.split("ans=")[1]
    except Exception:
        fail.append(f"unparseable row: {l[:60]}")
        continue
    seen.add(depth)
    station, pw = EXPECT[depth]
    if not ans.startswith("'") or pw not in ans:
        if verdict == "HIT":
            fail.append(f"d{depth}: HIT but answer {ans[:40]} lacks expected {pw}")
    if verdict == "HIT":
        hits += 1
        if pw not in ans: fail.append(f"d{depth}: HIT without codeword")
    if fr != "stop":
        fail.append(f"d{depth}: fr={fr} (expected stop for a clean cell)")

if seen != set(EXPECT): fail.append(f"missing depths: {set(EXPECT) - seen}")
if "ROWS=6" not in src: fail.append("ROWS=6 sentinel missing")
if "DEPTH-REMAP-S8807 DONE" not in src: fail.append("DONE sentinel missing")

total = [l for l in lines if "TOTAL" in l]
print(f"cells: {len(rows)} | HITs: {hits}/6 | " + (total[0] if total else "no TOTAL line"))
if fail:
    print("STRUCTURAL FAILURES:", *fail, sep="\n  ")
    sys.exit(1)
print("VERDICT: structure valid; curve tally above (any MISS = halt-and-report per pre-registration)")
