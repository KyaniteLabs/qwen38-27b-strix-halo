#!/usr/bin/env python3
"""LiveCodeBench-30 subset on the champion — 2026-08-20 CS session (COO-003 dispatch).

PRE-REGISTERED CONDITIONS (NOT card-comparable; label all numbers):
- Source: livecodebench/code_generation_lite test6.jsonl (release v6, 175 problems,
  contest window ~May 2025). Subset: 10 easy / 10 medium / 10 hard, deterministic
  selection seed 20260820 (sort by question_id then random.sample per difficulty).
- Serving: champion Q4_K_XL @262k, q4_0 KV, MTP+ngram capped, c7d8722-reverted build,
  temp 0.0, thinking OFF, max_tokens 2048. SHARED-SLOT label: another lane's API
  traffic interleaves on -parallel 1 during this run; scores unaffected (greedy,
  per-request), wall times inflated.
- Grading: PUBLIC test cases only (lite split withholds private cases — slight
  optimistic bias vs official leaderboard); up to 20 cases per problem, early-exit
  on first failure; stdin testtype = feed input, strip-compare stdout; functional
  testtype = parse JSON args, instantiate starter class, call entry method,
  pass if json.dumps(result) OR str(result) matches expected (dual-encode rule).
- Execution sandbox: python3 subprocess, 10s timeout per case, temp file per problem.
- Card anchor: Qwen3.8-27B official LCB 90.3 (bf16, full official harness, private
  tests). Our number = a different instrument (Q4, temp 0, no thinking, public-only,
  30-problem subset) — band-check only, no equivalence claim.
- Verdict class: pilot n=30. P10: dedicated results file + ROWS sentinel.
  P11: dry-run proves grader (known-good solution MUST pass; garbage MUST fail).
"""
import json, os, random, re, subprocess, sys, tempfile, time, urllib.request

DATASET = os.environ.get("LCB_DATASET", os.path.join(os.path.dirname(os.path.abspath(__file__)), "lcb-test6.jsonl"))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get("LCB_OUT", "lcb-30-results.log"))
MAXTOK = int(os.environ.get("LCB_MAX_TOKENS", "2048"))
ONLY = set(os.environ.get("LCB_ONLY", "").split(",")) - {""}
URL = os.environ.get("BENCH_URL", "http://127.0.0.1:46377/v1/chat/completions")
LABEL = os.environ.get("LCB_LABEL", "champion-q4-lcb30")
N_PER_DIFF = 10
MAX_CASES = 20

PROMPT_PREFIX = (
    "You are an expert Python programmer. You will be given a question (problem "
    "specification) and will generate a correct Python program that matches the "
    "specification and passes all tests.\n\n"
)
PROMPT_SUFFIX = (
    "\n\nRead input from standard input and write output to standard output. "
    "Provide the complete Python solution in a single ```python code block."
)

def select_subset(rows):
    rng = random.Random(20260820)
    subset = []
    for diff in ("easy", "medium", "hard"):
        pool = sorted([r for r in rows if r["difficulty"] == diff], key=lambda x: x["question_id"])
        subset += rng.sample(pool, N_PER_DIFF)
    return subset

def build_prompt(r):
    p = PROMPT_PREFIX + (r["question_content"] or "")
    sc = (r.get("starter_code") or "").strip()
    if sc:
        p += "\n\n" + sc
    return p + PROMPT_SUFFIX

THINK = os.environ.get("LCB_THINK", "0") == "1"
THINK_BUDGET = int(os.environ.get("LCB_THINK_BUDGET", "2048"))

def ask(prompt):
    kwargs = {"enable_thinking": THINK}
    body = {"messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAXTOK, "temperature": 0.0,
            "chat_template_kwargs": kwargs}
    if THINK:
        body["reasoning_budget_tokens"] = THINK_BUDGET
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        j = json.load(r)
    return j, time.time() - t0

def extract_code(text):
    blocks = re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)
    if blocks:
        return blocks[0]
    blocks = re.findall(r"```\s*\n(.*?)```", text, re.DOTALL)
    if blocks:
        return blocks[0]
    if "def " in text or "class " in text:
        return text
    return None

FUNC_WRAP = """
import json, sys
def _parse_arg(line):
    line = line.strip()
    try:
        return json.loads(line)
    except Exception:
        return line
if __name__ == "__main__":
    _raw = sys.stdin.read()
    _lines = [l for l in _raw.split(chr(10)) if l.strip() != ""]
    try:
        _args = json.loads(_raw)
        if not isinstance(_args, list):
            _args = [_args]
    except Exception:
        _args = [_parse_arg(l) for l in _lines]
    _sol = Solution()
    _out = _sol.{method}(*_args)
    try:
        print(json.dumps(_out))
    except (TypeError, ValueError):
        print(str(_out))
"""

def run_case(code, r, case):
    """Returns (passed, err)."""
    testtype = case.get("testtype", "stdin")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write("from typing import *\nimport math\nimport json\nimport re\n")
        f.write("import string\nimport copy\nimport random\n")
        f.write("from itertools import *\nfrom collections import *\nfrom functools import *\n")
        f.write("from heapq import *\nfrom bisect import *\nimport fractions\n")
        if testtype == "functional":
            sc = (r.get("starter_code") or "").strip()
            m = re.search(r"def\s+(\w+)\s*\(\s*self", sc)
            if not m:
                return False, "no-entry-method"
            guard = re.search(r"^if __name__ == .__main__.", code, re.M)
            body = code[:guard.start()] if guard else code
            f.write(body + "\n" + FUNC_WRAP.format(method=m.group(1)))
        else:
            f.write(code)
        path = f.name
    try:
        res = subprocess.run(["python3", path], input=case.get("input", ""),
                             capture_output=True, text=True, timeout=10)
        os.unlink(path)
        if testtype == "functional":
            return res.returncode == 0 and _func_match(res.stdout, case.get("output", "")), None
        return res.stdout.strip() == case.get("output", "").strip(), None
    except subprocess.TimeoutExpired:
        os.unlink(path)
        return False, "timeout"
    except Exception as e:
        if os.path.exists(path):
            os.unlink(path)
        return False, str(e)[:80]

def _func_payload(case):
    return case.get("input", "")

def _func_match(stdout, expected):
    got = stdout.strip()
    exp = expected.strip()
    if got == exp:
        return True
    try:
        return json.dumps(json.loads(got)) == json.dumps(json.loads(exp))
    except Exception:
        return False

def grade(code, r):
    cases = json.loads(r["public_test_cases"])[:MAX_CASES]
    for case in cases:
        ok, err = run_case(code, r, case)
        if not ok:
            return False, err or "case-mismatch", len(cases)
    return True, None, len(cases)

if __name__ == "__main__":
    rows = [json.loads(l) for l in open(DATASET)]
    subset = select_subset(rows)
    if ONLY:
        subset = [r for r in subset if r["question_id"] in ONLY]

    if "--dry-run" in sys.argv:
        # P11: grader must pass a known-good solution and fail garbage.
        easy = subset[0]
        print("[dry] problem:", easy["question_id"], easy["difficulty"])
        # a correct program for THIS problem cannot be hand-written generically;
        # instead prove grader mechanics: garbage must fail every case path.
        ok, err, n = grade("print('wrong')\n", easy)
        print(f"[dry] garbage-fails: passed={ok} err={err} cases={n} (want passed=False)")
        # stdin path end-to-end: trivial echo program against first case input
        c0 = json.loads(easy["public_test_cases"])[0]
        echo_ok, _ = run_case("import sys\nsys.stdout.write(sys.stdin.read())\n", easy,
                              {"input": c0["input"], "output": c0["input"], "testtype": "stdin"})
        print(f"[dry] echo-passes-self: {echo_ok} (want True)")
        okv, _ = run_case("import sys\nsys.stdout.write(sys.stdin.read())\n", easy, c0)
        print(f"[dry] echo-vs-real-expected: passed={okv} (real problem, real expected)")
        sys.exit(0)

    lines = []
    passed = 0
    for i, r in enumerate(subset):
        qid = r["question_id"]
        try:
            j, wall = ask(build_prompt(r))
            content = (j["choices"][0]["message"]["content"] or "").strip()
            fr = j["choices"][0].get("finish_reason")
            think_ch = len(j["choices"][0]["message"].get("reasoning_content") or "")
            code = extract_code(content)
            savedir = os.environ.get("LCB_SAVE")
            if savedir:
                os.makedirs(savedir, exist_ok=True)
                open(os.path.join(savedir, qid + ".py"), "w").write(code or "")
                open(os.path.join(savedir, qid + ".raw.txt"), "w").write(content)
            if code is None:
                lines.append(f"[{LABEL}] {qid} ({r['difficulty']}): FAIL no-code-extracted fr={fr} {wall:.0f}s think={think_ch}ch")
                continue
            ok, err, ncases = grade(code, r)
            if ok:
                passed += 1
                lines.append(f"[{LABEL}] {qid} ({r['difficulty']}): PASS {wall:.0f}s fr={fr} cases={ncases} think={think_ch}ch")
            else:
                lines.append(f"[{LABEL}] {qid} ({r['difficulty']}): FAIL ({err}) {wall:.0f}s fr={fr} cases={ncases} think={think_ch}ch")
        except Exception as e:
            lines.append(f"[{LABEL}] {qid} ({r['difficulty']}): ERROR {str(e)[:80]}")
        print(lines[-1], flush=True)

    summary = f"SCORE: {passed}/{len(subset)} = {100*passed/len(subset):.0f}%"
    lines.append(summary)
    lines.append(f"LABEL={LABEL} N={len(subset)}")
    lines.append("LCB-30 DONE")
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + f"\nROWS={len(subset)}\n")
    print(summary, f"ROWS={len(subset)}")
