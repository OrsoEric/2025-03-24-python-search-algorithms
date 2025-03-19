#

from numpy import random
from numpy.random import randint
import numpy
import logging

from typing import List, Tuple

from itertools import combinations, chain

class St_item:
    def __init__(self, i_n_value: int = 0, i_ln_cost: List[int] = list()):
        self.n_value : int = i_n_value
        self.ln_cost : int = i_ln_cost
        #compute an efficiency metric
        if i_n_value != 0:
            logging.debug(f"{sum(i_ln_cost)} | {i_n_value}")
            self.n_cost_over_value : float = 1.0 *sum(i_ln_cost) / i_n_value
        else:
            self.n_cost_over_value : float = 0.0
        return

    def __repr__(self):
        return f"Value: {self.n_value} | Cost: {self.ln_cost} | Efficiency: {self.n_cost_over_value}"
    
    def __add__(self, other):
        if not isinstance(other, St_item):
            raise TypeError("Can only add two St_item instances")

        # Sum the n_value attributes
        total_n_value : int = self.n_value + other.n_value
        total_ln_cost : List[int] = list()

        #handle empty lists
        if len(self.ln_cost) <= 0:
            return St_item(other.n_value, other.ln_cost)
        elif len(other.ln_cost) <= 0:
            return St_item(self.n_value, self.ln_cost)
        
        for n_cost_a, n_cost_b in zip(self.ln_cost, other.ln_cost):
            total_ln_cost.append( int(n_cost_a +n_cost_b) )

        return St_item(total_n_value, total_ln_cost)
    
    def __sub__(self, other):
        if not isinstance(other, St_item):
            raise TypeError("Can only subtract two St_item instances")

        # Subtract the n_value attributes
        diff_n_value = self.n_value - other.n_value
        diff_ln_cost = []

        # Handle empty lists or unequal length of cost lists
        if len(self.ln_cost) != len(other.ln_cost):
            raise ValueError(f"Cost lists must have the same length for subtraction {len(self.ln_cost)} of {len(other.ln_cost)}")

        for n_cost_a, n_cost_b in zip(self.ln_cost, other.ln_cost):
            diff_ln_cost.append(int(n_cost_a - n_cost_b))

        return St_item(diff_n_value, diff_ln_cost)
    
    def is_underflow(self) -> bool:
        """
        true a cost is below zero
        false all costs are above zero
        """

        for n_cost in self.ln_cost:
            if n_cost < 0:
                return True #underflow
            
        return False #no underflow

class St_solution:
    ln_index : List[int] = list()
    st_content : St_item = St_item()

    def __repr__(self):
        return f"Items: {self.ln_index} | Content: {self.st_content}"

class Cl_backpack:
    """
    """    

    def __init__(self, i_n_cost_dimension : int, i_n_cost_max : int ):
        #max cost for each dimension

        self.n_cost_dimension : int = i_n_cost_dimension
        self.n_cost_max = i_n_cost_max

        self.n_item_num : int = 0
        self.lst_item : List[St_item] = list()

        logging.info(f"Dimensions: {self.n_cost_dimension} | Max Cost: {self.n_cost_max}")
        return
    
    def get_max_cost(self) -> St_item:
        st_item : St_item = St_item()
        st_item.ln_cost = [self.n_cost_max] *self.n_cost_dimension
        return st_item

    def load_items(self, i_ln_value: List[int], i_lln_cost: List[List[int]]) -> bool:
        """
        Load items into the backpack based on given values and costs.
        
        :param i_ln_value: List of item values
        :param i_lln_cost: 2D list of item costs
        :return: False if successful, True fail
        """
        # Clear existing items
        self.lst_item.clear()

        if len(i_ln_value) != len(i_lln_cost):
            logging.error("ERR: unequal item sizes")
            return True #FAIL

        # Create St_item objects for each item and add them to lst_item
        for ln_value, lln_cost in zip(i_ln_value, i_lln_cost):
            new_item = St_item( ln_value, lln_cost)
            self.lst_item.append(new_item)

        self.lst_item = sorted(self.lst_item, key=lambda solution: solution.n_cost_over_value, reverse=False)

        self.n_item_num = len(i_ln_value)

        return False #OK

    def accumulate_items( self, ln_item_index : List[int] ) -> St_item:
        """
        accepts a list of indexes
        all indexes must be unique
        sum all values and cost
        return an Item that represents the total 
        """

        logging.debug(f"Accumulating items: {ln_item_index}")

        st_total_item = St_item()

        for n_item_index in ln_item_index:
            if (n_item_index >= self.n_item_num):
                logging.error(f"OOB Index {n_item_index} of {self.n_item_num}")
                return St_item()
            
            st_item = self.lst_item[n_item_index]
            st_total_item = st_total_item +st_item

        logging.debug(f"Result: {st_total_item}")

        return st_total_item

    def accumulate_items_with_cost_left( self, ln_itemindex : List[int] ) -> Tuple[St_item, St_item]:
        st_accumulate = self.accumulate_items( ln_itemindex )
        st_remaining = self.get_max_cost() -st_accumulate

        return (st_accumulate, st_remaining)

    def show(self) -> bool:
        """
        Show the details of items in the backpack.
        """
        for n_cnt, st_item in enumerate(self.lst_item):
            logging.info(f"Item {n_cnt:3} | Value: {st_item}")
        return False

def generate_combinations(n: int) -> iter:
    """
    Generates all unique combinations of N elements for all values of N from 1 to n.

    Parameters:
    n (int): The size of the set from which to generate combinations.

    Returns:
    iter: An iterator yielding each combination.
    """
    # Create a list of numbers from 1 to n
    numbers = list(range(0, n))
    
    # Generate all combinations for sizes ranging from 1 to n
    return chain.from_iterable(combinations(numbers, size) for size in range(1, n+1))

def backpack_allocator() -> bool:
    c_n_random_seed = 42
    random.seed(c_n_random_seed)

    #c_n_item_num = 10
    #c_n_item_cost_dimension = 5

    c_n_item_num = 100
    c_n_item_cost_dimension = 50
    c_n_cost_max = c_n_item_num *20

    lln_item_cost = randint(1, 50 + 1, size=(c_n_item_num, c_n_item_cost_dimension))
    ln_item_value = randint(1, 100 + 1, size=c_n_item_num)

    my_backpack = Cl_backpack(c_n_item_cost_dimension, c_n_cost_max)

    my_backpack.load_items( ln_item_value, lln_item_cost )

    my_backpack.show()

    #brute_force( my_backpack )

    greedy_solver( my_backpack, 100 )

    return False #OK


def brute_force(i_cl_backpack : Cl_backpack ) -> bool:
    """
    Try every combination
    Maintain two lists
    One with not exceeding cost
    One with exceeding cost
    
    Sort both by value
    """

    lst_valid : List[St_solution] = list()
    lst_invalid : List[St_solution] = list()

    # Example usage:
    n_item_num = i_cl_backpack.n_item_num
    combinations_generator = generate_combinations( n_item_num )
    for ln_item_index in combinations_generator:
        st_solution = St_solution()

        st_used, st_remaining = i_cl_backpack.accumulate_items_with_cost_left(ln_item_index)
        st_remaining.n_value = -st_remaining.n_value
        #logging.debug(f"{ln_item_index} -> Used {st_used} | Remaining {st_remaining}")
        
        st_solution.ln_index = ln_item_index
        st_solution.st_content = st_remaining

        if st_solution.st_content.is_underflow() == True:
            lst_invalid.append(st_solution)
            
        else:
            lst_valid.append(st_solution)

        logging.debug(f"Solution: {st_solution}")

    lst_valid = sorted(lst_valid, key=lambda solution: solution.st_content.n_value, reverse=True)
    lst_invalid = sorted(lst_invalid, key=lambda solution: solution.st_content.n_value, reverse=True)

    logging.debug(f"Valid {len(lst_valid)} | Invalid {len(lst_invalid)}")

    # Sort lst_valid by st_content.n_value in descending order
    
    for st_valid in lst_valid:
        logging.debug(f"Valid: {st_valid}")

    for st_invalid in lst_invalid:
        logging.debug(f"Invalid: {st_invalid}")

    #True, False, True, True, True, True, True, False, True, False
    #0              2,      3,  4,  5,      6,            8

    return

def greedy_solver(i_cl_backpack: Cl_backpack, max_num_step: int) -> St_solution:
    """
    Solves the backpack problem using a greedy algorithm and a maximum number of steps.

    Parameters:
    i_cl_backpack (Cl_backpack): The backpack object containing items and constraints.
    max_num_step (int): Maximum number of steps to take.

    Returns:
    St_solution: The optimal solution within the given constraints.
    """
    st_solution = St_solution()

    # Sort items based on value-to-cost ratio
    sorted_items = sorted(
        enumerate(i_cl_backpack.lst_item),
        key=lambda x: x[1].n_cost_over_value,
    )

    # Accumulate items while considering the cost constraints and the max number of steps
    for step, (index, item) in enumerate(sorted_items):
        if step >= max_num_step:
            logging.info(f"Max steps {max_num_step} reached")
            break

        # Check if adding this item will exceed the backpack's cost limit
        st_accumulate, st_remaining = i_cl_backpack.accumulate_items_with_cost_left(
            st_solution.ln_index + [index]
        )

        if st_remaining.is_underflow():
            logging.debug(f"Item {index} would exceed cost constraints")
            continue

        # Add the item to the solution
        st_solution.ln_index.append(index)
        st_solution.st_content = st_accumulate

    logging.info(f"Greedy Solution: {st_solution}")
    return st_solution


if __name__ == "__main__":
    logging.basicConfig(
        filename="debug.log",
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    backpack_allocator()

