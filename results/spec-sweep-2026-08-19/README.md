# Spec-stack sweep (2026-08-19, 5-arm A/B on champion @262k q4_0)
All arms: c30 warm x3 median + prose-150 spot. Champion config throughout (Q4_K_XL @262k, K+V q4_0).

| Arm | c30 median | Prose tok/s | Finding |
|-----|-----------|-------------|---------|
| uncapped (current) | 1.5s | 10.8 | baseline |
| capped-n12 | 1.5s | 11.0 | cap is FREE (same speed, better prose) |
| mtp-solo | 1.9s | 10.7 | ngram drafter adds value |
| ngram-capped-solo | 3.4s | 11.3 | best prose but 2.3x slower c30 |
| spec-off | 7.5s | 11.1 | spec = 5x speedup on repetition |

Key findings:
1. Spec decoding is worth 5x on repetition-heavy tasks (c30: 1.5s vs 7.5s)
2. --spec-ngram-mod-n-max 12 cap costs NOTHING — should be added to champion
3. MTP + ngram together beat either alone (dual-drafter confirmed)
4. Prose ~10-11 tok/s regardless of spec config (spec helps repetition, not open-ended)
