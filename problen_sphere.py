"""
This script implements a simple stochastic search algorithm to find the minimum of a fitness function.
The fitness function calculates the sum of squares of the input vector's elements.
The algorithm iteratively tweaks the current best solution by adding Gaussian noise and updates the best solution if the new solution has a lower fitness.
The script also includes a Plotter class to visualize the search progress, showing the solution space search and the fitness evolution over steps.
"""

import numpy
import matplotlib.pyplot as plt
from typing import List, Tuple

def fitness(i_ln_input: List[float]) -> float:
    """
    Calculates the fitness of an input vector as the sum of squares of its elements.

    Args:
        i_ln_input: A list of floats representing the input vector.

    Returns:
        The fitness value (sum of squares).
    """
    n_result: float = 0.0
    for n_value in i_ln_input:
        n_result += n_value * n_value
    return n_result

def tweak(i_ln_input: List[float], i_n_std: float) -> List[float]:
    """
    Generates a tweaked version of the input vector by adding Gaussian noise to each element.

    Args:
        i_ln_input: A list of floats representing the input vector.
        i_n_std: The standard deviation of the Gaussian noise.

    Returns:
        A list of floats representing the tweaked vector.
    """
    n_dimensions = len(i_ln_input)
    n_delta = numpy.random.normal(0, i_n_std, n_dimensions)
    ln_tweaked = i_ln_input + n_delta
    return ln_tweaked

def search(n_steps: int, n_dimensions: int, n_std_start: float) -> Tuple[List[float], float]:
    """
    Performs a stochastic search to find the minimum of the fitness function.

    Args:
        n_steps: The number of search steps.
        n_dimensions: The dimensionality of the solution vector.
        n_std_start: The initial standard deviation for the tweak function.

    Returns:
        A tuple containing the best solution vector and its fitness value.
    """
    target_fitness = 0  # Target fitness to minimize (sum of squares = 0)
    n_k_strength = 0.1  # Strength factor for adjusting the tweak standard deviation
    n_error_power = 1 # power factor for adjusting the tweak standard deviation
    ln_best_solution = numpy.random.normal(0, n_std_start, n_dimensions) # Initialize the best solution with random values.
    n_best_fitness = fitness(ln_best_solution) # Calculate the initial best fitness.

    plotter = Plotter() # Initialize the plotter for visualization.

    for n_step in range(n_steps):
        n_error = target_fitness - n_best_fitness # Calculate the error between the target and current best fitness.

        # Adjust the standard deviation of the tweak based on the error.
        n_std_tweak = n_k_strength * (abs(target_fitness - n_best_fitness) ** n_error_power)

        ln_new_solution = tweak(ln_best_solution, n_std_tweak) # Generate a new solution by tweaking the best solution.
        n_new_fitness = fitness(ln_new_solution) # Calculate the fitness of the new solution.

        # Update the best solution if the new solution has a lower fitness.
        if abs(target_fitness - n_new_fitness) < abs(target_fitness - n_best_fitness):
            ln_best_solution = ln_new_solution
            n_best_fitness = n_new_fitness

        plotter.add_solution(n_step, n_error, n_best_fitness, ln_best_solution) # Add the solution to the plotter.

        print(f"Step {n_step + 1:3}: Error {n_error:.2f} | Change {n_best_fitness:.2f} | Solution: {ln_best_solution}") # Print the search progress.

    plotter.generate() # Generate and display the plots.
    return ln_best_solution, n_best_fitness

class Plotter:
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

    def add_solution(self, step: int, fitness_value: float, solution_value: float, solution_point: List[float]):
        """
        Adds a solution point to the plotter's data.

        Args:
            step: The current step number.
            fitness_value: The fitness value of the solution.
            solution_value: The solution fitness.
            solution_point: The solution vector.
        """
        self.steps.append(step)
        self.fitness_values.append(fitness_value)
        self.solution_values.append(solution_value)
        self.solution_points.append(solution_point)

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
        plt.plot(self.steps, self.solution_values, marker='x', color='red')
        plt.title("Fitness vs Step")
        plt.xlabel(self.xlabel)
        plt.ylabel("Fitness")
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(filename)
        plt.show()

# Example usage
n_steps = 1000
n_dimensions = 5
n_std_start = 1.0

best_solution, best_fitness = search(n_steps, n_dimensions, n_std_start)

print(f"\nBest Solution: {best_solution}")
print(f"Best Fitness: {best_fitness}")