# Model-blob A/B — old bee238bb vs new 3f227079 Q4_K_XL (2026-08-19)

## Question
unsloth updated the Q4_K_XL blob (17.92GB → 17.56GB, sha256 3f227079…).
Does the new quant beat the incumbent on our instruments? Swap only on paired
evidence (pre-registered gate; tie = no swap).

## Design
ONE server on :46399, unit-exact champion flags + mmproj-F16 (UNCHANGED in the
new revision — remote etag == local sha cbb841a9…). Old-blob arm first, then
new-blob arm, identical serving conditions, same evening. Champion stopped
during the window, restored + verified after (PID/cmdline/KV readback).
mmproj held fixed so the ONLY variable is the main-model blob.

## Results — TRUE PAIRED TIE

| Cell | Old (bee238bb) | New (3f227079) |
|---|---|---|
| HumanEval-30 (thinking off, temp 0) | 28/30 | 28/30 |
| Failing problems | 50, 145 | 50, 145 (identical rows) |
| Vision VQA-6 | 5/6 | 5/6 (identical miss = grading artifact) |
| Speed spot (3× ~270-tok gens) | 268/271/280 tok, all fr=stop | 297/257/284 tok, all fr=stop |

## Verdict
**NO SWAP.** Row-identical tie on every instrument; zero tripwires; the 360MB
smaller file buys nothing measurable (n=30/n=6 pilot class). Champion stays on
bee238bb. The verified new blob is kept at
/srv/external/downloads/Qwen3.8-27B-UD-Q4_K_XL-3f227079.gguf for future re-test
(e.g. if a harder bench — LiveCodeBench-class — separates them).

## Raw logs
- `bench-results-{oldblob-paired,newblob-3f227079}.log` — per-problem rows
- `vision-{oldblob-paired,newblob-3f227079}.log` — per-question rows
- `blob-ab-driver.log` — window record (pre-registration, health waits,
  champion restore verification)
