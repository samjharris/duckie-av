# CICS 503 Fall 2019 DuckieTown Group 4
# Ticks to Distance
# Function: Covert the number of ticks counted by the wheel encoder into distance(cm)
# Last update: 10/25/2019
import numpy as np

# input:
#		ticks : int, the number of ticks
# return:
#		distance traveled in centimeter(cm)
def tick_to_centimeter(ticks):
	# based on the circumfrance of the wheel and the number of steps on encoder
	# distance_per_tick = 5 / 6 #unit: (cm per tick), experiment yielded 145cm over 174 ticks = 5/6cm per tick
	distance_per_tick = (6.5 * np.pi) / 26 #unit: (cm per tick), experiment yielded 145cm over 174 ticks = 5/6cm per tick

	return ticks*distance_per_tick

# input:
#		left_ticks: int, the number of ticks from the left wheel encoder
#		right_ticks: int, the number of ticks from the right wheel encoder
# return:
#		the distances traveled by each wheel in centimeter(cm)
def get_distances(left_ticks, right_ticks):
	# print("left_ticks, right_ticks : ", left_ticks, right_ticks)
	left_distance = tick_to_centimeter(left_ticks)
	right_distance = tick_to_centimeter(right_ticks)
	# print("left_distance, right_distance : ", left_distance, right_distance)
	return left_distance, right_distance
