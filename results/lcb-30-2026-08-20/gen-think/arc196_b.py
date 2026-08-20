import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    T = int(input())
    out = []

    for _ in range(T):
        H, W = map(int, input().split())
        S = [input().strip() for _ in range(H)]

        # Check consistency of horizontal constraints in each row.
        ok = True
        for i in range(H):
            parity = 0
            for ch in S[i]:
                if ch == 'A':
                    parity ^= 1
            if parity:
                ok = False
                break

        # Check consistency of vertical constraints in each column.
        if ok:
            for j in range(W):
                parity = 0
                for i in range(H):
                    if S[i][j] == 'A':
                        parity ^= 1
                if parity:
                    ok = False
                    break

        if not ok:
            out.append("0")
            continue

        # Count B cells.
        b = sum(row.count('B') for row in S)

        # If there is at least one B cell, the coupled constraints determine
        # all row/column flips uniquely.
        if b > 0:
            out.append("1")
        else:
            # All cells are A. Then horizontal and vertical choices are independent.
            # Each row has 2 choices and each column has 2 choices.
            ans = pow(2, H + W, MOD)
            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
