import sys
import json
import re
from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n = len(grid)
        m = len(grid[0])

        # Directions in clockwise order:
        # 0: down-right, 1: down-left, 2: up-left, 3: up-right
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # run[dir][phase][i][j] =
        # maximum number of consecutive cells starting at (i, j) in direction dir
        # that match the infinite pattern:
        #   phase 0: 1, 2, 0, 2, 0, ...
        #   phase 1: 2, 0, 2, 0, ...
        #   phase 2: 0, 2, 0, 2, ...
        #
        # For a valid V segment, the first part is phase 0 from the start.
        # After a clockwise turn, the continuation is a suffix of that pattern,
        # so it can be represented by one of these phases at the turn cell.
        run = [[[ [0] * m for _ in range(n)] for _ in range(3)] for _ in range(4)]

        for d in range(4):
            dr, dc = dirs[d]

            # Process cells in reverse order of the direction so that
            # run[d][phase][i][j] can use run[d][phase][i+dr][j+dc].
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)

            for i in rows:
                for j in cols:
                    ni, nj = i + dr, j + dc
                    inside = 0 <= ni < n and 0 <= nj < m

                    # phase 0: current cell must be 1
                    if grid[i][j] == 1:
                        run[d][0][i][j] = 1 + (run[d][1][ni][nj] if inside else 0)

                    # phase 1: current cell must be 2
                    if grid[i][j] == 2:
                        run[d][1][i][j] = 1 + (run[d][2][ni][nj] if inside else 0)

                    # phase 2: current cell must be 0
                    if grid[i][j] == 0:
                        run[d][2][i][j] = 1 + (run[d][1][ni][nj] if inside else 0)

        ans = 0

        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue

                # A single starting cell is always a valid segment.
                ans = max(ans, 1)

                for d in range(4):
                    # No turn: straight diagonal segment.
                    ans = max(ans, run[d][0][i][j])

                    # One clockwise turn.
                    # The turn cell is at distance t from the start,
                    # where t = first_len - 1.
                    # The first part has length first_len and phase 0.
                    # At the turn cell, the remaining suffix phase is:
                    #   t == 0 -> phase 0
                    #   t odd  -> phase 1
                    #   t even -> phase 2
                    #
                    # We can try every possible first_len along direction d.
                    # Naively this would be O(nm * max(n,m)), but the maximum
                    # possible length is at most 500, and n*m is 250k, so the
                    # total is still acceptable in Python for the given limits.
                    #
                    # To keep it efficient, we only iterate up to the actual
                    # straight run length from this start.
                    first_len = run[d][0][i][j]
                    nd = (d + 1) % 4

                    # If first_len == 1, turning at the start is equivalent
                    # to a straight segment in the turned direction, already
                    # covered by the no-turn case for that direction.
                    # Still, checking it here is harmless.
                    for first_len in range(1, run[d][0][i][j] + 1):
                        t = first_len - 1
                        if t == 0:
                            phase = 0
                        elif t % 2 == 1:
                            phase = 1
                        else:
                            phase = 2

                        # Turn cell coordinates.
                        dr, dc = dirs[d]
                        ti = i + dr * t
                        tj = j + dc * t

                        # Continue in the clockwise direction.
                        second_len = run[nd][phase][ti][tj]
                        # The turn cell is counted in both first_len and second_len,
                        # so subtract 1.
                        total = first_len + second_len - 1
                        if total > ans:
                            ans = total

        return ans


def _parse_grid_from_text(text: str) -> List[List[int]]:
    """
    Robustly parse the grid from standard input.

    Supported forms include:
      - JSON: [[1,2],[3,4]]
      - Python literal: [[1, 2], [3, 4]]
      - Lines of space-separated integers, one row per line
      - A single flat list of integers when the shape is unambiguous
    """
    text = text.strip()
    if not text:
        return []

    # Try JSON first.
    try:
        data = json.loads(text)
        if isinstance(data, list):
            if not data:
                return []
            if isinstance(data[0], list):
                return [[int(x) for x in row] for row in data]
            # Flat list: cannot infer shape unless it is a square.
            vals = [int(x) for x in data]
            size = int(round(len(vals) ** 0.5))
            if size * size == len(vals):
                return [vals[i * size:(i + 1) * size] for i in range(size)]
            return [vals]
    except Exception:
        pass

    # Try Python literal.
    try:
        data = eval(text, {"__builtins__": {}}, {})
        if isinstance(data, list):
            if not data:
                return []
            if isinstance(data[0], list):
                return [[int(x) for x in row] for row in data]
            vals = [int(x) for x in data]
            size = int(round(len(vals) ** 0.5))
            if size * size == len(vals):
                return [vals[i * size:(i + 1) * size] for i in range(size)]
            return [vals]
    except Exception:
        pass

    # Fallback: extract all integers.
    nums = [int(x) for x in re.findall(r"-?\d+", text)]
    if not nums:
        return []

    # If the input has line breaks and each line looks like a row, use that.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    rows = []
    ok = True
    for line in lines:
        # Remove brackets and commas, then split.
        cleaned = line.replace("[", " ").replace("]", " ").replace(",", " ")
        parts = cleaned.split()
        if not parts:
            continue
        try:
            row = [int(x) for x in parts]
        except ValueError:
            ok = False
            break
        rows.append(row)

    if ok and rows:
        # If all rows have the same length, use them.
        if all(len(r) == len(rows[0]) for r in rows):
            return rows
        # Otherwise, if the first line is dimensions n m, handle that.
        if len(rows[0]) == 2:
            n, m = rows[0]
            flat = []
            for r in rows[1:]:
                flat.extend(r)
            if len(flat) == n * m:
                return [flat[i * m:(i + 1) * m] for i in range(n)]

    # Last resort: square if possible, otherwise one row.
    size = int(round(len(nums) ** 0.5))
    if size * size == len(nums):
        return [nums[i * size:(i + 1) * size] for i in range(size)]
    return [nums]


def main() -> None:
    data = sys.stdin.read()
    grid = _parse_grid_from_text(data)
    result = Solution().lenOfVDiagonal(grid)
    print(result)


if __name__ == "__main__":
    main()
