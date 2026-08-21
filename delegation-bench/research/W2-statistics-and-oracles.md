# RESEARCH-BENCH-W2 — D2 Statistics + D3 Agentic Oracles (delegation bench v2)

- Worker: independent research worker (KyaniteLabs research lane)
- Date: 2026-08-21 (research window; sources span 1934–2026, cited with dates)
- Input: `DELEGATION-BENCH-DESIGN-2026-08-21.md` (v2, incorporating all 15 findings of the Sol-high adversarial audit)
- Scope: D2 (recommended n + interval methods for pass-rate claims; clustered trials; adaptive/sequential screen-n5-then-escalate; multiplicity) and D3 (documented gaming of "tests pass" oracles + accepted mitigations), ZH + EN venues, China-first.
- Convention per cell/section: named sources + dates; CONSENSUS vs SINGLE-SOURCE; verdict for v2: **ADOPT** / **VERIFY-CHANGE** / **NO-PRECEDENT**.

---

## 0. Reading the design's statistical claims (the object under review)

v2's quantitative core (section 5, 6, 8):

| Element | v2 rule |
|---|---|
| Screen | n=5 independent trials: 5/5 → escalate to n=15; 3–4/5 → YELLOW (pending confirmation run); ≤2/5 → RED |
| Full | n=15: 15/15 → CAPABILITY-GREEN candidate (confirmation run required); 13–14 → YELLOW; ≤12 → RED |
| Confirmation | GREEN cells face an UNTOUCHED confirmation run on fresh fixtures before entering the operator card |
| Clusters | ≥3 fixtures × 5 questions per cell (warm-slot classes); per-cluster reporting; "green requires EVERY cluster clean"; intervals cluster-aware (bootstrap over fixtures) |
| Multiplicity | one primary endpoint per class (headline pass rate); ALL cells published; rerun history public |

---

## D2 — STATISTICS

### D2.1 Recommended n and interval methods for pass-rate claims

**Claim 1 — Exact binomial intervals are the accepted method for small-n pass rates.**
Clopper–Pearson (1934) exact intervals and the Wilson score interval (1927) are the standard tools; the canonical review (Brown, Cai & DasGupta 2001, *Statistical Science* 16(2):101–133) shows the normal approximation fails badly for small n and extreme p, and recommends Wilson for coverage in practice, with Clopper–Pearson as the conservative exact fallback. The "rule of three" (0 failures in n → 95% upper bound on failure rate ≈ 3/n) traces to Hanley & Lippman-Hand (1983, *JAMA* 249:1743–1745).
[EN; CONSENSUS — textbook statistics; multiple independent sources.]

**Claim 2 — What v2's n values actually certify (computed, Clopper–Pearson 95%):**

| Run | CP lower 95% bound on pass rate | Rule-of-3 approx |
|---|---|---|
| 5/5 | 0.478 | 0.400 |
| 15/15 | 0.782 | 0.800 |
| 15/15 ×2 (confirmation) = 30/30 | 0.884 | 0.900 |
| 60/60 | 0.940 | 0.950 |

Implication: a single 15/15 green run excludes only pass rates <~0.78 (95% confidence). It does **not** distinguish a 0.90-reliable class from a 0.98-reliable class. Certifying a 0.95 floor with zero failures needs n≈60 (rule of three); 0.98 needs n≈150; 0.99 needs n≈300. If "CAPABILITY-GREEN (walk away)" is meant to certify ≈0.95+ reliability, n=15 is underpowered; if it is meant to certify "better than ~0.8", it is adequate.
[Computed from Claim 1 methods; CONSENSUS math.]

**Claim 3 — Reporting practice: point estimate alone is insufficient; intervals + trial-level transparency are the norm in serious eval reporting.** HELM (Liang et al., 2022, Stanford CRFM) institutionalized multi-metric + scenario transparency for LLM evals; NLP significance-testing guidance (Dror et al., 2018, ACL tutorial paper) demands intervals over point estimates.
[EN; CONSENSUS.]

**Verdict D2.1: VERIFY-CHANGE.** Keep n=5/n=15 as the cost envelope, but (a) report Clopper–Pearson or Wilson 95% intervals on every headline pass rate, never bare point estimates; (b) decide explicitly what pass-rate floor GREEN is supposed to certify — if ≥0.95, n≈60 per green class (or state the 0.78 floor honestly on the card); (c) state the floor on the operator card ("15/15 ⇒ ≥78% floor at 95% confidence").

---

### D2.2 Clustered trials — is bootstrap-over-clusters the standard?

**Claim 4 — Yes: cluster bootstrap / cluster-robust inference is the standard treatment for clustered data.** Cameron, Gelbach & Miller (2008, *Review of Economics and Statistics* 90(3):414–427) is the canonical reference establishing bootstrap-based inference over clusters (pairs/t-cluster). Field & Welsh (2007, *JRSS-B* 69(3):369–390) bootstrap over resampled clusters for mixed models. NLP/ML evaluation adopts the same device: Dror et al. (2018) recommend paired bootstrap (resampling units, not individual judgments) for model comparisons; LLM eval practice commonly resamples over documents/fixtures, not over questions within a document.
[EN; CONSENSUS — the cluster bootstrap is standard for clustered designs in econometrics and ML eval.]

**Claim 5 — Few-cluster caveat: bootstrap over 3–5 clusters is unreliable.** MacKinnon & Webb (2017, *J. Applied Econometrics*; 2018 "The wild bootstrap for few (treated) clusters") show cluster bootstrap and cluster-robust variance break down with very few clusters; the wild cluster bootstrap is the accepted fix, and below ~10–20 clusters even that is coarse. v2's "≥3 fixtures × 5 questions" bootstraps over only 3 units when at minimum; the interval will be dominated by which 3 fixtures were drawn.
[EN; CONSENSUS within the econometrics literature — few-cluster fragility is well documented.]

**Claim 6 — Within-fixture correlation: questions in one fixture are NOT independent trials.** The design already treats the fixture as the unit ("green requires EVERY cluster clean") — this matches the standard (cluster-level inference; questions are the within-cluster units). If questions were treated as independent, effective n would be inflated (3×5=15 nominal vs ~3 effective clusters).
[Math + standard cluster-inference reasoning; CONSENSUS.]

**Verdict D2.2: VERIFY-CHANGE (partial ADOPT).** ADOPT: bootstrap over fixtures is the right unit — it IS the standard. VERIFY-CHANGE: 3 fixtures is a statistically degenerate cluster count; raise the floor to ≥10–20 fixtures per cell for warm-slot classes (or at minimum report per-fixture rates + the fixture-level interval and label 3-fixture intervals as exploratory). The "EVERY cluster clean" conjunction rule is conservative and safe (it can only under-claim), but its operating characteristics should be published (P(all k clusters clean | p) = p^(k·q) under independence).

---

### D2.3 Adaptive/sequential testing — screen-n5-then-escalate: pitfalls and corrections

**Claim 7 — Optional stopping / peeking inflates false positives — the classic documented pitfall.** Sequential analysis (Wald 1945) formalized the price of data-dependent stopping; group-sequential designs with pre-specified alpha spending (Pocock 1977, *Biometrika*; O'Brien & Fleming 1979, *Biometrics*; Lan & DeMets 1983, *Biometrika*) are the accepted correction in clinical trials. The general-audience canonical citation for the pitfall is Simmons, Nelson & Simonsohn (2011, "False-Positive Psychology," *Psychological Science* 22(11):1359–1366): researcher degrees of freedom (deciding to collect more data after peeking) inflate type I error far above 5%. Gelman & Loken (2013, "The garden of forking paths," *Am. J. Epidemiology*) generalize: unacknowledged analysis flexibility makes "significant" results non-reproducible.
[EN; CONSENSUS — optional stopping as a false-positive engine is one of the most replicated findings in methodology.]

**Claim 8 — v2's specific screen does NOT inflate alpha for the green claim (good news, and why).** Because GREEN requires 5/5 at screen AND 15/15 at full (i.e., every one of the 15 trials passes), P(green | p) = p^15 regardless of the screen — the screen is a pure cost-saving device with identical type-I properties to a straight 15/15 run. The screen only changes *when* you spend trials, not the green claim's calibration. Computed: at null p0=0.8, P(green)=0.035 (≈alpha); at p0=0.85, 0.087; at p0=0.9, 0.206 — so "green" is well-calibrated only if the capability null is ~0.8, not if you want to reject a 0.9 null.
[Computed from the binomial; the *property* is elementary — but flag as SINGLE-SOURCE in the sense that it is a derivation, not a published analysis of v2's table.]

**Claim 9 — The YELLOW branch is statistically underspecified (the real gap).** "3–4/5 → YELLOW (delegate-with-review), pending confirmation run" — the confirmation run's size and pass threshold are not pre-specified, so the YELLOW path's operating characteristics are undefined. This is exactly the forking-paths pattern of Claim 7: any rule that is decided after seeing data has uncontrolled error rates. Also, the confirmation run doubles the green bar: green+confirmation = p^30. Computed power: a class with true p=0.95 passes green+confirmation only 21.5% of the time; p=0.98 → 54.5%; p=0.99 → 74%. So the confirmation gate makes the card conservative to the point of high false negatives for genuinely 0.95–0.98-reliable classes — a policy tradeoff, but it should be *decided*, not emergent.
[Computed; the underspecification is factual from the design text — SINGLE-SOURCE on the numbers, CONSENSUS on the principle (pre-specification is the accepted correction).]

**Claim 10 — Accepted corrections for adaptive designs.** (a) Pre-register the full decision tree before any data (thresholds, sizes, stopping rules) — the design already pre-registers the screen/full table; extend it to the YELLOW confirmation rule. (b) If interim looks are wanted with formal error control, use a group-sequential design with alpha spending (Pocock/O'Brien-Fleming/Lan-DeMets) or an exact binomial sequential plan; otherwise treat all interim analysis as cost-saving with inference only at the final n (which is what 5/5→15/15 effectively does). (c) The untouched-fresh-fixture confirmation run is the strongest available anti-peeking device (it removes the "rerun until green" option) — keep it. (d) Public rerun history (v2 §5) is the transparency norm (pre-registration movement; also Dror et al. 2018).
[EN; CONSENSUS.]

**Verdict D2.3: ADOPT with one VERIFY-CHANGE.** ADOPT: 5/5→15/15 green rule (no alpha inflation; cost-saving by construction), public rerun history, untouched confirmation run. VERIFY-CHANGE: (a) pre-specify the YELLOW confirmation rule (size + threshold) before any measurement; (b) publish the operating-characteristics table (p → P(green), P(yellow), P(red)) as a design appendix; (c) decide the target floor the confirmation run is meant to certify (p^30 certifies ≥~0.884 floor at 95% but has ~50% false-negative rate at true p=0.98 — consider n=15 green without confirmation for capability tier + confirmation only for AUTONOMY tier, or accept the conservative bias deliberately).

---

### D2.4 Multiplicity control when reporting many cells

**Claim 11 — The problem: 18 headline cells (9 classes × 2 tiers) at α=0.05 each.** Computed: if all 18 cells are null, P(≥1 false GREEN) ≈ 60% with no correction. Standard corrections: Bonferroni (1936); Holm's step-down (1979, *Scand. J. Statist.*); Benjamini & Hochberg FDR (1995, *JRSS-B* 57(1):289–300). In NLP/ML evaluation, Dror et al. (2018) cover multiple-comparisons control as standard practice; the FDR is the community-default for large tables; reporting all cells regardless of significance (no suppression of "failed" cells) is the transparency norm.
[EN; CONSENSUS.]

**Claim 12 — v2's structure is already multiplicity-moderate, and the confirmation run is an implicit correction.** One pre-registered primary endpoint per class is the textbook pre-specification device. Publishing ALL cells regardless of outcome removes publication-bias-style selection. And because GREEN requires two independent all-clean runs, per-cell false-green ≈ α² (e.g., 0.035² ≈ 0.0012 at p0=0.8); across 18 cells ≈ 2.2% expected — the confirmation run doubles as multiplicity control. The remaining exposure is the YELLOW tier and the 2-tier × 9-class headline table.
[Computed; structure is factual from design text.]

**Verdict D2.4: ADOPT.** One primary endpoint per class + publish-all-cells is the right architecture. Add: (a) state the multiplicity posture explicitly (confirmatory = the 9 primary endpoints with the confirmation-run gate; exploratory = everything else, labeled as such); (b) optionally report FDR-adjusted q-values on the primary endpoint table so the card's "green" claims carry a multiplicity-corrected read; (c) do not multiplicity-correct the *screening* tier (it is a cost device, not an inference).

---

## D3 — AGENTIC ORACLES: gaming of "tests pass" and accepted mitigations

(Research verification in flight — sources, dates, URLs, and ZH-venue items land here next; D3.1 gaming vectors, D3.2 mitigations, D3.3 ZH venues, each with CONSENSUS/SINGLE-SOURCE and verdicts.)

---

## 9. Cross-cutting recommendations for v2 (statistics + oracles)

TBD after D3 verification.

## IMPROVEMENTS

TBD.

<!-- research agents: c71552ce (D2 stats), 2a7678ae (D3 oracles EN), 8bcb53f2 (ZH venues) -->
