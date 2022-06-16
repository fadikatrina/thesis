import random
from src.algorithms.genetic.ga_component import ga_component

class cross(ga_component):

    def __init__(self, method_number, print_debug):
        ga_component.__init__(self, print_debug, method_number)


    def cross(self, parent1, parent2):
        if(self.METHOD_NUMBER == 1): offsprings = self.crossSinglePoint(parent1, parent2)
        if (self.METHOD_NUMBER == 2): offsprings = self.crossOrdered(parent1, parent2)

        if (self.PRINT): print("CROSS", "Parent 1: ", parent1, "2: ", parent2)
        if (self.PRINT): print("CROSS", "Son: ", offsprings[0], "Daughter: ", offsprings[1])

        return offsprings

    # 1
    def crossSinglePoint(self, parent1, parent2):
        cut_off = random.randint(0, len(parent1))
        if (self.PRINT): print("CROSS", "Cutoff: ", cut_off)
        son = parent1[:cut_off] + parent2[cut_off:]
        daughter = parent2[:cut_off] + parent1[cut_off:]
        return son, daughter

    # 2
    # the ordered crossover method was found in
    # https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
    def crossOrdered(self, parent1, parent2):

        def produceChild(parent1, parent2):
            randGeneOne = int(random.random() * len(parent1))
            randGeneTwo = int(random.random() * len(parent1))

            start = min(randGeneOne, randGeneTwo)
            end = max(randGeneOne, randGeneTwo)

            a1 = []
            a2 = []

            for i in range(start, end):
                a1.append(parent1[i])

            for i in range(len(parent2)):
                if (a1.count(parent2[i]) == 0):
                    a2.append(parent2[i])

            child = a1 + a2

            return child


        son = produceChild(parent1, parent2)
        daughter = produceChild(parent2, parent1)

        return son, daughter
