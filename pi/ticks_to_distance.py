#!/user/bin/env python
import serial
from serial.tools.list_ports import comports


# connect to the open serial port
ports = [p[0] for p in comports()]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
print("ports: {}".format(ports))

baud_rate = 9600


s1 = serial.Serial(ports[0], baud_rate)
s1.flushInput()
s2 = serial.Serial(ports[1], baud_rate)
s2.flushInput()

distance_per_tick = 22.0/26.0

def ticks_to_distance(ticks):
	return ticks*distance_per_tick

def main(left_ticks, right_ticks):
	left_distance = ticks_to_distance(left_ticks)
	right_distance = ticks_to_distance(right_ticks)
	return left_distance, right_distance

# comp_list = ["Ready? Pi\r\n"]

while True:
	if s1.inWaiting() > 0:
		love = s1.readline().strip()

		# if love in comp_list:
			# message = 
		if len(love.split()) != 2:
			continue

		left_ticks, right_ticks = [int(x) for x in love.split()]
		# print(left_ticks, right_ticks)

		left_distance, right_distance = main(left_ticks, right_ticks)
		print(left_distance, right_distance)

		# n = input("Set arduino flash times:")
		motor_values = ("5", "3")

		s1.write('%d %d', %motor_values)
			# if b in comp_list:
			# 	try:
				# except:
				# 	print("Input error, please input a number")
				# 	s1.write('0')

