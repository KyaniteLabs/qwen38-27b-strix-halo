# Qwen3.8-27B on Strix Halo — tuned serving profile

Fully measured configuration for serving **Qwen3.8-27B** (Apache-2.0, released 2026-08-14)
on **AMD Strix Halo** (Ryzen AI Max+ 395, Radeon 8060S, unified LPDDR5X, GTT 64GB) with
**llama.cpp** — speculation-stacked to the practical frontier of this silicon.

Current champion (production since 2026-08-15 19:10Z): **UD-Q3_K_XL @ 128k context**.
The AM publication ran UD-Q4_K_XL @ 96k; the quant ladder closed same day — see findings.

## The numbers (measured 2026-08-15, single box, reproducible via `components/bench/`)

count-to-30 bench, cold = first exposure, warm = back-to-back repeats:

| Config | Cold tok/s | Warm/repeat tok/s | Context |
|---|---|---|---|
| MTP n=2 (day-0 default) | 22 | 25 | 16k |
| MTP n=6 (mission baseline) | 32.7 | — | 32k |
| MTP n=9 | 55.7 | — | 32k |
| MTP n=9 + ngram-mod | 54.6 | 89.6-92.3 | 96k |
| MTP n=12 + ngram-mod | 59.4 | 94.7-98.5 | 96k |
| … n-min 24 — Q4_K_XL champion (AM version) | 59.7 | 148-158 | 96k (f16 KV) |
| **… swapped to Q3_K_XL @ 128k — this repo** | **63-64** | **148-161** | **128k (f16 KV)** |
| Q2_K_XL (rejected — see findings) | 54.7 | 134-153 | 128k |

GTT after swap: 52.7/64GB (11.3GB margin; Q4@96k ran 8.2GB).

## Read the warm numbers honestly (three bands)

- **Cold c30 63-64 tok/s** — what a one-shot query actually feels. ngram adds zero
  overhead when it misses; cold speed never regressed from stacking.
- **Warm c30 148-161 tok/s — a repetitive-bench artifact.** ngram speculation replays
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
llama-server -m Qwen3.8-27B-UD-Q3_K_XL.gguf -ngl 99 -c 131072 \
  --flash-attn on --jinja --parallel 1 --threads 16 -fit off --no-ui \
  --spec-type draft-mtp,ngram-mod --spec-draft-n-max 12 --spec-ngram-mod-n-min 24 \
  --chat-template-kwargs '{"enable_thinking": false}'
```

3. Higher-fidelity fallback: the same flags with `UD-Q4_K_XL.gguf -c 98304`
   (59.7 / 148-158; 8.2GB GTT margin).
4. Optional stanzas in the ini: creative profile (`--spec-draft-p-min 0.75`,
   +27% long-form at ~10% code cost), saturated (mtp-only A/B variant).

## What's inside

- `components/qwen38-27b-halo-mtp.ini` — the flagship profile + stanzas
- `components/strix-halo-env.sh` — ROCm/HIP env for gfx1151 APUs
- `components/AGENT-PREFIX.md` — byte-stable agent prefix doctrine (the real TTFT lever:
  warm prefix = 160x faster than cold)
- `components/bench/` — the bench suite (throughput, quality suite, TTFT, deep-ctx
  needle tests, rewrite-generator). Draft-acceptance metrics are read from the server
  journal (`journalctl -u qwen27 | grep acceptance`; warm c30 shows mean-len ~37.7,
  acceptance ~0.96).
- `docs/findings.md` — the negative results that saved us time (read before experimenting)

## Headline findings (all measured, ≥3 runs, quality-gated)

- **ngram-mod + MTP is the Strix Halo pattern**: ngram drafts cost zero bandwidth (prompt-
  derived) and stack losslessly (target-verified) on top of MTP heads. Full flag map,
  including the dead ends (n16, n-min below 24, p-split), is in findings.
- **The quant knee is Q3_K_XL**: Q4 → Q3 is faster AND 4GB lighter (less weight traffic),
  funding 128k context at an 11.3GB margin; Q2_K is *slower* than both (dequant kernel
  cost exceeds the bandwidth saved) with 30-40% more verbose thinking. Ladder closed.
- **Neural drafters LOSE on this chip**: DSpark (1.36B) and DFlash drafters compete for the
  same memory bus as the 27B verifier — acceptance 0.91-0.94 still nets ~32 tok/s. They're
  compute-rich-GPU plays, not unified-memory plays.
- **Do NOT**: `GGML_HIP_ROCWMMA_FATTN=ON` (-41% prefill on gfx1151, and prefill is our
  weak spot), Vulkan for spec-decode workloads (~half throughput vs ROCm here), KV-quant
  q8 with FA (load failure on ROCm builds).
- **Context is nearly free**: ~2.1GB KV per 32k on this GQA model — 128k runs at zero
  speed cost. That is why the Q3 swap bought context instead of speed.
- **Quality-gated at every step**: 6/6 suite on the Q3@128k champion (palindrome needs a
  1200-token budget — thinking eats fixed budgets; known artifact, recovers clean),
  43k-token deep-context needle probes show stacked spec == spec-off (no KV corruption),
  agentic soak 41/41 on the champion stack + 20/20 on the quant-ladder arms.

## License

MIT. Benchmark data collected on personally-owned hardware; your clocks will vary.
