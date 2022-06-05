from src.entities.simulation import Simulation
from pathlib import Path


def write_txt(sim: Simulation, filename):
	Path("../../output/results").mkdir(parents=True, exist_ok=True)
	with open(f'../../output/results/{filename}.txt', 'w') as f:

		f.write(f"SIMULATION END TIME {sim.simulation_clock}")
		f.write('\n')
		f.write('\n')

		f.write("COMPLETED TRIPS")
		f.write('\n')
		for trip in sim.completed_trip_list:
			f.write(str(trip))
			f.write('\n')
		f.write('\n')

		f.write("UNABLE TO COMPLETE TRIPS")
		f.write('\n')
		for trip in sim.rejected_trip_list:
			f.write(str(trip))
			f.write('\n')
		f.write('\n')

		f.write("STATIONS STATUS")
		f.write('\n')
		for station in sim.stations:
			f.write(str(station))
			f.write('\n')
			for car in station.cars:
				f.write(str(car))
				f.write('\n')
