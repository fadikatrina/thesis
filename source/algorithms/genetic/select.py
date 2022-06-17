import random
from source.algorithms.genetic.ga_component import ga_component


class select(ga_component):

    def __init__(self, method_number, print_debug, select_quantity, evaluationObject):
        ga_component.__init__(self, print_debug, method_number)
        self.SELECT_QUANTITY = select_quantity
        self.eval = evaluationObject

    def select(self, population):
        selection = []
        for x in range(self.SELECT_QUANTITY):
            if(self.METHOD_NUMBER == 1): selected = self.selectRoulette(population)
            selection.append(selected)

        if (self.PRINT): print("SELECT", "Pop size to select from: ", len(population), "Selected size: ", len(selection))

        return selection

    # 1
    def selectRoulette(self, population):
        population_fitness = population.getPopulationTotalFitness()
        roulette_result = population_fitness * random.random()
        fitness_sum = 0
        for individual in population.getPopulation():
            fitness_sum = fitness_sum  + individual.getFitness()
            if(fitness_sum>=roulette_result):
                selected_individual = individual
                break

        if (self.PRINT): print("SELECT", "Roulette Result: ", roulette_result, "Fitness Sum: ", fitness_sum, "Total Pop Fitness: ", population_fitness)

        return selected_individual

