import logging
import json
from pathlib import Path
import matplotlib.pyplot as plt
import time


def compare_first_and_second_week():

	file_names = ["0_best_guess","1_best_guess","2_best_guess"]

	total_difference = 0

	for file_name in file_names:
		f = open(f'./scrape_dump/first_week/{file_name}.json')
		first_week = json.load(f)
		f = open(f'./scrape_dump/best_guess_sample_second_week/{file_name}.json')
		second_week = json.load(f)

		for hour in range(24):
			for destination_i in range(2):
				first_observation = first_week[hour]["rows"][0]["elements"][destination_i]["duration_in_traffic"]["value"]
				second_observation = second_week[hour]["rows"][0]["elements"][destination_i]["duration_in_traffic"]["value"]
				total_difference += abs(first_observation - second_observation)

	logging.info(f"total_difference between first_week and second_week {total_difference}")


def compare_best_guess_and_pessimistic():

	NUMBER_OF_DESTINATIONS = 14

	total_difference = 0
	absolute_difference = 0
	difference_each_hour = None

	for i in range(NUMBER_OF_DESTINATIONS):
		f = open(f'./scrape_dump/realtime_grouped/{i}_best_guess.json')
		opt = json.load(f)
		f = open(f'./scrape_dump/realtime_grouped/{i}_pessimistic.json')
		pes = json.load(f)

		difference_each_destination = [0 for x in range(NUMBER_OF_DESTINATIONS)]
		difference_each_hour_each_destination = [[] for x in range(NUMBER_OF_DESTINATIONS)]
		if difference_each_hour is None:
			difference_each_hour = [0] * len(pes)

		for hour in range(len(opt)):
			difference_this_hour = 0
			for destination_i in range(14):
				assert opt[hour]["departure_time"] == pes[hour]["departure_time"]
				try:
					first_observation = opt[hour]["rows"][0]["elements"][destination_i]["duration_in_traffic"]["value"]
					second_observation = pes[hour]["rows"][0]["elements"][destination_i]["duration_in_traffic"]["value"]
				except (IndexError, KeyError) as e:
					logging.error(f"{i} {destination_i} {hour} {e}")
				# second_observation = opt[hour]["rows"][0]["elements"][destination_i]["duration"]["value"]
				current_difference = abs(first_observation - second_observation)
				total_difference += first_observation - second_observation
				absolute_difference += current_difference
				difference_this_hour += current_difference
				difference_each_destination[destination_i] += current_difference
				difference_each_hour_each_destination[destination_i].append(current_difference)
			difference_each_hour[hour] += difference_this_hour

		logging.info(
			f"starting station ({i}) difference_each_destination between best_guess and pessimistic {[str(x) for x in difference_each_destination]}")
		logging.info(
			f"starting station ({i}) difference_each_hour_each_destination between best_guess and pessimistic first destination {[str(x) for x in difference_each_hour_each_destination[0]]}")
		logging.info(
			f"starting station ({i}) difference_each_hour_each_destination between best_guess and pessimistic second destination {[str(x) for x in difference_each_hour_each_destination[1]]}")

	logging.info(f"total_difference between best_guess and pessimistic {total_difference}")
	logging.info(f"absolute_difference between best_guess and pessimistic {absolute_difference}")
	logging.info(f"difference_each_hour between best_guess and pessimistic {[str(x) for x in difference_each_hour]}")


def compare_hourly_times():

	hourly_timings = []
	NUMBER_OF_STATIONS_TO_PLOT = 15

	for i in range(NUMBER_OF_STATIONS_TO_PLOT):
		hourly_timings.append([[] for x in range(NUMBER_OF_STATIONS_TO_PLOT)])

		f = open(f'./scrape_dump/first_week/{f"{i}_best_guess"}.json')
		opt = json.load(f)

		for hour in range(24 * 7):
			for destination_i in range(14):
				time = opt[hour]["rows"][0]["elements"][destination_i]["duration_in_traffic"]["value"]
				hourly_timings[i][destination_i].append(time)

	for i in range(15):
		for destination_i in range(14):
			hourly_times = hourly_timings[i][destination_i]
			hours = list(range(24 * 7))
			hours = [s % 24 for s in hours]

			fig = plt.figure(figsize=(10, 5))
			plt.bar(hours, hourly_times, color='maroon', width=0.4)
			plt.xlabel("Hours")
			plt.ylabel("Trip Times")
			plt.title(f"Start ID ({i}) Destination ID ({destination_i})")
			plt.show()


def compare_hourly_times_realtime():

	NUMBER_OF_STATIONS_TO_PLOT = 15

	hourly_timings = []

	for i in range(NUMBER_OF_STATIONS_TO_PLOT):
		hourly_timings.append([[] for x in range(NUMBER_OF_STATIONS_TO_PLOT)])

		f = open(f'./scrape_dump/realtime_grouped/{f"{i}_best_guess"}.json')
		opt = json.load(f)

		for hour in range(len(opt)):
			for destination_i in range(14):
				if len(opt[hour]["rows"]) == 0:
					logging.info(f"{i} len of rows {len(opt[hour]['rows'])} so skipping")
					continue
				try:
					duration_in_traffic = opt[hour]["rows"][0]["elements"][destination_i]["duration_in_traffic"]["value"]
				except KeyError as e:
					logging.critical(f"{i} {hour} {destination_i} {e}")
				hourly_timings[i][destination_i].append(duration_in_traffic)

	for i in range(NUMBER_OF_STATIONS_TO_PLOT):
		for destination_i in range(14):
			hourly_times = hourly_timings[i][destination_i]
			filenames = ''
			with open(f'./scrape_dump/realtime/timestamps.txt') as file:
				for line in file:
					filenames = line.rstrip()

			filenames = filenames.split(",")
			filenames = filenames[:-1]
			hours = [time.strftime('%H:%M', time.localtime(int(x))) for x in filenames]

			fig = plt.figure(figsize=(40, 20))
			plt.plot(hours, hourly_times, color='maroon')
			plt.xlabel("Hour:Minute")
			plt.ylabel("Trip Duration")
			plt.xticks(rotation=90, ha='right')
			plt.title(f"Start ID ({i}) Destination ID ({destination_i})")
			plt.savefig(f"./viz/TripDuration_StartStation_{i}_EndStation_{destination_i}_BestGuess.png")
			fig.clear()
			plt.close(fig)


if __name__ == "__main__":
	Path("./logs").mkdir(parents=True, exist_ok=True)
	Path("./viz").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename="./logs/analysis.log", level=logging.DEBUG)
	# compare_first_and_second_week()
	# compare_best_guess_and_pessimistic()
	# compare_hourly_times()
	# compare_hourly_times_realtime()
