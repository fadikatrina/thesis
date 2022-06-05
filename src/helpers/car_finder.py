
def pop_from_list(list_, car_id, only_check=False):
	i = 0
	for car in list_:
		if car.id_ == car_id:
			if only_check:
				return
			found_car = list_.pop(i)
			return list_, found_car
		i += 1
	raise RuntimeError(f"Can not find CarID {car_id} in {[str(x) for x in list_]}")
