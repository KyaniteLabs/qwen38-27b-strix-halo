#!/bin/bash
# strix-halo-env.sh — ROCm/HIP environment for llama.cpp serving on Strix Halo
# (gfx1151 / Ryzen AI Max 395, GTT-backed UMA). Sourced before llama-server.
#
# Validated in production 2026-08-15 (qwen27.service, NUCBox):
#   Qwen3.8-27B UD-Q3_K_XL, -ngl 99, FA on, draft-mtp,ngram-mod n=12 n-min 24, -c 131072
#   c30 63-64 cold / 148-161 ngram-warm tok/s · GTT 52.7/64GB · 11.3GB margin
#   (AM-era validation: UD-Q4_K_XL @ 98304, 59.7 cold / 148-158 warm, 8.2GB margin)
#
# Lines marked "optional" are race/hang guards from community reports; the
# production unit ships only the two mandatory lines (keep the diff small).

export HSA_ENABLE_SDMA=0   # MANDATORY: kernel-hang guard under GTT pressure on UMA
export HSA_XNACK=1         # MANDATORY: correct memory-fault semantics for GTT pages

# Optional hardening (NOT in production — add only if chasing races/hangs):
# export HIP_LAUNCH_BLOCKING=1   # serialize launches; debug only, costs perf
# export AMD_LOG_LEVEL=3         # verbose HSA logging for triage

# Do NOT set: GGML_HIP_ROCWMMA_FATTN build flag — see STACK-ROADMAP item 3
# correction: -41% prefill regression on gfx1151 (llama.cpp #24437).
