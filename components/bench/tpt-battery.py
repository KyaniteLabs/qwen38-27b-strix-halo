import json, time, urllib.request, sys

# tpt-battery.py PORT TAG — the time-per-task instrument: 5 fixed auto-graded
# tasks (reason/json/tool/code/riddle), reports wall-clock seconds + completion
# tokens per correct task. n>=3 runs recommended; decode tok/s is not task latency.

PORT = sys.argv[1] if len(sys.argv) > 1 else "46377"
TAG = sys.argv[2] if len(sys.argv) > 2 else "run"
URL = f"http://127.0.0.1:{PORT}/v1/chat/completions"

TOOLS = [{"type": "function", "function": {
    "name": "read_file", "description": "Read a file from disk",
    "parameters": {"type": "object",
                   "properties": {"path": {"type": "string"}},
                   "required": ["path"]}}}]

def run(messages, max_tokens, tools=None):
    body = {"messages": messages, "max_tokens": max_tokens,
            "chat_template_kwargs": {"enable_thinking": True}}
    if tools:
        body["tools"] = tools
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        j = json.load(r)
    dt = time.time() - t0
    m = j["choices"][0]["message"]
    u = j.get("usage", {})
    return dt, (m.get("content") or ""), m.get("tool_calls"), u

def g_reason(c, tc, u):
    cc = c.replace(",", ".").replace(" ", "")
    return ("neither" in c.lower()
            and ("9.5" in cc or "19/2" in cc or "9\u00bd" in c))

def g_json(c, tc, u):
    try:
        return json.loads(c.strip()) == {"status": "ok", "items": [1, 2, 3]}
    except Exception:
        return False

def g_tool(c, tc, u):
    if not tc:
        return False
    try:
        f = tc[0]["function"] if isinstance(tc[0], dict) else tc[0].function
        name = f["name"] if isinstance(f, dict) else f.name
        args = f["arguments"] if isinstance(f, dict) else f.arguments
        return name == "read_file" and json.loads(args).get("path") == "/tmp/notes.txt"
    except Exception:
        return False

def g_code(c, tc, u):
    return ("def longest_palindrome" in c and "return" in c
            and ("while" in c or "for" in c))

def g_riddle(c, tc, u):
    return c.strip().startswith("9")

TASKS = [
    ("reason", g_reason, [{"role": "user", "content":
        "Compute 9+10, then multiply by 0.5, then tell me if the final result is odd or even. Show each step."}],
     800, None),
    ("json", g_json, [{"role": "user", "content":
        'Return ONLY valid JSON, no other text: {"status": "ok", "items": [1, 2, 3]}'}],
     600, None),
    ("tool", g_tool, [{"role": "user", "content":
        "Use the read_file tool to read /tmp/notes.txt"}],
     800, TOOLS),
    ("code", g_code, [{"role": "user", "content":
        "Write a Python function longest_palindrome(s) that returns the longest palindromic substring. Include a one-line comment on the approach."}],
     1600, None),
    ("riddle", g_riddle, [{"role": "user", "content":
        "A farmer has 17 sheep. All but 9 run away. How many sheep does he have left? Answer with the number first, then one sentence why."}],
     800, None),
]

total_t = total_tok = passed = 0
for tag, grader, msgs, mt, tools in TASKS:
    dt, c, tc, u = run(msgs, mt, tools)
    ok = grader(c, tc, u)
    comp = u.get("completion_tokens", 0)
    det = (u.get("completion_tokens_details") or {}).get("reasoning_tokens", "?")
    if ok:
        passed += 1; total_t += dt; total_tok += comp
    print(f"{TAG} {tag}: {'PASS' if ok else 'FAIL'}  {dt:.1f}s  completion_tokens={comp} (reasoning={det})")
    if not ok:
        print(f"  FAIL-CONTENT: {c[:200]!r}")

print(f"{TAG} SUMMARY: {passed}/5 passed | seconds-per-correct-task {total_t/max(passed,1):.1f} | "
      f"tokens-per-correct-task {total_tok/max(passed,1):.0f} | total wall {total_t:.1f}s")
