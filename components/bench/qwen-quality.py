import json, time, urllib.request, sys

# Reconstructed 2026-08-15 from ~/workspaces/qwen27-nucbox-stack/quality-q4.json
# (original /tmp/qwen-quality.py lost in NUC reboot 04:18Z).
# 6-prompt fixed suite, thinking FORCED ON via chat_template_kwargs so it is
# valid against both default-off and default-on servers.
# Usage: python3 qwen-quality.py [port] [outfile]

PORT = sys.argv[1] if len(sys.argv) > 1 else "46377"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/quality-run.json"

SUITE = [
    ("riddle", "A farmer has 17 sheep. All but 9 run away. How many sheep does he have left? Answer with the number, then one sentence why."),
    ("code", "Write a Python function longest_palindrome(s) that returns the longest palindromic substring. Include a one-line comment on the approach."),
    ("precision", "Reply with EXACTLY four words, no punctuation, describing the ocean."),
    ("explain", "Why does LLM inference speed scale with memory bandwidth instead of raw compute? Answer in exactly two sentences."),
    ("persona", "In the voice of a cocky, explosion-loving agent, decline a calendar invite in exactly two sentences."),
    ("multistep", "Compute 9+10, then multiply by 0.5, then tell me if the final result is odd or even. Show each step on its own line."),
]

results = []
for tag, prompt in SUITE:
    body = json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "stream": True,
        "chat_template_kwargs": {"enable_thinking": True},
    }).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json"})
    t0 = time.time()
    reasoning, content, usage = [], [], None
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
            if delta.get("reasoning_content"):
                reasoning.append(delta["reasoning_content"])
            if delta.get("content"):
                content.append(delta["content"])
    results.append({
        "tag": tag, "prompt": prompt, "secs": round(time.time() - t0, 1),
        "reasoning": "".join(reasoning), "content": "".join(content),
        "usage": usage,
    })
    print(f"{tag}: {results[-1]['secs']}s  content_len={len(results[-1]['content'])}  "
          f"reason_len={len(results[-1]['reasoning'])}", flush=True)

with open(OUT, "w") as f:
    json.dump(results, f, indent=1)
print(f"wrote {OUT}")
