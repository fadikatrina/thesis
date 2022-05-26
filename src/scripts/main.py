from src.entities.simulation import Simulation
from src.data_access.trips_requests import get_trip_requests
from src.helpers.report_results import write_txt
from src.helpers.logger import sim_logger
import copy

from src.algorithms.first_available import FirstAvailable
from src.algorithms.manual import Manual
from src.algorithms.nothing import Nothing


class Main:

	def __init__(self, trip_requests_filename="test_unassigned"):
		self.algo = FirstAvailable()
		self.sim = Simulation(get_trip_requests(trip_requests_filename))
		self.sim.set_logger(sim_logger)
		self.run()

	def run(self):
		while not self.sim.simulation_END:
			sim_copy = copy.deepcopy(self.sim)
			new_triplist = self.algo.assign_cars(sim_copy)
			self.sim.set_new_triplist(new_triplist)
			self.sim.advance_simulation()
		write_txt(self.sim, "test")



Main()
