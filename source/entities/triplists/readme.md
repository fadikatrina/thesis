
The simulation uses 5 triplists;
		request_trip_list       the input trip list
		announced_trip_list     this is what is given to the algorithm, the only difference with request_trip_list is
		                        that some trips are not announced yet
		in_progress_trip_list
		completed_trip_list
		rejected_trip_list

The reason there are 3 classes of triplists is:
        triplist                the trips are automatically sorted by start time
        requesttriplist         the trips are automatically sorted by request time
        inprogresstriplist      the trips are automatically sorted by end time


		request_trip_list           uses        requesttriplist
		announced_trip_list         uses        triplist
		in_progress_trip_list       uses        inprogresstriplist
		completed_trip_list         uses        triplist
		rejected_trip_list          uses        triplistc
