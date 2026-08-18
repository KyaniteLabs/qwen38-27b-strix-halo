# Measurement methodology

How every number in this repo is produced, and what each number is allowed to
claim. If a claim in this repo has no trace to a method here, treat it as
anecdote. Raw per-request data for the reasoning-budget experiments lives in
`results/` (counts and grades only, no model traces).

## Conditions of every headline number

All engine and accuracy numbers in this repo were measured on one box:

- Hardware: AMD Ryzen AI Max+ 395 mini-PC (Radeon 8060S, gfx1151), 96GB
  unified LPDDR5X
- Backend: ROCm 7.2.4 (HIP build)
- llama.cpp: b10435-era dflash branch build (9d57ce4), speculative stack
  `draft-mtp,ngram-mod` (n-max 12, n-min 24) unless a result says otherwise
- Single host, no cross-machine replication yet: treat absolute values as
  this-box measurements and compare only within-condition

A number quoted without this condition line (build, backend, silicon) is a
misquote. Build-era matters: spec-decode behavior moved between llama.cpp
builds during August 2026.

## Instruments

| Metric | Instrument | Class |
|---|---|---|
| Wire tokens | `srv_prompt_n` as reported by the server | source-reported |
| Reasoning/output length | `think_ch`, `out_ch`, `completion_tokens` from server response fields | source-reported |
| Engine decode speed | count-to-30 (c30) battery, cold and warm, custom | custom-labeled |
| Task latency | 5-task battery, n=3, thermal band | custom-labeled |
| Reasoning quality | official GSM8K exact-match grading (canonical extraction + exact match) | canonical-official |
| Math accuracy (stress) | Omni-MATH sampled subsets, boxed-answer extraction | custom-labeled |
| Win/loss significance | paired McNemar on same-problem cells | standard test, custom sampling |

Custom instruments are labeled as such everywhere they are quoted. The c30
warm band is a repetition-assisted artifact (ngram speculation replays repeated
structure); it is never quoted as conversational speed. Conversational prose
speed is the 11-24 tok/s band under these conditions, and that is memory
bandwidth, not a tunable.

## Evidence classes

Every published result carries one of three labels:

- CLEAN: paired design, n satisfies the rules below, official grading where
  grading is the claim, no known confounds. Quotable as a headline.
- DIRECTIONAL: real signal but underpowered, or measured with a custom
  instrument. Quote only with the label attached.
- PILOT: n=1 or uncontrolled. Never gates an adoption or tuning decision,
  never quoted without the label.

## n-rules

1. Repeat runs within a thermal window: n>=3 before any speed number is
   called CLEAN. First-run-after-idle (cold) and back-to-back (warm) are
   reported as separate bands and never averaged together.
2. n=1 is PILOT-class, always. It can justify running the real experiment,
   nothing more.
3. Accuracy cells are paired: every cell in a comparison sees the same
   problems (same-problem pairing with rotation), so comparisons are
   within-problem. Significance is paired McNemar on discordant pairs, not a
   two-sample test on independent sets.
4. Every cell declares its n in the runner header and in the dump.

## The server-default audit (read before firing any A/B)

Before any experiment that varies a per-request field, read the live
llama-server command line. Any server-level default on the experiment axis
(reasoning budget, effort kwargs, sampling) silently replaces the omitted
field in cells meant to be the control. Control arms send explicit huge or
explicit none overrides, never omissions.

This rule exists because it bit us: a first Omni-MATH run had a "no budget"
cell that was in fact a 2048-token cell inherited from the service-level
default. The paired dumps published in `results/` were produced with explicit
overrides on every arm, including the none arms.

## Output caps

max_tokens on an uncapped arm must not bind mid-thinking: a run that dies at
the cap is length-death, not a budget effect, and would masquerade as a
quality regression. Caps are set well above the observed thinking length for
the uncapped arms (6000 raised to 12000 for the published Omni-MATH runs), and
every row still carries `finish_reason`, so length-terminated rows are visible
in the dump rather than hidden in an accuracy denominator.

## Variance disclosure commitment

Every headline number ships with its run count and spread (range or sd) and
its thermal state. Where only one run exists, the number is labeled PILOT
until repeated. Where a band is an artifact of the instrument (repetition
assist, cache warmth), the artifact is named in the same sentence as the
number. Power/energy numbers are not published as measured claims on this
box yet; when they are, they will carry the same conditions line and
instrument class.

## What the raw dumps contain

`results/` holds per-request JSONL with counts, grades, and metadata only.
The model's reasoning text and final-answer text are stripped before
publishing: public data here is counts and grades, not traces. Schema and
production details: `results/README.md`.
