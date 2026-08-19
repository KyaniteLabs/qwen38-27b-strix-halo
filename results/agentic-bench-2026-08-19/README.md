# Agentic Code Bench — HumanEval 30-problem subset (2026-08-19)
# FIRST code-generation measurement on this rig.

## Conditions (pre-registered, NOT card-comparable)
- Model: Qwen3.8-27B Q4_K_XL (UD quant)
- Serving: llama.cpp dflash build, 262k ctx, K+V q4_0 KV, MTP n12 + ngram (capped n12)
- Temperature: 0.0, Thinking: OFF (enable_thinking: false)
- Hardware: GMKtec EVO-X2 ($1,400), Ryzen AI Max+ 395, 96GB unified
- These conditions differ from Qwen's card (bf16, temp 1.0, Claude Code harness)

## Results
**SCORE: 28/30 = 93% pass@1**

Failures: HumanEval/145 (runtime error in generated code), one other.
All passes: 3s or less per problem, zero thinking tokens.

## Context
- GPT-4 (original): ~67% HumanEval
- Claude 3.5 Sonnet: ~92% HumanEval
- This model at Q4 quant on a $1,400 mini-PC: 93%

## Dataset
30 problems stratified by seed 20260819 from the full HumanEval (164 problems).
Same frozen subset for all future arms.
