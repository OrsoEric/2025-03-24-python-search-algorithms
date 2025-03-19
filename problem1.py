#generate a string of all ones

c_n_problem_size = 64

from random import choice, randint, random
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

#TWEAK TWO
#runs the risk of NEVER finding a solution
#if I have N-1 correct, changing 2 will always result in wors or equal solution
#it's unimodal and not deceptive

def solver_tweak( i_fn_tweaker ):
    ax_solution = generate_random()
    n_cnt_true = 0
    n_cnt_attempts = 0
    while n_cnt_true < c_n_problem_size:
        ax_new_solution = i_fn_tweaker(ax_solution)
        n_cnt_true_new = fitness(ax_new_solution)
        #print(f"Test: {ax_solution} - {n_cnt_true}")
        if n_cnt_true_new > n_cnt_true:
            ax_solution = ax_new_solution[:]
            n_cnt_true = n_cnt_true_new
            print(f"New best: {ax_solution} - {n_cnt_true}")
        n_cnt_attempts += 1
    print(f"Solution: {ax_solution} | Fitness {n_cnt_true}")    
    print(f"Number of Attempts: {n_cnt_attempts} ")

    

def tweak2(i_ax_eval: List[bool]) -> bool:
    ax_eval = i_ax_eval[:]
    
    # Generate two unique random indices
    while True:
        idx1, idx2 = randint(0, len(ax_eval) - 1), randint(0, len(ax_eval) - 1)
        if idx1 != idx2:
            break
    
    ax_eval[idx1] = not ax_eval[idx1]
    ax_eval[idx2] = not ax_eval[idx2]

    # print(f"Indices: {idx1}, {idx2} | prev: {i_ax_eval} | next: {ax_eval}")
    return ax_eval

def tweak_p(i_ax_eval: List[bool], i_n_probability_change = 0.75) -> bool:
    ax_eval = i_ax_eval[:]

    # Generate two unique random indices
    while random() < i_n_probability_change:
        idx1 = randint(0, len(ax_eval) - 1)
        ax_eval[idx1] = not ax_eval[idx1]

    # print(f"Indices: {idx1}, {idx2} | prev: {i_ax_eval} | next: {ax_eval}")
    return ax_eval

def solver_tweak_p(i_n_p : float = 0.75):
    ax_solution = generate_random()
    n_cnt_true = 0
    n_cnt_attempts = 0
    while n_cnt_true < c_n_problem_size:
        ax_new_solution = tweak_p(ax_solution,i_n_p)
        n_cnt_true_new = fitness(ax_new_solution)
        #print(f"Test: {ax_solution} - {n_cnt_true}")
        if n_cnt_true_new > n_cnt_true:
            ax_solution = ax_new_solution[:]
            n_cnt_true = n_cnt_true_new
            #print(f"New best: {ax_solution} - {n_cnt_true}")
        n_cnt_attempts += 1
    #print(f"Solution: {ax_solution} | Fitness {n_cnt_true}")    
    print(f"Number of Attempts: {n_cnt_attempts} ")

if __name__ == "__main__":
    #solver_brute_force()    
    
    #200
    #solver_tweak( tweak )

    #if I get to N-1 it will never find solution
    #it changes the solution space
    #solver_tweak( tweak2 )

    #0.5 800
    #solver_tweak( tweak_p )
    
    #this tries different P and show the best is around 0.5
    for n in range(9):
        n_p = (n+1)/10
        print( n_p )
        solver_tweak_p( n_p )