import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_FOLDER_NAME = 'genetic_with_without'


def run():
	result_paths = ['../results/genetic_dynamic/output/results', '../results/genetic_dynamic_compact/output/results', '../results/genetic_not_dynamic/output/results', '../results/genetic_not_dynamic_compact/output/results']

	dict_res = {}

	for result_path in result_paths:

		filenames = next(walk(result_path), (None, None, []))[2]
		type_d = "dynamic"
		if "not" in result_path:
			type_d = "notdynamic"
		if "compact" in result_path:
			type_d += "_compact"

		for i in range(2):
			if i == 0:
				filenames_filtered = [k for k in filenames if "out" in k]
				type = type_d + "_without"
			else:
				filenames_filtered = [k for k in filenames if "out" not in k]
				type = type_d + "_with"

			perc_current = []
			for filename in filenames_filtered:
				with open(f"{result_path}/{filename}") as f:
					lines = f.readlines()
					perc_current.append(float(lines[4].split(" ")[3]))
			if len(perc_current) == 0:
				logging.warning(f"{result_path} {type} NO RESULTS, SO SKIPPIES")
				continue

			dict_res[type] = sum(perc_current) / len(perc_current)


	print(dict_res)
	x_labels = ['Offline', 'Online']
	x_axis = np.arange(len(x_labels))
	plt.figure(200)

	print([dict_res[f"notdynamic_without"], dict_res[f"dynamic_without"]])

	plt.bar(x_axis - 0.1, [dict_res[f"notdynamic_with"], dict_res[f"dynamic_with"]], width=0.2, label='With Genetic')
	plt.bar(x_axis + 0.1, [dict_res[f"notdynamic_without"], dict_res[f"dynamic_without"]], width=0.2, label='Without Genetic')

	plt.xticks(x_axis, x_labels)

	plt.legend()
	plt.title(f"ShortMode vs. Genetic Algorithm")
	plt.xlabel('Setting')
	plt.ylabel('Perc Completed')
	plt.ylim(ymin=0)
	plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/withwithoutgenetic.jpg')
	plt.show()


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG, format='%(message)s')
	run()
