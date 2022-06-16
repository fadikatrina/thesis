import random
from src.algorithms.genetic.ga_component import ga_component


class individual:

    def __init__(self, eval, genotype=None, genes=None, individual_size=None, print_debug=False, replacement=True):
        ga_component.__init__(self, print_debug)
        self.replacement = replacement
        self.eval = eval
        if(genotype):
            self.setGenotype(genotype)
        else:
            genotype = self.chooseRandomlyFromGenes(genes, individual_size)
            self.setGenotype(genotype)

    def setGenotype(self, genotype):
        self.individual_size = len(genotype)
        self.genotype = genotype
        self.fitness = self.eval.eval(genotype)

    def chooseRandomlyFromGenes(self, genes, individual_size):
        if (self.replacement):
            return random.choices(genes, k=individual_size)
        else:
            return random.sample(genes, k=individual_size)

    def getGenotype(self):
        return self.genotype

    def getFitness(self):
        return self.fitness
