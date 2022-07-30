import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_FOLDER_NAME = 'compare_setups_pess'


def run():
	no_trips = [60, 120, 500, 1000]
	filter_substrings = ['recreate_og', 'with_short_enhancement', 'with_station_limit', 'with_station_limit_and_enhancements']
	result_paths = ['../results/recreate_not_dynamic_pess/output/results', '../results/recreate_dynamic_pess/output/results']

	dict_res = {}

	for result_path in result_paths:
		filename_offset = 0
		lines_offset = 0
		type = "Not dynamic"

		if result_path == '../results/recreate_dynamic_pess/output/results':
			filename_offset = 3
			type = "Dynamic"

		for filter_substring in filter_substrings:
			filenames = next(walk(result_path), (None, None, []))[2]
			filenames = [k for k in filenames if filter_substring in k]
			filter_length = len(filter_substring.split("_"))

			if filter_substring == "with_station_limit":
				filenames = [k for k in filenames if "enhancements" not in k]

			perc_avg = []

			for no_trip in no_trips:
				f_no_trips = [k for k in filenames if no_trip == int(k.split("_")[1+filename_offset+filter_length])]
				perc_completed = []
				for f_no_trip in f_no_trips:
					with open(f"{result_path}/{f_no_trip}") as f:
						lines = f.readlines()
						perc_completed.append(float(lines[4+lines_offset].split(" ")[3]))
				if len(perc_completed) == 0:
					logging.warning(f"{result_path} {filter_substring} {no_trip} NO RESULTS, SO SKIPPIES")
					continue
				perc_avg.append(sum(perc_completed) / len(perc_completed))

			dict_res[filter_substring] = perc_avg

			print(f"{type} {filter_substring}")
			print(perc_avg)


		print(dict_res)
		x_labels = ['60', '120', '500', '1000']

		x_axis = np.arange(len(x_labels))

		# Multi bar Chart
		plt.figure(200)
		plt.bar(x_axis - 0.2, dict_res["recreate_og"], width=0.1, label='OG')
		plt.bar(x_axis - 0.1, dict_res["with_short_enhancement"], width=0.1, label='OG+Enhancement')
		plt.bar(x_axis, dict_res["with_station_limit"], width=0.1, label='OG+Limit')
		plt.bar(x_axis + 0.1, dict_res["with_station_limit_and_enhancements"], width=0.1, label='OG+Enhancement+Limit')

		# Xticks

		plt.xticks(x_axis, x_labels)

		plt.legend()
		plt.title(f"{type}")
		plt.xlabel('Trip Count')
		plt.ylabel('Perc Completed')
		plt.ylim(ymin=0)
		plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/{type}_{filter_substring}_perc.jpg')
		plt.show()


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()

