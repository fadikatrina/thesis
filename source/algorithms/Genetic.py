from source.entities.simulation import Simulation
from source.algorithms.genetic.ga import ga
from source.algorithms.genetic.helpers import assign_genotype_to_triplist, filter_illegal_assignments, assign_triplist_to_genotype
from source.algorithms.ShortMode import ShortMode
from source.helpers.logger import algo_genetic as l
from source.algorithms.genetic.helpers import reset_simulation_cache


class Genetic:

	def __init__(self, config, tracker):
		self.short_mode = ShortMode(config, tracker, False)
		self.eval_option = config["genetic_eval_strategy"]
		self.should_assign_option = config["genetic_should_assign_strategy"]
		self.assign_every_x_trips = config["genetic_assign_every_x_trips"]
		self.assign_every_x_seconds = config["genetic_assign_every_x_seconds"]
		self.use_long_mode_as_well = config["genetic_use_long_mode_as_well"]
		self.last_sim_clock_time_genetic_assigned = 0
		self.last_number_request_trips_genetic_assigned = 0
		self.config = config
		self.tracker = tracker
		self.count_uses = 0

	def assign_using_ga(self, sim):
		start_genotype = assign_triplist_to_genotype(self.short_mode.assign_cars(sim))
		ga_object = ga(
			populationSize=self.config["genetic_population_size"],
			targetFitness=len(sim.announced_trip_list),
			genes=[x.id_ for x in sim.get_all_cars()],
			genesInEachInidivudal=len(sim.announced_trip_list),
			evaluationChoice=self.eval_option,
			selectionChoice=self.config["genetic_select"],
			crossoverChoice=self.config["genetic_crossover"],
			mutateChoice=self.config["genetic_mutate"],
			numberToSelect=None,
			maxIterations=self.config["genetic_max_iterations"],
			pOfCrossing=self.config["p_of_crossover"],
			pOfMutating=self.config["p_of_mutate"],
			sim=sim,
			image_filename=self.config["image_filename"],
			count_uses=self.count_uses,
			start_genotype=start_genotype
		)
		ga_solution = ga_object.run()[0].getGenotype()
		self.tracker.genetic_most_fit_genotype.append(ga_solution)
		self.count_uses += 1
		return assign_genotype_to_triplist(sim, ga_solution)

	def should_assign_using_genetic(self, sim):
		l.debug(f"Checking if using genetic is needed")

		if self.should_assign_option == 1:
			if self.last_sim_clock_time_genetic_assigned == 0:
				return True
			if (sim.simulation_clock - self.last_sim_clock_time_genetic_assigned) > self.assign_every_x_seconds:
				l.debug(f"Accepted based on the time measure ({sim.simulation_clock}) ({self.last_sim_clock_time_genetic_assigned}) ({self.assign_every_x_seconds})")
				return True
		elif self.should_assign_option == 2:
			if self.last_number_request_trips_genetic_assigned == 0:
				return True
			if (self.last_number_request_trips_genetic_assigned - len(sim.request_trip_list)) > self.assign_every_x_trips:
				l.debug(f"Accepted based on the announced trips measure ({len(sim.request_trip_list)}) ({self.last_number_request_trips_genetic_assigned}) ({self.assign_every_x_trips})")
				return True
		else:
			raise ValueError(f"Invalid value of ({self.should_assign_option}) for should_assign_option in Genetic Algo")
		l.debug(f"Rejected ({sim.simulation_clock}) ({len(sim.request_trip_list)})")
		return False

	def assign_cars(self, sim: Simulation):
		if self.should_assign_using_genetic(sim):
			l.info("Genetic is running")
			self.last_number_request_trips_genetic_assigned = len(sim.request_trip_list)
			self.last_sim_clock_time_genetic_assigned = sim.simulation_clock
			new_trip_list = self.assign_using_ga(sim)
			reset_simulation_cache()
			sim.announced_trip_list = filter_illegal_assignments(new_trip_list, sim)
			reset_simulation_cache()
			self.tracker.genetic_most_fit_legal.append([x.car_id for x in sim.announced_trip_list])
			self.tracker.no_assignments_genetic.append(sum(i.car_id > -1 for i in sim.announced_trip_list))
		if self.use_long_mode_as_well:
			return self.short_mode.assign_cars(sim)
		else:
			return sim.announced_trip_list
