import numpy
import matplotlib.pyplot as plt
import logging

from typing import List, Tuple

#implement 1/5 P
#use a IRF infinite reaction filter to detect the percentage of better solution
    

class Cl_infinite_reaction_filter:
    def __init__(self, i_n_irf : float = 0.2):
        #parameter of the IRF infinite reaction filter. It's a low pass filter
        #0.0 no memory, only new sample count
        #1.0 infinite memory, only old samples count
        self.c_n_irf_parameter : float = i_n_irf
        #status var. I'ts like a low pass filter
        self.n_state : float = 0.0
        return

    def sample(self, i_n_value : float) -> float:
        self.n_state = self.n_state * self.c_n_irf_parameter +i_n_value *(1 -self.c_n_irf_parameter)
        return self.n_state
    
    def get(self) -> float:
        return self.n_state


class Cl_plotter:
    """
    A class for plotting the search progress.
    """
    def __init__(self, title="Search Progress", xlabel="Step", ylabel="Fitness"):
        """
        Initializes the Plotter object.

        Args:
            title: The title of the plots.
            xlabel: The label for the x-axis.
            ylabel: The label for the y-axis.
        """
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ln_steps = []
        self.ln_point = []
        self.ln_error = []
        self.ln_tweak = []
        self.ln_rate : List[float] = list()
        

    def add_solution(
        self,
        step: int,
        i_ln_point: List[float],
        i_n_error: float,
        i_n_tweak_strenght : float,
        i_n_rate : float
    ):
        """
        Adds a solution point to the plotter's data.

        Args:
            step: The current step number.
            fitness_value: The fitness value of the solution.
            solution_value: The solution fitness.
            solution_point: The solution vector.
        """
        self.ln_steps.append(step)
        self.ln_point.append(i_ln_point)
        self.ln_error.append(abs(i_n_error))
        self.ln_tweak.append(abs(i_n_tweak_strenght))
        #this is the rate of better solution.
        # 1 means everything is better and fitness keeps going up
        # 0 means every step is worse and fitness keeps going down
        self.ln_rate.append(abs(i_n_rate))

        return

    def generate(self, filename="search_plot.png"):
        """
        Generates and displays the plots.

        Args:
            filename: The filename to save the plot.
        """
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        x_values = [point[0] for point in self.ln_point]
        y_values = [point[1] for point in self.ln_point]
        plt.scatter(x_values, y_values, marker='.', label='2D Slice of solution point')
        plt.title("Solution Space Search")
        plt.xlabel("X Dimension")
        plt.ylabel("Y Dimension")
        plt.grid(True)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.scatter(self.ln_steps, self.ln_rate, marker='.', color='black', label='Improve Rate')
        plt.scatter(self.ln_steps, self.ln_error, marker='x', color='red', label='Error')
        plt.scatter(self.ln_steps, self.ln_tweak, marker='.', color='green', label='Tweak')
        plt.title("Error vs Step")
        plt.xlabel(self.xlabel)
        plt.ylabel("Error")
        plt.yscale('log')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.savefig(filename)
        #plt.show()

        return

def rastrigin(i_ln_input, c_n=10):
    """NumPy Rastrigin test function"""
    return -numpy.sum(c_n - c_n * numpy.cos(2 * numpy.pi * i_ln_input) + i_ln_input**2, axis=0)

def random_solution( i_n_dimensions : int = 2, i_n_std : float = 1.0 ):
    return numpy.random.normal(0, i_n_std, i_n_dimensions)

def fitness(i_ln_input: List[float]) -> float:
    return rastrigin(i_ln_input)

def tweak(i_ln_input: List[float], i_n_std: float) -> List[float]:
    n_dimensions = len(i_ln_input)
    ln_delta = random_solution(n_dimensions, i_n_std)
    ln_tweaked = i_ln_input + ln_delta
    return ln_tweaked

def solver( i_n_dimensions : int = 2, i_n_step_max : int = 100 ):
    """
    
    add p probability to explore randomly 1-p to continue from best
    """
    cl_plotter = Cl_plotter()

    #initial solution
    n_dimensions = i_n_dimensions
    n_std_init = 5
    ln_best_solution = random_solution( n_dimensions, n_std_init )
    n_best_fitness = fitness(ln_best_solution)

    n_target_fitness = 0.0

    n_std_bias : float = 0.0
    n_std_gain : float = 0.1
    n_error_power : int = 1
    
    n_lambda_candidates : int = 10

    #BACKUP
    ln_best_solution_backup = ln_best_solution
    n_best_fitness_backup = n_best_fitness
    n_cnt_backup_save = 0
    n_cnt_backup_load = 0

    #RESTART
    #probability to scramble the solution
    n_restart_rand : float = 0.05
    #probability to start from best from backup
    n_restart_best : float = 0.05
    n_cnt_restart : int = 0

    #STD CLIPPER
    n_std_tweak_max = 0.3
    n_cnt_std_tweak_clipped = 0

    #WORSE COUNTER
    n_cnt_worse = 0

    #BETTER/WORSE
    #percentage of new solutions that improved in fitness compared to previous solution

    cl_rate : Cl_infinite_reaction_filter = Cl_infinite_reaction_filter( 0.001 )

    #----------------------------------------------------------------------
    #   EURISTIC SEARCH
    #----------------------------------------------------------------------

    for n_step in range(i_n_step_max):

        n_current_fitness : float = n_best_fitness

        #----------------------------------------------------------------------
        #   RESTART
        #----------------------------------------------------------------------
        #   P   probability to overwrite the search from a random point

        if numpy.random.rand() < n_restart_rand:
            ln_best_solution = random_solution( n_dimensions, n_std_init )
            n_best_fitness = fitness(ln_best_solution)
            n_cnt_restart += 1

        elif numpy.random.rand() < n_restart_best:
            ln_best_solution = ln_best_solution_backup
            n_best_fitness = n_best_fitness_backup
            n_cnt_backup_load += 1

        # Calculate the error between the target and current best fitness.
        n_error = n_target_fitness - n_best_fitness 

        # Adjust the standard deviation of the tweak based on the error.
        n_std_tweak = n_std_bias +n_std_gain * (abs(n_target_fitness - n_best_fitness) ** n_error_power)
        #this can blow up to infinity if error is big
        if (n_std_tweak > n_std_tweak_max):
            n_std_tweak = n_std_tweak_max
            n_cnt_std_tweak_clipped += 1

        lln_candidates : List[List[float]] = list()
        for n_lambda_attempt in range(n_lambda_candidates):
            ln_candiate = tweak(ln_best_solution, n_std_tweak)
            lln_candidates.append(ln_candiate)

        #COMA LAMBDA always discard the seed solution
        lm_best_solution_temp = None
        n_best_fitness_temp = None

        #i'm discarding the previous solution
        for ln_candidate in lln_candidates:
            if lm_best_solution_temp is None:
                lm_best_solution_temp = ln_candidate
                n_best_fitness_temp = fitness(ln_candidate)
            else:
                n_new_fitness = fitness(ln_candidate) # Calculate the fitness of the new solution.
                # Update the best solution if the new solution has a lower fitness.
                if abs(n_target_fitness - n_new_fitness) < abs(n_target_fitness - n_best_fitness_temp):
                    lm_best_solution_temp = ln_candidate
                    n_best_fitness_temp = n_new_fitness

        #----------------------------------------------------------------------
        #   BETTER/WORSE SOLUTION
        #----------------------------------------------------------------------

        #If I recorded an improvement
        if (n_best_fitness_temp > n_current_fitness):
            #local improvement
            cl_rate.sample(1)
        #if I recorded a degradation
        else:
            cl_rate.sample(0)
            n_cnt_worse += 1

        #new solution becomes current solution
        ln_best_solution = lm_best_solution_temp
        n_best_fitness = n_best_fitness_temp

        #SAVE BACKUP
        #if the current best is better than the backed up best
        if abs(n_target_fitness - n_best_fitness) < abs(n_target_fitness - n_best_fitness_backup):
            #global improvement
            ln_best_solution_backup = ln_best_solution
            n_best_fitness_backup = n_best_fitness
            n_cnt_backup_save += 1

        n_irf_rate = cl_rate.get()

        cl_plotter.add_solution(n_step, ln_best_solution, n_error, n_std_tweak, n_irf_rate) # Add the solution to the plotter.

        logging.info(f"Step: {n_step} | Fitness: {n_best_fitness:.3f} | Solution: {ln_best_solution}")

    print(f"Picked worse solutions: {n_cnt_worse}")
    print(f"Clipped STD Tweak: {n_cnt_std_tweak_clipped}")
    print(f"Restart Search: {n_cnt_restart}")
    print(f"Backup | Saved: {n_cnt_backup_save} | Loaded: {n_cnt_backup_load}")

    cl_plotter.generate() # Generate and display the plots.
    return ln_best_solution, n_best_fitness

if __name__ == "__main__":
    logging.basicConfig(
        filename="debug.log",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(module)s:%(lineno)d > %(message)s ',
        filemode='w'
    )
    logging.info("Begin")

    n_dimensions = 5
    n_step_max = 20000

    solver(n_dimensions, n_step_max)

