# Findings: what we measured so you don't have to

## The quant ladder is closed — on time-per-task, not decode tok/s (2026-08-15 evening)
Q3@128k was swapped into production at 19:10Z (faster decode, +33% context, 6/6 suite)
and REVERTED at 19:36Z after a time-per-task battery (5 auto-graded tasks, wall-clock +
completion tokens) showed thinking verbosity, not decode speed, decides task latency.

| | Q4_K_XL @ 96k (champion) | Q3_K_XL @ 128k | Q2_K_XL @ 128k |
|---|---|---|---|
| c30 tok/s (cold / warm) | 59.7 / 148-158 | 63-64 / 148-161 | 54.7 / 134-153 |
| GTT margin | 9.2GB | 11.3GB | 13.8GB |
| quality suite | 6/6 | 6/6 | 5/6 |
| agentic soak | 41/41 | — | 20/20 |
| time-per-task (s @ tokens) | 7.6-7.7 @ ~170 | 10.6-16.1 @ 238-302 | not run (rejected on speed) |
| code-task tokens, 3 runs | 402 / 450 | 705 / 740 / 994 | zero content @ 500 budget |
| draft acceptance (novel traffic) | 0.345 | 0.492 | 0.478 |

- Q3's thinking runs ~2x more verbose on code/reasoning, so Q4 completes identical
  correct tasks 35-50% faster despite lower decode tok/s. **Decode tok/s is not task
  latency; token verbosity dominates** — measure wall-clock per completed task, always.
- Acceptance-collapse hypothesis FALSIFIED: Q3 novel-traffic acceptance (0.492) is
  HIGHER than Q4's (0.345). The revert is purely a verbosity/latency verdict, not a
  spec-decode failure — Q3 spec-decodes beautifully and still loses the clock.
- Q2 additionally loses on raw decode (Q2_K dequant kernels cost more than the 2.6GB
  bandwidth saved) and thinks 30-40% more: zero content at a 500-token budget (thinking
  1958 chars), full correct output at 1200; strict-JSON probe perfect. Gate passed
  formally, premise failed materially.
- Q3 also passed 6/6 (palindrome needs the 1200-token budget; recovers `finish=stop`),
  so this is NOT a quality cliff — it is a latency economics result.
- Champion: Q4_K_XL @ 98304, restored and verified on production 19:36Z.
  Q3@128k remains the documented context-hungry option when latency is not binding.

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
