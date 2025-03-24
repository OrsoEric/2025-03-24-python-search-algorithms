import numpy as np
import matplotlib.pyplot as plt

def random_gaussian_walk_2d(n_steps, std_dev=1.0):
    """
    Generates a 2D random walk with Gaussian steps.

    Args:
        n_steps: The number of steps in the walk.
        std_dev: The standard deviation of the Gaussian distribution for each step.

    Returns:
        A tuple of two lists representing the x and y coordinates of the walk.
    """

    x = [0.0]  # Start at (0, 0)
    y = [0.0]

    for _ in range(n_steps):
        dx = np.random.normal(0, std_dev)
        dy = np.random.normal(0, std_dev)
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    return x, y

def plot_walk(x, y):
    """
    Plots the 2D random walk.

    Args:
        x: List of x coordinates.
        y: List of y coordinates.
    """
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, marker='o', linestyle='-', markersize=3)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("2D Random Gaussian Walk")
    plt.grid(True)
    plt.axis('equal') #ensure same scale for x and y
    plt.show()

if __name__ == "__main__":
    n_steps = 1000
    std_dev = 1.0

    x, y = random_gaussian_walk_2d(n_steps, std_dev)
    plot_walk(x, y)
    
    