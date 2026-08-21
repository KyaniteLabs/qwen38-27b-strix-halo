# 27B optimal config — both open dials measured in one night (2026-08-21)

CEO directive: 27B optimal config gates all other work. Both remaining dials
measured tonight; the KV window was cut mid-run at the CEO's further ruling
(everything-35B stops) AFTER both 27B decision cells completed — the operator
cut + verdict are labeled in kv-sweep-driver.log; restores done by hand
(kill-verified PIDs; champion q4_0 readback; pmode performance + timer).

## Dial 1 — KV cache quant (paired, 27B Q4_K_XL, ctx 131072, spec off, no cache-reuse)
| quant | needle @52% of 130,719 tok | decode wall | warm quote/exist/sum | tg128 | GTT loaded |
|---|---|---|---|---|---|
| q8_0 | HIT exact, fr=stop | 3.2s | 8.0 / 1.3 / 9.1s | 12.3s | 21,592 MB |
| q4_0 | HIT exact, fr=stop | 4.0s | 8.4 / 1.5 / 11.9s | 11.9s | 19,589 MB |

**Verdict (pre-registered rule): q8_0** — quality parity (both exact), q8 faster
on decode and every warm query, +2.0 GB GTT (fits: 21.6 of 64 GB), matches CEO
lean. Serving flip pending CEO word. Labels: n=1 per cell, pilot; fill walls
930/915s (parity); 32k redundancy cells and f16 spot unfired (window cut).
Note: decode rows ended at ctok=17 both arms (early stop on the continuation
prompt; same shape both arms — pair valid, tok/s diagnostic only).

## Dial 2 — spec config (paired walls, same model/ctx/KV q4_0, 3 byte-identical prose problems)
| state | flags | mean wall / 200-tok problem |
|---|---|---|
| mirror (= serving) | draft-mtp,ngram-mod n-max 12 | **15.1s** |
| off | none | 17.8s |
| ngram only | ngram-mod | 17.7s |
| mtp only | draft-mtp | 15.1s |

**Verdict (pre-registered): MIRROR HOLDS** — the serving spec config is optimal
(off is 18% slower); MTP does the work, ngram adds nothing on prose.
Counting-class rows are diagnostic-only (repetition-assisted class, labeled in
raw). Champion cmdline captured pre-stop: spec-sweep-champion-cmdline.txt (box).

## The full 27B table after tonight
1. Weights: Q4_K_XL (CEO cap) — LOCKED
2. Context: 262144, retrieval proven at the native ceiling — LOCKED
3. Think routing: three-band knee maps — LOCKED
4. Spec: mirror config optimal (15.1 vs 17.8s) — PINNED
5. KV: q4_0 RETAINED BY CEO RULING (2026-08-21 ~04:20Z PT: "keep the cheap one") — FINAL

## CLOSE-OUT (2026-08-21 ~04:30Z PT)
The CEO weighed the trade (8 GB memory at full window vs 1-3s on warm
follow-ups; two-at-once servicing undecided) and kept the light setting.
The confirmation window was cut at the ruling (clean trap-restore; champion
never down for long): seed-A needle on q8 at 198k HIT exact before the cut
(10.4s, fr=stop, seed recorded), q4-arm GSM8K n=60 strict-match = 0.70
(thinking-off, 5-shot — NOT comparable to the 0.980 official canon, which ran
different eval settings; labeled). Seed B + q8 math arm unrun (moot).
**FINAL 27B CONFIG (serving now, zero changes needed): Q4_K_XL weights +
q4_0 KV + mirror spec config + 262144 ctx + think-off-default routing.**

## Raw
flip-confirm-results.log / flip-confirm-driver.log (cut window, partial gate labeled), kv-sweep-results.log / kv-sweep-driver.log (operator-cut + verdict labeled),
spec-sweep-results.log / spec-sweep-driver.log, per-launch server logs.
Instruments: qwen27-nucbox-stack components/exp-2026-08-19/ kv-sweep.sh,
kv-cells.py, spec-sweep.sh, spec-cells.py + self-tests (41/41, 32/32) after one
critic round each.
