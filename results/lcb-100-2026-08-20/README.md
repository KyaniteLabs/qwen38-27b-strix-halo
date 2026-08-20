# LiveCodeBench-100 — hard-weighted run on the champion (2026-08-20)

## Question
Tighten the CI on the champion's LiveCodeBench performance and get thinking-vs-not
knee data on the hard band. Sample deliberately hard-weighted (25 easy / 35 medium /
40 hard, seed 20260821) — a DIFFERENT INSTRUMENT from the stratified-30 (10/10/10):
not comparable to the 20/30=67% composite, which is best-per-problem across labeled
arms on the easier-weighted set.

## Conditions
Same serving/instrument family as LCB-30: Q4 champion, temp 0, public cases only,
shared-slot absent (solo overnight), thinking off, max 2048 for the base run.

## Results

| Arm | Score | Wilson 95% CI |
|---|---|---|
| Base (no-think, 2048, n=100) | **34/100 = 34%** | [25%, 44%] |
| Thinking-ON (budget 2048, max 6144) on hards | 3/10 first tranche; 30 more running | — |

Difficulty split (base): easy 19/25, medium 11/35, hard 4/40.

## Reading it honestly
- The point estimate sits far below the stratified-30 composite because the sample
  is hard-weighted AND single-config: no-thinking base on the 30's easy half was
  ~90%, on hards ~10-20%. Both numbers are true; they answer different questions.
  Cite the instrument, not just the number.
- Medium is the biggest gap band (11/35) — where prose-starvation bites hardest
  (the LCB-30 arm-C rescue was mostly mediums).
- The think-40 knee data (thinking-ON across all 40 hards) completes the routing
  picture: `lcb-100-think40-results.log` (first 10) + `lcb-100-think40b-results.log`
  (remaining 30) — combined verdict in the OPT-LOG when the second tranche lands.

## Warm-prefix confirmation (same overnight window)
`quote-rerun-results.log`: cold HIT; warm quote VERBATIM in 23.8s; exists 10.0s;
summary correct 17.5s. The load-once/query-many economics hold on the reverted
build — §13 two-tier model confirmed.

## Raw
`lcb-100-base-results.log`, `lcb-100-think40-results.log`, `quote-rerun-results.log`
