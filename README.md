# Thesis

## Simulation Configuration Settings
		algorithm_class="Genetic",                                  // FirstAvailable, Nothing, Manual, ShortMode, LongMode, Genetic
		assign_cars_only_after_all_trips_announced=True,            // this is for testing the algos "offline", so all the trips are announced beforehand and not during the simulation            

		
		// all these filenames need to be in the corresponding folders in a folder called `input` with a certain subdirectory structure, check `input` for examples
		trip_requests_filename="default",                           // list of start station, end station, request time, start time 
		general_config_filename="default",                          // some variables for cars and stations
		car_charge_config_filename="default",                       // if we want specific vehicle ids to have different charge levels
		check_results_filename="nothing",                           // this is for checking that the implementation is correct (also the deterministic algos) checks certain rules at the end of the simulation, for example `car_in_station` or `trip_assigned_car`
		
		station_metrics_filename="google_average_pessimistic",      // the distances and times between stations used in the simulation, options:
		                                                            // `pessimistic` start time dependent, changes throughout the day depending on usual traffic conditions at that time, from google
		                                                            // `best_guess` start time dependent, changes throughout the day depending on usual traffic conditions at that time, from google
		                                                            // `google_average_best_guess` averages from google
		                                                            // `google_average_pessimistic` averages from google
		                                                            // `bristol_metrics_ogpaper` the metrics as calculated in the original paper, not accurate though, because could not reproduce their method fully due to some missing constants in the paper and code

		// these will be created in a folder called `output` in root, during and after the simulation respectively
		log_filename="example",                                     // logs, levels can be configured in `src.helpers.logger`
		output_results_filename="example",                          // writes a summary of all the configs, trips, end stations of the vehicles 

## Algorithms Configuration Settings
### ShortMode
		algo_config={
			"pick_strategy": 2,                             // How to choose a car (from those that do not have any trips and have enough charge)    
			                                                // 0            random
			                                                // 1            most charge
			                                                // 2            least charge
			                                                // 3            balance the charges in the stations
		}
### LongMode
		algo_config={
			"pick_strategy": 2,                              // same as ShortMode
		}
### Genetic
		algo_config={
			"pick_strategy": 2,                             // same as ShortMode
			
			"genetic_eval_strategy": 1,                     // 1    count number of trips assigned
			                                                // 2    count only legal number of trips assigned
			                                                // 3    total duration of trips assigned
			                                                // 4    total duration of legal trips assigned
			                                                // 5    try to maintain the balance of the network
			                                                 
			                                                 
			                                                 of legal trips assigned
			                                                
			"genetic_should_assign_strategy": 1,            // 1    time based strategy for checking if should use genetic again (uses genetic_assign_every_x_seconds)
			                                                // 2    number of trips strategy for checking if should use genetic again (uses genetic_assign_every_x_trips)
			                                                                                                    
			"genetic_assign_every_x_seconds": 3600          // INT  number of simulation seconds to wait for before using genetic algorithm again
			
			"genetic_assign_every_x_trips": 5,              // INT  number of new trips to wait for before using genetic algorithm again
            
            "genetic_select": 1,                            // 1    roulette
            
            "genetic_crossover": 1,                         // 1    single point
			                                                // 2    ordered
			"p_of_crossover":0.1,                           // probability of crossover, double [0,1]                                                
			                                                
			"genetic_mutate": 1,                            // 1    single swap
			                                                // 2    scramble
			"p_of_mutate":0.1,                              // probability of mutate, double [0,1]
			
			"genetic_population_size": 1000
			"genetic_max_iterations": 500
			                                                   
		},
