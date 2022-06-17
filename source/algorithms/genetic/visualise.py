import matplotlib.pyplot as plt
from pathlib import Path


class visualise:

    def __init__(self):
        self.highest_fitness = []
        self.counts = []

    def add_iteration(self, new_highest_fitness, new_count):
        self.highest_fitness.append(new_highest_fitness)
        self.counts.append(new_count)

    def show(self, filename, label, title):
        Path("./output/genetic_fitness").mkdir(parents=True, exist_ok=True)
        plt.figure(200)
        plt.plot(self.counts, self.highest_fitness, label=str(label))
        plt.title(title)
        plt.xlabel('x - number of generations')
        plt.ylabel('y - highest fitness')
        plt.legend()
        plt.savefig(f'./output/genetic_fitness/{filename}.png')
