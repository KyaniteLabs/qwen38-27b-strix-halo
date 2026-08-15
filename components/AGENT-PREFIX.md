# AGENT-PREFIX — the 160x TTFT lever on Qwen3.8-27B @ NUCBox

Measured 2026-08-15 on the champion config (Q4_K_XL@96k, draft-mtp,ngram-mod
n12 n-min 24). PP is kernel-bound and spec-independent (~390 tok/s ceiling,
~232 at 43k ctx), so the bands carry across quant/context choices in this
family; re-measure if you depend on exact warm numbers.

| scenario | TTFT (16k-token prompt) |
|---|---|
| cold prefix (never seen) | 40.6 - 41.4 s |
| warm prefix (byte-identical repeat) | **0.25 s** (160x) |

The server's built-in slot prompt-cache does all the work — IF the prefix is
byte-stable. One changed byte anywhere before the divergence point re-processes
everything after it (~230-390 tok/s on this box).

## Rules for the harness (liam-class clients)
1. System prompt, tool definitions, persona: FROZEN strings — never embed
   timestamps, session ids, or rotating state at the TOP of the context.
2. Volatile state (clock, cwd, counters) goes LAST (closest to generation).
3. Keep tool schemas versioned constants; regenerate only on real changes.
4. Same conversation = same prefix; new turn = append-only.

## Repro (from any box with access to the endpoint)
```bash
python3 - <<'EOF'
import json, time, urllib.request
prompt = open("long-prompt.txt").read()          # any ~16k-token text
def go(tag):
    body = json.dumps({"messages":[{"role":"user","content":prompt}],
        "max_tokens":40,"stream":True,
        "chat_template_kwargs":{"enable_thinking":False}}).encode()
    req = urllib.request.Request("http://127.0.0.1:46377/v1/chat/completions",
        data=body, headers={"Content-Type":"application/json"})
    t0=time.time(); first=None
    with urllib.request.urlopen(req, timeout=600) as r:
        for raw in r:
            line=raw.decode(errors="replace").strip()
            if line.startswith("data:") and '"content"' in line:
                first=time.time()-t0; break
    print(f"{tag}: TTFT {first:.2f}s")
go("cold"); go("warm"); go("warm2")
EOF
```
Expect: cold ~40s, warm/warm2 ~0.25s. If warm is not fast, the client is
mutating the prefix — fix the client, not the server.

## Why not --cache-ram / --cache-reuse?
`--cache-reuse` is a no-op on this build ("not supported by this context").
`--cache-ram` (default 8192 MiB) covers the 96k slot KV (~6.3GB; a 128k slot is
~8.4GB at ~2.1GB per 32k). Raising it is the known UMA trap on this box — the
in-slot cache needs no flags at all.
