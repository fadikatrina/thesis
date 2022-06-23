import json


def generate():

	for eval_method in [2, 4, 5]:
		experiments = []
		for crossover_method in range(1, 3):
			for mutate_method in range(1, 3):
				for crossover_p in range(11):
					if crossover_p > 1:
						crossover_p = crossover_p / 10
					for mutate_p in range(11):
						if mutate_p > 1:
							mutate_p = mutate_p / 10
						experiments.append({
								"experiment_name": f"gen_hyper_100_{mutate_p}_{crossover_p}_{mutate_method}_{crossover_method}_{eval_method}",
								"number_of_runs": 1,
								"dynamic_trip_requests_filename": False,
								"config": {
									"algorithm_class": "Genetic",
									"trip_requests_filename": f"compact1hr/variant0_routes100",
									"station_metrics_filename": "google_average_pessimistic",
									"general_config_filename" : "og_paper_no_max_capacity",
									"algo_config": {
										"pick_strategy": 3,
										"dont_take_into_account_future_cars_and_charge": False,
										"genetic_eval_strategy": eval_method,
										"genetic_should_assign_strategy": 2,
										"genetic_assign_every_x_trips": 5,
										"genetic_assign_every_x_seconds": 10000,
										"genetic_select": 1,
										"genetic_crossover": crossover_method,
										"p_of_crossover": crossover_p,
										"genetic_mutate": mutate_method,
										"p_of_mutate": mutate_p,
										"genetic_population_size": 400,
										"genetic_max_iterations": 100,
										"genetic_use_long_mode_as_well": False
									}
								}
							})

		with open(f'./experiments_genetic_{eval_method}.json', 'w') as fp:
			json.dump(experiments, fp)


if __name__ == "__main__":
	generate()
