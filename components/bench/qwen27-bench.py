import json, time, urllib.request, sys

# qwen27-bench.py [prompt] [port] — streamed count-to-30 throughput bench
# (1 content chunk == 1 token). Default port 46377 = production; the ledger's
# test-server runs used 46381. Run 3x back-to-back: run 1 is cold, runs 2-3
# show the ngram warm effect. Acceptance/mean-len come from the server journal.
prompt = sys.argv[1] if len(sys.argv) > 1 else "Count from 1 to 30, comma separated, nothing else."
PORT = sys.argv[2] if len(sys.argv) > 2 else "46377"
body = json.dumps({"messages": [{"role": "user", "content": prompt}], "max_tokens": 250, "stream": True}).encode()
req = urllib.request.Request(f"http://127.0.0.1:{PORT}/v1/chat/completions", data=body,
                             headers={"Content-Type": "application/json"})
t0 = time.time(); first = None; last = None; n = 0; nreason = 0
with urllib.request.urlopen(req, timeout=180) as r:
    for raw in r:
        line = raw.decode(errors="replace").strip()
        if not line.startswith("data:"):
            continue
        d = line[5:].strip()
        if d == "[DONE]" or not d:
            continue
        try:
            j = json.loads(d)
        except Exception:
            continue
        delta = (j.get("choices") or [{}])[0].get("delta", {})
        if delta.get("reasoning_content"):
            nreason += 1
        if delta.get("content"):
            now = time.time() - t0
            if first is None:
                first = now
            last = now
            n += 1
span = (last - first) if (last and first and last > first) else 0
first = first if first is not None else 0.0
last = last if last is not None else 0.0
print(f"reasoning chunks: {nreason}  content chunks: {n}  first content: {first:.2f}s  "
      f"total: {last:.2f}s  content speed: {(n/span if span else 0):.1f} tok/s")
