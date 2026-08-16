# Qwen3.8-27B on Strix Halo — tuned serving profile

Fully measured configuration for serving **Qwen3.8-27B** (Apache-2.0, released 2026-08-14)
on **AMD Strix Halo** (Ryzen AI Max+ 395, Radeon 8060S, unified LPDDR5X, GTT 64GB) with
**llama.cpp** — speculation-stacked to the practical frontier of this silicon.

Current champion (production, restored 2026-08-15 19:36Z): **UD-Q4_K_XL @ 96k context**.
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

## License

MIT. Benchmark data collected on personally-owned hardware; your clocks will vary.
