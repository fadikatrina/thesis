import logging
from pathlib import Path
from os import walk


OUTPUT_FOLDER_NAME = 'battery_car_removed'
PATH_TO_RESULTS = '../results/car_removed_logs/output/results'


def run():

	filenames = next(walk(PATH_TO_RESULTS), (None, None, []))[2]
	print(filenames)
	count = 0

	for filename in filenames:
		if filename == ".DS_Store":
			continue
		# trips_no = int(filename.split("_")[-2])
		with open(f"{PATH_TO_RESULTS}/{filename}") as f:
			lines = f.readlines()
			lines = [x for x in lines if "REMOVEDCARSBECAUSENOTENOUGHCHARGE" in x]
			count = count + len(lines)

	print(count)
	# RESULT: 0 NEVER!!!!!


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()
