#!/usr/bin/env python3
"""Blind-spot probes for the LCB-30 gate (2026-08-20, Simon's exhaustiveness challenge).
P1: vacuous-pass scan — any public case with empty expected output could match
    empty stdout (a PASS that proves nothing). Scan ALL shipped cases.
P2: full independent re-grade of arm C from saved generations (gen-think/) with
    the shipped grader — every arm-C verdict re-executed from artifacts.
P3: binomial CI for the composite (computed, not remembered).
"""
import json, os, re, sys, importlib.util
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("lcbh", os.path.join(HERE, "lcb-bench.py"))
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
rows = [json.loads(l) for l in open(os.path.join(HERE, "lcb-subset30.jsonl"))]
by_id = {r["question_id"]: r for r in rows}

print("== P1: vacuous-pass scan (empty expected outputs) ==")
vacuous = []
for r in rows:
    for i, c in enumerate(json.loads(r["public_test_cases"])):
        if str(c.get("output", "")).strip() == "":
            vacuous.append((r["question_id"], i))
print(f"cases with empty expected: {len(vacuous)} {vacuous if vacuous else ''}")

print()
print("== P2: arm C independent re-grade from saved generations ==")
gen_dir = os.path.join(HERE, "gen-think")
armC = [l for l in open(os.path.join(HERE, "lcb-30-think2048-results.log")) if l.startswith("[")]
mismatches = 0
for line in armC:
    q = line.split("] ")[1].split(" ")[0]
    path = os.path.join(gen_dir, q + ".py")
    if not os.path.exists(path):
        print(f"[MISSING-GEN] {q}")
        mismatches += 1
        continue
    code = open(path).read()
    ok, err, n = h.grade(code, by_id[q])
    recorded = ": PASS" in line
    agree = ok == recorded
    if not agree:
        mismatches += 1
    print(f"[{'AGREE' if agree else 'DISAGREE'}] {q}: regrade={'PASS' if ok else 'FAIL'} recorded={'PASS' if recorded else 'FAIL'} {('err=' + str(err)) if err else ''}")

print()
print("== P3: binomial 95% CI for 20/30 (Wilson) ==")
n, p = 30, 20 / 30
z = 1.96
den = 1 + z * z / n
center = (p + z * z / (2 * n)) / den
half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
print(f"20/30 = 66.7%; Wilson 95% CI = [{(center - half) * 100:.0f}%, {(center + half) * 100:.0f}%] (n=30, wide)")
print()
print("VERDICT:", "CLEAN" if (not vacuous and mismatches == 0) else "ISSUES FOUND ABOVE")
sys.exit(0 if (not vacuous and mismatches == 0) else 1)
