# Findings: what we measured so you don't have to

## Neural drafters lose on unified memory (2026-08-15, 4-arm A/B, mirror-validated)
- DSpark 1.36B BF16 drafter (RadixArk, GGUF converted via patched convert_hf_to_gguf DSpark path): 32.6 cold / 150.9 warm vs champion 59.6/157.8-158.3 — loses everywhere.
- Mechanism: drafter forward pass costs ~2.7GB reads on the SAME bus as the 27B verify pass; acceptance 0.91 x 7-len still nets ~32 tok/s. ngram drafts are free (prompt-derived) with len 37.7.
- Cross-gen DFlash (z-lab Qwen3.6 drafter, CPU-drafted, vs 3.8 target): 79.1 cold (+32% over champion cold) but acceptance 0.063 on creative; no warm value. Cold-start-helper curiosity only.

## Build/backend traps on gfx1151
- GGML_HIP_ROCWMMA_FATTN=ON: -41% prefill (llama.cpp #24437)
- Vulkan RADV: ~half throughput on spec-decode workloads vs ROCm
- KV-quant q8_0 + FA: load failure on ROCm builds of this era; K-only loads but saves ~1GB at -1.6% (pointless — context is nearly free)

## Quality gates used
- 6-prompt fixed suite (riddle/code/precision/explain/persona/multistep), >=3 bench runs, draft-acceptance from server journal, deep-context needle probes at 43k (spec-on identical to spec-off = no KV corruption).
