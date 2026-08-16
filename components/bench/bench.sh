#!/usr/bin/env bash
# bench.sh — one-command reproducer for the qwen38-27b-strix-halo numbers.
# PREP-ONLY: staged in halo-collab/launch; lands in the repo root (or
# components/bench/) at T-1 with Simon's approval.
#
# Requires: a running llama-server with the champion flags (see README
# quickstart) and python3. Everything talks HTTP to localhost only.
#
# Usage:
#   ./bench.sh [port]        # default port 46377 (production)
#
# What it runs (all instruments from components/bench/):
#   1. count-to-30 x3 back-to-back  -> run 1 = cold, runs 2-3 = warm
#                                      (warm with ngram = repetition artifact,
#                                      label it as such in any public number)
#   2. tpt-battery x3               -> time-per-task (the primary metric)
#   3. quality suite x1             -> 6/6 expected on the champion
#   4. rewrite bench x2             -> agent file-echo pattern (warm)
# Then prints a filled numbers block — paste it into a "Post your numbers"
# issue (NUMBERS-TEMPLATE) with your hardware line.

set -euo pipefail

PORT="${1:-46377}"
DIR="$(cd "$(dirname "$0")" && pwd)"
BENCH="$DIR/components/bench"
[ -d "$BENCH" ] || BENCH="$DIR"   # allow living inside components/bench itself
PY=python3

echo "== bench.sh — Qwen3.8-27B on Strix Halo reproducer =="
echo "   bench dir : $BENCH"
echo "   endpoint  : http://127.0.0.1:$PORT"

if ! curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null 2>&1; then
  echo "ERROR: no llama-server on port $PORT (or curl missing)."
  echo "       Start it with the README quickstart flags, then re-run."
  exit 1
fi

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo
echo "== 1/4 count-to-30 x3 (run 1 = cold; runs 2-3 = warm ngram artifact) =="
for i in 1 2 3; do
  echo "-- c30 run $i:"
  "$PY" "$BENCH/qwen27-bench.py" "Count from 1 to 30, comma separated, nothing else." "$PORT"
done

echo
echo "== 2/4 time-per-task battery x3 (primary metric; n>=3 for verdicts) =="
for i in 1 2 3; do
  echo "-- tpt run $i:"
  "$PY" "$BENCH/tpt-battery.py" "$PORT" "benchsh-$i"
done

echo
echo "== 3/4 quality suite (expect 6/6 on the champion; palindrome needs a"
echo "      1200-token budget — a known budget artifact, not a regression) =="
"$PY" "$BENCH/qwen-quality.py" "$PORT" "/tmp/benchsh-quality.json" || \
  echo "      (quality runner exited nonzero — see /tmp/benchsh-quality.json)"

echo
echo "== 4/4 file-rewrite echo pattern x2 (warm; agent-loop shape) =="
"$PY" "$BENCH/juice-mkrewrite.py"
for i in 1 2; do
  echo "-- rewrite run $i:"
  "$PY" "$BENCH/qwen27-bench.py" "$(cat /tmp/juice-rewrite-prompt.txt)" "$PORT"
done

echo
echo "== numbers block (paste into a 'Post your numbers' issue) =="
cat <<EOF
---8<---
**Measured (UTC):** $TS
**Port / stack:** $PORT (llama.cpp b10435+, ROCm, flags per README quickstart)

**c30 throughput (tok/s):** cold = [run 1] · warm = [runs 2-3]  <- warm = ngram repetition artifact, label it
**time-per-task (x3):** [s/task @ tokens, per run]
**quality suite:** [n]/6
**rewrite/echo (warm):** [tok/s, run 1 / run 2]
**hardware:** [APU / memory / clocks]
**notes:** [anything unusual — thermal, background load, different flags]
---8<---

Reference bands on our box (champion, 2026-08-15): c30 59.7 cold / 148-163
warm-artifact / real prose 11-24; tpt 7.6-7.7s @ ~170 tok; rewrite 72-133.
Outside our bands is a valid result — post it anyway; outliers get published
as data, not arguments.
EOF
