import matplotlib.pyplot as plt

class visualise:

    average_fitnesses = []
    count = []

    def __init__(self):
        pass

    def visualise(self, average_fitness, count):
        self.average_fitnesses.append(average_fitness)
        self.count.append(count)

    def show(self):
        plt.figure(200)
        plt.plot(self.count, self.average_fitnesses)
        plt.xlabel('x - number of generations')
        plt.ylabel('y - average fitness')
        plt.savefig('stats.png')
