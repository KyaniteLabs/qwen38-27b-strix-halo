import sys

MOD = 998244353

def main():
    input = sys.stdin.readline
    N = int(input().strip())
    S = input().strip()

    # Parse the valid parenthesis sequence into a rooted ordered forest.
    # Each node is represented by the list of its children.
    # root is a virtual node whose children are the top-level components.
    root = []
    stack = [root]
    for ch in S:
        if ch == '(':
            node = []
            stack[-1].append(node)
            stack.append(node)
        else:
            stack.pop()

    # dp[u] = number of distinct forests reachable from the children of node u
    # under the allowed operations inside this subtree.
    dp = [0] * (len(root) + 1)
    # We need a list of all nodes. Since nodes are lists, assign ids by traversal.
    nodes = [root]
    for child in root:
        stack = [child]
        while stack:
            u = stack.pop()
            nodes.append(u)
            for v in u:
                stack.append(v)

    # Process nodes in postorder.
    # Since nodes were added in preorder, reverse order is a valid postorder
    # for this forest representation.
    for u in reversed(nodes):
        m = len(u)
        if m == 0:
            dp[u] = 1
            continue

        # For each child v, let a_v = dp[v].
        # We need the number of distinct sequences obtainable by repeatedly:
        # choosing a contiguous interval, reversing it, and replacing each
        # element by one of its reachable variants.
        #
        # This is equivalent to counting distinct sequences over alphabets
        # A_v of sizes a_v, where each position v may use any element of A_v,
        # and the whole sequence may be transformed by the same group generated
        # by interval reversals with independent per-position alphabet choices.
        #
        # The reachable set is exactly all sequences (x_1, ..., x_m) with
        # x_v in A_v, except that if the sequence is a palindrome in the
        # "abstract" sense x_i = x_{m+1-i} for all i, then the two choices
        # for the middle/centered symmetric construction are identified.
        #
        # More precisely, the number is:
        #   total = product a_v
        #   pal = product over i <= m/2 of min(a_i, a_{m+1-i})
        #   if m is odd: pal *= a_center
        #   answer = total - pal
        #
        # This formula follows from the fact that the operation group acts as
        # the full symmetric group on positions, while each position's value
        # can be independently chosen from its reachable set; the only
        # overcount is the fixed point of the reversal involution.
        total = 1
        for v in u:
            total = total * dp[v] % MOD

        pal = 1
        for i in range((m + 1) // 2):
            a = dp[u[i]]
            b = dp[u[m - 1 - i]]
            pal = pal * min(a, b) % MOD

        dp[u] = (total - pal) % MOD

    print(dp[root] % MOD)

if __name__ == "__main__":
    main()
