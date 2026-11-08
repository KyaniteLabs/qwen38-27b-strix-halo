# Qwen3.8-27B on Strix Halo

A reproducible serving-profile and measurement kit for running Qwen3.8-27B with llama.cpp/ROCm on AMD Strix Halo. Its useful experience is read the regime/method, configure a separately approved server, run the instrument, and compare within-condition results—not install a universal high-speed assistant.

## Existing assets

- Serving/env profile examples, agent prefix and a shell reproducer with seven Python bench instruments for throughput, latency, quality and rewrite/context probes.
- Methodology, raw/result ledgers including GSM8K/reasoning-budget and Omni-MATH comparisons, and documented corrections/quarantined measurements.
- A linked Delegation Benchmark project. Its certification claims belong to their exact conditions, not a blanket permission to delegate any job.

README's final profile is 262,144 context with q4_0 KV; the included August 15 INI/env examples still describe 98,304/f16-era settings. Treat them as dated assets, not interchangeable current production configuration. No model weights or llama.cpp runtime are supplied by this repository.

## Proof and limits

Shell syntax and seven Python AST parses passed. The actual SSE instrument consumed synthetic injected frames and counted one reasoning/two content chunks without network. That is parser proof, not model speed, accuracy, context retrieval or deployment acceptance.

All published numbers are historical single-box, build/thermal/prompt-regime-specific receipts; warm repeated counting is explicitly an artifact class. The small streaming script equates content chunks with tokens, which is not valid for arbitrary SSE providers. No live model endpoint, host/service/config, GPU memory, paid provider or publication was touched. See [ARCHITECTURE.md](ARCHITECTURE.md), [METHODOLOGY.md](METHODOLOGY.md) and [README.md](README.md).
