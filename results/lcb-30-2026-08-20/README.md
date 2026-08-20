# LiveCodeBench-30 — stratified subset on the champion (2026-08-20)

## Question
How does the Q4 champion score on a harder coding bench than HumanEval?
Card anchor: Qwen3.8-27B official LCB 90.3 (bf16, official harness, full set,
private tests) — NOT comparable to our instrument, band-check only.

## Conditions (pre-registered; all numbers carry these labels)
- Source: livecodebench/code_generation_lite **test6** (v6, 175 problems, ~May
  2025 contests). Subset: 10 easy / 10 medium / 10 hard, seed 20260820
  (deterministic; reproduces via `verify_claims.py`).
- **Contamination caveat (cuts AGAINST cleanliness):** the v6 problem window
  predates this model's training — in-training exposure is possible, so this
  score is if anything INFLATED vs a clean window. The card's own 90.3 shares
  this property on its window. The hard-split finding is conservative-safe
  (contamination would inflate it too).
- Serving: Q4_K_XL @262k, q4_0 KV, MTP+ngram capped, c7d8722-reverted build,
  temp 0, thinking off unless stated, shared-slot (another lane's API traffic
  interleaved; walls inflated, scores unaffected).
- Grading: PUBLIC cases only (lite withholds private), ≤20 cases/problem,
  early-exit-fail; stdin = strip-compare stdout; functional = JSON args
  per line into the entry method, model `__main__` guards stripped.

## Results — three arms

| Arm | Score | Notes |
|---|---|---|
| A: max 2048, thinking off | 13/30 raw; **15/30** after grader correction | 15 problems failed on LENGTH (prose, no code block); both fr=stop functional "fails" (3817, 3723) flipped to PASS under the fixed grader — see saga |
| B: max 4096, thinking off (15 length-failures retried) | **0/15** | Raising the cap recovered nothing — with thinking off the model reasons in visible PROSE and 4096 tokens still go to explanation, not code |
| C: thinking ON budget 2048 + max 6144 (same 15) | **5/15** | Reasoning moves to its own channel; code completes; 5 pass (4 medium + 1 hard), 10 genuine case-mismatches with complete code |

**Composite best-per-problem across the instrument's arms: 20/30 = 67%**
(difficulty split: easy 10/10, medium 8/10, hard 2/10). This is NOT a
single-config leaderboard number — it is each problem's best result across
the three labeled conditions above.

## Findings
1. **Thinking pays exactly where tasks are hard.** On HumanEval-30 thinking
   bought nothing at any budget (row-identical 28/30). Here it rescued 5/15
   problems that no-thinking could not even produce code for at 4096 tokens.
   With thinking off, hard problems trigger visible chain-of-thought IN THE
   CONTENT CHANNEL (diagnostic generation in `gen/`), starving the code.
   Routing rule: hard-problem lane → thinking ON with budget.
2. **The champion's contest-hard frontier is thin** — 2/10 hard vs 10/10
   easy, even with contamination possible in the model's favor.
3. **Instrument saga (documented for reproducibility):** the functional
   grader initially fed model code as stdin while executing only the
   starter+wrapper (model code never ran for functional problems). Caught by
   audit; fixing it flipped BOTH fr=stop functional failures to PASS — the
   model's solutions were correct, the grader was wrong. The guard-strip fix
   (3723's class method was right; its self-written `__main__` guard was the
   broken part) surfaced during the final triple-check, which is why the
   composite reads 20/30 and not the originally reported 19/30.

## Verification
- `verify_claims.py` recomputes every headline number from the raw logs (row
  counts, sentinels, arm scores, set identities, corrected composite,
  difficulty split, subset integrity). Exit 0.
- `probe_blindspots.py` closes three gate blind spots: (P1) zero public cases
  have empty expected outputs (no vacuous-pass class); (P2) all 15 arm-C
  verdicts independently re-executed from the saved generations — 15/15 agree;
  (P3) sampling uncertainty made explicit: **20/30 = 67%, Wilson 95% CI
  [49%, 81%] — n=30, read the CI, not the point estimate.**
- Grading environment: python3 on the nucbox (3.12); the shipped
  `lcb-bench.py` is the exact canonical grader (byte-verified against the box
  copy after a stale-version mixup was caught and fixed during the gate).
- Arm A/B generations were not saved (fixed for later arms); arm A was
  re-fired with saves as a reproduction check (`lcb-30-arepro-results.log`,
  `gen-arepro/`): **14/30 vs the original 13/30, 25/30 per-problem agreement.**
  The 5 flips: 3723/3817/3793 FAIL→PASS (independently reproducing the grader
  corrections), abc390_c/abc398_g PASS→FAIL (marginal truncation-edge passes
  — pass-capable but run-dependent). Composite unchanged at 20/30 (union of
  demonstrated passes). takeaway: single-run verdicts on this stack carry a
  ~±2-problem noise floor even at temp 0; the composite framing absorbs it.

## Raw
- `lcb-30-results.log` — arm A (30 rows + sentinel)
- `lcb-30-tok4096-results.log` — arm B
- `lcb-30-think2048-results.log` — arm C (think-chars per problem)
- `gen/`, `gen-think/` — saved generations (diagnostic + thinking arm)
- `audit-3723-code.py`, `audit-3817-code.py` — generations used for the audit
- `lcb-bench.py` — the exact harness (incl. all grader fixes)
- `lcb-subset30.jsonl` + `subset_ids.txt` — the exact 30 problems (full pool:
  HF `livecodebench/code_generation_lite` test6, seed 20260820, 10/10/10)
