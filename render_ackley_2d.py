import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def ackley(xx, a=20, b=0.2, c=2*np.pi):
    """
    Ackley function.

    Parameters:
    xx: array-like, input vector [x1, x2, ..., xd]
    a: float, constant (optional), default 20
    b: float, constant (optional), default 0.2
    c: float, constant (optional), default 2*pi

    Returns:
    float, Ackley function value
    """

    d = len(xx)

    sum1 = 0
    sum2 = 0
    for xi in xx:
        sum1 += xi**2
        sum2 += np.cos(c * xi)

    term1 = -a * np.exp(-b * np.sqrt(sum1 / d))
    term2 = -np.exp(sum2 / d)

    y = term1 + term2 + a + np.exp(1)
    return y

# 2D Example with 3D Chart
def ackley_2d_plot(a=20, b=0.2, c=2*np.pi):
    """
    Plots the 2D Ackley function in 3D.
    """
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = ackley([X[i, j], Y[i, j]], a, b, c)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Ackley)')
    ax.set_title('2D Ackley Function 3D Visualization')

    plt.show()

# Call the function to create the plot
ackley_2d_plot()