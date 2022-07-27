import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt


OUTPUT_FOLDER_NAME = 'max_no_cars'
PATH_TO_RESULTS = '../results/syncfrom1c/output/results'


def run():

	filenames = next(walk(PATH_TO_RESULTS), (None, None, []))[2]
	max_no_cars = 0
	max_no_cars_filename = ""
	max_dict = {}

	for filename in filenames:
		if filename == ".DS_Store":
			continue
		trips_no = int(filename.split("_")[-2])
		with open(f"{PATH_TO_RESULTS}/{filename}") as f:
			lines = f.readlines()
			if int(lines[3].split(" ")[-1]) > max_dict.get(trips_no, 0):
				max_no_cars = int(lines[3].split(" ")[-1])
				max_no_cars_filename = filename
				max_dict[trips_no] = int(lines[3].split(" ")[-1])
				max_dict[f"{trips_no}_filename"] = filename

	print(max_no_cars)
	print(max_no_cars_filename)
	print(max_dict)

	plt.bar([60, 120, 500, 1000], [max_dict[60], max_dict[120], max_dict[500], max_dict[1000]], width=50)
	plt.xlabel("Number of trip requests")
	plt.ylabel("Max number of cars at a station")
	plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/max_no_cars.jpg')
	plt.show()


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()

# RESULT
# {500: 26, '500_filename': 'recreate_og_long_500_0.txt', 60: 18, '60_filename': 'recreate_og_short_60_4.txt', 1000: 32, '1000_filename': 'with_short_enhancement_short_1000_1.txt', 120: 24, '120_filename': 'recreate_og_short_120_1.txt'}
