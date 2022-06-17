from source.algorithms.genetic.ga_component import ga_component
from source.algorithms.genetic.helpers import filter_illegal_assignments, assign_genotype_to_triplist
from collections import Counter
import operator
import functools


class evaluate(ga_component):

    def __init__(self, method_number, print_debug, sim=None):
        ga_component.__init__(self, print_debug, method_number)
        self.sim = sim

    def eval(self, individual):
        if self.METHOD_NUMBER == 1: fitness = self.eval_simple_sum_number_of_assigned_trips(individual)
        if self.METHOD_NUMBER == 2: fitness = self.eval_legal_sum_number_of_assigned_trips(individual)
        if self.METHOD_NUMBER == 3: fitness = self.eval_simple_sum_duration_of_assigned_trips(individual)
        if self.METHOD_NUMBER == 4: fitness = self.eval_legal_sum_duration_of_assigned_trips(individual)
        if self.METHOD_NUMBER == 5: fitness = self.eval_legal_balance_of_network(individual)

        fitness = fitness / len(individual)
        if self.PRINT: print("EVAL", "Individual Evaluated: ", individual, "Fitness: ", fitness)
        return fitness

    # 1
    def eval_simple_sum_number_of_assigned_trips(self, individual):
        return sum(i > -1 for i in individual)-1

    # 2
    def eval_legal_sum_number_of_assigned_trips(self, individual):
        triplist = assign_genotype_to_triplist(self.sim, individual)
        triplist = filter_illegal_assignments(triplist, self.sim)
        return sum(i.car_id > -1 for i in triplist)

    # 3
    def eval_simple_sum_duration_of_assigned_trips(self, individual):
        triplist = assign_genotype_to_triplist(self.sim, individual)
        return sum([x.duration for x in triplist if x.car_id > -1])

    # 4
    def eval_legal_sum_duration_of_assigned_trips(self, individual):
        global simulation_cache
        triplist = assign_genotype_to_triplist(self.sim, individual)
        triplist = filter_illegal_assignments(triplist, self.sim)
        return sum([x.duration for x in triplist if x.car_id > -1])

    # 5
    def eval_legal_balance_of_network(self, individual):
        triplist = assign_genotype_to_triplist(self.sim, individual)
        triplist = filter_illegal_assignments(triplist, self.sim)
        end_stations = [x.end_station_id for x in triplist if x.car_id > -1]
        if len(end_stations) == 0:
            return 0
        number_of_legal_assignments = sum(i.car_id > -1 for i in triplist)

        end_stations = Counter(end_stations).values()
        min_value = min(end_stations)
        normalised = [x-min_value+1 for x in end_stations]
        multiplied = functools.reduce(operator.mul, normalised, 1)
        inverse = 1/multiplied
        return inverse * number_of_legal_assignments
