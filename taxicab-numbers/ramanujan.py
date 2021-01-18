import numpy as np
from itertools import combinations
from typing import List

def get_taxicab_numbers(n: int) -> List[int]:

    """Code for finding first N ramanujan numbers"""
    
    numbers = np.arange(1, 101)
    pairs = np.array(list(combinations(numbers, 2))) # combinations w/o repetitions for numbers in range(1, 101)
    sums = np.apply_along_axis(lambda x: sum(x ** 3), axis=1, pairs) # apply element_1^3 + element_2^3 for each row 
    nums, counts = np.unique(sums, return_counts=True) # results and count of each result in array
    
    return [num for num, count in zip(nums, counts) if count == 2][:n]

if __name__ == "__main__":
    print(*get_taxicab_numbers(int(input())))
    
