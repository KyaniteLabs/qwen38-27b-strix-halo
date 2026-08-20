import sys
from collections import deque

def main():
    input = sys.stdin.readline
    H, W = map(int, input().split())
    S = [input().strip() for _ in range(H)]
    A, B, C, D = map(int, input().split())
    A -= 1
    B -= 1
    C -= 1
    D -= 1

    # dist[i][j] = minimum number of front kicks needed to make cell (i, j) reachable.
    INF = 10**9
    dist = [[INF] * W for _ in range(H)]
    dist[A][B] = 0

    dq = deque([(A, B)])

    # Directions: up, down, left, right
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while dq:
        i, j = dq.popleft()
        cur = dist[i][j]

        # 1) Move to adjacent cells that are originally roads: cost 0.
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W:
                if S[ni][nj] == '.' and dist[ni][nj] > cur:
                    dist[ni][nj] = cur
                    dq.appendleft((ni, nj))

        # 2) Perform a front kick in each direction: cost 1.
        #    It makes the cells 1 and 2 steps ahead reachable.
        for di, dj in dirs:
            # Cell 1 step away
            ni, nj = i + di, j + dj
            if 0 <= ni < H and 0 <= nj < W and dist[ni][nj] > cur + 1:
                dist[ni][nj] = cur + 1
                dq.append((ni, nj))

            # Cell 2 steps away
            ni, nj = i + 2 * di, j + 2 * dj
            if 0 <= ni < H and 0 <= nj < W and dist[ni][nj] > cur + 1:
                dist[ni][nj] = cur + 1
                dq.append((ni, nj))

    print(dist[C][D])

if __name__ == "__main__":
    main()
