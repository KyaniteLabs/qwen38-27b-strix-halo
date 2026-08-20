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

## UPDATE 2026-08-20 00:35Z — DEPTH REMAP COMPLETE: 6/6, contamination CONFIRMED
Post-revert curve (byte-identical needles, seed 4419, 198k, temp 0):

| depth | pre-revert (08-18 sweep2) | post-revert (tonight) |
|---|---|---|
| 10% | MISS — ans='ok' attractor | **HIT** GRANITE-3319-BRAVO |
| 25% | HIT | HIT TOKFLINT-7702-KILO |
| 35% | MISS — markdown attractor, fr=length | **HIT** SANDSTONE-5548-ECHO |
| 50% | MISS — ans='ok' (ptok=198228, token-identical) | **HIT** COBALT-8835-DELTA |
| 75% | MISS — markdown attractor, fr=length | **HIT** PIRATE-1290-FOXTROT |
| 90% | (never completed pre-revert — sweep died) | **HIT** JASMINE-2207-ECHO |

**6/6 exact retrieval post-revert; zero attractor outputs; every cell fr=stop.**
The anchor pair: d50, token-identical prompts (ptok=198228 both eras) —
MISS('ok') pre-revert, exact-code HIT post-revert; only delta = c7d8722 revert.

Pre-revert behavior was not uniformly-dead either: the (confounded) horizon
re-fire went 2/3 with an attractor MISS — i.e. the bug made long-context
retrieval UNRELIABLE, and the revert made it consistent.

## Verdict
The pre-revert deep-context failure map — the "degenerate basin" framing, the
attractor outputs, "no reliable needle retrieval at any tested length" — was
substantially the llama.cpp c7d8722 host-buffer bug on this integrated GPU,
not model/GDN behavior. On the reverted build, this rig retrieves arbitrary-ID
needles at ALL tested depths at 198k. Published mechanism claims built on
pre-revert measurements need corrective addenda (board D78/D79).

## Raw
- `depth-remap-results.log` — 5 cells + TOTAL + ROWS sentinel
- `depth-remap-run.log` — full run incl. parser probe

## UPDATE 2026-08-20 05:58Z — NATIVE CEILING TESTED: HIT
`nativemax-results.log`: same instrument, d50 LIMA needle, haystack extended to
7,630 paragraphs — **prompt_tokens = 261,130 of the 262,144 window (99.6%,
server-verified), exact code retrieved, finish_reason=stop, 53-min prefill.**
The corrected retrieval claim now holds at the literal native ceiling, not just
at 198k. "Tested at native ceiling" is now a true sentence.
