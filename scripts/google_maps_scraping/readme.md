# Google Distance Matrix API
Used to get realistic trip distances and time https://developers.google.com/maps/documentation/distance-matrix/distance-matrix

## Directory
- `call_google.py`          initial approach of scraping weeks in advance (not used anymore)
- `call_google_realtime.py` newer approach of calling google in realtime (currently used in simulation)
- `restructure`             gets the results from `call_google_realtime.py` and restructures them in a way that can be
                            used in simulation and analysis
- `analysis.py`             visualisations and metrics of the google data

## Setup Notes
- An element is the distance and duration between two specific locations 
- There is a limit to 100 elements per request to google (element = number of origins * number of destinations)
- For the bristol dataset, there are 15 locations, for each pair of locations we need the distance time needed, meaning 
we get 210 elements (15*14) per observed_time (observed_time is the predicted duration and distance at a specific departure time)
- Therefore I split the  to 1 station only and destinations into the other 14 stations, which gives 14 elements per request
- Per observed_time 15 requests need to be made, each giving 14 elements, leading to 210 elements
- ~~Observed_time are made at an hourly interval for 2 weeks, 5th to 11th of September 2022, and 6th to 12th March 2023, 
these dates are chosen because there are no national or religious holidays or special events happening close to or
during these weeks, and two different weeks with months apart are chosen to see if there are significant differences in
the time so if more observations are needed or changes need to be made.~~ 
    - The whole first week was scraped and a sample of 1 day and 2 locations from the second week, and there are no 
        differences, the times are identical, therefore a different approach had to be used 
- New approach: scrape in realtime for a few days
- An important parameter to specify is `traffic_model` (more about it in the next section) but the choice is between
    `best_guess`, `pessimistic`, `optimistic` estimates
- Along with the observed_time specific metrics of distance and duration, google provides a average time estimates, 
    these are also stored, because comparing against them would be interesting, and also in the original paper trip 
    generation its only 24 hours so they dont actually take into account any different days like I plan to do

## Extracts from the documentation that are relevant to the decisions made

### [departure_time](https://developers.google.com/maps/documentation/distance-matrix/distance-matrix#departure_time)
Specifies the desired time of departure. You can specify the time as an integer in seconds since midnight, January 1, 1970 UTC. If a departure_time later than 9999-12-31T23:59:59.999999999Z is specified, the API will fall back the departure_time to 9999-12-31T23:59:59.999999999Z. Alternatively, you can specify a value of now, which sets the departure time to the current time (correct to the nearest second). The departure time may be specified in two cases:

- For requests where the travel mode is driving: You can specify the departure_time to receive a route and trip duration (response field: duration_in_traffic) that take traffic conditions into account. The departure_time must be set to the current time or some time in the future. It cannot be in the past.

Notes:
- If departure time is not specified, choice of route and duration are based on road network and average time-independent traffic conditions. Results for a given request may vary over time due to changes in the road network, updated average traffic conditions, and the distributed nature of the service. Results may also vary between nearly-equivalent routes at any time or frequency.
- Distance Matrix requests specifying `departure_time` when `mode=driving` are limited to a maximum of 100 elements per request. The number of origins times the number of destinations defines the number of elements.

### [traffic_model](https://developers.google.com/maps/documentation/distance-matrix/distance-matrix#traffic_model)
Specifies the assumptions to use when calculating time in traffic. This setting affects the value returned in the duration_in_traffic field in the response, which contains the predicted time in traffic based on historical averages. The traffic_model parameter may only be specified for driving directions where the request includes a departure_time. The available values for this parameter are:

- best_guess (default) indicates that the returned duration_in_traffic should be the best estimate of travel time given what is known about both historical traffic conditions and live traffic. Live traffic becomes more important the closer the departure_time is to now.
- pessimistic indicates that the returned duration_in_traffic should be longer than the actual travel time on most days, though occasional days with particularly bad traffic conditions may exceed this value.
- optimistic indicates that the returned duration_in_traffic should be shorter than the actual travel time on most days, though occasional days with particularly good traffic conditions may be faster than this value.

The default value of best_guess will give the most useful predictions for the vast majority of use cases. It is possible the best_guess travel time prediction may be shorter than optimistic, or alternatively, longer than pessimistic, due to the way the best_guess prediction model integrates live traffic information.
