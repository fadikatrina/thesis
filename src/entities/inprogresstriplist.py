import operator


class InProgressTripList(list):

    # https://stackoverflow.com/questions/58080700/calling-functions-when-a-list-changes-in-python
    def append(self, value):
        super(InProgressTripList, self).append(value)
        self.sort_()

    def sort_(self):
        sort_key = operator.attrgetter("end_time")
        self.sort(key=sort_key, reverse=False)
