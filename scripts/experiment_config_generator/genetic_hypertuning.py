import json


def generate():
	experiments = []

	for eval_method in range(1, 6):
		for crossover_method in range(1, 3):
			for mutate_method in range(1, 3):
				for crossover_p in range(11):
					for mutate_p in range(11):
						for number_of_requests in [60, 120, 500, 1000]:
							crossover_p = crossover_p/10
							mutate_p = mutate_p/10
							experiments.append({
									"experiment_name": f"gen_hyper_{number_of_requests}_{mutate_p}_{crossover_p}_{mutate_method}_{crossover_method}_{eval_method}",
									"number_of_runs": 2,
									"dynamic_trip_requests_filename": True,
									"config": {
										"algorithm_class": "Genetic",
										"trip_requests_filename": f"exp/variant$_routes{number_of_requests}",
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
											"genetic_population_size": 300,
											"genetic_max_iterations": 50
										}
									}
								})

	with open(f'./experiments_genetic.json', 'w') as fp:
		json.dump(experiments, fp)


if __name__ == "__main__":
	generate()
