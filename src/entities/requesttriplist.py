import operator


class RequestTripList(list):

    # https://stackoverflow.com/questions/58080700/calling-functions-when-a-list-changes-in-python
    def append(self, value):
        super(RequestTripList, self).append(value)
        self.sort_()

    def sort_(self):
        sort_key = operator.attrgetter("request_time")
        self.sort(key=sort_key, reverse=False)
