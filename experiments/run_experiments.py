from src.main import Main
import json
import os


def start_experiments(experiments=None):

	cwd = os.getcwd()
	if cwd[:-3] != "src":
		os.chdir("../src")

	if experiments is None:
		f = open(f'../experiments/experiments.json')
		experiments = json.load(f)

	for experiment in experiments:
		for run_no in range(experiment["number_of_runs"]):
			print(f"Now running {run_no} of {experiment['experiment_name']}")
			config = experiment["config"]
			Main(
				algorithm_class=config["algorithm_class"],
				trip_requests_filename=config["trip_requests_filename"],
				log_filename=f"{config[f'log_filename']}_{run_no}",
				output_results_filename=f"{config[f'output_results_filename']}_{run_no}",
				check_results_filename=config["check_results_filename"],
				general_config_filename=config["general_config_filename"],
				car_charge_config_filename=config["car_charge_config_filename"],
				station_metrics_filename=config["station_metrics_filename"],
				algo_config=config["algo_config"]
			)


if __name__ == "__main__":
	start_experiments()
