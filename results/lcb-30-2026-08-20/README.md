# LiveCodeBench-30 — stratified subset on the champion (2026-08-20)

## Question
How does the Q4 champion score on a harder, contamination-light coding bench
than HumanEval? Card anchor: Qwen3.8-27B official LCB 90.3 (bf16, official
harness, full set, private tests) — NOT comparable to our instrument, band-check only.

## Conditions (pre-registered; all numbers carry these labels)
- Source: livecodebench/code_generation_lite **test6** (v6, 175 problems, ~May 2025
  contests). Subset: 10 easy / 10 medium / 10 hard, seed 20260820.
- Serving: Q4_K_XL @262k, q4_0 KV, MTP+ngram capped, c7d8722-reverted build,
  temp 0, thinking off unless stated, shared-slot (another lane's API traffic
  interleaved; walls inflated, scores unaffected).
- Grading: PUBLIC cases only (lite withholds private), ≤20 cases/problem,
  early-exit-fail; stdin = strip-compare stdout; functional = JSON args per
  line into the entry method (grader bugs found + fixed mid-experiment — see
  Instrument saga).

## Results — three arms

| Arm | Score | Notes |
|---|---|---|
| A: max 2048, thinking off | 13/30 raw, **14/30** after grader correction | 15 problems failed on LENGTH (prose, no code block); 3817 flipped FAIL→PASS when the grader's functional bug was fixed |
| B: max 4096, thinking off (15 length-failures retried) | **0/15** | Raising the cap recovered nothing — with thinking off the model reasons in visible PROSE and 4096 tokens still go to explanation, not code |
| C: thinking ON budget 2048 + max 6144 (same 15) | **5/15** | Reasoning moves to its own channel; code completes; 5 pass (4 medium + 1 hard), 10 genuine case-mismatches with complete code |

**Composite best-of-instrument: 19/30 = 63%** (difficulty split: easy 9/10,
medium 8/10, hard 2/10).

## Findings
1. **Thinking pays exactly where tasks are hard.** On HumanEval-30 thinking
   bought nothing at any budget (row-identical 28/30). Here it rescued 5/15
   problems that no-thinking could not even produce code for at 4096 tokens.
   With thinking off, hard problems trigger visible chain-of-thought IN THE
   CONTENT CHANNEL (diagnostic generation saved in `gen/`), starving the code.
   Product routing rule: hard-problem lane → thinking ON with budget.
2. **The champion's frontier on contest-hard problems is real but thin** —
   2/10 hard vs 9/10 easy. Card's 90.3 is a different instrument; within OUR
   instruments the gradient is the story.
3. **Instrument saga (documented for reproducibility):** the functional grader
   initially fed model code as stdin while executing only the starter+wrapper
   (model code never ran for functional problems) — caught by audit, fixed;
   one problem (3817) flipped to PASS on re-grade with its saved generation.
   3723 remains a genuine fail (mixed-protocol output that prints nothing).
   Dry-run lesson recorded: dry-runs must exercise EVERY grading path.

## Raw
- `lcb-30-results.log` — arm A (30 rows + sentinel)
- `lcb-30-tok4096-results.log` — arm B
- `lcb-30-think2048-results.log` — arm C (think-chars per problem)
- `gen/`, `gen-think/` — saved generations (diagnostic + thinking arm)
- `audit-*.py` — saved generations used for the grader audit
