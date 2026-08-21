# Ornith-1.5-35B-A3B (Q4_K_M) rehearsal window — first public Strix-Halo 35B cell (2026-08-21)

Plan: consensus v3 + TEXT-ONLY annotation (ralplan 2-round APPROVE, ultraqa 3/4).
Window: 2026-08-21 00:44:40Z-01:08:39Z (24 min wall, budget 2.5h). Champion stopped
for the window, restored after with q4_0 KV readback. Balanced pmode throughout.
One server launch per cell (restart-verified), no --cache-reuse, no mmproj.
Model: Ornith-1.5-35B-Q4_K_M.gguf (SHA_MATCH at download, re-hashed at staging).
Harness: seed 7719 haystack, needle `Station HERON access code: GRANITE-4417-OMEGA.`
at ~51-52% depth, fill targets ctx-300 with +-1% server-side token assert
(measured: 32483/32468 and 130715/130772).

## Speed (paired walls; tok/s diagnostic only)

| cell | ctx | KV | spec | result |
|---|---|---|---|---|
| A | 131072 | q4_0 | ON (champion-mirrored) | 11.3s mean per 200-tok prose (3 problems, byte-identical set) |
| B | 131072 | q4_0 | OFF | **3.6s mean** — same 3 problems |

**Spec verdict (paired same-problem walls): speculative config OFF is 3.1x faster
at empty context.** At 128k loaded: decode 200 tok = 15.4s (off) vs 18.0s (on);
131k prefill = 359s (off) vs 388s (on). Every wall class tonight favors OFF.
The 27B champion's draft-mtp+ngram-mod mirror HURTS this model on this build —
do not carry it into fire-35b.sh. (Ngram-ONLY arm not separately measured; MTP
acceptance on the probe warmup was 0.33 — consistent with ICCO's adopted
ngram-default / MTP-opt-in design.)

Prefill rate: 32k = 53s (613 tok/s); 128k = 364 tok/s (spec-off).
Decode at 128k: 12.9 tok/s (spec-off) / 11.1 tok/s (spec-on). Balanced pmode class.

## Retrieval (exact needle, arbitrary alphanumeric code, pilot n=1/cell)

| cell | loaded ctx | needle depth | quote wall | score |
|---|---|---|---|---|
| D | 32768 (q8_0 KV) | 51% | 2.0s | HIT exact, fr=stop |
| E | 130715 (q4_0 KV, spec-off) | 52% | 3.5s | HIT exact, fr=stop |
| F | 130715 (q4_0 KV, spec-on) | 52% | 4.0s | HIT exact, fr=stop |

Existence 0.4-0.9s, one-sentence summary 3.2-5.3s on the same loaded contexts
(fork-not-mutate: full history re-attached per follow-up).
C (32k q4_0 KV) fill landed but decode+warm was lost to a watchdog kill (below).

A 35B-class MoE on this $1,400 rig retrieves exact arbitrary codes from a
131,072-token context in under 4 seconds, with warm follow-ups under 5.3s.

## Labels (P13)
- Pilot class: n=1 per cell; walls are the claim, tok/s diagnostic; power mode
  balanced (never compare across power modes).
- tb/ta in raw rows are Tctl (control temp) — spike class 84-97C during sub-10s
  decode bursts while the logged EDGE stayed 44-74C; two different sensors, both
  raw files preserved. Prefill runs: edge 67-74C sustained, within envelope.
- Spec states for E/F were decided by the A/B paired walls (E=off winner, F=on).
- /metrics spec counters: this build returned none (empty grep sections in
  ornith-window-metrics.log) — acceptance evidence lives in the server logs'
  `draft acceptance` timing lines (see server-E/F logs).

## Events
- 00:48:20Z single CSV row `96.0C / 115.0W` sandwiched between 12W and 11W rows
  (115W is outside every observed load class tonight) tripped the pre-registered
  95C-instant watchdog rule; cell C lost only its decode+warm rows (partial
  appends worked as designed; fill row survived). The identical step ran clean
  in cells D/E/F with edge <=74C — second confirmed instance of the S-074-class
  single-row sensor artifact, this one above the instant line. Registered as
  S-085 in the stack repo.
- KV-size wording absent from this build's server logs (wide re-grep, see stack
  RUNBOOK/queue); the GTT guard rode direct load-class evidence instead: the
  probe loaded model+mmproj+drafter at n_ctx_slot=131072, and all four 131072
  window loads succeeded (kv-evidence file).

## CEO-ruling note (disclosed)
The CEO's standing ruling tonight: nothing larger than Q4. Cell D measured the
q8_0 KV cache setting in a stopped-champion measurement cell per the
pre-approved launch list (A-F). No serving config used anything above Q4.
If the ruling was meant to cover measurement cells too, this cell's rows should
be struck on his word — flagged to him in the session report.

## Raw
- `ornith-window-results.log` — all 26 rows
- `ornith-window-driver.log` — full driver log incl. gates, kills, restores
- `ornith-window-server-[A-F].log` — per-launch server logs (restart evidence)
- `ornith-window-kv-evidence.log`, `ornith-window-metrics.log`, `ornith-window-dryrun.log`
- Instruments: qwen27-nucbox-stack components/exp-2026-08-19/ornith-window*.sh,
  ornith-cells.py, test-ornith-window.sh (65/65 self-test; critic round applied)
