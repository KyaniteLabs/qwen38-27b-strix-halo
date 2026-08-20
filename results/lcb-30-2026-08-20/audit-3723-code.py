class Solution:
    def sumOfGoodNumbers(self, nums: list[int], k: int) -> int:
        n = len(nums)
        total = 0
        for i in range(n):
            is_good = True
            # Check i - k
            if i - k >= 0:
                if nums[i] <= nums[i - k]:
                    is_good = False
            # Check i + k
            if is_good and i + k < n:
                if nums[i] <= nums[i + k]:
                    is_good = False
            if is_good:
                total += nums[i]
        return total

# Read input and write output
import sys
from typing import List

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    # Parse input: first line has nums, second line has k
    # Format: nums = [1,3,2,1,5,4], k = 2
    # We need to parse this properly
    
    # Let's try to parse the input more carefully
    # The input format from the problem examples suggests:
    # Line 1: nums = [1,3,2,1,5,4]
    # Line 2: k = 2
    
    lines = sys.stdin.read().strip().split('\n')
    if len(lines) < 2:
        return
    
    # Parse nums from first line
    nums_line = lines[0].strip()
    # Extract the list part
    start = nums_line.find('[')
    end = nums_line.find(']')
    if start != -1 and end != -1:
        nums_str = nums_line[start+1:end]
        nums = [int(x.strip()) for x in nums_str.split(',') if x.strip()]
    else:
        return
    
    # Parse k from second line
    k_line = lines[1].strip()
    k = int(k_line.split('=')[1].strip())
    
    sol = Solution()
    result = sol.sumOfGoodNumbers(nums, k)
    print(result)

if __name__ == "__main__":
    main()
