import sys
from contextlib import contextmanager
import io

from src.entities.simulation import Simulation
from src.entities.trip import Trip
import copy


@contextmanager
def captured_output():
	new_out, new_err = io.StringIO(), io.StringIO()
	old_out, old_err = sys.stdout, sys.stderr
	try:
		sys.stdout, sys.stderr = new_out, new_err
		yield sys.stdout, sys.stderr
	finally:
		sys.stdout, sys.stderr = old_out, old_err

with captured_output() as (out, err):
	sim = Simulation()

	sim.trips.append(Trip(5, 5, 1, 2,))
	sim.trips.append(Trip(4, 4, 1, 2, 1,))
	sim.trips.append(Trip(3, 3, 1, 2))
	sim.trips.append(Trip(6, 6, 1, 2))
	sim.trips.append(Trip(7, 7, 1, 2, 1,))
	sim.trips.append(Trip(1, 6, 1, 2, 2))

	print("Auto sorting by trip list")
	for trip in sim.trips:
		print(trip)

	print("get_trips_without_cars")
	for trip_without_car in sim.trips.get_trips_without_cars():
		print(trip_without_car)

	print("stations and cars all init properly")
	for station in sim.stations:
		print(station)
		for car in station.cars:
			print(car)

	print("deep copy vs original ")
	sim2 = copy.deepcopy(sim)

	sim.stations = []
	print("Original")
	for station in sim.stations:
		print(station)
		for car in station.cars:
			print(car)

	print("Deep Copy")
	for station in sim2.stations:
		print(station)
		for car in station.cars:
			print(car)

	for trip in sim.trips:
		print(trip)
		print(trip.distance)
		print(trip.charge_cost)
		print(trip.end_time)

output = out.getvalue().strip()
print(output)
output = output.replace('\n', ' ')
print(output)
assert output == "Auto sorting by trip list Trip REQUEST_TIME 3 START_TIME 3 START_STATION 1 END_STATION 2 CAR_ID -1 Trip REQUEST_TIME 4 START_TIME 4 START_STATION 1 END_STATION 2 CAR_ID 1 Trip REQUEST_TIME 5 START_TIME 5 START_STATION 1 END_STATION 2 CAR_ID -1 Trip REQUEST_TIME 6 START_TIME 6 START_STATION 1 END_STATION 2 CAR_ID -1 Trip REQUEST_TIME 1 START_TIME 6 START_STATION 1 END_STATION 2 CAR_ID 2 Trip REQUEST_TIME 7 START_TIME 7 START_STATION 1 END_STATION 2 CAR_ID 1 get_trips_without_cars Trip REQUEST_TIME 3 START_TIME 3 START_STATION 1 END_STATION 2 CAR_ID -1 Trip REQUEST_TIME 5 START_TIME 5 START_STATION 1 END_STATION 2 CAR_ID -1 Trip REQUEST_TIME 6 START_TIME 6 START_STATION 1 END_STATION 2 CAR_ID -1 stations and cars all init properly Station ID 0 NAME Bradley Stoke Leisure Centre CARS# 5 Car ID 0 CHARGE 100 Car ID 1 CHARGE 100 Car ID 2 CHARGE 100 Car ID 3 CHARGE 100 Car ID 4 CHARGE 100 Station ID 1 NAME Town Centre East CARS# 5 Car ID 5 CHARGE 100 Car ID 6 CHARGE 100 Car ID 7 CHARGE 100 Car ID 8 CHARGE 100 Car ID 9 CHARGE 100 Station ID 2 NAME Tobacco Factory CARS# 5 Car ID 10 CHARGE 100 Car ID 11 CHARGE 100 Car ID 12 CHARGE 100 Car ID 13 CHARGE 100 Car ID 14 CHARGE 100 Station ID 3 NAME The Mall CARS# 5 Car ID 15 CHARGE 100 Car ID 16 CHARGE 100 Car ID 17 CHARGE 100 Car ID 18 CHARGE 100 Car ID 19 CHARGE 100 Station ID 4 NAME Stuart Street, Bristol CARS# 5 Car ID 20 CHARGE 100 Car ID 21 CHARGE 100 Car ID 22 CHARGE 100 Car ID 23 CHARGE 100 Car ID 24 CHARGE 100 Station ID 5 NAME Southmead Hospital Bristol CARS# 5 Car ID 25 CHARGE 100 Car ID 26 CHARGE 100 Car ID 27 CHARGE 100 Car ID 28 CHARGE 100 Car ID 29 CHARGE 100 Station ID 6 NAME Regent Arcade CARS# 5 Car ID 30 CHARGE 100 Car ID 31 CHARGE 100 Car ID 32 CHARGE 100 Car ID 33 CHARGE 100 Car ID 34 CHARGE 100 Station ID 7 NAME Longwell Green Leisure Centre CARS# 5 Car ID 35 CHARGE 100 Car ID 36 CHARGE 100 Car ID 37 CHARGE 100 Car ID 38 CHARGE 100 Car ID 39 CHARGE 100 Station ID 8 NAME Leigh Court Business Centre CARS# 5 Car ID 40 CHARGE 100 Car ID 41 CHARGE 100 Car ID 42 CHARGE 100 Car ID 43 CHARGE 100 Car ID 44 CHARGE 100 Station ID 9 NAME Counterslip, Finzels Reach CARS# 5 Car ID 45 CHARGE 100 Car ID 46 CHARGE 100 Car ID 47 CHARGE 100 Car ID 48 CHARGE 100 Car ID 49 CHARGE 100 Station ID 10 NAME City of Bristol College - South Bristol Skills Academy CARS# 5 Car ID 50 CHARGE 100 Car ID 51 CHARGE 100 Car ID 52 CHARGE 100 Car ID 53 CHARGE 100 Car ID 54 CHARGE 100 Station ID 11 NAME City of Bristol College - College Green Centre CARS# 5 Car ID 55 CHARGE 100 Car ID 56 CHARGE 100 Car ID 57 CHARGE 100 Car ID 58 CHARGE 100 Car ID 59 CHARGE 100 Station ID 12 NAME City of Bristol College - Ashley Down Centre CARS# 5 Car ID 60 CHARGE 100 Car ID 61 CHARGE 100 Car ID 62 CHARGE 100 Car ID 63 CHARGE 100 Car ID 64 CHARGE 100 Station ID 13 NAME Cheltenham Chase Hotel CARS# 5 Car ID 65 CHARGE 100 Car ID 66 CHARGE 100 Car ID 67 CHARGE 100 Car ID 68 CHARGE 100 Car ID 69 CHARGE 100 Station ID 14 NAME Bristol Airport CARS# 5 Car ID 70 CHARGE 100 Car ID 71 CHARGE 100 Car ID 72 CHARGE 100 Car ID 73 CHARGE 100 Car ID 74 CHARGE 100 deep copy vs original  Original Deep Copy Station ID 0 NAME Bradley Stoke Leisure Centre CARS# 5 Car ID 0 CHARGE 100 Car ID 1 CHARGE 100 Car ID 2 CHARGE 100 Car ID 3 CHARGE 100 Car ID 4 CHARGE 100 Station ID 1 NAME Town Centre East CARS# 5 Car ID 5 CHARGE 100 Car ID 6 CHARGE 100 Car ID 7 CHARGE 100 Car ID 8 CHARGE 100 Car ID 9 CHARGE 100 Station ID 2 NAME Tobacco Factory CARS# 5 Car ID 10 CHARGE 100 Car ID 11 CHARGE 100 Car ID 12 CHARGE 100 Car ID 13 CHARGE 100 Car ID 14 CHARGE 100 Station ID 3 NAME The Mall CARS# 5 Car ID 15 CHARGE 100 Car ID 16 CHARGE 100 Car ID 17 CHARGE 100 Car ID 18 CHARGE 100 Car ID 19 CHARGE 100 Station ID 4 NAME Stuart Street, Bristol CARS# 5 Car ID 20 CHARGE 100 Car ID 21 CHARGE 100 Car ID 22 CHARGE 100 Car ID 23 CHARGE 100 Car ID 24 CHARGE 100 Station ID 5 NAME Southmead Hospital Bristol CARS# 5 Car ID 25 CHARGE 100 Car ID 26 CHARGE 100 Car ID 27 CHARGE 100 Car ID 28 CHARGE 100 Car ID 29 CHARGE 100 Station ID 6 NAME Regent Arcade CARS# 5 Car ID 30 CHARGE 100 Car ID 31 CHARGE 100 Car ID 32 CHARGE 100 Car ID 33 CHARGE 100 Car ID 34 CHARGE 100 Station ID 7 NAME Longwell Green Leisure Centre CARS# 5 Car ID 35 CHARGE 100 Car ID 36 CHARGE 100 Car ID 37 CHARGE 100 Car ID 38 CHARGE 100 Car ID 39 CHARGE 100 Station ID 8 NAME Leigh Court Business Centre CARS# 5 Car ID 40 CHARGE 100 Car ID 41 CHARGE 100 Car ID 42 CHARGE 100 Car ID 43 CHARGE 100 Car ID 44 CHARGE 100 Station ID 9 NAME Counterslip, Finzels Reach CARS# 5 Car ID 45 CHARGE 100 Car ID 46 CHARGE 100 Car ID 47 CHARGE 100 Car ID 48 CHARGE 100 Car ID 49 CHARGE 100 Station ID 10 NAME City of Bristol College - South Bristol Skills Academy CARS# 5 Car ID 50 CHARGE 100 Car ID 51 CHARGE 100 Car ID 52 CHARGE 100 Car ID 53 CHARGE 100 Car ID 54 CHARGE 100 Station ID 11 NAME City of Bristol College - College Green Centre CARS# 5 Car ID 55 CHARGE 100 Car ID 56 CHARGE 100 Car ID 57 CHARGE 100 Car ID 58 CHARGE 100 Car ID 59 CHARGE 100 Station ID 12 NAME City of Bristol College - Ashley Down Centre CARS# 5 Car ID 60 CHARGE 100 Car ID 61 CHARGE 100 Car ID 62 CHARGE 100 Car ID 63 CHARGE 100 Car ID 64 CHARGE 100 Station ID 13 NAME Cheltenham Chase Hotel CARS# 5 Car ID 65 CHARGE 100 Car ID 66 CHARGE 100 Car ID 67 CHARGE 100 Car ID 68 CHARGE 100 Car ID 69 CHARGE 100 Station ID 14 NAME Bristol Airport CARS# 5 Car ID 70 CHARGE 100 Car ID 71 CHARGE 100 Car ID 72 CHARGE 100 Car ID 73 CHARGE 100 Car ID 74 CHARGE 100 Trip REQUEST_TIME 3 START_TIME 3 START_STATION 1 END_STATION 2 CAR_ID -1 78.83706055438327 27.824844901547035 58.64968980309407 Trip REQUEST_TIME 4 START_TIME 4 START_STATION 1 END_STATION 2 CAR_ID 1 78.83706055438327 27.824844901547035 59.64968980309407 Trip REQUEST_TIME 5 START_TIME 5 START_STATION 1 END_STATION 2 CAR_ID -1 78.83706055438327 27.824844901547035 60.64968980309407 Trip REQUEST_TIME 6 START_TIME 6 START_STATION 1 END_STATION 2 CAR_ID -1 78.83706055438327 27.824844901547035 61.64968980309407 Trip REQUEST_TIME 1 START_TIME 6 START_STATION 1 END_STATION 2 CAR_ID 2 78.83706055438327 27.824844901547035 61.64968980309407 Trip REQUEST_TIME 7 START_TIME 7 START_STATION 1 END_STATION 2 CAR_ID 1 78.83706055438327 27.824844901547035 62.64968980309407"
