#!/usr/bin/env python3
"""VISION REAL-SCREENSHOT BATTERY — 6 deterministic UI captures (2026-08-20 CS).
PRE-REGISTERED:
  - Stimuli: 6 fixtures rendered by a real browser engine (Chrome via Playwright,
    localhost HTTP) — bar chart, data table, form, terminal output, progress bars,
    line chart. Screenshots committed beside this harness. Ground truth is known
    from the fixture sources; grading = keyword match (case-insensitive).
  - Serving: mmproj server (old blob champion weights), temp 0, thinking OFF
    (arm 1) — the thinking-ON variant is a separate labeled arm if wanted.
  - Question class: screenshot-look-answer (OSWorld-adjacent), NOT color-patch VQA.
  - Verdict class: pilot n=6. GPU part fires in the NEXT window; this file
    dry-runs WITHOUT any API call (manifest + image validity only).
PATTERN 10: separate .py, dedicated results file, ROWS sentinel.
"""
import base64, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HERE, "vision-real")
URL = os.environ.get("BENCH_URL", "http://127.0.0.1:46399/v1/chat/completions")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   os.environ.get("VISION_OUT", "vision-real-results.log"))
LABEL = os.environ.get("VISION_LABEL", "champion-q4-realui")
THINK = os.environ.get("LCB_THINK", "0") == "1"

TESTS = [
    ("bar-chart.png", "Which product has the highest revenue? Answer with the product name only.", ["beta"]),
    ("table.png", "What is the latency in milliseconds for billing-worker? Answer with the number only.", ["312"]),
    ("form.png", "What email address is prefilled in the form? Answer with the address only.", ["simon@kyanitelabs.tech"]),
    ("terminal.png", "What error code did the health check fail with? Answer with the number only.", ["503"]),
    ("progress.png", "Which backup task is closest to completion? Answer with the task name only.", ["music-library"]),
    ("line-chart.png", "Is monthly active users trending up or down from January to June? Answer up or down.", ["up"]),
]

def ib64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def ask(img_path, prompt):
    body = {"messages": [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + ib64(img_path)}}
    ]}], "max_tokens": 1200 if THINK else 300, "temperature": 0.0,
        "chat_template_kwargs": {"enable_thinking": THINK}}
    if THINK:
        body["reasoning_budget_tokens"] = 512
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        j = json.load(r)
    return j, time.time() - t0

if __name__ == "__main__":
    if "--dry-run" in sys.argv:
        ok = True
        for fname, q, expect in TESTS:
            p = os.path.join(IMG_DIR, fname)
            exists = os.path.isfile(p)
            size = os.path.getsize(p) if exists else 0
            valid = exists and size > 5000
            print(f"[dry] {fname}: exists={exists} size={size} expect~>{','.join(expect)} -> {'OK' if valid else 'BAD'}")
            ok = ok and valid
        sys.exit(0 if ok else 1)

    lines = []
    correct = 0
    for i, (fname, q, expect) in enumerate(TESTS):
        try:
            j, wall = ask(os.path.join(IMG_DIR, fname), q)
            m = j["choices"][0]["message"]
            ans = (m.get("content") or "").strip()
            think = len(m.get("reasoning_content") or "")
            fr = j["choices"][0].get("finish_reason")
            ok = any(e.lower() in ans.lower() for e in expect)
            correct += ok
            line = f"[{LABEL}] R{i+1} ({fname}): {'HIT' if ok else 'MISS'} {wall:.1f}s fr={fr} think={think}ch ans={ans[:40]!r}"
        except Exception as e:
            line = f"[{LABEL}] R{i+1} ({fname}): ERROR {str(e)[:70]}"
        print(line, flush=True); lines.append(line)

    total = f"VISION-REAL: {correct}/{len(TESTS)} correct"
    print(total, flush=True); lines.append(total)
    lines.append("VISION-REAL DONE")
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + f"\nROWS={len(TESTS)}\n")
    print(f"ROWS={len(TESTS)}")
