import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt

OUTPUT_FOLDER_NAME = 'compare_setups'


def viz_best_pick_strategy():
	modes = ['short', 'long']
	no_trips = [60, 120, 500, 1000]
	# filter_substrings = ['recreate_og', 'with_short_enhancement', 'with_station_limit']
	filter_substrings = ['with_station_limit_and_enhancements']
	# result_paths = ['../results/syncfrom1c/output/results', '../results/syncfrom1b/output/results']
	result_paths = ['../results/syncfrom1c/output/results/temp', '../results/syncfrom1b/output/results/temp']

	for result_path in result_paths:
		filename_offset = 0
		lines_offset = 0
		type = ""

		if result_path == '../results/syncfrom1b/output/results' or result_path == '../results/syncfrom1b/output/results/temp':
			filename_offset = 3
			lines_offset = -1
			type = "dynamic"

		for filter_substring in filter_substrings:
			filenames = next(walk(result_path), (None, None, []))[2]
			filenames = [k for k in filenames if filter_substring in k]
			filter_length = len(filter_substring.split("_"))

			for mode in modes:
				f_mode = [k for k in filenames if mode in k]
				perc_avg = []

				for no_trip in no_trips:
					f_no_trips = [k for k in f_mode if no_trip == int(k.split("_")[1+filename_offset+filter_length])]
					perc_completed = []
					for f_no_trip in f_no_trips:
						with open(f"{result_path}/{f_no_trip}") as f:
							lines = f.readlines()
							perc_completed.append(float(lines[4+lines_offset].split(" ")[3]))
					if len(perc_completed) == 0:
						logging.warning(f"{result_path} {mode} {filter_substring} {no_trip} NO RESULTS, SO SKIPPIES")
						continue
					perc_avg.append(sum(perc_completed) / len(perc_completed))

				print(f"{type} {mode} {filter_substring}")
				print(perc_avg)

				if len(perc_avg) < 4: perc_avg.extend([0 for i in range(0, 4-len(perc_avg))])

				plt.figure(200)
				plt.plot(no_trips, perc_avg)
				plt.title(f"{type} {mode} {filter_substring} Percentage")
				plt.xlabel('Trip Count')
				plt.ylabel('Perc Completed')
				plt.ylim(ymin=0)
				plt.savefig(f'./compare_setups_viz/{type}_{mode}_{filter_substring}_perc.jpg')
				plt.clf()


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./{OUTPUT_FOLDER_NAME}_viz").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	viz_best_pick_strategy()


