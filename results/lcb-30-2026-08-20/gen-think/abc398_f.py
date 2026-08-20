import sys

def main():
    s = sys.stdin.buffer.read().strip()
    n = len(s)

    # Reverse of S
    r = s[::-1]

    # We need the longest suffix of S that is a palindrome.
    # A suffix of length L is a palindrome iff it equals the first L characters of reversed S.
    # So compute the longest prefix of r that is also a suffix of s using KMP prefix function.
    t = r + b'#' + s
    m = len(t)

    pi = [0] * m
    for i in range(1, m):
        j = pi[i - 1]
        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j

    longest_pal_suffix = pi[-1]

    # Append the reverse of the part before that palindromic suffix.
    ans = s + s[:n - longest_pal_suffix][::-1]

    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()
