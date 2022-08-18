from source.algorithms.genetic.individual import  individual
from source.algorithms.genetic.ga_component import ga_component


class population:

    def __init__(self, population_size, eval, genes, individual_size, print_debug=False, replacement=True, start_genotype=None):
        ga_component.__init__(self, print_debug)
        self.replacement = replacement
        self.eval = eval
        self.pop_list = []
        self.most_fit_individuals = []
        self.total_fitness = 0
        self.population_size = 0
        self.start_genotype = start_genotype
        self.addIndividuals(self.getRandomlyGeneratedIndividuals(population_size, genes, individual_size))

    def addIndividuals(self, individuals):
        for individual in individuals:
            self.population_size = self.population_size + 1
            self.total_fitness = self.total_fitness + individual.getFitness()
            self.updateMostFitIndividuals(individual)
            self.pop_list.append(individual)

    def updateMostFitIndividuals(self, individual):
        if len(self.most_fit_individuals) == 0:
            self.most_fit_individuals.append(individual)
        elif (individual.getFitness() > self.most_fit_individuals[0].getFitness()):
            self.most_fit_individuals.clear()
            self.most_fit_individuals.append(individual)
        elif (individual.getFitness() == self.most_fit_individuals[0].getFitness()):
            self.most_fit_individuals.append(individual)

    def getRandomlyGeneratedIndividuals(self, how_many, genes, individual_size):
        randomly_generated_individuals = []
        for i in range(0, how_many):
            randomly_generated_individuals.append(individual(self.eval, genes=genes, individual_size=individual_size, replacement=self.replacement, start_genotype=self.start_genotype))
        return randomly_generated_individuals

    def clear(self):
        self.pop_list = []
        self.most_fit_individuals = []
        self.total_fitness = 0
        self.population_size = 0

    def getPopulationSize(self):
        return self.population_size

    def getMostFitIndividuals(self):
        return self.most_fit_individuals

    def getPopulationTotalFitness(self):
        return self.total_fitness

    def getPopulation(self):
        return self.pop_list
