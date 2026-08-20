import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    B = list(map(int, data[1+n:1+2*n]))
    C = list(map(int, data[1+2*n:1+3*n]))
    
    # Calculate initial state cost
    S0 = sum(a * c for a, c in zip(A, C))
    
    # Identify positions to flip
    U = []  # 0->1 flips
    D = []  # 1->0 flips
    
    for i in range(n):
        if A[i] != B[i]:
            if A[i] == 0 and B[i] == 1:
                U.append(C[i])
            else:  # A[i]==1 and B[i]==0
                D.append(C[i])
    
    # Sort D in descending order, U in ascending order
    D.sort(reverse=True)
    U.sort()
    
    total_cost = 0
    current_S = S0
    
    # Process D flips first (1->0)
    for c in D:
        current_S -= c
        total_cost += current_S
    
    # Process U flips (0->1)
    for c in U:
        current_S += c
        total_cost += current_S
    
    print(total_cost)

if __name__ == "__main__":
    main()
