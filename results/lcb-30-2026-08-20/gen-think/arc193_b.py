import sys

MOD = 998244353

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    s = data[1].strip()

    # Count consecutive blocks of '1' in the cyclic string s.
    # If all characters are '1', there is exactly one cyclic block.
    if s.count('1') == N:
        blocks = 1
    else:
        blocks = 0
        i = 0
        while i < N:
            if s[i] == '1':
                blocks += 1
                while i < N and s[i] == '1':
                    i += 1
            else:
                i += 1

    # The number of distinct in-degree sequences is:
    #   2^(number of cyclic 1-blocks) - 1
    # modulo 998244353.
    ans = (pow(2, blocks, MOD) - 1) % MOD
    print(ans)

if __name__ == "__main__":
    main()
