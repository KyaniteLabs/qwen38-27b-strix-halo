import sys
import re
import json

def parse_input(text: str):
    text = text.strip()
    if not text:
        return [], []

    # 1) Try JSON object
    if text.startswith("{"):
        try:
            obj = json.loads(text)
            groups = None
            elements = None
            for key, value in obj.items():
                k = key.lower()
                if k in ("groups", "g"):
                    groups = value
                elif k in ("elements", "e"):
                    elements = value
            if groups is not None and elements is not None:
                return list(map(int, groups)), list(map(int, elements))
        except Exception:
            pass

    # 2) Try to find two bracketed lists
    bracketed = re.findall(r"\[([^\[\]]*)\]", text)
    if len(bracketed) >= 2:
        parsed = []
        for part in bracketed:
            nums = re.findall(r"-?\d+", part)
            if nums:
                parsed.append(list(map(int, nums)))
        if len(parsed) >= 2:
            return parsed[0], parsed[1]

    # 3) Try line-by-line parsing, optionally removing "name =" prefixes
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    parsed_lines = []
    for line in lines:
        if "=" in line:
            line = line.split("=", 1)[1]
        nums = re.findall(r"-?\d+", line)
        if nums:
            parsed_lines.append(list(map(int, nums)))

    if len(parsed_lines) >= 2:
        return parsed_lines[0], parsed_lines[1]

    # 4) Fallback: extract all integers and try common length-prefixed formats
    nums = list(map(int, re.findall(r"-?\d+", text)))
    if not nums:
        return [], []

    # Format: n, groups..., m, elements...
    if len(nums) >= 2:
        n = nums[0]
        if 0 <= n <= len(nums) - 1:
            groups = nums[1:1 + n]
            rest = nums[1 + n:]
            if rest:
                m = rest[0]
                if 0 <= m <= len(rest) - 1:
                    elements = rest[1:1 + m]
                    return groups, elements

    # Last resort: split all numbers in half
    mid = len(nums) // 2
    return nums[:mid], nums[mid:]


def solve():
    data = sys.stdin.read()
    groups, elements = parse_input(data)

    if not groups:
        print([])
        return

    max_group = max(groups)

    INF = 10**9
    min_index = [INF] * (max_group + 1)

    for idx, value in enumerate(elements):
        if value <= max_group and idx < min_index[value]:
            min_index[value] = idx

    best = [-1] * (max_group + 1)

    for divisor in range(1, max_group + 1):
        idx = min_index[divisor]
        if idx == INF:
            continue
        for multiple in range(divisor, max_group + 1, divisor):
            if best[multiple] == -1 or idx < best[multiple]:
                best[multiple] = idx

    result = [best[g] for g in groups]
    print(result)


if __name__ == "__main__":
    solve()
