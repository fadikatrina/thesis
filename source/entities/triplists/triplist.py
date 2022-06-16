import operator


class TripList(list):

    # https://stackoverflow.com/questions/58080700/calling-functions-when-a-list-changes-in-python
    def append(self, value):
        super(TripList, self).append(value)
        self.sort_()

    def sort_(self):
        sort_key = operator.attrgetter("start_time", "end_time")
        # secondary_key = operator.attrgetter("car_id")
        self.sort(key=sort_key, reverse=False)

    def get_trips_without_cars(self):
        return [x for x in self if x.car_id == -1]

    def get_trips_using_car(self, car_id, trip_starts_after_time=0):
        return [x for x in self if (x.car_id == car_id and x.start_time >= trip_starts_after_time)]

    def get_trip_by_id(self, id):
        return [x for x in self if x.id_ == id][0]

