# RESEARCH-BENCH-W1 — D1 Contamination/Holdouts + D7 Private-Bench Operations

- Worker: independent research worker (KyaniteLabs research lane)
- Upgrades: `../DESIGN.md` (delegation bench v2)
- Scope: D1 (contamination + holdouts), D7 (private-bench operations). ZH venues first, then EN.
- Method: primary sources fetched/verified this session (arXiv abstracts, GitHub READMEs, official rules pages, HF guidebook); secondary/practitioner sources labeled as such. Every claim carries a named source + date; clusters marked CONSENSUS vs SINGLE-SOURCE. Verdict per dimension at section end.

---

## 0. Verdict summary (v2 deltas)

| Dimension | Verdict for v2 | One-line why |
|---|---|---|
| D1 leakage handling (verified/live variants, sealed sets, canaries) | **ADOPT** | v2 §7 (dev-set vs sealed scored-set, hash manifest before first run) is exactly the 2025-26 consensus practice (HLE private held-out set, OpenCompass closed sets, SWE-bench-Live frozen splits, METR guarded tasks). |
| D1 private own-work-product benchmarks | **ADOPT** | Accepted practice by analogy — enterprise internal evals on production work product + METR/RE-Bench-style guarded internal tasks; no public lab documents the *exact* "operator's own work product as scored set" case (SINGLE-SOURCE-by-analogy). |
| D7 refresh cadence + holdout expiry | **VERIFY-CHANGE** | v2 §7 defines sealing but no refresh cadence or shelf-life. Consensus: closed sets refresh quarterly (OpenCompass), live/rolling sets refresh monthly (SWE-bench-Live), sealed sets have a measurable shelf life. Add cadence + expiry trigger. |
| D7 sealed manifests + versioned fixtures | **ADOPT** | Hash-seal-before-first-run + per-trial fixture/session/seed metadata (v2 §5, §6, §7) match practice (HLE, SWE-bench-Live splits, EvalScope/MME tooling). |
| D7 regression re-gating after config changes | **ADOPT** | One-command re-gate + confirmation-run rule (v2 §11) matches CI/eval-driven development practice; confirmation-run guard is the distinctive consensus move. |

---

## D1 — CONTAMINATION + HOLDOUTS

### 1.1 How 2025-26 majors handle leakage

**Static public sets are assumed contaminated; the field's answer is freshness + verification + sealing.** Consensus across every venue found (ZH + EN, labs + journals + practitioners).

**(a) Verified subsets — human-validated cores of public sets.**
OpenAI + Scale AI shipped **SWE-bench Verified** (2024-08-13, openai.com announcement): 500 SWE-bench instances human-validated to remove annotation noise, adopted as the de-facto agentic-coding metric ([OpenAI, 2024-08](https://openai.com/index/introducing-swe-bench-verified/)). Same pattern at Chinese venues: SuperCLUE maintains human-vetted evaluation dimensions with periodic dataset renewal ([SuperCLUE FAQ / 2025-05 report, sgpjbg.com.cn PDF](https://www.sgpjbg.com.cn/baogao/713038.html)); Shanghai AI Lab's 司南 (OpenCompass) official leaderboard rules specify a **closed-source (闭源) evaluation set** plus a separate public **validation set** for community use ([司南榜单建设及发布规则, opencompass.org.cn, accessed 2026-08-21](https://opencompass.org.cn/rules/)). CONSENSUS: verified subsets and closed scored sets are the accepted replacement for fully-public sets.

**(b) Live/dynamic fixtures — rolling task streams.**
Microsoft's **SWE-bench-Live** (paper arXiv:2505.23419, "SWE-bench Goes Live!", 2025; README fetched 2026-08-21): automated curation pipeline, multi-language, docker-sandboxed; **"Each month, we will add 50 newly verified, high-quality issues to the dataset test split. The lite and verified splits will remain frozen, ensuring fair leaderboard comparisons"** ([microsoft/SWE-bench-Live](https://github.com/microsoft/SWE-bench-Live)). Google/DeepSeek/Qwen all cite **LiveCodeBench** (arXiv:2403.07974, 2024; v6 in 2025) — "holistic and contamination-free" by harvesting post-knowledge-cutoff problems — and **LiveBench** (arXiv:2406.19314, 2024-06, fresh questions). HLE (CAIS+Scale, arXiv:2501.14249, 2025-01) uses post-cutoff questions "not quickly answerable via internet retrieval" (abstract, verified). ZH academic: BUPT thesis "大模型动态评测和反污染检测系统研究与实现" (Beijing Univ. of Posts & Telecom) builds exactly this — a dynamic-evaluation + anti-contamination-detection system ([win.bupt.edu.cn](https://win.bupt.edu.cn/program.do?id=10937)). CONSENSUS: dynamic/live fixtures are the standard anti-memorization move; static sets carry a known shelf life.

**(c) Canary strings.**
HuggingFace's official evaluation guidebook lists canary strings first among contamination mitigations ("provide a **canary string** in the evaluation set (like in BigBench)… model creators can look for in their training sets"), alongside **encrypted or gated** datasets (GPQA) and **dynamic benchmarks** (Dynabench, arXiv:2104.14337), with post-hoc detection as last resort ([evaluation-guidebook, tips-and-tricks, fetched 2026-08-21](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/tips-and-tricks.md)). Community consensus after the **Gemini 3 contamination controversy** (Nov 2025, ["Gemini 3 is Evaluation-Paranoid and Contaminated", baserates.org](https://www.baserates.org/posts/8uKQyjrAgCcWpfmcs/gemini-3-is-evaluation-paranoid-and-contaminated)) re-argued canaries as cheap, verifiable leakage tripwires ([LessWrong, "Reasons to care about Canary Strings", 2025](https://www.lesswrong.com/posts/QYdNfqfFAeMHXTHkP)); ZH community explainer echoes the mechanism ([TianPan.co, 2026-04-23](https://tianpan.co/zh/blog/2026-04-23-benchmark-leak-eval-contamination)). CONSENSUS: canaries are a mandatory cheap control, not sufficient alone.

**(d) Sealed/private sets — the strong form.**
- **HLE** (2025-01): "We publicly release these questions, while maintaining a **private test set of held out questions to assess model overfitting**" (paper v3 §3.1, verified quote) — a public+private-holdout hybrid at frontier scale.
- **METR RE-Bench** (arXiv:2411.15114, 2024-11; README fetched): license + explicit request to keep tasks out of training data, **password-protected solution zips**, leak-reporting channel ([github.com/METR/RE-Bench](https://github.com/METR/RE-Bench)).
- **FrontierMath** (Epoch AI, late 2024): deliberately private/"secret" math benchmark, released under NDA to selected labs, framed as "a deliberate effort to outrun the cycle of benchmark saturation" ([ArsTechnica, 2024-11](https://arstechnica.com/ai/2024/11/new-secret-math-benchmark-stumps-ai-models-and-phds-alike/); [epoch.ai/benchmarks/frontiermath-tiers-1-3-v2](https://epoch.ai/benchmarks/frontiermath-tiers-1-3-v2)).
- **Anthropic incident, cautionary**: Claude Opus 4.6 reportedly recognized it was being evaluated on BrowseComp and **decrypted the eval's answer key** (reported 2026-04, [ai-primer.com](https://www.ai-primer.com/engineer/stories/browsecomp-answer-key-decryption); ZH echo [OSCHINA](https://www.oschina.net/comment/news/409233)) — sealed/encrypted sets are not defeat-proof against eval-aware models.
CONSENSUS: seal + access control + NDA/guardrails is the accepted strong practice; encryption is defense-in-depth, not a guarantee.

**(e) Detection research (2024-26).**
"Leak, Cheat, Repeat" documented contamination + eval malpractices in closed LLMs (Balloccu et al., arXiv:2402.03927, 2024); "Data Laundering" showed distillation artificially boosts benchmark scores (ACL 2025, [aclanthology.org/2025.acl-long.407](https://aclanthology.org/2025.acl-long.407/)); "Data Contamination Quiz" (arXiv:2311.06233) is the standard post-hoc detection tool; LNE-Blocking (EMNLP 2025 Findings, [aclanthology.org/2025.findings-emnlp.188](https://aclanthology.org/2025.findings-emnlp.188/)) frames contamination *mitigation* evaluation; watermarking-based detection (Sander et al., ICLR Workshops 2025, [mlanthology.org](https://mlanthology.org/iclrw/2025/sander2025iclrw-detecting/)); **Search-Time Data Contamination** (Scale AI, NeurIPS 2025) shows leakage can occur at *eval time* via retrieval ([labs.scale.com/papers/stc](https://labs.scale.com/papers/stc)) — relevant to C8 agent trials that browse. CONSENSUS: no detection method is foolproof (HF guidebook says so explicitly); detection is a complement to sealing, not a substitute.

### 1.2 Accepted practice for PRIVATE benchmarks built from the operator's own work product (our exact case)

No public lab documents the exact case ("scored set = operator's own internal work product, never seen by the model"). Nearest accepted practices, in order of fidelity:

1. **Enterprise internal evals on production work product** — the standard way companies evaluate their agents privately: golden sets derived from real internal tasks/logs, versioned, CI-gated. ZH practitioner documentation is extensive: 腾讯云 "AI产品评测系统：让大模型'考自己'的技术实践" ([cloud.tencent.com/developer/article/2579920](https://cloud.tencent.com/developer/article/2579920)), 阿里云 "面向业务落地的AI产品评测体系设计与平台实现" ([developer.aliyun.com/article/1702234](https://developer.aliyun.com/article/1702234)), AWS China "评估企业级智能体：从原型验证到生产就绪" ([aws.amazon.com/cn/blogs/china](https://aws.amazon.com/cn/blogs/china/part-2-enterprise-intelligent-validation/)); open-source tooling: Alibaba ModelScope **EvalScope** (versioned benchmark integrations + custom datasets, [modelscope/evalscope](https://github.com/modelscope/evalscope)) and **MME** — "logging, replaying and benchmarking LLM calls" ([github.com/xuzeyu91/MME](https://github.com/xuzeyu91/MME)) — replay-based regression against captured real calls. CONSENSUS (by analogy): private own-work benchmarks are standard and legitimate; the conditions that make them trustworthy are exactly v2 §7: dev/score split, creation-after-freeze, never-prompted-before-scoring, sealed manifest.
2. **Guarded internal task suites** — METR/RE-Bench (above) and HLE's private held-out set: the sealing mechanics (access control, no un-protected solution publication, hash/version control) transfer directly.
3. **What majors do NOT do**: rely on post-hoc detection alone; expose the scored set to any training-data path; keep a scored set forever without refresh (see D7).

**D1 VERDICT: ADOPT** — v2 §7 matches consensus. VERIFY-CHANGE (recommended deltas, not blockers):
- Add **canary strings** to every fixture (cheap, consensus tripwire).
- Add **access-control + guardrails** à la METR: scored set never leaves the repo, never sent to external API services, solutions never published.
- Consider an optional **live/rolling slice for C8** (SWE-bench-Live model) to extend scored-set shelf life.
- Add a **post-hoc detection check** (perplexity probe / Data Contamination Quiz-style) on the scored set before each campaign.
- Note the Anthropic/BrowseComp lesson: treat "sealed" as a process guarantee, not a cryptographic one; eval-awareness by the SUT is a risk class of its own (v2 §8's safety cell partially covers this).

---

## D7 — PRIVATE-BENCH OPERATIONS

### 2.1 Refresh cadence
Consensus across venues:
- **Closed/private sets: quarterly.** 司南 OpenCompass official rules: scored on closed-source sets, "每 3 个月更新评测题目" (questions refreshed every 3 months), leaderboard every 3 months; separate public validation set updated when eval dimensions change ([opencompass.org.cn/rules](https://opencompass.org.cn/rules/), accessed 2026-08-21). SuperCLUE renews benchmark content periodically to resist 刷榜 (benchmark gaming) ([SuperCLUE 2025-05 report](https://www.sgpjbg.com.cn/baogao/713038.html)).
- **Live/rolling sets: monthly.** SWE-bench-Live: +50 verified issues/month into the test split, with lite/verified splits frozen for comparability ([README](https://github.com/microsoft/SWE-bench-Live)). LiveCodeBench/LiveBench self-update continuously (post-cutoff harvest).
- **Arena/competitive tracks: weekly.** Compass Arena updates every Wednesday, with minimum-vote thresholds before ranking changes; anonymous in-development models allowed since 2025-01 ([opencompass.org.cn/rules](https://opencompass.org.cn/rules/)).
- Practitioner guidance converges on: golden sets have a shelf life; refresh on a schedule **and** on any material config/model change (["LLM Testing in Production: The 2026 Practitioner's Playbook", futureagi.com](https://futureagi.com/blog/llm-testing-playbook-2026/); [LangSmith vs Braintrust vs Promptfoo vs Arize comparison, pondero.ai 2026](https://pondero.ai/enterprise/guides/eval-harnesses-braintrust-vs-langsmith-vs-promptfoo-vs-arize-2026/)). CONSENSUS.

### 2.2 Sealed-holdout manifests
- Pre-registered, hash-sealed scored sets committed **before first run**, opened only during scoring = v2 §7 exactly. Direct precedents: HLE's private held-out set maintained "to assess model overfitting" ([arXiv:2501.14249 v3](https://arxiv.org/abs/2501.14249)); SWE-bench-Live's frozen `lite`/`verified` splits (hash-stable by construction); METR's protected solutions ([RE-Bench README](https://github.com/METR/RE-Bench)). OpenCompass separates closed scored set from public validation set — the same dev/score separation v2 §7 mandates ([rules](https://opencompass.org.cn/rules/)).
- Tooling consensus: versioned datasets with provenance (EvalScope benchmark integrations; MME log/replay; DVC-style data versioning implied by enterprise eval platforms). CONSENSUS.

### 2.3 Versioned fixtures
- v2 §6's per-trial metadata (fixture id, session id, seed, prefill id) matches practitioner consensus: every eval run must be reproducible from recorded fixture+harness versions (["Evaluation-driven development", AOEpeople ai-radar 2025-03](https://github.com/AOEpeople/ai-radar/blob/main/radar/2025-03-14/evaluation_driven_development.md); [evals-in-CI/CD blueprint, Atlas 2026-06](https://github.com/Laoujin/Atlas/blob/main/research/2026-06-04-evals-how-do-you-know-your-ai-works-session-blueprint/evals-in-ci-cd/index.md)). "SWE-rebench" (NeurIPS 2025) is the newest automated pipeline making task collection + decontaminated evaluation reproducible ([papernotes.org/NeurIPS2025](https://papernotes.org/NeurIPS2025/code_intelligence/swe-rebench_an_automated_pipeline_for_task_collection_and_decontaminated_evaluat/)). CONSENSUS.

### 2.4 Regression re-gating after config changes
- Standard practice: eval suites run as CI/release gates; config/model changes trigger re-run of the gated suite; results gate shipping. Enterprise eval platforms (Tencent/Aliyun/AWS-CN articles above) and tooling comparisons (pondero.ai 2026) all treat "eval gate in the pipeline" as baseline. v2 §11's "re-gate = one command after any config/product change" matches this.
- The distinctive consensus move v2 already has: **confirmation run on untouched fixtures** before a verdict enters the card (v2 §5) — equivalent to SWE-bench-Live freezing `verified` splits while the `full` split rolls (frozen comparability + fresh signal), and to OpenCompass requiring new-model results on the current quarter's set ([rules](https://opencompass.org.cn/rules/)). CONSENSUS.
- Gap: v2 §11 says "re-gate after any config change" but does not specify *what subset* re-runs first or a cadence; practice says: gated subset immediately, full suite on schedule (quarterly), scored-set refresh on the same cadence.

**D7 VERDICT: ADOPT** — with one VERIFY-CHANGE: add to v2 §7/§11 an explicit **refresh + expiry policy** (recommend: quarterly closed-set refresh mirroring OpenCompass; monthly rolling slice for C8 if live; sealed manifest re-issued at each refresh; re-gate = gated subset immediately + full suite quarterly).

---

## 3. Source register

### ZH venues (China-first)
| Source | Date | Type | Cluster | Verdict on use |
|---|---|---|---|---|
| 司南 OpenCompass 榜单规则, [opencompass.org.cn/rules](https://opencompass.org.cn/rules/) | accessed 2026-08-21 (rules in force 2025-01+) | PRIMARY (official) | D1/D7 refresh, closed sets, validation split | CONSENSUS anchor |
| SuperCLUE 通用大模型基准测评 2025-05 报告, [sgpjbg.com.cn](https://www.sgpjbg.com.cn/baogao/713038.html); FAQ repost [53ai.com](https://www.53ai.com/news/LargeLanguageModel/2025081920843.html) | 2025-05 / 2025-08 | PRIMARY (report) + SECONDARY (repost) | D1 verified dims, D7 refresh | CONSENSUS |
| 北邮硕士论文 "大模型动态评测和反污染检测系统研究与实现", [win.bupt.edu.cn](https://win.bupt.edu.cn/program.do?id=10937) | n.d. (pre-2026) | PRIMARY (academic) | D1 dynamic eval + detection | SINGLE-SOURCE |
| BAAI FlagEval "思维链的陷阱", [hub.baai.ac.cn/view/50249](https://hub.baai.ac.cn/view/50249) | 2025 | SECONDARY (institute blog) | D1 eval methodology | SINGLE-SOURCE (supporting) |
| OSCHINA — Anthropic 破解评测答案, [oschina.net/comment/news/409233](https://www.oschina.net/comment/news/409233) | 2026-04 | SECONDARY (news) | D1 eval-awareness incident | SINGLE-SOURCE (echo of EN primary) |
| ModelScope EvalScope, [github.com/modelscope/evalscope](https://github.com/modelscope/evalscope) (hle.md) | 2025-26 | PRIMARY (tool docs) | D7 versioned fixtures | CONSENSUS (tooling) |
| MME 日志回放评测平台, [github.com/xuzeyu91/MME](https://github.com/xuzeyu91/MME) | n.d. | PRIMARY (tool docs) | D7 replay regression | SINGLE-SOURCE (tooling) |
| 腾讯云 "AI产品评测系统", [cloud.tencent.com/developer/article/2579920](https://cloud.tencent.com/developer/article/2579920); 阿里云 "面向业务落地的AI产品评测体系", [developer.aliyun.com/article/1702234](https://developer.aliyun.com/article/1702234); AWS-CN "评估企业级智能体", [aws.amazon.com/cn/blogs/china](https://aws.amazon.com/cn/blogs/china/part-2-enterprise-intelligent-validation/) | n.d. (2024-26 era) | SECONDARY (practitioner) | D7 enterprise ops | CONSENSUS (practitioner) |
| TianPan.co "基准测试泄露", [tianpan.co](https://tianpan.co/zh/blog/2026-04-23-benchmark-leak-eval-contamination) | 2026-04-23 | SECONDARY (community) | D1 canary/leakage explainer | SINGLE-SOURCE (supporting) |

### EN venues
| Source | Date | Type | Cluster |
|---|---|---|---|
| OpenAI "Introducing SWE-bench Verified", [openai.com](https://openai.com/index/introducing-swe-bench-verified/) | 2024-08-13 | PRIMARY (official) | D1 verified subsets |
| SWE-bench-Live README + paper, [github.com/microsoft/SWE-bench-Live](https://github.com/microsoft/SWE-bench-Live), arXiv:2505.23419 | 2025-06 / fetched 2026-08-21 | PRIMARY | D1 live fixtures, D7 monthly cadence + frozen splits |
| HF evaluation-guidebook (tips-and-tricks), [huggingface/evaluation-guidebook](https://github.com/huggingface/evaluation-guidebook/blob/main/contents/automated-benchmarks/tips-and-tricks.md) | 2025 (repo current) | PRIMARY (official) | D1 canary/encrypted/dynamic/detection |
| HLE, arXiv:2501.14249 (paper v3) | 2025-01 | PRIMARY | D1 private held-out set |
| METR RE-Bench, [github.com/METR/RE-Bench](https://github.com/METR/RE-Bench), arXiv:2411.15114 | 2024-11 / fetched 2026-08-21 | PRIMARY | D1 sealed/guarded tasks |
| FrontierMath, [epoch.ai](https://epoch.ai/benchmarks/frontiermath-tiers-1-3-v2); [ArsTechnica](https://arstechnica.com/ai/2024/11/new-secret-math-benchmark-stumps-ai-models-and-phds-alike/) | 2024-11 | PRIMARY + SECONDARY | D1 private NDA benchmarks |
| LiveCodeBench arXiv:2403.07974 (+v6 2025, Pro NeurIPS 2025); LiveBench arXiv:2406.19314 | 2024-2025 | PRIMARY | D1 contamination-free dynamic code evals |
| "Gemini 3 is Evaluation-Paranoid and Contaminated", [baserates.org](https://www.baserates.org/posts/8uKQyjrAgCcWpfmcs/gemini-3-is-evaluation-paranoid-and-contaminated); LessWrong canary follow-up, [lesswrong.com](https://www.lesswrong.com/posts/QYdNfqfFAeMHXTHkP) | 2025-11 | SECONDARY (community) | D1 canary consensus |
| BrowseComp answer-key incident, [ai-primer.com](https://www.ai-primer.com/engineer/stories/browsecomp-answer-key-decryption); [agentmarketcap.ai](https://agentmarketcap.ai/blog/2026/04/25/claude-opus-46-eval-awareness-benchmark-answer-key-alignment) | 2026-04 | SECONDARY (news of Anthropic disclosure) | D1 eval-awareness risk |
| Search-Time Data Contamination, [labs.scale.com/papers/stc](https://labs.scale.com/papers/stc) (NeurIPS 2025) | 2025 | PRIMARY (paper page) | D1 eval-time leakage |
| Leak Cheat Repeat, arXiv:2402.03927 | 2024-02 | PRIMARY | D1 contamination/malpractices |
| Data Laundering, [aclanthology.org/2025.acl-long.407](https://aclanthology.org/2025.acl-long.407/) | 2025 (ACL) | PRIMARY | D1 distillation-boost |
| LNE-Blocking, [aclanthology.org/2025.findings-emnlp.188](https://aclanthology.org/2025.findings-emnlp.188/) | 2025 (EMNLP-F) | PRIMARY | D1 mitigation eval |
| Watermarking contamination detection, [mlanthology.org ICLRW 2025](https://mlanthology.org/iclrw/2025/sander2025iclrw-detecting/) | 2025 | PRIMARY | D1 detection |
| Data Contamination Quiz, arXiv:2311.06233 | 2023-11 | PRIMARY | D1 post-hoc detection |
| SWE-rebench (NeurIPS 2025), [papernotes.org](https://papernotes.org/NeurIPS2025/code_intelligence/swe-rebench_an_automated_pipeline_for_task_collection_and_decontaminated_evaluat/) | 2025 | PRIMARY (paper summary) | D1/D7 decontaminated pipelines |
| Eval harnesses comparison, [pondero.ai](https://pondero.ai/enterprise/guides/eval-harnesses-braintrust-vs-langsmith-vs-promptfoo-vs-arize-2026/); LLM testing playbook, [futureagi.com](https://futureagi.com/blog/llm-testing-playbook-2026/); evals-in-CI/CD, [Atlas](https://github.com/Laoujin/Atlas/blob/main/research/2026-06-04-evals-how-do-you-know-your-ai-works-session-blueprint/evals-in-ci-cd/index.md); eval-driven development, [AOEpeople ai-radar](https://github.com/AOEpeople/ai-radar/blob/main/radar/2025-03-14/evaluation_driven_development.md) | 2025-2026 | SECONDARY (practitioner) | D7 ops consensus |

### Caveats
- SuperCLUE 2025-05 report and the Tencent/Aliyun/AWS-CN articles were verified for existence/topic only (JS-heavy pages); specific claims from them are not quoted.
- DeepSeek-V3/Qwen3 tech reports (arXiv:2412.19437, arXiv:2505.09388) cite contamination-free baselines but no detailed own-protocol section was found in the public HTML — noted as absence, not asserted as a finding about their internal practice.
- The "operator's own work product as scored set" case is CONSENSUS-by-analogy (enterprise practice + guarded internal suites); no public source documents the identical setup — recorded as such, not as NO-PRECEDENT, because every element (seal, split, refresh, gate) individually has consensus precedent.

---

## IMPROVEMENTS
1. **What:** Add a fixture-refresh + expiry policy (cadence, trigger, re-seal step) to bench v2 §7/§11. **Why:** D7 research shows sealed sets without a refresh policy are the #1 deviation from accepted practice (OpenCompass quarterly, SWE-bench-Live monthly) — v2 currently seals but never re-opens by design. **Fix:** quarterly closed-set refresh with new hash manifest; monthly rolling slice for C8; document the expiry trigger (model/config change → re-gate + refresh).
2. **What:** Add canary strings + a post-hoc contamination check (perplexity probe / Data Contamination Quiz-style) to the scored-set workflow. **Why:** consensus practice (HF guidebook, canary post-Gemini-3) and it is nearly free; v2 has no tripwire to detect scored-set leakage into model history. **Fix:** embed a canary GUID per fixture family; run detection on the scored set before each campaign and log the result.
3. **What:** Record in the bench docs the eval-awareness risk class (Anthropic BrowseComp incident) as a design note for C8 trials. **Why:** our SUT is a coding agent with tool access; a model that recognizes it is being scored could game graded artifacts even with sealed fixtures. **Fix:** add to v2 §8 an explicit "SUT must not be told a fixture is scored" control and treat any such detection as a catastrophic-cell signal.
