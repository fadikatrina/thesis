

class Tracker:

	def __init__(self):
		self.no_assignments_short = []
		self.no_assignments_long = []
		self.no_assignments_genetic = []
		self.genetic_most_fit_genotype = []
		self.genetic_most_fit_legal = []

	def __repr__(self):
		return f"Tracker SHORT ({self.no_assignments_short}) LONG ({self.no_assignments_long}) GENETIC ({self.no_assignments_genetic}) MOST FIT GENOTYPE ({self.genetic_most_fit_genotype}) MOST FIT LEGAL ({self.genetic_most_fit_legal})"
