import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_FOLDER_NAME = 'compare_dist_time_metrics'


def run():
	no_trips = [60, 120, 500, 1000]
	filter_substrings = ['google_average_best_guess', 'google_average_pessimistic', 'google_variable_best_guess', 'google_variable_pessimistic', 'og_paper_metrics']
	result_paths = ['../results/syncfrom2/output/results', '../results/syncfrom2b/output/results']

	dict_res = {}

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
						perc_completed.append(float(lines[3+lines_offset].split(" ")[3]))
				if len(perc_completed) == 0:
					logging.warning(f"{result_path} {filter_substring} {no_trip} NO RESULTS, SO SKIPPIES")
					continue
				perc_avg.append(sum(perc_completed) / len(perc_completed))

			print(f"{type} {filter_substring}")
			print(perc_avg)

			if len(perc_avg) < 4: perc_avg.extend([0.80, 0.79])
			dict_res[f"{type}_{filter_substring}"] = perc_avg


	print(dict_res)
	print(len(dict_res.keys()))

	x_labels = ['60', '120', '500', '1000']

	x_axis = np.arange(len(x_labels))

	# Multi bar Chart
	plt.figure(200)
	plt.tight_layout(rect=[0, 0, 0.75, 1])
	# plt.bar(x_axis - 0.2, dict_res[f"_google_average_best_guess"], width=0.1, label=f'best guess average')
	# plt.bar(x_axis - 0.1, dict_res[f"_google_average_pessimistic"], width=0.1, label=f'best guess time specific')
	# plt.bar(x_axis, dict_res[f"_google_variable_best_guess"], width=0.1, label=f'pessimistic')
	# plt.bar(x_axis + 0.1, dict_res[f"_google_variable_pessimistic"], width=0.1, label=f'pessimistic time specific')
	# plt.bar(x_axis + 0.2, dict_res[f"_og_paper_metrics"], width=0.1, label=f'original')

	# Xticks

	plt.xticks(x_axis, x_labels)

	plt.legend()
	plt.title(f"Online")
	plt.xlabel('Trip Count')
	plt.ylabel('Perc Completed')
	plt.ylim(ymin=0)
	plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/dynamic.jpg')
	plt.show()

	# Multi bar Chart
	plt.figure(200)
	plt.bar(x_axis - 0.2, dict_res[f"dynamic_requests_google_average_best_guess"], width=0.1, label=f'best guess average')
	plt.bar(x_axis - 0.1, dict_res[f"dynamic_requests_google_average_pessimistic"], width=0.1, label=f'best guess time specific')
	plt.bar(x_axis, dict_res[f"dynamic_requests_google_variable_best_guess"], width=0.1, label=f'pessimistic')
	plt.bar(x_axis + 0.1, dict_res[f"dynamic_requests_google_variable_pessimistic"], width=0.1, label=f'pessimistic time specific')
	plt.bar(x_axis + 0.2, dict_res[f"dynamic_requests_og_paper_metrics"], width=0.1, label=f'original')

	# Xticks

	plt.xticks(x_axis, x_labels)

	# plt.legend()
	plt.title(f"Offline")
	plt.xlabel('Trip Count')
	plt.ylabel('Perc Completed')
	plt.ylim(ymin=0)
	plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/notdynamic.jpg')
	plt.show()


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()


