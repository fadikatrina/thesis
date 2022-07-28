import logging
from pathlib import Path
from os import walk
import matplotlib.pyplot as plt


OUTPUT_FOLDER_NAME = 'long_mode_log_analysis'
PATH_TO_RESULTS = '../results/syncfrom2b/output/logs'


def run():

	filenames = next(walk(PATH_TO_RESULTS), (None, None, []))[2]
	# print(filenames)
	print(len(filenames))
	res_dict = {}

	for filename in filenames:
		if filename == ".DS_Store":
			continue

		trips_no = int(filename.split("_")[-2])
		with open(f"{PATH_TO_RESULTS}/{filename}") as f:
			lines = f.readlines()
			lines_long_called = [x for x in lines if "SHORT NOT ENOUGH, USING LONG MODE TRIP" in x]
			lines_no_other_options = [x for x in lines if "NO SUITABLE CARS (CHARGE & 1 TRIP) START STATION" in x]
			lines_other_options_not_suitable = [x for x in lines if "SHORTMODE NO ALTERNATIVE CAR THAN" in x]
			lines_long_success = [x for x in lines if "SUBSTITUTE FOUND ASSIGNED NEW CARD ID" in x]
			# print(f"trips_no {trips_no} lines_long_called {len(lines_long_called)} lines_no_other_options {len(lines_no_other_options)} lines_other_options_not_suitable {len(lines_other_options_not_suitable)} lines_long_success {len(lines_long_success)}")
			res_dict[trips_no] = res_dict.get(trips_no, 0) + 1
			res_dict[f"{trips_no}_lines_long_called"] = res_dict.get(f"{trips_no}_lines_long_called", 0) + len(lines_long_called)
			res_dict[f"{trips_no}_lines_no_other_options"] = res_dict.get(f"{trips_no}_lines_no_other_options", 0) + len(lines_no_other_options)
			res_dict[f"{trips_no}_lines_other_options_not_suitable"] = res_dict.get(f"{trips_no}_lines_other_options_not_suitable", 0) + len(lines_other_options_not_suitable)
			res_dict[f"{trips_no}_lines_long_success"] = res_dict.get(f"{trips_no}_lines_long_success", 0) + len(lines_long_success)

	x = ['60', '120', '500', '1000']
	y1 = [res_dict["60_lines_no_other_options"]/50, res_dict["120_lines_no_other_options"]/50, res_dict["500_lines_no_other_options"]/50, res_dict["1000_lines_no_other_options"]/50]
	y2 = [res_dict["60_lines_other_options_not_suitable"]/50, res_dict["120_lines_other_options_not_suitable"]/50, res_dict["500_lines_other_options_not_suitable"]/50, res_dict["1000_lines_other_options_not_suitable"]/50]

	# plot bars in stack manner
	plt.bar(x, y1, color='r')
	plt.bar(x, y2, bottom=y1, color='b')
	plt.xlabel("Number of trip requests")
	plt.ylabel("Number of times long mode stopped because of")
	plt.legend(["No other car options", "Other car options are not suitable"])
	plt.title("Why long mode could not find an alternative")
	plt.savefig(f'./viz/{OUTPUT_FOLDER_NAME}/stacked_bar_chart.jpg')
	plt.show()

	print(res_dict)


if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()
