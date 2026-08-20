import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    # dp[0]: best sum of a valid subsequence with an even number of selected elements
    # dp[1]: best sum of a valid subsequence with an odd number of selected elements
    #
    # A valid final stack corresponds to a subsequence whose selected indices
    # alternate parity, starting with an odd index.
    dp = [0, -10**30]

    for i, x in enumerate(a, start=1):
        if i % 2 == 1:
            # An odd index can be the first selected element, or the next
            # selected element after an even number of selected elements.
            dp[1] = max(dp[1], dp[0] + x)
        else:
            # An even index can only be selected after an odd number of
            # selected elements.
            dp[0] = max(dp[0], dp[1] + x)

    # If n is even, the final stack may be empty, giving sum 0.
    # If n is odd, the final stack size must be odd, so dp[1] is valid.
    if n % 2 == 0:
        print(max(0, dp[0]))
    else:
        print(dp[1])

if __name__ == "__main__":
    main()
