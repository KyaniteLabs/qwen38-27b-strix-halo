import json, time, urllib.request, sys

# tpt-style.py PORT TAG MARKER — the style A/B runner: same 5 auto-graded tasks
# with a thinking-STYLE system prompt. 4 arms: "-" baseline, "caveman", "ponytail",
# "both" (fused). Steering, never caps; n>=3 runs for sustained numbers.

PORT = sys.argv[1] if len(sys.argv) > 1 else "46377"
TAG = sys.argv[2] if len(sys.argv) > 2 else "run"
MARK = sys.argv[3] if len(sys.argv) > 3 else "-"

STYLES = {
    "-": None,
    "caveman": ("SYSTEM: Your INTERNAL REASONING follows caveman rules. Reason in short "
                "fragments, 3-8 words each. Prefer action over explanation. No motivational "
                "filler. No restating the problem. No step-by-step narration unless the task "
                "truly needs it. When confidence is high, decide and move. Structure thoughts "
                "as: finding / fix / next. Grunt the essentials, then answer. Only the final "
                "visible answer uses normal language."),
    "ponytail": ("SYSTEM: You are a lazy senior developer reasoning internally. Lazy means "
                 "efficient, not careless. Stop at the first thought that holds: if you "
                 "already know the answer, state it and stop. Never re-derive what you "
                 "already know. Never explore alternatives when the first one works. The "
                 "best reasoning is the reasoning never thought. One mental line beats "
                 "five. Only the final visible answer uses normal language."),
    "both": ("SYSTEM: Your INTERNAL REASONING is caveman + lazy-senior-dev. Reason in short "
             "fragments, 3-8 words each. If you already know the answer, state it and stop. "
             "Never re-derive what you know. Structure: finding / fix / next. The best "
             "reasoning is the reasoning never thought. Grunt essentials, then answer. "
             "Only the final visible answer uses normal language."),
}

sysmsg = STYLES[MARK]
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
    return time.time() - t0, (j["choices"][0]["message"].get("content") or ""), \
        j["choices"][0]["message"].get("tool_calls"), j.get("usage", {})

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
    ("reason", g_reason, "Compute 9+10, then multiply by 0.5, then tell me if the final result is odd or even. Show each step.", 800, None),
    ("json", g_json, 'Return ONLY valid JSON, no other text: {"status": "ok", "items": [1, 2, 3]}', 600, None),
    ("tool", g_tool, "Use the read_file tool to read /tmp/notes.txt", 800, TOOLS),
    ("code", g_code, "Write a Python function longest_palindrome(s) that returns the longest palindromic substring. Include a one-line comment on the approach.", 1600, None),
    ("riddle", g_riddle, "A farmer has 17 sheep. All but 9 run away. How many sheep does he have left? Answer with the number first, then one sentence why.", 800, None),
]

mark_print = MARK
total_t = total_tok = passed = 0
for tag, grader, q, mt, tools in TASKS:
    msgs = ([{"role": "system", "content": sysmsg}] if sysmsg else []) + \
           [{"role": "user", "content": q}]
    dt, c, tc, u = run(msgs, mt, tools)
    ok = grader(c, tc, u)
    comp = u.get("completion_tokens", 0)
    if ok:
        passed += 1; total_t += dt; total_tok += comp
    print(f"{TAG}/{mark_print} {tag}: {'PASS' if ok else 'FAIL'}  {dt:.1f}s  tok={comp}")
    if not ok:
        print(f"  FAIL-CONTENT: {c[:160]!r}")

print(f"{TAG} SUMMARY[{mark_print}]: {passed}/5 | {total_t/max(passed,1):.1f}s/task | "
      f"{total_tok/max(passed,1):.0f} tok/task | wall {total_t:.1f}s")
