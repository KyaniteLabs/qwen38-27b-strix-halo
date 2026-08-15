import json, time, urllib.request, sys, random

# juice-ttft.py PORT PROMPTFILE [runs] — long-prompt TTFT bench.
# Prepends a unique nonce per run so the server prefix-cache can't serve
# cached tokens (honest prompt-processing numbers every run).
PORT = sys.argv[1] if len(sys.argv) > 1 else "46381"
PF = sys.argv[2] if len(sys.argv) > 2 else "/tmp/juice-longprompt.txt"
RUNS = int(sys.argv[3]) if len(sys.argv) > 3 else 3

body_text = open(PF).read()
for i in range(RUNS):
    prompt = f"[ref {random.randint(1_000_000, 9_999_999)}]\n{body_text}"
    body = json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 40, "stream": True,
        "chat_template_kwargs": {"enable_thinking": False},
    }).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json"})
    t0 = time.time(); first = None; n = 0; usage = None
    with urllib.request.urlopen(req, timeout=600) as r:
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
            if j.get("usage"):
                usage = j["usage"]
            delta = (j.get("choices") or [{}])[0].get("delta", {})
            if delta.get("content"):
                if first is None:
                    first = time.time() - t0
                n += 1
    pt = usage["prompt_tokens"] if usage else -1
    ttft = first if first else -1
    pps = pt / ttft if (ttft > 0 and pt > 0) else 0
    print(f"run{i+1}: prompt_tokens={pt}  TTFT={ttft:.2f}s  PP-speed={pps:.0f} tok/s  gen={n} chunks")
