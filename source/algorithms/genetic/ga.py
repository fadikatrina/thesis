import random
from source.algorithms.genetic.evaluate import evaluate
from source.algorithms.genetic.select import select
from source.algorithms.genetic.cross import cross
from source.algorithms.genetic.mutate import mutate
from source.algorithms.genetic.visualise import visualise
from source.algorithms.genetic.population import population
from source.algorithms.genetic.individual import individual
from source.algorithms.genetic.helpers import reset_simulation_cache
from source.helpers.logger import algo_genetic as l


class ga:

    """
    Explanation of genetic options available when initialising
        Evaluation:
            1 : eval_sum_number_of_assigned_trips
        Selection:
            1 : selectRoulette
        Crossover:
            1 : crossSinglePoint
            2 : crossOrdered
        Mutate
            1 : mutateSingleSwap
            2 : mutateScramble

    All have default values that are for hitting a target string "Fadi & Arabi are cool"

    Notes/Possible improvements:
        - Measure time spent on each part of run and optimise accordingly
        - Make all the variables follow the underscore convention (especially in constructors)
        - Adopt "pop" instead of "population" everywhere
        - Try the scramble mutate method instead of single swap for the target word (might be better)
        - Visualisation, how can we show how the learning is progressing?

    """


    def __init__(self,
                 populationSize=1000,
                 targetFitness=21,
                 genes='''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}''',
                 genesInEachInidivudal=21,
                 evaluationChoice = 1,
                 selectionChoice = 1,
                 crossoverChoice = 1,
                 mutateChoice = 1,
                 numberToSelect = None,
                 maxIterations = 500,
                 pOfCrossing = 0.9,
                 pOfMutating = 0.6,
                 displayVisuals = True,
                 printSummary = True,
                 printEval = False,
                 printSelect = False,
                 printCross = False,
                 printMutate = False,
                 printPopulation = False,
                 replacement = True,
                 sim = None,
                 genesAsArray = False,
                 image_filename="stats",
                 count_uses = 0):
        if not numberToSelect: numberToSelect = int(populationSize/2)
        self.TARGET_FITNESS = targetFitness
        self.MAX_ITERATIONS = maxIterations
        self.P_CROSSING = pOfCrossing
        self.P_MUTATING = pOfMutating
        self.PRINT_SUMMARY = printSummary
        self.VISUALISE = displayVisuals
        self.REPLACEMENT = replacement
        self.eval = evaluate(evaluationChoice, printEval, sim)
        self.cross = cross(crossoverChoice, printCross)
        self.mutate = mutate(printMutate, mutateChoice)
        self.visual = visualise()
        self.select = select(selectionChoice, printSelect, numberToSelect, self.eval)
        self.image_filename = image_filename
        self.count_uses = count_uses

        if genes is not list: genes = list(genes)
        self.population = population(populationSize, self.eval, genes, genesInEachInidivudal, printPopulation, replacement=self.REPLACEMENT)
        reset_simulation_cache()

    def run(self):

        most_fit = self.population.getMostFitIndividuals()
        count = 0

        while most_fit[0].getFitness() < self.TARGET_FITNESS and count < self.MAX_ITERATIONS:
            if (self.PRINT_SUMMARY): self.printSummary(count, most_fit)

            mating_pool = self.getMatingPoolAndAdjustPopulation()

            while len(mating_pool) > 0:
                parent1 = mating_pool.pop(random.randrange(len(mating_pool)))
                parent2 = mating_pool.pop(random.randrange(len(mating_pool)))
                self.makeBabiesOrDuplicate(parent1, parent2)

            reset_simulation_cache()
            most_fit = self.population.getMostFitIndividuals()
            count = count + 1

            if self.PRINT_SUMMARY: self.printSummary(count, most_fit)
            if self.VISUALISE: self.visual.add_iteration(most_fit[0].getFitness(), count)

        if self.VISUALISE: self.visual.show(self.image_filename, self.count_uses)

        return most_fit

    def getMatingPoolAndAdjustPopulation(self):

        mating_pool = self.select.select(self.population)
        self.population.clear()
        self.population.addIndividuals(mating_pool)

        return mating_pool

    def makeBabiesOrDuplicate(self, parent1, parent2):

        if (random.random() < self.P_CROSSING):
            babies = self.cross.cross(parent1.getGenotype(), parent2.getGenotype())
            parent1 = individual(self.eval, genotype=babies[0])
            parent2 = individual(self.eval, genotype=babies[1])

        if (random.random() < self.P_MUTATING):
            parent1 = individual(self.eval, genotype=self.mutate.mutate(parent1.getGenotype()))
            parent2 = individual(self.eval, genotype=self.mutate.mutate(parent2.getGenotype()))

        self.population.addIndividuals([parent1, parent2])

    def printSummary(self, count, most_fit):

        population_size = self.population.getPopulationSize()
        population_total_fitness = self.population.getPopulationTotalFitness()

        l.info(f"{count} ;Pop Size; {population_size} ;Pop Fitness; {population_total_fitness} ;Avg fitness; {population_total_fitness / population_size} ;Highest Fitness; {len(most_fit)}; {most_fit[0].getFitness()}; {most_fit[0].getGenotype()}")
