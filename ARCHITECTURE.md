# Serving/measurement kit architecture

`components/` holds dated environment/INI/prefix assets, `components/bench/` holds instruments, [bench.sh](bench.sh) runs the sequence, and `results/`/methodology preserve interpretation. The actual serving process, model weights and hardware are external prerequisites.

```text
separately provisioned llama-server <- loopback HTTP requests from instruments
 -> streamed response/timing/grades -> raw result files -> methodology-bound claim
```

The shell reproducer defaults to port 46377, checks `/v1/models`, then runs repeated counting, time-per-task, quality and rewrite probes. Some quality/rewrite outputs use fixed `/tmp` paths. [qwen27-bench.py](components/bench/qwen27-bench.py) POSTs streamed chat completions, counts reasoning/content chunks and prints time/rate summaries. It executes on import; do not import it merely to discover functions. Profile/env files are text examples, not a service lifecycle manager.

## Risks / failure modes

- Running a bench targets an existing model service and consumes substantial inference memory/time; it is not a read-only/no-load host check. The shell's positional argument is a port, not a safe `--help` mode.
- Fixed result paths can replace earlier artifacts. A quality runner failure is echoed and does not necessarily terminate the complete shell run; inspect every stage, not shell exit alone.
- Content chunk count is not generally tokenizer count. Server defaults, reasoning caps, speculative repetition and cold/warm/prefill regimes can confound comparisons. Preserve corrections and quarantined instrument-era results.
- Dated profile files disagree with later README champion settings. Applying ROCm/cache/context knobs without current resource/rollback/owner review can hang or displace other inference; no settings are applied by this docs change.

## Docs verification

Purpose/methodology, shell, dated profiles/env and actual SSE instrument inspected. Shell/Python syntax and injected synthetic SSE parsing passed. No network/model, services, benchmark generation, hardware measurement or production configuration. Historical results were not independently reproduced; no current host/performance acceptance claimed. Revert docs for rollback.
