import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def rastrigin(i_ln_input, c_n=10):
    """NumPy Rastrigin test function"""
    return -numpy.sum(c_n - c_n * numpy.cos(2 * numpy.pi * i_ln_input) + i_ln_input**2, axis=0)

# Create a grid of x and y values
x = numpy.linspace(-5.12, 5.12, 100)
y = numpy.linspace(-5.12, 5.12, 100)
X, Y = numpy.meshgrid(x, y)

# Calculate the z values using the Rastrigin functionumpyython r   
Z = rastrigin(numpy.array([X, Y]))

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