import operator


class TripList(list):

    # https://stackoverflow.com/questions/58080700/calling-functions-when-a-list-changes-in-python
    def append(self, value):
        super(TripList, self).append(value)
        self.sort_()

    def sort_(self):
        sort_key = operator.attrgetter("start_time")
        self.sort(key=sort_key, reverse=False)

    def get_trips_without_cars(self):
        trips_without_car = []
        sort_key = operator.attrgetter("car_id")
        self.sort(key=sort_key, reverse=False)
        for trip in self:
            if trip.has_a_car():
                break
            trips_without_car.append(trip)
        self.sort_()
        return trips_without_car
