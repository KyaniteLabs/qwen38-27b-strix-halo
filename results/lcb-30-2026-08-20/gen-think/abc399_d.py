import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        a = data[idx:idx + 2 * n]
        idx += 2 * n

        # pos[x] = (first_position, second_position), 1-indexed
        pos = [None] * (n + 1)
        for i, x in enumerate(a, 1):
            if pos[x] is None:
                pos[x] = (i, i)
            else:
                pos[x] = (pos[x][0], i)

        # For each adjacent pair of positions (i, i+1), store the two labels.
        # If the two labels are different, this adjacent pair can be one of the
        # two final adjacent blocks for a valid pair of couples.
        adj = {}
        for i in range(2 * n - 1):
            x = a[i]
            y = a[i + 1]
            if x != y:
                if x > y:
                    x, y = y, x
                adj[(x, y)] = adj.get((x, y), 0) + 1

        ans = 0
        for x in range(1, n + 1):
            p1, p2 = pos[x]
            if p2 == p1 + 1:
                continue  # x is already adjacent, cannot be part of answer

            # The other adjacent block must be formed by one occurrence of x
            # and one occurrence of y, where y is the other couple.
            # Check the two possible adjacent positions involving x's occurrences.
            candidates = set()
            if p1 > 1 and a[p1 - 2] != x:
                candidates.add(a[p1 - 2])
            if p1 < 2 * n and a[p1] != x:
                candidates.add(a[p1])
            if p2 > 1 and a[p2 - 2] != x:
                candidates.add(a[p2 - 2])
            if p2 < 2 * n and a[p2] != x:
                candidates.add(a[p2])

            for y in candidates:
                if y == x:
                    continue
                if x > y:
                    x, y = y, x
                # Need two disjoint adjacent mixed pairs: one involving x and y,
                # and another involving x and y.
                if adj.get((x, y), 0) >= 2:
                    ans += 1
                x, y = y, x  # restore not needed, loop variable overwritten next iteration

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
