# Needle-format sweep S-027 — HALTED at control cell; anomaly = the finding (2026-08-19)

## What happened
The format sweep (prose control vs code-block vs semantic-phrase needles at 198k,
d50) was pre-registered with "control expected MISS; a HIT invalidates
comparability — halt+report." The control cell HIT.

## The decisive pair (token-identical prompts, ptok=198228 both)
- PRE-revert binary (2026-08-18, sweep2.log): MISS, fr=stop, ans='ok' (attractor)
- POST-revert binary (2026-08-19 21:46Z): HIT, fr=stop, ans='COBALT-8835-DELTA'

Only delta across the pair: llama.cpp c7d8722 revert (the fix that restored
vision — same host-buffer incoherence class on integrated GPUs).

## Why this matters
The pre-revert s4419 curve was 1/6 hits with degenerate attractors ('ok',
markdown risk-lists, fr=length, one byte-identical cross-prompt collapse).
The "degenerate basin" framing and the D19 mechanism paragraph rest on
pre-revert measurements. If the post-revert remap clears the basin, a
substantial part of the long-context failure map was the buffer bug, not
model/GDN behavior.

## Status
- Sweep HALTED per pre-registration (2 cells unfired).
- Post-revert depth remap (d10/25/35/75/90, byte-identical needles) RUNNING,
  ETA ~00:30Z. Board D78 transmitted; corrective addendum for affected blog
  posts recommended to hold until the curve lands.

## Raw
- `run-partial.log` — this run (parser probe + the HIT line)
- Pre-revert rows: ../deep-context-2026-08-18/sweep2.log
