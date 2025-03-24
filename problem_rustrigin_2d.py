import numpy
import matplotlib.pyplot as plt
import logging

from typing import List, Tuple


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
        self.steps = []
        self.fitness_values = []
        self.solution_values = []
        self.solution_points = []

    def add_solution(self, step: int, i_n_error: float, i_ln_point: List[float]):
        """
        Adds a solution point to the plotter's data.

        Args:
            step: The current step number.
            fitness_value: The fitness value of the solution.
            solution_value: The solution fitness.
            solution_point: The solution vector.
        """
        self.steps.append(step)
        self.solution_values.append(abs(i_n_error))
        self.solution_points.append(i_ln_point)

    def generate(self, filename="search_plot.png"):
        """
        Generates and displays the plots.

        Args:
            filename: The filename to save the plot.
        """
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        x_values = [point[0] for point in self.solution_points]
        y_values = [point[1] for point in self.solution_points]
        plt.scatter(x_values, y_values, marker='x')
        plt.title("Solution Space Search")
        plt.xlabel("X Dimension")
        plt.ylabel("Y Dimension")
        plt.grid(True)

        plt.subplot(1, 2, 2)
        plt.scatter(self.steps, self.solution_values, marker='x', color='red')
        plt.title("Fitness vs Step")
        plt.xlabel(self.xlabel)
        plt.ylabel("Fitness")
        plt.yscale('log')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(filename)
        #plt.show()

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

def test_random_walk( i_n_step : int = 10000 ) -> bool:
    
    cl_plotter = Cl_plotter()

    n_dimensions = 2
    n_std_bias = 0.1
    ln_best_solution = random_solution( n_dimensions, 5 )
    
    for n_cnt in range(i_n_step):
        ln_best_solution = tweak( ln_best_solution, n_std_bias)
        n_best_fitness = fitness( ln_best_solution )
        cl_plotter.add_solution( n_cnt, n_best_fitness, ln_best_solution )

        logging.info(f"Step: {n_cnt} | Fitness: {n_best_fitness:.3f} | Solution: {ln_best_solution}")

    cl_plotter.generate()

    return False #Ok

def solver( i_n_dimensions : int = 2, i_n_step_max : int = 100 ):

    cl_plotter = Cl_plotter()

    #initial solution
    n_dimensions = 2
    ln_best_solution = random_solution( n_dimensions, 5 )
    n_best_fitness = fitness(ln_best_solution)

    n_target_fitness = 0.0

    n_std_bias : float = 0.0
    n_std_gain : float = 0.1
    n_error_power : int = 1
    n_cnt_worse = 0
    n_lambda_candidates : int = 5

    n_std_tweak_max = 1.0
    n_cnt_std_tweak_clipped = 0

    for n_step in range(i_n_step_max):
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

        if (n_best_fitness_temp < n_best_fitness):
            n_cnt_worse += 1

        ln_best_solution = lm_best_solution_temp
        n_best_fitness = n_best_fitness_temp

        cl_plotter.add_solution(n_step, n_error, ln_best_solution) # Add the solution to the plotter.

        logging.info(f"Step: {n_step} | Fitness: {n_best_fitness:.3f} | Solution: {ln_best_solution}")

    print(f"Picked worse solutions: {n_cnt_worse}")
    print(f"Clipped STD Tweak: {n_cnt_std_tweak_clipped}")

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

    n_dimensions = 2
    n_step_max = 10000


    #test_random_walk()

    solver(n_dimensions, n_step_max)

