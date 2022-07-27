import logging
from pathlib import Path
from os import walk

OUTPUT_FOLDER_NAME = 'best_pick'
PATH_TO_RESULTS = '../results/syncfrom1c/output/results/best_pick_strategy'
# PATH_TO_RESULTS = '../results/syncfrom1b/output/results'
OFFSET = 0
# OFFSET = 3
FILTER_SUBSTRING = 'best_pick_strategy'


def run():
	pick_strategies = [0, 1, 2, 3]
	modes = ['short', 'long']
	no_trips = [60, 120, 500, 1000]

	filenames = next(walk(PATH_TO_RESULTS), (None, None, []))[2]
	filenames = [k for k in filenames if FILTER_SUBSTRING in k]

	for mode in modes:
		print(mode)
		f_mode = [k for k in filenames if mode in k]
		for pick_strategy in pick_strategies:
			f_strat = [k for k in f_mode if pick_strategy == int(k.split("_")[3+OFFSET])]
			perc_avg = []
			no_completed_l = []
			for no_trip in no_trips:
				f_no_trips = [k for k in f_strat if no_trip == int(k.split("_")[4+OFFSET])]
				perc_completed = []
				no_completed = 0
				for f_no_trip in f_no_trips:
					with open(f"{PATH_TO_RESULTS}/{f_no_trip}") as f:
						lines = f.readlines()
						perc_completed.append(float(lines[4].split(" ")[3]))
						no_completed += int(lines[6].split(" ")[3])
						# perc_completed.append(float(lines[3].split(" ")[3]))
				perc_avg.append(sum(perc_completed) / len(perc_completed))
				no_completed_l.append(no_completed)
			print(pick_strategy)
			print(no_completed_l)



if __name__ == "__main__":
	Path(f"./logs").mkdir(parents=True, exist_ok=True)
	Path(f"./viz/{OUTPUT_FOLDER_NAME}").mkdir(parents=True, exist_ok=True)
	logging.basicConfig(filename=f"./logs/{OUTPUT_FOLDER_NAME}.log", level=logging.DEBUG)
	run()


############# RESULTS ALL ANNOUNCED (1C) AVG PERC
# 0
# [0.8997529226839571, 0.833881810999458, 0.7091050410692078, 0.5182255055286463]
# 1
# [0.8997529226839571, 0.833881810999458, 0.7091050410692077, 0.5182255055286462]
# 2
# [0.8997529226839571, 0.833881810999458, 0.7091050410692077, 0.5182255055286463]
# 3
# [0.8997529226839571, 0.833881810999458, 0.7091050410692077, 0.5182255055286463]
# 0
# [0.8997529226839571, 0.833881810999458, 0.7091050410692077, 0.5182255055286464]
# 1
# [0.8997529226839571, 0.833881810999458, 0.7091050410692078, 0.5182255055286463]
# 2
# [0.8997529226839571, 0.833881810999458, 0.7091050410692078, 0.5182255055286463]
# 3
# [0.8997529226839571, 0.833881810999458, 0.7091050410692077, 0.5182255055286463]


############# RESULTS DYNAMIC (1B)
# 0
# [0.9015926662737008, 0.8319891829303593, 0.6588323715673614, 0.46482585132067344]
# 1
# [0.9015926662737008, 0.8319891829303593, 0.6575112655218188, 0.4652604956879367]
# 2
# [0.9015926662737008, 0.8319891829303595, 0.6588740938637566, 0.4658530560944242]
# 3
# [0.9015926662737008, 0.8319891829303595, 0.6586404490039434, 0.46482936934999763]
# 0
# [0.9015926662737008, 0.8319891829303595, 0.6577038404674365, 0.465285701352813]
# 1
# [0.9015926662737008, 0.8319891829303595, 0.6575112655218188, 0.4652604956879367]
# 2
# [0.9015926662737008, 0.8319891829303595, 0.6588740938637565, 0.4658530560944243]
# 3
# [0.9015926662737007, 0.8319891829303593, 0.6586404490039437, 0.46482936934999763]

# NUMBER OF TRIPS
# short
# 0
# [475, 877, 3144, 4580]
# 1
# [475, 877, 3144, 4580]
# 2
# [475, 877, 3144, 4580]
# 3
# [475, 877, 3144, 4580]
# long
# 0
# [475, 877, 3144, 4580]
# 1
# [475, 877, 3144, 4580]
# 2
# [475, 877, 3144, 4580]
# 3
# [475, 877, 3144, 4580]
