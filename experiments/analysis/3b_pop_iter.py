import matplotlib.pyplot as plt
import math

x = [100, 100, 100, 200, 300, 400]
y = [50, 100, 150, 200, 300, 50]
z = [23, 28, 32, 29, 33, 19]
z = [ x ** 2 for x in z]
print(z)

plt.scatter(x, y, z)
plt.ylabel("Max # of iterations")
plt.xlabel("Population size")
# inp = input('title number')
plt.title(f"Population size vs max # of iteration effect on completed trips")
plt.figtext(.65, .7, "Dot size = # completed trips")
plt.savefig(f'./viz/genetic_pop_iter/scatter.jpg')
plt.show()
