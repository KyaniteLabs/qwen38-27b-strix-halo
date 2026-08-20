# Vision real-screenshot battery — 6/6 on real browser-rendered UI (2026-08-20)

## Finding
The champion (Qwen3.8-27B UD-Q4_K_XL + mmproj-F16) answers questions about REAL
screenshots — not synthetic color-patch VQA — at **6/6** on a pre-registered
6-fixture pilot: bar chart, data table, web form, terminal output, progress
bars, line chart. Every fixture was rendered by a real browser engine (Chrome
via Playwright, served over localhost HTTP) and screenshotted; ground truth is
known from the fixture sources. Wall time 4.0–4.9s per answer, all
finish_reason=stop, zero thinking leakage (think=0ch), temp 0, thinking OFF.

This is the first screenshot→answer evidence on this rig (OSWorld-adjacent
question class: "look at the screen, answer the question"), one rung stronger
than the 5/6 PIL-JPEG VQA battery in `../vision-2026-08-19/`.

## Per-cell results
| # | Fixture | Question | Expected | Answer | Wall |
|---|---------|----------|----------|--------|------|
| R1 | bar-chart.png | highest-revenue product | beta | Beta | 4.0s |
| R2 | table.png | billing-worker latency (ms) | 312 | 312 | 4.4s |
| R3 | form.png | prefilled email | simon@kyanitelabs.tech | simon@kyanitelabs.tech | 4.9s |
| R4 | terminal.png | failed health-check code | 503 | 503 | 4.5s |
| R5 | progress.png | task closest to completion | music-library | music-library | 4.2s |
| R6 | line-chart.png | MAU trend Jan→Jun | up | up | 4.4s |

Grading = case-insensitive keyword match, decided at authoring time (in
`vision-battery-real.py`, committed beside the raw logs).

## Conditions
GMKtec EVO-X2 ($1,400), Ryzen AI Max+ 395, 96GB unified. Champion weights
(bee238bb blob) + mmproj-F16, q4_0 K+V, 262,144 ctx, MTP n12 + ngram capped,
llama.cpp dflash build WITH the c7d8722 revert (46aa138f3). Served on a
dedicated :46399 window (champion :46377 stopped; trap-restored + verified
q4_0 after — see `vision-real-driver.log`). Text-only positive control passed
before the battery. Window driver: `components/exp-2026-08-19/vision-real-window.sh`
in the nucbox-stack repo (same file shipped to the box).

## Verdict class (P13)
Pilot, n=6, one run. 6/6 is a PASS for the capability question "can it read
real UI screenshots at all" — not a calibrated accuracy estimate for
OSWorld-class suites. CI on n=6 at 6/6 hits would be wide; treat as
directional-labeled evidence. Thinking-ON arm not run for this battery
(vision thinking pays nothing per `../vision-2026-08-19/` think A/B).

## Raw logs
- `vision-real-results.log` — the 6 cells + `ROWS=6` sentinel (P10)
- `vision-real-driver.log` — window driver: dry-run gate 6/6, champion
  stop/restore with q4_0 readback, server health + load time, control probe
- `vision-real-dryrun.log` — manifest validity check output
- `vision-battery-real.py` — the harness (dry-run mode included)
- `fixtures/` — the 6 PNGs (what the model saw) + the 6 HTML sources
  (ground truth provenance)
