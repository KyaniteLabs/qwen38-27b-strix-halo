# Findings: what we measured so you don't have to

## The quant knee is Q3_K_XL (2026-08-15 evening, ladder closed)
- Q4_K_XL @ 96k: 59.7 cold / 148-158 warm, GTT margin 8.2GB (the AM champion).
- Q3_K_XL @ 128k: 63.0-64.0 cold / 148.0-161.6 warm, margin 11.3GB — faster AND 4GB
  lighter AND +33% context. Quality 6/6 (palindrome truncated at a 500-token budget —
  thinking ate 1678 chars; full working output at 1200, `finish=stop`). Swapped into
  production 19:10Z. Dequant cost < bandwidth saved: Q3 weights are simply less traffic.
- Q2_K_XL @ 128k: 54.7 cold / 134.3-152.6 warm — SLOWER than both Q3 and Q4 despite
  2.6GB less weights (Q2_K dequant kernels cost more than the bandwidth saved; negative
  return on the very axis compression is supposed to win). Margin only +2.4GB vs Q3.
  Reasoning 30-40% more verbose for the same problems: code prompt emitted ZERO content
  at a 500-token budget (thinking 1958 chars), recovers at 1200; strict-JSON probe
  perfect; 20-round agentic soak 20/20 clean. Gate passed formally, premise failed
  materially — REJECTED, quant lane closed.

## Flag map: dead ends measured once, don't re-run (2026-08-15)
- `--spec-draft-n-max 16`: code regresses to 21.3 tok/s (deep-draft waste returns). n12 is the peak.
- `--spec-ngram-mod-n-min 12`: identical to 24 (warm 146.6/158.0 vs 148.0/157.6, mean-len 37.67 both) — 24 is the plateau.
- `--spec-draft-p-split 0`: zero effect (94.3/99.4 vs 94.7/98.5).
- `-t 12` vs `-t 16`: identical — CPU threads are not the bottleneck at full GPU offload.
- `-ub 2048`: prefill WORSE (45.2-46.3s vs 40.6-41.4s on a 16k prompt); `-ub 1024` identical to default.
- `--cache-reuse 256`: no-op on this build ("not supported by this context" at load).
- `--parallel 2` @ 96k: works (2x49k slots, same GTT, single-stream unchanged) but halves
  per-conversation context — a serving option, not a default.
- `--spec-draft-p-min 0.75`: NOT a default (c30 -2%, code -10%) but story +27% / acceptance
  0.21→0.74 on creative long-form — shipped as the ini's creative stanza.

## Neural drafters lose on unified memory (2026-08-15, 4-arm A/B, mirror-validated)
- DSpark 1.36B BF16 drafter (RadixArk, GGUF converted via patched convert_hf_to_gguf DSpark path): 32.6 cold / 150.9 warm vs champion 59.6/157.8-158.3 — loses everywhere.
- Mechanism: drafter forward pass costs ~2.7GB reads on the SAME bus as the 27B verify pass; acceptance 0.91 x 7-len still nets ~32 tok/s. ngram drafts are free (prompt-derived) with len 37.7.
- Cross-gen DFlash (z-lab Qwen3.6 drafter, CPU-drafted, vs 3.8 target): 79.1 cold (+32% over champion cold) but acceptance 0.063 on creative; no warm value. Cold-start-helper curiosity only.

## Build/backend traps on gfx1151
- GGML_HIP_ROCWMMA_FATTN=ON: -41% prefill (llama.cpp #24437); the decode-at-depth gains don't matter for us because prefill is the weak spot — rebuild cancelled.
- Vulkan RADV (same 9d57ce4 source, stacked n12/96k): cold 16k-prompt TTFT 55.5-56.1s vs ROCm 40.6-41.4s (-36% PP), TG c30 48.8/50.2 vs 94.7-98.5 (~half), code 15.9 vs 30-40, story 5.3 vs ~12. Community "Vulkan wins on gfx1151" does not hold for spec-decode workloads on this box.
- KV-quant q8_0 + FA: load failure on ROCm builds of this era; K-only loads but saves ~1GB at -1.6% (pointless — context is nearly free).
- Loading a second model alongside a resident one OOMs GTT (55.8 + 12.3 > 64GB): quant-ladder tests require stopping production first.

## Quality gates used
- 6-prompt fixed suite (riddle/code/precision/explain/persona/multistep), >=3 bench runs, draft-acceptance from server journal, deep-context needle probes at 43k (spec-on identical to spec-off = no KV corruption), agentic tool-loop soak (41/41 on the champion stack, 20/20 on quant-ladder arms).
- Thermal note: sustained ~4s-cadence agent load rides the GPU edge at 92C (boost-throttle operating point, recovers 92→61C in 45s; no heat soak).
