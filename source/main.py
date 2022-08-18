from source.entities.simulation import Simulation
from source.input_access.trips_requests import get_trip_requests
from source.input_access.configuration import load_config_data
from source.input_access.station_metrics import load_station_metrics
from source.helpers.report_results import write_txt
from source.helpers.check_results import check_result
from source.entities.tracker import Tracker
from source.helpers.logger import sim_logger, config_logger
import copy
import importlib


class Main:

	def __init__(self, algorithm_class="FirstAvailable", trip_requests_filename="default_unassigned",
	             mod_filename="bristol", log_filename="default", output_results_filename="default",
	             check_results_filename="nothing", general_config_filename="default",
	             car_charge_config_filename="default", station_metrics_filename="bristol_metrics_ogpaper",
	             algo_config={"strategy": 1}, assign_cars_only_after_all_trips_announced=False, calculate_max_cars_in_station=False):

		# dynamically importing the needed algorithm class based on its name
		# https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
		self.tracker = Tracker()
		algo_class = getattr(importlib.import_module(f"source.algorithms.{algorithm_class}"), algorithm_class)
		self.algo = algo_class(algo_config, self.tracker)

		# saving them only for printing in the summary txt later
		self.config_vars = {
			"algorithm_class": algorithm_class,
			"trip_requests_filename": trip_requests_filename,
			"general_config_filename": general_config_filename,
			"car_charge_config_filename": car_charge_config_filename,
			"check_results_filename": check_results_filename,
			"log_filename": log_filename,
			"output_results_filename": output_results_filename,
			"station_metrics_filename": station_metrics_filename,
			"assign_cars_only_after_all_trips_announced": assign_cars_only_after_all_trips_announced,
			"config_algo": algo_config
		}

		# initialise all the input and output data/variables/files of the simulation
		self.output_results_filename = output_results_filename
		self.check_results_filename = check_results_filename
		config_logger(log_filename)
		load_config_data(general_config_filename, car_charge_config_filename)
		load_station_metrics(station_metrics_filename)
		self.sim = Simulation(get_trip_requests(trip_requests_filename), mod_filename)
		self.sim.set_logger(sim_logger)
		self.assign_cars_only_after_all_trips_announced = assign_cars_only_after_all_trips_announced
		self.calculate_max_cars_in_station = calculate_max_cars_in_station

		# everything is initialised, lets start the simulation
		sim_logger.critical("================================================")
		self.run()

	def run(self):
		while not self.sim.simulation_END:
			sim_copy = copy.deepcopy(self.sim)
			if not (self.assign_cars_only_after_all_trips_announced and len(self.sim.request_trip_list) > 0) and self.sim.new_trips_announced:
				self.tracker.no_announced_trips.append(len(self.sim.announced_trip_list))
				new_triplist = self.algo.assign_cars(sim_copy)
				self.sim.set_new_triplist(new_triplist)
				self.sim.new_trips_announced = False
			self.sim.advance_simulation()
			if self.calculate_max_cars_in_station: self.sim.update_max_cars_at_station()
		sim_logger.critical("======= SIM COMPLETE WRITING RESULTS NOW =======")
		write_txt(self.sim, self.output_results_filename, self.config_vars, self.tracker)
		check_result(self.sim, self.check_results_filename)


if __name__ == "__main__":
	Main(
		algorithm_class="Genetic",
		trip_requests_filename="exp/variant0_routes60",
		general_config_filename="og_paper_with_max_capacity",
		car_charge_config_filename="default",
		check_results_filename="nothing",
		log_filename="genetic_from_short",
		output_results_filename="genetic_from_short",
		station_metrics_filename="pessimistic",
		assign_cars_only_after_all_trips_announced=False,
		algo_config={
			"pick_strategy": 1,
			"dont_take_into_account_future_cars_and_charge": True,
			"genetic_eval_strategy": 1,
			"genetic_should_assign_strategy": 1,
			"genetic_assign_every_x_trips": 5,
			"genetic_assign_every_x_seconds": 40000,
			"genetic_select": 1,
			"genetic_crossover": 1,
			"p_of_crossover": 0.2,
			"genetic_mutate": 1,
			"p_of_mutate": 0.2,
			"genetic_population_size": 100,
			"genetic_max_iterations": 1,
			"image_filename": "itworks",
			"genetic_use_long_mode_as_well": False
		},
	)
