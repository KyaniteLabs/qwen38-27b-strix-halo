# results/ raw per-request dumps (counts and grades, no traces)

Public evidence backing the reasoning-budget experiments described in
`../METHODOLOGY.md`. Files are JSONL, one row per request. The model's
reasoning text and final-answer text are stripped before publishing: what you
get is counts, grades, and run metadata. Conditions for both files: single
AMD Ryzen AI Max+ 395 box (gfx1151, 96GB unified), ROCm 7.2.4, llama.cpp
b10435-era dflash build (9d57ce4), Qwen3.8-27B UD-Q4_K_XL, xhigh effort
unless the cell name says otherwise. Same-problem paired cells throughout:
`sample_idx` identifies the problem, and every cell contains the same
`sample_idx` set.

## Schema (identical fields in both files unless noted)

| Field | Type | Meaning |
|---|---|---|
| cell | str | experimental arm, `<effort>-<budget>`: e.g. `xhigh-512` = xhigh effort, 512-token reasoning budget; `none` = no budget cap (explicit override, see the server-default audit in METHODOLOGY.md) |
| sample_idx | int | problem identifier within the dataset sample; identical across cells (paired design) |
| correct | bool | grade for the row (official GSM8K exact-match / Omni-MATH boxed-answer extraction) |
| think_ch | int | reasoning text length in characters (server-reported response split) |
| out_ch | int | final-answer text length in characters |
| completion_tokens | int | total generated tokens as reported by the server |
| wall_s | float | wall-clock seconds for the request |
| extracted | str or int | graded answer extracted from the output (`null` = extraction failure) |
| expected | str or int | dataset reference answer |
| method | str | extraction method (`hash` = GSM8K canonical after-#### hash match; `boxed` = boxed-answer extraction; `noboxed` = extraction failed) |
| finish_reason | str | `stop` or `length` (length = hit the token cap mid-generation; visible so length-death is never hidden in an accuracy denominator) |
| difficulty | float | Omni-MATH difficulty 1-9 (omnimath file only) |
| ts | str | completion timestamp, UTC |

## gsm8k-budget-2026-08-17.jsonl

900 rows = 6 cells x 150 paired GSM8K test problems; reasoning-budget sweep
under official GSM8K grading (exact match on the canonical extraction).
Cells: `medium-none`, `xhigh-none`, `xhigh-2048`, `xhigh-4096`, `xhigh-8192`,
`xhigh-8192-msg` (the msg variant appends a budget-exhaustion notice to the
request).

Correct counts (n=150 per cell): medium-none 147, xhigh-none 147,
xhigh-2048 147, xhigh-4096 146, xhigh-8192 146, xhigh-8192-msg 146. Under
paired McNemar these cells are statistically indistinguishable at n=150:
budgeting reasoning from 2048 tokens up does not move official GSM8K accuracy
on this model and box, it only moves thinking length and wall time.

## omnimath-paired-2026-08-18.jsonl

150 rows = 3 cells x 50 paired Omni-MATH problems (difficulty 1-9 in this
sample), the stress test where a budget effect would show first. Correct
counts (n=50 per cell): xhigh-none 22, xhigh-512 20, xhigh-1024 20.
Discordant pairs: none-vs-512 = 5/3, none-vs-1024 = 3/1, 512-vs-1024 = 3/3;
none of these reach significance under paired McNemar at n=50. DIRECTIONAL
evidence class: the point estimate ordering (none > capped) is consistent
with truncation hurting on hard problems, but this sample cannot carry that
conclusion. `finish_reason: length` rows are present and are counted as
incorrect as-graded; they are not removed.

## How produced

Runners hit the local llama-server HTTP API (one request per row, cells
interleaved over the same problem list). Headers on the runner declare n per
cell. Rows were written per-request at `ts`, then post-processed for this
dump by deleting the `reasoning` and `content` fields only; no numeric or
grade field was touched. Reproduce with the harnesses under
`components/bench/` and the conditions line above.
