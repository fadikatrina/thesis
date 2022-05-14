from src.entities.simulation import Simulation

sim = Simulation()
stations = sim.stations

for station in stations:
	print(station)
	for car in station.cars:
		print(car)
