from source.entities.simulation import Simulation
from pathlib import Path
import json


def write_txt(sim: Simulation, filename, config_vars, tracker):
	Path("./output/results").mkdir(parents=True, exist_ok=True)
	with open(f'./output/results/{filename}.txt', 'w') as f:

		f.write(f"SIMULATION END TIME {sim.simulation_clock}")
		f.write('\n')
		f.write('\n')

		f.write(f"KEY METRICS")
		f.write('\n')
		f.write(f"MAX NUMBER OF CARS AT A STATION {sim.MAX_NO_CARS_AT_STATION}")
		f.write('\n')
		f.write(f"PERCENTAGE TRIPS COMPLETED {len(sim.completed_trip_list) / sim.TOTAL_TRIPS_NO}")
		f.write('\n')
		f.write(f"PERCENTAGE TRIPS REJECTED {len(sim.rejected_trip_list) / sim.TOTAL_TRIPS_NO}")
		f.write('\n')
		f.write(f"NUMBER TRIPS COMPLETED {len(sim.completed_trip_list)}")
		f.write('\n')
		f.write(f"NUMBER TRIPS REJECTED {len(sim.rejected_trip_list)}")
		f.write('\n')
		f.write(f"DURATION TRIPS COMPLETED {sum(x.duration for x in sim.completed_trip_list)}")
		f.write('\n')
		f.write(f"DURATION TRIPS REJECTED {sum(x.duration for x in sim.rejected_trip_list)}")
		f.write('\n')
		f.write(str(tracker))
		f.write('\n')
		f.write(f"SHORT {sum(tracker.no_assignments_short)}")
		f.write('\n')
		f.write(f"LONG {sum(tracker.no_assignments_long)}")
		f.write('\n')
		f.write(f"GENETIC {sum(tracker.no_assignments_genetic)}")
		f.write('\n')
		f.write('\n')

		f.write(f"CONFIG")
		f.write('\n')
		for key, value in config_vars.items():
			if key == "config_algo":
				f.write(key)
				f.write('\n')
				for key2, value2 in value.items():
					f.write(f"{key2}: {value2}")
					f.write('\n')
			else:
				f.write(f"{key}: {value}")
				f.write('\n')

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
