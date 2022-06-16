from src.entities.simulation import Simulation


class Algorithm:

	def __init__(self, config=None, tracker=None):
		pass

	def assign_cars(self, sim: Simulation):
		raise NotImplementedError
