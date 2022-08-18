import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt
import numpy as np
import re

OUTPUT_FOLDER_NAME = 'compare_genetic_config_better'


def sorted_nicely(l):
	""" Sort the given iterable in the way that humans expect."""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
	return sorted(l, key=alphanum_key)


def run():
	result_paths = ['../results/syncfrom3_2/output/results', '../results/syncfrom3_4/output/results',
	                '../results/syncfrom3_5/output/results']

	for result_path in result_paths:
		filenames = next(walk(result_path), (None, None, []))[2]
		filenames = sorted_nicely(set(filenames))
		evaluation_method = result_path.split("_")[1][0]

		mutate_ps = []
		crossover_ps = []
		trip_nos = []

		max_mutate_p = -1
		max_crossover_p = -1
		max_trip_no = -1

		z = [[0 for x in range(11)] for y in range(11)]

		for filename in filenames:
			filename_parts = filename.split("_")
			mutate_p = filename_parts[3]
			crossover_p = filename_parts[4]
			mutate_method = int(filename_parts[5])
			crossover_method = int(filename_parts[6])

			if mutate_method != 1 or crossover_method != 1:
				continue

			with open(f"{result_path}/{filename}") as f:
				lines = f.readlines()

			# print(f"{evaluation_method} {mutate_p} {crossover_p} {lines[5]}")
			# print(f"{int(float(mutate_p)*10)} {int(float(crossover_p)*10)}")
			mutate_ps.append(float(mutate_p))
			crossover_ps.append(float(crossover_p))
			trip_nos.append(int(lines[5].split(" ")[-1]) * 10)
			z[int(float(crossover_p)*10)][int(float(mutate_p)*10)] = int(lines[5].split(" ")[-1])

			if int(lines[5].split(" ")[-1]) > max_trip_no:
				max_trip_no = int(lines[5].split(" ")[-1])
				max_crossover_p = crossover_p
				max_mutate_p = mutate_p

		print(f"MAX method {evaluation_method} cross {max_crossover_p} mutate {max_mutate_p} trip_no {max_trip_no}")
		# plt.scatter(x=np.asarray(mutate_ps), y=np.asarray(crossover_ps), s=np.asarray(trip_nos))
		mutate_x, cross_y = np.meshgrid([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
		z = np.asarray(z)

		cp = plt.contour(mutate_x, cross_y, z)
		plt.colorbar(cp)  # Add a colorbar to a plot
		plt.clabel(cp, inline=True, fontsize=10)
		plt.ylabel("Crossover Probability")
		plt.xlabel("Mutate Probability")
		inp = input('title number')
		plt.title(f"Evaluation method {inp}")
		plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/{evaluation_method}.jpg')
		plt.show()


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()

# RESULTS
# MAX method 2 cross 0.8 mutate 0.8 trip_no 30
# MAX method 4 cross 1 mutate 0.4 trip_no 17
# MAX method 5 cross 0.7 mutate 0.7 trip_no 21
