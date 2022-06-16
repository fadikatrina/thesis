import random
from source.algorithms.genetic.ga_component import ga_component

class mutate(ga_component):

    def mutate(self, genotype):
        if(self.METHOD_NUMBER == 1): mutated_genotype = self.mutateSingleSwap(genotype)
        if(self.METHOD_NUMBER == 2): mutated_genotype = self.mutateScramble(genotype)

        if(self.PRINT): print("MUTATE", "Input genotype: ", genotype, "Mutated genotype: ", mutated_genotype)

        return mutated_genotype

    # 1
    def mutateSingleSwap(self, genotype):
        length = len(genotype)
        gene1_index = random.randint(0, length-1)
        gene2_index = random.randint(0, length-1)
        lst = list(genotype)
        lst[gene1_index], lst[gene2_index] = lst[gene2_index], lst[gene1_index]
        if(self.PRINT): print("MUTATE Single Swap", "Index 1: ", gene1_index, "Index 2: ", gene2_index)
        return lst

    #2
    def mutateScramble(self, genotype):
        length = len(genotype)
        gene1_index = random.randint(0, length-1)
        gene2_index = random.randint(0, length-1)
        lst = list(genotype)
        lst[gene1_index:gene2_index]
        # if(self.PRINT): print("MUTATE Scramble", "Index 1: ", gene1_index, "Index 2: ", gene2_index)
