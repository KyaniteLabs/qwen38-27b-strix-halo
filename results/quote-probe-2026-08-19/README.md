# QUOTE probe + horizon re-run (2026-08-19)
The GDN localizer experiment: can the model access a needle it can't answer from?

## QUOTE probe results (needle at 25% of 198k, "Station QUOTE access code: HORIZON-TEST-4419.")
| Question | Time | Result |
|----------|------|--------|
| Exact access code? | 1818s (cold) | HIT — full code retrieved |
| Quote the sentence? | 16s (warm) | Verbatim quote |
| Does a code exist? | 9s (warm) | YES |
| Summarize the text | 27s (warm) | Correct, specific |

## Key findings
1. Model CAN retrieve at 198k/25% — needle content matters, not just position
2. Warm-prefix caching works: 9-27s per follow-up query (vs 30-min prefill)
3. Retrieval is selective: distinctive strings survive GDN compression, arbitrary ones don't
4. The "no retrieval at any length" claim is FALSIFIED — it's "selective retrieval"

## Horizon re-run (different needle text — see S-027)
10% HIT, 25% MISS (Risk template), 50% HIT — but needle phrasing changed vs original
(Station GRANITE vs Station AURA), so cross-run comparison is confounded.
Internally valid: some codes work at some depths.

## Warm-prefix timing (product-relevant)
Once a 198k context is loaded (~30 min), follow-up queries take 9-27 seconds.
This means a persistent 198k session can be queried repeatedly at interactive speed.
