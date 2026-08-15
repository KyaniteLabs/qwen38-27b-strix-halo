import json, time, urllib.request, sys

prompt = sys.argv[1] if len(sys.argv) > 1 else "Count from 1 to 30, comma separated, nothing else."
body = json.dumps({"messages": [{"role": "user", "content": prompt}], "max_tokens": 250, "stream": True}).encode()
req = urllib.request.Request("http://127.0.0.1:46377/v1/chat/completions", data=body,
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
