import operator


class TripList(list):

    # def __setitem__(self, key, value):
    #     super(TripList, self).__setitem__(key, value)
    #     self.sort_()
    #     print("The list has been changed!")
    #
    # def __delitem__(self, value):
    #     super(TripList, self).__delitem__(value)
    #     print("The list has been changed!")
    #
    # def __add__(self, value):
    #     super(TripList, self).__add__(value)
    #     self.sort_()
    #     print("The list has been changed!")
    #
    # def __iadd__(self, value):
    #     super(TripList, self).__iadd__(value)
    #     self.sort_()
    #     print("The list has been changed!")

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

    # def remove(self, value):
    #     super(TripList, self).remove(value)
