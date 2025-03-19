#generate a string of all ones

c_n_problem_size = 64

from random import choice, randint
from typing import List

def generate_random() -> List[bool]:
    ax_solution = [choice((True,False)) for _ in range(c_n_problem_size)]

    return  ax_solution

def fitness( i_ax_eval : List[bool] ) -> int:
    n_cnt_true = 0
    for x_value in i_ax_eval:
        if x_value == True:
            n_cnt_true += 1

    return n_cnt_true

def solver_brute_force():
    ax_solution = list()
    n_cnt_true = 0
    n_cnt_attempts = 0
    while n_cnt_true < c_n_problem_size:
        ax_solution = generate_random()
        n_cnt_true = fitness(ax_solution)
        n_cnt_attempts += 1

    print(f"Solution: {ax_solution} | Fitness {n_cnt_true}")    
    print(f"Number of Attempts: {n_cnt_attempts} ")

    return

def tweak( i_ax_eval : List[bool]  ) -> bool:
    ax_eval = i_ax_eval[:]

    n_change = randint(0,c_n_problem_size-1)
    ax_eval[n_change] = not ax_eval[n_change]

    #print(f"Index: {n_change} | prev: {i_ax_eval} | next {ax_eval}")
    return ax_eval

def solver_tweak():
    ax_solution = generate_random()
    n_cnt_true = 0
    n_cnt_attempts = 0
    while n_cnt_true < c_n_problem_size:
        ax_new_solution = tweak(ax_solution)
        n_cnt_true_new = fitness(ax_new_solution)
        #print(f"Test: {ax_solution} - {n_cnt_true}")
        if n_cnt_true_new > n_cnt_true:
            ax_solution = ax_new_solution[:]
            n_cnt_true = n_cnt_true_new
            print(f"New best: {ax_solution} - {n_cnt_true}")
        n_cnt_attempts += 1
    print(f"Solution: {ax_solution} | Fitness {n_cnt_true}")    
    print(f"Number of Attempts: {n_cnt_attempts} ")

    


if __name__ == "__main__":
    #solver_brute_force()    
    solver_tweak()
