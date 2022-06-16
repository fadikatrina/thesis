from source.input_access.mod_stations import get_mod_location_data
from source.entities.station import Station
from source.entities.triplists.triplist import TripList
from source.entities.triplists.inprogresstriplist import InProgressTripList
from source.helpers.car_finder import pop_from_list
from source.input_access.configuration import get_config_value


class Simulation:

	#
	# This file is long because it contains both the simulation logic and state management, in hindsight maybe these
	# should have been separated, this section separators are to help understand what the different groups of functions
	# are doing
	#
	# THIS SECTION CONTAINS INITIALISATION AND SIMULATION PREPARATION
	#

	def __init__(self, trip_requests, mod_filename):
		self.stations = []
		self.l = None
		self.request_trip_list = trip_requests
		self.announced_trip_list = TripList()
		self.in_progress_trip_list = InProgressTripList()
		self.completed_trip_list = TripList()
		self.rejected_trip_list = TripList()
		self.cars_in_progress_trip = []
		self.initialise_station_data(mod_filename)
		self.simulation_END = False
		self.simulation_clock = 0  # seconds
		self.TOTAL_TRIPS_NO = len(trip_requests)
		self.TOTAL_CARS_NO = self.calculate_total_cars_no_in_stations()
		self.announced_trip_list.append(self.request_trip_list.pop(0))

	def set_logger(self, logger):
		self.l = logger
		self.l.debug(f"NEW LOGGER SET ({self}) ({self.l})")

	def initialise_station_data(self, filename):
		for ml in get_mod_location_data(filename):
			self.stations.append(Station(ml["id"], ml["site_name"], ml["longitude"], ml["latitude"]))

	# MAIN SIMULATION FUNCTION, the centre of the universe of this simulation
	def advance_simulation(self, if_no_trips=None):
		self.end_trips()
		if self.check_simulation_ended():
			last_trip_time = self.end_trips(True)
			if last_trip_time == 0 or last_trip_time is None:
				last_trip_time = if_no_trips
				if last_trip_time is None:
					return
			self.set_new_clock_time(last_trip_time)
			return
		self.check_number_of_cars_constant()

		if self.is_next_event_trip_request():
			new_request = self.request_trip_list[0]
			while self.request_trip_list[0].request_time == new_request.request_time:
				new_request = self.request_trip_list.pop(0)
				self.l.info(f"NEW REQUEST ({new_request})")
				self.check_new_announcing_trip_no_car_conflict(new_request)
				self.announced_trip_list.append(new_request)
				self.set_new_clock_time(new_request.request_time)
				if len(self.request_trip_list) == 0:
					break
		else:
			current_trip = self.announced_trip_list.pop(0)
			self.l.info(f"CURRENT TRIP ({current_trip})")
			if not current_trip.has_a_car():
				self.l.info(f"CURRENT TRIP REJECTED ({current_trip})")
				self.rejected_trip_list.append(current_trip)
				self.set_new_clock_time(current_trip.start_time)
			else:
				self.l.info(f"CURRENT TRIP ACCEPTED ({current_trip})")
				self.in_progress_trip_list.append(current_trip)
				self.set_new_clock_time(current_trip.start_time)
				self.start_trip(current_trip)

		self.check_number_of_trips_constant()

	#
	# THIS SECTION CONTAINS SIMULATION/BUSINESS LOGIC OF STARTING TRIPS/ENDING TRIPS/RECHARGING
	#

	# removes the car from start station, checks if the car has enough charge and subtracts the charge
	def start_trip(self, trip):
		self.l.info(f"STARTING TRIP ({trip})")
		start_station = self.stations[trip.start_station_id]
		car = start_station.remove_car(trip.car_id, trip)
		car.current_charge_level -= trip.charge_cost
		assert car.current_charge_level >= 0
		self.cars_in_progress_trip.append(car)
		self.l.debug(f"CAR ({car}) SUBTRACTED CHARGE ({trip.charge_cost})")

	# makes the cars available at end station, for trips with end time before current time, and moves the trips from
	# in progress to completed list
	def end_trips(self, force_all=False):
		last_trip_time = 0
		if force_all:
			self.l.info(f"ENDING ALL TRIPS")
		for i in range(len(self.in_progress_trip_list)):
			trip = self.in_progress_trip_list[0]
			if (trip.end_time <= self.simulation_clock) or force_all:
				self.l.info(f"ENDING TRIP ({trip})")
				self.completed_trip_list.append(trip)
				end_station = self.stations[trip.end_station_id]
				self.cars_in_progress_trip, car = pop_from_list(self.cars_in_progress_trip, trip.car_id, trip=trip)
				car.last_trip_end_time = trip.end_time
				end_station.add_car(car)
				self.in_progress_trip_list.remove(trip)
				last_trip_time = trip.end_time
			else:
				break
		return last_trip_time

	# check which cars are in stations and need to be recharged, what is the charge level we need to add? since they
	# finished their last trip
	def update_cars_charge_level(self):
		self.l.debug(f"UPDATING CHARGE")
		for station in self.stations:
			for car in station.cars:
				if not car.is_charge_full():
					charge_to_add = (self.simulation_clock - max(car.last_recharge, car.last_trip_end_time)) * get_config_value("car_recharge_per_second")
					self.l.debug(f"CAR ({car}) ADDING ({charge_to_add})")
					car.add_charge(charge_to_add)
					car.last_recharge = self.simulation_clock

	# receives the trips assignment from the algorithms, checks them using function `check_trip_list_altered`
	def set_new_triplist(self, new_triplist):
		self.check_trip_list_altered(new_triplist)
		self.announced_trip_list = new_triplist

	#
	# THIS SECTION CONTAINS THE TIMING FUNCTIONS
	#

	# fast forward to any point in time, as many iterations as needed to get there
	def advance_simulation_to_time(self, time):
		self.l.debug(f"FAST FORWARDING TO ({time})")
		while self.simulation_clock < time:
			self.advance_simulation(time)

	# changes the simulation clock, checks the new time is not in the past
	def set_new_clock_time(self, new_time):
		self.l.info(f"SIMULATION CLOCK ADVANCED TO ({new_time})")
		assert new_time >= self.simulation_clock
		self.simulation_clock = new_time
		self.end_trips()
		self.update_cars_charge_level()

	# check if simulation ended (by both trips and request trip list being empty)
	def check_simulation_ended(self):
		if (len(self.announced_trip_list) == 0) and (len(self.request_trip_list) == 0):
			self.simulation_END = True
			return True

	# this is used in order to know what do next in the simulation, announce a trip request or start/reject a trip
	def is_next_event_trip_request(self):
		try:
			next_trip = self.announced_trip_list[0]
		except IndexError:
			return True
		next_trip = next_trip.start_time
		try:
			next_trip_request = self.request_trip_list[0]
		except IndexError:
			return False
		next_trip_request = next_trip_request.request_time
		if next_trip < next_trip_request:
			return False
		return True

	#
	# THIS SECTION CONTAINS THE CORRECTNESS CHECK FUNCTIONS, IS THE SIMULATION BEHAVING PROPERLY?
	#

	# sanity/runtime check that sum of number of cars is constant across all stations and trips in progress
	def check_number_of_cars_constant(self):
		current_total = len(self.cars_in_progress_trip) + self.calculate_total_cars_no_in_stations()
		assert current_total == self.TOTAL_CARS_NO

	# sanity/runtime check that sum of number of trips is constant across all 3 lists
	def check_number_of_trips_constant(self):
		current_total = len(self.announced_trip_list) + len(self.request_trip_list) + len(
			self.completed_trip_list) + len(self.in_progress_trip_list) + len(self.rejected_trip_list)
		assert current_total == self.TOTAL_TRIPS_NO

	# this checks that the trip list given by the algorithms was not altered other than vehicles being assigned
	# whether the vehicle assignment is valid is checked during the simulation itself
	def check_trip_list_altered(self, new_triplist):
		assert type(self.announced_trip_list) == type(new_triplist)
		assert len(self.announced_trip_list) == len(new_triplist)
		for i in range(len(new_triplist)):
			assert self.announced_trip_list[i] == new_triplist[i]

	# There is a feature where I can announce trips to the system that already have a car assignment, the problem is
	# that sometimes this car has already been assigned/used by the algorithms, this method checks the integrity of the
	# simulation by detecting such conflicts
	def check_new_announcing_trip_no_car_conflict(self, new_request):
		car_id = new_request.car_id
		if not car_id or car_id == -1:
			return
		# car is not assigned
		if len(self.announced_trip_list.get_trips_using_car(car_id)) != 0:
			raise RuntimeWarning(f"New request ({new_request}) CAR_ID ({car_id}) already assigned to a trip")
		# car is at the start station
		try:
			pop_from_list(self.stations[new_request.start_station_id].cars, car_id, True)
		except RuntimeError:
			raise RuntimeWarning(f"New request ({new_request}) CAR_ID ({car_id}) is not at the start station")

	# helper functions
	def calculate_total_cars_no_in_stations(self):
		count = 0
		for station in self.stations:
			count += len(station.cars)
		return count

	def get_all_cars(self):
		cars_lists = [x.cars for x in self.stations]
		return [x for xs in cars_lists for x in xs]

	def __str__(self):
		return f"Simulation STATIONS# {len(self.stations)}"
