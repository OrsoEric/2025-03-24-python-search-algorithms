"""
Problem: Min Sum
Given an array of n positive integers
Find the minimum number of elements that sum to G
E.g.,
Array: [9, 10, 6, 8, 5]
Goal: 15
Solution: [6, 9] or [5, 10]
"""

from typing import List, Tuple

def find_min_elements(i_array: List[int], i_goal: int) -> Tuple[List[int], int]:
    """
    This function finds the minimum number of elements from the input array that sum up to the goal.
    It uses a brute force approach by checking all possible combinations.

    Parameters:
    i_array (List[int]): The list of positive integers.
    i_goal (int): The target sum goal.

    Returns:
    Tuple[List[int], int]: A tuple containing the list of elements that sum to the goal and the number of elements.
    """
    n_min_elements = float('inf')
    lt_best_combination = []

    # Generate all possible combinations using bitmasking
    for n_mask in range(1 << len(i_array)):
        ln_current_combination = []
        n_current_sum = 0

        for n_index in range(len(i_array)):
            if (n_mask & (1 << n_index)) != 0:
                ln_current_combination.append(i_array[n_index])
                n_current_sum += i_array[n_index]

        # Check if the current combination sums to the goal
        if n_current_sum == i_goal and len(ln_current_combination) < n_min_elements:
            lt_best_combination = ln_current_combination
            n_min_elements = len(ln_current_combination)

    return (lt_best_combination, n_min_elements)

# Input array and expected sum
ln_input_array = [9, 10, 6, 8, 5]
n_expected_sum = 15

# Find the minimum elements that sum to the goal
lt_result, n_count = find_min_elements(ln_input_array, n_expected_sum)

# Output the result
print(f"Combination: {lt_result}")
print(f"Number of elements: {n_count}")
