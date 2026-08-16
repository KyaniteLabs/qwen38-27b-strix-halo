# Qwen3.8-27B on Strix Halo — tuned serving profile

Fully measured configuration for serving **Qwen3.8-27B** (Apache-2.0, released 2026-08-14)
on **AMD Strix Halo** (Ryzen AI Max+ 395, Radeon 8060S, unified LPDDR5X, GTT 64GB) with
**llama.cpp** — speculation-stacked to the practical frontier of this silicon.

Current champion (production, restored 2026-08-15 19:36Z): **UD-Q4_K_XL @ 96k context**.

## UPDATE 2026-08-16 — champion advanced to the NATIVE CEILING: 262k context

Same hardware, same quant, three more gates passed in one night (ladder
96k → 160k → 192k → 262k, each A/B-tested on the real-task battery):

| Config | cold c30 | warm c30 | tpt battery | context |
|---|---|---|---|---|
| **NEW champion: Q4_K_XL + K+V q8_0 KV cache** | ~52-57 | **150-158 (band held)** | 6.8-12.9 s/task, 5/5 | **262,144 (native max)** |
| prior champion (row above) | 59.7 | 148-163 | 7.6-7.7 | 96k (f16 KV) |

The whole gain comes from KV-cache quantization (K+V q8_0 — KV halves, so
262k of q8 KV fits in LESS memory than 96k of f16). One labeled cost:
prefill ~299 tok/s vs ~390 on f16 KV (q8 dequant on cache reads; bigger
ubatch made it worse, not better). Time-per-task on real traces: unchanged
to faster. Measured, not estimated — every rung had a pre-registered gate
and the rollback unit stays in the RUNBOOK.

Also that night: spec-decode params swept (champion n12/n-min24 stands),
thermal un-capped (fan daemon owns dissipation), and a tool-position/
salience finding published upstream: ggml-org/llama.cpp#27165.
Q3_K_XL @ 128k was swapped in at 19:10Z and reverted the same hour — the quant ladder
(Q4 → Q3 → Q2) closed on **time-per-task**, not decode tok/s. See findings: that reversal
is the most useful result in this repo.

## The numbers (measured 2026-08-15, single box, reproducible via `components/bench/`)

count-to-30 bench, cold = first exposure, warm = back-to-back repeats:

| Config | Cold tok/s | Warm/repeat tok/s | Context |
|---|---|---|---|
| MTP n=2 (day-0 default) | 22 | 25 | 16k |
| MTP n=6 (mission baseline) | 32.7 | — | 32k |
| MTP n=9 | 55.7 | — | 32k |
| MTP n=9 + ngram-mod | 54.6 | 89.6-92.3 | 96k |
| MTP n=12 + ngram-mod | 59.4 | 94.7-98.5 | 96k |
| **… n-min 24, Q4_K_XL — this repo (champion)** | **59.7** | **148-163** | **96k (f16 KV)** |
| Q3_K_XL swap @ 128k (in 19:10Z, reverted 19:36Z) | 63-64 | 148-163 | 128k |
| Q2_K_XL (rejected — see findings) | 54.7 | 134-153 | 128k |

GTT on the champion: ~54.8/64GB (9.2GB margin). Note the trap this table hides: Q3
decodes faster than Q4 yet finishes identical correct tasks 35-50% slower — read the
time-per-task ladder in findings before picking a quant.

## Read the warm numbers honestly (three bands)

- **Cold c30 59.7 tok/s** (63-64 on the Q3@128k option) — what a one-shot query actually
  feels. ngram adds zero overhead when it misses; cold speed never regressed from stacking.
- **Warm c30 148-163 tok/s — a repetitive-bench artifact.** ngram speculation replays
  repeated structure across back-to-back identical runs. In production it only appears
  on genuinely repetitive output: agent tool loops and echoed-file rewrites (72-133 tok/s).
- **Real conversational traffic: 11-24 tok/s** — creative long-form ~11-14, a 2000-token
  essay ~12.4, structured/code ~29-40. That is memory-bandwidth physics for a 27B dense
  model on LPDDR5X; no flag fixes it. Anyone quoting 150+ tok/s for chat from this repo
  is misreading the bench.

First-token: 0.2-0.6s warm prefix, ~41s for a cold 16k-token prompt (PP kernel-bound at ~390 tok/s).

## Quickstart

1. `source components/strix-halo-env.sh` (HSA tuning for APUs: SDMA-off, XNACK on)
2. Serve with `components/qwen38-27b-halo-mtp.ini` flags on llama.cpp **b10435+**:

```bash
llama-server -m Qwen3.8-27B-UD-Q4_K_XL.gguf -ngl 99 -c 98304 \
  --flash-attn on --jinja --parallel 1 --threads 16 -fit off --no-ui \
  --spec-type draft-mtp,ngram-mod --spec-draft-n-max 12 --spec-ngram-mod-n-min 24 \
  --chat-template-kwargs '{"enable_thinking": false}'
```

3. Context-hungry option: the same flags with `UD-Q3_K_XL.gguf -c 131072`
   (63-64 cold / 148-163 warm, +33% context, 11.3GB margin) — but Q3's thinking runs
   ~2x more verbose on code/reasoning, so identical correct tasks complete 35-50%
   slower (7.6-7.7s vs 10.6-16.1s per task; tpt n=2). Choose it only when context, not
   latency, is the binding constraint.
4. Optional stanzas in the ini: creative profile (`--spec-draft-p-min 0.75`,
   +27% long-form at ~10% code cost), saturated (mtp-only A/B variant).

## What's inside

- `components/qwen38-27b-halo-mtp.ini` — the flagship profile + stanzas
- `components/strix-halo-env.sh` — ROCm/HIP env for gfx1151 APUs
- `components/AGENT-PREFIX.md` — byte-stable agent prefix doctrine (the real TTFT lever:
  warm prefix = 160x faster than cold)
- `components/bench/` — the bench suite (throughput, quality suite, TTFT, deep-ctx
  needle tests, rewrite-generator) plus the time-per-task instruments: `tpt-battery.py`
  (5 auto-graded tasks; the tool behind the quant-ladder verdict) and `tpt-style.py`
  (4-arm style A/B runner). Draft-acceptance metrics are read from the server
  journal (`journalctl -u qwen27 | grep acceptance`; warm c30 shows mean-len ~37.7,
  acceptance ~0.96).
- `docs/findings.md` — the negative results that saved us time (read before experimenting)

## Headline findings (all measured, ≥3 runs, quality-gated)

- **ngram-mod + MTP is the Strix Halo pattern**: ngram drafts cost zero bandwidth (prompt-
  derived) and stack losslessly (target-verified) on top of MTP heads. Full flag map,
  including the dead ends (n16, n-min below 24, p-split), is in findings.
- **The quant ladder is closed — on time-per-task, not decode tok/s**: Q3@128k decodes
  faster than Q4 (63-64 vs 59.7 cold c30) yet completes identical correct tasks 35-50%
  slower, because its thinking is ~2x more verbose; Q2 loses on both axes (dequant
  kernel cost exceeds the bandwidth saved) with 30-40% more verbose thinking. Decode
  tok/s is not task latency — token verbosity dominates. Full three-quant table in findings.
- **Neural drafters LOSE on this chip**: DSpark (1.36B) and DFlash drafters compete for the
  same memory bus as the 27B verifier — acceptance 0.91-0.94 still nets ~32 tok/s. They're
  compute-rich-GPU plays, not unified-memory plays.
- **Do NOT**: `GGML_HIP_ROCWMMA_FATTN=ON` (-41% prefill on gfx1151, and prefill is our
  weak spot), Vulkan for spec-decode workloads (~half throughput vs ROCm here), KV-quant
  q8 with FA (load failure on ROCm builds).
- **Context is nearly free**: ~2.1GB KV per 32k on this GQA model — 128k runs at zero
  speed cost. The Q3 revert was a verbosity verdict, not a capacity one.
- **Quality-gated at every step**: 6/6 suite on every promoted config (palindrome needs a
  1200-token budget — thinking eats fixed budgets; known artifact, recovers clean),
  43k-token deep-context needle probes show stacked spec == spec-off (no KV corruption),
  agentic soak 41/41 on the champion stack + 20/20 on the quant-ladder arms.

## Wave 2 — context engineering (the harness side)

Decode tok/s ran into memory-bandwidth physics, so the second arc attacked what the
model *reads* and how long it *thinks*. Measured tonight on the champion config;
single-run A/Bs carry variance — the sustained numbers are the headline.

- **Think-style steering (fused caveman+ponytail)**: a system prompt that steers the
  model's internal reasoning style. Sustained **-36% tokens / -33% task time**
  (n=3 vs n=8 baseline); a live single-run A/B showed **-51% wall** (single-run —
  treat as variance-colored, not the headline) (directional: measured on the full stacked config — stack delta, not style alone; re-baseline pending). Philosophy: caveman = terse reasoning
  ("finding / fix / next"); ponytail = lazy-senior-dev judgment — the
  does-it-need-to-exist → stdlib → one-line ladder, small fix beats big fix. Steering,
  never caps: the owner's standing veto on token-budget caps is a design feature —
  the model decides how little to think, not when it is forbidden from thinking.
- **Semantic navigation (`read_symbol` + `code_graph`)**: exploration task 48.6s /
  13,917B tool output / 53.5KB prompts (read-everything style) vs 22.6s / 276B /
  4.9KB — **-98% tool tokens** at roughly half the wall time (byte deltas
  -98%/-91% are deterministic and stand; wall-time delta is directional pending
  re-baseline after the tool-refusal fix).
- **Tool-result diet**: identical-output dedup stubs (**-66%** tokens on re-check
  loops), progressive disclosure with spill files, diff-hunk edit evidence with parse
  verdicts.
- **Context hygiene**: summary-node compaction past 300 events; parallel-tool
  advertisement so the model batches calls instead of serializing them.
- **Wave-regression law**: every wave lands with tests pinning the previous waves'
  gains — the in-repo suite grew 68→70 checks, including glass-contract tests born
  from a real crash.

Instruments: `components/bench/tpt-battery.py` and `tpt-style.py` reproduce all of
the above against any endpoint.

## Community results — post your numbers

Ran this stack (or a cousin of it) on your box? **PR or issue your row —
`components/bench/bench.sh` makes it one command** against a running server:
it runs the cold/warm c30, time-per-task battery, quality suite, and rewrite
bench, then prints a filled NUMBERS block you paste with your hardware line.

| Hardware | Backend/build | Config | Cold tok/s | Warm tok/s | Real-traffic band | Time-per-task | Source |
|---|---|---|---|---|---|---|---|
| AMD Ryzen AI Max+ 395 / Radeon 8060S (gfx1151, 64GB unified) | llama.cpp b10435-era (9d57ce4), ROCm/HIP | UD-Q4_K_XL @ 96k, `draft-mtp,ngram-mod` n12 / n-min 24, f16 KV | 59.7 (c30) | 148–163 (repetition-assisted — ngram replays repeat/pattern traffic) | prose 11–24, code 30–40 | 7.9–14.3 s/task, median 11.3 (5-task battery, n=3, thermal band) | [findings](docs/findings.md) |
| AMD Ryzen AI Max+ 395 / Radeon 8060S (gfx1151, 64GB unified) | llama.cpp b10435-era (9d57ce4), ROCm/HIP | UD-Q3_K_XL @ 128k, same spec stack | 63–64 (c30) | 148–163 (repetition-assisted) | — | 10.6–16.1 s/task (n=2) — ~2x more verbose thinking loses the clock | [findings](docs/findings.md) |

Label rules (kept in every row, ask the same of yours): warm c30 under ngram
is a repetition artifact — the label is part of the number; n>=3 per arm in
one thermal window; cold = first exposure.

**NUMBERS template** (bench.sh prints most of it filled in):

```text
hardware:
backend/build:            (llama.cpp commit/build, backend, OS)
config:                   (quant, ctx, spec flags, KV type)
cold tok/s:               (c30, first exposure)
warm tok/s:               (back-to-back repeats — label repetition-assisted)
real-traffic band:        (novel prose / code, same stack)
time-per-task:            (tpt-battery, n>=3, one thermal window)
source-link:
```

## Re-baseline update (2026-08-16)

Our own validity audit flagged two Wave-2 numbers as tainted, so every
directional number was re-measured on a fixed, fingerprinted harness
(liam-core 9fa358b; J-EV ledger fingerprint on every run; sequential runs).
The re-baseline cut both ways — one correction upgraded our claim, one
downgraded it — and both are recorded here. Everything above stands as
published history with its original labels (no-retract protocol). Source:
re-baseline experiment log (REBASELINE-RESULTS.md + VALIDITY-MAP.md,
2026-08-15/16 night).

- **Semantic reads (MUNCH): wall −65%, clean — bigger than we first claimed.**
  n=3/arm interleaved, 6/6 correct answers: wall median 27.9s → 9.8s
  (fingerprint 9fa358b). This supersedes the directional "roughly half the
  wall time" label in Wave 2 above. Byte deltas revise to −95% tool_result
  (5,182B → 277B) and −64% prompt_max (9,308B → 3,389B): W4 progressive
  disclosure truncates the vanilla arm's `read_file` to ~5KB, so these are
  the current-stack honest numbers (the earlier −98%/−91% were measured
  pre-W4). Vanilla needed 3-6 tool calls; the waved arm used exactly 2.
- **Style steering (STYLE) is regime-conditional — the −51% live A/B above is
  RETIRED.** Never cite it: re-measured harness-lane, n=15/arm interleaved at
  effort=low, the fused style measured **+65% wall** (median 10.7s vs 6.5s
  style-off) — the win inverts in that regime; correctness held 15/15 in both
  arms. The sustained −36%/−33% figure stands **only as a server-lane /
  default-(high-)effort number**: style pays where the model would overthink
  (the reasoning-heavy battery task ran −23% wall) and costs at low effort
  where there is nothing to cut. The production harness now routes style per
  session — high/xhigh-effort sessions only — rather than per turn, which
  also preserves the prompt cache. Regime note and per-regime verification
  method (battery) live in the sibling
  [context-kit](https://github.com/KyaniteLabs/context-kit) repo.
- **Time-per-task battery: upgraded from n=2 to n=3.** 7.9-14.3s per correct
  task (median 11.3; 15/15 correct; 189-281 tok/correct) — a
  thermal-dependent band; the warm-run value (7.9s) matches the old 7.6-7.7s
  label. The community table above already carries this band.
- **Fan daemon (measured in
  [evo-x2-ec](https://github.com/KyaniteLabs/evo-x2-ec)): −3.5 to −5.8°C
  peak, n=3.** Standardized ~105s probes with the daemon running: peak Tctl
  93/92/94°C vs the stock ledger band 97.5-97.8°C; fans at 100%. Labeled
  caveat: the stock arm was not re-run (daemon-untouched rule) — stock
  figures come from the 2026-08-15 ledger.
- Grader hardening shipped with the re-baseline: 6 FAIL→PASS flips, zero
  regressions across 139 re-graded sessions — pass counts published before
  this date may under-count.

## Credits

This recipe and every number in it stands on other people's work:

- **[ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)** (MIT) — the
  entire engine: MTP + ngram-mod speculative decoding, the GGUF runtime, and
  the b10435-era build every measurement here ran on. Nothing in this repo
  works without it.
- **[Unsloth](https://github.com/unslothai/unsloth)** (Apache-2.0 core; quants:
  [unsloth/Qwen3.8-27B-GGUF](https://huggingface.co/unsloth/Qwen3.8-27B-GGUF)) — the UD
  dynamic quants (Q4_K_XL champion, Q3/Q2 ladder arms) this repo benchmarks,
  used as-shipped with no re-quant. The dynamic-quant allocation scheme that
  makes Q4_K_XL the quality-per-token winner is their system.
- **[Qwen team](https://huggingface.co/Qwen/Qwen3.8-27B)** — Qwen3.8-27B
  (Apache-2.0), the model under test.
- **Unnamed public example (56 tok/s)** — best public figure we found for
  this class (a Qwen3.6-27B run at 56 tok/s). The original post was not
  re-located on 2026-08-15, so it stays unlabeled; no URL.
- **Skill authors whose thinking-style prompts Wave 2 fused and measured** —
  caveman origin: [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
  (skill MIT, (c) 2026 Julius Brussee; engine is separately BSL — unused here);
  a measured terse variant: [rolottr/caveman-skill](https://github.com/rolottr/caveman-skill)
  (MIT). Ponytail origin: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)
  (MIT, (c) 2026 DietrichGebert). The fused prompt and its measurements live in
  the sibling [context-kit](https://github.com/KyaniteLabs/context-kit) repo.
- **[nathanmarlor/strix-halo-fan-control](https://github.com/nathanmarlor/strix-halo-fan-control)**
  (MIT) — the EC fan daemon keeping this exact class of box cool; documented
  for the EVO-X2 chassis in the sibling [evo-x2-ec](https://github.com/KyaniteLabs/evo-x2-ec) repo.
- **Harness-side inspiration** — [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness)
  (MIT): plugin-first agent harness with an append-only session log and derived
  model context. [Pi](https://pi.dev/) ([earendil-works/pi](https://github.com/earendil-works/pi),
  MIT) — the coding-agent harness; configuration patterns from community setups.
  Detail in `context-kit`.

## License

MIT. Benchmark data collected on personally-owned hardware; your clocks will vary.
