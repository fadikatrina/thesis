from src.entities.simulation import Simulation
from src.input_access.trips_requests import get_trip_requests
from src.input_access.configuration import load_config_data
from src.input_access.station_metrics import load_station_metrics
from src.helpers.report_results import write_txt
from src.helpers.check_results import check_result
from src.helpers.logger import sim_logger, config_logger
import copy
import importlib


class Main:

	def __init__(self, algorithm_class="FirstAvailable", trip_requests_filename="default_unassigned",
	             mod_filename="bristol", log_filename="default", output_results_filename="default",
	             check_results_filename="default", general_config_filename="default",
	             car_charge_config_filename="default", station_metrics_filename="bristol_metrics_ogpaper",
	             algo_car_picking_mode=0):

		# dynamically importing the needed algorithm class based on its name
		# https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
		algo_class = getattr(importlib.import_module(f"src.algorithms.{algorithm_class}"), algorithm_class)
		self.algo = algo_class(algo_car_picking_mode)

		# initialise all the input and output data/variables/files of the simulation
		self.output_results_filename = output_results_filename
		self.check_results_filename = check_results_filename
		config_logger(log_filename)
		load_config_data(general_config_filename, car_charge_config_filename)
		load_station_metrics(station_metrics_filename)
		self.sim = Simulation(get_trip_requests(trip_requests_filename), mod_filename)
		self.sim.set_logger(sim_logger)

		# everything is initialised, lets start the simulation
		sim_logger.critical("================================================")
		self.run()

	def run(self):
		while not self.sim.simulation_END:
			sim_copy = copy.deepcopy(self.sim)
			new_triplist = self.algo.assign_cars(sim_copy)
			self.sim.set_new_triplist(new_triplist)
			self.sim.advance_simulation()
		write_txt(self.sim, self.output_results_filename)
		check_result(self.sim, self.check_results_filename)


if __name__ == "__main__":
	Main(
		algorithm_class="ShortMode",
		trip_requests_filename="default",
		general_config_filename="default",
		car_charge_config_filename="test_long_mode",
		check_results_filename="nothing",
		log_filename="debug_google",
		output_results_filename="debug_google",
		station_metrics_filename="google_average_pessimistic",
		algo_car_picking_mode=3
	)
