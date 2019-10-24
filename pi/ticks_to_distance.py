distance_per_tick = 22.0/26.0

def tick_to_centimeter(ticks):
	return ticks*distance_per_tick


def get_distances(left_ticks, right_ticks):
	left_distance = tick_to_centimeter(left_ticks)
	right_distance = tick_to_centimeter(right_ticks)
	return left_distance, right_distance

