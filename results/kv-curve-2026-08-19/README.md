# KV-cache curve — 2026-08-19

Archived per-sample results and paired summaries comparing the recorded `q8`
control with three lower-precision KV-cache treatments. This README describes
the adjacent logs; it does not represent a new benchmark run.

## Files and recorded labels

| Per-sample JSONL | `kv` label in records | Paired summary vs `q8` |
| --- | --- | --- |
| `q4kv-results-q8.jsonl` | `q8` | control |
| `q4kv-results-q4.jsonl` | `q4` | `summary-q8vq4.json` |
| `q4kv-results-q5_0.jsonl` | `q5` | `summary-q8vq5_0.json` |
| `q4kv-results-q5_1.jsonl` | `q6` | `summary-q8vq5_1.json` |

The filenames and record labels differ for the last two treatments; the table
preserves both without inferring an undocumented cache-type mapping. JSONL
records include sample index, decile, correctness, wall time, extracted and
expected answers, token counts, anomaly flags, and timestamp.

## Recorded paired results

Each summary reports 60 paired samples. Control and treatment accuracy are
96.6667% in every comparison, with a 0 percentage-point difference, zero
discordant pairs, McNemar p = 1.0, and empty anomaly lists.

| Recorded label | Mean wall time (seconds) |
| --- | ---: |
| `q8` (control) | 19.1147 |
| `q4` | 19.6363 |
| `q5` | 26.9910 |
| `q6` | 24.1975 |

These are results for this archived sample set only, not proof of general
quality equivalence or a fresh hardware/performance verification. Consult the
JSONL rows and summary JSON files for full precision and recorded timestamps.
