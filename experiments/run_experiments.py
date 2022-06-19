from source.main import Main
import json
from joblib import Parallel, delayed


def start_experiments(experiments=None):
	if experiments is None:
		f = open(f'./experiments/experiments.json')
		experiments = json.load(f)

	# for experiment in experiments:
	# 	run_experiment(experiment)

	Parallel(n_jobs=20)(delayed(run_experiment)(exp) for exp in experiments)
	print("FINISHED ALL EXPERIMENTS")


def run_experiment(experiment):
	for run_no in range(experiment["number_of_runs"]):
		try:
			exp_name = experiment['experiment_name']
			print(f"Now running {run_no} of {exp_name}")
			config = experiment["config"]
			config["algo_config"]["image_filename"] = f"{experiment['experiment_name']}_{run_no}"
			req_filename = config.get("trip_requests_filename")
			if experiment["dynamic_trip_requests_filename"]:
				req_filename = req_filename.replace("$", str(run_no))
			Main(
				algorithm_class=config.get("algorithm_class"),
				trip_requests_filename=req_filename,
				log_filename=f"{config.get('log_filename', exp_name)}_{run_no}",
				output_results_filename=f"{config.get('output_results_filename', exp_name)}_{run_no}",
				check_results_filename=config.get("check_results_filename", 'nothing'),
				general_config_filename=config.get("general_config_filename", 'default'),
				car_charge_config_filename=config.get("car_charge_config_filename", 'default'),
				station_metrics_filename=config.get("station_metrics_filename"),
				algo_config=config.get("algo_config"),
				assign_cars_only_after_all_trips_announced=config.get("assign_cars_only_after_all_trips_announced",
				                                                      False)
			)
			print(f"Completed successfully {run_no} of {exp_name}")
		except Exception as e:
			exp_name = experiment['experiment_name']
			print(f"ERROR RUNNING {run_no} OF {exp_name} ({str(e)})")


if __name__ == "__main__":
	start_experiments()
