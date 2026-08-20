import sys

def main():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))

    if N == 2:
        print(abs(A[0] - A[1]))
        return

    # For odd N, the optimal unmatched element is always one of the ends.
    # For even N, both ends are matched.
    if N % 2 == 1:
        candidates = [A[1:], A[:-1]]
    else:
        candidates = [A]

    ans = 0
    for B in candidates:
        m = len(B)
        # B has even length.
        # Maximum total score is:
        # sum of elements at even indices (0-based) - sum of elements at odd indices.
        s = 0
        for i, x in enumerate(B):
            if i % 2 == 0:
                s += x
            else:
                s -= x
        if s > ans:
            ans = s

    print(ans)

if __name__ == "__main__":
    main()
