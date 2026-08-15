# juice-mkrewrite.py — writes the 150-handler rewrite prompt to /tmp.
# Pair with the throughput bench to reproduce the ledger's rewrite numbers
# (72-133 tok/s on the champion stack vs ~42 mtp-only):
#   python3 juice-mkrewrite.py
#   python3 qwen27-bench.py "$(cat /tmp/juice-rewrite-prompt.txt)" [port]
lines = []
for i in range(1, 151):
    lines.append(f"def handler_{i}(state, payload):")
    lines.append(f"    # handler {i}: validate payload for stage {i}")
    lines.append(f'    if payload is None or state.get("stage") != {i}:')
    lines.append(f'        raise ValueError(f"invalid payload at stage {i}")')
    lines.append(f"    result = {i} * len(str(payload))")
    lines.append(f'    state["last_handler"] = {i}')
    lines.append(f"    return result")
    lines.append("")
code = "\n".join(lines)
prompt = ("Here is a Python module:\n\n```python\n" + code + "\n```\n\n"
          "Rewrite the ENTIRE module renaming every handler_N to step_N and return the full module. No commentary.")
open("/tmp/juice-rewrite-prompt.txt", "w").write(prompt)
print("rewrite prompt chars:", len(prompt))
