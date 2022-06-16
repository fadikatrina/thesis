from source.entities.simulation import Simulation
from pathlib import Path
import json


def write_txt(sim: Simulation, filename, config_vars, tracker):
	Path("../output/results").mkdir(parents=True, exist_ok=True)
	with open(f'../output/results/{filename}.txt', 'w') as f:

		f.write(f"SIMULATION END TIME {sim.simulation_clock}")
		f.write('\n')
		f.write('\n')

		f.write(f"KEY METRICS")
		f.write('\n')
		f.write(f"PERCENTAGE TRIPS COMPLETED {len(sim.completed_trip_list) / sim.TOTAL_TRIPS_NO}")
		f.write('\n')
		f.write(f"PERCENTAGE TRIPS REJECTED {len(sim.rejected_trip_list) / sim.TOTAL_TRIPS_NO}")
		f.write('\n')
		f.write(str(tracker))
		f.write('\n')

		f.write(f"CONFIG")
		f.write(json.dumps(config_vars))

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
