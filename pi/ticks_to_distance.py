import serial
import serial.tools.list_ports as list_ports
import struct
import time
import sys

distance_per_tick = 22.0/26.0

def tick_to_centimeter(ticks):
	return ticks*distance_per_tick


def get_distances(left_ticks, right_ticks):
	left_distance = tick_to_centimeter(left_ticks)
	right_distance = tick_to_centimeter(right_ticks)
	return left_distance, right_distance

# sys.path.append('../pi')
# import ticks_to_distance as ticks_to_distance

## connect to the open serial port
ports = list(list_ports.comports())
ports = [p[0] for p in ports]
if len(ports) == 0:
    print("error, couldn't find any open ports")
    exit()
print("found open ports: {}".format(ports))

## set the baud rate - this must match the uno's
baud_rate = 115200
#baud_rate = 9600

##initialize our serial connection
s_con = serial.Serial(ports[0], baud_rate)
s_con.flushInput()

comp_list = ["Motor Values? Pi\r\n"]
##begin control loop
while True:
	if s_con.inWaiting() > 0:

		inputValue = s_con.readline()

		
		# n = input("Set arduino flash times:")
		print(inputValue)
		if inputValue in comp_list:
			try:
				right_value = 20
				left_value = 50

				s_con.write(struct.pack('>BB', right_value, left_value))
			except:
				print("error passing motor values")
				s_con.write('0')


		if len(inputValue.split()) != 2:
			continue

		love = inputValue.strip()
		left_ticks, right_ticks = [int(x) for x in love.split()]
		# print(left_ticks, right_ticks)

		left_distance, right_distance = get_distances(left_ticks, right_ticks)
		print("distances: ", left_distance, right_distance)

		time.sleep(0.2)
