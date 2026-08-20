class Solution:
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        total_cells = n * n
        max_by_weight = maxWeight // w
        return min(total_cells, max_by_weight)
