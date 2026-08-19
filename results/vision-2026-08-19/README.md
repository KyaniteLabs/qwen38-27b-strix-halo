# Vision battery v5 — CORRECTED: llama.cpp buffer regression, not quant (2026-08-19)

## Finding (corrected same day)
Qwen3.8-27B at Q4_K_XL + mmproj-F16.gguf: all 6 vision questions returned
repeated slash characters (`//////...`) with finish_reason=length, think=0ch.

**Initial diagnosis (WRONG):** Q4-quantized language model cannot process F16
vision embeddings; vision needs Q8+. Falsified — the quant was never the problem.

**Actual root cause:** llama.cpp commit c7d8722 re-enables host buffers on
integrated GPUs → NaN logits on prompts >2k tokens split across decode calls
→ degenerate token loop. Vision prompts cross that threshold via image tokens
(image embeddings alone exceed ~2k tokens), so EVERY vision request degenerated.
Text prompts under 2k tokens stayed clean — which is why text benchmarks
passed on the same broken binary.

Fixed by reverting c7d8722 (see FIX-APPLIED.md). Upstream:
ggml-org/llama.cpp#26209 (bisected on same hardware class, gfx1151),
#23577, previously #16308/#15034 (Jetson Orin, same integrated-GPU class).

## After the revert (same quant, same mmproj, only delta = the revert)
- `vision-v5-after-fix.log`: **5/6 correct**, sub-second responses, all
  finish_reason=stop. The one miss (V5-1) is a grading miss — the answer
  "Stacked bar chart" was a reasonable description of the system graph.
- Text regression (`../agentic-bench-2026-08-19/bench-post-fix-regression.log`):
  HumanEval 28/30 = 93%, same two failing problems as pre-revert.

## Raw logs
- `vision-v5-results.log` — BEFORE the revert: 0/6, all `//////`, fr=length
- `vision-v5-after-fix.log` — AFTER the revert: 5/6, fr=stop

## Conditions
GMKtec EVO-X2 ($1,400), Ryzen AI Max+ 395, 96GB unified. Q4_K_XL + q4_0 KV.
MTP n12 + ngram capped. llama.cpp dflash fork (9d57ce4 + #27083 + c7d8722
revert, commit 46aa138f3). PIL-generated JPEGs. 6 questions × 300 max tokens.

## Thinking ON (added 2026-08-19 ~21:1xZ)
`vision-v5-think-results.log`: same 6 questions with enable_thinking true +
reasoning_budget 512. **5/6 — same score, same single miss (V5-1), 3.3–12.1s
per answer vs 0.3–1.8s thinking-off (4–12x slower).** The miss persists after
664 chars of reasoning — a chart-interpretation disagreement, not retrieval.
Verdict: VQA on this champion routes thinking-OFF.
