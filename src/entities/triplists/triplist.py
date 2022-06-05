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
        return [x for x in self if x.car_id == -1]

    def get_trips_using_car(self, car_id):
        return [x for x in self if x.car_id == car_id]

    def get_trip_by_id(self, id):
        return [x for x in self if x.id_ == id][0]

