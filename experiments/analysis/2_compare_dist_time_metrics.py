import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt

OUTPUT_FOLDER_NAME = 'compare_dist_time_metrics'


def run():
	no_trips = [60, 120, 500, 1000]
	filter_substrings = ['google_average_best_guess', 'google_average_pessimistic', 'google_variable_best_guess', 'google_variable_pessimistic', 'og_paper_metrics']
	result_paths = ['../results/syncfrom2/output/results', '../results/syncfrom2b/output/results']

	for result_path in result_paths:
		filename_offset = 0
		lines_offset = 0
		type = ""

		if result_path == '../results/syncfrom2b/output/results':
			# filename_offset = 3
			lines_offset = 1
			type = "dynamic_requests"

		for filter_substring in filter_substrings:
			filenames = next(walk(result_path), (None, None, []))[2]
			filenames = [k for k in filenames if filter_substring in k]
			filter_length = len(filter_substring.split("_"))

			perc_avg = []

			for no_trip in no_trips:
				f_no_trips = [k for k in filenames if no_trip == int(k.split("_")[filename_offset+filter_length])]
				perc_completed = []
				for f_no_trip in f_no_trips:
					with open(f"{result_path}/{f_no_trip}") as f:
						lines = f.readlines()
						print(lines[3+lines_offset])
						perc_completed.append(float(lines[3+lines_offset].split(" ")[3]))
				if len(perc_completed) == 0:
					logging.warning(f"{result_path} {filter_substring} {no_trip} NO RESULTS, SO SKIPPIES")
					continue
				perc_avg.append(sum(perc_completed) / len(perc_completed))

			print(f"{type} {filter_substring}")
			print(perc_avg)

			if len(perc_avg) < 4: perc_avg.extend([0 for i in range(0, 4-len(perc_avg))])

			plt.figure(200)
			plt.plot(no_trips, perc_avg)
			plt.title(f"{type} {filter_substring} Percentage")
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


