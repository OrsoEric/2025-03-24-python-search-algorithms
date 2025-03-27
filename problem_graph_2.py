"""
Problem: Min Sum
Given an array of n positive integers
Find the minimum number of elements that sum to G
E.g.,
Array: [9, 10, 6, 8, 5]
Goal: 15
Solution: [6, 9] or [5, 10]
https://en.wikipedia.org/wiki/Set_cover_problem

Solve with PATH SEARCH


Action: pick an item from the set

"""

from typing import Set

# Input array and expected sum
ls_input :Set[int] = set( (9, 10, 6, 8, 5) )
n_expected_sum = 15

class Cl_solver:
    def __init__(self):
        return
    

    def list_actions( self, i_ls_bag : Set[int] ) -> Set[int]:
        """
        list all the actions available
        I have a bag, and 
        """
        return ls_input -i_ls_bag
    
    def goal_reached(self, i_ls_bag : Set[int] ) -> bool:
        """
        return true if the items in the set sums to a constant
        """
        n_sum = sum( i_ls_bag )
        if n_sum == n_expected_sum:
            return True
        return False
    
    def execute_action( self, i_n_item : int ) -> Set[int]:
        return



cl_solver = Cl_solver()

print(f"Test action: {cl_solver.list_actions(set())}")
print(f"Test action:  {cl_solver.list_actions( set((9,10)) )}")

print(f"Test goal: {cl_solver.goal_reached( set((10,5)))}")
print(f"Test goal: {cl_solver.goal_reached( set((9,10)) )}")