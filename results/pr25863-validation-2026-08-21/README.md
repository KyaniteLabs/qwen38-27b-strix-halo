# PR 25863 validated on gfx1151 — the #26209 fix candidate matches our fixed build (2026-08-21)

Paired battery: llama.cpp PR 25863 ("ggml-cuda: avoid ROCm_Host compute on HIP
integrated GPUs", fdc1260e9) vs our c7d8722-reverted dflash build (46aa138f3).
Identical model (Qwen3.8-27B Q4_K_XL), identical flags (262144 ctx, q4_0 KV,
mmproj-F16, cache-reuse 256), identical fixtures — the binary was the only delta.
Champion stopped for the battery, restored after (q4_0 readback). Balanced pmode.
Battery wall: ~10 min. Pre-dispatch critic round applied (3 blockers caught
pre-fire: undefined restore function, dead tokenize route, verdict gating).

## Results (both arms complete; verdict completion-gated)

| class | PR 25863 build | dflash control (our fix) |
|---|---|---|
| vision-real (6 real-UI screenshots) | 6/6 HIT, answers byte-identical | 6/6 HIT |
| deep-control (10k/12k/16k needles at 50%) | 3/3 HIT exact, zero attractors, fr=stop | 3/3 HIT exact |
| prompt token counts (fixture identity) | 10013 / 12018 / 16015 | 10013 / 12018 / 16015 (identical) |

Every vision answer identical across arms (Beta, 312, simon@kyanitelabs.tech,
503, music-library, up). Every deep needle retrieved exactly in both arms
(OBSIDIAN-6612-KILO, AMETHYST-2049-LIMA, PLATINUM-8830-NOVA).

**VERDICT-CLASS: PR25863 VALIDATED ON GFX1151** — the upstream fix candidate
behaves exactly like our revert on the hardware class that exhibited the bug
(#26209: NaN logits >2k-token prompts on integrated GPUs, bisected to c7d8722
host buffers). This satisfies the validation prerequisite for the #26209
upstream-contribution gate: our repro recipe + this paired evidence are ready
to attach upstream (contribution lane per gate; auto-fire authority per
upstream-contribution-gate policy).

Labels (P13): accuracy-class verdicts (power-invariant); walls not verdict
inputs; n=6 vision (pilot) + n=3 deep per arm; token counts server-verified.

## Raw
- pr25863-battery-driver.log — full driver (gates, arms, verdict, restores)
- pr25863-vision-{pr25863,dflash}.log — 6/6 both arms
- pr25863-deep-{pr25863,dflash}.log — 3/3 both arms
- pr25863-server-{pr25863,dflash}.log — per-launch server logs
- Instruments: qwen27-nucbox-stack components/exp-2026-08-19/pr25863-battery.sh,
  deep-control.py, test-pr25863-battery.sh (28/28)
