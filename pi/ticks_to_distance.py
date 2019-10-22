#!/user/bin/env python

import serial
import serial.tools.list_ports as list_ports


# connect to the open serial port
ports = list(list_ports.comports())
ports = [p[0] for p in ports]
if len(ports) == 0:
    print("Error, couldn't find any open ports")
    exit()
print("ports: {}".format(ports))

baud_rate = 9600


s1 = serial.Serial(ports[0], baud_rate)
s1.flushInput()

comp_list = ["Flash complete\r\n", "Hello Pi, This is Arduino UNO...\r\n"]

distance_per_tick = 22/26

def ticks_to_distance(ticks):
	return ticks*distance_per_tick

def main(left_ticks, right_ticks):
	left_distance = ticks_to_distance(left_ticks)
	right_distance = ticks_to_distance(right_ticks)
	return left_distance, right_distance

while True:
	if s1.inWaiting() > 0:
		b = s1.read()
		print(b)
		if b in comp_list:
			try:
				n = input("Set arduino flash times:")
				s1.write('%d' % n)
			except:
				print("Input error, please input a number")
				s1.write('0')

