# Qwen3.8-27B on Strix Halo — tuned serving profile

First-mover measured configuration for serving **Qwen3.8-27B** (Apache-2.0, released 2026-08-14)
on **AMD Strix Halo** (Ryzen AI Max+ 395, Radeon 8060S, unified LPDDR5X, GTT 64GB) with
**llama.cpp** — speculation-stacked to the practical frontier of this silicon.

## The numbers (measured 2026-08-15, single box, reproducible via `components/bench/`)

| Config | Cold tok/s | Warm/repeat tok/s | Context |
|---|---|---|---|
| MTP n=2 (day-0 default) | 22 | 25 | 16k |
| MTP n=6 | 32.7 | — | 32k |
| **MTP n=12 + ngram-mod (n-min 24) — this repo** | **59.7** | **148-158** | **96k (f16 KV)** |

Warm = ngram speculation exploiting repetition (structured output, file rewrites, agent tool loops).
Creative/unstructured prose rides 12-35 tok/s (bandwidth physics; see findings).
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

3. Optional stanzas in the ini: creative profile (`--spec-draft-p-min 0.75`, +27% long-form),
   dual-slot (2x49k), 128k (knife-edge GTT margin).

## What's inside

- `components/qwen38-27b-halo-mtp.ini` — the flagship profile + stanzas
- `components/strix-halo-env.sh` — ROCm/HIP env for gfx1151 APUs
- `components/AGENT-PREFIX.md` — byte-stable agent prefix doctrine (the real TTFT lever:
  warm prefix = 160x faster than cold)
- `components/bench/` — the full bench suite (throughput, quality suite, TTFT, deep-ctx
  needle tests, rewrite-generator)
- `docs/findings.md` — the negative results that saved us time (read before experimenting)

## Headline findings (all measured, ≥3 runs, quality-gated)

- **ngram-mod + MTP is the Strix Halo pattern**: ngram drafts cost zero bandwidth (prompt-
  derived) and stack losslessly (target-verified) on top of MTP heads.
- **Neural drafters LOSE on this chip**: DSpark (1.36B) and DFlash drafters compete for the
  same memory bus as the 27B verifier — acceptance 0.91-0.94 still nets ~32 tok/s. They're
  compute-rich-GPU plays, not unified-memory plays.
- **Do NOT**: `GGML_HIP_ROCWMMA_FATTN=ON` (-41% prefill on gfx1151), Vulkan for spec-decode
  workloads (~half throughput vs ROCm here), KV-quant q8 with FA (load failure on ROCm builds).
- **Context is nearly free**: ~2.1GB KV per 32k on this GQA model — 96k runs at zero speed cost.

## License

MIT. Benchmark data collected on personally-owned hardware; your clocks will vary.
