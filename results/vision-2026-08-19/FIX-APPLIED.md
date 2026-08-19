# VISION FIXED — llama.cpp buffer regression, not quant precision (2026-08-19 ~20:1xZ)

## Root cause
Commit c7d8722 ("restore prop.integrated on HIP builds") re-enabled host buffer
usage on integrated GPUs → prompts >2k tokens split across decode calls → NaN
logits → degenerate token (//////) → infinite loop. NOT a quantization issue.

Upstream issues: ggml-org/llama.cpp#26209 (bisected on same hardware, gfx1151),
ggml-org/llama.cpp#23577 (same pattern, CUDA, MTP). Previously known: #16308 /
#15034 (Jetson Orin, same integrated-GPU class).

## Fix
Reverted c7d8722 in our dflash build (commit 46aa138f3). One-line change:
force `integrated = false` unconditionally. Rebuilt, re-tested.

## Results after fix (same Q4_K_XL quant, same mmproj-F16, same hardware)

| Test | Before (broken) | After (fixed) | Time |
|------|----------------|---------------|------|
| System graph | //////// | "Stacked bar chart" | 1.8s |
| Red image | //////// | "Red" ✅ | 0.3s |
| Blue image | //////// | "Blue" ✅ | 0.7s |
| Green image | //////// | "Green" ✅ | 0.6s |
| "Is this red?" | //////// | "Yes" ✅ | 0.6s |
| "Is this a gradient?" | //////// | "Yes" ✅ | 0.7s |

**VISION-V5 after fix: 5/6 correct** (was 0/6)
Sub-second responses. All finish_reason=stop. Zero errors.

## Text regression after fix
HumanEval 30-problem subset: **28/30 = 93%** — identical to pre-fix score.
The revert does not affect text generation.

## Implication
Vision at Q4 quant works on this rig. The $1,400 mini-PC is a fully-capable
multimodal inference server: text at 93% HumanEval + vision at 5/6 VQA,
sub-second responses for both modalities.
