"""
Find the sets that cover all True

"""

import logging
from numpy import random
from typing import List, Set

class St_set:
    lb_item : List[bool] = list()
    n_cost : int = 0

    def set( self, i_lb_item : List[bool], i_n_cost : int ):
        self.lb_item = i_lb_item
        self.n_cost = i_n_cost

    def __repr__(self):
        return f"Items: {self.lb_item} | Cost: {self.n_cost}"


def generate_problem( i_n_item_num : int, i_n_set_num : int ):
    logging.info("Generate problem")
    c_n_random_seed = 42
    random.seed(c_n_random_seed)

    llb_sets : List[bool] = random.random((i_n_set_num, i_n_item_num)) < 0.4
    ln_cost = random.randint(1, 10_000 + 1, size=(c_n_num_sets)) 

    lst_set : Set[St_set] = set()

    for lb_set, n_cost in zip( llb_sets, ln_cost ):
        st_set = St_set()
        st_set.set( lb_set,n_cost )
        lst_set.add(st_set)

    for st_set in lst_set:
        logging.info(f"{st_set}")

    return lst_set

class Cl_solver:
    def __init__(self, i_sst_set : Set[St_set]):
        logging.info("construct the solver")
        #all sets that can compose a solution
        self.sst_set : Set[St_set] = i_sst_set
        return

    def list_actions(self, i_sst_bag : Set[St_set] ):
        """
        A(s)
        """
        sst_action = self.sst_set -i_sst_bag
        lst_action : List[St_set] = list()
        for st_action in sst_action:
            lst_action.append(st_action)

        logging.info(f"{lst_action}")
        return lst_action

    def execute_action(self, i_sst_bag : Set[St_set], i_st_action : St_set ):
        """
        R(s,a)
        """
        i_sst_bag.add(i_st_action)
        return

    def evaluate_goal( self, i_sst_bag : Set[St_set] ) -> int:
        """
        Evaluate how many missing true are there
        """

        n_value_cnt : int = 0 
        st_accumulate : St_set = None
        #scan all items
        for st_item in i_sst_bag:
            #if accumulator is not initialized
            if st_accumulate is None:
                st_accumulate = st_item
            else:
                for n_index, b_value in enumerate(st_item):
                    if st_accumulate.lb_item[n_index] == False and b_value

        return


    def solver(self):
        """
        Find all the sets that put a true on every item
        """

        sst_solution : Set[St_set]  = set()
        
        #list all viable actions
        lst_action = self.list_actions(sst_solution)
        #execute the first action
        self.execute_action( sst_solution, lst_action[0] )
        #list all viable actions
        lst_action = self.list_actions(sst_solution)

        return



if __name__ == "__main__":
    logging.basicConfig(
        filename="debug.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    #c_n_item_num = 5
    #c_n_num_sets = 10
    
    c_n_item_num = 2
    c_n_num_sets = 3

    #generate all sets
    lst_set = generate_problem( c_n_item_num, c_n_num_sets )
    #construct the solver
    cl_solver = Cl_solver(lst_set)

    cl_solver.solver()

