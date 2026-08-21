# The Delegation Benchmark — a "safe to hand off my work" benchmark for local models

PRE-REGISTRATION NOTICE: this design is published BEFORE any run. No
measurement exists yet; nothing can be tuned after the fact. The first run
happens when the product under test freezes; results will land beside this
file with every raw log, exactly like everything else in this repo.

THE QUESTION IT ANSWERS: which of the operator's real jobs can be safely
delegated — consistently — to a local model (Qwen3.8-27B on a $1,400 Strix
Halo) running inside the actual product built around it (tokflint/tokpal)?
Not "is the model smart" — "can you hand it work and walk away."

WHY IT DOESN'T EXIST ELSEWHERE (per the research files beside this design):
the pieces exist — capability leaderboards, injection-safety suites, judge
protocols, freshness methods — but no published benchmark composes them into
a personal delegation decision with certified floors, a separate walk-away
(autonomy) tier, ask-quality scoring, and split-recovery tests for automatic
task decomposition. The ask-quality rubric has no standard form anywhere yet.

WHAT IS HERE:
- DESIGN.md — the full pre-registered design (v3.1): 9 job classes, size
  ladders, the single decision table with exact confidence floors printed on
  every result (15/15 = at least 82%; 30/30 = at least 90%), the computed
  honesty table (probability the test says green at any true skill level),
  blinded dual-judge protocol, hidden-test oracles, a sabotage safety cell,
  sealed holdouts with shelf life, and the four decomposition measurements.
- research/W1-W3 — the three sourced research passes (contamination and
  private-bench operations; statistics and oracle gaming; judging, safety
  precedent, decision evals). Every claim carries a named source and date.

WHAT WILL NEVER BE HERE: the sealed holdout set. We publish the sealing
method (hash-manifest before first run), never the contents — that is what
keeps our own green honest.

THREE-STAGE PUBLICATION: (1) this design, now, before any run; (2) the
runner, open source with template fixtures and a fixture generator, when
built; (3) the results and the operator's delegation card, when measured.

License: same as this repo. The design is the artifact; the audit trail
(internal review + external audit + field research) is summarized in
DESIGN.md's lineage block.
