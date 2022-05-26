
def pop_from_list(list_, car_id):
	i = 0
	for car in list_:
		if car.id_ == car_id:
			found_car = list_.pop(i)
			return list_, found_car
		i += 1
	raise RuntimeError(f"Can not find CarID {car_id} in {list_}")
