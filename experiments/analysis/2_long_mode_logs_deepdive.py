import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt


OUTPUT_FOLDER_NAME = 'long_mode_log_analysis'
PATH_TO_RESULTS = '../results/syncfrom2b/output/logs'


def run():

	filenames = next(walk(PATH_TO_RESULTS), (None, None, []))[2]
	print(filenames)

	for filename in filenames:
		if filename == ".DS_Store":
			continue
		# trips_no = int(filename.split("_")[-2])
		with open(f"{PATH_TO_RESULTS}/{filename}") as f:
			lines = f.readlines()
			if int(lines[12].split(" ")[-1]) > 0:
				print(filename)




if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()
