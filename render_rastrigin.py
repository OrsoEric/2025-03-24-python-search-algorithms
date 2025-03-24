import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rastrigin(x, A=10):
    """NumPy Rastrigin test function"""
    return np.sum(A - A * np.cos(2 * np.pi * x) + x**2, axis=0)

# Create a grid of x and y values
x = np.linspace(-5.12, 5.12, 100)
y = np.linspace(-5.12, 5.12, 100)
X, Y = np.meshgrid(x, y)

# Calculate the z values using the Rastrigin functionpython r   
Z = rastrigin(np.array([X, Y]))

# Create the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D plot of 2D Rastrigin Function')

# Display the plot
plt.show()