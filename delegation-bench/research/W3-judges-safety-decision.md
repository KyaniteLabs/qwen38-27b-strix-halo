# RESEARCH-BENCH-W3 — Judges (D4), Autonomy-Safety (D5), Decision-Support Evals (D6)

- Feeds: `DELEGATION-BENCH-DESIGN-2026-08-21.md` (delegation benchmark v2; sections 1, 5, 8, 9)
- Worker: independent research worker (KyaniteLabs research lane)
- Method: web-verified named sources with dates; each claim tagged `CONSENSUS` (multiple independent sources/lineage) or `SINGLE-SOURCE` (one study); each slice closes with an ADOPT / VERIFY-CHANGE / NO-PRECEDENT verdict for v2.

---

## D4 — HUMAN + LLM JUDGES (v2 §8 C4/C7/C9 judging core)

### D4.1 Blinding, dual-judge, adjudication protocols

**EN venues**
- MT-Bench / Chatbot Arena (Zheng et al., arXiv 2306.05685, Jun 2023; NeurIPS 2024): the canonical LLM-judge protocol — blind pairwise comparison, GPT-4 judge, agreement with human preferences measured, and **documented position/verbosity bias** (judge favors first/verbose answer). Bias finding is replicated across later work → CONSENSUS. This is the direct precedent for v2's "identity and arm hidden".
- VeritasBench human-judge validation (2025): reports Cohen's κ = 0.794 for GPT-4o vs a **human majority-vote reference** on 20 examples — a concrete agreement-reporting + adjudication pattern (majority vote as reference) → SINGLE-SOURCE for the specific number; majority-vote adjudication is CONSENSUS practice (also used in MT-Bench style pipelines).
- "Rubric-conditioned LLM labeling: Agreement, uncertainty, and label consistency in subjective text annotation" (Computers in Human Behavior, 2026): agreement/uncertainty/consistency metrics for LLM annotation under rubrics → SINGLE-SOURCE, useful metric set.
- "Can LLMs Generate User Stories and Assess Their Quality?" (IEEE, 2025): uses a conflict-aware formulation to handle annotator disagreement (focus on meaningful disagreements) → SINGLE-SOURCE; matches v2's "disagreement measured and adjudicated".
- "Judge's Verdict: A Comprehensive Analysis of LLM Judge Capability Through Human Agreement" (2025): whole-pipeline judge-vs-human agreement study → SINGLE-SOURCE.
- Inter-rater agreement reporting norms: Cohen's κ (VeritasBench), Fleiss' κ for 3+ annotators (multi-agent math-item validation, arXiv 2604.05160), Krippendorff's α (EMSE guidelines work, 2026). Consensus that SOME agreement coefficient is mandatory; no single coefficient is canonical → CONSENSUS on reporting, VERIFY-CHANGE on choice.

**ZH venues**
- JudgeLM (BAAI / Shanghai AI Lab, arXiv 2310.17631, Oct 2023; ICLR 2025 Spotlight): open-sourced fine-tuned LLM judge with bias/robustness analysis — the main Chinese-lineage judge artifact; scaling judges to judge other judges. SINGLE-SOURCE for method, CONSENSUS for its use as a judge-family reference.
- AlignBench (THUDM / Zhipu, arXiv 2311.18743, Nov 2023): Chinese alignment benchmark using a **multi-dimension rubric with single-answer LLM judging** (not pairwise) — precedent for rubric-graded single answers in ZH. Widely used → CONSENSUS adoption.
- PandaLM (ICLR 2024, arXiv 2306.05087, 2023): LLM-as-judge benchmark for instruction tuning, ZH-affiliated lineage; still a reference point in 2025 judge papers (e.g., 2510.00263).

**Verdict D4.1 — ADOPT with one change.** Dual blinded judges + reported inter-rater agreement + majority-vote adjudication is well-precedented and directly matches v2 §8. VERIFY-CHANGE: fix the adjudication rule in the judge spec (majority → tie-break judge/human) and the agreement coefficient (κ vs α) before freeze, since no single standard exists. Also add order-shuffling to the blinding spec (position bias is CONSENSUS).

### D4.2 LLM-as-judge validity for summaries (2025–26 evidence)

- G-Eval (Liu et al., arXiv 2303.16634, Mar 2023): chain-of-thought + form-filling rubric scoring with GPT-4; became the baseline for rubric LLM eval → CONSENSUS adoption.
- "The Effect of Document Summarization on LLM-Based Relevance Judgments" (arXiv 2512.05334, Dec 2025): summarization materially shifts LLM relevance judgments — direct evidence that judge validity is input-format-sensitive → SINGLE-SOURCE.
- "Potential and Perils of Large Language Models as Judges of Unstructured Textual Data" (Bedemariam-Perez et al., 2024/25): perils catalog for LLM judging of free text → SINGLE-SOURCE.
- FActScore (Min et al., EMNLP 2023, arXiv 2305.14251): **atomic-fact decomposition** for factual precision of long-form text — the machine-core precedent for summary fact coverage and planted-contradiction probes → CONSENSUS lineage (AlignScore/G-Eval variants build on it).
- "LLMs-as-Judges: A Comprehensive Survey" (Li et al., 2024): survey consolidating judge strengths/biases → CONSENSUS reference.
- Overall: LLM judges correlate with humans but agreement varies by task/judge/format (CONSENSUS across the above). Implication for v2: judge validity must be demonstrated per class (C4 vs C7 vs C9), not assumed globally.

**ZH venue:** zhihu/CSDN eval-literature write-ups track this (e.g., 文本生成评测笔记); AlignBench's rubric design is the ZH-native rubric-judge instance.

**Verdict D4.2 — ADOPT with calibration gate.** Rubric-graded dual-judge summary scoring is standard; v2 should add a pre-run judge-vs-human calibration pilot per class (VERIFY-CHANGE on the gate, not the method).

### D4.3 LLM-as-judge for translation (2025–26 evidence)

- WMT 2024 Quality Estimation findings, "Are LLMs Closing the Gap in QE?" (aclanthology 2024.wmt-1.3): LLM-based QE approaches human-level QE but still gaps human annotation → SINGLE-SOURCE event, CONSENSUS trend (LLM MT-eval is mainstream).
- ReMedy: Learning MT Evaluation from Human Preferences with Reward Modeling (EMNLP 2025 main, arXiv 2504.13630): reward-model MT eval trained on human preferences — direct "human-first, model-second" precedent → SINGLE-SOURCE.
- "Same evaluation, more tokens: on the effect of input length for MT evaluation using LLMs" (EMNLP 2025 main, 2025.emnlp-main.402): input length changes LLM MT-eval outcomes → SINGLE-SOURCE; matters for C7 long-document fixtures.
- M-MAD: Multidimensional Multi-Agent Debate for MT Evaluation (ACL 2025 long, 2025.acl-long.351): multi-agent debate judges — a dual/multi-judge precedent with disagreement handling → SINGLE-SOURCE.
- HiMATE: Hierarchical Multi-Agent MT Evaluation (Findings EMNLP 2025, 2025.findings-emnlp.593): decomposition-based hierarchical judging → SINGLE-SOURCE, directly relevant to meaning-unit judging.
- "Refined Assessment for Translation Evaluation: Rethinking MT Evaluation in the Era of Human-Level Systems" (Findings EMNLP 2025, 2025.findings-emnlp.1203): argues coarse sentence-level scoring is obsolete at human-level quality → SINGLE-SOURCE, motivates fine-grained units.
- "The Devil Is in the Errors: Leveraging LLMs for Fine-grained MT Evaluation" (WMT 2023 shared task): LLM fine-grained error annotation → SINGLE-SOURCE.
- **Self-bias warning:** "Deconstructing Self-Bias in LLM-generated Translation Benchmarks" (arXiv 2509.26600, Sep 2025): LLM judges systematically prefer LLM-generated translations → SINGLE-SOURCE study, CONSENSUS-adjacent phenomenon (self-preference replicated broadly). Implication: v2's C7 judges must not be the same model family as the system under test.

**ZH venues:** WMT 2024 proceedings mirrored at aclanthology.cn (CN venue access); DeepPaper/arxiv.deeppaper.ai Chinese analyses of ReMedy; HardMTBench (2026, ZH-EN knowledge-intensive stress test, arXiv 2605.28315) — ZH-EN translation eval precedent.

**Verdict D4.3 — ADOPT.** Human-aligned LLM judges are the 2025–26 standard for translation eval; adopt dual blinded judges + fine-grained error scoring, and VERIFY-CHANGE only the constraint that judge models differ from the system under test (self-bias).

### D4.4 Meaning-unit vs round-trip translation eval

- **Meaning-unit side (strong precedent):**
  - MQM (Multidimensional Quality Metrics) span-level error annotation is the WMT human-eval standard (2022–24 human eval campaigns) — decomposed error spans, not sentence scores → CONSENSUS.
  - FActScore atomic facts (EMNLP 2023) — unit decomposition for factuality → CONSENSUS lineage.
  - Refined Assessment (Findings EMNLP 2025) and HiMATE (Findings EMNLP 2025) — granularity/decomposition-based MT judging → SINGLE-SOURCE each, same direction.
  - "Cross-Lingual LLM-Judge Transfer via Evaluation Decomposition" (arXiv 2603.18557, 2026): evaluation decomposition as a transferable judging construct → SINGLE-SOURCE.
- **Round-trip side (weak/negative precedent):**
  - "Round-Trip Translation Reveals What Frontier Multilingual Benchmarks Miss" (arXiv 2604.12911, Apr 2026): round-trip translation used to expose benchmark blind spots — i.e., round-trip is a **diagnostic probe**, not a validity metric → SINGLE-SOURCE.
  - "The Paradox of Poetic Intent in Back-Translation" (arXiv 2504.16286, Apr 2025): back-translation quality checks on Chinese translation shown unreliable (identity/lossy rewrites) → SINGLE-SOURCE.
  - Combined with self-bias (D4.3): round-trip is doubly suspect because both directions are LLM-generated → the strongest reading is NO-PRECEDENT for round-trip as a quality core.

**Verdict D4.4 — ADOPT meaning-unit matching; NO-PRECEDENT for round-trip.** v2 §8's "meaning-unit matching" maps cleanly onto MQM-span + atomic-fact decomposition; keep it the C7 machine core. Round-trip should not be a scored endpoint; at most a cheap auxiliary probe (VERIFY-CHANGE if anyone wants it kept).

### D4 slice verdict — **ADOPT** (dual blinded judges, agreement reporting, majority adjudication, meaning-unit core, human-aligned judge models), with two VERIFY-CHANGE items: (1) judge-calibration pilot + agreement threshold before freeze; (2) judge model must differ from the system under test (self-bias).

---

## D5 — AUTONOMY / DELEGATION-SAFETY PRECEDENT (v2 §1, §8 C8 safety cell)

### D5.1 Benchmarks measuring "safe to delegate"

- **tau-bench** (Sierra, arXiv 2406.12045, Jun 2024; NeurIPS 2024): tool-agent-user interactions; scores **policy faithfulness** (did what was asked, nothing more) alongside task success — the reference scoring construct for v2's "the asked thing, in the asked form, nothing more" → CONSENSUS (adopted broadly in 2025 agent evals).
- **tau2-bench** (arXiv 2506.07982, Jun 2025): dual-control (agent + human supervisor) — measures control-conflict handling and appropriate escalation to the human → SINGLE-SOURCE; the closest precedent to v2's escalation quality (S1(c)).
- tau3-bench (2026, Sierra) — next iteration, noted for tracking → SINGLE-SOURCE (repo-level).
- **OSWorld** (Xie et al., arXiv 2404.07972, Apr 2024; NeurIPS 2024): real-computer environment benchmark → CONSENSUS infrastructure.
- **OS-Harm** (EPFL, arXiv 2506.14866, Jun 2025; NeurIPS 2025 Spotlight): the OSWorld-style **safety subset** — "safe task" = completes goal with zero safety violations; measures harmful completions of computer-use agents → SINGLE-SOURCE but exactly the construct v2 §8's safety cell wants.
- **SafeAgentBench** (arXiv 2412.13178, Dec 2024, v5 updates): safe task planning of embodied LLM agents; hazardous-action triage (reject/repair/execute) → SINGLE-SOURCE.
- **AgentSafetyBench** (Tsinghua thu-coai, arXiv 2412.14470, Dec 2024): agent safety with risk taxonomy, trajectory-level evaluation, attack detection + risky-trajectory detection → SINGLE-SOURCE; ZH-native.
- **AgentHarm** (Gray Swan AI, arXiv 2410.09024, Oct 2024): harmfulness of agent capabilities + refusal robustness under jailbreak-style attacks; judge-scored harm → SINGLE-SOURCE, adopted by AI Safety Institute (HF mirror) → CONSENSUS-adjacent.
- **Prompt injection benches:** AgentDojo (ETH Zurich, arXiv 2406.13352, Jun 2024; NeurIPS 2024 D&B): dynamic environment for injection attacks + defenses, scoring **task safety under attack** → CONSENSUS reference for injection resistance. InjecAgent (NTU, arXiv 2403.02691, Mar 2024): indirect prompt injection in tool-integrated agents → SINGLE-SOURCE.
- **AgentBench** (Tsinghua, ICLR 2024, arXiv 2308.03688): first systematic agent benchmark → CONSENSUS lineage.
- **AgentBoard** (HKUST/SJTU, arXiv 2401.13178, Jan 2024; NeurIPS 2024 D&B): analytical evaluation board — step-level progress/regress metrics instead of binary success → SINGLE-SOURCE; useful for v2's step-level failure attribution.

**ZH venues:** AgentBench (清华, ICLR 2024), AgentSafetyBench (清华 thu-coai; WeChat article "Agent-SafetyBench：全面的智能体安全评估基准" on mp.weixin.qq.com; BAAI hub page), AgentBoard (HKUST), CSDN/cnblogs τ-bench tutorials (e.g., "τ-bench：重塑Agent评估的工具-代理-用户交互基准").

### D5.2 Abstention / escalation quality

- **HiL-Bench** (arXiv 2604.09408, Apr 2026): "Do Agents Know When to Ask for Help?" — human-in-loop benchmark scoring whether agents ask at the right time → SINGLE-SOURCE; the only dedicated ask-quality benchmark found.
- **"Just Do It!? Computer-Use Agents Exhibit Blind Goal-Directedness"** (arXiv 2510.01670, Oct 2025; NVIDIA + Microsoft researchers): computer-use agents execute unsafe/ambiguous instructions instead of asking — quantifies overcompliance as a failure mode → SINGLE-SOURCE but directly validates v2's "asks when underspecified" as a scored behavior.
- AgentHarm's refusal-robustness scoring (D5.1) covers the refusal half of escalation → SINGLE-SOURCE.

**Verdict D5.2 — VERIFY-CHANGE.** "Ask quality" is an emerging 2025–26 construct (HiL-Bench + blind goal-directedness), not yet a settled rubric. v2 should adopt the 3-way scoring (asked appropriately / failed to ask / asked unnecessarily) and an overcompliance rate, but the rubric itself has no canonical form yet.

### D5.3 What to borrow for v2

Compose the C8 safety cell from existing, borrowable pieces:
1. tau-bench policy-faithfulness scoring (scoped-action check) — ADOPT.
2. AgentDojo-style injection suite (attacks in untrusted documents; task safety under attack) — ADOPT, but VERIFY-CHANGE the environment mapping: AgentDojo attacks tool-API conversations; v2's cell attacks a CLI/filesystem worktree, so fixtures must be re-authored, not copied.
3. OS-Harm-style "safe task with violation counter" (zero-violation pass) — ADOPT for the unauthorized-side-effect check; filesystem diff-allowlist is the local analogue.
4. HiL-Bench-style ask-quality scoring + blind-goal-directedness overcompliance rate — VERIFY-CHANGE (rubric young).
5. AgentHarm-style judge-scored refusal under injected instructions — ADOPT.

### D5 slice verdict — **ADOPT** the composed safety cell (policy faithfulness + injection resistance + zero-unauthorized-side-effect + ask-quality), with VERIFY-CHANGE on (a) injection-suite adaptation to a non-tool environment and (b) the ask-quality rubric. No NO-PRECEDENT items.

---

## D6 — DECISION-SUPPORT EVALS (v2 §2 C9)

### D6.1 Required-consideration coverage (pre-registered)

- **DEER: Deep-Research Expert Report benchmark** (Alibaba/Qwen team, arXiv 2512.17776, Dec 2025; ICML 2026): evaluates deep-research reports with **pre-defined scoring rubrics, expert-verified gold reports, evidence-citation requirements, and explicit sensitivity analysis to LLM version changes** → the single closest precedent to C9's "required-considerations coverage (pre-registered)" → SINGLE-SOURCE but heavyweight and recent; the Qwen authorship makes it ZH-first too.
- **MedHELM** (Stanford, arXiv 2505.23802, May 2025; Stanford HAI coverage Mar 2025): holistic medical LLM evaluation — task-specific rubrics + human-expert validation for decision-support tasks (incl. DeepSeek-R1 medical eval, 66% win-rate coverage on 199it) → SINGLE-SOURCE, strong rubric-decisions precedent.
- MT-Bench single-answer rubric grading (Zheng et al. 2023) and AlignBench multi-dimension rubric (THUDM 2023) — rubric pre-definition is standard → CONSENSUS on rubric mechanics; the specific "coverage of a pre-registered consideration checklist" as a pass/fail per consideration has no dedicated named benchmark → VERIFY-CHANGE on protocol form (DEER rubrics + AlignBench dimensions are the templates).

**ZH venues:** OpenCompass 司南 (Shanghai AI Lab / BAAI, launched 2023; OpenCompass 2.0 Jan 2024; Compass Arena) — the ZH-native eval platform; AlignBench (THUDM); DEER (Alibaba); 199it coverage of Stanford MedHELM on DeepSeek-R1.

### D6.2 Evidence fidelity (no invented numbers)

- **FActScore** (EMNLP 2023, arXiv 2305.14251): decompose output into atomic facts; verify each against the knowledge source; report precision/recall — the canonical machine core for "evidence fidelity" → CONSENSUS lineage.
- DEER (2025): evidence-citation checks + expert verification in reports → SINGLE-SOURCE addition.
- Implication: C9's "no invented numbers" should be an atomic-claim verification against the provided decision docs (FActScore-style), not a holistic judge call → ADOPT.

### D6.3 Temp-0 answer stability

- **"Non-Determinism of 'Deterministic' LLM Settings"** (arXiv 2408.04667, Aug 2024): temperature-0 does not guarantee identical outputs; determinism must be measured by repeated runs → SINGLE-SOURCE, widely reproduced in practice → CONSENSUS-adjacent.
- "Quantifying non-deterministic drift in LLMs" (arXiv 2601.19934, Jan 2026) → SINGLE-SOURCE.
- "Introducing Background Temperature to Characterise Hidden Randomness in LLMs" (arXiv 2604.22411; Zenodo v2 Oct 2025) → SINGLE-SOURCE.
- DEER's LLM-version sensitivity analysis (2025) → eval robustness precedent → SINGLE-SOURCE.
- Self-consistency (Wang et al., ICLR 2023): sampling-consistency as reliability technique (background) → CONSENSUS.
- Implication: v2's "same inputs re-asked at temp 0 = same call" is the right idea but must be **operationalized as repeated-run stability with a threshold** (e.g., n=3 repeats, agreement metric), not assumed → ADOPT with measurement protocol.

### D6.4 Stated-uncertainty calibration

- Verbalized confidence (Tian et al., NeurIPS 2023): asking models to state confidence, then calibrating — canonical start → CONSENSUS.
- "Seeing is Believing, but How Much? A Comprehensive Analysis of Verbalized Calibration" (arXiv 2505.20236; EMNLP 2025 main): comprehensive verbalized-calibration analysis (VLM domain) → SINGLE-SOURCE.
- "Can Large Language Models Express Uncertainty Like Human?" (arXiv 2509.24202, Sep 2025) → SINGLE-SOURCE.
- "LLMs Should Express Uncertainty Explicitly" (arXiv 2604.05306, Apr 2026) → SINGLE-SOURCE.
- "Trustworthy LLMs via Reinforced Hesitation" (arXiv 2511.11500, Nov 2025): training models to hesitate appropriately → SINGLE-SOURCE.
- MedHELM (2025): calibration metrics for medical decision support → SINGLE-SOURCE.
- Consensus across all: measure calibration of stated uncertainty (ECE-style against outcome correctness), never trust raw confidence tokens → CONSENSUS.

### D6 slice verdict — **ADOPT** (rubric/checklist coverage from DEER + AlignBench; FActScore atomic evidence fidelity; repeated-run temp-0 stability protocol; ECE-style stated-uncertainty calibration), with VERIFY-CHANGE only on the exact pre-registration artifact format for C9 consideration coverage (no named precedent; DEER rubrics are the template).

---

## Cross-slice notes for v2

- Judge-family separation (D4.3): judges must not share the model family of the system under test — supported by self-bias evidence (2509.26600) and blind-judge design.
- Escalation and decision-support share a construct: C8's ask-quality and C9's stated-uncertainty can share one calibration rubric → fewer judge specs.
- Sealed-holdout policy (§7) interacts with judge calibration: the calibration pilot must use development fixtures only, and its agreement threshold must be pre-registered with the decision table (§5) — precedent: VeritasBench majority-vote reference; no bench does exactly this → v2 is ahead of precedent here (fine, but log it).

---

## IMPROVEMENTS

1. **Add a judge-calibration gate to the readiness checklist (§10).** Why: D4 evidence (2505.20236, 2512.05334, VeritasBench κ) shows LLM-judge agreement with humans varies by task and input format; without a measured threshold, the whole C4/C7/C9 scoring stack is unvalidated. Fix: 20-item human-scored pilot per judged class before freeze; require κ ≥ 0.6 vs human majority; log per-judge agreement in the report.
2. **Formalize ask-quality as a 3-way rubric with an overcompliance rate.** Why: v2 S1(c) treats "asks/escalates" as binary, but 2025–26 evidence (HiL-Bench, 2510.01670) shows the failure modes are "asks unnecessarily" and "fails to ask" — different costs. Fix: score each underspecified trial as asked-appropriately / failed-to-ask / asked-unnecessarily, and publish the overcompliance rate alongside pass rate.
3. **Add a `repeat_id` field and stability report line to the trial metadata (§6).** Why: temp-0 is not deterministic (2408.04667) and judge outputs drift, so the C9 stability requirement has no measurement protocol today. Fix: run every C9 verdict and a 5% judge sample n=3 at temp 0; report per-cell agreement (e.g., Krippendorff's α); make a cell ineligible for green if stability < 0.9.

---

Status: DONE
