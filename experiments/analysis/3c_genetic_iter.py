import matplotlib.pyplot as plt

x = [3, 7, 10, 20, 30, 40, 50, 60, 70, 80]
y = [37, 32, 33, 25, 21, 20, 12, 13, 12, 14]

plt.scatter(x, y)
plt.ylabel("Completed trips")
plt.xlabel("Every x trips")
# inp = input('title number')
plt.title(f"Genetic activate every x trips vs. completed trips")
plt.savefig(f'./viz/genetic_iter/withwithoutgenetic.jpg')
plt.show()
